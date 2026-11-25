# draw.py — renders entry.png (1024x1024) for
# "Convince the AI Judge to Visit Your House: A Letter in One Image".
# Local build tool only: the grader never runs it (main.ts is copy-only).
# Python 3 stdlib + Pillow. Deterministic: no randomness, no timestamps.
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "entry.png"

# ---------- palette ----------
BG = (30, 61, 47)          # deep green backdrop
BG_DOT = (38, 76, 58)      # subtle pattern dots
PAPER = (248, 241, 222)    # cream letter paper
PAPER_EDGE = (233, 222, 196)
INK = (43, 33, 24)         # dark brown ink
RED = (139, 46, 46)        # oxblood red accent
GOLD = (166, 124, 46)      # brass gold
SEAL = (160, 32, 32)       # wax seal red
SEAL_DARK = (122, 22, 22)
SKY = (250, 238, 205)      # warm sky inside illustration band

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def spaced(draw, xy, text, fnt, fill, tracking=6):
    """Draw centred text with letter tracking (for small caps lines)."""
    x, y = xy
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    cx = x - total / 2
    for ch, w in zip(text, widths):
        draw.text((cx, y), ch, font=fnt, fill=fill)
        cx += w + tracking


def draw_house(draw, cx, top):
    """Small flat-colour house scene, centred on cx, top edge at `top`."""
    # moon + stars
    draw.ellipse([cx + 118, top + 2, cx + 146, top + 30], fill=(255, 226, 150))
    for sx, sy, r in [(cx - 150, top + 12, 2), (cx - 128, top + 34, 2),
                      (cx + 96, top + 44, 2), (cx + 168, top + 48, 2)]:
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 226, 150))
    # pine tree (left)
    tx = cx - 168
    for i, (w, h) in enumerate([(64, 34), (52, 30), (40, 28)]):
        y0 = top + 34 + i * 22
        draw.polygon([(tx, y0), (tx - w / 2, y0 + h), (tx + w / 2, y0 + h)],
                     fill=(47, 107, 58))
    draw.rectangle([tx - 5, top + 100, tx + 5, top + 114], fill=(92, 58, 33))
    # house body + roof
    bx0, bx1 = cx - 105, cx + 105
    by0, by1 = top + 52, top + 118
    draw.rectangle([bx0, by0, bx1, by1], fill=(196, 110, 74))
    draw.polygon([(bx0 - 16, by0), (bx1 + 16, by0), (cx, top + 8)],
                 fill=(122, 59, 46))
    # chimney + smoke
    draw.rectangle([cx + 62, top + 16, cx + 84, top + 52], fill=(150, 84, 60))
    for i, (sx, sy, r) in enumerate([(cx + 76, top + 2, 7), (cx + 70, top - 12, 9),
                                     (cx + 78, top - 26, 11)]):
        draw.ellipse([sx - r, sy - r, sx + r, sy + r],
                     fill=(214, 204, 186), outline=None)
    # lit windows
    for wx in (cx - 78, cx + 38):
        draw.rectangle([wx, by0 + 14, wx + 34, by0 + 46], fill=(255, 217, 122))
        draw.line([wx + 17, by0 + 14, wx + 17, by0 + 46], fill=(122, 59, 46), width=3)
        draw.line([wx, by0 + 30, wx + 34, by0 + 30], fill=(122, 59, 46), width=3)
    # door
    draw.rectangle([cx - 17, by0 + 34, cx + 17, by1], fill=(92, 58, 33))
    draw.ellipse([cx + 8, by0 + 62, cx + 13, by0 + 67], fill=(255, 217, 122))
    # path
    draw.polygon([(cx - 22, by1), (cx + 22, by1), (cx + 40, top + 138),
                  (cx - 40, top + 138)], fill=(233, 222, 196))
    # ground line
    draw.line([cx - 190, top + 138, cx + 190, top + 138], fill=(166, 124, 46), width=2)


