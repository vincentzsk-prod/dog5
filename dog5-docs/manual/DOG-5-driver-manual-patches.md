# DØG-5 — DRIVER MANUAL, PARTS 3–4 (the 32 patches)

*Continues `DOG-5-driver-manual.md` (Parts 0–2B). **Generated from the 32 voice cards** (`dog5-docs/voicing/cards/`)
by `tools/make_manual_patches.py` since Batch 30 (23 Nov 2026): edit a card, then run the script; don't edit this file
by hand. The measured voicing notes that used to be here are in each card's section 6 and in the repo's
`dog5-docs/manual/DOG-5-driver-manual-records.md`.*

## PART 3 — THE 32 PATCHES

Four chapters of eight, one per scene on HOME. Slots 1–32 are **THE POUND**: play them and tweak them as much as you
like; a save goes to **THE PACK** (33–99, see 1.9), so the factory sounds are always there to come back to.

Each patch has three parts: **what it sounds like**, **sound design notes** (where it lives on the keybed, how to play
it, what to reach for) and **the gear that inspired it**. The live tricks (SLOBBER, Tape Stop, HEEL) and the four Psych
Chain macros work on every patch; a note mentions them only where they suit or fight that patch. Every patch was voiced
by ear and the bank is level-matched, so switching patches doesn't jump, except where a note says so.

### CHAPTER I — JALOPY

*Egg punk and garage psych. Fat sources through a blown console: basses, a sync lead, a kick and the fuzz. On screen: the Jalopy scene, accent Sun Yellow.*

#### 01 · Red Pill

A nervous, spitting bass made to sit under a vocal. Two fat saws, stacked and held steady, push through a resonant filter that snaps at the start of every note, driven hard enough to be gritty and warm without getting piercing. It is nearly dry: a quick slap and a small spring sit behind each note, lifting it a little and never coming near the note's own loudness.

**Sound design notes**

- **Where it lives:** low, A1 to A2, in short detached notes and sixteenth bursts. That is where the filter snap spits.
- **Play it detached.** It is MONO: a legato note slides in without the snap, and a chord plays only its last key.
- **On small speakers** half its weight sits under 60 Hz, so a laptop gives you the grit, not the floor.
- **To push it:** CUTOFF and RESO on HOME sharpen the spit. GROWL adds more of the grit it already has.
- **Dry it out:** the slap and spring sit well under the note. DRAIN and the BBD page's MIX at 0 make it bone dry.
- It is slot 1: the patch you hear at power-on.

**Gear inspirations**

- **Korg MS-20** — the resonant filter and its bite: *nasty, biting, resonant*.
- **Minimoog** — the stacked saws: *fat, thick*.
- **Roland SH-101** — the tight snap at the front of a note: *tight, punchy*.
- **ProCo RAT** — the driven edge: *gritty, crunchy*.

Closest to: **an MS-20 bass through a RAT**.

#### 02 · Cement Grind

A low-mid grinder: two fat pulse waves whose widths sweep fast, so every note shudders and churns. A clear, quick pulse-width wobble, not a shimmer. The filter bites, it is pushed into a moderate crunch, and each note starts with a little skid and a snap. Thick, dry, and it hits hard.

**Sound design notes**

- **Where it lives:** A2 up to E3, in notes of about 400 ms: long enough for the wobble to swing two or three times inside each note.
- **Play it detached.** It is MONO: a legato note glides in (the skid) without a new snap, and a chord plays one note.
- **One LFO does both jobs:** the pulse-width sweep and a filter wobble share it, so LFO RATE speeds or slows both together. Each detached note restarts the sweep.
- **Don't push the PWM depth much further:** the sweep already just crosses the halfway width at the top of each swing, and past that a pulse sweep starts to sound twice as fast.
- It stops the moment you let go.

**Gear inspirations**

- **Roland Juno-60** — the pulse-width movement: *PWM, wobble, thick*.
- **Korg Polysix** — the stacked pulses: *fat, PWM*.
- **Roland SH-101** — the punchy PWM bass: *punchy*.
- **ProCo RAT** — the crunch: *crunchy*.
- **Korg MS-20** — the filter: *biting*.

Closest to: **a Juno-60 PWM bass through a RAT**.

#### 03 · Half-Life

Fat, slop-heavy dual saws with a sub-octave underneath: seasick, never quite in tune with itself, and thick without going murky. Short notes are chopped stone-dead by the gate, and the tail doesn't fade, it sputters: a few ragged stutters as the note dies. Raw, dry, engine-only: the drift and the chop are the whole point. The DØG-5 thesis in one patch.

**Sound design notes**

- **Where it lives:** low to low-mid, roots and fifths from about A1 to A3. Fifth-and-octave power chords are home ground.
- **Play it staccato:** notes of roughly 150 to 180 ms give a hard clean body and a sputtering tail. Hold a note longer and it spits all the way through; very short notes only catch the start. Riffs and stabs, not pads.
- **Chords: three notes at most.** Every note is two voices, so a fourth note steals from the others.
- **SLOBBER is its best trick:** ride ALGORITHM up and it goes from seasick to dying tape motor. Tape Stop (hold SEQ) makes a good riff ending; HEEL stops the sound and the sputter dead.
- **Keep the Psych Chain off:** a wash of ALLEY or DRAIN buries the sputter.

