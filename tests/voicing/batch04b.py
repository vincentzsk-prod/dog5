#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Voicing round for Batch 4B, Chapter II "the tape / crash pair": 13 Ghost Board, 14 Reef Break.

  python3 tests/voicing/batch04b.py [base_tree] [--only SLOT] [--quick] [--no-cost] [--no-wav]
  python3 tests/voicing/batch04b.py --emit SLOT KEY      the C array of a variant (from results.json)

Same method as batch04a.py (a variant is a FULL parameter list; A is rendered through the base program path; B..D over INIT; VOLUME is trimmed last to -18.0 dBFS RMS on the patch's own
phrase, effects and tape included, tails excluded; peak <= -4).  Output: listen/voicing/batch-04b/<NN-name>/ (tables on the merged voicing branch; WAVs only on the never-merged listen branch)."""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import batch01a as B
import batch02a as B2
import batch02a_metrics as M
import batch03a_metrics as N
import batch04a as A
import batch04a_metrics as Q
import batch04b_metrics as Z
from batch04b_variants import PATCHES

OUT = os.path.join(K.ROOT, "listen", "voicing", "batch-04b")
SHORT = {"b_stabs": "stabs", "t_ghost": "ghost", "u_crash": "crash"}
RET_WINS = A.RET_WINS
G_CH, G_LINE, G_FIG = (3000, 5400), [(8000, 8800), (9300, 10100), (10600, 11400), (11900, 12700)], [(14700 + 450 * i, 14850 + 450 * i) for i in range(6)]
U_HITS = [(t, t + 300) for t in (3000, 6500, 10000, 11000, 12000, 13500, 14100, 14700, 16200, 16600, 17000)]
SEED2 = ("2950 midi 0x90 24 1", "2970 midi 0x80 24 0")        # a quiet dummy note first: the hits then fall on other voice cards (other noise generators)


def f1(x, p=1):
    return A.f1(x, p)


def measure_13(exe, p, tag, w, m):
    a = w["t_ghost"]
    R = Q.fx_set(exe, "t_ghost", p, tag)
    nochew = K.render(exe, "t_ghost", params={**p, "CHEW": 0}, tag=tag + "n")[0]       # the same mix without the deck
    voice = R["dry"]                                                                # sends off, the deck still on
    notes_all = [G_CH] + G_LINE + G_FIG
    m["notes"] = Q.note_windows(a, notes_all)
    m["notes_nochew"] = Q.note_windows(nochew, notes_all)
    m["chord_nochew"] = Q.note_windows(nochew, [(G_CH[0] + 400, G_CH[1])])
    m["chord_dry"] = Q.note_windows(voice, [(G_CH[0] + 400, G_CH[1])])
    m["tape"] = Z.tape_probe(exe, p)
    m["tri"] = Z.harmonics_tri(exe, p)
    m["corr"] = Q.chan_corr(voice, G_CH[0] + 400, G_CH[1])
    m["corr_full"] = Q.chan_corr(a, G_CH[0] + 400, G_CH[1])
    T = Q.alley_ms(p["ALLEY"])
    S, on, off = Q.solo_set(exe, p, [64], 150, tail_ms=4000, tag="s13")
    m["delay_ms"] = T
    m["first"] = Q.first_repeat(S, on, off, T)
    m["train"] = Q.repeats_train(S, on, off, T, n=6)
    m["solo_split"] = Q.window_split(S["dly"] - S["dry"], on + T, on + T + 300)
    m["solo_onwin"] = {k: N.wet_windows(S[k], S["dry"], on) for k in ("dly", "spr")}
    m["ret"] = {"ch1": Q.return_windows(R, G_CH[1], 400, RET_WINS)}
    m["under"] = Q.under_note(R, G_FIG)
    dc = A.dc_of(a, 7000, 7600)
    m["tailsplit"] = Q.tail_after(a, G_CH[1], wins=((0, 250), (250, 750), (750, 1500)), dc=dc)
    m["tail"] = M.tail_times(a, G_CH[1], 150, 2500, dc=dc)
    m["tail_nochew"] = M.tail_times(nochew, G_CH[1], 150, 2500, dc=dc)
    m["line_tail"] = M.tail_times(a, G_LINE[-1][1], 100, 2000, dc=A.dc_of(a, 13000, 13600))
    return m


def measure_14(exe, p, tag, w, m):
    a = w["u_crash"]
    R = Q.fx_set(exe, "u_crash", p, tag)
    voice = R["dry"]
    a2 = K.render(exe, "u_crash", params=p, extra=SEED2, tag=tag + "s2")[0]
    m["seed2"] = {"rms": K.level_metrics(a2, "u_crash")["rms"], "peak": K.level_metrics(a2, "u_crash")["peak"], "crest": N.crest_db(a2, "u_crash")}
    m["rail"] = Z.rail_share(a, 3000, 3300)
    m["rail_all"] = float(np.mean([Z.rail_share(a, t, t + 300) for t, _ in U_HITS]))
    m["notes"] = Q.note_windows(a, U_HITS)
    m["att"] = {"low": Z.hit_attack(voice, 3000), "mid": Z.hit_attack(voice, 6500)}
    m["bands_low"] = Z.band_table(voice, 3000)
    m["bands_mid"] = Z.band_table(voice, 6500)
    m["bands_full"] = Z.band_table(a, 3000)
    m["nvs"] = {"low": Z.noise_vs_sub(exe, p, 33), "mid": Z.noise_vs_sub(exe, p, 45)}
    sub = K.render(exe, "u_crash", params={**p, **Q.FXOFF_ALL, "NOISE": 0}, tag=tag + "sub")[0]
    m["sub_shares"] = {"low": M.band_shares(sub, 3000, 3150), "mid": M.band_shares(sub, 6500, 6650)}
    m["sub_decay"] = Z.sub_decay(sub, 3000)
    m["voice_tail"] = M.tail_times(voice, 3300, 100, 1500, dc=A.dc_of(voice, 5500, 5900))
    S, on, off = Q.solo_set(exe, p, [33], 300, tail_ms=7000, vel=108, tag="s14")
    T = Q.alley_ms(p["ALLEY"])
    m["delay_ms"] = T
    m["echo"] = Z.repeats_re_burst(S, on, T, n=16)
    m["echo_n40"] = sum(1 for _, v in m["echo"] if v > -40)
    m["echo_windows"] = Z.echo_windows(S, on, T)
    m["echo_peak"] = float(20 * np.log10(np.abs(S["full"]).max() / 32767))
    m["echo_clip"] = int((np.abs(S["full"]) >= 32767).sum())
    m["first"] = Q.first_repeat(S, on, off, T)
    m["under"] = Q.under_note(R, U_HITS[2:])["dly"]
    m["tail"] = M.tail_times(S["full"], off, 100, 6500, dc=A.dc_of(S["full"], on + 6200, on + 6900))
    m["tail_voice"] = M.tail_times(S["dry"], off, 100, 1500, dc=A.dc_of(S["dry"], on + 5000, on + 6000))
    return m


MEASURE = {13: measure_13, 14: measure_14}


def measure(exe, cg, spec, params, tag, quick, orig=None, no_cost=False):
    w, m = A.level_block(exe, spec, params, tag, orig)
    m["attack"] = {"voice": Q.attack_long(exe, params, note=57)}
    m = MEASURE[spec["slot"]](exe, params, tag, w, m)
    m["cost"] = None
    if not quick and not no_cost:
        cb, cl = K.cost(cg, params=params, tag=tag)
        ir, fr = K.callgrind_ips(cg, "x_stress", params=params, tag=tag + "i", notes=False)
        m["cost"] = {"b": cb, "load": cl, "idle": ir / fr}
    return w, m


def summary(spec, key, m, vol):
    s = f"{spec['slot']:02d}{key} VOL {vol:3d} lvl {m['level']:6.2f} (b) {m['b']:6.2f} pk {m['peak_all']:6.2f} own {m[spec['level']]['peak']:6.2f} crest {m[spec['level']]['crest']:4.1f}"
    if spec["slot"] == 13:
        t = m["tape"]["tape"]
        s += f"  wobble {t['sd']:.1f}c {t['rate']:.1f}Hz  tri {' '.join(f'{x:.0f}' for x in m['tri'])}  cent {m['notes']['cent']:.0f} mud {m['notes']['mud']:.1f}  1st {m['first']['dly_re_note']:+.1f}dB spr-margin {m['first']['margin']:+.1f}  tailmud {' '.join(f'{t2['mud']:.0f}' for t2 in m['tailsplit'])}"
    else:
        s += f"  att {m['att']['low']['t10']:.1f}/{m['att']['low']['t50']:.1f}/{m['att']['low']['t90']:.1f}ms  nvs {m['nvs']['low']['ratio']:+.1f}dB  rail {m['rail']:.0f}%  seed2 pk {m['seed2']['peak']:.1f} crest {m['seed2']['crest']:.1f}  echo n40 {m['echo_n40']}  4k+ {f1(m['bands_low']['decay']['4k+']['t20'],0)}/{f1(m['bands_low']['decay']['4k+']['t40'],0)}ms"
    return s


def own_peak(exe, spec, params):
    """the peak that limits VOLUME: the patch's OWN phrase, and for 14 (noise: the peak follows the random seed) the worse of two seeds; phrase (b) stacks three noise voices on 14 and is reported, not limiting"""
    ph = spec["level"]
    pk = K.level_metrics(K.render(exe, ph, params=params, tag="pk")[0], ph)["peak"]
    if spec["slot"] == 14:
        pk = max(pk, K.level_metrics(K.render(exe, ph, params=params, extra=SEED2, tag="pk2")[0], ph)["peak"])
    if spec["slot"] == 13:
        pk = max(pk, K.level_metrics(K.render(exe, "b_stabs", params=params, tag="pk3")[0], "b_stabs")["peak"])
    return pk


