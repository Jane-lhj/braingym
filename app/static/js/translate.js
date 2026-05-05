(function() {
    'use strict';

    var LANG_KEY = 'braingym_language';
    var CHINESE_RE = /[\u3400-\u9fff]/;
    var ATTRS = ['placeholder', 'title', 'aria-label'];
    var observer = null;
    var translating = false;
    var statusTimer = null;

    // Local bilingual dictionary. When adding or changing Chinese copy in templates,
    // config, content, or question banks, add the matching English copy here too.
    var EXACT = {
        '健脑房 BrainGym': 'BrainGym',
        '健脑房 BrainGym — AI时代的思维健身房': 'BrainGym - A Thinking Gym for the AI Era',
        '健脑房 BrainGym — AI 时代的思维健身房': 'BrainGym - A Thinking Gym for the AI Era',
        '训练区 — 健脑房': 'Training Zone - BrainGym',
        '自由训练 — 健脑房': 'Free Training - BrainGym',
        '每日闯关 — 健脑房': 'Daily Challenge - BrainGym',
        '每日闯关结果 — 健脑房': 'Daily Challenge Result - BrainGym',
        '入馆体测 — 健脑房': 'Entrance Assessment - BrainGym',
        '体测结果 — 健脑房': 'Assessment Result - BrainGym',
        '训练结果 — 健脑房': 'Training Result - BrainGym',
        '健脑房': 'BrainGym',
        'AI 时代，身体去健身房，大脑来健脑房。 每天 10 分钟，保持思维锋利。': 'In the AI era, your body goes to the gym. Your mind comes to BrainGym.\n10 minutes a day keeps your thinking sharp.',
        'AI 时代，身体去健身房，大脑来健脑房。': 'In the AI era, your body goes to the gym. Your mind comes to BrainGym.',
        '每天 10 分钟，保持思维锋利。': '10 minutes a day keeps your thinking sharp.',
        '让思考成为习惯，让大脑永远年轻': 'Make thinking a habit. Keep your mind young.',
        '开始训练': 'Start Training',
        '选择昵称后开始': 'Choose a nickname to start',
        '输入你的昵称': 'Enter your nickname',
        '进入健脑房 →': 'Enter BrainGym ->',
        '每日闯关': 'Daily Challenge',
        '固定 5 分钟计划': 'A fixed 5-minute plan',
        '60 秒': '60 sec',
        '90 秒': '90 sec',
        '2 分钟': '2 min',
        '自由训练': 'Free Training',
        '按能力专项练': 'Target one ability at a time',
        '批判性思维': 'Critical Thinking',
        '提问力': 'Question Framing',
        '创造力': 'Creativity',
        '三大能力说明': 'The Three Core Abilities',
        '查看说明 →': 'View Guide ->',
        '思维能力雷达图': 'Thinking Ability Radar',
        '开始你的第一次体测': 'Start Your First Assessment',
        '完成一次体测，了解你的思维能力现状': 'Complete an assessment to understand your current thinking profile.',
        '重新体测': 'Retake Assessment',
        '开始体测': 'Start Assessment',
        '体测成绩趋势': 'Assessment Score Trend',
        '训练区': 'Training Zone',
        '进入训练区 →': 'Enter Training Zone ->',
        '今天怎么练？': 'How do you want to train today?',
        '固定计划像团课，自由训练像部位专攻。': 'The fixed plan feels like a class; free training feels like focused muscle work.',
        '今天固定 5 分钟计划': "Today's fixed 5-minute plan",
        '先完成快答，再进入限时辩论，最后落到现实任务。': 'Finish the quick round first, then enter timed debate, and finally land it in a real-world task.',
        '开始今日计划 →': "Start today's plan ->",
        '进入自由训练 →': 'Enter Free Training ->',
        '能力速练': 'Quick Ability Training',
        '像部位专攻一样，选择能力和项目': 'Choose an ability and exercise, like focused muscle training.',
        '我的健脑房': 'My BrainGym',
        '刷新本页': 'Refresh',
        '换昵称重进': 'Switch Nickname',
        '选择训练维度和项目，开始锻炼': 'Choose an ability and exercise to start training.',
        '今天练一题即可打卡': 'Finish one exercise today to check in.',
        '今天开练': 'Train Today',
        '固定 5 分钟': 'Fixed 5 minutes',
        '三站闯关：快答、辩论、任务卡': 'Three stations: quick answer, debate, task card.',
        '进入每日闯关 →': 'Enter Daily Challenge ->',
        '想练哪块就点哪块，也可以进入完整训练页。': 'Pick an ability directly, or enter the full training page.',
        '返回我的健脑房': '<- Back to My BrainGym',
        '← 我的健脑房': '<- My BrainGym',
        '← 返回我的健脑房': '<- Back to My BrainGym',
        '← 返回首页': '<- Back Home',
        '返回首页': 'Back Home',
        '换个项目': 'Choose Another Exercise',
        '继续训练 →': 'Keep Training ->',
        '入馆体测': 'Entrance Assessment',
        '道开放题': 'open-ended questions',
        '进度': 'Progress',
        '提交体测': 'Submit Assessment',
        '上一题': '<- Previous',
        '← 上一题': '<- Previous',
        '下一题 →': 'Next ->',
        '体测报告': 'Assessment Report',
        '体测结果': 'Assessment Result',
        '第一次来可以先测一下基线。': 'First time here? Take a baseline assessment.',
        '展开体测报告与能力说明': 'Expand Assessment Report and Ability Guide',
        '查看三大能力说明 →': 'View the Three Ability Guide ->',
        '完成一次体测，之后这里会显示简版结果；训练入口仍然会放在最上面。': 'Complete one assessment and a compact result will appear here; training stays at the top.',
        '思维能力评估': 'thinking ability assessment',
        '综合思维指数': 'Overall Thinking Index',
        '各题小结': 'Question Summaries',
        '开始训练 🏋️': 'Start Training',
        '训练结果': 'Training Result',
        '小结': 'Summary',
        '你的回答': 'Your Answer',
        '🗣️ 你的回答': 'Your Answer',
        '参考答案': 'Reference Answer',
        'AI 参考答案': 'Reference Answer',
        '🤖 AI 参考答案': 'Reference Answer',
        '提交答案': 'Submit Answer',
        '完成今日闯关': "Finish Today's Challenge",
        '写下你的思考…': 'Write your thoughts...',
        '写下你的思考...': 'Write your thoughts...',
        '阅读材料': 'Reading Material',
        '场景': 'Scenario',
        '场景（可选）': 'Scenario (optional)',
        '换场景': 'Change Scenario',
        '自定义一句，如：动漫剧情': 'Custom scenario, e.g. anime plot',
        '应用': 'Apply',
        '不选场景，用默认题': 'Use default questions without a scenario',
        '今日场景': "Today's Scenario",
        '已选择场景': 'Selected scenario',
        '结合这个场景完成今天的三站练习。': 'Use this scenario as the context for today’s three stations.',
        '换一题': 'Try Another Question',
        '三站式脑力循环': 'three-station brain loop',
        '快答题': 'Quick Round',
        '对抗题': 'Counter Round',
        '现实任务卡': 'Real-World Task Card',
        '完成快答，进入辩论': 'Finish Quick Round and Start Debate',
        '限时辩论': 'Timed Debate',
        '剩余时间': 'Time Left',
        'AI 观点': 'Opposing View',
        'AI 式观点': 'Opposing View',
        '对方观点': 'Opposing View',
        '看提示': 'Show Hint',
        '收起提示': 'Hide Hint',
        '提示': 'Hint',
        '请先写下你的快答。': 'Write your quick answer first.',
        '请先写一句回应。': 'Write one response first.',
        '发送回应': 'Send Response',
        '进入现实任务卡': 'Enter Real-World Task Card',
        '请先写下今天的小任务。': 'Write today’s small task first.',
        '你能给出一个更具体的理由吗？': 'Can you give a more specific reason?',
        '如果对方继续反驳，你最后会怎么收束？': 'If the other side keeps pushing back, how would you close your argument?',
        '辩论时间到，可以进入任务卡。': 'Debate time is up. You can enter the task card.',
        '你的回应': 'Your Response',
        '追问': 'Follow-Up',
        '正在准备追问…': 'Preparing follow-up...',
        '追问已准备好，可以继续回应，或进入现实任务卡。': 'Follow-up is ready. You can keep responding or enter the real-world task card.',
        '追问暂时没准备好，先继续写你的反驳也可以。': 'The follow-up is not ready yet. You can keep writing your rebuttal.',
        '先写一句具体回应，我再继续追问。': 'Write one specific response first, then I will follow up.',
        '你这句话最强的一点是什么？能把它压成一个追问吗？': 'What is the strongest point in your sentence? Can you turn it into a question?',
        '这些证据里，哪一个最能改变结论？为什么？': 'Which piece of evidence would most change the conclusion? Why?',
        '这个标准能被别人判断吗？你会怎么说得更具体？': 'Can others judge this standard? How would you make it more specific?',
        '边界说清了，那最容易被误用的情况是什么？': 'Now that the boundary is clearer, where is it most likely to be misused?',
        '还可以继续回应，或进入现实任务卡。': 'You can keep responding or enter the real-world task card.',
        '今日完成': 'Completed Today',
        '今日称号': "Today's Title",
        '综合完成度': 'Overall Completion',
        '一句复盘': 'One-Line Debrief',
        '三站回看': 'Three-Station Review',
        '回到健脑房': 'Back to BrainGym',
        '去自由训练': 'Go to Free Training',
        '联系邮箱 hello.lhj@foxmail.com': 'Contact: hello.lhj@foxmail.com',
        '返回': 'Back',
        '健脑房首页': 'BrainGym Home',
        '本维度说明': 'Ability Guide',
        '闯关难度': 'Difficulty Level',
        '未解锁': 'Locked',
        '参考难度': 'Reference difficulty',
        '节奏': 'Pace',
        '正在准备题目…': 'Preparing question...',
        '评分中...': 'Scoring...',
        '生活日常': 'Daily Life',
        '职场实战': 'Workplace Practice',
        '社会热点': 'Social Trends',
        '学术硬核': 'Academic Mode',
        '入门': 'Starter',
        '进阶': 'Advanced',
        '挑战': 'Challenge',
        '优秀 🌟': 'Excellent',
        '良好 👍': 'Good',
        '中等 💪': 'Average',
        '待提升 🎯': 'Needs Work',
        '思维达人！继续保持': 'Thinking pro! Keep it up.',
        '基础扎实，还有提升空间': 'Solid foundation, with room to grow.',
        '需要系统训练': 'Needs systematic training.',
        '欢迎来到健脑房！让我们开始吧': 'Welcome to BrainGym. Let us begin.',
        '太棒了！': 'Great work!',
        '🌟 太棒了！': 'Great work!',
        '不错！': 'Nice work!',
        '👍 不错！': 'Nice work!',
        '继续加油！': 'Keep going!',
        '💪 继续加油！': 'Keep going!',
        '还需要练习！': 'More practice needed.',
        '🎯 还需要练习！': 'More practice needed.',
        '分': 'pts',
        '第': 'Question',
        '题': 'questions',
        '已恢复中文': 'Chinese restored',
        '为什么练这三项 — 健脑房': 'Why Train These Three - BrainGym',
        'AI 时代，人该练什么？': 'What Should Humans Train in the AI Era?',
        '机器越强，这三项能力反而越值钱': 'The stronger machines get, the more valuable these three abilities become.',
        '没练过': 'Before Training',
        '练过之后': 'After Training',
        '训练区': 'Training Zone',
        '开始练 批判性思维 →': 'Train Critical Thinking ->',
        '开始练 提问力 →': 'Train Question Framing ->',
        '开始练 创造力 →': 'Train Creativity ->',

        '坚持小火苗': 'Training Streak',
        '本周已有': 'This week:',
        '天来过 · 共练': 'active days,',
        '题次': 'sessions',

        '谬误侦探': 'Fallacy Detective',
        '识别论述中隐藏的逻辑谬误': 'Identify hidden logical fallacies in arguments.',
        '论点攻防': 'Argument Attack',
        '找出看似合理的论证中的漏洞': 'Find weaknesses in arguments that sound reasonable.',
        '立场翻转': 'Stance Flip',
        '正反两面论证，锻炼多角度思考': 'Argue both sides to train multi-angle thinking.',
        '问题升级': 'Question Upgrade',
        '从表层到深层，层层追问直达本质': 'Move from surface questions to deeper causes.',
        '需求翻译': 'Demand Translation',
        '把模糊需求转化为精确可执行的问题': 'Turn vague requests into precise, actionable questions.',
        '视角切换': 'Perspective Switch',
        '从不同角色视角提出差异化问题': 'Ask different questions from different roles.',
        '随机碰撞': 'Random Collision',
        '两个随机概念，硬扭在一起看能擦出什么火花': 'Combine two unrelated concepts and see what sparks.',
        '逆向思维': 'Reverse Thinking',
        '先想怎么失败，再反转成创新方案': 'Imagine failure first, then reverse it into a solution.',
        '约束创新': 'Constraint Innovation',
        '在严格约束下找到最优解': 'Find the best solution under tight constraints.',
        '跨域迁移': 'Cross-Domain Transfer',
        '用A领域的方案解决B领域的问题': 'Use a solution from domain A to solve a problem in domain B.',

        '别被 AI 的自信骗了': "Do not be fooled by AI's confidence",
        '练习识别从众、证据不足和自信包装': 'Practice spotting bandwagon claims, weak evidence, and confident packaging.',
        '谬误猎人': 'Fallacy Hunter',
        'AI 自信过滤训练': 'AI Confidence Filter Training',
        '你今天练的是：不被流畅表达带着走，先问证据够不够。': 'Today you practiced not being led by fluent wording, and asking whether the evidence is enough.',
        '一段 AI 回答说：“这个方法被很多人推荐，所以一定有效。” 请指出这句话最大的问题。': 'An AI answer says: "This method is recommended by many people, so it must be effective."\n\nIdentify the biggest problem with this statement.',
        '例如：推荐人数不能直接证明有效，还需要证据……': 'For example: the number of recommendations cannot directly prove effectiveness; evidence is still needed...',
        '对方继续反驳：“但如果这么多人都推荐，至少说明它有价值吧？” 请继续回应它。': 'The other side pushes back: "But if so many people recommend it, at least it means it has value, right?"\n\nContinue responding.',
        '继续追问它：价值是哪种价值？推荐来自谁？有没有反例？': 'Keep questioning it: what kind of value? Who recommended it? Are there counterexamples?',
        '找一个你最近看到的 AI 回答，写下你会验证的 2 个点。': 'Find a recent AI answer you saw, and write two things you would verify.',
        '我会验证：1. 来源是否可靠；2. 关键数据是否真实……': 'I would verify: 1. whether the source is reliable; 2. whether the key data is real...',

        '拆掉非黑即白陷阱': 'Dismantle the black-and-white trap',
        '练习发现被藏起来的第三种选择': 'Practice finding the hidden third option.',
        '灰度侦探': 'Gray-Area Detective',
        '灰度判断训练': 'Gray-Area Judgment Training',
        '你今天练的是：不急着站队，先找被忽略的中间方案。': 'Today you practiced not rushing to take sides, and first finding the overlooked middle option.',
        '有人说：“你要么完全拥抱 AI，要么就会被时代淘汰。” 这句话有什么问题？': 'Someone says: "Either you fully embrace AI, or you will be eliminated by the times."\n\nWhat is wrong with this statement?',
        '它把选择简化成两个极端，忽略了……': 'It simplifies the choice into two extremes and ignores...',
        '对方追问：“那你到底支持还是反对用 AI？” 请给出一个不落入二选一的回应。': 'The other side asks: "So do you support or oppose using AI?"\n\nGive a response that does not fall into either-or thinking.',
        '我支持在……场景用 AI，但在……场景保留人工判断。': 'I support using AI in... situations, but keeping human judgment in... situations.',
        '写下一个你最近遇到的“两难选择”，给它补一个第三选项。': 'Write down a recent dilemma you faced, and add a third option.',
        '原本以为只能 A 或 B，但第三种做法可能是……': 'I originally thought it had to be A or B, but a third approach could be...',

        '给信息做体检': 'Give information a checkup',
        '练习判断来源、证据和可验证性': 'Practice judging sources, evidence, and verifiability.',
        '证据医生': 'Evidence Doctor',
        '信息体检训练': 'Information Checkup Training',
        '你今天练的是：先判断证据等级，再决定要不要相信。': 'Today you practiced judging evidence quality before deciding whether to believe something.',
        'AI 回答里写：“研究表明，经常冥想的人工作效率会提升 40%。” 你第一反应应该查什么？': 'An AI answer says: "Research shows that people who meditate regularly improve work efficiency by 40%."\n\nWhat should you check first?',
        '我会先查研究来源、样本、指标定义……': 'I would first check the research source, sample, and metric definitions...',
        '对方说：“虽然我没给出处，但这个结论听起来很合理。” 请回应它。': 'The other side says: "Although I did not provide a source, this conclusion sounds reasonable."\n\nRespond to it.',
        '合理不代表真实，尤其是带具体数字时……': 'Reasonable-sounding does not mean true, especially when specific numbers are involved...',
        '从你今天看到的一条信息里，挑出一个最需要查证的数字或结论。': 'From one piece of information you saw today, pick the number or conclusion that most needs verification.',
        '我想查证的是……我会去看……': 'What I want to verify is... I would check...',

        '把废话 Prompt 变锋利': 'Sharpen a vague prompt',
        '练习从模糊请求变成可执行问题': 'Practice turning vague requests into actionable questions.',
        '问题建筑师': 'Question Architect',
        'Prompt 升级训练': 'Prompt Upgrade Training',
        '你今天练的是：先把目标、背景和判断标准讲清楚，再让 AI 出力。': 'Today you practiced making the goal, context, and criteria clear before asking AI to help.',
        '把这个请求升级一下：“帮我写个方案。” 请改成一个更容易得到好答案的 Prompt。': 'Upgrade this request: "Help me write a plan."\n\nRewrite it as a prompt that is more likely to produce a good answer.',
        '背景是……目标是……输出格式要……': 'The context is... the goal is... the output format should...',
        '对方问：“你说的‘好方案’具体是什么意思？” 请补 3 个判断标准。': 'The other side asks: "What exactly do you mean by a good plan?"\n\nAdd three evaluation criteria.',
        '好的标准包括：可执行、成本低、能衡量……': 'Good criteria include: executable, low-cost, measurable...',
        '拿一个你真实想问 AI 的问题，写出升级版 Prompt。': 'Take a real question you want to ask AI, and write an upgraded prompt.',
        '原问题是……升级后我会这样问……': 'The original question is... After upgrading, I would ask...',

        '让会议不再打转': 'Stop meetings from going in circles',
        '练习用问题拉回目标、瓶颈和下一步': 'Practice using questions to return to goals, bottlenecks, and next steps.',
        '对齐教练': 'Alignment Coach',
        '会议对齐训练': 'Meeting Alignment Training',
        '你今天练的是：用几个高价值问题把讨论从发散拉回行动。': 'Today you practiced using high-value questions to pull discussion back from divergence to action.',
        '团队讨论 30 分钟还在争“要不要改版”。 你会问哪 3 个问题让讨论回到正轨？': 'The team has discussed for 30 minutes and is still arguing about whether to redesign.\n\nWhat three questions would you ask to bring the discussion back on track?',
        '目标是什么？现在卡在哪里？今天要决定什么？': 'What is the goal? Where are we stuck? What needs to be decided today?',
        '对方说：“大家各抒己见也挺好。” 请回应：为什么会议需要收束问题？': 'The other side says: "It is good for everyone to express their opinions."\n\nRespond: why does a meeting need narrowing questions?',
        '发散有价值，但如果没有决策标准……': 'Divergence is valuable, but without decision criteria...',
        '为你最近一次会议或讨论，补一个“如果重来我会问”的问题。': 'For a recent meeting or discussion, add one question you would ask if you could do it again.',
        '如果重来，我会问……因为它能帮助……': 'If I could do it again, I would ask... because it would help...',

        '换个角色问问题': 'Ask from another role',
        '练习从不同视角看到不同重点': 'Practice seeing different priorities from different perspectives.',
        '视角切换师': 'Perspective Switcher',
        '多视角提问训练': 'Multi-Perspective Questioning',
        '你今天练的是：同一件事，不同角色最需要的问题并不一样。': 'Today you practiced that different roles need different questions for the same situation.',
        '公司想上线一个 AI 客服。 请分别从用户、客服团队、老板三个视角各问一个问题。': 'A company wants to launch an AI customer service agent.\n\nAsk one question each from the perspectives of the user, the customer service team, and the boss.',
        '用户会问……客服团队会问……老板会问……': 'The user would ask... the customer service team would ask... the boss would ask...',
        '对方说：“只要老板觉得效率提升，就可以上线。” 请用另一个角色视角追问它。': 'The other side says: "As long as the boss thinks efficiency improves, it can be launched."\n\nQuestion it from another role’s perspective.',
        '从用户角度：如果回答错了谁负责？……': 'From the user perspective: who is responsible if it answers incorrectly?...',
        '挑一个你正在处理的任务，从另一个人的视角补一个问题。': 'Pick a task you are working on and add one question from someone else’s perspective.',
        '如果我是……我会问……': 'If I were... I would ask...',

        '约束不是刹车，是发动机': 'Constraints are not brakes; they are engines',
        '练习在钱少、时间短、规则多时找新路': 'Practice finding new paths when money, time, and rules are limited.',
        '约束发明家': 'Constraint Inventor',
        '约束创新训练': 'Constraint Innovation Training',
        '你今天练的是：先接受限制，再让限制逼出不普通的方案。': 'Today you practiced accepting constraints first, then letting them force a non-obvious solution.',
        '约束：0 元预算、只用微信群、今天之内。 请为一个新读书会拉来前 20 个参与者。': 'Constraints: 0 RMB budget, WeChat group only, by the end of today.\n\nBring the first 20 participants to a new book club.',
        '我会利用已有关系、共创名单、限时挑战……': 'I would use existing relationships, a co-created list, a time-limited challenge...',
        '对方说：“没有预算很难做出传播。” 请反驳它，并给出一个低成本传播动作。': 'The other side says: "Without a budget, it is hard to create reach."\n\nRebut it and give one low-cost distribution action.',
        '预算少不等于不能传播，可以用……': 'A low budget does not mean no reach; we can use...',
        '写下你最近一个受限任务，并把限制改写成一个创意提示。': 'Write down a recent constrained task, and rewrite the constraint as a creative prompt.',
        '限制是……它可以逼我尝试……': 'The constraint is... It can force me to try...',

        '先搞砸，再反转': 'Fail it first, then reverse it',
        '练习用失败预演找到创新入口': 'Practice using failure rehearsal to find innovation entry points.',
        '逆向设计师': 'Reverse Designer',
        '逆向思维训练': 'Reverse Thinking Training',
        '你今天练的是：先把失败讲具体，再逐条反转成行动。': 'Today you practiced making failure concrete first, then reversing each point into action.',
        '如果你想让一个学习打卡群彻底没人坚持，你会做哪 3 件事？': 'If you wanted a learning check-in group to completely lose everyone, what three things would you do?',
        '比如规则太复杂、反馈太慢、目标太大……': 'For example: rules are too complex, feedback is too slow, goals are too large...',
        '对方说：“那就把这些失败点反过来就好了。” 请把其中 1 个反转成更具体的新设计。': 'The other side says: "Then just reverse those failure points."\n\nTurn one of them into a more concrete new design.',
        '如果失败点是反馈慢，反转不是“反馈快”，而是……': 'If the failure point is slow feedback, the reversal is not just "fast feedback," but...',
        '挑一个你想坚持的小习惯，写下一个“必败设计”和一个反转策略。': 'Pick a small habit you want to keep, and write one guaranteed-failure design plus one reversal strategy.',
        '必败设计是……反转策略是……': 'The guaranteed-failure design is... The reversal strategy is...',

        '把别处的办法借过来': 'Borrow a method from elsewhere',
        '练习跨领域迁移，而不是照搬答案': 'Practice cross-domain transfer, not copying answers.',
        '跨界搬运师': 'Cross-Domain Mover',
        '跨域迁移训练': 'Cross-Domain Transfer Training',
        '你今天练的是：借结构，不照抄；换场景，保留核心机制。': 'Today you practiced borrowing structure without copying, changing the context while keeping the core mechanism.',
        '把“游戏里的新手任务”迁移到“新人入职”场景。 你会设计什么？': 'Transfer "beginner quests in games" to the "new employee onboarding" context.\n\nWhat would you design?',
        '我会把入职拆成可见任务、即时反馈、阶段奖励……': 'I would break onboarding into visible tasks, instant feedback, stage rewards...',
        '对方说：“游戏是娱乐，入职是工作，不能类比。” 请说明哪里能类比，哪里不能类比。': 'The other side says: "Games are entertainment and onboarding is work, so they cannot be compared."\n\nExplain where the analogy works and where it does not.',
        '能类比的是反馈和路径；不能类比的是……': 'What can be compared is feedback and pathways; what cannot be compared is...',
        '找一个你熟悉领域的做法，把它迁移到今天的一个小任务里。': 'Find a practice from a field you know well, and transfer it to one small task today.',
        '我想借用……领域的……来解决……': 'I want to borrow... from the field of... to solve...',

        'AI 可以一本正经地胡说八道。你能看出来吗？': 'AI can sound completely confident while being wrong. Can you spot it?',
        '当模型能秒出万字长文，「信息多」不再是优势——能分辨哪些可信、哪些在偷换概念，才是你的护城河。': 'When models can generate long essays in seconds, having more information is no longer the edge. Your edge is knowing what is credible and what quietly shifts the terms.',
        '别人转发「专家说…」就信了': 'Others believe it as soon as they see "an expert says..."',
        '你会先问：这位专家的领域对口吗？': 'You first ask: is this expert speaking within their field?',
        '别人觉得「听起来有道理」': 'Others stop at "that sounds reasonable."',
        '你能一眼看出稻草人、滑坡、以偏概全': 'You can spot straw men, slippery slopes, and overgeneralization.',
        'AI 什么都能答——但答什么，取决于你怎么问。': 'AI can answer almost anything, but what it answers depends on how you ask.',
        '同样用 ChatGPT，有人得到一篇废话，有人得到可执行方案。差距不在工具，在问题本身的清晰度。': 'With the same AI tool, one person gets fluff and another gets an actionable plan. The difference is the clarity of the question.',
        '「帮我优化一下」→ 得到一堆正确的废话': '"Help me optimize this" -> a pile of correct but useless advice.',
        '「首页跳出率 72%，首屏加载 4s，怎么降到 50% 以下」→ 得到可落地的方案': '"Homepage bounce rate is 72%, first screen loads in 4s; how do we reduce bounce below 50%?" -> an actionable plan.',
        '开会两小时没结论': 'A two-hour meeting ends with no decision.',
        '三个问题把目标、瓶颈、下一步全对齐': 'Three questions align the goal, bottleneck, and next step.',
        '标准答案，AI 比你快一万倍。非标的呢？': 'For standard answers, AI is far faster than you. What about non-standard answers?',
        '能被标准化的工作正在被自动化。在约束里拧出新组合、把 A 领域的套路迁到 B——这是人最难被替代的部分。': 'Work that can be standardized is being automated. Creating new combinations under constraints and transferring patterns across domains is the part humans are hardest to replace in.',
        '等灵感，想不出来就放弃': 'Wait for inspiration and give up when it does not arrive.',
        '随手拿两个概念碰撞，先出 20 个点子再筛': 'Collide two concepts, generate 20 ideas, then filter.',
        '只在自己的行业里找方案': 'Look for solutions only inside your own industry.',
        '把外卖调度的逻辑搬到医院排班，反而是创新': 'Move food-delivery dispatch logic into hospital scheduling, and that becomes innovation.',

        '诉诸权威': 'Appeal to Authority',
        '用「某专家」背书，但专业领域不对口。': 'Using an expert endorsement when the expertise is in the wrong field.',
        '稻草人': 'Straw Man',
        '把对方观点歪曲成好反驳的版本再打倒。': 'Distorting the other side into an easier version to attack.',
        '滑坡论证': 'Slippery Slope',
        '声称 A 必然导致灾难性 Z，但中间链条没证明。': 'Claiming A inevitably leads to disastrous Z without proving the steps in between.',
        '虚假二分': 'False Dichotomy',
        '只给两个极端选项，忽略中间方案。': 'Offering only two extremes while ignoring middle options.',
        '以偏概全': 'Overgeneralization',
        '用少数例子推广到全体。': 'Generalizing from a few examples to everyone.',
        '相关当因果': 'Correlation as Causation',
        '两件事先后或同时出现，不等于有因果关系。': 'Two things happening together or in sequence does not prove causation.',
        '论点与论据': 'Claim and Evidence',
        '先分清结论是什么、理由有哪些，再判断理由是否充分。': 'First identify the conclusion and reasons, then judge whether the reasons are sufficient.',
        '隐藏假设': 'Hidden Assumption',
        '论证常依赖未说穿的前提，找出来才能检验。': 'Arguments often rely on unstated premises; find them before testing the argument.',
        '证据质量': 'Evidence Quality',
        '轶事、个例、传闻比可重复数据弱得多。': 'Anecdotes, isolated cases, and rumors are much weaker than repeatable data.',
        '正反练习': 'Both-Sides Practice',
        '同一议题先尽力为对立面找合理论据，再给出自己的取舍。': 'First build the best case for both sides, then make your own judgment.',
        '强弱论证': 'Strong vs. Weak Arguments',
        '好反驳会针对对方最强版本，而不是挑软柿子。': 'A good rebuttal addresses the strongest version of the opposing argument.',
        '从表象到机制': 'From Symptoms to Mechanisms',
        '先问发生了什么，再问为什么，再问该不该、怎么改。': 'Ask what happened, then why, then whether and how to change it.',
        '信息价值': 'Information Value',
        '优先问能改变决策的问题，而不是最好回答的问题。': 'Prioritize questions that can change decisions, not questions that are easiest to answer.',
        '模糊需求': 'Vague Request',
        '把「优化/提升/不好」翻译成对象、场景、指标和现状。': 'Translate "optimize/improve/not good" into object, context, metric, and current state.',
        '可调研': 'Researchable',
        '好问题应能通过数据、访谈或实验部分回答。': 'A good question can be partly answered through data, interviews, or experiments.',
        '角色立场': 'Role Perspective',
        '同一局面下，用户、老板、执行方各自最在意什么？': 'In the same situation, what does the user, boss, or executor care about most?',
        '约束不同': 'Different Constraints',
        '换角色时，优先级和禁忌往往不同，问题要跟着变。': 'When the role changes, priorities and taboos change too; the question should change with them.',
        '强制组合': 'Forced Combination',
        '把两个远概念硬拧在一起，再追问服务谁、解决什么。': 'Force two distant concepts together, then ask who it serves and what it solves.',
        '先多后少': 'Diverge, Then Filter',
        '先列出多种联系，再筛可行与有趣的方向。': 'List many connections first, then filter for feasible and interesting directions.',
        '预演失败': 'Pre-Mortem',
        '先具体列出「怎样一定搞砸」，再逐条反转成对策。': 'First list exactly how to fail, then reverse each item into a countermeasure.',
        '反转要落地': 'Make the Reversal Concrete',
        '反转后应是可执行动作，而不是空洞口号。': 'A reversal should become an executable action, not an empty slogan.',
        '约束即创意': 'Constraints Create Ideas',
        '钱少、时间紧、规则多会砍掉平庸方案，逼出新形态。': 'Limited money, time, and rules cut away generic solutions and force new forms.',
        '在框内跳舞': 'Dance Inside the Box',
        '先接受硬约束，再在剩余空间里极大化目标。': 'Accept the hard constraints first, then maximize the goal within the remaining space.',
        '迁移不是照抄': 'Transfer Is Not Copying',
        '借 A 领域成熟套路的「结构」，填 B 领域的「内容」。': 'Borrow the structure of a mature pattern from domain A and fill it with content from domain B.',
        '类比边界': 'Analogy Boundaries',
        '能说清哪里像、哪里不像，迁移才可靠。': 'Transfer is reliable only when you can explain where the analogy fits and where it breaks.',

        '请阅读这段话：「张教授是物理学权威，他说这款保健品有效，所以一定有效。」 这段论证的逻辑有什么问题？请指出谬误类型并解释。': 'Read this statement: "Professor Zhang is an authority in physics. He says this health product works, so it must work."\n\nWhat is the logical problem in this argument? Identify the fallacy and explain it.',
        '请看这四句话，判断哪些是「事实」哪些是「观点」，并解释你的判断标准： 1. 中国是世界上最伟大的国家 2. 2023年中国GDP总量约为126万亿元人民币 3. 经济增长比环境保护更重要 4. 人工智能将在10年内取代大部分工作': 'Look at these four statements. Decide which are facts and which are opinions, and explain your criteria:\n\n1. China is the greatest country in the world\n2. China\'s GDP in 2023 was about 126 trillion RMB\n3. Economic growth is more important than environmental protection\n4. AI will replace most jobs within 10 years',
        '有人说：「既然我们无法确保AI100%安全，那就不应该发展AI。」 请找出这个论证的逻辑漏洞，并用 2-3 句话反驳。': 'Someone says: "Since we cannot make AI 100% safe, we should not develop AI."\n\nFind the logical flaw and rebut it in 2-3 sentences.',
        '「每次我洗车后第二天都会下雨，所以洗车会导致下雨。」': '"Every time I wash my car, it rains the next day, so washing my car causes rain."',
        '这段话的推理有什么问题？请指出谬误类型并用自己的话解释为什么这个推理不成立。': 'What is wrong with this reasoning? Identify the fallacy and explain in your own words why the reasoning fails.',
        '「你要么支持完全开放AI，要么你就是反对科技进步。」': '"Either you support fully opening AI, or you oppose technological progress."',
        '这段话的逻辑有什么漏洞？请指出谬误并解释现实中这个问题为什么不是非此即彼的。': 'What is the logical flaw here? Identify the fallacy and explain why the real issue is not either-or.',
        '「反对者说我们应该削减军费，但他们显然想让国家毫无防御能力，任人宰割。」': '"Opponents say we should reduce military spending, but clearly they want the country to have no defense and be at everyone\'s mercy."',
        '这段反驳的手法有什么问题？它准确地回应了反对者的原始观点吗？请分析。': 'What is wrong with this rebuttal? Does it accurately respond to the opponent\'s original view? Analyze it.',
        '「如果我们允许学生用AI写作业，接下来他们就会用AI写考试，然后用AI写毕业论文，最后整个教育体系就崩溃了。」': '"If we allow students to use AI for homework, next they will use AI for exams, then for graduation theses, and finally the whole education system will collapse."',
        '这段话预测了一连串后果。这种推理方式可靠吗？请指出问题并解释。': 'This statement predicts a chain of consequences. Is this reasoning reliable? Identify the problem and explain it.',
        '「这个减肥产品一定有效，因为已经有100万人购买了。」': '"This weight-loss product must work because one million people have bought it."',
        '「买的人多」能证明产品有效吗？请分析这段话的逻辑问题。': 'Can "many people bought it" prove that a product works? Analyze the logical problem.',
        '一篇文章标题写道：「成功人士都早起！你也应该5点起床。」文中列举了几位早起的CEO作为证据。': 'An article headline says: "Successful people all wake up early! You should wake up at 5 a.m. too." The article lists several early-rising CEOs as evidence.',
        '这篇文章用几位 CEO 的例子来论证「早起导致成功」，这个论证有哪些问题？请尽可能多地指出。': 'This article uses several CEOs as examples to argue that "waking up early causes success." What problems does this argument have? Identify as many as you can.',
        '有人主张：「应该禁止所有社交媒体，因为社交媒体导致青少年抑郁。」 请找出至少 2 个论证漏洞。': 'Someone argues: "All social media should be banned because social media causes teen depression."\n\nFind at least two weaknesses in this argument.',
        '有人说：「AI生成的画作获得了艺术大赛的奖项，这证明AI的创造力已经超越了人类。」 请反驳这个论点。': 'Someone says: "An AI-generated artwork won an art competition, which proves that AI creativity has surpassed human creativity."\n\nRebut this claim.',
        '有人说：「既然大数据能预测犯罪高发区域，我们就应该在这些区域加强巡逻和盘查。」 请分析这个主张可能存在的问题。': 'Someone says: "Since big data can predict high-crime areas, we should increase patrols and checks in those areas."\n\nAnalyze the possible problems with this claim.',
        '学校应该用AI来批改作文': 'Schools should use AI to grade essays.',
        '请就「学校应该用AI来批改作文」这个话题： 1. 先写出正方（支持）的 2 个核心论点 2. 再写出反方（反对）的 2 个核心论点 3. 最后给出你自己的判断和理由': 'For the topic "Schools should use AI to grade essays":\n\n1. Write two core arguments for the supporting side\n2. Write two core arguments for the opposing side\n3. Finally, give your own judgment and reasons',

        '你刚加入一个新团队，需要快速了解情况。你会优先问哪 3 个问题？请按信息价值从高到低排列，并解释为什么这个顺序最合理。': 'You have just joined a new team and need to understand the situation quickly. Which three questions would you ask first? Rank them by information value and explain why the order makes sense.',
        '老板说：「我们的用户增长太慢了，想想办法。」 请把这个模糊的需求转化为 3 个具体的、可调研的问题。': 'Your boss says: "Our user growth is too slow. Think of something."\n\nTurn this vague request into three specific, researchable questions.',
        '针对「AI会取代人类工作」这个话题，请从以下三个不同视角各提出一个深度问题： 1. 经济学家视角 2. 一线工人视角 3. AI研究员视角': 'For the topic "AI will replace human jobs," ask one deep question from each of these perspectives:\n\n1. Economist\n2. Frontline worker\n3. AI researcher',
        '你发现团队最近加班越来越多。': 'You notice that your team has been working more overtime recently.',
        '请针对「团队加班越来越多」这个现象，按从浅到深的顺序提出 4 个问题。 要求：第1个是表层问题，第4个要触及根本原因。': 'For the phenomenon "the team is working more overtime," ask four questions from shallow to deep.\n\nRequirement: the first should be surface-level, and the fourth should reach the root cause.',
        '一个朋友告诉你：「我觉得AI会让我失业。」': 'A friend tells you: "I think AI will make me lose my job."',
        '请针对朋友的担忧，按从浅到深的顺序提出 4 个问题，帮助他/她厘清思路。': 'Ask four questions, from shallow to deep, to help your friend clarify this concern.',
        '新闻报道：某城市房价连续3个月下跌。': 'News report: Housing prices in a city have fallen for three consecutive months.',
        '如果你是一个分析师，需要理解这个现象的深层原因，请从浅到深提出 4 个关键问题。': 'If you were an analyst trying to understand the deeper causes, ask four key questions from shallow to deep.',
        '「我们的App体验不好，优化一下。」': '"Our app experience is not good. Optimize it."',
        '你的老板说：「我们的App体验不好，优化一下。」 请将这个模糊需求转化为 3 个精确的、可执行的问题。': 'Your boss says: "Our app experience is not good. Optimize it."\n\nTurn this vague request into three precise, actionable questions.',
        '「我们需要一个更好的推荐算法。」': '"We need a better recommendation algorithm."',
        '产品经理说：「我们需要一个更好的推荐算法。」 请将这个模糊需求转化为 3 个精确的问题，帮助明确真正要解决的问题。': 'A product manager says: "We need a better recommendation algorithm."\n\nTurn this vague request into three precise questions that clarify the real problem.',
        '一家公司决定全面采用远程办公': 'A company decides to fully adopt remote work.',
        '「一家500人的科技公司宣布全面转为远程办公」 请分别从以下视角各提出 1 个有深度的问题： 1. CEO 2. 基层员工 3. HR负责人 4. 客户': '"A 500-person technology company announces a full shift to remote work."\n\nAsk one deep question from each perspective:\n1. CEO\n2. Frontline employee\n3. Head of HR\n4. Customer',

        '请用「火锅」和「版本控制」这两个毫不相关的概念，创造一个有趣的产品创意或商业点子。 要求：说清楚它是什么、解决什么问题、为什么有趣。': 'Use the unrelated concepts "hot pot" and "version control" to create an interesting product idea or business idea.\n\nExplain what it is, what problem it solves, and why it is interesting.',
        '如果你想让一个「读书会」彻底失败，你会怎么做？请列出 3 个方法。 然后，把这 3 个方法反转过来，变成让读书会成功的策略。': 'If you wanted a book club to fail completely, what would you do? List three methods.\n\nThen reverse those three methods into strategies that help a book club succeed.',
        '你只有 100 元预算和 3 天时间，要为一个社区设计一场让至少 50 人参与的活动。 请描述你的方案。': 'You have a budget of 100 RMB and three days to design a community activity that attracts at least 50 participants.\n\nDescribe your plan.',
        '雨伞': 'Umbrella',
        '社交网络': 'Social Network',
        '请用「雨伞」和「社交网络」创造一个产品创意。 要求：解释它是什么、解决什么问题、目标用户是谁。': 'Use "umbrella" and "social network" to create a product idea.\n\nExplain what it is, what problem it solves, and who the target users are.',
        '图书馆': 'Library',
        '健身': 'Fitness',
        '请用「图书馆」和「健身」创造一个创新的服务概念。': 'Use "library" and "fitness" to create an innovative service concept.',
        '菜市场': 'Wet Market',
        '区块链': 'Blockchain',
        '请用「菜市场」和「区块链」创造一个商业模式。 要求：说清楚它解决什么现实问题，为什么需要结合这两者。': 'Use "wet market" and "blockchain" to create a business model.\n\nExplain what real-world problem it solves and why these two concepts need to be combined.',
        '外婆': 'Grandmother',
        '元宇宙': 'Metaverse',
        '请用「外婆」和「元宇宙」创造一个产品或服务概念。': 'Use "grandmother" and "metaverse" to create a product or service concept.',
        '一款学习App': 'A learning app',
        '如果你想让一款学习App「用户绝对不想用」，你会怎么设计？请列出 3 个「必败」设计。 然后将每个「必败」设计反转，变成一个创新的设计策略。': 'If you wanted to design a learning app that users absolutely do not want to use, how would you design it? List three guaranteed-failure designs.\n\nThen reverse each failure design into an innovative design strategy.',
        '团队协作': 'Team collaboration',
        '如果你想让一个团队的协作「彻底崩溃」，你会做哪 3 件事？ 然后反转每一条，提出一个提升团队协作的创新方法。': 'If you wanted team collaboration to collapse completely, what three things would you do?\n\nThen reverse each one into an innovative way to improve team collaboration.',
        '城市交通': 'Urban transportation',
        '如果你想让一个城市的交通「彻底瘫痪」，你会实施哪 3 个政策？ 然后反转，提出 3 个创新的交通改善方案。': 'If you wanted a city\'s traffic to become completely paralyzed, what three policies would you implement?\n\nThen reverse them into three innovative traffic improvement plans.',
        '约束条件：0 元预算、只用微信、1 天时间。 任务：为一个刚起步的独立咖啡店获得前 100 个客户。 请给出你的具体方案。': 'Constraints: 0 RMB budget, WeChat only, one day.\n\nTask: Help a new independent coffee shop get its first 100 customers.\n\nGive your concrete plan.',
        '约束条件：不用任何屏幕（手机/电脑/电视），预算 50 元以内。 任务：设计一个让 10 个陌生人在 2 小时内成为朋友的活动。 请给出详细方案。': 'Constraints: no screens of any kind (phone/computer/TV), budget under 50 RMB.\n\nTask: Design an activity that helps 10 strangers become friends within two hours.\n\nGive a detailed plan.',
        "餐饮行业的'试吃'模式": 'The free-sample model in food service',
        '企业招聘': 'Corporate recruiting',
        '餐饮行业有一个经典策略：「免费试吃」。 请把这个概念迁移到「企业招聘」领域，设计一个创新的招聘方式。 说明：怎么做、为什么有效、可能的风险。': 'The food service industry has a classic strategy: "free samples."\n\nTransfer this concept to corporate recruiting and design an innovative hiring method.\n\nExplain how it works, why it is effective, and the possible risks.'
    };

    var PATTERNS = [
        [/^(.+) 的健脑房$/, '$1\'s BrainGym'],
        [/^累计训练 (\d+) 题$/, '$1 exercises completed'],
        [/^已连续 (\d+) 天有训练$/, '$1-day training streak'],
        [/^连续 (\d+) 天$/, '$1-day streak'],
        [/^本周 (\d+) 天$/, 'This week: $1 days'],
        [/^共练 (\d+) 题次$/, '$1 sessions'],
        [/^最近 (\d+) 条$/, 'Latest $1 items'],
        [/^本周已有 (\d+) 天来过 · 共练 (\d+) 题次$/, '$1 active days this week · $2 sessions'],
        [/^已训练 (\d+) 题$/, '$1 exercises completed'],
        [/^已训练 (\d+) 题 · 平均 (\d+) 分$/, '$1 exercises completed · avg $2 pts'],
        [/^当前第 (\d+) 档$/, 'Current tier $1'],
        [/^今日主题：(.+)$/, function(_, topic) {
            return "Today's theme: " + (translateText(topic) || topic);
        }],
        [/^第 (\d+) 站$/, 'Station $1'],
        [/^如果对方追问「(.+)」，你会怎么补上？$/, 'If the other side asks about "$1", how would you fill that gap?'],
        [/^第 (\d+) \/ (\d+) 题$/, 'Question $1 / $2'],
        [/^(\d+) \/ (\d+)$/, '$1 / $2'],
        [/^(.+) 的思维能力评估$/, '$1\'s thinking ability assessment'],
        [/^(\d+)分$/, '$1 pts'],
        [/^去看 (.+) 完整说明 →$/, 'View the full $1 guide ->'],
        [/^打开 (.+) 能力说明 →$/, 'Open the $1 ability guide ->'],
        [/^开始练 (.+) →$/, 'Train $1 ->'],
        [/^(.+) · 三站式脑力循环$/, function(_, dim) {
            return (translateText(dim) || dim) + ' · three-station brain loop';
        }],
        [/^(.+) · (.+)$/, function(_, left, right) {
            return (translateText(left) || left) + ' · ' + (translateText(right) || right);
        }],
    ];

    function storageGet(key, fallback) {
        try {
            return sessionStorage.getItem(key) || fallback;
        } catch (e) {
            return fallback;
        }
    }

    function storageSet(key, value) {
        try {
            sessionStorage.setItem(key, value);
        } catch (e) {
            // Language choice is nice-to-have.
        }
    }

    function normalize(text) {
        return (text || '').trim().replace(/\s+/g, ' ');
    }

    function hasChinese(text) {
        return CHINESE_RE.test(text || '');
    }

    function splitText(value) {
        var source = value || '';
        return {
            leading: (source.match(/^\s*/) || [''])[0],
            trailing: (source.match(/\s*$/) || [''])[0],
            core: source.trim()
        };
    }

    function translateText(text) {
        var key = normalize(text);
        var exact = EXACT[key];
        if (exact) {
            return exact;
        }
        for (var i = 0; i < PATTERNS.length; i += 1) {
            if (PATTERNS[i][0].test(key)) {
                return key.replace(PATTERNS[i][0], PATTERNS[i][1]);
            }
        }
        return null;
    }

    function isIgnoredElement(el) {
        return !el || !!el.closest('[data-no-translate], script, style, noscript, svg, canvas');
    }

    function getTextEntry(node) {
        if (node.__brainGymTranslation) {
            return node.__brainGymTranslation;
        }
        var parts = splitText(node.nodeValue || '');
        if (!parts.core || !hasChinese(parts.core)) {
            return null;
        }
        node.__brainGymTranslation = {
            original: node.nodeValue || '',
            core: parts.core,
            leading: parts.leading,
            trailing: parts.trailing
        };
        return node.__brainGymTranslation;
    }

    function collectTextTargets() {
        var targets = [];
        var walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            {
                acceptNode: function(node) {
                    if (isIgnoredElement(node.parentElement)) {
                        return NodeFilter.FILTER_REJECT;
                    }
                    if (node.__brainGymTranslation) {
                        return NodeFilter.FILTER_ACCEPT;
                    }
                    var text = (node.nodeValue || '').trim();
                    if (!text || !hasChinese(text)) {
                        return NodeFilter.FILTER_REJECT;
                    }
                    return NodeFilter.FILTER_ACCEPT;
                }
            }
        );

        var node = walker.nextNode();
        while (node) {
            var entry = getTextEntry(node);
            if (entry) {
                targets.push({ type: 'text', node: node, text: entry.core, entry: entry });
            }
            node = walker.nextNode();
        }
        return targets;
    }

    function getAttrStore(el) {
        if (!el.__brainGymTranslationAttrs) {
            el.__brainGymTranslationAttrs = {};
        }
        return el.__brainGymTranslationAttrs;
    }

    function collectAttrTargets() {
        var targets = [];
        var elements = document.querySelectorAll('[placeholder], [title], [aria-label]');
        elements.forEach(function(el) {
            if (isIgnoredElement(el)) {
                return;
            }
            var store = getAttrStore(el);
            ATTRS.forEach(function(attr) {
                var current = el.getAttribute(attr);
                if (!current) {
                    return;
                }
                if (!store[attr]) {
                    if (!hasChinese(current)) {
                        return;
                    }
                    store[attr] = current;
                }
                targets.push({ type: 'attr', element: el, attr: attr, text: store[attr] });
            });
        });
        return targets;
    }

    function collectTitleTarget() {
        if (!document.__brainGymOriginalTitle && hasChinese(document.title)) {
            document.__brainGymOriginalTitle = document.title;
        }
        if (!document.__brainGymOriginalTitle) {
            return [];
        }
        return [{ type: 'title', text: document.__brainGymOriginalTitle }];
    }

    function collectTargets() {
        return collectTextTargets().concat(collectAttrTargets(), collectTitleTarget());
    }

    function setStatus(message) {
        var status = document.getElementById('translationStatus');
        if (!status) {
            return;
        }
        window.clearTimeout(statusTimer);
        status.textContent = message || '';
        status.classList.toggle('show', !!message);
        if (message) {
            statusTimer = window.setTimeout(function() {
                status.classList.remove('show');
            }, 1800);
        }
    }

    function setButton(lang) {
        var button = document.getElementById('languageToggle');
        if (!button) {
            return;
        }
        button.textContent = lang === 'en' ? '\u4e2d\u6587' : 'English';
        button.disabled = false;
        button.setAttribute('aria-label', lang === 'en' ? 'Restore Chinese' : 'Switch to English');
    }

    function applyEnglish() {
        window.clearTimeout(scheduleTranslate.timer);
        translating = true;
        collectTargets().forEach(function(target) {
            var translated = translateText(target.text);
            if (!translated) {
                return;
            }
            if (target.type === 'text') {
                target.node.nodeValue = target.entry.leading + translated + target.entry.trailing;
            } else if (target.type === 'attr') {
                target.element.setAttribute(target.attr, translated);
            } else if (target.type === 'title') {
                document.title = translated;
            }
        });
        document.documentElement.lang = 'en';
        storageSet(LANG_KEY, 'en');
        setButton('en');
        translating = false;
    }

    function restoreChinese() {
        window.clearTimeout(scheduleTranslate.timer);
        translating = true;
        storageSet(LANG_KEY, 'zh');
        collectTargets().forEach(function(target) {
            if (target.type === 'text') {
                target.node.nodeValue = target.entry.original;
            } else if (target.type === 'attr') {
                target.element.setAttribute(target.attr, target.text);
            } else if (target.type === 'title') {
                document.title = target.text;
            }
        });
        document.documentElement.lang = 'zh-CN';
        setButton('zh');
        translating = false;
        window.clearTimeout(scheduleTranslate.timer);
        setStatus(EXACT['已恢复中文']);
    }

    function scheduleTranslate() {
        if (translating || storageGet(LANG_KEY, 'zh') !== 'en') {
            return;
        }
        window.clearTimeout(scheduleTranslate.timer);
        scheduleTranslate.timer = window.setTimeout(applyEnglish, 40);
    }

    function initObserver() {
        if (observer) {
            observer.disconnect();
        }
        observer = new MutationObserver(scheduleTranslate);
        observer.observe(document.body, {
            subtree: true,
            childList: true,
            characterData: true,
            attributes: true,
            attributeFilter: ATTRS
        });
    }

    function init() {
        var button = document.getElementById('languageToggle');
        if (!button) {
            return;
        }

        button.addEventListener('click', function() {
            var lang = storageGet(LANG_KEY, 'zh');
            if (lang === 'en') {
                restoreChinese();
            } else {
                applyEnglish();
                setStatus('English');
            }
        });

        var currentLang = storageGet(LANG_KEY, 'zh');
        setButton(currentLang === 'en' ? 'en' : 'zh');
        if (currentLang === 'en') {
            applyEnglish();
        }
        initObserver();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
