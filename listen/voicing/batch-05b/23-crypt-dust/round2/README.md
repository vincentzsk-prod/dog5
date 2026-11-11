# 23 Crypt Dust: Batch 5B round 2 (rendered, not yet heard): the noise removed, a trace of dust kept

From round 1's C (half tape) and D (tapeless): only NOISE (and, for C2 / C3, the tape HISS; D3's POLY) change. Trace = NOISE set so that the noise component (OSC 1 LEVEL 0 render) sits 25 dB under the pulse component (NOISE 0 render) of the whole chain, RMS over +4 .. +10 s of the held triad.

| var | from | VOLUME before -> after | NOISE | HISS | POLY | level | K-RMS | peak | noise vs pulse dB | (b) stabs | CPU |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C2 | C | 123 -> 127 | 43 | 0 | 2 | -18.06 | -17.16 | -5.49 | -25.1 | -24.0 | 2456 |
| C3 | C | 123 -> 127 | 0 | 0 | 2 | -18.03 | -17.13 | -5.42 | -192.3 | -23.9 | 2417 |
| D2 | D | 127 -> 127 | 43 | 64 | 2 | -19.23 | -18.25 | -4.72 | -25.0 | -25.6 | 1686 |
| D3 | D2 | 127 -> 120 | 43 | 64 | 4 | -18.89 | -17.98 | -4.01 | -24.4 | -27.4 | 2065 |

Round 1 for comparison: C and D had NOISE 127 and measured the noise **6.0 / 5.8 dB under the pulse** (C: noise-only -24.6, pulse-only -18.6 dBFS; D: -24.9 / -19.1), so removing it to -25 dB lowers the total by only about 0.5 dB (at VOLUME 127: C -17.57 -> C2 -18.06, D -18.69 -> D2 -19.23) and VOLUME could not come down.

## Parameter changes (everything else as in round 1)

* **C2** (from C): NOISE 127 -> 43 (-66% of range; the knob is a square law: 43 against 127 is -18.8 dB), TP_HISS 64 -> 0 (off; -50% of range)
* **C3** (from C): NOISE 127 -> 0 (-100%), TP_HISS 64 -> 0 (off)
* **D2** (from D): NOISE 127 -> 43 (-66%; -18.8 dB), POLY 2 as before (HISS has no effect: CHEW is 0)
* **D3** (from D2): POLY 2 -> 4 voices (+25% of the 8 voices); NOISE 43 as D2 (the noise reads -24.4 dB under the pulse with four voices)
* VOLUME: C 123 -> C2 127, C3 127; D 127 -> D2 127, D3 120 (all re-trimmed; the three at 127 have no VOLUME headroom; peaks -5.5 / -5.4 / -4.7 / -4.0)

## Which keys of A3 C#4 E4 sound, and the cost by POLY (D2, pulse only, fundamentals exposed; dB re the strongest)

| POLY | A3 | C#4 | E4 | CPU worst (idle + load) |
|---|---|---|---|---|
| 2 | -114.7 | -0.1 | 0.0 | 1686 (load 509) |
| 3 | -0.4 | -0.1 | 0.0 | 1939 (load 761) |
| 4 | -0.4 | -0.1 | 0.0 | 2065 (load 888) |
| 5 | -0.4 | -0.1 | 0.0 | 2065 (load 888) |

With POLY 2 the first key (A3) is stolen when the third arrives: C#4 and E4 sound. POLY 3, 4 and 5 sound all three (POLY 5 costs the same as 4 on the four-note stress chord).

## Tone in windows (held triad, seconds after the note-on) and release

