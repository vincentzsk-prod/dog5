# DØG-5 — PRESET ARCHITECTURE & THE 32

**Status:** working draft, 16 Oct 2026. ⚠️ **27 Oct:** §1 (the A/B store) is SUPERSEDED — the base ships 99
slots, so A/B is now a **write-lock over slots 1–64 (THE POUND) vs 65–99 (THE PACK)**, not a store expansion.
The 32 SOUND briefs, the Psych Chain and the bank model below otherwise stand. Measured against the base
source (`obv_params.h`, `obv_patches.h`, `obv_fx.h`).

**Prime directive: TONE IS KING.** Ship fewer, better.

**Names (27 Oct):** field widened to 14 chars; four names changed — 09→**Skeenhead**, 17→**Titanic**,
18→**Roto-scopo**, 19→**Blackwater**. All others fit at 14.

---

## 0. HOW TO READ THIS

Every patch is split into two briefs acted on by different processes:
- **SOUND brief** → the patch generator reads this (engine terms → an 80-byte, soon 96-byte, patch struct).
- **ART brief** → the visual work reads this. Full realisation (engine, dials, LED, rows) is in
  `DOG-5-chapter-specs.md`, governed by `DOG-5-art-direction.md`. ⚠️ ART briefs are written in the old
  reaper/orb framing; the live world is the dog (see `DOG-5-character-brief.md`).

**Phase tag:** **P1** = buildable on the voice engine + existing/cheap effects · **P2** = defining character
needs the new Psych Chain (Drive and/or Tape).

---

## 1. THE BANK (⚠️ SUPERSEDED — write-lock over 99 slots)

Base ships `NPROG 99` (1–64 factory, 65–99 INIT), SAVE writes anywhere. DØG-5 adds a **write-lock**: slots
1–64 are **THE POUND** (write-protected factory/originals — fat-finger safety on a dark stage); 65–99 are
**THE PACK** (the live working set, where Vincent saves multiple dialled variations of a patch to jump
between live). The old "expand store to 64" plan is obsolete — 99 is more room than it asked for. Live
scroll skips empty INIT slots.

---

## 2. THE PSYCH CHAIN (locked — repurpose + extend)

`VOICES → [1 PREAMP DRIVE (new)] → [2 BBD DELAY (re-voiced)] → [3 SPRING REVERB (re-voiced)] → [4 TAPE
DEGRADE (new)] → MASTER VCA GATE`. Reached by FX; KNOB 1–4 = the four macros (GROWL · ALLEY · DRAIN · CHEW);
secondaries on SELECT-hold. Repurpose the 3 freed chorus slots (`P_CHO_*`) for Drive + Tape — no new storage.

| Knob | Effect | Primary | Secondary | Status |
|---|---|---|---|---|
| K1 GROWL | Preamp Drive (new) | Drive 0–127 (warmth→gated fuzz) | Bias/asymmetry | New — integer asymmetric soft-clip before `sat16()` |
| K2 ALLEY | BBD Delay (re-voiced) | **Free-running ms** time | Feedback (→0.97 self-osc) | Tone-in-feedback + tape-slew already coded; **REC = tap-tempo** |
| K3 DRAIN | Spring Reverb (re-voiced) | Mix | Size/decay | Plate's allpasses pushed → spring chirp. "Next closest thing," excellence not required |
| K4 CHEW | Tape Degrade (new) | Degrade (wow→flutter→dropouts) | Wow/flutter balance | New — reuses Hermite moving-tap reader + HF roll-off + micro-dropouts |

Baked in: BBD = free ms (never a click live); REC = tap-tempo. Spring = re-voiced plate (true waveguide NOT
attempted; `REV_DIV 2` half-rate is the documented CPU fallback — Chapter II leans on it most). Order
consequences: Tape last compounds slop + wow; HOWL (ENV latch) holds the gate so latched drones carry the
chain's hiss/crackle; HEEL (PLAY/STOP) flushes buffers to dead air; FLOP (SEQ tape-stop — note: goes with the
deleted sequencer, re-home this function) pitch-dives before the chain.

---

## 3. THE 32

Chapter I re-voiced: start from FAT sources (dual-osc, unison, low register) pushed into aggression via Drive
+ gate + slop — not born-thin single oscillators. Each entry: slot · name · [phase] · nearest base patch /
SOUND / ART.

### CHAPTER I — THE WASTELAND ARSENAL (egg punk & garage psych) — JALOPY
- **01 "Red Pill" · P2 · from FAT BASS** — SOUND: dual saws, slight detune, low register, filter low+resonant
  with bass-comp, hard-chop gate, driven into asymmetric clip. ART: chaotic acid-green arcs tear the right HUD.
