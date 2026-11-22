# DØG-5 — DRIVER MANUAL, PART 3–4 (the 32 patches and gear inspirations)

*Continues `DOG-5-driver-manual.md` (Parts 0–2B). Last updated 12 Nov 2026 (Chapter IV checkpoint: **all 32 voiced**; installed on the FM-1 on 12 Nov, see `DOG-5-device-test-1.md`). **Updated 18 Nov for v0.2:** 14 Reef Break's new attack; REC = HOLD (the drone latch) where entries said there was none; DRIVE's new page; no tap tempo. **Updated 21 Nov for v0.4.4:** the chapters carry their scene names (JALOPY · BEE-TCH · MOONSHINE · ACID CAN, locked 17 Nov; the old long titles are retired) and their on-screen accent colours; THE POUND is write-locked (Manual 1.9).*

## PART 3 — THE 32 PATCHES

Four chapters of eight. Each chapter is a scene on HOME (the painting the dog stands in, Manual 1.8) with its own
accent colour, and a sonic character. Entries marked **VOICED** are the approved, player-facing description of the
finished patch (with gear inspirations in Part 4). Factory patches 1–32 = THE POUND (write-locked: you can play and
change them, and a save goes to THE PACK, 33–99).

**All 32 are voiced: Chapters I, II, III and IV are complete.** *(This includes the minimum-gig set.)* The
patches were voiced on a host renderer and approved by ear; on 12 Nov 2026 Vincent installed the firmware on his
FM-1 and reported that all 32 sound distinct and on brand (his words, not measured). Numbers in the entries below
are host measurements unless an entry says otherwise. Real-device CPU readings are in
`DOG-5-device-test-1.md`.

### CHAPTER I — JALOPY
*Egg punk & garage psych. On screen: the Jalopy scene, accent Sun Yellow. Fat sources through a blown console.*

- **01 Red Pill — VOICED (5 Nov 2026, approved as is; variant C of Batch 3A).**
  - *What it sounds like:* A nervous, spitting bass made to sit under a vocal. Two fat saws, stacked and held
    steady, push through a resonant filter that snaps at the start of every note, driven hard enough to be
    gritty and warm without getting piercing. It is nearly dry: a quick slap and a small spring sit behind
    each note as an afterthought, lifting it a little and never coming near the note's own loudness.
  - *How to play it:* Low. It was voiced on a riff from A1 up to A2 and on sixteenth-note bursts; other
    registers are untested. About half of the energy of the low riff is the A1 fundamental, under 60 Hz, so on
    a small speaker it is the harmonics from about 100 Hz up that carry it. Short detached notes (80–150 ms)
    are home: the filter snap gives the spit. **It is MONO, so legato doesn't re-fire the snap** — play it
    detached; a chord plays one note (the last). The wet is measured: in the loudest of three isolated notes
    it sits 43.6 / 25.0 / 16.5 dB under the dry note in the 0–20 / 20–100 / 100–250 ms windows, with a short
    wet tail of about half a second after key-up. Part of the grit is a GROWL step, so it costs more CPU than
    a plain bass (about 1640 host instr/sample worst case). Slot 1 is the boot patch. Tricks (SLOBBER, SEQ
    held, kill switch, CHEW) are untested on it.
- **02 Cement Grind — VOICED (5 Nov 2026, approved as is; variant D of Batch 3A).**
  - *What it sounds like:* A low-mid grinder built from two fat pulse waves whose widths sweep quickly, so
    every note shudders and churns on purpose: a clear, fast pulse-width wobble, not a shimmer. The filter
    bites, it is pushed into a moderate crunch, and each note starts with a little skid and a snap. Thick,
    dry, and it hits hard.
  - *How to play it:* A2 up to E3 with G2 (the riff it was voiced on), in notes of about 400 ms, long enough
    for the wobble to swing two or three times inside a note; other registers are untested. The wobble runs at
    about 11.5 Hz; on a held A2 it moves the 150–400 Hz band by about 12 dB and the overall level by about
    4 dB, and each detached note restarts it. **One LFO does both jobs:** the pulse-width sweep and a filter
    wobble run at the same rate; the original slow filter wobble is gone. **It is MONO — legato doesn't
    re-fire the envelopes;** play it detached. A chord plays one note. The note stops at once. Don't push the
    wobble depth much further (the sweep already just crosses 50% at the top of each swing). Light on CPU
    (about 298 host instr/sample). Tricks untested.
- **03 Half-Life — VOICED (4 Nov 2026, approved as is).** **The flagship of the unstable, chopped side; the
  DØG-5 thesis in one patch.**
  - *What it sounds like:* Fat, slop-heavy dual saws with a sub-octave underneath: seasick, never quite in
    tune with itself, and thick without going murky. Short notes are chopped stone-dead by the gate, and the
    tail doesn't fade, it sputters — a few ragged stutters as the note dies. A raw, dry, engine-only sound
    with no effects on it: the drift and the chop are the whole point.
  - *How to play it:* Low to low-mid register — roots and fifths from about A1 to A3, with fifth-and-octave
    power chords as home ground. Play it staccato: short notes of roughly 150–180 ms give a hard clean body
    and a sputtering tail. Held pads and sustained leads are the wrong job; use it for riffs and stabs. Keep
    chords to three notes (every note is two voices; a fourth note steals voices from earlier ones). Best
    trick: ride the ALGORITHM (SLOBBER) up to push it from seasick to dying tape motor. Tape Stop (SEQ held)
    makes a good riff ending; the kill switch (HEEL) stops the sound and the sputter dead. The Psych Chain
    macros are off on purpose; the dry chop is the sound, and a wash of ALLEY or DRAIN will bury the sputter
    (untested with this patch).
- **04 V-Sync — VOICED (4–5 Nov 2026, approved as is).**
  - *What it sounds like:* A tearing hard-sync lead: the pitch of the synced oscillator rips down on every
    note, nasal and biting, with a plain saw underneath for body. A pair of voices a few cents apart makes it
    fat enough to cut through a drum machine, and the note stops dead when you let go, with only a faint quick
    slap behind it. Raw on purpose: that is where the rip lives.
  - *How to play it:* Mid register, roughly A3–A4. One note at a time. **Play it staccato:** in MONO and
    UNISON a note struck while another is held slides in and doesn't re-fire the envelopes, so the sweep fires
    on detached notes only (a legato run glides and rips once, on its first note). The voice stops dead on
    release; a faint 1/16 slap follows each note (echo MIX to 0 for a literal dead stop). Tricks: ALGORITHM
    pulls the two voices apart, kill switch kills the slap too, Tape Stop dives a held note — all untested on
    this patch. A wash of DRAIN will blur the rip.
- **05 ZEAROX — VOICED (5 Nov 2026, approved as is; variant D of round 2 — round 1 was rejected).**
  - *What it sounds like:* A kick substitute made of one hard square wave, built toward a pixelated, gritty,
    blown-out sound like a photocopy reduced to pure black and white. The pitch drops fast over the first
    11 ms, and a random stepped pitch LFO moves it to a new value every 47 ms or so, so a 150 ms hit gets
    about three random pitch steps of up to ±4.7 semitones (a longer note gets more). The wave stays almost
    entirely at its two extreme levels, there is no attack, and the hit stops quickly. Dry: no tape, no drive,
    no echo, no spring.
  - *How to play it:* Low hits on A0, A1 and A2 (and four-in-a-bar A1 at 120 BPM); other registers are
    untested. **It is MONO — legato doesn't re-fire the envelopes;** play it detached. The kick is mostly the
    quick pitch drop; there is no click spike. **A0 is still mostly sub** (81% of its energy under 60 Hz after
    the first 20 ms): a 27.5 Hz square is inaudible on a small speaker whatever is done. VOLUME is 123 of 127,
    so there is almost no knob headroom above the bank reference. It is the lightest patch of its batch (about
    1337 host instr/sample). The random LFO is free-running, so it is not bit-comparable from the boot patch.
    Tricks untested.
