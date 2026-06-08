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
  var heroBg = $('.hero__bg');
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

  /* ===================== 核心亮点滑动卡片 ===================== */
  var statsTrack = $('.stats__track');
  var statsPrev = $('.stats__prev');
  var statsNext = $('.stats__next');
  var statsDots = $('.stats__dots');

  function updateStatsDots() {
    if (!statsTrack || !statsDots) return;
    var cards = Array.prototype.slice.call(statsTrack.querySelectorAll('.stat-card'));
    var center = statsTrack.scrollLeft + statsTrack.clientWidth / 2;
    cards.forEach(function (card, idx) {
      var dot = statsDots.children[idx];
      if (!dot) return;
      var left = card.offsetLeft;
      var right = left + card.offsetWidth;
      dot.classList.toggle('active', center >= left && center < right);
    });
  }

  if (statsTrack) {
    var statCards = Array.prototype.slice.call(statsTrack.querySelectorAll('.stat-card'));
    if (statsDots && statCards.length) {
      statCards.forEach(function (card, idx) {
        var dot = document.createElement('button');
        dot.type = 'button';
        dot.className = 'stats__dot' + (idx === 0 ? ' active' : '');
        dot.addEventListener('click', function () {
          statsTrack.scrollTo({ left: card.offsetLeft, behavior: 'smooth' });
        });
        statsDots.appendChild(dot);
      });
    }

    if (statsPrev) {
      statsPrev.addEventListener('click', function () {
        statsTrack.scrollBy({ left: -statsTrack.clientWidth * 0.85, behavior: 'smooth' });
      });
    }
    if (statsNext) {
      statsNext.addEventListener('click', function () {
        statsTrack.scrollBy({ left: statsTrack.clientWidth * 0.85, behavior: 'smooth' });
      });
    }

    statsTrack.addEventListener('scroll', function () {
      if (this._statsDotTimer) clearTimeout(this._statsDotTimer);
      this._statsDotTimer = setTimeout(updateStatsDots, 50);
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
  function animateCount(el) {
    var target = parseFloat(el.getAttribute('data-count')) || 0;
    var suffix = el.getAttribute('data-suffix') || '';
    var dur = 1400, start = null;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased) + suffix;
      if (p < 1) requestAnimationFrame(step);
      else el.textContent = target + suffix;
    }
    requestAnimationFrame(step);
  }
  var counters = $$('[data-count]');
  if ('IntersectionObserver' in window && counters.length) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { animateCount(e.target); cio.unobserve(e.target); }
      });
    }, { threshold: 0.5 });
    counters.forEach(function (c) { cio.observe(c); });
  }

  /* ===================== 表单 ===================== */
  var form = $('#leadForm');
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

  if (form) {
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
  } // if (form)

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

})();
