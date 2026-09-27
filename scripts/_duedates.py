# -*- coding: utf-8 -*-
"""
Statutory compliance calendar, month by month.

Recurring items repeat every month and are rendered under each month. Dated
items are specific to that month of a standard financial year.

Deliberately written without a year: extensions are routine in India, and a
calendar that hard-codes "2019" (as the template this was modelled on does)
becomes misleading within months. The page says plainly that these are
indicative.
"""

# (day, label, detail, tag)
RECURRING = [
    ("07", "TDS / TCS deposit", "Tax deducted in the previous month, via Challan 281.", "Income Tax"),
    ("10", "GSTR-7 &amp; GSTR-8", "TDS under GST, and TCS collected by e-commerce operators.", "GST"),
    ("11", "GSTR-1", "Outward supplies for monthly filers.", "GST"),
    ("13", "GSTR-1 IFF &amp; GSTR-6", "Invoice Furnishing Facility under QRMP; ISD return.", "GST"),
    ("15", "EPF &amp; ESI contribution", "Electronic Challan cum Return for the previous month.", "Labour"),
    ("20", "GSTR-3B", "Summary return and tax payment for monthly filers.", "GST"),
    ("25", "PMT-06", "Monthly tax payment for taxpayers under the QRMP scheme.", "GST"),
]

MONTHS = [
    ("January", [
        ("15", "TCS return, Q3", "Form 27EQ for October to December.", "Income Tax"),
        ("31", "TDS return, Q3", "Forms 24Q and 26Q for October to December.", "Income Tax"),
    ]),
    ("February", [
        ("15", "TDS certificates, Q3", "Form 16A issued to deductees.", "Income Tax"),
    ]),
    ("March", [
        ("15", "Advance tax, 4th instalment", "100% of estimated liability, cumulative.", "Income Tax"),
        ("31", "Financial year ends", "Last date for tax-saving investments and for filing an updated return for the relevant year.", "Income Tax"),
    ]),
    ("April", [
        ("30", "MSME-1 half-yearly", "Outstanding dues to micro and small enterprises, October to March.", "ROC"),
        ("30", "TDS deposit, March", "March deduction is due 30 April, not the usual 7th.", "Income Tax"),
    ]),
    ("May", [
        ("15", "TCS return, Q4", "Form 27EQ for January to March.", "Income Tax"),
        ("30", "LLP Form 11", "Annual return of an LLP for the year ended 31 March.", "ROC"),
        ("30", "PAS-6 half-yearly", "Reconciliation of share capital audit report.", "ROC"),
        ("31", "TDS return, Q4", "Forms 24Q and 26Q for January to March.", "Income Tax"),
    ]),
    ("June", [
        ("15", "Advance tax, 1st instalment", "15% of estimated liability.", "Income Tax"),
        ("15", "Form 16", "Salary TDS certificate issued to employees.", "Income Tax"),
    ]),
    ("July", [
        ("15", "TCS return, Q1", "Form 27EQ for April to June.", "Income Tax"),
        ("31", "TDS return, Q1", "Forms 24Q and 26Q for April to June.", "Income Tax"),
        ("31", "ITR filing, non-audit cases", "Individuals and businesses not subject to audit.", "Income Tax"),
    ]),
    ("August", [
        ("15", "TDS certificates, Q1", "Form 16A issued to deductees.", "Income Tax"),
    ]),
    ("September", [
        ("15", "Advance tax, 2nd instalment", "45% of estimated liability, cumulative.", "Income Tax"),
        ("30", "Tax audit report", "Forms 3CA or 3CB with 3CD, under Section 44AB.", "Income Tax"),
        ("30", "DIR-3 KYC", "Annual KYC for every person holding a DIN.", "ROC"),
        ("30", "AGM, most companies", "Annual General Meeting for the year ended 31 March.", "ROC"),
    ]),
    ("October", [
        ("15", "TCS return, Q2", "Form 27EQ for July to September.", "Income Tax"),
        ("30", "AOC-4", "Financial statements, within 30 days of the AGM.", "ROC"),
        ("30", "LLP Form 8", "Statement of account and solvency.", "ROC"),
        ("31", "TDS return, Q2", "Forms 24Q and 26Q for July to September.", "Income Tax"),
        ("31", "ITR filing, audit cases", "Where audit under Section 44AB applies.", "Income Tax"),
        ("31", "MSME-1 half-yearly", "Outstanding dues to micro and small enterprises, April to September.", "ROC"),
    ]),
    ("November", [
        ("15", "TDS certificates, Q2", "Form 16A issued to deductees.", "Income Tax"),
        ("29", "MGT-7 / MGT-7A", "Annual return, within 60 days of the AGM.", "ROC"),
        ("29", "PAS-6 half-yearly", "Reconciliation of share capital audit report.", "ROC"),
        ("30", "Transfer pricing report", "Form 3CEB and the related ITR, where international or specified domestic transactions apply.", "Income Tax"),
    ]),
    ("December", [
        ("15", "Advance tax, 3rd instalment", "75% of estimated liability, cumulative.", "Income Tax"),
        ("31", "GSTR-9 &amp; GSTR-9C", "Annual return and reconciliation statement for the previous financial year.", "GST"),
        ("31", "Belated / revised ITR", "Last date to file a belated or revised return for the assessment year.", "Income Tax"),
    ]),
]

# Official portals a CA firm's clients actually need.
PORTALS = [
    ("Income Tax e-Filing", "File returns, respond to notices, track refunds",
     "https://www.incometax.gov.in/iec/foportal/"),
    ("GST Portal", "Returns, registration, e-way bills, DRC replies",
     "https://www.gst.gov.in/"),
    ("MCA21", "Company and LLP filings, DIN, name reservation",
     "https://www.mca.gov.in/"),
    ("TRACES", "Form 16/16A, TDS statements, justification reports",
     "https://www.tdscpc.gov.in/"),
    ("EPFO", "Provident fund ECR, UAN, employer services",
     "https://www.epfindia.gov.in/"),
    ("ESIC", "Employee state insurance contributions and returns",
     "https://www.esic.gov.in/"),
    ("ICAI", "The Institute of Chartered Accountants of India",
     "https://www.icai.org/"),
    ("CBIC", "Central Board of Indirect Taxes and Customs",
     "https://www.cbic.gov.in/"),
]
