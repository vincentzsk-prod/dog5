# DRAIN — listening kit

DRAIN is the spring, stage 3 of the Psych Chain (`firmware/src/obv_fx.h`): OberVave's plate reverb (Dattorro's tank)
pushed toward a spring tank. "The next closest thing", not a waveguide model.

Everything here was rendered by the host build (`tests/host.c`), which runs the firmware's own integer code. These are
the samples the FM-1 would send over USB with MASTER all the way up: 16-bit stereo, 44.1 kHz, from just before the
first note.

**This is also the first time all four stages play together.** The `chain_*` files are GROWL → ALLEY → DRAIN → CHEW.

- Where things stood first (the overflow, the CPU, the Tape routing): [STEP0.md](STEP0.md).
- Every number below: [numbers.txt](numbers.txt), from `tests/spring/analyze.py`.

**Headphones help.** Listen to the attack's splash, the 60–70 ms flutter in the tail (the "boing"), and the top of
the tail going watery (the drip). Then compare with the `*_OLD_PLATE` files at the same bytes.

## Where it sits

`voices → GROWL → output stage → ALLEY → DRAIN → CHEW → out`, the brief's order. DRAIN is the reverb, in the
reverb's place.

**New:** while CHEW is on, the effects hand it their sum **unclipped**, on a ±2× full-scale rail, and CHEW's record
stage rounds any over with its own knee. With CHEW at 0 nothing changed: the effects still end in `sat16`.

## The controls

