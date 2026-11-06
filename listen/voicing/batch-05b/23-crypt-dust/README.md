# 23 Crypt Dust: Batch 5B round 1 (rendered, not yet heard)

| var | tag | VOLUME | level | K-RMS | (b) RMS | peak (all phrases) | clip | CPU worst (idle+load) |
|---|---|---|---|---|---|---|---|---|
| A | original | 100 | -31.12 | -28.91 | -44.13 | -16.11 | 0 | 2009 |
| A* | original-matched | 127 | -27.02 | n/a | n/a | -11.90 | n/a | n/a |
| B | heavy | 124 | -18.00 | -16.86 | -18.10 | -5.80 | 0 | 2455 |
| C | half | 123 | -18.11 | -16.89 | -18.16 | -5.46 | 0 | 2454 |
| D | tapeless | 123 | -19.24 | -17.96 | -19.00 | -4.08 | 0 | 1685 |

Level = RMS over +4 s .. +10 s of the held A3 C#4 E4 triad (phrase z_chord), reference -18.0 dBFS +-1.5; peak limit -4 dBFS over z_chord, z_tap, a_riff, b_stabs.

## Parameter changes against the original (A)

**B heavy** (the brief as written: heavy tape wow (CHEW 100, WOW/FLT 16 = mostly wow), DROPS 90, HISS 64 (CHEW's own))

* O1_WAVE OFF -> PULSE
* O1_PW 64 -> 15 (-39%)
* O1_LVL 110 -> 127 (+13%)
* NOISE 100 -> 127 (+21%)
* CUTOFF 70 -> 72 (+2%) (740 Hz -> 831 Hz)
* AA 100 -> 60 (-31%) (1218 ms -> 54 ms)
* POLY_N 5 -> 2 voices
* CHEW 0 -> 100 (+79%)
* TP_WOWFLT 64 -> 16 (-38%)
* TP_DROPS 64 -> 90 (+20%)

**C half** (about half of B's CHEW (50), the rest of the tape settings as B)

* O1_WAVE OFF -> PULSE
* O1_PW 64 -> 15 (-39%)
* O1_LVL 110 -> 127 (+13%)
* NOISE 100 -> 127 (+21%)
* CUTOFF 70 -> 72 (+2%) (740 Hz -> 831 Hz)
* AA 100 -> 60 (-31%) (1218 ms -> 54 ms)
* POLY_N 5 -> 2 voices
* CHEW 0 -> 50 (+39%)
* TP_WOWFLT 64 -> 16 (-38%)
* TP_DROPS 64 -> 90 (+20%)

**D tapeless** (CHEW 0; the crumble from the one LFO (S&H) on AMP and FILTER, a short echo and the spring)

* O1_WAVE OFF -> PULSE
* O1_PW 64 -> 15 (-39%)
* O1_LVL 110 -> 127 (+13%)
* NOISE 100 -> 127 (+21%)
* CUTOFF 70 -> 72 (+2%) (740 Hz -> 831 Hz)
* AA 100 -> 60 (-31%) (1218 ms -> 54 ms)
* LFO_SHAPE TRI -> S&H
* LFO_RATE 20 -> 58 (+30%) (0.1 Hz -> 0.9 Hz)
* LFO_FLT 60 -> 45 (-12%)
* LFO_AMP 0 -> 46 (+36%)
* DLY_FB 50 -> 60 (+8%)
* DLY_TONE 70 -> 55 (-12%)
* DLY_MIX 0 -> 85 (+67%)
* REV_MIX 60 -> 80 (+16%)
* POLY_N 5 -> 2 voices
* ALLEY 0 -> 60 (+47%) (SYNC -> 75 ms)

## Tone in windows (held triad A3 C#4 E4, seconds after the note-on) and in the release

MUD = share 150-400 Hz over share above 1.2 kHz (scale: 10 A 2.5, 12 C 12.3, medium muddy about 10-40).

| var | window | RMS dB | centroid Hz | MUD | <150 | 150-400 | 400-1.2k | 1.2k+ |
|---|---|---|---|---|---|---|---|---|
| A | 0-1s | -34.5 | 4179 | 0.10 | 0 | 4 | 50 | 46 |
| A | 1-2s | -32.4 | 3779 | 0.24 | 0 | 9 | 56 | 35 |
| A | 2-4s | -32.6 | 3957 | 0.19 | 0 | 8 | 52 | 40 |
| A | 4-10s | -31.1 | 4486 | 0.05 | 0 | 3 | 34 | 63 |
| A | tail 0-0.5s | -34.8 | 3903 | 0.20 | 0 | 8 | 52 | 40 |
| A | tail 0.5-1.5s | -40.0 | 4007 | 0.13 | 0 | 6 | 48 | 46 |
| A | tail 1.5-3s | -50.1 | 4352 | 0.06 | 1 | 4 | 36 | 60 |
| A | tail 3-5s | -68.2 | 5074 | 0.01 | 15 | 1 | 16 | 68 |
| B | 0-1s | -17.6 | 2472 | 0.42 | 0 | 8 | 73 | 19 |
| B | 1-2s | -17.8 | 2151 | 1.38 | 0 | 16 | 73 | 11 |
| B | 2-4s | -17.9 | 2327 | 0.73 | 0 | 11 | 73 | 16 |
| B | 4-10s | -18.0 | 2667 | 0.31 | 0 | 8 | 64 | 27 |
| B | tail 0-0.5s | -19.8 | 2339 | 0.74 | 0 | 10 | 76 | 14 |
| B | tail 0.5-1.5s | -26.0 | 2706 | 0.35 | 0 | 7 | 71 | 21 |
| B | tail 1.5-3s | -38.1 | 4013 | 0.12 | 0 | 4 | 58 | 37 |
| B | tail 3-5s | -51.9 | 8244 | 0.02 | 3 | 2 | 23 | 73 |
| C | 0-1s | -17.8 | 2769 | 0.35 | 0 | 7 | 73 | 20 |
| C | 1-2s | -18.0 | 2373 | 1.16 | 0 | 14 | 74 | 12 |
| C | 2-4s | -18.0 | 2592 | 0.62 | 0 | 10 | 73 | 17 |
| C | 4-10s | -18.1 | 3013 | 0.25 | 0 | 7 | 63 | 29 |
| C | tail 0-0.5s | -20.0 | 2562 | 0.63 | 0 | 9 | 76 | 15 |
| C | tail 0.5-1.5s | -26.2 | 2777 | 0.30 | 0 | 7 | 71 | 22 |
| C | tail 1.5-3s | -38.2 | 3359 | 0.10 | 0 | 4 | 58 | 38 |
| C | tail 3-5s | -56.5 | 4987 | 0.05 | 5 | 2 | 41 | 51 |
| D | 0-1s | -18.0 | 3596 | 0.09 | 0 | 3 | 57 | 40 |
| D | 1-2s | -17.6 | 3709 | 0.07 | 0 | 3 | 50 | 47 |
| D | 2-4s | -18.1 | 3500 | 0.09 | 0 | 4 | 55 | 41 |
| D | 4-10s | -19.2 | 3289 | 0.15 | 0 | 5 | 61 | 34 |
| D | tail 0-0.5s | -22.0 | 3063 | 0.23 | 0 | 6 | 68 | 26 |
| D | tail 0.5-1.5s | -28.3 | 2946 | 0.22 | 0 | 6 | 65 | 28 |
| D | tail 1.5-3s | -40.3 | 2916 | 0.29 | 0 | 7 | 69 | 24 |
| D | tail 3-5s | -58.4 | 3121 | 0.21 | 2 | 6 | 64 | 28 |

## What the tape does (against the same patch with CHEW 0)

Pitch: the strongest harmonic of the thin pulse alone (no noise, echo or spring) tracked in 100 ms frames (A3 held 8 s). Dips: level dips over 6 dB under the running median (10 ms RMS) on a held A3 of the whole patch, 7 s. Floor: RMS 14 s and 15 s after the chord's note-on (1 s windows), after the notes are off.

| var | CHEW | pitch s.d. cents | pitch 5-95 % cents | wow rate Hz | dips (count / deepest dB) | level s.d. dB | floor 17-18 s | floor 18-19 s | centroid 4-10 s | 1.2k+ share 4-10 s |
|---|---|---|---|---|---|---|---|---|---|---|
| A as | 0 | n/a | n/a .. n/a | n/a | 0 / 2.6 | 1.58 | -81.5 | -210.3 | 4486 | 62.9 |
| A chew0 | 0 | n/a | n/a .. n/a | n/a | 0 / 2.6 | 1.58 | -81.6 | -210.3 | 4484 | 62.7 |
| B as | 100 | 7.4 | -11.5 .. 13.2 | 0.55 | 4 / 10.7 | 1.33 | -53.5 | -53.6 | 2667 | 27.3 |
| B chew0 | 0 | 0.0 | -0.0 .. 0.0 | 11.75 | 0 / 1.7 | 0.68 | -71.8 | -210.3 | 3403 | 30.8 |
| C as | 50 | 2.6 | -4.4 .. 4.0 | 0.55 | 0 / 1.5 | 0.72 | -65.4 | -66.8 | 3013 | 29.4 |
| C chew0 | 0 | 0.0 | -0.0 .. 0.0 | 7.41 | 0 / 1.7 | 0.68 | -72.0 | -210.3 | 3403 | 30.8 |
| D as | 0 | 0.0 | -0.0 .. 0.0 | 7.41 | 0 / 2.1 | 1.01 | -74.3 | -87.3 | 3289 | 34.3 |
| D chew0 | 0 | 0.0 | -0.0 .. 0.0 | 7.41 | 0 / 2.1 | 1.01 | -74.3 | -87.3 | 3289 | 34.3 |

## The LFO and the echo (D)

| var | LFO Hz | shape | AMP dip dB | FILTER excursion st | level s.d. of the dry held chord dB | echo ms / FEEDBK | echo return -40 dB after the note (ms) | repeats above -40 dB |
|---|---|---|---|---|---|---|---|---|
| B | 0.14 | 0 | 0.0 | 10.6 | 0.64 | none | n/a | n/a |
| C | 0.14 | 0 | 0.0 | 10.6 | 0.64 | none | n/a | n/a |
| D | 0.93 | 4 | 3.9 | 5.7 | 1.26 | 75 / 60 | 382 | 6 |

Release: time to -20 / -40 / -60 dB after the note-off (ms): A 2308.0/3816.0/4610.0; B 1714.0/None/None; C 2064.0/3694.0/None; D 2028.0/3630.0/4530.0 (None = not reached inside 5.8 s).
