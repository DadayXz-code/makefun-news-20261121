#!/usr/bin/env python3
"""Generate entry.png: an original illustrated front page summing up the world news of
Saturday 21 November 2026. Every picture on the page is drawn here with code (flat
vector-style illustrations) -- no photographs, no copied artwork. Story facts were
checked against same-day reporting (COP31 overtime, Riyadh missiles, Peru quake,
fresh Kyiv strikes, FBI/USDA hacks, UK-EU signing). Run: python3 generate.py
-> writes entry.png (1024x1024).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (163, 18, 18)
BLUE = (31, 58, 95)
GREY = (110, 106, 96)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, maxw):
    """Greedy word wrap; returns list of lines that fit maxw."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, maxw, text, font, fill=INK, leading=None, max_lines=None):
    """Draw wrapped text; returns y just below the last line."""
    lh = leading if leading is not None else int(font.size * 1.22)
    lines = wrap(d, text, font, maxw)
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def hline(d, x0, x1, y, wdt=1, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=wdt)


def paste_ill(img, fn, x, y, w, h):
    """Render an illustration on its own layer, clipped to its box, then paste."""
    layer = Image.new("RGB", (w, h), PAPER)
    dl = ImageDraw.Draw(layer)
    fn(dl, 0, 0, w, h)
    img.paste(layer, (x, y))


def kicker(d, x, y, text, color=RED):
    d.text((x, y), text, font=F(SANS_B, 13), fill=color)
    return y + 18


# ---------------- illustrations (all drawn, original) ----------------

