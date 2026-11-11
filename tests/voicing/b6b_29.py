# SPDX-License-Identifier: GPL-3.0-only
"""Batch 6A2, 29 "i scream": a struck chime through a cheap van-horn speaker, tape wobble.  Probes and the driver.
  python3 tests/voicing/b6b_29.py [--no-cost] [--no-wav] [--only A,B]   -> listen/voicing/batch-06a2/29/ (results.json; WAVs only on the listen branch)"""
import json
import sys

from lib6b import *
from b6_common import jdefault, save, cpu, wav

OUT = os.path.join(K.ROOT, "listen", "voicing", "batch-06a2", "29")
BASE = os.path.join(K.BUILD, "base")
REF = -18.0
LEVEL_PH = "aj_chime_melody"
PHRASES = ["aj_chime_melody", "ak_chime_melody_lo", "al_chime_melody_hi", "am_chime_singles", "an_chime_chord", "ao_chime_run"]
SPEC = dict(slot=29, dir="29", name="i scream", level=LEVEL_PH, phrases=PHRASES)

# ---- the variants: changes over the ORIGINAL VALHALLA values (full lists are resolved from them) -----------------------------------------------------------------------------------
# the chime: OSC 1 a square, OSC 2 a saw a minor ninth + (O2_SEMI 39 = +15 st, ratio 2.38) at LEVEL 70 with X-MOD 25 and a short pitch zing (ENV>O2 76), a band-pass at a fixed 1.2 kHz (the speaker: KEY TRK 0), amp sustain 0, per-voice DRIVE 30
CHIME = dict(MODE=0, POLY_N=5, O1_WAVE=2, O1_PW=64, O1_LVL=127, O2_WAVE=1, O2_PW=64, O2_LVL=70, O2_SEMI=39, O2_FINE=64, XMOD=25, SYNC=0, ENV_O2=76,
             FTYPE=2, CUTOFF=77, RESO=105, KEYTRK=0, FENV_AMT=64, FA=0, FD=50, FS=0, FR=30, DRIVE=30, VEL_FLT=0,
             AA=0, AS=0, AR=50, VINTAGE=10, SPREAD=70, LFO_PHASE=0, LFO_PITCH=0, LFO_PWM=0, LFO_FLT=0, LFO_AMP=0, LFO_DELAY=0, GROWL=0,
             TP_WOWFLT=64, TP_HISS=25, TP_DROPS=20,
             ALLEY=56, ALLEY_FINE=0, DLY_FB=22, DLY_TONE=60, DLY_MIX=35, BBD_SPREAD=127, REV_SIZE=40, REV_DAMP=40, REV_PRE=8, REV_MIX=18, VOLUME=100)
V = {
    "B": ("plink", "van-true short plink: AMP DECAY 64, light tape (CHEW 25)", dict(CHIME, AD=64, CHEW=25)),
    "C": ("short-ring", "plink with a short ring: AMP DECAY 89, medium tape (CHEW 45)", dict(CHIME, AD=89, CHEW=45)),
    "D": ("long-shimmer", "FINGERSYM-style long ring: AMP DECAY 101, heavier tape (CHEW 65), the delayed LFO shimmer (TRI 0.8 Hz, pitch +-9.4 cents, amp 40, delay 40, PHASE SYNC)", dict(CHIME, AD=101, CHEW=65, LFO_SHAPE=0, LFO_RATE=55, LFO_PITCH=14, LFO_AMP=40, LFO_DELAY=40)),
}
CAL = {
    "Dfinal": ("D-no-tape", "the APPROVED version: variant D with CHEW 0 (no tape at all), everything else as D", dict(CHIME, AD=101, CHEW=0, LFO_SHAPE=0, LFO_RATE=55, LFO_PITCH=14, LFO_AMP=40, LFO_DELAY=40)),
    "Ebox": ("music-box", "calibration: C with a nearer-harmonic interval (OSC 2 +12 st, FINE 70, X-MOD 0, LEVEL 50)", dict(CHIME, AD=89, CHEW=45, O2_SEMI=36, O2_FINE=70, XMOD=0, O2_LVL=50, ENV_O2=64)),
    "Fmetal": ("metallic", "calibration: C with a strongly inharmonic interval (OSC 2 +17 st, LEVEL 100, X-MOD 70)", dict(CHIME, AD=89, CHEW=45, O2_SEMI=41, XMOD=70, O2_LVL=100)),
}


