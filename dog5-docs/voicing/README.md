# Voicing the 32 — kit, phrases, loudness reference

How the factory patches are voiced *by ear, backed by numbers*. Nobody on the build side can hear: every claim is
a measurement from the host build (`tests/host.c` runs the firmware's own integer code, so the renders are what the
engine makes, minus the device's DAC), and every voicing round ends with WAVs for Vincent's ears. Per-patch logs live
next to this file (`03-half-life.md`, …); the renders in `listen/voicing/<slot>-<name>/`.

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

Anything new goes in the same folder with a header comment saying what it judges, and gets one line in
`PHRASE_FILES` (voicekit.py).

## 2. The kit — `tests/voicing/voicekit.py`

```
python3 tests/voicing/voicekit.py bank            # RMS / K-RMS / peak of all 32 factory slots on phrase (b)
python3 tests/voicing/half_life.py                # the 03 Half-Life round (variants -> listen/voicing/03-half-life/ + README)
python3 tests/voicing/batch01a.py [--only SLOT] [--quick]   # Batch 1A (30, 31, 04, 25): variants -> listen/voicing/batch-01a/<NN-name>/
python3 tests/voicing/batch01a.py --emit SLOT KEY # the C array (overrides over the defaults) of a variant, ready for obv_patches.h
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
