# SPDX-License-Identifier: GPL-3.0-only
"""README.md for the Batch 5A round 2 slot 19 "Micro-mist" (listen/voicing/batch-05a/19-micro-mist/README.md), from results.json."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import batch01a as B
import batch05a_report as R1

SH = ("<150", "150-400", "400-1.2k", "1.2k+")


def sh(s):
    if "<60" in s:                               # a 5-band split (<60 / 60-150 / ...) folded into the four bands
        s = {"<150": s["<60"] + s["60-150"], "150-400": s["150-400"], "400-1.2k": s["400-1.2k"], "1.2k+": s["1.2k+"]}
    return " / ".join(f"{s[b]:.0f}" for b in SH)


def write_all(spec, R, d):
    keys = [k for k in "ABCD" if k in R]
    init = B.resolve(os.path.join(B.K.BUILD, "base"), 32)           # INIT's defaults ("before" for the first take: there is no original)
    L = [f"# Batch 5A round 2, 19 {spec['name']}: four fresh takes A-D (rendered, not yet heard; B committed provisionally)", "",
         "There is no original: the slot was Blackwater (dropped). **Level reading:** RMS dBFS (both channels, one power average) over **+4 s .. +10 s after the note-on of the A3 C#4 E4 chord held 10 s (phrase `z_chord`)**, target -18.0 +-1.5, VOLUME trimmed last; "
         "peak = the largest sample over the chord, the tap, the A4 single, the riff and the stabs, limit -4. K-RMS = the same window K-weighted. CPU = idle + stress-chord load, host instr/sample (target <= 2300).", "",
         "## Takes at a glance", "", "| take | name | VOLUME | held level (RMS) | K-RMS | peak | (b) stabs | CPU (host instr/sample) |", "|---|---|---|---|---|---|---|---|"]
    for k in keys:
        m = R[k]
        c = m["cost"]
        L.append(f"| {k} | {m['tag']} | {m['volume']} | {m['level']:.2f} | {m['krms']:.2f} | {m['peak_all']:.1f} | {m['b']:.1f} | {c['idle'] + c['load']:.0f} ({c['idle']:.0f} + {c['load']:.0f}) |")
    L += ["", "## Every parameter, before -> after", "", "B against INIT (the defaults), then A, C and D against B.", ""]
    for k, base, nm in (("B", init, "INIT"),) + tuple((k2, R["B"]["params"], "B") for k2 in "ACD"):
        if k not in R:
            continue
        L += [f"**{k} ({R[k]['tag']}) against {nm}: {R[k]['desc']}**", ""]
        for key in sorted(R[k]["params"], key=lambda x: B.K.PARAM_IDS[x]):
            if key == "VOLUME" or R[k]["params"][key] == base.get(key):
                continue
            L.append("* " + R1.chg(key, base[key], R[k]["params"][key]))
        L += [f"* VOLUME {base.get('VOLUME', 100)} -> {R[k]['volume']} (level trim, last)", ""]
    L += ["## Where the energy is (% of the energy: under 150 / 150-400 / 400-1.2k / over 1.2k Hz; centroid Hz; MUD = 150-400 share over 1.2k+ share)", "",
          "| take | window | level dB | centroid | bands | MUD |", "|---|---|---|---|---|---|"]
    for k in keys:
        for w, v in R[k]["windows"].items():
            L.append(f"| {k} | chord {w} (with echo + spring) | {v['rms']:.1f} | {v['cent']:.0f} | {sh(v['shares'])} | {v['mud']:.1f} |")
        for w, v in R[k]["dry_windows"].items():
            L.append(f"| {k} | chord {w} DRY (voice only) | {v['rms']:.1f} | {v['cent']:.0f} | {sh(v['shares'])} | {v['mud']:.1f} |")
        for w, v in (("A4 strike 0-1 s", R[k]["single"]["strike"]), ("A4 settled 4-6 s", R[k]["single"]["settled"])):
            L.append(f"| {k} | single {w} | {v['rms']:.1f} | {v['cent']:.0f} | {sh(v['shares'])} | {v['mud']:.1f} |")
    L += ["", "## The grain flicker (the one shared LFO)", "",
          "| take | shape / rate | PITCH depth (law, peak) | pitch probe on A4 (s.d. / 5-95 % range, 100 ms frames) | FILTER depth | filter-band swing (95th-5th pct dB) at its strongest rate | AMP dip | chord level swing (20 ms RMS, dB) |", "|---|---|---|---|---|---|---|---|"]
    names = {0: "TRI", 4: "S&H", 5: "RANDOM"}
    for k in keys:
        f = R[k]["flicker"]
        pp = f.get("pitch_probe")
        L.append(f"| {k} | {names[f['shape']]} {f['hz']:.2f} Hz | +-{f['pitch_cents']:.0f} cents | " + (f"{pp['sd']:.1f} / {pp['range']:.1f} cents" if pp else "off") +
                 f" | +-{f['filter_st']:.1f} st | {f['band_swing_db']:.1f} dB at {f['band_rate_hz']:.1f} Hz (band {f['cut_hz'] / 1.5:.0f}-{f['cut_hz'] * 1.5:.0f} Hz) | {f['amp_dip_db']:.1f} dB | {R[k]['am'][0]:.1f} dB at {R[k]['am'][1]:.1f} Hz |")
    L += ["", "## Shimmer and width", "", "| take | beating of the A3 band (dry): rate mean (min..max) Hz, envelope depth dB | L/R correlation 150-4000 Hz dry / with echo + spring | side/mid dB dry / full |", "|---|---|---|---|"]
    for k in keys:
        b = R[k]["beat"]
        L.append(f"| {k} | {b['rate_mean']:.2f} ({b['rate_min']:.2f}..{b['rate_max']:.2f}), {b['depth_db']:.1f} | {R[k]['corr_dry'][0]:.2f} / {R[k]['corr_full'][0]:.2f} | {R[k]['corr_dry'][1]:.1f} / {R[k]['corr_full'][1]:.1f} |")
    L += ["", "## Echo and spring (an isolated A4 struck 300 ms; the repeat is a whole copy of the note)", "",
          "| take | ALLEY ms | first repeat re the note (dB) | peak at (ms) | spring re the note (dB, same window) | echo over spring (dB) | repeats above -40 dB (of 14) | repeats re the first, k = 2..8 |", "|---|---|---|---|---|---|---|---|"]
    for k in keys:
        fr, tr = R[k]["first"], R[k]["train"]
        L.append(f"| {k} | {R[k]['delay_ms']:.0f} | {fr['dly_re_note']:+.1f} | {fr['t_ms']:.0f} | {fr['spr_re_note_same']:+.1f} | {fr['margin']:+.1f} | {R[k]['repeats_n40']} | " + " / ".join(f"{v:+.1f}" for _, _, v in tr[1:8]) + " |")
    L += ["", "## The hover: ms after key-up (the chord held 10 s) for the tail to fall 20 / 40 / 60 dB (None = not reached inside the 6 s render); the tail's band split in four windows", "",
          "| take | wet: -20 / -40 / -60 dB | dry voice alone | tail 0-0.5 / 0.5-1.5 / 1.5-3 / 3-5.5 s: dB, centroid Hz, bands |", "|---|---|---|---|"]
    for k in keys:
        h, hd = R[k]["hover"], R[k]["hover_dry"]
        L.append(f"| {k} | {h['t20']} / {h['t40']} / {h['t60']} | {hd['t20']} / {hd['t40']} / {hd['t60']} | " + "; ".join(f"{t['db']:.0f} dB, {t['cent']:.0f} Hz, {sh(t['shares'])}" for t in R[k]["tail_split"]) + " |")
    L += ["", "## Taps (150 ms)", "", "| take | chord tap re the held level (dB) | chord tap centroid Hz | A4 tap re the held level | hover after the chord tap -20 / -40 / -60 dB (ms) | after the A4 tap |", "|---|---|---|---|---|---|"]
    for k in keys:
        t = R[k]["taps"]
        L.append(f"| {k} | {t['chord_gate_re_held']:+.1f} | {t['chord_cent']:.0f} | {t['a4_re_held']:+.1f} | {t['chord_hover']['t20']} / {t['chord_hover']['t40']} / {t['chord_hover']['t60']} | {t['a4_hover']['t20']} / {t['a4_hover']['t40']} / {t['a4_hover']['t60']} |")
    L += ["", "## Self-oscillation probe (oscillators off, noise-fed, note A3; diff 12 dB = linear, 0 = the filter sings by itself)", "", "| take | RESO | diff dB |", "|---|---|---|"]
    for k in keys:
        for r in R[k]["selfosc"]:
            L.append(f"| {k} | {r['reso']:.0f} | {r['diff']:.1f} |")
    L += ["", "Per-phrase peaks (dBFS): " + "; ".join(f"{k}: " + ", ".join(f"{p} {v:.1f}" for p, v in R[k]["peaks"].items()) for k in keys), ""]
    open(os.path.join(d, "README.md"), "w").write("\n".join(L) + "\n")
