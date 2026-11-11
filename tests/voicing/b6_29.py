# SPDX-License-Identifier: GPL-3.0-only
"""Batch 6A, 29 VALHALLA: a medium-attack, eroding, chorused chordal wash (DUAL pair chorus, POLY 6), no tape, almost no slop.  Probes and the driver.
  python3 tests/voicing/b6_29.py [--no-cost] [--no-wav] [--quick]      -> listen/voicing/batch-06a/29-valhalla/ (results.json; WAVs only on the listen branch)"""
import sys

from b6_common import *

SPEC = dict(slot=29, dir="29-valhalla", name="VALHALLA", cname="VALHALLA", level="z_chord", phrases=["z_chord", "z_tap", "b_stabs", "w_chord_mid"])
ON, OFF = 3000, 13000          # z_chord: the triad A3 C#4 E4 from 3000 ms to 13000 ms, the script runs to 19000
TRIAD = (57, 61, 64)
ECHO_PROBE = dict(note=64, len=400)     # as 16: an isolated E4, 400 ms
WINS_TAIL = ((0, 250), (250, 750), (750, 1500))
NOWET = {"DLY_MIX": 0, "REV_MIX": 0}


def bloom(exe, p):
    """the amp envelope (10 / 50 / 90 % of the plateau, one voice, OSC 2 off, VINTAGE 0: Q.attack_long) and the HELD CHORD's level at 0.25 / 0.5 / 1.0 s after the key-down as a fraction of the
    settled level (RMS 4..10 s after the key-down, one reading): dry (voices only) and with the sends, linear amplitude and dB; the centroid at 0.25 / 0.5 / 1.0 s against the settled one (dry)"""
    out = {"env": Q.attack_long(exe, p, note=57, hold_ms=1800)}
    for nm, ov in (("dry", NOWET), ("full", {})):
        a, _ = K.render(exe, "z_chord", params={**p, **ov}, tag="bl6")
        settled = M.rms_db(a, ON + 4000, ON + 10000)
        rows = {}
        for t in (250, 500, 1000):
            r = M.rms_db(a, ON + t - 25, ON + t + 25)
            rows[str(t)] = {"db": r - settled, "lin": float(10 ** ((r - settled) / 20))}
        out[nm] = {"settled": settled, "rows": rows}
        if nm == "dry":
            sc = M.centroid(a, ON + 4000, ON + 10000, nfft=2048)
            out["cent"] = {"settled": sc, **{str(t): M.centroid(a, ON + t - 100, ON + t + 100, nfft=2048) for t in (250, 500, 1000)}}
    return out


def chorus(exe, p):
    """the chorus: LFO rate (Hz) and depth (cents, the law), the L/R correlation (150-4000 Hz, held chord 4-10 s, dry) with the LFO pitch as built and with LFO PITCH 0 (one render each: the oscillator start phases are random,
    differences of about 0.1 are not a trend), the beat of the A3 band (beat_metrics), and the cost with the chorus (as built) and as POLY with no LFO pitch"""
    out = {"rate_hz": lfo_hz(p["LFO_RATE"]), "cents": Q.pitch_cents(p["LFO_PITCH"])}
    for nm, ov in (("with", {}), ("without", {"LFO_PITCH": 0}), ("poly_without", {"LFO_PITCH": 0, "MODE": 0})):
        a, _ = K.render(exe, "z_chord", params={**p, **NOWET, **ov}, tag="ch6")
        c, sm = Q.chan_corr(a, ON + 4000, ON + 10000)
        out[nm] = {"corr": c, "side_mid_db": sm, "beat": K.beat_metrics(a, 220.0, ON + 1500, ON + 10000)}
    return out


