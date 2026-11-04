# 03 · Half-Life · Chapter I Wasteland

*Voiced 4 Nov 2026, approved as is. Renders: `listen/voicing/03-half-life/` (B is this patch). Log: `../03-half-life.md`.*

## 2. What it sounds like

Fat, slop-heavy dual saws with a sub-octave underneath: seasick, never quite in tune with itself, and thick without
going murky. Short notes are chopped stone-dead by the gate, and the tail doesn't fade, it sputters — a few ragged
stutters as the note dies. It is a raw, dry, engine-only sound with no effects on it: the drift and the chop are the
whole point. This is the DØG-5 thesis in one patch.

## 3. Gear inspirations (docs only, "inspired by")

- **Korg Mono/Poly** — detuned oscillators that drift and never settle: *fat, slop, seasick, thick*.
- **Sequential Prophet-5 (early, tuning-unstable revisions)** — the dual-saw warmth with the drift: *fat, warm, drift*.
- **Minimoog** — the body under the instability: *fat, sub-heavy, thick*.
- **Korg MS-20** — the bite and the spit in the filter and the tail: *nasty, biting, spitting*.

Closest to: **Korg Mono/Poly** — its drifting, detuned saw chaos, with Minimoog weight underneath, chopped by the gate.

## 4. How to play it

- **Register:** low to low-mid. Roots and fifths from about A1 to A3 are where the sub and the pair sit best. Fifth-and-octave
  power chords are its home ground.
- **Touch and gate:** play it staccato. **Short notes, roughly 150–180 ms, are where it works as intended**: a clean, hard
  body and a sputtering tail.
- **Where it does not work:** the sputter is tied to how long the note has been sounding, not to the key coming up. A note
  held past about a fifth of a second **spits all the way through**, and very short notes (under about 100 ms) only catch the
  start of it. Long held pads and sustained leads are the wrong job; use it for riffs and stabs.
- **Chords:** polyphony is set to **POLY 6** because every note is two voices. Two- and three-note chords (a fifth, or a fifth
  with the octave) play in full. A fourth note in a chord, or a very busy run, steals voices from the notes before it: keep chords to three notes.
- **Tricks that suit it:**
  - **ALGORITHM slop ride (SLOBBER):** the best one. The patch already drifts; the ride pushes it from seasick to
    dying-tape-motor, at up to about three and a half times the patch's own slop. Expect the low voice to sag flat and the others to lean sharp at full ride (accepted character).
  - **Tape Stop (FLOP held)** on the riff as an ending; it dives the whole sound.
  - **Kill switch (HEEL)** for a dead stop mid-riff: the sound and the sputter stop at once.
  - **Macros (GROWL, ALLEY, DRAIN, CHEW):** all at 0 on purpose. Untested on this patch, so treat them as
    open: the dry chop is the sound, and a wash of ALLEY or DRAIN on the tail will bury the sputter.

## 5. Final values (for debugging, not for players)

`MODE DUAL, DETUNE 60, POLY 6, SPREAD 110, VINTAGE 90, OSC1 SAW 110, OSC2 SAW -12st LVL 80, CUTOFF 76, RESO 30, ENV AMT 96, FILTER LP24, AMP RELEASE 62 (others default), LFO SQUARE RATE 119 (20.1 Hz) DELAY 19 (112 ms) -> AMP 100, VOLUME 112 (-18.0 dBFS RMS bank reference); GROWL/ALLEY/DRAIN/CHEW 0` — `PF_HALF_LIFE` in `firmware/src/obv_patches.h`.
