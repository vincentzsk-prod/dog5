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
python3 tests/voicing/check_slot.py SLOT KEY      # the committed slot against its variant: resolved bytes, and the audio from the boot patch and from INIT
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
* **A unison's attack from silence reads slow (13 ms to 90 % of the plateau on 08) and it is the stack, not the envelope:** the same patch with UNI_N 1 or 2 reads 1.2-1.5 ms (AMP ATTACK 2 = 0.5 ms); six detuned voices beat, so the level moves a couple of dB and the 90 % crossing lands where the beat does.
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
* **GROWL's loudness trim reads the output stage, so VOLUME changes how a note from silence starts:** judge and set a fuzz at its final VOLUME. A heavily clipped patch (06: held crest 1.7 dB) matches the level reference on its own phrase and reads about 2 dB hot on the chord phrase (b).
* **A change to slot 1 (the boot patch) shifts the first moments of the echo and spring programs:** CUTOFF / RESO smoothing stops short of its target by up to 63/256 when approaching from below, and that state, with the echo's and the spring's, is carried over from the boot patch into the first program loaded. Compare against a boot-matched base (`make_mid.py`), not the plain base, whenever slot 1 changes.
* **The audio cannot show cents of drift in a six-voice stack** (its own beating is ~8 cents s.d.): use the engine's `vlog` and the LFO law. **A unison's attack from silence reads slow** (13 ms) with six detuned voices and 1.2-1.5 ms with one or two: it is the stack's beating, not the envelope.
* **Brighter hides the zap:** a zap measured as the top burst over the body shrinks as the body brightens (08: +4.6 dB at CUTOFF 80, -2.0 dB at CUTOFF 90 with the second oscillator at +19 st); D was approved by ear regardless, so the burst is a diagnostic, not a target.
