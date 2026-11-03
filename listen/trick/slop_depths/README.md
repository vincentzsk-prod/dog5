# SLOP ride: three depths to choose from

This is the same held note and the same chord as `../slop_note.wav` and `../slop_chord.wav`. Each file plays 3 s
plain, then the ride turns up to the top over 4 s, holds there for 4 s (1.2 to 7.2 s in the file is the climb,
7.2 to 11.2 s is the hold), then comes back to 0 over 2 s.

**Decided 3 Nov: 2x ships** (`SLOP_SCALE_X2 4` in `obv_engine.h`). These renders are kept as the record of the
choice. The 1x and 1.5x files were host builds made with `-DSLOP_SCALE_X2=2` and `=3`. The 2x files are what ships,
byte-identical to `../slop_*.wav`.

| file | depth | VINTAGE at full ride (the patch's 30 + the ride) |
|---|---|---|
| `slop_note_1x.wav`, `slop_chord_1x.wav` | 1x (0..127 added) | 157 |
| `slop_note_1.5x.wav`, `slop_chord_1.5x.wav` | 1.5x (0..190 added) | 220 |
| `slop_note_2x.wav`, `slop_chord_2x.wav` | 2x, **shipped** (0..254 added) | 284 (byte-identical to `../slop_*.wav`) |

## At full ride, per voice

The numbers are read from inside the engine: each sounding voice card's vintage pitch over the 4 s hold. The
**mean** is where that voice sits (minus = flat). The **sd** and **range** are how far it wanders around that.

| depth | held note (card 0) | chord, per card (0 / 1 / 2 / 3) | chord, average of the 4 | wander sd, note / chord average |
|---|---|---|---|---|
| 1x | **−11.2** | −11.2 / +7.4 / +4.6 / −7.9 | −1.8 | 5.3 / 5.8 |
| 1.5x | **−15.6** | −15.6 / +10.6 / +6.5 / −10.7 | −2.3 | 7.4 / 8.1 |
| 2x | **−20.1** | −20.1 / +13.8 / +8.7 / −13.9 | −2.9 | 9.6 / 10.5 |

For reference, at ride 0 (the patch's own VINTAGE 30) the voices sit at −2.5 / +0.6 / +0.4 / −1.7 cents, with an
sd of about 1.

How to read the numbers:

- **The voices don't all go flat.** Each of the 8 voice cards has its own fixed tuning offset in VINTAGE's law, some
  flat and some sharp, and the ride scales it. Card 0 happens to be the flattest of the four used here (−8 cents at
  VINTAGE 127). So the chord spreads apart around roughly its true pitch, while a lone note on card 0 goes flat.
- **Which card a single note lands on:**
  - MONO and UNISON patches always use card 0, so they get the flat case.
  - In POLY a lone note can land on any of the first five cards (the round-robin), so it can come out flat or sharp.
- **The wander's range** grows with the depth: up to −28 … +29 cents at 1x, −40 … +41 at 1.5x and −51 … +53 at 2x. At
  2x that peaks at about a quarter-tone.
- **Cross-check:** the held note's pitch read off the audio agrees with the engine (1x: −8.7 cents from ride 0 in
  both).

The per-window detail for every card, including the ride-0 windows, is in `numbers.md`. To rebuild everything here:
`python3 tests/trick/slop_depths.py`.
