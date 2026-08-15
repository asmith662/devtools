# Copyright (c) 2026
"""Agent value objects."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.message import Message, MessageSource


@dataclass(frozen=True, slots=True)
class ConversationRef:
    """Represent opaque continuation state owned by an agent source.

    :ivar source: Source that owns the external conversation state.
    :ivar value: Opaque provider-owned continuation identifier.
    """

    source: MessageSource
    value: str

    def __post_init__(self) -> None:
        """Validate continuation identifier invariants.

        :raises ValueError: If the identifier is blank or has surrounding
            whitespace.
        """
        if not self.value.strip():
            msg = "Conversation reference cannot be blank."
            raise ValueError(msg)

        if self.value != self.value.strip():
            msg = "Conversation reference cannot have surrounding whitespace."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class AgentTurn:
    """Represent the final result of one agent invocation.

    :ivar message: Final message produced by the agent.
    :ivar conversation: Optional continuation state returned by the agent.
    """

    message: Message
    conversation: ConversationRef | None = None

    def __post_init__(self) -> None:
        """Validate that returned continuation state belongs to the message.

        :raises ValueError: If the conversation source differs from the
            returned message source.
        """
        if (
            self.conversation is not None
            and self.conversation.source != self.message.source
        ):
            msg = "Conversation reference source must match the message source."
            raise ValueError(msg)
