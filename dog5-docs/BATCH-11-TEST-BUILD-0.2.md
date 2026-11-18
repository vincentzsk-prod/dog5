# Batch 11 — test build 0.2 (Reef Break attack, version bump, installer)

Branch `build/batch-11-test-build-0.2`, off `main` (Batch 9B merged). Everything below is measured on the host build; **nothing was auditioned** (Vincent chose to hear the change on his unit). Claims are from the code (file:line) or marked *inference*.

## 0. Things you should know first

**Correction (merge of Batch 9B).** The first version of this report was built on a stale local `main` (Batch 8B, `7a1fba8`); the Batch 9B merge (`b673521`, with `dog5-docs/BATCH-09B-CONTROLS.md` and `tests/controls/`) was only on `origin/main`. I fetched, confirmed the 9B merge is on `origin/main`, merged `origin/main` into this branch (merge commit `562ffa9`; the only conflict was the generated `docs/play/dog5.wasm`, rebuilt) and redid every step that depends on the firmware. All figures below are from the merged tree and a fresh `origin/main` (9B) checkout as baseline. The earlier "9B figures do not match main" note was this staleness, not a brief error: image / RAM now equal the 9B figures.

1. **`firmware/src/dog5_id.h` did not need an edit, and I did not touch it.** The brief says it holds `FM-1_961`. It holds only the family `#define DOG5_ID_FM1 "FM-1_96"` (`dog5_id.h:19`); the minor digit comes from `tools/build.py` and `--release X.Y` (`build.py:74`, `:339-345`). `./build.sh --release 0.2` alone gives `FM-1_962`.
2. **`make_installer_page.py` deletes older `dog5-*.fwsc`** (its `for old in out.glob("dog5-*.fwsc"): old.unlink()` loop), and both `--check` and `tests/install/run.sh` require exactly one such file beside the page. The script ran, then the 0.1 package (byte-identical, SHA `3de092d5…87f6a`) was put back at **`docs/install/previous/dog5-0.1-20261112.fwsc`**. That moves it from the old path; if you want it at the old path, the installer check has to change instead. Your call.
3. **VOLUME had to change** (121 → 116), see §2.

## 1. Table check: 82 → 299 ms, both envelopes

* `firmware/gen/obv_tables.h:98` `TIME_MS_X10[128]`; element 82 = **2992** (parsed from the header: 128 entries, [81] = 2768, [83] = 3235).
* `FILTER ENV ATTACK` is `P_FA` and `AMP ENV ATTACK` is `P_AA`, both `K_MS` (`obv_params.h:86, 90`); `K_MS` display is `fmt_ms(s, TIME_MS_X10[v & 127])` (`obervave.c:235`) and `fmt_ms` for 1000 ≤ x < 10000 prints `x/10` + "ms" (`obervave.c:208`) → 2992/10 = **"299ms"** for both. (`P_AA` has a CC number 73 column only; no special display.) Confirmed; did not stop.
* Old values: 0 → `TIME_MS_X10[0]` = 5 (0.5 ms); 52 → 288 (28.8 ms).

## 2. The array diff (`firmware/src/obv_patches.h`, `PF_REEF_BREAK`)

```
-    ... P_FTYPE, F_HP12, P_FA, 0,
-    P_FD, 100, P_FS, 0, P_AA, 52, P_AD, 97, P_AS, 0, P_AR, 97, P_VOLUME, 121, ...
+    ... P_FTYPE, F_HP12, P_FA, 82,
+    P_FD, 100, P_FS, 0, P_AA, 82, P_AD, 97, P_AS, 0, P_AR, 97, P_VOLUME, 116, ...
```
FILTER ENV A 0 → 82, AMP ENV A 52 → 82, VOLUME 121 → 116. The patch's leading comment gets a Batch 11 note (comment only). No other array changed.

**VOLUME:** with 82 / 82 and VOLUME 121 the own-phrase peak was **−3.56 dBFS** (over the −4 limit), RMS −17.33 (in range). Sweep (own-phrase peak = worse of two noise seeds, crash-phrase RMS): 121 −3.56 / −17.33; 120 −3.68; 119 −3.80; 118 −3.92 / −17.75; 117 −4.05 / −17.89; **116 −4.17 / −18.03**; 115 −4.30 / −18.18. I chose 116, the kit's standing margin (`batch04b.py own_peak` loop trims until ≤ −4.2); 117 would pass the −4 limit by 0.05 dB only. VOLUME only, nothing else changed.

## 3. Before / after (crash phrase `u_crash` and the Batch 4B measures; kit `tests/voicing/batch11.py`, `batch11_bands.py`)

