# 26 BSyncA, Batch 6A round 1 (rendered, not yet heard)

Level phrase: the note-on region of `d_lead` (the single-note lead phrase), peak limit -4 dBFS over every audition phrase; the standard stabs phrase (b) is shown for the difference (a MONO patch plays the last key of a stab only).

| var | tag | VOLUME | level (d_lead) | peak | (b) stabs | (b) - level | CPU | what |
|---|---|---|---|---|---|---|---|---|
| A | original | 100 | -23.12 | -14.1 | -22.0 | 1.1 | 1370 | the original through the base program path |
| B | drive | 79 | -17.98 | -8.0 | -17.6 | 0.4 | 1775 | the fat base + per-voice filter DRIVE 60, no GROWL, dry |
| C | growl34 | 90 | -18.05 | -9.4 | -17.2 | 0.9 | 2326 | the fat base + GROWL 34, dry |
| D | growl44 | 90 | -18.05 | -11.0 | -17.1 | 0.9 | 2326 | the fat base + GROWL 44, dry |
| E52 | growl52 | 91 | -17.89 | -11.9 | -16.9 | 1.0 | 2326 | calibration: the fat base + GROWL 52, dry |
| F70 | growl70 | 91 | -17.92 | -12.6 | -16.9 | 1.0 | 2327 | calibration: the fat base + GROWL 70, dry (the dictionary's fuzzy edge) |
| Droom | growl44-room | 90 | -18.01 | -9.4 | -17.0 | 1.0 | 2340 | calibration: D + a very light room (86 ms slap, FEEDBK 22, MIX 28; spring MIX 18, SIZE 60) |

**Every change over the original (percent = of the parameter's range):**

* **B drive:** O1_LVL 0 -> 90 (+71%); CUTOFF 90 -> 84 (-5%); FENV_AMT 80 -> 100 (+16%); DRIVE 0 -> 60 (+47%); MODE MONO -> UNISON; UNI_N 4 -> 3 (-12%); UNI_DET 30 -> 22 (-6%); GLIDE 20 -> 50 (+24%); DLY_MIX 35 -> 0 (-28%); REV_MIX 22 -> 0 (-17%); VOLUME 100 -> 79
* **C growl34:** O1_LVL 0 -> 90 (+71%); CUTOFF 90 -> 84 (-5%); FENV_AMT 80 -> 100 (+16%); MODE MONO -> UNISON; UNI_N 4 -> 3 (-12%); UNI_DET 30 -> 22 (-6%); GLIDE 20 -> 50 (+24%); GROWL 0 -> 34 (+27%); DLY_MIX 35 -> 0 (-28%); REV_MIX 22 -> 0 (-17%); VOLUME 100 -> 90
* **D growl44:** O1_LVL 0 -> 90 (+71%); CUTOFF 90 -> 84 (-5%); FENV_AMT 80 -> 100 (+16%); MODE MONO -> UNISON; UNI_N 4 -> 3 (-12%); UNI_DET 30 -> 22 (-6%); GLIDE 20 -> 50 (+24%); GROWL 0 -> 44 (+35%); DLY_MIX 35 -> 0 (-28%); REV_MIX 22 -> 0 (-17%); VOLUME 100 -> 90
* **E52 growl52:** O1_LVL 0 -> 90 (+71%); CUTOFF 90 -> 84 (-5%); FENV_AMT 80 -> 100 (+16%); MODE MONO -> UNISON; UNI_N 4 -> 3 (-12%); UNI_DET 30 -> 22 (-6%); GLIDE 20 -> 50 (+24%); GROWL 0 -> 52 (+41%); DLY_MIX 35 -> 0 (-28%); REV_MIX 22 -> 0 (-17%); VOLUME 100 -> 91
* **F70 growl70:** O1_LVL 0 -> 90 (+71%); CUTOFF 90 -> 84 (-5%); FENV_AMT 80 -> 100 (+16%); MODE MONO -> UNISON; UNI_N 4 -> 3 (-12%); UNI_DET 30 -> 22 (-6%); GLIDE 20 -> 50 (+24%); GROWL 0 -> 70 (+55%); DLY_MIX 35 -> 0 (-28%); REV_MIX 22 -> 0 (-17%); VOLUME 100 -> 91
* **Droom growl44-room:** O1_LVL 0 -> 90 (+71%); CUTOFF 90 -> 84 (-5%); FENV_AMT 80 -> 100 (+16%); MODE MONO -> UNISON; UNI_N 4 -> 3 (-12%); UNI_DET 30 -> 22 (-6%); GLIDE 20 -> 50 (+24%); GROWL 0 -> 44 (+35%); DLY_FB 40 -> 22 (-14%); DLY_TONE 70 -> 55 (-12%); DLY_MIX 35 -> 28 (-6%); REV_SIZE 70 -> 60 (-8%); REV_MIX 22 -> 18 (-3%); ALLEY 0 -> 64 (+50%); VOLUME 100 -> 90

## The drive ladder (the fat base, dry, VOLUME 100, d_lead note-on region; compression = RMS change against the same patch with no drive)

| rung | crest dB | level shift dB | peak dBFS | CPU | rip centroid 0-50 / 50-150 / 150-400 ms (Hz) |
|---|---|---|---|---|---|
| filter DRIVE 60 only | 9.0 | +1.99 | -5.1 | 1775 | 4270 / 1896 / 1004 |
| GROWL 34 | 7.3 | -0.28 | -8.8 | 2326 | 2953 / 1801 / 1108 |
| GROWL 44 | 6.0 | -0.29 | -10.2 | 2326 | 2662 / 1724 / 1111 |
| GROWL 52 | 5.5 | -0.31 | -10.8 | 2326 | 2647 / 1761 / 1156 |
| GROWL 70 | 5.1 | -0.33 | -11.3 | 2327 | 2674 / 1899 / 1327 |
| no drive (the fat base) | 11.7 | +0.00 | -4.1 | n/a | |
| GROWL 90 | 5.0 | -0.30 | -11.4 | n/a | |
| GROWL 127 | 5.0 | -0.21 | -11.2 | n/a | |

## The rip (detached A3, 1 s, FX off; centroid Hz and share of energy above 1.2 kHz in the window; 'off' = ENV>O2 64, no sweep)

| var | 0-50 ms | 50-150 | 150-400 | no sweep: 0-50 / 50-150 / 150-400 |
|---|---|---|---|---|
| A | 2212 Hz (27 %) | 1396 Hz (12 %) | 1066 Hz (8 %) | 1619 / 1145 / 926 |
| B | 4276 Hz (37 %) | 1893 Hz (20 %) | 1008 Hz (8 %) | 3396 / 1588 / 850 |
| C | 2932 Hz (51 %) | 1773 Hz (24 %) | 1090 Hz (10 %) | 2355 / 1595 / 937 |
| D | 2626 Hz (48 %) | 1686 Hz (23 %) | 1082 Hz (9 %) | 2084 / 1509 / 919 |
| E52 | 2598 Hz (48 %) | 1713 Hz (23 %) | 1118 Hz (9 %) | 2050 / 1523 / 942 |
| F70 | 2598 Hz (48 %) | 1822 Hz (23 %) | 1255 Hz (9 %) | 2029 / 1619 / 1057 |
| Droom | 2626 Hz (48 %) | 1686 Hz (23 %) | 1082 Hz (9 %) | 2084 / 1509 / 919 |

## Detached against legato (the aa / ab riffs, notes 2-8, first 100 ms, FX off): centroid Hz and level

| var | detached with sweep | detached no sweep | legato with sweep | legato no sweep | sweep adds: detached / legato (Hz) | level detached / legato (dB) |
|---|---|---|---|---|---|---|
| A | 3349 | 2587 | 1755 | 1575 | +762 / +180 | -22.0 / -24.0 |
| B | 4588 | 3870 | 1593 | 1427 | +718 / +166 | -17.4 / -19.0 |
| C | 3235 | 2904 | 1752 | 1594 | +331 / +158 | -17.6 / -19.3 |
| D | 2935 | 2632 | 1742 | 1568 | +303 / +174 | -17.8 / -19.3 |
| E52 | 2932 | 2630 | 1813 | 1623 | +302 / +190 | -17.7 / -19.2 |
| F70 | 2985 | 2684 | 2032 | 1813 | +301 / +219 | -17.8 / -19.2 |
| Droom | 2935 | 2632 | 1742 | 1568 | +303 / +174 | -17.8 / -19.3 |

## The held A3 (4 s, FX off): centroid after the strike, the level, the stack's beat

| var | centroid 0-150 / 150-400 / 400-1000 / 1000-2500 / 2500-4000 ms | RMS 0-400 / 400-1000 / 1000-2500 / 2500-4000 ms | beat rate Hz (mean, min-max), depth dB |
|---|---|---|---|
| A | 1890 / 1086 / 983 / 981 / 981 | -23.0 / -23.6 / -23.6 / -23.6 | 4.34 (0.34-11.94), 0.1 |
| B | 3329 / 1049 / 901 / 886 / 860 | -20.8 / -19.4 / -18.4 / -18.3 | 1.04 (0.34-1.51), 17.6 |
| C | 2624 / 1115 / 1036 / 1029 / 1004 | -19.4 / -19.3 / -18.8 / -18.5 | 1.01 (0.34-1.51), 17.0 |
| D | 2420 / 1112 / 1041 / 1042 / 1021 | -19.2 / -19.3 / -18.8 / -18.5 | 0.99 (0.34-1.68), 16.9 |
| E52 | 2429 / 1156 / 1088 / 1098 / 1078 | -19.0 / -19.1 / -18.6 / -18.3 | 1.03 (0.34-1.85), 16.7 |
| F70 | 2516 / 1327 / 1259 / 1288 / 1269 | -18.8 / -19.1 / -18.6 / -18.2 | 1.30 (0.34-2.36), 17.3 |
| Droom | 2420 / 1112 / 1041 / 1042 / 1021 | -19.2 / -19.3 / -18.8 / -18.5 | 0.99 (0.34-1.68), 16.9 |

## Fatness (the fat base, GROWL 0, dry, VOLUME 100): voices and detune against beat, level and cost

| voices | DETUNE | beat rate Hz | beat depth dB | level (d_lead) | crest | CPU |
|---|---|---|---|---|---|---|
| 1 (MONO) | 0 | 5.48 | 0.0 | -20.9 | 10.0 | 1355 |
| 2 | 22 | 0.99 | 38.8 | -17.9 | 11.9 | 1543 |
| 3 | 22 | 1.04 | 17.2 | -16.0 | 11.7 | 1732 |
| 4 | 22 | 1.01 | 10.3 | -14.6 | 11.0 | 1920 |
| 3 | 40 | 1.97 | 19.2 | -16.3 | 11.8 | 1732 |

## Rip depth (ENV>O2 stepped on the fat base, GROWL 0, dry): the semitones at the top of the envelope are (value - 64) x 24 / 63

| ENV>O2 | st at the top | centroid 0-50 / 50-150 / 150-400 ms | 1.2k+ share |
|---|---|---|---|
| 80 | +6.1 | 3507 / 1772 / 912 | 24 % / 17 % / 5 % |
| 88 | +9.1 | 3634 / 1984 / 960 | 25 % / 18 % / 6 % |
| 104 | +15.2 | 4165 / 1961 / 1049 | 54 % / 25 % / 10 % |
| 116 | +19.8 | 4203 / 1983 / 1107 | 30 % / 21 % / 11 % |
| 127 | +24.0 | 4235 / 1957 / 1124 | 37 % / 23 % / 9 % |

## Glide: GLIDE 20 -> 50 on the fat variants: a legato octave step reaches within 50 cents in 64 ms (90 % of the octave in 39 ms); the original's GLIDE 20 measured 4 ms (no glide).
