# Copyright (c) 2026
# ruff: noqa: S101, D103, PT018, PLC0415, PLR2004 -- synthetic implementation-scope regression
"""Generated programs are scientific data, maintained adapters retain static checks."""

from __future__ import annotations

import asyncio
import json
import sys
from typing import TYPE_CHECKING, Any

from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor
from experiments.codex_dogfood.case_0009.artifacts import ROOT
from experiments.orchestration.storage import load
from experiments.source_grounding.freeze import implementations
from experiments.source_grounding.plan import source_scope, validation_commands
from experiments.source_grounding.workers import command, grounding_observer

if TYPE_CHECKING:
    from pathlib import Path


def test_static_scope_excludes_materialized_generated_payloads(tmp_path: Path) -> None:
    scope = source_scope(implementations())
    for path in (
        "runs/synthetic/PREPARATION/0020/reviewer_codec.py",
        "runs/synthetic/PACKET/0020/stage_c_builder.py",
    ):
        generated = tmp_path / "experiments/source_grounding" / path
        generated.parent.mkdir(parents=True, exist_ok=True)
        generated.write_text("generated=undefined_payload_name\n")
    assert scope == sorted(
        p.relative_to(ROOT).as_posix()
        for p in (ROOT / "experiments/source_grounding").glob("*.py")
    )
    checks = validation_commands(implementations())
    for argv in checks[1:]:
        assert sorted(arg for arg in argv if arg.endswith(".py")) == scope
        assert all("runs/" not in arg and "plans/" not in arg for arg in argv)

    async def run() -> None:
        for argv in checks[1:]:
            result = await CommandExecutor().execute(
                Command(argv[0])
                .args(*argv[1:])
                .cwd(resolve_path(ROOT))
                .with_timeout(Duration.seconds(120)),
            )
            assert result.exit_code == 0, result.stdout + result.stderr

    asyncio.run(run())


def test_maintained_implementation_defect_still_fails(tmp_path: Path) -> None:
    owned = "experiments/source_grounding/plan.py"
    defective = tmp_path / "plan.py"
    defective.write_bytes(
        (ROOT / owned).read_bytes()
        + b"\nknown_static_defect = undefined_maintained_binding\n",
    )
    argv = validation_commands(implementations())[1]
    assert owned in argv
    argv = [str(defective) if a == owned else a for a in argv]

    async def run() -> None:
        result = await CommandExecutor().execute(
            Command(argv[0])
            .args(*argv[1:])
            .cwd(resolve_path(ROOT))
            .with_timeout(Duration.seconds(120)),
        )
        assert result.exit_code != 0
        assert (
            b"F821" in result.stdout
            and b"undefined_maintained_binding" in result.stdout
        )

    asyncio.run(run())


def test_nested_grounding_adapter_bridge_with_fake_process(tmp_path: Path) -> None:
    sterile = tmp_path / "grounding-worker"
    sterile.mkdir()

    async def run() -> None:
        result = await command(
            [sys.executable, "-c", "print('bounded fake worker')"],
            sterile,
            tmp_path / "logs",
            20,
            observer=grounding_observer(sterile),
            metadata={
                "model": "GPT-6 Sol",
                "reasoning": "High",
                "semantic": True,
                "fresh": True,
                "instruction_sha256": "f" * 64,
            },
        )
        assert result.exit_code == 0

    asyncio.run(run())
    events = [
        json.loads(row)
        for row in (tmp_path / "operational.log").read_bytes().splitlines()
    ]
    assert {"QUEUED", "STARTED", "PID", "COMPLETE"} <= {
        event["status"] for event in events
    }
    assert all(
        event["model"] == "GPT-6 Sol" and event["reasoning"] == "High"
        for event in events
    )
    assert next(event for event in events if event["status"] == "PID")["pid"] > 0
    assert not (sterile / "operational.log").exists()
    assert not list(sterile.iterdir())
    assert load(tmp_path / "logs/exit.json")["launch_utc"]


def test_operational_process_completion_does_not_define_burden_interval() -> None:
    from experiments.source_grounding.timing import summarize

    events: list[Any] = [
        {"case": "synthetic", "stage": "B", "status": "RUNNING", "elapsed_seconds": 1},
        {
            "case": "synthetic",
            "stage": "B",
            "status": "COMPLETE",
            "worker_type": "OPERATIONAL",
            "elapsed_seconds": 3,
            "duration_seconds": 2,
        },
    ]
    assert summarize(events)["branch_critical_path_seconds"]["B"] is None
    events.append(
        {
            "case": "synthetic",
            "stage": "B",
            "status": "COMPLETE",
            "elapsed_seconds": 5,
            "duration_seconds": 4,
        },
    )
    assert summarize(events)["worker_seconds"]["synthetic/B"] == 4
