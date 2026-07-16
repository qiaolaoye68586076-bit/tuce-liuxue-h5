# 途策留学 H5 · 开发日志

> 说 **"总结一下"** 时，我会把本次对话追加到这里。

---

## ✦ 模板（复制这段开新条目）

```
## [YYYY-MM-DD] 第 N 次对话

### 完成
- 

### Debug / 踩坑
| 现象 | 原因 | 解决方式 |
|---|---|---|
|  |  |  |

### 遗留 / 下次继续
- 
```

---

## 已知 Bug & 长期注意事项

> 这里记「坑」，不记单次 debug——以后改代码时先瞄一眼。

| # | 位置 | 现象 | 状态 |
|---|---|---|---|
| 1 | `footer` | ~~ICP 备案号是占位 `沪ICP备 0000000 号`~~ | ✅ 已替换为 `沪ICP备2026025218号-2` + 工信部链接（2026-07-08 上线） |
| 2 | `#stats` 卡片 | 4 张图是 "Image placeholder"，未接真图 | ⏳ 待素材 |
| 3 | `#mentors` | 导师信息（哈佛/耶鲁等）为示例，未经授权 | ⏳ 待客户确认 |
| 4 | `cases.html` `#case-w/l/c` | W/L/C 同学案例为虚构占位（已迁至案例页） | ⏳ 待真实授权案例 |
| 5 | `js/main.js:9` | `LEAD_ENDPOINT` 留空，表单提交走本地模拟 | ⏳ 待后端接口 |
| 6 | `assets/qr-official.png` | 公众号二维码缺图，有 CSS 兜底但不显示内容 | ⏳ 待素材 |
| 7 | `teachers.html` | 导师信息（哈佛/耶鲁等）为示例，已迁至师资页 | ⏳ 待客户确认 |
| 8 | `services.html` `#features` | 核心亮点 4 张图仍为 "Image placeholder" | ⏳ 待素材 |

---

## 2026-06-12 · 项目初始化 + FAQ

### 完成
- 初版 H5 上线（Hero / 服务 / 流程 / 师资 / 案例 / 表单 / 页脚）
- 添加 GEO 学习资料（诊断报告 / 需求清单 / 完整笔记）
- 新增 FAQ 模块：5 条手风琴 + JSON-LD 结构化数据（已在 `<head>` 中）
- 建立 `CLAUDE.md` 项目记事本 + `memory/` 自动记忆系统
- 建立本 `LOG.md` 开发日志

### Debug / 踩坑
| 现象 | 原因 | 解决方式 |
|---|---|---|
| FAQ 展开动画需要 `max-height` 而非 `hidden` | `hidden` 属性无法做 CSS 过渡 | 用 `max-height:0→400px` + `.open` class 切换 |

### 遗留 / 下次继续
- 所有占位内容等客户提供素材后替换
- GEO 内容布局（知乎 / 小红书 / 百科）尚未启动
- 后端表单接口待配置

---

## 2026-06-12 · 项目记录系统搭建

### 完成
- 建立 `CLAUDE.md` 项目记事本（模块状态 + 待办清单 + 触发词规则）
- 建立 `LOG.md` 开发日志（含模板 + 已知 Bug 汇总表）
- 建立 `memory/` 自动记忆系统（中文回复偏好 + 收尾触发词规则）
- 配置"完成 / 结束 / 收工"触发词：自动更新 LOG.md 和 CLAUDE.md

### Debug / 踩坑
| 现象 | 原因 | 解决方式 |
|---|---|---|
| — | — | — |

### 遗留 / 下次继续
- 等客户提供真实素材（图片、导师信息、录取案例）后统一替换占位内容

---

## 2026-06-12 · GEO 技术优化 + 案例页

### 完成
- 新建 `robots.txt`：显式允许百度/字节跳动/DeepSeek/GPTBot/Claude 等 AI 爬虫
- 新建 `sitemap.xml`：含首页（priority 1.0）+ cases.html（priority 0.9），changefreq weekly
- 补全 `index.html` JSON-LD：新增 `logo`、`address`（PostalAddress 上海）、`knowsAbout`（9个服务标签）
- `<title>` 加"2026"年份（AI 偏爱时效性标题）；meta keywords 补充决策词
- 新建 `cases.html` 案例详情页：含 ItemList + Review 双 Schema，3 张可填写模板
- `#stories` 三张卡片各加"查看完整案例 →"跳转链接（锚点精确到 case-w/l/c）
- `#stories` 底部加"查看全部录取案例 →"按钮
- 删除 `#offers`（录取去向）模块：数据为虚构占位，先撤除待真实数据
- 删除页脚"联系我们"列：与 QR 码功能重叠且全为占位，保持页脚简洁
- `sitemap.xml` 加入 cases.html 条目

### Debug / 踩坑
| 现象 | 原因 | 解决方式 |
|---|---|---|
| Bash 命令报 ENOSPC | /tmp 临时文件系统被截图 PNG 塞满 | 删 /tmp/tuce-*.png 清空间；后续截图用完立即清理 |
| `page.waitForTimeout` 报错 | puppeteer 新版已移除该 API | 改用 `new Promise(r => setTimeout(r, ms))` |

### 遗留 / 下次继续
- cases.html 三张卡片内容全为占位，需填入真实案例（桌面 01_学生案例/Offer库）
- SSL 证书尚未开启（已存 memory，上线前必须处理）
- 页脚地址/电话/邮箱待客户提供后补回
- ICP 备案号审核通过后替换占位符
- 网站上线后向百度站长平台提交 sitemap

---

