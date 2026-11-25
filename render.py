#!/usr/bin/env python3
"""Render the news-image-20261125 front page: Wednesday 25 November 2026.

Fresh re-author for this edition (post-opening session, 25 Nov 2026).
Proven broadsheet formula: giant date, deck, numbers strip, region bar,
UTC timeline, 3 illustrated leads, 10 numbered cards, ALSO list,
DATE CHECK box, sources line. All stories verified against wire dates;
Tuesday/Monday items sit only in DATE CHECK, honestly dated.
Deterministic: no randomness, no clock, no network.
"""
import hashlib

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MX = 36                      # side margin
CW = W - 2 * MX              # content width = 952

PAPER = (244, 239, 228)
INK = (26, 26, 26)
RED = (178, 34, 30)
BLUE = (31, 78, 121)
TEAL = (14, 110, 96)
GOLD = (198, 152, 40)
MUTED = (112, 106, 94)
RULE = (186, 178, 158)
NAVY = (16, 32, 64)

DJ = "/usr/share/fonts/truetype/dejavu/"
LB = "/usr/share/fonts/truetype/liberation/"


def f(path, size):
    return ImageFont.truetype(path, size)


SANS = DJ + "DejaVuSans.ttf"
SANSB = DJ + "DejaVuSans-Bold.ttf"
SERIF = DJ + "DejaVuSerif.ttf"
SERIFI = LB + "LiberationSerif-Italic.ttf"

# ---------------------------------------------------------------- stories
# region tags: East Asia / Europe / Middle East / South Asia / SE Asia /
# Oceania / Americas / World
LEADS = [
    ("CHIP STOCKS LEAD ASIA SELLOFF", "East Asia · Markets",
     "Nikkei falls as much as 2.9%, Kospi 5.3%, Taiwan 5.1% as fresh US "
     "tariff threats hit and the AI rally fizzles.",
     "fall", "East Asia"),
    ("SHENZHOU-24 LIFTS OFF", "East Asia · Space",
     "China launches Shenzhou-24 from Jiuquan; Pakistan's Muhammad "
     "Zeeshan Ali, 40, is the first foreigner on its space station.",
     "rocket", "East Asia"),
    ("RUSSIA CRIES 'TERRORISM'", "Europe · War",
     "Moscow accuses Kyiv of terrorism after drone attacks on ships in "
     "the Baltic and off Libya; Zelenskiy confirmed the strikes.",
     "ship", "Europe"),
]

NUMBERS = [
    ("-5.3%", "KOSPI · WORST POINT"),
    ("-2.9%", "NIKKEI · WORST POINT"),
    ("$3,544.54", "GOLD"),
    ("3.8%", "AUS TRIMMED CPI"),
    ("-13%", "SOFTBANK"),
]

TIMELINE = [
    ("00:30", "Aus CPI hotter"),
    ("13:30", "US PCE + GDP"),
    ("14:00", "Gukesh Game 2"),
    ("19:00", "Beige Book"),
    ("21:00", "US close"),
]

CARDS = [
    ("PCE + GDP DUE 13:30 UTC",
     "PCE and Q3 GDP land today: PCE seen +0.3% on the month, 3.8% on "
     "the year; GDP 3.5%.",
     "Americas"),
    ("AUSTRALIA CPI HOTTER",
     "October prices beat forecasts; trimmed mean 3.8%, above target. "
     "The dollar jumps.",
     "Oceania"),
    ("ISRAEL WARNS IRAN",
     "Katz says Iran is developing chemical weapons and vows to stop "
     "it.",
     "Middle East"),
    ("GOLD SLIPS TO $3,544",
     "Gold falls 0.3% to $3,544.54 after a 2% drop; a Fed hike is "
     "priced at 96-97%.",
     "World"),
    ("SOFTBANK -13%",
     "It leads the chip rout, down 13% today and about 70% since June.",
     "East Asia"),
    ("BJP, AKALI DAL REUNITE",
     "The BJP and Shiromani Akali Dal announce an alliance for the "
     "2027 Punjab vote.",
     "South Asia"),
    ("25 HELD IN CARTAGENA",
     "Gunmen hold 25 hostage in an Exito store after a failed van "
     "robbery.",
     "Americas"),
    ("GUKESH GAME 2 TODAY",
     "Game 2 starts 15:00 CET in Geneva. Gukesh has White; 0.5-0.5 "
     "after a draw.",
     "Europe"),
    ("BRENT $90.8, -23% IN NOV",
     "Brent falls 0.7% to $90.8 on rising supply; it is down about "
     "23% in November.",
     "World"),
    ("INDIA REOPENS HIGHER",
     "GIFT Nifty points to 25,738 after a holiday; the Nifty closed "
     "at 25,349.65.",
     "South Asia"),
]

