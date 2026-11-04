# SPDX-License-Identifier: GPL-3.0-only
"""The variant tables of Batch 2A (the decisions).  Each variant = the changes over the patch's ORIGINAL (resolved from the base
firmware); VOLUME is trimmed by the run.  Names as in obv_params.h without the P_ prefix."""
SHORT = {"a_riff": "riff", "b_stabs": "stabs", "c_held": "held", "f_slow": "slow", "f2_slowmid": "slowmid", "g_skank": "skank", "h_surf": "surf"}

TITANIC = {   # B
    "O2_WAVE": 1, "O2_SEMI": 31, "O2_LVL": 100, "UNI_DET": 30, "POLY_N": 6, "VINTAGE": 40, "KEYTRK": 12, "CUTOFF": 66, "RESO": 12,
    "FENV_AMT": 84, "FA": 62, "FD": 90, "FS": 70, "FR": 85, "AA": 60, "AS": 127, "AR": 92,
}
COWL = {
    "UNI_N": 5, "UNI_DET": 40, "VINTAGE": 45, "O2_SEMI": 24, "O2_FINE": 66, "O2_LVL": 100, "O1_LVL": 110, "RESO": 14, "CUTOFF": 40, "FENV_AMT": 118,
    "FA": 127, "FD": 70, "FS": 127, "FR": 110, "AA": 96, "AS": 127, "AR": 108, "LFO_FLT": 0, "REV_MIX": 0, "SPREAD": 100, "KEYTRK": 127,
    "LFO_RATE": 70, "REV_SIZE": 80, "REV_DAMP": 60,
}
SKEEN = {
    "O1_WAVE": 2, "O1_PW": 64, "O2_WAVE": 0, "O2_PW": 64, "O2_FINE": 70, "FTYPE": 0, "RESO": 62, "CUTOFF": 40, "FENV_AMT": 118, "FD": 56, "FS": 0, "KEYTRK": 100, "AA": 0, "AD": 70,
    "AS": 30, "AR": 28, "REV_MIX": 90, "REV_SIZE": 70, "REV_DAMP": 40, "REV_PRE": 4,
}
SLAP = {
    "O1_WAVE": 2, "O1_PW": 64, "O1_LVL": 127, "O2_WAVE": 0, "O2_LVL": 100, "O2_SEMI": 24, "FTYPE": 0, "RESO": 16, "CUTOFF": 63, "KEYTRK": 127, "FENV_AMT": 96, "FD": 56, "FS": 0, "AA": 0, "AD": 72, "AS": 0, "AR": 24,
    "ALLEY": 62, "DLY_FB": 12, "DLY_MIX": 127, "DLY_TONE": 70, "BBD_SPREAD": 0,
}



def _cost(r):
    c = r["cost"]
    return f"{c['idle'] + c['load']:.0f} worst-case host instr/sample (idle {c['idle']:.0f} + load {c['load']:.0f})"


def _why17(R):
    A, B, C, D = R["A"], R["B"], R["C"], R["D"]
    return (f"dual saws a fifth apart (OSC 2 +7 st, both at full level) in a DUAL pair about 5.5 cents apart, cold (no drive, RESO 12, no effects) and heavy, with an "
            f"extreme bass compensation: KEY TRK 12 (9 %), so the filter opens for low notes and closes for high ones. The same note struck at A1 / A2 / A3 puts "
            f"{B['reg'][0]['harm']:.1f} / {B['reg'][1]['harm']:.1f} / {B['reg'][2]['harm']:.1f} harmonics under the centroid (A: {A['reg'][0]['harm']:.1f} / {A['reg'][1]['harm']:.1f} / "
            f"{A['reg'][2]['harm']:.1f}) and A1 is {B['reg'][0]['level'] - B['reg'][2]['level']:.1f} dB louder than A3; the stack is {B['f_slow']['bands']['<60']:.0f} % under 60 Hz, "
            f"{B['f_slow']['bands']['60-150']:.0f} % in 60-150 Hz (the fifth lives there), only {B['f_slow']['bands']['400-1.2k']:.0f} % above 400 Hz: freezing and desolate rather than bright. "
            f"It reads {B['level']:.1f} dBFS on the steady hold and {B['b_stabs']['rms']:.1f} on phrase (b) (difference {B['b_stabs']['rms'] - B['level']:+.1f} dB), "
            f"releases in {B['rel']['t60']:.0f} ms to -60 dB, and costs {_cost(B)}. C is the same patch colder and darker ({C['reg'][0]['harm']:.1f} harmonics at A1, "
            f"centroid {C["f_slow"]['centroid']:.0f} Hz against B's {B['f_slow']['centroid']:.0f}, release {C['rel']['t60']:.0f} ms); D adds the tape weather ({_cost(D)}).")


