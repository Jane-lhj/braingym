from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User

router = APIRouter()


@router.post("/login")
def login(request: Request, nickname: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.nickname == nickname).first()
    if not user:
        user = User(nickname=nickname)
        db.add(user)
        db.commit()
        db.refresh(user)
    response = RedirectResponse(url=f"/dashboard/{user.id}", status_code=303)
    return response
