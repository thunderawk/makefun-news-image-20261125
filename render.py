#!/usr/bin/env python3
"""Render the news-image-20261125 front page: 'The World in One Day'.

Draws one 1024x1024 broadsheet PNG (entry.png) summing up Wednesday
25 November 2026. Deterministic: no randomness, no clock, no network.
Run: python3 render.py  ->  writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MX = 36                      # side margin
CW = W - 2 * MX              # content width: 952

PAPER = (247, 241, 227)
INK = (28, 28, 28)
FAINT = (110, 105, 92)
RED = (176, 42, 32)
BLUE = (31, 78, 121)
CREAM2 = (238, 231, 214)
RULE = (150, 143, 126)
NAVY = (14, 42, 71)
SEA = (110, 157, 189)
SKY = (201, 218, 232)
LEAF = (46, 125, 91)
LEAF_D = (30, 96, 68)

F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_SANS_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
F_SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, fnt):
    return draw.textlength(s, font=fnt)


def wrap(draw, s, fnt, max_w):
    """Greedy word wrap; returns list of lines, never wider than max_w."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def tracked(draw, cx, y, s, fnt, fill, tracking):
    """Draw s centred on cx with extra tracking between letters."""
    widths = [draw.textlength(ch, font=fnt) for ch in s]
    total = sum(widths) + tracking * (len(s) - 1)
    x = cx - total / 2
    for ch, w in zip(s, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking


def rule(draw, x0, x1, y, width=1, color=RULE):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


# ---------------------------------------------------------------- data
MASTHEAD_L = "THE WORLD IN ONE DAY"
MASTHEAD_R = "26 STORIES · 8 REGIONS"
DATE = "25 NOVEMBER 2026"
WEEKDAY = "WEDNESDAY"
DECK = "Asia's chip rout. Shenzhou-24 lifts off. Russia cries 'terrorism'."

NUMBERS = [
    ("-5.3%", "KOSPI · WORST POINT"),
    ("-2.9%", "NIKKEI · WORST POINT"),
    ("$3,544.54", "GOLD"),
    ("3.8%", "AUS TRIMMED CPI"),
    ("-13%", "SOFTBANK"),
]

REGIONS = ("EAST ASIA 9 · AMERICAS 4 · EUROPE 4 · WORLD 3 · "
           "MIDDLE EAST 2 · SOUTH ASIA 2 · SE ASIA 1 · OCEANIA 1")

TIMELINE = [
    ("00:30", "Aus CPI hotter"),
    ("13:30", "US PCE + GDP"),
    ("14:00", "Gukesh Game 2"),
    ("19:00", "Beige Book"),
    ("21:00", "US close"),
]

LEADS = [
    dict(tag="East Asia · Markets", art="bars",
         head="CHIP STOCKS LEAD ASIA SELLOFF",
         body=("Nikkei falls as much as 2.9%, Kospi 5.3%, Taiwan 5.1% as "
               "fresh US tariff threats hit and the AI rally fizzles.")),
    dict(tag="East Asia · Space", art="rocket",
         head="SHENZHOU-24 LIFTS OFF",
         body=("China launches Shenzhou-24 from Jiuquan; Pakistan's "
               "Muhammad Zeeshan Ali, 40, is the first foreigner on "
               "its space station.")),
    dict(tag="Europe · War", art="ship",
         head="RUSSIA CRIES 'TERRORISM'",
         body=("Moscow accuses Kyiv of terrorism after drone attacks on "
               "ships in the Baltic and off Libya; Zelenskiy confirmed "
               "the strikes.")),
]

CARDS = [
    ("01", "PCE + GDP DUE 13:30 UTC",
     "PCE and Q3 GDP land today. PCE seen +0.3% on the month, 3.8% on the year; GDP 3.5%."),
    ("02", "AUSTRALIA CPI HOTTER",
     "October prices beat forecasts, trimmed mean 3.8%, above target. The dollar jumps."),
    ("03", "ISRAEL WARNS IRAN",
     "Katz says Iran is developing chemical weapons and vows to stop it."),
    ("04", "GOLD SLIPS TO $3,544",
     "Gold falls 0.3% to $3,544.54 after a 2% drop; a Fed hike is priced at 96-97%."),
    ("05", "SOFTBANK -13%",
     "It leads the chip rout, down 13% today and about 70% since June."),
    ("06", "BJP, AKALI DAL REUNITE",
     "The BJP and Shiromani Akali Dal announce an alliance for the 2027 Punjab vote."),
    ("07", "25 HELD IN CARTAGENA",
     "Gunmen hold 25 hostage in an Exito store after a failed van robbery."),
    ("08", "GUKESH GAME 2 TODAY",
     "Game 2 starts 15:00 CET in Geneva. Gukesh has White; 0.5-0.5 after a draw."),
    ("09", "BRENT $90.8, -23% IN NOV",
     "Brent falls 0.7% to $90.8 on rising supply; it is down about 23% in November."),
    ("10", "INDIA REOPENS HIGHER",
     "GIFT Nifty points to 25,738 after a holiday; the Nifty closed at 25,349.65."),
]

ALSO = [
    "Hang Seng slips 0.73% in the selloff.",
    "S&P 500 futures fall 0.3% in Asia.",
    "MSCI Asia-Pacific ex-Japan down 2.3%.",
    "Nikkei near 57,150, down 1,400-1,600 points.",
    "Kioxia -14%, Tokyo Electron -11%.",
    "SK Hynix and Samsung fall 8% each.",
    "Taiwan falls 3% to 5.1% at the worst.",
    "Libya denies collusion in the Benghazi ship strike.",
    "Medvedev sets out nuclear pre-emption terms.",
    "Chinese warships reach Ream base for Cambodia drills.",
    "Japan pulls car suppliers into drone arms push.",
    "Spain votes Sunday; the PP leads the polls.",
    "Fed Beige Book due 2pm ET.",
]

DATECHECK = ("TUE NOV 24: US close: S&P -0.50%, Nasdaq -1.48%, Dow +0.85% "
             "to 50,019; CAS restores Senegal as AFCON champions; "
             "Gukesh-Sindarov Game 1 draw, 38 moves; Sanofi buys Insmed "
             "for $41bn; Saudi 2027 budget approved: $371bn spend; Iran "
             "rial hits record low, 2.82m per dollar; England beat "
             "Australia by 8 wickets; Nvidia -6% after +31.5% on Monday; "
             "Houthis hit Riyadh tower, 11 hurt; Huawei guilty of "
             "trade-secret theft. MON NOV 23: Cikande factory-fire toll "
             "24 confirmed; COP31 ends with no deal (Sun 22 Nov).")

SOURCES = ("EDITION TO 03:00 UTC · Sources: Reuters · AP · FIDE · "
           "Chess.com · AFP · detikNews · ANI · ABC · The Hindu")


# ---------------------------------------------------------------- art
def art_bars(w, h):
    """Falling bar chart with a red downtrend arrow. Drawn on its own
    layer exactly w x h, so nothing can escape the panel."""
    layer = Image.new("RGB", (w, h), CREAM2)
    d = ImageDraw.Draw(layer)
    base = h - 10
    bars = [(LEAF_D, 56), (LEAF, 48), (LEAF_D, 40),
            (RED, 32), (RED, 26), (RED, 20)]
    bw, gap = 30, 12
    x = 14
    tops = []
    for color, bh in bars:
        d.rectangle([x, base - bh, x + bw, base], fill=color)
        tops.append((x + bw / 2, base - bh))
        x += bw + gap
    # downtrend line through the bar tops, ending in an arrowhead
    pts = [(tops[0][0] - 12, tops[0][1] - 8)] + tops + [(w - 8, base - 14)]
    d.line(pts, fill=RED, width=3)
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 12, ey - 5), (ex - 12, ey + 5)], fill=RED)
    return layer


