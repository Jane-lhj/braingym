"""
Question Framing (提问力) question bank.

Question types:
  - question_upgrade: progressively ask deeper questions about a scenario
  - demand_translate: turn vague descriptions into precise actionable questions
  - socratic_dialogue: pursue the essence through follow-up questions
  - perspective_switch: ask questions from different roles/perspectives
"""

ASSESSMENT_QUESTIONS = [
    {
        "id": "qf_assess_1",
        "type": "open_ended",
        "prompt": "你刚加入一个新团队，需要快速了解情况。你会优先问哪 3 个问题？请按信息价值从高到低排列，并解释为什么这个顺序最合理。",
        "scoring_rubric": {
            "key_points": [
                "优先问战略/目标层面的问题（核心目标、衡量标准）",
                "其次问现状与挑战（最大困难、瓶颈）",
                "能解释为什么目标比执行细节更重要",
                "体现从'为什么做'到'怎么做'的层次感",
            ],
            "min_points": 2,
            "max_score": 100,
        },
        "difficulty": 2,
    },
    {
        "id": "qf_assess_2",
        "type": "open_ended",
        "prompt": "老板说：「我们的用户增长太慢了，想想办法。」\n\n请把这个模糊的需求转化为 3 个具体的、可调研的问题。",
        "scoring_rubric": {
            "key_points": [
                "定义标准：'慢'是相对于什么？（竞品/历史/目标）",
                "拆解漏斗：用户在哪个环节流失最多？（获客/激活/留存）",
                "区分原因：是流量不够还是转化率低？",
                "明确范围：哪个渠道/哪类用户的增长慢？",
            ],
            "min_points": 2,
            "max_score": 100,
        },
        "difficulty": 1,
    },
    {
        "id": "qf_assess_3",
        "type": "open_ended",
        "prompt": "针对「AI会取代人类工作」这个话题，请从以下三个不同视角各提出一个深度问题：\n\n1. 经济学家视角\n2. 一线工人视角\n3. AI研究员视角",
        "scoring_rubric": {
            "key_points": [
                "经济学家视角：关注就业结构、生产力、财富分配等宏观问题",
                "一线工人视角：关注切身利益、转型困难、技能鸿沟",
                "AI研究员视角：关注技术边界、能力局限、发展路径",
                "三个问题之间有差异性，体现了真正的视角切换",
            ],
            "min_points": 3,
            "max_score": 100,
        },
        "difficulty": 3,
    },
]


QUESTION_UPGRADE = [
    {
        "id": "qf_qu_1",
        "difficulty": 1,
        "scenario": "你发现团队最近加班越来越多。",
        "prompt": "请针对「团队加班越来越多」这个现象，按从浅到深的顺序提出 4 个问题。\n\n要求：第1个是表层问题，第4个要触及根本原因。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "表层：加班频率/时长的具体数据（是什么）",
                "中层：加班的直接原因（需求多了？人手不够？效率低？）",
                "深层：组织/流程层面的根因（排期机制？需求管理？团队能力？）",
                "根本：战略/文化层面（公司增长模式是否健康？加班文化？）",
            ],
            "max_score": 100,
        },
        "example_good_answer": "1. 团队每周平均加班多少小时？比上个月增加了多少？\n2. 加班主要是因为需求量增加还是单个任务耗时变长？\n3. 我们的需求评审和优先级排序机制是否能有效过滤低价值需求？\n4. 公司的增长目标是否与团队的产能匹配？我们是在用加班来掩盖资源规划的问题吗？",
    },
    {
        "id": "qf_qu_2",
        "difficulty": 2,
        "scenario": "一个朋友告诉你：「我觉得AI会让我失业。」",
        "prompt": "请针对朋友的担忧，按从浅到深的顺序提出 4 个问题，帮助他/她厘清思路。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "具体化：你具体担心AI替代你工作中的哪些部分？",
                "验证假设：你了解过AI目前在你的行业/岗位的实际应用情况吗？",
                "反思价值：你工作中哪些能力是AI难以替代的？",
                "转化行动：你可以做些什么来让自己成为'会用AI的人'而不是'被AI替代的人'？",
            ],
            "max_score": 100,
        },
    },
    {
        "id": "qf_qu_3",
        "difficulty": 2,
        "scenario": "新闻报道：某城市房价连续3个月下跌。",
        "prompt": "如果你是一个分析师，需要理解这个现象的深层原因，请从浅到深提出 4 个关键问题。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "数据验证：下跌幅度多少？是均价还是中位数？哪些区域？",
                "直接原因：供需关系变化？政策变动？利率调整？",
                "结构原因：人口流动趋势？产业结构变化？居民收入变化？",
                "系统影响：这是短期波动还是长期趋势？对其他经济领域的连锁影响？",
            ],
            "max_score": 100,
        },
    },
]

