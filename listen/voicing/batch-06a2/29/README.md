# 29 i scream, Batch 6A2 round 1 (rendered, not yet heard)

Slot 29 was VALHALLA (a chordal wash: round 1 of Batch 6A was rejected). It is rebuilt as `i scream`, an ice-cream-van chime. A is the ORIGINAL VALHALLA values level-matched, a reference and not a candidate; B, C, D are the candidates; Dfinal is the APPROVED version (variant D with CHEW 0, re-measured; it has not been heard); Ebox and Fmetal are calibration renders of the OSC 2 interval (on C). Level phrase: the note-on region of the chime melody (aj, 27 notes 580 ms apart, gate 250 ms); peak limit -4 dBFS over every audition phrase (the three-note chord is the limiting one).

| var | tag | VOLUME | level aj | level chord (an) | level run (ao) | peak | (b) stabs | CPU | what |
|---|---|---|---|---|---|---|---|---|---|
| A | valhalla-ref | 110 | -20.81 | -18.4 | -18.6 | -4.1 | -16.8 | 1995 | the original VALHALLA values (a pad), level-matched: a reference, not a candidate |
| B | plink | 112 | -26.51 | -33.0 | -23.6 | -4.1 | -30.1 | 2640 | van-true short plink: AMP DECAY 64, light tape (CHEW 25) |
| C | short-ring | 111 | -19.17 | -24.2 | -16.9 | -4.0 | -22.5 | 2642 | plink with a short ring: AMP DECAY 89, medium tape (CHEW 45) |
| D | long-shimmer | 111 | -18.10 | -21.4 | -16.9 | -5.0 | -21.9 | 2647 | FINGERSYM-style long ring: AMP DECAY 101, heavier tape (CHEW 65), the delayed LFO shimmer (TRI 0.8 Hz, pitch +-9.4 cents, amp 40, delay 40, PHASE SYNC) |
| Dfinal | D-no-tape | 113 | -17.88 | -21.3 | -16.6 | -4.1 | -21.8 | 1863 | the APPROVED version: variant D with CHEW 0 (no tape at all), everything else as D |
| Ebox | music-box | 110 | -19.29 | -24.4 | -17.0 | -4.1 | -22.7 | 2600 | calibration: C with a nearer-harmonic interval (OSC 2 +12 st, FINE 70, X-MOD 0, LEVEL 50) |
| Fmetal | metallic | 112 | -18.66 | -23.9 | -16.5 | -4.1 | -21.9 | 2637 | calibration: C with a strongly inharmonic interval (OSC 2 +17 st, LEVEL 100, X-MOD 70) |

