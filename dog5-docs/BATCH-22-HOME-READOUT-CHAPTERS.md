# Batch 22: the HOME knob readout, the beam through TAPE STOP, a saved patch keeps its scene (v0.4.1)

21 Nov 2026, ZIGGY with Claude. Branch `build/batch-22-home-readout-chapters`. Asked for after v0.4 was flashed and
tested (20–21 Nov). The sound is untouched: WAVs byte-identical to `main` (SEQ-held scripts included).

## 1. The knob values on HOME

Before: on HOME, turning CUTOFF / RESO / ENV AMT / RELEASE showed nothing (only a MIDI CC to the cutoff did). Now the knob's
label and value show in the top bar for a second (`RESO 76`, `RELEASE 1.5ms`), as SELECT's `LFO RATE` already did, then the
tags come back (`readout()` in the encoder loop, HOME with no layer held). `tests/home_readout.txt`.

## 2. The beam dives with TAPE STOP

Before: the scope listened to the voices before the effects, so holding SEQ left the beam unchanged. Now, while TAPE STOP
runs (SEQ held, or its release still sounding), the scope listens to the whole mix after the deck (`scope_feed()` in
`engine_audio`; `deck_quiet` read once a block). At rest it listens where it always did (the dry voices: the clean beam).
The waves lengthen as the tape slows; when no zero crossing comes for 150 ms (the stopped tape's silence) the beam goes
flat. `tests/scene_tapestop.txt`.

## 3. A saved patch keeps its scene

Before: the scene came from the slot alone (`prog % 32 / 8`), so a factory patch saved into THE PACK showed the PACK slot's
scene (slot 33 = JALOPY, whatever the patch). Now the patch carries its chapter: byte 94 of the record (one of the two
spare bytes after the name), `PATCH_CHAPTER_AT`, 1–4 = I–IV. A factory patch gets its own when it loads; saving copies it;
`patch_chapter()` gives the scene (HOME and the boot animation), falling back to the slot's chapter when the byte is 0
(INIT, and saves made before this build: **a patch saved on v0.4 shows its slot's scene until it is saved again**). A
pre-lock save over 1–32 moved by `pound_rescue` takes the chapter of the slot it was saved over. The store format is
unchanged (the byte was always stored; the selftest still round-trips all 96 bytes). `tests/controls/chapter_save.txt`.

## Also

- `dog5-panic-test.html` (given to Vincent, not in the repo): a one-button Web MIDI page that sends CC 123 + CC 120 on all
  16 channels, to check on the unit that a MIDI panic releases HOLD.
- **To record in the housekeeping pass (Vincent, 21 Nov):** say up front, in the README, the installer page and the release
  notes, that DØG-5 was built and thoroughly tested on a unit with the older flash chip (Puya P25Q80, `0x856014`) and its
  behaviour on the newer chip (`0xB36014`) is untested.
- On-unit results 20–21 Nov: leaving DØG-5 for a Hub firmware (no trace of DØG-5 left in its menus) and coming back from our
  page both work; a save goes to the right PACK slot and survives a power cycle; 1–32 can't be overwritten.

## Numbers and the build

Image 389,604 B (+652); RAM 34,512 B and pool 308,496 B unchanged. `./build.sh --release 0.4.1` twice, same SHA-256
`5bf90d476f7094abd5c4ba2336b2a6ce5284c155f4217c2c9a724ad17ad94f53`, 614,757 B, identity `FM-1_964` (the identity carries
X.Y only: 0.4.1 and 0.4 read the same on the unit; the installer page names 0.4.1). Installer page regenerated
(`dog5-0.4.1-20261121.fwsc`), in sync, 20/20; `tests/run_tests.sh` ALL TESTS PASSED; `node tests/sim_test.mjs` passes.
