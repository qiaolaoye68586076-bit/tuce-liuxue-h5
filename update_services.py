import re

css = """
/* =========================================================
   ✦ 首页 · 服务大图交替排版 (2026-07-09 改版)
   ========================================================= */
.svc-rows {
  display: flex;
  flex-direction: column;
  gap: 32px;
  max-width: var(--maxw);
  margin: 0 auto;
  padding: 0 20px;
}

.svc-row {
  display: flex;
  flex-direction: column;
  border-radius: 28px;
  overflow: hidden;
  text-decoration: none;
  background: #ECE3D0;
  transition: transform 0.4s var(--ease), box-shadow 0.4s var(--ease);
}

@media (min-width: 768px) {
  .svc-row {
    flex-direction: row;
    height: 420px;
  }
  .svc-row--reverse {
    flex-direction: row-reverse;
  }
}

.svc-row:hover {
  transform: translateY(-6px);
  box-shadow: 0 24px 48px -16px rgba(0,0,0,0.15);
}

.svc-row__content {
  flex: 1;
  padding: 56px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.svc-row__visual {
  flex: 1;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  min-height: 280px;
}

/* Individual Colors */
.svc-row--us {
  background: var(--green); /* 深绿色 */
  color: #fff;
}
.svc-row--grad {
  background: #ECE3D0; /* 米金色 */
  color: var(--green);
}
.svc-row--multi {
  background: #FCFAF4; /* 纯白偏暖 */
  color: var(--green);
  border: 1px solid rgba(0,0,0,0.05);
}
.svc-row--transfer {
  background: var(--gold-soft); /* 柔金色 */
  color: var(--green);
}

/* Typography */
.svc-row h3 {
  font-size: 34px;
  font-weight: 800;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 14px;
}
.svc-row--us h3 { color: #fff; }
.svc-row__tag {
  font-size: 13px;
  font-weight: 700;
  padding: 6px 14px;
  border-radius: 999px;
  background: rgba(217, 194, 140, 0.2);
  color: var(--gold);
  border: 1px solid rgba(217, 194, 140, 0.4);
}
.svc-row--grad .svc-row__tag,
.svc-row--multi .svc-row__tag,
.svc-row--transfer .svc-row__tag {
  background: rgba(20, 52, 43, 0.08);
  color: var(--green);
  border-color: rgba(20, 52, 43, 0.15);
}

.svc-row__desc {
  font-size: 16px;
  line-height: 1.7;
  opacity: 0.85;
  max-width: 26em;
  margin-bottom: 36px;
}

.svc-row__btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  font-size: 15px;
  margin-top: auto;
  align-self: flex-start;
  transition: gap 0.3s ease;
}
.svc-row:hover .svc-row__btn {
  gap: 12px;
}
.svc-row__btn svg {
  width: 18px;
  height: 18px;
}
.svc-row--us .svc-row__btn { color: var(--gold); }
.svc-row--grad .svc-row__btn,
.svc-row--multi .svc-row__btn,
.svc-row--transfer .svc-row__btn { color: var(--green); }

/* Arch styling */
.svc-row__arch {
  position: absolute;
  bottom: -20px;
  left: 50%;
  transform: translateX(-50%);
  width: 280px;
  height: 380px;
  border-top-left-radius: 999px;
  border-top-right-radius: 999px;
  border: 2px solid;
  opacity: 0.15;
}
.svc-row--us .svc-row__arch { border-color: var(--gold); opacity: 0.25; }
.svc-row--grad .svc-row__arch { border-color: var(--green); }
.svc-row--multi .svc-row__arch { border-color: var(--green); width: 200px; height: 320px; bottom: 0; }

/* Image scaling */
.svc-row__visual img {
  position: relative;
  z-index: 2;
  height: 95%;
  width: auto;
  object-fit: contain;
  object-position: bottom center;
  transition: transform 0.6s var(--ease);
}
.svc-row:hover .svc-row__visual img {
  transform: scale(1.04);
}
.svc-row--us .svc-row__visual img {
  height: 105%;
  margin-bottom: -15px;
}
.svc-row--grad .svc-row__visual img {
  height: 100%;
}
.svc-row--multi .svc-row__visual img {
  height: 110%;
  margin-bottom: -10px;
}
.svc-row--transfer .svc-row__visual img {
  height: auto;
  width: 90%;
  object-position: bottom center;
  margin-bottom: -20px;
}

/* Highlight US Undergrad (Bigger) */
@media (min-width: 768px) {
  .svc-row--us {
    height: 480px; /* Higher priority */
  }
  .svc-row--us h3 { font-size: 42px; }
  .svc-row--us .svc-row__desc { font-size: 18px; }
  .svc-row--us .svc-row__arch { width: 340px; height: 460px; }
}

/* Mobile adjustments */
@media (max-width: 767px) {
  .svc-row__content { padding: 40px 24px; }
  .svc-row h3 { font-size: 28px; }
  .svc-row__visual { min-height: 260px; }
  .svc-row__arch { width: 220px; height: 300px; bottom: -10px; }
  .svc-row--us .svc-row__visual img { height: 110%; margin-bottom: -10px; }
}
"""

