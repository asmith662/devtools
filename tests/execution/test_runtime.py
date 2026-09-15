# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, RSE102, TRY003
"""Tests for narrow Runtime coordination and interaction-attempt lifecycle."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field

import pytest

from devtools.agents.conversation import (
    Conversation,
    ConversationMessage,
    ConversationMessageRole,
)
from devtools.execution import (
    InteractionAttempt,
    InteractionAttemptCancelled,
    InteractionAttemptFailed,
    InteractionAttemptOutcome,
    InteractionAttemptStage,
    InteractionAttemptSucceeded,
    Runtime,
)
from devtools.models.interaction import (
    ConversationRef,
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelSettings,
    Prompt,
)
from devtools.observability.evidence import ExecutionInspector

_CALLER = InteractionSource("caller")
_MODEL = InteractionSource("model")


def _message(content: str = "question") -> ConversationMessage:
    """Create one caller-owned conversation message."""
    return ConversationMessage.new(
        content,
        role=ConversationMessageRole.USER,
        source=_CALLER,
    )


@dataclass
class FakeInteraction:
    """Script one model interaction while recording prompt materialization."""

    source: InteractionSource = _MODEL
    responses: list[ModelResponse] = field(default_factory=list)
    error: BaseException | None = None
    prompts: list[tuple[Prompt, ConversationRef | None]] = field(default_factory=list)
    requested_output_tokens: list[int | None] = field(default_factory=list)
    requested_thinking: list[bool | None] = field(default_factory=list)

    async def send(
        self,
        request: ModelRequest,
    ) -> ModelResponse:
        """Record the materialized input and return one scripted result."""
        self.requested_output_tokens.append(request.settings.maximum_output_tokens)
        self.requested_thinking.append(request.settings.thinking_enabled)
        self.prompts.append((request.prompt, request.conversation))
        if self.error is not None:
            raise self.error
        return self.responses.pop(0)


@dataclass
class Observer:
    """Retain exact lifecycle callbacks from execution."""

    started: list[InteractionAttempt] = field(default_factory=list)
    finished: list[tuple[InteractionAttempt, InteractionAttemptOutcome]] = field(
        default_factory=list,
    )

    def attempt_started(self, attempt: InteractionAttempt) -> None:
        """Record admission of a new live attempt."""
        self.started.append(attempt)

    def attempt_finished(
        self,
        attempt: InteractionAttempt,
        outcome: InteractionAttemptOutcome,
    ) -> None:
        """Record a terminal attempt fact."""
        self.finished.append((attempt, outcome))


def test_runtime_projects_conversation_message_and_materializes_response() -> None:
    """Runtime turns durable messages into Prompt and response into a fresh message."""

    async def exercise() -> None:
        conversation = Conversation.new()
        response = ModelResponse(content="answer", source=_MODEL)
        interaction = FakeInteraction(responses=[response])

        returned = await Runtime().send(
            conversation=conversation,
            interaction=interaction,
            message=_message(),
        )

        assert returned is response
        fake = interaction
        assert fake.prompts == [(Prompt(content="question", role="user"), None)]
        assert [item.content for item in conversation.history] == ["question", "answer"]
        assert conversation.history[-1].role is ConversationMessageRole.ASSISTANT
        assert conversation.history[-1].source == _MODEL
        assert conversation.history[-1].id != conversation.history[0].id

    asyncio.run(exercise())


def test_runtime_forwards_an_explicit_output_bound_without_treating_it_as_budget() -> None:
    """Runtime mechanically forwards the caller's one-interaction constraint."""

    async def exercise() -> None:
        conversation = Conversation.new()
        interaction = FakeInteraction(
            responses=[ModelResponse(content="answer", source=_MODEL)],
        )

        await Runtime().send(
            conversation=conversation,
            interaction=interaction,
            message=_message(),
            settings=ModelSettings(maximum_output_tokens=64),
        )

        assert interaction.requested_output_tokens == [64]

    asyncio.run(exercise())


