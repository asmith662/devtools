# Copyright (c) 2026
# ruff: noqa: D103, E501, EM101, PLC0415, PLR2004, TC002, TRY003
"""Integrity tests for frozen Increment-23 configuration, not mechanics."""

from __future__ import annotations

from pathlib import Path

import pytest

from experiments.purpose_relative_admission.design import PurposeProfile
from experiments.purpose_relative_admission.validation_design import (
    INCREMENT_22_RULE_FINGERPRINT,
    AdjudicationCompleteness,
    ValidationRoute,
    abandonment_criteria,
    blinded_adjudication_protocol,
    comparison_arms,
    direct_resolution_validation_controls,
    failure_taxonomy,
    frozen_validation_cases,
    increment_23_validation_design_fingerprint,
    shadow_readiness_criteria,
)
from experiments.purpose_relative_import.cases import UsefulnessJudgment


def test_frozen_cases_are_complete_case_disjoint_and_repository_grounded() -> None:
    cases = frozen_validation_cases()
    names = {case.name for case in cases}
    increment_22_held_out = {
        "observation-resource-snapshot-flow",
        "public-relation-tests",
        "relation-source-availability",
        "observation-safe-change",
        "import-resolution-safe-change",
        "filesystem-translation-safe-change",
        "context-disclosure-architecture",
        "context-disclosure-implementation",
    }

    assert len(cases) == 6
    assert len(names) == len(cases)
    assert names.isdisjoint(increment_22_held_out)
    assert all(case.information_need and case.query_text for case in cases)
    assert all(case.route is ValidationRoute.HETEROGENEOUS_K5 for case in cases)
    assert all(
        case.adjudication_completeness is AdjudicationCompleteness.INITIAL_JUDGMENTS_ONLY
        for case in cases
    )
    for case in cases:
        addresses = [judgment.address for judgment in case.judgments]
        assert len(addresses) == len(set(addresses))
        assert any(item.judgment is UsefulnessJudgment.USEFUL for item in case.judgments)
        assert all((Path(item.address.value)).is_file() for item in case.judgments)


def test_frozen_cases_cover_profiles_controls_pair_and_test_semantics() -> None:
    cases = {case.name: case for case in frozen_validation_cases()}
    formula = cases["content-bm25-term-formula"]
    analysis = cases["baseline-lexical-analysis-definition"]
    consumer = cases["content-bm25-analysis-consumer"]

    assert {case.profile for case in cases.values()} == set(PurposeProfile)
    assert formula.profile is PurposeProfile.OUTGOING_DEPENDENCY
    assert consumer.profile is PurposeProfile.INCOMING_CONSUMER_OR_TEST
    assert analysis.profile is PurposeProfile.LOCAL_DEFINITION_OR_GOVERNANCE
    assert analysis.query_text == consumer.query_text
    assert analysis.information_need != consumer.information_need
    assert analysis.judgments != consumer.judgments
    assert {control.direction.value for case in cases.values() for control in case.relationship_controls} == {"outgoing", "incoming"}
    assert any(item.address.value.endswith("test_bm25.py") and item.judgment is UsefulnessJudgment.USEFUL for item in formula.judgments)
    assert any(item.address.value.endswith("test_filename.py") and item.judgment is UsefulnessJudgment.NOT_USEFUL and item.is_control for item in consumer.judgments)
    assert any("no-qualifier abstention opportunity" in case.caveat for case in cases.values())
    assert any(
        item.address.value == "docs/architecture/taxonomy.md"
        for item in cases["repository-context-taxonomy-boundary"].judgments
    )


def test_relationship_controls_are_explicit_true_directional_not_useful_judgments() -> None:
    cases = frozen_validation_cases()

    controls = [control for case in cases for control in case.relationship_controls]
    assert len(controls) == 3
    for control in controls:
        assert control.address in {control.relation_source, control.relation_target}
        assert control.relation_truth_rationale
        assert control.not_useful_rationale
    for case in cases:
        judgment_by_address = {item.address: item for item in case.judgments}
        for control in case.relationship_controls:
            judgment = judgment_by_address[control.address]
            assert judgment.judgment is UsefulnessJudgment.NOT_USEFUL
            assert judgment.is_control


def test_direct_resolution_controls_remain_outside_heterogeneous_metrics() -> None:
    controls = direct_resolution_validation_controls()

    assert len(controls) == 2
    assert {control.declared_name for control in controls} == {
        "retrieve_python_functions_by_exact_name",
        "materialize_python_function_disclosure_source",
    }
    assert all(Path(control.useful_address.value).is_file() for control in controls)


def test_design_loading_cannot_execute_prospective_mechanics(monkeypatch: pytest.MonkeyPatch) -> None:
    from devtools.context.python.imports import relations
    from devtools.context.retrieval.lexical import bm25
    from experiments.purpose_relative_admission import direct_resolution, reservation

    def prohibited(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("Pass-2 design loading must not execute prospective mechanics.")

    monkeypatch.setattr(bm25, "retrieve_repository_text_documents_by_bm25", prohibited)
    monkeypatch.setattr(relations, "derive_python_resolved_module_import_relations", prohibited)
    monkeypatch.setattr(reservation, "apply_directional_reservation_v1", prohibited)
    monkeypatch.setattr(
        direct_resolution, "run_exact_name_direct_resolution_control", prohibited,
    )

    assert frozen_validation_cases()
    assert direct_resolution_validation_controls()
    assert blinded_adjudication_protocol().hidden_fields
    assert failure_taxonomy()
    assert comparison_arms()
    assert shadow_readiness_criteria()
    assert abandonment_criteria()


def test_fingerprint_is_stable_and_captures_the_unchanged_rule_reference() -> None:
    assert INCREMENT_22_RULE_FINGERPRINT == "7e215ac2961a4329074e9a25d35d3decc554f394435aa0b73cb2251254160345"
    assert increment_23_validation_design_fingerprint() == "c36d39f18258e918f8a1023a22d821619fc08cb8840d4ed80aae31832feabef7"
