# Voicing log — 01 "Red Pill" (FACTORY[0], Batch 3A, the fat and driven set)

5 Nov 2026. Brief (Batch 3A, Chapter I): *a nervous, spitting bass that sits under a vocal. Fat detuned saws, low and resonant. TIGHT AND STABLE: minimal slop or movement (VINTAGE low, no LFO wobble). GRITTY and DRIVEN, warm with MEDIUM brightness, not harsh or piercing.
RELATIVELY DRY, but a slight wetness (spring and/or echo) enough to elevate the presence; the wet must never dominate the note.* Closest to: an MS-20 bass through a RAT (MS-20 nasty/biting/resonant, Minimoog fat/thick, SH-101 tight/punchy, ProCo RAT gritty/crunchy). Method and kit: `README.md` here (§1 phrases, §3 loudness, §12 Batch 3A).

**Status: RECOMMENDED B (centre), committed as the patch; awaiting Vincent's listening.** Round count so far: 1 silent measured round (tuning sweeps and the variants, no ears) + 1 listening round pending. Branches: code, logs, tables on `voicing/batch-03a-chapter1-fat-and-driven`; all WAVs only on `listen/batch-03a-chapter1-fat-and-driven` (`listen/voicing/batch-03a/01-red-pill/`). Full tables: `listen/voicing/batch-03a/01-red-pill/README.md` and `numbers.md` (on the voicing branch too).

## 0. Before

* **Current values (the full list over the defaults):** O2_WAVE 2, O2_PW 50, O2_SEMI 12, CUTOFF 40, RESO 30, FENV_AMT 109, DRIVE 40, FD 60, FS 10, AA 2, AR 30, MODE 3, GLIDE 10 (VOLUME 100 is the default). Name `Red Pill`.
* **Shared array:** `PF_FAT_BASS` was shared with **06 zzuFuzz and 27 R3V3RT**. 01 now has its own `PF_RED_PILL`; `PF_FAT_BASS` stays with 27 (06 got its own as well).
* **What the nearest starting patch does:** a MONO bass of one saw plus a pulse an octave below, a 131 Hz base cutoff, a plucking filter (decay 54 ms, sustain 10), DRIVE 40, no effects. Measured on the spit riff: **-19.7 dBFS RMS**, phrase (b) -20.9,
  peak -13.8, crest 5.5 dB, centroid 108 Hz with **98 % of the energy under 60 Hz**: it is a sub with almost no upper partials (the cutoff sits at the notes), nothing that cuts through a vocal.
* **The axes I judged most uncertain:** (1) **the wet amount** (a slap and a short spring "enough to elevate presence" and never above the note: measured per window) and (2) **the grit level** (per-voice DRIVE against a RAT-style GROWL step).
* **Control limits foreseen (and found):** the per-voice DRIVE sits *before* the filter, so it adds density and warmth but the low-pass takes the edge back (centroid 622 Hz at DRIVE 88 against 650 at DRIVE 0); the edge that survives comes from the filter's resonance and
  from GROWL (after the filter), which costs about +593 instr/sample whenever it is on; the echo is a faithful copy of the note (ALLEY TONE is inert on a bass echo), so the presence comes from its level and time; MONO does not re-fire the envelopes on a legato note
  (the spit is a detached-note sound).

## Final values (variant B, `PF_RED_PILL`), each change before -> after

* O2_WAVE PULSE -> SAW
* O2_LVL 100 -> 104 (+3%)
* O2_SEMI -12 -> +0 st
* O2_FINE 70 -> 74 (centre 64: +6 -> +10, +3% of range) (+4.7 cents -> +7.8 cents)
* CUTOFF 40 -> 92 (+41%) (131 Hz -> 2637 Hz)
* RESO 30 -> 58 (+22%)
* FENV_AMT 109 -> 104 (centre 64: +45 -> +40, -4% of range)
* KEYTRK 64 -> 100 (+28%)
* DRIVE 40 -> 88 (+38%)
* FA 20 -> 0 (-16%) (2 ms -> 0 ms)
* FD 60 -> 52 (-6%) (54 ms -> 29 ms)
* FS 10 -> 30 (+16%)
* FR 60 -> 40 (-16%) (54 ms -> 11 ms)
* AA 2 -> 0 (-2%) (1 ms -> 0 ms)
* AS 100 -> 127 (+21%)
* AR 30 -> 26 (-3%) (5 ms -> 4 ms)
* GLIDE 10 -> 0 (-8%)
* VINTAGE 30 -> 10 (-16%)
* SPREAD 60 -> 40 (-16%)
* VOLUME 100 -> 89 (-9%)
* DLY_FB 50 -> 10 (-31%)
* DLY_TONE 70 -> 60 (-8%)
* DLY_MIX 0 -> 30 (+24%)
* REV_SIZE 80 -> 40 (-31%)
* REV_DAMP 60 -> 70 (+8%)
* REV_MIX 0 -> 30 (+24%)
* ALLEY 0 -> 62 (+49%) (SYNC -> 80 ms)
* BBD_SPREAD 127 -> 0 (-100%)

