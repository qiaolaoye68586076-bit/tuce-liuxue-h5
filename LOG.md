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
| 1 | `footer` | ICP 备案号是占位 `沪ICP备 0000000 号` | ⏳ 待客户提供 |
| 2 | `#stats` 卡片 | 4 张图是 "Image placeholder"，未接真图 | ⏳ 待素材 |
| 3 | `#mentors` | 导师信息（哈佛/耶鲁等）为示例，未经授权 | ⏳ 待客户确认 |
| 4 | `#stories` | W/L/C 同学案例为虚构占位 | ⏳ 待真实授权案例 |
| 5 | `js/main.js:9` | `LEAD_ENDPOINT` 留空，表单提交走本地模拟 | ⏳ 待后端接口 |
| 6 | `assets/qr-official.png` | 公众号二维码缺图，有 CSS 兜底但不显示内容 | ⏳ 待素材 |

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
