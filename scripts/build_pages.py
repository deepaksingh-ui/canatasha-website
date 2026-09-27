# -*- coding: utf-8 -*-
"""About, Services, Contact, Blog, Career, Knowledge Base, 404."""
import html as html_lib
import io
import json
import os
import re
import sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nc_shell as S
import _team as T
import build_wp_services as WP
import nc_content as C

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def write(slug, doc):
    with io.open(os.path.join(ROOT, slug), "w", encoding="utf-8") as f:
        f.write(doc)
    print("  built %-46s %5d KB" % (slug, len(doc) // 1024))


# ===================================================================== ABOUT
def about():
    slug = "about-us.html"
    title = "About Natasha & Company | ISO 9001:2015 CA Firm in Bhopal"
    desc = ("Natasha & Company is an ISO 9001:2015 certified Chartered Accountancy firm at "
            "195-A Zone-1, M.P. Nagar, Bhopal, founded in 2017 by CA Natasha Rajvaidya (FCA). "
            "Meet the founder, our standards, vision and quality process.")

    values = [
        ("shield", "Independence",
         "We say what the law says, not what a client hopes it says. A position we cannot defend in a hearing is a position we will not sign."),
        ("clock", "Response",
         "Notices carry deadlines measured in days. Calls and messages are answered the same working day, and urgent notices the same hour."),
        ("scale", "Documentation",
         "Every filing, submission and opinion is archived under our ISO 9001:2015 process, so any file can be reconstructed years later."),
        ("users", "Continuity",
         "One partner owns your file for its life. You never re-explain your business to a new person mid-assessment."),
    ]
    vcards = "".join("""<article class="nc-card nc-card-i nc-svc" data-nc-rise>
  <span class="nc-svc-ico">%s</span>
  <h3 style="font-size:1.16rem">%s</h3>
  <p style="margin-bottom:0">%s</p>
</article>""" % (S.ico(i), t, d) for i, t, d in values)

    faqs = [
        ("Who founded Natasha &amp; Company?",
         "The firm was founded in 2017 by CA Natasha Rajvaidya, a Fellow member of the Institute of Chartered Accountants of India (FCA), and is based at 195-A, Zone-1, M.P. Nagar, Bhopal."),
        ("What does ISO 9001:2015 certification mean for a CA firm?",
         "It means the firm's working methods are documented, audited and repeatable rather than improvised &mdash; how files are opened, how reviews happen, how records are retained, and how client complaints are handled. For you it means the same standard of work regardless of who in the team touches your file."),
        ("How large is the practice?",
         "Natasha &amp; Company serves more than 1,000 clients across Madhya Pradesh and overseas, spanning 11 practice areas from bookkeeping to tax litigation, rated 4.8 across 194+ Google reviews."),
    ]

    body = """{phero}

<section class="nc-sec">
  <div class="nc-wrap">
    <div class="nc-split">
      <div data-nc-rise="left">
        <div class="nc-media">
          <img src="images/279.jpg" alt="Chartered Accountants reviewing financial documents across a desk"
               loading="lazy" decoding="async" width="800" height="600">
        </div>
      </div>
      <div data-nc-rise="right">
        <span class="nc-eyebrow">The practice</span>
        <h2>Nearly a decade, one standard</h2>
        <p>
          Natasha &amp; Company opened in 2017 in M.P. Nagar &mdash; Bhopal&rsquo;s financial
          district &mdash; with a narrow idea: that a mid-sized business deserves the same
          rigour a large one buys from a national firm, without the layers between the
          client and the person actually doing the work.
        </p>
        <p>
          That has held as the practice grew to <strong>11 specialised areas</strong> and
          <strong>1,000+ clients</strong>. We are an <strong>ISO 9001:2015 certified</strong>
          practice, which means our methods are documented and audited rather than assumed.
        </p>
        <p>
          The work spans routine compliance and contested matters in equal measure: statutory
          and tax audits, GST show-cause defence under Sections 73 and 74, income tax scrutiny
          and Section 148 reassessment, company formation and ROC compliance, NRI property
          transactions, and Madhya Pradesh contractor and security licensing.
        </p>
      </div>
    </div>
  </div>
</section>

<section class="nc-sec nc-sec-alt" id="founder">
  <div class="nc-wrap">
    <div class="nc-split">
      <div data-nc-rise="left">
        <span class="nc-eyebrow">The founder</span>
        <h2>CA Natasha Rajvaidya, FCA</h2>
        <p class="nc-lead">Founder &amp; Managing Partner</p>
        <p>
          A Fellow member of the Institute of Chartered Accountants of India, CA Natasha
          Rajvaidya founded the practice in 2017 and continues to lead its audit, litigation
          and advisory work personally.
        </p>
        <p>
          Her practice concentrates on the contested end of the profession &mdash; representing
          clients through GST show-cause proceedings, income tax scrutiny and reassessment,
          and appellate matters &mdash; alongside statutory audit and corporate structuring
          for growing businesses in Madhya Pradesh.
        </p>
        <ul class="nc-checks">
          <li>Fellow Chartered Accountant (FCA), ICAI</li>
          <li>Tax audit and statutory audit signing authority</li>
          <li>Representation before assessing officers and appellate authorities</li>
          <li>Practising in Bhopal since 2017</li>
        </ul>
        <div class="nc-row">
          <a class="nc-btn" href="{book}">Request a consultation</a>
          <a class="nc-alink" href="tel:{phone}">{phone_d} <span class="nc-ar">&rarr;</span></a>
        </div>
      </div>
      <div data-nc-rise="right">
        <div class="nc-media nc-media-portrait">
          <img src="images/brand/team-natasha-800.webp"
               srcset="images/brand/team-natasha-480.webp 480w, images/brand/team-natasha-800.webp 800w"
               sizes="(max-width: 900px) 92vw, 560px"
               alt="CA Natasha Rajvaidya, FCA, Founder of Natasha &amp; Company"
               decoding="async" width="800" height="1000">
          <div class="nc-media-badge">
            <span>
              <b>ISO 9001:2015 Certified</b>
              <span>Quality management</span>
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

{team}

<section class="nc-sec" id="vision">
  <div class="nc-wrap">
    <div class="nc-center">{vhead}</div>
    <div class="nc-grid nc-g4">{vcards}</div>
  </div>
</section>

<section class="nc-sec nc-sec-alt" id="quality">
  <div class="nc-wrap">
    <div class="nc-split">
      <div data-nc-rise="left">
        <span class="nc-eyebrow">Quality</span>
        <h2>What ISO 9001:2015 actually changes</h2>
        <p>
          Certification is easy to put in a footer and harder to run. In practice it means every
          engagement follows a written path: scope agreed before work starts, a named reviewer
          separate from the preparer, version-controlled working papers, and a retention policy
          that lets us reconstruct any filing years later when a notice arrives.
        </p>
        <p>
          It also means the process is audited by an external body rather than asserted by us.
          For a client, the practical benefit is that quality does not depend on who was
          available the week your return was due.
        </p>
      </div>
      <div data-nc-rise="right">
        <div class="nc-card">
          <h3 style="font-size:1.2rem">The engagement path</h3>
          <ul class="nc-checks" style="margin-bottom:0">
            <li>Documents reviewed before any fee is quoted</li>
            <li>Written scope, fee and timeline confirmed in advance</li>
            <li>Preparation and independent review by different people</li>
            <li>Client sign-off recorded before filing</li>
            <li>Working papers archived with a retention schedule</li>
            <li>Compliance calendar issued for the next cycle</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="nc-sec">
  <div class="nc-wrap nc-wrap-nar">
    {fhead}
    <div class="nc-faq" data-nc-rise>{faq}</div>
  </div>
</section>

{cta}""".format(
        phero=S.phero(
            "An ISO 9001:2015 certified practice in the heart of Bhopal",
            "Founded in 2017 by CA Natasha Rajvaidya (FCA). Eleven practice areas, "
            "1,000+ clients, and one partner accountable for every file.",
            [("Home", "index.html"), ("About", None)]),
        team=T.section(alt=False),
        vhead=S.sec_head("What we hold to", "Four things we do not negotiate", center=True),
        vcards=vcards,
        fhead=S.sec_head("Questions", "About the firm"),
        faq="".join('<details><summary>%s</summary><div class="nc-faq-a"><p>%s</p></div></details>'
                    % (q, a) for q, a in faqs),
        cta=S.cta_band(),
        phone=S.PHONE, phone_d=S.PHONE_DISPLAY, book=S.BOOK_URL)

    person = """{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "%s/about-us.html#founder",
  "name": "%s",
  "honorificSuffix": "FCA",
  "jobTitle": "Founder & Managing Partner",
  "image": "%s/images/brand/team-natasha.jpg",
  "worksFor": {"@id": "%s"},
  "alumniOf": {"@type": "Organization", "name": "The Institute of Chartered Accountants of India"},
  "knowsAbout": ["Income Tax", "GST Litigation", "Statutory Audit", "Tax Audit u/s 44AB", "Company Law", "ROC Compliance", "NRI Taxation"],
  "address": {"@type": "PostalAddress", "addressLocality": "Bhopal", "addressRegion": "Madhya Pradesh", "addressCountry": "IN"},
  "url": "%s/about-us.html"
}""" % (S.SITE, S.FOUNDER, S.SITE, S.ORG_ID, S.SITE)

    write(slug, S.page(
        title=title, desc=desc, slug=slug, body=body,
        schema=S.ld(S.org_schema(), person, *T.person_schemas(), S.faq_schema(faqs),
                    S.crumbs_schema([("Home", "index.html"), ("About", slug)]))))


# ================================================================== SERVICES
def services():
    slug = "services.html"
    title = "CA Services in Bhopal | Audit, Tax, GST & ROC — Natasha & Company"
    desc = ("Eleven Chartered Accountancy practice areas from Natasha & Company, Bhopal: "
            "statutory and tax audit u/s 44AB, GST notice defence, income tax scrutiny, "
            "company registration, ROC compliance, Virtual CFO, NRI taxation and MP licensing.")

    anchors = {
        "01": "accounting", "02": "taxation", "03": "audit", "04": "advisory",
        "05": "planning", "06": "compliance", "07": "registration",
        "08": "appeals", "09": "nri", "10": "vcfo", "11": "licensing",
    }

    # Full deliverables per practice, carried over from the original page.
    # These bullets are the page's real substance — the specific form numbers
    # and section references people actually search for.
    detail = json.load(io.open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "_services.json"),
        encoding="utf-8"))[:11]

    cards = []
    for i, (num, name, blurb, icon, href, photo) in enumerate(C.PRACTICES):
        d = detail[i] if i < len(detail) else {"intro": blurb, "items": []}
        bullets = "".join("<li>%s</li>" % x for x in d["items"])
        cards.append("""<article class="nc-pcard" id="%s" data-nc-rise>
  <a class="nc-pcard-img" href="%s" tabindex="-1" aria-hidden="true" data-hover="View this practice">
    <span class="nc-pcard-no">%s</span>
    <img src="%s" alt="" loading="lazy" decoding="async" width="768" height="512">
  </a>
  <a class="nc-pcard-bar" href="%s">%s</a>
  <div class="nc-pcard-body">
    <p>%s</p>
    <ul class="nc-checks" style="margin:0 0 1.35rem">%s</ul>
    <a class="nc-alink" href="%s">Learn more <span class="nc-ar">&rarr;</span></a>
  </div>
</article>""" % (anchors[num], href, num, photo, href, name,
                 d["intro"] or blurb, bullets, href))

    faqs = [
        ("Which CA services does Natasha &amp; Company offer in Bhopal?",
         "Eleven practice areas: accounting and bookkeeping; taxation; audit and assurance including Tax Audit u/s 44AB; business advisory; financial planning; formation and compliance; company registration; appeals and notice defence; specialised NRI practice; technology and Virtual CFO; and licensing including MP PWD contractor and PSARA registration."),
        ("Do you handle GST show-cause notices and appeals?",
         "Yes. We handle ASMT-10 scrutiny, DRC-01 and DRC-01A demands, Section 73 and Section 74 show-cause proceedings, Section 128A amnesty applications, and first appeals &mdash; including drafting replies and appearing at personal hearings."),
        ("Can you act as an outsourced finance function for a small business?",
         "Yes &mdash; that is the Virtual CFO practice. It typically covers cloud accounting on Tally Prime or Zoho, monthly MIS and cash-flow reporting, statutory compliance calendars, and periodic review calls, priced as a monthly retainer rather than per filing."),
        ("How do I choose the right service if I am not sure what I need?",
         "Send the document that prompted the question &mdash; a notice, a balance sheet, a bank letter. We read it before quoting and tell you which practice area it falls under and what it will cost. There is no charge for that first reading."),
    ]

    body = """{phero}

<section class="nc-sec">
  <div class="nc-wrap">
    <div class="nc-center">{head}</div>
    <div class="nc-grid nc-g2">{cards}</div>
  </div>
</section>

{more}

<section class="nc-sec">
  <div class="nc-wrap">
    {phead}
    <div class="nc-grid nc-g4">{steps}</div>
  </div>
</section>

<section class="nc-sec nc-sec-alt">
  <div class="nc-wrap nc-wrap-nar">
    {fhead}
    <div class="nc-faq" data-nc-rise>{faq}</div>
  </div>
</section>

{cta}""".format(
        phero=S.phero(
            "Eleven practice areas, one accountable firm",
            "Routine compliance and contested matters in equal measure &mdash; audit, taxation, "
            "GST litigation, corporate structuring and Madhya Pradesh licensing.",
            [("Home", "index.html"), ("Services", None)]),
        head=S.sec_head("Practice areas", "What we take on", center=True),
        cards="".join(cards),
        more=WP.more_services_section(),
        phead=S.sec_head("How an engagement runs", "Four steps, every time"),
        steps="".join("""<article class="nc-card nc-card-i nc-svc" data-nc-rise>
  <span class="nc-num">0%d</span><h3 style="font-size:1.16rem">%s</h3>
  <p style="margin-bottom:0">%s</p></article>""" % (i, t, d)
                      for i, (t, d) in enumerate(C.PROCESS, 1)),
        fhead=S.sec_head("Questions", "About our services"),
        faq="".join('<details><summary>%s</summary><div class="nc-faq-a"><p>%s</p></div></details>'
                    % (q, a) for q, a in faqs),
        cta=S.cta_band())

    write(slug, S.page(
        title=title, desc=desc, slug=slug, body=body,
        schema=S.ld(S.org_schema(), S.faq_schema(faqs),
                    S.crumbs_schema([("Home", "index.html"), ("Services", slug)]))))


