# Batch 4A, 16 Tidal Pull: variants and numbers

Chapter II (The Tidal Hexes). Round 1, **rendered, not yet heard**. Method and definitions: `dog5-docs/voicing/README.md` section 15. Level phrase: `s_wash` (own phrase, effects included, tails excluded), reference -18.0 dBFS RMS +-1.5, peak <= -4. WAVs (`<dir>_<KEY>_<organ|tangle|wash|stabs>.wav`) are on the never-merged listen branch only.

## Variants

* **A original**: the nearest-base patch as it stood (PWM STRINGS, shared with 13 Ghost Board: no delay, spring only, inert LFO PITCH 3).
* **B tri** (RECOMMENDED, committed): TRI LFO 1.26 Hz on pitch +-19 cents and the pulse widths, pulses, attack 101 ms to 90 %, the echo ahead of the spring (DLY MIX 100, DRAIN 45).
* **C random**: smooth RANDOM LFO ~1.7 Hz, attack 160 ms, the spring ahead of the echo (DRAIN 65, DLY MIX 90).
* **D soft**: the oscillators softened toward a triangle (narrow pulses through a key-tracking low-pass, an octave stack), TRI 2.3 Hz, attack 219 ms, echo up (MIX 110).

## Numbers

| | A original | B tri | C random | D soft |
|---|---|---|---|---|
| VOLUME | 100 | 63 | 65 | 76 |
| level, wash phrase (s) (dBFS RMS, note-on region, effects in, tails out; reference -18.0 +-1.5) | -11.79 | -18.07 | -17.96 | -19.13 |
| phrase (b) RMS (dBFS) / minus the level phrase (dB) | -14.2 / -2.4 | -21.6 / -3.5 | -22.2 / -4.2 | -26.8 / -7.6 |
| peak, whole renders (dBFS; limit -4) | -0.2 | -4.4 | -4.3 | -4.4 |
| crest factor, level phrase (dB) | 11.6 | 13.7 | 13.6 | 14.7 |
| K-weighted RMS, (b) (dBFS) | -14.8 | -22.1 | -22.7 | -27.5 |
| amp attack (probe, one voice, LFO off): 10 / 50 / 90 % of the plateau (ms) | 3 / 14 / 27 | 9 / 44 / 101 | 14 / 69 / 160 | 17 / 93 / 219 |
| AA byte -> the time table's nominal (ms) | 60 -> 54 | 72 -> 137 | 78 -> 219 | 82 -> 299 |
| note-on region: centroid (Hz) | 593 | 1609 | 1644 | 595 |
| note-on region: band split % <60 / 60-150 / 150-400 / 400-1.2k / 1.2k+ | 0 / 0 / 81 / 18 / 1 | 0 / 0 / 67 / 26 / 7 | 0 / 0 / 66 / 26 / 9 | 0 / 0 / 73 / 26 / 1 |
| MUD = share(150-400) / share(1.2k+), note-on region | 115.0 | 9.8 | 7.6 | 133.2 |
| worst-case CPU (host instr/sample: idle + load) | 2069 (1164 + 905) | 2026 (1180 + 847) | 2025 (1179 + 845) | 2027 (1180 + 847) |
| LFO: shape / rate (Hz, law) / pitch +-cents (law) / PWM +-points / phase | TRI / 0.62 / 0 / 5.5 / SPREAD | TRI / 1.26 / 19 / 9.8 / SPREAD | RANDOM / 1.70 / 19 / 9.8 / SPREAD | TRI / 2.30 / 19 / 0.0 / SPREAD |
| pitch probe (one voice, audio): wander s.d. / 5-95 % range (cents) / strongest rate (Hz) | 0.0 / 0.0 / 7.95 | 10.4 / 32.8 / 1.25 | 8.1 / 28.5 / 0.31 | 10.6 / 32.3 / 2.30 |
| oscillators: PW O1 / O2 (%), O2 semis, FINE (cents), triangle probe H3 / H5 / H7 re H1 of OSC 1 at rest (dB; triangle -19.1 / -28.0 / -34.2, square -9.5 / -14.0 / -16.9) | 50 / 32, +0, +7.0; -10.9 / -18.4 / -26.0 | 35 / 24, +0, +7.0; -26.0 / -16.1 / -16.9 | 35 / 24, +0, +7.0; -26.1 / -16.1 / -16.9 | 25 / 25, +12, +1.6; -17.2 / -27.3 / -36.8 |
| filter: type / CUTOFF (Hz at C4) / key tracking % | LP24 / 988 / 50 | LP12 / 4186 / 79 | LP12 / 4186 / 79 | LP12 / 523 / 100 |
| width, held chord: L/R correlation 150-4k Hz dry (full) / side-to-mid dry (dB) | 0.80 (0.80) / -9.5 | 0.70 (0.55) / -7.6 | 0.70 (0.44) / -7.5 | 0.70 (0.66) / -7.6 |
| chorus beating, A3 band of the held chord, dry: rate mean (min-max) Hz / envelope depth (dB) | 1.12 (1.01-1.18) / 17.7 | 0.90 (0.67-1.18) / 12.9 | 1.01 (0.84-1.18) / 15.4 | 2.24 (1.68-2.52) / 0.6 |
| brightness (voice, held chord dry): centroid (Hz) / MUD / share 1.2k+ % | 610 / 87.6 / 0.9 | 1733 / 7.8 / 7.9 | 1661 / 9.3 / 7.4 | 642 / 81.8 / 0.8 |
| delay: ALLEY (ms) / FEEDBK / MIX / PINGPONG | 10 / 50 / 0 / 127 | 337 / 78 / 100 / 127 | 337 / 78 / 90 / 127 | 337 / 78 / 110 / 127 |
| first repeat of an isolated 400 ms E4: peak re the dry note's peak (dB) / peak at ms after the note-on | - / -20 | -9.4 / 566 | -10.5 / 531 | -8.6 / 601 |
| spring in the same window re the note (dB); the delay's margin over the spring (dB) | -18.1 ; - | -16.0 ; 6.6 | -14.7 ; 4.2 | -16.3 ; 7.7 |
| the repeats 1..6 (dB re the first, one slot of a delay time each) | +0.0 +0.0 +0.0 +0.0 +0.0 +0.0 | +0.0 -0.6 -4.8 -10.8 -15.9 -20.9 | +0.0 -1.5 -5.6 -10.9 -15.9 -20.7 | +0.0 -0.2 -4.1 -8.7 -13.5 -18.6 |
| the first repeat's spectrum: centroid (Hz) / MUD | 0 / 0.0 | 1030 / 18.5 | 1010 / 20.2 | 696 / 56.8 |
| echo under the figure's three 400 ms notes (dB re the note) | - / - / - | -20.9 / -14.4 / -16.8 | -24.9 / -13.8 / -17.4 | -27.3 / -10.3 / -13.2 |
| spring under the same notes (dB) | -18.4 / -18.1 / -17.2 | -13.1 / -12.7 / -14.9 | -9.4 / -12.0 / -11.5 | -15.0 / -15.2 / -15.1 |
| isolated E4, spring return re the note, 0-20 / 20-100 / 100-250 ms (dB) | -45.9 / -19.1 / -19.0 | -46.0 / -20.3 / -16.4 | -42.5 / -18.3 / -14.2 | -38.8 / -19.1 / -14.4 |
| after the held chord's note-off: delay return re the chord (dB), 0-100 / 100-250 / 250-500 / 500-1000 / 1000-2000 ms | - / - / - / - / - | -6.9 / -7.7 / -8.8 / -13.4 / -22.8 | -6.7 / -7.2 / -9.5 / -14.7 / -23.7 | -5.9 / -6.4 / -7.2 / -11.8 / -21.3 |
| same, spring return (dB) | -2.7 / -2.4 / -5.0 / -13.4 / -29.6 | -10.2 / -7.5 / -9.8 / -22.7 / -41.4 | -4.0 / -6.9 / -12.7 / -24.0 / -42.3 | -6.5 / -8.8 / -11.5 / -18.9 / -37.3 |
| spring (DRAIN, SIZE, DAMP) | 35 (28 %), 100, 60 | 45 (35 %), 90, 35 | 65 (51 %), 90, 35 | 45 (35 %), 90, 35 |
| the tail after the chord: MUD / centroid (Hz) / level (dB re full scale) in 0-250 / 250-750 / 750-1500 ms | 696 / 559 / -13 ; 3094 / 490 / -20 ; 7874 / 609 / -34 | 9 / 1675 / -20 ; 21 / 1288 / -26 ; 25 / 973 / -35 | 2 / 1894 / -20 ; 8 / 1419 / -26 ; 11 / 1097 / -36 | 177 / 596 / -19 ; 407 / 571 / -24 ; 689 / 598 / -32 |
| tail after the held chord (to -20 / -40 / -60 dB, ms, DC out) | 878 / 1574 / 2146 | 1112 / 2452 / >win | 1070 / 2422 / >win | 1216 / 2404 / >win |

