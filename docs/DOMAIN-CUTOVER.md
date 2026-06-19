# 域名切换 / 备案上线验收清单（DOMAIN-CUTOVER）

> 途策留学 H5 官网 · 域名 `tuce.asia` 硬编码盘点 + 备案当天验收清单

---

## 1. 文档说明

**用途**
本文档用于 **ICP 备案完成、DNS 解析生效后**，作为「域名切换 / 上线验收清单」逐项核对。
当前网站通过公网 IP `121.43.101.155` 访问；备案前**不要**把站内的 `canonical` / `og:url` / `sitemap` 等绝对 URL 改成 IP（会污染未来域名的 SEO/GEO 权重）。所以这些位置目前**保持** `https://tuce.asia`，备案 + DNS 解析生效后会「自动正确」，绝大多数无需改动。

**适用前提**
备案下来的域名为 **`tuce.asia`**（所有权已在手）。在此前提下，第 2 节列出的 A–F 类硬编码**无需逐个替换**，只需按第 4 节验收清单确认它们在真实域名下生效。

**例外说明**
如果备案主体最终要求**更换域名**（最终域名不是 `tuce.asia`），则本文档第 2 节的 A–F 分类清单可直接当作**全站替换清单**使用，按第 5 节的 `find` / `sed` 批量替换方案执行即可。

**生成信息**
- 生成时间：2026-06-19
- 对应 git commit：`f2b582a`（`f2b582a1f710f096dde88d53b1d3b570f6143def`）
- 盘点命令：`grep -rn "tuce\.asia" frontend/`（行号以该 commit 为准；新增页面后需按第 6 节更新）

---

## 2. 当前域名硬编码盘点（A–F 分类）

> 范围：`frontend/`（线上部署根目录）。共 **81 处** 引用，全部为绝对 URL `https://tuce.asia`，分布在 11 个 HTML 页面 + `robots.txt` + `sitemap.xml`。
> 11 个 HTML 页面：`index` / `services` / `meiben` / `writing-camp` / `graduate` / `transfer` / `uk-eu` / `single-service` / `teachers` / `cases` / `blog`。

### A. canonical（规范链接）— 11 处

`<link rel="canonical">` 告诉搜索引擎该页面的「主版本」URL，避免重复内容分散权重。每页 1 个。

| 文件 | 行号 | 当前值 |
|---|---|---|
| frontend/index.html | 14 | `https://tuce.asia/` |
| frontend/services.html | 13 | `https://tuce.asia/services.html` |
| frontend/meiben.html | 13 | `https://tuce.asia/meiben.html` |
| frontend/writing-camp.html | 13 | `https://tuce.asia/writing-camp.html` |
| frontend/graduate.html | 13 | `https://tuce.asia/graduate.html` |
| frontend/transfer.html | 13 | `https://tuce.asia/transfer.html` |
| frontend/uk-eu.html | 13 | `https://tuce.asia/uk-eu.html` |
| frontend/single-service.html | 13 | `https://tuce.asia/single-service.html` |
| frontend/teachers.html | 13 | `https://tuce.asia/teachers.html` |
| frontend/cases.html | 13 | `https://tuce.asia/cases.html` |
| frontend/blog.html | 14 | `https://tuce.asia/blog.html` |

### B. og:url（Open Graph 页面地址）— 11 处

`<meta property="og:url">` 是社交平台（微信/微博等）分享时识别的页面正规地址。每页 1 个。

| 文件 | 行号 | 当前值 |
|---|---|---|
| frontend/index.html | 25 | `https://tuce.asia/` |
| frontend/services.html | 21 | `https://tuce.asia/services.html` |
| frontend/meiben.html | 21 | `https://tuce.asia/meiben.html` |
| frontend/writing-camp.html | 21 | `https://tuce.asia/writing-camp.html` |
| frontend/graduate.html | 21 | `https://tuce.asia/graduate.html` |
| frontend/transfer.html | 21 | `https://tuce.asia/transfer.html` |
| frontend/uk-eu.html | 21 | `https://tuce.asia/uk-eu.html` |
| frontend/single-service.html | 21 | `https://tuce.asia/single-service.html` |
| frontend/teachers.html | 21 | `https://tuce.asia/teachers.html` |
| frontend/cases.html | 21 | `https://tuce.asia/cases.html` |
| frontend/blog.html | 23 | `https://tuce.asia/blog.html` |

