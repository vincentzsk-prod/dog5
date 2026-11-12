# SPDX-License-Identifier: GPL-3.0-only
"""Batch 6B2: the per-slot README for 28 (round 2, the top grit) from base.json / iso.json / alias.json / cand.json.   python3 tests/voicing/b6d_report.py"""
import json
import os

import b6_report as R6
from b6d_28 import OUT2, BASE, V, B, GRIT_FIX

NOTES = ("A3", "A4", "A6")
WN = ("0-20", "20-100", "100-400", "1000-2000")
WL = {"0-20": "0-20 ms", "20-100": "20-100 ms", "100-400": "100-400 ms", "1000-2000": "1-2 s"}
SIX = {"B": (298, 612, 1034, 2069), "C": (648, 1218, 2147, 4062), "D": (900, 1895, 3096, 5979)}


def f(v, n=1):
    return "n/a" if v is None else f"{v:.{n}f}"


def db(a, b):
    return 10 * __import__("math").log10(max(b, 1e-6) / max(a, 1e-6))


def lad(L):
    return " / ".join("-" if L[k] is None else f"{L[k]['db']:+.1f}" for k in ("0.5", "1.0", "1.2", "1.5", "2.0"))


def grit_rows(R, keys, notes=NOTES):
    L = ["| var | note | window | >4 kHz % | 2-8 kHz % | flatness 2-10 kHz dB | off-ladder partials within -30 / -20 dB | RMS dB |", "|---|---|---|---|---|---|---|---|"]
    for k in keys:
        for nm in notes:
            for w in WN:
                g = R[k]["grit"][nm][w]
                nl = g.get("nonlad")
                L.append(f"| {k} | {nm} | {WL[w]} | {g['over4k']:.2f} | {g['s2_8k']:.1f} | {g['flat']:.1f} | " + ("-" if not nl else f"{nl['count']} / {nl['count20']}") + f" | {g['rms']:.1f} |")
    return L


def sat_rows(R, keys):
    L = ["| var | note | crest, dry, strike 0-400 ms / the note | dry peak dBFS | filter state saturating, % of voice samples (whole note / first 100 ms) | mix clamp (hard) | output tanh: samples input over 6000 (0.1 dB) / 12000 / 20000, max input | samples at full scale |", "|---|---|---|---|---|---|---|---|"]
    for k in keys:
        for nm in NOTES:
            c, s = R[k]["crest"][nm], R[k]["sat"][nm]
            L.append(f"| {k} | {nm} | {c['strike_0_400']:.1f} / {c['note_0_3000']:.1f} dB | {c['peak_dry']:.1f} | {s['svf_sat_pct']:.2f} / {s['strike100']['svf_sat_pct']:.2f} | {s['mix_clamp']} | {s['out_6k']} / {s['out_12k']} / {s['out_20k']}, {s['out_max']} | {R[k]['clip']} (all phrases) |")
    return L


