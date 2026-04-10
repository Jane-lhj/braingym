"""
AI service: scoring, question generation, and reference answer generation.
Uses DeepSeek (or any OpenAI-compatible API) with a rule-based fallback.
"""

import json
import re
import logging
import uuid
from typing import Optional

import httpx

from app.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL

logger = logging.getLogger(__name__)

_llm_client: Optional[httpx.AsyncClient] = None


def _get_llm_client() -> httpx.AsyncClient:
    """Reuse keep-alive connections across LLM calls (saves TLS + TCP per request)."""
    global _llm_client
    if _llm_client is None or _llm_client.is_closed:
        _llm_client = httpx.AsyncClient(
            timeout=httpx.Timeout(40.0, connect=10.0),
            limits=httpx.Limits(max_keepalive_connections=8, max_connections=20),
        )
    return _llm_client


async def aclose_llm_client() -> None:
    global _llm_client
    if _llm_client is not None and not _llm_client.is_closed:
        await _llm_client.aclose()
    _llm_client = None


SCORING_SYSTEM_PROMPT = """你是思维训练评分专家。根据题目、评分要点与用户回答打分。

硬性规则：若用户未作答、只有空白或仅「不知道」「无」等无效内容，score 必须为 0，feedback 说明未作答即可。

否则 score 为 0-100 整数；feedback 为一段「小结」（≤180字），必须依次包含且仅出现这两行开头：
【亮点】具体写 1-3 句
【可改进】具体写 1-3 句

仅输出 JSON，不要其他文字：
{"score": <整数>, "feedback": "<字符串>"}"""


def empty_answer_result() -> dict:
    """Public alias for routes/services that skip LLM on blank submissions."""
    return _empty_submission_result()


def _empty_submission_result() -> dict:
    return {
        "score": 0,
        "feedback": "【亮点】（未作答）\n【可改进】请填写有效回答后再提交。",
    }


def _normalize_scoring_dict(data: dict, user_answer: str) -> dict:
    """Single feedback field; merge legacy highlights/gaps into one summary."""
    if not (user_answer or "").strip():
        return _empty_submission_result()
    try:
        score = int(data.get("score", 0))
    except (TypeError, ValueError):
        score = 0
    score = max(0, min(100, score))
    feedback = (data.get("feedback") or "").strip()
    highlights = (data.get("highlights") or "").strip()
    gaps = (data.get("gaps") or "").strip()
    if not feedback and (highlights or gaps):
        feedback = f"【亮点】{highlights or '暂无'}\n【可改进】{gaps or '暂无'}"
    if not feedback:
        feedback = "【亮点】（解析暂缺）\n【可改进】可再对照题目补充论述。"
    return {"score": score, "feedback": feedback}

QUESTION_GEN_SYSTEM_PROMPT = """你是一个思维训练出题专家。请根据给定的练习类型和示例，生成一道新的开放式训练题目。

要求：
1. 题目风格和难度与示例相似，但内容必须是全新的
2. 题目应该有明确的思考方向，但没有唯一标准答案
3. 贴近日常生活或工作场景，让人有代入感

请严格按以下 JSON 格式返回（不要包含其他内容）：
{"passage": "<阅读材料/场景描述，如果不需要可以留空字符串>", "prompt": "<具体问题>", "scoring_rubric": {"key_points": ["要点1", "要点2", "要点3"], "max_score": 100}}"""

# Shorter prompt when scene is set: fewer input tokens -> faster API round-trip
QUESTION_GEN_SCENE_SYSTEM_PROMPT = """根据练习说明与指定场景，生成一道全新开放式训练题。材料精炼、问题明确、无唯一标准答案。
仅输出 JSON，无其他文字：
{"passage":"","prompt":"","scoring_rubric":{"key_points":["","",""],"max_score":100}}"""

REFERENCE_ANSWER_SYSTEM_PROMPT = """你是一个思维训练的优秀答题者。请根据题目和评分要点，写一份高质量的参考答案。

要求：
1. 覆盖主要评分要点
2. 逻辑清晰、论证有力
3. 控制在 200 字以内
4. 用分点或段落组织，易于阅读

直接输出答案文本，不需要任何 JSON 格式或额外标记。"""


async def score_open_ended(
    question_prompt: str,
    user_answer: str,
    scoring_rubric: dict,
) -> dict:
    """Score an open-ended answer. Uses LLM if available, otherwise falls back to heuristic."""
    if not (user_answer or "").strip():
        return _empty_submission_result()
    if LLM_API_KEY:
        return await _llm_score(question_prompt, user_answer, scoring_rubric)
    return _heuristic_score(user_answer, scoring_rubric)


