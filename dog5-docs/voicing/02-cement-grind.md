# Voicing log — 02 "Cement Grind" (FACTORY[1], Batch 3A, the fat and driven set)

5 Nov 2026. Brief (Batch 3A, Chapter I): *a low-mid grinder, dual pulse with FAST PWM. The thickness and the wobble must both be CLEAR. The fast PWM is there for a reason and must be clearly audible: clear intention, not subtle shimmer. Biting filter, a moderate drive crunch. Skid-and-shred.*
Closest to: a Juno-60 PWM bass through a RAT (Juno-60 PWM/wobble/thick, Polysix fat/PWM, SH-101 PWM bass/punchy, RAT crunchy, MS-20 the biting filter). Method and kit: `README.md` here (§1 phrases, §3 loudness, §12 Batch 3A).


## APPROVED: variant D (wobble) — committed as the patch

**Status: APPROVED by Vincent after listening, "all as rendered": variant D (wobble).** Committed 5 Nov 2026 (the array `PF_CEMENT_GRIND` in `firmware/src/obv_patches.h` equals variant D byte for byte: `tests/voicing/check_slot.py 2 D 3a`).
The recommendation in this log's first draft was B; the sections below describe the round as rendered (B was the recommendation, the approved variant is in the variants table). **Final round count: 1 silent measured round + 1 listening round (approved at the first listening).**
Voice card: `cards/02-cement-grind.md`; renders: `reference-renders/02-cement-grind_D_*.wav`.

* **Axes chosen:** the PWM axis, faster (11.5 Hz, LFO RATE 108, LFO PWM 110) with the filter wobbling at the same rate (LFO FILTER 28); thickness unchanged (pair 7.8 cents).
* **Final values (variant D), each change before -> after (the original is the nearest-base patch as it stood):**

* O1_WAVE SAW -> PULSE
* O1_PW 64 -> 46 (-14%)
* O2_WAVE SAW -> PULSE
* O2_PW 64 -> 46 (-14%)
* O2_LVL 100 -> 104 (+3%)
* O2_SEMI -12 -> +0 st
* O2_FINE 70 -> 74 (centre 64: +6 -> +10, +3% of range) (+4.7 cents -> +7.8 cents)
* CUTOFF 35 -> 60 (+20%) (98 Hz -> 415 Hz)
* RESO 50 -> 62 (+9%)
* FENV_AMT 64 -> 96 (centre 64: +0 -> +32, +25% of range)
* FTYPE LP24 -> LP12
* DRIVE 50 -> 78 (+22%)
* FA 20 -> 0 (-16%) (2 ms -> 0 ms)
* FD 70 -> 58 (-9%) (117 ms -> 46 ms)
* FS 100 -> 45 (-43%)
* FR 60 -> 40 (-16%) (54 ms -> 11 ms)
* AA 2 -> 1 (-1%) (1 ms -> 1 ms)
* LFO_RATE 45 -> 108 (+50%) (0.5 Hz -> 11.5 Hz)
* LFO_PHASE FREE -> SYNC
* LFO_PWM 0 -> 110 (+87%)
* LFO_FLT 70 -> 28 (-33%)
* GLIDE 0 -> 12 (+9%)
* VOLUME 100 -> 87 (-10%)

* **Level:** VOLUME 87; **-17.9 dBFS RMS** on the level phrase (j_grind); phrase (b) -18.0 (-0.0 dB), K-weighted (b) -18.5; peak -14.6 dBFS; crest 3.2 dB on the level phrase; worst-case CPU 298 host instr/sample (idle 104 + load 194).
* **Measured on the approved variant:** the LFO runs at 11.5 Hz (measured 11.6 Hz) and moves the held A2's 150-400 Hz band 11.9 dB peak to peak, 400-1.2k 6.7 dB, 1.2k-3k 5.3 dB, 3k+ 5.4 dB, overall level 4.1 dB; on the riff's 400 ms notes 8.0 dB (150-400), 5.6 dB (400-1.2k), 2.9 dB of level. The same single LFO also wobbles the filter (LFO FILTER 28) at that rate, so the original's 0.5 Hz filter wobble is gone. Centroid 515 Hz. A PWM sweep through 50 % doubles its rate (README section 12): the sweep here runs about 18-55 % (36 % +- 18 points), so it crosses 50 % by a few points at the top of each swing and folds back there; the measured rate (11.5 Hz) matches the LFO's, so the fold is not doubling the rate.
* **Device build:** not run (no JieLi toolchain in this environment); the change is parameter arrays only.
* **Other programs:** the boot-matched check (base tree plus only the new slot 1, `make_mid.py` + `identical.py ... 2,6,8`) is in the README, section 12; slot 1 is the boot patch, see there.

## 0. Before

