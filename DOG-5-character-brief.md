# DØG-5 — CHARACTER & WORLD BRIEF (v2 — rebuilt)

**Status:** v2, 19 Oct 2026. Rebuilt around the locked character and the beam decision. **Supersedes the
reaper/sorcerer/Fifth-Seal layer** in `DOG-5-art-direction.md` §1–§2, §4–§5, the grimoire layer in
`DOG-5-narrative-library.md`, and the reaper assets in `DOG-5-asset-library.md` §2.

**Untouched by any of this:** every SOUND brief, the locked 32 and their names, the A/B bank, the Psych
Chain, the four procedural engines, the four colours, the four motions, every per-patch dial row, the
dirty-area budget, the draw-priority order, the strobe clamps, and all IP/licence work. **TONE IS KING
stands.** This is packaging and on-screen art only.

**Scope right now: FIRMWARE ONLY.** The screen, the character on it, the four scenes as they render on
the 240×240 panel, the controls, the UI. All physical/print output (posters, cards, zine, toys, release
art) is parked by Vincent's instruction — recorded where decided (§7), not built here.

---

## DECISIONS LOG (provenance)

- **THE LOGLINE:** *the runt bastard no one wanted.* POLY 5 — fifth of the litter, and he got out anyway.
- **THE DOG IS DRAWN** — Vincent's own sketch (AI pass used as a visual target only; hero art is always
  hand-finished, never shipped AI). The four-legged cur, not the biped cyclops.
- **DØG-5 is his name** — not a designation over another name. Machine and dog are one thing.
- **The scope is a free beam, no container** — the bark balloon is dead.
- **Mouth is the only major dog animation** (+ a slow idle sway, silence-only).
- **Identity lives in a protected bottom UI bar**, not a tag.
- **FX alarm = the nose.** Wonky stacked eyes kept, freed of duty.
- **Scenes:** Jalopy · Bee-tch · Moonshine · Le Gato.
- **Two palettes:** screen stays one-spot-on-black (hardware-locked); print/physical goes full multicolour
  (Vincent's hand) — parked.
- **[27 Oct update] Moonshine's spot colour: purple is OUT, hot bubblegum magenta `#FF2FA0` is IN** (see
  `DOG-5-base-and-ui-decisions.md` §6). The scene's character is unchanged; only the colour.

---

## 0. THE TWO HARD RULES (every proposal is tested against these)

1. **READS AS DØGS** — bubblegum egg punk. Gross-cute juxtaposed with ditsy-sweet: menace delivered as
   stupidity. The visual "TONE IS KING." If a frame makes you go "aw" with no second beat, it's wrong.
2. **READS LIKE NO ONE ELSE** — the style lane (vintage/rubber-hose/halftone) is shared; the *character*,
   Vincent's hand, and the bark-as-scope thesis are what carry uniqueness. Never the style alone.

---

## 1. THE THESIS

> **DØG-5 is a bark with a synthesiser bolted to it.**

The dog is **not a mascot**. He is a readout with four legs — made of the signal path, not reacting to it.
When you hit a key he barks, and **the bark is the live oscilloscope**: the real waveform of what's playing,
fired straight out of his open mouth. The sound you shape on the FM-1 is the sound of his bark. The 32
presets are 32 barks.

**THE BARK NEVER LIES.** The trace is always the honest signal — clean, white, readable, never stylised,
never corrupted, at every FLEAS setting. It is the one fixed true thing on the screen.

This beats the old "scrying orb" thesis because it needs no prop: the thing he *does* is the thing the
scope shows. One object, not a character plus a gadget.

---

## 2. THE GOVERNING MYTH — OVER THE FENCE

> **The mouth is the source. The screen's edge is the fence. The art is what happens between.**

The HUD is the fence keeping him in the yard — status, poly count, battery, borders. The bark always goes
**over the fence**, and the fence is always failing and being put back up (U1 unchanged), because a dog
does this every day, forever. A standing argument, not a demolition.

**The release meta-narrative, intact and warmer:** *the release is the dog getting out* — free, GPL,
uncontained, loose in the street. Every future artifact is evidence he got out.

**The signal law, unchanged:** *if it isn't driven by signal, it isn't art — it's wallpaper. Cut it.*

