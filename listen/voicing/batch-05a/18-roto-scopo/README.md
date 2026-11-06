# Batch 5A, 18 Roto-scopo: variants A-D (round 1, rendered, not yet heard)

**Level reading:** RMS dBFS (both channels, one power average) over **+5 s .. +14 s after the note-on of the 15 s hold on the phrase `v_drone_lo`** (the held, settled state; the note-on is at 3 s), target -18.0 +-1.5, VOLUME trimmed last; peak = the largest sample of any audition phrase (riff, stabs, held, drone, chord, taps), limit -4. `first 1 s` = RMS over the first second of the same hold. K-RMS = the same window K-weighted (informational). Worst-case CPU = idle + stress-chord load, host instructions per sample (a relative yardstick; 2900 us aim / 5800 us limit are device numbers).

## Variants at a glance

| variant | name | VOLUME | held level (RMS) | K-RMS | first 1 s | (b) stabs | peak (all phrases) | clipped | chord voices gated | worst-case CPU (host instr/sample) |
|---|---|---|---|---|---|---|---|---|---|---|
| A | original | 100 | -15.15 | -19.62 | -15.4 | -22.6 | -2.8 | 0 | 8 | 3163 |
| B | random | 73 | -18.03 | -20.91 | -18.7 | -23.4 | -8.7 | 0 | 3 | 1900 |
| C | steps | 72 | -18.07 | -21.14 | -18.9 | -23.6 | -8.8 | 0 | 3 | 1901 |
| D | slow-deep | 72 | -17.94 | -20.66 | -18.7 | -23.3 | -8.0 | 0 | 3 | 1897 |
| A* | original, level-matched | 84 | -18.05 | - | - | - | -5.5 | - | - | - |

A* is the original's tone with VOLUME alone moved as near the reference as the knob allows (a listening aid, not a candidate).

## Every change, before -> after (against A, the original)

**B (random): 3-voice UNISON of two squares (second an octave down), LP12 RESO 100, CUTOFF 62, smooth RANDOM LFO at 0.23 Hz to the filter +-14 st, VINTAGE 114, dry**

* O1_WAVE SAW -> PULSE
* O2_WAVE SAW -> PULSE
* O2_LVL 100 -> 85 (-12%)
* CUTOFF 45 -> 62 (+13%) (175 Hz -> 466 Hz)
* RESO 10 -> 100 (+71%)
* FENV_AMT 79 -> 64 (centre 64: +15 -> +0, -12% of range)
* FTYPE LP24 -> LP12
* LFO_SHAPE TRI -> RANDOM
* LFO_RATE 25 -> 30 (+4%) (0.18 Hz -> 0.23 Hz)
* LFO_FLT 20 -> 70 (+39%) (+-1.1 -> +-14.4 st at the filter)
* UNI_N 8 -> 3 voices
* UNI_DET 80 -> 14 (-52%) (+-39.1 cents -> +-1.2 cents)
* VINTAGE 80 -> 114 (+27%)
* REV_MIX 50 -> 0 (-39%)
* VOLUME 100 -> 73 (level trim, last)

**C (steps): B with SAMPLE & HOLD in place of the smooth random, and faster (0.62 Hz = RATE 50: the cutoff jumps to a new random value every ~1.6 s)**

* O1_WAVE SAW -> PULSE
* O2_WAVE SAW -> PULSE
* O2_LVL 100 -> 85 (-12%)
* CUTOFF 45 -> 62 (+13%) (175 Hz -> 466 Hz)
* RESO 10 -> 100 (+71%)
* FENV_AMT 79 -> 64 (centre 64: +15 -> +0, -12% of range)
* FTYPE LP24 -> LP12
* LFO_SHAPE TRI -> S&H
* LFO_RATE 25 -> 50 (+20%) (0.18 Hz -> 0.62 Hz)
* LFO_FLT 20 -> 70 (+39%) (+-1.1 -> +-14.4 st at the filter)
* UNI_N 8 -> 3 voices
* UNI_DET 80 -> 14 (-52%) (+-39.1 cents -> +-1.2 cents)
* VINTAGE 80 -> 114 (+27%)
* REV_MIX 50 -> 0 (-39%)
* VOLUME 100 -> 72 (level trim, last)