**Gear inspirations**

- **Korg Mono/Poly** — detuned oscillators that drift and never settle: *fat, slop, seasick, thick*.
- **Sequential Prophet-5 (early, tuning-unstable revisions)** — the dual-saw warmth with the drift: *fat, warm, drift*.
- **Minimoog** — the body under the instability: *fat, sub-heavy, thick*.
- **Korg MS-20** — the bite and the spit in the filter and the tail: *nasty, biting, spitting*.

Closest to: **a Korg Mono/Poly: drifting, detuned saw chaos with Minimoog weight underneath, chopped by the gate**.

#### 04 · V-Sync

A tearing hard-sync lead: the pitch of the synced oscillator rips down on every note, nasal and biting, with a plain saw underneath for body. Two voices a few cents apart make it fat enough to cut through a drum machine. The note stops dead when you let go, with only a faint, quick slap behind it. Raw on purpose: that is where the rip lives.

**Sound design notes**

- **Where it lives:** mid register, around A3 to A4. One note at a time: no chords.
- **Play it staccato.** A note struck while another is held slides in without the rip; a legato run glides and rips only once, on its first note. Detached notes rip every time.
- **The slap:** a faint 1/16 echo follows each note. The BBD page's MIX at 0 gives a literal dead stop.
- **Tricks:** SLOBBER pulls the two voices apart; GROWL adds edge (it does little below about 28); HEEL kills the slap too. Keep DRAIN low: a spring blurs the rip.

**Gear inspirations**

- **Sequential Pro-One** — the sync sweep itself: *sync, punchy, ripping*.
- **Sequential Prophet-5** — the fatness of a doubled voice: *sync, fat*.
- **ARP Odyssey** — the nasal, cutting tone: *nasal, biting*.
- **Moog Prodigy** — the cheap, raw edge: *fat, cheap, raw*.

Closest to: **a Pro-One sync lead**.

#### 05 · ZEAROX

A kick substitute made of one hard square wave: pixelated, gritty and blown out, like a photocopy reduced to pure black and white. The pitch drops fast at the strike, and a random stepped pitch moves each hit to new values, so no two hits sound quite alike. No attack, and it stops quickly when you let go. Dry: no tape, no drive, no echo, no spring.

**Sound design notes**

- **Where it lives:** low hits on A1 and A2, or four on the floor. A0 is mostly below what a small speaker can play.
- **Play it detached.** It is MONO: a legato note slides without a new hit, and a chord plays one note.
- **The kick is the quick pitch drop,** not a click. The random steps are the glitch: LFO PITCH on the LFO DEST page sets how wild they get, and 0 makes every hit the same.
- **It is already near the top of its VOLUME,** so there is little room above the bank level: turn the master up, not the patch.

**Gear inspirations**

- **Roland TR-808 kick** — *sub, thump*.
- **Roland SH-101** — *sub, thick*.
- **Tascam Portastudio cassette 4-track** — *lo-fi, noisy*.
- **ProCo RAT** — *crunchy, driven*.

Closest to: **an 808 kick smashed onto a blown-out cassette 4-track (the tape and the drive are the inspiration, not in the patch)**.

#### 06 · zzuFuzz

The fuzz weapon: a huge, thick wall. Two fat saws on every voice are pushed hard into the drive until the sound is flat and relentless, and it does not die while you hold the key. The strike is quick, the filter and its resonance are wide open, and when you let go there is a short tail, not a ring. Completely dry. A power chord stays whole.

**Sound design notes**

- **Where it lives:** a low A1 up to power chords around A2–E3–A3, held or stabbed. Three-note chords play whole.
- **It is a wall, not a punch:** the fuzz flattens the dynamics, so the hit is in the quick rise. More punch means less GROWL.
- **It reads a little hot** next to the rest of the bank: about 2 dB on stabs.
- **Set VOLUME before you judge the strike:** GROWL's loudness trim follows it, so VOLUME changes how a note starts from silence.
- **RESO has room** up to about 120; past that the filter starts to sing by itself.
- It is not a voltage-starved, gating fuzz: it never sputters.

**Gear inspirations**

- **Death by Audio Fuzz War** — the benchmark, a huge fuzz beast: *fuzzy, thick wall*.
- **Electro-Harmonix Big Muff** — the wall: *fuzzy, thick wall*.
- **Fuzz Face** — the fuzz: *fuzzy, spitting*.
- **Univox Super-Fuzz** — *spitting*.
- **Korg Mono/Poly** — as the source: *fat, drifting*.
- **Realistic Concertmate MG-1** — *lo-fi*.

Closest to: **a Mono/Poly into a Big Muff**.

#### 07 · Tape Splice

A fat square with a wobble in its pitch, chopped short. Two square waves a hair apart, one frequency-modulating the other, so the tone carries extra weight below the note, and a random pitch wobble on top. Notes stop quickly when you let go, and a tape stage on the end nudges each note's timing slightly. Dry: no echo, no spring.

**Sound design notes**

