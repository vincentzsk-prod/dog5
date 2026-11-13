#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-only
# DØG-5 in the browser: the firmware's sources (unchanged) + web/sim/sim.c -> WebAssembly, plus the page.
#   sh web/sim/build.sh [OUTDIR]   ->  docs/play/{index.html, sim.js, sim.css, worklet.js, dog5.wasm, patches.json}
#   then: python3 -m http.server -d docs/play 8737   and open http://localhost:8737
# (Forked from OberVave's simulator, which followed Makkuro37's web/sim by M. Geisler and winampFM's by hericdk, GPL-3.0.
#  The stale OberVave build stays in tests/ref-sim/ as provenance; this script never writes there.)
# Tools (once, nothing system-wide, nothing installed by this script; the paths can be overridden with ZIG= / WASM_OPT=):
#   zig cc (wasm32-freestanding), the pip package ziglang:
#     python3 -m venv ~/.local/share/obervave-wasm && ~/.local/share/obervave-wasm/bin/pip install ziglang
#   Binaryen's wasm-opt (Asyncify: the main loop never returns, so it runs as a coroutine; see sim.c). Found on PATH, as
#   $WASM_OPT, in ~/.local/share/obervave-wasm/binaryen-*/bin/ (a release tarball) or the npm package (tested: 132):
#     npm install --prefix ~/.local/share/obervave-wasm/npm binaryen
set -e
cd "$(dirname "$0")/../.."
OUT="${1:-docs/play}"
T="$HOME/.local/share/obervave-wasm"
NEED=0
if [ -z "$ZIG" ]; then
    if [ -x "$T/bin/python" ] && "$T/bin/python" -c "import ziglang" 2>/dev/null; then ZIG="$T/bin/python -m ziglang"
    elif command -v zig >/dev/null 2>&1; then ZIG=zig
    else
        echo "sim: no zig. Get it with:"
        echo "  python3 -m venv ~/.local/share/obervave-wasm"
        echo "  ~/.local/share/obervave-wasm/bin/pip install ziglang"
        NEED=1
    fi
fi
if [ -z "$WASM_OPT" ]; then
    WASM_OPT=$(ls -d "$T"/binaryen-*/bin/wasm-opt 2>/dev/null | sort | tail -n 1)
    [ -n "$WASM_OPT" ] || WASM_OPT=$(command -v wasm-opt || true)
    [ -n "$WASM_OPT" ] || { [ -x "$T/npm/node_modules/.bin/wasm-opt" ] && WASM_OPT="$T/npm/node_modules/.bin/wasm-opt"; }
    if [ -z "$WASM_OPT" ]; then
        echo "sim: no wasm-opt. Get it with:"
        echo "  mkdir -p ~/.local/share/obervave-wasm/npm"
        echo "  npm install --prefix ~/.local/share/obervave-wasm/npm binaryen"
        NEED=1
    fi
fi
[ "$NEED" = 0 ] || exit 1
mkdir -p build/sim "$OUT"
nice -n 15 $ZIG cc --target=wasm32-freestanding -mcpu=generic+bulk_memory -O2 -fno-builtin -ffreestanding -nostdlib \
    -Wall -Wno-unused-function -Wno-unused-variable -Wno-unused-but-set-variable \
    -Ifirmware/src -Ifirmware/gen \
    -Wl,--no-entry -Wl,--export-memory -Wl,--export-dynamic -Wl,-z,stack-size=262144 \
    -o build/sim/raw.wasm web/sim/sim.c
nice -n 15 "$WASM_OPT" build/sim/raw.wasm --enable-bulk-memory --asyncify -O2 --strip-debug --strip-producers \
    -o "$OUT/dog5.wasm"
cp web/sim/index.html web/sim/sim.js web/sim/sim.css web/sim/worklet.js "$OUT/"
python3 web/sim/gen_patches.py "$OUT/patches.json"
echo "sim: $OUT ($(wc -c < "$OUT/dog5.wasm" | tr -d ' ') B wasm)"
