> The audio files in this folder were removed from main in the housekeeping commits e40f5d5 (rejected variants) and the follow-up that removed the duplicates of the approved variant (B); they are in the git history. The approved variant's renders are in `reference-renders/` (`03-half-life_B_*.wav`). The only audio file left in this folder is the approved variant's `B_centre_held.wav` (a held-note render not copied to `reference-renders/`). They can be regenerated with the round script named in `dog5-docs/voicing/README.md` (some need the pre-change base tree). The README below is generated; it still lists the removed files.

# 03 Half-Life — voicing round 1 (render-only variants A–F; B is committed)

Slot 03, "Half-Life" — the flagship ("unstable dual saws, heavy slop, a VCA that sputters on release, pure engine").
Rendered from the firmware's own code on the host build; the numbers are measurements, not hearing. How the kit,
the phrases and the loudness reference work: `dog5-docs/voicing/README.md`. Voicing log (final list, character notes,
rounds): `dog5-docs/voicing/03-half-life.md`. Regenerate everything with `python3 tests/voicing/half_life.py`.

## The files

Each variant on each phrase: `<letter>_<tag>_riff.wav` (a: low chopped riff, 4 s), `_stabs.wav` (b: fifth-based stabs),
`_held.wav` (c: one 2.4 s note released, then a 120 ms and a 150 ms note). Start with **stabs**, A then B, then the
others; use **held** for the slop and the sputter, **riff** for weight and the chop. Every variant is level-matched to
the bank reference (−18.0 dBFS RMS on the stabs, ±0.05 dB; A is left as it was, +0.4 dB) so louder never decides.
`release.png` overlays the release tails (level against time after note-off, the 2.4 s note and the 150 ms note).

