#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Voicing round for Batch 2A, "weight and space": 17 Titanic, 21 Cowl Shadow, 09 Skeenhead, 11 Slapback Strut.

  python3 tests/voicing/batch02a.py [base_tree] [--only SLOT] [--quick] [--out DIR]
        base_tree: the firmware exported from the commit before the batch (default build/voicing/base)
        --quick:   no WAVs, no callgrind, no files (for tuning a variant table; prints one line per variant)
        --emit SLOT KEY: the C array of a variant (from results.json)

Same method as batch01a.py (a variant is a FULL parameter list over INIT; the ORIGINAL "A" is rendered through the base
firmware's own program path; VOLUME is trimmed to the bank reference on the patch's LEVEL measure), with the Batch 2A
measures of batch02a_metrics.py: the bloom of the slow patches, the register tilt, the spring and the echo as the effects'
own contribution (wet minus the same render with the effects off).  Output: listen/voicing/batch-02a/<NN-name>/."""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import batch01a as B                           # change(), emit(), resolve(), unit(): the echo rule and the C array
import batch02a_metrics as M
from batch02a_variants import PATCHES

OUT = os.path.join(K.ROOT, "listen", "voicing", "batch-02a")
BANK_REF = -18.0
FXOFF = {"DLY_MIX": 0, "REV_MIX": 0, "CHEW": 0, "GROWL": 0}
ID_PH = ("a_riff", "b_stabs", "c_held")


# ---- the level of a patch: each on its own phrase -----------------------------------------------------------------------
def level_of(spec, wavs):
    """the patch's loudness-reference reading from its renders: ('slow') RMS over t = +6 .. +10 s of the held note (the bloomed state),
    else RMS over the level phrase's note-on region (K.level_metrics)"""
    if spec["kind"] == "slow":
        return M.steady_level(wavs[spec["level"]], 3000)
    return K.level_metrics(wavs[spec["level"]], spec["level"])["rms"]


PEAK_LIMIT = -4.3                              # the hard limit is -4 dBFS; a patch is trimmed down (never below -18.6) to keep this margin


def peak_of(exe, spec, params):
    return max(K.level_metrics(K.render(exe, ph, params=params, tag="pk")[0], ph)["peak"] for ph in spec["phrases"])


def trim_volume(exe, spec, params):
    """the VOLUME byte (square law, ~0.17 dB a step) whose reading is closest to the bank reference; then, if a phrase peaks above
    PEAK_LIMIT, the byte comes down until it does (the reading may fall to -18.6 for that)"""
    v, r = _trim(exe, spec, params)
    while peak_of(exe, spec, {**params, "VOLUME": v}) > PEAK_LIMIT and v > 1:
        a, _ = K.render(exe, spec["level"], params={**params, "VOLUME": v - 1}, tag="trim")
        if level_of(spec, {spec["level"]: a}) < BANK_REF - 0.6:
            break
        v -= 1
    return v, r


def _trim(exe, spec, params):
    v = params.get("VOLUME", 100)
    best = None
    for _ in range(9):
        a, _ = K.render(exe, spec["level"], params={**params, "VOLUME": v}, tag="trim")
        r = level_of(spec, {spec["level"]: a})
        if best is None or abs(r - BANK_REF) < abs(best[1] - BANK_REF):
            best = (v, r)
        if abs(r - BANK_REF) < 0.12:
            break
        nv = int(round(v * 10 ** ((BANK_REF - r) / 40)))
        v = max(1, min(127, nv if nv != v else v + (1 if BANK_REF > r else -1)))
    return best


