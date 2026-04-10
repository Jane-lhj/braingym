"""
Critical Thinking question bank.

Question types:
  - fallacy_detective: identify logical fallacies in a passage
  - info_verify: evaluate credibility of a claim
  - argument_attack: find weaknesses in an argument
  - stance_flip: argue both sides then give your own judgment
"""

# ---------- Assessment questions (used in 体测) ----------

ASSESSMENT_QUESTIONS = [
    {
        "id": "ct_assess_1",
        "type": "open_ended",
        "prompt": "请阅读这段话：「张教授是物理学权威，他说这款保健品有效，所以一定有效。」\n\n这段论证的逻辑有什么问题？请指出谬误类型并解释。",
        "scoring_rubric": {
            "key_points": [
                "识别出诉诸权威谬误",
                "指出张教授的权威在物理学而非医学/保健领域",
                "说明不相关领域的权威不能作为有效论据",
            ],
            "max_score": 100,
        },
        "difficulty": 1,
    },
    {
        "id": "ct_assess_2",
        "type": "open_ended",
        "prompt": "请看这四句话，判断哪些是「事实」哪些是「观点」，并解释你的判断标准：\n\n1. 中国是世界上最伟大的国家\n2. 2023年中国GDP总量约为126万亿元人民币\n3. 经济增长比环境保护更重要\n4. 人工智能将在10年内取代大部分工作",
        "scoring_rubric": {
            "key_points": [
                "正确识别第2句是事实（可验证的客观数据）",
                "能解释事实与观点的区别（可验证 vs 主观判断/价值取向/预测）",
                "对其余三句的分析合理",
            ],
            "max_score": 100,
        },
        "difficulty": 2,
    },
    {
        "id": "ct_assess_3",
        "type": "open_ended",
        "prompt": "有人说：「既然我们无法确保AI100%安全，那就不应该发展AI。」\n\n请找出这个论证的逻辑漏洞，并用 2-3 句话反驳。",
        "scoring_rubric": {
            "key_points": [
                "识别出这是完美主义谬误/涅槃谬误（要求100%才行动）",
                "指出几乎没有技术能做到100%安全",
                "提出应该在发展中管控风险，而非因噎废食",
            ],
            "max_score": 100,
        },
        "difficulty": 3,
    },
]


# ---------- Training exercises (used in 器械区) ----------

FALLACY_DETECTIVE = [
    {
        "id": "ct_fd_1",
        "difficulty": 1,
        "passage": "「每次我洗车后第二天都会下雨，所以洗车会导致下雨。」",
        "prompt": "这段话的推理有什么问题？请指出谬误类型并用自己的话解释为什么这个推理不成立。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "识别出因果谬误（把相关性/时间先后当因果）",
                "解释洗车和下雨之间只有巧合的时间先后关系",
                "说明相关性不等于因果性",
            ],
            "max_score": 100,
        },
        "example_good_answer": "这是「把相关性当因果」谬误（Post hoc ergo propter hoc）。洗车和下雨只是时间上碰巧先后发生，并不存在因果关系。要证明因果，需要排除巧合、找到机制，而不是仅凭「先后发生」就下结论。",
    },
    {
        "id": "ct_fd_2",
        "difficulty": 1,
        "passage": "「你要么支持完全开放AI，要么你就是反对科技进步。」",
        "prompt": "这段话的逻辑有什么漏洞？请指出谬误并解释现实中这个问题为什么不是非此即彼的。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "识别出虚假二分法（非黑即白谬误）",
                "指出被忽略的中间立场（如有条件支持、分领域监管等）",
                "说明现实中大多数议题存在多种立场",
            ],
            "max_score": 100,
        },
        "example_good_answer": "这是虚假二分法。它把问题简化成只有两个极端选项，忽略了「有条件地支持AI发展」「分领域分阶段开放」等大量中间立场。现实中几乎没有只有两种选择的问题。",
    },
    {
        "id": "ct_fd_3",
        "difficulty": 2,
        "passage": "「反对者说我们应该削减军费，但他们显然想让国家毫无防御能力，任人宰割。」",
        "prompt": "这段反驳的手法有什么问题？它准确地回应了反对者的原始观点吗？请分析。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "识别出稻草人谬误",
                "指出反对者主张的是「削减」而非「取消全部」",
                "解释论者歪曲了对方立场使其更容易反驳",
            ],
            "max_score": 100,
        },
        "example_good_answer": "这是稻草人谬误。反对者的原始观点是「削减军费」，而论者将其歪曲为「取消所有国防、任人宰割」，然后反驳这个被夸张后的版本。削减不等于取消，这种手法回避了原始论点。",
    },
    {
        "id": "ct_fd_4",
        "difficulty": 2,
        "passage": "「如果我们允许学生用AI写作业，接下来他们就会用AI写考试，然后用AI写毕业论文，最后整个教育体系就崩溃了。」",
        "prompt": "这段话预测了一连串后果。这种推理方式可靠吗？请指出问题并解释。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "识别出滑坡论证",
                "指出每一步之间的因果链未被证明",
                "说明允许写作业不必然导致极端后果",
            ],
            "max_score": 100,
        },
        "example_good_answer": "这是滑坡论证。它假设一个行为必然导致一连串越来越极端的后果，但每一步之间的因果关系都没有被证明。允许用AI写作业，学校完全可以在考试和论文环节设置不同的规则，不会自动滑向「教育体系崩溃」。",
    },
    {
        "id": "ct_fd_5",
        "difficulty": 3,
        "passage": "「这个减肥产品一定有效，因为已经有100万人购买了。」",
        "prompt": "「买的人多」能证明产品有效吗？请分析这段话的逻辑问题。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "识别出诉诸人数/从众谬误",
                "解释购买人数与产品功效之间没有必然联系",
                "可能提到营销、跟风等替代解释",
            ],
            "max_score": 100,
        },
        "example_good_answer": "这是诉诸人数谬误（从众谬误）。购买人数多只能说明营销成功或跟风效应，不能证明产品有效。要验证效果需要对照实验和数据，而不是「大家都买了所以有效」。",
    },
    {
        "id": "ct_fd_6",
        "difficulty": 3,
        "passage": "一篇文章标题写道：「成功人士都早起！你也应该5点起床。」文中列举了几位早起的CEO作为证据。",
        "prompt": "这篇文章用几位 CEO 的例子来论证「早起导致成功」，这个论证有哪些问题？请尽可能多地指出。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "幸存者偏差：只看了成功且早起的人，忽略了早起但不成功的",
                "因果倒置：可能是成功让他们有条件早起，而非早起导致成功",
                "样本偏差：几个CEO不能代表所有成功人士",
            ],
            "max_score": 100,
        },
        "example_good_answer": "至少有两个问题：①幸存者偏差——只看了成功且早起的人，忽略了早起但不成功的人和晚起但成功的人；②因果倒置——可能是成功后有条件/动力早起，而非早起导致了成功。另外，几个CEO的例子样本量太小，不能推广到所有人。",
    },
]

