# 途策留学 · H5 落地页

一个纯 HTML/CSS/JS 的移动端（H5）单页长滚动营销落地页，零构建、零依赖。
设计参考三士渡（stoooges.com）的高端极简风格，配色为「深森林绿 + 暖金」。

## 目录结构

```
tuce-liuxue-h5/
├── index.html        # 全部页面结构（单页）
├── css/style.css     # 样式（移动优先 + 响应式）
├── js/main.js        # 导航 / 滚动动画 / 数字滚动 / 表单
├── assets/           # 预留图片/二维码目录
└── README.md
```

## 本地预览

直接双击 `index.html` 即可，或起一个本地静态服务器（推荐，避免某些浏览器限制）：

```bash
cd tuce-liuxue-h5
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
- 对接后端：编辑 `js/main.js` 顶部的 `LEAD_ENDPOINT`，填入接收 POST JSON 的接口地址即可。
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

纯静态站点，可直接托管到：对象存储（COS/OSS）、Nginx、Vercel/Netlify、
GitHub Pages，或微信公众号自定义菜单跳转的网页。无需 Node 环境。
