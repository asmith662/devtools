# Copyright (c) 2026
"""JSON scalar filesystem models."""

from __future__ import annotations

from dataclasses import dataclass, field

from devtools.filesystem.models.json.base import JsonFile, JsonScalar


@dataclass(frozen=True, slots=True)
class JsonScalarFile(JsonFile):
    """Represent a JSON document whose root is a scalar value."""

    value: JsonScalar = field(kw_only=True)