# =================================================================== CONTACT
# Search by the Google Business Profile name, not a lat/lng: Google then pins the
# firm's own listing (with its card), where the old coordinates sat ~200 m off.
MAP_EMBED = ("https://www.google.com/maps?q=" + quote(
    "NATASHA & Co. CA in Bhopal, 195-A, Zone-1, M.P. Nagar, Bhopal 462011")
    + "&hl=en&z=16&output=embed")


def contact():
    slug = "contact-us.html"
    title = "Contact CA Natasha & Company, Bhopal | Book a Consultation"
    desc = ("Talk to a Chartered Accountant in Bhopal. Call +91 94070 00157, email "
            "info@canatasha.com, or visit 195-A Zone-1, M.P. Nagar, Bhopal 462011. "
            "Monday to Saturday, 10am to 7pm.")

    tiles = [
        ("phone", "Direct line", S.PHONE_DISPLAY, "tel:" + S.PHONE),
        ("wa", "WhatsApp", "Send a notice or document", "https://wa.me/919407000157"),
        ("mail", "Email", S.EMAIL, "mailto:" + S.EMAIL),
        ("pin", "Office", "195-A, 2nd Floor, Zone-1, M.P. Nagar (in front of DB Mall), Bhopal 462011", None),
        ("clock", "Hours", "Mon&ndash;Sat, 10:00&ndash;19:00 IST", None),
    ]
    tile_html = []
    for icon, label, val, href in tiles:
        ic = S.social("wa") if icon == "wa" else S.ico(icon)
        inner = ('<span class="nc-svc-ico">%s</span>'
                 '<span class="nc-ctile-t"><small>%s</small><b>%s</b></span>' % (ic, label, val))
        if href:
            ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
            tile_html.append('<a class="nc-ctile" href="%s"%s>%s</a>' % (href, ext, inner))
        else:
            tile_html.append('<div class="nc-ctile">%s</div>' % inner)

    # Only when there is a calendar to send people to.
    pick = ""
    if S.CALENDLY_URL:
        pick = ('<div class="nc-note" style="margin:0 0 2rem"><b>Prefer to pick a time?</b>'
                '<p>Book a slot straight into the calendar &mdash; no back-and-forth.</p>'
                '<a class="nc-btn nc-btn-sm" href="%s">Pick a time</a></div>' % S.BOOK_URL)

    subjects = ["GST notice or litigation", "Income tax notice or scrutiny",
                "Tax audit u/s 44AB", "Statutory audit", "ITR filing",
                "Company / LLP registration", "ROC compliance", "Virtual CFO / accounting",
                "NRI taxation or property sale", "PWD / PSARA licensing", "Something else"]

    faqs = [
        ("How quickly will I get a reply?",
         "Calls and WhatsApp messages are answered the same working day. If your message concerns a notice with a deadline, mark it urgent &mdash; those are picked up within the hour during office hours."),
        ("Is the first consultation chargeable?",
         "No. The first reading of your documents and the scoping conversation are free. We quote a written fixed fee before any work begins."),
        ("Where exactly is the office?",
         "195-A, 2nd Floor, Zone-1, M.P. Nagar, Bhopal 462011, Madhya Pradesh &mdash; in Bhopal's central business district, close to the main Zone-1 market."),
    ]

    body = """{phero}

<section class="nc-sec">
  <div class="nc-wrap">
    <div class="nc-split" style="align-items:start">

      <div data-nc-rise="left">
        {pick}
        <h2 style="font-size:clamp(1.6rem,3vw,2.1rem)">Reach us directly</h2>
        <p class="nc-muted">
          For anything with a deadline on it &mdash; a notice, a hearing date, a filing cut-off
          &mdash; call or WhatsApp rather than emailing.
        </p>
        <div class="nc-stack" style="gap:.85rem;margin-top:1.75rem">{tiles}</div>

        <div class="nc-note" style="margin-top:2rem">
          <b>Sending a notice?</b>
          <p>
            WhatsApp a clear photo or PDF of all pages, including the annexures. Do not reply to
            the department before we have read it &mdash; an early wrong answer narrows your
            options at appeal far more than the original issue does.
          </p>
        </div>
      </div>

      <div data-nc-rise="right">
        <div class="nc-card">
          <h2 style="font-size:clamp(1.5rem,2.6vw,1.9rem)">Request a consultation</h2>
          <p class="nc-muted" style="font-size:.95rem">
            Tell us what you are dealing with. We reply the same working day.
          </p>

          <form class="nc-form nc-form-2" style="margin-top:1.5rem"
                data-lead="contact" data-nc-contact
                action="#" method="post" novalidate>
            <div class="nc-field">
              <label for="f-name">Name <span class="req">*</span></label>
              <input class="nc-input" id="f-name" name="name" type="text" required autocomplete="name" placeholder="Your full name">
            </div>
            <div class="nc-field">
              <label for="f-phone">Phone <span class="req">*</span></label>
              <input class="nc-input" id="f-phone" name="phone" type="tel" required autocomplete="tel"
                     inputmode="tel" pattern="[0-9+ ()-]{{7,20}}" placeholder="+91 ">
            </div>
            <div class="nc-field nc-field-full">
              <label for="f-email">Email</label>
              <input class="nc-input" id="f-email" name="email" type="email" autocomplete="email" placeholder="you@company.com">
            </div>
            <div class="nc-field nc-field-full">
              <label for="f-subject">What is this about? <span class="req">*</span></label>
              <select class="nc-select" id="f-subject" name="subject" required>
                <option value="">Select a topic</option>
                {subjects}
              </select>
            </div>
            <div class="nc-field nc-field-full">
              <label for="f-msg">Details <span class="req">*</span></label>
              <textarea class="nc-textarea" id="f-msg" name="message" required
                        placeholder="Section and assessment year if it is a notice, turnover if it is an audit question, or just describe the situation."></textarea>
            </div>
            <div class="nc-field nc-field-full">
              <div class="nc-fstat" role="status" aria-live="polite"></div>
              <button class="nc-btn nc-btn-full nc-btn-lg" type="submit">Send request</button>
              <p class="nc-form-note" style="margin-top:.85rem">
                We use your details only to reply to this enquiry. See our
                <a href="privacy-policy.html">privacy policy</a>.
              </p>
            </div>
          </form>
        </div>
      </div>

    </div>
  </div>
</section>

<section class="nc-sec nc-sec-alt" id="office-location">
  <div class="nc-wrap">
    {mhead}
    <div class="nc-map-container" data-nc-rise style="display:grid;grid-template-columns:repeat(auto-fit, minmax(340px, 1fr));align-items:stretch;position:relative;width:100%;border-radius:20px;overflow:hidden;box-shadow:0 20px 50px rgba(14, 75, 140, 0.12);border:1px solid var(--nc-line);background:var(--nc-surface)">
      <!-- Office Identity Card (Side-by-Side, Zero Overlap) -->
      <div class="nc-map-float-card" style="position:relative;top:0;left:0;width:100%;background:var(--nc-surface);border:0;border-right:1px solid var(--nc-line);border-radius:0;padding:2.25rem 2rem;box-shadow:none;display:flex;flex-direction:column;justify-content:center;z-index:2">
        <div style="display:flex;align-items:center;justify-content:space-between;gap:.75rem;margin-bottom:.85rem">
          <span class="nc-map-status-pill">
            <span class="nc-map-status-dot"></span> Open Today: 10am&ndash;7pm
          </span>
          <a href="{reviews_url}" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:.3rem;text-decoration:none;font-size:.82rem;font-weight:700;color:var(--nc-ink)">
            <span style="color:var(--nc-acc);letter-spacing:.05em">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
            <span>{rating}</span>
            <small style="color:var(--nc-ink-4);font-weight:500">({reviews}+)</small>
          </a>
        </div>

        <h3 style="font-size:1.2rem;font-weight:700;margin:0 0 .35rem;color:var(--nc-pri)">Natasha &amp; Company</h3>
        <p style="font-size:.84rem;color:var(--nc-ink-3);margin:0 0 1rem;font-weight:500">Chartered Accountants &bull; ISO 9001:2015 Certified</p>

        <div style="display:grid;gap:.65rem;font-size:.88rem;color:var(--nc-ink-2);margin-bottom:1.25rem">
          <div style="display:flex;align-items:flex-start;gap:.6rem">
            <span style="color:var(--nc-pri);margin-top:.15rem;flex-shrink:0">{pin_ico}</span>
            <span><strong>195-A, 2nd Floor, Zone-1</strong>, M.P. Nagar, Bhopal 462011 (In front of DB City Mall area)</span>
          </div>
          <div style="display:flex;align-items:center;gap:.6rem">
            <span style="color:var(--nc-pri);flex-shrink:0">{ph_ico}</span>
            <a href="tel:{phone}" style="color:var(--nc-ink);font-weight:600;text-decoration:none">{phone_d}</a>
          </div>
        </div>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:.6rem">
          <a class="nc-btn nc-btn-sm" href="{directions_url}" target="_blank" rel="noopener" style="justify-content:center;padding:.65rem .8rem;font-size:.82rem">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:4px"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>
            Directions
          </a>
          <a class="nc-btn nc-btn-ghost nc-btn-sm" href="https://wa.me/919407000157?text=Hello%20Natasha%20%26%20Co.,%20I%20need%20directions%20to%20your%20office" target="_blank" rel="noopener" style="justify-content:center;padding:.65rem .8rem;font-size:.82rem">
            WhatsApp
          </a>
        </div>
      </div>

      <!-- Real Map Frame -->
      <div class="nc-map-iframe-wrap">
        <iframe title="Natasha &amp; Company office location, Zone-1 M.P. Nagar, Bhopal"
                src="{map_src}"
                loading="lazy" referrerpolicy="no-referrer-when-downgrade"
                allowfullscreen></iframe>
      </div>
    </div>
  </div>
</section>

<section class="nc-sec">
  <div class="nc-wrap nc-wrap-nar">
    {fhead}
    <div class="nc-faq" data-nc-rise>{faq}</div>
  </div>
</section>""".format(
        phero=S.phero(
            "Talk to a Chartered Accountant",
            "One call is usually enough to tell you where you stand, what it will cost, "
            "and what happens next.",
            [("Home", "index.html"), ("Contact", None)]),
        tiles="".join(tile_html),
        pick=pick,
        map_src=html_lib.escape(MAP_EMBED),
        subjects="".join('<option>%s</option>' % s for s in subjects),
        mhead=S.sec_head("Visit", "195-A, Zone-1, M.P. Nagar, Bhopal 462011"),
        directions_url="https://www.google.com/maps/dir/?api=1&destination=NATASHA+%26+Co.+CA+in+Bhopal%2C+195-A%2C+Zone-1%2C+M.P.+Nagar%2C+Bhopal+462011",
        reviews_url=S.REVIEWS_URL,
        rating=S.RATING,
        reviews=S.REVIEW_COUNT,
        pin_ico=S.ico("pin"),
        ph_ico=S.ico("phone"),
        phone=S.PHONE,
        phone_d=S.PHONE_DISPLAY,
        fhead=S.sec_head("Questions", "Before you get in touch"),
        faq="".join('<details><summary>%s</summary><div class="nc-faq-a"><p>%s</p></div></details>'
                    % (q, a) for q, a in faqs))

    cp = """{
  "@context": "https://schema.org",
  "@type": "ContactPage",
  "@id": "%s/contact-us.html#contact",
  "name": "Contact Natasha & Company",
  "about": {"@id": "%s"},
  "url": "%s/contact-us.html"
}""" % (S.SITE, S.ORG_ID, S.SITE)

    write(slug, S.page(
        title=title, desc=desc, slug=slug, body=body,
        schema=S.ld(S.org_schema(), cp, S.faq_schema(faqs),
                    S.crumbs_schema([("Home", "index.html"), ("Contact", slug)]))))