def steal(exe, p):
    """a fourth note on POLY 6 DUAL (the chord A3 C#4 E4 held, G#4 added at +3 s): the level of each note's fundamental band (+-40 cents, mono sum, 400 ms Hann) just before and 1.2 s after the fourth note-on"""
    q = {**p, **NOWET}
    ev = [f"3000 midi 0x90 {n} 100" for n in TRIAD] + ["6000 midi 0x90 68 100"] + [f"9000 midi 0x80 {n} 0" for n in (*TRIAD, 68)]
    a = N._run(exe, "st6", N._probe_script(q, ev, 11000))
    x = a.mean(1)

    def band(f0, t0, t1):
        seg = x[int(t0 * FS / 1000):int(t1 * FS / 1000)]
        X = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), 1 << 16)) ** 2
        f = np.fft.rfftfreq(1 << 16, 1 / FS)
        s = (f > f0 * 2 ** (-40 / 1200)) & (f < f0 * 2 ** (40 / 1200))
        return float(10 * np.log10(max(X[s].sum(), 1e-9)))
    out = {}
    for n in (*TRIAD, 68):
        f0 = 440 * 2 ** ((n - 69) / 12)
        out[n] = {"before": band(f0, 5600, 6000), "after": band(f0, 7000, 7400)}
    return out


def erosion(exe, p):
    """the held chord's erosion, dry: the 150-400 and 400-1.2k band levels (dB, one-second windows centred at 1 / 3 / 6 s and 9-10 s) re the 1 s window, and the centroid in the same windows"""
    a, _ = K.render(exe, "z_chord", params={**p, **NOWET}, tag="er6")
    wins = {"1": (500, 1500), "3": (2500, 3500), "6": (5500, 6500), "10": (9000, 10000)}
    out = {"bands": {}, "cent": {}, "rms": {}}
    for k, (x, y) in wins.items():
        out["bands"][k] = {b: R5.band_db(a, ON + x, ON + y, lo, hi, nfft=4096) for b, (lo, hi) in (("150-400", (150, 400)), ("400-1.2k", (400, 1200)), ("1.2k+", (1200, 22000)))}
        out["cent"][k] = M.centroid(a, ON + x, ON + y, nfft=4096)
        out["rms"][k] = M.rms_db(a, ON + x, ON + y)
    # the movement inside the 10 s: peak-to-peak of the band level in 1 s frames from 1 s on, and the strongest component of that series
    for b, (lo, hi) in (("150-400", (150, 400)), ("400-1.2k", (400, 1200))):
        ser = [R5.band_db(a, ON + s, ON + s + 1000, lo, hi, nfft=4096) for s in range(1000, 9000, 500)]
        out["bands"][b + "_pp"] = float(max(ser) - min(ser))
        out["bands"][b + "_drop"] = float(ser[0] - ser[-1])
    return out


def wet(exe, p):
    """the sends: return windows after the 10 s chord's key-up (delay's / spring's own return and the sum, dB re the chord's level over the 400 ms before; 0-250 / 250-750 / 750-1500 ms), the first repeat of an isolated E4 (re
    the note, and the delay's margin over the spring), the tail time of the whole patch to -20 / -40 / -60 dB after the key-up, MUD ratio and level in the tail windows"""
    out = {"echo_ms": alley_ms(p["ALLEY"]) if p["ALLEY"] else None, "fb": p["DLY_FB"], "mix": p["DLY_MIX"], "drain": p["REV_MIX"], "size": p["REV_SIZE"], "damp": p["REV_DAMP"], "pre": p["REV_PRE"]}
    r = Q.fx_set(exe, "z_chord", p, "w6")
    out["ret"] = Q.return_windows(r, OFF, 400, WINS_TAIL)
    dc = r["full"][int((OFF + 4500) * FS / 1000):int((OFF + 5500) * FS / 1000)].mean(0)
    out["tail"] = Q.tail_after(r["full"], OFF, wins=WINS_TAIL, dc=dc)
    out["held_mud"] = {f"{x}-{y}s": Q.window_split(r["full"], ON + x * 1000, ON + y * 1000) for x, y in ((1, 4), (4, 10))}
    rel = K.release_metrics(r["full"], OFF, hop_ms=5.0, pre_ms=400, win_ms=5500)
    out["tail_t"] = {k: rel[k] for k in ("first20", "first40", "first60")}
    if p["DLY_MIX"] == 0:           # the original has no echo: nothing to read
        out["first"] = None
        return out
    T = alley_ms(p["ALLEY"])
    S, on, off = Q.solo_set(exe, p, [ECHO_PROBE["note"]], ECHO_PROBE["len"], tail_ms=4000, tag="s6")
    out["first"] = Q.first_repeat(S, on, off, T)
    return out


