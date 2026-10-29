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
