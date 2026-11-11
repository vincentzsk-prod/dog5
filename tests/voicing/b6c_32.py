# SPDX-License-Identifier: GPL-3.0-only
"""Batch 6B, 32 Init bruv?: the raw blank slate that closes the bank.  A = the original array (= the engine defaults, VOLUME 100), B = the defaults with VOLUME on the reference (POLY 5), C = the same in MONO; one calibration (Craw) = the plain
single saw of the brief's words.   python3 tests/voicing/b6c_32.py [--no-cost] [--no-wav]   -> listen/voicing/batch-06b/32/ (results.json; WAVs only on the listen branch)"""
import json
import sys

from lib6c import *
from b6_common import jdefault, save, cpu

OUT = os.path.join(K.ROOT, "listen", "voicing", "batch-06b", "32")
BASE = os.path.join(K.BUILD, "base")
REF = -18.0
LEVEL_PH = "b_stabs"
PHRASES = ["b_stabs", "a_riff", "c_held", "w_chord_mid"]
WAVMAP = (("c_held", "held"), ("a_riff", "riff"), ("w_chord_mid", "chord"))
V = {
    "B": ("defaults-poly", "the engine's own defaults, POLY 5 (the default mode), VOLUME on the reference", {}),
    "C": ("defaults-mono", "the same in MONO", dict(MODE=3)),
}
CAL = {
    "Craw": ("plain-saw", "calibration: the brief's WORDS: one raw saw (OSC 2 off), the filter fully open (CUTOFF 127, RESO 0, no envelope amount), flat envelopes (attack 0, sustain full, release 30), POLY 5", dict(O2_LVL=0, CUTOFF=127, RESO=0, FENV_AMT=64, AA=0, AS=127, AR=30)),
}


def level_of(a):
    return K.level_metrics(a, LEVEL_PH)["rms"]


def fit(exe, p):
    v = p.get("VOLUME", 100); best = None
    for _ in range(10):
        a, _ = K.render(exe, LEVEL_PH, params={**p, "VOLUME": v}, tag="trim6d")
        r = level_of(a)
        if best is None or abs(r - REF) < abs(best[1] - REF):
            best = (v, r)
        if abs(r - REF) < 0.12:
            break
        v = max(1, min(127, int(round(v * 10 ** ((REF - r) / 40))) or v + 1))
        if v == best[0]:
            v += 1 if REF > r else -1
    p = {**p, "VOLUME": best[0]}
    while max(M.peak_db(K.render(exe, ph, params=p, tag="pk6d")[0]) for ph in PHRASES) > -4.0 and p["VOLUME"] > 1:
        p["VOLUME"] -= 1
    return p


def harmonics(exe, p, n, nh=10):
    """the first nh harmonic amplitudes of one held note (a Hann window over 0.4-1.4 s, 1/12-octave tolerance around each multiple): dB re the first, and the deviation from the saw's 1/n law (dB): a plain saw reads 0 everywhere"""
    a = solo(exe, p, n, hold=1800, tail=200)
    x = a.mean(1)[int(3400 * FS / 1000):int(4400 * FS / 1000)]
    NF = 1 << 17
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)), NF))
    f = np.fft.rfftfreq(NF, 1 / FS)
    f0 = f_of(n)
    pk = []
    for h in range(1, nh + 1):
        s = (f > h * f0 * 0.985) & (f < h * f0 * 1.015)
        pk.append(float(X[s].max()))
    db = [20 * np.log10(v / pk[0]) for v in pk]
    return {"db": db, "dev": [db[i] - 20 * np.log10(1 / (i + 1)) for i in range(nh)]}


def measure(exe, cg, p, key, no_cost):
    m = {}
    W = {ph: K.render(exe, ph, params=p, tag="mc6d")[0] for ph in PHRASES}
    m["level"] = level_of(W[LEVEL_PH])
    m["level_riff"] = K.level_metrics(W["a_riff"], "a_riff")["rms"]
    m["level_chord"] = K.level_metrics(W["w_chord_mid"], "w_chord_mid")["rms"] if False else float(M.rms_db(W["w_chord_mid"], 3000, 11000))
    m["krms"] = K.level_metrics(W[LEVEL_PH], LEVEL_PH)["rms_k"]
    m["peaks"] = {k: M.peak_db(v) for k, v in W.items()}
    m["peak_all"] = max(m["peaks"].values())
    m["clip"] = int(sum((np.abs(v) >= 32767).sum() for v in W.values()))
    m["cost"] = None if (no_cost or cg is None) else cpu(cg, p, "n" + key)
    m["harm"] = {"C3": harmonics(exe, p, 48), "C5": harmonics(exe, p, 72)}
    # the note-on: the peak of the first 2 ms after the note-on against the note's own peak (a click shows as a large first-2-ms peak)
    a = solo(exe, p, 48, hold=1500, tail=300)
    x = np.abs(a).max(1)
    i0 = int(np.nonzero(x > 8)[0][0])
    m["onset"] = {"first2ms_peak": float(20 * np.log10(max(x[i0:i0 + 88].max(), 1) / 32767)), "note_peak": float(20 * np.log10(x.max() / 32767)),
                  "first_nonzero_ms": float(i0 / FS * 1000 - 3000)}
    a = solo(exe, p, 48, hold=1500, tail=300)
    m["cent"] = {"C3": M.centroid(a, 3100, 4000, nfft=4096), "C5": M.centroid(solo(exe, p, 72, hold=1500, tail=300), 3100, 4000, nfft=4096)}
    return m, W


