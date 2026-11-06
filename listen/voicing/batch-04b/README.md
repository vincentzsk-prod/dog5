# Batch 4B (Chapter II): 13 Ghost Board, 14 Reef Break

Round 1, rendered, not yet heard. Per patch: `README.md` (variants and numbers), `probes.md` (one control stepped), `results.json`, and (on the listen branch only) the WAVs `<NN-name>_<KEY>_<phrase>.wav` (A is the original through the base program path; B, C, D are variants over INIT; VOLUME is trimmed so the own phrase's peak is <= -4 dBFS and the level near -18.0 dBFS RMS). Phrases: `ghost` = t_ghost (13), `crash` = u_crash (14), `stabs` = b_stabs. Method: `dog5-docs/voicing/README.md` section 17.

## 13 Ghost Board

| variant | what | VOLUME | level (own phrase) | (b) | peak (own) | worst-case CPU |
|---|---|---|---|---|---|---|
| A original | the nearest-base patch as it stood (PWM STRINGS, 13's alone now: two pulses with PWM, LP24, a spring, no echo, no tape, inert LFO PITCH 3) | 100 | -13.2 | -14.2 | -0.2 | 2069 |
| B middle (recommended, committed) | the middle: soft near-triangle tone, tape CHEW 100 (wow-leaning), echo 275 ms FEEDBK 82 MIX 70, spring DRAIN 50 | 81 | -18.0 | -19.7 | -5.2 | 2679 |
| C tape | leans Mellotron: clearer tone (CUTOFF 60, less octave), the most tape (CHEW 127, wow), less echo (MIX 40, FEEDBK 60) and spring | 95 | -18.0 | -18.7 | -5.6 | 2679 |
| D echo | leans Space Echo: richer body (CUTOFF 66, more octave), CHEW 70, long rich echo (MIX 110, FEEDBK 100, 387 ms), more spring (DRAIN 80, SIZE 100, DAMP 55) | 62 | -17.9 | -23.4 | -5.0 | 2680 |

## 14 Reef Break

| variant | what | VOLUME | level (own phrase) | (b) | peak (own) | worst-case CPU |
|---|---|---|---|---|---|---|
| A original | the nearest-base patch as it stood (PERC HIT, 14's alone: noise 60 + a saw and a saw +24 st, LP12 with a filter envelope, spring, no echo) | 100 | -47.9 | -44.4 | -11.1 | 1762 |
| B burst (recommended, committed) | near-instant attack, medium tail (top band 20 / 40 dB down in ~0.5 / ~0.9 s), echo FEEDBK 96 MIX 90 at 361 ms | 118 | -19.9 | -14.3 | -4.3 | 1832 |
| C swell | a quick swell (peak in ~10-40 ms), the longest tail, echo FEEDBK 100 MIX 80 | 121 | -18.0 | -12.8 | -4.5 | 1857 |
| D runaway | near-instant attack, the shortest tail, a near-runaway echo (FEEDBK 114 MIX 100, 337 ms) | 124 | -20.1 | -14.4 | -4.5 | 1827 |

