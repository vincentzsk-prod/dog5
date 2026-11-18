# Batch 12B — the clean-up (executed)

Branch `build/batch-12b-cleanup`, off `origin/main` at `1015e4e` (Merge PR #27, Batch 11, the v0.2 build flashed and
tested on the unit 18 Nov). Run directly by Claude in the planning chat, with the repo attached. Executes the inventory in
`history/BATCH-12A-CLEANUP-INVENTORY.md` with Vincent's decisions of 18 Nov. **No firmware source changed.**

## Proof

| check | `main` (before) | this branch |
|---|---|---|
| `dog5-0.2.fwsc` SHA-256 (clean `build/`) | `b2be33a9…6b96` | **`b2be33a9…6b96`**, identical (= the package on the unit and on the installer page) |
| `dog5.fwsc` (dev build) | `8f0e4a49…749f` | identical |
| image / RAM / pool | 82,352 / 32,432 / 304,896 B | identical |
| `sh tests/run_tests.sh` | rc 1: 20 stale `expect` FAILs + 2 false "FAIL" matches | **rc 0, ALL TESTS PASSED** |
| passing lines | 485 | 484 = 485 + 20 fixed expectations − 21 SMK-package lines (the 3 SMK packages are no longer built) |
| `make_installer_page.py --check` | in sync | in sync |
| `sh web/sim/build.sh` → `docs/play/dog5.wasm` | — | byte-identical to the committed one; `node tests/sim_test.mjs` passes |

## Decisions applied (12A numbering)

- **D1 SMK-37: frozen.** `release.yml` builds and publishes the FM-1 package only; `SMK37.md` is now a short "not
  supported" note. The SMK code, `smk37-port.yaml` and the SMK host tests stay until a firmware clean-up removes them.
- **D2** the three `listen/trick/*.wav` and **the four `listen/voicing/**/*_held.wav`** left main (10.8 MB). Identical
  copies (blob hashes checked) are on every `listen/` branch, e.g. `listen/batch-06b2-bell-clean`; the READMEs say so.
- **D3** `video/` deleted (it drove the deleted sequencer and was OberVave-branded).
- **D4** `docs/install/previous/` deleted. v0.1 as published is commit **`7a1fba8`** (the last `main` with the 0.1
  installer page; its `docs/install/dog5-0.1-20261112.fwsc` is byte-identical, sha256 `3de092d5…7f6a`). A tag was planned
  (`archive/dog5-0.1`) but the cloud session's git proxy refuses tag pushes (HTTP 403); never use a `v*` name for one:
  `release.yml` builds and publishes a release on `v*` tags.
- **D5** deleted `tests/pages.txt` (stale, no expectations; `families.txt` covers the 21 pages), `tests/controls/bitident.sh`
  + `render4.txt` (Batch 9B's one-off proof; `tests/drive/bitexact.sh` and `tests/voicing/identical.py` do the general
  job). The generated kit scripts stay. Moved to `dog5-docs/history/`: `BATCH-07`, `BATCH-08B`, `DOG-5-build-review.md`,
  and the 12A inventory itself.
- **D6** OberVave logo and splash kept until the DØG-5 wordmark exists (Stage 4).
- **D7** `reference-renders/` kept as is.
- **D8** `docs/API.md` → `dog5-docs/PLATFORM-API.md`, `docs/RULES.md` → `dog5-docs/CHIP-RULES.md`. Pages now serves only
  `docs/index.html`, `install/`, `play/`.
- **D9** the five merged branches deleted from the remote (the four `build/batch-*` and `claude/peaceful-planck-6oikap`).
  Every `listen/` branch kept (each holds WAVs found nowhere else).

## Also deleted (12A's DELETE list)

`tests/ref-sim/` (with its gate in `run_tests.sh` moved to `docs/play/dog5.wasm`, so the browser test still runs),
`dog5-docs/_archive/` (the reaper-era narrative and asset libraries), `dog5-docs/screens/`, `BATCH-08A`,
`docs/MAKE-IT-YOURS.md`, `assets/logo-transparent.*`, `assets/obervave-screen.png`, `tests/programs_33_64.txt`,
`tests/save_as.txt`. 41 files in all.

## Fixed

- **The 20 stale expectations:** `drive_page`, `layer_lock`, `tape_page` now set their own starting values with `param`
  lines (as `fx_layer` and `spring_page` already did), so re-voicing program 1 cannot break them again. Their expected
  numbers did not change; all 47 expect lines run and pass.
- **The 2 false matches:** the loader-screen check no longer has the word FAILED in its label (the panel still says
  UPDATE FAILED; only the test text changed).
- `tests/install_test.py`: the always-skipped `fm1pkg.js` cross-check removed (`tests/install/js_side.mjs` already compares
  the page's JavaScript image with Python's); its loader-marker checks kept.
- `release.yml`: deps from our `build-deps-v1` release (`get_vendored_deps.sh`), FM-1 only, **host tests now block a
  release**.
- `CLAUDE.md`: the 254-line duplicate of `CLAUDE.obervave.md` removed (53 → 31 KB, every session reads it); the doc map,
  the dev-setup notes (plain `./build.sh` last; branch from `origin/main`; SMK frozen) and §11 (v0.2 on the unit) updated.
- `README.md`: DØG-5 only. OberVave's README (which installed OberVave) is cut; a pointer to it upstream remains.
- `LICENSING.md`: three rows pointed at deleted paths. Credits unchanged; `LICENSE` and `NOTICE` untouched.
- `PERF-BASELINE.md`: a dated "now" table (the old figures were from before the sequencer went).
- Comments: `web/sim/build.sh`, the `run_tests.sh` header.

## Left for the firmware clean-up batch (12A §3, its own proof)

The 43 dead `PF_*` arrays and `P_CHO_*` in `obv_patches.h` / `obv_params.h`, unused functions, `SMK_PAD_HELD`, stale
firmware comments (`obervave.c:16` still says REC taps ALLEY), the SMK-37 code, and (separately, with a flash-map review)
the sequencer's pattern-sector reservation. Proof recipe in 12A §3.
