# 31 · Fi(l)fth · Chapter IV The Ancient Relics

*Voiced 4–5 Nov 2026, approved as is (variant C, the DUAL stab). Renders: `reference-renders/31-fifth_C_*.wav` (C is this patch); the rejected variants are in the git history before `e40f5d5`. Log: `../31-fifth.md`.*

## 2. What it sounds like

The aggressive chord stab: a fifth built into every note, a hard filter pluck, and a short slap-back echo right behind it. Each note is a detuned pair,
so it is fat and punchy rather than thin, warm rather than icy, with a bright snap on the front that settles into a solid body. It is dry apart from the
slap: no spring, no long wash, just the stab and its quick echo.

## 3. Gear inspirations (docs only, "inspired by")

- **Sequential Prophet-5** — the stab itself, with weight behind it: *punchy, fat, warm*.
- **Roland Juno-60** — the short, snappy pluck: *plucky, punchy*.
- **Roland Jupiter-8** — the open top on the attack: *bright, full*.
- **Korg MS-20** — the bite when you dig in: *biting*.
- **Roland RE-201 Space Echo** — for the short delay: *slap, warm*.

Closest to: **a Prophet-5 stab through a Space Echo**.

## 4. How to play it

- **Register:** low to low-mid. Single notes and fifth-based riffs (roots and octaves around A1 to A2) are its home ground: every note already carries its own
  fifth, so one finger plays a power chord.
- **Touch and gate:** short and hard. A stab of roughly 150–200 ms is the target: bright snap, a body that rings a moment, then the slap. The patch has **no
  gate-length control**; how long the stab is comes from how long you hold the key.
- **Chords, honestly:** because the fifth is built into every voice, a chord made of fifths stacks fifths on fifths and turns into a sus2-style cluster (root and
  fifth together sound like root, fifth, ninth). That is the engine doing what the patch asks, not a fault. Play single notes and fifth-based riffs; use real chords sparingly.
- **Polyphony:** every note is two voices (the DUAL pair), so **a chord is three notes at most by design**: three notes use six voices, a fourth still fits (all eight
  voices), and a fifth steals from the notes before it.
- **CPU:** it is heavier than the single-voice version, which is the price of the fatter pair. Check the GLOBAL page's render time if you stack it with other heavy settings.
- **Tricks that suit it:**
  - **The slap (ALLEY):** it is already on, and it is what makes this the Space-Echo stab. Turning it up for a longer echo, or tapping a time in on the BBD page, suits it. Untested on this patch.
  - **ALGORITHM slop ride (SLOBBER):** loosens the pair. Untested on this patch; the patch's own slop is mild.
  - **Kill switch (HEEL)** for a dead stop: it clears the echo as well, so nothing rings on. Untested on this patch.
  - **Tape Stop (SEQ held)** as an ending. Untested on this patch.
  - **GROWL / DRAIN / CHEW:** at 0 on purpose (the patch's drive is the filter DRIVE, already in the sound). A spring will blur the stab; untested here.

## 5. Final values (for debugging, not for players)

`MODE DUAL, DETUNE 36 (~7.8 cents between the pair), POLY 8, SPREAD 90, VINTAGE 35, OSC1 SAW 110, OSC2 SAW +7st FINE 66 LVL 100, CUTOFF 92, RESO 22, ENV AMT 106, FILTER LP24 DRIVE 20, FILTER ENV A0 D52 S22 R50, AMP ENV A0 D72 S70 R52, ALLEY 65 (89 ms) FEEDBK 28 TONE 55 MIX 36 PINGPONG 60, VOLUME 92 (-18.0 dBFS RMS bank reference, phrase b); GROWL/DRAIN/CHEW 0, no LFO, no arp` — `PF_FIFTH` in `firmware/src/obv_patches.h`.
