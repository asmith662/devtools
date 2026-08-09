# Copyright (c) 2026
"""CSV filesystem models."""

from __future__ import annotations

from dataclasses import dataclass

from devtools.filesystem.models.base import FileFormat
from devtools.filesystem.models.text import TextFile


@dataclass(frozen=True, slots=True)
class CsvFile(TextFile):
    """Represent immutable CSV source content.

    CSV parsing semantics such as delimiters, headers, quoting, dialects, and
    typed row representations are intentionally deferred until the CSV
    contract is defined.
    """

    @property
    def format(self) -> FileFormat:
        """Return the CSV file format.

        :returns: CSV file format.
        """
        return FileFormat.CSV
