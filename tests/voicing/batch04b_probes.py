#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Probes of Batch 4B: the recommended variant with ONE control stepped, as numbers (probes.md next to each README.md).   python3 tests/voicing/batch04b_probes.py [--only SLOT]"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import batch02a_metrics as M
import batch03a_metrics as N
import batch04a as A
import batch04a_metrics as Q
import batch04b_metrics as Z
import batch04b as P
from batch04b_variants import PATCHES

f1 = lambda x, p=1: "-" if x is None else f"{x:.{p}f}"


def md(hdr, rows):
    return ["| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)] + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows] + [""]


def probes_13(exe, p):
    L = ["## 13: what CHEW does (wobble, smear, cost), the soft tone, the deck's place in the chain", ""]
    rows = []
    for chew in (0, 40, 70, 100, 127):
        for wf in ((64,) if chew == 0 else (0, 64, 127)):
            q = {**p, "CHEW": chew, "TP_WOWFLT": wf}
            t = Z.tape_probe(exe, q)["tape"]
            a = K.render(exe, "t_ghost", params=q, tag="pb13")[0]
            nm = Q.note_windows(a, [P.G_CH] + P.G_LINE + P.G_FIG)
            rows.append((chew, wf, f"{t['sd']:.1f} / {t['range']:.1f} / {t['rate']:.1f}", f"{t['dips']} / {t['dip_db']:.1f}", f"{nm['cent']:.0f} / {nm['shares']['1.2k+']:.1f} / {nm['mud']:.1f}"))
    L += ["### CHEW and WOW/FLT on B (one voice A3 for the wobble; the whole ghost phrase for the tone)", ""]
    L += md(["CHEW", "WOW/FLT", "wobble: s.d. cents / 5-95 % range cents / strongest rate Hz", "dips >= 6 dB (n / deepest dB)", "note-on centroid Hz / % above 1.2k / MUD"], rows)
    cg = K.callgrind_exe()
    rows = []
    for nm, ov in (("B as shipped (CHEW 100)", {}), ("B with CHEW 0", {"CHEW": 0}), ("B with echo and spring off, CHEW 100", {"DLY_MIX": 0, "REV_MIX": 0})):
        q = {**p, **ov}
        cb, cl = K.cost(cg, params=q, tag="pb13c")
        ir, fr = K.callgrind_ips(cg, "x_stress", params=q, tag="pb13ci", notes=False)
        rows.append((nm, f"{ir / fr + cl:.0f}", f"{ir / fr:.0f}", f"{cl:.0f}"))
    L += ["### CPU (host instr/sample)", ""] + md(["", "worst case", "idle", "load"], rows)
    rows = []
    for c in (60, 64, 70, 76, 84):
        q = {**p, "CUTOFF": c}
        tri = Z.harmonics_tri(exe, q)
        a = K.render(exe, "t_ghost", params=q, tag="pb13b")[0]
        nm = Q.note_windows(a, [P.G_CH] + P.G_LINE + P.G_FIG)
        rows.append((c, f"{440 * 2 ** ((c + 8 - 69) / 12):.0f}", " / ".join(f"{x:.1f}" for x in tri), f"{nm['cent']:.0f}", f"{nm['mud']:.1f}"))
    L += ["### CUTOFF (LP12, 100 % key tracking) against the triangle probe and MUD (B's 2-octave-up copy kept)", ""] + md(["CUTOFF", "Hz at C4", "harmonics 3 / 5 / 7 re H1 (triangle -19.1 / -28.0 / -34.2)", "note-on centroid Hz", "note-on MUD"], rows)
    rows = []
    for lv in (0, 50, 80, 112, 127):
        q = {**p, "O2_LVL": lv}
        a = K.render(exe, "t_ghost", params=q, tag="pb13c")[0]
        nm = Q.note_windows(a, [P.G_CH] + P.G_LINE + P.G_FIG)
        dc = A.dc_of(a, 7000, 7600)
        ts = Q.tail_after(a, 5400, wins=((0, 250), (250, 750), (750, 1500)), dc=dc)
        rows.append((lv, f"{nm['cent']:.0f}", f"{nm['shares']['1.2k+']:.1f}", f"{nm['mud']:.1f}", " / ".join(f"{t['mud']:.0f}" for t in ts)))
    L += ["### the 2-octave-up copy (OSC 2 LEVEL; B 112): where the energy above 1.2 kHz comes from", ""] + md(["O2 LEVEL", "centroid Hz", "% above 1.2k", "note-on MUD", "tail MUD 0-250 / 250-750 / 750-1500 ms"], rows)
    return L


def probes_14(exe, p):
    L = ["## 14: what the filter does to a noise burst, the attack, the echo's limit", ""]

    def hitrow(q):
        v = K.render(exe, "u_crash", params={**q, **Q.FXOFF_ALL}, tag="pb14")[0]
        a = K.render(exe, "u_crash", params=q, tag="pb14a")[0]
        t = Z.band_table(v, 3000)
        sub = K.render(exe, "u_crash", params={**q, **Q.FXOFF_ALL, "NOISE": 0}, tag="pb14s")[0]
        sd = Z.sub_decay(sub, 3000)
        l = K.level_metrics(a, "u_crash")
        d = t["decay"]
        r = Z.noise_vs_sub(exe, q, 33)
        return [f"{f1(sd['t20'], 0)} / {f1(sd['t40'], 0)}", f"{f1(d['400-1.2k']['t20'], 0)} / {f1(d['400-1.2k']['t40'], 0)}", f"{f1(d['1.2k-4k']['t20'], 0)} / {f1(d['1.2k-4k']['t40'], 0)}", f"{f1(d['4k+']['t20'], 0)} / {f1(d['4k+']['t40'], 0)}",
                f"{r['ratio']:+.1f}", f"{l['rms']:.1f} / {l['peak']:.1f}"]

    H = ["sub (40-150) to -20 / -40 dB ms", "400-1.2k to -20 / -40 dB ms", "1.2k-4k to -20 / -40 dB ms", "4k+ to -20 / -40 dB ms", "noise-to-sub first 100 ms dB", "level / peak at the same VOLUME (dBFS)"]
    L += ["### what a filter can do for the cymbal's decay (B's noise, sub, envelopes; one control changed; VOLUME as B; the decays are of the voice alone, from the A1 hit)", ""]
    rows = []
    for nm, ov in (("B: HP12, CUTOFF 100, ENV AMT 0 (the cutoff climbs from -97 st), FD 100", {}),
                   ("LP12, CUTOFF 60, ENV AMT 110 (opens at the strike, closes: the original's way)", dict(FTYPE=0, CUTOFF=60, FENV_AMT=110)),
                   ("LP12 wide open (CUTOFF 127), no envelope", dict(FTYPE=0, CUTOFF=127, FENV_AMT=64)),
                   ("NOTCH, CUTOFF 85, RESO 30, no envelope", dict(FTYPE=3, CUTOFF=85, RESO=30, FENV_AMT=64)),
                   ("HP12 with no envelope (ENV AMT 64, the sub is cut)", dict(FENV_AMT=64)),
                   ("BP12, CUTOFF 100, ENV AMT 0", dict(FTYPE=2))):
        rows.append([nm] + hitrow({**p, **ov}))
    L += md([""] + H, rows)
    L += ["### FD (how long the high-pass stays low = the sub's duration), B", ""]
    L += md(["FD"] + H, [[v] + hitrow({**p, "FD": v}) for v in (85, 92, 100, 108)])
    L += ["### AD / AR (the ring-out; both stepped together), B", ""]
    L += md(["AD = AR"] + H, [[v] + hitrow({**p, "AD": v, "AR": v}) for v in (84, 88, 92, 97)])
    rows = []
    for aa in (0, 30, 44, 52, 60):
        a = K.render(exe, "u_crash", params={**p, **Q.FXOFF_ALL, "AA": aa}, tag="pb14aa")[0]
        at = Z.hit_attack(a, 3000)
        rows.append((aa, f"{at['t10']:.1f} / {at['t50']:.1f} / {at['t90']:.1f}", f"{at['peak_ms']:.1f}"))
    L += ["### AA -> the hit's attack (A1, voice alone, 10 / 50 / 90 % of the peak, ms)", ""] + md(["AA", "10 / 50 / 90 % ms", "peak at ms"], rows)
    rows = []
    for nz, o1, o2 in ((127, 80, 45), (127, 110, 60), (100, 80, 45), (127, 50, 30), (127, 0, 0), (0, 80, 45)):
        q = {**p, "NOISE": nz, "O1_LVL": o1, "O2_LVL": o2}
        r = Z.noise_vs_sub(exe, q, 33)
        a = K.render(exe, "u_crash", params=q, tag="pb14n")[0]
        l = K.level_metrics(a, "u_crash")
        rows.append((nz, o1, o2, f"{r['noise']:.1f} / {r['sub']:.1f}", f"{r['ratio']:+.1f}", f"{l['rms']:.1f} / {l['peak']:.1f}"))
    L += ["### NOISE / sub levels (B at VOLUME 118)", ""] + md(["NOISE", "O1 LVL", "O2 LVL", "noise / sub dBFS first 100 ms (A1)", "ratio dB", "level / peak of the phrase"], rows)
    rows = []
    for fb in (96, 105, 112, 114, 118, 122, 127):
        q = {**p, "DLY_FB": fb}
        S, on, off = Q.solo_set(exe, q, [33], 300, tail_ms=9000, vel=108, tag="pb14f")
        T = Q.alley_ms(q["ALLEY"])
        tr = Z.repeats_re_burst(S, on, T, n=24)
        n40 = sum(1 for _, v in tr if v > -40)
        pk = float(20 * np.log10(np.abs(S["full"]).max() / 32767))
        clip = int((np.abs(S["full"]) >= 32767).sum())
        rows.append((fb, " ".join(f"{v:+.0f}" for _, v in tr[:6]), f"{tr[11][1]:+.0f} / {tr[23][1]:+.0f}", n40, f"{pk:.1f} / {clip}"))
    L += ["### FEEDBK: where the echo stops decaying (B, MIX 90, 361 ms; 24 slots = 8.7 s)", ""] + md(["FEEDBK", "repeats 1..6 re the burst (dB)", "repeat 12 / 24 (dB)", "slots above -40 dB", "peak dBFS / clipped samples"], rows)
    return L


def main():
    argv = sys.argv[1:]
    only = int(argv[argv.index("--only") + 1]) if "--only" in argv else None
    exe = K.build_host()
    for spec in PATCHES:
        if only and spec["slot"] != only:
            continue
        d = os.path.join(P.OUT, spec["dir"])
        R = json.load(open(os.path.join(d, "results.json")))
        p = R[spec["recommend"]]["params"]
        hdr = [f"# Batch 4B, {spec['slot']:02d} {spec['name']}: probes (the recommended variant {spec['recommend']} with one control stepped; numbers, not variants)", ""]
        L = probes_13(exe, p) if spec["slot"] == 13 else probes_14(exe, p)
        open(os.path.join(d, "probes.md"), "w").write("\n".join(hdr + L) + "\n")
        print("wrote", d)


if __name__ == "__main__":
    main()
