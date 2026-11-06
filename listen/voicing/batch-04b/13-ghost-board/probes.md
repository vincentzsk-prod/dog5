# Batch 4B, 13 Ghost Board: probes (the recommended variant B with one control stepped; numbers, not variants)

## 13: what CHEW does (wobble, smear, cost), the soft tone, the deck's place in the chain

### CHEW and WOW/FLT on B (one voice A3 for the wobble; the whole ghost phrase for the tone)

| CHEW | WOW/FLT | wobble: s.d. cents / 5-95 % range cents / strongest rate Hz | dips >= 6 dB (n / deepest dB) | note-on centroid Hz / % above 1.2k / MUD |
|---|---|---|---|---|
| 0 | 64 | 0.0 / 0.0 / 3.2 | 0 / 0.1 | 825 / 4.6 / 14.1 |
| 40 | 0 | 2.3 / 7.9 / 0.4 | 0 / 0.2 | 831 / 4.2 / 15.8 |
| 40 | 64 | 2.3 / 7.8 / 0.4 | 0 / 0.2 | 831 / 4.2 / 15.8 |
| 40 | 127 | 1.9 / 4.7 / 0.3 | 0 / 0.2 | 831 / 4.2 / 15.8 |
| 70 | 0 | 4.1 / 13.2 / 0.5 | 0 / 0.2 | 902 / 3.9 / 17.1 |
| 70 | 64 | 4.2 / 13.3 / 0.5 | 0 / 0.2 | 902 / 3.9 / 17.1 |
| 70 | 127 | 2.0 / 5.7 / 0.3 | 0 / 0.2 | 903 / 3.9 / 17.1 |
| 100 | 0 | 6.2 / 22.2 / 0.5 | 1 / 7.5 | 1064 / 3.7 / 18.6 |
| 100 | 64 | 6.3 / 21.9 / 0.5 | 1 / 7.5 | 1064 / 3.7 / 18.6 |
| 100 | 127 | 2.1 / 6.7 / 0.3 | 1 / 7.5 | 1065 / 3.7 / 18.5 |
| 127 | 0 | 6.5 / 22.6 / 0.5 | 0 / 5.6 | 1205 / 3.4 / 20.2 |
| 127 | 64 | 6.7 / 22.3 / 0.5 | 0 / 5.6 | 1205 / 3.4 / 20.2 |
| 127 | 127 | 2.4 / 7.8 / 0.3 | 0 / 5.7 | 1205 / 3.4 / 20.2 |

### CPU (host instr/sample)

|  | worst case | idle | load |
|---|---|---|---|
| B as shipped (CHEW 100) | 2679 | 1948 | 731 |
| B with CHEW 0 | 1895 | 1179 | 716 |
| B with echo and spring off, CHEW 100 | 2663 | 1932 | 731 |

### CUTOFF (LP12, 100 % key tracking) against the triangle probe and MUD (B's 2-octave-up copy kept)

| CUTOFF | Hz at C4 | harmonics 3 / 5 / 7 re H1 (triangle -19.1 / -28.0 / -34.2) | note-on centroid Hz | note-on MUD |
|---|---|---|---|---|
| 60 | 415 | -19.0 / -29.9 / -39.6 | 1048 | 74.4 |
| 64 | 523 | -17.2 / -27.3 / -36.8 | 1035 | 42.3 |
| 70 | 740 | -14.5 / -23.2 / -32.1 | 1064 | 18.6 |
| 76 | 1047 | -12.6 / -19.8 / -27.8 | 1139 | 9.3 |
| 84 | 1661 | -11.2 / -16.7 / -23.4 | 1293 | 4.5 |

### the 2-octave-up copy (OSC 2 LEVEL; B 112): where the energy above 1.2 kHz comes from

| O2 LEVEL | centroid Hz | % above 1.2k | note-on MUD | tail MUD 0-250 / 250-750 / 750-1500 ms |
|---|---|---|---|---|
| 0 | 955 | 0.3 | 245.5 | 785 / 648 / 37 |
| 50 | 968 | 0.4 | 163.0 | 610 / 551 / 36 |
| 80 | 1006 | 1.2 | 58.6 | 240 / 258 / 29 |
| 112 | 1064 | 3.7 | 18.6 | 74 / 89 / 17 |
| 127 | 1096 | 5.8 | 11.1 | 43 / 54 / 12 |

