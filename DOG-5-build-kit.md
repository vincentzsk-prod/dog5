# DØG-5 — BUILD KIT: THE ART TO DRAW, AND WHAT ELSE IS NEEDED

**Status:** 21 Oct 2026. The production checklist for **v1.0, the preliminary build** — the version that is
finished, flashable and waiting when the FM-1 lands, so hardware time is spent testing rather than building.

**Companion to** `DOG-5-base-and-ui-decisions.md` (the base lock and the navigation). This one is the list of
things only Vincent can make, plus the handful of answers still needed before the big build starts.

---

## 0. WHAT v1.0 IS, AND WHAT IT ISN'T

**v1.0 is the preliminary build.** Everything that can be finished without the hardware, finished properly —
so that the day the unit arrives it gets flashed, played hard, and a list of adjustments comes back. Then v1.1
is the pass that uses that list.

| In v1.0 | Deferred to v1.1 |
|---|---|
| The pinned base, forked and owned | Final patch voicing by ear on the device |
| 20 screens, the panel map, the navigation | The four spot colours, eyeballed on the real panel |
| HOME / PERFORM, the transient readout, the bar | Legibility and dither corrections at real size |
| All four scenes, the dog, the beam, the fields | CPU / render-time trims, if any are needed |
| The Psych Chain, built and host-tested | `REV_DIV 2` decision (CPU lever, untested on device) |
| 32 patches, voiced by ear **on the host build** | Anything that needs an actual speaker and a room |
| The browser sim and the installer page | The web editor (dropped — §8 of the decisions doc) |
| Font fix, name field, polyphony control | |

The split is clean because the host build renders real audio to WAV and the sim runs the real firmware in a
browser. Nearly everything is judgeable before the hardware exists. What isn't, is the last mile of tone —
and that is the part that should take its time anyway.

---

## 1. THE ART TO DRAW BY HAND

This is the P0 list. Nothing else in the build is blocked by anything except this.

### 1.1 How to deliver it (read this first — it changes how you draw)

The screen is 1-bit: every pixel is on or off, one spot colour on black. There is no grey. So:

- **Draw in black ink on white, line and solid only.** No pencil tone, no wash, no grey marker. Dense
  hatching is good — it thresholds into dither, which is the texture, and the existing render already proves
  your hatching survives it.
- **Draw big: around 4× the target size.** The figure lands at roughly 140–150 px tall on screen, so work at
  roughly 600 px tall or larger. Scanning down is clean; scaling up is not.
- **One element per sheet or per layer.** The dog's body, the head, the nose, each field object — kept
  separate so they can be registered and recombined in code. If everything arrives as one flat drawing, it
  has to be cut apart by hand and the registration drifts.
- **Keep the heavy black keyline.** It is the law that makes the 1-bit reduction work, and it is what stops
  the figure dissolving into its own hatching at size.
- Scans or photos, 300 dpi or better, straight-on, no perspective. PNG or TIFF.

### 1.2 ⭐ THE DOG — three poses (the blocker)

Firmware tier: the maximalist drawing reduced so it reads at 240 px with the field and the UI around it.
Signature cues must survive in all three: **spiked back · stacked wonky eyes · lolling tongue · too many
teeth · dense hatched fur.**

| # | Pose | When it shows | Notes |
|---|---|---|---|
| **A1** | **REST** — mouth closed, standing, 3/4 profile, head up | Note-off. The resting state, and the idle sway | The default frame. Most of the time this is what is on screen |
| **A2** | **BARK** — mouth wide open, casting stance, head forward and up | Note-on. The beam fires from the open mouth | The hero frame. See the constraint below |
| **A3** | **HOWL** — head thrown back, mouth open upward | Moonshine only, on a held note | A separate full pose. Drone chapter, so it holds still |

**⚠️ The one constraint that matters, and it is a drawing constraint, not a code one:**

> **A1 and A2 must be the same dog in the same place, differing only around the head and mouth.**

Draw the body once. Draw two heads on it. If the two poses are registered so the difference is a small
rectangle around the muzzle, then every note-on repaints a postage stamp instead of the whole figure — and
notes come fast in this band. If the whole dog moves between the two, every note repaints the whole dog, and
that is the single most expensive thing the screen could possibly do.

Same thinking, less critically, for A3: it is a held-note pose in a slow chapter, so it can afford to be a
full separate sprite.

