"""Brand assets from the client's own files.

Reads scripts/brand_src/ (the logo and team photographs as supplied) and writes
web-ready versions into images/brand/. Idempotent: rerun after replacing any
source file.

    logo-horizontal  -> header logo, transparent (light grounds)
                        + white variant (the navy footer)
    logo-round       -> the CA mark alone -> favicon, app icons
    logo-stacked     -> transparent, for the about page and print
    team-*           -> 4:5 portraits, WebP 480w/800w + JPEG fallback
    og-card          -> 1200x630 share image built from the horizontal logo

Why not use the files directly: the horizontal logo sits on a grey gradient
with a generator watermark in one corner, all three are JPEG (no transparency),
and the blue wordmark disappears on the footer's navy.
"""
import io
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, "brand_src")
OUT = os.path.join(ROOT, "images", "brand")

NAVY = (10, 36, 64)


# --------------------------------------------------------------------------
# background -> alpha
# --------------------------------------------------------------------------
def estimate_background(rgb):
    """Per-pixel background colour, for grounds that are a gradient.

    Normalised convolution: blur only the pixels that look like background
    (bright and grey), then divide by the blurred mask. Foreground holes are
    filled from their surroundings.
    """
    a = rgb.astype(np.float32)
    lum = a.mean(axis=2)
    sat = a.max(axis=2) - a.min(axis=2)
    mask = ((lum > 212) & (sat < 22)).astype(np.float32)

    def blur(ch):
        # PIL cannot blur float images; scipy keeps the precision the
        # division below needs.
        from scipy.ndimage import gaussian_filter
        return gaussian_filter(ch, sigma=48, mode="nearest")

    m = blur(mask) + 1e-4
    bg = np.stack([blur(a[..., c] * mask) / m for c in range(3)], axis=2)
    return np.clip(bg, 1, 255)


def color_to_alpha(rgb, bg, floor=0.16):
    """GIMP's colour-to-alpha against a (per-pixel) background.

    Antialiased edges keep their true colour instead of a pale halo, which is
    what a plain threshold would leave on a dark footer.
    """
    c = rgb.astype(np.float32)
    # Only ink DARKER than the ground counts. Measuring brighter pixels too
    # divides by (255 - bg), which on a 240 ground is 15: a five-level JPEG
    # ripple became 33% opaque, and the watermark sparkle (brighter than the
    # ground) survived. Every part of this mark is darker than its ground.
    alpha = np.clip(((bg - c) / bg).max(axis=2), 0, 1)

    # Colour comes from the RAW alpha, so ink composites back to exactly the
    # supplied colour. Rescaling alpha first made the pale sage "& COMPANY"
    # lighter and bluer and dropped half its pixels.
    safe = np.maximum(alpha, 1e-4)[..., None]
    col = (c - bg * (1 - alpha[..., None])) / safe
    col = np.clip(col, 0, 255)

    # Then discard what is too faint to be ink: gradient noise, JPEG ripple.
    # A soft knee rather than a cliff keeps antialiased edges smooth.
    knee = floor * 0.5
    alpha = np.where(alpha < knee, 0,
                     np.where(alpha < floor, (alpha - knee) / (floor - knee) * floor, alpha))
    out = np.dstack([col, alpha * 255]).astype(np.uint8)
    out[alpha == 0] = 0
    return Image.fromarray(out, "RGBA")


def trim(img, pad=0.02):
    a = np.asarray(img)[..., 3]
    ys, xs = np.where(a > 24)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    p = int(max(x1 - x0, y1 - y0) * pad)
    return img.crop((max(0, x0 - p), max(0, y0 - p),
                     min(img.width, x1 + p + 1), min(img.height, y1 + p + 1)))


def to_white(img):
    """Blue parts of the mark -> white; the orange and green stay brand."""
    a = np.asarray(img).copy()
    r, g, b = (a[..., i].astype(int) for i in range(3))
    alpha = a[..., 3].astype(np.float32)

    # Blue and navy -> white.
    sel = (b > r + 20) & (b > g - 25) & (g < 150)
    a[sel, 0:3] = 255

    # The sage "& COMPANY" is so light that colour-to-alpha leaves it about
    # 20% opaque: fine over white, gone over navy. Restore its opacity and
    # lift it to a green that holds on the dark ground.
    green = (g > r + 8) & (g > b + 8) & (alpha > 0) & ~sel
    a[green, 0:3] = (164, 214, 122)
    a[green, 3] = np.clip(alpha[green] * 4.2, 0, 255).astype(np.uint8)
    return Image.fromarray(a, "RGBA")


def save_png_webp(img, name, width=None):
    if width and img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    img.save(os.path.join(OUT, name + ".png"), optimize=True)
    img.save(os.path.join(OUT, name + ".webp"), quality=92, method=6)
    return img


def load(name):
    return np.asarray(Image.open(os.path.join(SRC, name)).convert("RGB"))