**Every change over the original VALHALLA values (percent = of the parameter's range):**

* **B plink:** O1_WAVE saw -> pulse; O1_LVL 110 -> 127 (+13%); O2_LVL 100 -> 70 (-24%); O2_SEMI 24 -> 39 (+31%); XMOD 0 -> 25 (+20%); ENV_O2 64 -> 76 (+9%); O2_FINE 73 -> 64 (-7%); CUTOFF 55 -> 77 (+17%); RESO 15 -> 105 (+71%); FENV_AMT 94 -> 64 (-24%); KEYTRK 64 -> 0 (-50%); FTYPE LP24 -> BP12; DRIVE 0 -> 30 (+24%); VEL_FLT 40 -> 0 (-31%); FA 70 -> 0 (-55%); FD 70 -> 50 (-16%); FS 40 -> 0 (-31%); FR 90 -> 30 (-47%); AA 60 -> 0 (-47%); AD 70 -> 64 (-5%); AS 100 -> 0 (-79%); AR 90 -> 50 (-31%); LFO_PHASE FREE -> SYNC; VINTAGE 127 -> 10 (-92%); SPREAD 120 -> 70 (-39%); DLY_FB 50 -> 22 (-22%); DLY_TONE 70 -> 60 (-8%); DLY_MIX 0 -> 35 (+28%); REV_SIZE 105 -> 40 (-51%); REV_DAMP 60 -> 40 (-16%); REV_PRE 20 -> 8 (-9%); REV_MIX 45 -> 18 (-21%); CHEW 0 -> 25 (+20%); TP_HISS 64 -> 25 (-31%); TP_DROPS 64 -> 20 (-35%); ALLEY 0 -> 56 (+44%); VOLUME 100 -> 112
* **C short-ring:** O1_WAVE saw -> pulse; O1_LVL 110 -> 127 (+13%); O2_LVL 100 -> 70 (-24%); O2_SEMI 24 -> 39 (+31%); XMOD 0 -> 25 (+20%); ENV_O2 64 -> 76 (+9%); O2_FINE 73 -> 64 (-7%); CUTOFF 55 -> 77 (+17%); RESO 15 -> 105 (+71%); FENV_AMT 94 -> 64 (-24%); KEYTRK 64 -> 0 (-50%); FTYPE LP24 -> BP12; DRIVE 0 -> 30 (+24%); VEL_FLT 40 -> 0 (-31%); FA 70 -> 0 (-55%); FD 70 -> 50 (-16%); FS 40 -> 0 (-31%); FR 90 -> 30 (-47%); AA 60 -> 0 (-47%); AD 70 -> 89 (+15%); AS 100 -> 0 (-79%); AR 90 -> 50 (-31%); LFO_PHASE FREE -> SYNC; VINTAGE 127 -> 10 (-92%); SPREAD 120 -> 70 (-39%); DLY_FB 50 -> 22 (-22%); DLY_TONE 70 -> 60 (-8%); DLY_MIX 0 -> 35 (+28%); REV_SIZE 105 -> 40 (-51%); REV_DAMP 60 -> 40 (-16%); REV_PRE 20 -> 8 (-9%); REV_MIX 45 -> 18 (-21%); CHEW 0 -> 45 (+35%); TP_HISS 64 -> 25 (-31%); TP_DROPS 64 -> 20 (-35%); ALLEY 0 -> 56 (+44%); VOLUME 100 -> 111
* **D long-shimmer:** O1_WAVE saw -> pulse; O1_LVL 110 -> 127 (+13%); O2_LVL 100 -> 70 (-24%); O2_SEMI 24 -> 39 (+31%); XMOD 0 -> 25 (+20%); ENV_O2 64 -> 76 (+9%); O2_FINE 73 -> 64 (-7%); CUTOFF 55 -> 77 (+17%); RESO 15 -> 105 (+71%); FENV_AMT 94 -> 64 (-24%); KEYTRK 64 -> 0 (-50%); FTYPE LP24 -> BP12; DRIVE 0 -> 30 (+24%); VEL_FLT 40 -> 0 (-31%); FA 70 -> 0 (-55%); FD 70 -> 50 (-16%); FS 40 -> 0 (-31%); FR 90 -> 30 (-47%); AA 60 -> 0 (-47%); AD 70 -> 101 (+24%); AS 100 -> 0 (-79%); AR 90 -> 50 (-31%); LFO_RATE 70 -> 55 (-12%); LFO_DELAY 0 -> 40 (+31%); LFO_PHASE FREE -> SYNC; LFO_PITCH 0 -> 14 (+11%); LFO_AMP 0 -> 40 (+31%); VINTAGE 127 -> 10 (-92%); SPREAD 120 -> 70 (-39%); DLY_FB 50 -> 22 (-22%); DLY_TONE 70 -> 60 (-8%); DLY_MIX 0 -> 35 (+28%); REV_SIZE 105 -> 40 (-51%); REV_DAMP 60 -> 40 (-16%); REV_PRE 20 -> 8 (-9%); REV_MIX 45 -> 18 (-21%); CHEW 0 -> 65 (+51%); TP_HISS 64 -> 25 (-31%); TP_DROPS 64 -> 20 (-35%); ALLEY 0 -> 56 (+44%); VOLUME 100 -> 111
* **Dfinal D-no-tape:** O1_WAVE saw -> pulse; O1_LVL 110 -> 127 (+13%); O2_LVL 100 -> 70 (-24%); O2_SEMI 24 -> 39 (+31%); XMOD 0 -> 25 (+20%); ENV_O2 64 -> 76 (+9%); O2_FINE 73 -> 64 (-7%); CUTOFF 55 -> 77 (+17%); RESO 15 -> 105 (+71%); FENV_AMT 94 -> 64 (-24%); KEYTRK 64 -> 0 (-50%); FTYPE LP24 -> BP12; DRIVE 0 -> 30 (+24%); VEL_FLT 40 -> 0 (-31%); FA 70 -> 0 (-55%); FD 70 -> 50 (-16%); FS 40 -> 0 (-31%); FR 90 -> 30 (-47%); AA 60 -> 0 (-47%); AD 70 -> 101 (+24%); AS 100 -> 0 (-79%); AR 90 -> 50 (-31%); LFO_RATE 70 -> 55 (-12%); LFO_DELAY 0 -> 40 (+31%); LFO_PHASE FREE -> SYNC; LFO_PITCH 0 -> 14 (+11%); LFO_AMP 0 -> 40 (+31%); VINTAGE 127 -> 10 (-92%); SPREAD 120 -> 70 (-39%); DLY_FB 50 -> 22 (-22%); DLY_TONE 70 -> 60 (-8%); DLY_MIX 0 -> 35 (+28%); REV_SIZE 105 -> 40 (-51%); REV_DAMP 60 -> 40 (-16%); REV_PRE 20 -> 8 (-9%); REV_MIX 45 -> 18 (-21%); TP_HISS 64 -> 25 (-31%); TP_DROPS 64 -> 20 (-35%); ALLEY 0 -> 56 (+44%); VOLUME 100 -> 113
* **Ebox music-box:** O1_WAVE saw -> pulse; O1_LVL 110 -> 127 (+13%); O2_LVL 100 -> 50 (-39%); O2_SEMI 24 -> 36 (+25%); O2_FINE 73 -> 70 (-2%); CUTOFF 55 -> 77 (+17%); RESO 15 -> 105 (+71%); FENV_AMT 94 -> 64 (-24%); KEYTRK 64 -> 0 (-50%); FTYPE LP24 -> BP12; DRIVE 0 -> 30 (+24%); VEL_FLT 40 -> 0 (-31%); FA 70 -> 0 (-55%); FD 70 -> 50 (-16%); FS 40 -> 0 (-31%); FR 90 -> 30 (-47%); AA 60 -> 0 (-47%); AD 70 -> 89 (+15%); AS 100 -> 0 (-79%); AR 90 -> 50 (-31%); LFO_PHASE FREE -> SYNC; VINTAGE 127 -> 10 (-92%); SPREAD 120 -> 70 (-39%); DLY_FB 50 -> 22 (-22%); DLY_TONE 70 -> 60 (-8%); DLY_MIX 0 -> 35 (+28%); REV_SIZE 105 -> 40 (-51%); REV_DAMP 60 -> 40 (-16%); REV_PRE 20 -> 8 (-9%); REV_MIX 45 -> 18 (-21%); CHEW 0 -> 45 (+35%); TP_HISS 64 -> 25 (-31%); TP_DROPS 64 -> 20 (-35%); ALLEY 0 -> 56 (+44%); VOLUME 100 -> 110
* **Fmetal metallic:** O1_WAVE saw -> pulse; O1_LVL 110 -> 127 (+13%); O2_SEMI 24 -> 41 (+35%); XMOD 0 -> 70 (+55%); ENV_O2 64 -> 76 (+9%); O2_FINE 73 -> 64 (-7%); CUTOFF 55 -> 77 (+17%); RESO 15 -> 105 (+71%); FENV_AMT 94 -> 64 (-24%); KEYTRK 64 -> 0 (-50%); FTYPE LP24 -> BP12; DRIVE 0 -> 30 (+24%); VEL_FLT 40 -> 0 (-31%); FA 70 -> 0 (-55%); FD 70 -> 50 (-16%); FS 40 -> 0 (-31%); FR 90 -> 30 (-47%); AA 60 -> 0 (-47%); AD 70 -> 89 (+15%); AS 100 -> 0 (-79%); AR 90 -> 50 (-31%); LFO_PHASE FREE -> SYNC; VINTAGE 127 -> 10 (-92%); SPREAD 120 -> 70 (-39%); DLY_FB 50 -> 22 (-22%); DLY_TONE 70 -> 60 (-8%); DLY_MIX 0 -> 35 (+28%); REV_SIZE 105 -> 40 (-51%); REV_DAMP 60 -> 40 (-16%); REV_PRE 20 -> 8 (-9%); REV_MIX 45 -> 18 (-21%); CHEW 0 -> 45 (+35%); TP_HISS 64 -> 25 (-31%); TP_DROPS 64 -> 20 (-35%); ALLEY 0 -> 56 (+44%); VOLUME 100 -> 112

## Decay of the actual render (C#6 and C#5 held 3 s; ms after the strike's peak to fall 6 / 12 / 20 / 30 / 40 dB; 4 ms power envelope; the voice alone = no tape, echo or spring; the van recording read 19 / 33 / 70 ms for 6 / 12 / 20 dB, one hit, very rough)

| var | AMP DECAY nominal ms | FILTER DECAY nominal ms | voice C#6 | voice C#5 | whole patch C#6 | whole patch C#5 |
|---|---|---|---|---|---|---|
| A | 117 | 117 | 70 / 99 / 332 / 3190 / 3223 | 110 / 185 / 3145 / 3252 / 3313 | 59 / 93 / 1442 / 3495 / 3819 | 117 / 266 / 3183 / 3327 / 3587 |
| B | 74 | 25 | 18 / 35 / 57 / 86 / 114 | 16 / 33 / 56 / 84 / 111 | 18 / 36 / 61 / 116 / 186 | 18 / 35 / 73 / 125 / 167 |
| C | 517 | 25 | 123 / 243 / 401 / 598 / 787 | 111 / 235 / 389 / 584 / 775 | 86 / 219 / 362 / 572 / 758 | 113 / 231 / 390 / 587 / 779 |
| D | 1317 | 25 | 309 / 612 / 928 / 1577 / 1954 | 284 / 584 / 908 / 1548 / 1934 | 249 / 552 / 1031 / 1574 / 1907 | 252 / 566 / 913 / 1498 / 1939 |
| Dfinal | 1317 | 25 | 309 / 612 / 928 / 1577 / 1954 | 284 / 584 / 908 / 1548 / 1934 | 252 / 550 / 1030 / 1573 / 1896 | 276 / 584 / 938 / 1513 / 1943 |
| Ebox | 517 | 25 | 122 / 240 / 400 / 596 / 787 | 109 / 231 / 391 / 582 / 773 | 89 / 225 / 376 / 574 / 768 | 110 / 226 / 392 / 577 / 767 |
| Fmetal | 517 | 25 | 122 / 241 / 400 / 596 / 787 | 117 / 232 / 395 / 589 / 779 | 131 / 250 / 414 / 607 / 805 | 93 / 208 / 373 / 573 / 755 |

## Tape and shimmer (a ONE-VOICE probe: a held saw with a sustained envelope, the filter open, CHEW and the LFO as the patch has them; fundamental tracked in 25 ms hops, cents)

| var | CHEW | wobble s.d. as built | 5-95 % range | strongest rate Hz | s.d. with CHEW 0 (LFO only) | tremolo depth dB / rate Hz (probe) |
|---|---|---|---|---|---|---|
| A | 0 | 0.00 | -0.0 .. 0.0 | 0.00 | 0.00 | 0.08 / 8.73 |
| B | 25 | 1.65 | -3.2 .. 2.5 | 0.31 | 0.00 | 0.08 / 8.88 |
| C | 45 | 2.51 | -3.6 .. 4.4 | 0.42 | 0.00 | 0.08 / 11.00 |
| D | 65 | 6.14 | -12.2 .. 8.8 | 0.87 | 5.11 | 2.83 / 0.80 |
| Dfinal | 0 | 5.11 | -8.2 .. 8.3 | 0.80 | 5.11 | 2.85 / 0.80 |
| Ebox | 45 | 2.51 | -3.6 .. 4.4 | 0.42 | 0.00 | 0.08 / 10.99 |
| Fmetal | 45 | 2.51 | -3.6 .. 4.4 | 0.42 | 0.00 | 0.08 / 10.99 |

## The front edge (centroid over the first 20 ms from the audible onset, Hz; whole patch with the echo and spring off; CHEW as built against CHEW 0; onset = ms from the note-on to the first sample above -50 dB)

| var | C#6 CHEW | C#6 CHEW 0 | change | C#5 CHEW | C#5 CHEW 0 | change | onset (ms) CHEW / 0 |
|---|---|---|---|---|---|---|---|
| A | 1291 | 1291 | +0 | 711 | 711 | +0 | -3.9 / -3.9 |
| B | 2016 | 2095 | -78 | 1865 | 1952 | -87 | -3.4 / -4.6 |
| C | 1975 | 2097 | -122 | 1814 | 1957 | -143 | -3.3 / -4.6 |
| D | 1933 | 2094 | -161 | 1768 | 1958 | -190 | -3.3 / -4.6 |
| Dfinal | 2096 | 2096 | +0 | 1958 | 1958 | +0 | -4.6 / -4.6 |
| Ebox | 1905 | 2016 | -110 | 1734 | 1870 | -136 | -3.3 / -4.6 |
| Fmetal | 2082 | 2220 | -138 | 1931 | 2091 | -160 | -3.3 / -4.6 |

## The speaker band (the filter read with white noise, settled, 1/6 octave; and the melody's note-on region through the whole patch)

| var | honk peak Hz | -3 dB width Hz (from-to) | noise: under 400 Hz % | noise: above 4 kHz % | noise centroid Hz | melody: under 400 % | melody: above 4 kHz % | melody centroid Hz |
|---|---|---|---|---|---|---|---|---|
| A | 424 | 739 (133-872) | 34.8 | 0.0 | 657 | 0.00 | 2.17 | 1471 |
| B | 1099 | 447 (898-1345) | 0.4 | 4.1 | 1537 | 0.03 | 0.36 | 1276 |
| C | 1099 | 447 (898-1345) | 0.4 | 4.1 | 1537 | 0.00 | 0.39 | 1257 |
| D | 1099 | 447 (898-1345) | 0.4 | 4.1 | 1537 | 0.00 | 0.36 | 1251 |
| Dfinal | 1099 | 447 (898-1345) | 0.4 | 4.1 | 1537 | 0.00 | 0.45 | 1262 |
| Ebox | 1099 | 447 (898-1345) | 0.4 | 4.1 | 1537 | 0.00 | 0.37 | 1266 |
| Fmetal | 1099 | 447 (898-1345) | 0.4 | 4.1 | 1537 | 0.02 | 0.33 | 1272 |

## Partials of the first 100 ms (Hz, dB re the strongest, ratio to the played note; the voice alone, 'heard' = through the filter as built, 'raw' = the filter open and DRIVE 0; peaks under -45 dB left out)

* A C#6 1109 Hz heard: 1107 (+0 dB, x1.00), 2212 (-9 dB, x1.99), 3317 (-16 dB, x2.99), 4426 (-24 dB, x3.99), 5506 (-31 dB, x4.97), 6607 (-34 dB, x5.96), 7709 (-39 dB, x6.95); off the integer ratios by more than 0.1: 0
* A C#6 1109 Hz raw: 1104 (+0 dB, x1.00), 2206 (-7 dB, x1.99), 3310 (-12 dB, x2.99), 4416 (-17 dB, x3.98), 5522 (-20 dB, x4.98), 6625 (-23 dB, x5.98), 7729 (-25 dB, x6.97); off the integer ratios by more than 0.1: 0
* A C#5 554 Hz heard: 554 (+0 dB, x1.00), 1107 (-9 dB, x2.00), 1658 (-16 dB, x2.99), 2206 (-22 dB, x3.98), 2755 (-28 dB, x4.97), 3304 (-32 dB, x5.96), 3854 (-35 dB, x6.95); off the integer ratios by more than 0.1: 0
* A C#5 554 Hz raw: 552 (+0 dB, x1.00), 1103 (-8 dB, x1.99), 1653 (-15 dB, x2.98), 2199 (-20 dB, x3.97), 2750 (-22 dB, x4.96), 3320 (-22 dB, x5.99), 3870 (-22 dB, x6.98); off the integer ratios by more than 0.1: 0
* B C#6 1109 Hz heard: 948 (-43 dB, x0.86), 1106 (+0 dB, x1.00), 1266 (-43 dB, x1.14), 2640 (-35 dB, x2.38), 3319 (-15 dB, x2.99), 5533 (-26 dB, x4.99), 7746 (-37 dB, x6.99); off the integer ratios by more than 0.1: 3
* B C#6 1109 Hz raw: 1106 (+0 dB, x1.00), 2641 (-19 dB, x2.38), 3319 (-10 dB, x2.99), 5277 (-26 dB, x4.76), 5533 (-14 dB, x4.99), 7745 (-18 dB, x6.99), 9958 (-21 dB, x8.98); off the integer ratios by more than 0.1: 2
* B C#5 554 Hz heard: 553 (+0 dB, x1.00), 1106 (-29 dB, x2.00), 1322 (-19 dB, x2.38), 1659 (-8 dB, x2.99), 2765 (-16 dB, x4.99), 3871 (-21 dB, x6.98), 4978 (-27 dB, x8.98); off the integer ratios by more than 0.1: 1
* B C#5 554 Hz raw: 553 (+0 dB, x1.00), 1322 (-18 dB, x2.38), 1659 (-10 dB, x2.99), 2765 (-14 dB, x4.99), 3871 (-17 dB, x6.98), 4978 (-20 dB, x8.98), 6084 (-22 dB, x10.97); off the integer ratios by more than 0.1: 1
* C C#6 1109 Hz heard: 949 (-42 dB, x0.86), 1106 (+0 dB, x1.00), 1789 (-42 dB, x1.61), 2638 (-34 dB, x2.38), 3319 (-15 dB, x2.99), 5532 (-26 dB, x4.99), 7745 (-36 dB, x6.99); off the integer ratios by more than 0.1: 3
* C C#6 1109 Hz raw: 1106 (+0 dB, x1.00), 2638 (-18 dB, x2.38), 3319 (-10 dB, x2.99), 5274 (-25 dB, x4.76), 5532 (-14 dB, x4.99), 7745 (-18 dB, x6.99), 9958 (-21 dB, x8.98); off the integer ratios by more than 0.1: 2
* C C#5 554 Hz heard: 553 (+0 dB, x1.00), 893 (-29 dB, x1.61), 1320 (-19 dB, x2.38), 1659 (-8 dB, x2.99), 2765 (-16 dB, x4.99), 3871 (-21 dB, x6.98), 4978 (-27 dB, x8.98); off the integer ratios by more than 0.1: 2
* C C#5 554 Hz raw: 553 (+0 dB, x1.00), 1320 (-17 dB, x2.38), 1659 (-10 dB, x2.99), 2765 (-14 dB, x4.99), 3871 (-17 dB, x6.98), 4978 (-20 dB, x8.98), 6084 (-22 dB, x10.97); off the integer ratios by more than 0.1: 1
* D C#6 1109 Hz heard: 949 (-42 dB, x0.86), 1106 (+0 dB, x1.00), 1789 (-42 dB, x1.61), 2637 (-34 dB, x2.38), 3319 (-15 dB, x2.99), 5532 (-26 dB, x4.99), 7745 (-36 dB, x6.99); off the integer ratios by more than 0.1: 3
* D C#6 1109 Hz raw: 1106 (+0 dB, x1.00), 2638 (-18 dB, x2.38), 3319 (-10 dB, x2.99), 5273 (-25 dB, x4.76), 5532 (-14 dB, x4.99), 7745 (-18 dB, x6.99), 9958 (-21 dB, x8.98); off the integer ratios by more than 0.1: 2
* D C#5 554 Hz heard: 553 (+0 dB, x1.00), 893 (-28 dB, x1.61), 1320 (-18 dB, x2.38), 1659 (-8 dB, x2.99), 2765 (-16 dB, x4.99), 3871 (-21 dB, x6.98), 4978 (-27 dB, x8.98); off the integer ratios by more than 0.1: 2
* D C#5 554 Hz raw: 553 (+0 dB, x1.00), 1320 (-17 dB, x2.38), 1659 (-10 dB, x2.99), 2765 (-14 dB, x4.99), 3871 (-17 dB, x6.98), 4978 (-20 dB, x8.98), 6084 (-22 dB, x10.97); off the integer ratios by more than 0.1: 1
* Dfinal C#6 1109 Hz heard: 949 (-42 dB, x0.86), 1106 (+0 dB, x1.00), 1789 (-42 dB, x1.61), 2637 (-34 dB, x2.38), 3319 (-15 dB, x2.99), 5532 (-26 dB, x4.99), 7745 (-36 dB, x6.99); off the integer ratios by more than 0.1: 3
* Dfinal C#6 1109 Hz raw: 1106 (+0 dB, x1.00), 2638 (-18 dB, x2.38), 3319 (-10 dB, x2.99), 5273 (-25 dB, x4.76), 5532 (-14 dB, x4.99), 7745 (-18 dB, x6.99), 9958 (-21 dB, x8.98); off the integer ratios by more than 0.1: 2
* Dfinal C#5 554 Hz heard: 553 (+0 dB, x1.00), 893 (-28 dB, x1.61), 1320 (-18 dB, x2.38), 1659 (-8 dB, x2.99), 2765 (-16 dB, x4.99), 3871 (-21 dB, x6.98), 4978 (-27 dB, x8.98); off the integer ratios by more than 0.1: 2
* Dfinal C#5 554 Hz raw: 553 (+0 dB, x1.00), 1320 (-17 dB, x2.38), 1659 (-10 dB, x2.99), 2765 (-14 dB, x4.99), 3871 (-17 dB, x6.98), 4978 (-20 dB, x8.98), 6084 (-22 dB, x10.97); off the integer ratios by more than 0.1: 1
* Ebox C#6 1109 Hz heard: 1108 (+0 dB, x1.00), 1326 (-44 dB, x1.20), 2220 (-37 dB, x2.00), 3324 (-15 dB, x3.00), 5539 (-26 dB, x5.00), 7755 (-36 dB, x6.99), 9971 (-43 dB, x8.99); off the integer ratios by more than 0.1: 1
* Ebox C#6 1109 Hz raw: 1108 (+0 dB, x1.00), 2221 (-22 dB, x2.00), 3324 (-10 dB, x3.00), 4445 (-29 dB, x4.01), 5539 (-14 dB, x5.00), 7755 (-18 dB, x6.99), 9971 (-21 dB, x8.99); off the integer ratios by more than 0.1: 0
* Ebox C#5 554 Hz heard: 554 (+0 dB, x1.00), 1112 (-24 dB, x2.01), 1662 (-8 dB, x3.00), 2219 (-30 dB, x4.00), 2770 (-16 dB, x5.00), 3878 (-21 dB, x7.00), 4986 (-27 dB, x8.99); off the integer ratios by more than 0.1: 0
* Ebox C#5 554 Hz raw: 554 (+0 dB, x1.00), 1662 (-10 dB, x3.00), 2770 (-14 dB, x5.00), 3878 (-17 dB, x7.00), 4986 (-20 dB, x8.99), 6094 (-22 dB, x10.99), 7202 (-23 dB, x12.99); off the integer ratios by more than 0.1: 0
* Fmetal C#6 1109 Hz heard: 737 (-33 dB, x0.66), 1112 (+0 dB, x1.00), 1488 (-34 dB, x1.34), 1849 (-31 dB, x1.67), 2960 (-27 dB, x2.67), 3336 (-16 dB, x3.01), 5560 (-27 dB, x5.01); off the integer ratios by more than 0.1: 4
* Fmetal C#6 1109 Hz raw: 1112 (+0 dB, x1.00), 2961 (-11 dB, x2.67), 3336 (-10 dB, x3.01), 5560 (-15 dB, x5.01), 5919 (-19 dB, x5.34), 7783 (-19 dB, x7.02), 10007 (-22 dB, x9.03); off the integer ratios by more than 0.1: 2
* Fmetal C#5 554 Hz heard: 554 (+0 dB, x1.00), 928 (-20 dB, x1.67), 1289 (-22 dB, x2.32), 1481 (-13 dB, x2.67), 1662 (-8 dB, x3.00), 2770 (-17 dB, x5.00), 3878 (-22 dB, x7.00); off the integer ratios by more than 0.1: 3
* Fmetal C#5 554 Hz raw: 554 (+0 dB, x1.00), 1481 (-11 dB, x2.67), 1662 (-10 dB, x3.00), 2770 (-14 dB, x5.00), 2961 (-18 dB, x5.34), 3878 (-18 dB, x7.00), 4986 (-20 dB, x8.99); off the integer ratios by more than 0.1: 2

## Space (C#6 held 400 ms: the echo and spring's own return against the dry note in the windows after the strike; dry level in dB; the echo is 65 ms)

| var | 0-20 ms: dry / return / re dry | 20-100 ms | 100-250 ms | 250-500 ms re dry | 500-1000 ms re dry |
|---|---|---|---|---|---|
| A | -27.9 / -67.4 / -39.5 | -18.4 / -30.4 / -12.0 | -25.4 / -29.7 / -4.3 | -6.0 | +5.8 |
| B | -17.4 / -45.4 / -28.0 | -29.5 / -35.7 / -6.2 | -60.7 / -46.6 / +14.1 | +12.2 | -11.6 |
| C | -14.2 / -44.1 / -29.9 | -16.5 / -30.8 / -14.3 | -21.9 / -32.6 / -10.7 | -11.5 | +4.9 |
| D | -15.3 / -45.4 / -30.1 | -16.2 / -31.4 / -15.2 | -18.4 / -31.3 / -12.8 | -12.4 | +8.9 |
| Dfinal | -15.1 / -43.8 / -28.7 | -16.0 / -31.0 / -15.0 | -18.2 / -31.0 / -12.8 | -12.4 | +149.9 |
| Ebox | -14.3 / -44.3 / -30.0 | -16.7 / -31.7 / -15.0 | -22.0 / -34.2 / -12.2 | -12.6 | +2.0 |
| Fmetal | -14.2 / -44.4 / -30.2 | -16.5 / -32.4 / -15.9 | -21.9 / -36.6 / -14.7 | -14.8 | +5.7 |

## Register (one note each, 600 ms, whole patch: RMS 0-300 ms, centroid 0-100 ms and 100-400 ms, peak)

| var | A4 level / centroid / ring centroid | C#6 | A6 |
|---|---|---|---|
| A | -19.4 dB / 1102 / 871 Hz | -20.8 dB / 2007 / 1520 Hz | -21.7 dB / 2873 / 2114 Hz |
| B | -32.7 dB / 1847 / 2520 Hz | -28.2 dB / 2060 / 2303 Hz | -30.4 dB / 2464 / 3012 Hz |
| C | -23.8 dB / 1816 / 1849 Hz | -20.1 dB / 2040 / 2149 Hz | -21.7 dB / 2392 / 2470 Hz |
| D | -22.3 dB / 1779 / 1813 Hz | -18.7 dB / 2006 / 2086 Hz | -20.3 dB / 2359 / 2432 Hz |
| Dfinal | -22.1 dB / 1950 / 1964 Hz | -18.5 dB / 2183 / 2249 Hz | -20.1 dB / 2563 / 2610 Hz |
| Ebox | -24.0 dB / 1779 / 1809 Hz | -20.2 dB / 1986 / 2110 Hz | -22.0 dB / 2346 / 2430 Hz |
| Fmetal | -23.5 dB / 1884 / 1885 Hz | -19.3 dB / 2227 / 2132 Hz | -20.7 dB / 2559 / 2521 Hz |

## The voice pool (POLY 4 / 5 / 6 against POLY 8, VINTAGE 0 in all; levels of what rings, dB re POLY 8: negative = a ring was cut)

| var | melody slot tail, mean / worst note | fast run tail 1.4-2.4 s | chord tail |
|---|---|---|---|
| B POLY 4 | +0.1 / -0.2 | -0.1 | +0.0 |
| B POLY 5 | -0.0 / -0.6 | -0.1 | +0.0 |
| B POLY 6 | -0.1 / -0.7 | -0.5 | +0.0 |
| C POLY 4 | +0.0 / -0.1 | -0.1 | +0.0 |
| C POLY 5 | -0.0 / -0.6 | -0.1 | +0.0 |
| C POLY 6 | -0.1 / -0.6 | -0.3 | +0.0 |
| D POLY 4 | +0.0 / -0.1 | -0.1 | +0.0 |
| D POLY 5 | -0.0 / -0.6 | -0.2 | +0.0 |
| D POLY 6 | -0.1 / -0.6 | -0.2 | +0.0 |

## Crust and cost (on C: the melody, dry of nothing; crest = peak over RMS of the note-on region, dB; level at the same VOLUME; CPU = worst case idle + load)

| setting | crest | level | peak | CPU |
|---|---|---|---|---|
| DRIVE 0 | 10.2 | -18.7 | -8.5 | 2587 |
| DRIVE 30 (as built) | 10.3 | -19.2 | -8.9 | 2642 |
| DRIVE 60 | 10.1 | -18.8 | -8.7 | 2613 |
| DRIVE 100 | 10.1 | -18.8 | -8.7 | 2607 |
| GROWL 34 | 8.6 | -19.2 | -10.7 | 3236 |
| GROWL 44 | 7.4 | -19.3 | -11.9 | 3236 |
| GROWL 44, CHEW 0 | 7.4 | -19.4 | -11.9 | 2452 |
| CHEW 0 | 10.6 | -19.3 | -8.8 | 1858 |

## CPU levers on C (worst case, host instr/sample)

* C as built: 2642
* DRIVE 0: 2587
* POLY 4: 2642
* POLY 3: 2574
* DRIVE 0 + POLY 4: 2587
* OSC 2 silent, X-MOD 0, ENV>O2 0: 2600
* OSC 2 wave off: 2642
* LP12 instead of the band-pass: 2642
* no echo (DLY MIX 0): 2626
* no spring (DRAIN 0): 2642
* no echo, no spring: 2626
* OSC 1 saw instead of square: 2613
* CHEW 0 (from the crust table): 1858
