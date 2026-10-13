# Copyright (c) 2026
# ruff: noqa: ANN401, S101, D103 -- synthetic blind packet fixtures
"""Test deterministic isolation, tamper/leakage rejection and standalone validation."""

from __future__ import annotations

import asyncio
import copy
import gzip
import json
from typing import TYPE_CHECKING, Any

import pytest

from experiments.codex_dogfood.case_0009.artifacts import json_bytes
from experiments.codex_dogfood.case_0015.freeze import frame
from experiments.structural_discrimination.stage_b import capture
from experiments.structural_discrimination.stage_c import packet, validate_packet

if TYPE_CHECKING:
    from pathlib import Path


def synthetic_payload() -> Any:
    metadata, rows = frame({"docs/test.md": b"bounded independent synthetic source\n"})
    for row in rows:
        import hashlib  # noqa: PLC0415 -- exact synthetic Git blob identity

        content = row["content"].encode()
        row["git_blob_oid"] = hashlib.sha1(
            f"blob {len(content)}\0".encode() + content,
            usedforsecurity=False,
        ).hexdigest()
    return {
        "case_id": "synthetic-case",
        "task_identity": "synthetic-task",
        "task_text": "synthetic bounded work\n",
        "parent_frame": {k: v for k, v in metadata.items() if k != "resources"},
        "interpretation_gaps": ["unspecified external option"],
        "ambiguities": [],
        "obligations": [
            {
                "id": "O1",
                "requirement": "synthetic requirement",
                "satisfaction": "synthetic criterion",
                "excluded_interpretation": "external claims excluded",
                "obligation_identity": {"task": "synthetic-task", "value": "O1"},
            },
        ],
        "resources": [{k: row[k] for k in validate_packet.RESOURCE} for row in rows],
        "gold_status": "NOT_CREATED",
    }


def test_double_build_standalone_overwrite_and_physical_tamper(tmp_path: Path) -> None:
    value = synthetic_payload()
    first, bound = packet.render(value)
    second, second_bound = packet.render(copy.deepcopy(value))
    assert first == second
    assert bound == second_bound
    assert not any(
        b"direct-discrimination" in raw or b"structural_discrimination" in raw
        for name, raw in first.items()
        if name != "resources.json.gz"
    )
    root = tmp_path / "blind"
    assert packet.publish(root, first, bound)["status"] == "PASS; NO ADJUDICATION"
    assert (
        json.loads(asyncio.run(packet.standalone(root)))["status"]
        == "PASS; NO ADJUDICATION"
    )
    assert {p.name for p in root.iterdir()} == validate_packet.FILES
    with pytest.raises(FileExistsError, match="overwrite"):
        packet.publish(root, first, bound)
    for name in validate_packet.FILES:
        path = root / name
        path.write_bytes(first[name] + b"changed")
        with pytest.raises((ValueError, json.JSONDecodeError)):
            validate_packet.validate(root, bound)
        path.write_bytes(first[name])
    (root / "extra.txt").write_text("unwanted", encoding="utf8")
    with pytest.raises(ValueError, match="five files"):
        validate_packet.validate(root, bound)


@pytest.mark.parametrize(
    "field",
    [
        "query",
        "rank",
        "score",
        "annotations",
        "supports",
        "local_pairs",
        "timings",
        "child_commit",
        "child_tree",
        "changed_paths",
        "diff",
        "implementation",
        "execution",
    ],
)
def test_metadata_leakage_rejects_even_with_recomputed_payload_hash(field: str) -> None:
    value = synthetic_payload()
    value["interpretation_gaps"] = [{field: "forbidden metadata"}]
    with pytest.raises(ValueError, match="leakage"):
        packet.render(value)


@pytest.mark.parametrize(
    "field",
    [
        "task_text",
        "obligations",
        "interpretation_gaps",
        "parent_frame",
        "resources",
        "case_id",
    ],
)
def test_frozen_semantic_binding_rejects_mutation(field: str) -> None:
    value = synthetic_payload()
    _files, bound = packet.render(value)
    altered = copy.deepcopy(value)
    altered[field] = "foreign"
    with pytest.raises(ValueError, match="identity"):
        validate_packet.validate_payload(altered, bound)


def test_actual_stage_a_spec_shape_projects_only_semantic_fields(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    value = synthetic_payload()
    spec = {
        **value,
        "schema": "administrative-formulation-tag",
        "resources": "complete resources supplied separately",
    }
    (tmp_path / "blind_spec.json").write_bytes(json_bytes(spec))
    (tmp_path / "resources.json.gz").write_bytes(
        gzip.compress(json_bytes(value["resources"]), mtime=0),
    )
    monkeypatch.setattr(capture, "case_root", lambda _case: tmp_path)
    assert packet.payload("0017") == value
    files, _bound = packet.render(packet.payload("0017"))
    assert b"administrative-formulation-tag" not in gzip.decompress(
        files["resources.json.gz"],
    )
