# Copyright (c) 2026
"""Markdown filesystem models."""

from __future__ import annotations

from dataclasses import dataclass

from devtools.filesystem.models.base import FileFormat
from devtools.filesystem.models.text import TextFile


@dataclass(frozen=True, slots=True)
class MarkdownFile(TextFile):
    """Represent immutable Markdown source content.

    Structural Markdown parsing such as headings, sections, links, code
    blocks, front matter, and document hierarchy is intentionally deferred
    until the Markdown contract is defined.
    """

    @property
    def format(self) -> FileFormat:
        """Return the Markdown file format.

        :returns: Markdown file format.
        """
        return FileFormat.MARKDOWN
