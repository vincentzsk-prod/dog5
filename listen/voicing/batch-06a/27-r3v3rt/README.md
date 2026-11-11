# 27 R3V3RT, Batch 6A round 1 (rendered, not yet heard)

Level phrase: the note-on region of `a_riff` (the low chopped riff, gate 150 ms); the standard stabs phrase (b) is shown for the difference. Dry, MONO.

| var | tag | VOLUME | level (a_riff) | peak | (b) stabs | (b) - level | CPU | what |
|---|---|---|---|---|---|---|---|---|
| A | original | 100 | -20.33 | -13.8 | -20.9 | -0.5 | 1377 | the original through the base program path |
| B | sus70 | 105 | -18.07 | -12.5 | -18.6 | -0.5 | 1378 | the base, AMP SUSTAIN 70 |
| C | sus90 | 100 | -18.05 | -13.5 | -18.5 | -0.5 | 1378 | the base, AMP SUSTAIN 90 |
| D | sus110 | 96 | -17.97 | -14.0 | -18.4 | -0.4 | 1378 | the base, AMP SUSTAIN 110 |
| Ebite | bite | 105 | -17.98 | -12.3 | -18.2 | -0.2 | 1378 | calibration: C with a narrower pulse (PW 38 = 30 %), CUTOFF 74, FILTER DECAY 70 |
| Fround | round | 102 | -18.01 | -13.5 | -19.0 | -1.0 | 1378 | calibration: C with a square pulse (PW 64 = 50 %), CUTOFF 58, FILTER DECAY 50 |
| Glong | longdecay | 98 | -18.00 | -13.8 | -18.0 | -0.0 | 1379 | calibration: C with a longer filter decay (FD 85) |

