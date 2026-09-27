# -*- coding: utf-8 -*-
"""
Shared page shell for canatasha.com.

One source of truth for <head>, header, footer and structured data so all 64
pages stay identical where they should be. Import from the build scripts.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _knowledge_bank as KB

SITE = "https://www.canatasha.com"  # the host Google already indexes; the apex 301s here
NAME = "Natasha &amp; Company"
NAME_PLAIN = "Natasha & Company"
PHONE = "+919407000157"
PHONE_DISPLAY = "+91 94070 00157"
EMAIL = "info@canatasha.com"
STREET = "195-A, 2nd Floor, Zone-1, M.P. Nagar"
CITY = "Bhopal"
REGION = "Madhya Pradesh"
POSTAL = "462011"
LAT = "23.2332"
LON = "77.4342"
FOUNDER = "CA Natasha Rajvaidya"

# Straight off the firm's own Google Business Profile (checked 2026-09-20).
# Schema.org ratings must match what the listing and the page actually show.
RATING = "4.8"
REVIEW_COUNT = "194"
REVIEWS_URL = ("https://www.google.com/maps/search/?api=1&query="
               "NATASHA+%26+Co.+CA+in+Bhopal%2C+195-A%2C+Zone-1%2C+M.P.+Nagar%2C+Bhopal+462011")
OG_IMAGE = SITE + "/images/brand/og-card.jpg"   # 1200x630, built by build_brand.py
LOGO_512 = SITE + "/images/brand/icon-512.png"

# Calendly booking. Paste the firm's event link between the quotes, e.g.
# "https://calendly.com/<account>/<event>". Left blank there is no booking page
# and every "Book a consultation" button keeps going to contact-us.html.
# NC_CALENDLY_URL overrides it for a one-off build (previews, tests).
CALENDLY_URL = os.environ.get("NC_CALENDLY_URL", "https://calendly.com/natasharaj23/30min").strip()
BOOK_URL = "book-consultation.html" if CALENDLY_URL else "contact-us.html"

# Verified profiles — these feed schema.org sameAs, which is how search engines
# and AI systems tie the site to a single real-world entity.
PROFILES = [
    ("li", "LinkedIn", "https://www.linkedin.com/in/ca-natasha-rajvaidya-5710b953/"),
    ("fb", "Facebook", "https://www.facebook.com/canatasharaj/"),
    ("insta", "Instagram", "https://www.instagram.com/natasharajvaidya/"),
    ("wa", "WhatsApp", "https://wa.me/919407000157"),
]
SAME_AS = [
    "https://www.linkedin.com/in/ca-natasha-rajvaidya-5710b953/",
    "https://www.facebook.com/canatasharaj/",
    "https://www.instagram.com/natasharajvaidya/",
    "https://twitter.com/canatasharaj",
]

# ---------------------------------------------------------------- icons
# Inline SVG only — this replaces FontAwesome + Bootstrap Icons + Flaticon
# (roughly 180KB of webfont) with a few hundred bytes per glyph.
I = {
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/>',
    "chart": '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><line x1="9" y1="7" x2="9" y2="7"/><line x1="15" y1="7" x2="15" y2="7"/><line x1="9" y1="12" x2="9" y2="12"/><line x1="15" y1="12" x2="15" y2="12"/><path d="M10 22v-4h4v4"/>',
    "scale": '<path d="M12 3v18"/><path d="M5 7h14"/><path d="m5 7-3 7h6z"/><path d="m19 7-3 7h6z"/><path d="M8 21h8"/>',
    "calc": '<rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="11" x2="8" y2="11"/><line x1="12" y1="11" x2="12" y2="11"/><line x1="16" y1="11" x2="16" y2="11"/><line x1="8" y1="15" x2="8" y2="15"/><line x1="12" y1="15" x2="12" y2="15"/><line x1="16" y1="15" x2="16" y2="18"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "trend": '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>',
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    "award": '<circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/>',
    "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "search": '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    "up": '<line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/>',
    "arrow": '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
    "check": '<polyline points="20 6 9 17 4 12"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
}

_SOLID = {"caret", "wa", "li", "fb", "yt", "insta"}


# Every inline SVG carries its own size. An <svg> with only a viewBox renders
# as wide as its container until nc.css arrives, and on a slow phone that first
# paint showed the topbar phone and mail icons filling the whole screen. The
# attributes are presentation hints, so any size set in nc.css still wins.
SVG_DIM = ' width="1em" height="1em"'


def ico(name, cls="", size=None):
    """Inline SVG by key. Stroke icons unless listed in _SOLID."""
    if name == "caret":
        return ('<svg class="nc-caret"%s viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                '<polyline points="6 9 12 15 18 9"/></svg>' % SVG_DIM)
    body = I.get(name, I["check"])
    dim = ' width="%s" height="%s"' % (size, size) if size else SVG_DIM
    c = ' class="%s"' % cls if cls else ""
    return ('<svg%s%s viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
            % (c, dim, body))


SOCIAL_SVG = {
    "wa": '<path d="M17.47 14.38c-.3-.15-1.75-.86-2.02-.96-.27-.1-.47-.15-.67.15-.2.3-.77.96-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.25-.46-2.38-1.47-.88-.78-1.47-1.75-1.65-2.05-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.6-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.01-1.04 2.47s1.06 2.86 1.21 3.06c.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.69.63.71.22 1.36.19 1.87.12.57-.09 1.75-.72 2-1.41.25-.69.25-1.28.17-1.41-.07-.13-.27-.2-.57-.35zM12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.87 9.87 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2z"/>',
    "li": '<path d="M4.98 3.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM3 9h4v12H3zM9 9h3.8v1.65h.05c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.78 2.65 4.78 6.1V21h-4v-5.5c0-1.31-.02-3-1.83-3-1.83 0-2.11 1.43-2.11 2.9V21H9z"/>',
    "fb": '<path d="M22 12a10 10 0 1 0-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.5 1.49-3.89 3.77-3.89 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.45 2.89h-2.33v6.99A10 10 0 0 0 22 12z"/>',
    "insta": '<path d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41-.56-.22-.96-.48-1.38-.9-.42-.42-.68-.82-.9-1.38-.16-.42-.36-1.06-.41-2.23-.06-1.27-.07-1.65-.07-4.85s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41 1.27-.06 1.65-.07 4.85-.07zM12 7.85a4.15 4.15 0 1 0 0 8.3 4.15 4.15 0 0 0 0-8.3zm0 6.85a2.7 2.7 0 1 1 0-5.4 2.7 2.7 0 0 1 0 5.4zm5.28-7.01a.97.97 0 1 1-1.94 0 .97.97 0 0 1 1.94 0z"/>',
    "yt": '<path d="M21.6 7.2s-.2-1.4-.8-2c-.75-.8-1.6-.8-2-.85C16 4.2 12 4.2 12 4.2h-.01s-4 0-6.8.2c-.4.05-1.24.05-2 .85-.6.6-.79 2-.79 2S2.2 8.8 2.2 10.5v1.6c0 1.6.2 3.3.2 3.3s.19 1.4.79 2c.76.8 1.76.77 2.2.86 1.6.15 6.8.2 6.8.2s4 0 6.8-.21c.4-.05 1.25-.05 2-.85.6-.6.8-2 .8-2s.2-1.6.2-3.3v-1.6c0-1.6-.2-3.3-.2-3.3zM9.9 14.1V8.4l5.2 2.86-5.2 2.84z"/>',
}


def social(kind):
    return ('<svg%s viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">%s</svg>'
            % (SVG_DIM, SOCIAL_SVG[kind]))


def seo_title(headline, limit=62):
    """Append the brand only as far as the SERP will actually show it.

    Google truncates titles around 580px, roughly 60 characters. A long
    descriptive headline earns its place more than a brand suffix that gets
    cut off mid-word, so the suffix degrades rather than overflowing."""
    headline = headline.strip()
    for suffix in (" | " + NAME_PLAIN, " | CA Natasha & Co.", " | CA Bhopal"):
        if len(headline) + len(suffix) <= limit:
            return headline + suffix
    return headline


# ---------------------------------------------------------------- head
# Two requests on purpose. Headings (Fraunces) swap in, because the display
# face is the brand. Body text (Inter) is `optional`: if it is not ready within
# ~100ms the page keeps the metric-matched Arial fallback defined in nc.css,
# and cached visits get Inter immediately. Swapping the body font late
# re-painted the lead paragraph, which on inner pages is the Largest
# Contentful Paint element, and measured ~0.45s slower LCP on a throttled phone.
_FONT_DISPLAY = ("https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;"
                 "9..144,500;9..144,600;9..144,700&display=swap")
_FONT_BODY = "https://fonts.googleapis.com/css2?family=Inter:wght@400;450;500;600;700&display=optional"
FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    + "".join(
        '<link rel="preload" as="style" href="%(u)s">\n'
        '<link rel="stylesheet" href="%(u)s" media="print" onload="this.media=\'all\'">\n'
        % {"u": u.replace("&", "&amp;")} for u in (_FONT_DISPLAY, _FONT_BODY))
    + '<noscript><link rel="stylesheet" href="%s"><link rel="stylesheet" href="%s"></noscript>'
    % (_FONT_DISPLAY.replace("&", "&amp;"), _FONT_BODY.replace("&", "&amp;"))
)


def head(title, desc, slug, *, og_type="website", image=None, published=None,
         modified=None, schema="", keywords=None, noindex=False, extra_css="",
         section=None):
    """Full <head>. `slug` is the file name, e.g. 'about-us.html' or '' for home."""
    url = SITE + "/" + slug if slug and slug != "index.html" else SITE + "/"
    img = image or OG_IMAGE
    if img:
        import re
        img = re.sub(r"^https?://(?:www\.)?canatasha\.com", SITE, img)
        if not img.startswith("http"):
            img = SITE + "/" + img.lstrip("/")

    robots = ("noindex, nofollow" if noindex else
              "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1")

    kw = keywords or ("Chartered Accountant Bhopal, CA in Bhopal, Natasha and Company, "
                      "Tax Consultant Bhopal, GST Notice Bhopal, Company Registration Bhopal, "
                      "CA Natasha Rajvaidya, Tax Audit 44AB")

    art = ""
    if og_type == "article":
        if published:
            art += '\n<meta property="article:published_time" content="%s">' % published
        if modified:
            art += '\n<meta property="article:modified_time" content="%s">' % modified
        art += '\n<meta property="article:author" content="%s">' % FOUNDER
        if section:
            art += '\n<meta property="article:section" content="%s">' % section

    return """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{kw}">
