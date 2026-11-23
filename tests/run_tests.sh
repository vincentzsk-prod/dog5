#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-only
# DØG-5's host tests (no hardware). Run from the repo root after a plain FM-1 build, which must be the LAST build
# (the tests read build/dog5.fwsc and the FM-1 intermediates; `./build.sh --release X.Y` writes only dog5-X.Y.fwsc):
#   sh build.sh
#   sh tests/run_tests.sh
# Covers: the FM-1 app on the host (tests/run_host.sh + the scripts below), the program store, the update path (ota.c,
# the loader, tools/fm1_install.py), the browser player (docs/play) and the installer page (docs/install).
set -e
export AC79_SDK="${AC79_SDK:-$HOME/fw-AC79_AIoT_SDK}"   # (fm1pkg_make.py: the SDK files of a package)
cd "$(dirname "$0")/.."
OUT=build/host
mkdir -p "$OUT"
CC="${CC:-cc} -O1 -Wall -Wno-unused-function"
fail=0
run() { echo "== $1"; shift; "$@" || fail=1; }

[ -f build/dog5.fwsc ] || { echo "run ./build.sh first"; exit 1; }

run "FM-1 app on the host: the default script plays, screens and sound" sh tests/run_host.sh
# page families remember their last page: "T expect page N" lines in the script fail the run (exit 1) on a miss
run "FM-1 page families: EDIT to FILTER, HOME, EDIT returns to FILTER" sh tests/run_host.sh tests/families.txt
# HOLD HOME = the control map; a tap still goes HOME; the map draw yields to the notes (app_idle, the DRAW RULE)
run "FM-1 hold-HOME control map: held stays on the page, a tap goes HOME, the map follows the page, draws call app_idle" sh tests/run_host.sh tests/map.txt
# P_POLY_N (VOICE +): the POLY/DUAL voice window 1-8; "T expect voices N" counts gated cards (exit 1 on a miss)
run "FM-1 polyphony P_POLY_N: default 5, then 8 and 1, gated-voice counts under a 10-note cluster" sh tests/run_host.sh tests/poly.txt
# GROWL (obv_drive.h): KNOB 1 on DRIVE, SELECT held = DRIVE + (BIAS, TONE), the FX-held layer; "T expect param P V"
run "FM-1 DRIVE page: GROWL on KNOB 1, SELECT held turns it to BIAS / TONE, nowhere else; FX held reaches GROWL" sh tests/run_host.sh tests/drive_page.txt
# CHEW (obv_tape.h): KNOB 1 on TAPE, SELECT held = TAPE + (WOW/FLT, HISS, DROPS); the map; DRIVE + unchanged
run "FM-1 TAPE page: CHEW on KNOB 1, SELECT held turns it to WOW/FLT / HISS / DROPS, the map names them" sh tests/run_host.sh tests/tape_page.txt
# ALLEY (obv_fx.h): KNOB 1 leaves SYNC from the time sounding, SELECT held = BBD + (SYNC, FINE, PINGPONG), SYNC turned =
# SYNC again, (REC's tap tempo went in Batch 9B), FX held's 4th knob, CC 87
# the FX-held layer: KNOB 1-4 = GROWL ALLEY DRAIN CHEW on any page (ALLEY leaves SYNC from the time sounding), nothing else
run "FM-1 FX-held layer: GROWL / ALLEY / DRAIN / CHEW on KNOB 1-4, the BBD's MIX off it, the page's knobs back on release" sh tests/run_host.sh tests/fx_layer.txt
# DRAIN (obv_fx.h, the spring): KNOB 1 on SPRING, SELECT held = SPRING + (SIZE, DAMP, PRE-DLY), the map; TAPE + unchanged
run "FM-1 SPRING page: DRAIN on KNOB 1, SELECT held turns it to SIZE / DAMP / PRE-DLY, the map names them" sh tests/run_host.sh tests/spring_page.txt
# the reverb's overflow can't come back, the whole chain at its extremes is clean under the sanitizer, no crack
run "DRAIN: the sanitizer on the hot-input scripts, the chain's extremes and the bench's worst signals" sh tests/spring/regress.sh
run "FM-1 BBD DELAY page: ALLEY from SYNC, BBD +, REC no longer taps (it is HOLD), the FX layer's ALLEY, CC 87 = SYNC" sh tests/run_host.sh tests/bbd_page.txt
# Batch 9B, the control surface: EDIT held + a black key = a page jump (never a note), SELECT = LFO RATE on HOME only, REC = HOLD
run "FM-1 EDIT held + keys: OP1-OP6 PIT GLO jump (toggles on OP4 / GLO), MONO / POLY set the mode, no notes, no stuck notes, the tap acts on release" sh tests/run_host.sh tests/controls/edit_keys.txt
run "FM-1 SELECT dial: LFO RATE on HOME (2 a detent, clamped), nothing on other pages or with a layer held, the dice and the + knobs intact" sh tests/run_host.sh tests/controls/select_dial.txt
run "FM-1 REC = HOLD: one latch with the ARP button, ORed with the pedal, released by STOP only" sh tests/run_host.sh tests/controls/rec_hold.txt
run "FM-1 write-lock: THE POUND (1-32) reads the factory, SAVE goes to THE PACK (33-99) only, PRESETS while armed stays in 33-99" sh tests/run_host.sh tests/controls/write_lock.txt
# layer-lock with HOME acting on its release: hold FX + tap HOME locks; the tap never goes HOME; FX / ENV let it go
run "FM-1 boot animation: the whole ~6 s, ending on HOME, which then plays" sh tests/run_host.sh tests/splash.txt
run "FM-1 boot animation: a key pressed during it ends it and sounds at once" sh tests/run_host.sh tests/splash_skip.txt
run "FM-1 HOME knob readout: the value in the top bar for a second" sh tests/run_host.sh tests/home_readout.txt
run "FM-1 HOME beam with SEQ held: it reads the mix after TAPE STOP" sh tests/run_host.sh tests/scene_tapestop.txt
run "FM-1 a saved patch keeps its chapter's scene" sh tests/run_host.sh tests/controls/chapter_save.txt
run "FM-1 the fence (each chapter) and FLEAS (CLEAN, ITCH, SCRATCH, MANGE, back to CLEAN)" sh tests/run_host.sh tests/fleas_fence.txt
run "FM-1 HOME scene: the four chapters, REST / BARK + the beam, MOONSHINE's howl, out to EDIT and back, PACK slots follow the chapters" sh tests/run_host.sh tests/scene.txt
run "FM-1 layer-lock: FX held + HOME tapped locks (no jump HOME), the lock outlives FX's release, FX or ENV ends it" sh tests/run_host.sh tests/layer_lock.txt
# the live tricks (tests/trick): PLAY = STOP, the kill switch ("T expect peak MS MAX": the output's peak over the last MS ms)
run "FM-1 STOP (PLAY): mid note, silent in 5.8 ms, nothing back on PLAY, a new note plays" sh tests/run_host.sh tests/trick/kill_note.txt
run "FM-1 STOP (PLAY): a runaway BBD + the whole chain, cleared: the runaway never comes back" sh tests/run_host.sh tests/trick/kill_runaway.txt
run "FM-1 STOP (PLAY): a 3 s spring tail + CHEW, cleared: no tail, no hiss after PLAY" sh tests/run_host.sh tests/trick/kill_reverb.txt
run "FM-1 TAPE STOP (SEQ held): a chord dives and falls silent, let go it is back at once, nothing left behind" sh tests/run_host.sh tests/trick/tapestop_chord.txt
run "FM-1 TAPE STOP on the whole mix: a spring + BBD tail dives and stops with the rest, back on release" sh tests/run_host.sh tests/trick/tapestop_tail.txt
run "FM-1 SLOP ride (ALGORITHM): on top of VINTAGE on any page, the patch byte untouched, back to 0 adds nothing" sh tests/run_host.sh tests/trick/slop_ride.txt
# the 96-byte / 3-sector / DOG5 program store (the host binary from run_host.sh above):
# 99 distinct patches round-trip byte-exact across a power cycle, one save touches only its sector, an old
# 80-byte "BOVP" sector is rejected. Runnable on its own too: build/host/obervave selftest
run "FM-1 program store: 99 patches round-trip, save isolation, old format rejected, the POUND lock, the power-on rescue of old POUND saves" "$OUT/obervave" selftest