- **02 "Cement Grind" · P2 · from WOBBLE BS** — SOUND: dual pulse, fast LFO→PWM, ZDF filter biting, moderate
  drive, low-mid. ART: urethane wheels on Muizenberg concrete; shreds the battery indicator.
- **03 "Half-Life" · P1 · from DUAL SAW** — SOUND: unstable dual saws, heavy VINTAGE slop, VCA sputter on
  release. Pure engine. **FLAGSHIP — the DØG-5 thesis in one patch.** ART: HOODBOX display glitching in an
  acid storm.
- **04 "V-Sync" · P1 · from SYNC LEAD** — SOUND: hard-sync sweep (OSC2→OSC1) off the VCF env, alias-tolerant,
  dead-stop release. ART: metallic chirp arcs past the top-right frame.
- **05 "ZEAROX" · P2 · from SUB BASS** — SOUND: noise over a cranked sub, max TAPE DEGRADE. Blown lo-fi kick
  sub. ART: raw static overloads the borders on every downbeat.
- **06 "zzuFuzz" · P2 · from FAT BASS** — SOUND: dual-osc fat source into maxed Preamp Drive, cutoff open.
  Voltage-starved fuzz. ART: neon-green marks burned into the interface.
- **07 "Tape Splice" · P2 · from XMOD GROWL** — SOUND: fat square + X-MOD pitch wobble, chopped by the gate;
  tape adds splice jitter. ART: jittery transients too fast to contain.
- **08 "Wire Bite" · P1 · from UNISON LD** — SOUND: unison detuned saws, slow attack, chopped on release; slop
  adds the spit. ART: sparks and spits through the 5th quadrant.

### CHAPTER II — THE TIDAL HEXES (surf rock & skinhead reggae) — BEE-TCH (the spring chapter)
- **09 "Skeenhead" (was Skinhead Bubble) · P2 · from CLAV PLUCK** — SOUND: tight plucky square, resonant plop,
  drenched in SPRING. The reggae off-beat stab; most exposed to the spring caveat. ART: cyan spray over the HUD.
- **10 "Atlantic Swell" · P2 · from HOLLOW PAD** — SOUND: dual pulse, slow LFO vibrato, heavy BBD. Woozy
  combo-organ. ART: freezing Cape surf drags the top menu under.
- **11 "Slapback Strut" · P2 · from SUB BASS** — SOUND: single triangle, fast decay, one ~80 ms free-ms BBD
  repeat. Percussive surf bass. ART: a rogue wave over the boundary.
- **12 "Kelp Tangle" · P2 · from HOLLOW PAD** — SOUND: heavy PWM off OSC B, murky LP, spring tail. ART:
  deep-sea thrash.
- **13 "Ghost Board" · P2 · from PWM STRING** — SOUND: filtered near-sine, max tape wow/flutter, heavy spring.
  ART: a 1-bit coastal deluge swamps the text.
- **14 "Reef Break" · P2 · from PERC HIT** — SOUND: white-noise attack, thick sub, long BBD feedback. ART: a
  tidal maelstrom over the top-right.
- **15 "Trem Chop" · P1 · from SQUARE LD (reworked)** — SOUND: bright saw, LFO→VCA hard square tremolo + a
  touch of slop (broken-strobe trem). ART: rhythmic pulses lock to the drums, drag under each cycle.
- **16 "Tidal Pull" · P2 · from TIDAL/PWM** — SOUND: 5-voice poly detuned pulses, slow attack, BBD + spring.
  Massive wet wash. ART: threatens to drown the whole frame.

### CHAPTER III — THE BAKSHI TOMES (dark fantasy & atmosphere) — MOONSHINE (drone-latch; magenta)
- **17 "Titanic" (was North Water Ice) · P1 · from DUAL SAW + fifth** — SOUND: dual saws a fifth apart (OSC2
  +7), extreme bass-comp, low register; tape dropouts optional. **CHAPTER III ANCHOR.** ART: freezing weight
  exhales thick smoke over the top bar.
- **18 "Roto-scopo" (was Rotoscoped Void) · P1 · from DRONE UNI** — SOUND: low-passed square, Poly-Mod OSC
  B→cutoff, slop ~90%, VCA latched. ART: slow dense magic obscuring the battery.
- **19 "Blackwater" (was Blackwater Tank) · P1 · from SUB BASS** — SOUND: sub-osc only, highly resonant filter
  tracking the keys, long decay, latched. ART: dark fog suffocating the UI.
