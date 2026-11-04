# Voicing log — 30 "THE DØG" (FACTORY[29], Batch 1A, the signature patch)

4 Nov 2026. Brief (Batch 1A, the attack set): *every voice stacked on one note (unison), slight detune, filter wide open, low register, floor-shaking bass.* Minimoog-in-unison weight with a Taurus floor, SH-101 punch, a little MS-20 bite. Method and kit: `README.md` here (§1 phrases, §3 loudness, §7 lessons). Listening
files, the numbers and the variants table: `listen/voicing/batch-01a/30-the-dog/` (`README.md` there is the full table) (WAVs of the rejected variants were removed from main in e40f5d5; the approved variant's renders are in `reference-renders/`).

**Status: APPROVED (Vincent, 5 Nov 2026, after listening to round 2): variant H, exactly as committed.** No further changes to slot 30. A, C, D (round 1) and B, E, F, G (round 2) stay render-only in
`listen/voicing/batch-01a/30-the-dog/` and `.../round2/` (H is `round2/H_presence_*`). Round 1: Vincent kept B as the starting point (punch and slight dryness right; the stack and bottom end read thin; wanted it a bit wider
but clearly under C, a little brighter and warmer, driven a bit harder but not fuzzy, and "a LOT of presence"); round 2 answered that and H was approved.
**Final round count: 2 listening rounds + 2 silent measured rounds.** Voice card: `cards/30-the-dog.md`.

**Level note — not a precedent.** H deliberately sits at **−16.5 dBFS RMS** on its level phrase (+1.5 dB over the −18.0 bank reference, the top of the ±1.5 dB tolerance band; (b) reads −17.0), peak −7.3 dBFS
(limit −4), because this is the flagship and presence was the brief. Future batches should not treat the top of the band as a default: match to −18.0 unless a patch's brief, approved by Vincent, says otherwise.

## ROUND 2 (5 Nov)

### The brief, translated
Keep B's punch and dryness (hard limits: snap not lost, release to −60 dB ≲ 80 ms, no spring, no long tail). Fuller/thicker; slightly wider than B (14–16 cents, clearly under C's 23);
a very slight bit brighter and warmer; driven a bit harder but not fuzzy; flagship presence (allowed up to −16.5 dBFS RMS on the level phrase, peak ≤ −4, as a variant dimension).

### Final parameter list (what the tree holds now = variant H); bold = differs from round 1's B

| byte | parameter | value | was | in its own units |
|---|---|---|---|---|
| 2 | O1_LVL | **114** | 110 |  |
| 6 | O2_LVL | **94** | 100 |  |
| 7 | O2_SEMI | -12 st | -12 st |  |
| 12 | CUTOFF | **104** | 100 | 5274 Hz |
| 13 | RESO | 12 | 12 |  |
| 14 | FENV_AMT | **88** | 86 |  |
| 15 | KEYTRK | **60** | 64 |  |
| 17 | DRIVE | **100** | 0 |  |
| 20 | FA | 10 | 10 | 1 ms |
| 21 | FD | 58 | 58 | 46 ms |
| 22 | FS | **40** | 35 |  |
| 23 | FR | 50 | 50 | 25 ms |
| 24 | AA | 4 | 4 | 1 ms |
| 26 | AS | 127 | 127 |  |
| 27 | AR | 48 | 48 | 21 ms |
| 38 | MODE | UNISON | UNISON |  |
| 39 | UNI_N | 8 | 8 |  |
| 40 | UNI_DET | **35** | 28 | +-7.4 cents |
| 42 | VINTAGE | 40 | 40 |  |
| 43 | SPREAD | 50 | 50 |  |
| 45 | VOLUME | **56** | 65 |  |

### What I learned
* **B's band split** (phrase e, % of energy): <60 Hz 57.2 · 60–150 27.4 · 150–400 10.4 · 400–1.2k 3.9 · 1.2k+ 1.1.
  57 % is under 60 Hz, where small speakers and many PAs give nothing; the audible bottom is the 27 % in 60–150 and 10 % in 150–400. "Thin" is consistent with that, not with weak low-mids.
