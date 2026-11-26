"""Entrypoint for the news-image-20261125 V2 entry.

Reads the entry.png shipped in this repository, checks it is a real
PNG of the right size and under the 1 MiB cap, then copies it to the
output directory. Standard library only, no network, no clock, so
two runs write identical bytes.
"""

import os
import shutil
import struct
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
MAX_SIDE = 1024


def inspect_png(path):
    """Return (width, height, size) or raise ValueError on a bad file."""
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise ValueError("entry.png is %d bytes, over the 1 MiB cap"
                         % size)
    with open(path, "rb") as handle:
        head = handle.read(33)
    if head[:8] != PNG_MAGIC:
        raise ValueError("entry.png is not a PNG (bad magic bytes)")
    if head[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk where expected")
    width, height = struct.unpack(">II", head[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError("entry.png is %dx%d, over the 1024x1024 cap"
                         % (width, height))
    return width, height, size


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    width, height, size = inspect_png(source)
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    print("entry.png %dx%d %d bytes -> %s" % (width, height, size, target))


if __name__ == "__main__":
    main()
