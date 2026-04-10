"""
Creativity (创造力) question bank.

Question types:
  - random_collision: connect two unrelated concepts creatively
  - reverse_thinking: figure out how to make something fail, then invert
  - constraint_innovation: innovate under strict constraints
  - cross_domain: apply solutions from domain A to domain B
"""

ASSESSMENT_QUESTIONS = [
    {
        "id": "cr_assess_1",
        "type": "open_ended",
        "prompt": "请用「火锅」和「版本控制」这两个毫不相关的概念，创造一个有趣的产品创意或商业点子。\n\n要求：说清楚它是什么、解决什么问题、为什么有趣。",
        "scoring_rubric": {
            "key_points": [
                "两个概念之间建立了有意义的联系（而非强行拼凑）",
                "创意有一定的新颖性和趣味性",
                "能说清楚解决什么问题或满足什么需求",
                "表达清晰有感染力",
            ],
            "max_score": 100,
        },
        "difficulty": 2,
    },
    {
        "id": "cr_assess_2",
        "type": "open_ended",
        "prompt": "如果你想让一个「读书会」彻底失败，你会怎么做？请列出 3 个方法。\n\n然后，把这 3 个方法反转过来，变成让读书会成功的策略。",
        "scoring_rubric": {
            "key_points": [
                "失败方法具体且合理（不是泛泛而谈）",
                "反转后的策略确实有洞察力（不是简单取反）",
                "反转过程中产生了非显而易见的创新想法",
            ],
            "max_score": 100,
        },
        "difficulty": 1,
    },
    {
        "id": "cr_assess_3",
        "type": "open_ended",
        "prompt": "你只有 100 元预算和 3 天时间，要为一个社区设计一场让至少 50 人参与的活动。\n\n请描述你的方案。",
        "scoring_rubric": {
            "key_points": [
                "方案在预算和时间约束内可行",
                "能合理地吸引50人参与",
                "有创意，不是照搬常见活动",
                "考虑了执行细节",
            ],
            "max_score": 100,
        },
        "difficulty": 3,
    },
]


RANDOM_COLLISION = [
    {
        "id": "cr_rc_1",
        "difficulty": 1,
        "word_a": "雨伞",
        "word_b": "社交网络",
        "prompt": "请用「雨伞」和「社交网络」创造一个产品创意。\n\n要求：解释它是什么、解决什么问题、目标用户是谁。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "两个概念之间有合理的连接",
                "创意具有新颖性",
                "有明确的问题/需求指向",
                "目标用户清晰",
            ],
            "max_score": 100,
        },
    },
    {
        "id": "cr_rc_2",
        "difficulty": 1,
        "word_a": "图书馆",
        "word_b": "健身",
        "prompt": "请用「图书馆」和「健身」创造一个创新的服务概念。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "两个概念之间有合理的连接",
                "创意具有新颖性",
                "有明确的价值主张",
            ],
            "max_score": 100,
        },
    },
    {
        "id": "cr_rc_3",
        "difficulty": 2,
        "word_a": "菜市场",
        "word_b": "区块链",
        "prompt": "请用「菜市场」和「区块链」创造一个商业模式。\n\n要求：说清楚它解决什么现实问题，为什么需要结合这两者。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "结合方式有实际意义（不是为了区块链而区块链）",
                "解决了真实的痛点",
                "商业模式可行",
                "创意新颖",
            ],
            "max_score": 100,
        },
    },
    {
        "id": "cr_rc_4",
        "difficulty": 2,
        "word_a": "外婆",
        "word_b": "元宇宙",
        "prompt": "请用「外婆」和「元宇宙」创造一个产品或服务概念。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "创意有温度，不是纯技术堆砌",
                "解决了真实的人际/情感需求",
                "概念新颖有趣",
            ],
            "max_score": 100,
        },
    },
]

