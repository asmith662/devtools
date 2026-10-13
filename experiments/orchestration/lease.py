# Copyright (c) 2026
# ruff: noqa: PLC0415, FBT003 -- bounded controller/fixture boundary
"""Cooperative worktree writer lease; scientific claims remain independent authority."""

from __future__ import annotations

import importlib
import os
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

from experiments.orchestration.storage import no_links, require

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path


@contextmanager
def writer(root: Path) -> Iterator[None]:
    """Hold an OS-released lock through publication; never guess stale PID ownership."""
    path = root / ".local/experiment-controller.writer"
    no_links(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as stream:
        stream.seek(0, 2)
        if not stream.tell():
            stream.write(b"0")
            stream.flush()
        stream.seek(0)
        try:
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                fcntl: Any = importlib.import_module("fcntl")

                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            require(False, "Another controller owns this worktree writer lease")
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl = importlib.import_module("fcntl")

                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)
