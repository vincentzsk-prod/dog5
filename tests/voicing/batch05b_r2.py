#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Batch 5B round 2: 23 Crypt Dust with (almost) no noise.  C2 / C3 from round 1's C (half tape), D2 / D3 from D (tapeless).

  python3 tests/voicing/batch05b_r2.py [--no-cost] [--no-wav] [--cpu]      variants -> listen/voicing/batch-05b/23-crypt-dust/round2/
  python3 tests/voicing/batch05b_r2.py --emit KEY                          the C array

Trace = NOISE set so that the noise component sits TRACE_DB under the pulse component of the whole chain in the settled held chord (+4 .. +10 s of phrase z_chord): the noise-only render
(OSC 1 LEVEL 0) against the pulse-only render (NOISE 0), same chain, same VOLUME.  Tape HISS is 0 (off) in C2 / C3."""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib5b import *
import batch05b as X
from batch05b import win_tab, dips, partial_track, trk_stats
import batch04a as A

TRACE_DB = -25.0
OUT = os.path.join(X.OUT, "23-crypt-dust", "round2")
R1 = json.load(open(os.path.join(X.OUT, "23-crypt-dust", "results.json")))
SPEC = X.SPECS[23]; SPEC["slot"] = 23
WIN = (7000, 13000)


def comp(exe, p):
    """RMS (dBFS, +4..+10 s of the held triad) of the whole patch, of its noise alone (OSC 1 LEVEL 0) and of its pulse alone (NOISE 0)"""
    f = lambda q: M.rms_db(K.render(exe, "z_chord", params=q, tag="r2c")[0], *WIN)
    return f(p), f({**p, "O1_LVL": 0}), f({**p, "NOISE": 0})


def find_trace(exe, p):
    """the NOISE knob (square law) whose noise-only RMS is TRACE_DB under the pulse-only RMS; returns (knob, achieved dB)"""
    best = None
    for v in range(1, 128):
        _, n, pu = comp(exe, {**p, "NOISE": v}) if False else (None, M.rms_db(K.render(exe, "z_chord", params={**p, "NOISE": v, "O1_LVL": 0}, tag="r2n")[0], *WIN), None)
        if pu is None:
            pu = M.rms_db(K.render(exe, "z_chord", params={**p, "NOISE": 0}, tag="r2p")[0], *WIN)
        d = n - pu
        if best is None or abs(d - TRACE_DB) < abs(best[1] - TRACE_DB):
            best = (v, d)
        if d > TRACE_DB + 3:
            break
    return best


def which_notes(exe, p):
    """which keys of the triad sound: pulse only, fundamentals exposed (LP12 wide open, no FX, VINTAGE 0), energy at 220 / 277.2 / 329.6 Hz in 4..10 s (dB re the strongest)"""
    q = {**p, "NOISE": 0, "FTYPE": 0, "CUTOFF": 127, "KEYTRK": 0, "GROWL": 0, "DLY_MIX": 0, "REV_MIX": 0, "CHEW": 0, "VINTAGE": 0, "LFO_AMP": 0, "LFO_FLT": 0, "O1_PW": 64}
    a = K.render(exe, "z_chord", params=q, tag="r2w")[0].mean(1)[int(7 * FS):int(13 * FS)]
    X_ = np.abs(np.fft.rfft(a * np.hanning(len(a)), 1 << 19)); fr = np.fft.rfftfreq(1 << 19, 1 / FS)
    e = {n: X_[(fr > f * 0.99) & (fr < f * 1.01)].max() for n, f in (("A3", 220.0), ("C#4", 277.18), ("E4", 329.63))}
    m = max(e.values())
    return {n: 20 * np.log10(v / m) for n, v in e.items()}


def measure(exe, cg, key, p, no_cost, cpu_poly=False):
    m = {}
    W = {ph: K.render(exe, ph, params=p, tag="r2m")[0] for ph in ("z_chord", "z_tap", "a_riff", "b_stabs")}
    a = W["z_chord"]
    m["level"] = M.rms_db(a, *WIN); m["krms"] = X.R1.krms(a, *WIN)
    m["peaks"] = {k: M.peak_db(v) for k, v in W.items()}; m["peak_all"] = max(m["peaks"].values()); m["clip"] = int(sum((np.abs(v) >= 32767).sum() for v in W.values()))
    m["b"] = K.level_metrics(W["b_stabs"], "b_stabs")["rms"]
    tot, n, pu = comp(exe, p)
    m["comp"] = {"noise": n, "pulse": pu, "diff": n - pu, "whole": tot}
    if p["CHEW"]:
        h = comp(exe, {**p, "TP_HISS": 64}); m["comp_hiss64"] = {"noise": h[1], "pulse": h[2], "diff": h[1] - h[2]}
    m["windows"] = win_tab(a, 3000, tail_from=13000)
    m["pcm_notes"] = which_notes(exe, p)
    # the pulse's pitch wander on the real patch: one held A3, the strongest harmonic of the CHEW 0 render tracked (+-100 Hz)
    p0 = {**p, "CHEW": 0}
    one = lambda q: run(exe, q, note(3000, 11000, 57), 14000, tag="r2o")
    a0 = one(p0); a1 = one(p)
    Xs = np.abs(np.fft.rfft(a0.mean(1)[int(5 * FS):int(10 * FS)] * np.hanning(int(5 * FS)))); fq = np.fft.rfftfreq(int(5 * FS), 1 / FS)
    hs = {h: Xs[(fq > 220 * h - 60) & (fq < 220 * h + 60)].max() for h in range(5, 25)}; hb = max(hs, key=hs.get)
    t = {}
    for nm, aa in (("as", a1), ("chew0", a0)):
        c = partial_track(aa, 220.0 * hb, 100, 4000, 11000)
        t[nm] = trk_stats(c, hop_ms=25) if np.isfinite(c).all() else {"sd": None, "p5": None, "p95": None, "rate": None}
        t[nm]["dips"] = dips(aa, 4000, 11000)
    m["wobble"] = {"harmonic": hb, "hz": 220.0 * hb, **t}
    m["dips_chord"] = dips(a, *WIN)
    m["floor"] = {w: M.rms_db(a, 3000 + w * 1000, 3000 + (w + 1) * 1000) for w in (14, 15)}
    m["hf"] = M.band_shares(a, *WIN)["1.2k+"]; m["cent"] = M.centroid(a, *WIN, nfft=2048)
    m["level_sd"] = dips(a, *WIN)["level_sd"]
    m["tap"] = {"gate": M.rms_db(W["z_tap"], 3000, 3150), "re_held": M.rms_db(W["z_tap"], 3000, 3150) - m["level"], "a4_gate": M.rms_db(W["z_tap"], 8000, 8150), "hover": M.tail_times(W["z_tap"], 3150, 150, 4500)}
    m["hover"] = M.tail_times(a, 13000, 150, 5800)
    m["cost"] = None
    if cg and not no_cost:
        b, l = K.cost(cg, params=p, tag="r2c" + key); ir, fr = K.callgrind_ips(cg, "x_stress", params=p, tag="r2i" + key, notes=False)
        m["cost"] = {"b": b, "load": l, "idle": ir / fr}
    return m, W


def variants(exe):
    C, D = dict(R1["C"]["params"]), dict(R1["D"]["params"])
    V = {"C2": {**C, "TP_HISS": 0}, "C3": {**C, "NOISE": 0, "TP_HISS": 0}, "D2": dict(D), "D3": {**D, "POLY_N": 4}}
    out = {}
    for k, p in V.items():
        if k in ("C2", "D2"):
            p["VOLUME"] = 100
            v, d = find_trace(exe, p); p["NOISE"] = v
            print(k, "trace NOISE", v, "diff %.2f" % d, flush=True)
        out[k] = p
    out["D3"]["NOISE"] = out["D2"]["NOISE"]
    return out


def trim_final(exe, p):
    v, _ = X.trim(exe, SPEC, p); p["VOLUME"] = v
    while max(X.peaks(exe, SPEC, p).values()) > -4.0 and p["VOLUME"] > 1:
        p["VOLUME"] -= 1
    return p


def main():
    argv = sys.argv[1:]
    os.makedirs(OUT, exist_ok=True)
    if "--emit" in argv:
        from batch01a import emit
        print(emit("CRYPT_DUST", json.load(open(os.path.join(OUT, "results.json")))[argv[argv.index("--emit") + 1]]["params"])); return
    exe = K.build_host(); cg = None if "--no-cost" in argv else K.callgrind_exe()
    V = variants(exe)
    RES, WS = {}, {}
    for k, p in V.items():
        p = trim_final(exe, p)
        if k in ("C2", "D2"):         # the trace was found at VOLUME 100; check it again at the final level (the tape is not linear) and refit once
            v, d = find_trace(exe, p)
            if v != p["NOISE"]:
                print(k, "refit NOISE", p["NOISE"], "->", v, "(%.2f dB)" % d); p["NOISE"] = v; p = trim_final(exe, p)
            if k == "D2": V["D3"]["NOISE"] = p["NOISE"]
        m, W = measure(exe, cg, k, p, "--no-cost" in argv)
        m["params"], m["volume"] = p, p["VOLUME"]; RES[k], WS[k] = m, W
        print(f"{k} VOL {p['VOLUME']} NOISE {p['NOISE']} lvl {m['level']:.2f} pk {m['peak_all']:.2f} noise-pulse {m['comp']['diff']:.1f} " + (f"cpu {m['cost']['idle'] + m['cost']['load']:.0f}" if m["cost"] else ""), flush=True)
    # CPU of D2 at POLY 2..5 and the notes that sound
    RES["_poly"] = {}
    for n in (2, 3, 4, 5):
        q = {**RES["D2"]["params"], "POLY_N": n}
        notes = which_notes(exe, q)
        cpu = None
        if cg and "--no-cost" not in argv:
            b, l = K.cost(cg, params=q, tag="r2pn"); ir, fr = K.callgrind_ips(cg, "x_stress", params=q, tag="r2pi", notes=False); cpu = {"idle": ir / fr, "load": l, "worst": ir / fr + l}
        RES["_poly"][n] = {"notes": notes, "cpu": cpu}
    if "--no-wav" not in argv:
        for k in V:
            for ph, nm in (("z_chord", "held-chord"), ("z_tap", "tap"), ("b_stabs", "stabs")):
                K.write_wav(os.path.join(OUT, f"23-crypt-dust_{k}_{nm}.wav"), WS[k][ph][int(K.T_CUT * FS):])
    json.dump(RES, open(os.path.join(OUT, "results.json"), "w"), default=A.jdefault, indent=1)


if __name__ == "__main__":
    main()
