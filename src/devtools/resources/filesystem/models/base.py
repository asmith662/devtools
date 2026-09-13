# Copyright (c) 2026
"""Base filesystem models."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.core.paths import ResolvedPath


class FileFormat(StrEnum):
    """Supported file content formats."""

    BINARY = "binary"
    TEXT = "text"
    JSON = "json"
    CSV = "csv"
    MARKDOWN = "markdown"


@dataclass(frozen=True, slots=True)
class File(ABC):
    """Represent an immutable filesystem-backed file.

    :ivar path: Resolved filesystem path.
    """

    path: ResolvedPath

    @property
    @abstractmethod
    def format(self) -> FileFormat:
        """Return the represented file format."""
