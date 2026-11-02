#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-only
# Render GROWL's test scripts (tests/drive/*.txt from make_scripts.py) with the host build into build/drive/.
#   tests/drive/render.sh            then: python3 tests/drive/analyze.py build/drive
set -e
cd "$(dirname "$0")/../.."
mkdir -p build/drive
cc -O2 -Wall -Wno-unused-function -DOBV_HOST -DAPP_VER="\"dev\"" -Ifirmware/src -Ifirmware/gen \
   -o build/drive/obervave firmware/src/obervave.c
for s in tests/drive/src_*.txt tests/drive/alias_*.txt tests/drive/sweep_*.txt; do
    build/drive/obervave "build/drive/$(basename "$s" .txt)" "$s" >/dev/null
done
echo "renders -> build/drive/"
