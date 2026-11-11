# SPDX-License-Identifier: GPL-3.0-only
"""Batch 6A2 helpers (29 i scream, the ice-cream-van chime): partials, decay times, the speaker band, the tape wobble."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib6a import *          # K, B, M, N, Q, R5, FS, run, note, DRY, env_ms, crest ...

SEND_OFF = {"DLY_MIX": 0, "REV_MIX": 0, "CHEW": 0, "GROWL": 0}


def f_of(n):
    return 440 * 2 ** ((n - 69) / 12)


def solo(exe, p, n=85, hold=3000, tail=1500, vel=100, ov=None):
    """one note from silence (struck at 3000 ms), the patch with `ov` laid over it"""
    q = {**p, **(ov or {})}
    return run(exe, q, note(3000, 3000 + hold, n, vel), 3000 + hold + tail)


def partials(a, t0, t1, n=85, top=7, floor=-45, nfft=None):
    """the strongest spectral peaks of [t0, t1] ms (mono, Hann, zero padded): [(Hz, dB re the strongest)], by frequency; ratio to the played f0 and distance of that ratio from the nearest integer"""
    x = a.mean(1)[int(t0 * FS / 1000):int(t1 * FS / 1000)]
    NF = 1 << 16
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)), NF))
    f = np.fft.rfftfreq(NF, 1 / FS)
    keep = (f > 150) & (f < 12000)
    pk = [i for i in range(1, len(X) - 1) if X[i] > X[i - 1] and X[i] >= X[i + 1] and keep[i]]
    mx = X[pk].max() if pk else 1.0
    cand = sorted(((X[i] / mx, f[i]) for i in pk), reverse=True)
    out = []
    for v, fr in cand:
        db = 20 * np.log10(v)
        if db < floor or len(out) >= top:
            break
        if all(abs(fr - g) > 40 for g, _ in out):          # merge the lobes of one partial (40 Hz: the 100 ms window's width)
            out.append((float(fr), float(db)))
    f0 = f_of(n)
    return sorted((fr, db, fr / f0, abs(fr / f0 - round(fr / f0))) for fr, db in out)


def decay_times(a, on=3000, levels=(6, 12, 20, 30, 40), win=4.0):
    """ms after the note-on for the 4 ms power envelope to first fall to each level (dB) under its own peak in the first 150 ms (the strike); None where it does not within the render"""
    e, t = env_ms(a, 1.0, win)
    i0 = int(on)
    pk = float(e[i0:i0 + 150].max())
    ip = int(np.argmax(e[i0:i0 + 150])) + i0
    seg = e[ip:]
    out = {"peak_db": pk}
    for lv in levels:
        k = np.nonzero(seg <= pk - lv)[0]
        out[str(lv)] = float(k[0]) if len(k) else None
    return out


def front_edge(a, on=3000, ms=20, nfft=512):
    """centroid over the first `ms` after the audible onset (the first sample above -50 dB of the first 100 ms's peak): the tape's fixed 3.6 ms head moves the onset, so both renders are read from their own onset"""
    x = np.abs(a).max(1)
    seg = x[int((on - 10) * FS / 1000):int((on + 100) * FS / 1000)]
    thr = seg.max() * 10 ** (-50 / 20)
    s0 = int((on - 10) * FS / 1000) + int(np.nonzero(seg > thr)[0][0])
    t0 = s0 / FS * 1000
    return M.centroid(a, t0, t0 + ms, nfft=nfft), t0 - on


def ex_wobble(exe, p, n=73, cents=True):
    """the pitch wobble of the tape and the LFO on a ONE-VOICE probe: POLY 1 voice, VINTAGE 0, OSC 2 / X-MOD / filter envelope off, a held saw with a sustained amp envelope (a decaying chime has no steady pitch to read), the sends off but CHEW and the
    LFO as the patch has them; the fundamental tracked in 25 ms hops (3 s hold, from 0.4 s): s.d., 5-95 % range and the strongest rate (Hz) of the wander, cents"""
    q = {**p, "MODE": 0, "POLY_N": 1, "VINTAGE": 0, "O1_WAVE": 1, "O1_LVL": 110, "O2_LVL": 0, "XMOD": 0, "ENV_O2": 64, "FENV_AMT": 64, "FTYPE": 0, "CUTOFF": 127, "RESO": 0, "DRIVE": 0, "GROWL": 0, "DLY_MIX": 0, "REV_MIX": 0,
         "AA": 0, "AD": 127, "AS": 127, "AR": 40, "SPREAD": 64}
    a = run(exe, q, note(3000, 6600, n), 7000)
    f0 = f_of(n)
    c = R5.partial_track(a, f0, f0 * 0.04, 3400, 6400, frame_ms=100, hop_ms=25)
    X = np.abs(np.fft.rfft((c - c.mean()) * np.hanning(len(c)), 1 << 13)) ** 2
    fr = np.fft.rfftfreq(1 << 13, 0.025)
    sl = (fr >= 0.2) & (fr <= 12)
    return {"sd": float(c.std()), "p5": float(np.percentile(c, 5)), "p95": float(np.percentile(c, 95)), "rate": float(fr[sl][int(np.argmax(X[sl]))]) if c.std() > 0.05 else 0.0}


def speaker(exe, p, n=81):
    """the band of the voice's filter (the 'speaker') read with white noise: the oscillators off, NOISE 127, a sustained amp envelope, the filter envelope as the patch has it but read 1.2-2.6 s after the strike (settled), the sends off, the LFO off:
    the long-term spectrum in 1/6-octave smoothing: the peak (Hz, 300-6000), its -3 dB width (Hz, from-to), the share of the energy under 400 Hz and above 4 kHz (%), the centroid (Hz)"""
    q = {**p, "O1_LVL": 0, "O1_WAVE": 0, "O2_LVL": 0, "O2_WAVE": 0, "XMOD": 0, "NOISE": 127, "AA": 0, "AD": 127, "AS": 127, "AR": 40, **SEND_OFF, "LFO_PITCH": 0, "LFO_AMP": 0, "LFO_FLT": 0, "LFO_PWM": 0, "MODE": 0, "POLY_N": 1, "VINTAGE": 0, "DRIVE": p.get("DRIVE", 0)}
    a = run(exe, q, note(3000, 5800, n), 6200)
    x = a.mean(1)[int(4200 * FS / 1000):int(5600 * FS / 1000)]
    NF = 1 << 16
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)), NF)) ** 2
    f = np.fft.rfftfreq(NF, 1 / FS)
    fc = 2 ** np.arange(np.log2(100), np.log2(12000), 1 / 24)
    S = np.array([10 * np.log10(X[(f >= c * 2 ** (-1 / 12)) & (f < c * 2 ** (1 / 12))].mean() + 1e-9) for c in fc])
    sel = (fc >= 300) & (fc <= 6000)
    i = int(np.nonzero(sel)[0][np.argmax(S[sel])])
    lo = i
    while lo > 0 and S[lo] > S[i] - 3:
        lo -= 1
    hi = i
    while hi < len(S) - 1 and S[hi] > S[i] - 3:
        hi += 1
    tot = X[(f > 20)].sum()
    return {"peak_hz": float(fc[i]), "w3_lo": float(fc[lo]), "w3_hi": float(fc[hi]), "w3_hz": float(fc[hi] - fc[lo]), "under400": float(100 * X[(f > 20) & (f < 400)].sum() / tot), "over4k": float(100 * X[f > 4000].sum() / tot),
            "cent": float((f[f > 20] * X[f > 20]).sum() / tot)}
