#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Driver Manual Parts 3-4 from the 32 voice cards (Batch 30): one source for the patch text, so the manual, the cards
and the web player's card can't drift apart. Reads dog5-docs/voicing/cards/NN-*.md, sections 2-4 (and the name and
chapter from the card's title); writes dog5-docs/manual/DOG-5-driver-manual-patches.md.
   python3 tools/make_manual_patches.py [--check]"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CARDS = ROOT / "dog5-docs/voicing/cards"
OUT = ROOT / "dog5-docs/manual/DOG-5-driver-manual-patches.md"

CHAPTERS = [
    ("I", "JALOPY", "Egg punk and garage psych. Fat sources through a blown console: basses, a sync lead, a kick and "
     "the fuzz. On screen: the Jalopy scene, accent Sun Yellow."),
    ("II", "BEE-TCH", "Surf rock and skinhead reggae: the spring-reverb chapter. On screen: the Bee-tch scene, accent "
     "Wave Turquoise."),
    ("III", "MOONSHINE", "Dark fantasy and atmosphere: drones and slow pads. Most of them want a held key, so REC (HOLD) "
     "is your friend here. On screen: the Moonshine scene, accent Foam White; hold a note and the dog howls."),
    ("IV", "ACID CAN", "The survivors of the classic polysynths, rebuilt by ear (never copied from factory data), then "
     "the signature patch and the blank slate. On screen: the Acid Can scene, accent Acid Chartreuse."),
]

HEAD = """# COLLAR — THE DØG-5 MANUAL, PARTS 3–4 (the 32 patches)

*Continues `DOG-5-driver-manual.md` (Parts 0–2B). **Generated from the 32 voice cards** (`dog5-docs/voicing/cards/`)
by `tools/make_manual_patches.py` since Batch 30 (23 Nov 2026): edit a card, then run the script; don't edit this file
by hand. The measured voicing notes that used to be here are in each card's section 6 and in the repo's
`dog5-docs/manual/DOG-5-driver-manual-records.md`.*

## PART 3 — THE 32 PATCHES

Four chapters of eight, one per scene on HOME. Slots 1–32 are **THE POUND**: play them and tweak them as much as you
like; a save goes to **THE PACK** (33–99, see 1.9), so the factory sounds are always there to come back to.

Each patch has three parts: **what it sounds like**, **sound design notes** (where it lives on the keybed, how to play
it, what to reach for) and **the gear that inspired it**. The live tricks (SLOBBER, Tape Stop, HEEL) and the four Psych
Chain macros work on every patch; a note mentions them only where they suit or fight that patch. Every patch was voiced
by ear and the bank is level-matched, so switching patches doesn't jump, except where a note says so.
"""

TAIL = """
## PART 4 — ABOUT THE GEAR INSPIRATIONS

Each patch lists real instruments and pedals whose *character* it draws on, with the trait it carries in italics, so
"a bit more Mono/Poly" points somewhere you can hear. They are inspirations, not imitations: nothing is modelled,
sampled or copied, and the gear names appear only in this manual, never in patch names or on the screen. "Closest to"
is the one instrument you'd name if someone asked what it sounds like; it doesn't claim the patch matches it.

All trademarks belong to their owners. DØG-5 is not affiliated with or endorsed by any of them.
"""


def card(path):
    t = path.read_text(encoding="utf-8")
    title = t.splitlines()[0]
    m = re.match(r"# (\d\d) · (.+?) · Chapter (I{1,3}|IV) · ", title)
    if not m:
        sys.exit(f"make_manual_patches: {path.name}: title not in the card format: {title}")
    sec = {k: v.strip() for k, v in re.findall(r"^## (\d)\. [^\n]*\n(.*?)(?=^## \d\. |\Z)", t, re.S | re.M)}
    if not all(k in sec for k in "234"):
        sys.exit(f"make_manual_patches: {path.name} lacks section 2, 3 or 4")
    return m.group(1), m.group(2), m.group(3), sec


def build():
    cards = [card(p) for p in sorted(CARDS.glob("[0-3][0-9]-*.md"))]
    if [c[0] for c in cards] != [f"{i:02d}" for i in range(1, 33)]:
        sys.exit("make_manual_patches: expected cards 01-32")
    out = [HEAD]
    for ci, (num, name, intro) in enumerate(CHAPTERS):
        out.append(f"\n### CHAPTER {num} — {name}\n\n*{intro}*\n")
        for nn, pname, chap, sec in cards[ci * 8:(ci + 1) * 8]:
            if chap != num:
                sys.exit(f"make_manual_patches: card {nn} says chapter {chap}, expected {num}")
            out.append(f"\n#### {nn} · {pname}\n\n{sec['2']}\n\n**Sound design notes**\n\n{sec['4']}\n\n"
                       f"**Gear inspirations**\n\n{sec['3']}\n")
    out.append(TAIL)
    return "".join(out)


if __name__ == "__main__":
    text = build()
    if "--check" in sys.argv:
        ok = OUT.read_text(encoding="utf-8") == text
        print(("in sync: " if ok else "STALE: ") + str(OUT.relative_to(ROOT)))
        sys.exit(0 if ok else 1)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}  {len(text)} chars")