**Two more things about A2:** the open mouth is the beam's origin, so it needs **enough clear run to the
top-right corner that the bolt never crosses the dog's own body** — check that sightline while you draw it.
And the mouth wants to be wide enough that a couple of waveform cycles are legible coming out of it.

**Not needed, so don't draw them:**
- **The idle sway** is the same sprite shifted a pixel — no extra art.
- **The Moonshine near-white dog** is the same art inverted — no extra art.

### 1.3 THE NOSE — the FX alarm

A small separate element, registered onto all three poses, that can be drawn in its normal and its alarmed
state. It carries the FX-state signal now that the eyes are off duty. Two small drawings, or one plus a
filled version.

### 1.4 THE HEAD — the reducible mark (favicon tier)

His head alone, stripped to the fewest cues that still read as him: **spiked ridge + stacked eyes + snout.**

This is the hardest drawing on the list, and the brief already names it as the open blocker. It is not a
crop of A1 — it is a deliberate strip-down that has to survive at 32 px and smaller.

Used for: the browser tab icon on the sim and the installer, the Firmware Hub card, the README, and probably
the boot screen. It is the mark that represents the whole project everywhere it is small.

### 1.5 THE FOUR FIELDS — the backgrounds

Static, drawn once per scene, dithered. These are the scene identity — more than the colour is, because they
read before any text does.

| Ch | Scene | What's in it |
|---|---|---|
| I | **JALOPY** | Hot tar road, kerb, a car arse leaving frame |
| II | **BEE-TCH** | Flat cold Cape horizon, low dithered sea band, kelp |
| III | **MOONSHINE** | Bleak night, far horizon, the moon as the one static white disc |
| IV | **LE GATO** | Back alley, wall, wheelie bin, washing line, the cat in silhouette |

**Two constraints:**

1. **Each must be unmistakable in silhouette, from a metre, in the dark.** Not merely different in detail —
   different in *shape*. One strong recognisable form each: the car arse and kerb · the flat horizon line and
   kelp · the single white moon disc · the bin and washing line. If two of them read the same at a glance,
   the scene system has failed at the only job it has on stage.
2. **Leave the beam's corridor clear.** The bolt flies from the dog's mouth (left third) to a fence corner.
   Whatever is in that diagonal needs to be quiet, or the honest trace gets lost in the background.

### 1.6 LE GATO'S PROPS — two states each

Le Gato is the chapter where things get wrecked, so two of its objects need a before and an after:

- **The wheelie bin** — upright, and knocked over. (31 Fi(l)fth puts it over; 32 Init bruv? has it standing.)
- **The cat** — sitting unbothered, and the one moment it finally moves (30 THE DØG).

### 1.7 THE WORDMARK

- **`DØG-5`** — with the true slashed Ø. For the boot splash, the sim page, the installer page and the hub
  card.
- **`DØGS`** — if you want the band mark present anywhere in the firmware or on the pages.

### 1.8 Summary — the full hand-drawn list

| | Asset | Count |
|---|---|---|
| 1 | Dog — REST pose (A1) | 1 |
| 2 | Dog — BARK pose (A2), registered to A1 | 1 |
| 3 | Dog — HOWL pose (A3) | 1 |
| 4 | Nose — normal + alarmed | 2 |
| 5 | Head — reducible mark | 1 |
| 6 | Fields — Jalopy, Bee-tch, Moonshine, Le Gato | 4 |
| 7 | Wheelie bin — upright + over | 2 |
| 8 | Cat — sitting + moved | 2 |
| 9 | Wordmark DØG-5 (+ DØGS optional) | 1–2 |
| | **TOTAL** | **15–16 drawings** |

**If time is short, this is the order.** Each one unblocks the next stage of the build:

> **A2 (BARK) → A1 (REST) → Jalopy field → the head → the wordmark → the other three fields → the props → A3 (HOWL) → the nose**

A2 and A1 plus the Jalopy field are enough to build and prove the entire screen. Everything after that is
filling in scenes against an architecture that already works.

### 1.9 What is NOT hand-drawn — don't spend time on these

All of this is code, generated procedurally at run time. Drawing it would be wasted work:

the beam (live scope data) · the impact and shed in each scene · FLEAS degradation at all four stages · the
fence/HUD and its fracture, charring and shards · the bottom bar · the knob graphics and parameter-page
diagrams · the idle sway · the Moonshine inversion · the update-loader screen · the voice LEDs.

