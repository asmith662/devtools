# Copyright (c) 2026
# ruff: noqa: COM812
"""Deterministic partial resolution snapshots over an exact candidate view."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context.localization.association import (
    GeneratedWitnessHypothesisIdentity,
    build_candidate_witness_view,
)
from devtools.context.localization.resolution.contract import (
    CandidateHypothesisResolution,
    CandidateMemberResolution,
    HypothesisResolutionDisposition,
)

if TYPE_CHECKING:
    from devtools.context.localization.association import (
        CandidateWitnessHypothesis,
        CandidateWitnessView,
        WitnessHypothesisFamilyIdentity,
    )
    from devtools.context.localization.association.hypothesis import (
        CandidateHypothesisIdentity,
    )
    from devtools.context.localization.identity import LocalizationObligationIdentity
    from devtools.context.repository.resource import RepositoryResourceOccurrence


@dataclass(frozen=True, slots=True)
class WitnessResolutionView:
    """Cover an explicit subset, with one decision per recorded candidate member."""

    candidates: CandidateWitnessView
    records: tuple[CandidateMemberResolution, ...] = ()

    def __post_init__(self) -> None:
        """Validate the association frame and canonicalize partial decisions."""
        candidates = self.candidates
        if not candidates.hypotheses:
            msg = "Resolution requires a nonempty candidate frame."
            raise ValueError(msg)
        validated = build_candidate_witness_view(
            task=candidates.task,
            snapshot=candidates.snapshot,
            hypotheses=candidates.hypotheses,
            acquisition=candidates.acquisition,
            role_evidence=candidates.role_evidence,
            routing=candidates.routing,
        )
        if validated.hypotheses != candidates.hypotheses:
            msg = "Resolution candidate view must retain canonical association order."
            raise ValueError(msg)
        if any(item.candidates is not candidates for item in self.records):
            msg = "Resolution record belongs to a different or stale candidate view."
            raise ValueError(msg)
        keys = [(item.hypothesis.identity, item.member.target) for item in self.records]
        if len(set(keys)) != len(keys):
            msg = "Resolution view repeats a member decision."
            raise ValueError(msg)
        order = {
            item.identity: index for index, item in enumerate(candidates.hypotheses)
        }
        object.__setattr__(
            self,
            "records",
            tuple(
                sorted(
                    self.records,
                    key=lambda item: (
                        order[item.hypothesis.identity],
                        item.member.target.address.value,
                    ),
                )
            ),
        )

    def for_hypothesis(
        self, identity: CandidateHypothesisIdentity
    ) -> CandidateHypothesisResolution | None:
        """Return no record separately from an explicitly unresolved aggregate."""
        hypothesis = self._hypothesis(identity)
        members = tuple(item for item in self.records if item.hypothesis is hypothesis)
        return (
            CandidateHypothesisResolution(self.candidates, hypothesis, members)
            if members
            else None
        )

    def for_member(
        self,
        identity: CandidateHypothesisIdentity,
        target: RepositoryResourceOccurrence,
    ) -> CandidateMemberResolution | None:
        """Inspect one exact member, including absence of a decision."""
        hypothesis = self._hypothesis(identity)
        if not any(item.target == target for item in hypothesis.members):
            msg = "Resolution query names a foreign or stale member target."
            raise ValueError(msg)
        return next(
            (
                item
                for item in self.records
                if item.hypothesis is hypothesis and item.member.target == target
            ),
            None,
        )

    def for_obligation(
        self, obligation: LocalizationObligationIdentity
    ) -> tuple[CandidateHypothesisResolution, ...]:
        """Keep competing recorded hypotheses independently queryable."""
        self.candidates.for_obligation(obligation)
        return tuple(
            item
            for item in self.hypotheses
            if item.hypothesis.identity.obligation == obligation
        )

    def for_family(
        self, family: WitnessHypothesisFamilyIdentity
    ) -> tuple[CandidateHypothesisResolution, ...]:
        """Inspect concrete admitted children without resolving their parent family."""
        children = tuple(
            item
            for item in self.candidates.hypotheses
            if isinstance(item.identity, GeneratedWitnessHypothesisIdentity)
            and item.identity.family == family
        )
        if not children:
            msg = "Resolution candidate view has no such admitted family."
            raise ValueError(msg)
        return tuple(item for item in self.hypotheses if item.hypothesis in children)

    @property
    def hypotheses(self) -> tuple[CandidateHypothesisResolution, ...]:
        """Expose only hypotheses with at least one recorded member decision."""
        return tuple(
            result
            for item in self.candidates.hypotheses
            if (result := self.for_hypothesis(item.identity)) is not None
        )

    @property
    def completely_supported(self) -> tuple[CandidateHypothesisResolution, ...]:
        """Expose complete candidate support without witness promotion."""
        return self._with_disposition(
            HypothesisResolutionDisposition.COMPLETELY_SUPPORTED
        )

    @property
    def unresolved(self) -> tuple[CandidateHypothesisResolution, ...]:
        """Expose recorded incomplete hypotheses; absence remains separate."""
        return self._with_disposition(HypothesisResolutionDisposition.UNRESOLVED)

    @property
    def contradicted(self) -> tuple[CandidateHypothesisResolution, ...]:
        """Retain incompatible-fact judgments without eliminating candidates."""
        return self._with_disposition(HypothesisResolutionDisposition.CONTRADICTED)

    @property
    def unrecorded(self) -> tuple[CandidateWitnessHypothesis, ...]:
        """Expose hypotheses for which no member decision has been recorded."""
        return tuple(
            item
            for item in self.candidates.hypotheses
            if self.for_hypothesis(item.identity) is None
        )

    @property
    def supported_obligations(self) -> tuple[LocalizationObligationIdentity, ...]:
        """Report supported candidate presence, not satisfied obligation coverage."""
        supported = {
            item.hypothesis.identity.obligation for item in self.completely_supported
        }
        return tuple(
            item.identity
            for item in self.candidates.task.obligations
            if item.identity in supported
        )

    def _hypothesis(
        self, identity: CandidateHypothesisIdentity
    ) -> CandidateWitnessHypothesis:
        for item in self.candidates.hypotheses:
            if item.identity == identity:
                return item
        msg = "Resolution candidate view has no such hypothesis."
        raise ValueError(msg)

    def _with_disposition(
        self, disposition: HypothesisResolutionDisposition
    ) -> tuple[CandidateHypothesisResolution, ...]:
        return tuple(
            item for item in self.hypotheses if item.disposition is disposition
        )
