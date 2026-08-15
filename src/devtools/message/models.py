# Copyright (c) 2026
"""Message value objects."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from devtools.identity import Identity
from devtools.time import Timestamp


@dataclass(frozen=True, slots=True)
class MessageId:
    """Represent an immutable semantic identity for a message.

    :ivar value: Generic identity backing this message-specific identity.
    """

    value: Identity

    @classmethod
    def new(cls) -> MessageId:
        """Generate a new message identity.

        :returns: Newly generated message identity.
        """
        return cls(Identity.new())

    @classmethod
    def parse(cls, value: str) -> MessageId:
        """Parse a message identity from UUID text.

        :param value: UUID string representation.
        :returns: Parsed message identity.
        :raises ValueError: If the supplied value is not a valid UUID.
        """
        return cls(Identity.parse(value))

    def __str__(self) -> str:
        """Return the canonical message identity representation.

        :returns: Canonical UUID string.
        """
        return str(self.value)


class MessageRole(StrEnum):
    """Identify a message's conversational role."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass(frozen=True, slots=True)
class MessageSource:
    """Represent an immutable, provider-neutral message source.

    :ivar value: Nonblank source identifier without surrounding whitespace.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate source identifier invariants."""
        if not self.value.strip():
            msg = "Message source cannot be blank."
            raise ValueError(msg)

        if self.value != self.value.strip():
            msg = "Message source cannot have surrounding whitespace."
            raise ValueError(msg)

    def __str__(self) -> str:
        """Return the source identifier.

        :returns: Source identifier.
        """
        return self.value


@dataclass(frozen=True, slots=True)
class Message:
    """Represent an immutable piece of communicated text.

    :ivar id: Semantic identity of this message.
    :ivar created_at: Timestamp when this message was created.
    :ivar content: Uninterpreted communicated text.
    :ivar role: Conversational role of the message.
    :ivar source: Producer or origin of the message.
    """

    id: MessageId
    created_at: Timestamp
    content: str
    role: MessageRole
    source: MessageSource

    @classmethod
    def new(
        cls,
        content: str,
        *,
        role: MessageRole,
        source: MessageSource,
    ) -> Message:
        """Create a message with a new identity and current timestamp.

        :param content: Uninterpreted communicated text.
        :param role: Conversational role of the message.
        :param source: Producer or origin of the message.
        :returns: Newly created message.
        """
        return cls(
            id=MessageId.new(),
            created_at=Timestamp.now(),
            content=content,
            role=role,
            source=source,
        )

    def __str__(self) -> str:
        """Return the communicated text without presentation formatting.

        :returns: Message content.
        """
        return self.content
