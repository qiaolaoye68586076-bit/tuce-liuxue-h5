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

| 模块 | ID | 状态 |
|---|---|---|
| 导航 | `#nav` | ✅ 完成 |
| Hero 首屏 | `#top` | ✅ 完成（底图已有）|
| 核心亮点滑动卡片 | `#stats` | ⚠️ 卡片图片是占位符 |
| 服务 | `#services` | ✅ 完成 |
| 本科服务体系 | `#system` | ✅ 完成 |
| 为什么选途策 | `#why` | ✅ 完成 |
| 途策方法论 | `#method` | ✅ 完成 |
| 申请流程 | `#process` | ✅ 完成 |
| 文书训练营 | `#camp` | ✅ 完成 |
| 师资 | `#mentors` | ⚠️ 导师信息是占位（哈佛/耶鲁/斯坦福/MIT），待替换真实信息 |
| 录取去向 | `#offers` | 🗑️ 已删除（数据为虚构占位，待真实录取数据后重建）|
| 成功案例 | `#stories` | ⚠️ W/L/C 同学均为占位，需替换为真实授权案例 |
| 常见问题 FAQ | `#faq` | ✅ 完成（5 条手风琴，已有 JSON-LD 结构化数据）|
| 留资表单 | `#consult` | ✅ UI 完成，后端接口 `LEAD_ENDPOINT` 留空待配置 |
| 页脚 | — | ⚠️ ICP 备案号占位（`沪ICP备 0000000 号`）|

---

## 待办事项

### 内容替换（需客户提供）
- [ ] 核心亮点卡片：替换 4 张"Image placeholder"为真实图片
- [ ] 师资团队：替换为真实导师姓名、学校、照片
- [ ] 成功案例：W/L/C 同学 → 真实授权案例（文案 + 照片 + 学校）
- [ ] 录取院校墙：确认真实历届录取去向
- [ ] 页脚 ICP 备案号
- [ ] 协议弹层：替换为正式《用户协议》与《隐私政策》全文

### 技术待接入
- [ ] 留资表单后端：配置 `LEAD_ENDPOINT`（`js/main.js` 第 9 行）
- [ ] 微信公众号二维码：`assets/qr-official.png`（目前缺图有兜底）

### GEO / SEO（AI 可见度）
- 诊断结论：途策留学**目前未被 AI 提及**（见 `途策留学_GEO诊断报告.md`）
- 已做：
  - [x] FAQ JSON-LD 结构化数据、EducationalOrganization schema（含 logo/address/knowsAbout）
  - [x] `robots.txt`：允许百度/字节/DeepSeek/GPTBot/Claude 等 AI 爬虫
  - [x] `sitemap.xml`：首页 + cases.html，已含 cases 条目
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

---

## 触发词 · 自动执行

> **当用户说「完成」「结束」「收工」（任意一个），立即执行以下操作，不需要用户另行要求：**
>
> 1. 在 `LOG.md` 末尾追加本次对话的条目（用顶部模板格式）
> 2. 更新 `CLAUDE.md` 里"已完成的对话记录"表格
> 3. 更新"待办事项"中已完成项的状态
> 4. 用中文简短告知用户"已记录"

## 其他约定

- 说 **"记住这个：……"** → 存入 `memory/` 系统
- 说 **"待办清单"** → 列出所有未完成项
- `LOG.md` 顶部有模板，debug 踩坑单独列表格