| letter | tag | what it is |
|---|---|---|
| **A** | original | the nearest-base patch as it stood: DUAL saws, OSC2 off, VINTAGE 30, smooth release |
| **B** | centre | **recommended, committed.** The brief read straight: a sub-octave saw under the DUAL pair (Moog weight under Mono/Poly instability), VINTAGE 90, a bit more bite, and the VCA gate-chopped by a 20 Hz square that fades in |
| **C** | unstable | axis 1 up: VINTAGE 127 (the knob's top), pair 22 → 32 cents |
| **D** | stable | axis 1 down: VINTAGE 55, pair 22 → 14 cents |
| **E** | hardspit | axis 2 up: deeper (AMP 125), faster (26 Hz), longer-tailed (AR 100 ms), staggered left/right (PHASE SPREAD), the filter spits with it |
| **F** | cleanchop | axis 2 down: no sputter at all; a hard, short, clean chop (AR 25 ms) |

**The two axes** (the ones I'm least sure of): **1 — stable ↔ unstable** (VINTAGE with DETUNE: how seasick the pair is; C/B/D);
**2 — how hard the chop is / how much the VCA sputters** (LFO→AMP depth, rate, tail length; E/B/F). Everything else is
*the same in B–F*: that includes the three things I did **not** vary but am not sure of either — the **sub's level**
(OSC2 saw −12 st at LEVEL 80), the **brightness** (CUTOFF 76, ENV AMT +32: centroid ~815 Hz against A's 569) and the
**sputter's rate/shape** (SQUARE at ~20 Hz; I could not make S&H / RANDOM read as sputter, see the log). If your first
word is "thin / dark / boomy / too tremolo", that is a round-2 move on those, not on the letters.

## What changed (echo rule; % = of the control's full range, native units where named)

**B over A** (the others are B plus the line shown):

- OSC2 WAVE OFF -> SAW · OSC2 SEMI +0 -> −12 st · OSC2 LEVEL 100 -> 80 (−16 %) — the sub-octave saw (OSC2 was off)
- CUTOFF 70 -> 76 (+5 %: 740 Hz -> 1047 Hz) · RESO 20 -> 30 (+8 %) · ENV AMT 90 -> 96 (+26 -> +32 around the centre, +5 %)
- VINTAGE 30 -> 90 (+47 %) — heavy slop, with room for the ride (90 + 254 = 344 of the engine's 381)
- POLY 5 -> 6 voices — the three-note stabs (6 DUAL cards) no longer steal one another
- AMP RELEASE 60 -> 62 (+2 %: 54 -> 63 ms to −26 dB)
- LFO SHAPE TRI -> SQUARE · LFO RATE 70 -> 119 (+39 %: 1.7 -> 20.1 Hz) · LFO AMP 0 -> 100 (+79 %: dips to −13 dB)
  · LFO DELAY 0 -> 19 (+15 %: 0 -> 112 ms, then a 56 ms ramp) — **the sputter**: the note's body is clean, the chop grows
  in just as a 150–180 ms note lets go
- VOLUME 100 -> 112 (+9 %) — level-match to −18.0 dBFS (+2.0 dB: B untrimmed read −20.0, the chop's dips and the fixed −4 dB the LFO delay leaves on the body cost more than the sub adds)
- unchanged: MODE DUAL, DETUNE 60 (22 cents), SPREAD 110, FX macros all 0 (GROWL, ALLEY, DRAIN, CHEW), FILTER LP24, FILTER ENV, amp ATTACK 10 (1.1 ms), SUSTAIN 100
- **C**: VINTAGE 90 -> 127 (+29 %) · DETUNE 60 -> 72 (+9 %: 22 -> 32 cents) · VOLUME 112 -> 111
- **D**: VINTAGE 90 -> 55 (−28 %) · DETUNE 60 -> 48 (−9 %: 22 -> 14 cents) · VOLUME 112 -> 111
- **E**: LFO AMP 100 -> 125 (+20 %) · LFO RATE 119 -> 124 (+4 %: 20.1 -> 25.8 Hz) · AMP RELEASE 62 -> 68 (+5 %: 63 -> 100 ms) · LFO PHASE FREE -> SPREAD (each voice chops at its own phase, so the pair chops left against right) · LFO FILTER 0 -> 40 (+31 %) · VOLUME 112 -> 118
- **F**: LFO back to the original (TRI, 1.7 Hz, AMP 0, DELAY 0) · AMP RELEASE 62 -> 50 (−9 %: 63 -> 25 ms) · VOLUME 112 -> 88

## The numbers

| | **A** original | **B** centre | **C** unstable | **D** stable | **E** hardspit | **F** cleanchop |
|---|---|---|---|---|---|---|
| VOLUME (trim) | 100 | 112 | 111 | 111 | 118 | 88 |
| RMS (b, note-on) dBFS | -17.6 | -18.0 | -18.0 | -18.0 | -18.0 | -18.0 |
| vs reference −18.0 | +0.4 | +0.0 | +0.0 | +0.0 | -0.0 | +0.0 |
| K-weighted RMS (b) | -18.1 | -18.7 | -18.6 | -18.6 | -18.7 | -18.7 |
| peak (b) dBFS | -6.6 | -6.0 | -6.8 | -5.5 | -6.0 | -6.8 |
| RMS riff (a) / held (c) | -20.6 / -21.2 | -21.2 / -21.3 | -21.6 / -21.4 | -21.4 / -21.5 | -22.1 / -20.7 | -21.6 / -22.4 |
| peak riff / held | -12.1 / -12.6 | -11.4 / -9.5 | -11.5 / -9.3 | -11.4 / -9.8 | -10.9 / -8.6 | -12.1 / -12.4 |
| centroid Hz (b stabs) | 569 | 815 | 803 | 823 | 851 | 827 |
| centroid Hz (a riff) | 384 | 548 | 565 | 538 | 553 | 565 |
| low share < 150 Hz (b / a) | 42% / 76% | 51% / 80% | 48% / 79% | 35% / 79% | 46% / 80% | 48% / 79% |
| pair detune, DETUNE law (cents) | 21.9 | 21.9 | 31.6 | 14.1 | 21.9 | 21.9 |
| beat at A2 (Hz, mean [min–max]) | 1.40 [1.18–1.51] | 1.96 [1.68–2.19] | 2.75 [2.52–2.86] | 1.23 [1.18–1.35] | 1.96 [1.68–2.19] | 1.96 [1.68–2.19] |
| beat depth (dB p-p) | 39 | 27 | 23 | 32 | 25 | 23 |
| card offsets, static (cents) | -2.4 / +0.8 | -6.7 / +3.4 | -8.9 / +4.8 | -4.1 / +2.1 | -6.7 / +3.4 | -6.7 / +3.4 |
| wander sd (cents, per card) | 1.0 / 1.5 | 2.9 / 4.4 | 4.0 / 6.2 | 1.8 / 2.7 | 2.9 / 4.4 | 2.9 / 4.4 |
| wander range (cents, per card) | -5..+1 / -4..+5 | -15..+3 / -9..+17 | -20..+4 / -13..+23 | -9..+2 / -6..+10 | -15..+3 / -9..+17 | -15..+3 / -9..+17 |
| release 2.4 s note: −20 / −40 / −60 dB (ms) | 46 / 84 / 150 | 30 / 74 / 158 | 28 / 70 / 158 | 28 / 80 / 160 | 14 / 52 / 234 | 26 / 44 / 72 |
| sputter 2.4 s note: climb dB · re-rises · span ms | 0 · 0 · 0 | 24 · 3 · 32 | 20 · 2 · 34 | 20 · 2 · 24 | 141 · 6 · 108 | 2 · 0 · 0 |
| release 150 ms note: −20 / −40 / −60 dB (ms) | 54 / 96 / 134 | 64 / 114 / 162 | 64 / 114 / 188 | 64 / 114 / 170 | 46 / 84 / 266 | 30 / 52 / 80 |
| sputter 150 ms note: climb dB · re-rises · span ms | 0 · 0 · 0 | 38 · 3 · 0 | 40 · 3 · 0 | 27 · 3 · 0 | 166 · 7 · 106 | 1 · 0 · 0 |
| largest sample step dBFS (riff / stabs / held) | -21 / -18 / -19 | -18 / -14 / -16 | -18 / -15 / -16 | -18 / -14 / -16 | -18 / -16 / -16 | -17 / -16 / -16 |
| clipped samples (all phrases) | 0 | 0 | 0 | 0 | 0 | 0 |
| body flutter (s.d. dB, held A2) | 1.1 | 4.8 | 4.8 | 4.8 | 4.2 | 0.7 |
| cost: host instr/sample, phrase (b) | 378 | 427 | 428 | 427 | 515 | 334 |
| cost under load (4 notes, 8 cards wanted) | 966 | 1165 | 1165 | 1165 | 1195 | 1139 |


Reading the columns: definitions in `dog5-docs/voicing/README.md` §4. "climb" is the sputter index (total upward travel of the
tail's level, dB: 0 = smooth); "re-rises" counts climbs of ≥ 6 dB out of a dip. Cost is host instructions per sample
(a *relative* yardstick, not the device's microseconds: the render time on the GLOBAL page is the real check).

## What the numbers say, in vocabulary terms

* **fat / thick.** Below 150 Hz: 51 % of the stab energy in B against A's 42 % (riff: 80 % against 76 %): the sub saw
  gives the *thick* without a *murky* top (the centroid rises, 569 -> 815 Hz). It also costs peak headroom, so B ends
  −6.0 dBFS peak at −18.0 RMS (A: −6.6 at −17.6).
* **slop / seasick.** B's two voices beat at 2.0 Hz on A2 (A: 1.4 Hz; the card offsets add to DETUNE's 22 cents) and
  wander ±15–20 cents over a 2.4 s note (A: ±5). *Seasick*, not *dying tape motor*: the patch's own VINTAGE tops out at a
  6 cent s.d. (C), the *dying* territory is the SLOP ride's (B + ride = 16–17 cents s.d., ±60–80 range).
* **choppy / gated / sputter.** The 2.4 s note falls to −60 dB in 158 ms (A: 150) but as a stair: three dips and plateaus
  (24 dB of re-climbing), not the original's smooth slide. F is the *stone-dead* end (−60 dB at 72 ms, no sputter); E the
  *spitting* end (tail ~265 ms, six re-rises). On the 150 ms note B's tail is 162 ms and three chops.
* **a limit I'd rather say out loud:** the engine has no release-triggered modulation. The sputter is an LFO chop that
  starts ~110 ms after a note starts, so a *held* note starts to spit after about a fifth of a second (body flutter 4.8 dB
  s.d. on the 2.4 s A2) — it isn't silent until the release. Short notes (the house dynamic) get what the brief wants:
  clean body, spitting tail.

## Recommendation

**B (centre)**, committed as slot 03. On every measurable count of the brief it lands in the middle of its own spread
and it is the only one that is both *thick* (sub saw) and *sputters inside the original's tail length*: A's sound,
fatter, brighter, drifting, with the release gone ragged rather than longer. C is B with the same character a notch
more seasick (the difference is small: the engine's slop law is gentle until the ride is on); D loses the "heavy slop"
of the brief; E overshoots *"chopped stone-dead"*; F is a good patch but not *this* patch. **Listen for:** is the chop
at 20 Hz a *sputter* or a *tremolo*? is the sub too much / too little? is 815 Hz too bright, too polite? Answer in those
terms and round 2 moves them.
