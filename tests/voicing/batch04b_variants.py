# SPDX-License-Identifier: GPL-3.0-only
"""The variant tables of Batch 4B, Chapter II "the tape / crash pair" (13 Ghost Board, 14 Reef Break): the decisions.  Each variant = the changes over the patch's ORIGINAL (resolved from the
base firmware, so it cannot drift); VOLUME is trimmed by the run.  Names as in obv_params.h without the P_ prefix (DRAIN = REV_MIX, PINGPONG = BBD_SPREAD).
Enums: WAVE 0 off 1 saw 2 pulse 3 both; MODE 0 poly 1 dual 2 unison 3 mono; FTYPE 0 LP12 1 HP12 2 BP12 3 notch 4 LP24 5 SEM; LFO_SHAPE 0 tri .. 5 random; LFO_PHASE 0 sync 1 free 2 spread."""

# ---- 13 Ghost Board -------------------------------------------------------------------------------------------------------------------
# a soft, triangle-leaning tone: a narrow pulse (PW 25 %) through a key-tracking 12 dB low-pass (11 / 16 D's recipe) with a two-octave-up copy of it (the brightness: a 2' register; a single soft pulse alone leaves under 1 % of the energy above 1.2 kHz), a short organ-like tape start, no LFO (the tape is the
# wobble: CHEW), then the chain BBD -> spring -> TAPE: the deck wobbles the whole wet mix
GHOST_B = dict(MODE=0, POLY_N=5, O1_WAVE=2, O1_PW=32, O1_LVL=110, O2_WAVE=2, O2_PW=32, O2_SEMI=48, O2_FINE=64, O2_LVL=112, NOISE=0,
               FTYPE=0, CUTOFF=70, RESO=0, KEYTRK=127, FENV_AMT=64, AA=45, AD=70, AS=127, AR=80,
               LFO_PWM=0, LFO_PITCH=0, VINTAGE=50, SPREAD=100,
               CHEW=100, TP_WOWFLT=48, TP_HISS=40, TP_DROPS=50,
               DLY_FB=82, DLY_TONE=70, DLY_MIX=70, ALLEY=98, BBD_SPREAD=127,
               REV_SIZE=90, REV_DAMP=40, REV_PRE=20, REV_MIX=50)
GHOST_C = {**GHOST_B, "CUTOFF": 64, "O2_LVL": 125, "CHEW": 127, "TP_WOWFLT": 32, "TP_HISS": 32, "DLY_MIX": 40, "DLY_FB": 60, "REV_MIX": 35, "REV_SIZE": 80}
GHOST_D = {**GHOST_B, "CHEW": 70, "TP_WOWFLT": 64, "DLY_MIX": 105, "DLY_FB": 95, "ALLEY": 104, "REV_MIX": 70, "REV_SIZE": 100, "REV_DAMP": 25}

# ---- 14 Reef Break --------------------------------------------------------------------------------------------------------------------
# a noise burst over a square sub, shaped by ONE filter: a 12 dB HIGH-PASS whose cutoff is pushed far down at the strike by a NEGATIVE ENV AMT (0 = -97 semitones at the envelope's peak) and climbs
# back as the filter envelope falls: the sub and the lows pass at the start and go first, the top of the noise rings longest (the cymbal's decay); the amp envelope sets the ring-out; then a long
# BBD echo (the spring is not in this patch's gear list: DRAIN 0)
REEF_B = dict(MODE=0, POLY_N=5, O1_WAVE=2, O1_PW=64, O1_LVL=80, O2_WAVE=2, O2_PW=64, O2_SEMI=36, O2_FINE=64, O2_LVL=45, NOISE=127,
              FTYPE=1, CUTOFF=100, RESO=10, FENV_AMT=0, KEYTRK=0, FA=0, FD=100, FS=0, AA=0, AD=92, AS=0, AR=92, GLIDE=0, VINTAGE=30,
              DLY_FB=96, DLY_TONE=70, DLY_MIX=90, ALLEY=106, BBD_SPREAD=127, REV_MIX=0)
REEF_C = {**REEF_B, "AA": 52, "AD": 97, "AR": 97, "DLY_FB": 100, "DLY_MIX": 80}
REEF_D = {**REEF_B, "AA": 44, "AD": 88, "AR": 88, "FD": 92, "DLY_FB": 114, "DLY_MIX": 100, "ALLEY": 104}

PATCHES = [
    dict(slot=13, dir="13-ghost-board", name="Ghost Board", cname="GHOST_BOARD", kind="plain", level="t_ghost", phrases=["b_stabs", "t_ghost"], recommend="B",
         variants=[("A", "original", "the nearest-base patch as it stood (PWM STRINGS, 13's alone now: two pulses with PWM, LP24, a spring, no echo, no tape, inert LFO PITCH 3)", {}),
                   ("B", "middle", "the middle: soft near-triangle tone, tape CHEW 100 (wow-leaning), echo 275 ms FEEDBK 82 MIX 70, spring DRAIN 50", GHOST_B),
                   ("C", "tape", "leans Mellotron: clearer tone (CUTOFF 60, less octave), the most tape (CHEW 127, wow), less echo (MIX 40, FEEDBK 60) and spring", GHOST_C),
                   ("D", "echo", "leans Space Echo: richer body (CUTOFF 66, more octave), CHEW 70, long rich echo (MIX 110, FEEDBK 100, 387 ms), more spring (DRAIN 80, SIZE 100, DAMP 55)", GHOST_D)]),
    dict(slot=14, dir="14-reef-break", name="Reef Break", cname="REEF_BREAK", kind="plain", level="u_crash", phrases=["b_stabs", "u_crash"], recommend="B",
         variants=[("A", "original", "the nearest-base patch as it stood (PERC HIT, 14's alone: noise 60 + a saw and a saw +24 st, LP12 with a filter envelope, spring, no echo)", {}),
                   ("B", "burst", "near-instant attack, medium tail (top band 20 / 40 dB down in ~0.5 / ~0.9 s), echo FEEDBK 96 MIX 90 at 361 ms", REEF_B),
                   ("C", "swell", "a quick swell (peak in ~10-40 ms), the longest tail, echo FEEDBK 100 MIX 80", REEF_C),
                   ("D", "runaway", "near-instant attack, the shortest tail, a near-runaway echo (FEEDBK 114 MIX 100, 337 ms)", REEF_D)]),
]
