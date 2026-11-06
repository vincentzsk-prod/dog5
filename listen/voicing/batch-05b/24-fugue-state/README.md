# 24 Fugue State: Batch 5B round 1 (rendered, not yet heard)

| var | tag | VOLUME | level | K-RMS | (b) RMS | peak (all phrases) | clip | CPU worst (idle+load) |
|---|---|---|---|---|---|---|---|---|
| A | original | 100 | -13.58 | -13.73 | -11.64 | 0.00 | 2890 | 2152 |
| A* | original-matched | 65 | -17.93 | n/a | n/a | -4.04 | n/a | n/a |
| B | lurch | 85 | -17.95 | -18.02 | -22.02 | -4.88 | 0 | 2039 |
| C | wobble | 85 | -17.91 | -17.97 | -22.46 | -4.90 | 0 | 2038 |
| D | seasick | 84 | -17.98 | -18.06 | -22.75 | -4.99 | 0 | 2039 |

Level = RMS over +4 s .. +10 s of the held A3 C#4 E4 triad (phrase z_chord), reference -18.0 dBFS +-1.5; peak limit -4 dBFS over z_chord, z_tap, a_riff, b_stabs, ad_longhold, ae_repeat.

## Parameter changes against the original (A)

**B lurch** (slow lurch: LFO 0.31 Hz, +-4.7 st (PITCH 80), FEEDBK 100, echo 266 ms)

* O1_PW 50 -> 32 (-14%)
* O2_WAVE SAW+PLS -> PULSE
* O2_PW 80 -> 32 (-38%)
* O2_LVL 100 -> 45 (-43%)
* O2_SEMI +0 -> +12 st
* O2_FINE 74 -> 66 (centre 64: +10 -> +2, -6% of range) (+7.8 cents -> +1.6 cents)
* CUTOFF 52 -> 63 (+9%) (262 Hz -> 494 Hz)
* RESO 12 -> 5 (-6%)
* FENV_AMT 80 -> 64 (centre 64: +16 -> +0, -13% of range)
* KEYTRK 64 -> 127 (+50%)
* FTYPE LP24 -> LP12
* AD 70 -> 100 (+24%) (117 ms -> 1218 ms)
* AS 100 -> 127 (+21%)
* LFO_RATE 42 -> 36 (-5%) (0.4 Hz -> 0.3 Hz)
* LFO_PITCH 4 -> 80 (+60%)
* LFO_PWM 45 -> 0 (-35%)
* DLY_FB 40 -> 100 (+47%)
* DLY_TONE 30 -> 45 (+12%)
* DLY_MIX 35 -> 85 (+39%)
* REV_SIZE 118 -> 100 (-14%)
* REV_PRE 50 -> 30 (-16%)
* REV_MIX 70 -> 45 (-20%)
* ALLEY 0 -> 97 (+76%) (SYNC -> 266 ms)

**C wobble** (fast wobble: LFO 4.9 Hz, +-1.8 st (PITCH 50), FEEDBK 95, echo 144 ms)

* O1_PW 50 -> 32 (-14%)
* O2_WAVE SAW+PLS -> PULSE
* O2_PW 80 -> 32 (-38%)
* O2_LVL 100 -> 45 (-43%)
* O2_SEMI +0 -> +12 st
* O2_FINE 74 -> 66 (centre 64: +10 -> +2, -6% of range) (+7.8 cents -> +1.6 cents)
* CUTOFF 52 -> 63 (+9%) (262 Hz -> 494 Hz)
* RESO 12 -> 5 (-6%)
* FENV_AMT 80 -> 64 (centre 64: +16 -> +0, -13% of range)
* KEYTRK 64 -> 127 (+50%)
* FTYPE LP24 -> LP12
* AD 70 -> 100 (+24%) (117 ms -> 1218 ms)
* AS 100 -> 127 (+21%)
* LFO_RATE 42 -> 91 (+39%) (0.4 Hz -> 4.9 Hz)
* LFO_PITCH 4 -> 50 (+36%)
* LFO_PWM 45 -> 0 (-35%)
* DLY_FB 40 -> 95 (+43%)
* DLY_TONE 30 -> 45 (+12%)
* DLY_MIX 35 -> 85 (+39%)
* REV_SIZE 118 -> 100 (-14%)
* REV_PRE 50 -> 30 (-16%)
* REV_MIX 70 -> 45 (-20%)
* ALLEY 0 -> 79 (+62%) (SYNC -> 144 ms)

**D seasick** (middle rate and the deepest: LFO 1.1 Hz, +-7.3 st (PITCH 100), FEEDBK 110, echo 266 ms)

