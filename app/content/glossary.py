"""Short terms shown on exercise pages, keyed by exercise_type."""

from typing import Dict, List

Term = Dict[str, str]

GLOSSARY_BY_EXERCISE: Dict[str, List[Term]] = {
    "fallacy_detective": [
        {"title": "诉诸权威", "one_liner": "用「某专家」背书，但专业领域不对口。"},
        {"title": "稻草人", "one_liner": "把对方观点歪曲成好反驳的版本再打倒。"},
        {"title": "滑坡论证", "one_liner": "声称 A 必然导致灾难性 Z，但中间链条没证明。"},
        {"title": "虚假二分", "one_liner": "只给两个极端选项，忽略中间方案。"},
        {"title": "以偏概全", "one_liner": "用少数例子推广到全体。"},
        {"title": "相关当因果", "one_liner": "两件事先后或同时出现，不等于有因果关系。"},
    ],
    "argument_attack": [
        {"title": "论点与论据", "one_liner": "先分清结论是什么、理由有哪些，再判断理由是否充分。"},
        {"title": "隐藏假设", "one_liner": "论证常依赖未说穿的前提，找出来才能检验。"},
        {"title": "证据质量", "one_liner": "轶事、个例、传闻比可重复数据弱得多。"},
    ],
    "stance_flip": [
        {"title": "正反练习", "one_liner": "同一议题先尽力为对立面找合理论据，再给出自己的取舍。"},
        {"title": "强弱论证", "one_liner": "好反驳会针对对方最强版本，而不是挑软柿子。"},
    ],
    "question_upgrade": [
        {"title": "从表象到机制", "one_liner": "先问发生了什么，再问为什么，再问该不该、怎么改。"},
        {"title": "信息价值", "one_liner": "优先问能改变决策的问题，而不是最好回答的问题。"},
    ],
    "demand_translate": [
        {"title": "模糊需求", "one_liner": "把「优化/提升/不好」翻译成对象、场景、指标和现状。"},
        {"title": "可调研", "one_liner": "好问题应能通过数据、访谈或实验部分回答。"},
    ],
    "perspective_switch": [
        {"title": "角色立场", "one_liner": "同一局面下，用户、老板、执行方各自最在意什么？"},
        {"title": "约束不同", "one_liner": "换角色时，优先级和禁忌往往不同，问题要跟着变。"},
    ],
    "random_collision": [
        {"title": "强制组合", "one_liner": "把两个远概念硬拧在一起，再追问服务谁、解决什么。"},
        {"title": "先多后少", "one_liner": "先列出多种联系，再筛可行与有趣的方向。"},
    ],
    "reverse_thinking": [
        {"title": "预演失败", "one_liner": "先具体列出「怎样一定搞砸」，再逐条反转成对策。"},
        {"title": "反转要落地", "one_liner": "反转后应是可执行动作，而不是空洞口号。"},
    ],
    "constraint_innovation": [
        {"title": "约束即创意", "one_liner": "钱少、时间紧、规则多会砍掉平庸方案，逼出新形态。"},
        {"title": "在框内跳舞", "one_liner": "先接受硬约束，再在剩余空间里极大化目标。"},
    ],
    "cross_domain": [
        {"title": "迁移不是照抄", "one_liner": "借 A 领域成熟套路的「结构」，填 B 领域的「内容」。"},
        {"title": "类比边界", "one_liner": "能说清哪里像、哪里不像，迁移才可靠。"},
    ],
}


def get_glossary_for_exercise(exercise_type: str) -> List[Term]:
    return GLOSSARY_BY_EXERCISE.get(exercise_type, [])
