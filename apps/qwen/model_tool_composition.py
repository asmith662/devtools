# Copyright (c) 2026
"""Experiment composition between executable Tool disclosure and model input."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from devtools.models.interaction import ModelToolDefinition

if TYPE_CHECKING:
    from devtools.tools import ToolDescriptor


def normalize_tool_descriptor(
    descriptor: ToolDescriptor,
) -> ModelToolDefinition:
    """Normalize one explicit Tool disclosure into model-facing semantics."""
    try:
        schema = json.loads(descriptor.input_schema_json)
    except json.JSONDecodeError as error:  # Defensive after descriptor validation.
        msg = "Tool descriptor input schema must be valid JSON."
        raise ValueError(msg) from error
    if not isinstance(schema, dict):  # Defensive after descriptor validation.
        msg = "Tool descriptor input schema must be a JSON object."
        raise TypeError(msg)
    normalized_schema = json.dumps(schema, sort_keys=True, separators=(",", ":"))
    return ModelToolDefinition(
        name=descriptor.name,
        description=descriptor.description,
        input_schema_json=normalized_schema,
    )
