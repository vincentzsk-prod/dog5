# DØG-5 — ART DIRECTION (procedural engine canon)

**Status:** approved 17 Oct 2026. ⚠️ **27 Oct:** the reaper/orb/Fifth-Seal *framing* (§1–§2, §4–§5 of the
original) is DEAD — the live world is the dog/beam/fence (`DOG-5-character-brief.md`). **The mechanics below
are canon and still used:** the four procedural engines, the dirty-area budget, the draw-priority order, the
colour registers, the safety clamps, the legibility floor. Read the character brief for *what it depicts*;
read this for *how it's drawn and budgeted*. Moonshine's colour is now **magenta `#FF2FA0`**, not purple.

---

## COLOUR — three registers by behaviour

| Register | Behaviour | Meaning | Where |
|---|---|---|---|
| **White** | Constant | Information | The beam/trace. Never tinted. |
| **Chapter colour — static** | Still | Identity | (minimal now; the dog is black keyline) |
| **Chapter colour — moving** | Travelling | Consequence | The impact/shed/emission |
| **Functional colour** | Flashing | Alarm | Event-driven, specific objects (the nose) |

Chapter identity colours: **Fire/Jalopy = acid green `#39FF14`**, **Water/Bee-tch = abyssal cyan `#00C8D4`**,
**Air/Moonshine = bubblegum magenta `#FF2FA0`** (was bruised purple — changed 27 Oct), **Earth/Le Gato =
golden amber `#FFBF00`**. Functional: Arterial Red `#FF0000` (FX / the nose), Hazard Yellow `#FFEA00`, Magma
Orange `#FF4500`, Radioactive Mustard `#CCCC00`. All final values eyeballed on the real panel.

**LEDs** are monochrome (brightness only): keybed = struck-key brightness tracing what you play (per-chapter
envelope character: Jalopy snaps, Bee-tch rolls, Moonshine holds, Le Gato thuds); pads = tempo pulse + FX/ENV
alarm. No idle wash. The ~3 Hz strobe clamp covers LEDs too.

---

## THE FOUR ENGINES — delete / cover / dilute / displace

| Ch | Element | Verb | Pixel operation |
|---|---|---|---|
| I Jalopy | FIRE | SCORCHES | **Deletes** — chars the fence from an edge inward, embers rise |
| II Bee-tch | WATER | SOAKS | **Covers** — a dithered mass occludes from the top, then drains |
| III Moonshine | AIR | FOGS | **Dilutes** — rising dither density drowns status in grain; structure stays |
| IV Le Gato | EARTH | WRECKS | **Displaces** — geometry fractures, shards fall, then re-fuse |

Four cheap engines, one nozzle, four materials. All **procedural** (code-drawn, near-zero flash).

### Common dials (every engine)
| Dial | Range | Function |
|---|---|---|
| `INTENSITY` | 0–255 | Material per note-on |
| `DENSITY` | 0–255 | Particle/mass count = **animated dirty-area per second — the cost dial** |
| `SPEED` | 0–255 | Travel rate |
| `DECAY` | 0–255 | Settle rate after the gate closes |
| `SEED` | 0–255 | RNG seed (no two patches move identically) |
| `BIAS` | vector | Which edge takes the hit (chapter-locked, U2) |

Engine-specific: FIRE `CHAR` (blacken persistence) · WATER `LEVEL` (resting waterline) · AIR `OPACITY` (max
dither density) · EARTH `SHARD` (fragment size). Each dial carries a per-chapter floor/ceiling.

### Signal bindings — "the beam never lies," made concrete
note-on → burst · VCA gate → sustain · envelope level → INTENSITY · filter cutoff → trace brightness /
emission fineness · drive → CHAR/SHARD aggression · LFO → wobble · tap tempo → pad pulse. Gate-keyed and
transient: settles at rest, erupts on strike, decays back.

---

## THE BUDGET — runtime, not storage

Two budgets that don't trade (full detail in `DOG-5-foundation.md` §3.5):
- **Flash — not the binding constraint.** Procedural art is near-zero flash; per-patch variation is a tiny
  parameter row, not a stored picture. You get four chapter languages AND per-patch variation.
- **CPU — a duty cycle; the panel SPI (dirty area × frequency) is the real cost.** Animate small regions
  (beam, struck-key sparks, impact near the mouth); keep the field static; full-field motion degrades first.

### Draw priority — graceful degradation = "eat status, never identity," one mechanism
Each frame draw in this order, stop when time runs out (also an area order, smallest/most-important first):
1. **The beam trace** — small, highest. Never dropped.
2. **The bottom bar + name** — small solid. Never dropped.
3. **The fence (status HUD)** — droppable.
4. **The impact / shed** — droppable.
5. **The field + FLEAS + idle sway** — largest, lowest, first to drop.
Throttle = per-frame quality tier from the last audio-cost reading + a mid-frame hard stop via `fm1_ticks()`.
⚠️ Plus the DRAW RULE: every wait calls `app_idle()` so notes stay on time (see the brief §6).

---

## FLEAS — four stages + hard safety clamps

| % | Stage | Behaviour + clamp |
|---|---|---|
| 0–15 | CLEAN | Razor-sharp static 1-bit |
| 16–65 | ITCH | Line boil — **2px lattice (never ±1), every 3rd frame at 20fps (~6–7 Hz)**, figure edges only |
| 66–90 | SCRATCH | X-axis scanline shear — **even pixel steps only**, horizontal pipeline dither |
| 91–100 | MANGE | Dropped frames (real, over-driven SPI), HUD scramble, mustard — **never touches the bar** |

**Hard clamps (compile-time):** no full-screen luminance swing faster than ~**3 Hz**, applied globally after
all effects compose (covers LEDs too; the Le Gato seismic judder is a positional shake, inside the clamp). FX
inversion: invert to dirty white ~70% coverage, never 100%, ramped over 2–3 frames. Dither: blue-noise over
regular grids. FLEAS never touches the beam. ⚠️ Moonshine/Air fog IS animated dither, so it runs these clamps
at EVERY FLEAS setting, not just the high ones; its slowness is the safeguard.

---

## LEGIBILITY FLOOR

Strokes ≥ 2px. Solid black/white objects over detailed interiors (the figure is a shape). The patch name sits
well above the 10px HUD floor on the bottom bar at max contrast. 20 fps is legitimate for chunky animation (the
6-frame Bakshi chunk is deliberate).

---

## WHAT DØG-5 IS NOT
Not a mascot/visualiser/loading screen. Not a game (no win state). Not pretty/clean — 1-bit is a material.
Not a screen you look at instead of your hands.

## OPEN — hardware calibration only
The four spot-colour hex values, the per-chapter dial ceilings, the `DENSITY`/`OPACITY`/`SHARD` caps and the
render-time/SPI numbers all finalise on the real FM-1. The relationships are locked; the absolute numbers wait.
