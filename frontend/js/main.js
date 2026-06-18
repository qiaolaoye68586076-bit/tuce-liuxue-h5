/* =========================================================
   途策留学 H5 — main.js
   导航 / 滚动揭示 / 数字滚动 / 表单校验与提交
   ========================================================= */
(function () {
  'use strict';

  /* ------- 配置：留资提交端点（先占位，后端就绪后替换 URL）------- */
  var LEAD_ENDPOINT = '';        // 例如 'https://api.tuce.com/lead'，留空则只存本地
  var LEAD_STORAGE_KEY = 'tuce_leads';

  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ===================== 导航 ===================== */
  var nav    = $('#nav');
  var burger = $('#burger');
  var drawer = $('#drawer');
  var heroBg = $('.hero-bg');
  var brandLogo = $('#brandLogo');
  var prefersReduced = !!(window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches);

  function setLogo(useDark) {
    if (!brandLogo) return;
    var dark = brandLogo.getAttribute('data-logo-dark');
    var light = brandLogo.getAttribute('data-logo-light');
    brandLogo.src = useDark ? dark : light;
  }

  function onScroll() {
    var y = window.scrollY;
    if (y > 24) {
      nav.classList.add('scrolled');
      setLogo(true);
    } else {
      nav.classList.remove('scrolled');
      setLogo(false);
    }

    var cta = $('#floatCta');
    if (cta) {
      if (y > window.innerHeight * 0.8) cta.classList.add('show');
      else cta.classList.remove('show');
    }

    // 克制的首屏背景视差（仅首屏内、GPU transform，减弱动态效果时关闭）
    if (heroBg && !prefersReduced && y < window.innerHeight) {
      heroBg.style.transform = 'translate3d(0,' + (y * 0.18) + 'px,0)';
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ===================== 申请流程滑动卡片（板块3） ===================== */
  var flowTrack = $('.flow__track');
  var flowPrev  = $('.flow__prev');
  var flowNext  = $('.flow__next');
  var flowDots  = $('.flow__dots');

  if (flowTrack) {
    var flowCards = Array.prototype.slice.call(flowTrack.querySelectorAll('.flow-card'));

    function updateFlowDots() {
      if (!flowDots) return;
      var center = flowTrack.scrollLeft + flowTrack.clientWidth / 2;
      flowCards.forEach(function (card, idx) {
        var dot = flowDots.children[idx];
        if (!dot) return;
        dot.classList.toggle('active', center >= card.offsetLeft && center < card.offsetLeft + card.offsetWidth);
      });
    }

    if (flowDots && flowCards.length) {
      flowCards.forEach(function (card, idx) {
        var dot = document.createElement('button');
        dot.type = 'button';
        dot.className = 'flow__dot' + (idx === 0 ? ' active' : '');
        dot.setAttribute('aria-label', '第 ' + (idx + 1) + ' 个阶段');
        dot.addEventListener('click', function () {
          flowTrack.scrollTo({ left: card.offsetLeft, behavior: 'smooth' });
        });
        flowDots.appendChild(dot);
      });
    }

    if (flowPrev) {
      flowPrev.addEventListener('click', function () {
        flowTrack.scrollBy({ left: -flowTrack.clientWidth * 0.9, behavior: 'smooth' });
      });
    }
    if (flowNext) {
      flowNext.addEventListener('click', function () {
        flowTrack.scrollBy({ left: flowTrack.clientWidth * 0.9, behavior: 'smooth' });
      });
    }

    flowTrack.addEventListener('scroll', function () {
      if (this._flowDotTimer) clearTimeout(this._flowDotTimer);
      this._flowDotTimer = setTimeout(updateFlowDots, 50);
    });
  }

  function closeDrawer() {
    burger.classList.remove('open');
    drawer.classList.remove('open');
  }
  burger.addEventListener('click', function () {
    burger.classList.toggle('open');
    drawer.classList.toggle('open');
  });
  $$('#drawer a').forEach(function (a) { a.addEventListener('click', closeDrawer); });

  /* ===================== 滚动揭示 ===================== */
  var revealEls = $$('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.14, rootMargin: '0px 0px -8% 0px' });
    revealEls.forEach(function (el, i) {
      el.style.transitionDelay = (Math.min(i % 4, 3) * 70) + 'ms';
      io.observe(el);
    });
  } else {
    revealEls.forEach(function (el) { el.classList.add('in'); });
  }

  /* ===================== 数字滚动 ===================== */
  function animateCount(el, target, unit, showPlus, duration) {
    duration = duration || 1800;
    var startTime = null;
    function step(now) {
      if (!startTime) startTime = now;
      var progress = Math.min((now - startTime) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      var current = Math.round(eased * target);
      var html = String(current);
      if (showPlus && progress >= 1) html += '<span class="stat-plus">+</span>';
      if (unit) html += '<span class="stat-unit">' + unit + '</span>';
      el.innerHTML = html;
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        // 数字落定：触发一次弹跳缩放
        el.classList.add('is-pop');
      }
    }
    requestAnimationFrame(step);
  }

  var statNums = $$('.stat-num[data-target]');
  if ('IntersectionObserver' in window && statNums.length) {
    var statsBand = document.querySelector('.stats__band');
    if (statsBand) {
      var bandTriggered = false;
      var sio = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting && !bandTriggered) {
            bandTriggered = true;
            sio.unobserve(entry.target);
            statNums.forEach(function(el) {
              animateCount(
                el,
                parseInt(el.getAttribute('data-target'), 10) || 0,
                el.getAttribute('data-unit') || '',
                el.getAttribute('data-plus') === 'true'
              );
            });
          }
        });
      }, { threshold: 0.3 });
      sio.observe(statsBand);
    }
  }

  var counters = $$('[data-count]');
  if ('IntersectionObserver' in window && counters.length) {
    var cio = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        if (e.isIntersecting) {
          cio.unobserve(e.target);
          (function(el) {
            var tgt = parseFloat(el.getAttribute('data-count')) || 0;
            var sfx = el.getAttribute('data-suffix') || '';
            var dur = 1400, s = null;
            function run(ts) {
              if (!s) s = ts;
              var p = Math.min((ts - s) / dur, 1);
              var eased = 1 - Math.pow(1 - p, 3);
              el.textContent = Math.round(tgt * eased) + sfx;
              if (p < 1) requestAnimationFrame(run);
              else el.textContent = tgt + sfx;
            }
            requestAnimationFrame(run);
          })(e.target);
        }
      });
    }, { threshold: 0.5 });
    counters.forEach(function(c) { cio.observe(c); });
  }

  /* ===================== FAQ 手风琴 ===================== */
  $$('.faq__q').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var expanded = this.getAttribute('aria-expanded') === 'true';
      var panel = $('#' + this.getAttribute('aria-controls'));

      $$('.faq__q').forEach(function (b) {
        b.setAttribute('aria-expanded', 'false');
        var p = $('#' + b.getAttribute('aria-controls'));
        if (p) { p.classList.remove('open'); p.setAttribute('aria-hidden', 'true'); }
      });

      if (!expanded && panel) {
        this.setAttribute('aria-expanded', 'true');
        panel.classList.add('open');
        panel.setAttribute('aria-hidden', 'false');
      }
    });
  });

  /* ===================== 表单（仅首页存在，子页面安全跳过） ===================== */
  var form = $('#leadForm');
  if (form) {
  var note = $('#formNote');
  var btn  = $('#submitBtn');

  function setErr(name, msg) {
    var small = $('.err[data-for="' + name + '"]', form);
    var input = form.elements[name];
    if (small) small.textContent = msg || '';
    if (input) input.classList.toggle('invalid', !!msg);
  }

  function validate() {
    var ok = true;
    var v = function (n) { return (form.elements[n].value || '').trim(); };

    if (!v('uname'))      { setErr('uname', '请填写姓名'); ok = false; } else setErr('uname', '');
    if (!v('type'))       { setErr('type', '请选择咨询方向'); ok = false; } else setErr('type', '');

    var phone = v('phone');
    if (!phone)                       { setErr('phone', '请填写电话'); ok = false; }
    else if (!/^1[3-9]\d{9}$/.test(phone)) { setErr('phone', '请输入有效的 11 位手机号'); ok = false; }
    else setErr('phone', '');

    if (!form.elements['agree'].checked) {
      showNote('请先阅读并同意用户协议与隐私政策', 'bad');
      ok = false;
    }
    return ok;
  }

  function showNote(msg, type) {
    note.hidden = false;
    note.textContent = msg;
    note.className = 'form__note field--full ' + (type || '');
  }

  function collect() {
    var data = {};
    ['uname', 'type', 'phone', 'wechat', 'city', 'school', 'more'].forEach(function (n) {
      data[n] = (form.elements[n].value || '').trim();
    });
    data.ts = new Date().toISOString();
    data.source = 'h5';
    return data;
  }

  function saveLocal(data) {
    try {
      var arr = JSON.parse(localStorage.getItem(LEAD_STORAGE_KEY) || '[]');
      arr.push(data);
      localStorage.setItem(LEAD_STORAGE_KEY, JSON.stringify(arr));
    } catch (e) { /* localStorage 不可用时静默 */ }
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    note.hidden = true;
    if (!validate()) return;

    var data = collect();
    saveLocal(data);                       // 始终先本地留底
    btn.disabled = true;
    btn.textContent = '提交中…';

    var done = function (success) {
      btn.disabled = false;
      btn.textContent = '提交，预约免费评估';
      if (success) {
        showNote('提交成功！导师将在 24 小时内与你联系 ✓', 'ok');
        form.reset();
      } else {
        showNote('已为你保存，网络异常稍后将自动重试。也可直接扫码加导师微信。', 'bad');
      }
    };

    if (LEAD_ENDPOINT) {
      fetch(LEAD_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      .then(function (r) { done(r.ok); })
      .catch(function () { done(false); });
    } else {
      // 占位：尚未配置后端，模拟成功
      setTimeout(function () { done(true); }, 600);
    }
  });

  // 输入时清除该字段错误
  ['uname', 'type', 'phone'].forEach(function (n) {
    var el = form.elements[n];
    el.addEventListener('input',  function () { setErr(n, ''); });
    el.addEventListener('change', function () { setErr(n, ''); });
  });
  } /* end if (form) */

  // 协议弹层
  var policy = $('#policyLink');
  var policyModal = $('#policyModal');
  function closePolicy() { if (policyModal) policyModal.hidden = true; }
  if (policy && policyModal) {
    policy.addEventListener('click', function (e) {
      e.preventDefault();
      policyModal.hidden = false;
    });
    policyModal.addEventListener('click', function (e) {
      if (e.target.hasAttribute('data-close')) closePolicy();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closePolicy();
    });
  }


  /* ===================== Hero 动画与效果 ===================== */

  // 背景图加载后触发缩放动画
  var heroBgEl = document.querySelector('.hero-bg');
  if (heroBgEl) {
    var bgImg = new Image();
    bgImg.onload = function () { heroBgEl.classList.add('loaded'); };
    var bgUrl = window.getComputedStyle(heroBgEl).backgroundImage.replace(/url\(["']?|["']?\)/g, '');
    bgImg.src = bgUrl;
  }

  // 打字机循环动效
  (function () {
    var el = document.getElementById('heroTypewriter');
    if (!el || prefersReduced) {
      if (el) el.textContent = '我们对"千人一面"过敏。';
      return;
    }
    var phrases = [
      '我们对"千人一面"过敏。',
      '你的故事，只属于你。',
      '策略先行，拒绝模板。',
      '每一份申请，重新设计。'
    ];
    var phraseIdx = 0;
    var charIdx = 0;
    var deleting = false;
    var pauseFrames = 0;
    var PAUSE_AFTER_TYPE = 25;   // 打完停顿帧数（25 × 200ms ≈ 5s 停留）
    var PAUSE_AFTER_DEL  = 6;    // 删完后短暂停顿再开始下一句

    function tick() {
      var current = phrases[phraseIdx];
      if (deleting) {
        charIdx--;
        el.textContent = current.slice(0, charIdx);
        if (charIdx <= 0) {
          deleting = false;
          phraseIdx = (phraseIdx + 1) % phrases.length;
          pauseFrames = PAUSE_AFTER_DEL;
        }
      } else {
        charIdx++;
        el.textContent = current.slice(0, charIdx);
        if (charIdx >= current.length) {
          deleting = true;
          pauseFrames = PAUSE_AFTER_TYPE;
        }
      }
      var delay = deleting ? 70 : 130;  // 打字 130ms/字，删除 70ms/字
      if (pauseFrames > 0) { pauseFrames--; delay = 200; }
      setTimeout(tick, delay);
    }

    // 等 hero-footnote 动画结束后启动（1.6s delay + 0.6s duration）
    setTimeout(tick, 2400);
  })();

  // 滚动后隐藏向下提示
  window.addEventListener('scroll', function () {
    var hint = document.querySelector('.hero-scroll-hint');
    if (hint) {
      hint.style.opacity = '0';
      hint.style.transition = 'opacity 0.5s';
    }
  }, { once: true, passive: true });
})();
