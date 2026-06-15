/* =========================================================
   途策留学 H5 — experience.js
   金色航线 The Gilded Route · 体验编排层（渐进增强）
   开场幕 / 自定义光标 / 星座画布 / 航线轨 / GSAP 编舞
   依赖：gsap + ScrollTrigger（本地 vendor，缺失时全部优雅降级）
   ========================================================= */
(function () {
  'use strict';

  var doc = document.documentElement;
  var reduced = !!(window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  var finePointer = !!(window.matchMedia &&
    window.matchMedia('(hover:hover) and (pointer:fine)').matches);
  var hasGsap = typeof window.gsap !== 'undefined';
  var hasST = hasGsap && typeof window.ScrollTrigger !== 'undefined';
  if (hasST) gsap.registerPlugin(ScrollTrigger);

  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };

  /* =====================================================
     1. 开场幕（纯 vanilla，sessionStorage 跳过，CSS 自动兜底）
     ===================================================== */
  var preDone = false;
  var preListeners = [];
  function firePreDone() {
    if (preDone) return;
    preDone = true;
    preListeners.forEach(function (fn) { fn(); });
  }
  function onPreDone(fn) { preDone ? fn() : preListeners.push(fn); }

  (function preloader() {
    var pre = $('#pre');
    var skipped = doc.classList.contains('skip-pre');
    if (!pre || skipped || reduced) {
      if (pre && pre.parentNode && (skipped || reduced)) pre.parentNode.removeChild(pre);
      firePreDone();
      return;
    }
    try { sessionStorage.setItem('tuce_voyage', '1'); } catch (e) {}

    var count = $('#preCount');
    var t0 = null, DUR = 1050;
    function tick(ts) {
      if (!t0) t0 = ts;
      var p = clamp((ts - t0) / DUR, 0, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      if (count) count.textContent = String(Math.round(eased * 100)).padStart(2, '0');
      if (p < 1) requestAnimationFrame(tick);
      else {
        pre.classList.add('pre--done');
        setTimeout(function () {
          if (pre.parentNode) pre.parentNode.removeChild(pre);
        }, 1100);
        setTimeout(firePreDone, 320); // 幕布开启即入场，衔接更紧
      }
    }
    requestAnimationFrame(tick);
  })();

  /* =====================================================
     2. 自定义光标（精确指针 + 非减弱动效）
     ===================================================== */
  (function cursor() {
    if (!finePointer || reduced) return;
    var dot = $('#cur'), ring = $('#curRing');
    if (!dot || !ring) return;
    doc.classList.add('has-cursor');
    var label = ring.querySelector('.cur-ring__label');

    var mx = innerWidth / 2, my = innerHeight / 2;
    var rx = mx, ry = my;
    document.addEventListener('pointermove', function (e) {
      mx = e.clientX; my = e.clientY;
      dot.style.transform = 'translate(' + mx + 'px,' + my + 'px) translate(-50%,-50%)';
    }, { passive: true });

    (function loop() {
      rx += (mx - rx) * 0.16;
      ry += (my - ry) * 0.16;
      ring.style.transform = 'translate(' + rx + 'px,' + ry + 'px) translate(-50%,-50%)';
      requestAnimationFrame(loop);
    })();

    var LINK_SEL = 'a, button, .btn, .stat-card, .card, .feat, .offer-item, .mentor, .story, input, select, textarea, label.agree';
    document.addEventListener('pointerover', function (e) {
      var drag = e.target.closest('[data-cursor="drag"]');
      if (drag) {
        ring.classList.add('is-drag'); ring.classList.remove('is-link');
        if (label) label.textContent = '滑动';
        return;
      }
      if (e.target.closest(LINK_SEL)) {
        ring.classList.add('is-link'); ring.classList.remove('is-drag');
      } else {
        ring.classList.remove('is-link', 'is-drag');
      }
    }, { passive: true });
  })();

  /* =====================================================
     3. 星座画布（学校星图 + 航线 + 彗星）
     ===================================================== */
  (function constellation() {
    var cv = $('#stars');
    if (!cv || !cv.getContext) return;
    var ctx = cv.getContext('2d');
    var hero = $('.hero');
    var stars = [], W = 0, H = 0, DPR = 1;
    var px = 0.5, py = 0.4;          // 指针位置（归一化）
    var running = false, rafId = 0;
    var comet = null, lastComet = 0;

    function resize() {
      DPR = clamp(window.devicePixelRatio || 1, 1, 2);
      W = hero.offsetWidth; H = hero.offsetHeight;
      cv.width = W * DPR; cv.height = H * DPR;
      cv.style.width = W + 'px'; cv.style.height = H + 'px';
      ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
      seed();
    }

    function seed() {
      var n = W < 768 ? 64 : 124;
      stars = [];
      for (var i = 0; i < n; i++) {
        stars.push({
          x: Math.random() * W,
          y: Math.random() * H,
          r: Math.random() * 1.5 + 0.4,
          a: Math.random() * 0.55 + 0.18,
          tw: Math.random() * Math.PI * 2,
          ts: Math.random() * 0.018 + 0.004,
          d: Math.random() * 0.7 + 0.3    // 视差深度
        });
      }
    }

    function frame(ts) {
      ctx.clearRect(0, 0, W, H);
      var ox = (px - 0.5) * 26, oy = (py - 0.5) * 18;
      var LINK = W < 768 ? 96 : 132;

      // 航线（近邻连线）
      ctx.lineWidth = 0.6;
      for (var i = 0; i < stars.length; i++) {
        var a = stars[i];
        var ax = a.x + ox * a.d, ay = a.y + oy * a.d;
        for (var j = i + 1; j < stars.length; j++) {
          var b = stars[j];
          var bx = b.x + ox * b.d, by = b.y + oy * b.d;
          var dx = ax - bx, dy = ay - by;
          var dist2 = dx * dx + dy * dy;
          if (dist2 < LINK * LINK) {
            var t = 1 - Math.sqrt(dist2) / LINK;
            ctx.strokeStyle = 'rgba(201,163,92,' + (t * 0.10).toFixed(3) + ')';
            ctx.beginPath(); ctx.moveTo(ax, ay); ctx.lineTo(bx, by); ctx.stroke();
          }
        }
      }

      // 星点（闪烁）
      for (var k = 0; k < stars.length; k++) {
        var s = stars[k];
        s.tw += s.ts;
        var alpha = s.a * (0.65 + 0.35 * Math.sin(s.tw));
        ctx.fillStyle = 'rgba(222,200,146,' + alpha.toFixed(3) + ')';
        ctx.beginPath();
        ctx.arc(s.x + ox * s.d, s.y + oy * s.d, s.r, 0, Math.PI * 2);
        ctx.fill();
      }

      // 彗星：金色航迹，周期性从一星滑向另一星
      if (!reduced) {
        if (!comet && ts - lastComet > 6200 && stars.length > 8) {
          var s1 = stars[(Math.random() * stars.length) | 0];
          var s2 = stars[(Math.random() * stars.length) | 0];
          if (s1 !== s2) {
            comet = { x1: s1.x, y1: s1.y, x2: s2.x, y2: s2.y,
              cx: (s1.x + s2.x) / 2 + (Math.random() - 0.5) * 220,
              cy: Math.min(s1.y, s2.y) - 90, t: 0 };
          }
          lastComet = ts;
        }
        if (comet) {
          comet.t += 0.012;
          var ct = comet.t;
          if (ct >= 1) { comet = null; }
          else {
            ctx.lineWidth = 1.1;
            var TRAIL = 14;
            for (var q = 0; q < TRAIL; q++) {
              var t1 = clamp(ct - q * 0.012, 0, 1);
              var t2 = clamp(ct - (q + 1) * 0.012, 0, 1);
              if (t1 <= 0) break;
              var p1 = bez(comet, t1), p2 = bez(comet, t2);
              ctx.strokeStyle = 'rgba(222,200,146,' + ((1 - q / TRAIL) * 0.5 * Math.sin(Math.PI * ct)).toFixed(3) + ')';
              ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y); ctx.stroke();
            }
          }
        }
      }

      if (running) rafId = requestAnimationFrame(frame);
    }
    function bez(c, t) {
      var u = 1 - t;
      return {
        x: u * u * c.x1 + 2 * u * t * c.cx + t * t * c.x2,
        y: u * u * c.y1 + 2 * u * t * c.cy + t * t * c.y2
      };
    }

    function start() {
      if (running || reduced) return;
      running = true; rafId = requestAnimationFrame(frame);
    }
    function stop() {
      running = false; if (rafId) cancelAnimationFrame(rafId);
    }

    window.addEventListener('resize', function () { resize(); }, { passive: true });
    if (finePointer) {
      hero.addEventListener('pointermove', function (e) {
        var r = hero.getBoundingClientRect();
        px = (e.clientX - r.left) / r.width;
        py = (e.clientY - r.top) / r.height;
      }, { passive: true });
    }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) {
        en[0].isIntersecting ? start() : stop();
      }, { threshold: 0.02 }).observe(hero);
    } else start();
    document.addEventListener('visibilitychange', function () {
      document.hidden ? stop() : start();
    });

    resize();
    if (reduced) { frame(0); }       // 静态一帧
    else start();
  })();

  /* =====================================================
     4. 航线导航轨（≥1200 桌面）+ 顶部进度条（vanilla，无依赖）
     ===================================================== */
  (function railNav() {
    var rail = $('#rail');
    var sections = $$('[data-rail]');
    var fillEl = null;
    if (rail && sections.length) {
      var fill = document.createElement('i');
      fill.className = 'rail__fill';
      rail.appendChild(fill);
      fillEl = fill;
      sections.forEach(function (sec) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'rail__stop';
        b.innerHTML = '<span class="rail__dot"></span><span class="rail__label">' +
          sec.getAttribute('data-rail') + '</span>';
        b.addEventListener('click', function () {
          sec.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'start' });
        });
        rail.appendChild(b);
      });
    }
    var topbarFill = $('#topbarFill');
    var stops = rail ? $$('.rail__stop', rail) : [];
    var ticking = false;

    function update() {
      ticking = false;
      var max = document.documentElement.scrollHeight - innerHeight;
      var p = max > 0 ? clamp(scrollY / max, 0, 1) : 0;
      if (fillEl) fillEl.style.transform = 'scaleY(' + p + ')';
      if (topbarFill) topbarFill.style.transform = 'scaleX(' + p + ')';
      if (stops.length) {
        var idx = 0;
        for (var i = 0; i < sections.length; i++) {
          if (sections[i].getBoundingClientRect().top <= innerHeight * 0.45) idx = i;
        }
        stops.forEach(function (s, n) { s.classList.toggle('active', n === idx); });
      }
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    update();
  })();

  /* =====================================================
     5. 「为什么选途策」展开行（hover 桌面 / 点击触屏 / 键盘可达）
     ===================================================== */
  (function whyRows() {
    $$('.feat').forEach(function (feat) {
      function toggle() { feat.classList.toggle('open'); }
      feat.addEventListener('click', toggle);
      feat.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
      });
      if (finePointer) {
        feat.addEventListener('pointerenter', function () { feat.classList.add('open'); });
        feat.addEventListener('pointerleave', function () { feat.classList.remove('open'); });
      }
    });
  })();

  /* =====================================================
     6. GSAP 编舞（仅在 gsap 在场且未减弱动效时）
     ===================================================== */
  if (!hasGsap || reduced) return;

  gsap.defaults({ ease: 'power3.out', duration: 1 });

  /* ---- 6a. Hero 入场时间线 ---- */
  (function heroIntro() {
    // 拆字
    $$('[data-split]').forEach(function (el) {
      var text = el.textContent;
      el.textContent = '';
      text.split('').forEach(function (ch) {
        var s = document.createElement('span');
        s.className = 'ch';
        s.textContent = ch;
        el.appendChild(s);
      });
    });

    var ulPath = $('.hero__ul path');
    if (ulPath) { ulPath.style.animation = 'none'; }  // CSS 兜底交给 GSAP

    gsap.set('.nav', { yPercent: -110, opacity: 0 });
    gsap.set('.hero__eyebrow', { opacity: 0, y: 16 });
    gsap.set('.hero__line .ch', { yPercent: 118, rotate: 5 });
    gsap.set('.hero__hl', { yPercent: 118, rotate: 3, display: 'inline-block' });
    if (ulPath) gsap.set(ulPath, { strokeDashoffset: 330 });
    gsap.set(['.hero__sub', '.hero__cta'], { opacity: 0, y: 30 });
    gsap.set('.hero__coords', { clipPath: 'inset(0 100% 0 0)' });
    gsap.set('.hero__scroll', { opacity: 0 });
    gsap.set('.hero__vtext', { opacity: 0, letterSpacing: '.9em' });
    gsap.set(['.hero__compass', '#stars'], { opacity: 0 });

    function play() {
      var tl = gsap.timeline();
      tl.to('#stars', { opacity: 1, duration: 1.6, ease: 'power1.inOut' }, 0)
        .to('.hero__compass', { opacity: 0.6, duration: 1.6, ease: 'power1.inOut' }, 0.1)
        .to('.nav', { yPercent: 0, opacity: 1, duration: 0.9 }, 0.15)
        .to('.hero__eyebrow', { opacity: 1, y: 0, duration: 0.8 }, 0.3)
        .to('.hero__line .ch', {
          yPercent: 0, rotate: 0, duration: 1.1, ease: 'power4.out', stagger: 0.045
        }, 0.42)
        .to('.hero__hl', { yPercent: 0, rotate: 0, duration: 1.1, ease: 'power4.out' }, 0.78);
      if (ulPath) tl.to(ulPath, { strokeDashoffset: 0, duration: 1.0, ease: 'power2.inOut' }, 1.35);
      tl.to('.hero__sub', { opacity: 1, y: 0 }, 1.15)
        .to('.hero__cta', { opacity: 1, y: 0 }, 1.3)
        .to('.hero__coords', { clipPath: 'inset(0 0% 0 0)', duration: 1.2, ease: 'power2.inOut' }, 1.5)
        .to('.hero__vtext', { opacity: 1, letterSpacing: '.55em', duration: 1.4 }, 1.5)
        .to('.hero__scroll', { opacity: 1 }, 1.9);
    }
    onPreDone(play);
  })();

  /* ---- 6b. 巨型描边章节号 视差 ---- */
  $$('[data-ghost]').forEach(function (g) {
    gsap.fromTo(g, { yPercent: -14 }, {
      yPercent: 16, ease: 'none',
      scrollTrigger: { trigger: g.parentNode, start: 'top bottom', end: 'bottom top', scrub: 1.1 }
    });
  });

  /* ---- 6c. 服务 · 桌面横向航行（pin + scrub） ---- */
  ScrollTrigger.matchMedia ? setupVoyage() : null;
  function setupVoyage() {
    var mm = gsap.matchMedia();
    mm.add('(min-width:1024px)', function () {
      var pinEl = $('#svcPin'), track = $('#svcTrack');
      var progEl = $('#svcProgress'), progB = progEl ? progEl.querySelector('b') : null;
      if (!pinEl || !track) return;

      doc.classList.add('voyage-on');
      var cards = $$('.card', track);
      // 进入航行模式后强制可见（绕过 .reveal 的 IO 初始态）
      cards.forEach(function (c) { c.classList.add('in'); });

      var getDist = function () {
        return Math.max(0, track.scrollWidth - (innerWidth - pinEl.getBoundingClientRect().left) + innerWidth * 0.14);
      };
      var tween = gsap.to(track, {
        x: function () { return -getDist(); },
        ease: 'none',
        scrollTrigger: {
          trigger: pinEl,
          start: 'top top',
          end: function () { return '+=' + (getDist() + innerHeight * 0.4); },
          pin: true,
          scrub: 1,
          invalidateOnRefresh: true,
          anticipatePin: 1,
          onUpdate: function (st) {
            if (progB) {
              var idx = Math.min(cards.length, Math.round(st.progress * (cards.length - 1)) + 1);
              progB.textContent = String(idx).padStart(2, '0');
            }
          }
        }
      });

      return function () {                 // matchMedia 清理
        doc.classList.remove('voyage-on');
        tween.scrollTrigger && tween.scrollTrigger.kill();
        tween.kill();
        gsap.set(track, { clearProps: 'x' });
      };
    });
  }

  /* ---- 6d. 航程时间线：金线推进 + 节点点亮 ---- */
  $$('.timeline[data-route]').forEach(function (tlEl) {
    var prog = document.createElement('i');
    prog.className = 'timeline__prog';
    tlEl.appendChild(prog);
    gsap.to(prog, {
      scaleY: 1, ease: 'none',
      scrollTrigger: { trigger: tlEl, start: 'top 72%', end: 'bottom 55%', scrub: 0.8 }
    });
    $$('li', tlEl).forEach(function (li) {
      ScrollTrigger.create({
        trigger: li, start: 'top 70%',
        onEnter: function () { li.classList.add('lit'); },
        onLeaveBack: function () { li.classList.remove('lit'); }
      });
    });
  });

  /* ---- 6e. 磁性按钮 ---- */
  if (finePointer) {
    $$('[data-magnetic]').forEach(function (btn) {
      var sx = gsap.quickTo(btn, 'x', { duration: 0.4, ease: 'power3' });
      var sy = gsap.quickTo(btn, 'y', { duration: 0.4, ease: 'power3' });
      btn.addEventListener('pointermove', function (e) {
        var r = btn.getBoundingClientRect();
        sx((e.clientX - r.left - r.width / 2) * 0.28);
        sy((e.clientY - r.top - r.height / 2) * 0.34);
      });
      btn.addEventListener('pointerleave', function () { sx(0); sy(0); });
    });
  }

  /* ---- 6f. 纸页章节标题的细腻进入（不与 .reveal 冲突的元素） ---- */
  $$('.offers__group').forEach(function (g) {
    gsap.from(g, {
      opacity: 0, x: -28, duration: 0.9,
      scrollTrigger: { trigger: g, start: 'top 86%' }
    });
  });

})();
