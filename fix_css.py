import re

with open('frontend/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Make desktop QRs smaller
css = css.replace('.qr{\n  width:108px; height:108px;', '.qr{\n  width:84px; height:84px;')
css = css.replace('.qr--sm{ width:108px; height:108px; }', '.qr--sm{ width:84px; height:84px; }')

with open('frontend/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("CSS updated")
