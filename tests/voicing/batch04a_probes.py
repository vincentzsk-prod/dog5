#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Probes of Batch 4A: the recommended variant (or the named one) with ONE control stepped, as numbers (not variants).  Writes probes.md next to each patch's README.md.

  python3 tests/voicing/batch04a_probes.py [--only SLOT] [KEY]      (KEY = the variant the probes step from, default the recommended one)"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import batch02a_metrics as M
import batch03a_metrics as N
import batch04a_metrics as Q
import batch04a as A
from batch04a_variants import PATCHES

f1 = lambda x, p=1: f"{x:.{p}f}"


def md(hdr, rows):
    return ["| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)] + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows] + [""]


def probes_10(exe, p):
    L = ["## 10: what builds the chorus, what the delay's TONE does, the Leslie phase", ""]
    chorus = (("B as shipped: pitch +-19 cents on BOTH, SPREAD", {}), ("pitch on OSC 2 only", {"LFO_PITCH_TO": 1}), ("pitch +-19 cents, PHASE FREE (voices in step)", {"LFO_PHASE": 1}),
              ("no pitch LFO (only the DUAL detune, 5.5 cents)", {"LFO_PITCH": 0}),
              ("DETUNE 0, pitch LFO +-19 cents with SPREAD (the chorus without the static detune)", {"UNI_DET": 0}), ("DETUNE 0, pitch LFO +-19 cents, PHASE FREE", {"UNI_DET": 0, "LFO_PHASE": 1}), ("no LFO and no detune (DETUNE 0): a plain DUAL pair", {"LFO_PITCH": 0, "UNI_DET": 0}),
              ("a short BBD instead: no pitch LFO, ALLEY 15, FEEDBK 0, MIX 90, PINGPONG 127", {"LFO_PITCH": 0, "ALLEY": 15, "DLY_FB": 0, "DLY_MIX": 90}))
    rows = []
    for nm, ov in chorus:
        q = {**p, **ov}
        R = Q.fx_set(exe, "q_organ", {**q, "REV_MIX": 0, "DLY_MIX": q["DLY_MIX"] if "ALLEY" in ov else 0}, "pb10")
        dry = R["full"] if "ALLEY" in ov else R["dry"]
        c = Q.chan_corr(dry, 3500, 5400)
        b = Q.band_beat(dry, 220.0, 3300, 5400)
        am = Q.am_depth(dry, 3400, 5400)
        sp = Q.window_split(dry, 3500, 5400)
        rows.append((nm, f"{c[0]:.2f} / {c[1]:.1f}", f"{b['rate_mean']:.2f} / {b['depth_db']:.1f}", f"{am[0]:.1f}", f"{sp['cent']:.0f}"))
    L += md(["B with one thing changed (the held A minor chord, voice + the short BBD where named)", "L/R corr / side-to-mid dB", "A3-band beat rate Hz / depth dB", "level modulation dB", "centroid Hz"], rows)
    L += ["The short-BBD row has a fixed delay time (ALLEY 15 = " + f"{Q.alley_ms(15):.1f} ms" + "): the engine has no LFO on the BBD's time, so it is a comb filter and a Haas widener, not a chorus; the row shows its width and the comb's effect on the centroid. "
          "CHEW is not used in any variant (it smears the top, measured in 05 round 1; here the first repeat is already 43 % darker than the note by the BBD's own band-limit).", ""]
    rows = []
    for tone in (60, 90, 127):
        S, on, off = Q.solo_set(exe, {**p, "DLY_TONE": tone}, [64], 120, tail_ms=4000, tag="pb10t")
        T = Q.alley_ms(p["ALLEY"])
        e = S["dly"] - S["dry"]
        r1 = Q.window_split(e, on + T - 20, on + T + 140)
        r3 = Q.window_split(e, on + 3 * T - 20, on + 3 * T + 140)
        rows.append((tone, f"{r1['cent']:.0f}", f"{r3['cent']:.0f}", " ".join(f"{v:+.1f}" for _, _, v in Q.repeats_train(S, on, off, T, n=5))))
    L += ["### DLY TONE on the repeats (isolated E4)", ""] + md(["DLY_TONE", "first repeat centroid Hz", "third repeat centroid Hz", "repeats 1..5 dB re the first"], rows)
    rows = []
    for fb in (85, 95, 105):
        S, on, off = Q.solo_set(exe, {**p, "DLY_FB": fb}, [64], 120, tail_ms=6000, tag="pb10f")
        T = Q.alley_ms(p["ALLEY"])
        tt = M.tail_times(S["full"], off, 60, 6000, dc=A.dc_of(S["full"], off + 5700, off + 5990))
        rows.append((fb, " ".join(f"{v:+.1f}" for _, _, v in Q.repeats_train(S, on, off, T, n=8)), tailstr(tt)))
    L += ["### FEEDBK (isolated E4; tail = to -20 / -40 / -60 dB re the note, ms)", ""] + md(["DLY_FB", "repeats 1..8 dB re the first", "tail ms"], rows)
    rows = []
    for ph, nm in ((2, "SPREAD"), (1, "FREE"), (0, "SYNC")):
        for amp in (0, 45, 80):
            R = Q.fx_set(exe, "q_organ", {**p, "LFO_PHASE": ph, "LFO_AMP": amp, "DLY_MIX": 0, "REV_MIX": 0}, "pb10a")
            am = Q.am_depth(R["dry"], 3400, 5400)
            rows.append((nm, amp, f"{Q.amp_db(amp):.1f}" if amp else "0", f"{am[0]:.1f} / {am[1]:.2f}"))
    L += ["### the tremolo on the held chord by LFO PHASE (why D is FREE: with SPREAD the voices' tremolos are 45 degrees apart and cancel in the sum)", ""] + md(["LFO_PHASE", "LFO_AMP", "one voice's dip dB (law)", "tremolo of the chord: depth dB / rate Hz"], rows)
    cg = K.callgrind_exe()
    rows = []
    for nm, ov in (("B as shipped: DUAL, POLY 6, two oscillators", {}), ("B with one oscillator (OSC 2 off; the 4' register gone)", {"O2_WAVE": 0}), ("B as POLY (one voice per note: no L / R pair, the chorus is gone)", {"MODE": 0, "POLY_N": 5}),
                   ("B with the BBD and the spring off (voices only)", {"DLY_MIX": 0, "REV_MIX": 0})):
        cb, cl = K.cost(cg, params={**p, **ov}, tag="pb10c")
        ir, fr = K.callgrind_ips(cg, "x_stress", params={**p, **ov}, tag="pb10ci", notes=False)
        rows.append((nm, f"{ir / fr + cl:.0f}", f"{ir / fr:.0f}", f"{cl:.0f}"))
    L += ["### CPU levers (host instr/sample; the heaviest voiced patches are 15 D 2375, 07 B 2177)", ""] + md(["", "worst case", "idle", "load"], rows)
    return L


def tailstr(t):
    return " / ".join(f"{t[k]:.0f}" if t.get(k) is not None else ">win" for k in ("t20", "t40", "t60"))


def probes_12(exe, p, orig):
    L = ["## 12: the tension between murk and a PWM you can hear, the spring, the PWM depth", ""]
    bs = ("150-400", "400-1.2k", "1.2k-3k")

    def line(q, tag):
        a = K.render(exe, "r_tangle", params=q, tag="pb12")[0]
        dry = K.render(exe, "r_tangle", params={**q, "REV_MIX": 0}, tag="pb12d")[0]
        pa = N.pwm_metrics(dry, 3000, 6200)["bands"]
        pc = N.pwm_metrics(dry, 8000, 11000)["bands"]
        ca = Q.note_windows(dry, [(3500, 6200)])
        cc = Q.note_windows(dry, [(8500, 11000)])
        dc = A.dc_of(a, 12300, 12800)
        ts = Q.tail_after(a, 11000, wins=((0, 250), (250, 750), (750, 1500)), dc=dc)
        tt = M.tail_times(a, 11000, 150, 2150, dc=A.dc_of(a, 12900, 13150))
        rw = Q.return_windows({"full": a, "dry": dry, "dly": dry, "spr": a}, 11000, 400, ((0, 250), (250, 750), (750, 1500)))
        on = N.wet_windows(a, dry, 8000)
        return (tag, f"{ca['cent']:.0f} / {ca['shares']['1.2k+']:.1f}", " / ".join(f1(pa[b][0]) for b in bs), f1(pa["level"][0]), f"{cc['cent']:.0f} / {cc['shares']['1.2k+']:.1f}", " / ".join(f1(pc[b][0]) for b in bs),
                " / ".join(f"{t['mud']:.0f}" for t in ts), " / ".join(f"{t['db']:.0f}" for t in ts), " / ".join(f1(r["spr"]) for r in rw), " / ".join(f1(r["re_dry_db"]) for r in on), tailstr(tt))

    H = ["", "held A2 dry: centroid Hz / % 1.2k+", "A2 PWM depth dB 150-400 / 400-1.2k / 1.2k-3k", "A2 level modulation dB", "chord dry: centroid Hz / % 1.2k+", "chord PWM depth dB 150-400 / 400-1.2k / 1.2k-3k",
         "tail MUD 0-250 / 250-750 / 750-1500", "tail level dBFS, same windows", "spring return re the chord dB, same windows", "spring re the chord after its note-on, 0-20 / 20-100 / 100-250 ms dB", "tail to -20 / -40 / -60 dB ms"]
    L += ["### CUTOFF (LP24, 100 % key tracking; one step = a semitone; Hz at C4 = 440 * 2^((CUTOFF + 8 - 69) / 12))", ""]
    L += md(["CUTOFF"] + H[1:], [line({**p, "CUTOFF": c}, f"{c} ({440 * 2 ** ((c + 8 - 69) / 12):.0f} Hz)") for c in (78, 86, 92, 98, 104)])
    L += ["### per-voice DRIVE (FILTER + page KNOB 1; before the filter), CUTOFF 86", ""] + md(["DRIVE"] + H[1:], [line({**p, "DRIVE": d}, str(d)) for d in (0, 20, 40)])
    L += ["### DRAIN (SIZE 75, DAMP 30)", ""] + md(["DRAIN"] + H[1:], [line({**p, "REV_MIX": d}, f"{d} ({100 * d / 127:.0f} %)") for d in (0, 30, 55, 80)])
    L += ["### SIZE (DRAIN 55)", ""] + md(["SIZE"] + H[1:], [line({**p, "REV_SIZE": s}, str(s)) for s in (50, 62, 75, 90)])
    L += ["### LFO PWM depth (the sweep around 33 %: law +-(d*d>>7)*0.195 points) and the base width", ""]
    rows = []
    for pwm, pw in ((60, 42), (80, 42), (100, 42), (115, 42), (100, 36), (100, 48)):
        q = {**p, "LFO_PWM": pwm, "O1_PW": pw, "O2_PW": pw}
        pts = Q.pwm_points(pwm)
        c = 100 * (pw + .5) / 128
        r = line(q, "")
        rows.append((pwm, f"{c:.0f} % +-{pts:.1f} ({c - pts:.0f}-{c + pts:.0f} %)", r[2], r[3], r[5]))
    L += md(["LFO_PWM", "PW centre and sweep", "A2 PWM depth dB 150-400 / 400-1.2k / 1.2k-3k", "A2 level mod dB", "chord PWM depth dB"], rows)
    L += ["### what the original's audible movement is (A, the nearest-base patch)", ""]
    rows = []
    for nm, ov in (("A as it stood (PWM +-2.3 points, inverse narrow pulses 3.0 cents apart)", {}), ("A with LFO PWM 0", {"LFO_PWM": 0}), ("A with LFO PWM 0 and OSC 2 detune 0 (FINE 64)", {"LFO_PWM": 0, "O2_FINE": 64})):
        q = {**orig, **ov}
        a = K.render(exe, "r_tangle", params={**q, "REV_MIX": 0}, tag="pb12o")[0]
        pa = N.pwm_metrics(a, 3000, 6200)["bands"]
        rows.append((nm, " / ".join(f"{f1(pa[b][0])}" for b in bs), " / ".join(f"{pa[b][1]:.1f}" for b in bs)))
    L += md(["", "A2 depth dB 150-400 / 400-1.2k / 1.2k-3k", "strongest rate Hz"], rows)
    return L


def probes_16(exe, p, R):
    L = ["## 16: the attack, the width, the delay / spring balance", ""]
    rows = []
    for aa in (60, 66, 72, 78, 82, 86, 90):
        r = Q.attack_long(exe, {**p, "AA": aa})
        rows.append((aa, f"{Q.aa_ms(aa):.0f}", f"{r['t10']:.0f} / {r['t50']:.0f} / {r['t90']:.0f}", " / ".join(f"{r['re_plateau'][k]:.1f}" for k in ("20", "50", "100", "200"))))
    L += ["### AA -> the attack as heard (one voice, LFO off; the time table's nominal ms is NOT the 10-90 % time: 90 % arrives at about 0.75-0.85 of it)", ""]
    L += md(["AA", "nominal ms", "10 / 50 / 90 % of the plateau, ms", "level re the plateau at 20 / 50 / 100 / 200 ms, dB"], rows)
    rows = []
    for nm, ov in (("B as shipped: POLY 5, one voice per note", {}), ("B as DUAL, POLY 8 (each note a left / right pair; a 4-note chord uses all 8)", {"MODE": 1, "POLY_N": 8, "UNI_DET": 30})):
        q = {**p, **ov}
        RR = Q.fx_set(exe, "s_wash", q, "pb16")
        c, cf = Q.chan_corr(RR["dry"], 3400, 5000), Q.chan_corr(RR["full"], 3400, 5000)
        rows.append((nm, f"{c[0]:.2f} ({cf[0]:.2f})", f"{c[1]:.1f} ({cf[1]:.1f})"))
    L += ["### width", ""] + md(["", "L/R correlation dry (full)", "side-to-mid dB dry (full)"], rows)
    rows = []
    for mix in (70, 100, 127):
        for dr in (25, 45, 70, 100):
            q = {**p, "DLY_MIX": mix, "REV_MIX": dr}
            S, on, off = Q.solo_set(exe, q, [64], 400, tail_ms=3000, tag="pb16b")
            T = Q.alley_ms(q["ALLEY"])
            fr = Q.first_repeat(S, on, off, T)
            rows.append((mix, dr, f"{fr['dly_re_note']:.1f}", f"{fr['spr_re_note_same']:.1f}", f"{fr['margin']:+.1f}"))
    L += ["### delay / spring balance (isolated 400 ms E4; the first repeat and the spring in its window, re the dry note's peak)", ""]
    L += md(["DLY_MIX", "DRAIN", "first repeat dB", "spring dB", "delay over spring dB"], rows)
    return L


def main():
    argv = sys.argv[1:]
    only = int(argv[argv.index("--only") + 1]) if "--only" in argv else None
    exe = K.build_host()
    base = os.path.join(K.BUILD, "base")
    import batch01a as B
    for spec in PATCHES:
        if only and spec["slot"] != only:
            continue
        d = os.path.join(A.OUT, spec["dir"])
        R = json.load(open(os.path.join(d, "results.json")))
        p = R[spec["recommend"]]["params"]
        hdr = [f"# Batch 4A, {spec['slot']:02d} {spec['name']}: probes (the recommended variant {spec['recommend']} with one control stepped; numbers, not variants)", ""]
        if spec["slot"] == 10:
            L = probes_10(exe, p)
        elif spec["slot"] == 12:
            L = probes_12(exe, p, B.resolve(base, 12))
        else:
            L = probes_16(exe, p, R)
        open(os.path.join(d, "probes.md"), "w").write("\n".join(hdr + L) + "\n")
        print("wrote", d)


if __name__ == "__main__":
    main()
