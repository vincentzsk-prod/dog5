# Batch 5A round 2, 19 Micro-mist: four fresh takes A-D (rendered, not yet heard; B committed provisionally)

There is no original: the slot was Blackwater (dropped). **Level reading:** RMS dBFS (both channels, one power average) over **+4 s .. +10 s after the note-on of the A3 C#4 E4 chord held 10 s (phrase `z_chord`)**, target -18.0 +-1.5, VOLUME trimmed last; peak = the largest sample over the chord, the tap, the A4 single, the riff and the stabs, limit -4. K-RMS = the same window K-weighted. CPU = idle + stress-chord load, host instr/sample (target <= 2300).

## Takes at a glance

| take | name | VOLUME | held level (RMS) | K-RMS | peak | (b) stabs | CPU (host instr/sample) |
|---|---|---|---|---|---|---|---|
| A | haze | 97 | -17.92 | -15.68 | -4.2 | -21.9 | 2001 (1178 + 823) |
| B | glide | 100 | -19.13 | -17.39 | -4.1 | -23.7 | 2002 (1180 + 822) |
| C | warp | 109 | -18.14 | -15.68 | -4.0 | -22.4 | 2004 (1179 + 825) |
| D | tunnel | 96 | -17.95 | -16.27 | -4.7 | -24.9 | 2000 (1179 + 821) |

## Every parameter, before -> after

B against INIT (the defaults), then A, C and D against B.

**B (glide) against INIT: slow drifting scatter, long echo**

* O1_LVL 110 -> 127 (+13%)
* O2_WAVE SAW -> PULSE
* O2_SEMI +0 -> +12 st
* O2_FINE 70 -> 72 (centre 64: +6 -> +8, +2% of range) (+4.7 cents -> +6.2 cents)
* CUTOFF 80 -> 74 (-5%) (1319 Hz -> 932 Hz)
* RESO 20 -> 50 (+24%)
* FENV_AMT 90 -> 74 (centre 64: +26 -> +10, -13% of range)
* FTYPE LP24 -> BP12
* FA 20 -> 75 (+43%) (2 ms -> 173 ms)
* FD 70 -> 90 (+16%) (117 ms -> 558 ms)
* FS 40 -> 90 (+39%)
* AA 10 -> 70 (+47%) (1 ms -> 117 ms)
* AD 70 -> 100 (+24%) (117 ms -> 1218 ms)
* AS 100 -> 110 (+8%)
* AR 60 -> 95 (+28%) (54 ms -> 825 ms)
* LFO_SHAPE TRI -> RANDOM
* LFO_RATE 70 -> 60 (-8%) (1.70 Hz -> 1.03 Hz)
* LFO_PHASE FREE -> SPREAD
* LFO_PITCH 0 -> 22 (+17%)
* LFO_FLT 0 -> 30 (+24%) (+-0.0 -> +-2.7 st at the filter)
* LFO_AMP 0 -> 8 (+6%)
* VINTAGE 30 -> 40 (+8%)
* SPREAD 60 -> 100 (+31%)
* DLY_FB 50 -> 96 (+36%)
* DLY_TONE 70 -> 100 (+24%)
* DLY_MIX 0 -> 90 (+71%)
* REV_SIZE 80 -> 110 (+24%)
* REV_DAMP 60 -> 20 (-31%)
* REV_PRE 20 -> 10 (-8%)
* REV_MIX 0 -> 70 (+55%)
* POLY_N 5 -> 6 voices
* ALLEY 0 -> 110 (+87%) (SYNC -> 414 ms)
* VOLUME 100 -> 100 (level trim, last)

**A (haze) against B: dense fast flicker, wide shimmer, big spring**

* O2_LVL 100 -> 110 (+8%)
* O2_SEMI +12 -> +19 st
* O2_FINE 72 -> 76 (centre 64: +8 -> +12, +3% of range) (+6.2 cents -> +9.4 cents)
* CUTOFF 74 -> 78 (+3%) (932 Hz -> 1175 Hz)
* LFO_SHAPE RANDOM -> S&H
* LFO_RATE 60 -> 113 (+42%) (1.03 Hz -> 14.82 Hz)
* LFO_PITCH 22 -> 20 (-2%)
* LFO_FLT 30 -> 50 (+16%) (+-2.7 -> +-7.2 st at the filter)
* LFO_AMP 8 -> 30 (+17%)
* DLY_FB 96 -> 80 (-13%)
* DLY_MIX 90 -> 70 (-16%)
* REV_SIZE 110 -> 127 (+13%)
* REV_DAMP 20 -> 15 (-4%)
* REV_MIX 70 -> 100 (+24%)
* ALLEY 110 -> 80 (-24%) (414 ms -> 149 ms)
* VOLUME 100 -> 97 (level trim, last)

