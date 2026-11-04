# SPDX-License-Identifier: GPL-3.0-only
"""Round-2 measures for 30 THE DOG (and any patch that needs them): the band split, the harmonic / drive measures, trim."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K

BANDS = [("<60", 0, 60), ("60-150", 60, 150), ("150-400", 150, 400), ("400-1.2k", 400, 1200), ("1.2k+", 1200, 24000)]


def band_split(a, phrase, nfft=4096):
    """energy per band over the note-on region, mono sum, Hann frames: returns {band: energy} (absolute, arbitrary units)"""
    x = a.mean(1)
    m = K.gate_mask(phrase, len(x))
    win = np.hanning(nfft)
    f = np.fft.rfftfreq(nfft, 1 / K.FS)
    tot = {b[0]: 0.0 for b in BANDS}
    for s in range(0, len(x) - nfft, nfft // 2):
        if not m[s:s + nfft].all():
            continue
        P = np.abs(np.fft.rfft(x[s:s + nfft] * win)) ** 2
        for n, lo, hi in BANDS:
            tot[n] += P[(f >= lo) & (f < hi)].sum()
    return tot


def split_report(bs, ref=None):
    """shares (%) and, against a reference split, dB difference per band"""
    t = sum(bs.values())
    sh = {k: 100 * v / t for k, v in bs.items()}
    db = {k: 10 * np.log10(max(bs[k], 1e-9) / max(ref[k], 1e-9)) for k in bs} if ref else None
    return sh, db


def harmonics(a, on_ms, off_ms, f0=55.0):
    """the held note's harmonic content (a detuned stack's partials form tight clusters, so n*f0 +- min(3%, 15 Hz) windows work):
    odd and even harmonic energy (n = 2..40, 110 Hz..), the energy between the harmonics (the 'hash', % of 150 Hz..8 kHz), and the
    crest factor of the held body in dB"""
    x = a.mean(1)[int((on_ms + 500) * K.FS / 1000):int((off_ms - 100) * K.FS / 1000)]
    N = 1 << 17
    X = np.abs(np.fft.rfft(x[:N] * np.hanning(min(len(x), N)), N)) ** 2 if len(x) >= N else np.abs(np.fft.rfft(x * np.hanning(len(x)), N)) ** 2
    f = np.fft.rfftfreq(N, 1 / K.FS)
    # locate the true f0: the strongest peak within +-8 % of f0 (or of 2 f0 / 2 when the sub dominates)
    sel = (f > f0 * 0.92) & (f < f0 * 1.08)
    f0 = f[sel][np.argmax(X[sel])] if X[sel].max() > 0 else f0
    odd = even = 0.0
    inh = np.zeros(len(f), bool)
    for n in range(1, 140):
        hw = min(0.03 * n * f0, 15.0)
        w = (f > n * f0 - hw) & (f < n * f0 + hw)
        inh |= w
        if 2 <= n <= 40:
            e = X[w].sum()
            if n % 2: odd += e
            else: even += e
    band = (f > 150) & (f < 8000)
    hash_pct = 100 * X[band & ~inh].sum() / X[band].sum()
    crest = 20 * np.log10(np.abs(x).max() / np.sqrt((x ** 2).mean()))
    return {"f0": float(f0), "odd_db": float(10 * np.log10(odd + 1e-9)), "even_db": float(10 * np.log10(even + 1e-9)),
            "even_odd_db": float(10 * np.log10((even + 1e-9) / (odd + 1e-9))), "hash_pct": float(hash_pct), "crest_db": float(crest)}


def trim(exe, params, phrase, target, tag="tr", lo=1, hi=127):
    """VOLUME (square law, ~0.17 dB a step) whose RMS on the phrase is closest to target; returns (volume, rms)"""
    v = params.get("VOLUME", 100)
    best = None
    for _ in range(8):
        a, _ = K.render(exe, phrase, params={**params, "VOLUME": v}, tag=tag)
        r = K.level_metrics(a, phrase)["rms"]
        if best is None or abs(r - target) < abs(best[1] - target):
            best = (v, r)
        if abs(r - target) < 0.1:
            break
        nv = int(round(v * 10 ** ((target - r) / 40)))
        v = max(lo, min(hi, nv if nv != v else v + (1 if target > r else -1)))
    return best


def motion(a, on_ms, off_ms, lo=60.0, hi=400.0):
    """the stack's inner motion: the held body band-passed to lo..hi Hz (FFT mask), its envelope (analytic signal, smoothed 30 ms),
    in dB: returns (s.d. dB, peak-to-peak dB) -- beating between the voices and the two oscillators, the 'thickness' that moves"""
    x = a.mean(1)[int((on_ms + 500) * K.FS / 1000):int((off_ms - 100) * K.FS / 1000)]
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / K.FS)
    X[(f < lo) | (f > hi)] = 0
    A = np.zeros(len(x), complex)
    A[:len(X)] = X * 2
    env = np.abs(np.fft.ifft(A))
    k = int(0.03 * K.FS)
    env = np.convolve(env, np.ones(k) / k, "valid")[k:-k]
    db = 20 * np.log10(np.maximum(env, 1e-6))
    return float(db.std()), float(db.max() - db.min())


def chop_snap(a, phrase="e_lowuni"):
    """the attack snap on the eight chopped roots of phrase (e) (130 ms notes from 9000 ms, every 250 ms): per note the peak of the 2 ms /
    18 ms power envelope in the first 40 ms against the mean power 80..130 ms in; returns (mean dB, min dB).  Steadier than one held
    note, whose 'body' level moves with the stack's beating"""
    e, _ = K.env_db(a, 2.0, 18.0)
    out = []
    for on, off in [(n[1], n[2]) for n in K.notes_of(phrase) if 8900 < n[1] < 10000]:
        i0 = int(on / 2)
        pk = e[i0:i0 + 20].max()
        body = 10 * np.log10(np.mean(10 ** (e[i0 + 40:int(off / 2)] / 10)))
        out.append(pk - body)
    return float(np.mean(out)), float(np.min(out))


def held_snap(a, on_ms, off_ms, f0=55.0):
    """the attack snap of the held note, steadied against the stack's beating: the peak of the power envelope (2 ms hop, one period of f0
    wide) in the first 60 ms against the MEAN power over 500 ms .. the release (the earlier body estimate was the last 110 ms only, so the
    beat phase moved it by a dB or two)"""
    e, _ = K.env_db(a, 2.0, 1000 / f0)
    i0 = int(on_ms / 2)
    pk = e[i0:i0 + 30].max()
    body = 10 * np.log10(np.mean(10 ** (e[i0 + 250:int(off_ms / 2) - 3] / 10)))
    return float(pk - body)
