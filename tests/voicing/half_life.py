#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Voicing round for slot 03 "Half-Life": renders the variants on the three audition phrases, level-matches them to the
bank reference, measures them, and writes listen/voicing/03-half-life/ (WAVs, numbers.md, release.png, results.json).

  python3 tests/voicing/half_life.py [base_tree]       base_tree: the exported firmware before the change (default
                                                       build/voicing/base: `git archive <commit> | tar -x -C ...`)

A variant is a full parameter list over INIT (voicekit.render(params=...)), so the round never depends on what slot 3
holds in the tree: re-running it after the recommended variant is committed gives the same files.  The ORIGINAL list is
the pre-change slot 3 resolved (defaults + PF_DUAL_SAW); the run proves it renders bit-identically to the pre-change
firmware's own slot 3 before anything else."""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K

OUT = os.path.join(K.ROOT, "listen", "voicing", "03-half-life")
BANK_REF = -18.0                                # dBFS RMS, phrase (b) note-on region: the BANK REFERENCE LEVEL
BANK_TOL = 0.3                                  # the variants are trimmed to within this of it (VOLUME is 0.17 dB a step)

ORIGINAL = {    # slot 3 as it was: PDEF defaults + PF_DUAL_SAW {MODE DUAL, DETUNE 60, OSC2 OFF, CUTOFF 70, SPREAD 110}
    "O1_WAVE": 1, "O1_PW": 64, "O1_LVL": 110, "NOISE": 0, "O2_WAVE": 0, "O2_PW": 64, "O2_LVL": 100,
    "O2_SEMI": 24, "SYNC": 0, "XMOD": 0, "ENV_O2": 64, "O2_FINE": 70, "CUTOFF": 70, "RESO": 20,
    "FENV_AMT": 90, "KEYTRK": 64, "FTYPE": 4, "DRIVE": 0, "VEL_FLT": 40, "VEL_AMP": 60, "FA": 20, "FD": 70,
    "FS": 40, "FR": 60, "AA": 10, "AD": 70, "AS": 100, "AR": 60, "LFO_SHAPE": 0, "LFO_RATE": 70,
    "LFO_DELAY": 0, "LFO_PHASE": 1, "LFO_PITCH": 0, "LFO_PWM": 0, "LFO_FLT": 0, "LFO_AMP": 0,
    "LFO_PITCH_TO": 2, "LFO_PWM_TO": 2, "MODE": 1, "UNI_N": 4, "UNI_DET": 60, "GLIDE": 0, "VINTAGE": 30,
    "SPREAD": 110, "BEND": 2, "VOLUME": 100, "MOD_DEPTH": 0, "ARP_MODE": 0, "ARP_DIV": 3, "ARP_OCT": 1,
    "ARP_GATE": 64, "FMORPH": 0, "GRL_BIAS": 40, "GRL_TONE": 50, "GROWL": 0, "DLY_TIME": 3, "DLY_FB": 50,
    "DLY_TONE": 70, "DLY_MIX": 0, "REV_SIZE": 80, "REV_DAMP": 60, "REV_PRE": 20, "REV_MIX": 0, "POLY_N": 5,
    "CHEW": 0, "TP_WOWFLT": 64, "TP_HISS": 64, "TP_DROPS": 64, "ALLEY": 0, "ALLEY_FINE": 0,
    "BBD_SPREAD": 127,
}

# the moves shared by B..F (decided in the measured pre-round, see 03-half-life.md): weight, bite, the window, the slop
BODY = {"O2_WAVE": 1, "O2_SEMI": 12, "O2_LVL": 80,                    # a sub-octave saw under the pair: the body pole
        "CUTOFF": 76, "RESO": 30, "FENV_AMT": 96,                     # a little more bite (the attitude pole)
        "POLY_N": 6}                                                  # three-note stabs (6 cards) no longer steal
SPUTTER = {"LFO_SHAPE": 3, "LFO_RATE": 119, "LFO_DELAY": 19, "LFO_AMP": 100, "AR": 62}   # square-gating VCA, fades in
CENTRE = {**BODY, **SPUTTER, "VINTAGE": 90}

