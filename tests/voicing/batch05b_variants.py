# SPDX-License-Identifier: GPL-3.0-only
"""Batch 5B variant tables (20 Fire & Ice, 23 Crypt Dust, 24 Fugue State).  Each variant = the CHANGES over the patch's ORIGINAL (resolved from the base firmware, the commit before this batch);
A is the original through the base program path.  VOLUME is trimmed by the run.  Names as in obv_params.h without the P_ prefix.
Enums: WAVE 0 off 1 saw 2 pulse 3 saw+pulse; FTYPE 0 LP12 1 HP12 2 BP12 3 notch 4 LP24 5 SEM; LFO_SHAPE 0 tri 1 saw 2 ramp 3 square 4 S&H 5 random; LFO_PHASE 0 sync 1 free 2 spread; MODE 0 poly 1 dual 2 unison 3 mono.
LFO RATE = 0.05 x 600^(RATE/127) Hz; LFO PITCH peak = ((v*v)>>7) x 9.375 cents (inert below 12); LFO FILTER peak = ((v*v)>>7) x 97/256 semitones; LFO AMP v = a dip of up to v/128 of the level; PW byte 64 = 50 %, 32 = 25 %."""

# ---- 20 Fire & Ice: the cutoff axis (rolled off -> open); the drench, the glide and the sweep depth are shared ----------------------------------------------------------
ECHO20 = dict(O2_LVL=127, ALLEY=107, DLY_FB=92, DLY_TONE=55, DLY_MIX=85, BBD_SPREAD=127, REV_MIX=30, REV_SIZE=80, GLIDE=56, AR=50)
V20 = {
    "B": ("rolled", "the brief: tone rolled off (CUTOFF 54), the filter envelope opens it on the strike so some of the sweep survives; GROWL 70", dict(CUTOFF=54, FENV_AMT=127, RESO=14, GROWL=70, **ECHO20)),
    "C": ("half", "half closed (CUTOFF 66), GROWL 60", dict(CUTOFF=66, FENV_AMT=105, RESO=12, GROWL=60, **ECHO20)),
    "D": ("open", "moderately open (CUTOFF 84), GROWL 48: the sweep is the star", dict(CUTOFF=84, FENV_AMT=85, RESO=10, GROWL=48, **ECHO20)),
}

# ---- 23 Crypt Dust: the tape ladder (heavy -> moderate -> none) -------------------------------------------------------------------------------------------------------------------
# a thin pulse (OSC 1, PW 12 %) under the noise, both through the BP12 (key tracking at its default); no GROWL
DUST = dict(POLY_N=2, O1_WAVE=2, O1_PW=15, O1_LVL=127, NOISE=127, CUTOFF=72, RESO=50, GROWL=0)
V23 = {
    "B": ("heavy", "the brief as written: heavy tape wow (CHEW 100, WOW/FLT 16 = mostly wow), DROPS 90, HISS 64 (CHEW's own)", dict(**DUST, CHEW=100, TP_WOWFLT=16, TP_DROPS=90, TP_HISS=64)),
    "C": ("half", "about half of B's CHEW (50), the rest of the tape settings as B", dict(**DUST, CHEW=50, TP_WOWFLT=16, TP_DROPS=90, TP_HISS=64)),
    "D": ("tapeless", "CHEW 0; the crumble from the one LFO (S&H) on AMP and FILTER, a short echo and the spring", dict(**DUST, CHEW=0, LFO_SHAPE=4, LFO_RATE=58, LFO_PHASE=1, LFO_AMP=46, LFO_FLT=45, LFO_PITCH=0, LFO_PWM=0,
                                                                                  ALLEY=60, DLY_FB=60, DLY_TONE=55, DLY_MIX=85, BBD_SPREAD=127, REV_MIX=80)),
}

# ---- 24 Fugue State: a narrow pulse (25 %) through a key-tracking 12 dB low-pass, an octave-up copy, a TRI pitch LFO ---------------------------------------------------------------
FUGUE = dict(MODE=0, POLY_N=5, O1_WAVE=2, O1_PW=32, O1_LVL=110, O2_WAVE=2, O2_PW=32, O2_LVL=45, O2_SEMI=36, O2_FINE=66, FTYPE=0, CUTOFF=63, RESO=5, KEYTRK=127, FENV_AMT=64, ENV_O2=64,
             LFO_SHAPE=0, LFO_PHASE=2, LFO_PWM=0, LFO_FLT=0, LFO_AMP=0, LFO_PITCH_TO=2, LFO_DELAY=0, AA=85, AD=100, AS=127, AR=110, VINTAGE=60, SPREAD=120,
             REV_MIX=45, REV_SIZE=100, REV_DAMP=60, REV_PRE=30, BBD_SPREAD=127, DLY_TONE=45, DLY_TIME=5)
V24 = {
    "B": ("lurch", "slow lurch: LFO 0.31 Hz, +-4.7 st (PITCH 80), FEEDBK 100, echo 266 ms", dict(**FUGUE, LFO_RATE=36, LFO_PITCH=80, ALLEY=97, DLY_FB=100, DLY_MIX=85)),
    "C": ("wobble", "fast wobble: LFO 4.9 Hz, +-1.8 st (PITCH 50), FEEDBK 95, echo 144 ms", dict(**FUGUE, LFO_RATE=91, LFO_PITCH=50, ALLEY=79, DLY_FB=95, DLY_MIX=85)),
    "D": ("seasick", "middle rate and the deepest: LFO 1.1 Hz, +-7.3 st (PITCH 100), FEEDBK 110, echo 266 ms", dict(**FUGUE, LFO_RATE=62, LFO_PITCH=100, ALLEY=97, DLY_FB=110, DLY_MIX=85)),
}
