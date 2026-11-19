# Batch 19 — the installer page and the web player in the DØG-5 brand

Branch `build/batch-19-web-pages`, 19 Nov 2026. **Awaiting Vincent's merge.** No firmware change; the installed
package is the same v0.3 file (SHA-256 `293d7890…f763`).

## Shared: `web/brand/`

- `brand.css`: the palette as CSS variables, the three fonts, and the header lockup (the dog head, the pixel
  wordmark at exactly 2 × its 185 px grid, the tagline in Ray Pink, a line in Grime Olive).
- Fonts, subset to Latin and made into woff2 from Google's own font repository, all SIL OFL 1.1 (licences beside
  them as `OFL-*.txt`): Yatra One (titles), Space Mono 400/700 (labels, buttons, data), Cormorant Garamond Light 300
  and SemiBold 600 (body text; the SemiBold is for `<b>`).
- `dog5-favicon-240.png` and `dog5-wordmark-pixel.png`.
- **No page loads anything from another site** (checked in headless Chrome: zero outside requests on both).

## The installer (`docs/install/`)

- `web/install/index.template.html`: new styles and the header lockup; every element id and the safety text are
  unchanged. The checklist's text sits in a `<span>` so a bold word no longer splits the line.
- `tools/make_installer_page.py` inlines `brand.css`, its fonts and the two pictures as `data:` URLs, so the page is
  still one file that makes no request (it grows from ~860 KB to ~1.04 MB, the package being most of it).
- `docs/install/index.html` regenerated from the same v0.3 package; `--check` is in sync.

## The web player (`docs/play/`)

- `web/sim/sim.css` remapped to the palette: black page, Plum Night panels with a hard Sky Violet shadow, Acid
  Chartreuse as the accent (the selected patch, the Start-audio button, focus), the FM-1's red LEDs kept red.
  The device's knobs, buttons and keys stay neutral black and white, like the hardware.
- `web/sim/index.html`: the lockup header and the favicon as the tab icon. `web/sim/sim.js`: the screen before power
  is black.
- `web/sim/build.sh` copies `web/brand/` to `docs/play/brand/`.
- **Fixed:** the patch list showed the retired chapter titles (The Wasteland Arsenal, …). `web/sim/gen_patches.py`
  now writes I · Jalopy, II · Bee-tch, III · Moonshine, IV · Acid Can.
- `docs/play/` refreshed by copying the page files; `dog5.wasm` is unchanged (no rebuild needed).

## Proofs

`tests/run_tests.sh` ALL TESTS PASSED (installer 20/20), `node tests/sim_test.mjs` SIM TEST PASSED.

## Left alone, worth a look

- The installer's last paragraph still says "Not tested against a real unit by the author of this page." The page
  has since installed v0.1 and v0.2 on Vincent's FM-1. The wording is his call.
