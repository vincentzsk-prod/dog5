# Batch 25: SELECT's LFO dial, and the housekeeping (v0.4.4)

21 Nov 2026. Branch `build/batch-24-home-dials` (on top of Batch 24, both unmerged at the time).

## SELECT's LFO RATE as a dial

Vincent's yes (21 Nov): on HOME, a SELECT turn (LFO RATE, 2 a detent, as since Batch 9B) now shows on the same plate as
the four knobs (Batch 24, `sc_dial`), labelled **`LFO`** with the value in Hz underneath, for 1.2 s after the last turn.
"LFO RATE" was tried and ran into the plate's frame; "LFO" over a value in Hz reads unambiguously. The top-bar readout
(`readout()`) stays for the MONO / POLY keys only. In BEE-TCH the plate covers the dog's tail while it shows; Vincent
accepted that.

**Checks:** `tests/controls/select_dial.txt` (its shot at 4300 ms is the dial); sound byte-identical to `main`
(select_dial, scene, home_readout scripts, `cmp` of the WAVs); `tests/run_tests.sh` ALL TESTS PASSED;
`node tests/sim_test.mjs` passes (web player rebuilt). Image 392,144 B (+44), RAM 34,928 B, pool 319,760 B (unchanged).
`./build.sh --release 0.4.4` twice, same SHA-256 `2da5430ec4f12ebfaa1b65737848e7f86c875de3ef8059b02e37bd346100f758`,
identity `FM-1_964`; installer page regenerated (`dog5-0.4.4-20261121.fwsc`), in sync. Carries Batches 22–24.

## Housekeeping

- **The flash-chip note, up front** (Vincent, 20 Nov: "built and thoroughly tested on a unit with the older chip"):
  a quoted box at the top of `README.md`; a box under the installer page's intro (`web/install/index.template.html`,
  `#tested`) and the top of `docs/install/README.md`; every GitHub release now opens with
  `.github/release-header.md` (the workflow's `body_path`; GitHub's generated notes follow). The older chip is the Puya
  P25Q80 (`0x856014`); the newer UC25HQ80 (`0xB36014`) is accepted by the loader but has never run DØG-5.
- **The installer page's "Not tested against a real unit"** is gone: the page installed v0.1 from stock on 12 Nov
  (Chrome on macOS), and v0.4 went on over a Hub firmware and back (20–21 Nov). Its README says what the repository's
  tests show apart from that.
- **README status** rewritten: what has been on the unit (v0.1, v0.2, v0.4) and what has not (Batches 22–25).
- **`CLAUDE.md`:** §4 font row (Ø is in the font since Stage 1), the transient-message row, §5 knob readout (the dial),
  §5 SELECT, §7's Ø line, §8 (ACID CAN, not LE GATO; the colours as built replace the Moonshine-magenta rule), §10 build
  order, §11 item 3 (versions, where the chip note lives) and item 4 (the art is in), §12 doc map, "Last updated".
