# 16 · Tidal Pull · Chapter II · The Tidal Hexes

*Voiced 6 Nov 2026 (Batch 4A), approved after listening: variant D (the triangle-like oscillator stack). Renders: `reference-renders/16-tidal-pull_D_*.wav` (D is this patch). Log: `../16-tidal-pull.md`.*

## 2. What it sounds like

A stereo chord wash of triangle-like tones (narrow pulses through a low-pass, with an octave-up copy), moved by a slow triangle LFO on pitch. The notes come in gradually, an echo follows each note, and a spring rings behind both. It is a dark patch, not a bright one.

## 3. Gear inspirations (docs only, "inspired by")

- **Roland Juno-60** — *a wash of pulses* (pulses only; the L/R correlation is 0.70 dry and 0.66 with the echo and spring; the pair is 1.6 cents apart and beats 0.6 dB in the A3 band, so "fat" is not supported by the measurements).
- **Fender Twin Reverb** — *springy* (the spring's measured return is in section 4; "bright" is not supported: the centroid is 595 Hz).
- **Roland RE-201 Space Echo** — *wet* (the echo's measured level is in section 4; "drenched" is not measured).

Closest to: **a Juno-60 chord pad through a Twin Reverb spring and a Space Echo**.

Nothing here says the patch matches these: it was built toward the descriptions, by measurement, and approved by ear.

## 4. How to play it

- **It is triangle-like, not a sine, dark, and peak-limited.** Two narrow pulses (PW 25 %), OSC 2 an octave up (+12 st, LEVEL 84, +1.6 cents), through a 12 dB low-pass at 100 % key tracking (CUTOFF 64 = 523 Hz at C4, RESO 0). On OSC 1 through the filter, harmonics 3 / 5 / 7 re the fundamental are −17.2 / −27.3 / −36.8 dB against an ideal triangle's −19.1 / −28.0 / −34.2 (a square: −9.5 / −14.0 / −16.9). Centroid 595 Hz over the note-on region, 0.5 % of its energy above 1.2 kHz, MUD ratio (150 to 400 over 1.2k+) 133. Level: −19.1 dBFS RMS on the wash phrase (VOLUME 76), 1.1 dB under the bank reference and inside ±1.5 dB: the peak is −4.4 dBFS at this level, so it is limited by the peak, not matched to −18.0.
- **Attack (amp envelope, one voice, LFO off):** 10 / 50 / 90 % of the level at 17 / 93 / 219 ms (AA 82; the time table's nominal is 299 ms). Phrase (b), 180 ms stabs, reads −26.8 dBFS RMS, 7.7 dB under the wash phrase: on this phrase, short notes do not reach the level of the held chords.
- **LFO:** triangle, 2.30 Hz (RATE 76), on pitch ±19 cents (LFO PITCH 16; the original 3 was inert, the law is zero below 12), PHASE SPREAD. A one-voice probe reads 10.6 cents s.d., a 32.3 cent 5 to 95 % range at 2.30 Hz. No PWM (LFO PWM 0).
- **Echo:** ALLEY 104 = 337 ms, FEEDBK 78, MIX 110, TONE 100, PINGPONG 127. On an isolated 400 ms E4 the first repeat arrives 337 ms after the note-on; its peak (the end of the repeated note) falls 601 ms after the note-on and is **−8.6 dB re the dry note's peak**. The spring in the same window is −16.3 dB re the note, so **the delay is 7.7 dB above the spring**. The repeats fall 0 / −0.2 / −4.1 / −8.7 / −13.5 / −18.6 dB re the first. The first repeat's centroid is 696 Hz. The echo sits 27 / 10 / 13 dB under the three 400 ms notes of the figure. The spring is after the echo and rings the repeats.
- **Spring (DRAIN 45, SIZE 90, DAMP 35, PRE-DLY 20):** on the isolated E4 its return re the note is −38.8 / −19.1 / −14.4 dB in 0 to 20 / 20 to 100 / 100 to 250 ms. After the first chord's note-off the spring's return re the chord is −6.5 / −8.8 / −11.5 / −18.9 / −37.3 dB and the echo's −5.9 / −6.4 / −7.2 / −11.8 / −21.3 dB (0 to 100 / 100 to 250 / 250 to 500 / 500 to 1000 / 1000 to 2000 ms); after the second chord the spring's −9.4 / −13.3 / −19.3 / −29.2 / −52.5 dB and the echo's −6.2 / −6.8 / −7.7 / −12.5 / −22.0 dB. The tail is 20 dB down at 1216 ms and 40 dB down at 2404 ms; 60 dB is not reached inside the 2.5 s window.
- **The tail's MUD per window** after the first chord: 177 / 407 / 689 in 0 to 250 / 250 to 750 / 750 to 1500 ms, centroids 596 / 571 / 598 Hz at −19 / −24 / −32 dBFS.
- **Width:** the held A minor 7 chord's L/R correlation is 0.70 dry and 0.66 with the echo and spring (side-to-mid −7.6 and −6.7 dB). It is POLY 5, one voice per note. A DUAL, POLY 8 version measured 0.38 on variant B; that was not measured on this patch.
- **Register and gate:** voiced on the wash phrase: A minor 7 (A3 C4 E4 G4) and F major 7 (F3 A3 C4 E4) held 2.0 s, three 400 ms notes (E4 C4 A3), three 100 ms A3+E4 stabs; other registers are untested.
- **First play after power-on:** the program-load render differs from the render built over INIT: −24.0 dB (wash phrase) and −28.0 dB (stabs) relative to the signal; both loaded from INIT they are bit-identical. The cause is not isolated.
- **Costs:** about 2027 host instr/sample worst case (idle 1180 + 847 under load). The device build was not run and the device render time is not measured.
- **Tricks:** untested on this patch: the SLOBBER slop ride, SEQ held (Tape Stop), the kill switch (HEEL), GROWL, CHEW.

## 5. Final values (for debugging, not for players)

`MODE POLY (POLY 5), OSC1 PULSE PW 32 (25 %) LVL 110, OSC2 PULSE PW 32 SEMI +12 FINE 66 (+1.6 cents) LVL 84, CUTOFF 64 (523 Hz at C4), RESO 0, ENV AMT 64 (0), KEY TRK 127, FILTER LP12, AMP ENV A82 D70 S127 R92, LFO TRI RATE 76 (2.30 Hz) PHASE SPREAD PITCH 16 (±19 cents) PWM 0 AMP 0, VINTAGE 50, SPREAD 127, VOLUME 76 (−19.1 dBFS RMS on the wash phrase, peak −4.4); DLY MIX 110 (ALLEY 104 = 337 ms, FEEDBK 78, TONE 100, PINGPONG 127), DRAIN 45, SIZE 90, DAMP 35, PRE-DLY 20; CHEW 0, GROWL 0, no arp` — `PF_TIDAL_PULL` in `firmware/src/obv_patches.h`.