* O1_PW 50 -> 32 (-14%)
* O2_WAVE SAW+PLS -> PULSE
* O2_PW 80 -> 32 (-38%)
* O2_LVL 100 -> 45 (-43%)
* O2_SEMI +0 -> +12 st
* O2_FINE 74 -> 66 (centre 64: +10 -> +2, -6% of range) (+7.8 cents -> +1.6 cents)
* CUTOFF 52 -> 63 (+9%) (262 Hz -> 494 Hz)
* RESO 12 -> 5 (-6%)
* FENV_AMT 80 -> 64 (centre 64: +16 -> +0, -13% of range)
* KEYTRK 64 -> 127 (+50%)
* FTYPE LP24 -> LP12
* AD 70 -> 100 (+24%) (117 ms -> 1218 ms)
* AS 100 -> 127 (+21%)
* LFO_RATE 42 -> 62 (+16%) (0.4 Hz -> 1.1 Hz)
* LFO_PITCH 4 -> 100 (+76%)
* LFO_PWM 45 -> 0 (-35%)
* DLY_FB 40 -> 110 (+55%)
* DLY_TONE 30 -> 45 (+12%)
* DLY_MIX 35 -> 85 (+39%)
* REV_SIZE 118 -> 100 (-14%)
* REV_PRE 50 -> 30 (-16%)
* REV_MIX 70 -> 45 (-20%)
* ALLEY 0 -> 97 (+76%) (SYNC -> 266 ms)

## Tone in windows (held triad)

| var | window | RMS dB | centroid Hz | MUD | <150 | 150-400 | 400-1.2k | 1.2k+ |
|---|---|---|---|---|---|---|---|---|
| A | 0-1s | -12.6 | 447 | 532 | 0 | 89 | 11 | 0.2 |
| A | 1-2s | -13.0 | 373 | 7773 | 1 | 94 | 5 | 0.0 |
| A | 2-4s | -13.6 | 352 | 18931 | 1 | 95 | 3 | 0.0 |
| A | 4-10s | -13.6 | 349 | 17766 | 1 | 95 | 3 | 0.0 |
| A | tail 0-0.5s | -15.9 | 328 | 70607 | 3 | 96 | 1 | 0.0 |
| A | tail 0.5-1.5s | -25.7 | 366 | 95300 | 4 | 95 | 1 | 0.0 |
| A | tail 1.5-3s | -37.8 | 548 | 49254 | 7 | 93 | 0 | 0.0 |
| A | tail 3-5s | -56.7 | 1780 | 856 | 8 | 91 | 1 | 0.1 |
| B | 0-1s | -19.2 | 541 | 322 | 0 | 87 | 13 | 0.3 |
| B | 1-2s | -18.2 | 597 | 224 | 0 | 74 | 26 | 0.3 |
| B | 2-4s | -17.8 | 569 | 301 | 0 | 80 | 20 | 0.3 |
| B | 4-10s | -18.0 | 579 | 277 | 0 | 78 | 22 | 0.3 |
| B | tail 0-0.5s | -19.5 | 532 | 363 | 0 | 83 | 17 | 0.2 |
| B | tail 0.5-1.5s | -25.7 | 578 | 356 | 0 | 81 | 19 | 0.2 |
| B | tail 1.5-3s | -36.7 | 709 | 415 | 0 | 79 | 21 | 0.2 |
| B | tail 3-5s | -52.5 | 1199 | 355 | 1 | 79 | 20 | 0.2 |
| C | 0-1s | -19.2 | 586 | 307 | 0 | 83 | 16 | 0.3 |
| C | 1-2s | -17.8 | 587 | 327 | 0 | 80 | 20 | 0.2 |
| C | 2-4s | -17.9 | 588 | 325 | 0 | 81 | 19 | 0.2 |
| C | 4-10s | -17.9 | 588 | 318 | 0 | 80 | 20 | 0.3 |
| C | tail 0-0.5s | -19.7 | 579 | 326 | 0 | 82 | 18 | 0.3 |
| C | tail 0.5-1.5s | -26.5 | 620 | 364 | 0 | 82 | 18 | 0.2 |
| C | tail 1.5-3s | -38.0 | 715 | 345 | 0 | 80 | 20 | 0.2 |
| C | tail 3-5s | -56.1 | 1478 | 235 | 2 | 77 | 20 | 0.3 |
| D | 0-1s | -19.7 | 588 | 300 | 1 | 80 | 19 | 0.3 |
| D | 1-2s | -18.2 | 590 | 241 | 1 | 72 | 27 | 0.3 |
| D | 2-4s | -18.0 | 573 | 280 | 1 | 75 | 24 | 0.3 |
| D | 4-10s | -18.0 | 576 | 261 | 1 | 75 | 24 | 0.3 |
| D | tail 0-0.5s | -20.0 | 576 | 267 | 0 | 80 | 20 | 0.3 |
| D | tail 0.5-1.5s | -25.3 | 588 | 320 | 0 | 72 | 28 | 0.2 |
| D | tail 1.5-3s | -34.6 | 638 | 485 | 0 | 79 | 21 | 0.2 |
| D | tail 3-5s | -48.7 | 987 | 1041 | 1 | 86 | 13 | 0.1 |

