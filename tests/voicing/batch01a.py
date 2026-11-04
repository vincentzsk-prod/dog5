#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Voicing round for Batch 1A, "the attack set": 30 THE DOG, 31 Fi(l)fth, 04 V-Sync, 25 SAWTOOTH.

Renders each patch's variants on the audition phrases, level-matches them to the bank reference on the patch's LEVEL
phrase, measures them, and writes listen/voicing/batch-01a/<NN-name>/ (WAVs, README.md with the tables, results.json).

  python3 tests/voicing/batch01a.py [base_tree] [--only SLOT] [--quick]
        base_tree: the firmware exported from the commit before the batch (default build/voicing/base)
        --quick:   no WAVs, no callgrind (for tuning a variant table)

A variant is a FULL parameter list over INIT (voicekit.render(params=...)); the ORIGINAL ("A") is read from the base
tree's own patch resolver (dump_patch), so it can never drift from what the slot was.  The run proves that the original
list over INIT renders bit-identically to the base firmware's own slot (LFO phase pinned where an LFO free-runs)."""
import json
import os
import re
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K

OUT = os.path.join(K.ROOT, "listen", "voicing", "batch-01a")
BANK_REF = -18.0                                # dBFS RMS on the level phrase's note-on region
BANK_TOL = 0.3                                  # variants are trimmed to within this (VOLUME is 0.17 dB a step)
ID2N = {v: k for k, v in K.PARAM_IDS.items()}

WAVE = ["OFF", "SAW", "PULSE", "SAW+PLS"]
MODES = ["POLY", "DUAL", "UNISON", "MONO"]
NAMES = {"O1_WAVE": WAVE, "O2_WAVE": WAVE, "MODE": MODES, "LFO_SHAPE": ["TRI", "SAW", "RAMP", "SQUARE", "S&H", "RANDOM"],
         "LFO_PHASE": ["SYNC", "FREE", "SPREAD"], "SYNC": ["OFF", "ON"], "FTYPE": ["LP12", "HP12", "BP12", "NOTCH", "LP24", "SEM"],
         "LFO_PITCH_TO": ["OSC1", "OSC2", "BOTH"], "DLY_TIME": ["1/16", "1/8T", "1/8", "1/8.", "1/4", "1/4.", "1/2"]}
BBD_T = None


def bbd_ms(v):
    global BBD_T
    if BBD_T is None:
        s = open(os.path.join(K.ROOT, "firmware", "gen", "obv_tables.h")).read()
        m = re.search(r"BBD_T\[128\]\s*=\s*\{([^}]*)\}", s)
        BBD_T = [int(x) for x in m.group(1).replace("\n", " ").split(",") if x.strip()]
    return BBD_T[v] / K.FS * 1000


def ms_of(v):                                   # the engine's envelope time table: 0.5 ms * 20000^(v/127)
    return 0.5 * 20000 ** (v / 127)


def unit(k, v):
    """a value in the control's own terms (ms / Hz / semitones / cents), '' where the knob has none"""
    if k in ("AA", "AD", "AR", "FA", "FD", "FR"):
        return f"{ms_of(v):.0f} ms"
    if k == "LFO_RATE":
        return f"{0.05 * 600 ** (v / 127):.1f} Hz"
    if k == "LFO_DELAY":
        return f"{5000 * (v / 127) ** 2:.0f} ms"
    if k == "CUTOFF":
        return f"{440 * 2 ** ((v + 8 - 69) / 12):.0f} Hz"
    if k == "UNI_DET":
        return f"+-{(v * v // 64) * 100 / 256:.1f} cents"
    if k == "ALLEY":
        return "SYNC" if v == 0 else f"{bbd_ms(v):.0f} ms"
    if k == "ENV_O2":
        return f"{(v - 64) * 24 / 63:+.1f} st at the env peak"
    if k == "O2_FINE":
        return f"{(v - 64) * 2 * 100 / 256:+.1f} cents"
    return ""


