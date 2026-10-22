# Copyright (c) 2026
"""Independent regressions for the reconciled CommandOutputPolicy contract."""

from __future__ import annotations

import asyncio
import sys
from dataclasses import FrozenInstanceError, replace
from decimal import Decimal
from enum import IntEnum
from fractions import Fraction
from typing import cast

import pytest

from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor, CommandOutputPolicy
from devtools.tools import ToolRunner
from devtools.tools.command import CommandTool

FIELDS = ("max_stdout_bytes", "max_stderr_bytes", "max_pending_events")


class _Count(IntEnum):
    TWO = 2


class _IndexOnly:
    def __index__(self) -> int:
        return 2


@pytest.mark.parametrize("field", FIELDS)
@pytest.mark.parametrize(
    "value",
    [
        True,
        False,
        0.0,
        1.0,
        1.5,
        -0.5,
        float("nan"),
        float("inf"),
        "5",
        None,
        b"5",
        [],
        {},
        Decimal(2),
        Fraction(2, 1),
        _IndexOnly(),
    ],
)
def test_invalid_types_fail_before_coercion_or_value_comparison(
    field: str,
    value: object,
) -> None:
    """Both construction and replacement reject wrong types with exact TypeError."""
    invalid = {field: cast("int", value)}
    with pytest.raises(TypeError) as direct:
        CommandOutputPolicy(**invalid)
    assert type(direct.value) is TypeError
    original = CommandOutputPolicy()
    with pytest.raises(TypeError) as replaced:
        replace(original, **invalid)
    assert type(replaced.value) is TypeError
    assert original == CommandOutputPolicy()


@pytest.mark.parametrize(
    ("field", "value", "word"),
    [
        ("max_stdout_bytes", -1, "stdout"),
        ("max_stderr_bytes", -1, "stderr"),
        ("max_pending_events", 0, "pending events"),
        ("max_pending_events", -1, "pending events"),
    ],
)
def test_integer_range_errors_retain_public_value_error(
    field: str,
    value: int,
    word: str,
) -> None:
    """Wrong integer values keep existing exceptions and field diagnostics."""
    with pytest.raises(ValueError, match=word) as caught:
        CommandOutputPolicy(**{field: value})
    assert type(caught.value) is ValueError


@pytest.mark.parametrize("value", [1, 1024, 10**100, _Count.TWO])
def test_integers_preserve_identity_and_immutable_value_semantics(value: int) -> None:
    """Valid integers are not narrowed, coerced or assigned an arbitrary ceiling."""
    policy = CommandOutputPolicy(value, value, value)
    assert all(getattr(policy, field) is value for field in FIELDS)
    equal = CommandOutputPolicy(value, value, value)
    assert policy == equal
    assert hash(policy) == hash(equal)
    assert not hasattr(policy, "__dict__")
    attribute = "max_stdout_bytes"
    with pytest.raises(FrozenInstanceError):
        setattr(policy, attribute, 0)
    assert replace(policy, max_stdout_bytes=0) == CommandOutputPolicy(0, value, value)


def test_defaults_and_zero_retention_remain_compatible() -> None:
    """Zero output retention is valid while pending-event buffering stays positive."""
    assert CommandOutputPolicy() == CommandOutputPolicy(1_048_576, 1_048_576, 1_024)
    assert CommandOutputPolicy(0, 0, 1).max_stdout_bytes == 0


@pytest.mark.parametrize(
    ("stdout_limit", "stderr_limit", "stdout", "stderr"),
    [(0, 0, b"", b""), (3, 2, b"pay", b"er"), (32, 32, b"payload!", b"error")],
)
def test_valid_policy_preserves_real_child_and_tool_compatibility(
    stdout_limit: int,
    stderr_limit: int,
    stdout: bytes,
    stderr: bytes,
) -> None:
    """Bounds still reach actual output retention without changing other dimensions."""
    command = Command(
        sys.executable,
        (
            "-c",
            (
                "import os,sys; "
                "sys.stdout.buffer.write(sys.stdin.buffer.read()+"
                "os.environ['DEVTOOLS_OUTPUT15'].encode()); "
                "sys.stderr.buffer.write(b'error'); sys.exit(1)"
            ),
        ),
        stdin=b"payload",
        environment={"DEVTOOLS_OUTPUT15": "!"},
        timeout=Duration.seconds(8),
    ).with_success_exit_codes(1)
    executor = CommandExecutor(
        output_policy=CommandOutputPolicy(stdout_limit, stderr_limit, 1),
    )
    result = asyncio.run(ToolRunner().execute(CommandTool(executor), command))
    assert result.command is command
    assert result.succeeded
    assert result.exit_code == 1
    assert result.stdout == stdout
    assert result.stderr == stderr
    assert result.stdout_truncated is (stdout_limit < len(b"payload!"))
    assert result.stderr_truncated is (stderr_limit < len(b"error"))