<meta name="author" content="{founder}, {name_plain}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">

<meta name="theme-color" content="#0E4B8C">
<meta name="color-scheme" content="light">
<meta name="format-detection" content="telephone=yes">

<meta name="geo.region" content="IN-MP">
<meta name="geo.placename" content="Bhopal, Madhya Pradesh">
<meta name="geo.position" content="{lat};{lon}">
<meta name="ICBM" content="{lat}, {lon}">

<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{name_plain}">
<meta property="og:locale" content="en_IN">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{name_plain} — Chartered Accountants, Bhopal">{art}

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{img}">

<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="images/brand/favicon-32.png">
<link rel="apple-touch-icon" href="images/brand/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">

{fonts}
<link rel="stylesheet" href="assets/css/nc.css?v=2.2">{extra_css}
{schema}""".format(
        title=title, desc=desc, kw=kw, url=url, img=img, og_type=og_type,
        robots=robots, art=art, fonts=FONTS, schema=schema, extra_css=extra_css,
        founder=FOUNDER, name_plain=NAME_PLAIN, lat=LAT, lon=LON)


# ---------------------------------------------------------------- schema
ORG_ID = SITE + "/#organization"
SITE_ID = SITE + "/#website"


def org_schema():
    """AccountingService — the primary entity Google and AI engines resolve to."""
    return """{
  "@context": "https://schema.org",
  "@type": ["AccountingService", "ProfessionalService", "LocalBusiness"],
  "@id": "%(org)s",
  "name": "%(name)s",
  "alternateName": ["CA Natasha & Co.", "Natasha and Company Bhopal"],
  "url": "%(site)s/",
  "logo": {"@type": "ImageObject", "url": "%(site)s/images/brand/icon-512.png", "width": 512, "height": 512},
  "image": ["%(site)s/images/brand/og-card.jpg", "%(site)s/images/brand/logo-horizontal.png"],
  "description": "ISO 9001:2015 certified Chartered Accountancy firm in Bhopal founded by CA Natasha Rajvaidya (FCA). Statutory and tax audit, GST litigation, income tax notice defence, company registration and corporate advisory.",
  "telephone": "%(phone)s",
  "email": "%(email)s",
  "priceRange": "$$",
  "currenciesAccepted": "INR",
  "paymentAccepted": "Cash, UPI, Bank Transfer, Cheque",
  "foundingDate": "2017",
  "sameAs": %(same_as)s,
  "founder": {
    "@type": "Person",
    "name": "%(founder)s",
    "jobTitle": "Founder & Managing Partner, FCA",
    "worksFor": {"@id": "%(org)s"},
    "alumniOf": "The Institute of Chartered Accountants of India",
    "sameAs": %(same_as)s,
    "knowsAbout": ["Income Tax", "GST", "Statutory Audit", "Tax Audit u/s 44AB", "Company Law", "ROC Compliance", "Transfer Pricing", "NRI Taxation"]
  },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "%(street)s",
    "addressLocality": "%(city)s",
    "addressRegion": "%(region)s",
    "postalCode": "%(postal)s",
    "addressCountry": "IN"
  },
  "geo": {"@type": "GeoCoordinates", "latitude": %(lat)s, "longitude": %(lon)s},
  "hasMap": "https://www.google.com/maps/search/?api=1&query=%(lat)s,%(lon)s",
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
    "opens": "10:00", "closes": "19:00"
  }],
  "areaServed": [
    {"@type": "City", "name": "Bhopal"},
    {"@type": "State", "name": "Madhya Pradesh"},
    {"@type": "Country", "name": "India"}
  ],
  "knowsLanguage": ["en-IN", "hi-IN"],
  "hasCredential": {
    "@type": "EducationalOccupationalCredential",
    "credentialCategory": "certification",
    "name": "ISO 9001:2015 Quality Management Certification"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "%(rating)s",
    "reviewCount": "%(reviews)s",
    "bestRating": "5"
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Chartered Accountancy Services",
    "itemListElement": [
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Statutory Audit & Assurance", "url": "%(site)s/tax-audit-44ab-bhopal.html"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Tax Audit under Section 44AB", "url": "%(site)s/tax-audit-44ab-bhopal.html"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "GST Notice & Litigation Defence", "url": "%(site)s/gst-notice-consultant-bhopal.html"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Income Tax Notice & Scrutiny Representation", "url": "%(site)s/income-tax-notice-consultant-bhopal.html"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Company Registration & ROC Compliance", "url": "%(site)s/company-registration-bhopal.html"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "PSARA & PWD Contractor Registration", "url": "%(site)s/psara-pwd-contractor-registration-madhya-pradesh.html"}}
    ]
  }
}""" % dict(org=ORG_ID, site=SITE, name=NAME_PLAIN, phone=PHONE, email=EMAIL,
            founder=FOUNDER, street=STREET, city=CITY, region=REGION,
            postal=POSTAL, lat=LAT, lon=LON, rating=RATING, reviews=REVIEW_COUNT,
            same_as=json.dumps(SAME_AS))


def website_schema():
    return """{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "@id": "%(sid)s",
  "url": "%(site)s/",
  "name": "%(name)s",
  "publisher": {"@id": "%(org)s"},
  "inLanguage": "en-IN",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {"@type": "EntryPoint", "urlTemplate": "%(site)s/blog.html?q={search_term_string}"},
    "query-input": "required name=search_term_string"
  }
}""" % dict(sid=SITE_ID, site=SITE, name=NAME_PLAIN, org=ORG_ID)


def crumbs_schema(trail, url=None):
    """trail = [(name, slug_or_None), ...]; last item is the current page."""
    items = []
    n = len(trail)
    for i, (label, slug) in enumerate(trail, 1):
        entry = '{"@type": "ListItem", "position": %d, "name": "%s"' % (i, label.replace('"', "'"))
        target = slug
        if target is None and i == n and url:
            target = url
        if target is not None:
            if target.startswith("http"):
                u = target
            elif target in ("", "index.html"):
                u = SITE + "/"
            else:
                u = SITE + "/" + target.lstrip("/")
            entry += ', "item": "%s"' % u
        items.append(entry + "}")
    return ('{\n  "@context": "https://schema.org",\n  "@type": "BreadcrumbList",\n'
            '  "itemListElement": [\n    %s\n  ]\n}' % ",\n    ".join(items))


def faq_schema(pairs):
    qs = []
    for q, a in pairs:
        qs.append('{"@type": "Question", "name": %s, "acceptedAnswer": {"@type": "Answer", "text": %s}}'
                  % (_j(q), _j(a)))
    return ('{\n  "@context": "https://schema.org",\n  "@type": "FAQPage",\n'
            '  "mainEntity": [\n    %s\n  ]\n}' % ",\n    ".join(qs))


def faq_accordion(pairs, title="Frequently asked questions", eyebrow="Questions"):
    if not pairs:
        return ""
    items = "".join(
        '<details><summary>%s</summary><div class="nc-faq-a"><p>%s</p></div></details>' % (q, a)
        for q, a in pairs
    )
    return """<section class="nc-sec">
  <div class="nc-wrap nc-wrap-nar">
    <div class="nc-sec-head" data-nc-rise><span class="nc-eyebrow">%s</span><h2>%s</h2></div>
    <div class="nc-faq" data-nc-rise>%s</div>
  </div>
