# 14 · Reef Break · Chapter II · BEE-TCH

*Voiced 6 Nov 2026 (Batch 4B), approved after listening: round-1 variant C (the quick swell). **Changed 18 Nov 2026 (Batch 11, test build 0.2), on Vincent's instruction after he found the old attack too harsh: the attack of both envelopes is now 299 ms (FILTER ENV A 0 → 82, AMP ENV A 52 → 82) and VOLUME 121 → 116. It was not auditioned before merge; Vincent then played v0.2 on his FM-1 on 18 Nov and approved it ("reef break sounds spot on", his words).** The 6 Nov approval covers the old attack; the 18 Nov approval covers this one. Renders: `reference-renders/14-reef-break_C_*.wav` (the 6 Nov approved version, old attack, kept as history) and `reference-renders/14-reef-break_C-0.2_*.wav` (this version, approved on the unit 18 Nov). Log: `../14-reef-break.md`; the Batch 11 numbers: `../../BATCH-11-TEST-BUILD-0.2.md`.*

## 2. What it sounds like

A crash made of a burst of noise over a square-wave sub. The noise swells in over a fraction of a second rather than striking at once, the lows fall away first and the top rings out longest, as a cymbal does, and a long echo follows each hit. No spring, no tape.

## 3. Gear inspirations (docs only, "inspired by")

- **Roland TR-808** — *thick sub*.
- **Simmons SDS-V** — *noise burst*.
- **Roland RE-201 Space Echo** — *long repeats*.

Closest to: **an 808 kick with a noise burst into a Space Echo**.

## 4. Sound design notes

- **Where it lives:** single hits, low (A1) or mid (A2). Hits about 400 ms apart or more let each one bloom.
- **It swells in:** both envelopes have a 299 ms attack, so the crash peaks just after the hit. For a harder strike, bring the AMP and FILTER ENV attacks down.
- **The dry crash rings out in about a second; the echo runs several seconds.** The BBD page's MIX or FEEDBK shorten it.
- **Three keys at once** stack three noise voices and get loud: one key per hit.
- It is noise only: no metallic cymbal partials.

## 5. Final values (for debugging, not for players)

`MODE POLY (POLY 5), OSC1 PULSE PW 64 (50 %) LVL 80, OSC2 PULSE PW 64 SEMI +12 FINE 64 LVL 45, NOISE 127, CUTOFF 100 (4186 Hz at C4), RESO 10, ENV AMT 0 (−64, about −97 semitones at the envelope's peak), KEY TRK 0, FILTER HP12, FILTER ENV A82 (299 ms; was A0) D100 S0 R60, AMP ENV A82 (299 ms; was A52) D97 S0 R97, VINTAGE 30, SPREAD 60, VOLUME 116 (was 121; −18.03 dBFS RMS on the crash phrase, own-phrase peak −4.17 / −4.77 on two seeds). **History (6 Nov approved version, old attack): FILTER ENV A0, AMP ENV A52, VOLUME 121.** The attack values 82 / 82 display as `299ms` on the unit's screen (`TIME_MS_X10[82]` = 2992); DLY MIX 80 (ALLEY 106 = 361 ms, FEEDBK 100, TONE 70, PINGPONG 127); DRAIN 0, CHEW 0, GROWL 0, no arp` — `PF_REEF_BREAK` in `firmware/src/obv_patches.h`.

## 6. The voicing record (measured notes, not for players)

*Sections 2–4 as they stood before the Batch 30 rewrite (23 Nov 2026): the measurements, the variants and what was and wasn't tested. The player text above is drawn from this.*

### 2. What it sounds like

A crash made of a burst of noise over a square-wave sub. The noise swells in over a fraction of a second rather than starting at once (the attack is long since 18 Nov 2026), the lows fall away first and the top of the noise rings out longest, and a long echo follows each hit. There is no spring. After the slower attack the lows arrive later than before: they are measured as peaking at about the end of the 300 ms gate.

