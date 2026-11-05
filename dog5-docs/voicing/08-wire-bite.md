# Voicing log — 08 "Wire Bite" (FACTORY[7], Batch 3A, the fat and driven set)

5 Nov 2026. Brief (Batch 3A, Chapter I): *an anxious, thick drone that bites. The anxiety comes from a HIGHER frequency register, with a lot of ZAP from pulse: biting into a live electric wire. Emphasis on FAT but MEDIUM-TO-HIGH brightness. The DRIFTING is also key: a live wire being bitten into (unstable, wandering, nervous).
Unison/stacked detuned source; chopped on release; slop adds the spit.* Closest to: a Mono/Poly in unison with MS-20 bite (Mono/Poly fat/drifting, Minimoog thick, MS-20 the bite, Jupiter-4 fat/wobble, early Prophet-5 drift). Method and kit: `README.md` here (§1 phrases, §3 loudness, §12 Batch 3A).


## APPROVED: variant D (zap) — committed as the patch

**Status: APPROVED by Vincent after listening, "all as rendered": variant D (zap).** Committed 5 Nov 2026 (the array `PF_WIRE_BITE` in `firmware/src/obv_patches.h` equals variant D byte for byte: `tests/voicing/check_slot.py 8 D 3a`).
The recommendation in this log's first draft was B; the sections below describe the round as rendered (B was the recommendation, the approved variant is in the variants table). **Final round count: 1 silent measured round + 1 listening round (approved at the first listening).**
Voice card: `cards/08-wire-bite.md`; renders: `reference-renders/08-wire-bite_D_*.wav`.

* **Axes chosen:** the register / brightness axis (second oscillator +19 st, PW 14 %, CUTOFF 90, RESO 66, ENV AMT 124), drift unchanged from B (VINTAGE 127, pitch LFO +-19 cents).
* **Final values (variant D), each change before -> after (the original is the nearest-base patch as it stood):**

* O1_WAVE SAW -> PULSE
* O1_PW 64 -> 18 (-36%)
* O1_LVL 110 -> 108 (-2%)
* O2_WAVE SAW -> PULSE
* O2_PW 64 -> 50 (-11%)
* O2_SEMI +0 -> +19 st
* CUTOFF 85 -> 90 (+4%) (1760 Hz -> 2349 Hz)
* RESO 15 -> 66 (+40%)
* FENV_AMT 90 -> 124 (centre 64: +26 -> +60, +27% of range)
* KEYTRK 64 -> 70 (+5%)
* FTYPE LP24 -> LP12
* DRIVE 0 -> 40 (+31%)
* FA 10 -> 0 (-8%) (1 ms -> 0 ms)
* FD 70 -> 40 (-24%) (117 ms -> 11 ms)
* FS 40 -> 20 (-16%)
* FR 60 -> 30 (-24%) (54 ms -> 5 ms)
* AA 5 -> 2 (-2%) (1 ms -> 1 ms)
* AS 100 -> 127 (+21%)
* AR 50 -> 14 (-28%) (25 ms -> 1 ms)
* LFO_SHAPE TRI -> RANDOM
* LFO_RATE 70 -> 34 (-28%) (1.7 Hz -> 0.3 Hz)
* LFO_DELAY 70 -> 0 (-55%) (1519 ms -> 0 ms)
* LFO_PHASE FREE -> SPREAD
* LFO_PITCH 10 -> 16 (+5%)
* GLIDE 25 -> 0 (-20%)
* VINTAGE 30 -> 127 (+76%)
* VOLUME 100 -> 58 (-33%)
* DLY_MIX 30 -> 0 (-24%)
* REV_MIX 25 -> 0 (-20%)

