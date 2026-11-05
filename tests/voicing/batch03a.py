#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Voicing round for Batch 3A, "the fat and driven set": 01 Red Pill, 02 Cement Grind, 06 zzuFuzz, 08 Wire Bite.

  python3 tests/voicing/batch03a.py [base_tree] [--only SLOT] [--quick] [--no-cost]
        base_tree: the firmware exported from the commit before the batch (default build/voicing/base)
        --quick:   no WAVs, no callgrind, no files (for tuning a variant table; prints one line per variant)
        --emit SLOT KEY: the C array of a variant (from results.json)

Same method as batch02a.py: a variant is a FULL parameter list over INIT; the ORIGINAL "A" is rendered through the base firmware's own program path;
VOLUME is trimmed to the bank reference (-18.0 dBFS RMS over the note-on region) on the patch's level phrase, last.  New measures: batch03a_metrics.py.
Output: listen/voicing/batch-03a/<NN-name>/ (WAVs only ever go on the never-merged listen branch)."""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import batch01a as B                           # resolve(), emit(): the base tree's own resolver and the C array
import batch02a as B2                          # trim_volume(), change(): the level trim and the echo rule
import batch02a_metrics as M
import batch03a_metrics as N
from batch03a_variants import PATCHES

OUT = os.path.join(K.ROOT, "listen", "voicing", "batch-03a")
SHORT = {"a_riff": "riff", "b_stabs": "stabs", "c_held": "held", "i_spit": "spit", "j_grind": "grind", "k_wall": "wall", "l_wire": "wire"}
NOFX = {"DLY_MIX": 0, "REV_MIX": 0}            # the two sends: wet - this = the sends' own return (GROWL / CHEW stay: they are in the voice)
FXOFF = {"DLY_MIX": 0, "REV_MIX": 0, "CHEW": 0, "GROWL": 0}


def f1(x, p=1):
    return "-" if x is None or (isinstance(x, float) and x < -150) else f"{x:.{p}f}"


def measure(exe, cg, spec, params, tag, quick, orig=None, no_cost=False):
    lp, lvl_ph = spec["level"], spec["level"]
    wavs, outs = {}, {}
    for ph in spec["phrases"]:
        ex = [f"3000 vlog 1", f"{spec['vlog_off']} vlog 0"] if ph == "c_held" else ()
        if spec.get("drift") and ph == lp:
            ex = [f"{spec['drift'][0]} vlog 1", f"{spec['drift'][1]} vlog 0"]
        if orig:
            wavs[ph], outs[ph] = K.render(orig[0], ph, program=orig[1], extra=ex, tag="m_" + tag)
        else:
            wavs[ph], outs[ph] = K.render(exe, ph, params=params, extra=ex, tag="m_" + tag)
    m = {}
    for ph in spec["phrases"]:
        m[ph] = K.level_metrics(wavs[ph], ph)
        m[ph].update(K.tone_metrics(wavs[ph], ph))
        m[ph]["bands"] = M.band_split_phrase(wavs[ph], ph)
        m[ph]["crest"] = N.crest_db(wavs[ph], ph)
    m["peak_all"] = max(m[ph]["peak"] for ph in spec["phrases"])
    m["peak_phrase"] = max(spec["phrases"], key=lambda ph: m[ph]["peak"])
    m["clip"] = int(sum((np.abs(w) >= 32767).sum() for w in wavs.values()))
    m["step_db"] = {ph: float(20 * np.log10(np.abs(np.diff(wavs[ph], axis=0)).max() / 32767)) for ph in spec["phrases"]}
    m["level"] = m[lp]["rms"]
    m["vlog"] = {str(c): v for c, v in K.vlog_parse(outs["c_held"]).items()}
    if spec.get("drift"):
        m["vlog_hold"] = {str(c): v for c, v in K.vlog_parse(outs[lp]).items()}
    m["beat"] = K.beat_metrics(wavs["c_held"], 110.0, 3300, 5300)
    w = wavs[lp]
    dc = w[-2646:].mean(0)
    N_s = N._s
    # the voice alone (effects off) for the wet / dry readings
    dry_nofx = K.render(exe, lp, params={**params, **NOFX}, tag="d_" + tag)[0]
    dry_all = K.render(exe, lp, params={**params, **FXOFF}, tag="e_" + tag)[0]
    w_inits = w if not orig else K.render(exe, lp, params=params, tag="w_" + tag)[0]   # (A: wet and dry both over INIT, so wet - dry is exact)
    kind = spec["id"]
    on, off, f0 = spec["note"]                   # the reference note of the patch: on, off (ms), f0 (Hz)
    toff, d0, d1, twin = spec["tail"]
    m["tail"] = M.tail_times(w, toff, 120, twin, dc=w[N._s(d0):N._s(d1)].mean(0))
    m["tail_dry"] = M.tail_times(dry_nofx, toff, 120, twin, dc=dry_nofx[N._s(d0):N._s(d1)].mean(0))
    m["dc_dbfs"] = float(20 * np.log10(max(np.abs(w[N._s(d0):N._s(d1)].mean(0)).max(), 1e-3) / 32767))
    m["attack"] = N.attack_probe(exe, params)
    if spec.get("wet"):
        m["wet"] = [N.wet_windows(w_inits, dry_nofx, t) for t in spec["wet"]]
        m["wet_cent"] = M.centroid(w_inits - dry_nofx, spec["wet"][0], spec["wet"][0] + 1200)
        m["wet_bands"] = M.band_shares(w_inits - dry_nofx, spec["wet"][0], spec["wet"][-1] + 1200)
        m["wet_total_db"] = M.energy_db((w_inits - dry_nofx)[int(3.2 * K.FS):int(10.9 * K.FS)]) - M.energy_db(dry_nofx[int(3.2 * K.FS):int(10.9 * K.FS)])
        m["snap"] = M.attack_snap(dry_nofx, spec["wet"][0])
    if spec.get("pwm"):
        m["pwm"] = N.pwm_metrics(w, *spec["pwm"])
        m["pwm_dry"] = N.pwm_metrics(dry_all, *spec["pwm"])
        m["pwm_riff"] = N.pwm_riff(w, [(t, t + 400) for t in range(3000, 7000, 500)])
        m["snap"] = M.attack_snap(dry_all, spec["pwm"][0] - 4200)
    if spec.get("drift"):
        on_d, off_d, f0_d = spec["drift"]
        d_ = params["LFO_PITCH"]
        m["lfo_pitch_cents"] = float(((d_ * d_) >> 7) * 24 * 100 / 256)       # the engine's own law: peak of the pitch LFO, cents (LFO_PITCH 10 rounds to 0)
        m["zap"] = N.zap_metrics(dry_all, on_d)
        m["zap_chop"] = N.zap_metrics(dry_all, spec["chop"], body=(40, 100))
        m["tail_chop"] = M.tail_times(w, spec["chop"] + 110, 60, 130, dc=dc)
    if spec.get("curve"):
        c_on, c_off = spec["curve"]
        m["curve"] = N.level_curve(w, c_on, c_off - c_on)
        m["sustain_loss"] = m["curve"][0][1] - m["curve"][-1][1]
        m["crest_hold"] = N.crest_db(w, t0_ms=c_on + 200, t1_ms=c_off)
        m["crest_chord"] = N.crest_db(w, t0_ms=7100, t1_ms=8500)
        m["chord_tail"] = M.tail_times(w, 8500, 120, 800, dc=w[N._s(9200):N._s(9400)].mean(0))
        m["snap"] = M.attack_snap(w, 3000)
        m["snap_stab"] = M.attack_snap(w, 9500)
        m["selfosc"] = N.selfosc_probe(exe, params, resos=(0, 100, 115, 120, 124, 127))
        m["dry_cent"] = M.centroid(dry_all, c_on + 300, c_off)
    m["cost"] = None
    if not quick and not no_cost:
        cb, cl = K.cost(cg, params=params, tag=tag)
        ir, fr = K.callgrind_ips(cg, "x_stress", params=params, tag=tag + "i", notes=False)
        m["cost"] = {"b": cb, "load": cl, "idle": ir / fr}
    return wavs, m


def run_probe(exe, spec, params, name, vals):
    """the recommended variant with ONE parameter stepped (VOLUME as trimmed): what that knob does here, in numbers"""
    lp = spec["level"]
    rows = []
    for v in vals:
        a, _ = K.render(exe, lp, params={**params, name: v}, tag="pr")
        t = K.tone_metrics(a, lp)
        lm = K.level_metrics(a, lp)
        r = {"v": v, "rms": lm["rms"], "peak": lm["peak"], "crest": N.crest_db(a, lp), "cent": t["centroid"], "bands": M.band_split_phrase(a, lp)}
        if spec.get("curve"):
            r["hold_crest"] = N.crest_db(a, t0_ms=spec["curve"][0] + 200, t1_ms=spec["curve"][1])
            c = N.level_curve(a, spec["curve"][0], spec["curve"][1] - spec["curve"][0])
            r["sust"] = c[0][1] - c[-1][1]
        rows.append(r)
    return rows


def probe_table(spec, name, rows):
    extra = " | hold crest dB | sustain loss dB" if spec.get("curve") else ""
    L = [f"| {name} | level reading dBFS (VOLUME unchanged) | peak dBFS | crest dB (level phrase) | centroid Hz | band split % <60/60-150/150-400/400-1.2k/1.2k+{extra} |", "|---|---|---|---|---|---|" + ("---|---|" if extra else "")]
    for r in rows:
        L.append(f"| {r['v']} | {r['rms']:.1f} | {r['peak']:.1f} | {r['crest']:.1f} | {r['cent']:.0f} | {M.fmt_bands(r['bands'])}" + (f" | {r['hold_crest']:.1f} | {r['sust']:+.1f}" if spec.get("curve") else "") + " |")
    return "\n".join(L)


def quick_line(spec, key, vol, m):
    lp = spec["level"]
    L = (f"[{spec['slot']:02d}] {key} VOL {vol:3d} lvl {m['level']:6.1f} b {m['b_stabs']['rms']:6.1f} pk {m['peak_all']:5.1f} crest {m[lp]['crest']:4.1f} "
         f"cent {m[lp]['centroid']:5.0f} bands {M.fmt_bands(m[lp]['bands'])} atk {m['attack']['as']['t90']:.1f}ms t60 {m['tail']['t60']}")
    if "wet" in m:
        L += " wet " + " | ".join("/".join(f"{x['re_dry_db']:+.0f}" for x in ws) for ws in m["wet"]) + f" total {m['wet_total_db']:+.1f}"
    if "pwm" in m:
        p = m["pwm"]
        L += " pwm " + " ".join(f"{b}:{p['bands'][b][0]:.1f}dB@{p['bands'][b][1]:.1f}Hz({p['bands'][b][2]:.2f})" for b in list(N.PWM_BANDS) + ["level"])
    if "lfo_pitch_cents" in m:
        L += f" lfo {m['lfo_pitch_cents']:.0f}c vl-sd {np.mean([v[1] for v in m['vlog_hold'].values()]):.1f} zap {m['zap']['c_attack']:.0f}->{m['zap']['c_body']:.0f}Hz burst {m['zap']['burst_db']:.1f}dB chop-burst {m['zap_chop']['burst_db']:.1f}"
    if "curve" in m:
        L += f" sustain loss {m['sustain_loss']:.1f}dB crest hold {m['crest_hold']:.1f} chord {m['crest_chord']:.1f} selfosc " + " ".join(f"{r['reso']}:{r['diff']:.1f}" for r in m["selfosc"])
    return L


def tables(spec, R):
    ks = list(R)
    lp = spec["level"]
    L = ["| | " + " | ".join(f"**{k}** {R[k]['tag']}" for k in ks) + " |", "|---|" + "---|" * len(ks)]
    row = lambda name, f: L.append("| " + name + " | " + " | ".join(f(R[k]) for k in ks) + " |")
    row("VOLUME (trim)", lambda r: str(r["volume"]))
    row(f"LEVEL READING ({spec['level_def']}), dBFS", lambda r: f1(r["level"]))
    row("vs the bank reference −18.0", lambda r: f"{r['level'] + 18.0:+.1f}")
    row("RMS on phrase (b), the bank's own reading", lambda r: f1(r["b_stabs"]["rms"]))
    row("difference (b) − level reading, dB", lambda r: f"{r['b_stabs']['rms'] - r['level']:+.1f}")
    row("K-weighted RMS, level phrase · phrase (b)", lambda r: f"{f1(r[lp]['rms_k'])} · {f1(r['b_stabs']['rms_k'])}")
    row("peak of any phrase, dBFS (limit ≤ −4) · which", lambda r: f"{f1(r['peak_all'])} · {r['peak_phrase']}")
    row("crest factor (peak/RMS, dB), level phrase · phrase (b)", lambda r: f"{r[lp]['crest']:.1f} · {r['b_stabs']['crest']:.1f}")
    row("RMS note-on region per phrase (" + " / ".join(p[0] for p in spec["phrases"]) + ")", lambda r: " / ".join(f1(r[p]["rms"]) for p in spec["phrases"]))
    row("centroid Hz (level phrase / b)", lambda r: f"{r[lp]['centroid']:.0f} / {r['b_stabs']['centroid']:.0f}")
    row("band split % <60 / 60-150 / 150-400 / 400-1.2k / 1.2k+ (level phrase)", lambda r: M.fmt_bands(r[lp]["bands"]))
    row("band split % (b)", lambda r: M.fmt_bands(r["b_stabs"]["bands"]))
    row("attack, A5 probe from silence, as rendered: key-down → 10 % → 90 % of the plateau (ms) · rise 10-90 % · early peak re plateau (dB)", lambda r: f"{r['attack']['as']['t10']:.1f} → {r['attack']['as']['t90']:.1f} · {r['attack']['as']['rise']:.1f} · {r['attack']['as']['peak_re_plateau']:+.1f}")
    row("  level re plateau at 2 / 5 / 10 / 20 / 50 ms after the key-down (dB)", lambda r: " / ".join(f"{r['attack']['as']['bloom'][k]:+.1f}" for k in ("2", "5", "10", "20", "50")))
    row("  voice alone (GROWL and sends off): 10 → 90 % (ms) · rise · early peak re plateau", lambda r: f"{r['attack']['voice']['t10']:.1f} → {r['attack']['voice']['t90']:.1f} · {r['attack']['voice']['rise']:.1f} · {r['attack']['voice']['peak_re_plateau']:+.1f}")
    row("tail after the reference note: −20 / −40 / −60 dB (ms), as rendered", lambda r: f"{f1(r['tail']['t20'], 0)} / {f1(r['tail']['t40'], 0)} / {f1(r['tail']['t60'], 0)}")
    row("  voice alone (sends off)", lambda r: f"{f1(r['tail_dry']['t20'], 0)} / {f1(r['tail_dry']['t40'], 0)} / {f1(r['tail_dry']['t60'], 0)}")
    row("beat of the stack, held A2 (Hz mean [min–max] · depth dB)", lambda r: f"{r['beat']['rate_mean']:.2f} [{r['beat']['rate_min']:.2f}–{r['beat']['rate_max']:.2f}] · {r['beat']['depth_db']:.0f}")
    row("wander, engine log of the voice cards, held A2: static offset (cents)", lambda r: " / ".join(f"{v[0]:+.1f}" for v in r["vlog"].values()) or "-")
    row("  wander s.d. (cents per card)", lambda r: " / ".join(f"{v[1]:.1f}" for v in r["vlog"].values()) or "-")
    row("  wander range (cents per card)", lambda r: " / ".join(f"{v[2]:+.0f}..{v[3]:+.0f}" for v in r["vlog"].values()) or "-")
    if spec.get("wet"):
        for i, t in enumerate(spec["wet_names"]):
            for j, wn in enumerate(("0-20", "20-100", "100-250")):
                row(f"{t}: {wn} ms after note-on: dry dB · return dB · return re dry dB",
                    lambda r, i=i, j=j: f"{r['wet'][i][j]['dry_db']:.1f} · {f1(r['wet'][i][j]['fx_db'])} · " + (f"{r['wet'][i][j]['re_dry_db']:+.1f}" if r['wet'][i][j]['re_dry_db'] > -150 else "-"))
        row("return re the dry, whole phrase (dB)", lambda r: f1(r["wet_total_db"]))
        row("return: centroid Hz · share <150 Hz % · share >400 Hz %", lambda r: f"{r['wet_cent']:.0f} · {r['wet_bands']['<60'] + r['wet_bands']['60-150']:.0f} · {r['wet_bands']['400-1.2k'] + r['wet_bands']['1.2k+']:.0f}")
        row("dry note: centroid of the first 23 ms → next 67 ms (Hz, ratio)", lambda r: f"{r['snap'][0]:.0f} → {r['snap'][1]:.0f} (×{r['snap'][2]:.1f})")
    if spec.get("pwm"):
        for b in list(N.PWM_BANDS) + ["level"]:
            row(f"PWM, held A2: {b} band (level): depth dB (95-5 %) · rate Hz · purity", lambda r, b=b: f"{r['pwm']['bands'][b][0]:.1f} · {r['pwm']['bands'][b][1]:.1f} · {r['pwm']['bands'][b][2]:.2f}")
        row("PWM on the riff (8 quarter notes, 300 ms of each): depth dB per band 150-400 / 400-1.2k / 1.2k-3k / 3k+ · level", lambda r: " / ".join(f"{r['pwm_riff'][b]:.1f}" for b in N.PWM_BANDS) + f" · {r['pwm_riff']['level']:.1f}")
        row("PWM: the strongest band · the LFO's nominal rate (Hz)", lambda r: f"{r['pwm']['best']} · {r['lfo_hz']:.1f}")
        row("PWM, voice alone (GROWL 0): strongest band depth dB · rate Hz", lambda r: f"{r['pwm_dry']['bands'][r['pwm_dry']['best']][0]:.1f} · {r['pwm_dry']['bands'][r['pwm_dry']['best']][1]:.1f}")
        row("snap: centroid first 23 ms → next 67 ms, first riff note (Hz)", lambda r: f"{r['snap'][0]:.0f} → {r['snap'][1]:.0f} (×{r['snap'][2]:.1f})")
    if spec.get("drift"):
        row("DRIFT, engine log of the voice cards over the held A4: static offset of each card (cents)", lambda r: " / ".join(f"{v[0]:+.1f}" for v in r["vlog_hold"].values()))
        row("  wander s.d. per card (cents)", lambda r: " / ".join(f"{v[1]:.1f}" for v in r["vlog_hold"].values()))
        row("  wander range per card (cents)", lambda r: " / ".join(f"{v[2]:+.0f}..{v[3]:+.0f}" for v in r["vlog_hold"].values()))
        row("  pitch LFO (random, SPREAD phases): peak depth cents · rate Hz (a new target each period)", lambda r: f"{r['lfo_pitch_cents']:.0f} · {r['lfo_hz']:.2f}")
        row("ZAP, held A4 start: centroid first 23 ms → next 67 ms (Hz) · top (>1.2k) burst re body (dB)", lambda r: f"{r['zap']['c_attack']:.0f} → {r['zap']['c_body']:.0f} · {r['zap']['burst_db']:+.1f}")
        row("ZAP, first bite of the chopped phrase: same", lambda r: f"{r['zap_chop']['c_attack']:.0f} → {r['zap_chop']['c_body']:.0f} · {r['zap_chop']['burst_db']:+.1f}")
        row("tail after a 110 ms bite (140 ms before the next): −20 / −40 / −60 dB (ms)", lambda r: f"{f1(r['tail_chop']['t20'], 0)} / {f1(r['tail_chop']['t40'], 0)} / {f1(r['tail_chop']['t60'], 0)}")
    if spec.get("curve"):
        row("the 3 s hold, level per 0.5 s (dBFS)", lambda r: " ".join(f"{v:.1f}" for _, v in r["curve"]))
        row("sustain: first 0.5 s − last 0.5 s of the hold (dB; 0 = the wall holds)", lambda r: f"{r['sustain_loss']:+.1f}")
        row("crest factor of the held note · of the held power chord (dB)", lambda r: f"{r['crest_hold']:.1f} · {r['crest_chord']:.1f}")
        row("power chord (A2+E3+A3 held 1.5 s): tail −20 / −40 / −60 dB (ms)", lambda r: f"{f1(r['chord_tail']['t20'], 0)} / {f1(r['chord_tail']['t40'], 0)} / {f1(r['chord_tail']['t60'], 0)}")
        row("self-oscillation probe (noise-fed filter, 12 dB less noise → ? dB less output; 12 = linear, ≪ 12 = sings): RESO " + " / ".join(str(x) for x in (0, 100, 115, 120, 124, 127)).replace("0", "own", 1),
            lambda r: " / ".join(f"{x['diff']:.1f}" for x in r["selfosc"]))
        row("snap: centroid first 23 ms → next 67 ms, held A2 · first stab (Hz)", lambda r: f"{r['snap'][0]:.0f} → {r['snap'][1]:.0f} · {r['snap_stab'][0]:.0f} → {r['snap_stab'][1]:.0f}")
        row("voice alone (GROWL 0) centroid Hz", lambda r: f"{r['dry_cent']:.0f}")
    row("largest sample step dBFS (per phrase)", lambda r: " / ".join(f"{r['step_db'][p]:.0f}" for p in spec["phrases"]))
    row("clipped samples", lambda r: str(r["clip"]))
    if R[ks[0]]["cost"]:
        row("cost: host instr/sample, phrase (b)", lambda r: f"{r['cost']['b']:.0f}")
        row("cost idle (always-on stages)", lambda r: f"{r['cost']['idle']:.0f}")
        row(f"cost under load ({spec['load']}), on top of idle", lambda r: f"{r['cost']['load']:.0f}")
        row("cost worst case = idle + load", lambda r: f"{r['cost']['idle'] + r['cost']['load']:.0f}")
    return "\n".join(L)


def readme(spec, R, probe=None):
    L = [f"# {spec['slot']:02d} {spec['name']} — voicing round (Batch 3A, the fat and driven set)\n",
         f"*Generated by tests/voicing/batch03a.py. Level reading: {spec['level_def']}; matched to the bank reference (−18.0 dBFS RMS) by VOLUME; phrase (b)'s reading is in the table too. "
         f"Every change is before → after under the echo rule. WAVs are on the listen/batch-03a-chapter1-fat-and-driven branch only.*\n",
         f"**Recommended: {spec['recommend']}** — " + spec["why"](R, probe) + "\n", "## What to listen to\n", spec["listen"] + "\n", "## The variants\n"]
    for k, r in R.items():
        L.append(f"**{k} {r['tag']}** — {r['desc']}\n")
        L.append("\n".join(f"- {c}" for c in r["changes"]) or "- (none: the original)")
        L.append("")
    L += ["## The numbers\n", tables(spec, R)]
    for nm, rows in (probe or {}).items():
        L += [f"\n### What {nm} does on this patch (the recommended variant, {nm} stepped, probe renders, not variants)\n", probe_table(spec, nm, rows)]
    L += ["\n" + spec["notes"]]
    return "\n".join(L) + "\n"


def run_spec(spec, base, exe, cg, old, quick, no_cost, out_root):
    slot = spec["slot"]
    ORIGINAL = B.resolve(base, slot)
    d = os.path.join(out_root, spec["dir"])
    R = {}
    for key, tag, desc, ch in spec["variants"]:
        params = {**ORIGINAL, **ch}
        if key == "A":
            vol = params["VOLUME"]
        else:
            vol, _ = B2.trim_volume(exe, spec, params)
        params["VOLUME"] = vol
        wavs, m = measure(exe, cg, spec, params, spec["dir"][:2] + key, quick, orig=(old, slot - 1) if key == "A" else None, no_cost=no_cost)
        m.update(tag=tag, desc=desc, volume=vol, params=params, lfo_hz=0.05 * 600 ** (params["LFO_RATE"] / 127),
                 changes=[B2.change(k, ORIGINAL[k], v, params) for k, v in params.items() if v != ORIGINAL[k]])
        R[key] = m
        if not quick:
            os.makedirs(d, exist_ok=True)
            for ph in spec["phrases"]:
                K.write_wav(os.path.join(d, f"{key}_{tag}_{SHORT[ph]}.wav"), wavs[ph][int(K.T_CUT * K.FS):])
        print(quick_line(spec, key, vol, m), flush=True)
    if not quick:
        with open(os.path.join(d, "results.json"), "w") as f:
            json.dump({"variants": {k: dict(r) for k, r in R.items()}}, f, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o))
        probe = {nm: run_probe(exe, spec, R[spec["recommend"][0]]["params"], nm, vals) for nm, vals in spec.get("probes", [])}
        json.dump(probe, open(os.path.join(d, "probe.json"), "w"), default=float)
        open(os.path.join(d, "README.md"), "w").write(readme(spec, R, probe))
        with open(os.path.join(d, "numbers.md"), "w") as f:
            f.write(f"# generated by tests/voicing/batch03a.py -- slot {slot:02d} {spec['name']}\n\n")
            for k, r in R.items():
                f.write(f"**{k} {r['tag']}** — {r['desc']}\n\n" + ("\n".join(f"- {c}" for c in r["changes"]) or "- (none: the original)") + "\n\n")
            f.write(tables(spec, R) + "\n")
            for nm, rows in probe.items():
                f.write(f"\n### {nm} probe\n\n" + probe_table(spec, nm, rows) + "\n")
        print(f"[{slot:02d}] written {d}")
    return R


def main():
    if "--emit" in sys.argv:
        slot, key = int(sys.argv[sys.argv.index("--emit") + 1]), sys.argv[sys.argv.index("--emit") + 2]
        spec = [p for p in PATCHES if p["slot"] == slot][0]
        res = json.load(open(os.path.join(OUT, spec["dir"], "results.json")))
        print(B.emit(spec["cname"], res["variants"][key]["params"]))
        return
    if "--readme" in sys.argv:                    # rewrite README.md / numbers.md from results.json + probe.json (text edits, no renders)
        for spec in PATCHES:
            d = os.path.join(OUT, spec["dir"])
            R = json.load(open(os.path.join(d, "results.json")))["variants"]
            probe = json.load(open(os.path.join(d, "probe.json")))
            open(os.path.join(d, "README.md"), "w").write(readme(spec, R, probe))
            with open(os.path.join(d, "numbers.md"), "w") as f:
                f.write(f"# generated by tests/voicing/batch03a.py -- slot {spec['slot']:02d} {spec['name']}\n\n")
                for k, r in R.items():
                    f.write(f"**{k} {r['tag']}** — {r['desc']}\n\n" + ("\n".join(f"- {c}" for c in r["changes"]) or "- (none: the original)") + "\n\n")
                f.write(tables(spec, R) + "\n")
                for nm, rows in probe.items():
                    f.write(f"\n### {nm} probe\n\n" + probe_table(spec, nm, rows) + "\n")
        print("readmes rewritten")
        return
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    quick, no_cost = "--quick" in sys.argv, "--no-cost" in sys.argv
    only = int(sys.argv[sys.argv.index("--only") + 1]) if "--only" in sys.argv else None
    if only is not None:
        args = [x for x in args if x != str(only)]
    base = os.path.abspath(args[0] if args else os.path.join(K.BUILD, "base"))
    exe = K.build_host()
    cg = None if (quick or no_cost) else K.callgrind_exe()
    old = K.build_host(base, os.path.join(K.BUILD, "obervave_base"))
    for spec in PATCHES:
        if only is not None and spec["slot"] != only:
            continue
        run_spec(spec, base, exe, cg, old, quick, no_cost, OUT)


if __name__ == "__main__":
    main()
