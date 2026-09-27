"""The firm's people — one list, used by the homepage and the About page.

Photographs come from scripts/brand_src/team-<key>.jpeg via build_brand.py.

Only publish what the firm has confirmed. Names and credentials on a CA firm's
site are statements a regulator and a client can both rely on, so anything
still to be confirmed is marked `confirm=True` and kept out of structured data.
"""
import nc_shell as S

TEAM = [
    dict(
        key="natasha",
        name="CA Natasha Rajvaidya",
        tag="Founder &middot; FCA",
        role="Founder &amp; Managing Partner",
        job="Founder & Managing Partner",
        bio=("Fellow Chartered Accountant leading the firm&rsquo;s tax audit, GST litigation "
             "and corporate advisory practice since founding it in 2017. Direct tax planning, "
             "statutory audit and startup structuring."),
        schema_id="about-us.html#founder",
        confirm=False,
    ),
    dict(
        key="ashish",
        name="Ashish Gupta",
        tag="Taxation &amp; GST",
        role="Head &ndash; Taxation &amp; GST",
        job="Head of Taxation & GST",
        bio=("Leads the firm&rsquo;s income tax and GST practice: returns, notices, scrutiny "
             "replies and appeals, and advice for non-resident Indians on their tax position "
             "in India."),
        schema_id="about-us.html#ashish-gupta",
        confirm=False,
    ),
    dict(
        key="vk",
        name="VK Gupta",
        tag="Audit &amp; Secretarial",
        role="Head &ndash; Audit &amp; Secretarial",
        job="Head of Audit & Secretarial",
        bio=("Leads statutory, tax and internal audits, and the company secretarial work "
             "that goes with them: ROC filings and annual compliance for companies and LLPs."),
        schema_id="about-us.html#vk-gupta",
        confirm=False,   # name and role confirmed by the firm, 2026-09-14
    ),
]


def _first(name):
    parts = name.replace("CA ", "").split()
    return parts[0] if parts else name


def photo_img(m, sizes="(max-width: 700px) 92vw, 420px", eager=False, cls=""):
    k = m["key"]
    return ('<img%s src="images/brand/team-%s-800.webp" '
            'srcset="images/brand/team-%s-480.webp 480w, images/brand/team-%s-800.webp 800w" '
            'sizes="%s" alt="%s, %s" width="800" height="1000" %s decoding="async">'
            % (' class="%s"' % cls if cls else "", k, k, k, sizes, m["name"],
               m["role"].replace("&middot;", "&ndash;").replace("Head &ndash; ", "Head of "),
               'fetchpriority="high"' if eager else 'loading="lazy"'))


def cards_html():
    out = []
    for i, m in enumerate(TEAM):
        out.append("""<article class="nc-pcard nc-team" data-nc-rise style="--nc-i:%d" tabindex="-1">
  <div class="nc-team-photo">
    %s
    <span class="nc-team-tag">%s</span>
    <div class="nc-team-over">
      <p>%s</p>
      <a class="nc-team-cta" href="contact-us.html">Consult %s <span class="nc-ar">&rarr;</span></a>
    </div>
  </div>
  <div class="nc-team-body">
    <h3>%s</h3>
    <p class="nc-team-role">%s</p>
  </div>
</article>""" % (i, photo_img(m), m["tag"], m["bio"], _first(m["name"]), m["name"], m["role"]))
    return "".join(out)


def section(alt=True, head=None):
    head = head or S.sec_head(
        "The team",
        "Who actually works on your file",
        "The people who take your file from first review to final filing &mdash; "
        "not a call centre, and not a different face every year.",
        center=True)
    return """<section class="nc-sec%s" id="team">
  <div class="nc-wrap">
    <div class="nc-center">%s</div>
    <div class="nc-grid nc-g3 nc-team-grid">%s</div>
  </div>
</section>""" % (" nc-sec-alt" if alt else "", head, cards_html())


def person_schemas():
    """Person entities for confirmed members only."""
    import json
    out = []
    for m in TEAM:
        if m["confirm"] or not m["schema_id"]:
            continue
        if m["key"] == "natasha":
            continue            # the About page's richer founder entity covers her
        out.append(json.dumps({
            "@context": "https://schema.org",
            "@type": "Person",
            "@id": "%s/%s" % (S.SITE, m["schema_id"]),
            "name": m["name"],
            "jobTitle": m["job"],
            "image": "%s/images/brand/team-%s.jpg" % (S.SITE, m["key"]),
            "worksFor": {"@id": S.ORG_ID},
        }, indent=2))
    return out
