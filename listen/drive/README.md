> The audio files in this folder were removed from main in the housekeeping commit e40f5d5; they are in the git history before that commit, and can be regenerated with the Reproduce commands below.

# GROWL — listening kit

GROWL is the preamp drive, stage 1 of the Psych Chain (`firmware/src/obv_drive.h`). Everything here was rendered by the
host build (`tests/host.c`), which runs the firmware's own integer code, so these are the samples the FM-1 would send
over USB with MASTER all the way up. 16-bit stereo, 44.1 kHz, from just before the first note.

**Listen at one fixed volume and step through each row.** Every row should sit at about the same loudness while the
sound changes. That is the design goal, and the table shows the measurement.

## The files

| source | what it is | GROWL 0 % | 25 % | 50 % | 75 % | 100 % |
|---|---|---|---|---|---|---|
| **lowsaw** | one plain saw, C2 (65 Hz), held 3 s; filter open-ish (INIT, OSC 2 off) | [0](lowsaw_growl000.wav) | [25](lowsaw_growl025.wav) | [50](lowsaw_growl050.wav) | [75](lowsaw_growl075.wav) | [100](lowsaw_growl100.wav) |
| **chord** | a held Cmaj7 (C3 E3 G3 B3), two detuned saws a voice (INIT, POLY) | [0](chord_growl000.wav) | [25](chord_growl025.wav) | [50](chord_growl050.wav) | [75](chord_growl075.wav) | [100](chord_growl100.wav) |
| **bass** | program 1 *Red Pill* as voiced (MONO, saw + pulse an octave up, its own filter drive 40), an 8th-note riff on A1 | [0](bass_growl000.wav) | [25](bass_growl025.wav) | [50](bass_growl050.wav) | [75](bass_growl075.wav) | [100](bass_growl100.wav) |
| **lead** | a bright mono lead, filter wide open: G5 A5, then C6 held 2 s, E5 | [0](lead_growl000.wav) | [25](lead_growl025.wav) | [50](lead_growl050.wav) | [75](lead_growl075.wav) | [100](lead_growl100.wav) |

GROWL shows as a percentage. The raw knob values are 0, 32, 64, 95 and 127. BIAS and TONE stay at their defaults (40 and 50).

**The knob, turned:** [sweep_chord.wav](sweep_chord.wav) and [sweep_lead.wav](sweep_lead.wav) hold the chord, or the
lead's C6, for 9 s while KNOB 1 on the DRIVE page turns from 0 up to 100 % and back down. That is 64 single detents
each way, one every 60 ms, as a hand would turn it. Listen for clicks, zipper noise and level jumps. The tests found none
(see below).

### Loudness (ITU-R BS.1770-4 integrated, the whole file)

| source | 0 % | 25 % | 50 % | 75 % | 100 % |
|---|---:|---:|---:|---:|---:|
| lowsaw | −21.4 LUFS | −21.4 (−0.0) | −21.6 (−0.2) | −21.7 (−0.3) | −21.7 (−0.3) |
| chord | −12.3 LUFS | −12.3 (+0.0) | −12.2 (+0.1) | −12.0 (+0.3) | −11.8 (+0.4) |
| bass | −25.6 LUFS | −25.5 (+0.1) | −25.4 (+0.2) | −25.1 (+0.5) | −25.0 (+0.6) |
| lead | −15.9 LUFS | −16.0 (−0.1) | −16.2 (−0.3) | −16.0 (−0.1) | −16.0 (−0.1) |

The spec was "within about 1 dB between 0 and 100". The widest gap is +0.6 LU, on the bass. That is the trim settling
over the riff's first second: the static law reads the bass's added upper harmonics as louder than they are.

### The pictures

- [harmonics_lowsaw.png](harmonics_lowsaw.png), [harmonics_lead.png](harmonics_lead.png): each harmonic's level against the
  fundamental at the five settings. Here GROWL is easy to see. Driven hard, the low saw loses its even harmonics
  (2nd −5.4 → −32.5 dB, 4th −11.5 → −28.2 dB) while the odd ones keep a square's 1/k (3rd −9.9, 5th −15.4, 7th −19.5):
  a saw squared off. Default BIAS keeps a trace of the evens.
- [spectrum_chord.png](spectrum_chord.png), [spectrum_bass.png](spectrum_bass.png): the whole spectrum, one row per
  setting. The chord's intermodulation fills in between its notes from 25 % on.
- [aliasing_c6.png](aliasing_c6.png), [aliasing_c7.png](aliasing_c7.png): a single saw (VINTAGE 0, so an exact harmonic
  comb), filter open, held at C6 / C7 at GROWL 100 %. Blue is the harmonics. Red is everything else, which is where
  aliasing would show.

