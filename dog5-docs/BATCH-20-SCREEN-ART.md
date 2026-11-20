# Batch 20: the screen art on HOME (the v0.4 test build)

20 Nov 2026, Vincent Kruger with Claude. Branch `build/batch-20-screen-art-v04`. The compositions were approved by Vincent on 19–20 Nov
(scale 0.75, Bee-tch tilted 22° so he stands on the board, the howl poses kept as drawn).

## What HOME is now

HOME (PERFORM, no layer held, the map not up) is the chapter's scene: the field, the dog, and his bark. Every other page,
a held layer and the map keep the panel exactly as before.

| Rows | What |
| --- | --- |
| 0–18 | top bar: the status (the tags, a readout, `STOPPED (PLAY)`, `SAVE HERE? …`, or a toast for 1.5 s), the chapter on the right in Grime Olive when it fits |
| 19, 220 | white rules |
| 20–219 | the field (240 × 200), the dog, the beam |
| 221–239 | bottom bar: the program number (Acid Chartreuse) and name, `*` when edited. Never covered |

- **Chapter** = `prog % 32 / 8`: 1–8 I JALOPY, 9–16 II BEE-TCH, 17–24 III MOONSHINE, 25–32 IV ACID CAN; THE PACK (33–99)
  follows the same cycle (33 = I, 41 = II …).
- **Poses**: silent = REST; sounding (the loudest voice's amp envelope above ~2 %) = BARK; in MOONSHINE a note held 350 ms
  draws breath (HOWL-INHALE) and from 900 ms howls (HOWL). STOP (PLAY) counts as silence.
- **The beam**: while he barks, the live scope (zero-crossing triggered, about two cycles of the loudest voice) runs from his
  mouth to the field's top-right corner, 2 px white, up to ±10 px either side, starting on the centre line (8 px taper).
  A new capture every 50 ms. Straight path only (the brief).
- **The sway**: 500 ms after the sound stops, REST rocks 1 px left and right, ~2 s a cycle (steps of 200 ms), until a note.

## How it draws (no framebuffer)

`firmware/src/dog5_scene.h`. Every change repaints only a rectangle, composed in the existing strip canvas (`cv_px`, 240 × 124
in `.pool`) from the field, the pose sprite and the beam, then blitted; `app_idle()` after each strip (the DRAW RULE; `lcd_blit`
also yields inside its DMA wait).

- Entering HOME or a new chapter: the whole field, 2 strips (~77 ms of SPI).
- REST ↔ BARK: the head's rectangle only (the generator proves the bodies are identical; ~70 × 72 px).
- Other pose changes and the sway: the union of the two sprite boxes (≤ ~120 × 110 px).
- The beam: the box of the old beam ∪ the new one, every 50 ms while barking. Worst case is II BEE-TCH (mouth at 126,111): about
  115 × 95 px, ~15 ms of SPI per 50 ms. **To check on the unit**: that note timing and the knobs feel unchanged while holding a
  chord on a BEE-TCH patch. Levers if not: 80 ms a capture, or a 1 px beam.
- The bars: `draw_header` now calls `hdr()`, which draws the bars on HOME and `ui_header` elsewhere.

## The art

`assets/screen/` (Vincent's final renders, composed): four fields as 240 × 200 indexed PNGs (255 / 252 / 250 / 240 colours), the
dog poses (REST, BARK, the tilted Bee-tch pair, HOWL-INHALE, HOWL) and `layout.json` (each placement and the mouth). 
`tools/make_screen_art.py` writes `firmware/gen/dog5_screen_art.h`: 8-bit indices + RGB565 palettes (byte-swapped), 265,489 B of
flash; it refuses > 256 field colours, > 255 sprite colours and half-clear pixels, and works out each scene's head rectangle.
The `.pxo` sources stay out of the repo.

## Numbers

| | v0.4 |
| --- | --- |
| image | 350,916 B of 581,564 (v0.3: ~82.5 KB; the art is 265,489 B) |
| RAM .data+.bss | 33,552 B of 98,304 |
| pool | 304,896 B of 344,064 (the scene adds none: it uses the existing canvas) |
| web player wasm | 347,581 B |

The audio path is untouched: the sound is bit-identical (the sim's sample-for-sample check against the host build passes).

## Tests

- `tests/scene.txt` (in `tests/run_tests.sh`): the four chapters at rest and barking, MOONSHINE bark → breath → howl, EDIT and
  back HOME, a PACK slot; the whole-scene draw calls `app_idle` (`expect idle` now reads the last full-screen draw: the map's or
  the scene's).
- `tests/run_tests.sh`: all pass. `node tests/sim_test.mjs`: pass (`docs/play/` rebuilt).
- Sway measured on a 20 fps host film: the dog's box changes at +1, 0, −1, 0 px every 2 s, nothing else on the screen moves.

## The 0.4 test build

`./build.sh --release 0.4` twice, same SHA-256 `34a0a4e7ab1326c0486e5e1e22cdf9432e99653d812c74ff3995de0bd44d809d`, 614,748 B,
identity `FM-1_964`; installer page regenerated (`dog5-0.4-20261120.fwsc`), `--check` in sync, `tests/install/run.sh` 20/20.
The 0.3 package leaves the page (git history). **Not on the unit yet.**

## Not in this batch

The FLEAS fracture, the fence, impacts and chapter accents; the boot splash; Vincent's hand-pixelled 96 px head for the update
screen (`DOG-5-head-96.pxo`, in the round-two zip) is not yet wired into `tools/make_ldr_art.py`.
