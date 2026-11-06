# SPDX-License-Identifier: GPL-3.0-only
"""Batch 5A round 2: the variant tables of the NEW slot 19, "Micro-mist" (neon pixels floating in the ether).  There is no original: A-D are four fresh takes, each a FULL parameter list over INIT
(VOLUME is trimmed by the run).  Names as in obv_params.h without the P_ prefix (DRAIN = REV_MIX, PINGPONG = BBD_SPREAD).
Enums: WAVE 1 saw 2 pulse; FTYPE 0 LP12 1 HP12 2 BP12 3 notch; LFO_SHAPE 0 tri 4 S&H 5 random; LFO_PHASE 0 sync 1 free 2 spread.  LFO RATE = 0.05 x 600^(RATE/127) Hz; LFO PITCH = +- (v*v>>7) x 24 / 256 semitones
(inert below 12); LFO FILTER = +- (v*v>>7) x 97 / 256 semitones; LFO AMP v = a dip of up to v/128 of the level; ALLEY ms = batch04a_metrics.alley_ms."""

# the shared voice: POLY 6 (a three-key chord keeps its release tails), a saw and (an octave up, slightly detuned) a square (OSC 2 +12 st, FINE +6 cents beats), a band-pass at a high cutoff (the glass), a soft attack
MIST = dict(MODE=0, POLY_N=6, O1_WAVE=1, O1_LVL=127, O2_WAVE=2, O2_LVL=100, O2_SEMI=36, O2_FINE=72, FTYPE=2, CUTOFF=74, RESO=50, KEYTRK=64, FENV_AMT=74, FA=75, FD=90, FS=90,
            AA=70, AD=100, AS=110, AR=95, LFO_SHAPE=4, LFO_RATE=105, LFO_PHASE=2, LFO_PITCH=16, LFO_FLT=40, LFO_AMP=20, VINTAGE=40, SPREAD=100,
            DLY_FB=90, DLY_TONE=100, DLY_MIX=90, ALLEY=90, BBD_SPREAD=127, REV_MIX=70, REV_SIZE=110, REV_DAMP=20, REV_PRE=10)

MIST_A = {**MIST, "O2_SEMI": 43, "O2_FINE": 76, "O2_LVL": 110, "CUTOFF": 78, "LFO_RATE": 113, "LFO_PITCH": 20, "LFO_FLT": 50, "LFO_AMP": 30, "REV_MIX": 100, "REV_SIZE": 127, "REV_DAMP": 15, "ALLEY": 80, "DLY_FB": 80, "DLY_MIX": 70}
MIST_B = {**MIST, "LFO_SHAPE": 5, "LFO_RATE": 60, "LFO_PITCH": 22, "LFO_FLT": 30, "LFO_AMP": 8, "ALLEY": 110, "DLY_FB": 96, "DLY_MIX": 90}
MIST_C = {**MIST, "RESO": 85, "CUTOFF": 80, "LFO_RATE": 100, "LFO_PITCH": 0, "AA": 76, "FENV_AMT": 70, "ALLEY": 100, "DLY_FB": 90, "DLY_MIX": 120, "REV_MIX": 30}
MIST_D = {**MIST, "CUTOFF": 70, "RESO": 40, "AA": 80, "AS": 127, "LFO_PITCH": 0, "LFO_FLT": 10, "LFO_AMP": 0, "DLY_FB": 105, "DLY_MIX": 95, "ALLEY": 100, "REV_MIX": 80}

PATCH = dict(slot=19, dir="19-micro-mist", name="Micro-mist", cname="MICRO_MIST", level="z_chord", win=(4000, 10000), on=3000,
             phrases=["z_chord", "z_tap", "a_riff", "b_stabs", "z_single"], wav=["z_chord", "z_tap", "a_riff", "b_stabs"],
             variants=[("A", "haze", "dense fast flicker, wide shimmer, big spring", MIST_A),
                       ("B", "glide", "slow drifting scatter, long echo", MIST_B),
                       ("C", "warp", "resonant band-pass glassy top, the echo repeats the main event", MIST_C),
                       ("D", "tunnel", "a held pad hovering on near-100 feedback, minimal flicker", MIST_D)])