### C. og:image / twitter:image（分享封面图）— 4 处

分享卡片的封面图地址。仅 `index` 与 `blog` 两页有（M2-a 已统一为 `og-cover.jpg`）。

| 文件 | 行号 | 类型 | 当前值 |
|---|---|---|---|
| frontend/index.html | 28 | og:image | `https://tuce.asia/assets/og-cover.jpg` |
| frontend/index.html | 37 | twitter:image | `https://tuce.asia/assets/og-cover.jpg` |
| frontend/blog.html | 26 | og:image | `https://tuce.asia/assets/og-cover.jpg` |
| frontend/blog.html | 32 | twitter:image | `https://tuce.asia/assets/og-cover.jpg` |

> 注：其余 9 个页面当前缺 og:image，已记录为 M2-a 范围外 TODO（未来 GEO 批次处理）；那些页面补图时也会引入新的 `tuce.asia` 绝对 URL，需按第 6 节回填本文档。

### D. JSON-LD 结构化数据 — 42 处

各页 `<script type="application/ld+json">` 的 `@graph` 中的绝对 URL，供搜索引擎/AI 理解站点结构（GEO 关键）。按子类型拆分：

#### D1. 顶层实体 url（WebPage / Organization 的 `"url"`）— 10 处

| 文件 | 行号 | 当前值 |
|---|---|---|
| frontend/index.html | 46 | `https://tuce.asia/` |
| frontend/services.html | 29 | `https://tuce.asia/services.html` |
| frontend/meiben.html | 30 | `https://tuce.asia/meiben.html` |
| frontend/writing-camp.html | 30 | `https://tuce.asia/writing-camp.html` |
| frontend/graduate.html | 30 | `https://tuce.asia/graduate.html` |
| frontend/transfer.html | 30 | `https://tuce.asia/transfer.html` |
| frontend/uk-eu.html | 30 | `https://tuce.asia/uk-eu.html` |
| frontend/single-service.html | 30 | `https://tuce.asia/single-service.html` |
| frontend/cases.html | 30 | `https://tuce.asia/cases.html` |
| frontend/blog.html | 41 | `https://tuce.asia/blog.html` |

> `teachers.html` 无 JSON-LD `url`（该页 JSON-LD 结构较简，仅 A/B 类各 1 处）。

#### D2. logo（Organization 的 `"logo"`）— 2 处

| 文件 | 行号 | 当前值 |
|---|---|---|
| frontend/index.html | 47 | `https://tuce.asia/assets/logo.webp` |
| frontend/blog.html | 47 | `https://tuce.asia/assets/logo.webp` |

#### D3. image（实体 `"image"`）— 1 处

| 文件 | 行号 | 当前值 |
|---|---|---|
| frontend/index.html | 48 | `https://tuce.asia/assets/og-cover.jpg` |

#### D4. publisher 根域名 url（嵌套 Organization 的 `"url"`，无路径）— 8 处

值统一为 `https://tuce.asia`（注意：无尾斜杠、无路径）。

| 文件 | 行号 |
|---|---|
| frontend/meiben.html | 37 |
| frontend/writing-camp.html | 37 |
| frontend/graduate.html | 37 |
| frontend/transfer.html | 37 |
| frontend/uk-eu.html | 37 |
| frontend/single-service.html | 37 |
| frontend/cases.html | 46 |
| frontend/blog.html | 48 |

#### D5. BreadcrumbList 面包屑 item — 18 处（6 页 × 3 级）

每个详情页 3 条面包屑（首页 / 服务 / 当前页）。以 **meiben.html 为代表**完整列出，其余 5 页结构与行号完全相同：

```
frontend/meiben.html:48  {"position": 1, "name": "首页",  "item": "https://tuce.asia/"}
frontend/meiben.html:49  {"position": 2, "name": "服务",  "item": "https://tuce.asia/services.html"}
frontend/meiben.html:50  {"position": 3, "name": "美国本科申请", "item": "https://tuce.asia/meiben.html"}
```

同结构（均为 **行 48 / 49 / 50**，仅第 3 级 name 与 item 路径随页面不同）的页面：

