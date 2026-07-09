with open('frontend/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
match = re.search(r'\.footer\s*\{.*?(?=\/\* =========================================================|\Z)', css, re.DOTALL)
if match:
    print(match.group(0))
else:
    print("Not found")
