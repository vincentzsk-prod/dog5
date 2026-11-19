# Batch 16 — the update loader's screen, reskinned to the DØG-5 brand

Branch `build/batch-16-update-screen-reskin`, 19 Nov 2026. Designed and built in the planning chat with the repo
attached. **Awaiting Vincent's merge. No version bump: it ships with v0.4.**

## What changed

The screen the FM-1 shows while the update loader runs (UPDATE MODE, WRITING, UPDATE FAILED) now uses the
brand, not the Firmware Hub's colours and the loader's 5 × 7 letters for the name.

- **Black** background.
- **The dog head**: the 240 px black-and-white favicon, cropped to its ring and reduced to 96 px, 1 bit a pixel.
- **The DØG-5 pixel wordmark**, with the real Ø: Yatra One at 48 px on a 1-bit grid, Sun Yellow letters, a
  1 px black outline, and a hard Acid Chartreuse shadow 4 px down and right. It is 166 × 45 px, 2 bits a pixel.
- **The status** in Foam White, size 2. The percent now sits on the status line ("WRITING 57%"); it used to be
  a size-3 line under the bar, and that room went to the art. UPDATE FAILED is in **Ray Red**.
- **What to do** in **Grime Olive**.
- **20 segments**: off in **Plum Night**; lit, and the waiting light, in **Acid Chartreuse**. The afterglow is
  halfway between the two.
- **thefirmwarehub.com** at the foot, in **Ray Pink**.

Colours: `claude/DOG-5-brand-palette.md` in the Project (RGB565 values in its table).

## Files

- `firmware/loader/ldr_screen.c`: the new colours and layout, and `ldr_pic()`, which draws a picture from
  `ldr_art.h` one row at a time with `lcd_blit` (it waits for the last row's transfer before reusing the row
  buffer). The text, segment and waiting-light logic is unchanged. `LDR_NAME` and `DOG5_NAME_LOADER` are no
  longer drawn (the define stays in `dog5_id.h`).
- `firmware/loader/ldr_art.h` (new, generated): `LDR_HEAD` (1152 B) and `LDR_WORD` (1890 B).
- `tools/make_ldr_art.py` (new): `tools/make_ldr_art.py assets/brand/dog5-favicon-240.png YatraOne-Regular.ttf`
  regenerates `ldr_art.h`; it reproduces the committed file byte for byte. It needs Pillow, NumPy and SciPy (host
  only). Yatra One is SIL OFL; only rendered pixels go into the firmware, the font file does not.
- `assets/brand/dog5-favicon-240.png` (new): the source favicon, pure black and white.
- `tests/ldr_screen_test.c`: the checks now look for the head, the wordmark in yellow and chartreuse, the
  status, "WRITING 50%", UPDATE FAILED in red and the new colour set.
- **`ldr_core.c` (the flash writing) is untouched.**

## Proofs

- `tests/ldr_screen_test.c`: passes. Its PPM screens are the preview Vincent approved.
- **Device build** (vendored toolchain, plain `./build.sh`):

| | main (v0.3 source) | this branch |
|---|---|---|
| Loader image | 10,468 B | **13,760 B** |
| Staged `ota.bin` | 9,067 B | **11,592 B** |
| bss end | `0x1c0ff50` | `0x1c10df0` |

  `ota.bin` must stay under 19,968 B (`OTA_AREA_LEN - 0x200`), so 8,376 B are still free. The image limit is
  81,920 B (`0x14000`), and bss ends far below the stacks (`0x01C70000`). The app image is unchanged (82,536 B,
  RAM and pool unchanged).
- `tests/run_tests.sh`: **ALL TESTS PASSED** (installer page 20/20, no FAIL lines).

## On the unit

The loader runs from the package being installed, so the new screen appears **during the v0.4 install itself**.
If this loader's screen code ever failed, an install would stop partway. The way back is the usual one: download
mode plus M-Flasher with the stock backup (`DOG-5-smoke-test-plan.md`).

## Open

- **The 96 px head is reduced automatically**, and its eyes go soft. A 96 × 96 head pixelled by hand in
  Pixelorama would be better: drop it in and run `make_ldr_art.py` (it currently crops and shrinks the 240 px
  favicon; give it a 96 px file and change `CROP` / `HEAD` to match).
