# 途策留学 H5 官网 · 项目记事本

> 每次对话结束前说"总结一下"，我会把进展更新到这里。新开对话会自动读取。

---

## 项目概况

**客户：** 途策留学（TUCE Education）/ 上海途策必达教育科技有限公司  
**项目：** H5 官网（多页面架构，静态前端 + 轻后端规划中）；已部署上线 http://121.43.101.155，ICP 备案中  
**设计风格：** Collegiate Editorial Luxury — 深森林绿 + 暖金 + 米纸，Fraunces / 思源宋体  
**文件结构：**（2026-06-18 工程化重构，前后端分离预留）
```
frontend/                  前端整体（部署时以此为 web 根目录）
├── index.html             主页面
├── *.html                 子页面（services/teachers/cases/blog/meiben…）
├── css/style.css          全站样式
├── js/main.js             交互逻辑（experience.js 动效 + vendor/ GSAP）
├── assets/                图片、logo、二维码
├── images/                封面图
├── articles.json          博客数据（index/blog 通过 fetch 读取）
├── robots.txt sitemap.xml SEO（须随 frontend/ 部署在域名根）
backend/                   预留 Flask（app.py / leads.db）
scripts/                   独立 Python 脚本（scrape_reference.py；sync_articles.py 待开发：cron 调公众号 API → articles.json）
docs/                      项目级文档（DOMAIN-CUTOVER.md 域名切换/备案验收清单；未来 handoff 文档归属地）
archive/                   归档：legacy/ 旧版 + site/ Astro 探索项目
reference/                 竞品参考（stoooges）
途策留学_GEO诊断报告.md / 途策官网_GEO搭建需求清单.md / GEO完整学习笔记.md
```
> ⚠️ 资源引用均为「无前导斜杠」相对路径，HTML 与 css/js/assets 保持同级，整体平移不破坏路径。部署务必让 `frontend/` 作为 web 根，否则 robots.txt/sitemap.xml 不在域名根，AI 爬虫读不到。

---

## 页面模块（从上到下）

> **2026-06-15 重构**：已从单页改为「首页 + 3 个子页面」。导航全站共用：`首页 | 服务 | 师资 | 案例 | 常见问题 | 免费评估`（已去数字编号；「常见问题」首页用 `#faq`、子页面用 `index.html#faq`）。背景色用 `.sec-bleed` 全宽底色带做板块区分。

**首页 `index.html`（Hero 之后只留 4 个板块 + FAQ）**

| 模块 | ID | 背景 | 状态 |
|---|---|---|---|
| 导航 | `#nav` | 半透明米白 | ✅ 共用，已去编号 |
| Hero 首屏 | `#top` | 深色底图 | ✅ 已删徽章，加品牌大字 `.hero-brand` |
| 板块1 策略定制 | `#strategy` | 米色 | ✅ 合并 why/method，4 张亮点卡 + 双出口 |
| 板块2 数据冲击 + 案例引导 | `#stats` | **深绿反白** | ✅ 数字 countUp+弹跳放大；案例卡占位 |
| 板块3 申请流程 | `#process` | 米色 | ✅ 描金书脊纵轴（三章十步目录页：sticky 章节碑 + 滚动描金书脊线 + 终点印章 CTA，2026-07-03 改版，去轮播）|
| 常见问题 FAQ | `#faq` | 微暖灰 | ✅ 5 条手风琴 + JSON-LD（在 CTA 前）|
| 板块4 联系我们 | `#consult` | **深绿** | ✅ UI 完成，`LEAD_ENDPOINT` 留空待配置 |
| 页脚 | — | 白 | ⚠️ ICP 备案号占位（`沪ICP备 0000000 号`）|

**子页面**

