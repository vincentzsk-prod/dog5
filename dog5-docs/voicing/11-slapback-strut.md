# Voicing log — 11 "Slapback Strut" (FACTORY[10], Batch 2A, the percussive surf bass)

Nov 2026. Brief (Batch 2A, "weight and space"): *percussive surf bass. Single triangle, very fast decay, one loud ~80 ms free-time echo (ALLEY ~80 ms, FEEDBK low). This is why the delay runs in free ms.* A flatwound
Precision Bass into a Space Echo (SH-101 tightness, Minimoog round low end, a Fender-style spring for the surf wash). Method and kit: `README.md` here (§1 phrases, §3 loudness, §10 Batch 2A). Listening files (on the
`listen/batch-02a-weight-and-space` branch only): `listen/voicing/batch-02a/11-slapback-strut/`; the approved variant's renders are in `reference-renders/`; `README.md` and `numbers.md` there are the full tables and are on the voicing branch too.

**Status: APPROVED AS IS (Vincent, after listening to round 2): variant G (crisp), committed in this step** (H was committed first; the tree now holds G). "Hits the mark perfectly." B (round 1) and E, F, H (round 2) stay render-only. **Final round count: 2 listening + 2 silent measured rounds.** Voice card: `cards/11-slapback-strut.md`.

## 0. Before

* **Current values (the full list over the defaults):** MONO, OSC 1 PULSE (PW 50 %) at LEVEL 110, OSC 2 SAW **an octave below** (-12 st) at LEVEL 60, CUTOFF 35 (98 Hz base), RESO 10, LP24, ENV AMT 84, filter env DECAY 50 (25 ms) SUSTAIN 20,
  amp env ATTACK 1, DECAY 60 (54 ms) **SUSTAIN 100**, RELEASE 20 (2 ms), GLIDE 5. No echo, no spring. Name `Slapback Strut`.
* **What the nearest starting patch does.** `PF_SUB_BASS`, **shared with 05 ZEAROX and 19 Blackwater**, so 11 gets its own array `PF_SLAPBACK_STRUT` and `PF_SUB_BASS` is left alone for the other two. A dark mono sub: a pulse plus a saw an octave down through
  a 24 dB low-pass at 98 Hz, a sustained body. Measured on the surf riff: **-23.9 dBFS RMS**, (b) -29.6, peak -15.3, 100 % of the energy under 400 Hz (39 % under 60 Hz), harmonics 3 / 5 / 7 of the oscillator at -45 / -68 / -76 dB (a sine in effect: far duller than
  a triangle), the amp falls 9.6 dB inside the gate; no pluck, no echo.
