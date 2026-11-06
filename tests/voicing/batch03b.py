#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Voicing round for Batch 3B, "the wreck and chop set": 05 ZEAROX, 07 Tape Splice, 15 Trem Chop.

  python3 tests/voicing/batch03b.py [base_tree] [--only SLOT] [--quick] [--no-cost]
        base_tree: the firmware exported from the commit before the batch (default build/voicing/base)
        --quick:   no WAVs, no callgrind, no files (for tuning a variant table; prints one line per variant)
        --emit SLOT KEY: the C array of a variant (from results.json)
        --readme:  rewrite README.md / numbers.md from results.json (text edits, no renders)

Same method as batch03a.py: a variant is a FULL parameter list over INIT; the ORIGINAL "A" is rendered through the base firmware's own program path;
VOLUME is trimmed to the bank reference (-18.0 dBFS RMS over the note-on region) on the patch's level phrase, last.  New measures: batch03b_metrics.py.
Output: listen/voicing/batch-03b/<NN-name>/ (the tables go on the merged voicing branch; WAVs only ever on the never-merged listen branch)."""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import batch01a as B                           # resolve(), emit()
import batch02a as B2                          # trim_volume(), change()
import batch02a_metrics as M
import batch03a_metrics as N
import batch03b_metrics as Q
from batch03b_variants import PATCHES

OUT = os.path.join(K.ROOT, "listen", "voicing", "batch-03b")
SHORT = {"a_riff": "riff", "b_stabs": "stabs", "c_held": "held", "m_kick": "kick", "n_splice": "splice", "o_chop": "chop", "p_chopshort": "chopshort"}
FXOFF = {"DLY_MIX": 0, "REV_MIX": 0, "CHEW": 0, "GROWL": 0}
KICK_ISO = {"A0": 3000, "A1": 4500, "A2": 6000}
KICK_PAT = [8000 + 500 * i for i in range(8)]
KICK_ALL = [3000, 4500, 6000] + KICK_PAT
SPL_STACC = [(3000 + 125 * i, 3060 + 125 * i) for i in range(12)]
SPL_SHORT = [(9500, 9580), (9800, 9880), (10100, 10180)]
CHOP_SHORT = [(3000 + 250 * i, 3110 + 250 * i) for i in range(8)]


def f1(x, p=1):
    return "-" if x is None or (isinstance(x, float) and (x != x or x < -150)) else f"{x:.{p}f}"


def fl(v):
    return "silent" if v < -150 else f"{v:.0f}"


def noise_rms(a, t0_ms, t1_ms):
    """the RMS (dBFS) of a quiet stretch with its mean (a constant DC offset after GROWL / the delay path) taken out"""
    x = a[N._s(t0_ms):N._s(t1_ms)]
    x = x - x.mean(0)
    return float(10 * np.log10(max((x ** 2).mean(), 1e-9) / 32767 ** 2))


def dc_of(a, t0_ms, t1_ms):
    return a[N._s(t0_ms):N._s(t1_ms)].mean(0)


def measure(exe, cg, spec, params, tag, quick, orig=None, no_cost=False):
    lp = spec["level"]
    slot = spec["slot"]
    wavs = {}
    for ph in spec["phrases"]:
        if orig:
            wavs[ph], _ = K.render(orig[0], ph, program=orig[1], tag="m_" + tag)
        else:
            wavs[ph], _ = K.render(exe, ph, params=params, tag="m_" + tag)
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
    w = wavs[lp]
    # the voice alone: GROWL, CHEW and the sends off (what the tape stage and the overload add is the difference)
    voice = K.render(exe, lp, params={**params, **FXOFF}, tag="v_" + tag)[0]
    if orig:                                    # (A over INIT, so a difference to its voice-only render is exact)
        w_init = K.render(exe, lp, params=params, tag="w_" + tag)[0]
    else:
        w_init = w
    m["attack"] = N.attack_probe(exe, params)
    if slot == 5:
        m.update(measure_zearox(exe, cg, spec, params, tag, wavs, voice, quick, no_cost))
    elif slot == 7:
        m.update(measure_splice(exe, cg, spec, params, tag, wavs, quick))
    elif slot == 15:
        m.update(measure_chop(exe, cg, spec, params, tag, wavs, quick))
    m["cost"] = None
    if not quick and not no_cost:
        cb, cl = K.cost(cg, params=params, tag=tag)
        ir, fr = K.callgrind_ips(cg, "x_stress", params=params, tag=tag + "i", notes=False)
        m["cost"] = {"b": cb, "load": cl, "idle": ir / fr}
        if slot == 5:                           # what CHEW and GROWL cost on this patch: the idle cost with each switched off
            for nm, ov in (("no_chew", {"CHEW": 0}), ("no_growl", {"GROWL": 0}), ("voice", FXOFF)):
                ir2, fr2 = K.callgrind_ips(cg, "x_stress", params={**params, **ov}, tag=tag + nm, notes=False)
                m["cost"][nm] = ir2 / fr2
    return wavs, m


# ---- 05: the kick ------------------------------------------------------------------------------------------------------------------
def measure_zearox(exe, cg, spec, params, tag, wavs, voice, quick, no_cost):
    a = wavs["m_kick"]
    m = {"kick": {k: Q.kick_hit(a, t) for k, t in KICK_ISO.items()}}
    m["kick_voice"] = {k: Q.kick_hit(voice, t) for k, t in KICK_ISO.items()}
    m["hit_attack"] = {k: Q.hit_attack(a, t) for k, t in KICK_ISO.items()}
    m["drops"] = Q.hit_dropouts(exe, params)
    m["drops_voice"] = None
    m["hit_crest30"] = {k: N.crest_db(a, t0_ms=Q.onset(a, t), t1_ms=Q.onset(a, t) + 30) for k, t in KICK_ISO.items()}
    m["small"] = Q.small_speaker(a, "m_kick")
    m["small_b"] = Q.small_speaker(wavs["b_stabs"], "b_stabs")
    m["pat"] = Q.pattern_hits(a, KICK_PAT)
    m["pat_sd"] = float(np.std(m["pat"]))
    m["pat_span"] = float(max(m["pat"]) - min(m["pat"]))
    m["hits"] = Q.pattern_hits(a, KICK_ALL)
    off = 11650                                 # the last note-off
    wins = ((100, 300), (500, 700), (1500, 1700), (2300, 2500))
    m["floor"] = [noise_rms(a, off + x0, off + x1) for x0, x1 in wins]
    m["floor_voice"] = [noise_rms(voice, off + x0, off + x1) for x0, x1 in wins]
    m["dc_dbfs"] = float(20 * np.log10(max(np.abs(dc_of(a, 13900, 14400)).max(), 1e-3) / 32767))
    # the isolated A1 hit: -20 / -40 / -60 dB after the key-up, the DC subtracted; as rendered and the voice alone
    m["tail"] = M.tail_times(a, 4650, 60, 800, dc=dc_of(a, 5600, 5900))
    m["tail_voice"] = M.tail_times(voice, 4650, 60, 800, dc=dc_of(voice, 5600, 5900))
    # the hiss rests 2 s after the last note: its level against the hit it follows (dB), measured
    m["floor_re_hit"] = m["floor"][0] - M.rms_db(a, 11500, 11650)
    return m


# ---- 07: the splice ----------------------------------------------------------------------------------------------------------------
def measure_splice(exe, cg, spec, params, tag, wavs, quick):
    a = wavs["n_splice"]
    m = {}
    nt = {**params, "CHEW": 0}
    plain = K.render(exe, "n_splice", params=nt, tag="p_" + tag)[0] if params.get("CHEW") else a
    m["wobble"] = Q.wobble(a, 110.0, 6000, 8400)
    m["wobble_notape"] = Q.wobble(plain, 110.0, 6000, 8400)
    m["timbre"] = N.pwm_metrics(a, 6000, 8400, settle_ms=100)
    m["timbre_notape"] = N.pwm_metrics(plain, 6000, 8400, settle_ms=100)
    m["edges"] = Q.edges(a, SPL_STACC)
    m["edges_notape"] = Q.edges(plain, SPL_STACC)
    m["edges_short"] = Q.edges(a, SPL_SHORT)
    m["edges_short_notape"] = Q.edges(plain, SPL_SHORT)
    m["pair"] = {k: {e: Q.paired(m[f"edges{k}"][e]["vals"], m[f"edges{k}_notape"][e]["vals"]) for e in ("onset", "end")} for k in ("", "_short")}
    m["dips"] = M.dips(a, 6200, 8300)
    m["dips_notape"] = M.dips(plain, 6200, 8300)
    m["tail_held"] = M.tail_times(a, 8400, 120, 900, dc=dc_of(a, 9100, 9400))
    m["tail_short"] = M.tail_times(a, 4435, 60, 400, dc=dc_of(a, 5600, 5900))
    m["centroid_held"] = M.centroid(a, 6100, 8400)
    return m


# ---- 15: the chop ------------------------------------------------------------------------------------------------------------------
def measure_chop(exe, cg, spec, params, tag, wavs, quick):
    a = wavs["o_chop"]
    m = {"chop": Q.chop(a, 3300, 5300), "edge": Q.edge_rise(exe, params)}
    m["chop_riff"] = [Q.chop(a, on + 100, off) for on, off in ((6000, 6500), (6600, 7100), (7200, 7700))]
    m["first"] = Q.first_edge_spread(wavs["p_chopshort"], CHOP_SHORT)
    m["levels3"] = Q.level_shares(a, 3300, 5300)
    m["p_levels"] = K.level_metrics(wavs["p_chopshort"], "p_chopshort")
    return m


# ---- probes: the recommended variant with ONE knob stepped (numbers, not variants) ---------------------------------------------------------
def probe_rows(exe, spec, params):
    """{knob name: (column headers, [(value label, [cells])])} for the patch's probes"""
    slot, out = spec["slot"], {}
    if slot == 5:
        def kick_cells(p):
            a = K.render(exe, "m_kick", params=p, tag="pr")[0]
            lm = K.level_metrics(a, "m_kick")
            sp = Q.small_speaker(a, "m_kick")
            k1 = Q.kick_hit(a, 4500)
            hissy = p.get("TP_HISS", 64) > 0 and p.get("CHEW", 0) > 0     # (the hiss sits above the -60 dBFS onset threshold: the hit windows cannot be placed)
            return a, [f"{lm['rms']:.1f}", f"{lm['peak']:.1f}", "n/a (hiss)" if hissy else f"{N.crest_db(a, t0_ms=Q.onset(a, 4500), t1_ms=Q.onset(a, 4500) + 30):.1f}", f"{sp['60']:.1f} / {sp['100']:.1f}",
                       "n/a (hiss)" if hissy else f"{Q.share_above(k1['wins'][0], 3):.0f}", M.fmt_bands(M.band_split_phrase(a, "m_kick")), f"{noise_rms(a, 11750, 11950):.0f} / {noise_rms(a, 13950, 14150):.0f}"]
        hdr = ["level reading dBFS (VOLUME unchanged)", "peak dBFS", "A1 hit crest, first 30 ms (dB)", "kept after a 60 / 100 Hz high-pass (dB)", "click >400 Hz % (0-10 ms)",
               "band split % <60/60-150/150-400/400-1.2k/1.2k+", "floor +0.1 s / +2.4 s after the last note (dBFS)"]
        for nm, vals in (("CHEW", [0, 40, 80, 127]), ("TP_HISS", [0, 32, 64, 96]), ("GROWL", [0, 40, 76, 104]), ("NOISE", [0, 50, 110]), ("O1_LVL", [50, 70, 90, 110])):
            out[nm] = (hdr, [(str(v), kick_cells({**params, nm: v})[1]) for v in vals])
    elif slot == 7:
        hdr = ["wobble of the held A2: s.d. cents · range cents", "timbre (400-1.2k band): depth dB · rate Hz", "onset: mean ± s.d. ms (tape minus no tape, per note)", "dips >= 6 dB in a 12 s hold: n · deepest dB",
               "level reading dBFS (VOLUME unchanged)", "held A2 (6.1-8.4 s) band split % <60/60-150/150-400/400-1.2k/1.2k+ · centroid Hz"]
        def cells(p):
            a = K.render(exe, "n_splice", params=p, tag="pr")[0]
            nt = K.render(exe, "n_splice", params={**p, "CHEW": 0}, tag="pr2")[0] if p.get("CHEW") else a
            w = Q.wobble(a, 110.0, 6000, 8400)
            t = N.pwm_metrics(a, 6000, 8400, settle_ms=100)["bands"]["400-1.2k"]
            pr = Q.paired(Q.edges(a, SPL_STACC)["onset"]["vals"], Q.edges(nt, SPL_STACC)["onset"]["vals"])
            hd = Q.hold_dips(exe, p)
            return [f"{w['sd']:.1f} · {w['range']:.1f}", f"{t[0]:.1f} · {t[1]:.1f}", f"{pr['mean']:+.1f} ± {pr['sd']:.2f}", f"{hd['n']} · {hd['deepest']:.0f}", f"{K.level_metrics(a, 'n_splice')['rms']:.1f}",
                    f"{M.fmt_bands(M.band_shares(a, 6100, 8400))} · {M.centroid(a, 6100, 8400):.0f}"]
        for nm, vals in (("XMOD", [0, 40, 70, 100, 127]), ("CHEW", [0, 30, 60, 100, 127]), ("TP_DROPS", [0, 64, 90, 127])):
            out[nm] = (hdr, [(str(v), cells({**params, nm: v})) for v in vals])
    elif slot == 15:
        hdr = ["chop rate Hz", "depth dB (on - off)", "edge timing s.d. ms · period s.d. ms", "edge rise 10-90 % ms (A6 probe)", "start of the chop on 8 eighth-note notes: notes starting ON ; first edge mean ± s.d. ms",
               "level reading dBFS (VOLUME unchanged)"]
        def cells(p):
            a = K.render(exe, "o_chop", params=p, tag="pr")[0]
            c = Q.chop(a, 3300, 5300)
            ed = Q.edge_rise(exe, p)
            fe = Q.first_edge_spread(K.render(exe, "p_chopshort", params=p, tag="pr2")[0], CHOP_SHORT)
            return [f"{c['rate']:.2f}", f"{c['depth']:.1f}", f"{c['edge_sd']:.2f} · {c['period_sd']:.2f}", f"{ed['median']:.2f}", ("no edge inside the 110 ms gate" if not fe['n'] else f"{fe['n_on']} of {fe['n']} ON; {fe['mean']:.0f} ± {fe['sd']:.1f}"), f"{K.level_metrics(a, 'o_chop')['rms']:.1f}"]
        for nm, vals in (("LFO_AMP", [127, 110, 100, 80, 64]), ("VINTAGE", [0, 60, 127]), ("CHEW", [0, 30, 60, 100]), ("LFO_PHASE", [0, 1, 2]), ("LFO_RATE", [87, 95, 101, 104, 110])):
            out[nm] = (hdr, [(str(v), cells({**params, nm: v})) for v in vals])
    return out