</section>""" % (eyebrow, title, items)


def _j(s):
    import json
    import re
    return json.dumps(re.sub(r"<[^>]+>", "", s).replace("&amp;", "&").replace("&rsaquo;", ">").strip())


def ld(*blocks):
    return "\n".join('<script type="application/ld+json">\n%s\n</script>' % b
                     for b in blocks if b)


# ---------------------------------------------------------------- nav data
NAV = [
    ("Home", "index.html", None),
    ("About", "about-us.html", [
        ("About the Firm", "about-us.html", "Our practice, standards and story"),
        ("CA Natasha Rajvaidya (FCA)", "about-us.html#founder", "Founder &amp; Managing Partner"),
        ("Vision &amp; Mission", "about-us.html#vision", "What we hold ourselves to"),
        ("ISO 9001:2015 Standards", "about-us.html#quality", "Certified quality management"),
        ("Careers", "career.html", "Open roles &amp; articleship"),
    ]),
    ("Services", "services.html", [
        ("Accounting &amp; Bookkeeping", "accounting-bookkeeping-services-bhopal.html", "Indian GAAP, reconciliations, MIS"),
        ("Income Tax &amp; ITR Filing", "income-tax-return-filing-bhopal.html", "ITR, TDS, corporate tax planning"),
        ("Tax Audit u/s 44AB", "tax-audit-44ab-bhopal.html", "Turnover thresholds, Form 3CD"),
        ("GST Notice &amp; Litigation", "gst-notice-consultant-bhopal.html", "ASMT-10, DRC-01, appeals"),
        ("Income Tax Notice Defence", "income-tax-notice-consultant-bhopal.html", "143(1), 143(2), 148 scrutiny"),
        ("Company Registration &amp; ROC", "company-registration-bhopal.html", "Pvt Ltd, LLP, OPC, annual filing"),
        (None, None, None),
        ("Business Advisory &amp; Valuation", "business-advisory-valuation-bhopal.html", "Valuation, funding, restructuring"),
        ("Virtual CFO &amp; Cloud Accounting", "virtual-cfo-services-bhopal.html", "Outsourced finance function"),
        ("NRI Taxation &amp; Property", "nri-taxation-services-bhopal.html", "Section 195, 15CA/CB, DTAA"),
        ("Financial Planning &amp; FP&amp;A", "financial-planning-fpa-bhopal.html", "Forecasting, trusts, succession"),
        ("PSARA &amp; PWD Contractor", "psara-pwd-contractor-registration-madhya-pradesh.html", "Madhya Pradesh licensing"),
        (None, None, None),
        ("All 11 Practice Areas", "services.html", "The complete service portfolio"),
    ]),
    ("GST", "gst-notice-consultant-bhopal.html", [
        ("GST Notice &amp; Litigation", "gst-notice-consultant-bhopal.html", "Section 73 &amp; 74 defence"),
        ("GST Calculator", "gst-calculator.html", "Inclusive, exclusive, CGST/SGST split"),
        ("GST Due Dates", "knowledge-base.html#due-dates", "GSTR-1, 3B, 9 and 9C"),
        ("ISD Registration Guide", "isd-registration-now-mandatory-from-april-2025-dont-lose-your-gst-credit.html", "Mandatory from April 2025"),
        ("54th GST Council Decisions", "overview-of-the-54th-gst-council-meeting-key-decisions-their-implications.html", "Key changes explained"),
        (None, None, None),
        ("GST Official Portal", "https://www.gst.gov.in/", "Returns, registration, e-way bills"),
    ]),
    ("Knowledge Bank", "knowledge-base.html", "MEGA"),
    ("Insights", "blog.html", None),
    ("Contact", "contact-us.html", None),
]


def header_html():
    rows = []
    for label, href, kids in NAV:
        if kids == "MEGA":
            rows.append(
                '<li class="has-drop"><a href="%s" aria-expanded="false" aria-haspopup="true">%s %s</a>'
                '<div class="nc-drop nc-drop-mega">%s</div></li>'
                % (href, label, ico("caret"), KB.mega_html()))
            continue
        if not kids:
            rows.append('<li><a href="%s">%s</a></li>' % (href, label))
            continue
        sub = []
        for k in kids:
            if k[0] is None:
                sub.append('<div class="nc-drop-sep"></div>')
            else:
                sub.append('<a href="%s">%s<small>%s</small></a>' % (k[1], k[0], k[2]))
        rows.append(
            '<li class="has-drop"><a href="%s" aria-expanded="false" aria-haspopup="true">%s %s</a>'
            '<div class="nc-drop">%s</div></li>' % (href, label, ico("caret"), "".join(sub)))

    macc = []
    for label, href, kids in NAV:
        if kids == "MEGA":
            macc.append(
                '<li><button type="button" aria-expanded="false">%s %s</button>'
                '<div class="nc-msub"><div>%s</div></div></li>'
                % (label, ico("caret"), KB.mobile_html()))
            continue
        if not kids:
            macc.append('<li><a href="%s">%s</a></li>' % (href, label))
            continue
        links = "".join('<a href="%s">%s</a>' % (k[1], k[0]) for k in kids if k[0])
        macc.append(
            '<li><button type="button" aria-expanded="false">%s %s</button>'
            '<div class="nc-msub"><div>%s</div></div></li>' % (label, ico("caret"), links))

    return """<a class="nc-skip" href="#main">Skip to content</a>

