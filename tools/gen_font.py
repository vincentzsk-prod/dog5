#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""The panel's two fonts: tools/gen_font.py -> firmware/gen/felucca_font.h (committed, so a build needs
no regeneration). Cut from assets/fonts/ter-u16n.bdf (Terminus 16px, SIL OFL, see
assets/fonts/Terminus-LICENSE.txt): every glyph in it shares one 8x16 bounding box (BBX 8 16 0 -4), so
each row is a single hex byte, MSB = the glyph's leftmost column.

FONT_S is that glyph padded PAD px blank on each side (bw = 8 + 2*PAD) so gfx.c's cv_text can draw it
straight from the pen position; FONT_L is FONT_S's own bitmap doubled 2x in both axes (gfx.c draws the
OBERVAVE wordmark in it) -- not re-cut from a bigger source font. Both store 1-bit glyphs as 4-bit
nibbles (0x0 / 0xF) so cv_text's one blend path (a 16-step ramp) covers them without a second code path
for some future truly anti-aliased font.

FONT_S covers ASCII 32-126 plus Ø (U+00D8 / byte 0xD8, Latin-1 position -- gfx.c indexes text bytes
directly, no UTF-8 decoding, so a source string must spell it `\\xD8`, not a literal Ø saved as UTF-8's
two bytes) so `THE DØG` reads right instead of `THE D?G` (CLAUDE.md §4). gfx.c's glyph() already turns
anything in 127-159 (C1 controls) into '?' before it ever indexes the glyph tables, and anything outside
first..last the same way, so those bytes need an array *entry* (first..last must stay one contiguous
run) but never a real bitmap: they're written as zero-width placeholders (0 bytes of DATA) rather than
cutting the Latin-1 Supplement block the BDF does have, which would cost ~8 KB of flash nobody asked
for. A byte in 160-215 that's none of these placeholders would draw blank, not '?' -- harmless, since
nothing in the firmware emits one."""
import re
import sys
from pathlib import Path

BDF = Path(__file__).parent.parent / "assets" / "fonts" / "ter-u16n.bdf"
GW, GH = 8, 16    # every glyph's own bounding box in this font (BBX 8 16 0 -4, confirmed for all 1356)
PAD = 2           # blank px of canvas added left and right of the glyph: bw = GW + 2*PAD
S_FIRST, S_LAST = 32, 0xD8                       # ' ' .. 'Ø'
S_REAL = set(range(32, 127)) | {0xD8}            # codepoints that get a real bitmap; the rest, blank
L_FIRST, L_LAST = 32, 95                         # 'OBERVAVE' wordmark range: upper case + punctuation


def parse_bdf(path):
    """{codepoint: [16 row-bytes, MSB = leftmost column]} for every glyph whose BBX is the font's own."""
    text = path.read_text()
    glyphs = {}
    for m in re.finditer(r"STARTCHAR .*?\nENCODING (-?\d+)\n.*?BBX (\d+) (\d+) (-?\d+) (-?\d+)\nBITMAP\n(.*?)\nENDCHAR",
                          text, re.S):
        cp, bw, bh, xoff, yoff = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5))
        if cp < 0 or (bw, bh, xoff, yoff) != (GW, GH, 0, -4):
            continue      # (none in ter-u16n.bdf; a future source font could still have an odd one)
        rows = [int(r, 16) for r in m.group(6).strip("\n").split("\n")]
        glyphs[cp] = rows
    return glyphs


def pack_rows(rows, w):
    """rows: list of h GW-wide 1-bit row-bytes -> w-wide (w = GW + 2*PAD) nibble bitmap, PAD px of
    0x0 on each side, packed 2 px/byte (high nibble first, as cv_text reads it)."""
    bpr = (w + 1) // 2
    out = bytearray(bpr * GH)
    for y, row in enumerate(rows):
        for x in range(GW):
            if not (row >> (GW - 1 - x)) & 1:
                continue
            cx = PAD + x
            i = y * bpr + cx // 2
            out[i] |= 0xF0 if (cx & 1) == 0 else 0x0F
    return bytes(out)


