#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page (1024x1024 PNG).

Four-panel split screen under a headline banner, plus a bottom ticker.
All artwork is drawn from scratch with Pillow primitives; no photos,
no network, no external assets.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REGULAR = os.path.join(FONT_DIR, "DejaVuSans.ttf")

NAVY = (11, 31, 58)
INK = (16, 24, 40)
GOLD = (245, 179, 1)
RED = (229, 72, 77)
CYAN = (41, 182, 246)
ORANGE = (245, 124, 0)
WHITE = (255, 255, 255)
SOFT = (199, 208, 220)
BLACK = (10, 10, 12)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, size, max_w):
    """Largest font size at or below `size` that fits `text` in max_w."""
    while size > 8:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, 8)


def centered(draw, cx, y, text, fnt, fill):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)


def gradient(draw, box, top, bottom):
    """Vertical gradient across box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    span = max(1, y1 - y0)
    for yy in range(y0, y1):
        t = (yy - y0) / span
        col = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(x0, yy), (x1 - 1, yy)], fill=col)


def star_points(cx, cy, r_out, r_in, points=5, rot=-90):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / points)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def burst(draw, cx, cy, r_out, r_in, spikes, fill):
    draw.polygon(star_points(cx, cy, r_out, r_in, spikes, rot=-90),
                 fill=fill)


def skyline(draw, x0, y_base, x1, heights, color, windows=False):
    """Row of dark buildings between x0 and x1, tops at y_base - height."""
    n = len(heights)
    bw = (x1 - x0) / n
    for i, h in enumerate(heights):
        bx0 = x0 + i * bw + 2
        bx1 = x0 + (i + 1) * bw - 2
        draw.rectangle([bx0, y_base - h, bx1, y_base], fill=color)
        if windows:
            for wy in range(int(y_base - h) + 8, int(y_base) - 6, 14):
                for wx in range(int(bx0) + 5, int(bx1) - 5, 12):
                    if (wx * 7 + wy * 13) % 5 == 0:
                        draw.rectangle([wx, wy, wx + 3, wy + 4],
                                       fill=(255, 214, 90))


def flag_us(draw, x, y, w, h):
    stripe = h / 7
    for i in range(7):
        col = (178, 34, 52) if i % 2 == 0 else WHITE
        draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                       fill=col)
    draw.rectangle([x, y, x + w * 0.42, y + stripe * 4], fill=(30, 58, 138))
    for r in range(3):
        for c in range(4):
            draw.ellipse([x + 4 + c * 9, y + 4 + r * 8,
                          x + 7 + c * 9, y + 7 + r * 8], fill=WHITE)


def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    draw.polygon(star_points(x + w * 0.22, y + h * 0.30, 9, 3.6),
                 fill=(255, 222, 0))
    for sx, sy in [(0.52, 0.14), (0.66, 0.28), (0.66, 0.50), (0.52, 0.64)]:
        draw.polygon(star_points(x + w * sx, y + h * sy, 4.5, 1.8),
                     fill=(255, 222, 0))


def flag_ru(draw, x, y, w, h):
    for i, col in enumerate([WHITE, (0, 90, 180), (220, 30, 30)]):
        draw.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3],
                       fill=col)


def chip(draw, x, y, label, fill):
    f = font(BOLD, 21)
    tw = draw.textlength(label, font=f)
    draw.rounded_rectangle([x, y, x + tw + 22, y + 32], radius=6, fill=fill)
    draw.text((x + 11, y + 4), label, font=f, fill=WHITE)


def caption_bar(draw, box, accent, lines, sub):
    """Dark bar with accent stripe, two headline lines and a sub-line."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    draw.rectangle([x0, y0, x1, y0 + 5], fill=accent)
    f1 = fit_font(draw, max(lines, key=len), BOLD, 27, x1 - x0 - 28)
    yy = y0 + 13
    for line in lines:
        draw.text((x0 + 14, yy), line, font=f1, fill=WHITE)
        yy += 33
    f2 = font(REGULAR, 19)
    draw.text((x0 + 14, yy + 2), sub, font=f2, fill=SOFT)