def art_rocket(w, h):
    """Night launch: navy sky, fixed stars, green Earth arc, flat rocket.
    The arc is a circle whose centre sits below the layer, so only its
    top shows -- and the layer itself clips everything to the panel."""
    layer = Image.new("RGB", (w, h), NAVY)
    d = ImageDraw.Draw(layer)
    stars = [(18, 14), (52, 30), (88, 10), (120, 26), (150, 12),
             (186, 32), (220, 16), (252, 28), (280, 12), (36, 44),
             (104, 48), (168, 44), (232, 50), (268, 44)]
    for sx, sy in stars:
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(240, 240, 220))
    # Earth: big green disc rising from below the panel
    cx = w // 2
    d.ellipse([cx - 95, h - 26, cx + 95, h + 164], fill=LEAF)
    d.arc([cx - 95, h - 26, cx + 95, h + 164], 180, 360,
          fill=(120, 200, 160), width=2)
    # Rocket, centred, nose near the top
    rx = cx
    d.polygon([(rx - 9, 18), (rx + 9, 18), (rx, 4)], fill=RED)          # nose
    d.rectangle([rx - 9, 18, rx + 9, 52], fill=(245, 245, 240))         # body
    d.ellipse([rx - 4, 28, rx + 4, 36], fill=(90, 160, 210))            # window
    d.polygon([(rx - 9, 44), (rx - 18, 58), (rx - 9, 54)], fill=RED)    # fin L
    d.polygon([(rx + 9, 44), (rx + 18, 58), (rx + 9, 54)], fill=RED)    # fin R
    d.polygon([(rx - 6, 52), (rx + 6, 52), (rx, 68)], fill=(240, 140, 40))
    d.polygon([(rx - 3, 52), (rx + 3, 52), (rx, 62)], fill=(250, 210, 80))
    return layer