| 页面 | 承接内容 | 状态 |
|---|---|---|
| `services.html` | 美本专题（三大模块）+ 核心亮点轮播 + 其他服务网格 + 文书训练营 | ⚠️ 核心亮点 4 张图占位 |
| `teachers.html` | 师资团队 THE TEAM（4 位导师） | ⚠️ 导师信息占位（哈佛/耶鲁/斯坦福/MIT）|
| `cases.html` | 数据带 + 成功案例 + 完整策略复盘（ItemList/Review Schema）+ 录取去向 + 学员之声 | ⚠️ W/L/C 案例占位 |

---

## 待办事项

### 资源优化（M4/M5，已收尾）
- [x] **M4-a 清理 logo 死代码**（commit fbd8eda，零体积/零视觉变化）：删 main.js 切换死代码 + 11 HTML 冗余属性 + 删 logo-light.svg
- [x] **M4-b logo 压缩**（commit b3de3d9，已部署上线）：`logo-dark.svg`（内嵌 2048×2048 PNG）→ Pillow 合成 → 96×96 → `frontend/assets/logo.webp`（quality 90，3.7KB）；13 处引用替换；体积 1.27MB→3.7KB（-99.7%）；线上 logo.webp 200、旧 svg 404
- [x] **M5 修复 logo**（commit 5e52995，已部署上线）：M4-b 误把三合一设计拼版整张当 icon→页面显示「3 个小盾」；改为从拼版裁面板1单盾，方案A 保比例（77×96 居中于 96×96 透明画布）重导 → `logo.webp` 1832 字节；路径未变零 HTML/CSS 改动；线上 200 / Content-Length 1832

### 内容替换（需客户提供）
- [ ] 核心亮点卡片：替换 `services.html#features` 4 张"Image placeholder"为真实图片
- [ ] 师资团队：`teachers.html` 替换为真实导师姓名、学校、照片
- [ ] 成功案例：`cases.html` W/L/C 同学 → 真实授权案例（文案 + 照片 + 学校 + 策略复盘）
- [ ] 录取院校墙：`cases.html#offers` 确认真实历届录取去向
- [ ] 页脚 ICP 备案号
- [ ] 页脚联系方式：替换占位 `400-XXX-XXXX` / `contact@tuce-edu.com` / `上海市 · 详细地址待补充`（4 页共用 footer，改一处需同步全站）
- [ ] 协议弹层：替换为正式《用户协议》与《隐私政策》全文

### 技术待接入
- [ ] 留资表单后端（CTA）：Flask + SQLite + 微信推送（Server酱 或 pushplus）；前端已预留 `LEAD_ENDPOINT`（`frontend/js/main.js` 第 9 行），后端代码落地 `backend/app.py`（启用时注意 `LEAD_ENDPOINT` 注释示例域名修正，详见 docs/DOMAIN-CUTOVER.md §3.1）
- [ ] 微信公众号二维码：`frontend/assets/qr-official.png`（目前缺图有兜底）
- [ ] 公众号文章同步：Python cron job 调公众号 API → 生成 `frontend/articles.json`（脚本 `scripts/sync_articles.py` 待开发，blog.html 消费此文件）

> ⚠️ 后端上线时需同步扩展：`deploy.sh`（增加后端部署逻辑或拆出 `deploy-backend.sh`）/ `nginx.conf.example`（加 `location /api/` 反代到 Flask）/ `docs/DOMAIN-CUTOVER.md`（补后端域名策略一节）

### GEO / SEO（AI 可见度）
- 诊断结论：途策留学**目前未被 AI 提及**（见 `途策留学_GEO诊断报告.md`）
- 已做：
  - [x] FAQ JSON-LD 结构化数据、EducationalOrganization schema（含 logo/address/knowsAbout）
  - [x] `robots.txt`：允许百度/字节/DeepSeek/GPTBot/Claude 等 AI 爬虫
  - [x] `sitemap.xml`：全部 11 个页面（首页 / services 及 6 详情页 / teachers / cases / blog，M2-b 补全 blog）
  - [x] `cases.html` 案例详情页（ItemList + Review Schema）
  - [x] 首页 title 加年份"2026"
