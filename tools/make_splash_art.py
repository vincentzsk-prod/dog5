#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 ZIGGY, DØGS (DØG-5)
"""Generate the art tables of DØG-5's boot animation and of the panel header's wordmark.

  tools/make_splash_art.py [FAVICON_240.png] [YatraOne font]
      defaults: assets/brand/dog5-favicon-240.png, web/brand/YatraOne-Regular.woff2
  -> firmware/gen/dog5_splash_art.h   the boot animation (firmware/src/dog5_splash.h draws it)
  -> firmware/gen/dog5_ui_art.h    the small pixel wordmark in the panel pages' header (obv_ui.h)

The boot animation is Vincent's launch screen as approved (the claude.ai artifact "DØG-5 launch screen", 19 Nov 2026,
its last version: speed 95 ms a step, smooth, grain 62, halo 53, seal 78), drawn for the 240 x 240 panel. That page was
tuned at 400 x 400 = the panel x 5/3: every size here is the page's x 3/5.

  SPL_FAV     the favicon's brightness as coverage, 4 bits a pixel (its white areas take the colour cycle)
  SPL_WORD    "DØG-5" in Yatra One at 55 px (the page's 92 px), coverage, 4 bits a pixel, centred on the screen
  SPL_RAMP    the 16-colour cycle (the page's ramp), 8-bit RGB
  SPL_HALO    the colour-bleed halo's weight by distance from the centre (index: d*d >> 6), 0..256
  SPL_SEAL    the zig-zag seal's spike heights, one per vertex around the edge, 0..256 (the page's 0.28 + 0.72 hash)
  UI_WORD     the pixel wordmark, as the update screen's (tools/make_ldr_art.py) but at 18 px with a 2 px shadow:
              2 bits a pixel, 0 background or outline, 2 Sun Yellow, 3 Acid Chartreuse

Rows are MSB first (the high nibble is the left pixel). Needs Pillow, NumPy and SciPy (host only)."""
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import binary_dilation

ROOT = Path(__file__).resolve().parent.parent
RAMP = ["#EF6BFF", "#FF6BCE", "#FF8473", "#E69C21", "#BDBD00", "#8CD600", "#5AE631", "#008C31",
        "#1963D6", "#4242FF", "#7329FF", "#9C19CE", "#B5217B", "#B53121", "#9C4A00", "#C573FF"]
WORD_PX = 55                    # the page's 92 px x 3/5
HALO_R = 0.72 * 240             # the page: rad = S * 0.72
SEAL_PAD, SEAL_STEP = 11, 9     # the page's 18 and 15 px x 3/5 (its spike height, 11 -> 6.6, is in dog5_splash.h)
UI_PX, UI_SHADOW = 18, 2


def js_hash(x):
    """the page's hash(): fract(sin(x * 12.9898) * 43758.5453)"""
    s = math.sin(x * 12.9898) * 43758.5453
    return s - math.floor(s)


def fav(path):
    im = Image.open(path).convert("RGBA")
    flat = Image.alpha_composite(Image.new("RGBA", im.size, (0, 0, 0, 255)), im).convert("L")
    if flat.size != (240, 240):
        raise SystemExit(f"{path}: the favicon must be 240 x 240 (it is {flat.size})")
    return (np.asarray(flat).astype(np.int32) * 15 + 127) // 255


def word(font):
    f = ImageFont.truetype(str(font), WORD_PX)
    l, t, r, b = f.getbbox("DØG-5")
    m = Image.new("L", (r - l + 2, b - t + 2), 0)
    ImageDraw.Draw(m).text((1 - l, 1 - t), "DØG-5", font=f, fill=255)
    a = np.asarray(m).astype(np.int32)
    ys, xs = np.nonzero(a)
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return (a * 15 + 127) // 255


