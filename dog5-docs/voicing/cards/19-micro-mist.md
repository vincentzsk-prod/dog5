# 19 · Micro-mist · Chapter III · The Bakshi Tomes

*Voiced 6 Nov 2026 (Batch 5A), approved after listening: variant D, "tunnel" (Vincent: "sounds incredible, exactly what I was imagining"). Renders: `reference-renders/19-micro-mist_D_*.wav`. Log: `../19-micro-mist.md`. Slot 19 was Blackwater until the same day; that patch was dropped.*

## 2. What it sounds like

A soft-attack chord in the mid-to-upper register: a saw with a slightly sharp square an octave above it, through a band-pass filter. It hovers on its own echo and a large spring, and keeps hanging in the air for several seconds after you let go. It is bright rather than low, and it does not flicker or scatter: it is a held pad dissolving into its effects, not a granular texture.

## 3. Gear inspirations (docs only, "inspired by")

- **Hologram Microcosm** — *the Haze, Glide and Tunnel of its Granules and Micro Loop banks; Wash, Wet, Drifting.* Wash: the L/R correlation falls from 0.79 dry to 0.43 with the echo and spring (measured). Wet: the tail takes 5788 ms to fall 60 dB (measured). Drifting: not measured (the LFO does nothing at these values). The patch is not a granular looper (see section 4).
- **Yamaha CS-80** — *the Blade Runner pad voice; Soft, Swelling.* Soft: a 150 ms tap reads 8.7 dB under the held level because of the slow attack (AA 80, 256 ms nominal), measured. Swelling: the chord's level rises from −20.1 dBFS over the first second to −17.9 over the second (measured, a 2.2 dB rise); a longer swell was not measured.
- **Roland Jupiter-8** — *the bright top; Bright, Beating.* Bright: centroid 2300 Hz with 39 % of the energy over 1.2 kHz in the settled hold (measured; no comparison with the original was made). Beating: the A3 band swings only 0.4 dB at 3.7 Hz (measured, weak).

Closest to: **a CS-80 pad dissolved in a Microcosm Haze wash**.

Nothing here says the patch matches these: it was built toward the descriptions, by measurement, and approved by ear.

## 4. How to play it

- **Chords work.** POLY with 6 voices, one per note. POLY is not MONO or UNISON, so the no-retrigger rule for legato does not apply (engine fact; not tested on this patch). Best in the mid-to-upper register: judged on A3 C#4 E4 (held 10 s) and a single A4.
- **The mist after the key-up is the effect tail, not a latch.** There is no Drone Latch: a held chord needs the key or a sustain pedal. After a 10 s chord the tail is 20 / 40 / 60 dB down at 1596 / 4132 / 5788 ms (the dry voice alone: 734 / 1304 / 1730 ms). After a 150 ms chord tap the tail is 20 dB down at 2280 ms; 40 dB is not reached inside the 4.5 s window.
- **Echo and spring.** ALLEY 100 = 294 ms, FEEDBK 105, TONE 100, MIX 95, PINGPONG 127; spring DRAIN 80, SIZE 110, DAMP 20, PRE-DLY 10. On an isolated 300 ms A4 the first repeat is −9.6 dB re the note and **3.9 dB under the spring: the spring leads the echo**. The repeats re the first: 0 / +1.6 / +0.2 / −1.5 / −3.4 / −5.3 / −7.6 / −9.9 dB; **14 of 14 repeats are above −40 dB, so this measure is saturated** (a longer window would count more). The spring is after the echo and rings the repeats.
- **Attack and taps.** A 150 ms chord tap reads 8.7 dB under the held level (centroid 2566 Hz); a 150 ms A4 tap 13.4 dB under. The slow attack makes short notes quiet.
- **Where the energy is.** Settled chord (4 to 10 s): centroid 2300 Hz, energy under 150 Hz 0 %, 150 to 400 Hz 8 %, 400 to 1.2k 54 %, over 1.2k 39 %. At the strike (first second): centroid 2403 Hz, 0 / 6 / 61 / 33 %. A single A4, settled: centroid 3023 Hz, 0 / 0 / 55 / 45 %. Nothing sits under 150 Hz.
- **Width.** L/R correlation (150 to 4000 Hz) of the settled chord: 0.79 dry, 0.43 with the echo and spring (side-to-mid −9.1 dB dry, −3.9 dB full).
- **The LFO is set but inert at these values.** It is S&H at 9.91 Hz, PHASE SPREAD, but FILTER 10 is below the filter law's floor (0.0 st), PITCH is 0 and AMP is 0, so it adds no flicker, scatter or grain. The 4.5 dB swing measured in the filter band (at 2.3 Hz) comes from the beating of the voices and the echo, not from the LFO. Raising LFO FILTER or PITCH would make the LFO act (not tested on this patch).
- **Level and cost.** VOLUME 96: −17.95 dBFS RMS over +4 s to +10 s of the held chord (K-weighted −16.3). The chord peaks at −4.7 dBFS (the peak of the tap −9.8, the A4 single −9.8, the riff −13.7, the stabs −8.5); no clipped sample. About 2000 host instr/sample worst case (idle 1179 + 821 under load); the device render time is not measured.
- **Limits.** **Not a real granular engine:** no grains, no freeze (the nearest is high feedback, a decaying hover), no reverse, no pitch-shifted repeats (the repeats are copies of the note), and the BBD time has no LFO, so there is no chorus from the delay. Stabs and low notes are not what it is for: phrase (b) stabs read −24.9 dBFS RMS, and the patch has nothing under 150 Hz.
- **Tricks:** untested on this patch: SLOBBER, SEQ held (Tape Stop), the kill switch (HEEL), GROWL, CHEW (CHEW is off).

## 5. Final values (for debugging, not for players)

`MODE POLY (POLY 6), OSC1 SAW LVL 127, OSC2 PULSE PW 64 SEMI +12 FINE 72 (+6.2 cents) LVL 100, FILTER BP12 CUTOFF 70 (740 Hz) RESO 40 KEY TRK 64 ENV AMT 74 (+10), FILTER ENV A75 D90 S90 R60, AMP ENV A80 D100 S127 R95, LFO S&H RATE 105 (9.91 Hz) PHASE SPREAD FILTER 10 (0.0 st) PITCH 0 PWM 0 AMP 0, VINTAGE 40, SPREAD 100, VOLUME 96 (−17.95 dBFS RMS on the held chord, chord peak −4.7); BBD ALLEY 100 (294 ms) FEEDBK 105 TONE 100 MIX 95 PINGPONG 127, DRAIN 80, SIZE 110, DAMP 20, PRE-DLY 10; CHEW 0, GROWL 0, no arp` — `PF_MICRO_MIST` in `firmware/src/obv_patches.h`.