- **Where it lives:** staccato lines from A2 up to G3, and held notes.
- **Play it detached.** It is MONO: a legato note slides without restarting, and a chord plays one note.
- **The wobble is the random pitch LFO;** X-MOD adds the weight and the sidebands, not the wobble.
- **More tape:** CHEW is on at a mild setting. Turn it up for dropouts (they start around the middle of the knob and grow toward the top); it costs more CPU.
- Turning OSC 2's level to 0 does not remove it entirely: it still modulates through X-MOD.

**Gear inspirations**

- **Korg Mono/Poly** — the cross-modulated source: *fat, drifting*.
- **Sequential Prophet-5** — *wobble, nervous*.
- **Roland RE-201 Space Echo** — the worn tape stage: *wobble, lo-fi*.
- **Roland SH-101** — *punchy*.

Closest to: **a Mono/Poly cross-mod square through a worn tape echo**.

#### 08 · Wire Bite

An anxious, thick drone that bites, like touching a live wire. Six stacked pulse waves in the high register, with an upper layer an octave and a fifth above, through a resonant filter that zaps at the start of every note. Fat and bright, and it never sits still: the voices wander on their own and the whole stack leans and jitters in pitch. Dry, and each note is chopped off the moment you let go.

**Sound design notes**

- **Where it lives:** high, around A3 to E5: held notes and short bites.
- **Play it detached.** It is a unison of six voices: a legato note slides in without the zap, and a chord plays one note.
- **The zap is subtle** because the body is already so bright; a lower CUTOFF makes the strike stand out more.
- **The drift is built in:** every voice wanders on its own, and a slow random LFO leans the whole stack. SLOBBER multiplies it.

**Gear inspirations**

- **Korg Mono/Poly (in unison)** — the stack: *fat, drifting*.
- **Minimoog** — *thick*.
- **Korg MS-20** — the bite.
- **Roland Jupiter-4** — *fat, wobble*.
- **Sequential Prophet-5 (early revisions)** — the unsteadiness: *drift*.

Closest to: **a Mono/Poly in unison with MS-20 bite**.

### CHAPTER II — BEE-TCH

*Surf rock and skinhead reggae: the spring-reverb chapter. On screen: the Bee-tch scene, accent Wave Turquoise.*

#### 09 · Skeenhead

A tight, plucky square stab with a resonant plop on the front, drenched in spring. The note holds its body for as long as you play it; the spring rings on after the note and is the sound of the patch. A wet, springy, boingy reggae stab.

**Sound design notes**

- **Where it lives:** off-beat two-note stabs of about a tenth of a second, around A3 to C4: the skank.
- **The spring is the sound.** It sits a little under the note while you play and rings louder than it just after: that's the boing. DRAIN is the knob if you want it drier.
- **The plop is soft on purpose:** the filter rests above the notes so the body survives the gate. RESO brings more plop.
- It is a stab patch: one oscillator, steady, no wobble. Chords up to five notes.

**Gear inspirations**

- **Korg MS-20** — the resonant filter plop: *plucky, biting*.
- **Roland SH-101** — the tight, quick stab: *tight, punchy*.
- **Moog Prodigy** — the single raw square: *fat, cheap, raw*.
- **Fender spring reverb tank (Twin Reverb style)** — the drench: *springy, boingy*.
- **Roland RE-201 Space Echo** — the dub-style tail: *warm*.

Closest to: **an MS-20 plop into a Fender spring tank**.

#### 10 · Atlantic Swell

A bright organ: two narrow pulse waves through a notch filter, played polyphonically, with a spring behind it and nothing else. No vibrato, no chorus, no echo. The two pulses beat slowly against each other, so a held chord swells and dips about once a second, and the spring rings on after the notes.

**Sound design notes**

- **Where it lives:** organ chords and short stabs, around A3 to C5. Up to five notes.
- **The movement is the two pulses beating,** not an LFO: OSC 2's FINE changes the speed, and centring it stops the beating.
- **Fast playing blurs into the spring:** under quick staccato notes the tail catches up with the notes. DRAIN down for a tighter organ.
- **For vibrato or a rotary feel,** add LFO PITCH (LFO DEST page); a real chorus or rotary is not in this engine.

**Gear inspirations**

- **Farfisa Compact** — *nasal*.
- **Vox Continental** — *reedy, bright*.
- **Fender spring reverb** — *springy*.

Closest to: **a combo organ into a spring tank**.

#### 11 · Slapback Strut

A tight, gated surf bass: the note starts at once, holds its body for as long as you hold the key, and stops dead. Behind each note comes one clean, loud slap: a plain copy of the note a moment later, then nothing. Bright and crisp on top for a bass, sharp and a little biting, and dry otherwise.

**Sound design notes**

- **Where it lives:** low, A1 to A2: surf bass lines.
- **Play it detached.** It is MONO: a legato note slides without a new hit.
- **It is gated, not plucked:** the note holds flat for as long as you hold the key. Short notes for a pluck feel.
- **The slap is already as loud as the echo goes,** about 6 dB under the note. The delay's TONE does little here: the slap is a copy of the note, so shape the note.
- **Bright for a bass:** it can buzz on a very bright amp; CUTOFF down tames it. A spring (DRAIN) is yours to add.

