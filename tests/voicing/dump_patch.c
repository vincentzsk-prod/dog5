/* SPDX-License-Identifier: GPL-3.0-only */
/* Print factory patches as resolved by the firmware's own tables (defaults + the patch's overrides): a test tool for the
 * voicing batches, it includes the parameter table and the patch list and nothing of the engine.
 *   cc -Ifirmware/src -Ifirmware/gen -o build/voicing/dump_patch tests/voicing/dump_patch.c
 *   build/voicing/dump_patch 3        full list of slot 3 (1-based), "id name value" lines + the name
 *   build/voicing/dump_patch all      one line per slot: name and a hash of the 96 patch bytes (the byte-identical check) */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "obv_params.h"
#include "obv_patches.h"

static uint32_t fnv(const uint8_t *b, uint32_t n)
{
    uint32_t h = 2166136261u;
    while (n--) h = (h ^ *b++) * 16777619u;
    return h;
}

int main(int argc, char **argv)
{
    patch_t p;
    uint32_t n, i;
    if (argc > 1 && !strcmp(argv[1], "all")) {
        for (n = 0; n < NFACT; n++) {
            patch_from_factory(&p, &FACTORY[n]);
            printf("%02u %-14s %08x\n", n + 1u, FACTORY[n].name, fnv(p.v, PATCH_BYTES));
        }
        return 0;
    }
    n = argc > 1 ? (uint32_t)atoi(argv[1]) - 1u : 2u;
    patch_from_factory(&p, &FACTORY[n]);
    for (i = 0; i < NPARAM; i++)
        printf("%2u %-8s %3u%s\n", i, PDEF[i].name, p.v[i], p.v[i] != PDEF[i].def ? "  *" : "");
    printf("name \"%.14s\"\n", (const char *)&p.v[PATCH_NAME_AT]);
    return 0;
}
