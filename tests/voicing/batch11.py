#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Batch 11: 14 Reef Break attack change (FILTER ENV A 0 -> 82, AMP ENV A 52 -> 82), measured before / after with Batch 4B's measures.
  python3 tests/voicing/batch11.py MAIN_TREE      (MAIN_TREE = a checkout of main; "after" = this working tree)  -> build/voicing/batch11.json"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import batch01a as B
import batch04a as A
import batch04b as P
import batch04b_metrics as Z
from batch04b_variants import PATCHES

spec = next(s for s in PATCHES if s["slot"] == 14)
main_tree = os.path.abspath(sys.argv[1])
exe = K.build_host()
R = {}
for name, tree in (("before", main_tree), ("after", K.ROOT)):
    p = B.resolve(tree, 14)
    print(name, {k: p[k] for k in ("FA", "AA", "VOLUME")}, flush=True)
    w, m = A.level_block(exe, spec, p, "11" + name, None)
    m["attack"] = {"voice": P.Q.attack_long(exe, p, note=57)}
    m = P.measure_14(exe, p, "11" + name, w, m)
    m["params"] = p
    R[name] = m
    # per-band short-time energy of the dry voice on the A1 hit, 50 ms frames
    R[name]["frames"] = None
    print(P.summary(spec, name, m, p["VOLUME"]), flush=True)
json.dump(R, open(os.path.join(K.BUILD, "batch11.json"), "w"), default=A.jdefault, indent=1)