* **Level:** VOLUME 58; **-17.9 dBFS RMS** on the level phrase (l_wire); phrase (b) -18.2 (-0.4 dB), K-weighted (b) -17.8; peak -8.9 dBFS; crest 9.0 dB on the level phrase; worst-case CPU 1298 host instr/sample (idle 104 + load 1194).
* **Measured on the approved variant:** zap, top above 1.2 kHz re the body: -2.0 dB on the held A4 and +0.5 dB on the first bite (centroid 4295 -> 3845 Hz first 23 ms -> next 67 ms): **the brightness (centroid 3855 Hz on the wire phrase) reduces the measured burst; B measured +4.6 dB. The brighter D was approved by ear.** Drift (engine log, held A4): static offsets -9.3 to +7.2 cents, wander 3.8-5.7 cents s.d. per voice, pitch LFO +-19 cents at 0.28 Hz; chopped: 18 ms to -40 dB after a 110 ms bite.
* **Device build:** not run (no JieLi toolchain in this environment); the change is parameter arrays only.
* **Other programs:** the boot-matched check (base tree plus only the new slot 1, `make_mid.py` + `identical.py ... 2,6,8`) is in the README, section 12; slot 1 is the boot patch, see there.

## 0. Before

* **Current values (the full list over the defaults):** O2_FINE 67, CUTOFF 85, RESO 15, FA 10, AA 5, AR 50, LFO_DELAY 70, LFO_PITCH 10, MODE 2, UNI_N 6, UNI_DET 50, GLIDE 25, SPREAD 100, DLY_TIME 4, DLY_FB 35, DLY_MIX 30, REV_MIX 25. Name `Wire Bite`.
* **Shared array:** none. `PF_UNISON_LEAD` was used by this slot alone, so it is renamed `PF_WIRE_BITE` and rewritten in place.
* **What the nearest starting patch does:** a 6-voice UNISON of two saws (DETUNE 50, SPREAD 100), a 1/4-note echo (FEEDBK 35, MIX 30) and a spring (DRAIN 25), a glide of 25, and a pitch LFO at LFO PITCH 10 that **rounds to nothing** (the LFO law is `(d*d)>>7`, which is 0 below 12): it never drifted by the LFO.
  Measured on the wire phrase: **-14.0 dBFS RMS at VOLUME 100** (hot), phrase (b) -13.5, **peak -2.2 dBFS** (the bank limit is -4), centroid 1888 Hz, 1985 instr/sample worst case (the effects). The voices wander 1.1 cents s.d. each (VINTAGE 30).
