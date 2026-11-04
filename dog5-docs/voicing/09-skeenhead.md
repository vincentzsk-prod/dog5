# Voicing log — 09 "Skeenhead" (FACTORY[8], Batch 2A, the reggae off-beat stab)

Nov 2026. Brief (Batch 2A, "weight and space"): *the reggae off-beat stab. Tight plucky square, a resonant filter plop, drenched in spring. The spring chirp is the sound.* An MS-20 plop into a
Fender-style spring tank (SH-101 tightness, Prodigy rawness, a Space-Echo dub warmth in the tail). Method and kit: `README.md` here (§1 phrases, §3 loudness, §10 Batch 2A). Listening files (on the
`listen/batch-02a-weight-and-space` branch only): `listen/voicing/batch-02a/09-skeenhead/`; `README.md` and `numbers.md` there are the full tables and are on the voicing branch too.

**Status: B (centre) COMMITTED as the recommended variant, awaiting Vincent's ears.** A, C, D are render-only. **Round count so far: 1 silent measured round + 0 listening rounds.** No voice card yet.

## 0. Before

* **Current values (the full list over the defaults):** OSC 1 PULSE PW 20 %, OSC 2 PULSE PW 20 % FINE +2.3 cents (two narrow pulses), FILTER LP12, CUTOFF 55 (311 Hz base), RESO 40, ENV AMT 127 (full), KEY TRK 127,
  filter env DECAY 35 (8 ms) SUSTAIN 0, amp env ATTACK 1, DECAY 60 (54 ms) SUSTAIN 0 RELEASE 30 (5 ms). Everything else default. **No spring, no echo (DRAIN 0, MIX 0).** Name `Skeenhead`.
* **What the nearest starting patch does.** `PF_CLAV_PLUCK`, **not shared** (only 09 uses it; renamed `PF_SKEENHEAD` in place): a clavinet-style pluck, two narrow pulses, a very fast filter snap, an amp that dies in ~55 ms, bone dry.
  Measured on the skank: **-29.3 dBFS RMS** (the crest is 25 dB: the peak is -4.5), centroid 655 Hz, first 23 ms 542 Hz vs 727 Hz next (it gets brighter, there is no plop), the amp falls 43 dB inside the 110 ms gate; the tail is 20 ms.
  The "drenched in spring" part of the brief is entirely new.
* **The axes I judged most uncertain:** (1) **the spring** (how wet and how long before it masks the next stab or goes tubby: DRAIN, SIZE, PRE-DLY, DAMP); (2) **the plop** (resonance, cutoff and the filter's fall time:
  how deep and rounded the MS-20 "bwop").
* **Control limits foreseen:** the tank is a re-voiced plate (chirp chains of 5-sample allpasses, SIZE 0.3-3.0 s), not a measured spring: it is "the next closest thing"; a fast pluck cannot reach the reference
  level (README §10): the spring tail does not count in the level reading, so B's body is kept at 117 ms of amp decay (the snap lives in the filter); the peak sits at the -4 limit with this crest (see Level).

## Final parameter list (what the tree holds now = variant B)

`PF_SKEENHEAD` in `firmware/src/obv_patches.h`. Over the defaults; was = the original:

| byte | parameter | value | was | in its own units |
|---|---|---|---|---|
| 0 | OSC1 WAVE | PULSE | PULSE | |
| 1 | OSC1 PW | **64** | 20 | a 50 % square |
| 4 | OSC2 WAVE | **OFF** | PULSE | one oscillator |
| 5, 11 | OSC2 PW / FINE | default | 20 / 67 | (inert with OSC 2 off) |
| 12 | CUTOFF | **40** | 55 | 131 Hz base (311 before); rests near 115 Hz under an A3 |
| 13 | RESO | **62** | 40 | |
| 14 | ENV AMT | **118** | 127 | +54 around the centre |
| 15 | KEY TRK | **100** | 127 | 79 % |
| 16 | FILTER TYPE | LP12 | LP12 | |
| 21 | FILTER DECAY | **56** | 35 | 39 ms (8 ms before): the plop |
| 22 | FILTER SUSTAIN | 0 | 0 | |
| 24 | AMP ATTACK | **0** | 1 | 0.5 ms |
| 25 | AMP DECAY | default 70 | 60 | 117 ms (54 before) |
| 26 | AMP SUSTAIN | **30** | 0 | a body for the gate |
| 27 | AMP RELEASE | 28 | 30 | 4 ms: the voice stops dead, the spring carries the tail |
| 45 | VOLUME | **115** | 100 | the bank reference, spring on |
| 59 | SPRING SIZE | **70** | 80 | tail -60 dB at 1.0 s |
| 60 | SPRING DAMP | **40** | 60 | brighter |
| 61 | SPRING PRE-DLY | **4** | 20 | 4 ms: the chirp starts at once |
| 62 | **DRAIN** | **90** | 0 | the spring's wet (the macro) |

