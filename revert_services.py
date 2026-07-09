with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

start_marker = '  <!-- ===== 板块 1 · 申请路径'
end_marker = '  <!-- ===== 板块 2 · 数据冲击'

original_html = """  <!-- ===== 板块 1 · 申请路径（银雕陈列廊：1 深绿主展厅 + 3 侧廊展柜） ===== -->
  <section class="section services" id="service-summary">
    <div class="section__head reveal">
      <p class="eyebrow">SERVICES · 服务入口</p>
      <h2>先找到适合你的申请路径</h2>
      <p class="lead">从美国本科到研究生，从多国混申到本科转学——首页只保留四个关键入口，完整的方法论在各服务页里讲清楚。</p>
    </div>
    <div class="svcgal">
      <a class="svcgal-card svcgal-card--us reveal" href="meiben">
        <span class="svcgal-card__no" aria-hidden="true">01</span>
        <span class="svcgal-card__chip" aria-hidden="true"><svg class="ic"><use href="#ic-arrow"/></svg></span>
        <h3>美国本科<span class="svcgal-card__tag">·核心业务</span></h3>
        <p class="svcgal-card__desc">成长规划、学术硬实力、申请表达与影响力三大模块，整合名校文书训练营。</p>
        <ul class="svcgal-card__pts" role="list"><!-- 移动端专属：不点进去也能看到服务包含什么 -->
          <li>成长规划</li>
          <li>学术硬实力</li>
          <li>申请表达与影响力</li>
          <li>名校文书训练营</li>
        </ul>
        <span class="svcgal-card__stage" aria-hidden="true">
          <i class="svcgal-card__arch"></i>
          <img src="assets/svc-liberty.webp" alt="" width="511" height="1400" loading="lazy" />
          <em class="svcgal-card__fig">Fig. 01 · Liberty, New York</em>
        </span>
      </a>
      <a class="svcgal-card svcgal-card--sm svcgal-card--grad reveal" href="graduate">
        <span class="svcgal-card__no" aria-hidden="true">02</span>
        <span class="svcgal-card__chip" aria-hidden="true"><svg class="ic"><use href="#ic-arrow"/></svg></span>
        <h3>研究生</h3>
        <p class="svcgal-card__desc">专业定位、文书面试到签证入学，一路陪到落地。</p>
        <p class="svcgal-card__mods">综合评估 · 精准定位 · 笔面试辅导 · 职业规划与签证</p>
        <span class="svcgal-card__stage" aria-hidden="true">
          <i class="svcgal-card__arch"></i>
          <img src="assets/svc-dome.webp" alt="" width="536" height="1000" loading="lazy" />
          <em class="svcgal-card__fig">Fig. 02 · The Dome</em>
        </span>
      </a>
      <a class="svcgal-card svcgal-card--sm svcgal-card--multi reveal" href="uk-eu">
        <span class="svcgal-card__no" aria-hidden="true">03</span>
        <span class="svcgal-card__chip" aria-hidden="true"><svg class="ic"><use href="#ic-arrow"/></svg></span>
        <h3>多国联申</h3>
        <p class="svcgal-card__desc">美英加港新组合投递，把录取概率科学重组。</p>
        <p class="svcgal-card__mods">冲刺·稳妥·保底三档组合 · 一份准备多线投递</p>
        <span class="svcgal-card__stage" aria-hidden="true">
          <i class="svcgal-card__arch"></i>
          <img src="assets/svc-bigben.webp" alt="" width="252" height="1000" loading="lazy" />
          <em class="svcgal-card__fig">Fig. 03 · Westminster</em>
        </span>
      </a>
      <a class="svcgal-card svcgal-card--sm svcgal-card--transfer reveal" href="transfer">
        <span class="svcgal-card__no" aria-hidden="true">04</span>
        <span class="svcgal-card__chip" aria-hidden="true"><svg class="ic"><use href="#ic-arrow"/></svg></span>
        <h3>转学</h3>
        <p class="svcgal-card__desc">学分规划与转学申请，把 GPA 变成向上的跳板。</p>
        <p class="svcgal-card__mods">12 个月接力规划 · 学分转换 · 转学文书与截止日</p>
        <span class="svcgal-card__stage" aria-hidden="true">
          <img src="assets/svc-books.webp" alt="" width="900" height="1005" loading="lazy" />
          <em class="svcgal-card__fig">Fig. 04 · Ascending Stacks</em>
        </span>
      </a>
    </div>
  </section>
"""

start_idx = html_content.find(start_marker)
end_idx = html_content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_content = html_content[:start_idx] + original_html + "\n" + html_content[end_idx:]
    with open('frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Reverted HTML successfully.")
else:
    print("Could not find HTML markers.")