ALSO = [
    ("Hang Seng slips 0.73% in the selloff.", "East Asia"),
    ("S&P 500 futures fall 0.3% in Asia.", "Americas"),
    ("MSCI Asia-Pacific ex-Japan down 2.3%.", "World"),
    ("Nikkei near 57,150, down 1,400-1,600 points.", "East Asia"),
    ("Kioxia -14%, Tokyo Electron -11%.", "East Asia"),
    ("SK Hynix and Samsung fall 8% each.", "East Asia"),
    ("Taiwan falls 3% to 5.1% at the worst.", "East Asia"),
    ("Libya denies collusion in the Benghazi ship strike.", "Middle East"),
    ("Medvedev sets out nuclear pre-emption terms.", "Europe"),
    ("Chinese warships reach Ream base for Cambodia drills.", "SE Asia"),
    ("Japan pulls car suppliers into drone arms push.", "East Asia"),
    ("Spain votes Sunday; the PP leads the polls.", "Europe"),
    ("Fed Beige Book due 2pm ET.", "Americas"),
]

# Honestly dated: these did NOT happen on Wednesday.
DATE_CHECK_TUE = [
    "US close: S&P -0.50%, Nasdaq -1.48%, Dow +0.85% to 50,019",
    "CAS restores Senegal as AFCON champions",
    "Gukesh-Sindarov Game 1 draw, 38 moves",
    "Sanofi buys Insmed for $41bn",
    "Saudi 2027 budget approved: $371bn spend",
    "Iran rial hits record low, 2.82m per dollar",
    "England beat Australia by 8 wickets",
    "Nvidia -6% after +31.5% on Monday",
    "Houthis hit Riyadh tower, 11 hurt",
    "Huawei guilty of trade-secret theft",
]
DATE_CHECK_MON = [
    "Cikande factory-fire toll 24 confirmed",
    "COP31 ends with no deal (Sun 22 Nov)",
]

SOURCES = ("EDITION TO 03:00 UTC · Sources: Reuters · AP · FIDE · "
           "Chess.com · AFP · detikNews · ANI · ABC · The Hindu")

REGIONS = ["East Asia", "Americas", "Europe", "World",
           "Middle East", "South Asia", "SE Asia", "Oceania"]


def region_counts():
    counts = {r: 0 for r in REGIONS}
    for _, _, _, _, r in LEADS:
        counts[r] += 1
    for _, _, r in CARDS:
        counts[r] += 1
    for _, r in ALSO:
        counts[r] += 1
    return counts


# ---------------------------------------------------------------- helpers
def wrap(draw, text, font, max_w):
    """Greedy word wrap to a list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_rule(draw, x0, x1, y, color=RULE, width=1):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def draw_fall(draw, x, y, w, h):
    """Falling market bars with a red down-trend line."""
    draw.rectangle([x, y, x + w, y + h], fill=(233, 226, 210))
    vals = [0.85, 0.72, 0.62, 0.45, 0.30]
    bw = w // 7
    for i, v in enumerate(vals):
        bx = x + 14 + i * (bw + 6)
        bh = int(v * (h - 22))
        col = RED if i >= 3 else TEAL
        draw.rectangle([bx, y + h - 10 - bh, bx + bw, y + h - 10], fill=col)
    draw.line([(x + 10, y + 12), (x + w - 14, y + h - 12)], fill=RED, width=3)
    # arrowhead at the low end
    ax, ay = x + w - 14, y + h - 12
    draw.polygon([(ax, ay + 8), (ax - 12, ay - 2), (ax + 2, ay - 10)],
                 fill=RED)


def draw_rocket(draw, x, y, w, h):
    """Night launch: dark sky, stars, a white rocket on its flame."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    for sx, sy in [(18, 12), (52, 22), (96, 8), (150, 18), (210, 10),
                   (260, 26), (36, 40), (130, 34), (200, 44), (280, 48)]:
        draw.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3],
                     fill=(240, 236, 220))
    cx = x + w // 2
    top = y + 8
    # flame
    draw.polygon([(cx - 7, top + 34), (cx + 7, top + 34),
                  (cx, top + 56)], fill=(240, 120, 40))
    draw.polygon([(cx - 4, top + 34), (cx + 4, top + 34),
                  (cx, top + 46)], fill=(250, 200, 80))
    # body
    draw.rectangle([cx - 8, top + 6, cx + 8, top + 34],
                   fill=(245, 244, 238))
    draw.polygon([(cx - 8, top + 6), (cx + 8, top + 6), (cx, top - 2)],
                 fill=RED)
    draw.polygon([(cx - 8, top + 26), (cx - 18, top + 38),
                  (cx - 8, top + 38)], fill=RED)
    draw.polygon([(cx + 8, top + 26), (cx + 18, top + 38),
                  (cx + 8, top + 38)], fill=RED)
    draw.ellipse([cx - 4, top + 12, cx + 4, top + 20], fill=BLUE)
    # earth curve at the bottom, kept inside this panel's own box
    draw.arc([x + 10, y + h - 20, x + w - 10, y + h + 16], 180, 360,
             fill=(120, 170, 120), width=4)


