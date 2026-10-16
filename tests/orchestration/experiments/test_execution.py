# Copyright (c) 2026
# ruff: noqa: COM812, FBT001, TRY003, EM101, ANN401, PT011 -- deterministic transport and durable-state boundaries
"""Execution authority, unknown completion and observation-only recovery contracts."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from devtools.core.time import Duration
from devtools.orchestration.experiments import execution, receipts
from devtools.orchestration.experiments.__main__ import main
from devtools.orchestration.experiments.pipeline import (
    ExperimentExecutionPipeline,
    summary,
)
from devtools.resources.commands import Command, CommandResult
from devtools.resources.commands.events import CommandStderr, CommandStdout
from tests.orchestration.experiments.test_pipeline import pipeline


def prepared(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[ExperimentExecutionPipeline, Path]:
    """Provide immutable preparation without production grant construction."""
    subject = pipeline(tmp_path)
    monkeypatch.setattr(
        execution, "get_temp_dir", lambda: SimpleNamespace(value=tmp_path / "os-temp")
    )
    folder = subject.receipt_root / "preparation"
    folder.mkdir(parents=True)
    result = {
        "pipeline": "ExperimentExecutionPipeline",
        "version": "1",
        "attempt": "prep",
        "started": "2026-10-16T00:00:00+00:00",
        "target": str(subject.target),
        "python": str(subject.python),
        "plan": "plan.json",
        "plan_sha256": "sha",
        "target_head": "head",
        "target_git_directory": str(subject.target / ".git"),
        "validation": {
            "run_id": "run",
            "executable": {"sha256": "python-sha", "version": "python-version"},
        },
        "disposition": "READY_FOR_APPROVAL",
        "report": str(folder / "result.json"),
        "stages": [],
    }
    receipts.store(folder / "start.json", result)
    receipts.store(folder / "result.json", result)
    return subject, folder / "result.json"


def observations(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """Record actions and simulate externally authenticated admission."""
    actions: list[str] = []

    async def exchange(
        _pipeline: ExperimentExecutionPipeline,
        action: str,
        _request: Path,
        _observer: object = None,
    ) -> dict[str, Any]:
        actions.append(action)
        if callable(_observer):
            _observer({"status": "SYNTHETIC_OBSERVATION"})
        return (
            {
                "authorization": {"checkpoint": "approved"},
                "usage": {"status": "PARTIAL"},
            }
            if action == "admit"
            else {"status": "COMPLETE"}
        )

    monkeypatch.setattr(execution, "exchange", exchange)
    return actions


def test_execute_reconcile_and_duplicate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Dispatch once after admission and repeat only safe observation."""
    subject, _receipt = prepared(tmp_path, monkeypatch)
    actions = observations(monkeypatch)
    result = asyncio.run(subject.execute(Path("plan.json"), tmp_path / "work"))
    assert result["disposition"] == "COMPLETE"
    assert actions == ["admit", "dispatch"]
    assert result["preparation"]["sha256"]
    assert result["stages"]
    assert "maintainer review" in summary(result)
    for plan in (Path("plan.json"), None):
        reconciled = asyncio.run(subject.reconcile(plan))
        assert reconciled["disposition"] == "COMPLETE"
        assert (
            receipts.latest(subject.receipt_root, "plan.json")["observed_at"]
            == reconciled["observed_at"]
        )
    assert actions[-2:] == ["reconcile", "reconcile"]
    duplicate = asyncio.run(subject.execute(Path("plan.json"), tmp_path / "work"))
    assert duplicate["disposition"] == "ADMISSION_REFUSED"
    assert not duplicate["dispatch_requested"]


@pytest.mark.parametrize("phase", ["admit", "dispatch"])
@pytest.mark.parametrize("cancel", [False, True])
def test_unknown_dispatch_and_interruption(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, phase: str, cancel: bool
) -> None:
    """Preserve uncertain dispatch after lost transport."""
    subject, _receipt = prepared(tmp_path, monkeypatch)

    async def exchange(
        _pipeline: ExperimentExecutionPipeline,
        action: str,
        _request: Path,
        _observer: object = None,
    ) -> dict[str, Any]:
        if action == phase:
            if cancel:
                raise asyncio.CancelledError
            raise execution.TargetError("lost connection")
        return {"authorization": {"checkpoint": "approved"}, "usage": {}}

    monkeypatch.setattr(execution, "exchange", exchange)
    if cancel:
        with pytest.raises(asyncio.CancelledError):
            asyncio.run(subject.execute(Path("plan.json"), tmp_path / "work"))
    else:
        asyncio.run(subject.execute(Path("plan.json"), tmp_path / "work"))
    result = receipts.latest(subject.receipt_root)
    assert result["disposition"] == (
        "DISPATCH_COMPLETION_UNKNOWN"
        if phase == "dispatch"
        else "INTERRUPTED_BEFORE_DISPATCH"
        if cancel
        else "ADMISSION_REFUSED"
    )
    reconciled = asyncio.run(subject.reconcile(Path("plan.json")))
    assert reconciled["disposition"] in {
        "RECONCILIATION_REQUIRED",
        result["disposition"],
    }


