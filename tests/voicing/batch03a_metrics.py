# SPDX-License-Identifier: GPL-3.0-only
"""Measurements new in Batch 3A, "the fat and driven set" (01 Red Pill, 02 Cement Grind, 06 zzuFuzz, 08 Wire Bite).

Everything reads a host render (stereo float array from t = 0, 44.1 kHz) and returns numbers; batch03a.py decides which render is which.
The older measures (level, centroid, band split, tails, DC) are batch02a_metrics.py / voicekit.py.  Definitions: dog5-docs/voicing/README.md section 12."""
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import batch02a_metrics as M

FS = K.FS


def _s(ms):
    return int(round(ms * FS / 1000))


def crest_db(a, phrase=None, t0_ms=None, t1_ms=None):
    """crest factor: peak / RMS in dB, over the phrase's note-on region (both channels) or over [t0, t1] ms"""
    if phrase is not None:
        m = K.gate_mask(phrase, len(a))
        x = a[m]
    else:
        x = a[_s(t0_ms):_s(t1_ms)]
    return float(20 * np.log10(np.abs(x).max() / np.sqrt((x ** 2).mean())))


def rise_ms(a, on_ms, f0, window_ms=150.0):
    """attack time as heard in the render: the envelope is the largest |sample| of either channel in a sliding window of one period of the note (hop 0.5 ms);
    the time from 10 % to 90 % of its peak inside the first window_ms after the note-on (ms, measured from the key-down).  Also the time to 10 %"""
    x = np.abs(a).max(1)
    w = max(int(FS / f0), int(0.003 * FS))
    hop = int(0.0005 * FS)
    i0 = _s(on_ms) - int(0.002 * FS)
    seg = x[i0 - w:i0 + _s(window_ms)]
    idx = np.arange(w, len(seg), hop)
    e = np.array([seg[i - w:i].max() for i in idx])       # trailing window: the envelope rises as the first peaks arrive
    t = (idx - w) / FS * 1000 - 2.0
    pk = e.max()
    t10 = t[np.nonzero(e >= 0.1 * pk)[0][0]]
    t90 = t[np.nonzero(e >= 0.9 * pk)[0][0]]
    return {"t10": float(t10), "t90": float(t90), "rise": float(t90 - t10), "peak_ms": float(t[int(np.argmax(e))])}


def level_curve(a, on_ms, hold_ms, step_ms=500):
    """RMS dBFS per step_ms window across a held note: [(t_s after note-on, dB)]"""
    return [(t / 1000, M.rms_db(a, on_ms + t, on_ms + t + step_ms)) for t in range(0, int(hold_ms) - step_ms + 1, step_ms)]


def wet_windows(wet, dry, t_on_ms, wins=((0, 20), (20, 100), (100, 250))):
    """the effects' own return (wet - dry, the same params with DLY_MIX and DRAIN 0) against the dry note, per time window after a note-on:
    [(window, dry dB, return dB, return re dry dB)].  The dry is read as it falls (its release included): a short note's dry is already dying in the last window"""
    fx = wet - dry
    out = []
    for a, b in wins:
        d, f = M.rms_db(dry, t_on_ms + a, t_on_ms + b), M.rms_db(fx, t_on_ms + a, t_on_ms + b)
        out.append({"w": (a, b), "dry_db": d, "fx_db": f, "re_dry_db": f - d})
    return out


def band_env(a, t0_ms, t1_ms, bands, nfft=1024, hop=256):
    """short-time energy (dB) of the mono sum in each band over [t0, t1]: {band: np.array}, frame rate FS/hop"""
    x = a.mean(1)[_s(t0_ms):_s(t1_ms)]
    win = np.hanning(nfft)
    f = np.fft.rfftfreq(nfft, 1 / FS)
    out = {b: [] for b in bands}
    for s in range(0, len(x) - nfft, hop):
        P = np.abs(np.fft.rfft(x[s:s + nfft] * win)) ** 2
        for b, (lo, hi) in bands.items():
            out[b].append(10 * np.log10(max(P[(f >= lo) & (f < hi)].sum(), 1e-3)))
    return {b: np.array(v) for b, v in out.items()}, FS / hop


def mod_rate_depth(series, frame_rate, lo=0.8, hi=20.0):
    """the modulation of a dB series: depth = 95th - 5th percentile (dB), rate = the strongest component between lo and hi Hz (Hz) and its share of
    the modulation power in that range (0..1: 1 = a clean periodic swing)"""
    s = series - series.mean()
    depth = float(np.percentile(series, 95) - np.percentile(series, 5))
    n = 1 << 15
    X = np.abs(np.fft.rfft(s * np.hanning(len(s)), n)) ** 2
    f = np.fft.rfftfreq(n, 1 / frame_rate)
    sel = (f >= lo) & (f <= hi)
    k = int(np.argmax(X[sel]))
    tot = X[(f >= 0.2) & (f <= hi)].sum()
    return depth, float(f[sel][k]), float(X[sel][max(k - 3, 0):k + 4].sum() / max(tot, 1e-9))


