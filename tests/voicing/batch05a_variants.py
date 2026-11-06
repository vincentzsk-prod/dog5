# SPDX-License-Identifier: GPL-3.0-only
"""The variant tables of Batch 5A, Chapter III "the drones" (18 Roto-scopo, 19 Blackwater, 22 Melting Orb): the decisions.  Each variant = the changes over the patch's ORIGINAL (resolved
from the base firmware, so it cannot drift); VOLUME is trimmed by the run.  Names as in obv_params.h without the P_ prefix (DRAIN = REV_MIX, PINGPONG = BBD_SPREAD).
Enums: WAVE 0 off 1 saw 2 pulse 3 both; MODE 0 poly 1 dual 2 unison 3 mono; FTYPE 0 LP12 1 HP12 2 BP12 3 notch 4 LP24 5 SEM; LFO_SHAPE 0 tri 1 saw 2 ramp 3 square 4 S&H 5 random;
LFO_PHASE 0 sync 1 free 2 spread.  LFO RATE = 0.05 x 600^(RATE/127) Hz; LFO FILTER depth = +- (v*v>>7) x 97/256 semitones; ENV>O2 = (v-64) x 24/63 semitones at the filter envelope's top."""

# ---- 18 Roto-scopo ----------------------------------------------------------------------------------------------------------------------
# a moaning dungeon drone: two square waves (the second an octave down: the weight) in a 3-voice UNISON (slop needs several voices on their own cards), a resonant 12 dB low-pass whose cutoff
# is moved by the ONE shared LFO (random / sample-and-hold), VINTAGE ~90 % of its range, dry.  UNISON is monophonic: a chord plays its last key.
ROTO_B = dict(MODE=2, UNI_N=3, UNI_DET=14, O1_WAVE=2, O1_PW=64, O1_LVL=110, O2_WAVE=2, O2_PW=64, O2_LVL=85, O2_SEMI=12, FTYPE=0, CUTOFF=62, RESO=100, FENV_AMT=64, KEYTRK=64,
              LFO_SHAPE=5, LFO_RATE=30, LFO_FLT=70, LFO_PITCH=0, LFO_PHASE=1, VINTAGE=114, SPREAD=127, REV_MIX=0, DLY_MIX=0)
ROTO_C = {**ROTO_B, "LFO_SHAPE": 4, "LFO_RATE": 50}                                    # sample-and-hold steps in place of the smooth random, and faster: a new random cutoff every ~1.6 s (0.62 Hz)
ROTO_D = {**ROTO_B, "LFO_RATE": 15, "LFO_FLT": 90, "CUTOFF": 66, "RESO": 115, "VINTAGE": 127}   # slower, deeper, nearer the edge of self-oscillation, the sloppiest

# ---- 19 Blackwater ----------------------------------------------------------------------------------------------------------------------
# MONO, OSC 1 off, OSC 2 a narrow-ish pulse an octave down (the "sub"), through a 24 dB low-pass at 100 % key tracking so the resonant ring follows the note (cutoff peak ~ 6-12 x the note);
# the filter envelope opens it at the strike and sinks it slowly (the murky decay); held, long release.
BW_B = dict(MODE=3, O1_WAVE=0, O2_WAVE=2, O2_PW=40, O2_LVL=110, O2_SEMI=12, FTYPE=4, CUTOFF=70, RESO=115, KEYTRK=127, FENV_AMT=94, FA=0, FD=105, FS=20,
            AA=20, AD=112, AS=70, AR=105, GLIDE=5)
BW_C = {**BW_B, "RESO": 125}                                                           # past the edge: the filter sings by itself
BW_D = {**BW_B, "CUTOFF": 58, "KEYTRK": 80, "RESO": 110, "FENV_AMT": 100, "FD": 118, "FS": 10, "AD": 118, "AR": 115}   # a low floor, half tracking, the longest decay and release

