# Copyright (c) 2026
# ruff: noqa: ASYNC240, ASYNC230, E501, PLR0915 -- bounded read-only experiment status viewer
"""Read historical/current run identities and tail operational observations only."""

from __future__ import annotations

import asyncio
import json
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.authority import authenticate
from experiments.orchestration.model import RunPlan
from experiments.orchestration.observation import read_snapshot
from experiments.orchestration.publication import Repository
from experiments.orchestration.storage import binary, load, no_links, require, safe

if TYPE_CHECKING:
    from experiments.orchestration.observation import Console


async def snapshot(root: Path, run_id: str) -> dict[str, Any]:
    """Authenticate original bindings without requiring current executable bytes."""
    require(re.fullmatch(r"[0-9a-f]{64}", run_id), "Invalid run identity")
    operational = root / ".local/experiment-runs" / run_id
    no_links(operational)
    prefix = load(operational / "locator.json")["prefix"]
    science = safe(root, prefix)
    repo = Repository(root, push=False)
    context_path = science / "run.json"
    archived = False
    if not context_path.exists():
        archive = root / ".local/experiment-failures" / run_id
        no_links(archive)
        registration_path = (
            "experiments/orchestration/engineering/observability/failed-run.json"
        )
        registration_raw = await repo.git("show", "HEAD:" + registration_path)
        require(
            registration_raw == binary(safe(root, registration_path)),
            "Uncommitted preservation record",
        )
        registration = json.loads(registration_raw)
        require(
            registration["run_id"] == run_id
            and digest(binary(archive / "manifest.json"))
            == registration["manifest_sha256"],
            "Forensic manifest registration differs",
        )
        manifest = load(archive / "manifest.json")
        # A forensic copy locates historical bytes; the approved plan independently authenticates identity.
        entries = manifest["entries"] if isinstance(manifest, dict) else manifest
        context_path = archive / "repository-candidates" / prefix / "run.json"
        entry = next(
            e
            for e in entries
            if e["original_path"].endswith("/" + prefix + "/run.json")
        )
        require(
            digest(binary(context_path)) == entry["sha256"],
            "Archived run bytes differ",
        )
        science = context_path.parent
        archived = True
    context = load(context_path)
    plan = RunPlan.parse(context["plan"])
    require(
        context["run_id"] == run_id == plan.identity(context["implementation"]),
        "Run identity differs",
    )
    require(
        context["implementation"] == plan.value["controller_implementation"],
        "Recorded controller binding differs",
    )
    approval_path = prefix + "/authorization/approval.json"
    checkpoint = context["approval_checkpoint"]
    raw = await repo.git("show", checkpoint + ":" + approval_path)
    require(raw == binary(safe(root, approval_path)), "Approval bytes changed")
    approval = json.loads(raw)
    require(raw == json_bytes(approval), "Noncanonical approval")
    binding = {
        k: approval[k] for k in ("plan_path", "plan_checkpoint", "review_checkpoint")
    }
    binding.update(
        plan_sha256=digest(plan.canonical),
        run_id=run_id,
        stage_a_checkpoint=plan.value["stage_a"]["checkpoint"],
        controller_sha256=digest(json_bytes(context["implementation"])),
    )
    authenticate(approval, binding)
    require(
        await repo.git(
            "show",
            approval["plan_checkpoint"] + ":" + approval["plan_path"],
        )
        == plan.canonical,
        "Approved plan bytes differ",
    )
    require(
        (await repo.git("rev-parse", checkpoint + "^")).decode().strip()
        == approval["review_checkpoint"],
        "Approval parent differs",
    )
    receipt_path = prefix + "/authorization/publications/APPROVAL.json"
    receipt_raw = await repo.git("show", checkpoint + ":" + receipt_path)
    require(
        receipt_raw == binary(safe(root, receipt_path))
        and json.loads(receipt_raw)
        == {
            "boundary": "APPROVAL",
            "parent_head": approval["review_checkpoint"],
            "sha256": {"approval.json": digest(raw)},
        },
        "Approval receipt differs",
    )
    await repo.git("merge-base", "--is-ancestor", checkpoint, "HEAD")
    stages: dict[str, str] = {}
    cases = {case.identity: case for case in plan.cases}
    for entered in science.glob("journal/*/*/ENTERED.json"):
        value = load(entered)
        require(
            value["run_id"] == run_id
            and value["case"] in cases
            and value["frame"] == cases[value["case"]].frame,
            "Journal binding differs",
        )
        stage = value["stage"]
        require(
            entered.parent.name == stage
            and entered.parent.parent.name == value["case"],
            "Journal address differs",
        )
        returned, failed = (
            entered.with_name("RETURNED.json"),
            entered.with_name("FAILED.json"),
        )
        if returned.exists():
            completed = load(returned)
            require(
                all(
                    completed[k] == value[k]
                    for k in (
                        "run_id",
                        "case",
                        "stage",
                        "frame",
                        "inputs_sha256",
                        "workspace",
                    )
                ),
                "Return binding differs",
            )
        stages[value["case"] + "/" + stage] = (
            "DEAD"
            if failed.exists()
            else "COMPLETE"
            if returned.exists()
            else "ENTERED; RECOVERY_REQUIRES_PROOF"
        )
    publications: dict[str, str] = {}
    blocked: list[str] = []
    for marker in (science / "publications").glob("*.json"):
        address = prefix + "/publications/" + marker.name
        commit = (
            (await repo.git("log", "-1", "--format=%H", "--", address)).decode().strip()
        )
        if not commit:
            blocked.append("UNCOMMITTED_PUBLICATION:" + marker.stem)
            continue
        require(
            await repo.git("show", commit + ":" + address) == binary(marker),
            "Publication receipt differs",
        )
        receipt = load(marker)
        require(
            receipt["boundary"] == marker.stem
            and (await repo.git("rev-parse", commit + "^")).decode().strip()
            == receipt["parent_head"],
            "Publication parent differs",
        )
        for name, sha in receipt["sha256"].items():
            artifact = safe(root, prefix + "/" + name)
            require(
                digest(await repo.git("show", commit + ":" + prefix + "/" + name))
                == sha
                == digest(binary(artifact)),
                "Published artifact differs",
            )
        publications[marker.stem] = commit
    state: Any = (
        read_snapshot(operational / "state.json")
        if (operational / "state.json").exists()
        else {}
    )
    status = (
        "COMPLETE; MAINTAINER_REVIEW_READY"
        if "D" in publications
        else "RUNNING_OR_INTERRUPTED"
    )
    if (
        blocked
        or "DEAD" in stages.values()
        or str(state.get("status", "")).startswith("BLOCKED")
    ):
        status = "BLOCKED; MAINTAINER_DECISION_REQUIRED"
    return {
        "run_id": run_id,
        "status": status,
        "approval_checkpoint": checkpoint,
        "historical_approval_only": archived,
        "execution_authorized": "NOT_GRANTED_BY_STATUS",
        "stages": stages,
        "publications": publications,
        "publication_blockers": blocked,
        "operational_non_authoritative": state,
        "progress_log": str(operational / "progress.log"),
        "log_root": str(operational / "logs"),
        "archived": archived,
    }


