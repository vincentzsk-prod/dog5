# SPDX-License-Identifier: GPL-3.0-only
"""Measurements new in Batch 3B, "the wreck and chop set" (05 ZEAROX, 07 Tape Splice, 15 Trem Chop).

Everything reads a host render (stereo float array from t = 0, 44.1 kHz) and returns numbers; batch03b.py decides which render is which.
Older measures: voicekit.py, batch02a_metrics.py, batch03a_metrics.py.  Definitions: dog5-docs/voicing/README.md section 14."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import batch02a_metrics as M
import batch03a_metrics as N

FS = K.FS
_s = N._s
BANDS = [("<60", 0, 60), ("60-150", 60, 150), ("150-400", 150, 400), ("400-1.2k", 400, 1200), ("1.2k+", 1200, 22050)]


# ---- 05: where the kick lives ------------------------------------------------------------------------------------
def hp(a, fc, order=2):
    """zero-phase Butterworth-magnitude high-pass (|H| = 1/sqrt(1+(fc/f)^(2 order))): what a small speaker keeps"""
    n = len(a)
    f = np.fft.rfftfreq(n, 1 / FS)
    f[0] = 1e-9
    H = 1 / np.sqrt(1 + (fc / f) ** (2 * order))
    return np.stack([np.fft.irfft(np.fft.rfft(a[:, c]) * H, n) for c in (0, 1)], 1)


def small_speaker(a, phrase, fcs=(60, 100)):
    """the level of the note-on region after a 2nd-order high-pass at each fc, in dB RE the unfiltered level: how much of the sound a
    speaker that cannot reproduce below fc still plays (0 = all of it)"""
    m = K.gate_mask(phrase, len(a))
    full = (a[m] ** 2).mean()
    return {str(fc): float(10 * np.log10((hp(a, fc)[m] ** 2).mean() / full)) for fc in fcs}


def bsplit(a, t0_ms, t1_ms):
    """% of the energy per band (<60, 60-150, 150-400, 400-1.2k, 1.2k+) of the mono sum over [t0, t1] ms, one Hann-windowed FFT (zero-padded to 4096)"""
    x = a.mean(1)[_s(t0_ms):_s(t1_ms)]
    if len(x) < 32:
        return [0.0] * 5
    n = max(4096, 1 << int(np.ceil(np.log2(len(x)))))
    P = np.abs(np.fft.rfft(x * np.hanning(len(x)), n)) ** 2
    f = np.fft.rfftfreq(n, 1 / FS)
    e = [P[(f >= lo) & (f < hi)].sum() for _, lo, hi in BANDS]
    t = sum(e)
    return [100 * v / t if t > 0 else 0.0 for v in e]


KICK_WINS = ((0, 10, "click 0-10 ms"), (10, 50, "body 10-50 ms"), (50, 150, "tail 50-150 ms"))


def onset(a, t_nom_ms, floor_db=-60.0, search=(-8.0, 12.0)):
    """where a hit really starts: the host quantises note events to its blocks, so the sound begins up to a few ms either side of the phrase's nominal time.
    The first sample whose magnitude passes floor_db (dBFS) inside nominal + search (ms); the nominal time if there is none"""
    x = np.abs(a).max(1)
    i0, i1 = _s(t_nom_ms + search[0]), _s(t_nom_ms + search[1])
    k = np.nonzero(x[i0:i1] > 32767 * 10 ** (floor_db / 20))[0]
    return (i0 + int(k[0])) / FS * 1000.0 if len(k) else float(t_nom_ms)


def kick_hit(a, t_on):
    """one isolated hit: the band split in the click / body / tail windows and the hit's RMS over its 150 ms gate"""
    t0 = onset(a, t_on)
    return {"wins": [bsplit(a, t0 + x0, t0 + x1) for x0, x1, _ in KICK_WINS], "rms": M.rms_db(a, t_on, t_on + 150),
            "peak": M.peak_db(a, t_on, t_on + 150), "onset_shift": float(t0 - t_on),
            "click_re_body": float(M.rms_db(a, t0, t0 + 5) - M.rms_db(a, t0 + 10, t0 + 50))}


def pattern_hits(a, starts):
    """the RMS (dB) of each hit's first 150 ms: a dropout or a stolen hit shows as a dip"""
    return [M.rms_db(a, t, t + 150) for t in starts]


