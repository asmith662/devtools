# Copyright (c) 2026
# ruff: noqa: ANN401, TRY300 -- non-authoritative immutable preparation cache
"""Cache explicit deterministic byte representations; never pickle live objects."""

from __future__ import annotations

import base64
from typing import TYPE_CHECKING, Any

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.storage import load, require, save

if TYPE_CHECKING:
    from pathlib import Path


class PreparationCache:
    """Accelerate immutable adapter preparation with fresh validation on every hit."""

    def __init__(self, root: Path) -> None:
        """Choose ignored operational cache storage, never scientific authority."""
        self.root = root

    @staticmethod
    def key(binding: Any) -> str:
        """Bind tree/content, repository, observation, implementation and config."""
        require(
            set(binding)
            == {
                "schema",
                "parent_tree",
                "repository_id",
                "observation_semantics",
                "implementation",
                "configuration",
                "surfaces",
            },
            "Cache binding contract",
        )
        return digest(json_bytes(binding))

    def get(self, binding: Any) -> tuple[str, dict[str, bytes] | None]:
        """Reject corrupt data and request recomputation without scientific failure."""
        key = self.key(binding)
        path = self.root / (key + ".json")
        if not path.exists():
            return "CACHE_MISS", None
        try:
            value = load(path)
            require(
                value["binding"] == binding and value["key"] == key,
                "Cache identity differs",
            )
            files = {
                name: base64.b64decode(raw, validate=True)
                for name, raw in value["files"].items()
            }
            require(
                value["sha256"] == {n: digest(raw) for n, raw in files.items()},
                "Cache integrity differs",
            )
            return "CACHE_HIT", files
        except (ValueError, KeyError, TypeError, OSError):
            return "CACHE_REJECTED", None

    def put(self, binding: Any, files: dict[str, bytes]) -> None:
        """Retain replaceable bytes; authoritative capture still binds them."""
        key = self.key(binding)
        save(
            self.root / (key + ".json"),
            {
                "key": key,
                "binding": binding,
                "sha256": {n: digest(v) for n, v in files.items()},
                "files": {n: base64.b64encode(v).decode() for n, v in files.items()},
            },
        )
