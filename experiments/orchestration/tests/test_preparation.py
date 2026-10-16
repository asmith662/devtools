# Copyright (c) 2026
# ruff: noqa: PLR2004, S101, PT018, COM812, PLR0915 -- isolated authenticated checkout fixture
"""Exercise real target-owned validation/preflight/budget without scientific entry."""

from __future__ import annotations

import asyncio
import importlib.util
import shutil
import sys
from pathlib import Path
from typing import Any

from devtools.core.time import Timestamp
from devtools.observability.usage.storage import save as save_observations
from devtools.orchestration.experiments import ExperimentExecutionPipeline, receipts
from devtools.orchestration.experiments.pipeline import target_python
from devtools.resources.commands import Command, CommandExecutor
from experiments.codex_dogfood.case_0009.artifacts import digest
from experiments.orchestration.controller import PACKAGE, implementation
from experiments.orchestration.model import RunPlan
from experiments.orchestration.storage import save
from experiments.orchestration.tests.test_controller import fixture


async def checkout(
    tmp_path: Path, *, startup_success: bool = True
) -> tuple[ExperimentExecutionPipeline, Any]:
    """Build a committed main checkout with its own installed source/environment."""
    root = tmp_path / "target"
    controller = await fixture(root, tmp_path / "unused-work", approved=False)
    repo = controller.repository
    source = PACKAGE.parents[1]
    shutil.copytree(
        source / "src/devtools",
        root / "src/devtools",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    for address in implementation():
        destination = root / "experiments/orchestration" / address
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(PACKAGE / address, destination)
    for address in (
        "experiments/codex_dogfood/case_0009/artifacts.py",
        "experiments/structural_discrimination/stage_c/validate_packet.py",
    ):
        destination = root / address
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / address, destination)
    (root / ".gitignore").write_text(".local/\n.venv/\n__pycache__/\n")
    script = root / "worker.py"
    script.write_text(
        "import sys\n"
        'if sys.argv[1:] == ["--help"]:\n'
        '    print("usage: harmless fixture")\n'
        "else:\n"
        '    raise RuntimeError("SCIENTIFIC DISPATCH FORBIDDEN")\n',
    )
    if not startup_success:
        script.write_text('raise RuntimeError("synthetic startup failure")\n')
    value = controller.value
    value["semantic"]["model_id"] = "fixture-primary"
    value["implementation"]["worker.py"] = digest(script.read_bytes())
    value["worker_entrypoints"] = {
        "schema": "python-worker-entrypoint-preflight-v1",
        "mode": "DIRECT_SCRIPT_HELP",
        "timeout_seconds": 10,
        "scripts": {"worker.py": digest(script.read_bytes())},
    }
    calls = {
        c["id"] + "/C": {
            "model": "fixture-primary",
            "input_upper": 100,
            "output_upper": 20,
        }
        for c in value["cases"]
    }
    value["usage_budget"] = {
        "fresh_call_limit": 3,
        "model_call_limits": {"fixture-primary": 3},
        "calls": calls,
        "authorization": "EXACT_PLAN_EXECUTION_APPROVAL",
    }
    value["economics"]["calls"] = [
        {
            "invocation": k,
            "model": v["model"],
            "reasoning_effort": "high",
            "input_tokens": {"upper": 100},
            "output_tokens": {"upper": 20},
        }
        for k, v in calls.items()
    ]
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
    await repo.git("commit", "-m", "Synthetic preparation-only Stage A and target code")
    value["stage_a"]["checkpoint"] = (
        (await repo.git("rev-parse", "HEAD")).decode().strip()
    )
    value["stage_a"]["protocol"]["sha256"] = digest(
        (root / "protocol.json").read_bytes(),
    )
    (root / "plan.json").write_bytes(RunPlan.parse(value).canonical)
    await repo.git("add", "plan.json")
    await repo.git("commit", "-m", "Synthetic unapproved preparation plan")
    environment = await CommandExecutor().execute(
        Command(sys.executable).args(
            "-m", "venv", "--without-pip", str(root / ".venv")
        ),
    )
    assert environment.succeeded
    python = target_python(root)
    site = next((root / ".venv").glob("**/site-packages"))
    (site / "devtools.pth").write_text(str(root / "src") + "\n")
    tzdata = importlib.util.find_spec("tzdata")
    assert tzdata is not None and tzdata.origin is not None
    shutil.copytree(Path(tzdata.origin).parent, site / "tzdata")
    save_observations(root / ".local/usage/ledger.json", ())
    save(root / ".local/usage/backfill.json", {"observed_at": str(Timestamp.now())})
    save(
        root / ".local/usage/policy.json",
        {
            "limits": [
                {
                    "scope": "OBSERVED_WINDOW",
                    "identity": "local",
                    "limits": {
                        "fresh_calls": 3,
                        "input_tokens": 300,
                        "output_tokens": 60,
                    },
                },
            ],
        },
    )
    return ExperimentExecutionPipeline(root, tmp_path / "receipts", python), repo


