# -*- coding: utf-8 -*-
"""Home page."""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nc_shell as S
import nc_content as C

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TITLE = "Chartered Accountants in Bhopal | Tax, Audit & GST — Natasha & Company"
DESC = ("ISO 9001:2015 certified CA firm in Zone-1 M.P. Nagar, Bhopal, founded by "
        "CA Natasha Rajvaidya (FCA). Tax audit u/s 44AB, GST notice and litigation "
        "defence, income tax scrutiny representation, company registration and "
        "Virtual CFO services. Rated 4.8 across 194+ Google reviews.")


# Rotating hero slides. Each leads with a different practice so the first
# screen speaks to whichever problem brought the visitor here.
# One slide per major practice, the way the reference leads with a different
# service on each rotation, so the first screen speaks to whichever problem
# brought the visitor here.
SLIDES = [
    ("Chartered Accountants",
     "Audit &middot; Taxation &middot; Advisory",
     "Chartered", "Accountants",
     "Led by <strong>CA Natasha Rajvaidya (FCA)</strong>, we handle statutory and tax audits, "
     "GST notice defence, income tax scrutiny and corporate advisory for businesses across "
     "Madhya Pradesh &mdash; from 195-A, Zone-1, M.P. Nagar, Bhopal.",
     ("services.html", "Explore 11 practice areas"), "images/slide-1.jpg"),

    ("GST notice defence",
     "Section 73 &middot; Section 74 &middot; Appeals",
     "Got a GST", "notice?",
     "ASMT-10 scrutiny, DRC-01 show cause, Section 65 audits and first appeals in APL-01 "
     "&mdash; read, answered and represented through to closure. Send us the notice before "
     "you reply to it.",
     ("gst-notice-consultant-bhopal.html", "How we handle notices"), "images/slide-2.jpg"),

    ("Company formation",
     "Pvt Ltd &middot; LLP &middot; OPC &middot; ROC",
     "Start it", "properly",
     "Private Limited, LLP, OPC and Section 8 incorporation, Startup India DPIIT recognition, "
     "and the annual ROC compliance that follows &mdash; structured right the first time.",
     ("company-registration-bhopal.html", "Company registration"), "images/BPO-2048x1365.jpg"),

    ("Tax audit",
     "Section 44AB &middot; Form 3CD",
     "Tax audit,", "signed on time",
     "Turnover threshold reviewed properly, Form 3CA or 3CB with clause-wise 3CD, and the "
     "report filed before the due date &mdash; not the week after it.",
     ("tax-audit-44ab-bhopal.html", "Tax audit u/s 44AB"), "images/finance-1-2048x1365.jpg"),

    ("Income tax notices",
     "143(1) &middot; 143(2) &middot; 148 &middot; 133(6)",
     "Scrutiny", "handled",
     "Intimations, scrutiny and reassessment answered on the law, with representation before "
     "the assessing officer and through first appeal.",
     ("income-tax-notice-consultant-bhopal.html", "Notice defence"), "images/279.jpg"),

    ("Virtual CFO",
     "Cloud books &middot; MIS &middot; Cash flow",
     "Your finance", "function",
     "Cloud accounting on Tally Prime or Zoho, monthly MIS you can actually read, rolling "
     "cash-flow forecasts and a compliance calendar we own &mdash; on a monthly retainer.",
     ("virtual-cfo-services-bhopal.html", "Virtual CFO services"), "images/2052.jpg"),

    ("NRI taxation",
     "Section 195 &middot; 15CA / 15CB &middot; DTAA",
     "Selling property", "from abroad?",
     "TDS under Section 195 applies to the whole sale price, not your gain. A lower deduction "
     "certificate obtained before the sale is what fixes that &mdash; afterwards it is only a "
     "refund claim.",
     ("nri-taxation-services-bhopal.html", "NRI services"), "images/1427.jpg"),
]