def fmt_list(sp):
    """a band-split list (<60 / 60-150 / 150-400 / 400-1.2k / 1.2k+) as the README writes it"""
    return " / ".join(f"{v:.0f}" for v in sp)


def share_above(sp, i0):
    """% of a band split above band index i0 (1 = above 60 Hz)"""
    return float(sum(sp[i0:]))


# ---- pitch track and onsets ---------------------------------------------------------------------------------------
def f0_track(x, fmin, fmax, frame_ms=40.0, hop_ms=10.0):
    """pitch of a mono signal in cents against its median, by autocorrelation (frame_ms Hann frames, parabolic peak): returns (times s, cents).
    Frames with a weak peak (< 0.3) are dropped.  Used on a held note: its s.d. / range / the strongest component is the wobble"""
    nf, hop = int(FS * frame_ms / 1000), int(FS * hop_ms / 1000)
    lo, hi = int(FS / fmax), int(FS / fmin)
    ts, ps = [], []
    w = np.hanning(nf)
    for s in range(0, len(x) - nf, hop):
        f = x[s:s + nf] * w
        n = 1 << int(np.ceil(np.log2(2 * nf)))
        F = np.fft.rfft(f, n)
        ac = np.fft.irfft(np.abs(F) ** 2, n)[:hi + 2]
        ac /= max(ac[0], 1e-9)
        k = lo + int(np.argmax(ac[lo:hi]))
        if ac[k] < 0.3 or k <= lo or k >= hi - 1:
            continue
        y0, y1, y2 = ac[k - 1], ac[k], ac[k + 1]
        d = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2)
        ts.append((s + nf / 2) / FS)
        ps.append(FS / (k + d))
    ps = np.array(ps)
    return np.array(ts), 1200 * np.log2(ps / np.median(ps)) if len(ps) else ps


def wobble(a, f0, t0_ms, t1_ms, settle_ms=100):
    """the pitch wobble of a held note: the autocorrelation track over [t0 + settle, t1] ms: s.d. (cents), 5-95 % range, the strongest component 0.3-15 Hz of
    the track (Hz) and the share of frames kept"""
    x = a.mean(1)[_s(t0_ms + settle_ms):_s(t1_ms)]
    t, c = f0_track(x, f0 * 0.7, f0 * 1.4)
    if len(c) < 20:
        return {"sd": float("nan"), "range": float("nan"), "rate": float("nan"), "kept": 0.0}
    tt = np.arange(0, t[-1] + 0.01, 0.01)
    ci = np.interp(tt, t, c)
    X = np.abs(np.fft.rfft((ci - ci.mean()) * np.hanning(len(ci)), 1 << 14)) ** 2
    fr = np.fft.rfftfreq(1 << 14, 0.01)
    sel = (fr >= 0.3) & (fr <= 15)
    return {"sd": float(c.std()), "range": float(np.percentile(c, 95) - np.percentile(c, 5)), "rate": float(fr[sel][int(np.argmax(X[sel]))]),
            "kept": float(len(c) / max((len(x) - int(FS * 0.04)) / int(FS * 0.01), 1))}


def env_peak(a, win_ms=1.0, hop_ms=0.25):
    """the largest |sample| of either channel in a trailing window (default 1 ms), every hop_ms: (envelope array in full-scale units, hop ms)"""
    x = np.abs(a).max(1)
    w, h = max(int(FS * win_ms / 1000), 1), max(int(FS * hop_ms / 1000), 1)
    idx = np.arange(w, len(x), h)
    # trailing max via a strided view
    from numpy.lib.stride_tricks import sliding_window_view
    e = sliding_window_view(x, w)[::h].max(1)
    return e[:len(idx)] / 32767.0, hop_ms


