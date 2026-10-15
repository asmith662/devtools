# Copyright (c) 2026
# ruff: noqa: S101, D103, PLR2004, PLC0415, ASYNC240, FBT001, PLR0913 -- synthetic engineering fixtures
"""Prove fixed cohort infrastructure without scientific workers or network models."""

from __future__ import annotations

import asyncio
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Any

import pytest

from experiments.codex_dogfood.case_0009.artifacts import digest
from experiments.orchestration import isolation
from experiments.orchestration.authority import ApprovalRequest
from experiments.orchestration.cache import PreparationCache
from experiments.orchestration.controller import Controller, implementation
from experiments.orchestration.model import RunPlan, validation_tier
from experiments.orchestration.publication import Repository
from experiments.orchestration.storage import exclusive, load, save
from experiments.orchestration.workers.codex import argv
from experiments.orchestration.workers.process import invoke


class FixtureController(Controller):
    """Only the synthetic repository replaces devtools final validation commands."""

    async def checkpoint_validation(
        self,
        boundary: str,
        paths: tuple[str, ...],
    ) -> None:
        """Exercise fixture validators in place of a nonexistent framework."""
        from experiments.orchestration.controller import expand

        tier = validation_tier(boundary, paths)
        for command_argv in self.value["validation"][tier]:
            await self.process(
                expand(
                    command_argv,
                    {"python": sys.executable, "repository": str(self.repository.root)},
                ),
                self.repository.root,
                "cohort",
                boundary + "-" + tier,
                "validation",
            )


async def fixture(
    root: Path,
    work: Path,
    *,
    concurrency: int = 6,
    fault: str = "",
    approved: bool = True,
    attempt: int = 1,
) -> Controller:
    root.mkdir()
    repo = Repository(root, push=False)
    await repo.git("init", "-b", "main")
    await repo.git("config", "core.autocrlf", "false")
    await repo.git("config", "user.email", "fixture@example.invalid")
    await repo.git("config", "user.name", "Synthetic fixture")
    (root / ".gitignore").write_text(".local/\n", encoding="utf-8")
    script = root / "worker.py"
    script.write_bytes(Path(__file__).with_name("worker.py").read_bytes())
    (root / "protocol.json").write_bytes(b'{"fixture":true}\n')
    (root / "integrity.json").write_bytes(b'{"fixture":true}\n')
    cases = []
    for case in ("alpha", "beta", "gamma"):
        path = root / (case + ".txt")
        path.write_text(case, encoding="utf-8")
        cases.append(
            {
                "id": case,
                "frame": {
                    "repository_id": "fixture-repository",
                    "snapshot_id": case + "-snapshot",
                    "corpus_id": case + "-corpus",
                    "parent_tree": "immutable-" + case,
                },
                "inputs": [
                    {
                        "path": path.name,
                        "name": "task.txt",
                        "sha256": digest(path.read_bytes()),
                    },
                ],
            },
        )
    await repo.git("add", ".")
    await repo.git("commit", "-m", "Approved fake Stage A")
    stage_a = (await repo.git("rev-parse", "HEAD")).decode().strip()
    command = ["{python}", "-B", "{repository}/worker.py"]
    stages = ("prepare", "packet", "B", "import", "D")
    commands = {
        stage: [*command, "run", stage, "{case}", "{frame}"] for stage in stages
    }
    commands.update(
        {
            stage + "_validate": [*command, "validate", stage, "{case}", "{frame}"]
            for stage in stages
        },
    )
    commands["packet_validate"] = [*command, "check", "packet", "{case}", "{frame}"]
    commands["C_validate"] = [*command, "validate", "C", "{case}", "{frame}"]
    check = [*command, "check", "validation", "cohort", "{}"]
    value: dict[str, Any] = {
        "schema": "experiment-controller-plan-v2",
        "economics": {
            "schema": "semantic-economics-forecast-v1",
            "fresh_calls": 3,
            "provenance": "SYNTHETIC_NO_MODELS",
        },
        "name": "synthetic-three-case",
        "attempt": attempt,
        "stage_a": {
            "checkpoint": stage_a,
            "protocol": {
                "path": "protocol.json",
                "sha256": digest((root / "protocol.json").read_bytes()),
            },
            "integrity": {
                "path": "integrity.json",
                "sha256": digest((root / "integrity.json").read_bytes()),
            },
        },
        "cases": cases,
        "commands": commands,
        "semantic": {
            "kind": "process",
            "model": "fixture-primary",
            "reasoning": "high",
            "prompt_file": "README.md",
            "argv": [*command, "run", "C", "{case}", "{frame}"],
            "environment_allowlist": ["PATH", "SystemRoot", "TEMP", "TMP"],
        },
        "publication": {
            "root": "experiments/orchestration/runs",
            "remote": "origin",
            "branch": "main",
            "push": False,
            "subjects": {b: "Fixture " + b for b in ("PACKET", "B", "C", "D")},
        },
        "validation": {"local": [check], "checkpoint": [check], "final": [check]},
        "concurrency": {"cases": 3, "semantic": 3, "workers": concurrency},
        "timeouts": {"worker": 15, "validation": 15, "grace": 0.1},
        "retry": "NEVER_SCIENTIFIC",
        "implementation": {"worker.py": digest(script.read_bytes())},
        "controller_implementation": implementation(),
        "cache": {
            "enabled": True,
            "observation_semantics": "fake-observation-v1",
            "configuration": {},
            "surfaces": ["frame.json"],
        },
    }
    for frozen_command in value["commands"].values():
        frozen_command.append(fault)
    value["semantic"]["argv"].append(fault)
    plan = RunPlan.parse(value)
    (root / "plan.json").write_bytes(plan.canonical)
    await repo.git("add", ".")
    await repo.git("commit", "-m", "Publish unapproved fixture plan")
    controller = await FixtureController.from_plan(root, "plan.json", work)
    if approved:
        await controller.approve(
            ApprovalRequest(
                controller.run_id,
                "fixture",
                "explicit synthetic host grant",
            ),
        )
    return controller


