# Copyright (c) 2026
"""Path resolution operations."""

from __future__ import annotations

from pathlib import Path

from devtools.paths.errors import PathResolutionError
from devtools.paths.models import ResolvedPath


def resolve_path(
    path: str | Path,
    *,
    base_directory: str | Path | None = None,
) -> ResolvedPath:
    """Resolve a path according to explicit path policy.

    Relative paths require an explicit absolute base directory. Absolute paths
    are resolved directly and do not depend on the base directory.

    Resolution does not require the target path to exist.

    :param path: Path to resolve.
    :param base_directory: Absolute base directory used for relative paths.
    :returns: Resolved absolute path.
    :raises PathResolutionError: If a relative path has no base directory or
        the supplied base directory is not absolute.
    """
    candidate = Path(path)

    if candidate.is_absolute():
        return ResolvedPath(candidate.resolve(strict=False))

    if base_directory is None:
        msg = "Relative paths require an explicit base directory."
        raise PathResolutionError(msg)

    base = Path(base_directory)

    if not base.is_absolute():
        msg = "Base directory must be absolute."
        raise PathResolutionError(msg)

    return ResolvedPath((base / candidate).resolve(strict=False))