def edges(a, notes, pre_ms=6.0, post_ms=40.0, win_ms=1.0):
    """the note edges of a staccato phrase, from the 1 ms peak envelope.  For each (on, off) ms: the note's body level = the 90th percentile of the
    envelope inside the gate; onset delay = ms from the note-on to the envelope first exceeding body - 20 dB (the tape's latency + the attack);
    end delay = ms from the note-off to the envelope first falling below body - 40 dB (the release: the chop).  Returns the lists and their s.d."""
    e, hop = env_peak(a, win_ms)
    on_d, off_d = [], []
    for on, off in notes:
        i0, i1 = int((on - pre_ms) / hop), int((off + 200) / hop)
        seg = e[i0:i1]
        if len(seg) < 10:
            continue
        g0, g1 = int(pre_ms / hop), int((off - on + pre_ms) / hop)
        body = np.percentile(seg[g0:g1], 90)
        if body <= 1e-5:
            continue
        up = np.nonzero(seg >= body * 10 ** (-20 / 20))[0]
        if len(up):
            on_d.append(up[0] * hop - pre_ms)
        dn = np.nonzero(seg[g1:] <= body * 10 ** (-40 / 20))[0]
        if len(dn):
            off_d.append(dn[0] * hop + (g1 * hop - (off - on + pre_ms)))
    r = lambda v: {"vals": [float(x) for x in v], "mean": float(np.mean(v)) if len(v) else float("nan"), "sd": float(np.std(v)) if len(v) else float("nan"),
                   "min": float(np.min(v)) if len(v) else float("nan"), "max": float(np.max(v)) if len(v) else float("nan")}
    return {"onset": r(on_d), "end": r(off_d)}


# ---- 15: the chop -------------------------------------------------------------------------------------------------
def chop(a, t0_ms, t1_ms, win_ms=2.0, hop_ms=0.5):
    """the chop of a held note over [t0, t1] ms (the part after the LFO has settled).  Envelope = RMS over win_ms every hop_ms (dB).  ON level = median of
    the upper half of the envelope, OFF level = median of the lower tenth; depth = ON - OFF (dB); edges = the crossings of the midpoint (in dB between ON and
    OFF), rising and falling; rate = 1 / the mean period of the rising edges; period s.d. (ms) and the s.d. of the rising edges' times about the straight line
    through them (ms) = the edge timing jitter; on-time = the mean share of a cycle spent above the midpoint (duty)"""
    x = a[_s(t0_ms):_s(t1_ms)]
    p = (x ** 2).mean(1)
    w, h = int(FS * win_ms / 1000), int(FS * hop_ms / 1000)
    c = np.concatenate([[0.0], np.cumsum(p)])
    idx = np.arange(0, len(p) - w, h)
    e = 10 * np.log10(np.maximum((c[idx + w] - c[idx]) / w, 1e-3) / 32767 ** 2)
    on = float(np.median(e[e >= np.percentile(e, 50)]))
    off = float(np.median(e[e <= np.percentile(e, 10)]))
    mid = (on + off) / 2
    above = e > mid
    rise = np.nonzero(~above[:-1] & above[1:])[0]
    fall = np.nonzero(above[:-1] & ~above[1:])[0]
    t = (idx + w / 2) / FS * 1000.0
    rt, ft = t[rise], t[fall]
    out = {"on_db": on, "off_db": off, "depth": on - off, "n_rise": int(len(rt))}
    if len(rt) >= 3:
        per = np.diff(rt)
        k = np.arange(len(rt))
        fit = np.polyval(np.polyfit(k, rt, 1), k)
        out.update(rate=float(1000.0 / per.mean()), period_ms=float(per.mean()), period_sd=float(per.std()), edge_sd=float((rt - fit).std()),
                   edge_range=float(np.ptp(rt - fit)))
    else:
        out.update(rate=float("nan"), period_ms=float("nan"), period_sd=float("nan"), edge_sd=float("nan"), edge_range=float("nan"))
    if len(rt) and len(ft):
        f_ = ft[ft > rt[0]]
        n = min(len(f_), len(rt) - 1)
        out["duty"] = float(np.mean(f_[:n] - rt[:n]) / out["period_ms"]) if n and out["period_ms"] == out["period_ms"] else float("nan")
    else:
        out["duty"] = float("nan")
    return out


