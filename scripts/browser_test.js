/* Real-browser checks: does the page actually run, animate and lay out?
   Static validation cannot see a JS error or an element that never reveals.

   Usage:  node scripts/browser_test.js [baseUrl]
*/
const puppeteer = require('puppeteer-core');
const fs = require('fs');

/* Use the Chrome already on this machine rather than downloading one. */
const CHROME = [
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
].find(p => { try { return fs.existsSync(p); } catch (e) { return false; } });
if (!CHROME) { console.error('No Chrome/Edge found.'); process.exit(2); }

const BASE = process.argv[2] || 'http://127.0.0.1:8899';

const PAGES = [
  'index.html',
  'services.html',
  'about-us.html',
  'contact-us.html',
  'knowledge-base.html',
  'blog.html',
  'tax-audit-44ab-bhopal.html',
  'virtual-cfo-services-bhopal.html',
  'income-tax-calculator.html',
  'understanding-advance-tax-payment-and-the-need-to-file-itr.html',
  // carried over from WordPress: the longest and the list-heaviest
  'food-license-fssai.html',
  'bank-audit.html',
];

const VIEWPORTS = [
  { name: 'desktop', width: 1440, height: 900 },
  { name: 'tablet', width: 820, height: 1180 },
  { name: 'mobile', width: 390, height: 844 },
];

