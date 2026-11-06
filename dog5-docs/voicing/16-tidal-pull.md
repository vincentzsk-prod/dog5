# Voicing log — 16 "Tidal Pull" (FACTORY[15], Batch 4A, Chapter II, the spring / organ / wash set)

6 Nov 2026. Brief (Chapter II, The Tidal Hexes): *a massive wet chordal wash. Five-voice poly detuned pulses, delay and spring. Threatens to drown the mix. Medium attack, not slow. Vincent's notes: wide polys, wide chorus modulation; medium pulse rates on sine waves (triangle also approved); give options; no square or saw waves; make sure the delay does not get lost; the Fender Twin guides what 'wet' feels like: bright, clear, springy, washy, not punchy; bright and clear by note definition but heavily modulated.* Method and kit: `README.md` here (§1 phrases, §3 loudness, §16 Batch 4A).

## APPROVED: variant D (triangle-like oscillator stack, TRI 2.3 Hz, DLY MIX 110)

**Status: APPROVED by Vincent after listening (6 Nov 2026): variant D (triangle-like oscillator stack, TRI 2.3 Hz, DLY MIX 110).** Committed as `PF_TIDAL_PULL` in `firmware/src/obv_patches.h` (equals variant D byte for byte: `tests/voicing/check_slot.py 16 D 4a`). **Final round count: 1 silent measured round + 1 listening round.** Voice card: `cards/16-tidal-pull.md`; renders: `reference-renders/16-tidal-pull_D_*.wav`. The round-1 text below was written when variant B was the recommendation and is kept as the record; the numbers for the approved variant are in `listen/voicing/batch-04a/16-tidal-pull/README.md`.

* **Level of the approved variant:** VOLUME 76; -19.1 dBFS RMS on its own phrase (note-on region, effects in, tails out); phrase (b) -26.8; peak -4.4 dBFS over the whole renders; worst-case CPU 2027 host instr/sample (idle 1180 + load 847).
* **Final values, each change before -> after against main (the patch as it stood before Batch 4A):**
  * O1_PW 64 -> 32 (-25%)
  * O2_PW 40 -> 32 (-6%)
  * O2_LVL 100 -> 84 (-13%)
  * O2_SEMI +0 -> +12 st
  * O2_FINE 73 -> 66 (centre 64: +9 -> +2, -6% of range) (+7.0 cents -> +1.6 cents)
  * CUTOFF 75 -> 64 (-9%) (988 Hz -> 523 Hz)
  * RESO 5 -> 0 (-4%)
  * FENV_AMT 74 -> 64 (centre 64: +10 -> +0, -8% of range)
  * KEYTRK 64 -> 127 (+50%)
  * FTYPE LP24 -> LP12
  * FA 50 -> 20 (-24%) (25 ms -> 2 ms)
  * AA 60 -> 82 (+17%) (54 ms -> 299 ms)
  * AS 100 -> 127 (+21%)
  * AR 90 -> 92 (+2%) (558 ms -> 653 ms)
  * LFO_RATE 50 -> 76 (+20%) (0.6 Hz -> 2.3 Hz)
  * LFO_PITCH 3 -> 16 (+10%)
  * LFO_PWM 60 -> 0 (-47%)
  * SPREAD 100 -> 127 (+21%)
  * VOLUME 100 -> 76 (-19%)
  * DLY_FB 50 -> 78 (+22%)
  * DLY_TONE 70 -> 100 (+24%)
  * DLY_MIX 0 -> 110 (+87%)
  * REV_SIZE 100 -> 90 (-8%)
  * REV_DAMP 60 -> 35 (-20%)
  * REV_MIX 35 -> 45 (+8%)
  * ALLEY 0 -> 104 (+82%) (SYNC -> 337 ms)

### The starting point (the patch as it stood)

