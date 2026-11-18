# DØG-5 — BUILD REVIEW (tone & UI/UX) — condensed record

**Status:** 20 Oct 2026, condensed 27 Oct. This critique drove the decisions now captured authoritatively in
`DOG-5-base-and-ui-decisions.md` and `DOG-5-build-kit.md`. Kept as the reasoning trail. Everything flagged
here has since been resolved; this is the "why."

## Strengths (protect these under scope pressure)
- **TONE IS KING is operationalised** — the draw-priority list + dirty-area budget + per-frame quality tier +
  mid-frame µs hard stop are a mechanism, not a slogan.
- Graceful degradation and "eat status, never identity" are **one** mechanism (the draw order).
- **Bark-as-oscilloscope** is the only structurally unique idea (welded to the band name). The hill to defend.
- The signal law ("if it isn't driven by signal it's wallpaper") makes the screen teach the instrument.
- **IP position ahead of the scene** (build by ear, not shipping Sequential data).
- Preset work is tone-first (31 stock auditioned, ~65% liked, patterns identified, minimum gig set defined).
- The three-tier figure (hero / firmware / favicon) is the right production model.

## Weaknesses found → how they were resolved
- **"Audio can never be starved" was overstated.** Note *timing* (not the buffer) was the risk → RESOLVED:
  the base fixed it in 1.4.2 (`app_idle` in the DMA wait); inherited by pinning 1.5.3; one DRAW RULE carries
  it forward. (Vincent's instinct that latency wouldn't harm sharp tones was correct, for a better reason.)
- **Spring reverb was the biggest un-de-risked tone bet** (Bee-tch is 7/8 dependent) → RESOLVED: "next
  closest thing" is explicitly enough; re-voice the plate toward spring; no longer a gate.
- **Fork feature-pressure / divergence unpriced** → RESOLVED: pin v1.5.3, fetch-only upstream, cherry-pick.
- **Voice count 5-vs-8 decided on paper** → RESOLVED: made a knob (`P_POLY_N`, default 5), settled by ear.
- **HOME double-booked** (art vs PERFORM) → RESOLVED: HOME = PERFORM; the art is HOME's resting state; knob
  values are transient (Monologue), bar is number+name only.
- **UI map stale / renamed-controls legibility** → RESOLVED: 20-page table; hold-HOME control map (Skiff);
  families-remember; OCT stays octave; layer-lock inherited.
- **Patch-name budget** (field was 10) → RESOLVED: widen to 14 + grow `PATCH_BYTES` to 96; 4 names changed.
- **Scene identity by colour alone** → RESOLVED: the static field is the scene marker (must read in
  silhouette); Moonshine purple → magenta.
- **Idle sway vs navigation** → RESOLVED: suppressed while PRESETS turns (and on note-on).
- **No sim / installer / editor** → RESOLVED: sim + installer in scope (sim inherited from the base); web
  editor dropped (live instrument, not a sound-design workstation).
- **Doc debt** (the design-system file would reproduce a reaper) → RESOLVED: design-system deleted; reaper-era
  docs archived; this handoff re-states the live world.

## The honest summary
The thinking was well ahead of the building; the gap was the risk. Rule 1 is better enforced than in most
projects (the draw-priority mechanism). The identity work is strong; the navigation work was thin and is now
specced. Build the instrument you reach for in the dark, not just the image.