* **Current values (the full list over the defaults):** O2_SEMI 12, CUTOFF 35, RESO 50, FENV_AMT 64, DRIVE 50, FS 100, AA 2, AS 127, AR 20, LFO_RATE 45, LFO_FLT 70, MODE 3. Name `Cement Grind`.
* **Shared array:** none. `PF_WOBBLE_BASS` was used by this slot alone, so it is renamed `PF_CEMENT_GRIND` and rewritten in place.
* **What the nearest starting patch does:** a MONO saw plus a saw an octave below through a LP24 at 98 Hz with a **slow** 0.5 Hz filter wobble (LFO RATE 45, FILTER 70), the filter envelope amount centred (no snap), DRIVE 50, sustain full. No pulse, **no PWM at all**.
  Measured on the grind riff: **-24.5 dBFS RMS** (VOLUME 100), phrase (b) -25.8, peak -14.3, crest 10.1 dB, centroid 165 Hz, 91 % of the energy under 150 Hz. A slow low swell, not a grinder.
* **The axes I judged most uncertain:** (1) **the PWM's rate and depth** (how fast is "fast", and how far can the sweep go before it stops being a sweep) and (2) **thickness against the wobble** (the width of the pair and whether the filter should wobble with it).
* **Control limits foreseen (and found):** there is one LFO, shared: its rate is the PWM's rate, and anything else it is pointed at (filter, pitch) moves at the same rate (D uses that on purpose). The LFO PWM law is `(d*d>>7)`, so ±15 points at 100 and ±25 at 127. A sweep that crosses 50 % **doubles its rate**
  (a pulse of 36 % and one of 64 % sound alike): at LFO PWM 127 with PW 36 the measured rate was 15 Hz, not 7.7. The depth in the 150-400 band saturates near 12 dB peak to peak whatever the settings (tested at 100 / 112 / 127, PW 34-46). A MONO chord plays only its last note.

## Variant B values (the first-draft recommendation, as rendered; NOT the approved variant), each change before -> after

* O1_WAVE SAW -> PULSE
* O1_PW 64 -> 46 (-14%)
* O2_WAVE SAW -> PULSE
* O2_PW 64 -> 46 (-14%)
* O2_LVL 100 -> 104 (+3%)
* O2_SEMI -12 -> +0 st
* O2_FINE 70 -> 74 (centre 64: +6 -> +10, +3% of range) (+4.7 cents -> +7.8 cents)
* CUTOFF 35 -> 60 (+20%) (98 Hz -> 415 Hz)
* RESO 50 -> 62 (+9%)
* FENV_AMT 64 -> 96 (centre 64: +0 -> +32, +25% of range)
* FTYPE LP24 -> LP12
* DRIVE 50 -> 78 (+22%)
* FA 20 -> 0 (-16%) (2 ms -> 0 ms)
* FD 70 -> 58 (-9%) (117 ms -> 46 ms)
* FS 100 -> 45 (-43%)
* FR 60 -> 40 (-16%) (54 ms -> 11 ms)
* AA 2 -> 1 (-1%) (1 ms -> 1 ms)
* LFO_RATE 45 -> 100 (+43%) (0.5 Hz -> 7.7 Hz)
* LFO_PHASE FREE -> SYNC
* LFO_PWM 0 -> 100 (+79%)
* LFO_FLT 70 -> 0 (-55%)
* GLIDE 0 -> 12 (+9%)
* VOLUME 100 -> 86 (-11%)

Dictionary moves, in the vocabulary: *fast PWM / wobble* = LFO PWM 0 -> 100 at LFO RATE 45 -> 100 (0.5 -> 7.7 Hz), TRI, both pulses, restarting with each note (PHASE FREE -> SYNC); *thick* = two pulses 7.8 cents apart (FINE 70 -> 74), OSC 2 an octave down -> unison;
*biting filter* = LP24 -> LP12, RESO 50 -> 62 (+9 %), CUTOFF 35 -> 60 (+20 %), ENV AMT centre -> 96 (+32), filter sustain 100 -> 45 (the snap); *drive crunch* = DRIVE 50 -> 78 (+22 %); *skid* = GLIDE 0 -> 12 (+9 %).

## Level (README §3)

**-18.1 dBFS RMS over the note-on region of the grind riff (phrase j)**; phrase (b) -18.4 (difference -0.3), K-weighted -18.9. **Peak -14.8 dBFS.** VOLUME 100 -> 86. Crest 3.2 dB (saturated: DRIVE 78 before the filter; at DRIVE 0 the same patch reads 6.6 dB).

## The PWM's audibility (the brief's measure)

On the held A2 (phrase j, 7.2-9.6 s), band energies in 23 ms frames, depth = 95th - 5th percentile, rate = strongest component 0.8-20 Hz; the LFO's nominal rate for comparison:

