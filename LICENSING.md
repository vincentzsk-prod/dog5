# Licensing

**DØG-5 by ZIGGY (DØGS).** DØG-5 is a fork of OberVave, free software under the GNU General Public License,
version 3 only (`GPL-3.0-only`, full text in `LICENSE`). You may use, study, change and share it. If you give
someone a firmware built from it, give them its complete source under the same licence too. The table below is
OberVave's own credits, inherited and kept in full as the GPL requires.

## Who made what

| | |
| --- | --- |
| The platform: `firmware/hal/`, `firmware/loader/`, `crt0.S`, `app.ld`, `firmware/src/` (`usb.c`, `midi_uart.c` (the TRS MIDI IN; its fix from Felucca Salt by ChanceTheMaker, found by keremimo), `ota.c`, `recovery.c`, `lcd.c`, `gfx.c`, `libc.c`, `bootguard.h`, `uac_fir.h`), `tools/` | Copyright (C) 2026 Leo Kuroshita (@kurogedelic), Hügelton Instruments ([Felucca](https://github.com/hugelton/Felucca)), with the changes of [SLOOP](https://github.com/isod89/sloop-fm1) (isod89) |
| The platform's wiring `platform.c`, the host mode `tests/`, the docs, the build (`build.sh`, `tools/build.py`) | zvenson, as [Dinghy](https://github.com/zvenson/dinghy) |
| The update loader's screen: `firmware/loader/ldr_screen.c`, `tests/ldr_screen_test.c` | Copyright (C) 2026 zvenson (the Firmware Hub's look); the idea, a loader that draws, its 5 x 7 letters and the order of things from [Skiff](https://github.com/illuminus5/skiff) by illuminus5, GPL-3.0 |
| The synth: `firmware/src/obervave.c`, `obv_*.h`, `firmware/gen/obv_tables.h` and `tools/gen_tables.py`, the programs, the screen | Copyright (C) 2026 zvenson |
| The SMK-37 work: `firmware/hal/fm1_flash_map.h`, the SMK-37 parts of `tools/fm1pkg_make.py` and `tools/fm1_install.py` (so also of their JavaScript port in `web/install/fm1install.js`), `tests/ota_test.c`, `ldr_test.c`, `install_test.py`. (DØG-5 builds for the FM-1 only: the SMK-37 board layer of the firmware, `firmware/hal/smk_input.h`, `firmware/src/smk_wheel.h` and the SMK parts of the HAL, the loader and `tools/build.py`, was removed in Batch 13; it is in the git history.) | Copyright (C) 2026 M. Geisler (genkigenki/makkuro), from [genkigenki/sloop-fm1](https://github.com/genkigenki/sloop-fm1) branch `smk37` (the reference port of the [fm1-to-smk37](https://github.com/genkigenki/fm1-to-smk37) kit), on the platform above |
| The browser simulator: `web/sim/` (`sim.c`, `worklet.js`, `sim.js`, `index.html`, `sim.css`, `build.sh`), its build in `docs/play/`, `tests/sim_test.mjs` | Copyright (C) 2026 zvenson; the pattern (the firmware's sources in an AudioWorklet, the device's clock run by the audio) follows the web simulators of [Makkuro37](https://github.com/genkigenki/Makkuro37) (M. Geisler) and [winampFM](https://github.com/hericdk/winampFM) (hericdk), both GPL-3.0 |
| The installer page and its tooling: `web/install/`, `docs/install/`, `tools/make_installer_page.py`, `tools/image_diff.py`, `tests/install/`, `firmware/src/dog5_id.h` | DØG-5 by ZIGGY (DØGS). `web/install/fm1install.js` is a JavaScript port of `tools/fm1_install.py` (Copyright (C) 2026 Leo Kuroshita, Hügelton Instruments; SMK-37 parts M. Geisler) and keeps its copyright line |
| DØG-5's own parts: the four scenes, the dog and his poses, the head mark, the favicon and the launch screen (`assets/screen/`, `assets/brand/`; hand-painted by ZIGGY in Pixelorama, some started from a small sampled section of a public-domain still; **no AI-generated art**), the screen code that draws them (`firmware/src/dog5_scene.h`, `dog5_splash.h`, the DØG-5 palette (`dog5_palette.h`, used by `obv_ui.h`)) and their generators (`tools/make_screen_art.py`, `make_splash_art.py`, `make_ldr_art.py`), the Psych Chain, the 32 programs; the documents: the Driver Manual (`dog5-docs/manual/`, the page `docs/manual/` and its generators `tools/make_manual_page.py`, `tools/make_manual_patches.py`), the voice cards and the voicing kit (`dog5-docs/voicing/`), and DØG-5's changes to the web player (the patch list, the voice card, the brand) | Copyright (C) 2026 ZIGGY (DØGS), GPL-3.0-only |
| OberVave on the SMK-37 (`firmware/src/obv_smk.h`, `smk_store.h`, the SMK-37 parts of the app, `SMK37.md`, `smk37-port.yaml` and their tests): removed from DØG-5 in Batch 13, in the git history | Copyright (C) 2026 zvenson |

## Third-party material

| What | Licence | Where |
| --- | --- | --- |
| Terminus font 8x16 (ter-u16n), rendered into `firmware/gen/felucca_font.h` | SIL OFL 1.1 | `assets/fonts/Terminus-LICENSE.txt` |
| Yatra One (Copyright 2014 The Yatra Project Authors), rendered as bitmaps into `firmware/loader/ldr_art.h` (the update screen's wordmark), `firmware/gen/dog5_splash_art.h` (the boot animation's wordmark) and `firmware/gen/dog5_ui_art.h` (the panel header's wordmark); the subset web font `web/brand/YatraOne-Regular.woff2` | SIL OFL 1.1 | `web/brand/OFL-YatraOne.txt` |
| Cormorant Garamond and Space Mono, subset web fonts in `web/brand/` (the installer page, the web player and the Driver Manual page) | SIL OFL 1.1 | `web/brand/OFL-CormorantGaramond.txt`, `web/brand/OFL-SpaceMono.txt` |
| Zig (`zig cc`, MIT) and Binaryen's `wasm-opt` (Asyncify, Apache-2.0) build `docs/play/dog5.wasm`; neither is in this tree | MIT, Apache-2.0 | <https://ziglang.org>, <https://github.com/WebAssembly/binaryen> |
| JieLi AC79 SDK: `uboot.boot`, `cfg_tool.bin`, `eq_cfg_hw.bin` are read from your SDK checkout at build time and placed in the package; no SDK files are in this tree | Apache-2.0 | <https://gitee.com/Jieli-Tech/fw-AC79_AIoT_SDK> |

## Trademarks

"Felucca" and "Hügelton Instruments" are names of Hügelton Instruments; "M-VAVE", "FM-1", "SMK-37", "MKE-P37" and
"Starrykey" belong to their owners. OberVave is inspired by the classic 8-voice poly synths of 1979-84; "Oberheim", "OB-X" and "OB-8" are
trademarks of their owner. OberVave is not made or endorsed by any of them, and none of these marks appear in the
firmware itself.

The instruments and pedals named in the Driver Manual and the voice cards ("gear inspirations": Korg, Roland, Moog,
Sequential, Oberheim, Yamaha and others) are named as inspirations only. Their names are trademarks of their owners;
nothing is modelled, sampled or copied from them, none of them appears in a patch name or on the screen, and DØG-5 is not
affiliated with or endorsed by any of them.
