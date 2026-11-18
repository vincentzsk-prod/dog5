# Batch 14 — small clean-ups (18 Nov 2026)

Branch `build/batch-14-small-cleanups`, off `origin/main` b2e8138 (after Batch 13). **No firmware change:** nothing under
`firmware/` moved, so the device image and its sound are Batch 13's.

## What changed

1. **Card 28 (Arr 2 Dee 2):** dropped the clause "and the echo's band-limit darkens each repeat" — never measured on this
   patch, so it broke the card rule (only measured claims).
2. **The tap-tempo test is gone.** `tests/bbd/tap_bass.txt` measured REC's tap tempo, which left in Batch 9B (REC is HOLD), so
   it measured nothing. `tests/bbd/make_scripts.py` no longer writes it, `make_kit.py` no longer renders it,
   `listen/bbd/README.md` marks its old render as history. Regenerating the other BBD scripts changed nothing.
3. **Installer page:** a dry run now says it is done ("Dry run done: N frames built, nothing sent") and scrolls to the details;
   the package's SHA-256 wraps on a narrow screen instead of running off it (`dd.mono { word-break: break-all }`).
   `docs/install/index.html` regenerated from the template; the v0.2 package in it is byte-identical; `--check` in sync;
   `tests/install/run.sh` 20/20.
4. **Web player, MIDI-channel trap fixed.** A click in the patch list sent its program change on channel 1, so with a MIDI
   channel set on GLOBAL the click did nothing. It now goes through a new export, `sim_pick(p)` (`web/sim/sim.c`), which sends
   the program change on the channel set (`MIDI_OUT_CH`; OMNI = channel 1). `worklet.js` takes a `pick` message; `sim.js`
   sends it. `tests/sim_test.mjs` proves it: channel 5 set, a click loads the patch, a channel-1 program change is ignored,
   back to OMNI, a click loads again.
5. **Web player on phones and tablets.** At 980 px and narrower, `sim.js` moves the patch list inside the device, directly
   above the keys, as its own scrolling box (38 % of the screen height), so a patch is picked and played without scrolling
   between them. Wider, the list sits beside or under the device as before (the move follows a window resize). The patch
   buttons there take touch scrolling (the device's own buttons still take no gestures). Checked in headless Chromium at
   390, 820 and 1400 px wide: no script errors, all 32 patches listed.

## Proofs

- `sh web/sim/build.sh` → `docs/play/dog5.wasm` 96,344 B; `node tests/sim_test.mjs` passes, sound and screens still identical
  to the host build sample for sample.
- `sh build.sh` then `sh tests/run_tests.sh`: ALL TESTS PASSED.
- `python3 tools/make_installer_page.py --check`: in sync. `sh tests/install/run.sh`: 20/20.

## Still open (not this batch)

A/B write-lock (THE POUND 1–32 / THE PACK 33–99); the 0.3 test build (MIDI panic releases HOLD) and its on-unit check.
