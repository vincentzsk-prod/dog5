# Batch 4A, 10 Atlantic Swell: variants and numbers

Chapter II (The Tidal Hexes). Round 1, **rendered, not yet heard**. Method and definitions: `dog5-docs/voicing/README.md` section 15. Level phrase: `q_organ` (own phrase, effects included, tails excluded), reference -18.0 dBFS RMS +-1.5, peak <= -4. WAVs (`<dir>_<KEY>_<organ|tangle|wash|stabs>.wav`) are on the never-merged listen branch only.

## Variants

* **A original**: the nearest-base patch as it stood (HOLLOW PAD, shared with 12: POLY, two inverse narrow pulses through a notch, no vibrato, no delay).
* **B june** (RECOMMENDED, committed): clear chorus first: DUAL pair (L / R), TRI LFO 0.72 Hz on pitch +-19 cents with PHASE SPREAD, organ keying, BBD 361 ms FEEDBK 95 MIX 100, a touch of spring.
* **C wooze**: B along the depth axis: pitch +-28 cents at 0.84 Hz (vibrato-led), and a heavier echo (387 ms, FEEDBK 104, MIX 118).
* **D leslie**: B with a tremolo on the same LFO (AMP 45, a 3.8 dB dip) and PHASE FREE so every voice swings together: vibrato and tremolo at one rate, 0.84 Hz (the rotary-speaker idea).

## Numbers

