# 途策留学 H5 官网 · 项目记事本

> 每次对话结束前说"总结一下"，我会把进展更新到这里。新开对话会自动读取。

---

## 项目概况

**客户：** 途策留学（TUCE Education）/ 上海途策必达教育科技有限公司  
**项目：** H5 官网（单页，静态 HTML/CSS/JS）  
**设计风格：** Collegiate Editorial Luxury — 深森林绿 + 暖金 + 米纸，Fraunces / 思源宋体  
**文件结构：**
```
index.html      主页面
css/style.css   全站样式
js/main.js      交互逻辑
assets/         图片、logo、二维码
reference/      竞品参考（stoooges）
途策留学_GEO诊断报告.md
途策官网_GEO搭建需求清单.md
GEO完整学习笔记.md
```

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
| 板块3 申请流程 | `#process` | 米色 | ✅ 三阶段滑动卡片 + 横向时间轴 |
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

### 内容替换（需客户提供）
- [ ] 核心亮点卡片：替换 `services.html#features` 4 张"Image placeholder"为真实图片
- [ ] 师资团队：`teachers.html` 替换为真实导师姓名、学校、照片
- [ ] 成功案例：`cases.html` W/L/C 同学 → 真实授权案例（文案 + 照片 + 学校 + 策略复盘）
- [ ] 录取院校墙：`cases.html#offers` 确认真实历届录取去向
- [ ] 页脚 ICP 备案号
- [ ] 页脚联系方式：替换占位 `400-XXX-XXXX` / `contact@tuce-edu.com` / `上海市 · 详细地址待补充`（4 页共用 footer，改一处需同步全站）
- [ ] 协议弹层：替换为正式《用户协议》与《隐私政策》全文

### 技术待接入
- [ ] 留资表单后端：配置 `LEAD_ENDPOINT`（`js/main.js` 第 9 行）
- [ ] 微信公众号二维码：`assets/qr-official.png`（目前缺图有兜底）

### GEO / SEO（AI 可见度）
- 诊断结论：途策留学**目前未被 AI 提及**（见 `途策留学_GEO诊断报告.md`）
- 已做：
  - [x] FAQ JSON-LD 结构化数据、EducationalOrganization schema（含 logo/address/knowsAbout）
  - [x] `robots.txt`：允许百度/字节/DeepSeek/GPTBot/Claude 等 AI 爬虫
  - [x] `sitemap.xml`：首页 + services.html + teachers.html + cases.html（重构后已补全）
  - [x] `cases.html` 案例详情页（ItemList + Review Schema）
  - [x] 首页 title 加年份"2026"
- 待做：
  - [ ] SSL 证书（阿里云，上线前必须）⚠️
  - [ ] ICP 备案号替换页脚占位符（备案审核中）
  - [ ] 向百度站长平台提交 sitemap（上线后）
  - [ ] 知乎机构号 + 第一篇 GEO 文章
  - [ ] 百度百家号开通
  - [ ] cases.html 填入真实案例内容

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
  