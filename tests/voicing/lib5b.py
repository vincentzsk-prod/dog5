# SPDX-License-Identifier: GPL-3.0-only
"""Batch 5B helpers (20 Fire & Ice, 23 Crypt Dust, 24 Fugue State): windowed readings and small probes on top of the 4A/5A kit."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import batch01a as B
import batch02a_metrics as M
import batch03a_metrics as N
import batch04a_metrics as Q

FS = K.FS
FXOFF = {"GROWL": 0, "DLY_MIX": 0, "REV_MIX": 0, "CHEW": 0}


def run(exe, p, notes, end_ms, tag="p5b"):
    """INIT + p, then the note lines; returns the stereo render"""
    return N._run(exe, tag, N._probe_script(p, notes, end_ms))


def note(on, off, n, v=100):
    return [f"{on} midi 0x90 {n} {v}", f"{off} midi 0x80 {n} 0"]


def series(a, t0, step, n, nfft=1024):
    """per window of `step` ms from t0: (level dBFS, centroid Hz, share above 1.2 kHz %)"""
    out = []
    for i in range(n):
        a0, a1 = t0 + i * step, t0 + (i + 1) * step
        sh = M.band_shares(a, a0, a1, nfft=nfft)
        out.append((M.rms_db(a, a0, a1), M.centroid(a, a0, a1, nfft=nfft), sh["1.2k+"]))
    return out


def mud(a, t0, t1, nfft=4096):
    """MUD ratio = share 150-400 Hz over share above 1.2 kHz (voicing README, dictionary)"""
    s = M.band_shares(a, t0, t1, nfft=nfft)
    return s["150-400"] / max(s["1.2k+"], 1e-3), s


def alley_ms(v):
    return Q.alley_ms(v)


def lfo_hz(r):
    return 0.05 * 600 ** (r / 127)
