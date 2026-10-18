# Copyright (c) 2026
# ruff: noqa: COM812 -- fixed command-gate boundary tests
"""Verify shipped validation dispatch rather than the Git fixture's substitute."""

from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING, Any

import pytest

from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor, CommandResult
from scripts.backlog.integration.validation import validate_tree

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize("failure", [False, True])
def test_fixed_validation_and_failure_stop(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *, failure: bool
) -> None:
    """The actual gate invokes oracle/tests/static/protected, stopping on failure."""
    calls: list[Command] = []

    async def execute(_self: CommandExecutor, command: Command) -> CommandResult:
        calls.append(command)
        return CommandResult(
            command, int(failure), b"gate output\xff\n", b"", Duration.seconds(0)
        )

    monkeypatch.setattr(CommandExecutor, "execute", execute)
    plan: dict[str, Any] = {
        "source": "src/devtools/example.py",
        "tests": ["tests/test_example.py"],
        "files": [{"path": "src/devtools/example.py"}],
        "validation_seconds": 10,
    }
    report = asyncio.run(
        validate_tree(tmp_path, tmp_path / "pre", plan, "assert True\n", post=False)
    )
    assert report["passed"] is not failure
    assert len(calls) == (1 if failure else 6)
    if not failure:
        assert calls[-1].arguments == ("-I", "-B", str(tmp_path / "pre/protected.py"))
        assert "validate_development.py" in (tmp_path / "pre/protected.py").read_text()
        assert calls[2].arguments[:3] == ("-m", "ruff", "check")
    assert (
        json.loads((tmp_path / "pre/progress.json").read_text())["passed"]
        is not failure
    )
    assert (tmp_path / "pre/oracle-stdout.txt").read_bytes() == b"gate output\xff\n"
    assert "module.__file__" in (tmp_path / "pre/oracle.py").read_text()
    calls.clear()
    asyncio.run(
        validate_tree(tmp_path, tmp_path / "post", plan, "assert True\n", post=True)
    )
    assert len(calls) == (1 if failure else 2)


def test_protected_subprocess_uses_target_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Actually execute the target gate with an independently selected source tree."""
    package = tmp_path / "src/devtools"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "example.py").write_text("VALUE = 'candidate'\n")
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    (scripts / "validate_development.py").write_text(
        "from devtools.example import VALUE\nassert VALUE == 'candidate'\n"
        "print('TARGET_GATE_PASS')\n"
    )
    original = CommandExecutor.execute

    async def execute(owner: CommandExecutor, command: Command) -> CommandResult:
        if command.arguments[-1].endswith("protected.py"):
            return await original(owner, command)
        return CommandResult(command, 0, b"", b"", Duration.seconds(0))

    monkeypatch.setattr(CommandExecutor, "execute", execute)
    plan: dict[str, Any] = {
        "source": "src/devtools/example.py",
        "tests": ["tests/test_example.py"],
        "files": [{"path": "src/devtools/example.py"}],
        "validation_seconds": 10,
    }
    report = asyncio.run(
        validate_tree(
            tmp_path, tmp_path / "evidence", plan, "assert True\n", post=False
        )
    )
    assert report["passed"]
    assert report["checks"][-1]["stdout"].splitlines() == ["TARGET_GATE_PASS"]
