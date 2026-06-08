# 途策留学官网（2026 GEO 改造版）

按 2026 GEO（生成式引擎优化）规则改造的**多页**留学官网，面向中文 AI 引擎（豆包/Kimi/
DeepSeek/百度）与英文引擎（ChatGPT/Perplexity/Gemini/Claude）的检索与引用。

采用**轻量 Python 静态构建**（Jinja2 + YAML）："公共部件 + 内容数据 + 模板"
组装为纯静态 HTML，产物在 `dist/`，可直接托管到国内云 OSS+CDN（备案后）。
配色沿用「深森林绿 #14342B + 暖金」。

## 目录结构

```
tuce-liuxue-h5/
├── build.py                # 构建脚本（“中央厨房”）
├── requirements.txt        # 依赖：Jinja2 + PyYAML
├── site/
│   ├── data/               # 内容数据（单一数据源）
│   │   ├── site.yaml       #   全局：品牌/联系/导航/组织 schema
│   │   ├── services.yaml   #   5 个服务
│   │   ├── cases.yaml      #   成功案例（⚠️ 占位，待真实授权）
│   │   ├── team.yaml       #   师资团队（⚠️ 姓名待填）
│   │   ├── faq.yaml        #   常见问题
│   │   └── blog.yaml       #   升学资讯（待填）
│   ├── templates/          # Jinja2 模板（base + 各页型 + partials）
│   └── static/             # robots.txt / llms.txt（原样拷贝到 dist）
├── css/style.css           # 原有样式（保留）
├── css/pages.css           # 多页内页样式
├── js/main.js              # 交互/表单
├── assets/                 # 图片/二维码
└── dist/                   # 构建产物（git 忽略，运行构建生成）
```

## 构建与预览

```bash
python3 -m pip install -r requirements.txt
python3 build.py            # 构建到 dist/
python3 build.py --serve    # 构建并本地预览 http://localhost:8000
```

## 页面（19 个 URL）

首页 `/` · 关于 `/about/` · 服务总览 `/services/` + 5 个子页 ·
案例总览 `/cases/` + 案例子页 · 团队 `/team/` + 顾问子页 ·
常见问题 `/faq/` · 升学资讯 `/blog/`。
每页自动生成对应 JSON-LD（Organization / Service / HowTo / FAQPage /
Review / ItemList / BreadcrumbList）、OG 标签、面包屑、`sitemap.xml`。

## 改内容怎么改

- 改导航/页脚/品牌/联系方式 → `site/data/site.yaml`（改一处，全站更新）
- 加/改服务、案例、顾问、FAQ → 对应 `site/data/*.yaml`
- 改版式 → `site/templates/`、`css/pages.css`
- 改完跑 `python3 build.py` 重新生成

## 待替换的真实数据（TODO，标记为「【待填】/【待核实】」）

- [ ] `site.yaml`：成立年份、地址、电话、邮箱、ICP 备案号、社媒链接
- [ ] `cases.yaml`：3–5 个真实且授权的脱敏案例（背景/标化/院校/策略/感言）
- [ ] `team.yaml`：顾问真实姓名、从业年限、案例数
- [ ] `faq.yaml`：收费区间口径
- [ ] `assets/qr-official.png`：公众号二维码（当前为空文件）
- [ ] 留资接口 `LEAD_ENDPOINT`（`js/main.js`）
- [ ] 用户协议与隐私政策正式文本

## 留资表单

校验姓名/方向/电话（11 位）必填并勾选协议；提交先写入 `localStorage`（key `tuce_leads`）。
对接后端：改 `js/main.js` 顶部 `LEAD_ENDPOINT` 为接收 POST JSON 的接口。
字段：`uname, type, phone, wechat, city, school, more, ts, source`。

## 部署（备案通过后）

构建产物 `dist/` 为纯静态文件，上传到国内云对象存储 + CDN（阿里云 OSS / 腾讯云 COS），
绑定已备案域名 `tuceeducation.com`。提交百度站长 + Bing 站长 + Google Search Console。
若用 Cloudflare，需在面板关闭 “Block AI Bots / AI Audit”，否则 AI 爬虫会被默认拦截。
```
