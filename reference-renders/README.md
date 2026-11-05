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

Notes:
- Where the stabs phrase is the level phrase (03, 25, 31) only stabs + riff are kept; elsewhere level phrase + stabs + riff. Held-note renders were not kept.
- 30 THE DØG has only the two round-2 phrases (low unison, stabs).
- 09 Skeenhead: its log calls the skank phrase its "stabs" level reading (-17.9); the file named `_stabs` is phrase (b) (-17.4 per `results.json`).
- 21 Cowl Shadow's stabs phrase is far below reference (-31 dB): it is a slow bloom pad, not a stab patch; its level phrase is slowmid.
- Sources: 03, 04, 25, 30, 31 were copied from `listen/voicing/` on main (the originals were then removed from main as duplicates); 17, 21, 09, 11 from the `listen/batch-02a-weight-and-space` branch (`listen/voicing/batch-02a/...`), copied with `git show`; that branch was not merged.
- Regenerate: the `tests/voicing/*.py` round scripts (see `dog5-docs/voicing/README.md`); some need the pre-change base tree.
- 01 Red Pill, 02 Cement Grind, 06 zzuFuzz, 08 Wire Bite (Batch 3A, approved 5 Nov 2026: 01 C, 02 D, 06 C, 08 D): copied byte for byte from the `listen/batch-03a-chapter1-fat-and-driven` branch (`listen/voicing/batch-03a/...`) with `git show`; the held-note renders were not kept. 06's stabs phrase reads -16.1 (about 2 dB over its level phrase; the cause was not isolated); 08's level is read on the wire phrase.
