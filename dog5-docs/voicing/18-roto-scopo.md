# Voicing log: 18 "Roto-scopo" (FACTORY[17], Batch 5A, Chapter III, the drones)

## ROUND 1: rendered, not yet heard. Variant B is committed as the patch (own array); A, C, D are render-only.

Full tables for all four variants (level, peaks, CPU, every change before -> after, the measures below): `listen/voicing/batch-05a/18-roto-scopo/README.md` and `results.json`; the WAVs are on the never-merged `listen/batch-05a-chapter3-drones` branch only.

Variants:

* **A (original)**: the nearest-base patch as it stood (DRONE UNI: 8-voice UNISON of two saws, LP12 RESO 10, slow triangle LFO to the filter +-1 st, spring). VOLUME 100, held level -15.15 dBFS RMS over +5..+14 s, K-RMS -19.6, peak -2.8 (all phrases), worst-case CPU 3163 host instr/sample.
* **B (random)**: 3-voice UNISON of two squares (second an octave down), LP12 RESO 100, CUTOFF 62, smooth RANDOM LFO at 0.23 Hz to the filter +-14 st, VINTAGE 114, dry. VOLUME 73, held level -18.03 dBFS RMS over +5..+14 s, K-RMS -20.9, peak -8.7 (all phrases), worst-case CPU 1900 host instr/sample.
* **C (steps)**: B with SAMPLE & HOLD in place of the smooth random, and faster (0.62 Hz = RATE 50: the cutoff jumps to a new random value every ~1.6 s). VOLUME 72, held level -18.07 dBFS RMS over +5..+14 s, K-RMS -21.1, peak -8.8 (all phrases), worst-case CPU 1901 host instr/sample.
* **D (slow-deep)**: B slower (0.11 Hz) and deeper (+-24 st), CUTOFF 66, RESO 115 (just under self-oscillation), VINTAGE 127. VOLUME 72, held level -17.94 dBFS RMS over +5..+14 s, K-RMS -20.7, peak -8.0 (all phrases), worst-case CPU 1897 host instr/sample.

**Committed (B), each change before -> after against the patch as it stood:**

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
* VOLUME 100 -> 73

**What this patch cannot do in this engine:**

* **No Poly-Mod.** The wander is one shared LFO (smooth random or sample-and-hold) added to the cutoff: it cannot follow OSC 2, it is not tied to any oscillator's pitch or phase, and there is one LFO rate for everything the LFO touches (here the filter only; LFO PITCH is 0). The movement is common to all voices (the per-voice difference is the slop, VINTAGE, which moves pitch and the filter's own per-card offset, not a second wander).
* **UNISON is one note at a time.** A three-key chord plays its last key only (the cards gated after a 3-key chord: 3 = one group of three); a chord needs POLY or DUAL (not in this brief).
* There is no drone latch: the drone lasts as long as the key is down.

Status: not approved; no card, no `reference-renders/` until Vincent picks.
