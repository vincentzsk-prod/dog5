# 22 · Melting Orb · Chapter III · The Bakshi Tomes

*Voiced 6 Nov 2026 (Batch 5A), approved after listening: variant D (the DUAL one, where a chord melts together; Vincent: "sounds incredible"). Renders: `reference-renders/22-melting-orb_D_*.wav`. Log: `../22-melting-orb.md`.*

## 2. What it sounds like

A thick stack of detuned saw tones that opens bright when the key goes down and then slowly sinks: the filter closes and the pitch falls together over a few seconds, until the sound settles low and dark. It is a held collapse, not a zap. It takes chords (three keys gate six voices). It is dry: no echo, no spring. Held, it stays down; a short tap gives only the bright opening.

## 3. Gear inspirations (docs only, "inspired by")

- **Oberheim OB-Xa** — *a fat unison source* (a DUAL pair of saws per key, 9.8 cents apart plus the patch's slop; a width measurement was not made, so "fat" is not measured).
- **Sequential Prophet-5** — *the slow filter-envelope sweep* (measured: the centroid falls from 1323 Hz to 204 Hz, 32.4 semitones, reaching 90 % of the fall at 3.5 s on A2).
- **Korg MS-20** — *resonance, high but musical* (RESO 75 of 127 on a 12 dB low-pass, linear by the probe at 11.5 dB against 12; it sings by itself only at 127; "musical" is not measured).

Closest to: **an OB-Xa-style fat stack whose filter and pitch both sink slowly downward**.

Nothing here says the patch matches these: it was built toward the descriptions, by measurement, and approved by ear.

## 4. How to play it

- **Hold the key.** The melt happens while the key is down; there is no Drone Latch. A short tap hears the open start and none of the melt (a 150 ms tap reads −1.1 / −0.6 / 0.0 dB re the held level on A1 / A2 / A3, centroid 839 / 1266 / 1729 Hz).
- **OSC 1 is off.** ENV>O2 bends OSC 2's pitch only (and from the filter envelope, never the amp envelope), so the stack that melts is OSC 2 alone. With OSC 1 on it would stay at pitch while OSC 2 sank.
- **How it melts (A2 held, 0.5 s windows):** the pitch ends −678 cents (−6.8 st, the formula gives −6.86 st), reaching 90 % of the fall at 4.0 s and 98 % at 5.0 s; the centroid falls 1323 → 204 Hz, 90 % of the fall at 3.5 s, 98 % at 5.5 s. The fall is front-loaded (suggests an analog-style attack curve; not isolated): −436 of −678 cents in the window starting at 2.0 s. Level windows 0–1 / 1–3 / 3–6 / 6–8 / 9–14 s: −19.2 / −19.1 / −18.6 / −18.8 / −18.9 dBFS. Almost all the energy ends in 60 to 400 Hz (74 % / 26 %).
- **Chords:** DUAL with POLY 6, so three keys gate six voices. The melt itself was measured on a single held A2; a chord melting together as one stack was not measured. A three-key chord (A2 E3 A3) reads −14.2 dBFS RMS and **peaks at −4.1 dBFS**, 4.7 dB louder than one held note; this is what limits VOLUME (97). Phrase (b) stabs peak at −6.6 dBFS.
- **On key-up the melt partly runs backwards.** The filter envelope releases, so pitch and brightness climb back while the note fades, even at the slowest filter release. Measured on a 15 s A2 hold in the windows starting 0 / 0.5 / 1.0 s after key-up: pitch −639 / −549 / −469 cents, centroid 238 / 826 / 2469 Hz; the tail is 20 / 40 / 60 dB down at 474 / 932 / 1294 ms. Whether that is audible at those levels is not tested.
- **Level and cost:** VOLUME 97, −18.9 dBFS RMS over +9 s to +14 s of the A2 hold (K-weighted −20.3; the first second −19.2). **About 2489 host instr/sample worst case (idle 1164 + 1325 under load), the highest of any voiced patch** (15 D: 2375). The device render time is not measured.
- **Legato:** DUAL is polyphonic, so the MONO / UNISON no-retrigger rule does not apply (engine fact; not tested on this patch).
- **Tricks:** untested on this patch: SLOBBER, SEQ held (Tape Stop), the kill switch (HEEL), GROWL, CHEW.

## 5. Final values (for debugging, not for players)

`MODE DUAL (POLY 6, DETUNE 40 = ±9.8 cents), OSC1 OFF, OSC2 SAW LVL 110 SEMI 0, ENV>O2 46 (−6.86 st at the envelope's top), FILTER LP12 CUTOFF 100 (4186 Hz) RESO 75 KEY TRK 64 ENV AMT 32 (−32 = about −49 st at the top), FILTER ENV A118 (4.96 s nominal) D60 S127 R127, AMP ENV A60 D100 S127 R92, no LFO, VINTAGE 40, SPREAD 110, VOLUME 97 (−18.9 dBFS RMS on the A2 hold, chord peak −4.1); no echo, no spring, CHEW 0, GROWL 0, no arp` — `PF_MELTING_ORB` in `firmware/src/obv_patches.h`.
