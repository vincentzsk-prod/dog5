#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""05 ZEAROX, ROUND 2 (new direction: a pixelated, gritty, hard black-and-white kick substitute; square/pulse only, attack 0, no tape, light on CPU).

  python3 tests/voicing/batch03b_r2.py [--quick] [--no-cost]       -> listen/voicing/batch-03b/round2/05-zearox/ (WAVs only ever on the listen branch)
  python3 tests/voicing/batch03b_r2.py --emit KEY                  -> the C array of a variant (from results.json)

Round 1's variants are rejected (muddy); the diagnosis is tests/voicing/diag05.py (listen/voicing/batch-03b/round2/diagnosis.md).  Variants:
  A  07 Tape Splice C exactly as rendered, on the kick phrase m at the bank level (what was liked; heavy because of the tape)
  B  A with the tape removed (CHEW 0, HISS 0, DROPS 0)
  C  B reshaped as a kick: pulse waves only, a square body swept down by the filter envelope (ENV>O2), a quiet FM'd pulse under it, DRIVE 127 (hard clip), an open filter,
     attack 0, no sustain, a random stepped (S&H) pitch LFO = the glitch
  D  C at its lightest: ONE square (OSC 1 off), no X-MOD, no DRIVE
Measures: batch03b_metrics.py + diag05.py (two-level, HF share, flatness, MUD ratio, windows 0-20 / 20-100 / 100-300 ms)."""
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
import batch03b_metrics as Q
import diag05 as D
from batch03b_variants import PATCHES

OUT = os.path.join(K.ROOT, "listen", "voicing", "batch-03b", "round2", "05-zearox")
SPEC = [p for p in PATCHES if p["slot"] == 5][0]
R7 = json.load(open(os.path.join(K.ROOT, "listen", "voicing", "batch-03b", "07-tape-splice", "results.json")))["variants"]
R1 = json.load(open(os.path.join(K.ROOT, "listen", "voicing", "batch-03b", "05-zearox", "results.json")))["variants"]
PH = ["a_riff", "b_stabs", "c_held", "m_kick"]
SHORT = {"a_riff": "riff", "b_stabs": "stabs", "c_held": "held", "m_kick": "kick"}
KICK_PAT = [8000 + 500 * i for i in range(8)]

A07 = R7["C"]["params"]                                       # 07 Tape Splice C, exactly
NOTAPE = {**A07, "CHEW": 0, "TP_HISS": 0, "TP_DROPS": 0}
KICK_C = {**NOTAPE, "O1_WAVE": 2, "O2_WAVE": 2, "O1_PW": 64, "O2_PW": 64, "O1_LVL": 40, "O2_LVL": 127, "O2_SEMI": 36, "ENV_O2": 110, "XMOD": 127, "NOISE": 0,
          "DRIVE": 127, "RESO": 0, "FTYPE": 0, "CUTOFF": 105, "KEYTRK": 0, "FENV_AMT": 64, "FA": 0, "FD": 40, "FS": 0, "AA": 0, "AD": 76, "AS": 0, "AR": 20, "GLIDE": 0,
          "LFO_SHAPE": 4, "LFO_PHASE": 1, "LFO_RATE": 120, "LFO_PITCH": 80}
KICK_D = {**KICK_C, "O1_WAVE": 0, "XMOD": 0, "DRIVE": 0}
VARIANTS = [("A", "07C", "07 Tape Splice C exactly as rendered (X-MOD 100, random pitch LFO 22, pulse waves, CHEW 127, DROPS 110), on the kick phrase at the bank level: what was liked", A07),
            ("B", "notape", "A with the tape removed (CHEW 0, HISS 0, DROPS 0), level re-trimmed", NOTAPE),
            ("C", "kick", "B reshaped as a kick: pulse only, a swept square body, a quiet FM'd pulse, DRIVE 127, open filter, attack 0, S&H pitch LFO as the glitch", KICK_C),
            ("D", "light", "C at its lightest: one square, no X-MOD, no DRIVE", KICK_D)]


def measure(exe, cg, key, params, quick):
    wavs = {ph: K.render(exe, ph, params=params, tag="r2")[0] for ph in PH}
    a = wavs["m_kick"]
    m = {}
    for ph in PH:
        m[ph] = K.level_metrics(wavs[ph], ph)
        m[ph].update(K.tone_metrics(wavs[ph], ph))
        m[ph]["bands"] = M.band_split_phrase(wavs[ph], ph)
        m[ph]["crest"] = N.crest_db(wavs[ph], ph)
    m["peak_all"] = max(m[ph]["peak"] for ph in PH)
    m["peak_phrase"] = max(PH, key=lambda ph: m[ph]["peak"])
    m["clip"] = int(sum((np.abs(w) >= 32767).sum() for w in wavs.values()))
    m["level"] = m["m_kick"]["rms"]
    m["small"] = Q.small_speaker(a, "m_kick")
    m["hits"] = {nm: D.hit_row(a, t) for nm, t in (("A0", 3000), ("A1", 4500), ("A2", 6000))}
    m["kick"] = {nm: Q.kick_hit(a, t) for nm, t in (("A0", 3000), ("A1", 4500), ("A2", 6000))}
    m["pat"] = Q.pattern_hits(a, KICK_PAT)
    cs = []
    for t in KICK_PAT:
        t0 = Q.onset(a, t)
        cs.append(M.centroid(a, t0, t0 + 60, nfft=1024))
    m["spread"] = float(100 * np.std(cs) / np.mean(cs))
    m["hit_crest30"] = {nm: N.crest_db(a, t0_ms=Q.onset(a, t), t1_ms=Q.onset(a, t) + 30) for nm, t in (("A0", 3000), ("A1", 4500), ("A2", 6000))}
    m["attack"] = {nm: Q.hit_attack(a, t) for nm, t in (("A0", 3000), ("A1", 4500), ("A2", 6000))}
    m["dc_dbfs"] = float(20 * np.log10(max(np.abs(a[N._s(13900):N._s(14400)].mean(0)).max(), 1e-3) / 32767))
    m["cost"] = None
    if cg:
        ir, fr = K.callgrind_ips(cg, "x_stress", params=params, tag=key + "i", notes=False)
        on, _ = K.callgrind_ips(cg, "x_stress", params=params, tag=key + "o")
        m["cost"] = {"idle": ir / fr, "load": (on - ir) / (4.65 * K.FS)}
    return wavs, m


def cost_of(cg, params, tag):
    ir, fr = K.callgrind_ips(cg, "x_stress", params=params, tag=tag + "i", notes=False)
    on, _ = K.callgrind_ips(cg, "x_stress", params=params, tag=tag + "o")
    idle, load = ir / fr, (on - ir) / (4.65 * K.FS)
    return idle, load


def f1(x, p=1):
    return "-" if x is None or (isinstance(x, float) and (x != x or x < -150)) else f"{x:.{p}f}"


def table(R):
    ks = list(R)
    L = ["| | " + " | ".join(f"**{k}** {R[k]['tag']}" for k in ks) + " |", "|---|" + "---|" * len(ks)]
    row = lambda name, f: L.append("| " + name + " | " + " | ".join(f(R[k]).replace(" | ", " ; ") for k in ks) + " |")
    row("VOLUME (trim)", lambda r: str(r["volume"]))
    row("LEVEL READING (RMS over the note-on region of the kick phrase m, 11 hits x 150 ms), dBFS", lambda r: f1(r["level"]))
    row("RMS on phrase (b) · difference (b) - level reading, dB", lambda r: f"{r['b_stabs']['rms']:.1f} · {r['b_stabs']['rms'] - r['level']:+.1f}")
    row("K-weighted RMS, kick phrase · phrase (b)", lambda r: f"{r['m_kick']['rms_k']:.1f} · {r['b_stabs']['rms_k']:.1f}")
    row("peak of any phrase, dBFS (limit <= -4) · which", lambda r: f"{r['peak_all']:.1f} · {r['peak_phrase']}")
    row("crest factor over the kick phrase's note-on region · first 30 ms of an A1 hit (dB)", lambda r: f"{r['m_kick']['crest']:.1f} · {r['hit_crest30']['A1']:.1f}")
    row("centroid Hz (kick phrase / b)", lambda r: f"{r['m_kick']['centroid']:.0f} / {r['b_stabs']['centroid']:.0f}")
    row("band split % <60 / 60-150 / 150-400 / 400-1.2k / 1.2k+ (kick phrase)", lambda r: M.fmt_bands(r["m_kick"]["bands"]))
    for nm in ("A0", "A1", "A2"):
        row(f"{nm}: band split in 0-20 ms ; 20-100 ms ; 100-300 ms", lambda r, nm=nm: " ; ".join(Q.fmt_list(w) for w in r["hits"][nm]["wins"]))
    row("MUD = 150-400 Hz share / 1.2 kHz+ share, A1: 0-20 / 20-100 / 100-300 ms (lower = less body, more edge)", lambda r: " / ".join(f"{v:.1f}" for v in r["hits"]["A1"]["r_mud"]))
    row("BLACK AND WHITE: share of samples within 10 % of the rail, first 100 ms, A0 / A1 / A2 (%)", lambda r: " / ".join(f"{r['hits'][n]['two']:.0f}" for n in ("A0", "A1", "A2")))
    row("PIXELATED: share of the energy above 1.2 kHz, first 100 ms, A0 / A1 / A2 (%) · spectral flatness 100 Hz-10 kHz, A1", lambda r: " / ".join(f"{r['hits'][n]['hf100']:.1f}" for n in ("A0", "A1", "A2")) + f" · {r['hits']['A1']['flat']:.4f}")
    row("click (0-10 ms) share above 400 Hz, A0 / A1 / A2 (%)", lambda r: " / ".join(f"{Q.share_above(r['kick'][n]['wins'][0], 3):.0f}" for n in ("A0", "A1", "A2")))
    row("what a small speaker keeps: kick phrase after a 60 / 100 Hz high-pass (dB)", lambda r: f"{r['small']['60']:.1f} / {r['small']['100']:.1f}")
    row("TAIL of each isolated hit after the key-up: -40 / -60 dB (ms, DC subtracted), A0 / A1 / A2", lambda r: " / ".join(f"{r['hits'][n]['tail40']:.0f} / {r['hits'][n]['tail60']:.0f}" for n in ("A0", "A1", "A2")))
    row("level of A1 over time (RMS of 20 ms windows at +0 / 40 / 80 / 120 ms from the onset, dBFS)", lambda r: " ".join(f"{v:.0f}" for v in r["decay"]))
    row("ATTACK A1 (0.5 ms peak envelope): to 10 % · 90 % · peak (ms)", lambda r: f"{r['attack']['A1']['t_start']:.1f} · {r['attack']['A1']['t90']:.1f} · {r['attack']['A1']['t_peak']:.1f}")
    row("the glitch: hit-to-hit spread of the first-60-ms centroid over the 8 pattern hits (s.d. / mean, %)", lambda r: f"{r['spread']:.0f}")
    row("the 8 pattern hits (A1): RMS of each (dBFS)", lambda r: " ".join(f"{v:.1f}" for v in r["pat"]))
    row("clipped samples", lambda r: str(r["clip"]))
    if R[ks[0]].get("cost"):
        row("CPU: host instr/sample idle · under load · worst case = idle + load", lambda r: f"{r['cost']['idle']:.0f} · {r['cost']['load']:.0f} · {r['cost']['idle'] + r['cost']['load']:.0f}")
    return "\n".join(L)


def main():
    quick = "--quick" in sys.argv
    exe = K.build_host()
    D.exe = exe
    if "--emit" in sys.argv:
        key = sys.argv[sys.argv.index("--emit") + 1]
        res = json.load(open(os.path.join(OUT, "results.json")))["variants"][key]["params"]
        print(B.emit("ZEAROX", res))
        return
    cg = None if (quick or "--no-cost" in sys.argv) else K.callgrind_exe()
    R = {}
    os.makedirs(OUT, exist_ok=True)
    for key, tag, desc, params in VARIANTS:
        v, _ = B2.trim_volume(exe, SPEC, params)
        p = {**params, "VOLUME": v}
        wavs, m = measure(exe, cg, key, p, quick)
        a = wavs["m_kick"]
        t0 = Q.onset(a, 4500)
        m["decay"] = [M.rms_db(a, t0 + t, t0 + t + 20) for t in (0, 40, 80, 120)]
        base = B.resolve(os.path.join(K.ROOT, "build", "voicing", "base"), 5)
        m.update(tag=tag, desc=desc, volume=v, params=p,
                 changes=[B2.change(k, base[k], x, p) for k, x in p.items() if x != base[k]],
                 changes_vs_A=[B2.change(k, R['A']['params'][k], x, p) for k, x in p.items() if key != 'A' and x != R['A']['params'][k]])
        R[key] = m
        if not quick:
            for ph in PH:
                K.write_wav(os.path.join(OUT, f"{key}_{tag}_{SHORT[ph]}.wav"), wavs[ph][int(K.T_CUT * K.FS):])
        h = m["hits"]["A1"]
        print(f"{key} {tag:7s} VOL {v:3d} lvl {m['level']:.1f} (b){m['b_stabs']['rms']:.1f} pk {m['peak_all']:.1f} crest {m['m_kick']['crest']:.1f} two {'/'.join(f'{m['hits'][n]['two']:.0f}' for n in ('A0','A1','A2'))} "
              f"hf {h['hf100']:.1f} mud {h['r_mud'][1]:.1f} tail60 {h['tail60']:.0f} hp100 {m['small']['100']:.1f} spread {m['spread']:.0f}" +
              (f" cpu {m['cost']['idle'] + m['cost']['load']:.0f}" if m['cost'] else ""), flush=True)
    if quick:
        return
    # ---- element costs on C (idle + load), one element removed at a time ------------------------------------------------------
    abl = [("C as it is", {}), ("DRIVE 127 -> 0", {"DRIVE": 0}), ("X-MOD 127 -> 0", {"XMOD": 0}), ("OSC 1 off (one oscillator)", {"O1_WAVE": 0, "XMOD": 0}),
           ("pitch LFO 80 -> 0", {"LFO_PITCH": 0}), ("DRIVE, X-MOD, OSC 1 all off (= D)", {"DRIVE": 0, "XMOD": 0, "O1_WAVE": 0}), ("saw + saw instead of pulse", {"O1_WAVE": 1, "O2_WAVE": 1}),
           ("GROWL 104 added (round 1)", {"GROWL": 104, "GRL_BIAS": 72, "GRL_TONE": 64}), ("CHEW 127 added (round 1)", {"CHEW": 127})]
    P = R["C"]["params"]
    costs = []
    for nm, ov in abl:
        idle, load = cost_of(cg, {**P, **ov}, "ab")
        costs.append((nm, idle, load))
        print(f"cost {nm:40s} idle {idle:.0f} load {load:.0f} worst {idle + load:.0f}", flush=True)
    # ---- probes on D and C (tightness, how hard, where the glitch is) -----------------------------------------------------------
    def prow(p):
        a = K.render(exe, "m_kick", params=p, tag="pr")[0]
        lm = K.level_metrics(a, "m_kick")
        r = D.hit_row(a, 4500)
        sp = Q.small_speaker(a, "m_kick")
        cs = []
        for t in KICK_PAT:
            t0 = Q.onset(a, t)
            cs.append(M.centroid(a, t0, t0 + 60, nfft=1024))
        t0 = Q.onset(a, 4500)
        return [f"{lm['rms']:.1f}", f"{N.crest_db(a, 'm_kick'):.1f}", f"{r['two']:.0f}", f"{r['hf100']:.1f}", f"{r['r_mud'][1]:.1f}", f"{r['tail60']:.0f}", f"{sp['100']:.1f}",
                f"{100 * np.std(cs) / np.mean(cs):.0f}", f"{M.rms_db(a, t0, t0 + 20):.0f} / {M.rms_db(a, t0 + 120, t0 + 140):.0f}"]
    hdr = ["level reading dBFS (VOLUME unchanged)", "crest dB", "two-level % (A1)", ">1.2k % (A1, 0-100 ms)", "MUD (A1, 20-100 ms)", "tail -60 dB (ms)", "kept after 100 Hz high-pass (dB)", "hit-to-hit centroid spread %", "A1 level at +0 / +120 ms (dBFS)"]
    pr = {}
    Pd = R["D"]["params"]
    for nm, vals in (("AD (tightness)", ("AD", [60, 66, 72, 76, 82, 90])), ("LFO_PITCH (the glitch, S&H)", ("LFO_PITCH", [0, 40, 80, 110, 127])), ("CUTOFF (open filter)", ("CUTOFF", [70, 85, 100, 105, 115])),
                     ("DRIVE (on C)", ("DRIVE", [0, 60, 127]))):
        k, vv = vals
        base_p = R["C"]["params"] if k == "DRIVE" else Pd
        pr[nm] = (hdr, [(str(v), prow({**base_p, k: v})) for v in vv])
    pr["click: the filter envelope (D, CUTOFF 85, ENV AMT / DECAY)"] = (hdr, [(f"ENV AMT {e} DECAY {d}", prow({**Pd, "CUTOFF": 85, "FENV_AMT": e, "FD": d})) for e, d in ((64, 40), (100, 30), (127, 25))])
    json.dump({"variants": {k: dict(r) for k, r in R.items()}, "costs": costs}, open(os.path.join(OUT, "results.json"), "w"), indent=1,
              default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o))
    json.dump(pr, open(os.path.join(OUT, "probe.json"), "w"), default=float)
    write_readme(R, costs, pr)
    print("written", OUT)


def write_readme(R, costs, pr):
    L = ["# 05 ZEAROX — ROUND 2 (generated by tests/voicing/batch03b_r2.py)\n",
         "*New direction (Vincent, after listening to round 1): a pixelated, gritty, hard black-and-white kick substitute; not muddy; square/pulse only, attack 0, no tape; not a heavy patch (target about 1500 host instr/sample worst case). Round 1's variants are rejected; the diagnosis is `diagnosis.md` here. "
         "Level: the bank reference (-18.0 dBFS RMS, +-1.5, peak <= -4) over the 11 hits x 150 ms of the kick phrase m. WAVs are on the listen/batch-03b-chapter1-wreck-and-chop branch only.*\n",
         "## The variants\n"]
    for k, r in R.items():
        L.append(f"**{k} {r['tag']}** — {r['desc']}\n")
        if k == "A":
            L.append("- (07 Tape Splice C's parameter list, unchanged; VOLUME trimmed to the bank reference on phrase m)\n")
        else:
            L.append("Changes against variant A (07 C), before -> after:\n")
            L.append("\n".join(f"- {c}" for c in r["changes_vs_A"]) + "\n")
    L += ["## The numbers\n", table(R), "\n### What each element costs (host instr/sample; C with one element changed)\n",
          "| change on C | idle | under load | worst case | vs C |", "|---|---|---|---|---|"]
    c0 = costs[0][1] + costs[0][2]
    for nm, idle, load in costs:
        L.append(f"| {nm} | {idle:.0f} | {load:.0f} | {idle + load:.0f} | {idle + load - c0:+.0f} |")
    for nm, (hdr, rows) in pr.items():
        L += [f"\n### Probe: {nm}\n", "| value | " + " | ".join(hdr) + " |", "|---|" + "---|" * len(hdr)]
        L += [f"| {v} | " + " | ".join(c) + " |" for v, c in rows]
    open(os.path.join(OUT, "README.md"), "w").write("\n".join(L) + "\n")
    open(os.path.join(OUT, "numbers.md"), "w").write("\n".join(L[L.index("## The numbers\n"):]) + "\n")


if __name__ == "__main__":
    main()