- **06 zzuFuzz — VOICED (5 Nov 2026, approved as is; variant C of Batch 3A).** **The fuzz weapon.**
  - *What it sounds like:* A huge, thick wall. Two fat saws on every voice are pushed hard into the drive
    until the sound is flat and relentless, and it simply does not die while you hold the key. The strike is
    quick (about 2 ms), the filter and its resonance are wide open, and when you let go there is a short tail
    of about a third of a second rather than a ring. Completely dry: no echo, no spring. A power chord stays
    whole.
  - *How to play it:* A low A1 up to power chords around A2–E3–A3, held or stabbed; other registers are
    untested. The held note's level falls by nothing over three seconds, and its peak-to-RMS ratio is 1.7 dB
    (a square wave is 0). It is POLY with 6 voices, so every key re-fires the envelopes and a three-note
    chord plays whole. The strike's punch is the quick rise, not a level spike (+0.3 dB over the plateau):
    more punch would mean less wall. It reads about 2 dB hotter than the bank on the standard stabs phrase
    (the cause was not isolated), and VOLUME changes how a note from silence starts, because GROWL's loudness
    trim reads the output stage: set VOLUME first. Honest limit: it was built toward a Fuzz War-class wall
    from descriptions and approved by ear; nothing says it matches a real pedal, and the starved, gating
    sputter of the voltage-starved fuzzes is not in it. The GROWL costs about +595 host instr/sample (about
    1414 worst case).
- **07 Tape Splice — VOICED (5 Nov 2026, approved as is; variant B of Batch 3B).**
  - *What it sounds like:* A fat square with a wobble in its pitch, chopped short. Two square waves a hair
    apart, one frequency-modulating the other so the tone carries extra energy below the note, and a random
    pitch wobble (about 9.6 cents standard deviation, the LFO depth up to ±19 cents). Notes stop quickly when
    you let go, and a tape stage on the end delays each note by a couple of milliseconds. Dry.
  - *How to play it:* Staccato notes from A2 up to G3 (twelve 60 ms notes) and a held A2; other registers are
    untested. **It is MONO — legato doesn't re-fire the envelopes;** play it detached. A chord plays one
    note. The pitch wobble comes from the random LFO; X-MOD adds sidebands and low-end energy but does not
    move the measured pitch. No dropouts were measured at the shipped tape setting (a harsher setting, CHEW
    127, produces them and costs more). About 2177 host instr/sample worst case, about 770 of it the tape.
    Tricks untested.
- **08 Wire Bite — VOICED (5 Nov 2026, approved as is; variant D of Batch 3A).**
  - *What it sounds like:* An anxious, thick drone that bites, like touching a live wire. Six stacked pulse
    waves in the high register with a second layer an octave and a fifth above, through a resonant filter
    that zaps at the start of every note. Fat and bright (medium to high), and it never sits still: the
    voices wander on their own and the whole stack leans and jitters in pitch. Dry, and each note is chopped
    off the moment you let go.
  - *How to play it:* High: a held A4, eight 110 ms bites (E5, A4, C5, D5) and a held A3; low notes and
    other registers are untested. **It is a UNISON of 6 voices — legato doesn't re-fire the envelopes:** a
    key held while the next goes down slides and the zap doesn't happen again; play it detached. Chords play
    one note. The drift is measured from the engine's own log: static offsets of −9 to +7 cents between the
    voices, each wandering 4–6 cents, and a smooth-random pitch LFO leaning the stack up to 19 cents at 0.28
    Hz. The measured top-end burst at the strike is small, because the body is so bright; it was approved by
    ear. A bite is 40 dB down 18 ms after the key goes up. The original's echo and spring were removed (about
    1298 host instr/sample). Tricks untested.

### CHAPTER II — BEE-TCH
*Surf rock & skinhead reggae. On screen: the Bee-tch scene, accent Wave Turquoise. The spring-reverb chapter. All
eight patches (09–16) are voiced.*

- **09 Skeenhead — VOICED (4–5 Nov 2026, approved as is; variant E of round 2).** The reggae off-beat stab.
  - *What it sounds like:* A tight, plucky square stab with a resonant plop on the front, drenched in spring.
    The note has a body that holds for as long as you play it; the spring rings on after the note and is the
    sound of the patch. A wet, springy, boingy reggae stab.
  - *How to play it:* Off-beat two-note stabs of about a tenth of a second, around A3 to C4 (the skank it was
    voiced on); other registers are untested. The plop is still there but softer than in the first version —
    the first 20 ms is only a few dB above the body. The filter now rests above the played notes, so the body
    survives the gate. The spring is the sound: it ships at DRAIN 90, about 6 dB under the dry note over a
    stab, and is louder than the note in the 100–250 ms after it (natural for a spring), with a tail of about
    1.1 s. One oscillator, no LFO, no detune; VINTAGE is the default 30 (no wander was measured, so steadiness
    isn't claimed). It is a stab patch; held notes were not measured. Tricks (SLOBBER, Tape Stop, kill switch,
    ALLEY, turning DRAIN down) are untested on it.
- **10 Atlantic Swell — VOICED (6 Nov 2026, approved as is; variant A of Batch 4A, the starting point
  unchanged).**
  - *What it sounds like:* A bright pair of narrow pulse waves through a notch filter, played
    polyphonically, with a spring reverb behind it and nothing else. It has no vibrato, no chorus and no
    delay (measured). The two pulses beat slowly against each other and the spring rings on after the notes.
  - *How to play it:* Organ chords and short notes: voiced on an A minor triad (A3 C4 E4) held 2.4 s, a
    120 ms E4, four 120 ms notes and a D minor triad (D4 F4 A4); other registers are untested. POLY 5. The
    beating: on the held chord an A3 band swings 17.9 dB at about 1 Hz (no LFO is needed for it; the pulse
    width LFO, ±2.3 points, is not audible as PWM). Bright: the note-on centroid is 5369 Hz and 23% of the
    energy is above 1.2 kHz. The spring (DRAIN 40, SIZE 100) is louder than the notes by the last two of four
    staccato notes (−0.8 / −0.4 dB re each note), so fast playing blurs into the tail. Level −19.0 dBFS RMS on
    its own phrase at VOLUME 100 (the bank reference is −18.0 ± 1.5). Versions with a chorus, a rotary-speaker
    tremolo and a heavy echo were rendered (B, C, D, on the Batch 4A listening branch) and are not this patch;
    they stay a v1.1 candidate. "Cold" and "crisp" were not measured. About 2020 host instr/sample worst
    case. The first play after power-on differs from a program-load render by about −25 dB (not isolated).
    Tricks untested.
- **11 Slapback Strut — VOICED (4–5 Nov 2026, approved as is; variant G of round 2).** Percussive surf bass —
  now a **gated** bass with one loud slap.
  - *What it sounds like:* A tight, gated surf bass: the note starts at once, holds its body for as long as
    you hold the key, and stops dead. Behind each note comes one clean, loud echo, a plain copy of the note a
    moment later, and then nothing. Bright and crisp on top for a bass, sharp and a little biting, and dry
    otherwise.
  - *How to play it:* Low, A1 to A2 (the surf riff it was voiced on). It is a gated bass, not a pluck — the
    first version's pluck was traded away for crispness. There is no triangle oscillator, so the sound is a
    narrow pulse through a key-tracking low-pass, bright enough that its upper harmonics are near a square
    wave's: sharp and biting, and it may buzz on a very bright amp. The slap is one copy at 80 ms (first
    repeat about 6 dB under the note's peak, the second much lower) and already at the engine's maximum; the
    delay's TONE does nothing audible on this bass. Mono — **play it detached** (legato slides and doesn't
    re-hit). DRAIN ships at 0; a spring wash behind the slap is untested on this version.
- **12 Kelp Tangle — VOICED (6 Nov 2026, approved after listening; variant C of Batch 4A, CUTOFF 98).**
  - *What it sounds like:* A pad of pulse waves whose widths are swept slowly and steadily by a single
    triangle LFO, through a steep low-pass that leaves little in the high register, with a spring tail
    behind it. The sweep is measurable on held notes; on short notes only a slice of it is heard. No LFO pitch
    vibrato and no echo are set.
  - *How to play it:* Held chords and notes: voiced on a held A2 (3.2 s), the chord A2 E3 C4 (3 s) and six
    150 ms notes; other registers are untested. POLY 5. On a held A2, after the filter, the sweep moves the
    150–400 Hz band by 10.1 dB, the 400–1.2k band by 7.6 dB and the level by 5.7 dB; the LFO runs at 1.03 Hz
    and sweeps the pulse widths 18 to 48% (one side of 50%), restarted on each detached note (PHASE SYNC). On
    a 150 ms note it is only about 2 dB: **the PWM is a held-note effect.** Dark: centroid 531 Hz on the held
    A2, 0.8% of its energy above 1.2 kHz. The spring (DRAIN 55, SIZE 75) comes back at −47 / −13 / −6 dB re the
    dry chord in the first 250 ms; the tail is 60 dB down about 1.4 s after the chord, and its muddiness
    ratio is 10 / 15 / 77 in 0–250 / 250–750 / 750–1500 ms (the CUTOFF 86 variant was 29 / 39 / 180). Honest
    limits: one shared LFO moves both oscillators at one rate and there is no Poly-Mod, so "PWM driven by OSC
    B" is not possible; the 150–400 Hz depth tops out near 10 dB at any depth or cutoff measured. Level
    −18.0 dBFS RMS on its own phrase at VOLUME 74. About 2042 host instr/sample worst case. Tricks untested.
