# Copyright (c) 2026
# ruff: noqa: ANN001, D103, E501, I001, PLR0913, PLR2004
# mypy: disable-error-code="arg-type,index,no-untyped-def"
"""Focused tests for judgment-isolated Pass 4 execution and accounting."""

from __future__ import annotations

import inspect
import json
from types import SimpleNamespace
from typing import TYPE_CHECKING, cast

from devtools.context.repository.resource import RepositoryResourceAddress
from experiments.purpose_relative_admission.design import ExperimentPartition, frozen_admission_cases
from experiments.purpose_relative_admission.direct_resolution import DirectResolutionControlResult
from experiments.purpose_relative_admission.evaluation import (
    FrozenCaseRanking,
    FrozenRankingRun,
    _same_query_pair,
    aggregate_evaluated_cases,
    construct_frozen_rankings,
    evaluate_rankings,
    ranking_metrics,
    write_report,
)

if TYPE_CHECKING:
    import pytest


def _case(
    *,
    name: str,
    final: tuple[str, ...] = ("l1.py", "l2.py", "l3.py", "l4.py", "l5.py"),
    disposition: str = "abstained",
    abstention: str | None = "no-qualifying-target",
    admitted_judgment: str | None = None,
    displaced: str | None = None,
    loss: tuple[str, ...] = (),
    recovered: tuple[str, ...] = (),
    exposed: tuple[str, ...] = (),
    admitted_controls: tuple[str, ...] = (),
    direction: str | None = "incoming",
    targets: tuple[dict[str, object], ...] = (),
    encounters: int = 0,
) -> dict[str, object]:
    return {
        "name": name,
        "canonical_lexical_top_5": [
            {"rank": rank, "address": f"l{rank}.py", "native_score": 6 - rank}
            for rank in range(1, 6)
        ],
        "judgments": [
            {"address": "l1.py", "judgment": "useful", "rationale": "fixture", "is_control": False},
            {"address": "control.py", "judgment": "not-useful", "rationale": "fixture", "is_control": True},
        ],
        "practical": {
            "final_top_5": list(final),
            "disposition": disposition,
            "abstention_reason": abstention,
            "admitted_judgment": admitted_judgment,
            "admitted_unique_support_count": 2 if disposition == "admitted" else None,
            "displaced_lexical_rank_5": displaced,
        },
        "comparison_to_canonical": {
            "newly_recovered_relevant": list(recovered),
            "relevant_losses": list(loss),
        },
        "control_evidence": {
            "exposed_or_considered": list(exposed),
            "admitted": list(admitted_controls),
        },
        "relationship_evidence": {
            "eligible_direction": direction,
            "deduplicated_candidate_count": len(targets),
            "encounter_count": encounters,
            "deduplicated_targets": list(targets),
        },
    }


def test_ranking_construction_api_cannot_accept_judgments_or_expected_outcomes() -> None:
    parameters = inspect.signature(construct_frozen_rankings).parameters

    assert "judgments" not in parameters
    assert "controls" not in parameters
    assert "expected_outcomes" not in parameters
    assert set(parameters) == {"cases", "index", "relations", "interpretations_by_address"}


def test_evaluation_keeps_calibration_out_of_held_out_aggregate(monkeypatch: pytest.MonkeyPatch) -> None:
    cases = frozen_admission_cases()
    rankings = FrozenRankingRun(
        tuple(cast("FrozenCaseRanking", SimpleNamespace(name=case.need.name)) for case in cases),
    )

    monkeypatch.setattr(
        "experiments.purpose_relative_admission.evaluation._evaluate_case",
        lambda *, case, **_kwargs: {"name": case.need.name, "partition": case.partition.value},
    )
    monkeypatch.setattr(
        "experiments.purpose_relative_admission.evaluation.aggregate_evaluated_cases",
        lambda values: {"names": [value["name"] for value in values]},
    )
    monkeypatch.setattr(
        "experiments.purpose_relative_admission.evaluation._same_query_pair",
        lambda values: {"count": len(values)},
    )

    result = evaluate_rankings(rankings=rankings, cases=cases)

    assert len(result["calibration"]) == 4
    assert len(result["held_out"]) == 8
    assert result["held_out_aggregate"]["names"] == [
        case.need.name for case in cases if case.partition is ExperimentPartition.HELD_OUT
    ]


