# 06 · zzuFuzz · Chapter I Wasteland

*Voiced 5 Nov 2026, approved as rendered (variant C of Batch 3A). Renders: `reference-renders/06-zzufuzz_C_*.wav` (C is this patch). Log: `../06-zzufuzz.md`.*

## 2. What it sounds like

The fuzz weapon: a huge, thick wall. Two fat saws on every voice are pushed hard into the drive until the sound is flat and relentless, and it simply does not die while you hold the key. The strike is quick and snappy, the filter and its resonance are wide open, and when you let go there is a short tail rather than a ring. It is completely dry: no echo, no spring, nothing springy or boingy. A power chord stays whole.

## 3. Gear inspirations (docs only, "inspired by")

- **Death by Audio Fuzz War** — **the benchmark**, a huge fuzz beast: *fuzzy, thick wall*.
- **Electro-Harmonix Big Muff** — the wall: *fuzzy, thick wall*.
- **Fuzz Face** — the fuzz: *fuzzy, spitting*.
- **Univox Super-Fuzz** — *voltage-starved, spitting*.
- **Korg Mono/Poly** — as the source: *fat, drifting*.
- **Realistic Concertmate MG-1** — *voltage-starved, lo-fi*.

Closest to: **a Mono/Poly into a Big Muff**.

Nothing here says the patch matches the benchmark: it was built toward it from the descriptions, by measurement, and approved by ear. The "voltage-starved" gating and sputter of the Super-Fuzz and the MG-1 is not claimed: nothing in this patch gates (BIAS only raises the peaks).

## 4. How to play it

- **Register and touch:** it was voiced on a held A2 (3 s), a held power chord (A2, E3, A3, 1.5 s), 300 ms power-chord stabs and a low A1. Other registers are untested.
- **The wall, measured:** the held note's peak-to-RMS ratio is 1.7 dB (a square wave is 0, a sine 3), and the level over a 3 s hold falls by 0.0 dB, first half second to last. The held power chord is at 3.2 dB. The source is POLY with 6 voices, so a three-note chord plays whole; the number of notes it keeps before stealing is the 6 voices.
- **The strike:** AMP ATTACK is 2.4 ms in the engine's time table; measured on a high probe note, the voice alone rises from 10 to 90 % in 2.0 ms (and the fuzzed note in 1.0 ms), with the level -0.3 dB at 2 ms against its plateau when struck from silence. It is not a zero attack. The strike is only +0.3 dB over the plateau: the fuzz flattens the dynamics, so the "punch" is in the quick rise, not in a level spike; more punch means less GROWL.
- **The tail:** 60 dB down 278 ms after a 3 s note and 314 ms after the held chord.
- **The filter:** wide open, with RESO 80. The filter does not sing by itself until about RESO 124 on this patch (measured: linear to 115, still linear at 120, singing at 124 and above), so there is room above 80 but not above about 120.
- **Reads about 2 dB hot on the chord phrase:** it was matched to the bank reference (-18.1 dBFS RMS) on its own wall phrase of held notes and chords; on phrase (b), the bank's stab phrase, it reads -16.1 dBFS, about 2 dB hotter, because the three-note chords hit the clip harder and the signal is heavily compressed (RMS and peak sit 5 dB apart). It will sound louder than the same RMS on a dynamic patch; VOLUME is the lever.
- **VOLUME changes how a note from silence starts.** GROWL's loudness trim reads the output stage, so the level of the first moments depends on VOLUME; set VOLUME first, then judge the strike.
- **It is POLY, not MONO or UNISON**, so every key re-fires the envelopes. Legato does not matter here.
- **Costs, honestly:** the GROWL at 104 costs about +595 host instr/sample whenever it is on; the worst case for the patch is about 1414 host instr/sample (the original: 317). The device build was not run; the render time on the device is not measured.
- **Tricks:** untested on this patch: the SLOBBER slop ride, SEQ held (Tape Stop), the kill switch (HEEL), CHEW, ALLEY and DRAIN (all at 0 on purpose: dry is the brief). A version with a lower GROWL and one with four saws a note (DUAL) were rendered; the DUAL costs about 1964 host instr/sample.

## 5. Final values (for debugging, not for players)

`MODE POLY (POLY 6), OSC1 SAW LVL 118, OSC2 SAW 0 st LVL 118 FINE +12 (9.4 cents), CUTOFF 88, RESO 80, ENV AMT 120, KEY TRK 64, FILTER LP24 DRIVE 100, FILTER ENV A2 D58 S40 R40, AMP ENV A20 D75 S127 R70, VINTAGE 60, SPREAD 70, GROWL 104 BIAS 72 TONE 64, VOLUME 77 (-18.1 dBFS RMS on the wall phrase, peak -12.8; phrase (b) -16.1); ALLEY 0, DRAIN 0, CHEW 0, no LFO, no arp` — `PF_ZZUFUZZ` in `firmware/src/obv_patches.h`.
