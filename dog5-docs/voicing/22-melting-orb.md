# Voicing log: 22 "Melting Orb" (FACTORY[21], Batch 5A, Chapter III, the drones)

## APPROVED 6 Nov 2026 after one listening round: variant D (Vincent: "sounds incredible"). Committed as the patch (own array); the other three stay render-only on the listen branch. Card: `cards/22-melting-orb.md`.

Full tables for all four variants (level, peaks, CPU, every change before -> after, the measures below): `listen/voicing/batch-05a/22-melting-orb/README.md` and `results.json`; the WAVs are on the never-merged `listen/batch-05a-chapter3-drones` branch only.

Variants:

* **A (original)**: the nearest-base patch as it stood (BP QUACK: POLY, band-pass RESO 70, a fast filter-envelope snap, 1 ms attack). VOLUME 100, held level -26.54 dBFS RMS over +9..+14 s, K-RMS -27.1, peak -9.9 (all phrases), worst-case CPU 1770 host instr/sample.
* **B (melt)**: 6-voice UNISON of saws on OSC 2, filter and pitch sink together: ~4 s to 90 %, pitch -6.9 st (about a fifth), LP12 RESO 75. VOLUME 77, held level -18.06 dBFS RMS over +9..+14 s, K-RMS -19.4, peak -7.3 (all phrases), worst-case CPU 2488 host instr/sample.
* **C (slow-deep)**: B slower (~5.5 s to 90 %), deeper (pitch -12.2 st, about an octave), RESO 100, a slightly longer release. VOLUME 77, held level -18.03 dBFS RMS over +9..+14 s, K-RMS -19.8, peak -5.8 (all phrases), worst-case CPU 2502 host instr/sample.
* **D (dual-chord)**: B's melt in DUAL (POLY 6): a three-key chord melts together. VOLUME 97, held level -18.90 dBFS RMS over +9..+14 s, K-RMS -20.3, peak -4.1 (all phrases), worst-case CPU 2489 host instr/sample.

**Committed (D), each change before -> after against the patch as it stood:**

* O1_WAVE SAW -> OFF
* O1_LVL 110 -> 0 (-87%)
* O2_WAVE PULSE -> SAW
* O2_PW 30 -> 64 (+27%)
* O2_LVL 100 -> 110 (+8%)
* ENV_O2 64 -> 46 (centre 64: +0 -> -18, -14% of range) (+0.0 st at the env peak -> -6.9 st at the env peak)
* CUTOFF 50 -> 100 (+39%) (233 Hz -> 4186 Hz)
* RESO 70 -> 75 (+4%)
* FENV_AMT 124 -> 32 (centre 64: +60 -> -32, -72% of range)
* FTYPE BP12 -> LP12
* FA 20 -> 118 (+77%) (2 ms -> 4957 ms)
* FD 55 -> 60 (+4%) (36 ms -> 54 ms)
* FS 0 -> 127 (+100%)
* FR 60 -> 127 (+53%) (54 ms -> 10000 ms)
* AA 1 -> 60 (+46%) (1 ms -> 54 ms)
* AD 80 -> 100 (+16%) (256 ms -> 1218 ms)
* AS 70 -> 127 (+45%)
* AR 60 -> 92 (+25%) (54 ms -> 653 ms)
* MODE POLY -> DUAL
* UNI_N 4 -> 6 voices
* UNI_DET 30 -> 40 (+8%) (+-5.5 cents -> +-9.8 cents)
* VINTAGE 30 -> 40 (+8%)
* SPREAD 60 -> 110 (+39%)
* POLY_N 5 -> 6 voices
* VOLUME 100 -> 97

**What this patch cannot do in this engine:**

* **ENV>O2 routes the FILTER envelope to OSC 2's pitch only** (`obv_engine.h`: `p2 += fenv x (ENV>O2 - 64) x 97 >> 15`, Q8 semitones, i.e. (ENV>O2 - 64) x 24/63 semitones at the envelope's top; measured -675 cents for 46, -1209 for 32 against -6.86 / -12.19 st). It cannot bend OSC 1 and it cannot use the amp envelope. So the stack that melts is OSC 2 alone, with OSC 1 off; with both oscillators on, only OSC 2 would sink and the two would part.
* **An inverted envelope bends the pitch the wrong way for a collapse** if the envelope falls: a negative ENV>O2 with a decaying filter envelope starts low and RISES to the note. The melt here uses a RISING filter envelope (FA = the melt time) with negative ENV AMT and ENV>O2, so cutoff and pitch both sink while the key is down.
* **The key-up undoes the melt in the tail:** the filter envelope releases, so pitch and brightness climb back while the note fades, even at the slowest filter release (FR 127): D's pitch reads -639 cents in the first 0.4 s of the tail, -549 at 0.5 s and -469 at 1.0 s (the tail is 40 dB down at 0.93 s), the centroid 238 -> 826 -> 2469 Hz over the same three windows (B: -634 / -549 / -472 and 242 -> 724 -> 2529). Not isolated: whether it is audible at those levels (an untested perceptual question); a shorter AR makes it shorter (D's tail is 60 dB down at 1.29 s).
* UNISON is one note at a time (a chord plays its last key: B and C); D is DUAL, where three keys melt together.
* One shared LFO is unused here; no Poly-Mod; no drone latch.

Status: approved; card written; renders in `reference-renders/22-melting-orb_D_*.wav`.
