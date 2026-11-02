# CHEW — listening kit

CHEW is the tape, stage 4 of the Psych Chain (`firmware/src/obv_tape.h`). Everything here was rendered by the host build
(`tests/host.c`), which runs the firmware's own integer code, so these are the samples the FM-1 would send over USB
with MASTER all the way up. 16-bit stereo, 44.1 kHz, from just before the first note.

**Listen at one fixed volume and step through each row.** Every row should sit at about the same loudness while the
sound changes, as with GROWL. Most of what CHEW does is slow (wow) or quiet (hiss), so **use headphones** for the
hiss and the flutter.

## Where it sits, for now

`voices → GROWL → output stage → delay (old ping-pong) → reverb (old plate) → CHEW → out`.

CHEW sits last, where the brief puts it (after Spring). The delay and reverb aren't re-voiced yet, so **the final order
is not locked**. Two things to decide when BBD and Spring are done:
1. **Does Tape stay after the reverb?** Right now the reverb's tail and the delay's repeats get wowed and hissed too.
   That is the brief's "Tape last compounds slop + wow". It is also why a long reverb tail keeps the hiss awake.
2. **Should Tape see the effects' sum unclipped?** Today the delay + reverb sum is hard-clipped at full scale before
   Tape (it always was). Tape's soft saturation could round those peaks instead, but that means changing the effects'
   last line, which this session was told not to touch.

The scope (the bark) taps before the effects, so the dog's beam shows neither the wow nor the hiss.

## The files

CHEW 0 % is a bit-exact bypass, so the 0 % column is the GROWL kit's own file.

| source | what it is | CHEW 0 % | 25 % | 50 % | 75 % | 100 % |
|---|---|---|---|---|---|---|
| **lowsaw** | one plain saw, C2 (65 Hz), held 3 s; filter open-ish (INIT, OSC 2 off) | [0](../drive/lowsaw_growl000.wav) | [25](lowsaw_chew025.wav) | [50](lowsaw_chew050.wav) | [75](lowsaw_chew075.wav) | [100](lowsaw_chew100.wav) |
| **chord** | a held Cmaj7 (C3 E3 G3 B3), two detuned saws a voice (INIT, POLY) | [0](../drive/chord_growl000.wav) | [25](chord_chew025.wav) | [50](chord_chew050.wav) | [75](chord_chew075.wav) | [100](chord_chew100.wav) |
| **bass** | program 1 *Red Pill* as voiced, an 8th-note riff on A1 | [0](../drive/bass_growl000.wav) | [25](bass_chew025.wav) | [50](bass_chew050.wav) | [75](bass_chew075.wav) | [100](bass_chew100.wav) |
| **lead** | a bright mono lead, filter wide open: G5 A5, then C6 held 2 s, E5 | [0](../drive/lead_growl000.wav) | [25](lead_chew025.wav) | [50](lead_chew050.wav) | [75](lead_chew075.wav) | [100](lead_chew100.wav) |

