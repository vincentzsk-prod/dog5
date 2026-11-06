# 05 · ZEAROX · Chapter I Wasteland

*Voiced 5 Nov 2026, approved as rendered (variant D of round 2; round 1 was rejected). Renders: `reference-renders/05-zearox_D_*.wav` (D is this patch). Log: `../05-zearox.md`.*

## 2. What it sounds like

A kick substitute made of a single square wave. The pitch drops fast at the very start, and a fast random stepped pitch LFO moves it to a new random value again and again, so each hit gets a few random pitch steps (a longer note gets more). The wave stays almost entirely at its extreme levels, there is no attack, and the hit stops quickly when you let go. It is dry: no tape, no drive stage, no echo, no spring.

The owner's own description of the intent: pixelated, gritty, blown out, like a photocopy reduced to pure black and white. That is the intent, not a measurement.

## 3. Gear inspirations (docs only, "inspired by")

- **Roland TR-808 kick** — *sub, thump*.
- **Roland SH-101** — *sub, thick*.
- **Tascam Portastudio cassette 4-track** — *lo-fi, noisy*.
- **ProCo RAT** — *crunchy, driven*.

Closest to: **an 808 kick smashed onto a blown-out cassette 4-track**.

Nothing here says the patch matches these: it was built from the descriptions, by measurement, and approved by ear. The tape part of that picture is not in this patch: the tape was removed in round 2 at the owner's direction (CHEW, HISS and DROPS are 0), and the drive stage (GROWL) is not used either.

## 4. How to play it

- **Register:** it was voiced on three isolated 150 ms hits (A0 27.5 Hz, A1 55 Hz, A2 110 Hz) and four hits a bar of A1 at 120 BPM; the pilot riff and stabs phrases were rendered too. Other registers are untested.
- **It is MONO, so legato does not re-fire the envelopes:** a key held while the next goes down slides to the new note and the envelopes do not restart. Play it detached. A chord plays one note (the last).
- **What is in the voice:** one hard square (OSC 2 pulse, an octave up from the key, OSC 1 off), the filter open (12 dB, CUTOFF 105, RESO 0), amp and filter attack 0, a decay of 187 ms to sustain 0, a 2 ms release. The quick pitch drop is the filter envelope on OSC 2's pitch: +17 semitones at the strike, falling over 11 ms.
- **The glitch:** the LFO is sample-and-hold on pitch, 21 Hz, depth up to ±4.7 semitones (±470 cents), free-running. The hit-to-hit spread of the first-60-ms centroid over eight pattern hits (s.d. over mean) is 5 % with the LFO as shipped (LFO PITCH 80), 1 % with the LFO off (LFO PITCH 0) and 10 % at LFO PITCH 110. The ratio of 150–400 Hz energy to 1.2 kHz+ energy (A1, 20–100 ms) is 3.9 as shipped (PITCH 80) and 26.5 at PITCH 110. Other LFO rates are untested.
- **Black and white, measured:** the share of samples within 10 % of the rail (5 ms windows, first 100 ms of a hit) is 98 / 96 / 94 % on A0 / A1 / A2 (a decaying hard-clipped square reads near 100 %). Above 1.2 kHz is 0.9 / 3.4 / 5.6 % of the energy in the first 100 ms.
- **Tail:** 60 dB down 16 ms after the key goes up on A1 and A2, and 8 ms on A0 (DC subtracted). A1 falls from −12 to −29 dBFS (20 ms windows) over its first 120 ms.
- **The kick is mostly the quick pitch drop.** There is no click spike in the patch: the first 5 ms measure 3.1 dB over the 10–50 ms level, which is in step with the decay. A filter-envelope click was tried (CUTOFF 85, ENV AMT 100–127, DECAY 25–30): it closed the filter, leaving 1.3 % of the energy above 1.2 kHz against 3.4 % and 85–89 % black-and-white against 96 %, so it is not in the patch.
- **A0 is still mostly sub:** after its first 20 ms, 81 % of the A0 energy is under 60 Hz, and a 27.5 Hz square is inaudible on a small speaker. In its first 20 ms 45 % is at 60–150 Hz. A1 and A2 sit above that: after a 100 Hz high-pass the kick phrase keeps −1.6 dB of its level (the original: −10.9).
- **Level:** −18.1 dBFS RMS on the kick phrase (11 hits × 150 ms), phrase (b) −19.1, peak −10.7 dBFS; crest factor 7.3 dB over the kick phrase and 1.9 dB over the first 30 ms of a hit. **VOLUME is 123 of 127: there is almost no knob headroom above the bank reference.** A tighter decay (DECAY 72) already reads −19.5 dBFS at VOLUME 123.
- **Not bit-comparable from the boot patch:** the sample-and-hold LFO follows the engine's random state, and the audio differs between the boot patch and INIT (the difference between the two renders is 1.9 to 2.9 dB louder than the signal on the test phrases; they are bit-identical when both load from INIT). The cause was not isolated.
- **Costs, honestly:** about 1337 host instr/sample worst case (idle 1164, the engine alone, plus 173 under load; the original 1361). Not used here: GROWL 104 would add about 595 and CHEW 127 about 784 (measured on the round-2 test patch). The device build was not run and the render time on the device is not measured.
- **Tricks:** untested on this patch: the SLOBBER slop ride, SEQ held (Tape Stop), the kill switch (HEEL), ALLEY, DRAIN, GROWL, CHEW.

## 5. Final values (for debugging, not for players)

`MODE MONO, GLIDE 0, OSC1 OFF (LVL 40), OSC2 PULSE PW 64 SEMI +12 FINE 68 (+3.1 cents) LVL 127, ENV>O2 110 (+17 st), X-MOD 0, NOISE 0, CUTOFF 105, RESO 0, ENV AMT 64 (0), KEY TRK 0, FILTER LP12 DRIVE 0, FILTER ENV A0 D40 S0 R60, AMP ENV A0 D76 S0 R20, LFO S&H RATE 120 (21.1 Hz) PHASE FREE PITCH 80 (±470 cents) PITCH> BOTH, VINTAGE 30, SPREAD 60, VOLUME 123 (−18.1 dBFS RMS on the kick phrase, peak −10.7); CHEW 0 HISS 0 DROPS 0, GROWL 0, DLY MIX 0, DRAIN 0, ALLEY 0, no arp` — `PF_ZEAROX` in `firmware/src/obv_patches.h`.
