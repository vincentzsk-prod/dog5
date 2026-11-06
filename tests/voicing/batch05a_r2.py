#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Batch 5A round 2: the new slot 19 "Micro-mist" (mid / upper register chord that scatters into a hovering mist).  No original: A-D are fresh takes.

  python3 tests/voicing/batch05a_r2.py [--quick] [--no-cost] [--no-wav] [--only KEY]
  python3 tests/voicing/batch05a_r2.py --emit KEY        the C array
  python3 tests/voicing/batch05a_r2.py --report          rewrite the README from results.json

Level: -18.0 dBFS RMS +-1.5 over +4 s .. +10 s of the held A3 C#4 E4 chord (phrase z_chord), VOLUME trimmed last; peak <= -4 over the chord, the tap, the A4 single, the riff and the stabs.
Output: listen/voicing/batch-05a/19-micro-mist/ (README.md + results.json on the voicing branch; WAVs only on the never-merged listen branch)."""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import batch01a as B
import batch02a_metrics as M
import batch03a_metrics as N
import batch04a as A
import batch04a_metrics as Q
import batch05a as R1
from batch05a_r2_variants import PATCH

OUT = os.path.join(K.ROOT, "listen", "voicing", "batch-05a", PATCH["dir"])
FS = K.FS
REF = -18.0
SHORT = {"z_chord": "held-chord", "z_tap": "tap", "a_riff": "riff", "b_stabs": "stabs", "z_single": "single-A4"}
BANDS4 = {"<150": (0, 150), "150-400": (150, 400), "400-1.2k": (400, 1200), "1.2k+": (1200, 24000)}
CH = (3000, 13000)
EV = [(57, 3000, 13000), (61, 3000, 13000), (64, 3000, 13000)]


def shares4(a, t0, t1):
    b = M.band_shares(a, t0, t1)
    s = {"<150": b["<60"] + b["60-150"], "150-400": b["150-400"], "400-1.2k": b["400-1.2k"], "1.2k+": b["1.2k+"]}
    return s


def win(a, t0, t1):
    s = shares4(a, t0, t1)
    return {"rms": M.rms_db(a, t0, t1), "cent": M.centroid(a, t0, t1, nfft=2048), "shares": s, "mud": s["150-400"] / max(s["1.2k+"], 1e-3)}


def selfosc(exe, p, resos=(0, 127), note=57):
    """the noise-fed self-oscillation probe (as N.selfosc_probe) on A3 with the patch's own cutoff / key tracking"""
    out = []
    for r in resos:
        row = {"reso": r or p["RESO"]}
        for nm, nz in (("hi", 24), ("lo", 12)):
            q = {**p, "O1_WAVE": 0, "O2_WAVE": 0, "NOISE": nz, "GROWL": 0, "DLY_MIX": 0, "REV_MIX": 0, "CHEW": 0, "VOLUME": 127, "LFO_PITCH": 0, "LFO_FLT": 0, "LFO_AMP": 0}
            if r:
                q["RESO"] = r
            a = N._run(exe, "so5", N._probe_script(q, [f"3000 midi 0x90 {note} 100", f"4500 midi 0x80 {note} 0"], 5200))
            row[nm] = M.rms_db(a, 3500, 4400)
        row["diff"] = row["hi"] - row["lo"]
        out.append(row)
    return out


def trim(exe, p):
    v = p.get("VOLUME", 100)
    best = None
    for _ in range(9):
        a, _ = K.render(exe, "z_chord", params={**p, "VOLUME": v}, tag="trim5b")
        r = M.rms_db(a, 3000 + 4000, 3000 + 10000)
        if best is None or abs(r - REF) < abs(best[1] - REF):
            best = (v, r)
        if abs(r - REF) < 0.12:
            break
        nv = int(round(v * 10 ** ((REF - r) / 40)))
        v = max(1, min(127, nv if nv != v else v + (1 if REF > r else -1)))
    return best


def peaks(exe, p):
    return {ph: M.peak_db(K.render(exe, ph, params=p, tag="pk5b")[0]) for ph in PATCH["phrases"]}