let failures = 0;
const note = (ok, msg) => {
  if (!ok) failures++;
  console.log(`    ${ok ? 'ok  ' : 'FAIL'}  ${msg}`);
};

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'new',
    args: ['--no-sandbox', '--enable-webgl', '--use-gl=swiftshader',
           '--enable-unsafe-swiftshader', '--disable-dev-shm-usage'],
  });

  // ---- home-page specifics
  console.log('\n── index.html: motion features');
  const page = await browser.newPage();
  await page.setRequestInterception(true);
  page.on('request', r => (r.url().startsWith(BASE) ? r.continue() : r.abort()));
  await page.setViewport(VIEWPORTS[0]);
  /* Chrome throttles requestAnimationFrame in background tabs, which stalls
     the counters. Bring this page to the front before checking motion. */
  await page.bringToFront();
  await page.goto(`${BASE}/index.html`, { waitUntil: 'domcontentloaded' });
  await new Promise(r => setTimeout(r, 1200));

  const liquid = await page.evaluate(() => {
    const l = document.querySelector('.nc-liquid');
    if (!l) return 'absent';
    const blobs = l.querySelectorAll('i');
    const anim = getComputedStyle(blobs[0]).animationName;
    return blobs.length === 3 && anim && anim !== 'none' ? 'animating' : 'static';
  });
  note(liquid === 'animating', `liquid aurora background ${liquid}`);

  const carousel = await page.evaluate(async () => {
    const first = document.querySelector('.nc-slide.is-on');
    const bgFirst = document.querySelector('.nc-hero-bg figure.is-on');
    document.querySelector('[data-nc-slide="next"]').click();
    await new Promise(r => setTimeout(r, 800));
    return {
      slideMoved: document.querySelector('.nc-slide.is-on') !== first,
      bgMoved: document.querySelector('.nc-hero-bg figure.is-on') !== bgFirst,
    };
  });
  note(carousel.slideMoved, 'hero carousel advances on arrow click');
  note(carousel.bgMoved, 'hero background photo changes with the slide');

  /* Counters get their own page. This harness runs Chrome on software GL,
     where the aurora shader drags the frame rate to roughly 5fps, so the
     count needs a much longer window here than the 1.8s it takes on real
     hardware. */
  const cPage = await browser.newPage();
  await cPage.setRequestInterception(true);
  cPage.on('request', r => (r.url().startsWith(BASE) ? r.continue() : r.abort()));
  await cPage.setViewport(VIEWPORTS[0]);
  await cPage.bringToFront();
  await cPage.goto(`${BASE}/index.html`, { waitUntil: 'domcontentloaded' });
  await new Promise(r => setTimeout(r, 900));
  const counters = await cPage.evaluate(async () => {
    const s = document.querySelector('.nc-hero-stats');
    window.scrollTo(0, s.getBoundingClientRect().top + window.scrollY - 300);
    await new Promise(r => setTimeout(r, 7000));
    return Array.from(document.querySelectorAll('[data-count]'))
      .map(e => e.textContent.trim());
  });
  await cPage.close();
  await page.bringToFront();
  note(counters.every(v => v !== '0' && v !== ''),
       `counters animated → ${counters.join(', ')}`);

  const dirs = await page.evaluate(() => {
    const s = new Set();
    document.querySelectorAll('.nc-grid > [data-nc-rise]')
      .forEach(e => s.add(e.getAttribute('data-nc-rise')));
    return Array.from(s);
  });
  note(dirs.length >= 3, `grid entry directions vary → ${dirs.join(', ')}`);

  /* Hover on a practice card must do four things at once: lift the card,
     zoom the photo, fade the overlay in, and flip the title bar. */
  await page.evaluate(() => {
    const s = document.querySelector('#practices');
    window.scrollTo(0, s.getBoundingClientRect().top + window.scrollY - 90);
  });
  await new Promise(r => setTimeout(r, 1800));
  const spot = await page.evaluate(() => {
    const r = document.querySelector('.nc-pcard').getBoundingClientRect();
    return { x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 3) };
  });
  const read = () => page.evaluate(() => {
    const c = document.querySelector('.nc-pcard');
    const img = c.querySelector('.nc-pcard-img');
    return {
      lift: getComputedStyle(c).transform,
      zoom: getComputedStyle(c.querySelector('img')).transform,
      overlay: getComputedStyle(img, '::before').opacity,
      bar: getComputedStyle(c.querySelector('.nc-pcard-bar')).backgroundColor,
    };
  });
  const cold = await read();
  await page.mouse.move(spot.x, spot.y);
  await new Promise(r => setTimeout(r, 800));
  const hot = await read();
  note(hot.lift !== cold.lift, `card lifts on hover`);
  note(hot.zoom !== cold.zoom, `card photo zooms on hover`);
  note(parseFloat(hot.overlay) > 0.8 && parseFloat(cold.overlay) < 0.2,
       `image overlay fades in (${cold.overlay} → ${hot.overlay})`);
  note(hot.bar !== cold.bar, `title bar changes colour (${cold.bar} → ${hot.bar})`);
  await page.mouse.move(0, 0);

  /* The first screen must fit: badge through stat rail, inside the viewport. */
  for (const vp of [{ w: 1920, h: 1080 }, { w: 1440, h: 900 }, { w: 1366, h: 768 }]) {
    await page.setViewport({ width: vp.w, height: vp.h });
    await page.evaluate(() => window.scrollTo(0, 0));
    await new Promise(r => setTimeout(r, 700));
    const fits = await page.evaluate(() => {
      const s = document.querySelector('.nc-hero-stats');
      return Math.round(s.getBoundingClientRect().bottom) <= window.innerHeight;
    });
    note(fits, `hero fits the first screen at ${vp.w}x${vp.h}`);
  }
  await page.setViewport(VIEWPORTS[0]);

  /* The news / due-date / blog feeds scroll on their own and stop on hover. */
  await page.evaluate(() => {
    const s = document.querySelector('.nc-parallax');
    window.scrollTo(0, s.getBoundingClientRect().top + window.scrollY - 40);
  });
  await new Promise(r => setTimeout(r, 1600));
  const track = () => page.evaluate(() =>
    getComputedStyle(document.querySelector('.nc-ticker-track')).transform);
  const a1 = await track();
  await new Promise(r => setTimeout(r, 2000));
  const a2 = await track();
  note(a1 !== a2, 'news ticker scrolls on its own');

  const tbox = await page.evaluate(() => {
    const r = document.querySelector('.nc-ticker').getBoundingClientRect();
    return { x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2) };
  });
  await page.mouse.move(tbox.x, tbox.y);
  await new Promise(r => setTimeout(r, 500));
  const h1 = await track();
  await new Promise(r => setTimeout(r, 1400));
  const h2 = await track();
  note(h1 === h2, 'ticker pauses while hovered');
  await page.mouse.move(0, 0);

  /* Phones: the slideshow must keep moving after a tap, and on devices that
     report reduced motion (Android battery saver turns it on). Both used to
     leave the hero frozen on its first slide. */
  {
    const ph = await browser.newPage();
    await ph.setViewport({ width: 390, height: 844, isMobile: true, hasTouch: true });
    await ph.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'reduce' }]);
    await ph.goto(BASE + '/index.html', { waitUntil: 'networkidle2' });
    const at = () => ph.evaluate(() => Array.prototype.findIndex.call(
      document.querySelectorAll('.nc-hero-bg figure'), f => f.classList.contains('is-on')));
    await ph.tap('.nc-slide.is-on .nc-slide-eyebrow');
    const before = await at();
    await new Promise(r => setTimeout(r, 7200));
    const after = await at();
    const lines = await ph.evaluate(() => !!document.querySelector('svg.nc-paths path'));
    note(after !== before, `phone, reduced motion, after a tap: slideshow still advances (${before} -> ${after})`);
    note(lines, 'phone, reduced motion: background lines still drawn');
    await ph.close();
  }

  /* Brand + team: the client's own logo and photographs, not placeholders. */
  const brand = await page.evaluate(async () => {
    const ok = (img) => !!img && img.complete && img.naturalWidth > 0;
    const hdr = document.querySelector('.nc-hdr .nc-logo img');
    const ftr = document.querySelector('.nc-ftr .nc-logo img');
    // lazy-loaded: bring it into view and let it decode before judging it
    ftr.scrollIntoView({ block: 'center' });
    await new Promise(r => setTimeout(r, 700));
    if (ftr.decode) await ftr.decode().catch(() => {});
    const cards = Array.from(document.querySelectorAll('#team .nc-team'));
    for (const c of cards) c.scrollIntoView({ block: 'center' });
    await new Promise(r => setTimeout(r, 900));
    const photos = cards.map(c => c.querySelector('img'));
    await Promise.all(photos.map(i => i.decode ? i.decode().catch(() => {}) : 0));
    const dr = getComputedStyle(document.querySelector('.nc-drawer'));
    return {
      hdr: ok(hdr) && /brand\/logo-horizontal/.test(hdr.currentSrc),
      ftr: ok(ftr) && /logo-horizontal-white/.test(ftr.currentSrc),
      team: cards.length,
      photos: photos.filter(i => ok(i) && /brand\/team-/.test(i.currentSrc)).length,
      drawerHidden: dr.visibility === 'hidden' && dr.boxShadow === 'none',
      icon: !!document.querySelector('link[rel="apple-touch-icon"][href*="brand"]'),
    };
  });
  note(brand.hdr, 'header shows the client logo');
  note(brand.ftr, 'footer shows the white logo variant');
  note(brand.team === 3 && brand.photos === 3, `team: ${brand.photos}/${brand.team} real photographs loaded`);
  note(brand.drawerHidden, 'closed drawer casts no shadow and is not tabbable');
  note(brand.icon, 'brand app icon linked');

  const tc = await page.$$('#team .nc-team');
  if (tc.length) {
    const bb = await tc[0].boundingBox();
    await page.mouse.move(bb.x + bb.width / 2, bb.y + bb.height / 3);
    await new Promise(r => setTimeout(r, 900));
    const shown = await tc[0].evaluate(c => +getComputedStyle(c.querySelector('.nc-team-over p')).opacity);
    note(shown > 0.95, `team bio rises on hover (opacity ${shown})`);
    await page.mouse.move(5, 5);
  }

  /* Background paths + a photo that keeps moving and keeps changing, with the
     pointer resting mid-screen the way a real visitor's does. The carousel
     once paused on hover over the whole hero, which meant it never advanced. */
  const bg = await page.evaluate(() => {
    const s = document.querySelector('svg.nc-paths');
    const fig = document.querySelector('.nc-hero-bg figure.is-on');
    return {
      paths: s ? s.querySelectorAll('path').length : 0,
      flowing: s ? getComputedStyle(s.querySelector('path')).animationName : 'none',
      kenburns: fig ? getComputedStyle(fig).animationName : 'none',
    };
  });
  note(bg.paths >= 20, `background paths drawn (${bg.paths})`);
  note(bg.flowing === 'nc-path-flow', 'background paths animate');
  note(bg.kenburns === 'nc-kenburns', 'hero photo drifts continuously');

  await page.mouse.move(800, 400);
  const rotated = await page.evaluate(async () => {
    const at = () => Array.prototype.findIndex.call(
      document.querySelectorAll('.nc-hero-bg figure'), f => f.classList.contains('is-on'));
    const a = at();
    await new Promise(r => setTimeout(r, 6200));
    return a !== at();
  });
  note(rotated, 'photo keeps changing with the pointer resting on the hero');
  await page.mouse.move(5, 5);

  /* Motion layer: headings split into words, photos wipe in behind a mask,
     and a keyword band scrolls. These run on every page, not just home. */
  const motion = await page.evaluate(() => ({
    words: document.querySelectorAll('.nc-word').length,
    reveals: document.querySelectorAll('.nc-reveal').length,
    marquee: document.querySelectorAll('.nc-marquee-track').length,
  }));
  note(motion.words > 20, `headings split into ${motion.words} animated words`);
  note(motion.reveals > 5, `${motion.reveals} images set to wipe in`);
  note(motion.marquee === 1, 'keyword marquee present');

  const marqMoved = await page.evaluate(async () => {
    const tr = document.querySelector('.nc-marquee-track');
    const a = getComputedStyle(tr).transform;
    await new Promise(r => setTimeout(r, 1500));
    return a !== getComputedStyle(tr).transform;
  });
  note(marqMoved, 'keyword marquee scrolls');

  const fired = await page.evaluate(async () => {
    window.scrollTo(0, document.body.scrollHeight * 0.35);
    await new Promise(r => setTimeout(r, 1500));
    return {
      heads: document.querySelectorAll('h1.is-in, h2.is-in').length,
      imgs: document.querySelectorAll('.nc-reveal.is-in').length,
    };
  });
  note(fired.heads > 0 && fired.imgs > 0,
       `on scroll: ${fired.heads} headings and ${fired.imgs} images revealed`);
  await page.evaluate(() => window.scrollTo(0, 0));
  await new Promise(r => setTimeout(r, 600));

  /* Nav labels must never wrap — "Knowledge Bank" broke onto two lines once
     the bar got crowded, which reads as broken rather than dense. */
  for (const w of [1920, 1600, 1440, 1280, 1120]) {
    await page.setViewport({ width: w, height: 950 });
    await new Promise(r => setTimeout(r, 400));
    const wrapped = await page.evaluate(() => {
      const bad = [];
      document.querySelectorAll('.nc-nav > ul > li > a').forEach(a => {
        const tn = Array.from(a.childNodes).find(n => n.nodeType === 3 && n.textContent.trim());
        if (!tn) return;
        const r = document.createRange();
        r.selectNodeContents(tn);
        if (r.getClientRects().length > 1) bad.push(a.textContent.trim());
      });
      return bad;
    });
    note(wrapped.length === 0, `nav fits on one line at ${w}px${wrapped.length ? ' → ' + wrapped.join(', ') : ''}`);
  }
  await page.setViewport(VIEWPORTS[0]);

  /* Knowledge Bank: category column drives the link panel beside it. */
  await page.evaluate(() => window.scrollTo(0, 0));
  await new Promise(r => setTimeout(r, 500));
  const kbNav = await page.evaluate(() => {
    const li = Array.from(document.querySelectorAll('.nc-nav > ul > li'))
      .find(l => /Knowledge Bank/.test(l.textContent));
    if (!li) return null;
    const r = li.getBoundingClientRect();
    return { x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2) };
  });
  note(!!kbNav, 'Knowledge Bank appears in the nav');
  if (kbNav) {
    await page.mouse.move(kbNav.x, kbNav.y);
    await new Promise(r => setTimeout(r, 700));
    const kb = await page.evaluate(() => {
      const d = document.querySelector('.nc-drop-mega');
      return {
        open: getComputedStyle(d).visibility === 'visible',
        cats: document.querySelectorAll('.nc-mega-cat').length,
        links: document.querySelectorAll('.nc-mega-panel a').length,
        shown: document.querySelector('.nc-mega-panel.is-on').querySelectorAll('a').length,
      };
    });
    note(kb.open, `mega-menu opens (${kb.cats} categories, ${kb.links} links)`);
    const swapped = await page.evaluate(async () => {
      const before = document.querySelector('.nc-mega-cat.is-on').textContent.trim();
      document.querySelectorAll('.nc-mega-cat')[4]
        .dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
      await new Promise(r => setTimeout(r, 400));
      return document.querySelector('.nc-mega-cat.is-on').textContent.trim() !== before;
    });
    note(swapped, 'mega-menu switches category on hover');
    await page.mouse.move(0, 400);
  }

  /* Frame rate, measured with nothing hovered and over three samples. A single
     sample on software rendering swings widely with machine load; the median
     still catches a real problem — the blurred-layer version of this
     background measured 11fps here. */
  await page.mouse.move(5, 500);
  await new Promise(r => setTimeout(r, 800));
  const samples = [];
  for (let i = 0; i < 3; i++) {
    samples.push(await page.evaluate(async () => {
      let frames = 0;
      const t0 = performance.now();
      await new Promise(res => {
        (function f() {
          frames++;
          performance.now() - t0 < 1000 ? requestAnimationFrame(f) : res();
        })();
      });
      return frames;
    }));
  }
  samples.sort((a, b) => a - b);
  const fps = samples[1];
  note(fps >= 24,
       `frame rate healthy with the background running (median ${fps}fps of ${samples.join('/')})`);

  await page.close();

  for (const slug of PAGES) {
    console.log(`\n── ${slug}`);
    const page = await browser.newPage();

    const errors = [];
    page.on('pageerror', e => errors.push('JS: ' + e.message));
    page.on('console', m => {
      /* Requests to the font CDN are aborted by this harness on purpose, so
         the resulting console noise is not a site defect. */
      if (m.type() === 'error' && !/ERR_FAILED|ERR_BLOCKED|net::/.test(m.text())) {
        errors.push('console: ' + m.text());
      }
    });
    const bad = [];
    /* Only same-origin assets are the site's responsibility; the font CDN is
       unreachable from this sandbox and would otherwise stall the load. */
    await page.setRequestInterception(true);
    page.on('request', r => {
      if (r.url().startsWith(BASE)) r.continue();
      else r.abort();
    });
    page.on('requestfailed', r => {
      if (r.url().startsWith(BASE)) bad.push(r.url());
    });
    page.on('response', r => {
      if (r.status() >= 400 && r.url().startsWith(BASE)) {
        bad.push(`${r.status()} ${r.url()}`);
      }
    });

    await page.setViewport(VIEWPORTS[0]);
    await page.goto(`${BASE}/${slug}`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await new Promise(r => setTimeout(r, 900));   // let deferred scripts boot

    note(errors.length === 0, `no JS errors ${errors.length ? '→ ' + errors[0].slice(0, 110) : ''}`);
    note(bad.length === 0, `all assets load ${bad.length ? '→ ' + bad[0].slice(0, 90) : ''}`);

    // header actually visible (this regressed once behind the top bars)
    const hdr = await page.evaluate(() => {
      const h = document.querySelector('.nc-hdr');
      if (!h) return null;
      const r = h.getBoundingClientRect();
      const mid = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
      return { h: r.height, top: r.top, covered: !h.contains(mid) };
    });
    note(hdr && hdr.h > 40 && !hdr.covered, `header visible and on top (h=${hdr && Math.round(hdr.h)})`);

    // nav reachable
    const navCount = await page.evaluate(() =>
      document.querySelectorAll('.nc-nav > ul > li').length);
    note(navCount >= 6, `nav has ${navCount} top-level items`);

    // scroll reveals fire
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight / 2));
    await new Promise(r => setTimeout(r, 1100));
    const rev = await page.evaluate(() => {
      const all = document.querySelectorAll('[data-nc-rise]');
      const shown = document.querySelectorAll('[data-nc-rise].is-in');
      return { all: all.length, shown: shown.length };
    });
    note(rev.all > 0 && rev.shown > 0, `reveals: ${rev.shown}/${rev.all} triggered`);

    // no sideways scroll at any width
    for (const vp of VIEWPORTS) {
      await page.setViewport(vp);
      await new Promise(r => setTimeout(r, 350));
      const over = await page.evaluate(() =>
        document.documentElement.scrollWidth - document.documentElement.clientWidth);
      note(over <= 1, `${vp.name} (${vp.width}px): no horizontal scroll (${over}px)`);
    }

    // mobile menu opens
    await page.setViewport(VIEWPORTS[2]);
    await new Promise(r => setTimeout(r, 250));
    const drawer = await page.evaluate(async () => {
      const b = document.querySelector('.nc-burger');
      if (!b) return 'no burger';
      b.click();
      await new Promise(r => setTimeout(r, 550));
      const d = document.querySelector('.nc-drawer');
      const open = document.body.classList.contains('nc-menu-open');
      const x = d ? d.getBoundingClientRect().left : 9999;
      return open && x < window.innerWidth ? 'opens' : `stuck (open=${open}, x=${x})`;
    });
    note(drawer === 'opens', `mobile drawer ${drawer}`);

    await page.close();
  }

  await browser.close();

  console.log(`\n${'='.repeat(56)}`);
  console.log(failures === 0 ? '  All browser checks passed.' : `  ${failures} check(s) failed.`);
  process.exit(failures === 0 ? 0 : 1);
})();