| 文件 | 行号 | 第 3 级 item |
|---|---|---|
| frontend/meiben.html | 48,49,50 | `https://tuce.asia/meiben.html` |
| frontend/writing-camp.html | 48,49,50 | `https://tuce.asia/writing-camp.html` |
| frontend/graduate.html | 48,49,50 | `https://tuce.asia/graduate.html` |
| frontend/transfer.html | 48,49,50 | `https://tuce.asia/transfer.html` |
| frontend/uk-eu.html | 48,49,50 | `https://tuce.asia/uk-eu.html` |
| frontend/single-service.html | 48,49,50 | `https://tuce.asia/single-service.html` |

> 每行的第 1 级（`https://tuce.asia/`）与第 2 级（`https://tuce.asia/services.html`）在 6 页中完全相同。

#### D6. ItemList 案例锚点（cases.html 专有）— 3 处

| 文件 | 行号 | 当前值 |
|---|---|---|
| frontend/cases.html | 33 | `https://tuce.asia/cases.html#case-w`（W同学 → 宾夕法尼亚大学） |
| frontend/cases.html | 34 | `https://tuce.asia/cases.html#case-l`（L同学 → 芝加哥大学） |
| frontend/cases.html | 35 | `https://tuce.asia/cases.html#case-c`（C同学 → 康奈尔大学） |

> D 类小计：10 + 2 + 1 + 8 + 18 + 3 = **42 处**。

### E. robots.txt — 2 处

| 文件 | 行号 | 当前值 | 说明 |
|---|---|---|---|
| frontend/robots.txt | 2 | `# https://tuce.asia` | 文件头注释 |
| frontend/robots.txt | 139 | `Sitemap: https://tuce.asia/sitemap.xml` | Sitemap 声明，**必须**为绝对 URL |

### F. sitemap.xml — 11 处

`<loc>` 标签，每个页面 1 条，必须为绝对 URL。

| 文件 | 行号 | 当前值 |
|---|---|---|
| frontend/sitemap.xml | 6 | `https://tuce.asia/` |
| frontend/sitemap.xml | 14 | `https://tuce.asia/services.html` |
| frontend/sitemap.xml | 22 | `https://tuce.asia/meiben.html` |
| frontend/sitemap.xml | 30 | `https://tuce.asia/writing-camp.html` |
| frontend/sitemap.xml | 38 | `https://tuce.asia/graduate.html` |
| frontend/sitemap.xml | 46 | `https://tuce.asia/transfer.html` |
| frontend/sitemap.xml | 54 | `https://tuce.asia/uk-eu.html` |
| frontend/sitemap.xml | 62 | `https://tuce.asia/single-service.html` |
| frontend/sitemap.xml | 70 | `https://tuce.asia/teachers.html` |
| frontend/sitemap.xml | 78 | `https://tuce.asia/cases.html` |
| frontend/sitemap.xml | 86 | `https://tuce.asia/blog.html` |

### 小计

| 类别 | 数量 |
|---|---|
| A. canonical | 11 |
| B. og:url | 11 |
| C. og/twitter image | 4 |
| D. JSON-LD（D1–D6） | 42 |
| E. robots.txt | 2 |
| F. sitemap.xml | 11 |
| **合计（frontend）** | **81** |

> 复核方法：`grep -rn "tuce\.asia" frontend/ | wc -l` 应返回 **81**。如果数字不一致，说明仓库已增减引用，需重新盘点并按第 6 节更新本文档。

---

## 3. 边角项清单

> 不在 A–F「绝对 URL」主清单内，但与域名相关，单独记录。

### 3.1 main.js 的 LEAD_ENDPOINT 注释示例（非切换当天必做）

```
frontend/js/main.js:9   var LEAD_ENDPOINT = '';   // 例如 'https://api.tuce.com/lead'，留空则只存本地
```

- 这是**注释里的示例占位**，且 `LEAD_ENDPOINT` 当前为空字符串、不生效。
- 示例域名写的是 `api.tuce.com`（`.com`，非 `.asia`），未来若启用后端留资 API，需：
  1. 确认实际接口域名（应为 `.asia` 体系，如 `https://api.tuce.asia/lead` 或主域同源路径）；
  2. 把接口地址从硬编码改为配置项 / 构建注入，避免再次写死。
- **触发时机**：后端（`backend/`）开发并上线时，不是域名切换当天。

