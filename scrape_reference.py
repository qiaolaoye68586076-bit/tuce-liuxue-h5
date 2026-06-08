#!/usr/bin/env python3
"""
scrape_reference.py — design-DNA scraper for stoooges.com/web/

Downloads the reference landing page's HTML, CSS and JS into reference/stoooges/,
records an asset manifest, then distills a design-token report
(colors / type / spacing / radius / shadow / transitions) into
reference/design-tokens.md.

Goal: study the design SYSTEM (re-implement the style in our own brand),
NOT to copy proprietary images / copy / logos. See DESIGN-BRIEF.md.

Usage:
  python3 scrape_reference.py                # static scrape + token report
  python3 scrape_reference.py --render       # ALSO render the SPA via Playwright
  python3 scrape_reference.py --no-robots    # skip robots.txt check (study only)
  python3 scrape_reference.py --base URL     # override the target URL

Best practices folded in from the crawling guide:
  - robots.txt compliance (urllib.robotparser)
  - retry + exponential backoff on 5xx / connection errors
  - polite rate limiting (jittered delay between requests)
  - persistent Session + realistic User-Agent
  - class-based structure
Playwright (optional, for JS-rendered DOM):
  pip install playwright && playwright install chromium
"""

import argparse
import collections
import logging
import os
import random
import re
import time
import urllib.parse as up
import urllib.robotparser as robotparser

import requests
from bs4 import BeautifulSoup

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
log = logging.getLogger("scrape")

ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BASE = "https://stoooges.com/web/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


# ======================================================== token-mining helpers
HEX = re.compile(r'#[0-9a-fA-F]{3,8}\b')
RGB = re.compile(r'rgba?\([^)]*\)', re.I)
HSL = re.compile(r'hsla?\([^)]*\)', re.I)
FONT_FAMILY = re.compile(r'font-family\s*:\s*([^;{}]+)', re.I)
FONT_SIZE = re.compile(r'font-size\s*:\s*([0-9.]+(?:px|rem|em|vw|%))', re.I)
LINE_HEIGHT = re.compile(r'line-height\s*:\s*([0-9.]+(?:px|rem|em|%)?)', re.I)
LETTER_SP = re.compile(r'letter-spacing\s*:\s*(-?[0-9.]+(?:px|rem|em)?)', re.I)
RADIUS = re.compile(r'border-radius\s*:\s*([^;{}]+)', re.I)
SHADOW = re.compile(r'box-shadow\s*:\s*([^;{}]+)', re.I)
TRANSITION = re.compile(r'transition(?:-duration)?\s*:\s*([^;{}]+)', re.I)
PX = re.compile(r'\b([0-9]{1,3}(?:\.[0-9]+)?)px\b')
REM = re.compile(r'\b([0-9]+(?:\.[0-9]+)?)rem\b')
MEDIA = re.compile(r'@media[^{]+\(([^)]*(?:width|height)[^)]*)\)', re.I)
URL_REF = re.compile(r'url\(\s*[\'"]?([^\'")]+)[\'"]?\s*\)', re.I)
FONTFACE = re.compile(r'@font-face\s*{[^}]*}', re.I)


def norm_color(c):
    c = c.strip().lower()
    if c.startswith('#') and len(c) == 4:  # #abc -> #aabbcc
        c = '#' + ''.join(ch * 2 for ch in c[1:])
    return c


def top(counter, n=30):
    return counter.most_common(n)


def new_tokens():
    return {k: collections.Counter() for k in (
        "colors", "font_families", "font_sizes", "line_heights", "letter_spacing",
        "radius", "shadow", "transition", "px", "rem", "media")} | {"fontface": []}


def mine(css_text, t):
    """Accumulate design tokens from one CSS string into t."""
    for m in HEX.findall(css_text):
        t["colors"][norm_color(m)] += 1
    for rx in (RGB, HSL):
        for m in rx.findall(css_text):
            t["colors"][re.sub(r'\s+', '', m.lower())] += 1
    for m in FONT_FAMILY.findall(css_text):
        t["font_families"][m.strip().strip('"\'')] += 1
    for m in FONT_SIZE.findall(css_text):
        t["font_sizes"][m.strip()] += 1
    for m in LINE_HEIGHT.findall(css_text):
        t["line_heights"][m.strip()] += 1
    for m in LETTER_SP.findall(css_text):
        t["letter_spacing"][m.strip()] += 1
    for m in RADIUS.findall(css_text):
        t["radius"][m.strip()[:40]] += 1
    for m in SHADOW.findall(css_text):
        t["shadow"][m.strip()[:80]] += 1
    for m in TRANSITION.findall(css_text):
        t["transition"][m.strip()[:60]] += 1
    for m in PX.findall(css_text):
        t["px"][m + "px"] += 1
    for m in REM.findall(css_text):
        t["rem"][m + "rem"] += 1
    for m in MEDIA.findall(css_text):
        t["media"][re.sub(r'\s+', '', m)] += 1
    t["fontface"].extend(FONTFACE.findall(css_text))
    return t


