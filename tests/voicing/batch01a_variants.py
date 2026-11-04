# SPDX-License-Identifier: GPL-3.0-only
"""The variant tables of Batch 1A (the decisions).  Each variant = the changes over the patch's ORIGINAL (resolved from the
base firmware); VOLUME is trimmed by the run.  Names as in obv_params.h without the P_ prefix."""

SHORT = {"a_riff": "riff", "b_stabs": "stabs", "c_held": "held", "d_lead": "lead", "e_lowuni": "lowuni"}

# ---- 30 THE DOG: unison stack, low register -----------------------------------------------------------------------------
DOG = {   # the shared moves: a punchy low stack instead of the drone it was (slot 18 / 21's array)
    "UNI_N": 8, "O2_SEMI": 12, "O2_LVL": 100, "O1_LVL": 110, "RESO": 12, "FA": 10, "FD": 58, "FS": 35, "AA": 4, "AD": 70, "AS": 127,
    "AR": 48, "FR": 50, "LFO_FLT": 0, "SPREAD": 50, "REV_MIX": 0, "GROWL": 18, "GRL_BIAS": 20,
    "UNI_DET": 28, "VINTAGE": 40, "CUTOFF": 100, "FENV_AMT": 86,
    "LFO_RATE": 70, "REV_SIZE": 80, "REV_DAMP": 60,     # (the drone's leftovers, inert with LFO FILTER 0 and DRAIN 0: back to the defaults)
}

# ---- 31 Fi(l)fth: the fifth in every voice ---------------------------------------------------------------------------------
FIFTH = {
    "MODE": 0, "POLY_N": 6, "O2_SEMI": 31, "O2_FINE": 66, "CUTOFF": 92, "RESO": 22, "FENV_AMT": 106, "FA": 0, "FD": 52, "FS": 22, "FR": 50,
    "AA": 0, "AD": 72, "AS": 70, "AR": 52, "GLIDE": 0, "DRIVE": 20, "LFO_PITCH": 0, "LFO_DELAY": 0, "ALLEY": 65, "DLY_FB": 28,
    "DLY_TONE": 55, "DLY_MIX": 36, "BBD_SPREAD": 60, "REV_MIX": 0, "SPREAD": 70, "VINTAGE": 35,
}

# ---- 04 V-Sync ------------------------------------------------------------------------------------------------------------------
SYNC = {   # the original's O2 +7 st / SYNC / MONO kept; the sweep deepened, the master saw brought in under it, the tail cut
    "O1_LVL": 80, "O2_LVL": 127, "ENV_O2": 112, "FD": 78, "FS": 28, "CUTOFF": 92, "RESO": 24, "FENV_AMT": 88,
    "AA": 0, "AD": 70, "AS": 127, "AR": 30, "FR": 30, "DLY_TIME": 0, "DLY_MIX": 12, "DLY_FB": 18, "REV_MIX": 0, "REV_SIZE": 80, "DRIVE": 20,
}

# ---- 25 SAWTOOTH --------------------------------------------------------------------------------------------------------------
BRASS = {
    "O2_FINE": 71, "CUTOFF": 56, "RESO": 15, "FENV_AMT": 100, "FA": 70, "FD": 85, "FS": 50, "FR": 60, "AA": 50, "AR": 55,
    "VINTAGE": 30, "GROWL": 6, "GRL_BIAS": 20,
}

import numpy as np
def law(p):
    """the engine's detune law in words: DUAL separates the pair by DETUNE^2/64 Q8-semitones; UNISON spreads N voices +-that;
    POLY has none; OSC 2 sits FINE cents from OSC 1 in every voice"""
    det = (p["UNI_DET"] ** 2 >> 6) * 100 / 256
    fine = (p["O2_FINE"] - 64) * 2 * 100 / 256 if p["O2_WAVE"] else 0.0
    m = p["MODE"]
    if m == 1:
        st = f"pair {det:.1f}"
    elif m == 2 and p["UNI_N"] > 1:
        st = f"{p['UNI_N']} voices over {2 * det:.1f} (step {2 * det / (p['UNI_N'] - 1):.1f})"
    else:
        st = "none"
    return st, fine

