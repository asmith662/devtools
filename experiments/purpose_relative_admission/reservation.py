# Copyright (c) 2026
# ruff: noqa: E501, TC001
"""Directional reservation v1 over supplied experiment-local surfaces only."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from devtools.context.repository.resource import RepositoryResourceAddress
from experiments.import_relationship_cases import ImportRelationshipDirection
from experiments.purpose_relative_admission.design import PurposeProfile

_K = 5
_MINIMUM_DISTINCT_SUPPORTS = 2


class AdmissionDisposition(StrEnum):
    """Explicit outcome, including intentional no-admission behavior."""

    ADMITTED = "admitted"
    ABSTAINED = "abstained"


class AbstentionReason(StrEnum):
    """Why this deliberately narrow experiment made no relationship admission."""

    LOCAL_PROFILE = "local-profile"
    NO_QUALIFYING_TARGET = "no-qualifying-target"


@dataclass(frozen=True, slots=True)
class RelationshipSurface:
    """One encountered qualified relation projection with original provenance."""

    address: RepositoryResourceAddress
    direction: ImportRelationshipDirection
    seed_address: RepositoryResourceAddress
    seed_rank: int
    relation_identity: str
    encounter_ordinal: int


@dataclass(frozen=True, slots=True)
class RetainedRelationshipTarget:
    """One deduplicated resource retaining unique relation supports and encounters."""

    address: RepositoryResourceAddress
    direction: ImportRelationshipDirection
    unique_supports: tuple[RelationshipSurface, ...]
    encounters: tuple[RelationshipSurface, ...]

    @property
    def support_count(self) -> int:
        """Count unique underlying declaration-grounded relation identities only."""
        return len(self.unique_supports)

    @property
    def earliest_seed_rank(self) -> int:
        """Retain the best supporting lexical seed rank for deterministic order."""
        return min(surface.seed_rank for surface in self.unique_supports)

    @property
    def earliest_encounter_ordinal(self) -> int:
        """Retain original surface order independent of duplicated encounters."""
        return min(surface.encounter_ordinal for surface in self.encounters)


@dataclass(frozen=True, slots=True)
class DirectionalReservationResult:
    """One non-production admission result with the unchanged lexical ranking."""

    disposition: AdmissionDisposition
    addresses: tuple[RepositoryResourceAddress, ...]
    profile: PurposeProfile
    direction: ImportRelationshipDirection | None
    retained_targets: tuple[RetainedRelationshipTarget, ...]
    admitted_target: RetainedRelationshipTarget | None
    abstention_reason: AbstentionReason | None


def direction_for_profile(profile: PurposeProfile) -> ImportRelationshipDirection | None:
    """Map only the frozen profile to the one permitted relationship direction."""
    if profile is PurposeProfile.OUTGOING_DEPENDENCY:
        return ImportRelationshipDirection.OUTGOING
    if profile is PurposeProfile.INCOMING_CONSUMER_OR_TEST:
        return ImportRelationshipDirection.INCOMING
    return None


def retain_relationship_targets(
    *,
    surfaces: tuple[RelationshipSurface, ...],
    direction: ImportRelationshipDirection,
) -> tuple[RetainedRelationshipTarget, ...]:
    """Deduplicate resources while retaining each distinct relation exactly once."""
    grouped: dict[RepositoryResourceAddress, list[RelationshipSurface]] = {}
    for surface in surfaces:
        if surface.direction is direction:
            grouped.setdefault(surface.address, []).append(surface)
    values: list[RetainedRelationshipTarget] = []
    for address, encounters in grouped.items():
        supports: dict[str, RelationshipSurface] = {}
        for encounter in encounters:
            supports.setdefault(encounter.relation_identity, encounter)
        values.append(
            RetainedRelationshipTarget(
                address=address,
                direction=direction,
                unique_supports=tuple(supports.values()),
                encounters=tuple(encounters),
            ),
        )
    return tuple(values)


def apply_directional_reservation_v1(
    *,
    profile: PurposeProfile,
    canonical_lexical_top_five: tuple[RepositoryResourceAddress, ...],
    surfaces: tuple[RelationshipSurface, ...],
) -> DirectionalReservationResult:
    """Replace only lexical rank five when the frozen profile has one qualifier."""
    if len(canonical_lexical_top_five) != _K:
        msg = "Directional reservation v1 requires exactly five lexical resources."
        raise ValueError(msg)
    direction = direction_for_profile(profile)
    if direction is None:
        return DirectionalReservationResult(
            AdmissionDisposition.ABSTAINED,
            canonical_lexical_top_five,
            profile,
            None,
            (),
            None,
            AbstentionReason.LOCAL_PROFILE,
        )
    retained = retain_relationship_targets(surfaces=surfaces, direction=direction)
    qualifiers = tuple(
        target
        for target in retained
        if target.address not in canonical_lexical_top_five
        and target.support_count >= _MINIMUM_DISTINCT_SUPPORTS
    )
    if not qualifiers:
        return DirectionalReservationResult(
            AdmissionDisposition.ABSTAINED,
            canonical_lexical_top_five,
            profile,
            direction,
            retained,
            None,
            AbstentionReason.NO_QUALIFYING_TARGET,
        )
    admitted = min(
        qualifiers,
        key=lambda target: (
            -target.support_count,
            target.earliest_seed_rank,
            target.earliest_encounter_ordinal,
            str(target.address),
        ),
    )
    return DirectionalReservationResult(
        AdmissionDisposition.ADMITTED,
        (*canonical_lexical_top_five[:4], admitted.address),
        profile,
        direction,
        retained,
        admitted,
        None,
    )
