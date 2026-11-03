#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-only
# The reverb's overflow can't come back: the hot-input scripts, the whole chain at its extremes and the effects
# alone on the worst signals an int16 line carries, under -fsanitize=signed-integer-overflow,bounds; and the hot
# renders must hold no rail-to-rail crack (the overflow's wrap flipped one channel's polarity at full scale: a step
# of 65,534 between neighbouring samples; the true signal's largest step there is under 8,000).
#   tests/spring/regress.sh            exit 1 on any sanitizer report or a crack
set -e
cd "$(dirname "$0")/../.."
O=build/spring/regress
mkdir -p "$O"
SAN="-O1 -g -fsanitize=signed-integer-overflow,bounds -fno-sanitize-recover=all -Wall -Wno-unused-function"
cc $SAN -DOBV_HOST -DAPP_VER=\"dev\" -Ifirmware/src -Ifirmware/gen -o "$O/obervave" firmware/src/obervave.c
cc $SAN -Ifirmware/src -Ifirmware/gen -o "$O/bench" tests/spring/spring_bench.c -lm
fail=0
for s in tests/spring/hot_reverb.txt tests/spring/hot_reverb_vdrive.txt tests/spring/worst_rev.txt ${EXTRA_SCRIPTS:-}; do
    n=$(basename "$s" .txt)
    if "$O/obervave" "$O/$n" "$s" > "$O/$n.log" 2>&1; then echo "clean   $s"; else echo "FAIL    $s"; grep runtime "$O/$n.log"; fail=1; fi
done
# the bench: squares (50 Hz .. 7 kHz), alternating rails, noise, a low burst, all at full scale, into the reverb at
# MIX 127 and SIZE / DAMP at their ends (PRE-DLY 0), with ALLEY's runaway on and off
k=0
for sig in square:50:32767:2000 square:440:32767:2000 square:2000:32767:2000 square:7000:32767:2000 nyq:32767:2000 noise:32767:2000 burst:100:32767:2000; do
    for sz in 0 64 100 127; do for dp in 0 127; do for dm in 0 127; do
        k=$((k + 1))
        if ! "$O/bench" /dev/null $sig 3 0:mix=127 0:size=$sz 0:damp=$dp 0:pre=0 0:dmix=$dm 0:fb=127 0:alley=30 ${BENCH_EXTRA:-} > "$O/bench.log" 2>&1; then
            echo "FAIL    bench $sig size $sz damp $dp dmix $dm"; grep runtime "$O/bench.log"; fail=1
        fi
    done; done; done
done
[ "$fail" = 0 ] && echo "clean   bench: $k runs (7 signals x SIZE 0/64/100/127 x DAMP 0/127 x ALLEY off / runaway)"
# no crack in the plain build's hot renders
cc -O2 -Wall -Wno-unused-function -DOBV_HOST -DAPP_VER=\"dev\" -Ifirmware/src -Ifirmware/gen -o "$O/obervave_o2" firmware/src/obervave.c
for s in tests/spring/hot_reverb.txt tests/spring/hot_reverb_vdrive.txt; do
    n=$(basename "$s" .txt)
    "$O/obervave_o2" "$O/${n}_o2" "$s" > /dev/null
    python3 - "$O/${n}_o2.wav" <<'PY' || fail=1
import sys, wave, numpy as np
w = wave.open(sys.argv[1]); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2).astype(np.int64)
step = int(np.abs(np.diff(x, axis=0)).max())
ok = step < 32767
print(("ok     " if ok else "FAIL   "), sys.argv[1], "largest step between neighbouring samples", step, "(a crack: 65,534)")
sys.exit(0 if ok else 1)
PY
done
[ "$fail" = 0 ] && echo "regress: clean" || echo "regress: FAILED"
exit "$fail"
