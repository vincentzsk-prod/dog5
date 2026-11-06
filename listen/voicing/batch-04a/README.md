# Batch 4A (Chapter II): 10 Atlantic Swell, 12 Kelp Tangle, 16 Tidal Pull

Round 1, rendered, not yet heard. Per patch: `README.md` (variants and numbers), `probes.md` (one control stepped), `results.json`, and (on the listen branch only) the WAVs `<NN-name>_<KEY>_<phrase>.wav` (A is the original through the base program path; B, C, D are variants over INIT; VOLUME is trimmed to -18.0 dBFS RMS on the patch's own phrase, effects in, tails out). Phrases: `organ` = q_organ (10), `tangle` = r_tangle (12), `wash` = s_wash (16), `stabs` = b_stabs (the bank's reference phrase); each starts 100 ms before its first note. Method: `dog5-docs/voicing/README.md` section 16.

## 10 Atlantic Swell

| variant | what | VOLUME | level (own phrase) | (b) | peak | worst-case CPU |
|---|---|---|---|---|---|---|
| A original | the nearest-base patch as it stood (HOLLOW PAD, shared with 12: POLY, two inverse narrow pulses through a notch, no vibrato, no delay) | 100 | -19.0 | -17.6 | -4.8 | 2020 |
| B june (recommended, committed) | clear chorus first: DUAL pair (L / R), TRI LFO 0.72 Hz on pitch +-19 cents with PHASE SPREAD, organ keying, BBD 361 ms FEEDBK 95 MIX 100, a touch of spring | 64 | -18.2 | -19.0 | -4.4 | 2294 |
| C wooze | B along the depth axis: pitch +-28 cents at 0.84 Hz (vibrato-led), and a heavier echo (387 ms, FEEDBK 104, MIX 118) | 64 | -17.9 | -18.7 | -4.9 | 2294 |
| D leslie | B with a tremolo on the same LFO (AMP 45, a 3.8 dB dip) and PHASE FREE so every voice swings together: vibrato and tremolo at one rate, 0.84 Hz (the rotary-speaker idea) | 71 | -18.0 | -19.0 | -5.1 | 2287 |

## 12 Kelp Tangle

| variant | what | VOLUME | level (own phrase) | (b) | peak | worst-case CPU |
|---|---|---|---|---|---|---|
| A original | the nearest-base patch as it stood (HOLLOW PAD: narrow inverse pulses through a notch, PWM +-2 points: not audible as PWM) | 100 | -19.4 | -17.6 | -4.8 | 2020 |
| B murk (recommended, committed) | murk first: LP24 CUTOFF 86 at 100 % key tracking, RESO 30, PWM +-15 points around 33 % (18-48 %), TRI 1.03 Hz, PHASE SYNC, spring DRAIN 55 | 75 | -18.0 | -17.0 | -5.3 | 2042 |
| C open | B along the cutoff axis: CUTOFF 98 (more of each note's harmonics through the filter) | 74 | -18.0 | -17.0 | -5.3 | 2042 |
| D tangle | B along the rate / depth axis: PWM +-16.8 points, TRI 2.3 Hz, PHASE SPREAD (each voice 45 degrees on) | 76 | -17.9 | -17.1 | -5.0 | 2047 |

## 16 Tidal Pull

| variant | what | VOLUME | level (own phrase) | (b) | peak | worst-case CPU |
|---|---|---|---|---|---|---|
| A original | the nearest-base patch as it stood (PWM STRINGS, shared with 13 Ghost Board: no delay, spring only, inert LFO PITCH 3) | 100 | -11.8 | -14.2 | -0.2 | 2069 |
| B tri (recommended, committed) | TRI LFO 1.26 Hz on pitch +-19 cents and the pulse widths, pulses, attack 101 ms to 90 %, the echo ahead of the spring (DLY MIX 100, DRAIN 45) | 63 | -18.1 | -21.6 | -4.4 | 2026 |
| C random | smooth RANDOM LFO ~1.7 Hz, attack 160 ms, the spring ahead of the echo (DRAIN 65, DLY MIX 90) | 65 | -18.0 | -22.2 | -4.3 | 2025 |
| D soft | the oscillators softened toward a triangle (narrow pulses through a key-tracking low-pass, an octave stack), TRI 2.3 Hz, attack 219 ms, echo up (MIX 110) | 76 | -19.1 | -26.8 | -4.4 | 2027 |

