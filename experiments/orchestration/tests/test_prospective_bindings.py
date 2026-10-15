# Copyright (c) 2026
# ruff: noqa: S101, D103 -- explicit immutable prospective evidence fixtures
"""Prospective compatibility and forensic exceptions require exact bindings."""

import asyncio
import json
from pathlib import Path

import pytest

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.model import RunPlan
from experiments.orchestration.tests.test_adoption import authenticate, branch_fixture
from experiments.orchestration.tests.test_controller import FixtureController, fixture


def test_exact_preserved_journal_is_not_a_dirty_worktree_waiver(tmp_path: Path) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work", approved=False)
        address = "experiments/fake/runs/historical/journal/alpha/B/RETURNED.json"
        journal = c.repository.root / address
        journal.parent.mkdir(parents=True)
        journal.write_bytes(b'{"historical":true}\n')
        value = c.value
        value["preserved_evidence"] = {address: digest(journal.read_bytes())}
        (c.repository.root / "plan.json").write_bytes(RunPlan.parse(value).canonical)
        await c.repository.git("add", "plan.json")
        await c.repository.git("commit", "-m", "Bind exact historical evidence")
        checked = await FixtureController.from_plan(
            c.repository.root,
            "plan.json",
            c.work_root,
        )
        assert checked.plan_report()["execution_authorized"] == "NO"
        journal.write_bytes(b"changed")
        with pytest.raises(ValueError, match="Preserved journal changed"):
            await checked.repository.authenticate()
        journal.write_bytes(b'{"historical":true}\n')
        (c.repository.root / "unrelated.txt").write_bytes(b"unrelated")
        with pytest.raises(ValueError, match="Unexpected untracked"):
            await checked.repository.authenticate()
        for address in ("source.py", "experiments/x/runs/y/journal/secrets.txt"):
            value["preserved_evidence"] = {address: "0" * 64}
            with pytest.raises(ValueError, match="historical journal"):
                RunPlan.parse(value)

    asyncio.run(run())


def test_adoption_requires_explicit_prospective_compatibility(tmp_path: Path) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work", approved=False)
        value, files, _ = branch_fixture()
        value["frame"] = c.plan.cases[0].frame
        for name in ("ENTERED", "RETURNED"):
            row = json.loads(files["provenance/" + name + ".json"])
            row["frame"] = value["frame"]
            files["provenance/" + name + ".json"] = json_bytes(row)
        branch = authenticate(value, files)
        folder = c.repository.root / "sealed"
        folder.mkdir()
        (folder / "seal.json").write_bytes(branch.canonical)
        (folder / "closure.json.gz").write_bytes(branch.compressed)
        contract = value["compatibility"]["scientific_contract"]
        address = next(iter(contract))
        source = c.repository.root / address
        source.parent.mkdir(parents=True)
        source.write_bytes(b"prospectively attested operational change")
        binding = {
            "path": "sealed/seal.json",
            "sha256": digest(branch.canonical),
            "compatibility_sha256": value["compatibility_sha256"],
        }
        plan = c.value
        plan["adopted_branches"] = {"alpha": binding}
        (c.repository.root / "plan.json").write_bytes(RunPlan.parse(plan).canonical)
        await c.repository.git("add", ".")
        await c.repository.git("commit", "-m", "Unattested changed branch contract")
        with pytest.raises(ValueError, match="scientific contract changed"):
            await FixtureController.from_plan(
                c.repository.root,
                "plan.json",
                c.work_root,
            )
        attestation = json_bytes(
            {
                "origin_seal_sha256": binding["sha256"],
                "original_contract": contract,
                "prospective_contract": {address: digest(source.read_bytes())},
                "scientific_semantics": "UNCHANGED",
            },
        )
        (folder / "compatibility.json").write_bytes(attestation)
        binding["prospective_compatibility"] = {
            "path": "sealed/compatibility.json",
            "sha256": digest(attestation),
        }
        (c.repository.root / "plan.json").write_bytes(RunPlan.parse(plan).canonical)
        await c.repository.git("add", ".")
        await c.repository.git("commit", "-m", "Explicit prospective compatibility")
        checked = await FixtureController.from_plan(
            c.repository.root,
            "plan.json",
            c.work_root,
        )
        assert checked.plan_report()["execution_authorized"] == "NO"
        assert not list(c.work_root.glob("**/ENTERED.json"))

    asyncio.run(run())
