# SPDX-License-Identifier: GPL-3.0-only
"""Batch 6A: the per-patch READMEs (tables) from results.json.   python3 tests/voicing/b6_report.py"""
import json
import os
import re
import sys

from b6_common import *

SRC = open(os.path.join(K.ROOT, "firmware", "src", "obv_params.h")).read()
PMAX = {}
for k, mx in re.findall(r'\[P_([A-Z0-9_]+)\] = \{"[^"]*", (\d+),', SRC):
    PMAX[k] = int(mx)
ENUM = {"O1_WAVE": ("off", "saw", "pulse", "saw+pulse"), "O2_WAVE": ("off", "saw", "pulse", "saw+pulse"), "MODE": ("POLY", "DUAL", "UNISON", "MONO"), "FTYPE": ("LP12", "HP12", "BP12", "notch", "LP24", "SEM"),
        "LFO_SHAPE": ("TRI", "SAW", "RAMP", "SQUARE", "S&H", "RANDOM"), "LFO_PHASE": ("SYNC", "FREE", "SPREAD"), "SYNC": ("off", "on")}


def val(k, v):
    return ENUM[k][v] if k in ENUM and v < len(ENUM[k]) else str(v)


def changes(orig, p, skip=("VOLUME",)):
    out = []
    for k in K.PARAM_IDS:
        if k in p and k in orig and p[k] != orig[k] and k not in skip:
            mx = PMAX.get(k, 127)
            if k in ENUM:
                out.append(f"{k} {val(k, orig[k])} -> {val(k, p[k])}")
            else:
                out.append(f"{k} {orig[k]} -> {p[k]} ({100 * (p[k] - orig[k]) / mx:+.0f}%)")
    return "; ".join(out)


def f(x, n=1):
    return "n/a" if x is None else f"{x:.{n}f}"


def head(R, orig, keys, lvlname):
    L = ["| var | tag | VOLUME | level (" + lvlname + ") | peak | (b) stabs | (b) - level | CPU | what |", "|---|---|---|---|---|---|---|---|---|"]
    for k in keys:
        m = R[k]
        c = m.get("cost")
        L.append(f"| {k} | {m['tag']} | {m['volume']} | {f(m['level'], 2)} | {f(m.get('peak_all'), 1)} | {f(m.get('b'), 1)} | {f(m['b'] - m['level'], 1) if m.get('b') is not None else 'n/a'} | {('%.0f' % c['total']) if c else 'n/a'} | {m['desc']} |")
    return L


def chg(R, orig, keys):
    L = ["", "**Every change over the original (percent = of the parameter's range):**", ""]
    for k in keys:
        if k == "A":
            continue
        L.append(f"* **{k} {R[k]['tag']}:** " + changes(orig, R[k]["params"]) + f"; VOLUME {orig['VOLUME']} -> {R[k]['params']['VOLUME']}")
    return L


