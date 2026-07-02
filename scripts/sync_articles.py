#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/sync_articles.py — 公众号文章 → frontend/articles.json 同步

定时（cron）调用微信公众号 API 拉取已发布图文，生成前端消费的 articles.json，
并把封面图下载到本地（规避 mmbiz 图片防盗链），让 index.html / blog.html 自动更新。

零第三方依赖：生产服务器是 Python 3.6.8，装不了第三方包，全程只用标准库
（urllib / json / hashlib / ...），与 backend/app.py 同一思路。

环境变量：
  WX_APPID            公众号 AppID（必填）
  WX_APPSECRET        公众号 AppSecret（必填）—— 切勿写进代码或提交仓库，放 .env
  TUCE_WEB_ROOT       前端 web 根目录；默认脚本同级的 ../frontend
                      （服务器上设为 /var/www/tuce，直接写进线上站点）
  WX_ARTICLE_SOURCE   tikhub | auto | material | freepublish
                      tikhub=第三方接口取主页「文章」全量历史（需 TIKHUB_KEY+WX_GH_USERNAME）；
                      auto/material/freepublish=微信官方接口（需 WX_APPID+WX_APPSECRET）
  TIKHUB_KEY          source=tikhub 时必填：TikHub API key（Bearer 认证）
  WX_GH_USERNAME      source=tikhub 时必填：公众号 gh_ 原始ID（非 AppID）
  WX_MAX_ARTICLES     最多保留多少篇（默认 30）
  WX_FETCH_PAGES      每次最多翻几页（每页≈10篇）。0=全量翻到上限（首次/重建）；
                      1=增量只取最新一页并与现有 articles.json 合并去重（日常 cron 省钱）
  WX_DOWNLOAD_COVERS  1/0 是否把封面下载到本地（默认 1；mmbiz 直链有防盗链，建议开）
  WX_DEFAULT_CATEGORY 关键词命中不到时的兜底分类（默认 美国地区）

用法：
  python3 sync_articles.py            # 正式同步，写入 articles.json（+ 下载封面）
  python3 sync_articles.py --dry-run  # 只拉取并打印结果，不写任何文件
  python3 sync_articles.py -v         # 详细日志（DEBUG）

退出码：0 成功；1 配置/网络/接口错误（cron 可据此判断是否告警）。

依赖前提（详见 scripts/README.md）：
  1. 服务器公网出口 IP 必须加入「公众号后台 → 设置与开发 → 基本配置 → IP 白名单」，
     否则 cgi-bin/token 报 errcode 40164。
  2. 账号需具备「素材管理」或「发布」接口权限（认证服务号/订阅号）。
