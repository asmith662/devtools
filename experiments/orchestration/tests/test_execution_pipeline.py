# Copyright (c) 2026
# ruff: noqa: S101, PLR0915, PLR2004, COM812, FBT001 -- isolated synthetic execution
"""Test real orchestration processes with model-free substitutes."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

import pytest

from devtools.core.identity import Identity
from devtools.core.paths import resolve_path
from devtools.orchestration.experiments import (
    ExperimentExecutionPipeline,
    execution,
    receipts,
)
from devtools.resources.commands import Command
from experiments.codex_dogfood.case_0009.artifacts import digest
from experiments.orchestration.controller import PACKAGE, implementation
from experiments.orchestration.model import RunPlan
from experiments.orchestration.storage import save
from experiments.orchestration.tests.test_preparation import checkout

CHECKPOINT = r"""
async def _synthetic_checkpoint(self, boundary, paths):
    for command in self.value["validation"][validation_tier(boundary, paths)]:
        await self.process(
            expand(
                command,
                {"python": sys.executable, "repository": str(self.repository.root)},
            ),
            self.repository.root,
            "cohort",
            boundary + "-fixture",
            "validation",
        )


Controller.checkpoint_validation = _synthetic_checkpoint
"""

ACCOUNTING = r"""


    if mode == "run" and stage == "C":
        from types import SimpleNamespace
        from devtools.core.time import Duration
        from experiments.orchestration import usage_budget
        from experiments.orchestration.controller import implementation
        from experiments.orchestration.model import RunPlan
        from experiments.orchestration.storage import save
        from experiments.orchestration.workers import measurement

        target = Path(__file__).parent
        plan = RunPlan.parse(json.loads((target / "plan.json").read_bytes()))
        run_id = plan.identity(implementation())
        raw = (
            json.dumps({"type": "thread.started", "thread_id": "synthetic-" + case})
            + "\n"
            + json.dumps(
                {
                    "type": "turn.completed",
                    "usage": {
                        "input_tokens": 10,
                        "cached_input_tokens": 2,
                        "cache_write_input_tokens": 0,
                        "output_tokens": 4,
                        "reasoning_output_tokens": 1,
                    },
                }
            )
            + "\n"
        ).encode()
        measured = measurement.capture(
            plan.value["semantic"],
            case,
            run_id + "/" + case + "/C",
            b"synthetic",
            SimpleNamespace(stdout=raw, duration=Duration.seconds(1)),
            b"{}",
            validated=True,
            failure=None,
        )
        save(root / "synthetic-measurement.json", measured)
        usage_budget.capture(
            target,
            run_id,
            case,
            "C",
            root / "synthetic-measurement.json",
            accepted=True,
        )
