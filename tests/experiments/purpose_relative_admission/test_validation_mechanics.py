# Copyright (c) 2026
# ruff: noqa: COM812, D103, E501, EM101, FBT001, FBT003, I001, PLC0415, PLR0913, PLR2004, TRY003
"""Synthetic falsification tests for Increment-23 capture and adjudication mechanics."""

from __future__ import annotations

from dataclasses import replace

import pytest

from devtools.context.repository.resource import RepositoryResourceAddress
from experiments.import_relationship_cases import ImportRelationshipDirection
from experiments.purpose_relative_admission.design import PurposeProfile
from experiments.purpose_relative_admission.direct_resolution import DirectResolutionControlResult
from experiments.purpose_relative_admission.reservation import (
    AbstentionReason,
    AdmissionDisposition,
    RelationshipSurface,
    apply_directional_reservation_v1,
)
from experiments.purpose_relative_admission.validation_adjudication import (
    AdjudicationResourceMapping,
    BlindedAdjudicationPackage,
    BlindedResourceEvidence,
    FrozenAdjudication,
    ImmutableAdjudicationRecord,
    build_blinded_adjudication_package,
    freeze_adjudication,
    freeze_adjudication_set,
    unblind_records,
    validate_frozen_adjudication,
    validate_frozen_adjudication_set,
)
from experiments.purpose_relative_admission.validation_capture import (
    CapturedCaseSurface,
    RepositoryCheckpoint,
    captured_direct_resolution_control,
)
from experiments.purpose_relative_admission.validation_design import (
    AdjudicationCompleteness,
    FrozenValidationCase,
    RelationshipControl,
    ValidationRoute,
    increment_23_validation_design_fingerprint,
)
from experiments.purpose_relative_admission.validation_evaluation import (
    EvidenceState,
    ValidationCaseEvaluation,
    annotate_controls_after_unblinding,
    evaluate_frozen_case,
)
from experiments.purpose_relative_import.cases import (
    ResourceJudgment,
    UsefulnessJudgment,
)
from experiments.purpose_relative_import.comparison import RankedLexicalSurface


def _address(value: str) -> RepositoryResourceAddress:
    return RepositoryResourceAddress(value)


def _lexical() -> tuple[RankedLexicalSurface, ...]:
    return tuple(RankedLexicalSurface(_address(f"l{index}.py"), index, float(16 - index)) for index in range(1, 16))


def _surface(
    target: str,
    relation: str,
    ordinal: int,
    *,
    direction: ImportRelationshipDirection = ImportRelationshipDirection.OUTGOING,
    seed_rank: int = 1,
) -> RelationshipSurface:
    return RelationshipSurface(
        _address(target), direction, _address(f"seed{seed_rank}.py"), seed_rank, relation, ordinal
    )


def _capture(
    *,
    profile: PurposeProfile = PurposeProfile.OUTGOING_DEPENDENCY,
    surfaces: tuple[RelationshipSurface, ...] | None = None,
    oracle: tuple[RepositoryResourceAddress, ...] | None = None,
) -> CapturedCaseSurface:
    lexical = _lexical()
    supplied = surfaces or (
        _surface("target.py", "one", 1),
        _surface("target.py", "two", 2, seed_rank=2),
    )
    practical = apply_directional_reservation_v1(
        profile=profile,
        canonical_lexical_top_five=tuple(item.address for item in lexical[:5]),
        surfaces=supplied,
    )
    eligible = () if practical.direction is None else tuple(
        item for item in supplied if item.direction is practical.direction
    )
    return CapturedCaseSurface(
        "synthetic-case",
        "Determine the bounded synthetic behavior.",
        "synthetic query",
        profile,
        ValidationRoute.HETEROGENEOUS_K5,
        increment_23_validation_design_fingerprint(),
        RepositoryCheckpoint("repo", "snapshot", "corpus", 15, (("maximum", 15),)),
        lexical[:5],
        lexical,
        (),
        tuple(item for item in supplied if item.direction is ImportRelationshipDirection.OUTGOING),
        tuple(item for item in supplied if item.direction is ImportRelationshipDirection.INCOMING),
        eligible,
        practical.retained_targets,
        practical,
        supplied,
        tuple(item.address for item in lexical[:5]),
        oracle,
    )


