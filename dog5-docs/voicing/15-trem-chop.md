# Voicing log — 15 "Trem Chop" (FACTORY[14], Batch 3B, the wreck and chop set)

5 Nov 2026. Brief (Batch 3B, Chapter II): *a broken-strobe tremolo. A bright saw, a hard SQUARE-shaped LFO on the amp for a choppy on/off stutter (not a gentle sine), plus a touch of slop so the chop edges waver: a broken strobe, not a tidy trem.*
Closest to: an SH-101 saw through a TR-2 on square (SH-101 bright/punchy, Boss TR-2 square choppy/gated, Pulsar choppy/rhythmic, Polysix drift). Method and kit: `README.md` here (§1 phrases, §3 loudness, §14 Batch 3B).

## APPROVED: variant D (smeared) — committed as the patch

**Status: APPROVED by Vincent after listening, as rendered: variant D (smeared).** The round-1 recommendation (and first commit) was B (MONO, LFO PHASE SYNC); D replaced it on 5 Nov 2026 (the array `PF_TREM_CHOP` equals variant D byte for byte: `tests/voicing/check_slot.py 15 D 3b`; from INIT both paths are bit-identical, from the boot patch they are -5.5 dB apart: the spread LFO runs free, its phase at program load differs; not isolated further). **Final round count: 1 silent measured round + 1 listening round.**
Voice card: `cards/15-trem-chop.md`; renders: `reference-renders/15-trem-chop_D_*.wav` (chop = level phrase, stabs, riff).

* **Axes chosen:** how much the chop edges waver. B: LFO PHASE SYNC, tidy (every note starts ON). C: PHASE FREE. **D: DUAL (POLY 6) with PHASE SPREAD, the two voices of a note an eighth of a cycle apart.** Rate and depth are in the probes of the README (RATE 87-110, AMP 127-64).
* **Final values (variant D), each change before -> after (the original is the nearest-base patch as it stood):**

* O1_WAVE PULSE -> SAW
* O1_LVL 110 -> 127 (+13%)
* O2_WAVE PULSE -> SAW
* O2_LVL 100 -> 127 (+21%)
* CUTOFF 90 -> 95 (+4%) (2349 Hz -> 3136 Hz)
* DRIVE 30 -> 60 (+24%)
* AS 100 -> 127 (+21%)
* LFO_SHAPE TRI -> SQUARE
* LFO_RATE 70 -> 101 (+24%) (1.7 Hz -> 8.1 Hz)
* LFO_DELAY 50 -> 0 (-39%) (775 ms -> 0 ms)
* LFO_PHASE FREE -> SPREAD
* LFO_PITCH 8 -> 0 (-6%)
* LFO_AMP 0 -> 127 (+100%)
* MODE MONO -> DUAL
* GLIDE 30 -> 0 (-24%)
* VINTAGE 30 -> 60 (+24%)
* VOLUME 100 -> 84 (-13%)
* DLY_MIX 30 -> 0 (-24%)
* POLY_N 5 -> 6 voices

* **Level:** VOLUME 84; **-17.9 dBFS RMS** on the level phrase (chop phrase o, off parts included); phrase (b) -15.4 (+2.5 dB: reads hot), peak -6.2 dBFS; crest 11.8 dB on the level phrase; worst-case CPU 2375 host instr/sample (idle 1163 + load 1211; the original 1402, the MONO variant B 1366).
* **Measured on the approved variant:** 8.10 Hz square chop, 44.8 dB between on and off; the held A3 spends 35 % of the time off, 31 % at one voice's level, 33 % at full; edge rise 16.3 ms (this suggests the two voices' edges, about 15 ms apart at the default rate; not isolated); edge timing s.d. 0.18 ms; on the short phrase 5 of 8 notes start on, the first edge at 42 ± 21 ms. No tempo sync with existing controls (README section 14 has the RATE table); LFO PITCH 0 (12 untested).
* **Device build:** not run (no JieLi toolchain in this environment); the change is parameter arrays only. The render time on the device is not measured.
* **Other programs:** the patch bytes of the other 29 programs are equal and their audio is byte-identical on all 19 phrases (`identical.py build/voicing/base 5,7,15`, base `92cf51f`, re-run on 5 Nov 2026 with 15 = D); README section 14. (05 changes again in round 2, see its log.)
