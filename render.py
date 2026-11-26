"""Draw the news-image-20261125 V2 front page.

One image, 1024x1024, summing up the world's news of Wednesday
25 November 2026. Pure PIL, Liberation fonts, no randomness, no
clock, no network: running it twice gives identical bytes.

Layout (own geometry): masthead, giant serif date, weekday, double
rule, deck, BY THE NUMBERS strip, region bar, UTC timeline, three
flat-illustrated leads, a 3x4 grid of numbered cards, an ALSO list
in two columns, a DATE CHECK box for Tuesday's news, sources line.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 34
CONTENT_W = W - 2 * MARGIN

PAPER = (247, 242, 228)
INK = (28, 25, 23)
RED = (179, 64, 47)
MUTED = (110, 103, 92)
RULE = (201, 192, 172)
NAVY = (31, 42, 68)
GREEN = (46, 125, 50)
CREAM = (247, 242, 228)

FONT_DIR = "/usr/share/fonts/truetype/liberation"
SERIF_B = os.path.join(FONT_DIR, "LiberationSerif-Bold.ttf")
SANS_B = os.path.join(FONT_DIR, "LiberationSans-Bold.ttf")
SANS_R = os.path.join(FONT_DIR, "LiberationSans-Regular.ttf")
SERIF_I = os.path.join(FONT_DIR, "LiberationSerif-Italic.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def tracked_width(fnt, text, tracking):
    total = 0
    for ch in text:
        total += fnt.getlength(ch) + tracking
    return total - tracking if text else 0


def draw_tracked(draw, cx, y, text, fnt, fill, tracking):
    """Draw text centred on cx with extra tracking between letters."""
    w = tracked_width(fnt, text, tracking)
    x = cx - w / 2
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += fnt.getlength(ch) + tracking


def draw_centred(draw, cx, y, text, fnt, fill):
    w = fnt.getlength(text)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def fit_font(path, size, text, max_w):
    """Shrink the font until the text fits max_w (never below 10)."""
    while size > 10:
        fnt = font(path, size)
        if fnt.getlength(text) <= max_w:
            return fnt
        size -= 1
    return font(path, 10)


def wrap_to_width(text, fnt, max_w, max_lines=None):
    """Greedy word wrap by pixel width; returns a list of lines."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if fnt.getlength(trial) <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    if max_lines is not None:
        lines = lines[:max_lines]
    return lines


# ---------------------------------------------------------------- art panels
# Each panel is drawn on its own layer exactly the panel size, then
# pasted, so art can never spill outside its box.

PANEL_W, PANEL_H = 308, 60


def art_tariffs():
    """Tariff bars: four rising cream bars on navy, last one red."""
    layer = Image.new("RGB", (PANEL_W, PANEL_H), NAVY)
    d = ImageDraw.Draw(layer)
    base = PANEL_H - 8
    heights = [16, 26, 36, 46]
    bw = 34
    gap = 18
    x = 22
    for i, h in enumerate(heights):
        colour = RED if i == 3 else CREAM
        d.rectangle([x, base - h, x + bw, base], fill=colour)
        x += bw + gap
    d.line([(12, base), (PANEL_W - 12, base)], fill=CREAM, width=2)
    d.ellipse([PANEL_W - 46, 8, PANEL_W - 30, 24], fill=RED)
    return layer


def art_chips():
    """Chip rout: five falling bars plus a small chip square."""
    layer = Image.new("RGB", (PANEL_W, PANEL_H), (122, 42, 30))
    d = ImageDraw.Draw(layer)
    base = PANEL_H - 8
    heights = [46, 38, 30, 22, 14]
    bw = 22
    gap = 10
    x = 18
    for h in heights:
        d.rectangle([x, base - h, x + bw, base], fill=CREAM)
        x += bw + gap
    # chip square, top right
    cx0, cy0, s = PANEL_W - 62, 8, 34
    d.rectangle([cx0, cy0, cx0 + s, cy0 + s], fill=INK)
    d.rectangle([cx0 + 8, cy0 + 8, cx0 + s - 8, cy0 + s - 8],
                outline=CREAM, width=2)
    for px in (cx0 + 4, cx0 + s - 4):
        for py in (cy0 + 10, cy0 + 24):
            d.line([(px, py), (px + (6 if px < cx0 + s / 2 else -6), py)],
                   fill=CREAM, width=2)
    return layer


