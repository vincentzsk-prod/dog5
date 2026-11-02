# ALLEY — listening kit

ALLEY is the BBD delay, stage 2 of the Psych Chain (`firmware/src/obv_fx.h`): OberVave's ping-pong delay re-voiced as
a bucket brigade. Everything here was rendered by the host build (`tests/host.c`), which runs the firmware's own
integer code, so these are the samples the FM-1 would send over USB with MASTER all the way up. 16-bit stereo,
44.1 kHz, from just before the first note.

What stood before the re-voice, and the answers to the step-0 questions (buffer, CPU, the clip): [STEP0.md](STEP0.md).
**One correction to STEP0** is at the end of this file.

**Headphones help with the tails.** A delay adds energy only where the dry is silent, so unlike GROWL and CHEW there
is no loudness to hold. Listen for the repeats.

## Where it sits

`voices → GROWL → output stage → ALLEY → reverb (old plate) → CHEW → out`, the brief's order. Nothing moved: ALLEY
is the delay, in the delay's place.

## The controls

| where | knob | byte / CC | what |
|---|---|---|---|
| BBD DELAY, KNOB 1 | **ALLEY** | 68 / CC 87 (new) | the time. **0 = SYNC** (the note value below, at the tempo, as the old delay). 1–127 = free, **10 ms … 740 ms**, 3.5 % a step |
| BBD DELAY, KNOB 2 | FEEDBK | 56 (as before) | the old law (×250) up to 112. Above it the loop **holds at ~120** and **runs away** past it |
| BBD DELAY, KNOB 3 | TONE | 57 (as before) | the old one-pole in the loop: each repeat darker than the last |
| BBD DELAY, KNOB 4 | MIX | 58 (as before) | up to 0.70 of the dry. **0 = the old delay's bypass, bit for bit** |
| SELECT held (BBD +), KNOB 1 | SYNC | 55 (the old TIME byte, renamed on screen) | the note value ALLEY 0 follows. Turning it **puts ALLEY back on SYNC** |
| BBD +, KNOB 2 | FINE | 69 / CC 88 (new) | 1/128 of an ALLEY step. A tap sets it, so a tapped time is exact |
| BBD +, KNOB 3 | PINGPONG | 70 / CC 89 (new) | 0 = mono repeats (a BBD's), 127 = the old ping-pong (default, so old patches sound as placed) |
| **REC (WAG)** on the page | tap | — | the time between taps (the mean of the last 3). The REC LED is lit on this page |
| FX held, KNOB 4 | ALLEY | — | was the old TIME (note value); now ALLEY, free |

**No byte or CC moved.** Bytes 68–70 are appended; 71–79 stay free.

**The hand-over between free and SYNC** is designed so the echo never jumps:
- Turning ALLEY on a synced patch starts from the free step nearest to the time you hear (the 1/8. at 120 BPM, 375 ms,
  is step 107; one detent makes it 108).
- Turning FINE does the same.
- Turning SYNC (on BBD +) goes back to synced.
- A tap goes free.
- **CC 87 at 0 is SYNC**, by the byte's meaning, so a CC sweep to the bottom snaps to the note value. That is the one
  place the time can jump. Flagged.

**The tap.**
- Taps more than 2 s apart start again. A tap more than 30 % off the last interval starts a new tempo.
- The time is the mean of up to 3 intervals.
- Slower than 740 ms (a quarter below 81 BPM), it **folds to its 8th** (1000 ms taps give 500 ms).
- Measured: four taps 500 ms apart give ALLEY 115 + FINE 66, and an impulse's echo arrives **500.09 ms** later (the BBD
  filters delay it by ~0.1 ms).
- The host test `tests/bbd_page.txt` checks every step of this.
- The screen shows the time on KNOB 1. The fold's "/2" is in a toast, but **toasts are only drawn while a layer is
  held** (that is how the UI works today; the transient readout is Stage 3), so for now you'd only see the knob's value.

## The files

| source | what it is |
|---|---|
| **stab** | a short Cmaj7 stab (150 ms), twice, 2.5 s apart (INIT, POLY: two detuned saws a voice) |
| **bass** | program 1 *Red Pill* as voiced: one bar of the GROWL/CHEW kits' 8th-note riff on A1, then silence |
| **lead** | a bright mono lead, filter wide open: G5 A5 C6 short, then E5 |
| **slap** | program 11 *Slapback Strut* as voiced: quarter notes at 120 BPM, short |

