/* ===========================================================================
   CA Natasha & Co. — Lead Capture
   ---------------------------------------------------------------------------
   Every enquiry form on this site hands the visitor off to WhatsApp. If the
   visitor abandons that handoff, the lead is lost. This script records the
   lead on submit — BEFORE the WhatsApp tab opens — so the firm always has the
   name and number, whether or not the message is actually sent.

   It never blocks, never throws into the page, and never interferes with the
   existing form handlers. If the endpoint is unreachable the lead is queued in
   the browser and retried on the visitor's next page view.

   SETUP: paste your Google Apps Script Web App URL into LEAD_ENDPOINT below.
   Step-by-step instructions are in LEAD-CAPTURE-SETUP.md.
   =========================================================================== */
(function () {
  'use strict';

  /* ======================= CONFIGURE THIS ONE LINE ======================= */
  var LEAD_ENDPOINT = 'https://script.google.com/macros/s/AKfycbx2OG-NjMMu8xnX6Yuqwo1ew7p4eKSWmK5bkdyoVurWwGaibcx-CB-Qx54sGolysuQJ/exec';
  /* ====================================================================== */

  var QUEUE_KEY  = 'caLeadQueue.v1';
  var MAX_QUEUE  = 40;
  var BUSINESS   = 'Natasha & Co. Chartered Accountants';

  /* ---------------------------------------------------------------- utils */

  function safeLocal(fn, fallback) {
    /* Private mode and blocked site-data both throw on access. */
    try { return fn(); } catch (err) { return fallback; }
  }

  function readQueue() {
    return safeLocal(function () {
      return JSON.parse(window.localStorage.getItem(QUEUE_KEY) || '[]');
    }, []);
  }

  function writeQueue(list) {
    safeLocal(function () {
      window.localStorage.setItem(QUEUE_KEY, JSON.stringify(list.slice(-MAX_QUEUE)));
    });
  }

  function enqueue(payload) {
    var q = readQueue();
    q.push(payload);
    writeQueue(q);
  }

  /* --------------------------------------------------------------- sending */

  /* Apps Script accepts a text/plain body without a CORS preflight, and reads
     it from e.postData.contents. sendBeacon survives the navigation to
     WhatsApp, which a normal fetch would not reliably do. */
  function send(payload) {
    if (!LEAD_ENDPOINT) return false;
    var body = JSON.stringify(payload);

    if (navigator.sendBeacon) {
      try {
        var blob = new Blob([body], { type: 'text/plain;charset=utf-8' });
        if (navigator.sendBeacon(LEAD_ENDPOINT, blob)) return true;
      } catch (err) { /* fall through to fetch */ }
    }

    if (window.fetch) {
      try {
        window.fetch(LEAD_ENDPOINT, {
          method: 'POST',
          mode: 'no-cors',
          keepalive: true,
          headers: { 'Content-Type': 'text/plain;charset=utf-8' },
          body: body
        })['catch'](function () { enqueue(payload); });
        return true;
      } catch (err) { /* fall through */ }
    }
    return false;
  }

  function flushQueue() {
    if (!LEAD_ENDPOINT) return;
    var q = readQueue();
    if (!q.length) return;
    writeQueue([]);
    q.forEach(function (item) {
      if (!send(item)) enqueue(item);
    });
  }

  /* ------------------------------------------------------- field gathering */

  function labelFor(el) {
    return (el.id || el.name || el.getAttribute('placeholder') || '').trim();
  }

  /* Map the site's varied field ids (quick-name, inq-name, slot-name,
     calcLeadName ...) onto four clean columns for the spreadsheet. */
  function classify(key) {
    var k = key.toLowerCase();
    if (/name/.test(k) && !/username/.test(k)) return 'name';
    if (/phone|mobile|whatsapp|contact/.test(k))  return 'phone';
    if (/email|mail/.test(k))                     return 'email';
    if (/city|location|address/.test(k))          return 'city';
    if (/service|requirement|purpose/.test(k))    return 'service';
    return null;
  }

  function collect(form) {
    var fields = {};
    var summary = { name: '', phone: '', email: '', city: '', service: '' };
    var els = form.elements || [];

    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      if (!el || !el.type) continue;
      if (/^(submit|button|reset|file|password)$/i.test(el.type)) continue;
      if ((el.type === 'checkbox' || el.type === 'radio') && !el.checked) continue;

      var key = labelFor(el);
      var val = (el.value == null ? '' : String(el.value)).trim();
      if (!key || !val) continue;

      fields[key] = val;
      var slot = classify(key);
      if (slot && !summary[slot]) summary[slot] = val;
    }
    return { fields: fields, summary: summary };
  }

  /* --------------------------------------------------------------- capture */

  function capture(form) {
    var data = collect(form);

    /* A lead with neither a phone nor an email is not worth a row. */
    if (!data.summary.phone && !data.summary.email) return;

    var payload = {
      business:  BUSINESS,
      form:      form.getAttribute('data-lead') || 'unknown',
      name:      data.summary.name,
      phone:     data.summary.phone,
      email:     data.summary.email,
      city:      data.summary.city,
      service:   data.summary.service,
      fields:    data.fields,
      page:      window.location.pathname,
      url:       window.location.href,
      referrer:  document.referrer || '',
      userAgent: navigator.userAgent,
      submittedAt: new Date().toISOString()
    };

    if (!send(payload)) enqueue(payload);
  }

  /* Capture phase so this runs before the inline onsubmit handler calls
     preventDefault() and opens WhatsApp. Wrapped so that any failure here can
     never stop the visitor's actual submission. */
  document.addEventListener('submit', function (e) {
    try {
      var form = e.target;
      if (form && form.tagName === 'FORM' && form.hasAttribute('data-lead')) {
        capture(form);
      }
    } catch (err) { /* a broken analytics path must not break the form */ }
  }, true);

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', flushQueue);
  } else {
    flushQueue();
  }

  /* Exposed for manual use and for checking the backlog from the console. */
  window.caLeadCapture = {
    capture: capture,
    pending: function () { return readQueue().length; },
    flush:   flushQueue,
    configured: function () { return !!LEAD_ENDPOINT; }
  };
})();

