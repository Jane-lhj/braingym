"""Training Zone (器械区) business logic."""

import asyncio
import random
from collections import defaultdict
from typing import Optional, Set

from app.question_bank.critical_thinking import ALL_EXERCISES as CT_EXERCISES
from app.question_bank.question_framing import ALL_EXERCISES as QF_EXERCISES
from app.question_bank.creativity import ALL_EXERCISES as CR_EXERCISES
from app.services.ai_service import (
    score_open_ended,
    generate_question,
    generate_reference_answer,
    empty_answer_result,
)

DIMENSION_EXERCISES = {
    "critical_thinking": CT_EXERCISES,
    "question_framing": QF_EXERCISES,
    "creativity": CR_EXERCISES,
}

# In-memory: AI-generated questions by id (for scoring)
_ai_question_cache: dict = {}
# Reuse recent AI questions per (dimension, exercise, scene, difficulty) to cut latency
_AI_POOLS: dict = defaultdict(list)
_POOL_MAX = 8


def get_dimension_overview(dimension: str) -> Optional[dict]:
    exercises = DIMENSION_EXERCISES.get(dimension)
    if not exercises:
        return None
    return {
        "dimension": dimension,
        "exercises": {
            key: {
                "name": ex["name"],
                "icon": ex["icon"],
                "description": ex["description"],
            }
            for key, ex in exercises.items()
        },
    }


def _pool_key(
    dimension: str,
    exercise_type: str,
    scene_hint: str,
    difficulty: Optional[int],
) -> str:
    d = difficulty if difficulty is not None else 0
    return f"{dimension}\t{exercise_type}\t{scene_hint or ''}\t{d}"


def _pool_take(key: str, done_ids: Optional[Set[str]]) -> Optional[dict]:
    pool = _AI_POOLS[key]
    done = done_ids or set()
    usable = [q for q in pool if q.get("id") not in done]
    if usable:
        return random.choice(usable)
    return None


def _pool_push(key: str, q: dict) -> None:
    pool = _AI_POOLS[key]
    existing = {x.get("id") for x in pool}
    if q.get("id") and q["id"] not in existing:
        pool.append(q)
    while len(pool) > _POOL_MAX:
        pool.pop(0)


def get_exercise_question_sync(
    dimension: str,
    exercise_type: str,
    done_ids: Optional[Set[str]] = None,
    difficulty: Optional[int] = None,
) -> Optional[dict]:
    """Pick a question the user hasn't done yet; returns None if pool exhausted."""
    exercises = DIMENSION_EXERCISES.get(dimension, {})
    exercise = exercises.get(exercise_type)
    if not exercise:
        return None

    questions = exercise["questions"]
    if difficulty is not None:
        filtered = [q for q in questions if q.get("difficulty", 1) == difficulty]
        questions = filtered if filtered else questions

    if done_ids:
        unseen = [q for q in questions if q["id"] not in done_ids]
        if unseen:
            return random.choice(unseen)
        return None

    return random.choice(questions)


async def get_exercise_question_smart(
    dimension: str,
    exercise_type: str,
    done_ids: Optional[Set[str]] = None,
    difficulty: Optional[int] = None,
    scene_hint: str = "",
) -> Optional[dict]:
    """Pool-first, AI pool reuse, then AI generate. Force AI path when scene_hint is set."""
    exercises = DIMENSION_EXERCISES.get(dimension, {})
    exercise = exercises.get(exercise_type)
    if not exercise:
        return None

    tier = difficulty if difficulty is not None else 1
    key = _pool_key(dimension, exercise_type, scene_hint, tier)

    if not scene_hint:
        q = get_exercise_question_sync(dimension, exercise_type, done_ids, difficulty)
        if q is not None:
            return q

    cached = _pool_take(key, done_ids)
    if cached:
        _ai_question_cache[cached["id"]] = cached
        return cached

    meta = {"name": exercise["name"], "description": exercise["description"]}
    ai_q = await generate_question(
        meta,
        exercise["questions"],
        scene_hint=scene_hint,
        difficulty_level=tier,
    )
    if ai_q and ai_q.get("prompt"):
        _ai_question_cache[ai_q["id"]] = ai_q
        _pool_push(key, ai_q)
        return ai_q

    return random.choice(exercise["questions"]) if exercise["questions"] else None


async def score_exercise(
    dimension: str,
    exercise_type: str,
    question_id: str,
    user_answer: str,
) -> dict:
    """Score a training exercise and generate an AI reference answer."""
    if not (user_answer or "").strip():
        return empty_answer_result()

    exercises = DIMENSION_EXERCISES.get(dimension, {})
    exercise = exercises.get(exercise_type)

    q = None
    if exercise:
        for question in exercise["questions"]:
            if question["id"] == question_id:
                q = question
                break
    if not q:
        q = _ai_question_cache.get(question_id)
    if not q:
        return {"score": 0, "feedback": "【亮点】（无）\n【可改进】未找到对应题目，请返回训练区重试。"}

    prompt_text = q.get("prompt", q.get("question", ""))
    rubric = q.get("scoring_rubric", {"key_points": [], "max_score": 100})

    score_task = score_open_ended(prompt_text, user_answer, rubric)
    ref_task = generate_reference_answer(prompt_text, rubric)
    result, ai_answer = await asyncio.gather(score_task, ref_task)

    if ai_answer:
        result["ai_answer"] = ai_answer
    example = q.get("example_good_answer", "")
    if example and not result.get("ai_answer"):
        result["ai_answer"] = example

    return result
