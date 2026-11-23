# Batch 31 — v0.5, the release candidate (COLLAR, credits to ZIGGY, fmhub author)

**23 Nov 2026**, branch `build/batch-31-v0.5` from `origin/main` eaf5464 (Batch 30 merged).

## What ZIGGY asked (23 Nov)

- Credit the art as **painted by ZIGGY**, public-facing, not his legal name.
- The Batch 30 text is approved as final: it is **COLLAR**, the manual; rename across the board.
- `fmhub.json`: add `"author": "ZIGGY (DØGS)"`.
- Build v0.5.

## Done

- **ZIGGY everywhere the full name appeared** (28 files): `LICENSING.md` (DØG-5's own parts: "Copyright (C) 2026 ZIGGY
  (DØGS)", the art "hand-painted by ZIGGY"), `NOTICE`, `README.md`, the web player's, installer page's and manual page's
  footers, the source headers of DØG-5's own files and their generators (`Copyright (C) 2026 ZIGGY, DØGS (DØG-5 …)`,
  comments only: the firmware is unchanged), `CLAUDE.md`'s byline, and the batch records. The internal records still say
  "Vincent" (his first name) where they record what he decided; nothing public-facing carries the full name.
- **COLLAR:** the manual page is now "COLLAR — the DØG-5 manual" (title, header, a note "for v0.5" in place of "Draft"); the
  links in the web player, the installer page and the README say "The manual (COLLAR)"; the manual docs' titles carry
  COLLAR and record the approval. File names stay (`DOG-5-driver-manual*.md`, `/dog5/manual/`) so links keep working.
  The PDF is still to make (backlog §1 step 8).
- **`fmhub.json`:** `"author": "ZIGGY (DØGS)"` after `"what"`.
- **v0.5 = `FM-1_3645050`**: `./build.sh --release 0.5` twice, the same SHA-256
  **`2291529080d07b78c4042cdafffbbb6e53b9d78f3e6f04299b8ae8f4e6c215f4`**, 614,757 B. The firmware is the v0.4.5 code (no
  firmware change since Batch 27; only the identity differs). The installer page carries it as `dog5-0.5-20261123.fwsc`;
  README, the installer README and the feedback form say v0.5.

## Tests

A plain `./build.sh` last, then `sh tests/run_tests.sh`: **ALL TESTS PASSED** (installer 21/21, the manual in sync, the
player = the host build). `make_installer_page.py --check`: in sync with `dog5-0.5-20261123.fwsc`.

## Next (backlog §1 step 5)

ZIGGY tests this exact file on the unit before the tag: from stock, over another firmware, away and back, the identity,
playing, one install with the tab in the background, fm1-emu. Then the tag `v0.5`; the release's SHA-256 must equal the
one above.