def test_runtime_rejects_an_invalid_output_bound_before_interaction() -> None:
    """Runtime does not delegate malformed shared request semantics to providers."""

    async def exercise() -> None:
        interaction = FakeInteraction(
            responses=[ModelResponse(content="answer", source=_MODEL)],
        )
        with pytest.raises(ValueError, match="positive integer"):
            ModelSettings(maximum_output_tokens=0)
        assert interaction.requested_output_tokens == []

    asyncio.run(exercise())


@pytest.mark.parametrize("thinking_enabled", [True, False])
def test_runtime_forwards_explicit_thinking_control(
    *,
    thinking_enabled: bool,
) -> None:
    """Runtime forwards explicit thinking mode without selecting a policy."""

    async def exercise() -> None:
        interaction = FakeInteraction(
            responses=[ModelResponse(content="answer", source=_MODEL)],
        )
        await Runtime().send(
            conversation=Conversation.new(),
            interaction=interaction,
            message=_message(),
            settings=ModelSettings(thinking_enabled=thinking_enabled),
        )
        assert interaction.requested_thinking == [thinking_enabled]
        assert interaction.requested_output_tokens == [None]

    asyncio.run(exercise())


def test_runtime_rejects_malformed_thinking_control_before_interaction() -> None:
    """Runtime rejects malformed thinking values before invoking a provider."""
    interaction = FakeInteraction(
        responses=[ModelResponse(content="answer", source=_MODEL)],
    )
    with pytest.raises(TypeError, match="boolean"):
        ModelSettings(thinking_enabled=1)  # type: ignore[arg-type]
    assert interaction.requested_thinking == []


def test_runtime_hands_forward_and_replaces_provider_continuation() -> None:
    """Continuation remains model-owned and is only retained by Conversation."""

    async def exercise() -> None:
        previous = ConversationRef(_MODEL, "old")
        replacement = ConversationRef(_MODEL, "new")
        conversation = Conversation.new()
        conversation.set_conversation(previous)
        interaction = FakeInteraction(
            responses=[
                ModelResponse(content="first", source=_MODEL, conversation=replacement),
                ModelResponse(content="second", source=_MODEL),
            ],
        )
        runtime = Runtime()

        await runtime.send(
            conversation=conversation, interaction=interaction, message=_message()
        )
        await runtime.send(
            conversation=conversation,
            interaction=interaction,
            message=_message("again"),
        )

        assert interaction.prompts[0][1] is previous
        assert interaction.prompts[1][1] is replacement
        assert conversation.conversation_for(_MODEL) is replacement

    asyncio.run(exercise())


def test_runtime_rejects_mismatched_model_source_before_retaining_output() -> None:
    """A response from another model source fails at validation, not retention."""

    async def exercise() -> None:
        observer = Observer()
        conversation = Conversation.new()
        with pytest.raises(ValueError, match="source"):
            await Runtime(observer=observer).send(
                conversation=conversation,
                interaction=FakeInteraction(
                    responses=[
                        ModelResponse(content="bad", source=InteractionSource("other"))
                    ],
                ),
                message=_message(),
            )
        assert [message.content for message in conversation.history] == ["question"]
        assert isinstance(observer.finished[0][1], InteractionAttemptFailed)
        assert (
            observer.finished[0][1].stage is InteractionAttemptStage.RESULT_VALIDATION
        )

    asyncio.run(exercise())


def test_runtime_observer_exposes_execution_lifecycle_without_evidence_dependency() -> (
    None
):
    """Execution calls an observer; observability can independently construct Evidence."""

    async def exercise() -> None:
        inspector = ExecutionInspector()
        conversation = Conversation.new()
        await Runtime(observer=inspector).send(
            conversation=conversation,
            interaction=FakeInteraction(
                responses=[ModelResponse(content="ok", source=_MODEL)]
            ),
            message=_message(),
        )
        attempt_id = inspector.attempt_ids()[0]
        attempt = inspector.get_attempt(attempt_id)
        evidence = inspector.get_evidence_for_attempt(attempt_id)
        assert attempt is not None
        assert len(evidence) == 1
        assert isinstance(evidence[0].outcome, InteractionAttemptSucceeded)

    asyncio.run(exercise())


