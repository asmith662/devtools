# Copyright (c) 2026
"""Immutable retained message transcripts."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from typing import overload

from devtools.context.message import Message


@dataclass(frozen=True, slots=True)
class History(Sequence[Message]):
    """Represent an immutable insertion-ordered transcript of messages.

    :ivar messages: Messages in their retained insertion order.
    """

    messages: tuple[Message, ...] = ()

    def __len__(self) -> int:
        """Return the number of retained messages."""
        return len(self.messages)

    def __iter__(self) -> Iterator[Message]:
        """Iterate over retained messages in insertion order."""
        return iter(self.messages)

    @overload
    def __getitem__(self, index: int) -> Message: ...

    @overload
    def __getitem__(self, index: slice) -> History: ...

    def __getitem__(self, index: int | slice) -> Message | History:
        """Return one message or a domain-preserving message slice."""
        if isinstance(index, slice):
            return History(messages=self.messages[index])
        return self.messages[index]

    def append(self, message: Message) -> History:
        """Return a new history with a message appended in retained order."""
        return History(messages=(*self.messages, message))
