# Copyright (c) 2026
"""Model-facing output from one model interaction."""

from dataclasses import dataclass

from devtools.models.interaction.models import ConversationRef, InteractionSource


@dataclass(frozen=True, slots=True)
class ModelResponse:
    """Represent text and optional continuation returned by a ModelInteraction."""

    content: str
    source: InteractionSource
    conversation: ConversationRef | None = None

    def __post_init__(self) -> None:
        """Ensure returned continuation belongs to this response source."""
        if self.conversation is not None and self.conversation.source != self.source:
            msg = "Conversation reference source must match the response source."
            raise ValueError(msg)
