# -*- coding: utf-8 -*-
"""Post-build validation across every page."""
import collections
import glob
import html
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nc_shell as S

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
issues = collections.defaultdict(list)


def add(kind, msg):
    issues[kind].append(msg)


CONSULT_LABELS = {"book a consultation", "request a consultation"}
CALENDLY_SCRIPT = "https://assets.calendly.com/assets/external/widget.js"


def check_booking(real):
    """Calendly booking flow: one page carries the embed, every CTA points at it.

    With no CALENDLY_URL configured there is no booking page and the buttons
    keep going to the contact form, so nothing on the site is a dead end.
    """
    url = getattr(S, "CALENDLY_URL", None)
    book = getattr(S, "BOOK_URL", None)
    if url is None or book is None:
        add("booking", "nc_shell defines no CALENDLY_URL / BOOK_URL")
        return

    target = "book-consultation.html" if url else "contact-us.html"
    if book != target:
        add("booking", "BOOK_URL is %r, expected %r" % (book, target))

    exists = os.path.exists(os.path.join(ROOT, "book-consultation.html"))
    if url and not exists:
        add("booking", "CALENDLY_URL is set but book-consultation.html was not built")
    if not url and exists:
        add("booking", "book-consultation.html exists but no CALENDLY_URL is set")

    for slug in real:
        t = io.open(os.path.join(ROOT, slug), encoding="utf-8").read()

        for m in re.finditer(r"<a\b([^>]*)>(.*?)</a>", t, re.S):
            label = re.sub(r"<[^>]+>|&[a-z]+;", "", m.group(2)).strip().lower()
            href = re.search(r'href="([^"]*)"', m.group(1))
            if label in CONSULT_LABELS and href and href.group(1) != target:
                add("booking", "%s: '%s' goes to %s, not %s" % (slug, label, href.group(1), target))

        embeds = "calendly-inline-widget" in t or "assets.calendly.com" in t
        if slug == "book-consultation.html":
            if 'calendly-inline-widget' not in t or 'data-url="%s' % html.escape(url) not in t:
                add("booking", "%s: no inline widget pointing at CALENDLY_URL" % slug)
            if t.count(CALENDLY_SCRIPT) != 1:
                add("booking", "%s: expected the Calendly script exactly once" % slug)
        elif embeds:
            add("booking", "%s: loads Calendly but is not the booking page" % slug)


