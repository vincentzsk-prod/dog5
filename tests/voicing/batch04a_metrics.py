# SPDX-License-Identifier: GPL-3.0-only
"""Measurements new in Batch 4A (Chapter II: 10 Atlantic Swell, 12 Kelp Tangle, 16 Tidal Pull: the organ / PWM / wash set).

Everything reads a host render (stereo float array from t = 0, 44.1 kHz).  Older measures: batch02a_metrics.py (level, centroid, band shares, tails, echo),
batch03a_metrics.py (crest, attack probe, PWM, band envelopes).  Definitions: dog5-docs/voicing/README.md section 15."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import dog_metrics as D
import batch02a_metrics as M
import batch03a_metrics as N

FS = K.FS
_s = N._s
FXOFF_ALL = {"DLY_MIX": 0, "REV_MIX": 0, "CHEW": 0, "GROWL": 0}      # the voice alone (REV_MIX = DRAIN)


def window_split(a, t0_ms, t1_ms, nfft=4096):
    """band shares (%) over [t0, t1] and the MUD figure = share(150-400) / share(1.2k+) (the dictionary's muddy ratio: high = energy piled low with nothing above)"""
    b = M.band_shares(a, t0_ms, t1_ms, nfft=min(nfft, max(512, 1 << int(np.log2(max(_s(t1_ms - t0_ms), 512))))))
    top = max(b["1.2k+"], 1e-3)
    return {"shares": b, "mud": b["150-400"] / top, "cent": M.centroid(a, t0_ms, t1_ms, nfft=2048)}


def note_windows(a, notes, nfft=2048):
    """band shares / MUD / centroid over the note-on region of the given notes [(on, off)] (frames fully inside a note)"""
    x = a.mean(1)
    m = np.zeros(len(x), bool)
    for on, off in notes:
        m[_s(on):_s(off)] = True
    win = np.hanning(nfft)
    f = np.fft.rfftfreq(nfft, 1 / FS)
    tot = {b[0]: 0.0 for b in D.BANDS}
    num = den = 0.0
    for s in range(0, len(x) - nfft, nfft // 2):
        if not m[s:s + nfft].all():
            continue
        X = np.abs(np.fft.rfft(x[s:s + nfft] * win))
        P = X ** 2
        for n, lo, hi in D.BANDS:
            tot[n] += P[(f >= lo) & (f < hi)].sum()
        e = P.sum()
        if e > 0:
            num += e * (f * X).sum() / X.sum()
            den += e
    t = sum(tot.values()) or 1.0
    sh = {k: 100 * v / t for k, v in tot.items()}
    return {"shares": sh, "mud": sh["150-400"] / max(sh["1.2k+"], 1e-3), "cent": num / den if den else 0.0}


def fx_set(exe, phrase, params, tag):
    """the four renders that separate the sends: full, dry (voice, no sends), delay-only (DRAIN 0), spring-only (DLY_MIX 0).  The spring sits AFTER the delay
    and is fed the sum, so full - dry - delay_only - spring_only is the spring ringing the echo (the interaction)"""
    r = {"full": K.render(exe, phrase, params=params, tag=tag + "f")[0],
         "dry": K.render(exe, phrase, params={**params, "DLY_MIX": 0, "REV_MIX": 0}, tag=tag + "d")[0],
         "dly": K.render(exe, phrase, params={**params, "REV_MIX": 0}, tag=tag + "e")[0],
         "spr": K.render(exe, phrase, params={**params, "DLY_MIX": 0}, tag=tag + "s")[0]}
    return r


def return_windows(r, off_ms, pre_ms, wins):
    """after a note-off: the delay's own return (dly - dry), the spring's own return (spr - dry) and the interaction (the spring ringing the echo), per window (ms after the
    note-off), in dB re the dry note's RMS over the pre_ms before the note-off (a held note's level).  The DC the delay path leaves is taken out by the mean of each window"""
    dry_ref = M.rms_db(r["dry"], off_ms - pre_ms, off_ms)
    d = r["dly"] - r["dry"]
    s = r["spr"] - r["dry"]
    i = r["full"] - r["dry"] - d - s
    out = []
    for a, b in wins:
        row = {"w": (a, b)}
        for nm, sig in (("dly", d), ("spr", s), ("int", i), ("all", r["full"] - r["dry"])):
            x = sig[_s(off_ms + a):_s(off_ms + b)]
            x = x - x.mean(0)
            row[nm] = float(10 * np.log10(max((x ** 2).mean(), 1e-12) / 32767 ** 2)) - dry_ref
        out.append(row)
    return out


def first_repeat(r, on_ms, off_ms, delay_ms):
    """the delay's first repeat of one ISOLATED note (a whole copy of it, arriving delay_ms after the note-on): the delay-only return's (wet-minus-dry, spring off) 4 ms power
    envelope inside [delay_ms - 30, delay_ms + note length + 150] ms after the note-on: its peak re the dry note's own peak (dB) and the time of that peak after the note-on (ms);
    the spring-only return's peak in the same window re the note and the delay's margin over it (dB)"""
    d = r["dly"] - r["dry"]
    s = r["spr"] - r["dry"]
    e_d, e_s, e_n = M.env_ms(d), M.env_ms(s), M.env_ms(r["dry"])
    i0 = int(on_ms)
    ln = int(off_ms - on_ms)
    note_pk = float(e_n[i0:i0 + ln + 60].max())
    a, b = i0 + int(delay_ms - 30), i0 + int(delay_ms + ln + 150)
    k = int(np.argmax(e_d[a:b]))
    spk = float(e_s[a:b].max())
    return {"dly_re_note": float(e_d[a + k] - note_pk), "t_ms": float(a + k - i0), "spr_re_note_same": float(spk - note_pk), "margin": float(e_d[a + k] - spk)}


def repeats_train(r, on_ms, off_ms, delay_ms, n=6):
    """the delay-only return of an isolated note as a train: the peak of the 4 ms envelope in each successive slot of one delay time (the k-th repeat arrives k * delay_ms after
    the note-on), in dB re the first repeat's peak: [(k, t ms after the note-on, dB re the first)]"""
    d = r["dly"] - r["dry"]
    e = M.env_ms(d)
    i0 = int(on_ms)
    pk = []
    for k in range(1, n + 1):
        a, b = i0 + int(k * delay_ms - 30), i0 + int((k + 1) * delay_ms - 30)
        seg = e[a:b]
        j = int(np.argmax(seg)) if len(seg) else 0
        pk.append((k, float(a + j - i0), float(seg[j]) if len(seg) else -120.0))
    return [(k, t, v - pk[0][2]) for k, t, v in pk]


def tail_after(a, off_ms, wins=((0, 250), (250, 750), (750, 1500)), dc=None):
    """band split and MUD of the tail after a note-off, per window: [{w, level dB, shares, mud, cent}] (the DC is taken out first)"""
    x = a - (dc if dc is not None else 0)
    out = []
    for w0, w1 in wins:
        sp = window_split(x, off_ms + w0, off_ms + w1)
        sp["w"] = (w0, w1)
        sp["db"] = M.rms_db(x, off_ms + w0, off_ms + w1)
        out.append(sp)
    return out


def chan_corr(a, t0_ms, t1_ms, lo=150, hi=4000):
    """the stereo width as the L/R correlation coefficient of the band lo..hi over [t0, t1] (1 = mono, 0 = uncorrelated, <0 = out of phase) and the side/mid energy ratio in dB"""
    x = a[_s(t0_ms):_s(t1_ms)]
    f = np.fft.rfftfreq(len(x), 1 / FS)
    sel = (f >= lo) & (f <= hi)
    L = np.fft.irfft(np.fft.rfft(x[:, 0]) * sel, len(x))
    R = np.fft.irfft(np.fft.rfft(x[:, 1]) * sel, len(x))
    c = float((L * R).sum() / max(np.sqrt((L ** 2).sum() * (R ** 2).sum()), 1e-9))
    mid, side = (L + R) / 2, (L - R) / 2
    return c, float(10 * np.log10(max((side ** 2).sum(), 1e-9) / max((mid ** 2).sum(), 1e-9)))


def band_beat(a, f0, t0_ms, t1_ms):
    """the chorus's own beating, read on the mono sum around f0 (voicekit.beat_metrics): mean / min / max beat rate (Hz) and the peak-to-peak depth (dB) of the band's envelope"""
    return K.beat_metrics(a, f0, t0_ms, t1_ms)


def am_depth(a, t0_ms, t1_ms, lo=0.2, hi=12.0, win_ms=20.0):
    """the level modulation (tremolo) of a held sound: 20 ms RMS series, depth = 95th - 5th percentile (dB), rate = the strongest component lo..hi Hz"""
    x = a.mean(1)[_s(t0_ms):_s(t1_ms)]
    w = _s(win_ms)
    e = np.array([10 * np.log10(max((x[i:i + w] ** 2).mean(), 1e-3)) for i in range(0, len(x) - w, w // 2)])
    return N.mod_rate_depth(e, FS / (w // 2), lo=lo, hi=hi)


def lfo_hz(rate):
    return 0.05 * 600 ** (rate / 127)


def pitch_cents(pitch_byte):
    """the LFO pitch law: peak cents = ((d*d) >> 7) * 9.375 (0 below 12)"""
    return ((pitch_byte * pitch_byte) >> 7) * 9.375


def pwm_points(pwm_byte):
    """the LFO PWM law: +- ((d*d) >> 7) * 0.195 points of pulse width"""
    return ((pwm_byte * pwm_byte) >> 7) * 0.1953


def amp_db(amp_byte):
    """the amp LFO law on a TRI: full level at the top of the swing, 1 - AMP/128 at the bottom: the peak-to-peak dip in dB"""
    return float(-20 * np.log10(max(1 - amp_byte / 128, 1e-3)))


def aa_ms(v):
    """the amp / filter envelope's attack time knob in ms (the time table, 0.5 ms * 20000^(v/127)); the measured attack (attack probe) is what counts"""
    return 0.5 * 20000 ** (v / 127)


def alley_ms(v):
    import re
    s = open(os.path.join(K.ROOT, "firmware", "gen", "obv_tables.h")).read()
    i = s.index("BBD_T[128]")
    t = [int(x) for x in re.findall(r"\d+", s[i:].split("{")[1].split("}")[0])]
    return t[v] / 44.1


def attack_long(exe, params, note=57, vel=100, hold_ms=1800):
    """the attack of a SLOW envelope (80-250 ms), as heard: the note struck from silence with the LFO, GROWL and the sends off, OSC 2 off and VINTAGE 0 (a detuned pair beats by several dB and moves the plateau the percentages are taken against: this reads the envelope itself); the stereo RMS envelope in trailing windows of one
    period of the note (hop 0.25 ms); the plateau = the mean power 1.0-1.4 s after the key-down; ms from the key-down (the first sample above -60 dB of the plateau) to 10 / 50 / 90 %
    of the plateau (voltage) and the level re the plateau at 20 / 50 / 100 / 200 ms"""
    q = {**params, **FXOFF_ALL, "LFO_PITCH": 0, "LFO_PWM": 0, "LFO_AMP": 0, "LFO_FLT": 0, "O2_WAVE": 0, "MODE": 0, "VINTAGE": 0}
    lines = N._probe_script(q, [f"3000 midi 0x90 {note} {vel}", f"{3000 + hold_ms} midi 0x80 {note} 0"], 3000 + hold_ms + 400)
    a = N._run(exe, "attl", lines)
    f0 = 440 * 2 ** ((note - 69) / 12)
    w, hop = int(FS / f0), int(0.00025 * FS)
    p = (a ** 2).mean(1)
    c = np.concatenate([[0.0], np.cumsum(p)])
    idx = np.arange(w, len(p), hop)
    e = np.sqrt((c[idx] - c[idx - w]) / w)
    plat = np.sqrt(p[_s(4000):_s(4400)].mean())
    t0 = idx[np.nonzero(e >= plat * 10 ** (-60 / 20))[0][0]] / FS * 1000
    t = idx / FS * 1000 - t0
    r = {f"t{k}": float(t[np.nonzero(e >= k / 100 * plat)[0][0]]) for k in (10, 50, 90)}
    r["re_plateau"] = {str(ms): float(20 * np.log10(max(e[np.searchsorted(t, ms)], 1e-9) / plat)) for ms in (20, 50, 100, 200)}
    return r


def solo_set(exe, params, notes, len_ms, tail_ms=3500, vel=100, tag="solo"):
    """the four sends renders (full / dry / delay-only / spring-only, as fx_set) of ONE isolated note or chord struck at 3000 ms and held len_ms, with nothing before it (a clean
    train of repeats: in a phrase the previous notes' echoes are still ringing).  Returns (R, on_ms, off_ms)"""
    on, off = 3000, 3000 + len_ms
    ev = [f"{on} midi 0x90 {n} {vel}" for n in notes] + [f"{off} midi 0x80 {n} 0" for n in notes]
    end = off + tail_ms
    out = {}
    for nm, ov in (("full", {}), ("dry", {"DLY_MIX": 0, "REV_MIX": 0}), ("dly", {"REV_MIX": 0}), ("spr", {"DLY_MIX": 0})):
        out[nm] = N._run(exe, tag + nm, N._probe_script({**params, **ov}, ev, end))
    return out, on, off


def under_note(R, notes, which=("dly", "spr")):
    """how much echo / spring sits UNDER the notes of a staccato figure: for each note (on, off) the RMS of the send's own return over the note's span re the dry note's RMS over the
    same span (dB); returns {send: [per note dB]}.  Lower = a crisper note: the repeats of earlier notes land on it"""
    out = {}
    for k in which:
        fx = R[k] - R["dry"]
        out[k] = [float(M.rms_db(fx, on, off) - M.rms_db(R["dry"], on, off)) for on, off in notes]
    return out