def hero():
    stats = "".join(
        '<div><span class="nc-stat-n"><span data-count="%s"%s>0</span>%s</span>'
        '<span class="nc-stat-l">%s</span></div>'
        % (n, ' data-count-plain' if plain else '', suf, label)
        for n, suf, label, plain in C.STATS)

    slides, dots = [], []
    for i, (name, eyebrow, l1, l2, lead, (href, label), photo) in enumerate(SLIDES):
        # Only the first slide carries the <h1>. The others use a styled <p>,
        # so the document keeps exactly one top-level heading no matter which
        # slide is showing.
        head = ("<h1>%s<br><span class=\"nc-shimmer\">%s</span></h1>" % (l1, l2)
                if i == 0 else
                "<p class=\"nc-h1\" style=\"margin:0 0 .6em\">%s<br>"
                "<span class=\"nc-shimmer\">%s</span></p>" % (l1, l2))

        slides.append("""<div class="nc-slide%s" role="group" aria-roledescription="slide"
     aria-label="%d of %d: %s">
  <span class="nc-slide-eyebrow">%s</span>
  %s
  <p class="nc-lead">%s</p>
  <div class="nc-hero-btns">
    <a class="nc-btn nc-btn-lg" href="%s" data-open-modal="ncConsultModal">Book a consultation</a>
    <a class="nc-btn nc-btn-ghost nc-btn-lg nc-hero-btn-enq" href="#quick-enquiry" data-open-modal="ncConsultModal"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="margin-right:5px"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>Send Enquiry</a>
    <a class="nc-btn nc-btn-ghost nc-btn-lg" href="%s">%s <span class="nc-ar">&rarr;</span></a>
  </div>
</div>""" % (" is-on" if i == 0 else "", i + 1, len(SLIDES), name,
             eyebrow, head, lead, S.BOOK_URL, href, label))

        dots.append('<button class="nc-hero-dot" type="button" role="tab" '
                    'aria-selected="%s" tabindex="%d" aria-label="Show slide %d: %s"></button>'
                    % ("true" if i == 0 else "false", 0 if i == 0 else -1, i + 1, name))

    # Only the first photograph is requested up front. The other six carry
    # their URL in data-bg and nc.js loads each one just before its turn;
    # fetching all seven at once competed with the first for bandwidth and
    # delayed Largest Contentful Paint on phones.
    bgs = "".join(
        ('<figure class="is-on" style="background-image:url(&quot;%s&quot;)"></figure>' % s[6])
        if i == 0 else
        ('<figure data-bg="%s"></figure>' % s[6])
        for i, s in enumerate(SLIDES))

    arrow = lambda d, p: (
        '<button class="nc-hero-arrow" type="button" data-nc-slide="%s" aria-label="%s slide">'
        '<svg%s viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg></button>'
        % (d, "Previous" if d == "prev" else "Next", S.SVG_DIM, p))

    return """<section class="nc-hero" data-nc-paths>
  <div class="nc-hero-bg" aria-hidden="true">%s</div>
  <div class="nc-liquid" aria-hidden="true"><i></i><i></i><i></i></div>
  <div class="nc-hero-veil"></div>
  <div class="nc-grain"></div>

  <div class="nc-wrap nc-hero-in">
    <div class="nc-hero-copy" data-nc-rise>
      <div class="nc-slides" aria-roledescription="carousel" aria-label="What we do">%s</div>

      <div class="nc-hero-nav">
        <div class="nc-hero-dots" role="tablist" aria-label="Choose a slide">%s</div>
      </div>
    </div>

    <div class="nc-hero-stats" data-nc-rise style="--d:200ms">%s</div>
  </div>

  %s
  %s
</section>""" % (bgs, "".join(slides), "".join(dots), stats,
                  arrow("prev", '<polyline points="15 18 9 12 15 6"/>'),
                  arrow("next", '<polyline points="9 18 15 12 9 6"/>'))


def headline_services():
    cards = []
    for icon, title, blurb, href, cta in C.HEADLINE:
        cards.append("""<article class="nc-card nc-card-i nc-card-glow nc-svc" data-nc-rise>
  <span class="nc-svc-ico">%s</span>
  <h3>%s</h3>
  <p>%s</p>
  <a class="nc-alink" href="%s">%s <span class="nc-ar">&rarr;</span></a>
</article>""" % (S.ico(icon), title, blurb, href, cta))

    return """<section class="nc-sec">
  <div class="nc-wrap">
    %s
    <div class="nc-grid nc-g3">%s</div>
  </div>
</section>""" % (S.sec_head(
        "What we do",
        "Three practices, one accountable partner",
        "Most firms hand you to whoever is free. Here, one Chartered Accountant owns your "
        "file from the first reading of your papers through to the last hearing."),
        "".join(cards))


