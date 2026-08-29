# Copyright (c) 2026
"""Deterministic Runtime coordination tests."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pytest

import devtools.runtime as runtime_package
from devtools.agents import Agent, AgentTurn, ConversationRef
from devtools.context import Message, MessageRole, MessageSource, Session
from devtools.evidence import Attempt, AttemptObserver, AttemptState
from devtools.runtime import Runtime

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from devtools.time import Timestamp


class FakeAgent:
    """A structural agent fake with deterministic call controls."""

    def __init__(
        self,
        source: MessageSource,
        turns: Sequence[AgentTurn] = (),
        *,
        error: BaseException | None = None,
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


class FakeObserver:
    """A structural observer fake with ordered callback controls."""

    def __init__(
        self,
        *,
        started_error: BaseException | None = None,
        finished_error: BaseException | None = None,
        on_started: Callable[[Attempt], None] | None = None,
    ) -> None:
        """Initialize recorded lifecycle callbacks and optional failures."""
        self._started_error = started_error
        self._finished_error = finished_error
        self._on_started = on_started
        self.events: list[tuple[str, Attempt]] = []
        self.started: list[Attempt] = []
        self.finished: list[Attempt] = []

    def attempt_started(self, attempt: Attempt) -> None:
        """Record one started callback and optionally fail it."""
        self.events.append(("started", attempt))
        self.started.append(attempt)
        if self._on_started is not None:
            self._on_started(attempt)
        if self._started_error is not None:
            raise self._started_error

    def attempt_finished(self, attempt: Attempt) -> None:
        """Record one finished callback and optionally fail it."""
        self.events.append(("finished", attempt))
        self.finished.append(attempt)
        if self._finished_error is not None:
            raise self._finished_error


class ProcessControl(BaseException):
    """Represent a safe non-cancellation process-control exception in tests."""


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


def test_runtime_observer_configuration_is_optional_fixed_and_structural() -> None:
    """Runtime retains one readable fixed structural observer configuration."""
    observer: AttemptObserver = FakeObserver()
    runtime = Runtime(observer=observer)

    assert Runtime().observer is None
    assert runtime.observer is observer
    with pytest.raises(AttributeError):
        runtime.observer = FakeObserver()  # type: ignore[misc]


def test_runtime_observes_a_successful_turn_with_one_live_attempt() -> None:
    """An observed success retains the exact live Attempt across callbacks."""

    async def exercise() -> None:
        session = Session.new()
        input_message = _message("input", source="caller")
        response = _message("response", role=MessageRole.ASSISTANT, source="agent")
        conversation = _ref("agent", "thread")
        returned = AgentTurn(response, conversation)
        fake = FakeAgent(MessageSource("agent"), (returned,))

        def assert_started(attempt: Attempt) -> None:
            assert attempt.state is AttemptState.RUNNING
            assert session.history.messages == (input_message,)
            assert attempt.session_id is session.id
            assert attempt.message_id is input_message.id
            assert attempt.agent_source is fake.source
            assert fake.calls == []

        observer = FakeObserver(on_started=assert_started)

        turn = await Runtime(observer=observer).send(
            session=session,
            agent=fake,
            message=input_message,
        )

        assert turn is returned
        assert session.history.messages == (input_message, response)
        assert session.conversation_for(fake.source) is conversation
        assert len(observer.started) == len(observer.finished) == 1
        attempt = observer.started[0]
        assert observer.finished[0] is attempt
        assert attempt.session_id is session.id
        assert attempt.message_id is input_message.id
        assert attempt.agent_source is fake.source
        assert observer.events[0] == ("started", attempt)
        assert observer.events[1] == ("finished", attempt)
        assert attempt.state is AttemptState.SUCCEEDED
        assert attempt.completed_at is not None

    asyncio.run(exercise())


def test_runtime_observer_preserves_existing_continuation_and_distinct_attempts() -> (
    None
):
    """Observed repeated submissions retain continuation semantics and new IDs."""

    async def exercise() -> None:
        source = MessageSource("agent")
        previous = _ref("agent", "old")
        replacement = _ref("agent", "new")
        session = Session.new()
        session.set_conversation(previous)
        message = _message("input")
        first = _message("first", role=MessageRole.ASSISTANT, source="agent")
        second = _message("second", role=MessageRole.ASSISTANT, source="agent")
        fake = FakeAgent(source, (AgentTurn(first, replacement), AgentTurn(second)))
        observer = FakeObserver()
        runtime = Runtime(observer=observer)

        await runtime.send(session=session, agent=fake, message=message)
        await runtime.send(session=session, agent=fake, message=message)

        assert fake.calls == [(message, previous), (message, replacement)]
        assert session.conversation_for(source) is replacement
        assert [attempt.message_id for attempt in observer.started] == [
            message.id,
            message.id,
        ]
        assert observer.started[0].id != observer.started[1].id
        assert all(
            attempt.state is AttemptState.SUCCEEDED for attempt in observer.finished
        )

    asyncio.run(exercise())


def test_runtime_does_not_create_attempt_when_input_retention_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Input retention failure occurs before observer admission and Agent invocation."""

    async def exercise() -> None:
        session = Session.new()
        message = _message("input")
        error = LookupError("input retention failed")

        def fail_add(_: Session, __: Message) -> None:
            raise error

        monkeypatch.setattr(Session, "add", fail_add)
        observer = FakeObserver()
        fake = FakeAgent(MessageSource("agent"))

        with pytest.raises(LookupError) as raised:
            await Runtime(observer=observer).send(
                session=session,
                agent=fake,
                message=message,
            )

        assert raised.value is error
        assert observer.started == observer.finished == []
        assert fake.calls == []

    asyncio.run(exercise())