**Gear inspirations**

- **Fender Precision Bass (flatwounds)** — the snappy attack: *snappy*.
- **Roland SH-101** — the tight, quick note: *tight, punchy*.
- **Minimoog** — the round low end: *round*.
- **Binson Echorec / Roland RE-201** — the single slap: *slap, warm*.

Closest to: **a flatwound P-Bass into a Space Echo**.

#### 12 · Kelp Tangle

A pad of pulse waves whose widths are swept slowly and steadily by one triangle LFO, through a steep low-pass that leaves little up top, with a spring tail behind it. Dark and moving on held notes; on short notes you only hear a slice of the sweep. No vibrato, no echo.

**Sound design notes**

- **Hold the notes:** the sweep takes about a second, so it is a held-note effect. Short notes barely move.
- **Where it lives:** held notes and chords from A2 up; up to five notes.
- **Each detached note restarts the sweep,** so every note begins the same way.
- **Brighter:** CUTOFF up opens the top. **Deeper movement:** more DRIVE (MIXER page) deepens the sweep's colour but flattens its level swing.
- One LFO moves both oscillators at the same rate; there is no Poly-Mod here.

**Gear inspirations**

- **Moog Prodigy** — *dark, raw, murky*.
- **Fender spring reverb tank** — *springy*.
- **Roland Juno-60** — the pulse-width sweep: *PWM*.
- **Korg Polysix** — *fat, PWM*.

Closest to: **a Polysix PWM pad into a spring tank**.

#### 13 · Ghost Board

A dark pad: two slightly detuned pulse waves, played polyphonically, beating slowly against each other, with a long echo and a heavy spring behind every note. Very muddy, on purpose: almost nothing up top, all low-mid body and tail.

**Sound design notes**

- **Where it lives:** held chords and slow lines, around A3 to G4. Up to five notes.
- **The movement is the two oscillators beating** about once a second; OSC 2's FINE sets it, and centring it stops it.
- **The tail is big:** the spring is louder than the chord for a moment after you let go, and the echo (337 ms) follows. Short notes sink into it.
- **It is quiet on short stabs** compared with held chords.
- **Brighter:** CUTOFF up. It is a first pass Vincent means to dial further on the unit.
- There is no tape on it: the warped-tape idea of the first brief was dropped by ear.

**Gear inspirations**

- **Roland RE-201 Space Echo** — the echo: *wet*.
- **Fender spring reverb tank** — *springy*.
- **Mellotron M400** — the reference for the tone that was chased: *dark*.

Closest to: **a dark Mellotron voice through a Space Echo and a spring tank**.

#### 14 · Reef Break

A crash made of a burst of noise over a square-wave sub. The noise swells in over a fraction of a second rather than striking at once, the lows fall away first and the top rings out longest, as a cymbal does, and a long echo follows each hit. No spring, no tape.

**Sound design notes**

- **Where it lives:** single hits, low (A1) or mid (A2). Hits about 400 ms apart or more let each one bloom.
- **It swells in:** both envelopes have a 299 ms attack, so the crash peaks just after the hit. For a harder strike, bring the AMP and FILTER ENV attacks down.
- **The dry crash rings out in about a second; the echo runs several seconds.** The BBD page's MIX or FEEDBK shorten it.
- **Three keys at once** stack three noise voices and get loud: one key per hit.
- It is noise only: no metallic cymbal partials.

**Gear inspirations**

- **Roland TR-808** — *thick sub*.
- **Simmons SDS-V** — *noise burst*.
- **Roland RE-201 Space Echo** — *long repeats*.

Closest to: **an 808 kick with a noise burst into a Space Echo**.

#### 15 · Trem Chop

A broken-strobe tremolo: a bright saw chopped on and off by a hard square-wave LFO, not a gentle sine. Every note is two voices, and the pair chop slightly out of step, so the chop has an off part, a half part and a full part instead of a clean on/off. Dry.

**Sound design notes**

- **Where it lives:** held notes, riffs and three-note chords around A3 to A4. Every note is two voices, so three notes fill it.
- **The chop does not follow the tempo.** It ships at sixteenths for 120 BPM. Set it by ear with LFO RATE (SELECT on HOME): RATE 87 is eighths and 101 sixteenths at 120 BPM; at 140 BPM, 90 and 104; at 90 BPM, 81 and 95. Over a long phrase it slowly slides against the beat.
- **Notes don't always start on:** the chop runs freely, so a note can begin in an off part.
- **It reads a little hot** next to the rest of the bank: about 2.5 dB on stabs.

**Gear inspirations**

- **Roland SH-101** — the source: *bright, punchy*.
- **Boss TR-2 Tremolo (square setting)** — the chop: *choppy, gated*.
- **Electro-Harmonix Pulsar** — *choppy, rhythmic*.
- **Korg Polysix** — *drift*.

Closest to: **an SH-101 saw through a Boss TR-2 on square**.

#### 16 · Tidal Pull

A stereo chord wash of soft, triangle-like tones (narrow pulses through a low-pass, with an octave-up copy), moved by a slow vibrato. The notes come in gradually, an echo follows each one and a spring rings behind both. A dark patch, not a bright one.