## Parameter changes, each before -> after (the original is the nearest-base patch as it stood; variant A is that patch)

### B tri

* O1_PW 64 -> 44 (-16%)
* O2_PW 40 -> 30 (-8%)
* CUTOFF 75 -> 100 (+20%) (988 Hz -> 4186 Hz)
* RESO 5 -> 8 (+2%)
* FENV_AMT 74 -> 64 (centre 64: +10 -> +0, -8% of range)
* KEYTRK 64 -> 100 (+28%)
* FTYPE LP24 -> LP12
* FA 50 -> 20 (-24%) (25 ms -> 2 ms)
* AA 60 -> 72 (+9%) (54 ms -> 137 ms)
* AS 100 -> 127 (+21%)
* AR 90 -> 92 (+2%) (558 ms -> 653 ms)
* LFO_RATE 50 -> 64 (+11%) (0.6 Hz -> 1.3 Hz)
* LFO_PITCH 3 -> 16 (+10%)
* LFO_PWM 60 -> 80 (+16%)
* SPREAD 100 -> 127 (+21%)
* VOLUME 100 -> 63 (-29%)
* DLY_FB 50 -> 78 (+22%)
* DLY_TONE 70 -> 100 (+24%)
* DLY_MIX 0 -> 100 (+79%)
* REV_SIZE 100 -> 90 (-8%)
* REV_DAMP 60 -> 35 (-20%)
* REV_MIX 35 -> 45 (+8%)
* ALLEY 0 -> 104 (+82%) (SYNC -> 337 ms)

