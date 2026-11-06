# Batch 5A, 22 Melting Orb: variants A-D (round 1, rendered, not yet heard)

**Level reading:** RMS dBFS (both channels, one power average) over **+9 s .. +14 s after the note-on of the 15 s hold on the phrase `v_drone_mid`** (the held, settled state; the note-on is at 3 s), target -18.0 +-1.5, VOLUME trimmed last; peak = the largest sample of any audition phrase (riff, stabs, held, drone, chord, taps), limit -4. `first 1 s` = RMS over the first second of the same hold. K-RMS = the same window K-weighted (informational). Worst-case CPU = idle + stress-chord load, host instructions per sample (a relative yardstick; 2900 us aim / 5800 us limit are device numbers).

## Variants at a glance

| variant | name | VOLUME | held level (RMS) | K-RMS | first 1 s | (b) stabs | peak (all phrases) | clipped | chord voices gated | worst-case CPU (host instr/sample) |
|---|---|---|---|---|---|---|---|---|---|---|
| A | original | 100 | -26.54 | -27.10 | -25.7 | -21.9 | -9.9 | 0 | 3 | 1770 |
| B | melt | 77 | -18.06 | -19.45 | -19.6 | -19.2 | -7.3 | 0 | 6 | 2488 |
| C | slow-deep | 77 | -18.03 | -19.80 | -19.3 | -19.4 | -5.8 | 0 | 6 | 2502 |
| D | dual-chord | 97 | -18.90 | -20.32 | -19.2 | -18.3 | -4.1 | 0 | 6 | 2489 |
| A* | original, level-matched | 127 | -22.41 | - | - | - | -6.2 | - | - | - |

A* is the original's tone with VOLUME alone moved as near the reference as the knob allows (a listening aid, not a candidate).

## Every change, before -> after (against A, the original)

**B (melt): 6-voice UNISON of saws on OSC 2, filter and pitch sink together: ~4 s to 90 %, pitch -6.9 st (about a fifth), LP12 RESO 75**

* O1_WAVE SAW -> OFF
* O1_LVL 110 -> 0 (-87%)
* O2_WAVE PULSE -> SAW
* O2_PW 30 -> 64 (+27%)
* O2_LVL 100 -> 110 (+8%)
* ENV_O2 64 -> 46 (centre 64: +0 -> -18, -14% of range) (+0.0 st at the env peak -> -6.9 st at the env peak)
* CUTOFF 50 -> 100 (+39%) (233 Hz -> 4186 Hz)
* RESO 70 -> 75 (+4%)
* FENV_AMT 124 -> 32 (centre 64: +60 -> -32, -72% of range)
* FTYPE BP12 -> LP12
* FA 20 -> 118 (+77%) (2 ms -> 4957 ms)
* FD 55 -> 60 (+4%) (36 ms -> 54 ms)
* FS 0 -> 127 (+100%)
* FR 60 -> 127 (+53%) (54 ms -> 10000 ms)
* AA 1 -> 60 (+46%) (1 ms -> 54 ms)
* AD 80 -> 100 (+16%) (256 ms -> 1218 ms)
* AS 70 -> 127 (+45%)
* AR 60 -> 92 (+25%) (54 ms -> 653 ms)
* MODE POLY -> UNISON
* UNI_N 4 -> 6 voices
* UNI_DET 30 -> 40 (+8%) (+-5.5 cents -> +-9.8 cents)
* VINTAGE 30 -> 40 (+8%)
* SPREAD 60 -> 110 (+39%)
* VOLUME 100 -> 77 (level trim, last)

**C (slow-deep): B slower (~5.5 s to 90 %), deeper (pitch -12.2 st, about an octave), RESO 100, a slightly longer release**

