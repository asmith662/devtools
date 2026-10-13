# Copyright (c) 2026
# ruff: noqa: ANN401 -- historical external encoding boundary
"""Exact base85 decoding; optionally use the already-installed NumPy substrate."""

from __future__ import annotations

import base64
import importlib
from typing import Any


def decoder() -> Any:
    """Choose once per invocation, without adding a dependency or trusted cache."""
    try:
        numpy = importlib.import_module("numpy")
    except ImportError:
        return base64.b85decode
    alphabet = (
        b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        b"!#$%&()*+-;<=>?@^_`{|}~"
    )
    invalid = 255
    maximum_word = 0xFFFFFFFF
    table = numpy.full(256, invalid, dtype=numpy.uint64)
    for ordinal, value in enumerate(alphabet):
        table[value] = ordinal
    weights = numpy.array([85**4, 85**3, 85**2, 85, 1], dtype=numpy.uint64)

    def decode(encoded: bytes) -> bytes:
        padding = (-len(encoded)) % 5
        digits = table[numpy.frombuffer(encoded + b"~" * padding, dtype=numpy.uint8)]
        if numpy.any(digits == invalid):
            return base64.b85decode(encoded)  # preserve historical invalid-input error
        words = (digits.reshape(-1, 5) * weights).sum(axis=1)
        if numpy.any(words > maximum_word):
            return base64.b85decode(encoded)
        raw = bytes(words.astype(">u4").tobytes())
        return raw[:-padding] if padding else raw

    return decode
