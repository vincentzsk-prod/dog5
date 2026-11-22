# DØG-5 — DRIVER MANUAL (Draft 1)

*Free, open-source custom firmware for the M-VAVE FM-1. Forked from OberVave. GPL-3.0.*

**Draft 1 — 3 Nov 2026.**
- **12 Nov, the Chapter IV checkpoint.** All four chapters are complete and all 32 patches are voiced. DØG-5 v0.1 was installed on Vincent's FM-1. The controls, keybed, CPU-meter and dictionary sections below carry what that showed. The dictionary gained Bell, Ring, Chime (band-limited) and Blank slate. Part 4 gear inspirations and Part 5 voicing notes now cover all 32.
- **18 Nov, v0.2** (`FM-1_962`, flashed and tested on the unit). Parts 1.1, 1.2 and 1.5 were rewritten for the Batch 9B controls (21 pages with MIXER, REC = HOLD, SELECT = LFO RATE on HOME, hold EDIT + a black key). Part 1.7 was added (plain-language knob hints), and the dictionary's DRIVE and MORPH pointers were corrected.
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
  *(12 Nov: held on the real unit — Vincent, after installing: all 32 voices sound distinct and on brand.)*
- **This is a LIVE instrument.** Everything is built to be played in the dark, mid-performance, without
  menu-diving. *(The second standing rule: new controls are designed against it, e.g. the keybed shortcut layer.)*

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

*The hold-HOME control map lists the three tricks (HEEL STOP, FLOP TAPE STOP, SLOBBER SLOP RIDE) and WAG HOLD
since v0.2. To fit the screen it leaves out the HOME row itself and the FX-held macros.*

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
  Instant dead air — for a band stop, or when the delay runs away. Press again to resume. (Tap-toggle.) It also
  lets go of HOLD.
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
- **Per voice:** two oscillators (saw / pulse / both), hard sync, cross-mod, noise, a 24 dB low-pass filter
  with drive, two ADSR envelopes, an LFO, and "Vintage Slop" (per-voice tuning/drift instability). There is
  no triangle oscillator; a narrow pulse through a key-tracking low-pass is the nearest. There is **one LFO
  per patch**: everything it is routed to moves at the same rate. It cannot be tempo-synced.
- **The Psych Chain** sits after the voices, reached by FX. It is the DØG-5 dirt: Drive, a free-time
  bucket-brigade delay, a spring reverb, and tape degrade. The tape stage is last, so it wobbles the finished
  wet mix: a delay repeat is pitched by the tape's state when it arrives, and everything wobbles together
  (a real tape echo warps each repeat separately; this cannot).
- **The bank:** 99 slots. **THE POUND (1–32)** are the factory patches, locked: you can play and change them,
  but a save never lands on them (see 1.9). **THE PACK (33–99)** are yours to save into; an unused one starts as
  the INIT sound (slot 32's engine defaults at VOLUME 100). *(Saving into the later slots was tested on the unit
  on 12 Nov, and with the lock on 20–21 Nov: it survives a power-cycle.)*

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
- **SAVE armed + press SELECT** = randomise: a new random sound instead of saving.
- Saves keep their scene (1.8) and survive a power-cycle.
- *From v0.1 / v0.2:* a save made over 1–32 before the lock existed moves to the first free PACK slot at the first
  power-on. If THE PACK is full, it stays where it was, unread.

### 1.10 Installing, leaving and coming back

- **Install** from Chrome or Edge with the installer page (`vincentzsk-prod.github.io/dog5/install/`), over USB.
  It works from the stock firmware and from another custom firmware. If an install is cut off, the page offers
  **Resume** (tested on a computer; not yet tried on the unit).
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

The shared language for describing and shaping tone. Each term gives the plain meaning and the controls that
move it, so a direction like "fatter and nastier, but less wet" has one agreed reading. This is the contract
for the voicing process and the vocabulary the patch descriptions are written in.

