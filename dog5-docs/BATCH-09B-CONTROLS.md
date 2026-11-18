# Batch 9B: control surface (firmware)

Branch `build/batch-09b-controls`, off `main` at `7a1fba8`. 18 Nov 2026. **Status: BUILT.** Items 1-6 are done and tested on the
host and in the browser build; nothing was run on a real FM-1. Item 7 is a read-only look, nothing implemented.

Every claim below is quoted from the code with file and line, or marked **(inference)**. Line numbers are those of this branch.

## 0. Two things first

- **The Batch 9A report could not be fetched.** `git fetch origin build/batch-09a-control-recon` fails (`couldn't find remote ref`),
  and `git ls-remote origin` lists no branch with that name (41 refs, none for 9A). I re-derived the parameter table, the page
  table and the line references from the code at `main`. Nothing here depends on the 9A text.
- **The audio is bit-identical** (section 8): all four reference patches render to the same WAV as `main`, byte for byte.

## 1. The final page table, as the code builds it (`firmware/src/obv_params.h:155-171`)

21 pages (`_Static_assert(NPAGE == 21 ...)`, :188). `-` = no knob (`-1` in the table: nothing is drawn, a turn does nothing).

| # | Page | Button | KNOB 1 | KNOB 2 | KNOB 3 | KNOB 4 |
|---|---|---|---|---|---|---|
| 0 | DØG-5 (HOME, PERFORM) | HOME | CUTOFF | RESO | ENV AMT | RELEASE (`P_AR`) |
| 1 | OSC 1 | EDIT | WAVE | PW | - | - |
| 2 | OSC 2 | EDIT | WAVE | PW | SEMI | FINE |
| 3 | **MIXER** (new) | EDIT | O1 LVL | O2 LVL | NOISE | DRIVE (`P_DRIVE`) |
| 4 | OSC MOD | EDIT | SYNC | X-MOD | ENV>O2 | - |
| 5 | FILTER | EDIT | RESO | ENV AMT | MORPH | TYPE |
| 6 | FILTER + | EDIT | KEY TRK | VEL>FLT | VEL>AMP | - |
| 7-8 | FILTER ENV, AMP ENV | ENV | (unchanged) | | | |
| 9-11 | LFO, LFO DEST, LFO + | LFO | (unchanged) | | | |
| 12-15 | DRIVE, BBD DELAY, SPRING, TAPE | FX | (unchanged) | | | |
| 16 | ARP | ARP | (unchanged) | | | |
| 17-20 | GLOBAL, VOICE, VOICE +, OUTPUT | GLO | (unchanged) | | | |

- EDIT family = `{PG_OSC1, 6}` (:202), cycle order OSC 1, OSC 2, MIXER, OSC MOD, FILTER, FILTER + (the enum order, :157). Families
  still remember their last page (`fam_note`, unchanged; tests/families.txt, 47 `expect page` checks, all ok).
- **No parameter id moved, the patch record is untouched** (`PATCH_BYTES 96`, `NPARAM` unchanged). `git diff main -- firmware/src`
  touches only `obervave.c`, `obv_params.h`, `obv_ui.h`; `obv_patches.h` and `obv_engine.h` are not in it.
- **One label I had to change.** `P_O1_LVL` and `P_O2_LVL` were both named `LEVEL` in `PDEF` (:68, :72). On the MIXER page that would be
  two knobs reading "LEVEL". I renamed them **`O1 LVL`** and **`O2 LVL`** (the name is the knob label only; it is not stored and not
  a MIDI mapping). Everything else uses the code's own labels. If you want the old name, it is a two-word edit; the page still works.
- The knob label width: the longest label on MIXER is 6 characters; the pages fit the 60 px column.

## 2. Key-index derivation (item 2)

- `fm1_in.notes` bit 0 is F3 and bit 26 is G5 (`firmware/src/platform.c:20`, `firmware/hal/fm1_input.h:89`). `#define KEY0 53u /* key 0 = F3 */`
  (`obervave.c:553`); 53 is F3 in the C4 = 60 numbering.