def test_invalid_or_missing_preparation_and_retention(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Missing, foreign or non-ready preparation never reaches target authority."""
    subject, receipt_path = prepared(tmp_path, monkeypatch)
    actions = observations(monkeypatch)
    invalid = dict(receipts.restore(receipt_path), disposition="BUDGET_UNAVAILABLE")
    foreign = subject.receipt_root / "invalid.json"
    receipts.store(foreign, invalid)
    result = asyncio.run(
        subject.execute(Path("plan.json"), tmp_path / "work", preparation=foreign)
    )
    assert result["disposition"] == "ADMISSION_REFUSED"
    assert actions == []
    with pytest.raises(ValueError, match="No preparation"):
        asyncio.run(subject.execute(Path("other.json"), tmp_path / "work"))
    with pytest.raises(ValueError, match="unambiguous"):
        asyncio.run(subject.reconcile(Path("other.json")))
    monkeypatch.setattr(
        execution, "get_temp_dir", lambda: SimpleNamespace(value=tmp_path)
    )
    with pytest.raises(ValueError, match="persistent"):
        asyncio.run(subject.execute(Path("plan.json"), tmp_path / "work"))


def test_orphan_pipeline_intent_is_not_redispatched(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A crash after durable intent remains uncertain even without terminal receipt."""
    subject, receipt_path = prepared(tmp_path, monkeypatch)
    actions = observations(monkeypatch)
    result = asyncio.run(subject.execute(Path("plan.json"), tmp_path / "work"))
    folder = Path(result["report"]).parent
    (folder / "result.json").unlink()
    uncertain = receipts.latest(subject.receipt_root)
    assert uncertain["dispatch_requested"]
    assert uncertain["run_id"] == "run"
    assert uncertain["disposition"] == "INTERRUPTED_OR_IN_PROGRESS"
    refused = asyncio.run(
        subject.execute(Path("plan.json"), tmp_path / "work", preparation=receipt_path)
    )
    assert refused["disposition"] == "ADMISSION_REFUSED"
    assert actions == ["admit", "dispatch"]
    request_path = folder / "dispatch-request.json"
    request = receipts.restore(request_path)
    request["attempt"] = "other"
    request_path.unlink()
    receipts.store(request_path, request, schema=receipts.EXECUTION_SCHEMA)
    with pytest.raises(ValueError, match="identity"):
        receipts.history(subject.receipt_root)


@pytest.mark.parametrize("outcome", ["valid", "failed", "truncated", "malformed"])
def test_managed_transport(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, outcome: str
) -> None:
    """Stream existing structured controller events through the canonical handle."""
    subject, request_path = prepared(tmp_path, monkeypatch)

    class Handle:
        async def events(self) -> Any:
            yield CommandStdout(b"ignored as progress")
            yield CommandStderr(b'not json\n{"status":"STARTED"}\n')
            yield CommandStderr(b'{"status":"FINISHED"}\n')

        def __await__(self) -> Any:
            async def result() -> CommandResult:
                await asyncio.sleep(0)
                stdout = (
                    b"not json" if outcome == "malformed" else b'{"status":"COMPLETE"}'
                )
                return CommandResult(
                    Command("fake"),
                    1 if outcome == "failed" else 0,
                    stdout,
                    b"",
                    Duration.seconds(0),
                    stdout_truncated=outcome == "truncated",
                )

            return result().__await__()

    monkeypatch.setattr(subject.executor, "start", lambda _command: Handle())
    rows: list[dict[str, Any]] = []
    for action in ("admit", "dispatch"):
        if outcome == "valid":
            assert (
                asyncio.run(
                    execution.exchange(subject, action, request_path, rows.append)
                )["status"]
                == "COMPLETE"
            )
            assert (
                asyncio.run(execution.exchange(subject, action, request_path))["status"]
                == "COMPLETE"
            )
        else:
            with pytest.raises(ValueError):
                asyncio.run(execution.exchange(subject, action, request_path))
    if outcome == "valid":
        assert rows[0]["status"] == "STARTED"


def test_execution_cli(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """No approval flag is offered; execute requires persistent receipts/work root."""
    subject, _receipt = prepared(tmp_path, monkeypatch)
    observations(monkeypatch)
    monkeypatch.setattr(
        "devtools.orchestration.experiments.__main__.ExperimentExecutionPipeline",
        lambda *_args: subject,
    )
    base = [
        "experiment",
        "execute",
        "plan.json",
        "--target",
        str(subject.target),
        "--receipts",
        str(subject.receipt_root),
        "--work-root",
        str(tmp_path / "work"),
    ]
    monkeypatch.setattr(sys, "argv", base)
    assert main() == 0
    assert "COMPLETE" in capsys.readouterr().out
    for action in ("reconcile", "status"):
        args = [*base]
        args[1] = action
        monkeypatch.setattr(sys, "argv", [*args, "--json", "--refresh"])
        assert main() == 0
        assert json.loads(capsys.readouterr().out)["kind"] == "execution"
    monkeypatch.setattr(sys, "argv", base)
    assert main() == 1
    monkeypatch.setattr(sys, "argv", ["experiment", "execute", "plan.json"])
    with pytest.raises(SystemExit):
        main()


def test_incomplete_admission_and_active_integrity(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Missing admission evidence fails closed; corrupted reconciliation is refused."""
    subject, _receipt = prepared(tmp_path, monkeypatch)

    async def incomplete(*_args: object) -> dict[str, Any]:
        return {"authorization": {"checkpoint": "approved"}}

    monkeypatch.setattr(execution, "exchange", incomplete)
    result = asyncio.run(subject.execute(Path("plan.json"), tmp_path / "work"))
    assert result["disposition"] == "ADMISSION_REFUSED"
    with pytest.raises(ValueError, match="No matching"):
        receipts.latest(subject.receipt_root, active=True)
    folder = Path(result["report"]).parent
    result.update(target="foreign-target", observed_at="now")
    receipts.store(
        folder / "reconciliation-corrupt.json", result, schema=receipts.EXECUTION_SCHEMA
    )
    with pytest.raises(ValueError, match="Reconciliation/start"):
        receipts.history(subject.receipt_root)