## 2026-06-15 · GEO 全站 robots.txt + SEO meta + JSON-LD 深度升级

### 完成
- `robots.txt` 完整重写：修复原有两处归属错误（Qihoobot 归 360、YisouSpider 归神马），新增 360Spider / Shenmabot / Google-Extended / Googlebot-Image / msnbot / DuckDuckBot / YandexBot / ChatGPT-User / ClaudeBot / Tencent-Spider / DeepSeekBot / Bytespider / Qwen（通义千问）/ MoonshotBot（Kimi）/ xAI-Bot + Grok / facebookexternalhit + Facebot / Twitterbot / LinkedInBot / Applebot，共覆盖 20+ 平台
- `index.html` head 新增：Open Graph 完整组（og:image 1200×630、og:image:width/height/alt、og:locale zh_CN、og:site_name）、Twitter Card（summary_large_image）、author、content-language、geo.region CN-31、geo.placename 上海
- EducationalOrganization JSON-LD 增强：@type 升级为双类型 + LocalBusiness；alternateName 含英文名；新增 logo/image 字段；knowsAbout 扩充至 12 项；新增 hasOfferCatalog 服务目录（6 项）；sameAs 预留空数组

### Debug / 踩坑
| 现象 | 原因 | 解决方式 |
|---|---|---|
| 原 robots.txt Qihoobot 归到腾讯 | 命名混淆，Qihoo = 奇虎360 | 移至 360 条目组 |
| YisouSpider 原归 360 | 神马=移搜，yisou=移搜拼音 | 移至神马（sm.cn）条目组 |

### 遗留 / 下次继续
- 需在 `assets/` 新建 `og-cover.jpg`（1200×630）作为分享封面图，否则 OG 图片无效
- 通义千问 `Qwen`、Kimi `MoonshotBot`、xAI `xAI-Bot/Grok` 的官方爬虫 UA 尚未有公开文档，待后续确认
- `sameAs` 数组待上线后填入知乎机构号 / 公众号 / 微博链接

---

## 2026-06-15 · 数据统计区域数字样式 & 滚动动画升级

### 完成
- `index.html` `#stats .stats__band`：4 个 figure 改用新 data 属性（`data-target` / `data-unit` / `data-plus`），描述 span 加 `class="figure__desc"`，量词从描述文字分离为内联元素
- `css/style.css`：`.figure b` 字号改 28px（桌面 36px），字重 500，换用衬线体 Georgia/'Noto Serif SC'/Times New Roman；`.figure span` → `.figure__desc`（13px, #999）；新增 `.stat-unit`（14px, 金色 #A89157, sans-serif）、`.stat-plus`（金色）
- `js/main.js`：`animateCount` 改为新签名，用 `innerHTML` 写入数字 + `+` + 量词；IntersectionObserver 改为监听 `.stats__band` 整体（threshold: 0.3），`bandTriggered` flag 保证只触发一次；保留旧 `[data-count]` 观察器供 #offers 区块继续正常滚动
- 220、59、3 动画结束后出现金色 `+` 号；6（地区数固定）不加

### Debug / 踩坑
| 现象 | 原因 | 解决方式 |
|---|---|---|
| CSS 改动需更新两处 | `style.css` 内 stats 样式块重复出现两次 | 用 `replace_all:true` 一次同步两处 |

### 遗留 / 下次继续
- 等客户提供真实图片后替换 `#stats` 四张 "Image placeholder"

---

## 2026-06-15 · 全局颜色字体优化 + 导航/Hero 通栏化

### 完成
- `--gold` 更新为 `#A89157`（更饱和暖金）；`--muted` 更新为 `#888888`（二级辅助）
- 新增 `--terra: #B5542A` / `--terra-dk: #9A4723`（CTA 赤陶色）
- 正文灰色三级体系统一：主正文 `#555555` / 辅助 `#888888` / 最弱标签 `#999999`
- 中文正文段落（13–16px）`line-height` 全部统一为 `1.8`（原有 1.85/1.9/1.95 全部清理）
- 数字区 `.figure b` 新增 `letter-spacing: -.5px`，数字更紧凑有力
- 新增 `.btn--cta` 赤陶色实心按钮类；Hero/导航/抽屉/表单提交/浮动 CTA 共 5 处全部改用赤陶色
- 清除 `css/style.css` 中重复的 `.stats` 样式块（merge 遗留副本）
- `.nav__inner` 去掉 `max-width` + `margin:0 auto`，导航通栏，logo 贴左
- `.hero` 去掉 `max-width` + `margin:0 auto`，Hero 区通栏，标题铺满视口宽度

### Debug / 踩坑
| 现象 | 原因 | 解决方式 |
|---|---|---|
| `.figure b` 规则替换报两次匹配 | `style.css` 内 stats 块此前已有两份副本 | 先用 `replace_all:true` 同步，再删除第二份重复块 |

### 遗留 / 下次继续
- 标题深绿旧值 `#2C3E2D` 在当前代码中不存在（实际用 `--green: #14342B`），无需额外处理

---

## 2026-06-15 · 官网重构（导航改版 + 首页做减法 + 三个子页面）

