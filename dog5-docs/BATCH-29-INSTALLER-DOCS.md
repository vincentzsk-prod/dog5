# Batch 29 — the installer in a background tab, "Sound design notes", the manual's bullets, the art docs re-skin

**23 Nov 2026**, branch `build/batch-29-installer-docs` from `origin/main` 3ce669b (Batch 28 merged). **No firmware
code changed**: the 0.4.5 package is byte-identical (`ba176660…96a3`, `FM-1_3645045`).

## 1. The failed install (UPDATE FAILED on the unit)

Vincent installed 0.4.5 from the installer page and switched to another browser tab during the upload, for the first
time. The unit showed the loader's **UPDATE FAILED / INSTALL AGAIN** screen. Nothing was damaged: the loader keeps
waiting, and the page's Resume serves the package again.

**Cause (from the code, not reproduced):** the page waits 10 ms before each of about 1,200 replies
(`fm1install.js`, `DELAY.reply`) with `setTimeout`. Chrome slows a background tab's timers to about once a second, and
after a while to about once a minute. The loader asks for each piece up to three times, 5 s apart (`ota.c`,
`ota_read`), then gives up: `ldr_session` fails and `ldr_failed()` draws UPDATE FAILED. Nothing in 0.4.5 or the new
identity is involved (the loader always answers as `ota-FM-1_900`, which the page's `OWN_LOADER_RE` accepts).

**Fix (`web/install/index.template.html`, page regenerated):**
- waits of 20 ms or less (the per-reply wait) watch the clock instead of a timer, so no throttling can stretch them;
- longer waits (the few of 1–3 s) and the read timeouts run on a dedicated worker's timer (`FM1.setSleep`, the hook
  that was already there);
- the screen is kept awake while installing (Screen Wake Lock, where the browser allows it);
- if the tab goes to the background during an install, a warning box asks to bring it back and says what to do if the
  unit shows UPDATE FAILED; the log records it;
- the checklist line now says the tab stays in front until it says Done; the manual (1.10) says the same.

**Proof:** `tests/install/run.sh` 21/21 (a new check: the page's timers run in a worker). **Not proved:** behaviour in
a real background tab. Headless Chromium always reports the page as visible, so throttling can't be reproduced here;
the next real install with the tab in the background is the test (backlog 1.11). Whether Chrome also slows a background
worker's timers is not settled by what I could find, which is why the per-reply wait uses no timer at all.

The accidental cut-off doubles as the Hub's "interrupt an install, then resume it" test (backlog 1.2) once Vincent's
resume reports `FM-1_3645045`.

## 2. "How to play it" → "Sound design notes"

Vincent's call. Renamed in all 32 voice cards (section 4), the cards README, the web player's card heading, the
generator's comment, and every entry of Driver Manual Part 3 (Project and repo copies). The player and the manual page
were rebuilt.

## 3. The Driver Manual's bullets

Every bullet list in Parts 0–4 read for need and order. Changed (Part 0–2, Project and repo):
- Part 0: the two rules lose their dev-history parentheses.
- 1.1: the map note no longer says "since v0.2" and points out the two left-out rows are in the table. 1.3: "(Tap-toggle.)"
  removed (it repeated "press again to resume").
- 1.4: the per-voice line said "a 24 dB low-pass filter" and "an LFO"; the filter has six types (pointer to TYPE in
  1.7) and the LFO is one per patch, now its own bullet. The bank bullet drops the test-history note (1.9 has it).
- 1.9: saves keep their scene now comes before randomise (saving first, the dice after).
- 1.10: keep the installer tab in front; Resume as it now stands.
- Part 2 Dirt & aggression: **Clean** first; **Dust** moved after Gritty (it was first, before Clean).
- Parts 3–4: every entry has the same two parts in the same order (checked by script); no bullet changed.

**Left for Vincent (backlog 1.12):** Parts 2–4 carry a lot of internal voicing detail (dates, variants, host
instr/sample, dB readings). It is consistent, but heavy for a public page. Keep it, or move the measurements to Part 5.

## 4. The art docs re-skin (backlog 1.9)

- **Repo copies** (`dog5-docs/`): an **AS BUILT** box at the top of the character brief, build kit, chapter specs, art
  direction and presets (ACID CAN, no bin / washing line / cat, the screen is painted not one-spot, colours as built,
  the dial readout, the fence as built, controls as built, what is not built), and the stale names in their tables and
  headings (Le Gato → ACID CAN, the long chapter titles, VALHALLA → i scream, magenta / amber marked superseded).
- **The Gemini prompts** (`DOG-5-field-prompts.md`) moved to `dog5-docs/history/` with a note: nothing from them ships;
  the art is hand-painted (no AI art).
- **Project:** its art docs are the long Oct versions (different from the repo's), so instead of rewriting five large
  docs the Project gets one overlay, **`DOG-5-art-as-built.md`**, and the INDEX sends every art read through it.
  `narrative-library` and `asset-library` are left for Vincent to delete if he wants.

## Tests

A plain `./build.sh` (identity `FM-1_3645000`), then `sh tests/run_tests.sh`; `node tests/sim_test.mjs`;
`make_installer_page.py --check` and `make_manual_page.py --check` in sync. **ALL TESTS PASSED**, SIM TEST PASSED, installer 21/21, both pages in sync.
