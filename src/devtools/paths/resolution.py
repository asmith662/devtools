# Copyright (c) 2026
"""Path parsing, resolution, and well-known location helpers."""

from __future__ import annotations

import tempfile
from pathlib import Path

from devtools.paths.errors import PathParsingError, PathResolutionError
from devtools.paths.models import ResolvedPath


def parse_path(value: str | Path) -> Path:
    """Parse a filesystem path representation.

    This operation interprets the supplied value only as a filesystem path.
    It does not make the path absolute or inspect filesystem state.

    :param value: Filesystem path representation.
    :returns: Parsed path.
    :raises PathParsingError: If a string path is empty.
    """
    if isinstance(value, Path):
        return value

    if not value.strip():
        msg = "Filesystem path cannot be empty."
        raise PathParsingError(msg)

    return Path(value)


def parse_dot_path(
    value: str,
    *,
    suffix: str | None = None,
) -> Path:
    """Parse a dot-separated path into a filesystem path.

    Dot-path conversion is mechanical and does not assign language-specific
    meaning such as Python package or module semantics.

    For example, ``"devtools.paths.models"`` becomes
    ``Path("devtools", "paths", "models")``.

    :param value: Dot-separated path representation.
    :param suffix: Optional suffix to append to the final path component.
    :returns: Relative filesystem path.
    :raises PathParsingError: If the dot path is empty, contains empty
        components, or contains an invalid suffix.
    """
    value = value.strip()

    if not value:
        msg = "Dot path cannot be empty."
        raise PathParsingError(msg)

    parts = value.split(".")

    if any(not part for part in parts):
        msg = f"Dot path contains an empty component: {value!r}."
        raise PathParsingError(msg)

    path = Path(*parts)

    if suffix is None:
        return path

    if not suffix:
        msg = "Suffix cannot be empty."
        raise PathParsingError(msg)

    normalized_suffix = suffix if suffix.startswith(".") else f".{suffix}"

    return path.with_suffix(normalized_suffix)


def resolve_path(
    value: str | Path,
    *,
    base_directory: str | Path | None = None,
) -> ResolvedPath:
    """Resolve a filesystem path according to explicit path policy.

    Absolute inputs are resolved directly. Relative inputs require an explicit
    absolute base directory. The target does not need to exist.

    Existing symbolic-link components are resolved according to
    :meth:`pathlib.Path.resolve`.

    :param value: Filesystem path to resolve.
    :param base_directory: Absolute base directory for relative paths.
    :returns: Normalized absolute resolved path.
    :raises PathParsingError: If the filesystem path representation is empty.
    :raises PathResolutionError: If a relative path has no base directory or
        the supplied base directory is not absolute.
    """
    candidate = parse_path(value)

    if candidate.is_absolute():
        return ResolvedPath(candidate.resolve(strict=False))

    if base_directory is None:
        msg = "Relative paths require an explicit base directory."
        raise PathResolutionError(msg)

    base = parse_path(base_directory)

    if not base.is_absolute():
        msg = "Base directory must be absolute."
        raise PathResolutionError(msg)

    return ResolvedPath((base / candidate).resolve(strict=False))


def resolve_dot_path(
    value: str,
    *,
    base_directory: str | Path,
    suffix: str | None = None,
) -> ResolvedPath:
    """Parse and resolve a dot-separated path.

    This is a convenience wrapper around :func:`parse_dot_path` and
    :func:`resolve_path`.

    :param value: Dot-separated path representation.
    :param base_directory: Absolute directory against which to resolve it.
    :param suffix: Optional suffix for the final path component.
    :returns: Resolved absolute filesystem path.
    :raises PathParsingError: If the dot-path representation is invalid.
    :raises PathResolutionError: If the base directory is not absolute.
    """
    parsed = parse_dot_path(value, suffix=suffix)
    return resolve_path(parsed, base_directory=base_directory)


def get_home_dir() -> ResolvedPath:
    """Return the current user's home directory.

    :returns: Resolved user home directory.
    """
    return ResolvedPath(Path.home().resolve(strict=False))


def get_temp_dir() -> ResolvedPath:
    """Return the platform temporary directory.

    :returns: Resolved temporary directory.
    """
    return ResolvedPath(Path(tempfile.gettempdir()).resolve(strict=False))


def get_downloads_dir() -> ResolvedPath:
    """Return the conventional user downloads directory.

    This helper provides a portable conventional location based on the user's
    home directory. It does not currently query operating-system-specific
    redirected or customized known-folder configuration.

    :returns: Resolved conventional downloads directory.
    """
    return resolve_path("Downloads", base_directory=get_home_dir().value)
