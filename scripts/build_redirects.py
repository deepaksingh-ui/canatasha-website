# -*- coding: utf-8 -*-
"""
Turn the retired duplicate URLs into proper redirect stubs.

vercel.json already 301s these server-side, which is what search engines act on.
These files are the fallback for any host that ignores that config: canonical to
the surviving URL, noindex, and a meta refresh so a human who lands here moves on.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nc_shell as S

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TPL = """<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Moved &mdash; {name}</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{site}/{dest}">
<meta http-equiv="refresh" content="0; url={dest}">
<meta name="description" content="This page has moved. Redirecting to {dest}.">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="stylesheet" href="assets/css/nc.css">
</head>
<body>
<main id="main" class="nc-sec" style="display:grid;place-items:center;min-height:70vh;text-align:center">
  <div class="nc-wrap nc-wrap-nar">
    <span class="nc-eyebrow">Page moved</span>
    <h1 style="font-size:clamp(1.8rem,4vw,2.6rem)">This article has a new home</h1>
    <p class="nc-lead">If you are not redirected automatically, follow the link below.</p>
    <p class="nc-mt2"><a class="nc-btn nc-btn-lg" href="{dest}">Continue to the article</a></p>
  </div>
</main>
</body>
</html>
"""


def main():
    cfg = json.load(io.open(os.path.join(ROOT, "vercel.json"), encoding="utf-8"))
    n = 0
    for r in cfg.get("redirects", []):
        src = r["source"].lstrip("/")
        dest = r["destination"].lstrip("/")
        if not src.endswith(".html"):
            continue
        path = os.path.join(ROOT, src)
        if not os.path.exists(path):
            continue
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(TPL.format(name=S.NAME_PLAIN, site=S.SITE, dest=dest))
        n += 1
        print("  stub  %-72s -> %s" % (src, dest))
    print("wrote %d redirect stubs" % n)


if __name__ == "__main__":
    main()
