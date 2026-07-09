import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Grad
grad_old = """<p class="svcgal-card__desc">从专业定位、精细化文书打磨到全真面试辅导，扫除申请盲区，为名校录取和长远职业发展铺路，一路陪到落地。</p>"""
grad_new = """<p class="svcgal-card__desc">从专业精准定位、精细化文书打磨到全真模拟面试辅导，我们层层扫除申请盲区。不仅为您匹配顶尖学术资源，更为您的名校录取和长远职业发展铺设坚实基石，团队将一路陪伴直至您顺利落地入读。</p>"""
html = html.replace(grad_old, grad_new)

# Multi
multi_old = """<p class="svcgal-card__desc">美英加港新等多赛道同时发力。同一份顶尖准备，科学重组多国投递矩阵，冲刺稳妥保底三档组合，实现录取概率最大化。</p>"""
multi_new = """<p class="svcgal-card__desc">美英加港新等多赛道同时发力。利用同一份顶尖准备材料，结合各地区不同录取偏好，为您科学重组多国投递矩阵。通过设定冲刺、稳妥、保底三档极具策略性的组合，实现名校录取概率的最大化。</p>"""
html = html.replace(multi_old, multi_new)

# Transfer
trans_old = """<p class="svcgal-card__desc">精准的学分转换与转学策略制定，12个月接力规划重新盘活现有学术资源，把当前的 GPA 变成冲击梦校的坚实跳板。</p>"""
trans_new = """<p class="svcgal-card__desc">通过精准的学分转换评估与高阶转学策略制定，我们为您提供严密的12个月接力规划。重新盘活并最大化您现有的学术资源，将当前的 GPA 与履历变成冲击更顶尖梦校的坚实跳板，完成华丽逆袭。</p>"""
html = html.replace(trans_old, trans_new)

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Text expanded.")
