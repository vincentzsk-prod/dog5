# DØG-5 on the M-Vave SMK-37: not supported

DØG-5 is made and tested for the **M-VAVE FM-1 only**. The SMK-37 board code inherited from OberVave (the port by
M. Geisler, see `LICENSING.md`) is still in the source and its host tests still run, but since Batch 12B (18 Nov 2026)
**no SMK-37 packages are built or published**: no DØG-5 build has ever run on an SMK-37, and the SMK's pad grid was
OberVave's step sequencer, which DØG-5 removed. The code will be taken out in a later firmware clean-up.

OberVave's own SMK-37 guide (this file before Batch 12B) is in the git history and upstream at
[zvenson/obervave](https://github.com/zvenson/obervave). `smk37-port.yaml` records that port's decisions and goes with
the code.