html = """
  <!-- ===== 板块 1 · 申请路径（交替图文排版） ===== -->
  <section class="section services" id="service-summary">
    <div class="section__head reveal">
      <p class="eyebrow">SERVICES</p>
      <h2>专注美国顶尖名校，布局全球视野</h2>
      <p class="lead">以美国本科申请为核心引擎，同时提供研究生、本科转学及多国联申服务，满足不同阶段的高端留学需求。</p>
    </div>
    
    <div class="svc-rows">
      <!-- 1. 美国本科 (Image Right) - Highlighted -->
      <a href="meiben" class="svc-row reveal svc-row--us">
        <div class="svc-row__content">
          <h3>美国本科<span class="svc-row__tag">核心引擎</span></h3>
          <p class="svc-row__desc">成长规划、学术硬实力、申请表达与影响力三大模块，由全常春藤导师团队深度把控，发掘独一无二的智识好奇心。</p>
          <div class="svc-row__btn">了解详情 <svg><use href="#ic-arrow"/></svg></div>
        </div>
        <div class="svc-row__visual">
          <div class="svc-row__arch"></div>
          <img src="assets/svc-liberty.webp" alt="美国本科" loading="lazy" />
        </div>
      </a>
      
      <!-- 2. 研究生 (Image Left) -->
      <a href="graduate" class="svc-row reveal svc-row--grad svc-row--reverse">
        <div class="svc-row__content">
          <h3>研究生申请</h3>
          <p class="svc-row__desc">从选校定位、精细化文书打磨到全真面试辅导，扫除申请盲区，为名校录取和长远职业发展铺路。</p>
          <div class="svc-row__btn">了解详情 <svg><use href="#ic-arrow"/></svg></div>
        </div>
        <div class="svc-row__visual">
          <div class="svc-row__arch"></div>
          <img src="assets/svc-dome.webp" alt="研究生申请" loading="lazy" />
        </div>
      </a>
      
      <!-- 3. 多国联申 (Image Right) -->
      <a href="uk-eu" class="svc-row reveal svc-row--multi">
        <div class="svc-row__content">
          <h3>多国联申</h3>
          <p class="svc-row__desc">美、英、加、港、新等多赛道同时发力。同一份顶尖准备，科学重组多国投递矩阵，实现录取概率最大化。</p>
          <div class="svc-row__btn">了解详情 <svg><use href="#ic-arrow"/></svg></div>
        </div>
        <div class="svc-row__visual">
          <div class="svc-row__arch"></div>
          <img src="assets/svc-bigben.webp" alt="多国联申" loading="lazy" />
        </div>
      </a>
      
      <!-- 4. 转学 (Image Left) -->
      <a href="transfer" class="svc-row reveal svc-row--transfer svc-row--reverse">
        <div class="svc-row__content">
          <h3>本科转学</h3>
          <p class="svc-row__desc">精准的学分规划与转学策略制定，重新盘活现有学术资源，把当前的 GPA 变成冲击梦校的坚实跳板。</p>
          <div class="svc-row__btn">了解详情 <svg><use href="#ic-arrow"/></svg></div>
        </div>
        <div class="svc-row__visual">
          <img src="assets/svc-books.webp" alt="本科转学" loading="lazy" />
        </div>
      </a>
    </div>
  </section>
"""

with open('frontend/css/style.css', 'r', encoding='utf-8') as f:
    style_content = f.read()
    
# Append css
with open('frontend/css/style.css', 'a', encoding='utf-8') as f:
    f.write("\n" + css + "\n")

# Replace HTML
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

start_marker = '  <!-- ===== 板块 1 · 申请路径'
end_marker = '  <!-- ===== 板块 2 · 数据条'

start_idx = html_content.find(start_marker)
end_idx = html_content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_content = html_content[:start_idx] + html + "\n" + html_content[end_idx:]
    with open('frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Services HTML replaced.")
else:
    print("Could not find HTML markers.")
