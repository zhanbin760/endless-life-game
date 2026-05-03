"""
人生无限游戏 · 万维钢版月度陪伴计划
Streamlit 版本
"""

import streamlit as st
import json
import hashlib
from datetime import datetime
from typing import Optional

# Page config
st.set_page_config(
    page_title="人生无限游戏 · 万维钢版月度陪伴计划",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
    }
    .week-card {
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .week-card:hover {
        transform: translateY(-2px);
    }
    .week-card h3 {
        margin-top: 0;
    }
    .prompt-box {
        background-color: #f0f0f0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4A6FA5;
        margin: 0.5rem 0;
        font-family: monospace;
        white-space: pre-wrap;
    }
    .day-header {
        background: linear-gradient(90deg, #4A6FA5, #6B8F71);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .tool-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
    }
</style>
""", unsafe_allow_html=True)

# ===================================================================
# Data
# ===================================================================

WEEKLY_DATA = [
    {
        "id": 1,
        "title": "记录习惯",
        "subtitle": "建立认知回路",
        "icon": "📝",
        "color": "#4A6FA5",
        "summary": "每天记录，在你的认知回路中插入处理环节。不求完美，只求开始。",
        "tools": [
            {"name": "第一性原理", "summary": "回到为什么", "detail": "记录的第一性原理：今天的你，替未来的你，留下一点东西。不求有用，只求真实。不求深刻，只求存在。降低启动成本，是长期主义的第一步。"},
            {"name": "元认知", "summary": "对思考的思考", "detail": "记录就是元认知的最小化实践。当你写下焦虑的那一刻，你就在做两件事：感受焦虑（本能），观察自己在焦虑（元认知）。这两件事之间的距离，就是普通人和高手的差距。"},
            {"name": "反脆弱", "summary": "小步积累的力量", "detail": "每天写三句话，具备反脆弱的特征：低成本（每天5分钟）、高频次（每天一次）、收益不可预测。真正的优势不是某一次的大爆发，而是持续的小积累。连续性比完美性重要一万倍。"}
        ],
        "quote": "降低启动成本，是长期主义的第一步。连续性比完美性重要一万倍。",
        "days": [
            {
                "id": "w1-d1", "period": "Day 1-2", "title": "启动", "subtitle": "做，不要想",
                "content": "<h3>🎯 目标：写下第一条记录</h3><p>你有没有过这样的体验——刷了一天手机，晚上躺在床上回想，好像什么都没留下。那些看过的文章、听过的播客、群里讨论过的话题，像沙子一样从指缝漏掉了。</p><p>这不是你的记忆力出了问题。</p><p><strong>认知回路（Cognitive Loop）</strong>——人的认知是一个输入→处理→输出的闭环。信息进来，你消化它，然后产生新的想法或者行动——这才是一个完整的回路。</p><p>问题在于，大多数人的回路是断的。信息进来，没有经过思考的消化，直接就流失了。</p><p><strong>你不是没有想法。你是没有给想法一个停留的机会。</strong></p><p>每日真实记录，就是强行在你的认知回路里插入一个处理环节。哪怕只写三句话，你也在做一件事：让信息在你脑子里多待一会儿，被你真正消化。</p><h4>具体做法：</h4><ul><li>选一个模板。推荐从「每日复盘」或「碎片灵感」开始</li><li>今天就写。不要等到有灵感，不要等到有整块时间</li><li>哪怕只写3句话，也算完成</li></ul><p><strong>第一天最大的敌人不是写得不好，是还没开始写。</strong></p>",
                "prompts": [
                    {"name": "💡 碎片灵感捕捉", "text": "请帮我扩展今天的一个灵感碎片。\n我想到的是：[描述你的灵感]\n\n请帮我：\n1. 从这个灵感出发，延伸出 2-3 个相关的角度\n2. 用一句话说清楚这个灵感的核心价值\n3. 问一个能帮我深入思考这个问题的问题"},
                    {"name": "📋 每日复盘模板", "text": "📅 今日复盘\n┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅\n\n1️⃣ 今天让我印象最深刻的一件事\n（发生了什么？为什么印象深刻？）\n\n2️⃣ 今天的情绪关键词\n（用一个词描述今天的主要情绪）\n\n3️⃣ 今天的一个小发现\n（学到了什么？想到了什么？）\n\n4️⃣ 明天的 1 个小目标\n（最小行动，一句话说完）"}
                ],
                "tasks": ["选定至少 1 个记录模板", "写下第一条记录，哪怕只有 3 句话"]
            },
            {
                "id": "w1-d2", "period": "Day 3-4", "title": "适应", "subtitle": "探索节奏",
                "content": "<h3>🎯 目标：尝试不同模板，找到感觉</h3><p>你已经迈出了第一步。现在，让记录变得更有趣一点。</p><p><strong>元认知（Meta-cognition）</strong>——万维钢区分高手和普通人的关键概念。普通人只知道自己在想什么，高手能观察自己在怎么想。</p><p>记录，就是元认知的最小化实践。当你写下文字的那一刻，你就在审视自己的想法。</p><h4>具体做法：</h4><ul><li>换一种模板记录。比如之前用「每日复盘」，今天试试「碎片灵感」或「问题追踪」</li><li>用 AI 帮你扩展一个灵感碎片（但记住：AI 是你的镜子，不是你的嘴替）</li><li>在社群里分享一个你记录中的发现</li></ul><p>万维钢说：输出是最高效的输入方式。</p>",
                "prompts": [
                    {"name": "🔗 问题追踪模板", "text": "🔍 问题追踪\n┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅\n\n1️⃣ 我当前在纠结/困惑的问题\n（一句话说清楚）\n\n2️⃣ 我尝试过的思路\n（列 1-2 个我想过的方向）\n\n3️⃣ 我还缺什么信息？\n（如果能知道一件事，会是什么？）\n\n4️⃣ 换个角度问\n（如果是我敬佩的人，TA 会怎么看这个问题？）"},
                    {"name": "🧠 AI 灵感扩展提示词", "text": "你是一位思维教练。我的记录片段是：\n[在此粘贴你的记录]\n\n请帮我：\n1. 从这个片段中提炼出一个值得深入探讨的主题\n2. 提供 3 个我可能没意识到的角度\n3. 用一句话总结：我今天记录的核心洞察是什么？\n4. 问一个能引导我明天继续思考的问题\n\n注意：请用简洁、有温度的语言，不要套话和鸡汤。"}
                ],
                "tasks": ["尝试过至少 2 种不同模板", "用 AI 扩展一个灵感碎片", "在社群分享 1 次记录中的发现"]
            },
            {
                "id": "w1-d3", "period": "Day 5-7", "title": "固化", "subtitle": "建立正反馈",
                "content": "<h3>🎯 目标：回顾一周，发现模式，确定节奏</h3><p>一周即将结束。你可能觉得也没写什么了不起的东西。</p><p>这正是重点——记录的价值不在于任何单一条目，而在于积累本身形成的<strong>认知密度</strong>。你还没看到效果，是因为时间还不够长。</p><p><strong>反脆弱</strong>——每天写三句话，看似微不足道，但它具备反脆弱的特征：低成本、高频次、收益不可预测但长期复利。</p><h4>具体做法：</h4><ul><li>通读这周的所有记录</li><li>问自己：有没有什么让我<strong>惊讶</strong>的发现？</li><li>用 AI 复盘整理提示词分析一周</li><li>确定最适合你的记录节奏和模板</li></ul><p>不一定每天都要记，但一定要持续。</p>",
                "prompts": [
                    {"name": "📊 AI 复盘整理提示词", "text": "你是一位思维教练。以下是我本周的所有记录：\n[粘贴本周所有记录]\n\n请帮我复盘：\n1. 本周出现了哪些重复的主题/情绪/问题？\n2. 哪些记录最有能量？为什么？\n3. 我可能有哪些思维盲区？\n4. 下周我可以在哪个方向深入探索？\n5. 用一句话总结本周的认知收获\n\n风格要求：直接、有洞察、不带鸡汤。"},
                    {"name": "📝 情绪日记模板", "text": "🌤 情绪日记\n┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅\n\n1️⃣ 当前情绪状态\n（用 1-2 个词描述）\n\n2️⃣ 触发事件\n（发生了什么让我有这种情绪？）\n\n3️⃣ 我的反应\n（我做了什么？说了什么？想了什么？）\n\n4️⃣ 另一种可能\n（有没有另一种方式看待这件事？）\n\n5️⃣ 我需要什么？\n（安慰？行动？休息？还是更多信息？）"}
                ],
                "tasks": ["完成至少 5 条记录（总量）", "通读一周记录做回顾", "确定最适合的记录节奏和模板"]
            }
        ]
    },
    {
        "id": 2,
        "title": "借骨还魂",
        "subtitle": "让记录变成作品",
        "icon": "✍️",
        "color": "#E8A87C",
        "summary": "从记录中选出素材，用 AI 搭骨架，用自己的内容填灵魂，完成第一篇完整作品。",
        "tools": [
            {"name": "反常识", "summary": "先有骨架，再填血肉", "detail": "好文章是组装出来的，不是灵感涌现出来的。先确定这篇文章要说什么（骨架），再往每个部分填内容。AI 可以帮你搭骨架，但它不能替你填灵魂。"},
            {"name": "弱联系", "summary": "创新来自连接", "detail": "你第一周记录的碎片看起来分散、不相关。但当你把它们放在一起，你会发现弱联系——灵感碎片 A 和情绪日记 B 可能在说同一件事。创作的本质，就是发现弱联系并把它们连接起来。"},
            {"name": "最小可行产品 (MVP)", "summary": "先完成，再完美", "detail": "第二周的目标不是写出一篇爆款，而是写出一篇完整的作品。完整的意思是：有开头、有中间、有结尾，逻辑通顺，表达清楚。完成比完美重要——只有完成了，你才有东西可以迭代。"}
        ],
        "quote": "如果你不能说清楚一件事，说明你还没想清楚。完成比完美重要——只有完成了，才有迭代的机会。",
        "days": [
            {
                "id": "w2-d1", "period": "Day 8-9", "title": "拆解与选材", "subtitle": "从记录中挖掘宝藏",
                "content": "<h3>🎯 目标：从第一周记录中选出最有感觉的素材</h3><p>大多数人以为写作是这样的：坐在电脑前，灵感涌现，笔走龙蛇，一气呵成。如果有哪天灵感不来，就写不出来。</p><p><strong>这是幻觉。</strong></p><p>好的作品不是等灵感来了写出来的，而是<strong>组装出来的</strong>。</p><p>第一周你做的记录，就是在收集这些散落的碎片。第二周我们要做的事，就是把这些碎片组装成一件完整的作品。</p><p>方法叫<strong>借骨还魂术</strong>：</p><ul><li><strong>借骨</strong>：用 AI 帮你搭好文章的结构（骨架）</li><li><strong>还魂</strong>：你往骨架里填入自己真实的经历、想法和语言（灵魂）</li></ul><h4>具体做法：</h4><ul><li>重读你第一周的所有记录</li><li>标记出让你有感觉的条目——不是写得最好的，而是最有情绪共鸣的</li><li>至少选出 3 条</li></ul><p>问自己：这条记录为什么打动了我？它和我生活中的哪些经历有关？如果我要围绕这个主题写一篇文章，我会说什么？</p>",
                "prompts": [
                    {"name": "🔍 素材筛选提示词", "text": "以下是我第一周的所有记录：\n[粘贴所有记录]\n\n请帮我：\n1. 识别出 3 条最有能量的记录（最有情绪共鸣、最值得深挖的）\n2. 对每条记录，说明它可能的主题方向\n3. 建议这些素材可以组合成什么类型的文章\n4. 推荐一个最值得优先创作的主题"}
                ],
                "tasks": ["重读第一周所有记录", "选出至少 3 条有感觉的素材", "想清楚每条记录为什么打动你"]
            },
            {
                "id": "w2-d2", "period": "Day 10-11", "title": "搭骨架", "subtitle": "用 AI 构建文章结构",
                "content": "<h3>🎯 目标：用 AI 把选出的素材搭成文章结构</h3><p><strong>创新来自弱联系</strong>——万维钢多次引用社会学中的弱联系理论：真正有价值的创新和信息，往往不是来自你熟悉的人，而是来自你不太熟的人。</p><p>这个原理同样适用于创作。你第一周记录的碎片灵感、每日复盘、情绪日记——它们看起来是分散的、不相关的。但当你把它们放在一起看，你会发现一些弱联系。</p><p>创作的本质，就是发现弱联系并把它们连接起来。</p><h4>具体做法：</h4><ul><li>把你选出的素材和主题发给 AI，让它帮你搭一个文章骨架</li><li>审视 AI 搭的骨架：你觉得这个结构好吗？有没有想调整的地方？</li><li>大胆改——这是你的文章，AI 只是助手</li></ul><p><strong>关键原则：AI 搭骨（结构），你填魂（真实内容）。</strong></p>",
                "prompts": [
                    {"name": "🏗 AI 结构搭建提示词", "text": "你是一位写作教练。以下是我选出的素材和主题：\n\n主题：[输入你的文章主题]\n素材：[粘贴选出的记录]\n\n请帮我搭建一个文章骨架：\n1. 推荐文章结构（如：问题→分析→案例→结论）\n2. 每个部分的核心要点（用一句话概括）\n3. 每个部分建议用什么素材填入\n4. 整体预计篇幅（字数建议）\n\n要求：结构清晰、逻辑通顺、便于我往里面填内容。"},
                    {"name": "🎨 AI 风格学习提示词", "text": "以下是我写的一些记录片段：\n[粘贴 3-5 条你的记录]\n\n请分析我的写作风格：\n1. 我的语言特点（句式、用词偏好、语气）\n2. 我习惯的叙事方式（感性/理性、细节/概括、比喻/直白）\n3. 我独特的味道是什么？\n4. 给出 3 条建议：如何保持我的风格，同时让表达更清晰有力？\n5. 模仿我的风格，重写下面这段话：[输入一段你想润色的文字]"}
                ],
                "tasks": ["用 AI 搭出 1 篇文章骨架", "用 AI 风格学习提示词确认自己的表达风格", "审视并调整骨架"]
            },
            {
                "id": "w2-d3", "period": "Day 12-14", "title": "成品", "subtitle": "完成第一篇作品",
                "content": "<h3>🎯 目标：完成第一篇完整作品并发布</h3><p>万维钢讲创业和产品时经常用<strong>MVP（Minimum Viable Product）</strong>概念：不要追求一次性做出完美产品，先做一个刚好能用的版本，发布出去，根据反馈迭代。</p><p>写文章也是一样。第二周的目标不是写出一篇爆款，而是写出一篇<strong>完整</strong>的作品。</p><p>它可以不惊艳、不深刻、不精致。但它必须是完整的。</p><h4>具体做法：</h4><ul><li><strong>Day 12 填内容：</strong>按照骨架，往每个部分填入你的真实经历、想法和语言。不要追求完美，先把骨架填满。</li><li><strong>Day 13 打磨：</strong>用 AI 内容润色提示词优化表达，但保持自己的味道</li><li><strong>Day 14 发布：</strong>在社群、朋友圈或公众号发布。接受反馈，不要害怕。</li></ul><p>AI 给你效率，你给文章灵魂。这就叫借骨还魂。</p>",
                "prompts": [
                    {"name": "✨ AI 内容润色提示词", "text": "以下是我写的一篇文章草稿：\n[粘贴你的文章草稿]\n\n请帮我润色：\n1. 保持我的语言风格和味道\n2. 优化句子流畅度（不改变原意）\n3. 建议 2-3 处可以更生动的表达\n4. 检查逻辑连贯性\n\n重要：不要改写成AI风格的文章。保持真实、朴素的语气。如果某段已经很好，请直接说这段很好，无需修改。"}
                ],
                "tasks": ["往骨架里填满自己的真实内容", "用 AI 润色提示词优化表达", "完成第一篇完整作品并发布"]
            }
        ]
    },
    {
        "id": 3,
        "title": "思维升级",
        "subtitle": "从记录到洞察",
        "icon": "🧠",
        "color": "#6B8F71",
        "summary": "不再只是记录发生了什么，而是用思维工具分析为什么、怎么办。把思维模型从知道变成用过。",
        "tools": [
            {"name": "费曼技巧", "summary": "用最简单的语言讲清楚", "detail": "如果你不能用最简单的语言给一个外行讲清楚一件事，说明你自己也没理解透。卡壳的地方，就是你思维的盲区。费曼技巧的操作：选概念 → 假装讲给外行听 → 用最简单语言 → 找到卡壳点 → 回去补 → 再讲一遍。"},
            {"name": "多元思维模型", "summary": "一个问题，多个角度", "detail": "万维钢把芒格的多元思维模型理念做了实操化拆解。当你只有一个锤子，所有问题看起来都像钉子。但如果你有一个工具箱，你就能根据问题选择最合适的工具。本周每天用一个不同的思维框架分析一个真实问题。"},
            {"name": "二阶思维", "summary": "想一步，再想一步", "detail": "大多数人的思考停留在如果我做了 A，会直接得到什么结果。但高手会继续问：这个结果的后果是什么？后果的后果呢？一阶思维看直接结果，二阶思维看间接结果，三阶思维看连锁反应。"}
        ],
        "quote": "拥有一个思维模型的格栅，比拥有一个正确的答案重要得多。你只需要掌握最重要的几十个思维模型，就能应对生活中 90% 的问题。",
        "days": [
            {
                "id": "w3-d1", "period": "Day 15-16", "title": "费曼技巧实战", "subtitle": "讲清楚一个真正的问题",
                "content": "<h3>🎯 目标：用费曼技巧讲清楚一个你真正在意的问题</h3><p>你可能听说过第一性原理。你可能也知道机会成本这个词。你甚至能用它们侃侃而谈。</p><p>但问题来了：你上一次在做一个真实的人生决策时，主动用一个思维框架来分析，是什么时候？</p><p><strong>知道和做到之间，隔着一道巨大的鸿沟。</strong></p><p>费曼技巧的核心只有一句话：如果你不能用最简单的语言给一个外行讲清楚一件事，说明你自己也没理解透。</p><h4>具体做法：</h4><ul><li>从前两周的记录中，选一个反复出现但说不清楚的主题</li><li>假设对面坐着一个完全不懂这个话题的朋友</li><li>用大白话讲给他听——录音或者打字都可以</li><li><strong>找到卡壳的地方——那就是你思维的盲区</strong></li><li>记录：哪里卡壳了？为什么卡壳？需要补充什么信息？</li></ul>",
                "prompts": [
                    {"name": "🗣 费曼技巧引导提示词", "text": "你是一个完全不懂我专业的普通朋友。我想跟你讲清楚一个我一直在想的问题：\n\n问题：[输入你的问题]\n\n请扮演完全不懂的倾听者：\n1. 在我讲的过程中，对我用的术语提问：这个术语是什么意思？\n2. 如果我讲得太抽象，追问：能举个例子吗？\n3. 如果我有逻辑跳跃，指出来：这里我没跟上，这两件事是怎么连起来的？\n4. 最后告诉我：你觉得我哪些地方讲清楚了，哪些地方还没讲清楚。"},
                    {"name": "📓 费曼版记录模板", "text": "📓 费曼思考记录\n┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅\n\n🧩 我想搞清楚的问题：\n（一句话说清楚）\n\n🗣 用最简单的话解释：\n（假装讲给朋友听，写下来）\n\n⛔ 卡壳的地方：\n（讲到哪里说不清了？为什么？）\n\n💡 卡壳的原因分析：\n（缺信息？逻辑不通？概念没搞懂？）\n\n📚 下一步需要补充：\n（需要查什么、想什么、问什么？）\n\n🔄 再讲一遍（修订后）："}
                ],
                "tasks": ["选一个反复出现但说不清楚的主题", "用费曼技巧讲一遍，找到卡壳点", "记录思维盲区"]
            },
            {
                "id": "w3-d2", "period": "Day 17-20", "title": "思维模型工具箱", "subtitle": "每天一个框架，分析真实问题",
                "content": "<h3>🎯 目标：每天用一个思维框架分析一个真实问题</h3><p>万维钢把芒格的多元思维模型理念做了实操化拆解。核心观点是：当你只有一个锤子，所有问题看起来都像钉子。但如果你有一个工具箱，你就能根据问题选择最合适的工具。</p><p>关键要求：必须用在你自己的真实问题上，不是做练习。</p><h4>Day 17：第一性原理</h4><p>问自己：我这个问题的最底层是什么？剥掉所有的应该、别人觉得、社会期望，剩下的核心是什么？</p><h4>Day 18：机会成本</h4><p>每一次选择，你付出的不是你选的那个东西的价格，而是你放弃的那个东西的价值。选 A 你放弃 B，你真正放弃的是什么？那个放弃值得吗？</p><h4>Day 19：二阶效应</h4><p>一阶思维看直接结果。但高手问：这个结果的后果是什么？后果的后果呢？</p><h4>Day 20：奥卡姆剃刀 + 逆向思维</h4><p>如无必要，勿增实体——最简单的解释往往是正确的。</p><p>反过来想，总是反过来想。不要问我怎么做才能成功，问我做什么一定会失败——然后避免它。</p>",
                "prompts": [
                    {"name": "🔧 第一性原理提示词", "text": "我正在用第一性原理分析一个真实问题。\n\n问题：[描述你的问题]\n\n请帮我：\n1. 识别这个问题中哪些是社会默认假设（别人都这么说/做）\n2. 识别哪些是真实约束（物理/经济/时间的硬限制）\n3. 剥到最底层：剥离所有假设后，问题的核心是什么？\n4. 基于这个核心，有哪些我可能没想过的解决方向？"},
                    {"name": "⚖️ 机会成本提示词", "text": "我正在用机会成本框架分析一个选择。\n\n面临的选择：[描述你的选择 A vs B]\n\n请帮我分析：\n1. 选 A 我放弃的核心价值是什么？（不仅是钱/时间，还有体验、关系、可能性）\n2. 选 B 我放弃的核心价值是什么？\n3. 哪个放弃更让我三年后后悔？\n4. 有没有第三选项 C，能同时保留两边最重要的价值？"},
                    {"name": "🔮 二阶效应提示词", "text": "我正在用二阶思维分析一个决定。\n\n我打算做的决定：[描述决定]\n\n请帮我分析：\n1. 一阶结果：这个决定的直接、明显结果是什么？\n2. 二阶结果：一阶结果会导致什么？谁会受影响？什么会连锁发生？\n3. 三阶结果：二阶结果又会导致什么？\n4. 基于这个分析，这个决定还值得做吗？有没有调整方案？"},
                    {"name": "🪒 奥卡姆剃刀提示词", "text": "我正在用奥卡姆剃刀分析一个问题。\n\n问题：[描述问题]\n\n请帮我：\n1. 我对这个问题最复杂的解释是什么？\n2. 最简单的解释是什么？\n3. 简单的解释有没有遗漏关键因素？\n4. 如果我用最简单的解释来行动，会发生什么？\n\n万维钢说：当你有两个理论都能解释现象，选更简单的那个。"},
                    {"name": "🔄 逆向思维提示词", "text": "我正在用逆向思维分析一个目标。\n\n我的目标：[描述目标]\n\n请帮我：\n1. 反过来想：我做什么一定会搞砸这个目标？\n2. 列出 5 件确保失败的事\n3. 我现在在做的，有没有接近以上任何一件？\n4. 如果我要最少努力地达成这个目标，最低有效动作是什么？"}
                ],
                "tasks": ["Day 17: 用第一性原理分析一个问题", "Day 18: 用机会成本分析一个选择", "Day 19: 用二阶效应分析一个决定", "Day 20: 用奥卡姆剃刀 + 逆向思维分析", "完成至少 3 个框架的真实应用"]
            },
            {
                "id": "w3-d3", "period": "Day 21", "title": "整合与输出", "subtitle": "第二篇作品",
                "content": "<h3>🎯 目标：围绕本周的分析成果，完成第二篇作品</h3><p>第三周你做了大量思考：用费曼技巧找到了盲区，用不同的思维框架分析了真实问题。</p><p>现在，把这些分析成果变成一篇作品。</p><p>这次不再是凭感觉写，而是用思维框架驱动。你的文章会有一个清晰的分析结构，读者能跟着你的思路走。</p><h4>具体做法：</h4><ul><li>选一个本周最有感触的分析成果</li><li>用第二周学到的借骨还魂术搭骨架</li><li>填入本周的真实分析过程</li><li>发布并分享</li></ul><p><strong>从这一周开始，你不是在记录，你是在思考。</strong></p>",
                "prompts": [
                    {"name": "📝 分析成果扩展提示词", "text": "以下是我用思维框架分析一个问题的过程：\n\n问题：[描述问题]\n使用的框架：[框架名称]\n分析过程：[粘贴你的分析]\n\n请帮我：\n1. 这个分析中最有价值的洞察是什么？\n2. 如果把它扩展成一篇文章，推荐什么结构？\n3. 建议标题方向（3 个选项）\n4. 哪些地方可以加个人故事或案例来增强说服力？"}
                ],
                "tasks": ["选一个本周最有感触的分析成果", "用借骨还魂术搭骨架", "完成第二篇作品并发布"]
            }
        ]
    },
    {
        "id": 4,
        "title": "系统构建",
        "subtitle": "个人知识操作系统",
        "icon": "⚙️",
        "color": "#9B6B9E",
        "summary": "把记录、创作、思考整合成一个自动运转的系统。靠系统设计，不靠意志力。",
        "tools": [
            {"name": "系统思维", "summary": "看到整体，而不仅是局部", "detail": "当你把一件事看成孤立的事件，你只能做反应。当你把一件事放进系统里看，你就能做设计。高手不解决单个问题，他们优化系统。记录习惯、思维工具、作品输出——它们不是三件独立的事，它们是一个互相推动的飞轮。"},
            {"name": "习惯回路", "summary": "让系统自动运转", "detail": "任何习惯都由三部分组成：触发（ cue）、行动（ routine）、奖励（ reward）。想建立一个习惯，不要靠意志力，要靠设计。好触发：固定时间、固定动作之后。坏触发：有空的时候——永远不会来。"},
            {"name": "飞轮效应", "summary": "小行动驱动大改变", "detail": "当一个系统的各个部分互相推动，形成正向循环时，系统就会越转越快。飞轮启动时很慢——但一旦越过临界点，加速会非常惊人。大多数人的长期积累在开始时看不到变化，但累积到一定程度后差距是指数级的。"}
        ],
        "quote": "高手不解决单个问题，他们优化系统。真正能长期坚持的习惯，靠的不是自律，而是设计。",
        "days": [
            {
                "id": "w4-d1", "period": "Day 22-24", "title": "设计系统", "subtitle": "画出你的认知飞轮",
                "content": "<h3>🎯 目标：设计你的个人知识操作系统</h3><p>前三周，你学会了记录、创作、思考。第四周，我们要把这三件事整合成一个系统——一个能自动运转的个人知识操作系统。</p><p>普通人和高手的差距，不在于智商，不在于努力程度，而在于——<strong>高手思考的是系统，普通人思考的是事件</strong>。</p><p>事件思维：今天又没记录，我得补上。系统思维：什么条件会让我更容易记录？→ 睡前把记录本放在枕边 → 自动触发。</p><h4>Day 22：画出你的认知飞轮</h4><ul><li><strong>输入端：</strong>想法和素材从哪里来？（日常经历、阅读、社交、工作、播客…）</li><li><strong>处理端：</strong>你怎么消化这些素材？（哪个记录模板？什么时间记？AI 辅助哪些环节？）</li><li><strong>输出端：</strong>你产出了什么？（文章？复盘？社群分享？）</li><li><strong>反馈端：</strong>你怎么知道自己进步了？（社群反馈？自我回顾？数据追踪？）</li></ul><h4>Day 23：设计你的记录系统</h4><p>写一份个人记录系统说明书，包括：什么时间记、用什么工具、用什么模板、怎么用 AI、存在哪里。</p><h4>Day 24：设计你的思维工具箱</h4><p>列出你最常用的 3-5 个思维框架，每个写清：框架名称、核心问题、适用场景、使用示例。</p>",
                "prompts": [
                    {"name": "🔄 认知飞轮设计提示词", "text": "我正在设计我的个人认知飞轮。以下是我过去三周的情况：\n\n记录习惯：[描述你的记录习惯]\n常用工具：[你常用的记录工具和模板]\n创作产出：[你完成的作品]\n思维框架：[你用过的思维框架]\n反馈方式：[你如何获得反馈]\n\n请帮我：\n1. 设计一个完整的认知飞轮结构（输入→处理→输出→反馈→回到输入）\n2. 指出哪个环节最薄弱？怎么加强？\n3. 推荐 3 个能让我飞轮加速的杠杆点\n4. 帮我写一段飞轮说明书——用简洁的语言描述我的系统"},
                    {"name": "📋 记录系统说明书模板", "text": "📋 我的个人记录系统\n┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅\n\n⏰ 记录时间：\n（什么时间记？）\n\n📱 记录工具：\n（用什么工具记？）\n\n📄 记录模板：\n（用什么模板？按场景分）\n\n🤖 AI 使用规则：\n（AI 帮我做什么？不做什么？）\n\n📦 归档方式：\n（记录存在哪里？怎么整理？）\n\n📊 回顾节奏：\n（多久回顾一次？什么时候？）"},
                    {"name": "🧰 思维工具箱设计提示词", "text": "以下是我用过并且觉得有用的思维框架：[列出你用过并喜欢的框架]\n\n请帮我设计我的个人思维工具箱：\n1. 推荐 3-5 个最适合我的框架组合\n2. 每个框架配一个触发问题——遇到什么情况时调用它\n3. 每个框架配一个一句话记忆口诀\n4. 建议我优先熟练掌握哪 2 个框架？"}
                ],
                "tasks": ["画出个人认知飞轮（输入→处理→输出→反馈）", "写一份个人记录系统说明书", "设计个人思维工具箱（3-5 个框架）"]
            },
            {
                "id": "w4-d2", "period": "Day 25-28", "title": "运行与固化", "subtitle": "让系统自动运转",
                "content": "<h3>🎯 目标：运行系统、调整优化、月度总结</h3><p>系统设计好了，现在让它转起来。</p><p><strong>习惯回路</strong>——任何习惯都由三部分组成：触发（ cue）、行动（ routine）、奖励（ reward）。</p><p>想建立一个习惯，不要靠意志力，要靠设计。</p><h4>Day 25：为每个习惯设计触发器</h4><ul><li>记录习惯的触发器：每晚刷完牙 → 坐到书桌前 → 打开记录</li><li>思考习惯的触发器：每周六上午 → 选一个问题 → 用费曼技巧讲一遍</li><li>创作习惯的触发器：每月最后一周 → 回顾本月记录 → 选素材 → 借骨还魂</li></ul><h4>Day 26：运行系统一天</h4><p>按你设计的系统完整运行一天，记录感受：哪里顺畅？哪里卡壳？哪里想调整？</p><h4>Day 27：调整优化</h4><p>根据运行体验微调系统，写出最终版<strong>个人知识操作系统说明书</strong></p><h4>Day 28：月度总结</h4><p>回顾四周的所有记录，回答：</p><ul><li>这四周，我的认知回路有什么变化？</li><li>我找到了哪些适合自己的记录方式和思维工具？</li><li>我的认知飞轮是什么样子？</li><li>下个月，我要怎么继续运转这个系统？</li></ul>",
                "prompts": [
                    {"name": "🎯 习惯触发器设计提示词", "text": "我想为以下习惯设计触发器：\n\n我想要养成的习惯：[描述习惯]\n\n请帮我设计：\n1. 3 种可能的触发信号（时间、地点、前序动作）\n2. 找出最好的一个组合\n3. 设计一个奖励——完成这个习惯后给自己什么正反馈\n4. 如果某天没完成，设计一个最低可行版本（1 分钟搞定）"},
                    {"name": "📊 月度复盘提示词", "text": "你是一位思维教练。以下是我这四周的记录和作品：\n\n[粘贴所有记录和作品链接/摘要]\n\n请帮我做月度复盘：\n1. 这四周我的认知成长曲线是怎样的？\n2. 最重要的 3 个发现/洞察是什么？\n3. 我的记录习惯、创作习惯、思考习惯分别养成了多少？\n4. 我最适合哪些思维工具？\n5. 下个月我应该在哪个方向上继续深入？\n6. 给我写一段月度总结的开头，语气要真实、有温度"},
                    {"name": "📄 个人知识操作系统说明书模板", "text": "📄 我的个人知识操作系统说明书\n┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅\n编制日期：[日期]\n\n一、系统概览\n认知飞轮：[一句话描述]\n\n二、记录子系统\n- 时间：\n- 工具：\n- 模板：\n- AI 规则：\n- 归档：\n- 回顾节奏：\n\n三、思维工具箱\n1. [框架1] → 用于 [场景]\n2. [框架2] → 用于 [场景]\n3. [框架3] → 用于 [场景]\n\n四、创作流程\n- 频率：\n- 流程：选材 → 搭骨架 → 填内容 → 润色 → 发布\n- 发布渠道：\n\n五、习惯触发器\n- 记录触发：\n- 思考触发：\n- 创作触发：\n\n六、反馈与迭代\n- 如何获取反馈：\n- 多久做一次系统回顾："}
                ],
                "tasks": ["为每个习惯设计触发器", "完整运行系统至少 1 天", "完成最终版个人知识操作系统说明书", "写完月度复盘"]
            }
        ]
    }
]

THINKING_TOOLS_DICT = [
    {"name": "第一性原理", "source": "物理学/亚里士多德 → 马斯克推广", "summary": "回到最底层，问这件事的本质是什么。剥掉所有社会默认假设，找到不可再拆解的核心真理。", "question": "这件事最底层的、不可再拆解的核心是什么？"},
    {"name": "元认知", "source": "认知心理学", "summary": "对思考的思考。不仅能思考问题，还能跳出来审视自己的思考过程。", "question": "我此刻在想什么？我是怎么思考这个问题的？"},
    {"name": "反脆弱", "source": "纳西姆·塔勒布", "summary": "有些东西能从波动和不确定性中获益。小步高频的积累就是反脆弱的——每一次看似微不足道，但长期复利不可预测。", "question": "我怎么做才能从不确定性中获益？"},
    {"name": "费曼技巧", "source": "理查德·费曼", "summary": "用最简单的语言给一个外行讲清楚一件事。卡壳的地方就是你思维的盲区。", "question": "我能用一句话给一个 5 岁小孩讲清楚吗？"},
    {"name": "二阶思维", "source": "决策理论", "summary": "不只问如果我做了 A 会怎样，还问那然后呢？那再然后呢？考虑后果的后果。", "question": "这个结果的后果是什么？后果的后果呢？"},
    {"name": "机会成本", "source": "经济学", "summary": "选 A 的真正成本不是 A 的价格，而是放弃 B 所失去的价值。", "question": "选了这个，我放弃了什么？三年后我会后悔放弃那个吗？"},
    {"name": "奥卡姆剃刀", "source": "威廉·奥卡姆", "summary": "如无必要，勿增实体。最简单的解释往往是正确的。", "question": "最简单的解释是什么？"},
    {"name": "逆向思维", "source": "查理·芒格", "summary": "反过来想，总是反过来想。不要问怎么成功，问什么一定会导致失败，然后避免它。", "question": "我做什么一定会搞砸？"},
    {"name": "多元思维模型", "source": "查理·芒格 → 万维钢", "summary": "拥有一个思维模型的格栅，比拥有一个正确的答案重要得多。面对任何问题，能从多个不同学科的角度来分析。", "question": "这个问题还能从什么其他角度来理解？"},
    {"name": "系统思维", "source": "系统论", "summary": "看到整体和局部之间的关系，而不仅是孤立的事件。高手不解决单个问题，他们优化系统。", "question": "这是个孤立事件，还是系统里的一部分？我该怎么设计系统？"},
    {"name": "习惯回路", "source": "查尔斯·杜希格《习惯的力量》", "summary": "习惯 = 触发 → 行动 → 奖励。不要靠意志力，要靠设计。", "question": "什么信号触发我行动？做完后给我什么奖励？"},
    {"name": "飞轮效应", "source": "吉姆·柯林斯 → 贝佐斯", "summary": "系统的各个部分互相推动形成正向循环。开始时很慢，但越过临界点后加速惊人。", "question": "我的飞轮有哪些环节？哪个最弱？怎么加强？"},
    {"name": "弱联系", "source": "社会网络理论", "summary": "真正有价值的创新和信息，往往来自你不熟悉的人或事物——把不相关的想法连接起来。", "question": "这两个看似不相关的东西之间有什么联系？"},
    {"name": "最小可行产品 (MVP)", "source": "精益创业", "summary": "不求完美，先求完整。先做一个刚好能用的版本，发布出去，根据反馈迭代。", "question": "什么是最少努力就能完成的完整版本？"},
    {"name": "认知解耦", "source": "认知科学", "summary": "把心中的叙事和眼前的事实拆开，让情绪升起又消散，而自己不必跟着走。", "question": "我心中讲的故事和事实本身有多大差距？"},
    {"name": "探索与利用", "source": "计算机科学/决策理论", "summary": "探索发现机会，利用创造价值。先探索再利用，利用出成绩之后再探索，再利用。循环不止。", "question": "现在是应该探索新方向，还是深耕现有优势？"},
    {"name": "供给侧心态", "source": "经济学/博弈论", "summary": "把自己当成提供可验证价值的模块。主动降低协作摩擦，嵌入长期重复博弈与网络效应结构。", "question": "我能提供什么可验证的价值？怎么让别人跟我合作更顺？"},
    {"name": "场域理论", "source": "皮埃尔·布迪厄", "summary": "社会由多个相对独立的场域组成，每个场域有自己的规则和资本。努力不是硬通货，合规才是。", "question": "这个场域的规则是什么？我有没有在按不对的规则玩？"},
    {"name": "无免费午餐定理", "source": "计算机科学 (Wolpert & Macready)", "summary": "不存在普适最优的决策。任何在特定领域表现优异的方法，必然在其他领域表现不足。诸行无常，决策必有偏置。", "question": "这个方案在什么条件下会失效？"},
    {"name": "非遍历性", "source": "统计学/金融", "summary": "在乘法世界中，一次彻底的失败可能让你清零。个体必须控制方差和避免清零。对个体不利但对庄家有利。", "question": "最坏情况是什么？我能承受吗？"},
    {"name": "凯利公式", "source": "信息论/金融 (约翰·凯利)", "summary": "在不确定环境下，每次下注的最优比例 = 胜率 - 败率/赔率。在凯利公式看来，人生的根本自由是你始终有下一次下注的能力。", "question": "我该投入多少？我还有第二次机会吗？"}
]

# ===================================================================
# Session state
# ===================================================================

def init_session():
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "current_week" not in st.session_state:
        st.session_state.current_week = None
    if "current_day" not in st.session_state:
        st.session_state.current_day = None
    if "records" not in st.session_state:
        st.session_state.records = []
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    if "ai_config" not in st.session_state:
        st.session_state.ai_config = {
            "api_endpoint": "",
            "api_key": "",
            "model": ""
        }

init_session()

# ===================================================================
# Navigation functions
# ===================================================================

def navigate_to(page, week=None, day=None):
    st.session_state.page = page
    st.session_state.current_week = week
    st.session_state.current_day = day

def go_home():
    st.session_state.page = "home"
    st.session_state.current_week = None
    st.session_state.current_day = None

# ===================================================================
# UI Components
# ===================================================================

def render_header():
    st.markdown('<h1 class="main-header">🧠 人生无限游戏 · 万维钢版月度陪伴计划</h1>', unsafe_allow_html=True)

def render_week_card(week):
    color = week["color"]
    st.markdown(f"""
    <div class="week-card" style="border-left: 4px solid {color};">
        <h3>{week["icon"]} {week["title"]}</h3>
        <p><strong>{week["subtitle"]}</strong></p>
        <p>{week["summary"]}</p>
    </div>
    """, unsafe_allow_html=True)

def render_prompt_card(prompt):
    with st.container():
        st.markdown(f"**{prompt['name']}**")
        st.code(prompt["text"], language=None)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.button("📋 复制", key=f"copy_{prompt['name']}", use_container_width=True)
        with col2:
            if st.button("🤖 发送到 AI", key=f"send_{prompt['name']}", use_container_width=True):
                if st.session_state.ai_config["api_endpoint"] and st.session_state.ai_config["api_key"]:
                    st.session_state.ai_prompt = prompt["text"]
                    st.session_state.page = "ai_chat"
                else:
                    st.warning("请先在设置页面配置 AI 信息")

def render_day_content(week, day):
    st.markdown(f"## {day['period']} · {day['title']}")
    st.markdown(f"*{day['subtitle']}*")
    st.markdown(day["content"], unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📝 本日任务")
    for task in day["tasks"]:
        st.markdown(f"- [ ] {task}")

    st.markdown("---")
    st.markdown("### 💡 AI 提示词模板")
    for i, prompt in enumerate(day["prompts"]):
        render_prompt_card(prompt)

def render_tool_card(tool):
    with st.expander(f"**{tool['name']}** — {tool['summary']}"):
        st.markdown(f"**来源：** {tool['source']}")
        st.markdown(f"**定义：** {tool['summary']}")
        st.markdown(f"**触发问题：** {tool['question']}")

# ===================================================================
# Pages
# ===================================================================

def page_home():
    render_header()

    st.markdown("### 📅 四周路径")

    cols = st.columns(2)
    for i, week in enumerate(WEEKLY_DATA):
        with cols[i % 2]:
            with st.container():
                render_week_card(week)
                if st.button(f"进入 {week['title']}", key=f"week_{week['id']}", use_container_width=True):
                    navigate_to("week", week=week["id"])

    st.markdown("---")
    st.markdown("### 🧰 快速访问")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 思维工具词典", use_container_width=True):
            navigate_to("tools")
    with col2:
        if st.button("📝 我的记录", use_container_width=True):
            navigate_to("journal")

def page_week():
    week = next((w for w in WEEKLY_DATA if w["id"] == st.session_state.current_week), None)
    if not week:
        go_home()
        return

    if st.button("← 返回首页"):
        go_home()

    st.markdown(f"## {week['icon']} 第{week['id']}周：{week['title']}")
    st.markdown(f"*{week['subtitle']}*")
    st.markdown(week["quote"])

    st.markdown("---")
    st.markdown("### 🛠 核心思维工具")
    for tool in week["tools"]:
        render_tool_card(tool)

    st.markdown("---")
    st.markdown("### 📅 日程安排")

    for day in week["days"]:
        with st.expander(f"**{day['period']}：{day['title']}** — {day['subtitle']}"):
            if st.button(f"查看详情", key=f"day_{day['id']}"):
                navigate_to("day", week=week["id"], day=day["id"])

def page_day():
    week = next((w for w in WEEKLY_DATA if w["id"] == st.session_state.current_week), None)
    if not week:
        go_home()
        return

    day = next((d for d in week["days"] if d["id"] == st.session_state.current_day), None)
    if not day:
        navigate_to("week", week=week["id"])
        return

    if st.button("← 返回周概览"):
        navigate_to("week", week=week["id"])

    col1, col2 = st.columns([3, 1])
    with col1:
        render_day_content(week, day)
    with col2:
        st.markdown("### 记录")
        if st.button("✏️ 写记录", use_container_width=True):
            navigate_to("journal")

    st.markdown("---")

    st.markdown("### 📤 导出")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("导出为 JSON", use_container_width=True):
            data = {"week": week["id"], "day": day["id"], "date": datetime.now().isoformat()}
            st.download_button("下载 JSON", json.dumps(data, ensure_ascii=False), "record.json", "application/json")
    with col2:
        if st.button("导出为 Markdown", use_container_width=True):
            md = f"# {day['title']}\n\n{day['content']}\n\n## 提示词\n"
            for p in day["prompts"]:
                md += f"\n### {p['name']}\n\n```\n{p['text']}\n```\n"
            st.download_button("下载 Markdown", md, "record.md", "text/markdown")

def page_tools():
    st.markdown("## 📖 思维工具词典")

    search = st.text_input("🔍 搜索工具", "")

    filtered_tools = THINKING_TOOLS_DICT
    if search:
        filtered_tools = [t for t in THINKING_TOOLS_DICT if search.lower() in t["name"].lower() or search.lower() in t["summary"].lower()]

    st.markdown(f"共 {len(filtered_tools)} 个工具")

    for tool in filtered_tools:
        render_tool_card(tool)

    st.markdown("---")
    if st.button("← 返回首页"):
        go_home()

def page_journal():
    st.markdown("## 📝 每日记录")

    tabs = st.tabs(["✏️ 写记录", "📜 记录历史"])

    with tabs[0]:
        st.markdown("### 写新记录")

        week_options = [f"第{w['id']}周：{w['title']}" for w in WEEKLY_DATA]
        week_selected = st.selectbox("选择周", week_options, key="journal_week_select")

        record_type = st.selectbox("记录类型", ["日常复盘", "碎片灵感", "问题追踪", "情绪日记", "费曼思考", "其他"])

        record_content = st.text_area("记录内容", height=200, placeholder="写下你的想法...")

        col1, col2 = st.columns([1, 4])
        with col1:
            save = st.button("💾 保存", use_container_width=True)
        if save:
            if record_content:
                record = {
                    "id": hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8],
                    "date": datetime.now().isoformat(),
                    "week": week_selected,
                    "type": record_type,
                    "content": record_content
                }
                st.session_state.records.append(record)
                st.success("记录已保存！")
            else:
                st.warning("请输入内容")

    with tabs[1]:
        if st.session_state.records:
            for record in reversed(st.session_state.records):
                with st.container():
                    st.markdown(f"**{record['week']}** · {record['type']}")
                    st.caption(f"{record['date'][:10]}")
                    st.markdown(record["content"])
                    st.markdown("---")
        else:
            st.info("暂无记录，开始写第一条吧！")

    if st.button("← 返回首页"):
        go_home()

def page_settings():
    st.markdown("## ⚙️ 设置")

    st.markdown("### 🤖 AI 配置")
    st.markdown("配置你的 AI 接口信息以使用发送到 AI 功能")

    api_endpoint = st.text_input("API 端点", value=st.session_state.ai_config.get("api_endpoint", ""), placeholder="https://api.openai.com/v1/chat/completions")
    api_key = st.text_input("API Key", value=st.session_state.ai_config.get("api_key", ""), type="password", placeholder="sk-...")
    model = st.text_input("模型名称", value=st.session_state.ai_config.get("model", ""), placeholder="gpt-4o")

    if st.button("💾 保存配置"):
        st.session_state.ai_config = {
            "api_endpoint": api_endpoint,
            "api_key": api_key,
            "model": model
        }
        st.success("配置已保存！")

    st.markdown("---")
    st.markdown("### 🗑 数据管理")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 导出所有记录", use_container_width=True):
            st.download_button("下载 JSON", json.dumps(st.session_state.records, ensure_ascii=False, indent=2), "records.json", "application/json")

    with col2:
        uploaded = st.file_uploader("📥 导入记录", type="json")
        if uploaded:
            try:
                data = json.load(uploaded)
                st.session_state.records.extend(data)
                st.success(f"成功导入 {len(data)} 条记录！")
            except:
                st.error("导入失败，请检查文件格式")

    if st.button("← 返回首页"):
        go_home()

# ===================================================================
# Main
# ===================================================================

def main():
    page = st.session_state.page

    if page == "home":
        page_home()
    elif page == "week":
        page_week()
    elif page == "day":
        page_day()
    elif page == "tools":
        page_tools()
    elif page == "journal":
        page_journal()
    elif page == "settings":
        page_settings()
    else:
        page_home()

if __name__ == "__main__":
    main()