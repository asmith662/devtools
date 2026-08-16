# Copyright (c) 2026
"""Deterministic Runtime coordination tests."""
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pytest

import devtools.runtime as runtime_package
from devtools.agents import Agent, AgentTurn, ConversationRef
from devtools.context import Message, MessageRole, MessageSource, Session
from devtools.runtime import Runtime

if TYPE_CHECKING:
    from collections.abc import Sequence


class FakeAgent:
    """A structural agent fake with deterministic call controls."""

    def __init__(
        self,
        source: MessageSource,
        turns: Sequence[AgentTurn] = (),
        *,
        error: Exception | None = None,
        entered: asyncio.Event | None = None,
        release: asyncio.Event | None = None,
    ) -> None:
        """Initialize a fake with scripted results or one failure."""
        self._source = source
        self._turns = list(turns)
        self._error = error
        self._entered = entered
        self._release = release
        self.calls: list[tuple[Message, ConversationRef | None]] = []

    @property
    def source(self) -> MessageSource:
        """Return the fake agent source."""
        return self._source

    async def send(
        self,
        message: Message,
        *,
        conversation: ConversationRef | None = None,
    ) -> AgentTurn:
        """Record one call and return the next configured result."""
        self.calls.append((message, conversation))
        if self._entered is not None:
            self._entered.set()
        if self._release is not None:
            await self._release.wait()
        if self._error is not None:
            raise self._error
        return self._turns.pop(0)


def _message(
    content: str,
    *,
    role: MessageRole = MessageRole.USER,
    source: str = "user",
) -> Message:
    """Create a message with concise test defaults."""
    return Message.new(content, role=role, source=MessageSource(source))


def _ref(source: str, value: str) -> ConversationRef:
    """Create an opaque test continuation reference."""
    return ConversationRef(MessageSource(source), value)


def test_runtime_root_api_exports_only_runtime() -> None:
    """The Runtime package exposes only its coordination service."""
    assert runtime_package.__all__ == ["Runtime"]
    assert runtime_package.Runtime is Runtime


def test_runtime_coordinates_a_fresh_successful_turn() -> None:
    """A fresh session retains input, output, and returned continuation."""
    async def exercise() -> None:
        session = Session.new()
        input_message = _message("input")
        response = _message("response", role=MessageRole.ASSISTANT, source="agent")
        conversation = _ref("agent", "thread-1")
        returned = AgentTurn(response, conversation)
        fake: Agent = FakeAgent(MessageSource("agent"), (returned,))

        turn = await Runtime().send(
            session=session,
            agent=fake,
            message=input_message,
        )

        assert turn is returned
        assert session.history.messages == (input_message, response)
        assert session.history[0] is input_message
        assert session.history[1] is response
        assert session.conversation_for(MessageSource("agent")) is conversation
        assert isinstance(fake, FakeAgent)
        assert fake.calls == [(input_message, None)]

    asyncio.run(exercise())


def test_runtime_uses_and_replaces_the_current_continuation() -> None:
    """A continued turn uses the stored ref and replaces it on success."""
    async def exercise() -> None:
        previous = _ref("agent", "thread-old")
        session = Session.new()
        session.set_conversation(previous)
        input_message = _message("input")
        response = _message("response", role=MessageRole.ASSISTANT, source="agent")
        replacement = _ref("agent", "thread-new")
        fake = FakeAgent(
            MessageSource("agent"),
            (AgentTurn(response, replacement),),
        )

        await Runtime().send(session=session, agent=fake, message=input_message)

        assert fake.calls == [(input_message, previous)]
        assert session.history.messages == (input_message, response)
        assert session.conversation_for(MessageSource("agent")) is replacement

    asyncio.run(exercise())


def test_runtime_keeps_existing_continuation_when_turn_is_stateless() -> None:
    """A None continuation does not clear the current source continuation."""
    async def exercise() -> None:
        previous = _ref("agent", "thread-old")
        session = Session.new()
        session.set_conversation(previous)
        response = _message("response", role=MessageRole.ASSISTANT, source="agent")
        fake = FakeAgent(MessageSource("agent"), (AgentTurn(response),))

        await Runtime().send(
            session=session,
            agent=fake,
            message=_message("input"),
        )

        assert session.conversation_for(MessageSource("agent")) is previous

    asyncio.run(exercise())


