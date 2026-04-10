"""Per-exercise training difficulty unlock (score-based, not pass/fail)."""

from collections import defaultdict
from typing import List

from sqlalchemy.orm import Session

from app.config import TRAINING_LEVELS
from app.models import TrainingRecord


def _avg(scores: List[float]) -> float:
    return sum(scores) / len(scores) if scores else 0.0


def max_unlocked_level(
    db: Session,
    user_id: str,
    dimension: str,
    exercise_type: str,
) -> int:
    """Return highest difficulty level (1–3) the user may pick for this exercise."""
    records = (
        db.query(TrainingRecord)
        .filter(
            TrainingRecord.user_id == user_id,
            TrainingRecord.dimension == dimension,
            TrainingRecord.exercise_type == exercise_type,
        )
        .all()
    )
    by_level: dict = defaultdict(list)
    for r in records:
        d = getattr(r, "difficulty", None) or 1
        by_level[d].append(float(r.score))

    unlocked = 1
    for tier in TRAINING_LEVELS[1:]:
        prev = tier["level"] - 1
        prev_scores = by_level.get(prev, [])
        need_n = tier.get("unlock_min_attempts_prev", 2)
        need_avg = tier.get("unlock_min_avg_prev", 55)
        if len(prev_scores) >= need_n and _avg(prev_scores) >= need_avg:
            unlocked = tier["level"]
        else:
            break
    return unlocked


def clamp_level(requested: int, unlocked: int) -> int:
    r = max(1, min(3, int(requested or 1)))
    return min(r, unlocked)
