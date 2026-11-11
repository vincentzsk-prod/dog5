# SPDX-License-Identifier: GPL-3.0-only
"""Batch 6A, 26 BSyncA: a fat, warm, crunchy hard-sync lead (UNISON 3).  Variant tables, probes and the driver.
  python3 tests/voicing/b6_26.py [--no-cost] [--no-wav]      -> listen/voicing/batch-06a/26-bsynca/ (results.json, README.md; WAVs only on the listen branch)"""
import re
import sys

from b6_common import *

SPEC = dict(slot=26, dir="26-bsynca", name="BSyncA", cname="BSYNCA", level="d_lead",
            phrases=["d_lead", "aa_fire_detached", "ab_fire_legato", "b_stabs", "af_lead_held"])
# the fat, warm base shared by B, C, D (changes over the original): the master (OSC 1 saw) audible under the synced slave, UNISON 3 detuned, a lower cutoff with a bigger envelope, a little glide, dry
FAT = dict(O1_LVL=90, MODE=2, UNI_N=3, UNI_DET=22, CUTOFF=84, FENV_AMT=100, GLIDE=50, DLY_MIX=0, REV_MIX=0)
ROOM = dict(ALLEY=64, DLY_FB=22, DLY_TONE=55, DLY_MIX=28, REV_SIZE=60, REV_MIX=18)
V = {
    "B": ("drive", "the fat base + per-voice filter DRIVE 60, no GROWL, dry", dict(**FAT, DRIVE=60)),
    "C": ("growl34", "the fat base + GROWL 34, dry", dict(**FAT, GROWL=34)),
    "D": ("growl44", "the fat base + GROWL 44, dry", dict(**FAT, GROWL=44)),
}
CAL = {      # calibration renders, NOT candidates: where the ladder goes on, and the room
    "E52": ("growl52", "calibration: the fat base + GROWL 52, dry", dict(**FAT, GROWL=52)),
    "F70": ("growl70", "calibration: the fat base + GROWL 70, dry (the dictionary's fuzzy edge)", dict(**FAT, GROWL=70)),
    "Droom": ("growl44-room", "calibration: D + a very light room (86 ms slap, FEEDBK 22, MIX 28; spring MIX 18, SIZE 60)", {**FAT, "GROWL": 44, **ROOM}),
}
NOTE = 57          # A3, the rip probe note
WINS = ((0, 50), (50, 150), (150, 400))


def ons_of(phrase):
    return [(int(m[1]), int(m[2])) for l in K.phrase_text(phrase).splitlines() for m in [re.match(r"(\d+) midi 0x90 (\d+)", l)] if m]


def rip(exe, p):
    """one detached A3 (1 s), FX off, GROWL / DRIVE as set: centroid and 1.2 kHz+ share in the windows, with the sweep as set and without it (ENV>O2 64)"""
    out = {}
    for nm, ov in (("on", {}), ("off", {"ENV_O2": 64})):
        a = run(exe, {**p, **DRY, **ov}, note(3000, 4000, NOTE), 4500)
        out[nm] = [{"w": w, "cent": M.centroid(a, 3000 + w[0], 3000 + w[1], nfft=512), "hi": M.band_shares(a, 3000 + w[0], 3000 + w[1], nfft=512)["1.2k+"]} for w in WINS]
    return out


def riffs(exe, p):
    """centroid over the first 100 ms of notes 2-8 of the detached and the legato riff (dry), with the sweep and without; and the level of those 100 ms re the same in the detached riff"""
    res = {}
    for ph in ("aa_fire_detached", "ab_fire_legato"):
        on = [t for t, n in ons_of(ph)][1:8]
        r = {}
        for nm, ov in (("on", {}), ("off", {"ENV_O2": 64})):
            a, _ = K.render(exe, ph, params={**p, **DRY, **ov}, tag="rf6")
            r[nm] = [(M.centroid(a, t, t + 100, nfft=512), M.rms_db(a, t, t + 100)) for t in on]
        res[ph] = {nm: {"cent": float(np.mean([c for c, _ in v])), "rms": float(np.mean([l for _, l in v]))} for nm, v in r.items()}
    return res


def held(exe, p):
    """held A3 (4 s), dry: centroid in windows after the strike, the level re the first second, the unison beat (the 220 Hz band's envelope)"""
    a, _ = K.render(exe, "af_lead_held", params={**p, **DRY}, tag="hd6")
    out = {"cent": {f"{x}-{y}": M.centroid(a, 3000 + x, 3000 + y, nfft=2048) for x, y in ((0, 150), (150, 400), (400, 1000), (1000, 2500), (2500, 4000))}}
    out["rms"] = {f"{x}-{y}": M.rms_db(a, 3000 + x, 3000 + y) for x, y in ((0, 400), (400, 1000), (1000, 2500), (2500, 4000))}
    out["beat"] = K.beat_metrics(a, 220.0, 3500, 7000)
    return out


def glide_ms(exe, p):
    """ms to within 50 cents of A4 after a legato step A3 -> A4 (R5.glide_probe)"""
    return R5.glide_probe(exe, p)


def ladder_row(exe, cg, p, base_ref, no_cost):
    a, _ = K.render(exe, "d_lead", params={**p, **DRY, "VOLUME": 100}, tag="ld6")
    r = {"crest": R5.N.crest_db(a, "d_lead"), "level": K.level_metrics(a, "d_lead")["rms"], "peak": M.peak_db(a)}
    r["shift"] = r["level"] - base_ref
    r["rip"] = rip(exe, {**p, "VOLUME": 100})
    r["cost"] = None if no_cost else cpu(cg, {**p, **DRY}, "L")
    return r


