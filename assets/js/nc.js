/* ==========================================================================
   Natasha & Company — Interactions
   Vanilla JS. No jQuery, no framework. ~9KB.
   ========================================================================== */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ------------------------------------------------------------------
     1. Header: solid once scrolled
     ------------------------------------------------------------------ */
  function header() {
    var hdr = $('.nc-hdr');
    if (!hdr) return;
    var ticking = false;
    function check() {
      hdr.classList.toggle('is-stuck', window.scrollY > 24);
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(check); }
    }, { passive: true });
    check();
  }

  /* ------------------------------------------------------------------
     3. Desktop dropdowns — pointer + keyboard
     ------------------------------------------------------------------ */
  function dropdowns() {
    var items = $$('.nc-nav li.has-drop');
    if (!items.length) return;

    function closeAll(except) {
      items.forEach(function (li) {
        if (li === except) return;
        li.classList.remove('is-open');
        var t = $('a[aria-expanded], button[aria-expanded]', li);
        if (t) t.setAttribute('aria-expanded', 'false');
      });
    }

    items.forEach(function (li) {
      var trigger = li.querySelector(':scope > a');
      var timer;

      li.addEventListener('mouseenter', function () {
        clearTimeout(timer);
        closeAll(li);
        li.classList.add('is-open');
        if (trigger) trigger.setAttribute('aria-expanded', 'true');
      });
      li.addEventListener('mouseleave', function () {
        timer = setTimeout(function () {
          li.classList.remove('is-open');
          if (trigger) trigger.setAttribute('aria-expanded', 'false');
        }, 140);
      });
      // Keyboard: focus anywhere inside opens; leaving closes.
      li.addEventListener('focusin', function () {
        closeAll(li);
        li.classList.add('is-open');
        if (trigger) trigger.setAttribute('aria-expanded', 'true');
      });
      li.addEventListener('focusout', function (e) {
        if (!li.contains(e.relatedTarget)) {
          li.classList.remove('is-open');
          if (trigger) trigger.setAttribute('aria-expanded', 'false');
        }
      });
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeAll(null);
    });
  }

  /* ------------------------------------------------------------------
     4. Mobile drawer
     ------------------------------------------------------------------ */
  function drawer() {
    var burger = $('.nc-burger');
    var panel = $('.nc-drawer');
    var scrim = $('.nc-scrim');
    var close = $('.nc-drawer-close');
    if (!burger || !panel) return;

    var lastFocus = null;

    function open() {
      lastFocus = document.activeElement;
      document.body.classList.add('nc-menu-open', 'nc-locked');
      burger.setAttribute('aria-expanded', 'true');
      panel.removeAttribute('aria-hidden');
      var first = panel.querySelector('a, button');
      if (first) setTimeout(function () { first.focus(); }, 260);
    }
    function shut() {
      document.body.classList.remove('nc-menu-open', 'nc-locked');
      burger.setAttribute('aria-expanded', 'false');
      panel.setAttribute('aria-hidden', 'true');
      if (lastFocus) lastFocus.focus();
    }
    function toggle() {
      document.body.classList.contains('nc-menu-open') ? shut() : open();
    }

    burger.addEventListener('click', toggle);
    if (close) close.addEventListener('click', shut);
    if (scrim) scrim.addEventListener('click', shut);

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('nc-menu-open')) shut();
    });

    // Trap focus inside the open drawer.
    panel.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab') return;
      var f = $$('a[href], button:not([disabled]), input, select, textarea', panel)
        .filter(function (el) { return el.offsetParent !== null; });
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });

    // Close after tapping a real link (not an accordion toggle).
    $$('a[href]', panel).forEach(function (a) {
      a.addEventListener('click', function () {
        if (a.getAttribute('href').charAt(0) !== '#') shut();
      });
    });

    // Accordion sections
    $$('.nc-macc > li > button', panel).forEach(function (btn) {
      btn.addEventListener('click', function () {
        var li = btn.parentElement;
        var was = li.classList.contains('is-open');
        $$('.nc-macc > li', panel).forEach(function (o) {
          o.classList.remove('is-open');
          var b = o.querySelector(':scope > button');
          if (b) b.setAttribute('aria-expanded', 'false');
        });
        if (!was) { li.classList.add('is-open'); btn.setAttribute('aria-expanded', 'true'); }
      });
    });

    // Reset when the layout crosses back to desktop.
    window.addEventListener('resize', function () {
      if (window.innerWidth >= 1100 && document.body.classList.contains('nc-menu-open')) shut();
    }, { passive: true });
  }

  /* ------------------------------------------------------------------
     5. Scroll reveal
     ------------------------------------------------------------------ */
  /* Article and service pages carry their prose as one long block, so nothing
     animated as you read down them. Tag the top-level pieces here rather than
     in every builder, and the same reveal system covers every page. */
  /* The reference design gives each tile in a grid a different entry
     direction, which is why its service block reads as assembling rather than
     sliding. Same idea here: cycle the directions across each grid. */
  var GRID_PATTERN = ['right', 'down', 'left', 'right', 'up', 'left'];

  function autoTag() {
    if (reduce) return;

    // Long prose pages had nothing animated; tag their top-level blocks.
    $$('.nc-prose').forEach(function (prose) {
      Array.prototype.forEach.call(prose.children, function (el) {
        if (el.hasAttribute('data-nc-rise')) return;
        el.setAttribute('data-nc-rise', /^H[2-4]$/.test(el.tagName) ? 'scale' : '');
      });
    });

    $$('.nc-faq details').forEach(function (el) {
      if (!el.hasAttribute('data-nc-rise')) el.setAttribute('data-nc-rise', '');
    });

    // Every grid: alternate the direction tile by tile.
    $$('.nc-grid, .nc-portals, .nc-cal-list').forEach(function (grid) {
      var i = 0;
      Array.prototype.forEach.call(grid.children, function (el) {
        if (el.getAttribute('data-nc-rise')) { i++; return; }
        el.setAttribute('data-nc-rise', GRID_PATTERN[i % GRID_PATTERN.length]);
        i++;
      });
    });

    // Two-column splits lean in from their own side.
    $$('.nc-split').forEach(function (split) {
      Array.prototype.forEach.call(split.children, function (el, n) {
        if (!el.hasAttribute('data-nc-rise')) {
          el.setAttribute('data-nc-rise', n % 2 ? 'right' : 'left');
        }
      });
    });
  }

  function reveal() {
    autoTag();
    var els = $$('[data-nc-rise]');
    if (!els.length) return;
    if (reduce || !('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.classList.add('is-in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('is-in');
        io.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.04 });

    els.forEach(function (el) {
      // Stagger siblings that share a parent unless an explicit delay is set.
      if (!el.style.getPropertyValue('--d')) {
        var sibs = Array.prototype.filter.call(el.parentElement.children, function (c) {
          return c.hasAttribute('data-nc-rise');
        });
        var i = sibs.indexOf(el);
        if (i > 0 && sibs.length > 1) el.style.setProperty('--d', Math.min(i, 8) * 110 + 'ms');
      }
      io.observe(el);
    });
  }

  /* ------------------------------------------------------------------
     6. Counters
     ------------------------------------------------------------------ */
  function counters() {
    var els = $$('[data-count]');
    if (!els.length) return;

    function run(el) {
      var target = parseFloat(el.getAttribute('data-count'));
      if (isNaN(target)) return;
      var dur = parseInt(el.getAttribute('data-count-dur') || '1800', 10);
      var dec = (String(target).split('.')[1] || '').length;
      var t0 = null;

      // Years and similar identifiers must not be digit-grouped: 2017, not 2,017.
      var plain = el.hasAttribute('data-count-plain');
      function fmt(v) {
        if (plain) return v.toFixed(dec);
        return v.toLocaleString('en-IN', { minimumFractionDigits: dec, maximumFractionDigits: dec });
      }
      if (reduce) { el.textContent = fmt(target); return; }

      var done = false;
      function settle() {
        if (done) return;
        done = true;
        el.textContent = fmt(target);
      }

      function tick(ts) {
        if (done) return;
        if (t0 === null) t0 = ts;
        var p = Math.min((ts - t0) / dur, 1);
        var eased = 1 - Math.pow(1 - p, 3); // easeOutCubic
        el.textContent = fmt(target * eased);
        if (p < 1) requestAnimationFrame(tick);
        else settle();
      }
      requestAnimationFrame(tick);

      /* A backstop, so the figure is never left mid-count on a device where
         requestAnimationFrame is starved or throttled. */
      setTimeout(settle, dur + 400);
    }

    if (!('IntersectionObserver' in window)) { els.forEach(run); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        run(e.target);
        io.unobserve(e.target);
      });
    }, { threshold: 0.4 });
    els.forEach(function (el) { io.observe(el); });
  }

  /* ------------------------------------------------------------------
     7. Card cursor glow
     ------------------------------------------------------------------ */
  function cardGlow() {
    if (reduce || !window.matchMedia('(hover: hover)').matches) return;
    $$('.nc-card-glow').forEach(function (card) {
      card.addEventListener('pointermove', function (e) {
        var r = card.getBoundingClientRect();
        card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        card.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });
  }

  /* ------------------------------------------------------------------
     8. Back to top
     ------------------------------------------------------------------ */
  function toTop() {
    var btn = $('.nc-fab-top');
    if (!btn) return;
    var ticking = false;
    function check() { btn.classList.toggle('is-on', window.scrollY > 700); ticking = false; }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(check); }
    }, { passive: true });
    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
    });
    check();
  }

  /* ------------------------------------------------------------------
     9. Reading progress (articles)
     ------------------------------------------------------------------ */
  function progress() {
    var bar = $('.nc-progress');
    if (!bar) return;
    var ticking = false;
    function check() {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(window.scrollY / max, 1) : 0) + ')';
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(check); }
    }, { passive: true });
    window.addEventListener('resize', check, { passive: true });
    check();
  }

  /* ------------------------------------------------------------------
     10. Table of contents — build from article headings, track active
     ------------------------------------------------------------------ */
  function toc() {
    var nav = $('.nc-toc');
    var body = $('.nc-prose');
    if (!nav || !body) return;

    var heads = $$('h2', body).filter(function (h) { return h.textContent.trim(); });
    if (heads.length < 3) { var box = nav.closest('.nc-card'); if (box) box.remove(); return; }

    var frag = document.createDocumentFragment();
    heads.forEach(function (h, i) {
      if (!h.id) {
        h.id = h.textContent.trim().toLowerCase()
          .replace(/[^\w\s-]/g, '').replace(/\s+/g, '-').slice(0, 60) || 'section-' + i;
      }
      var a = document.createElement('a');
      a.href = '#' + h.id;
      a.textContent = h.textContent.trim();
      frag.appendChild(a);
    });
    nav.appendChild(frag);

    if (!('IntersectionObserver' in window)) return;
    var links = $$('a', nav);
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        links.forEach(function (l) {
          l.classList.toggle('is-active', l.getAttribute('href') === '#' + e.target.id);
        });
      });
    }, { rootMargin: '-90px 0px -70% 0px' });
    heads.forEach(function (h) { io.observe(h); });
  }

  /* ------------------------------------------------------------------
     11. Wrap wide tables so they scroll instead of breaking the layout
     ------------------------------------------------------------------ */
  function tables() {
    $$('.nc-prose table').forEach(function (t) {
      if (t.parentElement && t.parentElement.classList.contains('nc-tw')) return;
      var w = document.createElement('div');
      w.className = 'nc-tw';
      t.parentNode.insertBefore(w, t);
      w.appendChild(t);
    });
  }

  /* ------------------------------------------------------------------
     12. Footer year
     ------------------------------------------------------------------ */
  function year() {
    $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
  }

  /* ------------------------------------------------------------------
     13. Mark the current page in the nav
     ------------------------------------------------------------------ */
  function current() {
    var here = location.pathname.split('/').pop() || 'index.html';
    $$('.nc-nav > ul > li').forEach(function (li) {
      var links = $$('a[href]', li);
      var hit = links.some(function (a) {
        var href = a.getAttribute('href');
        return href && href.split('#')[0].split('/').pop() === here;
      });
      if (hit) {
        li.classList.add('is-current');
        var top = li.querySelector(':scope > a');
        if (top && top.getAttribute('href') &&
            top.getAttribute('href').split('#')[0].split('/').pop() === here) {
          top.setAttribute('aria-current', 'page');
        }
      }
    });
  }


  /* ------------------------------------------------------------------
     14. Compliance calendar — month tabs
     ------------------------------------------------------------------ */
  function calendar() {
    var tabs = $$('.nc-cal-tab');
    if (!tabs.length) return;

    function show(month) {
      tabs.forEach(function (t) {
        var on = t.getAttribute('data-month') === month;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
      });
      $$('.nc-cal-panel').forEach(function (p) {
        p.hidden = p.getAttribute('data-month') !== month;
      });
    }

    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { show(t.getAttribute('data-month')); });
      // Left/right arrows move between tabs, per the tablist pattern.
      t.addEventListener('keydown', function (e) {
        var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        var next = tabs[(i + d + tabs.length) % tabs.length];
        next.focus();
        show(next.getAttribute('data-month'));
      });
    });

    // Open on the current month.
    var now = String(new Date().getMonth() + 1);
    var here = tabs.filter(function (t) { return t.getAttribute('data-month') === now; });
    show(here.length ? now : tabs[0].getAttribute('data-month'));
  }


  /* ------------------------------------------------------------------
     15. Hero carousel — cross-fading slides
     ------------------------------------------------------------------ */
  function heroSlides() {
    var wrap = $('.nc-slides');
    if (!wrap) return;
    var slides = $$('.nc-slide', wrap);
    var dots = $$('.nc-hero-dot');
    if (slides.length < 2) return;

    var backgrounds = $$('.nc-hero-bg figure');
    var arrows = $$('[data-nc-slide]');
    var at = 0;
    var timer = null;
    var DWELL = 5200;

    // Photographs after the first are fetched on demand (see build_home.py).
    function ensureBg(n) {
      var f = backgrounds[(n + backgrounds.length) % backgrounds.length];
      if (f && f.dataset.bg) {
        f.style.backgroundImage = 'url("' + f.dataset.bg + '")';
        f.removeAttribute('data-bg');
      }
    }

    function go(i) {
      at = (i + slides.length) % slides.length;
      ensureBg(at);
      // Warm the next one so it is ready before its turn, but never before
      // the page has finished loading: the first photo gets the bandwidth.
      if (document.readyState === 'complete') ensureBg(at + 1);
      slides.forEach(function (s, n) { s.classList.toggle('is-on', n === at); });
      backgrounds.forEach(function (b, n) { b.classList.toggle('is-on', n === at); });
      dots.forEach(function (d, n) {
        d.setAttribute('aria-selected', n === at ? 'true' : 'false');
        d.tabIndex = n === at ? 0 : -1;
      });
    }
    /* The slideshow runs even when the device asks for reduced motion. Many
       Android phones switch that setting on with battery saver, and the hero
       then sat on its first slide for good. A cross-fade every few seconds is
       not the kind of movement the setting exists to stop (zoom, parallax,
       sliding panels), so those stay off there; see nc.css section 38. */
    function play() {
      if (!timer) timer = setInterval(function () { go(at + 1); }, reduce ? DWELL + 1300 : DWELL);
    }
    function pause() { if (timer) { clearInterval(timer); timer = null; } }

    dots.forEach(function (d, i) {
      d.addEventListener('click', function () { pause(); go(i); play(); });
      d.addEventListener('keydown', function (e) {
        var k = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (!k) return;
        e.preventDefault();
        pause(); go(at + k); dots[at].focus(); play();
      });
    });

    arrows.forEach(function (b) {
      b.addEventListener('click', function () {
        pause();
        go(at + (b.getAttribute('data-nc-slide') === 'prev' ? -1 : 1));
        play();
      });
    });

    // Respect the reader: stop rotating on hover, focus, or a hidden tab.
    /* Pause only over the controls and the copy — not the whole hero. The
       hero fills the viewport, so a pointer anywhere on screen counts as
       "hovering" it and the carousel would never advance for a real visitor. */
    var hero = wrap.closest ? wrap.closest('.nc-hero') || wrap : wrap;
    /* Controls only. Hovering the headline is not "reading" in the way a
       news ticker is, and stopping there left the photo stuck for anyone
       whose pointer rested mid-screen. */
    [document.querySelector('.nc-hero-nav')]
      .concat(arrows)
      .filter(Boolean)
      .forEach(function (zone) {
        zone.addEventListener('mouseenter', pause);
        zone.addEventListener('mouseleave', play);
      });
    // Pause for keyboard focus only. On a phone, a tap focuses whatever was
    // touched and nothing ever blurs it, so a tap used to stop the slideshow
    // for the rest of the visit.
    hero.addEventListener('focusin', function (e) {
      if (e.target.matches && e.target.matches(':focus-visible')) pause();
    });
    hero.addEventListener('focusout', function (e) {
      if (!hero.contains(e.relatedTarget)) play();
    });
    document.addEventListener('visibilitychange', function () {
      document.hidden ? pause() : play();
    });

    go(0);
    window.addEventListener('load', function () { ensureBg(at + 1); });
    play();
  }


  /* ------------------------------------------------------------------
     16. Contact form
        lead-capture.js already recorded the lead on the capture phase of
        this same submit event, so by the time we run, the row is on its way
        to the sheet. Our job is only to keep the visitor on the page, show
        that it worked, and offer the WhatsApp handoff rather than force it.
     ------------------------------------------------------------------ */
  function contactForm() {
    // The home page carries an enquiry form as well as the contact page.
    $$('form[data-nc-contact]').forEach(wire);
  }

  function wire(form) {
    var stat = $('.nc-fstat', form);
    var btn = $('button[type="submit"]', form);

    function say(kind, html) {
      if (!stat) return;
      stat.className = 'nc-fstat is-on ' + kind;
      stat.innerHTML = html;
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      // Native validation, surfaced rather than silently ignored.
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      var get = function (n) {
        var el = form.elements[n];
        return el && el.value ? el.value.trim() : '';
      };
      var name = get('name'), phone = get('phone');
      var email = get('email'), subject = get('subject'), message = get('message');

      var text = [
        'Hello Natasha & Company,',
        '',
        'Name: ' + name,
        'Phone: ' + phone,
        email ? 'Email: ' + email : null,
        'Topic: ' + subject,
        '',
        message
      ].filter(function (line) { return line !== null; }).join('\n');

      var wa = 'https://wa.me/919407000157?text=' + encodeURIComponent(text);

      say('ok',
        '<strong>Thank you, ' + (name.split(' ')[0] || 'there') + '.</strong> ' +
        'Your enquiry has reached us and we reply the same working day.<br>' +
        '<a href="' + wa + '" target="_blank" rel="noopener" style="font-weight:600">' +
        'Send it on WhatsApp too</a> if it is urgent, or call ' +
        '<a href="tel:+919407000157" style="font-weight:600">+91 94070 00157</a>.');

      if (btn) {
        btn.disabled = true;
        btn.textContent = 'Sent';
      }
      form.reset();
      stat.scrollIntoView({ block: 'nearest', behavior: reduce ? 'auto' : 'smooth' });
    });
  }


  /* ------------------------------------------------------------------
     17. Card tilt — the card leans towards the pointer
     ------------------------------------------------------------------ */
  function tilt() {
    if (reduce || !window.matchMedia('(hover: hover)').matches) return;
    $$('.nc-pcard').forEach(function (card) {
      var raf = 0;
      card.addEventListener('pointermove', function (e) {
        if (raf) return;
        raf = requestAnimationFrame(function () {
          raf = 0;
          var r = card.getBoundingClientRect();
          var x = (e.clientX - r.left) / r.width - 0.5;
          var y = (e.clientY - r.top) / r.height - 0.5;
          card.style.transform =
            'translateY(-10px) perspective(900px) rotateX(' + (-y * 5).toFixed(2) +
            'deg) rotateY(' + (x * 6).toFixed(2) + 'deg)';
        });
      });
      card.addEventListener('pointerleave', function () {
        card.style.transform = '';
      });
    });
  }


  /* ------------------------------------------------------------------
     18. Knowledge Bank mega-menu
     ------------------------------------------------------------------ */
  function mega() {
    var mm = $('.nc-mega');
    if (mm) {
      var cats = $$('.nc-mega-cat', mm);
      var panels = $$('.nc-mega-panel', mm);

      function show(i) {
        cats.forEach(function (c, n) {
          var on = n === i;
          c.classList.toggle('is-on', on);
          c.setAttribute('aria-selected', on ? 'true' : 'false');
          c.tabIndex = on ? 0 : -1;
        });
        panels.forEach(function (p, n) {
          p.hidden = n !== i;
          p.classList.toggle('is-on', n === i);
        });
      }

      cats.forEach(function (c, i) {
        // Pointer reveals on hover, as a reference menu should.
        c.addEventListener('mouseenter', function () { show(i); });
        c.addEventListener('focus', function () { show(i); });
        c.addEventListener('click', function (e) { e.preventDefault(); show(i); });
        c.addEventListener('keydown', function (e) {
          var d = e.key === 'ArrowDown' ? 1 : e.key === 'ArrowUp' ? -1 : 0;
          if (!d) return;
          e.preventDefault();
          var next = (i + d + cats.length) % cats.length;
          cats[next].focus();
          show(next);
        });
      });
    }

    // Drawer: flat accordion, one category open at a time.
    $$('.nc-msub-cat').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var was = btn.classList.contains('is-on');
        $$('.nc-msub-cat').forEach(function (b) { b.classList.remove('is-on'); });
        if (!was) btn.classList.add('is-on');
      });
    });
  }

  /* ------------------------------------------------------------------
     Reviews slider — arrows and dots over a scroll-snap track.
     The track scrolls and swipes on its own; this only adds controls.
     ------------------------------------------------------------------ */
  function sliders() {
    $$('[data-nc-slider]').forEach(function (box) {
      var track = $('.nc-revs-track', box);
      var dots = $('.nc-revs-dots', box);
      var prev = $('[data-nc-slide="prev"]', box);
      var next = $('[data-nc-slide="next"]', box);
      if (!track || !track.children.length) return;

      function page() {
        // One "page" is one screenful of cards, which is what a dot represents.
        return Math.max(1, Math.round(track.clientWidth));
      }
      function pages() {
        // Count from the distance the track can actually scroll. Dividing the
        // full scrollWidth instead left a phantom last page, because the track's
        // own padding pushed the total a few pixels past a whole screenful.
        var max = track.scrollWidth - track.clientWidth;
        return max <= 4 ? 1 : Math.round(max / page()) + 1;
      }
      function at() {
        return Math.min(pages() - 1, Math.round(track.scrollLeft / page()));
      }
      function go(i) {
        track.scrollTo({ left: i * page(), behavior: reduce ? 'auto' : 'smooth' });
      }

      function buildDots() {
        if (!dots) return;
        var n = pages();
        if (dots.children.length === n) return;
        dots.textContent = '';
        for (var i = 0; i < n; i++) {
          (function (i) {
            var b = document.createElement('button');
            b.type = 'button';
            b.setAttribute('role', 'tab');
            b.setAttribute('aria-label', 'Reviews, page ' + (i + 1) + ' of ' + n);
            b.addEventListener('click', function () { go(i); });
            dots.appendChild(b);
          })(i);
        }
      }

      function sync() {
        var i = at(), n = pages();
        if (dots) {
          $$('button', dots).forEach(function (b, k) {
            b.setAttribute('aria-selected', k === i ? 'true' : 'false');
          });
        }
        if (prev) prev.disabled = i <= 0;
        if (next) next.disabled = i >= n - 1;
      }

      if (prev) prev.addEventListener('click', function () { go(at() - 1); });
      if (next) next.addEventListener('click', function () { go(at() + 1); });

      var t;
      track.addEventListener('scroll', function () {
        clearTimeout(t);
        t = setTimeout(sync, 90);
      }, { passive: true });

      window.addEventListener('resize', function () {
        clearTimeout(t);
        t = setTimeout(function () { buildDots(); sync(); }, 150);
      }, { passive: true });

      // Auto-slide animation (4.5s loop with hover & touch pause)
      var autoTimer = null;
      var paused = false;

      function step() {
        if (paused || document.hidden) return;
        var cur = at(), total = pages();
        if (total <= 1) return;
        var nextIndex = (cur + 1) >= total ? 0 : cur + 1;
        go(nextIndex);
      }

      function startAuto() {
        if (reduce || autoTimer) return;
        autoTimer = setInterval(step, 4500);
      }

      box.addEventListener('mouseenter', function () { paused = true; });
      box.addEventListener('mouseleave', function () { paused = false; });
      box.addEventListener('touchstart', function () { paused = true; }, { passive: true });
      box.addEventListener('touchend', function () {
        setTimeout(function () { paused = false; }, 2500);
      }, { passive: true });

      buildDots();
      sync();
      startAuto();
    });
  }

  /* ------------------------------------------------------------------
     External links: open a new tab where the browser allows one.
     In-app browsers (WhatsApp, Instagram) often ignore target="_blank"
     entirely, and the tap then does nothing at all. Falling back to the
     same tab means the link always goes somewhere.
     ------------------------------------------------------------------ */
  function externalLinks() {
    document.addEventListener('click', function (e) {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      var a = e.target.closest ? e.target.closest('a[target="_blank"][href]') : null;
      if (!a) return;
      var href = a.href;
      if (!/^https?:/i.test(href)) return;

      // No 'noopener' in the feature string: with it, window.open always returns
      // null by spec, which reads here as "blocked" and would send every external
      // link to the same tab. The reference is severed afterwards instead.
      var win;
      try { win = window.open(href, '_blank'); } catch (err) { win = null; }
      e.preventDefault();
      if (win) { try { win.opener = null; } catch (err) {} }
      else window.location.href = href;   // no new tab available — go here instead
    });
  }

  /* ------------------------------------------------------------------
     Boot
     ------------------------------------------------------------------ */
  function init() {
    sliders();
    externalLinks();
    header();
    dropdowns();
    drawer();
    reveal();
    counters();
    cardGlow();
    toTop();
    progress();
    tables();
    toc();
    year();
    current();
    calendar();
    heroSlides();
    contactForm();
    tilt();
    mega();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
