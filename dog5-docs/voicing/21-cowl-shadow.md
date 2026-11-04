# Voicing log — 21 "Cowl Shadow" (FACTORY[20], Batch 2A, the slow brass bloom)

Nov 2026. Brief (Batch 2A, "weight and space"): *a brass wall that takes about 10 seconds to bloom. Five-voice unison, filter envelope sweeping very slowly, gate held open. The textbook slow
patch.* A CS-80 brass swell stretched (Oberheim OB-Xa brass body, Jupiter-8 blare at the top of the swell, Korg Mono/Poly unison drift). Method and kit: `README.md` here (§1 phrases, §3 loudness, §10
Batch 2A). Listening files (on the `listen/batch-02a-weight-and-space` branch only): `listen/voicing/batch-02a/21-cowl-shadow/`; `README.md` and `numbers.md` there are the full tables and are on the voicing branch too.

**Status: B (centre) COMMITTED as the recommended variant, awaiting Vincent's ears.** A, C, D are render-only. **Round count so far: 1 silent measured round (variant-table passes, incl. a sweep of
CUTOFF / ENV AMT pairs that left the bloom shape unchanged) + 0 listening rounds.** No voice card yet.

## 0. Before

* **Current values (the full list over the defaults):** UNISON, 8 voices, DETUNE 80 (the stack spans +-39 cents), OSC 2 saw **an octave below** (-12 st) at LEVEL 100, CUTOFF 45 (175 Hz base), RESO 10, ENV AMT 79, filter
  env ATTACK 100 (1.2 s) otherwise default, amp ATTACK 100 (1.2 s), RELEASE 110 (2.7 s), LFO (TRI, 0.2 Hz) -> FILTER 20, VINTAGE 80, SPREAD 127, spring SIZE 120 (huge), DAMP 80, **DRAIN 50**. Name `Cowl Shadow`.
* **What the nearest starting patch does.** `PF_DRONE_UNI`, **shared with 18 Roto-scopo** (and, until Batch 1A, with 30 THE DØG). So 21 gets its own array `PF_COWL_SHADOW`; `PF_DRONE_UNI` is left alone for 18.
  It is a wide, sub-octave drone: a 1.2 s swell, a slowly wandering filter, a big spring. Measured: **-15.4 dBFS RMS** over the steady hold (+2.6 over the reference), phrase (b) -22.7, 94 % of the energy under 150 Hz,
  centroid 147 Hz; it does not bloom (the centroid falls 0.5 octaves over the hold); 8 voices + the spring cost 2588 host instr/sample worst case.
