# Copyright (c) 2026
"""Tests for public asynchronous command execution."""

from __future__ import annotations

import asyncio
import sys
from typing import TYPE_CHECKING

import pytest

from devtools.commands import (
    Command,
    CommandError,
    CommandExecutor,
    CommandNotFoundError,
    CommandOutputPolicy,
    CommandTimeoutError,
)
from devtools.paths import ResolvedPath
from devtools.time import Duration

if TYPE_CHECKING:
    from pathlib import Path


def test_executor_runs_python_and_preserves_argument_bytes() -> None:
    """The executor captures raw output from a portable Python subprocess."""
    command = Command(
        sys.executable,
        ("-c", "import sys; print('|'.join(sys.argv[1:]))", "first", "second"),
    )

    result = asyncio.run(CommandExecutor().execute(command))

    assert result.succeeded is True
    assert result.stdout.strip() == b"first|second"
    assert result.stderr == b""
    assert isinstance(result.duration, Duration)
    assert result.duration.total_seconds >= 0


def test_executor_returns_nonzero_exit_codes_as_results() -> None:
    """A process failure code is represented without an execution exception."""
    expected_exit_code = 7
    command = Command(
        sys.executable,
        ("-c", f"import sys; sys.exit({expected_exit_code})"),
    )

    result = asyncio.run(CommandExecutor().execute(command))

    assert result.exit_code == expected_exit_code
    assert result.failed is True


def test_executor_passes_the_resolved_working_directory(tmp_path: Path) -> None:
    """The subprocess receives the native representation of its working directory."""
    command = Command(
        sys.executable,
        ("-c", "import os; print(os.getcwd())"),
        working_directory=ResolvedPath(tmp_path),
    )

    result = asyncio.run(CommandExecutor().execute(command))

    assert result.stdout.strip() == str(tmp_path).encode()


def test_executor_wraps_missing_executables(monkeypatch: pytest.MonkeyPatch) -> None:
    """A missing executable produces the public command-domain exception."""

    async def raise_not_found(*_args: object, **_kwargs: object) -> None:
        raise FileNotFoundError

    monkeypatch.setattr(
        "devtools.commands.execution.asyncio.create_subprocess_exec",
        raise_not_found,
    )

    with pytest.raises(CommandNotFoundError, match="not found"):
        asyncio.run(CommandExecutor().execute(Command("missing-command")))


