# Batch 28 — the v1.1 backlog, the voice cards, the card in the player, the manual and feedback

**22 Nov 2026**, branch `build/batch-28-v11-cards-player` from `origin/main` 33e0b1e (Batch 27). **No firmware code
changed**: the image is byte-identical to 0.4.5 (392,148 B), the sound in the browser player is still the host build's
sample for sample.

## What Vincent asked

Log the Kennel (a DØG-5 manager page in the spirit of the EVILGENIUS Manager) for v1.1; sweep the whole project so
every note and idea for v1.1 and later sits in one place; bring the voice cards fully up to date; make a patch's voice
card pop up in the web player when it is picked; give the player (and anywhere else it fits) a way to reach the Driver
Manual and to send feedback.

## What was done

**1. One backlog: `dog5-docs/V1.1-BACKLOG.md`** (and the same text as the Project doc `DOG-5-v1.1-backlog.md`). Gathered
from `CLAUDE.md`, every batch record, the voicing README and cards, `PERF-BASELINE.md`, the Project docs and the chats.
§1 is what stands between now and the public release (v0.5), §2 is v1.1 (sound, screen, tools / web with the Kennel
starred, repo housekeeping), §3 later, §4 the engine's accepted limits, §5 what was decided against. Nothing in §2–§3 is
approved to build. **The Kennel's real cost is firmware first:** DØG-5 takes every parameter as a CC, but nothing sends
a patch back over USB, so it needs a SysEx dump / load before any page.

**2. The 32 voice cards** (`dog5-docs/voicing/cards/`): each header now carries its chapter as built
(`# 30 · THE DØG · Chapter IV · ACID CAN`); the "no Drone Latch" lines (18, 19, 21, 22, 23) say REC (HOLD) now; 30's
DRIVE points at the MIXER page, knob 4 (Batch 9B). The cards README states the header format.

**3. The card in the web player.** `web/sim/gen_patches.py` reads each card's three reader sections (what it sounds
like, gear inspirations, how to play it) into `patches.json` as HTML (Python-Markdown; links unwrapped, no images or
scripts let through). Picking a patch in the list, or stepping with PRESETS on the unit, opens the card: under the unit
on a wide screen (the patch list stays on the right), below it on a phone. The card follows the firmware's program, so
it is always the patch that sounds. A pick made before the player is switched on is held and sent once it boots, and
the card keeps showing the patch picked while the boot animation runs (it used to fall back to 01 Red Pill).

**4. The Driver Manual on the web: `docs/manual/`** (`https://vincentzsk-prod.github.io/dog5/manual/` once merged).
Built by `tools/make_manual_page.py` from the repo copies of the Project docs in `dog5-docs/manual/` (Parts 0–2B and
3–4, the player's brand fonts and colours, a contents list, a "draft for v0.4" note with the flash-chip line).
`--check` says whether the page matches its sources. **Keep the two manual copies in step:** edit the Project doc, copy
it to `dog5-docs/manual/`, rebuild the page.

**5. Feedback.** `.github/ISSUE_TEMPLATE/feedback.md`: a short form (where, version, flash chip, patch, what you did,
what happened). Linked from the web player's top bar and footer, the installer page (its "report what happens" line and a
new Manual · Play · Send feedback row) and the README. **GitHub Issues are switched off on the repo**, so the links
land on an error page until Vincent turns them on (Settings → General → Features → Issues).

**6. Housekeeping found by the sweep.** `PERF-BASELINE.md`'s "now" numbers brought to 0.4.5 (image 392,148 B, RAM
34,928 B, pool 319,760 of 344,064 B). Manual 1.10 now says another firmware's saves don't show up in DØG-5 and that
DØG-5 can write over them (matching the Batch 27 README line). The README links the manual and feedback.

## Tests

A plain `./build.sh` (identity `FM-1_3645000`, 392,148 B), then `sh tests/run_tests.sh`: **ALL TESTS PASSED** (host
app, program store, update path, browser player bit-exact against the host build, installer page 20/20).
`make_manual_page.py --check` and `make_installer_page.py --check` in sync. In headless Chromium at 1400 px and 390 px:
the card opens on a click and on PRESETS, no page errors, and after boot the highlighted patch and the card are the one
clicked (18 Roto-scopo). Not tested: a real phone, Safari, Firefox.