def probe_table(name, hdr, rows):
    L = [f"| {name} | " + " | ".join(hdr) + " |", "|---|" + "---|" * len(hdr)]
    for v, cells in rows:
        L.append(f"| {v} | " + " | ".join(cells) + " |")
    return "\n".join(L)


def quick_line(spec, key, vol, m):
    lp = spec["level"]
    L = f"[{spec['slot']:02d}] {key} VOL {vol:3d} lvl {m['level']:6.1f} b {m['b_stabs']['rms']:6.1f} pk {m['peak_all']:5.1f} crest {m[lp]['crest']:4.1f} cent {m[lp]['centroid']:5.0f} bands {M.fmt_bands(m[lp]['bands'])}"
    if "kick" in m:
        L += f" | hp60 {m['small']['60']:.1f} hp100 {m['small']['100']:.1f} dB; A0/A1/A2 {[round(m['kick'][k]['rms'], 1) for k in m['kick']]} A1 click/body/tail >60Hz " + \
             "/".join(f"{Q.share_above(w, 1):.0f}" for w in m['kick']['A1']['wins']) + f" click>400 {Q.share_above(m['kick']['A1']['wins'][0], 3):.0f} hit30 {m['hit_crest30']['A1']:.1f}" + f" pat sd {m['pat_sd']:.2f} span {m['pat_span']:.1f} floor {m['floor'][0]:.0f}/{m['floor'][3]:.0f}"
    if "wobble" in m:
        L += f" | wobble {m['wobble']['sd']:.1f}c ({m['wobble_notape']['sd']:.1f} no tape) onset {m['edges']['onset']['mean']:.1f}±{m['edges']['onset']['sd']:.2f} ({m['edges_notape']['onset']['sd']:.2f}) end {m['edges']['end']['mean']:.1f}±{m['edges']['end']['sd']:.2f} dips {m['dips'][1]} deepest {m['dips'][0]:.0f}dB"
    if "chop" in m:
        c = m["chop"]
        L += f" | chop {c['rate']:.2f}Hz depth {c['depth']:.1f}dB duty {c['duty']:.2f} edge sd {c['edge_sd']:.2f}ms rise {m['edge']['median']:.2f}ms first-edge sd {m['first']['sd']:.1f}ms"
    return L


