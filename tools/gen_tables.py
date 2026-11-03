#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""OberVave's fixed-point tables (the chip has no FPU): tools/gen_tables.py -> firmware/gen/obv_tables.h
(committed, so a build needs no regeneration). FS = 44100, control rate every CTL = 16 frames."""
import math
import sys
from pathlib import Path

FS = 44100
CTL = 16


def arr(name, ctype, vals, per=10):
    out = [f"static const {ctype} {name}[{len(vals)}] = {{"]
    for i in range(0, len(vals), per):
        out.append("    " + ", ".join(str(v) for v in vals[i:i + per]) + ",")
    out.append("};")
    return out


def k_block(tau_s):
    """one-pole coefficient per control block, Q24: level += (target - level) * k >> 24"""
    return max(1, min((1 << 24) - 1, int(round((1 << 24) * (1 - math.exp(-CTL / (tau_s * FS)))))))


def growl_tables():
    """GROWL, the preamp drive (firmware/src/obv_drive.h). Levels are at the drive's scale (the voice bus >> 2): one
    voice of a plain saw peaks at ~1400 there (tests/drive measured 1396; a chord ~6200, the bright mono lead ~2500)."""
    one_voice = 1400.0
    L = []
    # the gain into the soft clip (32768 = tanh's 1), Q4 (it multiplies the full-resolution bus, 4x the drive's scale):
    # one voice from 0.2 (warmth) to 16 (fuzz) in tanh's units, exponential
    gain = [0.0] + [0.2 * 32768 / one_voice * 80 ** ((v - 1) / 126) for v in range(1, 128)]
    L += arr("GRL_G_Q4", "uint16_t", [int(round(16 * g)) for g in gain])

    # the pre-clip low-pass (two one-poles), k Q12 (on the full-resolution bus): open up to 25, then 14 kHz down to
    # 3 kHz at 127 -- a high-gain stage's bandwidth falls (as the classic op-amp fuzz's does), and it keeps the clipped
    # edges from aliasing
    def k14(hz):
        return min(16384, int(round(16384 * (1 - math.exp(-2 * math.pi * hz / FS)))))
    L += arr("GRL_KPRE", "uint16_t", [4096 if v <= 25 else int(round(4096 * (1 - math.exp(
        -2 * math.pi * 14000 * (3000 / 14000) ** ((v - 25) / 102) / FS)))) for v in range(128)])
    # TONE (the post one-pole), k Q14: 1.2 kHz .. open (50, the slot's default, is ~4.5 kHz)
    L += arr("GRL_KTONE", "uint16_t", [k14(1200 * 28.7 ** (v / 127)) for v in range(128)])
    # how much of TONE a GROWL setting gets, 0..256: none at a gentle drive (it stays open), all of it from 40
    L += arr("GRL_TONEW", "uint16_t", [min(256, int(round(256 * (v / 40) ** 1.5))) for v in range(128)])

    # the static makeup, Q15: a saw at one voice's level comes out at its own RMS (the soft clip is the tanh table, flat
    # beyond 2, as obv_drive.h). The trim (obv_drive.h) matches the rest (chords, other levels)
    def sat(z):
        return math.copysign(math.tanh(min(abs(z), 2.0)), z)
    n = 512
    saw = [one_voice * (2 * i / n - 1) for i in range(n)]
    rms_in = math.sqrt(sum(x * x for x in saw) / n)
    mk = [32768]
    for v in range(1, 128):
        g = gain[v]
        out = [32767 * sat(g * x / 32768) for x in saw]
        mk.append(min(32767, int(round(32768 * rms_in / math.sqrt(sum(y * y for y in out) / n)))))
    L += arr("GRL_M_Q15", "uint16_t", mk)
    return L


def tape_tables():
    """TAPE, the CHEW macro (firmware/src/obv_tape.h): per CHEW 0..127. The tape line runs at 2x (88.2 kHz)."""
    L = []
    fs2 = 2 * FS
    a = [v / 127 for v in range(128)]
    # wow: peak pitch deviation 1.4 % (24 cents) at CHEW 127, a^1.4 on the way (0.53 % at 64, 0.2 % at 32). The wow is
    # 0.7 sin(0.55 Hz) + 0.3 sin(1.37 Hz) (obv_tape.h): its slope peaks at 2 pi (0.7 0.55 + 0.3 1.37) of the depth
    wslope = 2 * math.pi * (0.7 * 0.55 + 0.3 * 1.37)
    L += arr("TP_WOW_Q8", "uint16_t", [int(round(256 * 0.014 * x ** 1.4 * fs2 / wslope)) for x in a])
    # flutter: up to 0.3 % peak, coming in from CHEW 20 % (wow first, then flutter, then dropouts): 0.65 sin(9.1 Hz)
    # + 0.35 band-limited noise (~15 Hz)
    fslope = 2 * math.pi * (0.65 * 9.1 + 0.35 * 15)
    L += arr("TP_FLT_Q8", "uint16_t", [int(round(256 * 0.003 * max(0.0, (x - 0.2) / 0.8) ** 1.2 * fs2 / fslope))
                                       for x in a])
    # the saturation's share (the tanh at 1.5, blended in), Q12
    L += arr("TP_SAT_Q12", "uint16_t", [int(round(4096 * x ** 1.2)) for x in a])
    # the head loss: two one-poles, k Q14, from ~30 kHz (all but open) down to 7.5 kHz each at 127; 0 = open
    def k14(hz):
        return min(16384, int(round(16384 * (1 - math.exp(-2 * math.pi * hz / FS)))))
    L += arr("TP_KHL_Q14", "uint16_t", [16384 if v == 0 else k14(7500 * 4 ** (1 - a[v] ** 0.7)) for v in range(128)])
    # the head bump (the difference of a 200 Hz and a 60 Hz one-pole, ~+2 dB near 100 Hz at 127), Q12
    L += arr("TP_BUMP_Q12", "uint16_t", [int(round(4096 * 0.62 * x)) for x in a])
    # the hiss at HISS 64 (0 dB): RMS -50 dBFS at 127, -86 at 1 (-50 - 36 (1 - a)^1.5). The source: uniform noise
    # +-32768 through a 400 Hz high-pass and a 7 kHz low-pass (one-poles, as obv_tape.h); its RMS simulated here.
    # Gain Q20 (obv_tape.h applies it as (noise >> 1) * g >> 19)
    import random
    rnd = random.Random(1)
    khp, klp, lp1, lp2, ss, N = 1 - math.exp(-2 * math.pi * 400 / FS), 1 - math.exp(-2 * math.pi * 7000 / FS), 0.0, 0.0, 0.0, 200000
    for i in range(N):
        n = rnd.uniform(-32768, 32768)
        lp1 += (n - lp1) * khp
        lp2 += ((n - lp1) - lp2) * klp
        ss += lp2 * lp2
    rms = math.sqrt(ss / N)
    L += arr("TP_HISS_Q20", "uint16_t", [0 if v == 0 else min(65535, int(round((1 << 20) * 32768 * 10 ** (
        (-50 - 36 * (1 - a[v]) ** 1.5) / 20) / rms))) for v in range(128)])
    # HISS (SELECT held + KNOB 2): 0 off, 1..127 = -12 .. +12 dB around the macro's own level, Q12
    L += arr("TP_DB12_Q12", "uint16_t", [0 if v == 0 else int(round(4096 * 10 ** ((v - 64) * 12 / 63 / 20)))
                                         for v in range(128)])
    # the dropouts' ramp, Q12: none below CHEW 45 %, then up (rate ~ ramp^2, depth with ramp: obv_tape.h)
    L += arr("TP_DRAMP_Q12", "uint16_t", [int(round(4096 * max(0.0, (x - 0.45) / 0.55))) for x in a])
    # the static makeup, Q12: -0.6 dB at 127 (the four test sources' mean; the slow trim in obv_tape.h does the rest)
    L += arr("TP_MK_Q12", "uint16_t", [int(round(4096 * 10 ** (-0.6 * x / 20))) for x in a])
    return L


def bbd_tables():
    """ALLEY, the BBD delay (firmware/src/obv_fx.h). Index 1..127 = the free time, 10 ms .. 740 ms, exponential
    (3.5 % a step; P_ALLEY_FINE splits a step in 128). The repeats' bandwidth falls as the time grows, as a BBD's does
    (a fixed number of buckets: a longer delay is a slower clock): each pass through the line is a 2-pole (Q 0.8) and
    a 1-pole low-pass at fc, 8 kHz at 10 ms .. 2.8 kHz at 740 ms. Index 0 (SYNC) reads index 1's numbers."""
    L = []
    ms = [10.0 * 74.0 ** ((max(i, 1) - 1) / 126) for i in range(128)]
    L += arr("BBD_T", "uint16_t", [min(32634, int(round(m * FS / 1000))) for m in ms])
    a14, a24, a34, k1 = [], [], [], []
    for m in ms:
        x = math.log(m / 10.0) / math.log(74.0)
        fc = 8000.0 * (2800.0 / 8000.0) ** (x ** 1.3)
        g, k = math.tan(math.pi * fc / FS), 1 / 0.8
        a1 = 1 / (1 + g * (g + k))
        a14.append(int(round(16384 * a1)))
        a24.append(int(round(16384 * g * a1)))
        a34.append(int(round(16384 * g * g * a1)))
        k1.append(int(round(32768 * (1 - math.exp(-2 * math.pi * fc / FS)))))
    L += arr("BBD_A1", "uint16_t", a14)          # Simper's SVF (Q14): v1 = a1 ic1 + a2 v3, v2 = ic2 + a2 ic1 + a3 v3
    L += arr("BBD_A2", "uint16_t", a24)
    L += arr("BBD_A3", "uint16_t", a34)
    L += arr("BBD_K1", "uint16_t", k1)           # the third pole, Q15
    return L


