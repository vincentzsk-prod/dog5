# 26 · BSyncA · Chapter IV · The Ancient Relics

*Voiced 11 Nov 2026 (Batch 6A), approved after listening: variant D (Vincent: "26 D"). Renders: `reference-renders/26-bsynca_D_*.wav`. Tables (on the voicing branch): `listen/voicing/batch-06a/26-bsynca/README.md`.*

## 2. What it sounds like

A hard-sync lead built from three slightly detuned voices that beat slowly against each other, with a master oscillator you can hear underneath the synced one. Every detached note starts with a bright sweep that tears down into a duller body; the whole thing is pushed into drive and left dry, with a short glide between notes. Played legato, the sweep does not come back.

## 3. Gear inspirations (docs only, "inspired by")

- **Sequential Prophet-5** — *the classic sync solo; Sync, Ripping, Fat.* Sync: OSC 2 is hard-synced to OSC 1 (a setting). Ripping: on notes 2–8 of the detached riff the centroid over the first 100 ms is 2935 Hz, 303 Hz above the same riff with the sweep off (measured). Fat: not measured, except that the three voices beat at 0.99 Hz with a 16.9 dB swing in the 220 Hz band on a held A3 (the same stack without GROWL: 1.04 Hz, 17.2 dB).
- **Sequential Pro-One** — *the sweep itself; Rip, Bright.* The sweep is ENV>O2 104, +15.2 semitones at the envelope's top (computed from the setting). On a detached A3 the centroid runs 2662 / 1724 / 1111 Hz over 0–50 / 50–150 / 150–400 ms (measured). No comparison with the Pro-One was made; "bright" is the 2662 Hz, and the same patch with filter DRIVE only reads 4270 Hz in the first 50 ms.
- **Moog Prodigy** — *the raw edge; Raw, Biting.* Not measured. The patch carries a drive (GROWL 44, below), which is not the same thing.
- **ARP Odyssey** — *the nasal cut; Nasal, Biting.* Not measured.

Closest to: **a Prophet-5 sync lead pushed into crunch**. "Crunch" is Vincent's word; the measured fact is the crest factor, 6.0 dB with GROWL 44 against 11.7 dB without drive.

Nothing here says the patch matches these: it was built toward the descriptions, by measurement, and approved by ear. "Warm" was part of the brief and is not measured.

## 4. How to play it

- **UNISON, one note at a time.** Three voices all play the key you press; a chord plays the last key only. The sweep fires on **detached** notes. With **legato** playing (a new key down before the old one is up) the envelopes are not re-fired: on notes 2–8 of the same riff the centroid over the first 100 ms is 2935 Hz detached against 1742 Hz legato, and the sweep adds +303 Hz detached against +174 Hz legato. The first note of either riff is the same. Notes 2–8 read −17.8 dB detached and −19.3 dB legato over those 100 ms.
- **Register:** the sweep was measured on A3 (above); the riff phrases run A3 to C6. No other register was measured.
- **Drive:** GROWL 44 lowers the crest factor of the dry lead from 11.7 to 6.0 dB, moves the level −0.3 dB at the same VOLUME, and lowers the peak from −4.1 to −10.2 dBFS (all measured, VOLUME 100). **It also darkens the strike**: the centroid over the first 50 ms is 2662 Hz with GROWL 44 against 4165 Hz with no drive and 4270 Hz with per-voice filter DRIVE 60 only. The brightness of the rip is a trade against the drive. The crest factor stays at 5.0 dB even at GROWL 127, so the 2.3 dB fuzz marker is not reached on this lead.
- **Glide:** GLIDE 50 takes 64 ms to come within 50 cents of a legato octave step (90 % of the octave in 39 ms).
- **Held note:** on a held A3 the centroid is 2420 Hz in the first 150 ms and 1112 / 1041 / 1042 / 1021 Hz over the next windows to 4 s; the level moves from −19.2 to −18.5 dB over the 4 s (measured, dry).
- **Dry:** no echo, no spring, no tape (DLY MIX 0, DRAIN 0, CHEW 0).
- **Level and cost:** VOLUME 90, −18.05 dBFS RMS over the note-on region of the single-note lead phrase (K-weighted −17.4), peak −11.0 dBFS; the standard stabs phrase (b) reads −17.1 dBFS, 0.9 dB louder than the lead phrase (a MONO or UNISON patch plays one key of a stab). **CPU 2326 host instr/sample worst case**: three UNISON voices cost +377 over one MONO voice (1732 against 1355 without GROWL), GROWL 44 about +595. The device render time is not measured.
- **Tricks:** SLOBBER, SEQ held (Tape Stop), the kill switch (HEEL) are untested on this patch.
- **Changed from the brief:** the original array had OSC 1 LEVEL 0 (a silent master: only the synced slave sounded), a single MONO voice, no drive, and a 1/8 echo with a spring. The patch now has an audible master (LEVEL 90), UNISON 3, GROWL 44 and no effects. The original brief is kept in `DOG-5-presets.md`.

## 5. Final values (for debugging, not for players)

`MODE UNISON (VOICES 3, DETUNE 22), OSC1 SAW LEVEL 90, OSC2 SAW LEVEL 120 SEMI +7 SYNC on ENV>O2 104 (+15.2 st at the envelope's top), FILTER LP24 CUTOFF 84 RESO 10 KEY TRK 64 ENV AMT 100, FILTER ENV A20 D80 S20 R60, AMP ENV A2 D70 S100 R40, GLIDE 50, VINTAGE 30, SPREAD 60, no LFO, DRIVE 0, GROWL 44, DLY MIX 0, DRAIN 0, CHEW 0, VOLUME 90` — `PF_BSYNCA` in `firmware/src/obv_patches.h`.
