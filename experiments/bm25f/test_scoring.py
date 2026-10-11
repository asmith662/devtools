# Copyright (c) 2026
# ruff: noqa: E501, COM812, S101, PLR2004 -- controlled mathematical/mutation fixtures
"""Synthetic-only mathematical oracles; never prospective effectiveness tests."""

from __future__ import annotations

import copy
import json
import math
from dataclasses import replace
from typing import Any
from unittest.mock import patch

import pytest

from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.snapshot import (
    RepositorySnapshot,
    RepositorySnapshotId,
)
from devtools.context.retrieval.lexical.bm25 import (
    RepositoryTextLexicalBm25Settings,
    analyze_repository_text_lexical_query,
)
from devtools.context.retrieval.lexical.scoring import calculate_bm25_term_contribution
from experiments.bm25f.fields import FieldState, build_fields
from experiments.bm25f.scoring import Parameters, compare, field_evidence, score
from experiments.bm25f.trace import (
    attribution,
    envelope,
    render,
    serialize,
    validate_envelope,
    verify_score,
)
from tests.context.retrieval.lexical._helpers import _collection, _document


def fixture(*rows: tuple[str, str]) -> FieldState:
    """Construct synthetic canonical identities, never read a repository frame."""
    collection = _collection(tuple(_document(address, text) for address, text in rows))
    snapshot = RepositorySnapshot(
        RepositorySnapshotId("a" * 64),
        collection.corpus.definition.discovery.repository_id,
        collection.corpus.resources,
    )
    return build_fields(collection, snapshot)


def result(state: FieldState, text: str, **values: float) -> dict[str, Any]:
    """Score only caller-constructed synthetic fixtures."""
    return score(
        state,
        analyze_repository_text_lexical_query(text=text),
        snapshot_id=state.snapshot.id,
        parameters=Parameters(**values),
    )


def test_pre_saturation_single_idf_nonadditive_oracle() -> None:
    """Both fields combine before the only saturation, unlike independent native A."""
    state = fixture(("alpha.txt", "alpha alpha"), ("quiet.txt", "quiet quiet"))
    comparison = compare(
        state,
        analyze_repository_text_lexical_query(text="ALPHA alpha"),
        snapshot_id=state.snapshot.id,
    )
    t = comparison["B"]["matches"][0]["terms"][0]
    assert t["N"] == 2
    assert t["df_union"] == 1
    assert t["CONTENT"]["tf"] == 2
    assert t["FILENAME"]["tf"] == 1
    assert t["CONTENT"]["average_length"] == 2
    assert t["FILENAME"]["average_length"] == 1
    assert t["combined_tf"] == 2.25
    assert t["saturation_numerator"] == (1.2 + 1) * 2.25
    assert t["saturation_denominator"] == 1.2 + 2.25
    expected = math.log(2) * ((1.2 + 1) * 2.25) / (1.2 + 2.25)
    assert t["term_score"].hex() == expected.hex()
    assert comparison["A"][0]["score"] == pytest.approx(math.log(2) * 1.625)
    assert comparison["B"]["matches"][0]["score"] != pytest.approx(
        comparison["A"][0]["score"]
    )
    assert len(comparison["B"]["matches"][0]["terms"]) == 1
    assert len(comparison["B"]["query"]["observations"]) == 2
    assert comparison["B"]["field_statistics"]["query_terms"][0]["content_df"] == 1
    assert comparison["B"]["field_statistics"]["query_terms"][0]["filename_df"] == 1
    assert (
        len(
            comparison["B"]["field_statistics"]["query_terms"][0][
                "union_document_identities"
            ]
        )
        == 1
    )
    trace = attribution(comparison)[0]
    assert trace["A_rank"] == trace["B_rank"] == 1
    assert sum(
        trace["terms"][0][k]
        for k in (
            "union_idf_delta",
            "pre_saturation_weight_delta",
            "cross_field_single_saturation_delta",
        )
    ) == pytest.approx(trace["score_delta"])
    assert render(comparison) == render(comparison)
    assert "float_hex" in render(comparison)


