# Copyright (c) 2026
# ruff: noqa: PLR2004, PLR0913, PLR0917, FBT001, SLF001, COM812 -- isolated preparation boundary fixtures
"""Preparation never confers authority, loses unknowns or retries science."""

from __future__ import annotations

import asyncio
import json
import runpy
import sys
from pathlib import Path
from typing import Any

import pytest

from devtools.core.time import Duration
from devtools.orchestration.experiments import ExperimentExecutionPipeline, receipts
from devtools.orchestration.experiments.__main__ import main
from devtools.orchestration.experiments.pipeline import (
    PreparationError,
    summary,
    target_python,
)
from devtools.resources.commands import Command, CommandResult
from devtools.resources.commands.errors import CommandTimeoutError


def pipeline(tmp_path: Path) -> ExperimentExecutionPipeline:
    """Bind harmless independent roots and an existing local interpreter."""
    target = tmp_path / "target"
    target.mkdir()
    (target / "plan.json").write_bytes(b'{"frozen":true}\r\n')
    return ExperimentExecutionPipeline(
        target,
        tmp_path / "receipts",
        Path(sys.executable),
    )


def successful_stages(
    monkeypatch: pytest.MonkeyPatch,
    subject: ExperimentExecutionPipeline,
    *,
    usage: str = "PARTIAL",
    budget: str = "BUDGET_CHECK_PASS",
) -> None:
    """Replace only target observations; production persistence stays real."""

    async def git(*_args: str) -> str:
        return "head"

    async def stage(name: str, *_args: str) -> dict[str, Any]:
        return {
            "validation": {"status": "PLAN_VALID", "name": "Synthetic purpose"},
            "usage": {"status": usage},
            "budget": {"status": budget},
        }[name]

    monkeypatch.setattr(subject, "_git", git)
    monkeypatch.setattr(subject, "_stage", stage)


@pytest.mark.parametrize(
    ("usage", "budget", "expected"),
    [
        ("PARTIAL", "BUDGET_CHECK_PASS", "READY_FOR_APPROVAL"),
        ("UNAVAILABLE", "BUDGET_CHECK_PASS", "EVIDENCE_UNAVAILABLE"),
        ("PARTIAL", "UNAVAILABLE", "BUDGET_UNAVAILABLE"),
        ("PARTIAL", "UNSET", "BUDGET_UNAVAILABLE"),
    ],
)
def test_repeat_and_history(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    usage: str,
    budget: str,
    expected: str,
) -> None:
    """Repeated observations have distinct immutable identities and no authority."""
    subject = pipeline(tmp_path)
    successful_stages(monkeypatch, subject, usage=usage, budget=budget)
    one = asyncio.run(subject.prepare(Path("plan.json")))
    two = asyncio.run(subject.prepare(Path("plan.json")))
    assert one["disposition"] == expected
    assert two["attempt"] != one["attempt"]
    assert one["execution_authorized"] == "NO"
    assert one["scientific_dispatches"] == 0
    assert receipts.latest(subject.receipt_root, "plan.json") == two
    assert len(receipts.history(subject.receipt_root)) == 2
    assert not receipts.history(subject.receipt_root, "other.json")
    assert "AUTHORIZED=NO" in summary(one)
    assert "UNKNOWN" in summary(one)
    assert hasattr(subject, "execute")
    assert not hasattr(subject, "approve")
    assert list(subject.target.iterdir()) == [subject.target / "plan.json"]


@pytest.mark.parametrize(
    "failure",
    [
        ValueError("broken"),
        CommandTimeoutError("timeout"),
        PreparationError("STARTUP_PREFLIGHT_FAILED", {"error": "startup"}),
    ],
)
def test_failed_stage(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure: Exception,
) -> None:
    """Failures retain diagnostics, elapsed timing and an immutable terminal record."""
    subject = pipeline(tmp_path)
    successful_stages(monkeypatch, subject)

    async def stage(*_args: str) -> dict[str, Any]:
        raise failure

    monkeypatch.setattr(subject, "_stage", stage)
    result = asyncio.run(subject.prepare(Path("plan.json")))
    assert result["disposition"] in {"PREPARATION_FAILED", "STARTUP_PREFLIGHT_FAILED"}
    assert result["failed_stage"] == "validation"
    evidence = receipts.restore(Path(result["report"]).with_name("validation.json"))
    assert evidence["elapsed_seconds"] >= 0
    assert evidence["evidence"]
    assert receipts.latest(subject.receipt_root) == result


