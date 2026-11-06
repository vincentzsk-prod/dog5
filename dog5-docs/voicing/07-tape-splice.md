# Voicing log — 07 "Tape Splice" (FACTORY[6], Batch 3B, the wreck and chop set)

5 Nov 2026. Brief (Batch 3B, Chapter I): *a fat square with an X-mod pitch wobble, chopped by the gate, with tape degrade adding splice jitter. Nervous and glitching, broken, unreliable; fast release, short gates.*
Closest to: a Mono/Poly cross-mod square through a worn tape echo (Mono/Poly fat/drifting, Prophet-5 wobble/nervous, RE-201 wobble/lo-fi, SH-101 punchy). Method and kit: `README.md` here (§1 phrases, §3 loudness, §14 Batch 3B).

## APPROVED: variant B (centre) — committed as the patch

**Status: APPROVED by Vincent after listening, as rendered: variant B (centre).** Committed 5 Nov 2026 (the array `PF_TAPE_SPLICE` in `firmware/src/obv_patches.h` equals variant B byte for byte: `tests/voicing/check_slot.py 7 B 3b`; from INIT both paths are bit-identical, from the boot patch the slew floor puts them -14.7 .. -23.8 dB apart). **Final round count: 1 silent measured round + 1 listening round (approved at the first listening).**
Voice card: `cards/07-tape-splice.md`; renders: `reference-renders/07-tape-splice_B_*.wav` (splice = level phrase, stabs, riff).

* **Axes chosen:** (unchanged by the approval) X-MOD depth, the pitch LFO and the tape together against how glitchy / jittery it gets (B centre, C glitchy, D gentle); probes for X-MOD, CHEW and DROPS alone.
* **Final values (variant B), each change before -> after (the original is the nearest-base patch as it stood):**

* O1_WAVE SAW -> PULSE
* O2_WAVE SAW -> PULSE
* O2_SEMI -5 -> +0 st
* XMOD 90 -> 70 (-16%)
* O2_FINE 70 -> 68 (centre 64: +6 -> +4, -2% of range) (+4.7 cents -> +3.1 cents)
* CUTOFF 50 -> 60 (+8%) (233 Hz -> 415 Hz)
* FS 30 -> 60 (+24%)
* AR 40 -> 25 (-12%) (11 ms -> 4 ms)
* LFO_SHAPE TRI -> RANDOM
* LFO_RATE 70 -> 94 (+19%) (1.7 Hz -> 5.7 Hz)
* LFO_PITCH 0 -> 16 (+13%)
* VOLUME 100 -> 104 (+3%)
* CHEW 0 -> 80 (+63%)
* TP_HISS 64 -> 0 (-50%)
* TP_DROPS 64 -> 90 (+20%)

* **Level:** VOLUME 104; **-18.1 dBFS RMS** on the level phrase (RMS over the note-on region of the splice phrase (phrase n)); phrase (b) -17.6 (+0.5 dB), K-weighted (b) -18.0; peak -12.5 dBFS (b_stabs); crest 5.2 dB on the level phrase; worst-case CPU 2177 host instr/sample (idle 1933 + load 244; the original 1384).
* **Measured on the recommended variant** (full tables: `listen/voicing/batch-03b/07-tape-splice/README.md`): MONO: two 50 % pulses a unison apart, 3.1 cents (OSC 2 FINE 68), the fat square, into a 24 dB low-pass (CUTOFF 60, per-voice DRIVE 40); OSC 2 frequency-modulates OSC 1 (X-MOD 70: this engine's OSC B -> OSC A cross-mod; there is no separate Poly-Mod, X-MOD is the closest control; the original's was 90). THE NERVOUS WOBBLE: a smooth-random LFO on both oscillators' pitch (RATE 94 = 5.7 Hz, a new target about every 176 ms, PITCH 16 = +-19 cents peak, PHASE FREE). Measured on the held A2 the pitch track has a s.d. of 9.6 cents (28 cents 5-95 %), of which the tape adds +0.8; X-MOD does not move the measured pitch in any clear way (the X-MOD probe: pitch s.d. 9.6-14.3 cents across X-MOD 0-127, with no order to it); what it adds, measurably, is energy BELOW the note: the share of the held A2's energy under 60 Hz is 0 / 0 / 2 / 10 / 18 % at X-MOD 0 / 40 / 70 / 100 / 127 (this suggests FM sidebands; not isolated). THE CHOP: AMP ATTACK 2, DECAY 70 to SUSTAIN 100, RELEASE 25 (= 4 ms), so a 60 ms note is 40 dB down 14 ms after the key-up and 60 dB down at 18 ms. THE SPLICE: CHEW 80 (HISS 0, DROPS 90): the tape stage delays every note by +2.4 ms on average with a per-note jitter of 0.59 ms s.d. (+1.2 .. +3.2 ms over the 12 staccato notes) at the onset and +3.0 ms +-1.6 at the end of a note; dips of 6 dB or more in a 12 s hold (the CHEW probe, n · deepest dB): 0 · 6 at CHEW 0, 4 · 6 at 30, 4 · 6 at 60, 8 · 11 at 100, 15 · 20 at 127. Level -18.1 dBFS on the splice phrase, -17.6 on phrase (b), peak -12.5, crest 5.2 dB, centroid 634 Hz (the original 262); worst case 2177 host instr/sample (the original 1384). C turns X-MOD, the pitch LFO and the tape up (wobble s.d. 22 cents, 4 dips in the held note); D turns them down (wobble s.d. 8 cents).
* **Device build:** not run (no JieLi toolchain in this environment); the change is parameter arrays only. The render time on the device is not measured.
* **Other programs:** the patch bytes of the other 29 programs are equal and their audio is byte-identical on all 19 phrases (`identical.py build/voicing/base 5,7,15`, base `92cf51f`; slot 1 is not touched, so the plain comparison holds); README section 14.