**Sound design notes**

- **Where it lives:** held chords (sevenths suit it) around F3 to G4. Up to five notes.
- **It fades in,** so held chords bloom and short stabs stay quiet.
- **The echo sits above the spring** (337 ms): you hear the repeat first, then the spring around it.
- **Wider:** DUAL mode with more voices widens it at the cost of polyphony and CPU.
- Soft and dark by design; CUTOFF up brightens it.

**Gear inspirations**

- **Roland Juno-60** — a wash of pulses: *wash*.
- **Fender Twin Reverb** — the spring: *springy*.
- **Roland RE-201 Space Echo** — the echo: *wet*.

Closest to: **a Juno-60 chord pad through a Twin Reverb spring and a Space Echo**.

### CHAPTER III — MOONSHINE

*Dark fantasy and atmosphere: drones and slow pads. Most of them want a held key, so REC (HOLD) is your friend here. On screen: the Moonshine scene, accent Foam White; hold a note and the dog howls.*

#### 17 · Titanic

Cold, heavy and hollow: two saws a fifth apart, steady rather than seasick, with a deep, sub-heavy floor. Low notes open up and ring out big; high notes close down and go dull, so the weight lives at the bottom of the keyboard. Dry, desolate, and it hangs on after you let go. The chapter's anchor.

**Sound design notes**

- **Where it lives:** low, roots and fifths around A1 to A2, where it opens up. Played high it goes dark and dull: that's the design.
- **Chords: three notes.** Every note is two voices.
- **It is a held-note patch:** the release is long (about 1.3 s), so quick chopped notes overlap.
- **Add space:** DRAIN puts a cold cloud above the dry weight. CHEW adds a dying-tape feel, at more CPU.

**Gear inspirations**

- **Yamaha CS-80** — cold, epic, slow weight: *fat, sub-heavy, desolate*.
- **Moog Taurus** — the floor under everything: *deep, floor-shaking*.
- **Memorymoog** — the thick, dark body: *thick, dark*.
- **Sequential Prophet-5** — two saws a fifth apart: *fat, warm*.

Closest to: **a CS-80 played low and cold**.

#### 18 · Roto-scopo

A low, dark drone: a square wave with a second square an octave below, played by three slightly out-of-tune voices. A resonant low-pass opens and closes slowly and unpredictably by itself, so the tone moans and drifts without a knob being touched. Dry. It lasts only while a key is held.

**Sound design notes**

- **Hold it:** a key, the sustain pedal or REC (HOLD). REC keeps it going until you press REC again or STOP.
- **One note at a time:** it is a three-voice unison, so a chord plays its last key.
- **Where it lives:** low, A1 and A2.
- **It fades in slowly,** so a short tap is much quieter than a held note.
- **The wander is one slow random LFO on the cutoff:** LFO RATE (SELECT on HOME) speeds the moaning up.
- Its slop is already at the top (VINTAGE 127); SLOBBER adds more.

**Gear inspirations**

- **Korg MS-20** — the resonant low-passed square: *resonant, unruly*.
- **ARP 2600 sample-and-hold** — the wandering cutoff (here a smooth random, not stepped).
- **Moog Taurus I** — *dungeon-low weight*.

Closest to: **a Taurus-weight square through an MS-20 filter that a random source keeps nudging**.

#### 19 · Micro-mist

A soft-attack chord in the mid-to-upper register: a saw with a slightly sharp square an octave above it, through a band-pass filter. It hovers on its own echo and a large spring and keeps hanging in the air for several seconds after you let go. Bright rather than low, and smooth: a held pad dissolving into its effects, not a granular texture.

**Sound design notes**

- **Where it lives:** chords in the mid-to-upper register. Nothing sits under 150 Hz, so it is not for low notes. Up to six notes.
- **The mist after you let go is the echo and spring,** not a latch: it falls away over about six seconds after a long chord. To hold the chord itself, use the sustain pedal or REC (HOLD).
- **It fades in,** so short taps are faint.
- **The spring leads the echo.** DRAIN and the BBD page's FEEDBK set how long it hovers.
- The LFO is set but does nothing at these values; turn up LFO FILTER or PITCH to add flicker.

**Gear inspirations**

- **Hologram Microcosm** — the haze and the hanging wash: *wash, wet*.
- **Yamaha CS-80** — the soft pad voice: *soft, swelling*.
- **Roland Jupiter-8** — the bright top: *bright*.

Closest to: **a CS-80 pad dissolved in a Microcosm haze**.

#### 20 · Fire & Ice

A single-voice lead that tears into every detached note with a bright hard-sync sweep, then settles into a rounder line. Pushed into overdrive and thrown into a long, ping-ponging echo that sits on top of a short spring. Notes slide into each other a little.

**Sound design notes**

- **One note at a time.** It is MONO.
- **Detached notes rip; legato notes don't.** Play a run legato and only the first note tears.
- **The echo is a fixed 374 ms,** not tied to the tempo: set ALLEY by ear to sit it in your song.
- **The glide** is short (an octave in under a tenth of a second); GLIDE on the VOICE page lengthens it.
- Its drive is GROWL: turn it down for a cleaner lead.

