"""Draw the orange numbered callouts onto real phone screenshots for the "Add to home screen" page.

The share sheet and Chrome menu belong to the phone, not the app, so Playwright can't capture them.
Take the screenshots on a real iPhone and Android phone, put them in phone-raw/ with the names below, then:

    python3 cap_install.py          # draw callouts, save WebP into delivery-tracker/img/
    python3 cap_install.py --grid   # write phone-raw/grid-*.png with a 10% grid, to read off positions

Positions are fractions of the screenshot (0 = left/top, 1 = right/bottom), so any phone size works.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "phone-raw")
OUT = os.path.join(HERE, "..", "..", "delivery-tracker", "img")
C = "#f97316"
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

# name: (raw file, crop (top, bottom) or None, [(box (x, y, w, h), number, side, extra options)])
SHOTS = {
    "install-iphone-share": ("iphone-1.png", None, [
        ((0.36, 0.62, 0.55, 0.05), 1, "top"),
    ]),
    "install-iphone-add": ("iphone-2.png", None, [
        ((0.04, 0.67, 0.92, 0.06), 1, "top"),
    ]),
    "install-iphone-confirm": ("iphone-3.png", (0, 0.45), [
        ((0.80, 0.095, 0.16, 0.045), 1, "bottom"),
    ]),
    "install-android-menu": ("android-1.png", None, [
        ((0.45, 0.73, 0.52, 0.05), 1, "left", {"dx": -40}),
    ]),
    "install-android-add": ("android-2.png", None, [
        ((0.71, 0.568, 0.11, 0.03), 1, "bottom"),
    ]),
    "install-android-confirm": ("android-3.png", None, [
        ((0.60, 0.62, 0.28, 0.04), 1, "bottom"),
    ]),
}

def draw(img, items):
    """Same look as annot.py: rounded box, arrow, white-ringed badge. Sizes are in CSS px (390 wide)."""
    W, H = img.size
    s = W / 390
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT, round(16 * s))
    for it in items:
        (fx, fy, fw, fh), n, side = it[0], it[1], it[2]
        o = it[3] if len(it) > 3 else {}
        x, y, w, h = fx * W, fy * H, fw * W, fh * H
        pad, dist, R, lw = 4 * s, o.get("dist", 56) * s, 15 * s, round(3 * s)
        if not o.get("noBox"):
            d.rounded_rectangle([x - pad, y - pad, x + w + pad, y + h + pad], radius=8 * s, outline=C, width=lw)
        cx, cy = x + w / 2, y + h / 2
        bx, by, tx, ty = {
            "left":   (x - pad - dist, cy, x - pad - 3 * s, cy),
            "right":  (x + w + pad + dist, cy, x + w + pad + 3 * s, cy),
            "top":    (cx, y - pad - dist, cx, y - pad - 3 * s),
            "bottom": (cx, y + h + pad + dist, cx, y + h + pad + 3 * s),
        }[side]
        bx += o.get("dx", 0) * s; by += o.get("dy", 0) * s
        length = max(((tx - bx) ** 2 + (ty - by) ** 2) ** 0.5, 1)
        ux, uy = (tx - bx) / length, (ty - by) / length
        if length > R + 6 * s:
            head = 10 * s
            d.line([bx + ux * R, by + uy * R, tx - ux * head * 0.6, ty - uy * head * 0.6], fill=C, width=lw)
            d.polygon([(tx, ty), (tx - ux * head - uy * head * 0.6, ty - uy * head + ux * head * 0.6),
                       (tx - ux * head + uy * head * 0.6, ty - uy * head - ux * head * 0.6)], fill=C)
        d.ellipse([bx - R - 3 * s, by - R - 3 * s, bx + R + 3 * s, by + R + 3 * s], fill="white")
        d.ellipse([bx - R, by - R, bx + R, by + R], fill=C)
        d.text((bx, by), str(n), fill="white", font=font, anchor="mm")

def grid(path):
    img = Image.open(path).convert("RGB")
    W, H = img.size
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT, W // 30)
    for i in range(1, 10):
        d.line([W * i / 10, 0, W * i / 10, H], fill="red", width=2)
        d.line([0, H * i / 10, W, H * i / 10], fill="red", width=2)
        d.text((W * i / 10 + 4, 4), f".{i}", fill="red", font=font)
        d.text((4, H * i / 10 + 4), f".{i}", fill="red", font=font)
    img.save(os.path.join(RAW, "grid-" + os.path.basename(path)))

if __name__ == "__main__":
    for name, (raw, crop, items) in SHOTS.items():
        path = os.path.join(RAW, raw)
        if not os.path.exists(path):
            print("missing:", raw); continue
        if "--grid" in sys.argv:
            grid(path); continue
        img = Image.open(path).convert("RGB")
        draw(img, items)
        if crop:
            img = img.crop((0, round(crop[0] * img.height), img.width, round(crop[1] * img.height)))
        img = img.resize((780, round(img.height * 780 / img.width)), Image.LANCZOS)  # 390 CSS px at 2x, like the other shots
        img.save(os.path.join(OUT, name + ".webp"), "WEBP", quality=82, method=6)
        print("webp:", name)
