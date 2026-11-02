#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-only
# Render ALLEY's test scripts (tests/bbd/*.txt from make_scripts.py) with the host build into build/bbd/, the "old_*"
# ones with the build before ALLEY (OLD, default 3b2fc9a: the old ping-pong delay), and the bench's (bbd_bench.c:
# ALLEY alone on ideal signals).
#   tests/bbd/render.sh [OLD]          then: python3 tests/bbd/analyze.py build/bbd
set -e
cd "$(dirname "$0")/../.."
OLD="${1:-3b2fc9a}"
mkdir -p build/bbd
CF="-O2 -Wall -Wno-unused-function -DOBV_HOST -DAPP_VER=\"dev\""
cc $CF -Ifirmware/src -Ifirmware/gen -o build/bbd/obervave firmware/src/obervave.c
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
git archive "$OLD" firmware/src firmware/gen firmware/hal tests/host.c | tar -x -C "$T"
cc $CF -I"$T/firmware/src" -I"$T/firmware/gen" -o build/bbd/obervave_old "$T/firmware/src/obervave.c"
cc -O2 -Wall -Wno-unused-function -Ifirmware/src -Ifirmware/gen -o build/bbd/bench tests/bbd/bbd_bench.c -lm
for s in tests/bbd/src_*.txt tests/bbd/combo_*.txt tests/bbd/tap_*.txt tests/bbd/sweep_*.txt tests/bbd/mix_off_ringing.txt; do
    build/bbd/obervave "build/bbd/$(basename "$s" .txt)" "$s" > "build/bbd/$(basename "$s" .txt).log"
done
grep -h "FAIL" build/bbd/tap_*.log && exit 1
for s in tests/bbd/old_*.txt tests/bbd/mix_off_ringing.txt; do
    build/bbd/obervave_old "build/bbd/$(basename "$s" .txt)$([ "${s#*old_}" = "$s" ] && echo _oldbuild)" "$s" >/dev/null
done
B=build/bbd/bench
# the repeats: an impulse at four times, FEEDBK 100, MIX 127, PINGPONG 127; TONE 127 (the BBD alone) and 70 (default)
for a in 1 60 100 127; do
    $B build/bbd/imp_$a.raw imp:16384 6 0:alley=$a 0:fb=100 0:mix=127 0:spread=127 0:tone=127
    $B build/bbd/impt_$a.raw imp:16384 6 0:alley=$a 0:fb=100 0:mix=127 0:spread=127
done
# the time changes: a 1 kHz sine, FEEDBK 0 (the echo's pitch IS the read's speed): one step, lengthen, shorten
$B build/bbd/tc.raw sine:1000:8192 6 0:alley=80 0:fb=0 0:mix=127 0:spread=127 0:tone=127 1500:alley=81 2500:alley=110 4000:alley=40
# ... the knob swept one step every 60 ms, 1 -> 127 -> 1, FEEDBK 0 and 110
SW=""; t=600; i=2; while [ $i -le 127 ]; do SW="$SW $t:alley=$i"; t=$((t + 60)); i=$((i + 1)); done
t=$((t + 300)); i=126; while [ $i -ge 1 ]; do SW="$SW $t:alley=$i"; t=$((t + 60)); i=$((i - 1)); done
$B build/bbd/ck0_sweep.raw sine:1000:8192 17 0:alley=1 0:fb=0 0:mix=127 0:spread=127 0:tone=127 $SW
$B build/bbd/ck_sweep.raw sine:1000:8192 17 0:alley=1 0:fb=110 0:mix=127 0:spread=127 $SW
$B build/bbd/ck0_jump.raw sine:1000:8192 8 0:alley=80 0:fb=0 0:mix=127 0:tone=127 2000:alley=120 4000:alley=20 6000:alley=127
# self-oscillation: a 440 Hz burst, then FEEDBK held at each value for 20 s (80 ms; 740 ms; 10 ms)
for fb in 100 112 116 118 120 122 124 127; do $B build/bbd/so_$fb.raw burst:440:16384:80 20 0:alley=80 0:fb=$fb 0:mix=127; done
$B build/bbd/so_127_long.raw burst:440:16384:80 20 0:alley=127 0:fb=127 0:mix=127
$B build/bbd/so_127_short.raw burst:440:16384:80 20 0:alley=1 0:fb=127 0:mix=127 0:tone=127
# the headroom: one repeat (FEEDBK 0, 294 ms) of a 200 ms 1 kHz burst at -20, -12, -6, 0 dBFS, measured once the dry
# has stopped (dry + echo would clip the output at 0 dBFS and spoil the measurement)
for p in 3277 8231 16423 32767; do $B build/bbd/thd_$p.raw burst:1000:$p:200 1 0:alley=100 0:fb=0 0:mix=127 0:spread=127 0:tone=127; done
# the tapped time (500 ms: ALLEY 115 + FINE 66): when does the echo of an impulse arrive?
$B build/bbd/tapcheck.raw imp:16384 2 0:alley=115 0:fine=66 0:fb=0 0:mix=127 0:spread=127 0:tone=127
echo "renders -> build/bbd/"
