# Copyright (c) 2026
# ruff: noqa: S101, D103, ANN401, PLC0415, PT018, E501, TRY003, EM101 -- bounded fake-worker observability fixtures
"""Operational visibility without a semantic model or scientific treatment."""

from __future__ import annotations

import asyncio
import json
import os
import sys
from typing import TYPE_CHECKING, Any

import pytest

from experiments.orchestration.follow import follow, snapshot
from experiments.orchestration.observation import Console, observed_wait, sanitized
from experiments.orchestration.storage import load, save
from experiments.orchestration.tests.test_controller import FixtureController, fixture
from experiments.orchestration.workers.process import invoke

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize("exit_code", [0, 7])
def test_live_process_streams_pid_heartbeat_and_failure(
    tmp_path: Path,
    capsys: Any,
    exit_code: int,
) -> None:
    async def run() -> None:
        events: list[dict[str, Any]] = []
        console = Console()

        def observe(event: dict[str, Any]) -> None:
            events.append(event)
            console.emit({"case": "0020", "stage": "B", **event})

        task = asyncio.create_task(
            invoke(
                [
                    sys.executable,
                    "-c",
                    "import time,sys; print('live-first',flush=True); print('diagnostic',file=sys.stderr,flush=True); time.sleep(0.7); print('last'); sys.exit("
                    + str(exit_code)
                    + ")",
                ],
                tmp_path,
                {
                    k: os.environ[k]
                    for k in ("PATH", "SystemRoot", "TEMP", "TMP")
                    if k in os.environ
                },
                10,
                0.2,
                tmp_path / "logs",
                observer=observe,
                heartbeat_seconds=0.15,
                metadata={
                    "operation": "grounding",
                    "model": "GPT-6 Sol",
                    "reasoning": "High",
                    "semantic": True,
                    "fresh": True,
                    "process_role": "source grounding",
                    "instruction_sha256": "a" * 64,
                },
            ),
        )
        for _ in range(200):
            await asyncio.sleep(0.01)
            path = tmp_path / "logs/stdout.log"
            if path.exists() and b"live-first" in path.read_bytes():
                break
        assert not task.done(), "Logs must be visible before process exit"
        assert b"diagnostic" in (tmp_path / "logs/stderr.log").read_bytes()
        result = await task
        assert result.exit_code == exit_code
        assert result.stdout == (tmp_path / "logs/stdout.log").read_bytes()
        assert result.stderr == (tmp_path / "logs/stderr.log").read_bytes()
        assert {
            "QUEUED",
            "STARTED",
            "PID",
            "HEARTBEAT",
            "FAILED" if exit_code else "COMPLETE",
        } <= {e["status"] for e in events}
        heartbeat = next(
            e for e in events if e["status"] == "HEARTBEAT" and e.get("pid")
        )
        assert heartbeat["timeout_remaining_seconds"] > 0
        assert heartbeat["output_idle_seconds"] >= 0
        state = load(tmp_path / "logs/exit.json")
        assert (
            state["launch_utc"] and state["exit_utc"] and state["duration_seconds"] > 0
        )
        assert state["failure_category"] == ("NONZERO_EXIT" if exit_code else None)

    asyncio.run(run())
    output = capsys.readouterr()
    assert not output.out
    assert "GPT-6 Sol" in output.err and 'reasoning="High"' in output.err
    assert "stdout_path=" in output.err and "pid=" in output.err
    if exit_code:
        assert (
            "=== FAILED ===" in output.err
            and "diagnostic" in output.err
            and "exit_code=7" in output.err
        )


def test_sanitized_prompt_identity_is_stable() -> None:
    argv = ["codex", "exec", "--model", "frozen", "private prompt body"]
    safe = sanitized(argv)
    assert "private prompt body" not in repr(safe)
    assert safe == sanitized(safe)


def test_nested_semantic_bridge_is_operational(tmp_path: Path, capsys: Any) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work")
        c.reporter = Console()
        workspace = tmp_path / "bridge"
        workspace.mkdir()
        events = [
            {
                "status": state,
                "operation": "grounding",
                "process_role": "source grounding",
                "model": "GPT-6 Sol",
                "reasoning": "High",
                "semantic": True,
                "pid": 1234,
                "instruction_sha256": "b" * 64,
                "workspace": str(workspace / "sterile"),
                "authority": "forged",
            }
            for state in ("QUEUED", "STARTED", "PID", "HEARTBEAT", "COMPLETE")
        ]
        code = (
            "from pathlib import Path; import time; Path('operational.log').write_text("
            + repr("".join(json.dumps(e) + "\n" for e in events))
            + "); time.sleep(0.3)"
        )
        await c.process([sys.executable, "-c", code], workspace, "alpha", "B")
        assert not c.journal("alpha", "B", "ENTERED").exists()
        assert "authority" not in repr(c.state["semantic_processes"])
        assert c.semantic_summary()["Sol_launched"]
        assert not c.semantic_summary()["B_entered"]

    asyncio.run(run())
    output = capsys.readouterr()
    assert "source grounding" in output.err and "GPT-6 Sol" in output.err


