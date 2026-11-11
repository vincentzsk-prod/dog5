# SPDX-License-Identifier: GPL-3.0-only
"""Batch 6B2, 28 Bell Tolls round 2: find and remove the top grit, keep the bell underneath.  Probes and the driver (on the 6B kit, b6c_28.py / lib6c.py).
  python3 tests/voicing/b6d_28.py base | alias | iso | cand | wav     -> listen/voicing/batch-06b2/28/*.json (WAVs only on the listen branch)
The grit proxies (a number is a number, Vincent's ear decides): per window after the strike (0-20 / 20-100 / 100-400 ms, 1-2 s) the share of the energy above 4 kHz, the share in 2-8 kHz, the spectral flatness over 2-10 kHz
(geometric over arithmetic mean of the averaged power spectrum, dB: a noise-like floor is near 0, a few clean partials is far below), the count of spectral peaks within -30 dB that are neither on the key's harmonic series (+-0.06 f0) nor on
the bell's tierce (2.4 x the key, +-3 %), the crest factor of the dry output, and the saturation counters of an instrumented host (build/voicing/instr: the voice's mix clamp, the filter's saturating state, the output tanh)."""
import json
import os
import re
import subprocess
import sys

from b6c_28 import *          # V, BELL, SHIM, fit, ring, space, measure, level_of, PHRASES ... (lib6c: K, B, M, N, Q, FS, run, note, solo, partials, decay_times, ladder, shares3, cent, tail_rows)
from b6_common import jdefault, save, cpu

OUT2 = os.path.join(K.ROOT, "listen", "voicing", "batch-06b2", "28")
INSTR = os.path.join(K.BUILD, "instr", "obv_instr")
NOTES = (("A3", 57), ("A4", 69), ("A6", 93))
WINS = ((0, 20), (20, 100), (100, 400), (1000, 2000))
NF = {(0, 20): 512, (20, 100): 2048, (100, 400): 4096, (1000, 2000): 8192}


def avg_spec(x, nfft):
    w = np.hanning(nfft)
    hop = nfft // 4
    P = np.zeros(nfft // 2 + 1)
    n = 0
    for s in range(0, max(len(x) - nfft, 0) + 1, hop):
        if s + nfft > len(x):
            break
        P += np.abs(np.fft.rfft(x[s:s + nfft] * w)) ** 2
        n += 1
    if n == 0:                                   # a window shorter than the frame: zero-pad one frame
        y = np.zeros(nfft); y[:len(x)] = x * np.hanning(len(x))
        P = np.abs(np.fft.rfft(y)) ** 2; n = 1
    return P / n


def nonladder(a, n, t0, t1, floor=-30.0):
    """peaks within `floor` dB of the strongest in [t0, t1] ms that are not on the key's harmonic series (+-0.06 f0) nor the tierce (2.4 f0, +-3 %): count and the list (Hz, dB)"""
    x = a.mean(1)[int(t0 * FS / 1000):int(t1 * FS / 1000)]
    NFt = 1 << 16
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)), NFt))
    f = np.fft.rfftfreq(NFt, 1 / FS)
    keep = (f > 100) & (f < 14000)
    idx = [i for i in range(1, len(X) - 1) if X[i] > X[i - 1] and X[i] >= X[i + 1] and keep[i]]
    mx = X[idx].max()
    cand = sorted(((X[i] / mx, f[i]) for i in idx), reverse=True)
    pk = []
    for v, fr in cand:
        db = 20 * np.log10(v)
        if db < floor:
            break
        if all(abs(fr - g) > 40 for g, _ in pk):
            pk.append((float(fr), float(db)))
    f0 = f_of(n)
    out = []
    for fr, db in pk:
        r = fr / f0
        if abs(r - round(r)) <= 0.06 or abs(r / 2.4 - 1) <= 0.03:
            continue
        out.append((round(fr, 1), round(db, 1)))
    return {"count": len(out), "count20": sum(1 for _, db in out if db >= -20), "list": sorted(out)[:12], "total_peaks": len(pk)}


