# SPDX-License-Identifier: GPL-3.0-only
"""Measurements for Batch 2A ("weight and space": 17 Titanic, 21 Cowl Shadow, 09 Skeenhead, 11 Slapback Strut).

Everything here reads a host render (stereo float array from t = 0, 44.1 kHz) and returns numbers; the round driver
(batch02a.py) decides which render is which.  Definitions are in dog5-docs/voicing/README.md sections 4 and 9."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import dog_metrics as D

FS = K.FS


def _s(ms):
    return int(round(ms * FS / 1000))


def rms_db(a, t0_ms, t1_ms):
    """RMS dBFS (both channels, one power average) over [t0, t1] ms"""
    x = a[_s(t0_ms):_s(t1_ms)]
    return float(10 * np.log10(max((x ** 2).mean(), 1e-12) / 32767 ** 2))


def peak_db(a, t0_ms=0, t1_ms=None):
    x = a[_s(t0_ms):(_s(t1_ms) if t1_ms else None)]
    return float(20 * np.log10(max(np.abs(x).max(), 1) / 32767))


def centroid(a, t0_ms, t1_ms, nfft=4096):
    """spectral centroid (Hz) of the mono sum over [t0, t1] ms: Hann frames, |X|-weighted per frame, frames weighted by energy"""
    x = a.mean(1)
    win = np.hanning(nfft)
    f = np.fft.rfftfreq(nfft, 1 / FS)
    num = den = 0.0
    for s in range(_s(t0_ms), max(min(_s(t1_ms), len(x)) - nfft, _s(t0_ms) + 1), nfft // 2):
        if s + nfft > len(x):
            break
        X = np.abs(np.fft.rfft(x[s:s + nfft] * win))
        e = (X ** 2).sum()
        if e > 0:
            num += e * (f * X).sum() / X.sum()
            den += e
    return float(num / den) if den else 0.0


def band_shares(a, t0_ms, t1_ms, nfft=4096):
    """% of the energy per band (<60, 60-150, 150-400, 400-1.2k, 1.2k+ Hz), mono sum, Hann frames, over [t0, t1] ms"""
    x = a.mean(1)
    win = np.hanning(nfft)
    f = np.fft.rfftfreq(nfft, 1 / FS)
    tot = {b[0]: 0.0 for b in D.BANDS}
    for s in range(_s(t0_ms), max(min(_s(t1_ms), len(x)) - nfft, _s(t0_ms) + 1), nfft // 2):
        if s + nfft > len(x):
            break
        P = np.abs(np.fft.rfft(x[s:s + nfft] * win)) ** 2
        for n, lo, hi in D.BANDS:
            tot[n] += P[(f >= lo) & (f < hi)].sum()
    t = sum(tot.values()) or 1.0
    return {k: 100 * v / t for k, v in tot.items()}


def band_split_phrase(a, phrase):
    """band shares (%) over the phrase's note-on region (dog_metrics.band_split)"""
    bs = D.band_split(a, phrase)
    t = sum(bs.values()) or 1.0
    return {k: 100 * v / t for k, v in bs.items()}


def fmt_bands(b):
    return " / ".join(f"{b[n]:.0f}" for n, _, _ in D.BANDS)


# ---- the bloom ---------------------------------------------------------------------------------------------------
def bloom(a, on_ms, hold_ms, step_ms=1000):
    """the brightness and level of a held note against time: [(t_s, level dBFS, centroid Hz, % of energy above 1.2k)] per
    1 s window over the hold, then the bloom times read off the curves (see bloom_times)"""
    rows = []
    t = 0
    while t + step_ms <= hold_ms:
        b = band_shares(a, on_ms + t, on_ms + t + step_ms)
        rows.append((t / 1000, rms_db(a, on_ms + t, on_ms + t + step_ms), centroid(a, on_ms + t, on_ms + t + step_ms), b["1.2k+"]))
        t += step_ms
    return rows


