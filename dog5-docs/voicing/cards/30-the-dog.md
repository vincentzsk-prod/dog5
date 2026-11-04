# 30 · THE DØG · Chapter IV The Ancient Relics (the signature patch)

*Voiced 4–5 Nov 2026, approved (variant H of round 2). Renders: `listen/voicing/batch-01a/30-the-dog/round2/` (H is this patch). Log: `../30-the-dog.md`.*

## 2. What it sounds like

A dry, punchy unison bass: every voice stacked on one note, fat and thick, loosened just enough that the stack breathes without ever going seasick. It is warm
with a driven edge that stops short of fuzz, and each note is chopped hard on release: no spring, no echo, no tail, only the silence after the hit. This is the
flagship, the DØG-5 signature, and it has presence: it sits forward and fills the room.

## 3. Gear inspirations (docs only, "inspired by")

- **Minimoog in unison** — the stacked saws and the octave-down body: *fat, sub-heavy, thick*.
- **Moog Taurus bass pedals** — the weight at the bottom: *deep, floor-shaking*.
- **Roland SH-101** — the quick attack and the hard stop: *tight, punchy*.
- **Oberheim OB-Xa in unison** — the wide, full stack with its warmth: *fat, full, warm*.
- **Korg MS-20** — the grit in the filter when it is pushed: *nasty, biting*.

Closest to: **a Minimoog in unison with Taurus weight**.

## 4. How to play it

- **Register:** low. Roots and octaves from about A1 to A2 are the sweet spot, and it is built for single-note bass lines and chopped roots.
  The very bottom (A0, and the A1 below it) is partly under what small speakers and many PAs reproduce: most of the audible weight is in the 60–150 Hz
  band and above, and the sub-octave saw underneath is inaudible at the very bottom. On a full-range system you feel it; on a laptop you hear the body, not the floor.
- **Touch and gate:** staccato to medium. Eighth-note chops (roughly 130 ms notes) are its home: a hard body, a stop, and the impact comes from the silence after.
  It also holds, as a wall of low unison, with a slow slight beat that stays under control.
- **One note at a time:** it is a unison. All eight voices play the one note you are holding, so chords are not available; use it for lines and roots.
- **Tricks that suit it:**
  - **ALGORITHM slop ride (SLOBBER):** loosens the stack further, from controlled to loose. Untested on this patch; the patch's own slop is mild, so there is room.
  - **Tape Stop (SEQ held)** as an ending: the whole low stack dives. Untested on this patch.
  - **Kill switch (HEEL)** for a dead stop; the patch has no tail to hide behind.
  - **Filter DRIVE (the FILTER + page):** the gentler route to more grit. It is already part of the sound; pushing it adds harmonics without squashing the dynamics.
  - **GROWL (adding it live):** the Psych Chain macros are 0 on purpose. GROWL only starts to do something above about 28 and compresses past about 40, so it is a
    big step, not a touch; it also costs noticeably more CPU than the filter drive.
  - **ALLEY, DRAIN, CHEW:** at 0 on purpose (dry and punchy is the sound); untested on this patch, and a wash will blur the chop.
- **Level:** it deliberately sits about 1.5 dB above the bank's usual level, for presence. Expect it to jump out a little when you switch to it.

## 5. Final values (for debugging, not for players)

`MODE UNISON, VOICES 8, DETUNE 35 (~15 cents end to end), VINTAGE 40, SPREAD 50, OSC1 SAW LVL 114, OSC2 SAW -12st LVL 94, CUTOFF 104, RESO 12, ENV AMT 88, KEY TRK 60, FILTER LP24 DRIVE 100, FILTER ENV A10 D58 S40 R50, AMP ENV A4 D70 S127 R48, VOLUME 56 (-16.5 dBFS RMS on the low-unison phrase; deliberately +1.5 dB over the -18.0 bank reference); GROWL/ALLEY/DRAIN/CHEW 0, no LFO, no arp` — `PF_THE_DOG` in `firmware/src/obv_patches.h`.
