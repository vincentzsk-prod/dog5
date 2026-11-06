# Voicing the 32 — kit, phrases, loudness reference

How the factory patches are voiced *by ear, backed by numbers*. Nobody on the build side can hear: every claim is
a measurement from the host build (`tests/host.c` runs the firmware's own integer code, so the renders are what the
engine makes, minus the device's DAC), and every voicing round ends with WAVs for Vincent's ears. Per-patch logs live
next to this file (`03-half-life.md`, …); the approved-variant renders in `reference-renders/` (rejected variants: git history before e40f5d5, or a `listen/` branch).

**WAV rule:** listening WAVs and rejected-variant renders go ONLY on a separate never-merged `listen/<batch>` branch; main holds only `reference-renders/` (approved variants).

Rules that hold for every batch (CLAUDE.md §2, §13): **edit only the patch's own parameter values** (no engine code, no
new parameters, no layout change); gear names appear in docs and logs only ("inspired by"), never in a patch name or
on-screen string; names stay within 14 characters; `tests/run_host.sh` must pass after every commit; the other 31
programs must render byte-identically before/after (recipe at the bottom).

## 1. The audition phrases — `tests/voicing/phrases/`

Host-script format (the same as every `tests/*.txt`: `<ms> midi 0x90 <note> <vel>` …). Bare note events only, no program
select; `tests/voicing/voicekit.py` puts the program select / parameters in front. They start at 3000 ms (the splash
takes 2.4 s; the select and parameters are in at 2600 / 2610 ms so CUTOFF and RESO have slewed in). 120 BPM, so the
arp/delay-synced patches see the same tempo.

| file | what | length | it judges |
|---|---|---|---|
| `a_riff.txt` | **(a) low chopped riff**: two bars of eighths, A1 root (MIDI 33, 55 Hz) up to A2, minor third / flat seventh / fourth, two rests, gate 150 ms (60 % of a 250 ms step), velocities 90–112 | 16 steps, 4 s + tail | weight in the low register, the chop, the release on short notes |
| `b_stabs.txt` | **(b) fifth-based stabs**: root + fifth (+ octave) on the eighth grid (E2+B2, E2+B2+E3, G2+D3, A2+E3, A2+E3+A3, D2+A2, E2+B2+E3), 7 stabs, gate 180 ms, velocities 95–112 | 7 stabs, 4 s + tail | chord body, voice stealing (3-note stabs need 6 cards in DUAL), brightness, **the loudness reference is read here** |
| `c_held.txt` | **(c) one held note released**: A2 (MIDI 45, 110 Hz) held 2.4 s, 2.6 s tail, then A3 for 120 ms and A2 for 150 ms | ≈ 8.8 s | slop and detune beating over the held part, release timing and sputter, what the tail does to a short note |

| `d_lead.txt` | **(d) single-note lead** (Batch 1A, for mono leads): a legato run A3 C4 D4 E4 A4 (each note-on 50 ms *before* the previous note-off, 350 ms apart), the last A4 held 1 s, a staccato run (six 120 ms notes, 300 ms apart), one A3 held 800 ms | ≈ 7 s + tail | the sweep of one note, legato vs retrigger, the dead stop. **Replaces (b) as the level phrase for a mono lead** (V-Sync) |
| `e_lowuni.txt` | **(e) low unison** (Batch 1A, for stacked basses): A1 (55 Hz) held 3 s, A0 (27.5 Hz) held 1.5 s, chopped roots (eighths, 130 ms gate: A1 A1 A2 A1 G1 A1 E1 A1), A2 held 800 ms | ≈ 10 s + tail | weight under 150 Hz, the width of the stack, the chop, headroom with eight voices on one note. **Replaces (b) as the level phrase for a unison bass** (THE DØG) |

| `f_slow.txt` | **(f) slow, low** (Batch 2A, for 17 Titanic): A1 (55 Hz) held **10 s**, released, the host script runs to 18.5 s so the whole release is measured | 12 s of note + tail | the bloom/settling over a long hold (brightness and level against time), the steady weight, beat and wander, the release. **The level phrase of the slow patches** (§10) |
| `f2_slowmid.txt` | **(f2) slow, mid** (Batch 2A, for 21 Cowl Shadow): the same hold an octave up, A2 (110 Hz) | the same | the same, where a brass wall reads as brass (at 55 Hz it is a rumble) |
| `g_skank.txt` | **(g) skank** (Batch 2A, for 09 Skeenhead): off-beat two-note minor dyads at 120 BPM (250 ms after each beat), gate 110 ms, vel 96-108: four on A minor (A3 C4), two on D minor (D4 F4), **two empty off-beats (the stabs either side are 1.5 s apart)**, A minor twice, E minor (E4 G4) last, then 3.5 s of nothing | 11 stabs, 9 s + tail | the plop per stab, the chirp of the spring, how the tail sits between stabs (the gap), the tail length. **The level phrase of a spring stab patch** |
| `h_surf.txt` | **(h) surf bass** (Batch 2A, for 11 Slapback Strut): single-note staccato eighths at 120 BPM, A1 (33) up to A2 (45) with C2 D2 E2 G2, gate 100 ms (40 % of a step, so an ~80 ms echo is a separate slap), vel 98-112, two bars, a 750 ms rest, one last A1, 2.5 s of nothing | 17 notes, 8 s + tail | the pluck, the roundness of one oscillator, how loud and how long the slap is. **The level phrase of an echo bass** |
| `x_register.txt` | **(x) register tilt**, measurement only (Batch 2A): the same velocity on A1, A2, A3, each held 1.5 s | 8 s | how many partials the filter lets through per octave (KEY TRK / CUTOFF): the bass compensation of 17 |
| `i_spit.txt` | **(i) spit** (Batch 3A, for 01 Red Pill): a nervous riff of sixteenths at 120 BPM (125 ms), A1 (55 Hz) with C2 D2 E2, gate 80 ms, five rests; then three ISOLATED notes with 1.2 s+ of silence after each: A1 gate 150 ms (6000 ms), D2 gate 150 ms (7500), A1 gate 300 ms (9000) | 11.4 s | the spit and grit of a low line, and the **wet return per time window** on the isolated notes (0-20 / 20-100 / 100-250 ms). **The level phrase of 01** |
| `j_grind.txt` | **(j) grind** (Batch 3A, for 02 Cement Grind): eight quarter notes at 120 BPM with a long gate (400 ms: a 6-9 Hz PWM swings 2-3 times inside each), A2 (110 Hz) with C3 D3 E3 G2; A2 HELD 2.4 s at 7200 ms (where the PWM is read); three chops A3 A2 E3 (150 ms) | 13 s | the PWM (rate, depth, whether it is obvious on the riff), thickness, bite. **The level phrase of 02** |
| `k_wall.txt` | **(k) wall** (Batch 3A, for 06 zzuFuzz): A2 held 3 s (sustain against time), a held power chord A2+E3+A3 1.5 s, three 300 ms power-chord stabs 800 ms apart (E2+B2+E3, G2+D3+G3, D2+A2+D3), one low A1 held 1.2 s; rests of 0.5-1 s after the note and the chord | 14.5 s | **sustain and the tail** of a fuzz, the size of the wall on chords (three notes: a DUAL patch needs POLY >= 6). **The level phrase of 06** |
| `l_wire.txt` | **(l) wire** (Batch 3A, for 08 Wire Bite): A4 (440 Hz) held 3.5 s (drift, stack and the zap of the start), eight bites on a 250 ms grid (E5 A4 C5 A4 D5 A4 E5 A4, gate 110 ms), A3 held 700 ms; detached notes only | 12.8 s | the high register: drift, zap, chop. **The level phrase of 08** |
| `m_kick.txt` | **(m) kick** (Batch 3B, for 05 ZEAROX): three ISOLATED hits with 1.35 s of silence after each (A0 27.5 Hz at 3000 ms, A1 55 Hz at 4500, A2 110 Hz at 6000), then four hits a bar at 120 BPM (500 ms) for two bars on A1 from 8000 ms (vel 112 100 106 100), every gate 150 ms, then 2.5 s of nothing | 11 hits, 11.5 s + tail | the click, the mid-range body and the sub of a kick substitute **by band split in the 0-10 / 10-50 / 50-150 ms windows**, the register (A0 is inaudible on a small speaker), the noise and hiss after the last note-off. **The level phrase of 05** (note-on region, 11 x 150 ms) |
| `n_splice.txt` | **(n) splice** (Batch 3B, for 07 Tape Splice): twelve staccato sixteenths at 120 BPM (125 ms), gate 60 ms, A2 (45) with C3 D3 E3 G3 and E3 D3, then A2 HELD 2.4 s from 6000 ms, then three 80 ms A3 notes | 12 + 1 + 3 notes, 8.5 s + tail | the X-mod wobble and the tape's wander over a held note, the chop, the tape's timing jitter at the note edges. **The level phrase of 07** |
| `o_chop.txt` | **(o) chop** (Batch 3B, for 15 Trem Chop): A3 (220 Hz) HELD 2.4 s from 3000 ms (the chop alone), a six-note riff of 500 ms notes (A3 C4 E4 D4 C4 A3, 600 ms a step: several LFO cycles inside each), the chord A3 + E4 + A4 held 1.2 s from 10000 ms | 9 s + tail | chop rate, depth and edge hardness over a long note, whether the chop restarts with each note (LFO PHASE), the chord on a MONO / DUAL patch. **The level phrase of 15** (note-on region including the off parts of the chop) |
| `p_chopshort.txt` | **(p) chop vs gate** (Batch 3B, for 15 Trem Chop): eight eighths at 120 BPM (250 ms) on A3 with C4 D4 E4, gate 110 ms, then four quarter-note notes with a 240 ms gate | 12 notes, 5.5 s + tail | how the chop sits against the gate; whether each note starts on an on or an off part (LFO PHASE SYNC against FREE) |
| `q_organ.txt` | **(q) organ** (Batch 4A, for 10 Atlantic Swell): the A minor triad A3 C4 E4 held 2.4 s (3000 ms), 2 s gap, ONE isolated 120 ms E4 (7400 ms; the delay's first repeat), 2.5 s gap, four staccato notes E4 G4 A4 C5 (120 ms, 300 ms apart, from 10000 ms), 1.2 s gap, the D minor triad D4 F4 A4 held 1.6 s (13000 ms), 2.4 s of nothing | 11 note-ons, 17 s | note definition under a heavy modulation and a heavy echo, the chorus / vibrato / tremolo on held notes, the echo's level and rhythm, the repeats piling onto the figure. **The level phrase of 10** (note-on region, echo included, tails excluded) |
| `r_tangle.txt` | **(r) tangle** (Batch 4A, for 12 Kelp Tangle): A2 (110 Hz) HELD 3.2 s alone (3000 ms: where the PWM is read), 1.8 s gap, the chord A2 E3 C4 held 3.0 s (8000 ms), 2.2 s gap, then six 150 ms notes A2 C3 D3 E3 G3 A3, 400 ms apart, from 13200 ms, 3 s of nothing | 10 note-ons, 18.5 s | PWM audibility through a murky filter (rate and depth by band), the dense chord, the spring tail after a held note and after short notes. **The level phrase of 12** |
| `s_wash.txt` | **(s) wash** (Batch 4A, for 16 Tidal Pull): A minor 7 A3 C4 E4 G4 held 2.0 s (3000 ms), 2.6 s gap, F major 7 F3 A3 C4 E4 held 2.0 s (7600 ms), 2.6 s gap, three 400 ms notes E4 C4 A3 (900 ms apart, from 12200 ms: the attack as a ramp), three 100 ms stabs of A3+E4 (600 ms apart, from 15000 ms: what a medium attack does to a short note), 3 s of nothing | 17 note-ons, 20.5 s | the wash, the delay audible against the spring (the gaps make the repeats and the tail separable), the attack. **The level phrase of 16** |
| `t_ghost.txt` | **(t) ghost** (Batch 4B, for 13 Ghost Board): the A minor 7 chord A3 C4 E4 G4 held 2.4 s (3000 ms), 2.6 s gap, a slow single-note line E4 D4 C4 A3 (800 ms notes, 500 ms apart, from 8000 ms), 2.1 s gap, six 150 ms notes C4 E4 G4 E4 C4 A3 450 ms apart from 14700 ms, 3.4 s of nothing | 11 note-ons, 20.5 s | the tone, the beating on a held chord and on single notes, the echo and spring bodies (the gaps), the short notes (round 1 also judged a tape deck). **The level phrase of 13** |
| `u_crash.txt` | **(u) crash** (Batch 4B, for 14 Reef Break): one LOW hit A1 (3000 ms), 3.5 s gap, one MID hit A2 (6500 ms), 3.5 s gap, then A1 hits 1000 ms apart (10000, 11000, 12000), 600 ms apart (13500, 14100, 14700) and 400 ms apart (16200, 16600, 17000), 3.5 s of nothing; every gate 300 ms, velocity 108 | 11 hits, 20.5 s | the burst and its attack, the cymbal-like decay, the sub, the echo against the next hit. **The level phrase of 14** (note-on region = the 300 ms gates) |
| `v_drone_lo.txt` | **(v lo) drone, low** (Batch 5A, for 18 Roto-scopo and 19 Blackwater): ONE note, A1 (MIDI 33, 55 Hz), held **15 s** from 3000 ms, released at 18000 ms, the script runs to 22.5 s | 15 s hold + 4.5 s release | the drone itself: wander over time (windowed centroid), the settled level (**the level phrase of 18 and 19: RMS over +5 s .. +14 s after the note-on**), the weight, the release |
| `v_drone_mid.txt` | **(v mid) drone, mid** (Batch 5A, for 22 Melting Orb; also 18 and 19): the same hold on A2 (MIDI 45, 110 Hz) | the same | the melt of 22 over its first 8 s; **the level phrase of 22: RMS over +9 s .. +14 s (the melted state)** |
| `w_chord_lo.txt` | **(w lo) held chord, low** (Batch 5A, 18 / 19): A1 + E2 + A2 (33, 40, 45) together, held 8 s, released at 11000 ms | 8 s + 3.5 s tail | what the patch does with three keys (UNISON and MONO play the last key only) |
| `w_chord_mid.txt` | **(w mid) held chord, mid** (Batch 5A, 22): A2 + E3 + A3 (45, 52, 57), held 8 s | the same | the same, one octave up |
| `y_tap.txt` | **(y) taps** (Batch 5A): A1, A2 and A3 each tapped 150 ms (3000 / 6000 / 9000 ms), 2.85 s of nothing after each | 13 s | what a drone sounds like when it is not held: the open start, the release |
| `z_chord.txt` | **(z chord) held triad, mid** (Batch 5A round 2, for 19 Micro-mist): A3 C#4 E4 (57, 61, 64) held 10 s from 3000 ms, released at 13000, the script runs to 19 s | 10 s hold + 6 s release | the mist: strike and settled tone, the echo's build-up, the hover after the key-up. **The level phrase of 19: RMS over +4 s .. +10 s** |
| `z_tap.txt` | **(z tap)** (Batch 5A round 2, 19): the triad tapped 150 ms (3000 ms), then A4 tapped 150 ms (8000 ms), 4.8 s of nothing after each | 10 s | what a tap leaves: the level against the held chord, the hover |
| `z_single.txt` | **(z single)** (Batch 5A round 2, 19): A4 (69) held 6 s from 3000 ms | 11 s | a lone upper note: peak, strike and settled tone of one voice |

Anything new goes in the same folder with a header comment saying what it judges, and gets one line in
`PHRASE_FILES` (voicekit.py).

## 2. The kit — `tests/voicing/voicekit.py`

```
python3 tests/voicing/voicekit.py bank            # RMS / K-RMS / peak of all 32 factory slots on phrase (b)
python3 tests/voicing/half_life.py                # the 03 Half-Life round (variants -> listen/voicing/03-half-life/ + README)
python3 tests/voicing/batch01a.py [--only SLOT] [--quick]   # Batch 1A (30, 31, 04, 25): variants -> listen/voicing/batch-01a/<NN-name>/
python3 tests/voicing/batch01a.py --emit SLOT KEY # the C array (overrides over the defaults) of a variant, ready for obv_patches.h
python3 tests/voicing/batch02a.py [--only SLOT] [--quick]   # Batch 2A (17, 21, 9, 11): variants -> listen/voicing/batch-02a/<NN-name>/ (WAVs only on the listen branch)
python3 tests/voicing/batch02a.py --emit SLOT KEY # the C array of a Batch 2A variant, ready for obv_patches.h
python3 tests/voicing/batch02a.py --index         # listen/voicing/batch-02a/README.md from the four results.json files
python3 tests/voicing/batch03a.py [--only SLOT] [--quick] [--no-cost]   # Batch 3A (1, 2, 6, 8): variants -> listen/voicing/batch-03a/<NN-name>/ (tables on voicing/, WAVs only on the listen branch)
python3 tests/voicing/batch03a.py --emit SLOT KEY # the C array of a Batch 3A variant
python3 tests/voicing/batch03b.py [--only SLOT] [--quick] [--no-cost]   # Batch 3B (5, 7, 15): variants -> listen/voicing/batch-03b/<NN-name>/ (tables on voicing/, WAVs only on the listen branch)
python3 tests/voicing/batch03b.py --emit SLOT KEY # the C array of a Batch 3B variant;  --readme rewrites README.md / numbers.md / the index from results.json;  --logs "text" writes the voicing logs
python3 tests/voicing/batch04a.py [--only SLOT] [--quick] [--no-cost] [--no-wav]   # Batch 4A (10, 12, 16): variants -> listen/voicing/batch-04a/<NN-name>/ (tables on voicing/, WAVs only on the listen branch)
python3 tests/voicing/batch04a.py --emit SLOT KEY # the C array of a Batch 4A variant;  batch04a_probes.py = probes.md (one control stepped);  batch04a_docs.py = the logs and the index README
python3 tests/voicing/batch04b.py [--only SLOT] [--quick] [--no-cost] [--no-wav]   # Batch 4B (13, 14): variants -> listen/voicing/batch-04b/<NN-name>/;  --emit SLOT KEY;  batch04b_probes.py = probes.md;  batch04b_docs.py = the logs and the index README
python3 tests/voicing/batch05a.py [--only SLOT] [--quick] [--no-cost] [--no-wav]   # Batch 5A (18, 19, 22): variants -> listen/voicing/batch-05a/<NN-name>/ (tables on voicing/, WAVs only on the listen branch); --emit SLOT KEY; --report rewrites the READMEs from results.json
python3 tests/voicing/batch05a_docs.py                                         # the approved Batch 5A logs (18, 22) from results.json
python3 tests/voicing/batch05a_r2.py [--quick] [--no-cost] [--no-wav] [--emit KEY] [--report]   # Batch 5A round 2: the new slot 19 Micro-mist, four fresh takes -> listen/voicing/batch-05a/19-micro-mist/ (+ batch05a_r2_variants / _report / _docs)
python3 tests/voicing/identical_par.py build/voicing/base 18,19,22             # identical.py on all cores (the same proof; 29 phrases x 32 slots x 2 builds is over an hour in series)
python3 tests/voicing/check_slot.py SLOT KEY [round2|3a|3b|4a|4b|5a]   # the committed slot against its variant: resolved bytes, and the audio from the boot patch and from INIT
build/voicing/dump_patch 3                        # slot 3 resolved (defaults + overrides), "*" = differs from the default
build/voicing/dump_patch all                      # slot, name, hash of the 96 patch bytes (the byte-identical check)
```
(`dump_patch` is built by `cc -Ifirmware/src -Ifirmware/gen -o build/voicing/dump_patch tests/voicing/dump_patch.c`.)

* `render(exe, phrase, program=N)` renders the tree's slot N+1 as it stands; `render(exe, phrase, params={…})` renders a
  **variant**: INIT (program 33, all defaults) with every parameter given set 10 ms later. A variant is therefore a
  complete parameter list and never depends on what the tree's slot holds, so the original ("A") stays reproducible
  after the slot is changed. Proof the mechanism is exact: slot 3's original list set over INIT renders **bit-identical**
  to `midi 0xC0 2` on all three phrases (`half_life.py` re-checks this against the pre-change commit each run).
* The parameter must come **10 ms after** the program change: the MIDI queue is read by the main loop, and a `param`
  in the same millisecond is overwritten when the program change lands.
* Renders are deterministic (same script → same WAV, sample for sample), so before/after comparisons are exact.

## 3. LOUDNESS REFERENCE — the method

Every patch in the bank is matched to one level, so that switching programs live never surprises the PA.

**Measured on phrase (b), `b_stabs`, the stereo render at the MASTER knob all the way up (the host WAV):**

* **RMS dBFS over the note-on region** — the samples between each stab's note-on and note-off (7 × 180 ms = 1.26 s;
  release tails and silences excluded), both channels in one power average, full scale = 32767:
  `10·log10( mean(L²+R²)/2 / 32767² )`.