def ill_summit(d, x, y, w, h):
    """Climate summit: globe, rising thermometer, flags."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 226))
    r = min(52, h // 2 - 4)
    cx, cy = x + int(w * 0.30), y + h // 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 130, 180))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(31, 58, 95), width=2)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360,
          fill=(90, 170, 110), width=max(3, r // 5))
    d.arc([cx - r // 2, cy - r, cx + r // 2, cy + r], 0, 360,
          fill=(90, 170, 110), width=max(3, r // 6))
    tx = x + int(w * 0.74)  # thermometer
    top, bot = y + 8, y + h - 22
    d.rectangle([tx - 7, top, tx + 7, bot], fill=(255, 255, 255),
                outline=(163, 18, 18), width=2)
    d.rectangle([tx - 4, top + (bot - top) // 2, tx + 4, bot], fill=(220, 60, 40))
    d.ellipse([tx - 13, bot - 4, tx + 13, bot + 18], fill=(220, 60, 40))
    if h >= 100:
        for i, col in enumerate(((31, 58, 95), (163, 18, 18), (176, 132, 40), (70, 130, 110))):
            fx = x + 12 + i * 24
            d.polygon([(fx, y + h - 6), (fx, y + h - 34), (fx + 16, y + h - 27),
                       (fx, y + h - 20)], fill=col)


def ill_missiles(d, x, y, w, h):
    """Night sky over Riyadh: skyline, interceptor trails, bursts."""
    for i in range(h):
        t = i / h
        d.line([(x, y + i), (x + w, y + i)],
               fill=(int(16 + 10 * t), int(18 + 12 * t), int(44 + 20 * t)))
    for sx, sy in ((0.12, 0.2), (0.3, 0.1), (0.55, 0.28), (0.78, 0.14), (0.9, 0.32)):
        d.ellipse([x + int(w * sx) - 2, y + int(h * sy) - 2,
                   x + int(w * sx) + 2, y + int(h * sy) + 2], fill=(255, 255, 255))
    base = y + h - 34  # skyline
    for bx, bw, bh in ((0.02, 0.14, 26), (0.20, 0.10, 40), (0.34, 0.12, 30),
                       (0.50, 0.09, 58), (0.63, 0.13, 34), (0.80, 0.11, 44)):
        d.rectangle([x + int(w * bx), base - bh, x + int(w * (bx + bw)), y + h],
                    fill=(10, 12, 26))
        for wy in range(base - bh + 6, y + h - 4, 9):  # lit windows
            d.rectangle([x + int(w * bx) + 4, wy,
                         x + int(w * bx) + 8, wy + 4], fill=(255, 210, 110))
    for tx0, ty0, tx1, ty1 in ((0.15, 0.15, 0.45, 0.55), (0.85, 0.12, 0.60, 0.5),
                               (0.5, 0.08, 0.52, 0.45)):  # interceptor trails
        d.line([(x + int(w * tx0), y + int(h * ty0)),
                (x + int(w * tx1), y + int(h * ty1))], fill=(255, 200, 90), width=3)
    for bx, by, s in ((0.45, 0.55, 16), (0.60, 0.5, 13)):  # intercept bursts
        cx, cy = x + int(w * bx), y + int(h * by)
        for k in range(8):
            a = k * math.pi / 4
            d.line([(cx, cy), (cx + int(s * math.cos(a)), cy + int(s * math.sin(a)))],
                   fill=(255, 170, 40), width=3)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 230, 150))


def ill_quake(d, x, y, w, h):
    """Andes mountains, a crack in the ground, seismograph trace."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 214, 188))
    d.polygon([(x, y + h), (x + int(w * 0.25), y + int(h * 0.25)),
               (x + int(w * 0.45), y + h)], fill=(120, 110, 95))
    d.polygon([(x + int(w * 0.30), y + h), (x + int(w * 0.58), y + int(h * 0.18)),
               (x + int(w * 0.85), y + h)], fill=(90, 82, 70))
    d.polygon([(x + int(w * 0.52), y + int(h * 0.18)), (x + int(w * 0.58), y + int(h * 0.18)),
               (x + int(w * 0.55), y + int(h * 0.30))], fill=(255, 255, 255))
    d.polygon([(x + int(w * 0.20), y + int(h * 0.25)), (x + int(w * 0.25), y + int(h * 0.25)),
               (x + int(w * 0.225), y + int(h * 0.36))], fill=(255, 255, 255))
    crack = [(0.48, 0.62), (0.52, 0.70), (0.47, 0.78), (0.53, 0.86), (0.49, 0.95)]
    d.line([(x + int(w * px), y + int(h * py)) for px, py in crack],
           fill=(60, 40, 30), width=4)
    pts = [(0.04, 0.30), (0.14, 0.30), (0.18, 0.18), (0.22, 0.44), (0.27, 0.30),
           (0.33, 0.30), (0.38, 0.08), (0.43, 0.55), (0.48, 0.30), (0.55, 0.30),
           (0.60, 0.20), (0.65, 0.40), (0.70, 0.30), (0.80, 0.30), (0.85, 0.22),
           (0.90, 0.38), (0.96, 0.30)]
    d.line([(x + int(w * px), y + int(h * py)) for px, py in pts],
           fill=(163, 18, 18), width=2)
    d.text((x + 8, y + 6), "M 6.7", font=F(SANS_B, 14), fill=(163, 18, 18))


def ill_bridge(d, x, y, w, h):
    """Dusk sky, river, a bridge, explosion bursts."""
    for i in range(h):
        t = i / h
        d.line([(x, y + i), (x + w, y + i)],
               fill=(int(44 + 60 * t), int(52 + 55 * t), int(84 + 60 * t)))
    d.rectangle([x, y + h - 46, x + w, y + h], fill=(38, 54, 74))
    d.rectangle([x, y + h - 96, x + w, y + h - 88], fill=(20, 20, 26))
    for px in (0.18, 0.5, 0.82):
        bx = x + int(w * px)
        d.rectangle([bx - 5, y + h - 88, bx + 5, y + h - 46], fill=(20, 20, 26))
    for bx, by, s, col in ((0.30, 0.30, 46, (255, 176, 32)),
                           (0.62, 0.22, 60, (255, 120, 20)),
                           (0.80, 0.38, 34, (255, 200, 90))):
        cx, cy = x + int(w * bx), y + int(h * by)
        for k in range(10):
            a = k * math.pi / 5
            d.line([(cx, cy), (cx + int(s * math.cos(a)), cy + int(s * math.sin(a)))],
                   fill=col, width=5)
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(255, 226, 140))
    for sx, sy, r in ((0.42, 0.16, 20), (0.52, 0.10, 26), (0.72, 0.30, 16)):
        d.ellipse([x + int(w * sx) - r, y + int(h * sy) - r,
                   x + int(w * sx) + r, y + int(h * sy) + r], fill=(90, 88, 92))


