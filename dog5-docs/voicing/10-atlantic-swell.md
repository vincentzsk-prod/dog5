# Voicing log — 10 "Atlantic Swell" (FACTORY[9], Batch 4A, Chapter II, the spring / organ / wash set)

6 Nov 2026. Brief (Chapter II, The Tidal Hexes): *a woozy combo-organ. Dual pulse, slow vibrato, heavy BBD delay. Rolls like Cape surf. Vincent's notes: Leslie / roto-sound inspiration welcome; cold, fresh, clear note definition, not a tropical wash, 'cold crispy Atlantic ocean water'; a clear chorus with the vibrato more than a vibrato-led modulation (the TC Electronic June-60 pedal's tone); one shared LFO, so a Leslie-style effect is vibrato plus tremolo at one rate; CHEW only if it demonstrably helps clarity.* Method and kit: `README.md` here (§1 phrases, §3 loudness, §16 Batch 4A).

## RECOMMENDED: variant B (june) — committed as the patch, awaiting Vincent's listening

**Status: round 1 rendered, not yet heard.** Variant B is committed as `PF_ATLANTIC_SWELL` in `firmware/src/obv_patches.h` (equals variant B byte for byte: `tests/voicing/check_slot.py 10 B 4a`); the others are render-only. **Round count so far: 1 silent measured round (variants fixed by sweeps of the existing controls, not for ears) + 1 listening round pending.** No voice card and no `reference-renders/` yet (after approval). WAVs: the never-merged `listen/batch-04a-chapter2-organ-kelp-wash` branch, `listen/voicing/batch-04a/10-atlantic-swell/`; tables: `listen/voicing/batch-04a/10-atlantic-swell/README.md` and `probes.md`.

### The starting point (the patch as it stood)

* **Current values (the whole list; every parameter not named is at the table's default):** O1_WAVE 2, O1_PW 20, O2_WAVE 2, O2_PW 108, O2_FINE 76, CUTOFF 70, FENV_AMT 64, FTYPE 3, AA 70, AR 100, LFO_RATE 40, LFO_PHASE 2, LFO_PWM 40, SPREAD 100, REV_SIZE 100, REV_MIX 40.
* **Nearest starting patch:** HOLLOW PAD (`PF_HOLLOW_PAD`, shared with 12 Kelp Tangle): POLY, two narrow pulses (PW 16 % and PW 85 %, which is an INVERTED 15 % pulse, so the pair partly cancels as it beats: that is the hollow), a notch filter, a 117 ms nominal attack (AA 70; measured 10 / 50 / 90 % at 6 / 29 / 61 ms), a 1.2 s nominal release (AR 100), a slow PWM +-2.3 points, **no pitch LFO (LFO PITCH 0), no delay (DLY MIX 0), a spring at DRAIN 40**. It is bright (centroid 5369 Hz) and has neither the vibrato, the chorus nor the BBD of the brief.
* **The 1-2 axes judged most uncertain:** (1) how deep the pitch modulation is against how clear the notes stay (chorus-led against vibrato-led); (2) how much echo: the first repeat's level, its feedback, and whether the repeats pile onto the next staccato note.
* **Control limits foreseen:** ONE LFO per patch: a Leslie's vibrato and tremolo come out IN PHASE (a rotor's loudness peak is 90 degrees from its Doppler pitch peak: not reachable); LFO PHASE SPREAD fixes 45 degrees per voice card; the BBD's time has no LFO (a short BBD is a comb / Haas widener, not a chorus); DLY TONE only shapes the feedback path (the first repeat is the BBD's own band-limit); a DUAL patch doubles the voices (CPU).
* **Plan:** chorus = **DUAL** (every note a left / right pair, SPREAD 127) + a slow **TRI pitch LFO in PHASE SPREAD** (the two voices of a note are 45 degrees apart in the LFO, so their pitch difference swings: that is the beating a chorus makes, built from the existing controls; a static detune alone, or a short BBD, does not move); a gentle pitch depth (+-19 cents at 0.72 Hz) keeps the vibrato under the chorus; organ keying (3 ms attack, full sustain, 29 ms release) and an open 12 dB low-pass keep the notes crisp; a heavy ping-pong BBD (361 ms, close to a dotted eighth at 120 BPM) with FEEDBK 95; the spring is only a touch (DRAIN 24: cold, not a wash). The Leslie-style option is variant D: the same LFO on pitch AND amp, PHASE FREE (SPREAD would cancel the tremolo in the sum: probe below). CHEW is not used.

