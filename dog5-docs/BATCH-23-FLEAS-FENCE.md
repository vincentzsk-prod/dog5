# Batch 23: the fence, FLEAS, the Acid Chartreuse beam, the chapter accents (v0.4.2)

21 Nov 2026, Vincent Kruger with Claude. Branch `build/batch-23-fleas-fence-beam`. Asked for 21 Nov ("finish Stage 3: the
fleas and the fence, and the beam in the chartreuse, one colour across all scenes"). The sound is untouched (WAVs
byte-identical to `main`). Built from the canon (character brief §2, §4.3, §5, §6.1; art direction §2.1 U1–U4, §9, §9.1),
re-read for the painted scenes; the choices below are mine where the canon left them open, and each is one place in
`firmware/src/dog5_scene.h`.

## The beam

**Acid Chartreuse `#DEF402` in all four chapters** (`SC_BEAM_C`). Vincent's call, 21 Nov; it replaces the canon's white
trace ("the truth channel"). FLEAS never touches it.

## The chapter accents (decided here, from each scene's art, all from the brand palette)

| Ch | Accent | From |
|---|---|---|
| I JALOPY | Sun Yellow `#F8CD30` | the taxi |
| II BEE-TCH | Wave Turquoise `#10C5AF` | the wave |
| III MOONSHINE | Foam White `#FFFFFF` | the moonlight (the canon's magenta never matched the painting) |
| IV ACID CAN | Acid Chartreuse `#DEF402` | the ooze |

They colour the chapter's name in the top bar (was Grime Olive) and its damage to the fence.

## The fence

The top bar (rows 0–19, with its rule) is THE FENCE. The beam lands in the top-right corner; there the fence breaks, in a
zone that grows in from the corner, ragged, each chapter by its canon verb:

- **I JALOPY scorches:** the fence is deleted to black behind a flickering edge (Sun Yellow / Ray Red), sparks in the char.
- **II BEE-TCH soaks:** the wave pours down over it from the top edge, dithered turquoise over deep teal.
- **III MOONSHINE fogs:** moonlight grain rises through it, densest low and near the corner.
- **IV ACID CAN wrecks:** it cracks into 8 px shards that each drop their own distance, acid in the cracks.

Signal: the bark's onset hits it (damage 160 of 256), a sounding note keeps chipping it (+12 every 150 ms), and it heals
32 a step after the sound stops, so **within 1.2 s, however long the note** (canon U1). It redraws only the top bar, at
most every 150 ms (6.7 Hz). **The bottom bar (number and name) is never touched.** Shards stay inside the fence (the
canon's debris falling down the right margin would repaint the field every frame; not done).

## FLEAS

A global dial (not per patch), 0–100, **GLOBAL page knob 2** (it was empty), shown as `ITCH 42`; 2 a detent; stored in
the settings byte the sequencer's pattern number had (`set.fleas`; layout and `SET_VERSION` unchanged; an old value over
100 reads as 0). Default CLEAN. It acts on HOME's scene only (the panel pages stay legible):

| Dial | Stage | On HOME |
|---|---|---|
| 0–15 | CLEAN | nothing |
| 16–65 | ITCH | the dog's edges boil: his rows, 8 at a time, jump ±2 px, re-rolled every 150 ms (15 → 60 % of them) |
| 66–90 | SCRATCH | + 1–5 bands of the field (2–8 rows) shear sideways 2–10 px in even steps, re-rolled every 330 ms |
| 91–100 | MANGE | + the fence's text scrambles (~40 % of its characters, ~3 Hz), 2–6 Radioactive Mustard blotches (a 50 % dither) on the field re-rolled every second, and the boil drops ~30 % of its frames |

Turning it back down clears each stage's rot. **Never touched:** the beam, the bottom bar. Safety (canon §9.1): every change
is a small area at ≤ 6.7 Hz, the boil and shear move on a 2 px lattice, nothing swings the whole screen's brightness.

## Numbers and checks

Image 391,560 B (+1,956); RAM 34,928 B (+416: the FLEAS state); pool unchanged. New `tests/fleas_fence.txt` (the four
chapters' fence and its healing, FLEAS through all four stages and back, the GLOBAL knob); `tests/run_tests.sh` ALL TESTS
PASSED; `node tests/sim_test.mjs` passes. `./build.sh --release 0.4.2` twice, same SHA-256
`2c733bfc24d80c72e20e924395bb4a5c8c64355c7cc0737f1a90bbd4852e17c6`, 614,757 B, identity `FM-1_964`; installer page
regenerated (`dog5-0.4.2-20261121.fwsc`), in sync, 20/20. It carries Batch 22 (v0.4.1 was not flashed).

## For the unit

The fence's look in each chapter, FLEAS at each stage (is ITCH's 2 px boil visible enough on the panel? is MANGE gross
enough?), the chartreuse beam over each scene, and any drag on notes or knobs with FLEAS at MANGE and a chord held.
