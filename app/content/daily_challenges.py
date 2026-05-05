"""Daily challenge content for the 5-minute fixed plan."""

from datetime import date
from typing import Dict, List

DailyChallenge = Dict[str, object]


DAILY_CHALLENGES: List[DailyChallenge] = [
    {
        "id": "daily_ct_confidence_filter",
        "dimension": "critical_thinking",
        "theme": "别被 AI 的自信骗了",
        "subtitle": "练习识别从众、证据不足和自信包装",
        "badge": "谬误猎人",
        "completion_title": "AI 自信过滤训练",
        "recap": "你今天练的是：不被流畅表达带着走，先问证据够不够。",
        "stats": [
            {"label": "锋利度", "value": 12},
            {"label": "清晰度", "value": 8},
            {"label": "现实迁移", "value": 5},
        ],
        "stations": [
            {
                "key": "quick",
                "name": "快答题",
                "time_hint": "60 秒",
                "prompt": "一段 AI 回答说：“这个方法被很多人推荐，所以一定有效。”\n\n请指出这句话最大的问题。",
                "placeholder": "例如：推荐人数不能直接证明有效，还需要证据……",
                "rubric": {
                    "key_points": [
                        "指出从众/诉诸人数不能证明有效",
                        "区分流行程度和真实效果",
                        "提出需要验证证据或对照数据",
                    ],
                    "max_score": 100,
                },
            },
            {
                "key": "debate",
                "name": "对抗题",
                "time_hint": "2 分钟",
                "prompt": "对方继续反驳：“但如果这么多人都推荐，至少说明它有价值吧？”\n\n请继续回应它。",
                "placeholder": "继续追问它：价值是哪种价值？推荐来自谁？有没有反例？",
                "rubric": {
                    "key_points": [
                        "承认推荐可能是线索但不是结论",
                        "追问推荐来源、样本和评价标准",
                        "要求用更可靠证据判断价值",
                    ],
                    "max_score": 100,
                },
            },
            {
                "key": "reality",
                "name": "现实任务卡",
                "time_hint": "2 分钟",
                "prompt": "找一个你最近看到的 AI 回答，写下你会验证的 2 个点。",
                "placeholder": "我会验证：1. 来源是否可靠；2. 关键数据是否真实……",
            },
        ],
    },
    {
        "id": "daily_ct_false_choice",
        "dimension": "critical_thinking",
        "theme": "拆掉非黑即白陷阱",
        "subtitle": "练习发现被藏起来的第三种选择",
        "badge": "灰度侦探",
        "completion_title": "灰度判断训练",
        "recap": "你今天练的是：不急着站队，先找被忽略的中间方案。",
        "stats": [
            {"label": "锋利度", "value": 10},
            {"label": "清晰度", "value": 10},
            {"label": "现实迁移", "value": 6},
        ],
        "stations": [
            {
                "key": "quick",
                "name": "快答题",
                "time_hint": "60 秒",
                "prompt": "有人说：“你要么完全拥抱 AI，要么就会被时代淘汰。”\n\n这句话有什么问题？",
                "placeholder": "它把选择简化成两个极端，忽略了……",
                "rubric": {
                    "key_points": [
                        "识别虚假二分/非黑即白",
                        "指出存在有选择、有边界地使用 AI",
                        "说明不同任务适合不同程度使用 AI",
                    ],
                    "max_score": 100,
                },
            },
            {
                "key": "debate",
                "name": "对抗题",
                "time_hint": "2 分钟",
                "prompt": "对方追问：“那你到底支持还是反对用 AI？”\n\n请给出一个不落入二选一的回应。",
                "placeholder": "我支持在……场景用 AI，但在……场景保留人工判断。",
                "rubric": {
                    "key_points": [
                        "明确区分场景",
                        "给出使用边界",
                        "体现不是简单支持或反对",
                    ],
                    "max_score": 100,
                },
            },
            {
                "key": "reality",
                "name": "现实任务卡",
                "time_hint": "2 分钟",
                "prompt": "写下一个你最近遇到的“两难选择”，给它补一个第三选项。",
                "placeholder": "原本以为只能 A 或 B，但第三种做法可能是……",
            },
        ],
    },
    {
        "id": "daily_ct_source_check",
        "dimension": "critical_thinking",
        "theme": "给信息做体检",
        "subtitle": "练习判断来源、证据和可验证性",
        "badge": "证据医生",
        "completion_title": "信息体检训练",
        "recap": "你今天练的是：先判断证据等级，再决定要不要相信。",
        "stats": [
            {"label": "锋利度", "value": 11},
            {"label": "清晰度", "value": 7},
            {"label": "现实迁移", "value": 8},
        ],
        "stations": [
            {
                "key": "quick",
                "name": "快答题",
                "time_hint": "60 秒",
                "prompt": "AI 回答里写：“研究表明，经常冥想的人工作效率会提升 40%。”\n\n你第一反应应该查什么？",
                "placeholder": "我会先查研究来源、样本、指标定义……",
                "rubric": {
                    "key_points": [
                        "查研究来源和是否真实存在",
                        "查样本、方法和指标定义",
                        "警惕具体数字但无出处",
                    ],
                    "max_score": 100,
                },
            },
            {
                "key": "debate",
                "name": "对抗题",
                "time_hint": "2 分钟",
                "prompt": "对方说：“虽然我没给出处，但这个结论听起来很合理。”\n\n请回应它。",
                "placeholder": "合理不代表真实，尤其是带具体数字时……",
                "rubric": {
                    "key_points": [
                        "区分合理感和真实性",
                        "指出具体数字需要来源",
                        "提出可验证的下一步",
                    ],
                    "max_score": 100,
                },
            },
            {
                "key": "reality",
                "name": "现实任务卡",
                "time_hint": "2 分钟",
                "prompt": "从你今天看到的一条信息里，挑出一个最需要查证的数字或结论。",
                "placeholder": "我想查证的是……我会去看……",
            },
        ],
    },
    {
        "id": "daily_qf_prompt_upgrade",
        "dimension": "question_framing",
        "theme": "把废话 Prompt 变锋利",
        "subtitle": "练习从模糊请求变成可执行问题",
        "badge": "问题建筑师",
        "completion_title": "Prompt 升级训练",
        "recap": "你今天练的是：先把目标、背景和判断标准讲清楚，再让 AI 出力。",
        "stats": [
            {"label": "锋利度", "value": 5},
            {"label": "清晰度", "value": 14},
            {"label": "现实迁移", "value": 8},
        ],
        "stations": [
            {
                "key": "quick",
                "name": "快答题",
                "time_hint": "60 秒",
                "prompt": "把这个请求升级一下：“帮我写个方案。”\n\n请改成一个更容易得到好答案的 Prompt。",
                "placeholder": "背景是……目标是……输出格式要……",
                "rubric": {
                    "key_points": [
                        "补充背景和目标",
                        "说明约束或受众",
                        "明确输出格式或评价标准",
                    ],
                    "max_score": 100,
                },
            },
            {
                "key": "debate",
                "name": "对抗题",
                "time_hint": "2 分钟",
                "prompt": "对方问：“你说的‘好方案’具体是什么意思？”\n\n请补 3 个判断标准。",
                "placeholder": "好的标准包括：可执行、成本低、能衡量……",
                "rubric": {
                    "key_points": [
                        "给出可判断的标准",
                        "避免只写好看、优秀等空词",
                        "标准和任务目标有关",
                    ],
                    "max_score": 100,
                },
            },
            {
                "key": "reality",
                "name": "现实任务卡",
                "time_hint": "2 分钟",
                "prompt": "拿一个你真实想问 AI 的问题，写出升级版 Prompt。",
                "placeholder": "原问题是……升级后我会这样问……",
            },
        ],
    },
    {
        "id": "daily_qf_meeting_focus",
        "dimension": "question_framing",
        "theme": "让会议不再打转",
        "subtitle": "练习用问题拉回目标、瓶颈和下一步",
        "badge": "对齐教练",
        "completion_title": "会议对齐训练",
        "recap": "你今天练的是：用几个高价值问题把讨论从发散拉回行动。",
        "stats": [
            {"label": "锋利度", "value": 6},
            {"label": "清晰度", "value": 13},
            {"label": "现实迁移", "value": 9},
        ],
        "stations": [
            {
                "key": "quick",
                "name": "快答题",
                "time_hint": "60 秒",
                "prompt": "团队讨论 30 分钟还在争“要不要改版”。\n\n你会问哪 3 个问题让讨论回到正轨？",
                "placeholder": "目标是什么？现在卡在哪里？今天要决定什么？",
                "rubric": {
                    "key_points": [
                        "追问目标或成功标准",
                        "追问当前卡点",
                        "追问下一步决策或行动",
                    ],
                    "max_score": 100,
                },
            },
            {
                "key": "debate",
                "name": "对抗题",
                "time_hint": "2 分钟",
                "prompt": "对方说：“大家各抒己见也挺好。”\n\n请回应：为什么会议需要收束问题？",
                "placeholder": "发散有价值，但如果没有决策标准……",
                "rubric": {
                    "key_points": [
                        "承认发散价值",
                        "指出会议需要产出或决策",
                        "提出收束问题的方式",
                    ],
                    "max_score": 100,
                },
            },
            {
                "key": "reality",
                "name": "现实任务卡",
                "time_hint": "2 分钟",
                "prompt": "为你最近一次会议或讨论，补一个“如果重来我会问”的问题。",
                "placeholder": "如果重来，我会问……因为它能帮助……",
            },
        ],
    },
    {
        "id": "daily_qf_role_switch",
        "dimension": "question_framing",
        "theme": "换个角色问问题",
        "subtitle": "练习从不同视角看到不同重点",
        "badge": "视角切换师",
        "completion_title": "多视角提问训练",
        "recap": "你今天练的是：同一件事，不同角色最需要的问题并不一样。",
        "stats": [
            {"label": "锋利度", "value": 7},
            {"label": "清晰度", "value": 12},
            {"label": "现实迁移", "value": 7},
        ],
        "stations": [
            {
                "key": "quick",
                "name": "快答题",
                "time_hint": "60 秒",
                "prompt": "公司想上线一个 AI 客服。\n\n请分别从用户、客服团队、老板三个视角各问一个问题。",
                "placeholder": "用户会问……客服团队会问……老板会问……",
                "rubric": {
                    "key_points": [
                        "三个视角有明显差异",
                        "问题贴合各角色利益",
                        "问题足够具体",
                    ],
                    "max_score": 100,
                },
            },
            {
                "key": "debate",
                "name": "对抗题",
                "time_hint": "2 分钟",
                "prompt": "对方说：“只要老板觉得效率提升，就可以上线。”\n\n请用另一个角色视角追问它。",
                "placeholder": "从用户角度：如果回答错了谁负责？……",
                "rubric": {
                    "key_points": [
                        "明确切换角色",
                        "指出老板视角之外的风险",
                        "用问题推动补充判断",
                    ],
                    "max_score": 100,
                },
            },
            {
                "key": "reality",
                "name": "现实任务卡",
                "time_hint": "2 分钟",
                "prompt": "挑一个你正在处理的任务，从另一个人的视角补一个问题。",
                "placeholder": "如果我是……我会问……",
            },
        ],
    },
    {
        "id": "daily_cr_constraint_spark",
        "dimension": "creativity",
        "theme": "约束不是刹车，是发动机",
        "subtitle": "练习在钱少、时间短、规则多时找新路",
        "badge": "约束发明家",
        "completion_title": "约束创新训练",
        "recap": "你今天练的是：先接受限制，再让限制逼出不普通的方案。",
        "stats": [
            {"label": "锋利度", "value": 5},
            {"label": "清晰度", "value": 8},
            {"label": "现实迁移", "value": 12},
        ],
        "stations": [
            {
                "key": "quick",
                "name": "快答题",
                "time_hint": "60 秒",
                "prompt": "约束：0 元预算、只用微信群、今天之内。\n\n请为一个新读书会拉来前 20 个参与者。",
                "placeholder": "我会利用已有关系、共创名单、限时挑战……",
                "rubric": {
                    "key_points": [
                        "遵守 0 元和微信群约束",
                        "方案具体可执行",
                        "有一点非常规吸引力",
                    ],
                    "max_score": 100,
                },
            },
            {
                "key": "debate",
                "name": "对抗题",
                "time_hint": "2 分钟",
                "prompt": "对方说：“没有预算很难做出传播。”\n\n请反驳它，并给出一个低成本传播动作。",
                "placeholder": "预算少不等于不能传播，可以用……",
                "rubric": {
                    "key_points": [
                        "指出预算不是唯一资源",
                        "提出低成本传播动作",
                        "说明为什么会有人愿意参与",
                    ],
                    "max_score": 100,
                },
            },
            {
                "key": "reality",
                "name": "现实任务卡",
                "time_hint": "2 分钟",
                "prompt": "写下你最近一个受限任务，并把限制改写成一个创意提示。",
                "placeholder": "限制是……它可以逼我尝试……",
            },
        ],
    },
    {
        "id": "daily_cr_reverse_design",
        "dimension": "creativity",
        "theme": "先搞砸，再反转",
        "subtitle": "练习用失败预演找到创新入口",
        "badge": "逆向设计师",
        "completion_title": "逆向思维训练",
        "recap": "你今天练的是：先把失败讲具体，再逐条反转成行动。",
        "stats": [
            {"label": "锋利度", "value": 7},
            {"label": "清晰度", "value": 7},
            {"label": "现实迁移", "value": 12},
        ],
        "stations": [
            {
                "key": "quick",
                "name": "快答题",
                "time_hint": "60 秒",
                "prompt": "如果你想让一个学习打卡群彻底没人坚持，你会做哪 3 件事？",
                "placeholder": "比如规则太复杂、反馈太慢、目标太大……",
                "rubric": {
                    "key_points": [
                        "失败原因具体",
                        "能切中用户坚持困难",
                        "不是泛泛而谈",
                    ],
                    "max_score": 100,
                },
            },
            {
                "key": "debate",
                "name": "对抗题",
                "time_hint": "2 分钟",
                "prompt": "对方说：“那就把这些失败点反过来就好了。”\n\n请把其中 1 个反转成更具体的新设计。",
                "placeholder": "如果失败点是反馈慢，反转不是“反馈快”，而是……",
                "rubric": {
                    "key_points": [
                        "选择一个失败点",
                        "反转后足够具体",
                        "不是简单取反",
                    ],
                    "max_score": 100,
                },
            },
            {
                "key": "reality",
                "name": "现实任务卡",
                "time_hint": "2 分钟",
                "prompt": "挑一个你想坚持的小习惯，写下一个“必败设计”和一个反转策略。",
                "placeholder": "必败设计是……反转策略是……",
            },
        ],
    },
    {
        "id": "daily_cr_cross_domain",
        "dimension": "creativity",
        "theme": "把别处的办法借过来",
        "subtitle": "练习跨领域迁移，而不是照搬答案",
        "badge": "跨界搬运师",
        "completion_title": "跨域迁移训练",
        "recap": "你今天练的是：借结构，不照抄；换场景，保留核心机制。",
        "stats": [
            {"label": "锋利度", "value": 6},
            {"label": "清晰度", "value": 8},
            {"label": "现实迁移", "value": 13},
        ],
        "stations": [
            {
                "key": "quick",
                "name": "快答题",
                "time_hint": "60 秒",
                "prompt": "把“游戏里的新手任务”迁移到“新人入职”场景。\n\n你会设计什么？",
                "placeholder": "我会把入职拆成可见任务、即时反馈、阶段奖励……",
                "rubric": {
                    "key_points": [
                        "抓住新手任务的结构",
                        "迁移到入职场景合理",
                        "方案有可执行动作",
                    ],
                    "max_score": 100,
                },
            },
            {
                "key": "debate",
                "name": "对抗题",
                "time_hint": "2 分钟",
                "prompt": "对方说：“游戏是娱乐，入职是工作，不能类比。”\n\n请说明哪里能类比，哪里不能类比。",
                "placeholder": "能类比的是反馈和路径；不能类比的是……",
                "rubric": {
                    "key_points": [
                        "说清可迁移的结构",
                        "说清不可照搬的边界",
                        "体现迁移不是复制",
                    ],
                    "max_score": 100,
                },
            },
            {
                "key": "reality",
                "name": "现实任务卡",
                "time_hint": "2 分钟",
                "prompt": "找一个你熟悉领域的做法，把它迁移到今天的一个小任务里。",
                "placeholder": "我想借用……领域的……来解决……",
            },
        ],
    },
]

_BY_DIMENSION: Dict[str, List[DailyChallenge]] = {
    "critical_thinking": [c for c in DAILY_CHALLENGES if c["dimension"] == "critical_thinking"],
    "question_framing": [c for c in DAILY_CHALLENGES if c["dimension"] == "question_framing"],
    "creativity": [c for c in DAILY_CHALLENGES if c["dimension"] == "creativity"],
}


def _dimension_for_day(day: date) -> str:
    weekday = day.weekday()
    if weekday in (0, 3):
        return "critical_thinking"
    if weekday in (1, 4):
        return "question_framing"
    if weekday in (2, 5):
        return "creativity"
    return "mixed"


def get_daily_challenge(today: date = None) -> DailyChallenge:
    """Return today's fixed challenge. Sunday rotates across all three abilities."""
    today = today or date.today()
    dimension = _dimension_for_day(today)
    pool = DAILY_CHALLENGES if dimension == "mixed" else _BY_DIMENSION[dimension]
    index = today.toordinal() % len(pool)
    return pool[index]


def get_daily_challenge_by_id(challenge_id: str) -> DailyChallenge:
    for challenge in DAILY_CHALLENGES:
        if challenge["id"] == challenge_id:
            return challenge
    return get_daily_challenge()
