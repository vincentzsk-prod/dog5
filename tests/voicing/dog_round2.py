#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Round 2 for 30 THE DOG: B (the round-1 patch, the A/B anchor) and four variants E..H, rendered on phrases (e) low unison and (b) stabs,
measured (band split, level, spread / wander, centroid, snap, release, drive measures, CPU), with the drive-route ladders.

  python3 tests/voicing/dog_round2.py [--quick] [--emit KEY]

Output: listen/voicing/batch-01a/30-the-dog/round2/ (WAVs, README.md, numbers.md, drive_routes.md, results.json).  Every variant is a
FULL parameter list over INIT (voicekit.render(params=...)); B is read from the tree's slot 30 as it stands before the round."""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import dog_metrics as M
import batch01a as B1

OUT = os.path.join(K.ROOT, "listen", "voicing", "batch-01a", "30-the-dog", "round2")
REF, PRESENCE = -18.0, -16.5
LVL = "e_lowuni"

# B as committed in round 1 (the anchor); the variants are changes over it
B_CH = {}
E_CH = {"UNI_DET": 35, "O1_LVL": 114, "O2_LVL": 94, "CUTOFF": 102, "FENV_AMT": 88, "KEYTRK": 60, "FS": 38}
F_CH = {**E_CH, "DRIVE": 80}
G_CH = {**E_CH, "DRIVE": 110, "GROWL": 55, "GRL_BIAS": 70, "GRL_TONE": 70}
H_CH = {**E_CH, "DRIVE": 100, "CUTOFF": 104, "FS": 40}
VARIANTS = [
    ("B", "anchor", "round 1's B as committed (the A/B anchor, VOLUME 65 as it is)", B_CH, None),
    ("E", "fuller", "fuller + a bit wider (14.8 cents) + a touch brighter, no added drive", E_CH, REF),
    ("F", "warmdrive", "E plus the moderate warm-drive route found: per-voice DRIVE 80 (FILTER+ page), no GROWL", F_CH, REF),
    ("G", "edge", "F pushed to the edge of fuzzy: DRIVE 110 plus GROWL 55 (BIAS 70, TONE 70), where the crest falls 2.6 dB and the hash doubles", G_CH, REF),
    ("H", "presence", "my blend for flagship presence: E, per-voice DRIVE 100 (no GROWL: cheap and uncompressed), CUTOFF 104 / FS 40 to give back the top the drive takes, and the +1.5 dB presence level (-16.5 dBFS)", H_CH, PRESENCE),
]
SHORT = {"e_lowuni": "lowuni", "b_stabs": "stabs"}


def shares(bs):
    t = sum(bs.values())
    return {k: 100 * v / t for k, v in bs.items()}


def measure(exe, cg, params, tag, ref_bands, quick):
    out, wavs = {}, {}
    for ph in ("e_lowuni", "b_stabs"):
        extra = ["3000 vlog 1", "6100 vlog 0"] if ph == "e_lowuni" else ()
        a, so = K.render(exe, ph, params=params, extra=extra, tag="r2" + tag)
        wavs[ph] = a
        out[ph] = {**K.level_metrics(a, ph), **K.tone_metrics(a, ph), "bands": M.band_split(a, ph)}
        if ph == "e_lowuni":
            out["vlog"] = {str(c): v for c, v in K.vlog_parse(so).items()}
    e = wavs["e_lowuni"]
    out["held"] = B1.held_env(e, 3000, 6000, 55.0)
    out["snap_mean"] = M.held_snap(e, 3000, 6000)
    out["snap_chop"] = M.chop_snap(e)
    out["harm"] = M.harmonics(e, 3000, 6000)
    out["motion"] = M.motion(e, 3000, 6000)
    out["rel"] = K.release_metrics(B1.dc_free(e, 6000, 900), 6000, win_ms=900)
    out["peak_all"] = max(out[p]["peak"] for p in ("e_lowuni", "b_stabs"))
    out["beat"] = K.beat_metrics(e, 55.0, 3500, 5950, win_s=2.0)
    if not quick:
        out["cost_b"], out["cost_load"] = K.cost(cg, params=params, tag="r2" + tag)
        ir, fr = K.callgrind_ips(cg, "x_stress", params=params, tag="r2" + tag + "i", notes=False)
        out["cost_idle"] = ir / fr
    return wavs, out


def spread_cents(p):
    return 2 * (p["UNI_DET"] ** 2 >> 6) * 100 / 256


