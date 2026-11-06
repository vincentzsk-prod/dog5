# Batch 4B, 14 Reef Break: probes (the recommended variant B with one control stepped; numbers, not variants)

## 14: what the filter does to a noise burst, the attack, the echo's limit

### what a filter can do for the cymbal's decay (B's noise, sub, envelopes; one control changed; VOLUME as B; the decays are of the voice alone, from the A1 hit)

|  | sub (40-150) to -20 / -40 dB ms | 400-1.2k to -20 / -40 dB ms | 1.2k-4k to -20 / -40 dB ms | 4k+ to -20 / -40 dB ms | noise-to-sub first 100 ms dB | level / peak at the same VOLUME (dBFS) |
|---|---|---|---|---|---|---|
| B: HP12, CUTOFF 100, ENV AMT 0 (the cutoff climbs from -97 st), FD 100 | 163 / 279 | 276 / 331 | 316 / 641 | 482 / 932 | +4.6 | -19.9 / -4.3 |
| LP12, CUTOFF 60, ENV AMT 110 (opens at the strike, closes: the original's way) | 499 / 964 | 276 / 633 | 302 / 351 | 223 / 302 | +1.2 | -20.5 / -3.9 |
| LP12 wide open (CUTOFF 127), no envelope | 499 / 964 | 357 / 749 | 441 / 879 | 496 / 975 | +2.0 | -19.6 / -3.6 |
| NOTCH, CUTOFF 85, RESO 30, no envelope | 499 / 964 | 276 / 749 | 392 / 879 | 496 / 967 | +2.2 | -19.6 / -5.0 |
| HP12 with no envelope (ENV AMT 64, the sub is cut) | 1416 / 1428 | 229 / 749 | 430 / 879 | 496 / 961 | +27.3 | -22.7 / -7.9 |
| BP12, CUTOFF 100, ENV AMT 0 | 232 / 267 | 151 / 566 | 421 / 801 | 473 / 868 | -17.2 | -31.1 / -15.9 |

### FD (how long the high-pass stays low = the sub's duration), B

| FD | sub (40-150) to -20 / -40 dB ms | 400-1.2k to -20 / -40 dB ms | 1.2k-4k to -20 / -40 dB ms | 4k+ to -20 / -40 dB ms | noise-to-sub first 100 ms dB | level / peak at the same VOLUME (dBFS) |
|---|---|---|---|---|---|---|
| 85 | 58 / 104 | 142 / 276 | 287 / 641 | 482 / 932 | +7.7 | -20.6 / -4.7 |
| 92 | 93 / 174 | 229 / 311 | 313 / 641 | 482 / 932 | +5.9 | -20.2 / -4.4 |
| 100 | 163 / 279 | 276 / 331 | 316 / 641 | 482 / 932 | +4.6 | -19.9 / -4.3 |
| 108 | 255 / 290 | 276 / 331 | 325 / 641 | 482 / 932 | +3.9 | -19.6 / -4.2 |

### AD / AR (the ring-out; both stepped together), B

| AD = AR | sub (40-150) to -20 / -40 dB ms | 400-1.2k to -20 / -40 dB ms | 1.2k-4k to -20 / -40 dB ms | 4k+ to -20 / -40 dB ms | noise-to-sub first 100 ms dB | level / peak at the same VOLUME (dBFS) |
|---|---|---|---|---|---|---|
| 84 | 139 / 232 | 148 / 308 | 255 / 351 | 270 / 511 | +4.4 | -22.3 / -4.9 |
| 88 | 151 / 267 | 229 / 313 | 311 / 467 | 345 / 700 | +4.5 | -21.0 / -4.8 |
| 92 | 163 / 279 | 276 / 331 | 316 / 641 | 482 / 932 | +4.6 | -19.9 / -4.3 |
| 97 | 174 / 290 | 305 / 337 | 340 / 879 | 679 / 1370 | +4.6 | -18.7 / -4.8 |

### AA -> the hit's attack (A1, voice alone, 10 / 50 / 90 % of the peak, ms)

| AA | 10 / 50 / 90 % ms | peak at ms |
|---|---|---|
| 0 | 0.0 / 0.2 / 8.5 | 9.0 |
| 30 | 0.2 / 2.5 / 8.5 | 9.0 |
| 44 | 1.2 / 8.0 / 27.2 | 27.4 |
| 52 | 2.2 / 8.7 / 27.2 | 27.4 |
| 60 | 3.2 / 18.0 / 27.4 | 64.1 |

### NOISE / sub levels (B at VOLUME 118)

| NOISE | O1 LVL | O2 LVL | noise / sub dBFS first 100 ms (A1) | ratio dB | level / peak of the phrase |
|---|---|---|---|---|---|
| 127 | 80 | 45 | -18.2 / -22.7 | +4.6 | -19.9 / -4.3 |
| 127 | 110 | 60 | -18.2 / -17.4 | -0.8 | -18.1 / -3.1 |
| 100 | 80 | 45 | -22.3 / -22.7 | +0.5 | -22.6 / -5.6 |
| 127 | 50 | 30 | -18.2 / -30.9 | +12.7 | -20.7 / -4.9 |
| 127 | 0 | 0 | -18.2 / -210.3 | +192.1 | -20.9 / -5.7 |
| 0 | 80 | 45 | -210.3 / -22.7 | -187.6 | -26.3 / -9.4 |

### FEEDBK: where the echo stops decaying (B, MIX 90, 361 ms; 24 slots = 8.7 s)

| FEEDBK | repeats 1..6 re the burst (dB) | repeat 12 / 24 (dB) | slots above -40 dB | peak dBFS / clipped samples |
|---|---|---|---|---|
| 96 | -12 -18 -23 -27 -31 -34 | -57 / -80 | 7 | -5.7 / 0 |
| 105 | -12 -17 -21 -25 -28 -30 | -46 / -80 | 9 | -5.7 / 0 |
| 112 | -12 -17 -20 -23 -26 -28 | -40 / -197 | 12 | -5.7 / 0 |
| 114 | -12 -16 -19 -21 -23 -25 | -34 / -55 | 15 | -5.7 / 0 |
| 118 | -12 -15 -17 -19 -20 -20 | -23 / -28 | 24 | -5.7 / 0 |
| 122 | -12 -14 -16 -16 -16 -16 | -14 / -10 | 24 | -5.7 / 0 |
| 127 | -12 -13 -14 -13 -13 -11 | -6 / -1 | 24 | -5.7 / 0 |

