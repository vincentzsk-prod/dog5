# Batch 5A, 19 Blackwater: variants A-D (round 1, rendered, not yet heard)

**Level reading:** RMS dBFS (both channels, one power average) over **+5 s .. +14 s after the note-on of the 15 s hold on the phrase `v_drone_lo`** (the held, settled state; the note-on is at 3 s), target -18.0 +-1.5, VOLUME trimmed last; peak = the largest sample of any audition phrase (riff, stabs, held, drone, chord, taps), limit -4. `first 1 s` = RMS over the first second of the same hold. K-RMS = the same window K-weighted (informational). Worst-case CPU = idle + stress-chord load, host instructions per sample (a relative yardstick; 2900 us aim / 5800 us limit are device numbers).

## Variants at a glance

| variant | name | VOLUME | held level (RMS) | K-RMS | first 1 s | (b) stabs | peak (all phrases) | clipped | chord voices gated | worst-case CPU (host instr/sample) |
|---|---|---|---|---|---|---|---|---|---|---|
| A | original | 100 | -24.80 | -28.34 | -24.4 | -29.6 | -15.6 | 0 | 1 | 1361 |
| B | ring | 127 | -18.20 | -23.07 | -14.7 | -13.8 | -6.2 | 0 | 1 | 1430 |
| C | singing | 122 | -18.01 | -21.61 | -14.5 | -13.6 | -5.5 | 0 | 1 | 1432 |
| D | low-floor | 127 | -18.21 | -23.35 | -14.3 | -13.7 | -6.4 | 0 | 1 | 1431 |
| A* | original, level-matched | 127 | -20.67 | - | - | - | -11.5 | - | - | - |

A* is the original's tone with VOLUME alone moved as near the reference as the knob allows (a listening aid, not a candidate).

## Every change, before -> after (against A, the original)

**B (ring): OSC 2 pulse (PW 40) an octave down alone, LP24 RESO 115 at 100 % key tracking, filter envelope opens it and sinks over ~2 s, amp decay ~3 s to sustain, release ~2 s**

* O1_WAVE PULSE -> OFF
* O2_WAVE SAW -> PULSE
* O2_PW 64 -> 40 (-19%)
* O2_LVL 60 -> 110 (+39%)
* CUTOFF 35 -> 70 (+28%) (98 Hz -> 740 Hz)
* RESO 10 -> 115 (+83%)
* FENV_AMT 84 -> 94 (centre 64: +20 -> +30, +8% of range)
* KEYTRK 64 -> 127 (+50%) (50 % -> 99 % tracking)
* FA 20 -> 0 (-16%) (2 ms -> 0 ms)
* FD 50 -> 105 (+43%) (25 ms -> 1799 ms)
* AA 1 -> 20 (+15%) (1 ms -> 2 ms)
* AD 60 -> 112 (+41%) (54 ms -> 3105 ms)
* AS 100 -> 70 (-24%)
* AR 20 -> 105 (+67%) (2 ms -> 1799 ms)
* VOLUME 100 -> 127 (level trim, last)

**C (singing): B with RESO 125: past the edge, the filter sings by itself**

* O1_WAVE PULSE -> OFF
* O2_WAVE SAW -> PULSE
* O2_PW 64 -> 40 (-19%)
* O2_LVL 60 -> 110 (+39%)
* CUTOFF 35 -> 70 (+28%) (98 Hz -> 740 Hz)
* RESO 10 -> 125 (+91%)
* FENV_AMT 84 -> 94 (centre 64: +20 -> +30, +8% of range)
* KEYTRK 64 -> 127 (+50%) (50 % -> 99 % tracking)
* FA 20 -> 0 (-16%) (2 ms -> 0 ms)
* FD 50 -> 105 (+43%) (25 ms -> 1799 ms)
* AA 1 -> 20 (+15%) (1 ms -> 2 ms)
* AD 60 -> 112 (+41%) (54 ms -> 3105 ms)
* AS 100 -> 70 (-24%)
* AR 20 -> 105 (+67%) (2 ms -> 1799 ms)
* VOLUME 100 -> 122 (level trim, last)

**D (low-floor): B with a lower cutoff floor (CUTOFF 58, KEY TRK 80), RESO 110, the longest filter decay / amp decay / release**

