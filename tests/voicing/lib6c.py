# SPDX-License-Identifier: GPL-3.0-only
"""Batch 6B helpers (28 Bell Tolls): the bell partial ladder, ring times, strike and tail windows, band shares."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib6b import *          # K, B, M, N, Q, R5, FS, run, note, DRY, SEND_OFF, env_ms, f_of, solo, partials, decay_times, ex_wobble

BELL = (0.5, 1.0, 1.2, 1.5, 2.0)          # a struck church bell's classical partials (hum, prime, tierce, quint, nominal) re the prime


def ladder(a, n, t0, t1, tol=0.03, floor=-50):
    """the measured partials of [t0, t1] ms (Hann, zero padded, peak pick) against the classical bell ladder 0.5 / 1 / 1.2 / 1.5 / 2 x the played note: for each classical ratio the nearest measured peak within +-tol (ratio, dB re the strongest) or None;
    plus the strongest peaks overall (Hz, dB, ratio)"""
    x = a.mean(1)[int(t0 * FS / 1000):int(t1 * FS / 1000)]
    NF = 1 << 17
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)), NF))
    f = np.fft.rfftfreq(NF, 1 / FS)
    keep = (f > 40) & (f < 16000)
    idx = [i for i in range(1, len(X) - 1) if X[i] > X[i - 1] and X[i] >= X[i + 1] and keep[i]]
    mx = X[idx].max()
    pk = [(f[i], 20 * np.log10(X[i] / mx)) for i in idx if 20 * np.log10(X[i] / mx) > floor]
    f0 = f_of(n)
    out = {}
    for r in BELL:
        c = [(abs(fr / f0 / r - 1), fr, db) for fr, db in pk if abs(fr / f0 / r - 1) <= tol]
        out[str(r)] = None if not c else {"ratio": float(min(c)[1] / f0), "db": float(max(c, key=lambda q: q[2])[2]), "hz": float(max(c, key=lambda q: q[2])[1])}
    top = sorted(pk, key=lambda q: -q[1])[:8]
    return {"classical": out, "top": [(float(a_), float(b_), float(a_ / f0)) for a_, b_ in sorted(top)]}


def shares3(a, t0, t1, nfft=8192):
    """% of the energy under 150 Hz, 150-800 Hz, 800-4000 Hz and above 4 kHz over [t0, t1] ms (mono, Hann frames)"""
    x = a.mean(1)
    win = np.hanning(nfft)
    f = np.fft.rfftfreq(nfft, 1 / FS)
    t = np.zeros(4)
    for s in range(int(t0 * FS / 1000), max(int(t1 * FS / 1000) - nfft, int(t0 * FS / 1000) + 1), nfft // 2):
        if s + nfft > len(x):
            break
        P = np.abs(np.fft.rfft(x[s:s + nfft] * win)) ** 2
        t += [P[f < 150].sum(), P[(f >= 150) & (f < 800)].sum(), P[(f >= 800) & (f < 4000)].sum(), P[f >= 4000].sum()]
    t = t / max(t.sum(), 1e-9) * 100
    return {"<150": float(t[0]), "150-800": float(t[1]), "800-4k": float(t[2]), ">4k": float(t[3])}


def cent(a, t0, t1, nfft=2048):
    return M.centroid(a, t0, t1, nfft=nfft)


def tail_rows(a, on=3000, wins=((0, 20), (20, 100), (100, 400), (1000, 2000), (2000, 4000), (4000, 6000))):
    """per window after the strike: level (dB), centroid (Hz) and the share above 4 kHz (%): the strike against the tail"""
    out = []
    for x, y in wins:
        nf = 1024 if y - x <= 100 else 4096
        out.append({"w": (x, y), "rms": M.rms_db(a, on + x, on + y), "cent": M.centroid(a, on + x, on + y, nfft=nf), "over4k": M.band_shares(a, on + x, on + y, nfft=nf)["1.2k+"] if False else shares3(a, on + x, on + y, nfft=min(nf, 4096))[">4k"]})
    return out