<div class="nc-topbar">
  <div class="nc-wrap nc-topbar-in">
    <div class="nc-topbar-l">
      <a href="tel:{phone}">{ph_ico} {phone_d}</a>
      <a href="mailto:{email}">{ml_ico} {email}</a>
      <span class="nc-hide-m" style="display:inline-flex;align-items:center;gap:.45rem;font-size:.815rem">{pin_ico} Zone-1, M.P. Nagar, Bhopal</span>
    </div>
    <div class="nc-topbar-r">{profiles}</div>
  </div>
</div>

<div class="nc-strip">
  ISO 9001:2015 Certified Practice &nbsp;&middot;&nbsp; Serving Madhya Pradesh since 2017
  &nbsp;&middot;&nbsp; <a href="{book}">Book a consultation</a>
</div>

<header class="nc-hdr">
  <div class="nc-wrap nc-hdr-in">
    <a class="nc-logo" href="index.html" aria-label="{name_plain} — home">
      <picture>
        <source srcset="images/brand/logo-horizontal-520.webp" type="image/webp">
        <img src="images/brand/logo-horizontal-520.png" alt="{name_plain} — Chartered Accountants, Bhopal" width="216" height="54" fetchpriority="high">
      </picture>
    </a>

    <nav class="nc-nav" aria-label="Primary">
      <ul>{nav}</ul>
    </nav>

    <div class="nc-hdr-act">
      <a class="nc-btn nc-btn-sm" href="{book}">Book a consultation</a>
      <button class="nc-burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="nc-drawer">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>

