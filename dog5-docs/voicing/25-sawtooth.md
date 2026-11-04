# Voicing log — 25 "SAWTOOTH" (FACTORY[24], Batch 1A, the iconic poly brass)

4 Nov 2026. Brief (Batch 1A, the attack set): *dual saws, slight detune, a classic 24 dB filter-envelope swell; stable, warm and brassy, related to but clearly distinct from 03 Half-Life.* A Prophet-5 brass swell, with OB-Xa brass, Jupiter-8 brightness, Memorymoog thickness and a hint of Polysix wobble. Rebuilt by ear: nothing from any factory data. Method and kit: `README.md` here (§1 phrases, §3 loudness, §7 lessons). Listening
files, the numbers and the variants table: `listen/voicing/batch-01a/25-sawtooth/` (`README.md` there is the full table).

**Status: AWAITING THE LISTENING ROUND (round 1).** Variant **B** is committed as the recommended starting point; A, C, D stay render-only.
No voice card yet (written after approval). **Round count so far: 1 silent measured round, 0 listening rounds.**

## 0. Before: where it stood

* **Current values (the full list over the defaults):** O2_FINE 71, CUTOFF 55, RESO 15, FENV_AMT 104, FA 55, FD 80, FS 45, AA 40, AR 55, LFO_RATE 75, LFO_DELAY 60, LFO_PITCH 20. Everything else default (POLY, OSC 1 / 2 SAW at 110 / 100, LP24, KEY TRK 64, no effects, no arp). Name `SAWTOOTH`.
* **What the nearest starting patch does.** `PF_POLY_BRASS` (this slot's alone) is already the brief: POLY, two saws 5.5 cents apart (FINE 71), a 24 dB filter at CUTOFF 55 with a +40 envelope
  (decay 378 ms to sustain 45), a fade-in vibrato (rate 2.2 Hz, depth ~±28 cents at the peak, LFO DELAY 60 ≈ 1.1 s so it only arrives on held notes). It reads **−17.5 dBFS** (the bank reference
  within 0.5 dB, peak −6.2), centroid 880 Hz, 44 % under 150 Hz. What it does *not* do is swell: its filter attack is 36 ms, so on a chord the brightness peaks at 12 ms (1501 Hz) and has gone by 100 ms
  (426 Hz in the body): a snap, not a swell.
* **The two axes I judged most uncertain.** (1) **The swell: how long the filter takes to open** (FA with AA) — brass lives in that time: C slows it. (2) **The bite: how bright and edgy**
  (CUTOFF, ENV AMT, RESO, and GROWL as the edge): D. Fixed in B–D: two saws, FINE 71, VINTAGE 30, POLY.
* **Control limits foreseen.** The swell is the *filter's* (the amp attack is a short 25 ms); there is no per-note unison in POLY, so "thickness" is the two oscillators only (DUAL would double the voices and
  the cost, and is Half-Life's territory); the 24 dB slope and the SEM morph are the filter choices; "warm" is a low cutoff and the 24 dB slope (a touch of GROWL measured as a −1.0 dB peak change and
  −7 Hz of centroid for +570 host instr/sample, so it is left to the live macro); the vibrato fade-in (LFO DELAY) is the engine's only note-age control; POLY 5 plays a three-note chord with the release tails
  of the previous one.

## Final parameter list (what the tree holds now)

`PF_SAWTOOTH` in `firmware/src/obv_patches.h`, over the defaults (everything not listed is the default). **Bold** = differs from before:

| byte | parameter | value | was | in its own units |
|---|---|---|---|---|
| 11 | O2_FINE | 71 | 71 | +5.5 cents |
| 12 | CUTOFF | **56** | 55 | 330 Hz |
| 13 | RESO | 15 | 15 |  |
| 14 | FENV_AMT | **100** | 104 |  |
| 20 | FA | **70** | 55 | 117 ms |
| 21 | FD | **85** | 80 | 378 ms |
| 22 | FS | **50** | 45 |  |
| 24 | AA | **50** | 40 | 25 ms |
| 27 | AR | 55 | 55 | 36 ms |
| 29 | LFO_RATE | 75 | 75 | 2.2 Hz |
| 30 | LFO_DELAY | 60 | 60 | 1116 ms |
| 32 | LFO_PITCH | 20 | 20 |  |
| 45 | VOLUME | **97** | 100 |  |

Resolved by `build/voicing/dump_patch 25`; the committed bytes equal variant B's list (checked) and render **bit-identically** to it on every phrase
(LFO phase pinned where an LFO runs).

## Level

Level phrase **(b) FIFTH-BASED STABS**: RMS **-18.0 dBFS** over the note-on region (K-weighted -18.5), VOLUME 97
(was 100). Bank reference −18.0 ±1.5. Read the bank's own way on phrase (b): **-18.0 dBFS** (difference +0.0 dB).
Peak, any phrase: **-6.9 dBFS** (limit −4). The original read -17.5 on its level phrase (-17.5 on (b)), peak -6.2.
Riff / stabs / held: -23.1 / -18.0 / -22.7.

## Character notes (what to expect, from the numbers)

* **The swell:** on the held A2 the brightness peaks at **1237 Hz after 84 ms** (the filter attack is 117 ms) and settles to 441 Hz; the original peaked at 1501 Hz at 12 ms.
  The amp attack is 25 ms and the level is within 3 dB of its body value from 4 ms (the swell adds up to +6 dB over the body), so the swell is mostly a brightness swell, which is what a Prophet-style brass does. C opens more slowly
  (peak 2086 Hz at 288 ms); a 180 ms stab on the chord phrase catches roughly its first half.
