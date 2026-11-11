# 32 Init bruv?, Batch 6B round 1 (rendered, not yet heard)

A = the original array (it IS the engine defaults); B = the engine defaults with VOLUME on the reference (POLY 5, the default mode); C = the same in MONO; Craw = a calibration render of the brief's WORDS (one raw saw, filter fully open, flat envelopes): **the engine's defaults are not that** (below). Level phrase: the stabs (b); second phrase the riff (a). Peak limit -4 dBFS over b, a, the held note and the chord.

| var | tag | VOLUME | stabs (b) | riff (a) | chord (A2 E3 A3, 8 s) | peak | CPU | what |
|---|---|---|---|---|---|---|---|---|
| A | original | 100 | -17.54 | -22.4 | -17.1 | -5.1 | 1814 | the original array (the engine defaults), VOLUME 100 |
| B | defaults-poly | 97 | -18.05 | -22.9 | -17.7 | -5.6 | 1814 | the engine's own defaults, POLY 5 (the default mode), VOLUME on the reference |
| C | defaults-mono | 120 | -18.09 | -17.3 | -18.8 | -8.9 | 1359 | the same in MONO |
| Craw | plain-saw | 99 | -17.98 | -22.1 | -17.3 | -7.3 | 1792 | calibration: the brief's WORDS: one raw saw (OSC 2 off), the filter fully open (CUTOFF 127, RESO 0, no envelope amount), flat envelopes (attack 0, sustain full, release 30), POLY 5 |

**Every change over the original array:** B ; VOLUME 100 -> 97; C MODE POLY -> MONO; VOLUME 100 -> 120; Craw O2_LVL 100 -> 0 (-79%); CUTOFF 80 -> 127 (+37%); RESO 20 -> 0 (-16%); FENV_AMT 90 -> 64 (-20%); AA 10 -> 0 (-8%); AS 100 -> 127 (+21%); AR 60 -> 30 (-24%); VOLUME 100 -> 99

**The engine's defaults (what slot 32 is):** POLY (POLY 5); OSC 1 a saw LEVEL 110; **OSC 2 ON** (a saw, LEVEL 100, SEMI 0, FINE 70 = +4.7 cents); LP24 **CUTOFF 80, RESO 20** (not open), ENV AMT 90 (bipolar, 64 = 0), KEY TRK 64, FILTER ENV A20 D70 S40 R60, AMP ENV A10 D70 S100 R60, LFO TRI RATE 70 with every depth 0 and PHASE FREE, VINTAGE 30, SPREAD 60, GLIDE 0, VOLUME 100, every effect 0 (GROWL, DLY MIX, DRAIN, CHEW), no arp. The original slot 32 array is `{X}` (empty: every parameter at its default): **no difference** between it and the default program; `PF_INIT` is also `FACT_INIT`, the INIT of slots 33-99.

## Harmonics of one held note (dB re the first; deviation from the saw's 1/n law in brackets: a plain saw reads 0 everywhere)

* A C3: 1: 0.0 (+0.0), 2: -7.9 (-1.9), 3: -14.3 (-4.7), 4: -18.0 (-6.0), 5: -19.7 (-5.7), 6: -21.0 (-5.5), 7: -22.5 (-5.6), 8: -24.0 (-5.9), 9: -25.3 (-6.3), 10: -26.8 (-6.8)
* A C5: 1: 0.0 (+0.0), 2: -8.4 (-2.4), 3: -12.2 (-2.7), 4: -15.9 (-3.9), 5: -18.8 (-4.8), 6: -21.8 (-6.2), 7: -25.1 (-8.2), 8: -28.5 (-10.4), 9: -31.9 (-12.8), 10: -35.8 (-15.8)
* B C3: 1: 0.0 (+0.0), 2: -7.9 (-1.8), 3: -14.3 (-4.7), 4: -18.0 (-6.0), 5: -19.7 (-5.7), 6: -21.0 (-5.5), 7: -22.5 (-5.6), 8: -24.0 (-5.9), 9: -25.3 (-6.3), 10: -26.8 (-6.8)
* B C5: 1: 0.0 (+0.0), 2: -8.4 (-2.4), 3: -12.2 (-2.7), 4: -15.9 (-3.9), 5: -18.8 (-4.8), 6: -21.8 (-6.2), 7: -25.1 (-8.2), 8: -28.5 (-10.4), 9: -31.9 (-12.8), 10: -35.8 (-15.8)
* C C3: 1: 0.0 (+0.0), 2: -7.9 (-1.9), 3: -14.3 (-4.8), 4: -18.1 (-6.0), 5: -19.7 (-5.7), 6: -21.1 (-5.5), 7: -22.6 (-5.7), 8: -24.0 (-6.0), 9: -25.4 (-6.3), 10: -26.8 (-6.8)
* C C5: 1: 0.0 (+0.0), 2: -8.4 (-2.4), 3: -12.2 (-2.7), 4: -15.9 (-3.9), 5: -18.8 (-4.8), 6: -21.8 (-6.3), 7: -25.1 (-8.2), 8: -28.5 (-10.4), 9: -31.8 (-12.7), 10: -35.7 (-15.7)
* Craw C3: 1: 0.0 (+0.0), 2: -6.1 (-0.1), 3: -9.5 (+0.0), 4: -12.1 (-0.0), 5: -14.1 (-0.1), 6: -15.6 (-0.0), 7: -17.0 (-0.1), 8: -18.3 (-0.2), 9: -19.2 (-0.1), 10: -20.2 (-0.2)
* Craw C5: 1: 0.0 (+0.0), 2: -6.2 (-0.2), 3: -9.8 (-0.2), 4: -12.4 (-0.4), 5: -14.7 (-0.7), 6: -16.6 (-1.1), 7: -18.2 (-1.3), 8: -19.8 (-1.7), 9: -21.2 (-2.2), 10: -22.7 (-2.7)

## Bypass proof: the effect chain at 0 renders the same samples with every effect's other controls at extremes (echo time / feedback / tone / pingpong / fine, spring size / damp / pre-delay, tape wow / hiss / drops, GROWL bias / tone), B: b_stabs bit-identical, a_riff bit-identical, c_held bit-identical

## The note-on (C3, the peak of the first 2 ms after the first sample against the note's own peak, dBFS)

* A: first 2 ms -18.4, the note -12.6 (5.9 dB under the note: no click)
* B: first 2 ms -19.0, the note -13.1 (5.9 dB under the note: no click)
* C: first 2 ms -16.9, the note -11.1 (5.8 dB under the note: no click)
* Craw: first 2 ms -20.3, the note -14.4 (5.9 dB under the note: no click)

## CPU (host instr/sample, worst case) of the whole bank on the same yardstick (slot: cost), lightest first

5: 1337, 2: 1359, 11: 1366, 27: 1379, 4: 1588, 9: 1747, 25: 1809, 32: 1814, 28: 1855, 14: 1857

Strike centroid (C3 / C5, Hz): A 620 / 1617; B 620 / 1618; C 620 / 1613; Craw 2592 / 4298