def test_three_case_integration(tmp_path: Path) -> None:
    async def run() -> None:
        controller = await fixture(
            tmp_path / "repository",
            tmp_path / "work",
            approved=False,
        )
        identity = controller.run_id
        assert controller.plan_report()["execution_authorized"] == "NO"
        assert controller.status()["status"] == "PLANNED"
        with pytest.raises(ValueError, match="authorization value"):
            await controller.run()
        assert not list(controller.science.glob("journal/*/*/ENTERED.json"))
        grant = ApprovalRequest(identity, "fixture", "explicit integration approval")
        await controller.approve(grant)
        assert controller.run_id == identity
        assert controller.status()["status"] == "APPROVED"
        start = time.perf_counter()
        result = await controller.run(await controller.execution_authorization())
        assert result["status"] == "COMPLETE; MAINTAINER_REVIEW_READY", result
        assert set(result["publications"]) == {"PACKET", "B", "C", "D"}
        assert not await controller.repository.git("status", "--porcelain=v1")
        records = [
            load(p) for p in controller.science.glob("journal/*/*/RETURNED.json")
        ]
        assert len(records) == 16
        assert all(r["validation"]["status"] == "PASS" for r in records)
        assert controller.status()["status"].startswith("COMPLETE")
        save(
            tmp_path / "measurement.json",
            {
                "runtime_seconds": time.perf_counter() - start,
                "publications": result["publications"],
            },
        )
        # Removing replaceable operational state cannot cause scientific re-execution.
        assert controller.operational.resolve().is_relative_to(tmp_path.resolve())
        assert controller.work_root.resolve().is_relative_to(tmp_path.resolve())
        shutil.rmtree(controller.operational)
        shutil.rmtree(controller.work_root)
        restarted = FixtureController(
            controller.repository,
            controller.plan,
            controller.work_root,
        )
        resumed = await restarted.run(
            await restarted.execution_authorization(),
            resume=True,
        )
        assert resumed["status"].startswith("COMPLETE"), resumed
        # Corrupt handoff/progress cannot change authenticated scientific status.
        (restarted.operational / "state.json").write_bytes(
            b"corrupt operational status",
        )
        assert (await restarted.verify())["verification"] == "PASS"
        result = await invoke(
            [
                sys.executable,
                "-m",
                "experiments.orchestration",
                "verify",
                controller.run_id,
                "--repository",
                str(controller.repository.root),
            ],
            Path(__file__).resolve().parents[3],
            controller.environment(),
            30,
            0.1,
            tmp_path / "cli-verify",
        )
        assert result.exit_code == 0, result.stderr
        import json

        assert json.loads(result.stdout)["verification"] == "PASS"
        receipt_path = controller.journal("alpha", "B", "RETURNED")
        altered = load(receipt_path)
        altered["files"] = {}
        save(receipt_path, altered)
        await controller.repository.git(
            "add",
            "--",
            str(receipt_path.relative_to(controller.repository.root)),
        )
        await controller.repository.git(
            "commit",
            "-m",
            "Fixture malicious journal edit",
        )
        with pytest.raises(ValueError, match="output list missing"):
            await restarted.verify()
        assert len(tuple(controller.science.glob("journal/*/*/ENTERED.json"))) == 16

    asyncio.run(run())


def test_plan_identity_and_authentication(tmp_path: Path) -> None:
    async def run() -> None:
        controller = await fixture(tmp_path / "repository", tmp_path / "work")
        assert controller.plan.identity(implementation()) == controller.run_id
        changed = controller.plan.value
        changed["attempt"] += 1
        assert RunPlan.parse(changed).identity(implementation()) != controller.run_id
        changed["retry"] = "AUTOMATIC"
        with pytest.raises(ValueError, match="retry"):
            RunPlan.parse(changed)
        save(controller.repository.root / "protocol.json", {"altered": True})
        with pytest.raises(ValueError, match=r"tracked|approval"):
            await Controller.from_plan(
                controller.repository.root,
                "plan.json",
                tmp_path / "other",
            )

    asyncio.run(run())


