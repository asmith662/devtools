# Copyright (c) 2026
# ruff: noqa: S101, D103, ANN401, SLF001, PT011 -- synthetic sealed-branch fixtures
"""Adoption authenticates immutable provenance and never runs a scientific worker."""

import asyncio
import json
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from devtools.core.time import Duration
from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.adoption import SCHEMA, AdoptedBranch, pack
from experiments.orchestration.model import RunPlan
from experiments.orchestration.storage import load
from experiments.orchestration.tests.test_controller import FixtureController, fixture
from experiments.orchestration.workers import accounting, measurement


def branch_fixture() -> tuple[dict[str, Any], dict[str, bytes], dict[str, bytes]]:
    """Construct a complete fictional independent B branch."""
    config = {
        "model": "SYNTHETIC",
        "model_id": "fake",
        "reasoning": "High",
        "runtime": {"identity": "original"},
        "evidence_locator": {},
        "response_schema": {},
    }
    protocol = {"workers": {"grounding": config}}
    frame = {"synthetic": True}
    origin = {
        "run_id": "old-run",
        "case": "alpha",
        "operation": "B",
        "attempt": 1,
        "stage_a": "stage-a",
        "packet_commit": "packet",
    }
    scientific = {
        "design.json": b"{}",
        "resources.json.gz": b"SYNTHETIC",
        "completion_proof.json": json_bytes(
            {"inputs": {"implementation_sha256": {"source": "hash"}}},
        ),
        "native/execution_started.json": json_bytes(
            {
                "run_binding": {
                    "run_id": "old-run",
                    "stage_a_checkpoint": "stage-a",
                    "packet_checkpoint": "packet",
                },
            },
        ),
    }
    inputs = {
        "design.json": b"{}",
        "resources.json.gz": b"SYNTHETIC",
        "INSTRUCTIONS_GROUNDING.md": b"fictional instruction",
        "reviewer_codec.py": b"fictional builder",
        "worker_configuration.json": json_bytes(protocol),
    }
    validation = {
        "status": "PASS",
        "mode": "SEALED",
        "native_archives_decoded": 0,
        "deep_correspondence_executions": 0,
        "completion_proof_sha256": digest(scientific["completion_proof.json"]),
    }
    entered = {
        "run_id": "old-run",
        "case": "alpha",
        "stage": "B",
        "frame": frame,
        "inputs_sha256": "input",
    }
    returned = {
        **entered,
        "validation": validation,
        "files": {n: digest(v) for n, v in scientific.items()},
    }
    stdout = (
        b'{"type":"thread.started","thread_id":"synthetic-thread"}\n'
        + json.dumps(
            {
                "type": "turn.completed",
                "usage": {
                    "input_tokens": 100,
                    "cached_input_tokens": 0,
                    "cache_write_input_tokens": 0,
                    "output_tokens": 10,
                    "reasoning_output_tokens": 2,
                },
            },
        ).encode()
        + b"\n"
    )
    usage = accounting.accept(
        measurement.capture(
            config,
            "alpha",
            "original-invocation",
            b"disclosure",
            SimpleNamespace(stdout=stdout, duration=Duration.seconds(2)),
            None,
            validated=True,
            failure=None,
        ),
        "SYNTHETIC-ORIGINAL",
    )
    compatibility = {
        "original_disclosure_replay_sha256": digest(b"disclosure"),
        "scientific_contract": {
            "experiments/source_grounding/reviewer.py": digest(b"fictional builder"),
        },
    }
    files = {"artifacts/" + n: v for n, v in scientific.items()}
    files.update(
        {
            "provenance/" + n: json_bytes(v)
            for n, v in {
                "ENTERED.json": entered,
                "RETURNED.json": returned,
                "Stage-A-protocol.json": protocol,
                "origin-run.json": {
                    "approval_checkpoint": "approval",
                    "plan": {
                        "attempt": 1,
                        "stage_a": {
                            "checkpoint": "stage-a",
                            "protocol": {"sha256": digest(json_bytes(protocol))},
                        },
                    },
                },
                "origin-PACKET-publication.json": {
                    "boundary": "PACKET",
                    "parent_head": "approval",
                },
                "process-exit.json": {"duration_seconds": 2},
                "semantic-receipt.json": {
                    "status": "PASS",
                    "process_exit": 0,
                    "model": "SYNTHETIC",
                    "reasoning": "High",
                    "input_sha256": digest(b"disclosure"),
                    "invocation": "original-invocation",
                    "thread_id": "synthetic-thread",
                    "usage": json.loads(stdout.splitlines()[1])["usage"],
                },
            }.items()
        },
    )
    files.update(
        {
            "provenance/stdout.jsonl": stdout,
            "provenance/disclosure.bin": b"disclosure",
            "provenance/instruction.bin": inputs["INSTRUCTIONS_GROUNDING.md"],
        },
    )
    value = {
        "schema": SCHEMA,
        "origin": origin,
        "frame": frame,
        "input_sha256": "input",
        "scientific_files": returned["files"],
        "validation": validation,
        "model": "SYNTHETIC",
        "reasoning": "High",
        "runtime": config["runtime"],
        "implementation": {"source": "hash"},
        "original_usage": usage,
        "compatibility": compatibility,
        "compatibility_sha256": digest(json_bytes(compatibility)),
        "independence": {
            "packet_commit": "packet",
            "sibling_dependency": False,
            "downstream_dependency": False,
            "forbidden_later_evidence_available": False,
        },
        "closure_file": "closure.json.gz",
        "eligibility": {
            "entered": True,
            "returned": True,
            "failed": False,
            "complete_artifact_closure": True,
            "independent": True,
            "unchanged_branch_semantics": True,
        },
    }
    return value, files, inputs


