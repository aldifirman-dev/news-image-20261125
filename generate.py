#!/usr/bin/env python3
"""Generate the 1024x1024 editorial world-news image for 25 November 2026."""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024
FONT_DIR = Path("/usr/share/fonts/truetype/noto")

# Palette
BG_DARK = (10, 15, 26)
HEADER_BG = (13, 20, 36)
MAP_LAND = (26, 42, 68)
MAP_BORDER = (52, 82, 128)
MAP_GRID = (16, 26, 44)
CARD_BG = (15, 23, 38, 224)
CARD_BORDER = (54, 76, 112)
TEXT_WHITE = (248, 250, 252)
TEXT_MUTED = (203, 213, 225)
TEXT_DIM = (148, 163, 184)
ACCENT_CRIMSON = (225, 29, 72)
ACCENT_AMBER = (245, 158, 11)
ACCENT_BLUE = (56, 189, 248)
ACCENT_EMERALD = (52, 211, 153)
ACCENT_ORANGE = (251, 146, 60)
ACCENT_RED = (248, 113, 113)


def load_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size)


def draw_world_map(canvas: Image.Image, top_y: int, bottom_y: int) -> None:
    """Draw a stylized dark world map across the background at 2x supersampling."""
    scale = 2
    mw, mh = WIDTH * scale, (bottom_y - top_y) * scale
    layer = Image.new("RGB", (mw, mh), BG_DARK)
    draw = ImageDraw.Draw(layer)

    # Latitude / longitude grid
    for gx in range(0, mw, 128 * scale):
        draw.line([(gx, 0), (gx, mh)], fill=MAP_GRID, width=2)
    for gy in range(0, mh, 110 * scale):
        draw.line([(0, gy), (mw, gy)], fill=MAP_GRID, width=2)

    def map_pt(lon: float, lat: float) -> tuple[float, float]:
        # Equirectangular projection mapped to background region
        x = (lon + 180.0) / 360.0 * mw
        y = (82.0 - lat) / 145.0 * mh
        return (x, y)

    # Simplified continent polygons (lon, lat)
    continents = [
        # North America
        [(-168, 66), (-140, 70), (-115, 70), (-95, 72), (-78, 63), (-62, 52),
         (-55, 47), (-67, 44), (-75, 36), (-81, 25), (-89, 21), (-84, 10),
         (-78, 8), (-85, 12), (-95, 16), (-105, 20), (-112, 28), (-123, 39),
         (-130, 54), (-150, 60), (-165, 62)],
        # Greenland
        [(-52, 60), (-42, 60), (-20, 72), (-25, 81), (-55, 78), (-58, 68)],
        # South America
        [(-78, 9), (-62, 11), (-50, 2), (-35, -6), (-39, -18), (-48, -28),
         (-58, -38), (-66, -50), (-69, -55), (-74, -46), (-72, -30), (-70, -18),
         (-81, -5), (-79, 2)],
        # Europe
        [(-9, 37), (0, 38), (5, 43), (12, 44), (16, 38), (23, 37), (28, 41),
         (30, 46), (40, 47), (52, 55), (60, 68), (35, 70), (20, 70), (5, 61),
         (-5, 58), (-10, 52), (-5, 48), (-9, 43)],
        # Africa
        [(-17, 15), (-6, 36), (10, 37), (25, 32), (33, 31), (43, 12), (51, 11),
         (41, -2), (40, -15), (33, -27), (20, -35), (15, -26), (12, -12),
         (9, 4), (-7, 5), (-16, 11)],
        # Asia
        [(28, 41), (42, 42), (55, 45), (60, 68), (95, 74), (135, 70), (170, 66),
         (160, 55), (142, 52), (130, 42), (122, 38), (121, 24), (109, 20),
         (104, 2), (98, 15), (90, 22), (80, 10), (77, 8), (68, 23), (57, 26),
         (48, 29), (44, 13), (35, 29), (35, 36)],
        # Australia
        [(114, -22), (130, -12), (142, -11), (153, -26), (149, -37), (138, -35),
         (125, -34), (115, -34)],
    ]

    for poly in continents:
        pts = [map_pt(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=MAP_LAND, outline=MAP_BORDER, width=3)

    # Highlight pins for the 6 news locations
    pins = [
        (26.0, 60.0, ACCENT_ORANGE),   # Gulf of Finland
        (-77.0, 38.9, ACCENT_BLUE),    # Washington DC
        (-74.0, 40.7, ACCENT_RED),     # New York
        (46.7, 24.7, ACCENT_AMBER),    # Riyadh
        (30.7, 36.9, ACCENT_EMERALD),  # Antalya
        (34.4, 31.5, ACCENT_CRIMSON),  # Gaza
    ]
    for lon, lat, color in pins:
        px, py = map_pt(lon, lat)
        draw.ellipse([px - 18, py - 18, px + 18, py + 18], outline=color, width=3)
        draw.ellipse([px - 7, py - 7, px + 7, py + 7], fill=color)

    down = layer.resize((WIDTH, bottom_y - top_y), Image.Resampling.LANCZOS)
    canvas.paste(down, (0, top_y))


def draw_panel_a_ship(w: int, h: int) -> Image.Image:
    """Burning cargo ship Sparta II and drones in Gulf of Finland."""
    s = 2
    img = Image.new("RGB", (w * s, h * s), (12, 22, 38))
    d = ImageDraw.Draw(img)
    W, H = w * s, h * s

    # Night sky glow from fire
    for r in range(220, 20, -25):
        c = (min(255, 22 + (220 - r) // 2), min(255, 28 + (220 - r) // 4), 44)
        d.ellipse([W * 0.50 - r * 1.4, H * 0.56 - r, W * 0.50 + r * 1.4, H * 0.56 + r], fill=c)

    # Sea & waves
    sea_y = int(H * 0.68)
    d.rectangle([0, sea_y, W, H], fill=(10, 38, 66))
    for wy in range(sea_y + 12, H, 20):
        pts = []
        for wx in range(0, W + 20, 24):
            pts.append((wx, wy + int(5 * math.sin(wx * 0.04 + wy))))
        d.line(pts, fill=(28, 82, 126), width=3)

    # Cargo ship hull (tilted slightly)
    hull = [(W * 0.18, sea_y - 10), (W * 0.78, sea_y - 6),
            (W * 0.85, sea_y - 44), (W * 0.22, sea_y - 38)]
    d.polygon(hull, fill=(55, 65, 81), outline=(148, 163, 184), width=3)
    # Red waterline stripe
    d.polygon([(W * 0.19, sea_y - 10), (W * 0.79, sea_y - 6),
               (W * 0.80, sea_y - 20), (W * 0.20, sea_y - 22)], fill=(165, 38, 42))

    # Bridge / superstructure at stern (left)
    d.rectangle([W * 0.24, sea_y - 96, W * 0.36, sea_y - 38], fill=(203, 213, 225), outline=(71, 85, 105), width=2)
    d.rectangle([W * 0.26, sea_y - 84, W * 0.34, sea_y - 72], fill=(30, 41, 59))
    # Mast / funnel
    d.rectangle([W * 0.28, sea_y - 120, W * 0.32, sea_y - 96], fill=(100, 116, 139))

    # Cargo containers on deck
    d.rectangle([W * 0.40, sea_y - 64, W * 0.52, sea_y - 40], fill=(37, 99, 235), outline=(147, 197, 253), width=2)
    d.rectangle([W * 0.54, sea_y - 64, W * 0.68, sea_y - 40], fill=(180, 83, 9), outline=(253, 186, 116), width=2)

    # Hull nameplate
    f_hull = load_font("NotoSans-Bold.ttf", 20)
    d.text((W * 0.36, sea_y - 29), "SPARTA II", font=f_hull, fill=(226, 232, 240), anchor="mm")

    # Smoke plumes rising from mid-ship
    smoke_blobs = [
        (0.55, 0.42, 46, (58, 64, 74)),
        (0.60, 0.30, 56, (50, 56, 66)),
        (0.67, 0.18, 66, (40, 45, 55)),
        (0.49, 0.46, 36, (75, 82, 92)),
    ]
    for sx, sy, sr, col in smoke_blobs:
        d.ellipse([W * sx - sr, H * sy - sr, W * sx + sr, H * sy + sr], fill=col)

    # Layered jagged flames
    d.polygon([
        (W * 0.45, sea_y - 40), (W * 0.48, sea_y - 98), (W * 0.51, sea_y - 74),
        (W * 0.54, sea_y - 134), (W * 0.58, sea_y - 84), (W * 0.62, sea_y - 142),
        (W * 0.65, sea_y - 92), (W * 0.69, sea_y - 40),
    ], fill=(234, 88, 12))
    d.polygon([
        (W * 0.48, sea_y - 40), (W * 0.52, sea_y - 102), (W * 0.55, sea_y - 68),
        (W * 0.59, sea_y - 114), (W * 0.62, sea_y - 72), (W * 0.66, sea_y - 40),
    ], fill=(250, 204, 21))
    # Fire reflection on water
    for ry, rw in [(sea_y + 18, 90), (sea_y + 38, 64), (sea_y + 58, 40)]:
        d.line([(W * 0.56 - rw, ry), (W * 0.56 + rw, ry)], fill=(234, 88, 12), width=4)

    # Approaching drones (top-left & top-right)
    for dx, dy in [(W * 0.14, H * 0.24), (W * 0.84, H * 0.28)]:
        d.line([(dx - 26, dy), (dx + 26, dy)], fill=(226, 232, 240), width=5)
        d.polygon([(dx - 10, dy - 6), (dx + 10, dy - 6), (dx + 6, dy + 8), (dx - 6, dy + 8)], fill=(239, 68, 68))
        d.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=(254, 240, 138))

    # Dashed attack arc
    for t in range(6):
        px = W * (0.18 + t * 0.05)
        py = H * (0.28 + t * 0.04)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(248, 113, 113))

    return img.resize((w, h), Image.Resampling.LANCZOS)


def draw_panel_b_cia_hack(w: int, h: int) -> Image.Image:
    """CIA seal + server room breach."""
    s = 2
    img = Image.new("RGB", (w * s, h * s), (10, 20, 34))
    d = ImageDraw.Draw(img)
    W, H = w * s, h * s

    # Cyber grid lines
    for gx in range(0, W, 40):
        d.line([(gx, 0), (gx, H)], fill=(16, 36, 56), width=2)
    for gy in range(0, H, 40):
        d.line([(0, gy), (W, gy)], fill=(16, 36, 56), width=2)

    # Server racks on right half
    rack_xs = [W * 0.56, W * 0.72, W * 0.86]
    for idx, rx in enumerate(rack_xs):
        rw = W * 0.12
        d.rectangle([rx, H * 0.12, rx + rw, H * 0.90], fill=(24, 34, 52), outline=(71, 85, 105), width=3)
        for slot_y in range(int(H * 0.18), int(H * 0.86), 24):
            d.rectangle([rx + 8, slot_y, rx + rw - 8, slot_y + 12], fill=(15, 23, 42))
            led_col = (239, 68, 68) if (idx + slot_y // 24) % 3 == 0 else (34, 211, 238)
            d.ellipse([rx + 14, slot_y + 3, rx + 22, slot_y + 11], fill=led_col)

    # CIA Seal emblem on left
    cx, cy = int(W * 0.25), int(H * 0.50)
    r_outer = int(H * 0.36)
    d.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], fill=(18, 42, 78), outline=(212, 175, 55), width=6)
    r_mid = int(r_outer * 0.82)
    d.ellipse([cx - r_mid, cy - r_mid, cx + r_mid, cy + r_mid], fill=(15, 32, 60), outline=(212, 175, 55), width=3)

    # Compass rose / star inside seal
    star_pts = []
    for i in range(16):
        ang = i * math.pi / 8 - math.pi / 2
        rad = r_mid * 0.72 if i % 2 == 0 else r_mid * 0.26
        star_pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(star_pts, fill=(212, 175, 55), outline=(254, 240, 138), width=2)
    # Central shield (wider so CIA fits cleanly with margin)
    d.polygon([
        (cx - 38, cy - 26), (cx + 38, cy - 26),
        (cx + 34, cy + 10), (cx, cy + 38), (cx - 34, cy + 10)
    ], fill=(15, 23, 42), outline=(248, 250, 252), width=3)

    # Breach lightning / data lines from seal to servers
    d.line([(cx + r_outer - 10, cy), (W * 0.44, cy - 28), (W * 0.49, cy + 16), (W * 0.56, cy - 10)],
           fill=(239, 68, 68), width=7)

    # Warning alert triangle
    tx, ty = int(W * 0.45), int(H * 0.24)
    d.polygon([(tx, ty - 28), (tx - 28, ty + 22), (tx + 28, ty + 22)], fill=(220, 38, 38), outline=(254, 226, 226), width=3)
    d.rectangle([tx - 3, ty - 12, tx + 3, ty + 6], fill=(255, 255, 255))
    d.ellipse([tx - 4, ty + 10, tx + 4, ty + 18], fill=(255, 255, 255))

    font_cia = load_font("NotoSans-Bold.ttf", 30)
    d.text((cx, cy - 1), "CIA", font=font_cia, fill=(255, 255, 255), anchor="mm")

    return img.resize((w, h), Image.Resampling.LANCZOS)


