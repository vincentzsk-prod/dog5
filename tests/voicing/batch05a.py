#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Voicing round for Batch 5A, Chapter III "the drones": 18 Roto-scopo, 19 Blackwater, 22 Melting Orb.

  python3 tests/voicing/batch05a.py [base_tree] [--only SLOT] [--quick] [--no-cost] [--no-wav]
  python3 tests/voicing/batch05a.py --emit SLOT KEY      the C array of a variant (from results.json)

Same method as batch04b.py: a variant is a FULL parameter list (the resolved original + the variant's changes); A is rendered through the base firmware's own program path, B..D over INIT;
VOLUME is trimmed last to -18.0 dBFS RMS on the patch's own HELD-note window (settled state: see batch05a_variants.py `win`), peak <= -4 over every phrase.  A drone is judged on a held key, so
the measures are time-windowed.  Output: listen/voicing/batch-05a/<NN-name>/ (README.md + results.json on the merged voicing branch; WAVs only on the never-merged listen branch)."""
import json
import os
import re
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import batch01a as B
import batch02a_metrics as M
import batch03a_metrics as N
import batch04a as A
import batch04a_metrics as Q
from batch05a_variants import PATCHES

OUT = os.path.join(K.ROOT, "listen", "voicing", "batch-05a")
FS = K.FS
REF = -18.0
SHORT = {"a_riff": "riff", "b_stabs": "stabs", "c_held": "held", "v_drone_lo": "drone-A1", "v_drone_mid": "drone-A2", "w_chord_lo": "chord-low", "w_chord_mid": "chord-mid", "y_tap": "taps"}
NOTE_NAME = {21: "A0", 33: "A1", 45: "A2", 57: "A3"}
BANDS = ("<60", "60-150", "150-400", "400-1.2k", "1.2k+")


def _s(ms):
    return int(round(ms * FS / 1000))


def krms(a, t0, t1):
    """K-weighted RMS dBFS over [t0, t1] ms (informational)"""
    seg = a[_s(t0):_s(t1)]
    k = np.stack([K.k_weight(seg[:, 0]), K.k_weight(seg[:, 1])], 1)
    return float(10 * np.log10(max((k ** 2).mean(), 1e-12) / 32767 ** 2))


def wins(a, t0, t1):
    """one window: level, centroid, band shares, MUD (= share 150-400 / share 1.2k+)"""
    w = Q.window_split(a, t0, t1)
    return {"rms": M.rms_db(a, t0, t1), "cent": w["cent"], "shares": w["shares"], "mud": w["mud"]}


def pitch_track(a, f0, t0_ms, t1_ms, win_ms=400, hop_ms=500, lo=0.35, hi=1.25, nh=4):
    """the dominant fundamental by harmonic summation over a log-spaced candidate grid, in cents re f0, per window (a unison stack with a sinking OSC 2: one common pitch)"""
    x = a.mean(1)
    N_ = 1 << 16
    f = np.fft.rfftfreq(N_, 1 / FS)
    cands = f0 * 2 ** np.linspace(np.log2(lo), np.log2(hi), 1400)
    out = []
    for t in range(int(t0_ms), int(t1_ms), hop_ms):
        s, w = _s(t), _s(win_ms)
        seg = x[s:s + w]
        if len(seg) < w:
            break
        P = np.abs(np.fft.rfft(seg * np.hanning(w), N_))
        sc = [sum(np.interp(c * h, f, P) for h in range(1, nh + 1)) for c in cands]
        out.append(1200 * np.log2(cands[int(np.argmax(sc))] / f0))
    return np.array(out)


def host_run(exe, tag, lines):
    """run a host script, return (audio, stdout)"""
    lines = sorted(lines, key=lambda l: int(l.split()[0]) if not l.endswith(" end") else 10 ** 9)
    sp = os.path.join(K.BUILD, tag + ".txt")
    open(sp, "w").write("\n".join(lines) + "\n")
    r = subprocess.run([exe, os.path.join(K.BUILD, tag), sp], cwd=K.ROOT, check=True, capture_output=True, text=True, errors="replace")
    for p in os.listdir(K.BUILD):
        if p.endswith(".ppm"):
            os.unlink(os.path.join(K.BUILD, p))
    return K.read_wav(os.path.join(K.BUILD, tag + ".wav")), r.stdout


def probe_lines(params, notes, end_ms):
    return [f"{K.T_SELECT} midi 0xC0 {K.INIT_PROGRAM} 0"] + [f"{K.T_PARAMS} param {K.PARAM_IDS[k]} {v}" for k, v in params.items()] + notes + [f"{end_ms} end"]


def vlog_slop(exe, params, note=33):
    """the engine's own per-card vintage pitch (cents) over a note held 13 s: {card: (static offset, s.d., lo, hi)}"""
    _, out = host_run(exe, "vl5", probe_lines(params, [f"3000 midi 0x90 {note} 100", "4000 vlog 1", "16000 vlog 0", "16100 midi 0x80 %d 0" % note], 17000))
    return K.vlog_parse(out)


def chord_voices(exe, params, keys, at_ms=4000):
    """cards gated on after the keys are struck together (the host's `expect voices`)"""
    notes = [f"3000 midi 0x90 {n} 100" for n in keys] + [f"{at_ms} expect voices 99"]
    try:
        _, out = host_run(exe, "cv5", probe_lines(params, notes, at_ms + 100))
    except subprocess.CalledProcessError as e:
        out = e.stdout or ""
    m = re.search(r"expect voices 99: (\d+) gated on", out)
    return int(m[1]) if m else None


def selfosc(exe, params, resos=(0, 127)):
    """does the filter sing by itself?  NOISE-fed, the oscillators off, 12 dB apart in the input: diff 12 = linear, near 0 = self-oscillation (note A2, the patch's own cutoff / key tracking)"""
    return N.selfosc_probe(exe, params, resos=resos)


def tap_block(a, on_list=(3000, 6000, 9000), gate=150, settled=None):
    """what a short tap does: for each tap the RMS over the 150 ms gate, the peak of the first 400 ms, the centroid over the gate, and the level 400 ms after the key-up"""
    out = []
    for t in on_list:
        out.append({"gate_rms": M.rms_db(a, t, t + gate), "peak": M.peak_db(a, t, t + 400), "cent": M.centroid(a, t, t + gate, nfft=2048),
                    "tail400": M.rms_db(a, t + gate + 350, t + gate + 450), "tail1500": M.rms_db(a, t + gate + 1450, t + gate + 1550)})
    return out


# ---- the common block ------------------------------------------------------------------------------------------------------------------------
class Ctx:
    def __init__(self, exe, old, spec, key, params):
        self.exe, self.old, self.spec, self.key, self.p = exe, old, spec, key, params
        self.cache = {}

    def rend(self, phrase, vol=None):
        k = (phrase, vol)
        if k not in self.cache:
            if self.key == "A":
                self.cache[k] = K.render(self.old, phrase, program=self.spec["slot"] - 1, tag="m5")[0]
            else:
                p = self.p if vol is None else {**self.p, "VOLUME": vol}
                self.cache[k] = K.render(self.exe, phrase, params=p, tag="m5")[0]
        return self.cache[k]


def level_of(a, spec):
    return M.rms_db(a, spec["on"] + spec["win"][0], spec["on"] + spec["win"][1])


def trim(exe, spec, params):
    """the VOLUME (square law, ~0.17 dB a step) whose HELD-window reading is closest to -18.0; then down while any phrase peaks above -4.3 (never below -19.5)"""
    v = params.get("VOLUME", 100)
    best = None
    for _ in range(9):
        a, _ = K.render(exe, spec["level"], params={**params, "VOLUME": v}, tag="trim5")
        r = level_of(a, spec)
        if best is None or abs(r - REF) < abs(best[1] - REF):
            best = (v, r)
        if abs(r - REF) < 0.12:
            break
        nv = int(round(v * 10 ** ((REF - r) / 40)))
        v = max(1, min(127, nv if nv != v else v + (1 if REF > r else -1)))
    return best


def peak_all(exe, spec, params):
    return max(M.peak_db(K.render(exe, ph, params=params, tag="pk5")[0]) for ph in spec["phrases"])


def common(ctx, m):
    spec = ctx.spec
    lp = spec["level"]
    a = ctx.rend(lp)
    on = spec["on"]
    w0, w1 = on + spec["win"][0], on + spec["win"][1]
    m["level"] = M.rms_db(a, w0, w1)
    m["krms"] = krms(a, w0, w1)
    m["first_s"] = M.rms_db(a, on, on + 1000)
    m["whole_hold"] = M.rms_db(a, on, on + 15000)
    m["b"] = K.level_metrics(ctx.rend("b_stabs"), "b_stabs")["rms"]
    pk = {ph: M.peak_db(ctx.rend(ph)) for ph in spec["phrases"]}
    m["peaks"] = pk
    m["peak_all"] = max(pk.values())
    m["clip"] = int(sum((np.abs(ctx.rend(ph)) >= 32767).sum() for ph in spec["phrases"]))
    m["settled"] = wins(a, w0, w1)
    m["taps"] = tap_block(ctx.rend("y_tap"))
    m["tap_vs_settled"] = [t["gate_rms"] - m["level"] for t in m["taps"]]
    ch = spec["chord"]
    keys = (33, 40, 45) if ch.endswith("lo") else (45, 52, 57)
    m["chord_voices"] = chord_voices(ctx.exe, ctx.p, keys)
    ac = ctx.rend(ch)
    m["chord"] = {"rms": M.rms_db(ac, 5000, 10500), "peak": M.peak_db(ac), "cent": M.centroid(ac, 5000, 10500, nfft=2048)}
    return m


# ---- 18 Roto-scopo: the wander ---------------------------------------------------------------------------------------------------------------
def measure_18(ctx, m):
    spec = ctx.spec
    for nm, ph in (("A1", "v_drone_lo"), ("A2", "v_drone_mid")):
        a = ctx.rend(ph)
        t = list(range(2000, 14500, 500))
        c = np.array([M.centroid(a, 3000 + x, 3000 + x + 500, nfft=2048) for x in t])
        r = np.array([M.rms_db(a, 3000 + x, 3000 + x + 500) for x in t])
        m["wander_" + nm] = {"cent_min": float(c.min()), "cent_max": float(c.max()), "cent_range": float(c.max() - c.min()), "cent_sd": float(c.std()), "cent_mean": float(c.mean()),
                              "log2_range_st": float(12 * np.log2(c.max() / c.min())), "rms_sd": float(r.std()), "rms_range": float(r.max() - r.min()), "series": [round(float(x)) for x in c],
                              "windows": len(t)}
        m["windows_" + nm] = {f"{x // 1000}-{y // 1000}s": wins(a, 3000 + x, 3000 + y) for x, y in ((0, 1000), (2000, 5000), (5000, 10000), (10000, 14000))}
        m["release_" + nm] = M.tail_times(a, 18000, 150, 4000)
    m["slop"] = vlog_slop(ctx.exe, ctx.p)
    m["selfosc"] = selfosc(ctx.exe, ctx.p)
    return m


# ---- 19 Blackwater: where it is heard ---------------------------------------------------------------------------------------------------------
def measure_19(ctx, m):
    reg = {}
    for n in (21, 33, 45, 57):
        a, _ = host_run(ctx.exe, "reg5", probe_lines(ctx.p, [f"3000 midi 0x90 {n} 100", "9000 midi 0x80 %d 0" % n], 9800))
        w = wins(a, 5000, 9000)
        sh = w["shares"]
        reg[NOTE_NAME[n]] = {"rms": w["rms"], "krms": krms(a, 5000, 9000), "peak": M.peak_db(a), "shares": sh, "cent": w["cent"],
                             "above60": 100 - sh["<60"], "above150": sh["150-400"] + sh["400-1.2k"] + sh["1.2k+"]}
    m["register"] = reg
    for nm, ph in (("A1", "v_drone_lo"), ("A2", "v_drone_mid")):
        a = ctx.rend(ph)
        m["windows_" + nm] = {f"{x // 1000}-{y // 1000}s": wins(a, 3000 + x, 3000 + y) for x, y in ((0, 1000), (1000, 3000), (3000, 6000), (6000, 10000), (10000, 14000))}
        m["release_" + nm] = M.tail_times(a, 18000, 150, 4000)
    m["selfosc"] = selfosc(ctx.exe, ctx.p)
    return m


# ---- 22 Melting Orb: the melt ----------------------------------------------------------------------------------------------------------------
def measure_22(ctx, m):
    a = ctx.rend("v_drone_mid")
    f0 = 110.0
    ts = list(range(0, 8000, 500))
    cent = np.array([M.centroid(a, 3000 + t, 3000 + t + 500, nfft=2048) for t in ts])
    rms = np.array([M.rms_db(a, 3000 + t, 3000 + t + 500) for t in ts])
    pt = pitch_track(a, f0, 3000, 13000, win_ms=400, hop_ms=500)
    fin_p = float(pt[-5:].mean())                                   # 8.0-13.0 s
    fin_c = float(np.mean([M.centroid(a, 3000 + t, 3000 + t + 500, nfft=2048) for t in range(9000, 14000, 500)]))
    cfull = np.array([M.centroid(a, 3000 + t, 3000 + t + 500, nfft=2048) for t in range(0, 12000, 500)])

    def first(series, frac, start, final, log=False):
        for i, v in enumerate(series):
            x, s, f = (np.log(v), np.log(start), np.log(final)) if log else (v, start, final)
            if abs(x - f) <= (1 - frac) * abs(s - f):
                return (i + 1) * 0.5                                  # the end of that 0.5 s window
        return None

    m["melt"] = {"t": [t / 1000 for t in ts], "cent": [round(float(x)) for x in cent], "rms": [round(float(x), 1) for x in rms], "pitch_cents": [round(float(x)) for x in pt[:16]],
                 "pitch_final": fin_p, "cent_final": fin_c, "cent_start": float(cent[0]),
                 "pitch_t90": first(pt, 0.9, 0.0, fin_p), "pitch_t98": first(pt, 0.98, 0.0, fin_p),
                 "cent_t90": first(cfull, 0.9, float(cfull[0]), fin_c, log=True), "cent_t98": first(cfull, 0.98, float(cfull[0]), fin_c, log=True),
                 "centroid_drop_st": float(12 * np.log2(cent[0] / fin_c)), "formula_st": (ctx.p["ENV_O2"] - 64) * 24 / 63 if ctx.key != "A" else None}
    m["windows"] = {f"{x}-{y}s": wins(a, 3000 + x * 1000, 3000 + y * 1000) for x, y in ((0, 1), (1, 3), (3, 6), (6, 8), (9, 14))}
    # the key-up: does the pitch / brightness snap back?
    m["release"] = {"tail": M.tail_times(a, 18000, 150, 4000), "pitch": [round(float(x)) for x in pitch_track(a, f0, 18000, 21000, win_ms=400, hop_ms=500)],
                    "cent": [round(float(M.centroid(a, 18000 + t, 18000 + t + 500, nfft=2048))) for t in range(0, 3000, 500)]}
    m["selfosc"] = selfosc(ctx.exe, ctx.p)
    return m


MEASURE = {18: measure_18, 19: measure_19, 22: measure_22}


def measure(exe, old, cg, spec, key, params, vol, no_cost, no_wav, orig_path=None):
    ctx = Ctx(exe, old, spec, key, params)
    m = {}
    m = common(ctx, m)
    m = MEASURE[spec["slot"]](ctx, m)
    m["cost"] = None
    if not no_cost:
        cb, cl = K.cost(cg, params=params, tag=f"{spec['slot']}{key}")
        ir, fr = K.callgrind_ips(cg, "x_stress", params=params, tag=f"{spec['slot']}{key}i", notes=False)
        m["cost"] = {"b": cb, "load": cl, "idle": ir / fr}
    return ctx, m


def run(spec, base, no_cost, no_wav, quick):
    exe = K.build_host()
    cg = None if no_cost else K.callgrind_exe()
    old = K.build_host(base, os.path.join(K.BUILD, "obervave_base"))
    orig = B.resolve(base, spec["slot"])
    d = os.path.join(OUT, spec["dir"])
    os.makedirs(d, exist_ok=True)
    R, ctxs = {}, {}
    todo = [(k, tag, desc, ch) for k, tag, desc, ch in spec["variants"]]
    for key, tag, desc, ch in todo:
        params = dict(orig) if key == "A" else {**orig, **ch}
        if key != "A":
            vol, r = trim(exe, spec, params)
            params["VOLUME"] = vol
            while peak_all(exe, spec, params) > -4.0 and params["VOLUME"] > 1:
                params["VOLUME"] -= 1
            vol = params["VOLUME"]
        else:
            vol = orig["VOLUME"]
        ctx, m = measure(exe, old, cg, spec, key, params, vol, no_cost, no_wav)
        m["volume"], m["params"], m["tag"], m["desc"] = vol, params, tag, desc
        R[key], ctxs[key] = m, ctx
        print(f"{spec['slot']:02d}{key} VOL {vol:3d} lvl {m['level']:6.2f} k {m['krms']:6.2f} (b) {m['b']:6.2f} pk {m['peak_all']:6.2f} chord-voices {m['chord_voices']}"
              + (f" cost {m['cost']['idle'] + m['cost']['load']:.0f}" if m["cost"] else ""), flush=True)
    # A matched to the reference by VOLUME alone (listening aid: same tone as the original, level of the others)
    pa = dict(orig)
    va, ra = trim(exe, spec, pa)
    pa["VOLUME"] = va
    R["A*"] = {"volume": va, "level": ra, "params": pa, "desc": "the original's tone with VOLUME alone moved onto the reference (a listening aid, not a candidate)", "tag": "original-matched",
               "peak_all": peak_all(exe, spec, pa)}
    print(f"{spec['slot']:02d}A* VOL {va} lvl {ra:.2f} pk {R['A*']['peak_all']:.2f}")
    if not no_wav:
        for key in R:
            for ph in spec["phrases"]:
                if key == "A*":
                    a = K.render(exe, ph, params=R[key]["params"], tag="wavA")[0]
                else:
                    a = ctxs[key].rend(ph)
                K.write_wav(os.path.join(d, f"{spec['dir']}_{key}_{SHORT[ph]}.wav"), a[int(K.T_CUT * FS):])
    return R


def jdefault(o):
    return A.jdefault(o)


def main():
    argv = sys.argv[1:]
    no_cost, no_wav, quick = "--no-cost" in argv, "--no-wav" in argv, "--quick" in argv
    only = int(argv[argv.index("--only") + 1]) if "--only" in argv else None
    if "--emit" in argv:
        i = argv.index("--emit")
        slot, key = int(argv[i + 1]), argv[i + 2]
        spec = next(s for s in PATCHES if s["slot"] == slot)
        res = json.load(open(os.path.join(OUT, spec["dir"], "results.json")))
        print(B.emit(spec["cname"], res[key]["params"]))
        return
    pos = [a for a in argv if not a.startswith("--") and not a.isdigit()]
    base = os.path.abspath(pos[0]) if pos else os.path.join(K.BUILD, "base")
    if "--report" in argv:                      # rewrite the READMEs from results.json (no renders)
        from batch05a_report import write_all
        for spec in PATCHES:
            d = os.path.join(OUT, spec["dir"])
            write_all(spec, json.load(open(os.path.join(d, "results.json"))), d, B.resolve(base, spec["slot"]))
        return
    for spec in PATCHES:
        if only and spec["slot"] != only:
            continue
        R = run(spec, base, no_cost, no_wav, quick)
        d = os.path.join(OUT, spec["dir"])
        json.dump(R, open(os.path.join(d, "results.json"), "w"), default=jdefault, indent=1)
        from batch05a_report import write_all
        write_all(spec, R, d, B.resolve(base, spec["slot"]))


if __name__ == "__main__":
    main()
