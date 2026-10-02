# Copyright (c) 2026
"""Deterministic obligation-frame coverage and bounded handoff readiness."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import TYPE_CHECKING

from devtools.context.localization.assessment import (
    ApplicabilityStatus,
    Disposition,
)
from devtools.context.localization.obligation import RequirementStatus
from devtools.evaluation.coverage import IdentityCoverage, compare_identity_coverage

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.localization.assessment import (
        LocalizationAssessment,
        LocalizationEvidenceReference,
    )
    from devtools.context.localization.identity import (
        LocalizationObligationIdentity,
    )
    from devtools.context.localization.obligation import LocalizationObligation
    from devtools.context.localization.task import LocalizationTaskInterpretation
    from devtools.context.repository.identity import RepositoryId
    from devtools.context.repository.snapshot import RepositorySnapshotId


class HandoffReadiness(StrEnum):
    """Distinguish complete, explicitly conditional, and blocked handoff."""

    READY = "ready"
    CONDITIONAL = "conditional"
    BLOCKED = "blocked"
    INVALID_FRAME = "invalid-frame"


@dataclass(frozen=True, slots=True)
class AssessedObligation:
    """Pair one interpreted obligation with its optional matching assessment."""

    obligation: LocalizationObligation
    assessment: LocalizationAssessment | None
    satisfied_alternative_index: int | None


@dataclass(frozen=True, slots=True)
class LocalizationReadiness:
    """Report frame coverage, dispositions, and a scoped handoff decision."""

    task: LocalizationTaskInterpretation
    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    readiness: HandoffReadiness
    identity_coverage: IdentityCoverage[LocalizationObligationIdentity]
    assessed_obligations: tuple[AssessedObligation, ...]
    resolved_mandatory: tuple[LocalizationObligationIdentity, ...]
    not_applicable_mandatory: tuple[LocalizationObligationIdentity, ...]
    unresolved_mandatory: tuple[LocalizationObligationIdentity, ...]
    abstained_mandatory: tuple[LocalizationObligationIdentity, ...]
    deferred_mandatory: tuple[LocalizationObligationIdentity, ...]
    unresolved_helpful: tuple[LocalizationObligationIdentity, ...]
    invalid_assessments: tuple[LocalizationObligationIdentity, ...]
    frame_errors: tuple[str, ...]

    @property
    def is_ready(self) -> bool:
        """Whether every applicable mandatory obligation is fully resolved."""
        return self.readiness is HandoffReadiness.READY

    @property
    def may_handoff(self) -> bool:
        """Whether complete or caller-accepted conditional handoff is permitted."""
        return self.readiness in {
            HandoffReadiness.READY,
            HandoffReadiness.CONDITIONAL,
        }


@dataclass(slots=True)
class _Diagnostics:
    """Accumulate caller-obligation outcomes in task declaration order."""

    resolved: list[LocalizationObligationIdentity] = field(default_factory=list)
    not_applicable: list[LocalizationObligationIdentity] = field(default_factory=list)
    unresolved: list[LocalizationObligationIdentity] = field(default_factory=list)
    abstained: list[LocalizationObligationIdentity] = field(default_factory=list)
    deferred: list[LocalizationObligationIdentity] = field(default_factory=list)
    helpful: list[LocalizationObligationIdentity] = field(default_factory=list)
    invalid: list[LocalizationObligationIdentity] = field(default_factory=list)


@dataclass(slots=True)
class _AssessmentRun:
    """Hold one frame's identities and ordered assessment diagnostics."""

    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    duplicate_identities: set[LocalizationObligationIdentity]
    diagnostics: _Diagnostics