def draw_panel_c_gavel(w: int, h: int) -> Image.Image:
    """Courtroom gavel + Huawei guilty 10 of 12."""
    s = 2
    img = Image.new("RGB", (w * s, h * s), (28, 20, 18))
    d = ImageDraw.Draw(img)
    W, H = w * s, h * s

    # Courtroom columns background
    for px in range(int(W * 0.08), W, int(W * 0.16)):
        d.rectangle([px, 0, px + 36, H], fill=(42, 30, 26))

    # Warm spotlight behind gavel
    d.ellipse([W * 0.10, H * 0.05, W * 0.62, H * 0.92], fill=(56, 36, 26))

    # Sound block at bottom-left
    bx, by = int(W * 0.30), int(H * 0.78)
    d.ellipse([bx - 88, by - 18, bx + 88, by + 26], fill=(120, 53, 15), outline=(217, 119, 6), width=4)
    d.ellipse([bx - 76, by - 24, bx + 76, by + 12], fill=(146, 64, 14), outline=(245, 158, 11), width=3)

    # Gavel handle (centered on gavel head)
    d.line([(W * 0.33, H * 0.40), (W * 0.55, H * 0.78)], fill=(180, 83, 9), width=22)
    d.line([(W * 0.33, H * 0.40), (W * 0.55, H * 0.78)], fill=(217, 119, 6), width=10)

    # Gavel head
    head_pts = [(W * 0.20, H * 0.42), (W * 0.37, H * 0.28), (W * 0.45, H * 0.38), (W * 0.28, H * 0.52)]
    d.polygon(head_pts, fill=(146, 64, 14), outline=(245, 158, 11), width=4)
    # Gold bands on gavel head
    d.line([(W * 0.22, H * 0.41), (W * 0.29, H * 0.50)], fill=(251, 191, 36), width=8)
    d.line([(W * 0.35, H * 0.30), (W * 0.43, H * 0.39)], fill=(251, 191, 36), width=8)

    # Impact lines above sound block
    for dx, dy in [(-55, -35), (0, -45), (55, -35)]:
        d.line([(bx + dx * 0.7, by - 36), (bx + dx, by - 36 + dy * 0.4)], fill=(253, 224, 71), width=5)

    # Verdict stamp box on right
    rx1, ry1, rx2, ry2 = int(W * 0.56), int(H * 0.16), int(W * 0.94), int(H * 0.82)
    d.rounded_rectangle([rx1, ry1, rx2, ry2], radius=16, fill=(40, 14, 18), outline=(239, 68, 68), width=6)
    f_lbl = load_font("NotoSans-Bold.ttf", 24)
    f_big = load_font("NotoSans-Bold.ttf", 54)
    f_sub = load_font("NotoSans-CondensedBold.ttf", 38)
    d.text(((rx1 + rx2) // 2, ry1 + 36), "HUAWEI VERDICT", font=f_lbl, fill=(252, 165, 165), anchor="mm")
    d.text(((rx1 + rx2) // 2, ry1 + 92), "GUILTY", font=f_big, fill=(248, 113, 113), anchor="mm")
    d.text(((rx1 + rx2) // 2, ry1 + 150), "10 / 12 COUNTS", font=f_sub, fill=(254, 240, 138), anchor="mm")

    return img.resize((w, h), Image.Resampling.LANCZOS)


def draw_panel_d_riyadh(w: int, h: int) -> Image.Image:
    """Riyadh KAFD skyline with PIF tower smoking halfway up."""
    s = 2
    img = Image.new("RGB", (w * s, h * s), (26, 20, 34))
    d = ImageDraw.Draw(img)
    W, H = w * s, h * s

    # Dusk desert sky gradient bands
    for band in range(6):
        y0 = int(H * band / 6)
        y1 = int(H * (band + 1) / 6) + 2
        col = (24 + band * 10, 18 + band * 6, 38 + band * 3)
        d.rectangle([0, y0, W, y1], fill=col)

    # Flanking KAFD towers
    skyline = [
        (0.06, 0.52, 0.14, (30, 41, 59)),
        (0.16, 0.40, 0.24, (38, 52, 74)),
        (0.26, 0.58, 0.34, (30, 41, 59)),
        (0.64, 0.44, 0.73, (36, 50, 72)),
        (0.75, 0.52, 0.84, (28, 39, 58)),
        (0.86, 0.60, 0.94, (24, 34, 52)),
    ]
    for x1, top, x2, col in skyline:
        d.rectangle([W * x1, H * top, W * x2, H], fill=col, outline=(71, 85, 105), width=2)
        for wy in range(int(H * top) + 16, H - 10, 22):
            for wx in range(int(W * x1) + 12, int(W * x2) - 10, 18):
                if (wx + wy) % 2 == 0:
                    d.rectangle([wx, wy, wx + 6, wy + 10], fill=(148, 163, 184))

    # Iconic faceted PIF Tower in center
    pif = [
        (W * 0.44, H), (W * 0.45, H * 0.28), (W * 0.49, H * 0.08),
        (W * 0.53, H * 0.22), (W * 0.55, H),
    ]
    d.polygon(pif, fill=(71, 95, 128), outline=(148, 184, 218), width=3)
    # Faceted glass diagonal lines
    d.line([(W * 0.49, H * 0.08), (W * 0.49, H)], fill=(186, 230, 253), width=3)
    for wy in range(int(H * 0.26), H, 28):
        d.line([(W * 0.45, wy), (W * 0.54, wy - 10)], fill=(100, 130, 168), width=2)

    # Drone strike burst halfway up PIF tower
    hit_x, hit_y = int(W * 0.51), int(H * 0.52)
    # Smoke billowing rightward
    for sx, sy, sr, col in [
        (hit_x + 28, hit_y - 16, 36, (75, 80, 90)),
        (hit_x + 74, hit_y - 42, 48, (60, 65, 76)),
        (hit_x + 128, hit_y - 68, 56, (48, 53, 64)),
    ]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=col)

    # Explosion flash
    d.ellipse([hit_x - 32, hit_y - 32, hit_x + 32, hit_y + 32], fill=(239, 68, 68))
    d.ellipse([hit_x - 20, hit_y - 20, hit_x + 20, hit_y + 20], fill=(251, 146, 60))
    d.ellipse([hit_x - 9, hit_y - 9, hit_x + 9, hit_y + 9], fill=(254, 240, 138))

    # Drone silhouette approaching from left
    dx, dy = int(W * 0.30), int(H * 0.42)
    d.line([(dx - 22, dy), (dx + 22, dy)], fill=(248, 250, 252), width=5)
    d.polygon([(dx - 8, dy - 6), (dx + 8, dy - 6), (dx + 4, dy + 8), (dx - 4, dy + 8)], fill=(239, 68, 68))
    d.line([(dx + 28, dy + 6), (hit_x - 36, hit_y - 6)], fill=(248, 113, 113), width=3)

    return img.resize((w, h), Image.Resampling.LANCZOS)


def draw_panel_e_cop31(w: int, h: int) -> Image.Image:
    """COP31 summit hall with empty chairs."""
    s = 2
    img = Image.new("RGB", (w * s, h * s), (14, 24, 38))
    d = ImageDraw.Draw(img)
    W, H = w * s, h * s

    # Summit hall floor & backdrop
    d.rectangle([0, 0, W, int(H * 0.56)], fill=(18, 38, 68))
    d.rectangle([0, int(H * 0.56), W, H], fill=(24, 32, 48))

    # UN-blue stage backdrop with COP31 label
    d.rounded_rectangle([W * 0.24, H * 0.07, W * 0.76, H * 0.47], radius=12,
                        fill=(23, 62, 118), outline=(96, 165, 250), width=4)
    f_cop = load_font("NotoSans-Bold.ttf", 50)
    d.text((W * 0.50, H * 0.22), "COP31", font=f_cop, fill=(248, 250, 252), anchor="mm")
    f_loc = load_font("NotoSans-SemiBold.ttf", 24)
    d.text((W * 0.50, H * 0.36), "ANTALYA • NO DEAL", font=f_loc, fill=(254, 202, 202), anchor="mm")

    # Empty podium below backdrop (no overlap)
    d.rectangle([W * 0.45, H * 0.49, W * 0.55, H * 0.62], fill=(51, 65, 85), outline=(148, 163, 184), width=3)

    # Rows of empty chairs (tiered arcs)
    for row_idx, ry in enumerate([H * 0.72, H * 0.86]):
        count = 7 + row_idx * 2
        for i in range(count):
            cx = W * (0.12 + 0.76 * (i / (count - 1)))
            cw, ch = 36, 34
            # Chair backrest & seat (empty)
            d.rounded_rectangle([cx - cw // 2, ry - ch, cx + cw // 2, ry], radius=6,
                                fill=(30, 58, 95), outline=(100, 116, 139), width=3)
            d.rectangle([cx - cw // 2 - 4, ry - 6, cx + cw // 2 + 4, ry + 6],
                        fill=(51, 65, 85), outline=(148, 163, 184), width=2)

    # Diagonal red 'X' / walkout cross across right corner or subtle red stamp
    d.line([(W * 0.80, H * 0.14), (W * 0.90, H * 0.34)], fill=(239, 68, 68), width=10)
    d.line([(W * 0.90, H * 0.14), (W * 0.80, H * 0.34)], fill=(239, 68, 68), width=10)

    return img.resize((w, h), Image.Resampling.LANCZOS)


def draw_panel_f_gaza(w: int, h: int) -> Image.Image:
    """Gaza City skyline with smoke column."""
    s = 2
    img = Image.new("RGB", (w * s, h * s), (22, 16, 22))
    d = ImageDraw.Draw(img)
    W, H = w * s, h * s

    # Twilight red/amber sky glow
    for band in range(6):
        y0 = int(H * band / 6)
        y1 = int(H * (band + 1) / 6) + 2
        col = (26 + band * 12, 16 + band * 5, 24 + band * 2)
        d.rectangle([0, y0, W, y1], fill=col)

    # Smoke plume rising from center-left building
    smoke = [
        (0.42, 0.56, 36, (82, 76, 80)),
        (0.45, 0.42, 52, (64, 62, 68)),
        (0.50, 0.28, 66, (52, 52, 58)),
        (0.56, 0.12, 78, (40, 42, 48)),
    ]
    for sx, sy, sr, col in smoke:
        d.ellipse([W * sx - sr, H * sy - sr, W * sx + sr, H * sy + sr], fill=col)

    # Strike fireball & blast shards behind damaged center-left building
    bx, by = int(W * 0.41), int(H * 0.60)
    d.polygon([
        (bx - 64, by + 18), (bx - 42, by - 40), (bx - 16, by - 16),
        (bx, by - 62), (bx + 22, by - 20), (bx + 54, by - 44),
        (bx + 62, by + 18)
    ], fill=(239, 68, 68))
    d.polygon([
        (bx - 36, by + 14), (bx - 22, by - 22), (bx, by - 38),
        (bx + 20, by - 14), (bx + 36, by + 14)
    ], fill=(251, 191, 36))

    # Damaged target building silhouette in foreground of blast
    d.polygon([
        (W * 0.36, H), (W * 0.36, H * 0.66), (W * 0.40, H * 0.72),
        (W * 0.43, H * 0.63), (W * 0.46, H * 0.70), (W * 0.46, H)
    ], fill=(18, 18, 24), outline=(82, 82, 96), width=2)

    # Gaza City flat-roofed skyline silhouettes
    buildings = [
        (0.02, 0.58, 0.13), (0.14, 0.50, 0.25), (0.26, 0.64, 0.36),
        (0.47, 0.54, 0.58), (0.60, 0.46, 0.71), (0.73, 0.60, 0.84),
        (0.86, 0.52, 0.98),
    ]
    for x1, top, x2 in buildings:
        d.rectangle([W * x1, H * top, W * x2, H], fill=(24, 24, 32), outline=(64, 64, 78), width=2)
        # Lit windows in some buildings
        for wy in range(int(H * top) + 18, int(H * 0.92), 26):
            for wx in range(int(W * x1) + 12, int(W * x2) - 14, 22):
                if (wx + wy) % 3 == 0:
                    d.rectangle([wx, wy, wx + 8, wy + 10], fill=(251, 191, 36))

    # Dome & minaret silhouette on right
    mx = int(W * 0.78)
    d.rectangle([mx - 8, H * 0.34, mx + 8, H * 0.60], fill=(24, 24, 32))
    d.polygon([(mx - 10, H * 0.34), (mx, H * 0.24), (mx + 10, H * 0.34)], fill=(24, 24, 32))
    d.chord([W * 0.62, H * 0.38, W * 0.74, H * 0.54], start=180, end=360, fill=(24, 24, 32))

    return img.resize((w, h), Image.Resampling.LANCZOS)


def fit_font(draw: ImageDraw.ImageDraw, text: str, font_name: str, max_width: int, start_size: int, min_size: int = 18) -> ImageFont.FreeTypeFont:
    for size in range(start_size, min_size - 1, -1):
        font = load_font(font_name, size)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width:
            return font
    return load_font(font_name, min_size)


def render() -> Path:
    img = Image.new("RGBA", (WIDTH, HEIGHT), BG_DARK + (255,))
    map_bg = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw_world_map(map_bg, top_y=108, bottom_y=HEIGHT)
    img.paste(map_bg, (0, 0))
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)

    # Masthead
    odraw.rectangle([0, 0, WIDTH, 108], fill=HEADER_BG + (255,))
    odraw.rectangle([0, 0, WIDTH, 6], fill=ACCENT_CRIMSON + (255,))
    odraw.line([(24, 105), (WIDTH - 24, 105)], fill=ACCENT_AMBER + (255,), width=3)

    f_mast = fit_font(odraw, "25 NOVEMBER 2026 — THE WORLD IN ONE DAY", "NotoSans-CondensedBold.ttf", WIDTH - 48, 44)
    odraw.text((WIDTH // 2, 40), "25 NOVEMBER 2026 — THE WORLD IN ONE DAY", font=f_mast, fill=TEXT_WHITE + (255,), anchor="mm")

    f_sub = load_font("NotoSans-SemiBold.ttf", 20)
    odraw.text((WIDTH // 2, 80), "WEDNESDAY GLOBAL BRIEFING  •  SIX MAJOR STORIES", font=f_sub, fill=ACCENT_AMBER + (255,), anchor="mm")

    # 2x3 Grid of Vignettes
    cards = [
        ("GULF OF FINLAND", "SPARTA II — UKRAINE: WE DID IT", "Russian cargo ship hit by drones", ACCENT_ORANGE, draw_panel_a_ship),
        ("WASHINGTON • CYBER", "CIA HACKED — UNCLASSIFIED DATA", "OSINT system breached; ODNI hit", ACCENT_BLUE, draw_panel_b_cia_hack),
        ("BROOKLYN • COURT", "HUAWEI: GUILTY 10 OF 12", "US jury convicts on fraud & sanctions", ACCENT_RED, draw_panel_c_gavel),
        ("RIYADH • KAFD", "RIYADH HIT AGAIN — 11 HURT", "Drone hits PIF tower; 2nd strike in week", ACCENT_AMBER, draw_panel_d_riyadh),
        ("ANTALYA • CLIMATE", "COP31: NO DEAL", "Summit ends without deal; EU walks out", ACCENT_EMERALD, draw_panel_e_cop31),
        ("GAZA CITY", "HAMAS SECURITY CHIEF KILLED", "Israeli strike kills Naeem Abu Nahel", ACCENT_CRIMSON, draw_panel_f_gaza),
    ]

    margin_x = 22
    gutter_x = 24
    card_w = (WIDTH - 2 * margin_x - gutter_x) // 2  # 478
    top_start = 122
    gap_y = 16
    card_h = (HEIGHT - top_start - 20 - 2 * gap_y) // 3  # 283

    f_tag = load_font("NotoSans-Bold.ttf", 16)

    for idx, (tag, headline, subline, accent, painter) in enumerate(cards):
        col = idx % 2
        row = idx // 2
        x1 = margin_x + col * (card_w + gutter_x)
        y1 = top_start + row * (card_h + gap_y)
        x2 = x1 + card_w
        y2 = y1 + card_h

        # Translucent card frame over dark world map
        odraw.rounded_rectangle([x1, y1, x2, y2], radius=12, fill=CARD_BG, outline=CARD_BORDER + (255,), width=2)

        # Illustration window at top of card
        ill_pad = 8
        ill_w = card_w - 2 * ill_pad
        ill_h = 158
        panel = painter(ill_w, ill_h).convert("RGBA")
        overlay.paste(panel, (x1 + ill_pad, y1 + ill_pad))
        odraw.rectangle([x1 + ill_pad, y1 + ill_pad, x1 + ill_pad + ill_w, y1 + ill_pad + ill_h],
                        outline=(51, 65, 85, 255), width=2)

        # Accent bar & location tag
        text_x = x1 + 14
        tag_y = y1 + ill_pad + ill_h + 10
        odraw.rectangle([text_x, tag_y + 2, text_x + 6, tag_y + 20], fill=accent + (255,))
        odraw.text((text_x + 14, tag_y), tag, font=f_tag, fill=accent + (255,))

        # Headline
        head_y = tag_y + 26
        f_head = fit_font(odraw, headline, "NotoSans-CondensedBold.ttf", card_w - 28, 30, min_size=22)
        odraw.text((text_x, head_y), headline, font=f_head, fill=TEXT_WHITE + (255,))

        # Sub-fact line
        fact_y = head_y + 38
        f_subline = fit_font(odraw, subline, "NotoSans-Medium.ttf", card_w - 28, 19, min_size=15)
        odraw.text((text_x, fact_y), subline, font=f_subline, fill=TEXT_MUTED + (255,))

    final_img = Image.alpha_composite(img, overlay).convert("RGB")
    out_path = Path(__file__).resolve().parent / "entry.png"
    final_img.save(out_path, format="PNG", optimize=True)
    return out_path


if __name__ == "__main__":
    p = render()
    print(f"Wrote {p} ({p.stat().st_size} bytes)")