def test_metric_aggregation_preserves_hit_recall_and_mrr() -> None:
    rankings = (
        tuple(RepositoryResourceAddress(value) for value in ("a.py", "x.py")),
        tuple(RepositoryResourceAddress(value) for value in ("x.py", "b.py")),
    )
    relevant = ({RepositoryResourceAddress("a.py")}, {RepositoryResourceAddress("b.py"), RepositoryResourceAddress("c.py")})

    assert ranking_metrics(rankings=rankings, relevant=relevant) == {
        "hit_at_5": 1.0,
        "mean_recall_at_5": 0.75,
        "mrr": 0.75,
    }


def test_aggregate_accounts_for_admission_abstention_displacement_loss_and_controls() -> None:
    qualifier = {"unique_support_count": 2, "qualification_reason": "qualified"}
    cases = (
        _case(
            name="admit",
            final=("l1.py", "l2.py", "l3.py", "l4.py", "control.py"),
            disposition="admitted",
            abstention=None,
            admitted_judgment="not-useful",
            displaced="l5.py",
            loss=("l5.py",),
            exposed=("control.py",),
            admitted_controls=("control.py",),
            targets=(qualifier,),
            encounters=3,
        ),
        _case(name="local", abstention="local-profile", direction=None),
    )

    aggregate = aggregate_evaluated_cases(cases)

    assert aggregate["admitted_case_count"] == 1
    assert aggregate["local_profile_abstention_count"] == 1
    assert aggregate["no_qualifying_target_abstention_count"] == 0
    assert aggregate["rank_5_displacement_count"] == 1
    assert aggregate["previously_retrieved_relevant_resource_lost_count"] == 1
    assert aggregate["explicit_controls_exposed_count"] == 1
    assert aggregate["explicit_controls_admitted_count"] == 1
    assert aggregate["admissions_irrelevant_or_unjudged_count"] == 1
    assert aggregate["unique_support_count_distribution"] == {"qualifying": {2: 1}, "admitted": {2: 1}}


def test_same_query_pair_reports_profiles_and_independent_metrics() -> None:
    architecture = {
        "name": "context-disclosure-architecture",
        "query": "Context disclosure",
        "purpose_profile": "local-definition-or-governance",
        "practical": {"abstention_reason": "local-profile", "final_top_5": ["architecture.md"]},
        "relationship_evidence": {"eligible_direction": None},
        "comparison_to_canonical": {"practical_metrics": {"recall_at_5": 1.0}},
    }
    implementation = {
        "name": "context-disclosure-implementation",
        "query": "Context disclosure",
        "purpose_profile": "incoming-consumer-or-test",
        "practical": {"abstention_reason": None, "final_top_5": ["disclosure.py"]},
        "relationship_evidence": {"eligible_direction": "incoming"},
        "comparison_to_canonical": {"practical_metrics": {"recall_at_5": 0.5}},
    }

    result = _same_query_pair((architecture, implementation))

    assert result["query_text_identical"]
    assert result["architecture_local_profile_abstained"]
    assert result["implementation_eligible_direction"] == "incoming"
    assert result["practical_outcomes_differ"]
    assert result["architecture_metrics"] != result["implementation_metrics"]


def test_direct_controls_are_excluded_from_heterogeneous_metrics() -> None:
    result = DirectResolutionControlResult("target", ("target.py",))

    assert not result.applicable_to_heterogeneous_k5_metrics


def test_report_serialization_is_deterministic(tmp_path) -> None:
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    payload = {"schema": "fixture-v1", "nested": {"z": 2, "a": 1}}

    write_report(path=first, payload=payload)
    write_report(path=second, payload=payload)

    assert first.read_bytes() == second.read_bytes()
    assert json.loads(first.read_text(encoding="utf-8")) == payload
