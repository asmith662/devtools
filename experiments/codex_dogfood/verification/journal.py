# Copyright (c) 2026
# ruff: noqa: ANN401, D105, D107, TC001, PLW1641 -- private unhashable comparison
"""Unchanged journal envelope checks with invocation-owned graph correspondence."""

from __future__ import annotations

import gzip
from collections import Counter
from hashlib import sha256
from types import FunctionType
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import json_bytes
from experiments.codex_dogfood.case_0012.stage_b.durability import Journal

from .archive import decoder
from .native import NativeMemo


class ArchiveMemo:
    """Exact encoded block binding; no trust survives the invocation."""

    def __init__(self) -> None:
        self.blocks: dict[bytes, tuple[str, bytes]] = {}
        self.decompressions = 0
        self.hits = 0
        self.decode = decoder()
        self.counts: Counter[bytes] | None = None

    def prepare(self, records: Any) -> None:
        """Retain decompressed bytes only for blocks the schedule reuses."""
        self.counts = Counter(
            sha256(value[name]["gzip_b85"].encode("ascii")).digest()
            for value, _ in records
            if value["state"] == "RETURNED"
            for name in ("native", "canonical")
        )

    def unpack(self, value: dict[str, str]) -> bytes:
        """Authenticate exact archive bytes, decoding repeated content once."""
        encoded = value["gzip_b85"].encode("ascii")
        key = sha256(encoded).digest()
        hit = self.blocks.get(key)
        if hit is not None:
            if hit[0] != value["sha256"]:
                message = "Journal native archive digest differs"
                raise ValueError(message)
            self.hits += 1
            return hit[1]
        compressed = self.decode(encoded)
        if sha256(compressed).hexdigest() != value["sha256"]:
            message = "Journal native archive digest differs"
            raise ValueError(message)
        raw = gzip.decompress(compressed)
        if self.counts is None or self.counts[key] > 1:
            self.blocks[key] = (value["sha256"], raw)
        self.decompressions += 1
        return raw


class Comparison:
    """Defer correspondence until the authenticated canonical bytes are available."""

    def __init__(self, memo: NativeMemo, native: Any) -> None:
        self.memo, self.native = memo, native

    def __eq__(self, other: object) -> bool:
        return isinstance(other, bytes) and self.memo.corresponds(self.native, other)


def journal_type(memo: NativeMemo) -> type[Journal]:
    """Require the caller to authenticate every physical capture byte first.

    Only describe/JSON comparison is substituted; the original load bytecode owns
    claim, hash chain, ordering, input hashes, native archive hashes and completion.
    The capture seal authenticates canonical JSON formatting as well as content.
    """

    def describe(value: Any) -> Comparison:
        return Comparison(memo, value)

    def encode(value: Any) -> Any:
        return value if isinstance(value, Comparison) else json_bytes(value)

    archives = ArchiveMemo()
    memo.archives = archives
    original = Journal.__dict__["load"].__func__

    def ordered(values: Any, *, key: Any) -> Any:
        records = sorted(values, key=key)
        archives.prepare(records)
        return records

    load = FunctionType(
        original.__code__,
        {
            **original.__globals__,
            "describe": describe,
            "json_bytes": encode,
            "unpack": archives.unpack,
            "sorted": ordered,
        },
        original.__name__,
        original.__defaults__,
        original.__closure__,
    )
    return type("AuthenticatedJournal", (Journal,), {"load": classmethod(load)})
