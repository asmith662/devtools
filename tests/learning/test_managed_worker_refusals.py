# Copyright (c) 2026
"""Host pre-entry bounds and explicit command-result fault controls."""

from __future__ import annotations

import asyncio
import importlib.metadata
import json
import sys
from typing import TYPE_CHECKING

import pytest

from devtools.core.time import Duration
from devtools.learning.investigation.classification.contracts import (
    ExecutionAuthorization,
)
from devtools.learning.investigation.errors import LearningUnavailableError
from devtools.learning.measurement.contracts import EvidenceReference
from devtools.resources.commands import Command, CommandExecutor, CommandResult
from devtools.tools.learning import ManagedLearningWorker, execution
from tests.learning.fixtures import authored_task

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize("fault", ["interpreter", "dependency"])
def test_current_worker_requires_qualified_interpreter_and_optional_distribution(
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
) -> None:
    """Simulate unavailable runtime metadata without changing the real environment."""
    if fault == "interpreter":
        monkeypatch.setattr(sys, "_base_executable", None)
        error: type[Exception] = ValueError
    else:

        def absent(_: str) -> None:
            raise importlib.metadata.PackageNotFoundError

        monkeypatch.setattr(importlib.metadata, "distribution", absent)
        error = LearningUnavailableError
    with pytest.raises(error, match=r"CPython|optional"):
        ManagedLearningWorker.current()


@pytest.mark.parametrize("fault", ["packet", "timeout"])
def test_host_preentry_limits_do_not_create_an_operation_root(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
) -> None:
    """Refusal happens before command construction, file effects or native entry."""
    plan = authored_task("regression").plan("mean", "online", "bound-control")
    grant = ExecutionAuthorization(
        plan.identity,
        (plan.method,),
        EvidenceReference("learning_execution_grant-v1", "unit", plan.identity),
    )
    timeout = Duration.seconds(301 if fault == "timeout" else 300)
    if fault == "packet":
        monkeypatch.setattr(execution, "MAX_PACKET_BYTES", 1)
    with pytest.raises(ValueError, match=r"pre-entry|timeout"):
        asyncio.run(
            ManagedLearningWorker.current().execute(
                plan,
                grant,
                tmp_path / "refused",
                operation_limit=timeout,
            ),
        )
    assert not tuple(tmp_path.iterdir())


@pytest.mark.parametrize("fault", ["exit", "truncated", "foreign", "shape", "type"])
def test_failed_or_foreign_command_reports_are_retained_without_retry(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
) -> None:
    """The command-result stand-in creates no process or scientific measurement."""
    plan = authored_task("regression").plan("mean", "online", "report-control")
    grant = ExecutionAuthorization(
        plan.identity,
        (plan.method,),
        EvidenceReference("learning_execution_grant-v1", "unit", plan.identity),
    )
    calls: list[Command] = []

    async def reported(_owner: CommandExecutor, command: Command) -> CommandResult:
        calls.append(command)
        value: object = {
            "generation_id": "authored",
            "manifest_sha256": "0" * 64,
            "plan_identity": "foreign" if fault == "foreign" else plan.identity,
        }
        if fault == "shape":
            value = []
        elif fault == "type":
            value = {
                "generation_id": 3,
                "manifest_sha256": "0" * 64,
                "plan_identity": plan.identity,
            }
        return CommandResult(
            command,
            1 if fault == "exit" else 0,
            json.dumps(value).encode(),
            b"",
            Duration.seconds(0),
            stdout_truncated=fault == "truncated",
        )

    monkeypatch.setattr(CommandExecutor, "execute", reported)
    worker = ManagedLearningWorker.current()
    root = tmp_path / "operation"
    with pytest.raises(
        (ValueError, RuntimeError),
        match=r"no automatic retry|exact invocation",
    ):
        asyncio.run(worker.execute(plan, grant, root))
    assert len(calls) == 1
    assert len(worker.receipts) == 1
    receipt = json.loads((root / "execution.json").read_bytes())
    assert receipt["retry"] == "NONE; this operation root is consumed"
    assert not (root / "science").exists()