| setting | ALLEY | FEEDBK | TONE | MIX | PINGPONG |
|---|---|---|---|---|---|
| **dbl** (doubling) | 25 ms | 0 | 127 | 64 | 0 (mono) |
| **slap** (slapback) | 90 ms | 15 | 100 | 90 | 0 |
| **sync** | SYNC 1/8. (375 ms at 120) | 60 | 70 | 70 | 127 |
| **long** | 600 ms | 85 | 70 | 70 | 127 |
| **runaway** | 300 ms | 124 | 90 | 60 | 64 |

| source | dry | dbl | slap | sync | long | runaway | **sync on the OLD delay** |
|---|---|---|---|---|---|---|---|
| stab | [▶](stab_dry.wav) | [▶](stab_dbl.wav) | [▶](stab_slap.wav) | [▶](stab_sync.wav) | [▶](stab_long.wav) | [▶](stab_runaway.wav) | [▶](stab_sync_OLD_DELAY.wav) |
| bass | [▶](bass_dry.wav) | [▶](bass_dbl.wav) | [▶](bass_slap.wav) | [▶](bass_sync.wav) | [▶](bass_long.wav) | [▶](bass_runaway.wav) | [▶](bass_sync_OLD_DELAY.wav) |
| lead | [▶](lead_dry.wav) | [▶](lead_dbl.wav) | [▶](lead_slap.wav) | [▶](lead_sync.wav) | [▶](lead_long.wav) | [▶](lead_runaway.wav) | [▶](lead_sync_OLD_DELAY.wav) |
| slap | [▶](slap_dry.wav) | [▶](slap_dbl.wav) | [▶](slap_slap.wav) | [▶](slap_sync.wav) | [▶](slap_long.wav) | [▶](slap_runaway.wav) | [▶](slap_sync_OLD_DELAY.wav) |

**The A/B with the old delay:** the "sync" column and the last one use **the same patch bytes** (SYNC 1/8., FEEDBK 60,
TONE 70, MIX 70). This is what the 8 factory patches that use the delay will sound like; see "factory patches" below.

**The demonstrations:**
- [tap_bass.wav](tap_bass.wav): the bass riff looped (8ths at 120 BPM), on the BBD page, with REC tapped. First 4 ×
  500 ms (a quarter: the echo lands on the beat). At ~4.4 s, 4 × 375 ms *while the repeats ring*, so the repeats bend
  to the new time. At ~8.4 s, 3 × 1000 ms, which folds to 500 ms, so the repeats bend back.
- [sweep_lead.wav](sweep_lead.wav): the lead's phrase at FEEDBK 95. KNOB 1 turns ALLEY down 30 steps (one every 80 ms)
  while it rings, then back up. This is the classic BBD "time knob" warble.
- [sweep_runaway.wav](sweep_runaway.wav): the stab once at FEEDBK 124 (runaway), then ALLEY swept down 40 and up 55
  steps while it sings (the spaceship), then FEEDBK pulled back to 100 to let it die.
- [sine1k_echo_time_changes.wav](sine1k_echo_time_changes.wav): the echo alone of a 1 kHz sine (FEEDBK 0, −12 dBFS):
  one knob step, a dive (103 → 395 ms) and a rise (395 → 42 ms). The pitch picture below draws it.

**With GROWL and CHEW** (sync, or runaway at the top; `_no_alley` is the same chain without ALLEY, for the A/B):

| source | GROWL 50 + ALLEY | ALLEY + CHEW 50 | GROWL 50 + ALLEY + CHEW 50 | the same, no ALLEY | GROWL 100 + ALLEY runaway + CHEW 100 | the same, no ALLEY |
|---|---|---|---|---|---|---|
| stab | [▶](stab_growl50_sync.wav) | [▶](stab_sync_chew50.wav) | [▶](stab_growl50_sync_chew50.wav) | [▶](stab_growl50_chew50_no_alley.wav) | [▶](stab_growl100_runaway_chew100.wav) | [▶](stab_growl100_chew100_no_alley.wav) |
| bass | [▶](bass_growl50_sync.wav) | [▶](bass_sync_chew50.wav) | [▶](bass_growl50_sync_chew50.wav) | [▶](bass_growl50_chew50_no_alley.wav) | [▶](bass_growl100_runaway_chew100.wav) | [▶](bass_growl100_chew100_no_alley.wav) |
| lead | [▶](lead_growl50_sync.wav) | [▶](lead_sync_chew50.wav) | [▶](lead_growl50_sync_chew50.wav) | [▶](lead_growl50_chew50_no_alley.wav) | [▶](lead_growl100_runaway_chew100.wav) | [▶](lead_growl100_chew100_no_alley.wav) |