def art_economy():
    """Hot inflation, strong growth: a rising green line on cream."""
    layer = Image.new("RGB", (PANEL_W, PANEL_H), (240, 233, 214))
    d = ImageDraw.Draw(layer)
    d.rectangle([0, 0, PANEL_W - 1, PANEL_H - 1], outline=RULE, width=1)
    pts = [(14, 46), (48, 40), (82, 43), (116, 30), (150, 33),
           (184, 20), (218, 23), (252, 10), (290, 12)]
    d.line(pts, fill=GREEN, width=3, joint="curve")
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=GREEN)
    d.ellipse([290 - 5, 12 - 5, 290 + 5, 12 + 5], fill=RED)
    d.rectangle([14, PANEL_H - 12, 60, PANEL_H - 8], fill=RED)
    d.rectangle([70, PANEL_H - 16, 116, PANEL_H - 8], fill=MUTED)
    return layer


# ------------------------------------------------------------------- content

LEADS = [
    {
        "tag": "AMERICAS · TRADE",
        "headline": "TRUMP TARIFFS 14 PARTNERS",
        "body": ("USTR proposes duties on 14 economies to fight excess "
                 "capacity. China capped 20%, 40% if the truce fails. "
                 "EU 15%."),
        "art": art_tariffs,
    },
    {
        "tag": "EAST ASIA · MARKETS",
        "headline": "ASIA CHIP ROUT: KOSPI −6.2%",
        "body": ("Kospi fell 6.2% to 4,698, Nikkei 2.8%, Taiex 4.8%. "
                 "SoftBank sank 14.8%; AI-spending doubts and tariff "
                 "fears drove the rout."),
        "art": art_chips,
    },
    {
        "tag": "AMERICAS · ECONOMY",
        "headline": "PCE HOT, GDP 4.3%",
        "body": ("Core PCE rose 3.3% on the year, above forecast; "
                 "headline 3.8%. Q3 GDP was revised up to 4.3%. A Dec "
                 "hike looks near-certain."),
        "art": art_economy,
    },
]

CARDS = [
    ("04", "EAST ASIA · SPACE", "SHENZHOU-24 LIFTS OFF",
     "Shenzhou-24 lifts off. Pakistan's Zeeshan Ali is the first "
     "foreign crew member on China's station."),
    ("05", "EUROPE · WAR", "RUSSIA CRIES 'TERRORISM'",
     "Moscow accuses Kyiv of terrorism after drone attacks on ships "
     "in the Baltic Sea and off Libya."),
    ("06", "AMERICAS · MARKETS", "DOW ERASES 1,100-POINT PLUNGE",
     "Dow gained 0.3% to 50,183 after an intraday plunge of 1,100 "
     "points. S&P fell 0.3%; Nasdaq 0.6%."),
    ("07", "WORLD · FED", "FED: COSTS OUTRUN PRICES",
     "Eight of 12 districts grew; wages rose moderately. Spending "
     "stayed flat as households traded down."),
    ("08", "EUROPE · CHESS", "GUKESH GAME 2: 20-MOVE DRAW",
     "A 20-move London draw by repetition. Match tied 1-1; Game 3 "
     "Thursday, Sindarov has White."),
    ("09", "MIDDLE EAST · WAR", "HORMUZ TANKERS 'HIT BY MINES'",
     "IRGC says two tankers struck mines; the claim is "
     "unconfirmed. Houthis say they hit a Saudi refinery."),
    ("10", "OCEANIA · ECONOMY", "AUSTRALIA CPI HOTTER",
     "October prices beat forecasts; trimmed mean 3.8%, above "
     "target. The Australian dollar jumped."),
    ("11", "MIDDLE EAST · WAR", "ISRAEL WARNS IRAN",
     "Katz says Iran is developing chemical weapons and vows to stop "
     "it, floating a pre-emptive strike."),
    ("12", "AFRICA · WAR", "19 KILLED IN SUDAN STRIKES",
     "RSF drones struck homes in Damazin. Nineteen civilians were "
     "killed and 20 hurt, lawyers said."),
    ("13", "SOUTH ASIA · POLITICS", "BJP, AKALI DAL REUNITE",
     "BJP and Akali Dal announce an alliance for the 2027 Punjab "
     "elections after a six-year split."),
]