# DRAIN's spring (firmware/src/obv_fx.h): the tank's loop (both halves, the figure-eight) is SPR_LOOP samples; the
# signal passes the decay four times a loop (twice a half, as Dattorro's), so for a decay time RT60 the gain is
# g = 10^(-60 dB / 4 passes / 20 * loop / RT60). SIZE 0..127 = RT60 0.3 .. 3.0 s, exponential: a spring's range, never
# a hall's (the plate it re-voices ran to ~30 s). DAMP: the one-pole in each half, 0 = open, 1..127 = 20 kHz .. 2.5 kHz
# (the plate's ran down to ~55 Hz).
SPR_LOOP = 2620                                 # the loop's effective length: its lines are 2,926 samples, but an
                                                # allpass passes part of its input at once (bench-fitted, tests/spring)


def spring_tables():
    L = []
    rt = [0.3 * 10 ** (v / 127) for v in range(128)]
    L += arr("SPR_DEC_Q15", "uint16_t", [int(round(32768 * 10 ** (-60 / 4 / 20 * SPR_LOOP / FS / t))) for t in rt])
    L += arr("SPR_RT_MS", "uint16_t", [int(round(1000 * t)) for t in rt])
    hz = [0] + [2500 * 8 ** ((127 - v) / 126) for v in range(1, 128)]
    L += arr("SPR_DAMP_K", "uint16_t", [32768 if v == 0 else int(round(32768 * (1 - math.exp(-2 * math.pi * hz[v] / FS))))
                                         for v in range(128)])
    L += arr("SPR_DAMP_HZ", "uint16_t", [0] + [int(round(h)) for h in hz[1:]])
    return L


