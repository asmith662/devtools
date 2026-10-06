# Copyright (c) 2026
# ruff: noqa: ANN401 -- JSON boundary of experimental diagnostic artifacts
"""Stable finite JSON encoding for diagnostic projections, never object reprs."""

from __future__ import annotations

import json
from typing import Any


def encode(value: Any) -> bytes:
    """Encode explicit projections as sorted ASCII JSON with a final newline."""
    return (
        json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2, allow_nan=False)
        + "\n"
    ).encode("utf-8")