* O1_WAVE SAW -> OFF
* O1_LVL 110 -> 0 (-87%)
* O2_WAVE PULSE -> SAW
* O2_PW 30 -> 64 (+27%)
* O2_LVL 100 -> 110 (+8%)
* ENV_O2 64 -> 32 (centre 64: +0 -> -32, -25% of range) (+0.0 st at the env peak -> -12.2 st at the env peak)
* CUTOFF 50 -> 100 (+39%) (233 Hz -> 4186 Hz)
* RESO 70 -> 100 (+24%)
* FENV_AMT 124 -> 32 (centre 64: +60 -> -32, -72% of range)
* FTYPE BP12 -> LP12
* FA 20 -> 122 (+80%) (2 ms -> 6771 ms)
* FD 55 -> 60 (+4%) (36 ms -> 54 ms)
* FS 0 -> 127 (+100%)
* FR 60 -> 127 (+53%) (54 ms -> 10000 ms)
* AA 1 -> 60 (+46%) (1 ms -> 54 ms)
* AD 80 -> 100 (+16%) (256 ms -> 1218 ms)
* AS 70 -> 127 (+45%)
* AR 60 -> 100 (+31%) (54 ms -> 1218 ms)
* MODE POLY -> UNISON
* UNI_N 4 -> 6 voices
* UNI_DET 30 -> 40 (+8%) (+-5.5 cents -> +-9.8 cents)
* VINTAGE 30 -> 40 (+8%)
* SPREAD 60 -> 110 (+39%)
* VOLUME 100 -> 77 (level trim, last)

**D (dual-chord): B's melt in DUAL (POLY 6): a three-key chord melts together**

* O1_WAVE SAW -> OFF
* O1_LVL 110 -> 0 (-87%)
* O2_WAVE PULSE -> SAW
* O2_PW 30 -> 64 (+27%)
* O2_LVL 100 -> 110 (+8%)
* ENV_O2 64 -> 46 (centre 64: +0 -> -18, -14% of range) (+0.0 st at the env peak -> -6.9 st at the env peak)
* CUTOFF 50 -> 100 (+39%) (233 Hz -> 4186 Hz)
* RESO 70 -> 75 (+4%)
* FENV_AMT 124 -> 32 (centre 64: +60 -> -32, -72% of range)
* FTYPE BP12 -> LP12
* FA 20 -> 118 (+77%) (2 ms -> 4957 ms)
* FD 55 -> 60 (+4%) (36 ms -> 54 ms)
* FS 0 -> 127 (+100%)
* FR 60 -> 127 (+53%) (54 ms -> 10000 ms)
* AA 1 -> 60 (+46%) (1 ms -> 54 ms)
* AD 80 -> 100 (+16%) (256 ms -> 1218 ms)
* AS 70 -> 127 (+45%)
* AR 60 -> 92 (+25%) (54 ms -> 653 ms)
* MODE POLY -> DUAL
* UNI_N 4 -> 6 voices
* UNI_DET 30 -> 40 (+8%) (+-5.5 cents -> +-9.8 cents)
* VINTAGE 30 -> 40 (+8%)
* SPREAD 60 -> 110 (+39%)
* POLY_N 5 -> 6 voices
* VOLUME 100 -> 97 (level trim, last)


## The melt: A2 held, per 0.5 s window of the first 8 s

Pitch = the stack's dominant fundamental by harmonic summation (400 ms windows), cents re A2 (110 Hz); centroid in Hz; level in dB.

**A** (original)

| t (s) | 0.0 | 0.5 | 1.0 | 1.5 | 2.0 | 2.5 | 3.0 | 3.5 | 4.0 | 4.5 | 5.0 | 5.5 | 6.0 | 6.5 | 7.0 | 7.5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pitch (cents) | 0 | 0 | 5 | 0 | -1 | 0 | 2 | 0 | 5 | 5 | 0 | 0 | 2 | 2 | 0 | 2 |
| centroid (Hz) | 957 | 1081 | 1169 | 970 | 1087 | 777 | 642 | 1079 | 1083 | 1113 | 1010 | 1056 | 665 | 743 | 1101 | 1128 |
| level (dB) | -26.7 | -24.8 | -24.8 | -25.5 | -26.2 | -27.0 | -30.4 | -26.1 | -24.7 | -24.9 | -25.9 | -26.2 | -28.0 | -29.3 | -25.4 | -24.7 |

**B** (melt)

| t (s) | 0.0 | 0.5 | 1.0 | 1.5 | 2.0 | 2.5 | 3.0 | 3.5 | 4.0 | 4.5 | 5.0 | 5.5 | 6.0 | 6.5 | 7.0 | 7.5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pitch (cents) | -48 | -173 | -275 | -370 | -441 | -530 | -564 | -609 | -664 | -680 | -679 | -675 | -677 | -679 | -680 | -675 |
| centroid (Hz) | 1328 | 826 | 540 | 475 | 365 | 316 | 235 | 278 | 257 | 203 | 186 | 201 | 184 | 175 | 164 | 172 |
| level (dB) | -20.8 | -18.7 | -17.8 | -19.3 | -18.5 | -19.3 | -17.4 | -20.1 | -21.4 | -19.0 | -17.5 | -19.7 | -17.3 | -16.4 | -14.9 | -16.8 |

