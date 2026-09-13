# Copyright (c) 2026
"""Tests for the experimental CommandTool bridge."""

from __future__ import annotations

import asyncio
import sys

import pytest

from devtools.core.time import Duration
from devtools.resources.commands import (
    Command,
    CommandExecutor,
    CommandNotFoundError,
    CommandResult,
    CommandTimeoutError,
)
from devtools.tools import Tool, ToolRunner
from devtools.tools.command import CommandTool

_NONZERO_EXIT_CODE = 7


def test_command_tool_is_typed_tool_and_returns_command_result() -> None:
    """CommandTool preserves the existing Command-to-CommandResult contract."""

    async def exercise() -> None:
        tool: Tool[Command, CommandResult] = CommandTool(CommandExecutor())
        command = Command(sys.executable, ("-c", "print('tool command')"))

        result: CommandResult = await ToolRunner().execute(tool, command)

        assert tool.name == "run_command"
        assert tool.description
        assert result.command is command
        assert result.stdout.strip() == b"tool command"

    asyncio.run(exercise())


def test_command_tool_preserves_nonzero_exit_as_result() -> None:
    """A nonzero process exit remains a CommandResult rather than Tool failure."""

    async def exercise() -> None:
        command = Command(
            sys.executable,
            ("-c", f"import sys; sys.exit({_NONZERO_EXIT_CODE})"),
        )
        result = await ToolRunner().execute(CommandTool(CommandExecutor()), command)

        assert isinstance(result, CommandResult)
        assert result.exit_code == _NONZERO_EXIT_CODE
        assert result.failed is True

    asyncio.run(exercise())


def test_command_tool_propagates_missing_command_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Command lookup failures remain owned by Commands."""

    async def raise_not_found(*_args: object, **_kwargs: object) -> None:
        raise FileNotFoundError

    monkeypatch.setattr(
        "devtools.resources.commands.execution.asyncio.create_subprocess_exec",
        raise_not_found,
    )

    with pytest.raises(CommandNotFoundError):
        asyncio.run(
            ToolRunner().execute(CommandTool(CommandExecutor()), Command("missing")),
        )


def test_command_tool_propagates_command_timeout() -> None:
    """Command timeout policy passes through the Tool bridge unchanged."""
    command = Command(
        sys.executable,
        ("-c", "import time; time.sleep(1)"),
        timeout=Duration.seconds(0.001),
    )

    with pytest.raises(CommandTimeoutError):
        asyncio.run(ToolRunner().execute(CommandTool(CommandExecutor()), command))


def test_command_tool_cancellation_preserves_command_cleanup(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cancellation through CommandTool retains immediate-child cleanup."""
    process = _BlockingProcess()

    async def create_process(*_args: object, **_kwargs: object) -> _BlockingProcess:
        return process

    monkeypatch.setattr(
        "devtools.resources.commands.execution.asyncio.create_subprocess_exec",
        create_process,
    )

    async def exercise() -> None:
        operation = asyncio.create_task(
            ToolRunner().execute(
                CommandTool(CommandExecutor()),
                Command("blocking-command"),
            ),
        )
        await process.read_started.wait()
        operation.cancel()

        with pytest.raises(asyncio.CancelledError):
            await operation

    asyncio.run(exercise())

    assert process.killed is True
    assert process.waited is True


class _BlockingProcess:
    """Minimal process fake that blocks stream collection until cancellation."""

    def __init__(self) -> None:
        """Initialize open streams and cleanup observations."""
        self.killed = False
        self.read_started = asyncio.Event()
        self.returncode: int | None = None
        self.stderr = _BlockingStream(self.read_started)
        self.stdout = _BlockingStream(self.read_started)
        self.waited = False

    def kill(self) -> None:
        """Record immediate-child termination."""
        self.killed = True

    async def wait(self) -> None:
        """Record immediate-child reaping."""
        self.waited = True


class _BlockingStream:
    """Stream fake that waits until cancellation reaches its read task."""

    def __init__(self, read_started: asyncio.Event) -> None:
        """Store the shared start observation."""
        self._read_started = read_started
        self._release = asyncio.Event()

    async def read(self, _size: int) -> bytes:
        """Block until cancellation interrupts this stream read."""
        self._read_started.set()
        await self._release.wait()
        return b""
