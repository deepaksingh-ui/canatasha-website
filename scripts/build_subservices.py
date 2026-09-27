# -*- coding: utf-8 -*-
"""
Dedicated sub-pages for the six practice areas that only had an anchor on
services.html.

Each one targets a distinct local search intent ("virtual CFO Bhopal",
"NRI property sale TDS", "accounting services Bhopal") and carries its own
Service + FAQPage schema, rather than sharing services.html's ranking signal.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nc_shell as S

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# slug, h1, short nav name, icon, meta description, lead, sections, faqs
PAGES = [
{
 "slug": "accounting-bookkeeping-services-bhopal.html",
 "h1": "Accounting &amp; Bookkeeping Services in Bhopal",
 "short": "Accounting &amp; Bookkeeping",
 "icon": "file",
 "title": "Accounting & Bookkeeping Services in Bhopal | Natasha & Company",
 "desc": ("Outsourced accounting and bookkeeping in Bhopal under Indian GAAP and Ind AS "
          "— daily entries, bank and party reconciliation, AP/AR, fixed asset register "
          "and monthly MIS, by an ISO 9001:2015 certified CA firm."),
 "lead": ("Books that stand up to an audit, a bank, and a scrutiny notice &mdash; "
          "maintained monthly, not reconstructed in March."),
 "sections": [
  ("Why bookkeeping is the first line of defence", [
   "<p>Almost every difficult assessment we defend traces back to the same thing: books "
   "written up late, from memory, after the year closed. Cash entries that nobody can "
   "explain. Creditor balances that never reconciled. A fixed asset register that does "
   "not match the depreciation claimed.</p>",
   "<p>When an assessing officer asks for a ledger three years later, the answer is "
   "either in the records or it is not. Accounting is cheap; reconstructing it under "
   "notice is not.</p>"]),
  ("What we maintain", [
   "<ul>"
   "<li>Daily and monthly entries under Indian GAAP, or Ind AS where applicable</li>"
   "<li>Bank reconciliation, and debtor and creditor reconciliation with confirmations</li>"
   "<li>Accounts payable and receivable ageing, with follow-up schedules</li>"
   "<li>Fixed asset register with block-wise depreciation under the Income-tax Act and "
   "the Companies Act separately</li>"
   "<li>Cash and fund flow statements, and liquidity tracking</li>"
   "<li>GST-ready records: ITC register, RCM tracking, and GSTR-2B reconciliation</li>"
   "<li>Payroll registers, TDS on salary, and Form 16 preparation</li>"
   "</ul>"]),
  ("How the engagement runs", [
   "<p>Most clients send documents weekly by WhatsApp or a shared drive. We post entries, "
   "raise queries on anything unclear rather than guessing, and close the month by the "
   "15th of the following month.</p>",
   "<p>You get a monthly pack: trial balance, P&amp;L, balance sheet, debtor and creditor "
   "ageing, and a short note on anything that needs a decision. Quarterly, we review the "
   "position against your tax and GST liability so nothing arrives as a surprise.</p>",
   '<div class="nc-note"><b>Software</b><p>We work on Tally Prime and Zoho Books. If you '
   "already run one of those, we work inside your instance so the data stays yours. If you "
   "do not, we set one up as part of onboarding.</p></div>"]),
  ("Who this suits", [
   "<p>Businesses with turnover from roughly Rs 50 lakh upward that need reliable monthly "
   "numbers but not a full-time accountant; startups that need clean books for due "
   "diligence; and firms whose existing accountant has left mid-year with the records "
   "in an unclear state.</p>"]),
 ],
 "faqs": [
  ("How much does outsourced bookkeeping cost in Bhopal?",
   "It depends on transaction volume, the number of bank accounts and GST registrations, and whether payroll is included. A small trading business with one bank account and under 200 entries a month sits at the lower end; a manufacturer with multiple locations and an ITC reconciliation burden sits considerably higher. We quote a fixed monthly fee in writing after reviewing three months of your existing records."),
  ("Can you take over books that are already behind?",
   "Yes, and a good share of our onboarding is exactly that. We first establish what exists and what is missing, give you a written scope for the catch-up work separately from the ongoing retainer, and tell you plainly if the gaps create exposure you should know about before we start."),
  ("Do you work on Tally or Zoho?",
   "Both. If you already run one, we work inside your instance so you retain ownership and access at all times. If you are starting fresh we will recommend one based on your invoicing volume and whether you need multi-user access."),
  ("Will you also file our GST and TDS returns?",
   "Yes. In practice, bookkeeping and return filing belong together &mdash; separating them is how mismatches between books and returns arise. Most retainers cover monthly GST returns, quarterly TDS returns and the annual reconciliation."),
 ],
},
{
 "slug": "income-tax-return-filing-bhopal.html",
 "h1": "Income Tax &amp; ITR Filing in Bhopal",
 "short": "Income Tax &amp; ITR Filing",
 "icon": "chart",
 "title": "Income Tax Return Filing in Bhopal | ITR, TDS & Tax Planning",
 "desc": ("ITR filing in Bhopal for salaried individuals, professionals, businesses and "
          "NRIs. Old versus new regime comparison, capital gains, TDS compliance, "
          "advance tax and corporate tax planning by CA Natasha Rajvaidya (FCA)."),
 "lead": ("Returns filed on the position we can defend, not the one that looks best "
          "for a single year."),
 "sections": [
  ("Who we file for", [
   "<ul>"
   "<li><strong>Salaried individuals</strong> &mdash; including multiple Form 16s, "
   "house property, and capital gains from shares or mutual funds</li>"
   "<li><strong>Professionals and freelancers</strong> &mdash; presumptive under "
   "Section 44ADA, or regular books where that works out better</li>"
   "<li><strong>Businesses</strong> &mdash; proprietorships, partnerships, LLPs and "
   "companies, with or without audit under Section 44AB</li>"
   "<li><strong>NRIs</strong> &mdash; residential status determination, DTAA relief, "
   "and income sourced in India</li>"
   "<li><strong>Trusts and societies</strong> &mdash; including 12A and 80G positions</li>"
   "</ul>"]),
  ("Old regime or new: it is an annual decision", [
   "<p>The new regime under Section 115BAC is now the default. Whether it beats the old "
   "regime depends on your actual deductions &mdash; 80C, 80D, home loan interest under "
   "Section 24, HRA under Section 10(13A) &mdash; not on a rule of thumb.</p>",
   "<p>For a salaried taxpayer with a home loan and full 80C, the old regime often still "
   "wins. For someone renting, without a loan and with little to invest, the new regime "
   "usually does. We compute both before filing and show you the working.</p>",
   '<p>Our <a href="income-tax-calculator.html">income tax calculator</a> gives you an '
   "indicative comparison in a minute. It is a sanity check, not a filing position.</p>"]),
  ("Beyond the return itself", [
   "<p>Filing is the visible part. The work that avoids notices sits around it:</p>",
   "<ul>"
   "<li>Advance tax estimation across the four instalments, so Sections 234B and 234C "
   "interest does not accumulate</li>"
   "<li>Form 26AS and AIS reconciliation before filing &mdash; most scrutiny notices "
   "start with a mismatch here</li>"
   "<li>TDS compliance: TAN registration, quarterly returns in 24Q, 26Q and 27Q, and "
   "Form 16 and 16A issuance</li>"
   "<li>Capital gains computation with indexation where it still applies, and "
   "Section 54, 54F and 54EC exemption planning</li>"
   "<li>Carry-forward and set-off of losses, which is lost entirely if the return is late</li>"
   "</ul>",
   '<div class="nc-note"><b>File on time, even if you cannot pay</b><p>A late return '
   "forfeits the right to carry forward business and capital losses. The tax can be paid "
   "later with interest; the loss, once lost, does not come back.</p></div>"]),
 ],
 "faqs": [
  ("What is the due date for filing an income tax return?",
   "For individuals and businesses not subject to audit, 31 July following the end of the financial year. Where audit under Section 44AB applies, 31 October. Where transfer pricing provisions apply, 30 November. A belated or revised return can generally be filed up to 31 December of the assessment year. Extensions are announced often enough that you should confirm the current date rather than rely on a chart."),
  ("Should I choose the old or new tax regime?",
   "It depends on your deductions, not on your income alone. If you claim substantial 80C, 80D, HRA and home loan interest, the old regime frequently still produces a lower liability. If you have few deductions, the new regime usually wins. Send us your figures and we will compute both."),
  ("I received an intimation under Section 143(1). Is that a notice?",
   "It is an intimation, not a scrutiny notice, and it commonly reflects an arithmetic adjustment or a mismatch with Form 26AS or the AIS. It still carries a response window and it can turn into a demand if ignored. Send it to us before you agree to the adjustment online."),
  ("Can you file returns for previous years I have missed?",
   "In many cases yes, through an updated return under Section 139(8A), subject to the time limits and additional tax that provision carries. Whether it is worth doing depends on the amounts and on whether the department has already opened proceedings. We will tell you honestly which of your open years are worth filing."),
 ],
},
{
 "slug": "virtual-cfo-services-bhopal.html",
 "h1": "Virtual CFO Services in Bhopal",
 "short": "Virtual CFO",
 "icon": "users",
 "title": "Virtual CFO Services in Bhopal | Outsourced Finance Function",
 "desc": ("Virtual CFO services in Bhopal from an ISO 9001:2015 certified CA firm — "
          "cloud accounting on Tally Prime and Zoho, monthly MIS, cash flow forecasting, "
          "compliance calendars and board-ready reporting, on a fixed monthly retainer."),
 "lead": ("A finance function that reports to you monthly, without the cost of a "
          "full-time CFO."),
 "sections": [
  ("The problem this solves", [
   "<p>Between an accountant who posts entries and a CFO who costs a senior salary, most "
   "growing businesses in Bhopal have nothing. The result is familiar: books are current "
   "but nobody reads them, cash gets managed from the bank balance, pricing decisions are "
   "made on gut feel, and a funding conversation exposes how little of the picture exists "
   "on paper.</p>",
   "<p>A Virtual CFO engagement puts a Chartered Accountant in that gap on a monthly "
   "retainer &mdash; close enough to your numbers to be useful, without the payroll.</p>"]),
  ("What the retainer covers", [
   "<ul>"
   "<li><strong>Cloud accounting</strong> deployed and maintained on Tally Prime or "
   "Zoho Books, with role-based access for your team</li>"
   "<li><strong>Monthly MIS</strong> &mdash; P&amp;L against budget, segment or "
   "product-wise margin, debtor and creditor ageing, and the three or four numbers that "
   "actually drive your business</li>"
   "<li><strong>Cash flow forecasting</strong> on a rolling 13-week basis, so a squeeze "
   "is visible before it arrives</li>"
   "<li><strong>Compliance calendar</strong> owned by us: GST, TDS, ROC, PF and ESI, "
   "with responsibility for the filing, not just a reminder</li>"
   "<li><strong>Monthly review call</strong> with the engagement partner to walk the "
   "numbers and agree actions</li>"
   "<li><strong>Board and lender reporting</strong> in a form banks and investors accept</li>"
   "</ul>"]),
  ("Where it earns its fee", [
   "<p>Usually in three places. Working capital, where disciplined debtor follow-up and "
   "creditor terms release cash that was already yours. Pricing, where product-level "
   "margin data changes what you charge. And financing, where a lender that can read your "
   "numbers lends on better terms than one that cannot.</p>",
   '<div class="nc-note"><b>What it is not</b><p>A Virtual CFO is not a bookkeeper with a '
   "better title, and it is not a statutory auditor &mdash; independence rules mean the "
   "same firm cannot both run your finance function and audit it. Where we act as Virtual "
   "CFO, your statutory audit goes to another firm, and we will say so upfront.</p></div>"]),
 ],
 "faqs": [
  ("How is a Virtual CFO different from an accountant?",
   "An accountant records what happened. A Virtual CFO interprets it and tells you what to do about it — where margin is leaking, when cash will be tight, whether a price or a hire is affordable. The bookkeeping is the input, not the deliverable."),
  ("What does a Virtual CFO cost in Bhopal?",
   "It is a monthly retainer, scoped to your transaction volume, the number of entities and locations, and how much of the compliance load we carry. It is materially less than a full-time senior finance hire, which is the comparison most clients are actually making. We quote in writing after an initial review of your books."),
  ("Can you also be our statutory auditor?",
   "No. ICAI independence requirements prevent the same firm from running a company's finance function and auditing it. We will tell you this at the outset and, if it helps, suggest firms for the audit."),
  ("Do we have to change our accounting software?",
   "Not usually. We work on Tally Prime and Zoho Books, and if you already run either we work inside your existing instance. If you are on something else we will assess whether migration is worth the disruption before recommending it."),
 ],
},
{
 "slug": "nri-taxation-services-bhopal.html",
 "h1": "NRI Taxation &amp; Property Services",
 "short": "NRI Taxation",
 "icon": "globe",
 "title": "NRI Tax Services India | Section 195 TDS, 15CA/CB, Property Sale",
 "desc": ("NRI taxation services from Bhopal — lower deduction certificates under "
          "Section 195 on property sale, Form 15CA and 15CB remittance certification, "
          "DTAA relief, residential status and repatriation, by CA Natasha Rajvaidya (FCA)."),
 "lead": ("Property sales, remittances and Indian income handled from India, for "
          "clients who are not in it."),
 "sections": [
  ("Selling property in India as an NRI", [
   "<p>This is where NRI clients lose the most money, and almost always to the same "
   "mistake. When an NRI sells property, the buyer must deduct TDS under "
   "<strong>Section 195</strong> &mdash; and the default rate applies to the "
   "<em>entire sale consideration</em>, not to the gain.</p>",
   "<p>On a property bought years ago for a fraction of its current value, the actual "
   "capital gains tax is often a small share of that deduction. The excess is recoverable "
   "only as a refund, after filing a return, typically many months later.</p>",
   '<div class="nc-note"><b>The fix is a certificate, applied for before the sale</b>'
   "<p>An application under Section 197 for a lower or nil deduction certificate, filed in "
   "Form 13, tells the buyer to deduct on the real gain instead. It has to be obtained "
   "<em>before</em> the transaction. Once the buyer has deducted and deposited at the full "
   "rate, the only route left is a refund claim.</p></div>",
   "<p>We handle the Form 13 application, the computation supporting it, coordination "
   "with the buyer and their accountant, and the eventual return filing.</p>"]),
  ("Remittances: Form 15CA and 15CB", [
   "<p>Repatriating funds out of India generally requires Form 15CA from the remitter and, "
   "above the prescribed threshold, Form 15CB certified by a Chartered Accountant "
   "confirming the tax position on the remittance.</p>",
   "<p>Banks will not process the transfer without them, and they will not tell you in "
   "advance which part of your documentation is inadequate. We prepare both, and where the "
   "remittance is from a property sale or an inheritance, the supporting trail the bank "
   "will ask for.</p>"]),
  ("The rest of the NRI practice", [
   "<ul>"
   "<li><strong>Residential status</strong> under Section 6, including the deemed "
   "residency provisions that catch high-income NRIs who assume they are outside the net</li>"
   "<li><strong>DTAA relief</strong> &mdash; treaty positions, tax residency certificates, "
   "and Form 10F</li>"
   "<li><strong>ITR filing</strong> for Indian-sourced income: rent, capital gains, "
   "interest and dividends</li>"
   "<li><strong>NRO and NRE account</strong> questions, and repatriation limits</li>"
   "<li><strong>Inherited property</strong> &mdash; cost of acquisition of the previous "
   "owner, holding period, and the documentation to establish both</li>"
   "</ul>"]),
 ],
 "faqs": [
  ("How much TDS is deducted when an NRI sells property in India?",
   "Under Section 195 the buyer deducts on the entire sale consideration, not on the capital gain, at the rate applicable to long-term or short-term gains plus surcharge and cess. Because it applies to the gross amount, the deduction usually far exceeds the actual tax. A lower deduction certificate under Section 197, applied for before the sale, is what corrects this."),
  ("Can I get the excess TDS back?",
   "Yes, by filing an Indian income tax return and claiming the refund, but you will wait — often well past the end of the assessment year. Applying for the Section 197 certificate before the sale avoids the problem instead of remedying it afterwards."),
  ("Do I need to file an ITR in India if I am an NRI?",
   "If your Indian-sourced income exceeds the basic exemption limit, yes. You should also file where TDS has been deducted and you want the refund, or where you need to carry forward a capital loss. Many NRIs who owe nothing still need to file to recover what was deducted."),
  ("What is Form 15CB and who can sign it?",
   "Form 15CB is a certificate from a Chartered Accountant confirming the taxability of a foreign remittance and the rate applied, including any treaty relief. Only a practising CA can issue it. Banks require it alongside Form 15CA above the prescribed threshold."),
  ("Can you handle this if I am not in India?",
   "Yes — most of this practice is conducted remotely. Documents move digitally, and where a physical signature or presence is genuinely required we will tell you early and, where possible, work through a power of attorney."),
 ],
},
{
 "slug": "business-advisory-valuation-bhopal.html",
 "h1": "Business Advisory &amp; Valuation in Bhopal",
 "short": "Business Advisory",
 "icon": "trend",
 "title": "Business Advisory & Valuation in Bhopal | CA Natasha & Company",
 "desc": ("Business valuation, financial due diligence, debt syndication, budgeting and "
          "restructuring advice for businesses in Madhya Pradesh, from an ISO 9001:2015 "
          "certified Chartered Accountancy firm in Bhopal."),
 "lead": ("Valuations, funding and restructuring &mdash; with the workings shown, "
          "because someone on the other side will test them."),
 "sections": [
  ("Valuation", [
   "<p>We value businesses and shareholdings for the reasons they usually need valuing: "
   "raising investment, admitting or retiring a partner, a family settlement, a "
   "transaction under the Companies Act, or a tax position that requires one.</p>",
   "<p>Method follows purpose. A profitable services business with predictable cash flows "
   "is a discounted cash flow candidate; an asset-heavy manufacturer often values better "
   "on net asset value; a comparable-company multiple is a cross-check, not an answer. "
   "We say which method we used and why, and what the number is sensitive to.</p>"]),
  ("Financial due diligence", [
   "<p>Whether you are buying, selling, or taking investment, due diligence is where "
   "assumptions meet records. We test revenue recognition, quality of earnings, working "
   "capital normalisation, related-party dealings, contingent liabilities, and the tax "
   "and GST exposures that transfer with the entity.</p>",
   "<p>The output is a report that says plainly what we found, what we could not verify, "
   "and which items should change the price or the warranties.</p>"]),
  ("Funding and restructuring", [
   "<ul>"
   "<li><strong>Debt syndication</strong> &mdash; CMA data preparation, projections that "
   "a credit committee will accept, and lender coordination</li>"
   "<li><strong>Budgeting and forecasting</strong> with variance reporting that gets used "
   "rather than filed</li>"
   "<li><strong>Financial restructuring</strong> &mdash; capital structure, promoter "
   "funding, and stressed-account positions</li>"
   "<li><strong>Business modelling</strong> for new lines, locations or capacity, with the "
   "break-even and downside cases stated</li>"
   "</ul>",
   '<div class="nc-note"><b>A note on projections</b><p>We will not build a projection we '
   "cannot defend in front of a lender. If the numbers you want to show require assumptions "
   "your history does not support, we will say so before the credit committee does.</p></div>"]),
 ],
 "faqs": [
  ("When does a business actually need a formal valuation?",
   "Most commonly: raising external investment, admitting or retiring a partner or shareholder, a family or matrimonial settlement, a merger or acquisition, an ESOP grant, or a statutory requirement under the Companies Act or the Income-tax Act. If money or ownership is changing hands on the basis of a number, that number should be defensible."),
  ("What is CMA data and why do banks ask for it?",
   "Credit Monitoring Arrangement data is the standardised financial format Indian banks use to assess working capital and term loan proposals — historical financials, projections, fund flow and ratio analysis. Banks ask for it because it lets a credit committee compare your proposal against others on the same basis. A poorly prepared CMA is a common reason a viable proposal stalls."),
  ("Do you help with the whole funding process or only the paperwork?",
   "Both. We prepare the financials and projections, but we also sit in lender discussions, respond to credit queries, and tell you when a term being offered is worse than it looks. Paperwork alone rarely gets a facility sanctioned."),
 ],
},
{
 "slug": "financial-planning-fpa-bhopal.html",
 "h1": "Financial Planning &amp; Analysis",
 "short": "Financial Planning",
 "icon": "calc",
 "title": "Financial Planning & Wealth Structuring in Bhopal | CA Firm",
 "desc": ("Personal and family financial planning from a Chartered Accountancy "
          "perspective in Bhopal — retirement planning, HUF and trust structuring, "
          "succession, and tax-efficient investment review."),
 "lead": ("Planning done by the people who file your return, so the tax position and "
          "the plan agree with each other."),
 "sections": [
  ("Planning from the tax side of the table", [
   "<p>Most financial advice in India is sold by people who earn a commission on the "
   "product. We do not distribute financial products and take no commission on any "
   "investment, which means our advice on what you should hold is worth exactly what our "
   "reasoning is worth &mdash; and nothing else.</p>",
   "<p>What we bring instead is the tax view: how a holding is taxed on exit, how it "
   "interacts with your business income, what it does to your advance tax, and whether "
   "the structure it sits in is the right one.</p>"]),
  ("Structuring: HUF, trusts and succession", [
   "<p>For families with business income or substantial assets, the structure often "
   "matters more than the individual investments.</p>",
   "<ul>"
   "<li><strong>Hindu Undivided Family</strong> &mdash; a separate assessable entity with "
   "its own exemption limit and slab benefit, useful where family income can properly be "
   "attributed to it. Formation, PAN, and the clubbing provisions that limit it.</li>"
   "<li><strong>Private family trusts</strong> for succession and asset protection, and "
   "the taxation that follows from how the trust is drafted</li>"
   "<li><strong>Succession planning</strong> &mdash; wills, nominations that conflict with "
   "wills, and the difference between the two</li>"
   "<li><strong>Gift and clubbing</strong> provisions under Sections 60 to 64, which "
   "undo a good deal of naive planning</li>"
   "</ul>",
   '<p>Read our guide on <a href="hindu-undivided-family-huf-a-strategic-way-to-save-income-tax.html">HUF as a tax planning structure</a> and on '
   '<a href="a-family-that-plans-together-pays-less-tax-together.html">planning across a family</a>.</p>']),
  ("Retirement and cash flow", [
   "<p>For business owners in particular, retirement planning is complicated by the fact "
   "that the business is both the income and the asset. We model what the household needs, "
   "what the business can sustainably distribute, and what a sale or succession would "
   "actually leave after tax &mdash; which is usually the number that matters.</p>",
   '<p>Our <a href="emi-loan-calculator.html">EMI calculator</a> and '
   '<a href="income-tax-calculator.html">income tax calculator</a> cover the arithmetic; '
   "the planning is the conversation around it.</p>"]),
 ],
 "faqs": [
  ("Do you sell insurance or mutual funds?",
   "No. We are not distributors and we earn no commission on any financial product. We review what you hold and advise on structure and tax, and you buy through whichever channel you prefer. This is deliberate — advice paid for by commission is not advice."),
  ("Is forming an HUF still worth it?",
   "It can be, where there is genuine family income that can properly be attributed to the HUF, because it is assessed separately with its own exemption limit and slabs. It is not a device for splitting your own salary — the clubbing provisions in Sections 60 to 64 exist precisely to stop that. Whether it helps depends on your family's income sources."),
  ("What is the difference between a nomination and a will?",
   "A nominee receives the asset from the institution; a will determines who is legally entitled to it. They frequently conflict, and where they do, the will generally prevails for succession while the institution still pays the nominee. Getting both aligned avoids a dispute among people who are grieving."),
 ],
},
]


def build(p):
    prose = []
    for heading, blocks in p["sections"]:
        prose.append("<h2>%s</h2>" % heading)
        prose.extend(blocks)

    faq_items = "".join(
        '<details><summary>%s</summary><div class="nc-faq-a"><p>%s</p></div></details>'
        % (q, a) for q, a in p["faqs"])

    others = "".join(
        '<a href="%s">%s</a>' % (o["slug"], o["short"]) for o in PAGES if o["slug"] != p["slug"])

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
            <a class="nc-btn nc-btn-full nc-btn-sm" href="{book}">Book a consultation</a>
            <a class="nc-btn nc-btn-ghost nc-btn-full nc-btn-sm" href="tel:{phone}">{phone_d}</a>
          </div>
        </div>

        <div class="nc-card">
          <h2 class="nc-h4" style="font-size:1.05rem">Related practices</h2>
          <div class="nc-ftr-links" style="margin-top:.85rem">
            {others}
            <a href="services.html">All 11 services</a>
          </div>
        </div>
      </aside>

    </div>
  </div>
</section>

<section class="nc-sec nc-sec-alt">
  <div class="nc-wrap nc-wrap-nar">
    {fhead}
    <div class="nc-faq" data-nc-rise>{faq}</div>
  </div>
</section>

{cta}""".format(
        phero=S.phero(p["h1"], p["lead"],
                      [("Home", "index.html"), ("Services", "services.html"),
                       (p["short"], None)]),
        prose="\n".join(prose), icon=S.ico(p["icon"]),
        phone=S.PHONE, phone_d=S.PHONE_DISPLAY, others=others, book=S.BOOK_URL,
        fhead=S.sec_head("Questions", "Frequently asked"),
        faq=faq_items, cta=S.cta_band())

    plain = lambda s: s.replace("&amp;", "&").replace('"', "'")
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
}""" % dict(site=S.SITE, slug=p["slug"], name=plain(p["h1"]),
            desc=plain(p["desc"])[:280], org=S.ORG_ID, phone=S.PHONE)

    doc = S.page(
        title=p["title"], desc=p["desc"], slug=p["slug"], body=body,
        keywords="%s Bhopal, CA Bhopal, Chartered Accountant Bhopal, CA Natasha Rajvaidya, %s"
                 % (plain(p["short"]), plain(p["h1"])),
        schema=S.ld(svc_ld, S.faq_schema(p["faqs"]), S.org_schema(),
                    S.crumbs_schema([("Home", "index.html"), ("Services", "services.html"),
                                     (plain(p["h1"]), p["slug"])])))

    with io.open(os.path.join(ROOT, p["slug"]), "w", encoding="utf-8") as f:
        f.write(doc)
    print("  built %-52s %3d KB" % (p["slug"], len(doc) // 1024))


def main():
    for p in PAGES:
        build(p)


if __name__ == "__main__":
    main()
