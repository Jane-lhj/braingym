"""Assessment (体测) business logic."""

import asyncio
import random
from typing import List, Dict

from app.question_bank.critical_thinking import ASSESSMENT_QUESTIONS as CT_QUESTIONS
from app.question_bank.question_framing import ASSESSMENT_QUESTIONS as QF_QUESTIONS
from app.question_bank.creativity import ASSESSMENT_QUESTIONS as CR_QUESTIONS
from app.config import DIMENSIONS
from app.services.ai_service import generate_assessment_questions, score_open_ended


def enrich_question_display(q: dict) -> dict:
    """Avoid passing nested DIMENSIONS dict into Jinja2 (triggers cache bug on some versions)."""
    meta = DIMENSIONS.get(q.get("dimension", ""), {})
    return {
        **q,
        "dimension_color": meta.get("color", "#666666"),
        "dimension_icon": meta.get("icon", ""),
    }


def enrich_detail_display(d: dict) -> dict:
    meta = DIMENSIONS.get(d.get("dimension", ""), {})
    return {
        **d,
        "dimension_color": meta.get("color", "#666666"),
        "dimension_icon": meta.get("icon", ""),
    }


def get_assessment_questions(shuffle: bool = True) -> List[dict]:
    """Return local assessment examples/fallback questions."""
    questions = []
    for q in CT_QUESTIONS:
        questions.append({**q, "dimension": "critical_thinking", "dimension_name": "批判性思维"})
    for q in QF_QUESTIONS:
        questions.append({**q, "dimension": "question_framing", "dimension_name": "提问力"})
    for q in CR_QUESTIONS:
        questions.append({**q, "dimension": "creativity", "dimension_name": "创造力"})
    if shuffle:
        random.shuffle(questions)
    return questions


async def get_assessment_questions_smart() -> List[dict]:
    """Generate assessment questions with AI; local bank is fallback only."""
    examples = {
        "critical_thinking": CT_QUESTIONS,
        "question_framing": QF_QUESTIONS,
        "creativity": CR_QUESTIONS,
    }
    ai_questions = await generate_assessment_questions(examples)
    if ai_questions:
        return ai_questions
    return get_assessment_questions()


async def score_assessment(answers: dict, questions: List[dict] = None) -> dict:
    """
    Score a complete assessment.
    answers: {question_id: user_answer_string}
    Returns: {"scores": {dimension: score}, "details": [...]}
    """
    questions = questions or get_assessment_questions(shuffle=False)
    q_map = {q["id"]: q for q in questions}

    dim_scores: Dict[str, List[float]] = {
        "critical_thinking": [],
        "question_framing": [],
        "creativity": [],
    }
    details = []

    async def score_one(qid: str, user_answer: str):
        q = q_map.get(qid)
        if not q:
            return None
        result = await score_open_ended(
            q["prompt"],
            user_answer,
            q.get("scoring_rubric", {"key_points": [], "max_score": 100}),
        )
        return {
            "question_id": qid,
            "dimension": q["dimension"],
            "dimension_name": q["dimension_name"],
            "score": result["score"],
            "feedback": result.get("feedback", ""),
            "user_answer": user_answer,
        }

    scored = await asyncio.gather(*(score_one(qid, answer) for qid, answer in answers.items()))
    for item in scored:
        if not item:
            continue
        dim_scores[item["dimension"]].append(item["score"])
        details.append(item)

    final_scores = {}
    for dim, scores_list in dim_scores.items():
        final_scores[dim] = round(sum(scores_list) / len(scores_list)) if scores_list else 0

    return {"scores": final_scores, "details": details}