| measure | before (A0 / A52, VOL 121) | after (A82 / A82, VOL 116) |
|---|---|---|
| RMS over the 11 300 ms gates (ref −18.0 ± 1.5) | −18.02 | **−18.03** |
| own-phrase peak (limit −4) | −4.53 | **−4.17** |
| second noise seed: peak / RMS | −4.30 / −18.00 | −4.77 / −18.07 |
| crest (seed 1 / 2) | 13.5 / 13.7 dB | 13.9 / 13.3 dB |
| samples within 10 % of the rail | 1.9 % | 2.2 % |
| phrase (b) (3 keys) RMS / peak | −12.84 / −1.55 | −16.95 / −2.82 |
| time to 10 / 50 / 90 % of peak, A1 voice alone | 2.2 / 8.7 / 27.2 ms | 25.2 / 126.2 / 208.0 ms |
| time to peak A1 / A2 | 27.4 / 32.2 ms | 208.3 / 267.9 ms |
| A2: 10 / 50 / 90 % | 2.7 / 12.2 / 32.2 ms | 24.4 / 112.7 / 258.4 ms |
| first echo repeat vs the dry note's peak | −13.2 dB | −13.2 dB |
| repeat time after onset | 391 ms | 620 ms |
| repeats −13 / −18 / −24 / −28 / −31 / −35 | same list | −13 / −18 / −23 / −26 / −30 / −33; repeats above −40 dB: 7 → 8 |
| isolated hit with echo: peak, clipped samples | −5.3 dBFS, 0 | −6.0 dBFS, 0 |
| dry tail 20 / 40 dB after gate | 590 / 1244 ms | 588 / 1284 ms |
| with echo 20 / 40 / 60 dB, last > −60 dB | 684 / 1462 / 1848, 5190 ms | 728 / 1472 / 1868, 4702 ms |
| noise vs sub, first 100 ms (A1 / A2) | +4.7 / +3.5 dB | +15.6 / +12.4 dB — *window now inside the attack ramp; not comparable* |

## 4. Crash character, in numbers

Per band, ms **after the note-on** (11.6 ms frames, dry voice, A1 hit): peak time / time to fall 20 dB / 40 dB below its own peak.

| band | before pk / −20 / −40 | after pk / −20 / −40 |
|---|---|---|
| 60–150 | 23 / 102 / 273 | 235 / 308 / 316 |
| 150–400 | 32 / 238 / 308 | 267 / 311 / 328 |
| 400–1.2k | 67 / 311 / 345 | 250 / 331 / 366 |
| 1.2k–4k | 29 / 345 / 885 | 276 / 435 / 1120 |
| 4k+ | 46 / 711 / 1376 | 255 / 923 / 1622 |

A2 (4k+): −20 / −40 at 723 / 1422 → 967 / 1654 ms; lowest band 250 / 305 → 311 / 319. (Counted from each band's own peak the old card's figure "4k+ 665 / 1329 ms" becomes 668 / not reached in the 1.5 s window, because the peak moved to ~255 ms; absolute times above are the comparable ones.)

**Does the identity hold?** By these numbers yes: the bands still fall in order lowest first (−40 dB at 316 < 328 < 366 < 1120 < 1622 ms) and the 4k+ band rings longest (−40 dB 1622 ms vs 1376 before). What changed: all bands now *peak* at 223–276 ms instead of 23–67 ms, so the lows no longer start the hit and then fall; they rise and fall inside about 80–130 ms around the end of the 300 ms gate. Band energy by window (dB re the loudest band-window): first 50 ms, 60–150 Hz −6 → −74, 4k+ −1 → −21; 150–400 ms, 60–150 Hz −28 → −9, 4k+ −1 → 0. Sub-only hit (noise 0), first 150 ms: under 60 Hz 41 % → 2.7 %, 60–150 Hz 28 % → 3.8 %. *Inference (not isolated):* the high-pass starts at its full CUTOFF 100 at the strike because the filter envelope (which pushes it down through the negative ENV AMT) now starts at 0 and climbs over 299 ms, so the lows arrive only as it opens. I did not render a variant to separate the filter attack from the amp attack.

## 5. Card and render

* `dog5-docs/voicing/cards/14-reef-break.md` updated: states plainly the change was made on Vincent's instruction after he found the old attack too harsh and that **the new version was not auditioned before merge**; keeps the old values as history (FILTER ENV A0, AMP ENV A52, VOLUME 121) beside the new ones; before/after figures marked as such; §2 has no numbers, gear names only in §3.
* Added `reference-renders/14-reef-break_C-0.2_crash.wav` and `_stabs.wav` (rendered through program 14 on this branch, cut at 2.9 s like the earlier ones; crash level −18.03 / peak −4.17, stabs −16.95 / −2.82). The old `14-reef-break_C_*.wav` stay as the approved old-attack history. *Naming:* I used `C-0.2` (C = the approved variant, 0.2 = the build) because the folder's names are variant letters; the README's "approved variants only" rule does not literally cover an unheard variant — flagging, your call.
* Not edited: `dog5-docs/voicing/14-reef-break.md` (the log; its status line still says approved C, old attack) and earlier BATCH reports. Not re-measured: host instr/sample cost (no code changed) and the program-load bit-identity check for slot 14.

