# -*- coding: utf-8 -*-
"""
Build the whole site.

    python scripts/build.py

Order matters: articles are generated first from the pre-redesign originals,
then the hand-authored pages, then the redirect stubs (which overwrite a few
of the article slugs), then config, which reads the finished pages to build
the sitemap and llms.txt. Everything reads from backup/pre-redesign-*, so
this is safe to re-run any number of times.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

STEPS = [
    ("build_images.py", "WebP versions of heavy images"),
    ("build_articles.py", "blog articles"),
    ("build_home.py", "home page"),
    ("build_pages.py", "about / services / contact / blog / career / KB / 404"),
    ("build_services.py", "service landing pages"),
    ("build_subservices.py", "service sub-pages"),
    ("build_wp_services.py", "service pages carried over from WordPress"),
    ("build_tools.py", "calculators"),
    ("build_legal.py", "privacy / terms"),
    ("build_redirects.py", "redirect stubs"),
    ("build_config.py", "vercel.json / sitemap / robots / llms.txt"),
]


def run(script, label):
    print("\n\033[1m-- %s\033[0m  (%s)" % (label, script))
    r = subprocess.run([sys.executable, os.path.join(HERE, script)],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    sys.stdout.write(r.stdout or "")
    if r.returncode != 0:
        sys.stderr.write(r.stderr or "")
        print("\n  BUILD FAILED at %s" % script)
        sys.exit(r.returncode)


def main():
    for script, label in STEPS:
        run(script, label)

    print("\n" + "=" * 62)
    r = subprocess.run([sys.executable, os.path.join(HERE, "validate.py")],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    sys.stdout.write(r.stdout or "")
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
