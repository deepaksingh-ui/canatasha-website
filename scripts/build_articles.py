# -*- coding: utf-8 -*-
"""
Migrate the blog/article pages onto the new shell.

Reads each legacy article, lifts out the parts worth keeping (headline, dates,
category, hero image, body prose, existing BlogPosting data), drops the old
Bootstrap chrome, and re-emits the page against nc_shell.
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nc_shell as S

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Always parse the pre-redesign originals, never the generated output, so the
# build stays idempotent and can be re-run after any shell change.
SRC = os.path.join(ROOT, "backup", "pre-redesign-20260905-134251")

# Pages built by hand elsewhere — never touched by this script.
HAND = {
    "index.html", "about-us.html", "services.html", "contact-us.html",
    "blog.html", "career.html", "knowledge-base.html", "404.html",
    "tax-audit-44ab-bhopal.html", "gst-notice-consultant-bhopal.html",
    "income-tax-notice-consultant-bhopal.html", "company-registration-bhopal.html",
    "psara-pwd-contractor-registration-madhya-pradesh.html",
    "income-tax-calculator.html", "hra-exemption-calculator.html",
    "gst-calculator.html", "emi-loan-calculator.html",
    "privacy-policy.html", "terms-and-conditions.html",
    "privacy.html", "terms.html", "admin-news-editor.html",
    # service sub-pages, authored in build_subservices.py
    "accounting-bookkeeping-services-bhopal.html",
    "income-tax-return-filing-bhopal.html",
    "virtual-cfo-services-bhopal.html",
    "nri-taxation-services-bhopal.html",
    "business-advisory-valuation-bhopal.html",
    "financial-planning-fpa-bhopal.html",
}


# Short <title> tags for articles whose headline runs past what a SERP shows.
# The full headline stays as the on-page <h1>; only the title tag is trimmed,
# with the primary keyword moved to the front.
TITLE_OVERRIDES = {
    "7-key-points-every-salaried-employee-must-know-before-filing-income-tax-return-for-fy-2024-25.html":
        "ITR Filing FY 2024-25: 7 Key Points for Salaried Employees",
    "dont-get-caught-off-guard-high-value-cash-transactions-tax-notices-in-india.html":
        "High-Value Cash Transactions & Income Tax Notices in India",
    "exploring-the-option-for-nris-to-opt-for-the-new-tax-regime-in-fy-2023-24-in-india.html":
        "Can NRIs Opt for the New Tax Regime? FY 2023-24 Guide",
    "itr-filing-deadline-extended-to-september-15-2025-more-time-for-accurate-returns.html":
        "ITR Filing Deadline Extended to 15 September 2025",
    "madhya-pradesh-26-61-lakh-crore-investment-inflow-gis-2025.html":
        "MP Draws Rs 26.61 Lakh Crore Investment at GIS 2025",
    "madhya-pradesh-global-investors-summit-2025-paving-the-way-for-a-viksit-bharat.html":
        "MP Global Investors Summit 2025: Road to Viksit Bharat",
    "major-tax-relief-alert-understand-the-new-section-128a-amnesty-scheme-in-budget-2024.html":
        "Section 128A GST Amnesty Scheme Explained (Budget 2024)",
    "maximizing-tax-benefits-understanding-section-24-deductions-from-house-property-income.html":
        "Section 24 Deductions on House Property Income",
    "overview-of-the-54th-gst-council-meeting-key-decisions-their-implications.html":
        "54th GST Council Meeting: Key Decisions Explained",
    "understanding-the-rules-and-benefits-of-carrying-forward-losses-in-income-tax-returns.html":
        "Carry Forward of Losses in ITR: Rules & Benefits",
    "unveiling-transparency-supreme-courts-directive-on-disclosure-of-electoral-bond-details.html":
        "Supreme Court Directive on Electoral Bond Disclosure",
    "why-your-gold-silver-just-got-more-precious-a-laymans-guide-by-ca-natasha-rajvaidya.html":
        "Why Gold & Silver Prices Are Rising: 6 Key Reasons",
}


def redirected():
    """Slugs that vercel.json 301s away — these become stubs, not articles."""
    cfg = json.load(io.open(os.path.join(ROOT, "vercel.json"), encoding="utf-8"))
    return {r["source"].lstrip("/") for r in cfg.get("redirects", [])}


REDIRECTED = redirected()


# --------------------------------------------------------------- extraction
def balanced(html, start_pat):
    """Inner HTML of the first tag matching start_pat, counting nested divs."""
    m = re.search(start_pat, html)
    if not m:
        return None
    i = m.end()
    depth = 1
    tag = re.compile(r"<(/?)div\b", re.I)
    while depth > 0:
        t = tag.search(html, i)
        if not t:
            return None
        depth += -1 if t.group(1) else 1
        i = t.end()
    return html[m.end():html.rfind("<", m.end(), i)]


def grab(pat, html, group=1, default=""):
    m = re.search(pat, html, re.I | re.S)
    return m.group(group).strip() if m else default


def old_ld(html):
    """First BlogPosting/Article JSON-LD block, as a dict."""
    for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.S | re.I):
        try:
            d = json.loads(m.group(1))
        except Exception:
            continue
        if isinstance(d, dict) and d.get("@type") in ("BlogPosting", "Article", "NewsArticle"):
            return d
    return {}


def clean(body):
    """Strip legacy Bootstrap classes and inline styles from migrated prose."""
    # Drop the old in-article CTA boxes; the new shell supplies its own.
    body = re.sub(r'<div class="svc-inline-cta">.*?</div>\s*', "", body, flags=re.S)

    # Bootstrap utility classes carry no meaning under the new stylesheet.
    def strip_cls(m):
        keep = [c for c in m.group(1).split()
                if c.startswith("nc-") or c in ("nc-note", "nc-table")]
        return ' class="%s"' % " ".join(keep) if keep else ""
    body = re.sub(r'\s+class="([^"]*)"', strip_cls, body)
    body = re.sub(r'\s+style="[^"]*"', "", body)
    body = re.sub(r'\s+(?:width|height|loading|decoding)="[^"]*"', "", body)

    # <i class="bi ..."> glyphs lose their font; remove the empty shells.
    body = re.sub(r"<i\b[^>]*>\s*</i>\s*", "", body)

    # Trailing hashtag blobs (#AdvanceTax #ITRFiling ...) are a social-media
    # habit that reads as keyword stuffing on a web page. Drop the paragraph
    # when it is nothing but hashtags.
    body = re.sub(r"<p>\s*(?:#[\w-]+[\s,]*){3,}</p>\s*", "", body)

    # Legacy headings inside articles came in as h1/h4; normalise the hierarchy.
    body = re.sub(r"<(/?)h1\b", r"<\1h2", body)
    body = re.sub(r"<(/?)h5\b", r"<\1h4", body)
    body = re.sub(r"<(/?)h6\b", r"<\1h4", body)
    body = S.close_heading_gaps(body)

    # Absolute links back to our own site (apex or www) become relative, so
    # they never pass through the apex -> www redirect.
    body = re.sub(r'href="https?://(?:www\.)?canatasha\.com/?([^"]*)"',
                  lambda m: 'href="%s"' % (m.group(1) or "index.html"), body)

    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


def read_time(body):
    words = len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", body)))
    return max(2, round(words / 210))


# --------------------------------------------------------------- build
def build(slug):
    with io.open(os.path.join(SRC, slug), encoding="utf-8", errors="replace") as f:
        html = f.read()

    art = balanced(html, r'<div class="article-content-body">')
    if art is None:
        art = balanced(html, r'<article class="single-blog-article">')
    if art is None:
        return None, "no article body"

    d = old_ld(html)
    title = (d.get("headline")
             or grab(r"<h1[^>]*>(.*?)</h1>", html)
             or grab(r"<title>(.*?)(?:\s*\|.*?)?</title>", html))
    title = re.sub(r"<[^>]+>", "", title).strip()

    desc = d.get("description") or grab(r'<meta name="description" content="([^"]*)"', html)
    desc = desc.strip()[:300]

    category = d.get("articleSection") or grab(
        r'<span class="badge[^"]*"[^>]*>(.*?)</span>', html) or "Insights"
    category = re.sub(r"<[^>]+>", "", category).strip()

    published = d.get("datePublished", "")
    modified = d.get("dateModified", published)

    hero = grab(r'(<picture>.*?</picture>)', html)
    if not hero:
        src = grab(r'<img[^>]+src="(images/[^"]+)"[^>]*class="img-fluid', html)
        hero = '<img src="%s" alt="%s">' % (src, title) if src else ""
    if hero:
        hero = re.sub(r'\s+(?:class|style)="[^"]*"', "", hero)

    img = d.get("image") or grab(r'<img[^>]+src="(images/[^"]+)"', hero or html)
    if img:
        img = re.sub(r"^https?://(?:www\.)?canatasha\.com", S.SITE, img)
        if not img.startswith("http"):
            img = S.SITE + "/" + img.lstrip("/")

    body = clean(art)
    mins = read_time(body)

    # Clean up truncated descriptions ending in "..."
    if desc.endswith("...") or desc.endswith("…") or desc.endswith(".."):
        clean_prefix = re.sub(r'[\.\s…]+$', '', desc)
        plain = re.sub(r"<[^>]+>", " ", body)
        plain = re.sub(r"\s+", " ", plain).strip()
        search_words = clean_prefix.split()
        completed = False
        while len(search_words) >= 4:
            sub = " ".join(search_words)
            pos = plain.find(sub)
            if pos != -1:
                rem = plain[pos:]
                m = re.search(r'^(.*?[.!?])(?:\s+[A-Z]|\s*$)', rem)
                if m:
                    cand = m.group(1).strip()
                    if 70 <= len(cand) <= 300:
                        desc = cand
                        completed = True
                        break
                p_idx = rem.find(". ")
                if p_idx != -1:
                    cand = rem[:p_idx + 1].strip()
                    if 70 <= len(cand) <= 300:
                        desc = cand
                        completed = True
                        break
                break
            search_words.pop()
        if not completed:
            m = re.search(r'^(.*[.!?])\s+[^.!?]*$', clean_prefix)
            if m and len(m.group(1).strip()) >= 70:
                desc = m.group(1).strip()
            else:
                sents = re.findall(r'([^.!?]+[.!?])', plain)
                acc = ""
                for s in sents:
                    s = s.strip()
                    if len(acc) + len(s) + 1 <= 280:
                        acc = (acc + " " + s).strip()
                        if len(acc) >= 70:
                            desc = acc
                            break
                    else:
                        break
                if not (70 <= len(desc) <= 300 and not desc.endswith("...") and not desc.endswith("…")):
                    desc = clean_prefix.rstrip() + "."

    # ---- date label
    label = published
    if re.match(r"^\d{4}-\d{2}-\d{2}$", published or ""):
        import datetime
        dt = datetime.date(*[int(x) for x in published.split("-")])
        label = dt.strftime("%d %B %Y")

    meta_bits = ['<span class="nc-tag">%s</span>' % category]
    if label:
        meta_bits.append('<time datetime="%s">%s</time>' % (published, label))
    meta_bits.append("%d min read" % mins)
    meta_bits.append(S.FOUNDER)

    hero_block = ('<figure class="nc-media" style="margin:0 0 2.5rem" data-nc-rise>%s</figure>'
                  % hero) if hero else ""

    # ---- schema
    esc = lambda s: s.replace("\\", "\\\\").replace('"', '\\"')
    art_ld = """{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "@id": "%(site)s/%(slug)s#article",
  "mainEntityOfPage": {"@type": "WebPage", "@id": "%(site)s/%(slug)s"},
  "headline": "%(title)s",
  "description": "%(desc)s",
  "image": "%(img)s",
  "articleSection": "%(cat)s",
  "datePublished": "%(pub)s",
  "dateModified": "%(mod)s",
  "wordCount": %(wc)d,
  "timeRequired": "PT%(mins)dM",
  "inLanguage": "en-IN",
  "isAccessibleForFree": true,
  "author": {
    "@type": "Person",
    "name": "%(founder)s",
    "jobTitle": "Chartered Accountant (FCA)",
    "url": "%(site)s/about-us.html#founder",
    "worksFor": {"@id": "%(org)s"}
  },
  "publisher": {"@id": "%(org)s"},
  "about": {"@type": "Thing", "name": "%(cat)s"}
}""" % dict(site=S.SITE, slug=slug, title=esc(title), desc=esc(desc),
            img=img if img.startswith("http") else S.SITE + "/" + img.lstrip("/"),
            cat=esc(category), pub=published or "2024-01-01",
            mod=modified or published or "2024-01-01",
            wc=len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", body))),
            mins=mins, founder=S.FOUNDER, org=S.ORG_ID)

    crumb_ld = S.crumbs_schema([
        ("Home", "index.html"), ("Insights", "blog.html"), (title, slug)])

    share = ("https://api.whatsapp.com/send?text="
             + re.sub(r"[^A-Za-z0-9]", "%20", title)[:160] + "%20"
             + S.SITE.replace(":", "%3A").replace("/", "%2F") + "%2F" + slug)

    body_html = """<div class="nc-progress"></div>