**C (warp) against B: resonant band-pass glassy top, the echo repeats the main event**

* CUTOFF 74 -> 80 (+5%) (932 Hz -> 1319 Hz)
* RESO 50 -> 85 (+28%)
* FENV_AMT 74 -> 70 (centre 64: +10 -> +6, -3% of range)
* AA 70 -> 76 (+5%) (117 ms -> 187 ms)
* LFO_SHAPE RANDOM -> S&H
* LFO_RATE 60 -> 100 (+31%) (1.03 Hz -> 7.70 Hz)
* LFO_PITCH 22 -> 0 (-17%)
* LFO_FLT 30 -> 40 (+8%) (+-2.7 -> +-4.5 st at the filter)
* LFO_AMP 8 -> 20 (+9%)
* DLY_FB 96 -> 90 (-5%)
* DLY_MIX 90 -> 120 (+24%)
* REV_MIX 70 -> 30 (-31%)
* ALLEY 110 -> 100 (-8%) (414 ms -> 294 ms)
* VOLUME 100 -> 109 (level trim, last)

**D (tunnel) against B: a held pad hovering on near-100 feedback, minimal flicker**

* CUTOFF 74 -> 70 (-3%) (932 Hz -> 740 Hz)
* RESO 50 -> 40 (-8%)
* AA 70 -> 80 (+8%) (117 ms -> 256 ms)
* AS 110 -> 127 (+13%)
* LFO_SHAPE RANDOM -> S&H
* LFO_RATE 60 -> 105 (+35%) (1.03 Hz -> 9.91 Hz)
* LFO_PITCH 22 -> 0 (-17%)
* LFO_FLT 30 -> 10 (-16%) (+-2.7 -> +-0.0 st at the filter)
* LFO_AMP 8 -> 0 (-6%)
* DLY_FB 96 -> 105 (+7%)
* DLY_MIX 90 -> 95 (+4%)
* REV_MIX 70 -> 80 (+8%)
* ALLEY 110 -> 100 (-8%) (414 ms -> 294 ms)
* VOLUME 100 -> 96 (level trim, last)

## Where the energy is (% of the energy: under 150 / 150-400 / 400-1.2k / over 1.2k Hz; centroid Hz; MUD = 150-400 share over 1.2k+ share)

