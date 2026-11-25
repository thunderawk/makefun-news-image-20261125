#!/usr/bin/env python3
"""Entrypoint: copy the rendered front page to the harness output dir.

Stdlib only. Verifies the PNG magic bytes and the 1 MiB size cap, then
prints the sha256 of the bytes it wrote, so a run can be checked.
"""
import hashlib
import os
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
# Output dir: argv[1] wins, else MAKEFUN_OUTPUT_DIR, else /output.
OUT_DIR = (sys.argv[1] if len(sys.argv) > 1
           else os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    with open(SRC, "rb") as fh:
        data = fh.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    if len(data) > 1 * 1024 * 1024:
        raise SystemExit("entry.png exceeds the 1 MiB cap: %d bytes"
                         % len(data))
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, "entry.png")
    with open(out, "wb") as fh:
        fh.write(data)
    print("entry.png %d bytes sha256 %s"
          % (len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
