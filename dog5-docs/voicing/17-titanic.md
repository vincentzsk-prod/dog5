# Voicing log — 17 "Titanic" (FACTORY[16], Batch 2A, the chapter anchor)

Nov 2026. Brief (Batch 2A, "weight and space"): *the chapter anchor. Dual saws a fifth apart, extreme bass-comp on the filter, low where the engine opens up. Freezing, desolate
weight. Tape dropouts (CHEW) optional garnish.* A CS-80 played low and cold (Moog Taurus floor, Memorymoog thickness, Prophet-5 dual saws a fifth apart). Method and kit: `README.md` here
(§1 phrases, §3 loudness, §10 Batch 2A). Listening files (on the `listen/batch-02a-weight-and-space` branch only): `listen/voicing/batch-02a/17-titanic/`; `README.md` and `numbers.md`
there are the full tables and are on the voicing branch too.

**Status: B (centre) COMMITTED as the recommended variant, awaiting Vincent's ears.** A, C, D are render-only. **Round count so far: 1 silent measured round (several quick passes of the
variant table) + 0 listening rounds.** No voice card yet (written after approval).

## 0. Before

* **Current values (the full list over the defaults):** MODE DUAL, DETUNE 60 (the pair 21.9 cents apart), OSC1 SAW at 110, **OSC 2 OFF**, CUTOFF 70 (740 Hz base), SPREAD 110; everything else default
  (LP24, RESO 20, ENV AMT 90, KEY TRK 64, filter env A20 D70 S40 R60, amp env A10 D70 S100 R60, VINTAGE 30, POLY 5, no LFO, no FX). Name `Titanic`.
* **What the nearest starting patch does.** `PF_DUAL_SAW`, **not shared any more**: it was Half-Life's base until Batch 1A and had only Titanic left (checked: it is used by no other slot), so it was
  renamed `PF_TITANIC` in place. It is a single saw per voice, doubled by DUAL into a wide (22 cents) pair, a default envelope and no effects: a plain, wide, slightly bright dual saw. Measured: steady
  hold -20.9 dBFS RMS on phrase f, (b) -17.6; 51 % of the energy under 60 Hz, centroid 275 Hz (5.3 partials at A1); no fifth, no bass compensation to speak of (A1 / A2 / A3 at 5.3 / 4.1 / 3.1 partials), fast and short (release -60 dB in 150 ms).
* **The axes I judged most uncertain:** (1) **how cold/dark versus open** (CUTOFF with KEY TRK: how far the bass comp goes and how dark the top of the stack is); (2) **the garnish**: whether
  tape dropouts help or distract (CHEW costs CPU all the time). Not varied, but worth a word: the pair width (22 -> 5.5 cents, narrower for cold).
* **Control limits foreseen:** no latch/drone, so "frozen" is a long release, not a held note; DUAL makes every note two voices (POLY 6 for a 3-note chord); the bass comp is KEY TRK only (0..127 =
  0..100 %), there is no negative tracking: low notes open as far as the cutoff goes and high notes close only to where KEY TRK 0 leaves them.

## Final parameter list (what the tree holds now = variant B)

`PF_TITANIC` in `firmware/src/obv_patches.h` (its own array). Over the defaults; was = the original:

| byte | parameter | value | was | in its own units |
|---|---|---|---|---|
| 4 | OSC2 WAVE | **SAW** | OFF | the second saw |
| 7 | OSC2 SEMI | **+7 st** | 0 | the fifth |
| 12 | CUTOFF | **66** | 70 | 587 Hz base (740 before) |
| 13 | RESO | **12** | 20 | |
| 14 | ENV AMT | **84** | 90 | +20 around the centre |
| 15 | KEY TRK | **12** | 64 | 9 % (50 % before): the bass compensation |
| 20 | FILTER ATTACK | **62** | 20 | 63 ms |
| 21 | FILTER DECAY | **90** | 70 | 558 ms |
| 22 | FILTER SUSTAIN | **70** | 40 | |
| 23 | FILTER RELEASE | **85** | 60 | 378 ms |
| 24 | AMP ATTACK | **60** | 10 | 54 ms |
| 26 | AMP SUSTAIN | **127** | 100 | |
| 27 | AMP RELEASE | **92** | 60 | 653 ms to the 5 % point (-60 dB at 1.3 s) |
| 38 | MODE | DUAL | DUAL | |
| 40 | DETUNE | **30** | 60 | the pair 5.5 cents apart (22 before) |
| 42 | VINTAGE | **40** | 30 | wander s.d. 1.9 cents, offsets -2.8 / +1.0 |
| 43 | SPREAD | 110 | 110 | |
| 45 | VOLUME | **93** | 100 | the bank reference on the steady hold |
| 63 | POLY | **6** | 5 | a three-note stab = 6 voices, no stealing |

Everything else default (OSC1 SAW at 110, LP24, GROWL / ALLEY / DRAIN / CHEW 0, no LFO, no arp). The committed bytes equal variant B's list (`tests/voicing/check_slot.py 17 B`: identical, and the program-load render is bit-identical to the variant render on a, b, c and f).

