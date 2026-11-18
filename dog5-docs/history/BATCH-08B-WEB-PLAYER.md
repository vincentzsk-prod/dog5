# Batch 8B — The DØG-5 web player

**BUILT.** `docs/play/` is a self-contained page (no network calls beyond its own files, no analytics, no cookies) that runs the
unchanged DØG-5 firmware as WebAssembly. Live path once merged: `https://vincentzsk-prod.github.io/dog5/play/` (Pages source
`main:/docs` is inferred from the installer's location, not checked).

## What changed, by file
- `web/sim/sim.c` — `exit()` stub (the store self-test in `obervave.c` calls it); exports 12 storage blobs (`sim_nblobs`, blobs 9–11 =
  `host_psect`), `sim_store_hash` over all 12. Header credits kept.
- `web/sim/worklet.js` — class `DOG5`, processor `dog5`; loads/reports `sim_nblobs()` (12) blobs, ignores a store of any other length
  (an old 9-blob store is dropped whole); frame message now carries `prog`.
- `web/sim/sim.js` — Matomo hook deleted entirely; keys `dog5-sim-store-1` / `dog5-sim-master`; fetches `dog5.wasm` at page load;
  patch list built from `patches.json`, a click sends a MIDI program change (`0xC0, slot-1`); current patch highlighted from `prog`;
  the 44.1 kHz refusal is now a clear message (below).
- `web/sim/index.html`, `sim.css` — new page (text wordmark, honest notice, patch list beside the device ≥1240 px and under it
  below, how-to, keyboard map, MIDI, footer with repo/installer/licence/credits). No logo image. Changed visible text: title, header,
  "install on your FM-1" link (now `../install/`), source link (now the dog5 repo), how-to box (rewritten; no sequencer text), "Your
  programs" → "Your patches", footer (DØG-5 line first; OberVave/Dinghy/Felucca/SLOOP credits copied from `README.md`).
- `web/sim/gen_patches.py` (new) — parses the `FACTORY[NFACT]` table of `obv_patches.h` (read only), `\xD8` → Ø, four chapters of eight.
- `web/sim/build.sh` — outputs `docs/play/` (or `$1`), `dog5.wasm`; finds wasm-opt on PATH / `$WASM_OPT` / `binaryen-*/bin` / the npm
  path; installs nothing, prints the commands when a tool is missing; no logo step; POSIX sh.
- `tests/sim_test.mjs` — default wasm `docs/play/dog5.wasm`; storage check now on the program sectors; new checks for 12 blobs, the
  9-blob store being ignored, `prog` in frames.
- `CLAUDE.md` — browser-player notes. `docs/play/*` — built output. `dog5-docs/screens/play-*.png`. `docs/index.html` untouched.

## Rebuild
```
python3 -m venv ~/.local/share/obervave-wasm && ~/.local/share/obervave-wasm/bin/pip install ziglang
npm install --prefix ~/.local/share/obervave-wasm/npm binaryen
sh web/sim/build.sh
node tests/sim_test.mjs
python3 -m http.server -d docs/play 8737
```

## What the page does not do
1. It does not model the FM-1's real-time limits (CPU budget): a heavy patch can sound different on the device.
2. Saved patches live in that browser's localStorage only; nothing is shared between browsers or people.
3. The GLOBAL page's CPU readout is the device's render-time meter and shows `0us` in the browser (seen on screen).

## Things to know
- Patch clicks use MIDI program change on channel 1: if someone sets a MIDI channel on the GLOBAL page, the list stops loading patches
  (PRESETS and the arrow keys still work).
- No write-lock exists in the firmware yet, so SAVE can overwrite slots 1–32 in the sim (it is the browser's copy; "Forget saved
  patches" restores them). The page advises saving into 33–99.
- The `.fwsc`-side firmware is unchanged: `git diff origin/main -- firmware/` is empty.
