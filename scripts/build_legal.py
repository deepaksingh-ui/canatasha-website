# -*- coding: utf-8 -*-
"""
Privacy Policy and Terms & Conditions.

The originals ran to three short paragraphs each, which is thin for a firm
handling PAN, Aadhaar and banking data. These are expanded to cover the
Digital Personal Data Protection Act 2023, the Chartered Accountants Act 1949
and the ICAI Code of Ethics.

NOTE FOR THE FIRM: this is drafted as a solid starting point, not as vetted
legal advice on your specific processes. Have it reviewed before relying on it,
and confirm the retention periods and grievance-officer details match reality.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nc_shell as S

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPDATED = "5 September 2026"


def legal_page(slug, title, desc, short, lead, sections, ld_type="WebPage"):
    prose = []
    for h, paras in sections:
        prose.append("<h2>%s</h2>" % h)
        for p in paras:
            prose.append(p if p.lstrip().startswith("<") else "<p>%s</p>" % p)

    body = """{phero}

<section class="nc-sec">
  <div class="nc-wrap">
    <div class="nc-article">
      <article>
        <div class="nc-note" style="margin-top:0">
          <b>Last updated</b>
          <p>{updated} &middot; Applies to canatasha.com and to engagements with {name}.</p>
        </div>
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
          <h2 class="nc-h4" style="font-size:1.05rem">Questions about this policy?</h2>
          <p style="font-size:.92rem;color:var(--nc-ink-3)">
            Write to our compliance contact and we will respond within the statutory period.
          </p>
          <div class="nc-stack" style="gap:.6rem;margin-top:1.15rem">
            <a class="nc-btn nc-btn-full nc-btn-sm" href="mailto:{email}">{email}</a>
            <a class="nc-btn nc-btn-ghost nc-btn-full nc-btn-sm" href="tel:{phone}">{phone_d}</a>
          </div>
        </div>
      </aside>
    </div>
  </div>