def run(spec, base, quick, no_cost, no_wav):
    exe = K.build_host()
    cg = None if (quick or no_cost) else K.callgrind_exe()
    old = K.build_host(base, os.path.join(K.BUILD, "obervave_base"))
    orig = B.resolve(base, spec["slot"])
    R, wavs = {}, {}
    for key, tag, desc, ch in spec["variants"]:
        if key == "A":
            params = dict(orig)
            w, m = measure(exe, cg, spec, params, f"{spec['slot']}{key}", quick, orig=(old, spec["slot"] - 1), no_cost=no_cost)
            vol = orig["VOLUME"]
        else:
            params = {**orig, **ch}
            vol, _ = B2.trim_volume(exe, {**spec, "phrases": [spec["level"]]}, params)
            while own_peak(exe, spec, {**params, "VOLUME": vol}) > -4.2 and vol > 1:
                a, _ = K.render(exe, spec["level"], params={**params, "VOLUME": vol - 1}, tag="trim")
                if B2.level_of(spec, {spec["level"]: a}) < (-21.0 if spec["slot"] == 14 else -19.3):
                    break
                vol -= 1
            params["VOLUME"] = vol
            w, m = measure(exe, cg, spec, params, f"{spec['slot']}{key}", quick, no_cost=no_cost)
        m["volume"], m["params"], m["tag"], m["desc"] = vol, params, tag, desc
        R[key], wavs[key] = m, w
        print(summary(spec, key, m, vol), flush=True)
    if quick:
        json.dump(R, open(os.path.join(K.BUILD, f"quick4b_{spec['slot']}.json"), "w"), default=A.jdefault)
        return R
    d = os.path.join(OUT, spec["dir"])
    os.makedirs(d, exist_ok=True)
    if not no_wav:
        for key in R:
            for ph in spec["phrases"]:
                K.write_wav(os.path.join(d, f"{spec['dir']}_{key}_{SHORT[ph]}.wav"), wavs[key][ph][int(K.T_CUT * K.FS):])
    return R