"""


async def executable_checkout(
    tmp_path: Path, *, fault: str = "", accounting: bool = True
) -> tuple[ExperimentExecutionPipeline, Any]:
    """Freeze test-only validators and workers into a separately installed target."""
    original, repo = await checkout(tmp_path)
    root = original.target
    controller_path = root / "experiments/orchestration/controller.py"
    controller_path.write_bytes(controller_path.read_bytes() + CHECKPOINT.encode())
    value = json.loads((root / "plan.json").read_bytes())
    worker = Path(__file__).with_name("worker.py").read_text()
    worker = worker.replace(
        "    mode, stage, case, raw_frame = sys.argv[1:5]",
        '    if sys.argv[1:] == ["--help"]:\n'
        '        print("usage: synthetic execution")\n'
        "        return\n"
        "    mode, stage, case, raw_frame = sys.argv[1:5]",
    )
    if accounting:
        worker = worker.replace(
            "        return\n    files = {}",
            ACCOUNTING + "\n        return\n    files = {}",
        )
    if fault == "preparefailure":
        worker = worker.replace(
            "    frame = json.loads(raw_frame)",
            '    if mode == "run" and stage == "prepare":\n'
            "        raise SystemExit(11)\n"
            "    frame = json.loads(raw_frame)",
        )
    (root / "worker.py").write_bytes(worker.encode())
    value["concurrency"]["semantic"] = 1
    value["implementation"]["worker.py"] = digest(worker.encode())
    value["worker_entrypoints"]["scripts"]["worker.py"] = digest(worker.encode())
    for command in [*value["commands"].values(), value["semantic"]["argv"]]:
        command[-1] = fault
    value["controller_implementation"] = {
        address: digest((root / "experiments/orchestration" / address).read_bytes())
        for address in implementation()
    }
    save(
        root / "protocol.json",
        {
            "usage_budget": value["usage_budget"],
            "economics": value["economics"],
            "semantic_execution": value["semantic"],
            "worker_entrypoints": value["worker_entrypoints"],
        },
    )
    await repo.git("add", ".")
    await repo.git("commit", "-m", "Freeze synthetic execution adapters and protocol")
    value["stage_a"]["checkpoint"] = (
        (await repo.git("rev-parse", "HEAD")).decode().strip()
    )
    value["stage_a"]["protocol"]["sha256"] = digest(
        (root / "protocol.json").read_bytes()
    )
    (root / "plan.json").write_bytes(RunPlan.parse(value).canonical)
    await repo.git("add", "plan.json")
    await repo.git("commit", "-m", "Synthetic prospective execution plan")
    # Persistent external storage exercises the real retention guard, without a bypass.
    retained = (
        PACKAGE.parents[1] / ".local/pipeline-execution-tests" / str(Identity.new())
    )
    return ExperimentExecutionPipeline(root, retained, original.python), repo


async def grant(subject: ExperimentExecutionPipeline, work: Path) -> None:
    """Issue approval from a separate trusted synthetic host."""
    program = """
import asyncio
from pathlib import Path
from experiments.orchestration.controller import Controller
from experiments.orchestration.authority import ApprovalRequest
async def main():
    c = await Controller.from_plan(
        Path.cwd(), 'plan.json', Path(__import__('sys').argv[1]))
    await c.approve(ApprovalRequest(
        c.run_id, 'synthetic-maintainer', 'isolated test grant'))
