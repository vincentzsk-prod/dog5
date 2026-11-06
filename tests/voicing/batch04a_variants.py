# SPDX-License-Identifier: GPL-3.0-only
"""The variant tables of Batch 4A, Chapter II "the spring / organ / wash set" (10 Atlantic Swell, 12 Kelp Tangle, 16 Tidal Pull): the decisions.
Each variant = the changes over the patch's ORIGINAL (resolved from the base firmware, so it cannot drift); VOLUME is trimmed by the run.  Names as in obv_params.h without
the P_ prefix (DRAIN = REV_MIX, PINGPONG = BBD_SPREAD).
Enums: WAVE 0 off 1 saw 2 pulse 3 both; MODE 0 poly 1 dual 2 unison 3 mono; FTYPE 0 LP12 1 HP12 2 BP12 3 notch 4 LP24 5 SEM;
LFO_SHAPE 0 tri 1 saw 2 ramp 3 square 4 S&H 5 random; LFO_PHASE 0 sync 1 free 2 spread; LFO_PITCH_TO / LFO_PWM_TO 0 osc1 1 osc2 2 both."""

# ---- 10 Atlantic Swell ----------------------------------------------------------------------------------------------------------------
# a combo organ: two narrow pulses (8' and 4' registers, exact octave), organ keying (3 ms attack, full sustain, 29 ms release), an open 12 dB low-pass (cold, clear),
# DUAL = two voices per note panned left / right, a slow TRI LFO on pitch with PHASE SPREAD (each card 45 degrees on: the two voices of a note wobble out of step = the chorus),
# a heavy BBD (ping-pong, ~360 ms, feedback 95, bright TONE) and only a touch of spring
ORG_B = dict(MODE=1, POLY_N=6, UNI_DET=30, O1_WAVE=2, O1_PW=26, O1_LVL=110, O2_WAVE=2, O2_PW=26, O2_LVL=84, O2_SEMI=36, O2_FINE=64,
             FTYPE=0, CUTOFF=104, RESO=22, KEYTRK=64, FENV_AMT=64, DRIVE=0,
             AA=18, AD=70, AS=127, AR=52,
             LFO_SHAPE=0, LFO_RATE=53, LFO_PHASE=2, LFO_DELAY=0, LFO_PITCH=16, LFO_PITCH_TO=2, LFO_PWM=0, LFO_AMP=0,
             VINTAGE=30, SPREAD=127,
             DLY_FB=95, DLY_TONE=90, DLY_MIX=100, ALLEY=106, ALLEY_FINE=0, BBD_SPREAD=127,
             REV_SIZE=70, REV_DAMP=30, REV_PRE=20, REV_MIX=24)
ORG_C = {**ORG_B, "LFO_PITCH": 22, "LFO_RATE": 56, "DLY_FB": 104, "DLY_MIX": 118, "ALLEY": 108}
ORG_D = {**ORG_B, "LFO_AMP": 45, "LFO_RATE": 56, "LFO_PHASE": 1}

# ---- 12 Kelp Tangle -------------------------------------------------------------------------------------------------------------------
# a murky PWM pad: two pulses a few cents apart, BOTH swept by the LFO's TRI on one side of 50 % (PW 44 = 35 %, +-12 points: 23-47 %), a key-tracking 24 dB low-pass
# (CUTOFF = how many harmonics of the note get through), LFO PHASE SYNC (every detached note starts its sweep together), a spring tail
KELP_B = dict(MODE=0, POLY_N=5, O1_WAVE=2, O1_PW=42, O1_LVL=110, O2_WAVE=2, O2_PW=42, O2_LVL=100, O2_SEMI=24, O2_FINE=73,
              FTYPE=4, CUTOFF=86, RESO=30, KEYTRK=127, FENV_AMT=64, DRIVE=0,
              AA=52, AD=70, AS=127, AR=88, FA=20,
              LFO_SHAPE=0, LFO_RATE=60, LFO_PHASE=0, LFO_DELAY=0, LFO_PITCH=0, LFO_PWM=100, LFO_PWM_TO=2, LFO_FLT=0, LFO_AMP=0,
              VINTAGE=50, SPREAD=100,
              REV_SIZE=75, REV_DAMP=30, REV_PRE=20, REV_MIX=55)
KELP_C = {**KELP_B, "CUTOFF": 98}
KELP_D = {**KELP_B, "LFO_RATE": 76, "LFO_PWM": 105, "LFO_PHASE": 2}

