# reference-renders/

**Purpose: host-render references to compare against recordings from the real FM-1.** Each file is the host build (the same engine and effects as the device, `tests/run_host.sh` path) playing a fixed audition phrase on the **approved, committed** variant of a voiced patch. Record the same phrase on the FM-1 (phrase scripts: `tests/voicing/phrases/`) and compare.

Only approved variants live here. Rejected variants and listening kits go on a separate never-merged `listen/<batch>` branch, never on main (see CLAUDE.md).

Format: 16-bit stereo, 44.1 kHz. Level = RMS over the note-on region, peak = sample peak, both dBFS, read from the variant's `results.json`. **Bank reference = -18.0 dBFS RMS (±1.5 dB, peak ≤ -4) on the patch's level phrase** (`dog5-docs/voicing/README.md`); the level phrase is marked LEVEL. Phrase letters are those of the voicing kit.

| File | Patch | Variant | Phrase | RMS dBFS | Peak dBFS | Role |
|---|---|---|---|---|---|---|
| `03-half-life_B_stabs.wav` | 03 half-life | B (centre) | (b) chord stabs | -18.0 | -6.0 | **LEVEL phrase** (reference -18.0) |
| `03-half-life_B_riff.wav` | 03 half-life | B (centre) | (a) riff | -21.2 | -11.4 | comparison |
| `30-the-dog_H_lowuni.wav` | 30 the-dog | H (presence) | (e) low unison | -16.5 | -7.3 | **LEVEL phrase** (reference -18.0) |
| `30-the-dog_H_stabs.wav` | 30 the-dog | H (presence) | (b) chord stabs | -17.0 | -8.1 | comparison |
| `31-fifth_C_stabs.wav` | 31 fifth | C (dual) | (b) chord stabs | -18.0 | -6.5 | **LEVEL phrase** (reference -18.0) |
| `31-fifth_C_riff.wav` | 31 fifth | C (dual) | (a) riff | -21.6 | -12.2 | comparison |
| `04-v-sync_D_lead.wav` | 04 v-sync | D (fat) | (d) single-note lead | -18.0 | -10.3 | **LEVEL phrase** (reference -18.0) |
| `04-v-sync_D_stabs.wav` | 04 v-sync | D (fat) | (b) chord stabs | -17.7 | -10.1 | comparison |
| `04-v-sync_D_riff.wav` | 04 v-sync | D (fat) | (a) riff | -18.1 | -10.6 | comparison |
| `25-sawtooth_B_stabs.wav` | 25 sawtooth | B (centre) | (b) chord stabs | -18.0 | -6.9 | **LEVEL phrase** (reference -18.0) |
| `25-sawtooth_B_riff.wav` | 25 sawtooth | B (centre) | (a) riff | -23.1 | -13.1 | comparison |
| `17-titanic_B_slow.wav` | 17 titanic | B (centre) | (f) slow, low (A1 held 10 s) | -17.8 | -9.2 | **LEVEL phrase** (reference -18.0) |
| `17-titanic_B_stabs.wav` | 17 titanic | B (centre) | (b) chord stabs | -17.1 | -4.4 | comparison |
| `17-titanic_B_riff.wav` | 17 titanic | B (centre) | (a) riff | -20.1 | -7.7 | comparison |
| `21-cowl-shadow_C_slowmid.wav` | 21 cowl-shadow | C (quick) | (f2) slow, mid | -17.6 | -6.8 | **LEVEL phrase** (reference -18.0) |
| `21-cowl-shadow_C_stabs.wav` | 21 cowl-shadow | C (quick) | (b) chord stabs | -31.3 | -19.4 | comparison |
| `21-cowl-shadow_C_riff.wav` | 21 cowl-shadow | C (quick) | (a) riff | -22.7 | -11.1 | comparison |
| `09-skeenhead_E_skank.wav` | 09 skeenhead | E (body) | (g) off-beat skank dyads | -17.9 | -8.7 | **LEVEL phrase** (reference -18.0) |
| `09-skeenhead_E_stabs.wav` | 09 skeenhead | E (body) | (b) chord stabs | -17.4 | -6.3 | comparison |
| `09-skeenhead_E_riff.wav` | 09 skeenhead | E (body) | (a) riff | -22.4 | -13.5 | comparison |
| `11-slapback-strut_G_surf.wav` | 11 slapback-strut | G (crisp) | (h) surf bass | -18.0 | -12.0 | **LEVEL phrase** (reference -18.0) |
| `11-slapback-strut_G_stabs.wav` | 11 slapback-strut | G (crisp) | (b) chord stabs | -17.6 | -11.9 | comparison |
| `11-slapback-strut_G_riff.wav` | 11 slapback-strut | G (crisp) | (a) riff | -17.9 | -12.2 | comparison |
| `01-red-pill_C_spit.wav` | 01 red-pill | C (grit) | (i) spit riff | -18.0 | -13.4 | **LEVEL phrase** (reference -18.0) |
| `01-red-pill_C_stabs.wav` | 01 red-pill | C (grit) | (b) chord stabs | -18.0 | -12.8 | comparison |
| `01-red-pill_C_riff.wav` | 01 red-pill | C (grit) | (a) riff | -18.1 | -13.4 | comparison |
| `02-cement-grind_D_grind.wav` | 02 cement-grind | D (wobble) | (j) grind riff | -17.9 | -14.7 | **LEVEL phrase** (reference -18.0) |
| `02-cement-grind_D_stabs.wav` | 02 cement-grind | D (wobble) | (b) chord stabs | -18.0 | -14.6 | comparison |
| `02-cement-grind_D_riff.wav` | 02 cement-grind | D (wobble) | (a) riff | -18.0 | -14.9 | comparison |
| `06-zzufuzz_C_wall.wav` | 06 zzufuzz | C (fiercer) | (k) wall: held note, power chords | -18.1 | -12.8 | **LEVEL phrase** (reference -18.0) |
| `06-zzufuzz_C_stabs.wav` | 06 zzufuzz | C (fiercer) | (b) chord stabs | -16.1 | -12.8 | comparison |
| `06-zzufuzz_C_riff.wav` | 06 zzufuzz | C (fiercer) | (a) riff | -21.3 | -17.0 | comparison |
| `08-wire-bite_D_wire.wav` | 08 wire-bite | D (zap) | (l) wire: high held note, bites | -17.9 | -8.9 | **LEVEL phrase** (reference -18.0) |
| `08-wire-bite_D_stabs.wav` | 08 wire-bite | D (zap) | (b) chord stabs | -18.2 | -9.0 | comparison |
| `08-wire-bite_D_riff.wav` | 08 wire-bite | D (zap) | (a) riff | -18.9 | -9.6 | comparison |
| `07-tape-splice_B_splice.wav` | 07 tape-splice | B (centre) | (n) splice: staccato, held A2, short A3s | -18.1 | -12.9 | **LEVEL phrase** (reference -18.0) |
| `07-tape-splice_B_stabs.wav` | 07 tape-splice | B (centre) | (b) chord stabs | -17.6 | -12.5 | comparison |
| `07-tape-splice_B_riff.wav` | 07 tape-splice | B (centre) | (a) riff | -16.8 | -13.0 | comparison |
| `15-trem-chop_D_chop.wav` | 15 trem-chop | D (smeared) | (o) chop: held A3, riff, chord | -17.9 | -6.2 | **LEVEL phrase** (reference -18.0; off parts of the chop included) |
| `15-trem-chop_D_stabs.wav` | 15 trem-chop | D (smeared) | (b) chord stabs | -15.4 | -6.2 | comparison (reads 2.5 dB over the level phrase) |
| `15-trem-chop_D_riff.wav` | 15 trem-chop | D (smeared) | (a) riff | -19.3 | -11.1 | comparison |
| `05-zearox_D_kick.wav` | 05 zearox | D (light, round 2) | (m) kick: 3 isolated hits A0 A1 A2, then 4 a bar | -18.1 | -10.7 | **LEVEL phrase** (reference -18.0) |
| `05-zearox_D_stabs.wav` | 05 zearox | D (light, round 2) | (b) chord stabs | -19.1 | -10.7 | comparison |
| `05-zearox_D_riff.wav` | 05 zearox | D (light, round 2) | (a) riff | -18.4 | -10.7 | comparison |
| `10-atlantic-swell_A_organ.wav` | 10 atlantic-swell | A (original, unchanged) | (q) organ: triads, staccato notes | -19.0 | -6.2 | **LEVEL phrase** (reference -18.0 ±1.5) |
| `10-atlantic-swell_A_stabs.wav` | 10 atlantic-swell | A (original, unchanged) | (b) chord stabs | -17.6 | -4.8 | comparison |
| `12-kelp-tangle_C_tangle.wav` | 12 kelp-tangle | C (cutoff 98) | (r) tangle: held A2, chord, short notes | -18.0 | -5.3 | **LEVEL phrase** (reference -18.0) |
| `12-kelp-tangle_C_stabs.wav` | 12 kelp-tangle | C (cutoff 98) | (b) chord stabs | -17.0 | -6.1 | comparison |
| `16-tidal-pull_D_wash.wav` | 16 tidal-pull | D (soft, triangle-like) | (s) wash: chords, notes, stabs | -19.1 | -4.4 | **LEVEL phrase** (peak-limited: -19.1, inside ±1.5) |
| `16-tidal-pull_D_stabs.wav` | 16 tidal-pull | D (soft, triangle-like) | (b) chord stabs | -26.8 | -10.8 | comparison (slow attack: 7.7 dB under the wash phrase) |
| `13-ghost-board_C2_ghost.wav` | 13 ghost-board | C2 (round 2, no PWM) | (t) ghost: chord, slow line, short notes | -18.0 | -4.9 | **LEVEL phrase** (reference -18.0 ±1.5) |
| `13-ghost-board_C2_stabs.wav` | 13 ghost-board | C2 (round 2, no PWM) | (b) chord stabs | -23.4 | -11.7 | comparison (5.4 dB under the ghost phrase) |
| `14-reef-break_C_crash.wav` | 14 reef-break | C (swell) | (u) crash: 11 hits, 300 ms gates | -18.0 | -4.5 | **LEVEL phrase** (reference -18.0; own-phrase peak -4.5 / -4.3 on two noise seeds) |
| `14-reef-break_C_stabs.wav` | 14 reef-break | C (swell) | (b) chord stabs | -12.8 | -1.5 | comparison: three keys at once stack three noise voices; no clipped sample |
| `18-roto-scopo_D_drone-A1.wav` | 18 roto-scopo | D (slow-deep) | (v lo) A1 held 15 s | -17.9 | -8.8 | **LEVEL phrase** (reference -18.0; RMS over +5..+14 s) |
| `18-roto-scopo_D_drone-A2.wav` | 18 roto-scopo | D (slow-deep) | (v mid) A2 held 15 s | -17.8 | -8.0 | comparison (long held, an octave up) |
| `18-roto-scopo_D_stabs.wav` | 18 roto-scopo | D (slow-deep) | (b) chord stabs | -23.3 | -11.6 | comparison (UNISON: one note per stab) |
| `18-roto-scopo_D_riff.wav` | 18 roto-scopo | D (slow-deep) | (a) riff | -20.1 | -10.6 | comparison |
| `22-melting-orb_D_drone-A2.wav` | 22 melting-orb | D (dual-chord) | (v mid) A2 held 15 s | -18.9 | -9.9 | **LEVEL phrase** (reference -18.0; RMS over +9..+14 s; the melt) |
| `22-melting-orb_D_chord-mid.wav` | 22 melting-orb | D (dual-chord) | (w mid) A2 E3 A3 held 8 s | -14.1 | -4.1 | comparison (long held chord, peak -4.1) |
| `22-melting-orb_D_stabs.wav` | 22 melting-orb | D (dual-chord) | (b) chord stabs | -18.3 | -6.6 | comparison |
| `22-melting-orb_D_riff.wav` | 22 melting-orb | D (dual-chord) | (a) riff | -20.9 | -9.1 | comparison |
| `19-micro-mist_D_held-chord.wav` | 19 micro-mist | D (tunnel) | (z chord) A3 C#4 E4 held 10 s + 6 s release | -17.9 | -4.7 | **LEVEL phrase** (reference -18.0; RMS over +4..+10 s) |
| `19-micro-mist_D_tap.wav` | 19 micro-mist | D (tunnel) | (z tap) chord and A4 taps, 150 ms | -28.4 | -9.8 | comparison (slow attack; RMS over the note-on region) |
| `19-micro-mist_D_stabs.wav` | 19 micro-mist | D (tunnel) | (b) chord stabs | -24.9 | -8.5 | comparison (low register; not what it is for) |
| `19-micro-mist_D_riff.wav` | 19 micro-mist | D (tunnel) | (a) riff | -28.6 | -13.7 | comparison (low register) |
| `20-fire-and-ice_D_lead.wav` | 20 fire-and-ice | D (open) | (d) single-note lead | -18.1 | -8.6 | **LEVEL phrase** (reference -18.0; note-on region) |
| `20-fire-and-ice_D_riff-detached.wav` | 20 fire-and-ice | D (open) | (aa) detached riff | -17.2 | -8.4 | comparison (detached riff: the sweep fires on every note) |
| `20-fire-and-ice_D_riff-legato.wav` | 20 fire-and-ice | D (open) | (ab) legato riff | -18.4 | -9.4 | comparison (the same notes legato: no re-fired sweep) |
| `20-fire-and-ice_D_stabs.wav` | 20 fire-and-ice | D (open) | (b) chord stabs | -16.6 | -8.5 | comparison (MONO plays one key of each stab) |
| `24-fugue-state_C_held-chord.wav` | 24 fugue-state | C (wobble) | (z chord) held triad 10 s + 6 s release | -17.9 | -5.4 | **LEVEL phrase** (reference -18.0; RMS over +4..+10 s; held 10 s, then 6 s of release) |
| `24-fugue-state_C_riff.wav` | 24 fugue-state | C (wobble) | (a) riff | -25.9 | -11.8 | comparison |
| `24-fugue-state_C_stabs.wav` | 24 fugue-state | C (wobble) | (b) chord stabs | -22.4 | -7.4 | comparison (slow attack: 4.5 dB under the held chord) |

