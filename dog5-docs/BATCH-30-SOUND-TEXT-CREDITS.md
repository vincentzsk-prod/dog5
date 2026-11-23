# Batch 30 — the player-facing sound text, the manual page's look, the credits pass

**23 Nov 2026**, branch `build/batch-30-sound-text-credits` from `origin/main` 6603484 (Batch 29 merged). **No firmware
code changed**: the 0.4.5 package and the installer's package are byte-identical; the browser player's sound is the host
build's, sample for sample.

## 1. The sound text, rewritten for players (backlog §1 step 2)

Vincent approved a two-patch sample (01 Red Pill, 30 THE DØG) and asked for the "Tricks untested" lines to go.

- **The 32 voice cards** (`dog5-docs/voicing/cards/`): sections 2–4 rewritten. *What it sounds like* lightly cleaned (no
  numbers); *Sound design notes* as 4–7 short bullets: where it lives on the keybed, how to play it, what to reach for,
  where it doesn't work, a number only where it helps playing; *Gear inspirations* as instrument + trait, the measurement
  brackets gone. **The old sections 2–4 are kept word for word as a new section 6, "The voicing record"**, so nothing
  measured is lost. The new text lives in `tools/sound_text_b30.py`, written in by `tools/apply_sound_text.py` (run once).
  Facts were taken from each card's own record; nothing new is claimed. The cards README states the new format.
- **Manual Parts 3–4 are now generated from the cards** (`tools/make_manual_patches.py`, `--check`): one source for the
  manual, the cards and the web player's card. Each patch: what it sounds like, sound design notes, gear inspirations.
  Part 4 is now one short section about the gear inspirations (not imitations; trademarks). One sentence at the top of
  Part 3 replaces every "Tricks untested": the tricks and macros work on every patch, and a note mentions them only
  where they suit or fight the patch.
- **Manual Parts 2 and 2B rewritten:** each dictionary word keeps its meaning and how to get more of it, with a patch to
  hear it on; the measurements, the "MUD ratio" and the voicing-session conventions (the echo rule) are out.
- **The old Parts 2, 2B, 3 and 4, word for word:** `dog5-docs/manual/DOG-5-driver-manual-records.md` (in the repo). The Parts 3–4 file went from about 90 KB to 40 KB.
- Two facts fixed on the way: card 07 and the dictionary said tape dropouts come in "from about 100"; the tape stage starts
  them at 45 % of CHEW (about the middle of the knob). Card 31's "tapping a time in on the BBD page" (tap tempo is gone)
  is out. Card 21 keeps "should" for the pedal / REC hold (not tried on that patch).

## 2. The manual page and the player's card (Vincent: easier to navigate and digest, and cooler)

`tools/make_manual_page.py` (page regenerated, 110 KB):
- **The contents** are one card per part with a numbered badge (0, 1, 2, 2B, 3, 4), collapsible, the open one following
  where you are; sections carry their numbers in mono and their names in the body face, so the groups read apart;
  Part 3 lists the four chapters in their accent colours with the 32 patches as a two-column grid; a find box filters
  sections and patches; the current section is highlighted as you scroll. On a phone the contents fold behind a button.
- **The text:** parts open with a banner, sections with a numbered heading and an accent bar, chapters in their colours,
  each patch is a card in its chapter's colour with a numbered badge and small labels for *Sound design notes* and *Gear
  inspirations*; lines are held to a readable width; tables are striped; a back-to-top button.
- **Patch names are set in the body face, not the display face:** the display face draws "z" like "3", so zzuFuzz read
  "33uFu33".
- **The web player's card** (`web/sim/sim.css`, `sim.js`): the same name fix, the card's top edge, number badge and labels
  in the patch's chapter colour.

Checked in headless Chromium at 1400 px and 390 px: no page errors.

## 3. The credits pass (backlog §1 step 3)

- `LICENSING.md`: DØG-5's own parts now include the launch screen, the documents (the manual, the voice cards, the
  voicing kit, the manual page's tools) and DØG-5's changes to the web player; the art line says hand-painted by Vincent
  in Pixelorama, some started from a small sampled section of a public-domain still, no AI-generated art (Vincent's
  record, `DOG-5-chapter-names.md`); the web fonts' row includes the manual page; a trademarks paragraph for the gear
  named as inspiration.
- `NOTICE`, `README.md`: the gear-trademark line, the hand-painted art (no AI), the four fonts (SIL OFL 1.1).
- The web player's footer and the manual page's footer: the art and the fonts. **The installer page had no credits
  line**: it now has a footer (OberVave / Dinghy / Felucca / SLOOP, the install protocol's origin, the art, the fonts).
- `fmhub.json`: unchanged (the Hub's card needs no credits). The Hub also accepts an optional `author` field; not added
  without the Hub's exact format.

## Tests

A plain `./build.sh` (`FM-1_3645000`), then `sh tests/run_tests.sh`: **ALL TESTS PASSED**, including a new check that
Parts 3–4 match the cards and the manual page matches its sources. Browser player test passed (sound = host build);
installer page 21/21 and in sync with the 0.4.5 package.