def edge_rise(exe, params, note=93, vel=100, hold_ms=1500, win_ms=None):
    """how hard the chop's edge is: the patch struck on a very high note (A6 1760 Hz: period 0.57 ms) and held; the peak envelope in a window of one period
    (hop 0.05 ms); every rising edge of the chop (the envelope crossing the midpoint between its OFF and ON levels) is measured 10 -> 90 % of the amplitude step
    (voltage, linear in amplitude); returns the median and the largest of those rises (ms) and the number of edges.  The window is one period, so the figure cannot
    be smaller than 0.6 ms: it is an upper bound on the edge"""
    lines = [f"{K.T_SELECT} midi 0xC0 {K.INIT_PROGRAM} 0"] + [f"{K.T_PARAMS} param {K.PARAM_IDS[k]} {v}" for k, v in params.items()]
    lines += [f"3000 midi 0x90 {note} {vel}", f"{3000 + hold_ms} midi 0x80 {note} 0", f"{3000 + hold_ms + 300} end"]
    a = N._run(exe, "edge", lines)
    f0 = 440 * 2 ** ((note - 69) / 12)
    w = max(int(FS / f0), 1)
    x = np.abs(a).max(1)
    from numpy.lib.stride_tricks import sliding_window_view
    step = max(int(0.00005 * FS), 1)
    e = sliding_window_view(x, w)[::step].max(1) / 32767.0
    dt = step / FS * 1000.0
    i0, i1 = int(3150 / dt), int((3000 + hold_ms) / dt)
    seg = e[i0:i1]
    hi, lo = np.percentile(seg, 90), np.percentile(seg, 3)
    if hi < 1e-4 or hi / max(lo, 1e-6) < 2:
        return {"median": float("nan"), "max": float("nan"), "n": 0, "hi": float(hi), "lo": float(lo)}
    mid = (hi + lo) / 2
    rises = []
    above = seg > mid
    for i in np.nonzero(~above[:-1] & above[1:])[0]:
        j0 = i
        while j0 > 0 and seg[j0] > lo + 0.1 * (hi - lo):
            j0 -= 1
        j1 = i
        while j1 < len(seg) - 1 and seg[j1] < lo + 0.9 * (hi - lo):
            j1 += 1
        rises.append((j1 - j0) * dt)
    return {"median": float(np.median(rises)) if rises else float("nan"), "max": float(max(rises)) if rises else float("nan"), "n": len(rises),
            "hi": float(hi), "lo": float(lo)}


def first_edge_spread(a, notes, win_ms=2.0, hop_ms=0.5, search_ms=250):
    """does the chop start the same way on every note?  For each (on, off): the state of the 2-ms envelope 4 ms after the note-on (ON = above the midpoint
    between the note's loud and quiet levels) and the time from the note-on to its first crossing of that midpoint (ms): where the first chop edge falls.
    Returns the states, the times, the number of notes that start ON, and the mean / s.d. of the times (same state, same time on every note = the chop is
    locked to the notes, LFO PHASE SYNC; different = it does not know where the note began)"""
    states, times = [], []
    for on, off in notes:
        x = a[_s(on):_s(min(off, on + search_ms))]
        p = (x ** 2).mean(1)
        w, h = int(FS * win_ms / 1000), int(FS * hop_ms / 1000)
        c = np.concatenate([[0.0], np.cumsum(p)])
        idx = np.arange(0, len(p) - w, h)
        if len(idx) < 8:
            continue
        en = 10 * np.log10(np.maximum((c[idx + w] - c[idx]) / w, 1e-3) / 32767 ** 2)
        hi, lo = np.percentile(en, 90), np.percentile(en, 5)
        if hi - lo < 6:
            continue
        mid = (hi + lo) / 2
        k0 = int(4.0 / hop_ms)
        st = en[k0] > mid
        cross = np.nonzero((en[k0:] > mid) != st)[0]
        states.append(bool(st))
        times.append(float((cross[0] + k0) * hop_ms) if len(cross) else float("nan"))
    t = np.array([v for v in times if v == v])
    return {"states": states, "vals": times, "n_on": int(sum(states)), "n": len(states), "mean": float(t.mean()) if len(t) else float("nan"),
            "sd": float(t.std()) if len(t) else float("nan")}


def paired(a_vals, b_vals):
    """the per-note difference of two measurements of the same notes (e.g. onset with the tape minus onset without it): mean, s.d., range (ms)"""
    n = min(len(a_vals), len(b_vals))
    d = np.array(a_vals[:n]) - np.array(b_vals[:n])
    if not n:
        return {"mean": float("nan"), "sd": float("nan"), "min": float("nan"), "max": float("nan"), "n": 0}
    return {"mean": float(d.mean()), "sd": float(d.std()), "min": float(d.min()), "max": float(d.max()), "n": int(n)}


