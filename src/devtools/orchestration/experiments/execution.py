# Copyright (c) 2026
# ruff: noqa: BLE001, S110, TRY301, TRY003, EM101, COM812, PLR0915 -- concrete durable execution transport
"""Governed target dispatch and observation-only closeout; no scientific scheduler."""

from __future__ import annotations

import asyncio
import json
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any

from devtools.core.paths import get_temp_dir, resolve_path
from devtools.core.time import Duration, Timestamp
from devtools.orchestration.experiments import receipts
from devtools.resources.commands import Command
from devtools.resources.commands.events import CommandStderr

if TYPE_CHECKING:
    from collections.abc import Callable

    from devtools.orchestration.experiments.pipeline import ExperimentExecutionPipeline


PROGRAM = r"""
import asyncio
import json
import sys
from pathlib import Path
from devtools.resources import commands
from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration import controller
from experiments.orchestration.storage import load, require


async def main():
    action, address, expected = sys.argv[1:]
    root = Path.cwd().resolve()
    if not Path(controller.__file__).resolve().is_relative_to(
        root / "experiments"
    ) or not Path(commands.__file__).resolve().is_relative_to(root / "src"):
        raise ValueError("Target source imported from another checkout")
    # The controller's existing canonical JSON is byte-identical to the receipt
    # payload encoding, including on older targets lacking the pipeline package.
    envelope = load(Path(address))
    request = envelope["value"]
    require(
        envelope["schema"] == "experiment-execution-v1"
        and envelope["sha256"] == digest(json_bytes(request)) == expected,
        "Execution request integrity differs",
    )
    try:
        from experiments.orchestration import pipeline
    except ImportError:
        # Read-only refusal on older targets still authenticates their own authority.
        checked = await controller.Controller.from_plan(
            root, request["plan"], Path(request["work_root"])
        )
        await checked.execution_authorization()
        raise ValueError("Target lacks governed execution contract")
    operation = {
        "admit": pipeline.admit,
        "dispatch": pipeline.dispatch,
        "reconcile": pipeline.reconcile,
    }[action]
    print(json.dumps(await operation(request)))


try:
    asyncio.run(main())
except (ValueError, OSError, KeyError) as error:
    print(json.dumps({"error": str(error)}))
    sys.exit(1)
"""


class TargetError(ValueError):
    """Retain a target refusal/unknown transport result without suggesting retry."""