def main():
    no_cost, no_wav = "--no-cost" in sys.argv, "--no-wav" in sys.argv
    exe = K.build_host()
    cg = None if no_cost else K.callgrind_exe()
    orig = B.resolve(BASE, 26)
    d = os.path.join(OUT, SPEC["dir"])
    R, WS = {}, {}
    ref_a, _ = K.render(exe, "d_lead", params={**orig, **FAT, **DRY, "VOLUME": 100}, tag="ref6")
    base_ref = K.level_metrics(ref_a, "d_lead")["rms"]
    allv = [("A", "original", "the original through the base program path", {})] + [(k, v[0], v[1], v[2]) for k, v in V.items()] + [(k, v[0], v[1], v[2]) for k, v in CAL.items()]
    for key, tag, desc, ch in allv:
        p = dict(orig) if key == "A" else {**orig, **ch}
        if key != "A":
            p = fit(exe, SPEC, p)
        m, W = common(exe, cg, SPEC, key, p, no_cost)
        m["rip"], m["riffs"], m["held"] = rip(exe, p), riffs(exe, p), held(exe, p)
        if key in ("A", "B", "C", "D"):
            m["glide"] = glide_ms(exe, p)
        m["ladder"] = ladder_row(exe, cg, p, base_ref, no_cost) if key != "A" else None
        m["volume"], m["params"], m["tag"], m["desc"] = p["VOLUME"], p, tag, desc
        R[key], WS[key] = m, W
        c = m["cost"]
        print(f"26{key} {tag:12s} VOL {p['VOLUME']:3d} lvl {m['level']:6.2f} b {m['b']:6.2f} pk {m['peak_all']:6.2f}" + (f" cost {c['total']:.0f}" if c else ""), flush=True)
    # A*: the original with VOLUME alone moved onto the reference
    pa = fit(exe, SPEC, dict(orig)); ra = trim(exe, SPEC, dict(orig))[1]
    R["A*"] = {"volume": pa["VOLUME"], "level": ra, "params": pa, "tag": "original-matched", "desc": "the original's tone with VOLUME alone moved onto the reference (a listening aid)"}
    # the fat base without any drive: the reference of the ladder
    R["ladder_ref"] = {"level_vol100": base_ref}
    # fatness probe: UNISON 1 (MONO) / 2 / 3 / 4 on the fat base (GROWL 0): the beat, the level at VOLUME 100 and the cost
    fat = []
    for n, det in ((1, 0), (2, 22), (3, 22), (4, 22), (3, 40)):
        q = {**orig, **FAT, "MODE": 3 if n == 1 else 2, "UNI_N": max(n, 2), "UNI_DET": det, "VOLUME": 100}
        a, _ = K.render(exe, "af_lead_held", params={**q, **DRY}, tag="ft6")
        al, _ = K.render(exe, "d_lead", params={**q, **DRY}, tag="ft6")
        fat.append({"voices": n, "det": det, "beat": K.beat_metrics(a, 220.0, 3500, 7000), "level": K.level_metrics(al, "d_lead")["rms"], "crest": R5.N.crest_db(al, "d_lead"),
                    "cost": None if no_cost else cpu(cg, {**q, **DRY}, "F")})
    R["fatness"] = fat
    # more rungs of the ladder (numbers only): no drive at all, GROWL 90 and 127 (where, if anywhere, the crest reaches the fuzz marker 2.3 dB)
    ex = []
    for nm, ch in (("no drive (the fat base)", {}), ("GROWL 90", {"GROWL": 90}), ("GROWL 127", {"GROWL": 127})):
        a, _ = K.render(exe, "d_lead", params={**orig, **FAT, **DRY, "VOLUME": 100, **ch}, tag="lx6")
        ex.append({"name": nm, "crest": R5.N.crest_db(a, "d_lead"), "shift": K.level_metrics(a, "d_lead")["rms"] - base_ref, "peak": M.peak_db(a)})
    R["ladder_extra"] = ex
    # rip depth probe: ENV>O2 88 / 104 / 116 on the fat base (dry, GROWL 0)
    dep = []
    for e2 in (80, 88, 104, 116, 127):
        q = {**orig, **FAT, "ENV_O2": e2, "VOLUME": 100}
        dep.append({"env_o2": e2, "st": (e2 - 64) * 24 / 63, "rip": rip(exe, q)})
    R["depth"] = dep
    if not no_wav:
        for key in [k for k in R if k in ("A*", "B", "C", "D", "E52", "F70", "Droom")]:
            pp = R[key]["params"]
            for ph, sh in (("d_lead", "lead"), ("aa_fire_detached", "riff-detached"), ("ab_fire_legato", "riff-legato"), ("b_stabs", "stabs"), ("af_lead_held", "held")):
                if key in ("E52", "F70", "Droom") and ph not in ("d_lead", "af_lead_held"):
                    continue              # (the calibrations: the lead run and the held note only, to keep the listen branch light)
                if key not in ("E52", "F70", "Droom") and ph == "d_lead":
                    continue              # (d_lead is the level phrase; the candidates are heard on the two riffs, the stabs and the held note)
                a = K.render(exe, ph, params=pp, tag="wv6")[0]
                wav(d, SPEC, key.replace("*", "star"), ph, a, sh)
    save(d, "results.json", R)


if __name__ == "__main__":
    main()
