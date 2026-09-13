# Copyright (c) 2026
# ruff: noqa: E501
"""Runtime integration tests for the command-backed Tool adapter."""

from __future__ import annotations

import asyncio
import sys

import pytest

from devtools.agents.conversation import (
    Conversation,
    ConversationMessage,
    ConversationMessageRole,
)
from devtools.execution import (
    InteractionAttemptCancelled,
    InteractionAttemptFailed,
    InteractionAttemptStage,
    Runtime,
)
from devtools.models.interaction import (
    ConversationRef,
    InteractionSource,
    ModelResponse,
    Prompt,
)
from devtools.observability.evidence import ExecutionInspector
from devtools.resources.commands import Command, CommandExecutor, CommandNotFoundError
from devtools.tools import ToolRunner
from devtools.tools.command import CommandTool


class _CommandToolInteraction:
    """Adapt one real CommandTool execution into model-boundary output for tests."""

    def __init__(
        self,
        command: Command,
        *,
        return_source: InteractionSource | None = None,
    ) -> None:
        """Configure one nested Tool invocation."""
        self._command = command
        self._return_source = return_source or self.source
        self._runner = ToolRunner()
        self._tool = CommandTool(CommandExecutor())

    @property
    def source(self) -> InteractionSource:
        """Return the source represented by this test ModelInteraction."""
        return InteractionSource("command-tool-interaction")

    async def send(
        self,
        prompt: Prompt,
        *,
        conversation: ConversationRef | None = None,
    ) -> ModelResponse:
        """Execute the Tool and return model output without conversation identity."""
        del prompt, conversation
        result = await self._runner.execute(self._tool, self._command)
        return ModelResponse(
            content=result.stdout.decode().strip(),
            source=self._return_source,
        )


def _message(content: str) -> ConversationMessage:
    """Create one caller-owned Runtime input ConversationMessage."""
    return ConversationMessage.new(
        content,
        role=ConversationMessageRole.USER,
        source=InteractionSource("caller"),
    )


def test_runtime_interaction_executes_real_command_tool_successfully() -> None:
    """A Tool result crosses the ModelResponse then conversation materialization boundary."""

    async def exercise() -> None:
        conversation = Conversation.new()
        response = await Runtime().send(
            conversation=conversation,
            interaction=_CommandToolInteraction(
                Command(sys.executable, ("-c", "print('nested tool')")),
            ),
            message=_message("run command"),
        )
        assert response.content == "nested tool"
        assert [message.content for message in conversation.history] == [
            "run command",
            "nested tool",
        ]

    asyncio.run(exercise())


def test_tool_failure_is_observed_as_interaction_invocation_failure() -> None:
    """Runtime owns lifecycle facts while observability constructs terminal Evidence."""

    async def exercise() -> None:
        inspector = ExecutionInspector()
        with pytest.raises(CommandNotFoundError):
            await Runtime(observer=inspector).send(
                conversation=Conversation.new(),
                interaction=_CommandToolInteraction(Command("missing-command")),
                message=_message("run command"),
            )
        attempt_id = inspector.attempt_ids()[0]
        evidence = inspector.get_evidence_for_attempt(attempt_id)[0]
        assert isinstance(evidence.outcome, InteractionAttemptFailed)
        assert evidence.outcome.stage is InteractionAttemptStage.INTERACTION_INVOCATION

    asyncio.run(exercise())


def test_tool_result_with_wrong_model_source_fails_response_validation() -> None:
    """Tool success does not bypass Runtime's model-response source validation."""

    async def exercise() -> None:
        inspector = ExecutionInspector()
        with pytest.raises(ValueError, match="source"):
            await Runtime(observer=inspector).send(
                conversation=Conversation.new(),
                interaction=_CommandToolInteraction(
                    Command(sys.executable, ("-c", "print('nested tool')")),
                    return_source=InteractionSource("wrong-source"),
                ),
                message=_message("run command"),
            )
        evidence = inspector.get_evidence_for_attempt(inspector.attempt_ids()[0])[0]
        assert isinstance(evidence.outcome, InteractionAttemptFailed)
        assert evidence.outcome.stage is InteractionAttemptStage.RESULT_VALIDATION

    asyncio.run(exercise())


def test_cancelled_command_tool_is_observed_as_invocation_cancellation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Nested Tool cancellation preserves the outer specialized attempt stage."""
    process = _BlockingProcess()

    async def create_process(*_args: object, **_kwargs: object) -> _BlockingProcess:
        return process

    monkeypatch.setattr(
        "devtools.resources.commands.execution.asyncio.create_subprocess_exec",
        create_process,
    )

    async def exercise() -> None:
        inspector = ExecutionInspector()
        task = asyncio.create_task(
            Runtime(observer=inspector).send(
                conversation=Conversation.new(),
                interaction=_CommandToolInteraction(Command("blocking-command")),
                message=_message("run command"),
            ),
        )
        await process.read_started.wait()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        evidence = inspector.get_evidence_for_attempt(inspector.attempt_ids()[0])[0]
        assert isinstance(evidence.outcome, InteractionAttemptCancelled)
        assert evidence.outcome.stage is InteractionAttemptStage.INTERACTION_INVOCATION

    asyncio.run(exercise())
    assert process.killed is True
    assert process.waited is True


class _BlockingProcess:
    """Minimal command process fake for deterministic nested cancellation."""

    def __init__(self) -> None:
        """Initialize stream and cleanup observations."""
        self.killed = False
        self.read_started = asyncio.Event()
        self.returncode: int | None = None
        self.stderr = _BlockingStream(self.read_started)
        self.stdout = _BlockingStream(self.read_started)
        self.waited = False

    def kill(self) -> None:
        """Record termination requested by CommandExecutor."""
        self.killed = True

    async def wait(self) -> None:
        """Record process reaping requested by CommandExecutor."""
        self.waited = True


class _BlockingStream:
    """Stream fake whose read waits for cancellation."""

    def __init__(self, read_started: asyncio.Event) -> None:
        """Store common stream-start observation."""
        self._read_started = read_started
        self._release = asyncio.Event()

    async def read(self, _size: int) -> bytes:
        """Block until cancellation reaches the command stream task."""
        self._read_started.set()
        await self._release.wait()
        return b""