* **Body can't be had from balance.** At equal level no oscillator / filter / drive lever moved a band by more than about ±1.5 dB (O2 level 40–127, O2 at 0 / −7 / −12 st, saw+pulse, O1 up, KEY TRK 64 → 20, CUTOFF 100 → 112, ENV AMT, FS,
  DETUNE, per-voice DRIVE 30–127): the spectrum is saws. E's "fuller" is +0.7 dB above 1.2 kHz and nothing below. The things that change feel: **width** (inner motion of the 60–400 Hz band, s.d. 0.99 → 1.47 dB at 14.8 cents; C
  measured 1.65), **K-weighted level** (H), and **harmonic density** (drive). Side result, not used: O2 at 0 st instead of −12 (the sub becomes a second layer at the root) (tried inside an H-like blend: O2 SEMI 0, LEVEL 80, DRIVE 90, GROWL 22, −16.5) gives the steadiest snap (+2.8 whole-hold) and the cleanest
  harmonic structure (hash 1.4 %), but it removes the sub-octave that is the patch's brief; it is a candidate for round 3 if the ears want it.
* **At A0 the −12 st sub is 13.75 Hz and at A1 27.5 Hz**: inaudible weight that costs headroom. Worth hearing H against a version with the sub moved up; I did not change it (not asked).
* **Wider:** DETUNE 28 → 35 = 14.8 cents end to end (B 9.4, C 23.4), 2.1 cents between neighbours; VINTAGE unchanged (40), wander s.d. 1.2–1.9 cents, range −7 … +8 per card.
* **Drive routes, compared at equal level** (`round2/drive_routes.md`): per-voice DRIVE (FILTER+ knob 1) adds harmonic density with no compression (crest ~9.4 dB) and takes 1–2 dB off the top: warmth; +~100 instr/sample.
  GROWL is inert to ~28, then compresses (crest 8.3 at 40, 7.0 at 55, 5.5 at 70) and the inter-harmonic hash reaches fuzz (17 % at 70); +~595 always on. BIAS exists only inside GROWL and trades peak for even harmonics (crest 8.3 → 10.3, peak −8.7 → −6.1).
  **Presence without compression = DRIVE.** The edge of fuzzy, by my definition (hash 2× the undriven E, crest −2.5 dB), is G (DRIVE 110 + GROWL 55); GROWL 70 alone is past it. The ears decide where the edge really is.
* **Correction to round 1:** its "snap +4.0 dB" (peak against the last 110 ms of the held note) moves ±2 dB with the stack's beat phase. Whole-hold it is +0.5 dB for B; on the chopped roots +0.9. The punch is spectral (attack 1224 Hz → body 725). Round 2 reads three
  ways (table in the README) and requires only that no variant fall below B on the steadier two and on the brightness ratio: E, F, H do not; G does a little on the ratio. By the literal round-1 reading E–H read +1.5 … +2.5, i.e. under +3.
* **Presence** is one dimension only: H alone uses −16.5 dBFS (E, F, G are at −18.0); H's peak is −7.3 dBFS (all four phrases ≤ −7.3), K-weighted −19.5 (B −20.9).
* CPU (host, relative, device unmeasured): B / E 1616, F 1718, H 1705, G 2294 (the only variant with GROWL). Check the GLOBAL page.
* Release to −60 dB: 54–64 ms in every variant (H 56 ms), no spring, no delay, no tail.

### Rounds
* **Round 2, silent (5 Nov):** ~120 host renders: band-balance levers (O2/O1 level, O2 semitone and wave, KEY TRK, CUTOFF, ENV AMT, FS, DETUNE), the stack's motion against DETUNE / FINE / VINTAGE, the drive ladders (DRIVE 30–127, GROWL 12–70, BIAS 0–100, TONE 20–80),
  and E–H with the hard limits checked. New measures (`tests/voicing/dog_metrics.py`): 5-band split, odd/even harmonic energy, inter-harmonic hash, crest, inner motion, whole-hold and chopped snap.