def r26(orig):
    R = json.load(open(os.path.join(OUT, "26-bsynca", "results.json")))
    keys = ["A", "B", "C", "D", "E52", "F70", "Droom"]
    L = ["# 26 BSyncA, Batch 6A round 1 (rendered, not yet heard)", "", "Level phrase: the note-on region of `d_lead` (the single-note lead phrase), peak limit -4 dBFS over every audition phrase; the standard stabs phrase (b) is shown for the difference (a MONO patch plays the last key of a stab only).", ""]
    L += head(R, orig, keys, "d_lead") + chg(R, orig, keys)
    L += ["", "## The drive ladder (the fat base, dry, VOLUME 100, d_lead note-on region; compression = RMS change against the same patch with no drive)", "",
          "| rung | crest dB | level shift dB | peak dBFS | CPU | rip centroid 0-50 / 50-150 / 150-400 ms (Hz) |", "|---|---|---|---|---|---|"]
    for k, nm in (("B", "filter DRIVE 60 only"), ("C", "GROWL 34"), ("D", "GROWL 44"), ("E52", "GROWL 52"), ("F70", "GROWL 70")):
        l = R[k]["ladder"]
        L.append(f"| {nm} | {l['crest']:.1f} | {l['shift']:+.2f} | {l['peak']:.1f} | {l['cost']['total']:.0f} | " + " / ".join(f"{x['cent']:.0f}" for x in l["rip"]["on"]) + " |")
    if "ladder_extra" in R:
        for x in R["ladder_extra"]:
            L.append(f"| {x['name']} | {x['crest']:.1f} | {x['shift']:+.2f} | {x['peak']:.1f} | n/a | |")
    L += ["", "## The rip (detached A3, 1 s, FX off; centroid Hz and share of energy above 1.2 kHz in the window; 'off' = ENV>O2 64, no sweep)", "", "| var | 0-50 ms | 50-150 | 150-400 | no sweep: 0-50 / 50-150 / 150-400 |", "|---|---|---|---|---|"]
    for k in keys:
        r = R[k]["rip"]
        L.append(f"| {k} | " + " | ".join(f"{x['cent']:.0f} Hz ({x['hi']:.0f} %)" for x in r["on"]) + " | " + " / ".join(f"{x['cent']:.0f}" for x in r["off"]) + " |")
    L += ["", "## Detached against legato (the aa / ab riffs, notes 2-8, first 100 ms, FX off): centroid Hz and level", "", "| var | detached with sweep | detached no sweep | legato with sweep | legato no sweep | sweep adds: detached / legato (Hz) | level detached / legato (dB) |", "|---|---|---|---|---|---|---|"]
    for k in keys:
        a, b = R[k]["riffs"]["aa_fire_detached"], R[k]["riffs"]["ab_fire_legato"]
        L.append(f"| {k} | {a['on']['cent']:.0f} | {a['off']['cent']:.0f} | {b['on']['cent']:.0f} | {b['off']['cent']:.0f} | {a['on']['cent'] - a['off']['cent']:+.0f} / {b['on']['cent'] - b['off']['cent']:+.0f} | {a['on']['rms']:.1f} / {b['on']['rms']:.1f} |")
    L += ["", "## The held A3 (4 s, FX off): centroid after the strike, the level, the stack's beat", "", "| var | centroid 0-150 / 150-400 / 400-1000 / 1000-2500 / 2500-4000 ms | RMS 0-400 / 400-1000 / 1000-2500 / 2500-4000 ms | beat rate Hz (mean, min-max), depth dB |", "|---|---|---|---|"]
    for k in keys:
        h = R[k]["held"]; bt = h["beat"]
        L.append(f"| {k} | " + " / ".join(f"{v:.0f}" for v in h["cent"].values()) + " | " + " / ".join(f"{v:.1f}" for v in h["rms"].values()) + f" | {bt['rate_mean']:.2f} ({bt['rate_min']:.2f}-{bt['rate_max']:.2f}), {bt['depth_db']:.1f} |")
    L += ["", "## Fatness (the fat base, GROWL 0, dry, VOLUME 100): voices and detune against beat, level and cost", "", "| voices | DETUNE | beat rate Hz | beat depth dB | level (d_lead) | crest | CPU |", "|---|---|---|---|---|---|---|"]
    for x in R["fatness"]:
        L.append(f"| {x['voices']}{' (MONO)' if x['voices'] == 1 else ''} | {x['det']} | {x['beat']['rate_mean']:.2f} | {x['beat']['depth_db']:.1f} | {x['level']:.1f} | {x['crest']:.1f} | {x['cost']['total']:.0f} |")
    L += ["", "## Rip depth (ENV>O2 stepped on the fat base, GROWL 0, dry): the semitones at the top of the envelope are (value - 64) x 24 / 63", "", "| ENV>O2 | st at the top | centroid 0-50 / 50-150 / 150-400 ms | 1.2k+ share |", "|---|---|---|---|"]
    for x in R["depth"]:
        L.append(f"| {x['env_o2']} | {x['st']:+.1f} | " + " / ".join(f"{y['cent']:.0f}" for y in x["rip"]["on"]) + " | " + " / ".join(f"{y['hi']:.0f} %" for y in x["rip"]["on"]) + " |")
    g = R["B"]["glide"]
    L += ["", f"## Glide: GLIDE 20 -> 50 on the fat variants: a legato octave step reaches within 50 cents in {g['t_within50']:.0f} ms (90 % of the octave in {g['t90']:.0f} ms); the original's GLIDE 20 measured {R['A']['glide']['t_within50']:.0f} ms (no glide)."]
    open(os.path.join(OUT, "26-bsynca", "README.md"), "w").write("\n".join(L) + "\n")


