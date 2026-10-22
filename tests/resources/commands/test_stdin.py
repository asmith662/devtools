# Copyright (c) 2026
"""Independent permanent tests of binary input and the managed child lifecycle."""

from __future__ import annotations

import asyncio
import hashlib
import sys
from dataclasses import FrozenInstanceError
from types import SimpleNamespace
from typing import TYPE_CHECKING, cast

import pytest

from devtools.core.paths import ResolvedPath
from devtools.core.time import Duration
from devtools.resources.commands import (
    Command,
    CommandExecutor,
    CommandStarted,
    CommandTimeoutError,
)

if TYPE_CHECKING:
    from pathlib import Path


def test_binary_stdin_is_an_immutable_command_value(tmp_path: Path) -> None:
    """Binary input participates in values and survives every fluent operation."""
    command = Command(sys.executable, stdin=b"a\x00\xff")
    assert Command(sys.executable).stdin is None
    assert command.stdin == b"a\x00\xff"
    assert command == Command(sys.executable, stdin=b"a\x00\xff")
    assert hash(command) == hash(Command(sys.executable, stdin=b"a\x00\xff"))
    assert command != Command(sys.executable, stdin=b"other")
    assert command.with_stdin(b"").stdin == b""
    assert command.without_stdin().stdin is None
    transformations = (
        command.args("-V"),
        command.with_args("-V"),
        command.without_args(),
        command.with_executable(sys.executable),
        command.cwd(ResolvedPath(tmp_path)),
        command.without_cwd(),
        command.with_timeout(Duration.seconds(2)),
        command.without_timeout(),
    )
    assert all(item.stdin == command.stdin for item in transformations)
    attribute = "stdin"
    with pytest.raises(FrozenInstanceError):
        setattr(command, attribute, b"changed")


@pytest.mark.parametrize(
    "invalid",
    ["text", bytearray(b"x"), 1, False, memoryview(b"x")],
)
def test_binary_stdin_rejects_mutable_or_nonbyte_inputs(invalid: object) -> None:
    """Validation occurs before process creation, including fluent replacement."""
    with pytest.raises(TypeError):
        Command(sys.executable, stdin=cast("bytes", invalid))
    with pytest.raises(TypeError):
        Command(sys.executable).with_stdin(cast("bytes", invalid))


@pytest.mark.parametrize(
    "data",
    [b"", b"\x00\xff\r\n\n", b"abc" * 100000],
    ids=("empty", "binary", "large"),
)
def test_binary_stdin_delivers_exact_bytes_and_eof(data: bytes) -> None:
    """The child sees complete input and EOF, while output/result identity survive."""
    script = (
        "import sys; data=sys.stdin.buffer.read(); "
        "sys.stdout.buffer.write(data); sys.stderr.buffer.write(b'err')"
    )
    command = Command(
        sys.executable,
        ("-c", script),
        stdin=data,
        timeout=Duration.seconds(8),
    )
    result = asyncio.run(CommandExecutor().execute(command))
    assert result.succeeded
    assert result.stdout == data
    assert result.stderr == b"err"
    assert result.command is command


def test_binary_stdin_and_both_output_streams_make_concurrent_progress() -> None:
    """Large output before reading input must not deadlock the pipe lifecycle."""
    payload = b"input" * 50000
    script = (
        "import sys,hashlib; sys.stdout.buffer.write(b'o'*200000); "
        "sys.stdout.buffer.flush(); sys.stderr.buffer.write(b'e'*200000); "
        "sys.stderr.buffer.flush(); data=sys.stdin.buffer.read(); "
        "print(hashlib.sha256(data).hexdigest())"
    )
    result = asyncio.run(
        CommandExecutor().execute(
            Command(
                sys.executable,
                ("-c", script),
                stdin=payload,
                timeout=Duration.seconds(8),
            ),
        ),
    )
    assert result.succeeded
    assert result.stdout[:200000] == b"o" * 200000
    assert result.stdout[200000:].splitlines() == [
        hashlib.sha256(payload).hexdigest().encode(),
    ]
    assert result.stderr == b"e" * 200000