### 完成
- **导航改版**（全站共用）：`首页 | 服务 | 师资 | 案例 | [免费评估]`，子页面 brand→index.html、CTA→index.html#consult，当前页加 `.is-active` 高亮
- **首页做减法**：Hero 之后只留 4 个板块 —— 板块1 策略定制（合并「为什么选途策 I-IV」+ 方法论关键词 G7/RP，4 张亮点卡 + 服务/师资双出口）→ 板块2 数据冲击 + 案例引导（数据带 countUp + 3 张精选案例卡 + 跳案例页）→ 板块3 申请流程（三阶段做成可滑动卡片 + 横向时间轴，窄屏转竖向）→ 板块4 联系我们（加引导语 + 原表单）；FAQ 保留在 CTA 前（GEO 资产）
- **新建 `services.html`**：美本核心业务专题大卡（含三大模块 01/02/03 完整文案）+ 核心亮点轮播 + 其他服务网格（研究生/转学/英欧加港/单项/商务，编号原样保留）+ 文书训练营 + CTA 带
- **新建 `teachers.html`**：复用深绿 THE TEAM 团队区，4 位导师信息完整保留 + CTA 带
- **重建 `cases.html`**：换用全站共用 header/footer，数据带 + 精选案例卡 + 完整策略复盘详情卡（保留 ItemList/Review Schema）+ 录取去向宣言 + 学员之声滚动剥卡 + CTA 带
- `css/style.css`：新增策略卡 `.hl`、流程时间轴 `.timeline/.tl-node`、子页 `.page-hero`、底部 `.cta-band`、美本 `.featured`、导航 `.is-active`；顺手修复旧 typo `..vcard`（双点）
- `js/main.js`：表单逻辑加 `if(form)` 守卫使其可被无表单子页安全共用；新增申请流程滑动卡片交互（dots/箭头/滚动联动）
- `sitemap.xml`：补入 services.html / teachers.html / cases.html

### Debug / 踩坑
| 现象 | 原因 | 解决方式 |
|---|---|---|
| main.js 在子页面会报错 | `form.addEventListener` 等无空值判断，子页无 `#leadForm` | 整块表单逻辑包进 `if (form) { … }` 守卫 |
| 一次性删除 8 个迁移板块 | Edit 需精确匹配大段 old_string | 用单次 Edit 把 system→stories 整段替换为 FAQ 注释锚点 |

### 遗留 / 下次继续
- 子页面占位内容（导师真实信息、案例详情、核心亮点配图）待客户提供后替换
- 旧 Astro `/cases/` 路由相关引用已全部改为 `cases.html`

---

## 2026-06-15 · 第二轮细节调整（导航去编号 + Hero 品牌字 + 数字冲击 + 板块换色）

### 完成
- **导航去编号**：4 个页面移除 `01/02/03/04` 数字前缀，只留文字
- **Hero**：删除顶部「◆ 途策留学 · TUCE EDUCATION ◆」徽章；副文案上方新增 `.hero-brand`「途策留学」大字（Fraunces/思源宋体衬线、clamp 34→58px、暖金 gold-soft、阴影、淡入）
- **数字统计区增强**：countUp 时长 1.5s→**1.8s**；数字落定后加 `is-pop` 类触发 `stat-pop` 弹跳关键帧（放大114%回弹）；字号桌面 36→58px / 移动 28→44px（≈1.6×）；`+` 号做上标小金字、单位（枚/所/大地区/届）相对数字 em 缩放+描金+错位
- **板块背景区分**：新增 `.sec-bleed` 全宽底色带工具类（`::before` width:100vw 居中铺底，不改结构）；板块2 数据=深绿反白、板块4 FAQ=微暖灰 `#EFEAE0`、板块5 CTA=更深一档绿 `#0F2820`；深色板块文字自动反白
- **FAQ 位置**：确认已在 CTA 前面，无需改动
- 补 reduced-motion 下 Hero 文案兜底可见性（防纯动画淡入元素在「减弱动效」时空白）

### Debug / 踩坑
| 现象 | 原因 | 解决方式 |
|---|---|---|
| `.section` 加 bg 色不通栏 | `.section` 有 max-width 居中 | 用 `::before` width:100vw + translateX(-50%) 铺满整屏底色 |
| 品牌字在 reduced-motion 下可能空白 | 靠 `opacity:0`+animation 淡入，减弱动效时 `animation:none` 致其停在 0 | 在 reduced-motion 块对 Hero 文案强制 `opacity:1` |

### 遗留 / 下次继续
- 本机无浏览器未做截图，建议本地 `open index.html` 滚动确认深色数据区反白数字弹跳 + 各板块换色边界 + 移动端大号数字不溢出

---

## 2026-06-16 · 导航新增「常见问题」项

### 完成
- 4 个页面导航栏（桌面 `.nav__links` + 移动 `.nav__drawer`）在「案例」与「免费评估」之间新增「常见问题」项，最终结构：`首页 | 服务 | 师资 | 案例 | 常见问题 | [免费评估]`
- 首页 `index.html` 用相对锚点 `#faq`（移动抽屉原已有，补齐桌面版）；子页面 `services/teachers/cases.html` 用 `index.html#faq`（跳回首页定位 FAQ）
- 确认首页 FAQ 板块已有 `id="faq"`（index.html:350）；平滑滚动依赖 CSS `html{scroll-behavior:smooth}`（style.css:39），无需新增

### Debug / 踩坑
| 现象 | 原因 | 解决方式 |
|---|---|---|
| — | — | — |

### 遗留 / 下次继续
- 无

---

## 2026-06-16 · 第三轮调整（时间轴占满 + Footer 深色四栏 + 导航 CTA 浮动 + 导师描边按钮）