<section class="nc-phero">
  <div class="nc-wrap nc-wrap-nar">
    {crumb}
    <h1 data-nc-rise>{title}</h1>
    <div class="nc-post-meta" style="margin-top:1.25rem;--d:90ms" data-nc-rise>{meta}</div>
  </div>
</section>

<section class="nc-sec">
  <div class="nc-wrap">
    <div class="nc-article">

      <article>
        {hero}
        <div class="nc-prose">
{body}
        </div>

        <div class="nc-note nc-mt3">
          <b>Written by {founder}</b>
          <p>
            Founder and Managing Partner at {name}, an ISO 9001:2015 certified
            Chartered Accountancy firm in Zone-1, M.P. Nagar, Bhopal. This article is
            general guidance, not advice on your specific facts &mdash;
            <a href="contact-us.html">talk to us</a> before you act on it.
          </p>
        </div>

        <div class="nc-row" style="justify-content:space-between;margin-top:2rem">
          <a class="nc-alink" href="blog.html"><span class="nc-ar">&larr;</span> All insights</a>
          <a class="nc-btn nc-btn-ghost nc-btn-sm" href="{share}" target="_blank" rel="noopener">Share on WhatsApp</a>
        </div>
      </article>

      <aside class="nc-aside">
        <div class="nc-card">
          <h2 class="nc-h4" style="font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:var(--nc-acc-dk);font-family:var(--nc-body)">On this page</h2>
          <nav class="nc-toc"></nav>
        </div>

        <div class="nc-card">
          <h2 class="nc-h4" style="font-size:1.05rem">Facing a notice or deadline?</h2>
          <p style="font-size:.92rem;color:var(--nc-ink-3)">
            We read the notice, tell you what it actually means, and represent you
            through to closure.
          </p>
          <div class="nc-stack" style="gap:.6rem;margin-top:1.15rem">
            <a class="nc-btn nc-btn-full nc-btn-sm" href="{book}">Book a consultation</a>
            <a class="nc-btn nc-btn-ghost nc-btn-full nc-btn-sm" href="tel:{phone}">{phone_d}</a>
          </div>
        </div>

        <div class="nc-card">
          <h2 class="nc-h4" style="font-size:1.05rem">Free calculators</h2>
          <div class="nc-ftr-links" style="margin-top:.85rem">
            <a href="income-tax-calculator.html">Income Tax Calculator</a>
            <a href="hra-exemption-calculator.html">HRA Exemption Calculator</a>
            <a href="gst-calculator.html">GST Calculator</a>
            <a href="emi-loan-calculator.html">EMI Loan Calculator</a>
          </div>
        </div>
      </aside>

    </div>
  </div>
