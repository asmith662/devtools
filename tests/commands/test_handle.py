# Copyright (c) 2026
"""Tests for public command execution handles."""

from __future__ import annotations

import asyncio
import sys

import pytest

from devtools.commands import (
    Command,
    CommandExecution,
    CommandExecutor,
    CommandExited,
    CommandNotFoundError,
    CommandStarted,
    CommandStderr,
    CommandStdout,
    CommandTimeoutError,
)
from devtools.time import Duration


def test_start_returns_one_awaitable_execution_handle() -> None:
    """A started command should create one awaitable live execution handle."""

    async def run() -> None:
        execution = CommandExecutor().start(
            Command(sys.executable, ("-c", "print('once')")),
        )

        assert isinstance(execution, CommandExecution)
        assert execution.is_running is True
        assert execution.is_complete is False

        first = await execution
        second = await execution

        assert first is second
        assert first.stdout.strip() == b"once"
        assert execution.is_running is False
        assert execution.is_complete is True

    asyncio.run(run())


def test_event_stream_preserves_output_and_closes_before_final_await() -> None:
    """Streaming observations and the final result share one execution."""

    async def run() -> None:
        execution = CommandExecutor().start(
            Command(
                sys.executable,
                (
                    "-c",
                    "import sys; print('out'); print('err', file=sys.stderr)",
                ),
            ),
        )
        events = [event async for event in execution.events()]
        result = await execution

        assert isinstance(events[0], CommandStarted)
        assert any(
            isinstance(event, CommandStdout) and b"out" in event.data
            for event in events
        )
        assert any(
            isinstance(event, CommandStderr) and b"err" in event.data
            for event in events
        )
        assert result.stdout.strip() == b"out"
        assert result.stderr.strip() == b"err"

    asyncio.run(run())


def test_event_stream_allows_only_one_consumer() -> None:
    """A second event consumer cannot silently split one execution stream."""

    async def run() -> None:
        execution = CommandExecutor().start(
            Command(sys.executable, ("-c", "pass")),
        )
        first_stream = execution.events()

        await anext(first_stream)

        with pytest.raises(RuntimeError, match="only be consumed once"):
            await anext(execution.events())

        async for _event in first_stream:
            pass

        await execution

    asyncio.run(run())