### 完成
- **申请流程时间轴占满卡片宽度**：`.timeline` 从 grid 改 flex；连线 `.timeline::before` 贯穿整卡可用宽度（left:0/right:0），圆点 `.tl-node{flex:1}` + `left:50%` 居中均匀分布，编号/标题/描述居中对齐；2 步的「后申请季」卡片自动均分两段、连线仍撑满整宽；移动端（≤760px）切竖向时间轴（圆点回左侧、`:not(:last-child)::before` 逐节点串联竖线）
- **Footer 深色四栏改版（全站共用）**：深绿 `#102A20` 底 + 浅色字 + 金色顶线分隔；四栏 = 品牌（logo/标语）/ 联系方式（电话·邮箱·地址，含图标，均为占位）/ 快速链接（服务方案·师资团队·成功案例·常见问题）/ 关注我们（沿用顾问微信+公众号二维码）；底部分隔线放版权 + ICP 备案占位。4 个页面 footer 完全一致
- **导航「免费评估」浮动动画**：`.nav__cta` 加 `nav-cta-float`（2.6s ease-in-out 无限循环，上下 4px + box-shadow 脉冲），hover 时 `animation:none` 暂停回正常 hover 态；用 transform 不触发回流，导航不抖
- **首页导师团队链接改描边按钮**：`.strategy__exit-link` → 复用 `.btn.btn--line`（深绿描边+深绿字，hover 填深绿+白字），比实心橙主 CTA 略小一档；移动端（≤560px）双按钮竖向堆叠占满整行；删除已无用的 `.strategy__exit-link` 样式
- 4 个页面 `style.css?v=4` → `?v=5` 破缓存

### Debug / 踩坑
| 现象 | 原因 | 解决方式 |
|---|---|---|
| Bash 命令报 ENOSPC | 本机磁盘几近写满（约 4.2G 余量 / 96%），harness 临时输出文件写失败 | 等待瞬时占用回落后继续；输出重定向到工作区文件再读 |
| grep 退出码 1 中断脚本 | 当前 shell 带 `set -e`，grep 无匹配返回 1 即终止后续命令 | 各命令加 `|| true` 或用 `{ …; } || true` 包裹 |

### 遗留 / 下次继续
- 本机磁盘吃紧 + 无浏览器，未做截图；建议本地 `open index.html` 确认三张流程卡时间轴占满、Footer 四栏在桌面/移动端表现、导航 CTA 浮动不抖
- Footer 联系方式电话/邮箱/地址仍为占位（`400-XXX-XXXX` / `contact@tuce-edu.com` / 上海市），待客户提供真实信息

---

## 2026-06-18 · 工程化目录重构（前后端分离预留）

### 完成
- **前端整体平移**：11 个 HTML + `css/` `js/`（含 `vendor/`）+ `assets/` `images/` + `articles.json` + `robots.txt`/`sitemap.xml` 一起搬入 `frontend/`；因引用全是「无前导斜杠」相对路径、与资源目录保持同级，**HTML/JS 引用零改动**（已逐项校验命中）
- **新建工程目录**：`backend/`（Flask 预留，含 README，`leads.db` 已 gitignore）、`scripts/`（`scrape_reference.py` 归位）
- **归档弃用栈**：`legacy/`（旧版）+ `site/`（Astro 探索项目）统一移入 `archive/`，根目录清爽
- **脚本修补**：`scrape_reference.py` 移入 `scripts/` 后，`ROOT` 由 `dirname(__file__)` 改为再上一级，确保仍写入仓库根的 `reference/`
- **.gitignore**：新增 `backend/*.db`、`backend/instance/`
- **全程 `git mv`**：77 文件识别为 rename，git 历史 100% 保留（脚本 98%，因改了 ROOT 一行）
- 两次提交：`ee6a7bf`(refactor) + `5f43495`(docs 同步 CLAUDE.md 文件结构/路径/对话记录)

### Debug / 踩坑
| 现象 | 原因 | 解决方式 |
|---|---|---|
| 脚本移入子目录会写错位置 | `scrape_reference.py` 用 `ROOT=dirname(__file__)` 拼 `reference/`，移到 `scripts/` 后 ROOT 变成 scripts | 改为 `dirname(dirname(__file__))` 指向仓库根 |

### 遗留 / 下次继续
- ⚠️ **部署须知**：必须让 `frontend/` 作为 web 根目录，否则 `robots.txt`/`sitemap.xml` 不在域名根，AI 爬虫/百度读不到（关系到 GEO 与 SSL 上线）
- `backend/app.py` 待开发：接 `LEAD_ENDPOINT` 留资表单 + SQLite
- `scripts/sync_articles.py` 待开发：同步公众号文章 → `frontend/articles.json`

---

## 2026-06-18 · 部署上线 + 部署工具链（M1：首次公网可访问 + deploy.sh 一键部署）

### 完成
- **阿里云 ECS 部署上线**：华东1·杭州 2核2GB / Alibaba Cloud Linux 3 / Nginx 1.24；rsync 本地 `frontend/` → `/var/www/tuce/`，站点配置 `/etc/nginx/conf.d/tuce.conf`；**公网首次可访问 http://121.43.101.155**（备案中，暂用 IP）
- **SSH 免密直连**：配置密钥 + 本地 `~/.ssh/config` 别名 `ssh tuce` 一行直连；SSH 端口改 **22022**（学校 WiFi 封 22）；阿里云安全组放行 22022 / 80 / 443
- **M1 部署工具链（commit 6482182）**：
  - `deploy.sh`：rsync 部署脚本，`-n`(dry-run) / `-v`(verbose) / `--backup`；本地 `<title>` 校验、变更 stats 统计、>10 文件警告、远端 `nginx -t && reload`（graceful）
  - `DEPLOY.md`：中文部署文档 + 故障排查清单
  - `nginx.conf.example`：线上 Nginx 配置的版本控制副本