def grit(a, n, on=3000):
    """the proxies per window for one note render `a` (struck at `on` ms)"""
    x = a.mean(1)
    f_cache = {}
    out = {}
    for w in WINS:
        s0, s1 = int((on + w[0]) * FS / 1000), int((on + w[1]) * FS / 1000)
        nf = NF[w]
        P = avg_spec(x[s0:s1], nf)
        f = np.fft.rfftfreq(nf, 1 / FS)
        tot = P[f > 20].sum()
        sel = (f >= 2000) & (f <= 10000)
        Q_ = P[sel] + 1e-12
        flat = 10 * np.log10(np.exp(np.mean(np.log(Q_))) / np.mean(Q_))
        out[f"{w[0]}-{w[1]}"] = {"over4k": float(100 * P[f >= 4000].sum() / tot), "s2_8k": float(100 * P[(f >= 2000) & (f < 8000)].sum() / tot), "flat": float(flat),
                                 "rms": float(M.rms_db(a, on + w[0], on + w[1]))}
        if w != (0, 20):
            out[f"{w[0]}-{w[1]}"]["nonlad"] = nonladder(a, n, on + w[0], on + w[1])
    return out


def istats(p, lines):
    """run the instrumented host on a probe script; the counters of the voice's mix clamp, the filter's saturating state and the output stage's tanh"""
    sp = os.path.join(K.BUILD, "istat.txt")
    open(sp, "w").write("\n".join(lines) + "\n")
    r = subprocess.run([INSTR, os.path.join(K.BUILD, "istat"), sp], cwd=K.ROOT, capture_output=True, text=True, errors="replace", check=True)
    m = re.search(r"STATS (.*)", r.stderr)
    t = m[1].split()
    d = {t[i]: int(t[i + 1]) for i in range(0, len(t), 2)}
    return d


def sat_row(p, n, hold=3000, tail=500):
    lines = N._probe_script(p, note(3000, 3000 + hold, n), 3000 + hold + tail)
    d = istats(p, lines)
    d["svf_sat_pct"] = 100 * d["svf_sat"] / max(d["svf_n"], 1)
    return d


def crest_dry(exe, p, n):
    a = solo(exe, p, n, hold=3000, tail=500, ov={"DLY_MIX": 0, "REV_MIX": 0})
    return {"strike_0_400": crest(a, 3000, 3400), "note_0_3000": crest(a, 3000, 6000), "peak_dry": float(M.peak_db(a))}


def one(exe, p, tag, full=True):
    """the grit set of one parameter set: the proxies at A3 / A4 / A6, the dry crest, the saturation counters; the bell's ladder / ring / shares / centroid / level at A4 (and A3 ladder)"""
    m = {"volume": p["VOLUME"], "params": p}
    m["grit"], m["crest"], m["sat"], m["ladder"], m["shares"], m["cent"] = {}, {}, {}, {}, {}, {}
    for nm, n in NOTES:
        a = solo(exe, p, n, hold=3000, tail=800)
        m["grit"][nm] = grit(a, n)
        m["crest"][nm] = crest_dry(exe, p, n)
        m["sat"][nm] = sat_row(p, n)
        m["sat"][nm]["strike100"] = sat_row(p, n, hold=100, tail=0)
        m["ladder"][nm] = ladder(a, n + 12, 3000, 3300)["classical"]
        m["shares"][nm] = {"strike_0_400": shares3(a, 3000, 3400), "body_1_2s": shares3(a, 4000, 5000)}
        m["cent"][nm] = {"0-20": cent(a, 3000, 3020, 512), "20-100": cent(a, 3020, 3100, 1024), "100-400": cent(a, 3100, 3400, 2048)}
    d, a = ring(exe, p, 69)
    m["ring"] = d
    m["level"] = level_of(K.render(exe, LEVEL_PH, params=p, tag="lv6d")[0])
    W = {ph: K.render(exe, ph, params=p, tag="mc6d")[0] for ph in PHRASES}
    m["level_chord"] = K.level_metrics(W["at_bell_chord"], "at_bell_chord")["rms"]
    m["peaks"] = {k: M.peak_db(v) for k, v in W.items()}
    m["peak_all"] = max(m["peaks"].values())
    m["clip"] = int(sum((np.abs(v) >= 32767).sum() for v in W.values()))
    m["sat_phr"] = {}
    for ph in ("ar_bell_toll", "at_bell_chord"):
        d_ = istats(p, K.compose(ph, None, p).splitlines())
        d_["svf_sat_pct"] = 100 * d_["svf_sat"] / max(d_["svf_n"], 1)
        m["sat_phr"][ph] = d_
    if full:
        m["space"] = space(exe, p)
    return m