@pytest.mark.parametrize("b", [0.0, 0.75, 1.0])
def test_single_field_equivalence_and_own_averages(b: float) -> None:
    """One matching field reduces algebraically to ordinary BM25 despite filename noise."""
    state = fixture(
        ("opaque.txt", "alpha alpha quiet"), ("other-long-name.md", "quiet")
    )
    t = result(state, "alpha", b_content=b)["matches"][0]["terms"][0]
    ordinary = calculate_bm25_term_contribution(
        term_frequency=2,
        inverse_document_frequency=math.log(2),
        document_length=3,
        average_document_length=2,
        settings=RepositoryTextLexicalBm25Settings(b=b),
    )
    assert t["term_score"] == pytest.approx(ordinary, rel=1e-15)
    assert t["FILENAME"]["tf"] == 0
    assert t["FILENAME"]["weighted_normalized_tf"] == 0
    assert t["CONTENT"]["average_length"] == 2
    assert t["FILENAME"]["average_length"] == 2
    assert t["CONTENT"]["normalization_denominator"] == 1 - b + b * 3 / 2


def test_union_df_disjoint_overlap_and_per_field_normalization() -> None:
    """Union membership spans content-only, filename-only and both without duplicates."""
    state = fixture(
        ("a/alpha.txt", "alpha"),
        ("b/alpha-long.txt", "quiet quiet quiet"),
        ("c/opaque.txt", "alpha alpha"),
        ("d/quiet.txt", ""),
    )
    r = result(
        state, "alpha missing", b_content=0.5, b_filename=0.25, filename_weight=0.5
    )
    assert len(r["matches"]) == 3
    for row in r["matches"]:
        t = row["terms"][0]
        assert t["df_union"] == 3
        assert t["N"] == 4
        assert t["CONTENT"]["average_length"] == 1.5
        assert t["FILENAME"]["average_length"] == 1.25
        assert t["FILENAME"]["weight"] == 0.5
        assert (
            t["combined_tf"]
            == t["CONTENT"]["weighted_normalized_tf"]
            + t["FILENAME"]["weighted_normalized_tf"]
        )
        assert row["terms"][1]["term_score"] == 0
    assert field_evidence(0, 0, 0, 1.0, 0.25)["normalized_tf"] == 0
    assert field_evidence(0, 0, 1, 1.0, 0.25)["normalized_tf"] == 0
    with pytest.raises(ValueError, match="counts"):
        field_evidence(1, 1, 0, 0.75, 1)


@pytest.mark.parametrize(
    "text", ["alpha", "contentonly", "alpha contentonly", "missing", ""]
)
def test_candidate_union_no_addition_loss_and_canonical_ties(text: str) -> None:
    """Identical membership includes filename-only candidates and excludes zero matches."""
    state = fixture(
        ("z/alpha.txt", ""), ("a/alpha.txt", ""), ("b/opaque.txt", "contentonly")
    )
    comparison = compare(
        state,
        analyze_repository_text_lexical_query(text=text),
        snapshot_id=state.snapshot.id,
    )
    assert {r["document_identity"] for r in comparison["A"]} == {
        r["document_identity"] for r in comparison["B"]["matches"]
    }
    assert comparison["candidate_identity"] == "PASS"
    if text == "alpha":
        assert [r["address"] for r in comparison["B"]["matches"]] == [
            "a/alpha.txt",
            "z/alpha.txt",
        ]
        assert (
            comparison["B"]["matches"][0]["score"]
            == comparison["B"]["matches"][1]["score"]
        )


def test_empty_filename_and_unchanged_filename_representation() -> None:
    """Punctuation-only stems have no evidence; directories and extensions never enter."""
    state = fixture(("alpha/---.txt", "alpha"), ("beta/Request_Assembly.py", "quiet"))
    r = result(state, "alpha Request_Assembly py beta")
    assert {t.normalized_term for t in state.filename.document_frequencies} == {
        "request_assembly"
    }
    assert state.filename.average_document_length == 0.5
    assert len(r["matches"]) == 2
    assert result(state, "py beta")["matches"] == []
    empty = fixture(("---.txt", "alpha"), ("!!!.txt", "quiet"))
    assert (
        result(empty, "alpha")["matches"][0]["terms"][0]["FILENAME"]["average_length"]
        == 0
    )