LISTEN30 = """`*_lowuni.wav` is the one to judge (A1 held 3 s, A0 held, chopped roots, A2): weight, the width of the stack, the chop. `*_riff.wav`
is the pilot's low riff (A1-A2), `*_held.wav` / `*_stabs.wav` are there for the bank's own readings. Listen for: how fat versus how
punchy B is (the attack should snap, the body should be a wall), and whether C's looser stack is seasick or just fat."""
NOTES30 = """*Notes.* The measured beat rate is the analysis window's floor (~0.4 Hz) and cannot tell B from C; the detune-law row is the real spread.
GROWL leaves a tiny constant DC offset behind after the note (the 10 Hz DC blocker's integer rounding, −44 … −53 dBFS, inaudible, an
engine trait left alone); release times are read after subtracting it. Variant A is rendered through the base firmware's own program path."""
LISTEN31 = """`*_riff.wav` (single notes = a fifth in every note: the real test of this patch) and `*_stabs.wav` (the pilot's fifth-based chords: a
fifth on every note of an already-fifth chord stacks into a sus2 cluster, so judge chord body on the riff rather than on the stabs).
Listen for: the pluck against the sustain, the slap's size, whether B is fat enough or C is needed."""
NOTES31 = """*Notes.* Phrase (b)'s chords already contain fifths, so +7 st stacks them (E+B becomes E, B, B, F#): that is the engine doing what the patch asks.
The level is read on (b) as for every patch. Variant A is the MONO fifths lead this slot was (rendered through the base program path)."""
LISTEN04 = """`*_lead.wav` is the one to judge (legato run A3 → A4, held A4, staccato run, a held A3 let go). Listen for: the rip on the attack,
the legato slide (glide kept), whether the master saw under it is enough fat to sit over a drum machine, and the dead stop at the end."""
NOTES04 = """*Notes.* A hard-sync lead has big sample steps by nature (the slave resets); the click row compares the release with the body, not against zero.
Level is read on the LEAD phrase (d), phrase (b) is in the table: the difference row is how much the lead phrase reads against the bank's own
reading. Variant A is rendered through the base program path (its spring is on)."""
LISTEN25 = """`*_stabs.wav` (fifth-and-octave chords, the bank's reading), `*_held.wav` (A2 held 2.4 s: the swell, the settle, the fade-in vibrato) and
`*_riff.wav`. Listen for: how it opens (the swell), warm versus bright, and whether it is clearly NOT 03 Half-Life (stable and brassy where that one is
unstable and chopped)."""
NOTES25 = """*Notes.* Against 03 Half-Life (pilot, variant B) on phrase (b): centroid 815 Hz, 51% under 150 Hz, wander s.d. 2.9 / 4.4 cents, gate-chop flutter
4.8 dB s.d. on the held note; SAWTOOTH B is steadier in all three (see the rows above). Variant A is rendered through the base program path."""