<div class="nc-scrim" hidden-role="presentation"></div>
<div class="nc-drawer" id="nc-drawer" aria-hidden="true" aria-label="Menu">
  <div class="nc-drawer-top">
    <a class="nc-logo" href="index.html">
      <picture>
        <source srcset="images/brand/logo-horizontal-520.webp" type="image/webp">
        <img src="images/brand/logo-horizontal-520.png" alt="{name_plain}" width="176" height="44">
      </picture>
    </a>
    <button class="nc-drawer-close" type="button" aria-label="Close menu">&#10005;</button>
  </div>
  <div class="nc-drawer-body">
    <ul class="nc-macc">{macc}</ul>
    <div class="nc-drawer-cta">
      <a class="nc-btn nc-btn-full" href="{book}">Book a consultation</a>
      <a class="nc-btn nc-btn-ghost nc-btn-full" href="tel:{phone}">{ph_ico} {phone_d}</a>
    </div>
  </div>
</div>""".format(nav="".join(rows), macc="".join(macc), phone=PHONE, book=BOOK_URL,
                 phone_d=PHONE_DISPLAY, ph_ico=ico("phone"), name_plain=NAME_PLAIN,
                 email=EMAIL, ml_ico=ico("mail"), pin_ico=ico("pin"),
                 profiles="".join(
                     '<a href="%s" target="_blank" rel="noopener me" aria-label="%s">%s</a>'
                     % (url, label, social(kind)) for kind, label, url in PROFILES))


def footer_html():
    return """<footer class="nc-ftr">
  <div class="nc-wrap">
    <div class="nc-ftr-grid">

      <div class="nc-ftr-brand">
        <a class="nc-logo" href="index.html">
          <picture>
            <source srcset="images/brand/logo-horizontal-white.webp" type="image/webp">
            <img src="images/brand/logo-horizontal-white.png" alt="{name_plain}" width="240" height="60" loading="lazy">
          </picture>
        </a>
        <p>
          ISO 9001:2015 certified Chartered Accountancy firm in Bhopal, founded by
          {founder} (FCA). Audit, taxation, GST litigation and corporate advisory
          for businesses across Madhya Pradesh since 2017.
        </p>
        <div class="nc-social">
{profiles}
        </div>
      </div>

      <div>
        <h2 class="nc-ftr-h">Practice areas</h2>
        <div class="nc-ftr-links">
          <a href="accounting-bookkeeping-services-bhopal.html">Accounting &amp; Bookkeeping</a>
          <a href="income-tax-return-filing-bhopal.html">Income Tax &amp; ITR Filing</a>
          <a href="tax-audit-44ab-bhopal.html">Tax Audit u/s 44AB</a>
          <a href="gst-notice-consultant-bhopal.html">GST Notice &amp; Litigation</a>
          <a href="company-registration-bhopal.html">Company Registration &amp; ROC</a>
          <a href="virtual-cfo-services-bhopal.html">Virtual CFO Services</a>
          <a href="nri-taxation-services-bhopal.html">NRI Taxation</a>
          <a href="services.html">All 11 services</a>
        </div>
      </div>

      <div>
        <h2 class="nc-ftr-h">Free tools</h2>
        <div class="nc-ftr-links">
          <a href="income-tax-calculator.html">Income Tax Calculator</a>
          <a href="hra-exemption-calculator.html">HRA Exemption Calculator</a>
          <a href="gst-calculator.html">GST Calculator</a>
          <a href="emi-loan-calculator.html">EMI Loan Calculator</a>
          <a href="knowledge-base.html">Knowledge Base</a>
          <a href="blog.html">Insights &amp; updates</a>
        </div>
      </div>

      <div>
        <h2 class="nc-ftr-h">Get in touch</h2>
        <div class="nc-stack" style="gap:.85rem">
          <a class="nc-ctile" href="tel:{phone}">
            <span class="nc-svc-ico">{ph}</span>
            <span class="nc-ctile-t"><small>Direct line</small><b>{phone_d}</b></span>
          </a>
          <a class="nc-ctile" href="mailto:{email}">
            <span class="nc-svc-ico">{ml}</span>
            <span class="nc-ctile-t"><small>Email</small><b>{email}</b></span>
          </a>
          <div class="nc-ctile">
            <span class="nc-svc-ico">{pin}</span>
            <span class="nc-ctile-t"><small>Office</small><b>{street}, {city} {postal}</b></span>
          </div>
        </div>
      </div>

    </div>

    <div class="nc-ftr-bar">
      <p class="nc-mb0">&copy; <span data-year>2026</span> {name_plain}. All rights reserved. &nbsp;|&nbsp; ISO 9001:2015 Certified</p>
      <nav aria-label="Legal">
        <a href="privacy-policy.html">Privacy</a>
        <a href="terms-and-conditions.html">Terms</a>
        <a href="contact-us.html">Contact</a>
        <a href="sitemap.xml">Sitemap</a>
      </nav>
    </div>
  </div>
