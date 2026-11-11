# SPDX-License-Identifier: GPL-3.0-only
"""Batch 6B, 28 Bell Tolls: a long struck bell with body and a clean base.  Probes and the driver.
  python3 tests/voicing/b6c_28.py [--no-cost] [--no-wav] [--only A,B] [--quick]   -> listen/voicing/batch-06b/28/ (results.json; WAVs only on the listen branch)"""
import json
import re
import sys

from lib6c import *
from b6_common import jdefault, save, cpu

OUT = os.path.join(K.ROOT, "listen", "voicing", "batch-06b", "28")
BASE = os.path.join(K.BUILD, "base")
REF = -18.0
LEVEL_PH = "ar_bell_toll"
PHRASES = ["ar_bell_toll", "as_bell_held", "at_bell_chord", "au_bell_run", "av_bell_register"]
WAVMAP = (("ar_bell_toll", "toll"), ("as_bell_held", "held"), ("at_bell_chord", "chord"), ("au_bell_run", "run"), ("av_bell_register", "register"))

# ---- the bell: the KEY is the hum; OSC 1 (a saw at the key) carries the hum, the prime (2x), the quint (3x) and the nominal (4x); OSC 2 (a saw +15 st, ratio 2.378 = the tierce of the prime) carries the minor third; a low-pass
# with the key tracking, an amp envelope that only decays (sustain 0) and a filter envelope that closes the brightness faster than the ring -------------------------------------------------------------------
BELL = dict(MODE=0, POLY_N=5, O1_WAVE=1, O1_PW=64, O1_LVL=127, O2_WAVE=1, O2_PW=64, O2_LVL=70, O2_SEMI=39, O2_FINE=64, XMOD=64, ENV_O2=64, SYNC=0,
            FTYPE=4, CUTOFF=88, RESO=0, KEYTRK=64, FENV_AMT=88, DRIVE=0, VEL_FLT=40, VEL_AMP=60,
            FA=0, FD=90, FS=30, FR=70, AA=0, AS=0,
            VINTAGE=20, SPREAD=70, LFO_PHASE=0, LFO_PITCH=0, LFO_PWM=0, LFO_FLT=0, LFO_AMP=0, LFO_DELAY=0, GROWL=0, CHEW=0, GLIDE=0,
            ALLEY=80, ALLEY_FINE=0, DLY_FB=25, DLY_TONE=80, DLY_MIX=30, BBD_SPREAD=127, REV_SIZE=70, REV_DAMP=35, REV_PRE=15, REV_MIX=20, VOLUME=100)
SHIM = dict(LFO_SHAPE=0, LFO_RATE=40, LFO_PITCH=14, LFO_AMP=20, LFO_DELAY=35, LFO_PHASE=0)
V = {
    "B": ("clean-2s", "the clean base, a ring of about 2 s: AMP DECAY 102, release 102", dict(BELL, AD=102, AR=102)),
    "C": ("dreamy-4s", "a ring of about 4 s, a slow shimmer (TRI 0.37 Hz, pitch +-9.4 cents, amp 20, delay 35)", dict(BELL, AD=111, AR=111, **SHIM)),
    "D": ("long-6s", "a ring of about 6 s, the shimmer, more space (MIX 45, DRAIN 35)", dict(BELL, AD=116, AR=116, DLY_MIX=45, REV_MIX=35, **SHIM)),
}
CAL = {      # calibrations (not candidates): two tries at a tail that keeps its top end
    "Xopen": ("tail-open", "calibration on C: the filter held open (FILTER SUSTAIN 100, DECAY 127, ENV AMT 100, CUTOFF 95): the tail keeps its top end instead of darkening", dict(BELL, AD=111, AR=111, **SHIM, FS=100, FD=127, FENV_AMT=100, CUTOFF=95)),
    "Yrise": ("tail-rise", "calibration on C: the filter opens slowly while the ring decays (CUTOFF 70, ENV AMT 120, FILTER ATTACK 95, SUSTAIN 127): a dark strike, a bright tail", dict(BELL, AD=111, AR=111, **SHIM, CUTOFF=70, FENV_AMT=120, FA=95, FD=120, FS=127)),
}


def level_of(a):
    return K.level_metrics(a, LEVEL_PH)["rms"]