def change(k, old, new):
    """one change under the echo rule: name old -> new, in the control's units and as % of its full range"""
    if k in NAMES:
        return f"{k} {NAMES[k][old]} -> {NAMES[k][new]}"
    if k == "O2_SEMI":
        return f"O2_SEMI {old - 24:+d} -> {new - 24:+d} st"
    pct = f"{100 * (new - old) / K.PDEF_MAX[k]:+.0f}%"
    u0, u1 = unit(k, old), unit(k, new)
    us = f" ({u0} -> {u1})" if u0 else ""
    if k in ("FENV_AMT", "ENV_O2", "O2_FINE"):
        return f"{k} {old} -> {new} (centre 64: {old - 64:+d} -> {new - 64:+d}, {pct} of range){us if k != 'FENV_AMT' else ''}"
    if k == "POLY_N":
        return f"POLY_N {old} -> {new} voices"
    if k == "UNI_N":
        return f"UNI_N {old} -> {new} voices"
    return f"{k} {old} -> {new} ({pct}){us}"


_ROW = re.compile(r"\[P_([A-Z0-9_]+)\]\s*=\s*\{\"[^\"]*\",\s*([^,]+),\s*([^,]+),")
_CONST = {"NFTYPE - 1": 5, "NDDIV - 1": 6}


def _pdef_max():
    s = open(os.path.join(K.ROOT, "firmware", "src", "obv_params.h")).read()
    return {m[1]: _CONST.get(m[2].strip(), None) or int(m[2]) for m in _ROW.finditer(s)}


K.PDEF_MAX = _pdef_max()


def _pdef_def():
    s = open(os.path.join(K.ROOT, "firmware", "src", "obv_params.h")).read()
    return {m[1]: m[3].strip() for m in _ROW.finditer(s)}


SYM = {"O1_WAVE": ["W_OFF", "W_SAW", "W_PLS", "W_BOTH"], "O2_WAVE": ["W_OFF", "W_SAW", "W_PLS", "W_BOTH"],
       "MODE": ["M_POLY", "M_DUAL", "M_UNISON", "M_MONO"], "FTYPE": ["F_LP12", "F_HP12", "F_BP12", "F_NOTCH", "F_LP24", "F_SEM"],
       "LFO_SHAPE": ["L_TRI", "L_SAW", "L_RAMP", "L_SQR", "L_SH", "L_RND"], "LFO_PHASE": ["LP_SYNC", "LP_FREE", "LP_SPREAD"],
       "LFO_PITCH_TO": ["TO_O1", "TO_O2", "TO_BOTH"], "LFO_PWM_TO": ["TO_O1", "TO_O2", "TO_BOTH"],
       "DLY_TIME": ["DD_16", "DD_8T", "DD_8", "DD_8D", "DD_4", "DD_4D", "DD_2"]}


def emit(name, params):
    """the C array (overrides over the defaults, in table order) for a resolved parameter list"""
    dflt = _pdef_def()
    SYMD = {"W_OFF": 0, "W_SAW": 1, "W_PLS": 2, "W_BOTH": 3, "M_POLY": 0, "M_DUAL": 1, "M_UNISON": 2, "M_MONO": 3, "F_LP12": 0, "F_HP12": 1,
            "F_BP12": 2, "F_NOTCH": 3, "F_LP24": 4, "F_SEM": 5, "L_TRI": 0, "L_SAW": 1, "L_RAMP": 2, "L_SQR": 3, "L_SH": 4, "L_RND": 5,
            "LP_SYNC": 0, "LP_FREE": 1, "LP_SPREAD": 2, "TO_O1": 0, "TO_O2": 1, "TO_BOTH": 2, "DD_16": 0, "DD_8T": 1, "DD_8": 2, "DD_8D": 3,
            "DD_4": 4, "DD_4D": 5, "DD_2": 6}
    items = []
    for k, i in sorted(K.PARAM_IDS.items(), key=lambda kv: kv[1]):
        if k not in params:
            continue
        d = dflt[k]
        d = SYMD.get(d, d)
        d = int(d)
        if params[k] != d:
            items.append(f"P_{k}, {SYM[k][params[k]] if k in SYM else params[k]}")
    lines, cur = [], f"static const uint8_t PF_{name}[] = {{"
    pad = " " * 4
    for n, it in enumerate(items):
        piece = it + ", "
        if len(cur) + len(piece) > 118:
            lines.append(cur.rstrip())
            cur = pad
        cur += piece
    return "\n".join(lines + [cur + "X};"])