</footer>

<div class="nc-float">
  <button class="nc-fab nc-fab-top" type="button" aria-label="Back to top">{up}</button>
  <a class="nc-fab nc-fab-wa" href="https://wa.me/919407000157?text=Hello%20Natasha%20%26%20Company%2C%20I%20need%20help%20with%20"
     target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{wa}</a>
</div>""".format(name_plain=NAME_PLAIN, founder=FOUNDER, phone=PHONE,
                 phone_d=PHONE_DISPLAY, email=EMAIL, street=STREET, city=CITY,
                 postal=POSTAL, wa=social("wa"), li=social("li"),
                 profiles="".join(
                     '<a href="%s" target="_blank" rel="noopener me" aria-label="%s">%s</a>'
                     % (url, label, social(kind)) for kind, label, url in PROFILES),
                 ph=ico("phone"), ml=ico("mail"), pin=ico("pin"), up=ico("up"))


# <title> tags kept to 60 characters, primary keyword first. Google cuts a
# title at roughly 580px (~60 characters); past that the brand, and often the
# keyword, is replaced by an ellipsis. The page's own <h1> is unchanged.
SERP_TITLES = {
    "index.html": "Chartered Accountant in Bhopal | Natasha & Company",
    "services.html": "CA Services in Bhopal: Audit, Tax, GST & ROC | Natasha & Co.",
    "knowledge-base.html": "Knowledge Base: TDS Rates, CII Chart & Tax Tools | CA Bhopal",
    "privacy-policy.html": "Privacy Policy | Natasha & Company, Chartered Accountants",
    "terms-and-conditions.html": "Terms & Conditions | Natasha & Company, CA Bhopal",
    "accounting-bookkeeping-services-bhopal.html": "Accounting & Bookkeeping Services in Bhopal | Natasha & Co.",
    "business-advisory-valuation-bhopal.html": "Business Advisory & Valuation in Bhopal | Natasha & Company",
    "nri-taxation-services-bhopal.html": "NRI Tax Services: Section 195 TDS, 15CA/CB & Property Sale",
    "psara-pwd-contractor-registration-madhya-pradesh.html": "PSARA Licence & PWD Contractor Registration, Madhya Pradesh",
    "hra-exemption-calculator.html": "HRA Exemption Calculator u/s 10(13A) | Natasha & Company",
    "income-tax-calculator.html": "Income Tax Calculator FY 2025-26: Old vs New Regime",
    "beyond-numbers-the-evolving-thought-process-of-a-chartered-accountant-firm.html":
        "Beyond Numbers: How a Chartered Accountant Firm Thinks",
    "hindu-undivided-family-huf-a-strategic-way-to-save-income-tax.html":
        "HUF: A Strategic Way to Save Income Tax | Natasha & Company",
    "invest-madhya-pradesh-global-investors-summit-2025-a-catalyst-for-growth.html":
        "MP Global Investors Summit 2025: A Catalyst for Growth",
    "isd-registration-now-mandatory-from-april-2025-dont-lose-your-gst-credit.html":
        "ISD Registration Mandatory from April 2025: Protect GST ITC",
    "itr-filing-deadline-extended-to-september-15-2025-more-time-for-accurate-returns.html":
        "ITR Filing Deadline Extended to 15 September 2025",
    "mastering-itr-filing-deadlines-2024-your-comprehensive-guide.html":
        "ITR Filing Deadlines 2024: A Complete Guide",
    "maximizing-tax-savings-on-long-term-capital-gains-a-comprehensive-guide.html":
        "Long-Term Capital Gains: How to Maximise Tax Savings",
    "new-dsc-rules-for-mp-tenders-signing-encryption-now-mandatory.html":
        "New DSC Rules for MP Tenders: Signing & Encryption Mandatory",
    "overview-of-the-54th-gst-council-meeting-key-decisions-their-implications.html":
        "54th GST Council Meeting: Key Decisions Explained",
    "tax-saving-strategies-for-salaried-employees-in-the-old-regime.html":
        "Tax Saving for Salaried Employees Under the Old Regime",
    "understanding-house-rent-allowance-hra-and-its-tax-exemption.html":
        "House Rent Allowance (HRA) and Its Tax Exemption Explained",
    "unlock-the-secrets-of-nri-property-sales-in-india.html":
        "NRI Property Sales in India: What Sellers Must Know",
    "unlocking-tax-savings-exploring-equity-linked-saving-schemes-elss.html":
        "ELSS Tax Saving: Equity Linked Saving Schemes Explained",
    "why-your-gold-silver-just-got-more-precious-a-laymans-guide-by-ca-natasha-rajvaidya.html":
        "Why Gold & Silver Prices Are Rising: 6 Key Reasons",
}


def page(*, title, desc, slug, body, og_type="website", image=None,
         published=None, modified=None, schema="", keywords=None,
         noindex=False, extra_css="", body_class="", extra_js="", section=None):
    """Assemble one complete HTML document."""
    title = SERP_TITLES.get(slug, title)
    bc = ' class="%s"' % body_class if body_class else ""
    return """<!DOCTYPE html>