def _frozen(
    capture: CapturedCaseSurface,
    judgments: dict[RepositoryResourceAddress, UsefulnessJudgment],
) -> tuple[
    BlindedAdjudicationPackage,
    tuple[AdjudicationResourceMapping, ...],
    FrozenAdjudication,
]:
    package, mappings = build_blinded_adjudication_package(
        capture=capture,
        purpose_rationale="Synthetic purpose rationale.",
        bounded_evidence_by_address={
            address: BlindedResourceEvidence(
                "structural-outline",
                "python",
                ("Module purpose: bounded source excerpt",),
            )
            for address in capture.material_addresses
        },
        address_visible={},
    )
    records = tuple(
        ImmutableAdjudicationRecord(
            mapping.neutral_id,
            judgments.get(mapping.address, UsefulnessJudgment.UNJUDGED),
            "synthetic judgment",
            mapping.address_visible_to_adjudicator,
            "synthetic-fixture-v1",
        )
        for mapping in mappings
    )
    return package, mappings, freeze_adjudication(package=package, records=records)


def _case(
    capture: CapturedCaseSurface,
    *,
    controls: tuple[RepositoryResourceAddress, ...] = (),
) -> FrozenValidationCase:
    return FrozenValidationCase(
        capture.case_name,
        capture.information_need,
        capture.query_text,
        capture.profile,
        capture.route,
        tuple(
            ResourceJudgment(
                address,
                UsefulnessJudgment.NOT_USEFUL,
                "Synthetic explicit control truth.",
                True,
            )
            for address in controls
        ),
        tuple(
            RelationshipControl(
                address,
                _address("seed1.py"),
                address,
                ImportRelationshipDirection.OUTGOING,
                "Synthetic relation truth.",
                "Synthetic control is not useful.",
            )
            for address in controls
        ),
        "Synthetic fixture provenance.",
        AdjudicationCompleteness.INITIAL_JUDGMENTS_ONLY,
        "Synthetic fixture caveat.",
    )


def _evaluate(
    *,
    capture: CapturedCaseSurface,
    package: BlindedAdjudicationPackage,
    mappings: tuple[AdjudicationResourceMapping, ...],
    frozen: FrozenAdjudication,
    controls: tuple[RepositoryResourceAddress, ...] = (),
    initial_useful: frozenset[RepositoryResourceAddress] = frozenset(),
) -> ValidationCaseEvaluation:
    return evaluate_frozen_case(
        package=package,
        case=_case(capture, controls=controls),
        capture=capture,
        frozen=frozen,
        mappings=mappings,
        initial_useful=initial_useful,
    )


def test_blinded_package_masks_all_mechanism_fields_and_address_by_default() -> None:
    capture = _capture()
    package, mappings, _frozen_value = _frozen(capture, {})

    assert all(item.visible_address is None for item in package.items)
    assert all(item.neutral_id.startswith("resource-") for item in package.items)
    payload = repr(package)
    for prohibited in ("rank", "score", "outgoing", "incoming", "support", "admitted", "oracle", "l1.py"):
        assert prohibited not in payload
    assert {mapping.address for mapping in mappings} == set(capture.material_addresses)


def test_duplicate_encounters_deduplicate_adjudication_but_retain_relation_evidence() -> None:
    surfaces = (
        _surface("target.py", "one", 1),
        _surface("target.py", "one", 2, seed_rank=2),
        _surface("target.py", "two", 3, seed_rank=3),
    )
    capture = _capture(surfaces=surfaces)
    package, mappings, _frozen_value = _frozen(capture, {})

    assert len([mapping for mapping in mappings if mapping.address == _address("target.py")]) == 1
    assert len(package.items) == len(mappings)
    assert len(capture.retained_targets[0].encounters) == 3
    assert capture.retained_targets[0].support_count == 2


def test_useful_admission_and_not_useful_control_are_distinguished() -> None:
    capture = _capture()
    admitted = capture.practical.admitted_target
    assert admitted is not None
    package, mappings, frozen = _frozen(capture, {admitted.address: UsefulnessJudgment.USEFUL})
    useful = _evaluate(capture=capture, package=package, mappings=mappings, frozen=frozen)
    assert useful.useful_admissions == (admitted.address,)

    package, mappings, frozen = _frozen(capture, {admitted.address: UsefulnessJudgment.NOT_USEFUL})
    control = _evaluate(capture=capture, package=package, mappings=mappings, frozen=frozen, controls=(admitted.address,))
    assert control.admitted_not_useful_controls == (admitted.address,)
    assert any(item.category == "rejection" and item.state is EvidenceState.NOT_OBSERVED for item in control.failures)


