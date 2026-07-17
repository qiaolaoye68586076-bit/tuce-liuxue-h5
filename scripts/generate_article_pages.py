#!/usr/bin/env python3
"""从 articles.json 生成静态文章页、sitemap.xml 和 llms.txt。"""

import html
import json
import os
import re
import time


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

CORE_SITEMAP = [
    ("https://tuce.asia/", "weekly", "1.0", "index.html"),
    ("https://tuce.asia/services", "monthly", "0.9", "services.html"),
    ("https://tuce.asia/meiben", "monthly", "0.9", "meiben.html"),
    ("https://tuce.asia/graduate", "monthly", "0.7", "graduate.html"),
    ("https://tuce.asia/transfer", "monthly", "0.7", "transfer.html"),
    ("https://tuce.asia/uk-eu", "monthly", "0.7", "uk-eu.html"),
    ("https://tuce.asia/immigration", "monthly", "0.7", "immigration.html"),
    ("https://tuce.asia/teachers", "monthly", "0.8", "teachers.html"),
    ("https://tuce.asia/cases", "monthly", "0.9", "cases.html"),
    ("https://tuce.asia/blog", "weekly", "0.8", "blog.html"),
]


TEMPLATE = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
  <meta name="theme-color" content="#FAF7F0" />
  <link rel="icon" type="image/webp" href="../assets/logo.webp" />
  <title>__TITLE_HTML__ | 途策留学 · 留学洞察</title>
  <meta name="description" content="__DIGEST_HTML__" />
  <meta name="keywords" content="__KEYWORDS__" />
  <meta name="author" content="途策留学 TUCE Education" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://tuce.asia/articles/__ID__.html" />
  <meta http-equiv="content-language" content="zh-CN" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="途策留学" />
  <meta property="og:locale" content="zh_CN" />
  <meta property="og:url" content="https://tuce.asia/articles/__ID__.html" />
  <meta property="og:title" content="__TITLE_HTML__ | 途策留学 · 留学洞察" />
  <meta property="og:description" content="__DIGEST_HTML__" />
  <meta property="og:image" content="https://tuce.asia/assets/og-cover-2026.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="途策留学 · 留学洞察" />
  <meta property="article:published_time" content="__ISO_DATE__" />
  <meta property="article:section" content="__CATEGORY_HTML__" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="__TITLE_HTML__ | 途策留学" />
  <meta name="twitter:description" content="__DIGEST_HTML__" />
  <meta name="twitter:image" content="https://tuce.asia/assets/og-cover-2026.jpg" />
  <script type="application/ld+json">__ARTICLE_JSON__</script>
  <script type="application/ld+json">__BREADCRUMB_JSON__</script>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Fraunces:wght@400;500;600&family=Noto+Sans+SC:wght@300;400;500;700&family=Noto+Serif+SC:wght@500;600;700&display=swap" />
  <link rel="stylesheet" href="../css/style.css?v=3d3621bf" />
  <style>
    .article-page { max-width:760px; margin:0 auto; padding:120px 20px 60px; }
    .article-page h1 { font-family:var(--serif,'Noto Serif SC',serif); font-size:clamp(26px,4.5vw,38px); line-height:1.35; margin:0 0 24px; }
    .article-page__digest { font-size:18px; line-height:1.85; margin-bottom:32px; padding:24px 28px; background:#FCFAF4; border-left:3px solid var(--gold,#A89157); }
    .article-page__notice { margin-top:48px; padding:16px 20px; font-size:13.5px; line-height:1.7; background:rgba(168,145,87,.08); }
    @media (max-width:759.98px){ .article-page{padding:100px 16px 48px}.article-page__digest{font-size:16px;padding:18px 20px} }
  </style>
</head>
<body>
  <header class="nav" id="nav"><div class="nav__inner">
    <a class="brand" href="../" aria-label="途策留学"><span class="brand__badge"><img src="../assets/logo.webp" alt="途策留学" class="brand__logo" /></span><span class="brand__text"><b>途策留学</b><i>TUCE&nbsp;EDUCATION</i></span></a>
    <nav class="nav__links"><a href="../">首页</a><a href="../services">服务</a><a href="../teachers">师资</a><a href="../cases">案例</a><a href="../#faq">常见问题</a><a href="../blog" class="is-active">洞察</a></nav>
    <a href="../#consult" class="btn btn--cta nav__cta">免费评估</a>
    <button class="nav__burger" id="burger" aria-label="菜单"><span></span><span></span><span></span></button>
  </div><div class="nav__drawer" id="drawer"><a href="../">首页</a><a href="../services">服务</a><a href="../teachers">师资</a><a href="../cases">案例</a><a href="../#faq">常见问题</a><a href="../blog">洞察</a><a href="../#consult" class="btn btn--cta">免费评估</a></div></header>
  <main class="article-page">
    <a class="article-page__back" href="../blog">← 返回洞察列表</a>
    <span class="article-page__category">__CATEGORY_HTML__</span>
    <h1>__TITLE_HTML__</h1>
    <div class="article-page__meta"><span>__PUBLISH_DATE__</span><span aria-hidden="true">·</span><span>途策留学</span></div>
    <div class="article-page__digest">__DIGEST_HTML__</div>
    __WECHAT_CTA__
    <p class="article-page__notice">__NOTICE__</p>
  </main>
  <footer class="footer"><div class="footer__inner">
    <div class="footer__brand"><div class="brand brand--footer"><span class="brand__text"><b>途策留学</b><i>TUCE&nbsp;EDUCATION</i></span></div><p class="footer__desc">用专业策略，陪你抵达理想院校。</p></div>
    <div class="footer__col"><h4>联系方式</h4><ul class="footer__contact"><li><a href="tel:+8613665152000">+86 13665152000</a></li><li><a href="mailto:kevinqiao@tucededu.com">kevinqiao@tucededu.com</a></li><li><span>上海办公室 · 长宁区</span></li><li><span>无锡办公室 · 锡山区</span></li></ul></div>
    <div class="footer__col"><h4>快速链接</h4><a href="../services">服务方案</a><a href="../teachers">师资团队</a><a href="../cases">成功案例</a><a href="../#faq">常见问题</a><a href="../blog">留学洞察</a></div>
    <div class="footer__col"><h4>关注我们</h4><div class="footer__qr"><div class="qr qr--sm"><img src="../assets/qr-official.jpg" alt="微信公众号二维码" /></div><p>微信公众号</p></div></div>
  </div><div class="footer__bar"><span>&copy; 2026 途策留学 TUCE Education. 保留所有权利。</span><span><a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener nofollow">沪ICP备2026025218号-2</a></span></div></footer>
  <script src="../js/main.js?v=9"></script>
</body>
</html>'''


def default_web_root():
    return os.environ.get("TUCE_WEB_ROOT", "").strip() or os.path.join(PROJECT_DIR, "frontend")


def html_escape(value):
    return html.escape(str(value or ""), quote=True)


def json_string(value):
    return json.dumps(str(value or ""), ensure_ascii=False)


def valid_external_url(url):
    value = (url or "").strip()
    return value.startswith(("http://", "https://")) and "placeholder" not in value.lower()


def generate_keywords(title, category):
    base = "途策留学,留学洞察,留学申请"
    if "美国" in category or "美本" in title:
        base += ",美本申请,美国留学"
    if "英国" in category or "UCL" in title or "KCL" in title:
        base += ",英国留学,英国申请"
    if "香港" in category or "新加坡" in category:
        base += ",香港留学,新加坡留学"
    if "澳洲" in category or "加拿大" in category or "墨尔本" in title or "悉尼" in title:
        base += ",澳洲留学,加拿大留学"
    if "文书" in title:
        base += ",留学文书,文书技巧"
    if "计算机" in title or "数据科学" in title:
        base += ",计算机专业,数据科学专业"
    return base


def write_text_atomic(path, content):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(content)
    os.replace(tmp, path)


def load_existing_lastmods(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
    except OSError:
        return {}
    result = {}
    for block in re.findall(r"<url>([\s\S]*?)</url>", raw):
        loc = re.search(r"<loc>([^<]+)</loc>", block)
        lastmod = re.search(r"<lastmod>([^<]+)</lastmod>", block)
        if loc and lastmod:
            result[loc.group(1).strip()] = lastmod.group(1).strip()
    return result


def file_date(path):
    return time.strftime("%Y-%m-%d", time.localtime(os.path.getmtime(path)))


def generate_sitemap(web_root, articles):
    path = os.path.join(web_root, "sitemap.xml")
    old_lastmods = load_existing_lastmods(path)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', ""]
    for loc, changefreq, priority, filename in CORE_SITEMAP:
        lastmod = old_lastmods.get(loc, "")
        if not lastmod and os.path.exists(os.path.join(web_root, filename)):
            lastmod = file_date(os.path.join(web_root, filename))
        lines += ["  <url>", "    <loc>%s</loc>" % loc]
        if lastmod:
            lines.append("    <lastmod>%s</lastmod>" % html_escape(lastmod))
        lines += ["    <changefreq>%s</changefreq>" % changefreq, "    <priority>%s</priority>" % priority, "  </url>", ""]
    lines.append("  <!-- ===== 洞察文章（由 articles.json 生成） ===== -->")
    for article in articles:
        article_id = re.sub(r"[^A-Za-z0-9_-]", "", str(article.get("id") or ""))
        if not article_id:
            continue
        lines += ["  <url>", "    <loc>https://tuce.asia/articles/%s.html</loc>" % article_id]
        publish_time = str(article.get("publish_time") or "")
        if re.match(r"^\d{4}-\d{2}-\d{2}$", publish_time):
            lines.append("    <lastmod>%s</lastmod>" % publish_time)
        lines += ["    <changefreq>monthly</changefreq>", "    <priority>0.7</priority>", "  </url>"]
    lines += ["", "</urlset>", ""]
    write_text_atomic(path, "\n".join(lines))


def generate_llms(web_root, articles):
    lines = [
        "# 途策留学 TUCE Education", "",
        "- 品牌实体：途策留学 = TUCE Education = https://tuce.asia/",
        "- 业务类别：留学申请、留学咨询、国际教育服务", "",
        "> 高端留学申请机构，专注美国本科、研究生及英联邦国家策略定制。3对1专属团队，从选校到文书全程陪伴。", "",
        "## 关于我们", "途策留学是一家以策略驱动的留学申请机构，不做模板化申请。先用 G7 潜能测评了解学生，再定制方案。2024–2026 三届学员取得 220+ 枚 Offer，覆盖美英港新澳加 59 所院校。", "",
        "## 核心页面", "",
        "- [首页](https://tuce.asia/)", "- [服务总览](https://tuce.asia/services)", "- [美国本科](https://tuce.asia/meiben)", "- [研究生](https://tuce.asia/graduate)", "- [转学](https://tuce.asia/transfer)", "- [多国联申](https://tuce.asia/uk-eu)", "- [美国移民](https://tuce.asia/immigration)", "- [师资团队](https://tuce.asia/teachers)", "- [成功案例](https://tuce.asia/cases)", "- [留学洞察](https://tuce.asia/blog)", "- [免费评估](https://tuce.asia/#consult)", "",
        "## 联系方式", "", "- 电话：+86 13665152000", "- 邮箱：kevinqiao@tucededu.com", "- 地址：上海长宁区 / 无锡锡山区", "",
        "## 文章列表", "",
    ]
    for article in articles:
        article_id = re.sub(r"[^A-Za-z0-9_-]", "", str(article.get("id") or ""))
        title = str(article.get("title") or "").replace("[", "\\[").replace("]", "\\]")
        if article_id and title:
            lines.append("- [%s](https://tuce.asia/articles/%s.html) — %s" % (title, article_id, article.get("publish_time", "")))
    lines.append("")
    write_text_atomic(os.path.join(web_root, "llms.txt"), "\n".join(lines))


def generate_pages(web_root=None, articles_json=None, out_dir=None):
    web_root = web_root or default_web_root()
    articles_json = articles_json or os.path.join(web_root, "articles.json")
    out_dir = out_dir or os.path.join(web_root, "articles")
    with open(articles_json, "r", encoding="utf-8") as f:
        articles = json.load(f).get("articles", [])
    os.makedirs(out_dir, exist_ok=True)

    # 文章目录完全由 articles.json 管理，清掉旧 ID，避免博客链接指向过期页面。
    for filename in os.listdir(out_dir):
        if filename.endswith(".html"):
            os.remove(os.path.join(out_dir, filename))

    for article in articles:
        article_id = re.sub(r"[^A-Za-z0-9_-]", "", str(article.get("id") or ""))
        if not article_id:
            continue
        title = str(article.get("title") or "")
        digest = str(article.get("digest") or "")
        category = str(article.get("category") or "途策洞察")
        publish_time = str(article.get("publish_time") or "")
        article_url = "https://tuce.asia/articles/%s.html" % article_id
        article_json = {
            "@context": "https://schema.org",
            "@type": "Article",
            "@id": article_url + "#article",
            "headline": title,
            "description": digest,
            "author": {"@id": "https://tuce.asia/#organization"},
            "publisher": {"@id": "https://tuce.asia/#organization"},
            "datePublished": (publish_time + "T00:00:00+08:00") if publish_time else "",
            "url": article_url,
            "mainEntityOfPage": {"@id": article_url},
            "inLanguage": "zh-CN",
            "about": category,
        }
        breadcrumb_json = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "首页", "item": "https://tuce.asia/"},
                {"@type": "ListItem", "position": 2, "name": "留学洞察", "item": "https://tuce.asia/blog"},
                {"@type": "ListItem", "position": 3, "name": title, "item": article_url},
            ],
        }
        if valid_external_url(article.get("url")):
            wechat_cta = '<a class="article-page__cta" href="%s" target="_blank" rel="noopener">在微信阅读全文 →</a>' % html_escape(article["url"])
            notice = "本文首发于途策留学微信公众号。点击上方按钮跳转微信阅读完整内容。"
        else:
            wechat_cta = ""
            notice = "本文摘要正在整理中，完整内容请返回途策留学留学洞察栏目查看最新文章。"
        values = {
            "__TITLE_HTML__": html_escape(title),
            "__DIGEST_HTML__": html_escape(digest),
            "__KEYWORDS__": html_escape(generate_keywords(title, category)),
            "__ID__": article_id,
            "__ISO_DATE__": html_escape((publish_time + "T00:00:00+08:00") if publish_time else ""),
            "__CATEGORY_HTML__": html_escape(category),
            "__ARTICLE_JSON__": json.dumps(article_json, ensure_ascii=False, indent=2),
            "__BREADCRUMB_JSON__": json.dumps(breadcrumb_json, ensure_ascii=False, indent=2),
            "__PUBLISH_DATE__": html_escape(publish_time),
            "__WECHAT_CTA__": wechat_cta,
            "__NOTICE__": html_escape(notice),
        }
        rendered = TEMPLATE
        for key, value in values.items():
            rendered = rendered.replace(key, value)
        with open(os.path.join(out_dir, article_id + ".html"), "w", encoding="utf-8") as f:
            f.write(rendered)

    generate_sitemap(web_root, articles)
    generate_llms(web_root, articles)
    return len(articles)


if __name__ == "__main__":
    print("Generated %d article pages and SEO files" % generate_pages())
