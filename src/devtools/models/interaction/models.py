# Copyright (c) 2026
"""Values exchanged at the model-invocation boundary."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InteractionSource:
    """Identify the model interaction that owns provider continuation state."""

    value: str

    def __post_init__(self) -> None:
        """Validate source identifier invariants."""
        if not self.value.strip():
            msg = "ModelInteraction source cannot be blank."
            raise ValueError(msg)
        if self.value != self.value.strip():
            msg = "ModelInteraction source cannot have surrounding whitespace."
            raise ValueError(msg)

    def __str__(self) -> str:
        """Return the source identifier."""
        return self.value


@dataclass(frozen=True, slots=True)
class ConversationRef:
    """Represent opaque continuation state owned by one ModelInteraction."""

    source: InteractionSource
    value: str

    def __post_init__(self) -> None:
        """Validate continuation identifier invariants."""
        if not self.value.strip():
            msg = "Conversation reference cannot be blank."
            raise ValueError(msg)
        if self.value != self.value.strip():
            msg = "Conversation reference cannot have surrounding whitespace."
            raise ValueError(msg)
