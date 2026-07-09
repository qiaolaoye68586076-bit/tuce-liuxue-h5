with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

start_marker = '  <!-- ===== 板块 1 · 申请路径'
end_marker = '  <!-- ===== 板块 2 · 数据冲击'

html = """  <!-- ===== 板块 1 · 申请路径（交替图文排版） ===== -->
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

start_idx = html_content.find(start_marker)
end_idx = html_content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_content = html_content[:start_idx] + html + "\n" + html_content[end_idx:]
    with open('frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Services HTML replaced successfully.")
else:
    print("Could not find HTML markers.")
