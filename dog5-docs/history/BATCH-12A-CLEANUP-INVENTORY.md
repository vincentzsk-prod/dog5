# Batch 12A — clean-up inventory (read-only, plus a dry run)

Branch `build/batch-12a-cleanup-inventory`, off `origin/main` at `1015e4e` (Merge PR #27, Batch 11). `dog5-docs/BATCH-11-TEST-BUILD-0.2.md` is present. **Nothing on `main` was changed; the only commit adds this file.** The dry run ran in a throwaway `git worktree` (removed afterwards). Every row below is evidence (file:line, grep, commit, test run) unless it says *judgment*; where I could not tell it says UNSURE and what I would need.

## 0. Status and the short version

* **Package hash after the dry run deletion is identical to `origin/main`'s**: see §6. No firmware file was touched.
* The 22 `FAIL` lines are **20 stale test expectations + 2 false positives** (the text "UPDATE FAILED" in a passing test). All 20 come from one cause: three host scripts assume patch 1 *Red Pill* is still at its Batch-2 values (GROWL 0, RESO 30, BIAS 40…), but Batch 3A voiced it (GROWL 46, RESO 58, BIAS 30). I re-ran the three scripts with only the expected numbers changed: **0 FAIL, exit 0** (§2). No real bug among them.
* **Biggest findings**
  1. `.git` is **686 MB** (pack), tracked tree 167 MB. 154 MB of that is WAVs: `reference-renders/` is 147 MB (protected, approved variants) and `listen/` still carries **7 WAVs (10.8 MB) on `main`** against the "WAVs only on `listen/` branches" rule. The 11 `listen/` branches hold the rest (about 2.5 GB if you count each tree, because every branch carries the previous kits).
  2. **`CLAUDE.md` lines 387–640 are a byte-for-byte copy of `dog5-docs/CLAUDE.obervave.md`** (`diff` = 0 lines). It makes `CLAUDE.md` 53 KB; every session pays for the duplicate.
  3. **Root `README.md` lines 28–end (about 85 % of the file) is OberVave's old README**, including install / build / hub instructions that install **OberVave, not DØG-5**, and a sequencer chapter.
  4. **`tests/run_tests.sh:102` gates the browser-simulator test on `tests/ref-sim/obervave.wasm`** (the stale OberVave build), while the test itself loads `docs/play/dog5.wasm`. Delete `tests/ref-sim/` and that test **silently skips**. It needs a one-line gate change first (done in the dry run).
  5. **The firmware has 43 dead OberVave patch arrays (13.7 KB of source)** in `obv_patches.h`, plus the sequencer's flash-sector reservation, unused fields and stale comments (§3). The `video/` pipeline drives the deleted sequencer and cannot reproduce its own video any more.
  6. The brief said ~41 remote branches. **`git ls-remote --heads origin` shows 16** (main + 15). I list all 16 (§4). If 41 were expected, ~25 were already deleted or live in another fork; I cannot tell which.

Counts (full table in §1): see the summary line at the end of §1.

## 1. Classification table

Columns: path · size (tracked bytes) · what it is · who references it (grep evidence) · last commit touching it · **class**. Sizes are from `git ls-tree -l`. "refs" excludes the file itself and the generated `docs/install/index.html`. Dates are the last commit date.

### 1.1 Root files

| path | size | what / who references it | last | class |
|---|---|---|---|---|
| `LICENSE` | 34 KB | GPL-3.0 text | a2fb3d0 15 Oct | **KEEP** (licence; never delete) |
| `NOTICE` | 1 KB | who made what, third parties; cited by README | 9290eb5 12 Nov | **KEEP** (attribution) |
| `LICENSING.md` | 4 KB | per-file licence table; credit line "DØG-5 by ZIGGY (DØGS)" | 3e81af8 12 Nov | **KEEP + REWRITE small**: rows 17 and 27 name `tests/ref-sim/` (and `web/sim` as built "in `tests/ref-sim/`"); row 19 is the SMK-37 port (follows the SMK decision); the video fonts (Permanent Marker Apache-2.0, VT323 OFL) are in `video/fonts/` with their licence texts but have **no row** in LICENSING.md |
| `CLAUDE.md` | 53 KB | the build brief. 640 lines: §1–13 DØG-5 (lines 1–383) + preserved OberVave notes (387–640) | 0941c54 18 Nov | **KEEP + MERGE**: drop 387–640 (exact duplicate of `dog5-docs/CLAUDE.obervave.md`, `diff` empty); fix §9 text about `tests/ref-sim/`; §12 doc map lists `_archive/` |
| `README.md` | 16 KB | lines 1–26 DØG-5 (status v0.2, install, build, credits); 28–end OberVave 1.5.3 README "preserved": "The synth", "The panel", **"The sequencer"** (deleted in DØG-5), "Build and run", `assets/logo.png`, a hub link that installs OberVave; line 70 and 179 point at `tests/ref-sim/`; line 74 SMK37.md; line 76 `video/` | 46c3c25 18 Nov | **REWRITE** (see §1.2) |
| `build.sh` | 1 KB | device build entry; called by README, run_tests, release.yml, CLAUDE.md §9 | 9290eb5 12 Nov | **KEEP** (header comment still says "forked from OberVave"; fine) |
| `SMK37.md` | 9 KB | user guide to OberVave on the SMK-37. refs: `README.md:74`, `build.sh:6` (comment), `firmware/src/obv_smk.h:3`, `platform.c:25`, `tools/build.py:13`, `LICENSING.md:19`, `smk37-port.yaml:3`. Still titled **"OberVave on the M-Vave SMK-37"**, lists `obervave-<version>-smk37.fwsc`, `SMK-37 Pro_95N` identities (stale: build now emits `dog5-*-smk37*.fwsc`, `SMK-37 Pro_96N`) and the pads as step sequencer (deleted) | 9290eb5 12 Nov | **UNSURE → decision D1** (the SMK variant). Stale either way → REWRITE or go with the variant |
| `smk37-port.yaml` | 8 KB | the SMK port's decisions file for the `fm1-to-smk37` kit; refs: `SMK37.md:141`, `LICENSING.md:19`, comments in `obv_smk.h:3`. Says "name: OberVave", "base: OberVave main 0b4512c" | a2fb3d0 15 Oct | **UNSURE → D1**; nothing in the build reads it (`git grep smk37-port` → only comments and docs) |
| `.gitignore` | <1 KB | `build/`, `__pycache__/`, `.DS_Store` | — | **KEEP** |
| `.github/workflows/release.yml` | 3 KB | CI: builds **3 SMK-37 + 1 FM-1 packages**, runs `tests/run_tests.sh` as `continue-on-error`, releases `build/dog5-*.fwsc` on a tag | 9290eb5 12 Nov | **KEEP + REWRITE small**: comment "(at the 18.10.2026 state some host tests are stale…)" and non-blocking tests (§2 makes the tests green, then make them blocking); uses `pkgman.jieliapp.com` + gitee instead of our `get_vendored_deps.sh` release (judgment: switch, it is the same pinned pair) |

### 1.2 `README.md` — what is wrong (REWRITE)

Keep lines 1–26 (DØG-5 status, install, build, credits) and update them; cut line 28–end. The cut section: (a) tells users to install OberVave from the Firmware Hub ("The install lines and the Firmware Hub link below install OberVave, not DØG-5" is the file's own warning at line 31), (b) documents a sequencer, a 3-page FX bank (chorus / delay / reverb) and a panel that no longer exist, (c) shows `assets/logo.png`/`assets/obervave-screen.png`, (d) points the browser player at `tests/ref-sim/`. If provenance of the base README matters, one line "OberVave 1.5.3's README is at upstream `zvenson/obervave@v1.5.3`" does it; it is also in git history. GPL attribution stays in the lines 1–26 credits paragraph plus `NOTICE` / `LICENSING.md`.

### 1.3 `firmware/` — all KEEP (protected: "firmware/ sources")

| path | size | note | class |
|---|---|---|---|
| `firmware/src/*` (21 files) | 380 KB | the app. `obv_patches.h` 49 KB, `obervave.c` 58 KB, `usb.c` 48 KB | **KEEP** (dead code inside: §3) |
| `firmware/src/obv_smk.h`, `smk_store.h`, `smk_wheel.h`, `firmware/hal/smk_input.h` | 10+3.5+2.7+31 KB | SMK-37-only files; `BOARD_SMK37` appears in 14 firmware files (counts in §3.4) | **KEEP** (follows D1) |
| `firmware/hal/*` (19 files), `firmware/loader/*` (5), `crt0.S`, `app.ld` | 150 KB | platform; `tools/build.py` compiles them | **KEEP** |
| `firmware/gen/obv_tables.h`, `felucca_font.h`, `obv_splash.h` | 34 / 212 / 124 KB | generated, committed (`gen_tables.py`, `gen_font.py`, `make_logo.py --splash`) | **KEEP** (splash is still the OberVave wordmark: see D6) |

### 1.4 `tools/` — all KEEP

| path | refs (evidence) | last | class |
|---|---|---|---|
| `build.py` | `build.sh`, release.yml, CLAUDE.md:38 | 12 Nov | KEEP |
| `fm1pkg_make.py`, `lz4blk.py` | imported by `build.py:41-42`; run_tests.sh:70,78 | 15 Oct | KEEP |
| `fm1_install.py` | README:14, `tests/install_test.py`, `tests/install/py_side.py` | 12 Nov | KEEP |
| `make_installer_page.py` | README:17, `docs/install/README.md:90`, run in dry run `--check` | 12 Nov | KEEP |
| `gen_tables.py`, `gen_font.py`, `make_logo.py` | generate committed headers (`firmware/gen/*.h` first line names them) | 3 Nov / 29 Oct / 15 Oct | KEEP |
| `get_toolchain.sh` | `release.yml:30`, `build.sh:17` | 15 Oct | KEEP |
| `get_vendored_deps.sh` | CLAUDE.md:303; ran in this batch | 2 Nov | KEEP |
| `image_diff.py` | only `LICENSING.md:18` and its own docstring; no script calls it. It is the "device image only shrinks / functions unchanged" proof tool the firmware clean-up batch needs (§3) | 12 Nov | KEEP (judgment) |

### 1.5 `web/`, `docs/`, Pages

| path | size | what / refs | last | class |
|---|---|---|---|---|
| `web/install/{fm1install.js,index.template.html}` | 22+22 KB | installer page source, read by `tools/make_installer_page.py` (tested by `tests/install/`) | 12 Nov | KEEP |
| `web/sim/{build.sh,sim.c,gen_patches.py,index.html,sim.css,sim.js,worklet.js}` | 53 KB | browser-player source; `index.html/sim.css/sim.js/worklet.js` are **byte-identical copies** of `docs/play/*` (`cmp`) — by design, `build.sh` copies them | 18 Nov | KEEP. `build.sh:7` comment about `tests/ref-sim/` → REWRITE (comment) |
| `docs/index.html` | 276 B | redirect to `install/` | 12 Nov | KEEP (Pages root) |
| `docs/install/index.html`, `dog5-0.2-20261118.fwsc` | 860 KB, 612 KB | generated installer + the package it embeds; `tests/install/run.sh` and `make_installer_page.py --check` require exactly one `dog5-*.fwsc` beside the page | 18 Nov | KEEP |
| `docs/install/README.md` | 8.5 KB | installer notes | 18 Nov | KEEP |
| `docs/install/previous/dog5-0.1-20261112.fwsc` | 612 KB | the v0.1 package; no code reads `previous/` (`make_installer_page.py` deletes older `dog5-*.fwsc` only beside the page; Batch 11 §0.2 put it here by hand). Referenced only in prose by `BATCH-11-…md:10` | 18 Nov | **UNSURE → D4** (it is in git history at 46c3c25's parent; I cannot tell whether users link to it) |
| `docs/play/{index.html,sim.css,sim.js,worklet.js,dog5.wasm,patches.json}` | 138 KB | the live browser player (`/play/`), rebuilt by `web/sim/build.sh`; `tests/sim_test.mjs` reads `dog5.wasm` | 18 Nov | KEEP |
| `docs/API.md` | 8 KB | "Dinghy API": platform.c's calls. Names `dinghy.c` which does not exist here. refs: `README.md:185`, `CLAUDE.md:511` | 12 Nov | **MOVE** to `dog5-docs/PLATFORM-API.md` (useful reference, wrongly served by Pages; REWRITE the `dinghy.c` line) |
| `docs/RULES.md` | 3 KB | "The chip's rules" (integers only, -Os, …) — duplicates CLAUDE.md §2, still true. refs `README.md:185`, `CLAUDE.md:511` | 12 Nov | **MOVE** to `dog5-docs/CHIP-RULES.md` (or MERGE into CLAUDE.md §2, judgment) |
| `docs/MAKE-IT-YOURS.md` | 3 KB | Dinghy template guide: "Use this template…", ids `FM-1_99x`, Hub submission steps for a *new* project. refs: only `CLAUDE.md:511` (a list) and `BATCH-07-…:55,63` (audit prose) | 12 Nov | **DELETE** (nothing builds / links it; describes copying Dinghy, not DØG-5) |

**Pages.** GitHub Pages serving mode is not readable from this container (no settings API). README says "once GitHub Pages is on for `main` `/docs`", CLAUDE.md §9 says `docs/play` is live at `https://vincentzsk-prod.github.io/dog5/play/`. So Pages serves `docs/`: `docs/index.html`, `install/`, `play/` are the public surface. Moving `API.md`, `RULES.md` out changes two public URLs (`/API.md`, `/RULES.md`; if Pages runs Jekyll they render as pages). Nothing in the repo links to those URLs except README:185 and CLAUDE.md:511. **Could not determine** whether anything outside the repo does.

### 1.6 `assets/`

| path | size | refs | last | class |
|---|---|---|---|---|
| `assets/fonts/ter-u16n.bdf`, `Terminus-LICENSE.txt` | 181 KB, 4 KB | `tools/gen_font.py:4-5`, `LICENSING.md:25`, `felucca_font.h:1` | 29 Oct | **KEEP** (font source + OFL notice) |
| `assets/logo.svg`, `logo.png` | 72 KB, 263 KB | `tools/make_logo.py` writes them; `README.md` (the part to be cut) shows `logo.png`; `LICENSING.md:26` covers the URW Bookman outlines in `assets/logo*.svg`; the OberVave wordmark | 12 Nov | **UNSURE → D6** (OberVave logo; the DØG-5 wordmark does not exist yet, Stage 4) |
| `assets/logo-transparent.svg`, `.png` | 72 KB, 289 KB | `make_logo.py` makes them; only prose in `BATCH-08A-…md` names the png; no page, test or doc displays them | 12 Nov | **DELETE** (regenerable by `make_logo.py`) |
| `assets/obervave-screen.png` | 4 KB | only `README.md` (the OberVave part to be cut) | 12 Nov | **DELETE** |

### 1.7 `dog5-docs/`

| path | size | status / refs | last | class |
|---|---|---|---|---|
| `DOG-5-base-and-ui-decisions.md` | 32 KB | "newest, authoritative"; refs CLAUDE.md §12, 5 docs | 18 Nov | KEEP (live) |
| `DOG-5-build-kit.md`, `DOG-5-character-brief.md`, `DOG-5-presets.md`, `DOG-5-art-direction.md`, `DOG-5-chapter-specs.md`, `DOG-5-field-prompts.md` | 18/16/17/6/7/5 KB | CLAUDE.md §8/§12 name them as the live art world & preset records (Stage 3 gates on them). `DOG-5-presets.md` is cited from `obv_patches.h` / `obv_params.h` / `obervave.c` | various | KEEP |
| `DOG-5-foundation.md` | 7 KB | CLAUDE.md §12: §1–2, §5 superseded | 18 Nov | **REWRITE** (strike the superseded sections, or MERGE the still-true DSP/IP rules into CLAUDE.md) |
| `DOG-5-build-review.md` | 3 KB | "tone + UI critique that drove the above"; refs CLAUDE.md §12 only | 29 Oct | **UNSURE → D5** (history; decisions already moved into the live docs) |
| `PERF-BASELINE.md` | 16 KB | host-instr tables per stage (`tests/perf_callgrind.sh`, `tests/host.c`, CLAUDE.md, voicing README). **Stale memory figures**: "image 107,920 B / RAM 32,304 / pool 275,868" (lines 119–233) vs. the current build **image 82,352 B, RAM 32,432 B, pool 304,896 B** (this batch's build log, same as Batch 11 §8) | 3 Nov | **REWRITE** (add a "now" table; keep the dated stage logs as history) |
| `CLAUDE.obervave.md` | 25 KB | OberVave's original notes; refs CLAUDE.md §12 and BATCH-09B. **Identical** to CLAUDE.md 387–640 | 29 Oct | **KEEP as the single copy** (MERGE: delete the copy in CLAUDE.md) |
| `_archive/` (3 files) | 5.5 KB | `README.md` + the two reaper-era docs. CLAUDE.md §12 says "do NOT build from"; refs: CLAUDE.md, BATCH-09B (prose) | 29 Oct | **DELETE** (+ edit CLAUDE.md §12 lines; the files are in git history) |
| `screens/*.png` (6) | 640 KB | `families-proof`, `hold-home-map`, `pages-20`, `poly-voice-plus`: **no reference anywhere** (`git grep -F` on each basename). `play-desktop`, `play-mobile`: named in prose by `BATCH-08B-…md:24` | 13 Nov / 2 Nov | **DELETE** (proof screenshots; `tests/run_host.sh` regenerates host screens; `pages-20.png` is also stale, 21 pages now) |
| `BATCH-07-IDENTITY-AUDIT.md` | 61 KB | the OberVave→DØG-5 identity audit with per-line KEEP/CHANGE decisions (incl. which attributions were kept). refs none | 12 Nov | **MOVE** to `dog5-docs/history/` (provenance of the attribution decisions; large; judgment) |
| `BATCH-08A-WEB-PLAYER-CHECK.md` | 14 KB | pre-build check of the simulator; its recommendations were carried out by 08B. refs none | 13 Nov | **DELETE** |
| `BATCH-08B-WEB-PLAYER.md` | 3 KB | what 8B built; facts now in CLAUDE.md §9 | 13 Nov | **MOVE** to `history/` |
| `BATCH-09B-CONTROLS.md` | 28 KB | the controls spec detail (CLAUDE.md §5 summarises it); cited by 11 | 18 Nov | **KEEP** (live facts: black-key map, SELECT/REC rules, test list) |
| `BATCH-11-TEST-BUILD-0.2.md` | 12 KB | the 0.2 build record; cited by the Reef Break card and `obv_patches.h` | 18 Nov | **KEEP** |
| `voicing/` (README 173 KB, 24 logs, `cards/` 32 cards + README) | 1.1 MB | **protected** (voicing kit and cards) | 18 Nov | **KEEP** |

### 1.8 `tests/`

| path | size | what / refs | last | class |
|---|---|---|---|---|
| `run_tests.sh`, `run_host.sh`, `host.c` | 10+1+26 KB | the harness; `host.c` is the host app | 18 Nov / 12 Nov | **KEEP**; `run_tests.sh:102-105` gate → `docs/play/dog5.wasm` (**REWRITE**, see §0 item 4); header comment still describes OberVave and `tests/ref-sim` |
| `sim_test.mjs` | 12 KB | run by run_tests.sh and by hand; default `docs/play/dog5.wasm` | 13 Nov | KEEP |
| `install/` (6 files) | 35 KB | `sh tests/install/run.sh` | 12 Nov | KEEP (protected) |
| `install_test.py`, `ota_test.c`, `ldr_test.c`, `ldr_screen_test.c` | 23/9/12/6 KB | in run_tests.sh | 12 Nov / 15 Oct / 19 Oct | KEEP |
| `smk_flash_test.c`, `smk_wheel_test.c`, `smk_pkg_test.py`, `smk_ui_test.py`, `smk/*.txt` | 5/5/3/4 KB + 4 files | in run_tests.sh; SMK-37 only | 29 Oct / 12 Nov | **UNSURE → D1** (go with the SMK variant) |
| `ref-sim/` (6 files: `obervave.wasm`, `index.html`, `sim.js`, `sim.css`, `worklet.js`, `logo.png`) | 283 KB | the **stale OberVave simulator**. refs: `run_tests.sh:102-105` (a gate only), `README.md:70,179`, `LICENSING.md:17,27`, `web/sim/build.sh:7` (comment), CLAUDE.md:296 ("kept untouched as provenance; nothing builds into it any more"), `BATCH-08A-…md` (prose). It is OberVave's own browser build (the upstream wasm, not our source) | 12 Nov | **DELETE**, **after** `run_tests.sh` gate fix + 3 pointer edits (done in dry run; sim test still ran and passed) |
| `controls/` (5 files) | 8 KB | `edit_keys.txt`, `select_dial.txt`, `rec_hold.txt` run by run_tests; `bitident.sh`, `render4.txt` are Batch-9B's before/after proof (not run; Batch 11 §11: slot 14 differs by design, so the script now reports "differ") | 18 Nov | KEEP the three; `bitident.sh`/`render4.txt` **UNSURE → D5** (one-off proof; `tests/drive/bitexact.sh` and `tests/voicing/identical.py` do the general job) |
| `trick/` (9 files) | 22 KB | 6 `*.txt` run by run_tests; `make_kit.py`, `slop_depths.py`, `tapestop_ab.py` cited by `obv_deck.h:27`, `obv_engine.h:71`, CLAUDE.md:167 | 3 Nov | **KEEP** (the scripts are tests; the three `.py` are the documented A/B kit) |
| `bbd/` (63), `drive/` (36), `tape/` (114), `spring/` (102) | 67/48/94/129 KB | measurement kits: `make_kit.py`, `make_scripts.py`, `analyze.py`, `*_bench.c`, `render.sh` + generated `*.txt` host scripts (58/29/107/94 files). Cited from `obv_drive.h:19,21`, `obv_tape.h:116`, PERF-BASELINE (tape `perf_*.txt`), `listen/*/README.md`. **Only `spring/regress.sh` and 5 `.txt` (spring/hot_*, worst_*, `tape/worst_voices.txt`) are run by `run_tests.sh:40`.** `bitexact.sh` (drive) is a general bit-identity tool | 18 Nov | KEEP the code; the generated `.txt` are regenerable from `make_scripts.py` → **UNSURE → D5** (≈ 0.2 MB, low value to remove) |
| `voicing/` (124 files) | 812 KB | the voicing kit (phrases, `voicekit.py`, `batch*.py`) | 18 Nov | **KEEP** (protected). Flag only: one-off diagnostics `diag05.py`, `diag09.py`, `check_5b_r2.py`, `fb24_probe.py` are not cited by any doc (`git grep` → only the kit README sections) — leave |
| `perf_callgrind.sh` | 1 KB | PERF-BASELINE.md:23, `host.c`, `tape/perf_scripts.py` | 29 Oct | KEEP |
| top-level scripts `families, map, poly, pages (no), layer_lock, drive_page, tape_page, fx_layer, bbd_page, spring_page`.txt | 1–4 KB | in run_tests (all but `pages.txt`) | 18 Nov | KEEP; **3 need their expected numbers fixed** (§2) |
| `fxhold.txt` | 171 B | not in run_tests; used by `tests/drive/bitexact.sh` default list | 3 Nov | KEEP |
| `pages.txt` | 642 B | not run; screenshot walk, no `expect`; header says **"20 pages"** (now 21) | 1 Nov | **REWRITE** (21 pages, add `expect page` lines, wire into run_tests) or DELETE — D5 |
| `programs_33_64.txt`, `save_as.txt` | 1.4 KB, 114 B | not run, not referenced anywhere (`git grep -F` → none); screenshot-only scripts for OberVave 1.5's 64-factory / save-as-slot UI | 16 Oct | **DELETE** |

### 1.9 `video/`, `listen/`, `reference-renders/`

| path | size | what / refs | last | class |
|---|---|---|---|---|
| `video/` (`song.py`, `make_video.py`, `make_short.py`, `.gitignore`, `fonts/` 4 files) | 323 KB | the **OberVave 1.2–1.4.1 promo video** pipeline. refs: `README.md:76,187-188`, CLAUDE.md:496-502 (preserved section), LICENSING.md:15 (prose). `song.py:71` `program_steps` and the kick/hat tracks drive the **step sequencer (deleted in b0fc69e, 29 Oct)**; titles are the "8-VOICE ANALOG POLY" OberVave logo (`make_video.py:204`); output `obervave-1.4.1.mp4`. Not run by anything. Fonts: Permanent Marker (Apache-2.0 text included), VT323 (OFL) | 16 Oct | **DELETE** (broken for DØG-5 and OberVave-branded; a DØG-5 clip would be a new script). Risk: if Vincent wants the video code as provenance → D3 |
| `listen/` (164 files, 14 MB on main) | 14 MB | `bbd/ drive/ spring/ tape/ trick/` measurement READMEs + PNGs (cited by CLAUDE.md §6 and firmware comments `obv_engine.h:64`); `voicing/**` README/results.json/png (cited by voicing logs/cards) | 11 Nov | **KEEP** the md/json/png (live evidence) |
| …7 WAVs under `listen/` on main (10.8 MB) | | `trick/kill_fullchain_REF.wav` 2 MB, `tapestop_{bass,chord}_APPROVED_per_voice.wav`, and 4 `voicing/…/*_held.wav` (1.5 MB each). **All 7 are also on every listen branch** (blob hashes matched on `batch-02a…06b2`). They break the "no WAVs on main except `reference-renders/`" rule | 3–11 Nov | the 4 voicing WAVs: **DELETE** (a README-cited kit file, copies on the listen branches). The 3 `trick/*.wav`: **UNSURE → D2** (the approved A/B reference `tapestop_ab.py APPROVED_DIR` expects) |
| `reference-renders/` (99 files, 147 MB) | 147 MB | approved-variant renders + README; protected | 18 Nov | **KEEP** (weight: §5) |

### 1.10 Counts

Rows of the tables in §1.1–1.9, counted by the **first** class word in each row's class cell (a row such as "KEEP + REWRITE small" counts as KEEP; the sub-items listed inside a row are not counted separately): **KEEP 45 · DELETE 10 · MOVE 4 · REWRITE 4 · UNSURE 6** (69 rows). Rows whose class is **DELETE**: `docs/MAKE-IT-YOURS.md`, `assets/logo-transparent.*`, `assets/obervave-screen.png`, `dog5-docs/_archive/`, `dog5-docs/screens/`, `BATCH-08A`, `tests/ref-sim/` (only with the gate edit), `tests/programs_33_64.txt` + `save_as.txt`, `video/`, and the four `listen` voicing WAVs. **MOVE:** `docs/API.md`, `docs/RULES.md`, `BATCH-07`, `BATCH-08B` (and the `CLAUDE.md` duplicate is a MERGE inside a KEEP row). **REWRITE:** `README.md`, `DOG-5-foundation.md`, `PERF-BASELINE.md`, `tests/pages.txt`. **UNSURE:** `SMK37.md`, `smk37-port.yaml`, the SMK tests, `docs/install/previous/`, `assets/logo.*`, `DOG-5-build-review.md`, and the sub-items under D2/D5.

## 2. The tests

### 2.1 `run_tests.sh` and its 22 FAIL lines

Baseline: `origin/main`, built the documented way (three SMK-37 builds, `--release 0.2`, plain `./build.sh` last: **`run_tests.sh:16` refuses to start unless `build/dog5.fwsc` exists**, and `./build.sh --release X` writes only `dog5-X.fwsc`, so the plain build is a required last step; README/Batch 11 did not say so). `grep -c FAIL` on the log = 23 lines: 20 `expect … FAIL` lines, 2 lines that only contain the words "UPDATE FAILED", and the closing "SOME TESTS FAILED". Batch 11's "22" is the first two groups.

| # | test (script) | lines | what it checks | why it fails | recommendation |
|---|---|---|---|---|---|
| 1–9 | DRIVE page (`tests/drive_page.txt`) | 3000 `param 54 = 0` got 46; 3500 `54 = 10` got 56; 4300 `52 = 46` got 36, `53 = 40` got 45, `54 = 10` got 56; 4600 `54 = 12` got 58, `52 = 46` got 36; 7700 `13 = 32` got 60; 8300 `54 = 14` got 60 | GROWL on KNOB 1, BIAS/TONE on SELECT held, nowhere else, FX held reaches GROWL | **stale expectation.** The script's header says "Program 1 (Red Pill): GROWL 0, BIAS 40, TONE 50, RESO 30". Batch 3A voiced Red Pill (`0745b78`, 5 Nov); `obv_patches.h:314` `PF_RED_PILL` now has `P_GROWL, 46`, `P_GRL_BIAS, 30`, `P_RESO, 58`. Every "got" is the old expectation plus the same offset (+46 GROWL, +28 RESO, −10 BIAS, +5 TONE): the *behaviour* (+2 per detent, untouched knobs stay) is right | **fix the expectation** (numbers only; or run on an INIT slot such as program 33 where the defaults are stable, so a re-voice cannot break it again — preferred) |
| 10–18 | layer-lock (`tests/layer_lock.txt`) | 3800 `13 = 30` got 58, `54 = 0` got 46; 4900/5400/6700/7200 the same pattern | FX held + HOME tap locks; lock outlives FX release; FX/ENV end it; no jump HOME | same cause (Red Pill RESO 58, GROWL 46); the page/lock logic expectations (`expect page`) all pass | same |
| 19–20 | TAPE page (`tests/tape_page.txt`) | 4100 `54 = 0` got 46; 7300 `52 = 42` got 32 | CHEW on KNOB 1; SELECT held = WOW/FLT/HISS/DROPS; map | same cause (GROWL 46, BIAS 30) | same |
| 21–22 | update-loader screen (`tests/ldr_screen_test.c`) | the section header `== … UPDATE FAILED` and the passing line `ldr_screen: UPDATE FAILED: the segments off, no percent, the way out … ok` | the loader's failure screen | **not a failure**: the line ends in `ok`; it matches only because the check text names the loader state "UPDATE FAILED" | **fix the grep, not the test**: count only lines ending in `FAIL`, or rename the check to "update error screen" |

**Verification that these are only stale numbers.** I copied the three scripts to the scratchpad, changed *only the numbers after `expect param`* (54: +46, 13: +28, 52: −10, 53 as above) and ran them on the host binary built from this tree: `drive_page`, `layer_lock`, `tape_page` → **0 FAIL, exit 0**. Files: not committed (they are test changes, a later batch).

Other things the run shows (not FAIL lines):
* `tests/ota_test.c:83` compiles with a `-Wmaybe-uninitialized` warning (`u`); harmless, 4×.
* Two lines print "skipped": stock SMK-37 packages (`SMK_STOCK_DIR` unset) and "logical image vs fm1pkg.js: skipped (needs … web/fm1pkg.js …; OberVave has no web/)": the message is stale (there *is* a `web/` now but not `web/fm1pkg.js`). **Dead check** → delete the skipped block or point it at `web/install/fm1install.js`. (UNSURE: I did not find what in `tests/install_test.py` implements it; grep for "fm1pkg.js" in that file.)
* The simulator test runs only because `tests/ref-sim/obervave.wasm` exists (§0 item 4).

### 2.2 Tests that exist but `run_tests.sh` does not run

| file | what | state |
|---|---|---|
| `tests/pages.txt` | screenshot walk of "20 pages" | stale (21 pages), no `expect` lines → REWRITE or DELETE |
| `tests/programs_33_64.txt`, `tests/save_as.txt` | screenshot scripts of OberVave 1.5's UI | referenced nowhere → DELETE |
| `tests/fxhold.txt` | FX-held hint line screenshot | used by `tests/drive/bitexact.sh` only |
| `tests/controls/bitident.sh` + `render4.txt` | Batch 9B audio-unchanged proof vs a REF commit | patch 14 now differs by design (Batch 11 §11) → one-off |
| `tests/drive/bitexact.sh REV` | general "sound byte-identical to REV" over all 32 patches + scripts | **the tool the firmware clean-up batch should use**; not a CI test (needs a REV) |
| `tests/voicing/identical.py`, `identical_par.py` | 32-patch × 52-phrase bit-identity | same; used in Batch 11 §6 |
| `tests/perf_callgrind.sh`, `tests/tape/perf_scripts.py` | CPU stand-in | documented, manual |
| `tests/bbd/`, `drive/`, `tape/`, `spring/` kits (`make_kit.py`, `analyze.py`, `render.sh`, `*_bench.c`) | measurement kits | manual; only `spring/regress.sh` is in the run |
| `tests/trick/make_kit.py`, `slop_depths.py`, `tapestop_ab.py` | listening-kit generators | manual |
| `tests/voicing/*` | voicing kit | manual (protected) |
| `tests/install/run.sh`, `tests/sim_test.mjs` | **are** run by `run_tests.sh` (the last lines) and by hand | — |

## 3. Firmware: dead code and stale comments (REPORT ONLY; no firmware file was changed)

Evidence is from the sources at `1015e4e` and a host build with `-Wall -Wextra`. **Proof recipe for the later firmware batch** (use for every item): (a) `tests/drive/bitexact.sh origin/main` and `tests/voicing/identical.py` — the host render of all 32 patches (+ the default, families, map, poly scripts) stays **byte-identical**; (b) `tools/image_diff.py` OLD NEW on `build/` — `.text`/`.data`/`.ram_text` unchanged or only smaller, functions unchanged; (c) `./build.sh --release 0.2` package: for a comments-only or dead-`static const` change the **package SHA-256 is unchanged** (dead statics are dropped by the compiler: that is the strongest proof); (d) `PATCH_BYTES 96`, `NPARAM 71` and the `"DOG5"` tag unchanged, and `build/host/obervave selftest` (99 patches round-trip) passes; (e) `run_tests.sh` same results.

### 3.1 Dead data

| item | evidence | what removing risks / how to prove |
|---|---|---|
| **43 `PF_*` arrays in `obv_patches.h`** (OberVave's base patches: `PF_DARK_ARP`, `PF_UPSIDE_ARP`, `PF_BRASS_STAB`, `PF_ARP_SEQ`, `PF_SWEEP_PAD`, … `PF_DREAM_ARP`; 76 arrays defined, 33 referenced by `FACTORY[32]` + `FACT_INIT`) ≈ **13.7 KB of the 48.8 KB file** | each name occurs once in the file (its definition); `FACTORY[NFACT]` at line 356 has 32 entries; `obervave.c:94` uses only `FACTORY` and `FACT_INIT` | zero risk to the image: they are `static const`, not emitted (package SHA unchanged proves it). Do not remove the arrays that the 32 use; keep each patch's leading comment |
| `P_CHO_RATE`, `P_CHO_DEPTH`, `P_CHO_MIX` (`obv_params.h:27-32`) | used **only by 16 of those dead arrays** (none of the 33 live arrays; checked per array) | removable together with the dead arrays; then drop the 4-line comment. SHA unchanged |
| `PF_INIT`'s relation `FACT_INIT` | live (slots 33–99) | KEEP |

### 3.2 Unused code

| item | evidence | risk / proof |
|---|---|---|
| `fmt_s`, `fmt_note` (`obervave.c:334, 341`) | `-Wunused-function` | delete; SHA unchanged (static, dropped) |
| `draw_text_box`, `cv_blit_from`, `palette_set` (`gfx.c:171, 74, 49`) | same | delete; SHA unchanged |
| `blob_load`, `blob_save` (`platform.c:250-251`), `BLOBS_AT`/`NBLOB` (8 sectors at `0xF4000`, `platform.c:127-137, 279-281`; SMK: `smk_store.h:19-20, 29, 36`) | host build warns both unused (`tests/host.c:134,140` stubs too); no caller in `src/`. **But** `BLOBS_AT..+8 sectors` is inside `FL_RANGE_OK` and the wipe loop at `platform.c:279`, i.e. it is the flash write-guard | **not free to remove**: touches which flash the device may erase. Do the function removal (static, dropped) in the first batch; treat the sector range as its own change with a flash-map review (`tests/smk_flash_test.c` pins the SMK range) — and note the browser store keeps "12 blobs … 8 pattern sectors" (`web/sim/sim.c`, `sim_test.mjs`) |
| `uint8_t pat, click` in `set` (`obervave.c:47`) | no other reference (`grep "set\.\(pat\|click\)"` → 0 in app, host, sim) | **layout**: changes the settings sector, `SET_VERSION`; leave (comment already says so) |
| `SMK_PAD_HELD` (`obervave.c:79, 404, 971`) | `#define … 0` | folds away; remove the macro and its `!SMK_PAD_HELD` terms: SHA unchanged (constant-folded) — verify |
| `tests/host.c:79 fm1_input_note_edges` | warning | host-only |

### 3.3 Stale comments (they contradict the code)

* `obervave.c:16`: "**REC taps ALLEY's time on the BBD page**" — Batch 9B removed it; REC is HOLD (`obervave.c:352` says so correctly). Rewrite the header block.
* `obervave.c:9, 15, 70-71, 374, 522, 840`: say "SEQ held" / the "SEQ/EDIT/GLO/SAVE hold-layers" — correct as button names but long-winded about a deleted sequencer; condense.
* `midi_uart.c:6-7, 44`: "routes them by channel as USB does (**seq.c**: SYNC TRS, `mclk_event`)" — `seq.c` is SLOOP's; it is not in this repo.
* `obv_params.h:27-29`: "The old names stay for obv_patches.h's base patches outside the DØG-5 32" — true until §3.1 is done, then delete.
* `obervave.c:950`: SELECT comment is accurate (LFO RATE on HOME); **no stale "SELECT is a page scroll" text found in the firmware** (the brief's example). The stale text is in the docs: `CLAUDE.obervave.md` ("PRESETS = program, ALGORITHM = CUTOFF, SELECT = page scroll…") and the README's OberVave half.
* `tests/run_tests.sh` header (lines 3–9): still "OberVave's host tests", sequencer-era wording.
* `platform.c:127`, `smk_store.h:4-8`: "OberVave's sequencer patterns" — true history of the reservation, wrong as description.
* 27 occurrences of the word "OberVave" in `firmware/src`: provenance comments (fine), `obv_*` file names (rename = noise; leave).

### 3.4 SMK-37 code paths (follow decision D1)

`BOARD_SMK37` appears in: `lcd.c` 2, `obervave.c` 8, `ota.c` 1, `platform.c` 15, `obv_engine.h` 2, `obv_smk.h` 1, `smk_store.h` 3, `hal/fm1_cc.h` 3, `fm1_flash_map.h` 4, `fm1_lcd_hw.h` 3, `loader/ldr_core.c` 1, `loader.c` 4, `tools/build.py` 2, `tests/host.c` 5, `ldr_test.c` 3, `ota_test.c` 1, `smk_flash_test.c` 3, `smk_ui_test.py` 2. Dedicated files: `obv_smk.h`, `smk_store.h`, `smk_wheel.h`, `hal/smk_input.h` (47.6 KB of source). Removing it **removes a shipped feature** (three packages: Pro, Elite, MKE-P37) and the flash-map checks; the FM-1 package would need the proof (a)–(e) above plus `run_tests.sh` minus the SMK lines. DØG-5's panel was designed for the FM-1; the SMK pads were OberVave's sequencer (`obv_smk.h:18, 154`: "pads are free"), so on an SMK DØG-5 ships a dead pad grid and an untested mapping.

### 3.5 Parameters and pages

* `NPARAM 71`; bytes 71–79 free by design (`obv_params.h:35-37`). No parameter id is unused: a script over the enum found every `P_*` referenced by the engine, UI, patches or params table. No change.
* The 21 pages are all reachable (`tests/families.txt`, 43 `expect page`).

## 4. Branches

`git ls-remote --heads origin` → **16 heads** (the brief expected about 41). No `voicing/*` branch exists any more (the merged PRs #20, #21 … were deleted at some point); only `build/`, `listen/`, `claude/` and `main`. Merged = `git merge-base --is-ancestor <tip> origin/main`. Tree sizes are `git ls-tree -r -l` of the tip; "only copy" = WAV blobs (by hash) found on **no other** listen branch and not on main. One tag: `build-deps-v1` (the toolchain + SDK release assets `get_vendored_deps.sh` downloads — **keep**).

| branch | last commit | merged into main? | what it holds | recommendation |
|---|---|---|---|---|
| `main` | 18 Nov | — | — | — |
| `build/batch-08a-web-player-check` | 13 Nov | yes (PR #24), ahead 0 | Batch 8A report | **can go** |
| `build/batch-08b-web-player` | 13 Nov | yes (PR #25), ahead 0 | the web player | **can go** |
| `build/batch-09b-controls` | 18 Nov | yes (PR #26), ahead 0 | the control surface | **can go** |
| `build/batch-11-test-build-0.2` | 18 Nov | yes (PR #27), ahead 0 | the 0.2 build | **can go** |
| `claude/peaceful-planck-6oikap` | 18 Nov | yes, tip = `1015e4e` = main | an earlier cloud session's working branch | **can go** (nothing ahead); the current harness may re-create it, say so if you delete it mid-session |
| `build/batch-12a-cleanup-inventory` | now | no (this report) | this file | merge or delete after you read it |
| `listen/batch-02a-weight-and-space` | 4 Nov | no | **429 MB tree, 365 WAVs, 332 only here (357 MB):** the DRIVE / BBD / SPRING / TAPE measurement WAVs (`listen/bbd` 47, `drive` 22, `spring` 64, `tape` 44), `listen/trick` + `slop_depths`, batch-01a variants (04 V-Sync, 25 Sawtooth, 30 The Dog + round 2, 31 Fifth), 03 Half-Life, batch-02a (09 Skeenhead, 11 Slapback Strut, 17 Titanic, 21 Cowl Shadow, round 2) | **keep — the only copy** of the Psych Chain measurement WAVs and all of batch 01a–02a's rejected variants |
| `listen/batch-03a-chapter1-fat-and-driven` | 5 Nov | no; **orphan root** `e86c7cb` (no merge base with main) | 80 MB, 61 WAVs, **49 only here**: 01 Red Pill, 02 Cement Grind, 06 zzuFuzz, 08 Wire Bite variants | keep (only copy) |
| `listen/batch-03b-chapter1-wreck-and-chop` | 5 Nov | no; orphan root | 85 MB, 68 WAVs, **56 only here**: 05 ZEAROX (+ round 2), 07 Tape Splice, 15 Trem Chop | keep (only copy) |
| `listen/batch-04a-chapter2-organ-kelp-wash` | 6 Nov | no; orphan root | 43 MB, 23 WAVs, **16 only here**: 10 Atlantic Swell, 12 Kelp Tangle, 16 Tidal Pull | keep (only copy) |
| `listen/batch-04b-chapter2-ghost-and-reef` | 6 Nov | no; orphan root | 54 MB, 26 WAVs, **21 only here**: 13 Ghost Board (+ round 2), 14 Reef Break | keep (only copy) |
| `listen/batch-05a-chapter3-drones` | 6 Nov | no (4 ahead) | 325 MB tree, 181 WAVs, **105 only here (195 MB)**: 18 Roto-scopo, 19 Blackwater, 19 Micro-mist (rounds 1–2), 22 Melting Orb | keep (only copy) |
| `listen/batch-05b-chapter3-fire-dust-fugue` | 6 Nov | no | 228 MB, 139 WAVs, **56 only here**: 20 Fire & Ice, 23 Crypt Dust (+ round 2), 24 Fugue State | keep (only copy) |
| `listen/batch-06a-chapter4-sync-bass-wash` | 11 Nov | no | 216 MB, 146 WAVs, **54 only here**: 26 BSyncA, 27 R3V3RT, 29 Valhalla | keep (only copy) |
| `listen/batch-06a2-i-scream` | 11 Nov | no | 197 MB, 117 WAVs, **23 only here**: 29 i scream (A–D, calibrations, the approved D) | keep (only copy) |
| `listen/batch-06b-bell-init` | 11 Nov | no | 214 MB, 123 WAVs, **18 only here**: 28 Bell Tolls and 32 Init bruv? round 1 | keep (only copy) |
| `listen/batch-06b2-bell-clean` | 11 Nov | no | 279 MB, 150 WAVs, **45 only here (99 MB)**: 28 Bell Tolls round 2 (A, B2, C2, D2, B1/C1/D1, six calibrations) + 1 file in `reference-renders/` | keep (only copy) |

* **Plainly redundant:** none. Every `listen/` branch has at least 16 WAVs found nowhere else.
* **Structure note (judgment, nothing to delete):** the later listen branches (05a … 06b2) each carry the full `tests/`/`firmware/` tree plus all earlier kits' WAV files, which is why a clone is 686 MB (`size-pack`). The orphan roots (03a–04b) are WAV-only. A future clone-weight fix is *not* deleting these branches: it is a shallow/partial clone for working sessions (`git clone --filter=blob:none`) and, if you ever want, moving the listen WAVs to a Release asset (not done, not recommended without asking).
* **Merged `build/` and `voicing/` branches that can go:** the four `build/batch-*` branches above plus `claude/peaceful-planck-6oikap`. There are no `voicing/` branches left to delete.
* Not determined: whether other branches existed (the "~41") and were already removed; GitHub's PR list was not queried.

## 5. Repo weight

* `.git` pack: **685.8 MiB** (`git count-objects -vH`). Working tree tracked: **166.9 MB** (`git ls-tree -r -l`). Tracked WAV: **105 files, 154.3 MB** (92 % of the tree).
* Ten biggest tracked files (all WAV, all in `reference-renders/`): `28-are-two-d2_D2_held.wav` 5.48 MB; `18-roto-scopo_D_drone-A1.wav` 3.30; `22-melting-orb_D_drone-A2.wav` 3.30; `18-roto-scopo_D_drone-A2.wav` 3.30; `29-i-scream_D_melody-C#6.wav` 3.16; `16-tidal-pull_D_wash.wav` 2.96; `14-reef-break_C_crash.wav` 2.96; `13-ghost-board_C2_ghost.wav` 2.96; `14-reef-break_C-0.2_crash.wav` 2.96; `28-are-two-d2_D2_register.wav` 2.79.
* By top-level dir (tracked KB): `reference-renders` 147 481, `listen` 15 754 (10.8 MB of it WAV), `docs` 2 193 (two 612 KB `.fwsc` + the 860 KB installer page), `tests` 1 637, `dog5-docs` 1 451, `assets` 864, `firmware` 855, `video` 323, `web` 95, `tools` 93.
* **Large and not needed (candidates):** `listen/` WAVs on main 10.8 MB (copies exist, §1.9); `video/` 323 KB; `tests/ref-sim/` 283 KB; `docs/install/previous/` 612 KB (UNSURE); `docs/install/index.html` 860 KB is generated and needed. The dry-run deletion removes **34 files, 7.7 MB** (tracked); the UNSURE items would add 4.7 MB (the three `listen/trick` WAVs) and 0.6 MB (`docs/install/previous/`). It does **not** shrink `.git` (history keeps everything). The weight is `reference-renders/` (protected) and the listen branches (never deleted). If clone size matters, the lever is `reference-renders/` (fewer phrases per patch), which is a decision, not a clean-up: D7.

## 6. The dry run

Throwaway worktree: `git worktree add --detach <scratchpad>/wt origin/main`, then `git rm`/`git mv` of **everything classified DELETE plus the pure MOVEs and the two edits that make the deletes safe**; nothing was committed, the worktree was removed afterwards.

**Applied (36 paths touched, 34 deleted = 7.7 MB, 2 moved, 2 edited):**
`tests/ref-sim/` (6) · `video/` (8) · `dog5-docs/_archive/` (3) · `dog5-docs/screens/` (6) · `dog5-docs/BATCH-08A-WEB-PLAYER-CHECK.md` · `docs/MAKE-IT-YOURS.md` · `assets/logo-transparent.{png,svg}`, `assets/obervave-screen.png` · `tests/programs_33_64.txt`, `tests/save_as.txt` · the 4 `listen/voicing/**/*_held.wav` · **moved** `docs/API.md` → `dog5-docs/PLATFORM-API.md`, `docs/RULES.md` → `dog5-docs/CHIP-RULES.md` · **edited** `tests/run_tests.sh` (`tests/ref-sim/obervave.wasm` → `docs/play/dog5.wasm` in the simulator gate) and `CLAUDE.md` (cut the duplicated preserved section, lines 385–640). **Not** applied (UNSURE or REWRITE, no effect on a build): SMK-37, `docs/install/previous/`, `assets/logo.*`, README/LICENSING text edits, the 3 `listen/trick` WAVs, any firmware change.

| step | result |
|---|---|
| `tools/get_vendored_deps.sh` | worked (toolchain 20260730.1 + SDK AC79NN_SDK_V1.2.1 from the `build-deps-v1` release) |
| `./build.sh --release 0.2` (after three SMK-37 builds) | `build/dog5-0.2.fwsc`, 612223 B, `FM-1_962`; checks `-Os`, no 64-bit division, `image 82352 B of 581564; RAM 32432 B of 98304; pool 304896 B of 344064` all ok |
| **package SHA-256** | **`b2be33a96864349ab155d7c29b3b3ccbe86ba0b38369289bb54995ab3da36b96` = the `origin/main` build = the package embedded in `docs/install/dog5-0.2-20261118.fwsc` = Batch 11 §8**. Also identical on `main` vs dry run: `dog5.fwsc` (`8f0e4a49…`), `dog5-smk37.fwsc` (`226a8dd1…`), `-elite` (`9e570fe0…`), `-mke` (`80f66c6b…`) |
| `tests/run_tests.sh` | rc 1 as on `main`. The `FAIL` lines: **identical set** (sorted `diff` of `grep FAIL` between the `origin/main` run and the dry run = empty; 23 lines incl. "SOME TESTS FAILED" = 20 + 2 + 1; the ok-line sets are identical too). The browser-simulator section **ran and passed** with the gate change (`SIM TEST PASSED`, program 1 bit-identical to the host render, 0 differing pixels) |
| `sh tests/install/run.sh` | rc 0, `20/20 checks passed`, 1203 replies served, page resumes after the cut-off |
| `node tests/sim_test.mjs` | rc 0, `SIM TEST PASSED` |
| `python3 tools/make_installer_page.py --check` | rc 0, `in sync: dog5-0.2-20261118.fwsc (FM-1_962) and index.html regenerate byte for byte from web/install` |
| `web/sim/build.sh` (installed zig via `pip install ziglang` and `npm install binaryen` in `~/.local/share/obervave-wasm`, as the script instructs) | rc 0; `docs/play/dog5.wasm` 96165 B is **byte-identical to the one on `origin/main`** (`cmp`), `patches.json` unchanged, `git status docs/play` clean; sim test passes against it |

**Failures the deletion caused: none**, with one dependency found and fixed: **`tests/ref-sim/` cannot be deleted alone.** Without the gate edit `run_tests.sh:102` evaluates `[ -f tests/ref-sim/obervave.wasm ]` false and prints "(no node or no tests/ref-sim/obervave.wasm: the browser simulator's test is skipped)" — the test would vanish from the run without a FAIL. So `ref-sim` is DELETE **only together with** that one-line gate change. Nothing else depended on any deleted item (greps in §1). `video/` imports `tools/make_logo.py` (not the reverse); nothing imports `video/`.

## 7. Proposed final tree (after the clean-up, SMK-37 kept as it is)

```
CLAUDE.md                  brief only, ~385 lines (the duplicate removed, §9 and §12 fixed)
README.md                  DØG-5 only: status, install, build, credits (REWRITTEN)
LICENSE  NOTICE  LICENSING.md      (LICENSING rows fixed)
build.sh  .gitignore  .github/workflows/release.yml
SMK37.md  smk37-port.yaml          (UNSURE D1: rewritten for DØG-5, or removed with the variant)
assets/    logo.svg logo.png (D6)  fonts/ter-u16n.bdf  fonts/Terminus-LICENSE.txt
docs/      index.html  install/ (page + package + README [+ previous/ D4])  play/
dog5-docs/ DOG-5-*.md (9 live)  PERF-BASELINE.md (refreshed)  CLAUDE.obervave.md (the one copy)
           PLATFORM-API.md  CHIP-RULES.md  BATCH-09B-CONTROLS.md  BATCH-11-TEST-BUILD-0.2.md
           BATCH-12A-CLEANUP-INVENTORY.md  history/ (BATCH-07, BATCH-08B)  voicing/ (README, 24 logs, cards/)
firmware/  src/ hal/ loader/ gen/ crt0.S app.ld      (dead code removed in its own batch, §3)
listen/    bbd drive spring tape trick (md + png)  voicing/ (md, json, png)   [WAVs on listen/ branches only]
reference-renders/         approved-variant renders + README
tests/     run_tests.sh run_host.sh host.c sim_test.mjs install/ controls/ trick/ voicing/
           bbd/ drive/ spring/ tape/ (kits)  smk* (D1)  *.txt (scripts, expectations fixed)  *_test.c/py
tools/     build.py fm1_install.py fm1pkg_make.py gen_*.py get_*.sh image_diff.py lz4blk.py make_*.py
web/       install/  sim/
```
(`video/`, `tests/ref-sim/`, `dog5-docs/_archive/`, `dog5-docs/screens/` are gone.)

### Decisions Vincent must make

* **D1 — SMK-37 variant (the biggest).** Keep or remove? It still builds (three packages in `release.yml`), passes its host tests, and is DØG-5 in name only: `SMK37.md` and `smk37-port.yaml` are OberVave documents with stale identities and a pad grid that was the deleted sequencer; no one has flashed a DØG-5 build on an SMK-37 (that I can find in the repo). Keeping costs: 47.6 KB of SMK source, 14 firmware files with `#if`, 5 test files, 4 run_tests blocks and three CI builds that DØG-5 never tests on hardware. Removing it **removes a shipped feature** and is a firmware batch with the §3 proof. My recommendation (judgment): **freeze, do not ship**: keep the code for now, stop building/publishing the three SMK packages in `release.yml`, rewrite `SMK37.md` to a 5-line "not supported in DØG-5 v0.x" note, and remove the code in the firmware clean-up batch after v0.2 is verified on the unit. Say if you want it kept as a real target instead.
* **D2 — the three `listen/trick/*.wav` (4.7 MB, "APPROVED per voice" tape-stop references and `kill_fullchain_REF`).** They are the `APPROVED_DIR` input of `tests/trick/tapestop_ab.py` and also on every listen branch. Keep on main (small, the rule's one honest exception) or move to the branch only?
* **D3 — `video/`.** Delete (broken: drives the deleted sequencer; OberVave logo/title) or keep as provenance of the upstream video? Its two fonts' licence texts go with it; if kept, add LICENSING.md rows for Permanent Marker (Apache-2.0) and VT323 (OFL).
* **D4 — `docs/install/previous/dog5-0.1-20261112.fwsc` (612 KB).** Nothing reads it; v0.1 is also in git history. Keep as a public rollback file or delete?
* **D5 — measurement-kit leftovers and history docs:** `tests/controls/bitident.sh`+`render4.txt`, `tests/pages.txt`, the generated `tests/{bbd,drive,tape,spring}/*.txt` (0.2 MB, regenerable), `DOG-5-build-review.md`, `BATCH-07`/`08B` → `history/`. All small; defaults in the table are my recommendation.
* **D6 — logo and splash.** `assets/logo.*` and `firmware/gen/obv_splash.h` are still the OberVave wordmark; the DØG-5 wordmark is Stage 4. Keep until then (and `LICENSING.md:26` stays).
* **D7 — `reference-renders/` 147 MB.** Protected, so out of this clean-up; say if you want the weight cut (e.g. one phrase per patch) in a separate batch.
* **D8 — GitHub Pages scope.** Moving `API.md`/`RULES.md` off `docs/` changes two public URLs; confirm that is fine, and whether Pages should publish only `/install/` and `/play/`.
* **D9 — branches:** approve deleting the five merged branches in §4 (the four `build/batch-*` and `claude/peaceful-planck-6oikap`).

## 8. What I could not determine

* **GitHub Pages settings** (source, Jekyll on or off), and whether anything outside the repo links to `docs/*.md`, `docs/install/previous/…` or `docs/play`.
* **The ~41 branches:** only 16 exist on the remote; I did not query PRs or forks.
* Whether any DØG-5 build has been flashed on an SMK-37 (nothing in the repo says so; Batch 11 §0 and README say the FM-1 only).
* Which `tests/install_test.py` check prints "logical image vs fm1pkg.js: skipped" (I did not read it; the message names a `web/fm1pkg.js` that does not exist).
* Device behaviour of anything: nothing here touches the device.
* Whether the 43 dead patch arrays / `P_CHO_*` removal leaves the package SHA unchanged: that is a prediction from "static const, unreferenced"; it needs the build in the firmware batch. Likewise the `SMK_PAD_HELD` fold.
* The 20 stale expectations: I proved the three scripts pass with new numbers on the host build; I did not commit those edits (a later batch).