def level_of(a):
    return K.level_metrics(a, LEVEL_PH)["rms"]


def trim(exe, p):
    v = p.get("VOLUME", 100)
    best = None
    for _ in range(10):
        a, _ = K.render(exe, LEVEL_PH, params={**p, "VOLUME": v}, tag="trim6b")
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
    while max(M.peak_db(K.render(exe, ph, params=p, tag="pk6b")[0]) for ph in PHRASES) > -4.0 and p["VOLUME"] > 1:
        p["VOLUME"] -= 1
    return p


def region_shares(a, phrase, nfft=2048):
    """over the note-on region (frames inside a note-on .. note-off): the share of the energy under 400 Hz and above 4 kHz, the centroid (Hz)"""
    x = a.mean(1)
    m = K.gate_mask(phrase, len(x))
    win = np.hanning(nfft)
    f = np.fft.rfftfreq(nfft, 1 / FS)
    lo = hi = tot = num = 0.0
    for s in range(0, len(x) - nfft, nfft // 2):
        if not m[s:s + nfft].all():
            continue
        P = np.abs(np.fft.rfft(x[s:s + nfft] * win)) ** 2
        lo += P[f < 400].sum(); hi += P[f > 4000].sum(); tot += P.sum(); num += (f * P).sum()
    return {"under400": 100 * lo / tot, "over4k": 100 * hi / tot, "cent": num / tot}


def pool(exe, p):
    """voice stealing against the pool (POLY 4 / 5 / 6 / 8; VINTAGE 0 in all): oscillator phases start at random, so renders of different pools never match sample for sample and a difference of waveforms is no measure. The LEVEL of what rings is: on the melody the RMS of the
    last 260 ms of each note's slot (300-560 ms after its note-on, before the next one) re POLY 8, mean and worst note (dB; negative = a ring was cut); on the fast run the RMS 1.4-2.4 s after its first note-on re POLY 8; on the chord the same 4.5 s after"""
    import re
    ons = [int(m[1]) for l in K.phrase_text("aj_chime_melody").splitlines() for m in [re.match(r"(\d+) midi 0x90", l)] if m]
    out = {}
    refs = {ph: K.render(exe, ph, params={**p, "POLY_N": 8, "VINTAGE": 0}, tag="pl8")[0] for ph in ("aj_chime_melody", "ao_chime_run", "an_chime_chord")}
    for nn in (4, 5, 6):
        row = {}
        a = K.render(exe, "aj_chime_melody", params={**p, "POLY_N": nn, "VINTAGE": 0}, tag="pln")[0]
        d = [M.rms_db(a, t + 300, t + 560) - M.rms_db(refs["aj_chime_melody"], t + 300, t + 560) for t in ons[:-1]]
        row["melody_mean"], row["melody_worst"] = float(np.mean(d)), float(min(d))
        a = K.render(exe, "ao_chime_run", params={**p, "POLY_N": nn, "VINTAGE": 0}, tag="pln")[0]
        row["run_tail"] = float(M.rms_db(a, 4400, 5400) - M.rms_db(refs["ao_chime_run"], 4400, 5400))
        a = K.render(exe, "an_chime_chord", params={**p, "POLY_N": nn, "VINTAGE": 0}, tag="pln")[0]
        row["chord_tail"] = float(M.rms_db(a, 7500, 8400) - M.rms_db(refs["an_chime_chord"], 7500, 8400))
        out[str(nn)] = row
    return out


def pdict(p):
    return {k: v for k, v in p.items()}


def measure(exe, cg, p, key, no_cost):
    m = {}
    W = {ph: K.render(exe, ph, params=p, tag="mc6b")[0] for ph in PHRASES}
    m["level"] = level_of(W[LEVEL_PH])
    m["level_chord"] = K.level_metrics(W["an_chime_chord"], "an_chime_chord")["rms"]
    m["level_run"] = K.level_metrics(W["ao_chime_run"], "ao_chime_run")["rms"]
    m["krms"] = K.level_metrics(W[LEVEL_PH], LEVEL_PH)["rms_k"]
    m["peaks"] = {k: M.peak_db(v) for k, v in W.items()}
    m["peak_all"] = max(m["peaks"].values())
    m["clip"] = int(sum((np.abs(v) >= 32767).sum() for v in W.values()))
    m["b"] = K.level_metrics(K.render(exe, "b_stabs", params=p, tag="mcb")[0], "b_stabs")["rms"]
    m["cost"] = None if (no_cost or cg is None) else cpu(cg, p, "i" + key)
    # decay of the actual render: C#6 and C#5 held 3 s, voice only (no tape / sends) and the whole patch
    m["decay"] = {}
    for nm, ov in (("voice", SEND_OFF), ("full", {})):
        m["decay"][nm] = {str(n): decay_times(solo(exe, p, n, hold=3000, tail=1500, ov=ov)) for n in (85, 73)}
    m["env_ms"] = {"amp_decay": 0.5 * 20000 ** (p["AD"] / 127), "filter_decay": 0.5 * 20000 ** (p["FD"] / 127)}      # the time table's nominal time (about 3x the time to 90 % of the fall)
    # tape: pitch wobble on a one-voice probe, with and without CHEW (the LFO as the patch has it in both); the front edge with and without CHEW
    m["wobble"] = {"as_built": ex_wobble(exe, p), "chew0": ex_wobble(exe, {**p, "CHEW": 0})}
    q = {**p, "MODE": 0, "POLY_N": 1, "VINTAGE": 0, "O1_WAVE": 1, "O1_LVL": 110, "O2_LVL": 0, "XMOD": 0, "ENV_O2": 64, "FENV_AMT": 64, "FTYPE": 0, "CUTOFF": 127, "RESO": 0, "DRIVE": 0, "GROWL": 0, "DLY_MIX": 0, "REV_MIX": 0, "AA": 0, "AD": 127, "AS": 127, "AR": 40}
    am = run(exe, q, note(3000, 6600, 73), 7000)
    m["tremolo"] = Q.am_depth(am, 3600, 6400)        # (the one-voice sustained probe: the level modulation of the LFO's AMP and of the tape)
    m["front"] = {}
    for n in (85, 73):
        w = {}
        for nm, ov in (("chew", {}), ("chew0", {"CHEW": 0})):
            a = solo(exe, p, n, hold=800, tail=300, ov={**ov, "DLY_MIX": 0, "REV_MIX": 0})
            c, off = front_edge(a)
            w[nm] = {"cent": c, "onset_ms": off}
        m["front"][str(n)] = w
    # speaker band: the noise probe, and the melody itself (note-on region, whole patch)
    m["speaker"] = speaker(exe, p)
    m["melody_band"] = region_shares(W[LEVEL_PH], LEVEL_PH)
    # partials of the first 100 ms of C#6 and C#5: as heard (the voice only) and raw (the filter open)
    m["partials"] = {}
    for n in (85, 73):
        heard = solo(exe, p, n, hold=600, tail=100, ov=SEND_OFF)
        raw = solo(exe, p, n, hold=600, tail=100, ov={**SEND_OFF, "FTYPE": 0, "CUTOFF": 127, "RESO": 0, "DRIVE": 0})
        m["partials"][str(n)] = {"heard": partials(heard, 3000, 3100, n), "raw": partials(raw, 3000, 3100, n)}
    # space: wet against dry (whole patch against the same with the echo and spring off) in 0-20 / 20-100 / 100-250 ms after the strike (C#6, held 400 ms)
    full = solo(exe, p, 85, hold=400, tail=1500)
    dry = solo(exe, p, 85, hold=400, tail=1500, ov={"DLY_MIX": 0, "REV_MIX": 0})
    m["space"] = N.wet_windows(full, dry, 3000)
    m["space_late"] = N.wet_windows(full, dry, 3000, wins=((250, 500), (500, 1000)))
    # register: A4 / C#6 / A6, one note each
    m["register"] = {}
    for n in (69, 85, 93):
        a = solo(exe, p, n, hold=600, tail=900)
        m["register"][str(n)] = {"rms": M.rms_db(a, 3000, 3300), "cent": M.centroid(a, 3000, 3100, nfft=1024), "cent_ring": M.centroid(a, 3100, 3400, nfft=1024), "peak": M.peak_db(a)}
    m["pool"] = pool(exe, p)
    return m, W


def wav_only(exe):
    """the listening WAVs from the parameter lists in results.json (no measuring)"""
    R = json.load(open(os.path.join(OUT, "results.json")))
    for key, m in R.items():
        if key == "crust":
            continue
        for ph, sh in (("aj_chime_melody", "melody"), ("am_chime_singles", "singles"), ("an_chime_chord", "chord"), ("ao_chime_run", "run"), ("ak_chime_melody_lo", "melody-A4"), ("al_chime_melody_hi", "melody-A6")):
            if key in CAL and ph not in ("aj_chime_melody", "an_chime_chord"):
                continue
            if key == "A" and ph != "aj_chime_melody":
                continue
            wav(OUT, SPEC, key, ph, K.render(exe, ph, params=m["params"], tag="wv6b")[0], sh)


def main():
    argv = sys.argv[1:]
    if "--wav-only" in argv:
        wav_only(K.build_host())
        return
    no_cost, no_wav = "--no-cost" in argv, "--no-wav" in argv
    only = argv[argv.index("--only") + 1].split(",") if "--only" in argv else None
    exe = K.build_host()
    cg = None if no_cost else K.callgrind_exe()
    orig = B.resolve(BASE, 29)
    d = OUT
    R = {}
    allv = [("A", "valhalla-ref", "the original VALHALLA values (a pad), level-matched: a reference, not a candidate", {})] + [(k, v[0], v[1], v[2]) for k, v in V.items()] + [(k, v[0], v[1], v[2]) for k, v in CAL.items()]
    for key, tag, desc, ch in allv:
        if only and key not in only:
            continue
        p = dict(orig) if key == "A" else {**orig, **ch}
        p = fit(exe, p)
        if key == "Dfinal":          # one step above the level search's 112 (-18.03, peak -4.17): 113 reads -17.88 with the chord peak at -4.06, still under -4
            p = {**p, "VOLUME": 113}
        m, W = measure(exe, cg, p, key, no_cost)
        m["volume"], m["params"], m["tag"], m["desc"] = p["VOLUME"], p, tag, desc
        R[key] = m
        c = m["cost"]; dc = m["decay"]["full"]["85"]
        print(f"29{key} {tag:12s} VOL {p['VOLUME']:3d} aj {m['level']:6.2f} an {m['level_chord']:6.2f} pk {m['peak_all']:6.2f}" + (f" cost {c['total']:.0f}" if c else "") +
              f" | decay -6/-12/-20/-40 " + "/".join("-" if dc[k] is None else f"{dc[k]:.0f}" for k in ("6", "12", "20", "40")), flush=True)
        if not no_wav and key != "A" or (not no_wav and key == "A"):
            for ph, sh in (("aj_chime_melody", "melody"), ("am_chime_singles", "singles"), ("an_chime_chord", "chord"), ("ao_chime_run", "run"), ("ak_chime_melody_lo", "melody-A4"), ("al_chime_melody_hi", "melody-A6")):
                if key in CAL and ph not in ("aj_chime_melody", "an_chime_chord"):
                    continue
                if key == "A" and ph not in ("aj_chime_melody",):
                    continue
                wav(d, SPEC, key.replace("*", "star"), ph, W[ph], sh)
    if not only and cg is not None and "C" in R:
        pc = R["C"]["params"]
        cr = []
        for nm, ch in (("DRIVE 0", {"DRIVE": 0}), ("DRIVE 30 (as built)", {}), ("DRIVE 60", {"DRIVE": 60}), ("DRIVE 100", {"DRIVE": 100}), ("GROWL 34", {"GROWL": 34}), ("GROWL 44", {"GROWL": 44}), ("GROWL 44, CHEW 0", {"GROWL": 44, "CHEW": 0}), ("CHEW 0", {"CHEW": 0})):
            q = {**pc, **ch}
            a, _ = K.render(exe, LEVEL_PH, params=q, tag="cr6b")
            cr.append({"name": nm, "crest": R5.N.crest_db(a, LEVEL_PH), "level": level_of(a), "peak": M.peak_db(a), "cost": cpu(cg, q, "cr")["total"]})
        R["crust"] = cr
    save(d, "results.json" if not only else "results_partial.json", R)


if __name__ == "__main__":
    main()