def tables(spec, R):
    ks = list(R)
    lp, slot = spec["level"], spec["slot"]
    L = ["| | " + " | ".join(f"**{k}** {R[k]['tag']}" for k in ks) + " |", "|---|" + "---|" * len(ks)]
    row = lambda name, f: L.append("| " + name.replace(" | ", " ; ") + " | " + " | ".join(f(R[k]).replace(" | ", " ; ") for k in ks) + " |")
    row("VOLUME (trim)", lambda r: str(r["volume"]))
    row(f"LEVEL READING ({spec['level_def']}), dBFS", lambda r: f1(r["level"]))
    row("vs the bank reference -18.0", lambda r: f"{r['level'] + 18.0:+.1f}")
    row("RMS on phrase (b), the bank's own reading", lambda r: f1(r["b_stabs"]["rms"]))
    row("difference (b) - level reading, dB", lambda r: f"{r['b_stabs']['rms'] - r['level']:+.1f}")
    row("K-weighted RMS, level phrase · phrase (b)", lambda r: f"{f1(r[lp]['rms_k'])} · {f1(r['b_stabs']['rms_k'])}")
    row("peak of any phrase, dBFS (limit <= -4) · which", lambda r: f"{f1(r['peak_all'])} · {r['peak_phrase']}")
    row("crest factor (peak/RMS over the note-on region, dB), level phrase · phrase (b)", lambda r: f"{r[lp]['crest']:.1f} · {r['b_stabs']['crest']:.1f}")
    row("RMS note-on region per phrase (" + " / ".join(p[0] for p in spec["phrases"]) + ")", lambda r: " / ".join(f1(r[p]["rms"]) for p in spec["phrases"]))
    row("centroid Hz (level phrase / b)", lambda r: f"{r[lp]['centroid']:.0f} / {r['b_stabs']['centroid']:.0f}")
    row("band split % <60 / 60-150 / 150-400 / 400-1.2k / 1.2k+ (level phrase)", lambda r: M.fmt_bands(r[lp]["bands"]))
    row("band split % (b)", lambda r: M.fmt_bands(r["b_stabs"]["bands"]))
    if slot == 7:
        row("attack, A5 probe from silence: key-down -> 10 % -> 90 % of the plateau (ms) · rise · early peak re plateau (dB)",
            lambda r: f"{r['attack']['as']['t10']:.1f} -> {r['attack']['as']['t90']:.1f} · {r['attack']['as']['rise']:.1f} · {r['attack']['as']['peak_re_plateau']:+.1f}")
        row("  level re plateau at 2 / 5 / 10 / 20 / 50 ms (dB)", lambda r: " / ".join(f"{r['attack']['as']['bloom'][k]:+.1f}" for k in ("2", "5", "10", "20", "50")))
    if slot == 5:
        for a_, nm in (("A0", "A0 27.5 Hz"), ("A1", "A1 55 Hz"), ("A2", "A2 110 Hz")):
            row(f"KICK {nm}, isolated hit: RMS over the 150 ms gate (dBFS) · band split % in 0-10 ms (click) | 10-50 ms (body) | 50-150 ms (tail)",
                lambda r, a_=a_: f"{r['kick'][a_]['rms']:.1f} · " + " ; ".join(Q.fmt_list(w) for w in r["kick"][a_]["wins"]))
        row("  share of energy ABOVE 60 Hz in click | body | tail, A0 / A1 / A2 (%)", lambda r: " / ".join(" | ".join(f"{Q.share_above(w, 1):.0f}" for w in r["kick"][a_]["wins"]) for a_ in ("A0", "A1", "A2")))
        row("  click (0-10 ms) share above 400 Hz, A0 / A1 / A2 (%)", lambda r: " / ".join(f"{Q.share_above(r['kick'][a_]['wins'][0], 3):.0f}" for a_ in ("A0", "A1", "A2")))
        row("  voice alone (CHEW and GROWL off): share above 60 Hz in click | body | tail, A1 (%)", lambda r: " | ".join(f"{Q.share_above(w, 1):.0f}" for w in r["kick_voice"]["A1"]["wins"]))
        row("ATTACK of each isolated hit (0.5 ms peak envelope): key-down -> 10 % of the peak · 90 % of the peak · the peak (ms), A0 / A1 / A2",
            lambda r: " / ".join(f"{r['hit_attack'][k]['t_start']:.1f} · {r['hit_attack'][k]['t90']:.1f} · {r['hit_attack'][k]['t_peak']:.1f}" for k in ("A0", "A1", "A2")))
        row("  the click: RMS of the first 5 ms re the body (10-50 ms), A0 / A1 / A2 (dB; 0 = as loud as the body, positive = a spike)", lambda r: " / ".join(f"{r['kick'][k]['click_re_body']:+.1f}" for k in ("A0", "A1", "A2")))
        row("what a small speaker keeps: the kick phrase after a 2nd-order high-pass at 60 / 100 Hz, re the unfiltered level (dB)", lambda r: f"{r['small']['60']:.1f} / {r['small']['100']:.1f}")
        row("  same on phrase (b)", lambda r: f"{r['small_b']['60']:.1f} / {r['small_b']['100']:.1f}")
        row("overload: crest factor of the first 30 ms of each hit, A0 / A1 / A2 (dB; sine 3, saw 4.8, a clipped note lower)", lambda r: " / ".join(f"{r['hit_crest30'][k]:.1f}" for k in ("A0", "A1", "A2")))
        row("the 8 pattern hits (A1, 4 a bar, 120 BPM): RMS of each hit (dBFS)", lambda r: " ".join(f"{v:.1f}" for v in r["pat"]))
        row("  hit-to-hit: s.d. · span (dB) (tape dropouts show as a dip)", lambda r: f"{r['pat_sd']:.2f} · {r['pat_span']:.1f}")
        row("tape dropouts: 48 hits of A1 (24 s): hits more than 3 dB · 6 dB under the median hit · the deepest dip (dB)", lambda r: f"{r['drops']['n3']} · {r['drops']['n6']} · {r['drops']['deepest']:.1f}")
        row("noise floor after the last note-off, DC removed, +0.1 / +0.5 / +1.5 / +2.4 s (dBFS), as rendered", lambda r: " / ".join(fl(v) for v in r["floor"]))
        row("  voice alone (CHEW and GROWL off)", lambda r: " / ".join(fl(v) for v in r["floor_voice"]))
        row("  first floor reading re the last hit's RMS (dB)", lambda r: "-" if r["floor"][0] < -150 else f"{r['floor_re_hit']:.0f}")
        row("tail of the isolated A1 hit after the key-up: -20 / -40 / -60 dB (ms), DC subtracted, as rendered", lambda r: f"{f1(r['tail']['t20'], 0)} / {f1(r['tail']['t40'], 0)} / {f1(r['tail']['t60'], 0)}")
        row("  voice alone", lambda r: f"{f1(r['tail_voice']['t20'], 0)} / {f1(r['tail_voice']['t40'], 0)} / {f1(r['tail_voice']['t60'], 0)}")
        row("constant DC left after the last note (dBFS)", lambda r: f1(r["dc_dbfs"], 0))
    if slot == 7:
        row("WOBBLE of the held A2 (6.0-8.4 s): pitch s.d. · 5-95 % range (cents) · strongest rate (Hz)", lambda r: f"{r['wobble']['sd']:.1f} · {r['wobble']['range']:.1f} · {r['wobble']['rate']:.2f}" + (f" (tracker kept {100 * r['wobble']['kept']:.0f} % of frames: unreliable)" if r['wobble']['kept'] < 0.9 else ""))
        row("  the same without the tape (CHEW 0): the cross-mod / LFO / slop alone", lambda r: f"{r['wobble_notape']['sd']:.1f} · {r['wobble_notape']['range']:.1f} · {r['wobble_notape']['rate']:.2f}")
        row("X-MOD timbre wobble, held A2: depth dB (95-5 %) · rate Hz, in the 150-400 | 400-1.2k | 1.2k-3k bands",
            lambda r: " | ".join(f"{r['timbre']['bands'][b][0]:.1f} · {r['timbre']['bands'][b][1]:.1f}" for b in ("150-400", "400-1.2k", "1.2k-3k")))
        row("  without the tape", lambda r: " | ".join(f"{r['timbre_notape']['bands'][b][0]:.1f} · {r['timbre_notape']['bands'][b][1]:.1f}" for b in ("150-400", "400-1.2k", "1.2k-3k")))
        row("EDGES, 12 staccato notes (60 ms gate): onset (note-on -> -20 dB of the note's body) mean ± s.d. (ms)", lambda r: f"{r['edges']['onset']['mean']:.1f} ± {r['edges']['onset']['sd']:.2f}")
        row("  the same without the tape", lambda r: f"{r['edges_notape']['onset']['mean']:.1f} ± {r['edges_notape']['onset']['sd']:.2f}")
        row("  the TAPE's own timing jitter: per-note onset difference (tape minus none): mean · s.d. · range (ms)", lambda r: f"{r['pair']['']['onset']['mean']:+.2f} · {r['pair']['']['onset']['sd']:.2f} · {r['pair']['']['onset']['min']:+.1f}..{r['pair']['']['onset']['max']:+.1f}")
        row("  end of the note (note-off -> -40 dB of the body), mean ± s.d. (ms); the tape's per-note difference mean · s.d.", lambda r: f"{r['edges']['end']['mean']:.1f} ± {r['edges']['end']['sd']:.2f}; {r['pair']['']['end']['mean']:+.2f} · {r['pair']['']['end']['sd']:.2f}")
        row("  3 short A3 notes (80 ms): the tape's onset difference mean · s.d. (ms)", lambda r: f"{r['pair']['_short']['onset']['mean']:+.2f} · {r['pair']['_short']['onset']['sd']:.2f}")
        row("dropouts in the held A2 (2.1 s): dips of 6 dB or more · deepest (dB); without the tape", lambda r: f"{r['dips'][1]} · {r['dips'][0]:.0f}; {r['dips_notape'][1]} · {r['dips_notape'][0]:.0f}")
        row("tail after the 2.4 s held A2: -20 / -40 / -60 dB (ms) · after a 60 ms staccato note", lambda r: f"{f1(r['tail_held']['t20'], 0)} / {f1(r['tail_held']['t40'], 0)} / {f1(r['tail_held']['t60'], 0)} · {f1(r['tail_short']['t20'], 0)} / {f1(r['tail_short']['t40'], 0)} / {f1(r['tail_short']['t60'], 0)}")
        row("LFO: the pitch LFO's nominal rate (Hz) · peak depth (cents; PITCH law (d*d)>>7 x 9.4)", lambda r: f"{r['lfo_hz']:.2f} · {((r['params']['LFO_PITCH'] ** 2) >> 7) * 9.4:.0f}")
    if slot == 15:
        def chopcell(r):
            c = r["chop"]
            if c["rate"] != c["rate"] or r["params"]["LFO_AMP"] == 0:
                return "no chop (LFO AMP 0)"
            return f"{c['rate']:.2f} Hz (LFO RATE {r['params']['LFO_RATE']} = {r['lfo_hz']:.2f}) · on {c['on_db']:.1f} / off {c['off_db']:.1f} dBFS"
        row("CHOP on the held A3 (3.3-5.3 s): measured rate · on / off levels", chopcell)
        row("  DEPTH: level swing between the on and the off parts (dB)", lambda r: "-" if r["params"]["LFO_AMP"] == 0 else f"{r['chop']['depth']:.1f}")
        row("  on-time (share of a cycle above the midpoint)", lambda r: "-" if r["params"]["LFO_AMP"] == 0 else f"{r['chop']['duty']:.2f}")
        row("  EDGE HARDNESS: rise 10 -> 90 % of a chop edge, A6 probe, median (ms; the window is one period, 0.57 ms: an upper bound)", lambda r: "-" if r["params"]["LFO_AMP"] == 0 else f"{r['edge']['median']:.2f}")
        row("  EDGE TIMING JITTER: s.d. of the rising edges about a straight line (ms; the reading's own resolution is 0.5 ms) · period s.d. (ms)", lambda r: "-" if r["params"]["LFO_AMP"] == 0 else f"{r['chop']['edge_sd']:.2f} · {r['chop']['period_sd']:.2f}")
        row("share of the held A3's time at: off (> 30 dB under the top) ; one voice (4-12 dB under) ; full (within 4 dB), %", lambda r: "-" if r["params"]["LFO_AMP"] == 0 else f"{r['levels3'][0]:.0f} ; {r['levels3'][1]:.0f} ; {r['levels3'][2]:.0f}")
        row("chop rate on the three long riff notes (Hz)", lambda r: "-" if r["params"]["LFO_AMP"] == 0 else " / ".join("-" if c['rate'] != c['rate'] else f"{c['rate']:.2f}" for c in r["chop_riff"]))
        row("where the chop starts on each note (phrase p, 8 eighth-note notes, 110 ms gate): notes starting ON · time to the first chop edge (ms)", lambda r: "-" if r["params"]["LFO_AMP"] == 0 else f"{r['first']['n_on']} of {r['first']['n']} start ON; first edge {r['first']['mean']:.0f} ± {r['first']['sd']:.1f} ms")
        row("level reading on the short-note phrase (p), dBFS", lambda r: f1(r["p_levels"]["rms"]))
    row("largest sample step dBFS (per phrase)", lambda r: " / ".join(f"{r['step_db'][p]:.0f}" for p in spec["phrases"]))
    row("clipped samples", lambda r: str(r["clip"]))
    if R[ks[0]]["cost"]:
        row("cost: host instr/sample, phrase (b)", lambda r: f"{r['cost']['b']:.0f}")
        row("cost idle (always-on stages)", lambda r: f"{r['cost']['idle']:.0f}")
        row(f"cost under load ({spec['load']}), on top of idle", lambda r: f"{r['cost']['load']:.0f}")
        row("cost worst case = idle + load", lambda r: f"{r['cost']['idle'] + r['cost']['load']:.0f}")
        if slot == 5:
            row("  idle cost with CHEW off · with GROWL off · voice alone (both off)", lambda r: f"{r['cost']['no_chew']:.0f} · {r['cost']['no_growl']:.0f} · {r['cost']['voice']:.0f}")
            row("  so CHEW costs · GROWL costs (idle host instr/sample)", lambda r: f"{r['cost']['idle'] - r['cost']['no_chew']:.0f} · {r['cost']['idle'] - r['cost']['no_growl']:.0f}")
    return "\n".join(L)


