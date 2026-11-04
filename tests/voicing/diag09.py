#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Diagnosis of 09 Skeenhead variant B (Batch 2A round 2): why does the note sound distant and separate from its spring?  Measures the dry note (effects off) in
0-20 / 20-100 / 100-250 ms windows, the filter's trajectory, the spring return against the dry note per window, the timing of the spring's onset and peak, and the
spectral gap between note and spring.  Usage: python3 tests/voicing/diag09.py [slot-source-tree=.]  (renders the tree's slot 9 through the program path)."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import batch02a_metrics as M

FX = {"DLY_MIX": 0, "REV_MIX": 0, "CHEW": 0, "GROWL": 0}
WIN = [(0, 20), (20, 100), (100, 250)]


def render(exe, ph, prog, over=None):
    if over is None:
        return K.render(exe, ph, program=prog, tag="d09")[0]
    return K.render(exe, ph, params=over, tag="d09")[0]


def main():
    src = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else K.ROOT
    exe = K.build_host(src, os.path.join(K.BUILD, "obervave_diag"))
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import batch01a as B
    P = B.resolve(src, 9)
    wet = render(exe, "g_skank", None, P)
    dry = render(exe, "g_skank", None, {**P, **FX})
    fx = wet - dry
    # the stab at 7250 (A minor dyad A3 C4): it follows the 1.4 s gap, so nothing else is sounding in front of it (the next stab is 500 ms later)
    t0 = 7250
    print("== 1. THE DRY NOTE (effects off), the stab at 7250 ms after the gap (A3 C4, gate 110 ms), windows after note-on")
    print("window ms | level dBFS | centroid Hz | band % <60/60-150/150-400/400-1.2k/1.2k+")
    for a, b in WIN:
        print(f"{a:3d}-{b:3d} | {M.rms_db(dry, t0 + a, t0 + b):7.1f} | {M.centroid(dry, t0 + a, t0 + b, nfft=1024):6.0f} | " + M.fmt_bands(M.band_shares(dry, t0 + a, t0 + b, nfft=1024)))
    print("   (the voice has a 4 ms release and the gate is 110 ms: the 100-250 window holds 10 ms of note and 140 ms of silence)")
    print("\n== 1b. the filter over the body: dry level and centroid every 10 ms from the note-on")
    print("t ms: " + " ".join(f"{t:5d}" for t in range(0, 120, 10)))
    print("dB:   " + " ".join(f"{M.rms_db(dry, t0 + t, t0 + t + 10):5.1f}" for t in range(0, 120, 10)))
    print("Hz:   " + " ".join(f"{M.centroid(dry, t0 + t, t0 + t + 10, nfft=512):5.0f}" for t in range(0, 120, 10)))
    # the engine's cutoff trajectory: cut(st) = CUTOFF + 8 + keytrack + fenv * (ENV AMT - 64) * 1.52 ; fenv RC fall over FILTER DECAY (time table = the 5 % point)
    cut, amt, fd = P["CUTOFF"], P["FENV_AMT"] - 64, P["FD"]
    tau = B.ms_of(fd) / 3.0
    kt = ((57 + 60) / 2 - 60) * P["KEYTRK"] * 2 / 256
    print(f"\n== 1c. the filter trajectory (engine formula; this dyad: key track {kt:+.1f} st; FILTER DECAY {fd} = {B.ms_of(fd):.0f} ms to the 5 % point, tau ~ {tau:.0f} ms)")
    print(f"the notes: A3 {440 * 2 ** ((57 - 69) / 12):.0f} Hz + C4 {440 * 2 ** ((60 - 69) / 12):.0f} Hz")
    print("t ms: " + " ".join(f"{t:6d}" for t in (0, 5, 10, 20, 30, 40, 60, 80, 110)))
    row = []
    for t in (0, 5, 10, 20, 30, 40, 60, 80, 110):
        fe = np.exp(-t / tau)
        st = cut + 8 + kt + fe * amt * 1.52
        row.append(440 * 2 ** ((st - 69) / 12))
    print("Hz:   " + " ".join(f"{min(v, 99999):6.0f}" for v in row))
    # 2. the spring against the note, per window
    print("\n== 2. THE SPRING RETURN against the dry note, per window after the note-on of the same stab (dB, fx = wet - dry)")
    print("window ms | dry dB | spring dB | spring re dry | spring centroid Hz | dry centroid Hz")
    for a, b in WIN + [(250, 500), (500, 1000)]:
        d_, f_ = M.rms_db(dry, t0 + a, t0 + b), M.rms_db(fx, t0 + a, t0 + b)
        print(f"{a:4d}-{b:4d} | {d_:7.1f} | {f_:7.1f} | {f_ - d_:+7.1f} | {M.centroid(fx, t0 + a, t0 + b, nfft=1024):6.0f} | {M.centroid(dry, t0 + a, t0 + b, nfft=1024):6.0f}")
    on = K.gate_mask("g_skank", len(dry))
    print(f"over all the stabs' note-on regions: spring re dry {M.energy_db(fx[on]) - M.energy_db(dry[on]):+.1f} dB (the table's -4.2); PRE-DLY {P['REV_PRE']} -> {P['REV_PRE'] * 35 / 127:.1f} ms")
    # 3. timing: onset and peak of the spring return vs the note
    e_d, e_f = M.env_ms(dry[int((t0 - 50) * K.FS / 1000):int((t0 + 900) * K.FS / 1000)], 1, 4), M.env_ms(fx[int((t0 - 50) * K.FS / 1000):int((t0 + 900) * K.FS / 1000)], 1, 4)
    def first_above(e, lvl): return int(np.nonzero(e > lvl)[0][0]) - 50
    print("\n== 3. TIMING (4 ms envelopes, ms re the note-on)")
    print(f"dry peak at {int(np.argmax(e_d)) - 50} ms ({e_d.max():.1f} dB); spring first within 30 dB of its peak at {first_above(e_f, e_f.max() - 30)} ms, within 10 dB at {first_above(e_f, e_f.max() - 10)} ms, peak at {int(np.argmax(e_f)) - 50} ms ({e_f.max():.1f} dB)")
    print(f"spring peak re dry peak {e_f.max() - e_d.max():+.1f} dB; the dry note ends at 110 ms, the spring is {e_f[50 + 110]:.1f} dB at 110 ms, {e_f[50 + 300]:.1f} at 300 ms")
    # 4. spectral gap
    print("\n== 4. SPECTRAL GAP (the first 250 ms of the stab): share of energy above 400 Hz, dry note vs spring return")
    print(f"dry {M.band_shares(dry, t0 + 20, t0 + 100, nfft=1024)['400-1.2k'] + M.band_shares(dry, t0 + 20, t0 + 100, nfft=1024)['1.2k+']:.1f} %   spring {M.band_shares(fx, t0, t0 + 250, nfft=1024)['400-1.2k'] + M.band_shares(fx, t0, t0 + 250, nfft=1024)['1.2k+']:.1f} %")
    # 5. the original's note (two narrow pulses) for comparison, through the base tree if given
    print("\n== 5. BODY of the dry note: the committed note against variants of it (effects off), windows 0-20 / 20-100 ms level and share above 400 Hz")
    for name, ch in (("B (committed)", {}), ("OSC 2 pulse on (same pitch, LEVEL 100)", {"O2_WAVE": 2, "O2_PW": 64}), ("CUTOFF floor +12 (52)", {"CUTOFF": 52}), ("FILTER SUSTAIN 40", {"FS": 40}), ("no filter envelope (ENV AMT centre)", {"FENV_AMT": 64, "CUTOFF": 60})):
        d = render(exe, "g_skank", None, {**P, **FX, **ch})
        r = []
        for a, b in ((0, 20), (20, 100)):
            bs = M.band_shares(d, t0 + a, t0 + b, nfft=1024)
            r.append(f"{M.rms_db(d, t0 + a, t0 + b):6.1f} dB {bs['400-1.2k'] + bs['1.2k+']:5.1f} %")
        print(f"{name:42s} 0-20: {r[0]} | 20-100: {r[1]}")
    base = os.path.join(K.BUILD, "base_r2" if os.path.isdir(os.path.join(K.BUILD, "base_r2")) else "base")
    import batch01a as B2
    old = K.build_host(os.path.join(K.BUILD, "base"), os.path.join(K.BUILD, "obervave_base"))
    Po = B2.resolve(os.path.join(K.BUILD, "base"), 9)                      # the ORIGINAL clav pluck (two narrow pulses, no spring), effects off
    d = K.render(old, "g_skank", params={**Po, **FX}, tag="d09o")[0]
    r = []
    for a, b in ((0, 20), (20, 100)):
        bs = M.band_shares(d, t0 + a, t0 + b, nfft=1024)
        r.append(f"{M.rms_db(d, t0 + a, t0 + b):6.1f} dB {bs['400-1.2k'] + bs['1.2k+']:5.1f} %")
    print(f"{'the ORIGINAL (two narrow pulses), dry':42s} 0-20: {r[0]} | 20-100: {r[1]}")


if __name__ == "__main__":
    main()