def test_runtime_records_provider_failure_and_preserves_primary_error() -> None:
    """Provider failures retain input and terminalize the specialized attempt."""

    async def exercise() -> None:
        observer = Observer()
        conversation = Conversation.new()
        error = LookupError("provider failed")
        with pytest.raises(LookupError) as raised:
            await Runtime(observer=observer).send(
                conversation=conversation,
                interaction=FakeInteraction(error=error),
                message=_message(),
            )
        assert raised.value is error
        assert [message.content for message in conversation.history] == ["question"]
        outcome = observer.finished[0][1]
        assert isinstance(outcome, InteractionAttemptFailed)
        assert outcome.stage is InteractionAttemptStage.INTERACTION_INVOCATION

    asyncio.run(exercise())


def test_runtime_records_cancellation_without_retaining_response() -> None:
    """Cancellation is terminal lifecycle information and is never rollback."""

    async def exercise() -> None:
        observer = Observer()
        conversation = Conversation.new()
        with pytest.raises(asyncio.CancelledError):
            await Runtime(observer=observer).send(
                conversation=conversation,
                interaction=FakeInteraction(error=asyncio.CancelledError()),
                message=_message(),
            )
        outcome = observer.finished[0][1]
        assert isinstance(outcome, InteractionAttemptCancelled)
        assert outcome.stage is InteractionAttemptStage.INTERACTION_INVOCATION
        assert [message.content for message in conversation.history] == ["question"]

    asyncio.run(exercise())


