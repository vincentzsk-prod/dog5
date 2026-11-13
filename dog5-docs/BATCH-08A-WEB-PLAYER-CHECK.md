# Batch 8A — Web player: toolchain check (no build, no merge)

Run 13 Nov 2026 in a Claude Code cloud session. Branch `build/batch-08a-web-player-check`. `firmware/`, `web/sim/` and
`tests/ref-sim/` were not touched; all build output is in `/tmp/dog5-sim/` (scratch, untracked).

## 1. Verdict

**READY WITH FIXES** — both tools install through the session network and the sim builds and passes the sound/screen test once one missing `exit()` is stubbed, but `web/sim/sim.c` as committed does not compile against the DØG-5 source and the sim's storage code does not cover the new program sectors.

## 2. Toolchain

| Tool | How obtained | Version | Result |
|---|---|---|---|
| zig | not preinstalled (`command -v zig` empty). `python3 -m venv ~/.local/share/obervave-wasm && .../bin/pip install ziglang` | ziglang pip package; `python -m ziglang version` = **0.17.1** | worked (PyPI reachable) |
| wasm-opt | not preinstalled. Option 4a: `npm install --prefix ~/.local/share/obervave-wasm/npm binaryen` | binaryen npm **132.0.0** (`wasm-opt version 132 (version_132)`) | worked. It is a `#!/usr/bin/env node` script (JS build), executable via the `.bin/wasm-opt` symlink, not a native binary. `build.sh` never needs a native one: it just runs `$WASM_OPT`. |
| `--asyncify`, `--enable-bulk-memory` | `wasm-opt --help \| grep` | — | both listed; `--asyncify` ran fine in Step 2 |
| Pillow | `python3 -c "import PIL"` | 12.3.0 | present (the logo step will resize, not fall back) |
| clang / cc / node | preinstalled | `/usr/bin/cc`, node v22.23.4 | present |

Not tried (stopped at first success): `pip install binaryen`, the GitHub release tarball.
Note: `build.sh` looks for `$T/binaryen-*/bin/wasm-opt` or `wasm-opt` on PATH. The npm install is at neither, so a future session must run `WASM_OPT=$HOME/.local/share/obervave-wasm/npm/node_modules/.bin/wasm-opt sh web/sim/build.sh` (the script honours `WASM_OPT=`). The script also still writes into `tests/ref-sim/` and `obervave.wasm` (hard-coded), which is why I ran the commands by hand.

## 3. Build result

Commands (copied from `build.sh`, outputs redirected):

```
Z="$HOME/.local/share/obervave-wasm/bin/python -m ziglang"
$Z cc --target=wasm32-freestanding -mcpu=generic+bulk_memory -O2 -fno-builtin -ffreestanding -nostdlib \
  -Wall -Wno-unused-function -Wno-unused-variable -Wno-unused-but-set-variable -Ifirmware/src -Ifirmware/gen \
  -Wl,--no-entry -Wl,--export-memory -Wl,--export-dynamic -Wl,-z,stack-size=262144 -o /tmp/dog5-sim/raw.wasm web/sim/sim.c
wasm-opt /tmp/dog5-sim/raw.wasm --enable-bulk-memory --asyncify -O2 --strip-debug --strip-producers -o /tmp/dog5-sim/dog5.wasm
```

**Compile of the committed `web/sim/sim.c`: FAILED, exit 1, 0.2 s.** Single error:

```
web/sim/../../firmware/src/obervave.c:719:5: error: call to undeclared function 'exit'; ISO C99 and later do not support implicit function declarations
  719 |     exit(sf_fail ? 1 : 0);
```

Cause: the store self-test (`store_selftest()`, `#if`-guarded host-only block in `obervave.c`, added with the 96-byte record) calls `exit()`; the freestanding wasm has no libc. Trivial, not structural. It is the only error; there were no warnings.

