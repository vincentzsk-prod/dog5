#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Prove a voicing commit touched only its own slot: render every factory program with the firmware as it was
(an exported older tree) and as it is now, compare byte for byte; also compare the 96-byte patch hashes.

  git archive <commit before> | tar -x -C build/voicing/base
  python3 tests/voicing/identical.py build/voicing/base [slots=3]      (one slot, or several: 30,31,4,25)

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


def main():
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
            a, _ = K.render(old, ph, program=s - 1, tag="id_old")
            b, _ = K.render(new, ph, program=s - 1, tag="id_new")
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
