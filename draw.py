#!/usr/bin/env python3
"""news-23 b121 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
31 stories. Output: entry.png (1024x1024, <1 MiB). Run: python3 draw.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FD = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Greedy wrap; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def chip(d, x, y, label, bg, fg="white", font=None, h=13):
    font = font or f(SANS_B, 8)
    w = int(d.textlength(label, font=font)) + 8
    d.rounded_rectangle([x, y, x + w, y + h], radius=2, fill=bg)
    d.text((x + 4, y + 2), label, font=font, fill=fg)
    return w


def main():
    img = Image.new("RGB", (W, H), "#F7F2E7")
    d = ImageDraw.Draw(img)

    NAVY = "#0B1F4B"
    RED = "#B00020"
    GREEN = "#1E6B3A"
    GOLD = "#C9A227"
    CREAM = "#F5EFE0"
    INK = "#1A1A1A"
    GREY = "#5A5A5A"

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 52], fill="#111111")
    d.text((16, 6), "THE WORLD TODAY", font=f(SERIF_B, 38), fill="white")
    date = "MONDAY 23 NOVEMBER 2026"
    d.text((W - 16 - d.textlength(date, font=f(SANS_B, 16)), 18),
           date, font=f(SANS_B, 16), fill=GOLD)

    # ---------- kicker ----------
    d.rectangle([0, 52, W, 70], fill=RED)
    kick = "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B"
    d.text(((W - d.textlength(kick, font=f(SANS_B, 11))) / 2, 56),
           kick, font=f(SANS_B, 11), fill="white")

    # ---------- number strip (2 rows x 5) ----------
    nums = [
        ("-3.3%", "KOSPI"), ("5.3", "US-CHINA POWER GAP"),
        ("11,762", "EBOLA CASES, DRC"), ("10T won", "SEOUL STABILISATION FUND"),
        ("2%", "BILLIONAIRE TAX IN PARIS"),
        ("$450M", "SKUBAL DEAL"), ("165", "RUSSIAN MISSILES/WEEK"),
        ("12,000", "CLEARED IN MANCHESTER"), ("264 kg", "EXPLOSIVES SEIZED"),
        ("$107.3B", "ANTHROPIC IPO"),
    ]
    xs = [8, 212, 416, 620, 824]
    for i, (val, lab) in enumerate(nums):
        col, row = i % 5, i // 5
        x = xs[col]
        vy = 76 + row * 36
        d.text((x, vy), val, font=f(SANS_B, 20), fill=INK)
        d.text((x, vy + 23), lab, font=f(SANS_B, 9), fill=GREY)

    # ---------- region bar ----------
    segs = [("ASIA-PACIFIC 7", NAVY, 227), ("AMERICAS 8", RED, 260),
            ("MIDDLE EAST 6", "#0E7C7B", 195), ("EUROPE 5", "#5B2D8E", 163),
            ("AFRICA 3", GREEN, 98), ("WORLD 2", "#555555", 65)]
    x = 8
    for label, col, w in segs:
        d.rectangle([x, 146, x + w, 164], fill=col)
        tw = d.textlength(label, font=f(SANS_B, 10))
        d.text((x + (w - tw) / 2, 150), label, font=f(SANS_B, 10), fill="white")
        x += w

    # ---------- UTC strip ----------
    utc = "THE DAY IN UTC  \u00b7  ~00:00 Kospi dives  \u00b7  ~05:30 Guterres opens  \u00b7  ~09:00 Power Index  \u00b7  ~12:00 Paris 2% tax  \u00b7  ~15:00 Kyiv missiles"
    d.text((8, 168), utc, font=f(SANS, 9), fill=GREY)
    d.text((W - 8 - d.textlength("~ APPROX", font=f(SANS, 9)), 168),
           "~ APPROX", font=f(SANS, 9), fill=GREY)

    # ---------- hero scenes ----------
    hx = [8, 348, 688]
    hw = 328
    sy, sh = 182, 140  # scene top, height

    # scene 1: Kospi skyline + falling chart
    d.rectangle([hx[0], sy, hx[0] + hw, sy + sh], fill=NAVY)
    import random
    random.seed(7)
    for bx in range(hx[0] + 8, hx[0] + hw - 8, 26):
        bh = random.randint(34, 78)
        d.rectangle([bx, sy + sh - 26 - bh, bx + 20, sy + sh - 26], fill="#132E63")
        for wy in range(sy + sh - 22 - bh, sy + sh - 28, 9):
            for wx in (bx + 4, bx + 12):
                if random.random() < 0.6:
                    d.rectangle([wx, wy, wx + 4, wy + 4], fill="#FFD76A")
    pts = [(hx[0] + 14, sy + 34), (hx[0] + 70, sy + 52), (hx[0] + 120, sy + 46),
           (hx[0] + 175, sy + 66), (hx[0] + 230, sy + 74), (hx[0] + 285, sy + 92),
           (hx[0] + 314, sy + 100)]
    d.line(pts, fill="#FF7A1A", width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill="white")
    d.rectangle([hx[0], sy, hx[0] + 150, sy + 40], fill=NAVY)
    d.text((hx[0] + 10, sy + 4), "\u22123.3%", font=f(SANS_B, 32), fill="white")
    d.rectangle([hx[0], sy + sh - 22, hx[0] + hw, sy + sh], fill=NAVY)
    d.text((hx[0] + 10, sy + sh - 19), "KOSPI 4,708.54  \u00b7  \u2212161 PTS",
           font=f(SANS_B, 11), fill="white")

    # scene 2: Guterres / 150 delegates
    d.rectangle([hx[1], sy, hx[1] + hw, sy + sh], fill=GREEN)
    d.text((hx[1] + 12, sy + 6), "150", font=f(SANS_B, 44), fill=GOLD)
    for j, ln in enumerate(["DELEGATES", "BACK A RISK", "FRAMEWORK"]):
        d.text((hx[1] + 12, sy + 58 + j * 20), ln, font=f(SANS_B, 17), fill=GOLD)
    cx, cy, r = hx[1] + 268, sy + 66, 42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#BFE3C0",
              outline="#8FCB96", width=2)
    for k in range(-2, 3):
        d.arc([cx - r + abs(k) * 12, cy - r, cx + r - abs(k) * 12, cy + r],
              90 if k >= 0 else 270, 270 if k >= 0 else 90, fill="#5FA86A", width=1)
    d.line([cx - r, cy, cx + r, cy], fill="#5FA86A", width=1)
    d.line([cx, cy - r, cx, cy + r], fill="#5FA86A", width=1)

    # scene 3: Power Index bars
    d.rectangle([hx[2], sy, hx[2] + hw, sy + sh], fill=CREAM)
    d.text((hx[2] + 12, sy + 6), "NARROWEST SINCE 2018", font=f(SANS_B, 13), fill=INK)
    d.text((hx[2] + hw - 12 - d.textlength("GAP 5.3", font=f(SANS_B, 13)), sy + 6),
           "GAP 5.3", font=f(SANS_B, 13), fill=RED)
    bars = [("78.9", "US", NAVY, 52), ("73.6", "CHINA", RED, 48),
            ("40.5", "INDIA", GOLD, 27)]
    bx0 = hx[2] + 22
    for j, (val, lab, col, bh) in enumerate(bars):
        bx = bx0 + j * 104
        d.text((bx + 14, sy + 34), val, font=f(SANS_B, 15), fill=INK)
        by = sy + 58 + (52 - bh)
        d.rectangle([bx, by, bx + 72, by + bh], fill=col)
        lw = d.textlength(lab, font=f(SANS_B, 11))
        d.text((bx + (72 - lw) / 2, by + (bh - 13) / 2), lab,
               font=f(SANS_B, 11), fill="white")

    # ---------- hero text blocks ----------
    heroes = [
        ("AI ROUT HITS ASIA",
         "Kospi closes \u22123.3% to 4,708.54, sheds 161 pts; intraday \u22125.8%. Samsung \u22123.1%, SK Hynix \u22122.5%.",
         "KOREA EXCHANGE"),
        ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
         "UNITED NATIONS"),
        ("US LEAD OVER CHINA AT RECORD LOW",
         "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
         "LOWY INSTITUTE"),
    ]
    ty = sy + sh + 8  # 330
    for j, (head, body, src) in enumerate(heroes):
        x = hx[j]
        hl = wrap(d, head, f(SANS_B, 16), hw)[:2]
        for k, ln in enumerate(hl):
            d.text((x, ty + k * 19), ln, font=f(SANS_B, 16), fill=INK)
        bl = wrap(d, body, f(SANS, 11), hw)[:2]
        for k, ln in enumerate(bl):
            d.text((x, ty + 44 + k * 14), ln, font=f(SANS, 11), fill=INK)
        sy2 = ty + 76
        d.text((x, sy2), src, font=f(SANS, 9), fill=GREY)
        chip(d, x + hw - 62, sy2 - 2, "REPORTED", NAVY)

    # ---------- MORE OF THE DAY strip ----------
    d.rectangle([0, 462, W, 480], fill="#111111")
    d.text((16, 466), "MORE OF THE DAY  \u2014  10 STORIES",
           font=f(SANS_B, 12), fill="white")

    # ---------- 10 cards ----------
    cards = [
        ("AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "WSJ", "REPORTED"),
        ("AMERICAS", "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
        ("WHITE HOUSE", "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
        ("MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED"),
        ("SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year, largest ever.", "AP", "REPORTED"),
        ("SPORT", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED"),
        ("LEGAL", "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED"),
        ("TECH", "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED"),
        ("EUROPE", "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM"),
        ("SPACE", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
    ]
    cxs = [8, 210, 412, 614, 816]
    for i, (cat, head, body, src, tag) in enumerate(cards):
        col, row = i % 5, i // 5
        cx, cy = cxs[col], 480 + row * 64
        d.rectangle([cx, cy, cx + 200, cy + 64], outline="#C9C2B2", width=1)
        d.text((cx + 6, cy + 5), cat, font=f(SANS_B, 8), fill=RED)
        d.text((cx + 194 - d.textlength(str(i + 1), font=f(SANS_B, 10)), cy + 4),
               str(i + 1), font=f(SANS_B, 10), fill=RED)
        hl = wrap(d, head, f(SANS_B, 11), 188)[:2]
        for k, ln in enumerate(hl):
            d.text((cx + 6, cy + 17 + k * 13), ln, font=f(SANS_B, 11), fill=INK)
        d.text((cx + 6, cy + 45), body, font=f(SANS, 9), fill=INK)
        d.text((cx + 6, cy + 56), src, font=f(SANS, 8), fill=GREY)
        tagcol = NAVY if tag == "REPORTED" else RED
        chip(d, cx + 200 - 62, cy + 52, tag, tagcol)

    # ---------- WHERE IT HAPPENED strip ----------
    d.rectangle([0, 608, W, 626], fill="#111111")
    d.text((16, 612), "WHERE IT HAPPENED", font=f(SANS_B, 12), fill="white")

    # ---------- map ----------
    mapcol = "#BFD9A8"
    # Americas blob
    d.polygon([(18, 700), (30, 650), (70, 636), (110, 640), (128, 668),
               (120, 720), (96, 772), (70, 786), (40, 770), (22, 730)],
              fill=mapcol)
    # Europe blob
    d.polygon([(136, 642), (168, 624), (214, 628), (238, 648), (232, 680),
               (204, 696), (168, 694), (142, 672)], fill=mapcol)
    # Asia blob
    d.polygon([(228, 646), (280, 632), (318, 640), (326, 668), (312, 700),
               (282, 722), (242, 712), (230, 682)], fill=mapcol)
    # Africa blob
    d.polygon([(150, 700), (190, 696), (212, 712), (206, 748), (186, 776),
               (164, 762), (150, 730)], fill=mapcol)
    pins = [(292, 668), (68, 768), (302, 692), (58, 700), (72, 672),
            (212, 664), (186, 676), (170, 660), (226, 650), (152, 650),
            (248, 690), (256, 706), (196, 760)]
    for i, (px, py) in enumerate(pins, 1):
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline="white", width=1)
        lbl = str(i)
        d.text((px - d.textlength(lbl, font=f(SANS_B, 9)) / 2, py - 5),
               lbl, font=f(SANS_B, 9), fill="white")
    leg = ["Pins 1\u201313: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing",
           "4 Washington \u00b7 5 New York \u00b7 6 Kyiv \u00b7 7 Paris",
           "8 London \u00b7 9 Warsaw \u00b7 10 Manchester \u00b7 11 Beirut",
           "12 Gaza \u00b7 13 Khartoum"]
    for k, ln in enumerate(leg):
        d.text((8, 790 + k * 10), ln, font=f(SANS, 8), fill=GREY)

    # ---------- ALSO ON MONDAY ----------
    d.text((348, 632), "ALSO ON MONDAY", font=f(SANS_B, 13), fill=INK)
    also = [
        "Paris: 100+ back 2% billionaire tax",
        "Manchester: 12,000 cleared",
        "Zelenskyy: 165 missiles in a week",
        "COP31: the day after Antalya pact rejected",
        "Israel unity talks resume",
        "Gaza: two killed in Israeli strike",
        "West Bank settler attacks",
        "Iran war: no deal in sight",
        "Lebanon seizes 264 kg explosives",
        "Bahrain: strike hits plant, 2 hurt",
        "Benghazi: UN demands probe",
        "Sudan: defences down drones",
        "DRC: fighting traps Ebola teams",
        "Bangladesh: Hasina jailed if she returns",
        "Seoul minister quits in exam row",
        "SK Telecom \u22127.3% as hype cools",
        "China eases margin rules",
        "Seoul readies 10T-won fund",
    ]
    claim_idx = {10, 11}  # 0-based: Benghazi (23), Sudan (24) -> items 24, 25
    for i, item in enumerate(also):
        col = i // 9
        row = i % 9
        x = 348 + col * 342
        y = 654 + row * 20
        num = 14 + i
        d.text((x, y), f"{num}. {item}", font=f(SANS, 11), fill=INK)
        if i in claim_idx:
            tw = d.textlength(f"{num}. {item}", font=f(SANS, 11))
            d.text((x + tw + 4, y), "[CLAIM]", font=f(SANS_B, 10), fill=RED)

    # ---------- DATE CHECK ----------
    d.rectangle([8, 830, 1016, 908], outline=RED, width=2)
    d.text((16, 838), "DATE CHECK  \u2014  READ 23 NOV 2026, 23:59 UTC  \u00b7  STORIES DATED 23 NOV ONLY",
           font=f(SANS_B, 12), fill=RED)
    d.text((16, 862), "LEFT OUT \u2014 NOT 23 NOV: Dems reach 258 (22 Nov)  \u00b7  Sparta II fire (22 Nov)  \u00b7  El Chapo Isidro captured (22 Nov)",
           font=f(SANS, 11), fill=INK)
    d.text((16, 878), "EU\u2013Indonesia pact (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  ICJ Myanmar ruling (19 Nov)",
           font=f(SANS, 11), fill=INK)
    d.text((16, 894), "NOT YET \u2014 Dymer search continues (14 missing)  \u00b7  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  WHO evacuating trapped Ebola staff",
           font=f(SANS, 11), fill=INK)

    # ---------- footer ----------
    d.text((16, 918), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
           font=f(SANS, 9), fill=GREY)
    d.text((16, 934), "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one side's claim, not independently confirmed \u00b7 ONGOING = still developing.",
           font=f(SANS, 9), fill=GREY)
    d.text((16, 950), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
           font=f(SANS, 9), fill=GREY)
    foot = "THE WORLD TODAY  \u00b7  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions"
    d.text(((W - d.textlength(foot, font=f(SANS_B, 12))) / 2, 984),
           foot, font=f(SANS_B, 12), fill=GOLD)

    img.save(OUT, optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