async def exchange(
    pipeline: ExperimentExecutionPipeline,
    action: str,
    request_path: Path,
    observer: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    """Stream controller observations through the canonical command lifecycle."""
    request = receipts.restore(request_path)
    command = (
        Command(str(pipeline.python))
        .args(
            "-B",
            "-c",
            PROGRAM,
            action,
            str(request_path),
            receipts.digest(request),
        )
        .cwd(resolve_path(pipeline.target))
    )
    command = (
        command.without_timeout()
        if action == "dispatch"
        else command.with_timeout(Duration.seconds(300))
    )
    execution = pipeline.executor.start(command)

    async def drain() -> None:
        pending = b""
        async for event in execution.events():
            if isinstance(event, CommandStderr):
                pending = (pending + event.data)[-(1 << 20) :]
                lines = pending.split(b"\n")
                pending = lines.pop()
                for line in lines:
                    try:
                        value = json.loads(line)
                        if observer is not None:
                            observer(value)
                    except Exception:
                        pass  # Operational observation cannot own or authorize science.

    draining = asyncio.create_task(drain())
    try:
        result = await execution
        await draining
    finally:
        draining.cancel()
        await asyncio.gather(draining, return_exceptions=True)
    if result.failed or result.stdout_truncated or result.stderr_truncated:
        raise TargetError(
            result.stdout.decode(errors="replace")
            + result.stderr.decode(errors="replace")[-2048:]
        )
    value = dict(json.loads(result.stdout))
    value["adapter_exit_code"] = result.exit_code
    return value


def retained(root: Path) -> None:
    """Refuse disposable default/temp storage before any consequential request."""
    if root.is_relative_to(get_temp_dir().value):
        message = (
            "Execution requires a persistent external receipt directory "
            "outside OS temporary storage"
        )
        raise ValueError(message)


def execution_history(root: Path, plan: str | None = None) -> list[dict[str, Any]]:
    """Select pipeline executions while retaining preparation-schema compatibility."""
    return [r for r in receipts.history(root, plan) if r.get("kind") == "execution"]


async def execute(
    pipeline: ExperimentExecutionPipeline,
    plan: Path,
    work_root: Path,
    *,
    preparation: Path | None = None,
    observer: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    """Consume a preparation reference and external exact-run approval, once."""
    retained(pipeline.receipt_root)
    address = (
        resolve_path(plan, base_directory=pipeline.target)
        .value.relative_to(pipeline.target)
        .as_posix()
    )
    if preparation is None:
        candidates = [
            r
            for r in receipts.history(pipeline.receipt_root, address)
            if r.get("kind") != "execution" and r["target"] == str(pipeline.target)
        ]
        if not candidates:
            message = "No preparation for this target/plan"
            raise ValueError(message)
        preparation = Path(candidates[0]["report"])
    preparation = resolve_path(preparation, base_directory=Path.cwd()).value
    prepared = receipts.restore(preparation)
    attempt = str(receipts.ExecutionId.new())
    folder = pipeline.receipt_root / attempt
    folder.mkdir(parents=True)
    start = time.perf_counter()
    result: dict[str, Any] = {
        "kind": "execution",
        "pipeline": "ExperimentExecutionPipeline",
        "version": "2",
        "attempt": attempt,
        "started": str(Timestamp.now()),
        "plan": address,
        "plan_sha256": prepared.get("plan_sha256"),
        "target": str(pipeline.target),
        "python": str(pipeline.python),
        "target_head": prepared.get("target_head"),
        "preparation": {"path": str(preparation), "sha256": receipts.digest(prepared)},
        "report": str(folder / "result.json"),
        "stages": [],
        "dispatch_requested": False,
        "execution_authorized": "NO",
        "scientific_acceptance": "UNASSESSED",
    }
    receipts.store(folder / "start.json", result, schema=receipts.EXECUTION_SCHEMA)
    active = "admission"
    stage_start = str(Timestamp.now())
    stage_begin = time.perf_counter()
    try:
        if (
            prepared["disposition"] != "READY_FOR_APPROVAL"
            or prepared["plan"] != address
            or prepared["target"] != str(pipeline.target)
            or prepared["python"] != str(pipeline.python)
        ):
            raise TargetError(
                "Preparation identity/readiness differs; no authority inferred"
            )
        run_id = prepared["validation"]["run_id"]
        result["run_id"] = run_id
        for previous in execution_history(pipeline.receipt_root, address):
            if (
                previous["attempt"] != attempt
                and previous["target"] == str(pipeline.target)
                and previous.get("run_id") == run_id
                and previous.get("dispatch_requested")
            ):
                raise TargetError(
                    "Prior dispatch request requires reconciliation; no retry"
                )
        request = {
            "attempt": attempt,
            "started": result["started"],
            "folder": str(folder),
            "target": str(pipeline.target),
            "python": str(pipeline.python),
            "plan": address,
            "plan_sha256": prepared["plan_sha256"],
            "run_id": run_id,
            "target_git_directory": prepared["target_git_directory"],
            "python_sha256": prepared["validation"]["executable"]["sha256"],
            "python_version": prepared["validation"]["executable"]["version"],
            "prepared_head": prepared["target_head"],
            "work_root": str(resolve_path(work_root, base_directory=Path.cwd()).value),
        }
        receipts.store(
            folder / "admission-request.json", request, schema=receipts.EXECUTION_SCHEMA
        )
        stage_start = str(Timestamp.now())
        admission = await exchange(
            pipeline, "admit", folder / "admission-request.json", observer
        )
        stage = {
            "name": "admission",
            "started": stage_start,
            "finished": str(Timestamp.now()),
            "elapsed_seconds": time.perf_counter() - stage_begin,
            "disposition": "ADMITTED",
            "evidence": admission,
        }
        receipts.store(
            folder / "admission.json", stage, schema=receipts.EXECUTION_SCHEMA
        )
        result["stages"].append({"name": "admission", "sha256": receipts.digest(stage)})
        result.update(
            execution_authorized="YES",
            authorization=admission["authorization"],
            baseline=admission["usage"],
        )
        request["authorization"] = admission["authorization"]
        active = "dispatch"
        stage_start = str(Timestamp.now())
        stage_begin = time.perf_counter()
        # Durable intent precedes launch; it does not prove scientific entry.
        receipts.store(
            folder / "dispatch-request.json", request, schema=receipts.EXECUTION_SCHEMA
        )
        result["dispatch_requested"] = True
        result["closeout"] = await exchange(
            pipeline, "dispatch", folder / "dispatch-request.json", observer
        )
        result["disposition"] = result["closeout"]["status"]
    except asyncio.CancelledError:
        result["disposition"] = (
            "DISPATCH_COMPLETION_UNKNOWN"
            if result["dispatch_requested"]
            else "INTERRUPTED_BEFORE_DISPATCH"
        )
        raise
    except Exception as error:
        result.update(
            disposition="DISPATCH_COMPLETION_UNKNOWN"
            if result["dispatch_requested"]
            else "ADMISSION_REFUSED",
            error=str(error),
        )
    finally:
        if not any(stage["name"] == active for stage in result["stages"]):
            stage = {
                "name": active,
                "started": stage_start,
                "finished": str(Timestamp.now()),
                "elapsed_seconds": time.perf_counter() - stage_begin,
                "disposition": result["disposition"],
                "evidence": result.get("closeout"),
                "error": result.get("error"),
            }
            receipts.store(
                folder / (active + ".json"), stage, schema=receipts.EXECUTION_SCHEMA
            )
            result["stages"].append({"name": active, "sha256": receipts.digest(stage)})
        result.update(
            finished=str(Timestamp.now()), elapsed_seconds=time.perf_counter() - start
        )
        receipts.store(folder / "result.json", result, schema=receipts.EXECUTION_SCHEMA)
    return result


async def reconcile(
    pipeline: ExperimentExecutionPipeline, plan: Path | None = None
) -> dict[str, Any]:
    """Append an observation; never resend a dispatch request or overwrite history."""
    address = (
        resolve_path(plan, base_directory=pipeline.target)
        .value.relative_to(pipeline.target)
        .as_posix()
        if plan is not None
        else None
    )
    rows = [
        r
        for r in execution_history(pipeline.receipt_root, address)
        if r["target"] == str(pipeline.target)
    ]
    if not rows or len({(r["plan_sha256"], r["target"]) for r in rows}) != 1:
        message = "No unambiguous execution to reconcile"
        raise ValueError(message)
    intents = [
        r for r in rows if (Path(r["report"]).parent / "dispatch-request.json").exists()
    ]
    result = dict((intents or rows)[0])
    folder = Path(result["report"]).parent
    request_path = folder / "dispatch-request.json"
    if not request_path.exists():
        return result
    begin = time.perf_counter()
    try:
        result["closeout"] = await exchange(pipeline, "reconcile", request_path)
        result["disposition"] = result["closeout"]["status"]
    except Exception as error:
        result.update(disposition="RECONCILIATION_REQUIRED", error=str(error))
    result.update(
        observed_at=str(Timestamp.now()),
        reconciliation_seconds=time.perf_counter() - begin,
    )
    destination = folder / (
        "reconciliation-" + str(receipts.ExecutionId.new()) + ".json"
    )
    result["report"] = str(destination)
    receipts.store(destination, result, schema=receipts.EXECUTION_SCHEMA)
    return result