**Probe (extra, beyond the stop rule; scratch only):** a copy of `sim.c` in `/tmp/dog5-sim/probe/sim_probe.c` with one added line, `static void exit(int c) { (void)c; for (;;) ; }`, same flags otherwise.
- zig compile: exit 0, 3.0 s, no warnings, `raw.wasm` 610,262 B.
- wasm-opt: exit 0, 2.5 s, `dog5.wasm` **96,480 B** (44,660 B gzipped). (The stale committed OberVave wasm is 176,128 B.)

## 4. Test result

`node tests/sim_test.mjs /tmp/dog5-sim/dog5.wasm` (needs `worklet.js` next to the wasm; I copied it to `/tmp/dog5-sim/`; the host binary is built by the test with `cc`):

```
ok    no imports (standalone)
ok    sim_init(44100)
264600 frames, peak 0.202, rms 0.0630, chord rms 0.1227
ok    no NaN / Inf
ok    the chord sounds
ok    no clipping (peak below full scale)
ok    the screen changes (31 different screens at 100 ms steps)
ok    PRESETS +1 -> program 02 (prog 1)
ok    button LEDs (0x4)
speed: 10 s of audio in 116 ms (86x real time)   [first run; ~same later]
ok    renders at least 5x faster than real time
heaviest program: 22, 1 s with 8 keys in 16.3 ms   (an earlier run named 07, 24.9 ms)
ok    every program renders at least 4x faster than real time
ok    storage blobs exported
FAIL  SAVE twice -> the settings sector changes
ok    a new instance with the saved bytes boots on program 33
ok    worklet.js: boots (ready)
ok    worklet.js: sends the screen when it changes (39 frames in 4 s)
ok    worklet.js: a key sounds through process()
ok    worklet.js: boots with the storage it was given
ok    sound = the host build's, sample for sample (264448 frames, 0 differ, max 0)
ok    screen at 2600 ms = the host build's (0 pixels differ)
ok    screen at 3400 ms = the host build's (0 pixels differ)
ok    screen at 5600 ms = the host build's (0 pixels differ)
SIM TEST FAILED   (only because of the one FAIL above)
```

**Sound equality with the native host build: bit-identical** (0 of 264,448 frames differ), and the three screens match pixel for pixel.

**The one FAIL is a real gap, not a flaky test:** SAVE now writes the program into `host_psect[]` (3 program sectors, `tests/host.c:148`), and `sim_blob()` / `sim_store_hash()` / the worklet's "9 blobs" cover only the settings sector + 8 pattern sectors. So the sim runs and saves in RAM, but **saved programs would never reach localStorage and would be lost on reload.** (Test's "boots on program 33" passes only because the program number lives in settings.)

Patches via PRESETS encoder (`sim_enc(6, n)`) / program change, chord keys 7,11,14,18 held 4 s, master unity, in node:
- **22 Melting Orb:** peak 0.542, rms 0.160, 0 NaN, 4 s rendered in 51 ms = **79x real time**.
- **30 THE DØG:** peak 0.422, rms 0.139, 0 NaN, 4 s in 59 ms = **67x real time**.
(Slot numbers are 1-based; confirmed names in `obv_patches.h`: 22 Melting Orb, 30 THE D\xD8G.)

## 5. Stale OberVave / Felucca references in `web/sim/`

