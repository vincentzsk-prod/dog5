#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-only
# Prove the sound is byte-identical to another revision: build that revision's host app and this tree's, render the
# same scripts with both, compare the WAVs byte for byte. Exit 1 on any difference.
#   tests/drive/bitexact.sh REV [script ...]     (default scripts: all 32 programs with the GROWL slot at 0, and the
#                                               host's default, families, map, poly, fxhold scripts)
set -e
cd "$(dirname "$0")/../.."
REV="${1:?usage: tests/drive/bitexact.sh REV [script ...]}"; shift
[ $# -gt 0 ] || set -- tests/drive/factory_all.txt "" tests/families.txt tests/map.txt tests/poly.txt tests/fxhold.txt
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
mkdir -p "$T/ref"
git archive "$REV" firmware/src firmware/gen firmware/hal tests/host.c | tar -x -C "$T/ref"
CF="-O2 -Wall -Wno-unused-function -DOBV_HOST -DAPP_VER=\"dev\""
cc $CF -I"$T/ref/firmware/src" -I"$T/ref/firmware/gen" -o "$T/old" "$T/ref/firmware/src/obervave.c"
cc $CF -Ifirmware/src -Ifirmware/gen -o "$T/new" firmware/src/obervave.c
fail=0; i=0
for s in "$@"; do
    i=$((i + 1))
    "$T/old" "$T/o$i" $s >/dev/null || true
    "$T/new" "$T/n$i" $s >/dev/null || true
    if cmp -s "$T/o$i.wav" "$T/n$i.wav"; then echo "identical  ${s:-(default script)}  $(md5sum < "$T/n$i.wav" | cut -c1-12)"
    else echo "DIFFERENT  ${s:-(default script)}"; fail=1; fi
done
[ "$fail" = 0 ] && echo "byte-identical to $REV" || echo "NOT byte-identical to $REV"
exit "$fail"
