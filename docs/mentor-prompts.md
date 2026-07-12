# 师资头像 — AI 出图提示词（Route A · 品牌同色）

电影感极简 + 途策品牌色（深森林绿 #14342B → 暖金 #C2A15B）。
4 张共用同一 style base + 同一 seed/风格，只改人物描述，保证师资栅格统一。

输出：原图可出 3:4 / 9:16，再**居中裁成 256×256**（保头部安全区）；
命名 `mentor-01.jpg`…`mentor-04.jpg` 放进 `assets/`，与现有 `<img src>` 一一对应。
jpg 质量 80，单张 ≤120KB。

---

## 通用风格基底（每条必加）

> Cinematic minimal editorial portrait, square 1:1, single dominant subject centered,
> symmetrical composition, head-and-shoulders to upper-chest framing.
> Intense deep-forest-green-to-antique-gold gradient environment (#14342B → #C2A15B),
> strong silhouette/rim lighting, deep shadow contrast, glossy reflective floor with a
> soft mirrored reflection below. Clean edges, minimal visual noise, controlled negative
> space. Fashion-editorial sense of drama. Premium, graphic, modern — not busy or
> over-rendered. Photorealistic, 85mm, shallow depth of field. No text, no logos.

---

## ① mentor-01.jpg — 规划导师（哈佛 · 升学战略）
A poised man in his late 30s, strategic and authoritative presence, short neat dark hair,
dark tailored blazer, calm confident gaze toward camera. Strong rim light carving his
silhouette against the gradient. + 通用风格基底

## ② mentor-02.jpg — 文书导师（耶鲁 · 文书共创）
A thoughtful woman in her early 30s, literary and warm, soft shoulder-length hair, fine
knit / blazer, gentle creative expression. Silhouette edge-lit, symmetrical, mirrored on
the glossy floor. + 通用风格基底

## ③ mentor-03.jpg — 个性化导师（斯坦福 · 背景提升）
An energetic person in their early 30s, innovative and approachable, modern smart-casual
dark sweater, bright curious eyes. Dramatic rim light, clean graphic silhouette, minimal
noise. + 通用风格基底

## ④ mentor-04.jpg — 学术导师（MIT · 理工方向）
A composed man in his 40s, scholarly and precise, fine-rimmed glasses, sharp charcoal
blazer, analytical calm expression. Strong silhouette lighting, deep shadow contrast,
symmetrical premium framing. + 通用风格基底

---

## 出图注意
- 统一性 > 戏剧性：4 张渐变方向、反光地面、打光角度保持一致。
- 可读性：脸部别落进死黑阴影，silhouette 重点在轮廓边缘光，面部仍留细节。
- 若用 AI 虚拟人物，建议页脚注明"配图为示意"。
