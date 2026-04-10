import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.database import Base


def gen_id():
    return uuid.uuid4().hex[:16]


class User(Base):
    __tablename__ = "users"

    id = Column(String(16), primary_key=True, default=gen_id)
    nickname = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    assessments = relationship("Assessment", back_populates="user", order_by="Assessment.created_at.desc()")
    training_records = relationship("TrainingRecord", back_populates="user")


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(String(16), primary_key=True, default=gen_id)
    user_id = Column(String(16), ForeignKey("users.id"), nullable=False)
    scores = Column(JSON, nullable=False)  # {"critical_thinking": 75, "question_framing": 60, ...}
    answers = Column(JSON, nullable=False)  # full answer data
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="assessments")


class TrainingRecord(Base):
    __tablename__ = "training_records"

    id = Column(String(16), primary_key=True, default=gen_id)
    user_id = Column(String(16), ForeignKey("users.id"), nullable=False)
    dimension = Column(String(32), nullable=False)  # critical_thinking / question_framing / creativity
    exercise_type = Column(String(64), nullable=False)
    question_id = Column(String(32), nullable=False)
    user_answer = Column(Text, nullable=False)
    score = Column(Float, nullable=False)
    feedback = Column(Text, nullable=True)
    difficulty = Column(Integer, nullable=False, default=1)  # 1 starter / 2 pro / 3 master
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="training_records")
