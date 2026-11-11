# SPDX-License-Identifier: GPL-3.0-only
"""Batch 6A, 27 R3V3RT: a tight MONO single-pulse bass, decay-only filter envelope, a healthy amp sustain with a very short release.
  python3 tests/voicing/b6_27.py [--no-cost] [--no-wav]      -> listen/voicing/batch-06a/27-r3v3rt/ (results.json; WAVs only on the listen branch)"""
import re
import sys

from b6_common import *

SPEC = dict(slot=27, dir="27-r3v3rt", name="R3V3RT", cname="R3V3RT", level="a_riff",
            phrases=["a_riff", "b_stabs", "ag_bass_long", "ah_bass_legato", "ai_a2_held"])
# the shared single-pulse base (changes over the original): OSC 1 a pulse alone (OSC 2 off; the original's saw + sub-octave pulse go), RESO 0, a decay-only filter envelope
# (attack 0, sustain 0, fast release), amp attack 0, a 5 ms release (the original's AR 30); filter DRIVE 30 for warmth
BASE = dict(O1_WAVE=2, O1_PW=54, O1_LVL=120, O2_WAVE=0, O2_LVL=0, RESO=0, FA=0, FD=60, FS=0, FR=20, AA=0, AD=80, AR=30, CUTOFF=66, FENV_AMT=118, DRIVE=30, KEYTRK=30)
V = {
    "B": ("sus70", "the base, AMP SUSTAIN 70", dict(**BASE, AS=70)),
    "C": ("sus90", "the base, AMP SUSTAIN 90", dict(**BASE, AS=90)),
    "D": ("sus110", "the base, AMP SUSTAIN 110", dict(**BASE, AS=110)),
}
CAL = {      # calibration renders for the other axes (AMP SUSTAIN 90 as C), NOT candidates
    "Ebite": ("bite", "calibration: C with a narrower pulse (PW 38 = 30 %), CUTOFF 74, FILTER DECAY 70", {**BASE, "AS": 90, "O1_PW": 38, "CUTOFF": 74, "FD": 70}),
    "Fround": ("round", "calibration: C with a square pulse (PW 64 = 50 %), CUTOFF 58, FILTER DECAY 50", {**BASE, "AS": 90, "O1_PW": 64, "CUTOFF": 58, "FD": 50}),
    "Glong": ("longdecay", "calibration: C with a longer filter decay (FD 85)", {**BASE, "AS": 90, "FD": 85}),
}
BANDS5 = ("<60", "60-150", "150-400", "400-1.2k", "1.2k+")


def ons_of(phrase):
    return [(int(m[1]), int(m[2])) for l in K.phrase_text(phrase).splitlines() for m in [re.match(r"(\d+) midi 0x90 (\d+)", l)] if m]


def cent_traj(a, t0, frames=30, hop=10):
    """centroid every hop ms from t0 (512-point frames, 11.6 ms)"""
    return [M.centroid(a, t0 + i * hop, t0 + i * hop + 12, nfft=512) for i in range(frames)]


def note_probe(exe, p, n, hold=1000, tail=900):
    """one note from silence, dry; returns the render, the on / off times"""
    p = {**p, **DRY}
    a = run(exe, p, note(3000, 3000 + hold, n, 100), 3000 + hold + tail)
    return a


def meas_note(exe, p, n):
    """one note n (A2 = 45, A1 = 33) held 1 s, FX off: level re the peak at 100 / 300 / 600 ms, run-off after the key-up, centroid windows, snap duration, bands"""
    hold = 1000
    a = note_probe(exe, p, n, hold)
    f0 = 440 * 2 ** ((n - 69) / 12)
    e, t = env_ms(a, 1.0, 1000 / f0)
    pk = float(e[3000:3060].max())
    out = {"f0": f0, "peak_db": pk}
    out["lvl"] = {f"{ms}": float(e[3000 + ms] - pk) for ms in (20, 50, 100, 300, 600)}
    rel = K.release_metrics(a, 3000 + hold, hop_ms=1.0, pre_ms=100, win_ms=700)
    out["off"] = {k: rel[k] for k in ("first20", "first40", "first60", "pre_db")}
    out["cent"] = {"0-20": M.centroid(a, 3000, 3020, nfft=512), "20-100": M.centroid(a, 3020, 3100, nfft=1024), "100-300": M.centroid(a, 3100, 3300, nfft=1024)}
    tr = cent_traj(a, 3000, 40, 5)
    body = M.centroid(a, 3150, 3400, nfft=1024)
    out["body_cent"] = body
    hit = [i for i, c in enumerate(tr) if c <= 1.25 * body]
    out["snap_ms"] = hit[0] * 5 if hit else None
    out["snap_peak_cent"] = float(max(tr))
    out["bands"] = {"0-400": M.band_shares(a, 3000, 3400, nfft=2048), "100-400": M.band_shares(a, 3100, 3400, nfft=2048)}
    # share above the fundamental's octave etc: energy above 100 Hz (what a small speaker reproduces)
    x = a.mean(1)[int(3.05 * FS):int(3.4 * FS)]
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
    fr = np.fft.rfftfreq(len(x), 1 / FS)
    out["above100"] = float(100 * X[fr >= 100].sum() / X.sum())
    out["above60"] = float(100 * X[fr >= 60].sum() / X.sum())
    return out