def about():
    checks = "".join("<li>%s</li>" % w for w in C.WHY)
    return """<section class="nc-sec nc-sec-alt" id="about">
  <div class="nc-wrap">
    <div class="nc-split">

      <div data-nc-rise="left">
        <div class="nc-media">
          <img src="images/279.jpg" alt="Chartered Accountants reviewing financial documents across a desk"
               loading="lazy" decoding="async" width="800" height="600">
          <div class="nc-media-badge">
            <img src="images/brand/team-natasha-480.webp" alt="CA Natasha Rajvaidya, FCA" loading="lazy" decoding="async" width="52" height="52" style="object-position:50%% 18%%">
            <span>
              <b>CA Natasha Rajvaidya</b>
              <span>FCA &middot; Founder</span>
            </span>
          </div>
        </div>
      </div>

      <div data-nc-rise="right">
        <span class="nc-eyebrow">About the firm</span>
        <h2>Bhopal&rsquo;s trusted CA firm, where quality is the standard</h2>
        <p>
          Established in 2017 in the financial hub of M.P. Nagar, <strong>Natasha &amp; Company</strong>
          is an ISO 9001:2015 certified Chartered Accountancy practice founded by
          <strong>CA Natasha Rajvaidya (FCA)</strong>. Over eight years we have earned the trust of
          more than 1,000 corporate clients, startups, high-net-worth individuals and institutions
          across Madhya Pradesh and overseas.
        </p>
        <p>
          We hold to ICAI ethical standards, accounting accuracy and prompt response. From complex
          GST summons and high-value scrutiny through to corporate structuring and contractor
          licensing, we protect your business at every milestone.
        </p>

        <ul class="nc-checks">%s</ul>

        <div class="nc-row">
          <a class="nc-btn" href="about-us.html">More about the firm</a>
          <a class="nc-alink" href="about-us.html#founder">Meet CA Natasha <span class="nc-ar">&rarr;</span></a>
        </div>
      </div>

    </div>
  </div>
</section>""" % checks


def practices():
    cards = [C.practice_card(*p) for p in C.PRACTICES]

    return """<section class="nc-sec" id="practices">
  <div class="nc-wrap">
    <div class="nc-center">%s</div>
    <div class="nc-grid nc-g3">%s</div>
  </div>
</section>""" % (S.sec_head(
        "Complete portfolio",
        "All 11 specialised practices",
        "From daily bookkeeping to tax litigation and government licensing &mdash; "
        "the full range of work this firm takes on.",
        center=True), "".join(cards))


def process():
    steps = []
    for i, (title, text) in enumerate(C.PROCESS, 1):
        steps.append("""<article class="nc-card nc-card-i nc-svc" data-nc-rise>
  <span class="nc-num">0%d</span>
  <h3 style="font-size:1.16rem">%s</h3>
  <p style="margin-bottom:0">%s</p>
</article>""" % (i, title, text))

    return """<section class="nc-sec nc-sec-alt">
  <div class="nc-wrap">
    %s
    <div class="nc-grid nc-g4">%s</div>
  </div>
</section>""" % (S.sec_head(
        "How we work",
        "No surprises, at any stage",
        "The same four steps whether it is a single ITR or a five-year GST demand."),
        "".join(steps))


def insights():
    posts = C.articles()[:3]
    if not posts:
        return ""
    cards = "".join(C.post_card(a) for a in posts)
    return """<section class="nc-sec">
  <div class="nc-wrap">
    <div class="nc-row" style="justify-content:space-between;align-items:flex-end;gap:2rem">
      %s
      <a class="nc-btn nc-btn-ghost" href="blog.html" style="margin-bottom:clamp(2.25rem,4.5vw,3.5rem)">
        All insights <span class="nc-ar">&rarr;</span>
      </a>
    </div>
    <div class="nc-grid nc-g3">%s</div>
  </div>
</section>""" % (S.sec_head(
        "Insights",
        "Notes on what just changed",
        "Deadlines, amendments and notices &mdash; written for business owners, not for other accountants."),
        cards)


import _team as T


