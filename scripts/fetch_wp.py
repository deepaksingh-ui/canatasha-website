# -*- coding: utf-8 -*-
"""
One-time snapshot of the live WordPress site (www.canatasha.com).

The live site is WordPress + Elementor; the static build replaces it. Before
it goes, this pulls the firm's own service-page copy into
scripts/wp_snapshot/<slug>.json so the build can carry it forward without
depending on the old server still being up.

    python scripts/fetch_wp.py            # refresh the snapshot

Extraction keeps the text and its order only (headings, paragraphs, list
items). Elementor repeats every section heading as a small H6 eyebrow above
the real H3; those duplicates are dropped.
"""
import html as H
import io
import json
import os
import re
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "wp_snapshot")
LIVE = "https://www.canatasha.com"

PAGES = [
    "financial-statement-audit", "bank-audit", "concurrent-audit", "stock-audit",
    "statutory-audit", "tax-audit", "trade-mark", "iso-certification",
    "pasara-security-license", "gst-appeals", "pf-fund-appeals", "esic-appeals",
    "professional-tax-ptrc-ptec", "railway-tender-registration", "food-license-fssai",
    "import-export-consultancy-iec-code", "trade-license", "secured-loan-unsecured-loan",
    "labour-law-compliances", "income-tax-appeals-tribunals", "mining-project-reports",
    "training", "about",
]


def clean(fragment):
    t = H.unescape(re.sub(r"<[^>]+>", " ", fragment))
    return re.sub(r"\s+", " ", t).strip()


def extract(page_html):
    m = re.search(r'(?is)<div[^>]+data-elementor-type="wp-page".*?'
                  r'(?=<footer\b|data-elementor-type="footer")', page_html)
    body = m.group(0) if m else page_html
    body = re.sub(r"(?is)<(script|style|svg|form|noscript)\b.*?</\1>", " ", body)

    blocks = []
    for tag in re.finditer(r"(?is)<(h[1-6]|p|li)\b[^>]*>(.*?)</\1>", body):
        kind, text = tag.group(1).lower(), clean(tag.group(2))
        if not text:
            continue
        blocks.append([kind, text])

    # Drop Elementor's H6 eyebrows that merely repeat the next heading, and the
    # generic "Our Services" label above the title.
    out = []
    for i, (k, t) in enumerate(blocks):
        if k == "h6":
            nxt = blocks[i + 1][1] if i + 1 < len(blocks) else ""
            if t.rstrip(":").lower() == nxt.rstrip(":").lower() or t.lower() == "our services":
                continue
        out.append([k, t])

    title = next((t for k, t in out if k in ("h1", "h2")), "")
    words = sum(len(t.split()) for k, t in out)
    return {"title": title, "blocks": out, "words": words}


def main():
    os.makedirs(OUT, exist_ok=True)
    for slug in PAGES:
        url = "%s/%s/" % (LIVE, slug)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (site migration)"})
        with urllib.request.urlopen(req, timeout=40) as r:
            page = r.read().decode("utf-8", "ignore")
        data = extract(page)
        data.update(slug=slug, source=url,
                    meta_title=clean((re.findall(r"(?is)<title>(.*?)</title>", page) or [""])[0]))
        with io.open(os.path.join(OUT, slug + ".json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        print("  %-38s %4d words  %s" % (slug, data["words"], data["title"][:50]))


if __name__ == "__main__":
    main()