**Gear inspirations**

- **Sequential Pro-One** — the hard-sync lead: *rip, bright*.
- **Ibanez Tube Screamer** — the soaring drive: *driven*.
- **Roland RE-201 Space Echo** — the drench: *wet*.

Closest to: **a Pro-One sync lead through an overdrive pedal into a Space Echo**.

#### 21 · Cowl Shadow

A brass wall that starts dark and soft and swells open while you hold the note: a quiet, murky hum that, over a few seconds, blooms into a wide, full, glowing brass, with a slow drift inside the stack. Dry. When you let go it fades out slowly and darkens as it goes.

**Sound design notes**

- **Hold the note:** the bloom takes about five seconds. Let go early and it never opens, it just fades dark.
- **It sounds quiet if you tap a note.** Hold it and it comes up to full level. The sustain pedal or REC (HOLD) should keep it open the same way.
- **One note at a time:** five voices in unison.
- **Legato does not restart the bloom:** release and play again to bloom again.
- It ships dry; a little DRAIN adds depth.

**Gear inspirations**

- **Yamaha CS-80** — the slow brass swell: *soft, slow, swelling*.
- **Oberheim OB-Xa** — the brassy body: *brassy, full*.
- **Roland Jupiter-8** — the bright blare at the top of a swell: *bright*.
- **Korg Mono/Poly (in unison)** — the stacked, drifting oscillators: *fat, drifting*.

Closest to: **a CS-80 brass swell, stretched**.

#### 22 · Melting Orb

A thick stack of detuned saws that opens bright when the key goes down and then slowly sinks: the filter closes and the pitch falls together over a few seconds, until the sound settles low and dark. A held collapse, not a zap. It takes chords. Dry.

**Sound design notes**

- **Hold the key:** the melt happens while it is down; the pitch ends almost seven semitones lower after about four seconds. A short tap gives only the bright opening.
- **Chords: three notes** (every note is two voices). A chord is loud: it is what sets the patch's level.
- **When you let go, the melt partly runs back up** as the note fades.
- **Deeper or shallower melt:** ENV>O2 on the OSC MOD page. OSC 1 is off on purpose: it would stay at pitch while the rest sinks.
- It is the heaviest patch on the CPU in the host tests; watch the reading on GLOBAL if you add effects.

**Gear inspirations**

- **Oberheim OB-Xa** — a fat unison source.
- **Sequential Prophet-5** — the slow filter-envelope sweep.
- **Korg MS-20** — *resonant*.

Closest to: **an OB-Xa-style fat stack whose filter and pitch both sink slowly downward**.

#### 23 · Crypt Dust

A thin, narrow pulse through a band-pass into a pale, dusty tone, with only a trace of noise under it. The level flutters slowly and irregularly, in steps. A short echo and a large spring blur it. It rises slowly when you press a chord and hangs on after you let go.

**Sound design notes**

- **Hold the chord:** a key, the sustain pedal or REC (HOLD). It is a held-chord pad; it fades in slowly, so short notes are faint.
- **Chords: up to four notes.**
- **The dust is the NOISE knob** (MIXER page). Keep it low: more noise quickly drowns the thin pulse.
- **The flutter is one stepped LFO** on level and filter: LFO RATE changes its pace.
- A chord peaks close to the limit, so there is little VOLUME headroom. There is no tape on it.

**Gear inspirations**

- **Korg MS-20** — noise plus a thin pulse: *thin*.
- **Roland RE-201 Space Echo** — the worn echo.
- **Mellotron M400** — the dusty, pale tone as the reference.

Closest to: **a thin pulse and a trace of dust through a band-pass, into a short echo and a large spring**.

#### 24 · Fugue State

A soft, dark, triangle-like pad whose pitch trembles quickly, wide in the stereo field. Each chord runs into a short echo that feeds back while the pitch is still moving, so the repeats sit at slightly different pitches from the notes and the chord smears. A spring adds a further tail, and it hangs on for seconds after you let go.

**Sound design notes**

- **Hold the chord:** it fades in, so stabs are quiet. Up to five notes.
- **The tremble is a fast vibrato** (about 5 per second): LFO RATE slows it toward a seasick sway, LFO PITCH sets its depth.
- **The echo is short (144 ms) and fed back hard,** so it smears rather than repeats. FEEDBK higher hovers longer; past about 120 it starts to run away.
- **HEEL clears the echo** if it gets out of hand.

**Gear inspirations**

- **Electro-Harmonix Deluxe Memory Man** — BBD feedback with pitch movement: *wet*.
- **Roland RE-201 Space Echo** — echo feedback: *wash*.
- **Korg Polysix** — the dizzy ensemble feel: *wobble*.

Closest to: **a soft triangle-like pad run through a Memory Man until it seasicks itself**.

### CHAPTER IV — ACID CAN

*The survivors of the classic polysynths, rebuilt by ear (never copied from factory data), then the signature patch and the blank slate. On screen: the Acid Can scene, accent Acid Chartreuse.*

#### 25 · SAWTOOTH

