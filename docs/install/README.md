# DØG-5 installer (self-hosted page)

`index.html` here installs DØG-5 on an **M-VAVE FM-1** over USB-MIDI, from **Chrome or Edge**. It is one file: the
package (`dog5-0.5-20261123.fwsc`, identity `FM-1_3645050`) is inside it, and it makes no network request of any kind. It is
served by GitHub Pages from `main` `/docs`; the expected address is <https://vincentzsk-prod.github.io/dog5/install/>
(GitHub's usual form; confirm it once Pages is on). WebMIDI itself needs `https://` or `http://localhost`.

> **Tested on one unit, with the older flash chip.** DØG-5 was built and tested on a real FM-1 with the Puya P25Q80 flash
> chip (JEDEC `0x856014`). This page installed it from the stock firmware (12 Nov 2026, v0.1, Chrome on macOS); v0.4 went on
> over another Hub firmware and back again (20–21 Nov). Newer FM-1s carry the UC25HQ80 (JEDEC `0xB36014`): the loader
> accepts it, but **DØG-5 has never been installed or played on one**, so its behaviour there is unknown. On a newer unit,
> keep M-Flasher and your backup ready, and report what happens.

What the repository's own tests show, and what they do not, is at the end.

## Using it

1. Open the page in Chrome or Edge. The top box says whether this browser can do it.
2. Read the package box: identity, size, SHA-256, and the self-check (the same header / file-list / file CRC checks the
   Python installer runs, plus a comparison with the SHA-256 recorded when the page was built).
3. Tick the five pre-flight boxes (USB data cable, stays plugged in, do not touch the unit, power stays on, M-Flasher and
   backup ready). **Dry run** needs none of this: it builds every reply frame and sends nothing (it does not even ask for
   MIDI access).
4. **Find my FM-1**: the browser asks for MIDI + SysEx permission; the page sends one identity question to the chosen
   port and shows the answer (`FM-1_015` is the stock firmware; `ota-FM-1_900` means the unit is already in update mode).
5. **Install…** shows a last box (unit, package, what will be written). Nothing is sent before **Yes, start**.
6. The page shows step 1 (the running firmware checks the package and switches to the update loader), step 2 (the loader
   writes; percent, one log line per chunk) and then waits for the unit to restart and checks that it reports
   the package identity (`FM-1_3645050` for v0.5; v0.4.5 was `FM-1_3645045`, v0.4 to v0.4.4 `FM-1_964`). That is all it can check: it does not test the sound.

If it is interrupted, **unplug, power-cycle, and run the page again**. A unit cut off during step 2 comes back in update
mode; the page then shows **Resume**, which skips step 1 and serves the package again. The loader skips sectors that
already match, so a resume rewrites only what is missing.

## What it can write, and what it cannot

The page cannot write flash. It answers read requests from the device with bytes of the package, and refuses a request
outside the package (`badreq`, as `tools/fm1_install.py` does). What gets written is decided by code that is in this
repository:

| Flash | Who | Source |
| --- | --- | --- |
| `0x000000–0x003FFF` (boot head, chip key) | nobody: never written | `firmware/loader/ldr_core.c` (`LDR_APP_LO`) |
| `0x004000–0x092FFF` (app area) | the update loader, sector by sector, only sectors that differ, each read back; checked first against this unit's own chip key | `ldr_core.c` (`LDR_APP_LO/HI`, `ldr_chip_key`, `ldr_pass`) |
| `0x093000–0x0FBFFF` | the loader erases only the sector that holds the update record, when it finishes | `ldr_core.c` (`ldr_records_drop`) |
| `0x0E0000–0x0E4FFF` | step 1: a staged copy of the loader and its update record, written by the firmware that is running when you start; erased at the end | `firmware/src/ota.c` (`OTA_AREA`, `OTA_RES`) |
| flash chip | the loader writes nothing unless the chip's JEDEC ID is `0x856014` (Puya P25Q80) or `0xB36014` (UC25HQ80) | `fm1_flash_map.h` (`FL_JEDEC_OK`), `ldr_core.c` |

**Step 1 on a stock unit is not covered by this table.** On a stock FM-1 (`FM-1_015`) step 1 is run by the stock
firmware, whose code is not in this repository. The repository documents the protocol it speaks (`ota.c` is Felucca's
reimplementation of the same exchange, and `tools/fm1_install.py` has installed Felucca-family packages from stock
units), but what the stock firmware checks or writes is **unverified here**.

## The protocol (from `tools/fm1_install.py`; the page is a port of it)

The device asks, the host answers; the host never pushes data.

- Wire frame: `F0 pack7(body) F7`, body = `00 59 cmd len24 …`, 8-bit to 7-bit packing LSB first (`pack7` / `unpack7`, lines 62-86).
- Identity question: `F0 00 32 45 00 00 00 40 7F F7` (`HS_QUERY`, line 33); the answer carries `NAME_NNN` (`parse_identity`).
- Upgrade command: `F0 22 24 35 7F F7` (`UPGRADE`, line 34).
- Read request (device → host, cmd `0x30`): flags, address (32 bit LE), length (24 bit), checksum (`parse_request`, line 96).
  Reply (`response`, line 88): `00 59 30 len+8 (24 bit) 00 flags address length data checksum`, checksum = `~sum(body[6:])`.
  Largest chunk `MAXDATA = 512` (line 36); a larger or out-of-image request is refused.
- Finish asks: address `0xE0000000` (end of step 1) and `0xF0000000` (end of step 2); the answer is `success\0`.
- The image served is the package without its marker bytes: one marker byte after each of the first 20 blocks of 47
  bytes; the markers spell the identity (`logical_image`, `product_of`, lines 133-172).
- Sequence (`Updater.serve` … `install`, lines 335-423): handshake → `UPGRADE` → 2 s → serve until `0xE0000000` (idle limit 8 s)
  → 3 s → wait up to 30 s for a port that answers as `ota-FM-1_9NN` (the update loader) → `UPGRADE` → 2 s → serve
  until `0xF0000000` (idle limit 180 s) → 3 s → wait up to 40 s for the unit, compare its identity with the package's.
  Each data reply is sent 10 ms after the request.
- Nothing checks a CRC or signature on the host except the package self-check; the update loader checks the package's
  CRC16 over everything it was served and this unit's chip key (`ldr_core.c`).
- **Resume**: a unit found as `ota-FM-1_900` (`OWN_LOADER_RE`, line 43) skips step 1 (`install`, line 410). There is no
  other resume mechanism; the loader stays active across a power cycle until it finishes (`ldr_core.c` header comment).

## Identity digits

The package identity is `FM-1_3645XYZ`: `3645` is DØG-5's own prefix (DØG-5 on a phone keypad: D=3, O=6, G=4, then 5),
and `XYZ` the version (`tools/build.py --release X.Y.Z`; v0.5 is `FM-1_3645050`, v0.4.5 was `FM-1_3645045`, a dev build `FM-1_3645000`). Until
21 Nov 2026 it was `FM-1_96N`; the Firmware Hub's catalogue showed that whole family already taken (`FM-1_964` is
SIDOU), so it changed before DØG-5 was submitted. **Digits only after the one underscore:** every FM-1 installer reads an
identity as `NAME_digits` (`parse_identity` in `fm1_install.py`, `parseIdentity` in `fm1install.js`), so a second
underscore, a letter or a full stop would leave the unit unrecognised (the version with its full stops is in the release's name and on this
page instead). The installer's logic uses the model name (`FM-1` must match the unit's) and, after the restart,
requires the unit to report exactly the identity of the package it was given. For the loader it matches
`ota-FM-1_9\d\d` (`OWN_LOADER_RE`), and the loader's own identity (`ota-FM-1_900`) is fixed in `firmware/loader/loader.c`,
independent of the app's.