- `build.sh:3,4,8,11,14,32,39` — OberVave comment; output dir `tests/ref-sim/`; `obervave.wasm`; `~/.local/share/obervave-wasm`; binaryen tarball hint (the install path I used is not the one the script searches).
- `sim.c:2` comment "OberVave in a browser"; `sim.c:12-13` `OBV_HOST`, `OBV_WASM` (`OBV_HOST` is still the right macro: the DØG-5 `tests/run_host.sh` and `tests/host.c` use it; `OBV_WASM` is defined but I found no use of it in `firmware/src` by grep, inferred unused); `sim.c:32` `obervave.c` (still the real DØG-5 filename).
- `worklet.js:2` comment, `:7` class `OberVave`, `:79` `registerProcessor('obervave', …)`; also hard-coded `9` blobs at `:16-18` and `:45-46`.
- `sim.js:2-3` comments; `:14` `STORE_KEY = 'obervave-sim-store-1'` and `'obervave-sim-master'`; `:20` Matomo event text `'OberVave: '`; `:64` `fetch('obervave.wasm')` and error text; `:66` `'obervave'` node name.
- `sim.css:2` comment.
- `index.html:7` title "OberVave Simulator"; `:8` meta description (says 8-voice analog-style polysynth); `:14` logo alt; `:18` link `thefirmwarehub.com/#fw-obervave`; `:19` link `github.com/zvenson/obervave`; `:124-127` footer ("OberVave by zvenson, built on Dinghy / Felucca (Leo Kuroshita…) / SLOOP"; the GPL credits must stay, per `CLAUDE.md` §11, but the first words need the DØG-5 line "DØG-5 by ZIGGY (DØGS)" above them); `:40-64` how-to text (says "program (32)", mentions the deleted sequencer: SEQ/PLAY/REC, "Hold SEQ", "SAVE twice", ALGORITHM "sequencer track", chorus/delay/reverb FX list). `web/sim/index.html` also still ships OberVave's logo via `assets/logo-transparent.png` in `build.sh`.
- The `Felucca` word appears only in the footer credit (`index.html:126`).

## 6. Answers to Step 4 (read from source)