# =================================================================== BOOKING
def booking():
    """Calendly booking page: the site's main call to action.

    Built only when S.CALENDLY_URL is set. Without it any stale copy is removed,
    so the sitemap never lists a page with an empty calendar.
    """
    slug = "book-consultation.html"
    path = os.path.join(ROOT, slug)
    if not S.CALENDLY_URL:
        if os.path.exists(path):
            os.remove(path)
            print("  removed %s (no CALENDLY_URL set)" % slug)
        return

    title = "Book a Consultation with a CA in Bhopal | Natasha & Company"
    desc = ("Book a free first consultation with a Chartered Accountant in Bhopal. Pick a day and "
            "time online with Natasha & Company, 195-A Zone-1, M.P. Nagar. For an urgent notice, "
            "call +91 94070 00157.")

    # Calendly's own primary colour is the site's blue: white text on the brand
    # orange fails contrast, and it is the button colour inside the widget.
    sep = "&" if "?" in S.CALENDLY_URL else "?"
    embed = S.CALENDLY_URL + sep + "hide_gdpr_banner=1&primary_color=0b5fa5"

    steps = [
        ("Pick a slot", "Choose any open day and time that suits you. Calendly shows times in your own time zone."),
        ("Tell us what it is about", "Add a line on what you need help with &mdash; a notice, an audit, a registration. The more specific, the better we can prepare."),
        ("Talk to a Chartered Accountant", "We tell you where you stand, what it will cost and what happens next, with a written fixed fee before any work begins."),
    ]
    tiles = [
        ("phone", "Call", S.PHONE_DISPLAY, "tel:" + S.PHONE),
        ("wa", "WhatsApp", "Send a notice or document", "https://wa.me/919407000157"),
        ("mail", "Write to us", "Use the contact form", "contact-us.html"),
    ]
    tile_html = []
    for icon, label, val, href in tiles:
        ic = S.social("wa") if icon == "wa" else S.ico(icon)
        ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
        tile_html.append(
            '<a class="nc-ctile" href="%s"%s><span class="nc-svc-ico">%s</span>'
            '<span class="nc-ctile-t"><small>%s</small><b>%s</b></span></a>'
            % (href, ext, ic, label, val))

    body = """{phero}

<section class="nc-sec nc-sec-tight">
  <div class="nc-wrap">
    <div class="nc-card nc-cal-card" data-nc-rise>
      <div class="nc-cal-head">
        <span class="nc-svc-ico">{cal}</span>
        <div>
          <h2>Choose a day and time</h2>
          <p class="nc-muted">The first consultation is free. You get a confirmation email, with a link to reschedule if plans change.</p>
        </div>
      </div>
      <div class="calendly-inline-widget nc-cal" data-url="{embed}"></div>
      <p class="nc-cal-alt">
        Calendar not loading? <a href="{url}" target="_blank" rel="noopener">Open it in a new tab</a>,
        or call <a href="tel:{phone}">{phone_d}</a>.
      </p>
    </div>
  </div>
</section>

<section class="nc-sec nc-sec-alt">
  <div class="nc-wrap">
    {shead}
    <div class="nc-grid nc-g3">{steps}</div>
  </div>
</section>

<section class="nc-sec">
  <div class="nc-wrap">
    {ohead}
    <div class="nc-grid nc-g3">{tiles}</div>
    <div class="nc-note" style="margin-top:2rem">
      <b>Got a notice with a deadline?</b>
      <p>
        Call or WhatsApp a clear photo or PDF of all pages instead of waiting for a slot.
        Do not reply to the department before we have read it &mdash; an early wrong answer
        narrows your options at appeal far more than the original issue does.
      </p>
    </div>
  </div>
</section>""".format(
        phero=S.phero(
            "Book a consultation",
            "Pick a day and time that suits you, and speak to a Chartered Accountant. "
            "The first consultation is free.",
            [("Home", "index.html"), ("Book a consultation", None)]),
        cal=S.ico("calendar"), embed=html_lib.escape(embed), url=html_lib.escape(S.CALENDLY_URL),
        phone=S.PHONE, phone_d=S.PHONE_DISPLAY,
        shead=S.sec_head("How it works", "Three steps, no back-and-forth"),
        steps="".join("""<article class="nc-card nc-card-i nc-svc" data-nc-rise>
  <span class="nc-num">0%d</span><h3 style="font-size:1.16rem">%s</h3>
  <p style="margin-bottom:0">%s</p></article>""" % (i, t, d)
                      for i, (t, d) in enumerate(steps, 1)),
        ohead=S.sec_head("Prefer another way?", "Call, message or send a notice"),
        tiles="".join(tile_html))

    wp = """{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "@id": "%s/%s#page",
  "name": "Book a consultation",
  "url": "%s/%s",
  "isPartOf": {"@id": "%s"},
  "about": {"@id": "%s"}
}""" % (S.SITE, slug, S.SITE, slug, S.SITE_ID, S.ORG_ID)

    write(slug, S.page(
        title=title, desc=desc, slug=slug, body=body,
        schema=S.ld(S.org_schema(), wp,
                    S.crumbs_schema([("Home", "index.html"), ("Book a consultation", slug)])),
        extra_js='\n<script src="https://assets.calendly.com/assets/external/widget.js" async></script>'))