* **Round 2, for ears:** five files per phrase. Budget: this is the flagship; further rounds as needed.

### Proofs (5 Nov)
* committed slot 30 == variant H: resolved bytes equal; audio bit-exact on a / b / c / e;
* the other 31 programs (including 31, 04 and 25 as committed in Batch 1A) byte-identical to the commit before this round: `python3 tests/voicing/identical.py build/voicing/base2 30` — **31 of 31 other slots byte-identical on all six phrases (a, b, c, stress chord, d, e), 31 of 32 patch hashes unchanged (only slot 30 differs)**;
* `tests/run_host.sh` passes.

---
# ROUND 1 RECORD (4 Nov; the values below are B, superseded by round 2's H)

## 0. Before: where it stood

* **Current values (the full list over the defaults):** O2_SEMI -12 st, CUTOFF 45, RESO 10, FENV_AMT 79, FA 100, AA 100, AR 110, LFO_RATE 25, LFO_FLT 20, MODE UNISON, UNI_N 8, UNI_DET 80, VINTAGE 80, SPREAD 127, REV_SIZE 120, REV_DAMP 80, REV_MIX 50. Everything else default (OSC 1 SAW 110, OSC 2 SAW 100, LP24, no GROWL, no BBD, no arp). Name `THE D\xD8G`.
* **What the nearest starting patch does.** `PF_DRONE_UNI`, shared with 18 Roto-scopo and 21 Cowl Shadow: an 8-voice UNISON *drone*. DETUNE 80 spreads the stack ±39 cents
  (78 cents end to end), VINTAGE 80, SPREAD 127, a 1.2 s filter and amp attack, a 2.6 s release, CUTOFF 45 with filter LFO and a big spring (DRAIN 50). Measured on the low-unison phrase:
  −14.9 dBFS RMS (peak **−2.8**, hot), 97 % of the energy under 150 Hz, centroid 102 Hz, 344 ms to come to level, and its release is still above −60 dB when the 0.9 s analysis window ends. It is a pad, the opposite of
  tight and punchy; only the 8-voice unison and the sub-octave saw carry over.
* **The two axes I judged most uncertain.** (1) **Width of the stack**: how fat versus how punchy (DETUNE × VINTAGE): C. (2) **Bite**: how open and how hard the filter and
  GROWL are, SH-101 clean versus MS-20 nasty: D. Fixed in all of B–D (decided in the silent round): a −12 st saw under the pair, an open filter with a filter-envelope snap,
  a fast attack and a short release.
* **Control limits foreseen.** UNISON is eight voices on *one* note, monophonic (the stack is the chord); the only sub is OSC 2 at −12 st (−24 st would be 13.75 Hz at A0, below what a PA
  reproduces); the DETUNE law is quadratic (`DETUNE²/64` Q8 st each side, so 28 is ±4.7 cents and one step near there is ~0.4 cents) with the voices spread evenly; SPREAD pans the
  stack (there is no mono-sum bass/treble split, so SPREAD stays modest); no velocity-to-detune; eight voices is the most CPU in this batch (device unmeasured), and GROWL adds ~580 host instr/sample that run even when nothing sounds.

## Final parameter list (what the tree holds now)

`PF_THE_DOG` in `firmware/src/obv_patches.h`, over the defaults (everything not listed is the default). **Bold** = differs from before:

| byte | parameter | value | was | in its own units |
|---|---|---|---|---|
| 7 | O2_SEMI | -12 st | -12 st |  |
| 12 | CUTOFF | **100** | 45 | 4186 Hz |
| 13 | RESO | **12** | 10 |  |
| 14 | FENV_AMT | **86** | 79 |  |
| 20 | FA | **10** | 100 | 1 ms |
| 21 | FD | **58** | 70 | 46 ms |
| 22 | FS | **35** | 40 |  |
| 23 | FR | **50** | 60 | 25 ms |
| 24 | AA | **4** | 100 | 1 ms |
| 26 | AS | **127** | 100 |  |
| 27 | AR | **48** | 110 | 21 ms |
| 29 | LFO_RATE | **70** | 25 | 1.7 Hz |
| 34 | LFO_FLT | **0** | 20 |  |
| 38 | MODE | UNISON | UNISON |  |
| 39 | UNI_N | 8 | 8 |  |
| 40 | UNI_DET | **28** | 80 | +-4.7 cents |
| 42 | VINTAGE | **40** | 80 |  |
| 43 | SPREAD | **50** | 127 |  |
| 45 | VOLUME | **65** | 100 |  |
| 59 | REV_SIZE | **80** | 120 |  |
| 60 | REV_DAMP | **60** | 80 |  |
| 62 | REV_MIX | **0** | 50 |  |

Resolved by `build/voicing/dump_patch 30`; the committed bytes equal variant B's list (checked) and render **bit-identically** to it on every phrase
(LFO phase pinned where an LFO runs).

## Level

Level phrase **(e) LOW UNISON (A0-A2 roots held and chopped)**: RMS **-17.9 dBFS** over the note-on region (K-weighted -20.9), VOLUME 65
(was 100). Bank reference −18.0 ±1.5. Read the bank's own way on phrase (b): **-18.4 dBFS** (difference -0.5 dB).
Peak, any phrase: **-6.2 dBFS** (limit −4). The original read -14.9 on its level phrase (-22.7 on (b)), peak -2.8.
Riff / stabs / held: -19.2 / -18.4 / -18.1.

## Character notes (what to expect, from the numbers)

* **Weight:** 85 % of the low-unison phrase's energy is under 150 Hz (the drone: 97 %), 41 % on the bank's stabs phrase; centroid 713 Hz
  (drone 102): the top is open, not a pure sub.
* **Stack and slop:** by the DETUNE law the eight voices spread over 9.4 cents (step 1.3); with VINTAGE 40 each card also sits
  a fixed few cents off and wanders (s.d. 1.2–1.9 cents), so the *wander* is the same size as the designed spread:
  it reads as one thick voice that breathes, not as eight distinct pitches. Measured beating is 0.42 Hz at that analysis's floor (it cannot tell B from C); C spreads 23.4 cents.
* **Attack and chop:** the filter envelope opens each note (1224 Hz in the first frames, 725 Hz in the body, +4.0 dB over the body); amp attack 0.7 ms; release 26 ms to −20 dB,
  62 ms to −60 dB — the chopped roots stop clean (no click: step -48 dBFS at the release against -27 in the body).
* **Headroom:** peak -6.2 dBFS with eight voices on VOLUME 65 (the drone peaked -2.8 at 100): room for GROWL / CHEW / a hot MASTER, and for the SLOBBER ride.
* Cost (host instr/sample, relative; **not a device number**: check the GLOBAL page's render time, budget 5800 µs, aim < 2900): worst case 1616 (idle 104 + load 1512), the original 2588 (idle 589 + load 1999).

## The axes chosen, and why

1. **Width (DETUNE with VINTAGE)** — "slight detune" is a matter of degree and the engine's law is quadratic. B = DETUNE 28 / VINTAGE 40 (≈ ±4.7 cents), C = 44 / 65 (±12 cents,
   wander s.d. 2.0–3.1 cents, snap down to +2.0 dB). B is the tight reading.
2. **Bite (CUTOFF with RESO and GROWL)** — D opens the filter all the way (CUTOFF 127), RESO 12 → 26, GROWL 0 → 42 (BIAS 20): centroid 1220 Hz, the biggest brightness of the four, same weight (low share 84 %).

Not varied but flagged uncertain: the sub's level (OSC 2 LEVEL 100 = OSC 1 at 110 minus 1.6 dB: the level knob is a square law), the filter-envelope snap (ENV AMT 86, decay 46 ms, sustain 35), SPREAD 50.