### Body & weight
- **Fat / thick** — more body and width. *More:* OSC 2 LEVEL up, slight DETUNE, UNISON or DUAL mode, sub/low
  register, both oscillators on. *The DØG-5 method: start fat, then drive — never a thin source pushed loud.*
  *(Measured on stacked-saw patches: once the oscillators are stacked, rebalancing levels or filter barely
  changes the spectrum; what changes the feel is **stack width (DETUNE), level and harmonic density
  (filter DRIVE).**)*
- **Thin / hollow** — narrow, reedy, little body. *More:* single oscillator, pulse with narrow PW, higher
  register, less detune. *(Diagnosis tip: very low notes put most of their energy under about 60 Hz, which
  small speakers and many PAs don't reproduce — "thin" on a low patch is often the 60–400 Hz band, not the
  sub.)*
- **Sub-heavy / deep** — weight in the low end. *More:* low octave, OSC 2 down an octave, low cutoff with the
  filter drive doing the work (bass-comp). *(At the very bottom, A0–A1, an octave-down oscillator is below
  audible range — it costs headroom without adding weight.)*
- **Full vs empty** — how much of the spectrum is filled. Fuller = both oscs + noise; emptier = one osc, no
  noise.
- **Muddy** *(added 5 Nov, from 05 ZEAROX round 1; extended 6 Nov)* — energy piled up in 150–400 Hz with
  almost nothing above 1.2 kHz, and a long tail: a smear, not a punch. *Cause found:* a saw wave through a
  24 dB low-pass at a low cutoff, plus GROWL's compression lengthening the tail. *Cure:* square/pulse
  oscillators, an open 12 dB filter, no GROWL, a short decay. Diagnose with the 150–400 Hz share against the
  1.2 kHz+ share ("MUD ratio") in time windows. *Scale (6 Nov, from Chapter II):* 10 A 2.5; 12 C 12.3 (tail
  10 / 15 / 77); a "medium muddy" target is about 10–40 on the note, tail windows no worse than about 80; 13
  (final) 315 with tails over 1000 — very muddy, chosen by ear; 16 D 133 (almost nothing above 1.2 kHz).
  *A soft, triangle-like tone is not "medium muddy" by this ratio on its own (245 with the second oscillator
  off in 13's round 1); the ratio is a diagnostic, and the owner's ear decides.*
- **Blank slate / init** *(added 12 Nov, from 32 Init bruv?)* — a plain starting voice with nothing added: no
  modulation, no echo, no spring, no tape, no drive. In this bank it is the engine's own default program (two
  saws 4.7 cents apart through a 24 dB low-pass at CUTOFF 80, RESO 20), not a single raw saw with an open filter
  (the saw's harmonics follow 1/n only with OSC 2 off, CUTOFF 127, RESO 0 and flat envelopes, which is a
  separate "raw saw" render kept for later).

### Brightness & tone
- **Bright** — more high end, more presence. *More:* CUTOFF up (HOME/FILTER), ENV AMT up, less SPRING DAMP,
  less BBD TONE roll-off, less TAPE head-loss.
- **Presence** *(added 4 Nov, from 30 THE DØG)* — the patch sits forward and fills the room without simply
  being louder or fuzzier. *More:* a wider stack (DETUNE), a touch more CUTOFF, per-voice filter DRIVE
  (warms without compressing), and — for a flagship only — sitting at the top of the loudness tolerance.
- **Dark / murky** — rolled-off top. *More:* CUTOFF down, more DAMP, more TONE roll-off on the delay.
- **Distant / "at the bottom of a well"** *(added 4 Nov, from 09 Skeenhead)* — the note's body vanishes and
  only the effects remain, so note and effect feel like two separate events. *Cause found:* the filter's
  cutoff resting **below the played notes** (a resonant plop closing under them), leaving a dark hum with no
  top, while the spring stays bright. *Cure:* raise the CUTOFF floor and the FILTER sustain so the filter
  rests above the notes; check the effect level relative to the dry note per time window (a single average
  hides it).
