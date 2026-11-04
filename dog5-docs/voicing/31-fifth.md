# Voicing log — 31 "Fi(l)fth" (FACTORY[30], Batch 1A, the aggressive chord stab)

4 Nov 2026. Brief (Batch 1A, the attack set): *the archetypal aggressive chord stab: OSC A + B a fifth apart (OSC 2 SEMI +7), fast decay, a short delay.* A Prophet-5 stab through a Space Echo, with Juno pluck and a little MS-20 bite. Method and kit: `README.md` here (§1 phrases, §3 loudness, §7 lessons). Listening
files, the numbers and the variants table: `listen/voicing/batch-01a/31-fifth/` (`README.md` there is the full table).

**Status: AWAITING THE LISTENING ROUND (round 1).** Variant **B** is committed as the recommended starting point; A, C, D stay render-only.
No voice card yet (written after approval). **Round count so far: 1 silent measured round, 0 listening rounds.**

## 0. Before: where it stood

* **Current values (the full list over the defaults):** O2_SEMI +7 st, CUTOFF 85, RESO 15, DRIVE 25, AA 2, AR 40, LFO_DELAY 60, LFO_PITCH 10, MODE MONO, GLIDE 15, DLY_FB 40, DLY_MIX 35, REV_MIX 20. Everything else default (OSC 1 / OSC 2 SAW at 110 / 100, LP24, no GROWL, no arp). Name `Fi(l)fth`.
* **What the nearest starting patch does.** `PF_FIFTHS_LEAD` (this slot's alone): a **MONO fifths lead**, last-note priority with 15 glide, a slow fade-in vibrato, DRIVE 25, a 2 ms
  attack, a dotted-eighth ping-pong echo (MIX 35, FEEDBK 40) and a little spring. On the chord phrase it plays only the top note of each chord, so it never was a *stab*: −21.4 dBFS RMS, peak −13.5,
  centroid 1106 Hz, 14 % under 150 Hz; its release with the echo and spring is still above −60 dB when the 1.2 s analysis window ends (the voice alone: 32 ms). Always-on cost 846 host
  instr/sample (the echo and spring running).
* **The two axes I judged most uncertain.** (1) **Body: one fifth-stacked voice per note (POLY) or a detuned pair per note (DUAL)** — fat versus clean, and twice the CPU: C. (2) **The slap: how long
  and how present** the short delay is — the thing that makes it a Space-Echo stab, and a matter of taste: D (89 ms → 149 ms). Fixed in B–D: the fifth in every voice, a filter-envelope pluck over an
  amp that rings on, DRIVE 20, no spring.
* **Control limits foreseen.** OSC A + B a fifth apart is OSC 2 SEMI +7 *inside every voice*, so a chord of fifths (phrase b) stacks fifths on fifths (E + B becomes E, B, B, F#: a sus2 cluster):
  correct, but judge chord body on single notes (the riff). "Fast decay" is the amp decay toward a sustain level plus the filter pluck; there is no hold or gate-length parameter, so a stab's
  length comes from the player's gate. A short delay with a fast attack is one global ALLEY line (no per-note delay); DUAL doubles the voices (a three-note chord = six) and its cost.

## Final parameter list (what the tree holds now)

`PF_FIFTH` in `firmware/src/obv_patches.h`, over the defaults (everything not listed is the default). **Bold** = differs from before:

| byte | parameter | value | was | in its own units |
|---|---|---|---|---|
| 7 | O2_SEMI | +7 st | +7 st |  |
| 11 | O2_FINE | **66** | 70 | +1.6 cents |
| 12 | CUTOFF | **92** | 85 | 2637 Hz |
| 13 | RESO | **22** | 15 |  |
| 14 | FENV_AMT | **106** | 90 |  |
| 17 | DRIVE | **20** | 25 |  |
| 20 | FA | **0** | 20 | 0 ms |
| 21 | FD | **52** | 70 | 29 ms |
| 22 | FS | **22** | 40 |  |
| 23 | FR | **50** | 60 | 25 ms |
| 24 | AA | **0** | 2 | 0 ms |
| 25 | AD | **72** | 70 | 137 ms |
| 26 | AS | **70** | 100 |  |
| 27 | AR | **52** | 40 | 29 ms |
| 30 | LFO_DELAY | **0** | 60 | 0 ms |
| 32 | LFO_PITCH | **0** | 10 |  |
| 38 | MODE | **POLY** | MONO |  |
| 41 | GLIDE | **0** | 15 |  |
| 42 | VINTAGE | **35** | 30 |  |
| 43 | SPREAD | **70** | 60 |  |
| 45 | VOLUME | **113** | 100 |  |
| 56 | DLY_FB | **28** | 40 |  |
| 57 | DLY_TONE | **55** | 70 |  |
| 58 | DLY_MIX | **36** | 35 |  |
| 62 | REV_MIX | **0** | 20 |  |
| 63 | POLY_N | **6** | 5 |  |
| 68 | ALLEY | **65** | 0 | 89 ms |
| 70 | BBD_SPREAD | **60** | 127 |  |

Resolved by `build/voicing/dump_patch 31`; the committed bytes equal variant B's list (checked) and render **bit-identically** to it on every phrase
(LFO phase pinned where an LFO runs).

## Level

Level phrase **(b) FIFTH-BASED STABS**: RMS **-18.1 dBFS** over the note-on region (K-weighted -18.3), VOLUME 113
(was 100). Bank reference −18.0 ±1.5. Read the bank's own way on phrase (b): **-18.1 dBFS** (difference +0.0 dB).
Peak, any phrase: **-6.0 dBFS** (limit −4). The original read -21.4 on its level phrase (-21.4 on (b)), peak -13.5.
Riff / stabs / held: -21.3 / -18.1 / -23.0.

## Character notes (what to expect, from the numbers)

* **The pluck:** the filter envelope opens each note (1850 Hz in the first frames) and settles to 912 Hz; the level snaps +6.8 dB over the body (the original +3.7), the amp
  attack is 0.5 ms and the amp decays to its sustain (70 of 127, −5 dB) over 137 ms, so a 180 ms stab has a body, not just a click.
* **Weight and brightness:** on the stabs 32 % of the energy is under 150 Hz (A: 14 %, because it played only the top note), centroid 1068 Hz (A 1106). Single notes read
  -3.3 dB against the chords (riff -21.3): one voice per note against three.
* **The slap:** 89 ms, FEEDBK 28, TONE 55 (darker than default), PINGPONG 60. With it the release reaches −20 dB at 54 ms and −60 dB at 288 ms; the voice alone: 30 / 72 ms. D's longer 149 ms
  echo takes 612 ms to −60 dB.
* **Detune and slop:** OSC 2 sits +1.6 cents above the equal-tempered fifth (FINE 66), which is within 0.4 cent of a pure 3:2 (701.96 cents), so the fifth locks and does not beat; VINTAGE 35, wander s.d. 1.1 cents. C's DUAL pair separates 7.8 cents: a visible beat (35 dB p-p depth).
* **Click check:** the voice alone's release step -38 dBFS against -29 in the body: no release click.
* Cost (host instr/sample, relative; **not a device number**: check the GLOBAL page's render time, budget 5800 µs, aim < 2900): worst case 1075 (idle 380 + load 695), the original 1053 (idle 846 + load 207). C (DUAL): 1765.

## The axes chosen, and why

1. **Body (POLY vs DUAL)** — "fat" is the Prophet's signature and the brief says punchy *and* fat. B is the single-pair reading; C stacks a detuned pair per note
   (DETUNE 36 ≈ 7.8 cents apart, POLY 8 so a three-note chord has its six voices), +8 points of low share, 1765 worst-case cost against 1075.
2. **The delay (ALLEY time, FEEDBK, MIX)** — "a short delay" can be a doubling (~60 ms) or a Space-Echo repeat (~150 ms). B = 89 ms / 28 / 36; D = 149 ms / 38 / 42 / TONE 50.

Not varied but flagged uncertain: the brightness (CUTOFF 92, ENV AMT 106: a pluck from the filter envelope), DRIVE 20, and the amp's body (AD 72 / AS 70).

## Rounds

* **Round 0 (silent, measured, not for ears):** about 16 host renders on stabs and riff to fix the design. The finding that shaped it: the first reading, a fast amp pluck (AD 62, AS 30), had a
  17.6 dB crest (−25.8 dBFS RMS with a −8.2 dBFS peak) and could not reach the −18 reference with VOLUME at 127; a stab that dies in the amp is a click with a ring. The amp therefore keeps a body (AS 90 /
  AD 80 read −17.8 but is a sustain, AS 55 −21.6, AS 70 −20.4) and the *pluck* lives in the filter envelope (decay 29 ms, sustain 22). Also: raising the oscillator levels gains 1.5 dB, DRIVE 45 gains 2.1 dB (rejected:
  oscillator levels and drive are tone), DUAL gains 3.6 dB, CUTOFF 68 / 78 / 90 read centroid 492 / 661 / 1004 Hz on the stabs (on the first, plucky amp; 92 chosen with the envelope behind it); slap 55 ms / FEEDBK 20 and echo 149 ms /
  FEEDBK 38 are within 0.1 dB of the dry level.
* **Round 1 (for ears)** — four variants A–D. Total so far: 1 silent + 0 listening. Budget: 1 more listening round.

## Surprises and things hard with existing controls

* **The brief's sound is a fifth-on-every-note patch, and the bank's chord phrase already holds fifths.** Phrase (b) therefore stacks them; the riff (single notes, A1–A2) is the honest
  test of chord body. Level is still read on (b), as for every patch.
* **The mono lead it replaces was not a stab in any way.** MONO plays one note, so the chord phrase read −21.4 dBFS because most of each chord is silent.
* **A variant's audio is not bit-exact against its program-load render for every patch.** CUTOFF / RESO slew in with `x += (target − x) >> 6`, which stops
  up to 63/256 st short when it approaches from below, so the same patch lands a fraction of a semitone apart depending on the patch it came from; a DRAIN patch's
  spring state also starts at another moment. Variant A is therefore rendered through the base firmware's own program path (it *is* the shipping original); B–D (and the
  committed slot, whose audio matched variant B bit for bit here) run INIT + parameters. Measured error of the INIT path vs the program path for the originals: −27 … −43 dB.
* **GROWL leaves a constant DC offset after the note** (the 10 Hz DC blocker's integer rounding sticks: −44 … −53 dBFS, mono more than stacks). Inaudible, an engine trait
  (left alone, no engine changes); the release-time columns subtract it. In this batch only the variants with GROWL on (30 D, 04 C, 25 D) have it.
* The original's dotted-eighth echo and spring made its always-on cost 846 host instr/sample; B's slap and no spring bring that to 380.

## Proofs (4 Nov)

* the original list over INIT vs the base firmware's own slot 31: error −40 dB on (b) (the spring); variant A is rendered through the base program path;
* committed slot 31 == variant B: resolved bytes equal; audio bit-exact on a / b / c;
* the other 28 programs byte-identical: `python3 tests/voicing/identical.py build/voicing/base 30,31,4,25` — 28 of 28 other slots render the same samples on all six phrases (a riff, b stabs, c held, the CPU stress chord, d lead, e low unison) with the firmware before (`git archive 8439b24`) and after, and the 28 other patches' 96-byte hashes are equal (`dump_patch all`); only `firmware/src/obv_patches.h` changed.
