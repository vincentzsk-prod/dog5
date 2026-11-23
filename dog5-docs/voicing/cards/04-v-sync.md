# 04 · V-Sync · Chapter I · JALOPY

*Voiced 4–5 Nov 2026, approved as is (variant D, the fat two-voice lead). Renders: `reference-renders/04-v-sync_D_*.wav` (D is this patch); the rejected variants are in the git history before `e40f5d5`. Log: `../04-v-sync.md`.*

## 2. What it sounds like

A tearing hard-sync lead: the pitch of the synced oscillator rips down on every note, nasal and biting, with a plain saw underneath for body. Two voices a few cents apart make it fat enough to cut through a drum machine. The note stops dead when you let go, with only a faint, quick slap behind it. Raw on purpose: that is where the rip lives.

## 3. Gear inspirations (docs only, "inspired by")

- **Sequential Pro-One** — the sync sweep itself: *sync, punchy, ripping*.
- **Sequential Prophet-5** — the fatness of a doubled voice: *sync, fat*.
- **ARP Odyssey** — the nasal, cutting tone: *nasal, biting*.
- **Moog Prodigy** — the cheap, raw edge: *fat, cheap, raw*.

Closest to: **a Pro-One sync lead**.

## 4. Sound design notes

- **Where it lives:** mid register, around A3 to A4. One note at a time: no chords.
- **Play it staccato.** A note struck while another is held slides in without the rip; a legato run glides and rips only once, on its first note. Detached notes rip every time.
- **The slap:** a faint 1/16 echo follows each note. The BBD page's MIX at 0 gives a literal dead stop.
- **Tricks:** SLOBBER pulls the two voices apart; GROWL adds edge (it does little below about 28); HEEL kills the slap too. Keep DRAIN low: a spring blurs the rip.

## 5. Final values (for debugging, not for players)

`MODE UNISON, VOICES 2, DETUNE 22 (~5.5 cents between the pair), GLIDE 20, OSC1 SAW LVL 80, OSC2 SAW +7st LVL 127 SYNC ON, ENV>O2 112 (+48, ~18 st sweep), CUTOFF 92, RESO 24, ENV AMT 88, FILTER LP24 DRIVE 20, FILTER ENV A20 D78 S28 R30, AMP ENV A0 D70 S127 R30, DLY 1/16 FEEDBK 18 MIX 12, VOLUME 91 (-18.0 dBFS RMS bank reference on the lead phrase); GROWL/DRAIN/CHEW 0, no LFO, no arp` — `PF_V_SYNC` in `firmware/src/obv_patches.h`.

## 6. The voicing record (measured notes, not for players)

*Sections 2–4 as they stood before the Batch 30 rewrite (23 Nov 2026): the measurements, the variants and what was and wasn't tested. The player text above is drawn from this.*

### 2. What it sounds like

A tearing hard-sync lead: the pitch of the synced oscillator rips down on every note, nasal and biting, with a plain saw underneath for body. A pair of voices
detuned slightly apart makes it fat enough to cut through a drum machine, and the note stops dead when you let go, with only a faint quick slap behind it. It is
raw on purpose: that is where the rip lives.

### 3. Gear inspirations (docs only, "inspired by")

- **Sequential Pro-One** — the sync sweep itself: *sync, punchy, ripping*.
- **Sequential Prophet-5** — the fatness of a doubled voice: *sync, fat*.
- **ARP Odyssey** — the nasal, cutting tone: *nasal, biting*.
- **Moog Prodigy** — the cheap, raw edge: *fat, cheap, raw*.

Closest to: **a Pro-One sync lead**.

### 4. Sound design notes

- **Register:** mid, roughly A3 to A4 and around it, where the lead was auditioned. It is a one-note-at-a-time lead: no chords.
- **Touch and gate: play it staccato.** The rip comes from the filter envelope sweeping the synced oscillator, and in MONO and UNISON a note struck while another is
  still held **slides in and does not re-fire the envelopes**. So the sweep fires on **detached notes only**; a legato run glides (a short slide is set) but rips just once, on its first note.
- **The stop:** the voice itself stops dead on release. The echo is not gated, so a **faint slap follows each note**; it is quiet and short (a 1/16 slap), and turning
  the echo's MIX down to 0 gives a literal dead stop.
- **Tricks that suit it:**
  - **ALGORITHM slop ride (SLOBBER):** pulls the two voices apart; untested on this patch.
  - **Kill switch (HEEL)** for an instant stop, including the slap. Untested on this patch.
  - **Tape Stop (SEQ held)** on a held note as a dive. Untested on this patch.
  - **GROWL (adding it live):** more edge on top of the filter DRIVE the patch already has; untested here, and GROWL below about 28 does little.
  - **DRAIN:** at 0 on purpose (no spring); a wash will blur the rip.
- **Level:** it is set to the bank's level on its lead phrase. Its own volume is a little *below* the default (about 1.6 dB), because the two-voice stack is louder than the one-voice version (which needed about 3 dB more).