def main():
    pages = sorted(glob.glob(os.path.join(ROOT, "*.html")))
    stubs = set()
    real = []

    for path in pages:
        slug = os.path.basename(path)
        t = io.open(path, encoding="utf-8").read()

        if 'http-equiv="refresh"' in t:
            stubs.add(slug)
            if 'content="noindex' not in t:
                add("stub", "%s: redirect stub missing noindex" % slug)
            if 'rel="canonical"' not in t:
                add("stub", "%s: redirect stub missing canonical" % slug)
            continue

        real.append(slug)
        noindex = 'name="robots" content="noindex' in t

        # --- head essentials
        if t.count("<title>") != 1:
            add("head", "%s: %d <title> tags" % (slug, t.count("<title>")))
        if t.count('name="viewport"') != 1:
            add("head", "%s: %d viewport tags" % (slug, t.count('name="viewport"')))
        if "maximum-scale=1" in t or "user-scalable=0" in t:
            add("a11y", "%s: viewport blocks pinch-zoom" % slug)
        if not noindex and t.count('rel="canonical"') != 1:
            add("head", "%s: %d canonical tags" % (slug, t.count('rel="canonical"')))
        if not noindex and t.count('property="og:title"') != 1:
            add("head", "%s: missing og:title" % slug)
        if not noindex and t.count('name="twitter:card"') != 1:
            add("head", "%s: missing twitter:card" % slug)

        # --- description length
        m = re.search(r'<meta name="description" content="([^"]*)"', t)
        if not m:
            add("head", "%s: no meta description" % slug)
        else:
            n = len(m.group(1))
            if n < 70:
                add("meta-len", "%s: description only %d chars" % (slug, n))
            elif n > 320:
                add("meta-len", "%s: description %d chars (will truncate)" % (slug, n))

        # --- title length
        m = re.search(r"<title>(.*?)</title>", t, re.S)
        if m and len(m.group(1)) > 75:
            add("meta-len", "%s: title %d chars" % (slug, len(m.group(1))))

        # --- headings
        h1 = len(re.findall(r"<h1[\s>]", t))
        if h1 != 1:
            add("headings", "%s: %d <h1>" % (slug, h1))

        # --- JSON-LD parses
        for jm in re.finditer(r'ld\+json[^>]*>(.*?)</script>', t, re.S):
            try:
                json.loads(jm.group(1))
            except Exception as e:
                add("schema", "%s: bad JSON-LD (%s)" % (slug, str(e)[:60]))

        # --- legacy leftovers (skipped on noindex internal tools)
        if noindex:
            continue
        if "jquery" in t.lower():
            add("legacy", "%s: still references jQuery" % slug)
        if re.search(r'href="css/(bootstrap|style|responsive|color)\.css"', t):
            add("legacy", "%s: still loads old theme CSS" % slug)
        if "font-awesome" in t.lower() or "bootstrap-icons@" in t:
            add("legacy", "%s: still loads icon webfont CDN" % slug)

        # --- inline SVGs need their own size, or they fill the screen until the CSS loads
        for sm in re.finditer(r"<svg\b[^>]*>", t):
            if not re.search(r'\swidth="', sm.group(0)):
                add("html", "%s: <svg> without width/height: %s" % (slug, sm.group(0)[:70]))
                break

        # --- duplicate attributes
        for am in re.finditer(r"<[a-z][^>]*>", t):
            tag = am.group(0)
            for attr in ("style", "class", "id"):
                if len(re.findall(r'\s%s="' % attr, tag)) > 1:
                    add("html", "%s: duplicate %s= in %s" % (slug, attr, tag[:60]))

        # --- local asset references resolve
        for ref in set(re.findall(r'(?:src|href)="((?!https?:|mailto:|tel:|#|data:)[^"]+)"', t)):
            clean = ref.split("#")[0].split("?")[0]
            if not clean or clean.endswith("/"):
                continue
            if not os.path.exists(os.path.join(ROOT, clean)):
                add("broken", "%s -> %s" % (slug, clean))

    # --- sitemap consistency
    sm = io.open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    locs = re.findall(r"<loc>(.*?)</loc>", sm)
    for loc in locs:
        if not loc.startswith(S.SITE):
            add("sitemap", "wrong domain: %s" % loc)
        f = loc[len(S.SITE):].lstrip("/") or "index.html"
        if f in stubs:
            add("sitemap", "lists a redirect stub: %s" % f)
        if not os.path.exists(os.path.join(ROOT, f)):
            add("sitemap", "lists a missing file: %s" % f)
    listed = {(l[len(S.SITE):].lstrip("/") or "index.html") for l in locs}
    for slug in real:
        t = io.open(os.path.join(ROOT, slug), encoding="utf-8").read()
        if 'content="noindex' in t:
            continue
        if slug not in listed:
            add("sitemap", "indexable page not in sitemap: %s" % slug)

    # --- canonical vs sitemap domain
    canon_hosts = set()
    for slug in real:
        t = io.open(os.path.join(ROOT, slug), encoding="utf-8").read()
        m = re.search(r'rel="canonical" href="(https?://[^/"]+)', t)
        if m:
            canon_hosts.add(m.group(1))
    if len(canon_hosts) > 1:
        add("sitemap", "canonicals use multiple hosts: %s" % sorted(canon_hosts))

    check_booking(real)

    # --- report
    print("Validated %d pages (%d content, %d redirect stubs)\n"
          % (len(pages), len(real), len(stubs)))
    if not issues:
        print("  No issues found.")
        return 0

    order = ["broken", "schema", "html", "legacy", "a11y", "head",
             "headings", "sitemap", "booking", "meta-len", "stub"]
    total = 0
    for k in order + [k for k in issues if k not in order]:
        if k not in issues:
            continue
        rows = issues[k]
        total += len(rows)
        print("  %s (%d)" % (k.upper(), len(rows)))
        for r in rows[:14]:
            print("    - %s" % r)
        if len(rows) > 14:
            print("    ... and %d more" % (len(rows) - 14))
        print()
    print("  %d issues total" % total)
    return 1


if __name__ == "__main__":
    sys.exit(main())