async def _llm_score(
    question_prompt: str,
    user_answer: str,
    scoring_rubric: dict,
) -> dict:
    if not (user_answer or "").strip():
        return _empty_submission_result()

    key_points = scoring_rubric.get("key_points", [])
    rubric_text = "\n".join(f"- {p}" for p in key_points)

    user_msg = (
        f"## 题目\n{question_prompt}\n\n"
        f"## 评分要点\n{rubric_text}\n\n"
        f"## 用户回答\n{user_answer}"
    )

    try:
        client = _get_llm_client()
        resp = await client.post(
            f"{LLM_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {LLM_API_KEY}"},
            json={
                "model": LLM_MODEL,
                "messages": [
                    {"role": "system", "content": SCORING_SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                ],
                "temperature": 0.25,
                "max_tokens": 400,
            },
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            raw = json.loads(match.group())
            return _normalize_scoring_dict(raw, user_answer)
    except Exception as e:
        logger.warning("LLM scoring failed, falling back to heuristic: %s", e)

    return _heuristic_score(user_answer, scoring_rubric)


def _heuristic_score(user_answer: str, scoring_rubric: dict) -> dict:
    """Simple keyword-matching heuristic when LLM is unavailable."""
    key_points = scoring_rubric.get("key_points", [])
    if not key_points or not user_answer.strip():
        return _empty_submission_result()

    answer_lower = user_answer.lower()
    matched = 0
    matched_points = []
    missed_points = []

    for point in key_points:
        keywords = re.findall(r"[\u4e00-\u9fff]+", point)
        if any(kw in answer_lower for kw in keywords if len(kw) >= 2):
            matched += 1
            matched_points.append(point)
        else:
            missed_points.append(point)

    base_score = int((matched / len(key_points)) * 70)
    length_bonus = min(20, len(user_answer) // 20)
    structure_bonus = 10 if any(c in user_answer for c in ["1.", "2.", "①", "一、", "首先"]) else 0

    score = min(100, base_score + length_bonus + structure_bonus)

    hi = "你覆盖了部分评分要点。" if matched_points else "（关键词匹配较少，建议对照题目再展开）"
    if matched_points and matched_points[0]:
        hi = matched_points[0][:100]
    gap = missed_points[0][:120] if missed_points else "保持分点作答会更清晰。"
    return {
        "score": score,
        "feedback": f"【亮点】{hi}\n【可改进】{gap}",
    }


_DIFFICULTY_HINTS = {
    1: "难度【入门】：材料简短，问题直白，适合热身。",
    2: "难度【进阶】：材料适中，要求多角度分析或对比。",
    3: "难度【挑战】：材料可更长，推理链更深，可含多个主张需辨析。",
}


async def generate_question(
    exercise_meta: dict,
    examples: list,
    scene_hint: str = "",
    difficulty_level: int = 1,
) -> dict:
    """Generate a new open-ended question using LLM, based on exercise metadata and examples."""
    if not LLM_API_KEY:
        return {}

    tier = max(1, min(3, int(difficulty_level or 1)))
    # With scene: one short few-shot + tight output cap -> faster model response
    ex_limit = 1 if scene_hint else 2
    max_tokens = 700 if scene_hint else 1000
    if tier >= 3:
        max_tokens = min(max_tokens + 200, 1200)
    temperature = 0.72 if scene_hint else 0.8
    system_prompt = QUESTION_GEN_SCENE_SYSTEM_PROMPT if scene_hint else QUESTION_GEN_SYSTEM_PROMPT

    examples_text = ""
    for i, ex in enumerate(examples[:ex_limit], 1):
        passage = ex.get("passage", ex.get("scenario", ""))
        prompt = ex.get("prompt", ex.get("question", ""))
        examples_text += f"\n### 示例{i}\n材料: {passage}\n问题: {prompt}\n"

    scene_instruction = ""
    if scene_hint:
        scene_instruction = f"\n场景：{scene_hint}\n"

    diff_line = _DIFFICULTY_HINTS.get(tier, _DIFFICULTY_HINTS[1])

    user_msg = (
        f"## 练习\n{exercise_meta['name']}：{exercise_meta['description']}\n"
        f"{diff_line}\n"
        f"{examples_text}"
        f"{scene_instruction}"
        f"请生成一道全新题目。"
    )

    try:
        client = _get_llm_client()
        resp = await client.post(
            f"{LLM_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {LLM_API_KEY}"},
            json={
                "model": LLM_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_msg},
                ],
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            q = json.loads(match.group())
            return {
                "id": f"ai_{uuid.uuid4().hex[:8]}",
                "type": "open_ended",
                "passage": q.get("passage", ""),
                "prompt": q.get("prompt", ""),
                "scoring_rubric": q.get("scoring_rubric", {"key_points": [], "max_score": 100}),
                "ai_generated": True,
            }
    except Exception as e:
        logger.warning("LLM question generation failed: %s", e)

    return {}


async def generate_reference_answer(question_prompt: str, scoring_rubric: dict) -> str:
    """Generate a high-quality reference answer using LLM."""
    if not LLM_API_KEY:
        return ""

    key_points = scoring_rubric.get("key_points", [])
    rubric_text = "\n".join(f"- {p}" for p in key_points)

    user_msg = f"## 题目\n{question_prompt}\n\n## 评分要点\n{rubric_text}"

    try:
        client = _get_llm_client()
        resp = await client.post(
            f"{LLM_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {LLM_API_KEY}"},
            json={
                "model": LLM_MODEL,
                "messages": [
                    {"role": "system", "content": REFERENCE_ANSWER_SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                ],
                "temperature": 0.5,
                "max_tokens": 400,
            },
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logger.warning("LLM reference answer generation failed: %s", e)

    return ""
