# Copyright (c) 2026
"""Independent regression of per-command environment values and child delivery."""

from __future__ import annotations

import asyncio
import json
import os
import sys
from collections import UserDict
from dataclasses import FrozenInstanceError
from pathlib import Path
from typing import TYPE_CHECKING, cast

import pytest

from devtools.core.paths import ResolvedPath
from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor

if TYPE_CHECKING:
    from collections.abc import Mapping, MutableMapping


def test_environment_is_snapshotted_read_only_and_order_independent() -> None:
    """Accepted Mapping inputs cannot mutate the command's immutable value."""
    supplied = UserDict({"ONE": "one", "EMPTY": ""})
    command = Command(sys.executable, environment=supplied)
    supplied["ONE"] = "changed"
    assert command.environment == {"ONE": "one", "EMPTY": ""}
    assert command == Command(sys.executable, environment={"EMPTY": "", "ONE": "one"})
    assert hash(command) == hash(
        Command(sys.executable, environment={"EMPTY": "", "ONE": "one"}),
    )
    assert command != Command(sys.executable, environment={"ONE": "different"})
    with pytest.raises(TypeError):
        cast("MutableMapping[str, str]", command.environment)["ONE"] = "changed"
    attribute = "environment"
    with pytest.raises(FrozenInstanceError):
        setattr(command, attribute, {})
    assert Command(sys.executable).environment is None
    assert hash(Command(sys.executable)) == hash(Command(sys.executable))


@pytest.mark.parametrize(
    "value",
    [[], "ONE=one", 1, False, {1: "x"}, {"ONE": 1}, {"ONE": None}],
)
def test_environment_rejects_nonmapping_or_nonstring_values(value: object) -> None:
    """Both construction and replacement validate the public string mapping."""
    invalid = cast("Mapping[str, str]", value)
    with pytest.raises(TypeError):
        Command(sys.executable, environment=invalid)
    with pytest.raises(TypeError):
        Command(sys.executable).with_environment(invalid)


@pytest.mark.parametrize(
    "value",
    [{"": "x"}, {"a=b": "x"}, {"a\0b": "x"}, {"a": "x\0y"}],
)
def test_environment_rejects_invalid_os_names_and_values(value: dict[str, str]) -> None:
    """Invalid data refuses before launching a child or replacing a valid value."""
    original = Command(sys.executable, environment={"OK": "value"})
    with pytest.raises(ValueError):  # noqa: PT011 -- public exception type, no wording contract
        Command(sys.executable, environment=value)
    with pytest.raises(ValueError):  # noqa: PT011 -- public exception type, no wording contract
        original.with_environment(value)
    assert original.environment == {"OK": "value"}


def test_environment_and_stdin_survive_other_fluent_operations(tmp_path: Path) -> None:
    """Independent command dimensions remain intact during immutable replacement."""
    command = Command(sys.executable, stdin=b"binary\0", environment={"KEY": "value"})
    for changed in (
        command.args("-V"),
        command.with_args("-V"),
        command.without_args(),
        command.with_executable(sys.executable),
        command.cwd(ResolvedPath(tmp_path)),
        command.without_cwd(),
        command.with_timeout(Duration.seconds(3)),
        command.without_timeout(),
        command.with_stdin(b"replacement"),
        command.without_stdin(),
    ):
        assert changed.environment == command.environment
    assert command.with_environment({"NEW": "value"}).stdin == command.stdin
    assert command.without_environment().stdin == command.stdin
    assert command.with_environment({"NEW": "value"}).environment == {"NEW": "value"}
    assert command.without_environment().environment is None


def test_real_children_use_launch_time_inheritance_and_isolated_overrides(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Concurrent child processes get exact overlays without parent mutation."""
    monkeypatch.setenv("DEVTOOLS_ENV12_ONE", "parent")
    monkeypatch.setenv("DEVTOOLS_ENV12_INHERITED", "before")
    monkeypatch.setenv("DEVTOOLS_ENV12_EMPTY", "parent")
    script = (
        "import os,json; print(json.dumps([os.environ.get(k) for k in "
        "['DEVTOOLS_ENV12_ONE','DEVTOOLS_ENV12_INHERITED','DEVTOOLS_ENV12_EMPTY']])); "
        "print(os.getcwd())"
    )
    command = Command(
        sys.executable,
        ("-c", script),
        working_directory=ResolvedPath(tmp_path),
        timeout=Duration.seconds(8),
        environment={"DEVTOOLS_ENV12_ONE": "λ", "DEVTOOLS_ENV12_EMPTY": ""},
    )
    monkeypatch.setenv("DEVTOOLS_ENV12_INHERITED", "launch")
    before = dict(os.environ)

    async def run() -> None:
        commands = (
            command,
            command.with_environment({"DEVTOOLS_ENV12_ONE": "sibling"}),
            command.without_environment(),
            command.with_environment({}),
        )
        results = await asyncio.gather(
            *(CommandExecutor().execute(c) for c in commands),
        )
        expected = (
            ["λ", "launch", ""],
            ["sibling", "launch", "parent"],
            ["parent", "launch", "parent"],
            ["parent", "launch", "parent"],
        )
        for result, values, original in zip(results, expected, commands, strict=True):
            assert result.succeeded
            assert result.stderr == b""
            values_line, directory = result.stdout.decode().splitlines()
            assert json.loads(values_line) == values
            assert Path(directory) == tmp_path
            assert result.command is original

    asyncio.run(run())
    assert dict(os.environ) == before


def test_environment_and_binary_stdin_are_delivered_together() -> None:
    """A child can consume both independently configured input resources."""
    command = Command(
        sys.executable,
        (
            "-c",
            (
                "import sys,os; sys.stdout.buffer.write("
                "os.environ['DEVTOOLS_ENV12_COMBINED'].encode()+b':'+"
                "sys.stdin.buffer.read())"
            ),
        ),
        stdin=b"\0\xff\r\n",
        environment={"DEVTOOLS_ENV12_COMBINED": "λ"},
        timeout=Duration.seconds(8),
    )
    result = asyncio.run(CommandExecutor().execute(command))
    assert result.succeeded
    assert result.stderr == b""
    assert result.stdout == "λ:".encode() + b"\0\xff\r\n"
