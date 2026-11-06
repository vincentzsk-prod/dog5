# SPDX-License-Identifier: GPL-3.0-only
"""Writes README.md (the tables) of a Batch 4A patch from its measured results (batch04a.py).  Definitions: dog5-docs/voicing/README.md section 15."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import batch01a as B
import batch02a as B2
import batch02a_metrics as M
import batch04a_metrics as Q

KEYS = "ABCD"


def f(x, p=1):
    return "-" if x is None or (isinstance(x, float) and (x != x or x < -150)) else f"{x:.{p}f}"


def bands(b):
    return M.fmt_bands(b)


def changes(orig, p):
    out = []
    for k, i in sorted(K.PARAM_IDS.items(), key=lambda kv: kv[1]):
        if k in orig and k in p and orig[k] != p[k]:
            out.append(B2.change(k, orig[k], p[k], p))
    return out


def table(R, rows, keys=None):
    keys = keys or [k for k in KEYS if k in R]
    L = ["| | " + " | ".join(f"{k} {R[k]['tag']}" for k in keys) + " |", "|---|" + "---|" * len(keys)]
    for lab, fn in rows:
        L.append(f"| {lab} | " + " | ".join(str(fn(R[k])) for k in keys) + " |")
    return L


def tailstr(t):
    return " / ".join(f(t[k], 0) if t.get(k) is not None else ">win" for k in ("t20", "t40", "t60"))


def common_rows(spec, lp):
    sh = SHORT_LEVEL[lp]
    return [
        ("VOLUME", lambda m: m["volume"]),
        (f"level, {sh} (dBFS RMS, note-on region, effects in, tails out; reference -18.0 +-1.5)", lambda m: f(m["level"], 2)),
        ("phrase (b) RMS (dBFS) / minus the level phrase (dB)", lambda m: f"{f(m['b'], 1)} / {m['b'] - m['level']:+.1f}"),
        ("peak, whole renders (dBFS; limit -4)", lambda m: f(m["peak_all"], 1)),
        ("crest factor, level phrase (dB)", lambda m: f(m[lp]["crest"], 1)),
        ("K-weighted RMS, (b) (dBFS)", lambda m: f(m["b_stabs"]["rms_k"], 1)),
        ("amp attack (probe, one voice, LFO off): 10 / 50 / 90 % of the plateau (ms)", lambda m: " / ".join(f(m["attack"]["voice"][k], 0) for k in ("t10", "t50", "t90"))),
        ("AA byte -> the time table's nominal (ms)", lambda m: f"{m['params']['AA']} -> {Q.aa_ms(m['params']['AA']):.0f}"),
        ("note-on region: centroid (Hz)", lambda m: f(m["notes"]["cent"], 0)),
        ("note-on region: band split % <60 / 60-150 / 150-400 / 400-1.2k / 1.2k+", lambda m: bands(m["notes"]["shares"])),
        ("MUD = share(150-400) / share(1.2k+), note-on region", lambda m: f(m["notes"]["mud"], 1)),
        ("worst-case CPU (host instr/sample: idle + load)", lambda m: "-" if not m["cost"] else f"{m['cost']['idle'] + m['cost']['load']:.0f} ({m['cost']['idle']:.0f} + {m['cost']['load']:.0f})"),
    ]


SHORT_LEVEL = {"q_organ": "organ phrase (q)", "r_tangle": "tangle phrase (r)", "s_wash": "wash phrase (s)"}


def rows_10():
    return [
        ("LFO: shape / rate (Hz, law) / pitch +-cents (law) / amp dip (dB p-p, law) / phase", lambda m: f"{['TRI','SAW','RAMP','SQUARE','S&H','RANDOM'][m['params']['LFO_SHAPE']]} / {m['lfo']['hz']:.2f} / {m['lfo']['cents']:.0f} on {['OSC1','OSC2','BOTH'][m['params']['LFO_PITCH_TO']]} / {m['lfo']['amp_db']:.1f} / {['SYNC','FREE','SPREAD'][m['params']['LFO_PHASE']]}"),
        ("pitch probe (one voice, audio): wander s.d. / 5-95 % range (cents) / rate (Hz)", lambda m: f"{m['pitch_probe']['sd']:.1f} / {m['pitch_probe']['range']:.1f} / {m['pitch_probe']['rate']:.2f}"),
        ("tremolo on the held chord, dry (audio): depth (dB, 95th-5th pct of 20 ms RMS) / strongest rate (Hz)", lambda m: f"{m['am'][0]:.1f} / {m['am'][1]:.2f}"),
        ("chorus width, held chord: L/R correlation 150-4k Hz dry (full) / side-to-mid dry (dB)", lambda m: f"{m['corr'][0]:.2f} ({m['corr_full'][0]:.2f}) / {m['corr'][1]:.1f}"),
        ("chorus beating, A3 band of the held chord, dry: rate mean (min-max) Hz / envelope depth (dB)", lambda m: f"{m['beat']['rate_mean']:.2f} ({m['beat']['rate_min']:.2f}-{m['beat']['rate_max']:.2f}) / {m['beat']['depth_db']:.1f}"),
        ("delay: ALLEY (ms) / FEEDBK / MIX / PINGPONG", lambda m: f"{m['delay_ms']:.0f} / {m['params']['DLY_FB']} / {m['params']['DLY_MIX']} / {m['params']['BBD_SPREAD']}"),
        ("first repeat of an isolated 120 ms E4: peak re the dry note's peak (dB) / peak at ms after the note-on", lambda m: f"{f(m['first']['dly_re_note'])} / {m['first']['t_ms']:.0f}"),
        ("the repeats 1..6 (dB re the first, one slot of a delay time each)", lambda m: " ".join(f"{v:+.1f}" for _, _, v in m["train"])),
        ("echo spectrum vs the note's, isolated E4: centroid note -> first repeat (Hz) / MUD of the repeat", lambda m: f"{m['solo_note_split']['cent']:.0f} -> {m['solo_split']['cent']:.0f} / {m['solo_split']['mud']:.1f}"),
        ("spring in the first repeat's window re the note (dB); delay's margin over it (dB)", lambda m: f"{f(m['first']['spr_re_note_same'])} ; {f(m['first']['margin'])}"),
        ("echo under the figure's four staccato notes (delay return re the note, dB, per note)", lambda m: " / ".join(f(x, 1) for x in m["under"]["dly"])),
        ("spring under the same notes (dB)", lambda m: " / ".join(f(x, 1) for x in m["under"]["spr"])),
        ("after the held chord's note-off: delay return re the chord (dB) in 0-100 / 100-250 / 250-500 / 500-1000 / 1000-2000 ms", lambda m: " / ".join(f(r["dly"], 1) for r in m["ret"]["ch1"])),
        ("same, spring return (dB)", lambda m: " / ".join(f(r["spr"], 1) for r in m["ret"]["ch1"])),
        ("spring (DRAIN %, SIZE, DAMP)", lambda m: f"{m['params']['REV_MIX']} ({100 * m['params']['REV_MIX'] / 127:.0f} %), {m['params']['REV_SIZE']}, {m['params']['REV_DAMP']}"),
        ("tail after the held chord (to -20 / -40 / -60 dB re its level, ms, DC out; window 2 s)", lambda m: tailstr(m["tail"])),
    ]


def rows_12():
    def pw(m):
        l = m["lfo"]
        return f"{l['pw_pct']:.0f} % +-{l['pts']:.1f} pts ({l['pw_lo']:.0f}-{l['pw_hi']:.0f} %)"

    def d(nm, b):
        return lambda m: " / ".join(f(m[nm]["bands"][x][0], 1) for x in b)

    bs = ("150-400", "400-1.2k", "1.2k-3k", "3k+")
    return [
        ("LFO: shape / rate (Hz, law) / PWM / phase", lambda m: f"{['TRI','SAW','RAMP','SQUARE','S&H','RANDOM'][m['params']['LFO_SHAPE']]} / {m['lfo']['hz']:.2f} / {pw(m)} / {['SYNC','FREE','SPREAD'][m['params']['LFO_PHASE']]}"),
        ("filter: type / CUTOFF (Hz at C4, key tracking %) / RESO", lambda m: f"{['LP12','HP12','BP12','NOTCH','LP24','SEM'][m['params']['FTYPE']]} / {440 * 2 ** ((m['params']['CUTOFF'] + 8 - 69) / 12):.0f} / {100 * m['params']['KEYTRK'] / 127:.0f} / {m['params']['RESO']}"),
        ("held A2, dry (after the filter): centroid (Hz) / % <150 / % 150-400 / % 400-1.2k / % 1.2k+", lambda m: f"{m['a2']['cent']:.0f} / {m['a2']['shares']['<60'] + m['a2']['shares']['60-150']:.0f} / {m['a2']['shares']['150-400']:.0f} / {m['a2']['shares']['400-1.2k']:.1f} / {m['a2']['shares']['1.2k+']:.1f}"),
        ("held A2, dry: PWM depth by band 150-400 / 400-1.2k / 1.2k-3k / 3k+ (dB, 95th-5th pct of 23 ms band energy)", d("pwm_a2", bs)),
        ("held A2, dry: strongest modulation rate by band (Hz)", lambda m: " / ".join(f(m["pwm_a2"]["bands"][x][1], 1) for x in bs)),
        ("held A2: level modulation dry (dB) / as rendered with the spring (dB)", lambda m: f"{m['pwm_a2']['bands']['level'][0]:.1f} / {m['pwm_a2_full']['bands']['level'][0]:.1f}"),
        ("held chord A2+E3+C4, dry: centroid (Hz) / % 1.2k+", lambda m: f"{m['chord']['cent']:.0f} / {m['chord']['shares']['1.2k+']:.1f}"),
        ("held chord, dry: PWM depth by band (dB)", d("pwm_chord", bs)),
        ("held chord: level modulation dry (dB)", lambda m: f"{m['pwm_chord']['bands']['level'][0]:.1f}"),
        ("short notes (150 ms, three of them): PWM depth, 150-400 / 400-1.2k / level (dB)", lambda m: f"{m['pwm_riff']['150-400']:.1f} / {m['pwm_riff']['400-1.2k']:.1f} / {m['pwm_riff']['level']:.1f}"),
        ("spring (DRAIN, SIZE, DAMP, PRE-DLY)", lambda m: f"{m['params']['REV_MIX']} ({100 * m['params']['REV_MIX'] / 127:.0f} %), {m['params']['REV_SIZE']}, {m['params']['REV_DAMP']}, {m['params']['REV_PRE']}"),
        ("spring return re the dry chord after its note-on, windows 0-20 / 20-100 / 100-250 ms (dB)", lambda m: " / ".join(f(r["re_dry_db"], 1) for r in m["onwin"]["chord"])),
        ("same on the held A2", lambda m: " / ".join(f(r["re_dry_db"], 1) for r in m["onwin"]["a2"])),
        ("spring tail after the chord's note-off: return re the chord's level (dB), windows 0-250 / 250-750 / 750-1500 / 1500-1800 ms", lambda m: " / ".join(f(r["spr"], 1) for r in m["ret"]["chord"])),
        ("the tail's band split, same windows: MUD (150-400 / 1.2k+) / centroid (Hz) / level (dB)", lambda m: " ; ".join(f"{t['mud']:.0f} / {t['cent']:.0f} / {t['db']:.0f}" for t in m["tailsplit"]["chord"])),
        ("tail after the chord (to -20 / -40 / -60 dB, ms, DC out)", lambda m: tailstr(m["tail"]["chord"])),
        ("tail after the held A2 / after the short-note figure (to -60 dB, ms)", lambda m: f"{f(m['tail']['a2']['t60'], 0) if m['tail']['a2']['t60'] else '>win'} / {f(m['tail_fig']['t60'], 0) if m['tail_fig']['t60'] else '>win'}"),
    ]


def rows_16():
    return [
        ("LFO: shape / rate (Hz, law) / pitch +-cents (law) / PWM +-points / phase", lambda m: f"{['TRI','SAW','RAMP','SQUARE','S&H','RANDOM'][m['params']['LFO_SHAPE']]} / {m['lfo']['hz']:.2f} / {m['lfo']['cents']:.0f} / {m['lfo']['pts']:.1f} / {['SYNC','FREE','SPREAD'][m['params']['LFO_PHASE']]}"),
        ("pitch probe (one voice, audio): wander s.d. / 5-95 % range (cents) / strongest rate (Hz)", lambda m: f"{m['pitch_probe']['sd']:.1f} / {m['pitch_probe']['range']:.1f} / {m['pitch_probe']['rate']:.2f}"),
        ("oscillators: PW O1 / O2 (%), O2 semis, FINE (cents), triangle probe H3 / H5 / H7 re H1 of OSC 1 at rest (dB; triangle -19.1 / -28.0 / -34.2, square -9.5 / -14.0 / -16.9)", lambda m: f"{100 * (m['params']['O1_PW'] + .5) / 128:.0f} / {100 * (m['params']['O2_PW'] + .5) / 128:.0f}, {m['params']['O2_SEMI'] - 24:+d}, {(m['params']['O2_FINE'] - 64) * 2 * 100 / 256:+.1f}; " + " / ".join(f(x, 1) for x in m["tri"])),
        ("filter: type / CUTOFF (Hz at C4) / key tracking %", lambda m: f"{['LP12','HP12','BP12','NOTCH','LP24','SEM'][m['params']['FTYPE']]} / {440 * 2 ** ((m['params']['CUTOFF'] + 8 - 69) / 12):.0f} / {100 * m['params']['KEYTRK'] / 127:.0f}"),
        ("width, held chord: L/R correlation 150-4k Hz dry (full) / side-to-mid dry (dB)", lambda m: f"{m['corr'][0]:.2f} ({m['corr_full'][0]:.2f}) / {m['corr'][1]:.1f}"),
        ("chorus beating, A3 band of the held chord, dry: rate mean (min-max) Hz / envelope depth (dB)", lambda m: f"{m['beat']['rate_mean']:.2f} ({m['beat']['rate_min']:.2f}-{m['beat']['rate_max']:.2f}) / {m['beat']['depth_db']:.1f}"),
        ("brightness (voice, held chord dry): centroid (Hz) / MUD / share 1.2k+ %", lambda m: f"{m['chord_dry']['cent']:.0f} / {m['chord_dry']['mud']:.1f} / {m['chord_dry']['shares']['1.2k+']:.1f}"),
        ("delay: ALLEY (ms) / FEEDBK / MIX / PINGPONG", lambda m: f"{m['delay_ms']:.0f} / {m['params']['DLY_FB']} / {m['params']['DLY_MIX']} / {m['params']['BBD_SPREAD']}"),
        ("first repeat of an isolated 400 ms E4: peak re the dry note's peak (dB) / peak at ms after the note-on", lambda m: f"{f(m['first']['dly_re_note'])} / {m['first']['t_ms']:.0f}"),
        ("spring in the same window re the note (dB); the delay's margin over the spring (dB)", lambda m: f"{f(m['first']['spr_re_note_same'])} ; {f(m['first']['margin'])}"),
        ("the repeats 1..6 (dB re the first, one slot of a delay time each)", lambda m: " ".join(f"{v:+.1f}" for _, _, v in m["train"])),
        ("the first repeat's spectrum: centroid (Hz) / MUD", lambda m: f"{m['solo_split']['cent']:.0f} / {m['solo_split']['mud']:.1f}"),
        ("echo under the figure's three 400 ms notes (dB re the note)", lambda m: " / ".join(f(x, 1) for x in m["under"]["dly"])),
        ("spring under the same notes (dB)", lambda m: " / ".join(f(x, 1) for x in m["under"]["spr"])),
        ("isolated E4, spring return re the note, 0-20 / 20-100 / 100-250 ms (dB)", lambda m: " / ".join(f(r["re_dry_db"], 1) for r in m["solo_onwin"]["spr"])),
        ("after the held chord's note-off: delay return re the chord (dB), 0-100 / 100-250 / 250-500 / 500-1000 / 1000-2000 ms", lambda m: " / ".join(f(r["dly"], 1) for r in m["ret"]["ch1"])),
        ("same, spring return (dB)", lambda m: " / ".join(f(r["spr"], 1) for r in m["ret"]["ch1"])),
        ("spring (DRAIN, SIZE, DAMP)", lambda m: f"{m['params']['REV_MIX']} ({100 * m['params']['REV_MIX'] / 127:.0f} %), {m['params']['REV_SIZE']}, {m['params']['REV_DAMP']}"),
        ("the tail after the chord: MUD / centroid (Hz) / level (dB re full scale) in 0-250 / 250-750 / 750-1500 ms", lambda m: " ; ".join(f"{t['mud']:.0f} / {t['cent']:.0f} / {t['db']:.0f}" for t in m["tailsplit"])),
        ("tail after the held chord (to -20 / -40 / -60 dB, ms, DC out)", lambda m: tailstr(m["tail"])),
    ]


ROWS = {10: rows_10, 12: rows_12, 16: rows_16}


def write_all(spec, R, d, orig):
    lp = spec["level"]
    L = [f"# Batch 4A, {spec['slot']:02d} {spec['name']}: variants and numbers", "",
         f"Chapter II (The Tidal Hexes). Round 1, **rendered, not yet heard**. Method and definitions: `dog5-docs/voicing/README.md` section 15. Level phrase: `{lp}` (own phrase, effects included, tails excluded), reference -18.0 dBFS RMS +-1.5, peak <= -4. "
         "WAVs (`<dir>_<KEY>_<organ|tangle|wash|stabs>.wav`) are on the never-merged listen branch only.", ""]
    L += ["## Variants", ""]
    for key, tag, desc, ch in spec["variants"]:
        L.append(f"* **{key} {tag}**{' (RECOMMENDED, committed)' if key == spec['recommend'] else ''}: {desc}.")
    L += ["", "## Numbers", ""] + table(R, common_rows(spec, lp) + ROWS[spec["slot"]]())
    L += ["", "## Parameter changes, each before -> after (the original is the nearest-base patch as it stood; variant A is that patch)", ""]
    for key, tag, desc, ch in spec["variants"]:
        if key == "A":
            continue
        L += [f"### {key} {tag}", ""] + [f"* {c}" for c in changes(orig, R[key]["params"])] + [""]
        if key != "B":
            L += [f"{key} against B:", ""] + [f"* {c}" for c in changes(R["B"]["params"], R[key]["params"]) if not c.startswith("VOLUME")] + [""]
    open(os.path.join(d, "README.md"), "w").write("\n".join(L) + "\n")