* **Current values (the whole list; every parameter not named is at the table's default):** O1_WAVE 2, O2_WAVE 2, O2_PW 40, O2_FINE 73, CUTOFF 75, RESO 5, FENV_AMT 74, FA 50, AA 60, AR 90, LFO_RATE 50, LFO_PHASE 2, LFO_PITCH 3, LFO_PWM 60, VINTAGE 50, SPREAD 100, REV_SIZE 100, REV_MIX 35.
* **Nearest starting patch:** PWM STRINGS (`PF_PWM_STRINGS`, shared with 13 Ghost Board): POLY 5, O1 a 50 % pulse (a SQUARE) and O2 a 31 % pulse 7 cents sharp, a 24 dB low-pass at CUTOFF 75 (988 Hz at C4, 50 % key tracking), a 54 ms attack (measured 3 / 14 / 27 ms), a slow TRI at 0.62 Hz on PWM +-5.5 points in PHASE SPREAD, **LFO PITCH 3 (inert: the law is zero below 12)**, a spring at DRAIN 35, **no delay**. It is very hot (-11.8 dBFS RMS on the wash phrase, peak -0.2) and dark (centroid 593 Hz).
* **The 1-2 axes judged most uncertain:** (1) the oscillator: bright pulses against softened toward a triangle (the 'sine' reading); (2) the LFO shape and rate (TRI against smooth RANDOM, medium rates 1.3-2.3 Hz) with the attack (three options: 101 / 160 / 219 ms); (3) the delay against the spring.
* **Control limits foreseen:** there is no sine oscillator and no sine LFO (the TRI is the nearest); no tempo sync; a PWM sweep through 50 % doubles its rate, so no pulse here is a 50 % square; LFO PITCH below 12 is inert; the amp envelope's nominal time is not its 10-90 % time (see below); the spring is fed AFTER the echo, so it rings the repeats; POLY gives each note one voice on one pan position: the width is limited (DUAL is wider and needs 8 voices).
* **Plan:** **My reading of the note:** 'sine waves' = the LFO's nearest shape, **TRI** (and **RANDOM**, which is smooth, as the second option); 'medium pulse rates' = **medium LFO rates** (1.3-2.3 Hz here); 'no square or saw waves' = no SQUARE / RAMP / SAW / S&H LFO shapes (none is used), and on the oscillators: **pulses only, never a 50 % square or a saw** (B and C: PW 35 % / 24 %; D: 25 %). The engine has no sine oscillator, so variant D softens the oscillators toward a triangle (narrow pulses through a key-tracking low-pass, as 11 Slapback Strut does). LFO PITCH 3 -> 16 (+-19 cents, a real value); the attack is three options (101 / 160 / 219 ms to 90 %).

### Axes chosen, variants

| variant | what | VOLUME | level (own phrase) | (b) | peak | worst-case CPU |
|---|---|---|---|---|---|---|
| A original | the nearest-base patch as it stood (PWM STRINGS, shared with 13 Ghost Board: no delay, spring only, inert LFO PITCH 3) | 100 | -11.8 | -14.2 | -0.2 | 2069 |
| B tri (recommended, committed) | TRI LFO 1.26 Hz on pitch +-19 cents and the pulse widths, pulses, attack 101 ms to 90 %, the echo ahead of the spring (DLY MIX 100, DRAIN 45) | 63 | -18.1 | -21.6 | -4.4 | 2026 |
| C random | smooth RANDOM LFO ~1.7 Hz, attack 160 ms, the spring ahead of the echo (DRAIN 65, DLY MIX 90) | 65 | -18.0 | -22.2 | -4.3 | 2025 |
| D soft | the oscillators softened toward a triangle (narrow pulses through a key-tracking low-pass, an octave stack), TRI 2.3 Hz, attack 219 ms, echo up (MIX 110) | 76 | -19.1 | -26.8 | -4.4 | 2027 |

* **Final values (variant B), each change before -> after (the original is the nearest-base patch as it stood):**

  * O1_PW 64 -> 44 (-16%)
  * O2_PW 40 -> 30 (-8%)
  * CUTOFF 75 -> 100 (+20%) (988 Hz -> 4186 Hz)
  * RESO 5 -> 8 (+2%)
  * FENV_AMT 74 -> 64 (centre 64: +10 -> +0, -8% of range)
  * KEYTRK 64 -> 100 (+28%)
  * FTYPE LP24 -> LP12
  * FA 50 -> 20 (-24%) (25 ms -> 2 ms)
  * AA 60 -> 72 (+9%) (54 ms -> 137 ms)
  * AS 100 -> 127 (+21%)
  * AR 90 -> 92 (+2%) (558 ms -> 653 ms)
  * LFO_RATE 50 -> 64 (+11%) (0.6 Hz -> 1.3 Hz)
  * LFO_PITCH 3 -> 16 (+10%)
  * LFO_PWM 60 -> 80 (+16%)
  * SPREAD 100 -> 127 (+21%)
  * VOLUME 100 -> 63 (-29%)
  * DLY_FB 50 -> 78 (+22%)
  * DLY_TONE 70 -> 100 (+24%)
  * DLY_MIX 0 -> 100 (+79%)
  * REV_SIZE 100 -> 90 (-8%)
  * REV_DAMP 60 -> 35 (-20%)
  * REV_MIX 35 -> 45 (+8%)
  * ALLEY 0 -> 104 (+82%) (SYNC -> 337 ms)

* **Level:** VOLUME 63; **-18.1 dBFS RMS** on the wash phrase (s: 2 chords + 3 notes + 3 stabs, echo and spring included, tails excluded); phrase (b) -21.6 (-3.5 dB: short stabs do not reach full level through a 101 ms attack), K-weighted (b) -22.1; peak -4.4 dBFS; crest 13.7 dB; worst-case CPU 2026 host instr/sample (idle 1180 + load 847; the original 2069). D is peak-limited to -19.1 dBFS RMS (VOLUME 76; its peak is -4.4 at that level).
* **Measured on the recommended variant** (full tables: `listen/voicing/batch-04a/16-tidal-pull/README.md`, `probes.md`):
  * **Attack (amp envelope, one voice, LFO off):** 10 / 50 / 90 % of the level at **9 / 44 / 101 ms** (AA 72, the table's nominal 137 ms); C 14 / 69 / 160 ms (AA 78); D 17 / 93 / 219 ms (AA 82). **The nominal time is not the attack time: 90 % arrives at 0.73-0.78 of it and 50 % at about a third** (`probes.md`). A detuned pair read on its own beats by several dB and moved the plateau the percentages are taken against: it read 87 ms where the envelope alone reads 160 (AA 78): suggests the beating, not isolated; the probe therefore runs with OSC 2 off and VINTAGE 0.
  * **LFO:** TRI 1.26 Hz (RATE 64) on pitch +-19 cents (LFO PITCH 16) and on the pulse widths +-9.8 points, PHASE SPREAD; the one-voice probe reads 10.4 cents s.d. (32.8 cents 5-95 %) at 1.25 Hz. C: smooth RANDOM at 1.70 Hz (probe 8.1 cents s.d.; not periodic, so no rate to read); D: TRI 2.30 Hz on pitch only.
  * **Width ('wide polys'):** the held chord's L/R correlation is 0.70 dry and 0.55 with the echo and spring (the original 0.80); POLY puts each note on one voice at one pan position. **As DUAL, POLY 8 (a left / right pair per note, a four-note chord uses all eight) it measures 0.38 dry (0.41 full)**: the wider option, not made a variant because the brief is a five-voice poly and the voice count doubles (not costed here).
  * **Bright / clear / not muddy:** B's chord (dry) centroid 1733 Hz, MUD 7.8, 7.9 % above 1.2 kHz (the original 610 Hz, MUD 88); its first repeat 1030 Hz. The tail after the chord: MUD 9 / 21 / 25 at 0-250 / 250-750 / 750-1500 ms (levels -20 / -26 / -35 dBFS), centroids 1675 / 1288 / 973 Hz: the tail darkens as the BBD takes the top off each repeat; C (more spring, less echo) is brighter in the tail (MUD 2 / 8 / 11).
  * **The delay does not get lost:** ALLEY 104 = 337 ms, FEEDBK 78, MIX 100, TONE 100, PINGPONG 127. On an isolated 400 ms E4 the first repeat arrives 337 ms after the note-on, its peak (the end of the repeated note, 566 ms) is **-9.4 dB re the dry note's peak**, the spring in the same window is -16.0 dB re the note, so **the delay is 6.6 dB above the spring** (C: -10.5 dB, margin 4.2; D: -8.6, 7.7). The repeats fall +0.0 -0.6 -4.8 -10.8 -15.9 -20.9 dB re the first. The echo sits 21 / 14 / 17 dB under the figure's three notes. The spring is in series after the echo (it rings the repeats). Balance table (DLY MIX 70-127 against DRAIN 25-100) in `probes.md`: at MIX 100 the delay stays above the spring up to DRAIN 70 (+2.7 dB) and is level with it at DRAIN 100.
  * **Spring ('wet' like the Twin: bright, springy, washy):** DRAIN 45 (35 %), SIZE 90, DAMP 35. On the isolated E4 the spring's return re the note is -46.0 / -20.3 / -16.4 dB in 0-20 / 20-100 / 100-250 ms; after the chord's note-off the spring's return is -10.2 / -7.5 / -9.8 / -22.7 / -41.4 dB re the chord and the delay's -6.9 / -7.7 / -8.8 / -13.4 / -22.8 dB (0-100 / 100-250 / 250-500 / 500-1000 / 1000-2000 ms). The whole tail is 20 / 40 dB down at 1112 / 2452 ms and past 2.5 s at -60 dB (a long, washy tail).
  * **Softened oscillators (D):** the triangle probe on D's OSC 1 through the filter, harmonics 3 / 5 / 7 re the fundamental: **-17.2 / -27.3 / -36.8 dB against an ideal triangle's -19.1 / -28.0 / -34.2** (a square is -9.5 / -14.0 / -16.9); B's pulses are -26.0 / -16.1 / -16.9 (a 35 % pulse). What D is and is not: narrow pulses through a key-tracking 12 dB low-pass at 2.0 x the note (CUTOFF 64 = 523 Hz at C4, 100 % key tracking), plus an octave-up pulse the same way: **a triangle-like tone, not a sine** (no filter makes a sine out of this); it is dark (centroid 595 Hz, 0.5 % above 1.2 kHz, MUD 133: by the dictionary's ratio muddy, because a triangle has almost nothing above 1.2 kHz) and its tail MUD is 177 / 407 / 689. It trades brightness for softness: the 'bright and clear' note and the 'no square or saw' note pull against each other here.
  * **CPU:** worst case 2026 host instr/sample (idle 1180 + load 847); the original 2069. The device build was not run.

### Recommendation (vocabulary)

**B (tri):** a bright, wide-ish, heavily modulated pulse wash with a medium (101 ms to 90 %) attack, a clear echo ahead of a springy tail, TRI LFO at 1.26 Hz. C is the RANDOM-LFO, slower-attack, spring-forward reading; D is the soft, triangle-like reading with the slowest attack and the most echo. Mix and match by ear: every difference is one control (LFO SHAPE / RATE, AA, the oscillator block with CUTOFF, DLY MIX, DRAIN).

### Surprising / hard with existing controls

* The original had no delay and an inert pitch LFO: it was hot (-11.8 dBFS RMS, peak -0.2) and dark (593 Hz).
* The amp envelope's nominal time (the table) is 1.3-1.4x its 90 % time: AA 72 = 137 ms nominal = 101 ms to 90 %.
* 'Wide' is limited in POLY (width 0.70 dry): DUAL doubles the voices for 0.38.
* D is a triangle-like tone and is dark; no brighter softened oscillator exists with one low-pass for both oscillators.