### 3. Gear inspirations (docs only, "inspired by")

- **Roland TR-808** — *thick sub*. The sub-only hit's first 150 ms: **Measured with the old attack (6 Nov): on A1 41 % of the energy is under 60 Hz and 28 % in 60 to 150 Hz (an A1 fundamental is 55 Hz); on A2 71 % is in 60 to 150 Hz; the sub's 40 to 150 Hz band is 20 / 40 dB down 174 / 290 ms after its peak. With the 299 ms attack (18 Nov) the same first 150 ms of the sub-only hit holds 2.7 % under 60 Hz and 3.8 % in 60 to 150 Hz on A1 (A2: 14 % in 60 to 150 Hz), and the sub's band peaks 255 ms after the note-on, 20 / 40 dB down 58 / 70 ms after that peak.** The first 150 ms now falls inside the attack, so these shares are not comparable with the old ones. "Booming" is not measured.
- **Simmons SDS-V** — *noise burst*. In the first 100 ms the noise was 4.7 dB over the sub on A1 (3.5 dB on A2) with the old attack; with the 299 ms attack it is 15.6 dB (A2 12.4 dB), a window that now sits inside the attack ramp. The attack of the hit (voice alone, 10 / 50 / 90 % of the peak): **old (A0 / A52):** A1 2.2 / 8.7 / 27.2 ms with the peak at 27.4 ms; A2 2.7 / 12.2 / 32.2 ms, peak at 32.2 ms; **new (A82 / A82):** A1 25.2 / 126.2 / 208.0 ms with the peak at 208.3 ms; A2 24.4 / 112.7 / 258.4 ms, peak at 267.9 ms. "Crashing" is supported only by the band decay below.
- **Roland RE-201 Space Echo** — *long repeats* (only that): ALLEY 106 = 361 ms, FEEDBK 100, MIX 80. On an isolated hit the first repeats were −13 / −18 / −24 / −28 / −31 / −35 dB re the burst's peak and 7 repeats stayed above −40 dB with the old attack; with the new attack they are −13 / −18 / −23 / −26 / −30 / −33 dB and 8 stay above −40 dB; the echo stays below clipping (peak of the isolated hit with echo −5.3 dBFS with the old attack, −6.0 dBFS with the new one, no clipped sample in either).

Closest to: **an 808 kick with a noise burst into a Space Echo**.

Nothing here says the patch matches these: it was built toward the descriptions, by measurement, and approved by ear.

### 4. Sound design notes