- **13 Ghost Board — VOICED (6 Nov 2026, approved after listening; variant C2 of Batch 4B round 2; the owner
  expects to dial it further on the FM-1).** *The brief changed after listening: the original called for a
  near-sine filtered triangle with maximum tape wow/flutter; the tape wobble was heard as "killing the
  overall tone" and was dropped, and the near-sine tone was not what was wanted.*
  - *What it sounds like:* A dark pad: a pair of slightly detuned pulse waves, played polyphonically,
    beating slowly against each other, with a long echo and a heavy spring behind every note. It is the
    original patch's voice, unchanged, with the pulse-width movement removed and no tape deck. By the
    dictionary's ratio it is very muddy.
  - *How to play it:* Held chords, a slow line and short notes: voiced on an A minor 7 chord held 2.4 s, four
    800 ms notes and six 150 ms notes; other registers are untested. POLY 5. No tape, no tape wobble (a
    one-voice probe reads 0.0 cents). The movement is the beating between the two oscillators: on one held
    voice the 150–400 Hz band moves 13.6 dB at 0.9 Hz (6.2 dB on the held chord). Dark and very muddy:
    note-on centroid 562 Hz, 0.2% of the energy above 1.2 kHz, muddiness ratio 315 (the original measured
    108); the tail 1108 / 2198 / 3331 in 0–250 / 250–750 / 750–1500 ms. The echo is 337 ms, FEEDBK 95, MIX
    105: on an isolated note the first repeat arrives 337 ms after the note-on at −8.7 dB re the note, 10.3 dB
    above the spring; the spring (DRAIN 70, SIZE 100) is louder than the chord for its first 250 ms or so.
    Level −18.0 dBFS RMS on its own phrase at VOLUME 55 (phrase (b) reads −23.4). About 2084 host
    instr/sample worst case (the tape was 784 of the earlier 2679). A program-load render is bit-identical
    from the boot patch (the earlier variant with the pulse-width LFO differed by −33 / −41 dB; this
    suggests the free-running LFO phase, not isolated). Tricks untested.
- **14 Reef Break — VOICED (6 Nov 2026, round-1 variant C of Batch 4B; the attack changed in v0.2 on 18 Nov,
  and Vincent approved the new version on the FM-1: "spot on", his words).**
  - *What it sounds like:* A crash made of a burst of noise over a square-wave sub. The noise swells in over a
    fraction of a second rather than striking at once, the lows fall away first and the top of the noise rings
    out longest, and a long echo follows each hit. There is no spring and no tape.
  - *How to play it:* One low hit (A1), one mid hit (A2), A1 hits 1000, 600 and 400 ms apart, every gate
    300 ms; other registers are untested. POLY 5. **Both envelopes have a 299 ms attack** (FILTER ENV and AMP ENV
    ATTACK 82, shown as `299ms`): on A1 the hit reaches 10 / 50 / 90% of its peak at 25.2 / 126.2 / 208.0 ms
    (A2 peaks at 268 ms), and the sub's band peaks 235 ms after the note-on, the top band (4k and up) 255 ms. By
    band, the time after the note-on at which each has fallen 20 / 40 dB below its own peak: 60–150 Hz
    308 / 316 ms; 1.2k–4k 435 / 1120 ms; 4k and up 923 / 1622 ms. The echo is 361 ms, FEEDBK 100, MIX 80: first
    repeats −13 / −18 / −23 dB re the burst, 8 repeats stay above −40 dB, no clipping. **The dry tail rings out
    in about a second; the echo runs several seconds.** Level −18.03 dBFS RMS on its own phrase at VOLUME 116,
    peak −4.17 dBFS. Three keys struck at once stack three noise voices and peak at −2.82 dBFS (no clipped
    sample). Limits: no inharmonic cymbal partials; noise and sub share one filter and one amp envelope. About
    1857 host instr/sample worst case (measured before the attack change). Tricks untested. *(The 6 Nov
    version struck at once, peaking at 27 ms; Vincent found it too harsh coming in.)*
- **15 Trem Chop — VOICED (5 Nov 2026, approved as is; variant D of Batch 3B; variant B was committed
  first).**
  - *What it sounds like:* A broken-strobe tremolo: a bright saw chopped on and off by a hard square-shaped
    LFO, not a gentle sine. Every note is two voices, and the two voices chop an eighth of a cycle apart, so
    the chop has an off part, a half-level part and a full part instead of a clean on/off. Dry: no echo, no
    spring, no tape.
  - *How to play it:* A held A3, a six-note riff of 500 ms notes, the chord A3 + E4 + A4 and short 110 ms
    notes; other registers are untested. It is DUAL with POLY 6, so every note is two voices: a three-note
    chord uses all six. The chop is 8.10 Hz (the nearest byte to sixteenths at 120 BPM), 44.8 dB between the
    on and off parts; the held note spends 35% of the time off, 31% at one voice's level and 33% at full.
    **There is no tempo sync with existing controls**, so the chop slides against a beat; the card carries
    the rate table (e.g. 140 BPM sixteenths = RATE 104, 9.42 Hz). The chop edges are steady to 0.18 ms:
    VINTAGE does not make them waver; the two-voice spread is what makes it sound unsteady. It reads about
    2.5 dB hotter than the bank on the stabs phrase, with a peak of −6.2 dBFS (limit −4), and costs about
    2375 host instr/sample. LFO PITCH is 0 (the original 8 was inert). Tricks untested.
- **16 Tidal Pull — VOICED (6 Nov 2026, approved after listening; variant D of Batch 4A, the triangle-like
  stack).**
  - *What it sounds like:* A stereo chord wash of triangle-like tones (narrow pulses through a low-pass, with
    an octave-up copy), moved by a slow triangle LFO on pitch. The notes come in gradually, an echo follows
    each note, and a spring rings behind both. It is a dark patch, not a bright one.
  - *How to play it:* Chords: voiced on A minor 7 (A3 C4 E4 G4) and F major 7 (F3 A3 C4 E4) held 2.0 s, three
    400 ms notes and three 100 ms stabs; other registers are untested. POLY 5. **It is triangle-like, not a
    sine, dark and peak-limited:** harmonics 3 / 5 / 7 read −17.2 / −27.3 / −36.8 dB against an ideal
    triangle's −19.1 / −28.0 / −34.2; centroid 595 Hz, 0.5% of the energy above 1.2 kHz, muddiness ratio 133;
    −19.1 dBFS RMS on its own phrase at VOLUME 76 (1.1 dB under the reference, inside ±1.5; the peak is −4.4).
    Attack 17 / 93 / 219 ms to 10 / 50 / 90%. The pitch LFO is triangle, 2.30 Hz, ±19 cents (LFO PITCH 16; the
    original 3 was inert), voices offset by PHASE SPREAD. The echo is 337 ms (ALLEY 104), FEEDBK 78, MIX 110:
    the first repeat is −8.6 dB re the note and **7.7 dB above the spring**. The spring (DRAIN 45, SIZE 90) is
    −39 / −19 / −14 dB re the note in 0–20 / 20–100 / 100–250 ms. The tail is 20 dB down at 1.2 s and 40 dB
    down at 2.4 s. Width: the held chord's L/R correlation is 0.70 dry, 0.66 with the echo and spring (an
    eight-voice DUAL version on variant B read 0.38; not measured here). On this phrase short notes do not
    reach the level of the held chords (the stabs read 7.7 dB under). The first play after power-on differs
    from a program-load render by about −24 dB (not isolated). About 2027 host instr/sample worst case.
    Tricks untested.

### CHAPTER III — MOONSHINE
*Dark fantasy & atmosphere. On screen: the Moonshine scene, accent Foam White; hold a note and the dog howls.
Drones and slow pads — these want long amp releases to survive the house hard-chop. (Live, a held-open gate helps:
**REC is HOLD** since v0.2, so press it with the notes down and they keep sounding until you press REC again or
STOP.)*

