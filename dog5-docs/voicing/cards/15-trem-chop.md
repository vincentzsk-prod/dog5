# 15 · Trem Chop · Chapter II THE TIDAL HEXES

*Voiced 5 Nov 2026, approved as rendered (variant D of Batch 3B; variant B was committed first). Renders: `reference-renders/15-trem-chop_D_*.wav` (D is this patch). Log: `../15-trem-chop.md`.*

## 2. What it sounds like

A broken-strobe tremolo: a bright saw chopped on and off by a hard square-shaped LFO, not a gentle sine. Every note is a pair of voices, and the voices of the pair chop slightly out of step, so the chop has an off part, a reduced-level part and a full part instead of a clean on/off. It is dry: no echo, no spring, no tape.

## 3. Gear inspirations (docs only, "inspired by")

- **Roland SH-101** — the source: *bright, punchy*.
- **Boss TR-2 Tremolo (square setting)** — the chop: *choppy, gated*.
- **Electro-Harmonix Pulsar** — *choppy, rhythmic*.
- **Korg Polysix** — *drift*.

Closest to: **an SH-101 saw through a Boss TR-2 on square**.

Nothing here says the patch matches these: it was built toward the descriptions, by measurement, and approved by ear.

## 4. How to play it

- **Register:** it was voiced on a held A3 (2.4 s), a six-note riff of 500 ms notes (A3 C4 E4 D4 C4 A3), the chord A3 + E4 + A4, and eight 110 ms notes; other registers are untested.
- **It is DUAL with POLY 6: every note is two voices.** A three-note chord uses all six and plays whole (the chord phrase was rendered); four-note chords were not tested. PHASE SPREAD offsets the LFO by 45° per voice, so the two voices of a note chop an eighth of a cycle apart (about 15 ms at the default rate).
- **The chop, measured on the held A3:** 8.10 Hz, 44.8 dB between the on and the off parts. The held note spends 35 % of the time off, 31 % at one voice's level and 33 % at full (the MONO variant B of the same round: 49 % off, 1 %, 50 %).
- **How hard the edges are:** a single edge rises 10 to 90 % in about 16 ms on a high probe note, which suggests the two voices' edges, about 15 ms apart at the default rate (the MONO variant B measured 0.77 ms, a reading limited by its window; the engine's own ramp across one 16-sample control block is 0.36 ms). The timing of the edges is steady: standard deviation 0.18 ms about a straight line, the reading's resolution being 0.5 ms.
- **Where a note starts in the chop:** on the short phrase (eight 110 ms notes at 120 BPM eighths) 5 of 8 notes start on, and the first edge falls at 42 ± 21 ms after the note-on. This suggests the spread phase is not restarted by the note, so it can differ from note to note (not isolated). With LFO PHASE SYNC (variant B) all 8 of 8 start on, the first edge at 59 ± 2.2 ms.
- **No tempo sync with existing controls.** The LFO rate is the RATE knob alone (0.05 × 600^(RATE/127) Hz, a step about 5 %). The default, RATE 101 = 8.10 Hz, is the nearest byte to sixteenths at 120 BPM (8.0 Hz). Nearest bytes for one on+off cycle per note value: 90 BPM quarter / eighth / sixteenth = RATE 68 / 81 / 95 (1.54 / 2.96 / 5.99 Hz); 120 BPM = 73 / 87 / 101 (1.98 / 4.00 / 8.10 Hz); 140 BPM = 76 / 90 / 104 (2.30 / 4.65 / 9.42 Hz). A byte can be up to 2.5 % off the tempo, so against a long phrase the chop slides against the beat.
- **Slop:** VINTAGE 60 moves the pitch and cutoff, not the chop. On the MONO variant B in the same round the edge timing's standard deviation was 0.18 / 0.24 / 0.16 ms at VINTAGE 0 / 60 / 127 (no effect).
- **LFO PITCH is 0.** The original 8 was inert (below 12 the law is zero); 12 would put a square ±9 cent pitch step on every edge, which is untested.
- **Level:** matched to the bank reference on the chop phrase, off parts included (−17.9 dBFS RMS). **It reads about 2.5 dB hot on phrase (b)** (−15.4), and its peak is −6.2 dBFS (whole renders; the limit is −4).
- **Costs, honestly:** about 2375 host instr/sample worst case (idle 1163 plus 1211 under load); the original is 1402 and the MONO variant B 1366; B and D differ only in MODE (MONO to DUAL), POLY 6, PHASE (SYNC to SPREAD) and VOLUME. The device build was not run and the render time on the device is not measured.
- **Tricks:** untested on this patch: the SLOBBER slop ride, SEQ held (Tape Stop), the kill switch (HEEL), GROWL, CHEW, ALLEY, DRAIN, the other LFO shapes (RAMP, SAW, S&H) on the amp.

## 5. Final values (for debugging, not for players)

`MODE DUAL (DETUNE 30: the pair is 5.5 cents apart), POLY 6, GLIDE 0, OSC1 SAW LVL 127, OSC2 SAW SEMI 0 FINE 69 (+3.9 cents) LVL 127, CUTOFF 95, RESO 20, ENV AMT 90, KEY TRK 64, FILTER LP24 DRIVE 60, FILTER ENV A20 D70 S40 R60, AMP ENV A3 D70 S127 R40, LFO SQUARE RATE 101 (8.10 Hz) PHASE SPREAD DELAY 0 AMP 127 PITCH 0, VINTAGE 60, SPREAD 60, VOLUME 84 (−17.9 dBFS RMS on the chop phrase, peak −6.2); DLY MIX 0 (DLY FEEDBK 35 is inert), DRAIN 0, CHEW 0, GROWL 0, no arp` — `PF_TREM_CHOP` in `firmware/src/obv_patches.h`.
