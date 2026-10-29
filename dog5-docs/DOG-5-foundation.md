# DØG-5 — PROJECT FOUNDATION (verified)

**Status:** verified against hardware manual, panel photo and the FM-1 firmware ecosystem, 16 Oct 2026.
⚠️ **27 Oct note:** the base-lock facts in §1–§2 and the UI map in §5 are SUPERSEDED by
`DOG-5-base-and-ui-decisions.md` (base is now OberVave v1.5.3, commit 7e1ccf9; 99 slots; 20-page UI). The
hardware constraints (§3), IP position (§4) and DSP targets (§6) stand. This document otherwise supersedes
the original "DØG-5 Initial overview" blueprint.

---

## 0. WHAT THIS IS

DØG-5 is custom firmware for the **M-VAVE FM-1**, an aggressive live-performance virtual-analog polysynth in
the spirit of late-1970s American polysynths — for garage psych and egg punk, for the band **DØGS**.

**Prime directive: TONE IS KING.** Features and presets are negotiable. Tone and functionality are not.
**Release intent:** primarily personal use, but **released free to the community** (GPL-3.0-only).

---

## 1. THE HARDWARE (confirmed)

| | |
|---|---|
| Device | M-VAVE FM-1 |
| SoC | **JieLi AC791N / WL82, pi32v2 CPU, dual core** |
| **FPU** | **NONE** |
| Flash | Single-bank, XIP (1 MB chip) |
| Screen | 1.54" TFT, **240 × 240** |
| Keybed | 27-key silicone, piano layout, per-key LEDs |
| Controls | MASTER pot + 7 × 360° encoders (SELECT, PRESETS, ALGORITHM, KNOB 1–4), 14 buttons |
| Audio | 3.5 mm stereo out, built-in speaker (auto-mute on headphone insert) |
| MIDI | USB-C, BLE, 3.5 mm TRS **IN** (opened in base 1.5.2) |
| Power | USB-C / 2000 mAh, ~12 h |

Panel layout (confirmed): LEFT = MASTER, SELECT, PRESETS, ALGORITHM, OCT−/OCT+. CENTRE = the TFT. RIGHT =
KNOB1–4 + the 12-button grid (FX SEL ENV LFO EDIT GLO / HOME SAVE ARP SEQ PLAY REC). Key is printed **GLO**,
not GLD. Native polyphony is **12**; a 5-voice default is our deliberate choice (now a variable `P_POLY_N`
1–8, default 5 — see base-and-ui-decisions §5.2).

**The structural fact:** the FM-1 has no VCF/ADSR/subtractive path stock — it is pure 6-op FM. DØG-5 is a
**full replacement of the voice**, inheriting the chassis (panel, screen, keybed, storage, USB/MIDI, update).

---

## 2. THE FORK — OberVave (⚠️ base now pinned at v1.5.3 — see base-and-ui-decisions)

Lineage: `Felucca (Kuroshita/Hügelton) → SLOOP (isod89) → Dinghy (zvenson) → OberVave`. OberVave is ~70% of
DØG-5: 2 osc/voice with hard sync + X-MOD, trapezoidal SVF (LP12/HP12/BP12/notch/LP24/SEM morph), two ADSRs
with analog RC curves, LFO, the **Vintage** per-voice-offset macro (the Vintage Slop, implemented correctly),
chorus/ping-pong-delay/Dattorro-plate FX, and the tap-a-button-page / hold-a-button-layer panel paradigm.
Host mode builds the whole synth on a computer (WAV + screen PNGs).

Rejected bases: Baud Girl (closed source), Felucca (too broad — 13 engines/4 tracks/sequencer/sampler),
Dinghy (minimal skeleton, our fallback), FM-106 (Juno architecture), Melodee (ships 200 Sequential programs —
IP exposure), Groove OS (paid/closed).

---

## 3. HARD CONSTRAINTS

- **NO FLOATING POINT.** Integers only, fixed-point throughout, tables generated at build time.
- **CPU and flash budget.** Dual-core but tiny. Reference binaries ~425–610 KB. Expected casualties in order:
  physical-model spring → cheaper algorithmic (committed: re-voiced plate toward spring, `REV_DIV 2` fallback);
  audio-rate Poly-Mod across all voices; voice count.