def test_authenticated_preparation_and_safety(tmp_path: Path) -> None:
    """Actual subprocesses use the target, preserve it and reject unsafe states."""

    async def run() -> None:
        subject, repo = await checkout(tmp_path)
        before = (
            await repo.git("rev-parse", "HEAD"),
            await repo.git("status", "--porcelain"),
        )
        local = {
            p.name: p.read_bytes() for p in (subject.target / ".local/usage").iterdir()
        }
        result = await subject.prepare(Path("plan.json"))
        assert result["disposition"] == "READY_FOR_APPROVAL", result
        assert result["validation"]["worker_entrypoint_preflight"]["status"] == "PASS"
        assert result["validation"]["worker_entrypoint_preflight"]["model_calls"] == 0
        assert receipts.latest(subject.receipt_root, "plan.json") == result
        assert result["validation"]["usage_budget"]["fresh_call_limit"] == 3
        assert before == (
            await repo.git("rev-parse", "HEAD"),
            await repo.git("status", "--porcelain"),
        )
        assert local == {
            p.name: p.read_bytes() for p in (subject.target / ".local/usage").iterdir()
        }
        assert not (subject.target / "experiments/orchestration/runs").exists()
        plan_path = subject.target / "plan.json"
        plan_bytes = plan_path.read_bytes()
        plan_path.write_bytes(plan_bytes + b" ")
        assert (await subject.prepare(Path("plan.json")))[
            "disposition"
        ] == "PLAN_INVALID_OR_INCOMPATIBLE"
        plan_path.write_bytes(plan_bytes)
        # Full-inventory refusal occurs before any reservation or scientific claim.
        local_root = subject.target / ".local/usage"
        save(
            local_root / "policy.json",
            {
                "limits": [
                    {
                        "scope": "OBSERVED_WINDOW",
                        "identity": "local",
                        "limits": {
                            "fresh_calls": 2,
                            "input_tokens": None,
                            "output_tokens": None,
                        },
                    }
                ]
            },
        )
        refused = await subject.prepare(Path("plan.json"))
        assert refused["disposition"] == "BUDGET_REJECTED", refused
        assert not (local_root / "reservations.json").exists()
        ledger = (local_root / "ledger.json").read_bytes()
        (local_root / "ledger.json").unlink()
        missing = await subject.prepare(Path("plan.json"))
        assert missing["disposition"] == "EVIDENCE_UNAVAILABLE", missing
        assert missing["usage"]["observation"] is None
        (local_root / "ledger.json").write_bytes(ledger)
        # Existing runs, including dead history, require controller reconciliation.
        run_record = (
            subject.target
            / "experiments/orchestration/runs"
            / result["validation"]["run_id"]
            / "run.json"
        )
        save(run_record, {"synthetic": "DEAD; DO_NOT_RETRY"})
        await repo.git("add", ".")
        await repo.git("commit", "-m", "Synthetic existing dead run record")
        dead = await subject.prepare(Path("plan.json"))
        assert dead["disposition"] == "PLAN_INVALID_OR_INCOMPATIBLE", dead
        assert "reconciliation" in str(dead["error"])
        run_record.unlink()
        await repo.git("add", "-u")
        await repo.git(
            "commit",
            "-m",
            "Remove synthetic run marker for independent supersession check",
        )
        orphan = await subject.prepare(Path("plan.json"))
        assert orphan["disposition"] == "PLAN_INVALID_OR_INCOMPATIBLE", orphan
        assert "reconciliation" in str(orphan["error"])
        # A dirty source cannot be substituted for the authenticated target.
        script = subject.target / "worker.py"
        original = script.read_bytes()
        script.write_bytes(b"raise RuntimeError('never run')\n")
        assert (await subject.prepare(Path("plan.json")))[
            "disposition"
        ] == "PLAN_INVALID_OR_INCOMPATIBLE"
        script.write_bytes(original)
        # Supersession is enforced by the controller rather than copied policy.
        run_id = result["validation"]["run_id"]
        marker = (
            subject.target
            / "experiments/orchestration/supersessions"
            / (run_id + ".json")
        )
        save(marker, {"synthetic": True})
        await repo.git("add", ".")
        await repo.git("commit", "-m", "Synthetic supersession")
        blocked = await subject.prepare(Path("plan.json"))
        assert blocked["disposition"] == "PLAN_INVALID_OR_INCOMPATIBLE"
        assert "Superseded" in str(blocked["error"])
        # Wrong environment never imports feature framework as target-equivalent.
        wrong = ExperimentExecutionPipeline(
            subject.target,
            tmp_path / "other-receipts",
            Path(sys.executable),
        )
        incompatible = await wrong.prepare(Path("plan.json"))
        assert incompatible["disposition"] == "PLAN_INVALID_OR_INCOMPATIBLE"
        assert "another checkout" in str(incompatible["error"])

    asyncio.run(run())


def test_real_startup_failure(tmp_path: Path) -> None:
    """The existing worker gate refuses a bound but non-starting script."""

    async def run() -> None:
        subject, _repo = await checkout(tmp_path, startup_success=False)
        result = await subject.prepare(Path("plan.json"))
        assert result["disposition"] == "STARTUP_PREFLIGHT_FAILED", result
        assert result["scientific_dispatches"] == 0

    asyncio.run(run())
