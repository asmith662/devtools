# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Fixed-budget fusion freeze, candidate, and joined-result invariants."""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from experiments.increment_27.depth_diagnostic import (
    _read_json,
    canonical_json_bytes,
    sha256_file,
)
from experiments.increment_27.fusion import (
    CANDIDATES_NAME,
    FREEZE_NAME,
    build_candidates,
    build_freeze,
)
from experiments.increment_27.fusion_results import RESULT_NAME, build_results
from experiments.increment_27.structural_imports.mechanics import _digest

ROOT = Path("experiments/increment_27")


def _saved(name: str) -> dict[str, Any]:
    path = ROOT / name
    artifact = cast("dict[str, Any]", _read_json(path))
    assert path.read_bytes() == canonical_json_bytes(artifact)
    assert artifact["content_identity"] == _digest(artifact["payload"])
    return artifact


def test_outcome_independent_freeze_and_candidate_surfaces_rebuild() -> None:
    freeze = _saved(FREEZE_NAME)
    candidates = _saved(CANDIDATES_NAME)
    assert freeze == build_freeze(ROOT)
    assert candidates == build_candidates(ROOT)
    assert candidates["payload"]["freeze_identity"] == freeze["content_identity"]
    cases = candidates["payload"]["cases"]
    assert len(cases) == 24
    assert not {case["case_id"] for case in cases} & set(
        freeze["payload"]["heldout_case_ids_sealed"],
    )
    assert [
        sum(len(case["surfaces"][name]) for case in cases)
        for name in (
            "canonical_top5",
            "lexical4_import1",
            "structural_top5_diagnostic",
        )
    ] == [120, 120, 92]
    for case in cases:
        baseline = case["surfaces"]["canonical_top5"]
        fusion = case["surfaces"]["lexical4_import1"]
        assert fusion[:4] == baseline[:4]
        assert fusion[4] == (
            case["ranked_structural_evidence"][0]["address"]
            if case["ranked_structural_evidence"]
            else baseline[4]
        )
        assert len(set(fusion)) == 5
        assert len(case["surfaces"]["structural_top5_diagnostic"]) <= 5


def test_result_reuses_exact_judgments_and_accounts_for_substitutions() -> None:
    result = _saved(RESULT_NAME)
    assert result == build_results(ROOT)
    payload = result["payload"]
    assert payload["new_judgments_required"] == 0
    assert payload["judgments_changed"] is False
    assert payload["confirmation_executed"] is False
    assert payload["freeze_sha256"] == sha256_file(ROOT / FREEZE_NAME)
    assert payload["candidate_sha256"] == sha256_file(ROOT / CANDIDATES_NAME)
    strategy = payload["strategy_results"]
    assert strategy["canonical_top5"]["USEFUL"] == 63
    assert strategy["lexical4_import1"]["USEFUL"] == 63
    assert strategy["lexical4_import1"]["cases_with_at_least_one_useful"] == 20
    assert strategy["lexical4_import1"]["useful_all_lexical_escape"] == 2
    assert strategy["structural_top5_diagnostic"]["candidate_occurrences"] == 92
    for name, counts in strategy.items():
        rows = payload["joined_surfaces"][name]
        assert counts["candidate_occurrences"] == len(rows)
        assert counts["distinct_pairs"] == len(
            {(row["case_id"], row["address"]) for row in rows},
        )
        assert counts["judged_total"] == counts["USEFUL"] + counts["NOT_USEFUL"]
        assert counts["candidate_occurrences"] == (
            counts["judged_total"] + counts["UNJUDGED"]
        )
    comparison = payload["fusion_vs_canonical"]
    assert (comparison["cases_gaining_useful"], comparison["cases_losing_useful"]) == (
        5,
        5,
    )
    assert comparison["substitution_counts"] == {
        "beneficial": 5,
        "harmful": 5,
        "useful_for_useful": 7,
        "unresolved": 2,
        "not_useful_for_not_useful": 4,
    }
    assert sum(comparison["substitution_counts"].values()) == len(
        comparison["substitutions"],
    )
    oracle = payload["oracle_upper_bound"]
    assert oracle["maximum_useful_at_k5"] == 85
    assert oracle["cases_coverable_at_least_one"] == 21
    assert strategy["lexical4_import1"]["gap_to_oracle_useful_at_k5"] == 22
