# Host CPU baseline — stock OberVave (v1.5.3, before any DØG-5 engine change)

## Why this exists

`tests/host.c`'s `OBV_PERF=1` path reads a Linux hardware performance counter
(`perf_event_open`, `PERF_COUNT_HW_INSTRUCTIONS`) around each `app_audio()` call to print
instructions/sample — the project's own stand-in for the device's real render time (CLAUDE.md §2:
"Audio ISR budget... Device render time shows on the GLOBAL page in µs... Measure on the device
before trading any sound quality").

That path doesn't work in this project's cloud build containers. Confirmed directly:

```
$ OBV_PERF=1 build/host/obervave build/host/obervave
  ...no "perf" line...
```

`perf_event_open` itself returns `ENOENT` here (checked with a 5-line standalone test of the same
syscall `tests/host.c` makes) — there's no hardware PMU exposed to the process in this sandboxed
environment, not a code or permission problem; `perf_event_paranoid` is 2 (the usual default), but
that governs *access*, and the failure here is *no such counter available* regardless of privilege.

## The stand-in: `tests/perf_callgrind.sh` (Valgrind's Callgrind)

Callgrind simulates the binary instruction-by-instruction rather than sampling a hardware counter, so
it needs no PMU and runs anywhere Valgrind runs (confirmed present here: `valgrind-3.22.0`). It gives
an **instruction *fetch* count** (`Ir`), which is the same quantity `PERF_COUNT_HW_INSTRUCTIONS`
reports (instructions executed), just counted by re-execution instead of sampled by hardware.

`tests/host.c` already brackets each `app_audio()` call with the perf counter's
reset/enable/disable, past a 1-second warm-up, and divides the total by the frames rendered in that
window (`perf_frames`) — that's the exact scope `OBV_PERF` measures. The callgrind path added
alongside it (`#ifdef OBV_CALLGRIND`, so the normal `tests/run_host.sh` build is untouched and
unaffected) brackets the same calls, past the same warm-up, with
[`CALLGRIND_TOGGLE_COLLECT`](https://valgrind.org/docs/manual/cl-manual.html) — a no-op client
request outside Valgrind, so it costs nothing when `OBV_CALLGRIND` isn't defined or the binary isn't
run under Valgrind. Run with `--collect-atstart=no`, so instruction collection is off by default and
only turns on inside those brackets: everything else (boot splash, screen draws, WAV writes, key/MIDI
handling outside the render call) is excluded from the count, exactly as `OBV_PERF` excludes it.

Run it:

```bash
tests/perf_callgrind.sh            # FM-1 build, the default script (tests/run_host.sh's SCRIPT)
BOARD=smk37 tests/perf_callgrind.sh   # SMK-37 build, same script
```

It builds `build/host/obervave-cg` with `-DOBV_CALLGRIND`, runs it under
`valgrind --tool=callgrind --collect-atstart=no --combine-dumps=yes`, and prints the frame count and
Callgrind's `Ir` total; instructions/sample is `Ir` total ÷ frame count.

## Measured baseline (2026-10-29, commit `92b31cb`, the default host test script)

| Build | Frames (past the 1 s warm-up) | `Ir` (instructions fetched) | Instructions / sample |
|---|---:|---:|---:|
| FM-1 (`obervave`) | 242,432 | 248,164,601 | **1,024** |
| SMK-37 (`obervave-smk37`) | 242,432 | 248,465,458 | **1,025** |

Re-run twice for the FM-1 build: **bit-for-bit identical** both times (`248,164,601` / `242,432`
exactly). That's the one real advantage over `OBV_PERF`'s hardware counter, which the existing code
comment already flags as noisy run to run — Callgrind re-executes the binary rather than sampling, so
there's no run-to-run variance to average out.

The default script plays program 01 (DARK ARP) — not the heaviest patch in the bank. The number sits
inside the range the code's own comment already uses as a yardstick ("sloopDX's engines sit at
~1000-1500 here and fit the ISR" — `tests/host.c`), and well under the worst case the 2026-10-13
session notes in `CLAUDE.md`'s preserved OberVave section recorded on this same host build (8 voices,
LP24, sync + x-mod, saw+pulse, drive: ~1900; BRASS STAB ~1600). A heavier patch would need its own run
of `tests/perf_callgrind.sh` with a script that plays it.

## What this number is — and isn't

**This is a host-only relative yardstick, not a measurement of the device.** Two different things are
being counted on two different machines:

- **Different instruction set.** The host build runs x86-64 instructions on this container's CPU. The
  device is a JieLi AC791N (no FPU — CLAUDE.md §2) with its own instruction set. "1,024 x86-64
  instructions" and "1,024 AC791N instructions" are not the same amount of work, and there's no fixed
  conversion factor between them.
- **Different build flags.** The host build here uses `-O2` (`tests/run_host.sh`, `tests/perf_callgrind.sh`)
  for a fast test loop. The device build is **required** to use `-Os` (CLAUDE.md §2, hard rule — `-O2`
  on-device is a brick-class USB-MIDI bug) and the real engine is entirely fixed-point/integer, with no
  FPU to fall back on. Flag and codegen differences alone can move an instruction count substantially.
- **No ISR, interrupt, or DMA-wait overhead.** The host build's `app_audio()` call is a plain function
  call in a loop; the device's audio ISR runs inside real interrupt and DMA-wait conditions (the
  `app_idle()` draw-rule in CLAUDE.md §6 exists because of exactly that kind of device-only timing).