## What ALLEY does, measured

### The repeats: a BBD's band-limit, falling with the time

Each pass through the line goes through a 2-pole (Q 0.8) and a 1-pole low-pass at the same corner. That corner falls
as the time grows (8 kHz at 10 ms → 2.8 kHz at 740 ms), because a BBD has a fixed number of buckets: a longer delay
is a slower clock. TONE (the old one-pole) then darkens every repeat after the first. An 80 Hz high-pass in the loop
thins them. [repeats.png](repeats.png) draws it.

An impulse, FEEDBK 100, each repeat against the impulse (MIX and PINGPONG taken out):

| ALLEY | repeat | −3 dB at (TONE 127: the BBD alone) | −3 dB at (TONE 70, default) | 100 Hz | 5 kHz (TONE 70) |
|---|---:|---:|---:|---:|---:|
| 10 ms | 1 | 7,064 Hz | 7,064 Hz | −0.2 dB | −1.3 dB |
| | 3 | 4,930 | 1,875 | −10.5 | −20.4 |
| 75 ms | 1 | 4,644 | 4,644 | −0.2 | −4.0 |
| | 3 | 3,297 | 1,759 | −9.8 | −27.4 |
| 294 ms | 1 | 3,152 | 3,152 | −0.2 | −10.2 |
| | 3 | 2,256 | 1,562 | −10.7 | −49.5 |
| 740 ms | 1 | 2,381 | 2,381 | −0.2 | −16.7 |
| | 3 | 1,674 | 1,320 | −10.5 | −48.6 |

The mids lose ~2.8 dB a pass at FEEDBK 100 (0.76). The lows lose ~5 dB a pass, so repeats thin out rather than boom.

**Against the old delay at the same bytes** (the echoes alone after the stab, [spectrum_old_vs_alley.png](spectrum_old_vs_alley.png)):

| | 0.1–1 kHz | 1–4 kHz | 4–8 kHz | 8–16 kHz |
|---|---:|---:|---:|---:|
| stab, ALLEY − old | −1.1 dB | −1.4 | **−12.6** | +0.3 (both at the floor) |
| lead, ALLEY − old | −0.4 | −0.7 | **−10.8** | **−28.9** |

So the body is the same and the top is gone. The old delay's first repeat was full-band (its TONE only worked from the
second repeat on).

### The headroom

One repeat (FEEDBK 0) of a 200 ms 1 kHz burst, measured once the dry has stopped:

| input | echo gain | H3 | H5 |
|---|---:|---:|---:|
| −20 dBFS | −0.19 dB | −84 dB | −83 dB |
| −12 dBFS | −0.22 | −61 | −92 |
| −6 dBFS | −0.32 | −48 | −101 |
| 0 dBFS | −0.70 | **−37** | −77 |

The line writes `tanh(u/2)` at half level: unity for small signals, a ceiling at 2× full scale. Repeats going round
also pass a tanh at full level, so they grit up as they build and a runaway settles under full scale. It is symmetric,
so odd harmonics only.

### FEEDBK's top: hold, then runaway

A 440 Hz burst, then FEEDBK held (80 ms, MIX 127). The echo's RMS in dBFS; [self_oscillation.png](self_oscillation.png):

