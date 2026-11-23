#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 ZIGGY, DØGS (DØG-5)
"""Generate firmware/gen/dog5_screen_art.h: the four scenes and the dog, from assets/screen/.

  assets/screen/field-*.png   the four fields, 240 x 200 (screen rows 20..219), at most 256 colours each
  assets/screen/dog-*.png     the dog's poses, RGBA, every pixel fully opaque or fully clear, at most 255 colours each
  assets/screen/layout.json   per scene: its field, and per pose the sprite, its top-left on the screen and the point
                              where the beam leaves the mouth (in sprite pixels)

Everything is stored as 8-bit indices into an RGB565 palette (stored byte-swapped, as the panel takes it), in flash.
Sprite index 0 is clear. Per scene the generator also works out the rectangle where REST and BARK differ (the head),
so a note repaints only that. Needs Pillow (host only). Run: tools/make_screen_art.py [OUT.h]
"""
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "assets" / "screen"
POSES = ["1-REST", "2-BARK", "3-HOWL-INHALE", "4-HOWL"]
FIELD_Y, FIELD_H = 20, 200


def rgb565_swapped(r, g, b):
    c = (r >> 3) << 11 | (g >> 2) << 5 | b >> 3
    return (c >> 8 | c << 8) & 0xFFFF


def carray(ctype, name, data, per):
    lines = [f"static const {ctype} {name}[{len(data)}] = {{"]
    fmt = "0x{:04X}" if ctype == "uint16_t" else "{}"
    for i in range(0, len(data), per):
        lines.append("    " + ",".join(fmt.format(v) for v in data[i:i + per]) + ",")
    return "\n".join(lines + ["};", ""])


def field(path):
    im = Image.open(path).convert("RGB")
    assert im.size == (240, FIELD_H), f"{path.name}: {im.size}, want 240 x {FIELD_H}"
    px = list(zip(*[iter(im.tobytes())] * len(im.getbands())))
    pal = sorted(set(px))
    assert len(pal) <= 256, f"{path.name}: {len(pal)} colours, at most 256"
    ix = {c: i for i, c in enumerate(pal)}
    return [rgb565_swapped(*c) for c in pal], [ix[c] for c in px]


def sprite(path):
    im = Image.open(path).convert("RGBA")
    px = list(zip(*[iter(im.tobytes())] * len(im.getbands())))
    assert all(a in (0, 255) for *_, a in px), f"{path.name}: half-clear pixels"
    pal = sorted({(r, g, b) for r, g, b, a in px if a})
    assert len(pal) <= 255, f"{path.name}: {len(pal)} colours, at most 255"
    ix = {c: i + 1 for i, c in enumerate(pal)}
    return im.size, [rgb565_swapped(*c) for c in pal], [ix[(r, g, b)] if a else 0 for r, g, b, a in px], im


def main(argv):
    out = Path(argv[0]) if argv else ROOT / "firmware" / "gen" / "dog5_screen_art.h"
    lay = json.loads((ART / "layout.json").read_text())
    parts, total, sprites = [], 0, {}
    for k, sc in enumerate(lay["scenes"].values()):
        pal, px = field(ART / sc["field"])
        parts += [carray("uint16_t", f"SA_FPAL{k}", pal, 12), carray("uint8_t", f"SA_FIELD{k}", px, 40)]
        total += 2 * len(pal) + len(px)
    structs = []
    for k, (sid, sc) in enumerate(lay["scenes"].items()):
        ptrs, canv = [], {}
        for p in POSES:
            if p not in sc["poses"]:
                ptrs.append("0")
                continue
            d = sc["poses"][p]
            if d["sprite"] not in sprites:
                (w, h), pal, px, im = sprite(ART / d["sprite"])
                n = len(sprites)
                parts += [carray("uint16_t", f"SA_SPAL{n}", pal, 12), carray("uint8_t", f"SA_SPX{n}", px, 40)]
                total += 2 * len(pal) + len(px)
                sprites[d["sprite"]] = (n, w, h, im)
            n, w, h, im = sprites[d["sprite"]]
            assert (w, h) == (d["w"], d["h"]), f"{d['sprite']}: layout says {d['w']} x {d['h']}"
            bx, by = d["beam"] if d["beam"] else (-1, -1)
            structs.append(f"static const sa_sprite_t SA_S{k}_{p[0]} = {{{d['x']}, {d['y']}, {w}, {h}, {bx}, {by}, SA_SPAL{n}, SA_SPX{n}}};")
            ptrs.append(f"&SA_S{k}_{p[0]}")
            c = Image.new("RGBA", (240, 240))
            c.paste(im, (d["x"], d["y"]), im)
            canv[p] = c
        # the head: where REST and BARK differ, on the screen (x0, y0, x1, y1; x1/y1 exclusive), 1 px of margin
        a, b = canv["1-REST"].tobytes(), canv["2-BARK"].tobytes()
        xs, ys = [], []
        for i in range(0, len(a), 4):
            if a[i:i + 4] != b[i:i + 4]:
                xs.append(i // 4 % 240)
                ys.append(i // 4 // 240)
        head = (max(min(xs) - 1, 0), max(min(ys) - 1, FIELD_Y), min(max(xs) + 2, 240), min(max(ys) + 2, FIELD_Y + FIELD_H))
        structs.append(f"/* {sid}: {sc['field']} */")
        structs.append(f"#define SA_HEAD{k} {{{head[0]}, {head[1]}, {head[2]}, {head[3]}}}")
        structs.append(f"static const sa_sprite_t *const SA_POSES{k}[4] = {{{', '.join(ptrs)}}};")
    scenes = ",\n    ".join(f"{{SA_FPAL{k}, SA_FIELD{k}, SA_POSES{k}, SA_HEAD{k}}}" for k in range(len(lay["scenes"])))
    text = (
        "/* SPDX-License-Identifier: GPL-3.0-only\n * Copyright (C) 2026 ZIGGY, DØGS (DØG-5: the four scenes and the dog, hand-painted) */\n"
        "/* Generated by tools/make_screen_art.py from assets/screen/. Do not edit by hand.\n"
        " * Fields: 240 x 200 (screen rows 20..219), 8-bit indices into an RGB565 palette stored byte-swapped.\n"
        " * Sprites: 8-bit indices, 0 = clear, into their own palette; x, y = top-left on the screen; bx, by = where the\n"
        " * beam leaves the mouth (sprite pixels, -1 = none). Poses: 0 REST, 1 BARK, 2 HOWL-INHALE, 3 HOWL (0 = none). */\n"
        f"#define SA_FIELD_Y {FIELD_Y}\n#define SA_FIELD_H {FIELD_H}\n#define SA_BYTES {total}u\n"
        "typedef struct { int16_t x, y; uint16_t w, h; int16_t bx, by; const uint16_t *pal; const uint8_t *px; } sa_sprite_t;\n"
        "typedef struct { const uint16_t *pal; const uint8_t *px; const sa_sprite_t *const *pose; int16_t head[4]; } sa_scene_t;\n\n"
        + "\n".join(parts) + "\n" + "\n".join(structs) + "\n\n"
        + f"static const sa_scene_t SA_SCENE[{len(lay['scenes'])}] = {{\n    {scenes}\n}};\n")
    out.write_text(text)
    print(f"{out}: {len(lay['scenes'])} scenes, {len(sprites)} sprites, {total} bytes of art")


if __name__ == "__main__":
    main(sys.argv[1:])
