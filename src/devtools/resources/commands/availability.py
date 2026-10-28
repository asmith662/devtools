# Copyright (c) 2026
"""Local executable discovery, not permission or proof an invocation will work."""

from __future__ import annotations

import shutil
import sys
from dataclasses import dataclass

from devtools.core.paths import ResolvedPath, resolve_path


@dataclass(frozen=True, slots=True)
class ExecutableAvailability:
    """Retain the selected platform and resolved executable, or explicit absence."""

    requested: str
    platform: str
    path: ResolvedPath | None


def discover_executable(name: str) -> ExecutableAvailability:
    """Use native PATH/PATHEXT discovery without launching or downloading anything.

    The returned path may change before execution. This does not discover
    versions, shell grammar, credentials, permissions or environment isolation.
    """
    if not name.strip() or "\x00" in name:
        msg = "Executable discovery requires a nonblank native name."
        raise ValueError(msg)
    found = shutil.which(name)
    return ExecutableAvailability(
        name,
        sys.platform,
        resolve_path(found) if found is not None else None,
    )