**C** (slow-deep)

| t (s) | 0.0 | 0.5 | 1.0 | 1.5 | 2.0 | 2.5 | 3.0 | 3.5 | 4.0 | 4.5 | 5.0 | 5.5 | 6.0 | 6.5 | 7.0 | 7.5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pitch (cents) | -64 | -231 | -384 | -513 | -605 | -734 | -825 | -904 | -976 | -1072 | -1123 | -1181 | -1205 | -1209 | -1206 | -1208 |
| centroid (Hz) | 1523 | 1018 | 717 | 687 | 558 | 321 | 293 | 266 | 277 | 187 | 191 | 199 | 195 | 209 | 182 | 152 |
| level (dB) | -20.5 | -18.4 | -17.7 | -20.2 | -21.1 | -15.4 | -16.4 | -17.3 | -19.8 | -15.7 | -17.1 | -19.2 | -20.2 | -20.7 | -18.4 | -16.1 |

**D** (dual-chord)

| t (s) | 0.0 | 0.5 | 1.0 | 1.5 | 2.0 | 2.5 | 3.0 | 3.5 | 4.0 | 4.5 | 5.0 | 5.5 | 6.0 | 6.5 | 7.0 | 7.5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pitch (cents) | -47 | -181 | -282 | -356 | -436 | -504 | -565 | -614 | -652 | -677 | -680 | -679 | -675 | -679 | -671 | -677 |
| centroid (Hz) | 1323 | 767 | 634 | 439 | 332 | 328 | 238 | 217 | 191 | 241 | 196 | 171 | 197 | 238 | 177 | 177 |
| level (dB) | -20.1 | -18.5 | -19.7 | -18.8 | -18.6 | -19.6 | -18.5 | -18.8 | -18.5 | -20.0 | -19.2 | -17.3 | -19.2 | -20.0 | -18.2 | -18.1 |

| variant | final pitch (cents re A2) | formula ENV>O2 (st) | pitch to 90 % / 98 % of its fall (s) | centroid start -> final (Hz) | fall in semitones | centroid to 90 % / 98 % of its fall (s, log axis) |
|---|---|---|---|---|---|---|
| A | +1 | - | - / - | 957 -> 937 | 0.4 | - / - |
| B | -675 | -6.86 | 4.0 / 4.5 | 1328 -> 201 | 32.7 | 3.5 / 5.0 |
| C | -1209 | -12.19 | 5.5 / 6.5 | 1523 -> 182 | 36.7 | 5.0 / 5.0 |
| D | -678 | -6.86 | 4.0 / 5.0 | 1323 -> 204 | 32.4 | 3.5 / 5.5 |

## Tone in windows (A2 hold): level dB / centroid Hz / MUD / band shares %

| variant | window | level | centroid | MUD | bands (<60 / 60-150 / 150-400 / 400-1.2k / 1.2k+) |
|---|---|---|---|---|---|
| A | 0-1s | -25.7 | 1035 | 174 | 0 / 69 / 27 / 3 / 0 |
| A | 1-3s | -25.8 | 1024 | 356 | 0 / 59 / 39 / 2 / 0 |
| A | 3-6s | -26.0 | 1043 | 232 | 0 / 68 / 29 / 2 / 0 |
| A | 6-8s | -26.5 | 992 | 248 | 0 / 62 / 35 / 3 / 0 |
| A | 9-14s | -26.5 | 991 | 320 | 0 / 55 / 43 / 3 / 0 |
| B | 0-1s | -19.6 | 1023 | 7 | 0 / 41 / 38 / 16 / 5 |
| B | 1-3s | -18.7 | 432 | 188 | 0 / 55 / 36 / 9 / 0 |
| B | 3-6s | -18.9 | 218 | 26037 | 0 / 59 / 41 / 0 / 0 |
| B | 6-8s | -16.3 | 172 | 23056 | 0 / 77 / 23 / 0 / 0 |
| B | 9-14s | -18.1 | 190 | 27229 | 0 / 73 / 27 / 0 / 0 |
| C | 0-1s | -19.3 | 1219 | 3 | 0 / 40 / 35 / 15 / 10 |
| C | 1-3s | -18.0 | 502 | 28 | 1 / 60 / 25 / 14 / 1 |
| C | 3-6s | -17.3 | 232 | 2889 | 24 / 53 / 22 / 1 / 0 |
| C | 6-8s | -18.5 | 173 | 16865 | 50 / 33 / 17 / 0 / 0 |
| C | 9-14s | -18.0 | 177 | 34181 | 36 / 30 / 34 / 0 / 0 |
| D | 0-1s | -19.2 | 952 | 6 | 0 / 60 / 24 / 13 / 4 |
| D | 1-3s | -19.1 | 418 | 178 | 0 / 57 / 34 / 9 / 0 |
| D | 3-6s | -18.6 | 203 | 26280 | 0 / 72 / 28 / 0 / 0 |
| D | 6-8s | -18.8 | 190 | 22448 | 0 / 77 / 22 / 0 / 0 |
| D | 9-14s | -18.9 | 193 | 25956 | 0 / 74 / 26 / 0 / 0 |

