#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
途策留学官网 — 静态站点构建脚本（"中央厨房"）
=================================================

做什么：
  把"公共部件（页头/导航/页脚）+ 内容数据（YAML）+ 模板（Jinja2）"
  组装成一批纯静态 HTML，输出到 dist/。改一次导航/页脚，全站自动更新；
  案例、顾问、服务、FAQ 这类重复结构由数据驱动批量生成。

为什么：
  站点是多页（关于/案例/服务/团队/FAQ/博客），纯手写会重复劳动且难维护。
  本脚本只依赖 Jinja2 + PyYAML，产物是普通 HTML，可直接传国内云 OSS+CDN。

怎么用：
  python3 -m pip install -r requirements.txt
  python3 build.py            # 构建到 dist/
  python3 build.py --serve    # 构建并本地预览 http://localhost:8000

URL 规则：
  采用"目录式漂亮链接"——/about/ 对应 dist/about/index.html，
  这样无需服务器特殊配置即可在 /about/ 访问。全站资源用根绝对路径（/css、/assets）。
"""

from __future__ import annotations

import json
import shutil
import sys
from datetime import date
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

# ---- 路径 ----
ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
DATA = SITE / "data"
TEMPLATES = SITE / "templates"
STATIC = SITE / "static"          # robots.txt / llms.txt / 自托管字体等，原样拷贝
DIST = ROOT / "dist"

# 直接从仓库根拷贝到 dist 的静态资源目录
ASSET_DIRS = ["assets", "css", "js"]

TODAY = date.today().isoformat()


# ============================================================
# 数据加载
# ============================================================
def load_yaml(name: str) -> dict | list:
    """读取 site/data/<name>.yaml；文件不存在时返回空。"""
    path = DATA / f"{name}.yaml"
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_data() -> dict:
    """汇总所有数据源，注入到每个模板的全局上下文。"""
    site = load_yaml("site")
    data = {
        "site": site,
        "services": load_yaml("services").get("items", []),
        "cases": load_yaml("cases").get("items", []),
        "team": load_yaml("team").get("items", []),
        "faq": load_yaml("faq").get("items", []),
        "blog": load_yaml("blog").get("items", []),
        "today": TODAY,
        "year": date.today().year,
    }
    return data


# ============================================================
# JSON-LD 结构化数据生成器（按页型自动产出）
# ============================================================
def org_schema(site: dict) -> dict:
    """EducationalOrganization —— 全站组织实体（每页都带，建立可信度）。"""
    c = site["contact"]
    b = site["brand"]
    same_as = [u for u in site.get("social", {}).values()
               if isinstance(u, str) and u.startswith("http")]
    org = {
        "@context": "https://schema.org",
        "@type": "EducationalOrganization",
        "@id": f"{site['site_url']}/#organization",
        "name": b["alt_name"],
        "alternateName": b["name_cn"],
        "url": site["site_url"],
        "logo": site["site_url"] + b["logo_url"],
        "description": "一家以策略驱动的留学申请机构，专注帮助学生用最优路径实现海外名校梦想。"
                       "提供美国本科、研究生、转学及英联邦国家高端留学申请服务。",
        "foundingDate": b.get("founding_date", ""),
        "areaServed": [c["region"], "全国"],
        "knowsAbout": site.get("knows_about", []),
        "serviceType": site.get("service_types", []),
        "parentOrganization": {"@type": "Organization", "name": b["legal_name"]},
    }
    # 仅在有真实数据时加入这些字段（避免占位污染 schema）
    addr = c.get("address", "")
    if addr and "待填" not in addr:
        org["address"] = {
            "@type": "PostalAddress",
            "addressLocality": c["locality"],
            "addressRegion": c["region"],
            "streetAddress": addr,
            "addressCountry": c["country"],
        }
    tel = c.get("telephone", "")
    if tel and "待填" not in tel:
        org["telephone"] = tel
    email = c.get("email", "")
    if email and "待填" not in email:
        org["email"] = email
    if same_as:
        org["sameAs"] = same_as
    return org


def breadcrumb_schema(site: dict, crumbs: list[tuple[str, str]]) -> dict:
    """BreadcrumbList —— crumbs 为 [(名称, 相对URL), ...]。"""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": site["site_url"] + url,
            }
            for i, (name, url) in enumerate(crumbs)
        ],
    }


def faq_schema(items: list[dict]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q["q"],
                "acceptedAnswer": {"@type": "Answer", "text": q["a"]},
            }
            for q in items
        ],
    }


def service_schema(site: dict, svc: dict) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": svc["title"],
        "serviceType": svc["title"],
        "description": svc.get("summary", ""),
        "areaServed": [site["contact"]["region"], "全国"],
        "provider": {"@id": f"{site['site_url']}/#organization"},
    }


def service_howto_schema(svc: dict) -> dict:
    """服务流程 → HowTo（AI 抽取“怎么做”类问题）。"""
    return {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": f"{svc['title']}流程",
        "description": svc.get("summary", ""),
        "step": [
            {
                "@type": "HowToStep",
                "position": i + 1,
                "name": s["t"],
                "text": s["d"],
            }
            for i, s in enumerate(svc.get("steps", []))
        ],
    }


def case_review_schema(site: dict, case: dict) -> dict:
    """单个案例 → Review（AI 最爱引用的真实案例）。"""
    return {
        "@context": "https://schema.org",
        "@type": "Review",
        "itemReviewed": {"@id": f"{site['site_url']}/#organization"},
        "reviewBody": case.get("quote") or case.get("summary", ""),
        "author": {"@type": "Person", "name": case.get("student", "途策学员")},
        "name": case.get("title", ""),
    }


def cases_itemlist_schema(site: dict, cases: list[dict]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": c.get("title", ""),
                "url": f"{site['site_url']}/cases/{c['slug']}/",
            }
            for i, c in enumerate(cases)
        ],
    }


# ============================================================
# 页面注册表：声明每个页面要渲染什么
# ============================================================
def build_registry(data: dict) -> list[dict]:
    site = data["site"]
    org = org_schema(site)
    pages: list[dict] = []

    def add(url, template, title, description, schemas, ctx=None, crumbs=None):
        crumbs = crumbs or []
        page_schemas = [org] + (schemas or [])
        if crumbs:
            page_schemas.append(breadcrumb_schema(site, [("首页", "/")] + crumbs))
        ctx = dict(ctx or {})
        # 可见面包屑（与 BreadcrumbList schema 一致），首页不显示
        ctx["crumbs"] = [("首页", "/")] + crumbs if crumbs else []
        pages.append({
            "url": url,
            "template": template,
            "title": title,
            "description": description,
            "schemas": page_schemas,
            "ctx": ctx,
        })

    # 首页
    add("/", "index.html",
        "途策留学 · 高端留学申请机构 | 美本/美研/英联邦 策略定制",
        "途策留学（TUCE Education）是一家以策略驱动的留学申请机构，专注美国本科、"
        "研究生及英联邦国家高端申请。3对1专属团队，从选校策略到文书创作全程陪伴。免费评估。",
        [faq_schema(data["faq"][:5])] if data["faq"] else [])

    # 关于我们
    add("/about/", "about.html",
        "关于途策留学 | 上海高端留学申请机构",
        "途策留学成立于上海，专注高端海外升学规划，3对1专属团队、策略先行、拒绝模板。"
        "了解途策的理念、团队与可验证的录取成果。",
        [], crumbs=[("关于我们", "/about/")])

    # 服务总览
    add("/services/", "services_index.html",
        "留学服务 | 美本·美研·英联邦·背景提升·文书 | 途策留学",
        "途策留学覆盖美国本科、美国研究生、英国本科/研究生、背景提升与文书服务，"
        "按目标定制策略团队与时间线。",
        [], ctx={"services": data["services"]},
        crumbs=[("服务", "/services/")])

    # 服务子页
    for svc in data["services"]:
        add(f"/services/{svc['slug']}/", "service_detail.html",
            f"{svc['title']} | 途策留学",
            svc.get("meta_desc", svc.get("summary", "")),
            [service_schema(site, svc), service_howto_schema(svc)], ctx={"svc": svc},
            crumbs=[("服务", "/services/"), (svc["title"], f"/services/{svc['slug']}/")])

    # 案例总览
    add("/cases/", "cases_index.html",
        "成功案例 | 途策留学2026录取榜",
        "途策留学历届真实录取案例：从背景定位到录取结果，每一步有迹可循。"
        "覆盖美国藤校、英国G5等顶尖院校。",
        [cases_itemlist_schema(site, data["cases"])] if data["cases"] else [],
        ctx={"cases": data["cases"]},
        crumbs=[("成功案例", "/cases/")])

    # 案例子页
    for case in data["cases"]:
        add(f"/cases/{case['slug']}/", "case_detail.html",
            f"{case['title']} | 途策留学",
            case.get("meta_desc", case.get("summary", "")),
            [case_review_schema(site, case)], ctx={"case": case},
            crumbs=[("成功案例", "/cases/"), (case["title"], f"/cases/{case['slug']}/")])

    # 团队总览
    add("/team/", "team_index.html",
        "师资团队 | 藤校背景留学导师 | 途策留学",
        "途策留学的策略顾问、文书导师与个性化导师团队，藤校背景、多年从业经验，"
        "1对1陪伴每一处申请细节。",
        [], ctx={"team": data["team"]},
        crumbs=[("师资团队", "/team/")])

    # 顾问子页
    for member in data["team"]:
        add(f"/team/{member['slug']}/", "team_detail.html",
            f"{member['name']} · {member.get('title','')} | 途策留学",
            member.get("meta_desc", member.get("bio", "")[:80]),
            [], ctx={"member": member},
            crumbs=[("师资团队", "/team/"), (member["name"], f"/team/{member['slug']}/")])

    # FAQ
    add("/faq/", "faq.html",
        "常见问题 | 途策留学收费·流程·换顾问·退费",
        "关于途策留学的服务流程、收费、签约、顾问更换、退费机制等常见问题解答。",
        [faq_schema(data["faq"])] if data["faq"] else [],
        ctx={"faq": data["faq"]},
        crumbs=[("常见问题", "/faq/")])

    # 博客总览
    add("/blog/", "blog_index.html",
        "升学资讯 | 留学申请干货 | 途策留学",
        "途策留学升学资讯：选机构、申请趋势、场景指南与对比分析，帮你做明智的留学决策。",
        [], ctx={"posts": data["blog"]},
        crumbs=[("升学资讯", "/blog/")])

    return pages


# ============================================================
# 渲染
# ============================================================
def jsonld_block(schemas: list[dict]) -> str:
    """把多个 schema 字典渲染成多段 <script type="application/ld+json">。"""
    out = []
    for s in schemas:
        out.append(
            '<script type="application/ld+json">\n'
            + json.dumps(s, ensure_ascii=False, indent=2)
            + "\n</script>"
        )
    return "\n".join(out)


def render(env: Environment, data: dict, pages: list[dict]) -> None:
    for p in pages:
        tpl = env.get_template(p["template"])
        ctx = dict(data)
        ctx.update(p["ctx"])
        ctx.update({
            "page_url": p["url"],
            "canonical": data["site"]["site_url"] + p["url"],
            "page_title": p["title"],
            "page_description": p["description"],
            "jsonld": jsonld_block(p["schemas"]),
        })
        html = tpl.render(**ctx)
        out_path = DIST / p["url"].lstrip("/") / "index.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
        print(f"  ✓ {p['url']:32s} -> {out_path.relative_to(ROOT)}")


def generate_sitemap(site: dict, pages: list[dict]) -> None:
    """根据页面注册表生成 sitemap.xml（含 lastmod）。"""
    urls = []
    for p in pages:
        loc = site["site_url"] + p["url"]
        urls.append(
            f"  <url>\n    <loc>{loc}</loc>\n"
            f"    <lastmod>{TODAY}</lastmod>\n  </url>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (DIST / "sitemap.xml").write_text(xml, encoding="utf-8")
    print(f"  ✓ sitemap.xml ({len(pages)} urls)")


def copy_static() -> None:
    """拷贝资源目录与 site/static/*（robots.txt、llms.txt、字体等）到 dist。"""
    for d in ASSET_DIRS:
        src = ROOT / d
        if src.exists():
            shutil.copytree(src, DIST / d, dirs_exist_ok=True)
            print(f"  ✓ copied {d}/")
    if STATIC.exists():
        for item in STATIC.iterdir():
            if item.is_dir():
                shutil.copytree(item, DIST / item.name, dirs_exist_ok=True)
            else:
                shutil.copy2(item, DIST / item.name)
        print(f"  ✓ copied site/static/* (robots.txt / llms.txt / fonts)")


def main() -> int:
    print("== 构建途策留学官网 ==")
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    data = load_data()
    pages = build_registry(data)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    print("- 渲染页面")
    render(env, data, pages)
    print("- 生成 sitemap")
    generate_sitemap(data["site"], pages)
    print("- 拷贝静态资源")
    copy_static()

    print(f"== 完成：{len(pages)} 个页面 -> {DIST} ==")

    if "--serve" in sys.argv:
        import http.server
        import os
        os.chdir(DIST)
        port = 8000
        print(f"预览：http://localhost:{port}  (Ctrl+C 退出)")
        http.server.test(
            HandlerClass=http.server.SimpleHTTPRequestHandler, port=port
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
