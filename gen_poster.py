#!/usr/bin/env python3
"""Render the 24 November 2026 world-news front page as a 1024x1024 PNG.

Stdlib only (struct, zlib, binascii). No fonts, no network, no clock, no
randomness: two runs write byte-identical output.
"""
import binascii
import struct
import zlib

W, H = 1024, 1024

PAPER = (247, 243, 234)
INK = (22, 22, 22)
NAVY = (20, 38, 74)
GOLD = (198, 158, 52)
RED = (172, 32, 32)
GREY = (96, 96, 96)
BOX = (233, 227, 211)
WHITE = (255, 255, 255)
RULE = (120, 110, 88)

# 5x7 bitmap font, drawn by hand: each glyph is 7 rows of 5 cells,
# '1' is ink, '0' is blank. Uppercase, digits and punctuation only.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "00000", "01100", "00000", "00000", "01100", "00000"),
    ';': ("00000", "01100", "00000", "01100", "00000", "00100", "01000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '+': ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '$': ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    '~': ("00000", "00000", "01001", "10110", "00000", "00000", "00000"),
    '_': ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    '\u2022': ("00000", "00000", "01110", "01110", "01110", "00000", "00000"),
}


class Page:
    def __init__(self):
        self.px = bytearray(PAPER * W * H)

    def _set(self, x, y, color):
        if 0 <= x < W and 0 <= y < H:
            i = (y * W + x) * 3
            self.px[i:i + 3] = bytes(color)

    def fill(self, x, y, w, h, color):
        for yy in range(y, y + h):
            base = (yy * W + x) * 3
            self.px[base:base + w * 3] = bytes(color) * w

    def outline(self, x, y, w, h, color, t=1):
        self.fill(x, y, w, t, color)
        self.fill(x, y + h - t, w, t, color)
        self.fill(x, y, t, h, color)
        self.fill(x + w - t, y, t, h, color)

    def text_w(self, s, scale):
        if not s:
            return 0
        return len(s) * 6 * scale - scale

    def draw_char(self, x, y, ch, scale, color):
        glyph = FONT.get(ch, FONT[' '])
        for r, row in enumerate(glyph):
            for c, bit in enumerate(row):
                if bit == '1':
                    self.fill(x + c * scale, y + r * scale, scale, scale, color)

    def draw(self, x, y, s, scale, color):
        for ch in s:
            self.draw_char(x, y, ch, scale, color)
            x += 6 * scale
        return x

    def draw_centred(self, cx, y, s, scale, color):
        self.draw(cx - self.text_w(s, scale) // 2, y, s, scale, color)

    def draw_right(self, right, y, s, scale, color):
        self.draw(right - self.text_w(s, scale), y, s, scale, color)

    def wrap(self, s, scale, max_w):
        lines, cur = [], ""
        for word in s.split(" "):
            trial = word if not cur else cur + " " + word
            if self.text_w(trial, scale) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    def para(self, x, y, s, scale, max_w, color, leading=6):
        for line in self.wrap(s, scale, max_w):
            self.draw(x, y, line, scale, color)
            y += 7 * scale + leading
        return y


def chunk(tag, data):
    out = struct.pack(">I", len(data)) + tag + data
    out += struct.pack(">I", binascii.crc32(tag + data) & 0xFFFFFFFF)
    return out


def write_png(page, path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += page.px[y * W * 3:(y + 1) * W * 3]
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def tag(pg, x, y, label, scale=2):
    w = pg.text_w(label, scale) + 16
    pg.fill(x, y, w, 7 * scale + 10, RED)
    pg.draw(x + 8, y + 5, label, scale, WHITE)
    return w


def card(pg, x, y, w, h, kicker, headline, body):
    pg.fill(x, y, w, h, WHITE)
    pg.outline(x, y, w, h, RULE, 1)
    pg.draw(x + 16, y + 14, kicker, 2, RED)
    yy = pg.para(x + 16, y + 40, headline, 3, w - 32, INK, leading=4)
    pg.para(x + 16, yy + 4, body, 2, w - 32, (58, 58, 58), leading=4)


NIGHT = (10, 22, 48)
MOON = (232, 230, 210)
ORANGE = (230, 120, 30)
FLAME = (245, 200, 60)
SMOKE = (180, 180, 180)
STEEL = (120, 120, 120)
PAD = (60, 60, 66)
SKYBLUE = (120, 180, 220)


def circle(pg, cx, cy, r, color):
    for yy in range(max(0, cy - r), min(H, cy + r + 1)):
        dy = yy - cy
        dx = int((r * r - dy * dy) ** 0.5)
        x0, x1 = max(0, cx - dx), min(W - 1, cx + dx)
        if x1 >= x0:
            pg.fill(x0, yy, x1 - x0 + 1, 1, color)


def tri(pg, pts, color):
    (x0, y0), (x1, y1), (x2, y2) = pts
    ys = sorted([y0, y1, y2])
    for yy in range(max(0, ys[0]), min(H, ys[2] + 1)):
        xs = []
        for (ax, ay), (bx, by) in (((x0, y0), (x1, y1)),
                                   ((x1, y1), (x2, y2)),
                                   ((x2, y2), (x0, y0))):
            if ay == by:
                continue
            if min(ay, by) <= yy <= max(ay, by):
                xs.append(ax + (bx - ax) * (yy - ay) / (by - ay))
        if len(xs) >= 2:
            xa, xb = int(min(xs)), int(max(xs))
            xa, xb = max(0, xa), min(W - 1, xb)
            if xb >= xa:
                pg.fill(xa, yy, xb - xa + 1, 1, color)


def build():
    pg = Page()
    pg.outline(14, 14, 996, 996, INK, 2)
    pg.outline(20, 20, 984, 984, RULE, 1)

    # Masthead.
    pg.fill(28, 28, 968, 104, NAVY)
    pg.draw(48, 56, "GLOBAL DAILY", 6, WHITE)
    pg.draw_right(968, 48, "WEDNESDAY", 3, GOLD)
    pg.draw_right(968, 80, "25 NOVEMBER 2026", 3, WHITE)
    pg.fill(28, 136, 968, 4, GOLD)

    # Kicker line.
    pg.draw(28, 150, "THE WORLD IN ONE PAGE", 2, INK)
    pg.draw_right(996, 150, "SOURCES: WIRE REPORTS", 2, GREY)

    # Hero panel: night launch of Shenzhou-24.
    HX, HY, HW, HH = 28, 172, 968, 264
    pg.fill(HX, HY, HW, HH, NIGHT)
    pg.outline(HX, HY, HW, HH, RULE, 1)
    for i in range(46):
        sx = 40 + (i * 173) % 920
        sy = 182 + (i * 97) % 200
        pg.fill(sx, sy, 2, 2, WHITE if i % 5 else GOLD)
    circle(pg, 150, 230, 18, MOON)
    circle(pg, 144, 224, 4, (200, 198, 180))
    circle(pg, 156, 236, 3, (200, 198, 180))
    # Tiangong station silhouette, upper middle.
    pg.fill(215, 250, 75, 18, (60, 110, 180))
    pg.fill(405, 250, 75, 18, (60, 110, 180))
    pg.fill(290, 256, 10, 6, STEEL)
    pg.fill(390, 256, 15, 6, STEEL)
    pg.fill(300, 246, 90, 26, (200, 200, 200))
    pg.outline(300, 246, 90, 26, GREY, 1)
    pg.fill(330, 240, 30, 6, (200, 200, 200))
    pg.draw(215, 280, "TIANGONG STATION", 2, GOLD)
    tag(pg, 44, 186, "SPACE")
    # Smoke, flame, fins, body, nose.
    circle(pg, 770, 412, 12, SMOKE)
    circle(pg, 872, 414, 14, SMOKE)
    circle(pg, 820, 420, 15, SMOKE)
    tri(pg, [(802, 352), (838, 352), (820, 408)], ORANGE)
    tri(pg, [(810, 352), (830, 352), (820, 388)], FLAME)
    tri(pg, [(800, 318), (772, 356), (800, 356)], (200, 200, 200))
    tri(pg, [(840, 318), (868, 356), (840, 356)], (200, 200, 200))
    pg.fill(800, 218, 40, 140, (240, 240, 240))
    pg.outline(800, 218, 40, 140, GREY, 1)
    tri(pg, [(800, 218), (840, 218), (820, 184)], RED)
    pg.fill(800, 252, 40, 10, RED)
    circle(pg, 820, 292, 9, NAVY)
    circle(pg, 820, 292, 5, SKYBLUE)
    # Launch tower and pad.
    pg.fill(752, 330, 10, 90, STEEL)
    pg.fill(752, 350, 26, 4, STEEL)
    pg.fill(752, 375, 26, 4, STEEL)
    pg.fill(736, 420, 168, 16, PAD)
    pg.draw(44, 412, "LONG MARCH 2F  •  JIUQUAN, CHINA", 2, GOLD)

    # Lead headline + deck: first foreign astronaut to Tiangong.
    pg.draw(28, 452, "FIRST FOREIGN ASTRONAUT", 7, INK)
    pg.draw(28, 508, "FLIES TO TIANGONG", 7, INK)
    pg.para(28, 570,
            "PAKISTAN'S MUHAMMAD ZEESHAN ALI, 40, RIDES CHINA'S SHENZHOU-24 "
            "TO THE TIANGONG STATION, THE FIRST FOREIGN ASTRONAUT ABOARD IT "
            "AND THE FIRST PAKISTANI IN ORBIT.",
            2, 968, (58, 58, 58), leading=6)

    # Second story: CIA / ODNI breach.
    tag(pg, 28, 646, "CYBERATTACK")
    pg.draw(28, 676, "US SPY AGENCIES HACKED", 6, INK)
    pg.para(28, 726,
            "HACKERS BREACH THE UNCLASSIFIED CIA AND ODNI NETWORK USED TO "
            "STUDY OPEN-SOURCE INTELLIGENCE. NO CLASSIFIED DATA EXPOSED, "
            "US OFFICIALS SAY.",
            2, 968, (58, 58, 58), leading=6)

    pg.fill(28, 774, 968, 2, RULE)

    # Trio row.
    card(pg, 28, 786, 312, 140, "RIYADH",
         "DRONE HITS TALLEST TOWER",
         "SECOND STRIKE IN A WEEK. 11 HURT.")
    card(pg, 352, 786, 312, 140, "CONGO",
         "EBOLA HOSPITAL EVACUATED",
         "WHO PULLS STAFF AFTER 3 DAYS OF FIGHTING.")
    card(pg, 676, 786, 312, 140, "UKRAINE",
         "KYIV CONFIRMS SHIP STRIKE",
         "ZELENSKYY CONFIRMS GULF OF FINLAND HIT.")

    # Also today.
    tag(pg, 28, 938, "ALSO TODAY")
    pg.para(176, 944,
            "HUAWEI GUILTY \u2022 NEPAL QUAKE 5.6 \u2022 GIULIANI MEDAL "
            "\u2022 SARKOZY TO TRIAL \u2022 NVIDIA -6%",
            2, 820, INK, leading=4)
    return pg


if __name__ == "__main__":
    write_png(build(), "entry.png")