asyncio.run(main())
"""
    result = await subject.executor.execute(
        Command(str(subject.python))
        .args("-B", "-c", program, str(work))
        .cwd(resolve_path(subject.target))
    )
    assert result.succeeded, result.stderr


def test_authorized_end_to_end(tmp_path: Path) -> None:
    """Consume approval, dispatch the controller and authenticate closeout."""

    async def run() -> None:
        subject, repo = await executable_checkout(tmp_path)
        prepared = await subject.prepare(Path("plan.json"))
        assert prepared["disposition"] == "READY_FOR_APPROVAL", prepared
        work = tmp_path / "workers"
        refused = await subject.execute(Path("plan.json"), work)
        assert refused["disposition"] == "ADMISSION_REFUSED", refused
        assert "approval absent" in refused["error"]
        assert not refused["dispatch_requested"]
        await grant(subject, work)
        local = subject.target / ".local/usage"
        policy = (local / "policy.json").read_bytes()
        save(
            local / "policy.json",
            {
                "limits": [
                    {
                        "scope": "OBSERVED_WINDOW",
                        "identity": "local",
                        "limits": {
                            "fresh_calls": 0,
                            "input_tokens": None,
                            "output_tokens": None,
                        },
                    }
                ]
            },
        )
        budget_refused = await subject.execute(Path("plan.json"), work)
        assert budget_refused["disposition"] == "ADMISSION_REFUSED"
        assert "BUDGET_BLOCKED" in budget_refused["error"]
        (local / "policy.json").unlink()
        unavailable = await subject.execute(Path("plan.json"), work)
        assert unavailable["disposition"] == "ADMISSION_REFUSED"
        assert "BUDGET_UNAVAILABLE" in unavailable["error"]
        (local / "policy.json").write_bytes(policy)
        worker = subject.target / "worker.py"
        bound_worker = worker.read_bytes()
        worker.write_bytes(bound_worker + b"# changed target after preparation\n")
        changed = await subject.execute(Path("plan.json"), work)
        assert changed["disposition"] == "ADMISSION_REFUSED"
        assert not changed["dispatch_requested"]
        worker.write_bytes(bound_worker)
        wrong_preparation = dict(prepared)
        wrong_preparation["validation"] = dict(prepared["validation"])
        wrong_preparation["validation"]["executable"] = {
            "sha256": "0" * 64,
            "version": "changed",
        }
        wrong_path = subject.receipt_root / "wrong-executable.json"
        receipts.store(wrong_path, wrong_preparation)
        wrong_executable = await subject.execute(
            Path("plan.json"), work, preparation=wrong_path
        )
        assert wrong_executable["disposition"] == "ADMISSION_REFUSED"
        assert "executable binding changed" in wrong_executable["error"]
        prior = Path(refused["report"]).with_name("admission-request.json")
        changed_plan = receipts.restore(prior)
        changed_plan["plan_sha256"] = "0" * 64
        changed_plan_path = subject.receipt_root / "changed-plan.json"
        receipts.store(
            changed_plan_path, changed_plan, schema=receipts.EXECUTION_SCHEMA
        )
        with pytest.raises(execution.TargetError, match="Prepared plan digest differs"):
            await execution.exchange(subject, "admit", changed_plan_path)
        admitted = await execution.exchange(subject, "admit", prior)
        mismatch = receipts.restore(prior)
        mismatch["authorization"] = {
            **admitted["authorization"],
            "approval_sha256": "foreign",
        }
        mismatch_path = subject.receipt_root / "mismatched-approval.json"
        receipts.store(mismatch_path, mismatch, schema=receipts.EXECUTION_SCHEMA)
        with pytest.raises(execution.TargetError, match="Approval changed"):
            await execution.exchange(subject, "dispatch", mismatch_path)
        progress: list[dict[str, Any]] = []
        result = await subject.execute(
            Path("plan.json"), work, observer=progress.append
        )
        assert result["disposition"] == "COMPLETE", result
        assert result["closeout"]["scientific_evidence"]["verification"] == "PASS"
        assert result["closeout"]["usage"]["experiment"]["tokens"]["input_tokens"] == 30
        assert (
            result["closeout"]["usage"]["experiment"]["tokens"]["cached_input_tokens"]
            == 6
        )
        assert (
            result["closeout"]["usage"]["experiment"]["tokens"]["output_tokens"] == 12
        )
        assert (
            result["closeout"]["usage"]["experiment"]["tokens"]["reasoning_tokens"] == 3
        )
        assert result["closeout"]["scientific_acceptance"].startswith("UNASSESSED")
        assert progress
        assert (await subject.reconcile(Path("plan.json")))["disposition"] == "COMPLETE"
        assert (
            receipts.latest(subject.receipt_root, "plan.json")["disposition"]
            == "COMPLETE"
        )
        duplicate = await subject.execute(Path("plan.json"), work)
        assert duplicate["disposition"] == "ADMISSION_REFUSED", duplicate
        assert not duplicate["dispatch_requested"]
        with pytest.raises(execution.TargetError, match="Existing run"):
            await execution.exchange(
                subject,
                "dispatch",
                Path(result["report"]).with_name("dispatch-request.json"),
            )
        assert not await repo.git("status", "--porcelain")
        save(
            PACKAGE.parents[1] / ".local/increment2-demonstration.json",
            {
                "target": str(subject.target),
                "receipts": str(subject.receipt_root),
                "result": result,
                "synthetic_model_calls": 3,
                "real_model_calls": 0,
            },
        )

        execution_folder = Path(result["report"]).parent
        returned = execution_folder / "controller-return.json"
        original_return = returned.read_bytes()
        foreign_return = receipts.restore(returned)
        foreign_return["attempt"] = "foreign"
        returned.unlink()
        receipts.store(returned, foreign_return, schema=receipts.EXECUTION_SCHEMA)
        corrupt_return = await subject.reconcile(Path("plan.json"))
        assert corrupt_return["disposition"] == "RECONCILIATION_REQUIRED"
        assert "return/dispatch identity differs" in corrupt_return["error"]
        returned.write_bytes(original_return)
        returned.unlink()
        unknown = await subject.reconcile(Path("plan.json"))
        assert unknown["disposition"] == "RECONCILIATION_REQUIRED"
        returned.write_bytes(original_return)
        ledger = (local / "ledger.json").read_bytes()
        (local / "ledger.json").unlink()
        missing = await subject.reconcile(Path("plan.json"))
        assert missing["disposition"] == "COMPLETE_WITH_PARTIAL_ACCOUNTING"
        assert missing["closeout"]["usage"]["experiment"] is None
        (local / "ledger.json").write_bytes(ledger)
        publication = Path(result["closeout"]["publication_root"]) / "D.json"
        publication_bytes = publication.read_bytes()
        publication.unlink()
        incomplete = await subject.reconcile(Path("plan.json"))
        assert incomplete["disposition"] == "RECONCILIATION_REQUIRED"
        publication.write_bytes(publication_bytes)
        marker = (
            subject.target
            / "experiments/orchestration/supersessions"
            / (result["run_id"] + ".json")
        )
        save(marker, {"synthetic": True})
        await repo.git("add", ".")
        await repo.git("commit", "-m", "Synthetic supersession after demonstration")
        other = ExperimentExecutionPipeline(
            subject.target,
            subject.receipt_root.parent / str(Identity.new()),
            subject.python,
        )
        superseded = await other.execute(
            Path("plan.json"), work, preparation=Path(prepared["report"])
        )
        assert superseded["disposition"] == "ADMISSION_REFUSED"
        assert "Superseded" in superseded["error"]

    asyncio.run(run())


@pytest.mark.parametrize(
    ("fault", "accounting", "expected"),
    [
        ("", False, "COMPLETE_WITH_PARTIAL_ACCOUNTING"),
        ("nonzero", False, "CONTROLLER_FAILED"),
        ("preparefailure", False, "CONTROLLER_FAILED"),
    ],
)
def test_controller_failure_and_partial_accounting(
    tmp_path: Path, fault: str, accounting: bool, expected: str
) -> None:
    """Keep real controller outcomes distinct from transport/process success."""

    async def run() -> None:
        subject, _repo = await executable_checkout(
            tmp_path, fault=fault, accounting=accounting
        )
        ready = await subject.prepare(Path("plan.json"))
        assert ready["disposition"] == "READY_FOR_APPROVAL", ready
        await grant(subject, tmp_path / "work")
        result = await subject.execute(Path("plan.json"), tmp_path / "work")
        assert result["disposition"] == expected, result
        assert result["closeout"]["automatic_scientific_retries"] == 0
        if fault == "preparefailure":
            assert result["closeout"]["phase"] == "BEFORE_SCIENTIFIC_STAGES"
            assert result["closeout"]["inventoried_operation_entries"] == []
        assert (await subject.reconcile(Path("plan.json")))["disposition"] == expected

    asyncio.run(run())


def test_interrupt_real_controller_then_observe(tmp_path: Path) -> None:
    """Cancel after journal entry and preserve unknown completion."""

    async def run() -> None:
        subject, _repo = await executable_checkout(tmp_path, accounting=False)
        ready = await subject.prepare(Path("plan.json"))
        assert ready["disposition"] == "READY_FOR_APPROVAL"
        await grant(subject, tmp_path / "work")
        task: asyncio.Task[dict[str, Any]]

        def observe(event: dict[str, Any]) -> None:
            if (
                event.get("case") == "alpha"
                and event.get("stage") == "C"
                and event.get("status") == "RUNNING"
            ):
                task.cancel()

        task = asyncio.create_task(
            subject.execute(Path("plan.json"), tmp_path / "work", observer=observe)
        )
        with pytest.raises(asyncio.CancelledError):
            await asyncio.wait_for(task, 240)
        latest = receipts.latest(subject.receipt_root, "plan.json", active=True)
        assert latest["disposition"] == "DISPATCH_COMPLETION_UNKNOWN"
        reconciled = await subject.reconcile(Path("plan.json"))
        assert reconciled["disposition"] == "RECONCILIATION_REQUIRED", reconciled
        refused = await subject.execute(Path("plan.json"), tmp_path / "work")
        assert refused["disposition"] == "ADMISSION_REFUSED"
        assert not refused["dispatch_requested"]

    asyncio.run(run())
