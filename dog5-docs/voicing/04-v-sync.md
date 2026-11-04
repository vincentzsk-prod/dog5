# Voicing log — 04 "V-Sync" (FACTORY[3], Batch 1A, the tearing sync lead)

4 Nov 2026. Brief (Batch 1A, the attack set): *tearing hard-sync lead: OSC 2 synced and swept by the filter envelope, alias-tolerant so it rips, fat enough to cut through a drum machine, dead-stop on release.* A Pro-One sync lead, with Prophet-5 fatness, ARP Odyssey nasal bite and Prodigy rawness. Method and kit: `README.md` here (§1 phrases, §3 loudness, §7 lessons). Listening
files, the numbers and the variants table: `listen/voicing/batch-01a/04-v-sync/` (`README.md` there is the full table).

**Status: APPROVED AS IS (Vincent, 5 Nov 2026, after listening to Batch 1A): variant **D (fat)**. D doubles the synced voice (UNISON, 2 voices, a few cents apart) for fatness. It is the committed patch; the other variants stay render-only in
`listen/voicing/batch-01a/04-v-sync/`. **Final round count: 1 listening round + 1 silent measured round.** Voice card: `cards/04-v-sync.md`.

### What the tree holds now (5 Nov): variant D, the fat sync lead (UNISON, 2 voices) — bold = differs from the round-1 B this log describes below

| byte | parameter | value | was | in its own units |
|---|---|---|---|---|
| 2 | O1_LVL | 80 | 80 |  |
| 6 | O2_LVL | 127 | 127 |  |
| 7 | O2_SEMI | +7 st | +7 st |  |
| 8 | SYNC | ON | ON |  |
| 10 | ENV_O2 | 112 | 112 | +18.3 st at the env peak |
| 12 | CUTOFF | 92 | 92 | 2637 Hz |
| 13 | RESO | 24 | 24 |  |
| 14 | FENV_AMT | 88 | 88 |  |
| 17 | DRIVE | 20 | 20 |  |
| 21 | FD | 78 | 78 | 219 ms |
| 22 | FS | 28 | 28 |  |
| 23 | FR | 30 | 30 | 5 ms |
| 24 | AA | 0 | 0 | 0 ms |
| 26 | AS | 127 | 127 |  |
| 27 | AR | 30 | 30 | 5 ms |
| 38 | MODE | **UNISON** | MONO |  |
| 39 | UNI_N | **2** | 4 |  |
| 40 | UNI_DET | **22** | 30 | +-2.7 cents |
| 41 | GLIDE | 20 | 20 |  |
| 45 | VOLUME | **91** | 107 |  |
| 55 | DLY_TIME | 1/16 | 1/16 |  |
| 56 | DLY_FB | 18 | 18 |  |
| 58 | DLY_MIX | 12 | 12 |  |

Level (lead phrase d): **-18.0 dBFS RMS** ((b) reads -17.7), peak -10.1, VOLUME 91. Worst-case CPU 790 host instr/sample (idle 381 + load 410; B was 587; device unmeasured).
Voice dead-stop alone: 20 ms to −60 dB. Proofs (5 Nov): the committed slot == variant D in resolved bytes and bit for bit in audio on a / b / c / d; the other programs byte-identical (see `README.md` §9).

---
# ROUND 1 RECORD (4 Nov; the values and numbers below describe B, the first committed reading, superseded by D)


## 0. Before: where it stood

* **Current values (the full list over the defaults):** O1_LVL 0, O2_LVL 120, O2_SEMI +7 st, SYNC ON, ENV_O2 104, CUTOFF 90, RESO 10, FENV_AMT 80, FD 80, FS 20, AA 2, AR 40, MODE MONO, GLIDE 20, DLY_FB 40, DLY_MIX 35, REV_SIZE 70, REV_MIX 22. Everything else default (LP24, AMP A10→2 D70 S100, no GROWL, no arp). Name `V-Sync`.
* **What the nearest starting patch does.** `PF_SYNC_LEAD`, shared with **20 Fire & Ice and 26 BSyncA**: MONO, OSC 1 *silent* (LEVEL 0, the sync master only), OSC 2 saw at LEVEL 120, +7 st, hard SYNC,
  the filter envelope sweeping OSC 2's pitch +15.2 st (ENV>O2 +40) over 256 ms to sustain 20, CUTOFF 90, RESO 10, 11 ms release, glide 20, and a washy dotted-eighth echo (MIX 35) and spring
  (DRAIN 22). Measured on the lead phrase: −23.1 dBFS RMS (peak -14.1), centroid 1511 Hz; the voice alone stops in 34 ms but with the echo and spring the release is
  still above −60 dB when the 1.2 s window ends. Always-on cost 845 host instr/sample (echo + spring).
