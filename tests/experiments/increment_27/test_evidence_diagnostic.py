# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Saved-evidence dataset and diagnostic reproducibility checks."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any, cast

from experiments.increment_27.depth_diagnostic import (
    _read_json,
    canonical_json_bytes,
    sha256_file,
)
from experiments.increment_27.evidence_diagnostic import (
    ANALYSIS_NAME,
    DATASET_NAME,
    FEATURE_CLASSES,
    build_analysis,
    build_dataset,
)
from experiments.increment_27.structural_imports.mechanics import _digest

ROOT = Path("experiments/increment_27")


def _saved(name: str) -> dict[str, Any]:
    path = ROOT / name
    artifact = cast("dict[str, Any]", _read_json(path))
    assert path.read_bytes() == canonical_json_bytes(artifact)
    assert artifact["content_identity"] == _digest(artifact["payload"])
    return artifact


def test_exact_evidence_population_and_three_states_reproduce() -> None:
    artifact = _saved(DATASET_NAME)
    assert artifact == build_dataset(ROOT)
    payload = artifact["payload"]
    assert len(payload["development_case_ids"]) == 24
    assert len(payload["heldout_case_ids_sealed"]) == 14
    assert not set(payload["development_case_ids"]) & set(
        payload["heldout_case_ids_sealed"],
    )
    assert len(payload["suspended_increment_26_case_ids_not_executed"]) == 16
    rows = payload["rows"]
    assert len(rows) == 389
    assert Counter(row["usefulness"] for row in rows) == {
        "USEFUL": 165,
        "NOT_USEFUL": 185,
        "UNJUDGED": 39,
    }
    assert len(payload["excluded_exact_judgments_without_candidate_evidence"]) == 16
    assert len(
        {
            (
                row["information_need"]["purpose"],
                row["information_need"]["lexical_query"],
                row["parent_snapshot_sha"],
                row["address"],
                row["usefulness_semantics"],
            )
            for row in rows
        },
    ) == len(rows)
    assert all(set(row["features"]) == set(FEATURE_CLASSES) for row in rows)
    assert all(row["features"]["resource_lexical_token_length"] is None for row in rows)
    assert payload["confirmation_executed"] is False
    assert payload["new_judgments_created"] is False


def test_diagnostic_preserves_missingness_and_oracle_boundary() -> None:
    artifact = _saved(ANALYSIS_NAME)
    assert artifact == build_analysis(ROOT)
    payload = artifact["payload"]
    assert payload["dataset_sha256"] == sha256_file(ROOT / DATASET_NAME)
    assert payload["population"]["total"] == 389
    assert payload["binary_population"]["total"] == 350
    assert payload["lexical_universe_escapes"]["states"] == {
        "total": 54,
        "USEFUL": 11,
        "NOT_USEFUL": 31,
        "UNJUDGED": 12,
        "judged_total": 42,
        "useful_rate_among_judged": 0.261905,
    }
    assert payload["feature_coverage"]["canonical_rank"]["judged_absent"] == 55
    assert payload["feature_coverage"]["resource_lexical_token_length"][
        "judged_present"
    ] == 0
    assert payload["redundancy"]["canonical_vs_bm25_plus_membership"][
        "jaccard"
    ] == 1.0
    assert payload["predeclared_intersections"]["single_lexical_method"][
        "total"
    ] == 0
    assert payload["oracle_gap"]["candidate_union_count"] == 229
    assert payload["oracle_gap"]["omitted_by_both_useful"]["states"]["total"] == 26
    assert payload["oracle_gap"]["oracle_maximum_useful_at_k5"] == 85
    assert payload["confirmation_executed"] is False
    assert payload["new_judgments_created"] is False
