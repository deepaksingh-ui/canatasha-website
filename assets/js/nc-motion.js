/* ==========================================================================
   Natasha & Company — motion layer
   --------------------------------------------------------------------------
   Applies to every page, home and sub-pages alike, without any per-page markup:

     · headings assemble word by word as they enter
     · photographs wipe in behind a coloured mask
     · buttons lean towards the pointer
     · section media drifts slightly against the scroll

   Everything here is decoration. It is skipped entirely under
   prefers-reduced-motion, and nothing depends on it to read the page.
   ========================================================================== */
(function () {
  'use strict';

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var $$ = function (s, r) {
    return Array.prototype.slice.call((r || document).querySelectorAll(s));
  };

  /* ------------------------------------------------------------------
     1. Split headings into words
        Only h1/h2 — going deeper turns every page into confetti. Skips
        headings that carry markup we would destroy by rewriting innerHTML.
     ------------------------------------------------------------------ */
  function splitHeadings() {
    $$('h1, h2').forEach(function (h) {
      // Small labels (footer columns, sidebar cards) are h2 for document
      // order only; they are not headlines and do not animate.
      if (h.closest('.nc-mega, .nc-drawer, .nc-panel-head, .nc-ftr, .nc-aside') ||
          h.classList.contains('nc-h4')) return;
      if (h.querySelector('.nc-word')) return;

      // Walk only direct text nodes so nested <em>/<span> keep their styling.
      var nodes = Array.prototype.slice.call(h.childNodes);
      var index = 0;

      nodes.forEach(function (node) {
        if (node.nodeType !== 3 || !node.textContent.trim()) return;
        var frag = document.createDocumentFragment();
        node.textContent.split(/(\s+)/).forEach(function (part) {
          if (!part.trim()) {
            frag.appendChild(document.createTextNode(part));
            return;
          }
          var w = document.createElement('span');
          w.className = 'nc-word';
          w.style.setProperty('--wd', Math.min(index, 14) * 45 + 'ms');
          w.textContent = part;
          frag.appendChild(w);
          index++;
        });
        h.replaceChild(frag, node);
      });

      // Inline elements inside the heading animate as one unit.
      $$(':scope > em, :scope > span:not(.nc-word)', h).forEach(function (el) {
        if (el.classList.contains('nc-shimmer')) return;   // shimmer runs its own
        el.classList.add('nc-word');
        el.style.setProperty('--wd', Math.min(index++, 14) * 45 + 'ms');
      });
    });
  }

  /* ------------------------------------------------------------------
     2. Mask-reveal photographs
     ------------------------------------------------------------------ */
  function markReveals() {
    $$('.nc-media, .nc-pcard-img, .nc-post-img').forEach(function (el) {
      if (!el.classList.contains('nc-reveal')) el.classList.add('nc-reveal');
    });
  }

  /* ------------------------------------------------------------------
     3. One observer drives both
     ------------------------------------------------------------------ */
  function observe() {
    if (!('IntersectionObserver' in window)) {
      $$('.nc-word, .nc-reveal').forEach(function (e) { e.classList.add('is-in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('is-in');
        io.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    // Headings animate as a group so the words stagger together.
    $$('h1, h2').forEach(function (h) {
      if (h.querySelector('.nc-word')) io.observe(h);
    });
    $$('.nc-reveal').forEach(function (el) { io.observe(el); });
  }

  /* ------------------------------------------------------------------
     4. Magnetic buttons — pointer devices only
     ------------------------------------------------------------------ */
  function magnetic() {
    if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;

    $$('.nc-btn').forEach(function (btn) {
      var raf = 0;
      btn.addEventListener('pointermove', function (e) {
        if (raf) return;
        raf = requestAnimationFrame(function () {
          raf = 0;
          var r = btn.getBoundingClientRect();
          var x = (e.clientX - r.left - r.width / 2) * 0.18;
          var y = (e.clientY - r.top - r.height / 2) * 0.28;
          btn.style.transform = 'translate(' + x.toFixed(1) + 'px,' +
                                (y - 2).toFixed(1) + 'px)';
        });
      });
      btn.addEventListener('pointerleave', function () { btn.style.transform = ''; });
    });
  }

  /* ------------------------------------------------------------------
     5. Parallax drift on section media
        A single scroll listener moves everything, so the cost stays flat
        however many elements are on the page.
     ------------------------------------------------------------------ */
  function parallax() {
    var items = $$('.nc-split .nc-media, .nc-phero::before');
    items = $$('.nc-split .nc-media');
    if (!items.length) return;
    items.forEach(function (el) { el.classList.add('nc-para'); });

    var ticking = false;
    function frame() {
      var vh = window.innerHeight;
      items.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.bottom < -100 || r.top > vh + 100) return;
        // -1 .. 1 across the viewport, scaled down hard: this should be felt,
        // not seen.
        var p = (r.top + r.height / 2 - vh / 2) / vh;
        el.style.transform = 'translateY(' + (p * -18).toFixed(1) + 'px)';
      });
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(frame); }
    }, { passive: true });
    frame();
  }

  function init() {
    splitHeadings();
    markReveals();
    observe();
    magnetic();
    parallax();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

/* ==========================================================================
   Background Paths
   --------------------------------------------------------------------------
   The technique from 21st.dev's "Modern Background Paths": a field of
   generated SVG curves whose stroke is animated so the lines appear to draw
   and flow continuously, each at its own rate.

   Rebuilt here in plain SVG + CSS keyframes rather than framer-motion —
   stroke-dashoffset is GPU-composited, so a field of 30 curves costs almost
   nothing and needs no library.
   ========================================================================== */
(function () {
  'use strict';

  // Drawn for everyone; with reduced motion the lines drift at a third of
  // the speed instead of disappearing (a slow ambient drift, not motion the
  // reader has to track).
  var SLOW = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 3 : 1;

  var host = document.querySelector('[data-nc-paths]');
  if (!host) return;

  var W = 1200, H = 620, COUNT = 30;
  var ns = 'http://www.w3.org/2000/svg';
  var svg = document.createElementNS(ns, 'svg');
  svg.setAttribute('class', 'nc-paths');
  svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
  svg.setAttribute('preserveAspectRatio', 'xMidYMid slice');
  svg.setAttribute('aria-hidden', 'true');
  svg.setAttribute('focusable', 'false');

  for (var i = 0; i < COUNT; i++) {
    var t = i / COUNT;

    // A long sweeping curve, each one offset from the last so the field reads
    // as one system rather than thirty unrelated lines.
    var y0 = -120 + t * (H + 240);
    var d = 'M -180 ' + (y0 + 90).toFixed(1) +
            ' C ' + (W * 0.22).toFixed(1) + ' ' + (y0 - 70 + i * 3).toFixed(1) +
            ', ' + (W * 0.58).toFixed(1) + ' ' + (y0 + 190 - i * 2).toFixed(1) +
            ', ' + (W + 180) + ' ' + (y0 + 20).toFixed(1);

    var p = document.createElementNS(ns, 'path');
    p.setAttribute('d', d);
    p.setAttribute('fill', 'none');
    p.setAttribute('stroke', i % 5 === 0 ? 'var(--nc-acc)' : '#ffffff');
    p.setAttribute('stroke-width', (0.5 + (i % 4) * 0.45).toFixed(2));
    p.setAttribute('stroke-linecap', 'round');
    p.style.opacity = (0.05 + (i % 6) * 0.028).toFixed(3);

    // Dash the stroke and slide the offset: the line draws itself, forever.
    var len = 2200 + (i % 7) * 260;
    p.style.strokeDasharray = (len * 0.42).toFixed(0) + ' ' + (len * 0.58).toFixed(0);
    p.style.animation = 'nc-path-flow ' + ((16 + (i % 9) * 2.6) * SLOW).toFixed(1) +
                        's linear infinite';
    p.style.animationDelay = (-i * 0.9).toFixed(1) + 's';
    p.style.setProperty('--dash', len);

    svg.appendChild(p);
  }

  host.insertBefore(svg, host.firstChild.nextSibling || null);
})();