def bypass_proof(exe, p):
    """the effect chain at 0 is bit-exact bypassed: the patch with every effect's OTHER controls moved to extremes (echo time / feedback / tone / spread, spring size / damp / pre-delay, tape wow / hiss / drops, GROWL bias / tone) must render the same samples as the patch as it is, on three phrases"""
    q = {**p, "DLY_FB": 120, "DLY_TONE": 127, "ALLEY": 90, "ALLEY_FINE": 100, "BBD_SPREAD": 0, "DLY_TIME": 6, "REV_SIZE": 127, "REV_DAMP": 0, "REV_PRE": 120, "TP_WOWFLT": 0, "TP_HISS": 127, "TP_DROPS": 127, "GRL_BIAS": 127, "GRL_TONE": 127}
    out = {}
    for ph in ("b_stabs", "a_riff", "c_held"):
        x = K.render(exe, ph, params=p, tag="bp1")[0]
        y = K.render(exe, ph, params=q, tag="bp2")[0]
        out[ph] = bool((x == y).all())
    return out


def wav_only(exe):
    R = json.load(open(os.path.join(OUT, "results.json")))
    for key, m in R.items():
        if "params" not in m:
            continue
        for ph, sh in WAVMAP:
            if key == "A" and ph != "a_riff":
                continue
            K.write_wav(os.path.join(OUT, f"32_{key}_{sh}.wav"), K.render(exe, ph, params=m["params"], tag="wv6d")[0][int(K.T_CUT * FS):])


def main():
    argv = sys.argv[1:]
    if "--wav-only" in argv:
        wav_only(K.build_host()); return
    no_cost, no_wav = "--no-cost" in argv, "--no-wav" in argv
    exe = K.build_host()
    cg = None if no_cost else K.callgrind_exe()
    orig = B.resolve(BASE, 32)
    R = {}
    allv = [("A", "original", "the original array (the engine defaults), VOLUME 100", {})] + [(k, v[0], v[1], v[2]) for k, v in V.items()] + [(k, v[0], v[1], v[2]) for k, v in CAL.items()]
    for key, tag, desc, ch in allv:
        p = {**orig, **ch}
        if key != "A":
            p = fit(exe, p)
        m, W = measure(exe, cg, p, key, no_cost)
        m["volume"], m["params"], m["tag"], m["desc"] = p["VOLUME"], p, tag, desc
        R[key] = m
        c = m["cost"]
        print(f"32{key} {tag:14s} VOL {p['VOLUME']:3d} stabs {m['level']:6.2f} riff {m['level_riff']:6.2f} pk {m['peak_all']:6.2f}" + (f" cost {c['total']:.0f}" if c else "") + f" | onset first-2ms {m['onset']['first2ms_peak']:.1f} dB, note peak {m['onset']['note_peak']:.1f}", flush=True)
        if not no_wav:
            for ph, sh in WAVMAP:
                if key == "A" and ph != "a_riff":
                    continue
                K.write_wav(os.path.join(OUT, f"32_{key}_{sh}.wav"), W[ph][int(K.T_CUT * FS):] if ph in W else K.render(exe, ph, params=p, tag="wv")[0][int(K.T_CUT * FS):])
    R["bypass"] = bypass_proof(exe, R["B"]["params"])
    R["defaults_vs_original"] = {k: [orig[k], v] for k, v in B.resolve(os.path.join(K.ROOT), 32).items() if k in orig and orig[k] != v}
    save(OUT, "results.json", R)
    if cg is not None:      # the whole bank's cost on the same yardstick: is slot 32 the lightest?
        bank = {}
        for slot in range(1, 33):
            cb, cl = K.cost(cg, program=slot - 1, tag="bk")
            ir, fr = K.callgrind_ips(cg, "x_stress", program=slot - 1, tag="bki", notes=False)
            bank[str(slot)] = ir / fr + cl
        R["bank_cost"] = bank
        save(OUT, "results.json", R)


if __name__ == "__main__":
    main()
