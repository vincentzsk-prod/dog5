# DØG-5

**Custom firmware for the M-VAVE FM-1 pocket synth, for the band DØGS.** An aggressive, live, virtual-analog voice (8
voices, a Psych Chain of GROWL / ALLEY / DRAIN / CHEW after them, 99 program slots with 32 factory patches). Free and
open source, GPL-3.0-only. The build brief and the reasoning are in [`CLAUDE.md`](CLAUDE.md) and [`dog5-docs/`](dog5-docs/).

> **Status (18 Nov 2026): a pre-release test build, v0.2, package identity `FM-1_962`**, flashed and played on a real
> FM-1. Made and tested for the **FM-1 only** (the SMK-37 is not supported: [`SMK37.md`](SMK37.md)).

**Install it:** the self-hosted installer page, [`docs/install/`](docs/install/README.md) (Chrome or Edge, over USB:
<https://vincentzsk-prod.github.io/dog5/install/>). It carries the package inside
the page, shows what it will write, has a dry run, and resumes an interrupted install. From a terminal:
`python3 tools/fm1_install.py docs/install/dog5-0.2-20261118.fwsc`. If the unit will not boot: M-Flasher and your backup.

**Build it:** `./build.sh --release 0.2` makes `build/dog5-0.2.fwsc` (identity `FM-1_962`; a dev build is `build/dog5.fwsc`,
`FM-1_960`); `python3 tools/make_installer_page.py --release 0.2` regenerates the installer page and its package together.
The product's name and identity live in one file, [`firmware/src/dog5_id.h`](firmware/src/dog5_id.h).

**Play it in your browser:** <https://vincentzsk-prod.github.io/dog5/play/> is the firmware itself (the same C sources,
compiled to WebAssembly). Rebuild it with `sh web/sim/build.sh` (the two tools it needs are listed in that script).

**Test it:** a plain `./build.sh` last, then `sh tests/run_tests.sh` (host app, program store, update path, browser player,
installer page; no hardware). `CLAUDE.md` §9 has the whole dev setup.

**Credits.** DØG-5 by ZIGGY (DØGS). **DØG-5 is a fork of OberVave v1.5.3 (pinned)** by
[zvenson](https://github.com/zvenson/obervave) (`zvenson/obervave`, tag `v1.5.3`, commit `7e1ccf9`), which stands on
[Dinghy](https://github.com/zvenson/dinghy), [Felucca](https://github.com/hugelton/Felucca) (Leo Kuroshita, Hügelton
Instruments) and [SLOOP](https://github.com/isod89/sloop-fm1) (isod89). Everything inherited keeps its copyright and
licence; see [`NOTICE`](NOTICE), [`LICENSING.md`](LICENSING.md) and [`LICENSE`](LICENSE) (GPL-3.0-only).

OberVave's own README (the base this was forked from) is upstream at
[`zvenson/obervave@v1.5.3`](https://github.com/zvenson/obervave/tree/v1.5.3) and in this repo's git history.
