#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Batch 30, run once: write the rewritten player text (tools/sound_text_b30.py) into sections 2-4 of the 32 voice
cards, and keep the old sections 2-4 word for word as section 6, "The voicing record", so nothing measured is lost."""
import pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from sound_text_b30 import P
CARDS = pathlib.Path(__file__).resolve().parent.parent / "dog5-docs/voicing/cards"
for f in sorted(CARDS.glob("[0-3][0-9]-*.md")):
    nn = f.name[:2]; t = f.read_text()
    if "## 6. The voicing record" in t:
        print("skip (done)", f.name); continue
    i2 = t.index("## 2."); i5 = t.index("## 5.")
    old = t[i2:i5].rstrip() + "\n"
    old = re.sub(r"^## ([234])\. ", r"### \1. ", old, flags=re.M)
    e = P[nn]
    gear = "\n".join(f"- **{g}** — {w}." for g, w in e["gear"])
    notes = "\n".join(f"- {n}" for n in e["notes"])
    new = (f"## 2. What it sounds like\n\n{e['sound']}\n\n"
           f"## 3. Gear inspirations (docs only, \"inspired by\")\n\n{gear}\n\nClosest to: **{e['closest']}**.\n\n"
           f"## 4. Sound design notes\n\n{notes}\n\n")
    tail = t[i5:].rstrip() + "\n"
    rec = ("\n## 6. The voicing record (measured notes, not for players)\n\n"
           "*Sections 2–4 as they stood before the Batch 30 rewrite (23 Nov 2026): the measurements, the variants and what "
           "was and wasn't tested. The player text above is drawn from this.*\n\n" + old)
    f.write_text(t[:i2] + new + tail + rec)
    print("ok", f.name)