def panel_frame(draw, box):
    draw.rectangle(box, outline=WHITE, width=3)


# ---------------------------------------------------------------- scenes

def scene_summit(draw, box):
    x0, y0, x1, y1 = box
    gradient(draw, box, (27, 42, 74), (232, 132, 60))
    # low sun
    draw.ellipse([x0 + 330, y0 + 150, x0 + 420, y0 + 240],
                 fill=(255, 205, 110))
    horizon = y1 - 58
    skyline(draw, x0, horizon, x1,
            [120, 70, 150, 95, 180, 80, 130, 60, 165, 90, 140, 75],
            INK, windows=True)
    draw.rectangle([x0, horizon, x1, y1], fill=(20, 20, 28))
    # three flagpoles
    pole_y = y1 - 6
    pole_top = y0 + 96
    for i, flag in enumerate([flag_us, flag_cn, flag_ru]):
        px = x0 + 110 + i * 145
        draw.rectangle([px, pole_top, px + 4, pole_y], fill=(210, 210, 210))
        flag(draw, px + 4, pole_top + 6, 92, 52)


def scene_war(draw, box):
    x0, y0, x1, y1 = box
    gradient(draw, [x0, y0, x1, y0 + 90], (42, 63, 85), (14, 42, 74))
    horizon = y0 + 90
    gradient(draw, [x0, horizon, x1, y1], (14, 42, 74), (10, 28, 52))
    # waves
    for wy in range(horizon + 26, y1 - 10, 26):
        for k in range(6):
            wx = x0 + 20 + k * 82 + (wy % 40)
            draw.arc([wx, wy, wx + 46, wy + 16], 200, 340,
                     fill=(90, 140, 190), width=3)
    # ships
    def ship(sx, sy, scale):
        draw.polygon([(sx, sy), (sx + 150 * scale, sy),
                      (sx + 128 * scale, sy + 26 * scale),
                      (sx + 22 * scale, sy + 26 * scale)], fill=(38, 48, 62))
        draw.rectangle([sx + 52 * scale, sy - 26 * scale,
                        sx + 96 * scale, sy], fill=(70, 82, 100))
        draw.rectangle([sx + 62 * scale, sy - 40 * scale,
                        sx + 72 * scale, sy - 26 * scale], fill=(70, 82, 100))
    ship(x0 + 40, y1 - 96, 1.0)
    ship(x0 + 300, y1 - 150, 0.75)
    # explosion bursts and smoke
    burst(draw, x0 + 250, y0 + 150, 46, 18, 9, (255, 140, 30))
    burst(draw, x0 + 250, y0 + 150, 26, 10, 9, (255, 210, 80))
    burst(draw, x0 + 420, y0 + 105, 34, 14, 8, (255, 140, 30))
    burst(draw, x0 + 420, y0 + 105, 18, 7, 8, (255, 210, 80))
    for cx, cy, r in [(x0 + 215, y0 + 105, 26), (x0 + 255, y0 + 88, 32),
                      (x0 + 300, y0 + 108, 22), (x0 + 395, y0 + 70, 22)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r * 0.8],
                     fill=(120, 120, 125))
    # warning triangle, top-right corner (clear of the WAR chip)
    tx, ty = x1 - 96, y0 + 20
    draw.polygon([(tx, ty + 44), (tx + 50, ty + 44), (tx + 25, ty)],
                 outline=(255, 60, 50), width=5)
    wf = font(BOLD, 30)
    draw.text((tx + 19, ty + 10), "!", font=wf, fill=(255, 60, 50))


def scene_storm(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(6, 40, 61))
    cx, cy = x0 + 250, y0 + 150
    # spiral arms
    for k in range(9):
        r = 34 + k * 17
        start = k * 55
        col = (255, 255, 255) if k % 2 == 0 else (120, 200, 235)
        draw.arc([cx - r, cy - r, cx + r, cy + r], start, start + 235,
                 fill=col, width=7)
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(210, 235, 245))
    draw.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(140, 190, 220))
    # coastline (Bay of Bengal shore) bottom-right
    draw.polygon([(x1, y1), (x1, y1 - 150), (x0 + 330, y1 - 60),
                  (x0 + 300, y1)], fill=(46, 125, 79))
    draw.polygon([(x1, y1), (x1, y1 - 150), (x0 + 330, y1 - 60),
                  (x0 + 300, y1)], outline=(120, 200, 140), width=3)
    # rain streaks
    for i in range(28):
        rx = x0 + 12 + (i * 37) % 470
        ry = y0 + 8 + (i * 53) % 250
        draw.line([(rx, ry), (rx - 7, ry + 16)], fill=(150, 205, 235),
                  width=2)


