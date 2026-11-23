# Batch 21: DØG-5 all the way through (the boot animation, the panel, the update screen's head, the OberVave leftovers)

20 Nov 2026, ZIGGY with Claude. Branch `build/batch-21-branding`. Asked for (20 Nov, after v0.4's merge): bring the
new boot splash and all the branding into v0.4 properly, no shortcuts, keeping the Felucca references.

## What changed, screen by screen

| Screen | Before | Now |
| --- | --- | --- |
| Power-on | OberVave's splash with the name swapped: "DØG-5", "8-VOICE ANALOG POLY / M-VAVE FM-1", blue-black, 2.4 s | **The launch animation** Vincent approved (below), ~6 s, ending on HOME's scene; any key or button ends it at once |
| HOME | the scene (Batch 20) | unchanged |
| Every other page, the hold-HOME map | OberVave's look: blue-black panel, red 7-segment number, blue arcs, the name with OberVave's three blue bands, red LEDs | **the brand palette** (`dog5_palette.h`): black; legends Foam White; dim legends Grime Olive; page name, value arcs, scope trace Acid Chartreuse; number in Acid Chartreuse over unlit Plum Night segments (as the update screen's bar); rules and tracks Sky Violet; knobs Plum Night; scope on Jungle Deep; LEDs Ray Pink; **the pixel wordmark** (Sun Yellow, black outline, Acid Chartreuse shadow) in the header. Layout and behaviour unchanged |
| Install, step 1 (the running firmware checks the package) | white text | "UPDATE" Foam White, the step Grime Olive, FAILED Ray Red, DRY RUN OK Acid Chartreuse |
| Update screen (the loader) | the head reduced automatically from the favicon | **Vincent's hand-pixelled 96 px head** (`DOG-5-head-96.pxo`, exported to `assets/brand/dog5-head-96.png`), as drawn; the wordmark is byte-identical |
| USB rescue, crash | white text; crash on dark red | the title Acid Chartreuse, the rest Foam White / Grime Olive; crash on Ray Red |

## The boot animation

Source: the claude.ai artifact **"DØG-5 launch screen"** (19 Nov), its last version: speed 95 ms a step (smooth), grain
62, halo 53, seal 78, the zig-zag scope seal. The page was 400 × 400; everything here is × 3/5.

| ms | |
| --- | --- |
| 0–500 | the favicon (`assets/brand/dog5-favicon-240.png`), its white areas white |
| 500–3540 | its white areas run the 16-colour cycle twice (32 steps of 95 ms) |
| 3540–5060 | 400 ms cross-fade to DØG-5 in Yatra One (55 px), the cycle on its letters (16 steps) |
| 5060–5510 | the melt: letters sag and stretch column by column, turning acid green |
| 5510–5960 | the burn: a green fire front with a hot core rises, embers fly, **the chapter's scene fades up under it** |

Behind: a static near-black grain, a halo of the cycle's colour, the zig-zag seal 8 steps out of phase, wobbling; halo
and seal fade out through the melt.

**Departures from the page, all deliberate (one-line changes if Vincent wants them back):**
1. **The burn reveals the real HOME scene**, not the page's blank white screen. The white was the stand-in for the
   (deleted) reaper frame "until Chapter 1 exists"; the scenes exist now.
2. **The melt and fire green is Acid Chartreuse `#DEF402`** with a Sun Glow core, not the page's `#39FF14`: that was the
   retired Chapter I accent, and the brand palette was locked later the same day.
3. **A key or button press ends it at once** (a live instrument: no waiting 6 s to play). Keys or buttons held at
   power-on don't count until let go (OCT− at power-on stays the rescue).
4. The page's random embers and flickering fire edge come from a fixed sequence (the same every boot).
5. The timing is by the clock, as the page's. **The device draws about 8–10 frames a second** (a full screen is 77 ms on
   the SPI link, plus ~10 M instructions of drawing a frame), so the cycle steps more coarsely than in the browser; the
   length does not change. The web player (and the GIF) show it at up to 25 frames a second.

It is ~6.0 s; Vincent's brief was "roughly 4 s, flexible", and the page's last speed setting (95 ms) is what gives 6 s.
Speed is one constant (`SPL_STEP`): at 55 ms (the page's earlier default) it is 4.0 s.

Code: `firmware/src/dog5_splash.h` (drawn in the strip canvas, 2 strips of 120 rows a frame, polling between them),
`tools/make_splash_art.py` → `firmware/gen/dog5_splash_art.h` (favicon and word as 4-bit coverage, the ramp, the halo
and seal tables) and `firmware/gen/dog5_ui_art.h` (the header's wordmark). `sc_px_rest()` in `dog5_scene.h` gives the
reveal its pixels. Integer only, no 64-bit division (the gradient's per-box steps are worked out once, 32-bit).

**Tests:** the host build (`tests/host.c`) stops the animation at 2.4 s (the old splash's length) so every existing
script keeps its timing; a script line `0 splash full` runs it whole. New `tests/splash.txt` (whole, ends on HOME, HOME
plays) and `tests/splash_skip.txt` (a key at 1.5 s ends it and sounds); the web player always runs it whole, and
`tests/sim_test.mjs` now runs the host whole too (its screens at 2.6 / 3.4 / 5.6 s compare mid-animation frames, pixel
for pixel).

## OberVave leftovers removed (git history keeps them)

`assets/logo.png`, `assets/logo.svg` (the OberVave wordmark), `firmware/gen/obv_splash.h` (its boot logo),
`tools/make_logo.py`, and in `obv_ui.h` the banded-logo code (`cv_stripes`, `draw_logo_small`, `STRIPE`). This was decision
D6 of the 12A inventory: "keep until the DØG-5 wordmark exists". `LICENSING.md`: the URW Bookman / Inter row (only
those files used them) is replaced by Yatra One, Cormorant Garamond and Space Mono rows, and DØG-5's own parts have a row.

**Kept on purpose:** the credits (`LICENSE`, `NOTICE`, `LICENSING.md`, the README and web player credit lines: the GPL
requires them); the USB product name "Felucca" (the installer finds the unit by it); the code's file names (`obv_*.h`,
`obervave.c`: internal, renaming them would only churn); the panel pages' layout (OberVave's, credited in `obv_ui.h`).

## Numbers

Image 350,916 → **388,952 B** of 581,564 (+38 KB: the animation's art and code; the hand-pixelled head is the same 1,152
B). RAM 33,552 → **34,512 B**. Pool 304,896 → **308,496 B** (+3,600: the seal's per-strip mask). Web player wasm 374,679 B.

## The rebuilt 0.4 test build

`./build.sh --release 0.4` twice, same SHA-256 `f5ceddc4a84cb4042de6cb8bb1b4913fabf0b7b11e0e480c811deac2dc53a033`,
614,757 B, identity `FM-1_964` (the version stays 0.4: it was never flashed). Installer page regenerated
(`dog5-0.4-20261120.fwsc`), `--check` in sync, `tests/install/run.sh` 20/20; `tests/run_tests.sh` ALL TESTS PASSED;
`node tests/sim_test.mjs` passes. The sound is unchanged (the sim's sample-for-sample check; no audio code touched).

## On the unit, check

1. Power on: the animation plays to HOME in ~6 s; the cycle looks smooth enough at the device's frame rate.
2. Power on and press a key straight away: it stops and plays.
3. The panel pages (EDIT, FX, GLO…) and the map in the new colours: legible in the dark? (Grime Olive labels are the
   dimmest text.)
4. Install screen 1 and the update screen show the new head.
