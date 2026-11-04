# SPDX-License-Identifier: GPL-3.0-only
"""Round 2 of Batch 2A (after Vincent's listening): 11 Slapback Strut and 09 Skeenhead.  Each variant = the changes over the COMMITTED variant B (the base tree
of the step); the anchor B is re-rendered through the base program path.  Names as in obv_params.h without the P_ prefix."""
from batch02a_variants import SHORT

SHORT2 = {**SHORT}

E11 = {"CUTOFF": 69, "DRIVE": 30, "FENV_AMT": 64, "FA": 0, "FD": 0, "FS": 127, "FR": 0, "AA": 0, "AD": 0, "AS": 127, "AR": 0}
F11 = {"CUTOFF": 69, "DRIVE": 30, "FENV_AMT": 76, "FA": 0, "FD": 55, "FS": 100, "FR": 10, "AA": 0, "AD": 55, "AS": 100, "AR": 10}
G11 = {**F11, "CUTOFF": 82, "KEYTRK": 90, "O1_PW": 32, "DRIVE": 40, "DLY_TONE": 127, "DLY_FB": 6}
H11 = {**F11, "CUTOFF": 74, "KEYTRK": 110, "O1_PW": 44, "DRIVE": 40, "DLY_TONE": 110, "DLY_FB": 8, "AD": 60, "FD": 60, "AS": 112, "FS": 112}


# ---- 09 Skeenhead round 2: the note's body (the filter must not shut below the notes), then the spring dialled back ----
BODY09 = {"CUTOFF": 46, "FS": 40, "AS": 64}                                  # E: body fix only, spring as B (DRAIN 90, SIZE 70, DAMP 40, PRE-DLY 4)
SPR_F = {"REV_MIX": 77, "REV_SIZE": 62, "REV_PRE": 2}
SPR_G = {"REV_MIX": 56, "REV_SIZE": 50, "REV_PRE": 0}
H09 = {**BODY09, "AS": 70, "AD": 62, "VINTAGE": 8, "AR": 20, "O2_WAVE": 2, "O2_SEMI": 36, "O2_LVL": 50, "DRIVE": 30, "REV_MIX": 66, "REV_SIZE": 58, "REV_PRE": 0}


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


def _why09(R):
    B, E, F, G, H = R["B"], R["E"], R["F"], R["G"], R["H"]
    w = lambda r, i: r["win"][i]
    return (f"the body kept: the filter now rests at CUTOFF 46 with a sustain of 40 (it was shutting below the notes within ~25 ms), the amp holds 70 of 127 through the gate, so the dry stab is {w(H, 0)['dry_db']:.1f} dB in its first "
            f"20 ms and {w(H, 1)['dry_db']:.1f} dB over 20-100 ms (B {w(B, 0)['dry_db']:.1f} / {w(B, 1)['dry_db']:.1f}) with {w(H, 1)['dry_bands']['400-1.2k'] + w(H, 1)['dry_bands']['1.2k+']:.0f} % of that body above 400 Hz (B {w(B, 1)['dry_bands']['400-1.2k'] + w(B, 1)['dry_bands']['1.2k+']:.1f} %); "
            f"the plop is still there (first 23 ms {H['snap'][0]:.0f} Hz against {H['snap'][1]:.0f} Hz). The spring is dialled back to {H['fx_re_dry_db']:.1f} dB re the dry stab (B {B['fx_re_dry_db']:.1f}): per window {' / '.join(f'{x['spr_db'] - x['dry_db']:+.1f}' for x in H['win'])} dB "
            f"(B {' / '.join(f'{x['spr_db'] - x['dry_db']:+.1f}' for x in B['win'])}), so it is under the note while the note sounds, with the same tone (DAMP 40, DRAIN 66, SIZE 58, PRE-DLY 0), tail {H['rel']['t60'] / 1000:.2f} s to -60 dB (B {B['rel']['t60'] / 1000:.2f}). "
            f"Tighter and steadier: VINTAGE 8 (B 30), AMP RELEASE 2 ms, a second pulse an octave up at low level for definition, a little DRIVE. Level {H['level']:.1f} dBFS at VOLUME {H['volume']} (B 115), peak {H['peak_all']:.1f} (B {B['peak_all']:.1f}). CPU {_c(H)} (B {_c(B)}). "
            f"E is the body fix alone (spring as B, {E['fx_re_dry_db']:.1f} dB), F the spring a bit down ({F['fx_re_dry_db']:.1f}), G further down and tighter ({G['fx_re_dry_db']:.1f}).")


LISTEN09 = """`*_skank.wav` is the one to judge (B_anchor first, then E to H): does the NOTE now have body and sit in front of its spring, is the plop still a plop, is the spring still the same tone but under the note, does H cut through.
`*_stabs.wav` is the pilot phrase. Listen for: E against B (the body alone), then how far down the spring can go before the chirp is lost (F, G)."""
NOTES09 = """*Notes.* The body numbers are read on the stab at 7.25 s (A3 C4 after the 1.4 s gap), dry, in 0-20 / 20-100 / 100-250 ms; the gate is 110 ms so the last window is 10 ms of note and the spring. The spring-re-dry in the table's headline row is the energy over the stabs' note-on
regions (B's -4.2 definition); per window it is in the rows below. PRE-DLY on the knob 4 is 1.1 ms. The trim is limited by the peak guard (-4.3 dBFS, any phrase); the phrase that peaks highest is named in the table. B_anchor is rendered through the base program path."""

PATCHES_R2.append(
    dict(slot=9, dir="09-skeenhead", name="Skeenhead", cname="SKEENHEAD", kind="spring", level="g_skank", level_def="RMS over the stabs' note-on region of the skank (phrase g), spring included",
         recommend="H blend", why=_why09, listen=LISTEN09, notes=NOTES09, short=SHORT2, phrases=["a_riff", "b_stabs", "c_held", "g_skank"], load="a fifth-and-octave chord + a fourth note",
         variants=[("B", "anchor", "the committed B re-rendered through the base program path", {}),
                   ("E", "body", "the body fix alone: the filter rests higher (CUTOFF 46) and holds (SUSTAIN 40), the amp holds 64 through the gate; the spring exactly as B", BODY09),
                   ("F", "spring1", "E with the spring dialled back slightly (to about -7 dB re dry): DRAIN 77, SIZE 62, PRE-DLY 2", {**BODY09, **SPR_F}),
                   ("G", "spring2", "E with the spring dialled back more and tighter (about -10 dB re dry): DRAIN 56, SIZE 50, PRE-DLY 0", {**BODY09, **SPR_G}),
                   ("H", "blend", "my best blend for cutting through a reggae track: E's body, a second pulse an octave up for definition, a little DRIVE, VINTAGE 8, a 2 ms release, the spring at about -9 dB re dry", H09)]))
