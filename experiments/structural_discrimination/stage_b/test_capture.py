# Copyright (c) 2026
# ruff: noqa: ANN401, EM101, TRY003, S101, PLR2004, D103 -- bounded synthetic capture tests
"""Test complete synthetic capture/proof and failures without cohort treatment."""

from __future__ import annotations

import gzip
import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

import pytest

from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.codex_dogfood.case_0012.stage_b.graph import describe
from experiments.codex_dogfood.case_0015.freeze import frame
from experiments.codex_dogfood.verification.native import NativeMemo
from experiments.structural_discrimination.stage_b import (
    authentication,
    capture,
    execute,
    reporting,
)


def synthetic(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Any, Any, Any]:
    blobs = {
        "src/source.py": (
            b"from target import f\ndef local():\n    pass\nlocal()\nf()\nf()\n"
        ),
        "src/target.py": b"def f():\n    pass\n",
        "docs/other.md": b"source target independent words f\n",
    }
    metadata, rows = frame(dict(sorted(blobs.items())))
    metadata["python_resource_count"] = 2
    task = "synthetic direct reference fixture"
    design = {
        "task_identity": "synthetic-task",
        "task_text": task,
        "parent_frame": metadata,
        "shared_protocol_sha256": digest(b"fixture protocol"),
        "interpretation_gaps": [],
        "obligations": [
            {
                "id": f"O{i}",
                "obligation_identity": {"task": "synthetic-task", "value": f"O{i}"},
                "query_identity": {"task": "synthetic-task", "value": f"Q{i}"},
                "need": "synthetic need",
                "query": "source target f",
            }
            for i in range(1, 4)
        ],
    }
    case = tmp_path / "case"
    case.mkdir()
    for name, value in {
        "protocol.json": design,
        "frame.json": metadata,
        "blind_spec.json": {},
    }.items():
        (case / name).write_bytes(json_bytes(value))
    (case / "task.txt").write_text(task, encoding="utf8")
    (case / "resources.json.gz").write_bytes(gzip.compress(json_bytes(rows), mtime=0))
    monkeypatch.setattr(capture, "case_root", lambda _case: case)
    monkeypatch.setattr(capture, "capture_root", lambda _case: case / "capture")
    monkeypatch.setattr(
        capture,
        "source_hashes",
        lambda: {"synthetic/stage_b/fixture.py": digest(b"synthetic-only")},
    )
    monkeypatch.setattr(authentication, "source_hashes", capture.source_hashes)
    monkeypatch.setattr(execute, "progress", lambda *_args: None)
    return design, rows, capture.schedule("0017", rows)


def test_complete_synthetic_capture_deep_and_sealed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    design, rows, plan = synthetic(tmp_path, monkeypatch)
    result = execute.execute_case("0017", design, rows, plan)
    assert result["proof"] == "CAPTURE_TIME_DEEP_PROOF_AUTHENTICATED"
    assert result["native_archives_decoded"] == 0
    root = capture.capture_root("0017")
    trace = json.loads(gzip.decompress((root / "trace.json.gz").read_bytes()))
    assert trace["summary"]["ri"]["resources_derived"] == 2
    assert trace["summary"]["ri"]["positive_references"] == 3
    assert trace["summary"]["ri"]["self_references"] == 1
    assert len(plan["operations"]) == 21
    seal = (root / "integrity.json").read_bytes()
    for _ in range(2):
        assert authentication.sealed(root, seal)["summary"] == result["summary"]
    with pytest.raises(FileExistsError, match="claimed"):
        execute.execute_case("0017", design, rows, plan)
    assert not (root / "capture_failure.json").exists()
    for name in (
        "execution_completed.json",
        "native_context.json",
        "completion_proof.json",
        "arm_a.json.gz",
        "references.json.gz",
        "operations/000001.returned.json",
    ):
        path = root / name
        original = path.read_bytes()
        path.write_bytes(original + b"changed")
        with pytest.raises(ValueError, match="bytes differ"):
            authentication.sealed(root, seal)
        path.write_bytes(original)
    altered = json.loads(seal)
    altered["implementation"]["synthetic/stage_b/fixture.py"] = digest(b"foreign")
    with pytest.raises(ValueError, match="integrity differs"):
        authentication.sealed(root, json_bytes(altered))
    for query in trace["queries"]:
        query["local_pairs"][0]["predecessor"]["a_rank"] = 999
        with pytest.raises(ValueError, match="predecessor"):
            reporting.canonical_validate(trace)
        break


def test_failed_native_boundary_is_dead_and_stops(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    design, rows, plan = synthetic(tmp_path, monkeypatch)

    def fail(*_args: Any) -> Any:
        raise RuntimeError("synthetic failure before native return")

    monkeypatch.setattr(execute, "prepare", fail)
    with pytest.raises(RuntimeError, match="synthetic failure"):
        execute.execute_case("0017", design, rows, plan)
    root = capture.capture_root("0017")
    failure = json.loads((root / "capture_failure.json").read_bytes())
    assert failure["returned_operations"] == []
    assert (root / "operations/000001.failed_no_return.json").exists()
    assert not (root / "execution_completed.json").exists()
    with pytest.raises(FileExistsError, match="claimed"):
        execute.execute_case("0017", design, rows, plan)


def test_exact_capture_graph_encoder_order_types_aliases() -> None:
    shared = ("utf8 π", 1.25, None)
    values = [
        None,
        (),
        {"second": shared, "first": [shared, shared]},
        (True, False, 0, -1, ""),
    ]
    memo = NativeMemo()
    for value in values:
        assert memo.encoding.encode(value) == json_bytes(describe(value))
    mutable = {"key": [1]}
    assert memo.encoding.encode(mutable) == json_bytes(describe(mutable))
    mutable["key"].append(2)
    assert memo.encoding.encode(mutable) == json_bytes(describe(mutable))


def test_schedule_deterministic_and_three_lanes() -> None:
    rows = [{"address": "a.py"}, {"address": "b.md"}, {"address": "c.py"}]
    plan = capture.schedule("0018", rows)
    assert plan == capture.schedule("0018", rows)
    assert len(plan["operations"]) == len(set(plan["operations"])) == 21
    assert sum(s.endswith(":A") for s in plan["operations"]) == 3
    assert sum(s.startswith("ri:references:") for s in plan["operations"]) == 2
    assert not any(s.endswith((":B", ":C")) for s in plan["operations"])