def _why21(R):
    A, B, C, D = R["A"], R["B"], R["C"], R["D"]
    bt, ct, dt = B["bloom_t"], C["bloom_t"], D["bloom_t"]
    return (f"five unison saws (two oscillators in every voice, DETUNE 40 = the stack spread +-9.8 cents, 2.4 cents between neighbours), a dark start and a filter envelope that takes its full 10 s attack "
            f"(ATTACK 127): the centroid climbs {bt['octaves']:.1f} octaves, from {bt['cent0']:.0f} Hz to {bt['cent_plateau']:.0f} Hz, reaching 10 % of the climb at {bt['cent_t10']:.1f} s and "
            f"90 % at {bt['cent_t90']:.1f} s; the amp is up in about a second ({B['lvl_first1s']:.1f} dB in the first second against {B['level']:.1f} dB in the bloomed state, "
            f"the level the reference is read on). Gate held open (both sustains at full). Released early (A2 held 2.4 s) it is a dark short note: centroid {B['early']['cent_end']:.0f} Hz "
            f"at the key-up and a tail of {B['early']['tail']['t40'] / 1000:.1f} s to -40 dB. The release is {B['rel']['t20'] / 1000:.1f} s to -20 dB after a full bloom, the filter envelope "
            f"falling with it. Dry: no spring (the original's 8 voices and spring cost {_cost(A)}; this costs {_cost(B)}). C is the same bloom in about 5 s (90 % at {ct['cent_t90']:.1f} s); "
            f"D opens to {dt['cent_plateau']:.0f} Hz ({dt['octaves']:.1f} octaves) for the Jupiter-style blare at the top.")


def _why09(R):
    A, B, C, D = R["A"], R["B"], R["C"], R["D"]
    return (f"a tight, plucky square (one 50 % pulse) through a resonant 12 dB low-pass whose envelope falls in about {0.5 * 20000 ** (56 / 127):.0f} ms, which is the plop (the first 23 ms "
            f"of a stab are {B['snap'][0]:.0f} Hz against {B['snap'][1]:.0f} Hz in the next 67 ms), and a short, bright spring drenching it: the spring's return is "
            f"{B['fx_re_dry_db']:.1f} dB under the dry stab inside the stab, the gap between stabs sits {B['gap_re_stab_db']:.1f} dB under the stab, and the tail runs {B['rel']['t60'] / 1000:.2f} s "
            f"to -60 dB. At the reference level ({B['level']:.1f} dBFS with the spring on; the dry stabs alone are {B['dry_rms']:.1f}) the peak is {B['peak_all']:.1f} dBFS. "
            f"Cost {_cost(B)}. C drenches it ({C['fx_re_dry_db']:+.1f} dB inside the stab, tail {C['rel']['t60'] / 1000:.2f} s); D goes deeper on the plop (first 23 ms {D['snap'][0]:.0f} Hz).")


def _why11(R):
    A, B, C, D = R["A"], R["B"], R["C"], R["D"]
    e = B["echo"]
    return (f"one pulse through a 12 dB low-pass that tracks the keyboard so the oscillator sits near a triangle (harmonics 3 / 5 / 7 at {B['tri'][1]:.0f} / {B['tri'][2]:.0f} / {B['tri'][3]:.0f} dB; "
            f"a triangle is -19 / -28 / -34), with a filter pluck and an amp that falls {B['drop'][0]:.0f} dB inside the 100 ms gate ({B['drop'][1]:.0f} ms to fall 10 dB), and one loud mono "
            f"slap at 80 ms (ALLEY 62): the first repeat is {e['echo_re_note_db']:+.1f} dB re the note's own peak and the second {e['repeat2_re_first_db']:.0f} dB "
            f"under the first. Reference level {B['level']:.1f} dBFS with the echo (dry notes alone {B['dry_rms']:.1f}), peak {B['peak_all']:.1f}. Cost {_cost(B)}. C adds a spring wash "
            f"(DRAIN 60, tail {C['rel']['t60'] / 1000:.2f} s to -60 dB, {_cost(C)}); D brightens the pluck toward a square (harmonics {D['tri'][1]:.0f} / {D['tri'][2]:.0f} / {D['tri'][3]:.0f} dB).")


