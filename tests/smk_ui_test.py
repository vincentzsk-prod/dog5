#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# SMK-37 port of OberVave: Copyright (C) 2026 zvenson
"""The SMK-37 mapping on the host (tests/host.c with BOARD_SMK37): the fader banks, the wheels, the outer keys
(the pads were the step sequencer; DØG-5 deleted it, CLAUDE.md §5 -- they're free and always dark now).
Builds build/host/obervave-smk37-test, runs tests/smk/*.txt, checks what comes out (MIDI out, the dumped
state). Exit 1 on a failure.

  python3 tests/smk_ui_test.py
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build" / "host"
BIN = OUT / "obervave-smk37-test"
fails = 0


def check(name, ok, detail=""):
    global fails
    print(("  ok    " if ok else "  FAIL  ") + name + ("" if ok else f"  ({detail})"))
    fails += not ok


def run(script):
    out = subprocess.run([str(BIN), str(OUT / f"smk-{script}"), str(ROOT / "tests" / "smk" / f"{script}.txt")],
                         capture_output=True, text=True, check=True).stdout
    dumps = {}
    for ln in out.splitlines():
        m = re.match(r"\s*(\d+) ms  (PADS|STATE)(.*)$", ln)
        if m:
            dumps.setdefault(int(m[1]), {})[m[2]] = m[3].strip()
    return out, dumps


def state(d, t):
    return dict(kv.split("=") for kv in d[t]["STATE"].split())


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cc", "-O1", "-Wall", "-Wno-unused-function", "-DOBV_HOST", "-DBOARD_SMK37=1", '-DAPP_VER="test"',
                    "-I" + str(ROOT / "firmware/src"), "-I" + str(ROOT / "firmware/gen"), "-o", str(BIN),
                    str(ROOT / "firmware/src/obervave.c")], check=True)

    print("== faders: banks A and B, a fader acts once it moves")
    out, d = run("faders")
    st = state(d, 3400)
    check("bank A: CUTOFF RESO ENV AMT RELEASE", (st["cutoff"], st["reso"], st["envamt"], st["release"]) ==
          ("100", "50", "0", "127"), st)
    st, st0 = state(d, 3700), state(d, 3400)
    check("FADER BANK: bank B, nothing moved yet", st["bank"] == "1" and st["cho"] == st0["cho"] and st["master"] == "724",
          st)
    st = state(d, 4100)
    check("bank B: CHORUS mix, MASTER (fader 4 back down to 64)", st["cho"] == "120" and st["master"] == "515" and
          st["cutoff"] == "100", st)
    st = state(d, 4400)
    check("back to A: CUTOFF follows fader 1 again", st["bank"] == "0" and st["cutoff"] == "30", st)

    print("== wheels")
    out, d = run("wheels")
    check("at rest: no bend, no vibrato", (state(d, 3000)["bend"], state(d, 3000)["vib"]) == ("0", "0"), state(d, 3000))
    check("pitch wheel up: full bend (the MIDI scale, x the program's BEND 2 = +2 semitones)",
          state(d, 3300)["bend"] == "8191", state(d, 3300))
    check("pitch wheel down: full bend down", state(d, 3600)["bend"] == "-8192", state(d, 3600))
    check("back at rest: 0", state(d, 3900)["bend"] == "0", state(d, 3900))
    check("mod wheel up: vibrato 127", state(d, 4200)["vib"] == "127", state(d, 4200))
    check("mod wheel down: 0", state(d, 4500)["vib"] == "0", state(d, 4500))

    print("== outer keys")
    out, d = run("outer")
    check("C3 (keybed 0) plays C3 at its velocity", "MIDI out 90 48 90" in out and "MIDI out 80 48 0" in out, out[-300:])
    check("C6 (keybed 36) plays C6", "MIDI out 90 84 40" in out)
    check("OCT+ moves the outer keys too (E3 -> E4)", "MIDI out 90 64 100" in out)

    print("SMK-37 UI: " + ("all passed" if not fails else f"{fails} FAILED"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