* **The axes I judged most uncertain:** (1) **the pluck** (round against snappy: how far from a triangle toward a square, the filter envelope's depth) and (2) **the space** (a dry slap against the slap into a spring wash).
* **Control limits foreseen (and found):** **there is no triangle oscillator** (the nearest is a 50 % pulse through a tracking 12 dB low-pass; measured below); the fastest decay is limited by the level (see below); the echo's top MIX puts
  the first repeat at -6 dB under the dry note's peak (the BBD sends at half level); DRAIN on a bass is audible but its character is a low, short wash (probe below).

## Final parameter list (what the tree holds now = variant B)

`PF_SLAPBACK_STRUT` in `firmware/src/obv_patches.h` (its own array). Over the defaults; was = the original:

| byte | parameter | value | was | in its own units |
|---|---|---|---|---|
| 0 | OSC1 WAVE | PULSE | PULSE | a 50 % pulse, the nearest to a triangle |
| 2 | OSC1 LEVEL | **127** | 110 | +1.3 dB |
| 4 | OSC2 WAVE | **OFF** | SAW | a single oscillator |
| 6, 7 | OSC2 LEVEL / SEMI | default | 60 / -12 st | (inert with OSC 2 off) |
| 12 | CUTOFF | **63** | 35 | 494 Hz base; with KEY TRK 127 it sits ~1.7 x the note |
| 13 | RESO | **16** | 10 | |
| 14 | ENV AMT | **96** | 84 | +32 around the centre |
| 15 | KEY TRK | **127** | 64 | 100 % |
| 16 | FILTER TYPE | **LP12** | LP24 | |
| 21 | FILTER DECAY | **56** | 50 | 39 ms |
| 22 | FILTER SUSTAIN | **0** | 20 | |
| 24 | AMP ATTACK | **0** | 1 | 0.5 ms |
| 25 | AMP DECAY | **72** | 60 | 137 ms |
| 26 | AMP SUSTAIN | **0** | 100 | a pure pluck |
| 27 | AMP RELEASE | 24 | 20 | 3 ms |
| 38, 41 | MODE / GLIDE | MONO / 5 | MONO / 5 | unchanged |
| 45 | VOLUME | **122** | 100 | the bank reference, echo included |
| 56 | DLY FEEDBK | **12** | 50 | the second repeat is 29 dB under the first |
| 58 | DLY MIX (ALLEY's) | **127** | 0 | the top |
| 68 | **ALLEY** | **62** | 0 (SYNC) | **80.3 ms** |
| 70 | PINGPONG | **0** | 127 | the repeat sits in the middle (127: the first repeat left only) |

Everything else default (no GROWL / DRAIN / CHEW, no LFO, no arp). The committed bytes equal variant B's list (`tests/voicing/check_slot.py 11 B`: identical, bit-identical audio from the boot patch and from INIT).

## Level (how it is read, README §10)

**-18.0 dBFS RMS over the note-on region of the surf riff (phrase h), echo included where it falls inside a 100 ms gate**; the dry notes alone read -18.7 (so the echo adds 0.7 dB to the reading: it mostly falls after the gate and is measured on its own).
Phrase (b): -20.2 (difference -2.1), K-weighted -20.5; riff (a) -19.7, held A2 -27.5. **Peak -10.8 dBFS** (the limit is not close). **VOLUME 122 of 127 is the ceiling:** this patch is as loud as it can be at a 100 ms pluck.

## The decay against the level (the hard limit found)

A pluck that dies inside a short gate has a high crest, so its RMS over the note-on region is low, and VOLUME stops at 127. Sweeping AMP DECAY on B (AS 0), with O1 LEVEL 120 and CUTOFF 60 (before the final tuning), VOLUME 127 reached:
DECAY 60 (54 ms): **-22.2 dBFS** (41 dB of fall inside the gate); 66 (86 ms): **-20.2** (26 dB); 72 (137 ms): **-18.5** (17 dB); and with O1 LEVEL 127, CUTOFF 63 and VOLUME 122 the committed B reads -18.0 with a **16.5 dB fall inside the gate, 10 dB in 46 ms**.
So "very fast decay" is as fast as the level allows: a 10 dB fall in ~45 ms and 16.5 dB over the 100 ms gate. To go faster the level would sit 2-4 dB under the bank. The snap lives in the filter, not the amp.

## Character notes (what to expect, from the numbers)

* **The oscillator against a triangle:** harmonics 3 / 5 / 7 at rest sit at **-17 / -29 / -38 dB** (a triangle: -19 / -28 / -34; a square: -9.5 / -14 / -17): close up to the 5th, a touch rounder above. D (CUTOFF 70, ENV AMT 112, RESO 24, FILTER DECAY 52) brightens to
  -13 / -24 / -32: between the two.
* **The pluck:** the first 23 ms of an A2 are 359 Hz against 241 Hz for the next 67 ms (x1.5); D 526 -> 279 Hz (x1.9). It is a round note with a tap on it, not a clavinet.
* **The slap:** ALLEY 62 = 80.3 ms. The first repeat is a whole copy of the note (as long as the note) and peaks **-6.3 dB under the dry note's own peak**; the second repeat is **28.9 dB** under the first (FEEDBK 12: a single slap; FEEDBK 40 would put it ~17 dB under).
  The top of the MIX knob is the loudest a slap can be: the BBD sends at half level, so it cannot be louder than that against the dry note. The FX return over the whole riff is -6.2 dB re the dry notes, 36 % under 60 Hz, 52 % in 60-150 Hz. The echo is band-limited as a BBD's.
* **The tail:** the voice alone is dead at 20 ms (to -60 dB); with the slap, -20 / -40 / -60 dB at 92 / 142 / 192 ms: a note and its one echo, then silence.
* **Cost:** worst case 553 host instr/sample (idle 380, the BBD's always-on cost, + load 173); the original 300.
* **MONO:** a legato second key slides and does not re-fire the pluck (the envelopes do not retrigger): play it detached. GLIDE 5 is left as it was.

## What DRAIN does on a bass (probe, not a variant; B with the spring added)

The brief's note was that DRAIN does very little on a bass because of the 150 Hz high-pass ahead of the tank. **Measured, the high-pass is a one-pole (-9 dB at 55 Hz) and the spring is audible on this bass:**

| DRAIN | return re the dry signal | in 60-150 Hz re the dry's own | in 150-400 | in 400-1.2k | share of the return < 150 Hz |
|---|---|---|---|---|---|
| 30 | -15.7 dB | -16 dB | -15 dB | -13 dB | 77 % |
| 60 | -9.7 dB | -10 dB | -9 dB | -7 dB | 77 % |
| 100 | -5.3 dB | -5 dB | -5 dB | -2 dB | 77 % |

The return is mostly low because the dry note is (96 % under 150 Hz); relative to each band the upper partials ring slightly more than the fundamental (-7 dB against -10 dB at DRAIN 60). It is a short, dark wash, not a shimmer; I expect the chirp (a spring's top end) to be faint, because this bass has little above 1 kHz (untested by ear). C is B with DRAIN 60 / SIZE 80: tail to -60 dB at 1.05 s, level -18.0 (VOLUME 120), +466 host instr/sample (the spring's idle cost).

## The axes chosen, and why

1. **the space (C wash):** B + DRAIN 60, SIZE 80. The repeat is unchanged; behind it a wash that rings to -60 dB in 1.05 s (the FX return grows from -6.2 to -3.9 dB re the dry notes). The spring also rings the echo (they are in series).
2. **the pluck (D snap):** CUTOFF 63 -> 70, ENV AMT 96 -> 112, RESO 16 -> 24, FILTER DECAY 56 -> 52: x1.9 attack brightness, harmonics -13 / -24 / -32, the highest peak of the four (-9.8). A bit more bite, less round.

## For Vincent's ears (questions)

* **Is the slap loud enough?** It is at the knob's top (-6.3 dB re the note's peak). If it should be louder than that it needs an engine change (report only).
* **Round enough?** B's harmonics are a touch rounder than a triangle above the fifth; is that a flatwound or just dull? D against B.
* **Is the decay fast enough?** B is the fastest the level allows (16.5 dB over the gate); a faster pluck would sit ~2-4 dB under the bank.
* **C: does the wash help the surf sound or blur the slap?** And would the slap be better with ping-pong on (PINGPONG 127: the first repeat on the left only)?

## Round count

1 silent measured round, 0 listening rounds.


---
# ROUND 2 (after Vincent's listening to Batch 2A)

His feedback (synth-talk): *"A touch more warmth: the soft top without going dull, and a touch more brightness. The lower frequencies are dulling the slapback, and we need the slapback SUPER crisp and clear. So NO decay on any envelope, or at the very least minimal: just enough to give the note body, but not give it a tail. A slight bit more tight."*
Renders: `listen/voicing/batch-02a/round2/11-slapback-strut/` (listen branch; the full tables are in `README.md` / `numbers.md` there, on the voicing branch too). The base is the committed B; B is re-rendered as the anchor.

## Translation, and what I did

* **Warmth / brightness:** a little per-voice filter DRIVE (FILTER+ knob 1, not GROWL): 0 -> 30 / 40; CUTOFF up (E, F +5 % as asked; G +15 %, H +9 %, with KEY TRK lowered for H and G).
* **Crisp slapback:** the echo is a faithful copy of the note (its band split and the note's agree to a point), so *the crispness has to be in the note*. ALLEY's TONE does almost nothing here: TONE 70 -> 127 moved the echo's centroid by 1 Hz (the note has nothing near the TONE filter's range). What does move it:
  the note's harmonics (CUTOFF, KEY TRK 127 -> lower, DRIVE, a narrower pulse) and the removal of the sub (a narrower pulse takes 6-10 points off the share under 150 Hz). I kept ALLEY 62 (80 ms) and FEEDBK low (6-12).
* **No decay:** E: both DECAYs 0, both SUSTAINs full, RELEASEs the shortest (0.5 ms), ATTACKs 0. F: a 36 ms settle to a sustain at 79 %, 1 ms releases. H: a 54 ms settle to 88 %, 1 ms releases.

## What no-decay does (the character and the level)

* **The pluck becomes a gate.** B fell 16.5 dB inside the gate (10 dB in 46 ms) and had a tap on the front (359 Hz in the first 23 ms against 241 Hz after); E, F, G, H fall 0 - 0.8 dB and the first 23 ms equal the next 67: the note starts at once, holds with body for the gate and stops in about a millisecond. No click from the 0.5 ms release (the largest sample step is lower than B's: -40 ... -26 dBFS against -20).
* **It got duller before it got brighter.** The B pluck's tap was where its top lived: E (decay zero, CUTOFF +5 %) has 0.4 % of its energy above 400 Hz against B's 2.3 % (centroid 284 Hz against 480); F (CUTOFF +5 %, a little body) 1.6 %. To get *more* brightness than B in a note without the tap the cutoff has to go up more and the sub has to come down: H 3.4 %, G 5.0 %.
* **Level and headroom:** a note that holds is more energy in the gate, so VOLUME falls: **B 122/127 (5 steps of headroom) -> E 93, F 98, G 102, H 92 (35 steps)**; peaks -10.8 -> -12 ... -13.4 dBFS. Phrase (b): B -20.2, the new ones -16.9 ... -17.6 (nearer the reference).
* **The slap:** the first repeat stays where B was (**-6.3 dB -> -6.0 ... -6.2 dB** under the note's peak: the loudest possible, MIX 127). The second repeat is **-24 dB (E, F), -26 (H), -29 (G, B) under the first**: because the held note is a longer copy, FEEDBK 12 leaves the second repeat louder; H and G take FEEDBK to 8 and 6.
  The whole thing ends 178-256 ms after the note (voice alone 18 ms); H 178, B 192, F 256 (F's echo reaches -60 dB later than H's although the envelopes differ only in the settle time and sustain level; I did not find out why).

## The table (round 2; ">400 Hz" = % of energy above 400 Hz)

| | B anchor | E nodecay | F minimal | G crisp | H blend |
|---|---|---|---|---|---|
| VOLUME (headroom to 127) | 122 (5) | 93 (34) | 98 (29) | 102 (25) | 92 (35) |
| level (riff, echo incl.) / (b) | -18.0 / -20.2 | -17.9 / -16.9 | -18.0 / -17.3 | -18.0 / -17.6 | -18.0 / -17.4 |
| peak any phrase | -10.8 | -12.7 | -13.4 | -11.9 | -13.0 |
| dry notes band split % <60/60-150/150-400/400-1.2k/1.2k+ | 34 / 53 / 10 / 2 / 0 | 31 / 63 / 5 / 0 / 0 | 30 / 58 / 11 / 2 / 0 | 34 / 44 / 17 / 4 / 1 | 31 / 54 / 12 / 3 / 0 |
| echo band split % | 36 / 52 / 10 / 2 / 0 | 32 / 62 / 5 / 0 / 0 | 31 / 57 / 11 / 2 / 0 | 34 / 44 / 17 / 4 / 1 | 32 / 53 / 12 / 3 / 0 |
| centroid Hz: dry · echo | 480 · 413 | 284 · 239 | 343 · 302 | 568 · 499 | 406 · 365 |
| share above 400 Hz %: dry · echo | 2.3 · 2.4 | 0.4 · 0.4 | 1.6 · 1.6 | 5.0 · 5.0 | 3.4 · 3.4 |
| first repeat re note peak · second re first (dB) | -6.3 · -29 | -6.1 · -24 | -6.2 · -24 | -6.0 · -29 | -6.2 · -26 |
| pluck: drop in gate dB · centroid first 23 ms → next 67 ms | 16.5 · 359→241 | -0.0 · 249→249 | 0.8 · 420→404 | 0.7 · 720→708 | 0.5 · 536→521 |
| harmonics 3/5/7 re 1 (dB) | -17 / -29 / -38 | -14 / -24 / -32 | -14 / -24 / -32 | -11 / -15 / -22 | -27 / -21 / -25 |
| tail to -20/-40/-60 dB (ms) | 92/148/192 | 96/178/186 | 96/178/256 | 96/112/180 | 96/112/178 |
| voice alone to -60 dB (ms) | 20 | 18 | 18 | 18 | 18 |
| largest sample step dBFS (h) | -20 | -40 | -35 | -26 | -32 |
| worst-case CPU | 553 | 572 | 572 | 569 | 568 |

Changes before -> after (over the committed B) are in `round2/11-slapback-strut/README.md`. Short version: **E** CUTOFF 63 -> 69 (+5 %), ENV AMT 96 -> 64 (centre: 0), DRIVE 0 -> 30, FILTER A/D/R 20/56/60 -> 0/0/0, FILTER SUSTAIN 0 -> 127, AMP DECAY 72 -> 0, AMP SUSTAIN 0 -> 127, AMP RELEASE 24 -> 0, VOLUME 122 -> 93.
**F** as E but ENV AMT 76, both DECAYs 55 (36 ms), both SUSTAINs 100, both RELEASEs 10 (1 ms), VOLUME 98. **G** = F + PULSE WIDTH 64 -> 32, CUTOFF 82, KEY TRK 90, DRIVE 40, TONE 127, FEEDBK 6, VOLUME 102. **H** = F + PULSE WIDTH 44, CUTOFF 74, KEY TRK 110, DRIVE 40, TONE 110, FEEDBK 8, both DECAYs 60 (54 ms), both SUSTAINs 112, VOLUME 92.

## Recommendation: H

In the vocabulary: *tight, gated, a warm-ish soft top with a little DRIVE, more harmonics and less sub than B, a clean one-copy slap.* H is brighter than B at the top (3.4 % against 2.3 % above 400 Hz) with the echo 3 points less bass-heavy (85 % against 88 % under 150 Hz) and a 54 ms settle of body; the harmonics 3 / 5 / 7 at -27 / -21 / -25 dB (B -17 / -29 / -38) mean the 44 % pulse has a hollower third and a stronger fifth than a triangle: a rounder-than-square, more *reedy* tone than B's (I have not heard it; this is a measurement).
F is the milder one (1.6 %); G is the crispest (5.0 %, the echo 78 % under 150 Hz) but nearly a square at -11 / -15 / -22 dB (buzzy risk); E is the literal zero-decay reading (duller than B at its CUTOFF).
**Not asked, flagged:** H raises CUTOFF by 9 % (not 5 %) because the tap that carried B's top is gone; H's third harmonic is low (-27 dB) because of the pulse width; both are one knob each (PULSE WIDTH 64 puts it back).

## Questions for Vincent's ears
* H against B_anchor: **is the slap crisp enough, is the top soft but not dull?** If not crisp enough: G (watch the buzz). If too bright: F.
* **Is a note with no pluck at all what you meant** (it is a gated tone now), or do you want the 36 ms tap back (F's FILTER ENV AMT up)?

## Round count (11)
Round 1: 1 silent measured + 1 listening. Round 2 so far: 1 silent measured + 0 listening.

## FINAL (approved): variant G

Committed: O1 PW 32, CUTOFF 82, RESO 16, ENV AMT 76, KEY TRK 90, DRIVE 40, filter and amp ATTACK 0, DECAY 55 (36 ms), SUSTAIN 100, RELEASE 10 (1 ms), FEEDBK 6, TONE 127, MIX 127, ALLEY 62, PINGPONG 0, MONO, GLIDE 5, VOLUME 102 (25 steps of headroom to 127). Level -18.0 dBFS (riff, echo included), phrase (b) -17.6, peak -11.9 dBFS, worst-case CPU 569 host instr/sample (idle 380).
First repeat -6.0 dB under the note's peak, second -29 dB under the first; harmonics 3 / 5 / 7 of the oscillator at -10.7 / -15.2 / -21.7 dB (a square -9.5 / -14.0 / -16.9, a triangle -19 / -28 / -34). `check_slot.py 11 G round2`: resolved bytes identical, audio bit-identical from the boot patch and from INIT.