def scene_gaza(draw, box):
    x0, y0, x1, y1 = box
    gradient(draw, box, (59, 35, 80), (232, 134, 60))
    # stars
    for sx, sy in [(40, 24), (120, 48), (210, 20), (330, 40), (430, 26),
                   (80, 80), (280, 66), (470, 58)]:
        draw.ellipse([x0 + sx - 2, y0 + sy - 2, x0 + sx + 2, y0 + sy + 2],
                     fill=WHITE)
    horizon = y1 - 52
    # glow on the horizon
    draw.ellipse([x0 + 120, horizon - 60, x0 + 380, horizon + 30],
                 fill=(255, 150, 60))
    skyline(draw, x0, horizon, x1,
            [110, 150, 90, 170, 120, 80, 140, 100, 160, 70, 130, 95],
            (26, 16, 37), windows=True)
    draw.rectangle([x0, horizon, x1, y1], fill=(24, 14, 32))
    # smoke columns
    for cx, cy, r in [(x0 + 120, y0 + 120, 24), (x0 + 150, y0 + 92, 30),
                      (x0 + 330, y0 + 105, 26), (x0 + 360, y0 + 76, 30)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r * 0.75],
                     fill=(105, 100, 110))


# ---------------------------------------------------------------- page

def build():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # banner
    d.rectangle([0, 0, W, 104], fill=NAVY)
    f_big = fit_font(d, "THE WORLD IN ONE DAY", BOLD, 46, W - 40)
    centered(d, W // 2, 10, "THE WORLD IN ONE DAY", f_big, WHITE)
    f_date = fit_font(d, "18 NOVEMBER 2026", BOLD, 34, W - 40)
    centered(d, W // 2, 60, "18 NOVEMBER 2026", f_date, GOLD)
    d.rectangle([0, 104, W, 108], fill=GOLD)

    panels = [
        ((8, 108, 508, 500), scene_summit, GOLD, "SUMMIT",
         ["TRUMP, XI & PUTIN", "MEET IN SHENZHEN"],
         "First-ever trilateral at APEC"),
        ((516, 108, 1016, 500), scene_war, RED, "WAR",
         ["IRAN WAR: US BASE", "IN KUWAIT HIT"],
         "Drones strike Ali Al Salem base"),
        ((8, 508, 508, 900), scene_storm, CYAN, "STORM",
         ["CYCLONE AKVAN", "HEADS FOR INDIA"],
         "Storm to cross Andhra coast 20 Nov"),
        ((516, 508, 1016, 900), scene_gaza, ORANGE, "GAZA",
         ["ISRAEL OPENS NEW", "GAZA OPERATION"],
         "Operation in three central areas"),
    ]
    for box, scene, accent, tag, lines, sub in panels:
        x0, y0, x1, y1 = box
        scene(d, (x0, y0, x1, y1 - 108))
        caption_bar(d, (x0, y1 - 108, x1, y1), accent, lines, sub)
        chip(d, x0 + 12, y0 + 12, tag, accent)
        panel_frame(d, box)

    # bottom ticker
    d.rectangle([0, 900, W, H], fill=BLACK)
    d.rectangle([0, 900, W, 904], fill=RED)
    tick = ["QUAD MEETS IN MANILA",
            "GTA VI LAUNCHES AT MIDNIGHT",
            "US LOSES MEASLES-FREE STATUS"]
    f_tick = fit_font(d, max(tick, key=len), BOLD, 27, W - 90)
    yy = 914
    for line in tick:
        d.text((28, yy), "\u2022", font=f_tick, fill=RED)
        d.text((56, yy), line, font=f_tick, fill=WHITE)
        yy += 37

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