- 待做：
  - [ ] SSL 证书（阿里云，上线前必须）⚠️
  - [ ] ICP 备案号替换页脚占位符（备案审核中）
  - [ ] 向百度站长平台提交 sitemap（上线后）
  - [ ] 知乎机构号 + 第一篇 GEO 文章
  - [ ] 百度百家号开通
  - [ ] cases.html 填入真实案例内容
  - [ ] 9 个页面缺 og:image：services.html / meiben.html / writing-camp.html / graduate.html / transfer.html / uk-eu.html / single-service.html / teachers.html / cases.html —— 候选并入未来 GEO 批次
  - [ ] 备案后清理 nginx conflicting server name "_" warning（详见 docs/DOMAIN-CUTOVER.md §4.11）

---

## 已完成的对话记录

| 日期 | 做了什么 |
|---|---|
| 2026-06-12 | 添加 FAQ 模块（手风琴交互 + JSON-LD 结构化数据）；导航加入"常见问题"链接 |
| 2026-06-12 | 建立 CLAUDE.md 项目记事本 + LOG.md 开发日志 + memory 自动记忆系统；配置收尾触发词 |
| 2026-06-12 | GEO 技术优化：robots.txt / sitemap.xml / JSON-LD 补全 / cases.html 新建 / #offers 删除 / stories 加跳转链接 |
| 2026-06-15 | #stats 数据带数字样式升级（衬线体 / 36px / 500）+ 滚动动画重写（IntersectionObserver threshold:0.3 / bandTriggered flag / 量词内联 / +号金色） |
| 2026-06-15 | GEO 深度升级：robots.txt 修复错误 UA 并扩充至 20+ 平台（含千问/Kimi/Grok）；head 补全 OG 图片/Twitter Card/地区声明；JSON-LD 升级双类型 + 服务目录 |
| 2026-06-15 | 全局颜色字体优化：金色→#A89157 / 正文灰三级(555/888/999) / 行高统一1.8 / 赤陶色CTA按钮(.btn--cta) / 导航+Hero去宽度限制通栏化 / 清理重复CSS副本 |
| 2026-06-15 | **官网重构**：导航改版（首页\|服务\|师资\|案例）；首页做减法只留 4 板块；新建 services/teachers/cases 三个子页面承接迁移内容；申请流程改滑动卡片+横向时间轴；main.js 表单加守卫可跨页共用 |
| 2026-06-15 | 第二轮细调：导航去数字编号；Hero 删徽章+加品牌大字；数字区放大 1.6×+落定弹跳+单位描金；板块换色(`.sec-bleed` 深绿/微灰区分)；确认 FAQ 在 CTA 前 |
| 2026-06-16 | 导航新增「常见问题」项（案例与免费评估之间）：首页用 `#faq`、子页面用 `index.html#faq`，桌面+移动抽屉全部同步（4 页共 8 处） |
| 2026-06-16 | 第三轮调整：申请流程时间轴 flex 化连线占满卡片宽度（含移动端竖向）；Footer 改深色四栏（品牌/联系方式/快速链接/关注我们）+底部版权条，4 页共用；导航免费评估按钮加浮动+脉冲动画（hover 暂停）；首页导师团队链接改描边按钮 `.btn--line`；css `?v=5` 破缓存 |
| 2026-06-18 | **工程化目录重构**：HTML+css/js/assets/images+articles.json+SEO 整体平移入 `frontend/`（相对路径零改动，77 文件 git mv 保历史）；新建 `backend/`(Flask 预留)、`scripts/`(scrape_reference.py 归位+修 ROOT)；`legacy/`+`site/` 归档进 `archive/`；`.gitignore` 加 backend 运行时忽略 |
| 2026-06-18 | **ECS 部署上线**：阿里云华东1（2核2GB / Alibaba Cloud Linux 3 / Nginx 1.24），公网可访问 http://121.43.101.155（备案中暂用 IP）；**M1 部署工具链**（commit 6482182）：deploy.sh（dry-run/verbose/backup + title 校验 + nginx -t&reload）/ DEPLOY.md / nginx.conf.example；顺带清理 37MB 冗余资源（618d4f7）|
| 2026-06-19 | **M2 SEO 修复批次**：og:image 全站统一为 og-cover.jpg（index 3 处 + blog 死链修复，png→jpg 1.46MB→293KB，f2b582a）；blog.html 补进 sitemap 10→11 条（487cf65）；新建 **docs/DOMAIN-CUTOVER.md**：81 处 tuce.asia 硬编码盘点（A–F 六类）+ 备案验收清单 + 替换备用方案（5cfda8e）|
| 2026-06-19 | **M4-a 清理 logo 死代码**（commit fbd8eda）：main.js 删 logo 切换死代码 10 行（`var brandLogo`/`setLogo()`/onScroll 两处调用）；11 个 HTML 剥离冗余 `data-logo-light`/`data-logo-dark` 属性；删零引用、与 logo-dark.svg 字节级相同的 `logo-light.svg`（1.27MB）。零视觉变化，为 **M4-b（logo 压缩）** 铺路 |
| 2026-06-19 | **M4-b 压缩 logo**（commit b3de3d9，已部署上线）：Pillow 从 logo-dark.svg 提取内嵌 PNG（RGB 彩色图 + L 灰度遮罩 putalpha 合成）→ 96×96 → `logo.webp`（q90，3.7KB）；删 logo-dark.svg + 替换 13 处引用（11 img + 2 JSON-LD）；同步 DOMAIN-CUTOVER/DESIGN-BRIEF/design-assets-needed；体积 1.27MB→3.7KB（-99.7%）；线上 logo.webp 200 image/webp、旧 svg 404 |
| 2026-06-19 | **M5 修复 logo**（commit 5e52995，已部署上线）：诊断出 M4-b 的「源图」`logo-dark.svg` 实为 2048×2048 三合一设计拼版（面板1 绿盾/面板2 Logo-Light/面板3 Favicon），整张缩放导致页面显示「3 个小盾」；从拼版裁面板1单盾（合成透明底→裁 `(293,110)-(1024,1024)`→alpha tight-crop 得 704×882），方案A 保比例缩 77×96 居中于 96×96 透明画布 → `logo.webp` 1832 字节；路径未变零 HTML/CSS 改动；线上 200 / Content-Length 1832（注：commit 仅本地未 push 远端 git）|
| 2026-06-26 | SSH 密钥配置 + 推送 5 个提交：生成 RSA 4096 位 SSH 密钥对并添加到 GitHub；推送 5 个本地提交（M5 commit 5e52995 + 新增 4 个 feat/chore）到 origin/main；branch tracking 已建立 |
| 2026-07-08 | **转学页+多国联申页全面改版 + 首页蛇形布局 + 师资横条 + 洞察期刊目录式**：转学页 tf-* 新内容（对比表/六要素/权重/截止日/结论卡）；多国联申四幕叙事重构（诊断→案例→方案→结果）；美本训练营深绿主卡（camp-* 课程表+成果条+理念对开）；首页流程 organic-snake SVG 蜿蜒布局取代滑动卡片；首页师资横条 team-band（4 位导师头像叠排+锚点深链）；首页洞察改版为特稿/索引期刊编辑式；导航全站统一「多国联申」+ 删除 single-service.html（6 处引用重定向）；CSS brace 修复 + 统一版本号 edd8afa3 |

---

## 触发词 · 自动执行

> **当用户说「完成」「结束」「收工」（任意一个），立即执行以下这些操作，不需要用户另行要求：**
>
> 1. 在 `LOG.md` 末尾追加本次对话的条目（用顶部模板格式）
> 2. 更新 `CLAUDE.md` 里"已完成的对话记录"表格
> 3. 更新"待办事项"中已完成项的状态
> 4. 用中文简短告知用户"已记录"

## 其他约定

- 说 **"记住这个：……"** → 存入 `memory/` 系统
- 说 **"待办清单"** → 列出所有未完成项
- `LOG.md` 顶部有模板，debug 踩坑单独列表格
  