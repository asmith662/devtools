# Copyright (c) 2026
# ruff: noqa: PLR2004 -- mechanical fixture constants
"""Exercise prospective overwrite, leakage and deterministic mechanics only."""

from __future__ import annotations

import asyncio
import copy
import io
import tarfile
from typing import TYPE_CHECKING, Any

import pytest

from experiments.codex_dogfood.case_0009 import execute, freeze, packet
from experiments.codex_dogfood.case_0009.artifacts import (
    START,
    binary,
    digest,
    json_bytes,
    put_json,
)
from experiments.codex_dogfood.case_0009.freeze import eligible, ensure_absent
from experiments.codex_dogfood.case_0009.packet import validate_packet
from experiments.codex_dogfood.case_0009.protocol import TASK, task_inputs, treatment

if TYPE_CHECKING:
    from pathlib import Path


def test_freeze_is_deterministic_outcome_free_and_refuses_overwrite(
    tmp_path: Path,
) -> None:
    """Only task/query/arm definitions enter freeze; repeated writes fail closed."""
    task, queries = task_inputs()
    assert len(task.obligations) == len(queries) == 9
    assert all(item.witness_alternatives == () for item in task.obligations)
    assert treatment()["full_task_query"] == TASK
    first = json_bytes(treatment())
    assert first == json_bytes(treatment())
    path = tmp_path / "treatment.json"
    put_json(path, treatment())
    assert binary(path) == first
    with pytest.raises(FileExistsError):
        put_json(path, treatment())
    with pytest.raises(FileExistsError):
        ensure_absent(tmp_path, ("treatment.json",))
    assert binary(path) == first


def test_selection_excludes_outcome_files_without_reading_them() -> None:
    """No historical outcomes, reserve or confirmation path can enter corpus."""
    assert eligible("src/devtools/context/localization/assessment.py")
    assert not eligible("experiments/codex_dogfood/case_0008/analysis.md")
    assert not eligible("tests/experiments/identifier_sparse/test_analysis.py")
    assert not eligible("docs/research/evidence-to-witness-resolution-policy.md")
    assert not eligible("docs/confirmation/outcome.md")


def test_packet_keys_reject_treatment_leakage_but_preserve_source_vocabulary() -> None:
    """Actual source can say rank; experiment metadata cannot be exported."""
    resources: dict[str, Any] = {
        "schema": "case-0009-blind-resources-v1",
        "resources": [
            {
                "address": "a.py",
                "content_identity": "opaque",
                "content": "rank score identifier",
            },
        ],
    }
    manifest = {
        "schema": "case-0009-blind-task-v1",
        "task": TASK,
        "task_identity": "test",
        "repository_id": "test",
        "snapshot_id": "test",
        "corpus_id": "test",
        "obligations": [],
        "resources_sha256": digest(json_bytes(resources)),
        "resource_count": 1,
        "instructions": "independent",
    }
    validate_packet(manifest, resources)
    leaked = copy.deepcopy(manifest)
    leaked["rank"] = 1
    with pytest.raises(ValueError, match="whitelist"):
        validate_packet(leaked, resources)
    leaked_resources = copy.deepcopy(resources)
    leaked_resources["resources"][0]["query_terms"] = ["identifier"]
    with pytest.raises(ValueError, match="whitelist"):
        validate_packet(manifest, leaked_resources)


def test_stage_a_b_and_blind_replay_on_small_mechanical_frame(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Exercise stage lineage/refusals on synthetic data, not the prospective case."""
    case = tmp_path / "case_0009"
    case.mkdir()
    for module in (execute, freeze, packet):
        monkeypatch.setattr(module, "CASE", case)
    files = {
        "docs/example.md": b"CandidateMemberResolution quiet",
        "README.md": b"plain prose",
    }
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w") as bundle:
        for address, content in files.items():
            member = tarfile.TarInfo(address)
            member.size = len(content)
            bundle.addfile(member, io.BytesIO(content))

    async def git(*args: str) -> bytes:
        if args[:2] == ("rev-parse", "HEAD"):
            return START.encode()
        if args[0] == "branch":
            return b"main"
        if args[0] == "ls-tree":
            return "\n".join(files).encode()
        if args[0] == "archive":
            return buffer.getvalue()
        return b""

    monkeypatch.setattr(freeze, "git", git)
    manifest = asyncio.run(freeze.freeze())
    assert manifest["query_execution"] == "NONE"
    assert not (case / "execution_started.json").exists()
    with pytest.raises(FileExistsError):
        asyncio.run(freeze.freeze())
    assert execute.execute()["lanes"] == 10
    assert execute.verify_capture()["status"].startswith("VERIFIED CAPTURE")
    with pytest.raises(FileExistsError):
        execute.execute()

    original_read = binary

    def blind_read(path: Path) -> bytes:
        assert path.name not in {"results.json.gz", "costs.json"}
        return original_read(path)

    monkeypatch.setattr(packet, "binary", blind_read)
    assert packet.build()["resources"] == 2
    assert packet.verify_packet()["obligations"] == 9
    with pytest.raises(FileExistsError):
        packet.build()