def test_binary_stdin_preserves_early_child_exit() -> None:
    """A child may close its input without turning a normal result into an error."""
    command = Command(
        sys.executable,
        ("-c", "import sys; sys.exit(7)"),
        stdin=b"x" * 300000,
        timeout=Duration.seconds(8),
    )
    result = asyncio.run(CommandExecutor().execute(command))
    assert result.exit_code == 7  # noqa: PLR2004 -- exact child exit status


def test_timeout_includes_blocked_binary_input() -> None:
    """The existing timeout also bounds a child that does not read its input."""
    command = Command(
        sys.executable,
        ("-c", "import time; time.sleep(5)"),
        stdin=b"x" * 300000,
        timeout=Duration.seconds(0.1),
    )
    with pytest.raises(CommandTimeoutError):
        asyncio.run(CommandExecutor().execute(command))


def test_concurrent_commands_keep_binary_inputs_separate() -> None:
    """Two managed executions never share mutable input transport state."""

    async def run() -> list[bytes]:
        results = await asyncio.gather(
            *(
                CommandExecutor().execute(
                    Command(
                        sys.executable,
                        (
                            "-c",
                            (
                                "import sys; "
                                "sys.stdout.buffer.write(sys.stdin.buffer.read())"
                            ),
                        ),
                        stdin=data,
                        timeout=Duration.seconds(8),
                    ),
                )
                for data in (b"first", b"second")
            ),
        )
        return [result.stdout for result in results]

    assert asyncio.run(run()) == [b"first", b"second"]


@pytest.mark.parametrize("payload", [None, b""])
def test_only_explicit_input_creates_a_pipe(payload: bytes | None) -> None:
    """Empty input must get an EOF pipe; None preserves inherited stdin."""
    pipes: list[bool] = []

    class InspectingExecutor(CommandExecutor):
        async def _create_process(self, command: Command) -> asyncio.subprocess.Process:
            process = await super()._create_process(command)
            pipes.append(process.stdin is not None)
            return process

    script = (
        "import sys; sys.stdout.buffer.write(sys.stdin.buffer.read())"
        if payload is not None
        else "print('inherited')"
    )
    result = asyncio.run(
        InspectingExecutor().execute(
            Command(
                sys.executable,
                ("-c", script),
                stdin=payload,
                timeout=Duration.seconds(8),
            ),
        ),
    )
    assert result.succeeded
    assert pipes == [payload is not None]


def test_cancellation_reaps_child_with_blocked_input() -> None:
    """Cancellation propagates through feeding/draining and reaps the real child."""
    processes: list[asyncio.subprocess.Process] = []

    class ObservedExecutor(CommandExecutor):
        async def _create_process(self, command: Command) -> asyncio.subprocess.Process:
            process = await super()._create_process(command)
            processes.append(process)
            return process

    async def run() -> None:
        async with asyncio.timeout(8):
            execution = ObservedExecutor().start(
                Command(
                    sys.executable,
                    ("-c", "import time; time.sleep(5)"),
                    stdin=b"x" * 300000,
                ),
            )
            pending = asyncio.ensure_future(execution)
            events = execution.events()
            assert isinstance(await anext(events), CommandStarted)
            pending.cancel()
            with pytest.raises(asyncio.CancelledError):
                await pending
            assert execution.is_complete
            assert processes[0].returncode is not None

    asyncio.run(run())


def test_absent_payload_leaves_an_existing_input_pipe_untouched() -> None:
    """An absent payload never writes or closes a pipe owned by another caller."""
    process = cast("asyncio.subprocess.Process", SimpleNamespace(stdin=object()))
    asyncio.run(CommandExecutor._feed_stdin(process, None))  # noqa: SLF001 -- optional-payload transport boundary