def reviews():
    """Client testimonials.

    These are the Google reviews the aggregateRating in our schema refers to.
    Google expects the ratings it reads in structured data to be visible on the
    page, so this section is what makes that markup legitimate rather than a
    claim with nothing behind it.
    """
    import json
    revs = json.load(io.open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "_reviews.json"),
        encoding="utf-8"))

    stars = ('<span style="color:var(--nc-acc);letter-spacing:.12em;font-size:.9rem" '
             'aria-label="Rated 5 out of 5">&#9733;&#9733;&#9733;&#9733;&#9733;</span>')

    # No data-nc-rise on the cards: they sit in a horizontally scrolling track,
    # so the ones off to the right are clipped, never intersect, and would stay
    # invisible. The section itself carries the reveal instead.
    cards = "".join("""<figure class="nc-card nc-card-i nc-rev" style="margin:0">
  <div class="nc-row" style="justify-content:space-between;margin-bottom:1rem">
    %s
    <span style="font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--nc-ink-4)">Google review</span>
  </div>
  <blockquote style="margin:0 0 1.25rem;padding:0;border:0;background:none;font-family:var(--nc-body);font-style:normal;font-size:.985rem;line-height:1.68;color:var(--nc-ink-2);flex:1 1 auto">
    &ldquo;%s&rdquo;
  </blockquote>
  <figcaption style="margin:0;text-align:left;font-size:.9rem;color:var(--nc-pri);font-weight:600">%s</figcaption>
</figure>""" % (stars, r["text"], r["name"]) for r in revs)

    arrow = ('<button class="nc-revs-arrow nc-revs-%s" type="button" data-nc-slide="%s" '
             'aria-label="%s reviews">%s</button>')

    return """<section class="nc-sec" id="reviews">
  <div class="nc-wrap">
    <div class="nc-center">%s</div>

    <div class="nc-revs" data-nc-slider data-nc-rise>
      <div class="nc-revs-track" tabindex="0" role="group" aria-label="Client reviews, scrollable">%s</div>
      %s
      %s
      <div class="nc-revs-dots" role="tablist" aria-label="Review pages"></div>
    </div>

    <p class="nc-center nc-mt2" style="color:var(--nc-ink-4);font-size:.87rem">
      Rated <strong style="color:var(--nc-pri)">%s out of 5</strong> across
      <strong style="color:var(--nc-pri)">%s</strong> Google reviews &mdash;
      <a href="%s" target="_blank" rel="noopener">read them all on Google</a>.
    </p>
  </div>
</section>""" % (S.sec_head(
        "Client reviews",
        "What clients across Bhopal and overseas say",
        "Verified Google reviews, unedited.", center=True),
        cards,
        arrow % ("prev", "prev", "Previous", S.ico("arrow", cls="nc-flip")),
        arrow % ("next", "next", "Next", S.ico("arrow")),
        S.RATING, S.REVIEW_COUNT, S.REVIEWS_URL)


def team():
    return T.section()



def news_panels():
    """News / due dates / blog, three auto-scrolling panels over a photograph.

    Each list is rendered twice and the track is translated by half its height,
    which makes the loop seamless. Hovering pauses it, as the firm's earlier
    "elevator" feed did.
    """
    import json
    cd = json.load(io.open(os.path.join(ROOT, "data", "compliance-data.json"),
                           encoding="utf-8"))

    def ticker(items, height, seconds):
        """items already rendered; duplicated once for the seamless loop."""
        body = "".join(items)
        return ('<div class="nc-ticker" style="--nc-ticker-h:%dpx;--nc-ticker-s:%ds">'
                '<div class="nc-ticker-track"><div>%s</div><div aria-hidden="true">%s</div>'
                '</div></div>' % (height, seconds, body, body))

    news = ["""<div class="nc-panel-item">
  <span class="nc-when">%s</span>
  <a href="%s">%s</a>
</div>""" % (n.get("tag", "Update"), n.get("link", "blog.html"), n.get("title", ""))
            for n in cd.get("latest_news", [])]

    dues = ["""<div class="nc-panel-item">
  <span class="nc-when">%s</span>
  <p>%s</p>
</div>""" % (d.get("due", ""), d.get("title", ""))
            for d in cd.get("due_dates", [])]

    posts = C.articles()[:6]
    blog = ["""<div class="nc-panel-item">
  <time datetime="%s">%s</time>
  <a href="%s">%s</a>
</div>""" % (a["date"], C.nice_date(a["date"]), a["slug"], a["title"][:88])
            for a in posts]

    return """<section class="nc-sec nc-parallax">
  <div class="nc-parallax-bg" style="background-image:url(&quot;images/finance-1-1536x1024.jpg&quot;)" aria-hidden="true"></div>
  <div class="nc-wrap">
    <div class="nc-center">%s</div>
    <div class="nc-grid nc-g3">

      <div class="nc-panel">
        <div class="nc-panel-head">News &amp; Updates <span class="nc-live">Live</span></div>
        <div class="nc-panel-body">
          %s
          <a class="nc-btn nc-btn-full nc-mt2" href="blog.html">All updates</a>
        </div>
      </div>

      <div class="nc-panel">
        <div class="nc-panel-head">Due Date Reminder <span class="nc-live">Live</span></div>
        <div class="nc-panel-body">
          %s
          <a class="nc-btn nc-btn-full nc-mt2" href="knowledge-base.html#due-dates">Full calendar</a>
        </div>
      </div>

      <div class="nc-panel">
        <div class="nc-panel-head">From the Blog</div>
        <div class="nc-panel-body">
          %s
          <a class="nc-btn nc-btn-full nc-mt2" href="blog.html">Read the blog</a>
        </div>
      </div>

    </div>
    <p class="nc-center nc-mt2" style="color:#B9CBE0;font-size:.85rem">
      Feeds scroll automatically &mdash; hover to pause and read.
    </p>
  </div>
</section>""" % (S.sec_head("Stay current",
                            "News, Due Dates and Blog",
                            "What changed this month, what is due next, and what we have "
                            "written about it.", center=True),
                 ticker(news, 330, 30),
                 ticker(dues, 330, 34),
                 ticker(blog, 330, 38))