def assess_localization_readiness(
    *,
    task: LocalizationTaskInterpretation,
    repository_id: RepositoryId,
    snapshot_id: RepositorySnapshotId,
    assessments: Sequence[LocalizationAssessment],
) -> LocalizationReadiness:
    """Assess exact task-frame coverage and caller-supplied disposition evidence.

    Checks evidence identities and witness-set satisfaction. It does not inspect
    repository content, execute retrieval, infer applicability, or decide whether
    the caller authored every real task obligation.
    """
    expected = tuple(item.identity for item in task.obligations)
    observed = tuple(item.obligation for item in assessments)
    coverage = compare_identity_coverage(expected=expected, observed=observed)
    by_identity = {item.obligation: item for item in assessments}
    diagnostics = _Diagnostics()
    run = _AssessmentRun(
        repository_id,
        snapshot_id,
        set(coverage.duplicate_observed),
        diagnostics,
    )
    assessed = tuple(
        _assess_obligation(
            obligation,
            by_identity.get(obligation.identity),
            run=run,
        )
        for obligation in task.obligations
    )
    frame_errors = (
        ("Task interpretation has no localization obligations.",)
        if not task.obligations
        else ()
    )
    frame_valid = (
        coverage.is_exact
        and not diagnostics.invalid
        and all(
            item.repository_id == repository_id and item.snapshot_id == snapshot_id
            for item in assessments
        )
        and all(
            _references_match_frame(item, repository_id, snapshot_id)
            for item in assessments
        )
    )
    readiness = _readiness_state(
        frame_valid=frame_valid,
        frame_errors=frame_errors,
        diagnostics=diagnostics,
    )
    return LocalizationReadiness(
        task=task,
        repository_id=repository_id,
        snapshot_id=snapshot_id,
        readiness=readiness,
        identity_coverage=coverage,
        assessed_obligations=assessed,
        resolved_mandatory=tuple(diagnostics.resolved),
        not_applicable_mandatory=tuple(diagnostics.not_applicable),
        unresolved_mandatory=tuple(diagnostics.unresolved),
        abstained_mandatory=tuple(diagnostics.abstained),
        deferred_mandatory=tuple(diagnostics.deferred),
        unresolved_helpful=tuple(diagnostics.helpful),
        invalid_assessments=tuple(diagnostics.invalid),
        frame_errors=frame_errors,
    )


def _assess_obligation(
    obligation: LocalizationObligation,
    assessment: LocalizationAssessment | None,
    *,
    run: _AssessmentRun,
) -> AssessedObligation:
    """Validate one assessment and append its task-local diagnostic disposition."""
    alternative = None
    invalid = obligation.identity in run.duplicate_identities
    if assessment is not None:
        invalid |= not _assessment_matches_frame(
            assessment,
            obligation,
            repository_id=run.repository_id,
            snapshot_id=run.snapshot_id,
        )
        alternative = _satisfied_alternative(obligation, assessment)
        invalid |= not _consistent_disposition(
            obligation,
            assessment,
            satisfied_alternative=alternative,
        )
    if invalid:
        run.diagnostics.invalid.append(obligation.identity)
    _record_disposition(
        obligation,
        assessment,
        invalid=invalid,
        diagnostics=run.diagnostics,
    )
    return AssessedObligation(obligation, assessment, alternative)


def _record_disposition(
    obligation: LocalizationObligation,
    assessment: LocalizationAssessment | None,
    *,
    invalid: bool,
    diagnostics: _Diagnostics,
) -> None:
    """Keep helpful diagnostics outside mandatory coverage."""
    if obligation.requirement is RequirementStatus.HELPFUL:
        _record_helpful(
            obligation,
            assessment,
            invalid=invalid,
            diagnostics=diagnostics,
        )
    else:
        _record_mandatory(
            obligation,
            assessment,
            invalid=invalid,
            diagnostics=diagnostics,
        )


def _record_helpful(
    obligation: LocalizationObligation,
    assessment: LocalizationAssessment | None,
    *,
    invalid: bool,
    diagnostics: _Diagnostics,
) -> None:
    """Record helpful obligations not resolved within this frame."""
    if (
        assessment is None
        or invalid
        or assessment.disposition
        not in {Disposition.RESOLVED, Disposition.NOT_APPLICABLE}
    ):
        diagnostics.helpful.append(obligation.identity)