def log_row(tag, m):
    g = m["grit"]["A4"]
    print(f"{tag:10s} VOL {m['volume']:3d} toll {m['level']:6.2f} chord {m['level_chord']:6.2f} pk {m['peak_all']:6.2f} | A4 >4k 0-20/20-100/100-400/1-2s " +
          "/".join(f"{g[k]['over4k']:.2f}" for k in ("0-20", "20-100", "100-400", "1000-2000")) + " flat100-400 %.1f nonlad %d crest %.1f svf%% %.2f" %
          (g["100-400"]["flat"], g["100-400"]["nonlad"]["count"], m["crest"]["A4"]["strike_0_400"], m["sat"]["A4"]["svf_sat_pct"]), flush=True)


# ---- the isolation set, all on C (the committed round-1 variant) -------------------------------------------------------------
ISO = {
    "xmod0": ("X-MOD 64 -> 0 (no FM)", {"XMOD": 0}),
    "xmod32": ("X-MOD 64 -> 32", {"XMOD": 32}),
    "o2_35": ("OSC 2 LEVEL 70 -> 35", {"O2_LVL": 35}),
    "o2_off": ("OSC 2 off (LEVEL 0)", {"O2_LVL": 0}),
    "o1only": ("OSC 1 alone (OSC 2 LEVEL 0, X-MOD 0)", {"O2_LVL": 0, "XMOD": 0}),
    "cut72": ("CUTOFF 88 -> 72", {"CUTOFF": 72}),
    "envamt64": ("ENV AMT 88 -> 64", {"FENV_AMT": 64}),
    "fd75": ("FILTER DECAY 90 -> 75", {"FD": 75}),
    "vint0": ("VINTAGE 20 -> 0", {"VINTAGE": 0}),
    "spread0": ("SPREAD 70 -> 0", {"SPREAD": 0}),
    "noshim": ("no LFO shimmer (the C extras off)", {"LFO_PITCH": 0, "LFO_AMP": 0, "LFO_DELAY": 0}),
    "dry": ("echo and spring off (MIX 0)", {"DLY_MIX": 0, "REV_MIX": 0}),
    "c2cut84": ("C2 (X-MOD 32) with CUTOFF 88 -> 84: the second axis, the strike's top trimmed", {"XMOD": 32, "CUTOFF": 84}),
    "head": ("mixer headroom: OSC 1 LEVEL 127 -> 64, OSC 2 70 -> 35 (VOLUME re-fitted)", {"O1_LVL": 64, "O2_LVL": 35}),
}


def refit(exe, p):
    return fit(exe, p)