def test_control_nonexposure_and_rejection_are_not_conflated() -> None:
    capture = _capture(surfaces=(_surface("target.py", "one", 1),))
    control = _address("l1.py")
    package, mappings, frozen = _frozen(capture, {control: UsefulnessJudgment.NOT_USEFUL})
    evaluation = _evaluate(capture=capture, package=package, mappings=mappings, frozen=frozen, controls=(control,))
    assert not any(item.category == "rejection" and item.state is EvidenceState.OBSERVED for item in evaluation.failures)
    assert dict(evaluation.metrics)["eligible_control_exposure"].value == 0.0

    target = _address("target.py")
    package, mappings, frozen = _frozen(capture, {target: UsefulnessJudgment.NOT_USEFUL})
    evaluation = _evaluate(capture=capture, package=package, mappings=mappings, frozen=frozen, controls=(target,))
    assert dict(evaluation.metrics)["eligible_control_exposure"].value == 1.0
    assert dict(evaluation.metrics)["eligible_control_qualification"].value == 0.0

    qualifying_capture = _capture()
    rejected_practical = replace(
        qualifying_capture.practical,
        disposition=AdmissionDisposition.ABSTAINED,
        addresses=tuple(item.address for item in qualifying_capture.lexical_top_five),
        admitted_target=None,
        abstention_reason=AbstentionReason.NO_QUALIFYING_TARGET,
    )
    qualified_control = replace(qualifying_capture, practical=rejected_practical)
    package, mappings, frozen = _frozen(qualified_control, {target: UsefulnessJudgment.NOT_USEFUL})
    evaluation = _evaluate(capture=qualified_control, package=package, mappings=mappings, frozen=frozen, controls=(target,))
    assert any(item.category == "rejection" and item.state is EvidenceState.OBSERVED for item in evaluation.failures)


def test_rank_five_displacement_and_unjudged_admission_have_correct_states() -> None:
    capture = _capture()
    rank_five = capture.rank_five_address
    package, mappings, frozen = _frozen(capture, {rank_five: UsefulnessJudgment.USEFUL})
    evaluation = _evaluate(capture=capture, package=package, mappings=mappings, frozen=frozen)
    assert evaluation.useful_rank_five_displacement is True
    assert evaluation.useful_losses == (rank_five,)

    package, mappings, frozen = _frozen(capture, {rank_five: UsefulnessJudgment.NOT_USEFUL})
    evaluation = _evaluate(capture=capture, package=package, mappings=mappings, frozen=frozen)
    assert evaluation.useful_rank_five_displacement is False
    assert not evaluation.useful_losses
    assert dict(evaluation.metrics)["useful_admission_precision"].state is EvidenceState.INSUFFICIENT_JUDGMENT


def test_initial_useful_resources_are_evaluation_only_and_can_be_absent_from_surface() -> None:
    capture = _capture()
    package, mappings, frozen = _frozen(capture, {})
    evaluation = _evaluate(
        capture=capture,
        package=package,
        frozen=frozen,
        mappings=mappings,
        initial_useful=frozenset({_address("absent.py")}),
    )
    metric = dict(evaluation.metrics)["surface_recall"]
    assert metric.state is EvidenceState.OBSERVED
    assert metric.value == 0.0


def test_local_and_no_qualifier_abstentions_and_inappropriate_abstention() -> None:
    local = _capture(profile=PurposeProfile.LOCAL_DEFINITION_OR_GOVERNANCE)
    package, mappings, frozen = _frozen(local, {})
    evaluation = _evaluate(capture=local, package=package, frozen=frozen, mappings=mappings)
    assert local.practical.abstention_reason is AbstentionReason.LOCAL_PROFILE
    assert evaluation.abstention_appropriate is True

    no_qualifier = _capture(surfaces=(_surface("one.py", "one", 1),))
    package, mappings, frozen = _frozen(no_qualifier, {})
    evaluation = _evaluate(capture=no_qualifier, package=package, frozen=frozen, mappings=mappings)
    assert no_qualifier.practical.abstention_reason is AbstentionReason.NO_QUALIFYING_TARGET
    assert evaluation.abstention_appropriate is True

    target = _address("target.py")
    qualifying_capture = _capture()
    incorrect_practical = replace(
        qualifying_capture.practical,
        disposition=AdmissionDisposition.ABSTAINED,
        addresses=tuple(item.address for item in qualifying_capture.lexical_top_five),
        admitted_target=None,
        abstention_reason=AbstentionReason.NO_QUALIFYING_TARGET,
    )
    incorrect = replace(qualifying_capture, practical=incorrect_practical)
    package, mappings, frozen = _frozen(incorrect, {target: UsefulnessJudgment.USEFUL})
    evaluation = _evaluate(capture=incorrect, package=package, frozen=frozen, mappings=mappings)
    assert evaluation.abstention_appropriate is False