def readme(spec, R, probe=None):
    L = [f"# {spec['slot']:02d} {spec['name']} — voicing round (Batch 3B, the wreck and chop set)\n",
         f"*Generated by tests/voicing/batch03b.py. Level reading: {spec['level_def']}; matched to the bank reference (-18.0 dBFS RMS) by VOLUME; phrase (b)'s reading is in the table too. "
         f"Every change is before -> after under the echo rule. WAVs are on the listen/batch-03b-chapter1-wreck-and-chop branch only.*\n",
         f"**Recommended: {spec['recommend']}** - " + spec.get("why", lambda R, P: "")(R, probe) + "\n", "## What to listen to\n", spec.get("listen", "") + "\n", "## The variants\n"]
    for k, r in R.items():
        L.append(f"**{k} {r['tag']}** — {r['desc']}\n")
        L.append("\n".join(f"- {c}" for c in r["changes"]) or "- (none: the original)")
        L.append("")
    L += ["## The numbers\n", tables(spec, R)]
    for nm, (hdr, rows) in (probe or {}).items():
        L += [f"\n### What {nm} does on this patch (the recommended variant, {nm} stepped, probe renders, not variants)\n", probe_table(nm, hdr, rows)]
    nt = spec.get("notes", "")
    L += ["\n" + (nt(R, probe) if callable(nt) else nt)]
    return "\n".join(L) + "\n"


