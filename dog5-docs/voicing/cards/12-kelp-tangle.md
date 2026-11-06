# 12 · Kelp Tangle · Chapter II · The Tidal Hexes

*Voiced 6 Nov 2026 (Batch 4A), approved after listening: variant C (CUTOFF 98) of Batch 4A. Renders: `reference-renders/12-kelp-tangle_C_*.wav` (C is this patch). Log: `../12-kelp-tangle.md`.*

## 2. What it sounds like

A two-pulse pad whose pulse widths are swept slowly and steadily by one triangle LFO, through a 24 dB low-pass that leaves little above 1.2 kHz, with a spring tail behind it. The sweep is measurable on held notes; on short notes only a slice of it is heard. No LFO pitch vibrato and no echo are set (VINTAGE 50 still adds the usual slop).

## 3. Gear inspirations (docs only, "inspired by")

- **Moog Prodigy** — *dark, raw, murky* (dark: the held A2's centroid is 531 Hz; raw and murky are not measured as such).
- **Fender spring reverb tank** — *springy* (the tail's measured return is in section 4).
- **Roland Juno-60** — *PWM, wobble, thick* (PWM: measured; the LFO is on the pulse widths only, there is no pitch wobble; thick is not measured).
- **Korg Polysix** — *fat, PWM* (PWM: measured; fat is not measured).

Closest to: **a Polysix PWM pad into a spring tank**.

Nothing here says the patch matches these: it was built toward the descriptions, by measurement, and approved by ear.

## 4. How to play it

- **What C measured (held A2, dry, after the filter):** the PWM moves the band energies by 10.1 dB in 150 to 400 Hz, 7.6 dB in 400 to 1.2k and 7.4 dB in 1.2k to 3k (95th to 5th percentile of 23 ms frames); the level itself moves 5.7 dB (5.9 dB with the spring). The strongest modulation is 0.9 Hz in 150 to 400 Hz and 1.6 Hz in 400 to 1.2k; the LFO runs at 1.03 Hz (triangle, RATE 60) and sweeps the pulse widths 18 to 48 % (±15.2 points around 33 %, one side of 50 %). On the held chord A2 E3 C4 the depths are 9.0 / 6.4 / 5.6 dB and the level moves 4.3 dB.
- **Cutoff 98:** a 24 dB low-pass at 100 % key tracking, CUTOFF 98 = 3729 Hz at C4, RESO 30. Held A2: centroid 531 Hz, 0.8 % of its energy above 1.2 kHz; held chord: centroid 879 Hz, 3.5 % above 1.2 kHz; note-on region MUD ratio (150 to 400 over 1.2k+) 12.3. The rendered variant B (CUTOFF 86) measured 339 Hz and 540 Hz and a note-on MUD of 38.8.
- **Spring (DRAIN 55, SIZE 75, DAMP 30, PRE-DLY 20):** its return re the dry chord after the chord's note-on is −47.1 / −12.8 / −5.9 dB in 0 to 20 / 20 to 100 / 100 to 250 ms (on the held A2: −40.5 / −18.7 / −19.0). After the chord's note-off it is −7.5 / −12.9 / −33.8 dB re the chord in 0 to 250 / 250 to 750 / 750 to 1500 ms. The tail is 20 / 40 / 60 dB down at 632 / 1100 / 1426 ms after the chord (DC out), and 60 dB down at 978 ms after the held A2 and 1054 ms after the short-note figure.
- **The tail's MUD per window:** 10.3 / 15.0 / 77.2 in 0 to 250 / 250 to 750 / 750 to 1500 ms after the chord, with centroids 921 / 927 / 1565 Hz at −20 / −31 / −52 dBFS (variant B: 29 / 39 / 180). The spring is fed the filtered voice; this suggests the tail has little more top than the voice.
- **Honest limits:** (1) one shared LFO moves both oscillators' pulse widths at one rate; there is no Poly-Mod in the engine, so a modulator with its own pitch or envelope was not possible. (2) The PWM depth in 150 to 400 Hz tops out near 10 dB on this patch: 10.0 to 10.3 dB at LFO PWM 60 to 115 and at CUTOFF 78 to 104 (measured on variant B); per-voice DRIVE raised it to 12.5 to 12.7 dB but cut the level swing to 3.4 to 3.7 dB. (3) Short notes: on three 150 ms notes the PWM moves 2.2 dB in 150 to 400 Hz, 1.5 dB in 400 to 1.2k and 1.9 dB in level; the sweep is one second long. The PWM is a held-note effect.
- **Sweep start:** LFO PHASE SYNC restarts the LFO on each detached note (the engine's code; not measured in audio here), so a short note begins at the same width every time.
- **Register and polyphony:** voiced on a held A2 (3.2 s), the chord A2 E3 C4 (3 s) and six 150 ms notes (A2 to A3); other registers are untested. POLY 5, one voice per note.
- **Envelope:** the amp attack reaches 10 / 50 / 90 % at 3 / 11 / 23 ms (AA 52).
- **Level:** −18.0 dBFS RMS on the tangle phrase (VOLUME 74, note-on region, spring included, tails excluded); phrase (b) −17.0; peak −5.3 dBFS; crest factor 12.7 dB.
- **Program-load check:** the program-load render and the render built over INIT are bit-identical, from the boot patch and from INIT.
- **Costs:** about 2042 host instr/sample worst case (idle 1164 + 878 under load). The device build was not run and the device render time is not measured.
- **Tricks:** untested on this patch: the SLOBBER slop ride, SEQ held (Tape Stop), the kill switch (HEEL), GROWL, CHEW, ALLEY.

## 5. Final values (for debugging, not for players)

`MODE POLY (POLY 5), OSC1 PULSE PW 42 (33 %) LVL 110, OSC2 PULSE PW 42 FINE 73 (+7.0 cents) LVL 100, CUTOFF 98 (3729 Hz at C4), RESO 30, ENV AMT 64 (0), KEY TRK 127, FILTER LP24, AMP ENV A52 D70 S127 R88, LFO TRI RATE 60 (1.03 Hz) PHASE SYNC PWM 100 (±15.2 points) PITCH 0 AMP 0, VINTAGE 50, SPREAD 100, VOLUME 74 (−18.0 dBFS RMS on the tangle phrase, peak −5.3); DRAIN 55, SIZE 75, DAMP 30, PRE-DLY 20; DLY MIX 0, CHEW 0, GROWL 0, no arp` — `PF_KELP_TANGLE` in `firmware/src/obv_patches.h`.
