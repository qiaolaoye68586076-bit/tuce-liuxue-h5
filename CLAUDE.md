# 途策留学 H5 官网 · 项目记事本

> 每次对话结束前说"总结一下"，我会把进展更新到这里。新开对话会自动读取。

---

## 项目概况

**客户：** 途策留学（TUCE Education）/ 上海途策必达教育科技有限公司  
**项目：** H5 官网（多页面架构，静态前端 + 轻后端规划中）；已正式上线 **https://tuce.asia**（Let's Encrypt SSL / HTTP→HTTPS 强跳 / ICP 备案 `沪ICP备2026025218号-2`，2026-07-08）；ECS IP `121.43.101.155`  
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
docs/                      项目文档（DOMAIN-CUTOVER / DESIGN-BRIEF / GEO 笔记 / mentor-prompts 等）
archive/                   归档：legacy/ 旧版 + site/ Astro 探索项目
reference/                 竞品参考（stoooges）
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
| `services.html` | 美本专题（三大模块）+ 核心亮点轮播 + 其他服务网格 + 文书训练营 | ✅ 内容已替换为真实素材 |
| `teachers.html` | 师资团队 THE TEAM（4 位导师） | ✅ 真实导师姓名/学校/经历已上线 |
| `cases.html` | 数据带 + 成功案例 + 完整策略复盘（ItemList/Review Schema）+ 录取去向 + 学员之声 | ✅ 真实化名案例（Yu/Li/Wang 同学）已上线 |

---

## 待办事项

> 网站主体内容与上线流程已基本完成（域名/HTTPS/备案/真实案例师资内容均已就绪）。以下是当前仍需跟进的事项。

### 待提交 / 待 commit（当前工作区）
- [ ] 移动端 / Safari 响应式修复批次：`style.css`（Hero 窄屏居中构图、服务卡移动端信息增量、博客滑动提示等）+ `timeline.css` + 10 个页面的配套改动，目前在工作区未提交
- [ ] `nginx.conf.example` 本地改动（新增 `/index.html` → `/` 与 `.html` 后缀隐藏的 301 规则）需要与线上 nginx 实际配置核对后一并提交，避免文档与服务器再次漂移
- [x] 根目录临时实验脚本（`fix_*.py` / `timeline*.html` / `generate_*.js` / `replace_*.py` 等）已清理，无残留

### 后端（留资表单）文档校正
- [x] 后端已实现并接入：`backend/app.py`（Python 标准库 `http.server` + `sqlite3`，零第三方依赖，因生产环境是 Python 3.6.8 装不了 Flask 3.x）；前端 `LEAD_ENDPOINT` 已指向 `/api/lead`（`frontend/js/main.js` 第 9 行）；`nginx.conf.example` 已有 `/api/` 反代配置
- [ ] `backend/README.md` 内容仍按旧版 "Flask + gunicorn" 方案写的，与 `app.py` 实际实现（零依赖标准库 + `python3 app.py` 直跑）不符，需要重写
- [ ] 确认后端服务是否已在 ECS 上以 systemd 常驻运行：LOG.md 里没有找到部署这一步的记录，需要登录服务器核实 `/api/health` 与 systemd 状态，并把部署步骤（systemd unit）补进 `DEPLOY.md`
- [ ] `deploy.sh` 目前只同步 `frontend/`，`backend/` 无自动化部署，需要时再评估是否值得写脚本

### 内容 / 素材（仍缺的部分）
- [ ] 协议弹层：替换为正式《用户协议》与《隐私政策》全文
- [ ] `cases.html#offers` 录取院校墙：核对是否为最新历届录取去向
- [ ] 9 个页面缺 `og:image`：services.html / meiben.html / writing-camp.html / graduate.html / transfer.html / uk-eu.html / teachers.html / cases.html / blog 详情页 —— 候选并入未来 GEO 批次

### GEO / SEO（AI 可见度）
- 已做：FAQ JSON-LD、EducationalOrganization schema、robots.txt（20+ 爬虫）、sitemap.xml 全页面、cases.html ItemList/Review schema、SSL、ICP 备案号
- 待做：
  - [ ] 站长验证：`frontend/` 下有两个哈希命名的验证文件（`8d888b2710be614049407f79e9395e79.txt` / `bdd3055ef7c866ad0b37748db446f15b.txt`），需要确认分别对应百度/Bing/360 中的哪家、验证是否已在对应站长平台完成
  - [ ] 正式提交 `https://tuce.asia/sitemap.xml` 给百度站长平台 + Bing + Google Search Console
  - [ ] 知乎机构号 + 第一篇 GEO 文章
  - [ ] 百度百家号开通

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
| 2026-07-08 | **🚀 备案通过正式上线（域名 + HTTPS + 备案号）**：ICP `沪ICP备2026025218号-2` 下证；阿里云 DNS 加 `tuce.asia`+`www` A 记录 + 安全组放行 443；服务器装 certbot 1.22.0 签 Let's Encrypt 证书（`--nginx --redirect`，有效期至 10/6 自动续），`server_name _`→`tuce.asia www.tuce.asia`，HTTP→HTTPS 301；10 页页脚占位备案号→真实号+工信部链接，`./deploy.sh` 上线；11 页 HTTPS 全 200，服务器端核验通过。踩坑：本地代理 fake-ip 污染 dig/curl（改 DoH+ssh 核验）；timeline 脚本临时文件触发 deploy 的 title 守卫中止 |

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
  