- **Warm** — soft top without going dull; gentle saturation. *More:* a little per-voice **filter DRIVE**
  (MIXER page, knob 4), LP filter, modest cutoff. *(Not "a touch of GROWL": GROWL does almost nothing below
  about 28.)*
- **Harsh / brittle / piercing** — aggressive, possibly fatiguing highs. *More:* high RESO near self-osc, high
  cutoff, hard sync, GROWL with high BIAS. Usually a thing to dial *back*.
- **Nasal / honky** — mid-forward, vowel-like. *More:* band-pass filter type, narrow PW, or TYPE SEM with
  MORPH toward notch.
- **Zap** *(added 5 Nov, from 08 Wire Bite)* — a burst of top end at the strike, like biting a live wire.
  *More:* narrow pulses, resonance, a fast filter envelope. *Limit:* a generally brighter cutoff **shrinks**
  the measured burst (the body is already bright), so "zappier" and "brighter" pull against each other.
- **Soft / triangle-like** *(added 6 Nov, from 11, 16 D and 13)* — there is no triangle or sine oscillator.
  The nearest is a narrow pulse (about 25%) through a key-tracking 12 dB low-pass: harmonics 3 / 5 / 7 read
  about −17 / −27 / −37 dB against an ideal triangle's −19 / −28 / −34. It is dark (centroid about 600 Hz,
  almost nothing above 1.2 kHz) and the ratio calls it muddy. An octave-up copy of the pulse brings the ratio
  down (13's round 1). It is a triangle-like stack, not a sine.
- **Chime (band-limited)** *(added 12 Nov, from 29 i scream)* — a bright struck ping inside a narrow band, like
  a small horn speaker. *How it is built:* a 12 dB band-pass at CUTOFF 77, RESO 105, KEY TRK 0 (peaks at 1099 Hz,
  −3 dB width 898–1345 Hz; 0.4% of its energy under 400 Hz and 4.1% above 4 kHz, measured with white noise),
  a pulse at 50% for OSC 1, and a second oscillator +15 semitones with X-MOD 25 and ENV>O2 76 for the zing at
  the strike. *Limit:* the +15 semitone partial is faint at the top of the keybed (−34 dB at C#6, −18 dB at C#5).

### Dirt & aggression
- **Dust (trace noise)** *(added 7 Nov, from 23 Crypt Dust)* — noise present only as a faint dust under the tone.
  *Measured:* the owner heard full-level noise (NOISE 127) as drowning a thin pulse even though the noise was only
  about 6 dB under the pulse by level, because it fills the spectrum between the pulse's harmonics; the final
  patch has the noise 24.4 dB under the pulse (NOISE 43; the NOISE knob is a square law: 43 against 127 is
  −18.8 dB). Removing the noise lowered the centroid by about 1.2 kHz and the 4 kHz+ share from 2.5% to 0.7%.
- **Clean** — no added grit. GROWL at 0 (a true bypass).
- **Driven / pushed** — console-into-the-red warmth to crunch. *More:* **filter DRIVE** for the gentle route
  (adds harmonics without squashing dynamics; it sits before the filter, so the filter takes some of the edge
  back); GROWL for the big step (inert up to about 28, compresses past about 40, fuzzy by about 70); BIAS
  (inside GROWL) adds peaks and even-harmonic buzz. *(12 Nov, from 26 BSyncA: GROWL also darkens a sync strike —
  the centroid over the first 50 ms is 2662 Hz with GROWL 44 against 4165 Hz with no drive — so the rip's
  brightness trades against the drive.)*
- **Nasty / gnarly / blown** — full aggression. *More:* GROWL high, resonant filter, hard-chop gate. The
  Chapter I register.
- **Fuzzy / voltage-starved** — gated, spitting fuzz like a dying battery. *More:* GROWL maxed into a thick
  source, cutoff open, fast gate. *(Measured on 06: held-note crest factor falls 5.8 dB at GROWL 0, 3.7 at 55,
  2.3 at 76, 1.5 at 100. Sustain comes from the amp envelope, not from GROWL. TONE is the audible one of
  GROWL's secondary controls; BIAS barely changes the peak.)*
- **Pixelated / black-and-white** *(added 5 Nov, from 05 ZEAROX)* — a hard two-level wave, like a photocopy
  reduced to pure black and white: harsh, glitchy, not smeared. *More:* pulse/square oscillators only, a
  12 dB filter held open, no GROWL, no tape. *Measured as* the share of samples within 10% of the rail:
  pulse waves 54% against 24% for saws; 05's final patch reads 94–98%.
- **Spitting / biting** — nervous, articulate attack grit. *More:* VINTAGE slop + a snappy gate + drive;
  comes from drive biting a thick source, not a thin one.
- **Gritty / crunchy** — midway dirt. GROWL in the 30–40 zone, or heavy filter DRIVE. *(12 Nov, from 28 round 2:
  on an FM bell the top grit was the FM itself — X-MOD 64 → 32 lowered the 2–10 kHz roughness, spectral flatness
  at A4 −16.9 → −25.4 dB — not CHEW, GROWL or drive. The share of energy above 4 kHz did not move: that is the
  saw's harmonics through an open filter at the strike, which suggests it moves with CUTOFF and the filter
  envelope.)*

### Movement & instability
- **Tight / stable** — locked, in tune, steady. *More:* VINTAGE/slop low, no LFO pitch, SYNC phase.
- **Slop** — the DØG-5 instability macro: per-voice tuning drift and wander. Low = solid, mid = seasick, high
  = dying tape motor. Rideable live on ALGORITHM. *(Measured: the patch's own VINTAGE is gentle — at 127 each
  voice wanders only about 6 cents. The dying-tape-motor territory comes mostly from the ALGORITHM ride,
  which multiplies the patch's own slop: about 5.6× at VINTAGE 55, 3.8× at 90 and 3.0× at 127.)*
- **Seasick / woozy** — slow pitch sway that unsettles. *More:* VINTAGE up, slow LFO→PITCH, slow TAPE wow.
- **Warped / chewed** — tape-style wobble and dropouts. *More:* CHEW up (wow/flutter/dropouts). Costs
  noticeably more CPU (about +770–784 host instr/sample at high CHEW; a Titanic variant with CHEW measured
  2371 vs 1594). *(Measured on 05 round 1: CHEW at maximum barely changed level, crest or click — it mostly
  smeared the top end. Measured on 13 round 1: the deck's wobble is about 2.3 / 4.1 / 6.2 / 6.5 cents s.d. at
  CHEW 40 / 70 / 100 / 127, slow wow only (0.3–0.5 Hz), and it added hiss that lifts the centroid. The owner
  heard the wobble as "killing the overall tone" and dropped it, so CHEW 0 on 13. On 29 the owner also took the
  tape off after hearing it: CHEW 65 cost 2647 host instr/sample against 1863 with CHEW 0.)*
- **Melt** *(added 7 Nov, from 22 Melting Orb)* — the filter closing and the pitch sinking together over a few
  seconds while the key is held. *How:* a rising filter envelope (FA 118, 4.96 s nominal) with a negative ENV
  AMT, plus ENV>O2 below centre (it bends OSC 2 only, from the filter envelope: (value − 64) × 24/63 semitones at
  the top; value 46 = −6.86 st). *Measured:* −678 cents final, 90% of the fall at 4.0 s, centroid 1323 → 204 Hz.
  *Limit:* on key-up the filter envelope releases and the melt partly runs backwards through the fade.
- **Wobble** — regular pitch or PWM movement. *More:* LFO→PITCH or LFO→PWM, moderate rate. *(PWM: the pulse
  width sweep runs at the LFO rate. A sweep that crosses 50% sounds like it doubles its rate, because a pulse
  and its mirror width sound alike; keep the sweep on one side of 50%, or only just across it. Through a
  murky low-pass the PWM movement is a ceiling of about 10 dB in the 150–400 Hz band whatever the depth or
  cutoff (12 Kelp Tangle); a faster, wider sweep or more per-voice DRIVE trades level swing for band depth.)*
- **Beating / shimmer** *(added 6 Nov, from 10 and 13)* — two oscillators a few cents apart drift in and out
  of phase, so the low-mid band swells and dips about once a second without any LFO. *Measured:* 10 A (a pulse
  pair with one 85% pulse nearly the inverse of the 16% one, +9.4 cents) swings its A3 band 17.9 dB at 1.01 Hz;
  13 (pair +7.0 cents) moves the 150–400 Hz band 13.6–13.8 dB at 0.9 Hz on one voice (6.2 dB on the held
  chord). Removing the detune (OSC 2 FINE 64) takes it to 0.3 dB; removing the PWM LFO leaves it. Slow PWM
  sweeps are a different movement, mostly in the 400–1.2k band (3.9 dB on 13's original).
- **Drifting** — slow, unrepeating wander (not a steady LFO). *More:* VINTAGE slop, a slow smooth-random
  LFO→PITCH (08 Wire Bite: ±19 cents at 0.28 Hz). *(There is no Poly-Mod control: X-MOD is OSC 2 → OSC 1 FM;
  checked again 6 Nov for 18.)* **Wander** *(added 7 Nov, from 18 Roto-scopo)* — the Poly-Mod substitute: the one
  shared smooth-random LFO (0.11 Hz) on the FILTER (±23.9 st) over a resonant low-pass, plus VINTAGE slop 127.
  Measured on A1: the centroid ranges 316–708 Hz (14 st); the level moves only about 1 dB. The wander is common to
  all voices and cannot follow OSC 2.
- **Glitchy** *(added 5 Nov, from 07 Tape Splice)* — nervous, broken, unreliable pitch and level. *More:* a
  fast random or sample-and-hold LFO to PITCH (5–21 Hz, ±19 cents up to several semitones), tape dropouts
  (CHEW high with DROPS up). *(Measured: the random pitch LFO carries the pitch jitter; tape carries the
  dips; X-MOD adds sidebands and low-end energy but does not move the measured pitch.)*
- **Chorus (clear, wide)** *(added 6 Nov, from 10 round 1)* — the engine has no chorus effect. A chorus is
  built from a DUAL pair (SPREAD 127) with a slow TRI pitch LFO in PHASE SPREAD, so the two voices of each
  note sit 45° apart in the LFO and their pitch difference swings. *Measured on 10 B:* ±19 cents at 0.72 Hz,
  L/R correlation 0.48 (0.78 without), band beating 29 dB. It costs about +490 host instr/sample over POLY
  (10 B 2294). A short BBD delay cannot be a chorus, because its time has no LFO.
- **Leslie-style (rotary)** *(added 6 Nov)* — vibrato plus tremolo from the one LFO routed to PITCH and AMP in
  PHASE FREE. Only an in-phase approximation: a real rotor's pitch and level are 90° apart and the engine has
  one LFO. With SPREAD the tremolo cancels in the sum (2.2 dB at AMP 45 with SPREAD, 2.9 FREE, 3.9 SYNC on a
  held chord).

### Space & wetness
- **Dry** — no effects tail. The chain mixes/macros at 0.
- **Wet / washed / drenched** — lots of tail. *More:* SPRING DRAIN up, BBD MIX + FEEDBK up.
- **Wash (washy, not punchy)** *(added 6 Nov, from 16 Tidal Pull)* — a chord that blooms in, trails into its
  own echo and spring and moves. *More:* a medium amp attack (AA 82 reads 17 / 93 / 219 ms to 10 / 50 / 90%;
  the envelope's nominal time is 1.3–1.4× its time to 90%), a slow TRI pitch LFO (±19 cents), a spread of
  detuned voices, echo at about 337 ms with FEEDBK 78 and MIX 110, DRAIN 45 SIZE 90. Keep the echo audibly
  above the spring (16 D: first repeat −8.6 dB re the note, 7.7 dB above the spring).
- **Hover** *(added 7 Nov, from 19 Micro-mist and 24 Fugue State)* — a chord that keeps hanging in the air on its
  own echo and spring after the key is up. *More:* echo FEEDBK near 100 or above with ALLEY 100–144 ms, a large
  spring (SIZE 100–110), a slow release. *Measured:* 19 D falls 20 / 40 / 60 dB in 1596 / 4132 / 5788 ms after a
  10 s chord; 24 C in 1648 / 3520 / 4624 ms. *Limits:* it is a decaying hover, not a freeze (no freeze, reverse or
  pitch-shifted repeats exist); FEEDBK 122 on 24 would peak at −2.1 dBFS, 127 clips.
- **Slap / slapback** — one short, loud echo. *More:* ALLEY short (free ms), FEEDBK low, MIX up. *(Measured
  on a bass: the echo is a faithful copy of the note, so ALLEY TONE does nothing audible there — the
  crispness has to live in the note. The loudest slap the engine can make is MIX 127, about 6 dB under the
  note's peak.)*
- **Springy / boingy** — the spring-reverb chirp and flutter. *More:* DRAIN up, SIZE up; the Chapter II sound.
  (Watch "tubby" — too much low-mid in the tail.) *(Measured: DRAIN is audible on bass, not absent — the
  tank's high-pass is one-pole, −9 dB at 55 Hz. At DRAIN 60 the return is about −5 dB re dry on Titanic and
  −9.7 dB on a bass with most energy below 150 Hz. The spring sits after the echo and rings the repeats; it
  is fed the filtered voice, so a murky patch gets a murky tail.)*
- **Roomy vs close** — amount and length of ambience (SIZE/PRE-DLY vs dry). *(PRE-DLY 4 is only about
  1 ms.)*
- **Wet return, measured per window** — for a patch with a slight wetness (01 Red Pill) the effect level is
  read relative to the dry note in 0–20 / 20–100 / 100–250 ms windows, never as an average.

### Envelope, attack & dynamics
- **Snappy / punchy** — fast attack, quick decay, immediate. *More:* AMP/FILTER ATTACK low, DECAY short.
  *(Where the punch lives: often in the filter envelope opening and closing — the brightness falling from
  attack to body — rather than in the amp level. A fast amp pluck can't reach the bank level on its own. A
  heavily clipped sound (06, 05) has almost no level spike at the strike; its punch is the quick rise.)*
- **Plucky** — percussive, fast decay, little sustain. *More:* short DECAY, low SUSTAIN, filter env.
- **Gated (as opposed to plucky)** *(added 4 Nov, from 11 Slapback Strut)* — zero decay: the note starts at
  once, holds its body for the length of the key, and stops in about a millisecond. *Note:* removing a
  pluck's decay can make the note **duller**, because the pluck's initial tap carried the top end; to end up
  bright, raise the cutoff and narrow the pulse.
- **Soft / slow / swelling** — gentle fade-in. *More:* ATTACK up, SUSTAIN high.
- **Bloom** *(added 4 Nov, from 21 Cowl Shadow)* — a slow filter-envelope swell that opens while the key is
  held: dark and soft at first, then wide and bright. It needs the key (or a sustain pedal) held for its full
  length; released early it never opens, it just fades. Short stabs on a bloom patch are far quieter than
  the bloomed state.
- **Sustained / drone** — holds indefinitely. *More:* high SUSTAIN, long RELEASE. Live: press **REC (HOLD)**
  with the arpeggiator off and the held notes keep ringing until you press REC again, STOP, or send a MIDI panic
  (see 1.1).
- **Choppy / gated / staccato** — hard on/off, dead silence between notes. *More:* fast RELEASE (hard-chop
  VCA), LFO→VCA square tremolo. The house dynamic — the impact of the noise comes from the silence after it.
- **Chop / strobe** *(added 5 Nov, from 15 Trem Chop)* — a hard on/off tremolo from a SQUARE LFO routed to
  AMP at full depth: about 43–45 dB between the on and off parts at AMP 127 (17 dB at 110, 13.5 at 100, 9 at
  80). Rate is the RATE knob alone: 0.05 × 600^(RATE/127) Hz, steps of about 5%. *Limits:* no tempo sync; PHASE
  SYNC restarts the chop on each detached note (so every note starts ON), FREE phase is unpredictable live;
  VINTAGE does not make the chop edges waver — only PHASE SPREAD on a DUAL pair does (the two voices chop an
  eighth of a cycle apart).
- **Sputter** *(added 4 Nov, from Half-Life)* — the tail doesn't fade, it breaks into a few ragged stutters as
  the note dies. Distinct from tremolo: the body is clean and only the tail chops. *More:* LFO SHAPE SQUARE
  around 20 Hz routed to AMP at full depth, with LFO DELAY around 110 ms so the chop fades in after the attack.
  *Limit:* the chop follows how long the note has been sounding, not the key coming up, so it works on short
  notes (roughly 150–180 ms); a longer held note spits all the way through.
- **Rip** *(added 4 Nov, from V-Sync)* — the hard-sync sweep: the synced oscillator's pitch tears down across
  the note. *Limit:* in MONO and UNISON, a note struck while another is held slides in and does **not**
  re-fire the envelopes, so the rip fires on detached notes only.
- **Crash / burst** *(added 6 Nov, from 14 Reef Break)* — a noise strike that rings out like a cymbal over a
  square sub. *Recipe that worked:* NOISE 127 over a square sub (noise 3–6 dB above it in the first 100 ms), a
  12 dB HIGH-pass at CUTOFF 100 with ENV AMT 0 (the cutoff starts about 97 semitones low at the strike, under
  the sub, and climbs back as the filter envelope falls, FD 100), AD = AR = 97 for the ring-out. The bands then
  fall lowest first and the top rings longest, as a cymbal does; a closing low-pass does the reverse. Attack
  options measured at 10 / 50 / 90%: 0 / 0.2 / 8.5 ms (near-instant), 2.2 / 8.7 / 27.2 ms (a quick swell, peak
  at 27 ms; chosen in round 1), 1.2 / 7.2 / 8.7 ms. *v0.2 (18 Nov, by ear: the strike was too harsh coming in):*
  14 now uses a 299 ms attack on both envelopes (FILTER ENV and AMP ENV ATTACK 82), so the crash swells in; every
  band peaks about 235–276 ms in, the bands still fall lowest first and the top still rings longest. *Limits:* no
  inharmonic cymbal partials (noise only); noise and sub share one filter and one amp envelope, so the sub leaves
  early only through the high-pass; a chord of three noise voices stacks and peaks near the rail.

### Struck & ringing *(added 12 Nov, from 28 Arr 2 Dee 2 and 29 i scream)*
- **Bell (struck)** — a sustained, struck tone with inharmonic partials that ring on after the key is up. *How it
  is built (28):* two saws, OSC 2 +15 semitones (a ratio of 2.38) feeding OSC 1 by X-MOD 32, a long amp release
  (AR 116), a slow shimmer. *Measured:* the five classical bell partials are present at fixed ratios (hum 0.5,
  prime 1, tierce 1.2, quint 1.5, nominal 2); the key you press is the hum and the prime sits an octave above it.
  *Limits:* **ENV>O2 ±10 breaks the bell** (the tierce falls from −10 dB to about −47 dB); one saw modulating
  another is not a DX7-style operator stack.
- **Ring** — how long a struck note takes to die, read as the milliseconds to fall 6 / 12 / 20 / 30 / 40 dB
  after the peak. *Measured:* 28 at A4 915 / 1962 / 3094 / 4700 / 5963 ms; a note released at 400 ms rings on and
  falls 20 dB in 3012 ms. Not "dreamy" or "healthy" — those are the owner's words.
- **Crystalline (not carried)** — a tail whose upper partials outlast the body. The engine has no per-partial
  envelope, so it cannot be built here; the share of energy above 4 kHz at A4 falls from 4.0% in the first 20 ms to
  0.4% at 1–2 s.

### DØG-5 house words
- **Blown console** — the overall Chapter I aesthetic: fat sources shoved through drive until they tear.
- **The thesis** — the pure DØG-5 move: a thick source + slop + hard-chop gate (see Half-Life).
- **The Monologue** — the reference point for a patch that "sits under" a spoken/sung vocal in the mix.

---

## PART 2B — TALKING IN NUMBERS (direct parameter moves)

Alongside the character words above, voicing uses plain synth-talk — direct moves on named controls ("cutoff
down 10%", "more delay feedback", "LFO rate up a touch"). These rules keep that unambiguous.

**The percent convention.** A percentage means percent of the control's **full range** — not of its current
value, and not of the number on screen. Most DØG-5 parameters run **0–127**, so:
- "−10%" / "down 10%" = subtract ~13 (10% of 127).
- "set to 40%" = ~51.
- rough sizes: *a touch* ≈ 5% (~6 steps) · *a bit* ≈ 10% · *a lot* ≈ 25–30%.

**Relative vs absolute** are both fine — "more feedback" / "+10%" (from where it is) or "set cutoff to 40%" /
"cutoff at 51" (a target). Say which when it matters; if unsaid, "more/less/up/down" is relative and "set
to / at" is absolute.

**The echo rule.** Every change the session makes is reported in concrete before→after: *"CUTOFF 80 → 67
(−10%)."* So a misread shows up in the notes, not just the sound — you catch it in the echo and correct it
there, which is faster than another render.

**Controls that aren't a plain 0–127 percent** — talk in their own units when that's easier:

| Control | Native unit | How to say it |
|---|---|---|
| BBD DELAY time (ALLEY) | free ms, 10–740 | "delay to 120 ms", or % of range |
| OSC 2 SEMI | semitones, −24…+24 | "OSC 2 up a fifth" (+7), "down an octave" (−12) |
| ENV AMT, FINE, ENV>O2 | bipolar, centre 64 | "+/−" from centre |
| OCT, BEND | octaves / semitones | in their own units |
| WAVE, MODE, FILTER TYPE, SYNC, LFO SHAPE/PHASE | named settings (switches) | by name ("pulse", "UNISON", "band-pass") |
| TEMPO | BPM | in BPM |
| FLEAS | 0–100 (a screen setting, never the sound) | by stage ("ITCH", "MANGE") or number |

Everything else is the straight 0–127 percent. *(Level knobs such as OSC LEVEL and VOLUME follow a square
law, so a small number change is a larger loudness change than it looks.)*

**Phrasebook — common synth-talk → the DØG-5 control it moves** (so a generic instruction lands on the right
page/knob):
- "open / close the filter" → CUTOFF (HOME K1, or the FILTER page)
- "more resonance / more Q" → RESO
- "more / less attack · decay · sustain · release" → the AMP ENV or FILTER ENV page (say which)
- "more filter envelope / more sweep" → ENV AMT
- "speed up / slow the wobble" → LFO RATE (the SELECT dial on HOME, or the LFO page; and check LFO DEST is on
  PITCH / PWM / FILTER)
- "more warmth / a bit more drive" → per-voice DRIVE (MIXER page, knob 4); "more dirt / grit / fuzz" →
  GROWL (DRIVE page, meaningful from about 30); "more buzz / edge" → BIAS
- "more delay feedback / more repeats" → FEEDBK (BBD page); "longer / shorter delay" → ALLEY
- "wetter / more reverb" → DRAIN (SPRING page); "bigger tail" → SIZE
- "more tape / more wobble / more lo-fi" → CHEW (TAPE page)
- "detune / thicken / wider" → DETUNE (VOICE page) or OSC 2 FINE
- "more voices / fatter stack" → MODE + VOICES (UNISON), or the POLY count
- "how hard is it working / am I near the limit" → GLO once, the CPU reading at the top of GLOBAL (see 1.6)
- "dirtier screen / cleaner screen" → FLEAS (GLOBAL knob 2; see 1.8)