# ---- 22 Melting Orb ---------------------------------------------------------------------------------------------------------------------
# a dignified collapse: a fat 6-voice UNISON of saws on OSC 2 ONLY (ENV>O2 bends OSC 2's pitch only, driven by the FILTER envelope; OSC 1 is off), the filter envelope rises slowly (FA = the melt
# time) and a NEGATIVE ENV AMT / ENV>O2 turn that rise into a fall of the cutoff and of the pitch together; sustain 127 keeps it down while held; FR 127 so the key-up does not snap it back up.
ORB_B = dict(MODE=2, UNI_N=6, UNI_DET=40, O1_WAVE=0, O1_LVL=0, O2_WAVE=1, O2_PW=64, O2_LVL=110, O2_SEMI=24, ENV_O2=46, FTYPE=0, CUTOFF=100, RESO=75, FENV_AMT=32, KEYTRK=64,
             FA=118, FD=60, FS=127, FR=127, AA=60, AD=100, AS=127, AR=92, VINTAGE=40, SPREAD=110)
ORB_C = {**ORB_B, "FA": 122, "ENV_O2": 32, "RESO": 100, "AR": 100}                                # slower, deeper (12 semitones), more resonance
ORB_D = {**ORB_B, "MODE": 1, "POLY_N": 6}                                              # the same melt as B in DUAL (two detuned voices a note): a 3-key chord melts together

PATCHES = [
    dict(slot=18, dir="18-roto-scopo", name="Roto-scopo", cname="ROTO_SCOPO", level="v_drone_lo", win=(5000, 14000), on=3000,
         phrases=["a_riff", "b_stabs", "c_held", "v_drone_lo", "v_drone_mid", "w_chord_lo", "y_tap"], chord="w_chord_lo", hold=("v_drone_lo", "v_drone_mid"),
         variants=[("A", "original", "the nearest-base patch as it stood (DRONE UNI: 8-voice UNISON of two saws, LP12 RESO 10, slow triangle LFO to the filter +-1 st, spring)", {}),
                   ("B", "random", "3-voice UNISON of two squares (second an octave down), LP12 RESO 100, CUTOFF 62, smooth RANDOM LFO at 0.23 Hz to the filter +-14 st, VINTAGE 114, dry", ROTO_B),
                   ("C", "steps", "B with SAMPLE & HOLD in place of the smooth random, and faster (0.62 Hz = RATE 50: the cutoff jumps to a new random value every ~1.6 s)", ROTO_C),
                   ("D", "slow-deep", "B slower (0.11 Hz) and deeper (+-24 st), CUTOFF 66, RESO 115 (just under self-oscillation), VINTAGE 127", ROTO_D)]),
    dict(slot=19, dir="19-blackwater", name="Blackwater", cname="BLACKWATER", level="v_drone_lo", win=(5000, 14000), on=3000,
         phrases=["a_riff", "b_stabs", "c_held", "v_drone_lo", "v_drone_mid", "w_chord_lo", "y_tap"], chord="w_chord_lo", hold=("v_drone_lo", "v_drone_mid"),
         variants=[("A", "original", "the nearest-base patch as it stood (SUB BASS: MONO, a pulse and a pulse an octave down, LP12 RESO 10, CUTOFF 35, fast envelopes)", {}),
                   ("B", "ring", "OSC 2 pulse (PW 40) an octave down alone, LP24 RESO 115 at 100 % key tracking, filter envelope opens it and sinks over ~2 s, amp decay ~3 s to sustain, release ~2 s", BW_B),
                   ("C", "singing", "B with RESO 125: past the edge, the filter sings by itself", BW_C),
                   ("D", "low-floor", "B with a lower cutoff floor (CUTOFF 58, KEY TRK 80), RESO 110, the longest filter decay / amp decay / release", BW_D)]),
    dict(slot=22, dir="22-melting-orb", name="Melting Orb", cname="MELTING_ORB", level="v_drone_mid", win=(9000, 14000), on=3000,
         phrases=["a_riff", "b_stabs", "c_held", "v_drone_mid", "w_chord_mid", "y_tap"], chord="w_chord_mid", hold=("v_drone_mid",),
         variants=[("A", "original", "the nearest-base patch as it stood (BP QUACK: POLY, band-pass RESO 70, a fast filter-envelope snap, 1 ms attack)", {}),
                   ("B", "melt", "6-voice UNISON of saws on OSC 2, filter and pitch sink together: ~4 s to 90 %, pitch -6.9 st (about a fifth), LP12 RESO 75", ORB_B),
                   ("C", "slow-deep", "B slower (~5.5 s to 90 %), deeper (pitch -12.2 st, about an octave), RESO 100, a slightly longer release", ORB_C),
                   ("D", "dual-chord", "B's melt in DUAL (POLY 6): a three-key chord melts together", ORB_D)]),
]