- **部署演练流程跑通**：`./deploy.sh -n` 验收得到「✓ 无变更，本地与远端已同步」干净基线，确立「演练 → 看 itemize → 正式部署」工作流
- **顺带清理 37MB 冗余资源（commit 618d4f7）**：删除 HTML 未引用的 mentor-01~04.png / qr 双份 / hero-bg / 重复封面，工作区 51MB → 14MB，rsync 才传得动

### Debug / 踩坑
| 现象 | 原因 | 解决方式 |
|---|---|---|
| SSH 连不上（22 端口）| 学校 Monash WiFi 封了 22 | sshd 配 `Port 22022` + 安全组加 22022 规则 |
| rsync 卡顿 / 上行极慢 | 学校 WiFi 上行 ~30KB/s + 大图体积 | 提前清理 37MB 冗余资源；rsync 加 `--progress --partial --timeout=120` |
| curl 80 端口不通 | 阿里云安全组 80 默认未开 | 手动添加 80 入站规则 |
| SSH 短暂 Connection refused | ECS 装新内核后自动重启 | 等 1–2 分钟自愈 |
| ssh-copy-id 推公钥失败 | 远端 authorized_keys 空文件写入异常 | 改手动 `cat >> ~/.ssh/authorized_keys` |
| deploy.sh 统计行解析不到字段 | macOS 自带 rsync 统计字段名与新版不同（无 "regular" 一词）| deploy.sh 改字段兼容写法 |

### 遗留 / 下次继续
- 备案下来后：切域名 tuce.asia（A 记录解析）+ 配 HTTPS（certbot）+ 清理 nginx conflicting server name warning（详见 docs/DOMAIN-CUTOVER.md）；当前仅 IP 访问，备案前国内访问 tuce.asia 会被拦截
- SSH 安全加固未完成：密钥已配但**密码登录未禁用**、22 端口未关、**fail2ban 未装**

---

## 2026-06-19 · SEO 修复批次（M2-a 统一 og:image + M2-b 域名硬编码盘点，顺带修两个 blog 隐性 bug）

### 完成
- **og:image 全站统一为 og-cover.jpg（M2-a，commit f2b582a，提交于 18 日深夜）**：index.html 3 处引用（og:image 行28 / twitter:image 行37 / JSON-LD image 行48）从 `.png` 统一到 `.jpg`；blog.html 的 og:image(行26)/twitter:image(行32) 本就指向 `.jpg`
- **PNG → JPG 转换**：`og-cover.png` 1.46MB → `og-cover.jpg` 293KB（sips quality 85，~1/5.5），删除冗余 png
- **docs/DOMAIN-CUTOVER.md 域名硬编码盘点（M2-b，commit 5cfda8e）**：盘点 `frontend/` 全部 **81 处** `https://tuce.asia` 引用，按 A–F 六类（canonical / og:url / og·twitter image / JSON-LD / robots / sitemap）逐文件逐行号登记；产出「备案当天验收清单」（DNS/HTTPS/curl/SEO 提交/nginx 收尾）为主 + 「全站替换备用方案」（find/sed）；含自校验命令（grep+wc 应返回 81）
- **blog.html 补进 sitemap（M2-b，commit 487cf65）**：sitemap.xml 10 条 → 11 条 `<loc>`，已部署上线，线上 `<loc>`=11 验证通过

### Debug / 踩坑
| 现象 | 原因 | 解决方式 |
|---|---|---|
| blog.html 分享无封面（og:image 死链）| 引用的 og-cover.jpg 根本不存在（仅有 png）| M2-a 转出 jpg 后，blog 死链顺带修复（文件名本就对）|
| blog.html 不被搜索引擎收录 | blog 漏进 sitemap.xml（只有 10 条，无 blog）| M2-b 盘点时发现，补为第 11 条 `<loc>` |
| grep 盘点漏引用 | 查 meta 标签名 `og:image` 只覆盖语义子集，漏掉 twitter:image / JSON-LD image | 改查文件名 `og-cover` 抓全所有引用（已存 memory）|

### 遗留 / 下次继续
- **9 个页面缺 og:image**：services.html / meiben.html / writing-camp.html / graduate.html / transfer.html / uk-eu.html / single-service.html / teachers.html / cases.html —— 候选并入未来 GEO 优化批次
- **备案后清理 nginx conflicting server name "_" warning**：详见 docs/DOMAIN-CUTOVER.md §4.11
- DOMAIN-CUTOVER.md 维护触发：新增 HTML 页面 / 新增 JSON-LD url / 修改 robots.txt 或 sitemap.xml 时，需重跑 `grep -rn "tuce\.asia" frontend/ | wc -l` 校准计数 + 同步更新第 2 节行号

---

## 2026-06-19 · M4-a 清理 logo 死代码 + 删 logo-light.svg（technical debt，零视觉变化）

### 完成
- **main.js 删 logo 切换死代码（10 行）**：移除 `var brandLogo`、`setLogo()` 函数、onScroll 内两处 `setLogo()` 调用 —— 该切换逻辑早已无效（明暗 logo 实为同一文件），属纯死代码
- **11 个 HTML 剥离冗余属性**：去掉 `<img id="brandLogo">` 上的 `data-logo-light` / `data-logo-dark`（两者都指向 `logo-dark.svg`，配合死代码才有意义），11 页同一行同一改法
- **删 `frontend/assets/logo-light.svg`（1.27 MB）**：零引用、与 `logo-dark.svg` 字节级相同的冗余文件
- commit `fbd8eda`（13 files changed, 11 insertions(+), 22 deletions(-)），已 push origin/main
- **无视觉变化**：导航 logo 渲染前后一致；为 M4-b（logo 压缩）做准备