---

## 2. ANSWERS TO THIS SESSION'S QUESTIONS

### 2.1 Name field — widened to 14, and the struct should grow too

**Measured:** `NPARAM` is 63, the name is 10, `PATCH_BYTES` is 80. Spare today: **7 bytes.**

**Widening the name to 14 fits without growing the struct** (63 + 14 = 77, 3 spare). And 14 is exactly the
number needed — with your four renames in, **nothing in the bank is over 14 and nothing needs cutting:**

| Was | Now | Len |
|---|---|---|
| 09 Skinhead Bubble | **Skeenhead** | 9 |
| 17 North Water Ice | **Titanic** | 7 |
| 18 Rotoscoped Void | **Roto-scopo** | 10 |
| 19 Blackwater Tank | **Blackwater** | 10 |

The other nine that were over 10 all fit at 14 untouched: Cement Grind (12) · Tape Splice (11) · Atlantic
Swell (14) · Slapback Strut (14) · Kelp Tangle (11) · Ghost Board (11) · Cowl Shadow (11) · Melting Orb (11)
· Fugue State (11). **Longest in the bank: Atlantic Swell and Slapback Strut at 14.**

**The bar is comfortable.** The font advances 8 px per character on a 240 px line, so the worst case —
`11 Atlantic Swell` — is 136 px with **104 px spare.** Legibility was never the constraint; the struct was.

**⚠️ But do one more thing while you are in there: bump `PATCH_BYTES` from 80 to 96.**

With the name at 14 and DØG-5's own new parameters (Tape's second macro, the polyphony limit), the struct
lands at 79 of 80 — **one spare byte.** You have already said there will be a v1.1 after hardware testing,
and a v1.1 with one spare byte cannot add a single parameter without migrating every saved patch.

Going to 96 costs **1,584 bytes of flash** (16 × 99 slots) against a budget where the whole preset bank was
~5 KB of 425 KB. It buys **17 spare bytes** — room for the v1.1 you are already planning. Do it now, in the
same change, before a single patch exists and while migration is free.

### 2.2 Variable polyphony — yes, and it is genuinely cheap

Verified in source. The voice pool is `NV 8`, and **every path that allocates or counts voices already asks
one function for its window** — `part_cards(part, &lo, &n)`. `voice_alloc`, `uni_count` and `voice_trigger`
all read from it.

So a user-selectable polyphony limit is **one clamp in one function, plus one parameter.** Add `P_POLY_N`
(range 1–8, default 5) on the VOICE page, clamp `n` in `part_cards`, done. That is the whole change.

**One honest caveat so the expectation is right:** this will not make the synth run faster in normal
playing. The render loop already skips idle voices, so an unused voice costs essentially nothing. What the
limit actually buys is worth having anyway:

- **A guaranteed worst-case CPU ceiling.** At 5 you know the maximum load you can ever hit, which matters
  when the art is competing for the same milliseconds.
- **Voice-stealing character.** A 5-voice poly steals notes; an 8-voice one mostly doesn't. That is a
  *tonal* difference, not a spec one — it changes how chords behave under your hands.
- **It settles the open 5-vs-8 question properly.** Instead of us choosing on paper, you A/B it live on the
  device with a knob, in a room, which is the only way that question should ever have been answered.

**Default ships at 5.** The five-motif stays intact — POLY 5, fifth of the litter, Fi(l)fth — and 6, 7 and 8
are there when a patch wants them. This costs so little that reverting to fixed-5 would save nothing worth
having.

*(Small consequence: the VOICE page's four knob slots are full — MODE, VOICES, DETUNE, GLIDE. `P_POLY_N`
needs a fifth slot, so VOICE becomes two pages. The screen count goes 19 → 20. It is a table row.)*

### 2.3 The spring — de-risked, and that closes the biggest tone risk in the bank

Taking "next closest thing, not expecting excellence, I have real units for that" as the instruction. That
is the right call and it removes the largest un-de-risked item in the whole project.

Concretely, the re-voice is: push the plate's two swaying allpasses **faster and shallower** for the
characteristic chirp, pull `PRE-DLY` short, brighten `DAMP`, and tighten `SIZE`'s range so it cannot bloom
into a hall. It lands as "a short bright boingy reverb that behaves like a spring" rather than a modelled
spring, and that is explicitly enough.

