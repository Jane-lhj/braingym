from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from urllib.parse import quote

from app.config import TEMPLATES_DIR, DIMENSIONS, SCENE_PRESETS, TRAINING_LEVELS
from app.database import get_db
from app.models import User, TrainingRecord
from app.content.glossary import get_glossary_for_exercise
from app.services.training_fun import build_fun_stats
from app.services.training_unlock import max_unlocked_level, clamp_level
from app.services.training_service import (
    get_dimension_overview,
    get_exercise_question_smart,
    score_exercise,
)

router = APIRouter(prefix="/training")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

_SCENE_MAP = {s["key"]: s for s in SCENE_PRESETS}


def _resolve_scene_hint(scene: str) -> str:
    """Resolve a scene key to its hint text, or treat as custom prompt."""
    if not scene:
        return ""
    preset = _SCENE_MAP.get(scene)
    if preset:
        return preset["hint"]
    return scene


def _exercise_query(level: int, scene: str = "") -> str:
    q = [f"level={int(level)}"]
    if scene:
        q.append("scene=" + quote(scene, safe=""))
    return "?" + "&".join(q)


@router.get("/{user_id}", response_class=HTMLResponse)
def training_home(request: Request, user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return HTMLResponse("用户不存在", status_code=404)

    overviews = {}
    for dim_key in DIMENSIONS:
        overviews[dim_key] = get_dimension_overview(dim_key)

    records = db.query(TrainingRecord).filter(TrainingRecord.user_id == user_id).all()
    stats = {}
    for dim_key in DIMENSIONS:
        dim_records = [r for r in records if r.dimension == dim_key]
        stats[dim_key] = {
            "total": len(dim_records),
            "avg_score": round(sum(r.score for r in dim_records) / len(dim_records)) if dim_records else 0,
        }

    return templates.TemplateResponse("training_home.html", {
        "request": request,
        "user": user,
        "dimensions": DIMENSIONS,
        "overviews": overviews,
        "stats": stats,
        "fun_stats": build_fun_stats(records),
    })


@router.get("/{user_id}/{dimension}", response_class=HTMLResponse)
def training_dimension(
    request: Request,
    user_id: str,
    dimension: str,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return HTMLResponse("用户不存在", status_code=404)
    if dimension not in DIMENSIONS:
        return HTMLResponse("维度不存在", status_code=404)

    overviews = {}
    for dim_key in DIMENSIONS:
        overviews[dim_key] = get_dimension_overview(dim_key)

    records = db.query(TrainingRecord).filter(TrainingRecord.user_id == user_id).all()
    stats = {}
    for dim_key in DIMENSIONS:
        dim_records = [r for r in records if r.dimension == dim_key]
        stats[dim_key] = {
            "total": len(dim_records),
            "avg_score": round(sum(r.score for r in dim_records) / len(dim_records)) if dim_records else 0,
        }

    return templates.TemplateResponse("training_home.html", {
        "request": request,
        "user": user,
        "dimensions": DIMENSIONS,
        "overviews": overviews,
        "stats": stats,
        "selected_dimension": dimension,
        "fun_stats": build_fun_stats(records),
    })


@router.get("/{user_id}/{dimension}/{exercise_type}", response_class=HTMLResponse)
async def exercise_page(
    request: Request,
    user_id: str,
    dimension: str,
    exercise_type: str,
    level: int = 1,
    scene: str = "",
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return HTMLResponse("用户不存在", status_code=404)

    max_u = max_unlocked_level(db, user_id, dimension, exercise_type)
    training_level = clamp_level(level, max_u)

    done_ids = {
        r.question_id
        for r in db.query(TrainingRecord.question_id)
        .filter(
            TrainingRecord.user_id == user_id,
            TrainingRecord.exercise_type == exercise_type,
        )
        .all()
    }

    scene_hint = _resolve_scene_hint(scene)
    question = await get_exercise_question_smart(
        dimension,
        exercise_type,
        done_ids,
        training_level,
        scene_hint=scene_hint,
    )
    if not question:
        return HTMLResponse("未找到练习", status_code=404)

    dim_info = DIMENSIONS.get(dimension, {})
    overview = get_dimension_overview(dimension)
    ex_info = overview["exercises"].get(exercise_type, {}) if overview else {}

    return templates.TemplateResponse("exercise.html", {
        "request": request,
        "user": user,
        "dimension": dimension,
        "dimension_info": dim_info,
        "exercise_type": exercise_type,
        "exercise_info": ex_info,
        "question": question,
        "glossary": get_glossary_for_exercise(exercise_type),
        "scene": scene,
        "scene_presets": SCENE_PRESETS,
        "training_levels": TRAINING_LEVELS,
        "training_level": training_level,
        "max_unlocked_level": max_u,
        "exercise_query": _exercise_query(training_level, scene),
        "exercise_query_level_only": _exercise_query(training_level, ""),
    })


@router.post("/{user_id}/{dimension}/{exercise_type}/submit")
async def submit_exercise(
    request: Request,
    user_id: str,
    dimension: str,
    exercise_type: str,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return HTMLResponse("用户不存在", status_code=404)

    form = await request.form()
    question_id = str(form.get("question_id", ""))
    user_answer = str(form.get("user_answer", ""))
    scene = str(form.get("scene", ""))
    try:
        training_level = int(form.get("training_level") or 1)
    except (TypeError, ValueError):
        training_level = 1
    training_level = max(1, min(3, training_level))
    max_u = max_unlocked_level(db, user_id, dimension, exercise_type)
    training_level = clamp_level(training_level, max_u)

    result = await score_exercise(dimension, exercise_type, question_id, user_answer)

    record = TrainingRecord(
        user_id=user_id,
        dimension=dimension,
        exercise_type=exercise_type,
        question_id=question_id,
        user_answer=user_answer,
        score=result["score"],
        feedback=result.get("feedback", ""),
        difficulty=training_level,
    )
    db.add(record)
    db.commit()

    dim_info = DIMENSIONS.get(dimension, {})
    overview = get_dimension_overview(dimension)
    ex_info = overview["exercises"].get(exercise_type, {}) if overview else {}

    return templates.TemplateResponse("exercise_result.html", {
        "request": request,
        "user": user,
        "dimension": dimension,
        "dimension_info": dim_info,
        "exercise_type": exercise_type,
        "exercise_info": ex_info,
        "result": result,
        "user_answer": user_answer,
        "glossary": get_glossary_for_exercise(exercise_type),
        "scene": scene,
        "training_level": training_level,
        "max_unlocked_level": max_unlocked_level(db, user_id, dimension, exercise_type),
        "exercise_query": _exercise_query(training_level, scene),
        "exercise_query_level_only": _exercise_query(training_level, ""),
    })