# --------------------------------------------------------------------------
def logos():
    # Horizontal: gradient ground + watermark
    rgb = load("logo-horizontal.jpeg")
    horiz = trim(color_to_alpha(rgb, estimate_background(rgb)))
    h = save_png_webp(horiz, "logo-horizontal", width=900)
    save_png_webp(to_white(h), "logo-horizontal-white", width=520)
    save_png_webp(h, "logo-horizontal-520", width=520)   # header, 2x of ~260px

    # Stacked: plain white ground
    rgb = load("logo-stacked.jpeg")
    flat = np.full(rgb.shape, 255, np.float32)
    save_png_webp(trim(color_to_alpha(rgb, flat)), "logo-stacked", width=551)

    # Round -> the CA mark only (everything above the word INDIA, inside the ring)
    rgb = load("logo-round.jpeg")
    flat = np.full(rgb.shape, 255, np.float32)
    # Drop the black ring before cutting: it is the only near-black, grey ink
    # in the file, so it can be removed by colour rather than by a crop that
    # would have to guess where the arc crosses.
    a = rgb.astype(int)
    ring = (a.max(axis=2) < 120) & ((a.max(axis=2) - a.min(axis=2)) < 40)
    rgb = rgb.copy(); rgb[ring] = 255
    full = color_to_alpha(rgb, flat)
    mark = trim(full.crop((120, 150, 940, 650)), pad=0.01)
    save_png_webp(mark, "ca-mark", width=700)
    return h, mark


def icons(mark):
    def tile(size, radius_ratio=0.22, inset=0.14):
        t = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(t)
        d.rounded_rectangle((0, 0, size - 1, size - 1),
                            radius=int(size * radius_ratio), fill=(255, 255, 255, 255))
        box = int(size * (1 - 2 * inset))
        m = mark.copy()
        m.thumbnail((box, box), Image.LANCZOS)
        t.alpha_composite(m, ((size - m.width) // 2, (size - m.height) // 2))
        return t

    for s in (512, 192, 180):
        name = "apple-touch-icon" if s == 180 else "icon-%d" % s
        img = tile(s)
        if s == 180:            # iOS draws its own corners; give it a full square
            img = Image.new("RGBA", (s, s), (255, 255, 255, 255))
            m = mark.copy(); m.thumbnail((int(s * .76),) * 2, Image.LANCZOS)
            img.alpha_composite(m, ((s - m.width) // 2, (s - m.height) // 2))
        img.save(os.path.join(OUT, name + ".png"), optimize=True)

    # Multi-size .ico at the site root, where browsers look without being told
    tile(256).save(os.path.join(ROOT, "favicon.ico"),
                   sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    tile(32, inset=0.06).save(os.path.join(OUT, "favicon-32.png"))


def og_card(horiz):
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    # a quiet brand band along the bottom
    d.rectangle((0, H - 150, W, H), fill=NAVY)
    d.rectangle((0, H - 156, W, H - 150), fill=(245, 130, 32))

    logo = horiz.copy()
    logo.thumbnail((900, 300), Image.LANCZOS)
    img.paste(logo, ((W - logo.width) // 2, (H - 156 - logo.height) // 2), logo)

    font = os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts", "segoeuib.ttf")
    try:
        f = ImageFont.truetype(font, 38)
    except OSError:
        f = ImageFont.load_default()
    line = "Chartered Accountants  \u00b7  M.P. Nagar, Bhopal  \u00b7  Since 2017"
    tw = d.textlength(line, font=f)
    d.text(((W - tw) / 2, H - 100), line, font=f, fill=(255, 255, 255))
    img.save(os.path.join(OUT, "og-card.jpg"), quality=90, optimize=True, progressive=True)


def portraits():
    for key in ("natasha", "ashish", "vk"):
        im = Image.open(os.path.join(SRC, "team-%s.jpeg" % key)).convert("RGB")
        # 4:5, anchored high so the face sits in the upper third on every card
        w, h = im.size
        tw, th = w, round(w * 5 / 4)
        if th > h:
            th, tw = h, round(h * 4 / 5)
        x0 = (w - tw) // 2
        crop = im.crop((x0, 0, x0 + tw, th))
        for width in (480, 800):
            r = crop.resize((width, width * 5 // 4), Image.LANCZOS)
            r.save(os.path.join(OUT, "team-%s-%d.webp" % (key, width)), quality=84, method=6)
        crop.resize((800, 1000), Image.LANCZOS).save(
            os.path.join(OUT, "team-%s.jpg" % key), quality=86, optimize=True, progressive=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    horiz, mark = logos()
    icons(mark)
    og_card(horiz)
    portraits()
    total = 0
    for f in sorted(os.listdir(OUT)):
        n = os.path.getsize(os.path.join(OUT, f))
        total += n
        print("  %-32s %7.1f KB" % (f, n / 1024))
    print("images/brand: %d files, %.0f KB" % (len(os.listdir(OUT)), total / 1024))


if __name__ == "__main__":
    main()
