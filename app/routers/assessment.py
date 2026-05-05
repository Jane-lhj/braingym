import json

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import TEMPLATES_DIR, DIMENSIONS_LIST
from app.database import get_db
from app.models import User, Assessment
from app.services.assessment_service import (
    get_assessment_questions_smart,
    score_assessment,
    enrich_question_display,
    enrich_detail_display,
)

router = APIRouter(prefix="/assessment")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/{user_id}", response_class=HTMLResponse)
async def assessment_page(request: Request, user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return HTMLResponse("用户不存在", status_code=404)
    raw_questions = await get_assessment_questions_smart()
    questions = [enrich_question_display(q) for q in raw_questions]
    context = {
        "request": request,
        "user": user,
        "questions": questions,
        "questions_payload": json.dumps(raw_questions, ensure_ascii=False),
        "dimensions_list": DIMENSIONS_LIST,
    }
    return templates.TemplateResponse("assessment.html", context)


@router.post("/{user_id}/submit")
async def submit_assessment(request: Request, user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return HTMLResponse("用户不存在", status_code=404)

    form = await request.form()
    answers = {}
    for key, value in form.items():
        if key.startswith("answer_"):
            qid = key.replace("answer_", "")
            answers[qid] = str(value)
    try:
        questions = json.loads(str(form.get("questions_payload", "")))
    except Exception:
        questions = None

    result = await score_assessment(answers, questions)

    assessment = Assessment(
        user_id=user_id,
        scores=result["scores"],
        answers=[
            {"question_id": d["question_id"], "answer": d["user_answer"], "score": d["score"]}
            for d in result["details"]
        ],
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    details = [enrich_detail_display(d) for d in result["details"]]
    context = {
        "request": request,
        "user": user,
        "scores": result["scores"],
        "details": details,
        "dimensions_list": DIMENSIONS_LIST,
        "assessment_id": assessment.id,
    }
    return templates.TemplateResponse("assessment_result.html", context)