DEMAND_TRANSLATE = [
    {
        "id": "qf_dt_1",
        "difficulty": 1,
        "vague_request": "「我们的App体验不好，优化一下。」",
        "prompt": "你的老板说：「我们的App体验不好，优化一下。」\n\n请将这个模糊需求转化为 3 个精确的、可执行的问题。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "明确'体验不好'的具体表现（加载慢？操作复杂？视觉丑？）",
                "定位问题范围（哪个页面/功能/用户群体）",
                "建立衡量标准（用什么指标衡量'好'？）",
                "了解优先级（最影响用户/营收的是哪个问题？）",
            ],
            "min_points": 2,
            "max_score": 100,
        },
    },
    {
        "id": "qf_dt_2",
        "difficulty": 2,
        "vague_request": "「我们需要一个更好的推荐算法。」",
        "prompt": "产品经理说：「我们需要一个更好的推荐算法。」\n\n请将这个模糊需求转化为 3 个精确的问题，帮助明确真正要解决的问题。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "'更好'的定义：是准确率、多样性、新颖性还是商业转化率？",
                "现有问题：当前推荐算法的具体短板是什么？有数据支撑吗？",
                "用户反馈：用户对当前推荐的不满主要集中在哪里？",
                "业务约束：是否有延迟、成本、冷启动等技术约束？",
            ],
            "min_points": 2,
            "max_score": 100,
        },
    },
]

PERSPECTIVE_SWITCH = [
    {
        "id": "qf_ps_1",
        "difficulty": 2,
        "topic": "一家公司决定全面采用远程办公",
        "prompt": "「一家500人的科技公司宣布全面转为远程办公」\n\n请分别从以下视角各提出 1 个有深度的问题：\n1. CEO\n2. 基层员工\n3. HR负责人\n4. 客户",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "CEO视角：关注战略/竞争力/成本（如：远程办公如何影响创新速度和团队凝聚力？）",
                "员工视角：关注切身体验/职业发展（如：远程后如何获得晋升所需的可见度？）",
                "HR视角：关注管理/制度/文化（如：如何评估远程环境下的绩效？如何维护文化？）",
                "客户视角：关注服务质量/响应速度（如：远程办公是否影响技术支持的响应速度？）",
                "四个问题确实体现了不同视角的差异",
            ],
            "min_points": 3,
            "max_score": 100,
        },
    },
]

ALL_EXERCISES = {
    "question_upgrade": {
        "name": "问题升级",
        "icon": "🎯",
        "description": "从表层到深层，层层追问直达本质",
        "questions": QUESTION_UPGRADE,
    },
    "demand_translate": {
        "name": "需求翻译",
        "icon": "🔄",
        "description": "把模糊需求转化为精确可执行的问题",
        "questions": DEMAND_TRANSLATE,
    },
    "perspective_switch": {
        "name": "视角切换",
        "icon": "🔀",
        "description": "从不同角色视角提出差异化问题",
        "questions": PERSPECTIVE_SWITCH,
    },
}
