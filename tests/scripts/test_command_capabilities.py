# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- actual operational script adoption and safe projection
"""Real operator entry points delegate to framework capabilities without models."""

from __future__ import annotations

import asyncio
import json
import sys
from typing import TYPE_CHECKING, Any

import pytest

from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor
from devtools.tools.repository.validation import InspectAndValidateTool
from scripts import check_change, command_patterns
from tests.tools.repository.fixtures import MODULE, repository

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.tools.repository.validation import ChangeValidationReport


def test_real_check_cli_delegates_and_reports_literal_git(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    revision, _scope = asyncio.run(repository(tmp_path))
    entered = []
    actual = InspectAndValidateTool.execute

    async def observed(
        self: InspectAndValidateTool,
        arguments: None,
    ) -> ChangeValidationReport:
        entered.append(self.plan)
        return await actual(self, arguments)

    monkeypatch.setattr(InspectAndValidateTool, "execute", observed)
    argv = [
        str(tmp_path),
        "--revision",
        revision,
        "--run",
        "operator-1",
        "--check",
        "whitespace",
    ]
    for path in (MODULE, "readme.txt", "notes [new].txt"):
        argv += ["--allow", path]
    assert check_change.main(argv) == 0
    report = json.loads(capsys.readouterr().out)
    assert len(entered) == 1
    assert entered[0].checks.checks[0].command.argv == (
        "git",
        "diff",
        "--check",
        "HEAD",
    )
    assert report["status"] == "passed"
    assert report["revision"] == revision
    assert report["checks"][0]["exit_code"] == 0
    assert report["checks"][0]["inputs_current"] is None
    assert report["observed_commands"] == 11
    assert (
        check_change.main(
            [
                str(tmp_path),
                "--revision",
                revision,
                "--run",
                "operator-2",
                "--check",
                "whitespace",
            ],
        )
        == 1
    )
    assert json.loads(capsys.readouterr().out)["status"] == "refused"


def test_real_cli_unicode_output_is_portable(tmp_path: Path) -> None:
    root = tmp_path / "space \u03c0 & [project]"
    revision, _ = asyncio.run(repository(root))
    args = [
        str(check_change.__file__),
        str(root),
        "--revision",
        revision,
        "--run",
        "real-operator",
        "--check",
        "whitespace",
    ]
    for path in (MODULE, "readme.txt", "notes [new].txt"):
        args += ["--allow", path]
    result = asyncio.run(
        CommandExecutor().execute(
            Command(sys.executable)
            .args("-B", *args)
            .cwd(resolve_path(root))
            .with_timeout(Duration.seconds(15)),
        ),
    )
    assert result.exit_code == 0, result.stderr.decode()
    report = json.loads(result.stdout)
    assert report["status"] == "passed"
    assert MODULE in {c["path"] for c in report["changes"]}


@pytest.mark.parametrize("name", ["whitespace", "tests", "lint", "typing", "unknown"])
def test_operator_fixed_argv_selection(tmp_path: Path, name: str) -> None:
    if name == "unknown":
        with pytest.raises(ValueError, match="selection"):
            check_change.selected_checks(resolve_path(tmp_path), (name,))
    else:
        plan = check_change.selected_checks(resolve_path(tmp_path), (name,))
        command = plan.checks[0].command
        assert command.working_directory == resolve_path(tmp_path)
        assert command.timeout.total_seconds == 1800  # type: ignore[union-attr]
        assert command.executable == ("git" if name == "whitespace" else "uv")
        if name == "tests":
            assert command.arguments == (
                "run",
                "python",
                "scripts/validate_development.py",
            )


def test_cli_cannot_fall_back_to_private_procedure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = []

    async def unavailable(*_args: Any, **_kwargs: Any) -> Any:  # noqa: ANN401 -- explicit shared boundary fault
        calls.append("shared")
        msg = "shared procedure unavailable"
        raise OSError(msg)

    monkeypatch.setattr(InspectAndValidateTool, "execute", unavailable)
    with pytest.raises(OSError, match="shared procedure"):
        check_change.main(
            [
                str(tmp_path),
                "--revision",
                "0" * 40,
                "--run",
                "failure",
                "--check",
                "whitespace",
            ],
        )
    assert calls == ["shared"]


@pytest.mark.parametrize(
    "mode",
    ["valid", "partial", "malformed", "line-limit", "record-limit", "byte-limit"],
)
def test_explicit_codex_fixture_analysis_without_private_output(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    mode: str,
) -> None:
    record = json.dumps(
        {
            "type": "item.completed",
            "item": {
                "type": "command_execution",
                "id": "item_1",
                "command": "git status --porcelain=v1 -z",
                "exit_code": 0,
                "status": "completed",
                "aggregated_output": "PRIVATE_SENTINEL",
            },
        },
    ).encode()
    data = record + b'\n{"type":"turn.completed"}\n'
    if mode == "partial":
        data = record
    elif mode == "malformed":
        data = record + b"\nPRIVATE_SENTINEL broken\n"
    elif mode == "line-limit":
        data = b"x" * 65537
    elif mode == "record-limit":
        data = b'{"type":"turn.started"}\n' * 4097
    elif mode == "byte-limit":
        data = b"x" * ((4 << 20) + 1)
    path = tmp_path / "authored-events.jsonl"
    path.write_bytes(data)
    args = [str(path), "--agent", "codex-fixture", "--task", "task", "--run", "run"]
    if mode == "byte-limit":
        with pytest.raises(ValueError, match="bound"):
            command_patterns.main(args)
        return
    assert command_patterns.main(args) == int(
        mode in {"malformed", "line-limit", "record-limit"},
    )
    text = capsys.readouterr().out
    assert "PRIVATE_SENTINEL" not in text
    result = json.loads(text)
    if mode in {"valid", "partial", "malformed"}:
        assert result["patterns"][0]["frequency"] == 1
        assert result["patterns"][0]["pattern"]["family"] == "git"
        assert (
            result["patterns"][0]["pattern"]["equivalent_tool"]
            == "tools.repository.GitInspectionTool"
        )
