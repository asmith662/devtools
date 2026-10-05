# Copyright (c) 2026
# ruff: noqa: COM812
"""Explicit caller judgments over existing candidate evidence."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.context.localization.assessment import LocalizationEvidenceReference
    from devtools.context.localization.association import (
        CandidateWitnessHypothesis,
        CandidateWitnessMember,
        CandidateWitnessView,
    )
    from devtools.context.localization.identity import (
        LocalizationObligationIdentity,
        LocalizationTaskIdentity,
        TaskProvenance,
    )
    from devtools.context.localization.obligation import SatisfactionCriterion
    from devtools.context.repository.identity import RepositoryId
    from devtools.context.repository.snapshot import RepositorySnapshotId


class MemberResolutionDisposition(StrEnum):
    """Keep established support, missing judgment and explicit contradiction apart."""

    SUPPORTED = "supported"
    UNRESOLVED = "unresolved"
    ABSTAINED = "abstained"
    CONTRADICTED = "contradicted"


class HypothesisResolutionDisposition(StrEnum):
    """Derive all-member support without accepting a witness automatically."""

    COMPLETELY_SUPPORTED = "completely-supported"
    UNRESOLVED = "unresolved"
    CONTRADICTED = "contradicted"


@dataclass(frozen=True, slots=True)
class CandidateMemberResolution:
    """Record one caller decision in an exact retained association context.

    Basis identities are the native support values attached to this member,
    wrapped in existing snapshot-qualified evidence references. They establish
    lineage, not the logical truth of the caller's claim.
    """

    candidates: CandidateWitnessView
    hypothesis: CandidateWitnessHypothesis
    member: CandidateWitnessMember
    disposition: MemberResolutionDisposition
    criterion: SatisfactionCriterion
    claim: str
    reason: str
    caller: str
    provenance: TaskProvenance
    basis: tuple[LocalizationEvidenceReference, ...] = ()

    def __post_init__(self) -> None:
        """Validate exact membership, criterion and caller-owned evidence lineage."""
        if not isinstance(self.disposition, MemberResolutionDisposition):
            msg = "Member resolution needs an explicit disposition."
            raise TypeError(msg)
        if not all(text.strip() for text in (self.claim, self.reason, self.caller)):
            msg = "Member resolution needs a claim, reason and named caller."
            raise ValueError(msg)
        if not any(item is self.hypothesis for item in self.candidates.hypotheses):
            msg = "Resolution hypothesis is foreign or stale to its candidate view."
            raise ValueError(msg)
        if not any(item is self.member for item in self.hypothesis.members):
            msg = "Resolution member is foreign to its exact candidate hypothesis."
            raise ValueError(msg)
        obligation = next(
            (
                item
                for item in self.candidates.task.obligations
                if item.identity == self.hypothesis.identity.obligation
            ),
            None,
        )
        if obligation is None or self.criterion != obligation.satisfaction:
            msg = "Resolution criterion differs from the obligation criterion."
            raise ValueError(msg)
        if (
            self.disposition
            in {
                MemberResolutionDisposition.SUPPORTED,
                MemberResolutionDisposition.CONTRADICTED,
            }
            and not self.basis
        ):
            msg = "Support or contradiction requires an explicit evidence basis."
            raise ValueError(msg)
        self._validate_basis()

    def _validate_basis(self) -> None:
        """Canonicalize only exact attached native supports in this frame."""
        supports = (
            *self.member.lexical,
            *self.member.roles,
            *self.member.routed,
            *self.member.structural,
        )
        positions = []
        for reference in self.basis:
            if (
                reference.repository_id != self.repository_id
                or reference.snapshot_id != self.snapshot_id
            ):
                msg = "Resolution evidence is foreign to the repository/snapshot."
                raise ValueError(msg)
            position = next(
                (
                    index
                    for index, support in enumerate(supports)
                    if support is reference.identity
                ),
                None,
            )
            if position is None:
                msg = "Resolution evidence is not an exact attached member support."
                raise ValueError(msg)
            positions.append(position)
        if len(set(positions)) != len(positions):
            msg = "Resolution basis repeats native support."
            raise ValueError(msg)
        object.__setattr__(
            self,
            "basis",
            tuple(
                reference
                for _, reference in sorted(zip(positions, self.basis, strict=True))
            ),
        )

    @property
    def task(self) -> LocalizationTaskIdentity:
        """Retain the exact task identity without a parallel resolution task."""
        return self.candidates.task.identity

    @property
    def obligation(self) -> LocalizationObligationIdentity:
        """Bind the decision to the candidate's named obligation."""
        return self.hypothesis.identity.obligation

    @property
    def repository_id(self) -> RepositoryId:
        """Use the retained candidate repository frame."""
        return self.candidates.snapshot.repository_id

    @property
    def snapshot_id(self) -> RepositorySnapshotId:
        """Use the retained candidate snapshot frame."""
        return self.candidates.snapshot.id


@dataclass(frozen=True, slots=True)
class CandidateHypothesisResolution:
    """Retain recorded conjunct decisions and derive their hypothesis state."""

    candidates: CandidateWitnessView
    hypothesis: CandidateWitnessHypothesis
    members: tuple[CandidateMemberResolution, ...]

    def __post_init__(self) -> None:
        """Require at least one decision and reject mixed or repeated members."""
        if not self.members or any(
            item.candidates is not self.candidates
            or item.hypothesis is not self.hypothesis
            for item in self.members
        ):
            msg = "Hypothesis resolution needs decisions from its exact frame."
            raise ValueError(msg)
        if len({item.member.target for item in self.members}) != len(self.members):
            msg = "Hypothesis resolution repeats a member decision."
            raise ValueError(msg)
        object.__setattr__(
            self,
            "members",
            tuple(
                sorted(
                    self.members,
                    key=lambda item: item.member.target.address.value,
                )
            ),
        )

    @property
    def disposition(self) -> HypothesisResolutionDisposition:
        """Contradiction dominates; complete support needs every conjunct."""
        if any(
            item.disposition is MemberResolutionDisposition.CONTRADICTED
            for item in self.members
        ):
            return HypothesisResolutionDisposition.CONTRADICTED
        if len(self.members) == len(self.hypothesis.members) and all(
            item.disposition is MemberResolutionDisposition.SUPPORTED
            for item in self.members
        ):
            return HypothesisResolutionDisposition.COMPLETELY_SUPPORTED
        return HypothesisResolutionDisposition.UNRESOLVED

    @property
    def unrecorded_members(self) -> tuple[CandidateWitnessMember, ...]:
        """Distinguish missing decisions from explicitly unresolved decisions."""
        recorded = {item.member.target for item in self.members}
        return tuple(
            item for item in self.hypothesis.members if item.target not in recorded
        )
