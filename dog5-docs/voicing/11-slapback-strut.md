# Voicing log — 11 "Slapback Strut" (FACTORY[10], Batch 2A, the percussive surf bass)

Nov 2026. Brief (Batch 2A, "weight and space"): *percussive surf bass. Single triangle, very fast decay, one loud ~80 ms free-time echo (ALLEY ~80 ms, FEEDBK low). This is why the delay runs in free ms.* A flatwound
Precision Bass into a Space Echo (SH-101 tightness, Minimoog round low end, a Fender-style spring for the surf wash). Method and kit: `README.md` here (§1 phrases, §3 loudness, §10 Batch 2A). Listening files (on the
`listen/batch-02a-weight-and-space` branch only): `listen/voicing/batch-02a/11-slapback-strut/`; `README.md` and `numbers.md` there are the full tables and are on the voicing branch too.

**Status: B (centre) COMMITTED as the recommended variant, awaiting Vincent's ears.** A, C, D are render-only. **Round count so far: 1 silent measured round (incl. a sweep of the decay against the reachable level)
+ 0 listening rounds.** No voice card yet.

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
