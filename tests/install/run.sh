#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-only
# The installer page's proof without a device (what it does and does not show: docs/install/README.md):
#   1. the page and package beside it regenerate byte for byte from web/install + the package (no drift)
#   2. the REAL device code (firmware/src/ota.c, firmware/loader/ldr_core.c) is run on the host and its read requests
#      recorded (trace_requests.c): 23 for step 1, 1180 for the loader's write pass
#   3. Python reference (tools/fm1_install.py) and the page's JavaScript answer those requests and whole install
#      sessions; every frame and every host->device byte must be identical (py_side.py, js_side.mjs)
#   4. headless Chromium drives the page itself against a fake WebMIDI unit (page_e2e.mjs; skipped without Playwright)
# usage: tests/install/run.sh [PACKAGE.fwsc]     (default: the package beside the page)
set -e
cd "$(dirname "$0")/../.."
OUT="${OUT:-build/install-test}"
mkdir -p "$OUT"
PKG="${1:-$(ls docs/install/dog5-*.fwsc)}"
python3 tools/make_installer_page.py --check ${1:+--package "$1"}
cc -O1 -Wall -Wno-unused-function -o "$OUT/trace_requests" tests/install/trace_requests.c
"$OUT/trace_requests" step1 "$PKG" > "$OUT/step1.txt"
"$OUT/trace_requests" write "$PKG" > "$OUT/write.txt"
echo "device code: $(wc -l < "$OUT/step1.txt") step-1 requests, $(wc -l < "$OUT/write.txt") loader requests"
python3 tests/install/py_side.py "$PKG" "$OUT/step1.txt" "$OUT/write.txt" "$OUT/py.json"
node tests/install/js_side.mjs "$OUT/py.json" docs/install/index.html web/install/fm1install.js
if node -e 'require("playwright")' 2>/dev/null; then
    node tests/install/page_e2e.mjs "$OUT/py.json" docs/install "$OUT/page.png"
else
    echo "page_e2e: skipped (no Playwright)"
fi