def change(k, old, new, params):
    """batch01a's echo-rule line, with DETUNE read in the patch's own mode (DUAL: the pair is that many cents APART; UNISON: the stack spans +-that)"""
    if k == "UNI_DET" and params["MODE"] == 1:
        pc = lambda v: (v * v // 64) * 100 / 256
        return f"UNI_DET {old} -> {new} ({100 * (new - old) / 127:+.0f}%) (the DUAL pair {pc(old):.1f} -> {pc(new):.1f} cents apart)"
    return B.change(k, old, new)


# ---- measuring ----------------------------------------------------------------------------------------------------------
def render_set(exe, spec, params, tag, orig=None, extra_for=None):
    """all phrases of the patch -> {phrase: wav}; orig=(base exe, program) renders through the base firmware's own program path"""
    wavs, out = {}, {}
    for ph in spec["phrases"] + ["x_register"]:
        ex = ()
        if extra_for and ph == extra_for[0]:
            ex = extra_for[1]
        if orig:
            a, o = K.render(orig[0], ph, program=orig[1], extra=ex, tag="m_" + tag)
        else:
            a, o = K.render(exe, ph, params=params, extra=ex, tag="m_" + tag)
        wavs[ph], out[ph] = a, o
    return wavs, out


def render_dry(exe, spec, params, ph, tag, orig=None):
    """the same phrase with the Psych Chain stages that make a tail switched off: the voice alone"""
    a, _ = K.render(exe, ph, params={**params, **FXOFF}, tag="d_" + tag)
    return a


def measure(exe, cg, spec, params, tag, quick, orig=None):
    kind = spec["kind"]
    lp = spec["level"]
    extra_for = None
    if kind == "slow":
        extra_for = (lp, [f"3000 vlog 1", f"13100 vlog 0"])
    wavs, outs = render_set(exe, spec, params, tag, orig, extra_for)
    m = {}
    for ph in spec["phrases"]:
        m[ph] = K.level_metrics(wavs[ph], ph)
        m[ph].update(K.tone_metrics(wavs[ph], ph))
        m[ph]["bands"] = M.band_split_phrase(wavs[ph], ph)
    m["peak_all"] = max(m[ph]["peak"] for ph in spec["phrases"])
    m["clip"] = int(sum((np.abs(w) >= 32767).sum() for w in wavs.values()))
    m["step_db"] = {ph: float(20 * np.log10(np.abs(np.diff(wavs[ph], axis=0)).max() / 32767)) for ph in spec["phrases"]}
    m["level"] = level_of(spec, wavs)
    m["reg"] = M.register_tilt(wavs["x_register"])
    # a dry reference of the level phrase (the voice alone), used by the tail / echo / spring readings
    dry = render_dry(exe, spec, params, lp, tag)
    fxw = wavs[lp] if not orig else K.render(exe, lp, params=params, tag="fxw")[0]     # (A: wet and dry both over INIT, so wet - dry is exact)
    m["peak_dry_lp"] = M.peak_db(dry)
    if kind == "slow":
        on, off, f0 = 3000, 13000, spec["f0"]
        rows = M.bloom(wavs[lp], on, 10000)
        m["bloom"] = rows
        m["bloom_t"] = M.bloom_times(rows, f0)
        m["lvl_first1s"] = M.rms_db(wavs[lp], on + 250, on + 1250)
        m["lvl_whole"] = M.rms_db(wavs[lp], on, off)
        m["bands_steady"] = M.band_shares(wavs[lp], on + 6000, on + 10000)
        m["bands_first"] = M.band_shares(wavs[lp], on + 250, on + 1250)
        m["beat"] = K.beat_metrics(wavs[lp], f0, on + 3000, off - 100, win_s=2.0)
        m["vlog"] = {str(c): v for c, v in K.vlog_parse(outs[lp]).items()}
        m["dips"] = M.dips(wavs[lp], on + 500, on + 10000)
        m["floor"] = M.rms_db(wavs[lp], 16500, 18400)             # 3.5 .. 5.4 s after the key-up: the hiss CHEW leaves, else silence
        m["rel"] = M.tail_times(wavs[lp], off, 150, 5400)
        m["rel_dry"] = M.tail_times(dry, off, 150, 5400)
        # early release: (c) A2 held 2.4 s let go; how bright did it get, how does it die
        m["early"] = {"cent_end": M.centroid(wavs["c_held"], 5000, 5380), "lvl_end": M.rms_db(wavs["c_held"], 5000, 5380),
                      "tail": M.tail_times(wavs["c_held"], 5400, 150, 4000)}
    if kind in ("spring", "echo"):
        t_on = 3250 if kind == "spring" else 3500          # the first stab (A minor dyad) / the first A2 of the riff
        m["snap"] = M.attack_snap(dry, t_on)
        m["drop"] = M.body_drop(dry, t_on, 110 if kind == "spring" else 100)
    if kind == "spring":
        on_m = K.gate_mask(lp, len(dry))
        fx = M.fx_part(fxw, dry)
        m["dry_rms"] = float(10 * np.log10((dry[on_m] ** 2).mean() / 32767 ** 2))
        m["wet_rms"] = m[lp]["rms"]
        m["fx_re_dry_db"] = M.energy_db(fx[on_m]) - M.energy_db(dry[on_m])        # the spring's return inside the stabs, re the dry stab
        # the gap between the stabs (5.9 .. 7.2 s: the only empty stretch in the phrase) and the last tail
        m["gap_re_stab_db"] = M.rms_db(wavs[lp], 5900, 7200) - M.energy_db(wavs[lp][on_m])
        m["fx_total_re_dry_db"] = M.energy_db(fx[int(3.2 * K.FS):int(11.9 * K.FS)]) - M.energy_db(dry[int(3.2 * K.FS):int(11.9 * K.FS)])
        m["fx_cent"] = M.centroid(fx, 3200, 11900)
        m["dry_cent"] = M.centroid(dry, 3200, 8500)
        m["fx_bands"] = M.band_shares(fx, 3200, 11900)
        m["rel"] = M.tail_times(wavs[lp], 8360, 100, 3600)
        m["rel_dry"] = M.tail_times(dry, 8360, 100, 600)
        # the first 1.5 s after the last stab is the tail the player hears; its level re the stab
        m["tail_1s_re_stab_db"] = M.rms_db(wavs[lp], 8420, 9420) - M.energy_db(wavs[lp][on_m])
        m["silence_before_return"] = M.rms_db(fx, 3250, 3252)
    elif kind == "echo":
        on_m = K.gate_mask(lp, len(dry))
        fx = M.fx_part(fxw, dry)
        m["dry_rms"] = float(10 * np.log10((dry[on_m] ** 2).mean() / 32767 ** 2))
        m["echo"] = M.echo_return(fxw, dry, 8350, 8450)
        m["fx_re_dry_db"] = M.energy_db(fx[int(3.2 * K.FS):int(11.9 * K.FS)]) - M.energy_db(dry[int(3.2 * K.FS):int(11.9 * K.FS)])
        m["fx_bands"] = M.band_shares(fx, 3200, 11900)
        m["rel"] = M.tail_times(wavs[lp], 8450, 100, 3000)
        m["rel_dry"] = M.tail_times(dry, 8450, 100, 600)
        m["silence_before_return"] = M.rms_db(fx, 8350, 8352)
        m["tri"] = triangle_probe(exe, params)
    m["cost"] = None
    if not quick:
        cb, cl = K.cost(cg, params=params, tag=tag)
        ir, fr = K.callgrind_ips(cg, "x_stress", params=params, tag=tag + "i", notes=False)
        m["cost"] = {"b": cb, "load": cl, "idle": ir / fr}
    return wavs, m, dry


def triangle_probe(exe, params):
    """how close is the oscillator + filter to a triangle at rest?  The patch's own OSC 1 / filter with the envelopes pinned (sustained note, filter
    envelope amount centred, AMP sustain full): the amplitudes of harmonics 1, 3, 5, 7 of a held A2 against an ideal triangle (0 / -19.1 / -28.0 /
    -34.2 dB) and a square (0 / -9.5 / -14.0 / -16.9 dB)"""
    p = {**params, **FXOFF, "FENV_AMT": 64, "AA": 0, "AS": 127, "AD": 70, "LFO_FLT": 0, "ENV_O2": 64, "VINTAGE": 0, "DLY_MIX": 0, "GLIDE": 0}
    sp = "3000 midi 0x90 45 100\n5000 midi 0x80 45 0\n5600 end\n"
    path = os.path.join(K.BUILD, "tri.txt")
    lines = [f"{K.T_SELECT} midi 0xC0 {K.INIT_PROGRAM} 0"] + [f"{K.T_PARAMS} param {K.PARAM_IDS[k]} {v}" for k, v in p.items()]
    open(path, "w").write("\n".join(lines) + "\n" + sp)
    import subprocess
    subprocess.run([exe, os.path.join(K.BUILD, "tri"), path], cwd=K.ROOT, check=True, capture_output=True)
    a = K.read_wav(os.path.join(K.BUILD, "tri.wav")).mean(1)[int(3.6 * K.FS):int(4.9 * K.FS)]
    N = 1 << 17
    X = np.abs(np.fft.rfft(a[:N] * np.hanning(min(len(a), N)), N))
    f = np.fft.rfftfreq(N, 1 / K.FS)
    amp = []
    for n in (1, 3, 5, 7):
        w = (f > n * 110 * 0.97) & (f < n * 110 * 1.03)
        amp.append(float(X[w].max()))
    return [20 * np.log10(v / amp[0]) for v in amp]


def drain_probe(exe, spec, params, drains=(0, 30, 60, 100)):
    """what DRAIN does on this patch (the tank is fed through a ONE-POLE 150 Hz high-pass: -9 dB at 55 Hz, not a wall): for each DRAIN setting the
    spring's own return (wet - dry) over the whole level phrase: its energy re the dry signal (dB), its energy re the dry in each band (the upper
    partials are what a small speaker plays), the share of the return below 150 Hz, its centroid.  The dry is the same voice with DRAIN 0"""
    lp = spec["level"]
    base = {**params, "REV_MIX": 0}
    dry, _ = K.render(exe, lp, params=base, tag="pdry")
    lo, hi = (3200, 14500) if lp != "h_surf" else (3200, 10900)
    rows = []
    for d in drains:
        if not d:
            continue
        w, _ = K.render(exe, lp, params={**params, "REV_MIX": d}, tag="pw")
        fx = w - dry
        e = M.energy_db(fx[int(lo * K.FS / 1000):int(hi * K.FS / 1000)]) - M.energy_db(dry[int(lo * K.FS / 1000):int(hi * K.FS / 1000)])
        b = M.band_shares(fx, lo, hi)
        rows.append({"drain": d, "fx_re_dry_db": e, "low150": b["<60"] + b["60-150"], "cent": M.centroid(fx, lo, hi),
                     "band_db": M.band_diff_db(fx, dry, lo, hi)})
    return rows


# ---- writing --------------------------------------------------------------------------------------------------------------
def f1(x, p=1):
    return "-" if x is None or x < -150 else f"{x:.{p}f}"


def tables(spec, R):
    ks = list(R)
    kind = spec["kind"]
    lp = spec["level"]
    L = ["| | " + " | ".join(f"**{k}** {R[k]['tag']}" for k in ks) + " |", "|---|" + "---|" * len(ks)]
    row = lambda name, f: L.append("| " + name + " | " + " | ".join(f(R[k]) for k in ks) + " |")
    row("VOLUME (trim)", lambda r: str(r["volume"]))
    row(f"LEVEL READING ({spec['level_def']}), dBFS", lambda r: f1(r["level"]))
    row("vs the bank reference −18.0", lambda r: f"{r['level'] + 18.0:+.1f}")
    row("RMS on phrase (b), the bank's own reading", lambda r: f1(r["b_stabs"]["rms"]))
    row("difference (b) − level reading, dB", lambda r: f"{r['b_stabs']['rms'] - r['level']:+.1f}")
    row("K-weighted RMS, phrase (b)", lambda r: f1(r["b_stabs"]["rms_k"]))
    row("peak of any phrase, dBFS (limit ≤ −4)", lambda r: f1(r["peak_all"]))
    row("RMS note-on region per phrase (" + " / ".join(p[0] for p in spec["phrases"]) + ")",
        lambda r: " / ".join(f1(r[p]["rms"]) for p in spec["phrases"]))
    row("centroid Hz (level phrase / b)", lambda r: f"{r[lp]['centroid']:.0f} / {r['b_stabs']['centroid']:.0f}")
    row("band split % <60 / 60-150 / 150-400 / 400-1.2k / 1.2k+ (level phrase)", lambda r: M.fmt_bands(r[lp]["bands"]))
    row("band split % (b)", lambda r: M.fmt_bands(r["b_stabs"]["bands"]))
    row("register tilt, A1 / A2 / A3 (x_register): level dBFS", lambda r: " / ".join(f1(x["level"]) for x in r["reg"]))
    row("  centroid in harmonics of the note (centroid / f0)", lambda r: " / ".join(f1(x["harm"]) for x in r["reg"]))
    if kind == "slow":
        row("bloom: first second (+0.25..1.25 s) level · centroid", lambda r: f"{r['lvl_first1s']:.1f} dB · {r['bloom'][0][2]:.0f} Hz")
        row("bloom: steady part (+6..10 s) level · centroid", lambda r: f"{r['level']:.1f} dB · {r['bloom_t']['cent_plateau']:.0f} Hz")
        if spec.get("bloom", True):
            row("bloom: octaves risen (centroid, first window → plateau)", lambda r: f1(r["bloom_t"]["octaves"]))
            row("bloom: brightness reaches 10 % / 90 % of the climb at (s)", lambda r: f"{f1(r['bloom_t']['cent_t10'])} / {f1(r['bloom_t']['cent_t90'])}")
            row("bloom: level reaches 90 % of its climb at (s)", lambda r: f1(r["bloom_t"]["lvl_t90"]))
        row("plateau centroid in harmonics of the note", lambda r: f1(r["bloom_t"]["plateau_harm"]))
        row("whole hold: deepest dip below the median (dB) · dips of ≥ 6 dB (dropouts)", lambda r: f"{r['dips'][0]:.1f} · {r['dips'][1]}")
        row("noise floor 3.5-5.4 s after the key-up (dBFS)", lambda r: f1(r["floor"]))
        row("band split % at the start (+0.25..1.25 s)", lambda r: M.fmt_bands(r["bands_first"]))
        row("band split % steady (+6..10 s)", lambda r: M.fmt_bands(r["bands_steady"]))
        row("whole-hold RMS (the dark start included), dBFS", lambda r: f1(r["lvl_whole"]))
        row("beat of the stack, held note (Hz mean [min–max] · depth dB)",
            lambda r: f"{r['beat']['rate_mean']:.2f} [{r['beat']['rate_min']:.2f}–{r['beat']['rate_max']:.2f}] · {r['beat']['depth_db']:.0f}")
        row("card static offsets (cents)", lambda r: " / ".join(f"{v[0]:+.1f}" for v in r["vlog"].values()) or "-")
        row("wander s.d. (cents per card)", lambda r: " / ".join(f"{v[1]:.1f}" for v in r["vlog"].values()) or "-")
        row("wander range (cents per card)", lambda r: " / ".join(f"{v[2]:+.0f}..{v[3]:+.0f}" for v in r["vlog"].values()) or "-")
        row("release after the 10 s hold: −20 / −40 / −60 dB (ms), with FX", lambda r: f"{f1(r['rel']['t20'], 0)} / {f1(r['rel']['t40'], 0)} / {f1(r['rel']['t60'], 0)}")
        row("release, voice alone (FX 0)", lambda r: f"{f1(r['rel_dry']['t20'], 0)} / {f1(r['rel_dry']['t40'], 0)} / {f1(r['rel_dry']['t60'], 0)}")
        row("EARLY RELEASE (A2 held 2.4 s): centroid Hz at the key-up · level dB", lambda r: f"{r['early']['cent_end']:.0f} · {r['early']['lvl_end']:.1f}")
        row("  its tail −20 / −40 / −60 dB (ms)", lambda r: f"{f1(r['early']['tail']['t20'], 0)} / {f1(r['early']['tail']['t40'], 0)} / {f1(r['early']['tail']['t60'], 0)}")
    if kind == "spring":
        row("dry stabs (spring off) RMS, note-on region dBFS", lambda r: f1(r["dry_rms"]))
        row("with the spring RMS, note-on region dBFS (this is the level reading)", lambda r: f1(r["wet_rms"]))
        row("spring's return inside the stabs, re the dry stab (dB)", lambda r: f1(r["fx_re_dry_db"]))
        row("spring's return over the whole phrase incl. tails, re the dry stabs (dB)", lambda r: f1(r["fx_total_re_dry_db"]))
        row("the 1.3 s gap between stabs: level re the stab (dB)", lambda r: f1(r["gap_re_stab_db"]))
        row("1 s after the last stab: level re the stab (dB)", lambda r: f1(r["tail_1s_re_stab_db"]))
        row("tail after the last stab, −20 / −40 / −60 dB (ms), with the spring", lambda r: f"{f1(r['rel']['t20'], 0)} / {f1(r['rel']['t40'], 0)} / {f1(r['rel']['t60'], 0)}")
        row("  voice alone", lambda r: f"{f1(r['rel_dry']['t20'], 0)} / {f1(r['rel_dry']['t40'], 0)} / {f1(r['rel_dry']['t60'], 0)}")
        row("spring's own spectrum: centroid Hz (dry stab centroid)", lambda r: f"{r['fx_cent']:.0f} ({r['dry_cent']:.0f})")
        row("spring's own band split % <60 / 60-150 / 150-400 / 400-1.2k / 1.2k+", lambda r: M.fmt_bands(r["fx_bands"]))
        row("pluck decay inside the gate (voice alone): level drop 10 ms → gate end (dB) · time to fall 10 dB (ms)", lambda r: f"{r['drop'][0]:.1f} · {f1(r['drop'][1], 0)}")
        row("pluck: centroid of the first 23 ms → next 67 ms of a stab (Hz, ratio), voice alone", lambda r: f"{r['snap'][0]:.0f} → {r['snap'][1]:.0f} (×{r['snap'][2]:.1f})")
        row("check: the send in the first 2 ms of the first note (dBFS; - = silent, the dry path is not touched)", lambda r: f1(r["silence_before_return"]))
    if kind == "echo":
        row("dry notes (echo and spring off) RMS, note-on region dBFS", lambda r: f1(r["dry_rms"]))
        row("echo (last note): first repeat re the dry note's peak (dB) · at (ms after note-on)",
            lambda r: f"{r['echo']['echo_re_note_db']:+.1f} · {r['echo']['echo_t_ms']:.0f}")
        row("  second repeat re the first (dB)", lambda r: f1(r["echo"]["repeat2_re_first_db"]))
        row("FX return over the whole phrase, re the dry notes (dB)", lambda r: f1(r["fx_re_dry_db"]))
        row("FX return band split % <60 / 60-150 / 150-400 / 400-1.2k / 1.2k+", lambda r: M.fmt_bands(r["fx_bands"]))
        row("tail after the last note, −20 / −40 / −60 dB (ms), with FX", lambda r: f"{f1(r['rel']['t20'], 0)} / {f1(r['rel']['t40'], 0)} / {f1(r['rel']['t60'], 0)}")
        row("  voice alone", lambda r: f"{f1(r['rel_dry']['t20'], 0)} / {f1(r['rel_dry']['t40'], 0)} / {f1(r['rel_dry']['t60'], 0)}")
        row("oscillator through the filter at rest: harmonics 3 / 5 / 7 re 1 (dB)  [triangle −19.1 / −28.0 / −34.2; square −9.5 / −14.0 / −16.9]",
            lambda r: " / ".join(f"{x:.1f}" for x in r["tri"][1:]))
        row("pluck decay inside the gate (voice alone): level drop 10 ms → gate end (dB) · time to fall 10 dB (ms)", lambda r: f"{r['drop'][0]:.1f} · {f1(r['drop'][1], 0)}")
        row("pluck: centroid of the first 23 ms → next 67 ms of A2 (Hz, ratio), voice alone", lambda r: f"{r['snap'][0]:.0f} → {r['snap'][1]:.0f} (×{r['snap'][2]:.1f})")
        row("check: the send in the first 2 ms of the last note (dBFS; - = silent, the dry path is not touched)", lambda r: f1(r["silence_before_return"]))
    row("largest sample step dBFS (per phrase)", lambda r: " / ".join(f"{r['step_db'][p]:.0f}" for p in spec["phrases"]))
    row("clipped samples", lambda r: str(r["clip"]))
    if R[ks[0]]["cost"]:
        row("cost: host instr/sample, phrase (b)", lambda r: f"{r['cost']['b']:.0f}")
        row("cost idle (always-on stages)", lambda r: f"{r['cost']['idle']:.0f}")
        row(f"cost under load ({spec['load']}), on top of idle", lambda r: f"{r['cost']['load']:.0f}")
        row("cost worst case = idle + load", lambda r: f"{r['cost']['idle'] + r['cost']['load']:.0f}")
    return "\n".join(L)


def bloom_table(R):
    ks = list(R)
    L = ["| t (s) | " + " | ".join(f"{k}: dB · Hz · %>1.2k" for k in ks) + " |", "|---|" + "---|" * len(ks)]
    for i in range(len(R[ks[0]]["bloom"])):
        L.append(f"| {R[ks[0]]['bloom'][i][0]:.0f} | " + " | ".join(f"{R[k]['bloom'][i][1]:.1f} · {R[k]['bloom'][i][2]:.0f} · {R[k]['bloom'][i][3]:.0f}" for k in ks) + " |")
    return "\n".join(L)


def probe_table(rows):
    L = ["| DRAIN | return re the dry signal, all bands (dB) | …in <60 / 60-150 / 150-400 / 400-1.2k / 1.2k+ Hz (dB, each band re the dry's own) | share of the return < 150 Hz (%) | its centroid (Hz) |", "|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['drain']} | {f1(r['fx_re_dry_db'])} | " + " / ".join(f"{v:.0f}" for v in r['band_db'].values()) + f" | {f1(r['low150'], 0)} | {f1(r['cent'], 0)} |")
    return "\n".join(L)


def readme(spec, R, probe):
    L = [f"# {spec['slot']:02d} {spec['name']} — voicing round (Batch 2A, weight and space)\n",
         f"*Generated by tests/voicing/batch02a.py. Level reading: {spec['level_def']}; matched to the bank reference (−18.0 dBFS RMS) by VOLUME; "
         f"phrase (b)'s reading is in the table too. Every change is before → after under the echo rule. WAVs are on the listen/batch-02a-weight-and-space branch only.*\n",
         f"**Recommended: {spec['recommend']}** — " + spec["why"](R) + "\n", "## What to listen to\n", spec["listen"] + "\n", "## The variants\n"]
    for k, r in R.items():
        L.append(f"**{k} {r['tag']}** — {r['desc']}\n")
        L.append("\n".join(f"- {c}" for c in r["changes"]) or "- (none: the original)")
        L.append("")
    L += ["## The numbers\n", tables(spec, R)]
    if spec["kind"] == "slow":
        L += ["\n### The hold second by second: level · centroid · share above 1.2 kHz\n", bloom_table(R)]
    if probe:
        L += [f"\n### What DRAIN does on this patch (variant {spec['recommend'][0]}, probe renders, not variants)\n", probe_table(probe)]
    L += ["\n" + spec["notes"]]
    return "\n".join(L) + "\n"


def main():
    if "--emit" in sys.argv:
        slot, key = int(sys.argv[sys.argv.index("--emit") + 1]), sys.argv[sys.argv.index("--emit") + 2]
        spec = [p for p in PATCHES if p["slot"] == slot][0]
        res = json.load(open(os.path.join(OUT, spec["dir"], "results.json")))
        print(B.emit(spec["cname"], res["variants"][key]["params"]))
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
        ORIGINAL = B.resolve(base, slot)
        d = os.path.join(OUT, spec["dir"])
        R = {}
        for key, tag, desc, ch in spec["variants"]:
            params = {**ORIGINAL, **ch}
            if key == "A":
                vol = params["VOLUME"]
            else:
                vol, _ = trim_volume(exe, spec, params)
            params["VOLUME"] = vol
            wavs, m, dry = measure(exe, cg, spec, params, spec["dir"][:2] + key, quick, orig=(old, slot - 1) if key == "A" else None)
            m.update(tag=tag, desc=desc, volume=vol, params=params,
                     changes=[change(k, ORIGINAL[k], v, params) for k, v in params.items() if v != ORIGINAL[k]])
            R[key] = m
            if not quick:
                os.makedirs(d, exist_ok=True)
                for ph in spec["phrases"]:
                    K.write_wav(os.path.join(d, f"{key}_{tag}_{spec['short'][ph]}.wav"), wavs[ph][int(K.T_CUT * K.FS):])
            line = (f"[{slot:02d}] {key} {tag:10s} VOL {vol:3d} level {m['level']:6.1f}  b {m['b_stabs']['rms']:6.1f}  pk {m['peak_all']:5.1f}  "
                    f"cent {m[spec['level']]['centroid']:5.0f} bands {M.fmt_bands(m[spec['level']]['bands'])}")
            if spec["kind"] == "slow":
                bt = m["bloom_t"]
                line += f"  bloom {bt['cent0']:.0f}->{bt['cent_plateau']:.0f}Hz ({bt['octaves']:.1f} oct) t10/t90 {f1(bt['cent_t10'])}/{f1(bt['cent_t90'])}s first {m['lvl_first1s']:.1f}dB  reg harm " + "/".join(f"{x['harm']:.1f}" for x in m["reg"]) + " lvl " + "/".join(f"{x['level']:.1f}" for x in m["reg"])
            if spec["kind"] == "spring":
                line += f"  snap {m['snap'][0]:.0f}->{m['snap'][1]:.0f} drop {m['drop'][0]:.1f}dB t10 {f1(m['drop'][1],0)}ms"
            if spec["kind"] == "spring":
                line += f"  spring {m['fx_re_dry_db']:+.1f}dB in stabs, gap {m['gap_re_stab_db']:.1f}, tail60 {f1(m['rel']['t60'], 0)}ms (dry {f1(m['rel_dry']['t60'], 0)}), fxcent {m['fx_cent']:.0f}"
            if spec["kind"] == "echo":
                e = m["echo"]
                line += f"  snap {m['snap'][0]:.0f}->{m['snap'][1]:.0f} drop {m['drop'][0]:.1f}dB t10 {f1(m['drop'][1],0)}ms"
                line += f"  echo {e['echo_re_note_db']:+.1f}dB @ {e['echo_t_ms']:.0f}ms rep2 {f1(e['repeat2_re_first_db'])} tail60 {f1(m['rel']['t60'], 0)} tri {' '.join(f'{x:.0f}' for x in m['tri'][1:])}"
            print(line)
        if quick:
            continue
        rec = spec["recommend"][0]
        probe = drain_probe(exe, spec, R[rec]["params"]) if spec.get("drain_probe") else None
        with open(os.path.join(d, "results.json"), "w") as f:
            json.dump({"variants": {k: dict(r) for k, r in R.items()}, "drain_probe": probe}, f, indent=1, default=float)
        with open(os.path.join(d, "README.md"), "w") as f:
            f.write(readme(spec, R, probe))
        with open(os.path.join(d, "numbers.md"), "w") as f:
            f.write(f"# generated by tests/voicing/batch02a.py -- slot {slot:02d} {spec['name']}\n\n")
            for k, r in R.items():
                f.write(f"**{k} {r['tag']}** — {r['desc']}\n\n" + ("\n".join(f"- {c}" for c in r["changes"]) or "- (none: the original)") + "\n\n")
            f.write(tables(spec, R) + "\n")
            if spec["kind"] == "slow":
                f.write("\n### Bloom per second\n\n" + bloom_table(R) + "\n")
            if probe:
                f.write("\n### DRAIN probe\n\n" + probe_table(probe) + "\n")
        print(f"[{slot:02d}] written {d}")


if __name__ == "__main__":
    main()
