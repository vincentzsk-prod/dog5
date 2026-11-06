# Batch 4B, 13 Ghost Board: variants and numbers

Chapter II (The Tidal Hexes). Round 1, **rendered, not yet heard**. Method and definitions: `dog5-docs/voicing/README.md` section 17. Level phrase: `t_ghost` (own phrase, effects included, tails excluded), reference -18.0 dBFS RMS +-1.5, peak <= -4. WAVs (`<dir>_<KEY>_<ghost|crash|stabs>.wav`) are on the never-merged listen branch only.

## Variants

* **A original**: the nearest-base patch as it stood (PWM STRINGS, 13's alone now: two pulses with PWM, LP24, a spring, no echo, no tape, inert LFO PITCH 3).
* **B middle** (RECOMMENDED, committed): the middle: soft near-triangle tone, tape CHEW 100 (wow-leaning), echo 275 ms FEEDBK 82 MIX 70, spring DRAIN 50.
* **C tape**: leans Mellotron: clearer tone (CUTOFF 60, less octave), the most tape (CHEW 127, wow), less echo (MIX 40, FEEDBK 60) and spring.
* **D echo**: leans Space Echo: richer body (CUTOFF 66, more octave), CHEW 70, long rich echo (MIX 110, FEEDBK 100, 387 ms), more spring (DRAIN 80, SIZE 100, DAMP 55).

## Numbers

| | A original | B middle | C tape | D echo |
|---|---|---|---|---|
| VOLUME | 100 | 81 | 95 | 62 |
| level, ghost phrase (t) (dBFS RMS, note-on region, effects in, tails out; reference -18.0 +-1.5) | -13.21 | -18.04 | -17.98 | -17.88 |
| phrase (b) RMS (dBFS) / minus the level phrase (dB) | -14.2 / -0.9 | -19.7 / -1.7 | -18.7 / -0.7 | -23.4 / -5.5 |
| peak of the own phrase (dBFS) / whole renders incl. (b) (limit -4 on the own phrase) | -0.2 / -0.2 | -5.2 / -5.2 | -5.6 / -5.6 | -5.0 / -5.0 |
| clipped samples in all renders | 0 | 0 | 0 | 0 |
| crest factor, own phrase (dB) | 13.0 | 12.9 | 12.4 | 12.9 |
| K-weighted RMS, (b) (dBFS) | -14.8 | -20.3 | -19.4 | -24.0 |
| note-on region: centroid (Hz) | 609 | 1064 | 1086 | 812 |
| note-on region: band split % <60 / 60-150 / 150-400 / 400-1.2k / 1.2k+ | 0 / 0 / 78 / 22 / 1 | 0 / 0 / 68 / 28 / 4 | 2 / 0 / 71 / 23 / 3 | 0 / 0 / 72 / 26 / 1 |
| MUD = share(150-400) / share(1.2k+), note-on region | 108.2 | 18.6 | 22.6 | 49.3 |
| worst-case CPU (host instr/sample: idle + load) | 2069 (1164 + 905) | 2679 (1948 + 731) | 2679 (1948 + 731) | 2680 (1948 + 731) |
| amp attack (one voice, LFO off) 10 / 50 / 90 % (ms); AA | 3 / 14 / 27; 60 | 2 / 6 / 15; 45 | 2 / 6 / 15; 45 | 2 / 6 / 15; 45 |
| tone: filter / CUTOFF (Hz at C4) / key tracking % / O1 PW % / O2 semis / O2 level | LP24 / 988 / 50 / 50 / +0 / 100 | LP12 / 740 / 100 / 25 / +24 / 112 | LP12 / 523 / 100 / 25 / +24 / 125 | LP12 / 740 / 100 / 25 / +24 / 112 |
| harmonics 3 / 5 / 7 re the fundamental, OSC 1 through the filter at rest (dB; triangle -19.1 / -28.0 / -34.2, square -9.5 / -14.0 / -16.9) | -10.9 / -18.4 / -26.0 | -14.5 / -23.2 / -32.1 | -17.2 / -27.3 / -36.8 | -14.4 / -23.2 / -32.0 |
| LFO PITCH (inert below 12) / LFO PWM | 3 / 60 | 0 / 0 | 0 / 0 | 0 / 0 |
| tape: CHEW / WOW-FLT / HISS / DROPS | 0 / 64 / 64 / 64 | 100 / 48 / 40 / 50 | 127 / 32 / 32 / 50 | 70 / 64 / 40 / 50 |
| tape wobble, one voice A3, sends off: pitch s.d. cents / 5-95 % range cents / strongest rate Hz (0.1-8 Hz) | 0.0 / 0.0 / 7.0 | 6.2 / 22.3 / 0.5 | 6.6 / 23.2 / 0.5 | 4.2 / 13.3 / 0.5 |
| same with CHEW 0 (the voice alone): s.d. cents | 0.0 | 0.0 | 0.0 | 0.0 |
| tape dropouts in the held note: dips >= 6 dB (n / deepest dB) | 0 / 0.1 | 1 / 7.5 | 0 / 5.7 | 0 / 0.2 |
| does the deck smear the top? note-on centroid Hz / % above 1.2 kHz / MUD, with the deck -> CHEW 0 | 609 / 0.7 / 108.2 -> 610 / 0.7 / 107.9 | 1064 / 3.7 / 18.6 -> 825 / 4.6 / 14.1 | 1086 / 3.2 / 22.6 -> 744 / 4.3 / 15.6 | 812 / 1.5 / 49.3 -> 725 / 1.7 / 41.3 |
| width, held chord: L/R correlation dry (full) | 0.80 (0.80) | 0.80 (0.79) | 0.80 (0.79) | 0.80 (0.85) |
| echo: ALLEY (ms) / FEEDBK / MIX / PINGPONG | 10 / 50 / 0 / 127 | 275 / 82 / 70 / 127 | 275 / 60 / 40 / 127 | 337 / 95 / 105 / 127 |
| first repeat of an isolated 150 ms E4: peak re the dry note's peak (dB) / at ms after the note-on | - / -20 | -12.2 / 403 | -17.4 / 302 | -8.8 / 374 |
| spring in the same window re the note (dB); the echo's margin over it (dB) | -17.5 ; - | -19.8 ; 7.6 | -24.5 ; 7.1 | -18.2 ; 9.4 |
| the repeats 1..6 (dB re the first) | +0.0 +0.0 +0.0 +0.0 +0.0 +0.0 | +0.0 -4.3 -9.0 -13.8 -18.5 -23.3 | +0.0 -6.7 -14.2 -22.0 -29.7 -37.3 | +0.0 -3.3 -6.7 -10.1 -13.6 -17.0 |
| the first repeat's spectrum: centroid Hz / MUD | 0 / 0.0 | 924 / 6.3 | 891 / 9.4 | 956 / 5.9 |
| echo under the figure's first four short notes (dB re the note) | - / - / - / - | -37.8 / -17.7 / -16.7 / -16.2 | -45.9 / -23.5 / -23.2 / -22.7 | -24.4 / -11.2 / -11.2 / -10.0 |
| spring (DRAIN, SIZE, DAMP) | 35 (28 %), 100, 60 | 50 (39 %), 90, 40 | 35 (28 %), 80, 40 | 70 (55 %), 100, 25 |
| isolated E4, spring return re the note 0-20 / 20-100 / 100-250 ms (dB) | -45.9 / -19.1 / -18.2 | -38.3 / -13.6 / -12.9 | -42.4 / -17.1 / -16.6 | -35.3 / -10.6 / -9.6 |
| after the held chord's note-off: echo return re the chord (dB) 0-100 / 100-250 / 250-500 / 500-1000 / 1000-2000 ms | - / - / - / - / - | -10.6 / -11.3 / -13.8 / -19.7 / -30.4 | -16.1 / -16.0 / -20.0 / -28.8 / -45.2 | -6.0 / -6.1 / -7.2 / -10.8 / -17.7 |
| same, spring return (dB) | -0.2 / -3.1 / -7.9 / -14.9 / -31.3 | 0.3 / -2.8 / -7.5 / -18.2 / -38.7 | -3.9 / -6.4 / -12.9 / -25.4 / -49.8 | 4.5 / 2.5 / -2.2 / -11.4 / -29.0 |
| the tail after the chord: MUD / centroid Hz / level dBFS in 0-250 / 250-750 / 750-1500 ms | 1028 / 477 / -12 ; 2345 / 509 / -21 ; 5877 / 662 / -36 | 74 / 1103 / -19 ; 89 / 1924 / -28 ; 17 / 4191 / -42 | 62 / 1203 / -20 ; 118 / 2963 / -32 ; 3 / 7207 / -50 | 225 / 757 / -15 ; 298 / 851 / -20 ; 305 / 1231 / -27 |
| tail after the held chord to -20 / -40 / -60 dB (ms, DC out; with the deck -> CHEW 0) | 770 / 1478 / 2054 -> 770 / 1480 / 2058 | 646 / 1778 / >win -> 644 / 1662 / >win | 492 / 1198 / >win -> 476 / 1062 / 1708 | 1644 / >win / >win -> 1640 / >win / >win |

## Parameter changes, each before -> after (the original is the nearest-base patch as it stood; variant A is that patch)

### B middle

* O1_PW 64 -> 32 (-25%)
* O2_PW 40 -> 32 (-6%)
* O2_LVL 100 -> 112 (+9%)
* O2_SEMI +0 -> +24 st
* O2_FINE 73 -> 64 (centre 64: +9 -> +0, -7% of range) (+7.0 cents -> +0.0 cents)
* CUTOFF 75 -> 70 (-4%) (988 Hz -> 740 Hz)
* RESO 5 -> 0 (-4%)
* FENV_AMT 74 -> 64 (centre 64: +10 -> +0, -8% of range)
* KEYTRK 64 -> 127 (+50%)
* FTYPE LP24 -> LP12
* AA 60 -> 45 (-12%) (54 ms -> 17 ms)
* AS 100 -> 127 (+21%)
* AR 90 -> 80 (-8%) (558 ms -> 256 ms)
* LFO_PITCH 3 -> 0 (-2%)
* LFO_PWM 60 -> 0 (-47%)
* VOLUME 100 -> 81 (-15%)
* DLY_FB 50 -> 82 (+25%)
* DLY_MIX 0 -> 70 (+55%)
* REV_SIZE 100 -> 90 (-8%)
* REV_DAMP 60 -> 40 (-16%)
* REV_MIX 35 -> 50 (+12%)
* CHEW 0 -> 100 (+79%)
* TP_WOWFLT 64 -> 48 (-13%)
* TP_HISS 64 -> 40 (-19%)
* TP_DROPS 64 -> 50 (-11%)
* ALLEY 0 -> 98 (+77%) (SYNC -> 275 ms)

### C tape

* O1_PW 64 -> 32 (-25%)
* O2_PW 40 -> 32 (-6%)
* O2_LVL 100 -> 125 (+20%)
* O2_SEMI +0 -> +24 st
* O2_FINE 73 -> 64 (centre 64: +9 -> +0, -7% of range) (+7.0 cents -> +0.0 cents)
* CUTOFF 75 -> 64 (-9%) (988 Hz -> 523 Hz)
* RESO 5 -> 0 (-4%)
* FENV_AMT 74 -> 64 (centre 64: +10 -> +0, -8% of range)
* KEYTRK 64 -> 127 (+50%)
* FTYPE LP24 -> LP12
* AA 60 -> 45 (-12%) (54 ms -> 17 ms)
* AS 100 -> 127 (+21%)
* AR 90 -> 80 (-8%) (558 ms -> 256 ms)
* LFO_PITCH 3 -> 0 (-2%)
* LFO_PWM 60 -> 0 (-47%)
* VOLUME 100 -> 95 (-4%)
* DLY_FB 50 -> 60 (+8%)
* DLY_MIX 0 -> 40 (+31%)
* REV_SIZE 100 -> 80 (-16%)
* REV_DAMP 60 -> 40 (-16%)
* CHEW 0 -> 127 (+100%)
* TP_WOWFLT 64 -> 32 (-25%)
* TP_HISS 64 -> 32 (-25%)
* TP_DROPS 64 -> 50 (-11%)
* ALLEY 0 -> 98 (+77%) (SYNC -> 275 ms)

C against B:

* O2_LVL 112 -> 125 (+10%)
* CUTOFF 70 -> 64 (-5%) (740 Hz -> 523 Hz)
* DLY_FB 82 -> 60 (-17%)
* DLY_MIX 70 -> 40 (-24%)
* REV_SIZE 90 -> 80 (-8%)
* REV_MIX 50 -> 35 (-12%)
* CHEW 100 -> 127 (+21%)
* TP_WOWFLT 48 -> 32 (-13%)
* TP_HISS 40 -> 32 (-6%)

### D echo

* O1_PW 64 -> 32 (-25%)
* O2_PW 40 -> 32 (-6%)
* O2_LVL 100 -> 112 (+9%)
* O2_SEMI +0 -> +24 st
* O2_FINE 73 -> 64 (centre 64: +9 -> +0, -7% of range) (+7.0 cents -> +0.0 cents)
* CUTOFF 75 -> 70 (-4%) (988 Hz -> 740 Hz)
* RESO 5 -> 0 (-4%)
* FENV_AMT 74 -> 64 (centre 64: +10 -> +0, -8% of range)
* KEYTRK 64 -> 127 (+50%)
* FTYPE LP24 -> LP12
* AA 60 -> 45 (-12%) (54 ms -> 17 ms)
* AS 100 -> 127 (+21%)
* AR 90 -> 80 (-8%) (558 ms -> 256 ms)
* LFO_PITCH 3 -> 0 (-2%)
* LFO_PWM 60 -> 0 (-47%)
* VOLUME 100 -> 62 (-30%)
* DLY_FB 50 -> 95 (+35%)
* DLY_MIX 0 -> 105 (+83%)
* REV_DAMP 60 -> 25 (-28%)
* REV_MIX 35 -> 70 (+28%)
* CHEW 0 -> 70 (+55%)
* TP_HISS 64 -> 40 (-19%)
* TP_DROPS 64 -> 50 (-11%)
* ALLEY 0 -> 104 (+82%) (SYNC -> 337 ms)

D against B:

* DLY_FB 82 -> 95 (+10%)
* DLY_MIX 70 -> 105 (+28%)
* REV_SIZE 90 -> 100 (+8%)
* REV_DAMP 40 -> 25 (-12%)
* REV_MIX 50 -> 70 (+16%)
* CHEW 100 -> 70 (-24%)
* TP_WOWFLT 48 -> 64 (+13%)
* ALLEY 98 -> 104 (+5%) (275 ms -> 337 ms)

