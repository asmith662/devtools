# Copyright (c) 2026
"""Runtime integration tests for nested experimental CommandTool execution."""

from __future__ import annotations

import asyncio
import sys
from typing import TYPE_CHECKING

import pytest

from devtools.commands import Command, CommandExecutor, CommandNotFoundError
from devtools.context import Message, MessageRole, MessageSource, Session
from devtools.evidence import AttemptCancelled, AttemptFailed, AttemptStage
from devtools.interactions import ConversationRef, InteractionTurn
from devtools.runtime import Runtime
from devtools.tools import ToolRunner
from devtools.tools.command import CommandTool

if TYPE_CHECKING:
    from devtools.evidence import AttemptTerminalEvidence


_EXPECTED_HISTORY_MESSAGES = 2


class _CommandToolInteraction:
    """Map one CommandTool result into an InteractionTurn in a realistic fake."""

    def __init__(
        self,
        command: Command,
        *,
        return_source: MessageSource | None = None,
    ) -> None:
        """Configure one nested CommandTool invocation."""
        self._command = command
        self._return_source = return_source or self.source
        self._runner = ToolRunner()
        self._tool = CommandTool(CommandExecutor())

    @property
    def source(self) -> MessageSource:
        """Return the source represented by this concrete test Interaction."""
        return MessageSource("command-tool-interaction")

    async def send(
        self,
        message: Message,
        *,
        conversation: ConversationRef | None = None,
    ) -> InteractionTurn:
        """Invoke CommandTool and map its output into the frozen contract."""
        del message, conversation
        result = await self._runner.execute(self._tool, self._command)
        return InteractionTurn(
            Message.new(
                result.stdout.decode().strip(),
                role=MessageRole.ASSISTANT,
                source=self._return_source,
            ),
        )


class _Sink:
    """Retain terminal Evidence through the frozen structural sink seam."""

    def __init__(self) -> None:
        """Create an empty Evidence collector."""
        self.accepted: list[AttemptTerminalEvidence] = []

    def accept(self, evidence: AttemptTerminalEvidence) -> None:
        """Retain one terminal Evidence value."""
        self.accepted.append(evidence)


def _message(content: str) -> Message:
    """Create one caller-owned Runtime input Message."""
    return Message.new(content, role=MessageRole.USER, source=MessageSource("caller"))


def test_runtime_interaction_executes_real_command_tool_successfully() -> None:
    """A real command executes through Runtime, Interaction, ToolRunner, and Tool."""

    async def exercise() -> None:
        interaction = _CommandToolInteraction(
            Command(sys.executable, ("-c", "print('nested tool')")),
        )
        session = Session.new()

        turn = await Runtime().send(
            session=session,
            interaction=interaction,
            message=_message("run command"),
        )

        assert turn.message.content == "nested tool"
        assert len(session.history) == _EXPECTED_HISTORY_MESSAGES

    asyncio.run(exercise())


def test_tool_failure_remains_outer_interaction_invocation_failure() -> None:
    """A CommandTool error leaves Runtime stage ownership unchanged."""

    async def exercise() -> None:
        sink = _Sink()
        interaction = _CommandToolInteraction(Command("missing-command"))

        with pytest.raises(CommandNotFoundError):
            await Runtime(evidence_sink=sink).send(
                session=Session.new(),
                interaction=interaction,
                message=_message("run command"),
            )

        outcome = sink.accepted[0].outcome
        assert isinstance(outcome, AttemptFailed)
        assert outcome.stage is AttemptStage.INTERACTION_INVOCATION

    asyncio.run(exercise())


def test_tool_cancellation_remains_outer_interaction_invocation_cancellation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """CommandTool cancellation preserves Runtime's outer stage vocabulary."""
    process = _BlockingProcess()

    async def create_process(*_args: object, **_kwargs: object) -> _BlockingProcess:
        return process

    monkeypatch.setattr(
        "devtools.commands.execution.asyncio.create_subprocess_exec",
        create_process,
    )

    async def exercise() -> None:
        sink = _Sink()
        task = asyncio.create_task(
            Runtime(evidence_sink=sink).send(
                session=Session.new(),
                interaction=_CommandToolInteraction(Command("blocking-command")),
                message=_message("run command"),
            ),
        )
        await process.read_started.wait()
        task.cancel()

        with pytest.raises(asyncio.CancelledError):
            await task

        outcome = sink.accepted[0].outcome
        assert isinstance(outcome, AttemptCancelled)
        assert outcome.stage is AttemptStage.INTERACTION_INVOCATION

    asyncio.run(exercise())

    assert process.killed is True
    assert process.waited is True


def test_tool_success_does_not_change_later_runtime_result_validation_stage() -> None:
    """A later invalid InteractionTurn remains Runtime's RESULT_VALIDATION failure."""

    async def exercise() -> None:
        sink = _Sink()
        interaction = _CommandToolInteraction(
            Command(sys.executable, ("-c", "print('nested tool')")),
            return_source=MessageSource("wrong-source"),
        )

        with pytest.raises(ValueError, match="source"):
            await Runtime(evidence_sink=sink).send(
                session=Session.new(),
                interaction=interaction,
                message=_message("run command"),
            )

        outcome = sink.accepted[0].outcome
        assert isinstance(outcome, AttemptFailed)
        assert outcome.stage is AttemptStage.RESULT_VALIDATION

    asyncio.run(exercise())


class _BlockingProcess:
    """Minimal command process fake for deterministic nested cancellation."""

    def __init__(self) -> None:
        """Initialize streams and immediate-child cleanup observations."""
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
        """Store the common stream-start event."""
        self._read_started = read_started
        self._release = asyncio.Event()

    async def read(self, _size: int) -> bytes:
        """Block until cancellation reaches the command stream task."""
        self._read_started.set()
        await self._release.wait()
        return b""