**D (slow-deep): B slower (0.11 Hz) and deeper (+-24 st), CUTOFF 66, RESO 115 (just under self-oscillation), VINTAGE 127**

* O1_WAVE SAW -> PULSE
* O2_WAVE SAW -> PULSE
* O2_LVL 100 -> 85 (-12%)
* CUTOFF 45 -> 66 (+17%) (175 Hz -> 587 Hz)
* RESO 10 -> 115 (+83%)
* FENV_AMT 79 -> 64 (centre 64: +15 -> +0, -12% of range)
* FTYPE LP24 -> LP12
* LFO_SHAPE TRI -> RANDOM
* LFO_RATE 25 -> 15 (-8%) (0.18 Hz -> 0.11 Hz)
* LFO_FLT 20 -> 90 (+55%) (+-1.1 -> +-23.9 st at the filter)
* UNI_N 8 -> 3 voices
* UNI_DET 80 -> 14 (-52%) (+-39.1 cents -> +-1.2 cents)
* VINTAGE 80 -> 127 (+37%)
* REV_MIX 50 -> 0 (-39%)
* VOLUME 100 -> 72 (level trim, last)


## The wander (spectral centroid in 0.5 s windows, +2 s .. +14.5 s of the 15 s hold, 25 windows)

| variant | A1 centroid min..max (Hz) | range | s.d. | range in semitones | A2 min..max | range | s.d. | range in st | level s.d. A1 / A2 (dB) |
|---|---|---|---|---|---|---|---|---|---|
| A | 81..127 | 46 | 12 | 7.8 | 124..178 | 54 | 11 | 6.3 | 1.5 / 1.2 |
| B | 203..344 | 141 | 33 | 9.1 | 347..508 | 162 | 43 | 6.6 | 1.1 / 1.1 |
| C | 107..331 | 224 | 70 | 19.5 | 164..536 | 372 | 118 | 20.5 | 1.2 / 1.2 |
| D | 316..708 | 392 | 100 | 14.0 | 479..1003 | 524 | 152 | 12.8 | 0.8 / 1.0 |

## Slop, from the engine's own per-card log (A1 held 13 s): static offset / s.d. / range, cents

| variant | cards | per card |
|---|---|---|
| A | 8 | c0: -5.0 / 3.7 / -15..+11; c1: +2.6 / 3.5 / -9..+19; c2: +1.1 / 4.2 / -18..+12; c3: -4.5 / 3.2 / -17..+7; c4: +4.7 / 3.0 / -6..+16; c5: -1.0 / 4.2 / -10..+18; c6: +0.1 / 3.2 / -13..+12; c7: -4.5 / 3.0 / -15..+7 |
| B | 3 | c0: -6.9 / 5.2 / -21..+16; c1: +3.9 / 5.0 / -12..+27; c2: +1.7 / 5.9 / -25..+17 |
| C | 3 | c0: -6.9 / 5.2 / -21..+16; c1: +3.9 / 5.0 / -12..+27; c2: +1.7 / 5.9 / -25..+17 |
| D | 3 | c0: -7.6 / 5.8 / -23..+18; c1: +4.3 / 5.6 / -14..+30; c2: +1.7 / 6.6 / -28..+19 |

## Tone in windows (A1 hold): level dB / centroid Hz / MUD (150-400 share over 1.2k+ share; a 1.2k+ share near 0 makes the ratio a floor artefact) / band shares % (<60 / 60-150 / 150-400 / 400-1.2k / 1.2k+)