**The identity law, unchanged in force:** *the bark may knock the status about, never the name.* Now
physical: the fence (top) breaks; the bottom bar (identity) is sacred (§4.3).

### Renames (the figure-neutral spine kept, re-skinned)

| Old | New | Note |
|---|---|---|
| The Fifth Seal | **Over the Fence** | Same mechanic, same U1–U4 |
| The seal (HUD) | **The fence** | Destructible, heals; lives at the TOP |
| The 5th quadrant | **Over the fence** / the gap | Edge where the bark gets out; U2 unchanged |
| The orb (contained trace) | **The beam** (§4.2) | No container; truth + emission in one |
| The banner / tag | **The bottom bar** (§4.3) | Protected UI strip; cheaper, more legible |
| The Gloom dial | **FLEAS** (§6.1) | Same four stages, same safety clamps |
| The icosahedron relic | **The wheelie bin** | The pristine thing that gets wrecked — now in Le Gato |

---

## 3. THE DOG

### 3.1 Who he is

**DØG-5. The runt bastard no one wanted.** Fifth of the litter — POLY 5 — and he got out anyway. That's
the backstory, the hook and the tagline in one. The number is the name; the machine and the dog are the
same thing. There is no "breed": when asked what he is, the honest answer is *whatever the hell this is.*
A Cape Town street cur mixed past the point of category.

### 3.2 The locked design (from Vincent's drawing)

A four-legged cur, carried by a heavy black keyline. The consistent cues — the things that must appear in
every drawing of him and survive into the reduced builds:

- **The spiked back** — a row of standing spines down the ridge. The silhouette-maker.
- **The stacked wonky eyes** — mismatched, piled, pointing slightly wrong. The face's character, and now
  freed of any job (the FX alarm moved to the nose), so they can just be weird.
- **The lolling tongue** and **too many teeth** — the gross-cute payload. The mouth is maximalist.
- Dense hatched fur that thresholds straight to 1-bit dither (already proven in the render).

More "wrong" features will keep arriving from Vincent's hand and get folded in as they recur — the rule is
consistency, not a closed list.

### 3.3 Three tiers of the figure (this is the real production structure)

1. **HERO** — the full drawing, all detail. Print, release, the casting pose. (Parked for now.)
2. **FIRMWARE BUILD** — readable as 1-bit halftone at 240px with the field and UI around it. The render
   already proves this tier holds up; interior detail survives as dither. This is the tier the rebuild targets.
3. **FAVICON = THE HEAD** — the reducible mark. His head alone, stripped to the fewest cues that still read
   as him (spiked ridge + stacked eyes + snout). Replaces the dead orb glyph as the favicon-scale logo.

### 3.4 Animation (firmware)

- **Mouth open/close is the only major animation**, gate-keyed: note-on opens the mouth and fires the beam;
  note-off shuts it and the beam retracts. The gate made visible.
- **Idle sway** — in silence only, he rocks slowly side to side (~2-second rock, a pixel every few frames).
  Note-on kills it instantly; sway and beam never draw together. Lowest draw priority, first dropped under
  load. Positional motion only (no flashing) → inside the strobe clamp. *(Also suppressed while PRESETS is
  being turned, so navigation stays still — 27 Oct.)*

### 3.5 Uniqueness traps — the do-not list

Avoid the famous-cartoon-dog tells: pie-eyes + white gloves (Cuphead/Bendy), white dog with black
ears/patch (Snoopy), droopy basset (Droopy), blue-heeler colouring (Bluey), brown-with-black-spots Great
Dane (Scooby), the generic collar-plus-one-expression dog. This creature collides with none of them.

---

## 4. THE SCREEN

### 4.1 Staging

| Element | Position | Treatment |
|---|---|---|
| **The dog** | Left third, 3/4 profile, head up | Solid black + heavy keyline; spiked back, stacked eyes in silhouette. Inverts near-white in Moonshine |
| **The beam** | From the open mouth to the scene's fence corner | **The scope.** Straight white live trace. The one honest thing |
| **The impact + shed** | Where the beam lands on the fence | Scene colour, moving. Where per-scene character lives (§5) |
| **The bottom bar** | Full-width bottom strip | Preset number + name. Protected, un-breakable |
| **The fence (HUD)** | Top bar + perimeter | Poly count, battery, status. Destructible. All fracture zones up top |
| **The field** | Background | Static dithered scene, per-scene. Drawn once |

