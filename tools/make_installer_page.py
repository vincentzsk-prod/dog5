#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""Build the self-hosted installer page and the package it installs, together, so they cannot drift.

  tools/make_installer_page.py [--build] [--release X.Y] [--package FILE] [--date YYYY-MM-DD]
  tools/make_installer_page.py --check [--package FILE]

--build            run ./build.sh --release X.Y first (needs the JieLi toolchain + SDK, see README)
--release X.Y      the version (default 0.1): the package is build/dog5-X.Y.fwsc
--package FILE     use this package instead (default: build/dog5-X.Y.fwsc)
--date             the date in the file name and on the page (default: today)
--check            write nothing: regenerate in memory from the package beside the page (or --package FILE) and the
                   current web/install sources, and fail if docs/install/index.html or the .fwsc there differ

Writes, in docs/install/ (served by GitHub Pages from main /docs):
  dog5-X.Y-YYYYMMDD.fwsc   a copy of the package (any older dog5-*.fwsc there is removed)
  index.html               web/install/index.template.html with web/install/fm1install.js and the package
                           (base64) embedded: one file, no external request
The package is checked with the Python reference (tools/fm1_install.py load_package) before it is embedded; the page's
own JavaScript checks it again and compares it with the SHA-256 recorded here. tests/install/run.sh re-checks it all."""
import argparse
import base64
import datetime
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import fm1_install  # noqa: E402


def build_page(pkg_path, version, date):
    raw = Path(pkg_path).read_bytes()
    product, image = fm1_install.load_package(str(pkg_path), False)       # the Python reference's own checks
    name = f"dog5-{version}-{date.replace('-', '')}.fwsc"
    core = (ROOT / "web" / "install" / "fm1install.js").read_text(encoding="utf-8")
    assert "</script" not in core
    page = (ROOT / "web" / "install" / "index.template.html").read_text(encoding="utf-8")
    subst = {"{{VERSION}}": f"v{version}", "{{DATE}}": date, "{{PKG_NAME}}": name, "{{PRODUCT}}": product,
             "{{PKG_SHA256}}": hashlib.sha256(raw).hexdigest(), "{{PKG_BYTES}}": str(len(raw)),
             "{{PKG_B64}}": base64.b64encode(raw).decode("ascii")}
    page = page.replace("/*__FM1_JS__*/", core)
    for k, v in subst.items():
        assert k in page, k
        page = page.replace(k, v)
    return name, raw, page, product, image


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--release", default="0.1")
    ap.add_argument("--package")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    out = ROOT / "docs" / "install"
    if a.check:
        beside = sorted(out.glob("dog5-*.fwsc"))
        if len(beside) != 1:
            raise SystemExit(f"--check: expected one dog5-*.fwsc in docs/install, found {len(beside)}")
        m = re.fullmatch(r"dog5-(.+)-(\d{4})(\d{2})(\d{2})\.fwsc", beside[0].name)
        version, date = m[1], f"{m[2]}-{m[3]}-{m[4]}"
        pkg = Path(a.package) if a.package else beside[0]
        name, raw, page, product, image = build_page(pkg, version, date)
        bad = []
        if name != beside[0].name or raw != beside[0].read_bytes():
            bad.append("the package beside the page differs from " + str(pkg))
        if page != (out / "index.html").read_text(encoding="utf-8"):
            bad.append("docs/install/index.html differs from what web/install + the package generate")
        for b in bad:
            print("DRIFT:", b)
        if bad:
            raise SystemExit(1)
        print(f"in sync: {name} ({product}) and index.html regenerate byte for byte from web/install" + (f" and {pkg}" if a.package else ""))
        return
    if a.build:
        subprocess.run(["sh", str(ROOT / "build.sh"), "--release", a.release], check=True, cwd=ROOT)
    pkg = Path(a.package) if a.package else ROOT / "build" / f"dog5-{a.release}.fwsc"
    name, raw, page, product, image = build_page(pkg, a.release, a.date)
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("dog5-*.fwsc"):
        old.unlink()
    (out / name).write_bytes(raw)
    (out / "index.html").write_text(page, encoding="utf-8")
    print(f"package  docs/install/{name}  {len(raw)} B  identity {product}  sha256 {hashlib.sha256(raw).hexdigest()}")
    print(f"page     docs/install/index.html  {len(page.encode('utf-8'))} B")


if __name__ == "__main__":
    main()
