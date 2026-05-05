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

from app.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, USE_LLM

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

DEBATE_REPLY_SYSTEM_PROMPT = """你是思维训练里的对抗陪练。你的任务不是给标准答案，而是根据用户刚才的回应继续追问。

规则：
1. 必须紧贴用户回应，不要另起话题
2. 用一句反问或追问推动用户补证据、补边界、补标准或补落地动作
3. 不要评价用户好坏，不要给长篇解释
4. 输出 35 字以内中文，只输出追问文本"""

ASSESSMENT_GEN_SYSTEM_PROMPT = """你是健脑房的入馆体测出题专家。请生成 9 道中文开放题，用来评估三种能力：critical_thinking、question_framing、creativity。

要求：
1. 每个维度各 3 题，共 9 题
2. 题目应贴近日常 AI 使用、工作、学习或生活判断
3. 题目不能有唯一标准答案，但必须能根据评分要点评分
4. 难度覆盖 1、2、3
5. 只输出 JSON，不要解释

JSON 格式：
{"questions":[{"dimension":"critical_thinking","prompt":"题干","difficulty":1,"scoring_rubric":{"key_points":["要点1","要点2","要点3"],"max_score":100}}]}"""

DAILY_CHALLENGE_SYSTEM_PROMPT = """你是健脑房每日闯关设计师。请生成一套中文三站式每日挑战。

要求：
1. 必须围绕指定能力维度和场景
2. 三站依次为 quick 快答题、debate 对抗题、reality 现实任务卡
3. debate 站要给出一个“对方说/对方追问”的观点，方便用户来回辩论
4. 每站都要有评分 rubric，方便 AI 后续评分
5. placeholder 只作为“看提示”内容，不要限制用户思路
6. 只输出 JSON，不要解释

JSON 格式：
{"theme":"今日主题","subtitle":"一句副标题","badge":"称号","completion_title":"完成标题","recap":"一句复盘","stations":[{"key":"quick","prompt":"题干","placeholder":"提示","rubric":{"key_points":["要点1","要点2","要点3"],"max_score":100}},{"key":"debate","prompt":"题干","placeholder":"提示","rubric":{"key_points":["要点1","要点2","要点3"],"max_score":100}},{"key":"reality","prompt":"题干","placeholder":"提示","rubric":{"key_points":["要点1","要点2","要点3"],"max_score":100}}]}"""


def _extract_json_object(content: str) -> dict:
    match = re.search(r"\{.*\}", content or "", re.DOTALL)
    if not match:
        return {}
    try:
        return json.loads(match.group())
    except Exception:
        return {}


async def score_open_ended(
    question_prompt: str,
    user_answer: str,
    scoring_rubric: dict,
    use_llm: bool = True,
) -> dict:
    """Score an open-ended answer. Uses LLM if available, otherwise falls back to heuristic."""
    if not (user_answer or "").strip():
        return _empty_submission_result()
    if use_llm and USE_LLM and LLM_API_KEY:
        return await _llm_score(question_prompt, user_answer, scoring_rubric)
    return _heuristic_score(user_answer, scoring_rubric)


def _keyword_matches(text: str, point: str) -> bool:
    answer_lower = (text or "").lower()
    keywords = re.findall(r"[\u4e00-\u9fff]+|[a-zA-Z]{4,}", point or "")
    return any(kw.lower() in answer_lower for kw in keywords if len(kw) >= 2)


def _fallback_debate_reply(user_reply: str, scoring_rubric: dict) -> str:
    key_points = scoring_rubric.get("key_points", []) if scoring_rubric else []
    for point in key_points:
        if not _keyword_matches(user_reply, point):
            clean = re.sub(r"[，。；、,.]+", "，", point).strip("， ")
            clean = clean[:22]
            return f"如果对方追问「{clean}」，你会怎么补上？"

    if any(word in user_reply for word in ["证据", "数据", "来源", "样本", "验证"]):
        return "这些证据里，哪一个最能改变结论？为什么？"
    if any(word in user_reply for word in ["标准", "目标", "定义", "指标"]):
        return "这个标准能被别人判断吗？你会怎么说得更具体？"
    if any(word in user_reply for word in ["场景", "边界", "条件", "情况"]):
        return "边界说清了，那最容易被误用的情况是什么？"

    return "你这句话最强的一点是什么？能把它压成一个追问吗？"