def hold_dips(exe, params, note=45, hold_ms=12000):
    """dropouts in a long hold (a probe render of its own: the patch's note held 12 s): the 10-ms envelope over 0.5 .. hold - 0.5 s; the deepest dip below the median
    (dB) and the number of dips of 6 dB or more.  The tape's dropouts are random but the render is deterministic, so the count is reproducible"""
    lines = [f"{K.T_SELECT} midi 0xC0 {K.INIT_PROGRAM} 0"] + [f"{K.T_PARAMS} param {K.PARAM_IDS[k]} {v}" for k, v in params.items()]
    lines += [f"3000 midi 0x90 {note} 100", f"{3000 + hold_ms} midi 0x80 {note} 0", f"{3000 + hold_ms + 200} end"]
    # (the exe is passed in: see batch03b.py)
    a = N._run(exe, "hold", lines)
    d, n = M.dips(a, 3500, 3000 + hold_ms - 500)
    return {"deepest": d, "n": n}


def hit_attack(a, t_on, win_ms=0.5):
    """the attack of one kick hit from a 0.5 ms peak envelope: ms from the key-down to 10 % (-20 dB) of the hit's peak, to 90 % of the peak (voltage), and the
    time of the peak (ms)"""
    t_on = onset(a, t_on)
    x = np.abs(a).max(1)[_s(t_on - 2):_s(t_on + 150)]
    w = max(int(FS * win_ms / 1000), 1)
    from numpy.lib.stride_tricks import sliding_window_view
    e = sliding_window_view(x, w).max(1) / 32767.0
    pk = e.max()
    t = np.arange(len(e)) / FS * 1000.0 - 2.0
    return {"t_start": float(t[np.nonzero(e >= pk * 0.1)[0][0]]), "t90": float(t[np.nonzero(e >= pk * 0.9)[0][0]]), "t_peak": float(t[int(np.argmax(e))])}


def hit_dropouts(exe, params, n=48, note=33, gate=150, step=500):
    """does the tape drop a kick?  n hits of one note (4 a bar at 120 BPM, 24 s), the RMS of each hit's 150 ms; returns the number of hits more than 3 dB / 6 dB
    below the median hit and the deepest dip (dB).  A probe render (the dropouts are random but the render is deterministic)"""
    lines = [f"{K.T_SELECT} midi 0xC0 {K.INIT_PROGRAM} 0"] + [f"{K.T_PARAMS} param {K.PARAM_IDS[k]} {v}" for k, v in params.items()]
    for i in range(n):
        lines += [f"{3000 + step * i} midi 0x90 {note} 100", f"{3000 + step * i + gate} midi 0x80 {note} 0"]
    lines += [f"{3000 + step * n + 200} end"]
    a = N._run(exe, "hits", lines)
    lv = np.array([M.rms_db(a, 3000 + step * i, 3000 + step * i + gate) for i in range(n)])
    med = np.median(lv)
    return {"n3": int((lv < med - 3).sum()), "n6": int((lv < med - 6).sum()), "deepest": float(med - lv.min()), "n": n}


def level_shares(a, t0_ms, t1_ms, win_ms=2.0):
    """how many levels does the chop have?  The 2 ms RMS envelope over [t0, t1], in dB under its 95th percentile: the % of the time it spends OFF (more than
    30 dB under), at one voice's level (4-12 dB under: a DUAL pair with one voice chopped off) and FULL (within 4 dB).  A clean gate is mostly off + full"""
    x = a[_s(t0_ms):_s(t1_ms)]
    p = (x ** 2).mean(1)
    w = int(FS * win_ms / 1000)
    c = np.concatenate([[0.0], np.cumsum(p)])
    e = 10 * np.log10(np.maximum((c[w:] - c[:-w]) / w, 1e-3) / 32767 ** 2)[::max(w // 4, 1)]
    d = e - np.percentile(e, 95)
    return [float(100 * (d < -30).mean()), float(100 * ((d >= -12) & (d < -4)).mean()), float(100 * (d >= -4).mean())]