1. **Audio start.** `sim.js start()` runs on a click on the full-screen `#power` button (and on the first pointerdown on any key/knob/button, or a mapped computer key). It checks `window.AudioWorkletNode` (throws "this browser has no AudioWorklet"), creates `AudioContext({sampleRate: 44100})` (falls back to default rate, then throws if not 44100 — **risk: some phone browsers/hardware run at 48000 and the page then refuses to start; I did not test a phone**), calls `ctx.resume()` inside the gesture, loads `worklet.js` + the wasm, shows errors on the power button. There is a visibility/touch `resume()` hook. Web MIDI is only requested when the "Connect MIDI" button is clicked, and the code checks `navigator.requestMIDIAccess` and says "no Web MIDI (Safari)". Ran in node only; no real browser or phone test done.
2. **Picking a program.** The sim exports `sim_prog()` (read) but **no "load slot N"**. Without any `sim.c` change: send a MIDI program change, `sim_midi(0xC0, n-1, 0)`, from the page (worklet already forwards `{t:'midi', d:[st,d1,d2]}`). I ran it: PC 30, 22, 1, 99 all give `sim_prog()+1` = 30, 22, 1, 99 (works while MIDI channel is OMNI, the default; see `obervave.c:599-603`). That is the clean way for a clickable list, no firmware or sim.c edit. What the page would still need: the 99 slot names. The sim has no name export (inferred from the exports list in `sim.c`); either the page hard-codes the 32 factory names (generated from `firmware/src/obv_patches.h`, "THE D\xD8G" needs the Ø) with 33-99 as "INIT", or a small `sim.c` addition `sim_prog_name(i)`. A highlight of the current slot can use `sim_prog()` through a new message or, with no sim.c change, be inferred from what was clicked. Note PRESETS wraps (encoder) vs PC direct.
3. **Computer keyboard map** (`sim.js` `CODEKEY`/`CODEBTN`, physical `e.code`): keys 0-6 (F3..B3): `Q 2 W 3 E 4 R`; keys 7-23 (C4..E5): `Z S X D C V G B H N J M , L . ; /`; keys 24-26 (F5, F#5, G5): `I 9 O`. Buttons: `1` HOME, `5` ENV, `7` LFO, `8` ARP, `0` SEQ, `-` EDIT, `=` GLO, `[` FX, `]` SAVE, Enter SEL, Space PLAY, `\` REC, ←/→ OCT−/+; ↑/↓ turn PRESETS. FETCH/ALGORITHM and KNOB 1-4 have no key (mouse drag/wheel only). Button index map is `platform.c`'s BTN_* (0 OCT− … 13 REC); I did not re-check it against the current `platform.c`, but the sim_test panel works with those indices. Note: the dog-name labels (HEEL, FLOP, WAG…) do not appear in this page; the SEQ button now does TAPE STOP and PLAY STOP.
4. **Phones home.** `sim.js:20`: `ev(a)` pushes `['trackEvent','Play','OberVave: '+a]` to `window._paq` (Matomo) **only if `window._paq` exists**. `web/sim/index.html` does not define `_paq` or load any Matomo script (grepped: no `matomo`/`_paq` in index.html), so on this page it sends nothing; it would only fire if embedded in a page that loads Matomo. Events if it did: `start`, `first note`, `1 min`, `5 min`, `midi` (no notes, no settings). No fetch/XHR/beacon anywhere else in `sim.js` or `worklet.js` (read in full). Recommendation: delete the hook for 8B. Everything else is local: `localStorage` for the store and master volume.
5. **Size** (what 8B would ship): wasm 96,480 B, `sim.js` 15,924, `sim.css` 8,493, `index.html` 6,883, `worklet.js` 3,458, logo 79,910 B (640 px resize, the stale one; the original `assets/logo-transparent.png` is 289,369 B and is the OberVave logo, so 8B needs the DØG-5 art or none) — **~211 KB uncompressed** (wasm alone is 44,660 B gzipped; the rest I did not gzip). Far below Pages limits.
6. **Where it lives.** I could not read the repo's Pages settings from this session (no `gh`, MCP only) — "Pages serves `main:/docs`" is **inferred** from the `docs/install/` installer and `docs/index.html`; not confirmed. If true, `docs/play/` would be `https://vincentzsk-prod.github.io/dog5/play/`. `docs/index.html` currently has `<meta http-equiv="refresh" content="0; url=install/">` and a link; it would need to change only if Vincent wants a landing page that links both; the player is reachable by URL without changing it. Not changed.

## 7. What Batch 8B would need to do

1. `sim.c`: add an `exit()` stub (one line) — or `#ifdef OBV_WASM` guard in `store_selftest` (but that is `firmware/`, forbidden here; stub in `sim.c` is the clean route).
2. `sim.c` + `worklet.js`: export the 3 `host_psect` sectors (blobs 9..11 → 12 blobs, `sim_blob`, `sim_store_hash`, the `9 * size` checks, the `store.byteLength` test) and bump `STORE_KEY` (new key `dog5-sim-store-1`) so old 80-byte data is never loaded. Update `tests/sim_test.mjs` (blob checks, SAVE test: it now has to save via SAVE → PRESETS slot → SAVE, per `CLAUDE.md` §5 and the write-lock).
3. `build.sh`: output to `docs/play/` (not `tests/ref-sim/`), rename `obervave.wasm`→`dog5.wasm`, add the npm wasm-opt path to the search list, DØG-5 logo.
4. `index.html`/`sim.js`/`worklet.js`/`sim.css`: rename everything in §5, rewrite the how-to for the 20-page / HEEL / FLOP / hold-HOME map reality, remove or neutralise Matomo, add the clickable patch list via MIDI program change, 99 slots, mark 1-32 THE POUND.
5. A names list generated from `obv_patches.h` (with the Ø) so no hand copy drifts.
6. Check the 44.1 kHz-only AudioContext requirement on a real phone.
7. Unsure: whether `OBV_WASM` is used anywhere; whether Pages is on `main:/docs`; whether a native host binary built from `-O2` hosting cc matches `-Os` device behaviour (irrelevant to the sim, it is a host/wasm build).

## 8. What I did not check

No real browser or phone (AudioWorklet, 48 kHz contexts, Web MIDI, touch), no hold-HOME/map or live-trick screens in the sim, Pages configuration, and the probe-only `exit()` stub was never put in the repo.
