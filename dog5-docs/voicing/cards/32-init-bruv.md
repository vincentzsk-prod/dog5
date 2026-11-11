# 32 · Init bruv? · Chapter IV · The Ancient Relics

*Voiced 11 Nov 2026 (Batch 6B), approved after listening: variant B (Vincent: "option B"). He chose it by ear over the MONO variant C and the raw-saw calibration render Craw. Renders: `reference-renders/32-init-bruv_B_*.wav`. Tables (on the voicing branch): `listen/voicing/batch-06b/32/README.md`.*

## 2. What it sounds like

A plain voice made of two saw waves played through a low-pass filter with a short envelope, dry, with chords and single notes both playable. Nothing is added to it: no modulation, no echo, no spring, no tape and no drive.

## 3. Gear inspirations (docs only, "inspired by")

- **Sequential Prophet-5** — *a plain saw, the filter open.* Not carried. The filter is not open: it is a 24 dB low-pass at CUTOFF 80 with RESO 20, and there are two saws, not one.
- **Minimoog** — *one raw oscillator.* Not carried: OSC 2 is on (a saw, LEVEL 100, 4.7 cents from OSC 1).
- **Roland SH-101** — *a saw, the filter open.* Not carried for the same two reasons.

What was measured: through the filter, the harmonics of C3 are −7.9 / −14.3 / −18.0 dB for the 2nd / 3rd / 4th (a plain saw is −6.0 / −9.5 / −12.0), and the 10th harmonic sits 6.8 dB under the 1/n law at C3 and 15.8 dB under it at C5. So B is two detuned saws through a closed-ish filter, not a plain saw. The strike centroid is 620 Hz at C3 and 1618 Hz at C5.

Closest to: **an analog two-saw init patch**. "Raw" and "blank" are Vincent's words and are not measured. Nothing here says the patch matches the instruments above: it carries none of them literally.

## 4. How to play it

- **What it is:** the engine's own default program, with one change, VOLUME 97 (the default is 100). It is not the single raw saw with an open filter and flat envelopes that the brief described: POLY 5, two saws 4.7 cents apart (OSC 2 FINE 70), a 24 dB low-pass at CUTOFF 80 with RESO 20 and KEY TRK 64, the filter envelope (ENV AMT 90, attack 20, decay 70, sustain 40, release 60), the amp envelope (attack 10, decay 70, sustain 100, release 60), VINTAGE 30, SPREAD 60, every effect at 0. **Slots 33–99 hold the same defaults as INIT, with VOLUME 100.**
- **Chords:** POLY 5 plays chords. Levels over the note-on region: −18.05 dBFS on the stabs phrase, −22.9 dB on the low chopped riff, −17.7 dB on the held chord (A2 E3 A3); the peak is −5.6 dBFS over every phrase tried. K-weighted level on the stabs −18.5 dB.
- **Note-on:** no click: on a held C3 the first 2 ms peak at −19.0 dBFS, 5.9 dB under the note's own peak (−13.1 dBFS); the amp attack is 10.
- **Effects at 0 are bypassed:** with GROWL, DLY MIX, DRAIN and CHEW at 0, the audio was bit-identical on the stabs, the riff and the held note when every other effect control was moved to its extreme: echo time, feedback, tone, pingpong and fine; spring size, damp and pre-delay; tape wow/flutter, hiss and dropouts; GROWL bias and tone. (Measured on B; it held on all three phrases.)
- **Cost:** CPU 1814 host instr/sample worst case (idle 1164, load 650), the same as the original and the 8th lightest of the 32 on that yardstick (slots 5, 2, 11, 27, 4, 9 and 25 are lighter, from 1337). The MONO variant C read 1359; it was not chosen. The device render time is not measured.
- **Changed from the brief:** the brief called for "single raw saw, open filter, flat envelopes, no effects"; Vincent chose the engine's defaults. **The raw single-saw render** (Craw: OSC 2 off, CUTOFF 127, RESO 0, ENV AMT 64, attack 0, sustain 127, release 30) stays on the listen branch: its harmonics follow 1/n within 0.25 dB up to the 10th at C3, level −17.98 dBFS on the stabs phrase, CPU 1792; it is a v1.1 candidate for a further blank canvas, as is a MONO init. The original brief is kept in `DOG-5-presets.md`.
- **Tricks:** SLOBBER, SEQ held (Tape Stop), the kill switch (HEEL): untested on this patch.

## 5. Final values (for debugging, not for players)

`every parameter at the engine default except VOLUME: MODE POLY (POLY 5), OSC1 SAW LEVEL 110, OSC2 SAW LEVEL 100 SEMI 0 FINE 70, FILTER LP24 CUTOFF 80 RESO 20 KEY TRK 64 ENV AMT 90, FILTER ENV A20 D70 S40 R60, AMP ENV A10 D70 S100 R60, LFO TRI RATE 70 (all depths 0, PHASE FREE), VINTAGE 30, SPREAD 60, GLIDE 0, GROWL / DLY MIX / DRAIN / CHEW 0, VOLUME 97` — `PF_INIT_BRUV = {P_VOLUME, 97}` in `firmware/src/obv_patches.h` (`PF_INIT` stays the empty array of slots 33–99).
