# The live tricks: listening kit

Three performance controls on the buttons and the encoder that the deleted sequencer left free. All three are
**global and live**: no patch byte, no MIDI CC and no factory patch was touched. When you don't use them, the output
is **bit for bit what it was before** (checked on six renders: the default script, the tape toggle, a BBD runaway,
two full-chain combos and the factory bank).

| control | dog name | what it does |
|---|---|---|
| **PLAY** (tap) | HEEL | **STOP**, the kill switch. A tap silences everything; another tap brings it back. The PLAY LED is lit and the header says `STOPPED (PLAY)` while it's stopped |
| **SEQ** (hold) | FLOP | **TAPE STOP**. Hold it and the deck loses power: the whole mix (voices, GROWL, ALLEY's repeats, DRAIN's tail, CHEW's hiss) slows and darkens together. Let go and it snaps back. The SEQ LED is lit while you hold it |
| **ALGORITHM** (turn) | SLOBBER | **SLOP**, a ride on top of the sound's VINTAGE, on any page. The header shows `SLOP +N = VINTAGE M` for a second |

Everything here was rendered by the host build (`tests/host.c` runs the firmware's own integer code). The files are
16-bit stereo, 44.1 kHz, cut to start just before the first note. To rebuild the kit: `python3 tests/trick/make_kit.py`
(it writes the scripts to `build/trick/`, renders them, measures them and draws the two pictures).

## The files

| file | what to listen for |
|---|---|
| `kill_fullchain.wav` | Red Pill's riff through the whole chain, all of it hard: GROWL 127, ALLEY at FEEDBK 124 (close to runaway), DRAIN 60, CHEW 127. **At 2.33 s** STOP lands mid-note. PLAY comes at 3.85 s and the riff starts again with **no tail coming back**. Then the riff ends and the repeats build up. **At 8.65 s** STOP lands in the middle of them. PLAY comes at 9.35 s, followed by **silence**: the lines were cleared, not muted |
| `kill_fullchain_REF.wav` | the same take without STOP. This is what the two STOPs cut off: a tail of up to 12,000 peak |
| `tapestop_chord.wav` | a held Cm7 pad (spread, a little ALLEY and DRAIN). **At 1.45 s** a short dab (0.35 s): a sag, let go mid-dive. **At 2.95 s** a full hold (1.6 s) to the stop, then let go. The delay's repeats and the spring's tail dive with the chord, and the stop is silent |
| `tapestop_chord_APPROVED_per_voice.wav` | **the A/B reference**: the same take on the approved per-voice dive of 3 Nov (the voices dived; the delay and spring kept their pitch and rang on through the stop) |
| `tapestop_bass.wav` | Red Pill's riff. TAPE STOP is held over the end of bar 2 as a power-down ending, then the riff goes on |
| `tapestop_bass_APPROVED_per_voice.wav` | the same on the approved per-voice dive |
| `slop_note.wav` | one held A4 (a saw, the filter half shut). It sits plain for 3 s at the patch's own VINTAGE 30. Then the ride turns to its top (+254, the shipped 2x depth) over 4 s, holds there for 4 s, and comes back to 0 over 2 s |
| `slop_chord.wav` | the same ride under the Cm7 pad (4 voices drifting apart, then together again) |
| `tapestop.png` | the pitch and the level of one saw (C5) through a 1.5 s hold, then let go |
| `slop.png` | the pitch of the held A4 through the ride |

## The measurements

**STOP** (`kill_fullchain`):

| | STOP 1 (mid-note) | STOP 2 (runaway tail) |
|---|---|---|
| last non-zero sample after the press | 2.0 ms | 3.6 ms |
| largest sample-to-sample step in the fade | 272 | 416 |
| largest step while playing, the 0.5 s before | 996 | 602 |
| peak after PLAY, before the next note | **0** | **0** |
| the same window without STOP | 5,493 | 12,093 |

- The fade is a straight line over 256 samples (5.8 ms). Its steps are smaller than the music's own, so there is no
  click.
- Host timing runs about one block ahead of the clock. On the device, expect press to silence in ≤ 11.6 ms: up to one
  audio block (5.8 ms) for the press to land, then the 5.8 ms fade.

**TAPE STOP** (`tapestop_note`, at 120 BPM; the same to ±0.2 st as the approved per-voice dive, see the A/B below):

| held for | pitch |
|---|---|
| 0 ms | 515 Hz (−0.3 st) |
| 250 ms | 388 Hz (−5.2 st) |
| 500 ms | 261 Hz (**−12.0 st**, an octave) |
| 600 ms | 211 Hz (−15.7 st) |
| 700 ms | 161 Hz (−20.4 st) |
| 800 ms | 111 Hz (−26.8 st) |

- The frequency falls in a straight line. That is a constant deceleration, the turntable-brake / tape-power-off curve:
  a slow sag, then the plunge.
- The level stays flat down to −19 st, then falls to silence by 1.0 s.
- Let go: the sound is back at once, the pitch is within −0.04 st 20 ms later, and the live mix crossfades back in
  over 5.8 ms.

**TAPE STOP, A/B against the approved render** (`tests/trick/tapestop_ab.py`: the approved per-voice build against
this one, on the same scripts). The chord's full hold, from the press:

| from the press | level, approved / new (dB) | brightness (spectral centroid), approved / new (Hz) |
|---|---|---|
| 0 ms | −14.4 / −15.9 | 943 / 1,095 |
| 200 ms | −15.5 / −16.3 | 789 / 848 |
| 400 ms | −16.4 / −16.9 | 624 / 599 |
| 600 ms | −16.7 / −16.5 | 449 / 443 |
| 700 ms | −16.4 / −16.5 | 326 / 331 |
| 800 ms | −21.3 / −20.7 | 286 / 198 |
| 900 ms | −27.2 / −29.1 | 427 / 130 |
| 1000 ms | −34.3 / −48.5 | 469 / 254 |
| 1100–1500 ms (held at the stop) | −41 … −56 / **silent** | 445–889 / — |

- **The pitch curve, the brightness and the level match through the whole audible dive.**
- **The one difference is the stop itself.** The approved render's delay repeats and spring tail stayed at their own
  pitch, so they rang on through the stop, undived, fading from −34 to −56 dB. Now they dive with everything else and
  the stop is silent: one motor.
- **No clicks**, on the chord's left channel (largest sample step / largest second difference; the playing window
  holds the delay's repeats, which differ between the two builds):

  | | approved | new |
  |---|---|---|
  | playing (a 1 s window) | 2,874 / 774 | 3,298 / 968 |
  | dab press | 2,536 / 732 | 2,542 / 735 |
  | dab release | 2,525 / 701 | 2,448 / 725 |
  | hold press | 1,598 / 572 | 1,820 / 570 |
  | hold release | 1,938 / 442 | 1,601 / 577 |

**SLOP** (`slop_note`, a held A4):

| ride | pitch, mean | wander, sd | range |
|---|---|---|---|
| 0 (VINTAGE 30) | −2.5 cents | 0.7 | −3.9 … −0.6 |
| full, +254 (VINTAGE 284) | −20.2 cents | 8.3 | −41.4 … +0.5 |
| back to 0 | −2.1 cents | 0.8 | −3.7 … +0.3 |

- Turning the ride adds no click or zipper.
  - On the note, the largest sample step while it turns is the same as before it (390 = 390).
  - On the chord it is 3,848 against 3,298, but that step sits in a smooth swing at a beating peak (the voices drift
    apart, so their sum peaks higher). The second difference of the signal, where a click or zipper would show, holds
    at 126–134 RMS through the whole ride.
- The three depths that were compared, with per-voice numbers: `slop_depths/` (2x was chosen).

## How each one works

**STOP** (`obv_engine.h`, `kill_gate` / `kill_clear`) is a master gate after everything, the brief's MASTER GATE
place after CHEW.
- Pressed: a 5.8 ms linear fade, then a clear, not a mute, of everything:
  - every voice (envelopes, filters, amps),
  - the held keys, the arp and the queued notes,
  - GROWL's oversampling filters (`drive_clear`),
  - ALLEY's two lines and BBD filters, and DRAIN's whole tank, chirps and pre-delay (`fx_clear`),
  - CHEW's tape line, filters, hiss gate and any dropout (`tape_clear`; the transport keeps turning, so a running
    CHEW doesn't spin up again).
- While stopped, the engine renders nothing and drops incoming notes.
- PLAY again: it starts from that silence, the gate opening over 5.8 ms. A key still held from before stays silent
  until it is played again.
- **Tap or hold?** It's a tap (toggle), as recommended. A kill switch on a live stage must stay down while you do
  something else (change a patch, talk, wait for the drummer), and the LED plus the header make a forgotten STOP
  obvious. A momentary chop is less useful here because the clear means nothing can resume on release.
  `#define KILL_MOMENTARY 1` in `obervave.c` makes it silence only while held: one line.
- **Cost:**
  - Untouched, two compares per audio block.
  - While it fades, one multiply per sample for one block.
  - The clear runs once: ~150 KB of zeroing in a block that renders nothing else.
  - Pool +0. RAM for all three tricks: under 64 bytes.

**TAPE STOP** (`obv_deck.h`, `deck_process`) is one stage at the very end: after the whole mix is summed (voices,
GROWL, ALLEY, DRAIN, CHEW) and before STOP's gate. It replaces the per-voice dive; nothing of that is left.
- The mix goes into a history line and is read back **falling behind as the speed drops**. The read is tape's 6-point
  read (`tp_taps`, the one CHEW's wow and flutter use), here on a 1x line: flat to 10 kHz, −1.7 dB at 15 kHz at worst.
- **One low-pass** for both channels, the voices' SVF (`svf_coef` and the plain stage `svf_lp`: the band-pass state's
  soft knee would colour a full-scale mix). It closes from wide open (19.8 kHz) by 1.25× the dive in semitones,
  which matches the approved render's brightness (table above).
- **The level** stays flat to a third of the speed, then goes to nothing with it. A stopped deck is silent.
- **The curve** is the approved one: the speed falls in a straight line over half a bar at the tempo (1 s at 120 BPM).
  The clamp is now **0.5–1.1 s** (was 2 s). The read falls behind by half the stop time, and that is what the line
  holds.
- **Press:** the read starts 3 samples behind the live mix, crossfaded in over 128 samples (no jump).
- **Let go:** the live mix (the effects ran on underneath) crossfades back over 5.8 ms, then the stage rests.
  - No pitch "catch" this time: the old 10 ms return swing is now the crossfade.
  - Nothing is latched: `T expect rest 1` proves it.
- **At rest** only the last 16 frames of each block are recorded (the press needs 3) and the output is untouched, bit
  for bit.
- **Cost (host instructions per sample, callgrind, the pad):**
  - At rest +0.8 (the full chain: −6, layout noise).
  - **While held or fading back: +140.** The per-voice dive was +3: it only nudged per-block numbers.
  - So the shared stage is **not** cheaper, it is ~45× dearer while it runs. That is the price of really resampling
    and filtering the whole mix. +140 is ~5 % of the full chain's 2,510.
- **Memory:** **pool +98,304 B** (the line: 24,576 stereo frames, 557 ms; the per-voice dive took none). The device
  pool goes 206,592 → 304,896 of 344,064 B (39 KB left). RAM about +40 B.
- `STOP` clears the line too (`deck_clear`). `TS_DIVE8` (`tools/gen_tables.py`) now drives the filter only: the pitch
  comes from the read itself.

**SLOP** (`obv_engine.h`, `block_globals`): the encoder drives `ctl_slop` (0..127, 2 a detent, ×3 on a fast turn),
doubled on its way into the engine (the 2x depth, chosen by ear on 3 Nov from `slop_depths/`).
- It glides into the engine (~23 ms, as CUTOFF does), so even a fast turn swells smoothly.
- It is **added** to the patch's VINTAGE, 0..254 on top. The sum runs to 381 (three times the knob's top) through
  VINTAGE's own law: the
  voice cards' fixed tune, cutoff and envelope offsets, and the slow random walk on each voice's pitch.
- Never stored, 0 at power-on, the same on every patch and every page.
- **Cost:** +0.7 instr/sample while it's up.

## How SLOP and the patch's VINTAGE interact

The patch's VINTAGE is the sound's voiced character. It is still set on OUTPUT, still saved, still sent on its CC, and
the ride never changes it (the patch isn't even marked edited). **The ride is a performance excursion on top: what
sounds is VINTAGE + ride**, and the header shows both for a second whenever it turns (`SLOP +40 = VINTAGE 70`).

- Because it adds rather than replaces, a patch voiced at VINTAGE 80 never gets *cleaner* by touching the ride, and a
  clean patch (VINTAGE 0) only gets the ride's slop. There's no "which one wins" moment, and no jump when the ride is
  first touched.
- It persists across patch changes. That's deliberate: it's a stage control, like the MASTER knob.

**Flagged:**
- It also persists across a STOP and has no reset gesture other than turning it back down. The header readout is the
  only display until the Stage 3 transient readout lands.
- **Accepted character, not a bug:** at full ride each voice sits off true by its own fixed VINTAGE offset, on top
  of the wander. Voice card 0 (every MONO/UNISON note) is about 20 cents flat; it was about 10 at 1x and is doubled at
  this range. Other cards sit sharp, so a chord averages about 3 cents flat. This was heard and approved on 3 Nov, so
  don't "fix" it.

## Tests

`tests/run_tests.sh` runs all six scripts. Each fails on a miss.

| script | what it checks |
|---|---|
| `tests/trick/kill_note.txt` | mid single-note: silent within 15 ms; nothing on PLAY with the key still held; a new note plays |
| `tests/trick/kill_runaway.txt` | mid-chord with a runaway BBD and the whole chain on: silent; 2.35 s of exact zero after PLAY; a new chord plays |
| `tests/trick/kill_reverb.txt` | a 3 s spring tail with CHEW: silent; 2.85 s of exact zero after PLAY (no tail, no hiss) |
| `tests/trick/tapestop_chord.txt` | the dive goes silent while held; on release the sound is back within 100 ms and every trick state is at rest |
| `tests/trick/tapestop_tail.txt` | SEQ held in a long spring + BBD tail: the tail itself stops (exact zero; the old per-voice dive left 952 ringing, and fails this); on release the live tail is back and the tricks are at rest |
| `tests/trick/slop_ride.txt` | the ride on two pages; the VINTAGE byte stays 30; back at 0 it adds nothing |

These rely on new host commands in `tests/host.c`: `T expect peak MS MAX`, `T expect peakmin MS MIN` and
`T expect rest R`.