def test_freeze_rejects_incompatible_or_mutated_judgments() -> None:
    capture = _capture()
    package, mappings, frozen = _frozen(capture, {})
    assert not hasattr(frozen.records[0], "is_control")
    validate_frozen_adjudication(package=package, frozen=frozen)
    with pytest.raises(ValueError, match="capture identity"):
        validate_frozen_adjudication(
            package=replace(package, capture_identity="different"),
            frozen=frozen,
        )
    with pytest.raises(ValueError, match="design fingerprint"):
        validate_frozen_adjudication(
            package=replace(package, design_fingerprint="different"),
            frozen=frozen,
        )
    changed_item = replace(
        package.items[0],
        bounded_evidence=BlindedResourceEvidence(
            "structural-outline",
            "python",
            ("Module purpose: different evidence",),
        ),
    )
    with pytest.raises(ValueError, match="package identity"):
        validate_frozen_adjudication(
            package=replace(package, items=(changed_item, *package.items[1:])),
            frozen=frozen,
        )
    mutated = replace(frozen, records=tuple(reversed(frozen.records)))
    with pytest.raises(ValueError, match="fingerprint"):
        validate_frozen_adjudication(package=package, frozen=mutated)
    with pytest.raises(ValueError, match="exactly one record"):
        freeze_adjudication(package=package, records=frozen.records[:-1])
    with pytest.raises(ValueError, match="exactly one record"):
        freeze_adjudication(
            package=package,
            records=(*frozen.records[:-1], frozen.records[0]),
        )
    with pytest.raises(ValueError, match="one-to-one"):
        unblind_records(
            package=package,
            capture=capture,
            frozen=frozen,
            mappings=(*mappings[:-1], mappings[0]),
        )
    with pytest.raises(ValueError, match="does not match"):
        unblind_records(
            package=package,
            capture=capture,
            frozen=frozen,
            mappings=mappings[:-1],
        )
    with pytest.raises(ValueError, match="retained capture"):
        unblind_records(
            package=package,
            capture=replace(capture, case_name="different"),
            frozen=frozen,
            mappings=mappings,
        )
    assert package.capture_identity == capture.identity()


def test_complete_adjudication_set_freezes_exact_blinded_case_order() -> None:
    first_capture = _capture()
    second_capture = replace(_capture(), case_name="second")
    first_package, _first_mappings, first_frozen = _frozen(first_capture, {})
    second_package, _second_mappings, second_frozen = _frozen(second_capture, {})
    records_by_case = {
        first_package.case_name: first_frozen.records,
        second_package.case_name: second_frozen.records,
    }
    frozen_set = freeze_adjudication_set(
        packages=(first_package, second_package),
        records_by_case=records_by_case,
        package_set_identity="package-set",
    )

    validate_frozen_adjudication_set(
        packages=(first_package, second_package),
        frozen=frozen_set,
        package_set_identity="package-set",
    )
    assert tuple(name for name, _case in frozen_set.cases) == (
        first_package.case_name,
        "second",
    )
    with pytest.raises(ValueError, match="package-set identity"):
        validate_frozen_adjudication_set(
            packages=(first_package, second_package),
            frozen=frozen_set,
            package_set_identity="different",
        )
    with pytest.raises(ValueError, match="exactly one record collection"):
        freeze_adjudication_set(
            packages=(first_package, second_package),
            records_by_case={first_package.case_name: first_frozen.records},
            package_set_identity="package-set",
        )


