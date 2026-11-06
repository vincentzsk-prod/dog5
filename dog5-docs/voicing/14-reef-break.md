# Voicing log — 14 "Reef Break" (FACTORY[13], Batch 4B, Chapter II, the tape / crash pair)

6 Nov 2026. Brief (Chapter II, The Tidal Hexes): *percussive crash: a noise burst on attack, a thick sub, long delay feedback (the original screen brief: a tidal maelstrom over the top-right corner). Vincent's notes: the noise must be a burst but not a complete blow-out; short to very short attack and/or a swell in quick (but not immediate) peak, then the decay ringing a crash-cymbal emulation out; the Space Echo reference and reach; emphasis on the burst with a medium-length tail.* Method and kit: `README.md` here (§1 phrases, §3 loudness, §17 Batch 4B).

## RECOMMENDED: variant B (burst) — committed as the patch, awaiting Vincent's listening

**Status: round 1 rendered, not yet heard.** Variant B is committed as `PF_REEF_BREAK` in `firmware/src/obv_patches.h` (equals variant B byte for byte: `tests/voicing/check_slot.py 14 B 4b`); the others are render-only. **Round count so far: 1 silent measured round (variants fixed by sweeps of the existing controls, not for ears) + 1 listening round pending.** No voice card and no `reference-renders/` yet. WAVs: the never-merged `listen/batch-04b-chapter2-ghost-and-reef` branch, `listen/voicing/batch-04b/14-reef-break/`; tables: `README.md` and `probes.md` there.

### The starting point (the patch as it stood)

