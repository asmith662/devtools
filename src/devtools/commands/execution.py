# Copyright (c) 2026
"""Asynchronous command execution."""

from __future__ import annotations

import asyncio
from dataclasses import replace
from functools import partial
from typing import TYPE_CHECKING

from devtools.commands.errors import (
    CommandError,
    CommandNotFoundError,
    CommandTimeoutError,
)
from devtools.commands.events import (
    CommandExited,
    CommandStarted,
    CommandStderr,
    CommandStdout,
)
from devtools.commands.handle import CommandExecution
from devtools.commands.models import Command, CommandOutputPolicy, CommandResult
from devtools.time import Stopwatch

if TYPE_CHECKING:
    from collections.abc import Callable

    from devtools.commands.events import CommandEvent


_DEFAULT_OUTPUT_POLICY = CommandOutputPolicy()


class CommandExecutor:
    """Execute commands asynchronously."""

    def __init__(
        self,
        *,
        output_policy: CommandOutputPolicy = _DEFAULT_OUTPUT_POLICY,
    ) -> None:
        """Create a command executor.

        :param output_policy: Per-execution output-retention limits.
        """
        self._output_policy = output_policy

    def start(self, command: Command) -> CommandExecution:
        """Start a command and return its live execution handle.

        The returned execution begins immediately and may be awaited for the
        final result or observed through its event stream.

        :param command: Command to execute.
        :returns: Live command execution.
        """
        return CommandExecution(
            partial(self._run, command),
            max_pending_events=self._output_policy.max_pending_events,
        )

    async def execute(self, command: Command) -> CommandResult:
        """Execute a command and await its final result.

        This is the convenience API for callers that do not need live event
        streaming.

        :param command: Command to execute.
        :returns: Completed command result.
        """
        return await self.start(command)

    async def _run(
        self,
        command: Command,
        execution: CommandExecution,
    ) -> CommandResult:
        """Run one command execution.

        :param command: Command to execute.
        :param execution: Live execution receiving emitted events.
        :returns: Completed command result.
        :raises CommandNotFoundError: If the executable cannot be found.
        :raises CommandTimeoutError: If execution exceeds its timeout.
        :raises CommandError: If the process completes without an exit code.
        """
        stopwatch = Stopwatch()
        process: asyncio.subprocess.Process | None = None

        try:
            process = await self._create_process(command)

            execution._emit(CommandStarted(command=command))  # noqa: SLF001

            try:
                (
                    stdout,
                    stderr,
                    stdout_truncated,
                    stderr_truncated,
                ) = await self._collect_output(
                    process,
                    execution,
                    command,
                )
            except TimeoutError as error:
                await self._terminate_and_reap(process)

                timeout = command.timeout

                if timeout is None:
                    msg = "Command timed out without a configured timeout."
                    raise CommandError(msg) from error

                msg = (
                    f"Command exceeded timeout of "
                    f"{timeout.total_seconds} seconds: "
                    f"{command.executable!r}."
                )
                raise CommandTimeoutError(msg) from error

        except asyncio.CancelledError:
            if process is not None:
                await self._terminate_and_reap(process)

            raise

        else:
            duration = stopwatch.stop()
            exit_code = process.returncode

            if exit_code is None:
                msg = (
                    "Command process completed without an exit code: "
                    f"{command.executable!r}."
                )
                raise CommandError(msg)

            result = CommandResult(
                command=command,
                exit_code=exit_code,
                stdout=stdout,
                stderr=stderr,
                duration=duration,
                stdout_truncated=stdout_truncated,
                stderr_truncated=stderr_truncated,
            )

            execution._emit(  # noqa: SLF001
                CommandExited(
                    exit_code=exit_code,
                    duration=duration,
                ),
            )

            return replace(result, events_dropped=execution.events_dropped)
        finally:
            stopwatch.stop()
            execution._close_events()  # noqa: SLF001

    async def _terminate_and_reap(
        self,
        process: asyncio.subprocess.Process,
    ) -> None:
        """Terminate and reap a running immediate child process."""
        if process.returncode is None:
            process.kill()

        await process.wait()

    async def _create_process(
        self,
        command: Command,
    ) -> asyncio.subprocess.Process:
        """Create the subprocess for a command.

        :param command: Command to execute.
        :returns: Running subprocess.
        :raises CommandNotFoundError: If the executable cannot be found.
        """
        try:
            return await asyncio.create_subprocess_exec(
                *command.argv,
                cwd=(
                    command.working_directory.value
                    if command.working_directory is not None
                    else None
                ),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        except FileNotFoundError as error:
            msg = f"Command executable not found: {command.executable!r}."
            raise CommandNotFoundError(msg) from error

    async def _collect_output(
        self,
        process: asyncio.subprocess.Process,
        execution: CommandExecution,
        command: Command,
    ) -> tuple[bytes, bytes, bool, bool]:
        """Collect stdout and stderr while emitting streaming events.

        :param process: Running subprocess.
        :param execution: Live execution receiving events.
        :param command: Command defining timeout policy.
        :returns: Complete stdout and stderr byte sequences.
        :raises TimeoutError: If the configured timeout expires.
        """
        operation = self._stream_process(
            process,
            execution,
            self._output_policy,
        )
        timeout = command.timeout

        if timeout is None:
            return await operation

        async with asyncio.timeout(timeout.total_seconds):
            return await operation

    async def _stream_process(
        self,
        process: asyncio.subprocess.Process,
        execution: CommandExecution,
        output_policy: CommandOutputPolicy,
    ) -> tuple[bytes, bytes, bool, bool]:
        """Stream subprocess output while preserving complete output.

        :param process: Running subprocess.
        :param execution: Live execution receiving events.
        :returns: Complete stdout and stderr byte sequences.
        """
        if process.stdout is None or process.stderr is None:
            msg = "Command subprocess streams were not created."
            raise CommandError(msg)

        stdout_task = asyncio.create_task(
            self._read_stream(
                process.stdout,
                execution._emit,  # noqa: SLF001
                CommandStdout,
                output_policy.max_stdout_bytes,
            ),
        )
        stderr_task = asyncio.create_task(
            self._read_stream(
                process.stderr,
                execution._emit,  # noqa: SLF001
                CommandStderr,
                output_policy.max_stderr_bytes,
            ),
        )

        (stdout, stdout_truncated), (stderr, stderr_truncated) = await asyncio.gather(
            stdout_task,
            stderr_task,
        )

        await process.wait()

        return stdout, stderr, stdout_truncated, stderr_truncated

    async def _read_stream(
        self,
        stream: asyncio.StreamReader,
        emit: Callable[[CommandEvent], None],
        event_type: type[CommandStdout | CommandStderr],
        max_output_bytes: int,
    ) -> tuple[bytes, bool]:
        """Read, emit, and retain bounded chunks from one subprocess stream."""
        output = bytearray()
        truncated = False

        while chunk := await stream.read(8192):
            remaining = max_output_bytes - len(output)

            if remaining > 0:
                output.extend(chunk[:remaining])

            if len(chunk) > remaining:
                truncated = True

            emit(event_type(data=chunk))

        return bytes(output), truncated
