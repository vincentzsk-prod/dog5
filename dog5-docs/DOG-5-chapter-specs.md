# DØG-5 — CHAPTER SPECS (per-patch dial rows)

**Status:** all four chapters specced, 17 Oct 2026. ⚠️ **27 Oct:** scene names/framing updated to the dog
world (Jalopy/Bee-tch/Moonshine/Le Gato; Moonshine = magenta). The engines, dials and per-patch rows below
stand — they are symbolic placeholders within each chapter's ranges, final tuning on hardware. Reads on top
of `DOG-5-art-direction.md`.

## §A — TEMPLATE & UNIVERSAL RULES (U1–U4)
Each chapter: Identity · scene · verb-as-beats · engine · dials (6 common + 1 engine-specific, with per-
chapter floor/ceiling) · signal bindings · LEDs · per-patch rows.
- **U1 — THE FENCE HEALS.** Whatever a chapter does reverses during `DECAY` within ~1–2 s after the gate
  closes (char redraws, water recedes, fog clears, shards re-fuse). Status never permanently lost over a set.
- **U2 — BIAS is chapter-locked to one fracture zone** (the "over the fence" gap): Jalopy top-right, Bee-tch
  top boundary, Moonshine top bar + upper-right, Le Gato top-right / right frame.
- **U3 — the bottom bar is never in the fracture zone.** Fire erupts up, water pours over the top, fog rises,
  debris falls down the right margin — all leave the lower bar clear.
- **U4 — the field is static.** Drawn once; only beam, impact, fence-damage and (high FLEAS) edge-boil animate.

## §B — CHAPTER I · JALOPY (FIRE) — acid green `#39FF14` · CONSUMES/deletes · 5th quadrant top-right
Electrical, not campfire: arcs, spits, overloads. Beats: rest → ignition gout to top-right → char creeps in →
sustain → gutters out → heal. Engine: white-hot arc segments + green fringe + rising ember pixels. LEDs:
snappiest key fall. Flagship **03 Half-Life** (orb numerals glitch), char-signature **06 zzuFuzz**.

| # | Name | INT | DEN | SPD | DEC | CHAR | SEED | BIAS (within TR) |
|---|---|---|---|---|---|---|---|---|
| 01 | Red Pill | 210 | 150 | 230 | 70 | 90 | chaotic | top-right, high |
| 02 | Cement Grind | 150 | 120 | 120 | 90 | 150 | low | right, at battery |
| 03 | Half-Life ⭐ | 230 | 160 | 240 | 60 | 130 | erratic | top edge |
| 04 | V-Sync | 170 | 70 | 255 | 40 | 30 | low | top-right, sharp |
| 05 | ZEAROX | 200 | 130 | 200 | 55 | 110 | med | all right border; tempo-pulsed |
| 06 | zzuFuzz 🔥 | 150 | 110 | 150 | 120 | **180** | med | scattered right |
| 07 | Tape Splice | 160 | 90 | 255 | 35 | 40 | high | top-right, spiky |
| 08 | Wire Bite | 170 | 140 | 170 | 65 | 80 | med | the corner itself |

Fire ranges: INT 40–255 · DEN 20–160 (hard dirty-area cap) · SPD 90–255 · DEC 30–140 · CHAR 0–180.

