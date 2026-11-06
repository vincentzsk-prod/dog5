# SPDX-License-Identifier: GPL-3.0-only
"""Measurements new in Batch 4B (Chapter II tape / crash pair: 13 Ghost Board, 14 Reef Break).  Older measures: batch04a_metrics.py (sends separated, return windows, first repeat,
width, MUD in windows), batch03a_metrics.py (crest, PWM, drift), batch02a_metrics.py (level, bands, tails).  Definitions: dog5-docs/voicing/README.md section 17."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import batch02a_metrics as M
import batch03a_metrics as N
import batch04a_metrics as Q

FS = K.FS
_s = N._s
CRASH_BANDS = (("60-150", 60, 150), ("150-400", 150, 400), ("400-1.2k", 400, 1200), ("1.2k-4k", 1200, 4000), ("4k+", 4000, 20000))
CRASH_WINS = ((0, 50), (50, 150), (150, 400), (400, 800), (800, 1500))


def band_frames(a, t0_ms, t1_ms, bands=CRASH_BANDS, nfft=512, hop=128):
    """short-time band energy of the mono sum (dB, arbitrary full-scale reference) in frames of 512 samples (11.6 ms, Hann), hop 128 (2.9 ms), over [t0, t1] ms:
    ({band: dB array}, frame centre times in ms from t0)"""
    x = a.mean(1)[_s(t0_ms):_s(t1_ms)]
    win = np.hanning(nfft)
    f = np.fft.rfftfreq(nfft, 1 / FS)
    out = {b[0]: [] for b in bands}
    ts = []
    for s in range(0, len(x) - nfft, hop):
        P = np.abs(np.fft.rfft(x[s:s + nfft] * win)) ** 2
        for n, lo, hi in bands:
            out[n].append(10 * np.log10(max(P[(f >= lo) & (f < hi)].sum(), 1e-3) / nfft ** 2 / 32767 ** 2 * 1e9 + 1e-9))
        ts.append((s + nfft / 2) / FS * 1000)
    return {k: np.array(v) for k, v in out.items()}, np.array(ts)


def decay_to(env, ts, drops=(20, 40)):
    """ms after the band's own peak until its short-time energy first falls `drop` dB below that peak (None = not reached inside the window)"""
    k = int(np.argmax(env))
    r = {"peak_ms": float(ts[k])}
    for d in drops:
        b = np.nonzero(env[k:] <= env[k] - d)[0]
        r[f"t{d}"] = float(ts[k + b[0]] - ts[k]) if len(b) else None
    return r


def band_table(a, on_ms, dry=None, wins=CRASH_WINS, bands=CRASH_BANDS):
    """the isolated hit's band energy per window (dB re the loudest band-window of the hit) and each band's decay to -20 / -40 dB from its own peak (11.6 ms frames, window 1.5 s
    after the onset); dc is not removed (every band is above 60 Hz)"""
    x = a.mean(1)
    tab, tot = {}, {}
    for n, lo, hi in bands:
        tab[n] = []
    for w0, w1 in wins:
        seg = x[_s(on_ms + w0):_s(on_ms + w1)]
        nf = max(len(seg), 1024)
        X = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), nf)) ** 2
        f = np.fft.rfftfreq(nf, 1 / FS)
        for n, lo, hi in bands:
            tab[n].append(10 * np.log10(max(X[(f >= lo) & (f < hi)].sum() / len(seg), 1e-6)))
    ref = max(max(v) for v in tab.values())
    tab = {k: [float(x - ref) for x in v] for k, v in tab.items()}
    env, ts = band_frames(a, on_ms, on_ms + 1500, bands)
    dec = {n: decay_to(env[n], ts) for n in env}
    return {"windows": tab, "decay": dec}


def rail_share(a, t0_ms, t1_ms, thr=0.9, win_ms=5.0):
    """the share of samples (mid channel) within 10 % of the rail (the largest |x| of each 5 ms window) over [t0, t1]: the pixelation measure of 05 (a hard-clipped square ~100 %, noise ~ 10-20 %)"""
    x = a.mean(1)[_s(t0_ms):_s(t1_ms)]
    w = _s(win_ms)
    n = 0
    tot = 0
    for i in range(0, len(x) - w, w):
        seg = np.abs(x[i:i + w])
        n += int((seg >= thr * seg.max()).sum())
        tot += len(seg)
    return 100.0 * n / max(tot, 1)


def noise_vs_sub(exe, params, note, on_ms=3000, t0=0, t1=100, gate=300):
    """the noise-to-sub level ratio in the first 100 ms of a hit: the same patch rendered twice, the sub alone (NOISE 0) and the noise alone (the oscillators off), sends off
    (stereo RMS over [on+t0, on+t1] ms; dB noise minus dB sub, and each in dBFS).  A random seed note is struck first (identical in both)"""
    base = {**params, **Q.FXOFF_ALL}
    ev = [f"{on_ms} midi 0x90 {note} 108", f"{on_ms + gate} midi 0x80 {note} 0"]
    res = {}
    for nm, ov in (("sub", {"NOISE": 0}), ("noise", {"O1_WAVE": 0, "O2_WAVE": 0})):
        a = N._run(exe, "nvs", N._probe_script({**base, **ov}, ev, on_ms + 1500))
        res[nm] = M.rms_db(a, on_ms + t0, on_ms + t1)
    res["ratio"] = res["noise"] - res["sub"]
    return res