PATCHES = [
    dict(slot=30, dir="30-the-dog", name="THE DØG", cname="THE_DOG", level_name="LOW UNISON (A0-A2 roots held and chopped)", recommend="B centre", why=lambda R: _why30(R),
         listen=LISTEN30, notes=NOTES30, level="e_lowuni", short=SHORT,
         phrases=["a_riff", "b_stabs", "c_held", "e_lowuni"], held=("e_lowuni", 3000, 6000, 55.0), beat_win=2.0, rel_win=900,
         held_name="A1 held 3 s", env_name="A1 held 3 s", load="8 voices on one note, held",
         variants=[
             ("A", "original", "the nearest-base patch as it stood (the drone array it shares with 18 and 21)", {}),
             ("B", "centre", "the brief's first reading: 8-voice stack, +-4.7 cents, sub saw, filter open, a touch of GROWL", DOG),
             ("C", "wide", "B along the width axis: a looser, wider stack (more detune, more slop)", {**DOG, "UNI_DET": 44, "VINTAGE": 65, "SPREAD": 70}),
             ("D", "nasty", "B along the bite axis: filter wide open, more resonance, more GROWL", {**DOG, "CUTOFF": 127, "RESO": 26, "GROWL": 42}),
         ]),
    dict(slot=31, dir="31-fifth", name="Fi(l)fth", cname="FIFTH", level_name="FIFTH-BASED STABS", recommend="B centre", why=lambda R: _why31(R),
         listen=LISTEN31, notes=NOTES31, level="b_stabs", short=SHORT,
         phrases=["a_riff", "b_stabs", "c_held"], held=("c_held", 3000, 5400, 110.0),
         held_name="A2 held 2.4 s", env_name="A2 held 2.4 s", load="a fifth-and-octave chord + a fourth note",
         variants=[
             ("A", "original", "the nearest-base patch as it stood (a MONO fifths lead)", {}),
             ("B", "centre", "POLY stab: OSC 2 a fifth up in every voice, filter-env pluck, a short slap behind it", FIFTH),
             ("C", "dual", "B along the body axis, fatter: DUAL pair per note", {**FIFTH, "MODE": 1, "POLY_N": 8, "UNI_DET": 36, "SPREAD": 90}),
             ("D", "echo", "B along the delay axis: a longer, more present Space-Echo repeat", {**FIFTH, "ALLEY": 80, "DLY_FB": 38, "DLY_MIX": 42, "DLY_TONE": 50}),
         ]),
    dict(slot=4, dir="04-v-sync", name="V-Sync", cname="V_SYNC", level_name="LEAD (single notes A3-A4, legato and staccato)", recommend="B rip", why=lambda R: _why04(R),
         listen=LISTEN04, notes=NOTES04, level="d_lead", short=SHORT,
         phrases=["a_riff", "b_stabs", "c_held", "d_lead"], held=("c_held", 3000, 5400, 110.0),
         env_note=("d_lead", 4400, 5400, 440.0), held_name="A2 held 2.4 s", env_name="A4 held 1 s", load="2 notes sounding (mono: 1 voice)",
         variants=[
             ("A", "original", "the nearest-base patch as it stood (the sync lead it shares with 20 and 26)", {}),
             ("B", "rip", "the brief's first reading: sync slave swept by the filter envelope, dry-ish and dead-stopped", SYNC),
             ("C", "zap", "B along the rip axis: a deeper, faster sweep from a higher slave interval, more resonance and drive", {**SYNC, "ENV_O2": 127, "O2_SEMI": 36, "FD": 66, "FS": 12, "RESO": 40, "DRIVE": 40, "GROWL": 25, "GRL_BIAS": 30}),
             ("D", "fat", "B along the fat axis: a detuned unison pair of the synced voice", {**SYNC, "MODE": 2, "UNI_N": 2, "UNI_DET": 22}),
         ]),
    dict(slot=25, dir="25-sawtooth", name="SAWTOOTH", cname="SAWTOOTH", level_name="FIFTH-BASED STABS", recommend="B centre", why=lambda R: _why25(R),
         listen=LISTEN25, notes=NOTES25, level="b_stabs", short=SHORT,
         phrases=["a_riff", "b_stabs", "c_held"], held=("c_held", 3000, 5400, 110.0),
         held_name="A2 held 2.4 s", env_name="A2 held 2.4 s", load="a fifth-and-octave chord + a fourth note",
         variants=[
             ("A", "original", "the nearest-base patch as it stood (the poly brass)", {}),
             ("B", "centre", "the brief's first reading: two saws a few cents apart, a ~90 ms filter swell, stable", BRASS),
             ("C", "slow", "B along the swell axis: a slower, lazier swell", {**BRASS, "FA": 84, "AA": 64, "CUTOFF": 50, "FENV_AMT": 112}),
             ("D", "bright", "B along the bite axis: brighter, edgier brass", {**BRASS, "CUTOFF": 70, "FENV_AMT": 100, "RESO": 22, "GROWL": 14}),
         ]),
]


# ---- the texts the README is made of (numbers come from the run) -----------------------------------------------------------------
def _cost(r):
    return f"{r['cost_idle'] + r['cost_load']:.0f} worst-case host instr/sample (idle {r['cost_idle']:.0f} + load {r['cost_load']:.0f})"


