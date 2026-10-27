# Copyright (c) 2026
"""Legacy disclosure facade and application-owned multiplexed operation input."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from devtools.agents.model_tools import (
    normalize_tool_descriptor as normalize_tool_descriptor,  # noqa: PLC0414 -- explicit legacy public re-export
)
from devtools.tools import ToolDescriptor

if TYPE_CHECKING:
    from devtools.models.interaction import ModelToolDefinition


@dataclass(frozen=True, slots=True)
class OperationInvocation:
    """Materialize legacy Qwen (operation, values) input, without granting it."""

    descriptor: ToolDescriptor

    @classmethod
    def selected(cls, definition: ModelToolDefinition) -> OperationInvocation:
        """Adapt one operation already selected by the trusted task host."""
        return cls(
            ToolDescriptor(
                definition.name,
                definition.description,
                definition.input_schema_json,
            ),
        )

    def materialize(self, serialized_arguments: str) -> tuple[str, dict[str, Any]]:
        """Retain existing JSON input semantics; Tool validation follows admission."""
        return self.descriptor.name, json.loads(serialized_arguments)
