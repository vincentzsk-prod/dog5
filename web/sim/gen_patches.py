#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# The 32 factory names for the web player's patch list, read (never written) from the {"NAME", PF_xxx} table
# FACTORY[NFACT] in firmware/src/obv_patches.h, as the firmware has them: "\xD8" is the Ø (font byte 0xD8).
# With each name, its voice card (dog5-docs/voicing/cards/NN-*.md), sections 2-4 as HTML: what it sounds like, the gear
# inspirations, how to play it. Section 5 (the final values, for debugging) and the card's italic file line stay out.
#   python3 web/sim/gen_patches.py OUT.json        (needs Python-Markdown: pip install markdown)
import html, json, re, sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
src = (root / "firmware/src/obv_patches.h").read_text(encoding="utf-8")
body = src[src.index("FACTORY[NFACT] = {"):]
body = body[:body.index("};")]
names = [m.group(1) for m in re.finditer(r'\{"((?:[^"\\]|\\.)*)",\s*PF_\w+\}', body)]
names = [re.sub(r"\\x([0-9A-Fa-f]{2})", lambda m: "Ø" if m.group(1).upper() == "D8" else chr(int(m.group(1), 16)), n) for n in names]
nfact = int(re.search(r"#define\s+NFACT\s+(\d+)", (root / "firmware/src/obv_params.h").read_text()).group(1))
if len(names) != nfact or any("\\" in n or '"' in n for n in names):
    sys.exit(f"gen_patches: found {len(names)} names for NFACT {nfact}, or an escape left: {names}")
chapters = ["I · Jalopy", "II · Bee-tch", "III · Moonshine", "IV · Acid Can"]   # 8 slots each (chapter names locked 17 Nov 2026)
try:
    import markdown
except ImportError:
    sys.exit("gen_patches: needs Python-Markdown for the voice cards (pip install markdown)")

def listfix(text):
    """Python-Markdown wants a blank line before a list; the docs (written for GitHub) often have none."""
    out, prev = [], ""
    for line in text.split("\n"):
        if re.match(r"\s{0,3}([-*+]|\d+\.) ", line) and prev.strip() and not re.match(r"\s*([-*+]|\d+\.) ", prev) and not prev.startswith("  "):
            out.append("")
        out.append(line); prev = line
    return "\n".join(out)

def md(text):
    h = markdown.markdown(listfix(text.strip()), extensions=["tables"], output_format="html")
    h = re.sub(r"<a\b[^>]*>(.*?)</a>", r"\1", h, flags=re.S)        # repo-relative links mean nothing on the page
    if re.search(r"<(script|iframe|img|style)\b", h, re.I):
        sys.exit("gen_patches: a card carries markup the page does not take")
    return h

def card(slot):
    f = sorted((root / "dog5-docs/voicing/cards").glob(f"{slot:02d}-*.md"))
    if len(f) != 1:
        sys.exit(f"gen_patches: no single card for slot {slot}: {f}")
    t = f[0].read_text(encoding="utf-8")
    sec = {}
    for m in re.finditer(r"^## (\d)\. [^\n]*\n(.*?)(?=^## \d\. |\Z)", t, re.S | re.M):
        sec[m.group(1)] = m.group(2)
    if not all(k in sec for k in "234"):
        sys.exit(f"gen_patches: {f[0].name} lacks section 2, 3 or 4")
    return {"sound": md(sec["2"]), "gear": md(sec["3"]), "play": md(sec["4"])}

out = [{"chapter": chapters[i // 8], "slot": i + 1, "name": n, "card": card(i + 1)} for i, n in enumerate(names)]
Path(sys.argv[1]).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"patches: {len(out)} names -> {sys.argv[1]}")
