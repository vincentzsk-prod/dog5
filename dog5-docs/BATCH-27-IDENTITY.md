# Batch 27: DØG-5's own identity, FM-1_3645 (v0.4.5)

21 Nov 2026, Vincent Kruger with Claude. Branch `build/batch-26-records` (on top of Batch 26's records).

## Why

The Firmware Hub requires an identity no other firmware uses. Its live catalogue (read 21 Nov) showed `FM-1_964` taken
(SIDOU), and so was the whole `FM-1_96N` family: 960 SID-1, 961 FOMAJAM, 963 Mini-Grain, 965 Quantum GammaWave, 966 GR!MM,
967 AETHER FM1, 968 RUPTURE, 969 Demake and Kitten Synths. The Project doc `DOG-5-hub-readiness.md` has the full inventory.

## What

- **`FM-1_3645XYZ`.** 3645 is DØG-5 on a phone keypad (D=3, O=6, G=4, then 5). XYZ is vX.Y.Z, one digit each (`.Z` absent =
  0): v0.4.5 is `FM-1_3645045`, v6.3.5 `FM-1_3645635`, a dev build `FM-1_3645000`. No catalogue entry starts with
  `FM-1_3645`. `firmware/src/dog5_id.h` (`DOG5_ID_FM1 "FM-1_3645"`), `tools/build.py` (the `--release` rule),
  `platform.c`'s host fallback.
- **Digits only.** Vincent asked for `FM-1_3645_V6.3.5`, or `FM-1_3645_V635` if the full stop was a problem. Both fail:
  every FM-1 installer reads an identity as `NAME_digits` (`re.fullmatch(r"([^_]+)_(\d+)")` in `fm1_install.py`,
  `/^([^_]+)_(\d+)$/` in `fm1install.js`, and the Hub's installer comes from the same line). A second underscore or a
  letter leaves the unit unrecognised: "Find my FM-1" would not find it, and an install could not confirm the unit
  restarted as the package. So the version digits follow `3645` directly.
- **Release assets are `dog5.fwsc` every time** (`release.yml`: the package is copied to `dist/dog5.fwsc`, with its
  `SHA256SUMS`, and only that is attached and attested). The Hub updates in place when the asset name stays the same.
  The installer page keeps its dated file (`dog5-0.4.5-20261121.fwsc`), and `./build.sh --release X.Y.Z` still writes
  `build/dog5-X.Y.Z.fwsc`.
- **README:** a line that DØG-5 reads only its own saves and can write over another firmware's; back up first. This is
  the Hub's Knowledge Base ask.
- Docs: `docs/install/README.md` (the identity section rewritten), `README.md`, `CLAUDE.md` §10–§12, `PLATFORM-API.md`.

## Checks

- The package's identity reads `FM-1_3645045` through `fm1_install.py`'s own `product_of`, and matches its identity
  pattern; the app image carries the string.
- Sound byte-identical to `main` (host WAVs, `cmp`). The only firmware change is the identity string.
- `./build.sh --release 0.4.5` twice, same SHA-256 `ba17666051fc293f9879c62ff81e74eeec41c62f5e566006305b264e2a2d96a3`,
  614,757 B. Image 392,148 B, RAM 34,928 B, pool 319,760 B.
- Installer page regenerated and in sync; `tests/run_tests.sh` ALL TESTS PASSED; `node tests/sim_test.mjs` passes.

## On the unit

Install 0.4.5 over 0.4.4 from the installer page. At the end the page must say the unit reports `FM-1_3645045`. If the
page cannot find the unit before installing, it is still on 0.4.4 (`FM-1_964`), which every installer reads fine. Then
"Find my FM-1" once more should show `FM-1_3645045`.
