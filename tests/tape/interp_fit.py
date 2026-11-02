#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""TAPE's play head (firmware/src/obv_tape.h, TP_IC): a 6-point, 5th-order polynomial interpolator fitted for a
2x-oversampled line, in Olli Niemitalo's z-form ("Polynomial Interpolators for High-Quality Resampling of
Oversampled Audio", 2001: the same structure; these numbers are this fit's own).

Why: a moving read wobbles the interpolator's response at the rate the fraction turns (hundreds of Hz under wow),
which puts sidebands around every partial. A 4-point Catmull-Rom (Hermite) read at 2x leaves them at -43 dB under a
10 kHz tone and -31 dB under 15 kHz; 4x would cost a second halfband stage and twice the reads. This fit (iteratively
reweighted least squares toward the minimax of the error re a 1/f (saw) spectrum, 100 Hz - 18 kHz, every fraction)
keeps the worst error <= -56 dB re the tone up to 18 kHz and <= -87 dB re a saw's harmonic; DC is pinned exactly.

  python3 tests/tape/interp_fit.py           prints the errors and the Q15 table for obv_tape.h
  python3 tests/tape/interp_fit.py --check   exit 1 unless obv_tape.h carries exactly this table"""
import os
import re
import sys
import numpy as np

F = np.linspace(0, 1, 101)


def basis(w, f):
    """z = f - 1/2; e_k = y_k + y_(1-k), o_k = y_k - y_(1-k) (k = 1, 2, 3 -> y1+y0, y2+y-1, y3+y-2); 18 terms"""
    z = f - 0.5
    E = [np.exp(1j * w) + 1, np.exp(2j * w) + np.exp(-1j * w), np.exp(3j * w) + np.exp(-2j * w)]
    O = [np.exp(1j * w) - 1, np.exp(2j * w) - np.exp(-1j * w), np.exp(3j * w) - np.exp(-2j * w)]
    b = []
    for p in (0, 2, 4):
        b += [e * z ** p for e in E]
    for p in (1, 3, 5):
        b += [o * z ** p for o in O]
    return np.array(b)


def fit():
    W = np.linspace(np.pi * 100 / 44100, np.pi * 18000 / 44100, 200)   # 100 Hz .. 18 kHz at 88.2 kHz
    A = np.array([basis(w, f) for w in W for f in F])
    t = np.array([np.exp(1j * w * f) for w in W for f in F])
    wts = np.array([1 / w for w in W for f in F])
    lw = np.ones(len(t))
    for _ in range(80):
        ww = np.sqrt(lw) * wts
        Ar = np.vstack([(A * ww[:, None]).real, (A * ww[:, None]).imag])
        tr = np.concatenate([(t * ww).real, (t * ww).imag])
        x, *_ = np.linalg.lstsq(Ar, tr, rcond=None)
        e = np.abs(A @ x - t) * wts
        lw = lw * e
        lw /= lw.sum()
    # DC exactly: the even sums 1/2, 0, 0 (the odd terms vanish at DC); the correction lands on the nearest pair
    x[0] += 0.5 - x[0:3].sum()
    x[3] -= x[3:6].sum()
    x[6] -= x[6:9].sum()
    return x


def main():
    x = fit()
    q = [int(round(v * 32768)) for v in x]
    q[0] += 16384 - sum(q[0:3]); q[3] -= sum(q[3:6]); q[6] -= sum(q[6:9])   # (DC exact in Q15 too)
    xq = np.array(q) / 32768
    line = "static const int32_t TP_IC[18] = {" + ", ".join(str(v) for v in q) + "};"
    if "--check" in sys.argv:
        src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../firmware/src/obv_tape.h")).read()
        ok = line in src
        print("obv_tape.h TP_IC", "matches the fit" if ok else "DIFFERS from the fit:\n" + line)
        sys.exit(0 if ok else 1)
    def cr(w, f):
        ym1, y0, y1, y2 = np.exp(-1j * w), 1, np.exp(1j * w), np.exp(2j * w)
        return y0 + 0.5 * f * (y1 - ym1 + f * (2 * ym1 - 5 * y0 + 4 * y1 - y2 + f * (3 * (y0 - y1) + y2 - ym1)))
    def err(fn, hz):
        w = np.pi * hz / 44100
        return 20 * np.log10(max(abs(fn(w, f) - np.exp(1j * w * f)) for f in F) + 1e-30)
    print("worst error over all fractions, re a tone at that frequency (88.2 kHz line):")
    for hz in (0, 100, 1000, 2000, 5000, 10000, 15000, 18000):
        e = err(lambda w, f: basis(w, f) @ xq, hz)
        print(f"  {hz:6d} Hz  Catmull-Rom {err(cr, hz):7.1f} dB   this fit (Q15) {e:7.1f} dB"
              + (f"   (re a 1/f saw from 500 Hz: {e + 20 * np.log10(500 / hz):6.1f})" if hz >= 500 else ""))
    print(line)


if __name__ == "__main__":
    main()