def art_ship(w, h):
    """Baltic scene: pale sky, sea band, dark hull, containers, drones."""
    layer = Image.new("RGB", (w, h), SKY)
    d = ImageDraw.Draw(layer)
    sea_y = int(h * 0.62)
    d.rectangle([0, sea_y, w, h], fill=SEA)
    # drones: two red dots with dotted drop lines
    for dx, dy in [(52, 14), (238, 10)]:
        d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=RED)
        y = dy + 6
        while y < sea_y - 26:
            d.line([(dx, y), (dx, y + 4)], fill=RED, width=1)
            y += 9
    # containers on deck
    d.rectangle([86, sea_y - 34, 150, sea_y - 16], fill=(245, 245, 240))
    d.rectangle([156, sea_y - 34, 196, sea_y - 16], fill=RED)
    d.rectangle([202, sea_y - 26, 232, sea_y - 16], fill=(60, 60, 60))
    # hull: trapezoid, bow to the right
    d.polygon([(28, sea_y - 16), (w - 22, sea_y - 16), (w - 52, sea_y + 14),
               (52, sea_y + 14)], fill=(24, 38, 52))
    d.line([(28, sea_y - 16), (w - 22, sea_y - 16)], fill=(24, 38, 52), width=2)
    return layer


ART = {"bars": art_bars, "rocket": art_rocket, "ship": art_ship}