* **Current values (the whole list; every parameter not named is at the table's default):** NOISE 60, O2_SEMI 48, CUTOFF 90, RESO 30, FENV_AMT 124, FTYPE 0, FD 25, FS 0, AA 1, AD 30, AS 0, AR 25, REV_SIZE 90, REV_MIX 40.
* **Nearest starting patch:** PERC HIT (`PF_PERC_HIT`, 14's alone): POLY 5, NOISE 60 over a saw at the key (the only 'sub': it measures 26 dB above the noise in the first 100 ms) and a saw two octaves up, a 12 dB LOW-pass at CUTOFF 90 with ENV AMT +60 (opens at the strike), filter decay 25 / amp decay 30 / sustain 0 / release 25, a spring at DRAIN 40, **no echo**. It rings 12 ms (the 4k+ band is 20 dB down 9 ms after its peak) and measures -47.9 dBFS RMS on the crash phrase (noise 26 dB under the saw in the first 100 ms): a click, not a crash.
* **The 1-2 axes judged most uncertain:** (1) the tail (the ring-out of the top bands: 0.5 / 0.9 / 1.3 s to -40 dB) and the attack (near-instant against a quick swell); (2) how far the echo runs (FEEDBK 96 / 100 / 114) without washing the burst.
* **Control limits foreseen:** ONE filter per voice, shared by the noise and the oscillators; ONE amp envelope for both (the sub cannot decay faster than the noise except through the filter); no inharmonic partials of a cymbal (only noise, plus X-MOD which was not used); the level is limited by the peak, not by VOLUME alone (the noise's peak and a stack of hits); a noise patch's peak follows the random seed (two seeds checked).
* **Plan:** **the cymbal's decay from a HIGH-PASS that climbs:** a 12 dB high-pass whose cutoff is pushed down at the strike by a NEGATIVE ENV AMT (0 = about -97 semitones at the envelope's peak: the cutoff starts at 15 Hz, under the sub) and climbs back to 4186 Hz as the filter envelope falls: the sub and the low noise pass at the strike and go first (the sub's own decay is set by FD), the top of the noise rings longest (4k+ outlasts 60-150 by a factor of 5 here), and the amp envelope (AD = AR) sets the ring-out; NOISE 127 against a square sub (O1 80, O2 an octave up 45) puts the noise 3-6 dB above the sub; then a BBD echo, **no spring** (not in this patch's gear list; DRAIN 0) and no tape.

### Axes chosen, variants

| variant | what | VOLUME | level (own phrase) | (b) | peak (own) | worst-case CPU |
|---|---|---|---|---|---|---|
| A original | the nearest-base patch as it stood (PERC HIT, 14's alone: noise 60 + a saw and a saw +24 st, LP12 with a filter envelope, spring, no echo) | 100 | -47.9 | -44.4 | -11.1 | 1762 |
| B burst (recommended, committed) | near-instant attack, medium tail (top band 20 / 40 dB down in ~0.5 / ~0.9 s), echo FEEDBK 96 MIX 90 at 361 ms | 118 | -19.9 | -14.3 | -4.3 | 1832 |
| C swell | a quick swell (peak in ~10-40 ms), the longest tail, echo FEEDBK 100 MIX 80 | 121 | -18.0 | -12.8 | -4.5 | 1857 |
| D runaway | near-instant attack, the shortest tail, a near-runaway echo (FEEDBK 114 MIX 100, 337 ms) | 124 | -20.1 | -14.4 | -4.5 | 1827 |

* **Final values (variant B), each change before -> after (the original is the nearest-base patch as it stood):**

  * O1_WAVE SAW -> PULSE
  * O1_LVL 110 -> 80 (-24%)
  * NOISE 60 -> 127 (+53%)
  * O2_WAVE SAW -> PULSE
  * O2_LVL 100 -> 45 (-43%)
  * O2_SEMI +24 -> +12 st
  * O2_FINE 70 -> 64 (centre 64: +6 -> +0, -5% of range) (+4.7 cents -> +0.0 cents)
  * CUTOFF 90 -> 100 (+8%) (2349 Hz -> 4186 Hz)
  * RESO 30 -> 10 (-16%)
  * FENV_AMT 124 -> 0 (centre 64: +60 -> -64, -98% of range)
  * KEYTRK 64 -> 0 (-50%)
  * FTYPE LP12 -> HP12
  * FA 20 -> 0 (-16%) (2 ms -> 0 ms)
  * FD 25 -> 100 (+59%) (4 ms -> 1218 ms)
  * AA 1 -> 0 (-1%) (1 ms -> 0 ms)
  * AD 30 -> 92 (+49%) (5 ms -> 653 ms)
  * AR 25 -> 92 (+53%) (4 ms -> 653 ms)
  * VOLUME 100 -> 118 (+14%)
  * DLY_FB 50 -> 96 (+36%)
  * DLY_MIX 0 -> 90 (+71%)
  * REV_MIX 40 -> 0 (-31%)
  * ALLEY 0 -> 106 (+83%) (SYNC -> 361 ms)

* **Level (note-on region = the 300 ms gates of the 11 hits: the burst and about the first 250 ms of its decay, echo included; the release, the rest of the decay and the tails excluded):** VOLUME 118; **-19.9 dBFS RMS** (seed 2: -19.8; C -18.0, D -20.1); phrase (b) -14.3 dBFS (three stacked noise voices: peak -1.0, no clipped sample); own-phrase peak -4.3 dBFS (seed 2 -4.6); crest 15.6 dB; worst-case CPU 1832 host instr/sample (the original 1762). **B (-19.9) and D (-20.1) sit 0.4 and 0.6 dB under the -19.5 floor of the band: with the peak held at -4 dBFS on both seeds the level falls there (VOLUME 118 / 124, of 127); C -18.0 is inside.**
* **Measured on the recommended variant** (full tables: `listen/voicing/batch-04b/14-reef-break/README.md`, `probes.md`):
  * **Not a blow-out:** own-phrase peak -4.3 / -4.6 dBFS on two seeds (the second seed = a quiet note struck first, so the hits land on other voice cards' noise generators), crest 15.6 / 15.3 dB, 2 % of samples within 10 % of the rail (noise: the pixelation measure of 05 reads 98 % on a clipped square), no clipped sample in any render; the isolated hit with the echo peaks at -5.7 dBFS.
  * **Noise against sub (first 100 ms):** noise +4.6 dB over the sub on A1 (+3.4 on A2); the original was -25.7. The sub-only A1 hit's first 150 ms: 42 % under 60 Hz, 28 % in 60-150 (an A1 fundamental is 55 Hz); on A2 71 % in 60-150. The sub's 40-150 Hz band falls 20 / 40 dB in 163 / 279 ms (C 174 / 290, D 93 / 163): thick for about a quarter of a second, then the noise alone.
  * **Attack (A1, 10 / 50 / 90 % of the peak, ms):** B 0.0 / 0.2 / 8.5 (near-instant: the first millisecond; the 90 % mark at 8.5 ms is the noise's own random peaks); C **2.2 / 8.7 / 27.2** (AA 52: the quick swell, peak at 27 ms); D 1.2 / 7.2 / 8.7 (AA 44: 50 % at about 7 ms).
  * **The cymbal's decay (A1 hit, voice alone, band energy to -20 / -40 dB after each band's own peak, ms):** 60-150: 96 / 267; 400-1.2k: 276 / 331; 1.2k-4k: 316 / 641; **4k+: 482 / 932** (the main body rings out to -40 dB in ~0.9 s). Tail options: B 0.93 s, **C 1.33 s** (AD = AR 97), **D 0.70 s** (AD = AR 88; FD 92). The bands fall in order, low first, as a cymbal does. For comparison the same noise through a closing LOW-pass (the original's way) has the top band 20 / 40 dB down at 223 / 302 ms and the sub still ringing at 499 / 964 ms: the wrong way round (`probes.md`).
  * **The echo (Space Echo):** ALLEY 106 = 361 ms, FEEDBK 96, MIX 90. Repeats 1..6 re the burst: -12 -18 -23 -27 -31 -34 dB; 7 repeats stay above -40 dB (C 7; **D, FEEDBK 114: all 16 slots, 5.4 s, -11 -15 -18 -20 -21 -23 dB**); the whole hit with echo is 20 / 40 / 60 dB down at 390 / 1104 / 1488 ms (D 326 / 704 / 3716). Stability: no clipped sample at any FEEDBK 96-127 on the isolated hit and its peak stays -5.7 dBFS; from FEEDBK 118 the repeats no longer fall below -40 dB (24 slots: -28 dB at repeat 24; 122: -10; 127: -1: the loop is held by its own ceiling, `probes.md`). The echo under the figure's hits: -49 -25 -24 -31 -20 -20 -30 -17 -16 dB re each hit (hits 3-11): it stays under the hits even at 400 ms spacing (D: -32 -20 -19 -23 -18 -16 -22 -17 -16).
  * **The sub in the repeats (MUD / centroid Hz / % in 60-150, repeat slots 1, 2, 3):** 1 / 2206 / 20 ; 2 / 1514 / 17 ; 3 / 1146 / 13: no tubby 150-400 Hz body (the echo's feedback path has a high-pass at 80 Hz; the repeats are mostly noise).
  * **What the filter can and cannot do (`probes.md`, one control changed):** the climbing high-pass is what makes the top outlast the lows and keeps the sub only at the strike; a closing low-pass does the opposite; a wide-open low-pass or a notch leave every band the same length (the amp envelope's); a high-pass without the envelope removes the sub (noise 27 dB over it); a band-pass at CUTOFF 100 leaves the noise 17 dB under the sub and the level 11 dB down. FD sets the sub's length (FD 85 / 92 / 100 / 108: sub -20 dB at 58 / 93 / 163 / 255 ms).
  * **What I could not do:** a cymbal's inharmonic metallic partials (only noise; X-MOD not tried, it is a cross-FM of the two oscillators); a sub that decays faster than the noise through the amp (one amp envelope: the high-pass does it); a separate envelope for the burst and the ring (one filter envelope, one amp envelope); the level reference at VOLUME 127 without raising the peak above -4 on a hit this peaky (B and D sit slightly under the band).

### Recommendation (vocabulary)

**B (burst):** an instant noise burst with a square sub that goes first, then the top of the noise ringing out over about a second into a runaway-leaning echo that stays well under the hits. C is the quick swell (peak in 27 ms) with the longest tail and the level inside the band; D is the shortest tail with a near-runaway echo that never falls below -40 dB. Turn it by ear on: AA (instant against swell), AD = AR (the ring-out), FD (the sub's length), NOISE / O1 / O2 (burst against sub), FEEDBK and MIX (the echo).

### Surprising / hard with existing controls

* The original rings 12 ms: it is a click; the brief's burst-and-ring needed a new filter strategy, not a re-trim.
* The sub can only leave early through the filter: a NEGATIVE ENV AMT on a high-pass is the one way to have the sub at the strike and the cymbal's top last.
* The peak limits the level (B -19.9, D -20.1) because a noise burst's crest is 15-16 dB; the swell (C) lowers it to 13.5.
* Phrase (b) (three notes at once) peaks at -1.0 / -1.5 / -1.7 dBFS on B / C / D: three noise voices stack; not the patch's use, not clipped.