ALSO_LEFT = [
    "Kioxia −14.2%, Advantest −12.9%, Tokyo Electron −13%",
    "Samsung −9.9%, SK Hynix −11.1%",
    "TSMC −3.6%, MediaTek −10%",
    "MSCI Asia Pacific −2.3%",
    "Nifty +1.8% to 25,816, against the tide",
    "Jobless claims 189K; income +0.7%, spending +0.3%",
    "WTI crude +2.5% to $84.08",
]

ALSO_RIGHT = [
    "Brazil: 10% tariff on Embraer jets, higher sugar duties",
    "Libya vows retaliation after 2 officers killed in Benghazi strike",
    "Medvedev sets out nuclear pre-emption terms",
    "Chinese warships reach Ream base for Cambodia drills",
    "Japan pulls car suppliers into drone arms push",
    "Spain votes Sunday; PP leads polls",
]

NUMBERS = [
    ("−6.2%", "KOSPI"),
    ("3.3%", "CORE PCE"),
    ("4.3%", "Q3 GDP"),
    ("+0.3%", "DOW"),
    ("−0.6%", "NASDAQ"),
]

TIMELINE = [
    ("00:30", "Aus CPI hotter"),
    ("13:30", "PCE + GDP"),
    ("14:16", "USTR tariffs"),
    ("19:00", "Beige Book"),
    ("21:00", "US close"),
]

REGION_BAR = ("EAST ASIA 7 · AMERICAS 5 · EUROPE 4 · MIDDLE EAST 3 · "
              "WORLD 2 · SOUTH ASIA 2 · OCEANIA 1 · AFRICA 1 · SE ASIA 1")

DATE_CHECK = ("US close Tue: S&P −0.50%, Nasdaq −1.48%, Dow +0.85%. CAS "
              "restores Senegal as AFCON champions. Gukesh–Sindarov Game "
              "1 draw. Sanofi buys Insmed for $41bn. Saudi 2027 budget "
              "approved. Iran rial record low, 2.82m per dollar. England "
              "beat Australia by 8 wickets. Nvidia −6% after +31.5% "
              "Monday. Houthis hit Riyadh tower, 11 hurt. Huawei guilty "
              "of trade-secret theft. (Mon) Cikande fire toll 24 "
              "confirmed. COP31 ends with no deal (Sun).")

SOURCES = ("Sources: Reuters · AP · BEA · Fed · ChessBase · "
           "detikNews/AFP · Emergency Lawyers · Just Security | "
           "EDITION TO 23:59 UTC · 26 STORIES · 9 REGIONS")


