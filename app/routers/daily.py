import json
import asyncio
from urllib.parse import quote

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import DIMENSIONS, SCENE_PRESETS, TEMPLATES_DIR
from app.content.daily_challenges import get_daily_challenge, get_daily_challenge_by_id
from app.database import get_db
from app.models import TrainingRecord, User
from app.services.ai_service import generate_daily_challenge, generate_debate_reply, score_open_ended

router = APIRouter(prefix="/daily")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
_SCENE_MAP = {s["key"]: s for s in SCENE_PRESETS}
_DAILY_CHALLENGE_CACHE = {}


def _resolve_scene(scene: str) -> dict:
    value = (scene or "").strip()[:80]
    if not value:
        return {"key": "", "label": "", "hint": "", "query": ""}

    preset = _SCENE_MAP.get(value)
    if preset:
        return {
            "key": value,
            "label": preset["name"],
            "hint": preset["hint"],
            "query": "?scene=" + quote(value, safe=""),
        }

    return {
        "key": value,
        "label": value,
        "hint": value,
        "query": "?scene=" + quote(value, safe=""),
    }


def _completion_score(text: str) -> dict:
    answer = (text or "").strip()
    if not answer:
        return {
            "score": 0,
            "feedback": "这站还没作答，先写下一个小想法也算启动。",
        }

    score = 45 + min(35, len(answer) // 4)
    if any(mark in answer for mark in ["1.", "2.", "①", "②", "第一", "第二", "：", ":"]):
        score += 10
    if len(answer) >= 80:
        score += 10
    score = min(100, score)

    return {
        "score": score,
        "feedback": "你把今日任务落到了真实场景里，这一步最容易把练习变成习惯。",
    }


async def _score_station(station: dict, answer: str) -> dict:
    rubric = station.get("rubric") or {
        "key_points": ["回答具体", "能回应题目要求", "能连接真实场景"],
        "max_score": 100,
    }
    return await score_open_ended(station["prompt"], answer, rubric)


@router.get("/{user_id}", response_class=HTMLResponse)
async def daily_page(request: Request, user_id: str, scene: str = "", db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return HTMLResponse("用户不存在", status_code=404)

    base_challenge = get_daily_challenge()
    dimension_info = DIMENSIONS.get(base_challenge["dimension"], {})
    scene_info = _resolve_scene(scene)
    challenge = await generate_daily_challenge(base_challenge, dimension_info, scene_info)
    if not challenge:
        challenge = base_challenge
    _DAILY_CHALLENGE_CACHE[challenge["id"]] = challenge
    context = {
        "request": request,
        "user": user,
        "challenge": challenge,
        "challenge_payload": json.dumps(challenge, ensure_ascii=False),
        "dimension_info": dimension_info,
        "scene": scene_info["key"],
        "scene_info": scene_info,
        "scene_presets": SCENE_PRESETS,
        "debate_seconds": 120,
    }
    return templates.TemplateResponse("daily.html", context)


def _challenge_from_payload(payload: str) -> dict:
    if not payload:
        return {}
    try:
        challenge = json.loads(payload)
    except Exception:
        return {}
    if isinstance(challenge, dict) and challenge.get("id") and challenge.get("stations"):
        _DAILY_CHALLENGE_CACHE[challenge["id"]] = challenge
        return challenge
    return {}


def _get_daily_challenge(challenge_id: str) -> dict:
    return _DAILY_CHALLENGE_CACHE.get(challenge_id) or get_daily_challenge_by_id(challenge_id)


@router.post("/{user_id}/debate-reply")
async def debate_reply(request: Request, user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return JSONResponse({"reply": "用户不存在", "source": "fallback"}, status_code=404)

    form = await request.form()
    challenge_id = str(form.get("challenge_id", ""))
    user_reply = str(form.get("message", ""))
    transcript = str(form.get("transcript", ""))
    challenge = _get_daily_challenge(challenge_id)
    debate_station = next(
        (station for station in challenge["stations"] if station.get("key") == "debate"),
        challenge["stations"][1],
    )
    result = await generate_debate_reply(
        debate_station["prompt"],
        user_reply,
        transcript=transcript,
        scoring_rubric=debate_station.get("rubric", {}),
    )
    return JSONResponse(result)


@router.post("/{user_id}/submit", response_class=HTMLResponse)
async def submit_daily(request: Request, user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return HTMLResponse("用户不存在", status_code=404)

    form = await request.form()
    challenge_id = str(form.get("challenge_id", ""))
    challenge = _challenge_from_payload(str(form.get("challenge_payload", ""))) or _get_daily_challenge(challenge_id)
    dimension_info = DIMENSIONS.get(challenge["dimension"], {})

    answers = {
        "quick": str(form.get("quick_answer", "")),
        "debate": str(form.get("debate_answer", "")),
        "reality": str(form.get("reality_answer", "")),
    }
    scene_info = _resolve_scene(str(form.get("scene", "")))

    async def score_station_for_result(station: dict) -> dict:
        key = station["key"]
        answer = answers.get(key, "")
        result = await _score_station(station, answer)
        return {
            "key": key,
            "name": station["name"],
            "answer": answer,
            "score": int(result.get("score", 0)),
            "feedback": result.get("feedback", ""),
        }

    station_results = await asyncio.gather(*(score_station_for_result(station) for station in challenge["stations"]))

    final_score = round(sum(r["score"] for r in station_results) / len(station_results))
    stored_answer = {
        "challenge_id": challenge["id"],
        "theme": challenge["theme"],
        "scene": scene_info["key"],
        "scene_label": scene_info["label"],
        "answers": answers,
        "station_scores": {r["key"]: r["score"] for r in station_results},
    }
    feedback = f"今日完成：{challenge['completion_title']}\n称号：{challenge['badge']}\n{challenge['recap']}"

    record = TrainingRecord(
        user_id=user_id,
        dimension=challenge["dimension"],
        exercise_type="daily_challenge",
        question_id=challenge["id"],
        user_answer=json.dumps(stored_answer, ensure_ascii=False),
        score=final_score,
        feedback=feedback,
        difficulty=1,
    )
    db.add(record)
    db.commit()

    context = {
        "request": request,
        "user": user,
        "challenge": challenge,
        "dimension_info": dimension_info,
        "scene": scene_info["key"],
        "scene_info": scene_info,
        "station_results": station_results,
        "final_score": final_score,
    }
    return templates.TemplateResponse("daily_result.html", context)