| | A original | **B** | C | D |
|---|---|---|---|---|
| LFO nominal rate (Hz) | 0.48 (filter) | **7.7** | 4.7 | 11.5 |
| 150-400 Hz band | 44.7 dB @ 0.8 Hz | **12.1 dB @ 7.7 Hz** | 10.6 dB @ 4.6 Hz | 11.9 dB @ 11.6 Hz |
| 400-1.2k band | 29.9 dB @ 0.8 Hz | **7.6 dB @ 7.7 Hz** | 7.9 dB @ 4.6 Hz | 6.7 dB @ 11.5 Hz |
| 1.2k-3k band | 3.7 dB @ 0.8 Hz | **5.6 dB @ 0.8 Hz** | 5.5 dB @ 0.8 Hz | 5.3 dB @ 11.7 Hz |
| 3k+ band | 1.8 dB @ 10.7 Hz | **7.9 dB @ 7.7 Hz** | 7.9 dB @ 4.7 Hz | 5.4 dB @ 11.5 Hz |
| overall level | 16.5 dB @ 0.8 Hz | **4.2 dB @ 7.7 Hz** | 4.2 dB @ 4.7 Hz | 4.1 dB @ 11.5 Hz |
| on the riff (8 notes x 300 ms), 150-400 / 400-1.2k band, level (dB p-p) | 15.0 / 9.8 / 5.2 | **7.6 / 5.4 / 3.1** | 7.8 / 6.2 / 2.8 | 8.0 / 5.6 / 2.9 |

(A's row is its 0.5 Hz filter wobble, which the 0.8 Hz floor of the rate search reads as 0.8; it has no PWM.) B's rate matches the LFO's to 0.1 Hz and the sweep is ~4 dB p-p in overall level and 12 dB in the lowest band: well past the 1-2 dB where modulation is a shimmer.
There is no GROWL or effect on this patch, so the PWM numbers are of the voice itself.

## The variants (full tables in the README next to the WAVs)

| | **A** original | **B** centre | **C** slower | **D** wobble |
|---|---|---|---|---|
| VOLUME | 100 | 86 | 87 | 87 |
| level reading, dBFS | -24.5 | -18.1 | -17.9 | -17.9 |
| phrase (b) RMS, dBFS (difference to the level reading) | -25.8 (-1.3) | -18.4 (-0.3) | -17.9 (+0.0) | -18.0 (-0.0) |
| peak, dBFS | -14.3 | -14.8 | -14.4 | -14.6 |
| worst-case CPU, host instr/sample | 309 | 298 | 299 | 298 |
| centroid Hz, riff / stabs | 165 / 183 | 527 / 645 | 528 / 633 | 515 / 631 |
| band split % <60/60-150/150-400/400-1.2k/1.2k+, riff | 43/48/9/0/0 | 8/51/31/10/0 | 12/46/31/11/0 | 7/50/33/10/0 |
| beat of the pair, held A2 (Hz mean · depth dB) | 0.88 · 23 | 0.97 · 16 | 2.02 · 13 | 1.01 · 30 |
| snap: first 23 ms -> next 67 ms (Hz) | 159 -> 270 | 723 -> 465 | 712 -> 479 | 823 -> 449 |

* **A** the nearest-base patch. **B** (recommended): 7.7 Hz PWM, ±15 points, pair 7.8 cents. **C**: slower (4.7 Hz) and deeper (LFO PWM 120), narrower pulses (PW 31 %), a wider pair (FINE 80 = 12.5 cents). **D**: faster (11.5 Hz) with the filter wobbling at the same rate (LFO FILTER 28).
  The beat column mixes the pair's beating with the PWM's own level swing (both move the band's envelope); it is a thickness indicator, not a clean beat rate.

## Recommendation

**B.** The PWM is the loudest thing the LFO does at 7.7 Hz (12 dB at 150-400, 8 dB at 400-1.2k and 3k+, 4 dB of level), it is on every note from the first swing (SYNC), and the filter and drive are set to bite around it, not to hide it. C is the one to ask for if "fast" should be slower and heavier;
D if the wobble should be a filter wobble as well (the filter at 28 of 127 adds a second layer at the same rate).

## Open for the ears

* Is 7.7 Hz "fast" in the intended sense (the sweep takes 65 ms each way), or should it be a slower C-like swing? Is it obviously PWM or does it read as tremolo?
* Is the pair thick enough at 7.8 cents (0.5 Hz beat at A2), or is C's 12.5 cents what "thick" means here?
* Drive: DRIVE 78 is before the filter, so the crunch is in the density rather than a fizz on top; if it should be edgier, GROWL ~45 is the (CPU-costly) step.