def trim(exe, p):
    v = p.get("VOLUME", 100); best = None
    for _ in range(10):
        a, _ = K.render(exe, LEVEL_PH, params={**p, "VOLUME": v}, tag="trim6c")
        r = level_of(a)
        if best is None or abs(r - REF) < abs(best[1] - REF):
            best = (v, r)
        if abs(r - REF) < 0.12 or (v == 127 and r < REF):
            break
        nv = int(round(v * 10 ** ((REF - r) / 40)))
        v = max(1, min(127, nv if nv != v else v + (1 if REF > r else -1)))
    return best


def fit(exe, p):
    vol, r = trim(exe, p)
    p = {**p, "VOLUME": vol}
    while max(M.peak_db(K.render(exe, ph, params=p, tag="pk6c")[0]) for ph in PHRASES) > -4.0 and p["VOLUME"] > 1:
        p["VOLUME"] -= 1
    return p


def ring(exe, p, n, ov=None, hold=6000, tail=4500):
    """ms after the strike's peak to fall 6 / 12 / 20 / 30 / 40 dB (a 40 ms power envelope: the beats of a bell's partials ripple a short one), the whole patch, the note held `hold` ms"""
    a = solo(exe, p, n, hold=hold, tail=tail, ov=ov)
    return decay_times(a, levels=(6, 12, 20, 30, 40), win=40.0), a


def ons_of(phrase):
    return [int(m[1]) for l in K.phrase_text(phrase).splitlines() for m in [re.match(r"(\d+) midi 0x90", l)] if m]


def pool(exe, p):
    """voice stealing (POLY 4 / 5 / 6 / 8, VINTAGE 0 in all; random start phases make waveforms differ, so levels): the toll (RMS 400-950 ms after each note-on, re POLY 8, mean and worst), the fast run (tail 1.4-3.4 s after its first note) and the chord (3.5 s after)"""
    out = {}
    refs = {ph: K.render(exe, ph, params={**p, "POLY_N": 8, "VINTAGE": 0}, tag="pl8")[0] for ph in ("ar_bell_toll", "au_bell_run", "at_bell_chord")}
    ons = ons_of("ar_bell_toll")
    for nn in (4, 5, 6):
        row = {}
        a = K.render(exe, "ar_bell_toll", params={**p, "POLY_N": nn, "VINTAGE": 0}, tag="pln")[0]
        d = [M.rms_db(a, t + 400, t + 950) - M.rms_db(refs["ar_bell_toll"], t + 400, t + 950) for t in ons[:-1]]
        row["toll_mean"], row["toll_worst"] = float(np.mean(d)), float(min(d))
        a = K.render(exe, "au_bell_run", params={**p, "POLY_N": nn, "VINTAGE": 0}, tag="pln")[0]
        row["run_tail"] = float(M.rms_db(a, 4400, 6400) - M.rms_db(refs["au_bell_run"], 4400, 6400))
        a = K.render(exe, "at_bell_chord", params={**p, "POLY_N": nn, "VINTAGE": 0}, tag="pln")[0]
        row["chord_tail"] = float(M.rms_db(a, 6500, 8500) - M.rms_db(refs["at_bell_chord"], 6500, 8500))
        out[str(nn)] = row
    return out


def space(exe, p, n=69):
    full = solo(exe, p, n, hold=400, tail=3500)
    dry = solo(exe, p, n, hold=400, tail=3500, ov={"DLY_MIX": 0, "REV_MIX": 0})
    return N.wet_windows(full, dry, 3000, wins=((0, 20), (20, 100), (100, 250), (250, 1000)))