/* ===========================================================================
   WhatsApp handoff + confirmation toast
   ---------------------------------------------------------------------------
   The site previously did:   alert("Thank you...");  window.open(waUrl, '_blank');

   That order loses the enquiry. A modal alert() ends the user-gesture window in
   most browsers, so the window.open() that follows is treated as an unrequested
   popup and is blocked silently — the visitor sees a thank-you and no WhatsApp.

   caWhatsApp() opens WhatsApp FIRST, while the click is still "trusted", using a
   synthetic anchor click (which popup blockers allow where window.open is
   refused), and only then shows a non-blocking toast.
   =========================================================================== */
(function () {
  'use strict';

  var WA_NUMBER = '919407000157';

  function injectStyles() {
    if (document.getElementById('caToastStyles')) return;
    var css = document.createElement('style');
    css.id = 'caToastStyles';
    css.textContent = [
      '.ca-toast-wrap{position:fixed;left:50%;bottom:26px;transform:translateX(-50%);',
      'z-index:2147483000;display:flex;flex-direction:column;gap:10px;',
      'width:min(420px,calc(100vw - 32px));pointer-events:none}',
      '.ca-toast{pointer-events:auto;display:flex;gap:12px;align-items:flex-start;',
      'background:#0b1b2e;color:#f1f5f9;border:1px solid rgba(255,255,255,.14);',
      'border-left:4px solid #22c55e;border-radius:10px;padding:14px 16px;',
      'box-shadow:0 18px 44px -14px rgba(0,0,0,.6);font-size:14px;line-height:1.55;',
      'font-family:inherit;opacity:0;transform:translateY(12px);',
      'transition:opacity .28s ease,transform .28s cubic-bezier(.16,1,.3,1)}',
      '.ca-toast.is-in{opacity:1;transform:translateY(0)}',
      '.ca-toast-ico{flex:0 0 auto;font-size:17px;line-height:1.35;color:#22c55e}',
      '.ca-toast-msg{flex:1 1 auto}',
      '.ca-toast-x{flex:0 0 auto;background:none;border:0;color:#94a3b8;cursor:pointer;',
      'font-size:19px;line-height:1;padding:0 2px}',
      '.ca-toast-x:hover{color:#fff}',
      '@media (prefers-reduced-motion:reduce){.ca-toast{transition:none;opacity:1;transform:none}}',
      '@media (max-width:575px){.ca-toast-wrap{bottom:84px}}'
    ].join('');
    document.head.appendChild(css);
  }

  function wrap() {
    var w = document.querySelector('.ca-toast-wrap');
    if (!w) {
      w = document.createElement('div');
      w.className = 'ca-toast-wrap';
      w.setAttribute('role', 'status');
      w.setAttribute('aria-live', 'polite');
      document.body.appendChild(w);
    }
    return w;
  }

  function toast(message, ms) {
    if (!message) return;
    try {
      injectStyles();
      var el = document.createElement('div');
      el.className = 'ca-toast';
      var ico = document.createElement('span');
      ico.className = 'ca-toast-ico';
      ico.textContent = '\u2713';
      var msg = document.createElement('span');
      msg.className = 'ca-toast-msg';
      msg.textContent = String(message).replace(/^[\u2705\s]+/, '');
      var x = document.createElement('button');
      x.className = 'ca-toast-x';
      x.type = 'button';
      x.setAttribute('aria-label', 'Dismiss');
      x.innerHTML = '&times;';
      el.appendChild(ico); el.appendChild(msg); el.appendChild(x);
      wrap().appendChild(el);

      requestAnimationFrame(function () { el.classList.add('is-in'); });
      var timer = setTimeout(close, ms || 6000);
      function close() {
        clearTimeout(timer);
        el.classList.remove('is-in');
        setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 300);
      }
      x.addEventListener('click', close);
    } catch (err) {
      /* never let a cosmetic toast break the enquiry */
    }
  }

  /* Anchor-click beats window.open against popup blockers, and falls back to a
     same-tab navigation on the browsers that still refuse it. */
  function openUrl(url) {
    try {
      var a = document.createElement('a');
      a.href = url;
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
      a.style.display = 'none';
      document.body.appendChild(a);
      a.click();
      setTimeout(function () { if (a.parentNode) a.parentNode.removeChild(a); }, 0);
      return true;
    } catch (err) {
      try { window.location.href = url; return true; } catch (e2) { return false; }
    }
  }

  function caWhatsApp(text, thankYou) {
    var url = 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(text || '');
    openUrl(url);                 // first, while the gesture is still trusted
    if (thankYou) toast(thankYou); // then, without blocking anything
    return false;
  }

  window.caWhatsApp = caWhatsApp;
  window.caToast    = toast;
  window.caOpenUrl  = openUrl;
})();

