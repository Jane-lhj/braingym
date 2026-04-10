"""
Dimension guide content for the guide page.
Keys must match app.config.DIMENSIONS.
"""

from typing import Any, Dict, List

from app.config import DIMENSIONS

_GUIDE: Dict[str, Dict[str, Any]] = {
    "critical_thinking": {
        "hook": "AI 可以一本正经地胡说八道。你能看出来吗？",
        "body": (
            "当模型能秒出万字长文，「信息多」不再是优势——"
            "能分辨哪些可信、哪些在偷换概念，才是你的护城河。"
        ),
        "contrast": [
            ("别人转发「专家说…」就信了", "你会先问：这位专家的领域对口吗？"),
            ("别人觉得「听起来有道理」", "你能一眼看出稻草人、滑坡、以偏概全"),
        ],
    },
    "question_framing": {
        "hook": "AI 什么都能答——但答什么，取决于你怎么问。",
        "body": (
            "同样用 ChatGPT，有人得到一篇废话，有人得到可执行方案。"
            "差距不在工具，在问题本身的清晰度。"
        ),
        "contrast": [
            ("「帮我优化一下」→ 得到一堆正确的废话", "「首页跳出率 72%，首屏加载 4s，怎么降到 50% 以下」→ 得到可落地的方案"),
            ("开会两小时没结论", "三个问题把目标、瓶颈、下一步全对齐"),
        ],
    },
    "creativity": {
        "hook": "标准答案，AI 比你快一万倍。非标的呢？",
        "body": (
            "能被标准化的工作正在被自动化。"
            "在约束里拧出新组合、把 A 领域的套路迁到 B——这是人最难被替代的部分。"
        ),
        "contrast": [
            ("等灵感，想不出来就放弃", "随手拿两个概念碰撞，先出 20 个点子再筛"),
            ("只在自己的行业里找方案", "把外卖调度的逻辑搬到医院排班，反而是创新"),
        ],
    },
}


def build_guide_sections() -> List[Dict[str, Any]]:
    """Merge DIMENSIONS metadata with guide copy for templates."""
    out: List[Dict[str, Any]] = []
    for key, meta in DIMENSIONS.items():
        g = _GUIDE[key]
        out.append(
            {
                "key": key,
                "name": meta["name"],
                "icon": meta["icon"],
                "color": meta["color"],
                "hook": g["hook"],
                "body": g["body"],
                "contrast": g["contrast"],
            }
        )
    return out
