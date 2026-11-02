#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-only
# Instructions/sample on the host build, standing in for OBV_PERF (tests/host.c's perf_event_open path)
# where that can't run -- no hardware PMU exposed to the process, as in this project's cloud build
# containers (confirmed: perf_event_open there fails with ENOENT). Deterministic: valgrind's callgrind
# simulates the run instruction-by-instruction instead of sampling a hardware counter, so the same
# script gives the same count every time (OBV_PERF's hardware counter can vary a few % run to run).
# See dog5-docs/PERF-BASELINE.md for the measured baseline, what it means, and why it is a host-only
# relative yardstick, not the device number.
#
#   tests/perf_callgrind.sh [script]
#   BOARD=smk37 tests/perf_callgrind.sh [script]     the SMK-37 build, same as tests/run_host.sh
set -e
cd "$(dirname "$0")/.."
mkdir -p build/host
N=obervave; D=
if [ "${BOARD:-fm1}" = smk37 ]; then N=obervave-smk37; D=-DBOARD_SMK37=1; fi
cc -O2 -Wall -Wno-unused-function -DOBV_HOST -DOBV_CALLGRIND $D -DAPP_VER="\"${APP_VER:-dev}\"" \
   -Ifirmware/src -Ifirmware/gen -o "build/host/$N-cg" firmware/src/obervave.c
valgrind --tool=callgrind --collect-atstart=no --combine-dumps=yes \
   --callgrind-out-file="build/host/$N-cg-callgrind.out" \
   "build/host/$N-cg" "build/host/$N-cg" ${1:+"$1"} 2>&1 | grep -E "callgrind frames|I +refs"