def measure(exe, cg, p, key, no_cost, quick=False):
    m = {}
    W = {ph: K.render(exe, ph, params=p, tag="mc6c")[0] for ph in PHRASES}
    m["level"] = level_of(W[LEVEL_PH])
    m["level_chord"] = K.level_metrics(W["at_bell_chord"], "at_bell_chord")["rms"]
    m["level_run"] = K.level_metrics(W["au_bell_run"], "au_bell_run")["rms"]
    m["krms"] = K.level_metrics(W[LEVEL_PH], LEVEL_PH)["rms_k"]
    m["peaks"] = {k: M.peak_db(v) for k, v in W.items()}
    m["peak_all"] = max(m["peaks"].values())
    m["clip"] = int(sum((np.abs(v) >= 32767).sum() for v in W.values()))
    m["b"] = K.level_metrics(K.render(exe, "b_stabs", params=p, tag="mcb")[0], "b_stabs")["rms"]
    m["cost"] = None if (no_cost or cg is None) else cpu(cg, p, "b" + key)
    m["ring"], tails, ladders, shares, cents = {}, {}, {}, {}, {}
    for nm, n in (("A4", 69), ("A3", 57)):
        d, a = ring(exe, p, n)
        m["ring"][nm] = d
        ladders[nm] = {"strike": ladder(a, n + 12, 3000, 3300), "body": ladder(a, n + 12, 4000, 5000)}
        shares[nm] = {"strike_0_400": shares3(a, 3000, 3400), "body_1_2s": shares3(a, 4000, 5000)}
        cents[nm] = {"0-20": cent(a, 3000, 3020, 512), "20-100": cent(a, 3020, 3100, 1024), "100-400": cent(a, 3100, 3400, 2048)}
        tails[nm] = tail_rows(a)
    m["ladder"], m["shares"], m["cent"], m["tail"] = ladders, shares, cents, tails
    # key-up: A4 struck, released at 400 ms (the toll's gate): the level 0.5 / 1 / 2 s after the key-up against the same note held (dB)
    short = solo(exe, p, 69, hold=400, tail=6000)
    held = solo(exe, p, 69, hold=6000, tail=500)
    m["keyup"] = {f"{t}": float(M.rms_db(short, 3400 + t - 50, 3400 + t + 50) - M.rms_db(held, 3400 + t - 50, 3400 + t + 50)) for t in (500, 1000, 2000)}
    m["keyup_t"] = decay_times(short, levels=(20, 40), win=40.0)
    # the dreamy movement: the pitch wobble and the level swing of the LFO on a one-voice probe
    m["wobble"] = ex_wobble(exe, p, n=57)
    q = {**p, "MODE": 0, "POLY_N": 1, "VINTAGE": 0, "O1_WAVE": 1, "O1_LVL": 110, "O2_LVL": 0, "XMOD": 0, "ENV_O2": 64, "FENV_AMT": 64, "FTYPE": 0, "CUTOFF": 127, "RESO": 0, "DRIVE": 0, "GROWL": 0, "DLY_MIX": 0, "REV_MIX": 0, "AA": 0, "AD": 127, "AS": 127, "AR": 40, "CHEW": 0}
    m["tremolo"] = Q.am_depth(run(exe, q, note(3000, 6600, 57), 7000), 3600, 6400)
    m["space"] = space(exe, p)
    m["register"] = {}
    for n in (45, 57, 69, 81, 93):
        a = solo(exe, p, n, hold=1500, tail=1500)
        d = decay_times(solo(exe, p, n, hold=6000, tail=4500), levels=(20, 40), win=40.0)
        m["register"][str(n)] = {"rms": M.rms_db(a, 3000, 3300), "cent": cent(a, 3000, 3100, 1024), "cent_ring": cent(a, 3300, 4000, 2048), "peak": M.peak_db(a), "t20": d["20"], "t40": d["40"]}
    m["pool"] = pool(exe, p)
    return m, W


def live_table(exe, p):
    """the live controls on the base (C) at A3: one step each way (CUTOFF +-10, X-MOD +-20, ENV>O2 +-10 = +-3.8 st at the envelope's top, OSC 2 FINE +-8 = +-6.3 cents, echo MIX +-15, DRAIN +-15; CHEW 0 -> 45, which has no way down): the classical ratios of the strike
    (hum / prime / tierce / quint / nominal re the played note as 1 / 2 / 2.4 / 3 / 4), the centroid of 0-100 ms, the ring to -20 / -40 dB, the level (RMS 0-300 ms, same VOLUME), the strike's partials count above -25 dB that are not on the harmonic series"""
    rows = []
    steps = (("CUTOFF", -10), ("CUTOFF", 0), ("CUTOFF", 10), ("XMOD", -20), ("XMOD", 0), ("XMOD", 20), ("ENV_O2", -10), ("ENV_O2", 0), ("ENV_O2", 10), ("O2_FINE", -8), ("O2_FINE", 0), ("O2_FINE", 8),
             ("DLY_MIX", -15), ("DLY_MIX", 0), ("DLY_MIX", 15), ("REV_MIX", -15), ("REV_MIX", 0), ("REV_MIX", 15), ("CHEW", 45))
    for k, d in steps:
        q = {**p, k: int(np.clip(p[k] + d, 0, 127))} if k != "CHEW" else {**p, "CHEW": d}
        a = solo(exe, q, 57, hold=6000, tail=4500)
        L = ladder(a, 69, 3000, 3300)
        dr = decay_times(a, levels=(20, 40), win=40.0)
        pr = partials(a, 3000, 3300, 57, top=16, floor=-25)
        inh = sum(1 for f_, db, r_, dist in pr if min(abs(f_ / f_of(57) - round(f_ / f_of(57))), 1) > 0.06)
        rows.append({"control": k, "base": p[k] if k != "CHEW" else 0, "step": d, "value": q[k], "ladder": L["classical"], "cent": M.centroid(a, 3000, 3100, nfft=1024), "t20": dr["20"], "t40": dr["40"], "rms": M.rms_db(a, 3000, 3300), "inharmonic": inh})
    return rows


