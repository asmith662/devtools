# Copyright (c) 2026
"""Independent regression tests for task-local command exit interpretation."""

from __future__ import annotations

import asyncio
import sys
from dataclasses import FrozenInstanceError, replace
from enum import IntEnum
from typing import TYPE_CHECKING, cast

import pytest

from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import (
    Command,
    CommandExecutor,
    CommandExited,
    CommandOutputPolicy,
    CommandResult,
    CommandStarted,
)
from devtools.tools import ToolRunner
from devtools.tools.command import CommandTool

if TYPE_CHECKING:
    from pathlib import Path


def test_success_code_values_are_immutable_and_include_all_command_dimensions() -> None:
    """Explicit interpretation preserves frozen values and structural hashing."""
    original = Command(sys.executable, stdin=b"input\0", environment={"KEY": "value"})
    command = original.with_success_exit_codes(7, 0, 7)
    assert command.success_exit_codes == frozenset({0, 7})
    assert type(command.success_exit_codes) is frozenset
    assert original.success_exit_codes == frozenset({0})
    equal = replace(original, success_exit_codes=frozenset({0, 7}))
    different = replace(original, success_exit_codes=frozenset({0}))
    assert command == equal
    assert hash(command) == hash(equal)
    assert command != different
    assert len({command, equal, different}) == len({command, different})
    assert not hasattr(command, "__dict__")
    attribute = "success_exit_codes"
    with pytest.raises(FrozenInstanceError):
        setattr(command, attribute, frozenset())
    restored = command.without_success_exit_codes()
    assert restored == original
    assert restored.stdin == original.stdin
    assert restored.environment == original.environment


@pytest.mark.parametrize(
    "value",
    [
        None,
        [],
        (),
        {0},
        "0",
        0,
        False,
        frozenset({True}),
        frozenset({1.5}),
        frozenset({"0"}),
    ],
)
def test_constructor_refuses_mutable_policies_and_noninteger_codes(
    value: object,
) -> None:
    """A success specification cannot hide mutable data or boolean codes."""
    with pytest.raises(TypeError):
        Command(sys.executable, success_exit_codes=cast("frozenset[int]", value))


@pytest.mark.parametrize(
    "values",
    [(True,), (1, True), (True, 1), (False, 0), (0, False), ("0",), (1.0,), (None,)],
)
def test_fluent_validation_checks_every_argument_before_deduplication(
    values: tuple[object, ...],
) -> None:
    """Boolean/integer equality cannot conceal an invalid supplied argument."""
    original = Command(sys.executable)
    with pytest.raises(TypeError):
        original.with_success_exit_codes(*cast("tuple[int, ...]", values))
    assert original.success_exit_codes == frozenset({0})


def test_exit_codes_survive_every_existing_fluent_dimension(tmp_path: Path) -> None:
    """Changing arguments, process context or input does not reset interpretation."""
    command = Command(sys.executable).with_success_exit_codes(1, 7)
    for updated in (
        command.args("-V"),
        command.with_args("-V"),
        command.without_args(),
        command.with_executable(sys.executable),
        command.cwd(resolve_path(tmp_path)),
        command.without_cwd(),
        command.with_timeout(Duration.seconds(3)),
        command.without_timeout(),
        command.with_stdin(b"input"),
        command.without_stdin(),
        command.with_environment({"KEY": "value"}),
        command.without_environment(),
    ):
        assert updated.success_exit_codes == command.success_exit_codes


class _Exit(IntEnum):
    """An integer-valued consumer exit vocabulary remains usable."""

    DIFFERENT = 1


def test_integer_subclasses_and_empty_policy_have_explicit_meaning() -> None:
    """Integer values remain literal and an empty set means no successful exit."""
    command = Command(sys.executable).with_success_exit_codes(_Exit.DIFFERENT, -9)
    assert command.success_exit_codes == frozenset({1, -9})
    assert command.with_success_exit_codes().success_exit_codes == frozenset()


@pytest.mark.parametrize(
    ("codes", "status", "wanted"),
    [
        (frozenset({0}), 0, True),
        (frozenset({0}), 1, False),
        (frozenset({1}), 1, True),
        (frozenset({1}), 0, False),
        (frozenset(), 0, False),
        (frozenset({-9}), -9, True),
    ],
)
def test_result_interpretation_preserves_raw_process_facts(
    codes: frozenset[int],
    status: int,
    *,
    wanted: bool,
) -> None:
    """Classification changes neither the status nor any captured result field."""
    command = Command(sys.executable, success_exit_codes=codes)
    result = CommandResult(command, status, b"out", b"err", Duration.seconds(1))
    assert result.succeeded is wanted
    assert result.failed is not wanted
    assert result.exit_code == status
    assert result.command is command
    assert result.stdout == b"out"
    assert result.stdout_text() == "out"
    assert result.stderr == b"err"
    assert result.stderr_text() == "err"


def test_real_child_tool_and_handle_preserve_nonzero_success_and_inputs(
    tmp_path: Path,
) -> None:
    """The existing execution/Tool paths transport policy without normalizing exit."""
    script = (
        "import os,sys;sys.stdout.buffer.write("
        "os.environ['DEVTOOLS_EXIT14'].encode()+b'|'+sys.stdin.buffer.read());"
        "sys.stderr.buffer.write(b'err');sys.exit(int(sys.argv[1]))"
    )
    command = Command(
        sys.executable,
        ("-c", script, "1"),
        working_directory=resolve_path(tmp_path),
        timeout=Duration.seconds(8),
        stdin=b"\0\xff\r\n",
        environment={"DEVTOOLS_EXIT14": "overlay"},
    ).with_success_exit_codes(0, 1)

    async def run() -> None:
        executor = CommandExecutor()
        result = await ToolRunner().execute(CommandTool(executor), command)
        assert result.succeeded
        assert not result.failed
        assert result.exit_code == _Exit.DIFFERENT
        assert result.command is command
        assert result.stdout == b"overlay|\0\xff\r\n"
        assert result.stderr == b"err"
        execution = executor.start(command)
        events = [event async for event in execution.events()]
        streamed = await execution
        assert streamed.succeeded
        assert await execution is streamed
        assert any(
            isinstance(e, CommandStarted) and e.command is command for e in events
        )
        assert [e.exit_code for e in events if isinstance(e, CommandExited)] == [1]
        default = await executor.execute(command.without_success_exit_codes())
        assert default.exit_code == _Exit.DIFFERENT
        assert default.failed
        excluded_zero = await executor.execute(
            command.with_args("-c", script, "0").with_success_exit_codes(7),
        )
        assert excluded_zero.exit_code == 0
        assert excluded_zero.failed
        empty = await executor.execute(
            command.with_args("-c", script, "0").with_success_exit_codes(),
        )
        assert empty.exit_code == 0
        assert empty.failed
        bounded = await CommandExecutor(
            output_policy=CommandOutputPolicy(max_stdout_bytes=3, max_stderr_bytes=1),
        ).execute(command)
        assert bounded.succeeded
        assert bounded.exit_code == _Exit.DIFFERENT
        assert bounded.stdout == b"ove"
        assert bounded.stderr == b"e"
        assert bounded.stdout_truncated
        assert bounded.stderr_truncated

    asyncio.run(run())
