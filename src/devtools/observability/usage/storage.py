# Copyright (c) 2026
"""Local versioned snapshots using the canonical filesystem substrate."""

from __future__ import annotations

import hashlib
import json
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING

from devtools.core.paths import resolve_path
from devtools.observability.usage.models import UsageObservation
from devtools.resources import filesystem
from devtools.resources.filesystem.models.json import JsonObjectFile

if TYPE_CHECKING:
    from collections.abc import Iterator

SCHEMA = "observed-usage-ledger-v1"


@contextmanager
def writer(path: Path) -> Iterator[None]:
    """Hold one local usage writer lease; contention/crash never triggers retry.

    Atomic exclusive directory creation supplies the locking capability absent
    from filesystem.write. A stale lease requires explicit operator recovery;
    it is not silently deleted and cannot authorize another invocation.
    """
    absolute = resolve_path(path, base_directory=Path.cwd()).value
    absolute.parent.mkdir(parents=True, exist_ok=True)
    lease = absolute.with_suffix(".writer")
    lease.mkdir()
    try:
        yield
    finally:
        lease.rmdir()


def load(path: Path) -> tuple[UsageObservation, ...]:
    """Restore metadata only; missing ledger is an empty partial observation set."""
    if not path.exists():
        return ()
    file = filesystem.read(
        resolve_path(path, base_directory=Path.cwd()),
        max_bytes=128 << 20,
    )
    if not isinstance(file, JsonObjectFile) or file["schema"] != SCHEMA:
        message = "Observed usage ledger schema differs"
        raise ValueError(message)
    value = json.loads(file.content)
    return tuple(UsageObservation.from_dict(v) for v in value["observations"])


def save(path: Path, rows: tuple[UsageObservation, ...]) -> None:
    """Atomically replace a local metadata snapshot; callers serialize writers."""
    path.parent.mkdir(parents=True, exist_ok=True)
    unique = {
        hashlib.sha256(json.dumps(r.to_dict(), sort_keys=True).encode()).hexdigest(): r
        for r in rows
    }
    value = {
        "schema": SCHEMA,
        "observations": [unique[k].to_dict() for k in sorted(unique)],
    }
    filesystem.write(
        JsonObjectFile(
            resolve_path(path, base_directory=Path.cwd()),
            "",
            value=json.loads(json.dumps(value)),
        ),
    )