ARGUMENT_ATTACK = [
    {
        "id": "ct_aa_1",
        "difficulty": 1,
        "prompt": "有人主张：「应该禁止所有社交媒体，因为社交媒体导致青少年抑郁。」\n\n请找出至少 2 个论证漏洞。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "相关性≠因果性：社交媒体与抑郁的关系可能只是相关，不一定是因果",
                "以偏概全：部分青少年受影响≠所有人受影响",
                "措施过度：禁止所有 vs 适度监管，手段与目标不成比例",
                "忽略正面作用：社交媒体也有社交、学习等正面价值",
            ],
            "min_points": 2,
            "max_score": 100,
        },
    },
    {
        "id": "ct_aa_2",
        "difficulty": 2,
        "prompt": "有人说：「AI生成的画作获得了艺术大赛的奖项，这证明AI的创造力已经超越了人类。」\n\n请反驳这个论点。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "获奖不代表'超越'——可能评委不知道是AI作品",
                "一次获奖不能推广到整体创造力的比较",
                "创造力不仅是产出作品，还包括意图、情感和自主性",
                "AI是工具，背后仍有人类的prompt设计和选择",
            ],
            "min_points": 2,
            "max_score": 100,
        },
    },
    {
        "id": "ct_aa_3",
        "difficulty": 2,
        "prompt": "有人说：「既然大数据能预测犯罪高发区域，我们就应该在这些区域加强巡逻和盘查。」\n\n请分析这个主张可能存在的问题。",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "数据偏见：历史数据可能本身就带有执法偏见（某些区域巡逻多→记录多→预测高）",
                "自我强化循环：加强巡逻→发现更多→数据更高→更多巡逻",
                "侵犯权利：对特定区域居民的系统性不公平对待",
                "相关性问题：区域犯罪率高不代表该区域每个人都是嫌疑人",
            ],
            "min_points": 2,
            "max_score": 100,
        },
    },
]

STANCE_FLIP = [
    {
        "id": "ct_sf_1",
        "difficulty": 3,
        "topic": "学校应该用AI来批改作文",
        "prompt": "请就「学校应该用AI来批改作文」这个话题：\n\n1. 先写出正方（支持）的 2 个核心论点\n2. 再写出反方（反对）的 2 个核心论点\n3. 最后给出你自己的判断和理由",
        "type": "open_ended",
        "scoring_rubric": {
            "key_points": [
                "正方论点合理且有说服力",
                "反方论点合理且有说服力",
                "个人判断有理有据，不是简单站队",
                "能看到双方立场的交叉点/共同前提",
            ],
            "max_score": 100,
        },
    },
]

ALL_EXERCISES = {
    "fallacy_detective": {
        "name": "谬误侦探",
        "icon": "🔍",
        "description": "识别论述中隐藏的逻辑谬误",
        "questions": FALLACY_DETECTIVE,
    },
    "argument_attack": {
        "name": "论点攻防",
        "icon": "⚔️",
        "description": "找出看似合理的论证中的漏洞",
        "questions": ARGUMENT_ATTACK,
    },
    "stance_flip": {
        "name": "立场翻转",
        "icon": "🎭",
        "description": "正反两面论证，锻炼多角度思考",
        "questions": STANCE_FLIP,
    },
}
