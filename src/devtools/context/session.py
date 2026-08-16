# Copyright (c) 2026
"""Mutable retained interaction-session state."""

from __future__ import annotations

from asyncio import Lock
from contextlib import asynccontextmanager
from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING

from devtools.context.history import History
from devtools.identity import Identity
from devtools.time import Timestamp

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterable, Mapping

    from devtools.agents import ConversationRef
    from devtools.context.message import Message, MessageSource


_EMPTY_HISTORY = History()


@dataclass(frozen=True, slots=True)
class SessionId:
    """Represent an immutable semantic identity for a retained Session.

    :ivar value: Generic identity backing this session-specific identity.
    """

    value: Identity

    @classmethod
    def new(cls) -> SessionId:
        """Generate a new Session identity.

        :returns: Newly generated Session identity.
        """
        return cls(Identity.new())

    @classmethod
    def parse(cls, value: str) -> SessionId:
        """Parse a Session identity from UUID text.

        :param value: UUID string representation.
        :returns: Parsed Session identity.
        :raises ValueError: If the supplied value is not a valid UUID.
        """
        return cls(Identity.parse(value))

    def __str__(self) -> str:
        """Return the canonical Session identity representation.

        :returns: Canonical UUID string.
        """
        return str(self.value)


class Session:
    """Represent a mutable application-owned retained interaction lifecycle."""

    __slots__ = (
        "_conversations",
        "_conversations_view",
        "_created_at",
        "_history",
        "_id",
        "_turn_lock",
    )

    __hash__ = None  # type: ignore[assignment]

    def __init__(
        self,
        *,
        id: SessionId,  # noqa: A002
        created_at: Timestamp,
        history: History = _EMPTY_HISTORY,
        conversations: Iterable[ConversationRef] = (),
    ) -> None:
        """Create or reconstruct retained Session state.

        :param id: Application-owned Session identity.
        :param created_at: Session lifecycle creation time.
        :param history: Current retained message transcript.
        :param conversations: Current unique continuation references by source.
        :raises ValueError: If multiple supplied references share a source.
        """
        self._id = id
        self._created_at = created_at
        self._history = history
        self._conversations: dict[MessageSource, ConversationRef] = {}
        for conversation in conversations:
            if conversation.source in self._conversations:
                msg = "Session cannot contain multiple conversations for one source."
                raise ValueError(msg)
            self._conversations[conversation.source] = conversation
        self._conversations_view: Mapping[MessageSource, ConversationRef] = (
            MappingProxyType(self._conversations)
        )
        self._turn_lock = Lock()

    @classmethod
    def new(cls) -> Session:
        """Create a new empty retained Session lifecycle.

        :returns: Session with fresh identity and creation timestamp.
        """
        return cls(
            id=SessionId.new(),
            created_at=Timestamp.now(),
        )

    @property
    def id(self) -> SessionId:
        """Return this Session's stable application-owned identity."""
        return self._id

    @property
    def created_at(self) -> Timestamp:
        """Return this Session's stable lifecycle creation time."""
        return self._created_at

    @property
    def history(self) -> History:
        """Return the current immutable retained message transcript."""
        return self._history

    @property
    def conversations(self) -> Mapping[MessageSource, ConversationRef]:
        """Return a live read-only view of current continuation references."""
        return self._conversations_view

    def add(self, message: Message) -> None:
        """Append one Message to the current retained transcript."""
        self._history = self._history.append(message)

    def conversation_for(self, source: MessageSource) -> ConversationRef | None:
        """Return the current continuation reference for a source, if any."""
        return self._conversations.get(source)

    def set_conversation(self, conversation: ConversationRef) -> None:
        """Store or replace the current continuation reference for its source."""
        self._conversations[conversation.source] = conversation

    @asynccontextmanager
    async def turn(self) -> AsyncIterator[None]:
        """Exclusively coordinate one complete logical Session turn."""
        async with self._turn_lock:
            yield

    def __eq__(self, other: object) -> bool:
        """Compare mutable Session entities by Python object identity."""
        return self is other