def test_runtime_accepts_all_message_roles_and_independent_input_source() -> None:
    """Runtime remains role-neutral and does not require matching sources."""
    async def exercise() -> None:
        session = Session.new()
        source = MessageSource("agent")
        inputs = tuple(
            _message(role.value, role=role, source="caller")
            for role in MessageRole
        )
        responses = tuple(
            _message(
                f"response-{role.value}",
                role=MessageRole.ASSISTANT,
                source="agent",
            )
            for role in MessageRole
        )
        fake = FakeAgent(source, tuple(AgentTurn(response) for response in responses))

        for message in inputs:
            await Runtime().send(session=session, agent=fake, message=message)

        assert [call[0] for call in fake.calls] == list(inputs)
        assert all(call[0].source != source for call in fake.calls)
        assert session.history.messages == tuple(
            item for pair in zip(inputs, responses, strict=True) for item in pair
        )

    asyncio.run(exercise())


def test_runtime_retains_repeated_submission_of_the_same_message() -> None:
    """Each invocation retains the supplied Message again without cloning it."""
    async def exercise() -> None:
        session = Session.new()
        input_message = _message("input")
        first = _message("first", role=MessageRole.ASSISTANT, source="agent")
        second = _message("second", role=MessageRole.ASSISTANT, source="agent")
        fake = FakeAgent(
            MessageSource("agent"),
            (AgentTurn(first), AgentTurn(second)),
        )
        runtime = Runtime()

        await runtime.send(session=session, agent=fake, message=input_message)
        await runtime.send(session=session, agent=fake, message=input_message)

        assert session.history.messages == (input_message, first, input_message, second)
        assert session.history[0] is session.history[2] is input_message
        assert session.history[0].id == session.history[2].id

    asyncio.run(exercise())


def test_runtime_preserves_input_and_continuation_when_agent_raises() -> None:
    """Agent exceptions propagate after recording only the input message."""
    async def exercise() -> None:
        previous = _ref("agent", "thread-old")
        session = Session.new()
        session.set_conversation(previous)
        input_message = _message("input")
        error = LookupError("agent failed")
        fake = FakeAgent(MessageSource("agent"), error=error)

        with pytest.raises(LookupError) as raised:
            await Runtime().send(session=session, agent=fake, message=input_message)

        assert raised.value is error
        assert session.history.messages == (input_message,)
        assert session.conversation_for(MessageSource("agent")) is previous
        assert fake.calls == [(input_message, previous)]

    asyncio.run(exercise())


def test_runtime_rejects_a_returned_message_from_another_source() -> None:
    """Runtime alone validates the selected agent against its returned message."""
    async def exercise() -> None:
        previous = _ref("agent", "thread-old")
        session = Session.new()
        session.set_conversation(previous)
        input_message = _message("input")
        invalid_response = _message(
            "invalid",
            role=MessageRole.ASSISTANT,
            source="other-agent",
        )
        invalid_ref = _ref("other-agent", "other-thread")
        fake = FakeAgent(
            MessageSource("agent"),
            (AgentTurn(invalid_response, invalid_ref),),
        )

        with pytest.raises(
            ValueError,
            match=r"^Agent turn message source does not match agent source\.$",
        ):
            await Runtime().send(session=session, agent=fake, message=input_message)

        assert session.history.messages == (input_message,)
        assert session.conversation_for(MessageSource("agent")) is previous
        assert fake.calls == [(input_message, previous)]

    asyncio.run(exercise())


def test_runtime_cancellation_while_waiting_leaves_session_unchanged() -> None:
    """Cancellation before turn acquisition neither records nor sends input."""
    async def exercise() -> None:
        session = Session.new()
        fake = FakeAgent(
            MessageSource("agent"),
            (
                AgentTurn(
                    _message(
                        "response",
                        role=MessageRole.ASSISTANT,
                        source="agent",
                    ),
                ),
            ),
        )
        runtime_started = asyncio.Event()

        async with session.turn():
            async def invoke() -> AgentTurn:
                runtime_started.set()
                return await Runtime().send(
                    session=session,
                    agent=fake,
                    message=_message("input"),
                )

            task = asyncio.create_task(invoke())
            await runtime_started.wait()
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task

            assert session.history.messages == ()
            assert fake.calls == []

    asyncio.run(exercise())


def test_runtime_cancellation_during_agent_releases_the_session_turn() -> None:
    """Cancellation in flight keeps input only and releases Session coordination."""
    async def exercise() -> None:
        session = Session.new()
        previous = _ref("agent", "thread-old")
        session.set_conversation(previous)
        input_message = _message("input")
        entered = asyncio.Event()
        release = asyncio.Event()
        fake = FakeAgent(
            MessageSource("agent"),
            (
                AgentTurn(
                    _message(
                        "response",
                        role=MessageRole.ASSISTANT,
                        source="agent",
                    ),
                ),
            ),
            entered=entered,
            release=release,
        )
        task = asyncio.create_task(
            Runtime().send(session=session, agent=fake, message=input_message),
        )
        await entered.wait()
        assert session.history.messages == (input_message,)

        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

        assert session.history.messages == (input_message,)
        assert session.conversation_for(MessageSource("agent")) is previous
        async with session.turn():
            pass

    asyncio.run(exercise())


