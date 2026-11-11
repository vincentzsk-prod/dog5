# SPDX-License-Identifier: GPL-3.0-only
"""Batch 6A shared driver parts: trimming to the reference, peaks, CPU, WAV export, JSON."""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib6a import *

OUT = os.path.join(K.ROOT, "listen", "voicing", "batch-06a")
REF = -18.0
BASE = os.path.join(K.BUILD, "base")


def lvl_fn(spec):
    """the patch's own level reading of a render of spec['level']"""
    if spec["level"] == "d_lead":
        return lambda a: K.level_metrics(a, "d_lead")["rms"]
    if spec["level"] == "a_riff":
        return lambda a: K.level_metrics(a, "a_riff")["rms"]
    if spec["level"] == "z_chord":
        return lambda a: M.rms_db(a, 7000, 13000)       # +4 s .. +10 s of the held triad (as 19, 23, 24)
    raise KeyError(spec["level"])


def trim(exe, spec, p, ref=REF):
    f = lvl_fn(spec)
    v = p.get("VOLUME", 100)
    best = None
    for _ in range(10):
        a, _ = K.render(exe, spec["level"], params={**p, "VOLUME": v}, tag="trim6")
        r = f(a)
        if best is None or abs(r - ref) < abs(best[1] - ref):
            best = (v, r)
        if abs(r - ref) < 0.12:
            break
        nv = int(round(v * 10 ** ((ref - r) / 40)))
        v = max(1, min(127, nv if nv != v else v + (1 if ref > r else -1)))
    return best


def peaks(exe, spec, p):
    return {ph: M.peak_db(K.render(exe, ph, params=p, tag="pk6")[0]) for ph in spec["phrases"]}


def fit(exe, spec, p):
    """VOLUME for the reference, lowered further if any audition phrase peaks above -4 dBFS"""
    vol, _ = trim(exe, spec, p)
    p = {**p, "VOLUME": vol}
    while max(peaks(exe, spec, p).values()) > -4.0 and p["VOLUME"] > 1:
        p["VOLUME"] -= 1
    return p


def cpu(cg, p, tag):
    cb, cl = K.cost(cg, params=p, tag="c6" + tag)
    ir, fr = K.callgrind_ips(cg, "x_stress", params=p, tag="ci6" + tag, notes=False)
    return {"b": cb, "load": cl, "idle": ir / fr, "total": ir / fr + cl}


def common(exe, cg, spec, key, p, no_cost=False):
    W = {ph: K.render(exe, ph, params=p, tag="mc6")[0] for ph in spec["phrases"]}
    m = {"level": lvl_fn(spec)(W[spec["level"]]), "peaks": {k: M.peak_db(v) for k, v in W.items()}}
    m["peak_all"] = max(m["peaks"].values())
    m["clip"] = int(sum((np.abs(v) >= 32767).sum() for v in W.values()))
    m["b"] = K.level_metrics(W["b_stabs"], "b_stabs")["rms"]
    m["krms"] = K.level_metrics(W[spec["level"]], spec["level"])["rms_k"] if spec["level"] in ("d_lead", "a_riff") else None
    m["cost"] = None if (no_cost or cg is None) else cpu(cg, p, spec["dir"][:2] + key)
    return m, W


def jdefault(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, tuple):
        return list(o)
    return str(o)


def save(d, name, obj):
    os.makedirs(d, exist_ok=True)
    json.dump(obj, open(os.path.join(d, name), "w"), default=jdefault, indent=1)


def wav(d, spec, key, ph, a, short):
    K.write_wav(os.path.join(d, f"{spec['dir']}_{key}_{short}.wav"), a[int(K.T_CUT * FS):])
