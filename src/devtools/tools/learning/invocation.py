# Copyright (c) 2026
"""Native disclosure and typed Tool adaptation; trusted admission stays host-owned."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.learning.investigation.proposals import LearningFeedback, LearningProposal
from devtools.tools import ToolDescriptor

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

DESCRIPTOR = ToolDescriptor(
    "learning_investigate",
    (
        "Request one bounded learning investigation action; proposals do "
        "not confer authority."
    ),
    json.dumps(
        {
            "type": "object",
            "additionalProperties": False,
            "required": list(LearningProposal.__dataclass_fields__),
            "properties": {
                name: {"type": "array", "items": {"type": "string"}}
                if name == "evidence"
                else {"type": ["string", "null"]}
                if name == "method"
                else {"type": "string"}
                for name in LearningProposal.__dataclass_fields__
            },
        },
    ),
)


@dataclass(frozen=True, slots=True)
class LearningInvocation:
    """Materialize scientific proposals without touching data or reserving effects."""

    descriptor: ToolDescriptor = DESCRIPTOR

    def materialize(self, serialized_arguments: str) -> LearningProposal:
        """Use the closed scientific proposal wire boundary."""
        return LearningProposal.materialize(serialized_arguments)


@dataclass(frozen=True, slots=True)
class LearningTool:
    """Delegate only the selected host's admitted learning action exactly once."""

    admit_semantics: Callable[[LearningProposal], None]
    perform: Callable[[LearningProposal], Awaitable[LearningFeedback]]
    name: str = DESCRIPTOR.name
    description: str = DESCRIPTOR.description

    def validate(self, arguments: LearningProposal) -> None:
        """Check host-held admission without creating new authority."""
        self.admit_semantics(arguments)

    async def execute(self, arguments: LearningProposal) -> LearningFeedback:
        """Consume the host's pending grant before awaiting an effect."""
        return await self.perform(arguments)