### Debug / 踩坑
| 现象 | 原因 | 解决方式 |
|---|---|---|
| 新窗口接续时 Edit/部署「已是目标态」| 上一上下文窗口在总结前已执行完 11 个 Edit 并跑过正式 deploy，进度超出交接 prompt 记录 | grep 实测确认无 `data-logo` 残留 + `deploy.sh -n -v` 零传输零删除核实远端已同步，再据实推进 |
| `deploy.sh --dry-run` 显示「无变更」却看不清删除项 | `--stats` 的 transferred 只算「传输文件」不算「删除文件」，且 plain dry-run 未开 `--itemize-changes` | 改跑 `-n -v` 看 itemize 明细，确认零传输零删除才是远端真已同步 |

### 遗留 / 下次继续
- M4-b（logo 压缩）待启动：`logo-dark.svg` 内嵌 2048×2048 PNG → 提取 → resize 96×96 → 输出 `frontend/assets/logo.webp`（quality 90）

---

## 2026-06-19 · M4-b 压缩 logo（logo-dark.svg → logo.webp，-99.7% 体积，已部署上线验证）

### 完成
- **生成 `frontend/assets/logo.webp`（96×96 / quality 90 / 3.7KB）**：`logo-dark.svg` 内含 2 个 2048×2048 内嵌 PNG（1 个 RGB 彩色图 + 1 个 L 灰度遮罩，SVG 原以「灰度按亮度作 alpha 遮罩」合成）；用 Pillow 把灰度图作为 alpha 通道合到彩色图 → resize 96×96 → 存 WebP；读图肉眼确认深绿徽章 + 白/金 TUCE 标识与原 logo 一致、透明通道正常（alpha extrema 0–255）
- **删 `logo-dark.svg`（1.2MB）** + **13 处引用替换**（11 HTML img src + index/blog 各 1 处 JSON-LD `"logo"`），`sed 's/logo-dark\.svg/logo.webp/g'` 一并覆盖；frontend/ 零残留
- **文档同步**：`docs/DOMAIN-CUTOVER.md`（D2 logo 2 条登记，域名仍 tuce.asia 总计数 81 不变）+ `DESIGN-BRIEF.md`（3 处）+ `design-assets-needed.md`（2 处）
- commit `b3de3d9`（16 files），已 push；`deploy.sh` 正式部署 = transferred 12（11 HTML + logo.webp）+ `*deleting logo-dark.svg`，nginx reload 成功
- **线上验证**：`logo.webp` → HTTP 200 / `Content-Type: image/webp` / `Content-Length: 3786`；旧 `logo-dark.svg` → HTTP 404（`--delete` 生效）
- **体积净减 ≈1.27MB（-99.7%）**

### Debug / 踩坑
| 现象 | 原因 | 解决方式 |
|---|---|---|
| 首次生成的 logo.webp 是灰度图 | 两个内嵌 PNG 像素面积相同，按 `>` 严格比较挑「最大」时灰度遮罩先入选未被彩色图替换 | 改为显式按 mode 取 RGB 彩色图 + L 灰度遮罩，`putalpha` 合成才是浏览器真实渲染态 |
| 本机无 ImageMagick（`identify`/`convert` 缺失）| 仅装了 Pillow 12.2.0 | 全程用 Pillow，GATE 验证用 Pillow 等价输出尺寸/格式替代 `identify`，不额外装 ImageMagick |

### 遗留 / 下次继续
- 无（M4 资源优化批次 a/b 均收尾）；favicon、页脚 logo 占位等仍属设计资产待补（见 DESIGN-BRIEF.md）

---

## 2026-06-19 · M5 修复 logo（裁切拼版面板1单盾，方案A 保比例，已部署上线验证）

### 完成
- **根因诊断**：M4-b 当「源图」的 `logo-dark.svg` 内嵌 PNG 其实是一张 **2048×2048 三合一设计拼版**（面板1 Logo-Dark 绿盾透明底 / 面板2 Logo-Light / 面板3 Favicon Concept），M4-b 把整张拼版缩到 96×96 → 页面显示成「3 个小盾拼一起」
- **重新裁切导出**：`git show fbd8eda:logo-dark.svg` 恢复源 → 一次性脚本 `/tmp/crop_logo.py`（RGB 彩图 + L 遮罩 putalpha 合成透明底 → 裁面板1 `(293,110)-(1024,1024)` → alpha tight-crop 得单盾 704×882）
- **方案 A（保比例·透明补白）**：盾按比例缩为 77×96，居中贴到 96×96 透明画布（避免强压 1:1 把竖长盾拉胖），WebP q90 → **1832 字节**（比 M4-b 的 3786 更小）
- **覆盖 `frontend/assets/logo.webp`**：路径未变，11 个 HTML 的 `src="assets/logo.webp"` 零改动、无 CSS 改动（方案 A 不依赖 `.brand__logo` 宽高假设，handoff 无埋雷）
- commit `5e52995`（1 file）；`deploy.sh` 演练（-n -v）确认仅传 1 文件 → 正式部署 rsync 1 + nginx -t 通过 + reload 成功
- **线上验证**：`/assets/logo.webp` → HTTP 200 / `image/webp` / `Content-Length 1832`（与本地一致）

### Debug / 踩坑
| 现象 | 原因 | 解决方式 |
|---|---|---|
| logo 显示成 3 个小盾拼在一起 | M4-b 误把三合一设计拼版整张当单 icon 缩放 | 从拼版裁出左上面板1单盾再导出；以后拿「设计稿」当资源前先肉眼确认是单 icon 而非排版稿 |
| 单盾 704×882（竖长）压成 96×96 正方形被横向拉胖 | 源盾宽高比 0.80，强压 1:1 失真 | 方案 A：保比例缩放 + 居中透明补白成 96×96，不碰 CSS |

