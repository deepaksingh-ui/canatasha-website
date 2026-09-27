# -*- coding: utf-8 -*-
"""
On-page SEO crawl of the built site (reads the HTML files, no server needed).

    python scripts/seo_audit.py [out.json]

Complements validate.py, which enforces hard rules at build time. This one
measures: title/description length and duplication, H1 and heading order,
image alt text and weight, internal link integrity, orphan pages and click
depth from the home page, body length, and structured data types per page.
"""
import collections
import html as H
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {"admin-news-editor.html"}


def text_of(h):
    h = re.sub(r"(?is)<(script|style|noscript|svg)\b.*?</\1>", " ", h)
    h = re.sub(r"(?is)<(header|footer|nav)\b.*?</\1>", " ", h)
    h = re.sub(r'(?is)<div class="nc-(drawer|mega)[^"]*".*?</div>\s*</div>', " ", h)
    return H.unescape(re.sub(r"<[^>]+>", " ", h))


def main(out_path=None):
    pages = sorted(f for f in os.listdir(ROOT) if f.endswith(".html") and f not in SKIP)
    data, links = {}, collections.defaultdict(set)

    for f in pages:
        h = io.open(os.path.join(ROOT, f), encoding="utf-8", errors="ignore").read()
        stub = 'http-equiv="refresh"' in h
        g = lambda p: (re.findall(p, h, re.I | re.S) or [""])[0]
        title = H.unescape(g(r"<title>(.*?)</title>")).strip()
        desc = H.unescape(g(r'<meta name="description" content="([^"]*)"'))
        robots = g(r'<meta name="robots" content="([^"]*)"')
        heads = [int(x) for x in re.findall(r"<h([1-6])[\s>]", h)]
        skips = sum(1 for a, b in zip(heads, heads[1:]) if b > a + 1)
        imgs = re.findall(r"<img\b[^>]*>", h, re.I)
        no_alt = [i for i in imgs if not re.search(r'\balt="', i)]
        empty_alt = [i for i in imgs if re.search(r'\balt=""', i)]
        types = []
        for block in re.findall(r'(?is)<script type="application/ld\+json">(.*?)</script>', h):
            try:
                j = json.loads(block)
                t = j.get("@type")
                types += t if isinstance(t, list) else [t]
            except ValueError:
                types.append("INVALID")
        for href in re.findall(r'<a\b[^>]*\bhref="([^"#?]+)', h):
            if href.startswith(("http", "mailto:", "tel:", "javascript:", "//")):
                continue
            links[f].add(href.lstrip("./"))
        img_bytes = 0
        for src in re.findall(r'<img\b[^>]*\bsrc="([^"]+)"', h):
            p = os.path.join(ROOT, src.split("?")[0])
            if os.path.exists(p):
                img_bytes += os.path.getsize(p)
        data[f] = dict(
            stub=stub, title=title, tlen=len(title), desc=desc, dlen=len(desc),
            noindex="noindex" in robots, h1=heads.count(1), heading_skips=skips,
            words=len(text_of(h).split()), imgs=len(imgs), no_alt=len(no_alt),
            decorative=len(empty_alt), img_kb=img_bytes // 1024,
            html_kb=len(h.encode("utf-8")) // 1024, schema=sorted(set(types)))

    # link integrity + depth
    broken = sorted({(src, dst) for src, ds in links.items() for dst in ds
                     if dst and not os.path.exists(os.path.join(ROOT, dst))
                     and not dst.endswith((".xml", ".txt", ".pdf"))})
    inbound = collections.Counter(d for s, ds in links.items() for d in ds if d != s)
    depth, frontier = {"index.html": 0}, ["index.html"]
    while frontier:
        nxt = []
        for p in frontier:
            for d in links.get(p, ()):
                if d in data and d not in depth:
                    depth[d] = depth[p] + 1
                    nxt.append(d)
        frontier = nxt

    real = {f: d for f, d in data.items() if not d["stub"] and not d["noindex"] and f != "404.html"}
    dup_t = {t: c for t, c in collections.Counter(d["title"] for d in real.values()).items() if c > 1}
    dup_d = {t: c for t, c in collections.Counter(d["desc"] for d in real.values()).items() if c > 1}
    summary = dict(
        pages=len(real),
        titles_over_60=sorted(f for f, d in real.items() if d["tlen"] > 60),
        titles_under_30=sorted(f for f, d in real.items() if d["tlen"] < 30),
        desc_over_160=sorted(f for f, d in real.items() if d["dlen"] > 160),
        desc_under_120=sorted(f for f, d in real.items() if d["dlen"] < 120),
        duplicate_titles=dup_t, duplicate_descriptions=dup_d,
        h1_not_one=sorted(f for f, d in real.items() if d["h1"] != 1),
        heading_skips=sorted((f, d["heading_skips"]) for f, d in real.items() if d["heading_skips"]),
        images=sum(d["imgs"] for d in real.values()),
        images_missing_alt=sum(d["no_alt"] for d in real.values()),
        thin_under_300=sorted((f, d["words"]) for f, d in real.items() if d["words"] < 300),
        broken_internal_links=broken,
        orphans=sorted(f for f in real if inbound[f] == 0 and f != "index.html"),
        unreachable_from_home=sorted(f for f in real if f not in depth),
        depth_over_3=sorted((f, depth[f]) for f in real if depth.get(f, 0) > 3),
        heaviest_img_pages=sorted(((d["img_kb"], f) for f, d in real.items()), reverse=True)[:8],
        no_schema=sorted(f for f, d in real.items() if not d["schema"]),
        schema_types=collections.Counter(t for d in real.values() for t in d["schema"]),
    )
    report = dict(summary=summary, pages=data, depth=depth)
    if out_path:
        with io.open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=1, ensure_ascii=False, default=list)
    return report


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    r = main(sys.argv[1] if len(sys.argv) > 1 else None)
    for k, v in r["summary"].items():
        if isinstance(v, (list, dict, collections.Counter)):
            print("%-24s %s" % (k, (len(v), list(v.items())[:6] if isinstance(v, dict) else v[:6])))
        else:
            print("%-24s %s" % (k, v))
