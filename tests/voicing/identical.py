#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Prove a voicing commit touched only its own slot: render every factory program with the firmware as it was
(an exported older tree) and as it is now, compare byte for byte; also compare the 96-byte patch hashes.

  git archive <commit before> | tar -x -C build/voicing/base
  python3 tests/voicing/identical.py build/voicing/base [slots=3] [--from-init]      (one slot, or several: 30,31,4,25)
  --from-init: every program is loaded from INIT (program 33 at 2000 ms) first. NEEDED when slot 1 changes: slot 1 is the boot patch, and CUTOFF / RESO slew in
  from it (README section 8), so every program loaded straight after boot starts its slew from a different place (a fraction of a semitone, up to -12 dB difference in the audio)

Each slot is rendered on every phrase in voicekit.PHRASE_FILES (a riff, b stabs, c held, the CPU stress chord and, since
Batch 1A, the lead and the low-unison phrases), so the whole sound path of the program is exercised (voices, filter, LFO,
every FX stage a patch has on).  Exit 0: only the named slots differ (in the patch bytes and the audio) and all the
others are identical; 1 otherwise."""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K


def dump_all(src_dir, tag):
    exe = os.path.join(K.BUILD, "dump_patch_" + tag)
    subprocess.run(["cc", "-Wall", "-Wno-unused-function", "-I" + os.path.join(src_dir, "firmware", "src"),
                    "-I" + os.path.join(src_dir, "firmware", "gen"), "-o", exe,
                    os.path.join(K.ROOT, "tests", "voicing", "dump_patch.c")], check=True)
    return subprocess.run([exe, "all"], capture_output=True, text=True, errors="replace", check=True).stdout.splitlines()


def render_pair(old, new, ph, slot, pre):
    """(old render, new render) of one slot on one phrase; with pre (the --from-init lines) the program select moves from 2600 to 2800 ms"""
    out = []
    for exe, tag in ((old, "id_old"), (new, "id_new")):
        if not pre:
            out.append(K.render(exe, ph, program=slot - 1, tag=tag)[0])
            continue
        sp = os.path.join(K.BUILD, tag + ".txt")
        lines = [l for l in K.compose(ph, program=slot - 1).splitlines() if not l.startswith(f"{K.T_SELECT} midi 0xC0")]
        lines = list(pre) + [f"2800 midi 0xC0 {slot - 1} 0"] + lines
        lines.sort(key=lambda l: int(l.split()[0]) if not l.endswith(" end") else 10 ** 9)
        open(sp, "w").write("\n".join(lines) + "\n")
        subprocess.run([exe, os.path.join(K.BUILD, tag), sp], cwd=K.ROOT, check=True, capture_output=True)
        out.append(K.read_wav(os.path.join(K.BUILD, tag + ".wav")))
    return out


def main():
    from_init = "--from-init" in sys.argv                # load every program from INIT (program 33 first): the boot patch (slot 1) no longer matters
    sys.argv = [a for a in sys.argv if a != "--from-init"]
    # --from-init: the boot patch (slot 1) must not matter.  CUTOFF / RESO slew by x += (target - x) >> 6, which stops up to 63/256 short when approaching from below but lands
    # exactly when approaching from above; so before the program is loaded the state is driven to INIT's by an approach from above (INIT, CUTOFF + RESO to 127, INIT), identical in
    # both builds whatever the boot patch was.  Events before the splash ends (~2.4 s) are ignored, so this runs 2420-2600 ms and the program is selected at 2800 ms.
    pre = ("2420 midi 0xC0 32 0", "2440 param 12 127", "2440 param 13 127", "2600 midi 0xC0 32 0") if from_init else ()
    base = os.path.abspath(sys.argv[1])
    slots = {int(x) for x in sys.argv[2].split(",")} if len(sys.argv) > 2 else {3}
    old = K.build_host(base, os.path.join(K.BUILD, "obervave_base"))
    new = K.build_host(K.ROOT, os.path.join(K.BUILD, "obervave_new"))
    ok = True
    d_old, d_new = dump_all(base, "old"), dump_all(K.ROOT, "new")
    for o, n in zip(d_old, d_new):
        s = int(o[:2])
        same = o == n
        if (s in slots) == same:                 # the named slots must differ, all others must not
            ok = False
            print(f"PATCH BYTES slot {s:02d}: {'unexpectedly differ' if not same else 'did not change'}  {o} | {n}")
    print(f"patch bytes: {sum(o == n for o, n in zip(d_old, d_new))} of 32 slots identical (slots {sorted(slots)} are the ones that change)")
    nid, named_differs = 0, {}
    for s in range(1, 33):
        same = True
        for ph in K.PHRASE_FILES:
            a, b = render_pair(old, new, ph, s, pre)
            same &= bool((a == b).all())
        if s not in slots:
            nid += same
            if not same:
                ok = False
                print(f"AUDIO slot {s:02d}: DIFFERS")
        else:
            named_differs[s] = not same
            if same:
                ok = False
                print(f"AUDIO slot {s:02d}: did not change")
    print(f"audio: {nid} of {32 - len(slots)} other slots byte-identical on all {len(K.PHRASE_FILES)} phrases; named slots differ: {named_differs}")
    print("OK" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
