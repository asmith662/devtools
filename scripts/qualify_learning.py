# Copyright (c) 2026
# ruff: noqa: INP001 -- standalone supported operator entry point
"""One explicitly invoked two-source engineering qualification; no live model calls."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import importlib.metadata
import json
import sys
from dataclasses import asdict
from pathlib import Path

from devtools.agents.learning.budgets import LearningBudget
from devtools.agents.learning.policy import PROFILE
from devtools.agents.learning.process import AdmittedLearningTask, investigate
from devtools.core.paths import resolve_path
from devtools.core.time import Stopwatch
from devtools.learning.integrations.local.classification.codec import document
from devtools.learning.investigation.plans import BinaryProblem, canonical
from devtools.learning.measurement.contracts import EvidenceReference
from devtools.learning.regression.state import RegressionPredictions
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelToolCall,
)
from devtools.resources.filesystem import BinaryFile, FileFormat, TextFile, read, write
from devtools.tools.learning import ManagedLearningWorker

_COMPARISON_MINIMUM = 2

FIXTURES = {
    ("iris-b0047-outer0.json"): (
        "124eb023dadb46a2172cb48c0b75a2302f781e84f73f01438b305a648c1b71fc"
    ),
    ("mpg-b0092-roles.json"): (
        "10a864855c822fc68359e1bbc17fb8f1f33d6f9df5e672a08037587923d1e590"
    ),
}


class ScriptedInvestigator:
    """A deterministic ModelInteraction reading only newly disclosed online evidence."""

    source = InteractionSource("learning-qualification-script-v1")

    def __init__(self) -> None:
        """Start a finite caller-owned native call sequence."""
        self.calls = 0

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Propose a closed action without data paths, grants or evaluator handles."""
        self.calls += 1
        frame = json.loads(request.prompt.messages[-1].content)
        seen = frame["observations"]
        method = None
        if any(o["value"] is None for o in seen):
            action = "ABSTAIN"
        elif frame["support"] is None:
            action = "CHECK_SUPPORT"
        elif len(seen) == len(frame["methods"]) or (
            len(seen) >= _COMPARISON_MINIMUM
            and (
                (seen[-1]["value"] <= max(o["value"] for o in seen[:-1]))
                if frame["family"] == "classification"
                else (seen[-1]["value"] >= min(o["value"] for o in seen[:-1]))
            )
        ):
            action = "STOP"
        elif seen and frame["support"]["changed_constant_coordinates"]:
            action = "ABSTAIN"
        else:
            action = "EVALUATE"
            method = frame["methods"][len(seen)]
        proposal = {
            name: frame[name]
            for name in (
                "task_identity",
                "source_handle",
                "family",
                "metric",
                "schema_identity",
                "unit_identity",
                "role",
                "state_identity",
                "evidence",
            )
        }
        proposal.update(
            action=action,
            method=method,
            rationale=(
                "Use only original acknowledged online measurements under the exp"
                "licitly selected engineering profile."
            ),
        )
        return ModelResponse(
            "One bounded learning request.",
            self.source,
            tool_calls=(
                ModelToolCall(
                    "learning_investigate",
                    canonical(proposal),
                    f"qualification-{self.calls}",
                ),
            ),
        )


def load_tasks(inputs: Path) -> list[AdmittedLearningTask]:
    """Inspect the declared scientific contract.

    Authenticate the two approved destination-owned inputs; no donor lookup
    exists.
    """
    tasks = []
    for name, digest in FIXTURES.items():
        member = read(
            resolve_path(inputs / name),
            file_format=FileFormat.BINARY,
            max_bytes=4 << 20,
        )
        if (
            not isinstance(member, BinaryFile)
            or hashlib.sha256(member.content).hexdigest() != digest
        ):
            msg = "the exact approved learning fixture bytes are required"
            raise ValueError(msg)
        d = json.loads(member.content)
        if d["schema"] != "devtools-learning-fixture-v1" or tuple(d["counts"]) != (
            (49, 17, 34) if d["family"] == "classification" else (274, 59, 59)
        ):
            msg = "the admitted source-role envelope differs"
            raise ValueError(msg)
        tasks.append(
            AdmittedLearningTask(
                d["identity"],
                d["family"],
                d["metric"],
                tuple(d["methods"]),
                canonical(d["online"]),
                canonical(d["final"]),
                canonical(d["source"]),
                EvidenceReference("current-parent-source-admission", digest, digest),
            ),
        )
    return tasks