| FEEDBK | 1 s | 3 s | 6 s | 10 s | 19 s | peak |
|---|---:|---:|---:|---:|---:|---:|
| 100 | −38 | −79 | — | — | — | −9.4 |
| 112 (the old law's last value) | −32 | −56 | — | — | — | −9.4 |
| 116 | −25 | −36 | −50 | — | — | −9.4 |
| 118 | −23 | −28 | −33 | −39 | −56 | −9.4 |
| **120** | −20 | −22 | −22 | −22 | −22 | −9.4 (holds) |
| 122 | −18 | −18 | −18 | −17 | −16 | −9.0 |
| 124 | −16 | −16 | −15 | −15 | −14 | −7.0 |
| 127 | −14 | −13 | −13 | −12 | −11 | **−5.2** |
| 127 at 740 ms | −26 | −21 | −19 | −22 | −22 | −5.3 |
| 127 at 10 ms, TONE 127 | −7 | −7 | −7 | −7 | −7 | −4.5 |

- The old FEEDBK reached 0.97 at 127 and never oscillated. ALLEY keeps the old values up to 112 (all factory patches are
  at 62 or below), then runs on to 1.25.
- The loop loses ~0.3 dB a pass (the filters, TONE), so the hold is near 120, not at unity.
- Above that it grows slowly. At 19 s it is still creeping up ~1 dB, settling under −5 dBFS.

### A time change: the BBD bend, no click

**What I chose: embrace the bend.** A real BBD's time is its clock, so turning the knob bends the pitch of everything
already in the line. That's the artefact people buy these pedals for, and the brief says "never a click live". A
digital delay that jumps its read clicks; one that crossfades smears. ALLEY moves its read like a clock:
- its speed changes at most by 0.5 in 23 ms (eased in);
- it heads for the new time over ~46 ms per step (eased out);
- it is capped at half speed (an octave down) while the time grows and 1.5× (a fifth up) while it shrinks.

A 1 kHz sine at FEEDBK 0 shows the read's speed as the echo's pitch ([time_change_pitch.png](time_change_pitch.png)):

| change | the echo's pitch | bent for | fastest bend |
|---|---:|---:|---:|
| one knob step (+3.5 %) | −1.9 semitones | 172 ms | 190 semitones/s |
| 103 → 395 ms (a jump) | −12.0 (held at the cap) | 725 ms | 610 |
| 395 → 42 ms | +7.0 (held at the cap) | 957 ms | 334 |

**No overshoot** (the pitch never crosses 0 the other way). The **old delay** switched its speed at once: a −12 / +7
semitone step in pitch in one sample, and back.

**Clicks.**
- **Method.** A 1 kHz sine's echo can only bend to 1.5 kHz, so anything at 2.5–7 kHz is an artefact. I measured that
  band in 2.9 ms frames against its own 120 ms median: a click is a spike.
- **Control.** The same echo with the time jumped at once (as a plain digital delay does), through the same kind of
  low-pass: **+37.8 dB**, the band 28.6 dB under the echo.

| ALLEY (FEEDBK 0) | worst spike | the band there, under the echo | frames over +6 dB |
|---|---:|---:|---:|
| jumps 80 → 120 → 20 → 127 | +5.0 dB | 70.0 dB | 0 |
| the time-change render above | +5.1 | 69.1 | 0 |
| swept 1 → 127 → 1, a step every 60 ms | +9.2 | **44.6** | 49 |

The sweep's worst moment is where it turns round (8.48 s): the read goes from half speed to 1.5× and the pitch swings
from −12 to +5 semitones in ~20 ms. That's the zip of a BBD clock yanked, 16 dB under the control click and not a
discontinuity. If it bothers you, the easing constant is one number (`32` in `fx_process`; 16 would make it 46 ms).
I used FEEDBK 0 on purpose: with feedback, a repeat is bent again on every pass and climbs into the band for real.
- **Why it can't click with feedback either.** Every element of the loop is continuous: the read position and its
  speed, the filters, the tanh. The filter coefficients change once per audio block as the time moves, and the sweep
  above covers that.

### Bypass, overflow, memory, CPU

**Bypass.** At MIX 0, ALLEY adds nothing: the output is the old delay's MIX-0 output, byte for byte.
- `tests/drive/bitexact.sh 9e8f638` is identical on 16 scripts: every factory program with the delay at 0, the UI
  scripts, and the GROWL and CHEW kits including CHEW > 0 and its sweeps.
- With the repeats still ringing at −17 dBFS when MIX drops to 0 (`tests/bbd/mix_off_ringing.txt`): **0 of 131,640**
  samples differ after the switch.

**Waking.** When MIX comes back after more than 12 s at 0, the lines are cleared. The old delay replayed whatever it
held, so a runaway left in the line would have come back.

**Overflow:** none, with this one exception.
- What ran clean under `-fsanitize=signed-integer-overflow,bounds`:
  - the bench at full scale (noise and a 60 Hz sine, ALLEY and FEEDBK jumped through everything, PINGPONG 0, TONE 127);
  - the whole synth in `tests/bbd/worst.txt`: 8-voice unison at VOLUME 127, GROWL and CHEW at 127, FEEDBK 127,
    ALLEY/FINE/PINGPONG/TONE/MIX jumped at random.
- ⚠️ **The exception: the reverb overflows** at REV_MIX/SIZE 127 with that input (`rev_tick`: the seven output taps
  summed, × 19,661). It happens on `main` too, with the old delay, so it is not ALLEY's. I left it alone, as asked:
  it belongs to the Spring re-voice. It is why `worst.txt` runs with the reverb off.

**Memory (device build).**
- Pool **275,868 B, unchanged.** The two 743 ms lines are the old delay's.
- RAM +96 B (32,304). Image +4,536 B (107,920: code and 1 KB of tables).
- No 64-bit division (the link has no `__divdi3`), `-Os`.

**CPU (host callgrind, instructions/sample while on):** ALLEY **310** (old delay 109).

| | before | after |
|---|---:|---:|
| GROWL | 742 | 741 |
| delay | 109 | **310** |
| reverb | 566 | 576 (the loop it shares is a call now) |
| CHEW | 961 | 961 |
| **all four** | **2,379** | **2,588** |

The breakdown and the levers are in `dog5-docs/PERF-BASELINE.md`.

### The kit's numbers

Energy against the dry render (ungated, the whole file), the peak in dBFS, and samples at full scale:

| source | dbl | slap | sync | long | runaway | old sync |
|---|---:|---:|---:|---:|---:|---:|
| stab | +0.5 / −4.4 | +0.5 / −5.3 | +0.3 / −5.3 | +0.4 / −5.3 | +2.9 / −5.3 | +0.4 / −5.3 |
| bass | **−0.5** / −14.2 | −0.1 / −12.8 | +0.3 / −13.1 | +0.2 / −12.8 | +0.6 / −14.2 | +0.2 / −12.9 |
| lead | −0.2 / −10.7 | +0.2 / −10.8 | +0.3 / −9.8 | +0.4 / −10.2 | +3.4 / −8.7 | +0.4 / −9.8 |
| slap | **−0.5** / −15.6 | +0.5 / −15.6 | +0.3 / −15.6 | +0.4 / −15.6 | +0.6 / −14.0 | +0.4 / −15.4 |

- **Nothing in the kit reaches full scale.**
- (Integrated LUFS is no use here: its relative gate reads sparse material with echoes as *quieter*. The old delay shows
  the same.)

## GROWL and CHEW together: what I found

| | what ALLEY adds | peak with ALLEY | peak without | at full scale |
|---|---:|---:|---:|---:|
| stab, GROWL 50 + sync + CHEW 50 | +0.3 dB | −12.2 dBFS | −12.2 | 0 |
| bass, GROWL 50 + sync + CHEW 50 | +0.3 | −12.8 | −12.9 | 0 |
| lead, GROWL 50 + sync + CHEW 50 | +0.3 | −12.8 | −14.9 | 0 |
| stab, GROWL 100 + runaway + CHEW 100 | +3.5 | −10.9 | −12.8 | 0 |
| bass, GROWL 100 + runaway + CHEW 100 | +1.2 | −12.5 | −14.4 | 0 |
| lead, GROWL 100 + runaway + CHEW 100 | +3.9 | −11.0 | −15.4 | 0 |

1. **The BBD strips GROWL's fizz from the repeats.**
   - GROWL 50 puts ~10 dB more energy at 4–10 kHz into the stab: −34.4 dB of the total, against −44.6 undriven.
   - The **first repeat is back to −43.6**, the top of an *undriven* stab. The second is at −55.8.
   - So the grit is in the dry note and the echoes are a warm ghost of it. That's what a fuzz into a real BBD does,
     and I think it's right.
   - If you want fuzzy repeats: TONE 127 and a short time keep the most top; the bandwidth curve is one table line.
2. **CHEW after ALLEY.**
   - The repeats and a runaway get wowed and hissed: the brief's "Tape last compounds slop + wow".
   - CHEW's hiss rests 2 s after its input falls silent, and ALLEY's tail *is* its input. So **a long FEEDBK keeps the
     hiss awake** until the repeats die, and a runaway keeps it on.
   - ALLEY's tiny DC (below) is under CHEW's silence threshold, so it does not hold the hiss on.
3. **No level surprises.**
   - GROWL and CHEW hold loudness and ALLEY's headroom works on the same level either way.
   - The combinations peak at most +4.4 dB above the same chain without ALLEY (the runaway on the lead), and nothing
     reaches full scale.
4. **Runaway + CHEW 100**: CHEW's wow wobbles the self-oscillation's pitch, a tape-echo sound on top of the BBD
   ([lead_growl100_runaway_chew100.wav](lead_growl100_runaway_chew100.wav)). Listen to that one first. (I haven't
   measured how CHEW's 1.5 s loudness trim follows a runaway's slow climb, so listen for pumping there too.)

## The correction to STEP0 (the clip question)

In step 0 I predicted that ALLEY's self-oscillation would make the effects' over-full-scale sum ordinary. **It does
not:** the loop's own limit keeps a runaway under −5 dBFS. Measured with the same instrumented scratch build (samples
over ±32,767 before `fx_process`'s clip):

| case | over full scale | peak |
|---|---:|---:|
| every kit render, the runaway and GROWL 100 + runaway + CHEW 100 combos included | 0 | −4.4 dBFS at most (stab dbl) |
| 6-note chord at velocity 127, ALLEY 294 ms, FEEDBK 127, MIX 127, reverb off | **0** | −0.01 dBFS |
| the same + reverb MIX/SIZE 127 | 2,718 of 793,600 (0.34 %) | +3.3 dBFS |
| the reverb alone at 127 (ALLEY MIX 0) | 13 | +0.26 dBFS |

So **what's left over full scale is the reverb's**. My recommendation stands (round the overs in CHEW's record stage,
not by removing the clip alone), but its timing changes: **do it together with the Spring re-voice**. That's the stage
that decides whether the sum can go over at all, and it's also where the reverb's overflow (above) gets fixed.

## Factory patches

No factory patch's bytes changed (`obv_patches.h` is untouched). New bytes take their defaults: ALLEY 0 = SYNC, FINE
0, PINGPONG 127 = ping-pong. So the 8 patches with the delay on keep their times, feedback, tone, mix and stereo, and
change only by the re-voice:
- a band-limited first repeat;
- the 80 Hz loop high-pass;
- the headroom (inaudible at their levels: H3 under −48 dB below −6 dBFS).

They are **04 V-Sync, 08 Wire Bite, 15 Trem Chop, 20 Fire & Ice, 24 Fugue State, 26 BSyncA, 28 Bell Tolls,
31 Fi(l)fth**. Their stab/lead equivalent is the "sync" column against "old".

## For your ears, specifically

1. **The darkness curve.** The first repeat is −3 dB at 4.6 kHz at 75 ms, 3.2 kHz at ~300 ms and 2.4 kHz at 740 ms.
   That's Memory Man territory. Too dark for the rhythmic delays (sync column), or right?
2. **The bend on a knob turn** (sweep_lead): −1.9 semitones a step. Character or seasick?
3. **The runaway** (sweep_runaway, *_runaway): the hold at ~120 and the climb above. Is the top loud enough, or too loud?
4. **The doubling on bass** (bass_dbl, slap_dbl): a 25 ms mono copy at half level is a comb with notches every 40 Hz
   from 20 Hz (−6 dB deep), which costs the bass −0.5 dB of energy. Doubling is for leads and stabs, not bass; I'd
   keep it out of bass patches.
5. **PINGPONG's default.** It stays 127 so the old patches keep their image. A *new* patch from INIT is ping-pong
   too. A BBD is mono; should INIT be mono?
6. **The tap's fold:** a tap slower than 740 ms gives its 8th. Would you rather it clamp to 740?

## Not done here, on purpose

- **Spring untouched**, including its overflow and the effects' clip (above).
- **The FX-held layer** is GROWL / BBD MIX / SPRING MIX / **ALLEY** (it was the old TIME, which ALLEY replaced, so it
  had to change). The brief maps it to GROWL / ALLEY / DRAIN / **CHEW**: CHEW isn't on it and the BBD's MIX is. That's
  your call. It was deferred by the Tape session too.
- **No modulation on the repeats** (the Memory Man's chorus/vibrato), no BBD clock noise, no compander "breathing".
  CHEW already brings wow and hiss after it. Ask if you want any of them.
- **A 1 s maximum:** +45 KB of pool, no CPU (STEP0.md). Not taken.
- **A tiny DC:** ALLEY's output carries +1 LSB of DC (−90 dBFS) while MIX > 0 (the third pole's rounding). It's
  inaudible, so I left it.

## Reproduce

```
python3 tests/bbd/make_scripts.py                    # the host scripts (tests/bbd/*.txt)
tests/bbd/render.sh                                  # host, old-delay and bench renders -> build/bbd/
python3 tests/bbd/analyze.py build/bbd               # every table above (--png DIR: the pictures)
python3 tests/bbd/make_kit.py build/bbd listen/bbd   # this folder's WAVs and pictures
tests/drive/bitexact.sh 9e8f638 tests/bbd/factory_nodly.txt   # MIX 0 == the old delay, byte for byte
for s in off dly all4; do tests/perf_callgrind.sh tests/tape/perf_$s.txt; done   # CPU
```