* O1_WAVE PULSE -> OFF
* O2_WAVE SAW -> PULSE
* O2_PW 64 -> 40 (-19%)
* O2_LVL 60 -> 110 (+39%)
* CUTOFF 35 -> 58 (+18%) (98 Hz -> 370 Hz)
* RESO 10 -> 110 (+79%)
* FENV_AMT 84 -> 100 (centre 64: +20 -> +36, +13% of range)
* KEYTRK 64 -> 80 (+13%) (50 % -> 62 % tracking)
* FA 20 -> 0 (-16%) (2 ms -> 0 ms)
* FD 50 -> 118 (+54%) (25 ms -> 4957 ms)
* FS 20 -> 10 (-8%)
* AA 1 -> 20 (+15%) (1 ms -> 2 ms)
* AD 60 -> 118 (+46%) (54 ms -> 4957 ms)
* AS 100 -> 70 (-24%)
* AR 20 -> 115 (+75%) (2 ms -> 3923 ms)
* VOLUME 100 -> 127 (level trim, last)


## Where it is heard: A0 / A1 / A2 / A3 held 6 s, window +2 .. +6 s (the strike excluded)

| variant | note | RMS | K-RMS | peak | % under 60 Hz | 60-150 | 150-400 | 400-1.2k | 1.2k+ | % above 60 Hz | % above 150 Hz | centroid |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | A0 | -23.3 | -32.7 | -18.0 | 100 | 0 | 0 | 0 | 0 | 0 | 0 | 117 |
| A | A1 | -26.0 | -29.6 | -17.8 | 79 | 21 | 0 | 0 | 0 | 21 | 0 | 172 |
| A | A2 | -30.4 | -31.7 | -17.1 | 11 | 89 | 0 | 0 | 0 | 89 | 0 | 262 |
| A | A3 | -38.4 | -39.0 | -16.5 | 2 | 40 | 58 | 0 | 0 | 98 | 58 | 512 |
| B | A0 | -18.3 | -26.2 | -7.1 | 85 | 14 | 1 | 0 | 0 | 15 | 1 | 86 |
| B | A1 | -18.3 | -23.1 | -6.7 | 77 | 12 | 10 | 0 | 0 | 23 | 10 | 142 |
| B | A2 | -18.3 | -20.3 | -6.5 | 48 | 34 | 10 | 8 | 0 | 52 | 18 | 268 |
| B | A3 | -18.2 | -18.7 | -6.9 | 0 | 62 | 20 | 17 | 2 | 100 | 38 | 526 |
| C | A0 | -18.1 | -23.4 | -7.1 | 70 | 28 | 3 | 0 | 0 | 30 | 3 | 98 |
| C | A1 | -18.1 | -21.6 | -6.9 | 63 | 11 | 26 | 0 | 0 | 37 | 27 | 166 |
| C | A2 | -18.1 | -19.7 | -5.9 | 38 | 28 | 9 | 25 | 0 | 62 | 33 | 316 |
| C | A3 | -18.1 | -18.3 | -6.1 | 0 | 50 | 17 | 31 | 2 | 100 | 50 | 609 |
| D | A0 | -17.9 | -26.3 | -6.9 | 87 | 9 | 3 | 0 | 0 | 13 | 3 | 90 |
| D | A1 | -17.9 | -22.9 | -6.9 | 79 | 12 | 8 | 0 | 0 | 21 | 8 | 139 |
| D | A2 | -17.8 | -19.9 | -6.8 | 49 | 35 | 13 | 3 | 0 | 51 | 16 | 223 |
| D | A3 | -17.8 | -18.3 | -7.1 | 0 | 64 | 20 | 16 | 0 | 100 | 36 | 356 |

## The 15 s hold on A1, per window: level dB / centroid Hz / % 150-400 / % above 400 Hz

| variant | 0-1s | 1-3s | 3-6s | 6-10s | 10-14s |
|---|---|---|---|---|---|
| A | -24.4 / 154 / 0 / 0 | -25.3 / 164 / 0 / 0 | -25.0 / 160 / 0 / 0 | -24.9 / 160 / 0 / 0 | -24.7 / 157 / 0 / 0 |
| B | -14.7 / 343 / 5 / 4 | -17.2 / 150 / 10 / 0 | -18.1 / 143 / 10 / 0 | -18.2 / 144 / 10 / 0 | -18.2 / 144 / 10 / 0 |
| C | -14.5 / 488 / 4 / 24 | -17.0 / 182 / 26 / 1 | -17.9 / 168 / 26 / 0 | -18.0 / 168 / 26 / 0 | -18.0 / 168 / 26 / 0 |
| D | -14.3 / 604 / 5 / 4 | -16.4 / 209 / 7 / 2 | -17.8 / 130 / 8 / 0 | -18.2 / 119 / 7 / 0 | -18.2 / 119 / 6 / 0 |