def write_all(spec, R, probe, d):
    json.dump({"variants": {k: dict(r) for k, r in R.items()}}, open(os.path.join(d, "results.json"), "w"), indent=1,
              default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o))
    json.dump(probe, open(os.path.join(d, "probe.json"), "w"), default=float)
    open(os.path.join(d, "README.md"), "w").write(readme(spec, R, probe))
    with open(os.path.join(d, "numbers.md"), "w") as f:
        f.write(f"# generated by tests/voicing/batch03b.py -- slot {spec['slot']:02d} {spec['name']}\n\n")
        for k, r in R.items():
            f.write(f"**{k} {r['tag']}** — {r['desc']}\n\n" + ("\n".join(f"- {c}" for c in r["changes"]) or "- (none: the original)") + "\n\n")
        f.write(tables(spec, R) + "\n")
        for nm, (hdr, rows) in probe.items():
            f.write(f"\n### {nm} probe\n\n" + probe_table(nm, hdr, rows) + "\n")


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
        probe = probe_rows(exe, spec, R[spec["recommend"][0]]["params"])
        write_all(spec, R, probe, d)
        print(f"[{slot:02d}] written {d}")
    return R


def write_index():
    """listen/voicing/batch-03b/README.md: one table per patch from the saved results.json files"""
    L = ["# Batch 3B — the wreck and chop set: 05 ZEAROX, 07 Tape Splice, 15 Trem Chop\n",
         "*Generated by `tests/voicing/batch03b.py --readme`. Each folder: `A` original (through the base program path), `B` centre (the recommended variant is the committed patch), `C`, `D` along the axes named in its README. "
         "WAV names: `<variant>_<tag>_<phrase>.wav`, phrases riff / stabs / held (the pilot phrases) and the patch's own (kick = m, splice = n, chop = o, chopshort = p). The WAVs are on the "
         "`listen/batch-03b-chapter1-wreck-and-chop` branch only; the full tables (`README.md`, `numbers.md`, `results.json`) are in each folder and on the voicing branch. Level: matched to -18.0 dBFS RMS on the patch's level phrase.*\n"]
    for spec in PATCHES:
        f = os.path.join(OUT, spec["dir"], "results.json")
        if not os.path.exists(f):
            continue
        R = json.load(open(f))["variants"]
        L.append(f"## {spec['slot']:02d} {spec['name']} — level read on: {spec['level_def']}\n")
        L.append("| | variant | VOLUME | level | (b) | peak any phrase | centroid (level phrase) | worst-case CPU | what it is |\n|---|---|---|---|---|---|---|---|---|")
        for k, r in R.items():
            c = r.get("cost")
            L.append(f"| {k} | {r['tag']} | {r['volume']} | {r['level']:.1f} | {r['b_stabs']['rms']:.1f} | {r['peak_all']:.1f} | {r[spec['level']]['centroid']:.0f} Hz | {(c['idle'] + c['load']) if c else float('nan'):.0f} | {r['desc']} |")
        L.append("")
    open(os.path.join(OUT, "README.md"), "w").write("\n".join(L) + "\n")


