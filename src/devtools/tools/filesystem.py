# Copyright (c) 2026
"""Experimental Tool bridge over bounded filesystem reads."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

from devtools.filesystem import (
    FilesystemNotFoundError,
    FilesystemPermissionError,
    read,
)
from devtools.paths import resolve_path
from devtools.tools.errors import ToolInputError

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.filesystem import File
    from devtools.paths import ResolvedPath


class ReadRepositoryFileTool:
    """Read supported files within one configured repository-root scope."""

    _NAME = "read_repository_file"
    _DESCRIPTION = "Read one supported file below the configured repository root."

    def __init__(self, root: ResolvedPath) -> None:
        """Create a read-only Tool scoped to one repository root."""
        self._root = _normalize(root)

    @property
    def name(self) -> str:
        """Return the local capability label."""
        return self._NAME

    @property
    def description(self) -> str:
        """Return the provider-neutral capability description."""
        return self._DESCRIPTION

    def validate(self, arguments: ResolvedPath) -> None:
        """Reject paths outside this Tool's configured semantic scope."""
        normalized_arguments = _normalize(arguments)

        if normalized_arguments.value.is_relative_to(self._root.value):
            return

        msg = f"Path is outside the configured repository root: {arguments}."
        raise ToolInputError(msg)

    async def execute(self, arguments: ResolvedPath) -> File:
        """Read one admitted path through the existing synchronous Filesystem API."""
        return read(_normalize(arguments))


class RepositoryDirectoryEntryKind(StrEnum):
    """Describe the direct filesystem kind exposed by bounded directory listing."""

    FILE = "file"
    DIRECTORY = "directory"
    SYMLINK = "symlink"
    OTHER = "other"


@dataclass(frozen=True, slots=True)
class RepositoryDirectoryEntry:
    """Retain one direct repository-directory entry without a host path."""

    name: str
    kind: RepositoryDirectoryEntryKind


@dataclass(frozen=True, slots=True)
class RepositoryDirectoryListing:
    """Retain one deterministic bounded direct repository-directory listing."""

    entries: tuple[RepositoryDirectoryEntry, ...]
    truncated: bool


class ListRepositoryDirectoryTool:
    """List bounded direct entries within one configured repository-root scope."""

    _NAME = "list_repository_directory"
    _DESCRIPTION = "List bounded direct entries inside one repository directory."
    _DEFAULT_MAXIMUM_ENTRIES = 64

    def __init__(
        self,
        root: ResolvedPath,
        *,
        maximum_entries: int = _DEFAULT_MAXIMUM_ENTRIES,
    ) -> None:
        """Create one non-recursive read-only listing capability."""
        if maximum_entries <= 0:
            msg = "Maximum directory entries must be positive."
            raise ValueError(msg)
        self._root = _normalize(root)
        self._maximum_entries = maximum_entries

    @property
    def name(self) -> str:
        """Return the local capability label."""
        return self._NAME

    @property
    def description(self) -> str:
        """Return the provider-neutral capability description."""
        return self._DESCRIPTION

    def validate(self, arguments: ResolvedPath) -> None:
        """Reject paths outside this Tool's configured semantic scope."""
        normalized_arguments = _normalize(arguments)
        if normalized_arguments.value.is_relative_to(self._root.value):
            return
        msg = f"Path is outside the configured repository root: {arguments}."
        raise ToolInputError(msg)

    async def execute(self, arguments: ResolvedPath) -> RepositoryDirectoryListing:
        """Enumerate a deterministic bounded direct listing for admitted input."""
        directory = _normalize(arguments).value
        try:
            if not directory.exists():
                msg = f"Filesystem path does not exist: {arguments}."
                raise FilesystemNotFoundError(msg)
            if not directory.is_dir():
                msg = f"Filesystem path is not a directory: {arguments}."
                raise NotADirectoryError(msg)
            paths = sorted(directory.iterdir(), key=lambda entry: entry.name)
        except PermissionError as error:
            msg = f"Permission denied while listing directory: {arguments}."
            raise FilesystemPermissionError(msg) from error
        limit = self._maximum_entries
        return RepositoryDirectoryListing(
            entries=tuple(_directory_entry(path) for path in paths[:limit]),
            truncated=len(paths) > limit,
        )


def _directory_entry(path: Path) -> RepositoryDirectoryEntry:
    """Classify one direct entry without resolving or disclosing its host path."""
    if path.is_symlink():
        kind = RepositoryDirectoryEntryKind.SYMLINK
    elif path.is_file():
        kind = RepositoryDirectoryEntryKind.FILE
    elif path.is_dir():
        kind = RepositoryDirectoryEntryKind.DIRECTORY
    else:
        kind = RepositoryDirectoryEntryKind.OTHER
    return RepositoryDirectoryEntry(path.name, kind)


def _normalize(path: ResolvedPath) -> ResolvedPath:
    """Apply the repository's existing path-resolution semantics."""
    return resolve_path(path.value)
