# Copyright (c) 2026
"""Base JSON filesystem models."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from devtools.filesystem.models.base import FileFormat
from devtools.filesystem.models.text import TextFile

type JsonScalar = str | int | float | bool | None
type JsonValue = JsonScalar | tuple[JsonValue, ...] | Mapping[str, JsonValue]
type JsonCompatible = (
    JsonScalar
    | list[JsonCompatible]
    | tuple[JsonCompatible, ...]
    | Mapping[str, JsonCompatible]
)


@dataclass(frozen=True, slots=True)
class JsonFile(TextFile):
    """Base class for immutable JSON file models.

    ``content`` is the decoded source text from which the model originated.
    It remains provenance after structured transformations. Concrete models'
    ``value`` fields represent the current immutable structured state; codecs
    serialize that value rather than regenerating ``content``.
    """

    @property
    def format(self) -> FileFormat:
        """Return the JSON format.

        :returns: JSON file format.
        """
        return FileFormat.JSON