**Every change over the original (percent = of the parameter's range):**

* **B sus70:** O1_WAVE saw -> pulse; O1_PW 64 -> 54 (-8%); O1_LVL 110 -> 120 (+8%); O2_WAVE pulse -> off; O2_LVL 100 -> 0 (-79%); CUTOFF 40 -> 66 (+20%); RESO 30 -> 0 (-24%); FENV_AMT 109 -> 118 (+7%); KEYTRK 64 -> 30 (-27%); DRIVE 40 -> 30 (-8%); FA 20 -> 0 (-16%); FS 10 -> 0 (-8%); FR 60 -> 20 (-31%); AA 2 -> 0 (-2%); AD 70 -> 80 (+8%); AS 100 -> 70 (-24%); VOLUME 100 -> 105
* **C sus90:** O1_WAVE saw -> pulse; O1_PW 64 -> 54 (-8%); O1_LVL 110 -> 120 (+8%); O2_WAVE pulse -> off; O2_LVL 100 -> 0 (-79%); CUTOFF 40 -> 66 (+20%); RESO 30 -> 0 (-24%); FENV_AMT 109 -> 118 (+7%); KEYTRK 64 -> 30 (-27%); DRIVE 40 -> 30 (-8%); FA 20 -> 0 (-16%); FS 10 -> 0 (-8%); FR 60 -> 20 (-31%); AA 2 -> 0 (-2%); AD 70 -> 80 (+8%); AS 100 -> 90 (-8%); VOLUME 100 -> 100
* **D sus110:** O1_WAVE saw -> pulse; O1_PW 64 -> 54 (-8%); O1_LVL 110 -> 120 (+8%); O2_WAVE pulse -> off; O2_LVL 100 -> 0 (-79%); CUTOFF 40 -> 66 (+20%); RESO 30 -> 0 (-24%); FENV_AMT 109 -> 118 (+7%); KEYTRK 64 -> 30 (-27%); DRIVE 40 -> 30 (-8%); FA 20 -> 0 (-16%); FS 10 -> 0 (-8%); FR 60 -> 20 (-31%); AA 2 -> 0 (-2%); AD 70 -> 80 (+8%); AS 100 -> 110 (+8%); VOLUME 100 -> 96
* **Ebite bite:** O1_WAVE saw -> pulse; O1_PW 64 -> 38 (-20%); O1_LVL 110 -> 120 (+8%); O2_WAVE pulse -> off; O2_LVL 100 -> 0 (-79%); CUTOFF 40 -> 74 (+27%); RESO 30 -> 0 (-24%); FENV_AMT 109 -> 118 (+7%); KEYTRK 64 -> 30 (-27%); DRIVE 40 -> 30 (-8%); FA 20 -> 0 (-16%); FD 60 -> 70 (+8%); FS 10 -> 0 (-8%); FR 60 -> 20 (-31%); AA 2 -> 0 (-2%); AD 70 -> 80 (+8%); AS 100 -> 90 (-8%); VOLUME 100 -> 105
* **Fround round:** O1_WAVE saw -> pulse; O1_LVL 110 -> 120 (+8%); O2_WAVE pulse -> off; O2_LVL 100 -> 0 (-79%); CUTOFF 40 -> 58 (+14%); RESO 30 -> 0 (-24%); FENV_AMT 109 -> 118 (+7%); KEYTRK 64 -> 30 (-27%); DRIVE 40 -> 30 (-8%); FA 20 -> 0 (-16%); FD 60 -> 50 (-8%); FS 10 -> 0 (-8%); FR 60 -> 20 (-31%); AA 2 -> 0 (-2%); AD 70 -> 80 (+8%); AS 100 -> 90 (-8%); VOLUME 100 -> 102
* **Glong longdecay:** O1_WAVE saw -> pulse; O1_PW 64 -> 54 (-8%); O1_LVL 110 -> 120 (+8%); O2_WAVE pulse -> off; O2_LVL 100 -> 0 (-79%); CUTOFF 40 -> 66 (+20%); RESO 30 -> 0 (-24%); FENV_AMT 109 -> 118 (+7%); KEYTRK 64 -> 30 (-27%); DRIVE 40 -> 30 (-8%); FA 20 -> 0 (-16%); FD 60 -> 85 (+20%); FS 10 -> 0 (-8%); FR 60 -> 20 (-31%); AA 2 -> 0 (-2%); AD 70 -> 80 (+8%); AS 100 -> 90 (-8%); VOLUME 100 -> 98

## A2 (45), held 1 s from silence, FX off: level re the peak (first 60 ms), the run-off, the centroid, the band shares

| var | level re peak at 20 / 50 / 100 / 300 / 600 ms (dB) | key-up to -20 / -40 / -60 dB (ms) | centroid 0-20 / 20-100 / 100-300 ms (Hz) | snap: peak centroid / lasts (ms) | bands 0-400 ms: <60 / 60-150 / 150-400 / 400-1.2k / 1.2k+ (%) | body 100-400 ms: same | above 60 Hz (body, %) |
|---|---|---|---|---|---|---|---|
| A | -3.7 / -3.5 / -4.4 / -5.0 / -5.0 | 11 / 15 / 17 | 246 / 116 / 114 | 346 / 5 | 42 / 56 / 1 / 0 / 0 | 43 / 57 / 0 / 0 / 0 | 7 |
| B | -1.0 / -2.5 / -4.1 / -5.8 / -6.0 | 11 / 15 / 19 | 1209 / 264 / 227 | 1573 / 30 | 2 / 89 / 8 / 2 / 0 | 2 / 90 / 7 / 1 / 0 | 98 |
| C | -0.8 / -1.9 / -2.9 / -3.8 / -3.9 | 11 / 15 / 19 | 1203 / 262 / 224 | 1572 / 30 | 2 / 89 / 7 / 2 / 0 | 2 / 90 / 7 / 1 / 0 | 98 |
| D | -0.5 / -1.3 / -1.9 / -2.2 / -2.3 | 11 / 15 / 19 | 1198 / 259 / 222 | 1570 / 30 | 2 / 89 / 7 / 2 / 0 | 2 / 90 / 7 / 1 / 0 | 98 |
| Ebite | -0.9 / -1.6 / -2.6 / -3.8 / -3.8 | 11 / 15 / 19 | 2903 / 664 / 286 | 3010 / 75 | 8 / 64 / 21 / 5 / 1 | 9 / 66 / 21 / 4 / 0 | 91 |
| Fround | -1.5 / -2.7 / -3.4 / -4.3 / -4.4 | 11 / 15 / 19 | 340 / 185 / 191 | 417 / 10 | 0 / 98 / 2 / 0 / 0 | 0 / 98 / 2 / 0 / 0 | 100 |
| Glong | -0.6 / -1.2 / -2.0 / -3.4 / -3.9 | 11 / 15 / 19 | 2828 / 1759 / 440 | 2891 / 175 | 1 / 82 / 9 / 6 / 1 | 1 / 84 / 9 / 5 / 0 | 99 |

## A1 (33), held 1 s from silence, FX off: level re the peak (first 60 ms), the run-off, the centroid, the band shares (A1: the band columns use 2048-point frames whose Hann lobe smears the 55 Hz fundamental over 60-150 Hz; the last column, one 350 ms window, is the one to read)

| var | level re peak at 20 / 50 / 100 / 300 / 600 ms (dB) | key-up to -20 / -40 / -60 dB (ms) | centroid 0-20 / 20-100 / 100-300 ms (Hz) | snap: peak centroid / lasts (ms) | bands 0-400 ms: <60 / 60-150 / 150-400 / 400-1.2k / 1.2k+ (%) | body 100-400 ms: same | above 60 Hz (body, %) |
|---|---|---|---|---|---|---|---|
| A | -1.2 / -1.7 / -4.2 / -4.1 / -2.7 | 10 / 16 / 20 | 71 / 89 / 81 | 279 / 0 | 90 / 9 / 0 / 0 / 0 | 92 / 8 / 0 / 0 / 0 | 1 |
| B | -0.9 / -2.2 / -3.5 / -5.1 / -5.3 | 11 / 15 / 19 | 554 / 180 / 151 | 698 / 15 | 41 / 49 / 9 / 1 / 0 | 41 / 50 / 8 / 0 / 0 | 13 |
| C | -0.7 / -1.5 / -2.3 / -3.2 / -3.3 | 11 / 15 / 19 | 551 / 176 / 148 | 699 / 15 | 41 / 49 / 9 / 1 / 0 | 41 / 50 / 8 / 0 / 0 | 13 |
| D | -0.4 / -0.9 / -1.4 / -1.7 / -1.7 | 11 / 15 / 19 | 548 / 173 / 147 | 700 / 15 | 41 / 50 / 9 / 1 / 0 | 41 / 50 / 8 / 0 / 0 | 13 |
| Ebite | -0.7 / -1.4 / -2.3 / -3.2 / -3.3 | 11 / 15 / 19 | 1695 / 504 / 207 | 2552 / 15 | 37 / 54 / 7 / 2 / 0 | 37 / 55 / 6 / 1 / 0 | 29 |
| Fround | -1.0 / -1.8 / -2.5 / -3.4 / -3.5 | 11 / 15 / 18 | 149 / 119 / 121 | 255 / 5 | 44 / 50 / 7 / 0 / 0 | 43 / 50 / 7 / 0 / 0 | 7 |
| Glong | -0.5 / -1.1 / -1.9 / -3.0 / -3.3 | 11 / 15 / 19 | 1795 / 1317 / 305 | 2671 / 70 | 39 / 47 / 11 / 3 / 1 | 39 / 48 / 11 / 2 / 0 | 17 |

## Legato (the ag / ah bass lines, notes 2-8, FX off): detached against legato

| var | first 20 ms level det / leg (dB) | 0-100 ms level det / leg | 100-300 ms level det / leg | centroid first 20 ms det / leg (Hz) | centroid 20-100 ms det / leg |
|---|---|---|---|---|---|
| A | -18.3 / -21.2 | -19.8 / -21.3 | -21.1 / -21.2 | 218 / 92 | 91 / 94 |
| B | -15.6 / -20.9 | -17.2 / -20.9 | -20.0 / -20.9 | 988 / 156 | 219 / 180 |
| C | -16.3 / -19.5 | -17.4 / -19.6 | -19.1 / -19.6 | 1078 / 153 | 214 / 176 |
| D | -16.8 / -18.5 | -17.5 / -18.5 | -18.3 / -18.5 | 989 / 152 | 211 / 174 |
| Ebite | -16.4 / -19.5 | -17.3 / -19.5 | -19.0 / -19.5 | 1915 / 196 | 589 / 224 |
| Fround | -16.0 / -19.4 | -17.4 / -19.5 | -19.0 / -19.5 | 379 / 125 | 145 / 147 |
| Glong | -16.6 / -19.9 | -17.4 / -19.9 | -19.0 / -19.9 | 2200 / 154 | 1600 / 178 |

## Probes on C (one control stepped; A2 body = centroid 150-400 ms, snap peak = the highest 12 ms centroid, A1 share = % of the 50-400 ms energy above 60 Hz)

| control | value | A2 body Hz | A2 snap peak Hz | snap lasts ms | A1 above 60 Hz % | A1 body Hz | CPU |
|---|---|---|---|---|---|---|---|
| DRIVE | 0 | 232 | 1483 | 30 | 13 | 150 | 1361 |
| DRIVE | 30 | 224 | 1572 | 30 | 13 | 150 | 1378 |
| DRIVE | 60 | 214 | 1637 | 30 | 12 | 147 | 1374 |
| DRIVE | 100 | 213 | 1674 | 30 | 12 | 147 | 1368 |
| O1_PW | 38 | 216 | 1680 | 30 | 26 | 156 |  |
| O1_PW | 46 | 219 | 1601 | 30 | 18 | 152 |  |
| O1_PW | 54 | 224 | 1572 | 30 | 13 | 150 |  |
| O1_PW | 64 | 225 | 1472 | 30 | 10 | 151 |  |
| KEYTRK | 0 | 247 | 1877 | 30 | 15 | 184 |  |
| KEYTRK | 30 | 224 | 1572 | 30 | 13 | 150 |  |
| KEYTRK | 64 | 203 | 1312 | 30 | 9 | 126 |  |
| KEYTRK | 100 | 188 | 1098 | 30 | 5 | 113 |  |
| CUTOFF | 58 | 189 | 1107 | 30 | 9 | 124 |  |
| CUTOFF | 66 | 224 | 1572 | 30 | 13 | 150 |  |
| CUTOFF | 74 | 285 | 2123 | 30 | 16 | 196 |  |
| FD | 40 | 224 | 269 | 0 | 13 | 150 |  |
| FD | 60 | 224 | 1572 | 30 | 13 | 150 |  |
| FD | 85 | 321 | 2891 | 175 | 17 | 222 |  |
