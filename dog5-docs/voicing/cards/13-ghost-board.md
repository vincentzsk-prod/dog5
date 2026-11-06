# 13 · Ghost Board · Chapter II · The Tidal Hexes

*Voiced 6 Nov 2026 (Batch 4B, round 2), approved after listening: variant C2 of round 2. Renders: `reference-renders/13-ghost-board_C2_*.wav` (C2 is this patch). Log: `../13-ghost-board.md`.*

## 2. What it sounds like

A dark pad: a pair of slightly detuned pulse waves, played polyphonically, beating slowly against each other, with a long echo and a heavy spring behind every note. It is the original patch's voice, unchanged, with the pulse-width movement removed and no tape deck. By the dictionary's ratio it is very muddy.

## 3. Gear inspirations (docs only, "inspired by")

- **Roland RE-201 Space Echo** — *wet*. The echo is 337 ms (ALLEY 104), FEEDBK 95, MIX 105. On an isolated 150 ms E4 the first repeat arrives 337 ms after the note-on, peaks 460 ms after it and is −8.7 dB re the note's peak, with the echo 10.3 dB above the spring in that window; the repeats fall 0 / −3.0 / −6.0 / −9.1 / −12.3 / −15.6 dB re the first. After the held chord's note-off the echo's return is −5.6 / −6.1 / −6.2 / −9.4 / −16.0 dB re the chord in 0 to 100 / 100 to 250 / 250 to 500 / 500 to 1000 / 1000 to 2000 ms.
- **Fender spring reverb tank** — *springy*. DRAIN 70, SIZE 100, DAMP 25, PRE-DLY 20. After the held chord's note-off the spring's return is +6.1 / +3.2 / −2.1 / −9.2 / −26.5 dB re the chord in the same windows (louder than the chord for its first 250 ms or so); on the isolated E4 it is −39.3 / −12.9 / −12.3 dB re the note in 0 to 20 / 20 to 100 / 100 to 250 ms.
- **Mellotron M400** — the reference for the tone that was being chased. Measured traits only: **dark** (the note-on region's centroid is 562 Hz, 0.2 % of its energy is above 1.2 kHz, MUD ratio 314.9) and **a slow beating between the two oscillators**: on one held voice the 150 to 400 Hz band moves 13.6 dB at 0.9 Hz (6.2 dB at 0.9 Hz on the held chord); with OSC 2's detune removed (the rendered variant D2) that movement was 0.3 dB, with the pulse-width movement removed it stays. **"Warped, wobbly tape" and "soft flute-like tone" are NOT in this patch:** the tape deck is off (CHEW 0), and harmonics 3 / 5 / 7 re the fundamental read −11 / −18 / −26 dB against an ideal triangle's −19 / −28 / −34.

Closest to: **a dark Mellotron voice through a Space Echo and a spring tank**.

Nothing here says the patch matches these: the traits are the approved descriptions, and only the ones with a number behind them are measured.

## 4. How to play it

- **What changed from the original brief.** The original brief was a filtered near-sine with maximum tape wow and flutter. After listening the tape deck was dropped (CHEW 0), and the pulse-width movement was removed (LFO PWM 0). The patch has no tape wobble (a one-voice probe reads 0.0 cents of pitch wander) and no near-sine tone. The echo and spring are those of an earlier round's variant D.
- **Very muddy, by the numbers.** MUD ratio (150 to 400 Hz over 1.2 kHz and up): 314.9 over the note-on region (energy split below 60 / 60 to 150 / 150 to 400 / 400 to 1.2k / above 1.2 kHz = 0 / 0 / 74.5 / 25.3 / 0.2 %); in the tail after the held chord 1108 / 2198 / 3331 in 0 to 250 / 250 to 750 / 750 to 1500 ms (centroids 488 / 509 / 528 Hz at −15 / −19 / −26 dBFS). The benchmark of 10 to 40 (note-on) and about 80 (tail windows) is far exceeded; the original patch measured 108 over the note-on region.
- **The movement.** One held voice (A3, echo and spring off): the 150 to 400 Hz band moves 13.6 dB at 0.9 Hz, the 400 to 1.2k band 1.2 dB, the broadband level 9.0 dB. LFO PWM is 0; the LFO (triangle, RATE 50 = 0.62 Hz, PHASE SPREAD) has no destination. LFO PITCH is 0 (the original 3 was inert: the two renders are bit-identical).
- **Register and gate:** voiced on the ghost phrase: the A minor 7 chord (A3 C4 E4 G4) held 2.4 s, a slow line of four 800 ms notes (E4 D4 C4 A3), and six 150 ms notes. Other registers are untested. POLY 5; chords of more than four notes were not tried.
- **Envelope:** the amp attack (one voice) reaches 10 / 50 / 90 % of its level at 3 / 14 / 27 ms (AA 60); release AR 90. The tail after the held chord is 20 dB down at 1686 ms (40 dB is not reached inside the 2.5 s window).
- **Under the short notes:** the echo's return is −18.0 / −16.8 / −8.6 / −8.7 dB re each of the figure's first four 150 ms notes; the spring's is −7.5 / −12.7 / −2.4 / +3.1 dB.
- **Width:** the held chord's L/R correlation is 0.81 dry and 0.84 with the echo and spring.
- **Level:** −18.0 dBFS RMS on the ghost phrase (VOLUME 55; the bank reference is −18.0 ± 1.5; note-on region, echo and spring included, tails excluded); peak −4.9 dBFS; crest factor 13.1 dB. Phrase (b) reads −23.4 dBFS RMS (5.4 dB under the ghost phrase), peak −11.7 dBFS.
- **First play after power-on:** in the host render the program-load render and the render built over INIT are bit-identical, both from INIT and from the boot patch. (The earlier variant A2, which still had the pulse-width LFO, differed from the boot patch by −33.2 dB on the stabs and −40.7 dB on the ghost phrase; this suggests the free-running LFO's phase at program load, not isolated.)
- **Costs:** about 2084 host instr/sample worst case (idle 1180 + 905 under load). The device build was not run and the device render time is not measured.
- **Tricks:** untested on this patch: the SLOBBER slop ride, SEQ held (Tape Stop), the kill switch (HEEL), GROWL, CHEW, the other LFO shapes.

## 5. Final values (for debugging, not for players)

`MODE POLY (POLY 5), OSC1 PULSE PW 64 (50 %) LVL 110, OSC2 PULSE PW 40 (31 %) SEMI 0 FINE 73 (+7.0 cents) LVL 100, CUTOFF 75 (988 Hz at C4), RESO 5, ENV AMT 74 (+10), KEY TRK 64, FILTER LP24, FILTER ENV A50 D70 S40 R60, AMP ENV A60 D70 S100 R90, LFO TRI RATE 50 (0.62 Hz) PHASE SPREAD PWM 0 PITCH 0 AMP 0, VINTAGE 50, SPREAD 100, VOLUME 55 (−18.0 dBFS RMS on the ghost phrase, peak −4.9); DLY MIX 105 (ALLEY 104 = 337 ms, FEEDBK 95, TONE 70, PINGPONG 127), DRAIN 70, SIZE 100, DAMP 25, PRE-DLY 20; CHEW 0, GROWL 0, no arp` — `PF_GHOST_BOARD` in `firmware/src/obv_patches.h`.