def draw_ship(draw, x, y, w, h):
    """A tanker at sea under three drones, red dashed tracks."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 228, 236))
    # sea
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=(120, 160, 190))
    draw.line([(x + 8, y + h - 14), (x + w - 8, y + h - 14)],
              fill=(240, 240, 240), width=2)
    # drones + dashed tracks
    for dx, dy in [(30, 10), (90, 6), (150, 12)]:
        draw.ellipse([x + dx, y + dy, x + dx + 6, y + dy + 6], fill=INK)
        for k in range(3):
            yy = y + dy + 10 + k * 6
            draw.line([(x + dx + 3, yy), (x + dx + 3, yy + 3)],
                      fill=RED, width=2)
    # hull
    hx, hy = x + 40, y + h - 38
    draw.polygon([(hx, hy), (hx + 220, hy), (hx + 200, hy + 16),
                  (hx + 20, hy + 16)], fill=(40, 44, 52))
    draw.rectangle([hx + 60, hy - 14, hx + 110, hy], fill=(240, 240, 240))
    draw.rectangle([hx + 120, hy - 10, hx + 140, hy], fill=RED)
    draw.rectangle([hx + 150, hy - 20, hx + 165, hy], fill=(60, 60, 60))


ART = {"fall": draw_fall, "rocket": draw_rocket, "ship": draw_ship}


# ---------------------------------------------------------------- render
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 26

    # masthead kicker
    kick_f = f(SANSB, 15)
    n_stories = len(LEADS) + len(CARDS) + len(ALSO)
    counts = region_counts()
    right = "%d STORIES · %d REGIONS" % (n_stories, len(REGIONS))
    d.text((MX, y), "THE WORLD IN ONE DAY", font=kick_f, fill=INK)
    rw = d.textlength(right, font=kick_f)
    d.text((MX + CW - rw, y), right, font=kick_f, fill=RED)
    y += 22

    # giant date
    date_f = f(SANSB, 60)
    date = "25 NOVEMBER 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, y), date, font=date_f, fill=INK)
    y += 72
    sub_f = f(SANSB, 14)
    sub = "W E D N E S D A Y"
    sw = d.textlength(sub, font=sub_f)
    d.text(((W - sw) / 2, y), sub, font=sub_f, fill=RED)
    y += 22
    draw_rule(d, MX, MX + CW, y, color=INK, width=2)
    y += 6
    draw_rule(d, MX, MX + CW, y, color=INK, width=1)
    y += 10

    # deck line
    deck_f = f(SERIFI, 17)
    deck = ("Asia's chip rout. Shenzhou-24 lifts off. "
            "Russia cries 'terrorism'.")
    for line in wrap(d, deck, deck_f, CW):
        lw = d.textlength(line, font=deck_f)
        d.text(((W - lw) / 2, y), line, font=deck_f, fill=INK)
        y += 22
    y += 8

    # numbers strip
    draw_rule(d, MX, MX + CW, y)
    y += 8
    val_f = f(SANSB, 21)
    lab_f = f(SANSB, 10)
    col_w = CW // 5
    for i, (val, lab) in enumerate(NUMBERS):
        cx = MX + i * col_w
        vw = d.textlength(val, font=val_f)
        d.text((cx + (col_w - vw) / 2, y), val, font=val_f, fill=INK)
        lw = d.textlength(lab, font=lab_f)
        d.text((cx + (col_w - lw) / 2, y + 26), lab, font=lab_f, fill=MUTED)
        if i:
            d.line([(cx, y), (cx, y + 40)], fill=RULE, width=1)
    y += 48
    draw_rule(d, MX, MX + CW, y)
    y += 10

    # region bar
    reg_f = f(SANSB, 11)
    parts = ["%s %d" % (r.upper(), counts[r]) for r in REGIONS]
    reg_line = "  ·  ".join(parts)
    rw = d.textlength(reg_line, font=reg_f)
    d.text(((W - rw) / 2, y), reg_line, font=reg_f, fill=BLUE)
    y += 20
    draw_rule(d, MX, MX + CW, y)
    y += 8

    # UTC timeline: 5 entries, one line each
    tl_lab_f = f(SANSB, 10)
    tl_txt_f = f(SERIF, 11)
    tl_w = CW // 5
    for i, (lab, txt) in enumerate(TIMELINE):
        cx = MX + i * tl_w
        d.text((cx, y), lab, font=tl_lab_f, fill=RED)
        d.text((cx, y + 13), txt, font=tl_txt_f, fill=INK)
    y += 30
    draw_rule(d, MX, MX + CW, y)
    y += 10

    # 3 lead panels
    lead_w = (CW - 2 * 20) // 3
    head_f = f(SANSB, 14)
    body_f = f(SERIF, 11)
    tag_f = f(SANSB, 9)
    lead_top = y
    lead_bottom = y
    for i, (head, tag, body, art, _reg) in enumerate(LEADS):
        x = MX + i * (lead_w + 20)
        d.rectangle([x, y, x + lead_w, y + 68], outline=RULE, width=1)
        ART[art](d, x + 1, y + 1, lead_w - 2, 66)
        by = y + 76
        d.text((x, by), tag, font=tag_f, fill=RED)
        by += 13
        for line in wrap(d, head, head_f, lead_w):
            d.text((x, by), line, font=head_f, fill=INK)
            by += 17
        for line in wrap(d, body, body_f, lead_w):
            d.text((x, by), line, font=body_f, fill=INK)
            by += 14
        lead_bottom = max(lead_bottom, by)
    y = lead_bottom + 8
    draw_rule(d, MX, MX + CW, y)
    y += 10

    # 10 numbered cards, rows of 3/3/3/1
    num_f = f(SANSB, 13)
    chead_f = f(SANSB, 12)
    cbody_f = f(SERIF, 11)
    rows = [CARDS[0:3], CARDS[3:6], CARDS[6:9], CARDS[9:10]]
    for row in rows:
        heights = []
        for idx, (head, body, _reg) in enumerate(row):
            lines_h = wrap(d, head, chead_f, lead_w - 30)
            lines_b = wrap(d, body, cbody_f, lead_w - 30)
            heights.append(16 + 15 * len(lines_h) + 14 * len(lines_b))
        row_h = max(heights)
        for idx, (head, body, _reg) in enumerate(row):
            x = MX + idx * (lead_w + 20)
            num = "%02d" % (CARDS.index((head, body, _reg)) + 1)
            d.text((x, y), num, font=num_f, fill=RED)
            by = y + 16
            for line in wrap(d, head, chead_f, lead_w - 30):
                d.text((x + 30, by), line, font=chead_f, fill=INK)
                by += 15
            for line in wrap(d, body, cbody_f, lead_w - 30):
                d.text((x + 30, by), line, font=cbody_f, fill=INK)
                by += 14
        y += row_h + 8
    draw_rule(d, MX, MX + CW, y)
    y += 8

    # ALSO list, 2 columns
    map_lab_f = f(SANSB, 10)
    d.text((MX, y), "ALSO ON WEDNESDAY", font=map_lab_f, fill=RED)
    y += 15
    also_f = f(SERIF, 11)
    col2_w = (CW - 20) // 2
    left = ALSO[:7]
    right_items = ALSO[7:]
    max_rows = max(len(left), len(right_items))
    for r in range(max_rows):
        for ci, items in enumerate((left, right_items)):
            if r < len(items):
                txt, _reg = items[r]
                x = MX + ci * (col2_w + 20)
                num = "%02d" % (r + 1 + ci * 7)
                d.text((x, y), num, font=f(SANSB, 10), fill=MUTED)
                d.text((x + 24, y), txt, font=also_f, fill=INK)
        y += 14
    y += 4
    draw_rule(d, MX, MX + CW, y)
    y += 8

    # DATE CHECK box
    dc_f = f(SERIF, 10)
    dc_lab_f = f(SANSB, 10)
    tue = "TUE NOV 24: " + "; ".join(DATE_CHECK_TUE) + "."
    mon = "MON NOV 23: " + "; ".join(DATE_CHECK_MON) + "."
    dc_lines = wrap(d, tue, dc_f, CW - 24) + wrap(d, mon, dc_f, CW - 24)
    box_h = 16 + 14 * len(dc_lines) + 8
    d.rectangle([MX, y, MX + CW, y + box_h], outline=INK, width=1)
    d.text((MX + 12, y + 5), "DATE CHECK \u2014 NOT WEDNESDAY", font=dc_lab_f,
           fill=RED)
    ly = y + 20
    for line in dc_lines:
        d.text((MX + 12, ly), line, font=dc_f, fill=MUTED)
        ly += 14
    y += box_h + 8

    # sources
    src_f = f(SERIF, 9)
    d.text((MX, y), SOURCES, font=src_f, fill=MUTED)
    y += 13

    print("content bottom y=%d (canvas %d)" % (y, H))
    assert y <= H - 8, "overflow: content bottom %d" % y
    return img


if __name__ == "__main__":
    im = render()
    im.save("entry.png", optimize=True)
    data = open("entry.png", "rb").read()
    print("entry.png %d bytes sha256 %s"
          % (len(data), hashlib.sha256(data).hexdigest()))