### Axes chosen, variants

| variant | what | VOLUME | level (own phrase) | (b) | peak | worst-case CPU |
|---|---|---|---|---|---|---|
| A original | the nearest-base patch as it stood (HOLLOW PAD, shared with 12: POLY, two inverse narrow pulses through a notch, no vibrato, no delay) | 100 | -19.0 | -17.6 | -4.8 | 2020 |
| B june (recommended, committed) | clear chorus first: DUAL pair (L / R), TRI LFO 0.72 Hz on pitch +-19 cents with PHASE SPREAD, organ keying, BBD 361 ms FEEDBK 95 MIX 100, a touch of spring | 64 | -18.2 | -19.0 | -4.4 | 2294 |
| C wooze | B along the depth axis: pitch +-28 cents at 0.84 Hz (vibrato-led), and a heavier echo (387 ms, FEEDBK 104, MIX 118) | 64 | -17.9 | -18.7 | -4.9 | 2294 |
| D leslie | B with a tremolo on the same LFO (AMP 45, a 3.8 dB dip) and PHASE FREE so every voice swings together: vibrato and tremolo at one rate, 0.84 Hz (the rotary-speaker idea) | 71 | -18.0 | -19.0 | -5.1 | 2287 |

* **Final values (variant B), each change before -> after (the original is the nearest-base patch as it stood):**

  * O1_PW 20 -> 26 (+5%)
  * O2_PW 108 -> 26 (-65%)
  * O2_LVL 100 -> 84 (-13%)
  * O2_SEMI +0 -> +12 st
  * O2_FINE 76 -> 64 (centre 64: +12 -> +0, -9% of range) (+9.4 cents -> +0.0 cents)
  * CUTOFF 70 -> 104 (+27%) (740 Hz -> 5274 Hz)
  * RESO 20 -> 22 (+2%)
  * FTYPE NOTCH -> LP12
  * AA 70 -> 18 (-41%) (117 ms -> 2 ms)
  * AS 100 -> 127 (+21%)
  * AR 100 -> 52 (-38%) (1218 ms -> 29 ms)
  * LFO_RATE 40 -> 53 (+10%) (0.4 Hz -> 0.7 Hz)
  * LFO_PITCH 0 -> 16 (+13%)
  * LFO_PWM 40 -> 0 (-31%)
  * MODE POLY -> DUAL
  * SPREAD 100 -> 127 (+21%)
  * VOLUME 100 -> 64 (-28%)
  * DLY_FB 50 -> 95 (+35%)
  * DLY_TONE 70 -> 90 (+16%)
  * DLY_MIX 0 -> 100 (+79%)
  * REV_SIZE 100 -> 70 (-24%)
  * REV_DAMP 60 -> 30 (-24%)
  * REV_MIX 40 -> 24 (-13%)
  * POLY_N 5 -> 6 voices
  * ALLEY 0 -> 106 (+83%) (SYNC -> 361 ms)

