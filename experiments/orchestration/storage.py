# Copyright (c) 2026
# ruff: noqa: ANN401 -- explicit experiment transport boundary
"""Bounded artifact transport over canonical paths/filesystem primitives."""

from __future__ import annotations

import json
import stat
from typing import TYPE_CHECKING, Any

from devtools.core.paths import resolve_path
from devtools.resources.filesystem import TextFile, write
from experiments.codex_dogfood.case_0009.artifacts import (
    digest,
    json_bytes,
    put_binary,
)

if TYPE_CHECKING:
    from pathlib import Path


def binary(path: Path) -> bytes:
    """Bound exact artifact bytes at the explicit experiment binary codec boundary."""
    no_links(path)
    with path.open("rb") as stream:
        raw = stream.read((128 << 20) + 1)
    require(len(raw) <= 128 << 20, "Artifact exceeds binary transport bound")
    return raw


def require(value: object, message: str) -> None:
    """Reject unverifiable state without inventing recovery."""
    if not value:
        raise ValueError(message)


def safe(root: Path, address: str) -> Path:
    """Resolve a portable owned relative address with canonical containment."""
    require(
        bool(address)
        and not address.startswith(("/", "\\"))
        and "\\" not in address
        and ":" not in address,
        "Invalid artifact address",
    )
    require(
        all(
            p not in {"", ".", "..", ".git", ".local", ".scratch", "__pycache__"}
            and not any(
                x in p.casefold()
                for x in (
                    "holdout",
                    "confirmation",
                    "reserve",
                    "reference_implementations",
                )
            )
            for p in address.split("/")
        ),
        "Restricted artifact address",
    )
    no_links(root)
    raw = root / address
    no_links(raw)
    resolved = resolve_path(raw).value
    require(resolved.is_relative_to(resolve_path(root).value), "Artifact escapes owner")
    return resolved


def no_links(path: Path) -> None:
    """Reject links/reparse points on existing ancestors and entries."""
    for p in (path, *path.parents):
        if p.exists() or p.is_symlink():
            require(
                not p.is_symlink()
                and not getattr(p.lstat(), "st_file_attributes", 0)
                & stat.FILE_ATTRIBUTE_REPARSE_POINT,
                "Link/reparse point rejected",
            )


def load(path: Path) -> Any:
    """Read bounded canonical JSON, never operational handoff authority."""
    no_links(path)
    return json.loads(binary(path))


def save(path: Path, value: Any) -> None:
    """Atomically replace operational summaries through the filesystem owner."""
    no_links(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    write(TextFile(resolve_path(path), json_bytes(value).decode()))


def exclusive(path: Path, value: Any) -> None:
    """Use exclusive binary creation for immutable claims/receipts."""
    no_links(path)
    put_binary(path, json_bytes(value))


def bundle(root: Path, files: dict[str, str]) -> dict[str, bytes]:
    """Authenticate every allowlisted artifact; no recursive unknown-file import."""
    result = {}
    for address, sha in files.items():
        path = safe(root, address)
        with path.open("rb") as stream:
            raw = stream.read((128 << 20) + 1)
        require(
            len(raw) <= 128 << 20 and digest(raw) == sha,
            "Artifact hash/size differs: " + address,
        )
        result[address] = raw
    return result


def materialize(root: Path, files: dict[str, bytes]) -> None:
    """Copy exact artifact bytes into a fresh directory, rejecting existing state."""
    no_links(root)
    require(not root.exists(), "Workspace already exists")
    root.mkdir(parents=True)
    for address, raw in files.items():
        put_binary(safe(root, address), raw)
