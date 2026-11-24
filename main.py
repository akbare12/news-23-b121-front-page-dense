#!/usr/bin/env python3
"""news-23 b121 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
Validates the PNG by parsing its header manually with struct.
"""
import hashlib
import os
import struct
import sys
import zlib


def fail(msg):
    print("error:", msg, file=sys.stderr)
    sys.exit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    if out_dir_abs == here or out_dir_abs.startswith(here + os.sep):
        fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    if os.path.isfile(out_dir_abs):
        fail("MAKEFUN_OUTPUT_DIR is a file, not a directory")
    dst = os.path.join(out_dir_abs, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(src):
        fail("output would overwrite the source image")

    try:
        with open(src, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        fail("cannot read %s: %s" % (src, exc))

    if len(data) < 10000:
        fail("entry.png too small: %d bytes" % len(data))
    if len(data) > 1024 * 1024:
        fail("entry.png too big: %d bytes (limit 1 MiB)" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("bad PNG signature")

    # Walk the chunks. Layout after the 8-byte signature: each chunk is
    # 4-byte length + 4-byte type + <length> bytes data + 4-byte CRC
    # (12 bytes of framing around the payload). First must be IHDR.
    pos = 8
    if len(data) < pos + 8:
        fail("truncated chunk header")
    (length,) = struct.unpack(">I", data[pos:pos + 4])
    ctype = data[pos + 4:pos + 8]
    if ctype != b"IHDR" or length != 13:
        fail("first chunk must be a 13-byte IHDR")
    ihdr = data[pos + 8:pos + 21]
    width, height, depth, ctype_code, comp, filt, inter = struct.unpack(
        ">IIBBBBB", ihdr)
    if (width, height) != (1024, 1024):
        fail("expected 1024x1024, got %dx%d" % (width, height))
    if depth != 8 or ctype_code not in (2, 6):
        fail("expected 8-bit RGB/RGBA, got depth=%d type=%d" % (depth, ctype_code))
    if comp != 0 or filt != 0 or inter != 0:
        fail("unexpected PNG compression/filter/interlace flags")
    crc_stored = struct.unpack(">I", data[pos + 21:pos + 25])[0]
    crc_calc = zlib.crc32(b"IHDR" + ihdr) & 0xFFFFFFFF
    if crc_stored != crc_calc:
        fail("IHDR CRC mismatch")

    pos += 12 + length
    idat_total = 0
    seen_iend = False
    while pos + 8 <= len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        if pos + 12 + length > len(data):
            fail("truncated chunk %r" % ctype)
        crc_stored = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])[0]
        crc_calc = zlib.crc32(data[pos + 4:pos + 8 + length]) & 0xFFFFFFFF
        if crc_stored != crc_calc:
            fail("CRC mismatch in chunk %r" % ctype)
        if ctype == b"IDAT":
            if length == 0:
                fail("empty IDAT chunk")
            idat_total += length
        if ctype == b"IEND":
            if length != 0:
                fail("IEND must be empty")
            if pos + 12 + length != len(data):
                fail("trailing data after IEND")
            seen_iend = True
            break
        pos += 12 + length
    if not seen_iend:
        fail("missing IEND chunk")
    if idat_total < 1000:
        fail("IDAT payload too small: %d bytes" % idat_total)

    os.makedirs(out_dir_abs, exist_ok=True)
    with open(dst, "wb") as fh:
        fh.write(data)
    with open(dst, "rb") as fh:
        back = fh.read()
    if back != data:
        fail("output does not match source byte-for-byte")
    print("wrote %s (%d bytes, sha256 %s)"
          % (dst, len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