The raw knob values are 0, 32, 64, 95 and 127. WOW/FLT, HISS and DROPS stay at their defaults (64 each: both, 0 dB, the
macro's own amount).

**GROWL and CHEW together**, as they will be played. Compare each with GROWL alone at the same setting
(`../drive/<source>_growl025/050/100.wav`):

| source | GROWL 25 + CHEW 25 | GROWL 50 + CHEW 50 | GROWL 100 + CHEW 50 | GROWL 50 + CHEW 100 | GROWL 100 + CHEW 100 |
|---|---|---|---|---|---|
| lowsaw | [▶](lowsaw_growl025_chew025.wav) | [▶](lowsaw_growl050_chew050.wav) | [▶](lowsaw_growl100_chew050.wav) | [▶](lowsaw_growl050_chew100.wav) | [▶](lowsaw_growl100_chew100.wav) |
| chord | [▶](chord_growl025_chew025.wav) | [▶](chord_growl050_chew050.wav) | [▶](chord_growl100_chew050.wav) | [▶](chord_growl050_chew100.wav) | [▶](chord_growl100_chew100.wav) |
| bass | [▶](bass_growl025_chew025.wav) | [▶](bass_growl050_chew050.wav) | [▶](bass_growl100_chew050.wav) | [▶](bass_growl050_chew100.wav) | [▶](bass_growl100_chew100.wav) |
| lead | [▶](lead_growl025_chew025.wav) | [▶](lead_growl050_chew050.wav) | [▶](lead_growl100_chew050.wav) | [▶](lead_growl050_chew100.wav) | [▶](lead_growl100_chew100.wav) |

**The knob, turned.** [sweep_chord.wav](sweep_chord.wav) and [sweep_lead.wav](sweep_lead.wav) hold the chord, or the
lead's C6, for 9 s while KNOB 1 on the TAPE page turns from 0 up to 100 % and back down, one detent every 60 ms.
[toggle_chord.wav](toggle_chord.wav) holds the chord while CHEW jumps 0 → 50 % → 0 → 100 % → 0, the way a patch
change does.

**The parts on their own.**
- [sine1k_chew100.wav](sine1k_chew100.wav), [..._wow_only](sine1k_chew100_wow_only.wav), [..._flutter_only](sine1k_chew100_flutter_only.wav):
  a bare 1 kHz sine (−12 dBFS) through CHEW 100 % at WOW/FLT 64, 0 and 127. A sine hides nothing, so this is the
  wobble itself.
- [hiss_only_chew100.wav](hiss_only_chew100.wav): the hiss alone at CHEW 100 % (the chord render minus the same with
  HISS 0). It is at its real level, so it is quiet. [hiss_only_chew100_plus30dB.wav](hiss_only_chew100_plus30dB.wav)
  is the same 30 dB up, to hear its colour.

### Loudness (ITU-R BS.1770-4 integrated, the whole file)

| source | 0 % | 25 % | 50 % | 75 % | 100 % |
|---|---:|---:|---:|---:|---:|
| lowsaw | −21.4 LUFS | −21.4 (+0.02) | −21.4 (+0.02) | −21.4 (−0.01) | −21.5 (−0.12) |
| chord | −12.3 LUFS | −12.2 (+0.02) | −12.2 (+0.02) | −12.3 (+0.00) | −12.4 (−0.11) |
| bass | −25.6 LUFS | −25.5 (+0.07) | −25.5 (+0.12) | −25.4 (+0.14) | −25.6 (+0.04) |
| lead | −15.9 LUFS | −15.9 (−0.02) | −15.9 (−0.05) | −16.0 (−0.12) | −16.2 (−0.27) |

The spec was "within about 1 dB, as GROWL". The widest gap is −0.27 LU, on the bright lead. Without the trim (below)
it was +1.7 LU on the low saw and −0.9 LU on the lead. With GROWL on as well, CHEW stays within −0.27 … +0.13 LU of the
same GROWL alone, on all four sources at all five combinations.

## What CHEW does, measured

One knob, in this order along its travel: **wow** from the start, **flutter** from 20 %, **dropouts** from 45 %. The
saturation, the head loss (darker), the head bump (+2 dB near 100 Hz) and the hiss rise all the way.

**Wow and flutter** (a 1 kHz sine, the pitch deviation; [wow_flutter.png](wow_flutter.png) draws it):

| CHEW | peak | RMS | of which wow (< 4 Hz), peak | flutter (4–200 Hz), peak |
|---|---:|---:|---:|---:|
| 25 % | 0.19 % (3 cents) | 0.08 % | 0.16 % | 0.03 % |
| 50 % | 0.55 % (9 cents) | 0.22 % | 0.42 % | 0.14 % |
| 75 % | 1.00 % (17 cents) | 0.39 % | 0.74 % | 0.26 % |
| 100 % | 1.53 % (26 cents) | 0.57 % | 1.11 % | 0.40 % |
| 100 %, WOW/FLT 0 (wow only) | 1.24 % | 0.56 % | 1.10 % | 0.14 % |
| 100 %, WOW/FLT 127 (flutter only) | 0.42 % | 0.13 % | 0.15 % | 0.36 % |

For scale, cassette decks' spec sheets quote roughly 0.05–0.15 % (weighted RMS), and a worn tape is worse. So 25 % is a decent deck, 50 % a tired one,
and 100 % is a warped tape, seasick on purpose. The wow is two slow sines (0.55 and 1.37 Hz), their rates and the
second one's depth wandering at random. The flutter is a 9 Hz wobble plus band-limited noise, which is what roughens
the sustain.

**The record's saturation** is Drive's tanh table at 1.5×, blended in by CHEW. On a 1 kHz sine at −6 dBFS:

| CHEW | H3 | H5 | H2 |
|---|---:|---:|---:|
| 25 % | −43 dB | −69 dB | −98 dB |
| 50 % | −36 dB | −63 dB | −96 dB |
| 100 % | −29 dB | −62 dB | −88 dB |

It is symmetric, so odd harmonics only: the warm-compression side of tape, not Drive's even-order bias.

**The hiss** (RMS of one channel; with the default HISS):

| CHEW | 1 % | 25 % | 50 % | 75 % | 100 % | 100 %, HISS −12 dB | 100 %, HISS +12 dB |
|---|---:|---:|---:|---:|---:|---:|---:|
| hiss | −86 dBFS | −73 | −63 | −55 | −50 | −62 | −38 |

It is shaped 400 Hz – 7 kHz: "shhh" rather than "ssss". L and R are independent, so it is wide. **It rests 2 s after
the input falls silent** (fading over ~0.7 s) and comes back with the next note, so a held tape never hisses into the
PA between songs. A held drone or a reverb tail keeps it awake.

**Dropouts** (a 30 s sine; a dip is a fall of more than 2 dB):

| CHEW | DROPS 64 (default) | DROPS 127 |
|---|---|---|
| 50 % | one every ~30 s, −3 dB | the same |
| 75 % | 0.45 a second, −5.6 dB median (−8 deepest), ~35 ms | 1.0 a second, to −11 dB |
| 100 % | 1.1 a second, −7 dB median (−16 deepest), ~40 ms | 4 a second, −10 dB median (−26 deepest) |

A dropout also closes the head loss (it dulls as it dips), and its edges glide over ~3 ms, so it never clicks.

## Aliasing, flagged

The pitch modulation is a moving read from a delay line. Done badly it smears inharmonic sidebands around everything
bright. Three proofs, from the general one to the specific:

**1. The synth, as in GROWL's table.** A single saw (VINTAGE 0, so an exact harmonic comb), filter open, C6 and C7,
the hiss and dropouts off (noise isn't aliasing). Wow spreads each harmonic by design, so "inharmonic" here means
outside each harmonic's own wobble (± k·f0·1.7 % + 20 Hz with the wow alone; ± k·f0·1.9 % + 150 Hz with the flutter
too). [aliasing_c6.png](aliasing_c6.png) and [aliasing_c7.png](aliasing_c7.png) show it: blue is the harmonics and
their wobble, red is everything else.

| test | inharmonic energy | loudest inharmonic component (re the fundamental) |
|---|---:|---:|
| C6 saw, CHEW 0 % (the dry synth) | −40.5 dB | −43.7 dB at 15.8 kHz |
| C6 saw, CHEW 100 %, wow only | **−53.0 dB** | −62.7 dB at 1.0 kHz (the fundamental's own skirt) |
| C6 saw, CHEW 100 %, wow + flutter | **−57.8 dB** | −70.6 dB at 847 Hz |
| C7 saw, CHEW 0 % | −38.0 dB | −38.6 dB at 14.8 kHz |
| C7 saw, CHEW 100 %, wow only | **−51.0 dB** | −61.0 dB at 2.0 kHz |
| C7 saw, CHEW 100 %, wow + flutter | **−54.6 dB** | −63.7 dB at 2.3 kHz |

As with GROWL, the tape measures **cleaner** than the dry synth: its head loss takes off the oscillators' own polyBLEP
residue near 15 kHz. What is left sits right beside the fundamental, which brings in proof 2.

**2. The read against its ideal.** The bench logs the head's exact path and computes the mathematically perfect
output for that path (the analysis fits the down-sampler's lag). The difference is the read's whole error:
interpolation, rounding and any aliasing together.

| tone | the read's error (re the tone) | loudest error component |
|---|---:|---:|
| 1 kHz | −69.0 dB | −74.5 dB |
| 5 kHz | −69.5 dB | −84.3 dB |
| 10 kHz | −68.8 dB | −72.7 dB |
| 15 kHz | −65.3 dB | −72.5 dB |
| 18 kHz | −61.8 dB | −64.2 dB |

For the same tones, the energy outside ±(1.9 % + 150 Hz) is the same to the decimal in the ideal output and in
CHEW's: −60.6, −49.9 and −47.2 dB at 1, 5 and 10 kHz. **So everything outside the partials in proof 1 is the
wobble itself (an FM skirt), not an artefact.** Compared per harmonic, a saw's 15th is already 23 dB down, so the
read's error at 15 kHz is about −88 dB re the fundamental.

**3. The record's saturation alone,** at 2× (a −6 dBFS tone): inharmonic −79.5 / −82.6 / −78.7 dB at 1 / 5 / 10 kHz.
**Flag:** a pure tone at 15–18 kHz at −6 dBFS folds its 5th harmonic back in at −54 dB. Nothing on this synth puts
that much energy up there (a C6 saw's 15th harmonic is already 23 dB down), so I left it.

**Why it took a custom read.** A 4-point Hermite read (what the brief suggested, as the old chorus used) at 44.1 kHz
leaves the moving read's sidebands at −30 dB under a 10 kHz tone. At 2× it is −43 dB. Both are audible as a fizz on
bright patches under wow. I ran the line at 2× and replaced Hermite with a **6-point, 5th-order polynomial fitted for a
2× line** (`tests/tape/interp_fit.py`, Niemitalo's form). Its worst error is −80 dB at 10 kHz and −56 dB at 18 kHz re
the tone. It needs no second halfband stage, which 4× Hermite would (the fit's numbers: `python3 tests/tape/interp_fit.py`).

## Clicks and the knob

- **Knob sweeps** (the bench: a sine through CHEW, 0 → 100 % → 0, one detent every 60 ms, against fixed settings): the
  worst step ratio is **1.02** on a 1 kHz sine (1.0 = nothing a fixed setting wouldn't do). The level against fixed
  settings is within 0.31 dB.
- **Entering the bypass** is the one exception. Leaving 0, CHEW crossfades from the dry signal to its own over 5.8 ms,
  as GROWL does. The two are ~2.5 samples apart (the halfbands), so for those 5.8 ms they form a comb: a 5 kHz sine
  dips by 2.9 dB (step ratio 1.40). In the chord sweep this shows as the only click candidate, at 3.199 s, at −78 dBFS
  above 10 kHz. Listen for a "tsk" there. GROWL's entry does the same.
- **A turn of CHEW never bends the pitch.** The head sits 3.6 ms behind the record point and the wow swings around it.
  The wobble's depth follows the knob at a limited rate (~3 s for the whole range, never more than 0.1 % of pitch from
  the turn itself). **Leaving 0** the head moves out to 3.6 ms over ~1.4 s (the tape spins up: 0.25 % flat). **Back to
  0** it returns first, then crossfades out. So CHEW 100 → 0 takes ~3 s to settle back to the dry sound (hear it in toggle_chord.wav).
- The synth sweeps and the toggles show no click candidates above −80 dBFS.

## Measured, apart from the sound

- **Bypass:** at CHEW 0, all 32 factory programs and the host scripts are byte-identical to `main` before CHEW existed,
  GROWL-on scripts included (`tests/drive/bitexact.sh 6630c5b`).
- **Overflow:** none. The bench (full-scale squares and noise, every CHEW, the secondaries' corners, knob jumps) and the
  whole synth (8-voice unison at VOLUME 127, GROWL 127, delay and reverb at 127, HISS and DROPS 127, CHEW and WOW/FLT
  stepped) run clean under `-fsanitize=signed-integer-overflow,bounds`. The read's products are bounded for any int16
  line content (Σ|h| ≤ 1.46).
- **CPU (host callgrind, x86-64 instructions per sample):** CHEW **961** at any setting above 0, the heaviest stage.
  All four on: **2,379** (GROWL 742, delay 109, reverb 566). CHEW 0 costs nothing. The breakdown and the levers are in
  `dog5-docs/PERF-BASELINE.md`. **The device's GLOBAL page decides.**
- **Memory (device build):** pool 271,772 → 275,868 B (+4,096: the line, 1024 stereo frames at 88.2 kHz). RAM +384 B.
  Image +7.4 KB (code and 2.8 KB of tables). **Latency +3.6 ms** while CHEW is on (the head).

## How GROWL and CHEW interact

[growl_chew_hiss.png](growl_chew_hiss.png) draws the music and the hiss separately (the hiss is the render minus the
same render with HISS 0, sample for sample). The table is music over hiss, band by band (dB; positive = the music
covers the hiss):

| | 1–4 kHz | 4–8 kHz | 8–16 kHz |
|---|---:|---:|---:|
| chord, CHEW 100 | +27.6 | −5.1 | −37.2 |
| chord, GROWL 50 + CHEW 100 | +30.1 | +6.6 | −16.5 |
| chord, GROWL 100 + CHEW 100 | +32.4 | +16.3 | +1.9 |
| bass, CHEW 100 | −0.2 | −28.9 | −38.7 |
| bass, GROWL 50 + CHEW 100 | −0.3 | **−31.2** | **−39.5** |
| bass, GROWL 100 + CHEW 100 | +6.8 | −13.1 | −31.6 |
| lead, CHEW 100 | +38.7 | +26.0 | +16.1 |
| lead, GROWL 100 + CHEW 100 | +39.0 | +22.7 | +8.6 |

What surprised me:

1. **Your worry is half right, on bass only.** At GROWL 50, Drive's darkening (its pre-clip low-pass and TONE) takes
   the bass riff's top down a further 2 dB under the hiss than CHEW alone. At GROWL 100 the fuzz's own harmonics win
   it back (+16 dB at 4–8 kHz). On the chord, any GROWL fills the top in and covers the hiss better. So the bad corner
   is **a dark, low patch with moderate GROWL and high CHEW**: there the hiss is a separate "shhh" layer above the
   riff rather than a texture inside it. HISS −12 dB is the remedy per patch.
2. **On anything low, the hiss is the only thing above ~4 kHz at CHEW ≥ 50 %**, with or without Drive (bass at CHEW 50:
   −14 dB at 4–8 kHz). That is how tape on a bass sounds, but it means the hiss will be heard on the bass patches long
   before it's heard on leads. **If you want it to sit inside the sound,** the next step would be to have the hiss
   follow the music's brightness. I didn't build that: ask.
3. **They stack cleanly in level.** Both trims (GROWL's, then CHEW's) hold loudness: every combination is within
   −0.27 … +0.13 LU of GROWL alone at the same setting.

## What I tuned, and why

- **2× line, 6-point read:** above. **The head at 3.6 ms, fixed** (not a delay that grows with CHEW), so CHEW turns
  never bend the pitch. The cost is 3.6 ms of latency.
- **The wow's shape:** first a plain parabola for the sine. Its pitch turned in corners at each extreme, a mechanical
  wobble. Now a refined sine (within 0.1 %).
- **Loudness:** the bump (+2 dB near 100 Hz) made low sources louder and the head loss made bright ones quieter, a
  2.6 dB spread that no static law could hold. Like GROWL: a static law (−0.6 dB at the top) plus a 1.5 s K-weighted
  trim, ±3 dB at most, none at a gentle setting. **The trim listens before the hiss and the dropouts,** so those stay
  heard as texture and are not compensated away.
- **Secondaries (SELECT held, TAPE +):** WOW/FLT (the brief's wow/flutter balance: 0 wow only, 64 both, 127 flutter
  only), HISS (0 off, else −12 … +12 dB around CHEW's own), DROPS (0 none, 64 CHEW's own, 127 three times as many and
  deeper). My reasoning: the patches in DOG-5-presets ask for different tapes. 13 *Ghost Board* wants max wow/flutter,
  23 *Crypt Dust* heavy wow, 17 *Titanic* "dropouts optional", 05 *ZEAROX* everything. That is a choice of *which*
  damage, not of how much: CHEW stays the one performance knob.

## For your ears, specifically

1. **The top of the wow (1.5 % peak at 100 %).** Seasick on purpose. Too much, or not enough for *Ghost Board*?
2. **The flutter's roughness** (sine1k_chew100_flutter_only.wav): the noise part is what makes it tape rather than a
   vibrato. Is it grit or is it fizz?
3. **The hiss level and colour,** especially on the bass at CHEW 50 (bass_chew050.wav, then the +30 dB file).
4. **The entry "tsk"** in sweep_chord.wav at 0.55 s (the first detent off 0).
5. **The 2 s rest of the hiss:** right for stage, or would you rather it ran like a deck?
6. **The record's saturation (H3 −29 dB at the top):** a touch, or too much on top of GROWL?

## Not done here, on purpose

- BBD and Spring untouched (as asked). The FX-held layer's four knobs are still GROWL / BBD mix / SPRING mix / BBD time.
  The brief maps them to GROWL / ALLEY / DRAIN / **CHEW**, so CHEW isn't on the FX-held layer yet. Decide that with the
  BBD re-voice.
- No factory patch changed: all 32 are at CHEW 0, so byte-identical.

## Reproduce

```
tests/tape/render.sh                                     # the host and bench renders -> build/tape/
python3 tests/tape/analyze.py build/tape                 # every table above
python3 tests/tape/make_kit.py build/tape listen/tape    # this folder's WAVs and pictures
python3 tests/tape/interp_fit.py                         # the read's fit (--check: obv_tape.h carries it)
tests/drive/bitexact.sh REV                              # CHEW 0 == another revision, byte for byte
for s in off chew all4; do tests/perf_callgrind.sh tests/tape/perf_$s.txt; done   # CPU (perf_scripts.py writes them)
```