## Level (how it is read, README §10)

**-17.9 dBFS RMS over +6..+10 s of the A1 hold (phrase f)**, the bloomed/steady state; reference -18.0. Phrase (b): -17.1 (difference +0.8 dB), K-weighted -17.4. Peak -4.4 dBFS on the most demanding
phrase (limit -4). Riff -20.1, held A2 -18.4.

## Character notes (what to expect, from the numbers)

* **Bass compensation, extreme:** the same note struck at A1 / A2 / A3 puts **8.4 / 5.5 / 3.4** partials under the centroid (the original 5.3 / 4.1 / 3.1) and A1 is 0.6 dB louder than A3 (the original: 0.4 dB): the low notes open up, the
  high ones close. C (KEY TRK 0, CUTOFF 54) goes the other way on the whole: 5.9 / 3.8 / 2.3.
* **Weight:** at equal level the stack is 28 % under 60 Hz, 45 % in 60-150 Hz (the fifth sits there: E2 is 82 Hz over A1) and 21 % in 150-400 Hz; only 6 % above 400 Hz, none above 1.2 kHz. "Freezing and desolate" is dark and
  hollow, not bright: if it should glint, CUTOFF is the knob (untested by ear).
* **Settles, does not bloom:** the first second has 32 % of its energy in 150-400 Hz against 21 % in the steady hold (the filter envelope's 63 ms attack, then 558 ms of decay to sustain 70), so the note starts a little more open and settles onto its weight; there is no swell (the bloom rows are not in 17's table; the second-by-second
  table shows it).
* **Slop / beat:** the DUAL pair beats at 0.47 Hz (A: 0.70) with a 25 dB deep envelope; each card wanders +-2 cents s.d. (A: 1.4): steady, cold, a slow throb. VINTAGE 40 only.
* **Release:** 496 / 970 / 1300 ms to -20 / -40 / -60 dB after a long hold (the original: 60 / 104 / 150 ms), 420 / 884 / 1288 ms after the 2.4 s A2 note: it hangs. Chopped riffs run into each other at 250 ms steps (releases overlap);
  that is the price of "frozen".
* **CPU:** worst case 1594 host instr/sample (idle 104 + load 1490), the original 1070; DUAL x two oscillators.

## The axes chosen, and why

1. **cold / comp (C):** KEY TRK 12 -> 0, CUTOFF 66 -> 54, filter and amp attack 117 ms, AMP RELEASE 92 -> 104 (1.7 s to the 5 % point, -60 dB at 3.0 s). Centroid 294 Hz against B's 421. Heavier and darker, at the cost of dulling
   the top notes (2.3 partials at A3).
2. **garnish (D):** B plus CHEW 80, DROPS 100. The tape adds hiss and wow (centroid 421 -> 788 Hz is mostly the hiss), one dropout of 8 dB in the 10 s hold (dips of >= 6 dB: 1), a noise floor of -68.8 dBFS that rests 3.5 s after the key-up, a release
   to -60 dB that takes 4.6 s because of the hiss, and +777 host instr/sample worst case (866 of idle against 104: always on). It is a garnish by design: the dropouts are rare (about one a hold at this setting).

## What DRAIN does on a bass (probe, not a variant; B with the spring added)

The brief's note was that DRAIN does very little on bass because of the 150 Hz high-pass ahead of the tank. **Measured, it is a one-pole high-pass (-9 dB at 55 Hz, not a wall), and on Titanic the spring is clearly audible:**

| DRAIN | return re the dry signal | in 150-400 Hz re the dry's own | in 400-1.2k | share of the return < 150 Hz |
|---|---|---|---|---|
| 30 | -11.0 dB | -8 dB | -15 dB | 12 % |
| 60 | -5.0 dB | -2 dB | -9 dB | 12 % |
| 100 | -0.5 dB | +3 dB | -4 dB | 12 % |

The return is the stack's *harmonics* (centroid 490 Hz, 88 % above 150 Hz): the weight stays dry (<60 Hz: -18 dB at DRAIN 60) and a cloud of 150-400 Hz rings above it. Whether that is "frozen" or "muddy" is for the ears;
it is not in B (DRAIN 0, dry is the brief), and the macro is there live. Cost about +490 host instr/sample if added (09's idle: 589 against 104).

## For Vincent's ears (questions)

* B against C: **cold and dark, or colder and darker?** Is B's top already too dull for "chapter anchor" (it has nothing above 1.2 kHz)?
* Is the **fifth** a hollow power chord (as designed) or a hum? OSC 2 is at full level; a lower O2 LEVEL would hide it, a higher DETUNE would warm it.
* Is the **long release** right on chopped riffs, or should the release come down to ~400 ms (AMP RELEASE 85)?
* D: garnish or distraction? And a listen to B with DRAIN ~40 live.

## Round count

1 silent measured round (variant-table passes on the quick harness), 0 listening rounds.
