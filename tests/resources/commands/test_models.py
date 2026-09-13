# Copyright (c) 2026
"""Tests for public command value objects."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from typing import TYPE_CHECKING

import pytest

from devtools.core.paths import ResolvedPath
from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandOutputPolicy, CommandResult

if TYPE_CHECKING:
    from pathlib import Path


def test_command_preserves_separate_executable_arguments_and_options(
    tmp_path: Path,
) -> None:
    """Commands retain structured process arguments and optional execution data."""
    command = Command(
        executable="python",
        arguments=("-c", "print('hello')"),
        working_directory=ResolvedPath(tmp_path),
        timeout=Duration.seconds(3),
    )

    assert command.executable == "python"
    assert command.arguments == ("-c", "print('hello')")
    assert command.working_directory == ResolvedPath(tmp_path)
    assert command.timeout == Duration.seconds(3)
    assert command.argv == ("python", "-c", "print('hello')")


def test_command_defaults_to_no_arguments_and_is_immutable() -> None:
    """Commands have an empty argument tuple and frozen value semantics."""
    command = Command("python")
    attribute = "executable"

    assert command.arguments == ()
    assert command == Command("python")
    assert hash(command) == hash(Command("python"))

    with pytest.raises(FrozenInstanceError):
        setattr(command, attribute, "other")


def test_command_fluent_methods_are_immutable_and_composable(tmp_path: Path) -> None:
    """Fluent command methods preserve unrelated immutable specification data."""
    original = (
        Command("python", ("-m",))
        .cwd(ResolvedPath(tmp_path))
        .with_timeout(Duration.seconds(1))
    )
    appended = original.args("pytest", "-q")
    replaced = appended.with_args("-c", "pass")
    cleared = replaced.without_args()
    renamed = cleared.with_executable("python3")
    without_cwd = renamed.without_cwd()
    without_timeout = without_cwd.without_timeout()

    assert original == Command(
        "python",
        ("-m",),
        ResolvedPath(tmp_path),
        Duration.seconds(1),
    )
    assert appended.arguments == ("-m", "pytest", "-q")
    assert replaced.arguments == ("-c", "pass")
    assert cleared.arguments == ()
    assert cleared.working_directory == ResolvedPath(tmp_path)
    assert cleared.timeout == Duration.seconds(1)
    assert renamed.executable == "python3"
    assert renamed.working_directory == ResolvedPath(tmp_path)
    assert renamed.timeout == Duration.seconds(1)
    assert without_cwd.working_directory is None
    assert without_cwd.timeout == Duration.seconds(1)
    assert without_timeout.timeout is None
    assert without_timeout.executable == "python3"

    with pytest.raises(ValueError, match="cannot be empty"):
        renamed.with_executable("   ")


@pytest.mark.parametrize("executable", ["", "   "])
def test_command_rejects_blank_executables(executable: str) -> None:
    """Commands require a non-blank executable representation."""
    with pytest.raises(ValueError, match="cannot be empty"):
        Command(executable)


def test_command_result_preserves_bytes_and_exit_status() -> None:
    """Nonzero exit codes remain ordinary completed command results."""
    command = Command("python")
    expected_exit_code = 3
    successful = CommandResult(command, 0, b"out", b"", Duration.seconds(1))
    failed = CommandResult(
        command,
        expected_exit_code,
        b"",
        b"error",
        Duration.seconds(2),
    )

    assert successful.command is command
    assert successful.stdout == b"out"
    assert successful.stderr == b""
    assert successful.duration == Duration.seconds(1)
    assert successful.stdout_truncated is False
    assert successful.stderr_truncated is False
    assert successful.events_dropped == 0
    assert successful.succeeded is True
    assert successful.failed is False
    assert failed.exit_code == expected_exit_code
    assert failed.stdout == b""
    assert failed.stderr == b"error"
    assert failed.succeeded is False
    assert failed.failed is True


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("max_stdout_bytes", -1, "stdout"),
        ("max_stderr_bytes", -1, "stderr"),
        ("max_pending_events", 0, "pending events"),
    ],
)
def test_command_output_policy_rejects_invalid_bounds(
    field: str,
    value: int,
    match: str,
) -> None:
    """Output limits reject values that cannot form bounded policies."""
    with pytest.raises(ValueError, match=match):
        CommandOutputPolicy(**{field: value})


def test_command_output_policy_exposes_default_bounds() -> None:
    """Default output limits are positive and practical for ordinary commands."""
    policy = CommandOutputPolicy()

    assert policy.max_stdout_bytes > 0
    assert policy.max_stderr_bytes > 0
    assert policy.max_pending_events > 0