def authenticate(value: Any, files: dict[str, bytes]) -> AdoptedBranch:
    """Resign a fixture to test eligibility beyond the outer digest gate."""
    compressed = pack(files)
    value["closure_sha256"] = digest(compressed)
    value["inventory"] = {
        n: {"bytes": len(v), "sha256": digest(v)} for n, v in sorted(files.items())
    }
    value["inventory_sha256"] = digest(json_bytes(value["inventory"]))
    raw = json_bytes(value)
    return AdoptedBranch.authenticate(
        raw,
        compressed,
        digest(raw),
        value["compatibility_sha256"],
    )


@pytest.mark.parametrize(
    "mutation",
    [
        "failed",
        "entered-only",
        "validator",
        "input",
        "stage-a",
        "packet",
        "runtime",
        "implementation",
        "artifact",
        "sibling",
        "downstream",
        "later",
        "usage",
    ],
)
def test_ineligible_branch_rejected(mutation: str) -> None:
    value, files, _ = branch_fixture()
    if mutation == "failed":
        value["eligibility"]["failed"] = True
    elif mutation == "entered-only":
        value["eligibility"]["returned"] = False
    elif mutation == "validator":
        value["validation"]["status"] = "FAIL"
    elif mutation == "input":
        value["input_sha256"] = "foreign"
    elif mutation in {"stage-a", "packet"}:
        value["origin"]["stage_a" if mutation == "stage-a" else "packet_commit"] = (
            "foreign"
        )
    elif mutation in {"runtime", "implementation"}:
        value[mutation] = {"foreign": True}
    elif mutation == "artifact":
        files["artifacts/design.json"] = b"foreign"
    elif mutation in {"sibling", "downstream", "later"}:
        key = {
            "sibling": "sibling_dependency",
            "downstream": "downstream_dependency",
            "later": "forbidden_later_evidence_available",
        }[mutation]
        value["independence"][key] = True
    else:
        value["original_usage"]["measurement"]["usage"]["input_tokens"] = 101
    with pytest.raises(ValueError):
        authenticate(value, files)


def test_immutable_materialization_and_scientific_compatibility(tmp_path: Path) -> None:
    value, files, inputs = branch_fixture()
    branch = authenticate(value, files)
    branch.compatible_inputs(inputs)
    restored = branch.materialize(tmp_path / "fresh")
    assert restored == {
        n.removeprefix("artifacts/"): v
        for n, v in files.items()
        if n.startswith("artifacts/")
    }
    with pytest.raises(ValueError, match="already exists"):
        branch.materialize(tmp_path / "fresh")
    for name in inputs:
        modified = deepcopy(inputs)
        modified[name] = b"{}" if name == "worker_configuration.json" else b"foreign"
        with pytest.raises((ValueError, KeyError)):
            branch.compatible_inputs(modified)
    assert (
        accounting.aggregate(
            (
                value["original_usage"],
                accounting.adopted(value["original_usage"], digest(branch.canonical)),
            ),
        ).invocations
        == 1
    )


def test_controller_adoption_never_enters_or_launches_model(tmp_path: Path) -> None:
    async def run() -> None:
        c = await fixture(tmp_path / "repo", tmp_path / "work")
        c._authorization = await c.execution_authorization()
        value, files, inputs = branch_fixture()
        # Align this fictional frame with the authorized synthetic fixture.
        frame = c.plan.cases[0].frame
        value["frame"] = frame
        for name in ("ENTERED", "RETURNED"):
            row = json.loads(files["provenance/" + name + ".json"])
            row["frame"] = frame
            files["provenance/" + name + ".json"] = json_bytes(row)
        branch = authenticate(value, files)
        destination = c.repository.root / "sealed"
        destination.mkdir()
        (destination / "seal.json").write_bytes(branch.canonical)
        (destination / "closure.json.gz").write_bytes(branch.compressed)
        plan_value = c.value
        plan_value["adopted_branches"] = {
            "alpha": {
                "path": "sealed/seal.json",
                "sha256": digest(branch.canonical),
                "compatibility_sha256": value["compatibility_sha256"],
            },
        }
        grant = c._authorization
        c = FixtureController(c.repository, RunPlan.parse(plan_value), c.work_root)
        # Unit-test dispatch; public plan/approval authority has separate tests.
        c._authorization = grant
        first, artifacts = await c._worker(c.plan.cases[0], "B", inputs)
        assert first["execution_origin"] == "ADOPTED"
        assert (
            first["original_usage"]["measurement"]["invocation_id"]
            == "original-invocation"
        )
        assert not c.journal("alpha", "B", "ENTERED").exists()
        assert not list((tmp_path / "work").glob("**/process/launch.json"))
        second, again = await c._worker(c.plan.cases[0], "B", inputs)
        assert first == second
        assert artifacts == again
        assert load(c.journal("alpha", "B", "ADOPTED"))["origin"]["run_id"] == "old-run"

    asyncio.run(run())