# ====================================================================== BLOG
def blog():
    slug = "blog.html"
    posts = C.articles()
    cats = sorted({a["cat"] for a in posts})

    title = "Tax, GST & Compliance Insights | Natasha & Company, Bhopal"
    desc = ("Practical notes on income tax, GST, ROC compliance and Madhya Pradesh business "
            "regulation from CA Natasha Rajvaidya (FCA) and the team at Natasha & Company, Bhopal.")

    cards = "".join(C.post_card(a) for a in posts)
    chips = "".join(
        '<span class="nc-tag" style="padding:.4rem .9rem;font-size:.78rem">%s</span>' % c
        for c in cats)

    itemlist = ",\n    ".join(
        '{"@type": "ListItem", "position": %d, "url": "%s/%s"}' % (i, S.SITE, a["slug"])
        for i, a in enumerate(posts, 1))
    blog_ld = """{
  "@context": "https://schema.org",
  "@type": "Blog",
  "@id": "%s/blog.html#blog",
  "name": "Natasha & Company Insights",
  "description": "Income tax, GST and compliance guidance for businesses in Madhya Pradesh.",
  "url": "%s/blog.html",
  "publisher": {"@id": "%s"},
  "inLanguage": "en-IN",
  "blogPost": {"@type": "ItemList", "numberOfItems": %d, "itemListElement": [
    %s
  ]}
}""" % (S.SITE, S.SITE, S.ORG_ID, len(posts), itemlist)

    body = """{phero}

<section class="nc-sec">
  <div class="nc-wrap">
    <h2 class="nc-sr">All articles</h2>
    <div class="nc-row" style="gap:.5rem;margin-bottom:2.5rem" data-nc-rise>{chips}</div>
    <div class="nc-grid nc-g3">{cards}</div>
  </div>
</section>

{cta}""".format(
        phero=S.phero(
            "Notes on what just changed",
            "%d guides on income tax, GST, ROC compliance and Madhya Pradesh business "
            "regulation &mdash; written for business owners, not for other accountants."
            % len(posts),
            [("Home", "index.html"), ("Insights", None)]),
        chips=chips, cards=cards, cta=S.cta_band())

    write(slug, S.page(
        title=title, desc=desc, slug=slug, body=body,
        schema=S.ld(blog_ld, S.org_schema(),
                    S.crumbs_schema([("Home", "index.html"), ("Insights", slug)]))))