def measure(exe, cg, p, key, no_cost):
    m = {}
    W = {ph: K.render(exe, ph, params=p, tag="m5b")[0] for ph in PATCH["phrases"]}
    dry_p = {**p, "DLY_MIX": 0, "REV_MIX": 0, "CHEW": 0, "GROWL": 0}
    dry = K.render(exe, "z_chord", params=dry_p, tag="m5bd")[0]
    a = W["z_chord"]
    m["level"] = M.rms_db(a, 7000, 13000)
    m["krms"] = R1.krms(a, 7000, 13000)
    m["peaks"] = {k: M.peak_db(v) for k, v in W.items()}
    m["peak_all"] = max(m["peaks"].values())
    m["clip"] = int(sum((np.abs(v) >= 32767).sum() for v in W.values()))
    m["b"] = K.level_metrics(W["b_stabs"], "b_stabs")["rms"]
    # tone in windows (wet) and the dry voice at the settled hold
    m["windows"] = {f"{x}-{y}s": win(a, 3000 + int(x * 1000), 3000 + int(y * 1000)) for x, y in ((0, 1), (1, 2), (2, 4), (4, 10))}
    m["dry_windows"] = {f"{x}-{y}s": win(dry, 3000 + int(x * 1000), 3000 + int(y * 1000)) for x, y in ((0, 1), (4, 10))}
    s1 = K.render(exe, "z_single", params=p, tag="m5bs")[0]
    m["single"] = {"strike": win(s1, 3000, 4000), "settled": win(s1, 7000, 9000), "peak": M.peak_db(s1)}
    # grain flicker
    lfo_hz = Q.lfo_hz(p["LFO_RATE"])
    d = (p["LFO_PITCH"] * p["LFO_PITCH"]) >> 7
    fd = (p["LFO_FLT"] * p["LFO_FLT"]) >> 7
    m["flicker"] = {"hz": lfo_hz, "shape": p["LFO_SHAPE"], "pitch_cents": d * 24 / 256 * 100, "filter_st": fd * 97 / 256, "amp_dip_db": -20 * np.log10(max(1 - p["LFO_AMP"] / 128, 1e-3)) if p["LFO_AMP"] else 0.0}
    if d:
        m["flicker"]["pitch_probe"] = A.pitch_probe(exe, {**p, "LFO_PITCH_TO": 2, "LFO_PHASE": 1}, 69)
    cut_hz = 440 * 2 ** ((p["CUTOFF"] + 8 - 69) / 12)
    band = {"cut": (cut_hz / 1.5, cut_hz * 1.5)}
    env, fr = N.band_env(dry, 3000 + 5000, 3000 + 10000, band)
    dep, rate, pur = N.mod_rate_depth(env["cut"], fr, lo=0.5, hi=25.0)
    m["flicker"]["band_swing_db"], m["flicker"]["band_rate_hz"], m["flicker"]["cut_hz"] = dep, rate, cut_hz
    m["am"] = Q.am_depth(dry, 3000 + 5000, 3000 + 10000, lo=0.5, hi=25.0)
    # shimmer and width
    m["beat"] = K.beat_metrics(dry, 220.0, 3000 + 4000, 3000 + 10000)
    m["corr_dry"] = Q.chan_corr(dry, 3000 + 4000, 3000 + 10000)
    m["corr_full"] = Q.chan_corr(a, 3000 + 4000, 3000 + 10000)
    # echo of an isolated A4 (a whole copy of the note), spring against echo
    T = Q.alley_ms(p["ALLEY"])
    S, on, off = Q.solo_set(exe, p, [69], 300, tail_ms=7500, tag="s5b")
    m["delay_ms"] = T
    m["first"] = Q.first_repeat(S, on, off, T)
    m["train"] = Q.repeats_train(S, on, off, T, n=14)
    m["repeats_n40"] = sum(1 for k, t, v in m["train"] if v + m["first"]["dly_re_note"] > -40)
    m["solo_split"] = Q.window_split(S["dly"] - S["dry"], on + T, on + T + 300)
    # hover after key-up
    dc = A.dc_of(a, 18000, 18900)
    m["hover"] = M.tail_times(a, 13000, 150, 5800, dc=dc)
    m["hover_dry"] = M.tail_times(dry, 13000, 150, 2500)
    m["tail_split"] = Q.tail_after(a, 13000, wins=((0, 500), (500, 1500), (1500, 3000), (3000, 5500)), dc=dc)
    # taps
    t = W["z_tap"]
    dc_t = A.dc_of(t, 12000, 12900)
    m["taps"] = {"chord_gate_re_held": M.rms_db(t, 3000, 3150) - m["level"], "chord_gate": M.rms_db(t, 3000, 3150), "chord_cent": M.centroid(t, 3000, 3150, nfft=2048),
                 "a4_gate": M.rms_db(t, 8000, 8150), "a4_re_held": M.rms_db(t, 8000, 8150) - m["level"],
                 "chord_hover": M.tail_times(t, 3150, 150, 4500, dc=dc_t), "a4_hover": M.tail_times(t, 8150, 150, 4500, dc=dc_t),
                 "chord_after400": M.rms_db(t, 3550, 3650), "attack": R1.tap_block(t, (3000, 8000))}
    m["selfosc"] = selfosc(exe, p)
    m["cost"] = None
    if not no_cost:
        cb, cl = K.cost(cg, params=p, tag="mist" + key)
        ir, fr_ = K.callgrind_ips(cg, "x_stress", params=p, tag="misti" + key, notes=False)
        m["cost"] = {"b": cb, "load": cl, "idle": ir / fr_}
    return m, W


