# Copyright (c) 2026
# ruff: noqa: E501, FBT001, FBT003, PLR0913, PLR2004, TC001
"""Evaluate a frozen Increment-23 capture only after blinded adjudication."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

from devtools.context.repository.resource import RepositoryResourceAddress
from experiments.purpose_relative_admission.reservation import (
    AbstentionReason,
    AdmissionDisposition,
)
from experiments.purpose_relative_admission.validation_adjudication import (
    AdjudicationResourceMapping,
    BlindedAdjudicationPackage,
    FrozenAdjudication,
    ImmutableAdjudicationRecord,
    UnblindedAdjudication,
    unblind_records,
)
from experiments.purpose_relative_admission.validation_capture import (
    CapturedCaseSurface,
)
from experiments.purpose_relative_admission.validation_design import (
    FrozenValidationCase,
)
from experiments.purpose_relative_import.cases import UsefulnessJudgment

if TYPE_CHECKING:
    from collections.abc import Sequence


class EvidenceState(StrEnum):
    """Avoid converting unobserved or incomplete evidence into a numeric claim."""

    OBSERVED = "observed"
    NOT_OBSERVED = "not-observed"
    NOT_APPLICABLE = "not-applicable"
    INSUFFICIENT_JUDGMENT = "insufficient-judgment"


class ControlConflictDisposition(StrEnum):
    """Resolve one reviewed experiment-local expectation disagreement."""

    CONTROL_EXPECTATION_UNSUPPORTED = "control-expectation-unsupported"
    BLINDED_JUDGMENT_UNSUPPORTED = "blinded-judgment-unsupported"
    AMBIGUOUS_USEFULNESS = "ambiguous-usefulness"
    PROJECTION_INDUCED_FALSE_POSITIVE = "projection-induced-false-positive"


@dataclass(frozen=True, slots=True)
class MetricEvidence:
    """One scalar only when its denominator and judgments support it."""

    state: EvidenceState
    value: float | None
    detail: str


@dataclass(frozen=True, slots=True)
class FailureObservation:
    """A factual localization observation; cases can have more than one."""

    category: str
    state: EvidenceState
    detail: str


@dataclass(frozen=True, slots=True)
class PostUnblindingControlAnnotation:
    """Attach frozen experiment-control truth only after address correlation."""

    neutral_id: str
    address: RepositoryResourceAddress
    provenance: str


@dataclass(frozen=True, slots=True)
class ControlAdjudicationConflictReview:
    """Retain one post-unblinding review without changing either frozen input."""

    case_name: str
    neutral_id: str
    address: RepositoryResourceAddress
    frozen_blinded_judgment: UsefulnessJudgment
    frozen_control_expectation: UsefulnessJudgment
    original_control_rationale: str
    reviewed_evidence: tuple[str, ...]
    disposition: ControlConflictDisposition
    rationale: str


@dataclass(frozen=True, slots=True)
class ValidationCaseEvaluation:
    """Post-unblinding diagnostic evidence, not a production selection result."""

    case_name: str
    canonical_top_five: tuple[RepositoryResourceAddress, ...]
    practical_top_five: tuple[RepositoryResourceAddress, ...]
    useful_admissions: tuple[RepositoryResourceAddress, ...]
    admitted_not_useful_controls: tuple[RepositoryResourceAddress, ...]
    useful_rank_five_displacement: bool | None
    useful_losses: tuple[RepositoryResourceAddress, ...]
    abstention_appropriate: bool | None
    metrics: tuple[tuple[str, MetricEvidence], ...]
    failures: tuple[FailureObservation, ...]
    direct_resolution_applicable_to_k5: bool


def evaluate_frozen_case(
    *,
    package: BlindedAdjudicationPackage,
    case: FrozenValidationCase,
    capture: CapturedCaseSurface,
    frozen: FrozenAdjudication,
    mappings: Sequence[AdjudicationResourceMapping],
    initial_useful: frozenset[RepositoryResourceAddress] = frozenset(),
) -> ValidationCaseEvaluation:
    """Combine retained mechanism facts with already-frozen manual judgments."""
    if case.name != capture.case_name:
        msg = "Frozen validation case differs from captured case."
        raise ValueError(msg)
    unblinded = unblind_records(
        package=package,
        capture=capture,
        frozen=frozen,
        mappings=mappings,
    )
    control_annotations = annotate_controls_after_unblinding(
        case=case,
        unblinded=unblinded,
    )
    records = unblinded.by_address()
    canonical = tuple(item.address for item in capture.lexical_top_five)
    practical = capture.practical.addresses
    eligible = {item.address for item in capture.profile_eligible_surfaces}
    qualified = {
        target.address
        for target in capture.retained_targets
        if target.address not in canonical and target.support_count >= 2
    }
    admitted = capture.practical.admitted_target.address if capture.practical.admitted_target else None
    useful = {address for address, record in records.items() if record.judgment is UsefulnessJudgment.USEFUL}
    useful |= set(initial_useful)
    controls = {annotation.address for annotation in control_annotations}
    useful_controls = {
        address
        for address in controls
        if records[address].judgment is UsefulnessJudgment.USEFUL
    }
    unjudged_controls = {
        address
        for address in controls
        if records[address].judgment is UsefulnessJudgment.UNJUDGED
    }
    unjudged = {address for address, record in records.items() if record.judgment is UsefulnessJudgment.UNJUDGED}
    final_metrics_allowed = not unjudged

    admitted_record = records.get(admitted) if admitted else None
    useful_admissions: tuple[RepositoryResourceAddress, ...] = ()
    admitted_controls: tuple[RepositoryResourceAddress, ...] = ()
    if admitted is not None and admitted_record is not None:
        if admitted_record.judgment is UsefulnessJudgment.USEFUL:
            useful_admissions = (admitted,)
        if (
            admitted in controls
            and admitted_record.judgment is UsefulnessJudgment.NOT_USEFUL
        ):
            admitted_controls = (admitted,)
    rank_five_record = records[capture.rank_five_address]
    displaced = capture.rank_five_address not in practical
    useful_rank_five_displacement = (
        displaced if rank_five_record.judgment is UsefulnessJudgment.USEFUL else False
        if rank_five_record.judgment is UsefulnessJudgment.NOT_USEFUL
        else None
    )
    useful_losses = tuple(address for address in canonical if address in useful and address not in practical)
    metrics = _metrics(
        capture=capture,
        records=records,
        useful=useful,
        controls=controls,
        qualified=qualified,
        admitted=admitted,
        final_metrics_allowed=final_metrics_allowed,
    )
    abstention_appropriate = _abstention_appropriateness(
        capture=capture,
        qualified=qualified,
        useful=useful,
        unjudged=unjudged,
    )
    failures = _failure_observations(
        capture=capture,
        qualified=qualified,
        eligible=eligible,
        controls=controls,
        admitted=admitted,
        useful_controls=useful_controls,
        unjudged_controls=unjudged_controls,
        useful_rank_five_displacement=useful_rank_five_displacement,
        abstention_appropriate=abstention_appropriate,
        final_metrics_allowed=final_metrics_allowed,
    )
    return ValidationCaseEvaluation(
        capture.case_name,
        canonical,
        practical,
        useful_admissions,
        admitted_controls,
        useful_rank_five_displacement,
        useful_losses,
        abstention_appropriate,
        tuple(metrics.items()),
        failures,
        False,
    )


def annotate_controls_after_unblinding(
    *,
    case: FrozenValidationCase,
    unblinded: UnblindedAdjudication,
) -> tuple[PostUnblindingControlAnnotation, ...]:
    """Join frozen control truth to already-unblinded immutable judgments."""
    records = unblinded.by_address()
    judgment_controls = {
        judgment.address: judgment
        for judgment in case.judgments
        if judgment.is_control
    }
    relationship_controls = {
        control.address: control for control in case.relationship_controls
    }
    if set(judgment_controls) != set(relationship_controls):
        msg = "Frozen control judgments and relationship-control evidence differ."
        raise ValueError(msg)
    if any(
        judgment.judgment is not UsefulnessJudgment.NOT_USEFUL
        for judgment in judgment_controls.values()
    ):
        msg = "Frozen explicit controls must carry NOT_USEFUL design truth."
        raise ValueError(msg)
    return tuple(
        PostUnblindingControlAnnotation(
            records[address].neutral_id,
            address,
            f"frozen-validation-case:{case.name}",
        )
        for address in judgment_controls
        if address in records
    )


def _metrics(
    *,
    capture: CapturedCaseSurface,
    records: dict[RepositoryResourceAddress, ImmutableAdjudicationRecord],
    useful: set[RepositoryResourceAddress],
    controls: set[RepositoryResourceAddress],
    qualified: set[RepositoryResourceAddress],
    admitted: RepositoryResourceAddress | None,
    final_metrics_allowed: bool,
) -> dict[str, MetricEvidence]:
    canonical = {item.address for item in capture.lexical_top_five}
    lexical_fifteen = {item.address for item in capture.lexical_top_fifteen}
    relationships = {item.address for item in capture.profile_eligible_surfaces}
    if not useful:
        surface_recall = MetricEvidence(EvidenceState.NOT_APPLICABLE, None, "No USEFUL resources were adjudicated.")
    else:
        surface_recall = MetricEvidence(EvidenceState.OBSERVED, len(useful & set(capture.material_addresses)) / len(useful), "Useful material resources present in the adjudicated consideration set.")
    admitted_record = records.get(admitted) if admitted else None
    admission_precision = (
        MetricEvidence(EvidenceState.NOT_APPLICABLE, None, "No relationship target was admitted.")
        if admitted is None
        else MetricEvidence(EvidenceState.INSUFFICIENT_JUDGMENT, None, "Admitted target is UNJUDGED.")
        if admitted_record and admitted_record.judgment is UsefulnessJudgment.UNJUDGED
        else MetricEvidence(EvidenceState.OBSERVED, 1.0 if admitted_record and admitted_record.judgment is UsefulnessJudgment.USEFUL else 0.0, "One fully judged admission.")
    )
    qualified_useful = useful & qualified
    admission_recall = (
        MetricEvidence(EvidenceState.NOT_APPLICABLE, None, "No qualified USEFUL target exists.")
        if not qualified_useful
        else MetricEvidence(EvidenceState.OBSERVED, float(admitted in qualified_useful), "Admission among qualified USEFUL targets.")
    )
    eligible_controls = controls & relationships
    return {
        "surface_recall": surface_recall,
        "useful_relationship_beyond_top_5": _count_evidence(useful & relationships - canonical, "Useful profile-eligible relation targets absent from lexical top five."),
        "useful_relationship_beyond_top_15": _count_evidence(useful & relationships - lexical_fifteen, "Useful profile-eligible relation targets absent from lexical top fifteen."),
        "qualification_rate_for_surfaced_useful": _ratio_evidence(len(qualified_useful), len(useful & relationships), "Qualified share of surfaced USEFUL relationship targets."),
        "useful_admission_precision": admission_precision,
        "admission_recall_conditional_on_qualified_useful": admission_recall,
        "eligible_control_exposure": _count_evidence(eligible_controls, "Post-unblinding explicit controls reaching the eligible relation surface."),
        "eligible_control_qualification": _count_evidence(eligible_controls & qualified, "Eligible controls meeting the support threshold."),
        "eligible_control_admission": _count_evidence(eligible_controls & {admitted} if admitted else set(), "Eligible controls admitted by the practical rule."),
        "final_hit_at_5": _ranking_metric(final_metrics_allowed, capture.practical.addresses, useful, "hit"),
        "final_recall_at_5": _ranking_metric(final_metrics_allowed, capture.practical.addresses, useful, "recall"),
        "final_mrr": _ranking_metric(final_metrics_allowed, capture.practical.addresses, useful, "mrr"),
    }


def _count_evidence(addresses: set[RepositoryResourceAddress], detail: str) -> MetricEvidence:
    return MetricEvidence(EvidenceState.OBSERVED, float(len(addresses)), detail)


def _ratio_evidence(numerator: int, denominator: int, detail: str) -> MetricEvidence:
    if not denominator:
        return MetricEvidence(EvidenceState.NOT_APPLICABLE, None, detail)
    return MetricEvidence(EvidenceState.OBSERVED, numerator / denominator, detail)


def _ranking_metric(allowed: bool, addresses: tuple[RepositoryResourceAddress, ...], useful: set[RepositoryResourceAddress], kind: str) -> MetricEvidence:
    if not allowed:
        return MetricEvidence(EvidenceState.INSUFFICIENT_JUDGMENT, None, "Material surface includes UNJUDGED evidence.")
    if not useful:
        return MetricEvidence(EvidenceState.NOT_APPLICABLE, None, "No USEFUL resources were adjudicated.")
    recovered = tuple(address for address in addresses[:5] if address in useful)
    if kind == "hit":
        value = float(bool(recovered))
    elif kind == "recall":
        value = len(recovered) / len(useful)
    else:
        value = next((1 / rank for rank, address in enumerate(addresses[:5], start=1) if address in useful), 0.0)
    return MetricEvidence(EvidenceState.OBSERVED, value, "Final practical top-five metric.")


def _abstention_appropriateness(*, capture: CapturedCaseSurface, qualified: set[RepositoryResourceAddress], useful: set[RepositoryResourceAddress], unjudged: set[RepositoryResourceAddress]) -> bool | None:
    if capture.practical.disposition is AdmissionDisposition.ADMITTED:
        return None
    if capture.practical.abstention_reason is AbstentionReason.LOCAL_PROFILE:
        return True
    if unjudged & qualified:
        return None
    return not bool(useful & qualified)


def _failure_observations(*, capture: CapturedCaseSurface, qualified: set[RepositoryResourceAddress], eligible: set[RepositoryResourceAddress], controls: set[RepositoryResourceAddress], admitted: RepositoryResourceAddress | None, useful_controls: set[RepositoryResourceAddress], unjudged_controls: set[RepositoryResourceAddress], useful_rank_five_displacement: bool | None, abstention_appropriate: bool | None, final_metrics_allowed: bool) -> tuple[FailureObservation, ...]:
    observations: list[FailureObservation] = []
    control_eligible = controls & eligible
    if useful_controls:
        observations.append(FailureObservation("adjudication", EvidenceState.OBSERVED, "A frozen USEFUL judgment contradicts post-unblinding explicit-control truth."))
    if unjudged_controls:
        observations.append(FailureObservation("judgment-coverage", EvidenceState.INSUFFICIENT_JUDGMENT, "An explicit control remains UNJUDGED; its usefulness was not coerced."))
    if controls and not control_eligible:
        observations.append(FailureObservation("rejection", EvidenceState.NOT_OBSERVED, "Controls did not reach the eligible surface; this is non-exposure, not rejection."))
    if control_eligible & qualified:
        state = EvidenceState.OBSERVED if admitted not in control_eligible else EvidenceState.NOT_OBSERVED
        observations.append(FailureObservation("rejection", state, "Qualified explicit controls were rejected." if state is EvidenceState.OBSERVED else "A qualified explicit control was admitted."))
    if useful_rank_five_displacement is True:
        observations.append(FailureObservation("reservation-capacity", EvidenceState.OBSERVED, "A confirmed USEFUL lexical rank-five resource was displaced."))
    if capture.practical.disposition is AdmissionDisposition.ABSTAINED:
        state = EvidenceState.OBSERVED if abstention_appropriate else EvidenceState.NOT_OBSERVED if abstention_appropriate is False else EvidenceState.INSUFFICIENT_JUDGMENT
        observations.append(FailureObservation("abstention", state, "Abstention appropriateness after frozen adjudication."))
    if not final_metrics_allowed:
        observations.append(FailureObservation("judgment-coverage", EvidenceState.INSUFFICIENT_JUDGMENT, "UNJUDGED material evidence prevents final evaluative claims."))
    return tuple(observations)
