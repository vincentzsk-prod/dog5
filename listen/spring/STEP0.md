# DRAIN (Spring) — step 0: where the reverb stands before the re-voice

Measured on `claude/psych-spring` at `f15fd96` (= `claude/psych-bbd`: main + GROWL + CHEW + ALLEY), before any change.
The overflow is reproduced on unmodified `main` (`9e8f638`, the old delay) as well.

## a. The reverb's integer overflow

### Reproduce

```bash
cc -O2 -g -fsanitize=signed-integer-overflow,bounds -Wno-unused-function -DOBV_HOST -DAPP_VER='"dev"' \
   -Ifirmware/src -Ifirmware/gen -o build/host/obv-san firmware/src/obervave.c
build/host/obv-san build/host/hot tests/spring/hot_reverb.txt
```

```
firmware/src/obv_fx.h:246:16: runtime error: signed integer overflow: -111151 * 19661 cannot be represented in type 'int'
firmware/src/obv_fx.h:247:16: runtime error: signed integer overflow: 109381 * 19661 cannot be represented in type 'int'
```

Two scripts make it happen with ordinary playing. Both use program 1 in POLY at VOLUME 127, a 6-note chord at
velocity 127 held for 3 s, and the reverb at SIZE 127 / MIX 127 / DAMP 0 / PRE-DLY 0:

| script | the hot input | overflowed reverb samples | where |
|---|---|---:|---|
| `tests/spring/hot_reverb.txt` | GROWL 127 | **76** in 5 bursts of 1–33 samples | 3.97 – 4.51 s (1.3 s into the chord) |
| `tests/spring/hot_reverb_vdrive.txt` | the voices' own DRIVE 127, no other effect | **29** in 1 burst | 4.32 s |
| `tests/bbd/worst.txt` with REV_MIX 127 | 8-voice unison, GROWL + CHEW + runaway ALLEY | 245 | |

The plain chord without a drive peaks at 0.92× the limit, so it stays just under.

The bench (`tests/spring/spring_bench.c`: the effects alone, fed the worst signals an int16 line can carry) overflows
in the same place. It took full-scale squares at 50 / 440 / 2000 / 7000 Hz, alternating rails, and full-scale noise,
at SIZE 100 and 127 with DAMP 0. **Nothing else in the reverb overflowed**: not the four diffusers, not the tank's
allpasses, not the decay multiplies, and not with DAMP 127 either.

### What overflows

`rev_tick`, `obv_fx.h:246-247`:

```c
a = line_read(&rv_d3, …) + line_read(&rv_d3, …) - … ;   /* Dattorro's seven output taps per side */
rv_yl = (a * 19661) >> 15;                              /* × 0.6 */
```