"""

import argparse
import hashlib
import json
import logging
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API = "https://api.weixin.qq.com"
TIKHUB_API = "https://api.tikhub.io/api/v1/wechat_mp/v2/fetch_account_articles"
HERE = os.path.dirname(os.path.abspath(__file__))
TOKEN_CACHE = os.path.join(HERE, ".wx_token_cache.json")
OVERRIDES_PATH = os.path.join(HERE, "article_overrides.json")

# 前端筛选 pills 固定 5 类（见 frontend/blog.html #blogFilter），关键词命中归入对应类
CATEGORY_KEYWORDS = [
    ("英国地区", ["英国", "伦敦", "牛津", "剑桥", "爱丁堡", "曼大", "曼彻斯特", "G5",
                  "UCL", "KCL", "LSE", "IC", "帝国理工", "杜伦", "布里斯托", "华威"]),
    ("香港·新加坡", ["香港", "港大", "港中文", "港中大", "港科", "港城", "理工",
                     "新加坡", "南洋", "港三", "新二", "NUS", "NTU", "SMU", "HKU"]),
    ("澳洲·加拿大", ["澳洲", "澳大利亚", "墨尔本", "悉尼", "昆士兰", "莫纳什", "G8",
                     "加拿大", "多伦多", "麦吉尔", "滑铁卢", "UBC", "麦考瑞"]),
    ("美国地区", ["美国", "美本", "美研", "藤校", "常春藤", "哈佛", "耶鲁", "斯坦福",
                  "MIT", "普林斯顿", "早申", "Common App", "ED", "EA", "UC", "T30", "Top30"]),
    ("专业解读", ["专业", "计算机", "数据科学", "人工智能", "金融", "商科", "经济",
                  "工程", "传媒", "法律", "医学", "文书", "选校", "选专业", "CS", "AI"]),
]

log = logging.getLogger("sync_articles")


# ----------------------------- HTTP 小工具 -----------------------------
def _request(url, data=None, timeout=15):
    """统一请求：data 为 dict 时按 JSON POST，否则 GET。"""
    headers = {"User-Agent": "tuce-sync/1.0", "Referer": "https://mp.weixin.qq.com"}
    if data is not None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=body, headers=headers)
    else:
        req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def wx_call(path, payload=None, token=None, timeout=15):
    """调用微信 API 并解析 JSON；遇到 errcode 抛出带中文提示的异常。"""
    url = API + path
    if token:
        sep = "&" if "?" in url else "?"
        url = "%s%saccess_token=%s" % (url, sep, urllib.parse.quote(token))
    raw = _request(url, data=payload, timeout=timeout)
    obj = json.loads(raw.decode("utf-8"))
    errcode = obj.get("errcode", 0)
    if errcode:
        raise WxError(errcode, obj.get("errmsg", ""))
    return obj


class WxError(Exception):
    HINTS = {
        40001: "AppSecret 不对或 token 失效（请核对 WX_APPSECRET）",
        40013: "AppID 无效（请核对 WX_APPID）",
        40164: "服务器 IP 不在公众号白名单 —— 去「基本配置 → IP 白名单」加上本机公网出口 IP",
        45009: "今日接口调用已达上限（明天再试或减少同步频率）",
        48001: "该接口未授权 —— 当前账号无「素材管理/发布」权限（需认证服务号/订阅号）",
    }

    def __init__(self, errcode, errmsg):
        self.errcode = errcode
        self.errmsg = errmsg
        hint = self.HINTS.get(errcode, "")
        msg = "微信接口报错 errcode=%s errmsg=%s" % (errcode, errmsg)
        if hint:
            msg += "  →  %s" % hint
        super().__init__(msg)


# ----------------------------- access_token -----------------------------
def get_access_token(appid, secret, force=False):
    """带文件缓存，避免触发每日取 token 次数上限（token 有效期 7200s）。"""
    now = int(time.time())
    if not force and os.path.exists(TOKEN_CACHE):
        try:
            with open(TOKEN_CACHE, "r", encoding="utf-8") as f:
                c = json.load(f)
            if c.get("appid") == appid and c.get("expires_at", 0) > now + 60:
                log.debug("复用缓存 token，剩余 %ds", c["expires_at"] - now)
                return c["access_token"]
        except Exception as e:  # 缓存损坏不致命，重新取
            log.debug("token 缓存读取失败，重新获取：%s", e)

    obj = wx_call("/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
                  % (urllib.parse.quote(appid), urllib.parse.quote(secret)))
    token = obj["access_token"]
    expires_in = int(obj.get("expires_in", 7200))
    try:
        with open(TOKEN_CACHE, "w", encoding="utf-8") as f:
            json.dump({"appid": appid, "access_token": token,
                       "expires_at": now + expires_in - 300}, f)
        os.chmod(TOKEN_CACHE, 0o600)  # token 是凭据，收紧权限
    except Exception as e:
        log.debug("token 缓存写入失败（不影响本次）：%s", e)
    log.debug("已获取新 token，有效期 %ds", expires_in)
    return token


# ----------------------------- 拉取图文列表 -----------------------------
def _flatten_items(items):
    """把 batchget 返回的 item[] 展开为单篇 news_item 列表，带上 item 级 update_time。"""
    out = []
    for it in items or []:
        update_time = it.get("update_time") or 0
        news = (it.get("content") or {}).get("news_item") or []
        for n in news:
            out.append((n, n.get("update_time") or update_time))
    return out


def fetch_source(token, path, payload_base, max_n):
    """通用分页拉取（material/batchget_material 与 freepublish/batchget 同构）。"""
    flat = []
    offset = 0
    count = 20  # 接口单页上限 20
    while len(flat) < max_n:
        payload = dict(payload_base)
        payload.update({"offset": offset, "count": count})
        obj = wx_call(path, payload=payload, token=token)
        items = obj.get("item") or []
        if not items:
            break
        flat.extend(_flatten_items(items))
        total = obj.get("total_count", 0)
        offset += len(items)
        if offset >= total or len(items) < count:
            break
    return flat[:max_n]


def fetch_articles_raw(token, source, max_n):
    """按 source 拉取；auto 模式先 material 后 freepublish，取先有数据者。"""
    plans = {
        "material": ("/cgi-bin/material/batchget_material", {"type": "news"}),
        "freepublish": ("/cgi-bin/freepublish/batchget", {"no_content": 1}),
    }
    order = ["material", "freepublish"] if source == "auto" else [source]
    last_err = None
    for name in order:
        path, base = plans[name]
        try:
            flat = fetch_source(token, path, base, max_n)
            if flat:
                log.info("数据源：%s，拉到 %d 篇", name, len(flat))
                return flat
            log.info("数据源 %s 返回 0 篇%s", name, "，尝试下一个" if source == "auto" else "")
        except WxError as e:
            last_err = e
            log.warning("数据源 %s 失败：%s%s", name, e, "，尝试下一个" if source == "auto" else "")
    if last_err and source == "auto":
        # auto 下两个都失败，把最后一个错误抛出去让 cron 感知
        raise last_err
    return []


# ----------------------------- TikHub 第三方源 -----------------------------
class TikhubError(Exception):
    pass


def fetch_tikhub(gh_username, api_key, max_n, item_show_type=0, timeout=35, max_pages=0):
    """经 TikHub 接口拉公众号主页「文章」tab 的历史发文。

    覆盖微信官方 freepublish/material 的盲区（群发未发表 / 图片 / 第三方排版发的文章）。
    手动翻页：offset 首页留空 → 取响应 next_offset 回传 → is_end 为真即末页。
    max_pages>0 时只翻这么多页（增量模式：日常只取最新一页，省计费）。
    返回与 fetch_source 同构的 [(news_item_like, update_ts), ...]，复用下游 build_articles。
    每页计费一次（约 $0.01）。
    """
    flat = []
    offset = ""
    page = 0
    while len(flat) < max_n:
        payload = {"username": gh_username, "page_size": 20, "offset": offset,
                   "item_show_type": item_show_type, "raw": False}
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(TIKHUB_API, data=body, headers={
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json",
            "User-Agent": "tuce-sync/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                obj = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "ignore")[:200]
            raise TikhubError("TikHub HTTP %s：%s（核对 TIKHUB_KEY 是否有效/额度）"
                              % (e.code, detail))
        if obj.get("code") != 200:
            raise TikhubError("TikHub 返回 code=%s message=%s"
                              % (obj.get("code"), obj.get("message")))
        data = obj.get("data") or {}
        arts = data.get("articles") or []
        page += 1
        for a in arts:
            news_item = {
                "title": (a.get("title") or "").strip(),
                "url": _canon_url((a.get("url") or "").strip()),
                "digest": (a.get("digest") or "").strip(),
                "thumb_url": (a.get("cover") or "").strip(),  # 复用封面下载逻辑
            }
            # 发表时间优先 create_time（微信 appmsg 的「发表时间」戳，预约发表=计划发布时刻），
            # 仅当缺失时才退到 update_time（最后编辑/上传时间）——避免把「上传时间」当「发表时间」。
            ts = a.get("create_time") or a.get("update_time") or 0
            flat.append((news_item, ts))
        log.info("TikHub 第 %d 页：+%d 篇（累计 %d）", page, len(arts), len(flat))
        if data.get("is_end") or not data.get("next_offset") or not arts:
            break
        if max_pages and page >= max_pages:
            break
        offset = data["next_offset"]
    return flat[:max_n]


# ----------------------------- 字段映射 -----------------------------
_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def make_digest(news_item):
    digest = (news_item.get("digest") or "").strip()
    if digest:
        return digest
    content = news_item.get("content") or ""
    text = _WS_RE.sub(" ", _TAG_RE.sub("", content)).strip()
    if not text:
        return ""
    return (text[:60] + "…") if len(text) > 60 else text


def categorize(title, default_cat):
    t = title or ""
    tl = t.lower()
    for cat, kws in CATEGORY_KEYWORDS:
        for kw in kws:
            if kw.lower() in tl:
                return cat
    return default_cat


def _canon_url(u):
    """规范化微信文章 url：只保留 __biz/mid/idx/sn（文章永久标识），去掉
    scene/sessionid 等每次请求都变的态参数——否则增量去重会把同一篇当新文章。"""
    if not u:
        return ""
    try:
        p = urllib.parse.urlparse(u)
        q = urllib.parse.parse_qs(p.query)
        keep = ["%s=%s" % (k, q[k][0]) for k in ("__biz", "mid", "idx", "sn") if q.get(k)]
        if keep:
            return "%s://%s%s?%s" % (p.scheme, p.netloc, p.path, "&".join(keep))
    except Exception:
        pass
    return u


def stable_id(url, title):
    seed = url or title or ""
    return hashlib.sha1(seed.encode("utf-8")).hexdigest()[:12]


def fmt_date(ts):
    try:
        return time.strftime("%Y-%m-%d", time.localtime(int(ts)))
    except Exception:
        return ""


# ----------------------------- 封面下载 -----------------------------
_EXT_BY_CT = {
    "image/jpeg": ".jpg", "image/jpg": ".jpg", "image/png": ".png",
    "image/gif": ".gif", "image/webp": ".webp",
}


def download_cover(url, dest_dir, key):
    """下载封面到 dest_dir/<key>.<ext>，返回相对 web 根的路径；失败返回空串。"""
    if not url:
        return ""
    try:
        headers = {"User-Agent": "tuce-sync/1.0", "Referer": "https://mp.weixin.qq.com"}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as resp:
            ct = (resp.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            data = resp.read()
        ext = _EXT_BY_CT.get(ct, ".jpg")
        fname = key + ext
        os.makedirs(dest_dir, exist_ok=True)
        tmp = os.path.join(dest_dir, fname + ".tmp")
        with open(tmp, "wb") as f:
            f.write(data)
        os.replace(tmp, os.path.join(dest_dir, fname))
        return "assets/insights/" + fname
    except Exception as e:
        log.warning("封面下载失败（用占位图兜底）：%s", e)
        return ""


def prune_covers(dest_dir, keep):
    """删除 insights 目录里本轮未引用的旧封面，避免无限堆积。"""
    if not os.path.isdir(dest_dir):
        return
    for f in os.listdir(dest_dir):
        if f.endswith(".tmp") or f not in keep:
            try:
                os.remove(os.path.join(dest_dir, f))
                log.debug("清理旧封面：%s", f)
            except OSError:
                pass


# ----------------------------- 覆盖配置 -----------------------------
def load_overrides():
    if not os.path.exists(OVERRIDES_PATH):
        return {}
    try:
        with open(OVERRIDES_PATH, "r", encoding="utf-8") as f:
            return json.load(f) or {}
    except Exception as e:
        log.warning("article_overrides.json 解析失败，忽略：%s", e)
        return {}


def load_existing(out_path):
    """读现有 articles.json 的 articles[]（增量合并用）；缺失/损坏按空处理。"""
    try:
        with open(out_path, "r", encoding="utf-8") as f:
            return (json.load(f).get("articles")) or []
    except Exception as e:
        log.debug("读现有 articles.json 失败（按空处理）：%s", e)
        return []


# ----------------------------- 组装 -----------------------------
def build_articles(raw, web_root, download_covers, default_cat, overrides, max_n, existing=None):
    by_url = overrides.get("by_url") or {}
    insights_dir = os.path.join(web_root, "assets", "insights")
    articles = []
    seen = set()  # 去重键：规范化 url

    # 增量：先纳入已有文章（保留其本地封面，避免重复下载/重复计费）
    for art in existing or []:
        if by_url.get(art.get("url") or "", {}).get("hidden"):
            continue
        seen.add(_canon_url(art.get("url") or ""))
        articles.append(art)

    for news_item, update_ts in raw:
        url = (news_item.get("url") or "").strip()
        title = (news_item.get("title") or "").strip()
        if not title:
            continue
        cu = _canon_url(url)
        if cu in seen:
            continue  # 已有（增量），跳过，省去重复封面下载
        ov = by_url.get(url, {})
        if ov.get("hidden"):
            log.debug("按覆盖配置隐藏：%s", title)
            continue

        aid = stable_id(url, title)
        cover = ""
        thumb_url = (news_item.get("thumb_url") or "").strip()
        if download_covers and thumb_url:
            rel = download_cover(thumb_url, insights_dir, aid)
            if rel:
                cover = rel
        elif thumb_url:
            cover = thumb_url  # 不下载时退而用直链（注意可能受防盗链影响）

        articles.append({
            "id": aid,
            "title": title,
            "digest": ov.get("digest") or make_digest(news_item),
            "cover_url": cover,
            "url": url,
            "publish_time": fmt_date(update_ts),
            "category": ov.get("category") or categorize(title, default_cat),
            "pinned": bool(ov.get("pinned", False)),
        })
        seen.add(cu)

    # 倒序（最新在前）并截断到上限。publish_time 为发表时间（见字段映射），
    # 故排序后 articles[0] 就是「最新发表 / 预约发表已生效」的一篇。
    articles.sort(key=lambda a: a.get("publish_time", ""), reverse=True)
    articles = articles[:max_n]

    # ---- 置顶（pinned）每轮全量重算，不沿用 articles.json 里的旧值 ----
    # 增量同步会把上轮「自动置顶的最新文」连同 pinned=True 原样读回来；若沿用旧值，
    # any(pinned) 恒为真 → 新发/预约发表的文章即使排到最前也不会置顶，featured 卡永远
    # 卡在旧文上。所以这里按「overrides 人工置顶」+「时间最新」重新判定：
    #   1) overrides 里显式 pinned 的文章存在于列表 → 人工置顶优先，且仅这些置顶；
    #   2) 否则默认置顶最新一篇（pin_latest_if_none，默认开）——保证置顶始终是最新文章。
    manual_pins = {u for u, ov in (by_url or {}).items() if ov.get("pinned")}
    present_manual = any((a.get("url") or "") in manual_pins for a in articles)
    if present_manual:
        for a in articles:
            a["pinned"] = (a.get("url") or "") in manual_pins
    else:
        for a in articles:
            a["pinned"] = False
        if articles and overrides.get("pin_latest_if_none", True):
            articles[0]["pinned"] = True

    # 清理未引用的本地封面：仅全量模式做（增量下旧文封面不在本轮 raw 里，prune 会误删）
    if download_covers and existing is None:
        keep = {os.path.basename(a["cover_url"]) for a in articles
                if a.get("cover_url") and not a["cover_url"].startswith("http")}
        prune_covers(insights_dir, keep)

    return articles


def write_json_atomic(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, path)


# ----------------------------- main -----------------------------
def main():
    parser = argparse.ArgumentParser(description="公众号文章 → articles.json 同步")
    parser.add_argument("-n", "--dry-run", action="store_true",
                        help="只拉取并打印，不写文件、不下载封面")
    parser.add_argument("-v", "--verbose", action="store_true", help="DEBUG 日志")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s")

    web_root = os.environ.get("TUCE_WEB_ROOT", "").strip() \
        or os.path.normpath(os.path.join(HERE, "..", "frontend"))
    source = os.environ.get("WX_ARTICLE_SOURCE", "auto").strip().lower()
    max_n = int(os.environ.get("WX_MAX_ARTICLES", "30"))
    fetch_pages = int(os.environ.get("WX_FETCH_PAGES", "0") or 0)
    incremental = fetch_pages > 0
    download_covers = os.environ.get("WX_DOWNLOAD_COVERS", "1").strip() != "0" and not args.dry_run
    default_cat = os.environ.get("WX_DEFAULT_CATEGORY", "美国地区").strip()
    out_path = os.path.join(web_root, "articles.json")

    log.info("web_root=%s  source=%s  max=%d  翻页=%s  下载封面=%s%s",
             web_root, source, max_n,
             ("增量%d页" % fetch_pages) if incremental else "全量",
             download_covers, "  [DRY-RUN]" if args.dry_run else "")

    try:
        if source == "tikhub":
            gh = os.environ.get("WX_GH_USERNAME", "").strip()
            key = os.environ.get("TIKHUB_KEY", "").strip()
            if not gh or not key:
                log.error("source=tikhub 需要 WX_GH_USERNAME（gh_ 原始ID）与 TIKHUB_KEY（见 .env.example）")
                return 1
            raw = fetch_tikhub(gh, key, max_n, max_pages=fetch_pages)
        else:
            appid = os.environ.get("WX_APPID", "").strip()
            secret = os.environ.get("WX_APPSECRET", "").strip()
            if not appid or not secret:
                log.error("缺少 WX_APPID / WX_APPSECRET 环境变量（见 .env.example）")
                return 1
            token = get_access_token(appid, secret)
            raw = fetch_articles_raw(token, source, max_n)
    except (WxError, TikhubError) as e:
        log.error("%s", e)
        return 1
    except Exception as e:
        log.error("拉取失败：%s", e)
        return 1

    if not raw:
        log.error("未拉到任何文章；保留现有 articles.json 不动。"
                  "（核对：账号是否已发布图文 / 接口权限 / WX_ARTICLE_SOURCE）")
        return 1

    existing = load_existing(out_path) if incremental else None
    articles = build_articles(raw, web_root, download_covers, default_cat,
                              load_overrides(), max_n, existing=existing)
    payload = {
        "updated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "articles": articles,
    }

    if args.dry_run:
        log.info("DRY-RUN：共 %d 篇，预览前 5 篇 ↓", len(articles))
        for a in articles[:5]:
            log.info("  [%s]%s %s  →  %s", a["category"],
                     "（置顶）" if a["pinned"] else "", a["title"], a["url"] or "(无链接)")
        return 0

    write_json_atomic(out_path, payload)
    log.info("✓ 已写入 %s（%d 篇，置顶 %d 篇）", out_path, len(articles),
             sum(1 for a in articles if a["pinned"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