## Rounds

* **Round 0 (silent, measured, not for ears):** a sweep of about 20 host renders on the low-unison and riff phrases to fix the design: DETUNE 16–46 with VINTAGE 22–65; CUTOFF 95 / 110 / 127;
  GROWL 0 / 18 / 30 / 42 (measured on B afterwards); OSC 2 LEVEL 60 / 100 (60 loses 1.8 dB and 2 (phrase e) to 9 (riff) points of low share); UNISON 6 vs 8 voices (6 loses 1.7 dB). Findings that fixed the design: the stack at VOLUME 100 peaks near −3 dBFS
  (so VOLUME lands at 65); the filter envelope with a low sustain gives the snap; the drone's tail and spring are the first things to go. **GROWL 18 is inert here** (peak 0.25 dB lower, centroid +4 Hz) and costs ~580 host instr/sample always on, so B has none; GROWL 42 compresses (peak −1.6 dB) and darkens (centroid −78 Hz), which is why D's bite comes from the open filter and RESO, with GROWL as the optional edge.
* **Round 1 (for ears)** — four variants A–D. Total so far: 1 silent + 0 listening. Budget: 1 more listening round.

## Surprises and things hard with existing controls

* **Phrase (b) is the wrong test for this patch**: a unison plays only the top note of a chord; the level is read on (e) and (b) is in the table (-18.4 vs -17.9).
* **A variant's audio is not bit-exact against its program-load render for every patch.** CUTOFF / RESO slew in with `x += (target − x) >> 6`, which stops
  up to 63/256 st short when it approaches from below, so the same patch lands a fraction of a semitone apart depending on the patch it came from; a DRAIN patch's
  spring state also starts at another moment. Variant A is therefore rendered through the base firmware's own program path (it *is* the shipping original); B–D (and the
  committed slot, whose audio matched variant B bit for bit here) run INIT + parameters. Measured error of the INIT path vs the program path for the originals: −27 … −43 dB.
* **GROWL leaves a constant DC offset after the note** (the 10 Hz DC blocker's integer rounding sticks: −44 … −53 dBFS, mono more than stacks). Inaudible, an engine trait
  (left alone, no engine changes); the release-time columns subtract it. In this batch only the variants with GROWL on (30 D, 04 C, 25 D) have it.
* **18 Roto-scopo and 21 Cowl Shadow keep `PF_DRONE_UNI`**: THE DØG got its own array, so their bytes and renders are untouched (proved below).
* **GROWL's low settings are inaudible by the numbers and not free.** On this patch 0 / 18 / 30 / 42 read peak −8.6 / −8.3 / −9.1 / −10.2 dBFS and centroid 713 / 717 / 676 / 635 Hz (the clip's pre-low-pass closes as GROWL rises): it compresses and darkens rather than brightens. Whether D's 42 *sounds* nastier is for the ears.
* **No real sub-bass control.** The "floor" is OSC 2 at −12 st, and at A0 the fundamental is 27.5 Hz; most of the felt weight is the saw's lower harmonics. Nothing in the engine can add a true sub-octave sine.
* Phrase (e)'s level includes an A0 note whose fundamental sits below small speakers: the RMS counts it, the ears on a laptop will not hear it.

## Proofs (4 Nov)

* the original list over INIT vs the base firmware's own slot 30: error −27 dB on (b) — not bit-exact (see above; the spring is on); variant A is rendered through the base program path;
* committed slot 30 == variant B: resolved bytes equal; audio bit-exact on a / b / c / e;
* the other 28 programs byte-identical: `python3 tests/voicing/identical.py build/voicing/base 30,31,4,25` — 28 of 28 other slots render the same samples on all six phrases (a riff, b stabs, c held, the CPU stress chord, d lead, e low unison) with the firmware before (`git archive 8439b24`) and after, and the 28 other patches' 96-byte hashes are equal (`dump_patch all`); only `firmware/src/obv_patches.h` changed.