## The pitch LFO (one voice, VINTAGE 0, no effects, LFO PHASE SYNC, A3 held 12 s)

| var | LFO PITCH | law peak cents | measured min / max cents | p5-p95 cents | measured pp semitones | rate set Hz | rate measured Hz |
|---|---|---|---|---|---|---|---|
| A | 4 | 0 | -3 / 0 | 0 .. 0 | 0.0 | 0.41 | 0.05 |
| B | 80 | 469 | -486 / 441 | -435 .. 405 | 9.3 | 0.31 | 0.31 |
| C | 50 | 178 | -150 / 150 | -147 .. 147 | 3.0 | 4.89 | 4.89 |
| D | 100 | 731 | -707 / 703 | -661 .. 652 | 14.1 | 1.14 | 1.14 |

## The echo (a triad stab of 120 ms with a fast attack and release, so the repeats stand apart), and the feedback tests

| var | ALLEY ms | FEEDBK | MIX | first repeat re note | repeats above -40 dB | above -20 dB | return -40 dB after the note (ms) | direct-vs-echo pitch gap, max cents (law) |
|---|---|---|---|---|---|---|---|---|
| A | 750 | 40 | 35 | -17.1 | 2 | 1 | 2912 | 0 |
| B | 266 | 100 | 85 | -9.8 | 10 | 4 | 3455 | 153 |
| C | 144 | 95 | 85 | -10.1 | 10 | 4 | 1721 | 212 |
| D | 266 | 110 | 85 | -9.8 | 13 | 5 | 4482 | 882 |

Long hold (triad held 30 s): peak per 2 s window (dBFS) and growth (last full window minus the second window)

| var | 0s | 4s | 8s | 12s | 16s | 20s | 24s | 28s | growth dB | release peaks 0/2/4/6 s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | -2.7 | -4.8 | -4.8 | -4.3 | -4.2 | -4.1 | -4.1 | -4.2 | -0.4 | -8 / -30 / -59 / -90 |
| B | -6.0 | -5.9 | -5.3 | -5.8 | -6.5 | -6.2 | -6.5 | -5.5 | +0.5 | -8 / -26 / -47 / -90 |
| C | -5.3 | -5.8 | -5.9 | -5.7 | -6.1 | -6.2 | -6.0 | -5.5 | +0.2 | -8 / -28 / -55 / -90 |
| D | -6.2 | -5.1 | -5.5 | -5.0 | -6.1 | -5.6 | -6.7 | -5.4 | -0.1 | -7 / -24 / -42 / -63 |

Repeated chord (triad 300 ms every 1 s, 12 times): peak of each second (dBFS), growth = best later chord minus the first

| var | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | growth dB | after: 0-2 / 2-4 / 4-6 s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | -2.8 | -2.9 | -1.0 | -3.8 | -3.9 | -4.6 | -6.2 | -1.6 | -4.0 | -3.2 | -2.0 | -2.8 | +1.2 | -11 / -37 / -64 |
| B | -8.4 | -7.1 | -7.9 | -7.2 | -6.8 | -8.7 | -8.0 | -7.8 | -8.5 | -6.9 | -9.0 | -7.2 | +1.5 | -14 / -34 / -58 |
| C | -8.7 | -7.7 | -7.5 | -7.6 | -7.7 | -7.9 | -7.3 | -8.0 | -6.7 | -5.6 | -7.5 | -5.5 | +3.3 | -14 / -32 / -67 |
| D | -9.7 | -8.6 | -9.0 | -7.4 | -7.8 | -8.7 | -8.2 | -7.9 | -6.9 | -7.3 | -7.7 | -7.3 | +2.8 | -13 / -30 / -49 |

## The triangle and the octave-up copy

Harmonics 3 / 5 / 7 of OSC 1 at rest against the fundamental (ideal triangle -19.1 / -28.0 / -34.2; square -9.5 / -14.0 / -16.9):

* B: -17.5 / -27.9 / -37.5 dB
* C: -17.5 / -27.9 / -37.5 dB
* D: -17.5 / -27.9 / -37.5 dB

The octave-up copy (OSC 2, PULSE 25 %, +12 st) puts energy on the EVEN harmonics only, so those odd-harmonic readings do not move with it. Probe on B (dry held triad, 4-10 s): OSC 2 level against shares and MUD:

| O2 LEVEL | RMS | centroid | <150 | 150-400 | 400-1.2k | 1.2k+ | MUD |
|---|---|---|---|---|---|---|---|
| 0 | -19.5 | 571 | 0 | 79 | 21 | 0.3 | 300 |
| 45 | -19.4 | 580 | 0 | 78 | 22 | 0.3 | 272 |
| 70 | -19.1 | 601 | 0 | 74 | 26 | 0.4 | 185 |
| 100 | -18.6 | 636 | 1 | 64 | 35 | 0.7 | 85 |