def build():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # Masthead + date + weekday.
    draw_tracked(d, W // 2, 24, "THE WORLD IN ONE DAY",
                 font(SANS_B, 18), INK, 3)
    draw_centred(d, W // 2, 46, "25 NOVEMBER 2026",
                 font(SERIF_B, 62), INK)
    draw_tracked(d, W // 2, 110, "WEDNESDAY",
                 font(SANS_B, 15), RED, 6)

    # Double rule.
    d.line([(MARGIN, 132), (W - MARGIN, 132)], fill=INK, width=2)
    d.line([(MARGIN, 138), (W - MARGIN, 138)], fill=INK, width=1)

    # Deck: the three leads in one line.
    draw_centred(d, W // 2, 148,
                 "US proposes tariffs on 14 partners  ·  Asia chip rout "
                 "deepens  ·  PCE hot as GDP hits 4.3%",
                 font(SERIF_I, 14), INK)

    # BY THE NUMBERS strip.
    draw_tracked(d, W // 2, 172, "BY THE NUMBERS",
                 font(SANS_B, 11), MUTED, 2)
    col_w = CONTENT_W / 5
    for i, (value, label) in enumerate(NUMBERS):
        cx = MARGIN + col_w * i + col_w / 2
        draw_centred(d, cx, 188, value, font(SANS_B, 26), RED)
        draw_centred(d, cx, 218, label, font(SANS_B, 10), MUTED)

    # Region bar.
    draw_centred(d, W // 2, 240, REGION_BAR, font(SANS_R, 10), MUTED)

    # UTC timeline.
    draw_tracked(d, W // 2, 258, "THE DAY IN UTC",
                 font(SANS_B, 11), MUTED, 2)
    for i, (when, what) in enumerate(TIMELINE):
        cx = MARGIN + col_w * i + col_w / 2
        time_fnt = font(SANS_B, 11)
        label_fnt = font(SANS_R, 11)
        total = time_fnt.getlength(when) + 6 + label_fnt.getlength(what)
        tx = cx - total / 2
        d.text((tx, 274), when, font=time_fnt, fill=RED)
        d.text((tx + time_fnt.getlength(when) + 6, 274), what,
               font=label_fnt, fill=INK)

    # Rule above the leads.
    d.line([(MARGIN, 292), (W - MARGIN, 292)], fill=RULE, width=1)

    # Three leads.
    lead_w = 308
    lead_gap = 16
    body_fnt = font(SANS_R, 13)
    for i, lead in enumerate(LEADS):
        x = MARGIN + i * (lead_w + lead_gap)
        panel = lead["art"]()
        page.paste(panel, (x, 300))
        draw_tracked(d, x + lead_w // 2, 368, lead["tag"],
                     font(SANS_B, 11), RED, 1)
        headline_fnt = fit_font(SANS_B, 17, lead["headline"], lead_w)
        draw_centred(d, x + lead_w // 2, 384, lead["headline"],
                     headline_fnt, INK)
        lines = wrap_to_width(lead["body"], body_fnt, lead_w, max_lines=3)
        y = 404
        for line in lines:
            d.text((x, y), line, font=body_fnt, fill=INK)
            y += 15

    # Numbered cards: 3 columns x 4 rows.
    card_pitch = 68
    card_y0 = 480
    num_fnt = font(SANS_B, 14)
    tag_fnt = font(SANS_R, 10)
    head_fnt_size = 18
    card_body_fnt = font(SANS_R, 12)
    for idx, (num, tag, headline, body) in enumerate(CARDS):
        row, col = divmod(idx, 3)
        x = MARGIN + col * (lead_w + lead_gap)
        y = card_y0 + row * card_pitch
        d.text((x, y), num, font=num_fnt, fill=RED)
        tag_x = x + num_fnt.getlength(num) + 8
        d.text((tag_x, y + 2), tag, font=tag_fnt, fill=MUTED)
        headline_fnt = fit_font(SANS_B, head_fnt_size, headline, lead_w)
        d.text((x, y + 18), headline, font=headline_fnt, fill=INK)
        lines = wrap_to_width(body, card_body_fnt, lead_w, max_lines=2)
        by = y + 40
        for line in lines:
            d.text((x, by), line, font=card_body_fnt, fill=INK)
            by += 15

    # ALSO list, two columns.
    draw_tracked(d, MARGIN + 20, 760, "ALSO", font(SANS_B, 11), INK, 2)
    also_fnt = font(SANS_R, 12)
    also_x = [MARGIN, MARGIN + CONTENT_W // 2 + 8]
    also_cols = [ALSO_LEFT, ALSO_RIGHT]
    for ci, items in enumerate(also_cols):
        y = 776
        for item in items:
            d.text((also_x[ci], y), item, font=also_fnt, fill=INK)
            y += 13

    # DATE CHECK box.
    box_y0, box_y1 = 892, 972
    d.rectangle([MARGIN, box_y0, W - MARGIN, box_y1], outline=INK, width=1)
    draw_tracked(d, MARGIN + 110, box_y0 + 8, "DATE CHECK — NOT WEDNESDAY",
                 font(SANS_B, 11), RED, 1)
    check_fnt = font(SANS_R, 12)
    lines = wrap_to_width(DATE_CHECK, check_fnt, CONTENT_W - 24)
    y = box_y0 + 26
    for line in lines:
        d.text((MARGIN + 12, y), line, font=check_fnt, fill=INK)
        y += 15

    # Sources line.
    draw_centred(d, W // 2, 986, SOURCES, font(SANS_R, 10), MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    page.save(out, "PNG")
    return out


if __name__ == "__main__":
    print(build())
