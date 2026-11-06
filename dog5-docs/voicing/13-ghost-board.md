# Voicing log — 13 "Ghost Board" (FACTORY[12], Batch 4B, Chapter II, the tape / crash pair)

## ROUND 2 (6 Nov 2026) — the original's voice with round 1's D echo, the deck off

**What Vincent heard (round 1):** variant C, built as "more Mellotron" (the tone nearest a triangle, tape wobble up, less echo), was the wrong direction: **the ORIGINAL A is the most Mellotron to his ear**. "Tape wobble is definitely killing the overall tone. Needs to be dropped entirely." "The echo, spring and first repeat of option D sound AMAZING! The Space Echo on D sounds SO GOOD! What I'm chasing is Mellotron + Space Echo, with the Space Echo as it is in D."

**What round 2 built (13 only, parameter values only):** all four variants carry the ORIGINAL's voice exactly (from the pre-4B base, not from memory: O1 PULSE PW 64, O2 PULSE PW 40 FINE 73, LP24 CUTOFF 75, RESO 5, ENV AMT 74, FA 50, AA 60, AR 90, LFO TRI RATE 50 PHASE SPREAD PWM 60, VINTAGE 50, SPREAD 100, POLY 5); LFO PITCH 3 -> 0 (**bit-identical to 3 on both phrases, proved by rendering both: the law is zero below 12**); CHEW 0 (the deck inactive: TP_* are not read with CHEW 0); and **every echo and spring value copied from round-1 D**: DLY_TIME 3 (was 3), DLY_FB 95 (was 50), DLY_TONE 70 (was 70), DLY_MIX 105 (was 0), ALLEY 104 (was 0), ALLEY_FINE 0 (was 0), BBD_SPREAD 127 (was 127), REV_SIZE 100 (was 100), REV_DAMP 25 (was 60), REV_PRE 20 (was 20), REV_MIX 70 (was 35). VOLUME re-trimmed on each. The four differ by one thing each: **A2 as is; B2 CUTOFF 75 -> 84; C2 LFO PWM 0; D2 OSC 2 FINE 64 (no detune)**. Two render-only references at the same bank level: the original patch (re-trimmed to -18, its own spring, no echo) and round-1 D exactly.

| variant | VOLUME | level | (b) (re level) | peak | crest | centroid Hz | note-on MUD | tail MUD 0-250 / 250-750 / 750-1500 | harmonics 3/5/7 dB | 150-400 depth dB / Hz | 400-1.2k depth dB / Hz | first repeat re note dB / echo over spring dB | CPU |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A2 as-is | 55 | -18.0 | -23.5 (-5.5) | -5.0 | 13.0 | 564 | 278 | 1370 / 2302 / 3233 | -11 / -18 / -26 | 13.8 / 0.9 | 3.9 / 2.4 | -8.6 / +10.1 | 2084 |
| B2 more-top | 54 | -18.1 | -23.5 (-5.5) | -4.8 | 13.3 | 731 | 82 | 328 / 611 / 1009 | -10 / -16 / -20 | 13.8 / 0.9 | 4.0 / 2.3 | -8.7 / +9.1 | 2084 |
| C2 no-pwm | 55 | -18.0 | -23.4 (-5.5) | -4.9 | 13.1 | 562 | 315 | 1108 / 2198 / 3331 | -11 / -18 / -26 | 13.6 / 0.9 | 1.2 / 2.7 | -8.7 / +10.3 | 2084 |
| D2 no-beat | 73 | -20.0 | -21.7 (-1.7) | -4.3 | 15.7 | 686 | 47 | 212 / 463 / 695 | -11 / -18 / -26 | 0.3 / 0.8 | 3.1 / 0.8 | -8.8 / +9.4 | 2084 |
| Aorig orig-ref | 75 | -17.9 | -18.9 (-1.0) | -4.5 | 13.5 | 605 | 110 | 1021 / 2376 / 5592 | -11 / -18 / -26 | 13.8 / 0.9 | 3.9 / 2.4 | -189.6 / -172.0 | 2069 |
| D1 round1-D | 62 | -17.9 | -23.4 (-5.5) | -5.0 | 12.9 | 812 | 49 | 225 / 298 / 305 | -14 / -23 / -32 | 0.0 / 20.0 | 0.0 / 20.0 | -8.8 / +9.4 | 2680 |

