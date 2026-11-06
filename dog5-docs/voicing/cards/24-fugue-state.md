# 24 · Fugue State · Chapter III · The Bakshi Tomes

*Voiced 6 Nov 2026 (Batch 5B), approved after listening: variant C ("24 Fugue State C"). Renders: `reference-renders/24-fugue-state_C_*.wav`. Tables (on the voicing branch): `listen/voicing/batch-05b/24-fugue-state/README.md`.*

## 2. What it sounds like

A soft, dark, triangle-like pad whose pitch trembles quickly, wide in the stereo field. Each chord runs into a short echo that feeds back on itself while the pitch is still moving, so the repeats sit at slightly different pitches from the notes being played and the chord smears. A spring adds a further tail, and the sound hangs on for several seconds after you let go. There is no filter movement, only the pitch and the echo.

## 3. Gear inspirations (docs only, "inspired by")

- **Electro-Harmonix Deluxe Memory Man** — *BBD feedback with pitch modulation; Seasick, Wet.* Wet: 10 repeats stay above −40 dB under the note, 4 above −20 dB, and the echo return takes 1721 ms to fall to −40 dB (measured). Pitch modulation: there is none inside the echo; the LFO moves the oscillators, so each repeat carries an earlier pitch state, and the largest gap between a note and its own repeat is 212 cents (computed from the LFO law, not from audio). Seasick: not measured; at 4.9 Hz the movement is a wobble, not the slow sway of the dictionary's Seasick.
- **Roland RE-201 Space Echo** — *self-oscillating echo feedback; Wash.* Wash: the release tail takes 4624 ms to fall 60 dB (measured). Self-oscillation: this patch does not self-oscillate; its repeats decay (FEEDBK 95), and a 30 s held chord grows by +0.2 dB with no clipping (measured). A higher FEEDBK was not voiced for this variant.
- **Korg Polysix** — *the ensemble-chorus dizziness; Wobble, Beating.* Wobble: a triangle pitch LFO at 4.9 Hz (RATE 91), law ±178 cents (measured ±150, under-read by the 60 ms analysis frames; the law is the number to trust). Beating: not measured (OSC 2 is the octave copy, 1.6 cents from true). There is no chorus in the patch.

Closest to: **a soft triangle-like pad run through a Memory Man until it seasicks itself**.

Nothing here says the patch matches these: it was built toward the descriptions, by measurement, and approved by ear.

## 4. How to play it

- **The pad:** a narrow pulse (OSC 1, PW 32 = 25 %) plus an octave-up copy of it (OSC 2, LEVEL 45) through a 12 dB low-pass at CUTOFF 63 with 100 % key tracking. Harmonics 3 / 5 / 7 of OSC 1 at rest read −17.5 / −27.9 / −37.5 dB against an ideal triangle's −19.1 / −28.0 / −34.2 (measured). The copy adds even harmonics only.
- **Dark:** the held chord's centroid is 588 Hz, with 80 % of the energy in 150–400 Hz, 20 % in 400–1.2 kHz and 0.25 % above (4–10 s). The MUD ratio (317) is saturated by that empty top, so read the shares. A stronger copy (OSC 2 LEVEL 100) moved the 150–400 Hz share from 79 % to 64 % in the round 1 probe on the B variant.
- **Slow and soft:** the amp attack is A85 (about 377 ms nominal) and the release R110 (about 2.6 s); a 150 ms chord tap reads −27.3 dBFS, 9.4 dB under the held chord, and its tail takes 3764 ms to fall 40 dB. Stabs are quiet (phrase (b) −22.5 dBFS RMS). It is a held-chord patch.
- **Width:** the left and right channels of the held chord correlate at 0.51 (measured, 150 Hz–4 kHz band).
- **The LFO:** one shared LFO (TRI, 4.9 Hz, PITCH 50, to both oscillators). PHASE is SPREAD, which gives per-voice offsets; their size was not measured. One shared LFO means no true rotary or quadrature movement.
- **The echo:** ALLEY 144 ms, FEEDBK 95, MIX 85, PINGPONG at its maximum. With a short 120 ms chord stab (a fast attack and release, the probe copy) the first repeat is −10.1 dB under the note and the spring return is 1.1 dB louder than that first repeat in the same window (measured).
- **Runaway tests:** a 30 s held triad: peak −4.9 to −6.5 dBFS in every 2 s window, growth +0.2 dB; twelve chords 1 s apart: the best later chord is +3.3 dB over the first, peaks no higher than −5.5 dBFS. No clipping. Release: the tail is 20 / 40 / 60 dB down at 1648 / 3520 / 4624 ms.
- **Polyphony:** POLY with the default 5 voices. The MONO / UNISON legato rule does not apply (engine fact; not tested on this patch).
- **Level and cost:** VOLUME 85, −17.9 dBFS RMS over +4 to +10 s of the held triad (K-weighted −18.0), peak −4.9 dBFS over every audition phrase. **CPU 2038 host instr/sample worst case.** The device render time is not measured.
- **Tricks:** SLOBBER, SEQ held (Tape Stop), GROWL and CHEW are untested. The PLAY/STOP kill switch clears the echo buffers, including the feedback (engine fact; not tested on this patch).

## 5. Final values (for debugging, not for players)

`MODE POLY (POLY 5), OSC1 PULSE PW 32 LEVEL 110, OSC2 PULSE PW 32 LEVEL 45 SEMI +12 FINE 66 (+1.6 cents), FILTER LP12 CUTOFF 63 (494 Hz) RESO 5 KEY TRK 127 ENV AMT 64 (zero), FILTER ENV A90 D100 S50 R100 (inert at ENV AMT 64), AMP ENV A85 D100 S127 R110, LFO TRI RATE 91 (4.9 Hz) PHASE SPREAD PITCH 50 (±178 cents, both oscillators), VINTAGE 60, SPREAD 120, BBD ALLEY 79 (144 ms) FEEDBK 95 TONE 45 MIX 85 PINGPONG 127, spring SIZE 100 DAMP 60 PRE-DLY 30 DRAIN 45, GROWL 0, CHEW 0, VOLUME 85` — `PF_FUGUE_STATE` in `firmware/src/obv_patches.h`.