## The 15 s hold on A2, per window: level dB / centroid Hz / % 150-400 / % above 400 Hz

| variant | 0-1s | 1-3s | 3-6s | 6-10s | 10-14s |
|---|---|---|---|---|---|
| A | -29.0 / 244 / 0 / 0 | -29.7 / 250 / 0 / 0 | -29.7 / 249 / 0 / 0 | -29.5 / 247 / 0 / 0 | -29.6 / 247 / 0 / 0 |
| B | -14.7 / 726 / 8 / 9 | -17.2 / 293 / 9 / 9 | -18.1 / 271 / 10 / 8 | -18.2 / 271 / 10 / 8 | -18.2 / 271 / 10 / 8 |
| C | -14.5 / 1012 / 6 / 27 | -17.0 / 352 / 7 / 25 | -17.9 / 323 / 8 / 25 | -18.0 / 322 / 8 / 25 | -18.0 / 323 / 8 / 25 |
| D | -14.3 / 1023 / 8 / 8 | -16.4 / 354 / 9 / 7 | -17.8 / 208 / 14 / 2 | -18.1 / 185 / 16 / 0 | -18.1 / 182 / 16 / 0 |

## Release after the 15 s hold (ms after key-up to -20 / -40 / -60 dB; the render ends 4.5 s after the key-up, None = not reached)

| variant | A1 | A2 |
|---|---|---|
| A | 38.0 / 40.0 / 40.0 | 38.0 / 40.0 / 42.0 |
| B | 1150.0 / 2356.0 / 2958.0 | 1174.0 / 2356.0 / 2964.0 |
| C | 1160.0 / 2350.0 / 2958.0 | 1192.0 / 2374.0 / 2980.0 |
| D | 2364.0 / None / None | 2358.0 / None / None |

## Self-oscillation probe (oscillators off, noise-fed, note A2; diff 12 dB = linear, 0 = the filter sings by itself)

| variant | RESO | diff dB | verdict |
|---|---|---|---|
| A | 10 | 3.4 | near the edge |
| A | 127 | -0.0 | self-oscillates |
| B | 115 | 11.2 | linear |
| B | 127 | -0.0 | self-oscillates |
| C | 125 | 0.0 | self-oscillates |
| C | 127 | -0.0 | self-oscillates |
| D | 110 | 11.8 | linear |
| D | 127 | -0.0 | self-oscillates |

## Taps and the chord

| variant | tap A1 / A2 / A3 (150 ms gate RMS, dB re the held level) | centroid of the taps (Hz) | RMS 400 ms after each key-up (dB) | 3-key chord: cards gated | chord RMS (5-10.5 s) / peak |
|---|---|---|---|---|---|
| A | 0.7 / -1.7 / -6.3 | 155 / 242 / 432 | -210.3 / -210.3 / -210.3 | 1 | -30.3 / -17.1 |
| B | 4.2 / 4.2 / 4.4 | 611 / 1295 / 2484 | -19.6 / -19.5 / -19.6 | 1 | -18.3 / -6.5 |
| C | 4.4 / 4.3 / 4.3 | 922 / 1982 / 4114 | -19.5 / -19.4 / -19.6 | 1 | -18.2 / -5.9 |
| D | 4.3 / 4.3 / 4.5 | 916 / 1522 / 2345 | -16.1 / -16.2 / -16.4 | 1 | -18.0 / -6.8 |

Per-phrase peaks (dBFS): A: a_riff -15.6, b_stabs -15.6, c_held -15.9, v_drone_lo -17.5, v_drone_mid -16.6, w_chord_lo -17.1, y_tap -15.6; B: a_riff -6.3, b_stabs -6.2, c_held -6.5, v_drone_lo -6.4, v_drone_mid -6.4, w_chord_lo -6.5, y_tap -6.5; C: a_riff -6.0, b_stabs -5.5, c_held -5.9, v_drone_lo -6.3, v_drone_mid -5.6, w_chord_lo -5.9, y_tap -5.9; D: a_riff -6.4, b_stabs -6.5, c_held -6.8, v_drone_lo -6.5, v_drone_mid -6.6, w_chord_lo -6.8, y_tap -6.8