* **The axes I judged most uncertain:** (1) **the drift** (VINTAGE slop plus a pitch LFO: how much) and (2) **the register and zap** (a narrow pulse and a resonant snap against brightness and the second oscillator's octave).
* **Control limits foreseen (and found):** the audio can't show the drift in cents (a six-voice stack's own beating moves its fundamental band's centroid ~8 cents s.d. with VINTAGE 0 and no LFO): the engine's own log and the LFO law are the numbers. A unison plays one note (chords: the last note). UNISON does not re-fire the envelopes on legato, so the zap
  is a detached-note sound. The one LFO is global: its random shape at SPREAD phases puts each voice at another point of the same random line. A brighter cutoff *shrinks* the zap (the burst is measured against the body), so "zappier" and "brighter" pull apart: D shows it.

## Variant B values (the first-draft recommendation, as rendered; NOT the approved variant), each change before -> after

* O1_WAVE SAW -> PULSE
* O1_PW 64 -> 22 (-33%)
* O1_LVL 110 -> 108 (-2%)
* O2_WAVE SAW -> PULSE
* O2_PW 64 -> 50 (-11%)
* O2_SEMI +0 -> +12 st
* CUTOFF 85 -> 80 (-4%) (1760 Hz -> 1319 Hz)
* RESO 15 -> 60 (+35%)
* FENV_AMT 90 -> 120 (centre 64: +26 -> +56, +24% of range)
* KEYTRK 64 -> 70 (+5%)
* FTYPE LP24 -> LP12
* DRIVE 0 -> 40 (+31%)
* FA 10 -> 0 (-8%) (1 ms -> 0 ms)
* FD 70 -> 44 (-20%) (117 ms -> 15 ms)
* FS 40 -> 20 (-16%)
* FR 60 -> 30 (-24%) (54 ms -> 5 ms)
* AA 5 -> 2 (-2%) (1 ms -> 1 ms)
* AS 100 -> 127 (+21%)
* AR 50 -> 14 (-28%) (25 ms -> 1 ms)
* LFO_SHAPE TRI -> RANDOM
* LFO_RATE 70 -> 34 (-28%) (1.7 Hz -> 0.3 Hz)
* LFO_DELAY 70 -> 0 (-55%) (1519 ms -> 0 ms)
* LFO_PHASE FREE -> SPREAD
* LFO_PITCH 10 -> 16 (+5%)
* GLIDE 25 -> 0 (-20%)
* VINTAGE 30 -> 127 (+76%)
* VOLUME 100 -> 58 (-33%)
* DLY_MIX 30 -> 0 (-24%)
* REV_MIX 25 -> 0 (-20%)

Dictionary moves, in the vocabulary: *higher register / anxious* = OSC 2 +12 st (SEMI 24 -> 36), CUTOFF 85 -> 80 with KEY TRK 64 -> 70; *zap from pulse* = OSC 1 saw -> pulse PW 17 %, OSC 2 saw -> pulse, a resonant snap (RESO 15 -> 60 (+35 %), ENV AMT 90 -> 120 (+24 %), filter decay 46 = 15 ms, sustain 20); *fat* = the 6-voice unison, DETUNE 50 kept;
*drifting* = VINTAGE 30 -> 127 (+76 %), LFO PITCH 10 -> 16 (rounds to 0 -> ±19 cents), a smooth-random LFO shape at 0.28 Hz, PHASE SPREAD; *chopped* = AMP RELEASE 50 -> 14 (25 ms -> 1.5 ms to the 5 % point), no delay, no spring; *slop adds the spit* = the SLOBBER ride adds up to 254 on top of the patch's VINTAGE 127 (untested on this patch).

## Level (README §3)

**-18.1 dBFS RMS over the note-on region of the wire phrase (phrase l)**; phrase (b) -18.2 (difference -0.1), K-weighted -18.0. **Peak -9.3 dBFS.** VOLUME 100 -> 58 (the original sat +4.0 dB over the reference with a peak of -2.2).
Crest 8.8 dB.

## Drift (the brief's key word)

The engine's own log of the six voice cards over the held A4 (3.5 s), exact; the audio can't resolve it (above):

| | A original | **B** | C | D |
|---|---|---|---|---|
| VINTAGE | 30 | **127** | 127 | 127 |
| static offset per card (cents) | -2.4 / +0.7 / +0.3 / -1.7 / +1.6 / -0.9 | **-9.3 / +4.7 / +2.5 / -5.9 / +7.2 / -1.7** | -9.3 / +4.7 / +2.5 / -5.9 / +7.2 / -1.7 | -9.3 / +4.7 / +2.5 / -5.9 / +7.2 / -1.7 |
| wander s.d. per card (cents) | 0.9 / 1.4 / 1.1 / 1.2 / 1.2 / 0.9 | **3.9 / 5.7 / 4.5 / 4.9 / 5.1 / 3.8** | 3.9 / 5.7 / 4.5 / 4.9 / 5.1 / 3.8 | 3.9 / 5.7 / 4.5 / 4.9 / 5.1 / 3.8 |
| wander range per card (cents) | -5..+1 / -4..+5 / -3..+3 / -6..+2 / -2..+6 / -3..+2 | **-20..+4 / -13..+23 / -10..+15 / -22..+11 / -7..+26 / -10..+10** | -20..+4 / -13..+23 / -10..+15 / -22..+11 / -7..+26 / -10..+10 | -20..+4 / -13..+23 / -10..+15 / -22..+11 / -7..+26 / -10..+10 |
| pitch LFO peak (cents) · rate (Hz) | 0 (LFO PITCH 10 rounds to 0) · 1.70 | **19 · 0.28** | 38 · 0.46 | 19 · 0.28 |

The wander is a random walk with a ~0.7 s time constant, so it moves faster than the LFO's 3.6 s segments; together they are a slow lean with a nervous jitter on top. (Both are unrepeating on the device; the host's random generator makes each render one fixed draw, so these numbers are of this render.)
The stack's static spread, separate from the drift: DETUNE 50 = ±15 cents between the outer voices, plus the cards' own offsets above.