async def qualify(
    inputs: Path,
    root: Path,
    denied: tuple[Path, ...],
) -> dict[str, object]:
    """Freeze one finite plan, run once, and preserve failures instead of retrying."""
    tasks = load_tasks(inputs)
    budget = LearningBudget()
    maximum = budget.admit_envelope(tuple(task.methods for task in tasks))
    await asyncio.to_thread(root.mkdir)
    worker = ManagedLearningWorker(
        resolve_path(Path(sys.executable)),
        resolve_path(
            Path(str(importlib.metadata.distribution("numpy").locate_file(""))),
        ),
        denied_roots=tuple(resolve_path(p) for p in denied),
    )
    intent = {
        "profile": PROFILE,
        "input_sha256": FIXTURES,
        "maximum_counts": maximum,
        "limits": budget.limits,
        "task_limit_seconds": 3600,
        "root_limit_seconds": 7200,
        "operation_limit_seconds": 300,
        "forecast_incremental_cost": None,
        "source_denominator": len(tasks),
        ("claim"): (
            "Exposed two-source engineering qualification, not a strategy/gen"
            "eralization/savings study."
        ),
    }
    write(
        TextFile(resolve_path(root / "intent.json"), canonical(intent)),
        overwrite=False,
    )
    source_results: list[dict[str, object]] = []
    clock = Stopwatch()
    proposer = ScriptedInvestigator()
    try:
        for index, task in enumerate(tasks):
            task_clock = Stopwatch()
            result = await investigate(
                proposer,
                task,
                worker,
                budget,
                root / f"task-{index}",
                profile=PROFILE,
            )
            report: dict[str, object] = {
                "identity": task.identity,
                "family": task.family,
                "metric": task.metric,
                "terminal": result.terminal,
                "observations": [asdict(o) for o in result.observations],
                "trace": result.trace,
                "seal_identity": result.seal_identity,
            }
            if result.artifact is None:
                report["final"] = None
                report["parent_consumption"] = None
            else:
                artifact = result.artifact
                _training, held = artifact.plan.populations()
                parent_input = (
                    held.features if isinstance(held, BinaryProblem) else held.inputs
                )
                predictions = artifact.predict(parent_input)
                member = read(
                    resolve_path(
                        artifact.reference.root.value
                        / "publication/generations"
                        / artifact.reference.generation_id
                        / "result.json",
                    ),
                    file_format=FileFormat.BINARY,
                    max_bytes=32 << 20,
                )
                if not isinstance(member, BinaryFile):
                    msg = "scientific member required for parent correspondence"
                    raise TypeError(
                        msg,
                    )
                scientific = json.loads(member.content)
                values = (
                    list(predictions.values)
                    if isinstance(predictions, RegressionPredictions)
                    else list(predictions)
                )
                expected = (
                    scientific["predictions"]["values"]
                    if isinstance(predictions, RegressionPredictions)
                    else scientific["predictions"]
                )
                if values != expected:
                    msg = (
                        "actual parent label-free prediction differs from indep"
                        "endently i"
                        "nspected evidence"
                    )
                    raise ValueError(
                        msg,
                    )
                report["final"] = {
                    "method": artifact.plan.method,
                    "quality": document(asdict(artifact.quality)),
                    "publication_sha256": artifact.reference.manifest_sha256,
                    "runtime": scientific["runtime"],
                    "native_correspondence": scientific["native_correspondence"],
                }
                report["parent_consumption"] = {
                    "rows": len(values),
                    "predictions": values,
                    "correspondence": "EXACT",
                    "fitting_calls": 0,
                }
            report["wrapper_seconds"] = task_clock.elapsed.total_seconds
            source_results.append(report)
    except BaseException as error:
        failure = {
            "status": "FAILED_OR_INTERRUPTED",
            "error_type": type(error).__name__,
            "error": str(error),
            "sources": source_results,
            "reserved_counts": budget.consumed,
            "worker_receipts": worker.receipts,
            "wrapper_seconds": clock.elapsed.total_seconds,
            "retry": "NONE; original roots/effects retained",
        }
        write(
            TextFile(resolve_path(root / "failure.json"), canonical(failure)),
            overwrite=False,
        )
        raise
    size = sum(p.stat().st_size for p in root.rglob("*") if p.is_file())
    if size > 512 << 20:
        msg = "actual retained scientific output exceeds the reviewed root cap"
        raise ValueError(
            msg,
        )
    result_report: dict[str, object] = {
        "status": "ENGINEERING_COMPLETE"
        if all(r["parent_consumption"] is not None for r in source_results)
        else "PARTIAL",
        "sources": source_results,
        "reserved_counts": dict(budget.consumed),
        "maximum_counts": maximum,
        "worker_receipts": worker.receipts,
        "native_model_calls": proposer.calls,
        "wrapper_seconds": clock.elapsed.total_seconds,
        "retained_bytes_before_report": size,
        "incremental_cost_forecasts": "UNAVAILABLE",
        "framework_release_gate": "SEPARATE_NOT_INFERRED_FROM_ENGINEERING_SUCCESS",
    }
    write(
        TextFile(resolve_path(root / "result.json"), canonical(result_report)),
        overwrite=False,
    )
    return result_report


def main() -> None:
    """Require explicit execution and a fresh caller-owned evidence root."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--deny-root", action="append", type=Path, default=[])
    parser.add_argument("--execute", action="store_true", required=True)
    args = parser.parse_args()
    report = asyncio.run(qualify(args.inputs, args.output, tuple(args.deny_root)))
    sys.stdout.write(
        canonical({"status": report["status"], "output": str(args.output)}) + "\n",
    )


if __name__ == "__main__":
    main()