| | A original | B june | C wooze | D leslie |
|---|---|---|---|---|
| VOLUME | 100 | 64 | 64 | 71 |
| level, organ phrase (q) (dBFS RMS, note-on region, effects in, tails out; reference -18.0 +-1.5) | -19.00 | -18.24 | -17.88 | -18.04 |
| phrase (b) RMS (dBFS) / minus the level phrase (dB) | -17.6 / +1.4 | -19.0 / -0.8 | -18.7 / -0.9 | -19.0 / -1.0 |
| peak, whole renders (dBFS; limit -4) | -4.8 | -4.4 | -4.9 | -5.1 |
| crest factor, level phrase (dB) | 12.8 | 13.9 | 12.9 | 12.9 |
| K-weighted RMS, (b) (dBFS) | -17.7 | -19.1 | -18.8 | -19.1 |
| amp attack (probe, one voice, LFO off): 10 / 50 / 90 % of the plateau (ms) | 6 / 29 / 61 | 1 / 1 / 3 | 1 / 1 / 3 | 1 / 1 / 3 |
| AA byte -> the time table's nominal (ms) | 70 -> 117 | 18 -> 2 | 18 -> 2 | 18 -> 2 |
| note-on region: centroid (Hz) | 5369 | 2154 | 2170 | 2144 |
| note-on region: band split % <60 / 60-150 / 150-400 / 400-1.2k / 1.2k+ | 0 / 0 / 57 / 20 / 23 | 0 / 0 / 38 / 45 / 17 | 0 / 0 / 34 / 49 / 17 | 0 / 0 / 32 / 49 / 18 |
| MUD = share(150-400) / share(1.2k+), note-on region | 2.5 | 2.3 | 2.0 | 1.8 |
| worst-case CPU (host instr/sample: idle + load) | 2020 (1164 + 856) | 2294 (1180 + 1114) | 2294 (1180 + 1114) | 2287 (1180 + 1107) |
| LFO: shape / rate (Hz, law) / pitch +-cents (law) / amp dip (dB p-p, law) / phase | TRI / 0.37 / 0 on BOTH / 0.0 / SPREAD | TRI / 0.72 / 19 on BOTH / 0.0 / SPREAD | TRI / 0.84 / 28 on BOTH / 0.0 / SPREAD | TRI / 0.84 / 19 on BOTH / 3.8 / FREE |
| pitch probe (one voice, audio): wander s.d. / 5-95 % range (cents) / rate (Hz) | 0.0 / 0.0 / 0.40 | 10.9 / 33.6 / 0.72 | 16.2 / 50.3 / 0.84 | 10.8 / 33.6 / 0.84 |
| tremolo on the held chord, dry (audio): depth (dB, 95th-5th pct of 20 ms RMS) / strongest rate (Hz) | 5.7 / 1.33 | 2.4 / 0.75 | 3.7 / 2.82 | 3.5 / 0.91 |
| chorus width, held chord: L/R correlation 150-4k Hz dry (full) / side-to-mid dry (dB) | 0.78 (0.70) / -8.8 | 0.48 (0.42) / -4.6 | 0.45 (0.31) / -4.2 | 0.41 (0.32) / -3.7 |
| chorus beating, A3 band of the held chord, dry: rate mean (min-max) Hz / envelope depth (dB) | 1.01 (0.67-1.18) / 17.9 | 1.18 (0.34-2.02) / 29.0 | 2.29 (1.18-2.69) / 30.4 | 1.08 (0.34-1.35) / 37.3 |
| delay: ALLEY (ms) / FEEDBK / MIX / PINGPONG | 10 / 50 / 0 / 127 | 361 / 95 / 100 / 127 | 387 / 104 / 118 / 127 | 361 / 95 / 100 / 127 |
| first repeat of an isolated 120 ms E4: peak re the dry note's peak (dB) / peak at ms after the note-on | - / -20 | -9.1 / 482 | -7.3 / 505 | -10.9 / 422 |
| the repeats 1..6 (dB re the first, one slot of a delay time each) | +0.0 +0.0 +0.0 +0.0 +0.0 +0.0 | +0.0 -3.2 -6.5 -9.8 -13.2 -16.5 | +0.0 -2.5 -4.8 -7.2 -9.9 -12.2 | +0.0 -3.3 -6.6 -9.8 -13.0 -16.2 |
| echo spectrum vs the note's, isolated E4: centroid note -> first repeat (Hz) / MUD of the repeat | 5916 -> 0 / 0.0 | 2595 -> 1454 / 1.7 | 2496 -> 1350 / 2.6 | 2534 -> 1468 / 0.6 |
| spring in the first repeat's window re the note (dB); delay's margin over it (dB) | -16.5 ; - | -25.2 ; 16.1 | -26.0 ; 18.7 | -26.0 ; 15.0 |
| echo under the figure's four staccato notes (delay return re the note, dB, per note) | - / - / - / - | -33.7 / -9.9 / -15.8 / -13.7 | -25.3 / -13.7 / -19.9 / -14.6 | -28.3 / -14.8 / -16.5 / -9.3 |
| spring under the same notes (dB) | -21.0 / -13.1 / -0.8 / -0.4 | -19.8 / -19.4 / -19.7 / -20.5 | -21.0 / -19.7 / -18.9 / -21.1 | -17.2 / -16.5 / -18.0 / -17.6 |
| after the held chord's note-off: delay return re the chord (dB) in 0-100 / 100-250 / 250-500 / 500-1000 / 1000-2000 ms | - / - / - / - / - | -7.6 / -7.5 / -8.1 / -11.8 / -17.8 | -5.0 / -5.6 / -5.7 / -8.7 / -13.0 | -6.5 / -6.6 / -8.6 / -11.9 / -18.0 |
| same, spring return (dB) | -13.2 / -15.5 / -19.3 / -25.3 / -38.7 | -19.6 / -25.3 / -34.7 / -50.1 / -84.1 | -14.1 / -19.4 / -28.0 / -42.2 / -71.2 | -16.6 / -22.5 / -31.2 / -46.0 / -77.2 |
| spring (DRAIN %, SIZE, DAMP) | 40 (31 %), 100, 60 | 24 (19 %), 70, 30 | 24 (19 %), 70, 30 | 24 (19 %), 70, 30 |
| tail after the held chord (to -20 / -40 / -60 dB re its level, ms, DC out; window 2 s) | 880 / 1700 / >win | 1134 / >win / >win | 1990 / >win / >win | 1472 / >win / >win |

## Parameter changes, each before -> after (the original is the nearest-base patch as it stood; variant A is that patch)

### B june

* O1_PW 20 -> 26 (+5%)
* O2_PW 108 -> 26 (-65%)
* O2_LVL 100 -> 84 (-13%)
* O2_SEMI +0 -> +12 st
* O2_FINE 76 -> 64 (centre 64: +12 -> +0, -9% of range) (+9.4 cents -> +0.0 cents)
* CUTOFF 70 -> 104 (+27%) (740 Hz -> 5274 Hz)
* RESO 20 -> 22 (+2%)
* FTYPE NOTCH -> LP12
* AA 70 -> 18 (-41%) (117 ms -> 2 ms)
* AS 100 -> 127 (+21%)
* AR 100 -> 52 (-38%) (1218 ms -> 29 ms)
* LFO_RATE 40 -> 53 (+10%) (0.4 Hz -> 0.7 Hz)
* LFO_PITCH 0 -> 16 (+13%)
* LFO_PWM 40 -> 0 (-31%)
* MODE POLY -> DUAL
* SPREAD 100 -> 127 (+21%)
* VOLUME 100 -> 64 (-28%)
* DLY_FB 50 -> 95 (+35%)
* DLY_TONE 70 -> 90 (+16%)
* DLY_MIX 0 -> 100 (+79%)
* REV_SIZE 100 -> 70 (-24%)
* REV_DAMP 60 -> 30 (-24%)
* REV_MIX 40 -> 24 (-13%)
* POLY_N 5 -> 6 voices
* ALLEY 0 -> 106 (+83%) (SYNC -> 361 ms)

