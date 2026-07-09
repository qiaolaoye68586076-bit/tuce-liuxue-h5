with open('frontend/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Fix the mobile adjustments block
old_mobile = """/* Mobile adjustments */
@media (max-width: 767px) {
  .svc-row__content { padding: 40px 24px; }
  .svc-row h3 { font-size: 28px; }
  .svc-row__visual { min-height: 260px; }
  .svc-row__arch { width: 220px; height: 300px; bottom: -10px; }
  .svc-row--us .svc-row__visual img { height: 110%; margin-bottom: -10px; }
}"""

new_mobile = """/* Mobile adjustments */
@media (max-width: 767px) {
  .svc-row__content { padding: 40px 24px; }
  .svc-row h3 { font-size: 28px; }
  /* 固定高度，防止内部 img 按原图比例被无限拉长 */
  .svc-row__visual { height: 260px; min-height: auto; }
  .svc-row__arch { width: 220px; height: 300px; bottom: -10px; }
  .svc-row--us .svc-row__visual img { height: 110%; margin-bottom: -10px; }
}"""

# Fix desktop img height to absolute 100% of parent instead of 95% which can be weird
old_img = """.svc-row__visual img {
  position: relative;
  z-index: 2;
  height: 95%;
  width: auto;
  object-fit: contain;
  object-position: bottom center;
  transition: transform 0.6s var(--ease);
}"""

new_img = """.svc-row__visual img {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  margin: 0 auto;
  z-index: 2;
  height: 95%;
  width: 100%;
  object-fit: contain;
  object-position: bottom center;
  transition: transform 0.6s var(--ease);
}"""

if old_mobile in css:
    css = css.replace(old_mobile, new_mobile)
else:
    print("Could not find old mobile css")
    
if old_img in css:
    css = css.replace(old_img, new_img)
else:
    print("Could not find old img css")

with open('frontend/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("CSS updated")
