# canatasha.com — Natasha & Company

Static site for an ISO 9001:2015 certified Chartered Accountancy firm in
Zone-1, M.P. Nagar, Bhopal. 64 pages, no framework, no build step at runtime.

## Rebuilding

```bash
python scripts/build.py
```

Regenerates every page from `backup/pre-redesign-20260905-134251/` (the
pre-redesign originals) plus the content defined in `scripts/`, then validates.
Safe to run repeatedly — it never reads its own output.

To check without rebuilding:

```bash
python scripts/validate.py
```

Local preview:

```bash
python -m http.server 8899
```

## How it fits together

| File | Role |
|---|---|
| `assets/css/nc.css` | The whole design system. Tokens, components, layout, motion. |
| `assets/js/nc.js` | All behaviour: gold beams canvas, nav, drawer, scroll reveal, counters, TOC, reading progress. No dependencies. |
| `assets/css/nc-compat.css` | Bootstrap-utility shim, calculator pages only. See below. |
| `scripts/nc_shell.py` | One source of truth for `<head>`, header, footer and structured data. |
| `scripts/nc_content.py` | Practice areas, FAQs, and the article index scanner. |
| `scripts/build_*.py` | One builder per page family. |
| `scripts/validate.py` | Post-build checks across all 64 pages. |

Change the header, footer or schema in `nc_shell.py` and every page picks it up
on the next build.

## Things worth knowing before you edit

**The calculators are not hand-styled.** `income-tax-calculator.html` and its
three siblings carry ~35KB of tax logic (FY 2025-26 / AY 2026-27, Finance Act
2025) wired to Bootstrap-classed markup by element id. `build_tools.py` copies
that markup and those scripts across byte for byte and lets `nc-compat.css`
restyle the utility classes. Nothing that computes a number was rewritten. If
you touch a calculator, edit the original in `backup/pre-redesign-*` and rebuild.

**`income-tax-calculator.html` was corrupt.** The original file held two
complete HTML documents concatenated, separated by an unclosed `<script>` at
line 509. Browsers treated the second document as script text, so the page hero
and consultation modal never rendered. `dedupe_document()` in `build_tools.py`
takes the later, complete document.

**Redirect stubs.** Seven slugs are 301'd in `vercel.json` and also written as
noindex stub pages, so they behave correctly on hosts that ignore that config.
`build_articles.py` skips them; `build_redirects.py` writes them. Order matters,
which is why `build.py` exists.

**`.vercelignore` is load-bearing.** Without it, `backup/` deploys as a
crawlable duplicate of every page on the site.

## Content

- Practice areas, FAQs and process steps: `scripts/nc_content.py`
- Article prose: migrated from the originals; edit the source in
  `backup/pre-redesign-*` and rebuild, or edit the generated file and add the
  slug to `HAND` in `build_articles.py` so it stops being overwritten.
- Long article headlines get a shorter `<title>` via `TITLE_OVERRIDES` in
  `build_articles.py`; the `<h1>` keeps the full headline.

## Open items

- **Contact form has no backend.** `contact-us.html` posts to a Formspree
  placeholder (`YOUR_FORM_ID`). Replace it, or wire the form to whatever
  `LEAD-CAPTURE-SETUP.md` describes, before relying on it.
- **Legal pages need review.** `privacy-policy.html` and
  `terms-and-conditions.html` were expanded from three short paragraphs to
  cover the DPDP Act 2023 and the ICAI Code of Ethics. They are a solid
  starting point, not vetted advice — confirm the retention periods and
  grievance contact match actual practice.
- **Images are unoptimised.** 23MB in `images/`, largest single file 1.3MB.
  Converting the PNGs to WebP would be the biggest remaining performance win.
- **Social profiles.** Footer and `sameAs` use the real LinkedIn, Facebook and
  Instagram accounts found in the old markup. The Twitter/X handle
  (`@canatasharaj`) is in `sameAs` but not linked in the footer — add it if the
  account is still active, remove it from `SAME_AS` if not.
