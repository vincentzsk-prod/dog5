#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-only
# Fetch the JieLi toolchain + AC79 SDK from our own GitHub Release instead of
# pkgman.jieliapp.com / gitee.com. Faster, and works even if those hosts are
# unreachable from a cloud environment. Unpacks to the same paths
# tools/get_toolchain.sh and build.sh already expect.
#   tools/get_vendored_deps.sh [DEST_TOOLCHAIN] [DEST_SDK]
#   DEST_TOOLCHAIN   default: ~/.jieli      (toolchain symlink lands at $DEST_TOOLCHAIN/toolchain)
#   DEST_SDK         default: ~/fw-AC79_AIoT_SDK
set -e

RELEASE_BASE="https://github.com/vincentzsk-prod/dog5/releases/download/build-deps-v1"
TOOLCHAIN_ASSET="jieli-linux-toolchain-20260730.1.tar.xz"
SDK_ASSET="fw-AC79_AIoT_SDK-AC79NN_SDK_V1.2.1_2023-12-13.tar.xz"

DEST_TOOLCHAIN="${1:-$HOME/.jieli}"
DEST_SDK="${2:-$HOME/fw-AC79_AIoT_SDK}"

mkdir -p "$DEST_TOOLCHAIN"
curl -fL --retry 3 "$RELEASE_BASE/$TOOLCHAIN_ASSET" | tar -xJ -C "$DEST_TOOLCHAIN"
TC="$(ls -d "$DEST_TOOLCHAIN"/jieli-linux-toolchains-* | sort | tail -1)"
ln -sfn "$(basename "$TC")" "$DEST_TOOLCHAIN/toolchain"
echo "JIELI_TOOLCHAIN=$DEST_TOOLCHAIN/toolchain ($(basename "$TC"))"

SDK_STAGE="$(mktemp -d)"
curl -fL --retry 3 "$RELEASE_BASE/$SDK_ASSET" | tar -xJ -C "$SDK_STAGE"
rm -rf "$DEST_SDK"
mv "$SDK_STAGE"/* "$DEST_SDK"
rmdir "$SDK_STAGE"
echo "AC79_SDK=$DEST_SDK"