Dictionary moves, in the vocabulary: *fat/thick* = two saws in unison pitch 7.8 cents apart (beating 0.25 Hz at A1); *tight and stable* = VINTAGE 30 -> 10 (-16 %), no LFO, GLIDE 10 -> 0; *warm / driven* = DRIVE 40 -> 88 (+38 %); *medium brightness* = CUTOFF 40 -> 92 (+41 %) with KEY TRK 64 -> 100;
*resonant* = RESO 30 -> 58 (+22 %); *spit* = the filter envelope's decay 60 -> 52 (54 -> 29 ms) and sustain 10 -> 30; *slight wet* = DLY MIX 0 -> 30, DRAIN 0 -> 30.

## Level (README §3)

**-17.9 dBFS RMS over the note-on region of the spit riff (phrase i)**; phrase (b) -18.0 (difference -0.0 dB), K-weighted -18.0. **Peak -10.8 dBFS** (on the stabs). VOLUME 100 -> 89. Crest factor 4.8 dB on the riff.

## The wet return, per time window (the brief's measure)

The effects' own return (the render minus the same render with DLY MIX and DRAIN at 0) in dB re the dry note, in the 0-20 / 20-100 / 100-250 ms after the note-on, for B's three isolated notes (phrase i):

| note | 0-20 ms | 20-100 ms | 100-250 ms |
|---|---|---|---|
| A1, gate 150 ms | -41.0 | -20.9 | -11.7 |
| D2, gate 150 ms | -39.6 | -20.5 | -15.3 |
| A1, gate 300 ms | -42.1 | -20.8 | -17.0 |

Worst over the three notes: **B -39.6 / -20.5 / -11.7 dB**, C -43.6 / -25.0 / -16.5, D -34.8 / -15.5 / -6.3. So B is under the dry note in every window, by at least 12 dB; the last window is the tight one
because the 150 ms note is already ending in it (the dry there is its release). Over the whole phrase the return is -15.7 dB re the dry (C -20.5, D -10.4). The return is mostly low (centroid 678 Hz, 76 % under 150 Hz).
Tail: the voice alone is 60 dB down 30 ms after the key-up; with the wet 102 / 276 / 486 ms to -20 / -40 / -60 dB.

## The variants (full tables in the README next to the WAVs)

| | **A** original | **B** centre | **C** grit | **D** wet |
|---|---|---|---|---|
| VOLUME | 100 | 89 | 87 | 89 |
| level reading, dBFS | -19.7 | -17.9 | -18.0 | -17.9 |
| phrase (b) RMS, dBFS (difference to the level reading) | -20.9 (-1.2) | -18.0 (-0.0) | -18.0 (+0.0) | -17.6 (+0.3) |
| peak, dBFS | -13.8 | -10.8 | -12.8 | -8.2 |
| worst-case CPU, host instr/sample | 317 | 1047 | 1640 | 1047 |
| centroid Hz, spit riff / stabs | 108 / 171 | 622 / 1406 | 625 / 1295 | 654 / 1411 |
| crest dB, spit riff | 5.5 | 4.8 | 4.6 | 6.1 |
| worst wet window re dry (dB) 0-20 / 20-100 / 100-250 | no wet | -40/-20/-12 | -44/-25/-16 | -35/-16/-6 |
| wander s.d. cents (card 0, held A2) | 1.0 | 0.3 | 0.3 | 0.3 |

* **A** the nearest-base patch. **B** (recommended): detuned saws, tight, DRIVE 88, a slight slap + spring. **C**: DRIVE 110 and GROWL 46 (RAT-style), less wet (DLY MIX 16, DRAIN 18). **D**: the wet at its upper limit (MIX 52 / DRAIN 52, SIZE 55): the echo is within 6 dB of the note in the last window, which is where 'slight' ends.

## Recommendation

**B.** It is the version that answers every line of the brief with a number: stable (wander s.d. 0.3 cents), driven (crest 4.8 dB), medium bright (centroid 622 Hz, 1406 on chords), a wet that is always at least 12 dB under the note, at 1047 instr/sample worst case.
C is the one to ask for if B is not gritty enough: the GROWL step adds the RAT's edge at +593 instr/sample. D is a reference for where the wet stops being slight.

## Open for the ears

* Is the grit enough, and is it warm rather than harsh (B against C)?
* Is the wet "enough to elevate the presence", or should it come up toward D (the slap at 30 of 127 is -20.5 dB re the note at 20-100 ms)?
* Is a 55 Hz fundamental audible enough under a vocal on the PA (51 % of the energy is under 60 Hz)? If not: KEY TRK / CUTOFF can lift the 2nd-4th harmonics; an octave-up oscillator would change the character.