## Aliasing, flagged

Anything not at a harmonic of the note counts as inharmonic. Measured from 20 Hz to 16 kHz, Blackman-Harris window, 2^16 points.

| test | inharmonic energy (re the harmonics) | loudest inharmonic component (re the fundamental) |
|---|---:|---:|
| the synth, C6 saw, GROWL **0 %** | −40.5 dB | −43.7 dB at 15.8 kHz |
| the synth, C6 saw, GROWL **100 %** | **−61.7 dB** | **−73.7 dB** at 1.19 kHz |
| the synth, C7 saw, GROWL **0 %** | −38.0 dB | −38.6 dB at 14.8 kHz |
| the synth, C7 saw, GROWL **100 %** | **−57.2 dB** | **−66.1 dB** at 2.24 kHz |
| GROWL alone, an ideal (alias-free) C6 saw, 100 % | −61.2 dB | −73.2 dB at 2.24 kHz |
| GROWL alone, an ideal C7 saw, 100 % | −60.5 dB | −67.6 dB at 147 Hz |
| GROWL alone, a 220 Hz saw 24 dB under one voice, 100 % | −52.5 dB | −61.9 dB at 120 Hz |

**Flags.** Driven flat out, a high note carries no inharmonic component louder than −66 dB below its fundamental.
The worst case in the table is a quiet decaying tail into full GROWL: a component at 120 Hz, −62 dB under a 220 Hz
fuzz. It sits below the note, where nothing masks it, so it is the one to listen for. It is integer resolution, not
aliasing: it falls 6 dB for every 6 dB the input rises. The dry synth's own oscillators leave −40 dB of residue near
15 kHz (polyBLEP's limit). GROWL's pre-clip low-pass removes most of that, so the drive at 100 % measures *cleaner*
than the dry patch.

## What I tuned, and why

**Where it sits.** On the summed voice bus, before the output stage (the gentle tanh with CC 7), the delay and the
reverb. CC 7 can't change how hard it drives, as with a pedal before the amp's master. The scope sits after the output
stage, so the bark shows the drive. GROWL reads the bus at its full resolution (two bits more than the output stage
keeps), which is worth 6–12 dB less grit on quiet tails.

**Gain.** At GROWL 1 % one voice peaks at 0.2 in tanh units, and at 100 % at 16. The steps are exponential, the
gain doubling every ~20 knob steps. The range comes from a measurement: one voice of a plain saw peaks at ~1400 on the
drive's scale, a chord at ~6200, the bright lead at ~2500. For a single note, then: 0–25 % is warmth, 25–50 % crunch,
50–75 % distortion and 75–100 % fuzz. A chord runs about 40 knob steps ahead of that.

**The clip.** It uses the existing tanh table (`softclip`'s), read once, branch-free, flat beyond 2. I first composed it
twice for a rounder knee past 2. That measured no better for aliasing (−58.3 vs −58.2 dB), and reading the table once
(branch-free) saved 213 instructions per sample. tanh's slope at 2 is already 0.07, so the knee is nearly round anyway.

**BIAS (asymmetry, SELECT held + KNOB 1).** An offset into the clip, minus the clip's value there, then a 10 Hz DC
block. Measured on a 220 Hz sine at one voice's level:

| | BIAS 0 | BIAS 40 (default) | BIAS 127 |
|---|---:|---:|---:|
| GROWL 1 %: 2nd harmonic | −86 dB | −40 dB | −22 dB |
| GROWL 25 % | −83 dB | −31 dB | −13 dB |
| GROWL 50 % | −69 dB | −28 dB | −8 dB |
| GROWL 100 % | −62 dB | −45 dB | −24 dB |

The default is "a little even-order warmth": −40 dB at the gentlest setting. The knob's travel is quadratic, so most
of it is fine adjustment near the default.

**Anti-aliasing.** The clip runs at 4× (176.4 kHz) between polyphase allpass halfband filters (4 + 2 coefficients,
12-bit integers, 18 kHz passband). Oversampling alone couldn't do it: a full-band saw driven hard still aliased at
−40 dB even at 8× (prototyped in Python first). The second half is a pre-clip low-pass, two one-poles, open up to
GROWL 25 % and closing from 14 kHz to 3 kHz at 100 %. A high-gain op-amp fuzz loses bandwidth the same way, and it is
what keeps the clipped edges clean. I tried bigger filters (5 + 3 coefficients): same aliasing, 95 instructions more.

**TONE (SELECT held + KNOB 2).** A one-pole after the clip, from 1.2 kHz to open. The default (50) is ~4.5 kHz, the
usual fuzz fizz cut. GROWL weights it in: none of it at a gentle setting (so turning GROWL up from 0 doesn't suddenly
darken a pad), all of it from GROWL ~31 %.

**Level.** There are two parts:
1. A static law per GROWL, which turns with the knob: a saw at one voice's level comes out at its own RMS.
2. A slow trim (~1.5 s) to the input's loudness. It hears the way you do: through the output stage's tanh with CC 7,
   then a K-weighting filter within 0.9 dB of BS.1770's real curve from 50 Hz to 16 kHz.

The trim is there because chords and hot patches clip harder than one voice. Plain RMS matching left the bass +1.4 and
the low saw −0.8. K-weighting brought that to +0.6 / −0.3. Detecting through the output stage took the chord from
+0.9 to +0.4. The trim's range is ±12 dB from GROWL ~31 % up and shrinks to nothing at a gentle setting, where the
static law is exact. A fast turn down to clean therefore never leaves a stale trim behind. The trim's slowness is
deliberate: a note's own swell and fuzz sustain inside 1.5 s stay.

**The knob.** The gain and the static makeup glide together, sample by sample, over ~1.5 ms; the trim glides over
~23 ms. Every glide lands exactly. An early version stepped them per 16-frame block, and the sweep test caught the
zipper (up to 5 % steps at the lowest gains). GROWL 0 is a bit-exact bypass (the engine skips the drive); entering or
leaving it crossfades over 256 frames.

## Measured, apart from the sound

- **Bypass:** at GROWL 0, all 32 factory programs and the host test scripts are byte-identical to the build before
  GROWL existed (`tests/drive/bitexact.sh`).
- **Knob sweeps** (a sine through GROWL, 0 → 100 % → 0, one detent every 60 ms). Click test: in each block, the largest
  sample-to-sample step over the RMS, against what any fixed setting nearby produces. The worst ratio is 1.02–1.11
  (1.0 = nothing a fixed setting wouldn't do; the 1.11 is the final 256-frame crossfade into bypass). Level against fixed
  settings drifts by at most 2.9 dB for realistic signals while the trim catches up. One exception: a full-scale sine
  (4× the loudest chord measured) entering at GROWL 2 % is 8.5 dB quieter than dry, because even 2 % squashes a signal
  that hot.
- **Overflow:** none. The bench and the whole synth were built with `-fsanitize=signed-integer-overflow` and run on
  full-scale squares and noise at every GROWL with BIAS and TONE at each extreme, full-scale knob sweeps, and 8-voice
  unison saws at VOLUME 127. The output can't exceed int16: the output stage's tanh comes after GROWL.
- **CPU (host callgrind, x86-64 instructions per sample):** GROWL **742** at any setting. Chorus was 169, delay is 109,
  reverb 566. With all of them on: 843 → **1,417**. GROWL 0 costs nothing. Details and levers:
  `dog5-docs/PERF-BASELINE.md`. **The device's GLOBAL page decides.**
- **Memory (device build):** pool 273,820 → 271,772 B (the chorus's line gone). RAM +288 B. Image +2.9 KB.

## For your ears, specifically

1. **Chord at 50 %.** The intermodulation of eight detuned saws is spitty. That is what a fuzzed chord does, but decide
   whether the 50 % chord is the sound you want, or whether chords need less gain than single notes.
2. **The top end.** Is 100 % enough fuzz on a single note, or too much? The range is one table (`tools/gen_tables.py`,
   `growl_tables`).
3. **TONE default (~4.5 kHz) and BIAS default (40).** Both are guesses at "a little" by number.
4. **The trim's 1.5 s.** Longer keeps more sustain; shorter matches loudness sooner. Listen to the bass riff at 100 %.
5. **"Gated" isn't built.** The brief says warmth → *gated* fuzz. This is warmth → fuzz. High BIAS and GROWL give a
   starved, asymmetric fuzz, but notes don't sputter out the way a starved transistor's do. Say if you want that.

## Reproduce

```
tests/drive/render.sh                                   # the host renders -> build/drive/
python3 tests/drive/analyze.py build/drive              # loudness, aliasing, sweep click candidates
python3 tests/drive/make_kit.py build/drive listen/drive   # this folder's WAVs and pictures
tests/drive/bitexact.sh REV                             # GROWL 0 == another revision, byte for byte
cc -O2 -Ifirmware/src -Ifirmware/gen -o build/drive/bench tests/drive/drive_bench.c -lm   # GROWL alone
```
