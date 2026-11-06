# 14 · Reef Break · Chapter II · The Tidal Hexes

*Voiced 6 Nov 2026 (Batch 4B), approved after listening: round-1 variant C (the quick swell). Renders: `reference-renders/14-reef-break_C_*.wav` (C is this patch). Log: `../14-reef-break.md`.*

## 2. What it sounds like

A crash made of a burst of noise over a square-wave sub. The noise swells in quickly rather than starting instantly, the lows fall away first and the top of the noise rings out longest, and a long echo follows each hit. There is no spring.

## 3. Gear inspirations (docs only, "inspired by")

- **Roland TR-808** — *thick sub*. The sub-only hit's first 150 ms: on A1 41 % of the energy is under 60 Hz and 28 % in 60 to 150 Hz (an A1 fundamental is 55 Hz); on A2 71 % is in 60 to 150 Hz. The sub's 40 to 150 Hz band is 20 / 40 dB down 174 / 290 ms after its peak. "Booming" is not measured.
- **Simmons SDS-V** — *noise burst*. In the first 100 ms the noise is 4.7 dB over the sub on A1 (3.5 dB on A2). The amp attack of the hit (voice alone, 10 / 50 / 90 % of the peak): A1 2.2 / 8.7 / 27.2 ms with the peak at 27.4 ms; A2 2.7 / 12.2 / 32.2 ms, peak at 32.2 ms. "Crashing" is supported only by the band decay below.
- **Roland RE-201 Space Echo** — *long repeats* (only that): ALLEY 106 = 361 ms, FEEDBK 100, MIX 80. On an isolated hit the first repeats are −13 / −18 / −24 / −28 / −31 / −35 dB re the burst's peak and 7 repeats stay above −40 dB; the echo stays below clipping (peak of the isolated hit with echo −5.3 dBFS, no clipped sample).

Closest to: **an 808 kick with a noise burst into a Space Echo**.

Nothing here says the patch matches these: it was built toward the descriptions, by measurement, and approved by ear.

## 4. How to play it

- **Register and gate:** voiced on the crash phrase: one low hit (A1), one mid hit (A2), and A1 hits 1000, 600 and 400 ms apart, every gate 300 ms, velocity 108. Other registers are untested. POLY 5.
- **The decay (A1 hit, voice alone):** each band's time from its own peak to −20 / −40 dB: 60 to 150 Hz 78 / 250 ms; 150 to 400 Hz 206 / 276 ms; 400 to 1.2k 244 / 279 ms; 1.2k to 4k 316 / 856 ms; **4k and up 665 / 1329 ms** (on A2: 4k and up 702 / 1402 ms). The top bands ring out longer than the sub and the lows. How: one 12 dB high-pass, CUTOFF 100 (4186 Hz at C4), whose cutoff is pushed far down at the strike by ENV AMT 0 (about −97 semitones at the envelope's peak) and climbs back as the filter envelope falls (FD 100); the amp envelope (AD = AR = 97) sets the ring-out.
- **Peak behaviour.** Own-phrase peak −4.5 dBFS (a second noise seed: −4.3), crest factor 13.5 / 13.7 dB, 2 % of samples within 10 % of the rail, no clipped sample. The second seed is a quiet note struck first, so the hits land on other voices' noise generators. **Near-rail warning: phrase (b), which strikes three keys at once, stacks three noise voices and reads −12.8 dBFS RMS with a peak of −1.55 dBFS (seed 2: −1.52), on the three-key stab E2 B2 E3: 1.5 dB under full scale, no clipped sample and none within 1 dB of full scale.**
- **Level:** −18.0 dBFS RMS on the crash phrase (VOLUME 121; the bank reference is −18.0 ± 1.5), the note-on region being the 300 ms gates of the 11 hits (the burst and about the first 250 ms of its decay, echo included; the release, the rest of the decay and the tails excluded).
- **The echo against the dry tail.** The dry voice (sends off) is 20 / 40 dB down 590 / 1244 ms after the gate; the isolated hit with the echo is 20 / 40 / 60 dB down at 684 / 1462 / 1848 ms and its last sample above −60 dB falls 5190 ms after the gate: the dry tail rings out in roughly a second, the echo runs several seconds. The echo sits 46 / 25 / 24 / 30 / 21 / 20 / 29 / 17 / 17 dB under the figure's hits 3 to 11.
- **The sub in the repeats:** MUD ratio / centroid / share in 60 to 150 Hz in repeat slots 1, 2, 3: 1 / 2242 Hz / 19 %, 2 / 1702 Hz / 15 %, 3 / 1325 Hz / 11 %: no 150 to 400 Hz body builds up.
- **The spring is off** (DRAIN 0). There is no tape (CHEW 0).
- **Limits.** No inharmonic cymbal partials: only noise (X-MOD was not tried). One filter and one amp envelope are shared by the noise and the sub, so the sub leaves early only through the high-pass. There is no separate burst envelope and ring envelope (one filter envelope, one amp envelope).
- **Costs:** about 1857 host instr/sample worst case (idle 1180 + 677 under load). The device build was not run and the device render time is not measured.
- **Program-load check:** the program-load render and the render built over INIT are bit-identical, from the boot patch and from INIT.
- **Tricks:** untested on this patch: the SLOBBER slop ride, SEQ held (Tape Stop), the kill switch (HEEL), GROWL, CHEW.

## 5. Final values (for debugging, not for players)

`MODE POLY (POLY 5), OSC1 PULSE PW 64 (50 %) LVL 80, OSC2 PULSE PW 64 SEMI +12 FINE 64 LVL 45, NOISE 127, CUTOFF 100 (4186 Hz at C4), RESO 10, ENV AMT 0 (−64, about −97 semitones at the envelope's peak), KEY TRK 0, FILTER HP12, FILTER ENV A0 D100 S0 R60, AMP ENV A52 D97 S0 R97, VINTAGE 30, SPREAD 60, VOLUME 121 (−18.0 dBFS RMS on the crash phrase, own-phrase peak −4.5); DLY MIX 80 (ALLEY 106 = 361 ms, FEEDBK 100, TONE 70, PINGPONG 127); DRAIN 0, CHEW 0, GROWL 0, no arp` — `PF_REEF_BREAK` in `firmware/src/obv_patches.h`.
