#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Compare two builds of the app (and the update loader), section by section and function by function.

  tools/image_diff.py OLD_BUILD_DIR NEW_BUILD_DIR      (each a build/ directory: obervave.elf, obervave.dis, loader/)

Used to show that a change touched only what it says. Sections: .text, .data, .ram_text sizes and bytes (the
binaries build.py extracts: text.bin, data.bin, ramtext.bin). Functions: the disassembly (obervave.dis,
loader/loader.dis) cut per symbol and normalised so a moved constant does not count: the address columns go, and a
load of a data address (`r1 = 33664150 <sym+0x4 : 201ac96 >`) becomes `r1 = @data`; calls and jumps keep their
target symbol. A function whose normalised text differs is listed with its first differing instruction.
Strings: the printable runs (>= 4 bytes) of the app and loader images that are in one build and not the other."""
import re
import sys
from pathlib import Path

LBL = re.compile(r"^([A-Za-z_.$][\w.$]*):\s*$")
INS = re.compile(r"^\s*([0-9a-f]+):\s+(?:[0-9a-f]{2} )+\s*\t(.*)$")
ADDR = re.compile(r"(-?\d+) <([^:>]+?) : [0-9a-f]+ >")


XIP = re.compile(r"= (3[34]\d{6})\b")            # 0x02000000.. as a decimal: an address in the XIP map


def norm(op):
    op = re.sub(r"\s*#.*$", "", op)                 # objdump's guesses at a constant's symbol
    if re.search(r"=\s*-?\d+ <", op) and not re.match(r"(call|goto|if)", op):
        op = re.sub(r"-?\d+ <[^>]*>", "@data", op)
    op = XIP.sub("= @xip", op)
    op = ADDR.sub(lambda m: f"<{m.group(2).strip()}>", op)
    return re.sub(r"(goto|call) (-?\d+) <", r"\1 <", re.sub(r"\+0x[0-9A-Fa-f]+>", "+@>", op))   # a branch's offset moves with the code around it


def symbol_sizes(elf):
    """{name: (address, size)} of the functions, from objdump -t (the code after a function's size is data the
    disassembler reads as instructions: not compared)"""
    import os
    import subprocess
    tc = os.environ.get("JIELI_TOOLCHAIN", str(Path.home() / ".jieli" / "toolchain"))
    out = subprocess.run([f"{tc}/common/bin/objdump", "-t", str(elf)], capture_output=True, text=True, check=True).stdout
    res = {}
    for ln in out.splitlines():
        p = ln.split()
        if len(p) >= 5 and p[-1] and re.fullmatch(r"[0-9a-f]{8}", p[0]) and re.fullmatch(r"[0-9a-f]{8}", p[-2]) and ".text" in p:
            res[p[-1]] = (int(p[0], 16), int(p[-2], 16))
    return res


def functions(dis_path, elf):
    sizes = symbol_sizes(elf)
    funcs, cur = {}, None
    for ln in Path(dis_path).read_text().splitlines():
        m = LBL.match(ln)
        if m:
            cur = m.group(1)
            funcs.setdefault(cur, [])
            continue
        m = INS.match(ln)
        if m and cur:
            a = int(m.group(1), 16)
            if cur in sizes and sizes[cur][1] and a >= sizes[cur][0] + sizes[cur][1]:
                continue                              # past the function's end: data
            funcs[cur].append(norm(m.group(2).strip()))
    return funcs


def strings(path, n=4):
    data = Path(path).read_bytes()
    return {m.group(0).decode("latin-1") for m in re.finditer(rb"[\x20-\x7e\xd8]{%d,}" % n, data)}


def regions(a, b):
    """byte ranges where two equal-length blobs differ"""
    out, i = [], 0
    while i < len(a):
        if a[i] != b[i]:
            j = i
            while j < len(a) and a[j] != b[j]:
                j += 1
            out.append((i, j))
            i = j
        else:
            i += 1
    return out


def compare_funcs(title, p_old, e_old, p_new, e_new):
    fo, fn = functions(p_old, e_old), functions(p_new, e_new)
    only_o, only_n = sorted(set(fo) - set(fn)), sorted(set(fn) - set(fo))
    diff = [k for k in sorted(set(fo) & set(fn)) if fo[k] != fn[k]]
    same = len(set(fo) & set(fn)) - len(diff)
    print(f"{title}: {len(fo)} / {len(fn)} functions; {same} identical after normalising, {len(diff)} differ, "
          f"{len(only_o)} only in OLD, {len(only_n)} only in NEW")
    for k in only_o:
        print(f"    only in OLD: {k} ({len(fo[k])} insns)")
    for k in only_n:
        print(f"    only in NEW: {k} ({len(fn[k])} insns)")
    for k in diff:
        a, b = fo[k], fn[k]
        i = next((i for i in range(min(len(a), len(b))) if a[i] != b[i]), min(len(a), len(b)))
        print(f"    differs: {k}: {len(a)} -> {len(b)} insns, first difference at #{i}: "
              f"{a[i] if i < len(a) else '-'}  |  {b[i] if i < len(b) else '-'}")
    return diff, only_o, only_n


def compare_blobs(title, old, new):
    a, b = Path(old).read_bytes(), Path(new).read_bytes()
    if len(a) != len(b):
        print(f"{title}: sizes differ, {len(a)} -> {len(b)} bytes")
        return
    r = regions(a, b)
    print(f"{title}: {len(a)} bytes, " + ("identical" if not r else f"{len(r)} differing regions, {sum(e - s for s, e in r)} bytes: " +
          ", ".join(f"[{s:#x},{e:#x})" for s, e in r[:40])))


def main():
    o, n = Path(sys.argv[1]), Path(sys.argv[2])
    for sect in ("text.bin", "data.bin", "ramtext.bin"):
        if (o / sect).exists() and (n / sect).exists():
            compare_blobs(f"app {sect}", o / sect, n / sect)
    compare_funcs("app", o / "obervave.dis", o / "obervave.elf", n / "obervave.dis", n / "obervave.elf")
    compare_funcs("loader", o / "loader" / "loader.dis", o / "loader" / "loader.elf", n / "loader" / "loader.dis", n / "loader" / "loader.elf")
    for what, po, pn in (("app", o / "obervave.bin", n / "obervave.bin"), ("loader", o / "loader" / "loader.bin", n / "loader" / "loader.bin")):
        so, sn = strings(po), strings(pn)
        print(f"{what} strings only in OLD: {sorted(so - sn)}")
        print(f"{what} strings only in NEW: {sorted(sn - so)}")


if __name__ == "__main__":
    main()
