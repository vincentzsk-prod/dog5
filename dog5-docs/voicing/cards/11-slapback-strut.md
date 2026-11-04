# 11 · Slapback Strut · Chapter II THE TIDAL HEXES

*Voiced Nov 2026, approved as is (variant G of Batch 2A round 2). Renders: `reference-renders/11-slapback-strut_G_*.wav` (G is this patch); the other variants and the held renders are in `listen/voicing/batch-02a/round2/11-slapback-strut/` on the `listen/batch-02a-weight-and-space` branch. Log: `../11-slapback-strut.md`.*

## 2. What it sounds like

A tight, gated surf bass: the note starts at once, holds its body for as long as you hold the key, and stops dead. Behind each note comes one clean, loud echo, a plain copy of the note a moment later, and then nothing.
It is bright and crisp on top for a bass, sharp and a little biting, and dry otherwise.

## 3. Gear inspirations (docs only, "inspired by")

- **Fender Precision Bass (flatwounds)** — the plucky, snappy attack: *plucky, snappy*.
- **Roland SH-101** — the tight, quick note: *tight, punchy*.
- **Minimoog** — the round, percussive low end: *round, percussive*.
- **Binson Echorec / Roland RE-201** — the single slap: *slap, warm*.
- **Fender spring reverb** — the surf wash: *surf wash*.

Closest to: **a flatwound P-Bass into a Space Echo**.

## 4. How to play it

- **It is a gated bass, not a pluck.** The decay is gone on purpose (measured: the level falls under 1 dB inside a 100 ms note, and the first 23 ms is as bright as the next 67), so the note starts at once, holds its body for the length of the gate and stops in about a millisecond
  (the voice alone is silent about 18 ms after the key-up). The pluck character of the first version is not in this one.
- **Register:** low, A1 to A2 (the surf riff it was voiced on). Other registers are untested.
- **No triangle oscillator exists in the engine**, so the sound is a narrow pulse through a key-tracking low-pass. It is bright enough that the upper harmonics are close to a square wave's (measured: the third and fifth harmonic sit at about -11 and -15 dB under the fundamental, a square's are -9.5 and -14, a triangle's -19 and -28),
  so it is sharp and biting, and it may buzz on a very bright amp.
- **The slap:** one clean copy of the note at 80 ms. The first repeat is about 6 dB under the note's peak (measured -6.0 dB) and the second is much lower (about 29 dB under the first), so it is a single slap, and it ends about 180 ms after you let go. It is already at the engine's maximum:
  the delay's MIX is at its top and cannot be louder. The delay's TONE does nothing audible on this bass (turning it from 70 to 127 moved the echo's brightness by 1 Hz on a close variant), because the echo is a faithful copy of the note.
- **Play it detached.** It is a mono patch, and the engine does not re-fire the envelopes on a legato note (an engine rule found in Batch 1A; not re-tested on this patch): a second key pressed while the first is down slides and does not hit again.
- **The spring (DRAIN):** it ships at 0. A spring wash behind the slap was measured on the first version of this patch (it rang out to -60 dB in about a second), but it is **untested on this version**.
- **Tricks that suit it:** untested on this patch: the SLOBBER slop ride, Tape Stop (SEQ held), the kill switch (HEEL), GROWL, CHEW. It does not use polyphony: one note at a time.

## 5. Final values (for debugging, not for players)

`MODE MONO, GLIDE 5, OSC1 PULSE PW 32 LVL 127, OSC2 OFF, CUTOFF 82, RESO 16, ENV AMT 76, KEY TRK 90, FILTER LP12, DRIVE 40, FILTER ENV A0 D55 S100 R10, AMP ENV A0 D55 S100 R10 (all on the 0-127 scale: D55 = a 36 ms settle, S100 = a sustain at 100/127 = 79 % of the peak, about -2 dB, R10 = 1 ms; the amp S100 is the engine default, so it is not in the committed byte list), ALLEY 62 (80 ms) FEEDBK 6 TONE 127 MIX 127 PINGPONG 0, VOLUME 102 (-18.0 dBFS RMS over the note-on region of the surf riff, echo included; phrase (b) -17.6; peak -11.9); GROWL/DRAIN/CHEW 0, no LFO, no arp` — `PF_SLAPBACK_STRUT` in `firmware/src/obv_patches.h`.