def r27(orig):
    R = json.load(open(os.path.join(OUT, "27-r3v3rt", "results.json")))
    keys = ["A", "B", "C", "D", "Ebite", "Fround", "Glong"]
    L = ["# 27 R3V3RT, Batch 6A round 1 (rendered, not yet heard)", "", "Level phrase: the note-on region of `a_riff` (the low chopped riff, gate 150 ms); the standard stabs phrase (b) is shown for the difference. Dry, MONO.", ""]
    L += head(R, orig, keys, "a_riff") + chg(R, orig, keys)
    for nn, nm in (("a2", "A2 (45)"), ("a1", "A1 (33)")):
        L += ["", f"## {nm}, held 1 s from silence, FX off: level re the peak (first 60 ms), the run-off, the centroid, the band shares" + (" (A1: the band columns use 2048-point frames whose Hann lobe smears the 55 Hz fundamental over 60-150 Hz; the last column, one 350 ms window, is the one to read)" if nn == "a1" else ""), "",
              "| var | level re peak at 20 / 50 / 100 / 300 / 600 ms (dB) | key-up to -20 / -40 / -60 dB (ms) | centroid 0-20 / 20-100 / 100-300 ms (Hz) | snap: peak centroid / lasts (ms) | bands 0-400 ms: <60 / 60-150 / 150-400 / 400-1.2k / 1.2k+ (%) | body 100-400 ms: same | above 60 Hz (body, %) |", "|---|---|---|---|---|---|---|---|"]
        for k in keys:
            x = R[k][nn]
            L.append(f"| {k} | " + " / ".join(f"{x['lvl'][t]:.1f}" for t in ("20", "50", "100", "300", "600")) + " | " + " / ".join(str(round(x['off'][q])) for q in ("first20", "first40", "first60")) +
                     " | " + " / ".join(f"{x['cent'][w]:.0f}" for w in ("0-20", "20-100", "100-300")) + f" | {x['snap_peak_cent']:.0f} / {x['snap_ms']} | " + " / ".join(f"{x['bands']['0-400'][q]:.0f}" for q in ("<60", "60-150", "150-400", "400-1.2k", "1.2k+")) +
                     " | " + " / ".join(f"{x['bands']['100-400'][q]:.0f}" for q in ("<60", "60-150", "150-400", "400-1.2k", "1.2k+")) + f" | {x['above60']:.0f} |")
    L += ["", "## Legato (the ag / ah bass lines, notes 2-8, FX off): detached against legato", "", "| var | first 20 ms level det / leg (dB) | 0-100 ms level det / leg | 100-300 ms level det / leg | centroid first 20 ms det / leg (Hz) | centroid 20-100 ms det / leg |", "|---|---|---|---|---|---|"]
    for k in keys:
        x = R[k]["legato"]
        L.append(f"| {k} | {x['d_first20']:.1f} / {x['l_first20']:.1f} | {x['d_p0_100']:.1f} / {x['l_p0_100']:.1f} | {x['d_p100_300']:.1f} / {x['l_p100_300']:.1f} | {x['d_c20']:.0f} / {x['l_c20']:.0f} | {x['d_c100']:.0f} / {x['l_c100']:.0f} |")
    L += ["", "## Probes on C (one control stepped; A2 body = centroid 150-400 ms, snap peak = the highest 12 ms centroid, A1 share = % of the 50-400 ms energy above 60 Hz)", "", "| control | value | A2 body Hz | A2 snap peak Hz | snap lasts ms | A1 above 60 Hz % | A1 body Hz | CPU |", "|---|---|---|---|---|---|---|---|"]
    for x in R["probes"]:
        L.append(f"| {x['param']} | {x['value']} | {x['a2_body']:.0f} | {x['a2_snap_peak']:.0f} | {x['a2_snap_ms']} | {x['a1_above60']:.0f} | {x['a1_body']:.0f} | {('%.0f' % x['cost']['total']) if x['cost'] else ''} |")
    open(os.path.join(OUT, "27-r3v3rt", "README.md"), "w").write("\n".join(L) + "\n")


