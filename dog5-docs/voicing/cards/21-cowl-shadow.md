# 21 · Cowl Shadow · Chapter III The Bakshi Tomes

*Voiced Nov 2026, approved as is (variant C of Batch 2A). Renders: `reference-renders/21-cowl-shadow_C_*.wav` (C is this patch); the other variants and the held renders are in `listen/voicing/batch-02a/21-cowl-shadow/` on the `listen/batch-02a-weight-and-space` branch. Log: `../21-cowl-shadow.md`.*

## 2. What it sounds like

A brass wall that starts dark and soft and swells open while you hold the note. It begins as a quiet, murky hum and, in a few seconds, blooms into a wide, full, glowing brass, with a slow
drift inside the stack. It is dry. When you let go it fades out slowly and darkens as it goes.

## 3. Gear inspirations (docs only, "inspired by")

- **Yamaha CS-80** — the slow brass swell: *soft, slow, swelling*.
- **Oberheim OB-Xa** — the brassy body: *brassy, full*.
- **Roland Jupiter-8** — the bright blare at the top of a swell: *bright blare*.
- **Korg Mono/Poly (in unison)** — the stacked, drifting oscillators: *fat, drifting*.

Closest to: **a CS-80 brass swell, stretched**.

## 4. How to play it

- **Hold the note.** The bloom happens while the key is down and takes about five seconds (measured on A2: the sound is a tenth of the way open at under a second and nine-tenths open at about four
  seconds). A **sustain pedal** should hold it open the same way (the engine has a sustain pedal; not tried on this patch). There is **no drone latch** (the ENV "Drone Latch" control does not exist), so
  there is no way to keep the gate open except the key or the pedal.
- **Release early and it never opens.** Let go after a couple of seconds and you get a dark, soft swell that just fades (measured: at a 2.4 s key-up it is still dark, about a fifth as bright as the
  full bloom, and dies away in about two seconds). Let go after a long hold and the release takes about a second to drop 20 dB and about four to vanish, with the brightness leaving with the level.
- **Legato does not restart the bloom.** It is a five-voice unison, and the engine does not re-fire the envelopes on a legato note (an engine rule found in Batch 1A; not re-tested on this patch): a
  second key pressed while the first is down slides and keeps going. To bloom again, release and play a new note.
- **It will sound quiet if you tap a note.** Short stabs are the dark start of the bloom: on the stabs phrase it reads about 13 dB under its fully bloomed level (measured). If you switch to it and tap
  a key it will seem far too quiet; hold the note and it comes up to the bank level.
- **Register:** it was voiced and measured on A2 only; other registers are untested.
- **One note at a time:** unison, all five voices on the note you hold; chords are not available.
- **Tricks that suit it:** untested on this patch: the SLOBBER slop ride, Tape Stop (SEQ held), the kill switch (HEEL). It ships dry; a little DRAIN would add depth (untested).

## 5. Final values (for debugging, not for players)

`MODE UNISON, VOICES 5, DETUNE 40 (spread +-9.8 cents), VINTAGE 45, SPREAD 100, OSC1 SAW 110, OSC2 SAW 0st FINE +1.6 cents LVL 100, CUTOFF 40, RESO 14, ENV AMT 118, KEY TRK 127, FILTER LP24, FILTER ENV A119 (5.3 s) S127 R110, AMP ENV A90 S127 R108, VOLUME 79 (-18.0 dBFS RMS over +6..+10 s of the A2 hold; phrase (b) -31.3); GROWL/ALLEY/DRAIN/CHEW 0, no LFO, no arp` — `PF_COWL_SHADOW` in `firmware/src/obv_patches.h`.
