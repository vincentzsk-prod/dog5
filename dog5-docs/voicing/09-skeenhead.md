# Voicing log — 09 "Skeenhead" (FACTORY[8], Batch 2A, the reggae off-beat stab)

Nov 2026. Brief (Batch 2A, "weight and space"): *the reggae off-beat stab. Tight plucky square, a resonant filter plop, drenched in spring. The spring chirp is the sound.* An MS-20 plop into a
Fender-style spring tank (SH-101 tightness, Prodigy rawness, a Space-Echo dub warmth in the tail). Method and kit: `README.md` here (§1 phrases, §3 loudness, §10 Batch 2A). Listening files (on the
`listen/batch-02a-weight-and-space` branch only): `listen/voicing/batch-02a/09-skeenhead/`; the approved variant's renders are in `reference-renders/`; `README.md` and `numbers.md` there are the full tables and are on the voicing branch too.

**Status: APPROVED AS IS (Vincent, after listening to round 2): variant E (the body fix alone, spring unchanged), committed in this step** (H was committed first; the tree now holds E). "Hits the mark." B (round 1) and F, G, H (round 2) stay render-only. **Final round count: 2 listening + 2 silent measured rounds.** Voice card: `cards/09-skeenhead.md`.

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
| 61 | SPRING PRE-DLY | **4** | 20 | 1.1 ms (the 0..127 knob spans 0..35 ms; this log first said 4 ms, which was wrong): the chirp starts at once |
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


---
# ROUND 2 (after Vincent's listening to Batch 2A)

His feedback (synth-talk): *"Sounds awful, very dull, very little body to the actual note. I like the effects and what comes after the note is struck, but the note itself almost completely disappears: far away, at the bottom of a well, distant,
completely separate from the effects it triggers. I like the sound and tone of the effects of option B, but B can be made slightly cleaner: something that would cut through cleanly on a reggae track. Definition with the effects, but not soaked. Good tone on the effects, but dial the effects back slightly. More tight, more stable."*

## DIAGNOSIS (done before any change; `tests/voicing/diag09.py`, run on the committed B)

The stab at 7250 ms (A minor dyad A3 C4, gate 110 ms, after the 1.4 s gap so nothing else is sounding in front of it); effects off for the dry note, fx = wet - dry for the spring.

```
== 1. THE DRY NOTE (effects off), the stab at 7250 ms after the gap (A3 C4, gate 110 ms), windows after note-on
window ms | level dBFS | centroid Hz | band % <60/60-150/150-400/400-1.2k/1.2k+
  0- 20 |   -13.3 |    641 | 0 / 0 / 94 / 6 / 1
 20-100 |   -24.3 |    314 | 0 / 0 / 100 / 0 / 0
100-250 |   -43.5 |    508 | 1 / 7 / 91 / 1 / 0
   (the voice has a 4 ms release and the gate is 110 ms: the 100-250 window holds 10 ms of note and 140 ms of silence)

== 1b. the filter over the body: dry level and centroid every 10 ms from the note-on
t ms:     0    10    20    30    40    50    60    70    80    90   100   110
dB:   -12.3 -14.7 -20.5 -18.8 -29.5 -25.0 -30.1 -30.4 -28.6 -35.4 -31.7 -73.1
Hz:     884   393   323   287   415   306   367   336   338   433   417  3342

== 1c. the filter trajectory (engine formula; this dyad: key track -1.2 st; FILTER DECAY 56 = 39 ms to the 5 % point, tau ~ 13 ms)
the notes: A3 220 Hz + C4 262 Hz
t ms:      0      5     10     20     30     40     60     80    110
Hz:    14005   3121   1119    344    198    153    128    124    122

== 2. THE SPRING RETURN against the dry note, per window after the note-on of the same stab (dB, fx = wet - dry)
window ms | dry dB | spring dB | spring re dry | spring centroid Hz | dry centroid Hz
   0-  20 |   -13.3 |   -36.2 |   -22.9 |   2299 |    641
  20- 100 |   -24.3 |   -23.5 |    +0.8 |   1429 |    314
 100- 250 |   -43.5 |   -27.8 |   +15.7 |   1198 |    508
 250- 500 |   -59.9 |   -38.2 |   +21.7 |   1105 |      0
 500-1000 |   -25.9 |   -29.3 |    -3.4 |   1357 |    861
over all the stabs' note-on regions: spring re dry -4.2 dB (the table's -4.2); PRE-DLY 4 -> 1.1 ms

== 3. TIMING (4 ms envelopes, ms re the note-on)
dry peak at 7 ms (-11.2 dB); spring first within 30 dB of its peak at 1 ms, within 10 dB at 21 ms, peak at 44 ms (-19.6 dB)
spring peak re dry peak -8.3 dB; the dry note ends at 110 ms, the spring is -22.2 dB at 110 ms, -34.5 at 300 ms

== 4. SPECTRAL GAP (the first 250 ms of the stab): share of energy above 400 Hz, dry note vs spring return
dry 0.1 %   spring 19.5 %

== 5. BODY of the dry note: the committed note against variants of it (effects off), windows 0-20 / 20-100 ms level and share above 400 Hz
B (committed)                              0-20:  -13.3 dB   6.4 % | 20-100:  -24.3 dB   0.1 %
OSC 2 pulse on (same pitch, LEVEL 100)     0-20:  -10.3 dB   1.6 % | 20-100:  -23.6 dB   0.1 %
CUTOFF floor +12 (52)                      0-20:  -13.3 dB  10.3 % | 20-100:  -19.7 dB   0.5 %
FILTER SUSTAIN 40                          0-20:  -13.2 dB  11.5 % | 20-100:  -19.4 dB   7.9 %
no filter envelope (ENV AMT centre)        0-20:  -13.1 dB   1.1 % | 20-100:  -19.3 dB   1.4 %
the ORIGINAL (two narrow pulses), dry      0-20:  -26.1 dB  24.3 % | 20-100:  -40.9 dB  10.1 %
```

