#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-only
# Render TAPE's test scripts (tests/tape/*.txt from make_scripts.py) with the host build into build/tape/, and the
# bench's (tape_bench.c: TAPE alone on ideal signals).
#   tests/tape/render.sh            then: python3 tests/tape/analyze.py build/tape
set -e
cd "$(dirname "$0")/../.."
mkdir -p build/tape
cc -O2 -Wall -Wno-unused-function -DOBV_HOST -DAPP_VER="\"dev\"" -Ifirmware/src -Ifirmware/gen \
   -o build/tape/obervave firmware/src/obervave.c
cc -O2 -Wall -Wno-unused-function -Ifirmware/src -Ifirmware/gen -o build/tape/bench tests/tape/tape_bench.c -lm
for s in tests/tape/src_*.txt tests/tape/nohiss_*.txt tests/tape/combo*.txt tests/tape/alias_*.txt \
         tests/tape/sweep_*.txt tests/tape/toggle_*.txt; do
    build/tape/obervave "build/tape/$(basename "$s" .txt)" "$s" >/dev/null
done
B=build/tape/bench
$B build/tape/bench_sweep_1k.raw sweep 1000 8192 0 0
$B build/tape/bench_sweep_5k.raw sweep 5000 8192 0 0
$B build/tape/bench_fixed_1k.txt fixed 1000 8192
$B build/tape/bench_fixed_5k.txt fixed 5000 8192
$B build/tape/bench_sweep_1k_hd.raw sweep 1000 8192 127 127
$B build/tape/bench_toggle.raw toggle 1000 8192 127
for v in 1 16 32 48 64 80 95 111 127; do
    $B build/tape/bench_hiss_$v.raw dc 200 4 $v 64
done
$B build/tape/bench_hiss_127_1.raw dc 200 4 127 1
$B build/tape/bench_hiss_127_127.raw dc 200 4 127 127
for f in 1000 5000 10000 15000 18000; do
    TP_ONLY=read TP_LOG=build/tape/bench_read_$f.d $B build/tape/bench_read_$f.raw sine $f 16384 6 127 64 0 0
    TP_ONLY=sat $B build/tape/bench_sat_$f.raw sine $f 16384 6 127 64 0 0
done
for v in 32 64 95 127; do $B build/tape/bench_wow_$v.raw sine 1000 16384 12 $v 64 0 0; done
$B build/tape/bench_wow_127_wf0.raw sine 1000 16384 12 127 0 0 0
$B build/tape/bench_wow_127_wf127.raw sine 1000 16384 12 127 127 0 0
for v in 32 64 95 127; do $B build/tape/bench_thd_$v.raw sine 1000 16384 6 $v 64 0 0; done
for c in 64 95 127; do for dr in 64 127; do $B build/tape/bench_drops_${c}_$dr.raw sine 1000 16384 30 $c 64 0 $dr; done; done
echo "renders -> build/tape/"
