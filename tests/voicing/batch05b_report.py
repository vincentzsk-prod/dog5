# SPDX-License-Identifier: GPL-3.0-only
"""Batch 5B: README.md per patch (and the parameter-change echo) from results.json.  python3 tests/voicing/batch05b_report.py"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import batch05b as X
from lib5b import *


def f(x, n=1):
    return "n/a" if x is None else f"{x:.{n}f}"


def changes(orig, p):
    return [B.change(k, orig[k], p[k]) for k in K.PARAM_IDS if k in p and k in orig and p[k] != orig[k] and k != "VOLUME"]


def cost(m):
    c = m.get("cost")
    return "n/a" if not c else f"{c['idle'] + c['load']:.0f}"


def head(slot, spec, R):
    L = [f"# {slot:02d} {spec['name']}: Batch 5B round 1 (rendered, not yet heard)", "",
         "| var | tag | VOLUME | level | K-RMS | (b) RMS | peak (all phrases) | clip | CPU worst (idle+load) |", "|---|---|---|---|---|---|---|---|---|"]
    for k in ("A", "A*", "B", "C", "D"):
        m = R[k]
        L.append(f"| {k} | {m['tag']} | {m['volume']} | {f(m.get('level'), 2)} | {f(m.get('krms'), 2)} | {f(m.get('b'), 2)} | {f(m['peak_all'], 2)} | {m.get('clip', 'n/a')} | {cost(m)} |")
    L += ["", "Level = " + ("the note-on region of phrase d_lead" if spec["level"] == "d_lead" else "RMS over +4 s .. +10 s of the held A3 C#4 E4 triad (phrase z_chord)") + ", reference -18.0 dBFS +-1.5; peak limit -4 dBFS over " + ", ".join(spec["phrases"]) + ".", ""]
    return L


def write20(R, orig):
    spec = X.SPECS[20]; L = head(20, spec, R)
    L += ["## Parameter changes against the original (A)", ""]
    for k in "BCD":
        L += [f"**{k} {R[k]['tag']}** ({R[k]['desc']})", ""] + [f"* {c}" for c in changes(orig, R[k]["params"])] + [""]
    L += ["## The hard-sync sweep on one detached A4 (900 ms, FX off, GROWL off, MONO)", "",
          "`sweep on` = ENV>O2 as set, `off` = ENV>O2 64 (no sweep). `d_hi` = energy above 1.2 kHz, on minus off (dB). `hi vs open` = that energy against the same patch with CUTOFF 127 (what the filter takes away).", "",
          "| var | window ms | centroid on | centroid off | d centroid | d_hi dB | hi vs open dB |", "|---|---|---|---|---|---|---|"]
    for k in "ABCD":
        for s in R[k]["sweep"]:
            L.append(f"| {k} | {s['w'][0]}-{s['w'][1]} | {s['cent_on']:.0f} | {s['cent_off']:.0f} | {s['d_cent']:+.0f} | {s['d_hi']:+.1f} | {s['hi_vs_open']:+.1f} |")
    L += ["", "## Detached riff against legato riff (same notes, dry): centroid Hz over 0-100 ms after each note-on", "",
          "| var | phrase | note 1 | notes 2-8 mean | notes 9-16 mean | sweep contribution (on - off), notes 2-8 mean | sweep contribution, note 1 |", "|---|---|---|---|---|---|---|"]
    for k in "ABCD":
        for nm, lab in (("det", "detached"), ("leg", "legato")):
            x = R[k][nm]; on = [c[0] for c in x["on"]]; off = [c[0] for c in x["off"]]
            L.append(f"| {k} | {lab} | {on[0]:.0f} | {np.mean(on[1:8]):.0f} | {np.mean(on[8:16]):.0f} | {np.mean(on[1:8]) - np.mean(off[1:8]):+.0f} | {on[0] - off[0]:+.0f} |")
    L += ["", "## GROWL (the drive): crest factor of the dry note-on region (phrase d_lead), GROWL 0 against as set; CPU", "",
          "CPU here = phrase (b) average + the stress chord's load (host instr/sample), the same two terms with and without GROWL.", "",
          "| var | GROWL | crest GROWL 0 | crest as set | change | RMS shift | CPU as set | CPU GROWL 0 | GROWL costs |", "|---|---|---|---|---|---|---|---|---|"]
    for k in "BCD":
        c = R[k]["crest"]; g0 = R[k].get("cost_growl0"); cc = R[k].get("cost")
        w0 = (g0["b"] + g0["load"]) if g0 else None
        w1 = (cc["b"] + cc["load"]) if cc else None
        L.append(f"| {k} | {c['growl_value']} | {c['growl0']:.1f} | {c['growl']:.1f} | {c['growl'] - c['growl0']:+.1f} dB | {c['rms_shift']:+.2f} dB | {f(w1, 0)} | {f(w0, 0)} | {f(None if w0 is None or w1 is None else w1 - w0, 0)} |")
    L += [""]
    L += [
          "## The echo (one detached A4, 300 ms)", "", "| var | ALLEY ms | FEEDBK | MIX | first repeat re note | repeats above -40 dB re the note | above -20 dB | repeat train (dB re the first) |", "|---|---|---|---|---|---|---|---|"]
    for k in "ABCD":
        e = R[k]["echo"]
        L.append(f"| {k} | {e['ms']:.0f} | {e['fb']} | {e['mix']} | {e['first']['dly_re_note']:.1f} | {e['n40']} | {e['n20']} | {' '.join(f'{v:.0f}' for _, _, v in e['train'][:10])} |")
    L += ["", "## Glide (legato step A3 -> A4, dry)", "", "| var | GLIDE | ms to within 50 cents | ms to 90 % of the octave |", "|---|---|---|---|"]
    for k in "ABCD":
        g = R[k]["glide"]; L.append(f"| {k} | {g['glide']} | {f(g['t_within50'], 0)} | {f(g['t90'], 0)} |")
    return L


def write23(R, orig):
    spec = X.SPECS[23]; L = head(23, spec, R)
    L += ["## Parameter changes against the original (A)", ""]
    for k in "BCD":
        L += [f"**{k} {R[k]['tag']}** ({R[k]['desc']})", ""] + [f"* {c}" for c in changes(orig, R[k]["params"])] + [""]
    L += ["## Tone in windows (held triad A3 C#4 E4, seconds after the note-on) and in the release", "",
          "MUD = share 150-400 Hz over share above 1.2 kHz (scale: 10 A 2.5, 12 C 12.3, medium muddy about 10-40).", "",
          "| var | window | RMS dB | centroid Hz | MUD | <150 | 150-400 | 400-1.2k | 1.2k+ |", "|---|---|---|---|---|---|---|---|---|"]
    for k in "ABCD":
        for w, x in R[k]["windows"].items():
            s = x["shares"]
            L.append(f"| {k} | {w} | {x['rms']:.1f} | {x['cent']:.0f} | {x['mud']:.2f} | {s['<60'] + s['60-150']:.0f} | {s['150-400']:.0f} | {s['400-1.2k']:.0f} | {s['1.2k+']:.0f} |")
    L += ["", "## What the tape does (against the same patch with CHEW 0)", "",
          "Pitch: the strongest harmonic of the thin pulse alone (no noise, echo or spring) tracked in 100 ms frames (A3 held 8 s). Dips: level dips over 6 dB under the running median (10 ms RMS) on a held A3 of the whole patch, 7 s. Floor: RMS 14 s and 15 s after the chord's note-on (1 s windows), after the notes are off.", "",
          "| var | CHEW | pitch s.d. cents | pitch 5-95 % cents | wow rate Hz | dips (count / deepest dB) | level s.d. dB | floor 17-18 s | floor 18-19 s | centroid 4-10 s | 1.2k+ share 4-10 s |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in "ABCD":
        m = R[k]
        for nm in ("as", "chew0"):
            t = m["tape"][nm]
            L.append(f"| {k} {nm} | {m['chew'] if nm == 'as' else 0} | {f(t['sd'])} | {f(t['p5'])} .. {f(t['p95'])} | {f(t['rate'], 2) if t['sd'] else 'n/a'} | {t['dips']['count']} / {t['dips']['deepest']:.1f} | {t['dips']['level_sd']:.2f} | {t['floor']['14']:.1f} | {t['floor']['15']:.1f} | {t['cent']:.0f} | {t['hf']:.1f} |")
    L += ["", "## The LFO and the echo (D)", "", "| var | LFO Hz | shape | AMP dip dB | FILTER excursion st | level s.d. of the dry held chord dB | echo ms / FEEDBK | echo return -40 dB after the note (ms) | repeats above -40 dB |", "|---|---|---|---|---|---|---|---|---|"]
    for k in "BCD":
        m = R[k]; l = m["lfo"]; e = m["echo"]
        L.append(f"| {k} | {l['hz']:.2f} | {l['shape']} | {l['amp_dip_db']:.1f} | {l['flt_st']:.1f} | {l['level_sd']:.2f} | " + (f"{e['ms']:.0f} / {e['fb']} | {e['t40_ms']:.0f} | {e['n40']}" if e else "none | n/a | n/a") + " |")
    L += ["", f"Release: time to -20 / -40 / -60 dB after the note-off (ms): " + "; ".join(f"{k} {m['hover']['t20']}/{m['hover']['t40']}/{m['hover']['t60']}" for k, m in R.items() if k in "ABCD") + " (None = not reached inside 5.8 s)."]
    return L


def write24(R, orig):
    spec = X.SPECS[24]; L = head(24, spec, R)
    L += ["## Parameter changes against the original (A)", ""]
    for k in "BCD":
        L += [f"**{k} {R[k]['tag']}** ({R[k]['desc']})", ""] + [f"* {c}" for c in changes(orig, R[k]["params"])] + [""]
    L += ["## Tone in windows (held triad)", "", "| var | window | RMS dB | centroid Hz | MUD | <150 | 150-400 | 400-1.2k | 1.2k+ |", "|---|---|---|---|---|---|---|---|---|"]
    for k in "ABCD":
        for w, x in R[k]["windows"].items():
            s = x["shares"]
            L.append(f"| {k} | {w} | {x['rms']:.1f} | {x['cent']:.0f} | {x['mud']:.0f} | {s['<60'] + s['60-150']:.0f} | {s['150-400']:.0f} | {s['400-1.2k']:.0f} | {s['1.2k+']:.1f} |")
    L += ["", "## The pitch LFO (one voice, VINTAGE 0, no effects, LFO PHASE SYNC, A3 held 12 s)", "", "| var | LFO PITCH | law peak cents | measured min / max cents | p5-p95 cents | measured pp semitones | rate set Hz | rate measured Hz |", "|---|---|---|---|---|---|---|---|"]
    for k in "ABCD":
        p = R[k]["pitch"]
        L.append(f"| {k} | {p['pitch_byte']} | {p['law_cents']:.0f} | {p['min']:.0f} / {p['max']:.0f} | {p['p5']:.0f} .. {p['p95']:.0f} | {p['semitones_pp']:.1f} | {p['hz']:.2f} | {p['rate']:.2f} |")
    L += ["", "## The echo (a triad stab of 120 ms with a fast attack and release, so the repeats stand apart), and the feedback tests", "",
          "| var | ALLEY ms | FEEDBK | MIX | first repeat re note | repeats above -40 dB | above -20 dB | return -40 dB after the note (ms) | direct-vs-echo pitch gap, max cents (law) |", "|---|---|---|---|---|---|---|---|---|"]
    for k in "ABCD":
        e = R[k]["echo"]
        L.append(f"| {k} | {e['ms']:.0f} | {e['fb']} | {e['mix']} | {e['first']['dly_re_note']:.1f} | {e['n40']} | {e['n20']} | {e['t40_ms']:.0f} | {R[k]['gap_cents']:.0f} |")
    L += ["", "Long hold (triad held 30 s): peak per 2 s window (dBFS) and growth (last full window minus the second window)", "", "| var | " + " | ".join(f"{s}s" for s in range(0, 30, 4)) + " | growth dB | release peaks 0/2/4/6 s |", "|---|" + "---|" * 11]
    for k in "ABCD":
        m = R[k]
        L.append(f"| {k} | " + " | ".join(f"{m['long'][i]['peak']:.1f}" for i in range(0, 15, 2)) + f" | {m['long_growth']:+.1f} | " + " / ".join(f"{x['peak']:.0f}" for x in m['long_tail'][:4]) + " |")
    L += ["", "Repeated chord (triad 300 ms every 1 s, 12 times): peak of each second (dBFS), growth = best later chord minus the first", "", "| var | " + " | ".join(str(i + 1) for i in range(12)) + " | growth dB | after: 0-2 / 2-4 / 4-6 s |", "|---|" + "---|" * 14]
    for k in "ABCD":
        m = R[k]
        L.append(f"| {k} | " + " | ".join(f"{v:.1f}" for v in m["rep"]) + f" | {m['rep_growth']:+.1f} | " + " / ".join(f"{v:.0f}" for v in m["rep_tail"][:3]) + " |")
    L += ["", "## The triangle and the octave-up copy", "", "Harmonics 3 / 5 / 7 of OSC 1 at rest against the fundamental (ideal triangle -19.1 / -28.0 / -34.2; square -9.5 / -14.0 / -16.9):", ""]
    for k in "BCD":
        L.append(f"* {k}: " + " / ".join(f"{v:.1f}" for v in R[k]["tri"]) + " dB")
    L += ["", "The octave-up copy (OSC 2, PULSE 25 %, +12 st) puts energy on the EVEN harmonics only, so those odd-harmonic readings do not move with it. Probe on B (dry held triad, 4-10 s): OSC 2 level against shares and MUD:", "",
          "| O2 LEVEL | RMS | centroid | <150 | 150-400 | 400-1.2k | 1.2k+ | MUD |", "|---|---|---|---|---|---|---|---|"]
    for r in R["B"]["o2_probe"]:
        s = r["shares"]
        L.append(f"| {r['o2_lvl']} | {r['rms']:.1f} | {r['cent']:.0f} | {s['<60'] + s['60-150']:.0f} | {s['150-400']:.0f} | {s['400-1.2k']:.0f} | {s['1.2k+']:.1f} | {r['mud']:.0f} |")
    return L


def main():
    for slot, wr in ((20, write20), (23, write23), (24, write24)):
        spec = X.SPECS[slot]; d = os.path.join(X.OUT, spec["dir"])
        R = json.load(open(os.path.join(d, "results.json")))
        orig = B.resolve(X.BASE, slot)
        open(os.path.join(d, "README.md"), "w").write("\n".join(wr(R, orig)) + "\n")
        print("wrote", d)


if __name__ == "__main__":
    main()
