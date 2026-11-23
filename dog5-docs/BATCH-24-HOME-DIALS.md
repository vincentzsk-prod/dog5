# Batch 24: the HOME knob dial (v0.4.3)

21 Nov 2026, ZIGGY with Claude. Branch `build/batch-24-home-dials`. Asked for 21 Nov: on HOME, show a turned knob
as the round dial the panel pages draw (it shows how far the knob is turned at a glance), not only a number.

**Now:** turning CUTOFF, RESO, ENV AMT or RELEASE on HOME shows that knob exactly as the panel pages draw it (the label,
the Acid Chartreuse value arc on its Sky Violet track, the pointer, the value) on a 64 x 88 px black plate with a Sky
Violet edge at the top left of the scene (x 2, y 22), for 1.2 s after the last turn; then the art comes back. It
replaces Batch 22's number in the top bar (a MIDI CC to the cutoff still shows there). The plate stays on top while the
beam, the sway and FLEAS repaint under it (it is kept in the pool, `sc_dial_px`, 11 KB, and laid over every repaint).

**Where:** the top left is clear of the beam (it flies to the top right) in every chapter, and of the dog in I, III and
IV; in II (BEE-TCH, the dog tilted on his board) it covers his tail and back while it shows.

**Checks:** `tests/home_readout.txt` (each knob, the dial over a barking scene, the art back after 1.2 s); sound
byte-identical to `main`; `tests/run_tests.sh` ALL TESTS PASSED; `node tests/sim_test.mjs` passes. Image 392,100 B
(+540), RAM unchanged, pool 319,760 B (+11,264). `./build.sh --release 0.4.3` twice, same SHA-256
`23a851b7172699da6de788552881eb6aedc23388ffa3b66dcabfae26bcaf84b9`, identity `FM-1_964`; installer page regenerated
(`dog5-0.4.3-20261121.fwsc`), in sync, 20/20. It carries Batches 22 and 23 (neither flashed yet).
