#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Build the BOOT-MATCHED base for tests/voicing/identical.py: the firmware as it was before a batch, plus ONLY the new boot patch (slot 1).

Slot 1 is the program the synth boots into, and the CUTOFF / RESO slew (README section 8: x += (target - x) >> 6 stops up to 63/256 short when approaching from below) and the
effects' idle states carry over from it into the first program loaded.  So when slot 1 changes, EVERY other program renders slightly differently when loaded straight from boot
(a fraction of a semitone of cutoff, a reverb/echo state), although its patch bytes and the code are identical.  Comparing the new tree against this tree (same boot patch) isolates
what the OTHER changed slots did:

  python3 tests/voicing/make_mid.py build/voicing/base build/voicing/mid "Red Pill" PF_RED_PILL
  python3 tests/voicing/identical.py build/voicing/mid 2,6,8

Copies the base tree, inserts the new array (with its comment) from the working tree before PF_INIT and points the named FACTORY entry at it."""
import os
import re
import shutil
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def main():
    base, out, name, arr = sys.argv[1:5]
    shutil.rmtree(out, ignore_errors=True)
    shutil.copytree(base, out)
    cur = open(os.path.join(ROOT, "firmware", "src", "obv_patches.h")).read()
    m = re.search(r"(/\*[^/]*?\*/\n)?static const uint8_t " + arr + r"\[\] = \{.*?X\};\n", cur, re.S)
    p = os.path.join(out, "firmware", "src", "obv_patches.h")
    s = open(p).read()
    s = s.replace("static const uint8_t PF_INIT[] = {X};", m.group(0) + "static const uint8_t PF_INIT[] = {X};")
    s, n = re.subn(r'\{"' + re.escape(name) + r'", PF_[A-Z0-9_]+\}', '{"' + name + '", ' + arr + "}", s)
    assert n == 1
    open(p, "w").write(s)
    print(f"{out}: base + {arr} as {name}")


if __name__ == "__main__":
    main()