async def generate_assessment_questions(examples_by_dimension: dict) -> list:
    """Generate the full entrance assessment with AI. Falls back in caller if unavailable."""
    if not USE_LLM or not LLM_API_KEY:
        return []

    compact_examples = {}
    for dimension, examples in (examples_by_dimension or {}).items():
        compact_examples[dimension] = [
            {
                "prompt": ex.get("prompt", ""),
                "rubric": ex.get("scoring_rubric", {}),
            }
            for ex in examples[:2]
        ]

    user_msg = (
        "请参考以下旧体测题风格，但生成全新题目，不要照抄。\n\n"
        f"{json.dumps(compact_examples, ensure_ascii=False)}"
    )

    try:
        client = _get_llm_client()
        resp = await client.post(
            f"{LLM_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {LLM_API_KEY}"},
            json={
                "model": LLM_MODEL,
                "messages": [
                    {"role": "system", "content": ASSESSMENT_GEN_SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                ],
                "temperature": 0.72,
                "max_tokens": 2600,
            },
        )
        resp.raise_for_status()
        data = _extract_json_object(resp.json()["choices"][0]["message"]["content"])
    except Exception as e:
        logger.warning("LLM assessment generation failed: %s", e)
        return []

    dimension_names = {
        "critical_thinking": "批判性思维",
        "question_framing": "提问力",
        "creativity": "创造力",
    }
    questions = []
    counts = {key: 0 for key in dimension_names}
    for raw in data.get("questions", []):
        dim = raw.get("dimension")
        prompt = (raw.get("prompt") or "").strip()
        rubric = raw.get("scoring_rubric") or raw.get("rubric") or {}
        if dim not in dimension_names or not prompt:
            continue
        key_points = rubric.get("key_points", [])
        if not key_points:
            continue
        counts[dim] += 1
        questions.append(
            {
                "id": f"ai_assess_{uuid.uuid4().hex[:10]}",
                "dimension": dim,
                "dimension_name": dimension_names[dim],
                "prompt": prompt,
                "difficulty": max(1, min(3, int(raw.get("difficulty") or counts[dim] or 2))),
                "scoring_rubric": {"key_points": key_points[:5], "max_score": 100},
                "ai_generated": True,
            }
        )

    if len(questions) < 9:
        return []
    return questions[:9]