def main():
    argv = sys.argv[1:]
    mode = argv[0] if argv else "base"
    exe = K.build_host()
    cg = K.callgrind_exe()
    os.makedirs(OUT2, exist_ok=True)
    orig = B.resolve(BASE, 28)
    if mode == "base":
        R = {}
        for key, (tag, desc, ch) in [("A", ("original", "", {}))] + list(V.items()):
            p = dict(orig) if key == "A" else {**orig, **ch}
            p = fit(exe, p)
            R[key] = one(exe, p, key)
            R[key]["cost"] = cpu(cg, p, "b6d" + key)
            log_row(key, R[key])
        save(OUT2, "base.json", R)
    elif mode == "iso":
        only = argv[1].split(",") if len(argv) > 1 else None
        R = json.load(open(os.path.join(OUT2, "iso.json"))) if only else {}
        pc = {**orig, **V["C"][2]}
        pc = fit(exe, pc)
        if not only:
            R["C"] = one(exe, pc, "C", full=False)
            R["C"]["cost"] = cpu(cg, pc, "b6dC")
            log_row("C", R["C"])
        for key, (desc, ch) in ISO.items():
            if only and key not in only:
                continue
            p = {**pc, **ch}
            p = fit(exe, p)
            R[key] = one(exe, p, key, full=False)
            R[key]["desc"], R[key]["change"] = desc, ch
            R[key]["cost"] = cpu(cg, p, "b6d" + key)
            log_row(key, R[key])
        save(OUT2, "iso.json", R)




def alias(exe):
    """OSC 1 alone (a saw), the filter open (LP24 CUTOFF 127, no envelope amount, KEY TRK 64), sustained, VINTAGE 0, the sends off: the long-term spectrum 1-2.5 s; the energy that is not on the harmonic series k f0 (+-6 Hz), in dB re the whole,
    and re the energy above 4 kHz; the strongest non-harmonic peaks (Hz, dB re the fundamental) and the reflection test (a peak at fs - k f0 is an alias of the k-th harmonic)"""
    q = {**BELL, "O1_LVL": 100, "O2_LVL": 0, "XMOD": 0, "FTYPE": 4, "CUTOFF": 127, "RESO": 0, "FENV_AMT": 64, "KEYTRK": 64, "VINTAGE": 0, "SPREAD": 0, "FA": 0, "FD": 127, "FS": 127, "AA": 0, "AD": 127, "AS": 127, "AR": 40, "DLY_MIX": 0, "REV_MIX": 0,
         "LFO_PITCH": 0, "LFO_AMP": 0, "LFO_DELAY": 0, "VOLUME": 60, "MODE": 0, "POLY_N": 1, "O1_WAVE": 1}
    out = {}
    for nm, n in (("A2", 45), ("A3", 57), ("A4", 69), ("A5", 81), ("A6", 93), ("A7", 105)):
        a = run(exe, q, note(3000, 5600, n), 5900)
        x = a.mean(1)[int(4000 * FS / 1000):int(5500 * FS / 1000)]
        NFt = 1 << 19
        X = np.abs(np.fft.rfft(x * np.hanning(len(x)), NFt)) ** 2
        f = np.fft.rfftfreq(NFt, 1 / FS)
        f0e = f_of(n)
        sel = (f > f0e * 0.97) & (f < f0e * 1.03)
        f0 = f[sel][int(np.argmax(X[sel]))]
        harm = np.zeros(len(f), bool)
        k = 1
        while k * f0 < FS / 2:
            harm |= np.abs(f - k * f0) < 6.0
            k += 1
        tot = X[f > 20].sum()
        hi = X[f > 4000].sum()
        nh = X[(~harm) & (f > 20)].sum()
        nh_hi = X[(~harm) & (f > 4000)].sum()
        # the strongest non-harmonic peaks
        Xn = np.where(harm | (f < 20), 0, X)
        idx = [i for i in range(1, len(Xn) - 1) if Xn[i] > Xn[i - 1] and Xn[i] >= Xn[i + 1]]
        idx = sorted(idx, key=lambda i: -Xn[i])[:6]
        fund = X[sel].max()
        pk = []
        for i in idx:
            fr = f[i]
            # which harmonic k reflects to this frequency: fs - k f0 = fr (or 2 fs ...)
            kk = round((FS - fr) / f0)
            refl = abs((FS - kk * f0) - fr) < 12 if kk >= 1 else False
            pk.append((round(float(fr), 1), round(float(10 * np.log10(Xn[i] / fund)), 1), int(kk) if refl else None))
        out[nm] = {"f0": float(f0), "nonharm_total_db": float(10 * np.log10(nh / tot + 1e-30)), "nonharm_of_over4k_db": float(10 * np.log10(nh_hi / max(hi, 1e-30) + 1e-30)), "over4k_pct": float(100 * hi / tot), "peaks": pk}
    return out