PWM_BANDS = {"150-400": (150, 400), "400-1.2k": (400, 1200), "1.2k-3k": (1200, 3000), "3k+": (3000, 10000)}


def pwm_metrics(a, on_ms, off_ms, settle_ms=400):
    """how obvious the PWM is: over the steady part of a held note the band energies (20-ms frames) are modulated; per band the depth in dB (95th - 5th
    percentile) and the rate in Hz; the broadband level's own modulation.  Returns {band: (depth, rate, purity)} plus the strongest band"""
    env, fr = band_env(a, on_ms + settle_ms, off_ms, PWM_BANDS)
    res = {b: mod_rate_depth(v, fr) for b, v in env.items()}
    x = a.mean(1)[_s(on_ms + settle_ms):_s(off_ms)]
    nfft, hop = 1024, 256
    lv = np.array([10 * np.log10(max((x[s:s + nfft] ** 2).mean(), 1e-3)) for s in range(0, len(x) - nfft, hop)])
    res["level"] = mod_rate_depth(lv, fr)
    best = max(PWM_BANDS, key=lambda b: res[b][0] * (res[b][2] > 0.15))
    return {"bands": res, "best": best}


def drift_track(a, f0, on_ms, off_ms, settle_ms=300, win_ms=100, hop_ms=25):
    """the common-mode wander of the stack, in cents: the centroid of the power in f0 +-12 % in 100-ms frames (zero-padded), against its median.
    Returns s.d. (cents), the 5-95 % range, the fastest typical rate (Hz, strongest component 0.1 .. 8 Hz of the track), the track itself"""
    x = a.mean(1)[_s(on_ms + settle_ms):_s(off_ms)]
    nf, hop = _s(win_ms), _s(hop_ms)
    N = 1 << 15
    f = np.fft.rfftfreq(N, 1 / FS)
    sel = (f > f0 * 0.88) & (f < f0 * 1.12)
    win = np.hanning(nf)
    cs = []
    for s in range(0, len(x) - nf, hop):
        P = np.abs(np.fft.rfft(x[s:s + nf] * win, N)) ** 2
        cs.append((f[sel] * P[sel]).sum() / max(P[sel].sum(), 1e-9))
    cs = np.array(cs)
    c = 1200 * np.log2(cs / np.median(cs))
    sd = float(c.std())
    rng = float(np.percentile(c, 95) - np.percentile(c, 5))
    X = np.abs(np.fft.rfft((c - c.mean()) * np.hanning(len(c)), 1 << 14)) ** 2
    fr = np.fft.rfftfreq(1 << 14, hop_ms / 1000)
    sl = (fr >= 0.1) & (fr <= 8)
    return {"sd": sd, "range": rng, "rate": float(fr[sl][int(np.argmax(X[sl]))]), "track": c}


def zap_metrics(a, on_ms, body=(150, 300)):
    """the zap of a note-on: centroid of the first 23 ms against the next 67 ms (Hz), and the energy above 1.2 kHz in the first 40 ms re the same band
    in the body (the body = 150 .. 300 ms after the note-on), dB: positive = a burst of top at the start"""
    c0, c1, r = M.attack_snap(a, on_ms)
    hi = {"hi": (1200, 12000)}
    e0, _ = band_env(a, on_ms, on_ms + 40, hi, nfft=512, hop=128)
    e1, _ = band_env(a, on_ms + body[0], on_ms + body[1], hi, nfft=512, hop=128)
    return {"c_attack": c0, "c_body": c1, "ratio": r, "burst_db": float(e0["hi"].max() - np.median(e1["hi"]))}


def _run(exe, tag, lines):
    path = os.path.join(K.BUILD, tag + ".txt")
    open(path, "w").write("\n".join(lines) + "\n")
    subprocess.run([exe, os.path.join(K.BUILD, tag), path], cwd=K.ROOT, check=True, capture_output=True)
    return K.read_wav(os.path.join(K.BUILD, tag + ".wav"))