- **Register and gate:** voiced on the crash phrase: one low hit (A1), one mid hit (A2), and A1 hits 1000, 600 and 400 ms apart, every gate 300 ms, velocity 108. Other registers are untested. POLY 5.
- **The decay (A1 hit, voice alone), measured from the note-on** (the band peaks moved with the attack, so times from each band's own peak are not comparable; Batch 11, 11.6 ms frames). Time at which each band's short-time energy has fallen 20 / 40 dB below its own peak, in ms after the note-on, **old attack → new attack**: 60 to 150 Hz 102 / 273 → 308 / 316; 150 to 400 Hz 238 / 308 → 311 / 328; 400 to 1.2k 311 / 345 → 331 / 366; 1.2k to 4k 345 / 885 → 435 / 1120; **4k and up 711 / 1376 → 923 / 1622** (A2, 4k and up: 723 / 1422 → 967 / 1654). Each band's peak time: 60 to 150 Hz 23 → 235 ms, 4k and up 46 → 255 ms. The bands still fall in the order lowest first and the 4k and up band rings longest. (With the old attack, from each band's own peak: 60 to 150 Hz 78 / 250 ms … 4k and up 665 / 1329 ms.) The top bands ring out longer than the sub and the lows. **With the new attack the first 50 ms of the hit holds 74 dB (60 to 150 Hz) and 21 dB (4k and up) less energy than the loudest band-window of the hit (4k and up, 150 to 400 ms); with the old attack the first 50 ms was −6 dB (60 to 150 Hz) and −1 dB (4k and up) re that loudest window.** The high-pass starts at its full cutoff at the strike (the filter envelope is at 0) and the filter envelope's slow rise takes it down; this is the suggested cause of the lows' late arrival, not isolated. How: one 12 dB high-pass, CUTOFF 100 (4186 Hz at C4), whose cutoff is pushed far down at the strike by ENV AMT 0 (about −97 semitones at the envelope's peak) and climbs back as the filter envelope falls (FD 100); the amp envelope (AD = AR = 97) sets the ring-out.
- **Peak behaviour.** Own-phrase peak **−4.17 dBFS (a second noise seed: −4.77)**, crest factor 13.9 / 13.3 dB, 2 % of samples within 10 % of the rail (2.2 %), no clipped sample (with the old attack: −4.5 / −4.3, crest 13.5 / 13.7, VOLUME 121; the old VOLUME 121 with the new attack gave −3.56, over the −4 limit, which is why VOLUME was lowered). The second seed is a quiet note struck first, so the hits land on other voices' noise generators. Phrase (b), which strikes three keys at once, stacks three noise voices and now reads −16.95 dBFS RMS with a peak of −2.82 dBFS (old attack: −12.8 / −1.55, the near-rail warning of 6 Nov); a second seed was not re-measured on (b).
- **Level:** −18.03 dBFS RMS on the crash phrase (VOLUME 116; before the attack change VOLUME 121 read −18.0, and with the new attack at VOLUME 121 it would read −17.3; the bank reference is −18.0 ± 1.5), the note-on region being the 300 ms gates of the 11 hits (the burst and about the first 250 ms of its decay, echo included; the release, the rest of the decay and the tails excluded).
- **The echo against the dry tail.** The dry voice (sends off) is 20 / 40 dB down 588 / 1284 ms after the gate (old attack: 590 / 1244); the isolated hit with the echo is 20 / 40 / 60 dB down at 728 / 1472 / 1868 ms (old: 684 / 1462 / 1848) and its last sample above −60 dB falls 4702 ms after the gate (old: 5190): the dry tail rings out in roughly a second, the echo runs several seconds. The first repeat is −13.2 dB re the dry note's peak with either attack, and it now lands 620 ms after the hit's onset (old: 391 ms), the peak itself being later. The echo sits 46 / 25 / 24 / 29 / 18 / 17 / 27 / 16 / 15 dB under the figure's hits 3 to 11 (old attack: 46 / 25 / 24 / 30 / 21 / 20 / 29 / 17 / 17).
- **The sub in the repeats:** MUD ratio / centroid / share in 60 to 150 Hz in repeat slots 1, 2, 3: old attack 1 / 2242 Hz / 19 %, 2 / 1702 Hz / 15 %, 3 / 1325 Hz / 11 %; new attack 1 / 2269 Hz / 9 %, 2 / 1980 Hz / 8 %, 3 / 1522 Hz / 7 %. The 150 to 400 Hz share in slot 3 is 38 % in both.
- **The spring is off** (DRAIN 0). There is no tape (CHEW 0).
- **Limits.** No inharmonic cymbal partials: only noise (X-MOD was not tried). One filter and one amp envelope are shared by the noise and the sub, so the sub leaves early only through the high-pass. There is no separate burst envelope and ring envelope (one filter envelope, one amp envelope).
- **Costs:** about 1857 host instr/sample worst case (idle 1180 + 677 under load), measured for the old attack; not re-measured after the attack change (no code changed, only two envelope values). The device build was not run and the device render time is not measured.
- **Program-load check:** measured for the old attack (the program-load render and the render built over INIT bit-identical, from the boot patch and from INIT); not re-run for the new attack. Batch 11 checked that the other 31 slots render bit-identical to `main` on all 52 phrases.
- **Tricks:** untested on this patch: the SLOBBER slop ride, SEQ held (Tape Stop), the kill switch (HEEL), GROWL, CHEW.