# ==================================================================== CAREER
def career():
    slug = "career.html"
    title = "Careers & Articleship at Natasha & Company, Bhopal"
    desc = ("Join an ISO 9001:2015 certified CA firm in Bhopal. Articleship, semi-qualified "
            "and qualified Chartered Accountant roles in audit, taxation and GST litigation. "
            "Apply to info@canatasha.com.")

    roles = [
        ("Articled Assistant", "ICAI registration &middot; 3 years",
         "Rotation across statutory audit, tax audit, GST compliance and litigation support. "
         "You will attend hearings and draft submissions, not only tick schedules."),
        ("Semi-Qualified Assistant", "IPCC / Inter cleared",
         "Ownership of a client set for GST returns, TDS and ROC filings, with review by the "
         "engagement partner. Suited to someone who wants breadth quickly."),
        ("Chartered Accountant", "Qualified &middot; 0&ndash;3 years",
         "Lead audits and assessments end to end, including representation before assessing "
         "officers and appellate authorities. Direct partner mentoring."),
        ("Accounts Executive", "B.Com / M.Com &middot; Tally, Zoho",
         "Day-to-day bookkeeping, bank reconciliation and MIS preparation for retainer clients "
         "on cloud accounting systems."),
    ]
    rcards = "".join("""<article class="nc-card nc-card-i nc-svc" data-nc-rise>
  <span class="nc-tag" style="align-self:flex-start;margin-bottom:1rem">%s</span>
  <h3 style="font-size:1.2rem">%s</h3>
  <p>%s</p>
  <a class="nc-alink" href="mailto:%s?subject=Application%%20%%E2%%80%%94%%20%s">
    Apply by email <span class="nc-ar">&rarr;</span></a>
</article>""" % (tag, t, d, S.EMAIL, t.replace(" ", "%20")) for t, tag, d in roles)

    body = """{phero}

<section class="nc-sec">
  <div class="nc-wrap">
    <div class="nc-split">
      <div data-nc-rise="left">
        <span class="nc-eyebrow">Why here</span>
        <h2>You will see the contested work, not just the filing</h2>
        <p>
          Plenty of firms will teach you to prepare a return. Fewer will put you in the room
          when the assessing officer asks why a particular deduction was claimed. Our practice
          runs heavily to notices, scrutiny and appeals, which means the people who train here
          learn to defend a position rather than only record one.
        </p>
        <ul class="nc-checks">
          <li>Rotation across audit, direct tax, GST and corporate law</li>
          <li>Exposure to hearings, submissions and appellate drafting</li>
          <li>ISO 9001:2015 documented working-paper discipline</li>
          <li>Direct review by the engagement partner, every file</li>
          <li>Study leave honoured around ICAI examination cycles</li>
        </ul>
      </div>
      <div data-nc-rise="right">
        <div class="nc-media">
          <img src="images/279.jpg" alt="Working through financial documents together at Natasha &amp; Company"
               loading="lazy" decoding="async" width="800" height="600">
        </div>
      </div>
    </div>
  </div>
</section>

<section class="nc-sec nc-sec-alt">
  <div class="nc-wrap">
    {rhead}
    <div class="nc-grid nc-g2">{roles}</div>
  </div>
</section>

<section class="nc-sec">
  <div class="nc-wrap nc-wrap-nar nc-center">
    <div class="nc-cta" data-nc-rise>
      <span class="nc-eyebrow">How to apply</span>
      <h2>Send a CV, and one paragraph</h2>
      <p>
        Email your CV to <a href="mailto:{email}">{email}</a> with the role in the subject line.
        In the body, tell us about one piece of work you found genuinely difficult and what you
        did about it. That paragraph matters more to us than your marks.
      </p>
      <div class="nc-row">
        <a class="nc-btn nc-btn-lg" href="mailto:{email}?subject=Application">Email your CV</a>
        <a class="nc-btn nc-btn-ghost nc-btn-lg" href="tel:{phone}">{phone_d}</a>
      </div>
    </div>
  </div>
</section>""".format(
        phero=S.phero(
            "Build a practice, not just a CV",
            "Articleship and qualified roles at an ISO 9001:2015 certified firm in "
            "Zone-1, M.P. Nagar, Bhopal.",
            [("Home", "index.html"), ("Careers", None)]),
        rhead=S.sec_head("Open roles", "Where we are hiring"),
        roles=rcards, email=S.EMAIL, phone=S.PHONE, phone_d=S.PHONE_DISPLAY)

    write(slug, S.page(
        title=title, desc=desc, slug=slug, body=body,
        schema=S.ld(S.org_schema(),
                    S.crumbs_schema([("Home", "index.html"), ("Careers", slug)]))))