def vs29(exe):
    """slot 29 i scream (main's array) against the bell: the same strike and ring measures at A4 and at C#6 (29's own centre)"""
    p29 = B.resolve(BASE, 29)
    out = {}
    for n in (69, 85):
        d, a = ring(exe, p29, n)
        out[str(n)] = {"ring": d, "cent": {"0-20": cent(a, 3000, 3020, 512), "20-100": cent(a, 3020, 3100, 1024), "100-400": cent(a, 3100, 3400, 2048)},
                       "shares": {"strike_0_400": shares3(a, 3000, 3400), "body_1_2s": shares3(a, 4000, 5000)}, "top": partials(a, 3000, 3300, n, top=8, floor=-40),
                       "ladder_vs_bell": ladder(a, n if n == 69 else n, 3000, 3300)["classical"]}
    return out


def wav_only(exe):
    R = json.load(open(os.path.join(OUT, "results.json")))
    for key, m in R.items():
        if "params" not in m:
            continue
        for ph, sh in WAVMAP:
            if key in CAL and ph not in ("ar_bell_toll", "as_bell_held"):
                continue
            if key == "A" and ph not in ("ar_bell_toll", "as_bell_held"):
                continue
            if ph == "av_bell_register" and key != "C":
                continue              # (the register file for the committed variant only: the listen branch stays light)
            K.write_wav(os.path.join(OUT, f"28_{key}_{sh}.wav"), K.render(exe, ph, params=m["params"], tag="wv6c")[0][int(K.T_CUT * FS):])


def main():
    argv = sys.argv[1:]
    if "--wav-only" in argv:
        wav_only(K.build_host()); return
    no_cost = "--no-cost" in argv
    only = argv[argv.index("--only") + 1].split(",") if "--only" in argv else None
    exe = K.build_host()
    cg = None if no_cost else K.callgrind_exe()
    orig = B.resolve(BASE, 28)
    R = {}
    allv = [("A", "original", "the original array (the FM chime with the hard-chop friction), level-matched: a reference", {})] + [(k, v[0], v[1], v[2]) for k, v in V.items()] + [(k, v[0], v[1], v[2]) for k, v in CAL.items()]
    for key, tag, desc, ch in allv:
        if only and key not in only:
            continue
        p = dict(orig) if key == "A" else {**orig, **ch}
        p = fit(exe, p)
        m, W = measure(exe, cg, p, key, no_cost)
        m["volume"], m["params"], m["tag"], m["desc"] = p["VOLUME"], p, tag, desc
        R[key] = m
        c = m["cost"]; d = m["ring"]["A4"]
        print(f"28{key} {tag:11s} VOL {p['VOLUME']:3d} toll {m['level']:6.2f} chord {m['level_chord']:6.2f} pk {m['peak_all']:6.2f}" + (f" cost {c['total']:.0f}" if c else "") + " | A4 ring " + "/".join("-" if d[k] is None else f"{d[k]:.0f}" for k in ("6", "12", "20", "40")), flush=True)
    if not only:
        pc = R["C"]["params"]
        R["live"] = live_table(exe, pc)
        R["vs29"] = vs29(exe)
        if cg is not None:
            R["addons"] = {"base": cpu(cg, pc, "ab")["total"], "CHEW 45": cpu(cg, {**pc, "CHEW": 45}, "ac")["total"], "GROWL 44": cpu(cg, {**pc, "GROWL": 44}, "ag")["total"], "CHEW 45 + GROWL 44": cpu(cg, {**pc, "CHEW": 45, "GROWL": 44}, "acg")["total"]}
    save(OUT, "results.json" if not only else "results_partial.json", R)


if __name__ == "__main__":
    main()
