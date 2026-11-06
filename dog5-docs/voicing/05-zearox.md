# Voicing log — 05 "ZEAROX" (FACTORY[4], Batch 3B, the wreck and chop set)

5 Nov 2026. Brief (Batch 3B, Chapter I): *a blown-out, lo-fi kick substitute. A cranked sub with noise over the top, pushed through maximum tape degrade; it overloads on every downbeat, each note hits like a blown speaker. The kick feel must be carried by the click and the mid-range body (60-1.2k Hz), the true sub a bonus: under 60 Hz is inaudible on small speakers. The noise should be gated with the note as far as existing controls allow.*
Closest to: an 808-style kick smashed onto a blown-out cassette 4-track (TR-808 kick sub/thump, SH-101 sub/thick, Portastudio lo-fi/noisy, ProCo RAT crunchy/driven). Method and kit: `README.md` here (§1 phrases, §3 loudness, §14 Batch 3B).

## APPROVED: variant D (light), round 2 — committed as the patch

**Status: APPROVED by Vincent after listening, as rendered: variant D (light) of round 2.** Round 1 (B blown recommended, A-D rendered) was rejected after listening ("way too messy and muddy"); the round-2 direction and diagnosis are below. The array `PF_ZEAROX` in `firmware/src/obv_patches.h` equals round-2 variant D byte for byte (`tests/voicing/check_slot.py 5 D 3b-r2`: resolved bytes identical; audio bit-identical when both paths load from INIT; from the boot patch the renders differ by 1.9-2.9 dB re the signal because the S&H pitch LFO follows the engine's random state: not bit-comparable from boot).
**Final round count: round 1 = 1 silent measured round + 1 listening round (rejected); round 2 = 1 silent measured round + 1 listening round (approved at the first listening).**
Voice card: `cards/05-zearox.md`; renders: `reference-renders/05-zearox_D_{kick,stabs,riff}.wav` (kick = level phrase m).

* **Axes chosen (round 2):** where the glitch comes from (07 C's tape and random LFO -> a stepped S&H pitch LFO), how hard the signal is clipped (two-level share 43-54 % in A and B, 96 % in D), how tight the kick is (AD 76, the tightest that reaches the reference at VOLUME 123 of 127).
* **Final values:** the "Final values (variant D)" list in the round-2 section below; level -18.1 dBFS on phrase m, (b) -19.1, peak -10.7, crest 7.3 dB, worst-case CPU 1337 host instr/sample.

## ROUND 2 (5 Nov 2026): variant D (light) is the recommendation and is committed; ROUND 1 is REJECTED

**Status: round 2 rendered, not yet heard.** Vincent after listening to round 1: *"I really don't like B. It sounds way too messy and muddy. I imagined something almost pixelated and gritty, blown out in that sense. What came out was one big mess. C is the closest. I want it glitchy blown out, not muddy blown out. The saw wave needs to be replaced with a square wave. Drop the attack to 0. Drop the tape completely. Think xerox machine photocopies reduced to pure black and white: that is where my glitchy imagination came from. It also can't be the heaviest patch ... What I was describing in 05 was present in 07 Tape Splice option C (glitchy). We can take 07 C and make that 05 ZEAROX."*
New intent (replaces the round-1 brief): a pixelated, gritty, hard black-and-white kick substitute: two-level, harsh, glitchy, not smeared, not muddy; a kick at A0-A2 on the downbeat carried by a hard click and a tight body, not a fat sub; square/pulse only, attack 0, no tape (CHEW 0, HISS 0, DROPS 0), light on CPU (about 1500 host instr/sample worst case at most).
Round 2 kit: `tests/voicing/diag05.py` (diagnosis), `tests/voicing/batch03b_r2.py` (variants, element costs, probes); tables `listen/voicing/batch-03b/round2/diagnosis.md` and `.../05-zearox/README.md`; WAVs on the never-merged `listen/batch-03b-chapter1-wreck-and-chop` branch only (`listen/voicing/batch-03b/round2/05-zearox/`). Committed: variant D as `PF_ZEAROX` (equals D byte for byte; both load paths bit-identical from INIT; from the boot patch the audio differs, because the S&H pitch LFO free-runs and its random sequence follows the engine's random state: not bit-comparable). No card (after approval). **Round count so far: round 1 (1 silent + 1 listening, rejected) + round 2 (1 silent measured round: diagnosis and variant sweeps; 1 listening round pending).**

**Why round 1 B / C were muddy (diagnosis, phrase m, A1 hit, windows from the real onset):**
* B's first 20 ms are 68 % in 150-400 Hz (1.2 kHz+: 3 %), MUD (150-400 share / 1.2k+ share) 26 at 0-20 ms and 58 at 20-100 ms, and over its first 100 ms only 0.7 % of the energy is above 1.2 kHz: body, no edge. At 100-300 ms it still has 33 % under 60 Hz and 57 % at 60-150 Hz (a boom, not a tight hit); the tail is 60 dB down 62 ms after the key-up; 29 % of the samples sit near the rail.
* GROWL 104 and CHEW 127 separately (B with each off): without GROWL the tail is 60 dB down at 28 ms (62 with it) but the 1.2k+ share falls to 0.0 % and MUD rises to 151; GROWL therefore lengthened the tail by about 34 ms (this suggests its compression and trim; not isolated) and supplied the only top end there was. Without CHEW the tail is the same (60 ms), the 1.2k+ share is 1.1 % against 0.7 and the two-level share 36 % against 29: CHEW smeared the edge a little and took top off. With both off the hit is still muddy (MUD 162 at 20-100 ms, 13 % two-level): the mud is the saw through a 24 dB low-pass at CUTOFF 65, a rounded 150-400 Hz body with nothing above it.
* Round 1's C (click-led) had MUD 18 / 25 / 33 (0-20 / 20-100 / 100-300 ms), 38 % two-level and a 64 ms tail.

**What makes 07 Tape Splice C glitchy (07 C exactly, then one element at a time; phrase m re-trimmed to -18.0, phrase n the held A2):**
* **The tape (CHEW 127, DROPS 110) carries the level glitches:** 4 dips of 6 dB or more in the held A2, deepest 19 dB; with the tape off there are none. It also adds about 7 cents to the pitch spread (14.9 -> 22.0 cents s.d.), lengthens the tail (18 -> 28 ms to -60 dB) and lowers the two-level share (54 -> 46 % on m, 47 -> 35 % on n).
* **The random pitch LFO (22) carries the pitch glitch:** with the tape off the pitch s.d. is 14.9 cents, and 2.9 cents with the LFO removed (13.8 with the tape on and the LFO off: the tape's wow).
* **X-MOD 100 does not carry the pitch glitch or the dips** (pitch s.d. 15.6 without it against 14.9 with it); it makes the held note less two-level (63 -> 47 % on n, tape off).
* **The pulse waves carry the black-and-white:** saw + saw instead of pulse drops the two-level share from 54 to 24 % on m and from 47 to 21 % on n (tape off), and needs VOLUME 108 against 97.
* **None of the 07 C variants has more than 1.2 % of its energy above 1.2 kHz** (CUTOFF 60): by this measure it is not bright; what is measurable in it is the pitch jitter, the dips and the pulse waves.

**Measures new in round 2 (definitions):** BLACK AND WHITE = the share of samples within 10 % of the rail (the largest |x| of each 5 ms window) over the first 100 ms of a hit (a hard-clipped square near 100 %; a decaying body lowers it); PIXELATED = the share of the energy above 1.2 kHz over the first 100 ms, and the spectral flatness (geometric / arithmetic mean of the power spectrum, 100 Hz-10 kHz, 1 = white); MUD = the 150-400 Hz share divided by the 1.2 kHz+ share; hit-to-hit centroid spread = s.d. / mean of the first-60-ms centroid over the 8 pattern hits (the glitch's size).

**Variants (all at the VOLUME that gives -18.0 dBFS RMS over the 11 hits x 150 ms of phrase m):**

| | VOLUME | (b) | peak | CPU worst case | black and white A0 / A1 / A2 | above 1.2 kHz, A1 | MUD A1 20-100 ms | tail -60 dB (A1) | kept after a 100 Hz high-pass |
|---|---|---|---|---|---|---|---|---|---|
| A 07C | 99 | -19.6 | -12.7 | 2177 | 43 / 46 / 51 % | 0.2 % | 43.4 | 28 ms | -6.4 dB |
| B notape | 97 | -19.5 | -13.6 | 1393 | 65 / 54 / 71 % | 0.4 % | 27.6 | 18 ms | -6.5 dB |
| C kick | 124 | -19.1 | -10.8 | 1364 | 98 / 96 / 94 % | 3.5 % | 3.8 | 16 ms | -1.6 dB |
| D light | 123 | -19.1 | -10.7 | 1337 | 98 / 96 / 94 % | 3.4 % | 3.9 | 16 ms | -1.6 dB |

* **A** = 07 C as rendered, **B** = A without the tape, **C** = B reshaped as a kick (two pulses: a quiet FM'd one under the body, DRIVE 127), **D** = one square, nothing else. The reshaping steps and their effect are in the round-2 README (probes: AD, LFO PITCH, CUTOFF, DRIVE, the filter-envelope click).
* **C and D measure the same** (bands, two-level 96 %, 1.2k+ share, tail, small-speaker figure): the second oscillator, X-MOD and DRIVE add nothing these measures can see (DRIVE only matters when two oscillators are summed: with DRIVE 0 on C the two-level share is 49 %). D is the cheaper by 27 host instr/sample.
* **CPU:** D 1337 (idle 1164, the engine alone, plus 173 under load), C 1364, B 1393, A (07 C) 2177, round-1 B 2753. What each element costs on C: DRIVE 7, X-MOD 13, OSC 1 20, saw instead of pulse 13 more, the pitch LFO 0; GROWL 104 +595, CHEW 127 +784 (both off in the final).
* **D's numbers:** level -18.1 dBFS on phrase m (-1.0 dB on phrase (b)), peak -10.7, crest 7.3 dB over the phrase and 1.9 dB over the first 30 ms of an A1 hit; attack to 90 % in -0.1 ms (attack 0); A1 level -12 / -18 / -23 / -29 dBFS at +0 / 40 / 80 / 120 ms; tail 60 dB down 16 ms after the key-up (round-1 B: 62); band split of the A1 hit over 0-20 ; 20-100 ; 100-300 ms: 0/33/50/13/3 ; 0/70/13/13/3 ; 2/78/11/6/2 %. **The A0 hit is mostly sub after its first 20 ms (81 % under 60 Hz in 20-100 ms): a 27.5 Hz square is inaudible on a small speaker whatever is done**; what carries it is its first 20 ms (45 % at 60-150 Hz).
* **The glitch in D:** an S&H pitch LFO at 21 Hz, LFO PITCH 80 (+-4.7 st), PHASE FREE: a new random pitch about every 47 ms, so a hit gets 3-4 steps; hit-to-hit centroid spread 5 % (1 % with the LFO off; 10 % at LFO PITCH 110, where the MUD rises to 26.5 because the pitch falls into the body). Other rates are untested.
* **Click:** the filter-envelope click was measured and not used: closing the filter after the strike (CUTOFF 85 with ENV AMT 100-127, DECAY 25-30) leaves 1.3 % above 1.2 kHz and 85-89 % two-level, against 3.4 % and 96 % with the filter simply open; D's "click" is the 11 ms pitch drop of the square (the A1 click window, 0-10 ms, has 16 % above 400 Hz).
* **Level:** VOLUME 123 (127 is the most there is). AD 76 is the tightest decay that reaches the reference: in the AD probe (VOLUME left at 123) AD 72 reads -19.5 dBFS, AD 66 -21.7 and AD 60 -24.1, so a tighter hit would have to be read under the reference (AD 72 is inside the +-1.5 dB band at VOLUME 123, with 4 steps of VOLUME left).
* **Axes:** where the glitch comes from (A, B: the tape and the random LFO of 07 C; C, D: a stepped S&H pitch LFO), how hard the signal is clipped (two-level share 43-54 % in A and B, 96 % in C and D), how tight the kick is (AD probe: AD 60-90 gives tails of 10-16 ms; A1 falls 17 dB over the first 120 ms at AD 76).
* **Final values (variant D), each change before -> after (the original is the nearest-base patch as it stood):**

* O1_WAVE PULSE -> OFF
* O1_LVL 110 -> 40 (-55%)
* O2_WAVE SAW -> PULSE
* O2_LVL 60 -> 127 (+53%)
* O2_SEMI -12 -> +12 st
* ENV_O2 64 -> 110 (centre 64: +0 -> +46, +36% of range) (+0.0 st at the env peak -> +17.5 st at the env peak)
* O2_FINE 70 -> 68 (centre 64: +6 -> +4, -2% of range) (+4.7 cents -> +3.1 cents)
* CUTOFF 35 -> 105 (+55%) (98 Hz -> 5588 Hz)
* RESO 10 -> 0 (-8%)
* FENV_AMT 84 -> 64 (centre 64: +20 -> +0, -16% of range)
* KEYTRK 64 -> 0 (-50%)
* FTYPE LP24 -> LP12
* FA 20 -> 0 (-16%) (2 ms -> 0 ms)
* FD 50 -> 40 (-8%) (25 ms -> 11 ms)
* FS 20 -> 0 (-16%)
* AA 1 -> 0 (-1%) (1 ms -> 0 ms)
* AD 60 -> 76 (+13%) (54 ms -> 187 ms)
* AS 100 -> 0 (-79%)
* LFO_SHAPE TRI -> S&H
* LFO_RATE 70 -> 120 (+39%) (1.7 Hz -> 21.1 Hz)
* LFO_PITCH 0 -> 80 (+63%)
* GLIDE 5 -> 0 (-4%)
* VOLUME 100 -> 123 (+18%)
* TP_HISS 64 -> 0 (-50%)
* TP_DROPS 64 -> 0 (-50%)

* **Device build:** not run; the render time on the device is not measured.
* **Other programs:** the patch bytes of the other 29 programs are equal and their audio is byte-identical on all 19 phrases (`identical.py build/voicing/base 5,7,15`, base `92cf51f`, re-run with 05 = round-2 D, 07 = B, 15 = D; slot 1 is not touched); README section 14-15.

## ROUND 1 (rejected, kept for the record)

### Round-1 recommendation: variant B (blown), REJECTED — it was committed; replaced in round 2

**Status: round 1 rendered, not yet heard.** Variant B is committed as `PF_ZEAROX` in `firmware/src/obv_patches.h` (equals variant B byte for byte: `tests/voicing/check_slot.py 5 B 3b`); A, C, D are render-only. **Round count so far: 1 silent measured round (variants fixed by sweeps of the existing controls, not for ears) + 1 listening round pending.** No voice card and no reference-renders yet (after approval). WAVs: the never-merged `listen/batch-03b-chapter1-wreck-and-chop` branch, `listen/voicing/batch-03b/05-zearox/`.

* **Axes chosen:** where the kick lives (the sub OSC 1 LEVEL against the click NOISE / filter envelope: B body, C click) and the amount of overload (GROWL 104 against 55: B blown, D tamer); CHEW stays at the top in all (the brief), its effect is in the CHEW probe.
* **Final values (variant B), each change before -> after (the original is the nearest-base patch as it stood):**

* O1_LVL 110 -> 90 (-16%)
* NOISE 0 -> 50 (+39%)
* O2_LVL 60 -> 127 (+53%)
* O2_SEMI -12 -> +12 st
* ENV_O2 64 -> 110 (centre 64: +0 -> +46, +36% of range) (+0.0 st at the env peak -> +17.5 st at the env peak)
* CUTOFF 35 -> 65 (+24%) (98 Hz -> 554 Hz)
* FENV_AMT 84 -> 120 (centre 64: +20 -> +56, +28% of range)
* KEYTRK 64 -> 20 (-35%)
* FA 20 -> 0 (-16%) (2 ms -> 0 ms)
* FD 50 -> 58 (+6%) (25 ms -> 46 ms)
* FS 20 -> 0 (-16%)
* AA 1 -> 0 (-1%) (1 ms -> 0 ms)
* AD 60 -> 82 (+17%) (54 ms -> 299 ms)
* AS 100 -> 0 (-79%)
* AR 20 -> 30 (+8%) (2 ms -> 5 ms)
* GLIDE 5 -> 0 (-4%)
* VOLUME 100 -> 122 (+17%)
* GRL_BIAS 40 -> 72 (+25%)
* GRL_TONE 50 -> 64 (+11%)
* GROWL 0 -> 104 (+82%)
* CHEW 0 -> 127 (+100%)
* TP_HISS 64 -> 0 (-50%)

* **Level:** VOLUME 122; **-18.0 dBFS RMS** on the level phrase (RMS over the note-on region of the kick phrase (phrase m: 11 hits x 150 ms)); phrase (b) -19.2 (-1.2 dB), K-weighted (b) -19.4; peak -10.3 dBFS (m_kick); crest 7.8 dB on the level phrase; worst-case CPU 2753 host instr/sample (idle 2511 + load 242; the original 1361).
* **Measured on the recommended variant** (full tables: `listen/voicing/batch-03b/05-zearox/README.md`): MONO, three layers in one voice. THE SUB: OSC 1 pulse at the note's own pitch (LEVEL 90); the original was this plus a saw an octave down and nothing else (sub only: -23.5 dBFS on the kick phrase at VOLUME 100, -10.9 dB of it left after a 100 Hz high-pass, no energy above 400 Hz). THE BODY: OSC 2 saw an octave UP (SEMI +12) at LEVEL 127, swept down by the filter envelope through ENV>O2 110 (+17 st at the strike, falling over FILTER DECAY 58 = 46 ms): the 808-style chirp, and it puts the pitch in the 60-400 Hz bands. THE CLICK: NOISE 50 through the same fast filter envelope (CUTOFF 65, ENV AMT 120, SUSTAIN 0, KEY TRK 20 so a low note is not darker than a high one). The amp is a drum's: attack 0.5 ms, DECAY 82 (= 299 ms), SUSTAIN 0, RELEASE 30. THE OVERLOAD: GROWL 104 (BIAS 72, TONE 64) and CHEW 127, HISS 0. Where the kick lives on the isolated A1 hit (share of the energy above 60 Hz in the click / body / tail windows): B 78 / 86 / 62 %, the original 38 / 21 / 10 %; the click window (0-10 ms) has 19 % of its energy above 400 Hz (the original: 0), the body window 51 % at 150-400 Hz and 27 % at 60-150 Hz, the true sub (under 60 Hz) 14 % of the body. On A0 the energy above 60 Hz is 93 / 86 / 63 % (click / body / tail) and on A2 96 / 100 / 100 %. The click is spectral, not a level spike: the first 5 ms of an A1 hit sit -1.0 dB against the body (the original: +2.0), and the hit reaches 90 % of its peak at 58 ms (the sub beating with the swept body); a click that spiked over the body would need a quieter body, which the -18.0 dBFS level over a 150 ms gate does not leave room for (README section 8). A small speaker that stops at 100 Hz keeps -2.6 dB of the kick phrase (the original -10.9). Level -18.0 dBFS on the kick phrase, -19.2 on phrase (b), peak -10.3 dBFS, crest 7.8 dB over the phrase; the first 30 ms of an A1 hit have a crest of 2.8 dB (GROWL 0 on this patch: 5.7; a sine is 3). Worst case 2753 host instr/sample (the original 1361): CHEW costs 768, GROWL 579. C puts the click first (click above 400 Hz: 13 % on A1, the sub down from 90 to 70), D is the tamer overload (GROWL 55: hit crest 5.8 dB, click above 400 Hz 0 % on A1).
* **Device build:** not run (no JieLi toolchain in this environment); the change is parameter arrays only. The render time on the device is not measured.
* **Other programs:** the patch bytes of the other 29 programs are equal and their audio is byte-identical on all 19 phrases (`identical.py build/voicing/base 5,7,15`, base `92cf51f`; slot 1 is not touched, so the plain comparison holds); README section 14.