BRIEFS = {
    5: ("a blown-out, lo-fi kick substitute. A cranked sub with noise over the top, pushed through maximum tape degrade; it overloads on every downbeat, each note hits like a blown speaker. The kick feel must be carried by the click and "
        "the mid-range body (60-1.2k Hz), the true sub a bonus: under 60 Hz is inaudible on small speakers. The noise should be gated with the note as far as existing controls allow.*\nClosest to: an 808-style kick smashed onto a blown-out cassette 4-track "
        "(TR-808 kick sub/thump, SH-101 sub/thick, Portastudio lo-fi/noisy, ProCo RAT crunchy/driven)."),
    7: ("a fat square with an X-mod pitch wobble, chopped by the gate, with tape degrade adding splice jitter. Nervous and glitching, broken, unreliable; fast release, short gates.*\nClosest to: a Mono/Poly cross-mod square through a worn tape echo "
        "(Mono/Poly fat/drifting, Prophet-5 wobble/nervous, RE-201 wobble/lo-fi, SH-101 punchy)."),
    15: ("a broken-strobe tremolo. A bright saw, a hard SQUARE-shaped LFO on the amp for a choppy on/off stutter (not a gentle sine), plus a touch of slop so the chop edges waver: a broken strobe, not a tidy trem.*\nClosest to: an SH-101 saw through a TR-2 on square "
         "(SH-101 bright/punchy, Boss TR-2 square choppy/gated, Pulsar choppy/rhythmic, Polysix drift)."),
}
AXES = {5: "where the kick lives (the sub OSC 1 LEVEL against the click NOISE / filter envelope: B body, C click) and the amount of overload (GROWL 104 against 55: B blown, D tamer); CHEW stays at the top in all (the brief), its effect is in the CHEW probe",
        7: "X-MOD depth, the pitch LFO and the tape together against how glitchy / jittery it gets (B centre, C glitchy, D gentle); probes for X-MOD, CHEW and DROPS alone",
        15: "how much the chop edges waver (B: LFO PHASE SYNC, tidy; C: PHASE FREE, the chop does not know where the note began; D: DUAL with PHASE SPREAD, the two voices of a note an eighth of a cycle apart); rate and depth are in the probes (RATE 87-110, AMP 127-64)"}


