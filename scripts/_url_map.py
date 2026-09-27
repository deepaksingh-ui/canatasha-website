# -*- coding: utf-8 -*-
"""
Old URL -> new URL, for the move from WordPress to this static site.

www.canatasha.com is WordPress today. Its URLs are /slug/ with a trailing
slash; this site serves /slug.html. Without a permanent redirect for each one,
every page Google has indexed (and every link anyone has shared) turns into a
404 on launch day and its ranking is lost.

The inventory is the live site's own sitemap, saved in
wp_snapshot/_live_urls.tsv (94 URLs). `resolve()` must return a destination
for every one of them, and every destination must be a file that exists;
`check()` enforces both and the build fails otherwise.
"""
import io
import os
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Pages whose slug differs, or that were merged into a stronger page.
EXPLICIT = {
    # identical intent, the new page is the deeper one
    "tax-audit": "tax-audit-44ab-bhopal.html",
    "gst-appeals": "gst-notice-consultant-bhopal.html",
    "income-tax-appeals-tribunals": "income-tax-notice-consultant-bhopal.html",
    # empty on WordPress ("No data...", "Coming soon.") -> nearest real page
    "pasara-security-license": "psara-pwd-contractor-registration-madhya-pradesh.html",
    "pf-fund-appeals": "labour-law-compliances.html",
    "mining-project-reports": "services.html",
    # theme placeholder pages (lorem ipsum) -> the real equivalents
    "training": "career.html",
    "about": "about-us.html",
    # core pages
    "services": "services.html",
    "about-us": "about-us.html",
    "contact-us": "contact-us.html",
    "blog": "blog.html",
    "career": "career.html",
    "job-openings": "career.html",
    "terms-and-conditions": "terms-and-conditions.html",
    "privacy-policy": "privacy-policy.html",
    # posts whose WordPress slug carried an emoji or a rupee sign
    "maha-kumbh-mela-2025-a-spiritual-and-economic-marvel\U0001f549️":
        "maha-kumbh-mela-2025-a-spiritual-and-economic-marvel.html",
    "madhya-pradeshs-giant-leap-₹26-61-lakh-crore-investment-inflow-from-gis-2025":
        "madhya-pradesh-26-61-lakh-crore-investment-inflow-gis-2025.html",
}

# Whole WordPress sections with no one-to-one page here.
PREFIXES = [
    ("category/", "blog.html"),
    ("tag/", "blog.html"),
    ("author/ashish", "about-us.html"),
    ("author/", "about-us.html"),
    ("job-category/", "career.html"),
    ("job-type/", "career.html"),
    ("job-location/", "career.html"),
    ("https-www-canatasha-com-career/", "career.html"),
]

# WordPress system URLs that crawlers and feed readers still request.
SYSTEM = [
    ("wp-sitemap.xml", "sitemap.xml"),
    ("feed", "blog.html"),
    ("comments/feed", "blog.html"),
]


def live_urls():
    rows = []
    for line in io.open(os.path.join(HERE, "wp_snapshot", "_live_urls.tsv"), encoding="utf-8"):
        line = line.strip()
        if line:
            rows.append(line.split("\t")[-1])
    return rows


def path_of(url):
    return urllib.parse.unquote(urllib.parse.urlparse(url).path).strip("/")


def resolve(path):
    """'bank-audit' -> 'bank-audit.html' (a file in ROOT), or None."""
    if path == "":
        return ""                                   # home
    if path in EXPLICIT:
        return EXPLICIT[path]
    for pre, dest in PREFIXES:
        if path.startswith(pre):
            return dest
    if os.path.exists(os.path.join(ROOT, path + ".html")):
        return path + ".html"
    return None


def rules():
    """[(source_path_without_slashes, destination_file)] for every live URL."""
    out, seen = [], set()
    for url in live_urls():
        p = path_of(url)
        if p == "" or p in seen:
            continue
        seen.add(p)
        out.append((p, resolve(p)))
    for src, dest in SYSTEM:
        out.append((src, dest))
    return out


def check():
    missing, broken = [], []
    for src, dest in rules():
        if dest is None:
            missing.append(src)
        elif dest and not os.path.exists(os.path.join(ROOT, dest.split("#")[0])):
            broken.append((src, dest))
    return missing, broken


def encoded(path):
    """Percent-encode the way a browser sends it (emoji and rupee-sign slugs)."""
    return urllib.parse.quote(path, safe="/-_.~")


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    m, b = check()
    for src, dest in rules():
        print("  /%-70s -> /%s" % ((src + "/")[:70], dest))
    print("\n%d rules, %d unmapped, %d broken destinations" % (len(rules()), len(m), len(b)))