* **Level:** VOLUME 64; **-18.2 dBFS RMS** on the organ phrase (q: 3 + 1 + 4 + 3 note-ons, echo and spring included, tails excluded); phrase (b) -19.0 (-0.8 dB), K-weighted (b) -19.1; peak -4.4 dBFS; crest 13.9 dB; worst-case CPU 2294 host instr/sample (idle 1180 + load 1114; the original 2020).
* **Measured on the recommended variant** (full tables: `listen/voicing/batch-04a/10-atlantic-swell/README.md`, `probes.md`):
  * **Note definition:** centroid 2154 Hz over the note-on region (the original 5369), MUD 2.3, 17 % of the energy above 1.2 kHz; the amp attack measures 10 / 50 / 90 % at 1 / 1 / 3.5 ms (the original 6 / 29 / 61).
  * **Chorus:** the LFO is TRI 0.72 Hz (RATE 53), pitch +-19 cents (LFO PITCH 16, the law); the one-voice audio probe reads a 10.9 cent s.d. and a 33.6 cent 5-95 % range at 0.72 Hz. The held A minor chord (dry): L/R correlation 0.48 (the original 0.78), the A3 band beats at 1.18 Hz (0.34-2.02) with a 29 dB envelope swing (a MONO reading: left and right are separate voices); the stereo level moves 2.4 dB. With DETUNE 0 the LFO's phase offset alone makes the beating (SPREAD 37 dB, PHASE FREE 5.8 dB, a plain DUAL pair 5.5 dB); with B's 5.5-cent DETUNE the static detune beats too (a DETUNE-only pair 39 dB, PHASE FREE 39 dB, B 29 dB): the chorus here is the pair's beat, moved by the LFO (`probes.md`). Left / right correlation differences of ~0.1 between settings are within what one render shows (oscillator start phases are random): not a trend.
  * **Delay:** ALLEY 106 = 361 ms, FEEDBK 95, MIX 100, PINGPONG 127. On an isolated 120 ms E4 the first repeat arrives 361 ms after the note-on and its peak is **-9.1 dB re the dry note's peak** (peak at 482 ms); the repeats fall about 3.2 dB each (+0.0 -3.2 -6.5 -9.8 -13.2 -16.5), the whole echo is 60 dB down 3.1 s after the note. The spring in the repeat's window is -25.2 dB re the note (the delay is 16 dB above it). The echo of the held A minor chord is -7.6 / -7.5 / -8.1 / -11.8 / -17.8 dB re the chord at 0-100 / 100-250 / 250-500 / 500-1000 / 1000-2000 ms after the note-off.
  * **Cold, clear echo:** the first repeat's centroid is 1454 Hz against the note's 2595 (the BBD's own band-limit, 2.8-8 kHz by time). **DLY TONE does not move the first repeat** (60 / 90 / 127: 1454 Hz each), only the later ones (third repeat 949 / 1082 / 1136 Hz), so the note's own spectrum is where the clarity is. The echoes of the staccato figure land 10 / 16 / 14 dB under notes 2 / 3 / 4 (the delay return re the note, 300 ms apart against a 361 ms delay).
  * **Spring:** DRAIN 24 (19 %), SIZE 70, DAMP 30: -19.6 dB re the chord in the first 100 ms after the note-off and -34.7 at 250-500 ms: a touch, as the 'cold, not tropical' note asks (the original: DRAIN 40, SIZE 100).
* **Leslie option (D):** the same TRI LFO (0.84 Hz) on pitch +-19 cents and on amp (AMP 45 = a 3.8 dB dip on one voice), PHASE FREE: the chord's tremolo measures 3.5 dB (B: 2.4). With PHASE SPREAD the 45 degree offsets cancel it (AMP 45: 2.2 dB, AMP 80: 2.8 dB); with SYNC or FREE it is a real tremolo (3.9 / 2.9 dB at AMP 45, 7.8 / 6.5 at 80). Pitch and tremolo are IN PHASE here; a rotary speaker's are not.
* **Heavy variant (C):** pitch +-28 cents at 0.84 Hz and MIX 118 / FEEDBK 104 / 387 ms: the first repeat is -7.3 dB re the note and the echo is 60 dB down later than 3.5 s (the window) after the isolated note (B 3.1 s).
* **CPU:** DUAL doubles the voices: the worst case is 2294 host instr/sample (the heaviest voiced patches are 15 D 2375, 07 B 2177); as POLY (one voice per note) it would be 1804 and the chorus is gone; one oscillator saves 48 (`probes.md`). The device build was not run; the render time on the device is not measured.

### Recommendation (vocabulary)

**B (june):** crisp, cold, clear: narrow-pulse organ with a slow, wide chorus (DUAL, TRI pitch, SPREAD) rather than a vibrato, and a heavy ping-pong echo that rolls without covering the notes. C is the same with more wooze and a heavier echo; D is the rotary-speaker reading. Turn it by ear on: pitch depth (LFO PITCH 12 = +-9 cents ... 22 = +-28), RATE, the echo (MIX, FEEDBK, ALLEY), the spring (DRAIN).

### Surprising / hard with existing controls

* The original had no vibrato, no chorus and no delay at all (LFO PITCH 0, DLY MIX 0): the brief's 'slow vibrato, heavy BBD' had to be built, not tuned.
* The chorus cannot be a modulated delay (the BBD's time has no LFO); it is two voices whose pitches wander out of step, so it can beat deeply in a mono sum (29 dB envelope swing on A3's band) while the stereo level moves 2.4 dB.
* Quadrature Leslie (tremolo 90 degrees from the vibrato) needs two LFO phases: not available. D is in phase.
* A DUAL chorus costs about +490 host instr/sample over a POLY version (2294 against 1804).