/* ===========================================================================
   Universal Modal Opener & "Consult CA" / "Request Quote" / "Book Consultation"
   ---------------------------------------------------------------------------
   Handles opening consultation/slot modals reliably across mobile, tablet,
   desktop, and touch devices. Closes active offcanvas navigation menus before
   opening modals and pre-selects the requested service.
   =========================================================================== */
(function () {
  'use strict';

  function caCloseModal(modalEl) {
    if (!modalEl) return;
    try {
      if (window.bootstrap && window.bootstrap.Modal) {
        var inst = window.bootstrap.Modal.getInstance(modalEl);
        if (inst) inst.hide();
      }
    } catch (err) {}
    modalEl.classList.remove('show');
    modalEl.style.display = 'none';
    modalEl.setAttribute('aria-hidden', 'true');
    modalEl.removeAttribute('aria-modal');
    var bds = document.querySelectorAll('.modal-backdrop');
    bds.forEach(function (bd) { bd.remove(); });
    document.body.classList.remove('modal-open');
    document.body.style.removeProperty('overflow');
    document.body.style.removeProperty('padding-right');
  }

  function caOpenModal(target) {
    var modalEl = typeof target === 'string' ? document.querySelector(target) : target;
    if (!modalEl) return false;

    // 1. Close any open mobile offcanvas first to avoid backdrop conflicts
    var openOffcanvas = document.querySelectorAll('.offcanvas.show');
    openOffcanvas.forEach(function (oc) {
      try {
        if (window.bootstrap && window.bootstrap.Offcanvas) {
          var ocInst = window.bootstrap.Offcanvas.getInstance(oc);
          if (ocInst) ocInst.hide();
        }
      } catch (e) {}
      oc.classList.remove('show');
    });

    var offcanvasBackdrops = document.querySelectorAll('.offcanvas-backdrop');
    offcanvasBackdrops.forEach(function (ob) { ob.remove(); });

    // 2. Open modal safely
    setTimeout(function () {
      try {
        if (window.bootstrap && window.bootstrap.Modal) {
          window.bootstrap.Modal.getOrCreateInstance(modalEl).show();
          return;
        }
      } catch (err) {}

      // Fallback display if bootstrap is unavailable or still loading
      modalEl.classList.add('show');
      modalEl.style.display = 'block';
      modalEl.setAttribute('aria-modal', 'true');
      modalEl.removeAttribute('aria-hidden');
      if (!document.querySelector('.modal-backdrop')) {
        var bd = document.createElement('div');
        bd.className = 'modal-backdrop fade show';
        document.body.appendChild(bd);
      }
      document.body.classList.add('modal-open');
    }, 120);

    return true;
  }

  window.caOpenModal  = caOpenModal;
  window.caCloseModal = caCloseModal;

  document.addEventListener('click', function (e) {
    // 1. Dismiss modal close button handling
    var dismissBtn = e.target && e.target.closest && e.target.closest('[data-bs-dismiss="modal"]');
    if (dismissBtn) {
      var pModal = dismissBtn.closest('.modal');
      if (pModal) {
        caCloseModal(pModal);
      }
      return;
    }

    // 2. "CONSULT CA" buttons on service cards
    var consultBtn = e.target && e.target.closest && e.target.closest('.btn-service-consult');
    if (consultBtn) {
      e.preventDefault();
      e.stopPropagation();

      var card = consultBtn.closest('.service-card-clean') || consultBtn.closest('.col-lg-4') || consultBtn.closest('.service-box') || consultBtn.closest('.col-md-6');
      var serviceTitle = '';
      if (card) {
        var hEl = card.querySelector('h3, h4, .service-title');
        if (hEl) serviceTitle = hEl.innerText.replace(/\s+/g, ' ').trim();
      }

      var modalEl = document.getElementById('consultationModal') || document.getElementById('slotBookingModal');
      if (modalEl) {
        var selectEl = modalEl.querySelector('#quote-service') || modalEl.querySelector('#slot-service') || modalEl.querySelector('select');
        if (selectEl && serviceTitle) {
          var titleLower = serviceTitle.toLowerCase();
          for (var i = 0; i < selectEl.options.length; i++) {
            var valLower = selectEl.options[i].value.toLowerCase();
            var txtLower = selectEl.options[i].text.toLowerCase();
            if (titleLower.includes('audit') && (valLower.includes('audit') || txtLower.includes('audit'))) {
              selectEl.selectedIndex = i; break;
            } else if (titleLower.includes('tax') && (valLower.includes('tax') || txtLower.includes('tax') || valLower.includes('itr'))) {
              selectEl.selectedIndex = i; break;
            } else if ((titleLower.includes('company') || titleLower.includes('incorporation') || titleLower.includes('llp')) && (valLower.includes('company') || valLower.includes('incorporation'))) {
              selectEl.selectedIndex = i; break;
            } else if (titleLower.includes('gst') && (valLower.includes('gst') || txtLower.includes('gst'))) {
              selectEl.selectedIndex = i; break;
            } else if ((titleLower.includes('advisory') || titleLower.includes('cfo') || titleLower.includes('financial')) && (valLower.includes('cfo') || valLower.includes('advisory'))) {
              selectEl.selectedIndex = i; break;
            } else if ((titleLower.includes('ngo') || titleLower.includes('trust')) && (valLower.includes('ngo') || valLower.includes('trust'))) {
              selectEl.selectedIndex = i; break;
            }
          }
        }
        caOpenModal(modalEl);
      }
      return;
    }

    // 3. "REQUEST QUOTE" or "Book Consultation" or "Let's Start Now" or "Book Slot"
    var modalTrigger = e.target && e.target.closest && e.target.closest('[data-bs-toggle="modal"], .btn-request-quote, .cine-btn-primary[data-bs-toggle], .sticky-action-btn.book-btn');
    if (modalTrigger) {
      var targetSelector = modalTrigger.getAttribute('data-bs-target') || modalTrigger.getAttribute('href');
      var targetModal = null;
      if (targetSelector && targetSelector.startsWith('#')) {
        targetModal = document.querySelector(targetSelector);
      }
      if (!targetModal) {
        if (modalTrigger.classList.contains('btn-request-quote') || modalTrigger.classList.contains('cine-btn-primary')) {
          targetModal = document.getElementById('consultationModal') || document.getElementById('slotBookingModal');
        } else if (modalTrigger.classList.contains('book-btn')) {
          targetModal = document.getElementById('slotBookingModal') || document.getElementById('consultationModal');
        }
      }
      if (targetModal) {
        e.preventDefault();
        e.stopPropagation();
        caOpenModal(targetModal);
      }
    }
  });
})();