| take | window | level dB | centroid | bands | MUD |
|---|---|---|---|---|---|
| A | chord 0-1s (with echo + spring) | -17.4 | 2997 | 0 / 1 / 57 / 42 | 0.0 |
| A | chord 1-2s (with echo + spring) | -18.3 | 3289 | 0 / 1 / 47 / 52 | 0.0 |
| A | chord 2-4s (with echo + spring) | -18.0 | 3160 | 0 / 1 / 54 / 45 | 0.0 |
| A | chord 4-10s (with echo + spring) | -17.9 | 3074 | 0 / 1 / 53 / 45 | 0.0 |
| A | chord 0-1s DRY (voice only) | -22.0 | 3228 | 0 / 2 / 52 / 46 | 0.0 |
| A | chord 4-10s DRY (voice only) | -22.3 | 3336 | 0 / 2 / 49 / 49 | 0.0 |
| A | single A4 strike 0-1 s | -21.9 | 3658 | 0 / 0 / 11 / 89 | 0.0 |
| A | single A4 settled 4-6 s | -22.0 | 3752 | 0 / 0 / 8 / 92 | 0.0 |
| B | chord 0-1s (with echo + spring) | -21.0 | 3127 | 0 / 5 / 27 / 68 | 0.1 |
| B | chord 1-2s (with echo + spring) | -20.4 | 2990 | 0 / 4 / 31 / 64 | 0.1 |
| B | chord 2-4s (with echo + spring) | -20.1 | 2895 | 0 / 3 / 36 / 60 | 0.1 |
| B | chord 4-10s (with echo + spring) | -19.1 | 2605 | 0 / 4 / 49 / 47 | 0.1 |
| B | chord 0-1s DRY (voice only) | -22.5 | 3174 | 0 / 4 / 32 / 64 | 0.1 |
| B | chord 4-10s DRY (voice only) | -22.2 | 2768 | 0 / 4 / 41 / 54 | 0.1 |
| B | single A4 strike 0-1 s | -25.5 | 3849 | 0 / 0 / 31 / 69 | 0.0 |
| B | single A4 settled 4-6 s | -22.5 | 2958 | 0 / 0 / 59 / 41 | 0.0 |
| C | chord 0-1s (with echo + spring) | -18.4 | 2874 | 0 / 3 / 30 / 67 | 0.0 |
| C | chord 1-2s (with echo + spring) | -17.8 | 2866 | 0 / 4 / 26 / 70 | 0.1 |
| C | chord 2-4s (with echo + spring) | -18.4 | 3041 | 0 / 4 / 23 / 74 | 0.1 |
| C | chord 4-10s (with echo + spring) | -18.1 | 2951 | 0 / 3 / 26 / 71 | 0.0 |
| C | chord 0-1s DRY (voice only) | -19.1 | 2940 | 0 / 2 / 24 / 74 | 0.0 |
| C | chord 4-10s DRY (voice only) | -19.5 | 3040 | 0 / 2 / 23 / 75 | 0.0 |
| C | single A4 strike 0-1 s | -22.9 | 3627 | 0 / 0 / 25 / 75 | 0.0 |
| C | single A4 settled 4-6 s | -22.6 | 3659 | 0 / 0 / 22 / 78 | 0.0 |
| D | chord 0-1s (with echo + spring) | -19.8 | 2403 | 0 / 6 / 61 / 33 | 0.2 |
| D | chord 1-2s (with echo + spring) | -17.9 | 2338 | 0 / 7 / 51 / 42 | 0.2 |
| D | chord 2-4s (with echo + spring) | -18.4 | 2314 | 0 / 9 / 51 / 39 | 0.2 |
| D | chord 4-10s (with echo + spring) | -17.9 | 2300 | 0 / 8 / 54 / 39 | 0.2 |
| D | chord 0-1s DRY (voice only) | -21.7 | 2540 | 0 / 6 / 50 / 44 | 0.1 |
| D | chord 4-10s DRY (voice only) | -21.0 | 2456 | 0 / 6 / 54 / 40 | 0.2 |
| D | single A4 strike 0-1 s | -24.7 | 3121 | 0 / 0 / 53 / 47 | 0.0 |
| D | single A4 settled 4-6 s | -23.9 | 3023 | 0 / 0 / 55 / 45 | 0.0 |

## The grain flicker (the one shared LFO)

| take | shape / rate | PITCH depth (law, peak) | pitch probe on A4 (s.d. / 5-95 % range, 100 ms frames) | FILTER depth | filter-band swing (95th-5th pct dB) at its strongest rate | AMP dip | chord level swing (20 ms RMS, dB) |
|---|---|---|---|---|---|---|---|
| A | S&H 14.82 Hz | +-28 cents | 15.4 / 48.5 cents | +-7.2 st | 5.2 dB at 4.3 Hz (band 783-1762 Hz) | 2.3 dB | 1.8 dB at 3.5 Hz |
| B | RANDOM 1.03 Hz | +-28 cents | 4.2 / 13.2 cents | +-2.7 st | 5.4 dB at 2.4 Hz (band 622-1398 Hz) | 0.6 dB | 2.1 dB at 2.3 Hz |
| C | S&H 7.70 Hz | +-0 cents | off | +-4.5 st | 5.8 dB at 4.7 Hz (band 879-1978 Hz) | 1.5 dB | 1.9 dB at 7.2 Hz |
| D | S&H 9.91 Hz | +-0 cents | off | +-0.0 st | 4.5 dB at 2.3 Hz (band 493-1110 Hz) | 0.0 dB | 2.1 dB at 2.3 Hz |

## Shimmer and width

| take | beating of the A3 band (dry): rate mean (min..max) Hz, envelope depth dB | L/R correlation 150-4000 Hz dry / with echo + spring | side/mid dB dry / full |
|---|---|---|---|
| A | 3.63 (0.84..7.57), 5.1 | 0.79 / 0.42 | -9.1 / -3.9 |
| B | 1.47 (1.01..4.88), 1.0 | 0.79 / 0.39 | -9.1 / -3.6 |
| C | 2.35 (1.01..4.04), 2.9 | 0.79 / 0.56 | -9.1 / -5.4 |
| D | 3.68 (1.18..7.07), 0.4 | 0.79 / 0.43 | -9.1 / -3.9 |

## Echo and spring (an isolated A4 struck 300 ms; the repeat is a whole copy of the note)

