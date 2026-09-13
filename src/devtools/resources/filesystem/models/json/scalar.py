# Copyright (c) 2026
"""JSON scalar filesystem models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from devtools.core.conversion import convert
from devtools.resources.filesystem.models.json.base import JsonFile, JsonScalar

if TYPE_CHECKING:
    from devtools.core.conversion import Converter


@dataclass(frozen=True, slots=True)
class JsonScalarFile(JsonFile):
    """Represent a JSON document whose root is a scalar value."""

    value: JsonScalar = field(kw_only=True)

    def convert[TargetT](
        self,
        converter: Converter[JsonScalar, TargetT],
    ) -> TargetT:
        """Convert the scalar value through an explicit callable.

        :param converter: Callable receiving the ordinary JSON scalar.
        :returns: Converter result.
        :raises ConversionError: If the converter raises an ordinary exception.
        """
        return convert(self.value, converter)