VARIANTS = [   # (key, file tag, one-line description, changes over ORIGINAL; VOLUME is trimmed by the run)
    ("A", "original", "the nearest-base patch as it stood (dual saws, VINTAGE 30)", {}),
    ("B", "centre", "the brief's first reading: sub saw under the pair, VINTAGE 90, VCA gate-chop fading in", dict(CENTRE)),
    ("C", "unstable", "B pushed along axis 1: VINTAGE at the knob's top, wider pair", {**CENTRE, "VINTAGE": 127, "UNI_DET": 72}),
    ("D", "stable", "B pulled back along axis 1: tight pair, little slop", {**CENTRE, "VINTAGE": 55, "UNI_DET": 48}),
    ("E", "hardspit", "B pushed along axis 2: deeper, faster, staggered chop with filter bite",
     {**CENTRE, "LFO_AMP": 125, "LFO_RATE": 124, "AR": 68, "LFO_PHASE": 2, "LFO_FLT": 40}),
    ("F", "cleanchop", "B pulled back along axis 2: no sputter at all, a hard clean chop",
     {**BODY, "VINTAGE": 90, "AR": 50}),
]

NAMES = {"O2_WAVE": ["OFF", "SAW", "PULSE", "SAW+PLS"], "MODE": ["POLY", "DUAL", "UNISON", "MONO"],
         "LFO_SHAPE": ["TRI", "SAW", "RAMP", "SQUARE", "S&H", "RANDOM"], "LFO_PHASE": ["SYNC", "FREE", "SPREAD"]}


def unit(k, v):
    """a value in its own units for the echo rule: ms / Hz / Hz of cutoff / semitones where the panel shows them"""
    if k in ("AR", "FR", "AA", "FA", "FD", "AD"):
        return f"{0.5 * 20000 ** (v / 127):.0f} ms"
    if k == "LFO_RATE":
        return f"{0.05 * 600 ** (v / 127):.1f} Hz"
    if k == "LFO_DELAY":
        return f"{5000 * (v / 127) ** 2:.0f} ms"
    if k == "CUTOFF":
        return f"{440 * 2 ** ((v + 8 - 69) / 12):.0f} Hz"
    return ""


def change(k, old, new):
    """one change, echo rule: name old -> new, in the control's own terms and as % of its full range"""
    if k in NAMES:
        return f"{k} {NAMES[k][old]} -> {NAMES[k][new]}"
    u0, u1 = unit(k, old), unit(k, new)
    us = f" ({u0} -> {u1})" if u0 else ""
    if k == "O2_SEMI":
        return f"O2_SEMI {old - 24:+d} -> {new - 24:+d} st"
    if k in ("FENV_AMT", "O2_FINE", "ENV_O2"):
        return f"{k} {old} -> {new} (centre 64: {old - 64:+d} -> {new - 64:+d}, {100 * (new - old) / 127:+.0f}% of range)"
    if k == "POLY_N":
        return f"POLY_N {old} -> {new} voices"
    return f"{k} {old} -> {new} ({100 * (new - old) / 127:+.0f}%){us}"


def trim_volume(exe, params, target=BANK_REF):
    """the VOLUME byte (square law, ~0.17 dB a step) whose RMS on phrase (b) is closest to the target"""
    v = 100
    best = None
    for _ in range(6):
        p = {**params, "VOLUME": v}
        a, _ = K.render(exe, "b_stabs", params=p, tag="trim")
        r = K.level_metrics(a, "b_stabs")["rms"]
        if best is None or abs(r - target) < abs(best[1] - target):
            best = (v, r)
        if abs(r - target) < 0.1:
            break
        nv = int(round(v * 10 ** ((target - r) / 40)))
        v = max(1, min(127, nv if nv != v else v + (1 if target > r else -1)))
    return best[0], best[1]


def measure(exe, cg, params, tag):
    """render the three phrases (returned for the WAVs) and all the numbers"""
    wavs, m = {}, {}
    for ph in K.AUDITION:
        extra = ["3000 vlog 1", "5400 vlog 0"] if ph == "c_held" else ()
        a, out = K.render(exe, ph, params=params, extra=extra, tag="m_" + tag)
        wavs[ph] = a
        m[ph] = K.level_metrics(a, ph)
        if ph == "c_held":
            vl = K.vlog_parse(out)
            m["vlog"] = {str(c): v for c, v in vl.items()}
    b, c, ar = wavs["b_stabs"], wavs["c_held"], wavs["a_riff"]
    m["tone_b"] = K.tone_metrics(b, "b_stabs")
    m["tone_a"] = K.tone_metrics(ar, "a_riff")
    m["beat"] = K.beat_metrics(c, 110.0, 3800, 5400)
    m["rel_long"] = K.release_metrics(c, 5400, win_ms=900)
    m["rel_a3"] = K.release_metrics(c, 8120, win_ms=600)
    m["rel_a2s"] = K.release_metrics(c, 9350, win_ms=600)
    m["flutter"] = K.body_flutter(c, 3800, 5300)
    m["step_db"] = {ph: 20 * np.log10(np.abs(np.diff(wavs[ph], axis=0)).max() / 32767) for ph in K.AUDITION}   # gate "clicks"
    m["clip"] = int(sum((np.abs(wavs[ph]) >= 32767).sum() for ph in K.AUDITION))
    e, _ = K.env_db(c, 2.0, 2 * 1000 / 110)
    m["tail_env"] = {"long": e[int(5400 / 2) - 20:int(5400 / 2) + 230].tolist(),
                     "a2s": e[int(9350 / 2) - 20:int(9350 / 2) + 230].tolist()}
    m["cost_b"], m["cost_load"] = K.cost(cg, params=params, tag=tag)
    return wavs, m


