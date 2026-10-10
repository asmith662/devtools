# Copyright (c) 2026
# ruff: noqa: COM812, S101, D103, PLR2004, ARG001 -- controlled Stage A assertions
"""Prospective reconstruction, no-execution, blindness and tamper contracts."""

from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING

import pytest

from devtools.context.localization import lexical as native_lexical
from devtools.context.localization.grounding import resolve as native_grounding
from devtools.context.python.modules import selection
from devtools.context.retrieval.lexical import bm25
from experiments.codex_dogfood.case_0009.artifacts import (
    binary,
    digest,
    json_bytes,
    put_text,
)
from experiments.codex_dogfood.case_0013 import blind, freeze, protocol
from experiments.exact_hint_routing import routing

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture
def no_execution(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args: object, **_kwargs: object) -> None:
        msg = "Case 0013 treatment execution prohibited"
        raise AssertionError(msg)

    for module, name in (
        (routing, "resolve"),
        (routing, "ground_task_anchor"),
        (native_grounding, "ground_task_anchor"),
        (native_grounding, "select_python_module_source_declarations"),
        (selection, "select_python_module_source_declarations"),
        (native_lexical, "acquire_localization_lexical_evidence"),
        (native_lexical, "retrieve_repository_text_documents_by_bm25"),
        (bm25, "retrieve_repository_text_documents_by_bm25"),
        (bm25, "retrieve_repository_text_documents_by_content_bm25"),
    ):
        monkeypatch.setattr(module, name, forbidden)
    # Frame preparation must not build even a query-independent retrieval index.
    from devtools.context.retrieval import lexical  # noqa: PLC0415

    monkeypatch.setattr(
        lexical, "build_repository_text_lexical_inverted_index", forbidden
    )


def test_task_matrix_intents_routes_and_complete_query_isolation(
    no_execution: None,
) -> None:
    t = protocol.definition()
    assert t == protocol.definition()
    assert (
        "".join(r["basis"]["text"] for r in t["task_requirement_matrix"])
        == t["task_text"]
    )
    assert all(r["obligations"] or r["exclusion"] for r in t["task_requirement_matrix"])
    assert len(t["obligations"]) == len(t["native_obligation_queries"]) == 9
    assert len(t["hint_inventory"]) == 10
    assert len(t["acquisition_intents"]) == 19
    assert [q["text"] for q in t["native_obligation_queries"]] == [
        o["query"] for o in t["obligations"]
    ]
    assert {i["need"]["obligation"]["value"] for i in t["acquisition_intents"]} == {
        o["key"] for o in t["obligations"]
    }
    assert [len(t["exact_route_requests"][a]) for a in ("A", "B", "C")] == [0, 10, 6]
    for h in t["hint_inventory"]:
        assert t["task_text"][h["span"]["start"] : h["span"]["end"]] == h["text"]
    assert set(t["execution"].values()) == {0}
    assert t["gold"] == "ABSENT"
    assert t["future_gold"]["model"] == "GPT-6 Astra"
    assert t["future_gold"]["reasoning"] == "High"
    assert t["settings"]["fusion"] is False
    assert {t["exact_route_requests"]["C"][n]["identity"] for n in range(6)} <= {
        r["identity"] for r in t["exact_route_requests"]["B"]
    }


def test_blind_allowlist_excludes_treatment_metadata(no_execution: None) -> None:
    resource = {
        "address": "src/fixture.py",
        "content_identity": "a" * 64,
        "text": "fixture\n",
        "encoding": "utf-8",
        "byte_size": 8,
        "rank": 999,
        "score": 999,
        "role": "forbidden",
        "arms": "forbidden",
    }
    packet = blind.packet_projection(protocol.definition(), [resource])
    assert set(packet) == {
        "case",
        "task_identity",
        "task_text",
        "obligations",
        "resources",
    }
    assert set(packet["resources"][0]) == {
        "address",
        "content_identity",
        "text",
        "encoding",
        "byte_size",
    }
    assert all(
        set(o)
        == {"identity", "key", "statement", "criterion", "applicability", "task_basis"}
        for o in packet["obligations"]
    )
    assert packet["case"] == "case-0013"