### C random

* O1_PW 64 -> 44 (-16%)
* O2_PW 40 -> 30 (-8%)
* CUTOFF 75 -> 100 (+20%) (988 Hz -> 4186 Hz)
* RESO 5 -> 8 (+2%)
* FENV_AMT 74 -> 64 (centre 64: +10 -> +0, -8% of range)
* KEYTRK 64 -> 100 (+28%)
* FTYPE LP24 -> LP12
* FA 50 -> 20 (-24%) (25 ms -> 2 ms)
* AA 60 -> 78 (+14%) (54 ms -> 219 ms)
* AS 100 -> 127 (+21%)
* AR 90 -> 92 (+2%) (558 ms -> 653 ms)
* LFO_SHAPE TRI -> RANDOM
* LFO_RATE 50 -> 70 (+16%) (0.6 Hz -> 1.7 Hz)
* LFO_PITCH 3 -> 16 (+10%)
* LFO_PWM 60 -> 80 (+16%)
* SPREAD 100 -> 127 (+21%)
* VOLUME 100 -> 65 (-28%)
* DLY_FB 50 -> 78 (+22%)
* DLY_TONE 70 -> 100 (+24%)
* DLY_MIX 0 -> 90 (+71%)
* REV_SIZE 100 -> 90 (-8%)
* REV_DAMP 60 -> 35 (-20%)
* REV_MIX 35 -> 65 (+24%)
* ALLEY 0 -> 104 (+82%) (SYNC -> 337 ms)

C against B:

* AA 72 -> 78 (+5%) (137 ms -> 219 ms)
* LFO_SHAPE TRI -> RANDOM
* LFO_RATE 64 -> 70 (+5%) (1.3 Hz -> 1.7 Hz)
* DLY_MIX 100 -> 90 (-8%)
* REV_MIX 45 -> 65 (+16%)

### D soft

* O1_PW 64 -> 32 (-25%)
* O2_PW 40 -> 32 (-6%)
* O2_LVL 100 -> 84 (-13%)
* O2_SEMI +0 -> +12 st
* O2_FINE 73 -> 66 (centre 64: +9 -> +2, -6% of range) (+7.0 cents -> +1.6 cents)
* CUTOFF 75 -> 64 (-9%) (988 Hz -> 523 Hz)
* RESO 5 -> 0 (-4%)
* FENV_AMT 74 -> 64 (centre 64: +10 -> +0, -8% of range)
* KEYTRK 64 -> 127 (+50%)
* FTYPE LP24 -> LP12
* FA 50 -> 20 (-24%) (25 ms -> 2 ms)
* AA 60 -> 82 (+17%) (54 ms -> 299 ms)
* AS 100 -> 127 (+21%)
* AR 90 -> 92 (+2%) (558 ms -> 653 ms)
* LFO_RATE 50 -> 76 (+20%) (0.6 Hz -> 2.3 Hz)
* LFO_PITCH 3 -> 16 (+10%)
* LFO_PWM 60 -> 0 (-47%)
* SPREAD 100 -> 127 (+21%)
* VOLUME 100 -> 76 (-19%)
* DLY_FB 50 -> 78 (+22%)
* DLY_TONE 70 -> 100 (+24%)
* DLY_MIX 0 -> 110 (+87%)
* REV_SIZE 100 -> 90 (-8%)
* REV_DAMP 60 -> 35 (-20%)
* REV_MIX 35 -> 45 (+8%)
* ALLEY 0 -> 104 (+82%) (SYNC -> 337 ms)

D against B:

* O1_PW 44 -> 32 (-9%)
* O2_PW 30 -> 32 (+2%)
* O2_LVL 100 -> 84 (-13%)
* O2_SEMI +0 -> +12 st
* O2_FINE 73 -> 66 (centre 64: +9 -> +2, -6% of range) (+7.0 cents -> +1.6 cents)
* CUTOFF 100 -> 64 (-28%) (4186 Hz -> 523 Hz)
* RESO 8 -> 0 (-6%)
* KEYTRK 100 -> 127 (+21%)
* AA 72 -> 82 (+8%) (137 ms -> 299 ms)
* LFO_RATE 64 -> 76 (+9%) (1.3 Hz -> 2.3 Hz)
* LFO_PWM 80 -> 0 (-63%)
* DLY_MIX 100 -> 110 (+8%)