**Verdicts on the four hypotheses (and one more):**

1. **The body disappears once the filter plop has closed: CONFIRMED.** FILTER DECAY 56 is a ~13 ms time constant on an envelope that starts ~80 semitones above the base: the cutoff is 14 kHz at 0 ms, 1.1 kHz at 10 ms, **344 Hz at 20 ms, 198 Hz at 30 ms**, and rests at ~122 Hz.
   The notes are 220 and 262 Hz, so from about 25 ms the low-pass (RESO 62, a 12 dB slope) sits **under the notes**. Dry level: -13.3 dBFS in the first 20 ms, **-24.3 dB for 20-100 ms**, then a hum (-30 ... -35 dB at 60-100 ms); the 20-100 ms window is **100 % in 150-400 Hz, 0.1 % above 400 Hz**: a sine-like hum, no top. That is "the bottom of a well".
2. **A single square has too little body: NOT THE CAUSE.** Adding OSC 2 (a second pulse on the same pitch, full level) raises the first 20 ms by 3 dB and **the 20-100 ms body by 0.7 dB** (-23.6): both oscillators go through the same closed filter. The *original* two narrow pulses were 13 dB quieter (-26 / -41 dB) but brighter (24 % / 10 % above 400 Hz): more oscillators did not give it body, the filter does.
3. **The spring is too loud against the dry note: CONFIRMED, and the -4.2 dB hides it.** -4.2 dB is the average over the gated regions, which are dominated by the loud first 20 ms. Window by window the spring return against the dry note is **-22.9 dB (0-20 ms), +0.8 dB (20-100 ms), +15.7 dB (100-250 ms)**:
   from about 20 ms on the spring is as loud as the note, and after the gate it is the only thing sounding.
4. **The pre-delay makes the spring a separate event: REFUTED.** PRE-DLY 4 on the knob is **1.1 ms** (it spans 0-35 ms); the spring is within 30 dB of its peak at 1 ms. But the spring *builds*: its envelope peaks at **44 ms**, 37 ms after the dry peak (7 ms), when the dry note has already fallen about 11 dB. That build-up, not the pre-delay, is the "separate event".
5. **(mine) A spectral gap: CONFIRMED.** Above 400 Hz the spring return holds **19.5 %** of its energy against the dry note's **0.1 %** in its body (centroids 1429 Hz against 314 Hz in 20-100 ms): the ear gets a bright, wide wash and a dark hum under it and hears two objects.