def test_executor_rejects_a_completed_process_without_an_exit_code(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An unexpected absent exit code is not exposed in a command result."""
    process = _NoExitCodeProcess()

    async def create_process(
        *_args: object,
        **_kwargs: object,
    ) -> _NoExitCodeProcess:
        return process

    monkeypatch.setattr(
        "devtools.commands.execution.asyncio.create_subprocess_exec",
        create_process,
    )

    with pytest.raises(CommandError, match="without an exit code"):
        asyncio.run(CommandExecutor().execute(Command("incomplete-command")))


def test_executor_rejects_subprocesses_without_output_pipes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The executor rejects a subprocess that violates its pipe invariant."""
    process = _MissingPipesProcess()

    async def create_process(
        *_args: object,
        **_kwargs: object,
    ) -> _MissingPipesProcess:
        return process

    monkeypatch.setattr(
        "devtools.commands.execution.asyncio.create_subprocess_exec",
        create_process,
    )

    with pytest.raises(CommandError, match="streams were not created"):
        asyncio.run(CommandExecutor().execute(Command("missing-pipes-command")))


def test_executor_kills_and_drains_a_timed_out_process(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A timeout kills the immediate process and awaits its final communication."""
    process = _TimedOutProcess()

    async def create_process(
        *_args: object,
        **_kwargs: object,
    ) -> _TimedOutProcess:
        return process

    monkeypatch.setattr(
        "devtools.commands.execution.asyncio.create_subprocess_exec",
        create_process,
    )

    with pytest.raises(CommandTimeoutError, match=r"0\.001 seconds"):
        asyncio.run(
            CommandExecutor().execute(
                Command("slow-command", timeout=Duration.seconds(0.001)),
            ),
        )

    assert process.killed is True
    assert process.waited is True


def test_executor_rejects_a_timeout_without_timeout_policy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A defensive timeout invariant rejects an unexpected missing policy."""
    executor = CommandExecutor()
    process = _TimedOutProcess()

    async def create_process(
        *_args: object,
        **_kwargs: object,
    ) -> _TimedOutProcess:
        return process

    async def raise_timeout(
        _process: object,
        _execution: object,
        _command: object,
    ) -> tuple[bytes, bytes]:
        raise TimeoutError

    monkeypatch.setattr(
        "devtools.commands.execution.asyncio.create_subprocess_exec",
        create_process,
    )
    monkeypatch.setattr(executor, "_collect_output", raise_timeout)

    with pytest.raises(CommandError, match="without a configured timeout"):
        asyncio.run(executor.execute(Command("unexpected-timeout-command")))

    assert process.killed is True
    assert process.waited is True


def test_executor_bounds_retained_output_and_pending_events(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Configured limits truncate retained bytes and drop excess queued events."""
    process = _OutputProcess()

    async def create_process(
        *_args: object,
        **_kwargs: object,
    ) -> _OutputProcess:
        return process

    monkeypatch.setattr(
        "devtools.commands.execution.asyncio.create_subprocess_exec",
        create_process,
    )

    async def run() -> None:
        executor = CommandExecutor(
            output_policy=CommandOutputPolicy(
                max_stdout_bytes=3,
                max_stderr_bytes=2,
                max_pending_events=1,
            ),
        )
        execution = executor.start(Command("bounded-output-command"))
        result = await execution
        events = [event async for event in execution.events()]

        assert result.stdout == b"abc"
        assert result.stderr == b"wx"
        assert result.stdout_truncated is True
        assert result.stderr_truncated is True
        expected_dropped_events = 4

        assert result.events_dropped == expected_dropped_events
        assert len(events) == 1

    asyncio.run(run())


class _TimedOutProcess:
    """Minimal subprocess fake that times out once before cleanup completes."""

    def __init__(self) -> None:
        """Initialize the fake process state."""
        self.killed = False
        self.returncode = None
        self.stderr = _EmptyStream()
        self.stdout = _TimeoutStream()
        self.waited = False

    def kill(self) -> None:
        """Record immediate-process termination."""
        self.killed = True

    async def wait(self) -> None:
        """Record that the executor awaited process cleanup."""
        self.waited = True


class _NoExitCodeProcess:
    """Minimal completed-process fake with an invalid absent exit code."""

    def __init__(self) -> None:
        """Initialize completed empty output streams without an exit code."""
        self.returncode: None = None
        self.stderr = _EmptyStream()
        self.stdout = _EmptyStream()

    async def wait(self) -> None:
        """Model a completed process wait operation."""


class _MissingPipesProcess:
    """Minimal process fake whose output-pipe invariant is invalid."""

    returncode = 0
    stderr = None
    stdout = None


class _OutputProcess:
    """Minimal completed process producing output beyond configured bounds."""

    def __init__(self) -> None:
        """Initialize deterministic output streams and completion state."""
        self.returncode: int | None = None
        self.stderr = _ChunkStream((b"wxyz",))
        self.stdout = _ChunkStream((b"abc", b"def"))

    async def wait(self) -> None:
        """Mark the process as successfully completed."""
        self.returncode = 0


class _EmptyStream:
    """Minimal stream fake that is immediately exhausted."""

    async def read(self, _size: int) -> bytes:
        """Return end-of-stream bytes."""
        return b""


class _TimeoutStream:
    """Minimal stream fake that reports a deterministic timeout."""

    async def read(self, _size: int) -> bytes:
        """Raise the timeout handled by the executor lifecycle."""
        raise TimeoutError


class _ChunkStream:
    """Minimal stream fake that returns a fixed sequence of chunks."""

    def __init__(self, chunks: tuple[bytes, ...]) -> None:
        """Initialize the remaining chunk sequence."""
        self._chunks = list(chunks)

    async def read(self, _size: int) -> bytes:
        """Return the next chunk or end-of-stream bytes."""
        if not self._chunks:
            return b""

        return self._chunks.pop(0)
