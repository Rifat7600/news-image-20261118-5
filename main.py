#!/usr/bin/env python3
"""Entry program: copy the bundled front-page image to the output dir.

Standard library only. Reads entry.png from this script's own folder
and writes it byte-for-byte to $MAKEFUN_OUTPUT_DIR/entry.png
(default /output/entry.png). Deterministic: same input, same output.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    print("wrote", target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
