#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-only
# Batch 9B: the audio must not change. Renders tests/controls/render4.txt (patches 03, 14, 28, 30) with the host build of a
# reference commit (default: main) and of this tree, and compares the two WAVs byte for byte.
#   sh tests/controls/bitident.sh [REF]      exit 1 if they differ
set -e
cd "$(dirname "$0")/../.."
REF="${1:-main}"
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
mkdir -p "$T/ref"
git archive "$REF" firmware tests/host.c | tar -x -C "$T/ref"
cc -O2 -Wall -Wno-unused-function -DOBV_HOST -DAPP_VER='"dev"' -I"$T/ref/firmware/src" -I"$T/ref/firmware/gen" -o "$T/ref/obervave" "$T/ref/firmware/src/obervave.c"
cc -O2 -Wall -Wno-unused-function -DOBV_HOST -DAPP_VER='"dev"' -Ifirmware/src -Ifirmware/gen -o "$T/new" firmware/src/obervave.c
"$T/ref/obervave" "$T/ref/out" tests/controls/render4.txt > /dev/null
"$T/new" "$T/new.out" tests/controls/render4.txt > /dev/null
sha256sum "$T/ref/out.wav" "$T/new.out.wav" | sed "s|$T/||"
cmp "$T/ref/out.wav" "$T/new.out.wav" && echo "IDENTICAL: the four patches render bit for bit the same as $REF"