</section>""".format(
        phero=S.phero(short, lead, [("Home", "index.html"), (short, None)]),
        updated=UPDATED, name=S.NAME, prose="\n".join(prose),
        email=S.EMAIL, phone=S.PHONE, phone_d=S.PHONE_DISPLAY)

    page_ld = """{
  "@context": "https://schema.org",
  "@type": "%s",
  "@id": "%s/%s#page",
  "name": "%s",
  "url": "%s/%s",
  "dateModified": "2026-09-05",
  "inLanguage": "en-IN",
  "publisher": {"@id": "%s"},
  "about": {"@id": "%s"}
}""" % (ld_type, S.SITE, slug, short, S.SITE, slug, S.ORG_ID, S.ORG_ID)

    doc = S.page(
        title=title, desc=desc, slug=slug, body=body,
        schema=S.ld(page_ld, S.org_schema(),
                    S.crumbs_schema([("Home", "index.html"), (short, slug)])))

    with io.open(os.path.join(ROOT, slug), "w", encoding="utf-8") as f:
        f.write(doc)
    print("  built %-30s %3d KB" % (slug, len(doc) // 1024))


def privacy():
    sections = [
        ("Who we are", [
            "%s is a Chartered Accountancy firm registered with the Institute of Chartered "
            "Accountants of India, practising from 195-A, Zone-1, M.P. Nagar, Bhopal 462011, "
            "Madhya Pradesh. In the language of the Digital Personal Data Protection Act 2023, "
            "we act as a <strong>Data Fiduciary</strong> for the personal data described below."
            % S.NAME,
            "Questions about this policy, or any request to exercise your rights under it, "
            'should go to <a href="mailto:%s">%s</a> or +91 94070 00157.' % (S.EMAIL, S.EMAIL),
        ]),
        ("What we collect", [
            "The data we hold falls into three groups, and they are treated differently.",
            "<h3>Engagement data</h3>",
            "Where you become a client, we necessarily handle books of account, PAN and Aadhaar "
            "details, GSTIN, bank statements, investment and loan records, salary particulars, "
            "property documents and prior filings. This is the material without which audit, "
            "return preparation or notice representation cannot be performed.",
            "<h3>Enquiry data</h3>",
            "When you use the contact form, WhatsApp or email, we receive your name, phone "
            "number, email address and whatever you choose to describe about your situation, "
            "including any notice you send us.",
            "<h3>Website data</h3>",
            "Our calculators run entirely in your browser: the figures you type are not "
            "transmitted to us unless you separately submit them through a form. Standard "
            "server logs record IP address, browser type and pages requested, which we use "
            "for security and aggregate traffic analysis only.",
        ]),
        ("Why we hold it, and on what basis", [
            "Engagement data is processed to perform the professional services you have "
            "engaged us for, and to meet obligations imposed on us by the Income-tax Act 1961, "
            "the CGST Act 2017, the Companies Act 2013 and the Chartered Accountants Act 1949. "
            "Enquiry data is processed on the basis of your consent, given when you contact us, "
            "and is used to respond to that enquiry.",
            "We do not sell personal data. We do not use client data to train machine learning "
            "systems. We do not share client lists with third parties for marketing.",
        ]),
        ("Professional confidentiality", [
            "Beyond data protection law, we are bound by the confidentiality obligations of the "
            "Chartered Accountants Act 1949 and the ICAI Code of Ethics. Client information is "
            "not disclosed to any person without your authority, except where disclosure is "
            "compelled by law or by a competent authority &mdash; for example a summons, a "
            "court order, or a statutory notice we are obliged to answer.",
            "Where we are compelled to disclose, we will tell you unless we are legally "
            "prohibited from doing so.",
        ]),
        ("Who else sees your data", [
            "Statutory filings are submitted to the portals they are meant for: the Income Tax "
            "e-filing portal, the GST Network, the MCA21 portal, EPFO, ESIC and the relevant "
            "Madhya Pradesh departments. That transmission is the purpose of the engagement.",
            "Internally, access is limited to the partner and team members assigned to your "
            "file. Our practice management and accounting systems are operated under our "
            "ISO 9001:2015 documented process, with access logged.",
            "Where a matter requires counsel, a valuer or a specialist, we tell you before "
            "sharing anything and share only what that person needs.",
        ]),
        ("How long we keep it", [
            "Working papers, audit files and filed returns are retained for the periods "
            "required by the ICAI and by tax legislation &mdash; in practice, at least eight "
            "years from the end of the relevant assessment year, because reassessment and "
            "appellate proceedings can reach back that far.",
            "Enquiry data from people who do not become clients is retained for up to two "
            "years, and then deleted.",
        ]),
        ("Your rights", [
            "Under the Digital Personal Data Protection Act 2023 you may ask us for a summary "
            "of the personal data we hold about you and how it is being processed; ask us to "
            "correct or complete inaccurate data; ask us to erase data where we are not "
            "obliged to retain it; withdraw consent where processing rests on consent; and "
            "nominate someone to exercise these rights if you are unable to.",
            "Write to <a href=\"mailto:%s\">%s</a> and we will respond within the statutory "
            "period. If you are not satisfied with our response you may complain to the Data "
            "Protection Board of India." % (S.EMAIL, S.EMAIL),
            "One limit is worth stating plainly: we cannot erase records we are legally "
            "required to retain, such as audit working papers within their retention period.",
        ]),
        ("Security", [
            "We apply access controls, encrypted transmission for portal filings, and the "
            "documented handling procedures required by our ISO 9001:2015 certification. "
            "Physical files are held in the office premises with controlled access.",
            "No system is perfectly secure. If a breach affecting your personal data occurs, "
            "we will notify you and the Data Protection Board of India as the Act requires.",
            "<div class=\"nc-note\"><b>Please do not email credentials</b>"
            "<p>We will never ask for your income tax, GST or banking portal password by "
            "email, phone or WhatsApp. If you receive such a request purporting to come from "
            "us, it is not from us &mdash; call the office on +91 94070 00157 to verify.</p></div>",
        ]),
        ("Cookies and third-party content", [
            "This site does not set advertising or cross-site tracking cookies. Pages that "
            "embed a Google Map load content from Google, which may set its own cookies under "
            "Google's privacy policy. Web fonts are served by Google Fonts."
            + (" The booking page embeds a Calendly scheduling calendar. Calendly processes the "
               "name, email and notes you enter there in order to confirm your appointment, and "
               "may set its own cookies under Calendly's privacy policy." if S.CALENDLY_URL else ""),
            "You can block cookies in your browser without losing access to any function of "
            "this site, including the calculators.",
        ]),
        ("Changes to this policy", [
            "We update this policy when our practices or the law change. The date at the top "
            "of this page reflects the current version. Material changes affecting existing "
            "clients will be communicated directly.",
        ]),
    ]

    legal_page(
        "privacy-policy.html",
        "Privacy Policy | Natasha & Company, Chartered Accountants, Bhopal",
        "How Natasha & Company collects, uses, protects and retains your personal and "
        "financial data, under the Digital Personal Data Protection Act 2023, the Chartered "
        "Accountants Act 1949 and the ICAI Code of Ethics.",
        "Privacy Policy",
        "How we handle your personal and financial data &mdash; and the confidentiality "
        "obligations that bind us beyond what the law requires.",
        sections, ld_type="WebPage")


def terms():
    sections = [
        ("These terms", [
            "These terms govern your use of canatasha.com and set out the basis on which "
            "%s provides professional services. Using this website means you accept them. "
            "Where you engage us for work, a separate engagement letter will govern that "
            "work and will prevail over anything on this page if the two differ." % S.NAME,
        ]),
        ("What this website is, and is not", [
            "The articles, guides, calculators and reference material on this site are "
            "general information about Indian tax and corporate law. They are not advice on "
            "your situation, and reading them does not create a client relationship.",
            "Tax law changes frequently and often retrospectively. Content is written as at "
            "the date of publication and is not systematically updated afterwards. Thresholds, "
            "rates and due dates that were correct when written may not be correct when you "
            "read them.",
            "<div class=\"nc-note\"><b>Before you act on anything here</b>"
            "<p>Confirm the position for your own facts, either with us or with your existing "
            "adviser. We accept no liability for action taken on the strength of general "
            "website content alone.</p></div>",
        ]),
        ("The calculators", [
            "The income tax, HRA, GST and EMI calculators run in your browser and produce "
            "indicative figures from the inputs you supply. They apply standard slabs and "
            "formulae and cannot account for the full range of exemptions, deductions, "
            "set-offs, carried-forward losses, surcharge interactions, residential status "
            "questions or prior-year positions that determine an actual liability.",
            "They are a sanity check, not a computation you should file on. Nothing they "
            "display constitutes a professional opinion.",
        ]),
        ("Engaging us", [
            "A client relationship begins only when we have issued, and you have accepted, "
            "a written engagement letter setting out scope, deliverables, timelines and fees. "
            "An enquiry, a phone call, or correspondence about a possible engagement does not "
            "by itself create one.",
            "We reserve the right to decline an engagement, including where accepting it would "
            "create a conflict of interest, where independence requirements under the ICAI "
            "Code of Ethics would be compromised, or where the instructions we are given are "
            "ones we cannot professionally support.",
        ]),
        ("Your responsibilities as a client", [
            "The quality of professional work depends on the completeness and accuracy of what "
            "we are given. You are responsible for providing complete, accurate and timely "
            "records, disclosing all material facts including matters you may consider "
            "unfavourable, and reviewing and approving filings before submission.",
            "Where information is withheld or misstated, we are not responsible for the "
            "consequences of a filing or opinion based on it.",
        ]),
        ("Fees", [
            "Fees are quoted in writing before work begins and are based on the scope agreed. "
            "Where the scope changes materially &mdash; a notice escalates, a period is "
            "reopened, records turn out to be incomplete &mdash; we will tell you and agree a "
            "revised fee before continuing.",
            "Government fees, portal charges, stamp duty and out-of-pocket expenses are "
            "additional and charged at cost. Fees are exclusive of GST unless stated otherwise.",
        ]),
        ("Limitation of liability", [
            "Our liability in respect of any engagement is limited to the professional fees "
            "paid for that engagement, except where liability cannot lawfully be limited.",
            "We are not liable for indirect or consequential loss, for loss arising from "
            "information withheld or misstated by you, or for outcomes attributable to changes "
            "in law, departmental interpretation or judicial decision after our work was "
            "completed.",
            "Nothing in these terms limits any liability that the Chartered Accountants Act "
            "1949 or ICAI regulations do not permit us to limit.",
        ]),
        ("Intellectual property", [
            "The content, structure, calculators and design of this site are the property of "
            "%s. You may read, print and share pages for your own reference and may quote "
            "short extracts with attribution and a link. Reproducing substantial portions, "
            "republishing articles, or copying the calculators requires our written "
            "permission." % S.NAME,
        ]),
        ("External links", [
            "We link to government portals and third-party resources for convenience. We do "
            "not control those sites and are not responsible for their content, accuracy or "
            "availability. A link is not an endorsement.",
        ]),
        ("Governing law", [
            "These terms are governed by the laws of India. Courts at Bhopal, Madhya Pradesh "
            "have exclusive jurisdiction over any dispute arising from them or from your use "
            "of this website.",
        ]),
        ("Contact", [
            'Questions about these terms should go to <a href="mailto:%s">%s</a> or '
            "+91 94070 00157, or by post to 195-A, 2nd Floor, Zone-1, M.P. Nagar, Bhopal 462011, "
            "Madhya Pradesh." % (S.EMAIL, S.EMAIL),
        ]),
    ]

    legal_page(
        "terms-and-conditions.html",
        "Terms & Conditions | Natasha & Company, Chartered Accountants",
        "Terms governing use of canatasha.com and the basis on which Natasha & Company "
        "provides Chartered Accountancy services, including scope, fees, client "
        "responsibilities and limitation of liability.",
        "Terms &amp; Conditions",
        "The basis on which we provide professional services, and the terms on which "
        "this website is made available.",
        sections, ld_type="WebPage")


if __name__ == "__main__":
    privacy()
    terms()
