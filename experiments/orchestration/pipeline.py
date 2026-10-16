# Copyright (c) 2026
# ruff: noqa: ASYNC240, COM812 -- concrete target/controller transport
"""Target-owned pipeline admission and read-only scientific reconciliation.

No approval is created here. Scientific operations remain exclusively in Controller.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from devtools.core.paths import resolve_path
from devtools.core.time import Timestamp
from devtools.observability.usage import UsageWindow, report
from devtools.observability.usage.storage import load as observations
from devtools.orchestration.experiments import receipts
from experiments.codex_dogfood.case_0009.artifacts import digest
from experiments.orchestration import usage_budget
from experiments.orchestration.controller import Controller
from experiments.orchestration.lease import writer
from experiments.orchestration.model import RunPlan
from experiments.orchestration.observation import Console, append_operational
from experiments.orchestration.publication import Repository
from experiments.orchestration.storage import binary, exclusive, load, require, safe


class Progress(Console):
    """Project existing controller observations without interpreting worker text."""

    def __init__(self, folder: Path) -> None:
        """Bind external operational progress; journals stay authoritative."""
        super().__init__()
        self.path = folder / "progress.jsonl"

    def emit(self, event: dict[str, Any]) -> None:
        """Stream bounded lifecycle fields with operational provenance."""
        selected: dict[str, Any] = {
            k: event[k]
            for k in (
                "timestamp",
                "elapsed_seconds",
                "case",
                "stage",
                "operation",
                "status",
                "pid",
                "duration_seconds",
                "operation_progress",
                "failure_category",
            )
            if k in event
        }
        selected["provenance"] = "CONTROLLER_OPERATIONAL_OBSERVATION"
        append_operational(self.path, selected)
        print(json.dumps(selected), file=sys.stderr, flush=True)  # noqa: T201


def usage(request: dict[str, Any]) -> dict[str, Any]:
    """Read existing metadata with stable execution-window and run attribution."""
    root = Path(request["target"])
    path = root / ".local/usage/ledger.json"
    now = Timestamp.now()
    rows = observations(path)
    selected = tuple(r for r in rows if r.attribution.experiment == request["run_id"])
    return {
        "status": "PARTIAL" if path.exists() else "UNAVAILABLE",
        "sources": {
            name: {
                "path": str(path.parent / name),
                "sha256": digest(binary(path.parent / name))
                if (path.parent / name).exists()
                else None,
            }
            for name in (
                "ledger.json",
                "policy.json",
                "backfill.json",
                "reservations.json",
            )
        },
        "local": report(rows, UsageWindow.rolling(now)) if path.exists() else None,
        "experiment": report(
            selected,
            UsageWindow(Timestamp.from_isoformat(request["started"]), now),
            experiment=request["run_id"],
        )
        if path.exists()
        else None,
    }


async def controller(request: dict[str, Any], *, prospective: bool) -> Controller:
    """Reuse controller authentication for the exact target/plan/environment."""
    root = resolve_path(request["target"]).value
    require(root == Path.cwd().resolve(), "Target checkout differs")
    require(
        Path(sys.executable).resolve() == resolve_path(request["python"]).value,
        "Target executable differs",
    )
    require(
        digest(binary(Path(sys.executable))) == request["python_sha256"]
        and sys.version == request["python_version"],
        "Target executable binding changed",
    )
    require(
        digest(binary(safe(root, request["plan"]))) == request["plan_sha256"],
        "Prepared plan digest differs",
    )
    repo = Repository(root, push=False)
    require(
        resolve_path(
            (await repo.git("rev-parse", "--absolute-git-dir")).decode().strip()
        ).value
        == resolve_path(request["target_git_directory"]).value,
        "Target Git identity differs",
    )
    if prospective:
        return await Controller.from_plan(
            root,
            request["plan"],
            Path(request["work_root"]),
            reporter=Progress(Path(request["folder"])),
        )
    plan = RunPlan.parse(load(safe(root, request["plan"])))
    checked = Controller(
        Repository(
            root,
            plan.value["publication"]["remote"],
            push=plan.value["publication"]["push"],
        ),
        plan,
        Path(request["work_root"]),
    )
    checked.plan_address = request["plan"]
    return checked


async def admit(request: dict[str, Any]) -> dict[str, Any]:
    """Read-only admission consumes durable exact authority; it mints no grant."""
    checked = await controller(request, prospective=True)
    authorization = await checked.execution_authorization()
    require(checked.run_id == request["run_id"], "Prepared scientific identity differs")
    require(
        not (checked.science / "run.json").exists(),
        "Existing run; reconciliation required; no retry",
    )
    require(
        {p.name for p in checked.science.iterdir()} <= {"authorization"},
        "Orphan scientific state; reconciliation required",
    )
    approved = load(checked.science / "authorization/approval.json")
    require(
        request["prepared_head"]
        in {approved["review_checkpoint"], authorization.checkpoint},
        "Prepared target is not the exact approval review/checkpoint",
    )
    require(
        checked.validated_head == authorization.checkpoint,
        "Target advanced after exact approval",
    )
    decision = usage_budget.preview(
        checked.repository.root, checked.value, checked.run_id
    )
    require(
        decision["status"] == "BUDGET_CHECK_PASS",
        "BUDGET_UNAVAILABLE: configured policy required",
    )
    claim = (
        checked.repository.root
        / ".local/experiment-pipeline-dispatch"
        / (checked.run_id + ".json")
    )
    require(
        not claim.exists(), "Prior dispatch intent; reconciliation required; no retry"
    )
    return {
        "status": "ADMITTED",
        "authorization": authorization.__dict__,
        "prefix": checked.prefix,
        "budget": decision,
        "usage": usage(request),
        "forecast": checked.value["economics"],
        "name": checked.value["name"],
    }


async def dispatch(request: dict[str, Any]) -> dict[str, Any]:
    """Claim once, then invoke the controller; never expose approval publication."""
    admission = await admit(request)
    require(
        admission["authorization"] == request["authorization"],
        "Approval changed after admission",
    )
    checked = await controller(request, prospective=True)
    authorization = await checked.execution_authorization()
    claim = (
        checked.repository.root
        / ".local/experiment-pipeline-dispatch"
        / (checked.run_id + ".json")
    )
    with writer(checked.repository.root):
        require(not claim.exists(), "Concurrent/prior dispatch; no retry")
        require(
            authorization == await checked.execution_authorization(),
            "Approval changed before dispatch",
        )
        exclusive(
            claim,
            {
                "schema": "experiment-pipeline-dispatch-v1",
                "request_sha256": receipts.digest(request),
                "attempt": request["attempt"],
                "folder": request["folder"],
                "run_id": checked.run_id,
                "started": str(Timestamp.now()),
            },
        )
    returned: dict[str, Any] = {
        "run_id": checked.run_id,
        "request_sha256": receipts.digest(request),
        "attempt": request["attempt"],
        "outcome": "UNKNOWN",
    }
    try:
        result = await checked.run(authorization, require_budget_policy=True)
        returned.update(outcome="RETURNED", controller_result=result)
    except BaseException as error:
        returned.update(
            outcome="RAISED", error=type(error).__name__ + ": " + str(error)
        )
        raise
    finally:
        returned["finished"] = str(Timestamp.now())
        receipts.store(
            Path(request["folder"]) / "controller-return.json",
            returned,
            schema=receipts.EXECUTION_SCHEMA,
        )
    return await reconcile(request)


async def reconcile(request: dict[str, Any]) -> dict[str, Any]:
    """Authenticate available authoritative records; never resume or dispatch."""
    checked = await controller(request, prospective=False)
    authorization = await checked.execution_authorization()
    require(
        authorization.__dict__ == request["authorization"], "Execution approval differs"
    )
    claim = (
        checked.repository.root
        / ".local/experiment-pipeline-dispatch"
        / (checked.run_id + ".json")
    )
    require(
        claim.exists() and load(claim)["request_sha256"] == receipts.digest(request),
        "No matching dispatch claim; completion unknown",
    )
    returned_path = Path(request["folder"]) / "controller-return.json"
    returned = receipts.restore(returned_path) if returned_path.exists() else None
    if returned is not None:
        require(
            returned["run_id"] == checked.run_id
            and returned["attempt"] == request["attempt"]
            and returned["request_sha256"] == receipts.digest(request),
            "Controller return/dispatch identity differs",
        )
    observed = usage(request)
    result: dict[str, Any] = {
        "status": "RECONCILIATION_REQUIRED",
        "authorization": authorization.__dict__,
        "controller_return": returned,
        "usage": observed,
        "forecast": checked.value.get("economics"),
        "journal_root": str(checked.science / "journal"),
        "publication_root": str(checked.science / "publications"),
        "scientific_acceptance": "UNASSESSED; MAINTAINER_REVIEW_REQUIRED",
        "automatic_scientific_retries": 0,
    }
    if not (checked.science / "run.json").exists():
        result["status"] = (
            "FAILED_BEFORE_SCIENTIFIC_ENTRY"
            if returned
            else "DISPATCH_COMPLETION_UNKNOWN"
        )
        return result
    verified = await checked.verify()
    result["scientific_evidence"] = verified
    result["scientific_stage_entries"] = sorted(
        k for k in verified["stages"] if k.split("/")[-1] in {"B", "C"}
    )
    result["phase"] = (
        "SCIENTIFIC_STAGES_ENTERED"
        if result["scientific_stage_entries"]
        else "BEFORE_SCIENTIFIC_STAGES"
    )
    result["inventoried_operation_entries"] = sorted(
        set(verified["stages"]) & set(checked.value["usage_budget"]["calls"])
    )
    if returned is None:
        return result
    if returned["outcome"] != "RETURNED" or not verified["status"].startswith(
        "COMPLETE"
    ):
        result["status"] = "CONTROLLER_FAILED"
        return result
    require(
        set(verified["publications"]) == {"PACKET", "B", "C", "D"},
        "Publication incomplete",
    )
    require(
        not any(v.startswith("DEAD") for v in verified["stages"].values()),
        "Dead scientific operation",
    )
    report_value = observed["experiment"]
    reservations_path = checked.repository.root / ".local/usage/reservations.json"
    reservations = (
        load(reservations_path)["calls"] if reservations_path.exists() else {}
    )
    own = {k: v for k, v in reservations.items() if v["run_id"] == checked.run_id}
    result["budget_reservations"] = own
    result["consumption_budget"] = usage_budget.consumption(
        checked.repository.root, checked.value, checked.run_id
    )
    result["forecast_comparison"] = {
        field: {
            "reported_subtotal": report_value["tokens"][field]
            if report_value
            else None,
            "forecast_upper": sum(
                call[bound] for call in checked.value["usage_budget"]["calls"].values()
            )
            if all(
                call[bound] is not None
                for call in checked.value["usage_budget"]["calls"].values()
            )
            else None,
            "unknown_observations": report_value["unknown_category_observations"][field]
            if report_value
            else None,
        }
        for field, bound in (
            ("input_tokens", "input_upper"),
            ("output_tokens", "output_upper"),
        )
    }
    expected = checked.value["usage_budget"]["fresh_call_limit"]
    complete = (
        report_value is not None
        and report_value["fresh_invocations"] == expected
        and not report_value["missing_usage_invocations"]
        and not report_value["conflicting_invocations_excluded"]
        and not report_value["unallocated_timestamp_observations"]
        and len(own) == expected
        and all(v["settled"] for v in own.values())
        and result["consumption_budget"]["status"] == "BUDGET_CHECK_PASS"
    )
    result["accounting"] = (
        "COMPLETE_OBSERVED_SCOPE" if complete else "PARTIAL_OR_MISSING"
    )
    result["status"] = "COMPLETE" if complete else "COMPLETE_WITH_PARTIAL_ACCOUNTING"
    return result