def test_runtime_without_observer_does_not_create_attempt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The narrow Runtime has no hidden observability work in bare mode."""

    def fail_new(**_: object) -> InteractionAttempt:
        raise AssertionError("attempt should not be created")

    monkeypatch.setattr(InteractionAttempt, "new", fail_new)

    async def exercise() -> None:
        await Runtime().send(
            conversation=Conversation.new(),
            interaction=FakeInteraction(
                responses=[ModelResponse(content="ok", source=_MODEL)]
            ),
            message=_message(),
        )

    asyncio.run(exercise())


def test_runtime_exposes_fixed_observer_configuration() -> None:
    """Observer configuration is narrow execution lifecycle plumbing."""
    observer = Observer()
    assert Runtime().observer is None
    assert Runtime(observer=observer).observer is observer


def test_runtime_preserves_observer_admission_failure_and_terminalizes_attempt() -> (
    None
):
    """Observer admission failure is an execution admission failure, not Evidence work."""

    class FailingObserver(Observer):
        def attempt_started(self, attempt: InteractionAttempt) -> None:
            super().attempt_started(attempt)
            raise LookupError("admission failed")

    async def exercise() -> None:
        observer = FailingObserver()
        with pytest.raises(LookupError, match="admission failed"):
            await Runtime(observer=observer).send(
                conversation=Conversation.new(),
                interaction=FakeInteraction(
                    responses=[ModelResponse(content="ok", source=_MODEL)]
                ),
                message=_message(),
            )
        assert len(observer.started) == 1
        assert len(observer.finished) == 1
        assert isinstance(observer.finished[0][1], InteractionAttemptFailed)
        assert observer.finished[0][1].stage is InteractionAttemptStage.ADMISSION

    asyncio.run(exercise())


def test_runtime_suppresses_secondary_terminalization_failures() -> None:
    """Observer completion errors do not replace completed model work."""

    class FailingObserver(Observer):
        def attempt_finished(
            self,
            attempt: InteractionAttempt,
            outcome: InteractionAttemptOutcome,
        ) -> None:
            super().attempt_finished(attempt, outcome)
            raise LookupError("secondary")

    async def exercise() -> None:
        observer = FailingObserver()
        response = await Runtime(observer=observer).send(
            conversation=Conversation.new(),
            interaction=FakeInteraction(
                responses=[ModelResponse(content="ok", source=_MODEL)]
            ),
            message=_message(),
        )
        assert response.content == "ok"
        assert len(observer.finished) == 1

    asyncio.run(exercise())


def test_runtime_preserves_admission_cancellation_when_observer_cancels() -> None:
    """Cancellation from execution observation terminalizes admission then propagates."""

    class CancellingObserver(Observer):
        def attempt_started(self, attempt: InteractionAttempt) -> None:
            super().attempt_started(attempt)
            raise asyncio.CancelledError()

    async def exercise() -> None:
        observer = CancellingObserver()
        with pytest.raises(asyncio.CancelledError):
            await Runtime(observer=observer).send(
                conversation=Conversation.new(),
                interaction=FakeInteraction(
                    responses=[ModelResponse(content="ok", source=_MODEL)]
                ),
                message=_message(),
            )
        assert isinstance(observer.finished[0][1], InteractionAttemptCancelled)
        assert observer.finished[0][1].stage is InteractionAttemptStage.ADMISSION

    asyncio.run(exercise())


def test_runtime_suppresses_terminalization_and_observer_cancellation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Secondary terminalization control flow cannot replace a committed response."""

    def cancel_terminalization(_attempt: InteractionAttempt) -> None:
        raise asyncio.CancelledError()

    class CancellingFinishObserver(Observer):
        def attempt_finished(
            self,
            attempt: InteractionAttempt,
            outcome: InteractionAttemptOutcome,
        ) -> None:
            super().attempt_finished(attempt, outcome)
            raise asyncio.CancelledError()

    monkeypatch.setattr(InteractionAttempt, "succeed", cancel_terminalization)

    async def exercise() -> None:
        observer = CancellingFinishObserver()
        response = await Runtime(observer=observer).send(
            conversation=Conversation.new(),
            interaction=FakeInteraction(
                responses=[ModelResponse(content="ok", source=_MODEL)]
            ),
            message=_message(),
        )
        assert response.content == "ok"
        assert observer.finished == []

    asyncio.run(exercise())

    attempt = InteractionAttempt.new(
        conversation_id=Conversation.new().id,
        message_id=_message().id,
        interaction_source=_MODEL,
    )
    Runtime._finish_attempt(  # noqa: SLF001 - direct coverage of narrow secondary guard
        CancellingFinishObserver(),
        attempt,
        lambda: None,
        InteractionAttemptSucceeded(),
    )

    def fail_terminalization() -> None:
        raise LookupError("secondary")

    Runtime._finish_attempt(  # noqa: SLF001 - direct coverage of narrow secondary guard
        Observer(),
        attempt,
        fail_terminalization,
        InteractionAttemptSucceeded(),
    )


def test_runtime_serializes_turns_for_one_conversation() -> None:
    """The conversation turn lock prevents interleaved durable transcript commits."""
    entered = asyncio.Event()
    release = asyncio.Event()

    @dataclass
    class BlockingInteraction(FakeInteraction):
        async def send(
            self,
            request: ModelRequest,
        ) -> ModelResponse:
            self.prompts.append((request.prompt, request.conversation))
            if len(self.prompts) == 1:
                entered.set()
                await release.wait()
            return self.responses.pop(0)

    async def exercise() -> None:
        conversation = Conversation.new()
        interaction = BlockingInteraction(
            responses=[
                ModelResponse(content="one", source=_MODEL),
                ModelResponse(content="two", source=_MODEL),
            ],
        )
        runtime = Runtime()
        first = asyncio.create_task(
            runtime.send(
                conversation=conversation,
                interaction=interaction,
                message=_message("a"),
            ),
        )
        await entered.wait()
        second = asyncio.create_task(
            runtime.send(
                conversation=conversation,
                interaction=interaction,
                message=_message("b"),
            ),
        )
        await asyncio.sleep(0)
        assert [message.content for message in conversation.history] == ["a"]
        release.set()
        await asyncio.gather(first, second)
        assert [message.content for message in conversation.history] == [
            "a",
            "one",
            "b",
            "two",
        ]

    asyncio.run(exercise())