So: this baseline is useful for **relative** comparisons on the host — did a DØG-5 engine change (the
Psych Chain, `P_POLY_N`, anything in `obv_engine.h`/`obv_fx.h`) make the render noticeably heavier or
lighter than this 1,024/1,025 baseline, measured the same way, on the same host. It is explicitly
**not** a substitute for the real number. **The device is the truth**: CLAUDE.md §2's budget (5,800 µs
per ISR call, aim under half) is measured on the actual FM-1's GLOBAL page, in µs, not inferred from
this count — every sound-quality trade-off still has to be decided there, per the existing project
rule, once the unit is in hand.

## The Psych Chain, stage 1: GROWL replaces the chorus (2026-11-02)

Measured the same way (`tests/perf_callgrind.sh`), on one script: program 1 switched to POLY, a held Cmaj7 (C4 E4 G4
B4) from 3.0 to 9.0 s, the effect under test switched on at 2.7 s. An effect's cost is its `Ir` over the effects-off
run, divided by the 299,880 frames it was on (instructions per sample, host x86-64, `-O2`).

| Stage | Before (chorus build, `cf9f246`) | After (GROWL build) |
|---|---:|---:|
| Everything off (the voices) | 269,667,985 Ir | 266,984,658 Ir |
| Chorus (mix 70) | **169** / sample | (gone) |
| GROWL (any setting: the clip is branch-free) | — | **742** / sample |
| BBD delay (mix 60) | 107 / sample | 109 / sample |
| Spring / plate reverb (mix 60) | 566 / sample | 566 / sample |
| All of them on | **843** / sample | **1,417** / sample (**+574**) |

Over the whole 8.5 s window (the way the table above this section counts): all on 1,394 -> 1,846 instructions per
sample; everything off 720 -> 712.

GROWL's 742 is two channels of: a 2-pole pre-clip low-pass, 4x up (6 allpass sections), 4 table soft clips, 4x down
(6 sections), DC block, TONE, makeup, and the loudness detectors. It was 1,572 before the inner loop was written out
(halfband loops unrolled: -525) and the clip read the table once, branch-free (-213), and the halfbands went from 5+3
to 4+2 coefficients (-95: tests/drive measured the same aliasing). GROWL 0 costs nothing: the engine skips it.

Memory (the device build, `./build.sh`): pool 273,820 -> **271,772 B** of 344,064 (the chorus's 2 KB line gone; GROWL
keeps no lines). RAM .data+.bss 31,536 -> 31,824 B (+288: GROWL's filter states). Image 92,768 -> 95,672 B (+2,904:
the code and 640 B of tables).

**If the device's render time is too high with all of it on** (the GLOBAL page, aim < 2900 us), the levers in order of
what they cost the sound (estimates, not measured): (1) `REV_DIV 2`, the half-rate reverb (CLAUDE.md section 6;
roughly half of its 566); (2) GROWL in mono, one channel for both (half of its 742 by construction; a driven pad loses
its stereo spread); (3) GROWL at 2x instead of 4x (roughly a third of it; the pre-clip low-pass would have to close to
~2 kHz at the top to keep the same aliasing). None is taken: the device decides.