**Why this matters beyond the one effect:** Bee-tch is 7 of 8 patches dependent on the spring, so an
unresolved spring meant a quarter of the bank was unresolved. Calling it good-enough in advance means
Chapter II can be voiced on the host build like every other chapter, with no gate in front of it. The build
review flagged this as the single largest tone bet; it is now simply not one.

---

## 3. WHAT ELSE IS NEEDED FROM YOU

Short list. Most are one-liners.

### 3.1 Blocking the build

| # | Need | Why it blocks |
|---|---|---|
| 1 | **The fork created on GitHub, and its name** | I cannot create it — it needs your account. Everything is checked out from it. Suggested: `dog-5` or `dog5-fm1` |
| 2 | **Author / credit line** for `LICENSING.md` and the README | GPL-3.0 obligation. How you want to be named — "Vincent Kruger", "DØGS", or both |
| 3 | **The art in §1**, in the order at §1.8 | A2 + A1 + the Jalopy field unblock the entire screen architecture |

### 3.2 Decisions, quick ones

| # | Question | My recommendation |
|---|---|---|
| 4 | `PATCH_BYTES` 80 → 96? | **Yes.** 1.6 KB of flash for a v1.1 that can actually add things (§2.1) |
| 5 | `DØGS` wordmark in the firmware, or just `DØG-5`? | Just `DØG-5` on screen; `DØGS` on the pages |
| 6 | Do the sim and installer pages get full art now, or placeholder until v1.1? | **Full art now** — they are the release, and the art is being drawn anyway |
| 7 | Does `THE POUND` / `THE PACK` survive as a write-lock over slots 1–64 vs 65–99? | **Yes**, it maps cleanly onto the inherited 99-slot store |

### 3.3 Useful, not blocking

- **The FM-1's actual ETA**, when you have it. "Two weeks" is enough to sequence against; a date would sharpen it.
- **Anything new from your hand** that should join the signature cues — the brief says the "wrong" features
  keep arriving and the rule is consistency, not a closed list. If a new one has turned up, fold it in before
  the three poses are drawn, not after.

---

## 4. THE BUILD SEQUENCE

What happens in what order once the fork exists. Items marked **[V]** wait on you.

**Stage 1 — foundations (no art needed)**
1. Fork, pin to `7e1ccf9`, tag `base/obervave-v1.5.3`, upstream as fetch-only **[V: the repo]**
2. Host build and browser sim running and renamed
3. Font: extend the generator for Ø, so `THE DØG` stops rendering `THE D?G`
4. Patch struct: name 10 → 14, `PATCH_BYTES` 80 → 96 **[V: confirm]**
5. Delete the sequencer; free SEQ, ALGORITHM, PLAY, REC
6. Page table: 20 screens, families-remember, hold-HOME control map
7. `P_POLY_N` on the VOICE pages

**Stage 2 — the voice (no art needed, runs in parallel with your drawing)**
8. Psych Chain: Drive and Tape built; Delay to free-ms with tap tempo; Spring re-voiced per §2.3
9. The 32 patches voiced by ear on the host build, against the SOUND briefs
10. A/B write-lock over the 99-slot store

**Stage 3 — the screen (gated on the art)**
11. **[V] A2 + A1** → the dog on screen, mouth gate-keyed, registered redraw
12. The beam from the mouth, fed by the existing zero-crossing scope capture
13. The bottom bar; the transient knob readout over the art
14. **[V] Jalopy field** → scene one complete, as the proof scene
15. **[V] the other three fields + props** → Bee-tch, Moonshine (magenta), Le Gato
16. **[V] A3 + the nose** → the howl pose, the FX alarm
17. FLEAS, the fence and its fracture, per-chapter impacts

**Stage 4 — the release**
18. **[V] the head + wordmark** → boot splash, favicon, update-loader reskin
19. The sim page and the installer page
20. GPL-3.0 `.fwsc` release on GitHub; submit to `zven@thefirmwarehub.com`

**Then:** the unit arrives, v1.0 goes on it, you play it hard, and the list that comes back is v1.1.

Stages 1 and 2 need nothing from you but the repo and two confirmations, so **the build can start before the
first drawing is finished.** The art gates Stage 3 only.