# ============================================================ KNOWLEDGE BASE
def _kb_tables():
    """TDS and CII reference tables lifted from the original knowledge base.

    In the old build these lived inside Bootstrap modals, so they never showed
    on the page and search engines got no value from them. They are real
    sections now.
    """
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_kb_tables.json")
    return json.load(io.open(p, encoding="utf-8"))


def _calendar():
    """Month-tabbed statutory compliance calendar.

    Recurring monthly items repeat under every month, since that is how they
    actually behave; dated items are month-specific. No year is printed —
    Indian due dates shift by extension often enough that a hard-coded year
    goes stale and misleads.
    """
    import _duedates as D

    tabs, panels = [], []
    for n, (month, items) in enumerate(D.MONTHS, 1):
        tabs.append(
            '<button class="nc-cal-tab" type="button" role="tab" data-month="%d" '
            'aria-selected="false" aria-controls="cal-%d" id="tab-%d" tabindex="-1">%s</button>'
            % (n, n, n, month[:3]))

        rows = []
        for day, label, detail, tag in items:
            rows.append("""<li class="nc-cal-row">
  <span class="nc-cal-day">%s<small>%s</small></span>
  <span class="nc-cal-body"><b>%s</b><p>%s</p><span class="nc-tag">%s</span></span>
</li>""" % (day, month[:3], label, detail, tag))

        for day, label, detail, tag in D.RECURRING:
            rows.append("""<li class="nc-cal-row">
  <span class="nc-cal-day">%s<small>every mo</small></span>
  <span class="nc-cal-body"><b>%s</b><p>%s</p><span class="nc-tag">%s</span></span>
</li>""" % (day, label, detail, tag))

        rows.sort(key=lambda r: int(re.search(r'nc-cal-day">(\d+)', r).group(1)))

        panels.append(
            '<div class="nc-cal-panel" role="tabpanel" id="cal-%d" data-month="%d" '
            'aria-labelledby="tab-%d" hidden><ul class="nc-cal-list">%s</ul></div>'
            % (n, n, n, "".join(rows)))

    return ('<div class="nc-cal-tabs" role="tablist" aria-label="Compliance month">%s</div>'
            '%s' % ("".join(tabs), "".join(panels)))


