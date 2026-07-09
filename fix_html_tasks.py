import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 师资文案
html = html.replace('<b>Kevin <i>· 创始人</i></b>\n            <em>宾大英语教学硕士 · 前波士顿报社记者</em>\n            <span>把「挖故事、讲清楚」的本事用到每个孩子身上</span>',
                    '<b>Kevin <i>· 创始人</i></b>\n            <em>宾大英语教学硕士 · 前波士顿报社记者</em>\n            <span>把挖故事讲清楚的本事用到每个孩子身上</span>')
html = html.replace('<b>Jennifer <i>· 导师</i></b>\n            <em>UCLA 心理学学士 · 哥大社会组织心理学硕士</em>\n            <span>200+ 学生性格测评，录取覆盖哈佛·剑桥·港大</span>',
                    '<b>Jennifer <i>· 导师</i></b>\n            <em>UCLA 心理学学士 · 哥大社会组织心理学硕士</em>\n            <span>200+ 学生测评，录取覆盖哈佛剑桥港大</span>')
html = html.replace('<b>荣子依 <i>· 导师</i></b>\n            <em>布雷拉美术学院 · 中科院认证心理咨询师</em>\n            <span>家庭教育与疗愈，帮孩子把学习动力从心里点起来</span>',
                    '<b>荣子依 <i>· 导师</i></b>\n            <em>布雷拉美术学院 · 中科院认证心理咨询师</em>\n            <span>家庭疗愈，帮孩子把学习动力从心里点起来</span>')
html = html.replace('<b>Tim 楚浩哲 <i>· 导师</i></b>\n            <em>斯坦福校友 · 前 Google GTM Director</em>\n            <span>提炼有辨识度的个人叙事，已助 30+ 名校录取</span>',
                    '<b>Tim 楚浩哲 <i>· 导师</i></b>\n            <em>斯坦福校友 · 前 Google GTM Director</em>\n            <span>提炼辨识度个人叙事，助 30+ 名校录取</span>')

# 2. 按钮大一统
# Team
html = html.replace('<a class="btn btn--line" href="teachers">认识我们的导师 <svg class="ic"><use href="#ic-arrow"/></svg></a>',
                    '<a class="btn btn--cta btn--lg" href="teachers">认识我们的导师 <svg class="ic"><use href="#ic-arrow"/></svg></a>')

# 3. 案例板块数字220下面把offer单词删了 压缩为一行
html = html.replace('<span class="figure__desc">Offer · 2024–2026</span>',
                    '<span class="figure__desc">2024–2026</span>')

# 4. 修改案例板块的查看完整的按钮 (It's already a span, I'll change text and add an arrow)
html = html.replace('<span class="casecard__more">查看完整策略复盘 →</span>',
                    '<span class="casecard__more">阅读完整复盘 <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-left:4px"><path d="M4 12h15M14 6.5 19.5 12 14 17.5"/></svg></span>')

# 5. 服务卡片左边字在放满一点 不要分段 就是保持小标题➕一段话的设计 美本也是 把标签都删了
# US
us_old = """<h3>美国本科<span class="svcgal-card__tag">·核心业务</span></h3>
        <p class="svcgal-card__desc">成长规划、学术硬实力、申请表达与影响力三大模块，整合名校文书训练营。</p>
        <ul class="svcgal-card__pts" role="list"><!-- 移动端专属：不点进去也能看到服务包含什么 -->
          <li>成长规划</li>
          <li>学术硬实力</li>
          <li>申请表达与影响力</li>
          <li>名校文书训练营</li>
        </ul>"""
us_new = """<h3>美国本科</h3>
        <p class="svcgal-card__desc">成长规划、学术硬实力、申请表达与影响力三大模块，由全常春藤导师团队深度把控，整合名校文书训练营，发掘独一无二的智识好奇心，拒绝模板化申请。</p>"""
html = html.replace(us_old, us_new)

# Grad
grad_old = """<h3>研究生</h3>
        <p class="svcgal-card__desc">专业定位、文书面试到签证入学，一路陪到落地。</p>
        <p class="svcgal-card__mods">综合评估 · 精准定位 · 笔面试辅导 · 职业规划与签证</p>"""
grad_new = """<h3>研究生</h3>
        <p class="svcgal-card__desc">从专业定位、精细化文书打磨到全真面试辅导，扫除申请盲区，为名校录取和长远职业发展铺路，一路陪到落地。</p>"""
html = html.replace(grad_old, grad_new)

# Multi
multi_old = """<h3>多国联申</h3>
        <p class="svcgal-card__desc">美英加港新组合投递，把录取概率科学重组。</p>
        <p class="svcgal-card__mods">冲刺·稳妥·保底三档组合 · 一份准备多线投递</p>"""
multi_new = """<h3>多国联申</h3>
        <p class="svcgal-card__desc">美英加港新等多赛道同时发力。同一份顶尖准备，科学重组多国投递矩阵，冲刺稳妥保底三档组合，实现录取概率最大化。</p>"""
html = html.replace(multi_old, multi_new)

# Transfer
trans_old = """<h3>转学</h3>
        <p class="svcgal-card__desc">学分规划与转学申请，把 GPA 变成向上的跳板。</p>
        <p class="svcgal-card__mods">12 个月接力规划 · 学分转换 · 转学文书与截止日</p>"""
trans_new = """<h3>转学</h3>
        <p class="svcgal-card__desc">精准的学分转换与转学策略制定，12个月接力规划重新盘活现有学术资源，把当前的 GPA 变成冲击梦校的坚实跳板。</p>"""
html = html.replace(trans_old, trans_new)

# Add all services button at bottom of services grid
services_end_old = '      </a>\n    </div>\n  </section>'
services_end_new = '      </a>\n    </div>\n    <div style="text-align:center; margin-top:40px;" class="reveal">\n      <a class="btn btn--cta btn--lg" href="services">查看全部服务 <svg class="ic" viewBox="0 0 24 24"><path d="M4 12h15M14 6.5 19.5 12 14 17.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></a>\n    </div>\n  </section>'
html = html.replace(services_end_old, services_end_new)

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML text replacements applied.")
