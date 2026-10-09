# Copyright (c) 2026
# ruff: noqa: COM812, S101, D103, PLR2004, ARG001, EM101, TRY003 -- fixture activation/assertions; formatter owns commas
"""Stage A task coverage, no execution, leakage, tamper and overwrite contracts."""

from __future__ import annotations

import asyncio
import gzip
import json
from typing import TYPE_CHECKING

import pytest

from devtools.context.localization import lexical as native_lexical
from devtools.context.localization.grounding import resolve as native_grounding
from devtools.context.python.modules import selection as native_selection
from devtools.context.retrieval.lexical import bm25
from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    json_bytes,
    put_text,
)
from experiments.codex_dogfood.case_0012 import blind, freeze, protocol
from experiments.exact_hint_routing import routing

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture
def no_execution(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("Case treatment execution prohibited in Stage A")

    monkeypatch.setattr(routing, "resolve", forbidden)
    monkeypatch.setattr(routing, "ground_task_anchor", forbidden)
    monkeypatch.setattr(native_grounding, "ground_task_anchor", forbidden)
    monkeypatch.setattr(
        native_lexical, "acquire_localization_lexical_evidence", forbidden
    )
    monkeypatch.setattr(
        native_lexical, "retrieve_repository_text_documents_by_bm25", forbidden
    )
    monkeypatch.setattr(
        native_selection, "select_python_module_source_declarations", forbidden
    )
    monkeypatch.setattr(
        native_grounding, "select_python_module_source_declarations", forbidden
    )
    monkeypatch.setattr(bm25, "retrieve_repository_text_documents_by_bm25", forbidden)
    monkeypatch.setattr(
        bm25, "retrieve_repository_text_documents_by_content_bm25", forbidden
    )


def test_complete_task_matrix_and_task_only_hints(no_execution: None) -> None:
    treatment = protocol.definition()
    assert treatment == protocol.definition()
    assert len(treatment["obligations"]) == 9
    assert len(treatment["native_task_interpretation"]["obligations"]) == 9
    assert [q["text"] for q in treatment["native_obligation_queries"]] == [
        o["query"] for o in treatment["obligations"]
    ]
    text = treatment["task_text"]
    assert ".local/codex-result.md" not in text
    matrix = treatment["task_requirement_matrix"]
    assert "".join(row["basis"]["text"] for row in matrix) == text
    assert all(row["obligations"] and row["exclusion"] is None for row in matrix)
    assert {owner for row in matrix for owner in row["obligations"]} == {
        o["key"] for o in treatment["obligations"]
    }
    for hint in treatment["caller_reviewed_hint_reference"]:
        assert text[hint["span"]["start"] : hint["span"]["end"]] == hint["text"]
    agreement = treatment["extraction_agreement"]
    assert agreement["caller_count"] == 10
    assert agreement["rule_count"] == 10
    assert agreement["accepted_rule_hints"] == 10
    assert agreement["false_rule_extractions"] == 0
    assert agreement["caller_only_hints"] == 0
    assert agreement["type_disagreements"] == 0
    for arm in ("B", "C"):
        routes = treatment["exact_route_requests"][arm]
        assert len(routes) == 10
        assert sum(r["locator"] is None for r in routes) == 2
        assert len({r["identity"] for r in routes}) == len(routes)
    assert treatment["lexical_query_executions"] == 0
    assert treatment["exact_route_executions"] == 0
    assert treatment["gold"] == "ABSENT"
    assert treatment["effectiveness"] == "UNKNOWN"


def test_blind_projection_allowlist(no_execution: None) -> None:
    treatment = protocol.definition()
    resource = {
        "address": "src/fixture.py",
        "content_identity": "a" * 64,
        "text": "def native(): pass\n",
        "encoding": "utf-8",
        "byte_size": 19,
        "score": 999,
        "exact_resolution": "forbidden",
        "locator": "forbidden",
    }
    packet = blind.packet_projection(treatment, [resource])
    assert set(packet) == {
        "case",
        "task_identity",
        "task_text",
        "obligations",
        "resources",
    }
    forbidden = {
        "query",
        "analyzed_terms",
        "hint",
        "hints",
        "routes",
        "locator",
        "score",
        "rank",
        "cost",
        "arms",
        "resolution",
        "exact_resolution",
    }
    assert not forbidden & set(packet["resources"][0])
    for o in packet["obligations"]:
        assert not forbidden & set(o)
    assert "caller_reviewed_hint_reference" not in packet
    assert "rule_extracted_hints" not in packet


@pytest.fixture
def frozen_fixture(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, no_execution: None
) -> Path:
    blobs = {
        "src/pkg/native.py": b"class Target: pass\n",
        "docs/notes.md": b"fixture docs\n",
    }
    frame, metadata = freeze.prepare_frame(blobs)
    output = freeze.artifacts(frame, metadata, blobs)
    assert output == freeze.artifacts(*freeze.prepare_frame(blobs), blobs)
    for name in freeze.AUTHORED:
        put_text(tmp_path / name, binary(freeze.CASE / name).decode())
    freeze.publish(output, tmp_path)

    async def committed() -> dict[str, bytes]:
        return blobs

    monkeypatch.setattr(freeze, "committed_blobs", committed)
    return tmp_path


def test_deterministic_protocol_input_trace_replay(frozen_fixture: Path) -> None:
    result = asyncio.run(freeze.verify(frozen_fixture))
    assert result["replay"] == "PASSED"
    assert result["exact_route_executions"] == 0
    assert result["lexical_query_executions"] == 0
    trace = json.loads(binary(frozen_fixture / "trace.json"))
    treatment = json.loads(binary(frozen_fixture / "treatment.json"))
    assert trace["treatment"] == treatment
    assert trace["results"] == "ABSENT"
    assert binary(frozen_fixture / "TRACE.md") == binary(
        frozen_fixture / "STAGE_A_REVIEW.md"
    )
    assert set(trace["execution"].values()) == {0}
    assert (
        len(
            json.loads(gzip.decompress(binary(frozen_fixture / "resources.json.gz")))[
                "resources"
            ]
        )
        == 2
    )
    seal = json.loads(binary(frozen_fixture / "pre_execution.json"))
    for path, expected in seal["implementation_sha256"].items():
        if path.startswith("experiments/"):
            assert digest(binary(ROOT / path)) == expected
    schema = json.loads(binary(frozen_fixture / "trace.schema.json"))
    assert set(schema["required"]) == set(trace)
    assert schema["properties"]["execution"]["const"] == trace["execution"]
    assert not schema["properties"]["treatment"]["additionalProperties"]
    assert set(schema["properties"]["treatment"]["required"]) == set(treatment)


@pytest.mark.parametrize(
    "filename", ["treatment.json", "inputs.json.gz", "STAGE_A_REVIEW.md"]
)
def test_tamper_rejection(frozen_fixture: Path, filename: str) -> None:
    target = frozen_fixture / filename
    target.write_bytes(target.read_bytes() + b"tamper")
    with pytest.raises(ValueError, match="hash differs"):
        asyncio.run(freeze.verify(frozen_fixture))


def test_resealed_semantic_tamper_rejection(frozen_fixture: Path) -> None:
    treatment = json.loads(binary(frozen_fixture / "treatment.json"))
    treatment["settings"]["k1"] = 5
    target = frozen_fixture / "treatment.json"
    target.write_bytes(json_bytes(treatment))
    seal = json.loads(binary(frozen_fixture / "integrity.json"))
    seal["sha256"]["treatment.json"] = digest(binary(target))
    (frozen_fixture / "integrity.json").write_bytes(json_bytes(seal))
    with pytest.raises(ValueError, match="replay differs"):
        asyncio.run(freeze.verify(frozen_fixture))


def test_overwrite_refusal_complete_and_partial(
    frozen_fixture: Path, tmp_path: Path
) -> None:
    before = {p.name: p.read_bytes() for p in frozen_fixture.iterdir()}
    with pytest.raises(ValueError, match="overwrite"):
        freeze.publish({"trace.json": b"changed"}, frozen_fixture)
    assert {p.name: p.read_bytes() for p in frozen_fixture.iterdir()} == before
    partial = tmp_path / "partial"
    put_text(partial / "trace.json", "already exists")
    with pytest.raises(ValueError, match="overwrite"):
        freeze.publish({"treatment.json": b"new", "trace.json": b"changed"}, partial)
    assert not (partial / "treatment.json").exists()


def test_published_stage_a_no_outcomes_if_present(no_execution: None) -> None:
    if not (freeze.CASE / "integrity.json").exists():
        return
    result = asyncio.run(freeze.verify())
    assert result["replay"] == "PASSED"
    assert not any((freeze.CASE / name).exists() for name in freeze.FORBIDDEN)