## The zap and the chop

| | A | **B** | C | D |
|---|---|---|---|---|
| held A4 start: centroid first 23 ms -> next 67 ms (Hz) | 3627 -> 2491 | **3376 -> 2390** | 3398 -> 2394 | 4295 -> 3845 |
| top (>1.2 kHz) burst re the body, held A4 (dB) | +2.0 | **+4.6** | +5.6 | -2.0 |
| first bite of the chopped phrase: centroid first 23 ms -> next (Hz) · burst (dB) | 4954 -> 2790 · +4.4 | **4909 -> 3158 · +3.2** | 4154 -> 2876 · +2.9 | 5472 -> 4414 · +0.5 |
| tail after a 110 ms bite: -20 / -40 ms (the next bite is 140 ms later) | 96 / - | **16 / 18** | 16 / 18 | 16 / 18 |
| tail after the last A3 (700 ms note): -20 / -40 / -60 dB (ms) | 188 / 1020 / - | **22 / 24 / 26** | 22 / 24 / 24 | 22 / 24 / 26 |

(`-` = not reached inside the window: the original's delay and spring.) B's chop is a hard stop: 60 dB down 26 ms after a held note. The zap of the held A4 is a 1.41x centroid fall in the first 90 ms and a +4.6 dB burst of top; the bites' burst is +3.2 dB.
It is a bite, not a laser: a bigger burst needs a lower resting cutoff, which takes the brightness away (tried in tuning: CUTOFF 66-72 gave a burst of +3.3 to +4.7 dB at a centroid of 1.2-1.9 kHz; the narrow pulse, PW 22 = 17 %, is what lifted it from +3.3 to +4.7).

## The variants (full tables in the README next to the WAVs)

| | **A** original | **B** centre | **C** drift | **D** zap |
|---|---|---|---|---|
| VOLUME | 100 | 58 | 58 | 58 |
| level reading, dBFS | -14.0 | -18.1 | -17.9 | -17.9 |
| phrase (b) RMS, dBFS (difference to the level reading) | -13.5 (+0.5) | -18.2 (-0.1) | -18.0 (-0.0) | -18.2 (-0.4) |
| peak, dBFS | -2.2 | -9.3 | -9.4 | -8.9 |
| worst-case CPU, host instr/sample | 1985 | 1296 | 1296 | 1298 |
| centroid Hz, wire / stabs | 1888 / 1207 | 2479 / 1329 | 2450 / 1313 | 3855 / 2209 |
| band split % <60/60-150/150-400/400-1.2k/1.2k+, wire | 0/0/10/75/15 | 8/0/0/67/25 | 7/0/2/66/25 | 5/0/1/24/71 |
| crest dB, wire | 11.7 | 8.8 | 8.6 | 9.0 |

* **A** the nearest-base patch. **B** (recommended): the unison of narrow pulses, VINTAGE 127, LFO PITCH 16 (±19 cents), CUTOFF 80. **C**: the drift axis, LFO PITCH 25 (±38 cents) at 0.46 Hz. **D**: the register / zap axis, second oscillator +19 st, PW 14 %, CUTOFF 90, RESO 66: brighter (centroid 3855 Hz) and the burst goes to -2.0 dB: the brightness hides the zap.

## Recommendation

**B.** It has the drift in numbers (voices wandering 4.6 cents s.d. each on offsets of -9 to +7 cents, plus a ±19 cent random lean), a +4.6 dB zap at the start, a medium-to-high centroid (2479 Hz on the high phrase), a hard chop, and 1296 instr/sample
(down from 1985: the effects are off). C if it should lean harder; D if it should be shrill.

## Open for the ears

* Is it "anxious", or too steady / too seasick? Drift is the key word: C doubles the LFO if B is too tame; the SLOBBER ride (untested here) adds up to 254 to VINTAGE live.
* Is the bite a zap, or a buzz? (The zap is a +4.6 dB burst of top: modest by the numbers.)
* Dry is my reading of "chopped on release": the original's echo and spring are off. If a little space is wanted, DRAIN is the least invasive (the tail hides the chop).
