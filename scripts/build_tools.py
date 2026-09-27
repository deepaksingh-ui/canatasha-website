# -*- coding: utf-8 -*-
"""
Migrate the four calculators.

Their inline JavaScript carries current, correct tax logic (FY 2025-26 /
AY 2026-27, Finance Act 2025) bound to Bootstrap-classed markup by element id.
Both the markup and the scripts are carried over byte for byte; only the page
shell changes, and nc-compat.css restyles the utility classes. Nothing that
computes a number is touched.
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nc_shell as S

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CALC_DIR = os.path.join(HERE, "calc_sources")
SRC = os.path.join(ROOT, "backup", "pre-redesign-20260905-134251")

PAGES = [
    ("income-tax-calculator.html", "Income Tax Calculator",
     "Income Tax Calculator FY 2025-26 (AY 2026-27) | Old vs New Regime",
     "Free income tax calculator for FY 2025-26 / AY 2026-27 under the Finance Act 2025. "
     "Compare the old and new regimes, see slab-wise tax, surcharge, cess and your effective "
     "rate. Built by Natasha & Company, Chartered Accountants, Bhopal.",
     "Compare the old and new regimes under the Finance Act 2025, with slab-wise workings, "
     "surcharge, cess and your effective rate."),
    ("hra-exemption-calculator.html", "HRA Exemption Calculator",
     "HRA Exemption Calculator | Section 10(13A) — CA Natasha & Company",
     "Calculate your House Rent Allowance exemption under Section 10(13A). Enter basic salary, "
     "dearness allowance, HRA received, rent paid and city type to see the exempt and taxable "
     "portions with the full three-limb working.",
     "The Section 10(13A) exemption is the least of three limbs. This shows all three, so you "
     "can see which one is binding."),
    ("gst-calculator.html", "GST Calculator",
     "GST Calculator | Inclusive & Exclusive of Tax — CA Bhopal",
     "Free GST calculator for 5%, 12%, 18% and 28% slabs. Split any amount inclusive or "
     "exclusive of GST, with CGST, SGST and IGST breakdown. From Natasha & Company, "
     "Chartered Accountants, Bhopal.",
     "Split any amount inclusive or exclusive of GST across the standard slabs, with the "
     "CGST, SGST and IGST split."),
    ("emi-loan-calculator.html", "EMI Loan Calculator",
     "EMI Calculator | Loan Instalment & Amortisation — CA Bhopal",
     "Free EMI calculator for home, business, car and personal loans. See your monthly "
     "instalment, total interest, total repayment and the full amortisation schedule. "
     "From Natasha & Company, Bhopal.",
     "Monthly instalment, total interest and the full amortisation schedule for any loan "
     "amount, rate and tenure."),
]

CALC_FAQS = {
    "gst-calculator.html": [
        ("How do I calculate GST inclusive and exclusive amounts?",
         "To calculate GST exclusive (add GST): GST Amount = (Base Amount &times; GST Rate) &divide; 100, and Total Invoice = Base + GST. To calculate GST inclusive (remove GST): Base Amount = (Total Amount &times; 100) &divide; (100 + GST Rate), and GST Amount = Total &minus; Base Amount."),
        ("What is the difference between CGST, SGST, and IGST?",
         "For intra-state transactions (within the same state, e.g. MP to MP), GST is split equally between Central GST (CGST) and State GST (SGST). For inter-state transactions (between two different states), Integrated GST (IGST) is levied at the full statutory rate."),
        ("What are the statutory GST rate slabs in India?",
         "India has statutory GST slabs: 0% (essential food and grains), 0.25% (rough precious stones), 3% (gold, silver, and precious metals), 5% (essentials, transport, economy footwear), 12% (processed foods, business services), 18% (standard goods and majority of professional services), and 28% (luxury and sin goods)."),
        ("When is GST registration mandatory for a business in Bhopal?",
         "GST registration is mandatory if aggregate turnover exceeds &#8377;40 Lakhs for goods (&#8377;20 Lakhs for services in Madhya Pradesh), or for any inter-state supply, e-commerce selling, or reverse charge mechanism (RCM) applicability.")
    ],
    "income-tax-calculator.html": [
        ("How does Section 87A marginal relief work under the New Tax Regime for FY 2025-26?",
         "Under the Finance Act 2025 New Tax Regime, taxable income up to &#8377;12,00,000 pays zero tax due to the Section 87A rebate (up to &#8377;60,000). For income exceeding &#8377;12,00,000, statutory marginal relief ensures that the total tax payable cannot exceed the amount by which taxable income exceeds &#8377;12,00,000. This marginal relief fully phases out at the break-even income of &#8377;12,70,588."),
        ("What is the standard deduction in FY 2025-26 (AY 2026-27)?",
         "For salaried individuals, the standard deduction under the New Tax Regime is &#8377;75,000 (increased from &#8377;50,000 by the Finance Act 2024/2025). Under the Old Tax Regime, the standard deduction remains &#8377;50,000. Non-salaried and self-employed professionals are not eligible for standard deduction."),
        ("How is Surcharge Marginal Relief calculated for high net-worth incomes?",
         "Surcharge applies at 10% above &#8377;50 Lakhs, 15% above &#8377;1 Crore, and 25% above &#8377;2 Crores. Surcharge marginal relief caps the total tax plus surcharge payable at the threshold tax plus the incremental income earned over that threshold (e.g. &#8377;50L, &#8377;1Cr, or &#8377;2Cr)."),
        ("Which tax regime should I choose: Old or New?",
         "The New Tax Regime is beneficial for individuals with deductions (Section 80C, 80D, HRA, Home Loan Interest) lower than approximately &#8377;3.75 Lakhs to &#8377;4.25 Lakhs. If your total eligible deductions exceed this threshold, the Old Regime may result in lower tax liability. CA Natasha &amp; Company provides personalized regime selection advisory.")
    ],
    "hra-exemption-calculator.html": [
        ("How is HRA exemption calculated under Section 10(13A)?",
         "Under Rule 2A of the Income Tax Rules, HRA exemption is calculated as the minimum of three limbs: (1) Actual HRA received from employer, (2) Rent paid minus 10% of salary (Basic + DA), and (3) 50% of salary for metro cities (Delhi, Mumbai, Kolkata, Chennai) or 40% of salary for non-metro cities (such as Bhopal, Indore, Pune)."),
        ("When is the Landlord's PAN mandatory for claiming HRA?",
         "Under CBDT Circular 08/2013, if total annual rent paid exceeds &#8377;1,00,000 (&#8377;8,333 per month), it is mandatory to report the landlord's PAN to your employer. If the landlord does not have a PAN, a signed Form 60 declaration along with landlord identity proof must be obtained."),
        ("What is Section 194-IB TDS on high rent payments?",
         "Under Section 194-IB, any individual or HUF paying rent exceeding &#8377;50,000 per month must deduct 5% TDS from the rent paid to the landlord and deposit it using Challan-cum-statement Form 26QC."),
        ("Can I claim HRA exemption under the New Tax Regime?",
         "No, HRA exemption under Section 10(13A) is disallowed under the New Tax Regime (Section 115BAC). You must opt for the Old Tax Regime to claim HRA tax exemption.")
    ],
    "emi-loan-calculator.html": [
        ("How is monthly loan EMI calculated?",
         "Monthly EMI is computed using the standard reducing-balance amortisation formula: EMI = [P &times; R &times; (1+R)<sup>N</sup>] &divide; [(1+R)<sup>N</sup> &minus; 1], where P is Principal loan amount, R is monthly interest rate (Annual rate &divide; 12 &divide; 100), and N is loan tenure in months."),
        ("What is an amortization schedule?",
         "An amortization schedule is an itemized year-by-year table displaying the breakdown of every loan payment into principal repayment and interest expense, tracking the reduction of the outstanding loan balance to zero over time."),
        ("Can loan interest and principal repayment save income tax in India?",
         "For home loans under the Old Tax Regime, principal repayment is eligible for deduction up to &#8377;1.5 Lakhs under Section 80C, and interest paid on self-occupied house property is deductible up to &#8377;2 Lakhs under Section 24(b). For business loans, 100% of interest paid is an allowable business expense under Section 36(1)(iii)."),
        ("What is CMA Data for bank loan sanctions?",
         "Credit Monitoring Arrangement (CMA) Data is a comprehensive financial report analyzing past, current, and projected financial statements, cash flows, and debt service coverage ratios (DSCR) required by commercial banks for approving working capital and term loans. Natasha &amp; Company prepares CA-certified CMA Data reports.")
    ]
}


def dedupe_document(html, slug):
    """Return the real document when a file holds more than one.

    income-tax-calculator.html shipped with two complete pages concatenated:
    an older copy, then an unclosed <script> at line 509, then a newer copy.
    Browsers treat everything after that unclosed tag as script text, so the
    newer page — the one with the hero and the consultation modal — never
    rendered. Where a second <body> exists, the later document is the live one.
    """
    bodies = [m.start() for m in re.finditer(r"<body\b", html)]
    if len(bodies) < 2:
        return html
    print("    NOTE %s carried %d concatenated documents "
          "(unclosed <script>); using the last one." % (slug, len(bodies)))
    return html[bodies[-1]:]


def region(html):
    """Everything between </header> and the footer — the calculator itself."""
    start = html.find("</header>")
    if start < 0:
        return None
    start += len("</header>")
    for marker in ("<!-- Main Footer", "<footer", "<!-- Footer"):
        end = html.find(marker, start)
        if end > 0:
            return html[start:end]
    return None


def repair_strings(js):
    """Turn raw newlines inside quoted JS strings into \\n escapes.

    The original calculators shipped a WhatsApp handler whose message string
    was written across several lines inside double quotes:

        var text = "* NEW CA CONSULTATION REQUEST *
        " + ...

    That is a syntax error, so the whole block — caWhatsApp and the lead
    handlers with it — never parsed, on the old site as well as this one.
    Walk the source tracking string state and escape the offending newlines.
    """
    out = []
    quote = None          # the character that opened the current string
    i, n = 0, len(js)
    while i < n:
        c = js[i]

        if quote:
            if c == "\\" and i + 1 < n:      # keep escapes intact
                out.append(js[i:i + 2])
                i += 2
                continue
            if c == "\n":
                out.append("\\n")
                i += 1
                continue
            if c == "\r":
                i += 1
                continue
            if c == quote:
                quote = None
            out.append(c)
            i += 1
            continue

        # outside a string: skip over comments so their contents are left alone
        if c == "/" and i + 1 < n and js[i + 1] == "/":
            j = js.find("\n", i)
            j = n if j < 0 else j
            out.append(js[i:j])
            i = j
            continue
        if c == "/" and i + 1 < n and js[i + 1] == "*":
            j = js.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out.append(js[i:j])
            i = j
            continue

        if c in "\"'":
            quote = c
        out.append(c)
        i += 1

    return "".join(out)


def scripts(html):
    """Inline <script> blocks that belong to the calculator, in order."""
    out = []
    for m in re.finditer(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", html, re.S):
        js = m.group(1)
        # Skip the legacy theme bootstrapping and any JSON-LD.
        if "application/ld+json" in m.group(0):
            continue
        if re.search(r"\$\(document\)|jQuery|owl[Cc]arousel|\.wow\(", js):
            continue
        if len(js.strip()) < 40:
            continue
        out.append(repair_strings(js))
    return out


def scrub(seg):
    """Drop legacy chrome that the new shell already provides."""
    # Old mobile nav, search popup, modals bound to Bootstrap JS, scroll-to-top.
    for pat in (r'<div class="mobile-menu">.*?</div>\s*</nav>\s*</div>',
                r'<div id="search-popup".*?</div>\s*</div>\s*</div>',
                r'<div class="scroll-to-top.*?</div>',
                r'<div class="sticky-header">.*?</div>\s*</div>\s*</div>'):
        seg = re.sub(pat, "", seg, flags=re.S)
    # Modals need Bootstrap's JS, which is gone. Remove them, then turn the
    # buttons that used to open them into real links to the contact page so
    # the call to action still goes somewhere.
    seg = re.sub(r'<div class="modal fade".*?</div>\s*</div>\s*</div>\s*</div>', "", seg, flags=re.S)

    # The income tax calculator also carried the old Bootstrap off-canvas
    # mobile menu. Without Bootstrap it rendered as a bare logo and a raw list
    # of links under the page hero. Remove every such block, counting nested
    # divs so the whole drawer goes and nothing after it.
    while True:
        m = re.search(r'<div class="offcanvas\b', seg)
        if not m:
            break
        depth, i = 0, m.start()
        for t in re.finditer(r"<(/?)div\b", seg[m.start():]):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                i = m.start() + t.end()
                i = seg.index(">", i) + 1
                break
        else:
            break
        seg = seg[:m.start()] + seg[i:]
    seg = re.sub(r'<button[^>]*data-bs-toggle="offcanvas".*?</button>', "", seg, flags=re.S)

    def relink(m):
        inner = m.group(2)
        cls = re.search(r'class="([^"]*)"', m.group(1))
        return '<a href="%s"%s>%s</a>' % (
            S.BOOK_URL, ' class="%s"' % cls.group(1) if cls else "", inner)
    seg = re.sub(r'<button([^>]*data-bs-target="#consultationModal"[^>]*)>(.*?)</button>',
                 relink, seg, flags=re.S)

    seg = re.sub(r'\sdata-bs-[a-z-]+="[^"]*"', "", seg)
    # Scripts are re-emitted once at the end of <body>; drop them here so the
    # calculator logic is not defined twice.
    seg = re.sub(r"<script(?![^>]*\bsrc=)[^>]*>.*?</script>", "", seg, flags=re.S)
    seg = re.sub(r'<script[^>]*\bsrc="[^"]*"[^>]*>\s*</script>', "", seg)
    # The page hero supplies the <h1>; demote any the region carried so each
    # page keeps exactly one.
    seg = re.sub(r"<(/?)h1\b", r"<\1h2", seg)
    # Some calculators print a branded result sheet; point it at the current
    # lockup instead of the retired logo files.
    seg = (seg.replace("images/logo-original.webp", "images/brand/logo-horizontal-520.webp")
              .replace("images/logo-original.png", "images/brand/logo-horizontal-520.png"))
    return seg.strip()


def build(slug, short, title, desc, blurb):
    content_file = os.path.join(CALC_DIR, slug.replace(".html", "-content.html"))
    script_file = os.path.join(CALC_DIR, slug.replace(".html", "-script.js"))
    if os.path.exists(content_file) and os.path.exists(script_file):
        seg = io.open(content_file, encoding="utf-8").read()
        js = "\n<script>\n" + io.open(script_file, encoding="utf-8").read() + "\n</script>"
    else:
        html = io.open(os.path.join(SRC, slug), encoding="utf-8").read()
        html = dedupe_document(html, slug)

        seg = region(html)
        if not seg:
            return "no content region"
        seg = scrub(seg)

        js = "".join('\n<script>%s</script>' % s for s in scripts(html))

    phero = S.phero(short, blurb,
                    [("Home", "index.html"), ("Knowledge Base", "knowledge-base.html"),
                     (short, slug)])
    faq_items = CALC_FAQS.get(slug, [])
    faq_html = S.faq_accordion(faq_items) if faq_items else ""
    faq_ld = S.faq_schema(faq_items) if faq_items else ""

    body = """{phero}