| variant | window | level | centroid | MUD | bands |
|---|---|---|---|---|---|
| A | 0-1s | -15.4 | 123 | 6753 | 69 / 24 / 7 / 0 / 0 |
| A | 2-5s | -14.3 | 94 | 1057 | 79 / 20 / 1 / 0 / 0 |
| A | 5-10s | -15.6 | 100 | 1448 | 76 / 23 / 1 / 0 / 0 |
| A | 10-14s | -14.6 | 93 | 1022 | 81 / 18 / 1 / 0 / 0 |
| B | 0-1s | -18.7 | 282 | 585 | 65 / 24 / 8 / 3 / 0 |
| B | 2-5s | -17.3 | 261 | 727 | 67 / 21 / 9 / 3 / 0 |
| B | 5-10s | -18.4 | 265 | 1415 | 60 / 19 / 19 / 2 / 0 |
| B | 10-14s | -17.7 | 278 | 886 | 66 / 18 / 13 / 4 / 0 |
| C | 0-1s | -18.9 | 231 | 1420 | 65 / 24 / 10 / 1 / 0 |
| C | 2-5s | -17.5 | 252 | 836 | 67 / 21 / 10 / 2 / 0 |
| C | 5-10s | -18.4 | 225 | 1380 | 63 / 22 / 14 / 2 / 0 |
| C | 10-14s | -17.7 | 155 | 10776 | 67 / 20 / 13 / 0 / 0 |
| D | 0-1s | -18.7 | 528 | 16 | 64 / 23 / 7 / 6 / 0 |
| D | 2-5s | -17.5 | 564 | 4 | 65 / 19 / 8 / 6 / 2 |
| D | 5-10s | -18.1 | 527 | 14 | 60 / 18 / 11 / 10 / 1 |
| D | 10-14s | -17.7 | 400 | 225 | 64 / 15 / 11 / 10 / 0 |

## Self-oscillation probe (oscillators off, noise-fed, note A2; diff 12 dB = linear, 0 = the filter sings by itself)

| variant | RESO | diff dB | verdict |
|---|---|---|---|
| A | 10 | 1.1 | self-oscillates |
| A | 127 | -0.0 | self-oscillates |
| B | 100 | 8.3 | near the edge |
| B | 127 | 0.0 | self-oscillates |
| C | 100 | 8.3 | near the edge |
| C | 127 | 0.0 | self-oscillates |
| D | 115 | 11.3 | linear |
| D | 127 | 0.0 | self-oscillates |

## Taps and the chord

| variant | tap A1 / A2 / A3 (150 ms gate RMS, dB re the held level) | centroid of the taps (Hz) | RMS 400 ms after each key-up (dB) | 3-key chord: cards gated | chord RMS (5-10.5 s) / peak |
|---|---|---|---|---|---|
| A | -16.3 / -16.1 / -17.6 | 262 / 276 / 384 | -30.3 / -33.4 / -33.7 | 8 | -16.1 / -5.0 |
| B | -15.9 / -13.3 / -15.8 | 438 / 441 / 671 | -32.4 / -31.7 / -31.5 | 3 | -18.5 / -8.9 |
| C | -16.1 / -13.5 / -16.0 | 456 / 476 / 658 | -32.7 / -32.0 / -31.8 | 3 | -18.7 / -9.1 |
| D | -16.1 / -13.1 / -17.9 | 684 / 830 / 1644 | -32.4 / -32.4 / -31.4 | 3 | -17.9 / -8.4 |

Per-phrase peaks (dBFS): A: a_riff -7.8, b_stabs -8.9, c_held -5.0, v_drone_lo -2.8, v_drone_mid -4.6, w_chord_lo -5.0, y_tap -19.6; B: a_riff -10.6, b_stabs -12.4, c_held -8.9, v_drone_lo -9.4, v_drone_mid -8.7, w_chord_lo -8.9, y_tap -20.7; C: a_riff -10.9, b_stabs -12.4, c_held -9.1, v_drone_lo -9.1, v_drone_mid -8.8, w_chord_lo -9.1, y_tap -21.0; D: a_riff -10.6, b_stabs -11.6, c_held -8.4, v_drone_lo -8.8, v_drone_mid -8.0, w_chord_lo -8.4, y_tap -20.1