# =============================================================== the scraper
class ReferenceScraper:
    def __init__(self, base, *, obey_robots=True,
                 min_delay=0.8, max_delay=2.0, max_retries=3):
        self.base = base
        self.out = os.path.join(ROOT, "reference", "stoooges")
        self.report = os.path.join(ROOT, "reference", "design-tokens.md")
        self.obey_robots = obey_robots
        self.min_delay, self.max_delay = min_delay, max_delay
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self._first = True
        self.robots = self._load_robots() if obey_robots else None

    # ---- politeness ------------------------------------------------------
    def _load_robots(self):
        robots_url = up.urljoin(self.base, "/robots.txt")
        rp = robotparser.RobotFileParser()
        try:
            txt = self.session.get(robots_url, timeout=15)
            if txt.status_code == 200:
                rp.parse(txt.text.splitlines())
                log.info("robots.txt loaded from %s", robots_url)
            else:
                log.info("no robots.txt (%s) — assuming allowed", txt.status_code)
                rp = None
        except requests.RequestException as e:
            log.warning("robots.txt fetch failed (%s) — assuming allowed", e)
            rp = None
        return rp

    def _allowed(self, url):
        if not self.obey_robots or self.robots is None:
            return True
        return self.robots.can_fetch(HEADERS["User-Agent"], url)

    def _pause(self):
        if self._first:
            self._first = False
            return
        time.sleep(random.uniform(self.min_delay, self.max_delay))

    # ---- fetch with retry/backoff ---------------------------------------
    def fetch(self, url, binary=False):
        if not self._allowed(url):
            raise PermissionError(f"robots.txt disallows {url}")
        self._pause()
        last = None
        for attempt in range(1, self.max_retries + 1):
            try:
                log.info("GET %s (try %d)", url, attempt)
                r = self.session.get(url, timeout=30, allow_redirects=True)
                if r.status_code >= 500:
                    raise requests.HTTPError(f"server {r.status_code}")
                r.raise_for_status()
                return r.content if binary else r.text
            except requests.RequestException as e:
                last = e
                backoff = 2 ** (attempt - 1) + random.uniform(0, 0.5)
                log.warning("  fail (%s) — backoff %.1fs", e, backoff)
                time.sleep(backoff)
        raise last

    # ---- io --------------------------------------------------------------
    @staticmethod
    def _safe_name(url):
        name = os.path.basename(up.urlparse(url).path) or "index"
        if not os.path.splitext(name)[1]:
            name += ".html"
        return name

    @staticmethod
    def save(path, data):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if isinstance(data, bytes):
            with open(path, "wb") as f:
                f.write(data)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(data)
        log.info("saved %s (%d bytes)", os.path.relpath(path, ROOT), len(data))

    # ---- main static flow ------------------------------------------------
    def scrape_static(self):
        os.makedirs(self.out, exist_ok=True)
        html = self.fetch(self.base)
        self.save(os.path.join(self.out, "index.html"), html)
        soup = BeautifulSoup(html, "html.parser")

        css_urls = [up.urljoin(self.base, l["href"]) for l in
                    soup.find_all("link", rel=lambda v: v and "stylesheet" in v)
                    if l.get("href")]
        js_urls = [up.urljoin(self.base, s["src"]) for s in soup.find_all("script", src=True)]
        img_urls = [up.urljoin(self.base, im["src"]) for im in soup.find_all("img", src=True)]

        tokens = new_tokens()
        asset_refs = set(img_urls)

        for u in css_urls:
            try:
                css = self.fetch(u)
            except Exception as e:
                log.warning("css fail %s: %s", u, e)
                continue
            self.save(os.path.join(self.out, "css", self._safe_name(u)), css)
            mine(css, tokens)
            for ref in URL_REF.findall(css):
                if not ref.startswith("data:"):
                    asset_refs.add(up.urljoin(u, ref))

        for u in js_urls:
            try:
                js = self.fetch(u)
            except Exception as e:
                log.warning("js fail %s: %s", u, e)
                continue
            self.save(os.path.join(self.out, "js", self._safe_name(u)), js)
            for m in HEX.findall(js):
                tokens["colors"][norm_color(m)] += 1
            for ref in URL_REF.findall(js):
                if not ref.startswith("data:"):
                    asset_refs.add(up.urljoin(u, ref))

        self.write_report(tokens, css_urls, js_urls, sorted(asset_refs))
        log.info("STATIC DONE — report at %s", os.path.relpath(self.report, ROOT))

    # ---- optional Playwright render (JS-rendered DOM) --------------------
    def render(self, sections=False):
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            log.error("Playwright not installed. Enable render mode with:\n"
                      "  pip install playwright\n  playwright install chromium")
            return
        os.makedirs(self.out, exist_ok=True)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1920, "height": 1080},
                                    user_agent=HEADERS["User-Agent"])
            log.info("rendering %s via Chromium…", self.base)
            page.goto(self.base, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(2500)  # let Vue hydrate + lazy content settle
            self.save(os.path.join(self.out, "rendered.html"), page.content())
            self.save(os.path.join(self.out, "rendered-text.txt"), page.inner_text("body"))
            shot = os.path.join(self.out, "rendered-fullpage.png")
            os.makedirs(self.out, exist_ok=True)
            page.screenshot(path=shot, full_page=True)
            log.info("saved %s (full-page screenshot)", os.path.relpath(shot, ROOT))
            if sections:
                self._capture_sections(page, self.out)
            browser.close()
        log.info("RENDER DONE")

    # ---- per-section screenshots (fullpage.js SPA) ----------------------
    def _capture_sections(self, page, out, max_sections=30):
        """The page is fullpage.js — sections are `.fp-section` panels revealed
        one at a time by a translateY transform, with per-section entrance
        animations. Drive it via its own `fullpage_api.moveTo(i)` (falling back
        to ArrowDown) so each section's content animates in, then screenshot the
        active viewport."""
        n = page.evaluate("() => document.querySelectorAll('.fp-section').length")
        if not n:
            log.warning("no fullpage sections found — skipping per-section capture")
            return []
        n = min(n, max_sections)
        has_api = page.evaluate(
            "() => typeof window.fullpage_api === 'object' && !!window.fullpage_api")
        log.info("found %d fullpage sections (api=%s) — walking…", n, has_api)

        vw = page.viewport_size
        page.mouse.move(vw["width"] // 2, vw["height"] // 2)
        saved = []
        for i in range(1, n + 1):
            moved = False
            if has_api:
                try:
                    page.evaluate("(i) => window.fullpage_api.moveTo(i)", i)  # 1-indexed
                    moved = True
                except Exception as e:
                    log.warning("moveTo(%d) failed: %s", i, e)
            if not moved:
                page.keyboard.press("Home" if i == 1 else "ArrowDown")
            page.wait_for_timeout(1300)  # transition + entrance animations settle
            path = os.path.join(out, f"section-{i:02d}.png")
            page.screenshot(path=path)
            saved.append(path)
            log.info("saved %s", os.path.relpath(path, ROOT))
        log.info("captured %d section screenshots", len(saved))
        return saved

    # ---- report ----------------------------------------------------------
    def write_report(self, t, css_urls, js_urls, assets):
        def section(title, pairs, fmt="`{0}`  ×{1}"):
            out = [f"\n### {title}\n"]
            if not pairs:
                out.append("_(none found)_\n")
            out += ["- " + fmt.format(k, v) for k, v in pairs]
            return "\n".join(out) + "\n"

        L = ["# stoooges.com — design-token report",
             "\n> Auto-extracted from compiled CSS/JS for **design study**. "
             "Re-implement the *style* in our own brand & assets — do not copy "
             "proprietary images / copy / logos. See ../DESIGN-BRIEF.md.\n",
             "> ⚠️ Counts are polluted by the iView/View-UI vendor framework. "
             "For the de-noised brand DNA see **design-summary.md**.\n",
             f"- Source: {self.base}",
             f"- CSS files: {len(css_urls)}  |  JS files: {len(js_urls)}  |  "
             f"asset refs: {len(assets)}"]
        L.append(section("Colors (by frequency)", top(t['colors'], 40)))
        L.append(section("Font families", top(t['font_families'], 15)))
        L.append(section("Font sizes", top(t['font_sizes'], 25)))
        L.append(section("Line heights", top(t['line_heights'], 15)))
        L.append(section("Letter spacing", top(t['letter_spacing'], 15)))
        L.append(section("Border radius", top(t['radius'], 15)))
        L.append(section("Box shadows", top(t['shadow'], 15)))
        L.append(section("Transitions", top(t['transition'], 15)))
        L.append(section("Spacing — px values", top(t['px'], 35)))
        L.append(section("Spacing — rem values", top(t['rem'], 25)))
        L.append(section("Breakpoints (@media)", top(t['media'], 15)))
        L.append("\n### @font-face blocks\n")
        if t["fontface"]:
            L += ["```css", *t["fontface"][:10], "```"]
        else:
            L.append("_(none found)_")
        L.append("\n### Asset references (NOT downloaded — study only)\n")
        L += [f"- {a}" for a in assets[:120]]
        self.save(self.report, "\n".join(L))


def main():
    ap = argparse.ArgumentParser(description="Design-DNA scraper for a reference site")
    ap.add_argument("--base", default=DEFAULT_BASE, help="target URL")
    ap.add_argument("--render", action="store_true", help="also render SPA via Playwright")
    ap.add_argument("--slides", action="store_true",
                    help="render + screenshot every section (swiper walk)")
    ap.add_argument("--no-robots", action="store_true", help="skip robots.txt check")
    args = ap.parse_args()

    s = ReferenceScraper(args.base, obey_robots=not args.no_robots)
    s.scrape_static()
    if args.slides:
        s.render(sections=True)
    elif args.render:
        s.render()


if __name__ == "__main__":
    main()