- **17 Titanic — VOICED (Nov 2026, approved as is; variant B of Batch 2A).** **The chapter anchor.**
  - *What it sounds like:* Cold, heavy and hollow: two saws a fifth apart, steady rather than seasick, with a
    deep sub-heavy floor. Low notes open up and ring out big; high notes close down and go dull, so the
    weight lives at the bottom of the keyboard. Dry, desolate, and it hangs on after you let go.
  - *How to play it:* Low — roots and fifths around A1 to A2, where it opens up; played high it is dark and
    dull, by design. Every note is two voices, so POLY 6 plays a three-note chord in full and a fourth note
    steals. It is a held-note patch: the release is long (about 1.3 s to silence), so quick chopped notes
    overlap (not auditioned on a fast riff by ear). It ships dry; the spring is clearly audible on it (about
    5 dB under the dry sound at DRAIN 60, mostly harmonics above 150 Hz — frozen or muddy is a matter of
    taste, untested by ear). Tape (CHEW) is an optional garnish for a dying-tape feel, at noticeably more CPU.
    Tricks untested on this patch.
- **18 Roto-scopo — VOICED (Nov 2026, approved; variant D of Batch 5A).** A moaning dungeon drone.
  - *What it sounds like:* A low, dark drone: a square tone with a second square an octave below it, played by
    three slightly out-of-tune voices. A resonant low-pass filter opens and closes slowly and unpredictably by
    itself, so the tone moans and drifts without a knob being touched. Dry: no echo, no spring. It lasts only
    while a key is held.
  - *How to play it:* **Hold a key, the sustain pedal or REC (HOLD);** the release is about 2.7 s nominal.
    **One note at a time:** a chord plays only its last key, and legato does not restart the
    envelopes. Best in the low register (judged on A1 and A2 holds of 15 s). A short tap is much quieter than the
    held note because the attack is slow. The wander is one shared random LFO on the cutoff; the engine has no
    Poly-Mod, so the movement cannot follow OSC 2 (measured on A1: the centroid ranges 316–708 Hz, a 14-semitone
    range). Slop is at the knob's top (VINTAGE 127). About 1897 host instr/sample worst case. Tricks untested.
- **19 Micro-mist — VOICED (Nov 2026, approved; variant D of Batch 5A round 2).** *Replaced "Blackwater", a
  sub-bass patch dropped on 6 Nov.* Neon pixels floating in the ether.
  - *What it sounds like:* A soft-attack chord in the mid-to-upper register: a saw with a slightly sharp square
    an octave above it, through a band-pass filter. It hovers on its own echo and a large spring, and keeps
    hanging in the air for several seconds after you let go. Bright rather than low, and it does not flicker or
    scatter: a held pad dissolving into its effects, not a granular texture.
  - *How to play it:* Chords work (POLY 6). **The mist after key-up is the effect tail, not a latch:** a held
    chord needs the key, a sustain pedal or REC (HOLD). After a 10 s chord the tail is 20 / 40 / 60 dB down at 1.6 / 4.1 /
    5.8 s. The spring leads the echo (first repeat 3.9 dB under the spring). Short notes are faint (a 150 ms
    chord tap is 8.7 dB under the held chord). Nothing sits under 150 Hz, so it is not for low notes. Not a
    real granular engine: no freeze, reverse or pitch-shifted repeats. The LFO is set but inert at these
    values. About 2000 host instr/sample worst case. Tricks untested.
- **20 Fire & Ice — VOICED (Nov 2026, approved; variant D of Batch 5B).** A soaring fantasy solo.
  - *What it sounds like:* A single-voice lead that tears into every detached note with a bright hard-sync
    sweep, which then settles into a rounder line. It is pushed into overdrive and thrown into a long,
    ping-ponging echo that sits on top of a short spring. Notes slide into each other a little.
  - *How to play it:* **MONO, one note at a time.** The sweep fires on **detached** notes; played legato the
    sweep is not re-fired (centroid over the first 100 ms of a riff: 3610 Hz detached against 1573 Hz legato).
    The sweep survives the filter (CUTOFF 84). Glide takes 94 ms for an octave step. The echo is a free 374 ms
    (FEEDBK 92; the first repeat is 10 dB under the note) and does not follow the tempo. Drive is GROWL 48. About
    1967 host instr/sample worst case. Tricks untested.
- **21 Cowl Shadow — VOICED (Nov 2026, approved as is; variant C of Batch 2A).** A brass wall that blooms.
  - *What it sounds like:* A brass wall that starts dark and soft and swells open while you hold the note: a
    quiet murky hum that, in a few seconds, blooms into a wide, full, glowing brass, with a slow drift inside
    the stack. Dry. When you let go it fades out slowly and darkens as it goes.
  - *How to play it:* **Hold the note.** The bloom takes about five seconds (a tenth open at under a second,
    nine-tenths at about four, measured on A2). A sustain pedal or REC (HOLD) should hold it open the same way
    (not tried on this patch). **Release early and it never opens** — let go at 2.4 s and it is
    still dark and just fades in about two seconds; after a long hold the release takes about a second to
    drop 20 dB and about four to vanish. Legato doesn't restart the bloom; release and play a new note.
    **It sounds quiet if you tap a note:** short stabs read about 13 dB under the bloomed level. One note at
    a time (five-voice unison). Measured only on A2. Tricks untested; a little DRAIN would add depth
    (untested).
- **22 Melting Orb — VOICED (Nov 2026, approved; variant D of Batch 5A).** A dignified collapse.
  - *What it sounds like:* A thick stack of detuned saw tones that opens bright when the key goes down and then
    slowly sinks: the filter closes and the pitch falls together over a few seconds until the sound settles low
    and dark. A held collapse, not a zap. Takes chords (three keys gate six voices). Dry.
  - *How to play it:* **Hold the key;** the melt happens while it is down (the pitch ends about 6.8 semitones
    lower, 90% of the fall at 4.0 s on A2). A short tap hears only the bright opening. **On key-up the melt
    partly runs backwards:** pitch and brightness climb back through the fade (not tested whether it is
    audible). OSC 1 is off, because ENV>O2 bends OSC 2 only. A three-key chord peaks at −4.1 dBFS. About 2489 host
    instr/sample worst case, the highest of any voiced patch on the host yardstick. Tricks untested.
- **23 Crypt Dust — VOICED (Nov 2026, approved; variant D3 of Batch 5B round 2).** Frail, crumbling
  atmosphere. *(Brief changed after listening; it was: noise + thin pulse, heavy tape wow, no drive. The final
  patch has no tape and only a trace of noise.)*
  - *What it sounds like:* A thin, narrow pulse run through a band-pass into a pale, dusty tone, with only a
    trace of noise under it. The level flutters slowly and irregularly, in steps. A short echo and a large
    spring blur it. It rises slowly when you press a chord and hangs on after you let go.
  - *How to play it:* A held-chord pad (POLY 4: all three keys of a triad sound); short notes are faint (a
    150 ms chord tap is 13.7 dB under the held chord). The noise sits 24.4 dB under the pulse. The chord peaks at
    −4.0 dBFS, which limits VOLUME. About 2065 host instr/sample worst case. Tricks untested.
- **24 Fugue State — VOICED (Nov 2026, approved; variant C of Batch 5B).** A dizzying pad.
  - *What it sounds like:* A soft, dark, triangle-like pad whose pitch trembles quickly, wide in the stereo
    field. Each chord runs into a short echo that feeds back on itself while the pitch is still moving, so the
    repeats sit at slightly different pitches from the notes being played and the chord smears. A spring adds a
    further tail. No filter movement, only the pitch and the echo.
  - *How to play it:* A held-chord pad (POLY 5). A triangle LFO at 4.9 Hz moves the pitch by ±178 cents; the echo
    is 144 ms at FEEDBK 95 (10 repeats above −40 dB). The tail is 20 / 40 / 60 dB down at 1.6 / 3.5 / 4.6 s.
    Runaway tests show no clipping. One shared LFO, so no true rotary. The kill switch clears the echo buffers
    (not tested here). About 2038 host instr/sample worst case. Tricks untested.

### CHAPTER IV — ACID CAN
*Prophet-5 survivors, rebuilt by ear — never ripped from factory data. On screen: the Acid Can scene (a
tipped-over can oozing acid in an alley), accent Acid Chartreuse. All eight patches (25–32) are voiced.*

- **25 SAWTOOTH — VOICED (4–5 Nov 2026, approved as is).** The iconic poly-brass, a Prophet-5 survivor rebuilt
  by ear.
  - *What it sounds like:* Two saws a few cents apart, stable and warm, with the filter swelling open on each
    note and settling into a solid, brassy body. It holds still: no wobble, no chop, only a gentle vibrato
    that fades in if you hold a note.
  - *How to play it:* Low-mid to mid register; chords and fifth-and-octave voicings are home ground (each
    note is one voice; three- and four-note chords should play in full — not yet chord-tested). Medium to long
    notes show the swell best: it peaks about 84 ms in, so a very short stab catches only the start. It is
    the stable counterpart to 03 Half-Life. The vibrato arrives after about 1.1 s on held notes; LFO PITCH to
    0 removes it. Ride the ALGORITHM for a tired-string-brass wobble; Tape Stop as a swell-out ending (both
    untested on this patch). All effects are at 0 on purpose: a dry brass, with a spring or echo yours to add.