def test_interrupted(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Cancellation propagates after persisting an INTERRUPTED preparation."""
    subject = pipeline(tmp_path)
    successful_stages(monkeypatch, subject)

    async def stage(*_args: str) -> dict[str, Any]:
        raise asyncio.CancelledError

    monkeypatch.setattr(subject, "_stage", stage)
    with pytest.raises(asyncio.CancelledError):
        asyncio.run(subject.prepare(Path("plan.json")))
    assert receipts.latest(subject.receipt_root)["disposition"] == "INTERRUPTED"


def test_identity_and_target_movement(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A changing checkout and plans outside the target never yield readiness."""
    subject = pipeline(tmp_path)
    successful_stages(monkeypatch, subject)
    values = iter(["head", "git-dir", "changed"])

    async def git(*_args: str) -> str:
        return next(values)

    monkeypatch.setattr(subject, "_git", git)
    assert (
        asyncio.run(subject.prepare(Path("plan.json")))["disposition"]
        == "PLAN_INVALID_OR_INCOMPATIBLE"
    )
    assert (
        asyncio.run(subject.prepare(tmp_path / "outside.json"))["disposition"]
        == "PREPARATION_FAILED"
    )
    with pytest.raises(ValueError, match="outside"):
        ExperimentExecutionPipeline(
            subject.target,
            subject.target / "receipts",
            Path(sys.executable),
        )
    assert target_python(subject.target).is_relative_to(subject.target / ".venv")


@pytest.mark.parametrize(
    ("stdout", "code", "truncated", "expected"),
    [
        (b'{"status":"PASS"}', 0, False, None),
        (b"{}", 0, True, "EVIDENCE_UNAVAILABLE"),
        (b"not json", 0, False, "EVIDENCE_UNAVAILABLE"),
        (b'{"error":"worker startup failed"}', 1, False, "STARTUP_PREFLIGHT_FAILED"),
        (b'{"error":"BUDGET_BLOCKED"}', 1, False, "BUDGET_REJECTED"),
        (b'{"error":"identity differs"}', 1, False, "PLAN_INVALID_OR_INCOMPATIBLE"),
        (b"{}", 1, False, "PLAN_INVALID_OR_INCOMPATIBLE"),
    ],
)
def test_command_transport(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    stdout: bytes,
    code: int,
    truncated: bool,
    expected: str | None,
) -> None:
    """Bounded managed subprocess transport preserves failure distinctions."""
    subject = pipeline(tmp_path)

    async def execute(command: Command) -> CommandResult:
        assert command.working_directory is not None
        return CommandResult(
            command,
            code,
            stdout,
            b"diagnostic",
            Duration.seconds(0),
            stdout_truncated=truncated,
        )

    monkeypatch.setattr(subject.executor, "execute", execute)
    if expected:
        with pytest.raises(PreparationError) as error:
            asyncio.run(subject._stage("validation", "plan.json", "head", "digest"))
        assert error.value.disposition == expected
    else:
        assert asyncio.run(
            subject._stage("validation", "plan.json", "head", "digest"),
        ) == {"status": "PASS"}
        assert asyncio.run(subject._git("rev-parse", "HEAD"))
    if code or truncated:
        with pytest.raises(PreparationError):
            asyncio.run(subject._git("rev-parse", "HEAD"))


def test_receipt_integrity_and_incomplete(tmp_path: Path) -> None:
    """Incomplete, ambiguous, changed and overwritten receipts remain explicit."""
    root = tmp_path / "receipts"
    root.mkdir()
    with pytest.raises(ValueError, match="No matching"):
        receipts.latest(root)
    one = root / "one"
    one.mkdir()
    value = {
        "started": "now",
        "attempt": "one",
        "target": "target",
        "plan": "plan.json",
        "plan_sha256": "sha",
    }
    receipts.store(one / "start.json", value)
    assert receipts.latest(root)["disposition"] == "INTERRUPTED_OR_IN_PROGRESS"
    with pytest.raises(FileExistsError):
        receipts.store(one / "start.json", value)
    two = root / "two"
    two.mkdir()
    receipts.store(two / "start.json", {**value, "attempt": "two", "target": "other"})
    with pytest.raises(ValueError, match="Ambiguous"):
        receipts.latest(root)
    receipts.store(one / "validation.json", {"observed": True})
    receipts.store(
        one / "result.json",
        {**value, "stages": [{"name": "validation", "sha256": "incorrect"}]},
    )
    with pytest.raises(ValueError, match="reference"):
        receipts.history(root)
    envelope = json.loads((one / "start.json").read_text())
    envelope["sha256"] = "changed"
    (one / "start.json").write_text(json.dumps(envelope))
    with pytest.raises(ValueError, match="integrity/schema"):
        receipts.restore(one / "start.json")


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("usage", "EVIDENCE_UNAVAILABLE"),
        ("budget", "BUDGET_UNAVAILABLE"),
    ],
)
def test_unavailable_stage_evidence(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, name: str, expected: str
) -> None:
    """Unavailable evidence is distinct from invalid scientific configuration."""
    subject = pipeline(tmp_path)

    async def execute(command: Command) -> CommandResult:
        return CommandResult(
            command, 1, b'{"error":"missing evidence"}', b"", Duration.seconds(0)
        )

    monkeypatch.setattr(subject.executor, "execute", execute)
    with pytest.raises(PreparationError) as error:
        asyncio.run(subject._stage(name, "plan.json", "head", "digest"))
    assert error.value.disposition == expected


