# Batch 13 — the firmware clean-up (executed)

Branch `build/batch-13-firmware-cleanup`, off `origin/main` at `294301f` (Merge PR #28, Batch 12B). Run directly by Claude
in the planning chat with the repo attached. Three commits, each proved on its own.

## 1. Dead code — device packages byte-identical

Removed: the **43 OberVave base patch arrays** no slot used (`obv_patches.h` 366 → 248 lines; each array was referenced
nowhere else, checked per name), with the two comments that described only them; the three `P_CHO_*` aliases (used only by
those arrays); the never-written palette block in `gfx.c` (`palette_t`, `PALETTES`, `pal[]` and its five colour macros: `pal`
was never assigned and the macros were never used); the unused `palette_set`, `cv_blit_from`, `fmt_note`; the always-0
`SMK_PAD_HELD`. Stale comments fixed: the `obervave.c` header ("REC taps ALLEY's time", "plate reverb"), the factory table's
"nearest base patch" note, `midi_uart.c`'s references to SLOOP's `seq.c` (in DØG-5 `midi_get` ignores the cable, so the TRS jack
is treated as USB).

**Proof:** `dog5-0.2.fwsc` **`b2be33a9…6b96`** and `dog5.fwsc` `8f0e4a49…749f`, both unchanged; image 82,352 B unchanged;
`tests/drive/bitexact.sh origin/main` byte-identical.

Kept on purpose: `draw_text_box` (the device's recovery screen uses it); `blob_load` / `blob_save` and the sequencer's
8-sector pattern reservation at `0xF4000` (inside `FL_RANGE_OK` and the wipe loop: changing which flash the device may erase
needs its own flash-map review, as 12A advised; the browser player's store also counts those 8 blobs).

## 2. The SMK-37 board — FM-1 packages byte-identical

`unifdef -DBOARD_SMK37=0` over the firmware and the host tests (no hand-edited `#if` logic); deleted `obv_smk.h`,
`smk_store.h`, `smk_wheel.h`, `hal/smk_input.h`, `SMK37.md`, `smk37-port.yaml`, `tests/smk/`, `tests/smk_*`; comments that named
the SMK hand-fixed (`fm1_cc.h`, `fm1_flash_map.h`, `fm1_lcd_hw.h`, `fm1_flash.h`, `ota.c`, the loader, `dog5_id.h` loses
`DOG5_ID_SMK`, `platform.c`'s `FELUCCA_UART` is now plainly 1). `tools/build.py` is FM-1 only and **refuses `BOARD=smk37`** with
a message; `build.sh`, `run_host.sh`, `perf_callgrind.sh`, `run_tests.sh` lost their SMK lines; `ldr_test.c` lost the
protected-range check that was a constant "ok" on the FM-1; `tests/host.c` lost the SMK-only script commands (`vel`, `pad`,
`fader`, `wheel`, `xkey`, `dump`, `check`; no script used them) and its event field is renamed `kind` (it carries every
script event). `fmt_s` became unused and went.

**Kept:** the installer tools (`tools/fm1_install.py`, `tools/fm1pkg_make.py`, `web/install/fm1install.js`) and their tests:
the install protocol's SMK-37 support is Felucca's and M. Geisler's, and changing it would change the published installer page.
`LICENSING.md` keeps M. Geisler's credit for what remains and notes what left; zvenson's "OberVave on the SMK-37" row now says it
was removed (git history).

**Proof:** both FM-1 packages unchanged (the update loader included); `docs/play/dog5.wasm` rebuilt byte-identical; host audio
byte-identical; `run_tests.sh` ALL TESTS PASSED. Passing lines 484 → 384: every removed line belongs to an SMK section (the SMK
host app, mapping, store, flash map, wheel, package layout, three SMK update-entry variants and the SMK loader run); the FM-1's
own update tests all still run.

## 3. A MIDI panic releases HOLD — the one behaviour change

Before: CC 123 (all notes off) or CC 120 (all sound off) silenced the voices but left HOLD latched, so the next notes latched
again and REC stayed lit. Now a panic lets HOLD go first, exactly as STOP does (`obervave.c`, the CC handler). A patch change and
the pedal still do not.

**Proof:** `tests/controls/rec_hold.txt` gained both cases; on the old code the new lines FAIL (the next note stays latched), with
the fix 24 of 24 expectations pass. Audio otherwise unchanged: `bitexact.sh origin/main` byte-identical, and
`tests/voicing/identical_par.py` against `main`: **all 32 patch records identical, all 32 patches byte-identical on all 52
phrases**. The device image is **88 B smaller** (82,352 → 82,264): `tools/image_diff.py` shows `midi_in` +6 instructions and
otherwise the unity build's usual ripple (global offsets moved by 4–8 B, `app_main` and `tape_process` re-scheduled; integer
code, same arithmetic); the update loader is identical. `docs/play/dog5.wasm` rebuilt with the fix (`sim_test.mjs` passes, its
sound bit-identical to the host build). `run_tests.sh`: ALL TESTS PASSED, 390 lines.

**Not on the unit yet.** The installer page still carries v0.2 (`FM-1_962`, unchanged). The panic fix and the smaller image ship
with the next version flashed; check then: a panic from a connected keyboard or DAW while HOLD is on lets REC's light go out.