def test_uncommitted_publication_is_blocked_and_follow_detaches(
    tmp_path: Path,
    capsys: Any,
) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work")
        save(
            c.science / "run.json",
            {
                "run_id": c.run_id,
                "plan": c.value,
                "implementation": c.value["controller_implementation"],
                "approval_checkpoint": c.approved_head,
            },
        )
        save(c.operational / "locator.json", {"prefix": c.prefix})
        save(
            c.science / "publications/PACKET.json",
            {"boundary": "PACKET", "parent_head": c.approved_head, "sha256": {}},
        )
        save(c.operational / "state.json", {"status": "RUNNING"})
        assert c.status()["status"].startswith("BLOCKED")
        assert (await snapshot(c.repository.root, c.run_id))[
            "publication_blockers"
        ] == ["UNCOMMITTED_PUBLICATION:PACKET"]
        before = {
            p: p.read_bytes()
            for root in (c.science, c.operational)
            for p in root.rglob("*")
            if p.is_file()
        }
        viewer = asyncio.create_task(
            follow(c.repository.root, c.run_id, Console(), interval=0.02),
        )
        await asyncio.sleep(0.4)
        viewer.cancel()
        with pytest.raises(asyncio.CancelledError):
            await viewer
        assert before == {
            p: p.read_bytes()
            for root in (c.science, c.operational)
            for p in root.rglob("*")
            if p.is_file()
        }
        save(
            c.operational / "state.json",
            {"status": "BLOCKED; MAINTAINER_DECISION_REQUIRED"},
        )
        result = await follow(
            c.repository.root,
            c.run_id,
            Console(json_output=True),
            interval=0.02,
        )
        assert result["status"].startswith("BLOCKED")

    asyncio.run(run())
    output = capsys.readouterr()
    assert "BLOCKED" in output.err
    assert all(isinstance(json.loads(line), dict) for line in output.out.splitlines())


def test_cli_stdout_json_and_lifecycle_stderr(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: Any,
) -> None:
    from experiments.orchestration import __main__ as cli

    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work", approved=False)
        monkeypatch.setattr(cli, "Controller", FixtureController)
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "orchestration",
                "run",
                "plan.json",
                "--repository",
                str(c.repository.root),
                "--work-root",
                str(c.work_root),
                "--approve",
                c.run_id,
            ],
        )
        await cli.main()

    asyncio.run(run())
    output = capsys.readouterr()
    result = json.loads(output.out)
    assert result["status"].startswith("COMPLETE")
    for token in (
        "controller-authentication",
        "plan-authentication",
        "APPROVAL-publication",
        "PACKET-publication",
        "STARTED",
        "PID",
        "COMPLETE",
        "blind semantic gold",
    ):
        assert token in output.err


def test_publication_failure_visibility(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: Any,
) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work")
        c.reporter = Console()

        async def fail(*_args: Any) -> str:
            raise ValueError("fixture publication ambiguity")

        monkeypatch.setattr(c.repository, "commit", fail)
        with pytest.raises(ValueError, match="ambiguity"):
            await c.observed_publication(
                "PACKET",
                c.prefix,
                {},
                "fixture",
                c.checkpoint_validation,
            )

    asyncio.run(run())
    output = capsys.readouterr()
    assert "PACKET-publication STARTED" in output.err
    assert (
        "=== FAILED ===" in output.err and "fixture publication ambiguity" in output.err
    )
    assert '"automatic_scientific_retries": 0' in output.err


def test_authentication_wait_heartbeat() -> None:
    async def run() -> None:
        events: list[dict[str, Any]] = []
        await observed_wait(
            asyncio.sleep(0.05),
            events.append,
            {"operation": "authentication"},
            interval=0.01,
        )
        assert events and all(e["status"] == "HEARTBEAT" for e in events)

    asyncio.run(run())


def test_zero_exit_validator_rejection_prints_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: Any,
) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work")
        c.reporter = Console()
        workspace = tmp_path / "validator"
        workspace.mkdir()
        monkeypatch.setattr(
            c,
            "arguments",
            lambda *_args: [sys.executable, "-c", 'print(\'{"status":"FAIL"}\')'],
        )
        with pytest.raises(ValueError, match="Validator rejected"):
            await c.validate("packet_validate", workspace, "alpha", "packet")
        assert c.state["failure_category"] == "VALIDATOR_REJECTION"
        assert c.state["failures"][-1]["exit_code"] == 0
        assert not c.journal("alpha", "B", "ENTERED").exists()

    asyncio.run(run())
    output = capsys.readouterr()
    assert "=== FAILED ===" in output.err
    assert "Validator rejected candidate" in output.err
    assert "exit_code=0" in output.err and "stdout_path=" in output.err


def test_follow_live_progress_and_terminal_stop(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: Any,
) -> None:
    from experiments.orchestration import follow as viewer

    async def run() -> None:
        save(tmp_path / "state.json", {"status": "RUNNING"})

        async def fixed_snapshot(_root: Path, _identity: str) -> dict[str, Any]:
            return {
                "status": load(tmp_path / "state.json")["status"],
                "log_root": str(tmp_path),
                "progress_log": str(tmp_path / "progress.log"),
                "stages": {},
                "archived": False,
            }

        monkeypatch.setattr(viewer, "snapshot", fixed_snapshot)
        task = asyncio.create_task(
            viewer.follow(tmp_path, "fake", Console(), interval=0.01),
        )
        await asyncio.sleep(0.03)
        (tmp_path / "progress.log").write_text(
            json.dumps(
                {
                    "case": "0020",
                    "stage": "C",
                    "status": "HEARTBEAT",
                    "pid": 42,
                    "model": "GPT-6 Astra",
                    "reasoning": "High",
                    "stdout_path": str(tmp_path / "stdout.log"),
                },
            )
            + "\n",
        )
        await asyncio.sleep(0.04)
        save(tmp_path / "state.json", {"status": "COMPLETE; MAINTAINER_REVIEW_READY"})
        result = await asyncio.wait_for(task, 2)
        assert result["status"].startswith("COMPLETE")

    asyncio.run(run())
    output = capsys.readouterr()
    assert (
        "HEARTBEAT" in output.err
        and "GPT-6 Astra" in output.err
        and "pid=42" in output.err
    )