def main():
    argv = sys.argv[1:]
    quick, no_cost, no_wav = "--quick" in argv, "--no-cost" in argv, "--no-wav" in argv
    only = int(argv[argv.index("--only") + 1]) if "--only" in argv else None
    if "--emit" in argv:
        i = argv.index("--emit")
        slot, key = int(argv[i + 1]), argv[i + 2]
        spec = next(s for s in PATCHES if s["slot"] == slot)
        orig = B.resolve(os.path.join(K.BUILD, "base"), slot)
        ch = dict(next(v for v in spec["variants"] if v[0] == key)[3])
        res = json.load(open(os.path.join(OUT, spec["dir"], "results.json")))
        p = {**orig, **ch}
        p["VOLUME"] = res[key]["volume"]
        print(B.emit(spec["cname"], p))
        return
    pos = [a for a in argv if not a.startswith("--") and not a.isdigit()]
    base = os.path.abspath(pos[0]) if pos else os.path.join(K.BUILD, "base")
    for spec in PATCHES:
        if only and spec["slot"] != only:
            continue
        R = run(spec, base, quick, no_cost, no_wav)
        if not quick:
            d = os.path.join(OUT, spec["dir"])
            json.dump(R, open(os.path.join(d, "results.json"), "w"), default=A.jdefault, indent=1)
            from batch04b_report import write_all
            write_all(spec, R, d, B.resolve(base, spec["slot"]))


if __name__ == "__main__":
    main()