def _why30(R):
    B, A, C, D = R["B"], R["A"], R["C"], R["D"]
    return (f"the tight, punchy stack the brief asks for: {law(B['params'])[0]} cents by the DETUNE law (DETUNE "
            f"{B['params']['UNI_DET']}; the original spread {law(A['params'])[0]}), {B['e_lowuni']['low_share']:.0f}% of the energy under 150 Hz (the drone this replaces: "
            f"{A['e_lowuni']['low_share']:.0f}%, centroid {A['e_lowuni']['centroid']:.0f} Hz vs {B['e_lowuni']['centroid']:.0f} Hz now), the filter "
            f"envelope opens each note ({B['held_env']['cent_peak']:.0f} Hz at the attack, {B['held_env']['cent_body']:.0f} Hz in the body, "
            f"+{B['held_env']['peak_over_body_db']:.1f} dB snap), it chops clean ({B['rel']['last60']:.0f} ms to −60 dB) and peaks at "
            f"{B['peak_all']:.1f} dBFS (worst-case CPU {B['cost_idle'] + B['cost_load']:.0f} host instr/sample against the original's {A['cost_idle'] + A['cost_load']:.0f}). C is the same patch looser (snap +{C['held_env']['peak_over_body_db']:.1f} dB, more wander); D opens the filter "
            f"and bites harder (centroid {D['e_lowuni']['centroid']:.0f} Hz).")


def _why31(R):
    B, A, C, D = R["B"], R["A"], R["C"], R["D"]
    return (f"a POLY stab with the fifth built into every voice (OSC 2 +7 st): fast pluck from the filter envelope "
            f"({B['held_env']['cent_peak']:.0f} Hz at the attack → {B['held_env']['cent_body']:.0f} Hz, +{B['held_env']['peak_over_body_db']:.1f} dB snap), a short "
            f"89 ms slap behind it, {B['rel']['last60']:.0f} ms to −60 dB with the repeats ({B['rel_dry']['last60']:.0f} ms voice alone), CPU {_cost(B)} "
            f"against C's {_cost(C)}. C (DUAL) is fatter ({C['b_stabs']['low_share']:.0f}% under 150 Hz vs {B['b_stabs']['low_share']:.0f}%) but doubles the "
            f"cost and the chord needs six voices; D only lengthens the echo.")


def _why04(R):
    B, A, C, D = R["B"], R["A"], R["C"], R["D"]
    return (f"the tearing sync lead: the master saw is brought in under a synced slave that the filter envelope sweeps "
            f"+{(B['params']['ENV_O2'] - 64) * 24 / 63:.0f} st over {0.5 * 20000 ** (B['params']['FD'] / 127):.0f} ms; centroid {B['d_lead']['centroid']:.0f} Hz "
            f"against the original's {A['d_lead']['centroid']:.0f} Hz, and the voice stops dead ({B['rel_dry']['last60']:.0f} ms to −60 dB alone, no click: "
            f"{B['click']['rel_step_db']:.0f} dBFS at the release against {B['click']['body_step_db']:.0f} in the body), with only a faint 1/16 slap behind it "
            f"({B['rel']['last60']:.0f} ms to −60 dB with it). CPU {_cost(B)}. C pushes the sweep and the drive; D doubles the voice (UNISON 2, "
            f"{law(D['params'])[0]} cents), costing {_cost(D)}.")


def _why25(R):
    B, A, C, D = R["B"], R["A"], R["C"], R["D"]
    return (f"stable, warm brass: two saws a few cents apart (law {law(B['params'])[1]:+.1f} cents), the filter swells to its brightest "
            f"{B['held_env']['cent_peak']:.0f} Hz at {B['held_env']['t_cent_peak_ms']:.0f} ms and settles to {B['held_env']['cent_body']:.0f} Hz, VINTAGE 30 "
            f"(wander s.d. {np.mean([v[1] for v in B['vlog'].values()]):.1f} cents), no chop. C is the lazy swell (peak at {C['held_env']['t_cent_peak_ms']:.0f} ms), "
            f"D the brighter edge ({D['b_stabs']['centroid']:.0f} Hz centroid). B's touch of GROWL is most of its CPU ({_cost(B)}; GROWL 0 would be about "
            f"{_cost(A)}).")
