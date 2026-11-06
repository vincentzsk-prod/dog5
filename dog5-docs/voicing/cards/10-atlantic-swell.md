# 10 · Atlantic Swell · Chapter II · The Tidal Hexes

*Voiced 6 Nov 2026 (Batch 4A), approved after listening: variant A, the starting point unchanged. Renders: `reference-renders/10-atlantic-swell_A_*.wav` (A is this patch). Log: `../10-atlantic-swell.md`.*

## 2. What it sounds like

A bright pair of narrow pulse waves through a notch filter, played polyphonically, with a spring reverb behind it and nothing else. It has no vibrato, no chorus and no delay (measured, below). The pulses beat slowly against each other, and the spring rings on after the notes.

## 3. Gear inspirations (docs only, "inspired by")

- **Farfisa Compact** — *nasal* (the approved trait; not measured here).
- **Vox Continental** — *reedy, bright* (bright: the note-on region's centroid is 5369 Hz and 23 % of its energy is above 1.2 kHz; reedy is not measured here).
- **Fender spring reverb** — *springy* (the spring's measured return is in section 4).

Closest to: **a combo organ into a spring tank**.

Nothing here says the patch matches these: the traits are the approved descriptions, and only the ones marked as measured have a number behind them.

## 4. How to play it

- **Register and gate:** it was voiced on the organ phrase: an A minor triad (A3 C4 E4) held 2.4 s, one 120 ms E4, four 120 ms notes (E4 G4 A4 C5) and a D minor triad (D4 F4 A4) held 1.6 s. Other registers are untested. Polyphony is POLY 5; chords of more than five notes were not tried.
- **What it does not have, measured:** no vibrato (LFO PITCH 0; a one-voice probe reads 0.0 cents of pitch wander), no delay (DLY MIX 0; the delay's return is below −180 dB re the note), no chorus (no pitch modulation and no left/right voice pair; the held chord's L/R correlation is 0.78 dry, 0.70 with the spring). Versions with a chorus, a rotary-speaker tremolo and a heavy echo were rendered (B, C and D, on the listen branch) and are not this patch.
- **The beating:** OSC 1 is a 16 % pulse and OSC 2 an 85 % pulse (a near-inverse of the first) 9.4 cents sharp. On the held A minor chord (dry) the A3 band's envelope swings 17.9 dB at a mean 1.01 Hz (0.67 to 1.18); the chord's level moves 5.7 dB (95th to 5th percentile of 20 ms RMS). On a held A2, the 150 to 400 Hz band moves 14.2 dB at 1.2 Hz; with LFO PWM at 0 it is the same 14.2 dB, and with OSC 2's detune also removed it is 1.0 dB: this suggests the movement is the pair beating, not the PWM.
- **The PWM is not audible as PWM:** the LFO (triangle, 0.37 Hz, PHASE SPREAD) moves the pulse widths ±2.3 points; the band movement above is unchanged with it off.
- **Tone, as measured:** centroid 5369 Hz over the note-on region; energy split below 60 / 60 to 150 / 150 to 400 / 400 to 1.2k / above 1.2 kHz = 0 / 0 / 57 / 20 / 23 %; MUD ratio (150 to 400 over 1.2k+) 2.5 over the note-on region and 2.2 / 2.5 / 3.0 in the spring tail's windows 0 to 250 / 250 to 750 / 750 to 1500 ms (the tail's centroids 5511 / 5350 / 5178 Hz at −21 / −29 / −40 dBFS). "Cold" and "crisp" were not measured and are not claimed.
- **Envelope:** the amp attack (one voice) reaches 10 / 50 / 90 % of its level at 6 / 29 / 61 ms (AA 70); the release is AR 100. After the held chord's note-off the tail is 20 dB down at 880 ms and 40 dB down at 1700 ms (DC out; 60 dB is not reached inside the 2 s window; the same render with the spring off: 790 and 1678 ms).
- **Spring:** DRAIN 40, SIZE 100. On an isolated E4 the spring's return re the note is −43.4 / −19.0 / −13.2 dB in 0 to 20 / 20 to 100 / 100 to 250 ms. After the held chord's note-off it is −13.2 / −15.5 / −19.3 / −25.3 / −38.7 dB re the chord in 0 to 100 / 100 to 250 / 250 to 500 / 500 to 1000 / 1000 to 2000 ms. Under the four staccato notes the spring's return is −21.0 / −13.1 / −0.8 / −0.4 dB re each note: the last two are as loud as the notes.
- **Level:** −19.0 dBFS RMS on the organ phrase (VOLUME 100, note-on region, spring included, tails excluded; the bank reference is −18.0 ± 1.5); phrase (b) −17.6; peak −4.8 dBFS over the whole renders (−6.2 on the organ phrase); crest factor 12.8 dB.
- **First play after power-on:** the program-load render differs from the render built over INIT: −25.3 dB (organ phrase) and −23.4 dB (stabs) relative to the signal; both loaded from INIT they are bit-identical. The cause is not isolated.
- **Costs:** about 2020 host instr/sample worst case (idle 1164 + 856 under load). The device build was not run and the device render time is not measured.
- **Tricks:** untested on this patch: the SLOBBER slop ride, SEQ held (Tape Stop), the kill switch (HEEL), GROWL, CHEW, ALLEY.

## 5. Final values (for debugging, not for players)

`MODE POLY (POLY 5), OSC1 PULSE PW 20 (16 %) LVL 110, OSC2 PULSE PW 108 (85 %) SEMI 0 FINE 76 (+9.4 cents) LVL 100, CUTOFF 70 (740 Hz at C4), RESO 20, ENV AMT 64 (0), KEY TRK 64, FILTER NOTCH, AMP ENV A70 D70 S100 R100, LFO TRI RATE 40 (0.37 Hz) PHASE SPREAD PWM 40 (±2.3 points) PITCH 0 AMP 0, VINTAGE 30, SPREAD 100, VOLUME 100 (−19.0 dBFS RMS on the organ phrase, peak −4.8); DRAIN 40, SIZE 100, DAMP 60, PRE-DLY 20; DLY MIX 0, CHEW 0, GROWL 0, no arp` — `PF_ATLANTIC_SWELL` in `firmware/src/obv_patches.h` (the values of the old `PF_HOLLOW_PAD`).
