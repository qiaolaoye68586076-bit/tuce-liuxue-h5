with open('frontend/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

old_mobile_faq = """@media (max-width:768px){
  .faq__q{ padding:20px 16px 20px 18px; font-size:16.5px; gap:12px; }
  .faq__q::before{ width:24px; font-size:12px; margin-top:2px; }
  .faq__q[aria-expanded="true"]{ padding-bottom:12px; }
  .faq__icon{ width:30px; height:30px; padding:7px; }
  .faq__a-inner{ margin:0 18px; padding:14px 0 22px; }
  .faq__a p{ font-size:15px; }
}"""

new_mobile_faq = """@media (max-width:768px){
  .faq__q{ padding:18px 12px 18px 14px; font-size:14.5px; gap:8px; }
  .faq__q::before{ width:20px; font-size:11px; margin-top:1px; }
  .faq__q[aria-expanded="true"]{ padding-bottom:12px; }
  .faq__icon{ width:26px; height:26px; padding:5px; }
  .faq__a-inner{ margin:0 14px; padding:12px 0 20px; }
  .faq__a p{ font-size:14px; line-height:1.7; }
}"""

if old_mobile_faq in css:
    css = css.replace(old_mobile_faq, new_mobile_faq)
    with open('frontend/css/style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("FAQ mobile css updated.")
else:
    print("Could not find the exact old mobile FAQ block.")
