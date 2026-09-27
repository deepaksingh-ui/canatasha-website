# -*- coding: utf-8 -*-
"""Map which scroll effect the reference design applies to which section.

Research only — it reads the public page to understand the technique so the
same feel can be rebuilt here. Nothing from it is copied into the site.
"""
import collections
import io
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/tpl.html"
h = io.open(path, encoding="utf-8", errors="replace").read()

TOKEN = re.compile(
    r'data-aos="([a-z-]+)"'
    r'|<h[12][^>]*>(.*?)</h[12]>'
    r'|class="([^"]*(?:section|banner|service|footer|contact|news)[^"]*)"',
    re.S | re.I)

marks = []
for m in TOKEN.finditer(h):
    if m.group(1):
        marks.append(("AOS", m.group(1)))
    elif m.group(2):
        txt = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if txt:
            marks.append(("HEAD", txt[:46]))
    elif m.group(3):
        marks.append(("SEC", m.group(3).split()[0][:40]))

groups = collections.OrderedDict()
cur = "(page top)"
for kind, val in marks:
    if kind in ("HEAD", "SEC"):
        cur = val
    else:
        groups.setdefault(cur, []).append(val)

print("=== reference: which effect, in which block ===")
for sec, fx in groups.items():
    c = collections.Counter(fx)
    print("  %-44s %s" % (sec[:44], ", ".join("%s x%d" % kv for kv in c.items())))

print()
print("=== totals ===")
allfx = collections.Counter(v for k, v in marks if k == "AOS")
for k, v in allfx.most_common():
    print("  %-12s %d" % (k, v))
print("  %-12s %d" % ("TOTAL", sum(allfx.values())))
