# 20 · Fire & Ice · Chapter III · The Bakshi Tomes

*Voiced 6 Nov 2026 (Batch 5B), approved after listening: variant D ("20 Fire & Ice D"). Renders: `reference-renders/20-fire-and-ice_D_*.wav`. Tables (on the voicing branch): `listen/voicing/batch-05b/20-fire-ice/README.md`.*

## 2. What it sounds like

A single-voice lead that tears into every detached note with a bright hard-sync sweep, which then settles into a rounder, singing line. It is pushed into overdrive and thrown into a long, ping-ponging echo that keeps repeating behind the playing and sits on top of a short spring. Notes slide into each other a little. Played legato, the sweep is not re-fired, so a smooth run carries only the settled tone and loses the tear.

## 3. Gear inspirations (docs only, "inspired by")

- **Sequential Pro-One** — *the hard-sync lead; Rip, Bright.* Rip: on a detached A4 the centroid falls 2793 → 1850 → 1360 → 1272 Hz over the windows 0–100 / 100–200 / 200–400 / 400–800 ms, and the sweep adds +1.8 dB above 1.2 kHz in the first 100 ms against the same note with the sweep off (measured). Bright: that first-100-ms centroid of 2793 Hz (measured; no comparison with the Pro-One was made).
- **Ibanez Tube Screamer** — *the soaring drive; Driven.* GROWL 48 lowers the crest factor of the dry note-on region by 3.3 dB (8.3 → 5.1 dB) with the level held within 0.03 dB (measured). No claim about the pedal's curve is made.
- **Roland RE-201 Space Echo** — *the drench; Wet.* The first repeat sits 10.0 dB under the note, and 8 repeats stay above −40 dB (3 above −20 dB) under it (measured). The echo is a free-ms time, not a tempo-synced one.

Closest to: **a Pro-One sync lead through an overdrive pedal into a Space Echo**.

Nothing here says the patch matches these: it was built toward the descriptions, by measurement, and approved by ear.

## 4. How to play it

- **MONO lead, one note at a time.** Chords play the last key only. The sweep fires on **detached** notes; with **legato** playing (a new key down before the old one is up) the envelopes are not re-fired and the sweep does not return. Measured on the same eight-note riff, dry: the centroid over the first 100 ms of notes 2–8 averages 3610 Hz detached against 1573 Hz legato; the first note of either is 1999 Hz.
- **Register:** the sweep was measured on A4 (above) and on A3: centroid 1999 → 1190 Hz in the windows 0–100 / 100–200 ms. Notes up to A5 were played in the riff phrases; no other register was measured.
- **The sweep survives the filter.** With the cutoff at 84 (1661 Hz before key tracking), the energy above 1.2 kHz of the sweep sits only −1.0 / −2.7 / −3.4 / −3.4 dB under the same patch with the filter fully open (CUTOFF 127), in the four windows (A4).
- **Glide:** GLIDE 56 takes 94 ms to come within 50 cents of an octave step (64 ms to 90 % of the octave).
- **Echo:** 374 ms, FEEDBK 92, MIX 85, PINGPONG at its maximum. There is no tempo sync: the time does not follow the clock.
- **Level and cost:** VOLUME 126, −18.1 dBFS RMS over the note-on region of the single-note lead phrase (K-weighted −17.5), peak −8.4 dBFS over every audition phrase. Phrase (b)'s stabs read −16.6 dBFS but a MONO patch plays one key of each. **CPU 1967 host instr/sample worst case** (GROWL accounts for +589 of it). The device render time is not measured.
- **Tricks:** SLOBBER, SEQ held (Tape Stop), the kill switch (HEEL), CHEW are untested on this patch. The kill switch clears the echo buffers (engine fact; not tested here).

## 5. Final values (for debugging, not for players)

`MODE MONO, OSC1 SAW LEVEL 0 (the silent sync master), OSC2 SAW LEVEL 127 SEMI +7 SYNC on ENV>O2 104 (+15.2 st at the envelope's top), FILTER LP24 CUTOFF 84 (1661 Hz) RESO 10 KEY TRK 64 ENV AMT 85, FILTER ENV A20 D80 S20 R60, AMP ENV A2 D70 S100 R50, GLIDE 56, VINTAGE 30, SPREAD 60, no LFO, GROWL 48, BBD ALLEY 107 (374 ms) FEEDBK 92 TONE 55 MIX 85 PINGPONG 127, spring SIZE 80 DAMP 60 PRE-DLY 20 DRAIN 30, CHEW 0, VOLUME 126` — `PF_FIRE_ICE` in `firmware/src/obv_patches.h`.
