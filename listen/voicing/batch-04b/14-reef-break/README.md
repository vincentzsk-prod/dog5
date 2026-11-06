# Batch 4B, 14 Reef Break: variants and numbers

Chapter II (The Tidal Hexes). Round 1, **rendered, not yet heard**. Method and definitions: `dog5-docs/voicing/README.md` section 17. Level phrase: `u_crash` (own phrase, effects included, tails excluded), reference -18.0 dBFS RMS +-1.5, peak <= -4. WAVs (`<dir>_<KEY>_<ghost|crash|stabs>.wav`) are on the never-merged listen branch only.

## Variants

* **A original**: the nearest-base patch as it stood (PERC HIT, 14's alone: noise 60 + a saw and a saw +24 st, LP12 with a filter envelope, spring, no echo).
* **B burst** (RECOMMENDED, committed): near-instant attack, medium tail (top band 20 / 40 dB down in ~0.5 / ~0.9 s), echo FEEDBK 96 MIX 90 at 361 ms.
* **C swell**: a quick swell (peak in ~10-40 ms), the longest tail, echo FEEDBK 100 MIX 80.
* **D runaway**: near-instant attack, the shortest tail, a near-runaway echo (FEEDBK 114 MIX 100, 337 ms).

## Numbers

| | A original | B burst | C swell | D runaway |
|---|---|---|---|---|
| VOLUME | 100 | 118 | 121 | 124 |
| level, crash phrase (u: 11 hits x 300 ms gates) (dBFS RMS, note-on region, effects in, tails out; reference -18.0 +-1.5) | -47.94 | -19.85 | -18.02 | -20.11 |
| phrase (b) RMS (dBFS) / minus the level phrase (dB) | -44.4 / +3.5 | -14.3 / +5.5 | -12.8 / +5.2 | -14.4 / +5.7 |
| peak of the own phrase (dBFS) / whole renders incl. (b) (limit -4 on the own phrase) | -11.1 / -7.9 | -4.3 / -1.0 | -4.5 / -1.5 | -4.5 / -1.7 |
| clipped samples in all renders | 0 | 0 | 0 | 0 |
| crest factor, own phrase (dB) | 31.9 | 15.6 | 13.5 | 15.6 |
| K-weighted RMS, (b) (dBFS) | -43.5 | -11.4 | -9.9 | -11.3 |
| note-on region: centroid (Hz) | 1926 | 10540 | 10579 | 10664 |
| note-on region: band split % <60 / 60-150 / 150-400 / 400-1.2k / 1.2k+ | 0 / 35 / 39 / 18 / 8 | 4 / 9 / 5 / 4 / 77 | 3 / 8 / 5 / 5 / 79 | 2 / 6 / 4 / 5 / 84 |
| MUD = share(150-400) / share(1.2k+), note-on region | 5.1 | 0.1 | 0.1 | 0.1 |
| worst-case CPU (host instr/sample: idle + load) | 1762 (1164 + 598) | 1832 (1180 + 653) | 1857 (1180 + 677) | 1827 (1180 + 648) |
| amp attack of the hit (voice alone), A1: 10 / 50 / 90 % of the peak (ms) [AA] | 0.0 / 0.5 / 1.7 [1] | 0.0 / 0.2 / 8.5 [0] | 2.2 / 8.7 / 27.2 [52] | 1.2 / 7.2 / 8.7 [44] |
| same on A2 | 0.0 / 0.5 / 1.5 | 0.0 / 0.7 / 5.0 | 2.7 / 12.2 / 32.2 | 1.5 / 5.5 / 14.2 |
| shape: filter / CUTOFF byte (Hz at C4) / ENV AMT (centre 64) / FD / AD / AR / NOISE / O1 lvl / O2 lvl | LP12 / 90 (2349) / 124 / 25 / 30 / 25 / 60 / 110 / 100 | HP12 / 100 (4186) / 0 / 100 / 92 / 92 / 127 / 80 / 45 | HP12 / 100 (4186) / 0 / 100 / 97 / 97 / 127 / 80 / 45 | HP12 / 100 (4186) / 0 / 92 / 88 / 88 / 127 / 80 / 45 |
| NOT A BLOW-OUT: own-phrase peak seed 1 / seed 2 (dBFS); crest seed 1 / seed 2 (dB) | -11.1 / -12.9; 31.9 / 34.2 | -4.3 / -4.6; 15.6 / 15.3 | -4.5 / -4.3; 13.5 / 13.7 | -4.5 / -4.2; 15.6 / 15.8 |
| level seed 1 / seed 2 (dBFS RMS) | -47.94 / -49.44 | -19.85 / -19.83 | -18.02 / -18.00 | -20.11 / -20.04 |
| share of samples within 10 % of the rail (first hit / mean of all 11 gates, %) | 4 / 4 | 2 / 2 | 2 / 2 | 2 / 2 |
| noise-to-sub level in the first 100 ms: A1 / A2 (dB; + = noise louder) | -25.7 / -25.7 | +4.6 / +3.4 | +4.7 / +3.5 | +5.9 / +4.1 |
| sub: share of the sub-only A1 hit's first 150 ms <60 / 60-150 / 150-400 / 400-1.2k / 1.2k+ % | 13 / 31 / 50 / 5 / 1 | 42 / 28 / 22 / 6 / 3 | 41 / 28 / 22 / 6 / 3 | 26 / 30 / 29 / 9 / 5 |
| sub: same on A2 | 7 / 28 / 37 / 21 / 7 | 0 / 71 / 17 / 8 / 5 | 0 / 71 / 17 / 8 / 5 | 0 / 64 / 20 / 10 / 6 |
| sub's 40-150 Hz band to -20 / -40 dB after its peak (ms, A1) | 12 / 12 | 163 / 279 | 174 / 290 | 93 / 163 |
| band 60-150 Hz, A1 hit (voice alone), dB re the loudest band-window, windows 0-50 / 50-150 / 150-400 / 400-800 / 800-1500 ms | -1 / -86 / -86 / -86 / -86 | -5 / -9 / -30 / -82 / -83 | -6 / -9 / -28 / -79 / -86 | -5 / -18 / -54 / -86 / -83 |
| band 150-400 Hz, A1 hit (voice alone), dB re the loudest band-window, windows 0-50 / 50-150 / 150-400 / 400-800 / 800-1500 ms | 0 / -86 / -86 / -86 / -86 | -10 / -9 / -19 / -73 / -79 | -11 / -9 / -18 / -67 / -78 | -10 / -12 / -37 / -79 / -85 |
| band 400-1.2k Hz, A1 hit (voice alone), dB re the loudest band-window, windows 0-50 / 50-150 / 150-400 / 400-800 / 800-1500 ms | -9 / -86 / -86 / -86 / -86 | -11 / -11 / -15 / -57 / -73 | -12 / -11 / -13 / -50 / -63 | -11 / -12 / -24 / -65 / -82 |
| band 1.2k-4k Hz, A1 hit (voice alone), dB re the loudest band-window, windows 0-50 / 50-150 / 150-400 / 400-800 / 800-1500 ms | -16 / -86 / -86 / -86 / -86 | -7 / -8 / -10 / -33 / -54 | -8 / -8 / -8 / -27 / -40 | -7 / -9 / -14 / -41 / -73 |
| band 4k+ Hz, A1 hit (voice alone), dB re the loudest band-window, windows 0-50 / 50-150 / 150-400 / 400-800 / 800-1500 ms | -26 / -86 / -86 / -86 / -86 | -0 / 0 / -3 / -15 / -35 | -1 / 0 / -1 / -8 / -21 | 0 / -1 / -6 / -23 / -56 |
| band 60-150 Hz: to -20 / -40 dB after its own peak (ms), A1 / A2 | 6 / 9; 6 / 9 | 96 / 267; 218 / 296 | 78 / 250; 200 / 255 | 41 / 174; 122 / 194 |
| band 400-1.2k Hz: to -20 / -40 dB after its own peak (ms), A1 / A2 | 6 / 12; 6 / 12 | 276 / 331; 282 / 311 | 244 / 279; 284 / 322 | 229 / 308; 209 / 290 |
| band 1.2k-4k Hz: to -20 / -40 dB after its own peak (ms), A1 / A2 | 6 / 12; 6 / 12 | 316 / 641; 287 / 639 | 316 / 856; 308 / 908 | 273 / 444; 287 / 485 |
| band 4k+ Hz: to -20 / -40 dB after its own peak (ms), A1 / A2 | 9 / 12; 9 / 12 | 482 / 932; 473 / 958 | 665 / 1329; 702 / 1402 | 348 / 697; 340 / 702 |
| the whole voice (sends off) after the gate to -20 / -40 / -60 dB (ms, DC out) | >win / >win / >win | 372 / 808 / 1130 | 590 / 1244 / >win | 270 / 588 / 806 |
| echo: ALLEY (ms) / FEEDBK / MIX / TONE | 10 / 50 / 0 / 70 | 361 / 96 / 90 / 70 | 361 / 100 / 80 / 70 | 337 / 114 / 100 / 70 |
| the first repeats 1..6 re the burst's peak (dB) | -181 -181 -181 -181 -181 -181 | -12 -18 -23 -27 -31 -34 | -13 -18 -24 -28 -31 -35 | -11 -15 -18 -20 -21 -23 |
| repeats above -40 dB re the burst (of 16 slots, 5.4 s) | 0 | 7 | 7 | 16 |
| echo stays below clipping: peak of the isolated hit with echo (dBFS) / clipped samples | -22.0 / 0 | -5.7 / 0 | -5.3 / 0 | -5.4 / 0 |
| the sub in the repeats: MUD / centroid Hz / % 60-150 in repeat slots 1, 2, 3 | 0 / 0 / 0 ; 0 / 0 / 0 ; 0 / 0 / 0 | 1 / 2206 / 20 ; 2 / 1514 / 17 ; 3 / 1146 / 13 | 1 / 2242 / 19 ; 2 / 1702 / 15 ; 3 / 1325 / 11 | 1 / 2305 / 20 ; 1 / 1466 / 16 ; 2 / 1125 / 12 |
| echo under the figure's hits (delay return re the hit in its 300 ms gate, dB; hits 3-11) | -145 -137 -168 -145 -138 -163 -148 -143 -150 | -49 -25 -24 -31 -20 -20 -30 -17 -16 | -46 -25 -24 -30 -21 -20 -29 -17 -17 | -32 -20 -19 -23 -18 -16 -22 -17 -16 |
| the isolated hit with echo, to -20 / -40 / -60 dB (ms, DC out) | 310 / 500 / 526 | 390 / 1104 / 1488 | 684 / 1462 / 1848 | 326 / 704 / 3716 |
| A1 hit as rendered with echo: 4k+ band to -20 / -40 dB (ms) | 168 / 763 | 482 / 940 | 665 / 1332 | 360 / 705 |

## Parameter changes, each before -> after (the original is the nearest-base patch as it stood; variant A is that patch)

### B burst

* O1_WAVE SAW -> PULSE
* O1_LVL 110 -> 80 (-24%)
* NOISE 60 -> 127 (+53%)
* O2_WAVE SAW -> PULSE
* O2_LVL 100 -> 45 (-43%)
* O2_SEMI +24 -> +12 st
* O2_FINE 70 -> 64 (centre 64: +6 -> +0, -5% of range) (+4.7 cents -> +0.0 cents)
* CUTOFF 90 -> 100 (+8%) (2349 Hz -> 4186 Hz)
* RESO 30 -> 10 (-16%)
* FENV_AMT 124 -> 0 (centre 64: +60 -> -64, -98% of range)
* KEYTRK 64 -> 0 (-50%)
* FTYPE LP12 -> HP12
* FA 20 -> 0 (-16%) (2 ms -> 0 ms)
* FD 25 -> 100 (+59%) (4 ms -> 1218 ms)
* AA 1 -> 0 (-1%) (1 ms -> 0 ms)
* AD 30 -> 92 (+49%) (5 ms -> 653 ms)
* AR 25 -> 92 (+53%) (4 ms -> 653 ms)
* VOLUME 100 -> 118 (+14%)
* DLY_FB 50 -> 96 (+36%)
* DLY_MIX 0 -> 90 (+71%)
* REV_MIX 40 -> 0 (-31%)
* ALLEY 0 -> 106 (+83%) (SYNC -> 361 ms)

### C swell

* O1_WAVE SAW -> PULSE
* O1_LVL 110 -> 80 (-24%)
* NOISE 60 -> 127 (+53%)
* O2_WAVE SAW -> PULSE
* O2_LVL 100 -> 45 (-43%)
* O2_SEMI +24 -> +12 st
* O2_FINE 70 -> 64 (centre 64: +6 -> +0, -5% of range) (+4.7 cents -> +0.0 cents)
* CUTOFF 90 -> 100 (+8%) (2349 Hz -> 4186 Hz)
* RESO 30 -> 10 (-16%)
* FENV_AMT 124 -> 0 (centre 64: +60 -> -64, -98% of range)
* KEYTRK 64 -> 0 (-50%)
* FTYPE LP12 -> HP12
* FA 20 -> 0 (-16%) (2 ms -> 0 ms)
* FD 25 -> 100 (+59%) (4 ms -> 1218 ms)
* AA 1 -> 52 (+40%) (1 ms -> 29 ms)
* AD 30 -> 97 (+53%) (5 ms -> 964 ms)
* AR 25 -> 97 (+57%) (4 ms -> 964 ms)
* VOLUME 100 -> 121 (+17%)
* DLY_FB 50 -> 100 (+39%)
* DLY_MIX 0 -> 80 (+63%)
* REV_MIX 40 -> 0 (-31%)
* ALLEY 0 -> 106 (+83%) (SYNC -> 361 ms)

C against B:

* AA 0 -> 52 (+41%) (0 ms -> 29 ms)
* AD 92 -> 97 (+4%) (653 ms -> 964 ms)
* AR 92 -> 97 (+4%) (653 ms -> 964 ms)
* DLY_FB 96 -> 100 (+3%)
* DLY_MIX 90 -> 80 (-8%)

### D runaway

* O1_WAVE SAW -> PULSE
* O1_LVL 110 -> 80 (-24%)
* NOISE 60 -> 127 (+53%)
* O2_WAVE SAW -> PULSE
* O2_LVL 100 -> 45 (-43%)
* O2_SEMI +24 -> +12 st
* O2_FINE 70 -> 64 (centre 64: +6 -> +0, -5% of range) (+4.7 cents -> +0.0 cents)
* CUTOFF 90 -> 100 (+8%) (2349 Hz -> 4186 Hz)
* RESO 30 -> 10 (-16%)
* FENV_AMT 124 -> 0 (centre 64: +60 -> -64, -98% of range)
* KEYTRK 64 -> 0 (-50%)
* FTYPE LP12 -> HP12
* FA 20 -> 0 (-16%) (2 ms -> 0 ms)
* FD 25 -> 92 (+53%) (4 ms -> 653 ms)
* AA 1 -> 44 (+34%) (1 ms -> 15 ms)
* AD 30 -> 88 (+46%) (5 ms -> 478 ms)
* AR 25 -> 88 (+50%) (4 ms -> 478 ms)
* VOLUME 100 -> 124 (+19%)
* DLY_FB 50 -> 114 (+50%)
* DLY_MIX 0 -> 100 (+79%)
* REV_MIX 40 -> 0 (-31%)
* ALLEY 0 -> 104 (+82%) (SYNC -> 337 ms)

D against B:

* FD 100 -> 92 (-6%) (1218 ms -> 653 ms)
* AA 0 -> 44 (+35%) (0 ms -> 15 ms)
* AD 92 -> 88 (-3%) (653 ms -> 478 ms)
* AR 92 -> 88 (-3%) (653 ms -> 478 ms)
* DLY_FB 96 -> 114 (+14%)
* DLY_MIX 90 -> 100 (+8%)
* ALLEY 106 -> 104 (-2%) (361 ms -> 337 ms)