**Best explanation:** the plop shuts the filter below the notes within ~25 ms, leaving a quiet (-11 dB from the first 20 ms), dark, harmonic-free hum; the spring is fed by the bright first 20 ms, blooms to its peak 37 ms after the note's, is as loud as the note by 20 ms and louder after,
and is 4.5 times brighter. So a bright wash with a hum underneath: distant, separate, at the bottom of a well. Fix the *note*: keep the filter above the notes' fundamentals through the gate (the floor and the sustain), so the body keeps harmonics and level (measured levers, dry,
20-100 ms: FILTER SUSTAIN 40: **-19.4 dB and 7.9 % above 400 Hz** against -24.3 / 0.1 %; CUTOFF +12: -19.7 dB; no filter envelope: -19.3 dB). Then bring the spring down so it is 7-11 dB under the note in the body.

## What I changed, and the variants (renders: `listen/voicing/batch-02a/round2/09-skeenhead/` on the listen branch; the full tables are in `README.md` / `numbers.md` there, on the voicing branch too)

* **Note body (the diagnosis' fix):** CUTOFF 40 -> 46 (+5 %, the floor), FILTER SUSTAIN 0 -> 40 (the filter rests above the notes' fundamentals instead of closing under them), AMP SUSTAIN 30 -> 64 (70 in H: the amp holds through the gate; the amp fell 16.7 dB inside it in B, 3.7 dB now).
  FILTER DECAY, RESO 62 and ENV AMT 118 are unchanged, so the plop sweep is the same (first 23 ms 1360 Hz against 657 Hz: x2.1, B x2.2).
* **Spring (same tone: DAMP 40 unchanged; DRAIN down, SIZE shorter, PRE-DLY toward 0):** F DRAIN 90 -> 77, SIZE 70 -> 62, PRE-DLY 4 -> 2; G DRAIN 56, SIZE 50, PRE-DLY 0; H DRAIN 66, SIZE 58, PRE-DLY 0.
* **Cleaner / tighter / stable (H only):** VINTAGE 30 -> 8, AMP RELEASE 28 -> 20 (4 -> 2 ms), AMP DECAY 70 -> 62, a second pulse an octave up (OSC 2 +12 st, LEVEL 50) for definition, filter DRIVE 0 -> 30. DETUNE is not in play (POLY, one note one voice).

