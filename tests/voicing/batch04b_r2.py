#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""13 GHOST BOARD, ROUND 2 (Batch 4B): the ORIGINAL's voice (the 'Mellotron' Vincent heard) with round 1's variant D echo and spring, the tape deck OFF (CHEW 0).

  python3 tests/voicing/batch04b_r2.py [--quick] [--no-cost] [--no-wav]      -> listen/voicing/batch-04b/13-round2/ (WAVs only ever on the listen branch)
  python3 tests/voicing/batch04b_r2.py --emit KEY                             -> the C array of a variant (from results.json)

Variants (each differs from A2 by ONE thing; every other value is the original's, except LFO PITCH 0 and the echo / spring copied from round-1 D):
  A2  the base as is                B2  CUTOFF up (the dark filter opened a little)
  C2  LFO PWM 0 (no pulse-width movement)      D2  OSC 2 FINE 64 (no detune: no beating)
Render-only references at the same bank level: Aorig (the original patch's voice, its own spring, no echo, deck off) and D1 (round-1 variant D exactly)."""
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
import batch04b as P
import batch04b_metrics as Z
import batch04b_report as RP

OUT = os.path.join(K.ROOT, "listen", "voicing", "batch-04b", "13-round2")
SLOT = 13
R1 = os.path.join(K.ROOT, "listen", "voicing", "batch-04b", "13-ghost-board", "results.json")
SPEC = dict(slot=13, dir="13-round2", name="Ghost Board", kind="plain", level="t_ghost", phrases=["b_stabs", "t_ghost"])
ECHO_KEYS = ("DLY_TIME", "DLY_FB", "DLY_TONE", "DLY_MIX", "ALLEY", "ALLEY_FINE", "BBD_SPREAD", "REV_SIZE", "REV_DAMP", "REV_PRE", "REV_MIX")
SHORT = {"b_stabs": "stabs", "t_ghost": "ghost"}
CUT_UP = 84


def tables(orig, d1):
    base = {**orig, "LFO_PITCH": 0, "CHEW": 0, **{k: d1[k] for k in ECHO_KEYS}}
    V = [("A2", "as-is", "the original's voice (oscillators, filter, envelopes, LFO, VINTAGE, SPREAD) with round-1 D's echo and spring, deck off, LFO PITCH 0", {}),
         ("B2", "more-top", f"A2 with the filter opened: CUTOFF {orig['CUTOFF']} -> {CUT_UP}", {"CUTOFF": CUT_UP}),
         ("C2", "no-pwm", "A2 with LFO PWM 0 (no pulse-width movement)", {"LFO_PWM": 0}),
         ("D2", "no-beat", "A2 with OSC 2 FINE 64 (no detune: no beating)", {"O2_FINE": 64})]
    return base, V


def level_trim(exe, params):
    spec = {**SPEC, "phrases": ["t_ghost", "b_stabs"]}
    v, _ = B2.trim_volume(exe, spec, params)
    return v


def mod_probe(exe, p, note=57, on=3000, off=6000):
    """the band-energy modulation of ONE held voice (A3, sends and deck off): depth dB (95th - 5th pct of 23 ms band energy) and strongest rate Hz in 150-400 and 400-1.2k, + the broadband level's depth: what the beating pair and the PWM do"""
    q = {**p, **Q.FXOFF_ALL, "MODE": 0, "VINTAGE": 0, "LFO_AMP": 0, "LFO_FLT": 0, "LFO_PHASE": 1}
    a = N._run(exe, "modp", N._probe_script(q, [f"{on} midi 0x90 {note} 100", f"{off} midi 0x80 {note} 0"], off + 300))
    b = N.pwm_metrics(a, on, off, settle_ms=400)["bands"]
    return {k: {"depth": b[k][0], "rate": b[k][1]} for k in ("150-400", "400-1.2k", "level")}


def measure(exe, cg, params, tag, quick, orig=None, no_cost=False):
    w, m = A.level_block(exe, SPEC, params, tag, orig)
    m = P.measure_13(exe, params, tag, w, m)
    m["mod"] = mod_probe(exe, params)
    m["mod_chord"] = {k: {"depth": v[0], "rate": v[1]} for k, v in N.pwm_metrics(Q.fx_set(exe, "t_ghost", params, tag + "m")["dry"], 3000, 5400, settle_ms=400)["bands"].items() if k in ("150-400", "400-1.2k", "level")}
    m["cost"] = None
    if not quick and not no_cost:
        cb, cl = K.cost(cg, params=params, tag=tag)
        ir, fr = K.callgrind_ips(cg, "x_stress", params=params, tag=tag + "i", notes=False)
        m["cost"] = {"b": cb, "load": cl, "idle": ir / fr}
    return w, m


def rows(R):
    P_ = lambda m, k: m["params"][k]
    common = RP.common("t_ghost")
    extra = [
        ("harmonics 3 / 5 / 7 re the fundamental, OSC 1 through the filter at rest (dB; triangle -19.1 / -28.0 / -34.2)", lambda m: " / ".join(RP.f(x, 1) for x in m["tri"])),
        ("MOVEMENT, one held voice A3, sends and deck off: band-energy depth dB / strongest rate Hz in 150-400", lambda m: f"{m['mod']['150-400']['depth']:.1f} / {m['mod']['150-400']['rate']:.1f}"),
        ("same in 400-1.2k", lambda m: f"{m['mod']['400-1.2k']['depth']:.1f} / {m['mod']['400-1.2k']['rate']:.1f}"),
        ("same, the broadband level", lambda m: f"{m['mod']['level']['depth']:.1f} / {m['mod']['level']['rate']:.1f}"),
        ("same on the held chord (dry), 150-400 / 400-1.2k depth dB", lambda m: f"{m['mod_chord']['150-400']['depth']:.1f} / {m['mod_chord']['400-1.2k']['depth']:.1f}"),
        ("filter / CUTOFF (Hz at C4) / key tracking % / RESO", lambda m: f"{['LP12','HP12','BP12','NOTCH','LP24','SEM'][P_(m,'FTYPE')]} / {P_(m,'CUTOFF')} ({440 * 2 ** ((P_(m,'CUTOFF') + 8 - 69) / 12):.0f}) / {100 * P_(m,'KEYTRK') / 127:.0f} / {P_(m,'RESO')}"),
        ("LFO PWM / OSC 2 FINE (cents) / LFO PITCH / CHEW", lambda m: f"{P_(m,'LFO_PWM')} / {P_(m,'O2_FINE')} ({(P_(m,'O2_FINE') - 64) * 2 * 100 / 256:+.1f}) / {P_(m,'LFO_PITCH')} / {P_(m,'CHEW')}"),
        ("echo: ALLEY (ms) / FEEDBK / MIX; spring DRAIN / SIZE / DAMP", lambda m: f"{m['delay_ms']:.0f} / {P_(m,'DLY_FB')} / {P_(m,'DLY_MIX')}; {P_(m,'REV_MIX')} / {P_(m,'REV_SIZE')} / {P_(m,'REV_DAMP')}"),
        ("first repeat of an isolated 150 ms E4: peak re the note (dB) / at ms after the note-on", lambda m: f"{RP.f(m['first']['dly_re_note'])} / {m['first']['t_ms']:.0f}"),
        ("the echo's margin over the spring in that window (dB)", lambda m: RP.f(m["first"]["margin"])),
        ("the repeats 1..6 (dB re the first)", lambda m: " ".join(f"{v:+.1f}" for _, _, v in m["train"])),
        ("echo return after the held chord's note-off (dB re the chord) 0-100 / 100-250 / 250-500 / 500-1000 / 1000-2000 ms", lambda m: " / ".join(RP.f(r["dly"], 1) for r in m["ret"]["ch1"])),
        ("spring return, same windows (dB)", lambda m: " / ".join(RP.f(r["spr"], 1) for r in m["ret"]["ch1"])),
        ("the tail after the chord: MUD / centroid Hz / level dBFS in 0-250 / 250-750 / 750-1500 ms", lambda m: " ; ".join(f"{t['mud']:.0f} / {t['cent']:.0f} / {t['db']:.0f}" for t in m["tailsplit"])),
        ("tail after the held chord to -20 / -40 / -60 dB (ms, DC out)", lambda m: RP.tailstr(m["tail"])),
    ]
    return common + extra


def main():
    argv = sys.argv[1:]
    quick, no_cost, no_wav = "--quick" in argv, "--no-cost" in argv, "--no-wav" in argv
    base_tree = os.path.join(K.BUILD, "base")
    orig = B.resolve(base_tree, SLOT)
    r1 = json.load(open(R1))
    d1 = r1["D"]["params"]
    base, V = tables(orig, d1)
    exe = K.build_host()
    if "--emit" in argv:
        key = argv[argv.index("--emit") + 1]
        res = json.load(open(os.path.join(OUT, "results.json")))
        print(B.emit("GHOST_BOARD", {**base, **dict(next(v for v in V if v[0] == key)[3]), "VOLUME": res[key]["volume"]}))
        return
    cg = None if (quick or no_cost) else K.callgrind_exe()
    # PROOF: LFO PITCH 3 against 0 (the law is zero below 12): bit-identical renders on both phrases
    pr = {}
    for ph in ("t_ghost", "b_stabs"):
        a = K.render(exe, ph, params={**base, "VOLUME": 80, "LFO_PITCH": 3}, tag="pf3")[0]
        b = K.render(exe, ph, params={**base, "VOLUME": 80, "LFO_PITCH": 0}, tag="pf0")[0]
        pr[ph] = bool((a == b).all())
    print("LFO PITCH 3 vs 0 bit-identical:", pr)
    R, wavs = {}, {}
    entries = [(k, t, d, {**base, **ch}) for k, t, d, ch in V]
    # references, level-matched: the original patch's voice (own spring, no echo, deck off) and round-1 D exactly
    entries.append(("Aorig", "orig-ref", "the ORIGINAL patch (its own spring, no echo, no deck) re-trimmed to the bank level: render-only reference", {**orig}))
    entries.append(("D1", "round1-D", "round-1 variant D exactly (CHEW 70, CUTOFF 70 voice, its echo and spring): render-only reference", {**d1}))
    for key, tag, desc, params in entries:
        params = dict(params)
        if key != "D1":
            v = level_trim(exe, params)
            while P.own_peak(exe, SPEC, {**params, "VOLUME": v}) > -4.2 and v > 1:
                v -= 1
            params["VOLUME"] = v
        w, m = measure(exe, cg, params, "13r2" + key, quick, no_cost=no_cost)
        m["volume"], m["params"], m["tag"], m["desc"] = params["VOLUME"], params, tag, desc
        R[key], wavs[key] = m, w
        print(f"{key:6s} VOL {m['volume']:3d} lvl {m['level']:6.2f} (b) {m['b']:6.2f} pk {m['t_ghost']['peak']:5.2f} crest {m['t_ghost']['crest']:4.1f} cent {m['notes']['cent']:5.0f} mud {m['notes']['mud']:6.1f} tail {' '.join(f'{t['mud']:.0f}' for t in m['tailsplit'])} tri {' '.join(f'{x:.0f}' for x in m['tri'])} mod150 {m['mod']['150-400']['depth']:.1f}/{m['mod']['150-400']['rate']:.1f} mod400 {m['mod']['400-1.2k']['depth']:.1f}/{m['mod']['400-1.2k']['rate']:.1f} 1st {m['first']['dly_re_note']:+.1f} mar {m['first']['margin']:+.1f}", flush=True)
    if quick:
        return
    os.makedirs(OUT, exist_ok=True)
    R["_proof_lfo_pitch"] = pr
    json.dump(R, open(os.path.join(OUT, "results.json"), "w"), default=A.jdefault, indent=1)
    if not no_wav:
        for key in wavs:
            for ph in SPEC["phrases"]:
                K.write_wav(os.path.join(OUT, f"13-round2_{key}_{SHORT[ph]}.wav"), wavs[key][ph][int(K.T_CUT * K.FS):])
    L = ["# Batch 4B, 13 Ghost Board, ROUND 2: variants and numbers", "",
         "Round 2 (6 Nov 2026), **rendered, not yet heard**. The ORIGINAL's voice with round-1 variant D's echo and spring, the tape deck OFF (CHEW 0). Definitions: `dog5-docs/voicing/README.md` section 17. Level phrase `t_ghost`; reference -18.0 dBFS RMS +-1.5, peak <= -4. "
         f"LFO PITCH 3 against 0, bit-identical renders: {pr}. WAVs only on the listen branch.", "", "## Variants", ""]
    for key, tag, desc, _ in entries:
        L.append(f"* **{key} {tag}**{' (RECOMMENDED, committed)' if key == 'A2' else ''}: {desc}.")
    keys = [k for k, *_ in entries]
    L += ["", "## Numbers", ""] + RP.table({k: R[k] for k in keys}, rows(R), keys)
    L += ["", "## Parameter changes against the ORIGINAL (before -> after); the echo and spring values are round-1 D's", ""]
    for key, tag, desc, params in entries:
        if key in ("Aorig", "D1"):
            continue
        L += [f"### {key} {tag}", ""] + [f"* {c}" for c in RP.changes(orig, R[key]["params"])] + [""]
        if key != "A2":
            L += [f"{key} against A2:", ""] + [f"* {c}" for c in RP.changes(R["A2"]["params"], R[key]["params"]) if not c.startswith("VOLUME")] + [""]
    L += ["### the echo and spring copied from round-1 D (value = D = what A2 has; the original's value in brackets)", ""] + [f"* {k} {d1[k]} ({orig[k]})" for k in ECHO_KEYS]
    open(os.path.join(OUT, "README.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