def selfosc_probe(exe, params, resos=(0,), noise_hi=24, noise_lo=12):
    """does the patch's filter sing by itself?  The oscillators off, only noise feeds the filter: two renders with the noise 12 dB apart (NOISE 24 and 12:
    the level knobs are square laws, 4x in power); a linear filter answers 12 dB apart, a self-oscillating one (the level set by its own saturation, not the input)
    answers with much less.  For each RESO (0 = the patch's own value) the output RMS (dBFS, 0.5-1.4 s into a 1.5 s note, GROWL / effects off) at both noise levels
    and the difference (12 = linear; near 0 = self-oscillation)"""
    out = []
    for r in resos:
        row = {"reso": r or params["RESO"]}
        for nm, nz in (("hi", noise_hi), ("lo", noise_lo)):
            p = {**params, "O1_WAVE": 0, "O2_WAVE": 0, "NOISE": nz, "GROWL": 0, "DLY_MIX": 0, "REV_MIX": 0, "CHEW": 0, "VOLUME": 127, "LFO_PITCH": 0, "LFO_FLT": 0, "LFO_AMP": 0}
            if r:
                p["RESO"] = r
            lines = [f"{K.T_SELECT} midi 0xC0 {K.INIT_PROGRAM} 0"] + [f"{K.T_PARAMS} param {K.PARAM_IDS[k]} {v}" for k, v in p.items()]
            lines += ["3000 midi 0x90 45 100", "4500 midi 0x80 45 0", "5200 end"]
            a = _run(exe, "selfosc", lines)
            row[nm] = M.rms_db(a, 3500, 4400)
        row["diff"] = row["hi"] - row["lo"]
        out.append(row)
    return out


def _probe_script(params, notes, end_ms):
    lines = [f"{K.T_SELECT} midi 0xC0 {K.INIT_PROGRAM} 0"] + [f"{K.T_PARAMS} param {K.PARAM_IDS[k]} {v}" for k, v in params.items()]
    return lines + notes + [f"{end_ms} end"]


def attack_probe(exe, params, note=81, vel=100):
    """the attack as heard, on a high note whose period (A5, 1.1 ms) is short enough to resolve it, struck from silence: the stereo RMS envelope in trailing
    windows of one period (hop 0.25 ms); ms from the key-down (the first sample above -60 dB of the plateau) to 10 % and 90 % of the PLATEAU (the mean level
    200-400 ms after the key-down; voltage, so 10 % = -20 dB, 90 % = -0.9 dB), the 10-90 % rise, and the level re the plateau at 2 / 5 / 10 / 20 / 50 ms (dB).
    Run on the patch as it is and with GROWL and the sends off ('voice')"""
    out = {}
    for nm, ov in (("as", {}), ("voice", {"GROWL": 0, "DLY_MIX": 0, "REV_MIX": 0, "CHEW": 0})):
        a = _run(exe, "attk", _probe_script({**params, **ov}, [f"3000 midi 0x90 {note} {vel}", "3600 midi 0x80 %d 0" % note], 3900))
        x = a[_s(2990):_s(3500)]
        w, hop = int(FS / (440 * 2 ** ((note - 69) / 12))), int(0.00025 * FS)
        p = (x ** 2).mean(1)
        c = np.concatenate([[0.0], np.cumsum(p)])
        idx = np.arange(w, len(p), hop)
        e = np.sqrt((c[idx] - c[idx - w]) / w)
        plat = np.sqrt(p[_s(210):_s(410)].mean())
        t0 = idx[np.nonzero(e >= plat * 10 ** (-60 / 20))[0][0]] / FS * 1000
        t = idx / FS * 1000 - t0
        t10 = t[np.nonzero(e >= 0.1 * plat)[0][0]]
        t90 = t[np.nonzero(e >= 0.9 * plat)[0][0]]
        bloom = {str(ms): float(20 * np.log10(max(e[np.searchsorted(t, ms)], 1e-9) / plat)) for ms in (2, 5, 10, 20, 50)}
        out[nm] = {"t10": float(t10), "t90": float(t90), "rise": float(t90 - t10), "bloom": bloom, "peak_re_plateau": float(20 * np.log10(e[t < 150].max() / plat))}
    return out


def pwm_riff(a, notes, settle_ms=100):
    """the PWM on the riff itself: for each note (on, off ms) the band energies' depth (95th - 5th percentile, dB) from on+100 ms to the key-up, averaged over the notes"""
    acc = {b: [] for b in PWM_BANDS}
    lv = []
    for on, off in notes:
        env, fr = band_env(a, on + settle_ms, off, PWM_BANDS)
        for b, v in env.items():
            acc[b].append(float(np.percentile(v, 95) - np.percentile(v, 5)))
        x = a.mean(1)[_s(on + settle_ms):_s(off)]
        e = np.array([10 * np.log10(max((x[i:i + 1024] ** 2).mean(), 1e-3)) for i in range(0, len(x) - 1024, 256)])
        lv.append(float(np.percentile(e, 95) - np.percentile(e, 5)))
    out = {b: float(np.mean(v)) for b, v in acc.items()}
    out["level"] = float(np.mean(lv))
    return out
