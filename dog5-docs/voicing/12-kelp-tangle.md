# Voicing log — 12 "Kelp Tangle" (FACTORY[11], Batch 4A, Chapter II, the spring / organ / wash set)

6 Nov 2026. Brief (Chapter II, The Tidal Hexes): *dense and tangled. Heavy PWM, murky low-pass, a spring tail. Vincent's notes: make the PWM stand out in the mix; stay close to the Moog Prodigy (murky, raw, dark), the Fender spring tank (the tail, springy) and, closest, a Polysix PWM pad into a spring tank; lean on the LFO; murky against PWM audible is the tension (a low cutoff hides PWM); watch tubby (150-400 Hz in the tail).* Method and kit: `README.md` here (§1 phrases, §3 loudness, §16 Batch 4A).

## RECOMMENDED: variant B (murk) — committed as the patch, awaiting Vincent's listening

**Status: round 1 rendered, not yet heard.** Variant B is committed as `PF_KELP_TANGLE` in `firmware/src/obv_patches.h` (equals variant B byte for byte: `tests/voicing/check_slot.py 12 B 4a`); the others are render-only. **Round count so far: 1 silent measured round (variants fixed by sweeps of the existing controls, not for ears) + 1 listening round pending.** No voice card and no `reference-renders/` yet (after approval). WAVs: the never-merged `listen/batch-04a-chapter2-organ-kelp-wash` branch, `listen/voicing/batch-04a/12-kelp-tangle/`; tables: `listen/voicing/batch-04a/12-kelp-tangle/README.md` and `probes.md`.

### The starting point (the patch as it stood)

* **Current values (the whole list; every parameter not named is at the table's default):** O1_WAVE 2, O1_PW 20, O2_WAVE 2, O2_PW 108, O2_FINE 76, CUTOFF 70, FENV_AMT 64, FTYPE 3, AA 70, AR 100, LFO_RATE 40, LFO_PHASE 2, LFO_PWM 40, SPREAD 100, REV_SIZE 100, REV_MIX 40.
* **Nearest starting patch:** HOLLOW PAD (`PF_HOLLOW_PAD`, shared with 10 Atlantic Swell): the same patch as the original 10, with a spring at DRAIN 40. Its LFO PWM is +-2.3 points around PW 16 % / 85 %: **the movement it has (14.2 dB in the 150-400 Hz band of a held A2 at 1.2 Hz) is the beating of its inverse narrow-pulse pair, not PWM** (with LFO PWM 0 it is still 14.2 dB; with the detune off too it is 1.0 dB: `probes.md`). It is not murky: centroid 4222 Hz, 13 % of the energy above 1.2 kHz.
* **The 1-2 axes judged most uncertain:** (1) the cutoff against the PWM and the tail (the murk): measured by the 150-400 / 400-1.2k / 1.2k+ bands of a held A2 and of a chord, and the tail's MUD; (2) the PWM depth and rate (sweep width, 1 Hz against 2.3 Hz, and whether the voices sweep together).
* **Control limits foreseen:** no Poly-Mod, so the brief's 'PWM driven by OSC B' is not possible: ONE shared TRI LFO drives the pulse widths of both oscillators (what is lost: a modulator with its own pitch / envelope, a different rate per oscillator, a sweep that follows the note); PWM through a low-pass reads as level and low-band movement, and the 150-400 Hz band's modulation saturates near 10 dB; a PWM sweep is one LFO period long (1 s here), so a 150 ms note hears only a slice; the spring is fed the murky voice, so its tail is murky too.
* **Plan:** two pulses 5.9 cents apart, both swept by the LFO's TRI on ONE side of 50 % (PW 42 = 33 %, +-15 points: 18-48 %, so no doubled rate), LFO PHASE SYNC (every detached note starts the sweep together), a 24 dB low-pass at 100 % key tracking (the filter sits at the same place in each note's harmonics: murky in every register), RESO 30 for some bite, no filter envelope (nothing moves but the PWM), a medium spring. PWM audibility is measured AFTER the filter (the band energies of a held A2, dry).

