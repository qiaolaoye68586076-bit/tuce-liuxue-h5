# scripts/ — 公众号文章同步

把微信公众号已发布的图文，定时拉成前端消费的 `frontend/articles.json`，
让首页「留学洞察」预览（最新 3 篇）和 `blog.html` 列表自动更新，无需手改 JSON。

- `sync_articles.py` — 同步脚本（纯标准库，兼容生产的 Python 3.6.8）
- `generate_article_pages.py` — 根据 `articles.json` 生成静态文章页、sitemap.xml 和 llms.txt
- `sync_articles.env.example` — 环境变量模板（复制为 `.env` 填密钥，**勿提交**）
- `article_overrides.json` — 人工微调表（分类 / 置顶 / 隐藏；API 无这些概念）
- `scrape_reference.py` — 旧的竞品参考抓取脚本（与本功能无关）

数据流：

```
公众号 API ──► sync_articles.py ──► <web根>/articles.json
                                  ├─► <web根>/articles/*.html
                                  ├─► <web根>/sitemap.xml
                                  ├─► <web根>/llms.txt
                                  └─► <web根>/assets/insights/*.jpg
                                         │
              index.html / blog.html  ◄──┘  fetch('articles.json')
```

---

## ⚠️ 两个硬前提（不满足就跑不通）

1. **服务器公网出口 IP 必须加入白名单**
   公众号后台 → 设置与开发 → 基本配置 → IP 白名单，填服务器公网 IP
   （阿里云 ECS 控制台可查，本项目是 `121.43.101.155`）。
   没加会报 `errcode 40164`。

2. **账号要有接口权限**
   `素材管理` 或 `发布` 接口仅对**已认证**的服务号 / 订阅号开放；
   个人未认证订阅号调不通，会报 `errcode 48001`。

> AppSecret 是敏感凭据：只放服务器上的 `.env`（`chmod 600`），
> 不写进代码、不进 git。本项目 `.gitignore` 已忽略 `.env` 和 token 缓存。

---

## 本地试跑（dry-run，不写文件）

```bash
cd <项目根>
cp scripts/sync_articles.env.example scripts/.env   # 填 WX_APPID / WX_APPSECRET
set -a; source scripts/.env; set +a
python3 scripts/sync_articles.py --dry-run -v        # 只打印拉到的文章，不落盘
```

> 本地若公网 IP 不在白名单，dry-run 也会 40164 失败——这是正常的，正式跑在服务器上。
> 去掉 `--dry-run` 才会真正写 `frontend/articles.json` 并下载封面。

---

## 服务器部署（在 ECS 上）

脚本不在 `deploy.sh` 的同步范围内（deploy 只传 `frontend/`），所以在服务器上
单独放一份脚本，cron 直接写线上站点目录。

```bash
# 1. 把脚本放到服务器（与 /var/www/tuce 分开）
mkdir -p /opt/tuce/scripts
# 将 sync_articles.py、generate_article_pages.py、
# article_overrides.json 放到 /opt/tuce/scripts/

# 2. 配密钥
cd /opt/tuce/scripts
cp sync_articles.env.example .env
vi .env        # 填 WX_APPID / WX_APPSECRET；TUCE_WEB_ROOT=/var/www/tuce
chmod 600 .env

# 3. 手动跑一次验证（会写 /var/www/tuce/articles.json）
set -a; source .env; set +a
/usr/bin/python3 sync_articles.py -v
curl -s http://127.0.0.1/articles.json | head     # 确认线上已更新

# 4. 配 cron：每 3 天 03:30 同步一次（公众号更新不频繁，无需更密）
crontab -e
# 加入（注意用绝对路径；日志留档便于排查）：
30 3 */3 * * cd /opt/tuce/scripts && set -a && . ./.env && set +a && /usr/bin/python3 sync_articles.py >> /var/log/tuce-sync.log 2>&1
```

---

## 与 deploy.sh 的关系（重要）

`deploy.sh` 用 `rsync --delete` 同步 `frontend/`，会**覆盖/删除**服务器上同步生成的内容。
为此 `deploy.sh` 已加 `--exclude`，保护以下内容不被部署清掉：

- `/articles.json`（脚本生成的真实数据，仓库里那份只是占位种子）
- `/articles/`（脚本生成的静态文章页；文章 ID 以线上数据为准）
- `/assets/insights/`（脚本下载的封面图）
- `/sitemap.xml`（脚本按线上文章数据生成）
- `/llms.txt`（脚本按线上文章数据生成）

所以：**部署前端照常 `./deploy.sh`，文章数据各走各的，互不打架。**
仓库里的 `frontend/articles.json` 保留为占位/兜底，首次同步后即被服务器上的真实数据取代。

---

## 字段映射 & 人工微调

| articles.json 字段 | 来源 | 说明 |
|---|---|---|
| `title` / `url` | 公众号图文 | 原样 |
| `digest` | 摘要，缺失时取正文前 60 字 | 可在 overrides 覆盖 |
| `cover_url` | 封面下载到 `assets/insights/` | 失败则留空，前端用 SVG 占位 |
| `publish_time` | 图文**发表时间**（tikhub `create_time`，预约发表=计划发布时刻；缺失才退 `update_time`） | `YYYY-MM-DD` |
| `category` | **标题关键词推断** | 命中不到归 `WX_DEFAULT_CATEGORY`；可在 overrides 覆盖 |
| `pinned` | 默认全 false | 每轮全量重算：overrides 显式置顶优先，否则自动顶**最新发表**一篇（增量同步也会随新文前移，不卡旧文） |

分类/置顶/隐藏改 `scripts/article_overrides.json`（按文章 URL），下次同步自动生效。

---

## 排查

| 现象 | 原因 / 处理 |
|---|---|
| `errcode 40164` | 服务器 IP 不在白名单（见上） |
| `errcode 48001` | 账号无接口权限（需认证） |
| `errcode 40001` | AppSecret 错 / 失效（删 `scripts/.wx_token_cache.json` 重试） |
| `errcode 45009` | 当天接口调用超限，降低 cron 频率 |
| 拉到 0 篇 | 账号还没发过图文，或试试 `WX_ARTICLE_SOURCE=freepublish` |
| 卡片封面是占位图 | 封面下载失败（防盗链/网络）；功能不受影响 |
