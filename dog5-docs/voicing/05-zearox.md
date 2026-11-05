# Voicing log — 05 "ZEAROX" (FACTORY[4], Batch 3B, the wreck and chop set)

5 Nov 2026. Brief (Batch 3B, Chapter I): *a blown-out, lo-fi kick substitute. A cranked sub with noise over the top, pushed through maximum tape degrade; it overloads on every downbeat, each note hits like a blown speaker. The kick feel must be carried by the click and the mid-range body (60-1.2k Hz), the true sub a bonus: under 60 Hz is inaudible on small speakers. The noise should be gated with the note as far as existing controls allow.*
Closest to: an 808-style kick smashed onto a blown-out cassette 4-track (TR-808 kick sub/thump, SH-101 sub/thick, Portastudio lo-fi/noisy, ProCo RAT crunchy/driven). Method and kit: `README.md` here (§1 phrases, §3 loudness, §14 Batch 3B).

## RECOMMENDED: variant B (blown) — committed as the patch, awaiting Vincent's listening

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