async def generate_daily_challenge(base_challenge: dict, dimension_info: dict = None, scene_info: dict = None) -> dict:
    """Generate a full daily challenge with AI. Falls back in caller if unavailable."""
    if not USE_LLM or not LLM_API_KEY:
        return {}

    dimension_info = dimension_info or {}
    scene_info = scene_info or {}
    base = {
        "dimension": base_challenge.get("dimension"),
        "theme": base_challenge.get("theme"),
        "subtitle": base_challenge.get("subtitle"),
        "stations": [
            {
                "key": s.get("key"),
                "prompt": s.get("prompt"),
                "rubric": s.get("rubric"),
            }
            for s in base_challenge.get("stations", [])
        ],
    }
    scene_text = scene_info.get("hint") or scene_info.get("label") or "默认通用场景"
    user_msg = (
        f"能力维度：{dimension_info.get('name', base_challenge.get('dimension'))}\n"
        f"场景：{scene_text}\n"
        "参考旧挑战结构如下。请生成全新的一套，不要照抄题干。\n\n"
        f"{json.dumps(base, ensure_ascii=False)}"
    )

    try:
        client = _get_llm_client()
        resp = await client.post(
            f"{LLM_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {LLM_API_KEY}"},
            json={
                "model": LLM_MODEL,
                "messages": [
                    {"role": "system", "content": DAILY_CHALLENGE_SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                ],
                "temperature": 0.78,
                "max_tokens": 2200,
            },
        )
        resp.raise_for_status()
        data = _extract_json_object(resp.json()["choices"][0]["message"]["content"])
    except Exception as e:
        logger.warning("LLM daily challenge generation failed: %s", e)
        return {}

    station_names = {
        "quick": ("快答题", "60 秒"),
        "debate": ("对抗题", "2 分钟"),
        "reality": ("现实任务卡", "2 分钟"),
    }
    raw_stations = {s.get("key"): s for s in data.get("stations", []) if isinstance(s, dict)}
    stations = []
    for key in ("quick", "debate", "reality"):
        raw = raw_stations.get(key) or {}
        prompt = (raw.get("prompt") or "").strip()
        rubric = raw.get("scoring_rubric") or raw.get("rubric") or {}
        key_points = rubric.get("key_points", [])
        if not prompt or not key_points:
            return {}
        name, time_hint = station_names[key]
        stations.append(
            {
                "key": key,
                "name": name,
                "time_hint": time_hint,
                "prompt": prompt,
                "placeholder": (raw.get("placeholder") or "可以先写下你的第一反应，再补一个理由。").strip(),
                "rubric": {"key_points": key_points[:5], "max_score": 100},
                "ai_generated": True,
            }
        )

    return {
        "id": f"ai_daily_{uuid.uuid4().hex[:10]}",
        "dimension": base_challenge.get("dimension"),
        "theme": (data.get("theme") or base_challenge.get("theme") or "今日 AI 闯关").strip(),
        "subtitle": (data.get("subtitle") or base_challenge.get("subtitle") or "AI 生成的三站式脑力循环").strip(),
        "badge": (data.get("badge") or base_challenge.get("badge") or "今日训练者").strip(),
        "completion_title": (data.get("completion_title") or base_challenge.get("completion_title") or "AI 每日闯关训练").strip(),
        "recap": (data.get("recap") or base_challenge.get("recap") or "你完成了一次从思考到现实迁移的训练。").strip(),
        "stats": base_challenge.get("stats", []),
        "stations": stations,
        "ai_generated": True,
    }


async def generate_debate_reply(
    debate_prompt: str,
    user_reply: str,
    transcript: str = "",
    scoring_rubric: dict = None,
) -> dict:
    """Generate a contextual debate follow-up. Falls back to a local rubric prompt."""
    answer = (user_reply or "").strip()
    if not answer:
        return {"reply": "先写一句具体回应，我再继续追问。", "source": "fallback"}

    scoring_rubric = scoring_rubric or {}
    if not USE_LLM or not LLM_API_KEY:
        return {"reply": _fallback_debate_reply(answer, scoring_rubric), "source": "fallback"}

    rubric_text = "\n".join(f"- {p}" for p in scoring_rubric.get("key_points", []))
    user_msg = (
        f"## 对抗题\n{debate_prompt}\n\n"
        f"## 评分要点\n{rubric_text}\n\n"
        f"## 已有对话\n{(transcript or '').strip()[-1200:]}\n\n"
        f"## 用户刚才回应\n{answer}"
    )

    try:
        client = _get_llm_client()
        resp = await client.post(
            f"{LLM_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {LLM_API_KEY}"},
            json={
                "model": LLM_MODEL,
                "messages": [
                    {"role": "system", "content": DEBATE_REPLY_SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                ],
                "temperature": 0.45,
                "max_tokens": 120,
            },
        )
        resp.raise_for_status()
        reply = resp.json()["choices"][0]["message"]["content"].strip()
        reply = re.sub(r"^追问[:：]\s*", "", reply).strip()
        if reply:
            return {"reply": reply[:120], "source": "llm"}
    except Exception as e:
        logger.warning("LLM debate reply failed, falling back: %s", e)

    return {"reply": _fallback_debate_reply(answer, scoring_rubric), "source": "fallback"}


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
    if not USE_LLM or not LLM_API_KEY:
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
    if not USE_LLM or not LLM_API_KEY:
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