def r28():
    base = json.load(open(os.path.join(OUT2, "base.json")))
    iso = json.load(open(os.path.join(OUT2, "iso.json")))
    ali = json.load(open(os.path.join(OUT2, "alias.json")))
    cd = json.load(open(os.path.join(OUT2, "cand.json")))
    orig = B.resolve(BASE, 28)
    L = ["# 28 Bell Tolls, Batch 6B2 round 2: the top grit (rendered, not yet heard)", "",
         "**Brief change, logged:** a clean base with no top grit; Vincent's premise ('it is coming from the CHEW and GROWL') was **not in the patch** (below). Round 1 (Batch 6B) stays as the record: variants B / C / D = 2.1 / 4.1 / 6.0 s rings, the shimmer on C and D.", "",
         "## The correction: there is no CHEW, GROWL or DRIVE in any 6B variant", "",
         "* The committed array of 6B round 1 (`ad8345c`, `PF_BELL_XMOD`) carries **no** `P_CHEW`, `P_GROWL` or `P_DRIVE` entry (0 of its 27 entries; the original array neither), and the resolved parameters of every variant read GROWL 0, CHEW 0, DRIVE 0 (`base.json`, `params`). The variants differ in the voice (X-MOD, levels, filter), the envelopes, the shimmer, the echo and the spring only.",
         "* The CPU says the same: base variant C reads " + f"{cd['addons']['base']:.0f}" + " host instr/sample; CHEW 45 adds " + f"{cd['addons']['CHEW 45'] - cd['addons']['base']:+.0f}" + " and GROWL 44 " + f"{cd['addons']['GROWL 44'] - cd['addons']['base']:+.0f}" + " (the 6B figures: +784 and +595): none of that is in the base.",
         "* So removing CHEW and halving GROWL would change nothing. The grit is somewhere else; this round finds where.", ""]
    L += ["## Verdict in short (numbers below; Vincent's ear decides)", "",
          "* **Where the grit comes from: the FM.** X-MOD 64 with OSC 2 at the inharmonic tierce ratio (+15 st = 2.378x) makes inharmonic sidebands: 13-18 spectral peaks within -30 dB that are not on the key's harmonic series or the tierce (the original array's +19 st = 3.0x is a harmonic ratio: 0-6) and a noise-like floor in 2-10 kHz (flatness at A4, 100-400 ms: C -17.2 dB, the original -27.2, X-MOD 0 -35.5, OSC 1 alone -39.2). With the FM off the five classical partials, the ring and the 150 Hz / 800 Hz / 4 kHz energy shares do not move (ladder within 0.1 dB, ring within 0.8 %, shares within 0.1 pp): **what Vincent likes underneath is not in the FM**.",
          "* **Not the source:** the echo and spring (dry: flatness -17.5), VINTAGE, SPREAD, the shimmer (none moves the flatness by more than 0.7 dB; the echo accounts for 3 of the 13 off-ladder peaks), the engine's saturators (the voice mix never clamps, no sample reaches full scale, the filter's soft state acts on 0.15 % of the voice samples and 0.02 % in the first 100 ms at A4, the output tanh compresses a few thousand samples by more than 0.1 dB, a few hundred by more than 0.35 dB at the chord's peaks and by about 1.0 dB at its highest input; halving the mixer levels with the saturations at zero (VOLUME at its maximum, the level 9 dB lower) left every proxy at A4 within 0.4 dB) and the oscillator's aliasing (real but at 14-19 kHz, -26 dB re the energy above 4 kHz in an open-filter test; in the patch the share above 14 kHz is 0.08 % at A4, 1.0 % at A6 in the first 100 ms and is not separable from the saw's real harmonics there: **not isolated**). **OSC 2's LEVEL 0 does not remove the FM** (the modulator is taken before its level): `o2_off` keeps the grit (flatness -17.0); only `o1only` (LEVEL 0 and X-MOD 0) removes both.",
          "* **The fix: X-MOD 64 -> 32** (one value, the same in B2 / C2 / D2). Flatness at A4 100-400 ms -17.2 -> -25.9 dB (-8.7 dB; -6.8 dB at A3, -10.1 dB at A6), off-ladder peaks 13 -> 3 (A4, 100-400 ms), the 20-100 ms flatness -10.1 -> -17.2. **It does not reach the second target: the share above 4 kHz moves by only -0.6 .. +0.3 dB** (a 6 dB fall is a quarter of the share: 4.6 % -> 1.1 % at A4 in the strike), because that share is the saw's harmonics through the open filter at the strike, not FM.",
          "* **Where crisp and bell-like trade.** (1) X-MOD 0 is the cleanest (flatness -35.5, off-ladder 4) and leaves the ring, the ladder and the energy shares untouched (its wet returns were not measured), but the 100-400 ms centroid falls 13.7 % (A4) against a +-10 % limit: the sidebands are part of the strike's body, and a real bell carries more inharmonic partials than the five of the ladder (general knowledge, not measured here), so some of the FM is bell-like, not only grit; X-MOD 32 is the lowest round value inside the limit (-9.2 % at A4). (2) A 6 dB fall of the share above 4 kHz in the body needs the filter lower (CUTOFF 80: -4.7 dB at 100-400 ms, -9.4 dB at 1-2 s at A4, but the centroid falls 26 % and the 150-800 Hz share rises 2.6 pp): that is the strike's top, the part that reads as crisp or as bright, and it is the part a bell's definition lives in. **Not done in B2 / C2 / D2; cal6 (C2 with CUTOFF 84) lets Vincent hear one step of it.**", ""]
    L += ["## 1. The grit baseline (the Batch 6B variants rendered again with this kit: the ring times and levels reproduce the 6B figures exactly)", "",
          "| var | VOLUME | toll (ar) dB | chord dB | peak dBFS | CPU | ring A4 to -6 / -12 / -20 / -40 ms |", "|---|---|---|---|---|---|---|"]
    for k in "ABCD":
        m = base[k]; r = m["ring"]
        L.append(f"| {k} | {m['volume']} | {m['level']:.2f} | {m['level_chord']:.1f} | {m['peak_all']:.2f} | {m['cost']['total']:.0f} | " + " / ".join(f"{r[q]:.0f}" for q in ("6", "12", "20", "40")) + " |")
    L += ["", "Proxies (a number, not a verdict): the share of the energy above 4 kHz and in 2-8 kHz; the spectral flatness over 2-10 kHz (geometric over arithmetic mean of the averaged power spectrum: 0 dB is a flat, noise-like floor, a large negative number is a few clean partials); the count of spectral peaks within -30 dB (and -20 dB) of the strongest that are neither on the key's harmonic series (+-0.06 f0) nor the bell's tierce (2.4 x the key, +-3 %); the crest factor of the dry output.", ""]
    L += grit_rows(base, "ABCD")
    L += ["", "### Crest, clipping and where the engine's own saturators act (instrumented host)", "",
          "The engine's chain: voice mix (hard clamp at +-65535, a headroom of 2x), the filter's band-pass state (linear below +-0.75 of full scale, soft above: `svf_step`), the output stage (`softclip`, a tanh: x/32768 -> 0.76 at 32768; 0.1 dB of compression from an input of about 6000 = -14.7 dBFS, 0.5 dB at about 13000), the effects' 16-bit clip (`sat16`).", ""]
    L += sat_rows(base, "ABCD")
    L += ["", "## 2. Where the grit comes from (the isolation set on C, one change at a time, each re-fitted to -18.0 dBFS on the toll)", "",
          "| key | what | VOLUME | toll dB | peak | CPU | A4 >4 kHz % 0-20 / 20-100 / 100-400 / 1-2 s | flatness A4 / A3 / A6 (100-400 ms) | off-ladder A4 (-30 dB, 100-400) | crest A4 strike | filter-state sat % |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in iso:
        m = iso[k]; g = m["grit"]
        L.append(f"| {k} | {m.get('desc', 'C, round 1')} | {m['volume']} | {m['level']:.2f} | {m['peak_all']:.2f} | {m['cost']['total']:.0f} | " + " / ".join(f"{g['A4'][w]['over4k']:.2f}" for w in WN) +
                 f" | {g['A4']['100-400']['flat']:.1f} / {g['A3']['100-400']['flat']:.1f} / {g['A6']['100-400']['flat']:.1f} | {g['A4']['100-400']['nonlad']['count']} | {m['crest']['A4']['strike_0_400']:.1f} | {m['sat']['A4']['svf_sat_pct']:.2f} |")
    L += ["", "What each does to the bell (A4; the ladder is dB re the strongest partial, first 300 ms: hum / prime / tierce / quint / nominal; the ring is to -6 / -12 / -20 / -40 dB; the centroid and the shares are the strike's body):", "",
          "| key | ladder | ring | centroid 100-400 ms Hz (change) | shares 150-800 / 800-4k / >4k over 0-400 ms (pp change) |", "|---|---|---|---|---|"]
    c0 = iso["C"]
    for k in iso:
        m = iso[k]; r = m["ring"]; s = m["shares"]["A4"]["strike_0_400"]; s0 = c0["shares"]["A4"]["strike_0_400"]
        cc = m["cent"]["A4"]["100-400"]; c00 = c0["cent"]["A4"]["100-400"]
        L.append(f"| {k} | {lad(m['ladder']['A4'])} | " + " / ".join(f"{r[q]:.0f}" for q in ("6", "12", "20")) + f" / {f(r['40'], 0)} | {cc:.0f} ({100 * (cc / c00 - 1):+.1f} %) | {s['150-800']:.1f} / {s['800-4k']:.1f} / {s['>4k']:.2f} ({s['150-800'] - s0['150-800']:+.1f} / {s['800-4k'] - s0['800-4k']:+.1f} / {s['>4k'] - s0['>4k']:+.2f}) |")
    L += ["", "### Does the oscillator alias? (OSC 1 alone, a saw, the filter open, VINTAGE 0, effects off; the energy off the harmonic series k f0 +-6 Hz)", "",
          "| note | f0 Hz | off-harmonic energy re the whole, dB | re the energy above 4 kHz, dB | >4 kHz % | strongest off-harmonic peaks: Hz, dB re the fundamental, the harmonic it reflects (fs - k f0) |", "|---|---|---|---|---|---|"]
    for nm, v in ali.items():
        L.append(f"| {nm} | {v['f0']:.2f} | {v['nonharm_total_db']:.1f} | {v['nonharm_of_over4k_db']:.1f} | {v['over4k_pct']:.2f} | " + "; ".join(f"{a} Hz {b:+.1f} dB (k {c})" for a, b, c in v["peaks"][:3]) + " |")
    L += ["", "## 3. Candidates B2 / C2 / D2: the grit fix is X-MOD 64 -> 32, applied identically (A = the original array, level-matched)", ""]
    L += ["| var | VOLUME | toll (ar) | chord | peak (all phrases) | clipped samples | CPU | what |", "|---|---|---|---|---|---|---|---|"]
    for k in ("A", "B2", "C2", "D2"):
        m = cd[k]
        L.append(f"| {k} | {m['volume']} | {m['level']:.2f} | {m['level_chord']:.1f} | {m['peak_all']:.2f} | {m['clip']} | {m['cost']['total']:.0f} | " + ("the original, level-matched" if k == "A" else f"{k[0]} (round 1) with X-MOD 32") + " |")
    L += ["", "**Every change over the original array (percent = of the parameter's range):**", ""]
    for k in ("B2", "C2", "D2"):
        L.append(f"* **{k}:** " + R6.changes(orig, cd[k]["params"]) + f"; VOLUME {orig['VOLUME']} -> {cd[k]['params']['VOLUME']}; against round 1's {k[0]}: X-MOD {base[k[0]]['params']['XMOD']} -> {cd[k]['params']['XMOD']}, VOLUME {base[k[0]]['volume']} -> {cd[k]['volume']}")
    L += ["", "### The grit against the baseline (dB change of the share above 4 kHz; flatness before -> after; off-ladder count before -> after)", "",
          "| var | note | >4 kHz dB change 0-20 / 20-100 / 100-400 / 1-2 s | flatness 0-20 / 20-100 / 100-400 / 1-2 s (dB) | off-ladder (-30 dB) 20-100 / 100-400 / 1-2 s | crest strike (dry) |", "|---|---|---|---|---|---|"]
    for k in ("B", "C", "D"):
        n_ = k + "2"
        for nm in NOTES:
            a, b = base[k]["grit"][nm], cd[n_]["grit"][nm]
            L.append(f"| {n_} | {nm} | " + " / ".join(f"{db(a[w]['over4k'], b[w]['over4k']):+.1f}" for w in WN) + " | " + " / ".join(f"{a[w]['flat']:.1f} -> {b[w]['flat']:.1f}" for w in WN) + " | " +
                     " / ".join(f"{a[w]['nonlad']['count']} -> {b[w]['nonlad']['count']}" for w in WN[1:]) + f" | {base[k]['crest'][nm]['strike_0_400']:.1f} -> {cd[n_]['crest'][nm]['strike_0_400']:.1f} dB |")
    L += ["", "### Keep underneath unchanged (the acceptance numbers; PASS = inside the stated tolerance)", ""]
    L += ["| var | ring A4 to -6 / -12 / -20 / -40 ms (6B figure; change %) | ladder A4 first 300 ms, dB change hum / prime / tierce / quint / nominal | shares A4 strike, pp change <150 / 150-800 / 800-4k | shares A3 | centroid 100-400 ms A4 / A3 (change %) | wet return re dry, dB change 4 windows | verdict |", "|---|---|---|---|---|---|---|---|"]
    for k in ("B", "C", "D"):
        n_ = k + "2"; a, b = base[k], cd[n_]
        rr = [b["ring"][q] for q in ("6", "12", "20", "40")]
        rp = [100 * (x / y - 1) for x, y in zip(rr, SIX[k])]
        ld = [(b["ladder"]["A4"][q]["db"] - a["ladder"]["A4"][q]["db"]) if a["ladder"]["A4"][q] and b["ladder"]["A4"][q] else None for q in ("0.5", "1.0", "1.2", "1.5", "2.0")]
        sh = {nm: [b["shares"][nm]["strike_0_400"][q] - a["shares"][nm]["strike_0_400"][q] for q in ("<150", "150-800", "800-4k")] for nm in ("A4", "A3")}
        ce = {nm: 100 * (b["cent"][nm]["100-400"] / a["cent"][nm]["100-400"] - 1) for nm in ("A4", "A3")}
        wr = [y["re_dry_db"] - x["re_dry_db"] for x, y in zip(a["space"], b["space"])]
        ok = [all(abs(p) <= 3 for p in rp), all(abs(x) <= 3 for x in ld if x is not None), all(abs(x) <= 3 for nm in sh for x in sh[nm]), all(abs(wv) <= 1 for wv in wr), all(abs(v) <= 10 for v in ce.values())]
        L.append(f"| {n_} | " + " / ".join(f"{x:.0f} ({SIX[k][i]}; {rp[i]:+.1f})" for i, x in enumerate(rr)) + " | " + " / ".join("-" if x is None else f"{x:+.1f}" for x in ld) + " | " + " / ".join(f"{x:+.1f}" for x in sh["A4"]) + " | " + " / ".join(f"{x:+.1f}" for x in sh["A3"]) +
                 " | " + " / ".join(f"{b['cent'][nm]['100-400']:.0f} ({ce[nm]:+.1f})" for nm in ("A4", "A3")) + " | " + " / ".join(f"{x:+.1f}" for x in wr) + " | ring " + ("PASS" if ok[0] else "FAIL") + ", ladder " + ("PASS" if ok[1] else "FAIL") + ", shares " + ("PASS" if ok[2] else "FAIL") + ", returns " + ("PASS" if ok[3] else "FAIL") + ", centroid " + ("PASS" if ok[4] else "FAIL") + " |")
    L += ["", "Ladder of C2 against the 6B text (hum 0, prime -7, tierce 1.196 at -11, quint 1.498 at -10, nominal 1.997 at -12): " + lad(cd["C2"]["ladder"]["A4"]) + " (ratios " + " / ".join("-" if cd["C2"]["ladder"]["A4"][q] is None else f"{cd['C2']['ladder']['A4'][q]['ratio']:.3f}" for q in ("0.5", "1.0", "1.2", "1.5", "2.0")) + ").", "",
          "Space (A4 held 400 ms: return against the dry note, dry / return / re dry dB, windows 0-20 / 20-100 / 100-250 / 250-1000 ms):", ""]
    for k in ("B", "C", "D"):
        for tag, m in ((k, base[k]), (k + "2", cd[k + "2"])):
            L.append(f"* {tag}: " + "; ".join(f"{x['dry_db']:.1f} / {x['fx_db']:.1f} / {x['re_dry_db']:+.1f}" for x in m["space"]))
    L += ["", "### Level, peak, clipping", ""]
    L += sat_rows(cd, ("B2", "C2", "D2"))
    L += ["", "### The tail and register of C2: level dB, centroid Hz, >4 kHz % per window after the strike (A4; X-MOD does not touch the tail's top: the same windows as C, which has no tail table in this kit's baseline)", ""]
    L.append("* C2 A4: " + "; ".join(f"{x['w'][0]}-{x['w'][1]} ms: {x['rms']:.1f} dB, {x['cent']:.0f} Hz, {x['over4k']:.1f} %" for x in cd["C2"]["b6c"]["tail"]["A4"]))
    L += ["", "Register (C2, RMS 0-300 ms dB / centroid 0-100 ms Hz): " + "; ".join(f"{nm} {cd['C2']['b6c']['register'][n]['rms']:.1f} / {cd['C2']['b6c']['register'][n]['cent']:.0f}" for n, nm in (("45", "A2"), ("57", "A3"), ("69", "A4"), ("81", "A5"), ("93", "A6"))), ""]
    L += ["## 4. Live controls on the base (C2, A3; one step each way) and the CPU of the add-ons", "",
          "| control | base | step | value | hum | prime | tierce | quint | nominal | centroid 0-100 ms | ring -20 / -40 ms | level 0-300 ms | off-harmonic partials above -25 dB |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for x in cd["live"]:
        c = x["ladder"]
        L.append(f"| {x['control']} | {x['base']} | {x['step']:+d} | {x['value']} | " + " | ".join("-" if c[q] is None else f"{c[q]['ratio']:.3f} ({c[q]['db']:+.0f})" for q in ("0.5", "1.0", "1.2", "1.5", "2.0")) + f" | {x['cent']:.0f} | {f(x['t20'], 0)} / {f(x['t40'], 0)} | {x['rms']:.1f} | {x['inharmonic']} |")
    L += ["", "CPU of the live add-ons on C2 (host instr/sample, worst case): " + "; ".join(f"{k} {v:.0f}" for k, v in cd["addons"].items()) + f" (soft limit 2400). The grit fix itself: C {base['C']['cost']['total']:.0f} -> C2 {cd['C2']['cost']['total']:.0f} ({cd['C2']['cost']['total'] - base['C']['cost']['total']:+.0f}); X-MOD 0 (isolation) {iso['xmod0']['cost']['total']:.0f} (the engine skips the FM at 0).", ""]
    open(os.path.join(OUT2, "README.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    r28()
