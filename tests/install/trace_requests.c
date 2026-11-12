/* SPDX-License-Identifier: GPL-3.0-only */
/* The read requests the REAL device code sends, for the installer page's frame test (tests/install/run.sh).
 * It compiles firmware/src/ota.c (the running firmware's side, step 1) and firmware/loader/ldr_core.c (the update
 * loader, step 2) unchanged against a fake host that serves a package, and prints each request:
 *   trace_requests step1|write PACKAGE.fwsc          one line per request: "<flags> <addr> <len>"
 * "step1" = ota_session() (stage the loader, ask 0xE0000000), "write" = ldr_session() (the app area, ask 0xF0000000).
 * Same hooks and package reading as tests/ldr_test.c, whose flash model this copies. FM-1 board only. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FELUCCA_OTA_DRYRUN 0
#define FELUCCA_ID "ota-FM-1_900"
#define T_REC 0xE4F00u
static uint8_t nor[0x100000], *logical;
static size_t logical_len;
static uint8_t rx[1024];
static uint32_t rx_len, rx_full, now_ms;
static int commit_called;

static uint32_t pack7(const uint8_t *in, uint32_t n, uint8_t *out)
{
    uint32_t acc = 0, nb = 0, o = 0;
    while (n--) {
        acc |= (uint32_t)*in++ << nb;
        nb += 8;
        while (nb >= 7) { out[o++] = acc & 0x7F; acc >>= 7; nb -= 7; }
    }
    if (nb) out[o++] = acc & 0x7F;
    return o;
}
static uint32_t unpack7h(const uint8_t *in, uint32_t n, uint8_t *out)
{
    uint32_t acc = 0, nb = 0, o = 0;
    while (n--) {
        acc |= (uint32_t)*in++ << nb;
        nb += 7;
        if (nb >= 8) { out[o++] = (uint8_t)acc; acc >>= 8; nb -= 8; }
    }
    return o;
}

static int ota_wire_send(const uint8_t *p, uint32_t n)
{
    uint8_t u[64], m[600];
    uint32_t addr, len, i, s = 0;
    unpack7h(p + 1, n - 2, u);
    if (u[2] == 0x11) return 0;
    addr = u[7] | u[8] << 8 | u[9] << 16 | (uint32_t)u[10] << 24;
    len = u[11] | u[12] << 8 | u[13] << 16;
    printf("%u %u %u\n", u[6], addr, len);
    memcpy(m, "\x00\x59\x30", 3);
    m[3] = (uint8_t)(len + 8); m[4] = (uint8_t)((len + 8) >> 8); m[5] = 0; m[6] = u[6];
    memcpy(m + 7, &addr, 4);
    m[11] = (uint8_t)len; m[12] = (uint8_t)(len >> 8); m[13] = 0;
    if (addr >= 0xE0000000u) {
        memset(m + 14, 0, len);
        memcpy(m + 14, "success", 8);
    } else {
        if (addr + len > logical_len) { fprintf(stderr, "read past the package %#x\n", addr); exit(1); }
        memcpy(m + 14, logical + addr, len);
    }
    for (i = 6; i < 14 + len; i++) s += m[i];
    m[14 + len] = (uint8_t)~s;
    rx_len = pack7(m, 15 + len, rx);
    rx_full = 1;
    return 0;
}
static int ota_frame_get(const uint8_t **p, uint32_t *n) { if (!rx_full) return 0; *p = rx; *n = rx_len; return 1; }
static void ota_frame_done(void) { rx_full = 0; }
static uint32_t ota_now_ms(void) { return now_ms; }
static void ota_idle(void) { now_ms++; }
static int ota_erase(uint32_t off) { memset(nor + off, 0xFF, 0x1000); return 0; }
static int ota_prog(uint32_t off, const void *p, uint32_t n)
{
    const uint8_t *s = p;
    uint32_t i;
    for (i = 0; i < n; i++) nor[off + i] &= s[i];
    return 0;
}
static int ota_fread(uint32_t off, void *p, uint32_t n) { memcpy(p, nor + off, n); return 0; }
static void ota_show(uint32_t step, int32_t code) { (void)step; (void)code; }
static void ota_commit(const uint8_t *parm) { (void)parm; commit_called = 1; }
#include "../../firmware/src/ota.c"

static int ldr_fread(uint32_t off, void *p, uint32_t n) { memcpy(p, nor + off, n); return 0; }
static int ldr_erase(uint32_t off) { memset(nor + off, 0xFF, 0x1000); return 0; }
static int ldr_prog(uint32_t off, const void *p, uint32_t n)
{
    const uint8_t *s = p;
    uint32_t i;
    for (i = 0; i < n; i++) nor[off + i] &= s[i];
    return 0;
}
static void ldr_record_clear(void) {}
static int ldr_flash_known(void) { return 1; }
static void ldr_progress(uint32_t done, uint32_t total) { (void)done; (void)total; }
#include "../../firmware/loader/ldr_core.c"

static uint8_t *load_logical(const char *path, size_t *len)    /* the package without its 20 marker bytes */
{
    FILE *f = fopen(path, "rb");
    uint8_t *raw = malloc(0x200000), *lg;
    size_t n, i;
    if (!f) { perror(path); exit(2); }
    n = fread(raw, 1, 0x200000, f);
    fclose(f);
    lg = malloc(n);
    for (i = 0; i < 20; i++) memcpy(lg + i * 47, raw + i * 48, 47);
    memcpy(lg + 20 * 47, raw + 20 * 48, n - 20 * 48);
    *len = n - 20;
    free(raw);
    return lg;
}

int main(int argc, char **argv)
{
    uint32_t i, n, fo = 0;
    uint8_t h[0x400];
    int rc;
    if (argc < 3) { fprintf(stderr, "usage: trace_requests step1|write PACKAGE.fwsc\n"); return 2; }
    logical = load_logical(argv[2], &logical_len);
    memcpy(h, logical, sizeof h);
    ota_jl_enc(h, 0x40);
    n = ota_rd16(h + 8);
    for (i = 0; i < n; i++) {
        uint8_t *e = h + 0x40 + i * 0x50u;
        ota_jl_enc(e, 0x50);
        if (ota_rd16(e) == 0) fo = ota_rd32(e + 8);
    }
    memset(nor, 0xFF, sizeof nor);
    memcpy(nor, logical + fo, 0x93000u);        /* the device already runs this package: same head, same chip key */
    if (!strcmp(argv[1], "step1")) {
        rc = ota_session();
        fprintf(stderr, "ota_session rc %d (commit %s)\n", rc, commit_called ? "called" : "not called");
    } else {
        memset(nor + 0x4000, 0xA5, 0x1000);    /* one sector differs: it is rewritten */
        rc = ldr_session();
        fprintf(stderr, "ldr_session rc %d\n", rc);
    }
    return rc ? 1 : 0;
}