| where | knob | byte / CC | what |
|---|---|---|---|
| SPRING, KNOB 1 | **DRAIN** | 62 / its old CC (the reverb's MIX byte, renamed) | the wet, the old MIX law (up to 0.70 of the dry). **0 = bypass, bit for bit** |
| SPRING, KNOB 2–4 | — | | nothing (one macro on the page, as DRIVE and TAPE) |
| SELECT held (SPRING +), KNOB 1 | SIZE | 59 (as before) | the decay, **0.3 … 3.0 s** (exponential; shown in s) |
| SPRING +, KNOB 2 | DAMP | 60 (as before) | **OPEN** at 0, then **20 kHz … 2.5 kHz** (shown in kHz) |
| SPRING +, KNOB 3 | PRE-DLY | 61 (as before) | **0 … 35 ms** (shown in ms) |
| FX held, KNOB 1–4 | GROWL · ALLEY · DRAIN · CHEW | — | the four macros (step 3; the title reads PSYCH CHAIN) |

- **No byte or CC moved, and DRAIN needed no new storage** (bytes 71–79 are still free).
- No factory patch's bytes changed. The 32 factory patches with the reverb on keep their SIZE / DAMP / PRE / MIX bytes,
  and those bytes now mean the spring's ranges.
- Holding HOME on the SPRING page, the map says "HOLD: SPRING +".
- Tests: `tests/spring_page.txt` and `tests/fx_layer.txt`.

## What the re-voice changed (CLAUDE.md §6: allpasses faster and shallower, short pre-delay, brighter damping, SIZE clamped)

| | old plate | DRAIN |
|---|---|---|
| tank loop | 725 ms (a hall's figure-eight) | **66 ms** (2,926 samples): a spring returns every 60–75 ms. That's the flutter |
| input diffusers | 4.8 / 3.6 / 12.7 / 9.3 ms, g 0.75 / 0.625 | **half the length** (primes 107 / 79 / 277 / 199), **g 0.6 / 0.5**: less smear, a splashier attack |
| tank's swaying allpasses | g −0.7, sway 1.0 / 0.7 Hz, ±8 samples | **g −0.5, sway 3.3 / 4.7 Hz, ±2.5 samples**: the wire's shimmer |
| tank's static allpasses | one each half, 1,800 / 2,656 samples, g 0.5 | **the chirp**: a chain of four 5-sample allpasses, g 0.7, each half, and one more at the input |
| band | input 5 kHz one-pole | **150 Hz high-pass + 6.5 kHz low-pass** (a spring's transducers: no low boom) |
| SIZE | decay 1.3 s … **23 s** (near-freeze) | **0.3 … 3.0 s**, gliding per sample |
| DAMP | ~5 kHz at default … ~55 Hz at 127 | **open** at 0, 7.5 kHz at default, **2.5 kHz** at 127 |
| PRE-DLY | 0 … 120 ms, a jump in the read | **0 … 35 ms**, a change crossfaded over one block |
| output taps | 7 a side | 5 a side (the two on the long allpasses went) |
| tank level | full | **half** (6 dB of headroom), a soft knee on the two main tank writes |
| pool | 83,098 B | **13,824 B** |

**The chirp.** A 5-sample allpass at g 0.7 isn't an echo. It's a stretched first-order allpass, which delays one
band more than the rest:

- Group delay per chain: **0.08 ms at DC, 2.57 ms at 4.4 kHz** (the stretch's corner, near a real spring's transition
  frequency). It falls off again above that.
- A loop passes two chains, so each loop spreads the 3–5 kHz band by ~5 ms more than the lows. After five loops (~0.3
  s) the band around 4.4 kHz lags by 25 ms against under 1 ms at 500 Hz.
- That rising sweep near the top is the drip. It compounds pass by pass, as dispersion does along a spring's wire.
- Measured on the firmware's integer chain: it matches the theory to 0.01 ms and stays flat in level (0.03 dB ripple).
  See `chirp_group_delay.png`.

**The tail always ends in silence.** Two things in the loop needed care:

- Plain floors in a 66 ms loop parked the tail at a DC offset.
- Rounding instead made a limit cycle: −83 dBFS for good at SIZE 80, −76 dBFS at 127.

So the allpasses round and the four decay multiplies truncate toward zero. The loop then loses at least a step per
pass. Measured: 0 from ~1.5 s after the tail falls under −85 dBFS, at any SIZE.

## The files

| source | what it is |
|---|---|
| **stab** | a short Cmaj7 stab (150 ms), twice, 2.5 s apart (INIT, POLY: two detuned saws a voice) |
| **bass** | program 1 *Red Pill* as voiced: one bar of the other kits' 8th-note riff on A1, then silence |
| **lead** | a bright mono lead, filter wide open: G5 A5 C6 short, then E5 |
| **pluck** | the spring's own test: a staccato mono pluck, a surf figure (E4 E4 G4 A4 · B4 A4), then E4 and a long E3 |
| **hit** | program 14 *Reef Break* as voiced (PERC HIT: noise and a pitched click), twice: a snare's job |

| setting | file suffix | DRAIN | SIZE | DAMP | PRE-DLY |
|---|---|---:|---|---|---|
| short boing | `_boing` | 70 | 20 (0.43 s) | 20 | 0 |
| patch defaults | `_default` | 60 | 80 (1.3 s) | 60 (7.5 kHz) | 20 (5 ms) |
| the drip, wet | `_splash` | 110 | 110 (2.2 s) | 10 (17 kHz) | 40 (11 ms) |
| a dull tank | `_dark` | 80 | 100 (1.8 s) | 120 (2.8 kHz) | 10 |
| all at the top | `_max` | 127 | 127 (3.0 s) | open | 0 |
| the same bytes, old plate | `_OLD_PLATE` | | | | |

**The whole chain** (`chain_<source>_<strength>`):

| strength | GROWL | ALLEY | DRAIN | CHEW |
|---|---|---|---|---|
| **mild** | 30 % | SYNC 1/8., FEEDBK 50, MIX 45 | the default spring, 60 | 30 % |
| **surf** | 50 % | 90 ms slap, mono | the splash spring, 110 | 50 % |
| **mangle** | 100 % | 300 ms runaway (FEEDBK 124) | DRAIN / SIZE 127 | 100 % |

- `_no_drain`: the same chain with DRAIN 0, so you hear what DRAIN adds.
- `_OLD_PLATE`: the same bytes on the build before the re-voice (the old plate, and the old routing into CHEW).

**The knobs while it rings** (on the panel: FX ×3, SELECT held, one detent every 40 ms, up, down, then a flick), over
the looped pluck:

- `sweep_size`, `sweep_damp`, `sweep_pre`.
- `jumps_hit`: SIZE, DAMP and PRE-DLY jumped end to end (as a CC would) while the splash spring rings after the hit.

**The overflow** (`tests/spring/hot_reverb.txt`: a 6-note chord at velocity 127 into GROWL 127, the reverb at SIZE /
MIX 127, from 3.5 s in):

- `overflow_plate_BEFORE_FIX`: the crack is at ~0.47 s into the file.
- `overflow_plate_fixed`: the same render with step 1's fix.
- `overflow_case_on_drain`: the same hot input on the spring.

Pictures:

- `ir_spectrogram.png`: plate vs spring impulse response.
- `decay_vs_size.png`.
- `chirp_group_delay.png`.
- `wet_spectrum.png`: the wet's band under a held noise.
- `overflow.png`: the crack and the fix, sample for sample.

## The numbers

**Decay** (T20 after a 300 ms noise burst, DAMP open):

| SIZE | 0 | 32 | 64 | 80 | 96 | 112 | 127 |
|---|---:|---:|---:|---:|---:|---:|---:|
| target | 0.30 | 0.54 | 0.96 | 1.28 | 1.71 | 2.29 | 3.00 |
| DRAIN | 0.32 | 0.56 | 0.97 | 1.29 | 1.70 | 2.24 | 2.89 |
| old plate | 1.34 | 1.46 | 1.94 | 2.47 | 3.50 | 6.17 | **23.1** |

**Level against the plate at the same bytes.**

- Bench (the reverb alone): within **±3 dB** everywhere, mostly within 2.
  - Under a held noise, the spring sits +0.6 … +2.6 dB above the plate.
  - In a note's first half second, −0.9 … −3.8 dB below it.
- Musical renders, energy against dry, default setting: spring **+1.4 / −0.1 / +0.9 / +1.7 / +1.2 dB**, plate +0.7 /
  +0.1 / +0.7 / +0.7 / +0.7 (stab / bass / lead / pluck / hit).
- **On splash the spring is louder on the percussive sources** (stab +5.3 vs +3.6, pluck +5.4 vs +3.5) **and quieter
  on bass and lead** (bass +0.1 vs +3.4, lead +1.9 vs +3.6).
- That is the band, not the gain: the spring is thinner and brighter. See the next section.

**No sample at full scale** in any source × setting render, nor in any chain render, mangle included. Peaks:

| | peak |
|---|---|
| stab at max | −0.4 dBFS |
| chain stab mangle | −3.1 dBFS |
| chain lead mangle | −6.0 dBFS |
| chain bass mangle | −9.1 dBFS |

**Clicks:** none.

- **Bench** (`tests/spring/clicks.py`: a pure 440 Hz sine, so a linear reverb's wet holds nothing above 2.5 kHz; the
  jumps are end to end, at once). SIZE, DAMP and PRE-DLY jumped, with the sine still playing and with the tail alone:
  **0 click candidates**. At every jump the spring's HF stays at the last bits (−85 … −99 dBFS).
- **The old plate as the control**, the same jumps: 121 candidates. Its HF rose 9–25 dB, to −47 … −70 dBFS. It stepped
  its decay per block and jumped its pre-delay read.
- **Host**: the three knob sweeps over a held dark pad have **0 candidates**, and the HF stays at −90 dBFS, the same as
  the pad held still. `jumps_hit`: only the hit's own attack.

**Bypass:** byte-identical to the build before the re-voice (`tests/drive/bitexact.sh db0701c`) on **189 renders**:

- every factory program with DRAIN at 0 (`tests/spring/factory_norev.txt`);
- every GROWL, ALLEY and CHEW kit render, CHEW > 0 and its sweeps included;
- the hardest CHEW render with DRAIN at 0 (`tests/spring/worst_voices_norev.txt`);
- the UI scripts.

**The only renders that change are the ones with the reverb on.** So the routing change into CHEW and its new record
knee changed none of the CHEW kit's renders: none of them ever reaches the knee.

## The overflow fix, and whether it changed anything that wasn't broken

**Step 1** (its own commit, `db0701c`) clamps the plate's tap sum to ±109,225 before the ×0.6. Below that it is the
identity; above it, it gives 2× full scale, which the output's clip pins exactly where the true product would have.

The proof:

- **Byte-identical on 186 renders** against the build before it: all 32 programs, an 18-setting reverb grid
  (`tests/spring/rev_grid.txt`), every GROWL, ALLEY and CHEW kit render, the UI scripts.
- On the two hot scripts, exactly the 76 and 29 overflowed frames change, and they now equal the exact (int64) maths.
  0 frames differ from it.
- The largest step between neighbouring samples drops from **65,534 (a rail-to-rail crack)** to 7,862.
- `tests/spring/regress.sh` (in `tests/run_tests.sh` now) runs under `-fsanitize=signed-integer-overflow,bounds`:
  - the hot scripts, `tests/tape/worst_voices.txt`;
  - the whole chain at its extremes with the spring's knobs jumped at random (`tests/spring/worst_chain.txt`);
  - 112 bench runs of the worst signals an int16 line carries.
  - All clean. On the pre-fix code it fails.

**So the fix itself changed no tail that wasn't broken: proven bit for bit.** The tails that changed, changed because
of the re-voice (step 2), which replaced the plate.

## The four stages together: what I found (flagged for your ears)

1. **The old plate was what made the chain a wall.** On the build before, the mangle chain on bass and lead comes out
   **2.4–2.9 LU louder** than now (bass −19.5 vs −21.9 LUFS, lead −13.1 vs −16.0). The plate at SIZE 127 was a 23 s
   near-freeze that piled the runaway ALLEY's repeats up into a wash. The spring stops at 3 s, so the runaway stays
   audible as repeats. Compare `chain_lead_mangle.wav` with `_OLD_PLATE`.
2. **DRAIN does almost nothing on bass.** On Red Pill it adds −0.1 … +0.5 dB (mild and surf), +2.7 at mangle. The plate
   added +0.1 … +6.8. That's the 150 Hz high-pass into the tank: a spring has no bass, and the low end stays dry and
   tight under it.
   - If you want the bass's harmonics wetter, the HP corner (`SP_HP_K`) is one constant.
   - If you want the spring to carry the bass's fundamental, it's the wrong effect: that's the brief's point.
3. **The spring is coloured.** Under a held noise its wet has narrow resonant peaks, up to about +13 dB between 150 and
   600 Hz (`wet_spectrum.png`). Those are the short loop's modes. The plate's wet is flat. Real spring tanks are very
   coloured too, but **this is the thing to judge by ear**: "boingy and metallic" is right, "tubby" is not. Listen to
   `pluck_splash.wav` and `hit_splash.wav`. The levers, if it's tubby:
   - more sway depth (it moves the peaks; costs nothing);
   - a longer loop (fewer, denser modes; less flutter);
   - the input diffusers' g back up (more smear).
4. **Pads drove the spring's tank into clipping, before a fix in this session.** At full level, four factory programs'
   sustained chords hard-clipped the tank's int16 lines (up to +3 dBFS inside the loop), where the plate's longer loop
   never did: **08 Wire Bite, 13 Ghost Board, 16 Tidal Pull, 24 Fugue State**. Held notes build the 66 ms loop's modes
   up.
   - Fixed in `a6a73d1`: the tank runs at half level (6 dB of headroom), and a soft knee (linear to 0.75 of full scale,
     then tanh) sits on its two main writes.
   - Now no program clips it. Two touch the knee: Wire Bite on 87 samples, Fugue State on 5.
   - At the chain's extremes (`worst_chain`) the knee works on ~1 % of tank writes. It rounds instead of hard-clipping.
5. **CHEW's record knee is mostly idle**, and that's correct.
   - With CHEW at 100 % the record is fully tanh(1.5x)/1.5, which never reaches −2 dBFS.
   - In every kit render the effects' sum stays under full scale, mangle included (CHEW and GROWL hold the level).
   - The sum only goes over in the stress scripts: `hot_reverb` +2.3 dBFS, `worst_chain` +6.1 dBFS. The ±2× rail
     engaged on **6 samples** of `worst_chain` and nowhere else.
   - So the routing change matters at low-to-mid CHEW with a hot sum. There it rounds what used to be a hard clip.
6. **The spring is louder than the plate in the chain on the percussive sources** (surf: stab +5.6 vs +3.6 dB, pluck
   +5.7 vs +3.5) and quieter on bass and lead. That's the band again (thinner, brighter, splashier). No factory patch
   changed, but **the 32 patches with the reverb on now sound a spring at their old bytes**: worth a pass when you
   voice them.
7. **The tail's last ~30 dB end early.** An impulse into SIZE 64 reaches exact silence at ~0.55 s (`ir_spectrogram.png`),
   once it's under ~−80 dBFS. That's the toward-zero truncation that kills the limit cycle, a little stronger with the
   tank at half level: SIZE 127 measures 2.89 s for 3.0. It's below CHEW's hiss and any room. Flagged in case you hear
   a "gate" on very quiet tails in headphones.

## Bypass, overflow, memory, CPU

**Device build** (`./build.sh`, `-Os`, no 64-bit division: the link has no `__divdi3`):

| | step 0 | now |
|---|---:|---:|
| pool | 275,868 B | **206,592 B** (−69,276: the spring's lines are 13.8 KB, the plate's were 83 KB) |
| RAM | 32,304 B | 32,368 B (+64: the chirp's rings, 192 B, less the plate's line headers) |
| image | 107,920 B | 109,716 B (+1,796: code, the spring's tables, the display kinds) |

**CPU** (host callgrind, `tests/tape/perf_*.txt`: program 1 in POLY, a held Cmaj7, the stage on for 299,880 frames).

The "everything off" run got **6.8 M Ir cheaper** (`fx_process` now returns at once when the delay and the spring
rest). That moves the baseline the per-stage numbers are taken against, so the absolute counts are the fair
comparison:

| script | step 0 Ir | now Ir | Δ / sample (over the stage's 299,880 frames) |
|---|---:|---:|---:|
| everything off | 267,117,879 | 260,322,688 | −22.7 |
| GROWL 100 | 489,386,808 | 483,583,130 | −19.4 |
| ALLEY (mix 60) | 359,979,965 | 364,082,030 | +13.7 |
| reverb (mix 60): old plate → **DRAIN** | 439,947,693 | 442,583,745 | **+8.8** (the fix +11.0, the spring −2.2 against the fixed plate) |
| CHEW 100 | 555,234,259 | 549,951,676 | −17.6 |
| **all four** | 1,043,252,469 | **1,054,083,499** | **+36.1** |

**The running total, all four on, over the whole window** (voices included): **2,812 instructions a sample** (step 0:
2,784, +1.0 %).

Per stage while on, against the new off run: GROWL 745, ALLEY 346, **DRAIN 608**, CHEW 966, all four **2,647** (step 0,
against the old off run: 741 / 310 / 576 / 961 / 2,588).

The spring costs what the plate did. Taking the chirp's 12 allpasses was paid for by:

- masked power-of-two lines with one write index for all, instead of compare-and-wrap, and the chirp chains written
  out: together 799 → 590 a sample, measured;
- 10 output taps instead of 14;
- no output multiply.

The device is the truth: the GLOBAL page's µs.

**The CPU lever** (`REV_DIV 2`, the spring at half rate) still compiles and runs clean under the sanitizer, and keeps
its decay times (0.31 / 1.25 / 2.77 s at SIZE 0 / 80 / 127). Untested on the device, as before.

## Not done here, on purpose

- **No factory patch changed** (`obv_patches.h` untouched).
- **No DWELL knob.** A spring's "dwell" (input drive into the transducer) would want its own byte (71) and CC. The
  tank's soft knee gives hot inputs a bit of that crunch already. Ask if you want it as a fourth knob on SPRING +.
- **The SMK-37's fader bank** (`obv_smk.h`) still maps GROWL / BBD MIX / REVERB MIX. It's that board's own panel, not
  the FX-held layer, so I left it. The REVERB MIX fader is DRAIN now.
- **The browser simulator** (`docs/sim`) is still the stale wasm from upstream OberVave 1.4 (`db799dd`). Its test in
  `tests/run_tests.sh` fails, and failed before this session too, with the same numbers. It needs `web/sim/build.sh`
  with emscripten, which this environment doesn't have.

## Reproduce

```bash
python3 tests/spring/make_scripts.py
tests/spring/render.sh
python3 tests/spring/make_kit.py
tests/spring/regress.sh
python3 tests/spring/clicks.py build/spring/kit/bench build/spring/kit/bench_db0701c
tests/drive/bitexact.sh db0701c tests/spring/factory_norev.txt tests/spring/worst_voices_norev.txt
```