### 3.2 archive/ 下的旧引用（已归档，不部署）

以下引用**不在线上部署范围**（`archive/` 不随 `frontend/` 上线），切换当天**无需处理**；仅在未来复用这些代码时需注意同步域名：

| 文件 | 性质 |
|---|---|
| archive/site/astro.config.mjs | 归档的 Astro 探索项目（Cloudflare Pages 方案）|
| archive/site/public/sitemap.xml | 同上 |
| archive/site/public/robots.txt | 同上 |
| archive/site/scripts/copy-h5.mjs | 同上 |
| archive/site/src/pages/cases.astro | 同上 |
| archive/site/README.md | 同上（文档）|
| archive/legacy/v2-gilded-route/index.html | 旧版 v2 页面 |

> 已确认 `CLAUDE.md` / `LOG.md` / `articles.json` 等文档与数据文件**无**域名硬编码，无需处理。

---

## 4. 备案当天验收清单（主用途）

> 前提：ICP 备案审核通过。按时间顺序执行，逐项打勾。命令中的 `121.43.101.155` 为当前 ECS 公网 IP。

### 4.1 DNS 解析
- [ ] 阿里云 DNS 控制台为 `tuce.asia` 添加 **A 记录**，主机记录 `@`，记录值 `121.43.101.155`
- [ ] （可选）添加 `www` 的 A 记录或 CNAME，指向同一 IP / 主域（若计划启用 www）
- [ ] TTL 建议初期设为 `600`（10 分钟），便于解析有误时快速调整；上线稳定后可调大（如 3600）

### 4.2 解析生效验证
- [ ] `dig tuce.asia +short` 返回 `121.43.101.155`（解析可能需数分钟到数小时全网生效）
- [ ] `dig www.tuce.asia +short` 正确（若配了 www）

### 4.3 HTTP 访问验证（HTTPS 之前）
- [ ] `curl -I http://tuce.asia` 返回 `200`（或后续配好跳转后返回 `301`）
- [ ] `curl -s http://tuce.asia | grep -i "<title>"` 内容为首页标题，确认指向正确站点

### 4.4 HTTPS 证书签发
- [ ] 在 ECS 上为 `tuce.asia` 签发 Let's Encrypt 证书。参考命令模板（**具体参数以 certbot 官方文档为准，按实际 nginx 环境调整**）：
  ```bash
  # 安装（Alibaba Cloud Linux 3 / dnf 系）
  sudo dnf install -y certbot python3-certbot-nginx
  # 签发 + 自动写入 nginx 配置（如启用 www 再加 -d www.tuce.asia）
  sudo certbot --nginx -d tuce.asia
  # 验证自动续期
  sudo certbot renew --dry-run
  ```

### 4.5 HTTPS 访问验证
- [ ] `curl -I https://tuce.asia` 返回 `200`
- [ ] 浏览器访问 `https://tuce.asia` 显示安全锁，无证书告警

### 4.6 HTTP → HTTPS 跳转
- [ ] `curl -I http://tuce.asia` 返回 `301`，`Location` 指向 `https://tuce.asia/`

### 4.7 11 个页面逐个 200 验证
- [ ] 逐个验证 HTTP 状态码为 `200`（首页用 `/`，其余带 `.html`，与 sitemap.xml 风格一致）：
  ```bash
  for path in / /services.html /meiben.html /writing-camp.html /graduate.html /transfer.html /uk-eu.html /single-service.html /teachers.html /cases.html /blog.html; do
    echo -n "https://tuce.asia${path}: "
    curl -s -o /dev/null -w "%{http_code}\n" "https://tuce.asia${path}"
  done
  ```

### 4.8 SEO 元数据生效抽查
- [ ] 抽查 canonical / og:url 指向（首页用 `/`，其余带 `.html`）：
  ```bash
  for url in https://tuce.asia/ https://tuce.asia/services.html https://tuce.asia/blog.html; do
    echo "=== $url ==="
    curl -s "$url" | grep -E 'rel="canonical"|og:url'
  done
  ```
  确认输出的 canonical / og:url 均指向 `https://tuce.asia/...` 正确路径。
- [ ] `curl -s https://tuce.asia/sitemap.xml | head` 可访问，`<loc>` 指向 `https://tuce.asia/...`
- [ ] `curl -s https://tuce.asia/robots.txt | grep -i sitemap` 返回 `Sitemap: https://tuce.asia/sitemap.xml`