### Axes chosen, variants

| variant | what | VOLUME | level (own phrase) | (b) | peak | worst-case CPU |
|---|---|---|---|---|---|---|
| A original | the nearest-base patch as it stood (HOLLOW PAD: narrow inverse pulses through a notch, PWM +-2 points: not audible as PWM) | 100 | -19.4 | -17.6 | -4.8 | 2020 |
| B murk (recommended, committed) | murk first: LP24 CUTOFF 86 at 100 % key tracking, RESO 30, PWM +-15 points around 33 % (18-48 %), TRI 1.03 Hz, PHASE SYNC, spring DRAIN 55 | 75 | -18.0 | -17.0 | -5.3 | 2042 |
| C open | B along the cutoff axis: CUTOFF 98 (more of each note's harmonics through the filter) | 74 | -18.0 | -17.0 | -5.3 | 2042 |
| D tangle | B along the rate / depth axis: PWM +-16.8 points, TRI 2.3 Hz, PHASE SPREAD (each voice 45 degrees on) | 76 | -17.9 | -17.1 | -5.0 | 2047 |

* **Final values (variant B), each change before -> after (the original is the nearest-base patch as it stood):**

  * O1_PW 20 -> 42 (+17%)
  * O2_PW 108 -> 42 (-52%)
  * O2_FINE 76 -> 73 (centre 64: +12 -> +9, -2% of range) (+9.4 cents -> +7.0 cents)
  * CUTOFF 70 -> 86 (+13%) (740 Hz -> 1865 Hz)
  * RESO 20 -> 30 (+8%)
  * KEYTRK 64 -> 127 (+50%)
  * FTYPE NOTCH -> LP24
  * AA 70 -> 52 (-14%) (117 ms -> 29 ms)
  * AS 100 -> 127 (+21%)
  * AR 100 -> 88 (-9%) (1218 ms -> 478 ms)
  * LFO_RATE 40 -> 60 (+16%) (0.4 Hz -> 1.0 Hz)
  * LFO_PHASE SPREAD -> SYNC
  * LFO_PWM 40 -> 100 (+47%)
  * VINTAGE 30 -> 50 (+16%)
  * VOLUME 100 -> 75 (-20%)
  * REV_SIZE 100 -> 75 (-20%)
  * REV_DAMP 60 -> 30 (-24%)
  * REV_MIX 40 -> 55 (+12%)

* **Level:** VOLUME 75; **-18.0 dBFS RMS** on the tangle phrase (r: 1 + 3 + 6 note-ons, spring included, tails excluded); phrase (b) -17.0 (+1.0 dB), K-weighted (b) -17.7; peak -5.3 dBFS; crest 12.7 dB; worst-case CPU 2042 host instr/sample (idle 1164 + load 878; the original 2020).
* **Measured on the recommended variant** (full tables: `listen/voicing/batch-04a/12-kelp-tangle/README.md`, `probes.md`):
  * **PWM after the filter, held A2 (dry):** the LFO is TRI 1.03 Hz sweeping the pulse width 18-48 % (+-15.2 points around 33 %). Band-energy modulation (95th - 5th percentile over 23 ms frames, depth in dB): **10.1 in 150-400 Hz, 9.8 in 400-1.2k, 11.1 in 1.2k-3k**, and the level itself moves 5.9 dB; the strongest component sits at 0.9 Hz in 150-400 (the LFO is 1.03: the sweep does not double). **02 D's figure (about 12 dB in 150-400 Hz) is not reached: 10.1 dB, and it does not move with the controls tried:** LFO PWM 60 / 80 / 100 / 115 gives 10.3 / 9.9 / 10.1 / 10.0 dB and CUTOFF 78-104 gives 9.8-10.2 (`probes.md`); DRIVE 20-40 lifts it to 12.5-12.7 dB but takes the level swing from 5.9 to 3.4-3.7 dB and the chord's 150-400 depth from 8.9 to 6.9-6.2, so it is not used. On the held chord (A2 E3 C4) the depths are 8.9 / 7.1 / 7.8 dB and the level moves 4.4 dB.
  * **Murky, with numbers:** held A2 centroid 339 Hz (the original 4222), 72 % of its energy under 150 Hz and 0.0 % above 1.2 kHz; the chord's centroid 540 Hz, 1.2 % above 1.2 kHz. Dictionary: this is DARK (CUTOFF down) with a ratio the dictionary would call MUDDY (MUD 39 over the note-on region); the PWM is what moves inside it.
  * **The cutoff axis (B 86 against C 98):** C's A2 centroid is 531 Hz and its chord centroid 879 Hz (3.5 % above 1.2k); its PWM depth in 400-1.2k is 7.6 dB against B's 9.8, in 150-400 the same (10.1); its tail's MUD is 10 / 15 / 77 against B's 29 / 39 / 180. So a murkier cutoff buys PWM depth in the upper bands and costs a more tubby tail; the cutoff is the lever to turn by ear.
  * **Spring (DRAIN 55 = 43 %, SIZE 75, DAMP 30, PRE-DLY 20):** the spring's return re the dry chord after its note-on is -48.1 / -12.9 / -5.9 dB in 0-20 / 20-100 / 100-250 ms; after the chord's note-off it is -7.7 / -12.8 / -33.6 dB re the chord in 0-250 / 250-750 / 750-1500 ms; the tail is 20 / 40 / 60 dB down at 632 / 1102 / 1432 ms (DC out). **Tubby watch:** the tail's MUD (150-400 share over 1.2k+ share) is 29 / 39 / 180 with centroids 576 / 642 / 1507 Hz at levels of -20 / -31 / -52 dBFS: it is tubby, as the voice it is fed has nothing above 1.2 kHz (the spring only sees the filtered voice). Spring probes: DRAIN 30 / 55 / 80 and SIZE 50 / 62 / 75 / 90 in `probes.md` (SIZE 62 shortens the tail to 1244 ms at -60 dB).
  * **Short notes:** the PWM sweep is one LFO period (1 s) long, so a 150 ms note hears 1.7 dB of it in 400-1.2k (2.1 dB of level); PHASE SYNC starts each detached note at the same point of the sweep, so every short note has the same timbre. D (2.3 Hz) reads 4.7 dB there. The PWM is a held-note effect.
  * **Tangle (D):** PWM +-16.8 points (16-50 %) at 2.3 Hz with PHASE SPREAD: the held A2's level moves 7.8 dB (B 5.9), its 150-400 / 400-1.2k depths are 10.1 / 8.4 dB; the chord's 9.0 / 6.2 (B 8.9 / 7.1). The top of D's sweep is 50.0 %: it just touches 50 %.
  * **CPU:** worst case 2042 host instr/sample (idle 1164 + load 878); the original 2020. The device build was not run.

### Recommendation (vocabulary)

**B (murk):** dark, raw, murky pulse pad with a PWM you can hear sweep on held notes (1 Hz, one side of 50 %), into a springy tail. If the tail reads too tubby, C (cutoff 98) is the same sweep with a brighter tail and PWM that is as deep in the low band and shallower above; D is the busy, faster, spread version.

### Surprising / hard with existing controls

* The original's 'PWM' was never PWM: it was the beating of an inverse narrow-pulse pair (this slot shared 10's array).
* PWM depth in 150-400 Hz is a ceiling (about 10 dB here, 12 in 02 D) that no PWM depth or cutoff moved; what the cutoff trades is the upper bands' depth against the tail's MUD.
* Murky against audible is also murky against a clean tail: the spring rings the filtered voice, so a murky patch has a tubby tail (MUD 29 / 39 / 180 over 0-1500 ms; the later windows are at -31 / -52 dBFS).
* A short-note PWM is not possible: the shared LFO's period (1 s at RATE 60) is longer than the notes; LFO DELAY and the rate cannot follow the note.