def _record_mandatory(
    obligation: LocalizationObligation,
    assessment: LocalizationAssessment | None,
    *,
    invalid: bool,
    diagnostics: _Diagnostics,
) -> None:
    """Classify mandatory coverage without treating deferral as resolution."""
    if assessment is None or invalid:
        diagnostics.unresolved.append(obligation.identity)
    elif assessment.disposition is Disposition.RESOLVED:
        diagnostics.resolved.append(obligation.identity)
    elif assessment.disposition is Disposition.NOT_APPLICABLE:
        diagnostics.not_applicable.append(obligation.identity)
    elif assessment.disposition is Disposition.ABSTAINED:
        diagnostics.abstained.append(obligation.identity)
        diagnostics.unresolved.append(obligation.identity)
    elif assessment.disposition is Disposition.DEFERRED_DISCOVERY:
        diagnostics.deferred.append(obligation.identity)
        if assessment.deferred is None or not assessment.deferred.accepted_for_handoff:
            diagnostics.unresolved.append(obligation.identity)
    else:
        diagnostics.unresolved.append(obligation.identity)


def _readiness_state(
    *,
    frame_valid: bool,
    frame_errors: tuple[str, ...],
    diagnostics: _Diagnostics,
) -> HandoffReadiness:
    """Prioritize invalid input, open obligations, deferral, then readiness."""
    if not frame_valid:
        return HandoffReadiness.INVALID_FRAME
    if frame_errors or diagnostics.unresolved:
        return HandoffReadiness.BLOCKED
    if diagnostics.deferred:
        return HandoffReadiness.CONDITIONAL
    return HandoffReadiness.READY


def _assessment_matches_frame(
    assessment: LocalizationAssessment,
    obligation: LocalizationObligation,
    *,
    repository_id: RepositoryId,
    snapshot_id: RepositorySnapshotId,
) -> bool:
    """Check status semantics, applicability evidence, and witness provenance."""
    if (
        assessment.repository_id != repository_id
        or assessment.snapshot_id != snapshot_id
    ):
        return False
    if obligation.applicability_condition is None:
        if assessment.applicability is not ApplicabilityStatus.NOT_REQUIRED:
            return False
    elif assessment.applicability is ApplicabilityStatus.NOT_REQUIRED:
        return False
    needs_condition_evidence = assessment.applicability in {
        ApplicabilityStatus.APPLIES,
        ApplicabilityStatus.DOES_NOT_APPLY,
    }
    if needs_condition_evidence and not assessment.applicability_evidence:
        return False
    return all(
        item.repository_id == repository_id and item.snapshot_id == snapshot_id
        for item in _evidence_references(assessment)
    )


def _satisfied_alternative(
    obligation: LocalizationObligation,
    assessment: LocalizationAssessment,
) -> int | None:
    """Return the first completely supported caller-declared witness alternative."""
    supports = {item.target for item in assessment.supported_witnesses}
    return next(
        (
            index
            for index, alternative in enumerate(obligation.witness_alternatives)
            if set(alternative.members) <= supports
        ),
        None,
    )


def _consistent_disposition(
    obligation: LocalizationObligation,
    assessment: LocalizationAssessment,
    *,
    satisfied_alternative: int | None,
) -> bool:
    """Reject claims that contradict the obligation's condition or witness sets."""
    conditional = obligation.applicability_condition is not None
    if assessment.disposition is Disposition.NOT_APPLICABLE:
        return (
            conditional
            and assessment.applicability is ApplicabilityStatus.DOES_NOT_APPLY
            and bool(assessment.applicability_evidence)
            and not assessment.supported_witnesses
        )
    if assessment.applicability is ApplicabilityStatus.DOES_NOT_APPLY:
        return False
    if assessment.disposition is Disposition.RESOLVED:
        return (
            not conditional or assessment.applicability is ApplicabilityStatus.APPLIES
        ) and satisfied_alternative is not None
    return satisfied_alternative is None


def _references_match_frame(
    assessment: LocalizationAssessment,
    repository_id: RepositoryId,
    snapshot_id: RepositorySnapshotId,
) -> bool:
    """Reject evidence from a foreign Repository or retained Snapshot."""
    return all(
        item.repository_id == repository_id and item.snapshot_id == snapshot_id
        for item in _evidence_references(assessment)
    )


def _evidence_references(
    assessment: LocalizationAssessment,
) -> tuple[LocalizationEvidenceReference, ...]:
    """Collect exact provenance from applicability and witness supports."""
    return (
        *assessment.applicability_evidence,
        *(
            reference
            for witness in assessment.supported_witnesses
            for reference in witness.evidence
        ),
    )
