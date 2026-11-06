# SPDX-License-Identifier: GPL-3.0-only
"""Writes README.md (the tables) of a Batch 4B patch from its measured results (batch04b.py).  Definitions: dog5-docs/voicing/README.md section 17."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import batch02a_metrics as M
import batch04a_metrics as Q
import batch04a_report as R4

f, bands, changes, table, tailstr = R4.f, R4.bands, R4.changes, R4.table, R4.tailstr
SHORT_LEVEL = {"t_ghost": "ghost phrase (t)", "u_crash": "crash phrase (u: 11 hits x 300 ms gates)"}


def common(lp):
    return [
        ("VOLUME", lambda m: m["volume"]),
        (f"level, {SHORT_LEVEL[lp]} (dBFS RMS, note-on region, effects in, tails out; reference -18.0 +-1.5)", lambda m: f(m["level"], 2)),
        ("phrase (b) RMS (dBFS) / minus the level phrase (dB)", lambda m: f"{f(m['b'], 1)} / {m['b'] - m['level']:+.1f}"),
        ("peak of the own phrase (dBFS) / whole renders incl. (b) (limit -4 on the own phrase)", lambda m: f"{f(m[lp]['peak'], 1)} / {f(m['peak_all'], 1)}"),
        ("clipped samples in all renders", lambda m: m["clip"]),
        ("crest factor, own phrase (dB)", lambda m: f(m[lp]["crest"], 1)),
        ("K-weighted RMS, (b) (dBFS)", lambda m: f(m["b_stabs"]["rms_k"], 1)),
        ("note-on region: centroid (Hz)", lambda m: f(m["notes"]["cent"], 0)),
        ("note-on region: band split % <60 / 60-150 / 150-400 / 400-1.2k / 1.2k+", lambda m: bands(m["notes"]["shares"])),
        ("MUD = share(150-400) / share(1.2k+), note-on region", lambda m: f(m["notes"]["mud"], 1)),
        ("worst-case CPU (host instr/sample: idle + load)", lambda m: "-" if not m["cost"] else f"{m['cost']['idle'] + m['cost']['load']:.0f} ({m['cost']['idle']:.0f} + {m['cost']['load']:.0f})"),
    ]


def rows_13():
    t = lambda m, k: m["tape"][k]
    return [
        ("amp attack (one voice, LFO off) 10 / 50 / 90 % (ms); AA", lambda m: " / ".join(f(m["attack"]["voice"][k], 0) for k in ("t10", "t50", "t90")) + f"; {m['params']['AA']}"),
        ("tone: filter / CUTOFF (Hz at C4) / key tracking % / O1 PW % / O2 semis / O2 level", lambda m: f"{['LP12','HP12','BP12','NOTCH','LP24','SEM'][m['params']['FTYPE']]} / {440 * 2 ** ((m['params']['CUTOFF'] + 8 - 69) / 12):.0f} / {100 * m['params']['KEYTRK'] / 127:.0f} / {100 * (m['params']['O1_PW'] + .5) / 128:.0f} / {m['params']['O2_SEMI'] - 24:+d} / {m['params']['O2_LVL']}"),
        ("harmonics 3 / 5 / 7 re the fundamental, OSC 1 through the filter at rest (dB; triangle -19.1 / -28.0 / -34.2, square -9.5 / -14.0 / -16.9)", lambda m: " / ".join(f(x, 1) for x in m["tri"])),
        ("LFO PITCH (inert below 12) / LFO PWM", lambda m: f"{m['params']['LFO_PITCH']} / {m['params']['LFO_PWM']}"),
        ("tape: CHEW / WOW-FLT / HISS / DROPS", lambda m: f"{m['params']['CHEW']} / {m['params']['TP_WOWFLT']} / {m['params']['TP_HISS']} / {m['params']['TP_DROPS']}"),
        ("tape wobble, one voice A3, sends off: pitch s.d. cents / 5-95 % range cents / strongest rate Hz (0.1-8 Hz)", lambda m: f"{t(m, 'tape')['sd']:.1f} / {t(m, 'tape')['range']:.1f} / {t(m, 'tape')['rate']:.1f}"),
        ("same with CHEW 0 (the voice alone): s.d. cents", lambda m: f"{m['tape']['voice']['sd']:.1f}"),
        ("tape dropouts in the held note: dips >= 6 dB (n / deepest dB)", lambda m: f"{m['tape']['tape']['dips']} / {m['tape']['tape']['dip_db']:.1f}"),
        ("does the deck smear the top? note-on centroid Hz / % above 1.2 kHz / MUD, with the deck -> CHEW 0", lambda m: f"{m['notes']['cent']:.0f} / {m['notes']['shares']['1.2k+']:.1f} / {m['notes']['mud']:.1f} -> {m['notes_nochew']['cent']:.0f} / {m['notes_nochew']['shares']['1.2k+']:.1f} / {m['notes_nochew']['mud']:.1f}"),
        ("width, held chord: L/R correlation dry (full)", lambda m: f"{m['corr'][0]:.2f} ({m['corr_full'][0]:.2f})"),
        ("echo: ALLEY (ms) / FEEDBK / MIX / PINGPONG", lambda m: f"{m['delay_ms']:.0f} / {m['params']['DLY_FB']} / {m['params']['DLY_MIX']} / {m['params']['BBD_SPREAD']}"),
        ("first repeat of an isolated 150 ms E4: peak re the dry note's peak (dB) / at ms after the note-on", lambda m: f"{f(m['first']['dly_re_note'])} / {m['first']['t_ms']:.0f}"),
        ("spring in the same window re the note (dB); the echo's margin over it (dB)", lambda m: f"{f(m['first']['spr_re_note_same'])} ; {f(m['first']['margin'])}"),
        ("the repeats 1..6 (dB re the first)", lambda m: " ".join(f"{v:+.1f}" for _, _, v in m["train"])),
        ("the first repeat's spectrum: centroid Hz / MUD", lambda m: f"{m['solo_split']['cent']:.0f} / {m['solo_split']['mud']:.1f}"),
        ("echo under the figure's first four short notes (dB re the note)", lambda m: " / ".join(f(x, 1) for x in m["under"]["dly"][:4])),
        ("spring (DRAIN, SIZE, DAMP)", lambda m: f"{m['params']['REV_MIX']} ({100 * m['params']['REV_MIX'] / 127:.0f} %), {m['params']['REV_SIZE']}, {m['params']['REV_DAMP']}"),
        ("isolated E4, spring return re the note 0-20 / 20-100 / 100-250 ms (dB)", lambda m: " / ".join(f(r["re_dry_db"], 1) for r in m["solo_onwin"]["spr"])),
        ("after the held chord's note-off: echo return re the chord (dB) 0-100 / 100-250 / 250-500 / 500-1000 / 1000-2000 ms", lambda m: " / ".join(f(r["dly"], 1) for r in m["ret"]["ch1"])),
        ("same, spring return (dB)", lambda m: " / ".join(f(r["spr"], 1) for r in m["ret"]["ch1"])),
        ("the tail after the chord: MUD / centroid Hz / level dBFS in 0-250 / 250-750 / 750-1500 ms", lambda m: " ; ".join(f"{t['mud']:.0f} / {t['cent']:.0f} / {t['db']:.0f}" for t in m["tailsplit"])),
        ("tail after the held chord to -20 / -40 / -60 dB (ms, DC out; with the deck -> CHEW 0)", lambda m: tailstr(m["tail"]) + " -> " + tailstr(m["tail_nochew"])),
    ]


def rows_14():
    P = lambda m, k: m["params"][k]
    bd = lambda nm, tab: (lambda m: " / ".join(f(x, 0) for x in m[tab]["windows"][nm]))
    rows = [
        ("amp attack of the hit (voice alone), A1: 10 / 50 / 90 % of the peak (ms) [AA]", lambda m: " / ".join(f(m["att"]["low"][k], 1) for k in ("t10", "t50", "t90")) + f" [{P(m, 'AA')}]"),
        ("same on A2", lambda m: " / ".join(f(m["att"]["mid"][k], 1) for k in ("t10", "t50", "t90"))),
        ("shape: filter / CUTOFF byte (Hz at C4) / ENV AMT (centre 64) / FD / AD / AR / NOISE / O1 lvl / O2 lvl", lambda m: f"{['LP12','HP12','BP12','NOTCH','LP24','SEM'][P(m, 'FTYPE')]} / {P(m, 'CUTOFF')} ({440 * 2 ** ((P(m, 'CUTOFF') + 8 - 69) / 12):.0f}) / {P(m, 'FENV_AMT')} / {P(m, 'FD')} / {P(m, 'AD')} / {P(m, 'AR')} / {P(m, 'NOISE')} / {P(m, 'O1_LVL')} / {P(m, 'O2_LVL')}"),
        ("NOT A BLOW-OUT: own-phrase peak seed 1 / seed 2 (dBFS); crest seed 1 / seed 2 (dB)", lambda m: f"{f(m['u_crash']['peak'], 1)} / {f(m['seed2']['peak'], 1)}; {f(m['u_crash']['crest'], 1)} / {f(m['seed2']['crest'], 1)}"),
        ("level seed 1 / seed 2 (dBFS RMS)", lambda m: f"{f(m['level'], 2)} / {f(m['seed2']['rms'], 2)}"),
        ("share of samples within 10 % of the rail (first hit / mean of all 11 gates, %)", lambda m: f"{m['rail']:.0f} / {m['rail_all']:.0f}"),
        ("noise-to-sub level in the first 100 ms: A1 / A2 (dB; + = noise louder)", lambda m: f"{m['nvs']['low']['ratio']:+.1f} / {m['nvs']['mid']['ratio']:+.1f}"),
        ("sub: share of the sub-only A1 hit's first 150 ms <60 / 60-150 / 150-400 / 400-1.2k / 1.2k+ %", lambda m: bands(m["sub_shares"]["low"])),
        ("sub: same on A2", lambda m: bands(m["sub_shares"]["mid"])),
        ("sub's 40-150 Hz band to -20 / -40 dB after its peak (ms, A1)", lambda m: f"{f(m['sub_decay']['t20'], 0)} / {f(m['sub_decay']['t40'], 0)}"),
    ]
    for nm in ("60-150", "150-400", "400-1.2k", "1.2k-4k", "4k+"):
        rows.append((f"band {nm} Hz, A1 hit (voice alone), dB re the loudest band-window, windows 0-50 / 50-150 / 150-400 / 400-800 / 800-1500 ms", bd(nm, "bands_low")))
    for nm in ("60-150", "400-1.2k", "1.2k-4k", "4k+"):
        rows.append((f"band {nm} Hz: to -20 / -40 dB after its own peak (ms), A1 / A2", lambda m, nm=nm: " / ".join(f(m["bands_low"]["decay"][nm][k], 0) for k in ("t20", "t40")) + "; " + " / ".join(f(m["bands_mid"]["decay"][nm][k], 0) for k in ("t20", "t40"))))
    rows += [
        ("the whole voice (sends off) after the gate to -20 / -40 / -60 dB (ms, DC out)", lambda m: tailstr(m["voice_tail"])),
        ("echo: ALLEY (ms) / FEEDBK / MIX / TONE", lambda m: f"{m['delay_ms']:.0f} / {P(m, 'DLY_FB')} / {P(m, 'DLY_MIX')} / {P(m, 'DLY_TONE')}"),
        ("the first repeats 1..6 re the burst's peak (dB)", lambda m: " ".join(f"{v:+.0f}" for _, v in m["echo"][:6]) if m["echo"] else "-"),
        ("repeats above -40 dB re the burst (of 16 slots, 5.4 s)", lambda m: m["echo_n40"]),
        ("echo stays below clipping: peak of the isolated hit with echo (dBFS) / clipped samples", lambda m: f"{f(m['echo_peak'], 1)} / {m['echo_clip']}"),
        ("the sub in the repeats: MUD / centroid Hz / % 60-150 in repeat slots 1, 2, 3", lambda m: " ; ".join(f"{t['mud']:.0f} / {t['cent']:.0f} / {t['shares']['60-150']:.0f}" for t in m["echo_windows"])),
        ("echo under the figure's hits (delay return re the hit in its 300 ms gate, dB; hits 3-11)", lambda m: " ".join(f"{v:+.0f}" for v in m["under"])),
        ("the isolated hit with echo, to -20 / -40 / -60 dB (ms, DC out)", lambda m: tailstr(m["tail"])),
        ("A1 hit as rendered with echo: 4k+ band to -20 / -40 dB (ms)", lambda m: f"{f(m['bands_full']['decay']['4k+']['t20'], 0)} / {f(m['bands_full']['decay']['4k+']['t40'], 0)}"),
    ]
    return rows


ROWS = {13: rows_13, 14: rows_14}


def write_all(spec, R, d, orig):
    lp = spec["level"]
    L = [f"# Batch 4B, {spec['slot']:02d} {spec['name']}: variants and numbers", "",
         f"Chapter II (The Tidal Hexes). Round 1, **rendered, not yet heard**. Method and definitions: `dog5-docs/voicing/README.md` section 17. Level phrase: `{lp}` (own phrase, effects included, tails excluded), reference -18.0 dBFS RMS +-1.5, peak <= -4. "
         "WAVs (`<dir>_<KEY>_<ghost|crash|stabs>.wav`) are on the never-merged listen branch only.", "", "## Variants", ""]
    for key, tag, desc, ch in spec["variants"]:
        L.append(f"* **{key} {tag}**{' (RECOMMENDED, committed)' if key == spec['recommend'] else ''}: {desc}.")
    L += ["", "## Numbers", ""] + table(R, common(lp) + ROWS[spec["slot"]]())
    L += ["", "## Parameter changes, each before -> after (the original is the nearest-base patch as it stood; variant A is that patch)", ""]
    for key, tag, desc, ch in spec["variants"]:
        if key == "A":
            continue
        L += [f"### {key} {tag}", ""] + [f"* {c}" for c in changes(orig, R[key]["params"])] + [""]
        if key != "B":
            L += [f"{key} against B:", ""] + [f"* {c}" for c in changes(R["B"]["params"], R[key]["params"]) if not c.startswith("VOLUME")] + [""]
    open(os.path.join(d, "README.md"), "w").write("\n".join(L) + "\n")
