# 20 Fire & Ice: Batch 5B round 1 (rendered, not yet heard)

| var | tag | VOLUME | level | K-RMS | (b) RMS | peak (all phrases) | clip | CPU worst (idle+load) |
|---|---|---|---|---|---|---|---|---|
| A | original | 100 | -23.11 | -22.44 | -22.01 | -14.10 | 0 | 1370 |
| A* | original-matched | 127 | -19.01 | n/a | n/a | -10.08 | n/a | n/a |
| B | rolled | 127 | -19.26 | -18.94 | -16.29 | -8.83 | 0 | 1967 |
| C | half | 127 | -18.76 | -18.39 | -16.46 | -8.36 | 0 | 1967 |
| D | open | 126 | -18.07 | -17.52 | -16.60 | -8.42 | 0 | 1967 |

Level = the note-on region of phrase d_lead, reference -18.0 dBFS +-1.5; peak limit -4 dBFS over d_lead, aa_fire_detached, ab_fire_legato, b_stabs.

## Parameter changes against the original (A)

**B rolled** (the brief: tone rolled off (CUTOFF 54), the filter envelope opens it on the strike so some of the sweep survives; GROWL 70)

* O2_LVL 120 -> 127 (+6%)
* CUTOFF 90 -> 54 (-28%) (2349 Hz -> 294 Hz)
* RESO 10 -> 14 (+3%)
* FENV_AMT 80 -> 127 (centre 64: +16 -> +63, +37% of range)
* AR 40 -> 50 (+8%) (11 ms -> 25 ms)
* GLIDE 20 -> 56 (+28%)
* GROWL 0 -> 70 (+55%)
* DLY_FB 40 -> 92 (+41%)
* DLY_TONE 70 -> 55 (-12%)
* DLY_MIX 35 -> 85 (+39%)
* REV_SIZE 70 -> 80 (+8%)
* REV_MIX 22 -> 30 (+6%)
* ALLEY 0 -> 107 (+84%) (SYNC -> 374 ms)

**C half** (half closed (CUTOFF 66), GROWL 60)

* O2_LVL 120 -> 127 (+6%)
* CUTOFF 90 -> 66 (-19%) (2349 Hz -> 587 Hz)
* RESO 10 -> 12 (+2%)
* FENV_AMT 80 -> 105 (centre 64: +16 -> +41, +20% of range)
* AR 40 -> 50 (+8%) (11 ms -> 25 ms)
* GLIDE 20 -> 56 (+28%)
* GROWL 0 -> 60 (+47%)
* DLY_FB 40 -> 92 (+41%)
* DLY_TONE 70 -> 55 (-12%)
* DLY_MIX 35 -> 85 (+39%)
* REV_SIZE 70 -> 80 (+8%)
* REV_MIX 22 -> 30 (+6%)
* ALLEY 0 -> 107 (+84%) (SYNC -> 374 ms)

**D open** (moderately open (CUTOFF 84), GROWL 48: the sweep is the star)

* O2_LVL 120 -> 127 (+6%)
* CUTOFF 90 -> 84 (-5%) (2349 Hz -> 1661 Hz)
* FENV_AMT 80 -> 85 (centre 64: +16 -> +21, +4% of range)
* AR 40 -> 50 (+8%) (11 ms -> 25 ms)
* GLIDE 20 -> 56 (+28%)
* GROWL 0 -> 48 (+38%)
* DLY_FB 40 -> 92 (+41%)
* DLY_TONE 70 -> 55 (-12%)
* DLY_MIX 35 -> 85 (+39%)
* REV_SIZE 70 -> 80 (+8%)
* REV_MIX 22 -> 30 (+6%)
* ALLEY 0 -> 107 (+84%) (SYNC -> 374 ms)

## The hard-sync sweep on one detached A4 (900 ms, FX off, GROWL off, MONO)

`sweep on` = ENV>O2 as set, `off` = ENV>O2 64 (no sweep). `d_hi` = energy above 1.2 kHz, on minus off (dB). `hi vs open` = that energy against the same patch with CUTOFF 127 (what the filter takes away).

