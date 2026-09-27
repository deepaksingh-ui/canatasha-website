# -*- coding: utf-8 -*-
"""Site content: practice areas, FAQs, and a scanner that indexes the articles."""
import datetime
import glob
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ------------------------------------------------------------------ services
# (number, title, blurb, icon key, link, photo)
PRACTICES = [
    ("01", "Accounting &amp; Bookkeeping",
     "Accounts preparation, bank reconciliation, AP/AR management and cash-flow modelling under Indian GAAP.",
     "file", "services.html#accounting", "images/finance-1-768x512.jpg"),
    ("02", "Taxation Services",
     "ITR preparation for salaried individuals and corporates, tax optimisation, TAN registration and TDS compliance.",
     "chart", "services.html#taxation", "images/legacy-ts.jpg"),
    ("03", "Audit &amp; Assurance",
     "Tax Audit under Section 44AB, statutory audit under the Companies Act, GST audit and stock verification.",
     "shield", "tax-audit-44ab-bhopal.html", "images/133-768x512.jpg"),
    ("04", "Business Advisory",
     "Business valuation, forecasting, budget planning, debt syndication and financial restructuring.",
     "trend", "services.html#advisory", "images/legacy-ba.jpg"),
    ("05", "Financial Planning &amp; FP&amp;A",
     "Retirement planning, family trust structuring, investment advisory and startup financial modelling.",
     "calc", "services.html#planning", "images/legacy-fp.jpg"),
    ("06", "Formation &amp; Compliance",
     "Corporate governance, secretarial audit, ROC Form AOC-4 and MGT-7, and director KYC compliance.",
     "building", "company-registration-bhopal.html", "images/socities-law-768x504.jpg"),
    ("07", "Company Registration",
     "Incorporation of Pvt Ltd, LLP, OPC, Section 8 NGO, Producer Company and Startup India recognition.",
     "briefcase", "company-registration-bhopal.html", "images/BPO-768x512.jpg"),
    ("08", "Appeals &amp; Notice Defence",
     "Income tax notice and Section 148 response, GST show cause under Section 73/74, and Section 128A amnesty.",
     "scale", "gst-notice-consultant-bhopal.html", "images/279-768x513.jpg"),
    ("09", "Specialised &amp; NRI Practice",
     "NRI property sale Section 195 TDS exemption certificates, Form 15CA/CB remittances and annual IEC updates.",
     "globe", "services.html#nri", "images/1427-768x512.jpg"),
    ("10", "Technology &amp; Virtual CFO",
     "Cloud accounting deployment (Zoho, Tally Prime), automated MIS dashboards and Virtual CFO leadership.",
     "users", "services.html#vcfo", "images/2052-768x512.jpg"),
    ("11", "Licensing &amp; Registrations",
     "EPFO, ESIC, MP PWD Contractor Registration (Class A to D), PSARA security agency licence and FSSAI.",
     "award", "psara-pwd-contractor-registration-madhya-pradesh.html", "images/background-6.jpg"),
]

# Three headline services for the home page
HEADLINE = [
    ("shield", "Audit &amp; Assurance",
     "Statutory audits, Tax Audit u/s 44AB, GST audits, stock audits and forensic due diligence, executed strictly to ICAI benchmarks.",
     "tax-audit-44ab-bhopal.html", "Tax audit &amp; assurance"),
    ("scale", "Taxation &amp; Appeals",
     "Strategic ITR planning, corporate taxation, TDS compliance, and representation against income tax and GST scrutiny notices.",
     "gst-notice-consultant-bhopal.html", "Notice &amp; litigation defence"),
    ("building", "Corporate Advisory",
     "Pvt Ltd, LLP and OPC incorporation, Startup India DPIIT recognition, ROC compliance and Virtual CFO leadership.",
     "company-registration-bhopal.html", "Company formation &amp; ROC"),
]

# (value, suffix, label, plain) — `plain` suppresses digit grouping
STATS = [
    ("194", "+", "Google reviews, 4.8★", False),
    ("1000", "+", "Clients served", False),
    ("11", "", "Practice areas", False),
    ("2017", "", "Practising since", True),
]

PROCESS = [
    ("Understand", "You send us the notice, the books, or the question. We read everything before we quote, so the scope is real and the fee does not move later."),
    ("Assess", "You get a written position: what the law says, what your exposure is, what the realistic outcomes are, and what each one costs."),
    ("Execute", "We file, represent, and follow through &mdash; hearings, submissions, appeals. One partner owns your file from start to finish."),
    ("Close out", "Compliance calendar handed over, documents archived, and a plan so the same issue does not come back next year."),
]

WHY = [
    "ISO 9001:2015 certified quality management &mdash; documented process, not ad-hoc work",
    "Direct partner access &mdash; you speak to a Chartered Accountant, not a junior",
    "Fixed written scope and fee before work starts, no surprise invoices",
    "Full representation before assessing officers, appellate authorities and GST officers",
    "Cloud accounting on Tally Prime and Zoho, with monthly MIS you can actually read",
    "Bilingual practice &mdash; English and Hindi, across Madhya Pradesh and for NRI clients",
]

