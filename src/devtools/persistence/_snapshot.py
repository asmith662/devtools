# Copyright (c) 2026
"""Private Session semantic snapshot capture and reconstruction helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context.history import History
from devtools.context.message import Message
from devtools.context.session import Session
from devtools.persistence.errors import PersistenceConflictError

if TYPE_CHECKING:
    from devtools.context.message import MessageId, MessageRole, MessageSource
    from devtools.context.session import SessionId
    from devtools.interactions import ConversationRef
    from devtools.time import Timestamp


@dataclass(frozen=True, slots=True)
class _MessageSnapshot:
    """Represent immutable Message state for private persistence use."""

    id: MessageId
    created_at: Timestamp
    content: str
    role: MessageRole
    source: MessageSource

    @classmethod
    def from_message(cls, message: Message) -> _MessageSnapshot:
        """Capture immutable Message state."""
        return cls(
            id=message.id,
            created_at=message.created_at,
            content=message.content,
            role=message.role,
            source=message.source,
        )

    def to_message(self) -> Message:
        """Restore one immutable Message value."""
        return Message(
            id=self.id,
            created_at=self.created_at,
            content=self.content,
            role=self.role,
            source=self.source,
        )


@dataclass(frozen=True, slots=True)
class _SessionSnapshot:
    """Represent private semantic Session state shared by persistence formats."""

    id: SessionId
    created_at: Timestamp
    messages: tuple[_MessageSnapshot, ...]
    conversations: tuple[ConversationRef, ...]


def capture_session(session: Session) -> _SessionSnapshot:
    """Capture the current semantic state of a Session.

    Callers coordinating with active Runtime work must hold ``session.turn()``
    before invoking a synchronous persistence operation.
    """
    return snapshot_from_values(
        session_id=session.id,
        created_at=session.created_at,
        messages=tuple(
            _MessageSnapshot.from_message(message) for message in session.history
        ),
        conversations=tuple(session.conversations.values()),
    )


def snapshot_from_values(
    *,
    session_id: SessionId,
    created_at: Timestamp,
    messages: tuple[_MessageSnapshot, ...],
    conversations: tuple[ConversationRef, ...],
) -> _SessionSnapshot:
    """Validate and assemble private semantic Session state."""
    _validate_message_ids(messages)
    return _SessionSnapshot(
        id=session_id,
        created_at=created_at,
        messages=messages,
        conversations=tuple(sorted(conversations, key=lambda item: str(item.source))),
    )


def restore_session(snapshot: _SessionSnapshot) -> Session:
    """Reconstruct a new Session with fresh local coordination state."""
    restored_messages: dict[MessageId, Message] = {}
    messages: list[Message] = []
    for message_snapshot in snapshot.messages:
        message = restored_messages.get(message_snapshot.id)
        if message is None:
            message = message_snapshot.to_message()
            restored_messages[message_snapshot.id] = message
        messages.append(message)
    return Session(
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