def hump(exe, p):
    """the filter's hump, read with white noise in place of the oscillators (a held chord's partials are lines, not a response): OSC 1 / OSC 2 off, NOISE 127, everything else as built (filter envelope at its settled state, 4-10 s
    of the held triad, dry), the long-term spectrum smoothed over 1/6 octave: the strongest point between 300 and 3000 Hz, its -3 dB width, its height over the same noise with RESO 0 (the resonance's own gain) and over the
    patch's own mean level 150-3000 Hz; plus the centroid of the held chord itself (oscillators as built)"""
    def spec(q):
        q = {**q, "O1_WAVE": 0, "O1_LVL": 0, "O2_WAVE": 0, "O2_LVL": 0, "NOISE": 127, **NOWET, "LFO_PITCH": 0, "LFO_PWM": 0}
        a, _ = K.render(exe, "z_chord", params=q, tag="hp6")
        x = a.mean(1)[int((ON + 4000) * FS / 1000):int((ON + 10000) * FS / 1000)]
        NF = 1 << 17
        X = np.abs(np.fft.rfft(x * np.hanning(len(x)), NF)) ** 2
        f = np.fft.rfftfreq(NF, 1 / FS)
        fc = 2 ** np.arange(np.log2(100), np.log2(8000), 1 / 24)
        return fc, np.array([10 * np.log10(X[(f >= c * 2 ** (-1 / 12)) & (f < c * 2 ** (1 / 12))].mean() + 1e-9) for c in fc])
    fc, S = spec(p)
    fc0, S0 = spec({**p, "RESO": 0})
    sel = (fc >= 300) & (fc <= 3000)
    i = int(np.nonzero(sel)[0][np.argmax(S[sel])])
    pk = S[i]
    lo = i
    while lo > 0 and S[lo] > pk - 3:
        lo -= 1
    hi = i
    while hi < len(S) - 1 and S[hi] > pk - 3:
        hi += 1
    a, _ = K.render(exe, "z_chord", params={**p, **NOWET}, tag="hp6c")
    return {"peak_hz": float(fc[i]), "w3_lo": float(fc[lo]), "w3_hi": float(fc[hi]), "w3_hz": float(fc[hi] - fc[lo]), "reso_gain_db": float(S[i] - S0[i]),
            "over_mean_db": float(pk - S[(fc >= 150) & (fc <= 3000)].mean()), "chord_cent": M.centroid(a, ON + 4000, ON + 10000, nfft=4096)}


def drift(exe, p):
    """the engine's own log of each voice card's pitch wander (the host-only vlog) for the patch's VINTAGE: DUAL, one note held 13 s: static offset / s.d. / range, cents"""
    lines = [f"{K.T_SELECT} midi 0xC0 {K.INIT_PROGRAM} 0", f"{K.T_PARAMS} param {K.PARAM_IDS['VINTAGE']} {p['VINTAGE']}", f"{K.T_PARAMS} param {K.PARAM_IDS['MODE']} 1",
             "3000 midi 0x90 57 100", "4000 vlog 1", "17000 vlog 0", "17100 midi 0x80 57 0", "18000 end"]
    sp = os.path.join(K.BUILD, "slop6.txt")
    open(sp, "w").write("\n".join(lines) + "\n")
    import subprocess
    r = subprocess.run([exe, os.path.join(K.BUILD, "slop6"), sp], cwd=K.ROOT, capture_output=True, text=True, errors="replace").stdout
    return K.vlog_parse(r)