## If it goes wrong

Unplug the USB cable, power-cycle the FM-1, run the page again. If the unit will not boot: **M-Flasher with your backup**.
App-level USB rescue (holding OCT− at power-on) is **unproven on this hardware**; do not rely on it.

## Rebuild and tests

```sh
./build.sh --release 0.5                          # build/dog5-0.5.fwsc (needs the JieLi toolchain + SDK)
python3 tools/make_installer_page.py --release 0.5 --date 2026-11-23     # the package and index.html, together
python3 tools/make_installer_page.py --check    # fails if the page or the package beside it have drifted
sh tests/install/run.sh                         # the proof below
```

`web/install/` holds the sources (`fm1install.js`: the protocol; `index.template.html`: the page).

What `tests/install/run.sh` shows, without a device:

- the page and package regenerate byte for byte from the sources (no drift);
- the real device code (`ota.c`, `ldr_core.c`) is run on the host and its read requests recorded (23 for step 1, 1180 for
  the loader's write pass); Python's installer and the page's JavaScript answer them with byte-identical frames, and
  complete install sessions (stock → loader → write → verify, resume, cut-off + resume, wrong model, foreign loader,
  read outside the package) give identical host-to-device byte streams and outcomes;
- headless Chromium drives the page itself against a fake WebMIDI unit: dry run (no MIDI access), the confirm step (no
  `UPGRADE` byte before it), a full install, a cut-off with the failure text, and the resume.

**Not shown by these tests** (the real unit above covers some of it, for the older chip and Chrome on macOS only): anything on a real FM-1 or a real WebMIDI stack (port names and re-enumeration on macOS, Windows, Linux;
how Chrome delivers large SysEx), the stock firmware's step 1, and the timing under real USB. The fake device asks for
the real loader's requests but answers instantly.
