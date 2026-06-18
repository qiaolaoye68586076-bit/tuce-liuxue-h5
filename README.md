# 途策留学 · H5 落地页

一个纯 HTML/CSS/JS 的移动端（H5）单页长滚动营销落地页，零构建、零依赖。
设计参考三士渡（stoooges.com）的高端极简风格，配色为「深森林绿 + 暖金」。

## 目录结构

> 2026-06-18 工程化重构：前后端分离，前端整体收入 `frontend/`。

```
tuce-liuxue-h5/
├── frontend/             # ★ 前端整体 = 部署 web 根目录
│   ├── index.html        # 首页（+ services/teachers/cases/blog… 多页面）
│   ├── css/style.css     # 全站样式（移动优先 + 响应式）
│   ├── js/main.js        # 导航 / 滚动动画 / 数字滚动 / 表单
│   ├── js/experience.js  # GSAP 动效（vendor/ 内为第三方库）
│   ├── assets/ images/   # 图片 / logo / 二维码 / 封面
│   ├── articles.json     # 博客数据（index/blog 通过 fetch 读取）
│   └── robots.txt sitemap.xml   # SEO（须随 frontend/ 暴露在域名根）
├── backend/              # Flask API 预留（app.py / leads.db）
├── scripts/             # 独立 Python 脚本（scrape_reference.py / 后续 sync_articles.py）
├── archive/             # 归档：legacy/ 旧版 + site/ Astro 探索项目
├── reference/            # 竞品参考（stoooges）
└── *.md                 # CLAUDE.md / LOG.md / GEO 文档等
```

## 本地预览

进入 `frontend/` 起一个本地静态服务器（推荐，`fetch('articles.json')` 在 `file://` 下会被浏览器拦截）：

```bash
cd tuce-liuxue-h5/frontend
python3 -m http.server 8080
# 浏览器打开 http://localhost:8080
```

手机预览：用手机访问电脑局域网 IP（如 `http://192.168.x.x:8080`），
或在 Chrome 开发者工具中切换到移动设备视图。

## 页面分区

导航 → Hero → 核心数据 → 服务（6 项）→ 为什么选途策 → 申请流程 →
师资 → Offer 墙 → 留资表单 → 页脚（二维码/联系方式）→ 移动端常驻 CTA。

## 留资表单

- 校验：姓名、咨询方向、电话（11 位手机号）为必填，需勾选协议。
- 提交后**始终先写入浏览器 `localStorage`**（key：`tuce_leads`）做本地留底。
- 对接后端：编辑 `frontend/js/main.js` 顶部的 `LEAD_ENDPOINT`，填入接收 POST JSON 的接口地址即可。
  留空时为占位模式，模拟提交成功。

  ```js
  var LEAD_ENDPOINT = 'https://api.tuce.com/lead';  // 改成你的接口
  ```

  提交的字段：`uname, type, phone, wechat, city, school, more, ts, source`。

## 待替换的占位内容（TODO）

- [ ] 真实数据：成立年限、Offer 数、导师数、满意度（`index.html` 的 `.stats`）
- [ ] 联系电话 / 邮箱 / ICP 备案号（页脚）
- [ ] 微信二维码图片（页脚 `.qr`，放入 `assets/` 后替换为 `<img>`）
- [ ] 用户协议与隐私政策正式链接（`#policyLink`）
- [ ] 师资真实头像与院校（`.mentors`）
- [ ] 留资接口 `LEAD_ENDPOINT`

## 部署

前端为纯静态站点，无需 Node 环境，可托管到对象存储（OSS/COS）、Nginx、Vercel/Netlify、
GitHub Pages，或微信公众号菜单跳转的网页。后端（`backend/`）就绪后另起 Flask 提供 `/api/*`。

### ⚠️ 第一原则：web 根目录 = `frontend/`

部署时**必须把 `frontend/` 设为网站根目录**，让 `frontend/robots.txt` 对外正好是 `https://域名/robots.txt`。
若误把仓库根当 web root，爬虫在 `/robots.txt` 找不到文件 → 直接影响百度收录与 GEO（AI 可见度）。

- **Nginx**：`root /var/www/tuce/frontend;`
- **OSS/COS**：只上传 `frontend/` 内的文件到 bucket 根，不要带 `frontend/` 这层目录
- **Vercel/Netlify**：把 *Output / Publish Directory* 设为 `frontend`

### 上线检查清单

- [ ] **SSL 证书**（阿里云 HTTPS）——上线前必须，是百度收录/GEO 的前置条件
- [ ] 访问 `https://域名/robots.txt` 与 `/sitemap.xml` 能直接打开（验证 web root 正确）
- [ ] 页脚 **ICP 备案号**替换占位 `沪ICP备 0000000 号`
- [ ] `LEAD_ENDPOINT` 已配置真实接口，表单能落库（否则只写本地 `localStorage`）
- [ ] 页脚联系方式（电话/邮箱/地址）已替换占位
- [ ] 上线后向**百度站长平台**提交 `sitemap.xml`

### 前后端同源部署（后端就绪后）

Flask 启动后用反向代理把动态接口和静态站拼到同一域名：

```nginx
server {
    server_name tuce.example.com;
    root /var/www/tuce/frontend;        # 静态站根 = frontend/
    location /api/ { proxy_pass http://127.0.0.1:5000; }  # 表单等动态接口走 Flask
    location /     { try_files $uri $uri/ =404; }
}
```