<html lang="en-IN">
<head>
{head}
</head>
<body{bc}>
{header}

<main id="main">
{body}
</main>

{footer}

<script src="js/lead-capture.js" defer></script>
<script src="assets/js/nc.js" defer></script>
<script src="assets/js/nc-motion.js" defer></script>{extra_js}
</body>
</html>
""".format(
        head=head(title, desc, slug, og_type=og_type, image=image,
                  published=published, modified=modified, schema=schema,
                  keywords=keywords, noindex=noindex, extra_css=extra_css,
                  section=section),
        header=header_html(), footer=footer_html(), body=webp_refs(body), bc=bc,
        extra_js=extra_js)


_WEBP_CACHE = {}
_IMG_REF = None


def webp_refs(html):
    """images/x.jpg -> images/x.webp wherever build_images.py made one.

    Matches relative references only (src, srcset, inline url()), so absolute
    share-image URLs in <head> and JSON-LD keep their JPEG.
    """
    import re
    global _IMG_REF
    if _IMG_REF is None:
        _IMG_REF = re.compile(r"(^|[\"'(,\s;])(images/[^\"'()\s,&]+?\.(?:jpe?g|png))(?=[\"')\s,&?])", re.I)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def swap(m):
        path = m.group(2)
        stem = os.path.splitext(path)[0]
        if path not in _WEBP_CACHE:
            _WEBP_CACHE[path] = os.path.exists(os.path.join(root, stem + ".webp"))
        return m.group(1) + (stem + ".webp" if _WEBP_CACHE[path] else path)

    return _IMG_REF.sub(swap, html)


# ---------------------------------------------------------------- fragments
def sec_head(eyebrow, title, lead=None, center=False, tag="h2"):
    """Section header.

    Centred headings render the first word in the accent colour, the rest in
    ink, with a rule-and-dot ornament underneath — the two-tone treatment the
    reference design uses for its section titles. Wrap words in <em> to colour
    them explicitly instead.
    """
    p = '<p>%s</p>' % lead if lead else ""
    heading = title
    if center and "<em>" not in title:
        bits = title.split(" ", 1)
        if len(bits) == 2:
            heading = "<em>%s</em> %s" % (bits[0], bits[1])
    return ('<div class="nc-sec-head" data-nc-rise>'
            '<span class="nc-eyebrow">%s</span>'
            '<%s>%s</%s>%s</div>' % (eyebrow, tag, heading, tag, p))


def crumb(trail):
    """trail = [(label, href_or_None)]"""
    out = []
    for i, (label, href) in enumerate(trail):
        if i:
            out.append('<i aria-hidden="true">/</i>')
        if href:
            out.append('<a href="%s">%s</a>' % (href, label))
        else:
            out.append('<span aria-current="page">%s</span>' % label)
    return '<nav class="nc-crumb" aria-label="Breadcrumb">%s</nav>' % "".join(out)


def cta_band(title="Let's get your compliance in order.",
             text="A 20-minute call with CA Natasha Rajvaidya is usually enough to tell you "
                  "where you stand, what it will cost, and what happens next."):
    return """<section class="nc-sec">
  <div class="nc-wrap">
    <div class="nc-cta" data-nc-rise>
      <span class="nc-eyebrow">Talk to a Chartered Accountant</span>
      <h2>%s</h2>
      <p>%s</p>
      <div class="nc-row">
        <a class="nc-btn nc-btn-lg" href="%s">Book a consultation</a>
        <a class="nc-btn nc-btn-ghost nc-btn-lg" href="tel:%s">%s Call %s</a>
      </div>
    </div>
  </div>
