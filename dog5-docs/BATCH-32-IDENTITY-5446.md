# Batch 32: a new identity, FM-1_54460XYZ (v0.5.1)

**23 Nov 2026.** The Firmware Hub's check of v0.5 passed everything except the identity: `FM-1_3645050` was "already
another card's: polly". Polly's catalogue entry claims `FM-1_3\d{6}` (every `FM-1_3` + 6 digits), and our 7-digit
identity fell inside it. Batch 27 had checked the catalogue's `product` values, not each entry's `ident` regex.

## The new identity

- **`FM-1_54460XYZ`**: `5446` (ZIGGY's pick), a `0`, then vX.Y.Z one digit each. v0.5.1 is `FM-1_54460051`, a dev
  build `FM-1_54460000`. `firmware/src/dog5_id.h` (`DOG5_ID_FM1 "FM-1_54460"`) is still the one place; `tools/build.py`
  and the comments follow.
- **Why 8 digits:** the 7-digit `FM-1_5446XYZ` is inside MONK-1's `FM-1_5(?!000201)\d{6}`. Every `ident` in
  `catalog.json` (all ~250 entries, read 23 Nov) was tested against `FM-1_54460051`: only the Felucca family's catch-all
  `FM-1_\d{3,8}` matches, which matches every identity (it did for `FM-1_3645050` too, and the Hub didn't object to it).
  The identity is 13 characters (the packer allows 20); digits only after the one underscore, as before.
- **Rule for next time:** test a candidate against every `ident` regex in `catalog.json`, not only the `product`s.

## v0.5.1

The same firmware as v0.5; only the identity and the version string (`0.5.1`) differ. `./build.sh --release 0.5.1`
twice: SHA-256 `6ffb7d421f4032d3c397564dfaf115c9003ca46c37aaf5bc7091637d50bf9aa6`, 614,757 B. The installer page is
regenerated (`dog5-0.5.1-20261123.fwsc`, `v0.5.1 · 2026-11-23`); READMEs, the feedback template and `PLATFORM-API.md`
follow. Older batch records keep the identities they had.

## For ZIGGY, on the unit

Install v0.5.1 from the installer page (over v0.5 is fine); "Find my FM-1" must report `FM-1_54460051`. Then another
firmware and back, and a minute of playing. Then the release `v0.5.1`, and "Check again" on the Hub's status page.