$CC -o "$OUT/ota_test" tests/ota_test.c
run "M-UPGRADE entry (FM-1)" "$OUT/ota_test" build/dog5.fwsc
head -c 60000 build/obervave.bin > "$OUT/old_app.bin"
python3 tools/fm1pkg_make.py "$OUT/old_app.bin" build/loader/ota.bin "$OUT/old.fwsc" >/dev/null
$CC -o "$OUT/ldr_screen_test" tests/ldr_screen_test.c
run "update loader's screen (from Skiff): UPDATE MODE, WRITING and its bar, the error screen" "$OUT/ldr_screen_test" "$OUT"
$CC -o "$OUT/ldr_test" tests/ldr_test.c
run "update loader (FM-1): other app -> this build" "$OUT/ldr_test" "$OUT/old.fwsc" build/dog5.fwsc

NODE=$(command -v node || true)
if [ -n "$NODE" ] && [ -f docs/play/dog5.wasm ]; then
    run "browser player (docs/play, built by web/sim/build.sh): boots, sounds, the screen, speed, storage, the worklet; = the host build" "$NODE" tests/sim_test.mjs
else
    echo "(no node or no docs/play/dog5.wasm: the browser player's test is skipped)"
fi

run "installer (tools/fm1_install.py): FM-1 and SMK-37, install and the update-mode resume check the model" python3 tests/install_test.py
if command -v node >/dev/null 2>&1; then
    run "installer page (docs/install): same frames and sessions as tools/fm1_install.py, no drift" sh tests/install/run.sh
else
    echo "(no node: the installer page's test is skipped)"
fi

if python3 -c "import markdown" 2>/dev/null; then
    run "Driver Manual: Parts 3-4 match the voice cards, the manual page matches its sources" sh -c "python3 tools/make_manual_patches.py --check && python3 tools/make_manual_page.py --check"
else
    echo "(no Python-Markdown: the manual's check is skipped)"
fi

[ "$fail" = 0 ] && echo "ALL TESTS PASSED" || echo "SOME TESTS FAILED"
exit "$fail"
