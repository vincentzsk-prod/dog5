# SPDX-License-Identifier: GPL-3.0-only
"""Round 2 of Batch 2A (after Vincent's listening): 11 Slapback Strut and 09 Skeenhead.  Each variant = the changes over the COMMITTED variant B (the base tree
of the step); the anchor B is re-rendered through the base program path.  Names as in obv_params.h without the P_ prefix."""
from batch02a_variants import SHORT

SHORT2 = {**SHORT}

E11 = {"CUTOFF": 69, "DRIVE": 30, "FENV_AMT": 64, "FA": 0, "FD": 0, "FS": 127, "FR": 0, "AA": 0, "AD": 0, "AS": 127, "AR": 0}
F11 = {"CUTOFF": 69, "DRIVE": 30, "FENV_AMT": 76, "FA": 0, "FD": 55, "FS": 100, "FR": 10, "AA": 0, "AD": 55, "AS": 100, "AR": 10}
G11 = {**F11, "CUTOFF": 82, "KEYTRK": 90, "O1_PW": 32, "DRIVE": 40, "DLY_TONE": 127, "DLY_FB": 6}
H11 = {**F11, "CUTOFF": 74, "KEYTRK": 110, "O1_PW": 44, "DRIVE": 40, "DLY_TONE": 110, "DLY_FB": 8, "AD": 60, "FD": 60, "AS": 112, "FS": 112}

def _c(r):
    c = r["cost"]
    return f"{c['idle'] + c['load']:.0f}"


def _why11(R):
    B, E, F, G, H = R["B"], R["E"], R["F"], R["G"], R["H"]
    return (f"the blend: a body that holds for the gate with only a {0.5 * 20000 ** (60 / 127):.0f} ms settle (amp and filter DECAY 60 to a sustain a hair under full), a short release, per-voice DRIVE 40 and CUTOFF "
            f"63 -> 74 for the soft top, a 44 % pulse and KEY TRK 110 so the note carries more harmonics and a little less sub, and the slap left at 80 ms with FEEDBK 8. Against B the share of the dry notes above "
            f"400 Hz goes {B['dry_hi']:.1f} -> {H['dry_hi']:.1f} % (the echo, a faithful copy, {B['echo_hi']:.1f} -> {H['echo_hi']:.1f} %), the share of the echo under 150 Hz {B['fx_bands']['<60'] + B['fx_bands']['60-150']:.0f} -> "
            f"{H['fx_bands']['<60'] + H['fx_bands']['60-150']:.0f} %, the first repeat stays at {H['echo']['echo_re_note_db']:+.1f} dB re the note (B {B['echo']['echo_re_note_db']:+.1f}), the second is {H['echo']['repeat2_re_first_db']:.0f} dB under the first "
            f"(B {B['echo']['repeat2_re_first_db']:.0f}); level -18.0 at VOLUME {H['volume']} (B 122), peak {H['peak_all']:.1f}; the echo is gone {H['rel']['t60']:.0f} ms after the note (B {B['rel']['t60']:.0f}). CPU {_c(H)} worst case (B {_c(B)}). "
            f"E is the zero-decay version (hi share {E['dry_hi']:.1f} %: gated and dull), F the minimal-decay one ({F['dry_hi']:.1f} %), G the crispest ({G['dry_hi']:.1f} % above 400 Hz, echo {G['fx_bands']['<60'] + G['fx_bands']['60-150']:.0f} % under 150 Hz, but "
            f"harmonics 3 / 5 / 7 at {G['tri'][1]:.0f} / {G['tri'][2]:.0f} / {G['tri'][3]:.0f} dB: nearly a square).")


LISTEN11 = """`*_surf.wav` is the one to judge (B_anchor first, then H, F, G, E): is the slap crisp and clear, is the soft top there without dullness, is the note tight. `*_riff.wav` and `*_stabs.wav` are the pilot phrases.
Listen for: the gated character (the note no longer plucks, it holds and stops), whether G's top is too buzzy and whether H or F is the right amount of brightness."""
NOTES11 = """*Notes.* Echo clarity: the echo is a faithful copy of the note, so its band shares follow the dry note's; the rows compare them over the same stretch (3.2 .. 10.9 s). ALLEY's TONE has almost no effect on this bass (TONE 70 -> 127 moves the echo's centroid by 1 Hz:
the note has nothing near the TONE filter's range); the crispness has to come from the note. The delay path leaves a constant -76 dBFS DC behind a driven voice (inaudible); tails are read with it removed. B_anchor is rendered through the base program path."""

PATCHES_R2 = [
    dict(slot=11, dir="11-slapback-strut", name="Slapback Strut", cname="SLAPBACK_STRUT", kind="echo", level="h_surf", level_def="RMS over the note-on region of the surf riff (phrase h), echo included",
         recommend="H blend", why=_why11, listen=LISTEN11, notes=NOTES11, short=SHORT2, phrases=["a_riff", "b_stabs", "c_held", "h_surf"], load="a fifth-and-octave chord + a fourth note",
         variants=[("B", "anchor", "the committed B re-rendered through the base program path", {}),
                   ("E", "nodecay", "decay ZERO: amp and filter DECAY 0, SUSTAIN full, RELEASE shortest, ATTACK 0; a little DRIVE, CUTOFF up a touch; a gated note, no pluck", E11),
                   ("F", "minimal", "decay MINIMAL: a ~36 ms settle to a sustain just under full on both envelopes, 1 ms releases; a little DRIVE, CUTOFF up a touch", F11),
                   ("G", "crisp", "F with the most crisp slapback: CUTOFF higher, KEY TRK lower, a narrow pulse (less sub, more harmonics), more DRIVE, TONE open, FEEDBK lower", G11),
                   ("H", "blend", "my best blend: F's body, a 44 % pulse, KEY TRK 110, CUTOFF 74, DRIVE 40, TONE 110, FEEDBK 8", H11)]),
]
