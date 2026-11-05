# Voicing log — 15 "Trem Chop" (FACTORY[14], Batch 3B, the wreck and chop set)

5 Nov 2026. Brief (Batch 3B, Chapter I): *a broken-strobe tremolo. A bright saw, a hard SQUARE-shaped LFO on the amp for a choppy on/off stutter (not a gentle sine), plus a touch of slop so the chop edges waver: a broken strobe, not a tidy trem.*
Closest to: an SH-101 saw through a TR-2 on square (SH-101 bright/punchy, Boss TR-2 square choppy/gated, Pulsar choppy/rhythmic, Polysix drift). Method and kit: `README.md` here (§1 phrases, §3 loudness, §14 Batch 3B).

## RECOMMENDED: variant B (centre) — committed as the patch, awaiting Vincent's listening

**Status: round 1 rendered, not yet heard.** Variant B is committed as `PF_TREM_CHOP` in `firmware/src/obv_patches.h` (equals variant B byte for byte: `tests/voicing/check_slot.py 15 B 3b`); A, C, D are render-only. **Round count so far: 1 silent measured round (variants fixed by sweeps of the existing controls, not for ears) + 1 listening round pending.** No voice card and no reference-renders yet (after approval). WAVs: the never-merged `listen/batch-03b-chapter1-wreck-and-chop` branch, `listen/voicing/batch-03b/15-trem-chop/`.

* **Axes chosen:** how much the chop edges waver (B: LFO PHASE SYNC, tidy; C: PHASE FREE, the chop does not know where the note began; D: DUAL with PHASE SPREAD, the two voices of a note an eighth of a cycle apart); rate and depth are in the probes (RATE 87-110, AMP 127-64).
* **Final values (variant B), each change before -> after (the original is the nearest-base patch as it stood):**

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
* LFO_PHASE FREE -> SYNC
* LFO_PITCH 8 -> 0 (-6%)
* LFO_AMP 0 -> 127 (+100%)
* GLIDE 30 -> 0 (-24%)
* VINTAGE 30 -> 60 (+24%)
* VOLUME 100 -> 108 (+6%)
* DLY_MIX 30 -> 0 (-24%)

* **Level:** VOLUME 108; **-18.0 dBFS RMS** on the level phrase (RMS over the note-on region of the chop phrase (phrase o), off parts of the chop included); phrase (b) -16.6 (+1.4 dB), K-weighted (b) -16.8; peak -10.5 dBFS (o_chop); crest 7.5 dB on the level phrase; worst-case CPU 1366 host instr/sample (idle 1163 + load 203; the original 1402).
* **Measured on the recommended variant** (full tables: `listen/voicing/batch-03b/15-trem-chop/README.md`): MONO: two bright saws 3.9 cents apart, both oscillators at LEVEL 127, the 24 dB low-pass open (CUTOFF 95, DRIVE 60), amp SUSTAIN 127, no delay (the original's 1/8 delay at MIX 30 is removed: a choice to keep the chop dry; on a held note it changed the depth by 0.1 dB in a trial render). THE CHOP: the LFO is a SQUARE at RATE 101 = 8.10 Hz, AMP 127 (the amp law is `1 - AMP/256 x (1 - lfo)`: full level for the high half, 1/128 = -42 dB for the low half, never exactly silent). Measured on the held A3: rate 8.10 Hz, on -15.4 / off -58.1 dBFS, depth 42.8 dB, on 52 % of the cycle; the edge rises 10-90 % in 0.77 ms on an A6 probe (the reading is limited by its one-period window, 0.57 ms; the engine's own amp ramp across a 16-sample block is 0.36 ms): a hard gate, not a tremolo. LFO PITCH was 8, inert (the law is (d*d)>>7 = 0 below 12); it is now 0 (the first real value, 12, would put a square +-9 cent pitch step on every edge; untested). LFO PHASE SYNC: every detached note starts the chop ON (phrase p: 8 of 8 notes start ON, the first edge at 59 ms +-2.2 after the note-on); a legato note in MONO slides without restarting it. **The wavering:** the edge timing is tidy: s.d. of the rising edges about a straight line 0.16 ms (the reading's resolution is 0.5 ms), the period s.d. 0.25 ms, and VINTAGE does not move it (0 / 60 / 127: 0.18 / 0.24 / 0.16 ms in the VINTAGE probe): VINTAGE 60 wanders the pitch and cutoff, not the LFO. What does waver the edges is in the other variants: C lets the chop free-run (0 of 8 notes start ON at this rate and phase, the first edge slides 46 -> 24 ms over the phrase), D puts the two voices of each note an eighth of a cycle apart (rise 16.3 ms; the held note spends 35 % of the time off, 31 % at one voice's level, 33 % at full, B: 49 / 1 / 50 %). Level -18.0 dBFS on the chop phrase (off parts included), -16.6 on phrase (b), peak -10.5, crest 7.5 dB, centroid 1958 Hz; worst case 1366 host instr/sample (the original 1402).
* **Device build:** not run (no JieLi toolchain in this environment); the change is parameter arrays only. The render time on the device is not measured.
* **Other programs:** the patch bytes of the other 29 programs are equal and their audio is byte-identical on all 19 phrases (`identical.py build/voicing/base 5,7,15`, base `92cf51f`; slot 1 is not touched, so the plain comparison holds); README section 14.