def measure(exe, p, quick=False):
    m = {"bloom": bloom(exe, p), "chorus": chorus(exe, p), "erosion": erosion(exe, p), "hump": hump(exe, p), "drift": drift(exe, p)}
    if not quick:
        m["steal"] = steal(exe, p)
        m["wet"] = wet(exe, p)
    return m


# ---- the variant tables (changes over the original) -----------------------------------------------------------------------------------------------------------------------------------
# shared by B, C, D: the chorus (a DUAL pair, POLY 6, SPREAD 127, TRI 0.72 Hz on pitch +-18.8 cents in PHASE SPREAD, as 10 B), PWM from the same LFO on both oscillators, OSC 2 +4.7 cents, VINTAGE 8, no tape, a slow release
CORE = dict(MODE=1, POLY_N=6, UNI_DET=20, O2_FINE=70, VINTAGE=8, SPREAD=127, AR=100, AS=127, FR=90, LFO_SHAPE=0, LFO_RATE=53, LFO_PHASE=2, LFO_PITCH=16, LFO_PITCH_TO=2, LFO_PWM_TO=2, CHEW=0, GROWL=0)
PLAIN = dict(CORE, O1_WAVE=2, O1_PW=44, O1_LVL=110, O2_WAVE=2, O2_PW=40, O2_LVL=100, O2_SEMI=24, FTYPE=0, CUTOFF=78, RESO=8, KEYTRK=100, FENV_AMT=100, FA=60, FD=118, FS=20, AA=96, LFO_PWM=80, DRIVE=0)
CHOIR = dict(CORE, O1_WAVE=2, O1_PW=38, O1_LVL=100, O2_WAVE=2, O2_PW=44, O2_LVL=45, O2_SEMI=36, FTYPE=0, CUTOFF=78, RESO=75, KEYTRK=0, FENV_AMT=70, FA=60, FD=118, FS=0, AA=100, LFO_PWM=60, DRIVE=0)
# the sends: an ALLEY of 257 ms and the spring; five rungs of wetness (L3 = the middle one)
LAD = {"L1": dict(ALLEY=96, DLY_FB=45, DLY_MIX=55, REV_MIX=20, REV_SIZE=70),
       "L2": dict(ALLEY=96, DLY_FB=55, DLY_MIX=70, REV_MIX=30, REV_SIZE=75),
       "L3": dict(ALLEY=96, DLY_FB=65, DLY_MIX=85, REV_MIX=35, REV_SIZE=80),
       "L4": dict(ALLEY=96, DLY_FB=78, DLY_MIX=105, REV_MIX=45, REV_SIZE=90),
       "L5": dict(ALLEY=96, DLY_FB=92, DLY_MIX=120, REV_MIX=65, REV_SIZE=100)}