The iconic poly brass: two saws a few cents apart, stable and warm, with the filter swelling open on each note and settling into a solid, brassy body. It holds still: no wobble, no chop, only a gentle vibrato that fades in if you hold a note. A survivor of the classic polysynths, rebuilt by ear.

**Sound design notes**

- **Where it lives:** low-mid to mid, chords and fifth-and-octave voicings. Each note is one voice, so ordinary chords play in full.
- **Medium to long notes show the swell best:** it peaks just under a tenth of a second in, so a very short stab catches only the start.
- **The vibrato** arrives after about a second on held notes; LFO PITCH at 0 makes it fully still.
- **The steady counterpart to 03 Half-Life.** SLOBBER makes it wobble like tired string-brass; Tape Stop is a good swell-out ending.
- **All effects are at 0:** a dry brass, with a spring or echo yours to add.

**Gear inspirations**

- **Sequential Prophet-5** — the swell and the two-saw body: *fat, warm, swell*.
- **Oberheim OB-Xa** — the brass-section feel: *brassy, full*.
- **Roland Jupiter-8** — the bright blare at the top of the swell: *bright brass*.
- **Memorymoog** — the weight of the chord: *thick, warm*.
- **Korg Polysix** — the slow vibrato on a held note: *wobble*.

Closest to: **a Prophet-5 brass swell**.

#### 26 · BSyncA

A hard-sync lead built from three slightly detuned voices that beat slowly against each other, with the master oscillator audible under the synced one. Every detached note starts with a bright sweep that tears down into a duller body; it is pushed into drive and left dry, with a short glide between notes.

**Sound design notes**

- **One note at a time:** three voices in unison.
- **Detached notes rip; legato notes don't.**
- **The drive darkens the strike:** GROWL down for a brighter rip and less crunch, up for more crunch and less rip.
- **Where it lives:** leads from about A3 up.
- Dry: no echo, no spring, no tape. The glide is short.

**Gear inspirations**

- **Sequential Prophet-5** — the classic sync solo: *sync, ripping, fat*.
- **Sequential Pro-One** — the sweep itself: *rip, bright*.
- **Moog Prodigy** — the raw edge: *raw, biting*.
- **ARP Odyssey** — the nasal cut: *nasal, biting*.

Closest to: **a Prophet-5 sync lead pushed into crunch**.

#### 27 · R3V3RT

A single-voice bass from one pulse wave. Each note opens with a bright filter snap that falls into a lower body; the body holds steady for as long as the key is down, and the note stops almost at once when you let go. Dry.

**Sound design notes**

- **Play it detached.** It is MONO: a legato note has no snap and no front edge.
- **Where it lives:** A2 and around it. A1 is mostly below what a small speaker can play.
- **The snap is the filter envelope:** FILTER ENV's DECAY lengthens it, ENV AMT makes it stronger.
- It stops almost instantly on release: tight enough for fast lines.

**Gear inspirations**

- **Roland SH-101** — the tight, quick note: *tight, punchy*.
- **Minimoog** — the round low end: *round, thick*.
- **Moog Prodigy** — the plain pulse: *raw*.
- **Sequential Pro-One** — the snap of the filter decay: *snappy*.

Closest to: **an SH-101 pulse bass with a Minimoog body**.

#### 28 · Arr 2 Dee 2

A sustained, struck bell built from two saw waves with a mid-range sideband ring. It rings for several seconds after the strike, a slow shimmer moves its pitch and level, and a small echo and a spring sit behind it. No drive, no tape.

**Sound design notes**

- **The key you press is the bell's hum,** its deepest partial; the strike may sound an octave above the key.
- **It rings on after you let go:** five or six seconds to fade. Leave space between notes, or let them pile up.
- **Shape it live:** CUTOFF and X-MOD change the brightness without changing the bell. Leave ENV>O2 at the centre: a step either way breaks the bell.
- **Where it lives:** A2 to A6, level across the whole keybed; the top octave is bright. Up to five notes; a fast run is its loudest phrase.
- **CPU:** adding CHEW or GROWL on top costs a lot here; on the unit, four notes with all effects pushed read about 4500 of 5800 µs on GLOBAL.

**Gear inspirations**