def get_in_touch():
    """Enquiry form on the home page.

    The reference closes its home page with the form itself rather than a link
    to a contact page, which removes a click from the only action that matters.
    Same form and the same data-lead hook, so entries reach the sheet.
    """
    subjects = ["GST notice or litigation", "Income tax notice or scrutiny",
                "Tax audit u/s 44AB", "ITR filing", "Company / LLP registration",
                "Virtual CFO / accounting", "NRI taxation", "Something else"]

    return """<section class="nc-sec nc-sec-alt" id="get-in-touch">
  <div class="nc-wrap">
    <div class="nc-center">{head}</div>
    <div class="nc-split" style="align-items:start">

      <div>
        <div class="nc-stack" style="gap:.85rem">
          <a class="nc-ctile" href="tel:{phone}">
            <span class="nc-svc-ico">{ph}</span>
            <span class="nc-ctile-t"><small>Direct line</small><b>{phone_d}</b></span>
          </a>
          <a class="nc-ctile" href="https://wa.me/919407000157" target="_blank" rel="noopener">
            <span class="nc-svc-ico">{wa}</span>
            <span class="nc-ctile-t"><small>WhatsApp</small><b>Send us the notice</b></span>
          </a>
          <a class="nc-ctile" href="mailto:{email}">
            <span class="nc-svc-ico">{ml}</span>
            <span class="nc-ctile-t"><small>Email</small><b>{email}</b></span>
          </a>
          <div class="nc-ctile">
            <span class="nc-svc-ico">{pin}</span>
            <span class="nc-ctile-t"><small>Office</small><b>195-A, 2nd Floor, Zone-1, M.P. Nagar, Bhopal 462011</b></span>
          </div>
          <div class="nc-ctile">
            <span class="nc-svc-ico">{clk}</span>
            <span class="nc-ctile-t"><small>Hours</small><b>Mon&ndash;Sat, 10:00&ndash;19:00 IST</b></span>
          </div>
        </div>
      </div>

      <div class="nc-card">
        <form class="nc-form nc-form-2" data-lead="home-enquiry" data-nc-contact
              action="#" method="post" novalidate>
          <div class="nc-field">
            <label for="h-name">Name <span class="req">*</span></label>
            <input class="nc-input" id="h-name" name="name" type="text" required
                   autocomplete="name" placeholder="Your full name">
          </div>
          <div class="nc-field">
            <label for="h-phone">Phone <span class="req">*</span></label>
            <input class="nc-input" id="h-phone" name="phone" type="tel" required
                   autocomplete="tel" inputmode="tel" placeholder="+91 ">
          </div>
          <div class="nc-field nc-field-full">
            <label for="h-subject">What is this about? <span class="req">*</span></label>
            <select class="nc-select" id="h-subject" name="subject" required>
              <option value="">Select a topic</option>
              {subjects}
            </select>
          </div>
          <div class="nc-field nc-field-full">
            <label for="h-msg">Details <span class="req">*</span></label>
            <textarea class="nc-textarea" id="h-msg" name="message" required
                      placeholder="Section and assessment year if it is a notice, or just describe the situation."></textarea>
          </div>
          <div class="nc-field nc-field-full">
            <div class="nc-fstat" role="status" aria-live="polite"></div>
            <button class="nc-btn nc-btn-full nc-btn-lg" type="submit">Send enquiry</button>
            <p class="nc-form-note" style="margin-top:.85rem">
              Same working day reply. See our <a href="privacy-policy.html">privacy policy</a>.
            </p>
          </div>
        </form>
      </div>

      <!-- Interactive Office Map & Directions Showcase (Side-by-Side, Zero Overlap) -->
      <div class="nc-map-container" data-nc-rise style="display:grid;grid-template-columns:repeat(auto-fit, minmax(340px, 1fr));align-items:stretch;position:relative;width:100%;border-radius:20px;overflow:hidden;box-shadow:0 20px 50px rgba(14, 75, 140, 0.12);border:1px solid var(--nc-line);background:var(--nc-surface);grid-column:1 / -1;margin-top:2.5rem">
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
              <span style="color:var(--nc-pri);margin-top:.15rem;flex-shrink:0">{pin}</span>
              <span><strong>195-A, 2nd Floor, Zone-1</strong>, M.P. Nagar, Bhopal 462011 (In front of DB City Mall area)</span>
            </div>
            <div style="display:flex;align-items:center;gap:.6rem">
              <span style="color:var(--nc-pri);flex-shrink:0">{ph}</span>
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

        <div class="nc-map-iframe-wrap">
          <iframe title="Natasha &amp; Company office location, Zone-1 M.P. Nagar, Bhopal"
                  src="{map_src}"
                  loading="lazy" referrerpolicy="no-referrer-when-downgrade"
                  allowfullscreen></iframe>
        </div>
      </div>

    </div>
  </div>
</section>""".format(
        head=S.sec_head("Get in touch", "Talk to a Chartered Accountant",
                        "One call is usually enough to tell you where you stand, what it "
                        "will cost, and what happens next.", center=True),
        subjects="".join('<option>%s</option>' % s for s in subjects),
        phone=S.PHONE, phone_d=S.PHONE_DISPLAY, email=S.EMAIL,
        ph=S.ico("phone"), ml=S.ico("mail"), pin=S.ico("pin"),
        clk=S.ico("clock"), wa=S.social("wa"),
        map_src="https://www.google.com/maps?q=NATASHA%20%26%20Co.%20CA%20in%20Bhopal%2C%20195-A%2C%20Zone-1%2C%20M.P.%20Nagar%2C%20Bhopal%20462011&hl=en&z=16&output=embed",
        directions_url="https://www.google.com/maps/dir/?api=1&destination=NATASHA+%26+Co.+CA+in+Bhopal%2C+195-A%2C+Zone-1%2C+M.P.+Nagar%2C+Bhopal+462011",
        reviews_url=S.REVIEWS_URL,
        rating=S.RATING,
        reviews=S.REVIEW_COUNT)


