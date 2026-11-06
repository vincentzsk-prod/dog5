#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Voicing round for Batch 4A, Chapter II "the spring / organ / wash set": 10 Atlantic Swell, 12 Kelp Tangle, 16 Tidal Pull.

  python3 tests/voicing/batch04a.py [base_tree] [--only SLOT] [--quick] [--no-cost] [--no-wav]
        base_tree: the firmware exported from the commit before the batch (default build/voicing/base)
        --quick:   no WAVs, no callgrind, no files (prints one line per variant: for tuning a variant table)
        --emit SLOT KEY: the C array (overrides over the defaults) of a variant, ready for obv_patches.h
        --readme:  rewrite README.md / numbers.md from results.json (text edits, no renders)

Same method as batch03b.py: a variant is a FULL parameter list; A is rendered through the base firmware's own program path; B..D over INIT; VOLUME is trimmed
to the bank reference (-18.0 dBFS RMS over the note-on region of the patch's own phrase, effects included, tails excluded; +-1.5 dB; peak <= -4 dBFS), last.
Output: listen/voicing/batch-04a/<NN-name>/ (tables on the merged voicing branch; WAVs only ever on the never-merged listen branch)."""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import batch01a as B                           # resolve(), emit(), change()
import batch02a as B2                          # trim_volume(), level_of()
import batch02a_metrics as M
import batch03a_metrics as N
import batch04a_metrics as Q
from batch04a_variants import PATCHES

OUT = os.path.join(K.ROOT, "listen", "voicing", "batch-04a")
SHORT = {"b_stabs": "stabs", "q_organ": "organ", "r_tangle": "tangle", "s_wash": "wash"}
FX_ALL = {"DLY_MIX": 0, "REV_MIX": 0, "CHEW": 0, "GROWL": 0}

# the notes of each phrase (ms, nominal)
Q_CH1, Q_ISO, Q_FIG, Q_CH2 = (3000, 5400), (7400, 7520), [(10000, 10120), (10300, 10420), (10600, 10720), (10900, 11020)], (13000, 14600)
R_A2, R_CH, R_FIG = (3000, 6200), (8000, 11000), [(13200 + 400 * i, 13350 + 400 * i) for i in range(6)]
S_CH1, S_CH2, S_FIG, S_STAB = (3000, 5000), (7600, 9600), [(12200, 12600), (13100, 13500), (14000, 14400)], [(15000, 15100), (15600, 15700), (16200, 16300)]
RET_WINS = ((0, 100), (100, 250), (250, 500), (500, 1000), (1000, 2000))
ON_WINS = ((0, 20), (20, 100), (100, 250))


def f1(x, p=1):
    return "-" if x is None or (isinstance(x, float) and (x != x or x < -150)) else f"{x:.{p}f}"


def dc_of(a, t0, t1):
    return a[N._s(t0):N._s(t1)].mean(0)


def sh(b):
    return M.fmt_bands(b)


# ---- the shared measures ---------------------------------------------------------------------------------------------------------------
def pitch_probe(exe, p, note, on=3000, off=6000):
    """the audio check of the pitch LFO: one voice (POLY, VINTAGE 0, no effects) with only the oscillator(s) the LFO moves: the common-mode wander of its fundamental in cents
    (N.drift_track: centroid of f0 +-12 % in 100 ms frames): s.d., 5-95 % range, strongest rate (Hz)"""
    to = p["LFO_PITCH_TO"]
    q = {**p, **FX_ALL, "MODE": 0, "VINTAGE": 0, "LFO_PWM": 0, "LFO_AMP": 0, "LFO_FLT": 0, "LFO_PHASE": 1, "AA": 0, "AS": 127,
         "O1_WAVE": 0 if to == 1 else p["O1_WAVE"], "O2_WAVE": 0 if to == 0 else p["O2_WAVE"]}
    if to == 2:
        q["O2_WAVE"] = 0
    lines = N._probe_script(q, [f"{on} midi 0x90 {note} 100", f"{off} midi 0x80 {note} 0"], off + 300)
    a = N._run(exe, "pprobe", lines)
    f0 = 440 * 2 ** ((note - 69) / 12)
    d = N.drift_track(a, f0, on, off, settle_ms=300)
    return {"sd": d["sd"], "range": d["range"], "rate": d["rate"]}


def tri_probe(exe, p):
    """harmonics 3 / 5 / 7 of a held A2 re the fundamental through the patch's OSC 1 and filter at rest (no LFO, no envelopes): triangle -19.1 / -28.0 / -34.2, square -9.5 / -14.0 / -16.9"""
    q = {**p, "LFO_PWM": 0, "LFO_PITCH": 0, "LFO_AMP": 0, "LFO_FLT": 0, "O2_WAVE": 0, "MODE": 0}
    return B2.triangle_probe(exe, q)[1:]


def residue_before(dry, full, onsets, on_len=100, pre=30):
    """note definition on a staccato figure: the level of everything that is NOT the dry note (echo repeats, spring) in the `pre` ms before each onset, re the note's own level
    over its first `on_len` ms; per onset and the mean (dB; the lower, the clearer the note stands)"""
    fx = full - dry
    vals = []
    for on in onsets:
        r = M.rms_db(fx, on - pre, on - 2)
        n = M.rms_db(dry, on + 5, on + on_len)
        vals.append(r - n)
    return vals


def level_block(exe, spec, params, tag, orig):
    lp = spec["level"]
    w = {}
    for ph in spec["phrases"]:
        if orig:
            w[ph], _ = K.render(orig[0], ph, program=orig[1], tag="m_" + tag)
        else:
            w[ph], _ = K.render(exe, ph, params=params, tag="m_" + tag)
    m = {ph: K.level_metrics(w[ph], ph) for ph in spec["phrases"]}
    for ph in spec["phrases"]:
        m[ph]["crest"] = N.crest_db(w[ph], ph)
        m[ph]["tone"] = K.tone_metrics(w[ph], ph)
        m[ph]["bands"] = M.band_split_phrase(w[ph], ph)
    m["level"] = m[lp]["rms"]
    m["b"] = m["b_stabs"]["rms"]
    m["peak_all"] = max(m[ph]["peak"] for ph in spec["phrases"])
    m["clip"] = int(sum((np.abs(x) >= 32767).sum() for x in w.values()))
    return w, m


# ---- 10: the organ -------------------------------------------------------------------------------------------------------------------------
def measure_10(exe, p, tag, w, m):
    a = w["q_organ"]
    R = Q.fx_set(exe, "q_organ", p, tag)
    dry = R["dry"]
    notes_all = [Q_CH1, Q_ISO] + Q_FIG + [Q_CH2]
    m["notes"] = Q.note_windows(a, notes_all)
    m["notes_dry"] = Q.note_windows(dry, notes_all)
    m["chord_dry"] = Q.note_windows(dry, [(Q_CH1[0] + 400, Q_CH1[1])])
    m["corr"] = Q.chan_corr(dry, Q_CH1[0] + 500, Q_CH1[1])
    m["corr_full"] = Q.chan_corr(a, Q_CH1[0] + 500, Q_CH1[1])
    m["beat"] = Q.band_beat(dry, 220.0, Q_CH1[0] + 300, Q_CH1[1])
    m["am"] = Q.am_depth(dry, Q_CH1[0] + 400, Q_CH1[1])
    m["pitch_probe"] = pitch_probe(exe, p, 57)
    m["lfo"] = {"hz": Q.lfo_hz(p["LFO_RATE"]), "cents": Q.pitch_cents(p["LFO_PITCH"]), "amp_db": Q.amp_db(p["LFO_AMP"]) if p["LFO_AMP"] else 0.0}
    T = Q.alley_ms(p["ALLEY"])
    S, on, off = Q.solo_set(exe, p, [64], 120, tail_ms=4000, tag="s10")
    m["delay_ms"] = T
    m["first"] = Q.first_repeat(S, on, off, T)
    m["train"] = Q.repeats_train(S, on, off, T, n=6)
    m["solo_split"] = Q.window_split(S["dly"] - S["dry"], on + T - 20, on + T + 140)
    m["solo_note_split"] = Q.window_split(S["dry"], on + 5, on + 120)
    m["solo_onwin"] = {k: N.wet_windows(S[k], S["dry"], on) for k in ("dly", "spr")}
    m["solo_tail"] = {"full": M.tail_times(S["full"], off, 60, 3500, dc=dc_of(S["full"], off + 3300, off + 3600))}
    m["ret"] = {k: Q.return_windows(R, off, 400, RET_WINS) for k, off in (("ch1", Q_CH1[1]), ("ch2", Q_CH2[1]))}
    m["under"] = Q.under_note(R, Q_FIG)
    m["tail"] = M.tail_times(a, Q_CH1[1], 150, 2000, dc=dc_of(a, 7000, 7300))
    m["tail_dry"] = M.tail_times(dry, Q_CH1[1], 150, 2000, dc=dc_of(dry, 7000, 7300))
    return m


# ---- 12: the tangle --------------------------------------------------------------------------------------------------------------------------
def measure_12(exe, p, tag, w, m):
    a = w["r_tangle"]
    R = Q.fx_set(exe, "r_tangle", p, tag)
    dry = R["dry"]
    m["pwm_a2"] = N.pwm_metrics(dry, R_A2[0], R_A2[1], settle_ms=400)
    m["pwm_a2_full"] = N.pwm_metrics(a, R_A2[0], R_A2[1], settle_ms=400)
    m["pwm_chord"] = N.pwm_metrics(dry, R_CH[0], R_CH[1], settle_ms=400)
    m["pwm_riff"] = N.pwm_riff(dry, [(on, off) for on, off in R_FIG[:3]], settle_ms=40)
    m["a2"] = Q.note_windows(dry, [(R_A2[0] + 500, R_A2[1])])
    m["chord"] = Q.note_windows(dry, [(R_CH[0] + 500, R_CH[1])])
    m["notes"] = Q.note_windows(a, [R_A2, R_CH] + R_FIG)
    m["notes_dry"] = Q.note_windows(dry, [R_A2, R_CH] + R_FIG)
    m["lfo"] = {"hz": Q.lfo_hz(p["LFO_RATE"]), "pts": Q.pwm_points(p["LFO_PWM"]), "pw_pct": 100 * (p["O1_PW"] + 0.5) / 128,
                "amp_db": 0.0}
    c, hw = m["lfo"]["pw_pct"], m["lfo"]["pts"]
    m["lfo"]["pw_lo"], m["lfo"]["pw_hi"] = c - hw, c + hw
    m["onwin"] = {"a2": N.wet_windows(R["spr"], dry, R_A2[0]), "chord": N.wet_windows(R["spr"], dry, R_CH[0])}
    m["ret"] = {k: Q.return_windows(R, off, 400, ((0, 250), (250, 750), (750, 1500), (1500, 1800))) for k, off in (("a2", R_A2[1]), ("chord", R_CH[1]))}
    dc = dc_of(a, 12300, 12800)
    m["tailsplit"] = {k: Q.tail_after(a, off, wins=((0, 250), (250, 750), (750, 1500)), dc=dc) for k, off in (("a2", R_A2[1]), ("chord", R_CH[1]))}
    m["tail"] = {k: M.tail_times(a, off, 150, 1750 if k == "a2" else 2150, dc=dc_of(a, off + 1500, off + 1750) if k == "a2" else dc_of(a, 12900, 13150)) for k, off in (("a2", R_A2[1]), ("chord", R_CH[1]))}
    m["tail_dry"] = M.tail_times(dry, R_CH[1], 150, 2150, dc=dc_of(dry, 12300, 12600))
    last = R_FIG[-1][1]
    m["tail_fig"] = M.tail_times(a, last, 60, 2500, dc=dc_of(a, last + 2500, last + 2900))
    return m


# ---- 16: the wash ----------------------------------------------------------------------------------------------------------------------------
def measure_16(exe, p, tag, w, m):
    a = w["s_wash"]
    R = Q.fx_set(exe, "s_wash", p, tag)
    dry = R["dry"]
    notes_all = [S_CH1, S_CH2] + S_FIG + S_STAB
    m["notes"] = Q.note_windows(a, notes_all)
    m["notes_dry"] = Q.note_windows(dry, notes_all)
    m["chord_dry"] = Q.note_windows(dry, [(S_CH1[0] + 300, S_CH1[1])])
    m["corr"] = Q.chan_corr(dry, S_CH1[0] + 400, S_CH1[1])
    m["corr_full"] = Q.chan_corr(a, S_CH1[0] + 400, S_CH1[1])
    m["beat"] = Q.band_beat(dry, 220.0, S_CH1[0] + 300, S_CH1[1])
    m["pwm_chord"] = N.pwm_metrics(dry, S_CH1[0], S_CH1[1], settle_ms=400)
    m["pitch_probe"] = pitch_probe(exe, p, 57)
    m["lfo"] = {"hz": Q.lfo_hz(p["LFO_RATE"]), "cents": Q.pitch_cents(p["LFO_PITCH"]), "pts": Q.pwm_points(p["LFO_PWM"]), "amp_db": 0.0}
    T = Q.alley_ms(p["ALLEY"])
    S, on, off = Q.solo_set(exe, p, [64], 400, tail_ms=4000, tag="s16")
    m["delay_ms"] = T
    m["first"] = Q.first_repeat(S, on, off, T)
    m["train"] = Q.repeats_train(S, on, off, T, n=6)
    m["solo_split"] = Q.window_split(S["dly"] - S["dry"], on + T, on + T + 300)
    m["solo_onwin"] = {k: N.wet_windows(S[k], S["dry"], on) for k in ("dly", "spr")}
    m["ret"] = {k: Q.return_windows(R, off, 400, RET_WINS) for k, off in (("ch1", S_CH1[1]), ("ch2", S_CH2[1]))}
    m["under"] = Q.under_note(R, S_FIG)
    dc = dc_of(a, 11100, 11700)
    m["tailsplit"] = Q.tail_after(a, S_CH1[1], wins=((0, 250), (250, 750), (750, 1500)), dc=dc)
    m["tail"] = M.tail_times(a, S_CH1[1], 150, 2500, dc=dc)
    m["tail_dry"] = M.tail_times(dry, S_CH1[1], 150, 2500, dc=dc_of(dry, 11100, 11700))
    m["tri"] = tri_probe(exe, p)
    m["attack_chord"] = None
    return m


MEASURE = {10: measure_10, 12: measure_12, 16: measure_16}


def measure(exe, cg, spec, params, tag, quick, orig=None, no_cost=False):
    w, m = level_block(exe, spec, params, tag, orig)
    # the attack of the AMP ENVELOPE, as heard (LFO / GROWL / sends off: they move the plateau the probe measures against)
    m["attack"] = {"voice": Q.attack_long(exe, params)}
    m = MEASURE[spec["slot"]](exe, params, tag, w, m)
    m["cost"] = None
    if not quick and not no_cost:
        cb, cl = K.cost(cg, params=params, tag=tag)
        ir, fr = K.callgrind_ips(cg, "x_stress", params=params, tag=tag + "i", notes=False)
        m["cost"] = {"b": cb, "load": cl, "idle": ir / fr}
    return w, m


# ---- the run ---------------------------------------------------------------------------------------------------------------------------------
def full_params(orig, ch):
    return {**orig, **ch}


def summary_line(spec, key, m, vol):
    s = f"{spec['slot']:02d}{key} VOL {vol:3d}  lvl {m['level']:6.2f}  (b) {m['b']:6.2f}  peak {m['peak_all']:6.2f}  t90 {m['attack']['voice']['t90']:5.1f}ms"
    if spec["slot"] == 10:
        s += f"  1st-rep {m['first']['dly_re_note']:+5.1f} dB @ {m['first']['t_ms']:.0f} ms  corr {m['corr'][0]:+.2f}  cent {m['notes']['cent']:.0f}  mud {m['notes']['mud']:.1f}  am {m['am'][0]:.1f} dB"
    if spec["slot"] == 12:
        b = m["pwm_a2"]["bands"]
        s += f"  PWM A2 150-400 {b['150-400'][0]:.1f} 400-1.2k {b['400-1.2k'][0]:.1f} lvl {b['level'][0]:.1f} dB  cent {m['a2']['cent']:.0f}  1.2k+ {m['a2']['shares']['1.2k+']:.1f}%"
    if spec["slot"] == 16:
        s += f"  1st-rep {m['first']['dly_re_note']:+5.1f} dB @ {m['first']['t_ms']:.0f} ms (spr margin {m['first']['margin']:+.1f})  corr {m['corr'][0]:+.2f}  cent {m['notes']['cent']:.0f}  mud {m['notes']['mud']:.1f}"
    return s


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
            params = full_params(orig, ch)
            vol, _ = B2.trim_volume(exe, spec, params)
            while B2.peak_of(exe, spec, {**params, "VOLUME": vol}) > -4.2 and vol > 1:          # the peak limit (-4 dBFS) beats the 0.6 dB window: down to -19.3 dBFS
                a, _ = K.render(exe, spec["level"], params={**params, "VOLUME": vol - 1}, tag="trim")
                if B2.level_of(spec, {spec["level"]: a}) < -19.3:
                    break
                vol -= 1
            params["VOLUME"] = vol
            w, m = measure(exe, cg, spec, params, f"{spec['slot']}{key}", quick, no_cost=no_cost)
        m["volume"], m["params"], m["tag"], m["desc"] = vol, params, tag, desc
        R[key], wavs[key] = m, w
        print(summary_line(spec, key, m, vol), flush=True)
    if quick:
        json.dump(R, open(os.path.join(K.BUILD, f"quick_{spec['slot']}.json"), "w"), default=jdefault)
        return R
    d = os.path.join(OUT, spec["dir"])
    os.makedirs(d, exist_ok=True)
    if not no_wav:
        for key in R:
            for ph in spec["phrases"]:
                K.write_wav(os.path.join(d, f"{spec['dir']}_{key}_{SHORT[ph]}.wav"), wavs[key][ph][int(K.T_CUT * K.FS):])
    return R


def jdefault(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(type(o))


def main():
    argv = sys.argv[1:]
    quick, no_cost, no_wav = "--quick" in argv, "--no-cost" in argv, "--no-wav" in argv
    only = None
    if "--only" in argv:
        only = int(argv[argv.index("--only") + 1])
    if "--emit" in argv:
        i = argv.index("--emit")
        slot, key = int(argv[i + 1]), argv[i + 2]
        spec = next(s for s in PATCHES if s["slot"] == slot)
        base = os.path.join(K.BUILD, "base")
        orig = B.resolve(base, slot)
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
            json.dump(R, open(os.path.join(d, "results.json"), "w"), default=jdefault, indent=1)
            from batch04a_report import write_all
            write_all(spec, R, d, B.resolve(base, spec["slot"]))


if __name__ == "__main__":
    main()
