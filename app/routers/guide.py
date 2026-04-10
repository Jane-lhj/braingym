from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import TEMPLATES_DIR, DIMENSIONS
from app.content.dimension_guide import build_guide_sections
from app.database import get_db
from app.models import User

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/guide/{user_id}", response_class=HTMLResponse)
def dimension_guide_page(request: Request, user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return HTMLResponse("用户不存在", status_code=404)

    context = {
        "request": request,
        "user": user,
        "dimensions": DIMENSIONS,
        "sections": build_guide_sections(),
    }
    return templates.TemplateResponse("guide.html", context)