- **⚠️ Build with `-Os`, not `-O2`** (the USB-babble brick trap — see the brief and the preserved OberVave
  notes). **Do not overclock.**
- **Toolchain:** Linux x86-64 native (on macOS it ran in a Docker container; DØG-5 builds in a cloud Linux
  env, no Docker — see base-and-ui-decisions §1.4 and the brief §9). Toolchain: `tools/get_toolchain.sh` →
  `pkgman.jieliapp.com`; SDK: gitee.com/Jieli-Tech/fw-AC79_AIoT_SDK (AC79NN_SDK_V1.2.1_2023-12-13).
- **Brick safety:** USB rescue = hold OCT− at power-on (⚠️ unproven here). A second FM-1 is the backup.

### §3.5 THE BUDGET — RESOLVED FRAMING (measured)

Two independent pools that do not trade:
- **FLASH — not the binding constraint.** 1 MB chip; procedural art costs near-zero flash; 1-bit frames
  compress to ~1–2 KB with the LZ4 compressor; the engine already draws with primitives.
- **CPU TIME — a duty cycle, not a per-redraw µs slice.** `CPU <n>us` is the *audio* engine's per-256-frame
  (5.8 ms) cost, NOT a screen meter. A full redraw spans ~5+ audio blocks (~30 ms SPI). The art's budget is
  the fraction of wall-clock the audio IRQ leaves the main loop; heavier audio stretches the redraw (lower
  frame rate), never starves the audio. **The real bottleneck is the PANEL:** ST7789 240×240 on SPI, polled
  DMA, no framebuffer; cost = dirty area × update frequency. Keep repaints to small dirty regions; keep the
  field static. ⚠️ The DRAW RULE (brief §6): every draw-wait calls `app_idle()` so notes stay on time.
- **LEDs:** 27 keybed + 12 button LEDs are **monochrome**, matrix-scanned, individually addressable, 3
  brightness tiers. Not RGB (that's the SMK-37 Pro). A near-free second animation channel.

---

## 4. IP AND LICENCE

**GPL-3.0-only** (inherited, non-negotiable). Rules: never ship Sequential's patch data; never brand it a
"Prophet-5 clone" (use "inspired by the classic American polysynths of 1979–84" in docs only); credit the
lineage; screen art original. The real company "DOOHBOX" never appears — use **HOODBOX**. Presets are built
by ear as original homages from published patch sheets, not ported SysEx.

---

## 5. UI MAP (⚠️ SUPERSEDED by base-and-ui-decisions §4 — the 20-page map)

Historical target. The live map is in `DOG-5-base-and-ui-decisions.md` §4 and the brief §5. Key live points:
HOME = PERFORM; the knob readout is transient (Monologue-style); the bottom bar is number + name only; the
sequencer is deleted; hold-HOME shows a control map; page families remember their last page; OCT = octave.

---

## 6. DSP TARGETS

All fixed-point. Priority when the budget bites: oscillators → filter → VCA gate → slop → effects.
1. **Oscillators** — free-running phase, imperfect geometry, alias-tolerant hard sync.
2. **Vintage Slop** — stable per-voice offsets + slow random walk, one macro (0% solid → 100% dying tape).
3. **VCF** — 24 dB LP with saturation in the feedback path (OberVave's SVF LP24 + pre-filter drive).
4. **Poly-Mod** — per-voice; sources filter env, Osc B; dests Osc A pitch, filter cutoff.
5. **VCA** — true zero gate, hard-chop exponential release, gates the whole noise floor incl. effects
   (exception: ENV Drone Latch / HOWL holds it open → latched drones carry tape hiss + drive crackle).
6. **Psych Chain** — Preamp Drive (asymmetric clipper) → BBD Delay (free-ms, REC=tap-tempo, LP in feedback)
   → Spring Reverb (re-voiced plate, `REV_DIV 2` fallback) → Tape Degrade (wow, flutter, dropouts).

---

## 7. OPEN DECISIONS (status 27 Oct)

- [x] Base/toolchain/CPU framing — resolved (base-and-ui-decisions).
- [x] Voice count 5 vs 8 — resolved as a knob `P_POLY_N`, default 5.
- [ ] Hardware calibration — the colour hex values, dial ceilings, render-time readings: eyeballed/measured
      on the real FM-1 when it arrives (feeds v1.1).
