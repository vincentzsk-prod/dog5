# 29 VALHALLA, Batch 6A round 1 (rendered, not yet heard)

Level phrase: RMS over +4 s .. +10 s of the held triad (`z_chord`, sends included), peak limit -4 dBFS over every audition phrase. Rung W1 (wetness L1) is measured but not rendered (listen branch weight).

| var | tag | VOLUME | level (z_chord +4..+10 s) | peak | (b) stabs | (b) - level | CPU | what |
|---|---|---|---|---|---|---|---|---|
| A | original | 100 | -18.55 | -5.0 | -18.4 | 0.1 | 1995 | the original through the base program path |
| B | plain | 55 | -17.90 | -5.3 | -32.1 | -14.2 | 2651 | a plain, brighter PWM wash: two pulses (PW 34 / 31 %) through LP12 (KEY TRK 100), mild erosion, wetness L3 |
| C | hollow | 66 | -18.05 | -5.4 | -35.4 | -17.4 | 2652 | the soft, hollow colour: a narrower pulse (30 %), an octave-up pulse copy at LEVEL 45, a resonant LP12 at a fixed CUTOFF 78 / RESO 75 (KEY TRK 0), a lighter spring (MIX 95, DRAIN 25) |
| D | hollow-wet | 65 | -17.96 | -4.8 | -35.4 | -17.4 | 2652 | C's colour, wetter (echo FEEDBK 82, MIX 110, DRAIN 38, SIZE 90) and a deeper filter bloom (ENV AMT 100) |
| W2 | wet-L2 | 55 | -18.07 | -5.7 | -32.3 | -14.2 | 2651 | B on wetness rung L2 |
| W4 | wet-L4 | 54 | -17.88 | -4.9 | -31.9 | -14.0 | 2651 | B on wetness rung L4 |
| W5 | wet-L5 | 52 | -17.96 | -4.7 | -31.5 | -13.5 | 2651 | B on wetness rung L5 |
| E2 | erode-deep | 58 | -17.96 | -4.8 | -31.3 | -13.3 | 2652 | B with a deeper erosion (CUTOFF 70, ENV AMT 90, FILTER SUSTAIN 0) |

