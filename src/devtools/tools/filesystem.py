# Copyright (c) 2026
"""Experimental Tool bridge over bounded filesystem reads."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.filesystem import read
from devtools.tools.errors import ToolInputError

if TYPE_CHECKING:
    from devtools.filesystem import File
    from devtools.paths import ResolvedPath


class ReadRepositoryFileTool:
    """Read supported files within one configured repository-root scope."""

    _NAME = "read_repository_file"
    _DESCRIPTION = "Read one supported file below the configured repository root."

    def __init__(self, root: ResolvedPath) -> None:
        """Create a read-only Tool scoped to one repository root."""
        self._root = root

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
        if arguments.value.is_relative_to(self._root.value):
            return

        msg = f"Path is outside the configured repository root: {arguments}."
        raise ToolInputError(msg)

    async def execute(self, arguments: ResolvedPath) -> File:
        """Read one admitted path through the existing synchronous Filesystem API."""
        return read(arguments)
