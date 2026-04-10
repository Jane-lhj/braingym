import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
# override=True: shell 里若误设了空的 LLM_API_KEY，仍以 .env 为准
load_dotenv(BASE_DIR / ".env", override=True)
DB_PATH = BASE_DIR / "braingym.db"
# Allow override e.g. Docker volume: sqlite:////data/braingym.db
DATABASE_URL = os.getenv("DATABASE_URL") or f"sqlite:///{DB_PATH}"

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
STATIC_DIR = Path(__file__).resolve().parent / "static"

LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")

SCENE_PRESETS = [
    {"key": "daily", "name": "生活日常", "icon": "🏠", "hint": "用日常消费、社交、家庭、出行等生活场景出题"},
    {"key": "work", "name": "职场实战", "icon": "💼", "hint": "用开会、汇报、团队协作、绩效等职场场景出题"},
    {"key": "trending", "name": "社会热点", "icon": "🔥", "hint": "用近期新闻、科技趋势、社会议题出题"},
    {"key": "academic", "name": "学术硬核", "icon": "🎓", "hint": "用论文、实验设计、学术辩论、数据分析场景出题"},
]

DIMENSIONS = {
    "critical_thinking": {"name": "批判性思维", "icon": "🔍", "color": "#EF4444"},
    "question_framing": {"name": "提问力", "icon": "🎯", "color": "#3B82F6"},
    "creativity": {"name": "创造力", "icon": "💡", "color": "#8B5CF6"},
}

# Training difficulty tiers (unlock by average score on previous tier, subjective-friendly)
TRAINING_LEVELS = [
    {
        "level": 1,
        "key": "starter",
        "name": "入门",
        "emoji": "🌱",
        "blurb": "材料较短，理清思路即可",
    },
    {
        "level": 2,
        "key": "pro",
        "name": "进阶",
        "emoji": "⚡",
        "blurb": "需要多角度分析",
        "unlock_min_attempts_prev": 2,
        "unlock_min_avg_prev": 55,
    },
    {
        "level": 3,
        "key": "master",
        "name": "挑战",
        "emoji": "🔥",
        "blurb": "材料更长、推理更深",
        "unlock_min_attempts_prev": 2,
        "unlock_min_avg_prev": 62,
    },
]
