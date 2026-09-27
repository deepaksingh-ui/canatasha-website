# -*- coding: utf-8 -*-
"""
Package the built site for the client. Run after `python scripts/build.py`.

    python scripts/package_client.py

Writes to ../client-docs/ (outside the site folder, so it never deploys):

  canatasha-website-upload.zip
      The launch file. Everything .vercelignore excludes is left out; keeps
      .htaccess (301 map, https + www) for the current cPanel host.

  canatasha-PREVIEW-sirf-dikhane-ke-liye.zip
      For showing the client on a temporary address before launch. No
      redirects to www.canatasha.com, and every page is marked noindex
      (.htaccess header, _headers for Netlify / Cloudflare Pages, and a
      Disallow-all robots.txt), so the preview never competes with the live site.
"""
import fnmatch
import io
import os
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
OUT = os.path.join(os.path.dirname(SITE), "client-docs")

EXTRA_IGNORE = ["LEAD-CAPTURE-SETUP.md", ".vercelignore", "vercel.json",
                "*.pyc", "__pycache__/", ".git/", "node_modules/"]

PREVIEW_HTACCESS = """# PREVIEW ONLY - for showing the client. Not the launch file.
# No redirects to www.canatasha.com, and search engines are told not to index it.
Options -Indexes
DirectoryIndex index.html
ErrorDocument 404 /404.html
<IfModule mod_headers.c>
  Header always set X-Robots-Tag "noindex, nofollow"
</IfModule>
"""


def ignore_patterns():
    pats = []
    for line in io.open(os.path.join(SITE, ".vercelignore"), encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#"):
            pats.append(line)
    return pats + EXTRA_IGNORE


def skipped(rel, pats):
    parts = rel.split("/")
    for pat in pats:
        if pat.endswith("/"):
            if pat[:-1] in parts[:-1]:
                return True
        elif fnmatch.fnmatch(parts[-1], pat) or fnmatch.fnmatch(rel, pat):
            return True
    return False


def site_files():
    pats = ignore_patterns()
    for root, dirs, files in os.walk(SITE):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, SITE).replace("\\", "/")
            if not skipped(rel, pats):
                yield full, rel


def main():
    os.makedirs(OUT, exist_ok=True)
    files = list(site_files())

    launch = os.path.join(OUT, "canatasha-website-upload.zip")
    with zipfile.ZipFile(launch, "w", zipfile.ZIP_DEFLATED) as z:
        for full, rel in files:
            z.write(full, rel)

    preview = os.path.join(OUT, "canatasha-PREVIEW-sirf-dikhane-ke-liye.zip")
    with zipfile.ZipFile(preview, "w", zipfile.ZIP_DEFLATED) as z:
        for full, rel in files:
            if rel in (".htaccess", "robots.txt", "sitemap.xml", "llms.txt"):
                continue
            z.write(full, rel)
        z.writestr(".htaccess", PREVIEW_HTACCESS)
        z.writestr("robots.txt", "User-agent: *\nDisallow: /\n")
        z.writestr("_headers", "/*\n  X-Robots-Tag: noindex, nofollow\n")

    names = set(zipfile.ZipFile(launch).namelist())
    leaked = [n for n in names if n.startswith(("backup/", "scripts/")) or n.endswith(".py")]
    assert not leaked, leaked
    assert {".htaccess", "index.html", "sitemap.xml"} <= names
    for path in (launch, preview):
        print("  %-48s %5.1f MB" % (os.path.basename(path), os.path.getsize(path) / 1048576))


if __name__ == "__main__":
    main()