## §C — CHAPTER II · BEE-TCH (WATER) — abyssal cyan `#00C8D4` · SOAKS/covers · top boundary
Occludes (not deletes): a dithered cyan mass hides glyphs then drains. Beam flies straight up; flood pours
DOWN from the landing (the beam can't arc). Beats: rest → wave arc to top → flood covers + foam → surges with
LFO (the seasick swell) → settles → tide drains. Showcase **16 Tidal Pull** (waterline kisses the bar, never
covers the name). LEDs: slower rolling fall.

| # | Name | INT | DEN | SPD | DEC | LEVEL | SEED | BIAS (top) |
|---|---|---|---|---|---|---|---|---|
| 09 | Skeenhead | 190 | 110 | 190 | 45 | 20 | low | top, wide; tempo-able |
| 10 | Atlantic Swell | 150 | 120 | 60 | 120 | 90 | low | top-wide; high LFO swell |
| 11 | Slapback Strut | 220 | 140 | 210 | 40 | 10 | low | top crest, high |
| 12 | Kelp Tangle | 150 | 140 | 90 | 90 | 130 | med | low / deep, murky |
| 13 | Ghost Board | 180 | 120 | 110 | 120 | 140 | med | full-top cover |
| 14 | Reef Break | 200 | 150 | 140 | 70 | 60 | med | top-right |
| 15 | Trem Chop | 160 | 110 | sync | sync | 70 | med | top rhythmic; tempo-pulsed |
| 16 | Tidal Pull ★ | 255 | 150 | 70 | 130 | 160 | high | full, deepest |

Water ranges: INT 40–255 · DEN 20–150 (tighter — the flood band is widest) · SPD 40–220 · DEC 30–140 ·
LEVEL 0–160.

## §D — CHAPTER III · MOONSHINE (AIR) — magenta `#FF2FA0` · FOGS/dilutes · top bar + upper-right
Slow, latch-driven (the howl chapter). Dilutes by rising dither — structure stays, info lost. The figure
inverts near-white (moonlit); magenta only in the moving fog. Beats: rest → exhale bloom → diffuse up → fog
drowns status while the beam sways with the LFO → thins → re-emerges. ⚠️ Fog IS animated dither → the §9
clamps run at EVERY FLEAS setting here. Anchor **17 Titanic** (fog also exhales from the muzzle). **24 Fugue
State** tends to black-out. LEDs: held keys stay lit for the drone.

| # | Name | INT | DEN | SPD | DEC | OPAC | SEED | BIAS |
|---|---|---|---|---|---|---|---|---|
| 17 | Titanic ⭐ | 200 | 130 | 20 | 90 | 150 | low | top bar, wide |
| 18 | Roto-scopo | 180 | 130 | 25 | 90 | 160 | mid | upper-right (battery) |
| 19 | Blackwater | 170 | 120 | 35 | 100 | 150 | mid | top + right margin |
| 20 | Fire & Ice | 160 | 110 | 40 | 80 | 130 | mid | right 1/5th |
| 21 | Cowl Shadow | 190 | 120 | **10** | 110 | 160 | low | top menu, slowest |
| 22 | Melting Orb | 175 | 125 | 30 | 95 | 155 | mid | rises low → status |
| 23 | Crypt Dust | 150 | 110 | 45 | 85 | 120 | high | margins, diffuse |
| 24 | Fugue State | 200 | 140 | 30 | 90 | **170** | mid | 5th quadrant; dark |

Air ranges: INT 40–255 · DEN 20–140 · SPD 10–90 (the slowness is the chapter) · DEC 20–120 · OPAC 0–170
(never fully opaque — it's dilute, not cover).

## §E — CHAPTER IV · LE GATO (EARTH) — golden amber `#FFBF00` · WRECKS/displaces · top-right / right frame
Displaces (not deleted/covered/diluted): glyphs fracture into polygonal shards that fall under gravity, then
fly back and re-fuse. Beam strikes → fracture-flash → shards drift/fall down the right margin → re-fuse.
Signature **30 THE DØG** (1–2 frame 2–3px seismic judder — a shake, not a strobe — + full keybed flash; the
bark that shifts the cat). **31 Fi(l)fth** wrecks the field relic (the wheelie bin goes over). **32 Init
bruv?** = the only patch where nothing fractures (dormant bookend). LEDs: hardest percussive cut.

| # | Name | INT | DEN | SPD | DEC | SHARD | SEED | BIAS |
|---|---|---|---|---|---|---|---|---|
| 25 | SAWTOOTH | 190 | 140 | 200 | 70 | 110 | low | right border |
| 26 | BSyncA | 200 | 150 | 220 | 60 | 120 | mid | screen edge, wide |
| 27 | R3V3RT | 180 | 120 | 230 | 50 | 90 | low | right frame, sharp |
| 28 | Bell Tolls | 150 | 130 | 120 | 130 | 60 | mid | poly-count; long shed |
| 29 | VALHALLA | 160 | 110 | 90 | 120 | 80 | low | HUD-wide; radiant cracks |
| 30 | THE DØG ★ | 255 | 160 | 180 | 110 | **180** | low | top-right, heaviest |
| 31 | Fi(l)fth ◆ | 230 | 150 | 210 | 80 | 160 | mid | bin + frame |
| 32 | Init bruv? | 40 | 20 | 120 | 60 | 0 | — | none (dormant) |

Earth ranges: INT 40–255 · DEN 20–160 · SPD 60–255 · DEC 30–140 · SHARD 0–180.

## §F — STATUS
Four distinct pixel-ops (delete/cover/dilute/displace), four motions (erupt-up/arc-over/rise-diffuse/
strike-and-fall), four LED characters (snap/roll/hold/thud), one architecture. Remaining: hardware
calibration of the absolute dial ceilings and the four spot-colour hex values.