def bloom_times(rows, f0):
    """when does the note get there?  Brightness is judged on a log axis (an ear hears octaves): the centroid in octaves above
    its value in the first window; t10 / t90 = first window at 10 % / 90 % of the way from the first window to the plateau (the
    mean of the last 3 windows).  Level the same way (dB).  Also the plateau centroid in harmonics of f0"""
    t = np.array([r[0] for r in rows])
    lv = np.array([r[1] for r in rows])
    ce = np.log2(np.array([r[2] for r in rows]))
    def tx(y, p):
        lo, hi = y[0], y[-3:].mean()
        if abs(hi - lo) < 1e-9:
            return None
        z = (y - lo) / (hi - lo)
        i = np.nonzero(z >= p)[0]
        if not len(i):
            return None
        i = int(i[0])
        if i == 0:
            return float(t[0])
        return float(t[i - 1] + (p - z[i - 1]) / (z[i] - z[i - 1]) * (t[i] - t[i - 1]))      # linear between windows
    return {"cent_t10": tx(ce, .1), "cent_t90": tx(ce, .9), "lvl_t90": tx(lv, .9), "cent0": float(2 ** ce[0]),
            "cent_plateau": float(2 ** ce[-3:].mean()), "octaves": float(ce[-3:].mean() - ce[0]),
            "plateau_harm": float(2 ** ce[-3:].mean() / f0)}


def steady_level(a, on_ms, steady_from_s=6.0, steady_to_s=10.0):
    """THE SLOW PHRASES' LEVEL (README section 9): RMS dBFS over t = +6 s .. +10 s after note-on, the bloomed state"""
    return rms_db(a, on_ms + steady_from_s * 1000, on_ms + steady_to_s * 1000)


def register_tilt(a):
    """x_register: the same velocity in three octaves (A1 / A2 / A3, each held 1.5 s): level (dBFS RMS over 0.1-1.4 s of the hold),
    centroid in harmonics of the note (centroid / f0: how many partials the filter lets through), per octave"""
    out = []
    for f0, on in ((55.0, 3000), (110.0, 5500), (220.0, 8000)):
        out.append({"f0": f0, "level": rms_db(a, on + 100, on + 1400), "harm": centroid(a, on + 100, on + 1400) / f0,
                    "cent": centroid(a, on + 100, on + 1400)})
    return out


# ---- the tails: spring and echo ------------------------------------------------------------------------------------
def tail_times(a, off_ms, pre_ms, win_ms, dc=None):
    """ms after note-off until the envelope first falls 20 / 40 / 60 dB below its level over the pre_ms before the release
    (voicekit.release_metrics, 2 ms frames); None = not reached inside the window"""
    r = K.release_metrics(a - (dc if dc is not None else 0), off_ms, pre_ms=pre_ms, win_ms=win_ms)
    return {"t20": r["first20"], "t40": r["first40"], "t60": r["first60"], "last60": r["last60"], "pre_db": r["pre_db"]}


def fx_part(wet, dry):
    """the effects' own contribution: wet render minus the same render with the effects off (both stages are parallel sends added
    onto the dry output, so the difference is the send's return; checked by the silence in front of the first return)"""
    return wet - dry


def energy_db(x):
    return float(10 * np.log10(max((x ** 2).mean(), 1e-12) / 32767 ** 2))


def env_ms(a, hop_ms=1.0, win_ms=4.0):
    """stereo power envelope in dBFS every hop_ms over a win_ms window (for echo peaks)"""
    h, w = _s(hop_ms), _s(win_ms)
    p = (a ** 2).mean(1)
    c = np.concatenate([[0.0], np.cumsum(p)])
    idx = np.arange(0, len(p) - w, h)
    return 10 * np.log10(np.maximum((c[idx + w] - c[idx]) / w, 1e-12) / 32767 ** 2)


