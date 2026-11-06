# 23 · Crypt Dust · Chapter III · The Bakshi Tomes

*Voiced 6 Nov 2026 (Batch 5B), approved after listening: variant D3 (Vincent: "D3 sounds great"). Renders: `reference-renders/23-crypt-dust_D3_*.wav`. Tables (on the voicing branch): `listen/voicing/batch-05b/23-crypt-dust/README.md` and `round2/README.md`. **The brief changed after listening** (see section 4): the brief asked for noise with a thin pulse and heavy tape wow; the final patch has a trace of noise and no tape.*

## 2. What it sounds like

A thin, narrow pulse run through a band-pass into a pale, dusty tone, with only a trace of noise under it. The level flutters slowly and irregularly, in steps. A short echo and a large spring blur it. It rises slowly when you press a chord and hangs on after you let go. It is a held-chord pad; short notes are faint.

## 3. Gear inspirations (docs only, "inspired by")

- **Korg MS-20** — *noise plus a thin pulse; Thin, Gritty.* The thin pulse is a 12 % pulse (OSC 1, PW 15) and the noise is a trace: it reads 24.4 dB under the pulse in the settled chord (NOISE 43, a square law) (measured). Thin: the pulse is narrow (measured as a setting); a comparison with a thin sound was not made. Gritty: not measured.
- **Roland RE-201 Space Echo** — *the worn echo.* The echo is 75 ms at FEEDBK 60 and MIX 85: the first repeat sits 9.6 dB under the note on a short chord stab, 6 repeats stay above −40 dB under the note and 4 above −20 dB, and the echo return takes 381 ms to fall to −40 dB (measured on a probe copy with a fast attack and release). The tape wobble and lo-fi trait of the worn unit are not in this patch: the tape is off.
- **Mellotron M400** — *the dusty, pale tone as the reference.* The tone is pale in the sense of the numbers below (centroid 1970 Hz); the warped tape of the reference is not in this patch.

Closest to: **a thin pulse and a trace of dust through a band-pass, into a short echo and a large spring**.

Nothing here says the patch matches these: it was built toward the descriptions, by measurement, and approved by ear.

## 4. How to play it

- **The brief changed.** The brief was "noise + thin pulse, heavy tape wow, no drive". The final patch has **no tape at all (CHEW 0)**, and the noise is a trace. Vincent found that the noise drowned out the pulse and asked for it to be removed except for a tiny trace of dust. **Not in the final patch: the heavy tape wow and the warped tape character.** No drive (GROWL 0).
- **Hold the chord.** There is no Drone Latch: a held pad needs the key or a sustain pedal.
- **Polyphony:** POLY 4. All three keys of the A3 C#4 E4 triad sound (with POLY 2 the first key, A3, is stolen: C#4 and E4 only). CPU worst case **2065 host instr/sample** (POLY 3 1939, POLY 5 2065; the stress chord has four notes). The device render time is not measured.
- **Level:** VOLUME 120, −18.89 dBFS RMS over +4 s to +10 s of the held triad (K-weighted −17.98); the chord peaks at **−4.0 dBFS, which limits VOLUME**.
- **The noise:** NOISE 43 (a square law: −18.8 dB against 127). Noise-only against pulse-only in the settled chord: −24.4 dB. The pulse's pitch s.d. is 1.9 cents on a held A3 (no tape: this is the floor of the voices' VINTAGE and the slow filter movement).
- **The flutter:** one S&H LFO at 0.93 Hz (RATE 58) on AMP (a dip of up to 3.9 dB) and FILTER (±5.7 semitones). The deepest level dip measured is 2.4 dB on the held chord (1.5 dB on a held A3), no dip over 6 dB, no dropout: it is a mild step.
- **Tone and floor:** centroid 1970 Hz and 25.6 % of the energy above 1.2 kHz in the settled chord (4–10 s). MUD ratio over the windows 0–1 / 1–2 / 2–4 / 4–10 s: 0.11 / 0.11 / 0.14 / 0.22 (release windows 0.27–0.41). The floor after the chord is off is −73.7 / −87.3 dBFS in the 1 s windows at 17–18 s and 18–19 s, which is the echo and spring only; there is no tape hiss. The release is 20 / 40 / 60 dB down at 1914 / 3608 / 4504 ms.
- **Slow attack:** the amp attack is A100 (about 1.2 s nominal), so a 150 ms chord tap reads −32.6 dBFS (13.7 dB under the held chord) and an A4 tap −41.3 dBFS; phrase (b)'s stabs read −27.4 dBFS. It is a held-chord patch.
- **What it loses against round 1, measured.** Against the noisy D (NOISE 127): the held-chord centroid 3289 → 1970 Hz (D2, the same with two voices: 2064 Hz), the share above 4 kHz 2.5 % → 0.7 %. Against the tape versions: the tape wow (pulse pitch s.d. 7.4 cents at heavy tape B, 3.3 cents at half tape C2, here 1.9), the dropouts (4 over 6 dB, deepest 10.7 dB, at B) and the hiss floor (−53.5 dBFS at B, −65 .. −67 at C, here −74 .. −87).
- **Legato:** POLY, so the MONO / UNISON no-retrigger rule does not apply (engine fact; not tested on this patch).
- **Tricks:** SLOBBER, SEQ held (Tape Stop), the kill switch (HEEL), GROWL are untested on this patch; CHEW is off. The kill switch clears the echo buffers (engine fact; not tested here).

## 5. Final values (for debugging, not for players)

`MODE POLY (POLY 4), OSC1 PULSE PW 15 (12 %) LEVEL 127, OSC2 OFF, NOISE 43, FILTER BP12 CUTOFF 72 (831 Hz before key tracking) RESO 50 KEY TRK 64 ENV AMT 64 (zero), FILTER ENV A60 D70 S40 R60 (inert at ENV AMT 64), AMP ENV A100 D70 S100 R110, LFO S&H RATE 58 (0.93 Hz) PHASE FREE AMP 46 FILTER 45 PITCH 0, VINTAGE 30, SPREAD 60, BBD ALLEY 60 (75 ms) FEEDBK 60 TONE 55 MIX 85 PINGPONG 127, spring SIZE 127 DAMP 40 PRE-DLY 20 DRAIN 80, GROWL 0, CHEW 0, VOLUME 120` — `PF_CRYPT_DUST` in `firmware/src/obv_patches.h`.