Notes:
- Where the stabs phrase is the level phrase (03, 25, 31) only stabs + riff are kept; elsewhere level phrase + stabs + riff. Held-note renders were not kept.
- 30 THE DØG has only the two round-2 phrases (low unison, stabs).
- 09 Skeenhead: its log calls the skank phrase its "stabs" level reading (-17.9); the file named `_stabs` is phrase (b) (-17.4 per `results.json`).
- 21 Cowl Shadow's stabs phrase is far below reference (-31 dB): it is a slow bloom pad, not a stab patch; its level phrase is slowmid.
- Sources: 03, 04, 25, 30, 31 were copied from `listen/voicing/` on main (the originals were then removed from main as duplicates); 17, 21, 09, 11 from the `listen/batch-02a-weight-and-space` branch (`listen/voicing/batch-02a/...`), copied with `git show`; that branch was not merged.
- Regenerate: the `tests/voicing/*.py` round scripts (see `dog5-docs/voicing/README.md`); some need the pre-change base tree.
- 01 Red Pill, 02 Cement Grind, 06 zzuFuzz, 08 Wire Bite (Batch 3A, approved 5 Nov 2026: 01 C, 02 D, 06 C, 08 D): copied byte for byte from the `listen/batch-03a-chapter1-fat-and-driven` branch (`listen/voicing/batch-03a/...`) with `git show`; the held-note renders were not kept. 06's stabs phrase reads -16.1 (about 2 dB over its level phrase; the cause was not isolated); 08's level is read on the wire phrase.
- 07 Tape Splice B and 15 Trem Chop D (Batch 3B, approved as rendered after listening): copied byte for byte from the `listen/batch-03b-chapter1-wreck-and-chop` branch (`listen/voicing/batch-03b/...`); the held-note renders were not kept. Levels from the variants' `results.json`; the peaks are the whole phrase. 15 D is DUAL (every note two voices), so its chord phrase plays all three notes.
- 05 ZEAROX D (round 2 of Batch 3B, approved as rendered after listening; round 1's variants were rejected and have no reference renders): copied byte for byte from the `listen/batch-03b-chapter1-wreck-and-chop` branch (`listen/voicing/batch-03b/round2/05-zearox/`); the held-note render was not kept. Levels from the variant's `results.json`; the peaks are the whole phrase.
- 10 Atlantic Swell A, 12 Kelp Tangle C, 16 Tidal Pull D (Batch 4A, approved after listening 6 Nov 2026): copied byte for byte from the `listen/batch-04a-chapter2-organ-kelp-wash` branch (`listen/voicing/batch-04a/...`) with `git show`; the level phrase and the stabs phrase only. 10's renders are the unchanged original (the same values as before Batch 4A). Levels and peaks from each variant's `results.json` (the peak column of the level-phrase row is that phrase's peak; 10's whole-render peak is -4.8, from the stabs).
- 13 Ghost Board C2 (Batch 4B round 2) and 14 Reef Break C (Batch 4B round 1), approved after listening 6 Nov 2026: copied byte for byte from the `listen/batch-04b-chapter2-ghost-and-reef` branch (`listen/voicing/batch-04b/13-round2/` and `.../14-reef-break/`) with `git show`; the level phrase and the stabs phrase only. Levels and peaks from each variant's `results.json` (the peak of a level-phrase row is that phrase's own peak; 14's stabs peak is the three-key stab's).
- 18 Roto-scopo D and 22 Melting Orb D (Batch 5A round 2, approved after listening 6 Nov 2026): rendered from the COMMITTED slots through the program-load path (`render(program=17)` / `render(program=21)`), not copied from the listen branch. 22's renders are bit-identical to the listened variant renders; 18's differ from them (-30.2 .. -39.0 dB relative to the signal, `check_slot.py 18 D 5a`: the free-running random LFO and the CUTOFF / RESO slew start from the boot patch; not isolated). 22 has no phrase of its own other than the A2 hold, so its second held file is the three-key chord.
- 19 Micro-mist D (Batch 5A round 2, approved after listening 6 Nov 2026): rendered from the COMMITTED slot through the program-load path. All four files are bit-identical to the variant renders that were heard (the LFO is inert at D's values, so the boot patch makes no difference).
- 20 Fire & Ice D and 24 Fugue State C (Batch 5B, approved after listening 6 Nov 2026): rendered from the COMMITTED slots through the program-load path (`render(program=19)` / `render(program=23)`). The 20 D files are bit-identical to the round 1 renders that were heard (the variant over INIT). The 24 C files are NOT: loaded from the boot patch the slot differs from the heard render (-0.2 dB re the signal on the held chord, -5.3 to -9.7 dB on the stabs and the riff; the held-chord level reads -17.9 either way, its peak -5.4 against -4.9 dBFS), which suggests the engine's random state (VINTAGE walk, random start phases; not isolated). Both files stand for the same patch.
