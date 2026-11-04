# 25 · SAWTOOTH · Chapter IV The Ancient Relics

*Voiced 4–5 Nov 2026, approved as is (variant B). Renders: `listen/voicing/batch-01a/25-sawtooth/` (B is this patch). Log: `../25-sawtooth.md`.*

## 2. What it sounds like

The iconic poly brass: two saws a few cents apart, stable and warm, with the filter swelling open on each note and settling into a solid, brassy body. It holds
still: no wobble, no chop, no mess, only a gentle vibrato that fades in if you hold a note. A Prophet-5 survivor, rebuilt by ear.

## 3. Gear inspirations (docs only, "inspired by")

- **Sequential Prophet-5** — the swell and the two-saw body: *fat, warm, swell*.
- **Oberheim OB-Xa** — the brass section feel: *brassy, full*.
- **Roland Jupiter-8** — the bright blare at the top of the swell: *bright brass*.
- **Memorymoog** — the weight of the chord: *thick, warm*.
- **Korg Polysix** — the slow vibrato wobble on a held note: *fat, wobble*.

Closest to: **a Prophet-5 brass swell**.

## 4. How to play it

- **Register:** low-mid to mid. Chords and fifth-and-octave voicings are its home ground; each note is one voice, so ordinary three- and four-note chords play in full.
- **Touch and gate:** medium to long. The swell comes from the **filter envelope** and peaks about 84 ms in, so the brass opens on each note: notes of a couple of hundred
  milliseconds or more show it best, and a very short stab catches only the first part of the swell.
- **Stable on purpose:** compare **03 Half-Life**, which is unstable and chopped; SAWTOOTH is the opposite, steady and warm. Use it where you want the chord to sit.
- **Vibrato:** a gentle vibrato fades in after about 1.1 s on held notes (a Prophet-style brass detail). It is the one moving part; set **LFO PITCH to 0** for a fully still sound.
- **Tricks that suit it:**
  - **ALGORITHM slop ride (SLOBBER):** the way to make it wobble like a tired string-brass; untested on this patch.
  - **Tape Stop (SEQ held)** as a swell-out ending. Untested on this patch.
  - **Kill switch (HEEL)** for a dead stop; there are no effects tails to hide behind.
  - **GROWL:** **0 on purpose.** A touch measured as almost nothing audible on this patch and costs noticeable CPU, so it is left to you live (GROWL only starts to do something above about 28). Untested by ear here.
  - **ALLEY, DRAIN, CHEW:** at 0 on purpose (a dry brass); a spring or echo is yours to add.

## 5. Final values (for debugging, not for players)

`MODE POLY (POLY 5), VINTAGE 30, OSC1 SAW 110, OSC2 SAW 0st FINE 71 (~5.5 cents) LVL 100, CUTOFF 56, RESO 15, ENV AMT 100, FILTER LP24, FILTER ENV A70 (~117 ms) D85 S50 R60, AMP ENV A50 D70 S100 R55, LFO TRI RATE 75 DELAY 60 -> PITCH 20, VOLUME 97 (-18.0 dBFS RMS bank reference, phrase b); GROWL/ALLEY/DRAIN/CHEW 0, no arp` — `PF_SAWTOOTH` in `firmware/src/obv_patches.h`.