- **26 BSyncA — VOICED (11 Nov 2026, approved after listening; variant D of Batch 6A).** A ripping sync solo.
  - *What it sounds like:* A hard-sync lead built from three slightly detuned voices that beat slowly against
    each other, with a master oscillator you can hear underneath the synced one. Every detached note starts
    with a bright sweep that tears down into a duller body; it is pushed into drive and left dry, with a short
    glide between notes. Played legato, the sweep does not come back.
  - *How to play it:* **UNISON, one note at a time:** three voices all play the key you press and a chord plays
    the last key only. The sweep fires on **detached** notes: on notes 2–8 of the riff, the centroid over the
    first 100 ms is 2935 Hz detached against 1742 Hz legato. The sweep was measured on A3; the riff runs A3 to
    C6 and nothing else was measured. **The drive darkens the strike:** GROWL 44 lowers the crest factor from
    11.7 to 6.0 dB, and the centroid over the first 50 ms is 2662 Hz against 4165 Hz with no drive, so the
    brightness of the rip trades against the drive. GLIDE 50 takes 64 ms to come within 50 cents of a legato
    octave step. Dry: no echo, no spring, no tape. VOLUME 90, −18.05 dBFS RMS on the lead phrase, peak
    −11.0 dBFS. About 2326 host instr/sample worst case (GROWL about +595 of it). Tricks untested. *The original
    brief had a silent master oscillator, one MONO voice, no drive and an echo with a spring; the brief is kept in
    the presets doc.*
- **27 R3V3RT — VOICED (11 Nov 2026, approved after listening; variant G, a calibration render of C with a
  longer filter decay, chosen by ear).** Tight, immediate analog bass.
  - *What it sounds like:* A single-voice bass from one pulse wave. Each note opens with a bright filter snap
    that falls into a lower body; the body holds at a steady level for as long as the key is down, and when the
    key goes up the note stops almost at once. Played legato, the snap is not re-fired and the notes after the
    first have no front edge. Dry.
  - *How to play it:* **MONO, one note at a time.** The snap fires on **detached** notes: on notes 2–8 of the
    eight-note line the first 20 ms centroid is 2200 Hz detached against 154 Hz legato. On A2 held 1 s the
    level is 2.0 dB under the peak at 100 ms and 3.4 dB under at 300 ms; after key-up it is down 20 / 40 / 60 dB
    in 11 / 15 / 19 ms. **Low register:** A1's fundamental is 55 Hz, and only 17% of A1's body energy is above
    60 Hz (99% on A2), so a low A1 is mostly inaudible on a small speaker. VOLUME 98, −18.00 dBFS RMS on the low
    riff, peak −13.8 dBFS. About 1379 host instr/sample worst case, not lighter than the original (1377).
    Tricks untested. *The original had a saw plus a sub-octave pulse; the sustained single-pulse body is what
    Vincent asked for.*