# ---- 16 Tidal Pull --------------------------------------------------------------------------------------------------------------------
# a Juno-style pulse wash: five POLY voices of two detuned PULSES (never a square: PW 44 and 30), a TRI (or smooth RANDOM) LFO at a medium rate on pitch +-19 cents and on the
# pulse widths, PHASE SPREAD (the five voices are 45 degrees apart: wide), a bright key-tracking low-pass, a medium attack, a clear ping-pong BBD echo and the spring
TIDE_B = dict(MODE=0, POLY_N=5, O1_WAVE=2, O1_PW=44, O1_LVL=110, O2_WAVE=2, O2_PW=30, O2_LVL=100, O2_SEMI=24, O2_FINE=73,
              FTYPE=0, CUTOFF=100, RESO=8, KEYTRK=100, FENV_AMT=64, DRIVE=0,
              AA=72, AD=70, AS=127, AR=92, FA=20,
              LFO_SHAPE=0, LFO_RATE=64, LFO_PHASE=2, LFO_DELAY=0, LFO_PITCH=16, LFO_PITCH_TO=2, LFO_PWM=80, LFO_PWM_TO=2, LFO_AMP=0,
              VINTAGE=50, SPREAD=127,
              DLY_FB=78, DLY_TONE=100, DLY_MIX=100, ALLEY=104, ALLEY_FINE=0, BBD_SPREAD=127,
              REV_SIZE=90, REV_DAMP=35, REV_PRE=20, REV_MIX=45)
TIDE_C = {**TIDE_B, "LFO_SHAPE": 5, "LFO_RATE": 70, "AA": 78, "REV_MIX": 65, "DLY_MIX": 90}
# D: the oscillators softened toward a triangle / sine-like tone (11's recipe: a narrow pulse through a key-tracking 12 dB low-pass; here at 2.0 x the note, plus an octave-up pulse the same way)
TIDE_D = {**TIDE_B, "O1_PW": 32, "O2_PW": 32, "O2_SEMI": 36, "O2_LVL": 84, "O2_FINE": 66, "CUTOFF": 64, "KEYTRK": 127, "RESO": 0, "LFO_PWM": 0, "LFO_RATE": 76,
          "AA": 82, "DLY_MIX": 110}

PATCHES = [
    dict(slot=10, dir="10-atlantic-swell", name="Atlantic Swell", cname="ATLANTIC_SWELL", kind="plain", level="q_organ", phrases=["b_stabs", "q_organ"], recommend="B",
         variants=[("A", "original", "the nearest-base patch as it stood (HOLLOW PAD, shared with 12: POLY, two inverse narrow pulses through a notch, no vibrato, no delay)", {}),
                   ("B", "june", "clear chorus first: DUAL pair (L / R), TRI LFO 0.72 Hz on pitch +-19 cents with PHASE SPREAD, organ keying, BBD 361 ms FEEDBK 95 MIX 100, a touch of spring", ORG_B),
                   ("C", "wooze", "B along the depth axis: pitch +-28 cents at 0.84 Hz (vibrato-led), and a heavier echo (387 ms, FEEDBK 104, MIX 118)", ORG_C),
                   ("D", "leslie", "B with a tremolo on the same LFO (AMP 45, a 3.8 dB dip) and PHASE FREE so every voice swings together: vibrato and tremolo at one rate, 0.84 Hz (the rotary-speaker idea)", ORG_D)]),
    dict(slot=12, dir="12-kelp-tangle", name="Kelp Tangle", cname="KELP_TANGLE", kind="plain", level="r_tangle", phrases=["b_stabs", "r_tangle"], recommend="B",
         variants=[("A", "original", "the nearest-base patch as it stood (HOLLOW PAD: narrow inverse pulses through a notch, PWM +-2 points: not audible as PWM)", {}),
                   ("B", "murk", "murk first: LP24 CUTOFF 86 at 100 % key tracking, RESO 30, PWM +-15 points around 33 % (18-48 %), TRI 1.03 Hz, PHASE SYNC, spring DRAIN 55", KELP_B),
                   ("C", "open", "B along the cutoff axis: CUTOFF 98 (more of each note's harmonics through the filter)", KELP_C),
                   ("D", "tangle", "B along the rate / depth axis: PWM +-16.8 points, TRI 2.3 Hz, PHASE SPREAD (each voice 45 degrees on)", KELP_D)]),
    dict(slot=16, dir="16-tidal-pull", name="Tidal Pull", cname="TIDAL_PULL", kind="plain", level="s_wash", phrases=["b_stabs", "s_wash"], recommend="B",
         variants=[("A", "original", "the nearest-base patch as it stood (PWM STRINGS, shared with 13 Ghost Board: no delay, spring only, inert LFO PITCH 3)", {}),
                   ("B", "tri", "TRI LFO 1.26 Hz on pitch +-19 cents and the pulse widths, pulses, attack 101 ms to 90 %, the echo ahead of the spring (DLY MIX 100, DRAIN 45)", TIDE_B),
                   ("C", "random", "smooth RANDOM LFO ~1.7 Hz, attack 160 ms, the spring ahead of the echo (DRAIN 65, DLY MIX 90)", TIDE_C),
                   ("D", "soft", "the oscillators softened toward a triangle (narrow pulses through a key-tracking low-pass, an octave stack), TRI 2.3 Hz, attack 219 ms, echo up (MIX 110)", TIDE_D)]),
]