LISTEN17 = """`*_slow.wav` (A1 held 10 s then let go: the weight, the beat of the pair, the release), `*_riff.wav` (A1-A2 chopped: the bass compensation, the long release against the chop)
and `*_stabs.wav` (fifth-and-octave chords: the DUAL pair, POLY 6). Listen for: cold or just dull (B against C), whether the fifth is a hollow power chord or a hum, whether the low
notes open up and the high ones close down the way an anchor should, and whether D's tape weather is a garnish or a distraction."""
NOTES17 = """*Notes.* Level for this patch is read on the steady part of the A1 hold (+6 to +10 s after note-on, README section 10); phrase (b) is in the table with the difference. 17 does not bloom:
it sits where it starts (the bloom rows are left out of the table; the second-by-second table shows it). Variant A is rendered through the base program path. The DRAIN probe is not a
variant: B with the spring added at three settings, to answer what the tank does on a bass (README section 10)."""
LISTEN21 = """`*_slowmid.wav` (A2 held 10 s: the bloom; start with C, B, D), `*_held.wav` (A2 held 2.4 s: what an early release does) and `*_stabs.wav` (chords on a unison patch: not its job, it is here
for the bank's reading). Listen for: how long before it opens, whether it blooms evenly or sits dark and then jumps, the blare at the top, and the release after a long hold."""
NOTES21 = """*Notes.* The level is read on the bloomed state (+6 to +10 s), since the patch is a slow swell; short notes on it (phrase b) read about 13 to 21 dB lower, because they are the dark start of the bloom
and never get further: this patch is for held notes. The engine has no drone latch: the bloom happens while the key is down, and an early release fades the note from wherever it got to.
The envelope's longest attack is 10 s (ATTACK 127); the brightness reaches 90 % of its climb at 7 s because the last part of the climb is above the harmonics that are left. Variant A is rendered through the base program path."""
LISTEN09 = """`*_skank.wav` is the one to judge (off-beat dyads with a 1.5 s gap and a long last tail: the plop and the chirp, the tail between stabs). `*_stabs.wav` and `*_riff.wav` are the pilot phrases. Listen for:
the chirp of the spring (does it sound like a tank or like a reverb), whether B's tail is wet enough or C's is too much (tubby), and whether the plop is a plop."""
NOTES09 = """*Notes.* The original has no spring at all (DRAIN 0): the "drenched in spring" part of the brief is new. The level is read on the stabs' note-on region with the spring on, so the spring adds
to the reading (the dry stabs alone are about 1.5 dB lower); its tail after note-off is not in the reading and is measured separately. The spring's return is measured as the render
with the spring on minus the same render with it off. Variant A is rendered through the base program path."""
LISTEN11 = """`*_surf.wav` is the one to judge (single-note staccato eighths, A1 to A2, a long last tail): the pluck, the roundness, the loud slap. `*_riff.wav` is the pilot's low riff (the same bass at 150 ms gates).
Listen for: is the slap loud enough and clean (B), does C's wash help or blur, does D's brighter pluck still read as a round bass, and whether the decay is fast enough."""
NOTES11 = """*Notes.* The engine has no triangle oscillator (OSC waves are saw and pulse, the LFO has the only triangle): the roundness is a 50 % pulse through a tracking 12 dB low-pass, measured against an ideal
triangle in the table. A faster decay than about 44 ms per 10 dB cannot reach the reference level even with VOLUME at 127 (the pluck then dies inside the 100 ms gate), so the decay is as fast as the level
allows; the filter envelope carries the snap. The level reading includes the slap. The DRAIN probe is not a variant: B with the spring at three settings. Variant A is rendered through the base program path."""