* **The two axes I judged most uncertain.** (1) **How hard it rips**: the sweep's depth, speed and start interval, plus resonance and drive (ENV>O2, FD, OSC 2 SEMI, RESO, DRIVE/GROWL): C. (2) **How fat**: the
  master saw under the slave is already in B (LEVEL 50); a detuned unison pair of the whole synced voice is the other way to get fat (UNISON 2): D.
* **Control limits foreseen.** (a) The sync master is OSC 1 at the played pitch (no OSC 1 transpose), so the sync *ratio* comes only from OSC 2 SEMI, FINE and the envelope. (b) There is no anti-aliasing
  switch: both oscillators are polyBLEP'd, so "alias-tolerant" can only be met by letting the sweep, RESO and DRIVE/GROWL do the ripping. (c) **MONO and UNISON play legato without retriggering**: a
  note struck while another is held slides and does *not* restart the envelopes, so the rip fires on detached notes only (the lead phrase has both on purpose). (d) A "dead stop" is the VCA's: the delay and
  spring have no gate and ring on after it; the only fix is a smaller MIX. (e) A synced slave is quiet: B needs VOLUME 111, so master headroom above the patch is 1.2 dB.

## Final parameter list (what the tree holds now)

`PF_V_SYNC` in `firmware/src/obv_patches.h`, over the defaults (everything not listed is the default). **Bold** = differs from before:

| byte | parameter | value | was | in its own units |
|---|---|---|---|---|
| 2 | O1_LVL | **80** | 0 |  |
| 6 | O2_LVL | **127** | 120 |  |
| 7 | O2_SEMI | +7 st | +7 st |  |
| 8 | SYNC | ON | ON |  |
| 10 | ENV_O2 | **112** | 104 | +18.3 st at the env peak |
| 12 | CUTOFF | **92** | 90 | 2637 Hz |
| 13 | RESO | **24** | 10 |  |
| 14 | FENV_AMT | **88** | 80 |  |
| 17 | DRIVE | **20** | 0 |  |
| 21 | FD | **78** | 80 | 219 ms |
| 22 | FS | **28** | 20 |  |
| 23 | FR | **30** | 60 | 5 ms |
| 24 | AA | **0** | 2 | 0 ms |
| 26 | AS | **127** | 100 |  |
| 27 | AR | **30** | 40 | 5 ms |
| 38 | MODE | MONO | MONO |  |
| 41 | GLIDE | 20 | 20 |  |
| 45 | VOLUME | **107** | 100 |  |
| 55 | DLY_TIME | **1/16** | 1/8. |  |
| 56 | DLY_FB | **18** | 40 |  |
| 58 | DLY_MIX | **12** | 35 |  |
| 59 | REV_SIZE | **80** | 70 |  |
| 62 | REV_MIX | **0** | 22 |  |

Resolved by `build/voicing/dump_patch 4`; the committed bytes equal variant B's list (checked) and render **bit-identically** to it on every phrase
(LFO phase pinned where an LFO runs).

## Level

Level phrase **(d) LEAD (single notes A3-A4, legato and staccato)**: RMS **-18.0 dBFS** over the note-on region (K-weighted -17.1), VOLUME 107
(was 100). Bank reference −18.0 ±1.5. Read the bank's own way on phrase (b): **-18.0 dBFS** (difference +0.0 dB).
Peak, any phrase: **-11.4 dBFS** (limit −4). The original read -23.1 on its level phrase (-22.0 on (b)), peak -14.1.
Riff / stabs / held: -18.2 / -18.0 / -18.2.

## Character notes (what to expect, from the numbers)

* **The rip:** OSC 2 sweeps +18.3 st from the filter envelope (was +15.2), over 219 ms, settling +4.0 st above its rest pitch (sustain 28); RESO 10 → 24 and DRIVE 0 → 20 put edge on it.
  Brightness: centroid 2054 Hz on the lead phrase (the original 1511); 2430 Hz at the attack → 2152 Hz held. Measured honestly: a sync sweep changes
  the *spectral shape* more than the centroid, so the centroid barely moves through the note (snap only +0.4 dB) — the sweep is a thing for ears, not for this number.
* **Fat:** OSC 1's saw at LEVEL 80 (the level knob is a square law: -8.0 dB against OSC 2 at 127) puts the played fundamental under the synced slave; 1 % of the energy is under 150 Hz because the lead lives at A3–A4 (D, the pair: 2 %).
* **Dead stop:** the voice alone reaches −20 dB at 14 ms and −60 dB at 20 ms (was 18 / 34); the step at the release is -55 dBFS against -25 in the body:
  no click. With the 1/16 slap (MIX 12, FEEDBK 18) it takes 262 ms to −60 dB (was still above −60 at 1.2 s). `DLY_MIX 0` is the literal dead stop.
