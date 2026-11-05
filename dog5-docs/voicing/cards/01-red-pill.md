# 01 · Red Pill · Chapter I Wasteland

*Voiced 5 Nov 2026, approved as rendered (variant C of Batch 3A). Renders: `reference-renders/01-red-pill_C_*.wav` (C is this patch). Log: `../01-red-pill.md`.*

## 2. What it sounds like

A nervous, spitting bass made to sit under a vocal. Two fat saws, stacked and held steady, push through a resonant filter that snaps at the start of every note, and the whole thing is driven hard enough to be gritty and warm without getting piercing. It is nearly dry: a quick slap and a small spring sit behind each note as an afterthought, lifting it a little, and never getting anywhere near as loud as the note itself.

## 3. Gear inspirations (docs only, "inspired by")

- **Korg MS-20** — the resonant filter and its bite: *nasty, biting, resonant*.
- **Minimoog** — the stacked saws: *fat, thick*.
- **Roland SH-101** — the tight snap at the front of a note: *tight, punchy*.
- **ProCo RAT** — the driven edge: *gritty, crunchy*.

Closest to: **an MS-20 bass through a RAT**.

## 4. How to play it

- **Register:** low. It was voiced on a riff from A1 (55 Hz) up to A2 and on sixteenth-note bursts of A1, C2, D2 and E2; other registers are untested. About half of the energy on the low riff sits under 60 Hz, which is the A1 fundamental itself: it is the 100 Hz and up that carries it on a small speaker, and whether it is heard enough under a vocal on a PA is for the room.
- **Touch and gate:** short, detached notes are its home (80 to 150 ms gates were measured). The filter snap gives the "spit": on an isolated A1 the first 23 ms are about 1.8 times as bright (centroid) as the next 67 ms.
- **It is MONO, so legato does not re-fire the envelopes:** a key still held when the next one goes down slides to the new note without a new snap. Play it detached for the spit. A chord plays one note (the last).
- **Stable on purpose:** the pitch wander measured 0.3 cents (s.d., the engine's log of the voice, held A2) on this variant, C, with VINTAGE 10, no LFO, no glide.
- **The wet is small, and it is measured.** Behind a note the slap and spring return is, in the loudest of three isolated notes, 43.6 dB under the dry note in the first 20 ms, 25.0 dB under at 20 to 100 ms and 16.5 dB under at 100 to 250 ms (that last window is the tightest, since a 150 ms note is already ending in it). After the key goes up the level is 20 dB down at 24 ms, 40 dB down at 214 ms and 60 dB down at 436 ms; the voice alone is 60 dB down at 54 ms. So there is a short wet tail of about half a second.
- **Costs, honestly:** the grit comes partly from a GROWL step, which costs about +595 host instr/sample whenever it is on; the worst case for the patch is about 1640 host instr/sample (the original: 317). The device build was not run; the render time on the device is not measured.
- **Slot 1 is the boot patch.** Changing it shifts the first moments of echo and spring programs loaded straight after power-on by a small amount (the filter smoothing carries the boot patch's state); see the voicing README, section 12.
- **Tricks:** untested on this patch: the SLOBBER slop ride (it will loosen the deliberately steady pair), SEQ held (Tape Stop), the kill switch (HEEL), CHEW. More GROWL than 46 or more echo than the measured amount is untested for the "never above the note" rule; a variant with the wet turned up was rendered, and there the echo came to about 6 dB under the note in the last window.
- **Level:** matched to the bank reference on the low riff (-18.0 dBFS RMS; peak -12.8 on the whole render; phrase (b) reads -18.0 too).

## 5. Final values (for debugging, not for players)

`MODE MONO, OSC1 SAW LVL 110, OSC2 SAW 0 st LVL 104 FINE +10 (7.8 cents), CUTOFF 92, RESO 58, ENV AMT 104, KEY TRK 100, FILTER LP24 DRIVE 110, FILTER ENV A0 D52 S30 R40, AMP ENV A0 D70 S127 R26, VINTAGE 10, SPREAD 40, GROWL 46 BIAS 30 TONE 55, ALLEY 62 (80 ms) FEEDBK 10 TONE 60 MIX 16 PINGPONG 0, SPRING DRAIN 18 SIZE 40 DAMP 70 PRE-DLY 20, VOLUME 87 (-18.0 dBFS RMS on the spit riff, peak -12.8); CHEW 0, no LFO, no glide, no arp` — `PF_RED_PILL` in `firmware/src/obv_patches.h`.
