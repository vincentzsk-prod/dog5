# Voicing log — 06 "zzuFuzz" (FACTORY[5], Batch 3A, the fat and driven set)

5 Nov 2026. Brief (Batch 3A, Chapter I): *voltage-starved fuzz: THE PLAYER'S FUZZ WEAPON AND GO-TO FUZZ PRESET. HUGE: a fuzzy, thick WALL. Benchmark: Death by Audio Fuzz War. Snappy and punchy, but with a slight tail through the decay and a LOT of sustain. Cutoff quite open, resonance quite open as well
(watch for self-oscillation, say what you chose). NO slapback, delay or reverb: dry, NOT springy or boingy (ALLEY, DRAIN, CHEW all 0). Instant bloom: a very slight attack, MINIMAL but NOT zero (report it in ms). The fat dual-oscillator source fed hard into Drive.* Closest to: a Mono/Poly into a Big Muff
(Big Muff fuzzy/thick wall, Fuzz Face fuzzy/spitting, Univox Super-Fuzz voltage-starved/spitting, Fuzz War the benchmark, Mono/Poly the source fat/drifting, Concertmate MG-1 voltage-starved/lo-fi). Method and kit: `README.md` here (§1 phrases, §3 loudness, §12 Batch 3A).


## APPROVED: variant C (fiercer) — committed as the patch

**Status: APPROVED by Vincent after listening, "all as rendered": variant C (fiercer).** Committed 5 Nov 2026 (the array `PF_ZZUFUZZ` in `firmware/src/obv_patches.h` equals variant C byte for byte: `tests/voicing/check_slot.py 6 C 3a`).
The recommendation in this log's first draft was B; the sections below describe the round as rendered (B was the recommendation, the approved variant is in the variants table). **Final round count: 1 silent measured round + 1 listening round (approved at the first listening).**
Voice card: `cards/06-zzufuzz.md`; renders: `reference-renders/06-zzufuzz_C_*.wav`.

* **Axes chosen:** the fuzz-intensity axis, fiercer (GROWL 104, BIAS 72, TONE 64) on the POLY two-saw source; the wall-size axis (DUAL) was not taken.
* **Final values (variant C), each change before -> after (the original is the nearest-base patch as it stood):**

* O1_LVL 110 -> 118 (+6%)
* O2_WAVE PULSE -> SAW
* O2_LVL 100 -> 118 (+14%)
* O2_SEMI -12 -> +0 st
* O2_FINE 70 -> 76 (centre 64: +6 -> +12, +5% of range) (+4.7 cents -> +9.4 cents)
* CUTOFF 40 -> 88 (+38%) (131 Hz -> 2093 Hz)
* RESO 30 -> 80 (+39%)
* FENV_AMT 109 -> 120 (centre 64: +45 -> +56, +9% of range)
* DRIVE 40 -> 100 (+47%)
* FA 20 -> 2 (-14%) (2 ms -> 1 ms)
* FD 60 -> 58 (-2%) (54 ms -> 46 ms)
* FS 10 -> 40 (+24%)
* FR 60 -> 40 (-16%) (54 ms -> 11 ms)
* AA 2 -> 20 (+14%) (1 ms -> 2 ms)
* AD 70 -> 75 (+4%) (117 ms -> 173 ms)
* AS 100 -> 127 (+21%)
* AR 30 -> 70 (+31%) (5 ms -> 117 ms)
* MODE MONO -> POLY
* GLIDE 10 -> 0 (-8%)
* VINTAGE 30 -> 60 (+24%)
* SPREAD 60 -> 70 (+8%)
* VOLUME 100 -> 77 (-18%)
* GRL_BIAS 40 -> 72 (+25%)
* GRL_TONE 50 -> 64 (+11%)
* GROWL 0 -> 104 (+82%)
* POLY_N 5 -> 6 voices

