# 三士渡 (stoooges.com) — design DNA, distilled

Curated from the raw token dump in [design-tokens.md](design-tokens.md). The raw
report is **polluted by the iView/View-UI Vue framework** baked into
`chunk-vendors.css` (its default blues/reds/greens/greys). Below is the *real*
brand system, mined from their own `app.css` only.

> ⚠️ Study the **system**, not the assets. 三士渡 is a direct competitor — do
> not copy their images, copy, logo, or fonts files into our commercial site.
> See ../DESIGN-BRIEF.md.

## 1. Palette — radical minimalism + one electric accent
| Role | Value | Note |
|---|---|---|
| Ink / text | `#000000` | near-pure black |
| Paper | `#ffffff` | pure white, lots of it |
| Hairline / fill | `#eeeeee` | the only grey |
| **Accent** | **`#1230b3`** (≈`#1230b8`) | electric cobalt — used sparingly |

The whole brand is **black + white + one bold blue**. Restraint *is* the luxury.

## 2. Type system
- **Fonts:** `OPPOSans-M` / `OPPOSans-B` (CJK), `HelveticaNowText` (Latin body),
  `AvenirNextLTProBold` + `Lobster` (display accents). All self-hosted `@font-face`.
- **Fluid `vw` scale** on a **1900px design width**:
  | token | ≈ px @1900 | role |
  |---|---|---|
  | `.736842vw` | 14px | body (most common) |
  | `.842105vw` | 16px | secondary |
  | `.947368vw` | 18px | lead |
  | `1.052632vw` | 20px | subhead |
  | `5.263158vw` | 100px | hero display |
- **Line-height** generous & editorial: body ≈ **1.68**, headings ≈ 1.05–1.26.
- **Letter-spacing** essentially `0` — they let the premium font breathe instead.

## 3. Motion & shape
- Minimal radii, hairline borders, sparing shadows — flat, paper-like.
- Reveal-on-scroll choreography (Vue + swiper carousels for case galleries).

---

## 4. How this maps to `tuce` — we're already aligned
| Principle | 三士渡 | tuce (current) | Verdict |
|---|---|---|---|
| Restrained palette | B/W + 1 cobalt | forest-green + gold + cream | ✅ both disciplined |
| Serif/sans pairing | OPPO Sans + Helvetica | Fraunces + Noto | ✅ intentional |
| Fluid type | raw `vw` @1900 | modern `clamp()` | ✅ tuce's is *more* robust |
| Editorial line-height | 1.68 body | 1.75 body | ✅ |
| Texture | flat paper | flat + paper-grain noise | ✅ tuce adds atmosphere |

**Do NOT adopt:** their cobalt `#1230b3` (off-brand for us), their `vw`-based
type (our `clamp()` is better), or their font files (licensing + brand).

## 5. Transferable lessons (optional refinements for tuce)
1. **Bigger hero display.** They go to ~100px; a bolder hero headline reads more
   premium. We could push the hero title clamp ceiling up.
2. **Even more negative space** around section heads (they lean very airy).
3. **Tighter accent discipline** — gold only on true CTAs / key numbers, never decorative.
4. **A single signature display accent** (like their Lobster moment) — for us that
   could be an italic Fraunces flourish on one hero word.

These are *enhancements to an already on-brand system*, not fixes.

---

## 6. Rendered view — corrections from the actual page
Captured via Playwright (`rendered.html` / `rendered-text.txt` / `rendered-fullpage.png`).
The CSS-only read was **partly wrong** — the real aesthetic is warmer than "austere minimal":

- **Hero:** huge black **serif wordmark "STOOOGES"** on pure white, an eyebrow in
  parentheses「（选择三士渡，人生不迷路）」, and a one-line English mission
  "We do education. We redefine education." → confirms the **big-hero** lesson. ✅
- **Not austere — playful.** The page is clean white but covered in **bright flat
  illustrations** (paper planes, books, hearts, students). Color comes from the
  *illustrations*, not flat color fields. The cobalt `#1230b3` is mainly a UI accent.
  → This is a *different* lane from tuce's forest-green editorial luxury; don't chase it.
- **Section structure** (from rendered text):
  1. Hero · 2. **Feature 我们的特点** (最牛的团队 / 多对一模式 / 人性化服务 / 个性化申请)
  · 3. **Process 我们的流程** — 17 numbered steps across 规划期 / 申请季 / 后申请季
  · 4. **Contact 联系我们** form · 5. Footer (8 city addresses, 400 line, email, QR).
- **Form fields nearly identical to tuce:** 姓名 / 咨询方向(必填) / 电话 / 微信 /
  所在学校 / 居住城市 / 更多信息 → validates tuce's lead-form design. ✅
- **Transferable structural idea:** their **numbered multi-step Process** is more
  detailed than tuce's 6-step flow — if you want depth, tuce could expand its
  申请流程 with sub-grouping (规划期/申请季/后申请季), in *your* style.

### ✅ Per-section screenshots (resolved)
The site is built with **fullpage.js** (`.fullpage-wrapper` + 10 × `.fp-section`,
each a 100vh panel revealed by a translateY transform, with per-section entrance
animations). The default full-page screenshot only caught the hero. Fixed by
driving fullpage's own API — `python3 scrape_reference.py --slides` now walks
`fullpage_api.moveTo(i)` and shoots each panel with content animated in:
`reference/stoooges/section-01…10.png`.

The 10 sections: 01 Hero (STOOOGES wordmark) · 02 我们的特点 · 03 多对一模式
(CROWDSOURCING) · 04 人性化服务 · 05 个性化申请 · 06 我们的流程 (Process) ·
07–08 录取墙 (**wall of university crests** — note: 校徽 are trademarks; tuce
should keep text Offers, per DESIGN-BRIEF) · 09 联系我们 · 10 footer.