* **Stable and warm:** VINTAGE stays at 30 (wander s.d. 1.0 cents, card offset -2.4); the two saws sit +5.5 cents apart, beating at the pair's 0.35 Hz (110 Hz × 5.5 cents) (the measured 0.67 Hz is the analysis floor;
  the band's amplitude moves 18 dB p-p); the held body's level wobbles 2.4 dB s.d. (Half-Life: 4.8, its gate-chop). Centroid 881 Hz on the stabs, 43 % under 150 Hz.
* **Against 03 Half-Life** (pilot B, on phrase b): centroid 815 Hz, 51 % under 150 Hz, wander s.d. 2.9 / 4.4 cents, pair separation 22 cents, gate-chop flutter 4.8 dB s.d.
  SAWTOOTH B: 881 Hz, 43 %, 1.0 cents, 5.5 cents, 2.4 dB, and a one-voice-per-note POLY instead of a DUAL pair with a sub-octave. Related (both saw-based, both fifth-and-octave friendly)
  and distinct in exactly the ways the brief asks: stable against unstable, swelling against chopped.
* **Release:** 34 ms to −20 dB, 104 ms to −60 dB; step at the release -48 dBFS against -42 in the body: no click.
* Cost (host instr/sample, relative; **not a device number**: check the GLOBAL page's render time, budget 5800 µs, aim < 2900): worst case 748 (idle 104 + load 645), the original 748 (idle 104 + load 644). D (GROWL 28): 1343.

## The axes chosen, and why

1. **The swell (FA with AA, CUTOFF, ENV AMT)** — "brass" is how the note opens. B = FA 70 / AA 50 (117 ms filter attack, 25 ms amp), CUTOFF 56, ENV AMT 100; C = FA 84 / AA 64 (350 ms / 73 ms),
   CUTOFF 50, ENV AMT 112: a lazier, darker-to-brighter swell (centroid 479 Hz on the stabs, it hardly opens inside a 180 ms gate: use it for held notes).
2. **The bite (CUTOFF 70, ENV AMT 100, RESO 22, GROWL 28 + BIAS 30)** — D: 1354 Hz centroid (B 881), body 687 Hz (B 441); the only one that carries the GROWL cost.

Not varied but flagged uncertain: the vibrato (kept from the original: depth 20, rate 75, fade-in 60) and the FINE (71 = 5.5 cents).

## Rounds

* **Round 0 (silent, measured, not for ears):** no separate sweep — the nearest base is already near the brief, so the design came straight from reading the original: the swell is the missing piece (its snap at 12 ms), FA / AA were
  stretched until the brightness peak landed near 85 ms. Five renders measured GROWL 0 / 6 / 6 (BIAS 0) / 14 / 30 on the stabs (rms −17.87 / −17.90 / −17.90 / −17.94 / −18.04, peak −6.7 / −7.8 / −7.9 / −8.2 / −9.6,
  centroid 881 / 874 / 875 / 875 / 840 Hz): below ~14 it is a −1 dB compression and no tone, for +570 instr/sample, so B has none and D carries 28.
* **Round 1 (for ears)** — four variants A–D. Total so far: 1 silent + 0 listening. Budget: 1 more listening round.

## Surprises and things hard with existing controls

* **This patch needed the least change of the four**: B is the original with a slower, bigger swell (FA 55 → 70, AA 40 → 50, ENV AMT 104 → 100, FD 80 → 85, FS 45 → 50, CUTOFF 55 → 56) and a level trim of 3 steps.
* **The vibrato is ±28 cents at its peak** (LFO PITCH 20 → `20²/128` = 3, × 24 Q8 = 0.28 st) and arrives after ~1.1 s on held notes: kept as the "brass survivor" detail, but it is the one unstable thing in a patch meant to be stable. LFO PITCH 0 removes it.
* **GROWL at low settings is expensive and nearly inert** (above): the macro is live (FX held) if the player wants it.
* **A variant's audio is not bit-exact against its program-load render for every patch.** CUTOFF / RESO slew in with `x += (target − x) >> 6`, which stops
  up to 63/256 st short when it approaches from below, so the same patch lands a fraction of a semitone apart depending on the patch it came from; a DRAIN patch's
  spring state also starts at another moment. Variant A is therefore rendered through the base firmware's own program path (it *is* the shipping original); B–D (and the
  committed slot, whose audio matched variant B bit for bit here) run INIT + parameters. Measured error of the INIT path vs the program path for the originals: −27 … −43 dB.
* **GROWL leaves a constant DC offset after the note** (the 10 Hz DC blocker's integer rounding sticks: −44 … −53 dBFS, mono more than stacks). Inaudible, an engine trait
  (left alone, no engine changes); the release-time columns subtract it. In this batch only the variants with GROWL on (30 D, 04 C, 25 D) have it.

## Proofs (4 Nov)

* the original list over INIT vs the base firmware's own slot 25: error −42 dB on (b) (CUTOFF / RESO slew rounding, see above); variant A is rendered through the base program path;
* committed slot 25 == variant B: resolved bytes equal; audio bit-exact on a / b / c;
* PROOF_OTHERS
