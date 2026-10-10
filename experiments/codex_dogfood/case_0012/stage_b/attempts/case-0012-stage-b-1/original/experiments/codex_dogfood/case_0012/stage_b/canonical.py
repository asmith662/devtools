# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003 -- formatter owns commas; frozen JSON boundary
"""Stream exactly the frozen canonical native JSON, avoiding graph expansion in RAM."""

from __future__ import annotations

import gzip
import hashlib
import io
import json
from contextlib import AbstractContextManager, contextmanager
from dataclasses import fields, is_dataclass
from enum import Enum
from pathlib import PurePath
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterator

from devtools.core.identity import Identity
from experiments.exact_hint_routing import behavior


class NativeEncoder(json.JSONEncoder):
    """Defer dataclass child projection to the standard JSON encoder traversal."""

    def default(self, value: object) -> Any:  # noqa: ANN401 -- native JSON boundary
        """Match frozen serialization.project at each native value boundary."""
        if isinstance(value, Identity):
            return str(value)
        if isinstance(value, PurePath):
            return value.as_posix()
        if isinstance(value, Enum):
            return value.value
        if is_dataclass(value) and not isinstance(value, type):
            return {f.name: getattr(value, f.name) for f in fields(value)}
        raise TypeError("Unsupported native serialization type")


def chunks(value: object) -> Iterator[str]:
    """Emit exact sorted/ASCII/indent-two JSON with the frozen final newline."""
    yield from NativeEncoder(ensure_ascii=True, sort_keys=True, indent=2).iterencode(
        value
    )
    yield "\n"


def native_hash(value: object) -> dict[str, str]:
    """Hash the same bytes as frozen encode(value), without materializing them."""
    h = hashlib.sha256()
    for chunk in chunks(value):
        h.update(chunk.encode())
    return {
        "native_type": type(value).__module__ + "." + type(value).__qualname__,
        "canonical_sha256": h.hexdigest(),
    }


def compressed(value: object) -> bytes:
    """Deterministic gzip stream for complete native resolution evidence."""
    stream = io.BytesIO()
    with gzip.GzipFile(fileobj=stream, mode="wb", mtime=0, filename="") as archive:
        for chunk in chunks(value):
            archive.write(chunk.encode())
    return stream.getvalue()


def projection_adapter() -> AbstractContextManager[None]:
    """Install byte-equivalent identities in the frozen comparison projection."""

    @contextmanager
    def installed() -> Iterator[None]:
        original = behavior._native  # noqa: SLF001 -- exact private frozen identity adapter
        cache: dict[int, tuple[object, dict[str, str]]] = {}

        def identity(value: object) -> dict[str, str]:
            hit = cache.get(id(value))
            if hit is not None and hit[0] is value:
                return hit[1]
            result = native_hash(value)
            cache[id(value)] = (value, result)
            return result

        behavior._native = identity  # noqa: SLF001
        try:
            yield
        finally:
            behavior._native = original  # noqa: SLF001

    return installed()
