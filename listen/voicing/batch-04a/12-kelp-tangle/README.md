# Batch 4A, 12 Kelp Tangle: variants and numbers

Chapter II (The Tidal Hexes). Round 1, **rendered, not yet heard**. Method and definitions: `dog5-docs/voicing/README.md` section 15. Level phrase: `r_tangle` (own phrase, effects included, tails excluded), reference -18.0 dBFS RMS +-1.5, peak <= -4. WAVs (`<dir>_<KEY>_<organ|tangle|wash|stabs>.wav`) are on the never-merged listen branch only.

## Variants

* **A original**: the nearest-base patch as it stood (HOLLOW PAD: narrow inverse pulses through a notch, PWM +-2 points: not audible as PWM).
* **B murk** (RECOMMENDED, committed): murk first: LP24 CUTOFF 86 at 100 % key tracking, RESO 30, PWM +-15 points around 33 % (18-48 %), TRI 1.03 Hz, PHASE SYNC, spring DRAIN 55.
* **C open**: B along the cutoff axis: CUTOFF 98 (more of each note's harmonics through the filter).
* **D tangle**: B along the rate / depth axis: PWM +-16.8 points, TRI 2.3 Hz, PHASE SPREAD (each voice 45 degrees on).

## Numbers

| | A original | B murk | C open | D tangle |
|---|---|---|---|---|
| VOLUME | 100 | 75 | 74 | 76 |
| level, tangle phrase (r) (dBFS RMS, note-on region, effects in, tails out; reference -18.0 +-1.5) | -19.42 | -17.99 | -17.99 | -17.88 |
| phrase (b) RMS (dBFS) / minus the level phrase (dB) | -17.6 / +1.8 | -17.0 / +1.0 | -17.0 / +1.0 | -17.1 / +0.7 |
| peak, whole renders (dBFS; limit -4) | -4.8 | -5.3 | -5.3 | -5.0 |
| crest factor, level phrase (dB) | 14.4 | 12.7 | 12.7 | 12.9 |
| K-weighted RMS, (b) (dBFS) | -17.7 | -17.7 | -17.6 | -17.7 |
| amp attack (probe, one voice, LFO off): 10 / 50 / 90 % of the plateau (ms) | 6 / 29 / 61 | 3 / 11 / 24 | 3 / 11 / 23 | 3 / 11 / 24 |
| AA byte -> the time table's nominal (ms) | 70 -> 117 | 52 -> 29 | 52 -> 29 | 52 -> 29 |
| note-on region: centroid (Hz) | 4456 | 504 | 808 | 513 |
| note-on region: band split % <60 / 60-150 / 150-400 / 400-1.2k / 1.2k+ | 0 / 32 / 48 / 7 / 13 | 0 / 43 / 45 / 10 / 1 | 0 / 41 / 43 / 13 / 3 | 0 / 44 / 43 / 12 / 1 |
| MUD = share(150-400) / share(1.2k+), note-on region | 3.7 | 38.8 | 12.3 | 37.2 |
| worst-case CPU (host instr/sample: idle + load) | 2020 (1164 + 856) | 2042 (1164 + 878) | 2042 (1164 + 878) | 2047 (1164 + 883) |
| LFO: shape / rate (Hz, law) / PWM / phase | TRI / 0.37 / 16 % +-2.3 pts (14-18 %) / SPREAD | TRI / 1.03 / 33 % +-15.2 pts (18-48 %) / SYNC | TRI / 1.03 / 33 % +-15.2 pts (18-48 %) / SYNC | TRI / 2.30 / 33 % +-16.8 pts (16-50 %) / SPREAD |
| filter: type / CUTOFF (Hz at C4, key tracking %) / RESO | NOTCH / 740 / 50 / 20 | LP24 / 1865 / 100 / 30 | LP24 / 3729 / 100 / 30 | LP24 / 1865 / 100 / 30 |
| held A2, dry (after the filter): centroid (Hz) / % <150 / % 150-400 / % 400-1.2k / % 1.2k+ | 4222 / 53 / 35 / 3.6 / 8.6 | 339 / 72 / 24 / 4.6 / 0.0 | 531 / 69 / 23 / 7.2 / 0.8 | 338 / 75 / 20 / 4.7 / 0.0 |
| held A2, dry: PWM depth by band 150-400 / 400-1.2k / 1.2k-3k / 3k+ (dB, 95th-5th pct of 23 ms band energy) | 14.4 / 5.5 / 2.7 / 1.5 | 10.1 / 9.8 / 11.1 / 14.8 | 10.1 / 7.6 / 7.4 / 4.3 | 10.1 / 8.4 / 9.2 / 14.3 |
| held A2, dry: strongest modulation rate by band (Hz) | 1.2 / 2.4 / 9.6 / 19.1 | 0.9 / 1.6 / 4.8 / 1.1 | 0.9 / 1.6 / 4.8 / 12.4 | 0.8 / 4.8 / 16.1 / 2.8 |
| held A2: level modulation dry (dB) / as rendered with the spring (dB) | 10.1 / 9.9 | 5.9 / 6.1 | 5.7 / 5.9 | 7.8 / 8.2 |
| held chord A2+E3+C4, dry: centroid (Hz) / % 1.2k+ | 4578 / 13.5 | 540 / 1.2 | 879 / 3.5 | 553 / 1.2 |
| held chord, dry: PWM depth by band (dB) | 6.9 / 9.2 / 2.9 / 1.9 | 8.9 / 7.1 / 7.8 / 7.1 | 9.0 / 6.4 / 5.6 / 4.4 | 9.0 / 6.2 / 7.7 / 7.5 |
| held chord: level modulation dry (dB) | 3.5 | 4.4 | 4.3 | 5.1 |
| short notes (150 ms, three of them): PWM depth, 150-400 / 400-1.2k / level (dB) | 3.4 / 3.3 / 2.3 | 2.2 / 1.7 / 2.1 | 2.2 / 1.5 / 1.9 | 2.3 / 4.7 / 2.2 |
| spring (DRAIN, SIZE, DAMP, PRE-DLY) | 40 (31 %), 100, 60, 20 | 55 (43 %), 75, 30, 20 | 55 (43 %), 75, 30, 20 | 55 (43 %), 75, 30, 20 |
| spring return re the dry chord after its note-on, windows 0-20 / 20-100 / 100-250 ms (dB) | -47.9 / -18.3 / -8.3 | -48.1 / -12.9 / -5.9 | -47.1 / -12.8 / -5.9 | -43.7 / -12.1 / -4.6 |
| same on the held A2 | -46.7 / -23.2 / -16.3 | -41.2 / -19.2 / -20.2 | -40.5 / -18.7 / -19.0 | -42.7 / -17.5 / -15.0 |
| spring tail after the chord's note-off: return re the chord's level (dB), windows 0-250 / 250-750 / 750-1500 / 1500-1800 ms | -9.3 / -7.2 / -16.0 / -38.6 | -7.7 / -12.8 / -33.6 / -85.7 | -7.5 / -12.9 / -33.8 / -85.8 | -8.2 / -13.7 / -32.8 / -81.6 |
| the tail's band split, same windows: MUD (150-400 / 1.2k+) / centroid (Hz) / level (dB) | 6 / 4542 / -20 ; 4 / 4358 / -25 ; 8 / 4115 / -35 | 29 / 576 / -20 ; 39 / 642 / -31 ; 180 / 1507 / -52 | 10 / 921 / -20 ; 15 / 927 / -31 ; 77 / 1565 / -52 | 30 / 594 / -20 ; 29 / 682 / -32 ; 95 / 1425 / -52 |
| tail after the chord (to -20 / -40 / -60 dB, ms, DC out) | 1174 / 1800 / >win | 632 / 1102 / 1432 | 632 / 1100 / 1426 | 598 / 1112 / 1446 |
| tail after the held A2 / after the short-note figure (to -60 dB, ms) | >win / 2294 | 960 / 1052 | 978 / 1054 | 994 / 1092 |

## Parameter changes, each before -> after (the original is the nearest-base patch as it stood; variant A is that patch)

### B murk

* O1_PW 20 -> 42 (+17%)
* O2_PW 108 -> 42 (-52%)
* O2_FINE 76 -> 73 (centre 64: +12 -> +9, -2% of range) (+9.4 cents -> +7.0 cents)
* CUTOFF 70 -> 86 (+13%) (740 Hz -> 1865 Hz)
* RESO 20 -> 30 (+8%)
* KEYTRK 64 -> 127 (+50%)
* FTYPE NOTCH -> LP24
* AA 70 -> 52 (-14%) (117 ms -> 29 ms)
* AS 100 -> 127 (+21%)
* AR 100 -> 88 (-9%) (1218 ms -> 478 ms)
* LFO_RATE 40 -> 60 (+16%) (0.4 Hz -> 1.0 Hz)
* LFO_PHASE SPREAD -> SYNC
* LFO_PWM 40 -> 100 (+47%)
* VINTAGE 30 -> 50 (+16%)
* VOLUME 100 -> 75 (-20%)
* REV_SIZE 100 -> 75 (-20%)
* REV_DAMP 60 -> 30 (-24%)
* REV_MIX 40 -> 55 (+12%)

### C open

* O1_PW 20 -> 42 (+17%)
* O2_PW 108 -> 42 (-52%)
* O2_FINE 76 -> 73 (centre 64: +12 -> +9, -2% of range) (+9.4 cents -> +7.0 cents)
* CUTOFF 70 -> 98 (+22%) (740 Hz -> 3729 Hz)
* RESO 20 -> 30 (+8%)
* KEYTRK 64 -> 127 (+50%)
* FTYPE NOTCH -> LP24
* AA 70 -> 52 (-14%) (117 ms -> 29 ms)
* AS 100 -> 127 (+21%)
* AR 100 -> 88 (-9%) (1218 ms -> 478 ms)
* LFO_RATE 40 -> 60 (+16%) (0.4 Hz -> 1.0 Hz)
* LFO_PHASE SPREAD -> SYNC
* LFO_PWM 40 -> 100 (+47%)
* VINTAGE 30 -> 50 (+16%)
* VOLUME 100 -> 74 (-20%)
* REV_SIZE 100 -> 75 (-20%)
* REV_DAMP 60 -> 30 (-24%)
* REV_MIX 40 -> 55 (+12%)

C against B:

* CUTOFF 86 -> 98 (+9%) (1865 Hz -> 3729 Hz)

### D tangle

* O1_PW 20 -> 42 (+17%)
* O2_PW 108 -> 42 (-52%)
* O2_FINE 76 -> 73 (centre 64: +12 -> +9, -2% of range) (+9.4 cents -> +7.0 cents)
* CUTOFF 70 -> 86 (+13%) (740 Hz -> 1865 Hz)
* RESO 20 -> 30 (+8%)
* KEYTRK 64 -> 127 (+50%)
* FTYPE NOTCH -> LP24
* AA 70 -> 52 (-14%) (117 ms -> 29 ms)
* AS 100 -> 127 (+21%)
* AR 100 -> 88 (-9%) (1218 ms -> 478 ms)
* LFO_RATE 40 -> 76 (+28%) (0.4 Hz -> 2.3 Hz)
* LFO_PWM 40 -> 105 (+51%)
* VINTAGE 30 -> 50 (+16%)
* VOLUME 100 -> 76 (-19%)
* REV_SIZE 100 -> 75 (-20%)
* REV_DAMP 60 -> 30 (-24%)
* REV_MIX 40 -> 55 (+12%)

D against B:

* LFO_RATE 60 -> 76 (+13%) (1.0 Hz -> 2.3 Hz)
* LFO_PHASE SYNC -> SPREAD
* LFO_PWM 100 -> 105 (+4%)

