# Voicing log — 03 "Half-Life" (FACTORY[2], P1, the flagship)

4 Nov 2026. Brief (presets §3): *unstable dual saws, heavy VINTAGE slop, VCA sputter on release; pure engine, FX macros
at 0.* Method and kit: `README.md` here. Listening files, numbers and the variants table: `listen/voicing/03-half-life/` (the WAVs were removed from main in e40f5d5 and the follow-up commit; the approved variant's renders are in `reference-renders/` only).

**Status: APPROVED AS IS (4 Nov 2026, Vincent, after listening to all six).** Variant B ("centre") is the committed patch,
no round-2 changes; A, C, D, E, F stay render-only in `listen/voicing/03-half-life/`. His answers to the three open questions:
the chop reads as a **sputter, not a tremolo**; the **sub-octave is exactly right**; **815 Hz is neither too bright nor too polite**.
**Final round count: 1 silent measured round + 1 listening round, approved as is.** Voice card: `cards/03-half-life.md`.

## Final parameter list (what the tree holds now)

`PF_HALF_LIFE` in `firmware/src/obv_patches.h` (its own array: `PF_DUAL_SAW`, the old base, is still **17 Titanic's** and
is untouched). Over the defaults, `*` = differs from the old Half-Life:

| byte | parameter | value | was | |
|---|---|---|---|---|
| 38 | MODE | DUAL | DUAL | two detuned voices per note |
| 40 | DETUNE | 60 | 60 | 22 cents between the pair (`60²/64` Q8) |
| 63 | POLY | **6** | 5 | the window: a 3-note stab = 6 cards, no stealing |
| 43 | SPREAD | 110 | 110 | the pair wide L/R |
| 42 | VINTAGE | **90** | 30 | wander s.d. ~4–5 cents, offsets −6/+3; ride on top → 344 of 381 |
| 4 | OSC2 WAVE | **SAW** | OFF | the sub-octave |
| 7 | OSC2 SEMI | **−12 st** | 0 | |
| 6 | OSC2 LEVEL | **80** | (100, off) | −5.5 dB under OSC1 (110) |
| 12 | CUTOFF | **76** | 70 | 740 -> 1047 Hz base (LP24, ENV AMT adds up to +32 st) |
| 13 | RESO | **30** | 20 | |
| 14 | ENV AMT | **96** | 90 | +32 around the centre |
| 27 | AMP RELEASE | **62** | 60 | 63 ms to −26 dB (the −60 dB point ≈ 160 ms) |
| 28 | LFO SHAPE | **SQUARE** | TRI | |
| 29 | LFO RATE | **119** | 70 | 20.1 Hz |
| 30 | LFO DELAY | **19** | 0 | 112 ms, then a 56 ms ramp |
| 35 | LFO -> AMP | **100** | 0 | dips of −13 dB at full depth |
| 45 | VOLUME | **112** | 100 | the bank reference, −18.0 dBFS RMS |

Everything else is the default: OSC1 SAW at 110, FILTER LP24, FILTER ENV A20 D70 S40 R60, AMP ENV A10 D70 S100, KEY TRK 64,
GROWL / ALLEY (BBD mix) / DRAIN / CHEW all 0 (so is the old delay MIX and the reverb MIX byte = DRAIN), no arp, no glide.
Resolved by `build/voicing/dump_patch 3`; the committed bytes equal variant B's list and render **bit-identically** to it
(LFO phase pinned: the LFO free-runs from the moment a program loads).

## Level

RMS −18.0 dBFS (phrase b, note-on region), peak −6.0 dBFS, K-weighted −18.7: the **bank reference** by definition
(README §5). Riff −21.2, held note −21.3 (a sparser, thinner signal than the stabs: normal).

## Character notes (what to expect, from the numbers)

* **Weight:** 51 % of the stab energy under 150 Hz (A 42 %), 80 % on the riff — the sub saw is the Moog-weight pole,
  with the top left open (centroid 815 Hz, A 569).
* **Slop:** the DUAL pair beats at about 2 Hz on A2 (1.4 Hz before), the cards' own offsets (−6.7 / +3.4 cents) lean it,
  and each card wanders ±15–20 cents over a couple of seconds. It reads as *seasick*, not as *dying*; "dying tape motor" is
  the SLOP ride's (patch 90 + ride: 16–17 cents s.d.). The patch leaves 3.8× of ride on top of itself.
* **Chop and sputter:** the original's smooth 150 ms release is now a stair — three dips and plateaus in about the same
  time — and the body of a 150–180 ms note is clean (the chop fades in after 112 ms, full by 168 ms). A held note starts to
  spit about a fifth of a second in (body flutter 4.8 dB s.d.): see "limits" below.
* **Attack:** unchanged (1.1 ms amp attack, the filter envelope's 20 ms snap): the thesis's hard edge stays.

## The axes chosen, and why

1. **stable ↔ unstable (VINTAGE with DETUNE)** — the brief's *heavy* is a matter of degree, and the engine's own slop law
   is gentle (the patch's VINTAGE tops out at a 6 cent s.d.). C = VINTAGE 127 / DETUNE 72, D = 55 / 48, B = 90 / 60.
2. **how hard the chop / how much it sputters (LFO -> AMP depth, rate, release length)** — the one thing with no clean
   existing control (below), so the most likely to be wrong. E = deeper, faster, longer-tailed, staggered, with filter
   bite; F = none.

Not varied but flagged uncertain, and common to B–F: the sub's level (LEVEL 80), the brightness (CUTOFF 76 / ENV AMT 96),
the sputter's shape and rate (SQUARE, 20 Hz).

## How "the VCA sputters on release" is done with existing controls (and what it cannot do)

The VCA takes the LFO (`LFO -> AMP`), and the LFO has a per-note **delay** that fades its effect in. SQUARE at ~20 Hz on AMP
with a DELAY of ~110 ms leaves a staccato note's body clean (a fixed −4 dB dip level) and chops it as it releases. What the
engine can't do: **there is no release-triggered modulation**, so the chop is "note age", not "the gate is closing" — a note
held longer than ~170 ms spits all the way through (until the key is let go and the tail dies), and a very short note
(< ~100 ms) catches only the first part of the ramp (the 120 ms test note still showed 38 dB of climb). Rejected on the way: **S&H and RANDOM** at 7–25 Hz (a random level per step: the
re-climbs in an exponentially falling tail were mostly under 5 dB and at best 14, it reads as a waver, not a sputter); a **longer release** alone
(smooth); **PHASE SPREAD with SQUARE** (E): per-voice phase offsets give a ragged left/right chop — kept as E's difference.
If the held-note spit is unwanted, the options with existing controls: raise LFO DELAY (the spit starts later, but so does
the tail's), or drop AMP (gentler dips); a true *sputter only on release* would need an engine change (an LFO or envelope
stage armed by the gate going off), which this round does not make.

## Rounds

* **Round 0 (silent, measured, not for ears):** three scripted sweeps of ~45 host renders to fix the design before
  rendering variants: the sub's level (OSC2 −12 st, LEVEL 60 / 80 / 100: low share 47 / 53 / 61 %, +0.5 / +1.2 / +2.4 dB, peak
  −5.3 / −4.3 / −3.4 at the same VOLUME; LEVEL 80 chosen); the sputter (SQUARE / S&H / RANDOM × rate 4–26 Hz × LFO DELAY 12 / 17 / 19 / 20 ×
  AMP 80–120 × release 56 / 62 / 68 × PHASE FREE / SPREAD, read on the 120 / 150 ms notes' tails: SQUARE gave a climb of 17–60 dB every note, S&H / RANDOM 0–14 dB, note to note unpredictable; DELAY 19 puts full depth at the 170 ms mark, just as the 150–180 ms notes let go; AR 62 keeps the tail at the
  original's length with the chop in it); the filter (CUTOFF 70 -> 76 -> 82, RESO 20 -> 30 -> 40, ENV AMT 90 -> 96 -> 100:
  centroid 531 / 669 / 888 / 917 Hz; 76 / 30 / 96 chosen ≈ 815).
* **Round 1 (for ears)** — six variants; B approved as is, so there was no round 2. Total: 1 silent + 1 listening.

For planning the other 31: the silent round was the cheap, useful one (the chop would have been built wrong without
it); each listening round is the slow one. Budget **1 silent + 2 listening rounds per patch**, 1 + 1 for the
patches whose character is a straight "nearest base" re-voice. The kit makes a round a one-command regeneration
(`python3 tests/voicing/half_life.py` is the template: a table of variants, trim to reference, measure, write).

## Surprises and things hard with existing controls

* **The engine's slop is gentler than the word.** VINTAGE 127 is a 6 cent s.d. wander; the ride is what makes it "dying".
  The brief's *heavy VINTAGE* is a 90 here on purpose (leaving the ride a 3.8× multiple). If the ears want it heavier, it's
  a patch value; if they want it *much* heavier, that's the ride (a live control), not the patch.
* **The slop ride adds up to 254, not 127** (CLAUDE.md §5: the shipped 2× depth); the sum is allowed to 381, so no patch
  VINTAGE value clips it.
* **`LFO DELAY` is not a delay of the LFO's own phase**: it scales every LFO destination toward the LFO's centre, so with
  AMP set the note sits at a fixed dip until the fade-in (−4 dB at AMP 100). Useful here; worth knowing for the other patches.
* **The three-note stab needs POLY 6 in DUAL** (6 cards), and the default window of 5 steals one voice from the first note
  of a fifth-and-octave chord: the old Half-Life played the stab with a hole (5 voices gated, not 6: checked on the pre-change build with `expect voices`). Any DUAL patch voiced on chords wants POLY ≥ 2 × notes.
* **The LFO free-runs per program load**, so a variant rendered via parameters over INIT differs from the program-load
  render in sputter *phase* only (not audible as a difference; the bit-exact proofs pin PHASE SYNC on both sides).
* **PF_DUAL_SAW is shared with 17 Titanic** (the slot map in `obv_patches.h`): Half-Life got its own array so Titanic's
  bytes and renders are untouched (proved).
* Cost (host, relative): +20 % instr/sample with a 4-note chord held (966 -> 1165; E 1195) — the sub saw doubles the
  oscillators, POLY 6 lets 6 voices run. Not a device number: check the GLOBAL page's render time (budget 5800 µs, aim < 2900).

## Proofs (4 Nov)

* the original list over INIT == the pre-change firmware's slot 3, **bit for bit on all three phrases** (`half_life.py` step 0);
* committed slot 3 == variant B: resolved bytes equal; audio bit-exact on all three phrases, LFO phase pinned;
* **the other 31 programs byte-identical**: `python3 tests/voicing/identical.py build/voicing/base 3` — 31 of 31 slots
  render the same samples on a/b/c with the firmware before (`git archive 31bf0a3`) and after, and the 96-byte patch hashes of
  those 31 match (`dump_patch all`); slot 3 alone differs;
* `tests/run_host.sh` passes (default script and the page/families/poly/spring/tape/bbd/map scripts), `obervave selftest` passes.

## Reproduce

```
git archive 31bf0a3 | tar -x -C build/voicing/base          # the pre-change firmware (once)
python3 tests/voicing/half_life.py                           # variants, level-match, measure, files, tree-vs-B check
python3 tests/voicing/identical.py build/voicing/base 3      # the other-31 proof
```
