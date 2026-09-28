# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004
"""Blinded sampled judgment freeze and mechanical Graph-2 result tests."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Any

import pytest

from experiments.increment_27.depth_diagnostic import sha256_file
from experiments.increment_30.mechanics import _verified_json
from experiments.increment_33 import analysis
from experiments.increment_33.judgments import (
    FROZEN_NAME,
    build_judgments,
    sampled_targets,
)
from experiments.increment_33.mechanics import CANDIDATES_NAME, GRAPH_ONE_SHA256, ROOT
from experiments.increment_33.population import JUDGMENT_FREEZE_NAME, STATES
from experiments.retrieval_judgment_coverage import (
    judgment_identity,
    validate_frozen_judgment_coverage,
)

if TYPE_CHECKING:
    from pathlib import Path


def decisions() -> list[dict[str, Any]]:
    return deepcopy(_verified_json(ROOT / FROZEN_NAME)["payload"]["decisions"])


def test_frozen_sample_has_exact_128_identity_coverage_and_no_prior_overlap() -> None:
    artifact = _verified_json(ROOT / FROZEN_NAME)
    assert artifact == build_judgments(decisions())
    targets = sampled_targets()
    assert len(targets) == len(artifact["payload"]["decisions"]) == 128
    indexed = validate_frozen_judgment_coverage(targets, decisions(), STATES)
    prior = _verified_json(ROOT / JUDGMENT_FREEZE_NAME)["payload"]["reused_judgments"]
    assert len(indexed) == 128
    assert {judgment_identity(row) for row in prior}.isdisjoint(set(indexed))
    assert all(row["rationale"].strip() for row in decisions())


@pytest.mark.parametrize(
    "fault", ["missing", "extra", "duplicate", "blank_rationale", "invalid_state"]
)
def test_bad_blinded_decision_sets_are_rejected(fault: str) -> None:
    rows = decisions()
    if fault == "missing":
        rows.pop()
    elif fault == "extra":
        rows.append({**rows[0], "neutral_resource_id": "extra", "address": "extra.py"})
    elif fault == "duplicate":
        rows.append(deepcopy(rows[0]))
    elif fault == "blank_rationale":
        rows[0]["rationale"] = " "
    else:
        rows[0]["judgment"] = "UNKNOWN"
    with pytest.raises(ValueError, match="Frozen judgment"):
        build_judgments(rows)


def test_join_requires_frozen_decisions_before_candidate_read(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    read_paths: list[Path] = []
    original = _verified_json

    def spy(path: Path) -> dict[str, Any]:
        read_paths.append(path)
        return original(path)

    def reject(*_args: object, **_kwargs: object) -> None:
        msg = "unfrozen decisions"
        raise ValueError(msg)

    monkeypatch.setattr(analysis, "_verified_json", spy)
    monkeypatch.setattr(analysis, "build_judgments", reject)
    with pytest.raises(ValueError, match="unfrozen decisions"):
        analysis.build_result()
    assert ROOT / CANDIDATES_NAME not in read_paths


def test_result_is_deterministic_complete_and_keeps_unsampled_unjudged() -> None:
    result = _verified_json(ROOT / analysis.RESULT_NAME)
    assert result == analysis.build_result()
    payload = result["payload"]
    summary = payload["complete_candidate_summary"]
    assert len(payload["joined_pairs"]) == summary["candidate_count"] == 987
    assert payload["population_counts"] == {
        "exact_reused_judged": 2,
        "sampled_newly_judged": 128,
        "unsampled_unadjudicated": 857,
    }
    assert (
        sum(
            row["population"] == "unsampled_unadjudicated" and "judgment" not in row
            for row in payload["joined_pairs"]
        )
        == 857
    )
    assert not payload["confirmation_executed"]
    assert payload["candidate_sha256"] == sha256_file(ROOT / CANDIDATES_NAME)
    assert (
        sha256_file(ROOT.parent / "increment_32" / "graph_round_one_candidates.json")
        == GRAPH_ONE_SHA256
    )


def test_wilson_interval_for_zero_observed_useful() -> None:
    interval = analysis.wilson_95(0, 128)
    assert interval["observed_useful_fraction"] == interval["lower"] == 0
    assert interval["upper"] == pytest.approx(0.029136956273508416)
    assert not interval["finite_population_correction_applied"]
    with pytest.raises(ValueError, match="Invalid sampled useful count"):
        analysis.wilson_95(1, 0)
