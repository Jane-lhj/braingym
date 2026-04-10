from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import TEMPLATES_DIR, STATIC_DIR, DIMENSIONS, DIMENSIONS_LIST
from app.database import init_db, get_db
from app.models import User
from app.routers import user, assessment, training, guide
from app.services import ai_service

app = FastAPI(title="健脑房 BrainGym")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/health")
def health():
    """For deployment probes (Render / Fly / k8s)."""
    return {"status": "ok"}


app.include_router(user.router)
app.include_router(guide.router)
app.include_router(assessment.router)
app.include_router(training.router)


@app.get("/classroom/{user_id}")
def legacy_classroom_home(user_id: str):
    return RedirectResponse(url=f"/guide/{user_id}", status_code=302)


@app.get("/classroom/{user_id}/{rest:path}")
def legacy_classroom_nested(user_id: str, rest: str):
    first = rest.split("/")[0]
    if first in DIMENSIONS:
        return RedirectResponse(url=f"/guide/{user_id}#{first}", status_code=302)
    return RedirectResponse(url=f"/guide/{user_id}", status_code=302)


templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.on_event("startup")
def on_startup():
    init_db()


@app.on_event("shutdown")
async def on_shutdown():
    await ai_service.aclose_llm_client()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "dimensions_list": DIMENSIONS_LIST}
    )


@app.get("/dashboard/{user_id}", response_class=HTMLResponse)
def dashboard(request: Request, user_id: str):
    db = next(get_db())
    user_obj = db.query(User).filter(User.id == user_id).first()
    db.close()
    if not user_obj:
        return HTMLResponse("用户不存在", status_code=404)

    from app.models import Assessment, TrainingRecord

    db = next(get_db())
    all_assessments = (
        db.query(Assessment)
        .filter(Assessment.user_id == user_id)
        .order_by(Assessment.created_at.asc())
        .all()
    )
    records = db.query(TrainingRecord).filter(TrainingRecord.user_id == user_id).all()
    db.close()

    latest_assessment = all_assessments[-1] if all_assessments else None
    scores = latest_assessment.scores if latest_assessment else None

    score_history = []
    for a in all_assessments:
        score_history.append({
            "date": a.created_at.strftime("%m/%d"),
            "scores": a.scores,
        })

    training_stats = {}
    for dim_key in DIMENSIONS:
        dim_records = [r for r in records if r.dimension == dim_key]
        training_stats[dim_key] = {
            "total": len(dim_records),
            "avg_score": round(sum(r.score for r in dim_records) / len(dim_records)) if dim_records else 0,
        }

    from app.services.training_fun import build_fun_stats

    fun_stats = build_fun_stats(records)

    return templates.TemplateResponse(
        "dashboard.html",
        context={
            "request": request,
            "user": user_obj,
            "scores": scores,
            "score_history": score_history,
            "training_stats": training_stats,
            "dimensions": DIMENSIONS,
            "total_training": len(records),
            "fun_stats": fun_stats,
        }
    )
