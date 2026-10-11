# Copyright (c) 2026
# ruff: noqa: E501, COM812, S101, PLR2004 -- prospective scientific guard assertions
"""Observation-only replay, exact task binding and blind/no-execution guards."""

from __future__ import annotations

import asyncio
import json
from contextlib import ExitStack
from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest

from experiments.codex_dogfood.case_0009.artifacts import json_bytes, put_text
from experiments.codex_dogfood.case_0015 import blind, freeze, protocol

if TYPE_CHECKING:
    from pathlib import Path


def test_task_obligation_query_binding_and_parameters() -> None:
    """Every substantive clause has a mandatory matching query, without query weighting."""
    d = protocol.authored()
    assert d == protocol.authored()
    assert len(d["queries"]) == len(d["requirement_matrix"]) == 6
    assert set(d["arms"]) == {"A", "B"}
    assert d["parameters"] == {
        "k1": 1.2,
        "content_weight": 1.0,
        "filename_weight": 0.25,
        "b_content": 0.75,
        "b_filename": 0.75,
    }
    for obligation, query in zip(d["requirement_matrix"], d["queries"], strict=True):
        span = obligation["task_span"]
        assert d["task_text"][span["start"] : span["end"]] == obligation["task_clause"]
        assert query["obligation"] == obligation["identity"]
        assert query["identity"] == obligation["query_identity"]
        assert query["all_term_multipliers"] == 1.0
        assert query["text"] == query["analysis"]["text"]
        assert obligation["mandatory"]
        assert obligation["applicability"] == "APPLICABLE"
    assert d["no_execution"] == protocol.COUNTS
    assert d["gold_policy"]["automatic_second_reviewer"] is False


def test_no_prospective_scientific_operation_can_run_during_replay() -> None:
    """Patch both canonical entry points and imported aliases; any call fails immediately."""
    targets = (
        "devtools.context.retrieval.lexical.index.build_repository_text_lexical_inverted_index",
        "devtools.context.retrieval.lexical.filename.build_repository_text_filename_lexical_index",
        "devtools.context.retrieval.lexical.bm25.retrieve_repository_text_documents_by_bm25",
        "devtools.context.retrieval.lexical.bm25.retrieve_repository_text_documents_by_content_bm25",
        "devtools.context.retrieval.lexical.statistics.calculate_repository_text_lexical_corpus_statistics",
        "devtools.context.retrieval.lexical.analysis.analyze_repository_text_document_collection",
        "experiments.bm25f.fields.build_repository_text_lexical_inverted_index",
        "experiments.bm25f.fields.build_repository_text_filename_lexical_index",
        "experiments.bm25f.fields.calculate_repository_text_lexical_corpus_statistics",
        "experiments.bm25f.fields.analyze_repository_text_document_collection",
        "experiments.bm25f.fields.build_fields",
        "experiments.bm25f.scoring.retrieve_repository_text_documents_by_bm25",
        "experiments.bm25f.scoring.score",
        "experiments.bm25f.scoring.compare",
    )
    with ExitStack() as stack:
        for target in targets:
            stack.enter_context(
                patch(
                    target,
                    side_effect=AssertionError("Prospective execution forbidden"),
                )
            )
        asyncio.run(freeze.verify(protocol.CASE))


def test_blind_projection_leakage_guards() -> None:
    """Experimental metadata is excluded; original natural text/obligations retained."""
    keys = (
        "repository_id",
        "snapshot_id",
        "corpus_id",
        "document_identity",
        "address",
        "content_identity",
        "encoding",
        "utf8_bytes",
        "content",
    )
    resource = dict.fromkeys(keys, "synthetic natural text")
    resource.update(
        dict.fromkeys(
            (
                "scores",
                "ranks",
                "df",
                "idf",
                "weights",
                "formula",
                "field_definitions",
                "gates",
                "costs",
                "outcome",
                "queries",
                "candidate_results",
            ),
            "SECRET_EXPERIMENT",
        )
    )
    design = protocol.authored()
    packet = blind.packet(design, [resource])
    assert list(packet) == protocol.GOLD_POLICY["allowed"]
    assert "SECRET_EXPERIMENT" not in json.dumps(packet)
    assert "query_identity" not in json.dumps(packet)
    assert packet["task_text"] == design["task_text"]
    assert packet["eligible_resources"][0]["content"] == resource["content"]
    assert packet == blind.packet(json.loads(json_bytes(design)), [resource])
    with pytest.raises(ValueError, match="Duplicate"):
        blind.packet(design, [resource, resource])
    design["queries"] = []
    with pytest.raises(ValueError, match="frozen"):
        blind.packet(design, [resource])


def test_overwrite_tamper_and_no_execution_rejection(tmp_path: Path) -> None:
    """Serialized synthetic artifacts test publication; no prospective scoring occurs."""
    values = {name: json_bytes({"name": name}) for name in freeze.GENERATED}

    async def expected() -> dict[str, bytes]:
        return values

    with patch.object(freeze, "expected", expected):
        asyncio.run(freeze.publish(tmp_path))
        asyncio.run(freeze.verify(tmp_path))
        with pytest.raises(FileExistsError):
            asyncio.run(freeze.publish(tmp_path))
        (tmp_path / "trace.json").write_bytes(b"tamper")
        with pytest.raises(ValueError, match="tamper"):
            asyncio.run(freeze.verify(tmp_path))
    for name in (*freeze.FORBIDDEN, "unrecognized-ranking.bin"):
        folder = tmp_path / ("probe-" + name.replace(".", "-"))
        put_text(folder / name, "{}")
        with pytest.raises(ValueError, match=r"forbidden|Unexpected"):
            freeze.no_execution(folder)


def test_eligibility_and_selection_criteria() -> None:
    """Eligibility is broad and independent of task/query; held-out excluded before reads."""
    assert freeze.eligible("src/devtools/resources/filesystem/reading.py")
    for address in (
        "tests/confirmation/a.py",
        "docs/reserve/a.md",
        "tests/experiments/a.py",
        ".local/codex-result.md",
        "experiments/bm25f/scoring.py",
    ):
        assert not freeze.eligible(address)
    criteria = json.loads((protocol.CASE / "SELECTION_CRITERIA.json").read_text())
    assert criteria["frozen_before_final_task_authoring"]
    assert criteria["source_head"] == protocol.START
    assert freeze.PRIOR_CASE.search(b"Case 0014 gold")
