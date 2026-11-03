#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-only
# Render DRAIN's test scripts (tests/spring/*.txt from make_scripts.py) with the host build into build/spring/kit/:
# "old_*" and "oldchain_*" with the build before the re-voice (OLD, default db0701c: the plate, overflow fixed, the
# old routing into CHEW), the hot-input case also with the build before the overflow fix (PREFIX, default c10db7d);
# and the bench's (spring_bench.c: the reverb alone on ideal signals, both builds; chirp_gd.c: the chirp chain).
#   tests/spring/render.sh [OLD] [PREFIX]          then: python3 tests/spring/analyze.py build/spring/kit
set -e
cd "$(dirname "$0")/../.."
OLD="${1:-db0701c}"; PRE="${2:-c10db7d}"
K=build/spring/kit
mkdir -p "$K"
CF="-O2 -Wall -Wno-unused-function -DOBV_HOST -DAPP_VER=\"dev\""
cc $CF -Ifirmware/src -Ifirmware/gen -o $K/obervave firmware/src/obervave.c
for r in "$OLD" "$PRE"; do
    T=$K/src_$r; rm -rf "$T"; mkdir -p "$T"
    git archive "$r" firmware/src firmware/gen firmware/hal tests/host.c | tar -x -C "$T"
    cc $CF -I"$T/firmware/src" -I"$T/firmware/gen" -o "$K/obervave_$r" "$T/firmware/src/obervave.c"
    cc -O2 -Wall -Wno-unused-function -I"$T/firmware/src" -I"$T/firmware/gen" -o "$K/bench_$r" tests/spring/spring_bench.c -lm
done
cc -O2 -Wall -Wno-unused-function -Ifirmware/src -Ifirmware/gen -o $K/bench tests/spring/spring_bench.c -lm
cc -O2 -Wall -Wno-unused-function -Ifirmware/src -Ifirmware/gen -o $K/chirp_gd tests/spring/chirp_gd.c
for s in tests/spring/src_*.txt tests/spring/chain_*.txt tests/spring/sweep_*.txt tests/spring/sweepm_*.txt tests/spring/jumps_*.txt tests/spring/hot_reverb.txt; do
    $K/obervave "$K/$(basename "$s" .txt)" "$s" > "$K/$(basename "$s" .txt).log"
done
grep -h "FAIL" $K/sweep_*.log && exit 1
for s in tests/spring/old_*.txt tests/spring/oldchain_*.txt; do
    $K/obervave_$OLD "$K/$(basename "$s" .txt)" "$s" > /dev/null
done
$K/obervave_$PRE "$K/hot_reverb_prefix" tests/spring/hot_reverb.txt > /dev/null
$K/obervave_$OLD "$K/hot_reverb_fixed" tests/spring/hot_reverb.txt > /dev/null
# the bench: impulse responses (SIZE 64, DAMP 0: the chirp and the flutter), a noise burst at each SIZE (the decay),
# the wet's spectrum under a held noise at the defaults; both builds
for b in bench bench_$OLD; do
    $K/$b $K/ir_$b.raw imp:16384 2 0:mix=127 0:size=64 0:damp=0 0:pre=0
    for sz in 0 16 32 48 64 80 96 112 127; do $K/$b $K/rt_${b}_$sz.raw noise:16384:300 14 0:mix=127 0:size=$sz 0:damp=0 0:pre=0; done
    $K/$b $K/ss_$b.raw noise:8231:3000 4.5 0:mix=127 0:size=80 0:damp=60 0:pre=20
done
for n in 2 4 10; do $K/chirp_gd $n > $K/gd_$n.txt; done
echo "renders -> $K/"
