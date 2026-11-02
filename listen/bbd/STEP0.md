# ALLEY (BBD) — step 0: where the delay stands before the re-voice

Measured on `main` at `9e8f638` (GROWL and CHEW merged), before any ALLEY change.

## a. The delay today vs the brief

**Today** (`firmware/src/obv_fx.h`, OberVave's delay, untouched since the fork):

- **Ping-pong, two lines.** The input (L+R)/2 enters the left line. Each line's output is low-passed (TONE) and
  fed into the *other* line × FEEDBK. The left line's output goes to L, the right line's to R. **A single repeat (FEEDBK 0)
  is hard left.**
- **Time = a note value of the tempo only** (`P_DLY_TIME` 0..6: 1/16, 1/8T, 1/8, 1/8., 1/4, 1/4., 1/2), clamped to
  64 samples .. `DLY_MAX − 4`.
- **TONE** is a one-pole in the feedback path only: the first repeat is full-band, the later ones darker.
- **FEEDBK** = value × 250 (Q15): 0 .. 0.969 at 127, linear. No saturation in the loop, so it can't self-oscillate.
  The line write is a hard `sat16`.
- **A time change** slews the read at a constant ±0.5 sample per sample. The pitch jumps straight to +7 / −12
  semitones and jumps back at the end. That is a step in pitch, not a click.
- **MIX** = value × 180/128 (Q8): up to 0.70 of the dry, added on top of it.
- **Off:** the line keeps running 12 s after MIX reaches 0, then freezes. Its content stays and replays when MIX comes
  back. At MIX 0 nothing is added to the dry, so the output is the dry signal bit for bit.

**What the brief wants** (CLAUDE.md §6, DOG-5-presets.md §2):

- ALLEY = free-running ms (not note values).
- FEEDBK → 0.97 / self-oscillation.
- A BBD character on the repeats.
- REC = tap tempo.
- "Never a click live".

Missing today: free ms, tap, self-oscillation and any BBD colour. The TONE-in-feedback and the slewing read are
already there to build on.

**The buffer:**

- `DLY_MAX` = **32,768 samples a side = 743.0 ms** at 44.1 kHz.
- Two int16 sides = **131,072 B** of the pool.
- Pool today: **275,868 of 344,064 B** (68,196 B free). The device build, confirmed: `./build.sh` → image 103,384 B,
  RAM .data+.bss 32,208 B.

**Does free-ms need a bigger buffer?** No. Free time only changes how the read position is chosen, not how far
back it can reach. Only a *longer maximum* needs memory:

| maximum | how | pool | fits? |
|---|---|---:|---|
| **743 ms (now)** | two full-rate int16 lines | 275,868 B (+0) | yes, 68 KB free |
| 1.0 s | two lines of 44,100 | **321,196 B (+45,328)** | yes, but leaves 22.9 KB for Spring's re-voice and v1.1 |
| 1.5 s | two lines of 66,150 | 409,396 B (+133,528) | **no** (65 KB over) |
| 1.49 s, mono only | one line of 65,536 (the same 131,072 B) | +0 | yes, but no ping-pong |
| 1.49 s, ping-pong | both lines at half rate (22.05 kHz), with a decimator and interpolator | +0 (+a few hundred B of state) | yes, costs CPU (two halfbands a side) |

**Recommendation, taken in step 1: keep 743 ms** (free range 10–740 ms).

- It is already longer than the BBD pedals the sound is modelled on: Deluxe Memory Man ~550 ms, Carbon Copy 600 ms,
  DM-2 300 ms.
- Slapback, doubling and rhythmic eighths at 100–180 BPM sit well inside it.
- A tap slower than 740 ms (a quarter below 81 BPM) folds to its eighth (and so on), and the screen says so.
- If a song needs a full second, the 1.0 s row is the cheapest real extension: +45 KB, no CPU change, one `#define`.
  Spring's memory needs should be known first.

## b. The CPU running total today

Host callgrind, x86-64 instructions per sample while the stage is on. The scripts are `tests/tape/perf_*.txt`, the same
recipe as `dog5-docs/PERF-BASELINE.md`. Re-run here, the counts match that file to the instruction.

| stage | Ir | instructions / sample while on |
|---|---:|---:|
| everything off (the voices) | 267,119,336 | (713 over the whole window) |
| GROWL 100 | 489,681,266 | **742** |
| old delay (mix 60) | 299,859,888 | **109** |
| old reverb (mix 60) | 436,930,955 | **566** |
| CHEW 100 | 555,239,232 | **961** |
| GROWL + delay + reverb | 692,233,437 | 1,418 |
| **all four** | 980,408,818 | **2,379** (2,616 over the whole window, the voices included) |

## c. The two open questions from the Tape session

**1. Does Tape stay after the reverb?** **Yes.** The brief's order is VOICES → DRIVE → BBD → SPRING → TAPE → master,
and the engine already runs it that way: voices → GROWL → output stage → delay → reverb → CHEW. ALLEY keeps the
delay's place, so nothing moves. "Tape last compounds slop + wow" is the brief's intent, so the repeats and the tail
get wowed and hissed too.

**2. Should the effects' sum reach Tape before Tape's own clip?**

Today `fx_process` ends in `sat16` (a hard clip at ±32,767) and Tape starts after it. Tape's own path has two more
clips:
- the int16 line write in its record stage (`tp_sat` returns `sat16(...)`), at 2× rate;
- its final `sat16`.

So "Tape's own hard clip" is really the line write, and Tape's tanh only rounds peaks in proportion to CHEW's
saturation share. That share is `TP_SAT_Q12`, about 0.19 at 25 % and 1.0 at 100 %.

**How often does the effects' clip actually fire?** I measured it with an instrumented scratch build (not committed)
that counts samples over ±32,767 before `fx_process`'s `sat16`:

| renders | clipped samples | peak before the clip |
|---|---:|---:|
| all 32 factory programs (`tests/drive/factory_all.txt`) | **0** of 5,291,520 | −1.06 dBFS |
| every Tape kit render at CHEW 100 (4 sources), GROWL 100 + CHEW 100 (4), the CHEW sweep | **0** | −3.8 dBFS at most |
| stress: 6-note chord at velocity 127, old delay mix 127 / FEEDBK 110, reverb mix 127 / SIZE 127 | 216 of 793,600 (0.03 %) | **+1.8 dBFS** |

**Does changing it affect anything proven bit-exact?**
- **No.** CHEW 0 is a bit-exact bypass because the engine skips Tape. The clip would only move when Tape runs, so
  `fx_process` keeps its `sat16` while CHEW is 0, and every CHEW-0 and GROWL-0 proof stands.
- At CHEW > 0, the Tape kit itself would not change either, because none of its renders ever reaches the clip (above).
- What *would* change them is the second half of the fix below: a soft knee in Tape's record stage that starts under
  full scale. It would touch any CHEW > 0 render whose peaks pass the knee. With the knee at −2 dBFS, no current kit
  render is affected (their loudest is −3.8 dBFS).

**My recommendation: yes, do it, but as its own small step with its own proof, and not as a bare "remove the clip".**

- **Only removing `fx_process`'s `sat16` when Tape runs gains almost nothing.** The over would reach Tape's int16
  line write instead and be hard-clipped there. That happens at 2× rate (less aliasing), but it is still a hard
  clip, and at a low CHEW Tape's tanh barely touches it.
- **Doing it properly** has three parts:
  1. With CHEW > 0, `fx_process` hands Tape the unclipped sum, held to ±2× full scale as a safety rail (Tape's
     halfbands and its K-weighted detector, which assumes |L+R| ≤ 65,534, need that bound).
  2. Tape's record stage gets a knee: linear to −2 dBFS, then a tanh-shaped approach to full scale, whatever CHEW is.
     Tape then rounds every over at 2×, and its line never hard-clips.
  3. The detector input is clamped.
- **Why it's worth doing now, after ALLEY:** before ALLEY, the over only happened at extreme settings (the table).
  ALLEY's self-oscillation makes it ordinary: a runaway BBD at full mix plus a loud chord. Step 1 measures how far
  over it goes.
- **Why not without Tape:** the effects' clip stays when CHEW is 0. A soft knee there would change every render of
  every patch whose peaks pass the knee, the bit-exact bypass proofs included.

Not applied, as asked.
