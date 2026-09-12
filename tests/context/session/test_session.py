# Copyright (c) 2026
"""Tests for mutable retained Session state."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime

import pytest

from devtools.context import History, Message, MessageId, MessageRole, MessageSource
from devtools.context.session import Session, SessionId
from devtools.interactions import ConversationRef
from devtools.time import Timestamp


class _TurnFailureError(Exception):
    """Represent a deterministic exception raised inside a turn test."""


def _message(
    value: str,
    *,
    role: MessageRole = MessageRole.USER,
) -> Message:
    """Create one deterministic contextual message."""
    return Message(
        id=MessageId.parse(value),
        created_at=Timestamp(datetime(2026, 8, 11, tzinfo=UTC)),
        content=value,
        role=role,
        source=MessageSource("test"),
    )


def _ref(source: str, value: str) -> ConversationRef:
    """Create one generic provider continuation reference."""
    return ConversationRef(MessageSource(source), value)


def _session(*, conversations: object = ()) -> Session:
    """Create a deterministic Session with configurable reconstruction refs."""
    return Session(
        id=SessionId.parse("12345678-1234-5678-1234-567812345678"),
        created_at=Timestamp(datetime(2026, 8, 11, 12, 0, tzinfo=UTC)),
        conversations=conversations,  # type: ignore[arg-type]
    )


def test_session_new_has_fresh_lifecycle_identity_and_empty_state() -> None:
    """New Sessions begin with fresh identity, time, History, and no refs."""
    first = Session.new()
    second = Session.new()

    assert first.id != second.id
    assert isinstance(first.created_at, Timestamp)
    assert first.history == History()
    assert dict(first.conversations) == {}


def test_session_direct_reconstruction_preserves_supplied_state() -> None:
    """Constructor is the deterministic reconstruction boundary."""
    message = _message("11111111-1111-1111-1111-111111111111")
    history = History(messages=(message,))
    ref = _ref("codex", "thread-1")
    identifier = SessionId.parse("12345678-1234-5678-1234-567812345678")
    created_at = Timestamp(datetime(2026, 8, 11, 12, 0, tzinfo=UTC))
    session = Session(
        id=identifier,
        created_at=created_at,
        history=history,
        conversations=(ref,),
    )

    assert session.id is identifier
    assert session.created_at is created_at
    assert session.history is history
    assert session.conversation_for(MessageSource("codex")) is ref


def test_session_public_lifecycle_properties_cannot_be_reassigned() -> None:
    """Public properties expose state without exposing direct mutation."""
    session = _session()

    with pytest.raises(AttributeError):
        session.id = SessionId.new()  # type: ignore[misc]
    with pytest.raises(AttributeError):
        session.created_at = Timestamp.now()  # type: ignore[misc]
    with pytest.raises(AttributeError):
        session.history = History()  # type: ignore[misc]
    with pytest.raises(AttributeError):
        session.conversations = {}  # type: ignore[misc]


def test_session_adds_all_message_roles_and_preserves_snapshots_and_duplicates() -> (
    None
):
    """Session mutation composes immutable History without role restrictions."""
    user = _message("11111111-1111-1111-1111-111111111111")
    assistant = _message(
        "22222222-2222-2222-2222-222222222222",
        role=MessageRole.ASSISTANT,
    )
    system = _message(
        "33333333-3333-3333-3333-333333333333",
        role=MessageRole.SYSTEM,
    )
    session = _session()
    before = session.history

    assert session.add(user) is None  # type: ignore[func-returns-value]
    session.add(assistant)
    session.add(system)
    session.add(user)

    assert before == History()
    assert session.history.messages == (user, assistant, system, user)
    assert session.history[-1] is user
    assert session.history[0].id == user.id
    assert session.history[0].created_at == user.created_at
    assert session.history[0].content == user.content
    assert session.history[0].role is user.role
    assert session.history[0].source is user.source


@pytest.mark.parametrize(
    "conversations",
    [
        (_ref("codex", "thread-1"),),
        [_ref("codex", "thread-1")],
        (_ref(source, value) for source, value in (("codex", "thread-1"),)),
    ],
)
def test_session_constructor_materializes_supported_conversation_iterables(
    conversations: object,
) -> None:
    """Tuple, list, and generator reconstruction inputs are consumed once."""
    session = _session(conversations=conversations)

    assert session.conversation_for(MessageSource("codex")) == _ref("codex", "thread-1")


def test_session_rejects_duplicate_constructor_sources_by_value() -> None:
    """Direct reconstruction remains unambiguous for equal source values."""
    duplicate_sources = (
        ConversationRef(MessageSource("codex"), "thread-1"),
        ConversationRef(MessageSource("codex"), "thread-2"),
    )

    with pytest.raises(ValueError, match="multiple conversations"):
        _session(conversations=duplicate_sources)


def test_session_conversations_are_live_read_only_source_keyed_state() -> None:
    """Read-only mapping exposure tracks controlled Session mutations."""
    session = _session()
    view = session.conversations
    codex = _ref("codex", "thread-1")
    qwen = _ref("qwen", "thread-2")

    assert session.conversation_for(MessageSource("missing")) is None
    assert session.set_conversation(codex) is None  # type: ignore[func-returns-value]
    session.set_conversation(qwen)

    assert view[MessageSource("codex")] is codex
    assert view[MessageSource("qwen")] is qwen
    assert set(view) == {MessageSource("codex"), MessageSource("qwen")}
    with pytest.raises(TypeError):
        view[MessageSource("local")] = _ref("local", "thread-3")  # type: ignore[index]
    with pytest.raises(TypeError):
        del view[MessageSource("codex")]  # type: ignore[attr-defined]


def test_session_replaces_current_conversation_for_one_source() -> None:
    """A newer same-source reference replaces prior active continuation state."""
    first = _ref("codex", "thread-1")
    replacement = _ref("codex", "thread-2")
    session = _session(conversations=(first,))

    session.set_conversation(replacement)

    assert session.conversation_for(MessageSource("codex")) is replacement
    assert tuple(session.conversations.values()) == (replacement,)


def test_sessions_use_object_identity_equality_and_are_unhashable() -> None:
    """Mutable Session entities separate Python equality from SessionId values."""
    first = _session()
    second = _session()

    assert first is not second
    assert first != second
    same_first = first
    assert first is same_first
    assert first.id == second.id
    with pytest.raises(TypeError, match="unhashable"):
        hash(first)


def test_session_lifecycle_identity_and_creation_time_remain_stable() -> None:
    """Controlled state mutation does not replace lifecycle identity or time."""
    session = _session()
    identifier = session.id
    created_at = session.created_at

    session.add(_message("11111111-1111-1111-1111-111111111111"))
    session.set_conversation(_ref("codex", "thread-1"))

    assert session.id is identifier
    assert session.created_at is created_at


def test_multiple_sessions_can_hold_the_same_provider_reference() -> None:
    """Session state does not impose provider-global continuation uniqueness."""
    ref = _ref("codex", "thread-1")

    first = _session(conversations=(ref,))
    second = _session(conversations=(ref,))

    assert first.conversation_for(MessageSource("codex")) is ref
    assert second.conversation_for(MessageSource("codex")) is ref


def test_session_turn_acquires_and_releases_normally() -> None:
    """The public turn context provides local asynchronous coordination."""
    session = _session()

    async def exercise() -> bool:
        async with session.turn():
            return True

    assert asyncio.run(exercise())


def test_session_constructed_outside_a_loop_yields_no_turn_value() -> None:
    """Synchronous construction supports first acquisition in an event loop."""
    session = Session.new()

    async def exercise() -> None:
        async with session.turn() as value:
            assert value is None

    asyncio.run(exercise())


def test_session_turn_releases_after_exception() -> None:
    """Turn exceptions propagate without retaining Session coordination."""
    session = _session()

    async def exercise() -> bool:
        with pytest.raises(_TurnFailureError):
            async with session.turn():
                raise _TurnFailureError
        async with session.turn():
            return True

    assert asyncio.run(exercise())


def test_session_turn_serializes_same_session_workers() -> None:
    """A second same-Session worker enters only after the first exits."""
    session = _session()

    async def exercise() -> list[str]:
        first_entered = asyncio.Event()
        release_first = asyncio.Event()
        second_attempted = asyncio.Event()
        second_entered = asyncio.Event()
        order: list[str] = []

        async def first() -> None:
            async with session.turn():
                order.append("first-entered")
                first_entered.set()
                await release_first.wait()
                order.append("first-exited")

        async def second() -> None:
            second_attempted.set()
            async with session.turn():
                order.append("second-entered")
                second_entered.set()

        first_task = asyncio.create_task(first())
        await first_entered.wait()
        second_task = asyncio.create_task(second())
        await second_attempted.wait()
        assert not second_entered.is_set()
        release_first.set()
        await second_entered.wait()
        await asyncio.gather(first_task, second_task)
        return order

    assert asyncio.run(exercise()) == [
        "first-entered",
        "first-exited",
        "second-entered",
    ]


def test_session_turn_allows_different_sessions_to_proceed_concurrently() -> None:
    """Independent Session objects own independent coordination state."""
    first = _session()
    second = _session()

    async def exercise() -> None:
        first_entered = asyncio.Event()
        second_entered = asyncio.Event()
        release = asyncio.Event()

        async def hold(session: Session, entered: asyncio.Event) -> None:
            async with session.turn():
                entered.set()
                await release.wait()

        first_task = asyncio.create_task(hold(first, first_entered))
        second_task = asyncio.create_task(hold(second, second_entered))
        await first_entered.wait()
        await second_entered.wait()
        release.set()
        await asyncio.gather(first_task, second_task)

    asyncio.run(exercise())


def test_session_turns_do_not_share_locks_for_equal_session_ids() -> None:
    """Separate reconstructed Session objects coordinate only locally."""
    first = _session()
    second = _session()

    async def exercise() -> None:
        first_entered = asyncio.Event()
        second_entered = asyncio.Event()
        release = asyncio.Event()

        async def hold(session: Session, entered: asyncio.Event) -> None:
            async with session.turn():
                entered.set()
                await release.wait()

        first_task = asyncio.create_task(hold(first, first_entered))
        second_task = asyncio.create_task(hold(second, second_entered))
        await first_entered.wait()
        await second_entered.wait()
        release.set()
        await asyncio.gather(first_task, second_task)

    assert first.id == second.id
    asyncio.run(exercise())


def test_session_turn_cancellation_releases_coordination() -> None:
    """Cancellation while holding a turn releases it for a later caller."""
    session = _session()

    async def exercise() -> bool:
        entered = asyncio.Event()
        waiting = asyncio.Event()

        async def hold() -> None:
            async with session.turn():
                entered.set()
                await waiting.wait()

        task = asyncio.create_task(hold())
        await entered.wait()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        async with session.turn():
            return True

    assert asyncio.run(exercise())


def test_session_turn_waiter_cancellation_does_not_acquire_coordination() -> None:
    """Cancellation while waiting propagates and leaves turn state available."""
    session = _session()

    async def exercise() -> bool:
        waiter_attempted = asyncio.Event()
        waiter_entered = asyncio.Event()

        async with session.turn():

            async def wait_for_turn() -> None:
                waiter_attempted.set()
                async with session.turn():
                    waiter_entered.set()

            waiter = asyncio.create_task(wait_for_turn())
            await waiter_attempted.wait()
            waiter.cancel()
            with pytest.raises(asyncio.CancelledError):
                await waiter
            assert not waiter_entered.is_set()

        async with session.turn():
            return True

    assert asyncio.run(exercise())