def sub_decay(a, on_ms, lo=40, hi=150):
    """the sub's own decay: the 40-150 Hz band's energy envelope (frames of 2048 samples, hop 512: the band is low) from its peak to -20 / -40 dB"""
    env, ts = band_frames(a, on_ms, on_ms + 1500, (("sub", lo, hi),), nfft=2048, hop=512)
    return decay_to(env["sub"], ts)


def tape_probe(exe, params, note=57, on=3000, off=6000):
    """the tape deck's pitch wander on a one-voice probe: POLY, VINTAGE 0, LFO PITCH / PWM / AMP 0, ECHO and SPRING off, the patch's own CHEW / WOW-FLT / HISS / DROPS: the common-mode
    wander of a held note's fundamental in cents (N.drift_track: centroid of f0 +-12 % in 100 ms frames): s.d., 5-95 % range, strongest rate (Hz), and the level's own dips
    (dips >= 6 dB in the held note); also with CHEW 0 (the voice alone) for the same two numbers"""
    out = {}
    for nm, ov in (("tape", {}), ("voice", {"CHEW": 0})):
        q = {**params, **ov, "MODE": 0, "VINTAGE": 0, "LFO_PITCH": 0, "LFO_PWM": 0, "LFO_AMP": 0, "LFO_FLT": 0, "DLY_MIX": 0, "REV_MIX": 0, "GROWL": 0, "O2_WAVE": 0}
        a = N._run(exe, "tpr", N._probe_script(q, [f"{on} midi 0x90 {note} 100", f"{off} midi 0x80 {note} 0"], off + 400))
        f0 = 440 * 2 ** ((note - 69) / 12)
        d = N.drift_track(a, f0, on, off, settle_ms=300)
        dp = M.dips(a, on + 300, off)
        out[nm] = {"sd": d["sd"], "range": d["range"], "rate": d["rate"], "dip_db": dp[0], "dips": dp[1]}
    return out


def harmonics_tri(exe, params):
    """harmonics 3 / 5 / 7 of a held A2 re the fundamental through the patch's OSC 1 and filter at rest (no LFO, no envelopes, no tape, no sends): triangle -19.1 / -28.0 / -34.2, square -9.5 / -14.0 / -16.9"""
    import batch02a as B2
    q = {**params, "LFO_PWM": 0, "LFO_PITCH": 0, "LFO_AMP": 0, "LFO_FLT": 0, "O2_WAVE": 0, "NOISE": 0, "MODE": 0, "CHEW": 0, "DRIVE": params.get("DRIVE", 0)}
    return B2.triangle_probe(exe, q)[1:]


def hit_attack(a, on_ms, win_ms=1.0, hop_ms=0.25, span_ms=300):
    """the amp attack of a decaying hit as 10 / 50 / 90 % of its PEAK (voltage): the stereo RMS envelope in trailing 1 ms windows (hop 0.25 ms) over the first span_ms after the note-on; the
    time zero is the first sample above -50 dB of the peak; also the peak's own time (ms from that zero)"""
    x = (a ** 2).mean(1)
    w, hop = _s(win_ms), max(int(hop_ms * FS / 1000), 1)
    seg = x[_s(on_ms - 5):_s(on_ms + span_ms)]
    c = np.concatenate([[0.0], np.cumsum(seg)])
    idx = np.arange(w, len(seg), hop)
    e = np.sqrt((c[idx] - c[idx - w]) / w)
    pk = e.max()
    t0 = idx[np.nonzero(e >= pk * 10 ** (-50 / 20))[0][0]]
    t = (idx - t0) / FS * 1000
    r = {f"t{k}": float(t[np.nonzero(e >= k / 100 * pk)[0][0]]) for k in (10, 50, 90)}
    r["peak_ms"] = float(t[int(np.argmax(e))])
    return r


def repeats_re_burst(S, on_ms, delay_ms, n=14):
    """an isolated hit's delay-only return as a train: the peak of the 4 ms envelope in each successive slot of one delay time (k * delay - 30 ms ..) in dB re the DRY hit's own peak: [(k, dB)];
    the count of repeats above -40 dB re the burst is the length of the echo"""
    d = S["dly"] - S["dry"]
    e, ed = M.env_ms(d), M.env_ms(S["dry"])
    i0 = int(on_ms)
    pk0 = float(ed[i0:i0 + 400].max())
    out = []
    for k in range(1, n + 1):
        a, b = i0 + int(k * delay_ms - 30), i0 + int((k + 1) * delay_ms - 30)
        seg = e[a:b]
        if len(seg) < 4:
            break
        out.append((k, float(seg.max() - pk0)))
    return out


def echo_windows(S, on_ms, delay_ms, slots=(1, 2, 3)):
    """the band split of the delay's return in the first slots (MUD, centroid, 60-150 share): is the sub building up a tubby 150-400 Hz body in the repeats?  [{slot, mud, cent, shares}]"""
    d = S["dly"] - S["dry"]
    out = []
    for k in slots:
        sp = Q.window_split(d, on_ms + k * delay_ms - 30, on_ms + k * delay_ms + 250)
        sp["slot"] = k
        out.append(sp)
    return out