| take | ALLEY ms | first repeat re the note (dB) | peak at (ms) | spring re the note (dB, same window) | echo over spring (dB) | repeats above -40 dB (of 14) | repeats re the first, k = 2..8 |
|---|---|---|---|---|---|---|---|
| A | 149 | -10.2 | 503 | +4.9 | -15.1 | 12 | +2.1 / +3.6 / +0.5 / -0.4 / -3.8 / -6.4 / -10.4 |
| B | 414 | -10.7 | 742 | -5.2 | -5.6 | 10 | -2.0 / -4.7 / -7.7 / -10.9 / -14.1 / -17.3 / -20.5 |
| C | 294 | -8.5 | 537 | -8.5 | -0.1 | 11 | -0.3 / -2.6 / -4.9 / -8.3 / -11.7 / -15.4 / -19.1 |
| D | 294 | -9.6 | 619 | -5.7 | -3.9 | 14 | +0.9 / -0.5 / -2.0 / -3.9 / -5.8 / -8.1 / -10.4 |

## The hover: ms after key-up (the chord held 10 s) for the tail to fall 20 / 40 / 60 dB (None = not reached inside the 6 s render); the tail's band split in four windows

| take | wet: -20 / -40 / -60 dB | dry voice alone | tail 0-0.5 / 0.5-1.5 / 1.5-3 / 3-5.5 s: dB, centroid Hz, bands |
|---|---|---|---|
| A | 1212.0 / 2204.0 / 2814.0 | 690.0 / 1264.0 / 1718.0 | -20 dB, 2181 Hz, 0 / 2 / 74 / 23; -31 dB, 1881 Hz, 0 / 1 / 77 / 23; -52 dB, 1989 Hz, 0 / 0 / 84 / 15; -210 dB, 0 Hz, 0 / 0 / 0 / 0 |
| B | 1752.0 / 4256.0 / None | 724.0 / 1300.0 / 1714.0 | -21 dB, 1702 Hz, 0 / 7 / 72 / 21; -29 dB, 1224 Hz, 0 / 6 / 78 / 16; -39 dB, 1059 Hz, 0 / 6 / 82 / 12; -53 dB, 1483 Hz, 0 / 6 / 87 / 7 |
| C | 1174.0 / 2660.0 / 3752.0 | 692.0 / 1274.0 / 1686.0 | -22 dB, 2324 Hz, 0 / 7 / 39 / 54; -34 dB, 1942 Hz, 0 / 17 / 38 / 45; -49 dB, 1483 Hz, 0 / 23 / 47 / 30; -73 dB, 2700 Hz, 5 / 27 / 53 / 16 |
| D | 1596.0 / 4132.0 / 5788.0 | 734.0 / 1304.0 / 1730.0 | -22 dB, 1660 Hz, 0 / 18 / 69 / 13; -32 dB, 1317 Hz, 0 / 32 / 54 / 14; -41 dB, 1151 Hz, 0 / 31 / 60 / 9; -55 dB, 1802 Hz, 0 / 30 / 64 / 6 |

## Taps (150 ms)

| take | chord tap re the held level (dB) | chord tap centroid Hz | A4 tap re the held level | hover after the chord tap -20 / -40 / -60 dB (ms) | after the A4 tap |
|---|---|---|---|---|---|
| A | -3.9 | 3240 | -8.1 | 1330.0 / 2172.0 / 2710.0 | 1400.0 / 2284.0 / 2694.0 |
| B | -4.7 | 3268 | -8.1 | 1646.0 / 4138.0 / None | 1874.0 / 4016.0 / None |
| C | -3.9 | 3281 | -8.3 | 1458.0 / 2910.0 / 4050.0 | 1622.0 / 2856.0 / 3482.0 |
| D | -8.7 | 2556 | -13.4 | 2280.0 / None / None | 2246.0 / 4302.0 / None |

## Self-oscillation probe (oscillators off, noise-fed, note A3; diff 12 dB = linear, 0 = the filter sings by itself)

| take | RESO | diff dB |
|---|---|---|
| A | 50 | 12.3 |
| A | 127 | 0.0 |
| B | 50 | 12.4 |
| B | 127 | -0.0 |
| C | 85 | 12.2 |
| C | 127 | 0.0 |
| D | 40 | 12.4 |
| D | 127 | -0.0 |

Per-phrase peaks (dBFS): A: z_chord -4.2, z_tap -6.0, a_riff -7.6, b_stabs -5.3, z_single -7.3; B: z_chord -4.1, z_tap -8.4, a_riff -10.1, b_stabs -7.3, z_single -7.9; C: z_chord -4.0, z_tap -6.1, a_riff -8.7, b_stabs -7.2, z_single -7.2; D: z_chord -4.7, z_tap -9.8, a_riff -13.7, b_stabs -8.5, z_single -9.8

