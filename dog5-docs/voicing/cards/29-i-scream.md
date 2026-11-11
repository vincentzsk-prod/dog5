# 29 · i scream · Chapter IV · The Ancient Relics

*Voiced 11 Nov 2026 (Batch 6A2), approved: variant D with CHEW 0 (Vincent: "29 D, but take off the CHEW completely"). **This exact version was not heard before approval**: Vincent heard D with the tape on and approved it without it; the reference renders are how he checks it. Renders: `reference-renders/29-i-scream_D_*.wav`. Tables (on the voicing branch): `listen/voicing/batch-06a2/29/README.md` (variant `Dfinal`).*

## 2. What it sounds like

A bright, struck chime built from a square wave with a second oscillator that zings down in pitch at the strike. The ring decays slowly, over a couple of seconds, and a gentle slow shimmer in pitch and level fades in after the strike and sways the ring. A small slap echo and a touch of spring sit behind it, and everything passes through a narrow, honky mid-band like a small horn speaker. There is no tape in it.

## 3. Gear inspirations (docs only, "inspired by")

- **Yamaha DX7 (tubular-bells voice)** — *FM clang, inharmonic.* OSC 2 sits +15 semitones above OSC 1 (a ratio of 2.38) with X-MOD 25. Through the filter that partial reads −34 dB under the note at C#6 and −18 dB at C#5 (measured, first 100 ms); the strongest partial after the note is the square's third harmonic at −15 dB (C#6). So it is faint at the top of the keybed. "Clang" is not measured.
- **A music box, struck** — *fast-decay, nostalgic.* Not carried: the ring takes 1896 ms to fall 40 dB at C#6 (measured), a long ring, not a fast decay. "Nostalgic" is Vincent's word and is not measured.
- **Finger cymbals (zills)** — *bright metallic ping.* The centroid over the first 20 ms is 2096 Hz at C#6 and 1958 Hz at C#5 (measured). "Metallic" is not measured.
- **A transistor radio or van horn speaker** — *band-limited, honky, lo-fi.* The filter read with white noise peaks at 1099 Hz, with a −3 dB width of 898–1345 Hz; 0.4 % of its energy is under 400 Hz and 4.1 % above 4 kHz (measured). On the chime melody through the whole patch: 0.0 % under 400 Hz, 0.45 % above 4 kHz, centroid 1262 Hz. "Lo-fi" is not measured.

Closest to: **a music-box chime played through a cheap van horn speaker**.

The reference for the register was Vincent's two phone recordings of a real ice-cream van: the chimes sit in a narrow band centred about C#6 (about 1110 Hz), notes about 580 ms apart. **Those measurements of the recordings were rough** (speaker, street and engine are in them), and the van chime's own spectrum is not known, so the partials above were measured on this patch, not copied from the recordings. Nothing here says the patch matches the gear or the van: it was built toward the descriptions, by measurement, and approved by ear (with the tape on).

## 4. How to play it

- **Register:** voiced for A4 to A6. RMS over the first 300 ms of one struck note, with the centroid over the first 100 ms: A4 −22.1 dB / 1950 Hz, C#6 −18.5 dB / 2183 Hz, A6 −20.1 dB / 2563 Hz (measured). A4 sits 3.6 dB under C#6 and A6 1.6 dB under it; neither end falls away in that range. Nothing outside A4–A6 was measured.
- **Ring and overlap:** the ring of a C#6 falls 6 / 12 / 20 / 40 dB in 252 / 550 / 1030 / 1896 ms (the whole patch; 276 / 584 / 938 / 1943 ms at C#5; the voice alone reads 1954 ms to −40 dB at C#6). With notes 580 ms apart several rings overlap. POLY 5 is set; POLY 4, 5 and 6 against POLY 8 change the level of what rings by at worst −0.1, −0.6 and −0.7 dB on the melody, −0.2 to −0.3 dB on the fast run's tail and 0.0 dB on the chord, so no cut ring is measurable (random oscillator start phases make a sample-for-sample comparison useless; not isolated whether stolen voices were the oldest).
- **Chord:** three notes struck together (A#5 C#6 F6) play whole on POLY 5 and are the loudest thing in the phrase set: RMS −21.3 dB over the chord's note-on region, peak −4.06 dBFS. Use it as a wind-chime.
- **Fast run:** eight 120 ms notes 160 ms apart (C6 up to G6 and back) read −16.6 dB RMS with a peak of −9.9 dBFS, no clip.
- **Shimmer:** a TRI LFO (the stock preset it was voiced from uses a sine, which this engine does not have): 0.8 Hz, pitch ±9.4 cents by the law, amp 40, delay 40, PHASE SYNC so every note starts it the same way. It fades in after the strike (by the engine's law the LFO is held at its centre for about 0.5 s and then ramped in; the delay was not measured separately). On a one-voice sustained probe the pitch wobble reads 5.1 cents s.d. (−8.2 to +8.3 cents, strongest component 0.80 Hz) and the level swings 2.8 dB; this is the LFO alone, as there is no tape. "Dreamy" and "ethereal" are Vincent's words and are not measured.
- **Echo and spring:** a 65 ms slap (FEEDBK 22, MIX 35) and a trace of spring (DRAIN 18). On a C#6 held 400 ms their return against the dry note is −28.7 / −15.0 / −12.8 dB in the windows 0–20 / 20–100 / 100–250 ms after the strike (measured).
- **No tape:** CHEW is 0 (a bit-exact bypass), so there is no wow, flutter, hiss or dropout. **Changed from the brief:** the brief called for tape wobble; Vincent removed it after hearing variant D, which had CHEW 65. HISS 25 and DROPS 20 are still stored but have no effect at CHEW 0; the front edge is the same with CHEW 0 as set (2096 / 1958 Hz at C#6 / C#5, against 1933 / 1768 Hz on the tape-on D).
- **Level and cost:** VOLUME 113, −17.9 dBFS RMS over the note-on region of the chime melody (K-weighted −16.6), peak −4.06 dBFS over every audition phrase (the chord); the standard stabs phrase (b) reads −21.8 dBFS. **CPU 1863 host instr/sample worst case** (idle 1179, load 685), against 2647 for the same patch with CHEW 65. The device render time is not measured.
- **Tricks:** SLOBBER rides a pitch drift, SEQ held (Tape Stop), the kill switch (HEEL): untested on this patch.
- **Changed from the brief:** the original VALHALLA array and round 1's PWM wash are retired; this is a new patch with a new name. The original brief is kept in `DOG-5-presets.md`.

## 5. Final values (for debugging, not for players)

`MODE POLY (POLY 5), OSC1 PULSE PW 50 % LEVEL 127, OSC2 SAW LEVEL 70 SEMI +15 FINE 0 X-MOD 25 ENV>O2 76 (+4.6 st at the envelope's top), FILTER BAND-PASS 12 dB CUTOFF 77 RESO 105 KEY TRK 0 ENV AMT 0 DRIVE 30, FILTER ENV A0 D50 S0 R30, AMP ENV A0 D101 S0 R50, LFO TRI RATE 55 PHASE SYNC PITCH 14 AMP 40 DELAY 40, VINTAGE 10, SPREAD 70, BBD ALLEY 56 (65 ms) FEEDBK 22 TONE 60 MIX 35 PINGPONG 127, spring SIZE 40 DAMP 40 PRE-DLY 8 DRAIN 18, CHEW 0 (WOW/FLT 64, HISS 25, DROPS 20 inert), GROWL 0, VOLUME 113` — `PF_I_SCREAM` in `firmware/src/obv_patches.h`.