@pytest.fixture
def frozen_fixture(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, no_execution: None
) -> Path:
    blobs = {
        "src/pkg/native.py": b"class Native: pass\n",
        "docs/notes.md": b"Controlled fixture only\n",
    }
    frame, metadata = freeze.prepare_frame(blobs)
    values = asyncio.run(freeze.output(frame, metadata, blobs))
    assert values == asyncio.run(freeze.output(*freeze.prepare_frame(blobs), blobs))
    for name in freeze.AUTHORED:
        put_text(tmp_path / name, binary(freeze.CASE / name).decode())
    freeze.publish(values, tmp_path)

    async def committed() -> dict[str, bytes]:
        return blobs

    monkeypatch.setattr(freeze, "committed_blobs", committed)
    return tmp_path


def test_deterministic_fixture_replay(frozen_fixture: Path) -> None:
    r = asyncio.run(freeze.verify(frozen_fixture))
    assert r["replay"] == "PASSED"
    assert set(r["execution"].values()) == {0}
    assert binary(frozen_fixture / "TRACE.md") == binary(
        frozen_fixture / "STAGE_A_REVIEW.md"
    )
    schema = json.loads(binary(frozen_fixture / "trace.schema.json"))
    assert schema["properties"]["gold"]["const"] == "ABSENT"
    assert schema["properties"]["execution"]["const"] == r["execution"]


@pytest.mark.parametrize(
    "name", ["task.txt", "inputs.json.gz", "treatment.json", "STAGE_A_REVIEW.md"]
)
def test_tamper_rejected(frozen_fixture: Path, name: str) -> None:
    target = frozen_fixture / name
    target.write_bytes(target.read_bytes() + b"tamper")
    with pytest.raises(ValueError, match="hash differs"):
        asyncio.run(freeze.verify(frozen_fixture))


def test_resealed_semantic_mutation_rejected(frozen_fixture: Path) -> None:
    t = json.loads(binary(frozen_fixture / "treatment.json"))
    t["settings"]["k1"] = 999
    (frozen_fixture / "treatment.json").write_bytes(json_bytes(t))
    seal = json.loads(binary(frozen_fixture / "integrity.json"))
    seal["sha256"]["treatment.json"] = digest(binary(frozen_fixture / "treatment.json"))
    (frozen_fixture / "integrity.json").write_bytes(json_bytes(seal))
    with pytest.raises(ValueError, match="replay differs"):
        asyncio.run(freeze.verify(frozen_fixture))


def test_partial_complete_overwrite_and_execution_rejection(
    frozen_fixture: Path, tmp_path: Path
) -> None:
    values = {n: binary(frozen_fixture / n) for n in freeze.GENERATED}
    before = {p.name: p.read_bytes() for p in frozen_fixture.iterdir()}
    with pytest.raises(ValueError, match="overwrite"):
        freeze.publish(values, frozen_fixture)
    assert before == {p.name: p.read_bytes() for p in frozen_fixture.iterdir()}
    partial = tmp_path / "partial"
    put_text(partial / "trace.json", "existing")
    with pytest.raises(ValueError, match="overwrite"):
        freeze.publish(values, partial)
    assert not (partial / "treatment.json").exists()
    put_text(frozen_fixture / "execution_started.json", "forbidden")
    with pytest.raises(ValueError, match="execution/gold"):
        asyncio.run(freeze.verify(frozen_fixture))


def test_published_case_replay_if_present(no_execution: None) -> None:
    if not (freeze.CASE / "integrity.json").exists():
        return
    r = asyncio.run(freeze.verify())
    assert r["replay"] == "PASSED"
    assert set(r["execution"].values()) == {0}