## The running total, re-measured before TAPE (2026-11-02, main at `6630c5b`)

The scripts are committed now (`tests/tape/perf_scripts.py` writes `tests/tape/perf_*.txt`; the same recipe as the
GROWL section: program 1 in POLY, a held Cmaj7 3.0-9.0 s, the stage(s) on at 2.7 s, 299,880 frames on). Run:
`for s in off growl dly rev all3; do tests/perf_callgrind.sh tests/tape/perf_$s.txt; done`.

| Stage | Ir (374,784 frames past the warm-up) | Instructions / sample while on |
|---|---:|---:|
| Everything off (the voices) | 268,155,759 | (715 over the whole window) |
| GROWL 100 | 489,450,503 | **738** |
| BBD delay (old ping-pong, mix 60) | 300,896,311 | **109** |
| Spring (old plate, mix 60) | 437,967,378 | **566** |
| GROWL + delay + reverb | 692,002,674 | **1,413** (1,846 over the whole window) |

Device build (`./build.sh`, the vendored toolchain): image **95,912 B**, RAM .data+.bss **31,824 B** of 98,304, pool
**271,772 B** of 344,064 (72,292 B free).

## The Psych Chain, stage 4: TAPE (CHEW) added (2026-11-02, branch `claude/psych-tape`)

The same scripts, plus `perf_chew` (CHEW 100 alone) and `perf_all4` (GROWL 100, delay 60, reverb 60, CHEW 100).
`tape_process` is `noinline`: inlined into `engine_audio` it shifted the voice loop's code and cost the *everything
off* run 7.3 M Ir (19 / sample) with TAPE never running; as a call (once an ISR) the off run is back to 267.1 M.

| Stage | Ir | Instructions / sample while on |
|---|---:|---:|
| Everything off | 267,119,336 | (713 over the whole window) |
| GROWL 100 | 489,681,266 | 742 |
| BBD delay (mix 60) | 299,859,888 | 109 |
| Spring (mix 60) | 436,930,955 | 566 |
| **CHEW 100** | 555,239,232 | **961** |
| GROWL + delay + reverb | 692,233,437 | 1,418 |
| **All four** | 980,408,818 | **2,379** (2,616 over the whole window, the voices included) |

CHEW 0 costs nothing (the engine skips it; byte-identical output, `tests/drive/bitexact.sh 6630c5b`). CHEW costs the
same at any setting above 0. Where its 961 go (callgrind, line by line): the 6-tap reads ~170 (4 a frame: 2 sub-samples
x L/R), the four tanh records ~150, the read's tap weights ~130 (2 a frame, shared by L and R), the halfbands up/down
~110, the K-weighted loudness detectors ~60, the hiss ~40, the rest (bump, head loss, glides, crossfade) ~300.

Device build: image 95,912 -> **103,316 B** (+7,404: code and 2.8 KB of tables), RAM 31,824 -> **32,208 B** (+384),
pool 271,772 -> **275,868 B** of 344,064 (+4,096: the tape line, 1024 stereo int16 frames at 88.2 kHz; 68,196 B free).

**TAPE is now the heaviest stage**, and all four together are ~2.4x what the chain cost before GROWL. If the device's
GLOBAL page says it is too much (aim < 2900 us), TAPE's own levers, in the order of what they cost the sound (host
estimates, not measured): (1) the record's saturation at 1x instead of 2x (~-75; it aliases above ~7 kHz at full CHEW,
under -60 dB re the tone); (2) a 4-point Hermite read instead of the 6-point (~-110; the wow's sidebands rise from
-80 to -43 dB under a 10 kHz tone, audible as a grainy top on bright patches); (3) the whole line at 1x (~-400; the
sidebands at -30 dB under 10 kHz: a fizz on the top octave under wow). Before any of these: `REV_DIV 2` (~-280) and
GROWL in mono (~-370), as the GROWL section says. None is taken: the device decides.

## The Psych Chain, stage 2: ALLEY (the BBD) re-voices the delay (2026-11-02, branch `claude/psych-bbd`)

