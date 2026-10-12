# Copyright (c) 2026
# ruff: noqa: TRY003, EM101, COM812, S101 -- synthetic arithmetic and durability guards
"""Synthetic-only native/oracle/journal tests, never prospective effectiveness."""

from __future__ import annotations

import copy
from contextlib import ExitStack
from dataclasses import asdict, replace
from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest

from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from experiments.bm25f.scoring import score
from experiments.bm25f.test_scoring import fixture
from experiments.codex_dogfood.case_0012.stage_b.durability import Journal, exclusive
from experiments.codex_dogfood.case_0015.stage_b import execute, reporting, validation

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any


def capture(text: str = "alpha quiet") -> tuple[Any, ...]:
    """Prepare controlled non-repository input and invoke synthetic arms only."""
    state = fixture(
        ("alpha.txt", "alpha alpha"), ("quiet.txt", ""), ("---.txt", "quiet")
    )
    query = analyze_repository_text_lexical_query(text=text)
    q = {"analysis": asdict(query), "normalized_terms": query.normalized_terms}
    union = execute.union_statistics(state)
    surface = validation.validate_fields(state, union)
    native = retrieve_repository_text_documents_by_bm25(
        query=query, index=state.content, maximum_results=3
    )
    b = score(state, query, snapshot_id=state.snapshot.id)
    return state, union, surface, native, b, q


def test_split_preparation_exactly_matches_frozen_builder() -> None:
    """Journal boundaries preserve exact frozen field/index objects and fingerprint."""
    state, *_rest = capture()
    frame = execute.PreparedFrame(state.collection, state.snapshot)
    fields = execute.prepare_fields(frame)
    split = execute.prepare_index(frame, fields)
    assert split == state


@pytest.mark.parametrize("text", ["alpha", "quiet", "ALPHA alpha quiet", "missing", ""])
def test_complete_pair_formula_statistics_and_diagnostics(text: str) -> None:
    """Native A and frozen B reconstruct without rerunning either treatment."""
    state, union, surface, native, b, q = capture(text)
    with (
        patch.object(execute, "score", side_effect=AssertionError("No replay scorer")),
        patch.object(
            execute,
            "retrieve_repository_text_documents_by_bm25",
            side_effect=AssertionError("No native replay"),
        ),
    ):
        comparison = validation.validate_pair(state, native, b, surface, union, q)
        rows, aggregates = reporting.decomposition(comparison)
        assert all(r["reconstruction"] == "PASS" for r in rows)
        assert set(aggregates) == {
            "union_idf_delta",
            "pre_saturation_weight_delta",
            "cross_field_single_saturation_delta",
        }
        pair = reporting.pairwise(comparison["A"], b["matches"])
        assert set(pair["top_k"]) == {"10", "20", "50"}
        assert len(reporting.joined(comparison, union)) == len(b["matches"])


@pytest.mark.parametrize(
    "field",
    [
        "combined_tf",
        "df_union",
        "idf_union",
        "saturation_numerator",
        "saturation_denominator",
        "term_score",
        "query_multiplier",
        "content_observations",
    ],
)
def test_b_contribution_tamper_rejected(field: str) -> None:
    """One saturation, one IDF and every intermediate are exact identities."""
    state, union, surface, native, b, q = capture()
    b["matches"][0]["terms"][0][field] = "TAMPER"
    with pytest.raises(ValueError, match="BM25F_APPLICATION_DEFECT"):
        validation.validate_pair(state, native, b, surface, union, q)


def test_candidate_field_and_native_score_tamper() -> None:
    """Missing/duplicate candidates are contract defects; native A is authoritative."""
    state, union, surface, native, b, q = capture()
    changed = copy.deepcopy(b)
    changed["matches"].pop()
    with pytest.raises(ValueError, match="CONTRACT_DEFECT"):
        validation.validate_pair(state, native, changed, surface, union, q)
    changed = copy.deepcopy(b)
    changed["matches"].append(changed["matches"][0])
    with pytest.raises(ValueError, match="duplicate"):
        validation.validate_pair(state, native, changed, surface, union, q)
    altered = replace(
        native, matches=(replace(native.matches[0], score=999.0), *native.matches[1:])
    )
    with pytest.raises(ValueError, match="authenticity"):
        validation.validate_pair(state, altered, b, surface, union, q)
    union["terms"]["alpha"]["df_union"] += 1
    with pytest.raises(ValueError, match="DF_DEFECT"):
        validation.validate_fields(state, union)


