# -*- coding: utf-8 -*-
"""
Knowledge Bank: a two-level reference menu of statutory resources.

Categories on the left, links on the right — the pattern CA firm sites use for
this material. Every external link points at the official government source, so
the firm is not restating law it would then have to maintain.
"""

# (category, [(label, url), ...])
BANK = [
    ("Quick Links", [
        ("PAN Services (Protean)", "https://www.protean-tinpan.com/services/pan/pan-index.html"),
        ("TAN Services", "https://www.protean-tinpan.com/services/tan/tan-index.html"),
        ("e-Pay Tax", "https://www.incometax.gov.in/iec/foportal/help/e-pay-tax"),
        ("Income Tax e-Filing", "https://www.incometax.gov.in/iec/foportal/"),
        ("GST Portal", "https://www.gst.gov.in/"),
        ("MCA21", "https://www.mca.gov.in/"),
        ("TRACES (TDS)", "https://www.tdscpc.gov.in/"),
        ("EPFO", "https://www.epfindia.gov.in/"),
        ("ESIC", "https://www.esic.gov.in/"),
        ("ICAI", "https://www.icai.org/"),
    ]),
    ("Acts", [
        ("Income-tax Act, 1961", "https://incometaxindia.gov.in/pages/acts/income-tax-act.aspx"),
        ("CGST Act, 2017", "https://cbic-gst.gov.in/CGST-bill-e.html"),
        ("IGST Act, 2017", "https://cbic-gst.gov.in/igst-bill-e.html"),
        ("Companies Act, 2013", "https://www.mca.gov.in/content/mca/global/en/acts-rules/ebooks/acts.html"),
        ("LLP Act, 2008", "https://www.mca.gov.in/content/mca/global/en/acts-rules/ebooks/acts.html"),
        ("Customs Act, 1962", "https://www.cbic.gov.in/entities/customs-acts"),
        ("Chartered Accountants Act, 1949", "https://www.icai.org/post/the-chartered-accountants-act-1949"),
    ]),
    ("Rules", [
        ("Income-tax Rules, 1962", "https://incometaxindia.gov.in/Pages/rules/income-tax-rules-1962.aspx"),
        ("CGST Rules, 2017", "https://cbic-gst.gov.in/cgst-rules.html"),
        ("Companies Rules", "https://www.mca.gov.in/content/mca/global/en/acts-rules/ebooks/rules.html"),
        ("LLP Rules, 2009", "https://www.mca.gov.in/content/mca/global/en/acts-rules/ebooks/rules.html"),
    ]),
    ("Circulars &amp; Notifications", [
        ("CBDT Circulars", "https://incometaxindia.gov.in/Pages/communications/circulars.aspx"),
        ("CBDT Notifications", "https://incometaxindia.gov.in/Pages/communications/notifications.aspx"),
        ("GST Circulars", "https://cbic-gst.gov.in/cgst-circulars.html"),
        ("GST Notifications", "https://cbic-gst.gov.in/central-tax-notification.html"),
        ("MCA Circulars", "https://www.mca.gov.in/content/mca/global/en/notifications-tender/circulars.html"),
    ]),
    ("Forms", [
        ("Income Tax forms", "https://incometaxindia.gov.in/Pages/downloads/income-tax-forms.aspx"),
        ("ITR forms", "https://www.incometax.gov.in/iec/foportal/downloads"),
        ("GST forms", "https://cbic-gst.gov.in/gst-forms.html"),
        ("ROC / MCA forms", "https://www.mca.gov.in/content/mca/global/en/mca/e-filing/company-forms-download.html"),
        ("TDS forms (24Q, 26Q, 27Q)", "https://www.tdscpc.gov.in/en/downloads.html"),
    ]),
    ("Calculators", [
        ("Income Tax Calculator", "income-tax-calculator.html"),
        ("HRA Exemption Calculator", "hra-exemption-calculator.html"),
        ("GST Calculator", "gst-calculator.html"),
        ("EMI Loan Calculator", "emi-loan-calculator.html"),
    ]),
    ("Rates &amp; Charts", [
        ("TDS rate chart, FY 2025-26", "knowledge-base.html#tds-rates"),
        ("Cost Inflation Index", "knowledge-base.html#cost-inflation-index"),
        ("Compliance due dates", "knowledge-base.html#due-dates"),
        ("Official portals", "knowledge-base.html#portals"),
    ]),
    ("Our Guides", [
        ("All insights", "blog.html"),
        ("Tax Audit u/s 44AB", "tax-audit-44ab-bhopal.html"),
        ("GST notice &amp; litigation", "gst-notice-consultant-bhopal.html"),
        ("Income tax notice defence", "income-tax-notice-consultant-bhopal.html"),
        ("NRI taxation", "nri-taxation-services-bhopal.html"),
    ]),
]


def mega_html():
    """Categories column plus a panel of links for each."""
    cats, panels = [], []
    for i, (name, links) in enumerate(BANK):
        cats.append(
            '<button class="nc-mega-cat%s" type="button" role="tab" '
            'aria-selected="%s" tabindex="%d" data-mega="%d">%s'
            '<svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
            'stroke-linecap="round" aria-hidden="true"><polyline points="9 18 15 12 9 6"/></svg>'
            '</button>'
            % (" is-on" if i == 0 else "", "true" if i == 0 else "false",
               0 if i == 0 else -1, i, name))

        rows = "".join(
            '<a href="%s"%s>%s</a>'
            % (url, ' target="_blank" rel="noopener"' if url.startswith("http") else "", label)
            for label, url in links)
        panels.append('<div class="nc-mega-panel%s" data-mega="%d" role="tabpanel"%s>%s</div>'
                      % (" is-on" if i == 0 else "", i,
                         "" if i == 0 else " hidden", rows))

    return ('<div class="nc-mega">'
            '<div class="nc-mega-cats" role="tablist" aria-label="Knowledge Bank sections">%s</div>'
            '<div class="nc-mega-panels">%s</div>'
            '</div>' % ("".join(cats), "".join(panels)))


def mobile_html():
    """Flat accordion for the drawer, where a flyout would be unusable."""
    out = []
    for name, links in BANK:
        rows = "".join(
            '<a href="%s"%s>%s</a>'
            % (url, ' target="_blank" rel="noopener"' if url.startswith("http") else "", label)
            for label, url in links)
        out.append('<button type="button" class="nc-msub-cat">%s</button>'
                   '<div class="nc-msub-links">%s</div>' % (name, rows))
    return "".join(out)