def scale2x(rows, w, h):
    """nibble bitmap (bpr = (w+1)//2 bytes/row, h rows) -> the same picture at 2x in both axes."""
    bpr = (w + 1) // 2
    w2, h2 = w * 2, h * 2
    bpr2 = (w2 + 1) // 2
    out = bytearray(bpr2 * h2)
    for y in range(h):
        for x in range(w):
            v = rows[y * bpr + x // 2]
            v = (v & 0xF) if (x & 1) else (v >> 4)
            if not v:
                continue
            for dy in range(2):
                for dx in range(2):
                    cx = x * 2 + dx
                    cy = y * 2 + dy
                    i = cy * bpr2 + cx // 2
                    out[i] |= 0xF0 if (cx & 1) == 0 else 0x0F
    return bytes(out)


def build_font(glyphs, first, last, real):
    """-> (data bytes, [offset per glyph], [bitmap width per glyph], [advance per glyph])."""
    w = GW + 2 * PAD
    data, off, bw, adv = bytearray(), [], [], []
    for cp in range(first, last + 1):
        off.append(len(data))
        if cp in real and cp in glyphs:
            data += pack_rows(glyphs[cp], w)
            bw.append(w)
            adv.append(GW)
        else:
            bw.append(0)        # never drawn: glyph() redirects 127-159 and anything > last to '?'
            adv.append(0)       # before indexing; anything else unused just advances the pen by 0
    return bytes(data), off, bw, adv


def hex_arr(name, data, per=24):
    out = [f"static const uint8_t {name}[{len(data)}] = {{"]
    for i in range(0, len(data), per):
        out.append("    " + ", ".join(f"0x{b:02x}" for b in data[i:i + per]) + ",")
    out.append("};")
    return out


def dec_arr(name, ctype, vals):
    return [f"static const {ctype} {name}[{len(vals)}] = {{" + ", ".join(str(v) for v in vals) + "};"]


def emit(name, first, last, data, off, bw, adv, h, pad):
    L = []
    L += hex_arr(f"{name}_DATA", data)
    L += dec_arr(f"{name}_OFF", "uint16_t", off)
    L += dec_arr(f"{name}_ADV", "uint8_t", adv)
    L += dec_arr(f"{name}_BW", "uint8_t", bw)
    L.append(f"static const felucca_font_t {name} = {{ {h}, {pad}, {first}, {last}, "
             f"{name}_ADV, {name}_BW, {name}_OFF, {name}_DATA }};")
    return L


def main(path):
    glyphs = parse_bdf(BDF)
    if 0xD8 not in glyphs:
        sys.exit(f"{BDF}: no Ø (U+00D8) glyph found")

    s_data, s_off, s_bw, s_adv = build_font(glyphs, S_FIRST, S_LAST, S_REAL)
    w_s = GW + 2 * PAD

    # FONT_L: FONT_S's own bitmap doubled 2x, for its narrower 32..95 range (gfx.c's wordmark font)
    l_real = set(range(L_FIRST, L_LAST + 1))
    l_data, l_off, l_bw, l_adv = bytearray(), [], [], []
    bpr_s = (w_s + 1) // 2
    for cp in range(L_FIRST, L_LAST + 1):
        l_off.append(len(l_data))
        if cp in l_real and cp in glyphs:
            rows_s = s_data[s_off[cp - S_FIRST]: s_off[cp - S_FIRST] + GH * bpr_s]
            l_data += scale2x(rows_s, w_s, GH)
            l_bw.append(w_s * 2)
            l_adv.append(GW * 2)
        else:
            l_bw.append(0)
            l_adv.append(0)

    L = ["/* generated by tools/gen_font.py from assets/fonts/ter-u16n.bdf: do not edit */", "#pragma once"]
    L += emit("FONT_S", S_FIRST, S_LAST, s_data, s_off, s_bw, s_adv, GH, PAD)
    L += emit("FONT_L", L_FIRST, L_LAST, bytes(l_data), l_off, l_bw, l_adv, GH * 2, PAD * 2)
    Path(path).write_text("\n".join(L) + "\n")
    print(f"font: {path} (FONT_S {S_FIRST}..{S_LAST}, FONT_L {L_FIRST}..{L_LAST})")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "firmware/gen/felucca_font.h")
