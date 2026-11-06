# SPDX-License-Identifier: GPL-3.0-only
"""README.md for each Batch 5A patch (listen/voicing/batch-05a/<NN-name>/README.md): the tables, from results.json's numbers.  Definitions: dog5-docs/voicing/README.md section 18."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import batch01a as B

BANDS = ("<60", "60-150", "150-400", "400-1.2k", "1.2k+")


def chg(k, old, new):
    """B.change plus the units the drones need (LFO depth in semitones, key tracking in %)"""
    s = B.change(k, old, new)
    if k == "LFO_FLT":
        d = lambda v: (v * v >> 7) * 97 / 256
        s += f" (+-{d(old):.1f} -> +-{d(new):.1f} st at the filter)"
    if k == "KEYTRK":
        s += f" ({old / 128 * 100:.0f} % -> {new / 128 * 100:.0f} % tracking)"
    if k == "LFO_RATE":
        hz = lambda v: 0.05 * 600 ** (v / 127)
        s = s.replace(B.unit(k, old) + " -> " + B.unit(k, new), f"{hz(old):.2f} Hz -> {hz(new):.2f} Hz")
    return s


def changes(orig, params):
    out = []
    for k in sorted(params, key=lambda k: B.K.PARAM_IDS[k]):
        if k == "VOLUME" or params[k] == orig.get(k):
            continue
        out.append(chg(k, orig[k], params[k]))
    return out


def f1(x, p=1):
    return "-" if x is None else f"{x:.{p}f}"


def sh(s):
    return " / ".join(f"{s[b]:.0f}" for b in BANDS)


def cpu(m):
    return "-" if not m.get("cost") else f"{m['cost']['idle'] + m['cost']['load']:.0f}"


def glance(spec, R, keys):
    L = ["| variant | name | VOLUME | held level (RMS) | K-RMS | first 1 s | (b) stabs | peak (all phrases) | clipped | chord voices gated | worst-case CPU (host instr/sample) |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in keys:
        m = R[k]
        L.append(f"| {k} | {m['tag']} | {m['volume']} | {f1(m['level'], 2)} | {f1(m['krms'], 2)} | {f1(m['first_s'], 1)} | {f1(m['b'], 1)} | {f1(m['peak_all'], 1)} | {m['clip']} | {m['chord_voices']} | {cpu(m)} |")
    if "A*" in R:
        m = R["A*"]
        L.append(f"| A* | original, level-matched | {m['volume']} | {f1(m['level'], 2)} | - | - | - | {f1(m['peak_all'], 1)} | - | - | - |")
    return L


def write_all(spec, R, d, orig):
    keys = [k for k in "ABCD" if k in R]
    win = spec["win"]
    L = [f"# Batch 5A, {spec['slot']:02d} {spec['name']}: variants A-D (round 1, rendered, not yet heard)", "",
         f"**Level reading:** RMS dBFS (both channels, one power average) over **+{win[0] / 1000:.0f} s .. +{win[1] / 1000:.0f} s after the note-on of the 15 s hold on the phrase `{spec['level']}`** (the held, settled state; "
         f"the note-on is at 3 s), target -18.0 +-1.5, VOLUME trimmed last; peak = the largest sample of any audition phrase (riff, stabs, held, drone, chord, taps), limit -4. "
         "`first 1 s` = RMS over the first second of the same hold. K-RMS = the same window K-weighted (informational). Worst-case CPU = idle + stress-chord load, host instructions per sample (a relative yardstick; 2900 us aim / 5800 us limit are device numbers).", ""]
    L += ["## Variants at a glance", ""] + glance(spec, R, keys) + [""]
    L += ["A* is the original's tone with VOLUME alone moved as near the reference as the knob allows (a listening aid, not a candidate)." if "A*" in R else "", ""]
    L += ["## Every change, before -> after (against A, the original)", ""]
    for k in keys[1:]:
        L += [f"**{k} ({R[k]['tag']}): {R[k]['desc']}**", ""] + [f"* {c}" for c in changes(orig, R[k]["params"])] + [f"* VOLUME {orig['VOLUME']} -> {R[k]['volume']} (level trim, last)", ""]
    {18: tables_18, 19: tables_19, 22: tables_22}[spec["slot"]](spec, R, keys, L)
    L += ["", "## Taps and the chord", "",
          "| variant | tap A1 / A2 / A3 (150 ms gate RMS, dB re the held level) | centroid of the taps (Hz) | RMS 400 ms after each key-up (dB) | 3-key chord: cards gated | chord RMS (5-10.5 s) / peak |", "|---|---|---|---|---|---|"]
    for k in keys:
        m = R[k]
        L.append(f"| {k} | {' / '.join(f1(x, 1) for x in m['tap_vs_settled'])} | {' / '.join(f'{t['cent']:.0f}' for t in m['taps'])} | {' / '.join(f1(t['tail400'], 1) for t in m['taps'])} | {m['chord_voices']} | {f1(m['chord']['rms'], 1)} / {f1(m['chord']['peak'], 1)} |")
    L += ["", "Per-phrase peaks (dBFS): " + "; ".join(f"{k}: " + ", ".join(f"{p} {v:.1f}" for p, v in R[k]["peaks"].items()) for k in keys), ""]
    open(os.path.join(d, "README.md"), "w").write("\n".join(L) + "\n")


def tables_18(spec, R, keys, L):
    L += ["", "## The wander (spectral centroid in 0.5 s windows, +2 s .. +14.5 s of the 15 s hold, 25 windows)", "",
          "| variant | A1 centroid min..max (Hz) | range | s.d. | range in semitones | A2 min..max | range | s.d. | range in st | level s.d. A1 / A2 (dB) |", "|---|---|---|---|---|---|---|---|---|---|"]
    for k in keys:
        a, b = R[k]["wander_A1"], R[k]["wander_A2"]
        L.append(f"| {k} | {a['cent_min']:.0f}..{a['cent_max']:.0f} | {a['cent_range']:.0f} | {a['cent_sd']:.0f} | {a['log2_range_st']:.1f} | {b['cent_min']:.0f}..{b['cent_max']:.0f} | {b['cent_range']:.0f} | {b['cent_sd']:.0f} | {b['log2_range_st']:.1f} | {a['rms_sd']:.1f} / {b['rms_sd']:.1f} |")
    L += ["", "## Slop, from the engine's own per-card log (A1 held 13 s): static offset / s.d. / range, cents", "", "| variant | cards | per card |", "|---|---|---|"]
    for k in keys:
        s = R[k]["slop"]
        L.append(f"| {k} | {len(s)} | " + "; ".join(f"c{c}: {v[0]:+.1f} / {v[1]:.1f} / {v[2]:+.0f}..{v[3]:+.0f}" for c, v in sorted(s.items(), key=lambda x: int(x[0]))) + " |")
    L += ["", "## Tone in windows (A1 hold): level dB / centroid Hz / MUD (150-400 share over 1.2k+ share; a 1.2k+ share near 0 makes the ratio a floor artefact) / band shares % (<60 / 60-150 / 150-400 / 400-1.2k / 1.2k+)", "",
          "| variant | window | level | centroid | MUD | bands |", "|---|---|---|---|---|---|"]
    for k in keys:
        for w, v in R[k]["windows_A1"].items():
            L.append(f"| {k} | {w} | {v['rms']:.1f} | {v['cent']:.0f} | {v['mud']:.0f} | {sh(v['shares'])} |")
    L += ["", "## Self-oscillation probe (oscillators off, noise-fed, note A2; diff 12 dB = linear, 0 = the filter sings by itself)", "", "| variant | RESO | diff dB | verdict |", "|---|---|---|---|"]
    for k in keys:
        for r in R[k]["selfosc"]:
            L.append(f"| {k} | {r['reso']:.0f} | {r['diff']:.1f} | {'self-oscillates' if r['diff'] < 3 else ('near the edge' if r['diff'] < 9 else 'linear')} |")


def tables_19(spec, R, keys, L):
    L += ["", "## Where it is heard: A0 / A1 / A2 / A3 held 6 s, window +2 .. +6 s (the strike excluded)", "",
          "| variant | note | RMS | K-RMS | peak | % under 60 Hz | 60-150 | 150-400 | 400-1.2k | 1.2k+ | % above 60 Hz | % above 150 Hz | centroid |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in keys:
        for n, r in R[k]["register"].items():
            s = r["shares"]
            L.append(f"| {k} | {n} | {r['rms']:.1f} | {r['krms']:.1f} | {r['peak']:.1f} | {s['<60']:.0f} | {s['60-150']:.0f} | {s['150-400']:.0f} | {s['400-1.2k']:.0f} | {s['1.2k+']:.0f} | {r['above60']:.0f} | {r['above150']:.0f} | {r['cent']:.0f} |")
    for nm in ("A1", "A2"):
        L += ["", f"## The 15 s hold on {nm}, per window: level dB / centroid Hz / % 150-400 / % above 400 Hz", "", "| variant | " + " | ".join(R[keys[0]]["windows_" + nm]) + " |", "|---|" + "---|" * len(R[keys[0]]["windows_" + nm])]
        for k in keys:
            L.append(f"| {k} | " + " | ".join(f"{v['rms']:.1f} / {v['cent']:.0f} / {v['shares']['150-400']:.0f} / {v['shares']['400-1.2k'] + v['shares']['1.2k+']:.0f}" for v in R[k]["windows_" + nm].values()) + " |")
    L += ["", "## Release after the 15 s hold (ms after key-up to -20 / -40 / -60 dB; the render ends 4.5 s after the key-up, None = not reached)", "", "| variant | A1 | A2 |", "|---|---|---|"]
    for k in keys:
        a, b = R[k]["release_A1"], R[k]["release_A2"]
        L.append(f"| {k} | {a['t20']} / {a['t40']} / {a['t60']} | {b['t20']} / {b['t40']} / {b['t60']} |")
    L += ["", "## Self-oscillation probe (oscillators off, noise-fed, note A2; diff 12 dB = linear, 0 = the filter sings by itself)", "", "| variant | RESO | diff dB | verdict |", "|---|---|---|---|"]
    for k in keys:
        for r in R[k]["selfosc"]:
            L.append(f"| {k} | {r['reso']:.0f} | {r['diff']:.1f} | {'self-oscillates' if r['diff'] < 3 else ('near the edge' if r['diff'] < 9 else 'linear')} |")


def tables_22(spec, R, keys, L):
    L += ["", "## The melt: A2 held, per 0.5 s window of the first 8 s", "", "Pitch = the stack's dominant fundamental by harmonic summation (400 ms windows), cents re A2 (110 Hz); centroid in Hz; level in dB.", ""]
    ts = R[keys[0]]["melt"]["t"]
    for k in keys:
        me = R[k]["melt"]
        L += [f"**{k}** ({R[k]['tag']})", "", "| t (s) | " + " | ".join(f"{t:.1f}" for t in ts) + " |", "|---|" + "---|" * len(ts),
              "| pitch (cents) | " + " | ".join(str(x) for x in me["pitch_cents"][:len(ts)]) + " |",
              "| centroid (Hz) | " + " | ".join(str(x) for x in me["cent"]) + " |", "| level (dB) | " + " | ".join(str(x) for x in me["rms"]) + " |", ""]
    L += ["| variant | final pitch (cents re A2) | formula ENV>O2 (st) | pitch to 90 % / 98 % of its fall (s) | centroid start -> final (Hz) | fall in semitones | centroid to 90 % / 98 % of its fall (s, log axis) |", "|---|---|---|---|---|---|---|"]
    for k in keys:
        me = R[k]["melt"]
        fm = "-" if me["formula_st"] is None else f"{me['formula_st']:+.2f}"
        L.append(f"| {k} | {me['pitch_final']:+.0f} | {fm} | {f1(me['pitch_t90'])} / {f1(me['pitch_t98'])} | {me['cent_start']:.0f} -> {me['cent_final']:.0f} | {me['centroid_drop_st']:.1f} | {f1(me['cent_t90'])} / {f1(me['cent_t98'])} |")
    L += ["", "## Tone in windows (A2 hold): level dB / centroid Hz / MUD / band shares %", "", "| variant | window | level | centroid | MUD | bands (<60 / 60-150 / 150-400 / 400-1.2k / 1.2k+) |", "|---|---|---|---|---|---|"]
    for k in keys:
        for w, v in R[k]["windows"].items():
            L.append(f"| {k} | {w} | {v['rms']:.1f} | {v['cent']:.0f} | {v['mud']:.0f} | {sh(v['shares'])} |")
    L += ["", "## The key-up (the note held to 15 s, then released): pitch cents and centroid Hz in 0.5 s windows after the key-up; ms to -20 / -40 / -60 dB", "",
          "| variant | pitch 0-0.4 / 0.5 / 1.0 / 1.5 / 2.0 s | centroid | -20 / -40 / -60 dB |", "|---|---|---|---|"]
    for k in keys:
        r = R[k]["release"]
        pp = lambda v: "-" if v < -1700 else str(v)                 # -1817 = the pitch tracker's floor: the tail is gone
        cc = lambda v: "-" if v == 0 else str(v)
        L.append(f"| {k} | {' / '.join(pp(x) for x in r['pitch'][:5])} | {' / '.join(cc(x) for x in r['cent'][:5])} | {r['tail']['t20']} / {r['tail']['t40']} / {r['tail']['t60']} |")
    L += ["", "## Self-oscillation probe (oscillators off, noise-fed, note A2; diff 12 dB = linear, 0 = the filter sings by itself)", "", "| variant | RESO | diff dB | verdict |", "|---|---|---|---|"]
    for k in keys:
        for r in R[k]["selfosc"]:
            L.append(f"| {k} | {r['reso']:.0f} | {r['diff']:.1f} | {'self-oscillates' if r['diff'] < 3 else ('near the edge' if r['diff'] < 9 else 'linear')} |")