def draw_chair(draw, x, y, s=1.0):
    """High-backed leather armchair doodle, top-left at (x, y), scale s."""
    u = lambda v: int(v * s)
    # back + seat + arms (flat leather red-brown)
    draw.rounded_rectangle([x, y, x + u(120), y + u(86)], radius=u(14),
                           fill=(122, 59, 46))
    draw.rounded_rectangle([x + u(8), y + u(78), x + u(112), y + u(104)],
                           radius=u(8), fill=(139, 69, 52))
    draw.rounded_rectangle([x - u(14), y + u(52), x + u(6), y + u(106)],
                           radius=u(8), fill=(107, 50, 40))
    draw.rounded_rectangle([x + u(114), y + u(52), x + u(134), y + u(106)],
                           radius=u(8), fill=(107, 50, 40))
    # cushion line + brass plaque
    draw.line([x + u(10), y + u(44), x + u(110), y + u(44)],
              fill=(92, 44, 34), width=2)
    draw.rectangle([x + u(38), y + u(14), x + u(82), y + u(34)], fill=(212, 175, 90))
    draw.rectangle([x + u(38), y + u(14), x + u(82), y + u(34)],
                   outline=(139, 104, 40), width=2)
    # legs
    draw.rectangle([x + u(6), y + u(104), x + u(14), y + u(118)], fill=(70, 45, 28))
    draw.rectangle([x + u(106), y + u(104), x + u(114), y + u(118)], fill=(70, 45, 28))
    # side table + steaming cup
    draw.rectangle([x + u(152), y + u(76), x + u(196), y + u(84)], fill=(92, 58, 33))
    draw.rectangle([x + u(171), y + u(84), x + u(177), y + u(118)], fill=(92, 58, 33))
    draw.rounded_rectangle([x + u(156), y + u(52), x + u(188), y + u(76)],
                           radius=u(6), fill=(248, 241, 222),
                           outline=(139, 46, 46), width=2)
    draw.arc([x + u(188), y + u(56), x + u(200), y + u(72)], 300, 60,
             fill=(139, 46, 46), width=2)
    for dx, w in [(162, 4), (172, 4), (182, 4)]:
        draw.arc([x + u(dx), y + u(28), x + u(dx + 12), y + u(50)], 180, 360,
                 fill=(150, 140, 120), width=2)


def draw_seal(draw, cx, cy, r):
    """Round red wax seal with a cream 'J'."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SEAL)
    draw.ellipse([cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6],
                 outline=SEAL_DARK, width=2)
    draw.ellipse([cx - r + 12, cy - r + 12, cx + r - 12, cy + r - 12],
                 outline=(200, 90, 80), width=1)
    f = font(SERIF_B, int(r * 1.05))
    tw = draw.textlength("J", font=f)
    th = f.getbbox("J")[3]
    draw.text((cx - tw / 2, cy - th / 2 - 4), "J", font=f, fill=(248, 241, 222))


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # subtle dot pattern on the backdrop
    for gy in range(24, H, 48):
        for gx in range(24, W, 48):
            draw.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=BG_DOT)

    # paper card + soft shadow
    draw.rounded_rectangle([70, 56, 970, 984], radius=6, fill=(18, 38, 29))
    draw.rounded_rectangle([62, 48, 962, 976], radius=6, fill=PAPER)
    draw.rounded_rectangle([76, 62, 948, 962], radius=4, outline=RED, width=3)
    draw.rounded_rectangle([84, 70, 940, 954], radius=3, outline=GOLD, width=1)

    # --- house illustration ---
    draw_house(draw, 512, 92)

    # --- kicker ---
    spaced(draw, (512, 252), "YOU ARE CORDIALLY INVITED",
           font(SANS_B, 23), RED, tracking=7)
    # gold rule with diamond
    draw.line([330, 292, 486, 292], fill=GOLD, width=2)
    draw.line([538, 292, 694, 292], fill=GOLD, width=2)
    draw.polygon([(512, 284), (520, 292), (512, 300), (504, 292)], fill=GOLD)

    # --- salutation ---
    draw.text((118, 312), "Dear Judge,", font=font(SERIF_B, 56), fill=INK)

    # --- letter body ---
    body = [
        "You have judged ten thousand houses from a screen. "
        "Come and judge this one in person.",
        "By the fireplace stands a high-backed leather chair \u2014 "
        "exactly 2.4 metres from the fire \u2014 with a small brass "
        "plaque that reads RESERVED FOR THE JUDGE.",
        "The kettle is already on. The Wi-Fi password is on the "
        "fridge. And the dog has already voted yes.",
        "Just say yes \u2014 no stamp needed. You already know the way.",
    ]
    bf = font(SERIF, 30)
    y = 386
    for i, para in enumerate(body):
        for line in wrap(draw, para, bf, 788):
            draw.text((118, y), line, font=bf, fill=INK)
            y += 42
        y += 12 if i < len(body) - 1 else 0

    # --- signature ---
    sig = font(SERIF_I, 30)
    draw.text((512, y + 4), "\u2014 Your hopeful host,", font=sig, fill=INK)
    draw.text((512, y + 40), "No. 7, Willow Lane", font=sig, fill=INK)

    # --- bottom strip: chair doodle + caption, wax seal ---
    # (anchored low; no rule above it, so nothing strikes the signature)
    draw_chair(draw, 130, 888, s=0.55)
    cap = font(SERIF_I, 22)
    draw.text((296, 896), "the chair awaits its judge.", font=cap, fill=INK)
    draw.text((296, 922), "P.S. A verdict counts as a visit.",
              font=cap, fill=RED)
    draw_seal(draw, 852, 924, 40)

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {img.size}")


if __name__ == "__main__":
    main()