* **Peak dBFS** — the largest sample magnitude of the whole render (tails included), `20·log10(max|s| / 32767)`.
* *K-weighted RMS* — the same RMS after BS.1770 K-weighting (shelf + 38 Hz high-pass). Informational: a bass-heavy
  patch reads louder in plain RMS than it sounds; if the two disagree by more than ~1.5 dB, Vincent's ears decide.

**BANK REFERENCE LEVEL: −18.0 dBFS RMS on phrase (b)'s note-on region (peak ≤ −4 dBFS) — §5.** A later patch is matched
within ≈ 1.5 dB of it, by `VOLUME` (a square law: `gain = VOLUME²/4096·…`, about 0.17 dB a step at 100; 100 is the default,
127 is +4.1 dB) and *last*, after the tone is right. Peaks stay under −4 dBFS so GROWL/CHEW and the master have room. The
Psych Chain macros are loudness-held by design (CLAUDE.md §6), so a patch measured with them at 0 stays near its level
with them up; patches whose whole point is the chain (05 ZEAROX, 06 zzuFuzz, 14 Reef Break …) are measured with
their macros *on* — and say so in their log.

Where the bank stood before voicing (untouched slots, phrase (b), RMS / peak): median ≈ −21 dBFS, range −44 (14 Reef
Break, a noise burst; 23 Crypt Dust, a wash) to −11.7 (24 SAWTOOTH, peak 0.0). Run `voicekit.py bank` for the table.

## 4. What the numbers mean (columns in each patch's README table)