- **20 "Fire & Ice" · P2 · from SYNC LEAD** — SOUND: hard-sync lead, tone rolled off, Drive + BBD. ART: smog
  across the right 1/5th on every held note.
- **21 "Cowl Shadow" · P1 · from DRONE UNI** — SOUND: 5-voice unison, very slow filter-env sweep, VCA latched.
  ~10 s brass wall. Textbook drone-latch. ART: suffocating brass erases the top menu.
- **22 "Melting Orb" · P1 · from BP QUACK (reworked)** — SOUND: slow downward filter-env melt on a fat unison
  source, inverted VCF env, high-but-musical resonance, latched. ART: a dense cloud rises to hide status.
- **23 "Crypt Dust" · P2 · from NOISE WASH** — SOUND: noise + thin pulse, heavy tape wow, no drive. ART:
  ancient smog into the margins.
- **24 "Fugue State" · P2 · from NEON PAD** — SOUND: triangle, extreme LFO pitch mod, BBD self-feedback. ART:
  pitch-black fog over the 5th quadrant, only the core visible.

### CHAPTER IV — THE ANCIENT RELICS (the survivors, rebuilt not ripped) — LE GATO (the closer)
- **25 "SAWTOOTH" · P1 · from POLY BRASS** — SOUND: dual saws, slight detune, classic 24 dB filter-env swell.
  ART: amber shrapnel pierces the right UI border.
- **26 "BSyncA" · P1 · from SYNC LEAD** — SOUND: OSC2 hard-synced, pitch env sweeping the slave. ART: geometric
  debris across the edge.
- **27 "R3V3RT" · P1 · from FAT BASS** — SOUND: single pulse, punchy decay-only filter env, zero resonance.
  Tight analog bass. ART: sharp polygonal strikes chip the frame.
- **28 "Bell Tolls" · P2 · from BELL XMOD (kept deliberately)** — SOUND: OSC B FM'ing OSC A (X-MOD), fast
  attack, long release. Inharmonic chimes; the friction with the hard-chop VCA IS the design. ART: golden code
  sheds over the poly-count.
- **29 "VALHALLA" · P1 · from VINTAGE PD** — SOUND: PWM on both osc, slow attack/release, slop ~20%. ART:
  fading amber radiates through the shattered HUD.
- **30 "THE DØG" · P1 · from DRONE UNI/unison** — SOUND: all voices on one note (UNISON), slight detune,
  filter wide open, low register. Floor-shaking. **SIGNATURE PATCH.** ART: acoustic weight crumbles the altar
  (now: the bark that shifts the cat; seismic judder + full keybed flash). ⚠️ needs the font Ø fix.
- **31 "Fi(l)fth" · P1 · from FIFTHS LD** — SOUND: OSC A + B seven semis apart, fast decay, short BBD. The
  archetypal aggressive chord stab. ART: shatters the pristine relic (now: the wheelie bin goes over).
- **32 "Init bruv?" · P1 · the INIT slot** — SOUND: single raw saw, open filter, flat envelopes, no effects.
  The blank slate. ART: the dormant bookend (bin upright, fence intact, cat still sitting).

---

## 4. CHAPTER BALANCE

| Chapter | Count | Phase split | Note |
|---|---|---|---|
| I Wasteland (Jalopy) | 8 | 3× P1, 5× P2 | bass, sync lead, fuzz, X-mod ✓ |
| II Tidal (Bee-tch) | 8 | 1× P1, 7× P2 | heavily Psych-Chain-dependent ⚠️ |
| III Bakshi (Moonshine) | 8 | 5× P1, 3× P2 | drones/pads on the latch ✓ |
| IV Relics (Le Gato) | 8 | 6× P1, 2× P2 | gig-ready early ✓ |

**P1 total 15 · P2 total 17.** Chapters III/IV deliver first; Chapter II waits on the spring/tape.

**Minimum gig set** (never ship below): 03 Half-Life, 17 Titanic, 30 THE DØG, 31 Fi(l)fth, 21 Cowl Shadow,
04 V-Sync, 25 SAWTOOTH, plus a reggae stab and a surf bass once the spring exists. ~9–12 patches.

---

## 5. OPEN

- [x] Screen art budget — procedural, resolved (see foundation §3.5).
- [ ] A/B gap scroll-wrap behaviour — match Vincent's gear.
- [ ] Generator build — against these SOUND briefs once the host build confirms ranges by ear.

## 6. WHAT'S NOT HERE YET
Final voicing. Every SOUND brief is a starting point in the right medium; the last-mile by-ear shaping on the
real engine is where these become DØG-5. Tone is king.