def run(quick, no_cost, no_wav, only):
    exe = K.build_host()
    cg = None if (quick or no_cost) else K.callgrind_exe()
    os.makedirs(OUT, exist_ok=True)
    RES, WAV = {}, {}
    for key, tag, desc, ch in PATCH["variants"]:
        if only and key != only:
            continue
        p = dict(ch)
        vol, r = trim(exe, p)
        p["VOLUME"] = vol
        while max(peaks(exe, p).values()) > -4.0 and p["VOLUME"] > 1:
            p["VOLUME"] -= 1
        m, W = measure(exe, cg, p, key, quick or no_cost)
        m["volume"], m["params"], m["tag"], m["desc"] = p["VOLUME"], p, tag, desc
        RES[key], WAV[key] = m, W
        c = m["cost"]
        print(f"19{key} {tag:6s} VOL {p['VOLUME']:3d} lvl {m['level']:6.2f} k {m['krms']:6.2f} pk {m['peak_all']:6.2f} cent {m['windows']['4-10s']['cent']:5.0f} sh {' '.join(f'{v:.0f}' for v in m['windows']['4-10s']['shares'].values())}"
              f" 1st {m['first']['dly_re_note']:+.1f} spr-margin {m['first']['margin']:+.1f} n40 {m['repeats_n40']} hover {m['hover']['t20']}/{m['hover']['t40']}/{m['hover']['t60']} tap {m['taps']['chord_gate_re_held']:+.1f}"
              f" so {[round(x['diff'], 1) for x in m['selfosc']]}" + (f" cpu {c['idle'] + c['load']:.0f}" if c else ""), flush=True)
    if quick:
        return RES
    if not no_wav:
        for key in RES:
            for ph in PATCH["wav"]:
                K.write_wav(os.path.join(OUT, f"{PATCH['dir']}_{key}_{SHORT[ph]}.wav"), WAV[key][ph][int(K.T_CUT * FS):])
    if not only:
        json.dump(RES, open(os.path.join(OUT, "results.json"), "w"), default=A.jdefault, indent=1)
        from batch05a_r2_report import write_all
        write_all(PATCH, RES, OUT)
    return RES


def main():
    argv = sys.argv[1:]
    if "--emit" in argv:
        res = json.load(open(os.path.join(OUT, "results.json")))
        print(B.emit(PATCH["cname"], res[argv[argv.index("--emit") + 1]]["params"]))
        return
    if "--report" in argv:
        from batch05a_r2_report import write_all
        write_all(PATCH, json.load(open(os.path.join(OUT, "results.json"))), OUT)
        return
    only = argv[argv.index("--only") + 1] if "--only" in argv else None
    run("--quick" in argv, "--no-cost" in argv, "--no-wav" in argv, only)


if __name__ == "__main__":
    main()
