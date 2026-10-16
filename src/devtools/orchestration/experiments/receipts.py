# Copyright (c) 2026
"""Pipeline-owned integrity-checked receipts, separate from scientific journals."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, cast

from devtools.core.identity import Identity
from devtools.core.paths import resolve_path
from devtools.resources.filesystem import FileFormat, TextFile, read, write

if TYPE_CHECKING:
    from pathlib import Path

SCHEMA = "experiment-preparation-v1"


@dataclass(frozen=True, slots=True)
class PreparationId(Identity):
    """Identify one preparation observation, never a scientific attempt."""


def encoded(value: object) -> str:
    """Encode the pipeline's versioned deterministic JSON representation."""
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def digest(value: object) -> str:
    """Authenticate a receipt payload independently of its file address."""
    return hashlib.sha256(encoded(value).encode()).hexdigest()


def store(path: Path, value: dict[str, Any]) -> None:
    """Write once within an exclusively allocated preparation directory."""
    write(
        TextFile(
            resolve_path(path),
            encoded({"schema": SCHEMA, "sha256": digest(value), "value": value}),
        ),
        overwrite=False,
    )


def restore(path: Path) -> dict[str, Any]:
    """Reject changed, foreign-version or malformed evidence."""
    file = cast(
        "TextFile",
        read(resolve_path(path), file_format=FileFormat.TEXT, max_bytes=16 << 20),
    )
    value = json.loads(file.content)
    if value["schema"] != SCHEMA or value["sha256"] != digest(value["value"]):
        message = "Preparation receipt integrity/schema differs"
        raise ValueError(message)
    return dict(value["value"])


def history(root: Path, plan: str | None = None) -> list[dict[str, Any]]:
    """List newest first; unfinished receipts remain explicitly indeterminate."""
    results = []
    for path in root.glob("*/start.json"):
        start = restore(path)
        final = path.with_name("result.json")
        result = (
            restore(final)
            if final.exists()
            else {
                **start,
                "disposition": "INTERRUPTED_OR_IN_PROGRESS",
                "report": str(final),
            }
        )
        if plan is not None and result["plan"] != plan:
            continue
        for stage in result.get("stages", []):
            receipt = restore(path.with_name(stage["name"] + ".json"))
            if digest(receipt) != stage["sha256"]:
                message = "Preparation stage reference differs"
                raise ValueError(message)
        results.append(result)
    return sorted(results, key=lambda v: (v["started"], v["attempt"]), reverse=True)


def latest(root: Path, plan: str | None = None) -> dict[str, Any]:
    """Find latest/by-plan without requiring an immutable scientific run ID."""
    results = history(root, plan)
    if not results:
        message = "No matching preparation receipts"
        raise ValueError(message)
    if len({(v["target"], v["plan_sha256"]) for v in results}) > 1:
        message = "Ambiguous preparation history; use a distinct receipt directory"
        raise ValueError(message)
    return results[0]