- The black keys are those whose pitch class is C# D# F# G# A#, i.e. note-key indices **1, 3, 5 | 8, 10 | 13, 15, 17 | 20, 22 | 25**: eleven
  keys in groups of 3, 2, 3, 2, 1. That is the 3 · 2 · 3 · 2 · 1 the brief expects, so the code does not contradict it. It is checked at
  compile time (`IS_BLACK`, two `_Static_assert`s, `obervave.c:579-586`: the ten shortcut keys are black, and a 27-key bed from F has 11).
- Mapping (`enum EK_*`, `obervave.c:574`): OP1 = 1 (F#3), OP2 = 3 (G#3), OP3 = 5 (A#3), OP4 = 8 (C#4), OP5 = 10 (D#4), OP6 = 13 (F#4),
  PIT = 15 (G#4), GLO = 17 (A#4), MONO = 20 (C#5), POLY = 22 (D#5), none = 25 (F#5). By key index, not note number, so the octave
  buttons do not move it.
- **Not verifiable from the code:** that the unit's panel prints OP1 .. POLY over exactly these keys. That is the brief's statement; I took it as given.

## 3. What changed, per item

### Item 1: page table
`obv_params.h`: `PG_MIXER` added to the enum (:157), `PAGE[]` rows (:166-171), `FAM_EDIT` count 6 (:202), assert 21 (:188), the two
level labels (:68, :72), and the stale "REC taps the time" comments on `PG_BBD` / `P_ALLEY`. An empty slot is inert: `draw_page`
sets `present = 0` for `p < 0` and the knob-turn code only acts on `p >= 0` (`obervave.c`, `draw_page` and the knob loop; unchanged code, already used by DRIVE / SPRING / TAPE).
Tests renumbered (the numbers shift from OSC MOD up): `families.txt` regenerated, `map.txt`, `layer_lock.txt`, `drive_page.txt`, `poly.txt`,
`spring_page.txt`, `tape_page.txt`, `bbd_page.txt`, and the page sanity line in the bbd / spring / tape measurement kits (+1).

### Item 2: hold EDIT + key
- **The gate is in `keys_in()`** (`obervave.c:598`), which both the main loop and `app_idle()` call. State: `edit = fm1_in.buttons >> BTN_EDIT & 1`.
  A key going down with `edit` held and in `EDIT_KEYS` (the ten shortcut keys) is **swallowed**: its bit goes in `edit_swallow`, no
  `play_note`, no `midi_send`, and the key index is queued in `edit_q[]` (8 slots). Its release is swallowed too (nothing sounded, so no note-off).
- **No stuck notes:** a key already down when EDIT is pressed has no new edge, so nothing changes: it keeps its note and `held_key[k]` ends it
  as always. A shortcut pressed and EDIT let go first: the key's later release is swallowed, nothing is sent (tests/controls/edit_keys.txt checks both; the host log shows no MIDI out for any shortcut).
- **The jump runs in the main loop** (`edit_key_do`, :624; called at :896, in the order pressed), not inside `keys_in`, because `keys_in` also
  runs mid-draw. Single-page keys stay; OP4 and GLO toggle (`cur == page ? page2 : page`): FILTER <-> FILTER +, GLOBAL <-> OUTPUT; from anywhere else the first press goes to FILTER / GLOBAL.
  A jump goes through the normal `np` path, so `fam_note` updates the family's remembered page, and a locked layer is let go as for any page change. HOME-held-with-a-layer locking is untouched.
- **MONO / POLY** call `set_param(P_MODE, M_MONO / M_POLY)` (the VOICE page's knob path) and show a header readout `MODE MONO` for 1 s (`readout`, :272).
- **EDIT tap acts on release** (:892): `if (rel & EDIT) { if (!edit_used) np = cycle_fam(FAM_EDIT); edit_used = 0; }`. `edit_used` is set when a shortcut key is swallowed.
  **Timing change:** the cycle now happens when the button comes up instead of when it goes down; for a finger tap that is the length of the press (typically tens of ms, I have not
  measured it on the unit). There is no maximum hold time: any EDIT press-and-release with no shortcut cycles, as any press did before. It is the same mechanism as HOME's tap (`home_down`).
- **The key right of POLY (F#5, index 25) is a normal note key** and does not count as "a shortcut used" (it does not suppress the tap). See "ambiguities".

### Item 3: SELECT
- `obervave.c:950`: `if (page == PG_PERFORM && !layer) { set_param(P_LFO_RATE, live.v[P_LFO_RATE] + e * 2); readout("LFO RATE", P_LFO_RATE); dirty_hdr = dirty_page = 1; }`.
  `set_param` clamps 0..127 (`PDEF[P_LFO_RATE].max` = 127) and sets `edited`, so SAVE stores it like a knob. `layer` is non-zero while FX is held or locked, so no layer = no action.
  2 per detent, no acceleration (the knobs' fast-turn x3 is not applied, per the brief).
- **Every other page: nothing.** The old always-on tempo scroll block is gone; the encoder is still drained (`fm1_enc_take`) so turns do not queue up.
- **Tempo is untouched:** `set.tempo` / `ctl_tempo` are written only by GLOBAL knob 1 (`obervave.c`, the `page == PG_GLOBAL` knob branch) and read as before (ARP DIV, BBD SYNC, Tape Stop, the MIDI clock override). Checked on screen: the GLOBAL page before and after a SELECT turn is pixel-identical (tests/controls/select_dial.txt, shots 7800 / 8200).
- **How the two things you named stayed intact:** I replaced only the `ENC_SELECT` (turn) block. *SAVE armed + SELECT press = randomise* is the separate **press** block (`if (b & (1u << BTN_SEL) && save_armed)`), and *SELECT held swaps in the + knobs* is `sel_held()` / `page_now()`; neither was edited. select_dial.txt exercises both (dice gives LFO RATE 50 from the fixed seed; SELECT held on DRIVE, a turn changes nothing) and the existing drive / tape / spring / bbd page tests still pass or fail exactly as on `main`.
- Readout: the header's tag line, `LFO RATE 4.2Hz`, 1 s (see "surprising", the toast).

### Item 4: REC = hold
- `hold_toggle()` (:567) is the single toggle site: `hold ^= 1; ctl_hold = hold; dirty_tags = 1`. The ARP button on its page (:900) and REC (:919, `b & BTN_REC && !layer`, any page) both call it. `ctl_hold` is read in `part_sus()` (`obv_engine.h:313`: `ctl_sustain || ctl_hold`), so it ORs with the pedal as before.
- `alley_tap()` and all its state (`tap_t`, `tap_n`, `tap_sum`, `tap_last_iv`, `tap_msg`, `TAP_GAP_MS`) are deleted. `alley_turn` / ALLEY's knob are unchanged.
- **REC LED:** `fm1_led_key(BTN_REC, hold)` (:1024). Checked in the film log: on at the REC press and at the ARP-button press, off at REC and at STOP, untouched with a layer held.
- **STOP:** when PLAY engages the kill switch, `if (killed && hold) { hold = 0; ctl_hold = 0; dirty_tags = 1; }` (:924). The kill switch's own audio code (`obv_engine.h`) is unchanged.
- **What happens to the hold in every other path (not changed):**
  - *Power-up:* `hold` is a static, 0 at boot, never saved. Off.
  - *STOP resume:* hold was released when STOP engaged and nothing sets it on resume. Off after resume.
  - *MIDI sustain pedal (CC 64):* separate flag `ctl_sustain` (`obervave.c`, `midi_in`); REC and the pedal OR. REC off with the pedal down keeps the notes; pedal up lets them go (tests/controls/rec_hold.txt).
  - *Patch change (PRESETS or MIDI program change):* `load_program` does not touch `hold`; it stays latched (tested).
  - *MIDI panic (CC 120 / 123):* `ctl_panic` clears held notes and releases the voices (`obv_engine.h:361`) but not the `hold` flag, so REC stays lit and the next notes latch again. **(Existing behaviour, not changed; reported because REC now makes it more visible.)**
  - *`KILL_MOMENTARY 1`:* the release also runs when PLAY is held, same line.

### Item 5: hold-HOME map
`ui_map` (`obv_ui.h:195`) and `draw_map` (`obervave.c:490`) rewritten to 13 rows under a 32 px head (`MAP_ROWS 13`, `MAP_HEAD 32`); still draws in two strips, calls `app_idle()` after the head, every row and each strip (DRAW RULE; tests/map.txt still asserts it: "the last map draw called app_idle 16 times", needs >= 10).
Rows: the six page buttons (where a press goes now; ZOOMIES shows HOLD on the ARP page), **HEEL (PLAY) STOP / RESUME**, **FLOP (SEQ) HOLD=TAPE STOP**, **SLOBBER (ALGO) SLOP RIDE**, **WAG (REC) HOLD**, then by page:

| Page | The last three rows |
|---|---|
| EDIT family (6 pages) | three lines of the EDIT-held shortcuts: `OP1 OSC1  OP2 OSC2  OP3 MIXER` / `OP4 FILTER OP5 VOICE MONO POLY` / `OP6 VOICE+ PIT MOD GLO GLOBAL` |
| HOME | FETCH (SELECT) LFO RATE, BURY (SAVE) TAP TWICE, BARKS (PRESETS) SOUND |
| DRIVE / BBD / SPRING / TAPE | FETCH (SELECT) HOLD: X +, BURY (SAVE), BARKS (PRESETS) |
| everything else | BURY (SAVE), BARKS (PRESETS), OCT-/+ OCTAVE |

**Did not fit, so dropped:** the HOME row ("TAP: HOME"), the foot line ("FX HELD: THE 4 MACROS", and the old "WAG (REC): TAP THE TIME" which is now wrong anyway), OCT-/+ on HOME / Psych / EDIT pages, and SAVE / PRESETS / SELECT rows on EDIT pages. The head lost its two rules to a single one. "OP4 again = FILTER +" and "GLO again = OUTPUT" are not on screen (manual). `ALGORITHM` is shown as `SLOBBER (ALGO)` because the full word would have pushed the right column off the screen. Checked on the host's screen PNGs (HOME, FILTER, ARP, DRIVE, SPRING): all text inside 240 px, the longest line (`OP4 FILTER OP5 VOICE MONO POLY`) uses the full width. **Not seen on the real LCD.**

### Item 6: web player and docs
- `sh web/sim/build.sh` rebuilt `docs/play/dog5.wasm` (95849 -> 96165 B) and copied `index.html`. The tools were installed per the script's printed commands (ziglang in a venv, binaryen from npm). `node tests/sim_test.mjs`: **SIM TEST PASSED** (sound = host build sample for sample, 0 differ; three screens 0 pixels differ).
- `web/sim/index.html`: the REC tap-tempo line is gone; it now says REC is HOLD on any page (same latch as ARP on its page, PLAY / STOP lets it go), SELECT sets the LFO rate on HOME only, and a new line describes hold EDIT + a black key. The hint line adds the computer-keyboard way.
- **Can the player do hold EDIT + key? Yes, with no new interface.** `sim.js` holds a button for as long as the pointer is down (`btnDown` / `btnUp`) and every black key has a computer key (`CODEKEY`: 2 3 4 S D G H J L ; for indices 1 3 5 8 10 13 15 17 20 22, and 9 for index 25). So: **keyboard alone** (hold `-`, press a black-key letter), **mouse on EDIT + the computer keys** with the other hand, or **two fingers on a phone**. **Mouse alone cannot** (one pointer). I checked the wasm directly (throwaway script, not committed): EDIT down, key 10 down/up, EDIT up -> the GLO LED lit and EDIT LED off (VOICE page, no cycle on release); a plain EDIT tap from HOME -> EDIT LED on.
- **Docs changed:** `CLAUDE.md` (the facts table's page count, the page table + a new paragraph for the EDIT knobs, the EDIT-held shortcuts, SELECT and REC; the hold-HOME map paragraph; the Psych Chain line and the BBD paragraph that said REC taps the time; "map is full" note). `dog5-docs/`: `DOG-5-base-and-ui-decisions.md` (the EDIT row of the family table, a note under the 19-page total), `DOG-5-presets.md` (two "REC = tap-tempo" lines marked superseded), `DOG-5-foundation.md`, `DOG-5-build-kit.md`, `DOG-5-character-brief.md` (one-line notes on REC). **Not touched:** `dog5-docs/_archive/`, the preserved OberVave section at the bottom of `CLAUDE.md`, `CLAUDE.obervave.md`, earlier `BATCH-*` reports, and the root `README.md` (still OberVave's, describes the sequencer era and "SELECT is the tempo" among much else).

## 4. The exact behaviour as built

- **EDIT:** tap = cycle (on release). Hold + a black key (OP1-OP6, PIT, GLO) = jump; OP4 / GLO again = the second page; MONO / POLY = voice mode; F#5 = a note. A jump counts as "used": letting go of EDIT then does nothing.
- **SELECT:** turn on HOME with no layer = LFO RATE +/- 2 a detent (clamped), header readout; turn anywhere else = nothing. Press (SAVE armed) = dice; held on a Psych page = the + knobs. Tempo: GLOBAL knob 1 and the MIDI clock only.
- **REC:** press, any page, no layer = hold on / off. LED = latched. Released by REC, by the ARP button on its page, or when STOP engages.

## 5. What I could not verify without the unit

- The **EDIT-tap feel** (release vs press latency under a real finger and the real 30 ms-per-draw loop).
- **Key gating on the real keybed:** `fm1_in.buttons` (EDIT) and `fm1_in.notes` (keys) come from the same debounce routine (`hal/fm1_input.h`, `fm1__key`), but I cannot tell if EDIT-then-key within a few ms ever lets the first note through. **(inference: a key that debounces before EDIT's state shows would sound once; the same race exists for any held-button + key combination.)**
- The **REC LED** on the panel (verified only as the LED call in the host log), and the real LCD legibility of the 13-row map.
- The **SMK-37** build compiles, builds (three packages) and runs its default host script, but the shortcuts, REC and SELECT were not exercised on it (its pads feed the same `fm1_in.notes` word; the black keys are keybed-only, **inference**).
- Anything about the printed OP1 .. POLY labels (section 2).

## 6. Ambiguities, and what I chose

1. "The 11 black keys ... must not sound a note" versus "the key right of POLY stays a normal note key even with EDIT held". I made **ten** keys swallowed and the eleventh a normal note, and the eleventh does not count as a used shortcut (so EDIT still cycles on release after it). If you want it to suppress the cycle, it is one line in `keys_in`.
2. "The transient readout a knob does": in this code a knob turn has none outside its own page (see 7.2). I used the header tag line for 1 s, the mechanism CUTOFF and the SLOP ride already use.
3. "Use the labels as they exist": see the O1 / O2 LVL note (section 1).
4. No maximum hold time on the EDIT tap (a long press with no key still cycles).

## 7. Surprising

1. The brief says 28 pre-existing `FAIL` lines on `main`. I count **22** lines containing `FAIL` in the test sections of `run_tests.sh` on `main` and **22** on the branch (in drive_page, tape_page, layer-lock, the installer page and the update loader screen, whose line is "UPDATE FAILED"). The sets are the same: drive_page's two lines carry later timestamps only because I shifted that script by 200 ms for the extra EDIT press (same expectation, same actual value).
2. **`say()` / `toast` is only drawn while a layer is held** (`draw_hints` is called under `if (layer)` in the main loop; `say()` calls such as "OCTAVE 0", "SAVED", and the old "TEMPO n" were therefore invisible on ordinary pages). CLAUDE.md §4 describes `say()` as the knob-readout popup; it is not wired to the screen yet. Not fixed (out of scope); I used the header readout instead.
3. The old SELECT-tempo `say()` was therefore never shown; the tempo turn on any page was silent except on GLOBAL.
4. MIDI panic does not release the hold (section 3, item 4).
5. `tests/bbd/tap_bass.txt` (a Batch BBD measurement kit, not part of `run_tests.sh`) still presses REC to tap tempo; I left it with a note at the top. The other bbd / spring / tape kit scripts only needed their page number bumped.
6. The package (`--release 0.1`) is byte-identical on two builds (reproducible), so the SHA-256 below can be checked by rebuilding from this branch.

## 8. Audio: bit-identical check

`sh tests/controls/bitident.sh main` (new): host builds of `main` and of this tree render `tests/controls/render4.txt` (program changes 2, 13, 27, 29 = patches 03, 14, 28, 30; a bass note + chord, 1.5 s each, plus tails; 837,888 frames) and compare:

```
c0882910b6e4f457aa5f51d372ebfe83087bae0f7b95113d31cda968f10be4d1  (main)
c0882910b6e4f457aa5f51d372ebfe83087bae0f7b95113d31cda968f10be4d1  (this branch)
IDENTICAL
```
All four segments have signal (peaks 21792, 27419, 20405, 13745 of 32767), so the comparison is not of silence. `git diff main -- firmware/src/obv_patches.h` is empty. The web build's sound also equals the host build's (sim_test).

## 9. Build numbers (device image, `./build.sh`, FM-1)

| | 9A baseline (`main`) | this branch | change |
|---|---|---|---|
| image | 82148 B of 581564 | **82352 B** of 581564 | +204 B |
| RAM .data+.bss | 32464 B of 98304 | **32432 B** of 98304 | -32 B |
| pool | 304896 B of 344064 | **304896 B** of 344064 | 0 (no new buffer) |

The build's own checks all print `ok` (`.ram_text: 916 insns, no calls`; the size line above; `register access: hal/ only`). `-Os` unchanged (`tools/build.py`). The three SMK-37 packages also build (`BOARD=smk37`, Pro / Elite / MKE; image 86956 / 86960 / 86944 B). The toolchain came from `tools/get_vendored_deps.sh`.

## 10. Test results

- **`tests/run_tests.sh`:** same failures as `main` (section 7.1: 22 vs 22, identical sections); every new check passes.
- New (added to `run_tests.sh`): `tests/controls/edit_keys.txt` (42 ok), `select_dial.txt` (13 ok), `rec_hold.txt` (18 ok). `families.txt` 47 ok, `map.txt` all ok.
- `node tests/sim_test.mjs`: **SIM TEST PASSED**.
- Host self-tests: `tests/run_host.sh` (FM-1 and SMK-37 default scripts) run clean; the 96-byte program store selftest still passes (both binaries).

## 11. Package

Built the way Batch 7 did (`docs/install/README.md:89`): `./build.sh --release 0.1`.

- Path (in this cloud session's container): `/home/user/dog5/build/dog5-0.1.fwsc` (git-ignored, **not committed**, gone when the session is reclaimed)
- Size 612223 B, identity `FM-1_961`
- **SHA-256 `1dc8465b70f892cb363e05c6a8bd1c1e68af7327b490cb67abb9a9a6ad7cda32`**
- Two builds gave the same hash, so rebuilding this branch gives the same file: `./build.sh --release 0.1` (after `tools/get_vendored_deps.sh`).
- **Note:** `docs/install/dog5-0.1-20261112.fwsc` is a different package (SHA-256 `3de092d5...`) with the **same identity string** `FM-1_961`. If you flash this one, a new release number (`--release 0.2`, `FM-1_962`) would tell them apart on the unit. Your call; I did not bump it.
- **Not done, by instruction:** `docs/install/` is not regenerated. That step would be `python3 tools/make_installer_page.py --release 0.1 --date <YYYY-MM-DD>` (README.md:90), which writes the dated package and `index.html` together.

## 12. Item 7: Psych Chain reorder (read-only; nothing implemented)

**Is the order fixed in code? Yes: it is the call sequence in `engine_audio` (`obv_engine.h:655-709`).**

```
voices
  -> drive_process(out, n, vol_q12)                 GROWL   obv_engine.h:687   (only if drive_on(); on the voice bus)
  -> the output stage: softclip(out * vol_q12 >> 10)        obv_engine.h:689-702
  -> fx_process(out, n)                             ALLEY then DRAIN, one loop   obv_engine.h:706, obv_fx.h:381
  -> tape_process(out, n)                           CHEW    obv_engine.h:707   (only if fx_to_tape)
  -> deck_process(out, n)                           TAPE STOP, after everything  obv_engine.h:708
  -> kill_gate(out, n)                              STOP    obv_engine.h:709
```

**How `obv_fx.h` is wired.** `fx_process` is one per-sample loop; inside it `if (do_dly)` (ALLEY, :392) runs first and adds its wet to `l` / `r`, then `if (do_rev)` (DRAIN, :416) takes `(l + r) >> 1` of that sum as its input. So the order inside the file is fixed by statement order and by the shared locals `l`, `r`. The two stages' memory is one block (`fx_mem[FX_MEM_N]`, :90-95, `.pool`). GROWL and CHEW live in their own files with their own state.

**Things that are not just a reorder of calls (all from the code):**
1. **GROWL works on a different scale.** `drive_process`'s input is the voice bus (it clamps to +-262144 and `>> 2`s to the output stage's scale; "s: the voice bus in, the output stage's scale (the bus >> 2) out", `obv_drive.h:172`), and its loudness trim is measured *through the output stage's tanh with `vol_q12`* (`obv_drive.h:198-199`). The effects and tape work on the output stage's Q15 samples (`obv_fx.h:3`, "the signals are Q15 as the output stage leaves them"). GROWL after the output stage would need a Q15 variant and its loudness law re-checked.
2. **The effects -> tape hand-off is special-cased:** `fx_to_tape` (`obv_fx.h:378`, set at `obv_engine.h:704`) makes `fx_process` skip its `sat16` and use a +-65534 rail so CHEW's own record knee does the rounding (`obv_fx.h:384-388, 436`). CHEW anywhere else needs that rule generalised.
3. **ALLEY and DRAIN share a loop** (point above); swapping them needs two loops (one per order) or a per-sample branch.
4. **Bypass bit-exactness** is per stage (`drive_on()`, `tape_on()`, `dly_active` / `rev_active`) plus the final `sat16` in `fx_process`; the default order's bit-exact bypasses must be kept by leaving the default path as it is.

**CPU and pool cost of a runtime reorder.**
- *The work does not change with the order:* the same four stages run. Measured on the host, while on (`dog5-docs/PERF-BASELINE.md:221`): GROWL 745, ALLEY 346, DRAIN 608, CHEW 966 instr/sample, all four 2,647. The device budget is in the brief (aim < 2900 us; device numbers for these stages are not recorded here).
- *The cost of the mechanism* (**inference, not measured**): two code paths for ALLEY / DRAIN, or one extra pass over the buffer per stage that moves, at roughly a load, a clamp and a store per sample per extra pass (single-digit to low-double-digit instructions per sample); +1-2 KB of image (there is room: 82352 of 581564 B). The fused loop was already sensitive to inlining (comment at `obv_fx.h:381`: "inlined, it moved the voice loop: +28 a sample with the effects off"), so any restructure needs a measurement.
- *Pool:* **0 extra** if each stage keeps its own buffer (the buffers do not depend on position): `fx_mem` (2 x 32768 + `REV_N` int16), `tp_line` (2 x 1024 int16, `obv_tape.h:39`), `dk_line` (`obv_deck.h:30`, 96 KB). **A second chain to crossfade between two orders would not fit:** pool free is 344064 - 304896 = **39,168 B**, and the effects' memory alone is over 140 KB (**inference** from `FX_MEM_N`).

**Where a per-patch order could be stored.** `obv_params.h:35-39`: parameters are bytes 0-79, **71 used (0-63, TAPE 64-67, ALLEY 68-70); 71-79 free**; the name is 80-93 and **94-95 are spare**. A permutation of four stages is 24 values: one byte, e.g. a new parameter appended at id 71 (the way `P_POLY_N`, TAPE and ALLEY were appended), default 0 = today's order, with a CC from the end of the map. `patch_defaults` zero-fills 71-79 (`obv_params.h:212`: "unused param space (71-79) + spare (94-95)").
- *Patches already saved:* **(inference)** their bytes 71-79 are 0 (they were saved from `live`, which starts from `patch_defaults`; `randomize()` writes only `i < NPARAM` and MIDI CC only reaches mapped ids), so they would load as order 0 = the current order, bit for bit, and the 32 factory patches the same (they are built over the defaults, `patch_from_factory`). No format version bump, no sector change. An older firmware would ignore the byte.
- *Alternative:* a global setting (the settings struct's unused `pat` / `click` bytes, `obervave.c` `set`) avoids the per-patch question but not the tail problem below.

**What changes in level or feedback with another order (all inference; not measured):**
- *GROWL after the delay / spring:* the repeats and the tail are driven too (a delay repeat distorts, a reverb tail is pushed into the clip and its noise floor rises); the loudness law (a static makeup for "one voice's saw at its own RMS", plus a ~1.5 s K-weighted trim) was fitted for the dry voice bus, so a reverb-heavy input would settle more slowly and could pump.
- *DRAIN before ALLEY:* the spring tail enters the BBD loop, each pass is band-limited (8 kHz at 10 ms down to 2.8 kHz at 740 ms) and high-passed at 80 Hz; at FEEDBK above ~120 the loop runs away and `bbd_sat` limits it, with a denser, longer input than a played note, so it saturates sooner.
- *CHEW before ALLEY / DRAIN:* the wow, flutter, dropouts and **hiss** go into the feedback: wobble and dropouts are echoed, the hiss builds up by about 1 / (1 - feedback). CHEW's hiss gate (rests 2 s after silence) and its trim assume it is last. The `fx_to_tape` hand-off would no longer apply.
- *TAPE STOP* stays after everything, so it is independent of the order (`obv_engine.h:708`).

**What stands in the way (summary):** (a) GROWL's scale and loudness law; (b) the `fx_to_tape` rail rule; (c) the fused ALLEY / DRAIN loop; (d) **a click-free switch**: a stage holds history (ALLEY 743 ms a side, the spring ~66 ms tank plus its pre-delay, CHEW 11.6 ms), so changing the order live or on a patch change would move audio from one place in the chain to another. Crossfading two chains does not fit in the pool; a short duck (fade out, switch, fade in) in the manner of the kill gate (`KILL_FADE` 256 samples, `obv_engine.h:615`) costs no memory. Today a patch change leaves the tails ringing (**inference**: `load_program` only copies parameters); a per-patch order would make that a decision. (e) The keybed UI to pick among 24 orders is not in scope here. The default order and its bit-exact bypasses stay untouched in every case above.