## The key-up (the note held to 15 s, then released): pitch cents and centroid Hz in 0.5 s windows after the key-up; ms to -20 / -40 / -60 dB

| variant | pitch 0-0.4 / 0.5 / 1.0 / 1.5 / 2.0 s | centroid | -20 / -40 / -60 dB |
|---|---|---|---|
| A | 2 / - / - / - / - | 968 / - / - / - / - | 74.0 / 114.0 / 168.0 |
| B | -634 / -549 / -472 / - / - | 242 / 724 / 2529 / - / - | 474.0 / 936.0 / 1428.0 |
| C | -1139 / -976 / -841 / -718 / -625 | 177 / 313 / 674 / 1194 / 2789 | 794.0 / 1732.0 / 2376.0 |
| D | -639 / -549 / -469 / - / - | 238 / 826 / 2469 / - / - | 474.0 / 932.0 / 1294.0 |

## Self-oscillation probe (oscillators off, noise-fed, note A2; diff 12 dB = linear, 0 = the filter sings by itself)

| variant | RESO | diff dB | verdict |
|---|---|---|---|
| A | 70 | 8.8 | near the edge |
| A | 127 | -0.0 | self-oscillates |
| B | 75 | 10.6 | linear |
| B | 127 | -0.2 | self-oscillates |
| C | 100 | 11.7 | linear |
| C | 127 | 0.2 | self-oscillates |
| D | 75 | 11.5 | linear |
| D | 127 | -0.0 | self-oscillates |

## Taps and the chord

| variant | tap A1 / A2 / A3 (150 ms gate RMS, dB re the held level) | centroid of the taps (Hz) | RMS 400 ms after each key-up (dB) | 3-key chord: cards gated | chord RMS (5-10.5 s) / peak |
|---|---|---|---|---|---|
| A | -3.6 / 2.1 / -1.9 | 524 / 1093 / 1326 | -210.3 / -210.3 / -210.3 | 3 | -21.4 / -11.3 |
| B | -3.6 / -5.2 / -3.8 | 895 / 1590 / 2007 | -36.7 / -36.3 / -32.6 | 6 | -18.2 / -7.3 |
| C | -3.4 / -3.1 / -3.4 | 1011 / 1634 / 2481 | -29.3 / -26.4 / -26.6 | 6 | -17.2 / -6.1 |
| D | -1.1 / -0.6 / 0.0 | 839 / 1266 / 1729 | -36.5 / -36.4 / -35.7 | 6 | -14.2 / -4.1 |

Per-phrase peaks (dBFS): A: a_riff -13.7, b_stabs -9.9, c_held -15.8, v_drone_mid -16.5, w_chord_mid -11.3, y_tap -14.0; B: a_riff -8.2, b_stabs -8.1, c_held -8.7, v_drone_mid -7.5, w_chord_mid -7.3, y_tap -11.4; C: a_riff -8.0, b_stabs -7.8, c_held -7.1, v_drone_mid -5.8, w_chord_mid -6.1, y_tap -9.4; D: a_riff -9.1, b_stabs -6.6, c_held -10.2, v_drone_mid -9.9, w_chord_mid -4.1, y_tap -10.7