**What each change removed (one held voice, A3, echo and deck off; band-energy depth in 23 ms frames):**
* **The beating pair is the movement in 150-400 Hz:** A2 13.8 dB at 0.9 Hz; removing the PWM (C2) leaves it 13.6 dB; removing the detune (D2, FINE 64) takes it to 0.3 dB. Opening the filter (B2) does not change it (13.8).
* **The PWM is the movement in 400-1.2k:** A2 3.9 dB; without the PWM (C2) 1.2 dB; D2 keeps 3.1 (its rate drops to 0.8 Hz, the LFO's, from 2.4).
* **The dark filter is the MUD, not the movement:** B2 (+9 steps, 988 -> 1661 Hz at C4) takes the note-on MUD from 278 to 82 and the tail MUD from 1370 / 2302 / 3233 to 328 / 611 / 1009, and leaves the movement as it was; the harmonics read -10 / -16 / -20 dB (A2 -11 / -18 / -26).
* **D2 is quieter in the tail and level-limited:** without the beating the note-on MUD is 47 and the tail 212 / 463 / 695; its crest is 15.7 dB (A2 13.0), so at the peak limit (phrase (b)'s peak -4.3 dBFS) its level is -20.0 dBFS, 0.5 dB under the band.

**The benchmark, honestly (MUD over the note-on region 10-40, tail windows no worse than about 80):** A2 278 / tail 1370 / 2302 / 3233 and C2 315 / 1108 / 2198 / 3331 are far over it (the original itself is 110); B2 82 / 328 / 611 / 1009 and D2 47 / 212 / 463 / 695 are closer; **no round-2 variant meets 10-40 and about 80**, round-1 D (49 / 225 / 298 / 305) was nearest on the tail. Vincent chooses by ear; the card will state these numbers.

**The echo against round 1's D:** first repeat re the note -8.6 dB at 337 ms delay (D -8.8), echo above spring +10.1 dB (D +9.4): the same within 0.2 dB and 0.7 dB. After the chord's note-off the echo returns -5.7 / -6.1 / -6.2 / -9.3 / -16.0 dB re the chord (D -6.0 / -6.1 / -7.2 / -10.8 / -17.7) and the spring 6.2 / 3.3 / -2.3 / -9.8 / -27.1 (D 4.5 / 2.5 / -2.2 / -11.4 / -29.0) in 0-100 / 100-250 / 250-500 / 500-1000 / 1000-2000 ms. Where they differ (the spring is +1.7 dB louder in the first 100 ms here, the later tail is the same within about 2 dB) the voice is different (a darker, beating source feeds them) and the deck is absent: this suggests the deck's absence and the source, not isolated which. The tail's MUD is the difference you can see: 1370 / 2302 / 3233 against D's 225 / 298 / 305.

**CPU:** 2084 host instr/sample worst case (idle 1180 + load 905); round-1 D 2680 (CHEW was +784 of it); the original 2069. Above the expected 1900 by about 180: the echo and spring on a 4-note chord of two oscillators through a 24 dB filter.

**Committed:** A2 as `PF_GHOST_BOARD` (VOLUME 55: -18.0 dBFS RMS on the ghost phrase, peak -5.0; phrase (b) -23.5, -5.5 dB: the slow-moving soft chords and the stabs differ), replacing round-1 B; `check_slot.py 13 A2 4b-r2`: resolved bytes identical, audio bit-identical from INIT, from the boot patch -33.2 dB (stabs) / -40.7 dB (ghost) relative to the signal (not isolated). Tables: `listen/voicing/batch-04b/13-round2/README.md`; WAVs on the listen branch only (`listen/voicing/batch-04b/13-round2/`). **Round count: 2 silent measured rounds + 1 listening round done + 1 listening round pending.**

### Recommendation (vocabulary)

**A2 (as is):** the original's dark, beating, slowly pulse-width-moving tone, untouched, into round 1's D echo and spring, no tape. It is very muddy by the ratio and that is the character Vincent chose to keep; B2 is the same with the filter opened (less mud, the movement untouched), C2 removes the slow PWM, D2 removes the beating. Turn it by ear on: CUTOFF (mud against dark), OSC 2 FINE (the beating), LFO PWM (the slow shimmer in the upper mids), and the echo (MIX, FEEDBK) and spring (DRAIN).

---

# ROUND 1 (kept as the record; superseded by round 2)


6 Nov 2026. Brief (Chapter II, The Tidal Hexes): *submerged and warped: a near-sine filtered triangle, maximum tape wow/flutter, heavy spring (the original screen brief: a 1-bit coastal deluge swamping the text). Vincent's notes: a MEDIUM level of muddy as the benchmark (MUD 150-400 over 1.2k+ roughly 10-40 over the note-on region, tail windows no worse than about 80); the Mellotron M400 (warped, wobbly tape, soft flute-like tone) to come through as much as possible, against the Space Echo's wet body: middle first, then he judges; B middle, C leans Mellotron, D leans Space Echo.* Method and kit: `README.md` here (§1 phrases, §3 loudness, §17 Batch 4B).

## RECOMMENDED: variant B (middle) — committed as the patch, awaiting Vincent's listening

**Status: round 1 rendered, not yet heard.** Variant B is committed as `PF_GHOST_BOARD` in `firmware/src/obv_patches.h` (equals variant B byte for byte: `tests/voicing/check_slot.py 13 B 4b`); the others are render-only. **Round count so far: 1 silent measured round (variants fixed by sweeps of the existing controls, not for ears) + 1 listening round pending.** No voice card and no `reference-renders/` yet. WAVs: the never-merged `listen/batch-04b-chapter2-ghost-and-reef` branch, `listen/voicing/batch-04b/13-ghost-board/`; tables: `README.md` and `probes.md` there.

### The starting point (the patch as it stood)

* **Current values (the whole list; every parameter not named is at the table's default):** O1_WAVE 2, O2_WAVE 2, O2_PW 40, O2_FINE 73, CUTOFF 75, RESO 5, FENV_AMT 74, FA 50, AA 60, AR 90, LFO_RATE 50, LFO_PHASE 2, LFO_PITCH 3, LFO_PWM 60, VINTAGE 50, SPREAD 100, REV_SIZE 100, REV_MIX 35.
* **Nearest starting patch:** PWM STRINGS (`PF_PWM_STRINGS`, 13's alone since 16 got its own array): POLY 5, a 50 % pulse and a 31 % pulse 7.0 cents sharp, a 24 dB low-pass (CUTOFF 75 = 988 Hz at C4, 50 % key tracking), a slow PWM (TRI 0.62 Hz, +-5.5 points, PHASE SPREAD), **LFO PITCH 3 (inert: the law is zero below 12)**, a spring at DRAIN 35, **no echo, no tape (CHEW 0)**. It is hot (-13.2 dBFS RMS on the ghost phrase, peak -0.2) and dark (centroid 609 Hz, MUD 108, 0.7 % above 1.2 kHz).
* **The 1-2 axes judged most uncertain:** (1) the tape wobble's depth against the tone's clarity (CHEW 70 / 100 / 127: s.d. 4.2 / 6.2 / 6.6 cents); (2) the echo and spring body against clarity (the MUD in the tail windows).
* **Control limits foreseen:** there is no triangle or sine oscillator (the nearest soft tone is a narrow pulse through a key-tracking low-pass); CHEW costs about +780 host instr/sample whenever it is on (the patch is then the heaviest voiced so far: see CPU); the deck sits LAST in the chain (VOICES, DRIVE, BBD, SPRING, TAPE) so it wobbles the whole mixed signal, not each repeat; the tape's wobble is wow-leaning at most (flutter-only reads smaller in the 100 ms-frame probe); no tempo sync, one LFO (unused here).
* **Plan:** a soft, triangle-leaning tone: a narrow pulse (PW 25 %) through a 12 dB low-pass at 100 % key tracking (the 11 / 16 D recipe) plus a copy two octaves up (OSC 2 +24 st: a measured necessity, see below); LFO PITCH **0** (not 12: the deck is the wobble, a second vibrato would only add to it) and LFO PWM 0 (PWM would change the harmonics the triangle probe reads); a short organ-like start (AA 45) and a tape-stop release (AR 80); CHEW 100 with WOW/FLT leaning to wow (48), a lower hiss (HISS 40) and fewer dropouts (DROPS 50); then BBD (275 ms, FEEDBK 82) -> spring -> deck.

### Axes chosen, variants

| variant | what | VOLUME | level (own phrase) | (b) | peak (own) | worst-case CPU |
|---|---|---|---|---|---|---|
| A original | the nearest-base patch as it stood (PWM STRINGS, 13's alone now: two pulses with PWM, LP24, a spring, no echo, no tape, inert LFO PITCH 3) | 100 | -13.2 | -14.2 | -0.2 | 2069 |
| B middle (recommended, committed) | the middle: soft near-triangle tone, tape CHEW 100 (wow-leaning), echo 275 ms FEEDBK 82 MIX 70, spring DRAIN 50 | 81 | -18.0 | -19.7 | -5.2 | 2679 |
| C tape | leans Mellotron: clearer tone (CUTOFF 60, less octave), the most tape (CHEW 127, wow), less echo (MIX 40, FEEDBK 60) and spring | 95 | -18.0 | -18.7 | -5.6 | 2679 |
| D echo | leans Space Echo: richer body (CUTOFF 66, more octave), CHEW 70, long rich echo (MIX 110, FEEDBK 100, 387 ms), more spring (DRAIN 80, SIZE 100, DAMP 55) | 62 | -17.9 | -23.4 | -5.0 | 2680 |

* **Final values (variant B), each change before -> after (the original is the nearest-base patch as it stood):**

  * O1_PW 64 -> 32 (-25%)
  * O2_PW 40 -> 32 (-6%)
  * O2_LVL 100 -> 112 (+9%)
  * O2_SEMI +0 -> +24 st
  * O2_FINE 73 -> 64 (centre 64: +9 -> +0, -7% of range) (+7.0 cents -> +0.0 cents)
  * CUTOFF 75 -> 70 (-4%) (988 Hz -> 740 Hz)
  * RESO 5 -> 0 (-4%)
  * FENV_AMT 74 -> 64 (centre 64: +10 -> +0, -8% of range)
  * KEYTRK 64 -> 127 (+50%)
  * FTYPE LP24 -> LP12
  * AA 60 -> 45 (-12%) (54 ms -> 17 ms)
  * AS 100 -> 127 (+21%)
  * AR 90 -> 80 (-8%) (558 ms -> 256 ms)
  * LFO_PITCH 3 -> 0 (-2%)
  * LFO_PWM 60 -> 0 (-47%)
  * VOLUME 100 -> 81 (-15%)
  * DLY_FB 50 -> 82 (+25%)
  * DLY_MIX 0 -> 70 (+55%)
  * REV_SIZE 100 -> 90 (-8%)
  * REV_DAMP 60 -> 40 (-16%)
  * REV_MIX 35 -> 50 (+12%)
  * CHEW 0 -> 100 (+79%)
  * TP_WOWFLT 64 -> 48 (-13%)
  * TP_HISS 64 -> 40 (-19%)
  * TP_DROPS 64 -> 50 (-11%)
  * ALLEY 0 -> 98 (+77%) (SYNC -> 275 ms)

* **Level:** VOLUME 81; **-18.0 dBFS RMS** on the ghost phrase (t: 1 + 4 + 6 note-ons, echo, spring and tape included, tails excluded); phrase (b) -19.7 (-1.7 dB); peak -5.2 dBFS; crest 12.9 dB; worst-case CPU **2679 host instr/sample** (idle 1948 + load 731; the original 2069). **That is above every voiced patch so far (15 D 2375, 10 B-style DUAL chorus 2294): CHEW alone is +784 (B with CHEW 0: 1895, `probes.md`).**
* **Measured on the recommended variant** (full tables: `listen/voicing/batch-04b/13-ghost-board/README.md`, `probes.md`):
  * **Medium muddy:** note-on MUD 18.6 (C 22.6, D 49.3, the original 108); the tail windows 0-250 / 250-750 / 750-1500 ms after the chord: MUD 74 / 89 / 17 (centroids 1103 / 1924 / 4191 Hz at -19 / -28 / -42 dBFS); C 62 / 118 / 3; D 225 / 298 / 305. B sits inside the 10-40 note-on band and under about 90 in the tail; D is the murky one (49 note-on, about 300 in the tail).
  * **The soft tone, honestly:** OSC 1 through the filter measures harmonics 3 / 5 / 7 at -14.5 / -23.2 / -32.1 dB against an ideal triangle's -19.1 / -28.0 / -34.2 (a square: -9.5 / -14.0 / -16.9); C -17.2 / -27.3 / -36.8 (nearest to a triangle), D -14.4 / -23.2 / -32.0. It is a triangle-LEANING tone, not a triangle and not a sine. **A lone soft pulse is far too dark for 'medium muddy'** (MUD 245 with OSC 2 off; CUTOFF 84 would reach MUD 4.5 but harmonics -11 / -17 / -23: no longer triangle-like): the energy above 1.2 kHz comes from the two-octave-up copy (OSC 2 LEVEL 0 / 50 / 80 / 112 / 127: MUD 245 / 163 / 59 / 18.6 / 11), which is why the second oscillator is on.
  * **Tape wobble (one voice A3, echo and spring off):** B 6.2 cents s.d. (22.3 cents 5-95 %), strongest rate 0.5 Hz, one dropout of 7.5 dB; C 6.6 cents (23.2); D 4.2 cents (13.3); the voice alone 0.0. The ladder (`probes.md`): CHEW 40 / 70 / 100 / 127 = 2.3 / 4.1 / 6.2 / 6.5 cents s.d.; WOW/FLT 127 (flutter only) reads 2.0-2.4 cents: the 100 ms-frame probe resolves the wow (0.3-0.5 Hz) but not the faster flutter, so flutter is not measured here. CHEW 127 is the most the deck gives (about 23 cents 5-95 %): 'maximum wow/flutter' of the original brief is C.
  * **Does the deck smear the top?** With the deck (CHEW 100) the note-on region has 3.7 % above 1.2 kHz and MUD 18.6; with CHEW 0, 4.6 % and 14.1: the share above 1.2 kHz falls by about a fifth and the MUD rises by about a third; the centroid goes UP (825 -> 1064 Hz) because the tape hiss adds top. The tape also lengthens the tail a little (40 dB down at 1778 ms with it, 1662 without; 20 dB: 646 / 644). For the tone the smear is small; the cost of CHEW is CPU and the tail, not the top.
  * **Echo and spring:** echo 275 ms (ALLEY 98), FEEDBK 82, MIX 70; the first repeat of an isolated 150 ms E4 is **-12.2 dB re the note** (C -17.4, D -8.8) with the echo 7.6 dB above the spring in its window; the repeats fall +0.0 -4.3 -9.0 -13.8 -18.5 -23.3 dB. Spring DRAIN 50, SIZE 90, DAMP 40: on the isolated E4 -38.3 / -13.6 / -12.9 dB re the note in 0-20 / 20-100 / 100-250 ms; after the chord's note-off the echo's return is -10.6 / -11.3 / -13.8 / -19.7 / -30.4 dB re the chord and the spring's 0.3 / -2.8 / -7.5 / -18.2 / -38.7 dB (0-100 / 100-250 / 250-500 / 500-1000 / 1000-2000 ms).
  * **What the chain order means (chain: voices, DRIVE, BBD echo, spring, TAPE deck, Tape Stop, kill switch):** the echo takes the dry voice, the spring takes voice plus echo, and the deck takes the sum of all three. So the wobble is applied to the finished wet mix at the moment it passes the deck: a repeat arriving 275 ms later is pitched by the deck's state THEN, not by the state when it was played; every layer (note, repeats, spring tail) wobbles together, coherently. A real Space Echo has its own tape inside the echo, so each repeat is warped separately (and a runaway one warps more every pass); here that is not possible, and the repeats themselves are clean copies (the BBD's band-limit only). This follows from the chain; I did not measure the wobble separately on the repeats.

### Recommendation (vocabulary)

**B (middle):** a triangle-leaning, medium-muddy tone with a 6-cent wobbling tape, a clear echo above the spring and a medium wet body. C leans Mellotron (the nearest to a triangle, the most wobble, little echo); D leans Space Echo (more echo and spring, murkier, less wobble). Turn it by ear on: CHEW (wobble, and CPU), the 2-octave copy (O2 LEVEL: the clarity/mud axis), the echo (MIX, FEEDBK), the spring (DRAIN).

### Surprising / hard with existing controls

* A soft triangle-leaning tone is NOT medium muddy by the dictionary's ratio: it needs an octave-up copy to reach MUD 10-40 (see above).
* CHEW makes this the heaviest patch so far (2679 against 2375); no lever short of CHEW 0 (-784) or dropping the echo (-16) changes it.
* The deck cannot warp each repeat separately: one wobble on the whole mix.
* The pitch-wander probe reads wow only; the flutter is not measured.