def plot_tails(path, results):
    """the release tails (envelope dB re the level before release), the long note and the 150 ms note, all variants"""
    W, H, L, R, T, B = 900, 700, 60, 20, 30, 40
    im = Image.new("RGB", (W, H), (250, 250, 248))
    d = ImageDraw.Draw(im)
    cols = {"A": (90, 90, 90), "B": (30, 90, 200), "C": (200, 40, 40), "D": (40, 150, 70), "E": (200, 110, 0), "F": (140, 60, 170)}
    for panel, (key, title) in enumerate((("long", "release of the 2.4 s held A2 (ms after note-off)"),
                                          ("a2s", "release of the 150 ms A2 (ms after note-off)"))):
        y0 = 10 + panel * (H // 2)
        h = H // 2 - T - B
        X = lambda ms: L + (ms + 40) / 440 * (W - L - R)
        Y = lambda db: y0 + T + (0 - db) / 70 * h
        d.text((L, y0 + 8), title, fill=(20, 20, 20))
        for db in range(0, -71, -10):
            d.line([(L, Y(db)), (W - R, Y(db))], fill=(225, 225, 222))
            d.text((10, Y(db) - 6), f"{db}", fill=(90, 90, 90))
        for ms in range(0, 401, 50):
            d.text((X(ms) - 8, y0 + T + h + 6), f"{ms}", fill=(90, 90, 90))
        d.line([(X(0), y0 + T), (X(0), y0 + T + h)], fill=(180, 180, 180))
        for i, (k, r) in enumerate(results.items()):
            e = np.array(r["tail_env"][key])
            pre = e[:20].mean() if False else 10 * np.log10(np.mean(10 ** (e[5:20] / 10)))
            pts = [(X((j - 20) * 2), Y(max(-70, v - pre))) for j, v in enumerate(e)]
            d.line(pts, fill=cols[k], width=2)
            d.text((W - R - 190, y0 + T + 6 + 14 * i), f"{k} {r['tag']}", fill=cols[k])
    im.save(path)


def md_tables(results):
    ks = list(results)
    L = []
    row = lambda name, f: L.append("| " + name + " | " + " | ".join(f(results[k]) for k in ks) + " |")
    L.append("| | " + " | ".join(f"**{k}** {results[k]['tag']}" for k in ks) + " |")
    L.append("|---|" + "---|" * len(ks))
    row("VOLUME (trim)", lambda r: str(r["volume"]))
    row("RMS (b, note-on) dBFS", lambda r: f"{r['b_stabs']['rms']:.1f}")
    row("vs reference −18.0", lambda r: f"{r['b_stabs']['rms'] - BANK_REF:+.1f}")
    row("K-weighted RMS (b)", lambda r: f"{r['b_stabs']['rms_k']:.1f}")
    row("peak (b) dBFS", lambda r: f"{r['b_stabs']['peak']:.1f}")
    row("RMS riff (a) / held (c)", lambda r: f"{r['a_riff']['rms']:.1f} / {r['c_held']['rms']:.1f}")
    row("peak riff / held", lambda r: f"{r['a_riff']['peak']:.1f} / {r['c_held']['peak']:.1f}")
    row("centroid Hz (b stabs)", lambda r: f"{r['tone_b']['centroid']:.0f}")
    row("centroid Hz (a riff)", lambda r: f"{r['tone_a']['centroid']:.0f}")
    row("low share < 150 Hz (b / a)", lambda r: f"{r['tone_b']['low_share']:.0f}% / {r['tone_a']['low_share']:.0f}%")
    row("pair detune, DETUNE law (cents)", lambda r: f"{(r['params']['UNI_DET'] ** 2 // 64) * 100 / 256:.1f}")
    row("beat at A2 (Hz, mean [min–max])", lambda r: f"{r['beat']['rate_mean']:.2f} [{r['beat']['rate_min']:.2f}–{r['beat']['rate_max']:.2f}]")
    row("beat depth (dB p-p)", lambda r: f"{r['beat']['depth_db']:.0f}")
    row("card offsets, static (cents)", lambda r: " / ".join(f"{v[0]:+.1f}" for v in r["vlog"].values()))
    row("wander sd (cents, per card)", lambda r: " / ".join(f"{v[1]:.1f}" for v in r["vlog"].values()))
    row("wander range (cents, per card)", lambda r: " / ".join(f"{v[2]:+.0f}..{v[3]:+.0f}" for v in r["vlog"].values()))
    for lab, key in (("2.4 s note", "rel_long"), ("150 ms note", "rel_a2s")):
        row(f"release {lab}: −20 / −40 / −60 dB (ms)",
            lambda r, key=key: f"{r[key]['first20']:.0f} / {r[key]['first40']:.0f} / {r[key]['last60']:.0f}")
        row(f"sputter {lab}: climb dB · re-rises · span ms",
            lambda r, key=key: f"{r[key]['climb_db']:.0f} · {r[key]['rerises']} · {max(r[key]['span40'], 0):.0f}")
    row("largest sample step dBFS (riff / stabs / held)", lambda r: " / ".join(f"{r['step_db'][p]:.0f}" for p in K.AUDITION))
    row("clipped samples (all phrases)", lambda r: str(r["clip"]))
    row("body flutter (s.d. dB, held A2)", lambda r: f"{r['flutter'][0]:.1f}")
    row("cost: host instr/sample, phrase (b)", lambda r: f"{r['cost_b']:.0f}")
    row("cost under load (4 notes, 8 cards wanted)", lambda r: f"{r['cost_load']:.0f}")
    return "\n".join(L)


def main():
    base = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(K.BUILD, "base"))
    exe = K.build_host()
    cg = K.callgrind_exe()
    # 0. the A mechanism: the original list over INIT == the pre-change firmware's own slot 3, bit for bit
    old = K.build_host(base, os.path.join(K.BUILD, "obervave_base"))
    proof = {}
    for ph in K.AUDITION:
        a, _ = K.render(old, ph, program=2, tag="proofa")
        b, _ = K.render(exe, ph, params=ORIGINAL, tag="proofb")
        proof[ph] = bool((a == b).all())
    print("A proof (pre-change slot 3 == ORIGINAL over INIT, bit for bit):", proof)
    assert all(proof.values()), "the original list does not reproduce slot 3"

    results = {}
    os.makedirs(OUT, exist_ok=True)
    for key, tag, desc, ch in VARIANTS:
        params = {**ORIGINAL, **ch}
        if key == "A":
            vol, rms = 100, None
        else:
            vol, rms = trim_volume(exe, params)
        params["VOLUME"] = vol
        wavs, m = measure(exe, cg, params, key)
        for ph, short in (("a_riff", "riff"), ("b_stabs", "stabs"), ("c_held", "held")):
            K.write_wav(os.path.join(OUT, f"{key}_{tag}_{short}.wav"), wavs[ph][int(K.T_CUT * K.FS):])
        m.update(tag=tag, desc=desc, volume=vol, params=params,
                 changes=[change(k, ORIGINAL[k], v) for k, v in params.items() if v != ORIGINAL[k]])
        results[key] = m
        print(f"{key} {tag:10s} VOLUME {vol:3d}  RMS(b) {m['b_stabs']['rms']:6.1f}  peak {m['b_stabs']['peak']:5.1f}  "
              f"centroid {m['tone_b']['centroid']:4.0f}  beat {m['beat']['rate_mean']:.2f} Hz  sputter(150ms) climb "
              f"{m['rel_a2s']['climb_db']:.0f}  cost {m['cost_b']:.0f}/{m['cost_load']:.0f}")
    plot_tails(os.path.join(OUT, "release.png"), results)
    with open(os.path.join(OUT, "results.json"), "w") as f:
        json.dump({k: {kk: vv for kk, vv in r.items() if kk != "tail_env"} for k, r in results.items()}, f, indent=1)
    with open(os.path.join(OUT, "numbers.md"), "w") as f:
        f.write("# generated by tests/voicing/half_life.py -- the numbers; README.md has the reading\n\n")
        for k, r in results.items():
            f.write(f"**{k} {r['tag']}** — {r['desc']}\n\n" + ("\n".join(f"- {c}" for c in r["changes"]) or "- (none: the original)")
                    + "\n\n")
        f.write(md_tables(results) + "\n")
    print(md_tables(results))


if __name__ == "__main__":
    main()