# ---------------------------------------------------------------- page
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 28

    # Masthead
    f_mast = font(F_SANS, 21)
    d.text((MX, y), MASTHEAD_L, font=f_mast, fill=INK)
    f_mast_r = font(F_SANS, 19)
    d.text((W - MX - text_w(d, MASTHEAD_R, f_mast_r), y + 2),
           MASTHEAD_R, font=f_mast_r, fill=RED)
    y += 26

    # Giant date, centred (v1: x-span 181-843, ~662px wide, cap ~50px)
    size = 68
    while size > 40:
        f_date = font(F_SANS, size)
        if text_w(d, DATE, f_date) <= CW:
            break
        size -= 2
    dw = text_w(d, DATE, f_date)
    d.text(((W - dw) / 2, y), DATE, font=f_date, fill=INK)
    y += size + 8

    # Weekday, letterspaced, centred
    tracked(d, W // 2, y, WEEKDAY, font(F_SANS, 19), RED, 7)
    y += 22

    # Double rule
    rule(d, MX, W - MX, y, 3, INK)
    rule(d, MX, W - MX, y + 6, 1, INK)
    y += 12

    # Deck
    f_deck = font(F_SERIF_IT, 20)
    dw = text_w(d, DECK, f_deck)
    d.text(((W - dw) / 2, y), DECK, font=f_deck, fill=INK)
    y += 26
    rule(d, MX, W - MX, y, 1)
    y += 6

    # BY THE NUMBERS strip
    col_w = CW / len(NUMBERS)
    f_num = font(F_SANS, 30)
    f_num_l = font(F_SANS, 11)
    for i, (val, lab) in enumerate(NUMBERS):
        cx = MX + col_w * i + col_w / 2
        vw = text_w(d, val, f_num)
        d.text((cx - vw / 2, y), val, font=f_num, fill=INK)
        lw = text_w(d, lab, f_num_l)
        d.text((cx - lw / 2, y + 34), lab, font=f_num_l, fill=FAINT)
        if i:
            x = MX + col_w * i
            d.line([(x, y + 2), (x, y + 44)], fill=RULE, width=1)
    y += 52
    rule(d, MX, W - MX, y, 1)
    y += 6

    # Region bar
    f_reg = font(F_SANS, 14)
    rw = text_w(d, REGIONS, f_reg)
    d.text(((W - rw) / 2, y), REGIONS, font=f_reg, fill=BLUE)
    y += 20
    rule(d, MX, W - MX, y, 1)
    y += 6

    # UTC timeline
    tcol = CW / len(TIMELINE)
    f_time = font(F_SANS, 14)
    f_tlab = font(F_SERIF, 14)
    for i, (t, lab) in enumerate(TIMELINE):
        x = MX + tcol * i
        d.text((x, y), t, font=f_time, fill=RED)
        d.text((x, y + 18), lab, font=f_tlab, fill=INK)
    y += 42

    # Lead panels: art (clipped layer) + tag + headline + body
    gutter = 23
    pw = (CW - 2 * gutter) // 3
    art_h = 60
    f_tag = font(F_SANS, 12)
    f_lhead = font(F_SANS, 17)
    f_lbody = font(F_SERIF, 14)
    lead_top = y
    lead_bottom = lead_top
    for i, lead in enumerate(LEADS):
        x = MX + i * (pw + gutter)
        layer = ART[lead["art"]](pw, art_h)
        img.paste(layer, (x, lead_top))
        ly = lead_top + art_h + 6
        d.text((x, ly), lead["tag"], font=f_tag, fill=RED)
        ly += 14
        for line in wrap(d, lead["head"], f_lhead, pw)[:2]:
            d.text((x, ly), line, font=f_lhead, fill=INK)
            ly += 21
        ly += 2
        for line in wrap(d, lead["body"], f_lbody, pw)[:3]:
            d.text((x, ly), line, font=f_lbody, fill=INK)
            ly += 17
        lead_bottom = max(lead_bottom, ly)
    y = lead_bottom + 20

    # Numbered cards, 3 columns x 4 rows (last row: one card).
    # v1 row pitch is 67px: number + 1-line headline + 2-line body.
    f_cnum = font(F_SANS, 16)
    f_chead = font(F_SANS, 17)
    f_cbody = font(F_SERIF, 13)
    rows = [CARDS[i:i + 3] for i in range(0, len(CARDS), 3)]
    for row in rows:
        row_h = 0
        heights = []
        for num, head, body in row:
            hlines = wrap(d, head, f_chead, pw)[:2]
            blines = wrap(d, body, f_cbody, pw)[:2]
            ch = 16 + len(hlines) * 19 + 2 + len(blines) * 15
            heights.append(ch)
            row_h = max(row_h, ch)
        for j, (num, head, body) in enumerate(row):
            x = MX + j * (pw + gutter)
            cy = y
            d.text((x, cy), num, font=f_cnum, fill=RED)
            cy += 16
            for line in wrap(d, head, f_chead, pw)[:2]:
                d.text((x, cy), line, font=f_chead, fill=INK)
                cy += 19
            cy += 2
            for line in wrap(d, body, f_cbody, pw)[:2]:
                d.text((x, cy), line, font=f_cbody, fill=INK)
                cy += 15
        y += row_h

    # ALSO list, two columns (01-07 left, 08-13 right)
    f_ahead = font(F_SANS, 13)
    f_anum = font(F_SANS, 11)
    f_atext = font(F_SERIF, 13)
    d.text((MX, y), "ALSO ON WEDNESDAY", font=f_ahead, fill=RED)
    y += 16
    half = 7
    left_x = MX
    right_x = MX + CW // 2 + 6
    col_w2 = CW // 2 - 12
    for k, item in enumerate(ALSO):
        if k < half:
            x = left_x
            yy = y + k * 13
        else:
            x = right_x
            yy = y + (k - half) * 13
        d.text((x, yy), "%02d" % (k + 1), font=f_anum, fill=RED)
        d.text((x + 24, yy), item, font=f_atext, fill=INK)
    y += half * 13 + 10

    # DATE CHECK box
    f_dhead = font(F_SANS, 13)
    f_dbody = font(F_SERIF, 13)
    inner = CW - 28
    dlines = wrap(d, DATECHECK, f_dbody, inner)
    box_h = 24 + len(dlines) * 15 + 8
    d.rectangle([MX, y, W - MX, y + box_h], outline=RED, width=2)
    d.text((MX + 14, y + 7), "DATE CHECK — NOT WEDNESDAY",
           font=f_dhead, fill=RED)
    by = y + 24
    for line in dlines:
        d.text((MX + 14, by), line, font=f_dbody, fill=INK)
        by += 15
    y += box_h + 8

    # Sources line
    f_src = font(F_SERIF, 12)
    d.text((MX, y), SOURCES, font=f_src, fill=FAINT)
    y += 16

    print("sections end y =", y, "(canvas", H, ")")
    img.save(OUT)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    render()