### 遗留 / 下次继续
- M5 commit `5e52995` 仅本地，未 `git push` 到远端 git（线上文件已 rsync 部署）；如需同步远端仓库再 push
- favicon 仍可从面板3「Favicon Concept 512×512」单独导出（待需要时）

---

## 2026-06-26 · SSH 密钥配置 + 推送 5 个提交

### 完成
- SSH 密钥不存在，生成新的 RSA 4096 位密钥对（`~/.ssh/id_rsa` + `~/.ssh/id_rsa.pub`）
- 将公钥添加至 GitHub Settings → SSH and GPG keys
- 推送 5 个本地提交到 `origin/main`：
  - aea7b81 feat(frontend): deploy latest updates and add new logos
  - c065483 chore(deploy): rsync 排除下划线前缀草稿页（/_*.html）
  - 13a2721 chore(deploy): CSS 版本号同步 → a11f6a6c
  - cc83c9a feat(blog): 洞察页进场动效 + 首页 #consult 锚点纠偏
  - d3b7115 feat(blog): 洞察页改版 + 纳入会话前全站 WIP（师资素材/文章同步脚本）
- branch 'main' now tracking 'origin/main'

### Debug / 踩坑
| 现象 | 原因 | 解决方式 |
|---|---|---|
| `git push` 提示 SSH 权限拒绝 | SSH 公钥未配置到 GitHub | 生成新 SSH 密钥对并添加公钥到 GitHub |

### 遗留 / 下次继续
- 无

## 2026-07-08 · 转学页+多国联申页全面改版 + 首页流程蛇形布局 + 洞察期刊目录式 + single-service 删除

**范围：** 25 文件（2577 插入 / 805 删除）
**commit:** `f025730`

### 内容改版
- **转学页** `transfer.html`：全新 tf-* 内容（数据带 + 对比表 + 六要素 + 权重公式 + 截止日 + 三条结论卡 + 关键材料卡），page-hero 深绿底图 + 动画入场
- **多国联申页** `uk-eu.html`：四幕叙事结构重排（诊断→案例→方案→结果），mc-bridge/mc-to-result 幕间过渡，section-nav 底部导航
- **美本训练营** `meiben.html#writing-camp`：camp-* 深绿主卡（3+2 课程表 + 成果条 + 理念对开 classroom 实拍）
- **首页洞察** `index.html#insights`：期刊编辑式版面（特稿 7fr + 索引 5fr + 藏书票兜底），tsweep 下划线动画
- **首页师资横条** `index.html#team`：team-band 纸白底（首尾引号 + 4 位导师头像叠排 + 锚点深链 teachers.html#mentor-xxx）
- **首页流程** `index.html#process`：organic-snake 蛇形布局（SVG 曲线 + 锚点圆点 + 终点印章）

### 导航重构
- 全站 nav/drawer 统一：「英欧加港本科」→「多国联申」，删除「单项服务」
- `single-service.html` 页面删除（6 处引用 → 咨询入口或服务总览）
- services.html svc-index/svcmap/gcard 三项引用全部替换

### CSS 修复
- Brace 平衡修正（2089:2087 → 2087:2087），修复了 `@media` 嵌套畸形区块
- 转学页 `.os-phase-bg` 标记为 legacy dead class
- 全局 `.sec-cream` 保留结构不变
- explore-card 升级（白卡 + box-shadow + 悬停位移）
- explore 区域 `explore__grid` 探索卡片改为暖白小卡片，删除左色带编号水印

---

## 2026-07-08 · 🚀 备案通过正式上线：域名 + HTTPS + 备案号

**里程碑：** ICP 备案（`沪ICP备2026025218号-2`）通过，站点从「IP 裸访问」升级为 `https://tuce.asia` 正式上线。

### 完成（上线六步）
1. **DNS 解析**：阿里云为 `tuce.asia` + `www` 加 A 记录 → `121.43.101.155`（TTL 600）
2. **安全组**：入方向放行 `443`（此前仅 80/22022）
3. **解析验证**：Google/阿里 DoH 双查均返回 `121.43.101.155`（绕开本地代理 fake-ip）
4. **SSL 证书**：服务器装 certbot 1.22.0 → `certbot --nginx -d tuce.asia -d www.tuce.asia --redirect`，Let's Encrypt 签发（有效期至 2026-10-06，自动续期任务已装，`renew --dry-run` 通过）
5. **nginx**：`server_name` 从占位 `_` 改为 `tuce.asia www.tuce.asia`（顺手消除文档 4.11 的 conflicting warning）；certbot 自动加 443 server 块 + HTTP→HTTPS 301
6. **备案合规**：10 个页面页脚 `沪ICP备 0000000 号` → `沪ICP备2026025218号-2`，并加 `beian.miit.gov.cn` 链接；随 `./deploy.sh` 上线

### 验收（服务器端 ground truth）
- 11 页 HTTPS 全部 200；HTTP→HTTPS 301；www 正常；证书 issuer=Let's Encrypt
- 服务器端 `grep`：10 页含真实备案号、0 页占位残留