def resolve(src_dir, slot):
    """a slot's full parameter list as the firmware's own tables resolve it (defaults + the patch's overrides)"""
    exe = os.path.join(K.BUILD, "dump_patch_r")
    subprocess.run(["cc", "-Wall", "-Wno-unused-function", "-I" + os.path.join(src_dir, "firmware", "src"),
                    "-I" + os.path.join(src_dir, "firmware", "gen"), "-o", exe,
                    os.path.join(K.ROOT, "tests", "voicing", "dump_patch.c")], check=True)
    d = {}
    for l in subprocess.run([exe, str(slot)], capture_output=True, text=True, errors="replace", check=True).stdout.splitlines():
        t = l.split()
        if t and t[0].isdigit():
            d[ID2N[int(t[0])]] = int(t[-2] if t[-1] == "*" else t[-1])
    return d


# ---- the patches ----------------------------------------------------------------------------------------------------------
from batch01a_variants import PATCHES, law            # the variant tables (the decisions), one per patch


# ---- measuring --------------------------------------------------------------------------------------------------------------
def centroid_at(a, t0_ms, t1_ms, nfft=2048):
    """spectral centroid (Hz) of the mono sum over [t0, t1] ms (frames weighted by energy)"""
    x = a.mean(1)
    win = np.hanning(nfft)
    f = np.fft.rfftfreq(nfft, 1 / K.FS)
    num = den = 0.0
    s0, s1 = int(t0_ms * K.FS / 1000), int(t1_ms * K.FS / 1000)
    for s in range(s0, max(s1 - nfft, s0 + 1), nfft // 4):
        X = np.abs(np.fft.rfft(x[s:s + nfft] * win))
        e = (X ** 2).sum()
        if e > 0:
            num += e * (f * X).sum() / X.sum(); den += e
    return num / den if den else 0.0


def dc_free(a, off_ms, win_ms):
    """the render minus the constant it has settled on at the end of the release window: GROWL's 10 Hz DC blocker leaves an
    integer-rounding offset behind (-44 .. -53 dBFS, a constant) that would hide a release's last 40 dB.  The level numbers
    never use this"""
    e = int((off_ms + win_ms) * K.FS / 1000)
    return a - a[e - 2646:e].mean(0)


def held_env(a, on_ms, off_ms, f0):
    """the envelope of the one held note (phrase c / d / e): ms to reach -3 dB of the body level, the peak above the body
    (the 'snap', dB), and the brightness swell: the spectral centroid of 46 ms frames (hop 11.6 ms) over the first 600 ms
    -- its maximum (Hz) and when it happens (ms after note-on) -- against the body's centroid (300 ms in .. release)."""
    e, dt = K.env_db(a, 2.0, 1000 / f0)
    i0, i1 = int(on_ms / 2), int(off_ms / 2)
    seg = e[i0:i1]
    body = 10 * np.log10(np.mean(10 ** (e[i1 - 60:i1 - 5] / 10)))        # the last ~110 ms before release
    peak = float(seg.max())
    t3 = float(np.nonzero(seg >= body - 3)[0][0] * 2)
    x = a.mean(1)
    nfft, win, fq = 2048, np.hanning(2048), np.fft.rfftfreq(2048, 1 / K.FS)
    cs = []
    for s in range(0, 600, 12):
        o = int((on_ms + s) * K.FS / 1000) - 512            # frames centred on the time s (so s = 0 sees the onset)
        X = np.abs(np.fft.rfft(x[o:o + nfft] * win))
        cs.append((fq * X).sum() / X.sum() if X.sum() > 0 else 0.0)
    k = int(np.argmax(cs))
    return {"t_minus3_ms": t3, "peak_over_body_db": peak - body, "cent_peak": float(cs[k]), "t_cent_peak_ms": float(k * 12),
            "cent_body": centroid_at(a, max(on_ms + 300, off_ms - 400), off_ms - 20)}


def measure(exe, cg, spec, params, tag, quick=False, orig=None):
    """render the patch's phrases and gather all the numbers.  orig=(base exe, program): render through the base firmware's
    own program path instead (variant A: literally the shipping original)"""
    wavs, m = {}, {}
    def rend(ph, extra, tg, p=None):
        if orig and p is None:
            return K.render(orig[0], ph, program=orig[1], extra=extra, tag=tg)
        return K.render(exe, ph, params=params if p is None else p, extra=extra, tag=tg)
    for ph in spec["phrases"]:
        extra = ()
        if ph == spec["held"][0]:
            extra = [f"{spec['held'][1] - 0} vlog 1", f"{spec['held'][2] + 100} vlog 0"]
        a, out = rend(ph, extra, "m_" + tag)
        wavs[ph] = a
        m[ph] = K.level_metrics(a, ph)
        m[ph].update(K.tone_metrics(a, ph))
        if extra:
            m["vlog"] = {str(c): v for c, v in K.vlog_parse(out).items()}
    hp, on, off, f0 = spec["held"]
    h = wavs[hp]
    ep, eon, eoff, ef0 = spec.get("env_note", spec["held"])        # the note the envelope / sweep is read from
    m["held_env"] = held_env(wavs[ep], eon, eoff, ef0)
    m["beat"] = K.beat_metrics(h, f0, on + 500, off - 50, win_s=spec.get("beat_win", 1.5))
    m["rel"] = K.release_metrics(dc_free(h, off, spec.get("rel_win", 1200)), off, win_ms=spec.get("rel_win", 1200))
    a_dry, _ = rend(hp, (), "d_" + tag, {**params, "DLY_MIX": 0, "REV_MIX": 0, "CHEW": 0})   # the voice alone
    m["rel_dry"] = K.release_metrics(dc_free(a_dry, off, min(600, spec.get("rel_win", 1200))), off, win_ms=min(600, spec.get("rel_win", 1200)))
    st = lambda x: 20 * np.log10(max(np.abs(np.diff(x[:, 0])).max(), 1) / 32767)
    i_off = int(off * K.FS / 1000)
    m["click"] = {"body_step_db": float(st(a_dry[i_off - 4410:i_off])), "rel_step_db": float(st(a_dry[i_off:i_off + 1323]))}
    m["flutter"] = K.body_flutter(h, on + 500, off - 100)
    m["step_db"] = {ph: 20 * np.log10(np.abs(np.diff(wavs[ph], axis=0)).max() / 32767) for ph in wavs}
    m["clip"] = int(sum((np.abs(w) >= 32767).sum() for w in wavs.values()))
    m["peak_all"] = max(m[ph]["peak"] for ph in wavs)
    if not quick:
        m["cost_b"], m["cost_load"] = K.cost(cg, params=params, tag=tag)
        ir, fr = K.callgrind_ips(cg, "x_stress", params=params, tag=tag + "i", notes=False)
        m["cost_idle"] = ir / fr                       # nothing sounding: the always-on stages (GROWL, ALLEY, ...) alone
    return wavs, m


def trim_volume(exe, params, phrase, target=BANK_REF):
    """the VOLUME byte (square law, ~0.17 dB a step) whose RMS on the level phrase is closest to the target"""
    v = params.get("VOLUME", 100)
    best = None
    for _ in range(8):
        a, _ = K.render(exe, phrase, params={**params, "VOLUME": v}, tag="trim")
        r = K.level_metrics(a, phrase)["rms"]
        if best is None or abs(r - target) < abs(best[1] - target):
            best = (v, r)
        if abs(r - target) < 0.12:
            break
        nv = int(round(v * 10 ** ((target - r) / 40)))
        v = max(1, min(127, nv if nv != v else v + (1 if target > r else -1)))
    return best


def f0s(v):
    return ">win" if v is None else f"{v:.0f}"


def md_tables(spec, results):
    ks = list(results)
    L = []
    lvl = spec["level"]
    row = lambda name, f: L.append("| " + name + " | " + " | ".join(f(results[k]) for k in ks) + " |")
    L.append("| | " + " | ".join(f"**{k}** {results[k]['tag']}" for k in ks) + " |")
    L.append("|---|" + "---|" * len(ks))
    row("VOLUME (trim)", lambda r: str(r["volume"]))
    row(f"RMS on level phrase ({lvl[0]}), note-on dBFS", lambda r: f"{r[lvl]['rms']:.1f}")
    row("vs reference −18.0", lambda r: f"{r[lvl]['rms'] - BANK_REF:+.1f}")
    if lvl != "b_stabs":
        row("RMS on phrase (b) (the bank's own reading)", lambda r: f"{r['b_stabs']['rms']:.1f}")
        row("difference (b) − level phrase, dB", lambda r: f"{r['b_stabs']['rms'] - r[lvl]['rms']:+.1f}")
    row("K-weighted RMS (level phrase)", lambda r: f"{r[lvl]['rms_k']:.1f}")
    row("peak, whole render, level phrase dBFS", lambda r: f"{r[lvl]['peak']:.1f}")
    row("peak, any phrase dBFS (limit ≤ −4)", lambda r: f"{r['peak_all']:.1f}")
    row("RMS per phrase (" + " / ".join(p[0] for p in spec["phrases"]) + ")",
        lambda r: " / ".join(f"{r[p]['rms']:.1f}" for p in spec["phrases"]))
    row("centroid Hz (level phrase)", lambda r: f"{r[lvl]['centroid']:.0f}")
    row("centroid Hz (b stabs)", lambda r: f"{r['b_stabs']['centroid']:.0f}")
    row("low share < 150 Hz (level phrase / b)", lambda r: f"{r[lvl]['low_share']:.0f}% / {r['b_stabs']['low_share']:.0f}%")
    hp, on, off, f0 = spec["held"]
    row(f"env note ({spec['env_name']}): −3 dB at (ms) · peak above body (dB)",
        lambda r: f"{r['held_env']['t_minus3_ms']:.0f} · {r['held_env']['peak_over_body_db']:+.1f}")
    row("env note: brightness peak Hz @ ms after note-on → body Hz",
        lambda r: f"{r['held_env']['cent_peak']:.0f} @ {r['held_env']['t_cent_peak_ms']:.0f} → {r['held_env']['cent_body']:.0f}")
    row("detune law: stack/pair spread (cents)", lambda r: law(r["params"])[0])
    row("OSC 2 vs OSC 1 inside each voice (FINE, cents)", lambda r: f"{law(r['params'])[1]:+.1f}")
    row("beat measured (Hz, mean [min–max]) · depth dB p-p",
        lambda r: f"{r['beat']['rate_mean']:.2f} [{r['beat']['rate_min']:.2f}–{r['beat']['rate_max']:.2f}] · {r['beat']['depth_db']:.0f}")
    row("card static offsets (cents)", lambda r: " / ".join(f"{v[0]:+.1f}" for v in r["vlog"].values()) or "-")
    row("wander s.d. (cents, per card)", lambda r: " / ".join(f"{v[1]:.1f}" for v in r["vlog"].values()) or "-")
    row("wander range (cents, per card)", lambda r: " / ".join(f"{v[2]:+.0f}..{v[3]:+.0f}" for v in r["vlog"].values()) or "-")
    row("release −20 / −40 / −60 dB (ms), with FX",
        lambda r: f"{f0s(r['rel']['first20'])} / {f0s(r['rel']['first40'])} / {f0s(r['rel']['last60'])}")
    row("release −20 / −40 / −60 dB (ms), voice alone (FX 0)",
        lambda r: f"{f0s(r['rel_dry']['first20'])} / {f0s(r['rel_dry']['first40'])} / {f0s(r['rel_dry']['last60'])}")
    row("voice alone: largest sample step, body (100 ms before) → release (30 ms after), dBFS",
        lambda r: f"{r['click']['body_step_db']:.0f} → {r['click']['rel_step_db']:.0f}")
    row("largest sample step dBFS (per phrase)", lambda r: " / ".join(f"{r['step_db'][p]:.0f}" for p in spec["phrases"]))
    row("clipped samples", lambda r: str(r["clip"]))
    if "cost_b" in results[ks[0]]:
        row("cost: host instr/sample, phrase (b)", lambda r: f"{r['cost_b']:.0f}")
        row("cost idle, nothing sounding (always-on stages)", lambda r: f"{r['cost_idle']:.0f}")
        row(f"cost under load ({spec['load']}), on top of idle", lambda r: f"{r['cost_load']:.0f}")
        row("cost worst case = idle + load", lambda r: f"{r['cost_idle'] + r['cost_load']:.0f}")
    return "\n".join(L)


def readme(spec, results):
    L = [f"# {spec['slot']:02d} {spec['name']} — voicing round (Batch 1A, the attack set)\n",
         f"*Generated by tests/voicing/batch01a.py. Level-matched to the bank reference (−18.0 dBFS RMS, note-on region) on phrase "
         f"({spec['level'][0]}) {spec['level_name']}; the bank's own phrase (b) is in the table as well. Every parameter change is "
         f"before → after under the echo rule in numbers.md.*\n",
         f"**Recommended: {spec['recommend']}** — " + spec["why"](results) + "\n", "## What to listen to\n", spec["listen"] + "\n",
         "## The variants\n"]
    for k, r in results.items():
        L.append(f"**{k} {r['tag']}** — {r['desc']}\n")
        L.append("\n".join(f"- {c}" for c in r["changes"]) or "- (none: the original)")
        L.append("")
    L.append("## The numbers\n")
    L.append(md_tables(spec, results))
    L.append("\n" + spec["notes"])
    return "\n".join(L) + "\n"


def main():
    if "--emit" in sys.argv:                     # --emit SLOT KEY: the C array of that variant (from the saved results.json)
        slot, key = int(sys.argv[sys.argv.index("--emit") + 1]), sys.argv[sys.argv.index("--emit") + 2]
        spec = [p for p in PATCHES if p["slot"] == slot][0]
        res = json.load(open(os.path.join(OUT, spec["dir"], "results.json")))
        print(emit(spec["cname"], res[key]["params"]))
        return
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    quick = "--quick" in sys.argv
    only = int(sys.argv[sys.argv.index("--only") + 1]) if "--only" in sys.argv else None
    if only is not None:
        args = [x for x in args if x != str(only)]
    base = os.path.abspath(args[0] if args else os.path.join(K.BUILD, "base"))
    exe = K.build_host()
    cg = None if quick else K.callgrind_exe()
    old = K.build_host(base, os.path.join(K.BUILD, "obervave_base"))
    for spec in PATCHES:
        slot = spec["slot"]
        if only is not None and slot != only:
            continue
        ORIGINAL = resolve(base, slot)
        # A mechanism: the original list over INIT against the base firmware's own slot.  Not bit-exact by nature: CUTOFF / RESO
        # slew in with `x += (target - x) >> 6`, which stops short of the target when it comes from below (a floor), so the
        # same patch lands up to 63/256 st of cutoff apart depending on where it came from (the INIT path comes from above, the
        # program path from the boot patch), and a DRAIN patch's spring state starts at another moment.  Error in dB vs signal:
        pin = K.PARAM_IDS["LFO_PHASE"]
        proof = {}
        for ph in K.AUDITION:
            a, _ = K.render(old, ph, program=slot - 1, extra=[f"{K.T_PARAMS} param {pin} 0"], tag="proofa")
            b, _ = K.render(exe, ph, params={**ORIGINAL, "LFO_PHASE": 0}, tag="proofb")
            proof[ph] = round(float(10 * np.log10(max(((a - b) ** 2).mean(), 1e-9) / (a ** 2).mean())), 1) if (a != b).any() else None
        print(f"[{slot:02d}] A proof (base slot vs ORIGINAL over INIT, error vs signal in dB; None = bit-identical):", proof)
        assert all(v is None or v < -25 for v in proof.values()), "the original list does not reproduce the slot"
        d = os.path.join(OUT, spec["dir"])
        os.makedirs(d, exist_ok=True)
        results = {}
        for key, tag, desc, ch in spec["variants"]:
            params = {**ORIGINAL, **ch}
            if key == "A":
                vol = params["VOLUME"]
            else:
                vol, _ = trim_volume(exe, params, spec["level"])
            params["VOLUME"] = vol
            wavs, m = measure(exe, cg, spec, params, spec["dir"][:2] + key, quick, orig=(old, slot - 1) if key == "A" else None)
            if not quick:
                for ph in spec["phrases"]:
                    K.write_wav(os.path.join(d, f"{key}_{tag}_{spec['short'][ph]}.wav"), wavs[ph][int(K.T_CUT * K.FS):])
            m.update(tag=tag, desc=desc, volume=vol, params=params,
                     changes=[change(k, ORIGINAL[k], v) for k, v in params.items() if v != ORIGINAL[k]])
            results[key] = m
            L = spec["level"]
            print(f"  {key} {tag:12s} VOL {vol:3d}  RMS({L[0]}) {m[L]['rms']:6.1f}  pk {m['peak_all']:5.1f}  b {m['b_stabs']['rms']:6.1f}  "
                  f"cent {m[L]['centroid']:5.0f}  low {m[L]['low_share']:3.0f}%  beat {m['beat']['rate_mean']:.2f}  "
                  f"t-3dB {m['held_env']['t_minus3_ms']:4.0f} snap {m['held_env']['peak_over_body_db']:+4.1f} bright {m['held_env']['cent_peak']:5.0f}@{m['held_env']['t_cent_peak_ms']:3.0f}ms/body {m['held_env']['cent_body']:5.0f}  rel60 {m['rel']['last60']:4.0f}/{m['rel_dry']['last60']:4.0f}"
                  + (f"  cost {m['cost_b']:.0f} idle {m['cost_idle']:.0f} +load {m['cost_load']:.0f}" if "cost_b" in m else ""))
        if quick:
            continue
        with open(os.path.join(d, "results.json"), "w") as f:
            json.dump({k: dict(r) for k, r in results.items()}, f, indent=1, default=float)
        with open(os.path.join(d, "README.md"), "w") as f:
            f.write(readme(spec, results))
        with open(os.path.join(d, "numbers.md"), "w") as f:
            f.write(f"# generated by tests/voicing/batch01a.py -- slot {slot:02d} {spec['name']}\n\n")
            for k, r in results.items():
                f.write(f"**{k} {r['tag']}** — {r['desc']}\n\n" + ("\n".join(f"- {c}" for c in r["changes"]) or "- (none: the original)") + "\n\n")
            f.write(md_tables(spec, results) + "\n")
        print(f"[{slot:02d}] written {d}")


if __name__ == "__main__":
    main()
