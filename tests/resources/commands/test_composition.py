# Copyright (c) 2026
"""Codex destination-integration regressions across all five Commands features."""

from __future__ import annotations

import asyncio
import os
import sys
from typing import TYPE_CHECKING

import pytest

from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import (
    Command,
    CommandEvent,
    CommandExecutor,
    CommandExited,
    CommandOutputPolicy,
    CommandResult,
    CommandStarted,
)

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize("payload", [b"", b"\0\xff" + bytes(range(256)) * 32])
def test_composed_binary_input_environment_status_and_decoding(
    payload: bytes,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Real children preserve independent value policies and raw process facts."""
    monkeypatch.setenv("DEVTOOLS_COMMANDS_COMPOSED", "parent")
    monkeypatch.setenv("DEVTOOLS_COMMANDS_INHERITED", "inherited")
    environment = {"DEVTOOLS_COMMANDS_COMPOSED": "child"}
    script = (
        "import os,sys; data=sys.stdin.buffer.read(); "
        "prefix=(os.environ['DEVTOOLS_COMMANDS_COMPOSED']+'|'"
        "+os.environ['DEVTOOLS_COMMANDS_INHERITED']+'|').encode(); "
        "sys.stdout.buffer.write(prefix+data); "
        "sys.stderr.buffer.write('\\u96ea|done'.encode()); sys.exit(17)"
    )
    base = Command(sys.executable)
    command = (
        base.with_stdin(payload)
        .with_environment(environment)
        .with_success_exit_codes(17)
        .with_args("-c", script)
        .cwd(resolve_path(tmp_path))
        .with_timeout(Duration.seconds(10))
    )
    equal = Command(
        sys.executable,
        arguments=("-c", script),
        working_directory=resolve_path(tmp_path),
        timeout=Duration.seconds(10),
        stdin=payload,
        environment={"DEVTOOLS_COMMANDS_COMPOSED": "child"},
        success_exit_codes=frozenset({17}),
    )
    assert command == equal
    assert hash(command) == hash(equal)
    environment["DEVTOOLS_COMMANDS_COMPOSED"] = "caller-mutated"
    assert command == equal
    assert hash(command) == hash(equal)
    assert command.with_args("-V").stdin == payload
    assert command.with_args("-V").environment == equal.environment
    assert command.with_args("-V").success_exit_codes == frozenset({17})
    assert base.stdin is None
    assert base.environment is None
    assert base.success_exit_codes == frozenset({0})

    async def exercise() -> tuple[CommandResult, list[CommandEvent]]:
        execution = CommandExecutor(
            output_policy=CommandOutputPolicy(
                max_stdout_bytes=257,
                max_stderr_bytes=64,
                max_pending_events=32,
            ),
        ).start(command)
        events = [event async for event in execution.events()]
        return await execution, events

    result, events = asyncio.run(exercise())
    expected = b"child|inherited|" + payload
    assert result.command == command
    assert result.exit_code == 17  # noqa: PLR2004 -- configured real child status
    assert result.succeeded
    assert not result.failed
    assert result.stdout == expected[:257]
    assert result.stdout_truncated == (len(expected) > 257)  # noqa: PLR2004
    assert result.stdout_text(errors="replace") == expected[:257].decode(
        errors="replace",
    )
    assert result.stderr_text() == "雪|done"
    assert not result.stderr_truncated
    assert isinstance(events[0], CommandStarted)
    assert isinstance(events[-1], CommandExited)
    assert events[-1].exit_code == result.exit_code
    assert os.environ["DEVTOOLS_COMMANDS_COMPOSED"] == "parent"
    assert os.environ["DEVTOOLS_COMMANDS_INHERITED"] == "inherited"