def test_sterile_boundaries(tmp_path: Path) -> None:
    files = {"README.md": b"case alpha only\n", "manifest.json": b'{"case":"alpha"}\n'}
    isolation.sterile(tmp_path / "alpha", files)
    isolation.preserve_packet(tmp_path / "alpha", files)
    with pytest.raises(ValueError, match="exists"):
        isolation.sterile(tmp_path / "alpha", files)
    with pytest.raises(ValueError, match=r"Treatment|metadata"):
        isolation.sterile(tmp_path / "leaked", {"manifest.json": b'{"rank":1}\n'})
    (tmp_path / "alpha/README.md").write_bytes(b"mutation")
    with pytest.raises(ValueError, match="mutation"):
        isolation.preserve_packet(tmp_path / "alpha", files)


def test_cache(tmp_path: Path) -> None:
    cache = PreparationCache(tmp_path)
    binding = {
        "schema": "v1",
        "parent_tree": "tree",
        "repository_id": "repo",
        "observation_semantics": "observed-v1",
        "implementation": {"producer": "sha"},
        "configuration": {},
        "surfaces": ["frame.json"],
    }
    assert cache.get(binding) == ("CACHE_MISS", None)
    cache.put(binding, {"frame.json": b"{}\n"})
    assert cache.get(binding) == ("CACHE_HIT", {"frame.json": b"{}\n"})
    (tmp_path / (cache.key(binding) + ".json")).write_bytes(b"corrupt")
    assert cache.get(binding) == ("CACHE_REJECTED", None)
    different = {**binding, "implementation": {"producer": "new"}}
    assert cache.key(binding) != cache.key(different)
    assert cache.get(different) == ("CACHE_MISS", None)


def test_codex_fresh_command(tmp_path: Path) -> None:
    from experiments.orchestration.workers import runtime

    config = {
        "model_id": "frozen-account-model",
        "reasoning": "high",
        "prompt_file": "README.md",
        "executable": "codex-fixture",
        "runtime": runtime.configuration(),
    }
    command = argv(
        config,
        tmp_path,
        schema=tmp_path.parent / "schema.json",
        response=tmp_path.parent / "response.txt",
    )
    assert "resume" not in command
    assert "fork" not in command
    assert "--ephemeral" in command
    assert "--ignore-user-config" in command
    assert command[command.index("--model") + 1] == "frozen-account-model"
    assert str(tmp_path) == command[command.index("--cd") + 1]
    assert command[-1] == "-"
    assert "features.shell_tool=false" in command


@pytest.mark.parametrize(
    ("boundary", "paths", "tier"),
    [
        ("LOCAL", (), "local"),
        ("PACKET", ("experiments/example/a.json",), "checkpoint"),
        ("B", ("src/devtools/test.py",), "final"),
        ("D", (), "final"),
    ],
)
def test_validation_tier(boundary: str, paths: tuple[str, ...], tier: str) -> None:
    assert validation_tier(boundary, paths) == tier


@pytest.mark.parametrize("entered", [False, True])
def test_resume_boundary(tmp_path: Path, entered: bool) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repository", tmp_path / "work")
        exclusive(
            c.science / "run.json",
            {
                "run_id": c.run_id,
                "plan": c.value,
                "implementation": implementation(),
                "approval_checkpoint": c.approved_head,
            },
        )
        if entered:
            exclusive(c.journal("alpha", "prepare", "ENTERED"), {"run_id": c.run_id})
        result = await c.run(await c.execution_authorization(), resume=True)
        assert result["status"].startswith("BLOCKED" if entered else "COMPLETE"), result

    asyncio.run(run())


def test_process_timeout_and_nonzero(tmp_path: Path) -> None:
    async def run() -> None:
        environment = {
            n: os.environ[n]
            for n in ("PATH", "SystemRoot", "TEMP", "TMP")
            if n in os.environ
        }
        result = await invoke(
            [sys.executable, "-c", "raise SystemExit(3)"],
            tmp_path,
            environment,
            3,
            0.1,
            tmp_path / "nonzero",
        )
        assert result.exit_code != 0
        result = await invoke(
            [sys.executable, "-c", "import time; time.sleep(20)"],
            tmp_path,
            environment,
            0.15,
            0.1,
            tmp_path / "timeout",
        )
        assert result.exit_code != 0
        assert load(tmp_path / "timeout/child.json")["pid"] > 0

    asyncio.run(run())


def test_main_advancement(tmp_path: Path) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repository", tmp_path / "work")
        await c.repository.git(
            "commit",
            "--allow-empty",
            "-m",
            "Maintainer advancement",
        )
        with pytest.raises(ValueError, match="advancement"):
            await c.repository.authenticate(c.approved_head)

    asyncio.run(run())
