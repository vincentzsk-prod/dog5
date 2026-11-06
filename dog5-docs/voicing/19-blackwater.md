> **SUPERSEDED, patch dropped 6 Nov 2026** (Vincent rejected every variant; slot 19 is now Micro-mist, see `19-micro-mist.md`). Kept as history.

# Voicing log: 19 "Blackwater" (FACTORY[18], Batch 5A, Chapter III, the drones)

## ROUND 1: rendered, not yet heard. Variant B is committed as the patch (own array); A, C, D are render-only.

Full tables for all four variants (level, peaks, CPU, every change before -> after, the measures below): `listen/voicing/batch-05a/19-blackwater/README.md` and `results.json`; the WAVs are on the never-merged `listen/batch-05a-chapter3-drones` branch only.

Variants:

* **A (original)**: the nearest-base patch as it stood (SUB BASS: MONO, a pulse and a pulse an octave down, LP12 RESO 10, CUTOFF 35, fast envelopes). VOLUME 100, held level -24.80 dBFS RMS over +5..+14 s, K-RMS -28.3, peak -15.6 (all phrases), worst-case CPU 1361 host instr/sample.
* **B (ring)**: OSC 2 pulse (PW 40) an octave down alone, LP24 RESO 115 at 100 % key tracking, filter envelope opens it and sinks over ~2 s, amp decay ~3 s to sustain, release ~2 s. VOLUME 127, held level -18.20 dBFS RMS over +5..+14 s, K-RMS -23.1, peak -6.2 (all phrases), worst-case CPU 1430 host instr/sample.
* **C (singing)**: B with RESO 125: past the edge, the filter sings by itself. VOLUME 122, held level -18.01 dBFS RMS over +5..+14 s, K-RMS -21.6, peak -5.5 (all phrases), worst-case CPU 1432 host instr/sample.
* **D (low-floor)**: B with a lower cutoff floor (CUTOFF 58, KEY TRK 80), RESO 110, the longest filter decay / amp decay / release. VOLUME 127, held level -18.21 dBFS RMS over +5..+14 s, K-RMS -23.3, peak -6.4 (all phrases), worst-case CPU 1431 host instr/sample.

**Committed (B), each change before -> after against the patch as it stood:**

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
* VOLUME 100 -> 127

**What this patch cannot do in this engine:**

* **There is no sub oscillator.** The sub is OSC 2 an octave down (SEMI -12, the lowest the knob offers); OSC 1 is off. On A1 that is 27.5 Hz, on A0 13.75 Hz.
* **At A0 and A1 most of the energy is under 60 Hz** (B: A0 85 %, A1 77 %), which small speakers do not reproduce. The ring of the resonant filter (a tone at a multiple of the key) is what is heard there; the sub itself becomes audible from A2 (52 % above 60 Hz) and fully at A3.
* VOLUME tops out at 127: B and D sit at the top of the knob and cannot go louder on the same tone (their K-weighted level is 5 dB under the reference).
* A MONO patch: a chord plays its last key.

Status: not approved; no card, no `reference-renders/` until Vincent picks.