async def follow(
    root: Path,
    run_id: str,
    console: Console,
    *,
    interval: float = 1.0,
) -> dict[str, Any]:
    """Tail read-only until terminal; cancellation detaches only this coroutine."""
    initial = await snapshot(root, run_id)
    console.emit(
        {
            "operation": "status",
            "status": initial["status"],
            "snapshot": initial,
            "workspace": initial["log_root"],
            "operation_progress": initial["stages"],
        },
    )
    path = Path(initial["progress_log"])
    offset = 0
    pending = b""
    while True:
        if path.exists():
            no_links(path)
            with path.open("rb") as stream:
                if path.stat().st_size < offset:
                    offset, pending = 0, b""
                stream.seek(offset)
                raw = stream.read(1 << 20)
                offset = stream.tell()
            rows = (pending + raw).split(b"\n")
            pending = rows.pop()[-65536:]
            for row in rows:
                try:
                    event = json.loads(row)
                    if isinstance(event, dict):
                        console.emit(event)
                except ValueError:
                    pass
        state = (
            read_snapshot(path.parent / "state.json")
            if (path.parent / "state.json").exists()
            else {}
        )
        # Active publication candidates are shown blocked, but a live viewer waits
        # while the supervisor reports RUNNING; that observation cannot permit resume.
        if (
            str(state.get("status", "")).startswith(("COMPLETE", "BLOCKED"))
            or initial["archived"]
            or "DEAD" in initial["stages"].values()
            or (
                initial["status"].startswith(("COMPLETE", "BLOCKED"))
                and state.get("status") != "RUNNING"
            )
        ):
            result = await snapshot(root, run_id)
            console.emit(
                {"operation": "status", "status": result["status"], "snapshot": result},
            )
            return result
        await asyncio.sleep(interval)