def test_missing_executable_closes_the_event_stream(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Failure during process creation does not leave event consumers waiting."""

    async def raise_not_found(*_args: object, **_kwargs: object) -> None:
        raise FileNotFoundError

    async def run() -> None:
        execution = CommandExecutor().start(Command("missing-command"))
        events = [event async for event in execution.events()]

        assert events == []

        with pytest.raises(CommandNotFoundError):
            await execution

    monkeypatch.setattr(
        "devtools.commands.execution.asyncio.create_subprocess_exec",
        raise_not_found,
    )
    asyncio.run(run())


def test_timeout_closes_the_event_stream(monkeypatch: pytest.MonkeyPatch) -> None:
    """Timeout cleanup closes event iteration before propagating the error."""
    process = _TimedOutProcess()

    async def create_process(
        *_args: object,
        **_kwargs: object,
    ) -> _TimedOutProcess:
        return process

    async def run() -> None:
        execution = CommandExecutor().start(
            Command("slow-command", timeout=Duration.seconds(0.001)),
        )
        events = [event async for event in execution.events()]

        assert len(events) == 1
        assert isinstance(events[0], CommandStarted)

        with pytest.raises(CommandTimeoutError):
            await execution

    monkeypatch.setattr(
        "devtools.commands.execution.asyncio.create_subprocess_exec",
        create_process,
    )
    asyncio.run(run())


def test_cancellation_kills_reaps_and_closes_events(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cancelling a live execution cleans up its immediate child process."""
    process = _BlockingProcess()

    async def create_process(
        *_args: object,
        **_kwargs: object,
    ) -> _BlockingProcess:
        return process

    async def await_execution(execution: CommandExecution) -> None:
        """Await one execution so caller cancellation reaches its task."""
        await execution

    async def run() -> None:
        execution = CommandExecutor().start(Command("blocking-command"))
        events_task = asyncio.create_task(_collect_events(execution))
        awaiter = asyncio.create_task(await_execution(execution))
        shared_awaiter = asyncio.create_task(await_execution(execution))

        await process.stdout.read_started.wait()
        awaiter.cancel()

        with pytest.raises(asyncio.CancelledError):
            await awaiter

        with pytest.raises(asyncio.CancelledError):
            await shared_awaiter

        events = await events_task

        assert process.killed is True
        assert process.waited is True
        assert any(isinstance(event, CommandStarted) for event in events)
        assert not any(isinstance(event, CommandExited) for event in events)

    monkeypatch.setattr(
        "devtools.commands.execution.asyncio.create_subprocess_exec",
        create_process,
    )
    asyncio.run(run())


def test_stream_read_failure_reaps_process_and_closes_events(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An unexpected stream failure does not leave the immediate child running."""
    process = _FailingStreamProcess()

    async def create_process(
        *_args: object,
        **_kwargs: object,
    ) -> _FailingStreamProcess:
        return process

    async def run() -> None:
        execution = CommandExecutor().start(Command("failing-stream-command"))
        events_task = asyncio.create_task(_collect_events(execution))

        with pytest.raises(RuntimeError, match="stream failure"):
            await execution

        events = await events_task
        assert process.killed is True
        assert process.waited is True
        assert any(isinstance(event, CommandStarted) for event in events)
        assert not any(isinstance(event, CommandExited) for event in events)

    monkeypatch.setattr(
        "devtools.commands.execution.asyncio.create_subprocess_exec",
        create_process,
    )
    asyncio.run(run())


def test_cancellation_before_process_creation_closes_events(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cancellation while creating a process still closes its event stream."""
    process_creation_started = asyncio.Event()
    process_creation_release = asyncio.Event()

    async def create_process(*_args: object, **_kwargs: object) -> None:
        process_creation_started.set()
        await process_creation_release.wait()

    async def await_execution(
        execution: CommandExecution,
        awaiting_execution: asyncio.Event,
    ) -> None:
        """Await an execution after reporting that cancellation can propagate."""
        awaiting_execution.set()
        await execution

    async def run() -> None:
        execution = CommandExecutor().start(Command("creating-command"))
        events_task = asyncio.create_task(_collect_events(execution))
        awaiting_execution = asyncio.Event()
        awaiter = asyncio.create_task(await_execution(execution, awaiting_execution))

        await process_creation_started.wait()
        await awaiting_execution.wait()
        awaiter.cancel()

        with pytest.raises(asyncio.CancelledError):
            await awaiter

        assert await events_task == []

    monkeypatch.setattr(
        "devtools.commands.execution.asyncio.create_subprocess_exec",
        create_process,
    )
    asyncio.run(run())


def test_cancellation_reaps_an_already_exited_process(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cancellation reaps a child without killing it after it has exited."""
    process = _BlockingProcess(returncode=0)

    async def create_process(
        *_args: object,
        **_kwargs: object,
    ) -> _BlockingProcess:
        return process

    async def run() -> None:
        execution = CommandExecutor().start(Command("completed-command"))
        awaiter = asyncio.ensure_future(execution)

        await process.stdout.read_started.wait()
        awaiter.cancel()

        with pytest.raises(asyncio.CancelledError):
            await awaiter

        assert process.killed is False
        assert process.waited is True

    monkeypatch.setattr(
        "devtools.commands.execution.asyncio.create_subprocess_exec",
        create_process,
    )
    asyncio.run(run())


async def _collect_events(execution: CommandExecution) -> list[object]:
    """Collect an execution event stream until it closes."""
    return [event async for event in execution.events()]


class _TimedOutProcess:
    """Minimal process fake that times out while streaming standard output."""

    def __init__(self) -> None:
        """Initialize the process and stream state."""
        self.killed = False
        self.returncode = None
        self.stderr = _EmptyStream()
        self.stdout = _TimeoutStream()
        self.waited = False

    def kill(self) -> None:
        """Record immediate child-process termination."""
        self.killed = True

    async def wait(self) -> None:
        """Record process cleanup completion."""
        self.waited = True


class _EmptyStream:
    """Minimal stream fake that is immediately exhausted."""

    async def read(self, _size: int) -> bytes:
        """Return end-of-stream bytes."""
        return b""


class _TimeoutStream:
    """Minimal stream fake that reports the tested timeout."""

    async def read(self, _size: int) -> bytes:
        """Raise the timeout handled by the execution lifecycle."""
        raise TimeoutError


class _BlockingProcess:
    """Minimal process fake that remains active until cancellation cleanup."""

    def __init__(self, *, returncode: int | None = None) -> None:
        """Initialize process state and a blocking stdout stream."""
        self.killed = False
        self.returncode = returncode
        self.stderr = _EmptyStream()
        self.stdout = _BlockingStream()
        self.waited = False

    def kill(self) -> None:
        """Record immediate child-process termination."""
        self.killed = True

    async def wait(self) -> None:
        """Record process reaping during cancellation cleanup."""
        self.waited = True


class _BlockingStream:
    """Minimal stream fake that remains blocked until task cancellation."""

    def __init__(self) -> None:
        """Initialize deterministic read-start coordination."""
        self.read_started = asyncio.Event()
        self._release = asyncio.Event()

    async def read(self, _size: int) -> bytes:
        """Wait until cancellation interrupts the active read."""
        self.read_started.set()
        await self._release.wait()
        return b""


class _FailingStreamProcess:
    """Minimal process fake whose stdout read fails unexpectedly."""

    def __init__(self) -> None:
        """Initialize a running process with one failing stream."""
        self.killed = False
        self.returncode: int | None = None
        self.stderr = _EmptyStream()
        self.stdout = _FailingStream()
        self.waited = False

    def kill(self) -> None:
        """Record immediate-process termination."""
        self.killed = True

    async def wait(self) -> None:
        """Record process cleanup completion."""
        self.waited = True


class _FailingStream:
    """Minimal stream fake that raises a deterministic read failure."""

    async def read(self, _size: int) -> bytes:
        """Raise the unexpected stream failure under test."""
        message = "stream failure"
        raise RuntimeError(message)