def echo_return(wet, dry, on_ms, off_ms, window_ms=(20, 400)):
    """the first echo of one isolated note: the FX contribution (wet - dry); the peak of its 4 ms envelope between on+20 and on+400 ms
    re the dry note's own peak envelope (dB), the time of that peak after note-on (the echo's delay + the note's attack), and the
    second repeat: the next peak at about twice the delay, re the first.  Returns dict"""
    fx = fx_part(wet, dry)
    e_fx, e_dr = env_ms(fx), env_ms(dry)
    i0 = int(on_ms)
    note_pk = float(e_dr[i0:i0 + int(off_ms - on_ms) + 40].max())
    seg = e_fx[i0 + window_ms[0]:i0 + window_ms[1]]
    k = int(np.argmax(seg))
    pk = float(seg[k])
    t1 = window_ms[0] + k
    # second repeat: the first echo is a whole copy of the note (as long as the note), so wait until it has ended (30 dB under its peak),
    # then take the largest 4 ms envelope in the next 400 ms, re the first echo's peak
    r2 = None
    j = k
    while j < len(seg) and seg[j] > pk - 30:
        j += 1
    if j < len(seg):
        tail = e_fx[i0 + window_ms[0] + j:i0 + window_ms[0] + j + 400]
        r2 = float(tail.max() - pk) if len(tail) else None
    return {"echo_re_note_db": pk - note_pk, "echo_t_ms": float(t1), "repeat2_re_first_db": r2, "note_pk_db": note_pk}


def attack_snap(a, on_ms, short_ms=23, body_ms=(23, 90)):
    """the brightness of the first 23 ms of a note (centroid Hz, 1024-point Hann) against the next 67 ms: a plop / pluck / snap reads as a high
    first number falling to the second.  Returns (attack Hz, body Hz, ratio)"""
    c0 = centroid(a, on_ms, on_ms + short_ms, nfft=1024)
    c1 = centroid(a, on_ms + body_ms[0], on_ms + body_ms[1], nfft=1024)
    return c0, c1, (c0 / c1 if c1 else 0.0)


def body_drop(a, on_ms, gate_ms):
    """how fast a plucked note dies inside its gate: level of the voice alone (10 ms RMS) around 10 ms after note-on, minus the level around
    gate - 10 ms (dB, positive = it fell by that much) and the time (ms) the 2 ms envelope takes to fall 10 dB from its peak"""
    top = rms_db(a, on_ms + 5, on_ms + 15)
    end = rms_db(a, on_ms + gate_ms - 15, on_ms + gate_ms - 5)
    e, dt = K.env_db(a[_s(on_ms):_s(on_ms + gate_ms + 200)], 2.0, 8.0)
    k = int(np.argmax(e))
    below = np.nonzero(e[k:] <= e[k] - 10)[0]
    t10 = float(below[0] * 2.0) if len(below) else None
    return top - end, t10


def dips(a, t0_ms, t1_ms):
    """dropouts / flutter in a steady held note: the 10 ms power envelope (2 ms hop) over [t0, t1]; the deepest dip below the median (dB) and the
    number of separate dips of 6 dB or more (a dip ends when the envelope is back within 3 dB of the median)"""
    e, _ = K.env_db(a[_s(t0_ms):_s(t1_ms)], 2.0, 10.0)
    med = np.median(e)
    d = med - e
    n, inside = 0, False
    for v in d:
        if not inside and v >= 6:
            inside, n = True, n + 1
        elif inside and v <= 3:
            inside = False
    return float(d.max()), n


def band_diff_db(fx, dry, t0_ms, t1_ms, nfft=4096):
    """per band (<60, 60-150, 150-400, 400-1.2k, 1.2k+): the FX return's energy re the dry signal's energy in the same band (dB), mono sum"""
    ex, ed = {}, {}
    for name, sig in (("fx", fx), ("dry", dry)):
        x = sig.mean(1)
        win = np.hanning(nfft)
        f = np.fft.rfftfreq(nfft, 1 / FS)
        tot = {b[0]: 0.0 for b in D.BANDS}
        for s in range(_s(t0_ms), max(min(_s(t1_ms), len(x)) - nfft, _s(t0_ms) + 1), nfft // 2):
            if s + nfft > len(x):
                break
            P = np.abs(np.fft.rfft(x[s:s + nfft] * win)) ** 2
            for n, lo, hi in D.BANDS:
                tot[n] += P[(f >= lo) & (f < hi)].sum()
        (ex if name == "fx" else ed).update(tot)
    return {k: float(10 * np.log10(max(ex[k], 1e-9) / max(ed[k], 1e-9))) for k in ex}