* **The axes I judged most uncertain:** (1) **bloom time** (the brief says about 10 s; the engine's envelope tops at 10 s and the brightness only gets to 90 % at ~7 s: how much of that does the player want?),
  (2) **how bright it gets at the top** (the Jupiter-style blare against a darker CS-80 wall).
* **Control limits foreseen (stated before building):** the **"Drone Latch" control does not exist**, so the bloom happens while the key is down (a ~10 s hold, or the sustain pedal, CC 64, which does hold it);
  released early the note fades from wherever the filter got to; the longest envelope time is 10 s (ATTACK 127); UNISON does not re-fire its envelopes on a legato note, so a legato second note slides and does not restart the bloom;
  short notes (phrase b) are the dark start of the bloom and read ~21 dB under the bloomed level.

## Final parameter list (what the tree holds now = variant B)

`PF_COWL_SHADOW` in `firmware/src/obv_patches.h` (its own array). Over the defaults; was = the original:

| byte | parameter | value | was | in its own units |
|---|---|---|---|---|
| 7 | OSC2 SEMI | **0 st** | -12 st | the second saw is on the same pitch now: brass, not a drone |
| 11 | OSC2 FINE | 66 | 70 | +1.6 cents (+4.7 before) |
| 12 | CUTOFF | **40** | 45 | 131 Hz base: the dark start |
| 13 | RESO | **14** | 10 | |
| 14 | ENV AMT | **118** | 79 | +54 around the centre: the full bloom |
| 15 | KEY TRK | **127** | 64 | 100 %: the bloom is the same at any pitch |
| 20 | FILTER ATTACK | **127** | 100 | **10 s** (the engine's longest) |
| 22 | FILTER SUSTAIN | **127** | 40 | held open |
| 23 | FILTER RELEASE | **110** | 60 | 2.7 s: the brightness leaves with the level |
| 24 | AMP ATTACK | 96 | 100 | 0.9 s (1.2 s before) |
| 26 | AMP SUSTAIN | **127** | 100 | |
| 27 | AMP RELEASE | 108 | 110 | 2.3 s to the 5 % point (-60 dB at 3.8 s) |
| 38 | MODE | UNISON | UNISON | |
| 39 | VOICES | **5** | 8 | |
| 40 | DETUNE | **40** | 80 | the stack spans +-9.8 cents, 2.4 cents between neighbours (+-39 before) |
| 42 | VINTAGE | **45** | 80 | wander s.d. 1.6-2.1 cents per card |
| 43 | SPREAD | 100 | 127 | |
| 45 | VOLUME | **79** | 100 | the bank reference on the bloomed state |
| 29, 34 | LFO RATE / LFO -> FILTER | default / **0** | 25 / 20 | no LFO on the filter (the bloom is the movement) |
| 59, 60, 62 | SPRING SIZE / DAMP / DRAIN | default / default / **0** | 120 / 80 / 50 | **dry**: no spring (see the questions) |

Everything else default (LP24, OSC1 SAW 110, GROWL / ALLEY / CHEW 0, no arp). The committed bytes equal variant B's list (`tests/voicing/check_slot.py 21 B`: identical; the audio matches bit for bit when both are loaded from INIT; loaded from the boot patch
CUTOFF's slew floor puts the two ~20-38 dB apart, README §8).

## Level (how it is read, README §10)

**-18.1 dBFS RMS over +6..+10 s of the A2 hold (phrase f2)**, the bloomed state; reference -18.0. Whole-hold RMS -18.1 (the dark start included: B's first second is -25.8 dB, a swell of 7.7 dB). **Phrase (b): -38.8 dBFS (difference -20.8 dB):**
chords on a unison patch are the dark start of the bloom, struck and let go before it opens; (b) is not a fair yardstick here and the patch is not for stabs. Peak -7.0 dBFS on any phrase (limit -4). K-weighted (b) -39.6.

## The bloom (A2 held 10 s, phrase f2; per second in the README table)

| | start (+0.25..1.25 s) | steady (+6..10 s) | octaves climbed | 10 % / 90 % of the climb | level 90 % |
|---|---|---|---|---|---|
| A original | 211 Hz, -15.3 dB | 152 Hz, -15.4 dB | -0.5 (it darkens) | | |
| **B centre** | 312 Hz, -25.8 dB | 1775 Hz, -18.1 dB | **2.5** | **2.8 s / 7.1 s** | 1.1 s |
| C quick | 231 Hz, -21.6 dB | 2020 Hz, -18.0 dB | 3.1 | 0.8 s / 4.1 s | 0.8 s |
| D blare | 234 Hz, -21.3 dB | 3925 Hz, -17.9 dB | 4.1 | 1.3 s / 6.3 s | 1.0 s |

B by the second (centroid Hz): 312 218 237 406 508 815 1055 1445 1982 1952. **Nearly nothing happens for the first ~3 s** (the filter envelope's RC attack starts slowly: 312 -> 406 Hz in 3 s), then it climbs about half an octave a
second until ~8 s, then it is there. I tried CUTOFF 44-50 with ENV AMT lowered to keep the top: the shape did not change (10 % of the climb at 2.3-2.8 s, 90 % at 7.1 s in all of them); it is the curve of the 10 s attack, not the start level.
The first second is 97 % in 60-150 Hz (the fundamental alone, very quiet): a dark pad that opens. At the steady state the stack is 47 % in 60-150, 33 % in 150-400, 15 % in 400-1.2k, 5 % above.

## What happens when the key is released (plainly)

* **Held 10 s then released:** the amp falls over 2.3 s (**-20 / -40 / -60 dB at 1.2 / 2.2 / 3.8 s**) and the filter closes with it (FILTER RELEASE 2.7 s), so the wall darkens as it dies instead of snapping dull first.
* **Released early (A2 held 2.4 s, phrase c): it never blooms.** At the key-up the centroid is 213 Hz (the bloomed state is 1775) and the level -16.1 dB; the tail is -20 / -40 dB at 0.7 / 1.9 s. In the player's ears: a dark, soft swell that fades.
  There is no way to keep the bloom going after the key-up with the existing controls. **The sustain pedal (CC 64) holds the note**, and so does a held key; a legato second key does not restart the bloom (unison, no re-fire).

## Character notes (the rest, from the numbers)

* **Beat / wander:** the stack beats at 1.0 Hz (range 0.67-1.35) with a 28 dB deep envelope on A2; each of the five cards wanders +-2 cents s.d., static offsets -3.2 / +1.4 / +0.7 / -2.6 / +2.5 cents.
* **Cost:** 1360 host instr/sample worst case (idle 104 + load 1256); the original 2588 (8 voices and the spring). The patch is **dry**: the original's spring (DRAIN 50, SIZE 120) is gone; the brief does not ask for one.
* **Register:** with KEY TRK 127 the A1 / A2 / A3 notes put 2.8 / 1.7 / 1.5 partials under the centroid *in the first second* (x_register holds 1.5 s, so it sees only the dark start): not a bloom measurement.

## The axes chosen, and why

1. **bloom time (C quick):** FILTER ATTACK 127 -> 119 (5.3 s), AMP ATTACK 96 -> 90. 10 % / 90 % of the climb at 0.8 s / 4.1 s: it opens in the time of a chord change, and has climbed 3.1 octaves (it ends brighter, 2020 Hz, because more of the envelope has run by the plateau).
2. **top of the swell (D blare):** CUTOFF 40 -> 50, ENV AMT 118 -> 127, RESO 14 -> 22, filter DRIVE 0 -> 40: 3925 Hz at the top (4.1 octaves), harsher at the peak; the filter DRIVE costs 61 host instr/sample on (b) (874 against 813).

## For Vincent's ears (questions)

* B's **first 3 seconds**: is a long dark nothing before it opens acceptable, or should it already be brass at the start (C is the 5 s version; a brighter start needs a different envelope shape than the engine has)?
* **Dry or a spring?** The original had one. DRAIN is a live macro; a bit of spring on the wall would add depth (its input is high-passed at 150 Hz, which is fine for brass).
* **Does the stack beat too fast or too slowly** (1 Hz at A2, +-10 cents)? DETUNE is the knob; VINTAGE 45 only.
* Is **A2 the right register** to judge a brass wall (phrase f2), or should 21 also be heard at A1 / A3?

## Round count

1 silent measured round, 0 listening rounds.
