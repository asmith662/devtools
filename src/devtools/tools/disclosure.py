# Copyright (c) 2026
"""Explicit model-disclosure values without executable Tool authority."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class ToolDescriptor:
    """Describe the intentionally bounded portion of a Tool visible to a model."""

    name: str
    description: str
    input_schema_json: str

    def __post_init__(self) -> None:
        """Validate and canonically retain one JSON Schema object."""
        if not self.name.strip() or self.name != self.name.strip():
            msg = (
                "Tool descriptor name must be nonblank without surrounding "
                "whitespace."
            )
            raise TypeError(msg)
        if not self.description.strip():
            msg = "Tool descriptor description cannot be blank."
            raise TypeError(msg)
        try:
            schema = json.loads(self.input_schema_json)
        except json.JSONDecodeError as error:
            msg = "Tool descriptor input schema must be valid JSON."
            raise ValueError(msg) from error
        if not isinstance(schema, dict):
            msg = "Tool descriptor input schema must be a JSON object."
            raise TypeError(msg)
        object.__setattr__(
            self,
            "input_schema_json",
            json.dumps(schema, sort_keys=True, separators=(",", ":")),
        )


class ToolInvocation[ArgumentsT](Protocol):
    """Materialize untrusted model arguments into candidate Tool input only."""

    @property
    def descriptor(self) -> ToolDescriptor:
        """Return the explicitly disclosed descriptor."""

    def materialize(self, serialized_arguments: str) -> ArgumentsT:
        """Produce candidate typed Tool input without validation or execution."""