* **Glide 20** stays (a short slide between legato notes). In the legato run the sweep does not re-fire (above).
* **Cost:** Cost (host instr/sample, relative; **not a device number**: check the GLOBAL page's render time, budget 5800 µs, aim < 2900): worst case 587 (idle 381 + load 206), the original 1036 (idle 845 + load 190). C (GROWL 25 + DRIVE 40): 1181; D (two voices): 790. GROWL is an always-on stage: C's idle cost is 959.

## The axes chosen, and why

1. **The rip (sweep depth/speed, resonance, drive)** — the whole character; the brief says "rips" and the engine's levers are all at the sweep and the filter. B = ENV>O2 +48 (18 st), FD 219 ms, RESO 24, DRIVE 20.
   C = ENV>O2 +63 (24 st), OSC 2 +12 st instead of +7, a faster 86 ms decay to a lower sustain (12), RESO 40, DRIVE 40, GROWL 25: a zap rather than a growl; centroid 1554 Hz (B 2054).
2. **Fat (the master saw, a unison pair)** — B already carries the saw under the slave (LEVEL 80); D is B in UNISON 2 voices, DETUNE 22 (≈ ±2.7 cents; beat 39 dB p-p), +1.3 dB of peak at the same RMS and
   790 worst-case cost against 587.

Not varied but flagged uncertain: the slave interval (+7 st, as the original), the saw's level (80), the slap (1/16, MIX 12), glide 20.

## Rounds

* **Round 0 (silent, measured, not for ears):** about 12 host renders on the lead phrase to fix the design: ENV>O2 96 / 112 / 127, OSC 2 SEMI 0 / +5 / +12, OSC 1 LEVEL 0 / 50 / 90 (at LEVEL 50 against OSC 2 at 127 the saw is 16 dB down and adds 0.4 dB: inaudible as "fat", so B uses 80 = 8 dB down), UNISON 2 and 3 voices, GROWL 40,
  FX on / off. They fixed two things: the level (an OSC 1 at 90 gains 1.3 dB; a two-voice stack gains 2.9 dB and three voices 4.9 dB, so the fat variants trim *down*) and the VOLUME ceiling (B at the first values
  needed VOLUME 122 of 127; OSC 2 LEVEL 110 → 127 brought it to 111, then 107 with OSC 1 raised). Then two quick table runs adjusted C (it was too close to B).
* **Round 1 (for ears)** — four variants A–D. Total so far: 1 silent + 0 listening. Budget: 1 more listening round.

## Surprises and things hard with existing controls

* **Legato does not re-fire the sweep.** MONO/UNISON slide into overlapped notes without retriggering envelopes (existing behaviour, `voice_trigger`); the lead phrase's legato run therefore
  rips once. To rip every note the player must detach them.
* **A sync lead is a bad fit for phrase (b)** (a mono voice playing the top note of each chord); the level is read on the lead phrase (d) and (b) is in the table (-18.0 vs -18.0).
* **The sweep does not show in the spectral centroid** (see above): the measurable parts are the sweep's range in semitones and the level, the audible part is the formant sliding.
* **A variant's audio is not bit-exact against its program-load render for every patch.** CUTOFF / RESO slew in with `x += (target − x) >> 6`, which stops
  up to 63/256 st short when it approaches from below, so the same patch lands a fraction of a semitone apart depending on the patch it came from; a DRAIN patch's
  spring state also starts at another moment. Variant A is therefore rendered through the base firmware's own program path (it *is* the shipping original); B–D (and the
  committed slot, whose audio matched variant B bit for bit here) run INIT + parameters. Measured error of the INIT path vs the program path for the originals: −27 … −43 dB.
* **GROWL leaves a constant DC offset after the note** (the 10 Hz DC blocker's integer rounding sticks: −44 … −53 dBFS, mono more than stacks). Inaudible, an engine trait
  (left alone, no engine changes); the release-time columns subtract it. In this batch only the variants with GROWL on (30 D, 04 C, 25 D) have it.
* **PF_SYNC_LEAD is shared with 20 Fire & Ice and 26 BSyncA**: V-Sync got its own array, so their bytes and renders are untouched (proved below).

## Proofs (4 Nov)

* the original list over INIT vs the base firmware's own slot 4: error −35 dB on (b) (the spring); variant A is rendered through the base program path;
* committed slot 4 == variant B: resolved bytes equal; audio bit-exact on a / b / c / d;
* the other 28 programs byte-identical: `python3 tests/voicing/identical.py build/voicing/base 30,31,4,25` — 28 of 28 other slots render the same samples on all six phrases (a riff, b stabs, c held, the CPU stress chord, d lead, e low unison) with the firmware before (`git archive 8439b24`) and after, and the 28 other patches' 96-byte hashes are equal (`dump_patch all`); only `firmware/src/obv_patches.h` changed.
