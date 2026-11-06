# 18 · Roto-scopo · Chapter III · The Bakshi Tomes

*Voiced 6 Nov 2026 (Batch 5A), approved after listening: variant D (the slow, deep, sloppiest one; Vincent: "sounds awesome"). Renders: `reference-renders/18-roto-scopo_D_*.wav`. Log: `../18-roto-scopo.md`.*

## 2. What it sounds like

A low, dark drone: a square-wave tone with a second square an octave below it, played by three slightly out-of-tune voices. A resonant low-pass filter opens and closes slowly and unpredictably by itself, so the tone moans and drifts without a knob being touched. It is dry: no echo, no spring. It only lasts while a key is held.

## 3. Gear inspirations (docs only, "inspired by")

- **Korg MS-20** — *resonant, unruly low-passed square* (resonant: measured, a 12 dB low-pass at RESO 115 that is still linear, probe 11.3 dB against 12 for a linear filter, and sings by itself only at RESO 127; "unruly" is not measured).
- **ARP 2600 sample-and-hold** — *wandering cutoff* (the cutoff does wander, measured below, but this variant uses the smooth RANDOM shape, not sample-and-hold; the sample-and-hold take was variant C, not chosen).
- **Moog Taurus I** — *dungeon-low weight* (measured on A1: 62 % of the energy under 60 Hz and 17 % in 60 to 150 Hz; the second oscillator sits an octave down).

Closest to: **a Taurus-weight square through an MS-20 filter that a random source keeps nudging**.

Nothing here says the patch matches these: it was built toward the descriptions, by measurement, and approved by ear.

## 4. How to play it

- **It needs a held key or the sustain pedal.** There is no Drone Latch; the sound ends with the key (AMP release about 2.7 s nominal; on A1 the tail is 20 dB down at 1.75 s and 40 dB down at 3.31 s, 60 dB is not reached in the 4.5 s render).
- **One note at a time.** The patch is a 3-voice UNISON: a chord plays only its last key (three keys gate three voices, not nine). Legato: a key struck while another is held slides and does not restart the envelopes (MONO and UNISON behave so; known engine fact, README section 8).
- **Best in the low register.** Judged on A1 (55 Hz) and A2 (110 Hz) holds of 15 s. A short tap is much quieter than the held note because the amp attack is slow (AA 100): a 150 ms tap reads 16.1 / 13.1 / 17.9 dB under the held level on A1 / A2 / A3, centroid 684 / 830 / 1644 Hz.
- **The wander is one shared LFO on the cutoff, and nothing else.** A smooth random LFO at 0.11 Hz (RATE 15), FILTER depth ±23.9 st, PHASE FREE. There is **no Poly-Mod** in this engine: the movement cannot follow OSC 2, it is not tied to any oscillator, and the one LFO rate is the same for everything the LFO touches (here only the filter; LFO PITCH is 0). The wander is common to all voices. Measured over 0.5 s windows from 2 s to 14.5 s of the hold: spectral centroid on A1 316 to 708 Hz (s.d. 100 Hz, a 14.0 semitone range), on A2 479 to 1003 Hz (s.d. 152 Hz, 12.8 semitones); the level moves 0.8 dB s.d. (A1) and 1.0 dB (A2).
- **Slop (VINTAGE 127, the knob's top):** the engine's own log on a 13 s A1 hold: the three voices sit at −7.6 / +4.3 / +1.7 cents static, with 5.8 / 5.6 / 6.6 cents s.d. of wander (ranges −23..+18, −14..+31, −29..+19). The SLOBBER ride adds to it (untested on this patch).
- **Tone on A1, settled hold (5 to 14 s):** energy under 60 Hz 62 %, 60 to 150 Hz 17 %, 150 to 400 Hz 11 %, 400 to 1.2k 10 %, over 1.2k 0.4 %; centroid 465 Hz. MUD ratio per window (0–1 / 2–5 / 5–10 / 10–14 s): 16 / 4 / 14 / 225.
- **Level and cost:** VOLUME 72, −17.9 dBFS RMS over +5 s to +14 s of the A1 hold (K-weighted −20.7; the first second −18.7), peak −8.0 dBFS over all audition phrases, no clipped sample. Phrase (b) stabs read −23.3 dBFS RMS: stabs are not what this patch is for. About 1897 host instr/sample worst case (idle 1164 + 734 under load); the device render time is not measured.
- **Tricks:** untested on this patch: SLOBBER, SEQ held (Tape Stop), the kill switch (HEEL), GROWL, CHEW.

## 5. Final values (for debugging, not for players)

`MODE UNISON (VOICES 3, DETUNE 14 = ±1.2 cents), OSC1 PULSE PW 64 LVL 110, OSC2 PULSE PW 64 SEMI −12 LVL 85, FILTER LP12 CUTOFF 66 (587 Hz) RESO 115 KEY TRK 64 ENV AMT 64 (0), AMP ENV A100 D70 S100 R110, FILTER ENV FA 100 (inert: ENV AMT 0), LFO RANDOM RATE 15 (0.11 Hz) PHASE FREE FILTER 90 (±23.9 st) PITCH 0 PWM 0 AMP 0, VINTAGE 127, SPREAD 127, VOLUME 72 (−17.9 dBFS RMS on the A1 hold, peak −8.0); no echo, spring off (REV MIX 0; SIZE 120 / DAMP 80 are dead values), CHEW 0, GROWL 0, no arp` — `PF_ROTO_SCOPO` in `firmware/src/obv_patches.h`.