The same scripts (`tests/tape/perf_*.txt`; `perf_dly` is ALLEY at MIX 60 in SYNC, which costs the same as any other
setting: the loop has no branches on the settings). `fx_process` is `noinline` now: inlined, the bigger loop moved the
voice loop's code and cost the *everything off* run +8.5 M Ir with no effect running (the same thing CHEW's section
describes); as a call, the off run is back to 267.1 M.

| Stage | Ir | Instructions / sample while on |
|---|---:|---:|
| Everything off | 267,117,879 | (713 over the whole window) |
| GROWL 100 | 489,386,808 | 741 |
| **ALLEY (mix 60)** | 359,979,965 | **310** (old delay 109) |
| Spring (old plate, mix 60) | 439,947,693 | 576 (566: it shares the loop, now a call) |
| CHEW 100 | 555,234,259 | 961 |
| GROWL + ALLEY + reverb | 755,078,708 | 1,627 |
| **All four** | 1,043,252,469 | **2,588** (2,784 over the whole window, the voices included) |

Where ALLEY's 310 go (callgrind, line by line): the four tanh reads (two line writes, two loop limits) ~86, the two
line reads and writes ~80, the two BBD filters (2-pole SVF + 1-pole each) ~57, TONE, the high-passes, PINGPONG and the
mix ~60. A branch-free tanh read instead of `softclip` took it from 329 to 310.

Device build: image 103,384 -> **107,920 B** (+4,536: code and 1 KB of tables), RAM 32,208 -> **32,304 B** (+96), pool
**275,868 B unchanged** (the two 743 ms lines are the old delay's).

ALLEY's own levers if the device needs them (estimates): the right line's write without its tanh (~-22; the
ping-pong's right-hand repeats lose one stage of grit), the 2-pole + 1-pole as a single 2-pole (~-30; a softer knee,
repeats a little muddier). Before those, `REV_DIV 2` and GROWL in mono, as above.

## The Psych Chain, stage 3: DRAIN (the spring) re-voices the plate (2026-11-03, branch `claude/psych-spring`)

The same scripts (`tests/tape/perf_*.txt`; `perf_rev` is DRAIN at 60 on the patch's SIZE 80 / DAMP 60 / PRE 20). The
"everything off" run is **6.8 M Ir cheaper** now: `fx_process` returns at once (only the clip) when the delay and the
spring both rest. That moves the baseline under every "while on" number, so the absolute counts are the fair comparison:

| script | before (step 0) | after | Δ / sample (over 299,880 frames) |
|---|---:|---:|---:|
| everything off | 267,117,879 | 260,322,688 | −22.7 |
| GROWL 100 | 489,386,808 | 483,583,130 | −19.4 |
| ALLEY (mix 60) | 359,979,965 | 364,082,030 | +13.7 |
| reverb → **DRAIN** (mix 60) | 439,947,693 | 442,583,745 | +8.8 (the plate's overflow clamp +11.0; the spring −2.2 against the clamped plate) |
| CHEW 100 | 555,234,259 | 549,951,676 | −17.6 |
| **all four** | 1,043,252,469 | **1,054,083,499** | **+36.1** (2,812 a sample over the whole window, voices included; was 2,784) |

**Per stage, against the new off run:** GROWL 745, ALLEY 346, DRAIN 608, CHEW 966, all four 2,647.

**Where DRAIN's goes** (callgrind line by line, `perf_rev`, per sample):
- the saturation of ~21 int16 nodes (every tank write and allpass node), `sat16`, **~119**;
- the three chirp chains' arithmetic (12 allpasses written out), **~120**;
- the four diffusers and the two swaying allpasses (their reads, interpolation, products), **~110**;
- the 10 output taps ~24, the tank's decay / damping / band filters / glides and the pre-delay, the rest.

The lines' bookkeeping is small now: masked power-of-two lines with one shared write index, where the plate's
compare-and-wrap lines cost ~90 more. The chirp's sat16 is what keeps its node provably in range. If the device needs
cycles, the next lever after `REV_DIV 2` is dropping the input chirp chain (about −60, a less drippy first arrival).

**Device build:** pool 275,868 → **206,592 B** (the spring's lines 13,824 B, the plate's were 83,098), RAM +64 B
(32,368), image +1,796 B (109,716).

**Lever if the device needs it:** `REV_DIV 2`, the spring at half rate, still builds and keeps its decay times
(`listen/spring/README.md`).
