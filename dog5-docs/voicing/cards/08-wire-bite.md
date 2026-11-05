# 08 · Wire Bite · Chapter I Wasteland

*Voiced 5 Nov 2026, approved as rendered (variant D of Batch 3A). Renders: `reference-renders/08-wire-bite_D_*.wav` (D is this patch). Log: `../08-wire-bite.md`.*

## 2. What it sounds like

An anxious, thick drone that bites, like touching a live wire. Six stacked pulse waves in the high register, with a second layer an octave and a fifth above, run through a resonant filter that zaps at the start of every note. It is fat and bright, medium-to-high, and it never sits still: the voices wander on their own and the whole stack leans and jitters in pitch. It is dry and each note is chopped off the moment you let go.

## 3. Gear inspirations (docs only, "inspired by")

- **Korg Mono/Poly (in unison)** — the stack: *fat, drifting*.
- **Minimoog** — *thick*.
- **Korg MS-20** — the bite: *the bite*.
- **Roland Jupiter-4** — *fat, wobble*.
- **Sequential Prophet-5 (early revisions)** — the unsteadiness: *drift*.

Closest to: **a Mono/Poly in unison with MS-20 bite**.

## 4. How to play it

- **Register:** high. It was voiced on a held A4 (3.5 s), eight 110 ms bites (E5, A4, C5, D5) and a held A3, plus the pilot phrases; low notes and other registers are untested.
- **It is a UNISON of 6 voices on one note, so legato does not re-fire the envelopes:** a key held while the next goes down slides to it and the zap does not happen again. Play it detached for the bite. Chords play one note (the last).
- **Chopped:** a bite is 40 dB down 18 ms after the key goes up, and a held note is 60 dB down at 26 ms. No echo, no spring.
- **The drift, measured by the engine's own log over the held A4:** the six voices sit at static offsets from -9.3 to +7.2 cents from each other's centre and each wanders by 3.8 to 5.7 cents (s.d.), over ranges of up to about -22 to +26 cents; on top of that a smooth-random pitch LFO leans the stack by up to 19 cents at about 0.28 Hz (a new target about every 3.6 s), each voice at a different point of it. The audio alone cannot show this: the stack's own beating moves its measured pitch by more than the wander does. The SLOBBER slop ride (up to 254 on top of VINTAGE 127) is untested on this patch.
- **The zap, stated honestly:** the measured top-end burst (energy above 1.2 kHz in the first 40 ms against the body) is -2.0 dB on the held A4 and +0.5 dB on a bite: the bright body (centroid 3855 Hz on the wire phrase, 71 % of its energy above 1.2 kHz) reduces the measured burst. The darker version rendered alongside measured +4.6 dB. This one was approved by ear, as rendered; the burst number is a diagnostic here, not a promise of a big zap.
- **Level and attack:** matched to the bank reference on the wire phrase (-17.9 dBFS RMS, peak -8.9; the chord phrase reads -18.2). The original sat 4 dB over the reference with a peak of -2.2 dBFS at VOLUME 100. Struck from silence on a high probe note, the stack rises from 10 to 90 % of its plateau in about 11 ms; with one or two voices the same patch reads 1.2 to 1.5 ms, so this is the six voices beating, not the envelope.
- **Costs, honestly:** about 1298 host instr/sample in the worst case (the original: 1985, with its effects); no GROWL. The device build was not run.
- **Tricks:** untested on this patch: SEQ held (Tape Stop), the kill switch (HEEL), GROWL, any effect. The original's echo and spring are deliberately off (to keep the chop); turning DRAIN up is untested and would blur it.

## 5. Final values (for debugging, not for players)

`MODE UNISON, VOICES 6, DETUNE 50 (+-15 cents), OSC1 PULSE PW 18 (14 %) LVL 108, OSC2 PULSE PW 50 +19 st FINE 67 (+2.3 cents) LVL 100, CUTOFF 90, RESO 66, ENV AMT 124, KEY TRK 70, FILTER LP12 DRIVE 40, FILTER ENV A0 D40 S20 R30, AMP ENV A2 D70 S127 R14, LFO RANDOM RATE 34 (0.28 Hz) PHASE SPREAD PITCH 16 (+-19 cents), VINTAGE 127, SPREAD 100, VOLUME 58 (-17.9 dBFS RMS on the wire phrase, peak -8.9); DLY MIX 0, DRAIN 0, GLIDE 0, no arp` — `PF_WIRE_BITE` in `firmware/src/obv_patches.h`.
