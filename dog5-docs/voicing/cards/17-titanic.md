# 17 · Titanic · Chapter III The Bakshi Tomes

*Voiced Nov 2026, approved as is (variant B of Batch 2A). Renders: `listen/voicing/batch-02a/17-titanic/` on the `listen/batch-02a-weight-and-space` branch (B is this patch). Log: `../17-titanic.md`.*

## 2. What it sounds like

Cold, heavy and hollow: two saws a fifth apart, steady rather than seasick, with a deep sub-heavy floor. Low notes open up and ring out big; high notes close down and go dull, so the
weight lives at the bottom of the keyboard. It is dry and desolate, and it hangs on after you let go. This is the chapter anchor.

## 3. Gear inspirations (docs only, "inspired by")

- **Yamaha CS-80** — cold, epic, slow weight: *fat, sub-heavy, desolate*.
- **Moog Taurus** — the floor under everything: *deep, floor-shaking*.
- **Memorymoog** — the thick, dark body: *thick, dark*.
- **Sequential Prophet-5** — two saws a fifth apart: *fat, warm*.

Closest to: **a CS-80 played low and cold**.

## 4. How to play it

- **Register:** low. Roots and fifths around A1 to A2 are where it opens up. The key tracking is almost off, so low notes get more harmonics than high ones (measured: about 8 partials under the
  centre of the sound on A1, about 3 on A3). Played high it is dark and dull; that is the design.
- **Chords:** every note is two voices (a DUAL pair), so polyphony must be at least twice the notes you play. It ships at **POLY 6**: a three-note chord plays in full, a fourth note steals a voice.
- **Touch and gate:** it is a held-note patch. The release is long (about 1.3 s to silence after a held note, measured), so quick chopped notes will overlap; this was not auditioned on a fast riff by ear.
- **The spring (DRAIN):** it ships dry. Turn DRAIN up and the spring is clearly audible on it (measured: the return is about 5 dB under the dry sound at DRAIN 60, and almost all of it is harmonics
  above 150 Hz): the weight stays dry and a cloud rings above it. Whether that is frozen or muddy is a matter of taste (untested by ear).
- **Tape (CHEW):** an optional garnish for a dying-tape feel (hiss, wow, the odd dropout). It is **not** in the patch, and it costs noticeably more CPU than the rest (the variant with CHEW measured 2371
  host instr/sample against 1594 without). At the setting tried it gave about one dropout in a ten-second hold.
- **Tricks that suit it:** untested on this patch: the SLOBBER slop ride, Tape Stop (FLOP held) and the kill switch (HEEL). GROWL, ALLEY: 0 and untested.

## 5. Final values (for debugging, not for players)

`MODE DUAL, DETUNE 30 (pair 5.5 cents apart), POLY 6, SPREAD 110, VINTAGE 40, OSC1 SAW 110, OSC2 SAW +7st LVL 100, CUTOFF 66, RESO 12, ENV AMT 84, KEY TRK 12, FILTER LP24, FILTER ENV A62 D90 S70 R85, AMP ENV A60 S127 R92, VOLUME 93 (-17.9 dBFS RMS on the steady A1 hold; phrase (b) -17.1); GROWL/ALLEY/DRAIN/CHEW 0, no LFO, no arp` — `PF_TITANIC` in `firmware/src/obv_patches.h`.