def legato(exe, p):
    """notes 2-8 of the legato riff against the same notes detached (dry): the 0-100 ms level re the detached note, the first-20 ms centroid, the 100-300 ms level"""
    res = {}
    for ph in ("ag_bass_long", "ah_bass_legato"):
        a, _ = K.render(exe, ph, params={**p, **DRY}, tag="lg6")
        ons = [t for t, n in ons_of(ph)][1:8]
        res[ph] = {"first20_rms": [M.rms_db(a, t, t + 20) for t in ons], "p0_100": [M.rms_db(a, t, t + 100) for t in ons], "p100_300": [M.rms_db(a, t + 100, t + 300) for t in ons],
                   "cent0_20": [M.centroid(a, t, t + 20, nfft=512) for t in ons], "cent20_100": [M.centroid(a, t + 20, t + 100, nfft=1024) for t in ons]}
    d, l = res["ag_bass_long"], res["ah_bass_legato"]
    return {"d_p0_100": float(np.mean(d["p0_100"])), "l_p0_100": float(np.mean(l["p0_100"])), "d_p100_300": float(np.mean(d["p100_300"])), "l_p100_300": float(np.mean(l["p100_300"])),
            "d_c20": float(np.mean(d["cent0_20"])), "l_c20": float(np.mean(l["cent0_20"])), "d_c100": float(np.mean(d["cent20_100"])), "l_c100": float(np.mean(l["cent20_100"])),
            "d_first20": float(np.mean(d["first20_rms"])), "l_first20": float(np.mean(l["first20_rms"]))}


def measure(exe, p):
    return {"a2": meas_note(exe, p, 45), "a1": meas_note(exe, p, 33), "legato": legato(exe, p)}


def main():
    no_cost, no_wav = "--no-cost" in sys.argv, "--no-wav" in sys.argv
    exe = K.build_host()
    cg = None if no_cost else K.callgrind_exe()
    orig = B.resolve(BASE_TREE, 27) if False else B.resolve(os.path.join(K.BUILD, "base"), 27)
    d = os.path.join(OUT, SPEC["dir"])
    R, WS = {}, {}
    allv = [("A", "original", "the original through the base program path", {})] + [(k, v[0], v[1], v[2]) for k, v in V.items()] + [(k, v[0], v[1], v[2]) for k, v in CAL.items()]
    for key, tag, desc, ch in allv:
        p = dict(orig) if key == "A" else {**orig, **ch}
        if key != "A":
            p = fit(exe, SPEC, p)
        m, W = common(exe, cg, SPEC, key, p, no_cost)
        m.update(measure(exe, p))
        m["volume"], m["params"], m["tag"], m["desc"] = p["VOLUME"], p, tag, desc
        R[key], WS[key] = m, W
        c = m["cost"]
        print(f"27{key} {tag:8s} VOL {p['VOLUME']:3d} lvl {m['level']:6.2f} b {m['b']:6.2f} pk {m['peak_all']:6.2f}" + (f" cost {c['total']:.0f}" if c else ""), flush=True)
    pa = fit(exe, SPEC, dict(orig)); ra = trim(exe, SPEC, dict(orig))[1]
    R["A*"] = {"volume": pa["VOLUME"], "level": ra, "params": pa, "tag": "original-matched", "desc": "the original's tone with VOLUME alone moved onto the reference (a listening aid)"}
    # probes on C (AMP SUSTAIN 90): one control stepped at a time; A2 body centroid / snap peak centroid, A1 share of the body's energy above 60 Hz, the cost where asked
    pc = R["C"]["params"]
    pr = []
    for nm, vals in (("DRIVE", (0, 30, 60, 100)), ("O1_PW", (38, 46, 54, 64)), ("KEYTRK", (0, 30, 64, 100)), ("CUTOFF", (58, 66, 74)), ("FD", (40, 60, 85))):
        for v in vals:
            q = {**pc, nm: v}
            a2, a1 = meas_note(exe, q, 45), meas_note(exe, q, 33)
            pr.append({"param": nm, "value": v, "a2_body": a2["body_cent"], "a2_snap_peak": a2["snap_peak_cent"], "a2_snap_ms": a2["snap_ms"], "a1_above60": a1["above60"], "a1_body": a1["body_cent"],
                       "cost": cpu(cg, {**q, **DRY}, "P") if (cg and nm == "DRIVE") else None})
    R["probes"] = pr
    if not no_wav:
        for key in [k for k in R if k in ("A*", "B", "C", "D") or k in CAL]:
            pp = R[key]["params"]
            for ph, sh in (("a_riff", "riff-chopped"), ("ag_bass_long", "line-long"), ("ah_bass_legato", "line-legato"), ("ai_a2_held", "held-A2")):
                if key in CAL and ph == "a_riff":
                    continue              # (the calibrations: no chopped riff, to keep the listen branch light)
                wav(d, SPEC, key.replace("*", "star"), ph, K.render(exe, ph, params=pp, tag="wv6")[0], sh)
    save(d, "results.json", R)


if __name__ == "__main__":
    main()
