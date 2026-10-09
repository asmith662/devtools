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
    git,
    json_bytes,
    put_text,
)
from experiments.codex_dogfood.case_0012 import amendment, blind, freeze, protocol
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


def test_bc_route_equivalence_and_contract(no_execution: None) -> None:
    treatment = protocol.definition()
    clarification = amendment.definition(treatment)
    b, c = (treatment["exact_route_requests"][arm] for arm in ("B", "C"))
    assert [r["identity"] for r in b] == [r["identity"] for r in c]
    assert [(r["locator"], r["association"], r["mechanism"]) for r in b] == [
        (r["locator"], r["association"], r["mechanism"]) for r in c
    ]
    contract = clarification["bc_equivalence"]
    assert set(contract["forbidden_differences"]) == {
        "resolution disposition",
        "native target",
        "promoted resource",
        "routed order",
        "fallback candidate membership",
        "fallback order",
        "native rank",
        "native score",
    }
    assert "EXPERIMENTAL_CONTRACT_DEFECT" in contract["failure"]
    assert "measurement noise" in contract["cost"]
    assert "does not provide a differential effectiveness test" in contract["scope"]
    c[0]["identity"] = "tampered"
    with pytest.raises(ValueError, match="identities differ"):
        amendment.definition(treatment)


def test_route_family_partition_and_review_decisions(no_execution: None) -> None:
    treatment = protocol.definition()
    clarification = amendment.definition(treatment)
    families = clarification["route_families"]
    assert {f: tuple(v["hints"]) for f, v in families.items()} == {
        "RESOURCE_ADDRESS": ("H07", "H08", "H09", "H10"),
        "PYTHON_DIRECT_DECLARATION": ("H01", "H02"),
        "PYTHON_MODULE": ("H03",),
        "PYTHON_DIRECT_METHOD": ("H04",),
        "UNSUPPORTED_BARE_CLASS": ("H05", "H06"),
    }
    members = [h for v in families.values() for h in v["hints"]]
    assert len(members) == len(set(members)) == 10
    assert sum(v["admitted_route_count"] for v in families.values()) == 8
    assert all(
        v["required_future_fields"] == list(amendment.FIELDS) for v in families.values()
    )
    routes = treatment["exact_route_requests"]["B"]
    assert routes[2]["association"]["lane"]["value"] == "choices"
    assert sum(r["hint"]["text"] == "devtools.context.planning" for r in routes) == 1
    for n in (4, 5):
        assert routes[n]["locator"] is None
        assert routes[n]["mechanism"] == "UNSUPPORTED_EXACT_HINT"
    assert "not failed extraction" in clarification["family_reporting"]
    assert "not the primary U2 baseline arm" in clarification["baseline_scope"]
    assert "obligation-level canonical BM25" in clarification["baseline_scope"]


def test_family_conclusion_scope_without_execution(no_execution: None) -> None:
    counts = dict.fromkeys(amendment.FAMILIES, 0)
    assert all(
        amendment.conclusion_scope(counts, frozenset())[f] == "NOT_ASSESSED"
        for f in counts
    )
    counts["RESOURCE_ADDRESS"] = 1
    result = amendment.conclusion_scope(counts, frozenset({"RESOURCE_ADDRESS"}))
    assert (
        result["conclusion"] == "exact repository-path routing supported in Case 0012"
    )
    assert result["PYTHON_DIRECT_DECLARATION"] == "NOT_ASSESSED"
    counts["PYTHON_DIRECT_METHOD"] = 1
    result = amendment.conclusion_scope(counts, frozenset({"PYTHON_DIRECT_METHOD"}))
    assert (
        result["conclusion"] == "Case 0012 value established for: PYTHON_DIRECT_METHOD"
    )
    with pytest.raises(ValueError, match="REQUIRED target"):
        amendment.conclusion_scope(counts, frozenset({"PYTHON_MODULE"}))
    assert "HELPFUL_ONLY-only" in amendment.SCOPE["no_required_target"]
    assert "Do not claim empirical support" in amendment.SCOPE["path_only"]


def test_amendment_correspondence_and_original_treatment(no_execution: None) -> None:
    trace = json.loads(binary(freeze.CASE / "trace.json"))
    clarification = amendment.definition(protocol.definition())
    assert trace["clarification"] == clarification
    from experiments.codex_dogfood.case_0012 import reporting  # noqa: PLC0415

    for name in ("TRACE.md", "STAGE_A_REVIEW.md", "PROTOCOL.md"):
        assert amendment.review(clarification) in binary(freeze.CASE / name).decode()
    assert binary(freeze.CASE / "STAGE_A_REVIEW.md").decode() == reporting.review(
        protocol.definition(), trace["frame"]
    )
    assert clarification["history"]["original_stage_a_checkpoint"] == amendment.ORIGINAL
    assert set(clarification["execution"].values()) == {0}
    protected = (
        "task.txt",
        "TASK_REQUIREMENT_MATRIX.md",
        "treatment.json",
        "frame.json",
        "inputs.json.gz",
        "resources.json.gz",
        "AUTHORING.md",
        "SELECTION.md",
        "STAGE_C_PROTOCOL.md",
    )
    for name in protected:
        original = asyncio.run(
            git(
                "show",
                amendment.ORIGINAL + ":experiments/codex_dogfood/case_0012/" + name,
            )
        )
        assert binary(freeze.CASE / name) == original


def test_amendment_overwrite_refusal(
    no_execution: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def mock_git(*args: str) -> bytes:
        if args == ("rev-parse", "HEAD"):
            return amendment.ORIGINAL.encode()
        if args == ("branch", "--show-current"):
            return b"main"
        if args[0] == "show":
            return b'{"sha256":{},"scope":"original"}'
        raise AssertionError(args)

    monkeypatch.setattr(freeze, "git", mock_git)
    before = binary(freeze.CASE / "integrity.json")
    with pytest.raises(ValueError, match="overwrite refused"):
        asyncio.run(freeze.amend())
    assert binary(freeze.CASE / "integrity.json") == before
