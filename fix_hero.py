with open('frontend/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

old_mobile = """@media (max-width: 600px) {
  .hero--light .hero-bg { background-position: 74% center; }
  .hero--light .hero-overlay {
    background: linear-gradient(180deg,
      rgba(250, 247, 240, 0.55) 0%,
      rgba(250, 247, 240, 0.90) 78%);
  }
}

@media (max-width: 600px) {
  /* —— 窄屏改居中构图：桌面的左轴版式在手机上（建筑被遮罩盖住）失去右侧配重，
        文字左对齐 + 按钮通栏会显得头重脚轻；单轴对称是窄屏最稳的平衡 —— */
  .hero-content,
  .hero--light .hero-content {
    align-items: center;
    text-align: center;
    padding: 0 24px clamp(32px, 7vh, 56px);
  }
  .hero-eyebrow { font-size: 11px; letter-spacing: 0.22em; }
  .hero--light .hero-title-line1 { font-size: clamp(22px, 6.4vw, 28px); }
  .hero--light .hero-title-line2 { font-size: clamp(44px, 13vw, 58px); margin-top: 6px; }
  .hero-brand-row { flex-direction: column; align-items: center; gap: 10px; margin-top: 24px; }
  .hero-body { max-width: 21em; font-size: 14px; line-height: 1.9; }
  .hero-body br { display: none; }   /* 桌面的手动断行在窄屏造成参差空行 */
  .hero-cta-group {
    flex-direction: column;
    width: 100%;
    max-width: 320px;   /* 不通栏：收窄居中，让按钮组成为构图的「基座」而非满宽色块 */
    gap: 11px;
    margin-top: 40px;
  }
  .hero-cta-primary,
  .hero-cta-secondary {
    width: 100%;
    justify-content: center;
  }
  .hero-cta-primary { padding-left: 9px; }   /* 居中构图下对称 padding，内容才是光学居中 */
  .hero--light .hero-footnote { justify-content: center; margin-top: 22px; }
  .hero-divider__line { width: 40px; }
}"""

new_mobile = """@media (max-width: 600px) {
  /* —— 移动端高级编辑感构图 ——
     背景图让出上半屏幕，文字压沉底端，左对齐，去除非必要的遮罩阻挡
     ========================================================= */
  .hero--light .hero-bg { 
    background-position: 50% 0%; 
    background-size: cover;
  }
  .hero--light .hero-overlay {
    background: linear-gradient(180deg,
      rgba(250, 247, 240, 0) 0%,
      rgba(250, 247, 240, 0.4) 30%,
      rgba(250, 247, 240, 0.95) 55%,
      rgba(250, 247, 240, 1) 100%);
  }
}

@media (max-width: 600px) {
  .hero-content,
  .hero--light .hero-content {
    align-items: flex-start;
    text-align: left;
    justify-content: flex-end; /* 将文字压到底部 */
    padding: 0 24px 64px;
  }
  
  .hero-eyebrow { 
    font-size: 12px; 
    letter-spacing: 0.18em; 
    color: var(--gold) !important;
    font-weight: 700;
  }
  
  /* 优化移动端标题字体排印：不再过度放纵字号，紧凑而有张力 */
  .hero--light .hero-title-line1 { 
    font-size: clamp(24px, 7vw, 30px); 
    line-height: 1.2;
    margin-top: 16px;
    opacity: 0.9;
  }
  .hero--light .hero-title-line2 { 
    font-size: clamp(38px, 10.5vw, 48px); 
    line-height: 1.1; 
    margin-top: 6px; 
    letter-spacing: -0.04em;
  }
  
  .hero-brand-row { 
    flex-direction: column; 
    align-items: flex-start; 
    gap: 16px; 
    margin-top: 32px; 
  }
  .hero-body { 
    max-width: 100%; 
    font-size: 15px; 
    line-height: 1.8; 
    color: #444; 
    font-weight: 400;
  }
  .hero-body br { display: none; }
  
  .hero-cta-group {
    flex-direction: column;
    width: 100%;
    max-width: 100%;
    gap: 16px;
    margin-top: 44px;
  }
  
  .hero-cta-primary,
  .hero-cta-secondary {
    width: 100%;
    justify-content: center;
    height: 56px; /* 更高级的加大尺寸触摸区 */
    font-size: 16px;
    border-radius: 28px;
  }
  .hero-cta-primary { padding-left: 0; }
  
  .hero--light .hero-footnote { 
    justify-content: flex-start; 
    margin-top: 28px; 
    font-size: 13px;
    opacity: 0.8;
  }
}"""

if old_mobile in css:
    css = css.replace(old_mobile, new_mobile)
    with open('frontend/css/style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Mobile Hero CSS updated successfully.")
else:
    print("Could not find the exact old mobile CSS block!")