def main(path):
    L = ["/* generated by tools/gen_tables.py: do not edit */", "#pragma once", "#include <stdint.h>",
         f"#define CTL {CTL}u", ""]
    # pitch: one octave of phase steps for MIDI 120..131 (C9..B9), lower octaves shift right
    L += arr("INC_C9", "uint32_t", [int(440.0 * 2 ** ((n - 69) / 12) / FS * 2 ** 32) for n in range(120, 132)], 6)
    # a semitone in 256 steps: 2^(i / 3072), Q16
    L += arr("FINE_Q16", "uint32_t", [int(round(65536 * 2 ** (i / 3072))) for i in range(256)])
    # SVF g = tan(pi f / fs) at integer semitones 0..136 (8.2 Hz .. 19.9 kHz), Q12, f capped at 0.45 fs
    fc = [min(440.0 * 2 ** ((n - 69) / 12), 0.45 * FS) for n in range(137)]
    L += arr("SVF_G", "uint16_t", [int(round(4096 * math.tan(math.pi * f / FS))) for f in fc])
    L += arr("CUT_HZ", "uint16_t", [int(round(f)) for f in fc])
    # tanh(x / 32768 * 2) * 32767 for x = i * 256 (sloopdx's softclip)
    L += arr("TANH_Q15", "int16_t", [int(32767 * math.tanh(i / 256 * 2)) for i in range(257)])
    # envelope times 0.5 ms .. 10 s: attack aims at 1.3 and stops at 1.0 (t = 1.466 tau), decay / release
    # reach 5 % of the way in t (t = 3 tau)
    ms = [0.5 * (20000 ** (v / 127)) for v in range(128)]
    L += arr("TIME_MS_X10", "uint32_t", [int(round(m * 10)) for m in ms])
    L += arr("ENV_K_ATT", "uint32_t", [k_block(m / 1000 / 1.466) for m in ms], 8)
    L += arr("ENV_K_DEC", "uint32_t", [k_block(m / 1000 / 3.0) for m in ms], 8)
    # glide 0 = off, else 5 ms .. 5 s to 95 % of the way, Q16 per block
    gms = [5.0 * (1000 ** (v / 127)) for v in range(128)]
    L += arr("GLIDE_MS", "uint16_t", [int(round(m)) for m in gms])
    L += arr("GLIDE_K", "uint16_t", [max(1, min(65535, int(round(65536 * (1 - math.exp(-CTL / (m / 3000 * FS)))))))
                                     for m in gms])
    # LFO 0.05 .. 30 Hz, phase step per control block
    hz = [0.05 * (600 ** (v / 127)) for v in range(128)]
    L += arr("LFO_HZ_X100", "uint16_t", [int(round(h * 100)) for h in hz])
    L += arr("LFO_INC", "uint32_t", [int(h * CTL / FS * 2 ** 32) for h in hz], 8)
    # LFO delay / fade 0 .. 5 s in control blocks
    L += arr("LFO_DELAY_BLK", "uint16_t", [int(round((5000 * (v / 127) ** 2) / 1000 * FS / CTL)) for v in range(128)])
    # equal-power pan: gain Q12 for position 0..128 (sin), the other side reads it mirrored
    L += arr("PAN_Q12", "uint16_t", [int(round(4096 * math.sin(math.pi / 2 * i / 128))) for i in range(129)])
    # the knobs' arcs: cos in 5 degree steps, Q8
    L += arr("COS_Q8", "int16_t", [int(round(256 * math.cos(math.radians(5 * i)))) for i in range(72)], 12)
    L += growl_tables()
    L += tape_tables()
    L += bbd_tables()
    L += spring_tables()
    # TAPE STOP (SEQ held, obv_deck.h): the pitch of a tape whose speed falls in a straight line, 12 log2(speed)
    # semitones (Q8) at speed 1 - i/64, held at -48 semitones from there (the deck all but stopped); the deck's
    # low-pass closes by it (the pitch itself comes from the read)
    L += arr("TS_DIVE8", "int16_t", [max(-48 * 256, int(round(12 * 256 * math.log2(1 - i / 64)))) if i < 64 else -48 * 256
                                     for i in range(65)])
    Path(path).write_text("\n".join(L) + "\n")
    print(f"tables: {path}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "firmware/gen/obv_tables.h")