def ill_server(d, x, y, w, h):
    """Server racks with a warning triangle."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 238, 240))
    for i in range(3):
        rx = x + 10 + i * ((w - 20) // 3)
        rw = (w - 20) // 3 - 8
        d.rectangle([rx, y + 8, rx + rw, y + h - 8], fill=(52, 58, 68))
        for u in range(4):
            uy = y + 14 + u * ((h - 28) // 4)
            d.rectangle([rx + 6, uy, rx + rw - 6, uy + (h - 28) // 4 - 6],
                        fill=(90, 98, 110))
            d.ellipse([rx + rw - 16, uy + 3, rx + rw - 10, uy + 9],
                      fill=(120, 220, 130) if u % 2 else (255, 80, 60))
    tx, ty = x + w - 44, y + h - 44
    d.polygon([(tx + 18, ty), (tx + 36, ty + 34), (tx, ty + 34)], fill=(255, 190, 0),
              outline=(163, 18, 18))
    d.text((tx + 15, ty + 12), "!", font=F(SANS_B, 16), fill=(163, 18, 18))


def ill_flags(d, x, y, w, h):
    """Union Jack (simplified) beside the EU circle of stars."""
    hw = w // 2
    d.rectangle([x, y, x + hw - 4, y + h], fill=(18, 40, 90))
    d.rectangle([x, y + h // 2 - 7, x + hw - 4, y + h // 2 + 7], fill=(255, 255, 255))
    d.line([(x, y), (x + hw - 4, y + h)], fill=(255, 255, 255), width=10)
    d.line([(x + hw - 4, y), (x, y + h)], fill=(255, 255, 255), width=10)
    d.rectangle([x, y + h // 2 - 4, x + hw - 4, y + h // 2 + 4], fill=(200, 16, 46))
    d.line([(x, y), (x + hw - 4, y + h)], fill=(200, 16, 46), width=4)
    d.line([(x + hw - 4, y), (x, y + h)], fill=(200, 16, 46), width=4)
    ex = x + hw + 4
    d.rectangle([ex, y, ex + hw - 4, y + h], fill=(0, 51, 153))
    ccx, ccy = ex + (hw - 4) // 2, y + h // 2
    for k in range(12):
        a = -math.pi / 2 + k * math.pi / 6
        sx, sy = ccx + int(30 * math.cos(a)), ccy + int(30 * math.sin(a))
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 204, 0))


# ---------------- content: Saturday 21 November 2026 ----------------

LEAD = {
    "kicker": "CLIMATE  ·  COP31",
    "headline": "COP31 goes into overtime as fossil-fuel row deadlocks talks",
    "dek": ("Nearly 200 nations in Antalya failed to agree a deal by the Friday "
            "deadline. The draft omits any mention of phasing out fossil fuels, "
            "and talks ran into an extra day."),
    "ill": ill_summit,
    "caption": "Illustration: the COP31 climate summit in Antalya. Drawn, not a photograph.",
}

ROW2 = [
    {"kicker": "MIDDLE EAST  ·  RIYADH", "region": "Middle East",
     "headline": "Coalition intercepts three Houthi missiles aimed at Riyadh",
     "body": ("Saudi air defences shot down three ballistic missiles, the third "
              "night of alerts. A Houthi strike damaged the PIF Tower in the "
              "capital's financial district this week."),
     "ill": ill_missiles},
    {"kicker": "PERU  ·  EARTHQUAKE", "region": "South America",
     "headline": "Magnitude 6.7 quake shakes the Peruvian Andes",
     "body": ("The quake struck near Carhuamayo, Junín, 108 km deep, sparking "
              "panic but no major damage at first, the USGS reported."),
     "ill": ill_quake},
]

GRID = [
    {"kicker": "UKRAINE  ·  KYIV", "region": "Eastern Europe",
     "headline": "Fresh Russian strikes: 148 drones hit 19 sites",
     "body": ("Three missiles and 148 drones hit 19 sites; houses caught fire "
              "in Kyiv."),
     "ill": ill_bridge},
    {"kicker": "UNITED STATES  ·  CYBER", "region": "Americas",
     "headline": "FBI and Agriculture Department hit by hackers",
     "body": ("Cyberattacks followed days of computer outages in US strategic "
              "sectors."),
     "ill": ill_server},
    {"kicker": "BRITAIN  ·  EUROPE", "region": "Western Europe",
     "headline": "London and Brussels sign biggest deal since Brexit",
     "body": ("Food trade, linked carbon markets and a youth scheme signed in "
              "Brussels."),
     "ill": ill_flags},
]

BRIEFS = [
    ("Eastern Europe", "Kryvyi Rih strike kills child and paramedic; 21 hurt"),
    ("Eastern Europe", "Zaporizhzhia kindergarten attacked; flats catch fire"),
    ("Middle East", "Coalition says it destroyed six Houthi workshops"),
    ("Climate", "COP31: extra day of talks amid fears of no deal"),
    ("Western Europe", "Youth climate strikes target military spending"),
    ("Asia", "Pakistan hit by nationwide internet outage"),
    ("Western Europe", "Cost-of-living protests sweep the continent"),
    ("Eastern Europe", "Poland calls missile fall 'intentional'"),
    ("Americas", "Roundup complaints near preliminary settlement"),
    ("Science", "BepiColombo reaches Mercury"),
    ("Africa", "Displacement grows in Ethiopia"),
    ("Middle East", "Iran drone claim reported, unconfirmed"),
    ("Americas", "AI stock rout leads world markets lower"),
    ("Western Europe", "UK–EU reset: youth scheme for 100,000 a year"),
    ("Climate", "Nearly 200 nations still split over fossil fuels"),
]

TICKER = "COP31 OVERTIME  ·  3 MISSILES INTERCEPTED  ·  M6.7 PERU QUAKE  ·  148 DRONES  ·  108 KM DEEP"
DATE_LINE = "SATURDAY, 21 NOVEMBER 2026"
DAY = "Saturday 21 November 2026"


def main():
    regions = set()
    for s in ROW2 + GRID:
        regions.add(s["region"])
    for r, _ in BRIEFS:
        regions.add(r)
    n_stories = 1 + len(ROW2) + len(GRID) + len(BRIEFS)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 26  # margin
    X1 = W - M

    # masthead
    d.text((M, 16), DATE_LINE, font=F(SANS_B, 14), fill=INK)
    meta = f"{n_stories} STORIES · {len(regions)} REGIONS"
    d.text((X1 - d.textlength(meta, font=F(SANS_B, 14)), 16), meta,
           font=F(SANS_B, 14), fill=INK)
    title = "THE WORLD TODAY"
    d.text(((W - d.textlength(title, font=F(SERIF_B, 62))) / 2, 34), title,
           font=F(SERIF_B, 62), fill=INK)
    sub = "SATURDAY 21 NOVEMBER 2026  ·  LATE EDITION  ·  THE DAY'S NEWS IN ONE PAGE"
    d.text(((W - d.textlength(sub, font=F(SANS_B, 13))) / 2, 104), sub,
           font=F(SANS_B, 13), fill=GREY)
    hline(d, M, X1, 126, 3)
    hline(d, M, X1, 131, 1)

    # ticker strip
    d.text(((W - d.textlength(TICKER, font=F(SANS_B, 13))) / 2, 140), TICKER,
           font=F(SANS_B, 13), fill=RED)
    hline(d, M, X1, 162, 1)

    # lead story
    y = 176
    ill_w, ill_h = 470, 218
    paste_ill(img, LEAD["ill"], M, y, ill_w, ill_h)
    d.text((M, y + ill_h + 6), LEAD["caption"], font=F(SERIF, 12), fill=GREY)
    tx = M + ill_w + 20
    tw = X1 - tx
    yy = kicker(d, tx, y, LEAD["kicker"])
    yy = block(d, tx, yy + 2, tw, LEAD["headline"], F(SERIF_B, 35), leading=40)
    block(d, tx, yy + 8, tw, LEAD["dek"], F(SERIF, 17), leading=23)
    hline(d, M, X1, 424, 1)

    # row 2: two stories, illustration left, text right
    y = 440
    col_w = (X1 - M - 24) // 2
    for i, s in enumerate(ROW2):
        x = M + i * (col_w + 24)
        iw, ih = 168, 118
        paste_ill(img, s["ill"], x, y, iw, ih)
        tx2 = x + iw + 12
        tw2 = col_w - iw - 12
        yy = kicker(d, tx2, y, s["kicker"])
        yy = block(d, tx2, yy + 1, tw2, s["headline"], F(SERIF_B, 19), leading=23,
                   max_lines=3)
        block(d, tx2, yy + 4, tw2, s["body"], F(SERIF, 13.5), leading=17, max_lines=4)
        if i == 0:
            d.line([(M + col_w + 12, y), (M + col_w + 12, y + 168)], fill=GREY, width=1)
    hline(d, M, X1, 622, 1)

    # grid: three stories, illustration on top
    y = 638
    gw = (X1 - M - 48) // 3
    for i, s in enumerate(GRID):
        x = M + i * (gw + 24)
        paste_ill(img, s["ill"], x, y, gw, 70)
        yy = kicker(d, x, y + 78, s["kicker"])
        yy = block(d, x, yy + 1, gw, s["headline"], F(SERIF_B, 18), leading=21,
                   max_lines=2)
        block(d, x, yy + 4, gw, s["body"], F(SERIF, 13.5), leading=16, max_lines=2)
        if i < 2:
            d.line([(x + gw + 12, y), (x + gw + 12, y + 168)], fill=GREY, width=1)
    hline(d, M, X1, 822, 1)

    # briefs: two columns, one line each
    y = 838
    d.text((M, y), "THE DAY IN BRIEF", font=F(SANS_B, 15), fill=INK)
    d.text((X1 - d.textlength(DAY, font=F(SERIF, 13)), y + 2), DAY,
           font=F(SERIF, 13), fill=GREY)
    hline(d, M, X1, y + 24, 1)
    by = y + 34
    bw = (X1 - M - 24) // 2
    for idx, item in enumerate(BRIEFS):
        col, row = idx % 2, idx // 2
        x = M + col * (bw + 24)
        yy = by + row * 16
        d.text((x, yy), "▪", font=F(SANS_B, 11), fill=RED)
        d.text((x + 14, yy), item[1], font=F(SERIF, 12.5), fill=INK)
    foot = "Events reported on 21 November 2026. All pictures are original drawings, not photographs."
    d.text(((W - d.textlength(foot, font=F(SERIF, 12))) / 2, 1004), foot,
           font=F(SERIF, 12), fill=GREY)

    img.save("entry.png", optimize=True)
    print(f"saved entry.png {n_stories} stories, {len(regions)} regions")


if __name__ == "__main__":
    main()
