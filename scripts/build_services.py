# -*- coding: utf-8 -*-
"""
Migrate the five service landing pages onto the new shell.

These pages already carry accurate, well-researched copy (thresholds, form
numbers, section references). This preserves that text verbatim and only
replaces the chrome around it.
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nc_shell as S
import nc_content as C

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "backup", "pre-redesign-20260905-134251")

PAGES = [
    ("tax-audit-44ab-bhopal.html", "Tax Audit under Section 44AB",
     "Tax audit u/s 44AB in Bhopal &mdash; turnover threshold review, Form 3CA/3CB and "
     "clause-wise 3CD reporting, filed before the due date."),
    ("gst-notice-consultant-bhopal.html", "GST Notice &amp; Litigation Defence",
     "ASMT-10 scrutiny, DRC-01 show cause, Section 65 audits and first appeals in APL-01, "
     "handled end to end from Bhopal."),
    ("income-tax-notice-consultant-bhopal.html", "Income Tax Notice Defence",
     "Notices under Sections 143(1), 143(2), 148 and 133(6) &mdash; read, answered and "
     "represented through to closure."),
    ("company-registration-bhopal.html", "Company Registration &amp; ROC",
     "Pvt Ltd, LLP, OPC and Section 8 incorporation, plus the annual ROC compliance that "
     "follows it."),
    ("psara-pwd-contractor-registration-madhya-pradesh.html", "PSARA &amp; PWD Contractor Licensing",
     "Madhya Pradesh security agency (PSARA) and PWD contractor registration, Class A to D."),
]


def balanced(html, tag, cls):
    """Inner HTML of <tag class="cls">, counting nested tags of the same name."""
    m = re.search(r'<%s class="%s"[^>]*>' % (tag, cls), html)
    if not m:
        return None
    i, depth = m.end(), 1
    pat = re.compile(r"<(/?)%s\b" % tag, re.I)
    while depth > 0:
        t = pat.search(html, i)
        if not t:
            return None
        depth += -1 if t.group(1) else 1
        i = t.end()
    return html[m.end():html.rfind("<", m.end(), i)]


# Legacy semantic wrappers that have a direct equivalent in the new stylesheet.
CLASS_MAP = {
    "svc-callout": "nc-note",
    "svc-table-wrap": "nc-tw",
    "svc-related": "nc-note",
}


def clean(body):
    body = re.sub(r'<div class="svc-inline-cta">.*?</div>\s*', "", body, flags=re.S)

    def strip_cls(m):
        keep = []
        for c in m.group(1).split():
            if c.startswith("nc-"):
                keep.append(c)
            elif c in CLASS_MAP:
                keep.append(CLASS_MAP[c])
        return ' class="%s"' % " ".join(keep) if keep else ""
    body = re.sub(r'\s+class="([^"]*)"', strip_cls, body)
    body = re.sub(r'\s+style="[^"]*"', "", body)
    body = re.sub(r'\s+(?:width|height|loading|decoding)="[^"]*"', "", body)
    body = re.sub(r"<i\b[^>]*>\s*</i>\s*", "", body)
    body = re.sub(r"<(/?)h5\b", r"<\1h4", body)
    body = re.sub(r"<(/?)h6\b", r"<\1h4", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


def pull_faqs(body):
    """Lift the trailing 'Frequently asked questions' block out of the prose."""
    m = re.search(r"<h2[^>]*>\s*Frequently asked questions\s*</h2>(.*)$", body, re.S | re.I)
    if not m:
        return body, []
    tail = m.group(1)
    pairs = re.findall(r"<h3[^>]*>(.*?)</h3>\s*(.*?)(?=<h3|\Z)", tail, re.S)
    faqs = []
    for q, a in pairs:
        q = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", q)).strip()
        a = re.sub(r"\s+", " ", a).strip()
        if q and a:
            faqs.append((q, a))
    return body[:m.start()].rstrip(), faqs


def build(slug, short, blurb):
    src = os.path.join(SRC, slug)
    html = io.open(src, encoding="utf-8").read()

    art = balanced(html, "article", "svc-body")
    if art is None:
        return "no svc-body"

    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    h1 = re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else short

    desc = re.search(r'<meta name="description" content="([^"]*)"', html)
    desc = desc.group(1).strip() if desc else blurb

    body_prose, faqs = pull_faqs(clean(art))

    faq_html = ""
    if faqs:
        items = "".join(
            '<details><summary>%s</summary><div class="nc-faq-a">%s</div></details>' % (q, a)
            for q, a in faqs)
        faq_html = """