| column | definition |
|---|---|
| RMS / peak / K-RMS | §3, per phrase; "vs ref" = RMS − the bank reference |
| centroid | spectral centroid in Hz of the note-on region (phrase b unless said), mono sum, 2048-point Hann FFT, |X|-weighted per frame and frames weighted by energy |
| low share | % of that energy below 150 Hz — the "weight" |
| beat | the beating of the detuned pair, read from phrase (c)'s held A2: the amplitude envelope (analytic signal) of the band f0 ±15 % in 1 s windows, its strongest component 0.3–12 Hz = the beat rate (mean, min–max over the held note) and the envelope's peak-to-peak depth in dB |
| detune | the engine's DETUNE law: DUAL separates the pair by `DETUNE²/64` Q8-semitones = `DETUNE²/64·100/256` cents, plus each card's own VINTAGE tune offset (±8 cents at 127) |
| wander | the engine's own log of each card's vintage pitch (the host-only `vlog`): mean (static offset, cents), s.d. and range of the random walk over the held note — exact, not estimated from audio |
| release −20/−40/−60 | ms after note-off for the envelope to first fall 20/40/60 dB below its level before release (2 ms frames) |
| span | time between the first and the last crossing of −40 dB: 0 = a smooth fall, more = the tail opens and shuts inside it |
| re-rises | how many times the tail climbs back ≥ 6 dB out of a dip (6 dB hysteresis) — a count of sputters |
| flutter | s.d. (dB) of the held body's 10 ms level — what the VCA LFO does before the release |
| cost | host instructions per sample on phrase (b) under callgrind (`tests/perf_callgrind.sh`'s yardstick, a *relative* number: dog5-docs/PERF-BASELINE.md) |

## 5. The reference, and engine facts every batch reuses

**BANK REFERENCE LEVEL = −18.0 dBFS RMS** (phrase (b), note-on region, MASTER up) — set by 03 Half-Life, 4 Nov 2026.
Tolerance for every other patch: ±1.5 dB (aim ±0.5; VOLUME's step is 0.17 dB). Peak (whole render) ≤ −4 dBFS; Half-Life
peaks at −6.0. K-weighted RMS is reported next to it, not matched (Half-Life: −18.7).

Why −18: the untouched bank sat anywhere from −44 to −11.7 (median ≈ −21), so no value is "already right"; −18 is where
the flagship's original sat (−17.6, so it hardly moves), it leaves 12+ dB between the loud-playing level and full scale
for GROWL/CHEW and a hot MASTER, and VOLUME has room both ways (100 is the default, 127 is +4.1 dB, 60 is −8.5 dB).
Level-match **last**, with VOLUME, after the tone is right; never with the oscillator levels (they are the tone).

**VINTAGE in cents** (the engine's own log, `tests/voicing/slop_table.py`; a note held 13 s, DUAL = two cards; the card
offsets are fixed per card, the wander is a random walk with a ≈ 0.7 s time constant):

| VINTAGE (patch + ride) | engine value | static offset of the two cards (cents) | wander s.d. | wander range |
|---|---|---|---|---|
| 30 (the default) | 30 | −2.1 / +0.5 | 1.4 / 1.5 | −6..+4 / −6..+7 |
| 55 | 55 | −3.6 / +1.6 | 2.5 / 2.8 | −10..+7 / −10..+13 |
| 90 | 90 | −5.9 / +2.6 | 4.0 / 4.6 | −17..+12 / −18..+22 |
| 100 | 100 | −6.2 / +3.0 | 4.5 / 5.1 | −18..+14 / −20..+24 |
| 127 (the knob's top) | 127 | −7.7 / +3.6 | 5.7 / 6.5 | −23..+18 / −25..+30 |
| 90 + the SLOP ride at 127 | 344 | −19.9 / +10.9 | 15.7 / 17.5 | −62..+49 / −66..+84 |
| 127 + the ride at 127 | 381 | −22.1 / +11.9 | 17.3 / 19.4 | −69..+54 / −73..+93 |

**The ride adds up to 254, not 127** (`SLOP_SCALE_X2 4`: the encoder's 0..127 doubled, CLAUDE.md §5, chosen by ear 3 Nov),
and the sum is allowed to 381 (`SLOP_MAX`), so no VINTAGE value from 0 to 127 ever clips the ride: headroom is about how
much the ride *multiplies* the patch's own slop (patch 90: ×3.8; 127: ×3.0; 55: ×5.6), not about a clamp. The patch's
own slop tops out at a 6 cent s.d.; the "dying tape motor" territory is the ride's.

**The VCA / release, as the engine does it** (`obv_engine.h`): the amp envelope is an analog RC fall, the release time
(0.5 ms · 20000^(v/127), the *5 %* point; the voice is freed at −78 dB, about 3× that) is scaled per card by VINTAGE (±12 %
on the rate at 127, ±37 % at the ride's top), and the VCA also takes the LFO: `AMP` (LFO → amp) multiplies the voice by
`1 − AMP/256 · (1 − lfo)` (lfo −1..+1), so SQUARE at AMP 127 swings between full level and silence (a hard gate) and a lower AMP swings between full level and a dip of `AMP/128`. **LFO DELAY is a per-note
fade-in of every LFO destination** (`5000 ms · (v/127)²`, then a ramp half as long again): until it has run, the LFO is
held at its centre, so with AMP set the note first sits at a fixed `1 − AMP/256` (−3 dB at AMP 80) and the chop grows in
after. That is the only note-age control the engine has — **there is no release-triggered modulation**; a "VCA that
sputters on release" is made from a gate-chop LFO that fades in around the time a staccato note lets go (03-half-life.md).

## 6. The "other 31 are untouched" proof

```
git archive <commit before> | tar -x -C build/voicing/base      # the firmware as it was
# build both host apps, render all 32 slots on phrase (b) with each, compare byte for byte:
python3 tests/voicing/identical.py build/voicing/base 30,31,4,25  # exit 0 = only the named slots differ (default: slot 3)
build/voicing/dump_patch all                                     # and the 96-byte patch hashes, before and after
```

## 7. Batch lessons from the pilot (03 Half-Life)

* **Round budget:** one silent measured round (design decisions fixed by sweeps, not for ears) plus **two listening
  rounds** per patch; **one plus one** for plain nearest-base re-voices. Half-Life, approved as is after its first listening round, took 1 + 1.
  The silent round is the cheap, useful one; each listening round is the slow one. A voice card (`cards/`) is written once approved.
* **Voice-stealing rule:** in DUAL every note is two voices, so **POLY must be at least 2× the notes played on chords**
  (a fifth-and-octave stab = 3 notes = POLY 6; the default 5 played it with a hole, 5 voices not 6). Voice the chord phrase with the real chord size.
* **LFO DELAY fades every LFO destination toward its centre**, not just the LFO's onset: until it has run, the LFO is held at
  zero, so with AMP set the note sits at a fixed dip (`1 − AMP/256`, −4 dB at AMP 100) and the modulation grows in afterwards
  (`5000 ms · (v/127)²`, then a ramp half as long). It is the engine's only note-age control; budget the dip into VOLUME.
* **The sputter recipe** (Half-Life): LFO **SQUARE**, **~20 Hz** (RATE 119), **AMP 100**, **LFO DELAY ~112 ms** (19), AMP RELEASE ~62.
  A staccato note of ~150–180 ms has a clean body and a chopped tail. SQUARE works; S&H and RANDOM did not (mostly under 5 dB of re-climb).
  **Limitation: the chop follows note age, not gate close.** There is no release-triggered modulation, so a note held past ~170 ms
  spits all the way through, and notes under ~100 ms catch only the start of it. A true release-only sputter needs an engine change.
* Level-match last, with VOLUME; the kit's `half_life.py` is the template for a round (variants table, trim to reference, measure, write).

## 8. Batch lessons from 1A (30 THE DØG, 31 Fi(l)fth, 04 V-Sync, 25 SAWTOOTH)

* **The batch kit is data, not code:** `tests/voicing/batch01a_variants.py` holds each patch's variant table (changes over the original, which `batch01a.py`
  reads from the base tree's own resolver, so it can never drift), the phrases it is judged on and its texts; `batch01a.py` trims VOLUME to the reference on the patch's
  *level phrase*, measures, writes the WAVs, `README.md`, `numbers.md`, `results.json`. A new batch is a new table.
* **A level phrase per patch:** (b) for chord patches, (d) for a mono lead, (e) for a unison bass; (b) is always reported next to it, with the difference.
* **A variant's audio is not bit-exact against the program-load render.** `CUTOFF` / `RESO` slew in with `x += (target − x) >> 6`, which stops up to 63/256 st
  *short* when approaching from below (a floor), so the same patch lands a fraction of a semitone apart depending on where it came from; a DRAIN patch's spring
  also starts at another moment. Measured error −27 … −43 dB. The kit therefore renders **A through the base program path** and B–D over INIT; the *committed* slot
  and its variant matched bit for bit in all four patches (cutoff approached from the same side). The pilot's "bit-identical" check held because Half-Life has no spring.
* **GROWL costs ~580 host instr/sample whether or not anything sounds** (an always-on stage): the "cost under load" column is marginal (it subtracts the same script
  without notes), so the table also shows *idle* and *worst case = idle + load*. Low GROWL is nearly inert by the numbers (a touch of 6 on the brass: −1.0 dB of peak,
  −7 Hz of centroid; 18 on the unison stack: 0.25 dB, +4 Hz; higher GROWL compresses and darkens, because its pre-clip low-pass closes), so Batch 1A leaves it at 0 where it
  could not be heard to earn its cost, and keeps it on only in the variants whose point it is.
* **GROWL leaves a small constant DC offset after the note** (the 10 Hz DC blocker's integer rounding sticks: −44 … −53 dBFS, more in MONO). Inaudible; it hides a release's
  last 40 dB, so the kit's release columns subtract the constant the tail settles on.
* **MONO and UNISON do not re-fire the envelopes on a legato note** (a key still held: slide, no retrigger), so a sync sweep or a filter snap happens on *detached* notes only.
* **The level knobs are square laws** (`LEVEL²/128`): OSC 1 at 50 against OSC 2 at 127 is 16 dB down (inaudible as "fat"), at 80 it is 8 dB down. Judge a balance in dB, not in knob steps.
* **A fast amp pluck cannot reach the bank reference:** a stab whose amp dies in the 180 ms gate has a ~17 dB crest, and −18 RMS would need VOLUME above 127. Put the pluck in the
  *filter* envelope and let the amp keep a body.

## 9. Batch 1A lessons (short)

Approved 5 Nov 2026: 30 THE DØG (H, 2 listening + 2 silent rounds), 31 Fi(l)fth (C), 04 V-Sync (D), 25 SAWTOOTH (B) (1 + 1 each). §8 has the kit detail.

* **Per-voice DRIVE (FILTER+ page) beats GROWL for warmth and presence.** GROWL is inert below about 28, compresses past about 40 (crest 9.5 → 7.0 dB at 55, fuzz at 70), and costs ~+595 host instr/sample whenever it is on;
  DRIVE adds harmonic density with no compression, takes a dB or two off the top (warm), and costs ~+100. BIAS exists only inside GROWL and raises peaks, not presence.
* **Diagnose "thin" with the band split** (<60, 60–150, 150–400, 400–1.2k, 1.2k+ Hz as % of energy, `tests/voicing/dog_metrics.py`). Energy under 60 Hz is inaudible on small speakers: B had 57 % there, so it measured
  "85 % under 150 Hz" and still read thin. And no oscillator / filter lever moves the split more than ~±1.5 dB at equal level; width, level and drive are what change the feel.
* **Measure the attack snap over the whole hold, not the last 110 ms:** a beating stack moves the short-window body level by ±2 dB with the beat phase. Read the chopped roots too, and the attack-to-body brightness ratio.
* **Level knobs are square laws** (`LEVEL²/128`): a balance is in dB, not knob steps (OSC 1 at 50 against OSC 2 at 127 is 16 dB down, inaudible).
* **Legato does not re-fire the envelopes in MONO / UNISON:** a sync sweep or filter snap happens on detached notes only (04 V-Sync's card says play it staccato).
* **Variant renders are not bit-exact against program-load renders on spring patches** (the spring's state starts at another moment; CUTOFF / RESO slew rounding): render the original through the base program path; the committed
  slot and its approved variant matched bit for bit in all four patches.
* **DUAL needs POLY ≥ 2 × the notes:** verified for 31 C with the host's `expect voices` (`tests/voicing/dual_voices_31.txt`): a three-note chord gates 6 voices, a fourth note 8.
* **The flagship (30) deliberately sits at −16.5 dBFS RMS** (+1.5 dB over the −18.0 reference, the top of the tolerance band, peak −7.3): presence was its brief. It is **not a precedent**: match the others to −18.0.
* **Proof for the whole batch** (`identical.py build/voicing/base 30,31,4,25`, base = the commit before Batch 1A): only slots 30, 31, 4 and 25 changed; the other 28 programs are byte-identical on all six phrases and their 96-byte patch hashes are equal.

## 10. Batch 2A — weight and space (17 Titanic, 21 Cowl Shadow, 09 Skeenhead, 11 Slapback Strut)

The kit is `tests/voicing/batch02a.py` (driver), `batch02a_metrics.py` (the measures) and `batch02a_variants.py` (the variant tables and texts), the same method as 1A (§8): a variant is a full
parameter list over INIT, A is rendered through the base program path, VOLUME is trimmed last. **Two-branch rule (new):** code, docs, logs, cards and the small README/numbers tables go on the
`voicing/` branch that is merged; **every listening WAV lives only on the never-merged `listen/` branch** (`listen/voicing/batch-02a/` and nothing else), so the merged history does not grow; the one exception on main is `reference-renders/` (approved variants only).

**How the level is read, per kind of patch** (the reference stays -18.0 dBFS RMS, ±1.5 dB, peak ≤ -4):

| kind | patches | level reading | why |
|---|---|---|---|
| slow | 17, 21 | RMS over **+6 s .. +10 s** after note-on of the 10 s hold (phrase f: A1; f2: A2) = **the bloomed, steady state**; the whole-hold RMS, the first second and phrase (b) are reported next to it | a swell's whole-hold RMS counts its dark start; the steady state is what the player stands in. Phrase (b) is a poor yardstick for a bloom (short notes are the dark start): 21 reads 13-21 dB under its steady level on (b) |
| spring stab | 09 | RMS over the **note-on region** (11 stabs x 110 ms) of phrase g, **spring included, tail excluded** | the reference is a note-on-region reading everywhere; the tail after note-off is measured separately. The spring raises the reading by about 1.5 dB over the dry stabs alone (both are in the table) |
| echo bass | 11 | RMS over the note-on region of phrase h (17 notes x 100 ms), **echo included where it falls inside a gate, tails excluded**; the echo is also read on its own | same as above |

**The spring and the echo as the effects' own contribution:** the FX stages are parallel sends added onto the dry output, so `wet - dry` (the same script with `DLY_MIX 0, REV_MIX 0, CHEW 0, GROWL 0`) is
exactly what they return. The tables report it re the dry note (dB), per band, its centroid, and a check that the send adds nothing before its own delay. The delay's repeats and the spring's tail are
read as "release to -20 / -40 / -60 dB" against the level of the last note before the key-up.

**Measures new in 2A:** the *bloom* (per second of the hold: level, centroid, % above 1.2 kHz; the centroid is judged on a log axis, 10 % / 90 % of the climb from the first window to the plateau, linear between windows),
the *register tilt* (`x_register`: centroid in harmonics of the note per octave, and level), *dropouts* (deepest dip of the 10 ms envelope below the median, count of dips ≥ 6 dB), the *pluck* (centroid of the first 23 ms against the next 67 ms; level drop inside the gate; time to fall 10 dB), the
*triangle probe* (the harmonics 3 / 5 / 7 of a held A2 re the fundamental against an ideal triangle -19.1 / -28.0 / -34.2 dB and a square -9.5 / -14.0 / -16.9 dB), the *DRAIN probe* (B with the spring at three settings).

**Engine facts found in 2A (existing controls only; nothing was coded):**

* **There is no triangle oscillator** (waves: saw, pulse, saw+pulse; the LFO has the only triangle). The nearest is a 50 % pulse through a key-tracking 12 dB low-pass with the cutoff at about 1.7 x the note: 11's harmonics 3 / 5 / 7 measure -17 / -29 / -38 dB against a triangle's -19 / -28 / -34.
* **The longest envelope time is 10 s** (ATTACK 127); there is no drone latch. A bloom happens while the key is down; an early release fades the note from wherever the filter got to. Brightness reaches 90 % of its climb at about 7 s with a 10 s filter attack (21 B), because the last part of the climb is above the harmonics left to reveal.
* **A fast pluck cannot reach the reference level.** With the amp falling more than ~17 dB inside a 100 ms gate (10 dB in under ~44 ms) -18.0 RMS needs VOLUME above 127 (1B lesson, now with a number). 11 takes the fastest decay the level allows and puts the snap in the filter.
* **DRAIN on a bass is audible, not absent:** the tank is fed through a *one-pole* 150 Hz high-pass (-9 dB at 55 Hz, not a wall), so it still rings the note's body; what it lacks is boom below ~60 Hz. Numbers in 11's and 17's READMEs (DRAIN probe).
* **Spring and echo are in series** (echo into the spring): with both on, the spring rings the repeat too.
* **ALLEY's first repeat is a whole copy of the note** (as long as the note, 100 ms here); FEEDBK 12 puts the second repeat 27 dB under the first (a single slap), 40 puts it 17 dB under. PINGPONG 0 puts the repeat centred (0.71 on each side), 127 puts the first repeat on the left only.
* **MONO/UNISON do not re-fire the envelopes on legato** (11 is MONO: play it detached; 21 is a unison: a legato second note slides and does not restart the bloom).

**Proof for the batch** (`identical.py build/voicing/base 17,21,9,11`, base = `e2a7ad7`, the commit before Batch 2A): the patch bytes of the other 28 programs are equal and their audio is byte-identical on all 11 phrases (a, b, c, d, e, f, f2, g, h, x_stress, x_register).
Each committed slot equals its variant B by `check_slot.py` (resolved bytes identical; audio bit-identical when both are loaded from INIT; from the boot patch the CUTOFF / RESO slew floor of §8 puts 21 and 09 20-38 dB apart, 17 and 11 are bit-identical either way).
**Where each Batch 2A patch's own array came from:** 17 `PF_DUAL_SAW` (only Titanic used it; renamed `PF_TITANIC`), 09 `PF_CLAV_PLUCK` (only Skeenhead; renamed `PF_SKEENHEAD`), 21 and 11 got new arrays (`PF_DRONE_UNI` stays with 18 Roto-scopo, `PF_SUB_BASS` with 05 ZEAROX and 19 Blackwater).

## 11. Batch 2A lessons (short)

Approved: 17 Titanic B, 21 Cowl Shadow C (1 listening + 1 silent round each); 11 Slapback Strut G and 09 Skeenhead E (2 + 2 each). §10 has the kit and the engine facts.

* **Diagnose before changing, with time-windowed measurements.** 09's spring read -4.2 dB re the dry note on average and looked fine; per window it was +0.8 dB at 20-100 ms and +15.7 dB at 100-250 ms: as loud as the note from 20 ms (`diag09.py`). One average hid it.
* **Failure mode: the filter resting below the played notes.** A fast filter decay with a base cutoff under the notes' fundamentals shuts the filter within ~25 ms and leaves a quiet hum with no top ("the bottom of a well"); a second oscillator does not help, it goes through the same filter. Fix: the cutoff floor and the filter sustain.
* **ALLEY TONE is inert on a bass echo.** The echo is a faithful copy of the note (its band split follows the dry note's), and the note has nothing near TONE's range (TONE 70 -> 127 moved the echo's centroid by 1 Hz). Clarity has to be built into the note.
* **Removing a pluck's decay made the note duller, not brighter:** the filter tap carried the top (11: 0.4 % of the energy above 400 Hz with zero decay against 2.3 % with the pluck); the cutoff has to go up and the sub down to compensate.
* **No triangle oscillator:** use a pulse through a key-tracking 12 dB low-pass and measure harmonics 3 / 5 / 7 against -19 / -28 / -34 dB (a triangle) and -9.5 / -14 / -17 (a square).
* **A fast pluck cannot reach the level reference** (VOLUME stops at 127); a held, gated note can (11 went from VOLUME 122 to 102).
* **Slow patches have two levels.** 21 C reads -18.0 dBFS in the bloomed state and -31.3 on phrase (b): a 13.3 dB gap that will surprise a player who taps a note after switching to it.
* **The delay path leaves a constant -76 dBFS DC offset behind a driven voice** (inaudible); tail readings subtract it.
* **INIT-loaded and boot-patch-loaded renders differ** by the CUTOFF / RESO slew floor (20-41 dB on some patches); compare both loaded from INIT (`check_slot.py` does both).

## 12. Batch 3A — the fat and driven set (01 Red Pill, 02 Cement Grind, 06 zzuFuzz, 08 Wire Bite)

The kit is `tests/voicing/batch03a.py` (driver), `batch03a_metrics.py` (the new measures) and `batch03a_variants.py` (the variant tables and texts): the same method as 2A (§10), with four new phrases
(i, j, k, l, §1), a level phrase per patch (reported next to phrase (b)), and, new, a **probe** section: the recommended variant with one knob stepped (DRIVE, GROWL, TONE, BIAS), as numbers.
Two branches, as in 2A: code, logs, cards and the small tables on `voicing/batch-03a-chapter1-fat-and-driven` (merged); every WAV on the never-merged `listen/batch-03a-chapter1-fat-and-driven`.

**Measures new in 3A (definitions):**

| measure | definition |
|---|---|
| crest factor | peak / RMS in dB over the note-on region (square wave 0 dB, sine 3 dB, saw 4.8 dB; a fuzz wall reads 2-3 dB on a held note) |
| attack probe | a note on A5 (1.1 ms period, so a millisecond attack is resolvable) struck from silence; the stereo RMS over one period, trailing, hop 0.25 ms; ms from the key-down (first sample above -60 dB of the plateau) to 10 % and 90 % of the plateau (the mean level 200-400 ms later), and the level re the plateau at 2 / 5 / 10 / 20 / 50 ms. Run on the patch as it is and with GROWL and the sends off ("voice") |
| wet return per window | the sends' own return = the render minus the same render with DLY_MIX and DRAIN at 0 (GROWL / CHEW stay, they are in the voice), RMS in the 0-20 / 20-100 / 100-250 ms after a note-on, in dB re the dry note's RMS in the same window. The dry is read as it falls, so the last window of a 150 ms note compares the return with a note that has already ended: it is the tight one. Three isolated notes (phrase i) |
| PWM | over the steady part of a held note (+400 ms to the key-up) the energy of four bands (150-400, 400-1.2k, 1.2k-3k, 3k+) and of the whole level in 23 ms frames (hop 5.8 ms): depth = 95th - 5th percentile in dB, rate = the strongest component between 0.8 and 20 Hz. Also over the riff (300 ms of each 400 ms note, depth only) |
| zap | the energy above 1.2 kHz in the first 40 ms re the same band in the body (+150..300 ms of a held note; +40..100 ms of a 110 ms bite), dB; and the centroid of the first 23 ms against the next 67 |
| drift | the engine's own log (`vlog`) of each voice card over a held note, exact: static offset, wander s.d. and range in cents; plus the LFO law below |
| self-oscillation probe | the oscillators off, only noise feeds the filter, two renders with the noise 12 dB apart (NOISE 24 and 12); a linear filter answers 12 dB apart, a singing one answers with far less. At the patch's own RESO and at 100 / 115 / 120 / 124 / 127 |
| tail | -20 / -40 / -60 dB after the key-up, the DC the render settles on (read in the quiet stretch before the next note) subtracted; with the sends and with the voice alone |

**Engine facts found in 3A (existing controls only; nothing was coded):**

* **LFO PITCH, LFO PWM and LFO FILTER are square laws, `(d*d) >> 7`, integer:** LFO PITCH below 12 is 0 (**the original Wire Bite's LFO PITCH 10 did nothing**); the pitch LFO's peak is `(d*d>>7) * 9.4` cents (12-15: 9, 16-19: 19, 20-22: 28, 23-25: 38, 32: 75). LFO PWM is ±`(d*d>>7) * 0.195` points of pulse width (100: ±15 points, 127: ±25).
* **A PWM that crosses 50 % doubles its rate:** a pulse of width w and of 100-w sound alike, so a sweep through 50 % cycles twice per LFO period (02 measured 15 Hz at LFO RATE 100 with PW 36 and PWM 127). Keep the base off 50 % by more than the depth so the sweep is one-directional; the depth in the 150-400 band saturates at about 12 dB p-p.
* **LFO PHASE SYNC restarts the LFO with each detached note** (the first key of a chord): every note starts its PWM identically, which reads as intention.
* **The per-voice DRIVE is before the filter** (voices -> DRIVE -> filter): it adds harmonic density and compresses (01: crest 8.9 -> 4.8 dB, DRIVE 0 -> 88) and the low-pass then takes the edge back (centroid 650 -> 622 Hz). GROWL is after the filter and is the one that adds edge (GROWL 0 -> 55 on 06: crest 10.3 -> 6.4 dB, held-note crest 5.8 -> 3.7 dB).
* **06: the sustain is the envelope's, the squash is GROWL's.** At AMP SUSTAIN 127 the held note already loses only 0.2 dB in 3 s at GROWL 0; GROWL 55-100 flattens the waveform (held crest 5.8 -> 3.7 -> 1.5 dB) and the loudness trim keeps the level; BIAS 15 -> 80 only lifts the peak 0.8 dB (crest 5.3 -> 6.1, centroid unchanged) while TONE 25 -> 90 moves the centroid 1251 -> 2051 Hz at the same level (probe tables in 06's README).
* **GROWL's loudness trim reads the output stage, so VOLUME changes how a note from silence starts:** with the patch at its trimmed VOLUME 77 the strike is -0.7 dB at 2 ms re its plateau; the same patch tuned at VOLUME 100 started -4 dB under it and took 25 ms to reach 90 % (seen while tuning, not tabled).
* **The audio estimate of a six-voice stack's pitch wander cannot resolve it:** the stack's own beating moves the centroid of its fundamental band by about 8 cents s.d. (VINTAGE 0, no LFO), more than the 4-5 cents of wander VINTAGE 127 puts on each voice. Use the engine's log (exact) and the LFO law.
* **A unison's attack from silence reads slow (13 ms to 90 % of the plateau on 08) and it suggests the stack, not the envelope:** the same patch with UNI_N 1 or 2 reads 1.2-1.5 ms (AMP ATTACK 2 = 0.5 ms); six detuned voices beat, which suggests the level moves a couple of dB and the 90 % crossing lands where the beat does.
* **The SVF at LP24 does not sing before RESO ~124 on these patches** (06: 12.0 dB linear to RESO 115, 11.8 at 120, 3.3 at 124, 0.3 at 127): RESO up to about 120 is safe on a fuzz.
* **Shared arrays:** 01 Red Pill and 06 zzuFuzz both used `PF_FAT_BASS` (with 27 R3V3RT, which keeps it); each got its own, `PF_RED_PILL` and `PF_ZZUFUZZ`. `PF_WOBBLE_BASS` (only 02) became `PF_CEMENT_GRIND` and `PF_UNISON_LEAD` (only 08) became `PF_WIRE_BITE`.

**Proof for the batch, and a finding about slot 1 (the boot patch).** Batch 3A changes slot 1, which is the program the synth boots into, so the §6 recipe (`identical.py base`) cannot return "everything else identical" any more:
* **Why:** CUTOFF and RESO slew by `x += (target - x) >> 6`, which lands exactly when approaching from above but stops up to 63/256 short from below (the debug trace: 19393 against 19456, 7617 against 7680), so the first program loaded after boot starts from a different place when the boot patch has another CUTOFF / RESO
  (Red Pill 92 / 58, the old one 40 / 30): that alone changes the audio of the first program loaded by -32 dB-class amounts (max sample difference 474 of 19980). And the effects remember the boot patch (the echo's time, the spring's state): after driving CUTOFF / RESO to the same state (`identical.py ... --from-init`: INIT, CUTOFF + RESO 127, INIT, then the program at 2.8 s) **11 of the 28 other programs are byte-identical on all 15 phrases, and the 17 that are not are exactly the 17 with the echo or the spring on** (4, 9-16, 18, 20, 23, 24, 26, 28, 29, 31).
* **The clean proof is boot-matched:** `make_mid.py` builds the base tree plus only the new slot 1; then `identical.py build/voicing/mid 2,6,8` compares the new tree against it: **29 of 29 other programs are byte-identical on all 15 phrases (a, b, c, x_stress, d, e, f, f2, g, h, x_register, i, j, k, l), the patch bytes of 29 slots are equal (hashes), and only 2, 6 and 8 differ.**
  Slot 1's own effect on the others is therefore only the boot state: a player who powers on in Red Pill and then selects a programme with an echo or spring gets that effect's first moments from a slightly different state (a fraction of a semitone on the filter, a different echo-time easing). Inaudible by the numbers (-32 dB-class on the first note), not bit-exact.
* Each committed slot equals its **approved** variant by `check_slot.py SLOT KEY 3a` (01 C, 02 D, 06 C, 08 D: resolved bytes identical; audio bit-identical loaded the same way; from the boot patch the slew floor puts 06 and 08 apart, -45 dB and +0.4 dB, the latter because a unison's random start phases follow the state). The numbers above were measured with B committed; the final run with the approved four is in section 13.

## 13. Batch 3A lessons (short)

Approved 5 Nov 2026, all as rendered, 1 silent measured round + 1 listening round each: 01 Red Pill C, 02 Cement Grind D, 06 zzuFuzz C, 08 Wire Bite D. Cards in `cards/`, renders in `reference-renders/`. §12 has the kit and the engine facts; the short version:

* **LFO PITCH is inert below about 12:** the law is `(d*d) >> 7` in integers, so 1-11 rounds to 0 (12-15: +-9 cents, 16-19: +-19, 20-22: +-28, 23-25: +-38). A "touch of vibrato" at 5 or 10 is no vibrato (the same law applies to LFO PWM and LFO FILTER).
* **A PWM sweep through 50 % doubles its rate:** a pulse of w % and one of 100-w % sound alike, so keep the base width off 50 % by more than the depth (02 D: PW 36 %, +-18 points, runs 18-55 %: it just crosses 50 % at the top of each swing and folds back, and the measured rate still equals the LFO's) or the timbre cycles at twice the LFO rate. The depth in the 150-400 Hz band saturates near 12 dB peak to peak.
* **GROWL's loudness trim reads the output stage, so VOLUME changes how a note from silence starts:** judge and set a fuzz at its final VOLUME. A heavily clipped patch (06: held crest 1.7 dB) matches the level reference on its own phrase and reads about 2 dB hot on phrase (b) (cause not isolated).
* **A change to slot 1 (the boot patch) shifts the first moments of the echo and spring programs:** CUTOFF / RESO smoothing stops short of its target by up to 63/256 when approaching from below, and that state, with the echo's and the spring's, is carried over from the boot patch into the first program loaded. Compare against a boot-matched base (`make_mid.py`), not the plain base, whenever slot 1 changes.
* **The audio cannot show cents of drift in a six-voice stack** (its own beating is ~8 cents s.d.): use the engine's `vlog` and the LFO law. **A unison's attack from silence reads slow** (13 ms) with six detuned voices and 1.2-1.5 ms with one or two: this suggests the stack's beating, not the envelope.
* **Brighter hides the zap:** a zap measured as the top burst over the body shrinks as the body brightens (08: +4.6 dB at CUTOFF 80, -2.0 dB at CUTOFF 90 with the second oscillator at +19 st); D was approved by ear regardless, so the burst is a diagnostic, not a target.
* **Reminder (audit, nothing edited):** slots 13, 15, 16 and 24 have an inert LFO PITCH (3, 8, 3, 4) and must get a real value (12 or more) or 0 when they are voiced.

## 14. Batch 3B — the wreck and chop set (05 ZEAROX, 07 Tape Splice, 15 Trem Chop)

*Chapter labels: 05 and 07 are Chapter I (The Wasteland Arsenal); **15 Trem Chop is Chapter II (The Tidal Hexes)** (`DOG-5-presets.md` §3). The batch and its branch names (`...chapter1-wreck-and-chop`) were labelled Chapter I as a whole; that label was wrong for 15.*

Round 1 (5 Nov 2026), **rendered, not yet heard**: each patch has its recommended variant B committed and A, C, D render-only. The kit is `tests/voicing/batch03b.py` (driver), `batch03b_metrics.py` (the new measures) and `batch03b_variants.py` (variant tables and texts), the same method as 3A (§12): a variant is a full parameter list over INIT, A is rendered through the base program path, VOLUME is trimmed last to
-18.0 dBFS RMS on the patch's level phrase (±1.5 dB, peak ≤ -4). Two branches, as in 2A / 3A: code, logs, cards and the small tables on `voicing/batch-03b-chapter1-wreck-and-chop` (to be merged), every WAV on the never-merged `listen/batch-03b-chapter1-wreck-and-chop` (`listen/voicing/batch-03b/` only). New phrases m, n, o, p (§1).
Each patch has its own array now: 05 `PF_ZEAROX` (it shared `PF_SUB_BASS` with 19 Blackwater, which keeps it), 07 `PF_TAPE_SPLICE` (was `PF_XMOD_GROWL`, only 07's), 15 `PF_TREM_CHOP` (was `PF_SQUARE_LEAD`, only 15's).

**Measures new in 3B (definitions):**

| measure | definition |
|---|---|
| kick windows | one isolated hit, from its REAL onset (the first sample over -60 dBFS: the host quantises note events to its blocks, so the sound starts up to a few ms either side of the phrase's nominal time): the band split (<60 / 60-150 / 150-400 / 400-1.2k / 1.2k+ %) of the mono sum in 0-10 ms (click), 10-50 ms (body) and 50-150 ms (tail); "above 60 Hz" is the sum of the last four. "Click re body" = RMS of the first 5 ms against the 10-50 ms RMS (0 = as loud, positive = a spike) |
| small speaker | the note-on region after a zero-phase 2nd-order Butterworth-magnitude high-pass at 60 / 100 Hz, in dB re the unfiltered region: how much a speaker that cannot reproduce below that still plays (0 = all) |
| hit crest (first 30 ms) | peak / RMS of the first 30 ms of an A1 hit: the overload reading (sine 3 dB, saw 4.8, a flattened wave lower). The crest over the whole 150 ms is bigger because the amp decays |
| dropouts (05) | 48 hits of A1 (24 s): hits more than 3 / 6 dB under the median hit, and the deepest dip |
| noise floor | the RMS of a quiet stretch with its mean removed (a constant DC offset after GROWL), +0.1 / +0.5 / +1.5 / +2.4 s after the last note-off; "silent" = under -150 dBFS |
| pitch wobble (07) | autocorrelation pitch of the held A2 (40 ms frames, 10 ms hop, weak frames dropped; the share kept is reported where it is under 90 %): s.d. and 5-95 % range in cents, strongest component 0.3-15 Hz. Re-rendered with CHEW 0 to separate the tape's part |
| edge timing (07) | the 1 ms peak envelope: onset = note-on to -20 dB of the note's body, end = note-off to -40 dB of it; the tape's own jitter = the per-note difference between the render with and without CHEW (mean, s.d., range) |
| chop (15) | the 2 ms RMS envelope of the held A3: ON = median of the upper half, OFF = median of the lowest tenth, depth = ON - OFF (dB); edges = the midpoint crossings: rate = 1 / mean period, edge timing jitter = s.d. of the rising edges about a straight line (the reading's resolution is the 0.5 ms hop), duty = share of a cycle above the midpoint; level shares = % of time off (> 30 dB under the top) / at one voice's level (4-12 dB under) / full (within 4 dB) |
| edge rise (15) | the patch struck on A6 (1760 Hz, period 0.57 ms) and held; the peak envelope in a window of ONE period (so the figure cannot be below 0.57 ms: an upper bound); the median 10-90 % rise of the chop's rising edges |
| first edge (15) | on phrase p, per note: whether the chop is ON 4 ms after the note-on and the time to its first midpoint crossing: all ON at the same time = the chop is locked to the notes (LFO PHASE SYNC) |

**Engine facts found in 3B (existing controls only; nothing was coded):**

* **There is no Poly-Mod.** The cross-mod is X-MOD: OSC 2 -> OSC 1 linear FM, `(d*d)>>7` law. The modulator is taken from OSC 2's output before its level knob (`o2n = v->o2.prev`), so OSC 2 LEVEL 0 still modulates (read in the code and **measured** in round 2: on 07 B's held A2 with O2 LEVEL 0, X-MOD 100 against 0 differs by 3.1 dB re the signal). **ENV>O2** (the filter envelope on OSC 2's pitch, up to +24 st at the strike) is the pitch-drop chirp of a kick. On 07, X-MOD 0 -> 127 does not move the measured pitch in any ordered way; it spreads energy BELOW the note (the share under 60 Hz of the held A2: 0 / 0 / 2 / 10 / 18 % at X-MOD 0 / 40 / 70 / 100 / 127; this suggests FM sidebands, not isolated).
* **The voice's NOISE is gated by the note** (it goes through the filter and the amp envelope: 05 B's isolated A1 hit is 60 dB down 62 ms after the key-up, the voice alone 18 ms). **The tape hiss is not**: with CHEW on it comes up, stays about 2 s after the last note and fades; **HISS 0 removes it** (digital silence after the last note on 05). With HISS 32 / 64 / 96 the floor right after the last note is -56 / -50 / -44 dBFS (05 B's hits are at -18), 5 dB lower by 2.4 s.
* **CHEW at the top changes little in 05's numbers**: with CHEW 0 / 127 the level moves 0.2 dB, the first-30-ms crest 2.3 -> 2.8 dB, the band split by 1 point and the click's share above 400 Hz 23 -> 19 % (head loss); no hit in 48 dipped 3 dB at DROPS 64 (the HISS rows of the probe cannot place the hit windows: the hiss is above the -60 dBFS onset threshold, marked n/a). What flattens the wave is **GROWL** (crest 5.7 at 0, 3.4 at 76, 2.8 at 104). CHEW costs +768 host instr/sample on top of the voice (GROWL +579): 05 B is 2753 worst case, the original 1361, above the base's 1900 worst case; the device render time is not measured.
* **The sub is OSC 1 LEVEL**: 05's energy under 60 Hz goes 9 -> 49 % for O1_LVL 50 -> 110 (after VOLUME re-trims). An A1 fundamental (55 Hz) sits under the 60 Hz band edge, so a played A1 reads as "sub" in any band split; the body is OSC 2 an octave up (110 Hz) and the harmonics GROWL adds.
* **A kick cannot have both a level spike and the bank reference level over a 150 ms gate** (§8): 05 B's first 5 ms sit about 1 dB under the body, so the click is spectral (19 % above 400 Hz in the first 10 ms against 0 for the original), not a level spike.
* **The tape stage delays everything by a few ms and not by a constant**: 07 B (CHEW 80) shifts a note's onset by +2.4 ms on average with 0.59 ms s.d. (+1.2 .. +3.2 over 12 notes) and the end of a note by +3.0 ms ± 1.6; the head sits 3.6 ms behind and the wow / flutter move it.
* **The LFO has no tempo sync.** Its rate is the RATE knob alone (`0.05 x 600^(RATE/127)` Hz, a step is about 5 %); the tempo (GLOBAL, a MIDI clock, REC tap on the BBD page) feeds the arp, the delay's SYNC and ALLEY, never the LFO. Nearest RATE bytes for a chop of one on+off cycle per note value: 90 BPM quarter / eighth / sixteenth = 1.5 / 3.0 / 6.0 Hz = RATE 68 (1.54) / 81 (2.96) / 95 (5.99); 120 BPM = 2.0 / 4.0 / 8.0 Hz = RATE 73 (1.98) / 87 (4.00) / 101 (8.10); 140 BPM = 2.33 / 4.67 / 9.33 Hz = RATE 76 (2.30) / 90 (4.65) / 104 (9.42). The nearest thing to a lock is **LFO PHASE SYNC** (the first key of a detached note restarts the LFO, `pt.lfo_ph = 0`; a legato MONO note does not): the chop is locked to each note, not to the beat.
* **A free-running chop at a tempo-matched rate can start every note OFF.** 15 C (PHASE FREE, 8.10 Hz) against eighths at 120 BPM (2.025 cycles a step): all eight notes of phrase p begin in an off part and the first edge slides 46 -> 24 ms (3 ms a step). Where it starts depends on where the LFO happens to be, so a live player can get either. The reason 15 B is SYNC.
* **VINTAGE does not move the LFO.** It scales the pitch and cutoff offsets and the envelope times, not the LFO rate or phase: the chop's edge timing s.d. at VINTAGE 0 / 60 / 127 is 0.18 / 0.24 / 0.16 ms (the reading's resolution is 0.5 ms), and the SLOBBER ride adds to the same VINTAGE. The only existing sources of wavering edges are the tape (CHEW 100: 0.57 ms s.d.) and the voice cards' phase offsets (LFO PHASE SPREAD: 45° per voice, an eighth of a cycle between a DUAL pair, 15 ms at 8.1 Hz).
* **The amp LFO is not a gate to silence.** The law is `1 - AMP/256 x (1 - lfo)`: AMP 127 on a SQUARE swings between full level and 1/128 (-42 dB); the measured depth is 42.8 dB, AMP 100 is 13.5, AMP 80 8.8. The edge is a ramp across one 16-sample control block (0.36 ms); measured rise on an A6 probe is 0.77 ms (limited by the window).
* **LFO SQUARE amp, hard edges: the largest sample step is -11 dBFS** on 15 B (it is a gate; the step is the edge).
* **MONO / UNISON do not re-fire the envelopes on legato** (all three patches are MONO: play them detached).

**Round 1 results (the recommended variants; the full tables are `listen/voicing/batch-03b/<NN-name>/README.md`):**

| slot | recommended | VOLUME | level (level phrase) | (b) | peak | worst-case CPU (original) | headline |
|---|---|---|---|---|---|---|---|
| 05 ZEAROX | B blown | 122 | -18.0 (kick phrase) | -19.2 | -10.3 | 2753 (1361) | a small speaker keeps -2.6 dB of the kick phrase after a 100 Hz high-pass (the original -10.9); the A1 hit has 78 / 86 / 62 % of its click / body / tail energy above 60 Hz (the original 38 / 21 / 10); first-30-ms crest 2.8 dB |
| 07 Tape Splice | B centre | 104 | -18.1 (splice phrase) | -17.6 | -12.5 | 2177 (1384) | pitch wobble 9.6 cents s.d. (28 cents 5-95 %), the tape adds +0.8 and delays each note +2.4 ms ± 0.59 |
| 15 Trem Chop | B centre | 108 | -18.0 (chop phrase) | -16.6 | -10.5 | 1366 (1402) | 8.10 Hz square chop, depth 42.8 dB, edge rise 0.77 ms (upper bound), edge timing s.d. 0.16 ms; every detached note starts ON |

**Proof for the batch** (`identical.py build/voicing/base 5,7,15`, base = `92cf51f`, the commit before Batch 3B; slot 1, the boot patch, is not touched, so the plain comparison holds): the patch bytes of 29 of 32 slots are equal (only 5, 7 and 15 differ) and the audio of the **other 29 programs is byte-identical on all 19 phrases** (a, b, c, x_stress, d, e, f, f2, g, h, x_register, i, j, k, l and the four new ones m, n, o, p). Each committed slot equals its variant B by `check_slot.py SLOT B 3b` (resolved bytes identical; audio bit-identical when both are loaded from INIT; from the boot patch the slew floor of §8 puts 05 and 07 apart by -13 .. -24 dB, 15 is bit-identical either way).
**Where the arrays came from:** 05 got a new `PF_ZEAROX` (`PF_SUB_BASS` stays with 19 Blackwater and, in a comment, is no longer called 05's), 07's `PF_XMOD_GROWL` became `PF_TAPE_SPLICE` and 15's `PF_SQUARE_LEAD` became `PF_TREM_CHOP` (each was used by its slot alone).

**Decisions after listening (5 Nov 2026):** 07 Tape Splice **B** approved as rendered; 15 Trem Chop **D** approved as rendered (the committed slot was B and was replaced by D; D is DUAL with POLY 6 and PHASE SPREAD, 8.10 Hz, reads 2.5 dB hot on phrase (b), peak -6.2 dBFS, worst case 2375 host instr/sample); 05 ZEAROX: round-1 variants rejected (too messy and muddy), see section 15. Cards `cards/07-tape-splice.md` and `cards/15-trem-chop.md`; renders in `reference-renders/`. The table above lists round 1's recommendations (15 B); the committed 15 is D.

## 15. 05 ZEAROX, round 2 (5 Nov 2026) — the pixelated black-and-white kick

Round 1's variants were rejected after listening ("way too messy and muddy ... I want it glitchy blown out, not muddy blown out"); the new direction took 07 Tape Splice C as the starting point. Kit: `diag05.py` (diagnosis: why round 1 was muddy, what makes 07 C glitchy), `batch03b_r2.py` (variants A-D, element costs, probes); tables in `listen/voicing/batch-03b/round2/`, WAVs only on the listen branch. The 05 log has the full diagnosis and the variant table; the short version:

* **Round 1 was a rounded 150-400 Hz body with no top end**: B's first 20 ms were 68 % in 150-400 Hz and its first 100 ms 0.7 % above 1.2 kHz; the saw through the 24 dB low-pass is the mud (with GROWL and CHEW both off it still had MUD 162), GROWL 104 added about 34 ms of tail and all of the little top end there was, CHEW 127 took top off and lowered the share of samples near the rail (36 -> 29 %).
* **07 C's glitch is the random pitch LFO (pitch spread 14.9 -> 2.9 cents without it) and the tape's dropouts (4 dips of 6-19 dB, none without the tape); X-MOD does not carry either; the pulse waves carry the black-and-white** (24 % of samples near the rail with saw + saw, 54 % with pulse waves, tape off).
* **A single pulse through an open filter (CUTOFF 105, 12 dB) is already almost two-level (96 % of samples within 10 % of the rail on the A1 hit)**; a hard DRIVE only matters when two oscillators are summed. The filter-envelope click was measured and rejected (a closing filter cut the top end from 3.4 to 1.3 % and the two-level share from 96 to 85-89 %).
* **Cost:** the final (D) is 1337 host instr/sample worst case (round 1: 2753); the engine alone is 1164 of that, each oscillator, DRIVE and X-MOD costs 7-20, an S&H pitch LFO nothing measurable; GROWL +595 and CHEW +784 are the expensive elements and are off.
* **Limits found:** (1) the level reference over a 150 ms gate sets how tight a kick can be (AD 72 is already -19.5 dBFS at VOLUME 123; the 127 ceiling is the stop); (2) at A0 (27.5 Hz) the energy after the first 20 ms is mostly under 60 Hz, inaudible on a small speaker; (3) a patch with a free-running S&H LFO is not bit-comparable between the boot patch and INIT (its random sequence follows the engine's random state), so `check_slot.py`-style comparisons only hold from INIT.

## 16. Batch 4A — Chapter II, the organ / PWM / wash set (10 Atlantic Swell, 12 Kelp Tangle, 16 Tidal Pull)

*(Numbered 16 because section 15 is 05 ZEAROX round 2, which 05's log and card refer to.)* Round 1 (6 Nov 2026), **rendered, not yet heard**: each patch has its recommended variant B committed and A, C, D render-only. The kit is `tests/voicing/batch04a.py` (driver), `batch04a_metrics.py` (the measures),
`batch04a_variants.py` (the variant tables), `batch04a_report.py` (README tables), `batch04a_probes.py` (`probes.md`: the recommended variant with one control stepped) and `batch04a_docs.py` (the logs and the index README), the same method as 3B (§14): a variant is a full parameter list, A is rendered through the base program path, VOLUME is trimmed last to -18.0 dBFS RMS on the patch's own phrase
(±1.5 dB, peak ≤ -4, effects included, tails excluded). A peak-limited variant may sit down to -19.3 (16 D: -19.1). Two branches: code, docs, logs and the small tables on `voicing/batch-04a-chapter2-organ-kelp-wash` (to be merged), every WAV on the never-merged `listen/batch-04a-chapter2-organ-kelp-wash` (`listen/voicing/batch-04a/` only). New phrases q, r, s (§1).
Each patch has its own array now: 10 `PF_ATLANTIC_SWELL` (it shared `PF_HOLLOW_PAD` with 12; the name went with the array), 12 `PF_KELP_TANGLE` (new), 16 `PF_TIDAL_PULL` (new; `PF_PWM_STRINGS` stays with 13 Ghost Board).

**Measures new in 4A (definitions):**

| measure | definition |
|---|---|
| attack, as heard | the amp envelope itself: one voice (OSC 2 off, VINTAGE 0, LFO / GROWL / sends off) struck from silence, held 1.8 s; the stereo RMS envelope in trailing windows of one period of the note (hop 0.25 ms); ms from the key-down (the first sample above -60 dB of the plateau = the mean power 1.0-1.4 s later) to 10 / 50 / 90 % of the plateau (voltage). A detuned pair beats by several dB and moves the plateau: it read 87 ms where the envelope alone reads 160 (AA 78): suggests the beating, not isolated |
| sends separated | four renders per phrase: full, dry (DLY MIX and DRAIN 0), delay-only (DRAIN 0), spring-only (DLY MIX 0): the delay's own return = delay-only minus dry, the spring's = spring-only minus dry. **The spring sits after the echo and rings the repeats**, so full minus dry minus both is the interaction (reported where it matters) |
| return windows | after a held chord's note-off: the delay's and the spring's own return in 0-100 / 100-250 / 250-500 / 500-1000 / 1000-2000 ms (12: 0-250 / 250-750 / 750-1500 / 1500-1800), RMS in dB re the chord's own level over the 400 ms before the note-off, the DC out. After a note-on: `wet_windows` 0-20 / 20-100 / 100-250 ms re the dry note in the same window |
| first repeat | an ISOLATED note struck alone (nothing before it: in the phrase the chord's echoes are still ringing): the delay-only return's 4 ms envelope inside [delay - 30 ms, delay + note + 150 ms]: the peak re the dry note's peak (dB) and its time after the note-on; the spring-only return's peak in the same window and the delay's margin over it. The repeats train = the peak in each successive slot of one delay time re the first |
| echo under the notes | per staccato note: the delay's (or spring's) own return over the note's span re the dry note's RMS there (dB): how much of earlier notes' echo sits under it |
| MUD in windows | share(150-400 Hz) / share(1.2k+), per time window (the note-on region, or the tail after a note-off in 0-250 / 250-750 / 750-1500 ms with each window's level next to it: a MUD in a window 50 dB down is not heard) |
| width | L/R correlation of the 150-4000 Hz band (1 = mono) and side-to-mid energy (dB) of a held chord, dry and with the sends. One render per setting (oscillator start phases are random): differences of about 0.1 are not a trend |
| chorus beating | `beat_metrics` on the A3 band of the held chord (mono sum): the beat rate and the envelope's peak-to-peak depth; a mono reading of what are left and right voices |
| tremolo | the level modulation of the held chord (20 ms RMS, 95th - 5th percentile, dB) and its strongest rate 0.2-12 Hz |
| PWM after the filter | `pwm_metrics` (3A) on the dry render: the band energies (150-400 / 400-1.2k / 1.2k-3k / 3k+) in 23 ms frames, depth in dB and strongest rate, over the steady part of a held note; plus the level's own modulation. The same on the short notes (300 ms ... of each 400 ms) |
| pitch probe | the audio check of the pitch LFO: one voice (POLY, VINTAGE 0, the sends off) with only the oscillator the LFO moves: the common-mode wander of the fundamental in cents (`drift_track`): s.d., 5-95 % range, strongest rate |

**Engine facts found in 4A (existing controls only; nothing was coded):**

* **The amp envelope's nominal time is not the attack time.** The time table's `0.5 ms x 20000^(AA/127)` is 1.3-1.4x the time to 90 %: AA 60 / 66 / 72 / 78 / 82 / 90 = 54 / 86 / 137 / 219 / 299 / 558 ms nominal and 42 / 65 / 101 / 160 / 219 / 406 ms to 90 % (50 % at about a third of the nominal). For a 80-250 ms attack as heard, AA 70-83.
* **One shared LFO cannot give a rotary speaker's quadrature**: vibrato and tremolo on the same LFO are in phase; LFO PHASE SPREAD (45 degrees a voice card) cancels a tremolo in the sum (AMP 45 on a six-voice DUAL chord: 2.2 dB with SPREAD, 2.9 FREE, 3.9 SYNC; one voice's dip 3.8 dB). A Leslie-style patch is PHASE FREE or SYNC.
* **A chorus from existing controls is a DUAL pair whose pitches wander out of step**: the beat of the pair, moved by a slow TRI pitch LFO in PHASE SPREAD (with DETUNE 0: SPREAD 37 dB envelope swing in the A3 band, PHASE FREE 5.8). The BBD's time has no LFO: a short BBD is a comb filter and a Haas widener, not a chorus. A DUAL patch doubles the voices: 10 B costs 2294 host instr/sample against 1804 as POLY.
* **DLY TONE does not move the first repeat** (60 / 90 / 127: the same 1454 Hz centroid); it shapes the feedback path, so only the later repeats (third: 949 / 1082 / 1136 Hz). The first repeat is the BBD's own band-limit (a 2595 Hz note became 1454 Hz at 361 ms).
* **The PWM's band-energy depth saturates**: 150-400 Hz of a held A2 reads 10.0-10.3 dB at LFO PWM 60-115 and at CUTOFF 78-104 (12 B); per-voice DRIVE 20-40 lifts it to 12.5-12.7 and takes the level swing from 5.9 to 3.4-3.7 dB. The cutoff trades the upper bands' depth (400-1.2k: 11.8 -> 7.4 dB from CUTOFF 78 to 104) against the tail's MUD (12 B at CUTOFF 78 / 86 / 98: 159 / 29 / 10 in the first 250 ms of the tail).
* **A murky voice has a tubby spring tail**: the spring is fed the filtered voice (a one-pole high-pass at 150 Hz, no more top than it is given), so 12 B's tail MUD is 29 / 39 / 180 over 0-1500 ms; SIZE and DRAIN shorten and soften it (SIZE 62: -60 dB at 1244 ms) but do not brighten it.
* **The old HOLLOW PAD's "movement" was not PWM**: its inverse narrow-pulse pair (PW 16 % and 85 %) beats, and that is the 14.2 dB in 150-400 Hz (LFO PWM 0 leaves it at 14.2; detune 0 too: 1.0 dB).
* **A PWM sweep is one LFO period long**: at 1 Hz a 150 ms note hears about 2 dB of it (12 B's short notes); PHASE SYNC starts each detached note at the same width.
* **No sine oscillator, no sine LFO**: the nearest is a narrow pulse through a key-tracking 12 dB low-pass at about 2 x the note (16 D: harmonics 3 / 5 / 7 at -17.2 / -27.3 / -36.8 dB against a triangle's -19.1 / -28.0 / -34.2): triangle-like, dark (0.5 % above 1.2 kHz).
* **POLY is narrow, DUAL is wide**: 16 B's chord correlates 0.70 dry (0.55 with the sends); the same patch as DUAL POLY 8 reads 0.38.
* **LFO PITCH is inert below 12**: 16's original had 3; it is 16 (+-19 cents) now. Audit: slots 13 (3) and 24 (4) still have an inert LFO PITCH; 15's was set to 0 when it was voiced.

**Round 1 results (the recommended variants; the full tables are `listen/voicing/batch-04a/<NN-name>/README.md` and `probes.md`):**

| slot | recommended | VOLUME | level | (b) (re level) | peak | worst-case CPU (original) | headline |
|---|---|---|---|---|---|---|---|
| 10 Atlantic Swell | B | 64 | -18.2 (own phrase) | -19.0 (-0.8) | -4.4 | 2294 (2020) | DUAL pair with a TRI pitch LFO in PHASE SPREAD (0.72 Hz, +-19 cents) as the chorus, organ keying, 361 ms ping-pong BBD at FEEDBK 95: first repeat -9.1 dB re the note, 16 dB above the spring |
| 12 Kelp Tangle | B | 75 | -18.0 (own phrase) | -17.0 (+1.0) | -5.3 | 2042 (2020) | two pulses swept 18-48 % at 1.03 Hz (one side of 50 %) through a 24 dB low-pass at 100 % key tracking: held-A2 PWM depth 10.1 / 9.8 / 11.1 dB in 150-400 / 400-1.2k / 1.2k-3k, centroid 339 Hz; spring tail 1432 ms to -60 dB, tail MUD 29 / 39 / 180 |
| 16 Tidal Pull | B | 63 | -18.1 (own phrase) | -21.6 (-3.5) | -4.4 | 2026 (2069) | five POLY voices of two detuned pulses, TRI 1.26 Hz on pitch +-19 cents and PWM, attack 9 / 44 / 101 ms (10 / 50 / 90 %), 337 ms echo ahead of the spring: first repeat -9.4 dB re the note, 6.6 dB above the spring |

**Proof for the batch** (`identical.py build/voicing/base 10,12,16`, base = `c6edc48` plus the Step 0 doc commit, the firmware unchanged; slot 1, the boot patch, is not touched, so the plain comparison holds): the patch bytes of 29 of 32 slots are equal (only 10, 12 and 16 differ) and the audio of the **other 29 programs is byte-identical on all 22 phrases** (a, b, c, x_stress, d, e, f, f2, g, h, x_register, i, j, k, l, m, n, o, p and the three new ones q, r, s).
Each committed slot equals its variant B by `check_slot.py SLOT B 4a` (resolved bytes identical; audio bit-identical when both are loaded from INIT; from the boot patch the slew floor and the echo / spring state of §8 put 10 and 16 apart (-2.4 .. -21.7 dB), 12 is bit-identical either way; not isolated further).

**Approved after listening (6 Nov 2026), 1 silent measured round + 1 listening round each:** **10 Atlantic Swell A** (the original starting point, unchanged: no vibrato, no chorus, no delay; the array is its own `PF_ATLANTIC_SWELL`, the values of the old `PF_HOLLOW_PAD`, which is deleted; VOLUME 100, -19.0 dBFS RMS on phrase q, peak -4.8, 2020 host instr/sample), **12 Kelp Tangle C** (CUTOFF 98; VOLUME 74, -18.0 on phrase r, peak -5.3, 2042) and **16 Tidal Pull D** (the triangle-like stack, TRI 2.3 Hz, DLY MIX 110; VOLUME 76, -19.1 on phrase s, peak-limited at -4.4, 2027). Cards `cards/10-atlantic-swell.md`, `cards/12-kelp-tangle.md`, `cards/16-tidal-pull.md`; renders in `reference-renders/` (level phrase + stabs each). The batch's rejected variants (B, C, D of 10; B, D of 12; B, C of 16) stay on the listen branch only.
Proof after the approval commit (`identical.py build/voicing/base 12,16`; base = the commit before Batch 4A, which is also the pre-4A firmware): slot 10 equals the base (patch hash and audio), the audio of the **other 30 programs** (everything except 12 and 16) is **byte-identical on all 22 phrases**, so the other 29 besides 10 as well. `check_slot.py` 10 A / 12 C / 16 D (4a): resolved bytes identical; audio bit-identical loaded from INIT; from the boot patch 12 is bit-identical, 10 differs by -25.3 dB (phrase q) and -23.4 dB (b), 16 by -24.0 dB (phrase s) and -28.0 dB (b); not isolated. An erratum to the round-1 text: OSC 2's FINE 73 on 12 and 16 is +7.0 cents, not 5.9 (the formula is (FINE - 64) x 2 x 100 / 256).

*(Section numbering: Batch 4A is section 16 (section 15 is 05 ZEAROX round 2); Batch 4B is section 17.)*


## 17. Batch 4B — Chapter II, the tape / crash pair (13 Ghost Board, 14 Reef Break)

Round 1 (6 Nov 2026), **rendered, not yet heard**: each patch has its recommended variant B committed and A, C, D render-only. The kit is `tests/voicing/batch04b.py` (driver), `batch04b_metrics.py`, `batch04b_variants.py`, `batch04b_report.py`, `batch04b_probes.py` (`probes.md`) and `batch04b_docs.py`, built on the 4A kit (§16, whose metrics it imports): a variant is a full parameter list, A is rendered through the base program path, VOLUME is trimmed last. Two branches: code, docs, logs and the small tables on `voicing/batch-04b-chapter2-ghost-and-reef` (to be merged), every WAV on the never-merged `listen/batch-04b-chapter2-ghost-and-reef` (`listen/voicing/batch-04b/` only). New phrases t, u (§1; also a 24th phrase for `identical.py`). Each patch has its own array: 13 `PF_GHOST_BOARD` (was `PF_PWM_STRINGS`, 13's alone since 16 got its own array in 4A), 14 `PF_REEF_BREAK` (was `PF_PERC_HIT`, 14's alone).

**Level and peak, as 4B does them.** 13 as 4A (-18.0 dBFS RMS +-1.5 on its own phrase, effects and tape included, tails excluded; peak <= -4 on both its phrases). **14: the note-on region is the 300 ms gates of the 11 hits (the burst and about the first 250 ms of its decay, echo included; the release and the rest of the decay excluded), and the peak that limits VOLUME is the OWN phrase's, the worse of two noise seeds** (seed 2 = a quiet dummy note struck first, so the hits land on other voices' noise generators; a noise patch's peak follows the seed). Phrase (b) stacks three noise voices on 14: its peak is reported (about -1 dBFS, no clipped sample) and does not limit. A variant that cannot reach -19.5 dBFS with its own peak at -4 on both seeds is left under the band and says so (14 B, D).

**Measures new in 4B (definitions):**

| measure | definition |
|---|---|
| tape wobble | the deck's pitch wander on a one-voice probe (POLY, VINTAGE 0, the LFO, the echo and the spring off, OSC 2 off): the common-mode wander of a held A3's fundamental in cents (`drift_track`, centroid of f0 +-12 % in 100 ms frames): s.d., 5-95 % range, strongest rate 0.1-8 Hz; dips of the held note >= 6 dB. The 100 ms frames resolve the wow (0.3-0.5 Hz) and not the faster flutter: flutter is not measured |
| smear | the same phrase with and without the deck (CHEW 0): the note-on region's centroid, % above 1.2 kHz and MUD |
| hit attack | the stereo RMS envelope in trailing 1 ms windows over the first 300 ms after the note-on: 10 / 50 / 90 % of its PEAK (voltage) and the peak's time, from the first sample above -50 dB of the peak; the voice alone (sends off). A noise burst's 90 % mark is its own random peaks |
| band decay | the isolated hit's band energy (60-150 / 150-400 / 400-1.2k / 1.2k-4k / 4k+ Hz) in 11.6 ms Hann frames (hop 2.9 ms): each band's time from its own peak to -20 / -40 dB; and per window (0-50 / 50-150 / 150-400 / 400-800 / 800-1500 ms) in dB re the loudest band-window |
| noise-to-sub | the same patch rendered twice, the sub alone (NOISE 0) and the noise alone (oscillators off), sends off: stereo RMS over the first 100 ms, noise minus sub (dB) |
| sub | the sub-only hit's band split over its first 150 ms (<60 / 60-150 / ...) and the 40-150 Hz band's decay to -20 / -40 dB |
| echo of a hit | an isolated hit alone with the echo: the delay-only return's 4 ms envelope peak in each slot of one delay time, in dB re the DRY hit's peak (repeat 1, 2, ...); repeats above -40 dB; peak of the whole render and clipped samples; the band split (MUD, centroid, % 60-150) of the return in the first slots (is the sub building a tubby body?) |
| rail share | the share of samples within 10 % of the rail (5 ms windows): 05's pixelation measure; noise reads a few percent, a clipped square ~100 % |

**Engine facts found in 4B (existing controls only; nothing was coded):**

* **ENV AMT is +-97 semitones:** the filter envelope moves the cutoff `(ENV AMT - 64) x 1.52` semitones at its peak, so ENV AMT 0 pushes a cutoff 97 semitones DOWN at the strike. On a high-pass this is the way to have the sub and the lows at the strike and the top of a noise burst last (14 B: HP12, CUTOFF 100 = 4186 Hz, ENV AMT 0, FD 100: the sub's band is 20 dB down at 163 ms, the 4k+ band at 482 ms, 40 dB at 932 ms). A closing low-pass does the opposite (top 20 dB down at 223 ms, sub at 499 ms); a wide-open low-pass or a notch leave every band as long as the amp envelope; a high-pass with no envelope removes the sub (noise 27 dB over it).
* **FD sets the sub's length in that scheme** (FD 85 / 92 / 100 / 108: the sub 20 dB down at 58 / 93 / 163 / 255 ms) and AD = AR the ring-out (AD 84 / 88 / 92 / 97: the top band 40 dB down at 511 / 700 / 932 / 1370 ms).
* **The amp envelope's attack on a hit:** AA 0 / 30 / 44 / 52 / 60 = 50 % of the peak at 0.2 / 2.5 / 8.0 / 8.7 / 18.0 ms and the peak at 9 / 9 / 27 / 27 / 64 ms (A1, voice alone; 1 ms windows).
* **FEEDBK has a ceiling, not a runaway to clipping:** on an isolated hit FEEDBK 96 / 105 / 112 / 114 / 118 / 122 / 127 gives 7 / 9 / 12 / 15 / 24 / 24 / 24 slots above -40 dB (of 24, 8.7 s) with the peak unchanged at -5.7 dBFS and no clipped sample; from FEEDBK 118 the repeats stop falling (repeat 24: -28 / -10 / -1 dB re the burst at 118 / 122 / 127).
* **Noise and level:** NOISE is a square-law level (NOISE 100 against 127 is 4 dB); the noise's crest factor is 15-16 dB over the gate on a near-instant hit and 13.5 on a quick swell, so the peak limits the level (VOLUME 118-124 of 127 gives -19.9 to -20.1 dBFS at the -4 dBFS peak).
* **CHEW costs +784 host instr/sample whenever it is on** (13 B: 2679 worst case, 1895 with CHEW 0): the heaviest voiced patch so far (15 D 2375). CHEW 40 / 70 / 100 / 127 measures 2.3 / 4.1 / 6.2 / 6.5 cents s.d. of wobble (5-95 % range up to 23 cents) at 0.3-0.5 Hz; WOW/FLT 127 (flutter only) reads 2.0-2.4 (the probe cannot see flutter).
* **The deck is last in the chain** (VOICES, DRIVE, BBD, SPRING, TAPE): the wobble is applied to the finished wet mix when it passes the deck, so a repeat is pitched by the deck's state at its arrival, not by the state when the note was played, and all layers wobble together; a real tape echo warps each repeat on its own. (A consequence of the chain; not measured on the repeats.)
* **A soft tone is not medium muddy:** a narrow pulse through a key-tracking low-pass leaves under 1 % of the energy above 1.2 kHz (13: MUD 245 with OSC 2 off); raising the cutoff to get MUD 4.5 loses the triangle shape (harmonics 3 / 5 / 7 -11 / -17 / -23 dB against -19 / -28 / -34). A two-octave-up copy (OSC 2 +24 st) puts the top back: MUD 245 / 163 / 59 / 18.6 / 11 at OSC 2 LEVEL 0 / 50 / 80 / 112 / 127.
* **The tape lengthens the tail a little (13 B: 40 dB down at 1778 ms against 1662 without) and takes a little off the top share:** 13 B with CHEW 0 has 4.6 % of the note-on energy above 1.2 kHz and MUD 14.1; with CHEW 100, 3.7 % and 18.6 (the centroid rises 825 -> 1064 Hz, the hiss).

**Round 1 results (the recommended variants; the full tables are `listen/voicing/batch-04b/<NN-name>/README.md` and `probes.md`):**

| slot | recommended | VOLUME | level (own phrase) | (b) | peak (own) | worst-case CPU (original) | headline |
|---|---|---|---|---|---|---|---|
| 13 Ghost Board | B | 81 | -18.0 | -19.7 | -5.2 | 2679 (2069) | triangle-leaning tone (harmonics 3 / 5 / 7 -14 / -23 / -32 dB), tape CHEW 100 = 6.2 cents s.d. of wobble, MUD 18.6 note-on and 74 / 89 / 17 in the tail windows, echo 275 ms first repeat -12.2 dB re the note |
| 14 Reef Break | B | 118 | -19.9 | -14.3 | -4.3 | 1832 (1762) | HP12 climbing from -97 st: noise +4.6 dB over the sub, sub 20 / 40 dB down at 163 / 279 ms, 4k+ at 482 / 932 ms, echo 7 repeats above -40 dB, peak -4.3 / -4.6 (two seeds) |

*(These are round 1's recommendations (B). Superseded after listening: 13 by round 2 (§17.1, approved C2, §17.2); 14's approved pick is variant C.)*

**Proof for the batch** (`identical.py build/voicing/base 13,14`, base = the commit before Batch 4B's patches, the firmware unchanged from main; slot 1, the boot patch, is not touched, so the plain comparison holds): the patch bytes of 30 of 32 slots are equal (only 13 and 14 differ) and the audio of the **other 30 programs is byte-identical on all 24 phrases** (a, b, c, x_stress, d, e, f, f2, g, h, x_register, i, j, k, l, m, n, o, p, q, r, s and the two new ones t, u).
Each committed slot equals its variant B by `check_slot.py SLOT B 4b` (resolved bytes identical; audio bit-identical when both are loaded from INIT; from the boot patch 14 is bit-identical, 13 differs by -20.5 dB (stabs) and -16.4 dB (ghost phrase) relative to the signal: the echo / spring / deck state, not isolated).


### 17.1 Round 2 for 13 Ghost Board (6 Nov 2026)

Vincent's ears on round 1: the ORIGINAL is the most Mellotron-like (round 1's tone-nearest-a-triangle, tape and less-echo levers were the wrong direction); the tape wobble "is killing the overall tone" (CHEW 0 everywhere); round 1's **D echo and spring are what he is chasing**. Round 2 (`tests/voicing/batch04b_r2.py`, `listen/voicing/batch-04b/13-round2/`; the round-1 files untouched) keeps the ORIGINAL voice exactly, sets LFO PITCH 0 (bit-identical to the inert 3, proved on both phrases) and CHEW 0, copies D's echo and spring (ALLEY 104, FEEDBK 95, MIX 105, TONE 70, PINGPONG 127, DRAIN 70, SIZE 100, DAMP 25, PRE-DLY 20), re-trims VOLUME, and changes ONE thing per variant: **A2 as is (committed, replacing round-1 B), B2 CUTOFF 75 -> 84, C2 LFO PWM 0, D2 OSC 2 FINE 64**; render-only references: the original and round-1 D, level-matched.
Isolation, one held voice: the beating pair is the 150-400 Hz movement (13.8 dB at 0.9 Hz; 0.3 dB with FINE 64; unchanged without the PWM), the PWM is the 400-1.2k movement (3.9 dB; 1.2 without the PWM), the filter is the MUD (note-on 278 -> 82 at CUTOFF 84, tail 1370 / 2302 / 3233 -> 328 / 611 / 1009) and does not move the movement. No round-2 variant meets the 10-40 / about-80 benchmark (A2 is far over it: it is the original's tone). CPU 2084 (round-1 D 2680: CHEW was +784). The first repeat (-8.6 dB at 337 ms) and the echo's margin over the spring (+10.1 dB) match round-1 D's (-8.8, +9.4). Checks: `identical.py` against the round-1 commit: the other 31 programs, 14 included, byte-identical on all 24 phrases and the patch bytes of 31 of 32 slots equal.

### 17.2 Approved after listening (6 Nov 2026)

**13 Ghost Board: round 2 variant C2 ("no PWM")**, after two listening rounds: Vincent: "This is the closest we have to what I imagined. I'll dial this more later." (round 1: "Tape wobble is definitely killing the overall tone, needs to be dropped entirely"; the echo and spring of round-1 variant D: "SO GOOD".) The patch is the original's dark, beating voice with NO pulse-width movement (LFO PWM 0), NO tape deck (CHEW 0), a long echo (337 ms, FEEDBK 95, MIX 105) and a heavy spring (DRAIN 70); VOLUME 55, -18.0 dBFS RMS on phrase t, peak -4.9, 2084 host instr/sample; it is very muddy by the ratio (note-on MUD 315, tail 1108 / 2198 / 3331). **The brief changed after listening:** the original brief (near-sine filtered triangle, maximum tape wow/flutter) no longer applies (`DOG-5-presets.md` updated; the log has the note). **14 Reef Break: round-1 variant C ("swell")**, after one listening round: "C is the one." VOLUME 121, -18.0 dBFS RMS on phrase u (peak -4.5 / -4.3 on two seeds), phrase (b) -12.8 with a three-key peak of -1.55 dBFS (no clipped sample), 1857 host instr/sample. Cards `cards/13-ghost-board.md`, `cards/14-reef-break.md`; renders in `reference-renders/` (level phrase + stabs each); round-1 variants B and D of 14, A / B / D of 13 and round 2's A2 / B2 / D2 stay on the listen branch.
**The round-2 isolation result (13):** the beating pair carries the 150-400 Hz movement (13.8 dB at 0.9 Hz on one held voice; 0.3 dB with OSC 2 FINE 64; unchanged without the PWM), the pulse-width LFO carries the 400-1.2k movement (3.9 dB; 1.2 dB with LFO PWM 0), and the dark filter carries the mud and not the movement (CUTOFF 84: note-on MUD 278 -> 82, the movement unchanged).
Proof after the approval commit (`identical.py build/voicing/base 13,14`, base = the commit before Batch 4B's patches, which is also the pre-4B firmware): the patch bytes of 30 of 32 slots are equal and the audio of the **other 30 programs is byte-identical on all 24 phrases**. `check_slot.py 13 C2 4b-r2` and `14 C 4b`: resolved bytes identical; audio bit-identical from INIT **and from the boot patch** for both (A2 differed from the boot patch by -33.2 / -40.7 dB; C2 does not: it has no LFO destination, which suggests the free-running LFO's phase at program load was the cause, not isolated).

## 18. Batch 5A: Chapter III, the drones (18 Roto-scopo, 19 Blackwater, 22 Melting Orb)

Round 1 (6 Nov 2026), **rendered, not yet heard**: each patch has its variant B committed (own array) and A, C, D render-only. The kit is `tests/voicing/batch05a.py` (driver and measures), `batch05a_variants.py` (the variant tables), `batch05a_report.py` (README tables) and `batch05a_docs.py` (the logs), built on the 4A/4B kit. Two branches: code, docs, logs and the small tables on `voicing/batch-05a-chapter3-drones` (to be merged), every WAV on the never-merged `listen/batch-05a-chapter3-drones` (`listen/voicing/batch-05a/` only). New phrases v lo, v mid, w lo, w mid, y (section 1; five more phrases for `identical.py`). Own arrays: 18 `PF_ROTO_SCOPO` (was `PF_DRONE_UNI`), 19 `PF_BLACKWATER` (was `PF_SUB_BASS`), 22 `PF_MELTING_ORB` (was `PF_BP_QUACK`); each array had only its slot as user (30, 21, 05 and 11 had been moved off the shared ones in earlier batches).

**Level, as a drone does it.** The reference stays -18.0 dBFS RMS +-1.5, peak <= -4, read on the **held, settled state** of a 15 s hold: 18 and 19 on A1, **+5 s .. +14 s** after the note-on (phrase v lo); 22 on A2, **+9 s .. +14 s** (phrase v mid: the melt has ended in every variant, the last by 6.5 s). The first second, the whole hold, K-weighted RMS, phrase (b) and the peak of every audition phrase are reported next to it. Peak limit: the largest sample of the riff, stabs, held, drone, chord and tap renders (22 D is limited by its three-key chord at -4.1, so it sits at -18.9).

**Measures new in 5A (definitions):**

| measure | definition |
|---|---|
| wander (18) | the spectral centroid (Hann 2048, mono) in 0.5 s windows over +2 s .. +14.5 s of the hold (25 windows) on A1 and on A2: min..max, range, s.d., and the range in semitones (12 x log2 max/min); the level's s.d. over the same windows (dB) |
| slop (18) | the engine's own per-card vintage pitch (`vlog`), A1 held 13 s: static offset, s.d. and range in cents for each card the patch uses |
| melt (22) | per 0.5 s window of A2's first 8 s: the dominant fundamental by harmonic summation over 400 ms (cents re 110 Hz, `pitch_track`), the centroid and the level; the time to 90 % / 98 % of the pitch's fall (to the 8-13 s mean) and of the centroid's fall (log axis, to the 9-14 s mean). The window's end is reported |
| register (19) | A0, A1, A2, A3 each held 6 s (window +2 .. +6 s): RMS, K-RMS, peak, the energy shares (<60 / 60-150 / 150-400 / 400-1.2k / 1.2k+ Hz), the share above 60 Hz and above 150 Hz |
| key-up (22) | after the 15 s hold: the pitch and centroid in 0.5 s windows after the key-up (does the melt undo itself in the tail?), and the time to -20 / -40 / -60 dB |
| self-oscillation | `selfosc_probe` (3A) at the patch's own RESO and at 127: oscillators off, noise-fed 12 dB apart; a diff of 12 dB is a linear filter, near 0 is a filter that sings by itself |
| taps | the 150 ms gate's RMS re the held level, the centroid of the gate, the RMS 400 ms after the key-up |
| chord | three keys together: the cards gated (the host's `expect voices`) and the chord's RMS / peak |

**Engine facts found in 5A (existing controls only; nothing was coded):**

* **ENV>O2 bends OSC 2's pitch only, from the filter envelope** (`p2 += fenv x (ENV>O2 - 64) x 97 >> 15` Q8 semitones = (ENV>O2 - 64) x 24/63 st at the envelope's top; measured -675 / -904 / -1209 cents for 46 / 40 / 32 against -6.86 / -9.14 / -12.19). OSC 1 has no route, the amp envelope has none. 
* **A negative ENV>O2 on a decaying filter envelope makes the pitch RISE** (lowest at the strike). A collapse that sinks while the key is down needs a RISING filter envelope (FA = the melt time, FS 127) with negative ENV AMT and ENV>O2: cutoff and pitch then fall together. The attack is an analog RC curve: front-loaded (22 B: -441 of -675 cents in the window starting at 2.0 s; 90 % of the pitch fall at 4.0 s with FA 118 = 4.96 s nominal, 98 % at 4.5 s).
* **The key-up replays the envelope backwards:** the filter envelope releases, so pitch and brightness climb back during the amp's release tail, even at FR 127 (22 B: -634 -> -472 cents and centroid 242 -> 2529 Hz over the tail's first 1.5 s, while the level is 40-60 dB down). Not isolated whether it is audible at those levels.
* **UNISON (and MONO) play the last key only:** a three-key chord gates one unison group (3 cards at UNI_N 3, 6 at 6). A chord that melts together needs DUAL (22 D: 6 cards = 3 notes x 2).
* **There is no sub oscillator:** the lowest voice is OSC 2 at SEMI -12. On A1 that is 27.5 Hz.
* **Register changes the sub's audibility, not its RMS:** 19 B reads -18.3 dBFS RMS on A0, A1, A2 and A3 alike (a square of the same amplitude), but the energy under 60 Hz is 85 / 77 / 48 / 0 %, and the K-weighted RMS climbs -26.2 / -23.1 / -20.3 / -18.7.
* **The resonant ring is what is heard on a low sub:** at RESO 125 (past self-oscillation) 26 % of A1's energy sits in 150-400 Hz against 10 % at RESO 115; the singing does not depend on the input (probe diff 0.0 dB) and its energy lands in 150-400 Hz (suggests the filter's own frequency; not isolated). A RESO 115 LP24 and a RESO 75 / 100 LP12 are linear (probe diffs 11.2 / 10.6 / 11.7 dB); RESO 127 sings in every filter tried.
* **The MUD ratio saturates:** with almost nothing above 1.2 kHz (18 B/C, 22 after the melt) the ratio runs to the thousands (a floor at a 0.001 % share); read the band shares, not the ratio, there.
* **22's CPU is the highest of the voiced patches** (2488-2502 host instr/sample worst case against 15 D's 2375): six unison voices on one oscillator each; UNI_N 5 gives 2266, 4 gives 2046 (idle 1164, load 1324 / 1102 / 882).

**Round 1 results (the variant B of each; the full tables are `listen/voicing/batch-05a/<NN-name>/README.md`):**

| slot | committed | VOLUME | held level | K-RMS | peak (all phrases) | worst-case CPU (original) | headline |
|---|---|---|---|---|---|---|---|
| 18 Roto-scopo | B | 73 | -18.0 (A1, +5..+14 s) | -20.9 | -8.7 | 1900 (3163) | 3-voice UNISON of two squares (the second an octave down), LP12 RESO 100, smooth RANDOM LFO 0.23 Hz to the filter +-14 st; centroid A1 203..344 Hz (s.d. 33, 9.1 st), A2 347..508; VINTAGE 114: static -6.9 / +3.9 / +1.7 cents, s.d. 5.0-5.9; dry |
| 19 Blackwater **(SUPERSEDED, patch dropped 6 Nov 2026)** | B | 127 | -18.2 (A1, +5..+14 s) | -23.1 | -6.2 | 1430 (1361) | MONO, OSC 2 pulse an octave down, LP24 RESO 115 at 100 % tracking; A1: 77 % under 60 Hz, 10 % in 150-400; A2: 52 % above 60 Hz; first second 3.5 dB over the settled level |
| 22 Melting Orb | B | 77 | -18.1 (A2, +9..+14 s) | -19.5 | -7.3 | 2488 (1770) | 6-voice UNISON of saws on OSC 2, filter and pitch sink together: pitch -675 cents (90 % at 4.0 s), centroid 1328 -> 201 Hz (90 % at 3.5 s), LP12 RESO 75 |

**Proof for the batch** (`identical_par.py build/voicing/base 18,19,22`, base = the commit before the patches, the firmware unchanged from main; slot 1, the boot patch, is not touched, so the plain comparison holds): the patch bytes of 29 of 32 slots are equal (only 18, 19 and 22 differ) and the audio of the **other 29 programs is byte-identical on all 29 phrases** (a, b, c, x_stress, d, e, f, f2, g, h, x_register, i, j, k, l, m, n, o, p, q, r, s, t, u and the five new ones v lo, v mid, w lo, w mid, y); the three named slots differ on all 29.
`check_slot.py SLOT B 5a`: resolved bytes identical for 18, 19 and 22; audio bit-identical when both are loaded from INIT; from the boot patch 19 and 22 are bit-identical and 18 differs by -39.6 .. -44.4 dB (the CUTOFF / RESO slew floor of section 8, suggests; not isolated).

### 18.1 Round 2 (6 Nov 2026): decisions, 19 dropped and rebuilt

**Decisions (Vincent, after listening):** **18 Roto-scopo = variant D** ("sounds awesome"), **22 Melting Orb = variant D** ("sounds incredible"); **19 Blackwater: all variants rejected, the patch dropped completely** ("I don't see myself ever using this"). The round-1 Blackwater material stays in the repo as history, **superseded, patch dropped 6 Nov**: `dog5-docs/voicing/19-blackwater.md`, `listen/voicing/batch-05a/19-blackwater/` (README, results.json) and the section 18 text above that mentions it. Slot 19 is now a different patch.

* **18 and 22:** `PF_ROTO_SCOPO` and `PF_MELTING_ORB` set to D (18 B -> D: CUTOFF 62 -> 66, RESO 100 -> 115, LFO RATE 30 -> 15 (0.23 -> 0.11 Hz), LFO FILTER 70 -> 90 (+-14.4 -> +-23.9 st), VINTAGE 114 -> 127, VOLUME 73 -> 72; 22 B -> D: MODE UNISON -> DUAL, POLY_N 5 -> 6, VOLUME 77 -> 97). Cards `cards/18-roto-scopo.md`, `cards/22-melting-orb.md`; renders `reference-renders/18-roto-scopo_D_*.wav`, `22-melting-orb_D_*.wav`; logs rewritten as approved.
* **19 Micro-mist** (the one allowed non-value change: the preset name string `"Blackwater"` -> `"Micro-mist"` in the `FACTORY[]` table of `firmware/src/obv_patches.h`, and the array renamed `PF_BLACKWATER` -> `PF_MICRO_MIST`, its values rebuilt from scratch). Four fresh takes A haze / B glide / C warp / D tunnel, B committed provisionally. Kit: `batch05a_r2.py`, `batch05a_r2_variants.py`, `batch05a_r2_report.py`, `batch05a_r2_docs.py`; new phrases z chord, z tap, z single (section 1). Log `19-micro-mist.md`; tables and results `listen/voicing/batch-05a/19-micro-mist/`. **Not a granular engine** (no grains, freeze, reverse or pitch-shifted repeats: the log says what is lost). Level -18.0 +-1.5 over +4 .. +10 s of the held A3 C#4 E4 chord; every take about 2000 host instr/sample (CHEW off: +770 would exceed the 2300 target).
* **Proof (round 2):** `identical_par.py build/voicing/base 18,19,22` (base = `main`'s firmware): the patch bytes of 29 of 32 slots are equal (only 18, 19 and 22 differ) and the audio of the **other 29 programs is byte-identical on all 32 phrases** (the 29 of round 1 plus z chord, z tap, z single); the three named slots differ on all 32. `check_slot.py`: 18 D and 22 D resolved bytes identical, audio bit-identical from INIT (from the boot patch 22 is bit-identical, 18 differs -30.2 .. -39.0 dB); 19 B (`5a-r2`) resolved bytes identical, bit-identical from INIT, from the boot patch it differs -0.5 dB (chord) .. -15 dB: its RANDOM LFO's state follows the engine's random state (suggests; not isolated).
* **Wording fix:** "other voice cards' noise generators" -> "other voices' noise generators" in this README (section 17) and in `14-reef-break.md`.

### 18.2 Approved (6 Nov 2026): 18 D, 22 D, 19 D final

* **18 Roto-scopo = D** ("sounds awesome"), **22 Melting Orb = D** ("sounds incredible"), **19 Micro-mist = D "tunnel"** ("sounds incredible, exactly what I was imagining"). No new variants or sound decisions in the approve step: `PF_MICRO_MIST` moved from B to D (CUTOFF 74 -> 70, RESO 50 -> 40, AA 70 -> 80, AS 110 -> 127, LFO S&H at RATE 105, LFO PITCH 22 -> 0, LFO FILTER 30 -> 10 (inert), LFO AMP 8 -> 0, FEEDBK 96 -> 105, MIX 90 -> 95, ALLEY 110 -> 100, DRAIN 70 -> 80, VOLUME 100 -> 96). D's LFO is inert at those values and was left exactly as rendered.
* **Files:** cards `cards/18-roto-scopo.md`, `cards/22-melting-orb.md`, `cards/19-micro-mist.md`; renders `reference-renders/18-roto-scopo_D_*`, `22-melting-orb_D_*`, `19-micro-mist_D_*`; logs `18-roto-scopo.md`, `22-melting-orb.md`, `19-micro-mist.md` (the Blackwater log stays as superseded history); tables and results `listen/voicing/batch-05a/<NN-name>/README.md` + `results.json` (19-blackwater and 19-micro-mist included).
* **The listen branch** (`listen/batch-05a-chapter3-drones`, never merged) holds every WAV of the batch: the round-1 variants A-D of 18, 19 (Blackwater) and 22 plus the A* level-matched originals, and the round-2 Micro-mist takes A-D. The voicing branch holds no WAV outside `reference-renders/`.
* Stale doc names fixed: slot 19 is "Micro-mist" in `CLAUDE.md` and the DOG-5 planning docs (the old Blackwater brief in `DOG-5-presets.md` is kept and marked).


## 19. Batch 5B: Chapter III, the last three (20 Fire & Ice, 23 Crypt Dust, 24 Fugue State)

Round 1 (6 Nov 2026), **rendered, not yet heard**: each patch has its **variant B committed PROVISIONALLY** (own array) and A, C, D render-only; no cards, no `reference-renders/` until Vincent picks. The kit is `tests/voicing/batch05b.py` (driver and measures), `batch05b_variants.py` (the variant tables), `batch05b_report.py` (the READMEs), `lib5b.py` (small helpers), `fb24_probe.py` (24's feedback headroom), `check` via `batch05b.py --check B`. Two branches: code, docs and the small tables on `voicing/batch-05b-chapter3-fire-dust-fugue` (to be merged), every WAV on the never-merged `listen/batch-05b-chapter3-fire-dust-fugue` (`listen/voicing/batch-05b/`). Own arrays: 20 `PF_FIRE_ICE` (a copy of `PF_SYNC_LEAD`, which **26 BSyncA keeps**), 23 `PF_CRYPT_DUST` (was `PF_NOISE_WASH`, 23's alone), 24 `PF_FUGUE_STATE` (was `PF_NEON_PAD`, 24's alone). Step 0 (own commit): card 19 section 2 "bright and glassy" -> "bright".

New phrases (section 1 style, `tests/voicing/phrases/`): `aa_fire_detached` (eight 420 ms notes on a 500 ms step A3 E4 A4 C5 E5 A5 E5 C5, eight 200 ms notes on a 300 ms step, one E4 held 1.5 s; every note-off lands before the next note-on, so a MONO envelope re-fires), `ab_fire_legato` (the same notes, each note-on 50 ms before the previous note-off: no re-fire), `ad_longhold` (the triad A3 C#4 E4 held 30 s, released at 33 s, run to 45 s), `ae_repeat` (the triad 300 ms every 1000 ms, twelve times, 8 s after). Level phrases: 20 the note-on region of `d_lead`; 23 and 24 the RMS over +4 s .. +10 s of `z_chord` (the held triad). Peak limit -4 dBFS over every audition phrase.

**Variants (full parameter lists are in each `listen/voicing/batch-05b/<NN>/README.md`, every change echoed before -> after):**

| slot | A | B (committed) | C | D | axis |
|---|---|---|---|---|---|
| 20 Fire & Ice | original (MONO sync lead, CUTOFF 90, LP24, 375 ms echo FEEDBK 40, no drive) | CUTOFF 54, ENV AMT 127, GROWL 70 | CUTOFF 66, ENV AMT 105, GROWL 60 | CUTOFF 84, ENV AMT 85, GROWL 48 | the cutoff, rolled off -> open; shared: OSC 2 LEVEL 127, GLIDE 56 (94 ms), ALLEY 374 ms, FEEDBK 92, MIX 85, TONE 55, DRAIN 30 |
| 23 Crypt Dust | original (noise through a BP12) | CHEW 100, WOW/FLT 16, DROPS 90 | CHEW 50, same | CHEW 0, S&H LFO on AMP + FILTER, 75 ms echo, DRAIN 80 | the tape ladder; shared: a 12 % pulse under the noise, POLY 2 (CPU) |
| 24 Fugue State | original (pulse and saw+pulse pad, LFO PITCH 4, 750 ms echo FEEDBK 40) | LFO 0.31 Hz, +-4.7 st, FEEDBK 100, 266 ms | LFO 4.9 Hz, +-1.8 st, FEEDBK 95, 144 ms | LFO 1.14 Hz, +-7.3 st, FEEDBK 110, 266 ms | rate, depth and feedback; shared: a 25 % pulse through a key-tracking LP12 + an octave-up copy, TRI, PHASE SPREAD |

**Round 1 numbers (host; level / peak per section above; CPU = worst case idle + load, host instr/sample):**

| slot | var | VOLUME | level dBFS | K-RMS | peak | CPU |
|---|---|---|---|---|---|---|
| 20 | A / A* | 100 / 127 | -23.1 / -19.0 | -22.4 | -14.1 | 1370 |
| 20 | B / C / D | 127 / 127 / 126 | -19.3 / -18.8 / -18.1 | -18.9 / -18.4 / -17.5 | -8.8 / -8.4 / -8.4 | 1967 |
| 23 | A / A* | 100 / 127 | -31.1 / -27.0 | -28.9 | -16.1 | 2009 |
| 23 | B / C / D | 124 / 123 / 127 | -18.0 / -18.1 / -18.7 | -16.9 / -16.9 / -17.4 | -5.9 / -5.6 / -4.0 | **2456 / 2455** / 1685 |
| 24 | A / A* | 100 / 65 | -13.6 / -17.9 | -13.7 | **0.0 (2890 samples clipped)** | 2152 |
| 24 | B / C / D | 85 / 85 / 84 | -17.95 / -17.9 / -18.0 | -18.0 / -18.0 / -18.1 | -4.9 / -4.9 / -5.0 | 2039 |

**Flags:** 20 B, C and D sit at VOLUME 127, 127 and 126 (no VOLUME headroom; B reads -19.3, inside the +-1.5 band; the original cannot reach the reference either: A* 127 = -19.0). 23 B and C are over the 2400 flag line (2456 / 2455; the cap is about 2500): CHEW costs about +755 idle, so the voice count was cut to POLY 2 to get there (POLY 5 + CHEW 100 reads 2831, POLY 3 2705). 23 D sits at VOLUME 127 (-18.7) with its stabs peak at -4.0 (the limit). **23 keeps the original's 1.2 s amp attack (AA 100)**, so phrase (b)'s stabs read -24.4 dBFS (the level phrase is the held triad) and a 150 ms tap barely sounds; that is the original's trait, not a change.

**Engine facts found in 5B (existing controls only; nothing was coded):**

* **GLIDE is a time constant on a log scale; the original's GLIDE 20 is about 4 ms (no glide at all).** Time to within 50 cents of a one-octave legato step (A3 -> A4, measured): GLIDE 20 4 ms, 40 29, 50 64, 56 94, 60 124, 70 223, 80 398, 90 702, 100 1226 ms.
* **The hard-sync sweep is the slave's pitch envelope (ENV>O2) and survives a rolled-off filter only at the strike.** 20 B (CUTOFF 54, ENV AMT 127): the 1.2 kHz+ energy of the sweep reads -0.4 dB re the same patch fully open over the first 100 ms, -6.2 dB over 100-200 ms, -14.4 dB over 200-400 ms and -17.1 dB over 400-800 ms; the centroid runs 3830 -> 1356 -> 756 -> 652 Hz (sweep off: 3261 / 952 / 600 / 540). In D (CUTOFF 84) the same windows read -1.0 / -2.7 / -3.4 / -3.4 dB, in C (CUTOFF 66) -0.9 / -5.6 / -9.1 / -9.9 dB.
* **MONO legato does not re-fire the sweep:** on the same notes the centroid over the first 100 ms of notes 2-8 averages 4709 Hz detached against 759 Hz legato (20 B), 4024 / 975 (C), 3610 / 1573 (D) and, for the original, 3549 / 1782. The sweep's contribution (centroid with the sweep minus without) is +821 Hz detached against +128 legato on B. The first note of either phrase is the same.
* **GROWL on a lead (20):** crest factor of the dry note-on region 10.2 -> 6.0 dB at GROWL 70 (-4.2), 9.5 -> 5.6 at 60 (-3.9), 8.3 -> 5.1 at 48 (-3.3), RMS shift +0.18 / +0.03 / -0.03 dB (the loudness trim holds); **cost +589 instr/sample** (phrase b average + stress load, 1435 -> 2024).
* **The echo's repeats stand apart from a pad only if its envelope lets them:** a pad's long release (AR 110 is about 2.5 s) makes the delay-only return of a held chord a smear that decays with the voice, not with FEEDBK (23 D measured 3.6 s to -40 dB at FEEDBK 20 and at 80 alike). The echo columns for 23 D and 24 are therefore read on a probe copy with a fast attack and release (AA 30, AR 40); the tail columns on the real patch.
* **A tape wobble on a noise patch is read on the pulse, not the noise:** with the thin pulse alone (no noise, echo or spring) the strongest harmonic (1100 Hz) tracked in 100 ms frames: 23 B (CHEW 100, WOW/FLT 16): s.d. 7.4 cents (5-95 % -11.5 .. +13.2), 0.55 Hz; C (CHEW 50): 2.6 cents (-4.4 .. +4.0); CHEW 0: 0.0. The tape's other work on B, held A3: **4 dropouts over 6 dB (deepest 10.7 dB) in 7 s** (C, A and D: none), a hiss floor of **-53.5 dBFS** in the release (35 dB under the held level; C -65 .. -67; D -74 .. -87 from its echo and spring), centroid 3403 -> 2667 Hz (top end smeared). The hiss floor stops B's release from falling 40 dB inside 5.8 s (t20 1714 ms, t40 and t60 not reached).
* **A noise patch's MUD ratio is not the problem a low-passed noise would suggest:** all three 23 variants centre at 2.2-3.7 kHz in the held windows (MUD 0.06-1.3 across the windows; scale 10 A 2.5, 12 C 12.3, medium muddy 10-40), because a band-pass at CUTOFF 72 with the key tracking leaves 12-47 % of the energy above 1.2 kHz. The original is brighter still (centroid 3.8-4.5 kHz, MUD 0.05-0.24).
* **A TRI pitch LFO's measured excursion equals the law:** (v*v>>7) x 9.375 cents peak: 24 B PITCH 80 law 469, measured -486 / +441 (0.307 Hz); D PITCH 100 law 731, measured -707 / +703 (1.14 Hz); C PITCH 50 law 178, measured +-150 (4.89 Hz: the 60 ms analysis frames average a 4.9 Hz swing down, the law is the number to trust).
* **A 25 % pulse (PW 32) through a key-tracking LP12 (KEYTRK 127, CUTOFF 63, RESO 5) reads harmonics 3 / 5 / 7 at -17.5 / -27.9 / -37.5 dB** (a triangle -19.1 / -28.0 / -34.2): closest at CUTOFF 62-64 (PW 28: 3rd -16 and 5th -36 at cutoff 60; PW 34-36 drop the 7th to -44 .. -71 dB). The octave-up copy (OSC 2 at +12 st) adds energy on the even harmonics only, so those readings do not move; it lowers the 150-400 Hz share from 79 % (no copy) to 78 / 74 / 64 % at OSC 2 LEVEL 45 / 70 / 100 (MUD 300 -> 272 / 185 / 85). **The MUD ratio saturates here** (the 1.2 kHz+ share is 0.3-0.7 %): read the band shares.
* **FEEDBK headroom (24 D, the 30 s held triad / 12 repeated chords):** FEEDBK 110 peaks -5.0 .. -6.3 dBFS with no growth over 30 s (-1.2 dB from the 4-8 s window to the 24-28 s window), 114 and 118 likewise (-4.0 .. -6.1), 122 peaks -2.1, **127 reaches 0.0 dBFS (1 sample clipped) and the hold grows +0.5 dB**; the repeated-chord peak growth (best later chord against the first) is +2.8 dB at 110, +3.6 at 118, +5.6 at 122, +8.9 at 127. Table: `python3 tests/voicing/fb24_probe.py`.
* **The pitch gap between the direct voice and its own echo** (from the LFO law, computed): 24 B 153 cents, C 212, D 882 (8.8 semitones at the worst moment): this, not a pitch modulation inside the BBD (there is none), is what the repeats add to the seasickness.
* **From the boot patch 23 and 24 differ from their variant path (23 by -6.2 .. -16.2 dB re the patch, 24 by +2.9 .. +3.2 dB, i.e. as large as the signal; 23 has noise voices, 24 a VINTAGE walk), while 20 is bit-identical; both from INIT first all three are bit-identical on every audition phrase** (suggests the engine's random state; not isolated).

**Proof for the batch** (`identical_par.py build/voicing/base 20,23,24`, base = `main`'s firmware (84ac59a); slot 1, the boot patch, is not touched, so the plain comparison holds): the patch bytes of 29 of 32 slots are equal (only 20, 23 and 24 differ) and the audio of the **other 29 programs is byte-identical on all 36 phrases** (the 32 of 5A plus aa_fire_detached, ab_fire_legato, ad_longhold, ae_repeat); the three named slots differ on all 36. Every program array is untouched except these three: the array split alone (before any value moved) left all 32 patch hashes equal to `main`'s. `tests/run_host.sh` passes (exit 0). `batch05b.py --check B`: resolved bytes of the committed slots 20, 23, 24 equal variant B; audio bit-identical to the variant path on every audition phrase (20 also from the boot patch; 23 and 24 only with INIT loaded first, see the last fact).