def test_runtime_serializes_complete_turns_for_one_session() -> None:
    """A second same-session call cannot invoke its agent before the first ends."""
    async def exercise() -> None:
        runtime = Runtime()
        session = Session.new()
        entered_a = asyncio.Event()
        release_a = asyncio.Event()
        entered_b = asyncio.Event()
        started_b = asyncio.Event()
        input_a = _message("input-a")
        response_a = _message("response-a", role=MessageRole.ASSISTANT, source="a")
        input_b = _message("input-b")
        response_b = _message("response-b", role=MessageRole.ASSISTANT, source="b")
        agent_a = FakeAgent(
            MessageSource("a"),
            (AgentTurn(response_a),),
            entered=entered_a,
            release=release_a,
        )
        agent_b = FakeAgent(
            MessageSource("b"),
            (AgentTurn(response_b),),
            entered=entered_b,
        )

        task_a = asyncio.create_task(
            runtime.send(session=session, agent=agent_a, message=input_a),
        )
        await entered_a.wait()

        async def invoke_b() -> AgentTurn:
            started_b.set()
            return await runtime.send(session=session, agent=agent_b, message=input_b)

        task_b = asyncio.create_task(invoke_b())
        await started_b.wait()
        assert agent_b.calls == []
        assert len(session.history) == 1
        assert session.history[0] is input_a

        release_a.set()
        await entered_b.wait()
        await task_a
        await task_b

        assert session.history.messages == (
            input_a,
            response_a,
            input_b,
            response_b,
        )

    asyncio.run(exercise())


def test_runtime_hands_a_replacement_continuation_to_a_queued_same_source_turn(
) -> None:
    """A queued same-source turn receives the prior turn's replacement ref."""
    async def exercise() -> None:
        runtime = Runtime()
        source = MessageSource("agent")
        initial = ConversationRef(source, "thread-a")
        replacement = ConversationRef(source, "thread-b")
        session = Session.new()
        session.set_conversation(initial)
        entered_a = asyncio.Event()
        release_a = asyncio.Event()
        entered_b = asyncio.Event()
        started_b = asyncio.Event()
        input_a = _message("input-a")
        response_a = _message("response-a", role=MessageRole.ASSISTANT, source="agent")
        input_b = _message("input-b")
        response_b = _message("response-b", role=MessageRole.ASSISTANT, source="agent")
        agent_a = FakeAgent(
            source,
            (AgentTurn(response_a, replacement),),
            entered=entered_a,
            release=release_a,
        )
        agent_b = FakeAgent(
            source,
            (AgentTurn(response_b),),
            entered=entered_b,
        )
        task_a = asyncio.create_task(
            runtime.send(session=session, agent=agent_a, message=input_a),
        )
        await entered_a.wait()
        assert agent_a.calls == [(input_a, initial)]

        async def invoke_b() -> AgentTurn:
            started_b.set()
            return await runtime.send(session=session, agent=agent_b, message=input_b)

        task_b = asyncio.create_task(invoke_b())
        await started_b.wait()
        assert agent_b.calls == []

        release_a.set()
        await entered_b.wait()
        await asyncio.gather(task_a, task_b)

        assert agent_b.calls == [(input_b, replacement)]
        assert agent_b.calls[0][1] is replacement
        assert session.history.messages == (
            input_a,
            response_a,
            input_b,
            response_b,
        )

    asyncio.run(exercise())


def test_runtime_allows_different_sessions_to_run_concurrently() -> None:
    """One Runtime instance adds no serialization across distinct Sessions."""
    async def exercise() -> None:
        runtime = Runtime()
        release = asyncio.Event()
        entered_a = asyncio.Event()
        entered_b = asyncio.Event()
        agent_a = FakeAgent(
            MessageSource("a"),
            (
                AgentTurn(
                    _message(
                        "response-a",
                        role=MessageRole.ASSISTANT,
                        source="a",
                    ),
                ),
            ),
            entered=entered_a,
            release=release,
        )
        agent_b = FakeAgent(
            MessageSource("b"),
            (
                AgentTurn(
                    _message(
                        "response-b",
                        role=MessageRole.ASSISTANT,
                        source="b",
                    ),
                ),
            ),
            entered=entered_b,
            release=release,
        )

        task_a = asyncio.create_task(
            runtime.send(session=Session.new(), agent=agent_a, message=_message("a")),
        )
        task_b = asyncio.create_task(
            runtime.send(session=Session.new(), agent=agent_b, message=_message("b")),
        )
        await asyncio.gather(entered_a.wait(), entered_b.wait())
        assert len(agent_a.calls) == 1
        assert len(agent_b.calls) == 1

        release.set()
        await asyncio.gather(task_a, task_b)

    asyncio.run(exercise())