### C wooze

* O1_PW 20 -> 26 (+5%)
* O2_PW 108 -> 26 (-65%)
* O2_LVL 100 -> 84 (-13%)
* O2_SEMI +0 -> +12 st
* O2_FINE 76 -> 64 (centre 64: +12 -> +0, -9% of range) (+9.4 cents -> +0.0 cents)
* CUTOFF 70 -> 104 (+27%) (740 Hz -> 5274 Hz)
* RESO 20 -> 22 (+2%)
* FTYPE NOTCH -> LP12
* AA 70 -> 18 (-41%) (117 ms -> 2 ms)
* AS 100 -> 127 (+21%)
* AR 100 -> 52 (-38%) (1218 ms -> 29 ms)
* LFO_RATE 40 -> 56 (+13%) (0.4 Hz -> 0.8 Hz)
* LFO_PITCH 0 -> 22 (+17%)
* LFO_PWM 40 -> 0 (-31%)
* MODE POLY -> DUAL
* SPREAD 100 -> 127 (+21%)
* VOLUME 100 -> 64 (-28%)
* DLY_FB 50 -> 104 (+43%)
* DLY_TONE 70 -> 90 (+16%)
* DLY_MIX 0 -> 118 (+93%)
* REV_SIZE 100 -> 70 (-24%)
* REV_DAMP 60 -> 30 (-24%)
* REV_MIX 40 -> 24 (-13%)
* POLY_N 5 -> 6 voices
* ALLEY 0 -> 108 (+85%) (SYNC -> 387 ms)

C against B:

* LFO_RATE 53 -> 56 (+2%) (0.7 Hz -> 0.8 Hz)
* LFO_PITCH 16 -> 22 (+5%)
* DLY_FB 95 -> 104 (+7%)
* DLY_MIX 100 -> 118 (+14%)
* ALLEY 106 -> 108 (+2%) (361 ms -> 387 ms)

### D leslie

* O1_PW 20 -> 26 (+5%)
* O2_PW 108 -> 26 (-65%)
* O2_LVL 100 -> 84 (-13%)
* O2_SEMI +0 -> +12 st
* O2_FINE 76 -> 64 (centre 64: +12 -> +0, -9% of range) (+9.4 cents -> +0.0 cents)
* CUTOFF 70 -> 104 (+27%) (740 Hz -> 5274 Hz)
* RESO 20 -> 22 (+2%)
* FTYPE NOTCH -> LP12
* AA 70 -> 18 (-41%) (117 ms -> 2 ms)
* AS 100 -> 127 (+21%)
* AR 100 -> 52 (-38%) (1218 ms -> 29 ms)
* LFO_RATE 40 -> 56 (+13%) (0.4 Hz -> 0.8 Hz)
* LFO_PHASE SPREAD -> FREE
* LFO_PITCH 0 -> 16 (+13%)
* LFO_PWM 40 -> 0 (-31%)
* LFO_AMP 0 -> 45 (+35%)
* MODE POLY -> DUAL
* SPREAD 100 -> 127 (+21%)
* VOLUME 100 -> 71 (-23%)
* DLY_FB 50 -> 95 (+35%)
* DLY_TONE 70 -> 90 (+16%)
* DLY_MIX 0 -> 100 (+79%)
* REV_SIZE 100 -> 70 (-24%)
* REV_DAMP 60 -> 30 (-24%)
* REV_MIX 40 -> 24 (-13%)
* POLY_N 5 -> 6 voices
* ALLEY 0 -> 106 (+83%) (SYNC -> 361 ms)

D against B:

* LFO_RATE 53 -> 56 (+2%) (0.7 Hz -> 0.8 Hz)
* LFO_PHASE SPREAD -> FREE
* LFO_AMP 0 -> 45 (+35%)

