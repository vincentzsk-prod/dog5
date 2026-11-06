#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Voicing round for Batch 5B, Chapter III "last three": 20 Fire & Ice, 23 Crypt Dust, 24 Fugue State.

  python3 tests/voicing/batch05b.py [--only SLOT] [--no-cost] [--no-wav] [--quick]
  python3 tests/voicing/batch05b.py --emit SLOT KEY      the C array of a variant (from results.json)

A variant is a FULL parameter list (the resolved original + the variant's changes); A is rendered through the base firmware's own program path, B..D over INIT.  VOLUME is trimmed last to -18.0 dBFS RMS
on the patch's level window (20: the note-on region of phrase d_lead; 23, 24: +4 s .. +10 s of the held triad, phrase z_chord), peak <= -4 over every audition phrase.
Output: listen/voicing/batch-05b/<NN-name>/ (README.md + results.json on the merged voicing branch; WAVs only on the never-merged listen branch)."""
import json
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib5b import *
import batch02a as B2
import batch04a as A
import batch05a as R1
from batch05b_variants import V20, V23, V24

OUT = os.path.join(K.ROOT, "listen", "voicing", "batch-05b")
REF = -18.0
NOTE_MS = [125.0, 500 / 3, 250.0, 375.0, 500.0, 750.0, 1000.0]   # DLY_TIME 1/16 1/8T 1/8 1/8. 1/4 1/4. 1/2 at 120 BPM
BASE = os.path.join(K.BUILD, "base")

SPECS = {
    20: dict(dir="20-fire-ice", name="Fire & Ice", cname="FIRE_ICE", V=V20, level="d_lead", phrases=["d_lead", "aa_fire_detached", "ab_fire_legato", "b_stabs"],
             wav=["d_lead", "aa_fire_detached", "ab_fire_legato", "b_stabs"]),
    23: dict(dir="23-crypt-dust", name="Crypt Dust", cname="CRYPT_DUST", V=V23, level="z_chord", phrases=["z_chord", "z_tap", "a_riff", "b_stabs"],
             wav=["z_chord", "z_tap", "a_riff", "b_stabs"]),
    24: dict(dir="24-fugue-state", name="Fugue State", cname="FUGUE_STATE", V=V24, level="z_chord", phrases=["z_chord", "z_tap", "a_riff", "b_stabs", "ad_longhold", "ae_repeat"],
             wav=["z_chord", "z_tap", "a_riff", "b_stabs"]),
}
SHORT = {"d_lead": "lead", "aa_fire_detached": "riff-detached", "ab_fire_legato": "riff-legato", "b_stabs": "stabs", "z_chord": "held-chord", "z_tap": "tap", "a_riff": "riff"}


# ---- shared measures ------------------------------------------------------------------------------------------------------------------------------------------------------
def level_of(a, spec):
    if spec["level"] == "d_lead":
        return K.level_metrics(a, "d_lead")["rms"]
    return M.rms_db(a, 7000, 13000)


def band_db(a, t0, t1, lo, hi, nfft=2048):
    """energy (dB, arbitrary full scale) of the mono sum in [lo, hi) Hz over [t0, t1] ms, Hann frames summed"""
    x = a.mean(1)
    f = np.fft.rfftfreq(nfft, 1 / FS)
    win = np.hanning(nfft)
    e = 0.0
    for s in range(int(t0 * FS / 1000), max(int(t1 * FS / 1000) - nfft, int(t0 * FS / 1000) + 1), nfft // 2):
        if s + nfft > len(x):
            break
        P = np.abs(np.fft.rfft(x[s:s + nfft] * win)) ** 2
        e += P[(f >= lo) & (f < hi)].sum()
    return float(10 * np.log10(max(e, 1e-9)))


def f0_track(a, f0, t0, t1, frame_ms=80, hop_ms=40, span=(0.35, 2.9)):
    """the fundamental in frames (harmonic sum of 3 partials on a 3-cent grid, Hann, zero padded): cents re the median, around the expected f0"""
    x = a.mean(1)
    n, hop = int(frame_ms * FS / 1000), int(hop_ms * FS / 1000)
    NF = 1 << 16
    fr = np.fft.rfftfreq(NF, 1 / FS)
    cand = f0 * 2 ** (np.arange(1200 * np.log2(span[0]), 1200 * np.log2(span[1]), 3) / 1200)
    win = np.hanning(n)
    out = []
    for s in range(int(t0 * FS / 1000), int(t1 * FS / 1000) - n, hop):
        X = np.abs(np.fft.rfft(x[s:s + n] * win, NF))
        sc = sum(np.interp(h * cand, fr, X) / (1 + 0.15 * (h - 1)) for h in (1, 2, 3))
        out.append(cand[int(np.argmax(sc))])
    out = np.array(out)
    return 1200 * np.log2(out / np.median(out)), out


def trk_stats(c, hop_ms=40):
    X = np.abs(np.fft.rfft((c - c.mean()) * np.hanning(len(c)), 1 << 14)) ** 2
    fr = np.fft.rfftfreq(1 << 14, hop_ms / 1000)
    sl = (fr >= 0.05) & (fr <= 12)
    return {"sd": float(c.std()), "min": float(c.min()), "max": float(c.max()), "p5": float(np.percentile(c, 5)), "p95": float(np.percentile(c, 95)), "rate": float(fr[sl][int(np.argmax(X[sl]))])}


def partial_track(a, fc, half_bw, t0, t1, frame_ms=100, hop_ms=25):
    """one partial's frequency over time, as cents re its median: the power centroid of fc +- half_bw Hz in 100 ms Hann frames (zero padded)"""
    x = a.mean(1)
    n, hop, NF = int(frame_ms * FS / 1000), int(hop_ms * FS / 1000), 1 << 15
    fr = np.fft.rfftfreq(NF, 1 / FS)
    sel = (fr > fc - half_bw) & (fr < fc + half_bw)
    out = []
    for s in range(int(t0 * FS / 1000), int(t1 * FS / 1000) - n, hop):
        P = np.abs(np.fft.rfft(x[s:s + n] * np.hanning(n), NF)) ** 2
        out.append((fr[sel] * P[sel]).sum() / max(P[sel].sum(), 1e-9))
    c = np.array(out)
    return 1200 * np.log2(c / np.median(c))


def dips(a, t0, t1, drop_db=6.0, win_ms=10, ref_ms=300):
    """level dips: 10 ms RMS series of the mono sum; an event = a run of frames more than drop_db under the running median of +-ref_ms; returns (count, deepest dB, % of frames inside an event)"""
    x = a.mean(1)[int(t0 * FS / 1000):int(t1 * FS / 1000)]
    w = int(win_ms * FS / 1000)
    n = len(x) // w
    e = 10 * np.log10(np.maximum((x[:n * w].reshape(n, w) ** 2).mean(1), 1e-3) / 32767 ** 2)
    k = int(ref_ms / win_ms)
    med = np.array([np.median(e[max(0, i - k):i + k + 1]) for i in range(n)])
    below = e < med - drop_db
    cnt = int(((below[1:]) & (~below[:-1])).sum() + (1 if below[0] else 0))
    return {"count": cnt, "deepest": float((med - e).max()), "pct": float(100 * below.mean()), "level_sd": float(e.std())}


def win_tab(a, t0=3000, wins=((0, 1), (1, 2), (2, 4), (4, 10)), tail_from=None, tail=((0, .5), (.5, 1.5), (1.5, 3), (3, 5))):
    """windowed tone of a held chord: rms, centroid, band shares, MUD ratio per window of the hold (seconds after the note-on) and of the release"""
    out = {}
    for x, y in wins:
        r, s = mud(a, t0 + x * 1000, t0 + y * 1000)
        out[f"{x}-{y}s"] = {"rms": M.rms_db(a, t0 + x * 1000, t0 + y * 1000), "cent": M.centroid(a, t0 + x * 1000, t0 + y * 1000, nfft=2048), "mud": r, "shares": s}
    if tail_from is not None:
        for x, y in tail:
            r, s = mud(a, tail_from + x * 1000, tail_from + y * 1000)
            out[f"tail {x}-{y}s"] = {"rms": M.rms_db(a, tail_from + x * 1000, tail_from + y * 1000), "cent": M.centroid(a, tail_from + x * 1000, tail_from + y * 1000, nfft=2048), "mud": r, "shares": s}
    return out


def echo_block(exe, p, notes, len_ms=300, tail_ms=7000, n=16, ov=None):
    pfull = p
    p = {**p, **(ov or {})}       # (a pad's own slow attack / long release would smear the repeats into its tail: ov shortens both for this probe only)
    T0 = alley_ms(p["ALLEY"]) if p["ALLEY"] else NOTE_MS[p["DLY_TIME"]]
    if n == 0:                                   # as many repeats as fit in 14 s (up to 40)
        n = int(min(40, 13000 // T0)); tail_ms = int(min(14000, (n + 1) * T0 + 600))
    """the delay's first repeat of an isolated note / chord, its repeat train and the count above -40 dB re the note (Q.first_repeat / repeats_train)"""
    T = alley_ms(p["ALLEY"]) if p["ALLEY"] else NOTE_MS[p["DLY_TIME"]]      # ALLEY 0 = the SYNC note value at the host's 120 BPM
    S, on, off = Q.solo_set(exe, p, notes, len_ms, tail_ms=tail_ms, tag="e5b")
    first = Q.first_repeat(S, on, off, T)
    train = Q.repeats_train(S, on, off, T, n=n)
    d_ = S["dly"] - S["dry"]
    e_ = M.env_ms(d_)
    pk_ = float(e_[int(on):int(on) + len_ms + 2 * int(T)].max())
    last_ = int(np.nonzero(e_[int(on):] > pk_ - 40)[0].max())
    return {"t40_ms": float(last_ - len_ms), "ms": T, "fb": p["DLY_FB"], "first": first, "train": train, "n40": sum(1 for k, t, v in train if v + first["dly_re_note"] > -40),
            "n20": sum(1 for k, t, v in train if v + first["dly_re_note"] > -20), "mix": p["DLY_MIX"]}


def peaks(exe, spec, p):
    return {ph: M.peak_db(K.render(exe, ph, params=p, tag="pk5b")[0]) for ph in spec["phrases"]}


def trim(exe, spec, p):
    v = p.get("VOLUME", 100)
    best = None
    for _ in range(9):
        a, _ = K.render(exe, spec["level"], params={**p, "VOLUME": v}, tag="trim5b")
        r = level_of(a, spec)
        if best is None or abs(r - REF) < abs(best[1] - REF):
            best = (v, r)
        if abs(r - REF) < 0.12:
            break
        nv = int(round(v * 10 ** ((REF - r) / 40)))
        v = max(1, min(127, nv if nv != v else v + (1 if REF > r else -1)))
    return best


# ---- 20 Fire & Ice ---------------------------------------------------------------------------------------------------------------------------------------------------------
SW_WINS = ((0, 100), (100, 200), (200, 400), (400, 800))


def sweep_rows(exe, p, note_n=69):
    """the hard-sync sweep on one detached note (A4, 900 ms), FX off: per window the centroid and the 1.2 kHz+ energy with the sweep (ENV>O2 as set) and without (ENV>O2 = 64), and the same energy with the
    filter fully open (CUTOFF 127, sweep on) = what the sweep would be with nothing rolled off"""
    res = {}
    for nm, ov in (("on", {}), ("off", {"ENV_O2": 64}), ("open", {"CUTOFF": 127})):
        q = {**p, **FXOFF, **ov}
        a = run(exe, q, note(3000, 3900, note_n), 4400, tag="sw5b")
        res[nm] = [{"cent": M.centroid(a, 3000 + x, 3000 + y, nfft=1024), "hi": band_db(a, 3000 + x, 3000 + y, 1200, 22000, nfft=1024), "rms": M.rms_db(a, 3000 + x, 3000 + y)} for x, y in SW_WINS]
    rows = []
    for i, w in enumerate(SW_WINS):
        rows.append({"w": w, "cent_on": res["on"][i]["cent"], "cent_off": res["off"][i]["cent"], "d_cent": res["on"][i]["cent"] - res["off"][i]["cent"],
                     "d_hi": res["on"][i]["hi"] - res["off"][i]["hi"], "hi_vs_open": res["on"][i]["hi"] - res["open"][i]["hi"], "rms": res["on"][i]["rms"]})
    return rows


def riff_rows(exe, p, phrase, tag):
    """per note of a riff, dry (FX off, GROWL 0): centroid over 0-100 ms and 100-300 ms after the note-on, with the sweep (as set) and without (ENV>O2 64)"""
    import re
    ons = [int(m[1]) for l in K.phrase_text(phrase).splitlines() for m in [re.match(r"(\d+) midi 0x90 (\d+)", l)] if m]
    ns = [int(m[2]) for l in K.phrase_text(phrase).splitlines() for m in [re.match(r"(\d+) midi 0x90 (\d+)", l)] if m]
    out = {}
    for nm, ov in (("on", {}), ("off", {"ENV_O2": 64})):
        q = {**p, **FXOFF, **ov}
        a, _ = K.render(exe, phrase, params=q, tag=tag)
        out[nm] = [(M.centroid(a, t, t + 100, nfft=1024), M.centroid(a, t + 100, t + 300, nfft=1024), band_db(a, t, t + 100, 1200, 22000, nfft=1024)) for t in ons[:16]]
    return {"notes": ns[:16], "on": out["on"], "off": out["off"]}


def glide_probe(exe, p):
    """the slide of a legato step A3 -> A4: dry, the fundamental tracked in 20 ms frames; ms from the second note-on to within 50 cents of A4 and the time to 90 % of the octave"""
    q = {**p, **FXOFF, "ENV_O2": 64, "SYNC": 0, "O1_LVL": p["O2_LVL"], "O1_WAVE": 1, "O2_WAVE": 0, "FENV_AMT": 64, "LFO_PITCH": 0}
    a = run(exe, q, ["3000 midi 0x90 57 100", "5000 midi 0x90 69 100", "5050 midi 0x80 57 0", "7000 midi 0x80 69 0"], 7400, tag="gl5b")
    x = a.mean(1)
    n, hop = int(0.04 * FS), int(0.005 * FS)
    NF = 1 << 16
    fr = np.fft.rfftfreq(NF, 1 / FS)
    cand = 220 * 2 ** (np.arange(-100, 1400, 4) / 1200)
    res = []
    for s in range(int(4.5 * FS), int(6.5 * FS), hop):
        X = np.abs(np.fft.rfft(x[s:s + n] * np.hanning(n), NF))
        sc = sum(np.interp(h * cand, fr, X) for h in (1, 2, 3))
        res.append((s / FS * 1000 - 5000, 1200 * np.log2(cand[int(np.argmax(sc))] / 220)))
    t = np.array([r[0] for r in res]); c = np.array([r[1] for r in res])
    post = t >= 0
    t, c = t[post], c[post]
    t50 = float(t[np.nonzero(np.abs(c - 1200) <= 50)[0][0]]) if (np.abs(c - 1200) <= 50).any() else None
    t90 = float(t[np.nonzero(c >= 1200 * 0.9)[0][0]]) if (c >= 1080).any() else None
    return {"glide": p["GLIDE"], "t_within50": t50, "t90": t90}


def measure_20(exe, p, m, W):
    m["sweep"] = sweep_rows(exe, p)
    m["sweep_a3"] = sweep_rows(exe, p, note_n=57)[0:2]
    m["det"] = riff_rows(exe, p, "aa_fire_detached", "rd5b")
    m["leg"] = riff_rows(exe, p, "ab_fire_legato", "rl5b")
    m["glide"] = glide_probe(exe, p)
    dry = {**p, **FXOFF}
    nog = K.render(exe, "d_lead", params=dry, tag="cr5b")[0]
    gr = K.render(exe, "d_lead", params={**dry, "GROWL": p["GROWL"]}, tag="cr5b2")[0]
    m["crest"] = {"growl0": N.crest_db(nog, "d_lead"), "growl": N.crest_db(gr, "d_lead"), "rms_shift": K.level_metrics(gr, "d_lead")["rms"] - K.level_metrics(nog, "d_lead")["rms"], "growl_value": p["GROWL"]}
    m["echo"] = echo_block(exe, p, [69], len_ms=300, tail_ms=8000, n=16)
    m["growl_cost"] = None


# ---- 23 Crypt Dust ---------------------------------------------------------------------------------------------------------------------------------------------------------
def measure_23(exe, p, m, W):
    a = W["z_chord"]
    m["windows"] = win_tab(a, 3000, tail_from=13000)
    m["chew"] = p["CHEW"]
    # tape and what it does, against the same patch with CHEW 0: pitch wander of the thin pulse on one held A3, dropouts and hiss floor on the held triad
    p0 = {**p, "CHEW": 0}
    a0 = K.render(exe, "z_chord", params=p0, tag="m23c0")[0]
    m["windows_nochew"] = win_tab(a0, 3000, tail_from=13000, wins=((4, 10),), tail=((0, .5),))
    t = {}
    # the pitch wander of the thin pulse alone (noise, echo and spring off, LFO off, one voice): the strongest harmonic of A3 between the 5th and the 24th in the CHEW 0 render is tracked (+-100 Hz)
    pp = {**p, "NOISE": 0, "DLY_MIX": 0, "REV_MIX": 0, "GROWL": 0, "VINTAGE": 0, "MODE": 0, "LFO_AMP": 0, "LFO_FLT": 0}
    ref = run(exe, {**pp, "CHEW": 0}, note(3000, 11000, 57), 11500, tag="w23r")
    Xs = np.abs(np.fft.rfft(ref.mean(1)[int(5 * FS):int(10 * FS)] * np.hanning(int(5 * FS))))
    fq = np.fft.rfftfreq(int(5 * FS), 1 / FS)
    hs = {h: Xs[(fq > 220 * h - 60) & (fq < 220 * h + 60)].max() for h in range(5, 25)}
    hbest = max(hs, key=hs.get)
    m["wow_partial"] = {"harmonic": hbest, "hz": 220.0 * hbest}
    for nm, q in (("as", p), ("chew0", p0)):
        a2 = run(exe, {**pp, "CHEW": q["CHEW"]}, note(3000, 11000, 57), 11500, tag="w23p")
        c = partial_track(a2, 220.0 * hbest, 100, 4000, 11000)
        a1 = run(exe, {**q, "GROWL": 0}, note(3000, 11000, 57), 14000, tag="w23")
        t[nm] = trk_stats(c, hop_ms=25) if np.isfinite(c).all() else {"sd": None, "p5": None, "p95": None, "rate": None, "min": None, "max": None}
        t[nm]["dips"] = dips(a1, 4000, 11000)
        t[nm]["dips_chord"] = dips(a if nm == "as" else a0, 7000, 13000)
        t[nm]["floor"] = {w: M.rms_db(a if nm == "as" else a0, 3000 + w * 1000, 3000 + (w + 1) * 1000) for w in (14, 15)}
        t[nm]["hf"] = M.band_shares(a if nm == "as" else a0, 7000, 13000)["1.2k+"]
        t[nm]["cent"] = M.centroid(a if nm == "as" else a0, 7000, 13000, nfft=2048)
    m["tape"] = t
    dry = {**p, **FXOFF}
    ad = K.render(exe, "z_chord", params=dry, tag="m23d")[0]
    m["dry_windows"] = win_tab(ad, 3000, wins=((4, 10),))
    m["lfo"] = {"hz": lfo_hz(p["LFO_RATE"]), "shape": p["LFO_SHAPE"], "amp_dip_db": Q.amp_db(p["LFO_AMP"]) if p["LFO_AMP"] else 0.0, "flt_st": ((p["LFO_FLT"] * p["LFO_FLT"]) >> 7) * 97 / 256,
                "level_sd": dips(ad, 7000, 13000)["level_sd"]}
    m["echo"] = echo_block(exe, p, [57, 61, 64], 120, 0, 0, ov=dict(AA=30, AR=40)) if p["DLY_MIX"] else None
    m["tap"] = {"gate": M.rms_db(W["z_tap"], 3000, 3150), "hover": M.tail_times(W["z_tap"], 3150, 150, 4500)}
    m["hover"] = M.tail_times(a, 13000, 150, 5800)


# ---- 24 Fugue State --------------------------------------------------------------------------------------------------------------------------------------------------------
def tri_cents(v):
    return ((v * v) >> 7) * 9.375


def lfo_pair_gap(peak_c, hz, T_ms):
    """the largest pitch difference (cents) between the direct voice and its echo T ms later, from the LFO law (a triangle of +-peak at hz): computed, not measured"""
    t = np.linspace(0, 4 / hz, 20000)
    tri = lambda x: 2 * np.abs(2 * ((x * hz) % 1) - 1) - 1
    return float(np.abs(peak_c * tri(t) - peak_c * tri(t - T_ms / 1000)).max())


def measure_24(exe, p, m, W):
    a = W["z_chord"]
    m["windows"] = win_tab(a, 3000, tail_from=13000)
    dryp = {**p, **FXOFF}
    ad = K.render(exe, "z_chord", params=dryp, tag="m24d")[0]
    m["dry_windows"] = win_tab(ad, 3000, wins=((4, 10),))
    m["tri"] = A.tri_probe(exe, {**p, "FTYPE": p["FTYPE"], "O2_WAVE": 0})[:]
    both = {**p, "O1_WAVE": 2}
    m["tri_pair"] = B2.triangle_probe(exe, {**both, "LFO_PWM": 0, "LFO_PITCH": 0, "MODE": 0})[1:]
    # the measured pitch excursion of the LFO: one voice, POLY, VINTAGE 0, no effects, LFO phase SYNC, A3 held 12 s (the slow rates need several cycles)
    q = {**dryp, "MODE": 0, "VINTAGE": 0, "LFO_PHASE": 0, "O2_WAVE": 0}
    a1 = run(exe, q, note(3000, 15000, 57), 15500, tag="p24")
    c, _ = f0_track(a1, 220.0, 3500, 15000, frame_ms=60, hop_ms=30, span=(0.35, 3.0))
    m["pitch"] = trk_stats(c, hop_ms=30)
    m["pitch"]["law_cents"] = tri_cents(p["LFO_PITCH"])
    m["pitch"]["hz"] = lfo_hz(p["LFO_RATE"])
    m["pitch"]["semitones_pp"] = (m["pitch"]["max"] - m["pitch"]["min"]) / 100
    m["pitch"]["pitch_byte"] = p["LFO_PITCH"]
    T = alley_ms(p["ALLEY"])
    m["echo"] = echo_block(exe, p, [57, 61, 64], 120, 0, 0, ov=dict(AA=30, AR=40))
    m["gap_cents"] = lfo_pair_gap(tri_cents(p["LFO_PITCH"]), lfo_hz(p["LFO_RATE"]), T)
    # long hold: the triad held 30 s: peak and RMS per 2 s window; the repeated chord: peak per chord
    h = W["ad_longhold"]
    m["long"] = [{"t": s, "peak": M.peak_db(h, 3000 + s * 1000, 3000 + (s + 2) * 1000), "rms": M.rms_db(h, 3000 + s * 1000, 3000 + (s + 2) * 1000)} for s in range(0, 30, 2)]
    m["long_tail"] = [{"t": s, "peak": M.peak_db(h, 33000 + s * 1000, 33000 + (s + 2) * 1000), "rms": M.rms_db(h, 33000 + s * 1000, 33000 + (s + 2) * 1000)} for s in range(0, 12, 2)]
    m["long_growth"] = m["long"][-2]["peak"] - m["long"][1]["peak"]
    e = W["ae_repeat"]
    m["rep"] = [M.peak_db(e, 3000 + k * 1000, 3000 + (k + 1) * 1000) for k in range(12)]
    m["rep_tail"] = [M.peak_db(e, 15000 + s * 1000, 15000 + (s + 2) * 1000) for s in (0, 2, 4, 6)]
    m["rep_growth"] = max(m["rep"][3:]) - m["rep"][0]
    m["hover"] = M.tail_times(a, 13000, 150, 5800)
    m["tap"] = {"gate": M.rms_db(W["z_tap"], 3000, 3150), "hover": M.tail_times(W["z_tap"], 3150, 150, 4500)}
    m["o2_probe"] = []
    for lv in (0, 45, 70, 100):
        ao = K.render(exe, "z_chord", params={**dryp, "O2_LVL": lv, "O2_WAVE": 2 if lv else 0}, tag="o2p")[0]
        r_, s_ = mud(ao, 7000, 13000)
        m["o2_probe"].append({"o2_lvl": lv, "cent": M.centroid(ao, 7000, 13000, nfft=2048), "mud": r_, "shares": s_, "rms": M.rms_db(ao, 7000, 13000)})
    m["corr_full"] = Q.chan_corr(a, 7000, 13000)


# ---- the common block ------------------------------------------------------------------------------------------------------------------------------------------------------
def common(exe, old, spec, key, p, no_cost, cg):
    m = {}
    use_old = key == "A"
    def rend(ph, params=p):
        if use_old:
            return K.render(old, ph, program=spec["slot"] - 1, tag="mc5b")[0]
        return K.render(exe, ph, params=params, tag="mc5b")[0]
    W = {ph: rend(ph) for ph in spec["phrases"]}
    m["level"] = level_of(W[spec["level"]], spec)
    m["krms"] = (R1.krms(W["z_chord"], 7000, 13000) if spec["level"] == "z_chord" else K.level_metrics(W["d_lead"], "d_lead")["rms_k"])
    m["peaks"] = {k: M.peak_db(v) for k, v in W.items()}
    m["peak_all"] = max(m["peaks"].values())
    m["clip"] = int(sum((np.abs(v) >= 32767).sum() for v in W.values()))
    m["b"] = K.level_metrics(W["b_stabs"], "b_stabs")["rms"]
    m["cost"] = None
    if cg and not no_cost:
        cb, cl = K.cost(cg, params=p, tag="c5b" + key)
        ir, fr = K.callgrind_ips(cg, "x_stress", params=p, tag="ci5b" + key, notes=False)
        m["cost"] = {"b": cb, "load": cl, "idle": ir / fr}
    return m, W


def run_spec(slot, no_cost, no_wav, quick):
    spec = SPECS[slot]; spec["slot"] = slot
    exe = K.build_host()
    cg = None if (no_cost or quick) else K.callgrind_exe()
    old = K.build_host(BASE, os.path.join(K.BUILD, "obervave_base"))
    orig = B.resolve(BASE, slot)
    d = os.path.join(OUT, spec["dir"]); os.makedirs(d, exist_ok=True)
    R, WS = {}, {}
    todo = [("A", "original", "the original through the base program path", {})] + [(k, v[0], v[1], v[2]) for k, v in spec["V"].items()]
    for key, tag, desc, ch in todo:
        p = dict(orig) if key == "A" else {**orig, **ch}
        if key != "A":
            vol, _ = trim(exe, spec, p)
            p["VOLUME"] = vol
            while max(peaks(exe, spec, p).values()) > -4.0 and p["VOLUME"] > 1:
                p["VOLUME"] -= 1
        m, W = common(exe, old, spec, key, p, no_cost, cg)
        if not quick:
            {20: measure_20, 23: measure_23, 24: measure_24}[slot](exe, p, m, W) if key != "A" else \
                {20: measure_20, 23: measure_23, 24: measure_24}[slot](exe, p, m, W)
        if slot == 20 and cg and not no_cost and key != "A":
            cb, cl = K.cost(cg, params={**p, "GROWL": 0}, tag="cg5b" + key)
            m["cost_growl0"] = {"b": cb, "load": cl}
        m["volume"], m["params"], m["tag"], m["desc"] = p["VOLUME"], p, tag, desc
        R[key], WS[key] = m, W
        c = m["cost"]
        print(f"{slot}{key} {tag:9s} VOL {p['VOLUME']:3d} lvl {m['level']:6.2f} k {m['krms']:6.2f} b {m['b']:6.2f} pk {m['peak_all']:6.2f}" + (f" cost {c['idle'] + c['load']:.0f}" if c else ""), flush=True)
    # A* = the original's tone, VOLUME alone moved onto the reference (a listening aid)
    pa = dict(orig); va, ra = trim(exe, spec, pa); pa["VOLUME"] = va
    while max(peaks(exe, spec, pa).values()) > -4.0 and pa["VOLUME"] > 1:
        pa["VOLUME"] -= 1
    R["A*"] = {"volume": pa["VOLUME"], "level": ra, "params": pa, "tag": "original-matched", "desc": "the original's tone with VOLUME alone moved onto the reference (a listening aid, not a candidate)", "peak_all": max(peaks(exe, spec, pa).values())}
    print(f"{slot}A* VOL {pa['VOLUME']} lvl {ra:.2f}")
    if not no_wav and not quick:
        for key in R:
            pp = R[key]["params"]
            for ph in spec["wav"]:
                if key == "A" and ph != spec["level"]:
                    continue                       # the raw original: the level phrase only (A* carries the rest at the common level)
                a = WS[key][ph] if key in WS else K.render(exe, ph, params=pp, tag="wav5b")[0]
                K.write_wav(os.path.join(d, f"{spec['dir']}_{key.replace('*', 'star')}_{SHORT[ph]}.wav"), a[int(K.T_CUT * FS):])
    return R, d


def jdefault(o):
    return A.jdefault(o)


def main():
    argv = sys.argv[1:]
    if "--emit" in argv:
        i = argv.index("--emit"); slot, key = int(argv[i + 1]), argv[i + 2]
        res = json.load(open(os.path.join(OUT, SPECS[slot]["dir"], "results.json")))
        print(B.emit("PF_" + SPECS[slot]["cname"] if False else SPECS[slot]["cname"], res[key]["params"]))
        return
    if "--check" in argv:                       # the committed slot against its variant: resolved bytes, and the audio loaded from INIT
        exe = K.build_host()
        for slot, spec in SPECS.items():
            key = argv[argv.index("--check") + 1] if len(argv) > argv.index("--check") + 1 and not argv[argv.index("--check") + 1].startswith("--") else "B"
            res = json.load(open(os.path.join(OUT, spec["dir"], "results.json")))
            cur = B.resolve(K.ROOT, slot)
            same = cur == res[key]["params"]
            print(f"{slot:02d} {key}: resolved bytes identical: {same}")
            for label, extra in (("from the boot patch", ()), ("both from INIT first (program 33 at 2000 ms)", ("2000 midi 0xC0 32 0",))):
                out = []
                for ph in spec["phrases"]:
                    x = K.render(exe, ph, program=slot - 1, extra=extra, tag="chk")[0]
                    y = K.render(exe, ph, params=res[key]["params"], extra=extra, tag="chk2")[0]
                    out.append(f"{ph} " + ("bit-identical" if (x == y).all() else f"differs {10 * np.log10(max(((x - y) ** 2).mean(), 1e-9) / (x ** 2).mean()):.1f} dB"))
                print(f"   {label}: " + "; ".join(out))
        return
    only = int(argv[argv.index("--only") + 1]) if "--only" in argv else None
    for slot in SPECS:
        if only and slot != only:
            continue
        R, d = run_spec(slot, "--no-cost" in argv, "--no-wav" in argv, "--quick" in argv)
        if "--quick" not in argv:
            json.dump(R, open(os.path.join(d, "results.json"), "w"), default=jdefault, indent=1)


if __name__ == "__main__":
    main()
