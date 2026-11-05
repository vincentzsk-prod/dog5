# 02 · Cement Grind · Chapter I Wasteland

*Voiced 5 Nov 2026, approved as rendered (variant D of Batch 3A). Renders: `reference-renders/02-cement-grind_D_*.wav` (D is this patch). Log: `../02-cement-grind.md`.*

## 2. What it sounds like

A low-mid grinder built from two fat pulse waves whose widths sweep quickly, so every note shudders and churns on purpose: a clear, fast pulse-width wobble you can hear on the riff, not a shimmer. The filter bites, it is pushed into a moderate crunch, and each note starts with a little skid and a snap. It is thick and dry, and it hits hard.

## 3. Gear inspirations (docs only, "inspired by")

- **Roland Juno-60** — the pulse-width movement: *PWM, wobble, thick*.
- **Korg Polysix** — the stacked pulses: *fat, PWM*.
- **Roland SH-101** — the punchy PWM bass: *PWM bass, punchy*.
- **ProCo RAT** — the crunch: *crunchy*.
- **Korg MS-20** — the filter: *biting*.

Closest to: **a Juno-60 PWM bass through a RAT**.

## 4. How to play it

- **Register and gate:** it was voiced on a riff of A2 (110 Hz) up to E3 with G2, in notes of about 400 ms (long enough for the PWM to swing two or three times inside each note) and on a held A2, plus a few 150 ms chops. Other registers are untested.
- **The PWM, measured:** the sweep runs at about 11.5 Hz. On a held A2 it moves the 150 to 400 Hz band by 11.9 dB from the top of its swing to the bottom, the 400 to 1,200 Hz band by 6.7 dB, the upper bands by 5 dB, and the overall level by 4.1 dB; on the riff's 400 ms notes the same band moves 8.0 dB and the level 2.9 dB. Each detached note restarts the sweep from the same place.
- **One LFO does both jobs.** The pulse-width sweep and the filter wobble share the single LFO and run at the same rate; the slow, half-cycle-a-second filter wobble the original patch had is gone. There is no way to slow one without the other.
- **A PWM sweep that crosses 50 % doubles its rate** (a pulse and its mirror width sound alike). Here the widths run from about 18 to 55 %, so it crosses 50 % by a few points at the top of each swing; the measured rate still matches the LFO's, so it is not doubling. Do not push the PWM depth much further.
- **It is MONO, so legato does not re-fire the envelopes:** a key held while the next goes down glides to it (the GLIDE is set for the skid) without a new snap. Play it detached. A chord plays one note.
- **Thickness:** the two pulses sit about 8 cents apart (a beat of about half a hertz at A2); the sound is dense and heavily driven, and its peak-to-RMS ratio is 3.2 dB.
- **Costs, honestly:** about 298 host instr/sample in the worst case (the original: 309); no GROWL. The device build was not run.
- **Tricks:** untested on this patch: the SLOBBER slop ride, SEQ held (Tape Stop), the kill switch (HEEL), GROWL, any effect. Two other versions were rendered, one at 7.7 Hz without the filter wobble and a slower, deeper one with a wider pair; nothing else was tried.
- **Level:** matched to the bank reference on the grind riff (-17.9 dBFS RMS, peak -14.6; the chord phrase reads -18.0, where a chord plays only its last note). The sound stops at once: 60 dB down 26 ms after the key goes up.

## 5. Final values (for debugging, not for players)

`MODE MONO, OSC1 PULSE PW 46 (36 %) LVL 110, OSC2 PULSE PW 46 0 st LVL 104 FINE +10 (7.8 cents), CUTOFF 60, RESO 62, ENV AMT 96, KEY TRK 64, FILTER LP12 DRIVE 78, FILTER ENV A0 D58 S45 R40, AMP ENV A1 D70 S127 R20, LFO TRI RATE 108 (11.5 Hz) PHASE SYNC, LFO PWM 110 (both oscillators, +-18 points) FILTER 28, GLIDE 12, VINTAGE 30, VOLUME 87 (-17.9 dBFS RMS on the grind riff, peak -14.6); no GROWL, no effects, no arp` — `PF_CEMENT_GRIND` in `firmware/src/obv_patches.h`.