def r29(orig):
    R = json.load(open(os.path.join(OUT, "29-valhalla", "results.json")))
    keys = ["A", "B", "C", "D", "W2", "W4", "W5", "E2"]
    L = ["# 29 VALHALLA, Batch 6A round 1 (rendered, not yet heard)", "", "Level phrase: RMS over +4 s .. +10 s of the held triad (`z_chord`, sends included), peak limit -4 dBFS over every audition phrase. Rung W1 (wetness L1) is measured but not rendered (listen branch weight).", ""]
    L += head(R, orig, keys, "z_chord +4..+10 s") + chg(R, orig, keys)
    L += ["", "## Bloom: the amp envelope (one voice, OSC 2 off, VINTAGE 0, FX off) and the held chord's level against its settled level (RMS 4-10 s)", "",
          "| var | amp env 10 / 50 / 90 % (ms) | chord at 0.25 / 0.5 / 1.0 s, linear, dry | same with the sends | 1.0 s with the sends (dB) | meets 60 % by 1.0 s | centroid settled / 0.25 / 0.5 / 1.0 s (Hz, dry) |", "|---|---|---|---|---|---|---|"]
    for k in keys:
        b = R[k]["bloom"]
        ok = "yes" if min(b["dry"]["rows"]["1000"]["lin"], b["full"]["rows"]["1000"]["lin"]) >= 0.6 else "NO"
        L.append(f"| {k} | {b['env']['t10']:.0f} / {b['env']['t50']:.0f} / {b['env']['t90']:.0f} | " + " / ".join(f"{b['dry']['rows'][t]['lin']:.2f}" for t in ("250", "500", "1000")) + " | " + " / ".join(f"{b['full']['rows'][t]['lin']:.2f}" for t in ("250", "500", "1000")) +
                 f" | {b['full']['rows']['1000']['db']:+.1f} | {ok} | {b['cent']['settled']:.0f} / {b['cent']['250']:.0f} / {b['cent']['500']:.0f} / {b['cent']['1000']:.0f} |")
    L += ["", "## Chorus (DUAL pair, SPREAD 127, TRI LFO PHASE SPREAD; held chord 4-10 s, dry, 150-4000 Hz; one render each: differences of about 0.1 are not a trend)", "",
          "| var | LFO Hz | depth cents | L/R corr as built | LFO PITCH 0 | POLY (no chorus) | beat depth dB with / without the pitch LFO (A3 band) | CPU as built | CPU as POLY, no pitch LFO |", "|---|---|---|---|---|---|---|---|---|"]
    for k in keys:
        c = R[k]["chorus"]
        L.append(f"| {k} | {c['rate_hz']:.2f} | {c['cents']:.1f} | {c['with']['corr']:.2f} | {c['without']['corr']:.2f} | {c['poly_without']['corr']:.2f} | {c['with']['beat']['depth_db']:.1f} / {c['without']['beat']['depth_db']:.1f} | {('%.0f' % R[k]['cost']['total']) if R[k].get('cost') else ''} | {('%.0f' % R[k]['cost_nochorus']) if R[k].get('cost_nochorus') else ''} |")
    L += ["", "## Drift (the engine's own vlog, DUAL, one held note, cents: static offset / s.d. / range, per card)", ""]
    for k in ("A", "B", "C"):
        d = R[k]["drift"]
        L.append(f"* {k} (VINTAGE {R[k]['params']['VINTAGE']}): " + "; ".join(f"card {c}: {v[0]:+.1f} / {v[1]:.1f} / {v[2]:+.0f}..{v[3]:+.0f}" for c, v in sorted(d.items())))
    L += ["", "## A fourth note on POLY 6 DUAL (A3 C#4 E4 held, G#4 added at +3 s; each note's fundamental band +-40 cents, dB, before -> 1.2 s after the fourth note-on)", ""]
    for k in ("B", "C"):
        s = R[k]["steal"]
        L.append(f"* {k}: " + "; ".join(f"MIDI {n}: {v['before']:.1f} -> {v['after']:.1f}" for n, v in s.items()))
    L += ["", "## Erosion (dry, held chord; band level in dB in one-second windows, change from the 1 s window to the 10 s window = 'drop'; centroid Hz)", "",
          "| var | 150-400 Hz drop 1->10 s | 400-1.2k drop | 1.2k+ drop | 150-400 / 400-1.2k peak-to-peak 1.5-9 s | RMS 1 / 3 / 6 / 10 s | centroid 1 / 3 / 6 / 10 s |", "|---|---|---|---|---|---|---|"]
    for k in keys:
        e = R[k]["erosion"]; b = e["bands"]
        L.append(f"| {k} | {b['1']['150-400'] - b['10']['150-400']:+.1f} | {b['1']['400-1.2k'] - b['10']['400-1.2k']:+.1f} | {b['1']['1.2k+'] - b['10']['1.2k+']:+.1f} | {b['150-400_pp']:.1f} / {b['400-1.2k_pp']:.1f} | " + " / ".join(f"{e['rms'][t]:.1f}" for t in ('1', '3', '6', '10')) + " | " + " / ".join(f"{e['cent'][t]:.0f}" for t in ('1', '3', '6', '10')) + " |")
    L += ["", "## The wetness ladder and the sends (full patch; return windows after the 10 s chord's key-up in dB re the chord's own level over the 400 ms before; first repeat of an isolated E4 re the note, delay's margin over the spring)", "",
          "| var | echo ms | FEEDBK | MIX | DRAIN | SIZE | echo return 0-250 / 250-750 / 750-1500 ms | spring return same | sum same | first repeat dB | margin over spring dB | tail to -20 / -40 / -60 dB (ms) | tail MUD 0-250 / 250-750 / 750-1500 (level dB) |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in keys[1:]:
        w = R[k]["wet"]
        L.append(f"| {k} | {w['echo_ms']:.0f} | {w['fb']} | {w['mix']} | {w['drain']} | {w['size']} | " + " / ".join(f"{x['dly']:.1f}" for x in w["ret"]) + " | " + " / ".join(f"{x['spr']:.1f}" for x in w["ret"]) + " | " + " / ".join(f"{x['all']:.1f}" for x in w["ret"]) +
                 f" | {w['first']['dly_re_note']:.1f} | {w['first']['margin']:.1f} | {w['tail_t']['first20']:.0f} / {w['tail_t']['first40']:.0f} / {w['tail_t']['first60']:.0f} | " + " / ".join(f"{x['mud']:.0f} ({x['db']:.0f})" for x in w["tail"]) + " |")
    L += ["", "Reference (16 D): first repeat -8.6 dB, 7.7 dB over the spring.", "", "## The hump (white noise through the settled filter, held triad 4-10 s, dry; 1/6-octave smoothing)", "", "| var | peak Hz (300-3000) | -3 dB width Hz (from-to) | height over the same filter at RESO 0 (dB) | peak over the 150-3000 Hz mean (dB) | centroid of the held chord (Hz) |", "|---|---|---|---|---|---|"]
    for k in keys:
        h = R[k]["hump"]
        L.append(f"| {k} | {h['peak_hz']:.0f} | {h['w3_hz']:.0f} ({h['w3_lo']:.0f}-{h['w3_hi']:.0f}) | {h['reso_gain_db']:+.1f} | {h['over_mean_db']:+.1f} | {h['chord_cent']:.0f} |")
    open(os.path.join(OUT, "29-valhalla", "README.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    for slot, fn in ((26, r26), (27, r27), (29, r29)):
        fn(B.resolve(BASE, slot))
