# 途策留学 · H5 官网

多页面静态官网，正式上线：**https://tuce.asia**
（Let's Encrypt HTTPS / HTTP→HTTPS 强跳 / ICP 备案 `沪ICP备2026025218号-2`）

前端零构建、零依赖（纯 HTML/CSS/JS）；后端是一个零第三方依赖的留资 API（Python 标准库）。
设计风格：Collegiate Editorial Luxury — 深森林绿 + 暖金 + 米纸，Fraunces / 思源宋体。

## 目录结构

```
tuce-liuxue-h5/
├── frontend/              # ★ 前端整体 = 部署 web 根目录
│   ├── index.html         # 首页
│   ├── services.html      # 美本专题 + 其他服务
│   ├── teachers.html      # 师资团队
│   ├── cases.html         # 成功案例（真实化名案例复盘）
│   ├── transfer.html      # 转学专题
│   ├── uk-eu.html         # 多国联申（英/欧/加/港）
│   ├── meiben.html        # 美本训练营
│   ├── writing-camp.html  # 文书训练营
│   ├── graduate.html      # 研究生申请
│   ├── blog.html          # 留学洞察列表
│   ├── css/style.css      # 全站样式；css/timeline.css 申请流程时间轴
│   ├── js/main.js         # 导航 / 滚动动画 / 表单（LEAD_ENDPOINT 见下）
│   ├── js/experience.js + js/vendor/  # GSAP 动效（vendor/globe.js 是手工 esbuild 产物，无构建脚本，改源码需同步手改 bundle）
│   ├── assets/ images/    # 图片、logo、二维码
│   ├── articles.json      # 博客数据（index/blog 通过 fetch 读取；仓库里这份是占位种子，服务器上由同步脚本覆盖为真实数据）
│   └── robots.txt sitemap.xml  # SEO（必须随 frontend/ 暴露在域名根）
├── backend/                # 留资 API：Python 标准库 http.server + sqlite3（零第三方依赖）
│   ├── app.py              # POST /api/lead · GET /api/leads（导出）· GET /api/health
│   └── leads.db             # 运行时生成，已 gitignore
├── scripts/                 # 公众号文章同步（TikHub API，见 scripts/README.md）
├── docs/                    # DOMAIN-CUTOVER.md 等项目级文档
├── archive/                  # 归档：legacy/ 旧版 + site/ Astro 探索项目
├── reference/                 # 竞品参考（stoooges）
├── deploy.sh                  # 部署脚本（rsync frontend/ → 服务器）
├── nginx.conf.example          # 参考配置（含 /api/ 反代、.html 后缀隐藏 301）
└── CLAUDE.md / LOG.md            # 项目记事本 / 开发日志（每次改动的详细记录）
```

> ⚠️ 前端资源引用均为「无前导斜杠」相对路径，HTML 与 css/js/assets 保持同级。部署时必须让 `frontend/` 作为 web 根，否则 `robots.txt`/`sitemap.xml` 不在域名根，AI 爬虫读不到，直接影响 GEO。

## 本地预览

```bash
cd frontend
python3 -m http.server 8080
# 浏览器打开 http://localhost:8080
```

用本地静态服务器而非直接双击打开 HTML，否则 `fetch('articles.json')` 会被浏览器的 `file://` 限制拦截。

## 留资表单（CTA）

`frontend/js/main.js` 第 9 行：

```js
var LEAD_ENDPOINT = '/api/lead';   // 同域 nginx 反代到 backend/app.py（127.0.0.1:5000）
```

- 提交前**始终先写入浏览器 `localStorage`**（key：`tuce_leads`）做本地留底，接口失败也不丢数据。
- 后端（`backend/app.py`）零第三方依赖：`http.server` + `sqlite3`，因为生产服务器是 Python 3.6.8 装不了 Flask 3.x。字段：`uname / type / phone / wechat / city / school / more`，手机号服务端复校验。
- 可选环境变量 `SERVERCHAN_KEY` / `PUSHPLUS_TOKEN` 配置后会把新留资推送到微信。
- 详见 `backend/app.py` 顶部 docstring（`backend/README.md` 目前仍按旧版 Flask + gunicorn 方案写的，与当前实现不符，见 CLAUDE.md 待办）。

## 公众号文章同步

`scripts/sync_articles.py` 定时把公众号已发布图文拉成 `frontend/articles.json`，供首页「留学洞察」与 `blog.html` 消费。官方公众号 API 抓不到这个号的文章，改走 TikHub API。服务器 `/opt/tuce/scripts` 下有独立一份，cron 增量同步。用法与排查见 `scripts/README.md`。

## 部署

纯静态前端可托管到任意静态服务；本项目实际用阿里云 ECS + Nginx。

### 第一原则：web 根目录 = `frontend/`

- **Nginx**：`root /var/www/tuce/frontend;`
- 若误把仓库根当 web root，`robots.txt`/`sitemap.xml` 找不到，直接影响百度收录与 GEO

```bash
./deploy.sh            # rsync frontend/ → 服务器，--exclude 保护 articles.json 与 assets/insights/（脚本生成内容不被覆盖）
./deploy.sh --dry-run  # 预演，不实际同步
```

`deploy.sh` 只同步 `frontend/`；`backend/` 与 `scripts/` 需要另外手动部署/更新（无自动化脚本，见 CLAUDE.md 待办）。

### 线上状态（2026-07-08 起）

- HTTPS：Let's Encrypt（`certbot --nginx`），有效期至 2026-10-06，自动续期已装
- ICP 备案：`沪ICP备2026025218号-2`，10 页页脚已替换真实备案号 + 工信部链接
- nginx `server_name`：`tuce.asia www.tuce.asia`

## GEO / SEO

- `robots.txt` 显式允许百度 / 360 / 搜狗 / 神马 / 字节 / DeepSeek / GPTBot / Claude 等 20+ 爬虫
- `sitemap.xml` 覆盖全部页面；FAQ JSON-LD、EducationalOrganization schema、cases.html 的 ItemList/Review schema 均已接入
- 待办：向百度/Bing/Google 站长平台正式提交 sitemap；知乎机构号等渠道内容

## 项目文档索引

| 文档 | 用途 |
|---|---|
| `CLAUDE.md` | 项目记事本：模块状态、待办事项、对话历史（每次对话结束前更新） |
| `LOG.md` | 开发日志：每次改动的详细记录 + 踩坑表 |
| `docs/DOMAIN-CUTOVER.md` | 域名切换 / 备案上线验收清单 |
| `DESIGN-BRIEF.md` / `design-assets-needed.md` | 给设计师的素材与文案需求清单 |
| `backend/README.md` | 后端接口说明（⚠️ 待更新，见上） |
| `scripts/README.md` | 公众号文章同步脚本使用说明 |