def test_runtime_does_not_notify_when_attempt_creation_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Attempt construction failure occurs before observer admission and sending."""

    async def exercise() -> None:
        session = Session.new()
        message = _message("input")
        error = LookupError("attempt creation failed")

        def fail_new(**_: object) -> Attempt:
            raise error

        monkeypatch.setattr(Attempt, "new", fail_new)
        observer = FakeObserver()
        fake = FakeAgent(MessageSource("agent"))

        with pytest.raises(LookupError) as raised:
            await Runtime(observer=observer).send(
                session=session,
                agent=fake,
                message=message,
            )

        assert raised.value is error
        assert session.history.messages == (message,)
        assert observer.started == observer.finished == []
        assert fake.calls == []

    asyncio.run(exercise())


def test_runtime_start_observer_failure_fails_attempt_without_sending() -> None:
    """Start observation failure is primary while best-effort cleanup finishes."""

    async def exercise() -> None:
        previous = _ref("agent", "old")
        session = Session.new()
        session.set_conversation(previous)
        message = _message("input")
        error = LookupError("start failed")
        observer = FakeObserver(started_error=error)
        fake = FakeAgent(MessageSource("agent"))

        with pytest.raises(LookupError) as raised:
            await Runtime(observer=observer).send(
                session=session,
                agent=fake,
                message=message,
            )

        assert raised.value is error
        assert session.history.messages == (message,)
        assert session.conversation_for(fake.source) is previous
        assert fake.calls == []
        assert len(observer.started) == len(observer.finished) == 1
        assert observer.started[0] is observer.finished[0]
        assert observer.finished[0].state is AttemptState.FAILED
        async with session.turn():
            pass

    asyncio.run(exercise())


def test_runtime_start_observer_cancellation_cancels_attempt_without_sending() -> None:
    """Start-callback cancellation is primary and terminalizes as cancelled."""

    async def exercise() -> None:
        session = Session.new()
        message = _message("input")
        error = asyncio.CancelledError()
        observer = FakeObserver(started_error=error)
        fake = FakeAgent(MessageSource("agent"))

        with pytest.raises(asyncio.CancelledError) as raised:
            await Runtime(observer=observer).send(
                session=session,
                agent=fake,
                message=message,
            )

        assert raised.value is error
        assert session.history.messages == (message,)
        assert fake.calls == []
        assert observer.finished[0].state is AttemptState.CANCELLED

    asyncio.run(exercise())


def test_runtime_propagates_start_observer_process_control_without_cleanup() -> None:
    """Non-cancellation BaseException is not classified as an Attempt outcome."""

    async def exercise() -> None:
        session = Session.new()
        error = ProcessControl()
        observer = FakeObserver(started_error=error)
        fake = FakeAgent(MessageSource("agent"))

        with pytest.raises(ProcessControl) as raised:
            await Runtime(observer=observer).send(
                session=session,
                agent=fake,
                message=_message("input"),
            )

        assert raised.value is error
        assert fake.calls == []
        assert observer.started[0].state is AttemptState.RUNNING
        assert observer.finished == []

    asyncio.run(exercise())


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


def test_runtime_without_observer_never_creates_an_attempt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An unobserved turn never calls Attempt.new()."""

    async def exercise() -> None:
        session = Session.new()
        input_message = _message("input")
        response = _message("response", role=MessageRole.ASSISTANT, source="agent")
        conversation = _ref("agent", "thread")
        returned = AgentTurn(response, conversation)
        fake = FakeAgent(MessageSource("agent"), (returned,))

        def fail_new(**_: object) -> Attempt:
            msg = "Runtime created an Attempt without an observer."
            raise AssertionError(msg)

        monkeypatch.setattr(Attempt, "new", fail_new)
        runtime = Runtime()

        turn = await runtime.send(
            session=session,
            agent=fake,
            message=input_message,
        )

        assert runtime.observer is None
        assert turn is returned
        assert fake.calls == [(input_message, None)]
        assert session.history.messages == (input_message, response)
        assert session.conversation_for(fake.source) is conversation

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
            _message(role.value, role=role, source="caller") for role in MessageRole
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