SEND = dict(DLY_TONE=70, REV_DAMP=60, REV_PRE=20)
V = {
    "B": ("plain", "a plain, brighter PWM wash: two pulses (PW 34 / 31 %) through LP12 (KEY TRK 100), mild erosion, wetness L3", {**PLAIN, **SEND, **LAD["L3"]}),
    "C": ("hollow", "the soft, hollow colour: a narrower pulse (30 %), an octave-up pulse copy at LEVEL 45, a resonant LP12 at a fixed CUTOFF 78 / RESO 75 (KEY TRK 0), a lighter spring (MIX 95, DRAIN 25)", {**CHOIR, **SEND, **LAD["L3"], "DLY_MIX": 95, "REV_MIX": 25}),
    "D": ("hollow-wet", "C's colour, wetter (echo FEEDBK 82, MIX 110, DRAIN 38, SIZE 90) and a deeper filter bloom (ENV AMT 100)", {**CHOIR, "FENV_AMT": 100, **SEND, **LAD["L4"], "DLY_FB": 82, "DLY_MIX": 110, "REV_MIX": 38}),
}
CAL = {      # calibrations on B (not candidates): the wetness ladder and a deeper erosion
    "W1": ("wet-L1", "B on wetness rung L1", {**PLAIN, **SEND, **LAD["L1"]}),
    "W2": ("wet-L2", "B on wetness rung L2", {**PLAIN, **SEND, **LAD["L2"]}),
    "W4": ("wet-L4", "B on wetness rung L4", {**PLAIN, **SEND, **LAD["L4"]}),
    "W5": ("wet-L5", "B on wetness rung L5", {**PLAIN, **SEND, **LAD["L5"]}),
    "E2": ("erode-deep", "B with a deeper erosion (CUTOFF 70, ENV AMT 90, FILTER SUSTAIN 0)", {**PLAIN, "CUTOFF": 70, "FENV_AMT": 90, "FS": 0, **SEND, **LAD["L3"]}),
}


def main():
    argv = sys.argv[1:]
    no_cost, no_wav, quick = "--no-cost" in argv, "--no-wav" in argv, "--quick" in argv
    only = argv[argv.index("--only") + 1].split(",") if "--only" in argv else None
    exe = K.build_host()
    cg = None if (no_cost or quick) else K.callgrind_exe()
    orig = B.resolve(BASE, 29)
    d = os.path.join(OUT, SPEC["dir"])
    R, WS = {}, {}
    allv = [("A", "original", "the original through the base program path", {})] + [(k, v[0], v[1], v[2]) for k, v in V.items()] + [(k, v[0], v[1], v[2]) for k, v in CAL.items()]
    for key, tag, desc, ch in allv:
        if only and key not in only:
            continue
        p = dict(orig) if key == "A" else {**orig, **ch}
        if key != "A":
            p = fit(exe, SPEC, p)
        m, W = common(exe, cg, SPEC, key, p, no_cost)
        m.update(measure(exe, p, quick))
        if cg and key in ("B", "C", "D"):
            m["cost_nochorus"] = cpu(cg, {**p, "MODE": 0, "LFO_PITCH": 0}, "29n")["total"]     # the same patch as POLY, no LFO pitch
        m["volume"], m["params"], m["tag"], m["desc"] = p["VOLUME"], p, tag, desc
        R[key], WS[key] = m, W
        c = m["cost"]
        b = m["bloom"]
        print(f"29{key} {tag:10s} VOL {p['VOLUME']:3d} lvl {m['level']:6.2f} b {m['b']:6.2f} pk {m['peak_all']:6.2f}" + (f" cost {c['total']:.0f}" if c else "") +
              f" | t10/50/90 {b['env']['t10']:.0f}/{b['env']['t50']:.0f}/{b['env']['t90']:.0f} 1s {b['full']['rows']['1000']['lin']:.2f}", flush=True)
    if not only:
        pa = fit(exe, SPEC, dict(orig)); ra = trim(exe, SPEC, dict(orig))[1]
        R["A*"] = {"volume": pa["VOLUME"], "level": ra, "params": pa, "tag": "original-matched", "desc": "the original's tone with VOLUME alone moved onto the reference (a listening aid)"}
    if not no_wav and not quick:
        for key in [k for k in R if k in ("A*", "B", "C", "D") or k in CAL]:
            pp = R[key]["params"]
            for ph, sh in (("z_chord", "held-chord"), ("b_stabs", "stabs"), ("z_tap", "tap")):
                if key in CAL and ph != "z_chord":
                    continue
                if key == "W1":
                    continue              # (rung L1 is measured, not rendered: the listen branch stays light)
                wav(d, SPEC, key.replace("*", "star"), ph, K.render(exe, ph, params=pp, tag="wv6")[0], sh)
    save(d, "results.json" if not only else "results_partial.json", R)


if __name__ == "__main__":
    main()