</section>

{cta}""".format(crumb=S.crumb([("Home", "index.html"), ("Insights", "blog.html"), (title, None)]),
                title=title, meta="".join(meta_bits), hero=hero_block, body=body,
                founder=S.FOUNDER, name=S.NAME, share=share,
                phone=S.PHONE, phone_d=S.PHONE_DISPLAY, book=S.BOOK_URL,
                cta=S.cta_band())

    doc = S.page(
        title=S.seo_title(TITLE_OVERRIDES.get(slug, title)),
        desc=desc,
        slug=slug,
        body=body_html,
        og_type="article",
        image=img,
        published=published,
        modified=modified,
        section=category,
        schema=S.ld(art_ld, crumb_ld, S.org_schema()),
        keywords="%s, CA Bhopal, %s, Chartered Accountant Bhopal, CA Natasha Rajvaidya"
                 % (title[:70], category),
    )
    return doc, None


def main():
    files = sorted(f for f in os.listdir(SRC)
                   if f.endswith(".html") and f not in HAND
                   and f not in REDIRECTED)
    ok, skip = [], []
    for f in files:
        doc, err = build(f)
        if err:
            skip.append((f, err))
            continue
        with io.open(os.path.join(ROOT, f), "w", encoding="utf-8") as out:
            out.write(doc)
        ok.append(f)

    print("rebuilt %d article pages" % len(ok))
    for f, e in skip:
        print("  SKIPPED %-70s %s" % (f, e))


if __name__ == "__main__":
    main()