def test_runtime_observes_agent_failure_without_replacing_primary_error() -> None:
    """Agent failure terminalizes Attempt while preserving the Agent exception."""

    async def exercise() -> None:
        previous = _ref("agent", "old")
        session = Session.new()
        session.set_conversation(previous)
        message = _message("input")
        error = LookupError("agent failed")
        fake = FakeAgent(MessageSource("agent"), error=error)
        observer = FakeObserver()

        with pytest.raises(LookupError) as raised:
            await Runtime(observer=observer).send(
                session=session,
                agent=fake,
                message=message,
            )

        assert raised.value is error
        assert session.history.messages == (message,)
        assert session.conversation_for(fake.source) is previous
        assert observer.finished[0].state is AttemptState.FAILED
        async with session.turn():
            pass

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


def test_runtime_observes_returned_source_mismatch_as_failed() -> None:
    """Runtime validation failures are Attempt failures, not Agent successes."""

    async def exercise() -> None:
        source = MessageSource("agent")
        previous = _ref("agent", "old")
        session = Session.new()
        session.set_conversation(previous)
        message = _message("input")
        invalid = _message("invalid", role=MessageRole.ASSISTANT, source="other")
        fake = FakeAgent(source, (AgentTurn(invalid, _ref("other", "thread")),))
        observer = FakeObserver()

        with pytest.raises(
            ValueError,
            match=r"^Agent turn message source does not match agent source\.$",
        ):
            await Runtime(observer=observer).send(
                session=session,
                agent=fake,
                message=message,
            )

        assert session.history.messages == (message,)
        assert session.conversation_for(source) is previous
        assert observer.finished[0].state is AttemptState.FAILED

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


def test_runtime_observes_cancellation_during_agent_without_replacing_it() -> None:
    """Agent cancellation retains input and terminalizes the live Attempt."""

    async def exercise() -> None:
        session = Session.new()
        previous = _ref("agent", "old")
        session.set_conversation(previous)
        message = _message("input")
        entered = asyncio.Event()
        release = asyncio.Event()
        fake = FakeAgent(
            MessageSource("agent"),
            (
                AgentTurn(
                    _message("response", role=MessageRole.ASSISTANT, source="agent"),
                ),
            ),
            entered=entered,
            release=release,
        )
        observer = FakeObserver()
        task = asyncio.create_task(
            Runtime(observer=observer).send(
                session=session,
                agent=fake,
                message=message,
            ),
        )
        await entered.wait()

        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

        assert session.history.messages == (message,)
        assert session.conversation_for(fake.source) is previous
        assert observer.finished[0].state is AttemptState.CANCELLED
        async with session.turn():
            pass

    asyncio.run(exercise())