def faq():
    items = "".join(
        '<details><summary>%s</summary><div class="nc-faq-a"><p>%s</p></div></details>' % (q, a)
        for q, a in C.HOME_FAQ)
    return """<section class="nc-sec nc-sec-alt" id="faq">
  <div class="nc-wrap nc-wrap-nar">
    %s
    <div class="nc-faq" data-nc-rise>%s</div>
  </div>
</section>""" % (S.sec_head(
        "Common questions",
        "Straight answers, before you call"), items)


def build():
    body = "\n\n".join([
        hero(), S.marquee(), headline_services(), about(), practices(),
        process(), news_panels(), reviews(), team(), insights(), faq(),
        get_in_touch(),
    ])

    schema = S.ld(
        S.org_schema(),
        S.website_schema(),
        S.faq_schema(C.HOME_FAQ),
    )

    first = S.webp_refs(" " + SLIDES[0][6] + " ").strip()   # padded: the pattern needs a boundary
    doc = S.page(title=TITLE, desc=DESC, slug="index.html", body=body, schema=schema,
                 extra_css='\n<link rel="preload" as="image" href="%s" fetchpriority="high">' % first)
    with io.open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(doc)
    print("built index.html (%d KB)" % (len(doc) // 1024))


if __name__ == "__main__":
    build()
