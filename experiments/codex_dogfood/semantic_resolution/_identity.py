# Copyright (c) 2026
# ruff: noqa: COM812
"""Case-independent experiment fingerprints, never production semantic identities."""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Mapping
from dataclasses import fields, is_dataclass
from enum import Enum
from pathlib import PurePath
from uuid import UUID


def canonical(value: object) -> bytes:
    """Encode finite JSON data deterministically without textual repr fallback."""
    return (
        json.dumps(
            value,
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def digest(value: object) -> str:
    """Fingerprint exact retained values, preserving native type distinctions."""
    return json_digest(_native(value))


def json_digest(value: object) -> str:
    """Hash canonical JSON payload bytes, including their final newline."""
    return hashlib.sha256(canonical(value)).hexdigest()


def text_digest(value: str) -> str:
    """Hash excerpt/definition bytes; native resource identities remain opaque."""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def native_descriptor(value: object) -> object:
    """Describe caller provenance without loading arbitrary native classes on replay."""
    return _native(value)


def _native(value: object) -> object:  # noqa: PLR0911 - explicit native type dispatch
    if isinstance(value, Enum):
        return {"type": _type(value), "value": _native(value.value)}
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float) and math.isfinite(value):
        return value
    if isinstance(value, (UUID, PurePath)):
        return {"type": _type(value), "value": str(value)}
    if is_dataclass(value) and not isinstance(value, type):
        return {
            "type": _type(value),
            "fields": {
                field.name: _native(getattr(value, field.name))
                for field in fields(value)
            },
        }
    if isinstance(value, (tuple, list)):
        return {type(value).__name__: [_native(item) for item in value]}
    if isinstance(value, frozenset):
        return {"frozenset": sorted((_native(item) for item in value), key=canonical)}
    if isinstance(value, Mapping):
        return {
            "mapping": sorted(
                ([_native(key), _native(item)] for key, item in value.items()),
                key=canonical,
            )
        }
    msg = f"Unsupported experiment fingerprint value: {_type(value)}."
    raise TypeError(msg)


def _type(value: object) -> str:
    return f"{type(value).__module__}.{type(value).__qualname__}"


def require_text(*values: str) -> None:
    """Reject missing or blank caller text rather than guessing semantics."""
    if any(not isinstance(value, str) or not value.strip() for value in values):
        msg = "Expected nonblank text."
        raise ValueError(msg)
