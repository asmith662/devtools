# Copyright (c) 2026
# ruff: noqa: D103
"""Focused contract tests for the semantic Localization kernel."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.context.localization import (
    ApplicabilityStatus,
    DeferredDiscovery,
    Disposition,
    HandoffReadiness,
    LocalizationAnchor,
    LocalizationAnchorIdentity,
    LocalizationAssessment,
    LocalizationEvidenceReference,
    LocalizationObligation,
    LocalizationObligationIdentity,
    LocalizationReadiness,
    LocalizationTaskIdentity,
    LocalizationTaskInterpretation,
    RequirementStatus,
    SatisfactionCriterion,
    SupportedWitness,
    TaskProvenance,
    TaskTextSpan,
    WitnessSet,
    assess_localization_readiness,
)
from devtools.context.repository.identity import RepositoryId
from devtools.context.repository.snapshot import RepositorySnapshotId

if TYPE_CHECKING:
    from collections.abc import Hashable

_REPOSITORY = RepositoryId.parse("00000000-0000-0000-0000-000000000001")
_SNAPSHOT = RepositorySnapshotId("a" * 64)
_OTHER_SNAPSHOT = RepositorySnapshotId("b" * 64)


def _provenance(value: str = "task-prompt") -> TaskProvenance:
    return TaskProvenance(value, TaskTextSpan(0, 12), "explicit caller interpretation")


def _obligation(
    key: str = "implement",
    *,
    task: LocalizationTaskIdentity | None = None,
    requirement: RequirementStatus = RequirementStatus.MANDATORY,
    condition: str | None = None,
    alternatives: tuple[WitnessSet, ...] | None = None,
) -> LocalizationObligation:
    task_id = task or LocalizationTaskIdentity("task-1")
    return LocalizationObligation(
        identity=LocalizationObligationIdentity(task_id, key),
        predicate=f"locate {key} information",
        anchors=(LocalizationAnchorIdentity(task_id, "Obligation"),),
        provenance=_provenance(f"task:{key}"),
        requirement=requirement,
        satisfaction=SatisfactionCriterion(
            "explicit",
            "all targets in one alternative",
        ),
        witness_alternatives=(alternatives or (WitnessSet(("implementation",)),)),
        applicability_condition=condition,
    )


def _task(
    *obligations: LocalizationObligation,
    identity: LocalizationTaskIdentity | None = None,
) -> LocalizationTaskInterpretation:
    task_id = identity or LocalizationTaskIdentity("task-1")
    anchor = LocalizationAnchorIdentity(task_id, "Obligation")
    return LocalizationTaskInterpretation(
        identity=task_id,
        provenance=_provenance("full-task"),
        anchors=(LocalizationAnchor(anchor, "Obligation", _provenance("anchor")),),
        obligations=obligations,
    )


def _evidence(
    identity: str = "evidence-1",
    *,
    snapshot: RepositorySnapshotId = _SNAPSHOT,
) -> LocalizationEvidenceReference:
    return LocalizationEvidenceReference(identity, _REPOSITORY, snapshot)


def _resolved(
    obligation: LocalizationObligation,
    targets: tuple[Hashable, ...] = ("implementation",),
    *,
    snapshot: RepositorySnapshotId = _SNAPSHOT,
    repository: RepositoryId = _REPOSITORY,
) -> LocalizationAssessment:
    return LocalizationAssessment(
        obligation=obligation.identity,
        repository_id=repository,
        snapshot_id=snapshot,
        disposition=Disposition.RESOLVED,
        applicability=(
            ApplicabilityStatus.APPLIES
            if obligation.applicability_condition is not None
            else ApplicabilityStatus.NOT_REQUIRED
        ),
        applicability_evidence=(
            (_evidence("applies", snapshot=snapshot),)
            if obligation.applicability_condition is not None
            else ()
        ),
        supported_witnesses=tuple(
            SupportedWitness(
                target,
                (_evidence(f"supports:{target}", snapshot=snapshot),),
            )
            for target in targets
        ),
    )


def _assess(
    task: LocalizationTaskInterpretation,
    *assessments: LocalizationAssessment,
    snapshot: RepositorySnapshotId = _SNAPSHOT,
) -> LocalizationReadiness:
    return assess_localization_readiness(
        task=task,
        repository_id=_REPOSITORY,
        snapshot_id=snapshot,
        assessments=assessments,
    )


def test_task_local_anchor_identity_is_deterministic_and_not_repository_identity() -> (
    None
):
    first_task = LocalizationTaskIdentity("task-1")
    repeated_task = LocalizationTaskIdentity("task-1")
    other_task = LocalizationTaskIdentity("task-2")
    first = LocalizationAnchorIdentity(first_task, "obligation")
    repeated = LocalizationAnchorIdentity(repeated_task, "obligation")
    other = LocalizationAnchorIdentity(other_task, "obligation")

    assert first == repeated
    assert first != other
    assert not isinstance(first, str)
    assert LocalizationAnchor(first, "Obligation").provenance is None


def test_task_interpretation_shares_anchor_across_obligations() -> None:
    task_id = LocalizationTaskIdentity("shared-task")
    task = _task(
        _obligation("implement", task=task_id),
        _obligation("export", task=task_id),
        identity=task_id,
    )

    assert task.obligations[0].anchors == task.obligations[1].anchors
    assert len(task.anchors) == 1


def test_task_source_and_optional_anchor_span_preserve_provenance() -> None:
    task = _task(_obligation())

    assert task.provenance.source_identity == "full-task"
    assert task.anchors[0].provenance is not None
    assert task.anchors[0].provenance.span == TaskTextSpan(0, 12)


def test_task_rejects_foreign_and_missing_anchor_references() -> None:
    task_id = LocalizationTaskIdentity("task-1")
    foreign = LocalizationAnchorIdentity(LocalizationTaskIdentity("task-2"), "x")
    with pytest.raises(ValueError, match="same task"):
        replace(_obligation(), anchors=(foreign,))
    orphan = replace(
        _obligation(task=task_id),
        anchors=(LocalizationAnchorIdentity(task_id, "missing"),),
    )
    with pytest.raises(ValueError, match="outside its task"):
        _task(orphan)
    foreign_anchor = LocalizationAnchor(
        foreign,
        "outside",
        _provenance("foreign-anchor"),
    )
    with pytest.raises(ValueError, match="foreign task-local"):
        LocalizationTaskInterpretation(
            task_id,
            _provenance(),
            (foreign_anchor,),
            (),
        )


def test_identity_and_provenance_values_reject_invalid_inputs() -> None:
    with pytest.raises(ValueError, match="task identity"):
        LocalizationTaskIdentity(" ")
    with pytest.raises(ValueError, match="anchor key"):
        LocalizationAnchorIdentity(LocalizationTaskIdentity("t"), " ")
    with pytest.raises(ValueError, match="interval"):
        TaskTextSpan(2, 2)
    with pytest.raises(ValueError, match="hashable"):
        TaskProvenance([], None)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="obligation key"):
        LocalizationObligationIdentity(LocalizationTaskIdentity("t"), " ")
    with pytest.raises(ValueError, match="explanation"):
        TaskProvenance("task", None, " ")


def test_obligation_retains_requirement_condition_criterion_and_anchor() -> None:
    obligation = _obligation(condition="if this package registers plugins")

    assert obligation.requirement is RequirementStatus.MANDATORY
    assert obligation.applicability_condition == "if this package registers plugins"
    assert obligation.provenance.explanation == "explicit caller interpretation"
    assert obligation.satisfaction.name == "explicit"
    assert obligation.anchors[0].value == "Obligation"


def test_helpful_is_not_a_conditional_priority() -> None:
    obligation = _obligation(
        requirement=RequirementStatus.HELPFUL,
        condition="if an overview is requested",
    )

    assert obligation.requirement is RequirementStatus.HELPFUL
    assert obligation.applicability_condition is not None


def test_witness_set_requires_distinct_hashable_targets() -> None:
    assert WitnessSet(("implementation", "registration")).members == (
        "implementation",
        "registration",
    )
    with pytest.raises(ValueError, match="at least one"):
        WitnessSet(())
    with pytest.raises(ValueError, match="repeat"):
        WitnessSet(("x", "x"))
    with pytest.raises(ValueError, match="hashable"):
        WitnessSet(([],))  # type: ignore[arg-type]


def test_task_and_assessment_values_reject_invalid_structure() -> None:
    task_id = LocalizationTaskIdentity("task-1")
    with pytest.raises(ValueError, match="anchor text"):
        LocalizationAnchor(LocalizationAnchorIdentity(task_id, "x"), " ")
    task = _task(_obligation())
    with pytest.raises(ValueError, match="duplicate anchor"):
        replace(task, anchors=task.anchors + task.anchors)
    with pytest.raises(ValueError, match="duplicate obligation"):
        replace(task, obligations=task.obligations + task.obligations)
    foreign = _obligation(task=LocalizationTaskIdentity("other"))
    with pytest.raises(ValueError, match="foreign task-local"):
        replace(task, obligations=(foreign,))

    with pytest.raises(ValueError, match="at least one evidence"):
        SupportedWitness("x", ())
    with pytest.raises(ValueError, match="observation and reason"):
        DeferredDiscovery(" ", "reason")
    with pytest.raises(ValueError, match="observation and reason"):
        DeferredDiscovery("observe", " ")
    with pytest.raises(ValueError, match="hashable"):
        LocalizationEvidenceReference([], _REPOSITORY, _SNAPSHOT)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="hashable"):
        SupportedWitness([], (_evidence(),))  # type: ignore[arg-type]

    obligation = _obligation()
    with pytest.raises(ValueError, match="distinct witness target"):
        replace(
            _resolved(obligation),
            supported_witnesses=(
                SupportedWitness("x", (_evidence("one"),)),
                SupportedWitness("x", (_evidence("two"),)),
            ),
        )
    with pytest.raises(ValueError, match="must not be blank"):
        replace(_resolved(obligation), explanation=" ")
    with pytest.raises(ValueError, match="must name its later observation"):
        replace(_resolved(obligation), disposition=Disposition.DEFERRED_DISCOVERY)
    with pytest.raises(ValueError, match="Only a deferred disposition"):
        replace(
            _resolved(obligation),
            deferred=DeferredDiscovery("observe", "reason"),
        )


def test_obligation_rejects_foreign_duplicate_anchors_and_alternatives() -> None:
    obligation = _obligation(alternatives=(WitnessSet(("x",)), WitnessSet(("y",))))
    with pytest.raises(ValueError, match="repeat an anchor"):
        replace(obligation, anchors=(obligation.anchors[0], obligation.anchors[0]))
    with pytest.raises(ValueError, match="equivalent witness"):
        replace(
            obligation,
            witness_alternatives=(WitnessSet(("x",)), WitnessSet(("x",))),
        )
    with pytest.raises(ValueError, match="condition must not be blank"):
        replace(obligation, applicability_condition=" ")
    with pytest.raises(ValueError, match="predicate must not be blank"):
        replace(obligation, predicate=" ")
    with pytest.raises(ValueError, match="criterion needs"):
        replace(obligation, satisfaction=SatisfactionCriterion(" ", "statement"))


def test_single_witness_resolves_and_reports_alternative_index() -> None:
    obligation = _obligation()
    result = _assess(_task(obligation), _resolved(obligation))

    assert result.readiness is HandoffReadiness.READY
    assert result.is_ready
    assert result.assessed_obligations[0].satisfied_alternative_index == 0
    assert result.resolved_mandatory == (obligation.identity,)


def test_conjunctive_witness_needs_every_member() -> None:
    obligation = _obligation(
        alternatives=(WitnessSet(("implementation", "registration")),),
    )
    task = _task(obligation)

    incomplete = _assess(task, _resolved(obligation, ("implementation",)))
    complete = _assess(task, _resolved(obligation, ("implementation", "registration")))

    assert incomplete.readiness is HandoffReadiness.INVALID_FRAME
    assert incomplete.invalid_assessments == (obligation.identity,)
    assert complete.readiness is HandoffReadiness.READY


def test_any_complete_alternative_satisfies_and_order_is_stable() -> None:
    obligation = _obligation(
        alternatives=(WitnessSet(("api", "facade")), WitnessSet(("package-export",))),
    )
    task = _task(obligation)
    selected = _assess(task, _resolved(obligation, ("package-export",)))
    reversed_alternatives = replace(
        obligation,
        witness_alternatives=tuple(reversed(obligation.witness_alternatives)),
    )
    reversed_result = _assess(
        _task(reversed_alternatives),
        _resolved(reversed_alternatives, ("package-export",)),
    )

    assert selected.readiness is HandoffReadiness.READY
    assert selected.assessed_obligations[0].satisfied_alternative_index == 1
    assert reversed_result.assessed_obligations[0].satisfied_alternative_index == 0


def test_witness_targets_preserve_native_hashable_identity_types() -> None:
    obligation = _obligation(alternatives=(WitnessSet((_REPOSITORY,)),))
    assessment = _resolved(obligation, (_REPOSITORY,))
    result = _assess(_task(obligation), assessment)

    assert result.readiness is HandoffReadiness.READY
    assert assessment.supported_witnesses[0].target is _REPOSITORY


def test_unconditional_resolution_does_not_claim_applicability_evidence() -> None:
    obligation = _obligation()
    assessment = replace(
        _resolved(obligation),
        applicability=ApplicabilityStatus.APPLIES,
    )
    result = _assess(_task(obligation), assessment)

    assert result.readiness is HandoffReadiness.INVALID_FRAME


def test_conditional_obligation_requires_an_explicit_applicability_assessment() -> None:
    obligation = _obligation(condition="if registration applies")
    assessment = replace(
        _resolved(obligation),
        applicability=ApplicabilityStatus.NOT_REQUIRED,
    )
    result = _assess(_task(obligation), assessment)

    assert result.readiness is HandoffReadiness.INVALID_FRAME


def test_does_not_apply_cannot_also_claim_resolution() -> None:
    obligation = _obligation(condition="if registration applies")
    assessment = replace(
        _resolved(obligation),
        applicability=ApplicabilityStatus.DOES_NOT_APPLY,
        applicability_evidence=(_evidence("not-applicable"),),
    )
    result = _assess(_task(obligation), assessment)

    assert result.readiness is HandoffReadiness.INVALID_FRAME


def test_conditional_not_applicable_requires_same_snapshot_evidence() -> None:
    obligation = _obligation(condition="if registry participation is required")
    assessment = LocalizationAssessment(
        obligation.identity,
        _REPOSITORY,
        _SNAPSHOT,
        Disposition.NOT_APPLICABLE,
        ApplicabilityStatus.DOES_NOT_APPLY,
        (_evidence("not-applicable"),),
    )
    result = _assess(_task(obligation), assessment)

    assert result.readiness is HandoffReadiness.READY
    assert result.not_applicable_mandatory == (obligation.identity,)


def test_absent_conditional_evidence_cannot_become_not_applicable() -> None:
    obligation = _obligation(condition="if registration applies")
    assessment = LocalizationAssessment(
        obligation.identity,
        _REPOSITORY,
        _SNAPSHOT,
        Disposition.NOT_APPLICABLE,
        ApplicabilityStatus.DOES_NOT_APPLY,
    )
    result = _assess(_task(obligation), assessment)

    assert result.readiness is HandoffReadiness.INVALID_FRAME
    assert result.invalid_assessments == (obligation.identity,)


def test_open_mandatory_is_blocked_and_open_helpful_is_diagnostic_only() -> None:
    mandatory = _obligation("implement")
    helpful = _obligation("overview", requirement=RequirementStatus.HELPFUL)
    task = _task(mandatory, helpful)
    assessments = (
        LocalizationAssessment(
            mandatory.identity,
            _REPOSITORY,
            _SNAPSHOT,
            Disposition.OPEN,
        ),
        LocalizationAssessment(
            helpful.identity,
            _REPOSITORY,
            _SNAPSHOT,
            Disposition.OPEN,
        ),
    )
    result = _assess(task, *assessments)

    assert result.readiness is HandoffReadiness.BLOCKED
    assert result.unresolved_mandatory == (mandatory.identity,)
    assert result.unresolved_helpful == (helpful.identity,)


def test_abstention_is_not_mandatory_coverage() -> None:
    obligation = _obligation()
    assessment = LocalizationAssessment(
        obligation.identity,
        _REPOSITORY,
        _SNAPSHOT,
        Disposition.ABSTAINED,
        explanation="candidate evidence is insufficient",
    )
    result = _assess(_task(obligation), assessment)

    assert result.readiness is HandoffReadiness.BLOCKED
    assert result.abstained_mandatory == (obligation.identity,)
    assert result.unresolved_mandatory == (obligation.identity,)


def test_named_accepted_deferred_discovery_permits_only_conditional_handoff() -> None:
    obligation = _obligation()
    assessment = LocalizationAssessment(
        obligation.identity,
        _REPOSITORY,
        _SNAPSHOT,
        Disposition.DEFERRED_DISCOVERY,
        deferred=DeferredDiscovery(
            "run focused validation",
            "runtime registration is revealed on execution",
            accepted_for_handoff=True,
        ),
    )
    result = _assess(_task(obligation), assessment)

    assert result.readiness is HandoffReadiness.CONDITIONAL
    assert not result.is_ready
    assert result.may_handoff
    assert result.deferred_mandatory == (obligation.identity,)


def test_unaccepted_deferred_observation_does_not_permit_handoff() -> None:
    obligation = _obligation()
    assessment = LocalizationAssessment(
        obligation.identity,
        _REPOSITORY,
        _SNAPSHOT,
        Disposition.DEFERRED_DISCOVERY,
        deferred=DeferredDiscovery("inspect runtime", "dynamic behavior"),
    )
    result = _assess(_task(obligation), assessment)

    assert result.readiness is HandoffReadiness.BLOCKED
    assert result.unresolved_mandatory == (obligation.identity,)


def test_resolved_obligation_cannot_be_abstained_or_left_open() -> None:
    obligation = _obligation()
    supported = _resolved(obligation)
    for disposition in (Disposition.OPEN, Disposition.ABSTAINED):
        result = _assess(_task(obligation), replace(supported, disposition=disposition))
        assert result.readiness is HandoffReadiness.INVALID_FRAME


def test_incomplete_obligation_assessment_identity_coverage_is_visible() -> None:
    first, second = _obligation("first"), _obligation("second")
    result = _assess(_task(first, second), _resolved(first))

    assert result.identity_coverage.missing == (second.identity,)
    assert result.unresolved_mandatory == (second.identity,)
    assert result.readiness is HandoffReadiness.INVALID_FRAME


def test_duplicate_and_foreign_assessment_ids_are_invalid() -> None:
    obligation = _obligation()
    resolved = _resolved(obligation)
    duplicate = _assess(_task(obligation), resolved, resolved)
    foreign_id = LocalizationObligationIdentity(obligation.identity.task, "other")
    unexpected = _assess(
        _task(obligation),
        replace(resolved, obligation=foreign_id),
    )

    assert duplicate.identity_coverage.duplicate_observed == (obligation.identity,)
    assert duplicate.invalid_assessments == (obligation.identity,)
    assert unexpected.identity_coverage.unexpected == (foreign_id,)
    assert unexpected.readiness is HandoffReadiness.INVALID_FRAME


def test_snapshot_or_repository_mismatch_invalidates_assessment() -> None:
    obligation = _obligation()
    stale = _resolved(obligation, snapshot=_OTHER_SNAPSHOT)
    stale_evidence = _assess(_task(obligation), stale)
    foreign_repository = RepositoryId.parse("00000000-0000-0000-0000-000000000002")
    other_repository = _resolved(obligation, repository=foreign_repository)
    cross_repository = _assess(_task(obligation), other_repository)

    assert stale_evidence.readiness is HandoffReadiness.INVALID_FRAME
    assert cross_repository.readiness is HandoffReadiness.INVALID_FRAME


def test_stale_evidence_reference_invalidates_current_assessment_frame() -> None:
    obligation = _obligation()
    assessment = replace(
        _resolved(obligation),
        supported_witnesses=(
            SupportedWitness("implementation", (_evidence(snapshot=_OTHER_SNAPSHOT),)),
        ),
    )
    result = _assess(_task(obligation), assessment)

    assert result.readiness is HandoffReadiness.INVALID_FRAME


def test_helpful_resolution_is_not_required_for_mandatory_readiness() -> None:
    required = _obligation("implementation")
    helpful = _obligation("orientation", requirement=RequirementStatus.HELPFUL)
    result = _assess(
        _task(required, helpful),
        _resolved(required),
        LocalizationAssessment(
            helpful.identity,
            _REPOSITORY,
            _SNAPSHOT,
            Disposition.OPEN,
        ),
    )

    assert result.readiness is HandoffReadiness.READY
    assert result.unresolved_helpful == (helpful.identity,)

    resolved_helpful = _assess(
        _task(required, helpful),
        _resolved(required),
        _resolved(helpful),
    )
    assert resolved_helpful.readiness is HandoffReadiness.READY
    assert resolved_helpful.unresolved_helpful == ()


def test_empty_or_incomplete_obligation_frame_never_claims_readiness() -> None:
    empty = _task()
    empty_result = _assess(empty)
    obligation = _obligation()
    missing = _assess(_task(obligation))

    assert empty_result.readiness is HandoffReadiness.BLOCKED
    assert empty_result.frame_errors
    assert missing.readiness is HandoffReadiness.INVALID_FRAME
