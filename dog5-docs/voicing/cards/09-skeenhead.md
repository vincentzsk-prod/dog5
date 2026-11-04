# 09 · Skeenhead · Chapter II THE TIDAL HEXES

*Voiced Nov 2026, approved as is (variant E of Batch 2A round 2). Renders: `listen/voicing/batch-02a/round2/09-skeenhead/` on the `listen/batch-02a-weight-and-space` branch (E is this patch). Log: `../09-skeenhead.md`.*

## 2. What it sounds like

A tight, plucky square stab with a resonant plop on the front, drenched in spring. The note has a body now and it holds for as long as you play it; the spring rings on after the note and is the sound of the patch. It is a wet, springy, boingy reggae stab.

## 3. Gear inspirations (docs only, "inspired by")

- **Korg MS-20** — the resonant filter plop: *plucky, biting*.
- **Roland SH-101** — the tight, quick stab: *tight, punchy*.
- **Moog Prodigy** — the single raw square: *fat, cheap, raw*.
- **Fender spring reverb tank (Twin Reverb style)** — the drench: *springy, boingy*.
- **Roland RE-201 Space Echo** — the dub-style tail: *warm*.

Closest to: **an MS-20 plop into a Fender spring tank**.

## 4. How to play it

- **Register and gate:** off-beat two-note stabs of about a tenth of a second, around A3 to C4 (the skank it was voiced on). Other registers are untested.
- **The plop is still there, softer.** The resonant filter sweep is still audible by tone (measured: the first 23 ms of a stab are twice as bright as the next 67), but the first 20 ms is now only about 3.5 dB louder than the body, so the pop is softer than in the first version of this patch.
- **The body survives the gate.** The filter now rests above the played notes instead of closing under them, and the amp holds (measured: the level falls under 4 dB inside the gate; the first version fell almost 17 dB and left a hum).
- **The spring is the sound:** it ships at DRAIN 90. Measured, the spring's return is about 6 dB under the dry note over the stabs (6.1 dB), and by time window after a stab it is about 22 dB under the note in the first 20 ms, about 6 dB under in 20 to 100 ms, and **about 6 dB louder than the note in 100 to 250 ms**, which is natural for a spring:
  it is what rings after the note stops. The tail takes about 1.1 s to fall 60 dB. The gap between stabs sits about 16 dB under the stab (measured -16.3 dB on variant E, the committed one; `../09-skeenhead.md`, round-2 table).
- **Tight and stable:** one voice per note, one oscillator, no detune and no LFO. VINTAGE is at the default (30); I measured no wander on this patch, so I do not claim how steady it is.
- **Chords:** polyphony is the default 5, so a two-note stab uses two voices; larger chords were not tried.
- **Tricks that suit it:** untested on this patch: the SLOBBER slop ride, Tape Stop (SEQ held), the kill switch (HEEL), the ALLEY echo, GROWL, CHEW. Turning DRAIN down for a drier stab is untested.
- **Held notes:** it is a stab patch. A held note was not measured on this version.

## 5. Final values (for debugging, not for players)

`MODE POLY (POLY 5), OSC1 PULSE PW 64 LVL 110, OSC2 OFF, CUTOFF 46, RESO 62, ENV AMT 118, KEY TRK 100, FILTER LP12, FILTER ENV A20 D56 S40 R60, AMP ENV A0 D70 S64 R28, SPRING DRAIN 90 SIZE 70 DAMP 40 PRE-DLY 4 (1.1 ms), VOLUME 92 (-17.9 dBFS RMS over the stabs of the skank phrase, spring on; dry stabs alone -19.0; phrase (b) -17.4; peak -6.3); GROWL/ALLEY/CHEW 0, no LFO, no arp` — `PF_SKEENHEAD` in `firmware/src/obv_patches.h`.
