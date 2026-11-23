# DØG-5 — DRIVER MANUAL (Draft 1)

*Free, open-source custom firmware for the M-VAVE FM-1. Forked from OberVave. GPL-3.0.*

**Draft 1 — 3 Nov 2026.**
- **12 Nov, the Chapter IV checkpoint.** All four chapters are complete and all 32 patches are voiced. DØG-5 v0.1 was installed on Vincent's FM-1. The controls, keybed, CPU-meter and dictionary sections below carry what that showed. The dictionary gained Bell, Ring, Chime (band-limited) and Blank slate. Part 4 gear inspirations and Part 5 voicing notes now cover all 32.
- **18 Nov, v0.2** (`FM-1_962`, flashed and tested on the unit). Parts 1.1, 1.2 and 1.5 were rewritten for the Batch 9B controls (21 pages with MIXER, REC = HOLD, SELECT = LFO RATE on HOME, hold EDIT + a black key). Part 1.7 was added (plain-language knob hints), and the dictionary's DRIVE and MORPH pointers were corrected.
- **23 Nov, Batch 30.** Parts 2 and 2B rewritten for players: each word's meaning and how to get more of it, with the measurements moved to the records doc (repo `dog5-docs/manual/DOG-5-driver-manual-records.md`). Parts 3–4 are now generated from the voice cards.
- **23 Nov, bullet pass.** Every list in Parts 0–2 read for need and order: dev notes out of Part 0, the filter and LFO lines in 1.4 corrected, the bank line points to 1.9, 1.9 reordered, 1.10 gains "keep the installer tab in front", Dirt & aggression reordered. The cards' "How to play it" is now **Sound design notes** (Part 3 too).
- **21 Nov, v0.4.4** (flashed and tested on the unit). Parts 1.1, 1.2, 1.4 and 1.6 were updated: the SAVE lock, a MIDI panic releasing HOLD, FLEAS on the GLOBAL page, and the CPU reading at the top of GLOBAL. Part 1.8 was added (the screen: the boot animation, HOME's scene, the dial, the fence, FLEAS), and so were Part 1.9 (saving: THE POUND and THE PACK) and Part 1.10 (installing, leaving, coming back).

This is the single source of truth for controls, voicing vocabulary, and the 32 patches. It combines and supersedes the earlier Button Matrix and Knob Parameter Map docs. Controls are drawn from the live firmware (`main` branch). Every patch description is the approved player-facing description of a **VOICED** patch. Vincent edits this draft; at release (Stage 4) it becomes the public user manual.


> **This manual is split across three Project docs (it outgrew one):** `DOG-5-driver-manual.md` (Parts 0–2B: what it is, the panel and screen, the voicing dictionary, number conventions), `DOG-5-driver-manual-patches.md` (Part 3 the 32 patches, Part 4 gear inspirations), `DOG-5-driver-manual-voicing-notes.md` (Part 5 internal voicing notes, Appendix). Together they are the single source of truth. First real-hardware readings: `DOG-5-device-test-1.md`.

---

## 0. WHAT DØG-5 IS

DØG-5 turns the M-VAVE FM-1 pocket synth into an aggressive, live, virtual-analog voice for the band DØGS
(bubblegum egg punk / garage psych). It is an 8-voice analog-style polysynth with a four-stage "Psych Chain"
effect engine and a hard-chopping performance architecture built for the stage.

**The one idea:** the on-screen character is a dog, and his bark **is** the live oscilloscope — the real
waveform of whatever you're playing fires out of his open mouth. The sound you shape is the sound of his bark.

**Two rules govern everything:**
- **TONE IS KING.** Features are negotiable; tone is not. A patch that isn't right by ear doesn't ship.
- **This is a LIVE instrument.** Everything is built to be played in the dark, mid-performance, without
  menu-diving.

---

## PART 1 — THE PANEL

### 1.1 Buttons / the 12-pad command grid

DØG-5 uses **page-family buttons**: tapping a family button cycles through its pages, and each page maps the
four knobs to four parameters. Every button also has a "dog name" (the live performance register); the printed
panel label is what's physically on the unit.

**Top row — synthesis & modifiers**

| Button | Dog name | What it does |
|---|---|---|
| **FX** | — | Psych Chain family. Tap cycles DRIVE · BBD DELAY · SPRING · TAPE. Hold = the four effect macros on the knobs (GROWL · ALLEY · DRAIN · CHEW), on any page. |
| **SEL** (dial + press) | FETCH | **Turned on HOME** (no button held): the **LFO RATE** of the patch, 2 steps a click, saved with the patch; it shows as a dial labelled `LFO` at the top left of the scene (see 1.8). Turned anywhere else: nothing. **Held on a Psych page:** the knobs become that effect's secondary controls. **With SAVE armed, pressed:** randomise (new sound). |
| **ENV** | HOWL | Envelopes family. Tap cycles FILTER ENV · AMP ENV. |
| **LFO** | PANT | Modulation family. Tap cycles LFO · LFO DEST · LFO +. |
| **EDIT** | DIG | Voice family. Tap cycles OSC 1 · OSC 2 · MIXER · OSC MOD · FILTER · FILTER + (on release). **Hold EDIT + a black key** jumps straight to a page (see 1.5). |
| **GLO** | FLEAS | System family. Tap cycles GLOBAL · VOICE · VOICE + · OUTPUT. **The GLOBAL page carries the CPU reading (see 1.6) and the FLEAS dial (see 1.8).** |

**Bottom row — performance & transport**

| Button | Dog name | What it does |
|---|---|---|
| **HOME** | — | **Tap** (acts on release): back to the live PERFORM page, the dog's scene. **Hold:** the control map of the page you are on (every knob and button, with its dog name and panel label); let go and you stay on the page. While a family button is held, tap HOME to lock that layer open; that button releases it. |
| **SAVE** | BURY | Tap to arm, tap again to save. Armed, the header shows the slot it will save into and what is there now (`SAVE HERE?`); turn PRESETS to pick another slot. Factory slots 1–32 are locked, so on one of those SAVE offers the first free slot from 33. Armed does nothing for 3 seconds: it lets go. See 1.9. |
| **ARP** | ZOOMIES | Arpeggiator page / on-off. On the ARP page, the ARP button also toggles **HOLD** (the same latch as REC). |
| **REC** | WAG | **HOLD**, on any page: press to latch the notes you are holding (they keep sounding after you let go), press again to release them. The REC light shows it. A drone latch: with the arpeggiator **OFF**, held notes simply ring. It is the same latch as the ARP button on its page and works alongside a sustain pedal. **Changing patch does not release it; STOP does, and so does a MIDI panic** ("all notes off" / "all sound off", CC 123 / 120, from a keyboard or DAW). |
| **PLAY/STOP** | HEEL | **Global kill switch** (see 1.3). It also releases HOLD. |
| **SEQ** | FLOP | **Tape Stop** (see 1.3). |

**Left panel**

| Control | Dog name | What it does |
|---|---|---|
| **PRESETS** | BARKS | Load a preset slot, instant, no confirm. With SAVE armed: picks the slot to save into (33–99 only). |
| **ALGORITHM** | SLOBBER | **Vintage Slop ride** (see 1.3). |
| **MASTER** | — | Master volume. |
| **OCT− / OCT+** | — | Octave −2..+2 (both pressed = 0). |

*The hold-HOME control map lists the three tricks (HEEL STOP, FLOP TAPE STOP, SLOBBER SLOP RIDE) and WAG HOLD.
To fit the screen it leaves out the HOME row itself and the FX-held macros (both are in this table).*

### 1.2 The knobs & the 21 pages

Four knobs, contextual to the page showing. Each parameter page shows its four knobs and their values, and
draws what they affect. On HOME a turned knob pops up as a dial over the scene for a moment (see 1.8). The
**bottom bar always shows only the preset number + name**. Hold **HOME** for a live control map of the current page.

| Family | Page | Knob 1 | Knob 2 | Knob 3 | Knob 4 |
|---|---|---|---|---|---|
| HOME | **DØG-5** (PERFORM) | CUTOFF | RESO | ENV AMT | RELEASE |
| EDIT | OSC 1 | WAVE | PW | — | — |
| EDIT | OSC 2 | WAVE | PW | SEMI | FINE |
| EDIT | MIXER | O1 LVL | O2 LVL | NOISE | DRIVE |
| EDIT | OSC MOD | SYNC | X-MOD | ENV>O2 | — |
| EDIT | FILTER | RESO | ENV AMT | MORPH | TYPE |
| EDIT | FILTER + | KEY TRK | VEL>FLT | VEL>AMP | — |
| ENV | FILTER ENV | ATTACK | DECAY | SUSTAIN | RELEASE |
| ENV | AMP ENV | ATTACK | DECAY | SUSTAIN | RELEASE |
| LFO | LFO | SHAPE | RATE | DELAY | PHASE |
| LFO | LFO DEST | PITCH | PWM | FILTER | AMP |
| LFO | LFO + | PITCH> | PWM> | — | — |
| FX | DRIVE | GROWL | — | — | — |
| FX | BBD DELAY | ALLEY | FEEDBK | TONE | MIX |
| FX | SPRING | DRAIN | — | — | — |
| FX | TAPE | CHEW | — | — | — |
| ARP | ARP | ARP | DIV | OCTAVES | GATE |
| GLO | GLOBAL | TEMPO | FLEAS | MIDI CH | TUNE |
| GLO | VOICE | MODE | VOICES | DETUNE | GLIDE |
| GLO | VOICE + | POLY | — | — | — |
| GLO | OUTPUT | VINTAGE | SPREAD | BEND | VOLUME |

*GLOBAL's knobs are settings for the whole unit, not the patch: TEMPO, FLEAS (the screen, see 1.8), the MIDI
channel (OMNI or 1–16) and TUNE. The CPU reading sits at the top of the GLOBAL page (see 1.6).*

*MIXER's DRIVE is the per-voice drive in front of the filter (the gentle warmth), not GROWL. **MORPH only acts
when the filter TYPE is SEM** (it sweeps that filter from low-pass through notch to high-pass); on the other
types it does nothing.*

**Hold SELECT on a Psych Chain page** for its secondary controls: DRIVE → BIAS · TONE · BBD DELAY → SYNC
(the note value) · FINE · PINGPONG · SPRING → SIZE · DAMP · PRE-DLY · TAPE → WOW/FLT · HISS · DROPS.

**The tempo** (the arpeggiator and a synced delay) is GLOBAL knob 1, or an incoming MIDI clock. There is no tap
tempo.

### 1.3 The live "trick" controls

Three controls built for live chaos, independent of the patch you're on:

- **PLAY/STOP — Global kill switch (HEEL).** A live panic button. One press and everything stops in a few
  milliseconds: voices, and every effect buffer (delay, reverb, tape) flushed clean, so nothing rings on.
  Instant dead air — for a band stop, or when the delay runs away. Press again to resume. It also lets go of HOLD.
- **SEQ (held) — Tape Stop.** Hold it and the whole sound drags down to a halt like a tape machine or
  turntable losing power: pitch, brightness and all — voices, delay repeats, reverb tail and tape hiss dive
  together. Release and it snaps straight back. The dog's beam dives with it.
- **ALGORITHM — Vintage Slop ride (SLOBBER).** A live knob that rides the per-voice tuning instability up on
  top of whatever the patch already has. Clean and stable at zero; wound up full, it's worn, drifting,
  seasick. Never saved — resets to zero at power-up, like a master knob. At full ride, a held single note
  sits about 20 cents flat (a chord about 3 cents flat); that detune is the character, not a fault.

### 1.4 The signal path & architecture

```
VOICES → DRIVE (GROWL) → BBD DELAY (ALLEY) → SPRING (DRAIN) → TAPE (CHEW) → TAPE STOP → MASTER GATE
```

- **8 voices.** Modes: POLY, DUAL, UNISON, MONO. Variable polyphony (POLY knob, 1–8, default 5).
- **Per voice:** two oscillators (saw / pulse / both), hard sync, cross-mod, noise, a filter with drive (LP 24,
  LP 12, HP, BP, notch or SEM: see TYPE in 1.7), two ADSR envelopes, and "Vintage Slop" (per-voice tuning/drift
  instability). There is no triangle oscillator; a narrow pulse through a key-tracking low-pass is the nearest.
- **One LFO per patch:** everything it is routed to moves at the same rate. It cannot be tempo-synced.
- **The Psych Chain** sits after the voices, reached by FX. It is the DØG-5 dirt: Drive, a free-time
  bucket-brigade delay, a spring reverb, and tape degrade. The tape stage is last, so it wobbles the finished
  wet mix: a delay repeat is pitched by the tape's state when it arrives, and everything wobbles together
  (a real tape echo warps each repeat separately; this cannot).
- **The bank:** 99 slots. **THE POUND (1–32)** are the factory patches, locked: you can play and change them,
  but a save never lands on them (see 1.9). **THE PACK (33–99)** are yours to save into; an unused one starts as
  the INIT sound (slot 32's engine defaults at VOLUME 100).

### 1.5 The keybed shortcuts (hold EDIT + a black key)

The FM-1 prints a second set of labels on the keybed's **upper (black) row, left to right: OP1 OP2 OP3 · OP4
OP5 · OP6 PIT GLO · MONO POLY**, with one unlabelled key to the right of POLY. **Hold EDIT and press one of them**
to jump straight to a page, wherever you are:

| Key | Goes to |
|---|---|
| **OP1** | OSC 1 |
| **OP2** | OSC 2 |
| **OP3** | MIXER |
| **OP4** | FILTER (press again: FILTER +) |
| **OP5** | VOICE |
| **OP6** | VOICE + |
| **PIT** | OSC MOD |
| **GLO** | GLOBAL (press again: OUTPUT) |
| **MONO / POLY** | sets the patch's voice MODE to MONO or POLY (the header shows `MODE MONO`) |

While EDIT is held these keys **never play a note** and send no MIDI. The key right of POLY always stays a
note. A jump also becomes the page EDIT (or GLO) returns to next time. A plain tap on EDIT still cycles its pages,
on release; if you used a shortcut during the hold, the release does not cycle. *(In the browser player:
hold `-` for EDIT and press a black-key letter; a mouse alone can't hold two things.)*

### 1.6 The CPU meter (it is already there)

**Press GLO once** (it opens the GLOBAL page, the first in the GLO family). The top of the page reads `CPU <n>us`:
how long the engine took to render the last chunk of audio, in microseconds. **The source states the budget is
5800 µs** for each chunk. The nearer the number is to 5800, the less room is left for the patch, the held notes and
the Psych Chain together. It measures only the audio render; the screen, knobs and buttons run separately.

*What was measured on Vincent's unit (12 Nov, readings drift by about ±100 µs; all four Psych Chain effects
pushed hard — GROWL 82, ALLEY 443 ms, DRAIN 83, CHEW 85):* with no note held the meter reads about 2700–3200 µs;
with four notes held, 4500–4900 µs on most patches and about 5600 µs on 30 THE DØG. Playing 30 at that level
the screen, knobs and sound all responded normally. *Since the screen art (v0.4, 20–21 Nov):* ordinary playing
reads no higher than about 3000 µs, and FLEAS at MANGE does not raise it: the scene does not slow the sound.
**Not tested:** more than four notes, any reading above 5800, and what happens past the budget. So this manual
does not promise what happens there. The Psych Chain's crackle and dropout are part of the sound.

### 1.7 The steering knobs, in plain words

There is no room on the screen for explanations, so they live here. These are the knobs that change a sound the
most:

- **CUTOFF** — how bright the sound is. Down = darker and rounder, up = brighter and more open.
- **RESO** — how much the filter rings at the cutoff. Up = a sharper, whistling edge; near the top it sings on its own.
- **ENV AMT** — how hard the filter envelope sweeps the cutoff on each note. The middle (64) = no sweep; above it
  the sound opens with each note (a "wow" or a bite), below it the sweep goes the other way.
- **RELEASE** — how long a note rings after you let go of the key.
- **LFO RATE** (the SELECT dial on HOME) — the speed of the patch's one wobble, whatever it is routed to.
- **TYPE** — the filter's shape: LP 12, LP 24 (darker, steeper), HP 12 (takes the low end away), BP 12 (a narrow,
  nasal band), NOTCH (a hole in the middle), SEM (a sweepable filter: see MORPH).
- **MORPH** — only on TYPE SEM: sweeps the filter from low-pass (0) through notch (64) to high-pass (127).
- **GROWL · ALLEY · DRAIN · CHEW** — the four Psych Chain effects: drive, echo, spring reverb, tape. Hold FX and
  all four are on the knobs, on any page.

### 1.8 The screen

**Power-on: the boot animation.** About 6 seconds: the head, the colours cycling, DØG-5, then it melts and burns
through to your patch's scene. **Press any key or button and it skips straight to playing.**

**HOME is the dog's scene.** Each patch lives in one of four chapters, and HOME shows that chapter's painting with
the dog in it:

| Slots | Chapter | Accent colour |
|---|---|---|
| 1–8 | I JALOPY | Sun Yellow |
| 9–16 | II BEE-TCH | Wave Turquoise |
| 17–24 | III MOONSHINE | Foam White |
| 25–32 | IV ACID CAN | Acid Chartreuse |

THE PACK (33–99) runs through the same four in blocks of eight, and **a patch you save keeps the scene it was saved
from**: save a Moonshine sound into 50 and slot 50 is Moonshine.

- **The dog** rests and sways while nothing plays. Play a note and he barks. In MOONSHINE, hold the note: he barks,
  draws breath, then howls.
- **The beam** is the live waveform of what you are playing, fired from his mouth to the top-right corner, in Acid
  Chartreuse in every chapter. It is the true signal: nothing on the screen (FLEAS included) ever touches it.
  Hold SEQ for Tape Stop and the beam dives with the sound.
- **The top bar is the fence.** It shows the voice mode and filter type, then `ARP`, `FX` (an effect is up) and
  `HOLD` when they are on, plus the chapter's name, and it carries short messages (`SAVED`, `STOPPED (PLAY)`, `MODE MONO`, the SLOP ride). Where the
  bark lands, the fence breaks, each chapter its own way: Jalopy scorches it, Bee-tch soaks it, Moonshine fogs it,
  Acid Can wrecks it. When the sound stops it heals within about a second.
- **The bottom bar** is the patch number and name. Nothing ever breaks it.
- **The dial.** Turn a knob on HOME (CUTOFF, RESO, ENV AMT, RELEASE, or SELECT for the LFO rate) and it pops up at
  the top left as the panel's own round knob: its name, how far it is turned, its value. It goes 1.2 seconds after
  your last turn. *(In BEE-TCH it covers the dog's tail while it shows.)*

**FLEAS — how mangy the screen gets.** GLOBAL knob 2, 0–100 (2 a click), a setting for the whole unit (not saved
with patches). It dirties HOME's scene only; the panel pages stay clean and readable, and **it never changes the
sound**.

| Dial | Stage | What happens on HOME |
|---|---|---|
| 0–15 | **CLEAN** | nothing |
| 16–65 | **ITCH** | the dog's outline boils, more as you turn it up |
| 66–90 | **SCRATCH** | + bands of the painting shear sideways |
| 91–100 | **MANGE** | + the fence's text scrambles, mustard blotches appear on the painting, the boil stutters |

Turn it down and the rot clears. The beam and the bottom bar are never touched. Every flicker is small and slow
(under 7 times a second, never the whole screen at once).

### 1.9 Saving: THE POUND and THE PACK

- **Slots 1–32 (THE POUND) are the factory patches and are locked.** You can tweak them as much as you like
  while playing; you just can't save over them. A firmware update brings their latest voicing.
- **To save:** tap SAVE. The header shows the slot it will save into and what is there now. On a POUND patch
  that is the **first free slot from 33**; on a PACK patch, the slot you are on. Turn **PRESETS** to choose another
  slot (it stays inside 33–99). Tap **SAVE** again to save: the header says `SAVED` and you are now on that slot.
  Do nothing for 3 seconds and SAVE lets go without saving.
- Saves keep their scene (1.8) and survive a power-cycle.
- **SAVE armed + press SELECT** = randomise: a new random sound instead of saving.
- *From v0.1 / v0.2:* a save made over 1–32 before the lock existed moves to the first free PACK slot at the first
  power-on. If THE PACK is full, it stays where it was, unread.

### 1.10 Installing, leaving and coming back

- **Install** from Chrome or Edge with the installer page (`vincentzsk-prod.github.io/dog5/install/`), over USB.
  It works from the stock firmware and from another custom firmware. **Keep the installer tab in front until it
  says Done:** in a background tab Chrome slows the page down, and the unit gives up waiting (it shows UPDATE
  FAILED). If an install is cut off, the unit stays in update mode and the page offers **Resume**.
- **Leave and come back:** another firmware (from the Firmware Hub, say) installs over DØG-5 the usual way, and
  DØG-5 installs back over it. Tested on the unit 20–21 Nov.
- **Your saves belong to DØG-5.** It reads only its own saved patches. Another firmware's saves don't show up here,
  and saving in DØG-5 can write over them. Other firmwares may treat DØG-5's saves the same way. **Back up first**
  (M-Flasher's BACKUP FULL FLASH) if anything on the unit matters to you.
- **Back to stock:** M-Flasher's DOWNLOAD MODE works from DØG-5, and RESTORE FULL FLASH with your stock backup puts
  the original firmware back. Tested on the unit 21 Nov.
- **The flash chip.** DØG-5 was built and tested on an FM-1 with the older Puya P25Q80 flash chip (`0x856014`).
  Newer units with the UC25HQ80 (`0xB36014`) are accepted by the update loader, but DØG-5 has never been installed
  or played on one. M-Flasher's Device Info shows which chip yours has.

---

## PART 2 — THE VOICING DICTIONARY

The words this manual uses for sound, and the controls that move each one. When a note says a patch is "seasick" or
"springy", this is what it means and where to reach. *(The measurements behind these words are kept in the voicing
records, not here.)*

### Body & weight
- **Fat / thick** — body and width. *More:* OSC 2's level up, a little DETUNE, UNISON or DUAL mode, both oscillators
  on. The DØG-5 way: start fat, then drive; a thin sound pushed loud never gets there. Once a sound is stacked, width
  (DETUNE) and per-voice DRIVE change its feel more than levels or filter do.
- **Thin / hollow** — narrow and reedy. *More:* one oscillator, a narrow pulse, a higher register, less detune.
- **Sub-heavy / deep** — weight in the low end. *More:* a low octave, OSC 2 down an octave, a low cutoff with the
  filter's DRIVE doing the work. At the very bottom (A0–A1) an octave-down oscillator is below hearing and only costs
  headroom.
- **Small speakers:** very low notes put most of their energy under about 60 Hz, which laptops, phones and many PAs
  don't play. "Thin" on a low patch is usually the 60–400 Hz band missing, not the sub.
- **Full vs empty** — how much of the spectrum is filled. Fuller: both oscillators plus noise; emptier: one, no noise.
- **Muddy** — a pile-up in the low mids with almost no top and a long tail: a smear, not a punch. *Cure:* square or
  pulse waves, an open 12 dB filter, less GROWL, a shorter decay. Some patches are muddy on purpose (13 Ghost Board).
- **Blank slate** — a plain voice with nothing added: 32 Init bruv?, and every empty PACK slot.

### Brightness & tone
- **Bright** — more top and presence. *More:* CUTOFF up, ENV AMT up, less SPRING DAMP, less BBD TONE roll-off.
- **Presence** — the patch sits forward and fills the room without just being louder or fuzzier. *More:* a wider stack
  (DETUNE), a touch more CUTOFF, per-voice DRIVE.
- **Dark / murky** — the top rolled off. *More:* CUTOFF down, more DAMP, more TONE roll-off on the delay.
- **Distant ("at the bottom of a well")** — the note's body vanishes and only the effects remain. *Cause:* the cutoff
  resting below the notes you play. *Cure:* raise CUTOFF and the filter envelope's SUSTAIN so the filter sits above them.
- **Warm** — a soft top that isn't dull, gentle saturation. *More:* a little per-voice DRIVE (MIXER page, knob 4), a
  low-pass, a modest cutoff. Not "a touch of GROWL": GROWL does almost nothing below about 28.
- **Harsh / piercing** — aggressive, tiring highs. *More:* RESO near the top, a high cutoff, hard sync, GROWL with high
  BIAS. Usually something to dial back.
- **Nasal / honky** — mid-forward and vowel-like. *More:* the band-pass filter, a narrow pulse, or TYPE SEM with MORPH
  toward notch.
- **Zap** — a burst of top end at the strike. *More:* narrow pulses, resonance, a fast filter envelope. A brighter
  cutoff overall makes the zap stand out *less*.
- **Soft / triangle-like** — there is no triangle or sine oscillator. The nearest: a narrow pulse (about 25%) through a
  key-tracking 12 dB low-pass, perhaps with an octave-up copy (16 Tidal Pull, 24 Fugue State). Dark by nature.
- **Chime** — a bright struck ping inside a narrow band, like a small horn speaker: a band-pass filter with high RESO
  and a second oscillator zinging down at the strike (29 i scream).

### Dirt & aggression
- **Clean** — no added grit: GROWL at 0 (a true bypass).
- **Driven / pushed** — warm to crunchy. *More:* per-voice **DRIVE** for the gentle route (adds harmonics without
  squashing the dynamics); **GROWL** for the big step (nothing up to about 28, compressing past 40, fuzzy by about 70);
  BIAS adds peaks and buzz. GROWL also darkens a sync rip a little.
- **Nasty / gnarly / blown** — full aggression: GROWL high, a resonant filter, a hard-chop gate. The Chapter I register.
- **Fuzzy** — a flat, relentless wall: GROWL high into a thick source, the cutoff open (06 zzuFuzz). The held note's
  length comes from the amp envelope, not from GROWL.
- **Pixelated / black-and-white** — a hard two-level wave, harsh and glitchy, not smeared: pulse or square only, an open
  12 dB filter, no GROWL, no tape (05 ZEAROX).
- **Spitting / biting** — nervous grit on the attack: slop, a snappy gate and drive biting a thick source.
- **Gritty / crunchy** — midway dirt: GROWL around 30–40, or heavy per-voice DRIVE. On an FM sound (X-MOD) the grit is
  often the FM itself: lower X-MOD before reaching for GROWL.
- **Dust** — noise as a faint trace under the tone. Keep NOISE low: full noise drowns a thin pulse even when it isn't
  louder, because it fills the gaps between the pulse's harmonics (23 Crypt Dust).

### Movement & instability
- **Tight / stable** — locked and in tune: VINTAGE low, no LFO on pitch.
- **Slop** — DØG-5's instability: each voice drifts on its own. Low = solid, middle = seasick, high = dying tape motor.
  The patch's VINTAGE is gentle on its own; the **SLOBBER ride** (ALGORITHM) multiplies it, live.
- **Seasick / woozy** — a slow pitch sway: VINTAGE up, a slow LFO on PITCH, tape wow (CHEW).
- **Warped / chewed** — tape wobble and dropouts: CHEW up (wow first, then flutter, then dropouts from about the middle of the knob). It costs more CPU than any other
  stage.
- **Melt** — the filter closing and the pitch sinking together while you hold the key: a slow filter envelope, ENV
  AMT below centre and ENV>O2 below centre (22 Melting Orb). On release it partly climbs back.
- **Wobble** — regular pitch or pulse-width movement: the LFO on PITCH or PWM. A pulse-width sweep that crosses the
  halfway point sounds twice as fast; keep it on one side.
- **Beating / shimmer** — two oscillators a few cents apart drift in and out of phase, so the sound swells and dips
  about once a second with no LFO at all. OSC 2's FINE sets the speed; centring it stops it.
- **Drifting / wander** — slow, unrepeating movement: VINTAGE, or the LFO's smooth random shape, slow, on PITCH or
  FILTER (18 Roto-scopo). There is no Poly-Mod: the one LFO moves every voice the same way.
- **Glitchy** — nervous, broken pitch and level: a fast random or sample-and-hold LFO on PITCH, and tape dropouts.
- **Chorus** — there is no chorus effect. The nearest: DUAL mode with SPREAD up and a slow triangle LFO on PITCH with
  PHASE SPREAD. A short delay can't do it (the BBD time has no LFO).
- **Leslie-style** — vibrato plus tremolo from the one LFO on PITCH and AMP. Only an approximation: a real rotor moves
  them out of step, and there is one LFO.

### Space & wetness
- **Dry** — no tail: the Psych Chain macros at 0.
- **Wet / drenched** — lots of tail: DRAIN up, the BBD page's MIX and FEEDBK up.
- **Wash** — a chord that blooms in and trails into its own echo and spring: a medium amp attack, a slow vibrato, a
  spread of detuned voices, an echo around 300 ms with plenty of feedback, a medium spring. Keep the echo above the
  spring so it reads (16 Tidal Pull).
- **Hover** — a chord that keeps hanging in the air after the key is up: echo FEEDBK near 100 with a short ALLEY, a
  large spring, a slow release (19 Micro-mist, 24 Fugue State). It decays; there is no freeze.
- **Slap** — one short, loud echo: ALLEY short, FEEDBK low, MIX up. The loudest slap sits about 6 dB under the note.
  The slap is a copy of the note, so shape the note, not the delay's TONE.
- **Springy / boingy** — the spring's chirp and flutter: DRAIN up, SIZE up. The Chapter II sound. Watch for "tubby" (too
  much low-mid in the tail); the spring is fed the filtered voice, so a dark patch gets a dark tail.
- **Roomy vs close** — how much and how long: SIZE and PRE-DLY against dry.

### Envelope, attack & dynamics
- **Snappy / punchy** — fast attack, quick decay. The punch often lives in the filter envelope opening and closing,
  not in the level; on a heavily driven sound it is the quick rise.
- **Plucky** — percussive: a short decay, low sustain, a filter envelope.
- **Gated** — no decay: the note starts at once, holds for the length of the key and stops dead (11 Slapback Strut).
  Taking a pluck's decay away can make it duller; raise the cutoff to compensate.
- **Soft / swelling** — a gentle fade-in: ATTACK up, SUSTAIN high.
- **Bloom** — a slow filter swell that opens while the key is held: dark at first, then wide and bright. Release early
  and it never opens (21 Cowl Shadow).
- **Sustained / drone** — holds as long as you want: high SUSTAIN, long RELEASE, and live, **REC (HOLD)** with the
  arpeggiator off: the notes ring until REC again, STOP or a MIDI panic.
- **Choppy / staccato** — hard on/off with dead silence between notes: a fast RELEASE, a square LFO on AMP. The house
  dynamic: the impact comes from the silence after.
- **Chop / strobe** — a hard on/off tremolo: a SQUARE LFO on AMP at full depth (15 Trem Chop). The rate is LFO RATE
  alone; it doesn't follow the tempo.
- **Sputter** — the tail breaks into ragged stutters as the note dies: a fast square LFO on AMP with LFO DELAY so it
  fades in after the attack (03 Half-Life). It follows how long the note has sounded, so it suits short notes.
- **Rip** — the hard-sync sweep tearing down across the note. In MONO and UNISON a legato note doesn't re-fire it:
  play detached.
- **Crash** — a noise strike that rings out like a cymbal over a sub: noise through a high-pass that sweeps down
  (14 Reef Break). The lows fall first and the top rings longest.

### Struck & ringing
- **Bell** — a struck tone with inharmonic partials that rings on after the key: two saws, one feeding the other by
  X-MOD, a long release (28 Arr 2 Dee 2). On 28, ENV>O2 off-centre breaks the bell.
- **Ring** — how long a struck note takes to die away.
- **Crystalline** — a tail whose top outlasts the body. This engine can't make it (there is no per-partial envelope).

### DØG-5 house words
- **Blown console** — the Chapter I aesthetic: fat sources shoved through drive until they tear.
- **The thesis** — the pure DØG-5 move: a thick source, slop and a hard-chop gate (03 Half-Life).
- **Sits under the vocal** — a patch voiced to live under a singer in the mix (01 Red Pill).

---

## PART 2B — TALKING IN NUMBERS

Synth-talk is often direct: "cutoff down 10%", "more feedback", "LFO a touch faster". These rules keep it exact.

**A percentage is percent of the control's full range,** not of where it is now. Most DØG-5 controls run 0–127, so:
- "down 10%" = about 13 steps;
- "set to 40%" = about 51;
- *a touch* ≈ 5% (about 6 steps) · *a bit* ≈ 10% · *a lot* ≈ 25–30%.

"More / less / up / down" means from where it is now; "set to / at" means a target.

**Controls with their own units:**

| Control | Unit | Say it like |
|---|---|---|
| BBD DELAY time (ALLEY) | milliseconds, 10–740 | "delay to 120 ms" |
| OSC 2 SEMI | semitones, −24…+24 | "OSC 2 up a fifth" (+7), "down an octave" (−12) |
| ENV AMT, FINE, ENV>O2 | centred at 64 | "+/−" from the centre |
| OCT, BEND | octaves / semitones | in their own units |
| WAVE, MODE, TYPE, SYNC, LFO SHAPE / PHASE | switches | by name ("pulse", "UNISON", "band-pass") |
| TEMPO | BPM | in BPM |
| FLEAS | 0–100, the screen only | by stage ("ITCH", "MANGE") |

Level knobs (OSC levels, VOLUME, NOISE) follow a square law: a small move is a bigger loudness change than it looks.

**Phrasebook: common synth-talk → the DØG-5 control**
- "open / close the filter" → CUTOFF (HOME knob 1, or the FILTER page)
- "more resonance / Q" → RESO
- "more or less attack · decay · sustain · release" → the AMP ENV or FILTER ENV page
- "more sweep" → ENV AMT
- "faster / slower wobble" → LFO RATE (the SELECT dial on HOME, or the LFO page; LFO DEST says what it moves)
- "more warmth / a bit more drive" → per-voice DRIVE (MIXER page, knob 4)
- "more dirt / grit / fuzz" → GROWL (DRIVE page; it starts around 30) · "more buzz / edge" → BIAS
- "more repeats" → FEEDBK (BBD DELAY page) · "longer / shorter delay" → ALLEY
- "wetter / more reverb" → DRAIN (SPRING page) · "bigger tail" → SIZE
- "more tape / wobble / lo-fi" → CHEW (TAPE page)
- "thicker / wider" → DETUNE (VOICE page) or OSC 2 FINE
- "more voices / fatter stack" → MODE + VOICES (UNISON), or the POLY count
- "how hard is it working?" → GLO once: the CPU reading at the top of GLOBAL (1.6)
- "dirtier / cleaner screen" → FLEAS (GLOBAL knob 2; 1.8)