- **28 Arr 2 Dee 2 — VOICED (11–12 Nov 2026, approved after listening; variant D2 of Batch 6B round 2).**
  *Renamed from "Bell Tolls" at Vincent's request; he asked for "Arr Two Dee Two", which is 15 characters
  against the 14-character name field, so the on-screen name is "Arr 2 Dee 2". The brief changed after
  listening: the original was an inharmonic FM chime set against the hard-chop gate; Vincent asked for a bell
  ring with body, healthy decay and sustain, a clean base to shape live, and no top grit.*
  - *What it sounds like:* A sustained, struck bell tone built from two saw waves with a mid-frequency
    sideband character. It rings for several seconds, a slow shimmer moves its pitch and level, and a small
    echo and a spring sit behind it. It is dry of drive and tape.
  - *How to play it:* **The key you press is the bell's hum, the strongest partial; the prime is an octave
    above it**, so the strike may feel an octave above the key (not measured as perceived pitch). The five
    classical bell partials (hum 0.5, prime 1, tierce 1.2, quint 1.5, nominal 2) are all present; at A4 in the
    first 300 ms they read 0 / −7.7 / −11.1 / −10.5 / −13.6 dB. **It rings on after key-up:** a note released at
    400 ms falls 20 dB in 3012 ms and 40 dB in 5610 ms. The ring of a held note to −40 dB is about 5.8–6.0 s
    across A2–A6, and the level is within 1.2 dB across the keybed; **A6 is bright** (21.3% of its first-20 ms
    energy above 4 kHz). POLY 5; a three-note chord reads −21.0 dBFS RMS, peak −6.0. A fast eight-note run
    peaks at −4.03 dBFS and sets the level limit. **Live shaping** (it sits mid-range on CUTOFF 88, X-MOD 32,
    ENV>O2 64, OSC 2 FINE 64, echo MIX 45, DRAIN 35, CHEW 0): CUTOFF and X-MOD change the brightness without
    moving the partials; echo MIX, DRAIN and FINE barely move the ring; **ENV>O2 ±10 breaks the bell**, because
    the tierce falls from −10 dB to about −47 dB at either side. The top grit of the first version was the FM,
    not CHEW or GROWL (neither is in the patch). **Not carried: a crystalline tail** (the engine has no
    per-partial envelope). About 2118 host instr/sample worst case; **riding CHEW 45 or GROWL 44 on top reads
    2901 or 2713, and both 3496, on the host yardstick.** On the FM-1 (12 Nov), with all four Psych Chain
    effects pushed hard, four notes held read about 4500 µs against the 5800 µs budget in the source
    (Vincent's reading, ±100). Tricks untested.
- **29 i scream — VOICED (11 Nov 2026, approved: variant D with CHEW 0).** *Built by ear from Vincent's field
  recordings of a real South African ice-cream van; nothing is sampled. The exact version was not heard
  before approval (Vincent heard D with tape and approved it without).*
  - *What it sounds like:* A bright, struck chime built from a square wave with a second oscillator that
    zings down in pitch at the strike. The ring decays slowly, over a couple of seconds, and a gentle slow
    shimmer in pitch and level fades in after the strike and sways the ring. A small slap echo and a touch of
    spring sit behind it, and everything passes through a narrow, honky mid-band like a small horn speaker.
    There is no tape in it. *Vincent hears it as closer to an arcade or vintage video-game chime than to finger
    cymbals (his ear, not measured); the bank had nothing in that register before.*
  - *How to play it:* Voiced for A4 to A6; nothing outside was measured. The ring of a C#6 falls 6 / 12 / 20 /
    40 dB in 252 / 550 / 1030 / 1896 ms, so with notes 580 ms apart several rings overlap (POLY 5). **A
    three-note chord (A#5 C#6 F6) plays whole and is the loudest phrase** (−21.3 dB RMS, peak −4.06 dBFS): use
    it as a wind-chime. The shimmer is a TRI LFO at 0.8 Hz (the engine has no sine). The filter is a band-pass
    peaking at 1099 Hz. No tape: CHEW is 0, so no wow, flutter, hiss or dropout. VOLUME 113, −17.9 dBFS RMS on
    the chime melody. About 1863 host instr/sample worst case. On the FM-1 (12 Nov), with all four Psych Chain
    effects pushed hard, four notes held read about 4500 µs against the 5800 µs budget (Vincent's reading,
    ±100). Tricks untested.
- **30 THE DØG — VOICED (4–5 Nov 2026, approved; variant H of round 2).** **The signature patch, and the
  flagship.**
  - *What it sounds like:* A dry, punchy unison bass: every voice stacked on one note, fat and thick, loosened
    just enough that the stack breathes without ever going seasick. Warm, with a driven edge that stops short
    of fuzz, and each note is chopped hard on release: no spring, no echo, no tail, only the silence after
    the hit. It has presence: it sits forward and fills the room.
  - *How to play it:* Low register. Roots and octaves from about A1 to A2 are the sweet spot, for single-note
    bass lines and chopped roots; the very bottom (A0 and the low end of A1) is partly below what small
    speakers and many PAs reproduce, so on a laptop you hear the body, not the floor. Staccato to medium —
    eighth-note chops (roughly 130 ms) are home — and it also holds as a wall of low unison with a slow,
    controlled beat. It is a unison: one note at a time, no chords. Tricks: ALGORITHM loosens the stack
    further; Tape Stop dives the whole low stack; the kill switch stops it dead; per-voice DRIVE (MIXER
    page, knob 4) is the gentle route to more grit, while GROWL is a big step (nothing below about 28, compressing
    past about 40). Effects are at 0 on purpose (dry and punchy is the sound; a wash will blur the chop). It
    deliberately sits about 1.5 dB above the bank's usual level for presence — expect it to jump out a little
    when you switch to it. **On the FM-1 (12 Nov), with all four Psych Chain effects pushed hard, four notes held
    read about 5600 µs against the 5800 µs budget in the source (Vincent's reading, ±100): the highest of the
    six patches he read, so it is the one to watch when riding the effects hard.**
- **31 Fi(l)fth — VOICED (4–5 Nov 2026, approved as is; variant C, the DUAL stab).** The archetypal aggressive
  chord stab. Directly the top-voted DØG-5 sound.
  - *What it sounds like:* A fifth built into every note, a hard filter pluck, and a short slap-back echo right
    behind it. Each note is a detuned pair, so it is fat and punchy rather than thin, warm rather than icy,
    with a bright snap on the front that settles into a solid body. Dry apart from the slap: no spring, no long
    wash, just the stab and its quick echo.
  - *How to play it:* Low to low-mid register; single notes and fifth-based riffs (roots and octaves around A1
    to A2) are home ground — every note already carries its own fifth, so one finger plays a power chord.
    Short and hard: a stab of roughly 150–200 ms (there is no gate-length control; the stab is as long as you
    hold the key). Chords, honestly: because the fifth is built into every voice, chords of fifths stack
    fifths on fifths into sus2-style clusters — the engine doing what the patch asks. Every note is two
    voices, so chords are three notes by design (three notes use six voices; a fourth still fits, using all
    eight; a fifth steals). It is heavier on CPU than a single-voice stab. The slap (ALLEY) is on and is what
    makes it the Space-Echo stab; turn ALLEY up on the BBD DELAY page for a longer echo. Other tricks untested
    on this patch; a spring will blur the stab.
- **32 Init bruv? — VOICED (11 Nov 2026, approved after listening; variant B).** The blank slate that closes
  the bank.
  - *What it sounds like:* A plain voice made of two saw waves played through a low-pass filter with a short
    envelope, dry, with chords and single notes both playable. Nothing is added to it: no modulation, no echo,
    no spring, no tape and no drive.
  - *How to play it:* **It is the engine's own default program with one change, VOLUME 97** (the default is
    100). It is not a single raw saw with an open filter: POLY 5, two saws 4.7 cents apart, a 24 dB low-pass at
    CUTOFF 80 with RESO 20, a filter envelope and an amp envelope, VINTAGE 30, SPREAD 60, every effect at 0.
    **Slots 33–99 hold the same defaults as INIT, with VOLUME 100.** Chords play (POLY 5); −18.05 dBFS RMS on the
    stabs phrase, peak −5.6 dBFS. With GROWL, DLY MIX, DRAIN and CHEW at 0 the audio was bit-identical when
    every other effect control was moved to its extreme. About 1814 host instr/sample worst case. *A raw
    single-saw render ("Craw") and a MONO init stay on the listening branch as v1.1 candidates for more blank
    canvases.*

---

## PART 4 — GEAR INSPIRATIONS

For each voiced patch: real-world instruments and pedals whose *character* it draws on, each tagged with the
dictionary trait it carries — so "a bit more Mono/Poly" translates straight into parameter moves. These are
inspirations, not imitations: nothing here is modelled, ripped or sampled, and gear names appear only in this
manual — never in patch names or on-screen text. All trademarks belong to their owners; DØG-5 is not affiliated
with or endorsed by any of them. *A tag is kept only where the final patch carries the trait; traits the patch
lacks are named as such.*

Each entry ends with a **Closest to** line: the one instrument you would name if someone asked "what does it
sound like?"

### Chapter I — JALOPY

**01 Red Pill**
- **Korg MS-20** — the resonant filter and its bite. *Nasty, biting, resonant.*
- **Minimoog** — the stacked saws. *Fat, thick.*
- **Roland SH-101** — the tight snap at the front of a note. *Tight, punchy.*
- **ProCo RAT** — the driven edge. *Gritty, crunchy.*
- *Closest to:* an MS-20 bass through a RAT.

**02 Cement Grind**
- **Roland Juno-60** — the pulse-width movement. *PWM, wobble, thick.*
- **Korg Polysix** — the stacked pulses. *Fat, PWM.*
- **Roland SH-101** — the punchy PWM bass. *PWM bass, punchy.*
- **ProCo RAT** — the crunch. *Crunchy.*
- **Korg MS-20** — the filter. *Biting.*
- *Closest to:* a Juno-60 PWM bass through a RAT.

**03 Half-Life**
- **Korg Mono/Poly** — detuned oscillators that drift and never settle. *Fat, slop, seasick, thick.*
- **Sequential Prophet-5 (early, tuning-unstable revisions)** — dual-saw warmth with the drift. *Fat, warm, drift.*
- **Minimoog** — the body under the instability. *Fat, sub-heavy, thick.*
- **Korg MS-20** — the bite and the spit in the filter and the tail. *Nasty, biting, spitting.*
- *Closest to:* Korg Mono/Poly — its drifting, detuned saw chaos, with Minimoog weight underneath, chopped by
  the gate.

**04 V-Sync**
- **Sequential Pro-One** — the sync sweep itself. *Sync, punchy, ripping.*
- **Sequential Prophet-5** — the fatness of a doubled voice. *Sync, fat.*
- **ARP Odyssey** — the nasal, cutting tone. *Nasal, biting.*
- **Moog Prodigy** — the cheap, raw edge. *Fat, cheap, raw.*
- *Closest to:* a Pro-One sync lead.

**05 ZEAROX**
- **Roland TR-808 kick** — the thump. *Sub, thump.*
- **Roland SH-101** — the weight. *Sub, thick.*
- **Tascam Portastudio cassette 4-track** — lo-fi squash. *Lo-fi, noisy.*
- **ProCo RAT** — the overload. *Crunchy, driven.*
- *Closest to:* an 808 kick smashed onto a blown-out cassette 4-track. *(Honest note: the tape and the drive
  stage are not in the final patch — they were removed in round 2 at the owner's direction; what remains is the
  hard, two-level square.)*

**06 zzuFuzz**
- **Death by Audio Fuzz War** — **the benchmark**, a huge fuzz beast. *Fuzzy, thick wall.*
- **Electro-Harmonix Big Muff** — the wall. *Fuzzy, thick wall.*
- **Fuzz Face** — the fuzz. *Fuzzy, spitting.*
- **Univox Super-Fuzz** — *voltage-starved, spitting.*
- **Korg Mono/Poly** — as the source. *Fat, drifting.*
- **Realistic Concertmate MG-1** — *voltage-starved, lo-fi.*
- *Closest to:* a Mono/Poly into a Big Muff. *(Built toward the descriptions by measurement and approved by
  ear; nothing says it matches the benchmark, and the voltage-starved gating of the Super-Fuzz and MG-1 is not
  claimed.)*

**07 Tape Splice**
- **Korg Mono/Poly** — the cross-modulated fat square. *Fat, drifting.*
- **Sequential Prophet-5** — the nervous pitch wobble. *Wobble, nervous.*
- **Roland RE-201 Space Echo** — the worn tape stage. *Wobble, lo-fi.*
- **Roland SH-101** — the clipped, punchy gate. *Punchy.*
- *Closest to:* a Mono/Poly cross-mod square through a worn tape echo.

**08 Wire Bite**
- **Korg Mono/Poly (in unison)** — the stack. *Fat, drifting.*
- **Minimoog** — *thick.*
- **Korg MS-20** — the bite. *The bite.*
- **Roland Jupiter-4** — *fat, wobble.*
- **Sequential Prophet-5 (early revisions)** — the unsteadiness. *Drift.*
- *Closest to:* a Mono/Poly in unison with MS-20 bite.

### Chapter II — BEE-TCH

**09 Skeenhead**
- **Korg MS-20** — the resonant filter plop. *Plucky, biting.*
- **Roland SH-101** — the tight, quick stab. *Tight, punchy.*
- **Moog Prodigy** — the single raw square. *Fat, cheap, raw.*
- **Fender spring reverb tank (Twin Reverb style)** — the drench. *Springy, boingy.*
- **Roland RE-201 Space Echo** — the dub-style tail. *Warm.*
- *Closest to:* an MS-20 plop into a Fender spring tank.

**10 Atlantic Swell** *(as the final patch: a pulse pair into a spring; no chorus, rotary or echo)*
- **Farfisa Compact** — *nasal* (the approved trait; not measured on this patch).
- **Vox Continental** — *reedy, bright* (bright is measured: note-on centroid 5369 Hz, 23% of the energy
  above 1.2 kHz; reedy is not).
- **Fender spring reverb** — *springy* (measured return in Part 3).
- *Closest to:* a combo organ into a spring tank.
- *Not in this patch (they belong to the chorus, rotary and echo versions B, C, D rendered in Batch 4A):*
  Leslie rotary speaker, TC Electronic June-60 chorus, Roland RE-201 Space Echo.

**11 Slapback Strut**
- **Fender Precision Bass (flatwounds)** — the plucky, snappy attack. *Plucky, snappy.*
- **Roland SH-101** — the tight, quick note. *Tight, punchy.*
- **Minimoog** — the round, percussive low end. *Round, percussive.*
- **Binson Echorec / Roland RE-201** — the single slap. *Slap, warm.*
- **Fender spring reverb** — the surf wash. *Surf wash.*
- *Closest to:* a flatwound P-Bass into a Space Echo.

**12 Kelp Tangle**
- **Moog Prodigy** — *dark* (measured: held A2 centroid 531 Hz; "raw" and "murky" are not measured as such).
- **Fender spring reverb tank** — the tail. *Springy.*
- **Roland Juno-60** — the pulse-width sweep. *PWM* (measured; there is no pitch wobble; "thick" is not
  measured).
- **Korg Polysix** — *PWM* (measured; "fat" is not measured).
- *Closest to:* a Polysix PWM pad into a spring tank.

**13 Ghost Board** *(as the final patch: a dark, slowly beating pulse pair, long echo, heavy spring; no tape)*
- **Roland RE-201 Space Echo** — the echo. *Wet* (337 ms, FEEDBK 95, MIX 105; first repeat −8.7 dB re the
  note, 10.3 dB above the spring).
- **Fender spring reverb tank** — *springy* (DRAIN 70; louder than the chord for its first 250 ms or so).
- **Mellotron M400** — the reference for the tone that was being chased. Measured traits only: *dark* (centroid
  562 Hz, muddiness ratio 315) and *a slow beating between the two oscillators* (13.6 dB at 0.9 Hz on one
  voice). **"Warped, wobbly tape" and "soft flute-like tone" are not in this patch** (the tape deck is off;
  harmonics 3 / 5 / 7 read −11 / −18 / −26 dB against a triangle's −19 / −28 / −34).
- *Closest to:* a dark Mellotron voice through a Space Echo and a spring tank.

**14 Reef Break** *(v0.2: the 299 ms attack)*
- **Roland TR-808** — *thick sub* (with the 299 ms attack the sub's 40–150 Hz band peaks 255 ms after the note-on
  and falls 20 / 40 dB in 58 / 70 ms after that peak; the 6 Nov version's shares are in the voice card; "booming"
  is not measured).
- **Simmons SDS-V** — *noise burst* (the noise is 15.6 dB over the sub in the first 100 ms on A1, a window that
  now sits inside the attack; attack 10 / 50 / 90% at 25.2 / 126.2 / 208.0 ms; "crashing" is supported only by
  the band decay).
- **Roland RE-201 Space Echo** — *long repeats* (361 ms, FEEDBK 100, MIX 80; 8 repeats above −40 dB; not a
  runaway).
- *Closest to:* an 808 kick with a noise burst into a Space Echo.

**15 Trem Chop**
- **Roland SH-101** — the bright saw. *Bright, punchy.*
- **Boss TR-2 Tremolo (square setting)** — the hard chop. *Choppy, gated.*
- **Electro-Harmonix Pulsar** — the pulsing tremolo. *Choppy, rhythmic.*
- **Korg Polysix** — a little instability behind the chop. *Drift.*
- *Closest to:* an SH-101 saw through a Boss TR-2 on square.

**16 Tidal Pull**
- **Roland Juno-60** — a wash of pulses (the L/R correlation is 0.70 dry, 0.66 with echo and spring; "fat" is
  not supported). *Wash.*
- **Fender Twin Reverb** — the spring. *Springy* (the centroid is 595 Hz, so "bright" is not supported).
- **Roland RE-201 Space Echo** — the echo. *Wet* (first repeat −8.6 dB re the note, 7.7 dB above the spring;
  "drenched" is not measured).
- *Closest to:* a Juno-60 chord pad through a Twin Reverb spring and a Space Echo.

### Chapter III — MOONSHINE

**17 Titanic**
- **Yamaha CS-80** — cold, epic, slow weight. *Fat, sub-heavy, desolate.*
- **Moog Taurus** — the floor under everything. *Deep, floor-shaking.*
- **Memorymoog** — the thick, dark body. *Thick, dark.*
- **Sequential Prophet-5** — two saws a fifth apart. *Fat, warm.*
- *Closest to:* a CS-80 played low and cold.

**18 Roto-scopo**
- **Korg MS-20** — *resonant, unruly low-passed square* (resonant is measured: a 12 dB low-pass at RESO 115 that
  is still linear; unruly is not measured).
- **ARP 2600 sample-and-hold** — *wandering cutoff* (the cutoff wanders, measured; this variant uses the smooth
  RANDOM shape, not sample-and-hold).
- **Moog Taurus I** — *dungeon-low weight* (on A1, 62% of the energy under 60 Hz and 17% in 60–150 Hz, measured).
- *Closest to:* a Taurus-weight square through an MS-20 filter that a random source keeps nudging.

**19 Micro-mist**
- **Hologram Microcosm** — *the Haze, Glide and Tunnel of its Granules and Micro Loop banks; Wash, Wet.* Wash:
  the L/R correlation falls from 0.79 dry to 0.43 with echo and spring (measured). Wet: the tail takes 5788 ms to
  fall 60 dB (measured). Drifting: not measured. Not a granular looper.
- **Yamaha CS-80** — *the Blade Runner pad voice; Soft, Swelling.* A 150 ms tap is 8.7 dB under the held chord
  (measured); the chord rises 2.2 dB over its first two seconds.
- **Roland Jupiter-8** — *the bright top; Bright, Beating.* Settled centroid 2300 Hz, 39% above 1.2 kHz
  (measured); the beating is weak (0.4 dB).
- *Closest to:* a CS-80 pad dissolved in a Microcosm Haze wash.

**20 Fire & Ice**
- **Sequential Pro-One** — *the hard-sync lead; Rip, Bright.* Centroid on a detached A4 falls 2793 → 1272 Hz over
  800 ms (measured).
- **Ibanez Tube Screamer** — *the soaring drive; Driven.* GROWL 48 lowers the crest factor by 3.3 dB at the same
  level (measured). No claim about the pedal's curve.
- **Roland RE-201 Space Echo** — *the drench; Wet.* First repeat 10.0 dB under the note, 8 repeats above −40 dB
  (measured).
- *Closest to:* a Pro-One sync lead through an overdrive pedal into a Space Echo.

**21 Cowl Shadow**
- **Yamaha CS-80** — the slow brass swell. *Soft, slow, swelling.*
- **Oberheim OB-Xa** — the brassy body. *Brassy, full.*
- **Roland Jupiter-8** — the bright blare at the top of a swell. *Bright blare.*
- **Korg Mono/Poly (in unison)** — the stacked, drifting oscillators. *Fat, drifting.*
- *Closest to:* a CS-80 brass swell, stretched.

**22 Melting Orb**
- **Oberheim OB-Xa** — *a fat unison source* (a DUAL pair of saws per key, 9.8 cents apart; "fat" is not
  measured).
- **Sequential Prophet-5** — *the slow filter-envelope sweep* (centroid falls 1323 → 204 Hz, 90% of the fall at
  3.5 s, measured).
- **Korg MS-20** — *resonance, high but musical* (RESO 75 on a 12 dB low-pass, linear by the probe; "musical" is
  not measured).
- *Closest to:* an OB-Xa-style fat stack whose filter and pitch both sink slowly downward.

**23 Crypt Dust** *(as the final patch: a trace of dust, no tape)*
- **Korg MS-20** — *noise plus a thin pulse; Thin.* The pulse is 12% wide and the noise sits 24.4 dB under it
  (measured); "gritty" is not measured.
- **Roland RE-201 Space Echo** — *the worn echo.* 75 ms, first repeat 9.6 dB under the note, 6 repeats above −40
  dB (measured). The tape wobble of the worn unit is **not in this patch**.
- **Mellotron M400** — the dusty, pale tone as the reference (centroid 1970 Hz, measured); the warped tape is
  **not in this patch**.
- *Closest to:* a thin pulse and a trace of dust through a band-pass, into a short echo and a large spring.

**24 Fugue State**
- **Electro-Harmonix Deluxe Memory Man** — *BBD feedback with pitch modulation; Wet.* 10 repeats above −40 dB,
  return to −40 dB in 1721 ms (measured). There is no pitch modulation inside the echo; the largest gap between a
  note and its own repeat is 212 cents (computed). "Seasick" is not measured: at 4.9 Hz it is a wobble.
- **Roland RE-201 Space Echo** — *echo feedback; Wash.* The tail takes 4624 ms to fall 60 dB (measured). This
  patch does not self-oscillate (FEEDBK 95).
- **Korg Polysix** — *the ensemble-chorus dizziness; Wobble.* A triangle pitch LFO at 4.9 Hz, ±178 cents
  (measured). Beating is not measured; there is no chorus in the patch.
- *Closest to:* a soft triangle-like pad run through a Memory Man until it seasicks itself.

### Chapter IV — ACID CAN

**25 SAWTOOTH**
- **Sequential Prophet-5** — the swell and the two-saw body. *Fat, warm, swell.*
- **Oberheim OB-Xa** — the brass-section feel. *Brassy, full.*
- **Roland Jupiter-8** — the bright blare at the top of the swell. *Bright brass.*
- **Memorymoog** — the weight of the chord. *Thick, warm.*
- **Korg Polysix** — the slow vibrato wobble on a held note. *Fat, wobble.*
- *Closest to:* a Prophet-5 brass swell.

**26 BSyncA**
- **Sequential Prophet-5** — *the classic sync solo; Sync, Ripping, Fat.* Sync: OSC 2 is hard-synced to OSC 1 (a
  setting). Ripping: on notes 2–8 of the detached riff the centroid over the first 100 ms is 2935 Hz, 303 Hz above
  the same riff with the sweep off (measured). Fat: not measured, except that the three voices beat at 0.99 Hz
  with a 16.9 dB swing in the 220 Hz band on a held A3.
- **Sequential Pro-One** — *the sweep itself; Rip, Bright.* The sweep is ENV>O2 104, +15.2 semitones at the
  envelope's top (computed). On a detached A3 the centroid runs 2662 / 1724 / 1111 Hz over 0–50 / 50–150 /
  150–400 ms (measured). No comparison with the Pro-One was made.
- **Moog Prodigy** — *the raw edge; Raw, Biting.* Not measured. The patch carries a drive (GROWL 44), which is
  not the same thing.
- **ARP Odyssey** — *the nasal cut; Nasal, Biting.* Not measured.
- *Closest to:* a Prophet-5 sync lead pushed into crunch. ("Crunch" is Vincent's word; the measured fact is the
  crest factor, 6.0 dB with GROWL 44 against 11.7 dB without drive.)

**27 R3V3RT**
- **Roland SH-101** — *the tight, quick note; Tight, Punchy.* Key-up to −20 / −40 / −60 dB is 11 / 15 / 19 ms on
  A2 (measured; the 9 ms meter window is the floor of these readings). Punchy: not measured.
- **Minimoog** — *the round immediate low end; Round, Thick.* Not measured. The band shares are measured: on A2
  the first 400 ms are 1 / 82 / 9 / 6 / 1 % in <60 / 60–150 / 150–400 / 400–1.2k / 1.2k+ Hz.
- **Moog Prodigy** — *the plain pulse; Raw, Fat.* A single pulse (OSC 1 PW 54, OSC 2 off); "raw" and "fat" are
  not measured.
- **Sequential Pro-One** — *the snap of the filter decay; Snappy.* On A2 the filter snap peaks at a centroid of
  2891 Hz and lasts 175 ms; the centroid reads 2828 / 1759 / 440 Hz over 0–20 / 20–100 / 100–300 ms (measured).
  No comparison with the Pro-One was made.
- *Closest to:* an SH-101 pulse bass with a Minimoog body.

**28 Arr 2 Dee 2**
- **Yamaha DX7 (tubular-bells voice)** — *FM clang, inharmonic.* Partly carried: OSC 2 sits +15 semitones above
  OSC 1 (a ratio of 2.38) and feeds OSC 1 by X-MOD 32. At A4 in the first 300 ms that partial reads 1.197 × the
  prime at −11.1 dB. Not carried: DX7-style operators (this is one saw modulating another). "Clang" is not
  measured.
- **Roland D-50 ("Fantasia")** — *crystalline.* **Not carried.** The engine has no per-partial envelope, so no
  partial outlasts the body. At A4 the share of energy above 4 kHz is 4.0% in the first 20 ms and 0.4% at 1–2 s.
- **Casio CZ-101 (phase-distortion bells)** — *a bright, bell-like phase-distortion tone.* Not carried: the
  engine has no phase distortion; the sideband character here comes from X-MOD. Whether it resembles those bells
  is not measured.
- **A struck tubular or church bell** — *the classical partials.* Carried, measured: the five classical
  partials of the ladder (hum 0.5, prime 1, tierce 1.2, quint 1.5, nominal 2) are all present, with the
  amplitudes in Part 3. "Church bell" is Vincent's word and is not measured.
- *Closest to:* a DX7 tubular bell with a long, slowly moving tail.

**29 i scream**
- **Yamaha DX7 (tubular-bells voice)** — *FM clang, inharmonic.* OSC 2 sits +15 semitones above OSC 1 (a ratio of
  2.38) with X-MOD 25. Through the filter that partial reads −34 dB under the note at C#6 and −18 dB at C#5
  (measured, first 100 ms), so it is faint at the top of the keybed. "Clang" is not measured.
- **A music box, struck** — *fast-decay, nostalgic.* Not carried: the ring takes 1896 ms to fall 40 dB at C#6
  (measured), a long ring. "Nostalgic" is Vincent's word and is not measured.
- **Finger cymbals (zills)** — *bright metallic ping.* The centroid over the first 20 ms is 2096 Hz at C#6 and
  1958 Hz at C#5 (measured). "Metallic" is not measured.
- **A transistor radio or van horn speaker** — *band-limited, honky, lo-fi.* The filter read with white noise
  peaks at 1099 Hz, with a −3 dB width of 898–1345 Hz; 0.4% of its energy is under 400 Hz and 4.1% above 4 kHz
  (measured). "Lo-fi" is not measured.
- *Closest to:* a music-box chime played through a cheap van horn speaker. *Provenance: built by ear from
  Vincent's field recordings of a real ice-cream van; the measurements of the recordings were rough; nothing is
  sampled. Vincent's ear (not measured): closer to an arcade or vintage video-game chime.*

**30 THE DØG**
- **Minimoog in unison** — the stacked saws and the octave-down body. *Fat, sub-heavy, thick.*
- **Moog Taurus bass pedals** — the weight at the bottom. *Deep, floor-shaking.*
- **Roland SH-101** — the quick attack and the hard stop. *Tight, punchy.*
- **Oberheim OB-Xa in unison** — the wide, full stack with its warmth. *Fat, full, warm.*
- **Korg MS-20** — the grit in the filter when it is pushed. *Nasty, biting.*
- *Closest to:* a Minimoog in unison with Taurus weight.

**31 Fi(l)fth**
- **Sequential Prophet-5** — the stab itself, with weight behind it. *Punchy, fat, warm.*
- **Roland Juno-60** — the short, snappy pluck. *Plucky, punchy.*
- **Roland Jupiter-8** — the open top on the attack. *Bright, full.*
- **Korg MS-20** — the bite when you dig in. *Biting.*
- **Roland RE-201 Space Echo** — for the short delay. *Slap, warm.*
- *Closest to:* a Prophet-5 stab through a Space Echo.

**32 Init bruv?**
- **Sequential Prophet-5** — *a plain saw, the filter open.* Not carried: the filter is a 24 dB low-pass at
  CUTOFF 80 with RESO 20, and there are two saws, not one.
- **Minimoog** — *one raw oscillator.* Not carried: OSC 2 is on (a saw, 4.7 cents from OSC 1).
- **Roland SH-101** — *a saw, the filter open.* Not carried, for the same two reasons.
- What was measured: through the filter, the 2nd / 3rd / 4th harmonics of C3 are −7.9 / −14.3 / −18.0 dB (a
  plain saw is −6.0 / −9.5 / −12.0). So it is two detuned saws through a closed-ish filter, not a plain saw.
- *Closest to:* an analog two-saw init patch. ("Raw" and "blank" are Vincent's words and are not measured.)

*(Gear inspirations are complete for all 32 patches. Nothing here says a patch matches any instrument listed.)*

---
