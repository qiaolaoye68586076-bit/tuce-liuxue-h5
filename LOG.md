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
