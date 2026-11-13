#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# The 32 factory names for the web player's patch list, read (never written) from the {"NAME", PF_xxx} table
# FACTORY[NFACT] in firmware/src/obv_patches.h, as the firmware has them: "\xD8" is the Ø (font byte 0xD8).
#   python3 web/sim/gen_patches.py OUT.json
import json, re, sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
src = (root / "firmware/src/obv_patches.h").read_text(encoding="utf-8")
body = src[src.index("FACTORY[NFACT] = {"):]
body = body[:body.index("};")]
names = [m.group(1) for m in re.finditer(r'\{"((?:[^"\\]|\\.)*)",\s*PF_\w+\}', body)]
names = [re.sub(r"\\x([0-9A-Fa-f]{2})", lambda m: "Ø" if m.group(1).upper() == "D8" else chr(int(m.group(1), 16)), n) for n in names]
nfact = int(re.search(r"#define\s+NFACT\s+(\d+)", (root / "firmware/src/obv_params.h").read_text()).group(1))
if len(names) != nfact or any("\\" in n or '"' in n for n in names):
    sys.exit(f"gen_patches: found {len(names)} names for NFACT {nfact}, or an escape left: {names}")
chapters = ["The Wasteland Arsenal", "The Tidal Hexes", "The Bakshi Tomes", "The Ancient Relics"]   # 8 slots each
out = [{"chapter": chapters[i // 8], "slot": i + 1, "name": n} for i, n in enumerate(names)]
Path(sys.argv[1]).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"patches: {len(out)} names -> {sys.argv[1]}")
