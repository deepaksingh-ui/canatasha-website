/* ==========================================================================
   Hero contrast — measured from rendered pixels, per slide
   --------------------------------------------------------------------------
   Token maths is not enough here. The hero copy sits on a photograph that
   changes every 5.2s, so the same colour pair passes on the dark slides and
   fails on the bright ones. This walks all seven slides, hides the copy,
   screenshots what is actually behind each run of text, and reports the
   WORST pixel — not the average, because one blown-out highlight behind a
   word is exactly where reading breaks down.

   Usage:  node scripts/contrast_test.js [origin]
   Exits non-zero if anything falls below WCAG AA.
   ========================================================================== */
const puppeteer = require('puppeteer-core');
const PNG = require('pngjs').PNG;

function lin(c){c/=255;return c<=0.03928?c/12.92:Math.pow((c+0.055)/1.055,2.4);}
function lum(r,g,b){return 0.2126*lin(r)+0.7152*lin(g)+0.0722*lin(b);}
function ratio(a,b){const L1=Math.max(a,b),L2=Math.min(a,b);return (L1+0.05)/(L2+0.05);}

const ORIGIN = (process.argv[2] || 'http://127.0.0.1:8080').replace(/\/$/, '');

(async () => {
  const b = await puppeteer.launch({ executablePath: process.env.CHROME_PATH,
    headless: 'new', args: ['--no-sandbox'] });
  const p = await b.newPage();
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto(ORIGIN + '/index.html', { waitUntil: 'networkidle2' });
  await new Promise(r => setTimeout(r, 1800));

  await p.evaluate(() => {
    const z = document.querySelector('.nc-hero-nav');
    if (z) z.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
  });
  // Slides after the first load their photograph on demand (data-bg). Force
  // them all in and wait, or slides 2-7 would be measured over no photo.
  await p.evaluate(async () => {
    const figs = Array.from(document.querySelectorAll('.nc-hero-bg figure'));
    await Promise.all(figs.map(f => new Promise(done => {
      const src = f.dataset.bg || (f.style.backgroundImage.match(/url\("?([^")]+)/) || [])[1];
      if (f.dataset.bg) { f.style.backgroundImage = 'url("' + f.dataset.bg + '")'; f.removeAttribute('data-bg'); }
      if (!src) return done();
      const im = new Image(); im.onload = im.onerror = done; im.src = src;
    })));
  });
  const n = await p.evaluate(() => document.querySelectorAll('.nc-hero-bg figure').length);
  const rows = [];

  for (let i = 0; i < n; i++) {
    // Jump straight to slide i and freeze everything that moves.
    await p.evaluate((idx) => {
      document.querySelectorAll('.nc-hero-bg figure').forEach((f, j) => {
        f.classList.toggle('is-on', j === idx);
        f.style.animationPlayState = 'paused';
      });
      document.querySelectorAll('.nc-slide').forEach((s, j) =>
        s.classList.toggle('is-on', j === idx));
      document.querySelectorAll('svg.nc-paths path').forEach(x =>
        x.style.animationPlayState = 'paused');
    }, i);
    await new Promise(r => setTimeout(r, 900));
    const painted = await p.evaluate(() => getComputedStyle(document.querySelector('.nc-hero-bg figure.is-on')).backgroundImage);
    if (!/url\(/.test(painted)) throw new Error('slide ' + (i + 1) + ' has no photograph to measure against');

    const targets = await p.evaluate(() => {
      const on = document.querySelector('.nc-slide.is-on') || document;

      /* Sample the glyph line boxes, not the element box. An element box
         includes its own border ring and — on a pill with a 100px radius —
         four corners of bare photograph. Neither sits behind a letter, and
         both dragged the "worst pixel" down to numbers that described the
         chip's own orange border rather than anything a reader looks at.
         A Range over the text gives the line boxes instead. */
      const pick = (sel) => {
        const el = on.querySelector(sel);
        if (!el) return null;
        const rng = document.createRange();
        rng.selectNodeContents(el);
        const rects = Array.from(rng.getClientRects())
          .filter(r => r.width > 3 && r.height > 3)
          .map(r => ({
            // Inset vertically: a line box carries half-leading above and
            // below the glyphs, which is not ink.
            x: Math.round(r.x),
            y: Math.round(r.y + r.height * 0.18),
            w: Math.round(r.width),
            h: Math.max(2, Math.round(r.height * 0.64)),
          }));
        if (!rects.length) return null;
        return { sel, color: getComputedStyle(el).color, rects };
      };
      return [pick('h1, .nc-h1'), pick('.nc-lead'),
              pick('.nc-slide-eyebrow'), pick('.nc-btn-ghost')].filter(Boolean);
    });

    // Hide only the GLYPHS, never the boxes. Hiding whole elements was wrong:
    // the eyebrow paints its own background, so blanking the slide sampled the
    // photograph instead of the chip the text actually sits on. Backgrounds,
    // borders and veils all stay exactly as a visitor sees them.
    await p.evaluate(() => {
      document.querySelectorAll('.nc-slide.is-on *').forEach(e => {
        e.style.setProperty('color', 'transparent', 'important');
        e.style.setProperty('-webkit-text-fill-color', 'transparent', 'important');
        e.style.setProperty('text-shadow', 'none', 'important');
        // .nc-shimmer paints its text through a clipped gradient, which
        // survives a transparent fill; drop the image so it does not.
        if (e.classList.contains('nc-shimmer')) {
          e.style.setProperty('background-image', 'none', 'important');
        }
      });
    });
    await new Promise(r => setTimeout(r, 350));
    const buf = await p.screenshot({ type: 'png' });
    await p.evaluate(() => {
      document.querySelectorAll('.nc-slide.is-on *').forEach(e => {
        ['color', '-webkit-text-fill-color', 'text-shadow', 'background-image']
          .forEach(prop => e.style.removeProperty(prop));
      });
    });

    const png = PNG.sync.read(Buffer.from(buf));
    for (const t of targets) {
      const m = t.color.match(/[\d.]+/g).map(Number);
      const tl = lum(m[0], m[1], m[2]);
      let worst = Infinity, cnt = 0, sum = 0;
      for (const box of t.rects) {
        for (let y = box.y; y < box.y + box.h; y++) {
          for (let x = box.x; x < box.x + box.w; x++) {
            if (x < 0 || y < 0 || x >= png.width || y >= png.height) continue;
            const o = (png.width * y + x) << 2;
            const bl = lum(png.data[o], png.data[o+1], png.data[o+2]);
            const cr = ratio(tl, bl);
            if (cr < worst) worst = cr;
            sum += bl; cnt++;
          }
        }
      }
      if (!cnt) continue;
      rows.push({ slide: i + 1, el: t.sel, worst: +worst.toFixed(2),
                  avgBgLum: +(sum / cnt).toFixed(3) });
    }
  }
  await b.close();

  // h1 is large text, so AA is 3:1; everything else is 4.5:1.
  const limit = (el) => (el.indexOf('h1') !== -1 ? 3.0 : 4.5);
  let bad = 0;
  console.log('');
  console.log('  slide  element                worst   verdict');
  for (const r of rows) {
    const ok = r.worst >= limit(r.el);
    if (!ok) bad++;
    console.log('   ' + String(r.slide).padEnd(6) + r.el.padEnd(24) +
                String(r.worst).padStart(6) + '   ' + (ok ? 'ok' : 'FAIL'));
  }
  console.log('');
  console.log('  ' + rows.length + ' measurements, ' + bad + ' below AA.');
  console.log('');
  process.exit(bad ? 1 : 0);
})();
