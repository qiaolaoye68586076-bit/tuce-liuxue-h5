/* =========================================================
   途策留学 H5 — experience.js（Ignite 风）
   ① 磁性 CTA（精确指针 + GSAP）
   ② 学员之声：滚动剥卡（移植 Ignite 真实源码 testimonials.ts 机制——
      跑道高 = (卡数+1)×视口高，sticky 钉住，每卡独占一个视口高的
      scrub 段，向上飞出并转向随机终角；初始角≈终角的一成手感）
      回退（reduced-motion / 无 ScrollTrigger）→ 点击/回车轮换便签
   reveal 由 main.js 的 IO + CSS 过渡负责；跑马灯为纯 CSS。
   ========================================================= */
(function () {
  'use strict';

  var reduced = !!(window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  var finePointer = !!(window.matchMedia &&
    window.matchMedia('(hover:hover) and (pointer:fine)').matches);
  var hasGsap = typeof window.gsap !== 'undefined';

  /* ---------- 磁性按钮 ---------- */
  if (!reduced && finePointer && hasGsap) {
    document.querySelectorAll('[data-magnetic]').forEach(function (btn) {
      var sx = gsap.quickTo(btn, 'x', { duration: 0.4, ease: 'power3' });
      var sy = gsap.quickTo(btn, 'y', { duration: 0.4, ease: 'power3' });
      btn.addEventListener('pointermove', function (e) {
        var r = btn.getBoundingClientRect();
        sx((e.clientX - r.left - r.width / 2) * 0.22);
        sy((e.clientY - r.top - r.height / 2) * 0.3);
      });
      btn.addEventListener('pointerleave', function () { sx(0); sy(0); });
    });
  }

  /* ---------- 学员之声 ---------- */
  var voices = document.getElementById('voices');
  var stack = document.getElementById('voicesStack');
  if (!voices || !stack) return;
  var cards = Array.prototype.slice.call(stack.querySelectorAll('.vcard'));

  var canPeel = !reduced && cards.length > 1 && hasGsap &&
    typeof window.ScrollTrigger !== 'undefined';

  if (canPeel) {
    /* —— 滚动剥卡（原版机制 1:1） —— */
    gsap.registerPlugin(ScrollTrigger);
    voices.classList.add('voices--scroll');

    var vh = function () { return window.innerHeight; };
    var setRunway = function () {
      voices.style.height = ((cards.length + 1) * vh()) + 'px';
    };
    setRunway();

    var seeds = [-1.5, 4, -6];            // 初始便签小角度（设计预设）
    cards.slice().reverse().forEach(function (card, i) {
      var seed = seeds[i % seeds.length];
      var finalRot = (seed < 0 ? -1 : 1) * gsap.utils.random(24, 42);
      gsap.set(card, { rotation: seed });
      gsap.to(card, {
        y: function () { return -vh() * 1.15; },
        rotation: finalRot,
        ease: 'none',
        scrollTrigger: {
          trigger: voices,
          start: function () { return 'top+=' + (i * vh()) + ' top'; },
          end: function () { return 'top+=' + ((i + 1) * vh()) + ' top'; },
          scrub: true,
          invalidateOnRefresh: true
        }
      });
    });

    var rT;
    window.addEventListener('resize', function () {
      clearTimeout(rT);
      rT = setTimeout(function () { setRunway(); ScrollTrigger.refresh(); }, 200);
    }, { passive: true });
  } else {
    /* —— 回退：点击/回车轮换便签 —— */
    var busy = false;
    var cycle = function () {
      if (busy || cards.length < 2) return;
      busy = true;
      var top = cards.filter(function (c) { return c.dataset.pos === '0'; })[0];
      var delay = reduced ? 0 : 240;
      if (!reduced && top) top.classList.add('fly');
      setTimeout(function () {
        cards.forEach(function (c) {
          c.dataset.pos = String((parseInt(c.dataset.pos, 10) + 2) % 3);
        });
        if (top) top.classList.remove('fly');
        busy = false;
      }, delay);
    };
    stack.addEventListener('click', cycle);
    stack.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); cycle(); }
    });
  }
})();
