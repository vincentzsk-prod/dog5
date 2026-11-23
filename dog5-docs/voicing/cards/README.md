# Voice cards

One card per approved patch: `NN-name.md` (e.g. `03-half-life.md`). It is the permanent catalogue entry — what the patch
sounds like, so nobody has to remember — and its text becomes the player-facing description in the Driver Manual.

**A card is written for every approved patch, including patches approved "as is".**

## Format (follow it exactly)

1. **HEADER** — `NN · Name · Chapter <numeral> · <CHAPTER NAME>` (JALOPY · BEE-TCH · MOONSHINE · ACID CAN, since 17 Nov) as the title (plus one italic line: date, where the renders and log are).
2. **WHAT IT SOUNDS LIKE** — 2–3 plain sentences for a player, in the dictionary vocabulary (fat, slop, seasick, choppy…).
   No parameter numbers. Someone who has never heard the patch must know what to expect.
3. **GEAR INSPIRATIONS** — 3–6 items from the approved list, each with the trait it carries, then one line `Closest to: …`.
4. **SOUND DESIGN NOTES** (was "How to play it", renamed 23 Nov; rewritten for players in Batch 30) — 4 to 7 short bullets:
   where it lives on the keybed, how to play it (detached / held, chords), what to reach for to push it, and where it
   does not work. A number only where it helps playing. Mention a trick or macro only where it suits or fights the
   patch; no "untested" lines (the manual says once that every trick works on every patch).
5. **FINAL VALUES** — the committed parameter list as one compact line, labelled "for debugging, not for players".
6. **THE VOICING RECORD** (since Batch 30) — the measured notes: variants, dates, levels, CPU, what was and wasn't
   tested. Not for players; the player text above is drawn from it. For the 32 factory patches it holds their sections
   2–4 as they stood before the rewrite.

**Sections 2–4 are the source of Driver Manual Parts 3–4** (`tools/make_manual_patches.py`) and of the web player's
card (`web/sim/gen_patches.py`): edit the card, then run both.

## Rules

- **Card text may name gear** (docs only, "inspired by"). **Patch names and on-screen strings never may** (CLAUDE.md §13).
- **Sections 1–4 are player-facing text for the Driver Manual.** Write them to be lifted as they are. **Section 5 is for debugging only, section 6 the record.**
- Only claim what was measured or heard in the voicing round. Player text (2–4) stays plain; the evidence and anything untested go in section 6.