PATCHES = [
    dict(slot=17, dir="17-titanic", name="Titanic", cname="TITANIC", kind="slow", bloom=False, f0=55.0, level="f_slow", level_def="RMS over +6..+10 s of the A1 hold (phrase f)",
         recommend="B centre", why=_why17, listen=LISTEN17, notes=NOTES17, short=SHORT, phrases=["a_riff", "b_stabs", "c_held", "f_slow"], load="a fifth-and-octave chord + a fourth note",
         drain_probe=True, variants=[
             ("A", "original", "the nearest-base patch as it stood (one saw per voice in a DUAL pair, CUTOFF 70, dry)", {}),
             ("B", "centre", "the brief's first reading: dual saws a fifth apart, extreme bass compensation, cold and dry, a long release", TITANIC),
             ("C", "colder", "B along the cold / comp axis: KEY TRK 0 and a lower, darker cutoff, a slower open and a longer release", {**TITANIC, "KEYTRK": 0, "CUTOFF": 54, "FA": 70, "AA": 70, "AR": 104}),
             ("D", "weather", "B along the garnish axis: tape dropouts and hiss (CHEW 80, DROPS 100); costs CPU all the time", {**TITANIC, "CHEW": 80, "TP_DROPS": 100}),
         ]),
    dict(slot=21, dir="21-cowl-shadow", name="Cowl Shadow", cname="COWL_SHADOW", kind="slow", f0=110.0, level="f2_slowmid", level_def="RMS over +6..+10 s of the A2 hold (phrase f2)",
         recommend="B centre", why=_why21, listen=LISTEN21, notes=NOTES21, short=SHORT, phrases=["a_riff", "b_stabs", "c_held", "f2_slowmid"], load="5 unison voices on one note",
         variants=[
             ("A", "original", "the nearest-base patch as it stood (the 8-voice drone it shared with 18 Roto-scopo: a wide, spring-soaked pad)", {}),
             ("B", "centre", "the brief's first reading: five-voice unison brass, a dark start, a 10 s filter attack, gate held open, long release", COWL),
             ("C", "quick", "B along the bloom axis: about five seconds to open (ATTACK 119 for the filter, a quicker amp)", {**COWL, "FA": 119, "AA": 90}),
             ("D", "blare", "B along the top-of-swell axis: brighter and edgier at the top (CUTOFF, ENV AMT, RESO, filter DRIVE up)", {**COWL, "CUTOFF": 50, "FENV_AMT": 127, "RESO": 22, "DRIVE": 40}),
         ]),
    dict(slot=9, dir="09-skeenhead", name="Skeenhead", cname="SKEENHEAD", kind="spring", level="g_skank", level_def="RMS over the stabs' note-on region of the skank (phrase g), spring included",
         recommend="B centre", why=_why09, listen=LISTEN09, notes=NOTES09, short=SHORT, phrases=["a_riff", "b_stabs", "c_held", "g_skank"], load="a fifth-and-octave chord + a fourth note",
         variants=[
             ("A", "original", "the nearest-base patch as it stood (two narrow pulses, LP12, a clav pluck, no spring)", {}),
             ("B", "centre", "the brief's first reading: one tight square, a resonant plop, a short bright spring drenching it", SKEEN),
             ("C", "drench", "B along the spring axis: wetter and longer (DRAIN 115, SIZE 95, PRE-DLY 0)", {**SKEEN, "REV_MIX": 115, "REV_SIZE": 95, "REV_PRE": 0}),
             ("D", "plop", "B along the plop axis: a lower cutoff, more resonance and a longer fall, so a deeper, rounder plop", {**SKEEN, "RESO": 80, "FD": 66, "CUTOFF": 34}),
         ]),
    dict(slot=11, dir="11-slapback-strut", name="Slapback Strut", cname="SLAPBACK_STRUT", kind="echo", level="h_surf", level_def="RMS over the note-on region of the surf riff (phrase h), echo included",
         recommend="B centre", why=_why11, listen=LISTEN11, notes=NOTES11, short=SHORT, phrases=["a_riff", "b_stabs", "c_held", "h_surf"], load="a fifth-and-octave chord + a fourth note",
         drain_probe=True, variants=[
             ("A", "original", "the nearest-base patch as it stood (pulse + saw octave, MONO, dry; shared with 05 ZEAROX and 19 Blackwater)", {}),
             ("B", "centre", "the brief's first reading: one round pulse (the nearest to a triangle), a fast pluck, one loud mono slap at 80 ms", SLAP),
             ("C", "wash", "B along the space axis: the same slap into a spring wash (DRAIN 60)", {**SLAP, "REV_MIX": 60, "REV_SIZE": 80}),
             ("D", "snap", "B along the pluck axis: brighter, snappier, closer to a square", {**SLAP, "CUTOFF": 70, "FENV_AMT": 112, "RESO": 24, "FD": 52}),
         ]),
]
