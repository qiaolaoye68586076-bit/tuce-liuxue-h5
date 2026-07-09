import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 按钮改为原先设计
# Restore Team Button
html = html.replace('<a class="btn btn--cta btn--lg" href="teachers">认识我们的导师',
                    '<a class="btn btn--line" href="teachers">认识我们的导师')
# Remove the custom Services Button I added
html = re.sub(r'<div style="text-align:center; margin-top:40px;" class="reveal">\s*<a class="btn btn--cta btn--lg" href="services">查看全部服务[^<]*<svg[^>]*>.*?<\/svg><\/a>\s*<\/div>', '', html, flags=re.DOTALL)


with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('frontend/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 2. 四个服卡片 美本文字和标题居中 增加另外三个小卡片的文字说明内容
# US Undergrad Card - text center
css = css.replace('.svcgal-card--us .svcgal-card__desc{', 
                  '.svcgal-card--us .svcgal-card__desc{\n  text-align: center; margin-left: auto; margin-right: auto;')
css = css.replace('.svcgal-card--us h3{',
                  '.svcgal-card--us h3{\n  text-align: center;')

# 4. 免费评估卡片太长了 压缩短一点
# Reduce form padding and margins
css = css.replace('.consult{ padding-top:96px; padding-bottom:110px; }',
                  '.consult{ padding-top:64px; padding-bottom:72px; }')
css = css.replace('@media (max-width:600px){ .consult{ padding-top:44px; padding-bottom:64px; } }',
                  '@media (max-width:600px){ .consult{ padding-top:32px; padding-bottom:40px; } }')
css = css.replace('.consult__copy{ padding:54px 44px; }',
                  '.consult__copy{ padding:36px 32px; }')
css = css.replace('.form{ display:grid; grid-template-columns:1fr 1fr; gap:18px 14px; }',
                  '.form{ display:grid; grid-template-columns:1fr 1fr; gap:14px 12px; }')

# 3. 所有页面上方hero背景图上沿和导航栏中间有一个米白色间隙 修复
# Add a negative top to hero-bg or set top margin to 0 explicitly
# It is highly likely the nav was pushed by something or body has a gap.
if '/* Hero Gap Fix */' not in css:
    css += '\n/* Hero Gap Fix */\nhtml, body { margin: 0 !important; padding: 0 !important; }\n.hero, .page-hero { margin-top: 0 !important; }\n.hero-bg, .hero-overlay { top: 0 !important; margin-top: 0 !important; }\n'

with open('frontend/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("HTML and CSS fixes applied.")
