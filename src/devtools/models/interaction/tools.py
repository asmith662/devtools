# Copyright (c) 2026
"""Normalized model-facing callable definitions and requested calls."""

from __future__ import annotations

import json
from dataclasses import dataclass


def _canonical_schema(value: str, *, label: str) -> str:
    """Validate one provider-neutral JSON Schema object deterministically."""
    try:
        decoded = json.loads(value)
    except json.JSONDecodeError as error:
        msg = f"{label} input schema must be valid JSON."
        raise ValueError(msg) from error
    if not isinstance(decoded, dict):
        msg = f"{label} input schema must be a JSON object."
        raise TypeError(msg)
    return json.dumps(decoded, sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True, slots=True)
class ModelToolDefinition:
    """Describe one provider-neutral callable disclosed for one model request."""

    name: str
    description: str
    input_schema_json: str

    def __post_init__(self) -> None:
        """Validate semantics without referencing executable Tools."""
        if not self.name.strip() or self.name != self.name.strip():
            msg = (
                "Model Tool definition name must be nonblank without surrounding "
                "whitespace."
            )
            raise TypeError(msg)
        if not self.description.strip():
            msg = "Model Tool definition description cannot be blank."
            raise ValueError(msg)
        object.__setattr__(
            self,
            "input_schema_json",
            _canonical_schema(self.input_schema_json, label="Model Tool definition"),
        )


@dataclass(frozen=True, slots=True)
class ModelToolCall:
    """Represent one provider-requested callable invocation without authority."""

    name: str
    arguments_json: str
    provider_call_id: str | None = None

    def __post_init__(self) -> None:
        """Preserve a syntactically valid untrusted argument object exactly."""
        if not self.name.strip() or self.name != self.name.strip():
            msg = (
                "Model Tool call name must be nonblank without surrounding "
                "whitespace."
            )
            raise TypeError(msg)
        if self.provider_call_id is not None and not self.provider_call_id.strip():
            msg = "Model Tool call provider ID cannot be blank when supplied."
            raise ValueError(msg)
        try:
            arguments = json.loads(self.arguments_json)
        except json.JSONDecodeError as error:
            msg = "Model Tool call arguments must be valid JSON."
            raise ValueError(msg) from error
        if not isinstance(arguments, dict):
            msg = "Model Tool call arguments must be a JSON object."
            raise TypeError(msg)