| var | window ms | centroid on | centroid off | d centroid | d_hi dB | hi vs open dB |
|---|---|---|---|---|---|---|
| A | 0-100 | 2943 | 2246 | +697 | +3.1 | -0.6 |
| A | 100-200 | 2067 | 1545 | +521 | -0.5 | -2.1 |
| A | 200-400 | 1587 | 1383 | +204 | -0.6 | -2.4 |
| A | 400-800 | 1499 | 1351 | +148 | -0.5 | -2.4 |
| B | 0-100 | 3830 | 3261 | +569 | +1.9 | -0.4 |
| B | 100-200 | 1356 | 952 | +404 | -1.8 | -6.2 |
| B | 200-400 | 756 | 600 | +156 | -2.7 | -14.4 |
| B | 400-800 | 652 | 540 | +112 | -1.8 | -17.1 |
| C | 0-100 | 3132 | 2611 | +521 | +1.9 | -0.9 |
| C | 100-200 | 1400 | 997 | +403 | -1.7 | -5.6 |
| C | 200-400 | 905 | 742 | +163 | -2.1 | -9.1 |
| C | 400-800 | 815 | 695 | +120 | -1.6 | -9.9 |
| D | 0-100 | 2793 | 2317 | +476 | +1.8 | -1.0 |
| D | 100-200 | 1850 | 1369 | +481 | -0.7 | -2.7 |
| D | 200-400 | 1360 | 1172 | +188 | -0.8 | -3.4 |
| D | 400-800 | 1272 | 1134 | +138 | -0.7 | -3.4 |

## Detached riff against legato riff (same notes, dry): centroid Hz over 0-100 ms after each note-on

| var | phrase | note 1 | notes 2-8 mean | notes 9-16 mean | sweep contribution (on - off), notes 2-8 mean | sweep contribution, note 1 |
|---|---|---|---|---|---|---|
| A | detached | 1997 | 3549 | 3975 | +855 | +524 |
| A | legato | 1997 | 1782 | 2012 | +179 | +524 |
| B | detached | 3159 | 4709 | 5170 | +821 | +698 |
| B | legato | 3159 | 759 | 860 | +128 | +698 |
| C | detached | 2314 | 4024 | 4503 | +771 | +540 |
| C | legato | 2314 | 975 | 1119 | +147 | +540 |
| D | detached | 1999 | 3610 | 4102 | +698 | +467 |
| D | legato | 1999 | 1573 | 1793 | +166 | +467 |

## GROWL (the drive): crest factor of the dry note-on region (phrase d_lead), GROWL 0 against as set; CPU

CPU here = phrase (b) average + the stress chord's load (host instr/sample), the same two terms with and without GROWL.

| var | GROWL | crest GROWL 0 | crest as set | change | RMS shift | CPU as set | CPU GROWL 0 | GROWL costs |
|---|---|---|---|---|---|---|---|---|
| B | 70 | 10.2 | 6.0 | -4.2 dB | +0.18 dB | 2024 | 1435 | 589 |
| C | 60 | 9.5 | 5.6 | -3.9 dB | +0.03 dB | 2024 | 1435 | 589 |
| D | 48 | 8.3 | 5.1 | -3.3 dB | -0.03 dB | 2024 | 1435 | 590 |

## The echo (one detached A4, 300 ms)

| var | ALLEY ms | FEEDBK | MIX | first repeat re note | repeats above -40 dB re the note | above -20 dB | repeat train (dB re the first) |
|---|---|---|---|---|---|---|---|
| A | 375 | 40 | 35 | -18.8 | 2 | 1 | 0 -12 -23 -35 -46 -51 -51 -51 -51 -51 |
| B | 374 | 92 | 85 | -10.0 | 8 | 3 | 0 -4 -9 -13 -17 -21 -25 -29 -33 -38 |
| C | 374 | 92 | 85 | -10.0 | 8 | 3 | 0 -4 -9 -13 -17 -21 -25 -29 -33 -38 |
| D | 374 | 92 | 85 | -10.2 | 8 | 3 | 0 -4 -9 -13 -17 -21 -25 -29 -34 -38 |

## Glide (legato step A3 -> A4, dry)

| var | GLIDE | ms to within 50 cents | ms to 90 % of the octave |
|---|---|---|---|
| A | 20 | 4 | 4 |
| B | 56 | 94 | 64 |
| C | 56 | 94 | 64 |
| D | 56 | 94 | 64 |