REVERSE_THINKING = [
    {
        "id": "cr_rt_1",
        "difficulty": 1,
        "topic": "一款学习App",
        "prompt": "如果你想让一款学习App「用户绝对不想用」，你会怎么设计？请列出 3 个「必败」设计。\n\n然后将每个「必败」设计反转，变成一个创新的设计策略。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "必败设计具体且一针见血",
                "反转后的策略有洞察力",
                "反转不是简单取反，而是产生了新思路",
            ],
            "max_score": 100,
        },
    },
    {
        "id": "cr_rt_2",
        "difficulty": 2,
        "topic": "团队协作",
        "prompt": "如果你想让一个团队的协作「彻底崩溃」，你会做哪 3 件事？\n\n然后反转每一条，提出一个提升团队协作的创新方法。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "必败策略切中团队协作的关键痛点",
                "反转后有超越常规管理建议的创新性",
                "方法具有可操作性",
            ],
            "max_score": 100,
        },
    },
    {
        "id": "cr_rt_3",
        "difficulty": 3,
        "topic": "城市交通",
        "prompt": "如果你想让一个城市的交通「彻底瘫痪」，你会实施哪 3 个政策？\n\n然后反转，提出 3 个创新的交通改善方案。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "瘫痪策略展示了对交通系统的深刻理解",
                "反转方案有创新性，不是常见的'多修路、发展公交'",
                "方案考虑了系统性影响",
            ],
            "max_score": 100,
        },
    },
]

CONSTRAINT_INNOVATION = [
    {
        "id": "cr_ci_1",
        "difficulty": 2,
        "prompt": "约束条件：0 元预算、只用微信、1 天时间。\n\n任务：为一个刚起步的独立咖啡店获得前 100 个客户。\n\n请给出你的具体方案。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "严格遵守约束条件",
                "方案具体可执行",
                "利用约束产生了巧妙的创意",
                "有合理的预期效果",
            ],
            "max_score": 100,
        },
    },
    {
        "id": "cr_ci_2",
        "difficulty": 3,
        "prompt": "约束条件：不用任何屏幕（手机/电脑/电视），预算 50 元以内。\n\n任务：设计一个让 10 个陌生人在 2 小时内成为朋友的活动。\n\n请给出详细方案。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "严格遵守无屏幕和预算约束",
                "活动设计能真正促进陌生人之间的连接",
                "有创意，不是简单的自我介绍或游戏",
                "考虑了实际执行的可行性",
            ],
            "max_score": 100,
        },
    },
]

CROSS_DOMAIN = [
    {
        "id": "cr_cd_1",
        "difficulty": 3,
        "source_domain": "餐饮行业的'试吃'模式",
        "target_domain": "企业招聘",
        "prompt": "餐饮行业有一个经典策略：「免费试吃」。\n\n请把这个概念迁移到「企业招聘」领域，设计一个创新的招聘方式。\n\n说明：怎么做、为什么有效、可能的风险。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "类比迁移合理（抓住了'试吃'的本质而非表面）",
                "招聘方案具有创新性和可行性",
                "分析了优势和可能的风险",
            ],
            "max_score": 100,
        },
    },
]

ALL_EXERCISES = {
    "random_collision": {
        "name": "随机碰撞",
        "icon": "🎲",
        "description": "两个随机概念，硬扭在一起看能擦出什么火花",
        "questions": RANDOM_COLLISION,
    },
    "reverse_thinking": {
        "name": "逆向思维",
        "icon": "🔄",
        "description": "先想怎么失败，再反转成创新方案",
        "questions": REVERSE_THINKING,
    },
    "constraint_innovation": {
        "name": "约束创新",
        "icon": "📦",
        "description": "在严格约束下找到最优解",
        "questions": CONSTRAINT_INNOVATION,
    },
    "cross_domain": {
        "name": "跨域迁移",
        "icon": "🌉",
        "description": "用A领域的方案解决B领域的问题",
        "questions": CROSS_DOMAIN,
    },
}