| var | window | RMS | centroid | MUD | <150 | 150-400 | 400-1.2k | 1.2k+ |
|---|---|---|---|---|---|---|---|---|
| C2 | 0-1s | -19.3 | 1692 | 0.61 | 0 | 9 | 78 | 13.9 |
| C2 | 1-2s | -17.5 | 1508 | 1.61 | 0 | 14 | 77 | 9.0 |
| C2 | 2-4s | -17.6 | 1648 | 0.82 | 0 | 11 | 77 | 12.8 |
| C2 | 4-10s | -18.1 | 1904 | 0.38 | 0 | 8 | 70 | 21.6 |
| C2 | tail 0-0.5s | -19.7 | 1619 | 0.91 | 0 | 10 | 79 | 11.1 |
| C2 | tail 0.5-1.5s | -26.0 | 1769 | 0.42 | 0 | 7 | 77 | 16.5 |
| C2 | tail 1.5-3s | -38.4 | 2114 | 0.16 | 0 | 4 | 67 | 28.2 |
| C2 | tail 3-5s | -57.7 | 2610 | 0.10 | 5 | 3 | 56 | 35.2 |
| C3 | 0-1s | -19.4 | 1593 | 0.63 | 0 | 9 | 77 | 14.1 |
| C3 | 1-2s | -17.5 | 1408 | 1.62 | 0 | 14 | 77 | 8.7 |
| C3 | 2-4s | -17.7 | 1540 | 0.83 | 0 | 11 | 77 | 12.7 |
| C3 | 4-10s | -18.0 | 1764 | 0.38 | 0 | 8 | 70 | 21.6 |
| C3 | tail 0-0.5s | -19.7 | 1498 | 0.90 | 0 | 10 | 79 | 11.2 |
| C3 | tail 0.5-1.5s | -26.3 | 1648 | 0.44 | 0 | 7 | 76 | 16.8 |
| C3 | tail 1.5-3s | -38.5 | 1974 | 0.16 | 0 | 5 | 66 | 29.6 |
| C3 | tail 3-5s | -57.5 | 2491 | 0.11 | 4 | 4 | 59 | 33.6 |
| D2 | 0-1s | -20.1 | 2195 | 0.14 | 0 | 4 | 65 | 31.2 |
| D2 | 1-2s | -17.7 | 2338 | 0.10 | 0 | 4 | 58 | 37.8 |
| D2 | 2-4s | -18.1 | 2199 | 0.12 | 0 | 4 | 61 | 34.4 |
| D2 | 4-10s | -19.2 | 2064 | 0.21 | 0 | 6 | 67 | 27.4 |
| D2 | tail 0-0.5s | -22.0 | 1930 | 0.32 | 0 | 7 | 72 | 20.8 |
| D2 | tail 0.5-1.5s | -28.4 | 1890 | 0.30 | 0 | 7 | 71 | 22.3 |
| D2 | tail 1.5-3s | -40.4 | 1905 | 0.37 | 0 | 7 | 75 | 18.5 |
| D2 | tail 3-5s | -58.7 | 2484 | 0.34 | 2 | 7 | 71 | 20.0 |
| D3 | 0-1s | -19.1 | 2051 | 0.11 | 0 | 3 | 66 | 30.2 |
| D3 | 1-2s | -17.1 | 2206 | 0.11 | 0 | 3 | 64 | 32.4 |
| D3 | 2-4s | -17.6 | 2084 | 0.14 | 0 | 4 | 68 | 28.2 |
| D3 | 4-10s | -18.9 | 1970 | 0.22 | 0 | 6 | 69 | 25.6 |
| D3 | tail 0-0.5s | -20.9 | 1782 | 0.32 | 0 | 5 | 77 | 17.2 |
| D3 | tail 0.5-1.5s | -27.5 | 1761 | 0.28 | 0 | 5 | 75 | 19.1 |
| D3 | tail 1.5-3s | -40.2 | 1794 | 0.41 | 0 | 7 | 77 | 16.4 |
| D3 | tail 3-5s | -58.8 | 2424 | 0.27 | 3 | 7 | 64 | 26.4 |

## The pulse on the real patch, the tape, taps

Wobble = the thin pulse's strongest harmonic (1100 Hz) tracked on a held A3 of the REAL patch (noise trace, echo, spring and tape in); `CHEW 0` row = the same patch without tape (VINTAGE and the slow filter LFO move the tracked partial too: the method floor). Dips = level dips over 6 dB under the running median (10 ms RMS), 7 s of A3 / the held triad. Floor = RMS in the 1 s windows 14 s and 15 s after the chord's note-on (17-18 s, 18-19 s), notes off.

| var | pulse pitch s.d. cents (5-95 %) | rate Hz | CHEW 0 s.d. | dips A3 (count / deepest dB) | dips chord | floor 17-18 / 18-19 s | centroid 4-10 s | 1.2k+ share | 150 ms tap (dBFS, re held) | A4 tap | stabs (b) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C2 | 3.3 (-4.4 .. 5.8) | 0.54 | 1.5 | 0 / 1.0 | 0 / 2.1 | -70.8 / -84.3 | 1904 | 21.6 | -32.9 (-14.8) | -37.8 | -24.0 |
| C3 | 3.3 (-4.8 .. 6.7) | 0.54 | 1.6 | 0 / 1.1 | 0 / 1.9 | -69.2 / -84.3 | 1764 | 21.6 | -32.9 (-14.9) | -37.7 | -23.9 |
| D2 | 1.9 (-3.0 .. 3.6) | 0.39 | 1.9 | 0 / 1.5 | 0 / 2.0 | -74.0 / -87.3 | 2064 | 27.4 | -33.4 (-14.2) | -40.6 | -25.6 |
| D3 | 1.9 (-3.0 .. 3.6) | 0.39 | 1.9 | 0 / 1.5 | 0 / 2.4 | -73.7 / -87.3 | 1970 | 25.6 | -32.6 (-13.7) | -41.3 | -27.4 |

Hiss: with HISS 64 (round 1 C) the floor after the chord was -65.4 / -66.8 dBFS; with HISS 0 (C2, C3) it is -70.8 / -84.3 and -69.2 / -84.3, the same as D2 / D3 (-74.0 / -87.3, no tape) within the echo and spring tails. During the held chord HISS makes no difference to the noise-to-pulse figure (HISS 64 on C2: noise-only -43.2 either way): the hiss shows only in the quiet after the notes (it rests 2 s after silence).

Release: -20 / -40 / -60 dB after the note-off (ms): C2 1908/3608/4610; C3 1898/3582/4608; D2 1906/3604/4526; D3 1914/3608/4504

## What the patch loses when the noise goes (held triad 4-10 s, round 1 against round 2)

| var | NOISE | centroid Hz | 1.2-4 kHz % | above 4 kHz % | spectral flatness 0.4-10 kHz dB | floor after chord |
|---|---|---|---|---|---|---|
| C round 1 | 127 | 3013 | 26.9 | 2.5 | -11.0 | -65.4 / -66.8 |
| C2 | 43 | 1904 | 21.0 | 0.6 | -24.4 | -70.8 / -84.3 |
| C3 | 0 | 1764 | 21.0 | 0.6 | -30.8 | -69.2 / -84.3 |
| D round 1 | 127 | 3289 | 31.9 | 2.4 | -11.2 | -73.7 / -87.3 |
| D2 | 43 | 2064 | 26.8 | 0.7 | -25.3 | -74.0 / -87.3 |
| D3 | 43 | 1970 | 25.0 | 0.7 | -24.1 | -73.7 / -87.3 |