- **Yamaha DX7 (tubular-bells voice)** — the FM ring: *inharmonic*.
- **A struck tubular or church bell** — the classical bell partials.
- **Casio CZ-101 (phase-distortion bells)** — a bright, bell-like tone (inspiration only).
- **Roland D-50 ("Fantasia")** — crystalline (inspiration only: the engine can't make a tail that outlasts its body).

Closest to: **a DX7 tubular bell with a long, slowly moving tail**.

#### 29 · i scream

A bright, struck chime from a square wave, with a second oscillator that zings down in pitch at the strike. The ring decays over a couple of seconds, and a gentle shimmer in pitch and level fades in and sways it. A small slap and a touch of spring sit behind it, and everything passes through a narrow, honky band, like a small horn speaker. Closer to an arcade chime than to finger cymbals.

**Sound design notes**

- **Where it lives:** A4 to A6: melodies with notes about half a second apart, so the rings overlap.
- **Three-note chords play whole** and are its loudest sound: use one as a wind chime.
- **The zing is OSC 2:** it fades out toward the top of the keybed. ENV>O2 sets how far it drops.
- **Built by ear** from Vincent's phone recordings of a real ice-cream van outside his house; nothing is sampled.
- No tape: CHEW is 0, so there is no wow or hiss.

**Gear inspirations**

- **Yamaha DX7 (tubular-bells voice)** — the zing: *FM, inharmonic*.
- **Finger cymbals (zills)** — *bright ping*.
- **A transistor radio or van horn speaker** — *band-limited, honky*.
- **A music box, struck** — the idea of it (its ring here is longer).

Closest to: **a music-box chime through a cheap van horn speaker**.

#### 30 · THE DØG

A dry, punchy unison bass: every voice stacked on one note, fat and thick, loosened just enough that the stack breathes without going seasick. Warm, with a driven edge that stops short of fuzz, and each note is chopped hard on release: no spring, no echo, no tail, only the silence after the hit. The flagship, the DØG-5 signature: it sits forward and fills the room.

**Sound design notes**

- **Where it lives:** low, A1 to A2. It suits single-note bass lines and chopped roots; eighth-note chops are home, and it holds as a wall too.
- **One note at a time:** it's a unison, every voice on one key, so it plays no chords.
- **On small speakers** the very bottom (A0, low A1) partly drops out.
- **It's a touch louder than the rest of the bank on purpose:** it jumps forward when you switch to it.
- **More grit:** MIXER's DRIVE (knob 4) is the gentle route. GROWL is the big step and does nothing below about 28.
- **Keep it dry:** delay or spring blurs the chop. SLOBBER loosens the stack, Tape Stop dives it, and HEEL stops it dead.
- **Watch the CPU here:** with all four effects pushed and four notes held it reads about 5,600 of the 5,800 µs budget, the highest in the bank.

**Gear inspirations**

- **Minimoog in unison** — the stacked saws and the octave-down body: *fat, sub-heavy, thick*.
- **Moog Taurus bass pedals** — the weight at the bottom: *deep, floor-shaking*.
- **Roland SH-101** — the quick attack and the hard stop: *tight, punchy*.
- **Oberheim OB-Xa in unison** — the wide, full stack with its warmth: *fat, full, warm*.
- **Korg MS-20** — the grit in the filter when it is pushed: *nasty, biting*.

Closest to: **a Minimoog in unison with Taurus weight**.

#### 31 · Fi(l)fth

The aggressive chord stab: a fifth built into every note, a hard filter pluck, and a short slap-back echo right behind it. Each note is a detuned pair, so it is fat and punchy, with a bright snap on the front that settles into a solid body. Dry apart from the slap. The top-voted DØG-5 sound.

**Sound design notes**

- **One finger is a power chord:** every note carries its own fifth. Roots and octaves around A1 to A2 are home.
- **Short and hard:** stabs of about 150 to 200 ms. The stab is as long as you hold the key.
- **Chords stack fifths on fifths** into sus2-style clusters. That's the patch, not a fault: use real chords sparingly, three notes at most (every note is two voices).
- **The slap is ALLEY:** turn it up on the BBD DELAY page for a longer echo. A spring blurs the stab.
- It is heavier on the CPU than a single-voice stab.

**Gear inspirations**

- **Sequential Prophet-5** — the stab itself, with weight behind it: *punchy, fat, warm*.
- **Roland Juno-60** — the short, snappy pluck: *plucky, punchy*.
- **Roland Jupiter-8** — the open top on the attack: *bright, full*.
- **Korg MS-20** — the bite when you dig in: *biting*.
- **Roland RE-201 Space Echo** — the short slap: *slap, warm*.

Closest to: **a Prophet-5 stab through a Space Echo**.

#### 32 · Init bruv?

A plain voice: two saw waves through a low-pass filter with a short envelope. Dry, with chords and single notes both playable, and nothing added: no modulation, no echo, no spring, no tape, no drive. The blank slate that closes the bank.

**Sound design notes**

- **Start here:** it is the engine's own default program (at VOLUME 97). Every empty slot in THE PACK (33 to 99) starts from the same sound.
- **Chords play:** up to five notes.
- **Every effect is at 0,** and at 0 each one is a true bypass, so nothing colours it until you turn something up.
- **Where to go first:** OSC 2 off for one raw saw; CUTOFF up and RESO down for an open sound; FX held for the four Psych Chain macros.

**Gear inspirations**

- **Sequential Prophet-5** — an analog init patch (here two saws through a gently closed filter, not one open saw).
- **Minimoog** — a raw oscillator to start from.
- **Roland SH-101** — a plain saw to start from.

Closest to: **an analog two-saw init patch**.

## PART 4 — ABOUT THE GEAR INSPIRATIONS

Each patch lists real instruments and pedals whose *character* it draws on, with the trait it carries in italics, so
"a bit more Mono/Poly" points somewhere you can hear. They are inspirations, not imitations: nothing is modelled,
sampled or copied, and the gear names appear only in this manual, never in patch names or on the screen. "Closest to"
is the one instrument you'd name if someone asked what it sounds like; it doesn't claim the patch matches it.

All trademarks belong to their owners. DØG-5 is not affiliated with or endorsed by any of them.
