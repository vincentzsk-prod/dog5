#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""identical.py on all cores (Batch 5A: 29 phrases x 32 slots x 2 builds is over an hour in series).  Same proof, same exit code; each worker renders in its own build folder.

  python3 tests/voicing/identical_par.py build/voicing/base 18,19,22 [--jobs 4]"""
import multiprocessing as mp
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voicekit as K
import identical as I

OLD = NEW = None


def init(old, new):
    global OLD, NEW
    OLD, NEW = old, new
    d = os.path.join(K.BUILD, f"w{os.getpid()}")
    os.makedirs(d, exist_ok=True)
    K.BUILD = d


def job(a):
    slot, ph = a
    x = K.render(OLD, ph, program=slot - 1, tag="o")[0]
    y = K.render(NEW, ph, program=slot - 1, tag="n")[0]
    return slot, ph, bool((x == y).all())


def main():
    base = os.path.abspath(sys.argv[1])
    slots = {int(x) for x in sys.argv[2].split(",")}
    jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else os.cpu_count()
    old = K.build_host(base, os.path.join(K.BUILD, "obervave_base"))
    new = K.build_host(K.ROOT, os.path.join(K.BUILD, "obervave_new"))
    ok = True
    d_old, d_new = I.dump_all(base, "old"), I.dump_all(K.ROOT, "new")
    for o, n in zip(d_old, d_new):
        s = int(o[:2])
        if (s in slots) == (o == n):
            ok = False
            print(f"PATCH BYTES slot {s:02d}: {'unexpectedly differ' if o != n else 'did not change'}  {o} | {n}")
    print(f"patch bytes: {sum(o == n for o, n in zip(d_old, d_new))} of 32 slots identical (slots {sorted(slots)} are the ones that change)", flush=True)
    work = [(s, ph) for s in range(1, 33) for ph in K.PHRASE_FILES]
    res = {}
    with mp.Pool(jobs, init, (old, new)) as p:
        for s, ph, same in p.imap_unordered(job, work, chunksize=4):
            res.setdefault(s, {})[ph] = same
    nid = 0
    named = {}
    for s in range(1, 33):
        same = all(res[s].values())
        if s in slots:
            named[s] = {"differs_on": sum(1 for v in res[s].values() if not v)}
            if same:
                ok = False
                print(f"AUDIO slot {s:02d}: did not change")
        else:
            nid += same
            if not same:
                ok = False
                print(f"AUDIO slot {s:02d}: DIFFERS on {[ph for ph, v in res[s].items() if not v]}")
    print(f"audio: {nid} of {32 - len(slots)} other slots byte-identical on all {len(K.PHRASE_FILES)} phrases; named slots: {named}")
    print("OK" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