{seg}

{faq_html}

{cta}""".format(
        phero=phero,
        seg=seg,
        faq_html=faq_html,
        cta=S.cta_band(
            title="Numbers look off? Let us check the real position.",
            text="A calculator works from what you type in. A Chartered Accountant works from "
                 "your actual books, notices and prior filings &mdash; which is usually where "
                 "the difference lives."))

    app_ld = """{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "@id": "%(site)s/%(slug)s#app",
  "name": "%(name)s",
  "url": "%(site)s/%(slug)s",
  "applicationCategory": "FinanceApplication",
  "operatingSystem": "Any",
  "browserRequirements": "Requires JavaScript",
  "description": "%(desc)s",
  "inLanguage": "en-IN",
  "isAccessibleForFree": true,
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "INR"},
  "publisher": {"@id": "%(org)s"},
  "provider": {"@id": "%(org)s"}
}""" % dict(site=S.SITE, slug=slug, name=short,
            desc=desc.replace('"', "'")[:280], org=S.ORG_ID)

    doc = S.page(
        title=title, desc=desc, slug=slug, body=body,
        extra_css='\n<link rel="stylesheet" href="assets/css/nc-compat.css">',
        extra_js=js,
        schema=S.ld(app_ld, faq_ld, S.org_schema(),
                    S.crumbs_schema([("Home", "index.html"),
                                     ("Knowledge Base", "knowledge-base.html"),
                                     (short, slug)])),
        keywords="%s, %s Bhopal, CA Bhopal, Chartered Accountant Bhopal, CA Natasha Rajvaidya"
                 % (short, short))

    with io.open(os.path.join(ROOT, slug), "w", encoding="utf-8") as f:
        f.write(doc)
    return None


def main():
    for slug, short, title, desc, blurb in PAGES:
        err = build(slug, short, title, desc, blurb)
        if err:
            print("  SKIP  %-40s %s" % (slug, err))
        else:
            print("  built %-40s %3d KB" % (slug, os.path.getsize(os.path.join(ROOT, slug)) // 1024))


if __name__ == "__main__":
    main()
