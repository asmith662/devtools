# Copyright (c) 2026
# ruff: noqa: EM101, TRY003 -- explicit serialization boundary errors
"""Explicit deterministic experiment projection, retaining native provenance."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from enum import Enum
from pathlib import PurePath
from typing import Any

from devtools.core.identity import Identity
from experiments.codex_dogfood.case_0009.artifacts import json_bytes


def project(value: object) -> Any:  # noqa: ANN401, PLR0911 -- recursive JSON boundary
    """Project immutable native/experimental values; reject opaque repr fallback."""
    if isinstance(value, Identity):
        return str(value)
    if isinstance(value, PurePath):
        return value.as_posix()
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value) and not isinstance(value, type):
        return {f.name: project(getattr(value, f.name)) for f in fields(value)}
    if isinstance(value, tuple | list):
        return [project(v) for v in value]
    if isinstance(value, dict):
        if any(not isinstance(k, str) for k in value):
            raise TypeError("Serialization requires string dictionary keys")
        return {k: project(v) for k, v in value.items()}
    if value is None or isinstance(value, str | int | float | bool):
        return value
    raise TypeError("Unsupported experiment serialization type")


def encode(value: object) -> bytes:
    """Use the established canonical JSON substrate."""
    return json_bytes(project(value))
