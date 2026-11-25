#!/usr/bin/env python3
"""Copy the rendered front page to the grading output directory.

Reads entry.png next to this file, checks it is a real PNG under the
1 MiB cap, then writes it to /output/entry.png (or the directory given
as the first argument). Stdlib only, no network.
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024
EXPECT_W, EXPECT_H = 1024, 1024


def png_size(path):
    """Read width/height from the PNG IHDR chunk (stdlib only)."""
    with open(path, "rb") as fh:
        data = fh.read(33)
    if data[:8] != PNG_MAGIC or data[12:16] != b"IHDR":
        return None
    w, h = struct.unpack(">II", data[16:24])
    return w, h


def main():
    dest_dir = sys.argv[1] if len(sys.argv) > 1 else "/output"
    if not os.path.isfile(SRC):
        print("missing:", SRC)
        return 1
    with open(SRC, "rb") as fh:
        head = fh.read(len(PNG_MAGIC))
    if head != PNG_MAGIC:
        print("not a PNG:", SRC)
        return 1
    size = os.path.getsize(SRC)
    if size > MAX_BYTES:
        print("over 1 MiB cap:", size, "bytes")
        return 1
    dims = png_size(SRC)
    if dims != (EXPECT_W, EXPECT_H):
        print("unexpected dimensions:", dims)
        return 1
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    print("wrote", dest, size, "bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