* **Level:** VOLUME 77; **-18.1 dBFS RMS** on the level phrase (k_wall); phrase (b) -16.1 (+2.0 dB), K-weighted (b) -16.4; peak -12.8 dBFS; crest 5.2 dB on the level phrase; worst-case CPU 1414 host instr/sample (idle 683 + load 731).
* **Measured on the approved variant:** held A2 crest 1.7 dB (power chord 3.2); the 3 s hold loses 0.0 dB; voice-alone attack 10-90 % 2.0 ms (AMP ATTACK 20 = 2.4 ms), as rendered 1.0 ms, level -0.3 dB at 2 ms re plateau (from silence, at VOLUME 77); tail -60 dB at 278 ms after the 3 s note, 314 ms after the held chord; self-oscillation probe linear (12.0 dB) to RESO 115, 11.8 at 120, singing from 124 (3.3); centroid 2058 Hz. **Phrase (b) reads -16.1, about 2 dB hot against the level phrase** (matched on the wall phrase; a compressed signal, the chords hit the clip harder). GROWL 104 costs about +595 instr/sample whenever on; VOLUME changes how a note from silence starts (GROWL's loudness trim reads the output stage).
* **Device build:** not run (no JieLi toolchain in this environment); the change is parameter arrays only.
* **Other programs:** the boot-matched check (base tree plus only the new slot 1, `make_mid.py` + `identical.py ... 2,6,8`) is in the README, section 12; slot 1 is the boot patch, see there.

## 0. Before

* **Current values (the full list over the defaults):** O2_WAVE 2, O2_PW 50, O2_SEMI 12, CUTOFF 40, RESO 30, FENV_AMT 109, DRIVE 40, FD 60, FS 10, AA 2, AR 30, MODE 3, GLIDE 10. Name `zzuFuzz`.
* **Shared array:** `PF_FAT_BASS`, shared with **01 Red Pill and 27 R3V3RT**. 06 now has its own `PF_ZZUFUZZ` (01 got `PF_RED_PILL`; 27 keeps `PF_FAT_BASS`).
* **What the nearest starting patch does:** a MONO bass (saw + pulse an octave below, 131 Hz base cutoff, filter decay to sustain 10, DRIVE 40, GROWL 0): a dark pluck-bass, nothing like a fuzz. Measured on the wall phrase: -21.5 dBFS RMS, crest 7.6 dB, centroid 146 Hz,
  the held note's crest 5.0 dB; it plays one note at a time (a power chord plays a single note).
* **How "HUGE fuzzy wall + a lot of sustain + snappy + very short but non-zero attack + open filter and resonance" is built from GROWL, BIAS, TONE and filter DRIVE (the plan, and what the numbers said):**
  * **The wall = the source pushed hard into two clips in series.** Two full-level saws per voice, detuned 9 cents, in POLY so that a power chord (three notes, six oscillators) is a stack of twelve partial-rich saw cycles; per-voice DRIVE 100 (before the filter: density, not edge) and GROWL 76 (after the filter: the edge).
    GROWL is inert below about 28 and fuzzy by about 70; 76 is a real step, not "a touch". The probe (below) steps it: the held note's crest falls 5.8 -> 3.7 -> 2.3 -> 1.5 dB for GROWL 0 -> 55 -> 76 -> 100 (a square is 0).
  * **The sustain is the envelope's, the squash is GROWL's:** AMP SUSTAIN 127 holds the note (it loses 0.2 dB in 3 s even at GROWL 0); GROWL then flattens the waveform and its loudness trim keeps the level, so a decaying input still sounds sustained. The finished patch's 3 s hold loses 0.1 dB from its first to its last half second.
  * **Snappy and punchy:** a filter snap (ENV AMT 120, decay 46 ms to sustain 40, centroid of the first 23 ms 1663 Hz -> next 67 ms 1595 Hz on the held note; first stab 1809 -> 1770) and the 2.4 ms attack. **What I cannot do:** GROWL flattens the dynamics, so
    the punch is small in level (the strike is +0.5 dB over the plateau) and lives in the 2 ms rise and the brightness settle. More punch means a lower GROWL (less wall) or a lower resting cutoff (less open): C / D trade along that.
  * **BIAS** (asymmetry, even harmonics): 15 -> 80 only lifts the peak 0.8 dB (crest 5.3 -> 6.1) and does not move the centroid: left at 45, a mild asymmetry. **TONE** (a one-pole, weighted in with GROWL): 25 -> 90 moves the centroid 1251 -> 2051 Hz at the same level: the audible one; 55 = the middle.
  * **No spring, delay or tape:** ALLEY, DRAIN, CHEW 0, DLY MIX 0. **Not boingy:** nothing to bounce.
* **The axes I judged most uncertain:** (1) **the fuzz intensity** (GROWL / BIAS / TONE: B 76 / 45 / 55, C 104 / 72 / 64) against sustain, and (2) **the size of the wall** (POLY with two saws a voice against DUAL, four saws a note).
* **Control limits foreseen (and found):** no gate or octave-up fuzz (existing controls only); GROWL's trim means the patch holds its loudness whatever GROWL is, so the knob changes the sound, not the level; a three-note chord needs POLY >= 6 in DUAL; the fuzz is dry by brief so the only "tail" is the amp release.

## Variant B values (the first-draft recommendation, as rendered; NOT the approved variant), each change before -> after

* O1_LVL 110 -> 118 (+6%)
* O2_WAVE PULSE -> SAW
* O2_LVL 100 -> 118 (+14%)
* O2_SEMI -12 -> +0 st
* O2_FINE 70 -> 76 (centre 64: +6 -> +12, +5% of range) (+4.7 cents -> +9.4 cents)
* CUTOFF 40 -> 88 (+38%) (131 Hz -> 2093 Hz)
* RESO 30 -> 80 (+39%)
* FENV_AMT 109 -> 120 (centre 64: +45 -> +56, +9% of range)
* DRIVE 40 -> 100 (+47%)
* FA 20 -> 2 (-14%) (2 ms -> 1 ms)
* FD 60 -> 58 (-2%) (54 ms -> 46 ms)
* FS 10 -> 40 (+24%)
* FR 60 -> 40 (-16%) (54 ms -> 11 ms)
* AA 2 -> 20 (+14%) (1 ms -> 2 ms)
* AD 70 -> 75 (+4%) (117 ms -> 173 ms)
* AS 100 -> 127 (+21%)
* AR 30 -> 70 (+31%) (5 ms -> 117 ms)
* MODE MONO -> POLY
* GLIDE 10 -> 0 (-8%)
* VINTAGE 30 -> 60 (+24%)
* SPREAD 60 -> 70 (+8%)
* VOLUME 100 -> 77 (-18%)
* GRL_BIAS 40 -> 45 (+4%)
* GRL_TONE 50 -> 55 (+4%)
* GROWL 0 -> 76 (+60%)
* POLY_N 5 -> 6 voices

## Level, and how it was read (README §3, §12)

**-17.9 dBFS RMS over the note-on region of the wall phrase (phrase k)**; phrase (b) -16.0 (difference +1.9 dB: the chords of (b) read hotter than the wall phrase, whose notes are mostly single or held; outside the +-1.5 dB band), K-weighted -16.4.
**Peak -12.4 dBFS** (on the wall phrase). VOLUME 100 -> 77. **Crest factor: 5.5 dB over the wall phrase, 2.3 dB on the held A2, 3.6 dB on the held power chord** (a square wave 0 dB, a sine 3 dB; the original's held note: 5.0).
The signal is compressed to a near-constant amplitude, so RMS and peak sit 5.5 dB apart and the patch will sound louder than the same RMS on a patch with a 9 dB crest. If it sits too loud next to the bank in practice, VOLUME is the lever (0.17 dB a step).

## The attack, in ms (the brief asks for it)

AMP ATTACK **20 = 2.4 ms** by the engine's time table (the original: 2 = 0.6 ms). Measured on a high probe note (A5, so a millisecond is resolvable) struck from silence: the voice alone rises 10-90 % of its plateau in **2.0 ms** (key-down to 90 % in 2.2 ms);
as rendered, through the fuzz, **2.0 ms** 10-90 % (2.2 ms to 90 %). The level at 2 / 5 / 10 / 20 / 50 ms is -0.7 / -0.4 / -0.1 / +0.2 / +0.5 dB re the plateau: the bloom is instant (under 1 dB down at 2 ms).
It is not zero: AMP ATTACK 0 would be 0.5 ms; this is five times that, a very short push in on the strike. (Seen while tuning, not tabled: at VOLUME 100 instead of the trimmed 77, GROWL's loudness trim started a note from silence about 4 dB under its plateau and took ~25 ms to 90 %: set VOLUME before judging the strike.)

## Sustain and the tail

The 3 s hold, level per half second: -20.0 -20.1 -20.1 -20.1 -20.0 -20.1 dBFS: flat to within 0.1 dB. After the key-up the level is -20 / -40 / -60 dB at 118 / 206 / 274 ms (AMP RELEASE 70 = 117 ms to 5 %): a slight tail, not a ring;
the held power chord: 148 / 240 / 314 ms. The voice alone and the output are the same (no effects).

## Resonance: what I chose and why (the self-oscillation probe)

RESO **80 of 127** (63 %). The probe feeds the filter noise only (oscillators off), twice, 12 dB apart: a linear filter answers 12 dB apart, a singing one answers with far less (its level is set by its own saturation). B's filter, by RESO: 80: 12.0 / 100: 12.0 / 115: 12.0 / 120: 11.8 / 124: 3.3 / 127: 0.3
(12.0 = linear). It is linear to RESO 115, still 11.8 at 120, and **sings from about 124** (3.3 dB at 124, 0.3 at 127): RESO 80 is well clear of it, and "quite open" has room up to ~120 before the filter starts to ring by itself. (A's row shows nothing meaningful: its filter is nearly shut at the notes.)

## The variants (full tables in the README next to the WAVs)

| | **A** original | **B** centre | **C** fiercer | **D** wall |
|---|---|---|---|---|
| VOLUME | 100 | 77 | 77 | 61 |
| level reading, dBFS | -21.5 | -17.9 | -18.1 | -18.1 |
| phrase (b) RMS, dBFS (difference to the level reading) | -20.9 (+0.6) | -16.0 (+1.9) | -16.1 (+2.0) | -18.3 (-0.2) |
| peak, dBFS | -13.8 | -12.4 | -12.8 | -13.0 |
| worst-case CPU, host instr/sample | 317 | 1414 | 1414 | 1964 |
| centroid Hz, wall / stabs | 146 / 171 | 1656 / 1621 | 2058 / 1886 | 1479 / 1539 |
| crest dB: phrase / held A2 / held chord | 7.6 / 5.0 / 4.8 | 5.5 / 2.3 / 3.6 | 5.2 / 1.7 / 3.2 | 5.1 / 3.5 / 3.6 |
| sustain loss over the 3 s hold (dB) | +0.8 | +0.1 | +0.0 | -0.3 |
| attack 10-90 %, as rendered (ms) · level at 2 ms re plateau | 0.2 · +14.7 | 2.0 · -0.7 | 1.0 · -0.3 | 2.5 · -1.2 |
| tail -60 dB after the 3 s note / the chord (ms) | 22 / 28 | 274 / 314 | 278 / 314 | 278 / 314 |

* **A** the nearest-base patch. **B** (recommended): POLY, GROWL 76 / BIAS 45 / TONE 55. **C**: fiercer, GROWL 104 / BIAS 72 / TONE 64 (brighter: centroid 2058 Hz, held crest 1.7 dB, more squash, the peak -12.8). **D**: B as DUAL (four saws a note, UNI_DET 40: a pair ~10 cents apart), VOLUME 61, 1964 instr/sample.

### GROWL probe (B with GROWL stepped, VOLUME unchanged)

| GROWL | level dBFS | peak dBFS | crest, phrase (dB) | crest, held A2 (dB) | centroid Hz | 3 s sustain loss (dB) |
|---|---|---|---|---|---|---|
| 0 | -17.6 | -7.3 | 10.3 | 5.8 | 2110 | +0.2 |
| 28 | -17.6 | -8.8 | 8.8 | 5.6 | 1792 | +0.2 |
| 40 | -17.6 | -10.0 | 7.7 | 4.6 | 1568 | +0.2 |
| 55 | -17.7 | -11.3 | 6.4 | 3.7 | 1565 | +0.2 |
| 76 | -17.9 | -12.4 | 5.5 | 2.3 | 1656 | +0.1 |
| 100 | -18.0 | -12.8 | 5.1 | 1.5 | 1871 | -0.0 |
| 127 | -18.1 | -12.9 | 4.9 | 1.5 | 2078 | -0.0 |

## Recommendation

**B.** The wall holds (flat to 0.1 dB over 3 s, held crest 2.3 dB), it is dry, it has a 2.0 ms rise with an instant bloom, the filter is open at a resonance that cannot sing, and it keeps a three-note chord whole. C is for "more": GROWL 104, BIAS 72, TONE 64 is squashed to a 1.7 dB crest and brighter (2058 Hz).
D is for "bigger": DUAL doubles the oscillators under the same clip (a held crest of 3.5 dB: less flat than B's 2.3) at 1964 instr/sample against 1414 (worst case, host instructions; the device yardstick is the render time on the GLOBAL page, CLAUDE.md §2).

## Open for the ears

* Is it HUGE (the benchmark is a Fuzz War): if not, C first (GROWL 104), then D (four saws a note).
* Snappy and punchy enough? The strike is small in level by nature of the clip (+0.5 dB over the plateau); the filter snap is in the brightness. A lower GROWL (55-65) keeps more dynamics at the price of less wall.
* Is the tail (274 ms to -60 dB) "slight", or too long / short for a go-to fuzz (AMP RELEASE)?
* The six-voice POLY window plays a power chord whole; a bigger voicing (5+ notes) steals.
