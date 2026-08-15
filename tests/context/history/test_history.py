# Copyright (c) 2026
"""Tests for immutable message history."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from devtools.context import History
from devtools.context.history import History as HistoryFromSubmodule
from devtools.context.message import Message, MessageId, MessageRole, MessageSource
from devtools.time import Timestamp


def _message(
    value: str,
    *,
    content: str | None = None,
    timestamp: datetime | None = None,
) -> Message:
    """Create one deterministic message with configurable retained metadata."""
    return Message(
        id=MessageId.parse(value),
        created_at=Timestamp(timestamp or datetime(2026, 8, 10, tzinfo=UTC)),
        content=content or value,
        role=MessageRole.USER,
        source=MessageSource("test"),
    )


def _messages() -> tuple[Message, Message, Message, Message]:
    """Create four distinct deterministic transcript messages."""
    return (
        _message("11111111-1111-1111-1111-111111111111", content="one"),
        _message("22222222-2222-2222-2222-222222222222", content="two"),
        _message("33333333-3333-3333-3333-333333333333", content="three"),
        _message("44444444-4444-4444-4444-444444444444", content="four"),
    )


def test_context_root_and_submodule_expose_the_same_history_type() -> None:
    """History has matching aggregate-root and canonical submodule imports."""
    assert History is HistoryFromSubmodule


def test_history_supports_empty_and_direct_deterministic_construction() -> None:
    """The constructor represents empty and pre-existing message transcripts."""
    first, second, _, _ = _messages()
    empty = History()
    history = History(messages=(first, second))

    assert empty.messages == ()
    assert len(empty) == 0
    assert tuple(empty) == ()
    assert history.messages == (first, second)
    assert history[0] is first
    assert history[1] is second


def test_history_preserves_insertion_order_not_message_timestamps() -> None:
    """Tuple position, rather than Message metadata, determines transcript order."""
    later = _message(
        "11111111-1111-1111-1111-111111111111",
        timestamp=datetime(2026, 8, 11, tzinfo=UTC),
    )
    earlier = _message(
        "22222222-2222-2222-2222-222222222222",
        timestamp=datetime(2026, 8, 9, tzinfo=UTC),
    )
    history = History(messages=(later, earlier))

    assert tuple(history) == (later, earlier)


def test_history_provides_normal_sequence_length_iteration_and_membership() -> None:
    """Sequence operations retain order and use Message value equality."""
    first, second, third, _ = _messages()
    history = History(messages=(first, second, third))
    equal_first = _message("11111111-1111-1111-1111-111111111111", content="one")
    missing = _message("44444444-4444-4444-4444-444444444444", content="missing")
    expected_length = len((first, second, third))

    assert len(history) == expected_length
    assert list(history) == [first, second, third]
    assert equal_first in history
    assert missing not in history


def test_history_integer_indexing_supports_positive_and_negative_positions() -> None:
    """Integer indices use standard tuple semantics."""
    first, second, third, fourth = _messages()
    history = History(messages=(first, second, third, fourth))

    assert history[0] is first
    assert history[1] is second
    assert history[3] is fourth
    assert history[-1] is fourth
    assert history[-2] is third

    with pytest.raises(IndexError):
        _ = history[4]

    with pytest.raises(IndexError):
        _ = history[-5]


def test_history_slices_return_history_with_tuple_selection_semantics() -> None:
    """Every slice preserves the domain while retaining normal tuple selection."""
    first, second, third, fourth = _messages()
    history = History(messages=(first, second, third, fourth))

    middle = history[1:3]
    full = history[:]
    empty = history[:0]
    trailing = history[-2:]
    stepped = history[::2]
    reversed_history = history[::-1]

    assert isinstance(middle, History)
    assert middle.messages == (second, third)
    assert full == history
    assert empty.messages == ()
    assert trailing.messages == (third, fourth)
    assert stepped.messages == (first, third)
    assert reversed_history.messages == (fourth, third, second, first)
    assert history.messages == (first, second, third, fourth)


def test_history_append_returns_a_new_history_without_transforming_message() -> None:
    """Appending retains both original transcript and supplied message values."""
    first, second, third, _ = _messages()
    original = History(messages=(first, second))
    appended = original.append(third)
    from_empty = History().append(first)

    assert isinstance(appended, History)
    assert original.messages == (first, second)
    assert appended.messages == (first, second, third)
    assert appended[-1] is third
    assert appended[-1].id == third.id
    assert appended[-1].created_at == third.created_at
    assert appended[-1].content == third.content
    assert appended[-1].role is third.role
    assert appended[-1].source is third.source
    assert from_empty.messages == (first,)


def test_history_uses_ordered_immutable_value_and_hash_semantics() -> None:
    """Equal sequences compare and hash equally, while ordering remains material."""
    first, second, _, _ = _messages()
    equal = History(messages=(first, second))
    same_values = History(messages=(first, second))
    reversed_values = History(messages=(second, first))
    different = History(
        messages=(
            first,
            _message(
                "33333333-3333-3333-3333-333333333333",
                content="different",
            ),
        ),
    )

    assert equal == same_values
    assert hash(equal) == hash(same_values)
    assert equal != reversed_values
    assert equal != different
    assert {equal} == {same_values}

    with pytest.raises(FrozenInstanceError):
        equal.messages = ()  # type: ignore[misc]


def test_history_retains_duplicate_messages_as_distinct_transcript_positions() -> None:
    """History is an ordered transcript rather than a deduplicating set."""
    message, _, _, _ = _messages()
    history = History(messages=(message, message))
    expected_length = len((message, message))

    assert len(history) == expected_length
    assert history.messages == (message, message)
    assert history[0] is message
    assert history[1] is message


def test_history_inherits_standard_sequence_conveniences() -> None:
    """Standard Sequence helpers retain ordinary Message value semantics."""
    first, second, third, fourth = _messages()
    history = History(messages=(first, second, third, first))
    expected_count = len((first, first))

    assert history.index(first) == 0
    assert history.count(first) == expected_count
    assert tuple(reversed(history)) == (first, third, second, first)

    with pytest.raises(ValueError, match=r"^$"):
        history.index(fourth)