| | B anchor | E body | F spring1 | G spring2 | H blend |
|---|---|---|---|---|---|
| VOLUME · peak (any phrase, b_stabs highest) | 115 · -4.4 | 92 · -6.3 | 93 · -7.5 | 96 · -7.0 | 96 · -6.7 |
| level (stabs, spring on) · dry stabs alone · phrase (b) | -18.2 · -19.6 · -18.7 | -17.9 · -19.0 · -17.4 | -18.1 · -18.8 · -17.8 | -17.9 · -18.3 · -17.7 | -18.0 · -18.4 · -17.4 |
| dry stab level dB 0-20 / 20-100 / 100-250 ms | -13.3 / -24.3 / -43.5 | -16.4 / -19.9 / -34.6 | -16.2 / -19.8 / -34.4 | -15.7 / -19.2 / -33.8 | -16.6 / -18.7 / -33.7 |
|   body fall: 20-100 re 0-20 (dB) | -11.0 | -3.5 | -3.5 | -3.5 | -2.0 |
| dry centroid Hz 0-20 / 20-100 / 100-250 | 641 / 314 / 508 | 1329 / 663 / 576 | 1329 / 663 / 575 | 1329 / 663 / 573 | 1573 / 655 / 632 |
| dry share above 400 Hz % 0-20 / 20-100 / 100-250 | 6.4 / 0.1 / 1.4 | 11.8 / 13.1 / 5.7 | 11.8 / 13.1 / 5.7 | 11.8 / 13.1 / 5.7 | 37.6 / 14.3 / 23.9 |
| dry band split 20-100 ms % <60/60-150/150-400/400-1.2k/1.2k+ | 0 / 0 / 100 / 0 / 0 | 0 / 0 / 87 / 12 / 1 | 0 / 0 / 87 / 12 / 1 | 0 / 0 / 87 / 12 / 1 | 0 / 0 / 86 / 13 / 1 |
| plop: centroid first 23 ms → next 67 ms | 689→318 (×2.2) | 1360→657 (×2.1) | 1359→656 (×2.1) | 1359→655 (×2.1) | 1350→644 (×2.1) |
| amp fall inside the gate (dB) | 16.7 | 3.7 | 3.7 | 3.7 | 2.9 |
| spring re dry, stab regions (B's definition) dB | -4.2 | -6.1 | -7.6 | -10.6 | -9.0 |
| spring re dry per window 0-20 / 20-100 / 100-250 dB | -22.9 / +0.8 / +15.7 | -21.7 / -5.9 / +5.9 | -22.4 / -7.3 / +3.9 | -24.5 / -10.3 / +0.0 | -21.4 / -8.8 / +3.0 |
| gap between stabs re stab (dB) | -18.3 | -16.3 | -18.7 | -23.1 | -20.2 |
| tail to -20/-40/-60 dB (ms) | 318/704/994 | 466/840/1072 | 338/686/934 | 242/524/742 | 270/608/858 |
| worst-case CPU | 1171 | 1172 | 1172 | 1172 | 1254 |

**Level and the peak limit:** B was held at -4.4 dBFS by the -4 peak limit (the crest of its plucked stab, on the stabs phrase). The new variants have a much lower crest (the amp holds): the peaks are -6.3 ... -7.5 dBFS, so **the trim is set by the level reference, not by the peak**, and VOLUME comes down 115 -> 92-96.
**The plop is as recognisable by tone** (x2.1) **but is less of a "pop" in level:** the first 20 ms is now only 2-3.5 dB above the body (B: 11 dB); the dry stab's very first moment is quieter against the rest.
**The spring** (B's definition, energy over the stabs' note-on regions): -4.2 dB -> E -6.1 (spring unchanged, the note got louder), F -7.6, G -10.6, H -9.0; per window H is -21.4 / **-8.8** / +3.0 dB (B -22.9 / +0.8 / +15.7): under the note while the note sounds (20-100 ms),
level with it just after the gate. The spring's tail: B 0.99 s -> E 1.07, F 0.93, G 0.74, H 0.86 s to -60 dB. CPU: H 1254 worst case (the second oscillator and the drive, +83), the others 1172, B 1171.

## Recommendation: H

In the vocabulary: *punchy and tight, with a body that holds through the gate; resonant plop kept; definition from the octave-up pulse and a touch of DRIVE; steady (VINTAGE 8) and dry-stopped (2 ms release); the spring same tone, tight, under the note.* It is the one meant to
**cut through a reggae track**. Caveats from the numbers: H's first 20 ms is the brightest (37.6 % above 400 Hz: the octave-up pulse), which is edge, not warmth; if it is too edgy, E-to-G (no second pulse) are the same body without it. F is the mildest spring change, G the driest.

## For Vincent's ears (questions)

* **E against B_anchor:** is the note now a note (body in front of the spring)? If E is right the rest is the spring's amount.
* **How far down can the spring go** (F -7.6, H -9.0, G -10.6 dB re dry) before the chirp is lost?
* **H: definition or too much edge?** And is the plop still a plop with its pop softened (the first 20 ms 2 dB above the body)?

## Round count (09)
Round 1: 1 silent measured + 1 listening (rejected for the note). Round 2 so far: 1 silent measured (diagnosis + variants) + 0 listening.

## FINAL (approved): variant E

Committed over round 1's B: CUTOFF 40 -> 46, FILTER SUSTAIN 0 -> 40, AMP SUSTAIN 30 -> 64, VOLUME 115 -> 92 (35 steps of headroom); the spring is exactly B's (DRAIN 90, SIZE 70, DAMP 40, PRE-DLY 4 = 1.1 ms); VINTAGE stays at the default 30. Level -17.9 dBFS (stabs, spring on; dry stabs alone -19.0), phrase (b) -17.4, peak -6.3 dBFS (stabs phrase b), worst-case CPU 1172 host instr/sample (idle 589).
Spring re dry: -6.1 dB over the stabs' note-on regions; per window -21.7 / -5.9 / +5.9 dB (0-20 / 20-100 / 100-250 ms); tail -20 / -40 / -60 dB at 0.47 / 0.84 / 1.07 s. `check_slot.py 9 E round2`: resolved bytes identical, audio bit-identical when both are loaded from INIT (from the boot patch they differ 28-36 dB: the slew floor).