def _portals():
    import _duedates as D
    return '<div class="nc-portals">%s</div>' % "".join(
        '<a class="nc-portal" href="%s" target="_blank" rel="noopener">'
        '<b>%s</b><span>%s</span></a>' % (url, name, desc)
        for name, desc, url in D.PORTALS)


def _table(rows, cls=""):
    head = "".join("<th>%s</th>" % c for c in rows[0])
    body = "".join(
        "<tr>%s</tr>" % "".join(
            "<td>%s</td>" % (("<strong>%s</strong>" % c) if i == 0 else c)
            for i, c in enumerate(r))
        for r in rows[1:])
    return ('<div class="nc-tw" data-nc-rise><table class="nc-table%s">'
            "<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>"
            % ((" " + cls) if cls else "", head, body))


def kb():
    slug = "knowledge-base.html"
    title = "Knowledge Base | TDS Rates, CII Chart & Tax Calculators — CA Bhopal"
    desc = ("TDS rate chart for FY 2025-26, the full Cost Inflation Index directory from "
            "2001-02, statutory due dates, and free income tax, HRA, GST and EMI "
            "calculators from Natasha & Company, Chartered Accountants, Bhopal.")

    tools = [
        ("calc", "Income Tax Calculator", "Compare the old and new regimes and see your effective rate.", "income-tax-calculator.html"),
        ("building", "HRA Exemption Calculator", "Section 10(13A) exemption from rent, salary and city.", "hra-exemption-calculator.html"),
        ("chart", "GST Calculator", "Split any amount inclusive or exclusive of GST across slabs.", "gst-calculator.html"),
        ("trend", "EMI Loan Calculator", "Monthly instalment, total interest and full amortisation.", "emi-loan-calculator.html"),
    ]
    tcards = "".join("""<article class="nc-card nc-card-i nc-card-glow nc-svc" data-nc-rise>
  <span class="nc-svc-ico">%s</span><h3 style="font-size:1.18rem">%s</h3><p>%s</p>
  <a class="nc-alink" href="%s">Open the calculator <span class="nc-ar">&rarr;</span></a>
</article>""" % (S.ico(i), t, d, h) for i, t, d, h in tools)

    posts = C.articles()
    by_cat = {}
    for a in posts:
        by_cat.setdefault(a["cat"], []).append(a)

    guides = []
    for cat in sorted(by_cat):
        links = "".join('<a href="%s">%s</a>' % (a["slug"], a["title"]) for a in by_cat[cat][:8])
        guides.append("""<div class="nc-card" data-nc-rise>
  <h3 style="font-size:1.1rem;color:var(--nc-pri)">%s</h3>
  <div class="nc-ftr-links" style="margin-top:1rem">%s</div>
</div>""" % (cat, links))

    dates = [
        ("GSTR-1", "11th of the following month", "Monthly outward supplies"),
        ("GSTR-3B", "20th of the following month", "Summary return and payment"),
        ("TDS payment", "7th of the following month", "Challan 281"),
        ("TDS return", "31 Jul / 31 Oct / 31 Jan / 31 May", "Form 24Q, 26Q quarterly"),
        ("Advance tax", "15 Jun / 15 Sep / 15 Dec / 15 Mar", "15%, 45%, 75%, 100% cumulative"),
        ("ITR (non-audit)", "31 July", "Individuals and non-audit cases"),
        ("Tax audit report", "30 September", "Form 3CA/3CB and 3CD"),
        ("ITR (audit cases)", "31 October", "Where audit u/s 44AB applies"),
        ("ROC AOC-4", "30 days from AGM", "Financial statements"),
        ("ROC MGT-7", "60 days from AGM", "Annual return"),
    ]
    rows = "".join("<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td></tr>" % d for d in dates)

    # Live news + recurring due dates, driven by data/compliance-data.json so
    # the admin editor's output actually reaches the page.
    cd = json.load(io.open(os.path.join(ROOT, "data", "compliance-data.json"),
                           encoding="utf-8"))
    news = "".join("""<a class="nc-card nc-card-i nc-svc" href="%s" data-nc-rise>
  <span class="nc-tag" style="align-self:flex-start;margin-bottom:.9rem">%s</span>
  <p style="color:var(--nc-ink);font-size:.98rem;margin-bottom:1rem">%s</p>
  <span class="nc-alink" style="margin-top:auto">Read more <span class="nc-ar">&rarr;</span></span>
</a>""" % (n.get("link", "blog.html"), n.get("tag", "Update"), n.get("title", ""))
                   for n in cd.get("latest_news", []))

    recur = "".join(
        "<tr><td><strong>%s</strong></td><td>%s</td></tr>"
        % (d.get("title", ""), d.get("due", "")) for d in cd.get("due_dates", []))

    tabs = _kb_tables()

    body = """{phero}

<section class="nc-sec">
  <div class="nc-wrap">
    {nhead}
    <div class="nc-grid nc-g3">{news}</div>
  </div>
</section>

<section class="nc-sec nc-sec-alt">
  <div class="nc-wrap">
    {thead}
    <div class="nc-grid nc-g4">{tools}</div>
  </div>
</section>

<section class="nc-sec" id="due-dates">
  <div class="nc-wrap">
    {dhead}
    <div data-nc-rise>{calendar}</div>
    <p class="nc-form-note nc-mt2">
      Indicative dates for a standard financial year, opening on the current month.
      Extensions and case-specific variations are common &mdash; confirm your own
      position before relying on this. <a href="contact-us.html">Ask us</a> if a
      deadline is close.
    </p>
  </div>
</section>

<section class="nc-sec nc-sec-alt" id="portals">
  <div class="nc-wrap">
    {phead}
    <div data-nc-rise>{portals}</div>
  </div>
</section>

<section class="nc-sec nc-sec-alt" id="tds-rates">
  <div class="nc-wrap">
    {tdshead}
    {tdstable}
    <p class="nc-form-note nc-mt1">
      Rates under the Income-tax Act 1961 as amended by the Finance Acts 2024 and 2025.
      Section 206AA applies a higher rate where PAN is not furnished or is inoperative.
    </p>
  </div>
</section>

<section class="nc-sec" id="cost-inflation-index">
  <div class="nc-wrap">
    {ciihead}
    <div class="nc-note" data-nc-rise>
      <b>Indexed cost of acquisition</b>
      <p>
        Indexed Cost = (Actual Cost of Acquisition &times; CII of the year of transfer)
        &divide; CII of the year of acquisition.
      </p>
      <p style="margin-top:.6rem">
        Budget 2024 changed the position for property: for transfers on or after
        23 July 2024, long-term capital gains are taxed at 12.5% without indexation,
        with a grandfathering option for resident individuals and HUFs on property
        acquired before that date. Which route is better depends on your holding
        period and gain &mdash; <a href="contact-us.html">ask us to run both</a>.
      </p>
    </div>
    {ciitable}
  </div>
</section>

<section class="nc-sec nc-sec-alt">
  <div class="nc-wrap">
    {ghead}
    <div class="nc-grid nc-g3">{guides}</div>
  </div>
</section>

{cta}""".format(
        phero=S.phero(
            "TDS rates, CII chart, due dates and calculators",
            "The reference material our clients ask for most often, free to use "
            "and kept current.",
            [("Home", "index.html"), ("Knowledge Base", None)]),
        nhead=S.sec_head("Latest", "What changed recently"),
        news=news,
        thead=S.sec_head("Free tools", "Four calculators that answer the usual questions"),
        tools=tcards,
        dhead=S.sec_head("Compliance calendar", "Statutory due dates, month by month",
                         "Recurring filings repeat under every month; dated items are "
                         "specific to that month."),
        calendar=_calendar(),
        phead=S.sec_head("Official portals", "Where the filings actually go"),
        portals=_portals(),
        tdshead=S.sec_head("Reference", "TDS rate chart, FY 2025-26 (AY 2026-27)"),
        tdstable=_table(tabs["tds"]),
        ciihead=S.sec_head("Reference", "Cost Inflation Index, 2001-02 to 2025-26"),
        ciitable=_table(tabs["cii"]),
        ghead=S.sec_head("Guides", "By subject"),
        guides="".join(guides),
        cta=S.cta_band())

    ds = """{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "@id": "%(site)s/knowledge-base.html#cii",
  "name": "Cost Inflation Index (CII) directory, India, FY 2001-02 to FY 2025-26",
  "description": "Cost Inflation Index notified under the Income-tax Act 1961, by financial year and assessment year, used to compute the indexed cost of acquisition for long-term capital gains.",
  "url": "%(site)s/knowledge-base.html#cost-inflation-index",
  "creator": {"@id": "%(org)s"},
  "isAccessibleForFree": true,
  "inLanguage": "en-IN",
  "spatialCoverage": {"@type": "Country", "name": "India"},
  "temporalCoverage": "2001-04-01/2026-03-31",
  "variableMeasured": ["Financial Year", "Assessment Year", "Cost Inflation Index"]
}""" % dict(site=S.SITE, org=S.ORG_ID)

    write(slug, S.page(
        title=title, desc=desc, slug=slug, body=body,
        keywords="TDS rate chart FY 2025-26, Cost Inflation Index chart, CII table, "
                 "GST due dates, tax calculator, CA Bhopal, Natasha and Company",
        schema=S.ld(ds, S.org_schema(),
                    S.crumbs_schema([("Home", "index.html"), ("Knowledge Base", slug)]))))


