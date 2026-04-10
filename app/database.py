from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import DATABASE_URL


def _ensure_sqlite_parent_dir(url: str) -> None:
    if not url.startswith("sqlite"):
        return
    u = make_url(url)
    if not u.database or u.database == ":memory:":
        return
    Path(u.database).parent.mkdir(parents=True, exist_ok=True)


_ensure_sqlite_parent_dir(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _migrate_sqlite() -> None:
    if not str(DATABASE_URL).startswith("sqlite"):
        return
    with engine.connect() as conn:
        rows = conn.execute(text("PRAGMA table_info(training_records)")).fetchall()
        col_names = {r[1] for r in rows}
        if "difficulty" not in col_names:
            conn.execute(text("ALTER TABLE training_records ADD COLUMN difficulty INTEGER DEFAULT 1"))
            conn.execute(text("UPDATE training_records SET difficulty = 1 WHERE difficulty IS NULL"))
            conn.commit()


def init_db():
    Base.metadata.create_all(bind=engine)
    _migrate_sqlite()