**SOURCE → EMISSION → EXIT** survives: mouth → beam → over the fence.

### 4.2 The beam

No container. The live oscilloscope trace shoots straight from the mouth to the scene's fence corner like a
bolt — both the truth channel and the emission in one. Zero-crossing trigger (~20 lines of C, already in the
base), diagnostic-by-design, patch-identity-by-silhouette, FLEAS never touches it.

**The one hard law:** it reads as a scope **only while it flies straight** (linear time-axis). Never curved,
arced or polar. ⚠️ Its jaggedness must BE the waveform, not stylised lightning on top. An aggressive patch
looks like a lightning bolt for free because the signal is violent.

**Cost:** gate-keyed — mouth shut, no note, no beam (cheap at rest). Give the mouth enough run to the corner
to show a cycle or two; strokes ≥2px. The knob-turn readout flashes in the bottom bar then falls back.

### 4.3 The bottom bar

Full-width strip carrying **preset number + name** (e.g. `17 TITANIC`) and the transient knob readout. Cheap,
maximally legible, no footprint cost to the scene. **Dedicated, un-breakable:** the breakable fence stays at
the TOP; top breaks, bottom is sacred. Draw priority: 1. beam trace (never dropped) 2. bottom bar (never
dropped) 3. fence (status) 4. impact/shed 5. field + FLEAS + idle sway (first out).

### 4.4 Scrapped outright

The orb and the bark balloon; the tag; the cowl/skull/skeletal hands/raised-arm staging; the Santa
Cruz/O'Brien composition reference and its entire IP-boundary section; the grimoire, the five incarnations,
the doomed-sorcerer backstory; the control spellcraft (replaced §6); "Bakshi rotoscoped rot" as the texture
thesis (replaced §7); the tarot-suit deck mapping.

---

## 5. THE FOUR SCENES — THE WALK

He gets out, and the walk gets progressively more out of hand. He does not come home. The four engines,
colours, motions, pixel-ops, dial ranges and per-patch rows are untouched — only what they depict changes,
and the per-scene character lives in the impact + shed + colour, not the beam's path (the beam always flies
straight).

| Ch | Scene | Colour | Verb | Pixel-op | Impact motion | Music |
|---|---|---|---|---|---|---|
| **I** | **JALOPY** | Acid green `#39FF14` | SCORCHES | Deletes — chars the fence from an edge in | beam → top-right; char + sparks from impact | egg punk / garage psych |
| **II** | **BEE-TCH** | Abyssal cyan `#00C8D4` | SOAKS | Covers — dithered mass hides the fence, drains | beam → top; flood pours DOWN from landing | surf / skinhead reggae |
| **III** | **MOONSHINE** | Bubblegum magenta `#FF2FA0` | FOGS | Dilutes — rising dither drowns the fence in grain | beam held (the howl); fog blooms & rises | drones / atmosphere |
| **IV** | **LE GATO** | Golden amber `#FFBF00` | WRECKS | Displaces — fence fractures into falling shards | beam strikes → debris falls down right margin | the closer / signature |

**5.1 JALOPY (Fire):** acid green behaves electrically — backfiring exhaust, toxic green fumes, blown muffler.
Bark detonates top-right and scorches the fence; green sparks shed from impact. *Field:* hot tar road, kerb,
a car arse leaving frame. Static.

**5.2 BEE-TCH (Water):** a dog barking at the sea. The bolt flies straight to the top and the flood pours down
from the landing point, then drains. Surf/reggae, the spring (DRAIN) chapter. *Field:* flat cold Cape horizon,
low dithered sea band, kelp. Static.

**5.3 MOONSHINE (Air) — the howl chapter:** the drone-latch chapter. A held note is a howl — head back, mouth
open, the beam shows the slow drone while fog blooms and rises to dilute the fence. The figure inverts to
near-white (lit by the moon); magenta only in the cold breath rising off him. Strobe hotspot: fog is animated
dither, so the 2px-lattice / every-3rd-frame / blue-noise rules apply at every FLEAS setting here. *Field:*
bleak night, far horizon, the moon as the one static white disc. Static.