GRIT_FIX = {"XMOD": 32}          # the single best top-grit reduction (step 2): X-MOD 64 -> 32


def cand(exe, cg, orig):
    R = {}
    for key in ("A", "B2", "C2", "D2"):
        if key == "A":
            p = fit(exe, dict(orig))
        else:
            p = fit(exe, {**orig, **V[key[0]][2], **GRIT_FIX})
        m = one(exe, p, key)
        m["cost"] = cpu(cg, p, "b6d" + key)
        mm, _ = measure(exe, cg, p, key, True)
        m["b6c"] = {k: v for k, v in mm.items() if k not in ("params",)}
        log_row(key, m)
        R[key] = m
    pc = R["C2"]["params"]
    R["live"] = live_table(exe, pc)
    R["addons"] = {"base": cpu(cg, pc, "ab")["total"], "CHEW 45": cpu(cg, {**pc, "CHEW": 45}, "ac")["total"], "GROWL 44": cpu(cg, {**pc, "GROWL": 44}, "ag")["total"],
                   "CHEW 45 + GROWL 44": cpu(cg, {**pc, "CHEW": 45, "GROWL": 44}, "acg")["total"]}
    save(OUT2, "cand.json", R)
    return R


CALS = (("cal1xmod0", "xmod0"), ("cal2o1only", "o1only"), ("cal3o2half", "o2_35"), ("cal4cut72", "cut72"), ("cal5fd75", "fd75"), ("cal6c2cut84", "c2cut84"))


def wavs(exe):
    """the listening WAVs (listen branch only): A, B2, C2, D2 on every phrase (the register for C2 only), the round-1 B / C / D (as B1 / C1 / D1) on the toll, the held notes and A6, the six calibrations on the same three"""
    base = json.load(open(os.path.join(OUT2, "base.json")))
    cd = json.load(open(os.path.join(OUT2, "cand.json")))
    iso = json.load(open(os.path.join(OUT2, "iso.json")))
    cut = int(K.T_CUT * FS)

    def w(name, a):
        K.write_wav(os.path.join(OUT2, f"28_{name}.wav"), a[cut:])

    def phr(key, p, names):
        for ph, sh in WAVMAP:
            if sh in names:
                w(f"{key}_{sh}", K.render(exe, ph, params=p, tag="wv6d")[0])

    def single(key, p, n, nm):
        w(f"{key}_{nm}", run(exe, p, note(3000, 6000, n), 9500))

    for k in ("A", "B2", "C2", "D2"):
        p = cd[k]["params"]
        phr(k, p, ("toll", "held", "chord", "run") + (("register",) if k == "C2" else ()))
        single(k, p, 81, "a5"); single(k, p, 93, "a6")
    for k in "BCD":
        p = base[k]["params"]
        phr(k + "1", p, ("toll", "held")); single(k + "1", p, 93, "a6")
    for key, ik in CALS:
        p = iso[ik]["params"]
        phr(key, p, ("toll", "held")); single(key, p, 93, "a6")


if __name__ == "__main__":
    a_ = sys.argv[1:]
    if a_ and a_[0] == "wav":
        wavs(K.build_host())
    elif a_ and a_[0] == "cand":
        e_ = K.build_host(); cg_ = K.callgrind_exe()
        os.makedirs(OUT2, exist_ok=True)
        cand(e_, cg_, B.resolve(BASE, 28))
    else:
        main()
