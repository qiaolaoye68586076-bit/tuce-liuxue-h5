import re

with open('frontend/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Hide the numbers
css += "\n/* User request: Delete numbers 0102 from service cards */\n.svcgal-card__no { display: none !important; }\n"

# 2. Show the description text (pts/mods) on desktop
old_mods = """/* —— 移动端信息增量：服务卡内直接亮出「这项服务包含什么」——
   手机用户大多不点二级页，卡面即概览；桌面竖柜保持极简，隐藏 —— */
.svcgal-card__pts, .svcgal-card__mods{ display:none; }
@media (max-width:900px){
  .svcgal-card__pts{
    display:flex; flex-wrap:wrap; gap:7px;
    list-style:none; margin:0 0 22px; padding:0;
  }
  .svcgal-card__pts li{
    font-size:11.5px; font-weight:500; letter-spacing:.05em; line-height:1;
    color:var(--gold-soft); padding:7px 12px; border-radius:999px;
    border:1px solid rgba(217,194,140,.4); background:rgba(20,52,43,.4);
    -webkit-backdrop-filter:blur(2px); backdrop-filter:blur(2px);
  }
  .svcgal-card__mods{
    display:block; margin:9px 0 0; max-width:24ch;
    font-size:11.5px; line-height:1.7; letter-spacing:.03em;
    color:#7A6535;
  }
}"""

new_mods = """/* —— 信息增量：服务卡内直接亮出「这项服务包含什么」—— */
.svcgal-card__pts{
  display:flex; flex-wrap:wrap; gap:7px;
  list-style:none; margin:16px 0 22px; padding:0;
  position: relative; z-index: 10;
}
.svcgal-card__pts li{
  font-size:11.5px; font-weight:500; letter-spacing:.05em; line-height:1;
  color:var(--gold-soft); padding:7px 12px; border-radius:999px;
  border:1px solid rgba(217,194,140,.4); background:rgba(20,52,43,.4);
  -webkit-backdrop-filter:blur(2px); backdrop-filter:blur(2px);
}
.svcgal-card__mods{
  display:block; margin:16px 0 0; max-width:26ch;
  font-size:12.5px; line-height:1.6; letter-spacing:.02em;
  color:var(--green); opacity: 0.8;
  position: relative; z-index: 10;
}
"""
css = css.replace(old_mods, new_mods)

with open('frontend/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("CSS updated.")