@pytest.mark.parametrize(
    ("judgment", "is_control", "expected_failure"),
    [
        (UsefulnessJudgment.USEFUL, False, None),
        (UsefulnessJudgment.NOT_USEFUL, False, None),
        (UsefulnessJudgment.UNJUDGED, False, "judgment-coverage"),
        (UsefulnessJudgment.NOT_USEFUL, True, None),
        (UsefulnessJudgment.UNJUDGED, True, "judgment-coverage"),
        (UsefulnessJudgment.USEFUL, True, "adjudication"),
    ],
)
def test_complete_blinded_freeze_unblind_control_annotation_and_evaluation_transition(
    judgment: UsefulnessJudgment,
    is_control: bool,
    expected_failure: str | None,
) -> None:
    capture = _capture()
    target = _address("target.py")
    package, mappings, frozen = _frozen(capture, {target: judgment})
    frozen_records_before_unblinding = frozen.records
    frozen_fingerprint_before_unblinding = frozen.fingerprint

    assert all(not hasattr(record, "is_control") for record in frozen.records)
    validate_frozen_adjudication(package=package, frozen=frozen)
    unblinded = unblind_records(
        package=package,
        capture=capture,
        frozen=frozen,
        mappings=mappings,
    )
    records = unblinded.by_address()
    case = _case(capture, controls=(target,) if is_control else ())
    annotations = annotate_controls_after_unblinding(
        case=case,
        unblinded=unblinded,
    )
    evaluation = evaluate_frozen_case(
        package=package,
        case=case,
        capture=capture,
        frozen=frozen,
        mappings=mappings,
    )

    assert frozen.records == frozen_records_before_unblinding
    assert frozen.fingerprint == frozen_fingerprint_before_unblinding
    assert bool(annotations) is is_control
    assert records[target].judgment is judgment
    if is_control:
        assert annotations[0].neutral_id == records[target].neutral_id
        assert dict(evaluation.metrics)["eligible_control_exposure"].value == 1.0
    if judgment is UsefulnessJudgment.UNJUDGED:
        assert records[target].judgment is UsefulnessJudgment.UNJUDGED
    if expected_failure is not None:
        assert any(item.category == expected_failure for item in evaluation.failures)
    if is_control and judgment is UsefulnessJudgment.NOT_USEFUL:
        assert evaluation.admitted_not_useful_controls == (target,)
    if is_control and judgment is UsefulnessJudgment.USEFUL:
        assert evaluation.admitted_not_useful_controls == ()


def test_same_query_different_purpose_and_oracle_stay_outside_practical_rule() -> None:
    outgoing = _capture(profile=PurposeProfile.OUTGOING_DEPENDENCY, oracle=(_address("oracle.py"),))
    local = _capture(profile=PurposeProfile.LOCAL_DEFINITION_OR_GOVERNANCE, oracle=(_address("different.py"),))
    assert outgoing.query_text == local.query_text
    assert outgoing.profile is not local.profile
    assert outgoing.practical.addresses[-1] == _address("target.py")
    assert local.practical.addresses == tuple(item.address for item in local.lexical_top_five)
    assert outgoing.oracle_top_five != local.oracle_top_five
    _package, mappings, frozen = _frozen(outgoing, {_address("target.py"): UsefulnessJudgment.USEFUL})
    _package, local_mappings, local_frozen = _frozen(local, {_address("target.py"): UsefulnessJudgment.NOT_USEFUL})
    assert frozen.fingerprint != local_frozen.fingerprint
    assert mappings != local_mappings


def test_direct_resolution_is_excluded_and_design_loading_uses_no_real_mechanics(monkeypatch: pytest.MonkeyPatch) -> None:
    from devtools.context.python.imports import relations
    from devtools.context.retrieval.lexical import bm25
    from experiments.purpose_relative_admission import direct_resolution, reservation

    def prohibited(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("Synthetic capture must not execute real repository mechanics.")

    monkeypatch.setattr(bm25, "retrieve_repository_text_documents_by_bm25", prohibited)
    monkeypatch.setattr(relations, "derive_python_resolved_module_import_relations", prohibited)
    monkeypatch.setattr(reservation, "apply_directional_reservation_v1", prohibited)
    monkeypatch.setattr(direct_resolution, "run_exact_name_direct_resolution_control", prohibited)
    control = captured_direct_resolution_control(
        name="synthetic-direct",
        result=DirectResolutionControlResult("named", ("resource.py",)),
    )
    assert control.result.applicable_to_heterogeneous_k5_metrics is False