def test_journal_exact_return_recovery_and_no_retry(tmp_path: Path) -> None:
    """Durable shared identities survive loading and operations cannot execute again."""
    j = Journal.start(tmp_path, {"execution": "synthetic-only"})
    value = ["synthetic"]
    assert j.call("once", {}, lambda: value) is value
    j.complete()
    recovered = Journal.load(tmp_path)
    assert recovered.state["values"]["once"] == value
    with pytest.raises(ValueError, match="already entered"):
        j.call("once", {}, lambda: value)
    with pytest.raises(ValueError, match="Loaded"):
        recovered.call("other", {}, lambda: value)
    with pytest.raises(FileExistsError):
        Journal.start(tmp_path, {"execution": "synthetic-only"})


def test_failed_return_publication_and_native_raise_stop(tmp_path: Path) -> None:
    """Returned-but-undurable and raised operations are never retried."""
    j = Journal.start(tmp_path / "undurable", {"execution": "synthetic-only"})
    calls = []
    original = j.event

    def event(sequence: int, status: str, payload: dict[str, object]) -> None:
        if status == "RETURNED":
            raise OSError("synthetic publication failure")
        original(sequence, status, payload)

    def invoke() -> int:
        calls.append(1)
        return 7

    with patch.object(j, "event", event), pytest.raises(OSError, match="publication"):
        j.call("once", {}, invoke)
    assert calls == [1]
    with pytest.raises(ValueError, match="already entered"):
        j.call("once", {}, invoke)
    with pytest.raises(ValueError, match="Unrecoverable"):
        Journal.load(tmp_path / "undurable").ready()
    other = Journal.start(tmp_path / "raise", {"execution": "synthetic-only"})

    def fail() -> None:
        raise RuntimeError("synthetic native failure")

    with pytest.raises(RuntimeError):
        other.call("once", {}, fail)
    with pytest.raises(ValueError, match="Unrecoverable"):
        Journal.load(tmp_path / "raise").ready()
    with pytest.raises(FileExistsError):
        exclusive(tmp_path / "raise/execution.claim", {})


def test_publication_overwrite_refusal_and_incomplete_stop(tmp_path: Path) -> None:
    """Publication checks absence/completion before any reconstruction work."""
    (tmp_path / "arm_a.json.gz").write_bytes(b"synthetic")
    with pytest.raises(FileExistsError):
        reporting.publish(tmp_path)
    with pytest.raises(ValueError, match="complete successful"):
        reporting.data(tmp_path / "missing")


def test_durable_replay_has_no_native_invocations() -> None:
    """Captured mechanical replay is valid with every scientific entry point blocked."""
    if not (execute.CAPTURE / "integrity.json").exists():
        pytest.skip("Prospective capture has not executed; no native invocation")
    targets = (
        "experiments.codex_dogfood.case_0015.stage_b.execute.prepare",
        "experiments.codex_dogfood.case_0015.stage_b.execute.prepare_fields",
        "experiments.codex_dogfood.case_0015.stage_b.execute.prepare_index",
        "experiments.codex_dogfood.case_0015.stage_b.execute.union_statistics",
        "experiments.codex_dogfood.case_0015.stage_b.execute.score",
        "experiments.codex_dogfood.case_0015.stage_b.execute.retrieve_repository_text_documents_by_bm25",
        "experiments.bm25f.scoring.score",
        "devtools.context.retrieval.lexical.index.build_repository_text_lexical_inverted_index",
        "devtools.context.retrieval.lexical.bm25.retrieve_repository_text_documents_by_bm25",
        "devtools.context.retrieval.lexical.filename.build_repository_text_filename_lexical_index",
    )
    with ExitStack() as stack:
        for target in targets:
            stack.enter_context(
                patch(target, side_effect=AssertionError("Scientific rerun forbidden"))
            )
        reporting.verify(execute.CAPTURE)
