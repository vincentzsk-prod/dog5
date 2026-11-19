# Batch 17 — the Firmware Hub card

Branch `build/batch-17-hub-card`, 19 Nov 2026. **Awaiting Vincent's merge.** Nothing here touches the firmware.

## What the Hub reads (thefirmwarehub.com/submit, read 19 Nov 2026)

The card's description, picture and links come from **`fmhub.json` in the repo root**; its version comes from the
newest GitHub release. Edit and push, and the card follows within about three hours.

- `image`: a square file in the repo, 240×240 to 1024×1024, PNG, WebP or JPEG, 300 KB at most. The Hub shows it at
  about 160 px wide.
- `what`: plain English, 300 characters at most; anything longer is cut at a word. No HTML or links.
- `kinds`: one of `synth`, `groove`, `drums`, `chords`, `tracker`, `other`, written as a list (OberVave's own file
  uses `["synth"]`).
- `color`: an optional `#RRGGBB` for the card; very dark colours are refused.
- `play`, `editor`, `cheat`: optional links.
- `sounds`: **required here**, because the repo carries `.wav` files (99 in `reference-renders/`, all rendered by
  DØG-5's own engine). Declared as `"own"`.

## What this branch adds

- `fmhub.json`: the description (236 characters), `["synth"]`, the card image, colour Acid Chartreuse `#DEF402`,
  the web player as `play`, `"sounds": "own"`.
- `assets/brand/dog5-hub-card.png`: 900 × 900 (a 300 px pixel grid, each pixel 3 × 3), 12.9 KB. The black-and-white
  favicon over the pixel wordmark, on black. It is cropped tighter than the release cover, so it still reads at the
  Hub's 160 px.

## Before submitting (the Hub's requirements still open)

1. **A GitHub release with the `.fwsc` attached.** Not done yet; `release.yml` publishes one when a `v*` tag is pushed.
2. **Tested on a real FM-1: installed from V15 (stock) and from another firmware, and left again.** Installing from
   stock has been done. **Leaving DØG-5 again (installing another firmware over it) has not been tested yet.**
3. **Own identity** (`FM-1_96x`) and the **update loader in the package**: done.
4. Add `"cheat"` (the COLLAR manual PDF) once it exists.
5. **The description promises the dog whose bark is the live waveform.** That is true only once the screen art is
   built (v0.5). Submit with v0.5, or trim that clause if submitting earlier.