def ui_word(font):
    f = ImageFont.truetype(str(font), UI_PX)
    l, t, r, b = f.getbbox("DØG-5")
    m = Image.new("L", (r - l + 4, b - t + 4), 0)
    ImageDraw.Draw(m).text((2 - l, 2 - t), "DØG-5", font=f, fill=255)
    m = np.pad(np.asarray(m) > 140, UI_SHADOW + 2)
    h, w = m.shape
    out = np.zeros((h, w), np.uint8)
    sh = np.zeros_like(m)
    sh[UI_SHADOW:, UI_SHADOW:] = m[:h - UI_SHADOW, :w - UI_SHADOW]
    out[sh] = 3
    out[binary_dilation(m, np.ones((3, 3)))] = 0
    out[m] = 2
    ys, xs = np.nonzero(out)
    return out[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def pack(img, bpp):
    per = 8 // bpp
    data = []
    for row in img:
        for b in range((len(row) + per - 1) // per):
            v = 0
            for k in range(per):
                x = b * per + k
                if x < len(row):
                    v |= int(row[x]) << (8 - bpp - k * bpp)
            data.append(v)
    return data


def carray(ctype, name, data, per_line=24, fmt="0x{:02X}"):
    lines = [f"static const {ctype} {name}[{len(data)}] = {{"]
    for i in range(0, len(data), per_line):
        lines.append("    " + ", ".join(fmt.format(v) for v in data[i:i + per_line]) + ",")
    return "\n".join(lines + ["};", ""])


def seal_vertices():
    """the vertex count around the edge, as the page's sealPts walks it (four sides, corners shared)"""
    a, bb, n = SEAL_PAD, 240 - SEAL_PAD, 0
    for _ in range(4):
        n += len(range(a + SEAL_STEP, bb, SEAL_STEP))
    return n


def main(argv):
    favp = Path(argv[0]) if argv else ROOT / "assets/brand/dog5-favicon-240.png"
    font = Path(argv[1]) if len(argv) > 1 else ROOT / "web/brand/YatraOne-Regular.woff2"
    fv, wd, uw = fav(favp), word(font), ui_word(font)
    halo = []
    for i in range((2 * 120 * 120 >> 6) + 1):           # the page: stops 0 (a), 0.42 (a * 0.45), 1 (0), linear
        d = math.sqrt(i * 64) / HALO_R
        w = 1 - d / 0.42 * 0.55 if d < 0.42 else (0.45 * (1 - (d - 0.42) / 0.58) if d < 1 else 0)
        halo.append(round(256 * w))
    nv = seal_vertices()
    seal = [round(256 * (0.28 + 0.72 * js_hash((g + 1) * 1.37))) for g in range(nv)]
    ramp = [int(c[k:k + 2], 16) for c in RAMP for k in (1, 3, 5)]
    wx, wy = (240 - wd.shape[1]) // 2, (240 - wd.shape[0]) // 2
    gen = ROOT / "firmware/gen"
    hdr = ("/* SPDX-License-Identifier: GPL-3.0-only\n * Copyright (C) 2026 ZIGGY, DØGS (DØG-5) */\n"
           "/* Generated by tools/make_splash_art.py. Do not edit by hand. Yatra One (SIL OFL 1.1) drawn as bitmaps. */\n")
    (gen / "dog5_splash_art.h").write_text(
        hdr + "/* The boot animation's art (firmware/src/dog5_splash.h draws it): see the generator's notes. Coverage is\n"
        " * 0..15, 4 bits a pixel, the left pixel in the high nibble. */\n"
        f"#define SPL_WORD_W {wd.shape[1]}\n#define SPL_WORD_H {wd.shape[0]}\n#define SPL_WORD_X {wx}\n#define SPL_WORD_Y {wy}\n"
        f"#define SPL_SEAL_N {nv}\n#define SPL_SEAL_PAD {SEAL_PAD}\n#define SPL_SEAL_STEP {SEAL_STEP}\n"
        f"#define SPL_HALO_N {len(halo)}\n"
        + carray("uint8_t", "SPL_FAV", pack(fv, 4)) + carray("uint8_t", "SPL_WORD", pack(wd, 4))
        + carray("uint8_t", "SPL_RAMP", ramp, 12) + carray("uint16_t", "SPL_HALO", halo, 16, "{}")
        + carray("uint16_t", "SPL_SEAL", seal, 16, "{}"))
    (gen / "dog5_ui_art.h").write_text(
        hdr + "/* The panel header's wordmark: 2 bits a pixel (0 background or the black outline, 2 Sun Yellow, 3 Acid\n"
        " * Chartreuse, the shadow), rows MSB first. */\n"
        f"#define UI_WORD_W {uw.shape[1]}\n#define UI_WORD_H {uw.shape[0]}\n" + carray("uint8_t", "UI_WORD", pack(uw, 2)))
    print(f"dog5_splash_art.h: favicon {len(pack(fv, 4))} B, word {wd.shape[1]}x{wd.shape[0]} at {wx},{wy}, {nv} seal vertices;"
          f" dog5_ui_art.h: word {uw.shape[1]}x{uw.shape[0]}")


if __name__ == "__main__":
    main(sys.argv[1:])
