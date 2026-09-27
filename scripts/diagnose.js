/* Pinpoint what overflows, and why the counters sit at zero. */
const puppeteer = require('puppeteer-core');
const fs = require('fs');

const CHROME = [
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
].find(p => fs.existsSync(p));

const BASE = 'http://127.0.0.1:8899';

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'new',
    args: ['--no-sandbox', '--enable-webgl', '--use-gl=swiftshader',
           '--enable-unsafe-swiftshader'],
  });

  for (const slug of ['knowledge-base.html', 'tax-audit-44ab-bhopal.html']) {
    const page = await browser.newPage();
    await page.setRequestInterception(true);
    page.on('request', r => (r.url().startsWith(BASE) ? r.continue() : r.abort()));
    await page.setViewport({ width: 390, height: 844 });
    await page.goto(`${BASE}/${slug}`, { waitUntil: 'domcontentloaded' });
    await new Promise(r => setTimeout(r, 800));

    const wide = await page.evaluate(() => {
      const limit = document.documentElement.clientWidth;
      const out = [];
      document.querySelectorAll('*').forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.width === 0) return;
        if (r.right > limit + 1 || r.left < -1) {
          out.push({
            tag: el.tagName.toLowerCase(),
            cls: (el.className && el.className.toString().slice(0, 54)) || '',
            left: Math.round(r.left),
            right: Math.round(r.right),
            w: Math.round(r.width),
          });
        }
      });
      // deepest offenders first, they are the actual cause
      return out.slice(-12);
    });
    console.log(`\n── ${slug} @390px — elements past the viewport`);
    wide.forEach(w =>
      console.log(`   ${w.tag.padEnd(7)} w=${String(w.w).padStart(5)}  ${w.left}→${w.right}  .${w.cls}`));
    await page.close();
  }

  // counters
  const page = await browser.newPage();
  await page.setRequestInterception(true);
  page.on('request', r => (r.url().startsWith(BASE) ? r.continue() : r.abort()));
  await page.setViewport({ width: 1440, height: 900 });
  await page.goto(`${BASE}/index.html`, { waitUntil: 'domcontentloaded' });
  await new Promise(r => setTimeout(r, 700));
  await page.evaluate(() => document.querySelector('.nc-hero-stats').scrollIntoView({block:'center'}));
  await new Promise(r => setTimeout(r, 2500));

  const info = await page.evaluate(() => {
    const els = Array.from(document.querySelectorAll('[data-count]'));
    return {
      count: els.length,
      reduced: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
      hasIO: 'IntersectionObserver' in window,
      sample: els.map(e => ({
        target: e.getAttribute('data-count'),
        text: e.textContent,
        visible: e.getBoundingClientRect().top < window.innerHeight,
        opacity: getComputedStyle(e.closest('[data-nc-rise]') || e).opacity,
      })),
    };
  });
  console.log('\n── counters');
  console.log('   found:', info.count, '| reduced-motion:', info.reduced, '| IO:', info.hasIO);
  info.sample.forEach(s =>
    console.log(`   target=${s.target} text="${s.text}" visible=${s.visible} wrapperOpacity=${s.opacity}`));

  await browser.close();
})();
