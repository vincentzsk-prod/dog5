# Batch 7 audit: where the name OberVave / FM-1_95x appears (12 Nov 2026)

Step 0 of the identity batch, written before the changes were made, against `main` at `ea19a61`. The table at the end
lists every hit (file:line in `main`) with a class and whether this batch CHANGED or KEPT it. The class is assigned by
a script (rules: a copyright, credit, fork or upstream mention is ATTRIBUTION; the project's own notes and history in
`CLAUDE.md` and `dog5-docs/` are ATTRIBUTION; anything that names a build output, a package, a test path, a store key or
a file the build or the updater reads is FUNCTIONAL; the rest is IDENTITY), so a few lines may be classed one step
off; the sections below are the hand-checked part.

## What this batch changed

**IDENTITY (shown on the device, or the product's name):**

- `firmware/src/dog5_id.h` (new): the one place for the name (`DOG5_NAME` = `DØG-5`, the panel font's Ø), the package
  identity prefixes (`FM-1_96`, `SMK-37 Pro_96`) and the file stem (`dog5`). `tools/build.py` reads it.
- `firmware/src/platform.c:75-83` `APP_NAME` (the rescue and crash screens), `FELUCCA_ID` default.
- `firmware/src/obv_ui.h` header logo (`OBERVAVE` in FONT_S, top right of every page) -> `DØG-5`; the boot splash (a bitmap of
  the OberVave wordmark) -> the name as text, same 2.4 s timing. `firmware/gen/obv_splash.h` and `tools/make_logo.py` stay in
  the tree, unused (the bitmap needs a font that is not in this environment).
- `firmware/loader/ldr_screen.c` `LDR_NAME` -> `DOG 5` (the loader's own letters have no hyphen and no Ø).
- `tests/host.c` `APP_NAME` default.
- Package names `obervave*.fwsc` -> `dog5*.fwsc` (`tools/build.py`, `.github/workflows/release.yml`, `build.sh` comment, the
  tests that read the package, `SMK37.md`, `README.md`); the SMK-37 identities `SMK-37 Pro_95N` -> `_96N` (so no DØG-5 build
  reports an OberVave identity).
- `README.md`: a DØG-5 front section; the OberVave README stays below it, labelled. `NOTICE` (new), `LICENSING.md` (one row).

**FUNCTIONAL, changed, with the proof that it is safe:**

| Change | Proof |
| --- | --- |
| The loader's screen name (`LDR_NAME`), in the update loader that writes flash | `tools/image_diff.py` on the old and new `loader.elf`/`loader.dis`: **45 of 45 functions identical** after normalising data addresses; the only difference in the loader image is the string (`OBERVAVE` -> `DOG 5`). `tests/ldr_screen_test.c` passes (it checks every letter is in the loader's font); `ldr_test` and `ota_test` pass. |
| The boot splash code (`ui_splash`, inlined in `app_main`) | `image_diff.py` on the app: **250 of 251 functions identical**; `app_main` differs in one contiguous region (the splash drawing; instructions 199-351 of 2753, nothing outside it). `data.bin` and `ramtext.bin` are byte-identical. |
| Package identity bytes (`FM-1_950` -> `FM-1_960`, release 0.1: `FM-1_961`) | The marker bytes (offset 0x2F of each of the first 20 blocks) are the only place the package carries it, and the app's `FELUCCA_ID` string; a dev build and a release build differ in exactly one byte (the last digit). No marker byte equals the reserved `0x7D`. |
| Build and test file names (`obervave*.fwsc` -> `dog5*.fwsc`) | `tests/run_tests.sh` outcome set on the new tree equals `main`'s except the two items listed in the report (three screen comparisons against the old web sim, which already failed on `main`, now with 162 more differing pixels each: the old sim still draws OBERVAVE in the header; not isolated further, and nothing else differs). |

## Left unchanged (identity-like, but functional or not this batch's to decide)

- USB product string **"Felucca"** (`firmware/src/usb.c` `STR2`) and manufacturer "Hügelton Instruments": the Felucca platform's USB
  name, not OberVave's; `tools/fm1_install.py` `PORT_RE` matches it (and `felucca` is how the installer finds the unit), so
  renaming it would change how every installer finds the device. The page and Python find the unit the same way.
- `SMK_DATA_FAMILY = "OBERVAV"` (`tools/build.py`, `platform.c smk_owner_check`): the SMK-37 flash store's owner tag.
  Changing it would make an SMK unit treat OberVave's saved data as foreign.
- Internal build file names `firmware/src/obervave.c`, `build/obervave.bin`, `obervave.elf`, the host binary
  `build/host/obervave`, and every test script that uses them (about forty): not shown to a user; renaming them is churn
  with no effect on the product.
- `docs/sim/` (the browser simulator): a **build of OberVave** (`obervave.wasm`, OberVave logo, a link to the upstream hub
  entry and to `zvenson/obervave`). Rebuilding needs zig + wasm-opt and the artwork, so it waits for the artwork batch.
  Once Pages is on it will be served at `/sim/` as it is.
- `docs/firmware/`: **upstream OberVave packages** (`obervave-1.5.3.fwsc`, SMK-37 betas). Pages will serve them from
  `/firmware/`. Not touched (deleting is outside this batch).
- `assets/logo*`, `docs/screen.png`: OberVave artwork, with the artwork batch.
- `tests/sim_test.mjs` compares the sim's screens with the host build and was already failing on `main`; see the report.
- `tools/fm1_install.py:6` says "web/fm1ota.js". **That file does not exist in this tree** (nor does `web/fm1pkg.js`, which
  `tests/install_test.py` also mentions and skips). The only reference is that docstring; nothing loads it.
- `docs/MAKE-IT-YOURS.md` (Dinghy's): says the web installers resume only loaders named `FM-1_9NN`; in source the resume rule is
  `OWN_LOADER_RE` on the **loader's** identity (`ota-FM-1_9\d\d`), which is fixed at `ota-FM-1_900` whatever the app's identity.

## The identity digits

`FM-1_9XY`: `9` fixed, `X` family, `Y` minor (`tools/build.py`: `BOARD_PREFIX` + the release's minor digit). From source,
nothing in this repository reads the digits for a decision (see `docs/install/README.md`). DØG-5 takes family `6`:
`FM-1_96N`. `FM-1_960` is a dev build, `FM-1_961` the v0.1 test build. The documented families are 900 SLOOP, 91N Felucca,
93N sloopDX, 95N OberVave, 97N zp12, 98N a Doom port, 99N Dinghy (`docs/MAKE-IT-YOURS.md`, `CLAUDE.md`); 92N, 94N and 96N
are not named anywhere in the repository. The hub's list could not be reached from this environment, so 96N is
**unchecked against it**.

## Every hit

399 hits in 84 files (tracked files of main, case-insensitive: obervave | FM-1_95 | fm1ota; listen/ and reference-renders/ excluded)

| class | CHANGED | KEPT |
|---|---|---|
| IDENTITY | 8 | 89 |
| ATTRIBUTION | 3 | 124 |
| FUNCTIONAL | 34 | 141 |


### `.github/workflows/release.yml`

| line | class | status | text |
|---|---|---|---|
| 1 | IDENTITY | CHANGED | `# OberVave: build the packages on GitHub, run the host tests, and on a tag vX.Y publish the release with a bui` |
| 62 | FUNCTIONAL | CHANGED | `ls -l build/obervave-"$V"*.fwsc` |
| 63 | FUNCTIONAL | CHANGED | `(cd build && sha256sum obervave-"$V"*.fwsc > SHA256SUMS)` |
| 67 | FUNCTIONAL | CHANGED | `name: obervave-fwsc` |
| 68 | FUNCTIONAL | CHANGED | `path: build/obervave*.fwsc` |
| 75 | FUNCTIONAL | CHANGED | `subject-path: build/obervave-*.fwsc` |
| 82 | FUNCTIONAL | CHANGED | `build/obervave-*.fwsc` |

### `CLAUDE.md`

| line | class | status | text |
|---|---|---|---|
| 3 | ATTRIBUTION | KEPT | `**This repo is a fork of OberVave, being turned into DØG-5.** This brief is the operating truth for` |
| 4 | ATTRIBUTION | KEPT | `the build. Where it conflicts with anything in the preserved OberVave notes (below the divider) or in` |
| 15 | ATTRIBUTION | KEPT | `Custom firmware for the **M-VAVE FM-1** pocket synth, forked from **OberVave** (an 8-voice analog-style` |
| 52 | ATTRIBUTION | KEPT | `Base:    zvenson/obervave` |
| 55 | ATTRIBUTION | KEPT | `Identity:FM-1_955` |
| 69 | ATTRIBUTION | KEPT | `One line, no effect on the program-sector / flash-write logic. Upstream OberVave 3.x history is recorded in` |
| 87 | ATTRIBUTION | KEPT | `\| Transient message \| `say(s)` → `toast`/`toast_t` (used for the knob-readout popup) \| `obervave.c` \|` |
| 88 | ATTRIBUTION | KEPT | `\| HOME = PERFORM \| already in base (`np = PG_PERFORM`); HOME LED lights on it \| `obervave.c` \|` |
| 89 | ATTRIBUTION | KEPT | `\| Layer-lock \| already in base: hold a layer + tap HOME = lock open; its button releases \| `obervave.c` \|` |
| 179 | ATTRIBUTION | KEPT | `**BBD (ALLEY) — DONE** (`obv_fx.h`, branch `claude/psych-bbd`): OberVave's ping-pong delay re-voiced in place ` |
| 328 | ATTRIBUTION | KEPT | `- `CLAUDE.obervave.md` — the base project's original notes (where things are in the code; still useful).` |
| 351 | ATTRIBUTION | KEPT | `# ↓↓↓ PRESERVED: ORIGINAL OBERVAVE CLAUDE.md (base-project notes — still useful for where code lives) ↓↓↓` |
| 353 | ATTRIBUTION | KEPT | `# OberVave` |
| 357 | ATTRIBUTION | KEPT | `GPL-3.0. Identity `FM-1_95N`. Name by the user ("OberVave": Ober... + M-VAVE).` |
| 368 | ATTRIBUTION | KEPT | `Oberheim Two Voice, so this synth's family), the name stays OberVave, and the show is never named in the produ` |
| 377 | ATTRIBUTION | KEPT | `- `firmware/src/obervave.c`: the app (panel, MIDI, storage, what to draw when). Includes `platform.c` first, t` |
| 437 | ATTRIBUTION | KEPT | `the SMK-37 came in staggered): the keys and MIDI are `keys_in` / `midi_in` (obervave.c); the main loop calls t` |
| 449 | ATTRIBUTION | KEPT | `- Installing on the FM-1: `python3 tools/fm1_install.py build/obervave.fwsc --yes` (USB-MIDI, ~3 min, `--info`` |
| 450 | ATTRIBUTION | KEPT | `shows the identity). Works from SLOOP (FM-1_971) and from OberVave itself.` |
| 452 | ATTRIBUTION | KEPT | `buttons / MIDI / `enc ID N` encoder turns). Film mode (`build/host/obervave OUT script FPS`) writes a frame ev` |
| 454 | ATTRIBUTION | KEPT | `instructions per sample (Linux perf counter): the yardstick is sloopDX's engines at ~1000-1500; OberVave's wor` |
| 462 | ATTRIBUTION | KEPT | `- The video: `video/song.py` (nine OberVaves from the host build, D Phrygian 94 BPM, 40 bars: slow dark disco,` |
| 468 | ATTRIBUTION | KEPT | ``video/obervave-1.2.mp4` (copied with thumb + YOUTUBE.md to ~/youtube/fm1-hub/). The renders are git-ignored.` |
| 469 | ATTRIBUTION | KEPT | `The kick and the hats are programmed on OberVave's own step sequencer by key presses (`Part.program_steps`),` |
| 476 | ATTRIBUTION | KEPT | `- `tools/build.py`: `./build.sh [--release X.Y]` -> `build/obervave[-X.Y].fwsc`, identity FM-1_95Y.` |
| 478 | ATTRIBUTION | KEPT | `- Workspace file: `../obervave.code-workspace` (opened in VSCodium Insiders, flatpak).` |
| 482 | ATTRIBUTION | KEPT | `Released: **1.5.3** (2026-10-19, FM-1_955, tag v1.5.3: the update loader's screen, `firmware/loader/ldr_screen` |
| 485 | ATTRIBUTION | KEPT | `SMK-37 1.5.2-beta) after **1.5** (2026-10-16, FM-1_955, tag v1.5: 99 programs, 64 factory (33-64 new), 65-99 I` |
| 487 | ATTRIBUTION | KEPT | `Before: **1.3.1** (FM-1_953, tag v1.3.1: the tracks coloured, A blue / B orange) after **1.3** (tag v1.3: the ` |
| 489 | ATTRIBUTION | KEPT | `Before: 1.2.1 (FM-1_952; 1.2 replaced: a held function button's knobs` |
| 498 | ATTRIBUTION | KEPT | `on the device**: updates from the running OberVave fail (the FM-1 stops answering after the first read request` |
| 506 | ATTRIBUTION | KEPT | `17:42, the first minute of OberVave on the device (keys send MIDI out too). Not the CPU load (idle, effects of` |
| 510 | ATTRIBUTION | KEPT | `0.5 ms from TIMER5, also nested in the audio ISR) send fine; OberVave/Dinghy's platform defers usb_poll while` |
| 512 | ATTRIBUTION | KEPT | `on OberVave's platform babbled; **the difference was -O2** (OberVave's APP_CFLAGS, the unity build puts usb.c ` |
| 526 | ATTRIBUTION | KEPT | `(112 KB image, 21 KB RAM, 274 KB pool) was **installed on the user's FM-1** (it came up as FM-1_950, the insta` |
| 594 | ATTRIBUTION | KEPT | `rects), "OBERVAVE" in FONT_L with three blue bands through the lower half of the letters, section titles betwe` |
| 606 | ATTRIBUTION | KEPT | `On GitHub: <https://github.com/zvenson/obervave> (public, since 2026-10-13). Push after each tested step.` |

### `LICENSING.md`

| line | class | status | text |
|---|---|---|---|
| 3 | ATTRIBUTION | KEPT | `**DØG-5 by ZIGGY (DØGS).** DØG-5 is a fork of OberVave, free software under the GNU General Public License,` |
| 6 | ATTRIBUTION | KEPT | `OberVave's own credits, inherited and kept in full as the GPL requires.` |
| 15 | ATTRIBUTION | KEPT | `\| The synth: `firmware/src/obervave.c`, `obv_*.h`, `firmware/gen/obv_tables.h` and `tools/gen_tables.py`, the ` |
| 18 | ATTRIBUTION | KEPT | `\| OberVave on the SMK-37: `firmware/src/obv_smk.h`, `smk_store.h`, the SMK-37 parts of `platform.c`, `obervave` |
| 26 | ATTRIBUTION | KEPT | `\| Zig (`zig cc`, MIT) and Binaryen's `wasm-opt` (Asyncify, Apache-2.0) build `docs/sim/obervave.wasm`; neither` |
| 32 | ATTRIBUTION | KEPT | `"Starrykey" belong to their owners. OberVave is inspired by the classic 8-voice poly synths of 1979-84; "Oberh` |
| 33 | ATTRIBUTION | KEPT | `trademarks of their owner. OberVave is not made or endorsed by any of them, and none of these marks appear in ` |

### `README.md`

| line | class | status | text |
|---|---|---|---|
| 1 | IDENTITY | KEPT | `<p align="center"><img src="assets/logo.png" width="800" alt="OberVave: the name in red glowing outlines, thre` |
| 3 | IDENTITY | KEPT | `# OberVave` |
| 7 | IDENTITY | KEPT | `OberVave turns the FM-1 into a single, deep instrument in the spirit of the classic American 8-voice poly synt` |
| 12 | IDENTITY | KEPT | `<p align="center"><img src="docs/screen.png" width="240" alt="OberVave's screen: program 01 DARK ARP, the ARP ` |
| 15 | FUNCTIONAL | KEPT | `> `tools/fm1_install.py docs/firmware/obervave-1.5.3.fwsc` (identity `FM-1_955`). 1.5.3: the update loader sho` |
| 18 | IDENTITY | KEPT | `> jack: a keyboard, a drum machine or a sequencer through a TRS-to-DIN adapter plays OberVave (notes, CC, prog` |
| 43 | IDENTITY | KEPT | `Hear it: [the video](video/) is nine OberVaves (the host build) playing one slow, dark track; every sound in i` |
| 58 | IDENTITY | KEPT | `\| **Sequencer** \| Two tracks that share 256 steps (one track can have them all, or A and B split them). A step` |
| 139 | ATTRIBUTION | KEPT | `OberVave is built on [Dinghy](https://github.com/zvenson/dinghy), whose platform (boot, USB, updates, audio, s` |
| 144 | FUNCTIONAL | KEPT | `tests/run_host.sh                 # the synth on your computer: build/host/obervave.wav and screens as PNG` |
| 147 | FUNCTIONAL | CHANGED | `./build.sh                        # the device package: build/obervave.fwsc` |
| 148 | FUNCTIONAL | CHANGED | `python3 tools/fm1_install.py build/obervave.fwsc   # onto the FM-1 over USB` |
| 159 | IDENTITY | KEPT | `GPL-3.0-only, see `LICENSE` and `LICENSING.md` for who made what. OberVave stands on` |
| 165 | IDENTITY | KEPT | `OberVave is inspired by the classic 8-voice poly synths of 1979-84 (Oberheim's OB-X and OB-8 era). Those names` |
| 166 | IDENTITY | KEPT | `trademarks of their owners; OberVave is not made by or affiliated with them, and none of the marks appear in t` |

### `SMK37.md`

| line | class | status | text |
|---|---|---|---|
| 1 | IDENTITY | KEPT | `# OberVave on the M-Vave SMK-37` |
| 3 | IDENTITY | KEPT | `OberVave also runs on the **M-Vave SMK-37** keyboards: the SMK-37 Pro, the SMK-37 Elite and the MKE-P37 (and t` |
| 13 | FUNCTIONAL | KEPT | `\| SMK-37 Pro, Starrykey 37 Play \| `obervave-<version>-smk37.fwsc` \| `SMK-37 Pro_95N` \|` |
| 14 | FUNCTIONAL | KEPT | `\| SMK-37 Elite \| `obervave-<version>-smk37-elite.fwsc` \| `SMK-37 Elite_95N` \|` |
| 15 | FUNCTIONAL | KEPT | `\| MKE-P37 \| `obervave-<version>-smk37-mke.fwsc` \| `MKE-P37_95N` \|` |
| 17 | FUNCTIONAL | KEPT | `N is the minor version, as on the FM-1 (`FM-1_95N`). Each package reports its own model's name, so M-Vave's ow` |
| 24 | IDENTITY | KEPT | `pad and wheel calibration (`0xC1000`), the Bluetooth pairing, the chip's key data. OberVave never writes there` |
| 32 | IDENTITY | KEPT | `2. On the first start OberVave clears the stock firmware's settings area it uses (10 sectors from `0x9D000`; t` |
| 37 | ATTRIBUTION | KEPT | `With the SMK-37 connected over USB (it shows up as a USB-MIDI device; under OberVave its name is "Felucca"):` |
| 40 | FUNCTIONAL | KEPT | `python3 tools/fm1_install.py obervave-<version>-smk37.fwsc        # SMK-37 Pro (the Elite / MKE-P37: their pac` |
| 45 | IDENTITY | KEPT | `loader, writes the app and restarts into OberVave (about 3 minutes).` |
| 47 | IDENTITY | KEPT | `**USB rescue:** hold **OCTAVE-** while you switch the keyboard on: OberVave starts without sound, only the upd` |
| 55 | IDENTITY | KEPT | `Everything from the FM-1 keeps its job, on the SMK button with the same meaning; OberVave's manual (README.md,` |
| 58 | IDENTITY | KEPT | `\| SMK-37 \| OberVave (FM-1 name) \| \|` |
| 124 | IDENTITY | KEPT | `- No TRS MIDI IN (OberVave has none on the FM-1 either). USB-MIDI in and out, clock, start and stop work.` |
| 130 | FUNCTIONAL | CHANGED | `BOARD=smk37 ./build.sh                    # SMK-37 Pro:   build/obervave-smk37.fwsc        (SMK-37 Pro_950)` |
| 131 | FUNCTIONAL | CHANGED | `BOARD=smk37 MODEL=elite ./build.sh        # SMK-37 Elite: build/obervave-smk37-elite.fwsc  (SMK-37 Elite_950)` |
| 132 | FUNCTIONAL | CHANGED | `BOARD=smk37 MODEL=mke ./build.sh          # MKE-P37:      build/obervave-smk37-mke.fwsc    (MKE-P37_950)` |
| 133 | FUNCTIONAL | CHANGED | `BOARD=smk37 ./build.sh --release 1.3-beta # a release:    build/obervave-1.3-beta-smk37.fwsc (SMK-37 Pro_953)` |
| 150 | IDENTITY | KEPT | `OberVave is not made or endorsed by them.` |

### `build.sh`

| line | class | status | text |
|---|---|---|---|
| 4 | IDENTITY | CHANGED | `# Build OberVave (see README.md).` |
| 6 | FUNCTIONAL | CHANGED | `#   BOARD            target board: fm1 (default) or smk37 (M-Vave SMK-37 -> build/obervave-smk37.fwsc, SMK37.m` |

### `docs/firmware/smk37/SHA256SUMS`

| line | class | status | text |
|---|---|---|---|
| 1 | FUNCTIONAL | KEPT | `d00c5a20147e2ef34a332c7c9d8af09feb54268478ee417da9bf76fe2b209fbf  obervave-1.5.2-beta-smk37-elite.fwsc` |
| 2 | FUNCTIONAL | KEPT | `51f7f7fb700741642665be75dda3cb439b265e316aa7a136428457feae8f09eb  obervave-1.5.2-beta-smk37.fwsc` |
| 3 | FUNCTIONAL | KEPT | `a8444da7d9bbf5b90914d9305e69d50c0b5a71d52e7fc103debd48aa78afda63  obervave-1.5.2-beta-smk37-mke.fwsc` |

### `docs/sim/index.html`

| line | class | status | text |
|---|---|---|---|
| 7 | IDENTITY | KEPT | `<title>OberVave Simulator</title>` |
| 8 | IDENTITY | KEPT | `<meta name="description" content="OberVave, an 8-voice analog-style polysynth firmware for the FM-1, running i` |
| 14 | IDENTITY | KEPT | `<img class="logo" src="logo.png" alt="OberVave">` |
| 18 | IDENTITY | KEPT | `<a class="cta" href="https://thefirmwarehub.com/#fw-obervave">Install on your FM-1 &rarr;</a>` |
| 19 | ATTRIBUTION | KEPT | `<a href="https://github.com/zvenson/obervave">Source code</a>` |
| 124 | ATTRIBUTION | KEPT | `<p>OberVave by <a href="https://github.com/zvenson">zvenson</a>, built on` |

### `docs/sim/sim.css`

| line | class | status | text |
|---|---|---|---|
| 2 | IDENTITY | KEPT | `/* OberVave simulator: thefirmwarehub.com's warm dark, OberVave's red and blue (assets/logo) */` |

### `docs/sim/sim.js`

| line | class | status | text |
|---|---|---|---|
| 2 | IDENTITY | KEPT | `// OberVave simulator, the page: builds the panel (27 keys, 14 buttons, 7 encoders + MASTER), starts the Audio` |
| 3 | FUNCTIONAL | KEPT | `// (worklet.js runs obervave.wasm, the firmware), draws its 240 x 240 screen and LEDs, and feeds it the mouse,` |
| 14 | FUNCTIONAL | KEPT | `const STORE_KEY = 'obervave-sim-store-1', MASTER_KEY = 'obervave-sim-master';` |
| 20 | IDENTITY | KEPT | `const ev = (a) => { try { if (window._paq) window._paq.push(['trackEvent', 'Play', 'OberVave: ' + a]); } catch` |
| 64 | FUNCTIONAL | KEPT | `const [wasm] = await Promise.all([fetch('obervave.wasm').then((r) => { if (!r.ok) throw new Error('obervave.wa` |
| 66 | FUNCTIONAL | KEPT | `S.node = new AudioWorkletNode(S.ctx, 'obervave', { numberOfInputs: 0, outputChannelCount: [2], processorOption` |

### `docs/sim/worklet.js`

| line | class | status | text |
|---|---|---|---|
| 2 | FUNCTIONAL | KEPT | `// OberVave in an AudioWorklet: obervave.wasm is the firmware (firmware/src, unchanged) on a simulated FM-1` |
| 7 | IDENTITY | KEPT | `class OberVave extends AudioWorkletProcessor {` |
| 79 | FUNCTIONAL | KEPT | `registerProcessor('obervave', OberVave);` |

### `dog5-docs/CLAUDE.obervave.md`

| line | class | status | text |
|---|---|---|---|
| 1 | ATTRIBUTION | KEPT | `# OberVave` |
| 5 | ATTRIBUTION | KEPT | `GPL-3.0. Identity `FM-1_95N`. Name by the user ("OberVave": Ober... + M-VAVE).` |
| 16 | ATTRIBUTION | KEPT | `Oberheim Two Voice, so this synth's family), the name stays OberVave, and the show is never named in the produ` |
| 25 | ATTRIBUTION | KEPT | `- `firmware/src/obervave.c`: the app (panel, MIDI, storage, what to draw when). Includes `platform.c` first, t` |
| 85 | ATTRIBUTION | KEPT | `the SMK-37 came in staggered): the keys and MIDI are `keys_in` / `midi_in` (obervave.c); the main loop calls t` |
| 97 | ATTRIBUTION | KEPT | `- Installing on the FM-1: `python3 tools/fm1_install.py build/obervave.fwsc --yes` (USB-MIDI, ~3 min, `--info`` |
| 98 | ATTRIBUTION | KEPT | `shows the identity). Works from SLOOP (FM-1_971) and from OberVave itself.` |
| 100 | ATTRIBUTION | KEPT | `buttons / MIDI / `enc ID N` encoder turns). Film mode (`build/host/obervave OUT script FPS`) writes a frame ev` |
| 102 | ATTRIBUTION | KEPT | `instructions per sample (Linux perf counter): the yardstick is sloopDX's engines at ~1000-1500; OberVave's wor` |
| 110 | ATTRIBUTION | KEPT | `- The video: `video/song.py` (nine OberVaves from the host build, D Phrygian 94 BPM, 40 bars: slow dark disco,` |
| 116 | ATTRIBUTION | KEPT | ``video/obervave-1.2.mp4` (copied with thumb + YOUTUBE.md to ~/youtube/fm1-hub/). The renders are git-ignored.` |
| 117 | ATTRIBUTION | KEPT | `The kick and the hats are programmed on OberVave's own step sequencer by key presses (`Part.program_steps`),` |
| 124 | ATTRIBUTION | KEPT | `- `tools/build.py`: `./build.sh [--release X.Y]` -> `build/obervave[-X.Y].fwsc`, identity FM-1_95Y.` |
| 126 | ATTRIBUTION | KEPT | `- Workspace file: `../obervave.code-workspace` (opened in VSCodium Insiders, flatpak).` |
| 130 | ATTRIBUTION | KEPT | `Released: **1.5.3** (2026-10-19, FM-1_955, tag v1.5.3: the update loader's screen, `firmware/loader/ldr_screen` |
| 133 | ATTRIBUTION | KEPT | `SMK-37 1.5.2-beta) after **1.5** (2026-10-16, FM-1_955, tag v1.5: 99 programs, 64 factory (33-64 new), 65-99 I` |
| 135 | ATTRIBUTION | KEPT | `Before: **1.3.1** (FM-1_953, tag v1.3.1: the tracks coloured, A blue / B orange) after **1.3** (tag v1.3: the ` |
| 137 | ATTRIBUTION | KEPT | `Before: 1.2.1 (FM-1_952; 1.2 replaced: a held function button's knobs` |
| 146 | ATTRIBUTION | KEPT | `on the device**: updates from the running OberVave fail (the FM-1 stops answering after the first read request` |
| 154 | ATTRIBUTION | KEPT | `17:42, the first minute of OberVave on the device (keys send MIDI out too). Not the CPU load (idle, effects of` |
| 158 | ATTRIBUTION | KEPT | `0.5 ms from TIMER5, also nested in the audio ISR) send fine; OberVave/Dinghy's platform defers usb_poll while` |
| 160 | ATTRIBUTION | KEPT | `on OberVave's platform babbled; **the difference was -O2** (OberVave's APP_CFLAGS, the unity build puts usb.c ` |
| 174 | ATTRIBUTION | KEPT | `(112 KB image, 21 KB RAM, 274 KB pool) was **installed on the user's FM-1** (it came up as FM-1_950, the insta` |
| 242 | ATTRIBUTION | KEPT | `rects), "OBERVAVE" in FONT_L with three blue bands through the lower half of the letters, section titles betwe` |
| 254 | ATTRIBUTION | KEPT | `On GitHub: <https://github.com/zvenson/obervave> (public, since 2026-10-13). Push after each tested step.` |

### `dog5-docs/DOG-5-base-and-ui-decisions.md`

| line | class | status | text |
|---|---|---|---|
| 17 | ATTRIBUTION | KEPT | `\| 1 \| **Base locked: OberVave `v1.5.3`, commit `7e1ccf9ca9e96a14a961e48ea8fe6efa907422df`** \| LOCKED \|` |
| 42 | ATTRIBUTION | KEPT | `Project:  zvenson/obervave` |
| 47 | ATTRIBUTION | KEPT | `Identity: FM-1_955` |
| 87 | ATTRIBUTION | KEPT | `# 1. Fork zvenson/obervave on GitHub (web UI) → github.com/<you>/dog-5` |
| 94 | ATTRIBUTION | KEPT | `git tag base/obervave-v1.5.3 7e1ccf9ca9e96a14a961e48ea8fe6efa907422df` |
| 98 | ATTRIBUTION | KEPT | `git remote add upstream https://github.com/zvenson/obervave.git` |
| 138 | ATTRIBUTION | KEPT | `\| Transient message \| `say(s)` → `toast` + `toast_t` timestamp \| `obervave.c:133` \|` |
| 216 | ATTRIBUTION | KEPT | `**HOME is PERFORM.** Confirmed in source (`obervave.c:1592–1595`): `else np = PG_PERFORM;`. The base already` |
| 219 | ATTRIBUTION | KEPT | `(`obervave.c:1795`), so the panel itself tells you where you are without looking at the screen. Keep that.` |
| 302 | ATTRIBUTION | KEPT | `(`obervave.c:1592–1599`). Adopted as decision 9.` |
| 430 | ATTRIBUTION | KEPT | `docs/sim/            the built output, obervave.wasm already committed` |
| 458 | ATTRIBUTION | KEPT | `OberVave has **no** web editor. Felucca, SLOOP, Skiff, Melodee, JIANT and GammaWave all do, so it is the` |

### `dog5-docs/DOG-5-build-kit.md`

| line | class | status | text |
|---|---|---|---|
| 281 | ATTRIBUTION | KEPT | `1. Fork, pin to `7e1ccf9`, tag `base/obervave-v1.5.3`, upstream as fetch-only **[V: the repo]**` |

### `dog5-docs/DOG-5-foundation.md`

| line | class | status | text |
|---|---|---|---|
| 5 | ATTRIBUTION | KEPT | ``DOG-5-base-and-ui-decisions.md` (base is now OberVave v1.5.3, commit 7e1ccf9; 99 slots; 20-page UI). The` |
| 46 | ATTRIBUTION | KEPT | `## 2. THE FORK — OberVave (⚠️ base now pinned at v1.5.3 — see base-and-ui-decisions)` |
| 48 | ATTRIBUTION | KEPT | `Lineage: `Felucca (Kuroshita/Hügelton) → SLOOP (isod89) → Dinghy (zvenson) → OberVave`. OberVave is ~70% of` |
| 66 | ATTRIBUTION | KEPT | `- **⚠️ Build with `-Os`, not `-O2`** (the USB-babble brick trap — see the brief and the preserved OberVave` |
| 111 | ATTRIBUTION | KEPT | `3. **VCF** — 24 dB LP with saturation in the feedback path (OberVave's SVF LP24 + pre-filter drive).` |

### `dog5-docs/DOG-5-presets.md`

| line | class | status | text |
|---|---|---|---|
| 132 | ATTRIBUTION | KEPT | `- **29 "i scream" · P1 · from VINTAGE PD** — SOUND: a struck chime through a cheap van horn speaker (an ice-cr` |

### `dog5-docs/PERF-BASELINE.md`

| line | class | status | text |
|---|---|---|---|
| 1 | ATTRIBUTION | KEPT | `# Host CPU baseline — stock OberVave (v1.5.3, before any DØG-5 engine change)` |
| 14 | ATTRIBUTION | KEPT | `$ OBV_PERF=1 build/host/obervave build/host/obervave` |
| 48 | ATTRIBUTION | KEPT | `It builds `build/host/obervave-cg` with `-DOBV_CALLGRIND`, runs it under` |
| 56 | ATTRIBUTION | KEPT | `\| FM-1 (`obervave`) \| 242,432 \| 248,164,601 \| **1,024** \|` |
| 57 | ATTRIBUTION | KEPT | `\| SMK-37 (`obervave-smk37`) \| 242,432 \| 248,465,458 \| **1,025** \|` |
| 67 | ATTRIBUTION | KEPT | `session notes in `CLAUDE.md`'s preserved OberVave section recorded on this same host build (8 voices,` |

### `dog5-docs/voicing/03-half-life.md`

| line | class | status | text |
|---|---|---|---|
| 122 | ATTRIBUTION | KEPT | `* `tests/run_host.sh` passes (default script and the page/families/poly/spring/tape/bbd/map scripts), `obervav` |

### `dog5-docs/voicing/README.md`

| line | class | status | text |
|---|---|---|---|
| 752 | ATTRIBUTION | KEPT | `* **Provenance and Vincent's ear (docs addendum, 11 Nov 2026):** the patch is built by ear on the OberVave eng` |

### `dog5-docs/voicing/cards/29-i-scream.md`

| line | class | status | text |
|---|---|---|---|
| 20 | ATTRIBUTION | KEPT | `**Provenance, built by ear:** the patch was built by ear on the OberVave engine from field recordings Vincent ` |

### `firmware/hal/fm1_flash_map.h`

| line | class | status | text |
|---|---|---|---|
| 29 | IDENTITY | KEPT | `*   0x9D000-0xBAFFF  VM: the app's store (OberVave: settings, 8 patterns, owner tag)  FL_DATA` |
| 33 | ATTRIBUTION | KEPT | `*   0xC2000-0xE9FFF  USRFLASH: (SLOOP: user sample slots; OberVave: unused)        FL_SMP` |
| 72 | IDENTITY | KEPT | `/* the app's own store: FL_DATA and the sample slots (OberVave's platform.c gives a narrower FL_RANGE_OK) */` |
| 90 | ATTRIBUTION | KEPT | `/* Felucca's own store (projects, user samples; settings); OberVave's platform.c gives its own FL_RANGE_OK */` |

### `firmware/hal/fm1_lcd_hw.h`

| line | class | status | text |
|---|---|---|---|
| 18 | IDENTITY | KEPT | `*   fm1_lcd_done()             1: the SPI transfer is done (fm1_lcd_wait still clears it; OberVave: works mean` |

### `firmware/hal/smk_input.h`

| line | class | status | text |
|---|---|---|---|
| 4 | ATTRIBUTION | KEPT | `* OberVave: the pad event queue (smk_pad_events, smk_pad_take): Copyright (C) 2026 zvenson */` |
| 145 | IDENTITY | KEPT | `/* pad events for an app that handles the pads itself (smk_pad_events = 1, OberVave: the step pads): hardware ` |

### `firmware/loader/ldr_screen.c`

| line | class | status | text |
|---|---|---|---|
| 2 | ATTRIBUTION | KEPT | `* Copyright (C) 2026 zvenson (OberVave; the Firmware Hub's look)` |
| 14 | IDENTITY | CHANGED | `#define LDR_NAME "OBERVAVE"` |
| 17 | IDENTITY | CHANGED | `#define LDR_COLOUR 0x3C1Du               /* OberVave's blue, #3C82EB */` |

### `firmware/src/lcd.c`

| line | class | status | text |
|---|---|---|---|
| 28 | IDENTITY | KEPT | `LCD_IDLE();                /* the app's own work while the strip goes out (OberVave: the keys, MIDI) */` |

### `firmware/src/obervave.c`

| line | class | status | text |
|---|---|---|---|
| 2 | ATTRIBUTION | KEPT | `/* DØG-5 (forked from OberVave): one 8-voice analog-style polysynth for the M-VAVE FM-1. Built on Dinghy's` |
| 15 | FUNCTIONAL | KEPT | `* (OberVave's step sequencer, obv_seq.h, and the two-sound track B it alone drove, are gone: CLAUDE.md §5.` |
| 51 | IDENTITY | KEPT | `/* (the OberVave SET_VERSION 2 migration that brought 32 old programs over embedded an 80-byte patch_t; with t` |
| 634 | FUNCTIONAL | KEPT | `* prog_get, psect_save, psect_load, the boot reload) over tests/host.c's flash model. Run: `obervave selftest`` |

### `firmware/src/obv_dsp.h`

| line | class | status | text |
|---|---|---|---|
| 2 | IDENTITY | KEPT | `/* OberVave DSP building blocks, all fixed point (no FPU, no 64-bit division on the chip).` |

### `firmware/src/obv_fx.h`

| line | class | status | text |
|---|---|---|---|
| 7 | IDENTITY | KEPT | `* ALLEY (the Psych Chain's stage 2, CLAUDE.md section 6) is OberVave's ping-pong delay re-voiced as a bucket b` |
| 13 | IDENTITY | KEPT | `*   - the feedback path keeps OberVave's TONE (a 1-pole, the same law), loses its lows (a 1-pole high-pass at ` |
| 226 | IDENTITY | KEPT | `else {                                      /* SYNC: a note value of the tempo, as OberVave's delay */` |

### `firmware/src/obv_params.h`

| line | class | status | text |
|---|---|---|---|
| 198 | FUNCTIONAL | KEPT | `/* the button families: each remembers its last page (fam_last in obervave.c) */` |

### `firmware/src/obv_smk.h`

| line | class | status | text |
|---|---|---|---|
| 2 | ATTRIBUTION | KEPT | `* SMK-37 port of OberVave: Copyright (C) 2026 zvenson */` |
| 3 | IDENTITY | KEPT | `/* OberVave on the M-Vave SMK-37 (BOARD_SMK37; SMK37.md, smk37-port.yaml). The FM-1's panel keeps its jobs (th` |
| 18 | IDENTITY | KEPT | `* (The pads were OberVave's step sequencer and < > its page nav; both free, pads dark, with the sequencer DØG-` |
| 160 | IDENTITY | KEPT | `/* ---- KNOB BANK held: the panel check (OberVave has no serial console; this is what the kit's "smk" command ` |

### `firmware/src/obv_ui.h`

| line | class | status | text |
|---|---|---|---|
| 3 | IDENTITY | KEPT | `* American polys had them, a red LED program number drawn as 7-segment digits, "OBERVAVE" with three blue band` |
| 142 | IDENTITY | CHANGED | `static void draw_logo_small(int32_t x, int32_t y)   /* "OBERVAVE" in FONT_S with the bands through the lower h` |
| 144 | IDENTITY | CHANGED | `cv_text(x, y, &FONT_S, "OBERVAVE", C_CREAM);` |
| 161 | IDENTITY | CHANGED | `draw_logo_small(240 - 4 - text_w(&FONT_S, "OBERVAVE"), 4);` |

### `firmware/src/platform.c`

| line | class | status | text |
|---|---|---|---|
| 2 | ATTRIBUTION | KEPT | `/* OberVave's platform (Dinghy's): everything an FM-1 firmware needs before it can be fun, taken unchanged fro` |
| 15 | FUNCTIONAL | KEPT | `* The app (obervave.c) includes this file first and supplies:` |
| 76 | IDENTITY | CHANGED | `#define APP_NAME "OBERVAVE"` |
| 82 | FUNCTIONAL | CHANGED | `#define FELUCCA_ID "FM-1_950"                   /* package identity: 95N = OberVave build N (tools/build.py) *` |
| 95 | IDENTITY | KEPT | `#define CV_MAX (240u * 120u)                    /* the biggest strip drawn at once (OberVave: the knob page) *` |
| 125 | IDENTITY | KEPT | `#define SETTINGS_MAX (4096u - 12u)              /* the sector minus the header (OberVave keeps 32 programs in ` |
| 126 | IDENTITY | KEPT | `#define BLOBS_AT 0x000F4000u                    /* OberVave's sequencer patterns: 8 sectors below the settings` |
| 248 | IDENTITY | KEPT | `/* blob i (0..NBLOB-1): one more sector each, the same format (OberVave: a sequencer pattern) */` |
| 251 | IDENTITY | KEPT | `/* program sector i (0..NPSECT-1): the same format (OberVave: 50 user programs each) */` |
| 341 | IDENTITY | KEPT | `whose MIDI out works on the device; OberVave's babbled with the poll put off) */` |

### `firmware/src/smk_store.h`

| line | class | status | text |
|---|---|---|---|
| 2 | ATTRIBUTION | KEPT | `* SMK-37 port of OberVave: Copyright (C) 2026 zvenson */` |
| 3 | IDENTITY | KEPT | `/* OberVave's flash data on the M-Vave SMK-37 (BOARD_SMK37; platform.c includes this instead of its FM-1 lines` |
| 18 | IDENTITY | KEPT | `#define SETTINGS_MAX (4096u - 12u)              /* the sector minus the header (OberVave keeps 32 programs in ` |

### `firmware/src/smk_wheel.h`

| line | class | status | text |
|---|---|---|---|
| 3 | ATTRIBUTION | KEPT | `* (from genkigenki/sloop-fm1 smk37; OberVave: +-2 semitones, its range the program's BEND, obv_smk.h) */` |
| 4 | FUNCTIONAL | KEPT | `/* The SMK-37 Pro's pitch wheel as a bend (OberVave: obv_smk.h smk_wheels, into the engine's ctl_bend):` |
| 15 | IDENTITY | KEPT | `#define SMK_PW_ST 2               /* +- semitones at the end of the travel (OberVave: x the program's BEND / 2` |

### `firmware/src/usb.c`

| line | class | status | text |
|---|---|---|---|
| 43 | IDENTITY | KEPT | `* cure OberVave's MIDI IN babble, kept as harmless; the cure was building the app with -Os, see tools/build.py` |

### `smk37-port.yaml`

| line | class | status | text |
|---|---|---|---|
| 1 | IDENTITY | KEPT | `# smk37-port.yaml: every decision for OberVave's SMK-37 port, in one place (the fm1-to-smk37 kit's setup file,` |
| 6 | IDENTITY | KEPT | `name: OberVave                # unchanged on the SMK-37: the same name, logo and boot splash` |
| 7 | ATTRIBUTION | KEPT | `upstream: https://github.com/zvenson/obervave` |
| 8 | ATTRIBUTION | KEPT | `base: OberVave main 0b4512c (after 1.2.1, with the step sequencer), on Dinghy's platform` |
| 13 | ATTRIBUTION | KEPT | `# Dinghy's platform.c and OberVave's own storage (smk_store.h)` |
| 15 | IDENTITY | KEPT | `- TRS MIDI IN / MIDI clock in over TRS (none on the SMK; OberVave had no TRS MIDI IN on the FM-1 either,` |
| 21 | IDENTITY | KEPT | `- no USB serial console (OberVave has none on the FM-1 either): the kit's smk / padtest / leds commands are` |
| 24 | IDENTITY | KEPT | `- the OberVave workflow and manual unchanged (keys, the 14 buttons by name, the four knobs and their pages,` |
| 31 | ATTRIBUTION | KEPT | `mode: own                     # the owner's own firmware: the SMK build lives on branch smk37 of zvenson/oberv` |
| 34 | FUNCTIONAL | KEPT | `package: obervave-<ver>-smk37.fwsc, obervave-<ver>-smk37-elite.fwsc, obervave-<ver>-smk37-mke.fwsc` |
| 35 | FUNCTIONAL | KEPT | `# (a dev build without --release: obervave-smk37[-elite\|-mke].fwsc)` |
| 36 | FUNCTIONAL | KEPT | `identity: SMK-37 Pro_95N, SMK-37 Elite_95N, MKE-P37_95N   # N as the FM-1's FM-1_95N: the minor version, 0 = d` |
| 37 | ATTRIBUTION | KEPT | `usb_name: Felucca             # OberVave's USB / MIDI device name (Dinghy's usb.c); every installer finds it` |
| 38 | FUNCTIONAL | KEPT | `data_family: OBERVAV          # own family (tools/build.py SMK_DATA_FAMILY; "OBERVAVE" has 8 letters, 1..7 all` |
| 39 | ATTRIBUTION | KEPT | `copyright: zvenson            # new SMK files: "SMK-37 port of OberVave: Copyright (C) 2026 zvenson"; the laye` |
| 53 | IDENTITY | KEPT | `first_boot: clears the 10 sectors once if the tag is not OberVave's (the stock VM settings there, another port` |
| 64 | FUNCTIONAL | KEPT | `pattern: steps                # OberVave's sequencer (obv_seq.h): the 16 steps of the selected track's page` |
| 85 | IDENTITY | KEPT | `A: [CUTOFF, RESO, ENV AMT, RELEASE]          # OberVave's PERFORM page` |
| 130 | IDENTITY | KEPT | `style: keep                   # OberVave's screens; plus the fader / page overlay, the step view while a pad i` |
| 132 | IDENTITY | KEPT | `colours: OberVave's (blue-black panel, light blue accent, red program LEDs); pads in the same blue / cream / r` |
| 148 | IDENTITY | KEPT | `OberVave has no serial console for the kit's bring-up commands; keep it, or give it another job?` |
| 149 | IDENTITY | KEPT | `- KEY VELOCITY setting (the kit's DYNAMIC / SOFT / HARD / FIXED): not added, OberVave's GLOBAL page is full an` |

### `tests/bbd/render.sh`

| line | class | status | text |
|---|---|---|---|
| 12 | FUNCTIONAL | KEPT | `cc $CF -Ifirmware/src -Ifirmware/gen -o build/bbd/obervave firmware/src/obervave.c` |
| 15 | FUNCTIONAL | KEPT | `cc $CF -I"$T/firmware/src" -I"$T/firmware/gen" -o build/bbd/obervave_old "$T/firmware/src/obervave.c"` |
| 18 | FUNCTIONAL | KEPT | `build/bbd/obervave "build/bbd/$(basename "$s" .txt)" "$s" > "build/bbd/$(basename "$s" .txt).log"` |
| 22 | FUNCTIONAL | KEPT | `build/bbd/obervave_old "build/bbd/$(basename "$s" .txt)$([ "${s#*old_}" = "$s" ] && echo _oldbuild)" "$s" >/de` |

### `tests/bbd_page.txt`

| line | class | status | text |
|---|---|---|---|
| 1 | FUNCTIONAL | KEPT | `# ALLEY on the BBD DELAY page (obv_fx.h, obervave.c alley_*): KNOB 1 = ALLEY leaves SYNC from the time soundin` |

### `tests/drive/bitexact.sh`

| line | class | status | text |
|---|---|---|---|
| 16 | FUNCTIONAL | KEPT | `cc $CF -I"$T/ref/firmware/src" -I"$T/ref/firmware/gen" -o "$T/old" "$T/ref/firmware/src/obervave.c"` |
| 17 | FUNCTIONAL | KEPT | `cc $CF -Ifirmware/src -Ifirmware/gen -o "$T/new" firmware/src/obervave.c` |

### `tests/drive/render.sh`

| line | class | status | text |
|---|---|---|---|
| 9 | FUNCTIONAL | KEPT | `-o build/drive/obervave firmware/src/obervave.c` |
| 11 | FUNCTIONAL | KEPT | `build/drive/obervave "build/drive/$(basename "$s" .txt)" "$s" >/dev/null` |

### `tests/host.c`

| line | class | status | text |
|---|---|---|---|
| 2 | FUNCTIONAL | KEPT | `/* A fake FM-1 on a computer: the app (firmware/src/obervave.c) runs unchanged on it. platform.c includes` |
| 7 | FUNCTIONAL | KEPT | `*   cc -O2 -Wall -DOBV_HOST -Ifirmware/src -Ifirmware/gen -o build/host/obervave firmware/src/obervave.c` |
| 8 | FUNCTIONAL | KEPT | `*   build/host/obervave build/host/obervave        (-> build/host/obervave.wav, build/host/obervave-<ms>.ppm)` |
| 9 | FUNCTIONAL | KEPT | `*   build/host/obervave OUT script.txt [FPS]    (your own script; with FPS: OUT-NNNNN.ppm, a frame every 1/FPS` |
| 30 | FUNCTIONAL | CHANGED | `#define APP_NAME "OBERVAVE"` |
| 161 | FUNCTIONAL | KEPT | `static int host_selftest;                       /* "selftest" argv: run store_selftest() (obervave.c) instead ` |
| 195 | FUNCTIONAL | KEPT | `static uint32_t host_page_now(void);            /* (obervave.c: the page the panel is on) */` |
| 196 | FUNCTIONAL | KEPT | `static uint32_t host_map_idle_calls(void);      /* (obervave.c: app_idle calls the last control-map draw made)` |
| 197 | FUNCTIONAL | KEPT | `static void host_set_param(uint32_t p, int32_t v);   /* (obervave.c: set a parameter, as a knob would) */` |
| 198 | FUNCTIONAL | KEPT | `static uint32_t host_voices_on(void);           /* (obervave.c: how many voice cards are gated on) */` |
| 199 | FUNCTIONAL | KEPT | `static uint32_t host_get_param(uint32_t p);     /* (obervave.c: a parameter's value now) */` |
| 201 | FUNCTIONAL | KEPT | `static void host_vlog_set(uint32_t on);         /* (obervave.c: start / stop-and-print each card's vintage pit` |
| 271 | FUNCTIONAL | KEPT | `static const char *host_out = "build/host/obervave";` |
| 336 | FUNCTIONAL | KEPT | `*   valgrind --tool=callgrind --collect-atstart=no --combine-dumps=yes ./obervave ...` |
| 496 | FUNCTIONAL | KEPT | `app_main();                                 /* store_selftest() runs and exits if host_selftest (obervave.c) *` |

### `tests/install_test.py`

| line | class | status | text |
|---|---|---|---|
| 9 | ATTRIBUTION | CHANGED | `build/obervave.fwsc, skipped otherwise: OberVave has no web installer of its own; from genkigenki/sloop-fm1 sm` |
| 172 | FUNCTIONAL | KEPT | `TMP = Path(tempfile.mkdtemp(prefix="obervave-install-"))` |
| 366 | FUNCTIONAL | CHANGED | `clean = ROOT / "build/obervave.fwsc"` |
| 375 | FUNCTIONAL | CHANGED | `clean = ROOT / "build/obervave.fwsc"` |
| 376 | FUNCTIONAL | CHANGED | `for f in [clean, *sorted((ROOT / "build").glob("obervave*-smk37*.fwsc"))]:   # (OberVave: every package built)` |
| 380 | FUNCTIONAL | CHANGED | `print("logical image vs fm1pkg.js: skipped (needs node, web/fm1pkg.js and build/obervave.fwsc; OberVave has no` |

### `tests/ldr_screen_test.c`

| line | class | status | text |
|---|---|---|---|
| 2 | ATTRIBUTION | KEPT | `* Copyright (C) 2026 illuminus5 (Skiff's test), zvenson (OberVave) */` |

### `tests/pages.txt`

| line | class | status | text |
|---|---|---|---|
| 2 | FUNCTIONAL | KEPT | `# a screen after each. tests/run_host.sh tests/pages.txt -> build/host/obervave-<ms>.png` |

### `tests/perf_callgrind.sh`

| line | class | status | text |
|---|---|---|---|
| 16 | FUNCTIONAL | KEPT | `N=obervave; D=` |
| 17 | FUNCTIONAL | KEPT | `if [ "${BOARD:-fm1}" = smk37 ]; then N=obervave-smk37; D=-DBOARD_SMK37=1; fi` |
| 19 | FUNCTIONAL | KEPT | `-Ifirmware/src -Ifirmware/gen -o "build/host/$N-cg" firmware/src/obervave.c` |

### `tests/run_host.sh`

| line | class | status | text |
|---|---|---|---|
| 3 | FUNCTIONAL | KEPT | `# Run firmware/src/obervave.c on this computer (tests/host.c): build/host/obervave.wav and the screens as PNG.` |
| 4 | FUNCTIONAL | KEPT | `#   BOARD=smk37 tests/run_host.sh [script]: the SMK-37 build (pads, faders, wheels, outer keys; build/host/obe` |
| 8 | FUNCTIONAL | KEPT | `N=obervave; D=` |
| 9 | FUNCTIONAL | KEPT | `if [ "${BOARD:-fm1}" = smk37 ]; then N=obervave-smk37; D=-DBOARD_SMK37=1; fi` |
| 10 | FUNCTIONAL | KEPT | `cc -O2 -Wall -Wno-unused-function -DOBV_HOST $D -DAPP_VER="\"${APP_VER:-dev}\"" -Ifirmware/src -Ifirmware/gen ` |
| 15 | FUNCTIONAL | KEPT | `for p in sorted(Path("build/host").glob("obervave-*.ppm")):   # (the SMK build's too: obervave-smk37-*.ppm)` |

### `tests/run_tests.sh`

| line | class | status | text |
|---|---|---|---|
| 3 | IDENTITY | KEPT | `# OberVave's host tests (no hardware). Run from the repo root after building, the SMK-37 first, the FM-1 last` |
| 19 | FUNCTIONAL | CHANGED | `[ -f build/obervave.fwsc ] \|\| { echo "run ./build.sh first"; exit 1; }` |
| 54 | FUNCTIONAL | KEPT | `# 80-byte "BOVP" sector is rejected. Runnable on its own too: build/host/obervave selftest` |
| 55 | FUNCTIONAL | KEPT | `run "FM-1 program store: 99 patches round-trip, save isolation, old format rejected" "$OUT/obervave" selftest` |
| 56 | FUNCTIONAL | KEPT | `run "SMK-37 program store: same checks" "$OUT/obervave-smk37" selftest` |
| 64 | FUNCTIONAL | CHANGED | `run "M-UPGRADE entry (FM-1)" "$OUT/ota_test" build/obervave.fwsc` |
| 65 | FUNCTIONAL | KEPT | `head -c 60000 build/obervave.bin > "$OUT/old_app.bin"` |
| 70 | FUNCTIONAL | CHANGED | `run "update loader (FM-1): other app -> this build" "$OUT/ldr_test" "$OUT/old.fwsc" build/obervave.fwsc` |
| 74 | FUNCTIONAL | KEPT | `python3 tools/fm1pkg_make.py --board smk37 build/obervave.bin build/loader/ota.bin "$OUT/smk_new.fwsc" >/dev/n` |
| 88 | FUNCTIONAL | CHANGED | `for f in build/obervave*-smk37${m%%:*}.fwsc; do` |
| 91 | FUNCTIONAL | CHANGED | `v=$(echo "$f" \| sed -n 's/.*obervave-[0-9]\.\([0-9]\).*/\1/p'); v=${v:-0}` |
| 98 | FUNCTIONAL | KEPT | `if [ -n "$NODE" ] && [ -f docs/sim/obervave.wasm ]; then` |
| 101 | FUNCTIONAL | KEPT | `echo "(no node or no docs/sim/obervave.wasm: the browser simulator's test is skipped)"` |

### `tests/sim_test.mjs`

| line | class | status | text |
|---|---|---|---|
| 2 | FUNCTIONAL | KEPT | `// The browser simulator without a browser: loads docs/sim/obervave.wasm in node, boots it, plays a chord, MID` |
| 7 | FUNCTIONAL | KEPT | `//   node tests/sim_test.mjs [docs/sim/obervave.wasm]      (after sh web/sim/build.sh)` |
| 14 | FUNCTIONAL | KEPT | `const WASM = process.argv[2] \|\| path.join(ROOT, 'docs/sim/obervave.wasm');` |
| 136 | FUNCTIONAL | KEPT | `registerProcessor: (name, c) => { if (name === 'obervave') Proc = c; },` |
| 159 | FUNCTIONAL | KEPT | `const host = path.join(ROOT, 'build/host/obervave-simcmp');` |
| 163 | FUNCTIONAL | KEPT | `execFileSync('cc', ['-O2', '-w', '-DOBV_HOST', '-Ifirmware/src', '-Ifirmware/gen', '-o', host, 'firmware/src/o` |

### `tests/smk_flash_test.c`

| line | class | status | text |
|---|---|---|---|
| 2 | ATTRIBUTION | KEPT | `* SMK-37 port of OberVave: Copyright (C) 2026 zvenson` |
| 4 | IDENTITY | KEPT | `/* OberVave's SMK-37 flash map (build with -DBOARD_SMK37=1; firmware/src/smk_store.h, hal/fm1_flash_map.h): ev` |
| 7 | IDENTITY | KEPT | `* USR 0xF4000-0xFDFFF or key_mac 0xFF000-. OberVave's objects (settings, 8 patterns, the owner tag) and the OT` |

### `tests/smk_pkg_test.py`

| line | class | status | text |
|---|---|---|---|
| 3 | ATTRIBUTION | CHANGED | `# (from genkigenki/sloop-fm1 smk37; OberVave: identity SMK-37 Pro_950)` |

### `tests/smk_ui_test.py`

| line | class | status | text |
|---|---|---|---|
| 3 | ATTRIBUTION | KEPT | `# SMK-37 port of OberVave: Copyright (C) 2026 zvenson` |
| 6 | FUNCTIONAL | KEPT | `Builds build/host/obervave-smk37-test, runs tests/smk/*.txt, checks what comes out (MIDI out, the dumped` |
| 18 | FUNCTIONAL | KEPT | `BIN = OUT / "obervave-smk37-test"` |
| 47 | FUNCTIONAL | KEPT | `str(ROOT / "firmware/src/obervave.c")], check=True)` |

### `tests/smk_wheel_test.c`

| line | class | status | text |
|---|---|---|---|
| 1 | ATTRIBUTION | KEPT | `/* SPDX-License-Identifier: GPL-3.0-only (from genkigenki/sloop-fm1 smk37; OberVave: SMK_PW_ST 2) */` |
| 78 | IDENTITY | KEPT | `check(nb == SMK_PW_ST * 4096, "a quick bend to the top: +SMK_PW_ST semitones (OberVave: 2)");` |

### `tests/spring/regress.sh`

| line | class | status | text |
|---|---|---|---|
| 13 | FUNCTIONAL | KEPT | `cc $SAN -DOBV_HOST -DAPP_VER=\"dev\" -Ifirmware/src -Ifirmware/gen -o "$O/obervave" firmware/src/obervave.c` |
| 18 | FUNCTIONAL | KEPT | `if "$O/obervave" "$O/$n" "$s" > "$O/$n.log" 2>&1; then echo "clean   $s"; else echo "FAIL    $s"; grep runtime` |
| 35 | FUNCTIONAL | KEPT | `cc -O2 -Wall -Wno-unused-function -DOBV_HOST -DAPP_VER=\"dev\" -Ifirmware/src -Ifirmware/gen -o "$O/obervave_o` |
| 38 | FUNCTIONAL | KEPT | `"$O/obervave_o2" "$O/${n}_o2" "$s" > /dev/null` |

### `tests/spring/render.sh`

| line | class | status | text |
|---|---|---|---|
| 14 | FUNCTIONAL | KEPT | `cc $CF -Ifirmware/src -Ifirmware/gen -o $K/obervave firmware/src/obervave.c` |
| 18 | FUNCTIONAL | KEPT | `cc $CF -I"$T/firmware/src" -I"$T/firmware/gen" -o "$K/obervave_$r" "$T/firmware/src/obervave.c"` |
| 24 | FUNCTIONAL | KEPT | `$K/obervave "$K/$(basename "$s" .txt)" "$s" > "$K/$(basename "$s" .txt).log"` |
| 28 | FUNCTIONAL | KEPT | `$K/obervave_$OLD "$K/$(basename "$s" .txt)" "$s" > /dev/null` |
| 30 | FUNCTIONAL | KEPT | `$K/obervave_$PRE "$K/hot_reverb_prefix" tests/spring/hot_reverb.txt > /dev/null` |
| 31 | FUNCTIONAL | KEPT | `$K/obervave_$OLD "$K/hot_reverb_fixed" tests/spring/hot_reverb.txt > /dev/null` |

### `tests/tape/render.sh`

| line | class | status | text |
|---|---|---|---|
| 10 | FUNCTIONAL | KEPT | `-o build/tape/obervave firmware/src/obervave.c` |
| 14 | FUNCTIONAL | KEPT | `build/tape/obervave "build/tape/$(basename "$s" .txt)" "$s" >/dev/null` |

### `tests/trick/make_kit.py`

| line | class | status | text |
|---|---|---|---|
| 134 | FUNCTIONAL | KEPT | `exe = os.path.join(bd, "obervave")` |
| 136 | FUNCTIONAL | KEPT | `"-Ifirmware/gen", "-o", exe, "firmware/src/obervave.c"], cwd=ROOT, check=True)` |

### `tests/trick/slop_depths.py`

| line | class | status | text |
|---|---|---|---|
| 32 | FUNCTIONAL | KEPT | `exe = os.path.join(bd, f"obervave_{x2}")` |
| 34 | FUNCTIONAL | KEPT | `'-DAPP_VER="dev"', "-Ifirmware/src", "-Ifirmware/gen", "-o", exe, "firmware/src/obervave.c"],` |

### `tests/voicing/batch01a.py`

| line | class | status | text |
|---|---|---|---|
| 347 | FUNCTIONAL | KEPT | `old = K.build_host(base, os.path.join(K.BUILD, "obervave_base"))` |

### `tests/voicing/batch02a.py`

| line | class | status | text |
|---|---|---|---|
| 421 | FUNCTIONAL | KEPT | `old = K.build_host(base, os.path.join(K.BUILD, "obervave_base"))` |

### `tests/voicing/batch03a.py`

| line | class | status | text |
|---|---|---|---|
| 335 | FUNCTIONAL | KEPT | `old = K.build_host(base, os.path.join(K.BUILD, "obervave_base"))` |

### `tests/voicing/batch03b.py`

| line | class | status | text |
|---|---|---|---|
| 464 | FUNCTIONAL | KEPT | `old = K.build_host(base, os.path.join(K.BUILD, "obervave_base"))` |

### `tests/voicing/batch04a.py`

| line | class | status | text |
|---|---|---|---|
| 235 | FUNCTIONAL | KEPT | `old = K.build_host(base, os.path.join(K.BUILD, "obervave_base"))` |

### `tests/voicing/batch04b.py`

| line | class | status | text |
|---|---|---|---|
| 142 | FUNCTIONAL | KEPT | `old = K.build_host(base, os.path.join(K.BUILD, "obervave_base"))` |

### `tests/voicing/batch05a.py`

| line | class | status | text |
|---|---|---|---|
| 272 | FUNCTIONAL | KEPT | `old = K.build_host(base, os.path.join(K.BUILD, "obervave_base"))` |

### `tests/voicing/batch05b.py`

| line | class | status | text |
|---|---|---|---|
| 350 | FUNCTIONAL | KEPT | `old = K.build_host(BASE, os.path.join(K.BUILD, "obervave_base"))` |

### `tests/voicing/diag09.py`

| line | class | status | text |
|---|---|---|---|
| 27 | FUNCTIONAL | KEPT | `exe = K.build_host(src, os.path.join(K.BUILD, "obervave_diag"))` |
| 86 | FUNCTIONAL | KEPT | `old = K.build_host(os.path.join(K.BUILD, "base"), os.path.join(K.BUILD, "obervave_base"))` |

### `tests/voicing/half_life.py`

| line | class | status | text |
|---|---|---|---|
| 205 | FUNCTIONAL | KEPT | `old = K.build_host(base, os.path.join(K.BUILD, "obervave_base"))` |

### `tests/voicing/identical.py`

| line | class | status | text |
|---|---|---|---|
| 57 | FUNCTIONAL | KEPT | `old = K.build_host(base, os.path.join(K.BUILD, "obervave_base"))` |
| 58 | FUNCTIONAL | KEPT | `new = K.build_host(K.ROOT, os.path.join(K.BUILD, "obervave_new"))` |

### `tests/voicing/identical_par.py`

| line | class | status | text |
|---|---|---|---|
| 36 | FUNCTIONAL | KEPT | `old = K.build_host(base, os.path.join(K.BUILD, "obervave_base"))` |
| 37 | FUNCTIONAL | KEPT | `new = K.build_host(K.ROOT, os.path.join(K.BUILD, "obervave_new"))` |

### `tests/voicing/voicekit.py`

| line | class | status | text |
|---|---|---|---|
| 9 | FUNCTIONAL | KEPT | `exe = build_host()                                  # build/voicing/obervave (the working tree's firmware)` |
| 60 | FUNCTIONAL | KEPT | `out = out or os.path.join(BUILD, "obervave")` |
| 64 | FUNCTIONAL | KEPT | `"-I" + os.path.join(ROOT, "tests"), "-o", out, os.path.join(src_dir, "firmware", "src", "obervave.c")],` |
| 286 | FUNCTIONAL | KEPT | `return build_host(src_dir, os.path.join(BUILD, "obervave-cg"), ("-DOBV_CALLGRIND",))` |

### `tools/build.py`

| line | class | status | text |
|---|---|---|---|
| 4 | ATTRIBUTION | CHANGED | `"""Build OberVave (on Felucca / SLOOP's platform): the app, the update loader and an installable .fwsc package` |
| 8 | FUNCTIONAL | CHANGED | `Outputs in build/: obervave.bin (app), loader/ota.bin (update loader),` |
| 9 | FUNCTIONAL | CHANGED | `obervave.fwsc (package). See README.md for the toolchain and the SDK.` |
| 12 | FUNCTIONAL | CHANGED | `identity SMK-37 Pro_950 (release X.Y: SMK-37 Pro_95Y, as the FM-1's FM-1_95Y), the SMK flash layout (fm1pkg_ma` |
| 13 | FUNCTIONAL | CHANGED | `app slot 0x97400), the package build/obervave-smk37.fwsc (obervave-X.Y-smk37.fwsc for a release). MODEL=elite ` |
| 16 | FUNCTIONAL | CHANGED | `that unit's factory package: obervave-smk37-elite.fwsc, -mke.fwsc. The default stays the FM-1, built exactly a` |
| 59 | FUNCTIONAL | CHANGED | `PRODUCT = "FM-1_950"                # OberVave: 95N (OUR_LOADER in the installer wants FM-1_9NN). Your fork: p` |
| 61 | FUNCTIONAL | CHANGED | `BOARD_PREFIX = {"fm1": "FM-1_95", "smk37": "SMK-37 Pro_95"}   # identity: prefix + the minor version (0: a dev` |
| 179 | FUNCTIONAL | KEPT | `("cc", *flags, "-c", FW / "src" / "obervave.c", "-o", OUT / "obervave.o")]` |
| 181 | FUNCTIONAL | KEPT | `elf = OUT / "obervave.elf"` |
| 190 | FUNCTIONAL | KEPT | `OUT / "fm1_isr.o", OUT / "obervave.o", "-o", elf)` |
| 199 | FUNCTIONAL | KEPT | `(OUT / "obervave.dis").write_text(dis)` |
| 216 | FUNCTIONAL | KEPT | `(OUT / "obervave.bin").write_bytes(img)` |
| 301 | FUNCTIONAL | CHANGED | `ap.add_argument("--release", metavar="X.Y", help="release build: identity FM-1_95Y, version string X.Y")` |
| 323 | FUNCTIONAL | CHANGED | `name = f"obervave{suffix}.fwsc"` |
| 330 | FUNCTIONAL | CHANGED | `name = f"obervave-{a.release}{suffix}.fwsc"` |
| 351 | FUNCTIONAL | KEPT | `print(f"app      {OUT / 'obervave.bin'}  {len(img)} B")` |

### `tools/fm1_install.py`

| line | class | status | text |
|---|---|---|---|
| 6 | FUNCTIONAL | KEPT | `The same update as the web installer (web/fm1ota.js): step 1, the` |
| 41 | ATTRIBUTION | KEPT | `# (the FM-1 and the SMK-37 family under OberVave / Felucca (its USB name), under the other ports, the update l` |

### `tools/gen_font.py`

| line | class | status | text |
|---|---|---|---|
| 10 | FUNCTIONAL | KEPT | `OBERVAVE wordmark in it) -- not re-cut from a bigger source font. Both store 1-bit glyphs as 4-bit` |
| 32 | FUNCTIONAL | KEPT | `L_FIRST, L_LAST = 32, 95                         # 'OBERVAVE' wordmark range: upper case + punctuation` |

### `tools/gen_tables.py`

| line | class | status | text |
|---|---|---|---|
| 3 | FUNCTIONAL | KEPT | `"""OberVave's fixed-point tables (the chip has no FPU): tools/gen_tables.py -> firmware/gen/obv_tables.h` |

### `tools/make_logo.py`

| line | class | status | text |
|---|---|---|---|
| 3 | IDENTITY | KEPT | `"""OberVave's logo: tools/make_logo.py -> assets/logo.svg, assets/logo.png (and the same on a transparent back` |
| 22 | FUNCTIONAL | KEPT | `WORD = "OBERVAVE"` |

### `video/make_short.py`

| line | class | status | text |
|---|---|---|---|
| 3 | IDENTITY | KEPT | `"""OberVave 1.2.1: the Short (1080 x 1920, 30 fps, ~45 s), the same found VHS tape as the long video (make_vid` |
| 17 | FUNCTIONAL | KEPT | `OUT = MV.A / "obervave-1.2.1-short.mp4"` |
| 128 | IDENTITY | KEPT | `CASS = MV.cassette(940, "OBERVAVE", "DO NOT ERASE!")` |
| 217 | IDENTITY | KEPT | `c = MV.cassette(820, "OBERVAVE 1.2.1", DOMAIN, (40, 90, 200)).rotate(-6, Image.BICUBIC, expand=True)` |

### `video/make_video.py`

| line | class | status | text |
|---|---|---|---|
| 3 | IDENTITY | KEPT | `"""OberVave video 1.4.1 (1920 x 1080, 30 fps, ~115 s): eight OberVaves play one slow dark track (song.py: the ` |
| 6 | IDENTITY | KEPT | `labelled OBERVAVE · DO NOT ERASE goes into the recorder, the picture has the tape's soft colours, a wobble, th` |
| 38 | FUNCTIONAL | KEPT | `OUT = HERE / "obervave-1.4.1.mp4"` |
| 198 | IDENTITY | KEPT | `for _wd in WORDS + ["OBERVAVE"]:` |
| 202 | IDENTITY | KEPT | `make_logo.render(make_logo.logo_svg(_p, _w, background=False, bands=_wd == "OBERVAVE", pad=70), _png, int((_w ` |
| 422 | IDENTITY | KEPT | `TAPE = cassette(1100, "OBERVAVE", "DO NOT ERASE!")` |
| 790 | IDENTITY | KEPT | `END_TAPE = cassette(820, "OBERVAVE 1.4.1", "thefirmwarehub.com", (40, 90, 200))` |
| 821 | ATTRIBUTION | KEPT | `for ln in ("OberVave 1.4.1: free firmware, GPL-3.0. Built on Dinghy,",` |
| 825 | IDENTITY | KEPT | `"Every sound: OberVave on the FM-1, eight of them. No samples were harmed."):` |
| 908 | IDENTITY | KEPT | `c = cassette(1000, "OBERVAVE", "DO NOT ERASE!").rotate(8, Image.BICUBIC, expand=True)` |

### `video/song.py`

| line | class | status | text |
|---|---|---|---|
| 2 | FUNCTIONAL | KEPT | `"""The OberVave video's music: eight OberVaves (the real firmware's host build, firmware/src/obervave.c), each` |
| 16 | FUNCTIONAL | KEPT | `HOST = OBV / "build" / "host" / "obervave"` |
| 215 | IDENTITY | KEPT | `# DRUMS: three OberVaves from INIT. Kick: the resonant 12 dB filter rings like a sine, the envelope drops its ` |
| 224 | IDENTITY | KEPT | `"""kick and hats on ONE OberVave (1.4: track B has a sound of its own): the kick is sound A on track A, the ha` |

### `web/sim/build.sh`

| line | class | status | text |
|---|---|---|---|
| 3 | IDENTITY | KEPT | `# OberVave in the browser: the firmware's sources (unchanged) + web/sim/sim.c -> WebAssembly, plus the page.` |
| 4 | FUNCTIONAL | KEPT | `#   sh web/sim/build.sh   ->  docs/sim/{index.html, sim.js, sim.css, worklet.js, obervave.wasm, logo.png}` |
| 8 | FUNCTIONAL | KEPT | `#     python3 -m venv ~/.local/share/obervave-wasm && ~/.local/share/obervave-wasm/bin/pip install ziglang` |
| 11 | FUNCTIONAL | KEPT | `#     unpacked into ~/.local/share/obervave-wasm/` |
| 14 | FUNCTIONAL | KEPT | `T="$HOME/.local/share/obervave-wasm"` |
| 32 | FUNCTIONAL | KEPT | `-o docs/sim/obervave.wasm` |
| 39 | FUNCTIONAL | KEPT | `echo "sim: docs/sim ($(wc -c < docs/sim/obervave.wasm \| tr -d ' ') B wasm)"` |

### `web/sim/index.html`

| line | class | status | text |
|---|---|---|---|
| 7 | IDENTITY | KEPT | `<title>OberVave Simulator</title>` |
| 8 | IDENTITY | KEPT | `<meta name="description" content="OberVave, an 8-voice analog-style polysynth firmware for the FM-1, running i` |
| 14 | IDENTITY | KEPT | `<img class="logo" src="logo.png" alt="OberVave">` |
| 18 | FUNCTIONAL | KEPT | `<a class="cta" href="https://thefirmwarehub.com/#fw-obervave">Install on your FM-1 &rarr;</a>` |
| 19 | ATTRIBUTION | KEPT | `<a href="https://github.com/zvenson/obervave">Source code</a>` |
| 124 | ATTRIBUTION | KEPT | `<p>OberVave by <a href="https://github.com/zvenson">zvenson</a>, built on` |

### `web/sim/sim.c`

| line | class | status | text |
|---|---|---|---|
| 2 | FUNCTIONAL | KEPT | `/* OberVave in a browser: the firmware's own sources (firmware/src/obervave.c, unchanged) on the host build's ` |
| 32 | FUNCTIONAL | KEPT | `#include "../../firmware/src/obervave.c"` |

### `web/sim/sim.css`

| line | class | status | text |
|---|---|---|---|
| 2 | IDENTITY | KEPT | `/* OberVave simulator: thefirmwarehub.com's warm dark, OberVave's red and blue (assets/logo) */` |

### `web/sim/sim.js`

| line | class | status | text |
|---|---|---|---|
| 2 | IDENTITY | KEPT | `// OberVave simulator, the page: builds the panel (27 keys, 14 buttons, 7 encoders + MASTER), starts the Audio` |
| 3 | FUNCTIONAL | KEPT | `// (worklet.js runs obervave.wasm, the firmware), draws its 240 x 240 screen and LEDs, and feeds it the mouse,` |
| 14 | FUNCTIONAL | KEPT | `const STORE_KEY = 'obervave-sim-store-1', MASTER_KEY = 'obervave-sim-master';` |
| 20 | IDENTITY | KEPT | `const ev = (a) => { try { if (window._paq) window._paq.push(['trackEvent', 'Play', 'OberVave: ' + a]); } catch` |
| 64 | FUNCTIONAL | KEPT | `const [wasm] = await Promise.all([fetch('obervave.wasm').then((r) => { if (!r.ok) throw new Error('obervave.wa` |
| 66 | FUNCTIONAL | KEPT | `S.node = new AudioWorkletNode(S.ctx, 'obervave', { numberOfInputs: 0, outputChannelCount: [2], processorOption` |

### `web/sim/worklet.js`

| line | class | status | text |
|---|---|---|---|
| 2 | FUNCTIONAL | KEPT | `// OberVave in an AudioWorklet: obervave.wasm is the firmware (firmware/src, unchanged) on a simulated FM-1` |
| 7 | IDENTITY | KEPT | `class OberVave extends AudioWorkletProcessor {` |
| 79 | FUNCTIONAL | KEPT | `registerProcessor('obervave', OberVave);` |
