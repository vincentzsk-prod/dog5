# SPDX-License-Identifier: GPL-3.0-only
"""Batch 6A helpers (26 BSyncA, 27 R3V3RT, 29 VALHALLA): small probes on top of the 5B kit (lib5b)."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib5b import *          # K, B, M, N, Q, FS, FXOFF, run, note, series, mud, alley_ms, lfo_hz
import batch05b as R5

DRY = {"DLY_MIX": 0, "REV_MIX": 0, "CHEW": 0}
FXOFF_ALL = {"GROWL": 0, "DLY_MIX": 0, "REV_MIX": 0, "CHEW": 0}
BANDS = ("<60", "60-150", "150-400", "400-1.2k", "1.2k+")


def crest(a, t0, t1):
    x = a[int(t0 * FS / 1000):int(t1 * FS / 1000)]
    return float(20 * np.log10(np.abs(x).max() / np.sqrt((x ** 2).mean())))


def env_ms(a, hop=1.0, win=4.0):
    """stereo power envelope in dBFS every hop ms over a sliding win ms window"""
    h, w = int(FS * hop / 1000), int(FS * win / 1000)
    p = (a ** 2).mean(1)
    c = np.concatenate([[0.0], np.cumsum(p)])
    idx = np.arange(w, len(p), h)
    return 10 * np.log10(np.maximum((c[idx] - c[idx - w]) / w, 1e-3) / 32767 ** 2), idx / FS * 1000


def shares(a, t0, t1, nfft=4096):
    s = M.band_shares(a, t0, t1, nfft=nfft)
    return {k: float(v) for k, v in s.items()}


def lfo_pitch_cents(v):
    return ((v * v) >> 7) * 9.375


def detune_cents(det):
    return det * det / 64 * 100 / 256