def routes(exe, base, tag="rt"):
    """the drive-route ladders on the E base at equal level: GROWL, per-voice DRIVE, BIAS; crest, hash, even/odd, centroid, peak, 150-400 / 400+ bands"""
    v0, _ = M.trim(exe, base, LVL, REF, tag=tag)
    a0, _ = K.render(exe, LVL, params={**base, "VOLUME": v0}, tag=tag)
    b0 = M.band_split(a0, LVL)
    rows = []

    def row(name, ch):
        p = {**base, **ch}
        v, _ = M.trim(exe, p, LVL, REF, tag=tag)
        a, _ = K.render(exe, LVL, params={**p, "VOLUME": v}, tag=tag)
        m, t, h = K.level_metrics(a, LVL), K.tone_metrics(a, LVL), M.harmonics(a, 3000, 6000)
        bs = M.band_split(a, LVL)
        db = {k: 10 * np.log10(bs[k] / b0[k]) for k in bs}
        rows.append((name, ch, v, m, t, h, db))
    row("E (no drive)", {})
    for d in (30, 70, 110, 127):
        row(f"DRIVE {d}", {"DRIVE": d})
    for g in (12, 22, 28, 40, 55, 70):
        row(f"GROWL {g} (BIAS 60, TONE 70)", {"GROWL": g, "GRL_BIAS": 60, "GRL_TONE": 70})
    for b in (0, 40, 70, 100):
        row(f"GROWL 28, BIAS {b}", {"GROWL": 28, "GRL_BIAS": b, "GRL_TONE": 70})
    return rows


def routes_md(rows):
    L = ["| route | VOLUME | peak (e) | crest dB | hash % | even/odd dB | centroid Hz | K−plain dB | band dB vs E: <60 / 60-150 / 150-400 / 400-1.2k / 1.2k+ |", "|---|---|---|---|---|---|---|---|---|"]
    for name, ch, v, m, t, h, db in rows:
        L.append(f"| {name} | {v} | {m['peak']:.1f} | {h['crest_db']:.1f} | {h['hash_pct']:.1f} | {h['even_odd_db']:+.1f} | {t['centroid']:.0f} | "
                 f"{m['rms_k'] - m['rms']:+.1f} | " + " / ".join(f"{x:+.1f}" for x in db.values()) + " |")
    return "\n".join(L)


def table(R, keys):
    L = []
    row = lambda name, f: L.append("| " + name + " | " + " | ".join(f(R[k]) for k in keys) + " |")
    L.append("| | " + " | ".join(f"**{k}** {R[k]['tag']}" for k in keys) + " |")
    L.append("|---|" + "---|" * len(keys))
    row("VOLUME (trim)", lambda r: str(r["volume"]))
    row("level target (dBFS RMS, phrase e)", lambda r: f"{r['target']:.1f}" if r["target"] else "as round 1")
    row("RMS (e) · vs reference −18.0", lambda r: f"{r['e_lowuni']['rms']:.1f} · {r['e_lowuni']['rms'] - REF:+.1f}")
    row("RMS (b) · vs reference", lambda r: f"{r['b_stabs']['rms']:.1f} · {r['b_stabs']['rms'] - REF:+.1f}")
    row("K-weighted RMS (e) · (b)", lambda r: f"{r['e_lowuni']['rms_k']:.1f} · {r['b_stabs']['rms_k']:.1f}")
    row("peak, e / b dBFS (limit ≤ −4)", lambda r: f"{r['e_lowuni']['peak']:.1f} / {r['b_stabs']['peak']:.1f}")
    for ph, lab in (("e_lowuni", "(e)"), ("b_stabs", "(b)")):
        row(f"band share {lab}: <60 / 60-150 / 150-400 / 400-1.2k / 1.2k+ %", lambda r, ph=ph: " / ".join(f"{v:.1f}" for v in shares(r[ph]["bands"]).values()))
        row(f"band dB vs B {lab}", lambda r, ph=ph, R=R: " / ".join(f"{10 * np.log10(r[ph]['bands'][k] / R['B'][ph]['bands'][k]):+.1f}" for k in r[ph]["bands"]))
    row("centroid Hz (e) · (b)", lambda r: f"{r['e_lowuni']['centroid']:.0f} · {r['b_stabs']['centroid']:.0f}")
    row("stack spread by the DETUNE law (cents)", lambda r: f"{spread_cents(r['params']):.1f}")
    row("wander s.d. per card (cents), 8 cards", lambda r: " / ".join(f"{v[1]:.1f}" for v in r["vlog"].values()))
    row("wander range (cents), widest card", lambda r: f"{min(v[2] for v in r['vlog'].values()):+.0f} .. {max(v[3] for v in r['vlog'].values()):+.0f}")
    row("inner motion of the 60-400 Hz band (s.d. · p-p dB)", lambda r: f"{r['motion'][0]:.2f} · {r['motion'][1]:.1f}")
    row("snap: held, last 110 ms body (round 1's reading)", lambda r: f"{r['held']['peak_over_body_db']:+.1f}")
    row("snap: held, whole-hold mean body (steadier)", lambda r: f"{r['snap_mean']:+.1f}")
    row("snap: eight chopped roots, mean / worst", lambda r: f"{r['snap_chop'][0]:+.1f} / {r['snap_chop'][1]:+.1f}")
    row("brightness at the attack → body (Hz)", lambda r: f"{r['held']['cent_peak']:.0f} → {r['held']['cent_body']:.0f}")
    row("release −20 / −60 dB (ms), with FX (none on)", lambda r: f"{r['rel']['first20']:.0f} / {r['rel']['last60']:.0f}")
    row("crest factor of the held body (dB)", lambda r: f"{r['harm']['crest_db']:.1f}")
    row("inter-harmonic hash (% of 150 Hz-8 kHz)", lambda r: f"{r['harm']['hash_pct']:.1f}")
    row("even / odd harmonic energy (dB)", lambda r: f"{r['harm']['even_odd_db']:+.1f}")
    if "cost_idle" in R["B"]:
        row("CPU idle + load = worst (host instr/sample)", lambda r: f"{r['cost_idle']:.0f} + {r['cost_load']:.0f} = {r['cost_idle'] + r['cost_load']:.0f}")
    return "\n".join(L)