@pytest.mark.parametrize(
    "values",
    [
        {"filename_weight": 0},
        {"content_weight": -1},
        {"k1": 0},
        {"b_filename": 1.01},
        {"b_content": -0.1},
        {"k1": math.inf},
        {"content_weight": math.nan},
    ],
)
def test_invalid_parameters_rejected(values: dict[str, float]) -> None:
    """Weights must be positive and every frozen coefficient finite/in-range."""
    with pytest.raises(ValueError, match="parameters"):
        Parameters(**values)


@pytest.mark.parametrize("weight", [0.01, 0.25, 1.0, 10.0])
def test_positive_weights_preserve_candidates(weight: float) -> None:
    """Synthetic alternative weights test the invariant, never select a Case 0015 weight."""
    state = fixture(("alpha.txt", ""), ("opaque.txt", "alpha"))
    assert len(result(state, "alpha", filename_weight=weight)["matches"]) == 2


def test_foreign_stale_frames_query_and_observations_rejected() -> None:
    """Exact frames include content and ordered document identity, not filename mapping."""
    state = fixture(("alpha.txt", "alpha"), ("quiet.txt", "quiet"))
    with pytest.raises(ValueError, match="snapshot"):
        score(
            state,
            analyze_repository_text_lexical_query(text="alpha"),
            snapshot_id=RepositorySnapshotId("b" * 64),
        )
    foreign = replace(
        state.snapshot,
        repository_id=RepositoryId.parse("00000000-0000-4000-8000-000000000002"),
    )
    with pytest.raises(ValueError, match="frame"):
        build_fields(state.collection, foreign)
    with pytest.raises(ValueError, match="frame"):
        build_fields(
            state.collection,
            replace(state.snapshot, resources=state.snapshot.resources[::-1]),
        )
    with pytest.raises(ValueError, match="tamper"):
        result(
            replace(state, filename=replace(state.filename, average_document_length=2)),
            "alpha",
        )
    query = analyze_repository_text_lexical_query(text="alpha")
    with pytest.raises(ValueError, match="query"):
        score(state, replace(query, observations=()), snapshot_id=state.snapshot.id)


@pytest.mark.parametrize(
    "field",
    [
        "score",
        "tf",
        "length",
        "average_length",
        "b",
        "weight",
        "normalized_tf",
        "combined_tf",
        "df_union",
        "N",
        "idf_union",
        "saturation_numerator",
        "saturation_denominator",
        "term_score",
        "content_observations",
        "document_identity",
        "rank",
    ],
)
def test_exact_score_provenance_replay_and_mutation_rejection(field: str) -> None:
    """Every scientific intermediate and identity is checked against canonical evidence."""
    state = fixture(("alpha.txt", "alpha alpha"), ("quiet.txt", "quiet quiet"))
    r = result(state, "alpha")
    verify_score(r, state)
    changed = copy.deepcopy(r)
    row = changed["matches"][0]
    if field in {"score", "rank", "document_identity"}:
        row[field] = "TAMPER"
    elif field in row["terms"][0]["CONTENT"]:
        row["terms"][0]["CONTENT"][field] = "TAMPER"
    else:
        row["terms"][0][field] = "TAMPER"
    with pytest.raises(ValueError, match="tamper"):
        verify_score(changed, state)
    raw = envelope(r)
    assert validate_envelope(raw) == json.loads(serialize(r))
    assert raw == envelope(r)
    modified = json.loads(raw)
    modified["payload"]["matches"][0]["rank"] = 99
    with pytest.raises(ValueError, match="tamper"):
        validate_envelope(serialize(modified))


@pytest.mark.parametrize("change", ["loss", "addition", "duplicate"])
def test_candidate_mismatch_is_rejected_without_union_repair(change: str) -> None:
    """Mutation of either arm's captured set is a contract defect, never repaired."""
    state = fixture(("alpha.txt", "alpha"), ("quiet.txt", "quiet"))
    r = result(state, "alpha")
    if change == "loss":
        r["matches"] = []
    elif change == "addition":
        extra = copy.deepcopy(r["matches"][0])
        extra["document_identity"] = "foreign"
        r["matches"].append(extra)
    else:
        r["matches"].append(copy.deepcopy(r["matches"][0]))
    with (
        patch("experiments.bm25f.scoring.score", return_value=r),
        pytest.raises(ValueError, match="EXPERIMENTAL_CONTRACT_DEFECT"),
    ):
        compare(
            state,
            analyze_repository_text_lexical_query(text="alpha"),
            snapshot_id=state.snapshot.id,
        )
