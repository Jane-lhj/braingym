"""Lightweight stats: streak and week activity for training."""

from datetime import date, datetime, timedelta
from typing import List, Set, Tuple


def _dates_from_records(records: List[object]) -> Set[date]:
    out: Set[date] = set()
    for r in records:
        ts = getattr(r, "created_at", None)
        if ts is None:
            continue
        if isinstance(ts, datetime):
            out.add(ts.date())
        else:
            out.add(ts)
    return out


def compute_streak_days(active_dates: Set[date], today: date = None) -> int:
    """Consecutive calendar days with training, anchored on today or yesterday."""
    today = today or date.today()
    yesterday = today - timedelta(days=1)
    if today in active_dates:
        anchor = today
    elif yesterday in active_dates:
        anchor = yesterday
    else:
        return 0
    streak = 0
    d = anchor
    while d in active_dates:
        streak += 1
        d -= timedelta(days=1)
    return streak


def week_activity_summary(
    records: List[object],
    today: date = None,
) -> Tuple[int, int]:
    """
    Returns (distinct_days_this_iso_week, sessions_this_week).
    Week = Monday 00:00 .. Sunday (by date).
    """
    today = today or date.today()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    week_days: Set[date] = set()
    sessions = 0
    for r in records:
        ts = getattr(r, "created_at", None)
        if ts is None:
            continue
        d = ts.date() if isinstance(ts, datetime) else ts
        if monday <= d <= sunday:
            week_days.add(d)
            sessions += 1
    return len(week_days), sessions


def build_fun_stats(records: List[object]) -> dict:
    """Dashboard-friendly bundle."""
    dates = _dates_from_records(records)
    streak = compute_streak_days(dates)
    week_days, week_sessions = week_activity_summary(records)
    return {
        "streak_days": streak,
        "week_active_days": week_days,
        "week_sessions": week_sessions,
    }
