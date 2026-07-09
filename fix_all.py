import re

# 1. Update index.html for Services text and button
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace lead text
old_lead = '<p class="lead">以美国本科申请为核心引擎，同时提供研究生、本科转学及多国联申服务，满足不同阶段的高端留学需求。</p>'
new_lead = '<p class="lead" style="max-width: 24em; margin: 0 auto;">以美国本科申请为核心引擎，辐射全球顶尖名校，量身定制高端升学路径。</p>'
html = html.replace(old_lead, new_lead)

# Insert the "All Services" button at the end of svc-rows
svc_rows_end = '      </a>\n    </div>\n  </section>'
button_html = """      </a>
    </div>
    
    <div style="margin-top: 56px; text-align: center; display: flex; justify-content: center;" class="reveal">
      <a href="services" class="btn btn--cta" style="padding: 16px 42px; font-size: 16px;">查看全部服务</a>
    </div>
  </section>"""
html = html.replace(svc_rows_end, button_html)

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html)


# 2. Update style.css for FAQ and Hero
with open('frontend/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# FAQ remove 01, 02
css = re.sub(r'\.faq__q::before\s*\{[^}]*\}', '.faq__q::before { display: none; }', css)
css = re.sub(r'\.faq__q:hover::before,\s*\.faq__q\[aria-expanded="true"\]::before\s*\{[^}]*\}', '', css)

# Hero fix mobile background visibility
old_mobile_hero = """  .hero--light .hero-bg { 
    background-position: 50% 0%; 
    background-size: cover;
  }
  .hero--light .hero-overlay {
    background: linear-gradient(180deg,
      rgba(250, 247, 240, 0) 0%,
      rgba(250, 247, 240, 0.4) 30%,
      rgba(250, 247, 240, 0.95) 55%,
      rgba(250, 247, 240, 1) 100%);
  }"""

new_mobile_hero = """  .hero--light .hero-bg { 
    background-position: 72% center; /* 恢复原本的右侧位移，让建筑主体在屏幕中央 */
    background-size: cover;
  }
  .hero--light .hero-overlay {
    background: linear-gradient(180deg,
      rgba(250, 247, 240, 0) 0%,
      rgba(250, 247, 240, 0) 25%,
      rgba(250, 247, 240, 0.4) 45%,
      rgba(250, 247, 240, 0.95) 68%,
      rgba(250, 247, 240, 1) 100%);
  }"""

if old_mobile_hero in css:
    css = css.replace(old_mobile_hero, new_mobile_hero)
else:
    print("Could not find the old mobile hero css.")

with open('frontend/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updates applied.")