HOME_FAQ = [
    ("Who is the best CA in Bhopal for GST notices and tax scrutiny?",
     "Natasha &amp; Company, at 195-A Zone-1 M.P. Nagar, is an ISO 9001:2015 certified firm founded by CA Natasha Rajvaidya (FCA), rated 4.8 across 194+ Google reviews. The firm handles GST show-cause notices under Sections 73 and 74, ASMT-10 scrutiny, DRC-01 demands, and income tax notices under Sections 143(1), 143(2) and 148 &mdash; including full representation at hearings and first appeal."),
    ("How much does a Chartered Accountant in Bhopal charge?",
     "Fees depend on scope, not on a rate card. ITR filing for a salaried individual starts lower than a corporate tax audit under Section 44AB, which in turn is lower than defending a multi-year GST demand. We read your papers first and give a written, fixed fee before starting, so the number does not move mid-engagement."),
    ("What should I do first after receiving a GST or income tax notice?",
     "Do not reply on your own and do not ignore it. Note the section, the assessment year and the response deadline &mdash; most notices carry 15 to 30 days. Send us a scan on WhatsApp at +91 94070 00157. A wrong or late reply narrows your options at the appeal stage far more than the original issue does."),
    ("Do you work with clients outside Bhopal, including NRIs?",
     "Yes. Filings, notices and ROC compliance are handled digitally for clients across Madhya Pradesh and India. NRI work is a distinct practice: Section 195 TDS exemption certificates on property sale, Form 15CA and 15CB remittance certification, DTAA positions and residential status determination."),
    ("Is Tax Audit under Section 44AB mandatory for my business?",
     "It applies once turnover crosses the prescribed threshold &mdash; and the threshold itself changes with the proportion of your receipts and payments made digitally, and with whether you have opted out of the presumptive scheme under Section 44AD. Send us your turnover and payment-mode split and we will confirm your position in writing."),
    ("What makes Natasha &amp; Company different from other CA firms?",
     "Three things: ISO 9001:2015 certified process so the work is documented rather than improvised; direct partner access so you are not routed through juniors; and a written scope and fee agreed before work begins."),
]

# ------------------------------------------------------------------ articles
_MONTHS = {}


def articles():
    """Index every rebuilt article page. Newest first."""
    from build_articles import HAND
    out = []
    for path in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
        slug = os.path.basename(path)
        if slug in HAND:
            continue
        t = io.open(path, encoding="utf-8").read()
        if "nc-prose" not in t:      # redirect stub
            continue
        d = {}
        for m in re.finditer(r'<script[^>]*ld\+json[^>]*>(.*?)</script>', t, re.S):
            try:
                j = json.loads(m.group(1))
            except Exception:
                continue
            if isinstance(j, dict) and j.get("@type") == "BlogPosting":
                d = j
                break
        if not d:
            continue

        img = d.get("image", "")
        img = img.replace("https://canatasha.com/", "")

        out.append({
            "slug": slug,
            "title": d.get("headline", ""),
            "desc": d.get("description", ""),
            "cat": d.get("articleSection", "Insights"),
            "date": d.get("datePublished", ""),
            "img": img,
            "mins": int(re.sub(r"\D", "", d.get("timeRequired", "PT5M")) or 5),
        })

    out.sort(key=lambda a: a["date"], reverse=True)
    return out


def nice_date(iso):
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", iso or ""):
        return iso or ""
    y, m, d = (int(x) for x in iso.split("-"))
    return datetime.date(y, m, d).strftime("%d %b %Y")


def post_card(a, rise=True):
    """One article card."""
    img = a["img"] or "images/blog-1.jpg"
    r = ' data-nc-rise="scale"' if rise else ""
    return """<article class="nc-card nc-card-i nc-post"{r}>
  <a class="nc-post-img" href="{slug}" tabindex="-1" aria-hidden="true">
    <img src="{img}" alt="" loading="lazy" decoding="async" width="640" height="400">
  </a>
  <div class="nc-post-body">
    <div class="nc-post-meta">
      <span class="nc-tag">{cat}</span>
      <time datetime="{date}">{nice}</time>
      <span>{mins} min</span>
    </div>
    <h3><a href="{slug}">{title}</a></h3>
    <p>{desc}</p>
    <a class="nc-alink" href="{slug}">Read the guide <span class="nc-ar">&rarr;</span></a>
  </div>
</article>""".format(r=r, slug=a["slug"], img=img, cat=a["cat"], date=a["date"],
                     nice=nice_date(a["date"]), mins=a["mins"],
                     title=a["title"], desc=a["desc"][:155].rstrip() + "&hellip;")


def practice_card(num, title, blurb, icon, href, photo, rise=True):
    """Photo card: image, solid title bar, body. Used on home and services."""
    r = ' data-nc-rise' if rise else ''
    return """<article class="nc-pcard"%s>
  <a class="nc-pcard-img" href="%s" tabindex="-1" aria-hidden="true" data-hover="View this practice">
    <span class="nc-pcard-no">%s</span>
    <img src="%s" alt="" loading="lazy" decoding="async" width="768" height="512">
  </a>
  <a class="nc-pcard-bar" href="%s">%s</a>
  <div class="nc-pcard-body">
    <p>%s</p>
    <a class="nc-alink" href="%s">Learn more <span class="nc-ar">&rarr;</span></a>
  </div>
</article>""" % (r, href, num, photo, href, title, blurb, href)
