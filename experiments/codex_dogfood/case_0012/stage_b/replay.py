# Copyright (c) 2026
# ruff: noqa: COM812, ANN401, EM101, TRY003, T201, E501 -- bounded publication reader
"""Byte-equivalent memoized canonical hashing for immutable captured statistics.

Producer source remains pinned and unchanged. This reader calls finalization or
verification only. It never resolves, retrieves, presents or constructs arms.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterator
from devtools.context.retrieval.lexical.statistics import (
    RepositoryTextLexicalDocumentStatistics,
)
from experiments.codex_dogfood.case_0009.artifacts import (
    binary,
    digest,
    json_bytes,
    put_text,
    read_json,
)
from experiments.codex_dogfood.case_0012.stage_b import canonical, execute


def fast_hash(value: object) -> dict[str, str]:  # noqa: C901 -- exact bounded encoder
    """Hash exactly frozen canonical JSON, caching bounded immutable fragments."""
    cache: dict[tuple[int, int], tuple[object, bytes]] = {}
    cache_size = 0

    def emit(item: Any, level: int, *, cached: bool = True) -> Iterator[bytes]:
        nonlocal cache_size
        if cached and isinstance(item, RepositoryTextLexicalDocumentStatistics):
            key = (id(item), level)
            hit = cache.get(key)
            if hit is not None and hit[0] is item:
                yield hit[1]
                return
            raw = b"".join(emit(item, level, cached=False))
            if cache_size + len(raw) <= 256 << 20:
                cache[key] = (item, raw)
                cache_size += len(raw)
            yield raw
            return
        if item is None or isinstance(item, (str, bool, int, float)):
            yield json.dumps(item, ensure_ascii=True).encode()
            return
        if not isinstance(item, (dict, tuple, list)):
            yield from emit(canonical.NativeEncoder().default(item), level)
            return
        if not item:
            yield b"{}" if isinstance(item, dict) else b"[]"
            return
        mapping = isinstance(item, dict)
        yield b"{\n" if mapping else b"[\n"
        for n, key in enumerate(sorted(item) if mapping else range(len(item))):
            if n:
                yield b",\n"
            yield b"  " * (level + 1)
            if mapping:
                yield json.dumps(key, ensure_ascii=True).encode() + b": "
            yield from emit(item[key], level + 1)
        yield b"\n" + b"  " * level + (b"}" if mapping else b"]")

    h = hashlib.sha256()
    for chunk in emit(value, 0):
        h.update(chunk)
    h.update(b"\n")
    return {
        "native_type": type(value).__module__ + "." + type(value).__qualname__,
        "canonical_sha256": h.hexdigest(),
    }


def run(operation: str) -> dict[str, Any]:
    """Replay complete durable native state without any production entry point."""
    original = canonical.native_hash
    canonical.native_hash = fast_hash
    try:
        return execute.finalize() if operation == "finalize" else execute.verify()
    finally:
        canonical.native_hash = original


def seal_reader() -> None:
    """Bind publication-reader source separately from immutable producer hashes."""
    root = execute.CAPTURE
    value = {
        "schema": "case-0012-publication-reader-v1",
        "producer_source": "UNCHANGED; marker implementation hashes",
        "native_operations": "72 RETURNED; no rerun",
        "reason": "Read-only finalization interrupted while expanding repeated index statistics; resumed with byte-equivalent bounded fragment caching",
        "reader_sha256": digest(binary(execute.PACKAGE / "replay.py")),
        "tests_sha256": digest(binary(execute.PACKAGE / "test_replay.py")),
        "stage_b_integrity_sha256": digest(binary(root / "integrity.json")),
    }
    path = root / "publication_reader.json"
    if path.exists():
        if read_json(path) != value:
            raise ValueError("Publication reader binding differs")
    else:
        put_text(path, json_bytes(value).decode())


def main() -> None:
    """Finalize/verify only; there is deliberately no execute operation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=("finalize", "verify"))
    args = parser.parse_args()
    result = run(args.operation)
    seal_reader()
    print(
        json.dumps(
            {
                k: result[k]
                for k in (
                    "stage_b",
                    "execution",
                    "counts",
                    "arms",
                    "behavioral_resolution_equality",
                    "behavioral_presentation_equality",
                    "gold",
                    "effectiveness",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
