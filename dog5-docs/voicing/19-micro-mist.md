# Voicing log: 19 "Micro-mist" (FACTORY[18], Batch 5A round 2, Chapter III)

## APPROVED 6 Nov 2026 after listening: take D "tunnel" (Vincent: "sounds incredible, exactly what I was imagining"). Committed as the patch (own array `PF_MICRO_MIST`); A, B, C stay render-only on the listen branch. Card: `cards/19-micro-mist.md`. D's LFO is inert at its values (FILTER 10, PITCH 0, AMP 0) and was left exactly as rendered.

Slot 19 was Blackwater until 6 Nov 2026; Vincent dropped it completely ("I don't see myself ever using this") and the slot was rebuilt from scratch. The old log is `19-blackwater.md` (superseded). There is no original to compare with: A-D are four fresh takes.

**Brief:** neon pixels floating in the ether: a soft, glassy chord in the mid-to-upper register that scatters into a hovering, shimmering mist; after the key-up the echo and spring keep it hanging for a few seconds. Chords work (POLY).

**It is NOT a granular engine.** What this engine does instead: a slightly detuned octave-up pair (the shimmer), one shared LFO (smooth random or sample-and-hold) on pitch, filter and a little level, per-voice phase offsets (PHASE SPREAD) so the voices flicker out of step, a band-pass at a high cutoff (the glass), a high-feedback BBD echo and a large spring. **What is lost:** no grains (no slicing or re-triggering of a captured buffer), no freeze (the nearest is high feedback: a decaying hover), no reverse, no pitch-shifted repeats (the repeats are copies of the note; the BBD time has no LFO, so no chorus from the delay), and the LFO has one rate and one shape for everything.

Full tables (level, peaks, CPU, every parameter before -> after, the measures): `listen/voicing/batch-05a/19-micro-mist/README.md` and `results.json`; the WAVs (held chord with 6 s of release, tap, riff, stabs per take) are on the never-merged `listen/batch-05a-chapter3-drones` branch only.

Takes (level: RMS over +4..+10 s of the held A3 C#4 E4 chord; peak over the chord, tap, A4 single, riff and stabs):

* **A (haze)**: dense fast flicker, wide shimmer, big spring. VOLUME 97, -17.92 dBFS RMS (K-RMS -15.7), peak -4.2, 2001 host instr/sample worst case; settled centroid 3074 Hz, bands under 150 / 150-400 / 400-1.2k / over 1.2k Hz 0 / 1 / 53 / 45 %; hover -20 / -40 / -60 dB at 1212.0 / 2204.0 / 2814.0 ms; first repeat -10.2 dB re the note, 12 repeats above -40 dB, echo over spring -15.1 dB; tap -3.9 dB re the held level.
* **B (glide)**: slow drifting scatter, long echo. VOLUME 100, -19.13 dBFS RMS (K-RMS -17.4), peak -4.1, 2002 host instr/sample worst case; settled centroid 2605 Hz, bands under 150 / 150-400 / 400-1.2k / over 1.2k Hz 0 / 4 / 49 / 47 %; hover -20 / -40 / -60 dB at 1752.0 / 4256.0 / None ms; first repeat -10.7 dB re the note, 10 repeats above -40 dB, echo over spring -5.6 dB; tap -4.7 dB re the held level.
* **C (warp)**: resonant band-pass glassy top, the echo repeats the main event. VOLUME 109, -18.14 dBFS RMS (K-RMS -15.7), peak -4.0, 2004 host instr/sample worst case; settled centroid 2951 Hz, bands under 150 / 150-400 / 400-1.2k / over 1.2k Hz 0 / 3 / 26 / 71 %; hover -20 / -40 / -60 dB at 1174.0 / 2660.0 / 3752.0 ms; first repeat -8.5 dB re the note, 11 repeats above -40 dB, echo over spring -0.1 dB; tap -3.9 dB re the held level.
* **D (tunnel)**: a held pad hovering on near-100 feedback, minimal flicker. VOLUME 96, -17.95 dBFS RMS (K-RMS -16.3), peak -4.7, 2000 host instr/sample worst case; settled centroid 2300 Hz, bands under 150 / 150-400 / 400-1.2k / over 1.2k Hz 0 / 8 / 54 / 39 %; hover -20 / -40 / -60 dB at 1596.0 / 4132.0 / 5788.0 ms; first repeat -9.6 dB re the note, 14 repeats above -40 dB, echo over spring -3.9 dB; tap -8.7 dB re the held level.

**Committed (D), each parameter before -> after against INIT (the defaults); B -> D is in README section 18.2:**

* O1_LVL 110 -> 127 (+13%)
* O2_WAVE SAW -> PULSE
* O2_SEMI +0 -> +12 st
* O2_FINE 70 -> 72 (centre 64: +6 -> +8, +2% of range) (+4.7 cents -> +6.2 cents)
* CUTOFF 80 -> 70 (-8%) (1319 Hz -> 740 Hz)
* RESO 20 -> 40 (+16%)
* FENV_AMT 90 -> 74 (centre 64: +26 -> +10, -13% of range)
* FTYPE LP24 -> BP12
* FA 20 -> 75 (+43%) (2 ms -> 173 ms)
* FD 70 -> 90 (+16%) (117 ms -> 558 ms)
* FS 40 -> 90 (+39%)
* AA 10 -> 80 (+55%) (1 ms -> 256 ms)
* AD 70 -> 100 (+24%) (117 ms -> 1218 ms)
* AS 100 -> 127 (+21%)
* AR 60 -> 95 (+28%) (54 ms -> 825 ms)
* LFO_SHAPE TRI -> S&H
* LFO_RATE 70 -> 105 (+28%) (1.70 Hz -> 9.91 Hz)
* LFO_PHASE FREE -> SPREAD
* LFO_FLT 0 -> 10 (+8%) (+-0.0 -> +-0.0 st at the filter)
* VINTAGE 30 -> 40 (+8%)
* SPREAD 60 -> 100 (+31%)
* DLY_FB 50 -> 105 (+43%)
* DLY_TONE 70 -> 100 (+24%)
* DLY_MIX 0 -> 95 (+75%)
* REV_SIZE 80 -> 110 (+24%)
* REV_DAMP 60 -> 20 (-31%)
* REV_PRE 20 -> 10 (-8%)
* REV_MIX 0 -> 80 (+63%)
* POLY_N 5 -> 6 voices
* ALLEY 0 -> 100 (+79%) (SYNC -> 294 ms)
* VOLUME 100 -> 96

**Not used, and why:** CHEW (tape wobble) is off in every take: it costs about +770 host instr/sample and the takes already sit at about 2000 (target <= 2300), so C with CHEW would be about 2770. GROWL is off (inert below about 28, +595 instr/sample). A pitch LFO at 12 or more is used where it is measured to do something (A, B); C and D keep LFO PITCH 0.

**What this patch cannot do in this engine:** see the paragraph on granular above; also no Drone Latch (a held mist needs a held key; the hover after the key-up is the echo and spring tail); the LFO is one shared rate; no tempo sync; the BBD time is not modulated.

Status: approved; card written; renders in `reference-renders/19-micro-mist_D_*.wav`.