Everything else default (GROWL / ALLEY / CHEW 0, no LFO, no arp, MODE POLY, POLY 5). The committed bytes equal variant B's list (`tests/voicing/check_slot.py 9 B`: identical; bit-identical audio when both are loaded from INIT; loaded from the boot patch the spring
patch's slew floor puts the two ~27-31 dB apart, README §8).

## Level (how it is read, README §10)

**-18.1 dBFS RMS over the stabs' note-on region of phrase g, with the spring on** (11 stabs x 110 ms; tails excluded). The dry stabs alone are -19.6: **the spring adds 1.5 dB to the reading**, and the VOLUME 115 includes that. Phrase (b): -18.6
(difference -0.5), K-weighted -19.4. **Peak -4.4 dBFS** (limit -4; the trim stops at -4.3: the crest of a plucked stab is the limit, not the level). Riff -22.5, held A2 -28.6 (a stab patch on a held note decays to its sustain 30).

## Character notes (what to expect, from the numbers)

* **The plop:** the first 23 ms of a stab are 689 Hz, the next 67 ms 318 Hz (x2.2; the original went 542 -> 727). Inside the 110 ms gate the amp falls 16.7 dB and 10 dB in 32 ms; the filter rests below the note, so the body is the resonance and the
  fundamental under it: a rounded, bwop-ish stab.
* **The spring, inside the stab:** its return is **-4.2 dB** under the dry stab (energy over the stabs); over the whole phrase including the tails it is -2.2 dB. It is 82 % in 150-400 Hz, 13 % in 400-1.2k, 4 % above: the spring's centroid is 1507 Hz against the
  dry stab's 1998 Hz.
* **The gap:** the 1.3 s of two empty off-beats sits **-18.2 dB** under the stab at its start; 1 s after the last stab the tail is -16.1 dB under the stab, and the tail from the last stab runs -20 / -40 / -60 dB at **0.32 / 0.71 / 0.99 s**
  (the voice alone is dead at 24 ms). In the dense bars (a stab every 500 ms) each stab therefore lands on the previous one's tail at roughly -30 dB (-20 dB at 0.32 s, -40 dB at 0.71 s); the two empty off-beats are where the tail is heard alone.
* **Cost:** worst case 1171 host instr/sample (idle 589, the spring's always-on cost, + load 582); the original 706.
* **Not measured, only listenable:** the *chirp* itself (the dispersive sweep that makes a tank a tank). The numbers say the tail is bright and early (PRE-DLY 4 ms, DAMP 40, centroid ~1.5 kHz); whether it reads as a spring is for the ears.

## The axes chosen, and why

1. **the spring (C drench):** DRAIN 90 -> 115, SIZE 70 -> 95, PRE-DLY 4 -> 0. The return is -1.6 dB under the stab inside it (+1.6 dB over the whole phrase: the tails add up to more than the stabs), the gap -13.4 dB, the tail -60 dB at 1.52 s. Level trimmed to -18.1
   (VOLUME 110). The risk is tubby (82 % of its energy in 150-400 Hz is the same as B).
2. **the plop (D plop):** CUTOFF 40 -> 34, RESO 62 -> 80, FILTER DECAY 56 -> 66 (39 -> 117 ms): the first 23 ms are 1157 Hz against 348 Hz (x3.3), the amp falls 20.5 dB inside the gate. Rounder and deeper; the highest peak of the three before the guard (trimmed to VOLUME 106, level -18.3).

## For Vincent's ears (questions)

* **Does B's spring read as a spring tank** (the chirp on the stab's attack) or as a short reverb? If not, DAMP, PRE-DLY and SIZE are the knobs; C is the same with more and longer.
* **Is B drenched enough**, or is C closer? Does C go tubby in the dense bars?
* **Is the plop a plop**, or too bwop / too clavinet? D against B.
* Is the stab too short or too long in B (the voice stops dead after the gate; the spring carries the rest)?

## Round count

1 silent measured round, 0 listening rounds.