<section class="nc-sec nc-sec-alt">
  <div class="nc-wrap nc-wrap-nar">
    %s
    <div class="nc-faq" data-nc-rise>%s</div>
  </div>
</section>""" % (S.sec_head("Questions", "Frequently asked"), items)

    # Sidebar: the other four services + contact
    others = "".join(
        '<a href="%s">%s</a>' % (s, t)
        for s, t, _ in PAGES if s != slug)

    body = """{phero}

<section class="nc-sec">
  <div class="nc-wrap">
    <div class="nc-article">

      <article>
        <div class="nc-prose">
{prose}
        </div>
      </article>

      <aside class="nc-aside">
        <div class="nc-card">
          <h2 class="nc-h4" style="font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:var(--nc-acc-dk);font-family:var(--nc-body)">On this page</h2>
          <nav class="nc-toc"></nav>
        </div>

        <div class="nc-card">
          <h2 class="nc-h4" style="font-size:1.05rem">Speak to CA Natasha</h2>
          <p style="font-size:.92rem;color:var(--nc-ink-3)">
            Send the document, get a written position and a fixed fee before any work starts.
          </p>
          <div class="nc-stack" style="gap:.6rem;margin-top:1.15rem">
            <a class="nc-btn nc-btn-full nc-btn-sm" href="{book}">Book a consultation</a>
            <a class="nc-btn nc-btn-ghost nc-btn-full nc-btn-sm" href="tel:{phone}">{phone_d}</a>
          </div>
        </div>

        <div class="nc-card">
          <h2 class="nc-h4" style="font-size:1.05rem">Other practice areas</h2>
          <div class="nc-ftr-links" style="margin-top:.85rem">
            {others}
            <a href="services.html">All 11 services</a>
          </div>
        </div>
      </aside>

    </div>
  </div>
</section>
{faq}

{cta}""".format(
        phero=S.phero(h1, blurb,
                      [("Home", "index.html"), ("Services", "services.html"), (short, None)]),
        prose=body_prose, faq=faq_html, cta=S.cta_band(),
        phone=S.PHONE, phone_d=S.PHONE_DISPLAY, others=others, book=S.BOOK_URL)

    svc_ld = """{
  "@context": "https://schema.org",
  "@type": "Service",
  "@id": "%(site)s/%(slug)s#service",
  "name": "%(name)s",
  "description": "%(desc)s",
  "url": "%(site)s/%(slug)s",
  "serviceType": "%(name)s",
  "provider": {"@id": "%(org)s"},
  "areaServed": [
    {"@type": "City", "name": "Bhopal"},
    {"@type": "State", "name": "Madhya Pradesh"},
    {"@type": "Country", "name": "India"}
  ],
  "audience": {"@type": "BusinessAudience", "audienceType": "Businesses, professionals and individual taxpayers"},
  "availableChannel": {
    "@type": "ServiceChannel",
    "servicePhone": {"@type": "ContactPoint", "telephone": "%(phone)s", "contactType": "customer service"},
    "serviceUrl": "%(site)s/contact-us.html"
  }
}""" % dict(site=S.SITE, slug=slug, name=h1.replace('"', "'"),
            desc=desc.replace('"', "'")[:280], org=S.ORG_ID, phone=S.PHONE)

    blocks = [svc_ld, S.org_schema(),
              S.crumbs_schema([("Home", "index.html"), ("Services", "services.html"), (h1, slug)])]
    if faqs:
        blocks.append(S.faq_schema(faqs))

    doc = S.page(
        title=S.seo_title(h1),
        desc=desc, slug=slug, body=body, schema=S.ld(*blocks),
        keywords="%s, CA Bhopal, Chartered Accountant Bhopal, %s Bhopal, CA Natasha Rajvaidya"
                 % (h1, short.replace("&amp;", "and")))

    with io.open(os.path.join(ROOT, slug), "w", encoding="utf-8") as f:
        f.write(doc)
    return None


def main():
    for slug, short, blurb in PAGES:
        err = build(slug, short, blurb)
        if err:
            print("  SKIP  %-56s %s" % (slug, err))
        else:
            size = os.path.getsize(os.path.join(ROOT, slug)) // 1024
            print("  built %-56s %3d KB" % (slug, size))


if __name__ == "__main__":
    main()
