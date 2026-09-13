# Copyright (c) 2026
"""Private Conversation semantic snapshot capture and reconstruction helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.agents.conversation.conversation import Conversation
from devtools.agents.conversation.history import History
from devtools.agents.conversation.message import ConversationMessage
from devtools.persistence.errors import PersistenceConflictError

if TYPE_CHECKING:
    from devtools.agents.conversation.conversation import ConversationId
    from devtools.agents.conversation.message import (
        ConversationMessageRole,
        MessageId,
    )
    from devtools.core.time import Timestamp
    from devtools.models.interaction import ConversationRef, InteractionSource


@dataclass(frozen=True, slots=True)
class _MessageSnapshot:
    """Represent immutable ConversationMessage state for private persistence use."""

    id: MessageId
    created_at: Timestamp
    content: str
    role: ConversationMessageRole
    source: InteractionSource

    @classmethod
    def from_message(cls, message: ConversationMessage) -> _MessageSnapshot:
        """Capture immutable ConversationMessage state."""
        return cls(
            id=message.id,
            created_at=message.created_at,
            content=message.content,
            role=message.role,
            source=message.source,
        )

    def to_message(self) -> ConversationMessage:
        """Restore one immutable ConversationMessage value."""
        return ConversationMessage(
            id=self.id,
            created_at=self.created_at,
            content=self.content,
            role=self.role,
            source=self.source,
        )


@dataclass(frozen=True, slots=True)
class _ConversationSnapshot:
    """Represent private semantic Conversation state shared by persistence formats."""

    id: ConversationId
    created_at: Timestamp
    messages: tuple[_MessageSnapshot, ...]
    conversations: tuple[ConversationRef, ...]


def capture_conversation(conversation: Conversation) -> _ConversationSnapshot:
    """Capture the current semantic state of a Conversation.

    Callers coordinating with active Runtime work must hold ``conversation.turn()``
    before invoking a synchronous persistence operation.
    """
    return snapshot_from_values(
        conversation_id=conversation.id,
        created_at=conversation.created_at,
        messages=tuple(
            _MessageSnapshot.from_message(message) for message in conversation.history
        ),
        conversations=tuple(conversation.conversations.values()),
    )


def snapshot_from_values(
    *,
    conversation_id: ConversationId,
    created_at: Timestamp,
    messages: tuple[_MessageSnapshot, ...],
    conversations: tuple[ConversationRef, ...],
) -> _ConversationSnapshot:
    """Validate and assemble private semantic Conversation state."""
    _validate_message_ids(messages)
    return _ConversationSnapshot(
        id=conversation_id,
        created_at=created_at,
        messages=messages,
        conversations=tuple(sorted(conversations, key=lambda item: str(item.source))),
    )


def restore_conversation(snapshot: _ConversationSnapshot) -> Conversation:
    """Reconstruct a new Conversation with fresh local coordination state."""
    restored_messages: dict[MessageId, ConversationMessage] = {}
    messages: list[ConversationMessage] = []
    for message_snapshot in snapshot.messages:
        message = restored_messages.get(message_snapshot.id)
        if message is None:
            message = message_snapshot.to_message()
            restored_messages[message_snapshot.id] = message
        messages.append(message)
    return Conversation(
        id=snapshot.id,
        created_at=snapshot.created_at,
        history=History(messages=tuple(messages)),
        conversations=snapshot.conversations,
    )


def _validate_message_ids(messages: tuple[_MessageSnapshot, ...]) -> None:
    """Reject conflicting immutable values assigned to one MessageId."""
    known: dict[MessageId, _MessageSnapshot] = {}
    for message in messages:
        existing = known.get(message.id)
        if existing is not None and existing != message:
            msg = f"Conflicting immutable state for MessageId {message.id}."
            raise PersistenceConflictError(msg)
        known[message.id] = message