### 4.9 分享封面抓取测试
- [ ] 用微信「公众平台调试工具」或在线 OG 解析器（如 opengraph.xyz）测试 `https://tuce.asia/` 与 `https://tuce.asia/blog.html`，确认 og:image（`og-cover.jpg`）能正确抓取显示

### 4.10 搜索引擎提交
- [ ] 百度站长平台：验证站点所有权 + 提交 `https://tuce.asia/sitemap.xml`
- [ ] Bing Webmaster Tools：提交 sitemap
- [ ] Google Search Console：提交 sitemap（GEO/海外可见度）

### 4.11 nginx 配置收尾
- [ ] 将站点 `server_name` 从 `_` 改为 `tuce.asia`（如启用 www 则 `tuce.asia www.tuce.asia`），**顺手消除 M1 部署演练时遗留的 `conflicting server name "_"` 警告**
- [ ] 远端 `nginx -t` 通过后 reload（可通过 `./deploy.sh` 触发，或手动 `sudo systemctl reload nginx`）
- [ ] 把线上最终 nginx 配置同步回仓库 `nginx.conf.example` 并 commit，保持版本控制副本与线上一致

---

## 5. 替换清单备用方案（仅当最终域名 ≠ tuce.asia 时使用）

> 仅在备案主体最终域名**不是** `tuce.asia` 时执行。把下文 `NEW-DOMAIN` 替换为真实新域名（不含协议与尾斜杠，如 `example.com`）。

### 5.1 先定位所有受影响文件
```bash
cd ~/Desktop/留学实习/tuce-liuxue-h5
grep -rln "tuce\.asia" frontend/
```

### 5.2 批量替换（绝对 URL）
```bash
# macOS / BSD sed 用 -i.bak（生成备份）；GNU/Linux sed 同样兼容 -i.bak
find frontend -type f \( -name "*.html" -o -name "*.xml" -o -name "*.txt" \) \
  -exec sed -i.bak 's|https://tuce.asia|https://NEW-DOMAIN|g' {} +
```
> 说明：
> - 纯 macOS 的 `sed -i` 需要显式参数 `sed -i '' '...'`；用 `-i.bak` 可同时兼容 macOS 与 Linux。
> - 上面只覆盖 `*.html / *.xml / *.txt`，**不含** `js/main.js`（其内只是 `.com` 注释示例，按第 3.1 节单独处理）。

### 5.3 验证零残留
```bash
grep -rn "tuce\.asia" frontend/        # 应无输出
```

### 5.4 清理备份文件
```bash
find frontend -name "*.bak" -delete
```

### 5.5 部署前演练 + 部署
```bash
./deploy.sh -n -v     # 看 itemize 范围，确认改动文件数符合预期（见下方推导）
./deploy.sh           # 确认无误后正式部署（触发远端 nginx reload）
```

> **预期变更文件数 = 13**，推导：`11 个 HTML + robots.txt + sitemap.xml = 13`。
> 说明：A–F 类引用共 81 处，但散落在这 13 个文件内；`sed` 按文件改，itemize 显示的是**文件数**而非引用数。M2-b 给 sitemap.xml 新增的 blog `<loc>` 仍在 sitemap.xml 同一文件内，**不增加文件数**，预期仍为 13。

---

## 6. 维护说明

**本文档需在以下情况更新（行号会变，需重新 grep 校准）：**
- 新增页面：会增加对应的 canonical / og:url / sitemap `<loc>` / JSON-LD url
- 现有页面新增带绝对 URL 的 JSON-LD（如补全 9 个页面缺失的 og:image，见第 2 节 C 注）
- 修改 `robots.txt` 的 Sitemap 声明或 `sitemap.xml` 的 `<loc>` 列表

**更新方法：** 重跑 `grep -rn "tuce\.asia" frontend/`，对照第 2 节各表更新文件/行号/数量，并刷新第 1 节的「生成时间」与「对应 git commit」。

**长期目标（未来重构候选，不在本次范围）：**
把绝对域名抽取为模板变量 / 构建时注入（如 Astro、Eleventy 等静态站点生成器的 `site` 配置），从源头消除散落各页的硬编码，未来换域名只改一处。