**Every change over the original (percent = of the parameter's range):**

* **B plain:** O1_WAVE saw -> pulse; O1_PW 64 -> 44 (-16%); O2_WAVE saw -> pulse; O2_PW 64 -> 40 (-19%); O2_FINE 73 -> 70 (-2%); CUTOFF 55 -> 78 (+18%); RESO 15 -> 8 (-6%); FENV_AMT 94 -> 100 (+5%); KEYTRK 64 -> 100 (+28%); FTYPE LP24 -> LP12; FA 70 -> 60 (-8%); FD 70 -> 118 (+38%); FS 40 -> 20 (-16%); AA 60 -> 96 (+28%); AS 100 -> 127 (+21%); AR 90 -> 100 (+8%); LFO_RATE 70 -> 53 (-13%); LFO_PHASE FREE -> SPREAD; LFO_PITCH 0 -> 16 (+13%); LFO_PWM 0 -> 80 (+63%); MODE POLY -> DUAL; UNI_DET 30 -> 20 (-8%); VINTAGE 127 -> 8 (-94%); SPREAD 120 -> 127 (+6%); DLY_FB 50 -> 65 (+12%); DLY_MIX 0 -> 85 (+67%); REV_SIZE 105 -> 80 (-20%); REV_MIX 45 -> 35 (-8%); POLY_N 5 -> 6 (+12%); ALLEY 0 -> 96 (+76%); VOLUME 100 -> 55
* **C hollow:** O1_WAVE saw -> pulse; O1_PW 64 -> 38 (-20%); O1_LVL 110 -> 100 (-8%); O2_WAVE saw -> pulse; O2_PW 64 -> 44 (-16%); O2_LVL 100 -> 45 (-43%); O2_SEMI 24 -> 36 (+25%); O2_FINE 73 -> 70 (-2%); CUTOFF 55 -> 78 (+18%); RESO 15 -> 75 (+47%); FENV_AMT 94 -> 70 (-19%); KEYTRK 64 -> 0 (-50%); FTYPE LP24 -> LP12; FA 70 -> 60 (-8%); FD 70 -> 118 (+38%); FS 40 -> 0 (-31%); AA 60 -> 100 (+31%); AS 100 -> 127 (+21%); AR 90 -> 100 (+8%); LFO_RATE 70 -> 53 (-13%); LFO_PHASE FREE -> SPREAD; LFO_PITCH 0 -> 16 (+13%); LFO_PWM 0 -> 60 (+47%); MODE POLY -> DUAL; UNI_DET 30 -> 20 (-8%); VINTAGE 127 -> 8 (-94%); SPREAD 120 -> 127 (+6%); DLY_FB 50 -> 65 (+12%); DLY_MIX 0 -> 95 (+75%); REV_SIZE 105 -> 80 (-20%); REV_MIX 45 -> 25 (-16%); POLY_N 5 -> 6 (+12%); ALLEY 0 -> 96 (+76%); VOLUME 100 -> 66
* **D hollow-wet:** O1_WAVE saw -> pulse; O1_PW 64 -> 38 (-20%); O1_LVL 110 -> 100 (-8%); O2_WAVE saw -> pulse; O2_PW 64 -> 44 (-16%); O2_LVL 100 -> 45 (-43%); O2_SEMI 24 -> 36 (+25%); O2_FINE 73 -> 70 (-2%); CUTOFF 55 -> 78 (+18%); RESO 15 -> 75 (+47%); FENV_AMT 94 -> 100 (+5%); KEYTRK 64 -> 0 (-50%); FTYPE LP24 -> LP12; FA 70 -> 60 (-8%); FD 70 -> 118 (+38%); FS 40 -> 0 (-31%); AA 60 -> 100 (+31%); AS 100 -> 127 (+21%); AR 90 -> 100 (+8%); LFO_RATE 70 -> 53 (-13%); LFO_PHASE FREE -> SPREAD; LFO_PITCH 0 -> 16 (+13%); LFO_PWM 0 -> 60 (+47%); MODE POLY -> DUAL; UNI_DET 30 -> 20 (-8%); VINTAGE 127 -> 8 (-94%); SPREAD 120 -> 127 (+6%); DLY_FB 50 -> 82 (+25%); DLY_MIX 0 -> 110 (+87%); REV_SIZE 105 -> 90 (-12%); REV_MIX 45 -> 38 (-6%); POLY_N 5 -> 6 (+12%); ALLEY 0 -> 96 (+76%); VOLUME 100 -> 65
* **W2 wet-L2:** O1_WAVE saw -> pulse; O1_PW 64 -> 44 (-16%); O2_WAVE saw -> pulse; O2_PW 64 -> 40 (-19%); O2_FINE 73 -> 70 (-2%); CUTOFF 55 -> 78 (+18%); RESO 15 -> 8 (-6%); FENV_AMT 94 -> 100 (+5%); KEYTRK 64 -> 100 (+28%); FTYPE LP24 -> LP12; FA 70 -> 60 (-8%); FD 70 -> 118 (+38%); FS 40 -> 20 (-16%); AA 60 -> 96 (+28%); AS 100 -> 127 (+21%); AR 90 -> 100 (+8%); LFO_RATE 70 -> 53 (-13%); LFO_PHASE FREE -> SPREAD; LFO_PITCH 0 -> 16 (+13%); LFO_PWM 0 -> 80 (+63%); MODE POLY -> DUAL; UNI_DET 30 -> 20 (-8%); VINTAGE 127 -> 8 (-94%); SPREAD 120 -> 127 (+6%); DLY_FB 50 -> 55 (+4%); DLY_MIX 0 -> 70 (+55%); REV_SIZE 105 -> 75 (-24%); REV_MIX 45 -> 30 (-12%); POLY_N 5 -> 6 (+12%); ALLEY 0 -> 96 (+76%); VOLUME 100 -> 55
* **W4 wet-L4:** O1_WAVE saw -> pulse; O1_PW 64 -> 44 (-16%); O2_WAVE saw -> pulse; O2_PW 64 -> 40 (-19%); O2_FINE 73 -> 70 (-2%); CUTOFF 55 -> 78 (+18%); RESO 15 -> 8 (-6%); FENV_AMT 94 -> 100 (+5%); KEYTRK 64 -> 100 (+28%); FTYPE LP24 -> LP12; FA 70 -> 60 (-8%); FD 70 -> 118 (+38%); FS 40 -> 20 (-16%); AA 60 -> 96 (+28%); AS 100 -> 127 (+21%); AR 90 -> 100 (+8%); LFO_RATE 70 -> 53 (-13%); LFO_PHASE FREE -> SPREAD; LFO_PITCH 0 -> 16 (+13%); LFO_PWM 0 -> 80 (+63%); MODE POLY -> DUAL; UNI_DET 30 -> 20 (-8%); VINTAGE 127 -> 8 (-94%); SPREAD 120 -> 127 (+6%); DLY_FB 50 -> 78 (+22%); DLY_MIX 0 -> 105 (+83%); REV_SIZE 105 -> 90 (-12%); POLY_N 5 -> 6 (+12%); ALLEY 0 -> 96 (+76%); VOLUME 100 -> 54
* **W5 wet-L5:** O1_WAVE saw -> pulse; O1_PW 64 -> 44 (-16%); O2_WAVE saw -> pulse; O2_PW 64 -> 40 (-19%); O2_FINE 73 -> 70 (-2%); CUTOFF 55 -> 78 (+18%); RESO 15 -> 8 (-6%); FENV_AMT 94 -> 100 (+5%); KEYTRK 64 -> 100 (+28%); FTYPE LP24 -> LP12; FA 70 -> 60 (-8%); FD 70 -> 118 (+38%); FS 40 -> 20 (-16%); AA 60 -> 96 (+28%); AS 100 -> 127 (+21%); AR 90 -> 100 (+8%); LFO_RATE 70 -> 53 (-13%); LFO_PHASE FREE -> SPREAD; LFO_PITCH 0 -> 16 (+13%); LFO_PWM 0 -> 80 (+63%); MODE POLY -> DUAL; UNI_DET 30 -> 20 (-8%); VINTAGE 127 -> 8 (-94%); SPREAD 120 -> 127 (+6%); DLY_FB 50 -> 92 (+33%); DLY_MIX 0 -> 120 (+94%); REV_SIZE 105 -> 100 (-4%); REV_MIX 45 -> 65 (+16%); POLY_N 5 -> 6 (+12%); ALLEY 0 -> 96 (+76%); VOLUME 100 -> 52
* **E2 erode-deep:** O1_WAVE saw -> pulse; O1_PW 64 -> 44 (-16%); O2_WAVE saw -> pulse; O2_PW 64 -> 40 (-19%); O2_FINE 73 -> 70 (-2%); CUTOFF 55 -> 70 (+12%); RESO 15 -> 8 (-6%); FENV_AMT 94 -> 90 (-3%); KEYTRK 64 -> 100 (+28%); FTYPE LP24 -> LP12; FA 70 -> 60 (-8%); FD 70 -> 118 (+38%); FS 40 -> 0 (-31%); AA 60 -> 96 (+28%); AS 100 -> 127 (+21%); AR 90 -> 100 (+8%); LFO_RATE 70 -> 53 (-13%); LFO_PHASE FREE -> SPREAD; LFO_PITCH 0 -> 16 (+13%); LFO_PWM 0 -> 80 (+63%); MODE POLY -> DUAL; UNI_DET 30 -> 20 (-8%); VINTAGE 127 -> 8 (-94%); SPREAD 120 -> 127 (+6%); DLY_FB 50 -> 65 (+12%); DLY_MIX 0 -> 85 (+67%); REV_SIZE 105 -> 80 (-20%); REV_MIX 45 -> 35 (-8%); POLY_N 5 -> 6 (+12%); ALLEY 0 -> 96 (+76%); VOLUME 100 -> 58

## Bloom: the amp envelope (one voice, OSC 2 off, VINTAGE 0, FX off) and the held chord's level against its settled level (RMS 4-10 s)

| var | amp env 10 / 50 / 90 % (ms) | chord at 0.25 / 0.5 / 1.0 s, linear, dry | same with the sends | 1.0 s with the sends (dB) | meets 60 % by 1.0 s | centroid settled / 0.25 / 0.5 / 1.0 s (Hz, dry) |
|---|---|---|---|---|---|---|
| A | 3 / 15 / 27 | 1.21 / 1.09 / 0.95 | 1.21 / 1.08 / 1.00 | -0.0 | yes | 468 / 468 / 452 / 504 |
| B | 46 / 272 / 639 | 0.52 / 0.99 / 0.99 | 0.50 / 0.94 / 0.94 | -0.5 | yes | 1087 / 3567 / 3132 / 2341 |
| C | 63 / 376 / 878 | 0.37 / 0.60 / 0.92 | 0.36 / 0.54 / 0.85 | -1.4 | yes | 892 / 1168 / 1246 / 1050 |
| D | 64 / 377 / 882 | 0.36 / 0.58 / 0.90 | 0.34 / 0.50 / 0.79 | -2.0 | yes | 927 / 3809 / 3894 / 2772 |
| W2 | 46 / 272 / 639 | 0.52 / 0.99 / 0.99 | 0.51 / 0.96 / 0.95 | -0.5 | yes | 1087 / 3567 / 3132 / 2341 |
| W4 | 46 / 273 / 641 | 0.52 / 0.99 / 0.99 | 0.48 / 0.91 / 0.93 | -0.7 | yes | 1087 / 3567 / 3132 / 2341 |
| W5 | 46 / 273 / 641 | 0.52 / 0.99 / 0.98 | 0.46 / 0.87 / 0.89 | -1.0 | yes | 1087 / 3567 / 3132 / 2341 |
| E2 | 45 / 266 / 627 | 0.58 / 1.09 / 1.06 | 0.55 / 1.03 / 1.02 | +0.1 | yes | 629 / 1899 / 1548 / 1209 |

## Chorus (DUAL pair, SPREAD 127, TRI LFO PHASE SPREAD; held chord 4-10 s, dry, 150-4000 Hz; one render each: differences of about 0.1 are not a trend)

| var | LFO Hz | depth cents | L/R corr as built | LFO PITCH 0 | POLY (no chorus) | beat depth dB with / without the pitch LFO (A3 band) | CPU as built | CPU as POLY, no pitch LFO |
|---|---|---|---|---|---|---|---|---|
| A | 1.70 | 0.0 | 0.69 | 0.69 | 0.69 | 19.1 / 19.1 | 1995 |  |
| B | 0.72 | 18.8 | 0.39 | 0.37 | 0.66 | 15.0 / 8.1 | 2651 | 2041 |
| C | 0.72 | 18.8 | 0.36 | 0.38 | 0.67 | 23.9 / 16.1 | 2652 | 2042 |
| D | 0.72 | 18.8 | 0.36 | 0.38 | 0.67 | 23.9 / 16.1 | 2652 | 2041 |
| W2 | 0.72 | 18.8 | 0.39 | 0.37 | 0.66 | 15.0 / 8.1 | 2651 |  |
| W4 | 0.72 | 18.8 | 0.39 | 0.37 | 0.66 | 15.0 / 8.1 | 2651 |  |
| W5 | 0.72 | 18.8 | 0.39 | 0.37 | 0.66 | 15.0 / 8.1 | 2651 |  |
| E2 | 0.72 | 18.8 | 0.39 | 0.37 | 0.66 | 15.1 / 8.0 | 2652 |  |

## Drift (the engine's own vlog, DUAL, one held note, cents: static offset / s.d. / range, per card)

* A (VINTAGE 127): card 0: -7.7 / 5.7 / -23..+18; card 1: +3.6 / 6.5 / -25..+30
* B (VINTAGE 8): card 0: -1.0 / 0.4 / -2..+1; card 1: -0.2 / 0.4 / -2..+2
* C (VINTAGE 8): card 0: -1.0 / 0.4 / -2..+1; card 1: -0.2 / 0.4 / -2..+2

## A fourth note on POLY 6 DUAL (A3 C#4 E4 held, G#4 added at +3 s; each note's fundamental band +-40 cents, dB, before -> 1.2 s after the fourth note-on)

* B: MIDI 57: 144.7 -> 146.4; MIDI 61: 149.3 -> 140.5; MIDI 64: 144.2 -> 143.4; MIDI 68: 94.0 -> 145.2
* C: MIDI 57: 143.9 -> 142.9; MIDI 61: 149.2 -> 139.4; MIDI 64: 144.7 -> 146.4; MIDI 68: 91.5 -> 142.6

## Erosion (dry, held chord; band level in dB in one-second windows, change from the 1 s window to the 10 s window = 'drop'; centroid Hz)

| var | 150-400 Hz drop 1->10 s | 400-1.2k drop | 1.2k+ drop | 150-400 / 400-1.2k peak-to-peak 1.5-9 s | RMS 1 / 3 / 6 / 10 s | centroid 1 / 3 / 6 / 10 s |
|---|---|---|---|---|---|---|
| A | -0.5 | -0.4 | +0.1 | 0.9 / 1.3 | -19.1 / -19.0 / -18.8 / -18.7 | 488 / 485 / 475 / 477 |
| B | +0.7 | -1.0 | +3.7 | 3.5 / 1.9 | -18.4 / -18.6 / -17.9 / -18.5 | 2838 / 1597 / 1125 / 1167 |
| C | +1.3 | -1.0 | +1.0 | 2.0 / 1.3 | -19.3 / -18.6 / -18.5 / -18.8 | 1103 / 1000 / 937 / 990 |
| D | +1.2 | -1.6 | +1.9 | 2.0 / 1.3 | -19.8 / -19.0 / -18.8 / -19.1 | 2904 / 1377 / 980 / 991 |
| W2 | +0.7 | -1.0 | +3.7 | 3.5 / 1.9 | -18.4 / -18.6 / -17.9 / -18.5 | 2838 / 1597 / 1125 / 1167 |
| W4 | +0.7 | -1.0 | +3.7 | 3.5 / 1.9 | -18.7 / -18.9 / -18.2 / -18.8 | 2838 / 1597 / 1125 / 1168 |
| W5 | +0.7 | -1.0 | +3.7 | 3.5 / 1.9 | -19.3 / -19.6 / -18.8 / -19.5 | 2839 / 1598 / 1126 / 1168 |
| E2 | +1.2 | +1.2 | +10.1 | 3.4 / 3.5 | -17.7 / -18.4 / -17.9 / -18.7 | 1424 / 861 / 630 / 674 |

## The wetness ladder and the sends (full patch; return windows after the 10 s chord's key-up in dB re the chord's own level over the 400 ms before; first repeat of an isolated E4 re the note, delay's margin over the spring)

| var | echo ms | FEEDBK | MIX | DRAIN | SIZE | echo return 0-250 / 250-750 / 750-1500 ms | spring return same | sum same | first repeat dB | margin over spring dB | tail to -20 / -40 / -60 dB (ms) | tail MUD 0-250 / 250-750 / 750-1500 (level dB) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B | 257 | 65 | 85 | 35 | 80 | -10.9 / -14.8 / -24.3 | -17.9 / -23.2 / -37.6 | -10.1 / -14.0 / -24.2 | -10.4 | 7.8 | 865 / 1695 / 2495 | 12 (-22) / 51 (-27) / 35 (-39) |
| C | 257 | 65 | 95 | 25 | 80 | -10.2 / -12.2 / -22.1 | -16.2 / -24.6 / -38.8 | -8.8 / -11.7 / -22.0 | -10.7 | 7.8 | 935 / 1930 / 2535 | 16 (-20) / 22 (-26) / 15 (-38) |
| D | 257 | 82 | 110 | 38 | 90 | -8.2 / -9.7 / -17.9 | -12.0 / -19.7 / -34.2 | -6.2 / -8.9 / -17.6 | -9.6 | 6.0 | 1150 / 2295 / 3155 | 16 (-20) / 21 (-25) / 20 (-35) |
| W2 | 257 | 55 | 70 | 30 | 75 | -13.0 / -17.2 / -27.1 | -19.5 / -25.0 / -39.2 | -12.1 / -16.3 / -27.0 | -12.1 | 7.5 | 865 / 1695 / 2490 | 13 (-22) / 55 (-27) / 37 (-40) |
| W4 | 257 | 78 | 105 | 45 | 90 | -8.5 / -11.9 / -20.4 | -15.1 / -20.1 / -34.5 | -7.5 / -11.0 / -20.2 | -8.6 | 7.3 | 920 / 1965 / 2750 | 12 (-21) / 42 (-26) / 33 (-38) |
| W5 | 257 | 92 | 120 | 65 | 100 | -6.4 / -9.2 / -16.2 | -11.4 / -16.0 / -29.8 | -4.8 / -7.8 / -15.6 | -7.4 | 5.2 | 1210 / 2495 / 3525 | 12 (-21) / 30 (-25) / 31 (-35) |
| E2 | 257 | 65 | 85 | 35 | 80 | -11.0 / -14.8 / -24.2 | -19.0 / -24.0 / -37.8 | -10.3 / -14.1 / -24.2 | -10.4 | 7.8 | 865 / 1695 / 2500 | 66 (-22) / 212 (-27) / 106 (-39) |

Reference (16 D): first repeat -8.6 dB, 7.7 dB over the spring.

## The hump (white noise through the settled filter, held triad 4-10 s, dry; 1/6-octave smoothing)

| var | peak Hz (300-3000) | -3 dB width Hz (from-to) | height over the same filter at RESO 0 (dB) | peak over the 150-3000 Hz mean (dB) | centroid of the held chord (Hz) |
|---|---|---|---|---|---|
| A | 356 | 517 (100-617) | +0.5 | +10.1 | 481 |
| B | 490 | 1367 (100-1467) | +0.1 | +2.3 | 1183 |
| C | 1165 | 1338 (308-1647) | +7.3 | +3.3 | 937 |
| D | 1199 | 1487 (308-1796) | +7.2 | +3.0 | 975 |
| W2 | 490 | 1367 (100-1467) | +0.1 | +2.3 | 1183 |
| W4 | 490 | 1367 (100-1467) | +0.1 | +2.3 | 1183 |
| W5 | 490 | 1367 (100-1467) | +0.1 | +2.3 | 1184 |
| E2 | 490 | 592 (100-692) | +0.4 | +5.1 | 668 |
