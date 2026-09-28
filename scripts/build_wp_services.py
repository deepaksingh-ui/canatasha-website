# -*- coding: utf-8 -*-
"""
Service pages carried forward from the live WordPress site.

The live www.canatasha.com has a page for each of these services. The static
rebuild had folded them into one-line mentions, which would have thrown away
indexed pages and the firm's own copy. Each is rebuilt here, in the new
design, from scripts/wp_snapshot/<slug>.json (see fetch_wp.py), at the same
slug so the old URL maps one-to-one: /bank-audit/ -> /bank-audit.html.

The body text is the firm's, unchanged apart from cleanup of Elementor
artefacts (duplicated headings, a step that repeated the next step's text).
Titles, descriptions and grouping are written here.

Not rebuilt, on purpose (they redirect instead, see _url_map.py):
  tax-audit, gst-appeals, income-tax-appeals-tribunals
      -> the new site already has deeper dedicated pages for these
  pasara-security-license, pf-fund-appeals, mining-project-reports
      -> empty on the live site ("No data...", "Coming soon.")
  training, about
      -> theme placeholder text (lorem ipsum), never real content
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nc_shell as S

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SNAP = os.path.join(HERE, "wp_snapshot")

GROUPS = [
    ("audit", "Audit &amp; assurance", "shield"),
    ("reg", "Registrations &amp; licences", "award"),
    # The loans explainer sits with compliance: a group of one left a lone card
    # hanging on its own row.
    ("comp", "Compliance, appeals &amp; finance", "scale"),
]

# slug, group, short name, <title>, meta description, card blurb
PAGES = [
    # Every description below says only what the page itself covers.
    ("statutory-audit", "audit", "Statutory Audit",
     "Statutory Audit in Bhopal | Natasha & Company, CA",
     "Statutory audit in Bhopal: audit planning, internal control review, substantive "
     "testing and the auditor's report, by an ISO 9001:2015 certified Chartered "
     "Accountancy firm.",
     "Planning, control testing and the auditor&rsquo;s report."),
    ("financial-statement-audit", "audit", "Financial Statement Audit",
     "Financial Statement Audit in Bhopal | Natasha & Company",
     "Independent audit of financial statements for businesses in Bhopal: risk assessment, "
     "internal controls, substantive procedures and a clear audit opinion from Natasha & "
     "Company, Chartered Accountants.",
     "An independent opinion on whether your accounts are true and fair."),
    ("bank-audit", "audit", "Bank Audit",
     "Bank Audit Services in Bhopal | Natasha & Company, CA",
     "Bank audit by Chartered Accountants in Bhopal: regulatory compliance, risk "
     "assessment, asset quality review, liquidity and capital adequacy, internal controls "
     "and communication with regulators.",
     "Asset quality, capital adequacy and regulatory compliance for banks."),
    ("concurrent-audit", "audit", "Concurrent Audit",
     "Concurrent Audit in Bhopal | Natasha & Company, CA",
     "Concurrent audit for banks and businesses in Bhopal: transactions examined as they "
     "happen, so errors, irregularities and control gaps are caught early rather than at "
     "year end.",
     "Transactions checked as they happen, not months later."),
    ("stock-audit", "audit", "Stock Audit",
     "Stock Audit in Bhopal | Natasha & Company, CA",
     "Stock audit in Bhopal: physical verification, inventory valuation, documentation "
     "review, cut-off procedures and assessment of internal controls over inventory.",
     "Physical verification, valuation and cut-off checks on inventory."),
    ("trade-mark", "reg", "Trademark Registration",
     "Trademark Registration in Bhopal | Natasha & Company",
     "Trademark registration in Bhopal: search, class selection, filing, examination "
     "replies and opposition support, so your brand name and logo are protected.",
     "Search, filing and objection replies to protect your brand."),
    ("iso-certification", "reg", "ISO Certification",
     "ISO Certification Consultants in Bhopal | Natasha & Co.",
     "ISO certification support in Bhopal: gap analysis, documentation, implementation and "
     "audit readiness, from a firm that is ISO 9001:2015 certified itself.",
     "Gap analysis, documentation and audit readiness, from a certified firm."),
    ("food-license-fssai", "reg", "FSSAI Food Licence",
     "FSSAI Food Licence Registration in Bhopal | Natasha & Co.",
     "FSSAI registration and food licence in Bhopal: choosing Basic, State or Central, "
     "documents, online application, fees, validity and renewal, for food businesses "
     "including home kitchens.",
     "Basic, State or Central FSSAI licence, applied for and renewed."),
    ("import-export-consultancy-iec-code", "reg", "IEC Code (Import &amp; Export)",
     "IEC Code Registration in Bhopal | Natasha & Company",
     "Importer Exporter Code (IEC) registration with DGFT and import-export consultancy in "
     "Bhopal, for traders starting or growing cross-border business.",
     "DGFT registration and import-export consultancy."),
    ("trade-license", "reg", "Trade Licence",
     "Trade Licence Registration in Bhopal | Natasha & Company",
     "Trade licence in Bhopal: documents required, application submission, inspection "
     "coordination and renewals, so your business is authorised to operate.",
     "Authorisation to operate, applied for and renewed."),
    ("railway-tender-registration", "reg", "Railway Tender Registration",
     "Railway Tender Registration in Bhopal | Natasha & Company",
     "Railway tender registration in Bhopal: vendor registration with railway authorities, "
     "documents required, and bidding assistance for businesses seeking railway contracts.",
     "Vendor registration and bidding assistance for railway tenders."),
    ("professional-tax-ptrc-ptec", "comp", "Professional Tax (PTRC / PTEC)",
     "Professional Tax PTRC & PTEC Registration | Natasha & Co.",
     "Professional tax enrolment (PTEC) and registration (PTRC): who needs each, documents "
     "required, application process, validity and renewal.",
     "PTEC and PTRC: who needs them, documents and renewal."),
    ("labour-law-compliances", "comp", "Labour Law Compliances",
     "Labour Law Compliance Services in Bhopal | Natasha & Co.",
     "Labour law compliance for employers in Bhopal: minimum wages, payment of wages, EPF, "
     "ESI, bonus, gratuity and standing orders obligations, explained in one place.",
     "Wages, EPF, ESI, bonus and gratuity obligations for employers."),
    ("esic-appeals", "comp", "ESIC Appeals",
     "ESIC Appeals in Bhopal | Natasha & Company, CA",
     "ESIC appeals in Bhopal: case assessment, documentation and filing before the ESIC "
     "appellate authority, with follow-up aimed at reducing disputed liabilities and "
     "penalties.",
     "Case assessment, documentation and appeal filing."),
    ("secured-loan-unsecured-loan", "comp", "Secured vs Unsecured Loans",
     "Secured vs Unsecured Loans Explained | Natasha & Company",
     "Secured and unsecured loans compared: collateral, interest rates, risk and common "
     "examples, explained by Natasha & Company, Chartered Accountants, Bhopal.",
     "Collateral, interest rates and risk, compared."),
]

WP_FAQS = {
    "statutory-audit": [
        ("Who is required to undergo a statutory audit in India?", "Under the Companies Act, 2013, all private limited and public limited companies registered in India must have their accounts audited annually by an independent Chartered Accountant, regardless of their turnover or profit."),
        ("What documents are required for a statutory audit?", "Key documents include general ledgers, trial balance, bank statements, bank confirmations, statutory registers, board minutes, fixed asset registers, tax returns, and prior year audited financials."),
        ("What is the timeline for completing a statutory audit?", "Statutory audits must be completed before the company's Annual General Meeting (AGM), which typically must take place within 6 months of the close of the financial year (by 30th September).")
    ],
    "financial-statement-audit": [
        ("What is the purpose of an independent financial statement audit?", "An independent financial statement audit provides external assurance to banks, investors, regulators, and management that financial statements present a true and fair view in accordance with applicable accounting standards."),
        ("How does a financial statement audit differ from an internal audit?", "An internal audit is an operational review conducted for management's internal control improvement, whereas a financial statement audit is an external, independent verification of statutory financial statements for external stakeholders."),
        ("How often should financial statements be audited?", "Financial statements are typically audited annually at financial year-end, although mid-year or quarterly reviews may be requested by lenders, prospective investors, or boards of directors.")
    ],
    "bank-audit": [
        ("What is involved in a bank branch statutory audit?", "Chartered Accountants verify advances, loan classifications (NPA identification and provisioning), compliance with RBI prudential norms, revenue leakage, cash verification, and adherence to KYC/AML guidelines."),
        ("Who appoints statutory auditors for bank branches?", "Statutory branch auditors (SBAs) are selected from the RBI and ICAI approved panels and appointed by the respective bank's Board of Directors or Audit Committee in consultation with RBI."),
        ("What is an LFAR (Long Form Audit Report)?", "The LFAR is an exhaustive questionnaire mandated by the Reserve Bank of India covering internal controls, credit appraisal, documentation, loan monitoring, liquidity, and operational compliance at the branch level.")
    ],
    "concurrent-audit": [
        ("What is the objective of a concurrent audit?", "A concurrent audit examines transactions concurrently or as close to the time of transaction as possible to identify irregularities, deviations from policy, and compliance gaps in real time rather than post-mortem."),
        ("Which entities typically require concurrent audits?", "Banks, financial institutions, NBFCs, and large trading houses commonly mandate concurrent audits for high-volume transactions, forex operations, treasury, and large loan disbursements."),
        ("How frequently are concurrent audit reports submitted?", "Concurrent audit reports are typically submitted monthly or quarterly to the audit committee or controlling authority with action-taken tracking on past irregularities.")
    ],
    "stock-audit": [
        ("Why do banks mandate a stock audit for borrowers?", "Banks require periodic stock and receivable audits for borrowers enjoying cash credit (CC) or working capital facilities to verify security hypothecated, ensure realistic drawing power calculation, and assess collateral safety."),
        ("What is verified during a physical stock audit?", "Auditors conduct physical count verification, verify stock condition (obsolete/slow-moving goods), inspect storage facilities, check insurance adequacy, and cross-verify with purchase invoices and stock registers."),
        ("What is drawing power (DP) in a stock audit?", "Drawing power is the maximum borrowing limit calculated against eligible paid-up stock and book debts after deducting stipulated bank margins, unpaid creditors, and statutory liabilities.")
    ],
    "trade-mark": [
        ("Why should a business register a trademark in India?", "Trademark registration confers exclusive legal ownership over brand names, logos, or taglines under the Trade Marks Act, 1999, preventing counterfeiters and competitors from misleading customers."),
        ("How long does trademark registration take and what is its validity?", "Trademark registration typically takes 6 to 12 months if there are no objections. Once registered, a trademark is valid for 10 years and can be renewed indefinitely every 10 years."),
        ("What is the difference between TM and R symbols?", "The TM symbol can be used as soon as a trademark application is filed, indicating claim of ownership. The (R) symbol can only be legally displayed once the trademark is officially registered by the Trademark Registry.")
    ],
    "iso-certification": [
        ("What is ISO 9001:2015 certification?", "ISO 9001:2015 is the international benchmark for Quality Management Systems (QMS), demonstrating an organization's ability to consistently deliver products and services that satisfy customer and regulatory requirements."),
        ("What is the step-by-step process for getting ISO certified?", "The process involves gap analysis, process documentation, staff training, implementation of standard operating procedures, internal audit, management review, and the external certification audit."),
        ("How does Natasha & Company assist with ISO certification?", "As an ISO 9001:2015 certified CA firm ourselves, we provide complete advisory including readiness assessments, documentation templates, internal audits, and liaising with accredited certification bodies.")
    ],
    "food-license-fssai": [
        ("Who requires an FSSAI registration or license in India?", "Any food business operator (FBO) involved in manufacturing, processing, packaging, distributing, transporting, catering, or retailing food items—including cloud kitchens and restaurants—must hold an FSSAI registration or license."),
        ("What is the difference between FSSAI Basic, State, and Central licenses?", "Basic Registration is for micro-enterprises with annual turnover up to ₹12 Lakhs; State License applies to turnover between ₹12 Lakhs and ₹20 Crores; Central License is mandatory for turnover exceeding ₹20 Crores, multi-state operations, or import/export."),
        ("What is the validity period of an FSSAI license?", "An FSSAI license can be issued for 1 to 5 years depending on the applicant's preference and fee paid, and must be renewed at least 30 days before expiry to avoid penalties.")
    ],
    "import-export-consultancy-iec-code": [
        ("What is an Importer Exporter Code (IEC)?", "An IEC is a mandatory 10-digit code issued by the Directorate General of Foreign Trade (DGFT) required for importing into or exporting commercial goods and specified services from India."),
        ("Is annual IEC update mandatory?", "Yes. DGFT mandates that every IEC holder must confirm or update their details electronically on the DGFT portal between April and June every year, even if there are no changes, to keep the IEC active."),
        ("Does an IEC code expire?", "No, an IEC code has lifetime validity once issued, subject to mandatory annual electronic validation on the DGFT portal.")
    ],
    "trade-license": [
        ("What is a Trade License and who issues it in Bhopal?", "A Trade License is an official municipal permission issued by the Bhopal Municipal Corporation (BMC) permitting an entity to conduct specific commercial activities without health hazards."),
        ("What documents are required to obtain a trade license in Bhopal?", "Documents include property tax receipts or rent agreement, electricity bill, applicant PAN and Aadhaar, establishment photos, fire NOC (if applicable), and business incorporation documents."),
        ("When must a Trade License be renewed?", "Trade licenses are generally renewed annually before the beginning of the financial year (typically by 31st March or April) with the local municipal authority.")
    ],
    "railway-tender-registration": [
        ("What is IREPS and vendor registration for railway tenders?", "IREPS (Indian Railways E-Procurement System) is the official portal for Indian Railways tenders. Businesses must obtain digital signature certificates, vendor registration, and technical credential approvals to participate in bids."),
        ("What financial documents do railways require for tender qualification?", "Railways require CA-certified net worth certificates, annual audited balance sheets, working capital certificates, turnover certificates, and solvency certificates."),
        ("How can a CA assist with railway tender bids?", "Chartered Accountants provide bid capacity calculations, prepare CMA and financial compliance documents, verify earnest money deposit (EMD) exemptions (MSME), and audit financial ratios.")
    ],
    "professional-tax-ptrc-ptec": [
        ("What is the difference between PTRC and PTEC in Madhya Pradesh?", "PTEC (Professional Tax Enrolment Certificate) is paid by business entities, proprietors, and professionals on their own trade. PTRC (Professional Tax Registration Certificate) is obtained by employers to deduct and remit professional tax from employee salaries."),
        ("What are the due dates for professional tax payment and returns in MP?", "PTEC is paid annually (usually by 30th April), whereas PTRC returns and tax payments are made monthly or quarterly depending on the employer's liability under the MP Commercial Tax Department."),
        ("What are the penalties for non-registration of Professional Tax?", "Failure to register or late payment attracts interest and statutory penalties under the Madhya Pradesh Professional Tax Act.")
    ],
    "labour-law-compliances": [
        ("Which key labour laws apply to private businesses in Bhopal?", "Applicable laws include the EPF Act, ESI Act, Payment of Gratuity Act, Minimum Wages Act, Payment of Wages Act, MP Industrial Employment Standing Orders, and the Maternity Benefit Act."),
        ("When is EPF and ESIC registration mandatory for employers?", "EPF is mandatory for establishments employing 20 or more employees (voluntary below 20). ESIC is mandatory for entities with 10 or more employees earning up to ₹21,000 per month."),
        ("What happens during a labour law audit?", "A labour audit reviews statutory wage registers, attendance records, overtime logs, remittance challans for PF/ESI, annual return filings, and workplace safety compliance.")
    ],
    "esic-appeals": [
        ("Under what sections can an employer appeal an ESIC demand?", "Employers can dispute arbitrary determination orders under Section 45A by filing an appeal under Section 45AA before the ESIC Appellate Authority or approaching the Employees' Insurance Court (EI Court) under Section 75."),
        ("What is the limitation period for filing an ESIC appeal?", "An appeal under Section 45AA must generally be filed within 60 days of the receipt of the determination order, accompanied by proof of deposit of 25% of the disputed contribution."),
        ("Can penalties and damages under Section 85B be waived in an appeal?", "Yes, where the employer demonstrates reasonable cause, bona fide financial distress, or factual errors in employee headcounts, the appellate authority or court can grant substantial waiver.")
    ],
    "secured-loan-unsecured-loan": [
        ("What is the main distinction between secured and unsecured loans?", "Secured loans require pledging collateral (such as property, equipment, or fixed deposits) and offer lower interest rates and higher amounts. Unsecured loans require no collateral but carry higher interest rates."),
        ("What financial documentation do banks require for business loan sanction?", "Banks require 3 years of audited financials, computation of income, ITR acknowledgements, GST returns, 6-12 months bank statements, and a CA-certified CMA (Credit Monitoring Arrangement) report."),
        ("Why is a CA-prepared CMA report critical for loan approval?", "A CMA report projects financial performance, debt service coverage ratio (DSCR), current ratio, and funds flow, allowing credit managers to assess borrower repayment capacity.")
    ],
}


# ------------------------------------------------------------------ cleanup
def _dedupe_heading(t):
    """'Pay the Application Fee​Pay the Application Fee' -> one copy."""
    t = t.replace("​", "").strip()
    half = len(t) // 2
    if len(t) % 2 == 0 and t[:half] == t[half:]:
        return t[:half]
    return t


def _esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


LIST_HEADINGS = re.compile(r"prerequisite|documents? required|deliverable|eligib", re.I)


def render(blocks):
    """Snapshot blocks -> (lead, prose html)."""
    # Elementor accordion answers end in " ." after a stripped icon.
    blocks = [[k, re.sub(r"\s+\.$", "", _dedupe_heading(t)).rstrip()] for k, t in blocks]
    blocks = [[k, t if t.endswith((".", ":", "?", "!")) or k != "p" or len(t) < 60 else t + "."]
              for k, t in blocks]

    # The title is the page H1 (phero); drop it from the body.
    if blocks and blocks[0][0] in ("h1", "h2"):
        blocks = blocks[1:]

    # Remove a paragraph that is an exact copy of the next paragraph two
    # blocks on (Elementor step cards where one body was pasted twice).
    clean = []
    for i, (k, t) in enumerate(blocks):
        if k == "p":
            later = [b for b in blocks[i + 1:i + 4] if b[0] == "p"]
            if later and later[0][1] == t:
                continue
        clean.append([k, t])
    blocks = clean

    lead = ""
    out, ul, in_list_section, in_faq = [], [], False, False

    def flush():
        if ul:
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % _esc(x) for x in ul))
            ul.clear()

    for k, t in blocks:
        label = t.rstrip(":").strip()
        if k == "p" and label.lower() == "overview":
            continue                                    # a label, not content
        if not lead and k == "p" and len(t.split()) > 12:
            lead = t
            continue

        if label.lower() in ("f.a.q.", "faq", "frequently asked questions"):
            if not in_faq:
                flush()
                out.append("<h2>Frequently asked questions</h2>")
                in_faq = True
            continue

        starts_list = bool(LIST_HEADINGS.search(label)) and k.startswith("h")
        if starts_list or (k in ("h2", "h3") and not (in_list_section and k == "h3")):
            flush()
            in_list_section = bool(LIST_HEADINGS.search(label))
            out.append("<h2>%s</h2>" % _esc(label))
            continue

        if k in ("h4", "h5", "h6", "h3"):
            if in_list_section:
                ul.append(label)                         # deliverables as a list
            else:
                flush()
                out.append("<h3>%s</h3>" % _esc(label))
            continue

        if k == "li" or (k == "p" and in_list_section and len(t) < 140):
            ul.append(t)
            continue

        flush()
        out.append("<p>%s</p>" % _esc(t))
    flush()
    return lead, "\n".join(out)


# ------------------------------------------------------------------ page
def build(entry):
    slug, group, short, title, desc, blurb = entry
    data = json.load(io.open(os.path.join(SNAP, slug + ".json"), encoding="utf-8"))
    lead, prose = render(data["blocks"])
    prose = S.close_heading_gaps(prose)
    # Keep the hero to two sentences; the rest of a long intro opens the body.
    sentences = re.split(r"(?<=[.!?])\s+", lead)
    if len(lead.split()) > 45 and len(sentences) > 2:
        lead = " ".join(sentences[:2])
        prose = "<p>%s</p>\n%s" % (_esc(" ".join(sentences[2:])), prose)
    h1 = _esc(data["title"]).replace("( ", "(").strip()
    if slug == "trade-mark":
        h1 = "Trademark Registration"
    # An explainer, not a local service: "in Bhopal" would promise one.
    h1_full = short if slug == "secured-loan-unsecured-loan" else "%s in Bhopal" % h1

    gname = dict((g, n) for g, n, _ in GROUPS)[group]
    icon = dict((g, i) for g, _, i in GROUPS)[group]
    siblings = "".join('<a href="%s.html">%s</a>' % (p[0], p[2])
                       for p in PAGES if p[1] == group and p[0] != slug)

    faqs = WP_FAQS.get(slug, [])
    if faqs and "<h2>Frequently asked questions</h2>" not in prose:
        faq_markup = "\n\n<h2>Frequently asked questions</h2>\n" + "\n".join(
            "<h3>%s</h3>\n<p>%s</p>" % (_esc(q), _esc(a)) for q, a in faqs)
        prose += faq_markup

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
          <span class="nc-svc-ico">{icon}</span>
          <h2 class="nc-h4" style="font-size:1.05rem">Speak to CA Natasha</h2>
          <p style="font-size:.92rem;color:var(--nc-ink-3)">
            Send your documents, get a written position and a fixed fee before any work starts.
          </p>
          <div class="nc-stack" style="gap:.6rem;margin-top:1.15rem">
            <a class="nc-btn nc-btn-full nc-btn-sm" href="{book}" data-open-modal="ncConsultModal">Book a consultation</a>
            <a class="nc-btn nc-btn-ghost nc-btn-full nc-btn-sm" href="#quick-enquiry" data-open-modal="ncConsultModal">Send Quick Enquiry</a>
            <a class="nc-btn nc-btn-ghost nc-btn-full nc-btn-sm" href="tel:{phone}">{phone_d}</a>
          </div>
        </div>

        <div class="nc-card">
          <h2 class="nc-h4" style="font-size:1.05rem">{gname}</h2>
          <div class="nc-ftr-links" style="margin-top:.85rem">
            {siblings}
            <a href="services.html#more">All services</a>
          </div>
        </div>
      </aside>

    </div>
  </div>
</section>

{cta}""".format(
        phero=S.phero(h1_full, _esc(lead) or blurb,
                      [("Home", "index.html"), ("Services", "services.html"), (short, slug + ".html")]),
        prose=prose, icon=S.ico(icon), phone=S.PHONE, phone_d=S.PHONE_DISPLAY,
        book=S.BOOK_URL, gname=gname, siblings=siblings, cta=S.cta_band())

    plain = lambda s: s.replace("&amp;", "&").replace('"', "'")
    svc_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Service",
        "@id": "%s/%s.html#service" % (S.SITE, slug),
        "name": plain(h1),
        "serviceType": plain(short),
        "description": plain(desc),
        "url": "%s/%s.html" % (S.SITE, slug),
        "provider": {"@id": S.ORG_ID},
        "areaServed": [{"@type": "City", "name": "Bhopal"},
                       {"@type": "State", "name": "Madhya Pradesh"}],
    }, indent=2, ensure_ascii=False)

    faq_ld = S.faq_schema(faqs) if faqs else ""

    doc = S.page(
        title=title, desc=desc, slug=slug + ".html", body=body,
        keywords="%s Bhopal, %s, CA Bhopal, Chartered Accountant Bhopal"
                 % (plain(short), plain(h1)),
        schema=S.ld(svc_ld, faq_ld, S.org_schema(),
                    S.crumbs_schema([("Home", "index.html"), ("Services", "services.html"),
                                     (plain(short), slug + ".html")])))
    with io.open(os.path.join(ROOT, slug + ".html"), "w", encoding="utf-8") as f:
        f.write(doc)
    words = len(re.sub(r"<[^>]+>", " ", prose).split()) + len(lead.split())
    print("  built %-44s %4d words" % (slug + ".html", words))


def more_services_section():
    """Grouped cards for services.html, so every carried-forward page is linked."""
    cols = []
    for g, gname, icon in GROUPS:
        items = [p for p in PAGES if p[1] == g]
        links = "".join("""<li><a href="%s.html"><b>%s</b><span>%s</span></a></li>"""
                        % (p[0], p[2], p[5]) for p in items)
        cols.append("""<article class="nc-card nc-card-i nc-card-glow nc-svc nc-more" data-nc-rise>
  <span class="nc-svc-ico">%s</span>
  <h3>%s</h3>
  <ul class="nc-more-list">%s</ul>
</article>""" % (S.ico(icon), gname, links))
    return """<section class="nc-sec nc-sec-alt" id="more">
  <div class="nc-wrap">
    <div class="nc-center">%s</div>
    <div class="nc-grid nc-g3 nc-more-grid">%s</div>
  </div>
</section>""" % (S.sec_head(
        "More services",
        "Specialised audits, registrations and compliance",
        "Each of these has its own page with the scope, process and documents involved.",
        center=True), "".join(cols))


def main():
    for p in PAGES:
        build(p)


if __name__ == "__main__":
    main()
