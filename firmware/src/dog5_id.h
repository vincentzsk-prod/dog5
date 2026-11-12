/* SPDX-License-Identifier: GPL-3.0-only */
/* DØG-5's identity, in ONE place (12 Nov 2026). Everything that names the product comes from here: the app
 * (platform.c, obv_ui.h), the update loader's screen (loader/ldr_screen.c), the host test (tests/host.c) and,
 * through tools/build.py which READS the #define lines below, the package identity and the package file names.
 * To change the identity later (the artwork batch), edit this file only; keep each #define on one line with a
 * plain "string" value, because tools/build.py parses them.
 *
 * DOG5_NAME is what the screens show. The Ø is the panel font's byte 0xD8 (FONT_S has it, FONT_L does not; the
 * update loader's own letters do not either), written as "\xD8" because gfx.c indexes bytes, not UTF-8.
 * DOG5_NAME_ASCII is for a place that cannot draw it. DOG5_NAME_LOADER is the update loader's screen: its own 5 x 7
 * letters are capitals and digits only (no hyphen, no Ø), so it reads "DOG 5" there.
 * DOG5_ID_FM1 / DOG5_ID_SMK: the package identity is this + the release's minor digit (tools/build.py), so the FM-1
 * is "FM-1_96N": family 96, N = minor version (a dev build is N = 0). Nothing in the updater reads those two digits;
 * see docs/install/README.md.
 * DOG5_PACKAGE: the .fwsc file name stem (dog5-X.Y.fwsc). */
#define DOG5_NAME "D\xD8G-5"
#define DOG5_NAME_ASCII "DOG-5"
#define DOG5_NAME_LOADER "DOG 5"
#define DOG5_ID_FM1 "FM-1_96"
#define DOG5_ID_SMK "SMK-37 Pro_96"
#define DOG5_PACKAGE "dog5"