def test_runtime_preserves_primary_cancellation_when_terminalization_cancels(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Secondary terminalization cancellation cannot replace Agent cancellation."""

    async def exercise() -> None:
        session = Session.new()
        entered = asyncio.Event()
        release = asyncio.Event()
        secondary = asyncio.CancelledError()

        def cancel_attempt(_: Attempt) -> None:
            raise secondary

        monkeypatch.setattr(Attempt, "cancel", cancel_attempt)
        observer = FakeObserver()
        fake = FakeAgent(
            MessageSource("agent"),
            (
                AgentTurn(
                    _message("response", role=MessageRole.ASSISTANT, source="agent"),
                ),
            ),
            entered=entered,
            release=release,
        )
        task = asyncio.create_task(
            Runtime(observer=observer).send(
                session=session,
                agent=fake,
                message=_message("input"),
            ),
        )
        await entered.wait()
        task.cancel()

        with pytest.raises(asyncio.CancelledError) as raised:
            await task

        assert raised.value is not secondary
        assert observer.started[0].state is AttemptState.RUNNING
        assert observer.finished == []
        async with session.turn():
            pass

    asyncio.run(exercise())


@pytest.mark.parametrize(
    "finished_error",
    [LookupError("finished failed"), asyncio.CancelledError()],
)
def test_runtime_suppresses_ordinary_or_cancellation_finished_failure_after_success(
    finished_error: BaseException,
) -> None:
    """Secondary finished failures cannot falsify committed Runtime success."""

    async def exercise() -> None:
        session = Session.new()
        message = _message("input")
        response = _message("response", role=MessageRole.ASSISTANT, source="agent")
        returned = AgentTurn(response, _ref("agent", "thread"))
        fake = FakeAgent(MessageSource("agent"), (returned,))
        observer = FakeObserver(finished_error=finished_error)

        turn = await Runtime(observer=observer).send(
            session=session,
            agent=fake,
            message=message,
        )

        assert turn is returned
        assert session.history.messages == (message, response)
        assert session.conversation_for(fake.source) is returned.conversation
        assert observer.finished[0].state is AttemptState.SUCCEEDED

    asyncio.run(exercise())


def test_runtime_propagates_finished_process_control_after_committed_success() -> None:
    """Non-cancellation BaseException remains visible after primary success."""

    async def exercise() -> None:
        session = Session.new()
        message = _message("input")
        response = _message("response", role=MessageRole.ASSISTANT, source="agent")
        returned = AgentTurn(response)
        error = ProcessControl()
        observer = FakeObserver(finished_error=error)

        with pytest.raises(ProcessControl) as raised:
            await Runtime(observer=observer).send(
                session=session,
                agent=FakeAgent(MessageSource("agent"), (returned,)),
                message=message,
            )

        assert raised.value is error
        assert session.history.messages == (message, response)
        assert observer.finished[0].state is AttemptState.SUCCEEDED

    asyncio.run(exercise())


@pytest.mark.parametrize(
    "finished_error",
    [LookupError("finished failed"), asyncio.CancelledError()],
)
def test_runtime_preserves_agent_failure_over_finished_secondary_error(
    finished_error: BaseException,
) -> None:
    """Ordinary or cancellation observer failure cannot mask Agent failure."""

    async def exercise() -> None:
        session = Session.new()
        message = _message("input")
        primary = LookupError("agent failed")
        observer = FakeObserver(finished_error=finished_error)

        with pytest.raises(LookupError) as raised:
            await Runtime(observer=observer).send(
                session=session,
                agent=FakeAgent(MessageSource("agent"), error=primary),
                message=message,
            )

        assert raised.value is primary
        assert observer.finished[0].state is AttemptState.FAILED

    asyncio.run(exercise())


def test_runtime_preserves_cancellation_over_finished_secondary_error() -> None:
    """Ordinary finished failure cannot mask primary Agent cancellation."""

    async def exercise() -> None:
        session = Session.new()
        entered = asyncio.Event()
        release = asyncio.Event()
        observer = FakeObserver(finished_error=LookupError("finished failed"))
        fake = FakeAgent(
            MessageSource("agent"),
            (
                AgentTurn(
                    _message("response", role=MessageRole.ASSISTANT, source="agent"),
                ),
            ),
            entered=entered,
            release=release,
        )
        task = asyncio.create_task(
            Runtime(observer=observer).send(
                session=session,
                agent=fake,
                message=_message("input"),
            ),
        )
        await entered.wait()
        task.cancel()

        with pytest.raises(asyncio.CancelledError):
            await task

        assert observer.finished[0].state is AttemptState.CANCELLED

    asyncio.run(exercise())


def test_runtime_preserves_start_failure_over_finished_secondary_error() -> None:
    """The start-observer failure remains primary after finished callback failure."""

    async def exercise() -> None:
        session = Session.new()
        primary = LookupError("start failed")
        observer = FakeObserver(
            started_error=primary,
            finished_error=LookupError("finished failed"),
        )

        with pytest.raises(LookupError) as raised:
            await Runtime(observer=observer).send(
                session=session,
                agent=FakeAgent(MessageSource("agent")),
                message=_message("input"),
            )

        assert raised.value is primary
        assert observer.finished[0].state is AttemptState.FAILED

    asyncio.run(exercise())


def test_runtime_preserves_primary_agent_failure_when_terminalization_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Terminal timestamp failure leaves Attempt running without masking Agent error."""

    async def exercise() -> None:
        session = Session.new()
        message = _message("input")
        primary = LookupError("agent failed")
        accounting_error = RuntimeError("timestamp unavailable")

        def fail_timestamp(_: Attempt) -> None:
            def raise_timestamp_error() -> Timestamp:
                raise accounting_error

            monkeypatch.setattr(
                "devtools.evidence.attempt.Timestamp.now",
                raise_timestamp_error,
            )

        observer = FakeObserver(on_started=fail_timestamp)
        with pytest.raises(LookupError) as raised:
            await Runtime(observer=observer).send(
                session=session,
                agent=FakeAgent(MessageSource("agent"), error=primary),
                message=message,
            )

        assert raised.value is primary
        assert observer.started[0].state is AttemptState.RUNNING
        assert observer.started[0].completed_at is None
        assert observer.finished == []
        async with session.turn():
            pass

    asyncio.run(exercise())


def test_runtime_preserves_primary_success_when_terminalization_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Terminal accounting failure cannot convert committed success into failure."""

    async def exercise() -> None:
        session = Session.new()
        message = _message("input")
        response = _message("response", role=MessageRole.ASSISTANT, source="agent")
        returned = AgentTurn(response, _ref("agent", "thread"))

        def fail_timestamp(_: Attempt) -> None:
            message = "timestamp unavailable"

            def raise_timestamp_error() -> Timestamp:
                raise RuntimeError(message)

            monkeypatch.setattr(
                "devtools.evidence.attempt.Timestamp.now",
                raise_timestamp_error,
            )

        observer = FakeObserver(on_started=fail_timestamp)
        turn = await Runtime(observer=observer).send(
            session=session,
            agent=FakeAgent(MessageSource("agent"), (returned,)),
            message=message,
        )

        assert turn is returned
        assert session.history.messages == (message, response)
        assert session.conversation_for(MessageSource("agent")) is returned.conversation
        assert observer.started[0].state is AttemptState.RUNNING
        assert observer.started[0].completed_at is None
        assert observer.finished == []

    asyncio.run(exercise())


def test_runtime_observes_later_conversation_commit_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A local failure after output retention is forward-only and terminally failed."""

    async def exercise() -> None:
        session = Session.new()
        message = _message("input")
        response = _message("response", role=MessageRole.ASSISTANT, source="agent")
        error = LookupError("conversation commit failed")

        def fail_set_conversation(
            _: Session,
            __: ConversationRef,
        ) -> None:
            raise error

        monkeypatch.setattr(Session, "set_conversation", fail_set_conversation)
        observer = FakeObserver()

        with pytest.raises(LookupError) as raised:
            await Runtime(observer=observer).send(
                session=session,
                agent=FakeAgent(
                    MessageSource("agent"),
                    (AgentTurn(response, _ref("agent", "thread")),),
                ),
                message=message,
            )

        assert raised.value is error
        assert session.history.messages == (message, response)
        assert session.conversation_for(MessageSource("agent")) is None
        assert observer.finished[0].state is AttemptState.FAILED

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


def test_runtime_hands_a_replacement_continuation_to_a_queued_same_source_turn() -> (
    None
):
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


def test_runtime_observer_callbacks_remain_ordered_with_one_session() -> None:
    """Callbacks finish one Session turn before the next turn starts."""

    async def exercise() -> None:
        session = Session.new()
        entered_a = asyncio.Event()
        release_a = asyncio.Event()
        entered_b = asyncio.Event()
        observer = FakeObserver()
        runtime = Runtime(observer=observer)
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
        task_b = asyncio.create_task(
            runtime.send(session=session, agent=agent_b, message=input_b),
        )
        assert agent_b.calls == []
        assert [name for name, _ in observer.events] == ["started"]

        release_a.set()
        await entered_b.wait()
        await asyncio.gather(task_a, task_b)

        assert [name for name, _ in observer.events] == [
            "started",
            "finished",
            "started",
            "finished",
        ]
        assert session.history.messages == (
            input_a,
            response_a,
            input_b,
            response_b,
        )

    asyncio.run(exercise())


def test_runtime_observer_preserves_same_source_continuation_handoff() -> None:
    """Observation does not weaken queued same-source continuation replacement."""

    async def exercise() -> None:
        source = MessageSource("agent")
        initial = _ref("agent", "thread-a")
        replacement = _ref("agent", "thread-b")
        session = Session.new()
        session.set_conversation(initial)
        entered_a = asyncio.Event()
        release_a = asyncio.Event()
        entered_b = asyncio.Event()
        observer = FakeObserver()
        runtime = Runtime(observer=observer)
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
        agent_b = FakeAgent(source, (AgentTurn(response_b),), entered=entered_b)

        task_a = asyncio.create_task(
            runtime.send(session=session, agent=agent_a, message=input_a),
        )
        await entered_a.wait()
        task_b = asyncio.create_task(
            runtime.send(session=session, agent=agent_b, message=input_b),
        )
        assert agent_b.calls == []

        release_a.set()
        await entered_b.wait()
        await asyncio.gather(task_a, task_b)

        assert agent_a.calls == [(input_a, initial)]
        assert agent_b.calls == [(input_b, replacement)]
        assert agent_b.calls[0][1] is replacement
        assert [name for name, _ in observer.events] == [
            "started",
            "finished",
            "started",
            "finished",
        ]

    asyncio.run(exercise())


def test_runtime_observer_does_not_serialize_different_sessions() -> None:
    """A shared observer adds no global Runtime serialization."""

    async def exercise() -> None:
        observer = FakeObserver()
        runtime = Runtime(observer=observer)
        release = asyncio.Event()
        entered_a = asyncio.Event()
        entered_b = asyncio.Event()
        agent_a = FakeAgent(
            MessageSource("a"),
            (
                AgentTurn(
                    _message("response-a", role=MessageRole.ASSISTANT, source="a"),
                ),
            ),
            entered=entered_a,
            release=release,
        )
        agent_b = FakeAgent(
            MessageSource("b"),
            (
                AgentTurn(
                    _message("response-b", role=MessageRole.ASSISTANT, source="b"),
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

        expected_attempt_count = len((agent_a, agent_b))
        assert len(observer.started) == expected_attempt_count
        release.set()
        await asyncio.gather(task_a, task_b)
        assert len(observer.finished) == expected_attempt_count

    asyncio.run(exercise())