# ======================================================================= 404
def notfound():
    slug = "404.html"
    body = """<section class="nc-sec" style="display:grid;place-items:center;min-height:74vh;text-align:center">
  <div class="nc-wrap nc-wrap-nar">
    <span class="nc-eyebrow" style="justify-content:center">Error 404</span>
    <h1 style="font-size:clamp(3rem,10vw,6rem);margin-bottom:.4em">
      <span class="nc-shimmer">404</span>
    </h1>
    <h2 style="font-size:clamp(1.4rem,3vw,2rem)">This page is not where it used to be</h2>
    <p class="nc-lead">
      The link may be out of date, or the page may have moved. Here is where most people
      were heading.
    </p>
    <div class="nc-row" style="justify-content:center;margin-top:2rem">
      <a class="nc-btn nc-btn-lg" href="index.html">Back to home</a>
      <a class="nc-btn nc-btn-ghost nc-btn-lg" href="services.html">Our services</a>
    </div>
    <div class="nc-grid nc-g4 nc-mt3" style="text-align:left">
      <a class="nc-card nc-card-i" href="blog.html"><h3 style="font-size:1.05rem">Insights</h3>
        <p class="nc-muted" style="font-size:.9rem;margin:0">Tax and GST guides</p></a>
      <a class="nc-card nc-card-i" href="knowledge-base.html"><h3 style="font-size:1.05rem">Calculators</h3>
        <p class="nc-muted" style="font-size:.9rem;margin:0">Tax, HRA, GST, EMI</p></a>
      <a class="nc-card nc-card-i" href="about-us.html"><h3 style="font-size:1.05rem">About</h3>
        <p class="nc-muted" style="font-size:.9rem;margin:0">The firm and founder</p></a>
      <a class="nc-card nc-card-i" href="contact-us.html"><h3 style="font-size:1.05rem">Contact</h3>
        <p class="nc-muted" style="font-size:.9rem;margin:0">Book a consultation</p></a>
    </div>
  </div>
</section>"""

    write(slug, S.page(
        title="Page not found | " + S.NAME_PLAIN,
        desc="The page you are looking for could not be found. Browse our services, "
             "calculators and insights, or contact Natasha & Company, Bhopal.",
        slug=slug, body=body, noindex=True))


def main():
    about()
    services()
    contact()
    booking()
    blog()
    career()
    kb()
    notfound()


if __name__ == "__main__":
    main()
