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

Anything new goes in the same folder with a header comment saying what it judges, and gets one line in
`PHRASE_FILES` (voicekit.py).

## 2. The kit — `tests/voicing/voicekit.py`

```
python3 tests/voicing/voicekit.py bank            # RMS / K-RMS / peak of all 32 factory slots on phrase (b)
python3 tests/voicing/half_life.py                # the 03 Half-Life round (variants -> listen/voicing/03-half-life/ + README)
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

**BANK REFERENCE LEVEL: see §5 (set by the first voiced patch, 03 Half-Life).** A later patch is matched within
≈ 1.5 dB of it, by `VOLUME` (a square law: `gain = VOLUME²/4096·…`, about 0.17 dB a step at 100; 100 is the default,
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

## 5. Current reference

*(filled in by the 03 Half-Life round — see `03-half-life.md`)*

## 6. The "other 31 are untouched" proof

```
git archive <commit before> | tar -x -C build/voicing/base      # the firmware as it was
# build both host apps, render all 32 slots on phrase (b) with each, compare byte for byte:
python3 tests/voicing/identical.py build/voicing/base            # exit 0 = only the named slot differs
build/voicing/dump_patch all                                     # and the 96-byte patch hashes, before and after
```
