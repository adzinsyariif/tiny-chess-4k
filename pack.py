#!/usr/bin/env python3
"""Pack engine.py into main.py so the whole engine fits the 4,096-byte limit.

The competition counts main.py as committed, and explicitly allows an
lzma/zlib compressed payload with a short unpacker (the house baseline,
sunfish NNUE 4K, ships exactly this way). This script compresses engine.py
with lzma (FORMAT_ALONE, tuned lc/lp/pb) and base85-encodes it behind a
two-line unpacker. Deterministic: same input, same output.
"""
import base64
import lzma
import pathlib

HERE = pathlib.Path(__file__).parent
src = (HERE / "engine.py").read_bytes()
filters = [{"id": lzma.FILTER_LZMA1, "dict_size": 1 << 24, "lc": 0, "lp": 0, "pb": 0}]
comp = lzma.compress(src, format=lzma.FORMAT_ALONE, filters=filters)
main = (
    b"import lzma,base64\n"
    b"exec(lzma.decompress(base64.b85decode(b'"
    + base64.b85encode(comp)
    + b"'),format=lzma.FORMAT_ALONE))\n"
)
(HERE / "main.py").write_bytes(main)
print(f"engine.py {len(src)} bytes -> main.py {len(main)} bytes (limit 4096)")