</section>""" % (title, text, BOOK_URL, PHONE, ico("phone"), PHONE_DISPLAY)


def split_words(markup, start=0, step=45, cap=14):
    """Wrap each word in <span class="nc-word"> at build time.

    nc-motion.js used to do this after the page loaded, which kept the page's
    <h1> invisible until deferred JavaScript ran: on a mid-range phone that
    pushed Largest Contentful Paint to ~5s. Done here, CSS can animate the
    words from the first paint. Tags (<em>, <br>, <span>) pass through intact.
    """
    import re
    out, i = [], start
    for part in re.split(r"(<[^>]+>)", markup):
        if not part or part.startswith("<"):
            out.append(part)
            continue
        for tok in re.split(r"(\s+)", part):
            if not tok or tok.isspace():
                out.append(tok)
                continue
            out.append('<span class="nc-word" style="--wd:%dms">%s</span>' % (min(i, cap) * step, tok))
            i += 1
    return "".join(out)


def phero(title, lead, trail):
    return """<section class="nc-phero">
  <div class="nc-wrap">
    %s
    <h1 data-nc-rise>%s</h1>
    <p class="nc-lead" data-nc-rise style="--d:90ms">%s</p>
  </div>
</section>""" % (crumb(trail), split_words(title), lead)


MARQUEE = [
    "Tax Audit u/s 44AB", "GST Notice Defence", "Income Tax Scrutiny",
    "Company Registration", "ROC Compliance", "Virtual CFO", "NRI Taxation",
    "Statutory Audit", "TDS &amp; TCS", "Section 128A Amnesty",
    "PSARA Licensing", "PWD Contractor", "ITR Filing", "Transfer Pricing",
]


def marquee():
    """A slow band of practice keywords. Duplicated once so the loop is
    seamless; the copy is hidden from assistive tech."""
    row = "".join("<span>%s</span>" % k for k in MARQUEE)
    return ('<div class="nc-marquee" aria-label="Practice areas">'
            '<div class="nc-marquee-track">%s<span aria-hidden="true">%s</span></div>'
            '</div>' % (row, "</span><span aria-hidden=\"true\">".join(MARQUEE)))


def close_heading_gaps(body):
    import re
    """Renumber headings so none is more than one level below the last.

    The page H1 is the article title, so the body starts at h2. Several
    articles were written with h3 sections directly under the title; screen
    readers and crawlers read that as a missing level.
    """
    out, pos, prev, remap = [], 0, 1, {}
    for m in re.finditer(r"<(/?)h([2-6])\b", body):
        closing, lvl = m.group(1), int(m.group(2))
        if closing:
            new = remap.get(lvl, lvl)
        else:
            new = min(lvl, prev + 1)
            remap[lvl] = new
            # deeper levels seen earlier must follow this one down
            for deeper in [k for k in remap if k > lvl]:
                del remap[deeper]
            prev = new
        out.append(body[pos:m.start()])
        out.append("<%sh%d" % (closing, new))
        pos = m.end()
    out.append(body[pos:])
    return "".join(out)