**5.4 LE GATO (Earth) — the closer:** knocked-over bins, rattled fences, pots off the wall — and the cat on
the wall, unbothered. Amber = dusk, rust, old brass. The wheelie bin is the pristine relic that gets wrecked
(31 Fi(l)fth puts it over; 32 Init bruv? has it standing). 30 THE DØG keeps its seismic judder + full keybed
flash — the bark that finally shifts the cat. *Field:* back alley, wall, bin, washing line, cat in silhouette.
Static.

**5.5 On the 32 names:** don't force all 32 into one rigid frame. A found lexicon in the band's real voice.
The scene gives each chapter its arc; the names are its vocabulary, implied not enforced.

---

## 6. THE CONTROLS (all kept — function unchanged, names are the dumb-dog register)

| Panel | Function | Name | | Panel | Function | Name |
|---|---|---|---|---|---|---|
| ALGORITHM | Vintage Slop | **SLOBBER** | | LFO | Cyclic mod | **PANT** |
| ENV | Drone Latch | **HOWL** | | SAVE | Store patch | **BURY** |
| SEQ | Tape Stop | **FLOP** | | EDIT | Param pages | **DIG** |
| PLAY/STOP | Global kill | **HEEL** | | SEL | Reorder FX | **FETCH** |
| REC | Tap tempo | **WAG** | | PRESETS | Patch select | **BARKS** |
| GLO | Degradation | **FLEAS** | | HOME | Main screen | **HOME** |
| ARP | Arpeggiator | **ZOOMIES** | | | | |

**Psych Chain (FX):** K1 Drive = **GROWL** · K2 BBD Delay = **ALLEY** · K3 Spring = **DRAIN** · K4 Tape =
**CHEW**. **A/B bank:** A (locked originals) = **THE POUND** · B (live set) = **THE PACK**.

*(Note, 27 Oct: SEQ/FLOP goes with the deleted sequencer; the renamed-control legibility problem is solved by
the hold-HOME control map adopted from Skiff — see `DOG-5-base-and-ui-decisions.md` §4.4.)*

### 6.1 FLEAS — four stages (same thresholds + all safety clamps)

| % | Stage | Behaviour |
|---|---|---|
| 0–15 | **CLEAN** | Razor-sharp static 1-bit |
| 16–65 | **ITCH** | Line boil, edge jitter — 2px lattice, every 3rd frame |
| 66–90 | **SCRATCH** | X-axis scanline shear, even pixel steps only |
| 91–100 | **MANGE** | Dropped frames, HUD scramble, mustard infection |

FLEAS never touches the beam.

---

## 7. THE LOOK — TWO SYSTEMS

- **THE SCREEN** — hardware-locked: 1-bit, one chapter spot colour on black, static field. This is what the
  firmware builds.
- **PRINT / PHYSICAL** — full multicolour, Vincent's hand. A deliberately different system from the screen.
  **Parked.**

Carried over: 1-bit as a material (screen), the black keyline law, white = information, dither for tone,
degradation as aesthetic, caused-not-decorated, the 6-frame chunk, the sacred slashed Ø, every safety clamp.
In: Vincent's own marker-and-ink hand, vintage print grime folded in as seasoning.

---

## 8. HONEST RISKS

1. **The reduction is the hard part now, not the hero.** Getting the maximalist drawing to read as a solid
   mark at favicon size, and keeping the signature cues consistent, is the real work.
2. **Style lane is shared.** The dog's wrongness, your hand and the bark thesis carry uniqueness; the style
   never will. Mind the §3.5 traps.
3. **Cute is the failure mode.** Bubblegum without menace is a kids' brand. Every frame needs the second beat.
4. **Scope is real** — re-skinning the lore, controls, four scenes and 32 ART briefs is days, not hours.

---

## 9. NEXT STEPS (firmware only)

1. Lock the firmware-tier figure (the drawn cur reduced to a clean 1-bit 240px build; hero + favicon derived).
2. Draw the beam — straight bolt from the open mouth.
3. The bottom bar — number + name; un-breakable.
4. JALOPY first as the proof scene.
5. Re-skin the 32 ART briefs — mechanical pass.
6. (Design system: rebuild fresh from this brief — the old one was deleted.)