## 6. The 32-patch comparison

`python3 tests/voicing/identical.py <fresh origin/main (9B) checkout> 14`: **patch bytes: 31 of 32 slots identical (slot 14 differs)**; **audio: 31 of 31 other slots byte-identical on all 52 phrases (the kit's full phrase set); slot 14 differs: True.** `OK`. The before / after measurements of §3 and §4 were re-run on the merged tree: same numbers (9B did not change the sound).

## 7. Version label

Driven by `build.py --release` (`-DFELUCCA_ID`, `-DAPP_VER`, `build.py:184`); the header, the loader screen and the web player need no edit: `dog5_id.h` has no version, `web/sim` and `docs/play` contain no version string, `loader/ldr_screen.c` shows the name only (`DOG 5`). Found and changed (labels the build does not drive):

* `README.md`: status line (12 Nov, v0.1, `FM-1_961` → 18 Nov, v0.2, `FM-1_962`), the `fm1_install.py docs/install/dog5-0.1-20261112.fwsc` path, the `--release 0.1` build and installer commands.
* `docs/install/README.md`: package name + identity (line 4), the expected-identity line (23), the rebuild commands (89–90).
* `docs/install/index.html`: regenerated by the script (v0.2 · 2026-11-18, package name, SHA, `FM-1_962`, 612223 B).
* `web/install/fm1install.js:163` and `index.html:268` only carry the example `"FM-1_960"` in a comment: left.
* Left alone as history: `dog5-docs/DOG-5-base-and-ui-decisions.md:456-462` (the Batch 7 record of v0.1), `tests/smk_wheel_test.c`, other "0.1" numbers (not versions).

## 8. Package

`./build.sh --release 0.2` on the merged tree: **`build/dog5-0.2.fwsc`, 612223 B, SHA-256 `b2be33a96864349ab155d7c29b3b3ccbe86ba0b38369289bb54995ab3da36b96`**, identity `FM-1_962`. Built twice: identical hash.

| | 9B figure | `origin/main` (9B), `--release 0.2` | this branch |
|---|---|---|---|
| image | 82352 B | 82352 B | 82352 B |
| RAM .data+.bss | 32432 B | 32432 B | 32432 B |
| pool | 304896 B | 304896 B | 304896 B |
| package | — | 612223 B, SHA `745630ca…c195` | 612223 B, SHA `b2be33a9…6b96` |

Only the patch bytes differ from 9B's package (same size). Build checks passed (`-Os`, no 64-bit division, register access in `hal/` only).

## 9. Installer page

`python3 tools/make_installer_page.py --release 0.2 --date 2026-11-18` (re-run after the merge) wrote `docs/install/dog5-0.2-20261118.fwsc` (612223 B, identity FM-1_962, SHA as in §8) and `docs/install/index.html` (860438 B); it deleted nothing new (the 0.1 file is already under `previous/`); `README.md` is hand-edited (§7). `--check`: in sync. `sh tests/install/run.sh`: "embedded package SHA-256 == Python's", "every reply the page sent matched the reference frame, 1203 replies served", 20/20 page checks. This is the existing frame-identity check against `fm1_install.py`.

## 10. Web player

`sh web/sim/build.sh` rebuilt `docs/play/dog5.wasm` (96165 B) from the merged tree (the merge's own `.wasm` conflict was resolved this way); `patches.json` unchanged. `node tests/sim_test.mjs`: **SIM TEST PASSED** (sound = the host build's sample for sample, screens identical). That sound check runs program 1, so slot 14 is covered by §6.

## 11. `tests/run_tests.sh`

Fresh `origin/main` (9B) checkout: 22 FAIL lines. This branch: **22 FAIL lines, the identical set** (sorted `diff` empty), nothing new. Both trees were built the documented way (three SMK-37 builds, FM-1 last). The 9B tests are in the run and produce no FAIL line: `tests/controls/edit_keys.txt`, `select_dial.txt`, `rec_hold.txt`. The 22 lines sit in the DRIVE page (9), layer-lock (9), TAPE page (2) and update-loader screen (2) tests, as on `main`. Not run: `tests/controls/bitident.sh` (it compares patches 03, 14, 28, 30 against a reference and 14 now differs by design; §6 covers the 31 others).

## 12. Surprising / open

* The identity header and the "9B figures" premises of the brief were both off (§0.1, §0.2).
* The installer script's delete-old-package behaviour conflicts with "do not delete" (§0.2).
* The slower attack moves the sub to the end of the gate: with a 300 ms gate the lows are barely there before the release starts (their −20 dB points are 308–311 ms). Short staccato playing will give a more top-heavy hit than the old one; I measured only the 300 ms gate.
* Not done: any listening; any device run.
