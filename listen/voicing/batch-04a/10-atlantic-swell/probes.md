# Batch 4A, 10 Atlantic Swell: probes (the recommended variant B with one control stepped; numbers, not variants)

## 10: what builds the chorus, what the delay's TONE does, the Leslie phase

| B with one thing changed (the held A minor chord, voice + the short BBD where named) | L/R corr / side-to-mid dB | A3-band beat rate Hz / depth dB | level modulation dB | centroid Hz |
|---|---|---|---|---|
| B as shipped: pitch +-19 cents on BOTH, SPREAD | 0.48 / -4.6 | 1.18 / 29.0 | 2.4 | 2037 |
| pitch on OSC 2 only | 0.42 / -3.9 | 1.01 / 38.0 | 2.3 | 2070 |
| pitch +-19 cents, PHASE FREE (voices in step) | 0.41 / -3.8 | 1.01 / 39.0 | 1.9 | 2026 |
| no pitch LFO (only the DUAL detune, 5.5 cents) | 0.41 / -3.8 | 1.01 / 39.3 | 1.8 | 2024 |
| DETUNE 0, pitch LFO +-19 cents with SPREAD (the chorus without the static detune) | 0.40 / -3.7 | 1.08 / 37.3 | 3.2 | 2102 |
| DETUNE 0, pitch LFO +-19 cents, PHASE FREE | 0.36 / -3.2 | 0.91 / 5.8 | 4.4 | 2003 |
| no LFO and no detune (DETUNE 0): a plain DUAL pair | 0.35 / -3.2 | 0.91 / 5.5 | 4.5 | 1997 |
| a short BBD instead: no pitch LFO, ALLEY 15, FEEDBK 0, MIX 90, PINGPONG 127 | 0.31 / -2.8 | 1.01 / 35.8 | 2.4 | 2060 |

The short-BBD row has a fixed delay time (ALLEY 15 = 16.1 ms): the engine has no LFO on the BBD's time, so it is a comb filter and a Haas widener, not a chorus; the row shows its width and the comb's effect on the centroid. CHEW is not used in any variant (it smears the top, measured in 05 round 1; here the first repeat is already 43 % darker than the note by the BBD's own band-limit).

### DLY TONE on the repeats (isolated E4)

| DLY_TONE | first repeat centroid Hz | third repeat centroid Hz | repeats 1..5 dB re the first |
|---|---|---|---|
| 60 | 1454 | 949 | +0.0 -3.6 -7.3 -11.0 -14.5 |
| 90 | 1454 | 1082 | +0.0 -3.2 -6.5 -9.8 -13.2 |
| 127 | 1454 | 1136 | +0.0 -3.1 -6.3 -9.5 -12.8 |

### FEEDBK (isolated E4; tail = to -20 / -40 / -60 dB re the note, ms)

| DLY_FB | repeats 1..8 dB re the first | tail ms |
|---|---|---|
| 85 | +0.0 -4.2 -8.4 -12.7 -17.0 -21.4 -25.5 -29.7 | 148 / 938 / 3636 |
| 95 | +0.0 -3.2 -6.5 -9.8 -13.2 -16.5 -19.6 -22.7 | 148 / 956 / 3100 |
| 105 | +0.0 -2.4 -4.8 -7.2 -9.7 -12.2 -14.3 -16.5 | 148 / 1294 / 4834 |

### the tremolo on the held chord by LFO PHASE (why D is FREE: with SPREAD the voices' tremolos are 45 degrees apart and cancel in the sum)

| LFO_PHASE | LFO_AMP | one voice's dip dB (law) | tremolo of the chord: depth dB / rate Hz |
|---|---|---|---|
| SPREAD | 0 | 0 | 2.4 / 0.75 |
| SPREAD | 45 | 3.8 | 2.2 / 1.21 |
| SPREAD | 80 | 8.5 | 2.8 / 1.15 |
| FREE | 0 | 0 | 1.9 / 0.75 |
| FREE | 45 | 3.8 | 2.9 / 0.57 |
| FREE | 80 | 8.5 | 6.5 / 0.64 |
| SYNC | 0 | 0 | 1.8 / 0.76 |
| SYNC | 45 | 3.8 | 3.9 / 0.76 |
| SYNC | 80 | 8.5 | 7.8 / 0.73 |

### CPU levers (host instr/sample; the heaviest voiced patches are 15 D 2375, 07 B 2177)

|  | worst case | idle | load |
|---|---|---|---|
| B as shipped: DUAL, POLY 6, two oscillators | 2294 | 1180 | 1114 |
| B with one oscillator (OSC 2 off; the 4' register gone) | 2246 | 1180 | 1066 |
| B as POLY (one voice per note: no L / R pair, the chorus is gone) | 1804 | 1180 | 624 |
| B with the BBD and the spring off (voices only) | 2278 | 1164 | 1114 |

