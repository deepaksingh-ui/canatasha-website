# -*- coding: utf-8 -*-
"""
WebP versions of every heavy JPEG/PNG in images/.

Runs first in the build. For each .jpg/.jpeg/.png over 60 KB without a WebP
sibling, writes <name>.webp (quality 80, capped at 2000px wide, which still
covers a full-width hero). Existing WebP files are left alone.

nc_shell.page() then points every local image reference in the page body at
the WebP when one exists. Share images in <head> stay JPEG: several chat apps
still fail to preview WebP.
"""
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES = os.path.join(ROOT, "images")
MIN_BYTES = 60 * 1024
MAX_W = 2000


def main():
    made, before, after = 0, 0, 0
    for dirpath, _, files in os.walk(IMAGES):
        for f in files:
            stem, ext = os.path.splitext(f)
            if ext.lower() not in (".jpg", ".jpeg", ".png"):
                continue
            src = os.path.join(dirpath, f)
            dst = os.path.join(dirpath, stem + ".webp")
            if os.path.exists(dst) or os.path.getsize(src) < MIN_BYTES:
                continue
            im = Image.open(src)
            im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
            if im.width > MAX_W:
                im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
            im.save(dst, "WEBP", quality=80, method=6)
            made += 1
            before += os.path.getsize(src)
            after += os.path.getsize(dst)
    if made:
        print("  %d WebP files written: %.1f MB -> %.1f MB"
              % (made, before / 1048576, after / 1048576))
    else:
        print("  all heavy images already have WebP versions")


if __name__ == "__main__":
    main()