def main():
    quick = "--quick" in sys.argv
    exe = K.build_host()
    cg = None if quick else K.callgrind_exe()
    b_params = B1.resolve(K.ROOT, 30)
    if "--emit" in sys.argv:
        key = sys.argv[sys.argv.index("--emit") + 1]
        R = json.load(open(os.path.join(OUT, "results.json")))
        print(B1.emit("THE_DOG", R[key]["params"]))
        return
    os.makedirs(OUT, exist_ok=True)
    R = {}
    for key, tag, desc, ch, target in VARIANTS:
        p = {**b_params, **ch}
        if target is None:
            vol = p["VOLUME"]
        else:
            vol, _ = M.trim(exe, p, LVL, target, tag="r2trim")
        p["VOLUME"] = vol
        wavs, m = measure(exe, cg, p, key, None, quick)
        if not quick:
            for ph, w in wavs.items():
                K.write_wav(os.path.join(OUT, f"{key}_{tag}_{SHORT[ph]}.wav"), w[int(K.T_CUT * K.FS):])
        m.update(tag=tag, desc=desc, volume=vol, params=p, target=target,
                 changes=[B1.change(k, b_params[k], v) for k, v in p.items() if v != b_params[k]])
        R[key] = m
        h = m["harm"]
        print(f"{key} {tag:10s} VOL {vol:3d} RMS e {m['e_lowuni']['rms']:.1f} b {m['b_stabs']['rms']:.1f} pk {m['peak_all']:.1f} cent {m['e_lowuni']['centroid']:.0f} "
              f"spread {spread_cents(p):.1f} snapM {m['snap_mean']:+.1f} chop {m['snap_chop'][0]:+.1f} rel60 {m['rel']['last60']:.0f} crest {h['crest_db']:.1f} hash {h['hash_pct']:.1f}"
              + (f" cpu {m['cost_idle'] + m['cost_load']:.0f}" if not quick else ""))
    if quick:
        return
    rows = routes(exe, {**b_params, **E_CH})
    with open(os.path.join(OUT, "drive_routes.md"), "w") as f:
        f.write("# Drive routes on the E base, each trimmed to −18.0 dBFS RMS on phrase (e)\n\n" + routes_md(rows) + "\n")
    with open(os.path.join(OUT, "results.json"), "w") as f:
        json.dump(R, f, indent=1, default=float)
    with open(os.path.join(OUT, "numbers.md"), "w") as f:
        f.write("# generated by tests/voicing/dog_round2.py\n\n")
        for k, r in R.items():
            f.write(f"**{k} {r['tag']}** — {r['desc']}\n\n" + ("\n".join(f"- {c}" for c in r["changes"]) or "- (none: the anchor)") + "\n\n")
        f.write(table(R, list(R)) + "\n")
    print(routes_md(rows))


if __name__ == "__main__":
    main()