Every tap is an int16 from a tank line (each line write is `sat16`'d), so the sum `a` can reach 7 × 32,767 = 229,369.
The ×0.6 is done as a 32-bit product, `a × 19661`, and that leaves int32 once |a| > **109,225**: the seven taps
together are more than 3.33× full scale.

A hot input fills the tank: at SIZE 127 the decay is 0.96, and the tank's lines hard-clip at int16. Once that happens,
the taps line up in sign and their sum crosses the limit.

**In C this is undefined behaviour** (signed overflow): the standard allows any result, or for the compiler to assume
it never happens.

### What it actually does on the chip

The device build (`-Os`, the JieLi pi32v2 toolchain) compiles it to a plain 32-bit multiply that keeps the low 32 bits,
followed by an arithmetic shift. From `objdump -d build/obervave.elf`:

```
2003298:  r5 = 19661
200329c:  r3 *= r5            ; 32 x 32 -> low 32 bits: wraps mod 2^32
200329e:  r6 = r3 >>> 15      ; arithmetic shift
```

So in practice it **wraps** (two's complement). The host's x86 `imul` does exactly the same thing, so the host WAV is
what the FM-1 plays.

What the wrap sounds like:

- A sum just over the limit wraps to a big number of the **opposite sign**. For example, a = +109,381 should give
  +65,628, and gives about −65,500 instead.
- That value × MIX goes into the output, and the final `sat16` pins it to the **opposite rail**.

I compared the wrapped output with the same build computing the product exactly (int64):

| | GROWL case | voice-DRIVE case |
|---|---:|---:|
| frames that differ | 76 | 29 |
| polarity flipped | **all 76** | **all 29** |
| error | 65,534 LSB = **2× full scale (+6 dBFS)** | the same |
| largest step between neighbouring samples, wrapped | 65,534 | 65,534 |
| largest step between neighbouring samples, exact | 7,862 | 6,967 |

So each burst is one channel slammed from one rail to the other for 0.02–0.75 ms: **a loud crack**, not silence and
not a long transient.

**It does not persist.** The output taps only read the tank, and nothing feeds `rv_yl` back, so the reverb's state
and its tail carry on exactly as if nothing had happened. Every click is confined to the overflowing samples.

With CHEW on, the spike also goes through Tape's filters and loudness detector, so it gets smeared and can nudge
Tape's slow trim. The DØG-5 renders here have CHEW off.

### The fix I propose (not applied yet)

Clamp the tap sums before the multiply:

```c
rv_yl = (clampi(a, -109225, 109225) * 19661) >> 15;
rv_yr = (clampi(b, -109225, 109225) * 19661) >> 15;
```

- **Exactly the same result wherever it didn't overflow.** |a| ≤ 109,225 passes through untouched, so every render
  that was never broken stays bit-identical (this is proven in step 1).
- **Where it did overflow, the output becomes what the maths meant.** At the clamp, rv_yl = ±65,535, which is twice
  full scale. × MIX that is still past the final `sat16`, so the clamped output equals the exact int64 output
  sample for sample. I checked both scripts: **0 frames differ from the exact product**, and the largest
  sample-to-sample step drops to the exact one (7,862 / 6,967).
- **Why not a soft knee here?** A knee has to start below the limit, so it would change renders that were never
  broken. Any rounding of the reverb's loudest moments belongs to the re-voice (step 2) and to Tape's record knee (c),
  not to the bug fix.
- **Cost:** two `clampi` per reverb tick, 4 compares, about +4–6 host instructions a sample (measured in step 1).
  **Pool +0 B**, RAM +0 B.

## b. The running total today

These are host callgrind numbers (`tests/perf_callgrind.sh` on `tests/tape/perf_*.txt`: program 1 in POLY, a held
Cmaj7, the stage on for 299,880 frames). An effect's cost = (Ir − Ir with everything off) / 299,880. They reproduce
the BBD session's numbers to the instruction, as callgrind is deterministic.

| stage | Ir | instructions / sample while on |
|---|---:|---:|
| everything off | 267,117,879 | (713 over the whole window) |
| GROWL 100 | 489,386,808 | **741** |
| ALLEY (mix 60) | 359,979,965 | **310** |
| old reverb (mix 60) | 439,947,693 | **576** |
| CHEW 100 | 555,234,259 | **961** |
| **all four** | 1,043,252,469 | **2,588** (2,784 over the whole window, the voices included) |

**Pool** (device build, `./build.sh`, toolchain from `tools/get_vendored_deps.sh`): **275,868 B of 344,064**. The
image is 107,920 B and RAM 32,304 B. Where the pool goes:

| what | B |
|---|---:|
| ALLEY's two 743 ms lines | 131,072 |
| **the reverb** | **83,098** |
| CHEW's line | 4,096 |
| the screen canvas and the rest | ~57,600 |

The reverb's 83,098 B are its 120 ms pre-delay (16,384 B) and the plate's 13 lines.

## c. The Tape routing: safe now, and what changes

**Yes, it's safe**, and the overflow fix is what makes it safe.

Today the overflow's wrapped spike is clipped to a rail by `fx_process`'s final `sat16` before Tape sees it. Hand Tape
the unclipped sum without the fix, and a bogus ±2× full-scale step would go straight into its record stage and
filters. With the clamp:

- Every value the effects add is a true signal value.
- The reverb's wet is bounded at ±65,535 × MIX, and so is ALLEY's.
- The dry is the output stage's tanh, ≤ 31,600.

So the sum is a real, bounded overshoot: at most ~1.3 × 10^5, no risk inside int32. Measured so far it goes up to
+3.3 dBFS (BBD session: a runaway at full mix plus the reverb at 127).

What changes (applied in step 2, together with the re-voice, as you asked):

1. **`fx_process` ends in a clamp to ±65,534 (2× full scale) instead of `sat16` while Tape runs** (`tape_on()`). That
   is a safety rail Tape's halfbands and detector need. With CHEW 0 it keeps `sat16`, so every CHEW-0 render, and so
   every bit-exact bypass proof, is untouched.
2. **Tape's record stage gets its own knee instead of `sat16`** (`tp_sat`): linear up to −2 dBFS (26,029), then
   `K + R·tanh((|u| − K)/R)` (R = 6,738, Drive's tanh table) towards full scale, whatever CHEW is.
   - Slope 1 at the knee, so no corner.
   - Tape rounds every over at 2×, so its line never hard-clips.
   - At high CHEW the blended tanh(1.5x) already keeps the record under the knee. The knee matters at low CHEW, where
     the record is nearly linear.
3. **Two guards inside Tape** for the bigger input:
   - The K-weighted detector's input `L+R` is clamped to ±65,534, the range it was written for.
   - The bypass crossfade's `(y − x) × tp_mix` is clamped to ±131,071 before the multiply. With x up to 65,534 it could
     otherwise leave int32 in theory.
   - Neither changes a value that fitted before.
4. **Tape's final `sat16` stays**: it's the DAC's limit.

Who hears a difference:

- **Only CHEW > 0 renders whose effects sum passes full scale, or whose record passes −2 dBFS.**
- The Tape and BBD kits' loudest renders peak at −3.8 dBFS and −4.4 dBFS. Step 2 checks they stay bit-identical; if any
  one isn't, it's listed.
- CPU: the knee is one compare in the usual path, ~+5–10 a sample with CHEW on. Pool +0.

## Reproduce

```bash
tests/spring/regress.sh                 # (step 1) the sanitizer on the hot scripts and the bench's grid
tests/perf_callgrind.sh tests/tape/perf_all4.txt
JIELI_TOOLCHAIN=~/.jieli/toolchain AC79_SDK=~/fw-AC79_AIoT_SDK ./build.sh
```