def write_log(spec, R, proof, probe):
    slot, rk = spec["slot"], spec["recommend"][0]
    r = R[rk]
    L = [f"# Voicing log — {slot:02d} \"{spec['name']}\" (FACTORY[{slot - 1}], Batch 3B, the wreck and chop set)\n",
         f"5 Nov 2026. Brief (Batch 3B, Chapter {'II' if slot == 15 else 'I'}): *{BRIEFS[slot]} Method and kit: `README.md` here (§1 phrases, §3 loudness, §14 Batch 3B).\n",
         f"## RECOMMENDED: variant {rk} ({r['tag']}) — committed as the patch, awaiting Vincent's listening\n",
         f"**Status: round 1 rendered, not yet heard.** Variant {rk} is committed as `{'PF_' + spec['cname']}` in `firmware/src/obv_patches.h` (equals variant {rk} byte for byte: `tests/voicing/check_slot.py {slot} {rk} 3b`); A, C, D are render-only. "
         f"**Round count so far: 1 silent measured round (variants fixed by sweeps of the existing controls, not for ears) + 1 listening round pending.** No voice card and no reference-renders yet (after approval). WAVs: the never-merged `listen/batch-03b-chapter1-wreck-and-chop` branch, `listen/voicing/batch-03b/{spec['dir']}/`.\n",
         f"* **Axes chosen:** {AXES[slot]}.",
         f"* **Final values (variant {rk}), each change before -> after (the original is the nearest-base patch as it stood):**\n"]
    L += [f"* {c}" for c in r["changes"]]
    cs = r["cost"]
    L += ["", f"* **Level:** VOLUME {r['volume']}; **{r['level']:.1f} dBFS RMS** on the level phrase ({spec['level_def']}); phrase (b) {r['b_stabs']['rms']:.1f} ({r['b_stabs']['rms'] - r['level']:+.1f} dB), K-weighted (b) {r['b_stabs']['rms_k']:.1f}; "
          f"peak {r['peak_all']:.1f} dBFS ({r['peak_phrase']}); crest {r[spec['level']]['crest']:.1f} dB on the level phrase; worst-case CPU {cs['idle'] + cs['load']:.0f} host instr/sample (idle {cs['idle']:.0f} + load {cs['load']:.0f}; the original {R['A']['cost']['idle'] + R['A']['cost']['load']:.0f}).",
          f"* **Measured on the recommended variant** (full tables: `listen/voicing/batch-03b/{spec['dir']}/README.md`): " + spec["why"](R, probe),
          "* **Device build:** not run (no JieLi toolchain in this environment); the change is parameter arrays only. The render time on the device is not measured.",
          f"* **Other programs:** {proof}"]
    open(os.path.join(K.ROOT, "dog5-docs", "voicing", f"{slot:02d}-{spec['dir'][3:]}.md"), "w").write("\n".join(L) + "\n")


def main():
    if "--logs" in sys.argv:
        proof = sys.argv[sys.argv.index("--logs") + 1]
        for spec in PATCHES:
            R = json.load(open(os.path.join(OUT, spec["dir"], "results.json")))["variants"]
            write_log(spec, R, proof, json.load(open(os.path.join(OUT, spec["dir"], "probe.json"))))
        print("logs written")
        return
    if "--emit" in sys.argv:
        slot, key = int(sys.argv[sys.argv.index("--emit") + 1]), sys.argv[sys.argv.index("--emit") + 2]
        spec = [p for p in PATCHES if p["slot"] == slot][0]
        res = json.load(open(os.path.join(OUT, spec["dir"], "results.json")))
        print(B.emit(spec["cname"], res["variants"][key]["params"]))
        return
    if "--readme" in sys.argv:                    # rewrite README.md / numbers.md from results.json + probe.json (text edits, no renders)
        for spec in PATCHES:
            d = os.path.join(OUT, spec["dir"])
            if not os.path.exists(os.path.join(d, "results.json")):
                continue
            R = json.load(open(os.path.join(d, "results.json")))["variants"]
            probe = json.load(open(os.path.join(d, "probe.json")))
            write_all(spec, R, probe, d)
        write_index()
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
