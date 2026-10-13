# Copyright (c) 2026
# ruff: noqa: ANN401, PLR2004, COM812, EM101, TRY003 -- bounded external byte grammar
"""Exact literal-reference scanning in the authenticated canonical byte grammar."""

from __future__ import annotations

import re
from hashlib import sha256
from typing import Any


def template(numpy: Any, raw: bytes) -> tuple[bytes, Any]:
    """Compile exact constant bytes and reference slots from a proven block."""
    del numpy
    pattern = re.compile(rb'"ref": ([0-9]+)')
    parts = []
    start = 0
    for match in pattern.finditer(raw):
        parts.append(raw[start : match.start(1)])
        start = match.end(1)
    parts.append(raw[start:])
    return b"", tuple(parts)


def render(
    numpy: Any, base: bytes, positions: Any, values: Any, ordinal_bytes: Any = None
) -> bytes:
    """Render only exact decimal reference bindings; constant content is reused."""
    del base
    if not len(values):
        return b"".join(positions)
    if ordinal_bytes is None:
        lengths = 1 + numpy.searchsorted(
            [10**i for i in range(1, 19)], values, side="right"
        )
        encoded = values.astype(f"S{int(lengths.max())}").tolist()
    else:
        encoded = ordinal_bytes[values].tolist()
    pieces = [b""] * (2 * len(values) + 1)
    pieces[::2] = positions
    pieces[1::2] = encoded
    return b"".join(pieces)


def surface(numpy: Any, raw: bytes, *, normalized: bool) -> tuple[Any, bytes | None]:
    """Match the historical regex and optionally hash its exact replacement.

    Scan overlapping uint64 windows in bounded chunks. NumPy only accelerates
    byte operations; it does not infer domain identity or authenticate content.
    """
    pattern = b'"ref": '
    literal = int.from_bytes(pattern, "little")
    mask = (1 << 56) - 1
    starts = []
    limit = max(0, len(raw) - 7)
    chunk = 1024 * 1024
    for offset in range(0, limit, chunk):
        count = min(chunk, limit - offset)
        words = numpy.ndarray(
            (count,), dtype="<u8", buffer=raw, offset=offset, strides=(1,)
        )
        matches = numpy.flatnonzero((words & mask) == literal)
        if len(matches):
            starts.append(matches + offset + len(pattern))
    positions = (
        numpy.concatenate(starts) if starts else numpy.empty(0, dtype=numpy.int64)
    )
    data = numpy.frombuffer(raw, dtype=numpy.uint8)
    first = data[positions]
    positions = positions[(first >= 48) & (first <= 57)]
    values = numpy.zeros(len(positions), dtype=numpy.int64)
    lengths = numpy.zeros(len(positions), dtype=numpy.int64)
    active = numpy.ones(len(positions), dtype=bool)
    for column in range(19):
        digits = data[numpy.minimum(positions + column, len(raw) - 1)]
        active &= (digits >= 48) & (digits <= 57)
        if not numpy.any(active):
            break
        old = values[active]
        digit = digits[active].astype(numpy.int64) - 48
        if numpy.any(old > (0x7FFFFFFFFFFFFFFF - digit) // 10):
            raise ValueError("Canonical reference ordinal exceeds native graph bounds")
        values[active] = old * 10 + digit
        lengths += active
    else:
        digits = data[numpy.minimum(positions + 19, len(raw) - 1)]
        if numpy.any(active & (digits >= 48) & (digits <= 57)):
            raise ValueError("Canonical reference ordinal exceeds native graph bounds")
    if not normalized:
        return values, None
    selected = numpy.ones(len(raw), dtype=bool)
    output = data.copy()
    output[positions] = 64  # '@': exactly the historical regex replacement
    for column in range(1, int(lengths.max()) if len(lengths) else 1):
        selected[positions[lengths > column] + column] = False
    digest = sha256(output[selected].tobytes()).digest()
    return values, digest