def test_cli(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The operator can prepare, inspect latest and find history using a plan."""
    subject = pipeline(tmp_path)
    successful_stages(monkeypatch, subject)
    monkeypatch.setattr(
        "devtools.orchestration.experiments.__main__.ExperimentExecutionPipeline",
        lambda *_args: subject,
    )
    argv = [
        "experiment",
        "prepare",
        "plan.json",
        "--target",
        str(subject.target),
        "--receipts",
        str(subject.receipt_root),
    ]
    monkeypatch.setattr(sys, "argv", argv)
    assert main() == 0
    assert "READY_FOR_APPROVAL" in capsys.readouterr().out
    monkeypatch.setattr(sys, "argv", [*argv, "--json", "--python", sys.executable])
    assert main() == 0
    assert json.loads(capsys.readouterr().out)["execution_authorized"] == "NO"
    successful_stages(monkeypatch, subject, budget="UNSET")
    assert main() == 1
    capsys.readouterr()
    for command in ("status", "history"):
        for output in ([], ["--json"]):
            monkeypatch.setattr(
                sys,
                "argv",
                [
                    "experiment",
                    command,
                    "plan.json",
                    "--receipts",
                    str(subject.receipt_root),
                    *output,
                ],
            )
            assert main() == 0
            rendered = capsys.readouterr().out
            assert rendered
            if command == "history" and not output:
                assert "BUDGET_UNAVAILABLE" in rendered
                assert "report=" in rendered
                assert len(rendered.splitlines()) == 3
    monkeypatch.setattr(
        sys,
        "argv",
        ["experiment", "history", "--receipts", str(subject.receipt_root)],
    )
    assert main() == 0
    capsys.readouterr()
    monkeypatch.setattr(sys, "argv", ["experiment", "prepare"])
    with pytest.raises(SystemExit):
        main()


def test_module_entrypoint(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The installed module exposes the same status/history command."""
    monkeypatch.setattr(
        sys, "argv", ["experiment", "history", "--receipts", str(tmp_path)]
    )
    with pytest.raises(SystemExit) as error:
        runpy.run_module(
            "devtools.orchestration.experiments.__main__", run_name="__main__"
        )
    assert error.value.code == 0


def test_summary_accounting_categories() -> None:
    """Keep the forecast, model inventory and observed categories distinct."""
    text = summary(
        {
            "disposition": "READY_FOR_APPROVAL",
            "plan": "plan.json",
            "plan_sha256": "sha",
            "target": "target",
            "target_head": "head",
            "report": "result.json",
            "approval": "REQUIRED",
            "validation": {
                "name": "Synthetic purpose",
                "models": {"model_id": "fake", "reasoning": "high"},
                "economics": {
                    "calls": [{"model": "fake", "reasoning_effort": "high"}],
                    "input_range": [10, 20],
                    "output_range": [0, 5],
                },
            },
            "usage": {"status": "UNAVAILABLE", "observation": None},
        }
    )
    assert "fake" in text
    assert '"fresh_invocations": null' in text
    assert "NOT account-wide" in text