### Debug / 踩坑
| 现象 | 原因 | 解决方式 |
|---|---|---|
| `ssh tuce` 报 `kex_exchange_identification: Connection closed` | 本地科学上网代理拦截了到固定 IP:22022 的 SSH 连接 | 关代理后 SSH 直通（**关代理**是前提） |
| 本地 `dig tuce.asia` 返回 `198.18.0.x` 假 IP | 代理 fake-ip 模式劫持 DNS | 改用 DoH（dns.google / 223.5.5.5）查真实公网解析 |
| 本地 `curl` 验证线上结果「时有时无」反复横跳 | 代理偶发拦截 curl，即使 `--resolve` 也可能被系统级代理绕过 | 一律以 `ssh` 到服务器 `grep /var/www/tuce/*.html` 为准 |
| `./deploy.sh` 中止：`_tl_test.html 缺 <title>` 但该文件又不存在 | timeline 生成脚本往 `frontend/` 写了一闪而过的临时 html，触发 deploy 的 title 守卫 | 临时文件清掉后重跑；**教训：生成脚本别往 `frontend/` 写临时文件** |
| 两次误报「已生效」 | 用 grep 过滤了 deploy 输出没看见中止；又信了被代理污染的 curl | 改为完整输出 + 服务器端核验 |

### 遗留 / 下次继续
- [ ] 提交 sitemap 给百度/Bing/Google（`https://tuce.asia/sitemap.xml`）
- [ ] 同步线上 nginx 配置回仓库 `nginx.conf.example`（现多了 443/证书/server_name）并 commit
- [ ] 清理仓库根目录临时实验文件（`fix_*.py` / `timeline*.html` / `generate_*.js` / `replace_*.py` 等）+ 提交 7/8 及本次改动

---

## [2026-07-16] 第 N+1 次对话 · SEO/GEO 全面优化

### 完成

**高优先级**
- **teachers.html 补 H1**：`<h2 class="team__title">` → `<h1 class="team__title">`（CSS class 选择器不受影响）
- **博客静态化**：新建 `frontend/articles/001–006.html`，含完整 SEO（Article + BreadcrumbList Schema、OG type=article + article:published_time ISO 8601、Twitter Card），CTA 按钮跳微信原文，sitemap 新增 6 篇文章条目
- **全站 BreadcrumbList**：17 个文件均补 JSON-LD 面包屑（首页→分类→页面名）

**中优先级**
- **deploy.sh sitemap 动态化**：新增 `bump_sitemap_lastmod()` 函数，每次部署 `sed` 替换为当天日期
- **llms.txt**：新建 `frontend/llms.txt`（AI 爬虫发现标准），含站点简介、核心页面列表、联系方式、6 篇文章索引
- **cases.html Wang Review**：补第三条 5 星 Review Schema
- **LCP 预加载**：index.html `<head>` 新增 `<link rel="preload" as="image" href="images/page-hero.webp" fetchpriority="high">`
- **旧 og-cover.jpg**：已删除（全站已切 og-cover-2026.jpg，零引用）

**低优先级**
- **robots.txt**：+GoogleOther / GoogleOther-Image / GoogleOther-Video（3 个 UA），-Claude-Web（无效 UA）
- **writing-camp 软重定向页**：robots→noindex，og:url 与 canonical 统一为 meiben，删重复 BreadcrumbList
- **5 服务详情页**：删旧版 "面包屑" BreadcrumbList（与批量添加的新版重复）

**架构修正**
- **articles.json url 字段回写**：服务器的 sync_articles.py 会覆盖 `url` 字段，本轮恢复为微信占位链接
- **JS 跳转改为 id 驱动**：blog.html + index.html 卡片点击改为 `localUrl(article)` 从 `a.id` 构造 `articles/${id}.html`，不再依赖 `url` 字段做站内导航
- **新建生成脚本**：`scripts/generate_article_pages.py` — 从 articles.json 生成/重新生成所有文章静态页，含 ISO 8601 日期处理

**项目记事本**
- CLAUDE.md 更新：文件结构、待提交、GEO 待办、对话记录、文章静态化架构说明

### 文件变更
```
新增: frontend/articles/001–006.html  (6 篇静态文章)
      frontend/llms.txt
      scripts/generate_article_pages.py

修改: frontend/*.html ×11             (BreadcrumbList / H1 / preload / noindex / 跳转)
      frontend/articles.json           (updated_at)
      frontend/sitemap.xml             (+6 篇, 17 条总)
      frontend/robots.txt              (+3 UA, -1 UA)
      frontend/blog.html               (BlogPosting Schema + localUrl 跳转)
      deploy.sh                        (bump_sitemap_lastmod)
      CLAUDE.md

删除: frontend/assets/og-cover.jpg
```

### Debug / 踩坑
| 现象 | 原因 | 解决方式 |
|---|---|---|
| 批量 BreadcrumbList 脚本给 writing-camp.html 多加了第二个 BreadcrumbList | 旧手动版和批量版共存 | 手动删旧版 4 行，保留新版 |
| 5 个服务详情页都有双重 BreadcrumbList | 此前已有手动版 "面包屑" + 本轮批量 "BreadcrumbList" | Python regex 批量清理旧 "面包屑" 块 |
| articles.json 的 `url` 被改为相对路径，但服务器 sync_articles.py 会覆盖 | 该文件由 cron 在服务器端生成 | url 恢复为微信占位链接，JS 改用 `id` 字段构造静态页路径 |
| `og:url` 含 `#writing-camp` 片段与 canonical 不一致 | og:url 不应带 hash fragment | 去掉 hash，统一 https://tuce.asia/meiben |

### 遗留 / 下次继续
- [ ] 提交所有改动 + 部署到服务器
- [ ] 提交 sitemap 给百度/Bing/Google Search Console
- [ ] 确认 `8d888b...txt` 和 `bdd3055...txt` 归属（360/搜狗站长平台）
- [ ] 同步线上 nginx 配置回 `nginx.conf.example`

