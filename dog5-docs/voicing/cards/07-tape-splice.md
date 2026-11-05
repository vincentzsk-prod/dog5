# 07 · Tape Splice · Chapter I Wasteland

*Voiced 5 Nov 2026, approved as rendered (variant B of Batch 3B). Renders: `reference-renders/07-tape-splice_B_*.wav` (B is this patch). Log: `../07-tape-splice.md`.*

## 2. What it sounds like

A fat square with a wobble in its pitch, chopped short. Two square waves a hair apart, one frequency-modulating the other so the tone carries extra energy below the note, and a random pitch wobble (9.6 cents standard deviation on the held A2, the LFO depth up to ±19 cents). Notes stop quickly when you let go, and a tape stage on the end delays every note by a couple of milliseconds. It is dry: no echo, no spring.

## 3. Gear inspirations (docs only, "inspired by")

- **Korg Mono/Poly** — the source: *fat, drifting*.
- **Sequential Prophet-5** — *wobble, nervous*.
- **Roland RE-201 Space Echo** — the tape stage: *wobble, lo-fi*.
- **Roland SH-101** — *punchy*.

Closest to: **a Mono/Poly cross-mod square through a worn tape echo**.

Nothing here says the patch matches these: it was built toward the descriptions, by measurement, and approved by ear.

## 4. How to play it

- **Register:** it was voiced on a held A2 (2.4 s), twelve 60 ms staccato notes from A2 up to G3, and three 80 ms A3 notes; other registers are untested.
- **It is MONO, so legato does not re-fire the envelopes:** a key held while the next goes down slides to the new note and the envelopes do not restart. Play it detached. A chord plays one note (the last).
- **Where the wobble comes from:** the random pitch LFO (5.7 Hz, a new target about every 176 ms, up to ±19 cents). Measured on the held A2 the pitch track has a standard deviation of 9.6 cents (28 cents from 5th to 95th percentile); without the tape (CHEW 0) it is 8.9.
- **What X-MOD does:** it adds sidebands and energy below the note, and it does not move the measured pitch. On the held A2 the share of energy under 60 Hz is 2 % at X-MOD 70 (0 % at 0 and 40, 10 % at 100, 18 % at 127); the cause of that low-end energy was not isolated (it suggests FM sidebands). The pitch track's spread showed no order across X-MOD 0 to 127.
- **The tape's timing:** CHEW 80 delays a note's start by about +2.4 ms on average, with a spread of 0.59 ms between notes (+1.2 to +3.2 ms over twelve notes), and the end of a note by +3.0 ms ± 1.6.
- **Dropouts:** none measured on the held A2 at CHEW 80 (no dip of 6 dB or more; the deepest was 5 dB over 2.1 s). A separate 12-second hold counted dips of 6 dB or more: 0 at CHEW 0, 4 at CHEW 30 and 60 (deepest 6 dB), 8 at CHEW 100 (deepest 11 dB) and 15 at CHEW 127 (deepest 20 dB); the 4 dips at CHEW 60 also appeared with DROPS 0, so they were not isolated as dropouts.
- **Chopped:** a 60 ms note is 40 dB down 14 ms after the key goes up and 60 dB down at 18 ms; after the 2.4 s held note it is 60 dB down at 36 ms.
- **Level:** matched to the bank reference on the splice phrase (−18.1 dBFS RMS, peak −12.9); phrase (b) reads −17.6 with a peak of −12.5.
- **Costs, honestly:** about 2177 host instr/sample worst case (the original: 1384); CHEW accounts for about 770 of it. The device build was not run and the render time on the device is not measured.
- **Tricks:** untested on this patch: the SLOBBER slop ride, SEQ held (Tape Stop), the kill switch (HEEL), GROWL, ALLEY, DRAIN, ENV>O2. OSC 2 LEVEL 0 still modulates through X-MOD (measured on this patch's held A2: the render with X-MOD 100 differs from X-MOD 0 by 3.1 dB re the signal); how that sounds is untested.

## 5. Final values (for debugging, not for players)

`MODE MONO, GLIDE 0, OSC1 PULSE PW 64 LVL 110, OSC2 PULSE PW 64 SEMI 0 FINE 68 (+3.1 cents) LVL 100, X-MOD 70, CUTOFF 60, RESO 20, ENV AMT 114, KEY TRK 64, FILTER LP24 DRIVE 40, FILTER ENV A20 D60 S60 R60, AMP ENV A2 D70 S100 R25, LFO RANDOM RATE 94 (5.7 Hz) PHASE FREE PITCH 16 (±19 cents) PITCH> BOTH, VINTAGE 30, SPREAD 60, VOLUME 104 (−18.1 dBFS RMS on the splice phrase, peak −12.9), CHEW 80 WOW/FLT 64 HISS 0 DROPS 90; DLY MIX 0, DRAIN 0, ALLEY 0, GROWL 0, no arp` — `PF_TAPE_SPLICE` in `firmware/src/obv_patches.h`.
