# Copyright (c) 2026
# ruff: noqa: S101, D103, PT018, PLC0415, COM812 -- inert real-process startup fixtures
"""Prospective startup admission is separate from scientific execution."""

import asyncio
from pathlib import Path
from typing import Any

import pytest

from experiments.codex_dogfood.case_0009.artifacts import digest
from experiments.orchestration import entrypoints


def specification(root: Path, content: bytes) -> dict[str, Any]:
    """Build one explicit direct-script entrypoint with no scientific actions."""
    (root / "worker.py").write_bytes(content)
    argv = ["{python}", "-B", "{repository}/worker.py", "never-executed-stage"]
    return {
        "commands": {"prepare": argv, "validate": argv},
        "semantic": {"kind": "process", "argv": argv},
        "implementation": {"worker.py": digest(content)},
        "worker_entrypoints": {
            "schema": entrypoints.SCHEMA,
            "mode": "DIRECT_SCRIPT_HELP",
            "timeout_seconds": 30,
            "scripts": {"worker.py": digest(content)},
        },
    }


def test_unique_real_script_preflight(tmp_path: Path) -> None:
    value = specification(
        tmp_path, b"import argparse\nargparse.ArgumentParser().parse_args()\n"
    )
    assert entrypoints.inventory(value) == ["worker.py"]
    result = asyncio.run(entrypoints.check(tmp_path, value))
    assert result["status"] == "PASS" and len(result["scripts"]) == 1
    receipt = result["scripts"][0]
    assert receipt["argv"][1:] == ["-B", str(tmp_path / "worker.py"), "--help"]
    assert receipt["external_cwd"] and receipt["cwd_unchanged"]
    assert not list(tmp_path.glob("**/ENTERED.json"))


@pytest.mark.parametrize(
    "content", [b"import nonexistent_startup_fixture\n", b"print('not help')\n"]
)
def test_import_failure_invalidates_plan(tmp_path: Path, content: bytes) -> None:
    value = specification(tmp_path, content)
    with pytest.raises(ValueError, match=r"PLAN_INVALID.*startup"):
        asyncio.run(entrypoints.check(tmp_path, value))


def test_preflight_inventory_and_hash_are_closed(tmp_path: Path) -> None:
    value = specification(
        tmp_path, b"import argparse\nargparse.ArgumentParser().parse_args()\n"
    )
    value["worker_entrypoints"]["scripts"] = {}
    with pytest.raises(ValueError, match="inventory"):
        entrypoints.validate(value)
    value = specification(tmp_path, b"pass\n")
    (tmp_path / "worker.py").write_bytes(b"changed\n")
    with pytest.raises(ValueError, match="bytes changed"):
        asyncio.run(entrypoints.check(tmp_path, value))
    value["commands"]["prepare"][1] = "-I"
    with pytest.raises(ValueError, match="shape"):
        entrypoints.validate(value)


def test_discrimination_cannot_skip_gate() -> None:
    value = {
        "commands": {
            "prepare": [
                "{python}",
                "-B",
                "{repository}/experiments/source_grounding/discrimination/entry.py",
            ]
        },
        "semantic": {"kind": "codex"},
    }
    with pytest.raises(ValueError, match="preflight required"):
        asyncio.run(entrypoints.check(Path.cwd(), value))


def test_controller_rejects_startup_before_approval(tmp_path: Path) -> None:
    from experiments.orchestration.controller import Controller
    from experiments.orchestration.storage import save
    from experiments.orchestration.tests.test_controller import fixture

    async def run() -> None:
        controller = await fixture(tmp_path / "repo", tmp_path / "work", approved=False)
        value = controller.value
        broken = b"import nonexistent_startup_fixture\n"
        (controller.repository.root / "worker.py").write_bytes(broken)
        value["implementation"]["worker.py"] = digest(broken)
        value["worker_entrypoints"] = specification(tmp_path, broken)[
            "worker_entrypoints"
        ]
        save(controller.repository.root / "plan.json", value)
        await controller.repository.git("add", "worker.py", "plan.json")
        await controller.repository.git("commit", "-m", "Bind broken startup fixture")
        with pytest.raises(ValueError, match=r"PLAN_INVALID.*startup"):
            await Controller.from_plan(
                controller.repository.root, "plan.json", tmp_path / "new-work"
            )
        assert not list(controller.repository.root.glob("experiments/**/approval.json"))
        assert not list(controller.repository.root.glob("experiments/**/ENTERED.json"))

    asyncio.run(run())
