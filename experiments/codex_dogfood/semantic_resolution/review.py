# Copyright (c) 2026
# ruff: noqa: COM812
"""Separate human review artifacts and explicit kernel materialization."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

from devtools.context.localization.assessment import LocalizationEvidenceReference
from devtools.context.localization.identity import TaskProvenance
from devtools.context.localization.resolution import (
    CandidateMemberResolution,
    WitnessResolutionView,
)
from experiments.codex_dogfood.semantic_resolution._identity import digest, require_text
from experiments.codex_dogfood.semantic_resolution.contract import (
    SCHEMA,
    SemanticDecisionBatch,
    SemanticDecisionRequest,
    SemanticResolutionProposal,
)

if TYPE_CHECKING:
    from devtools.context.localization.association import CandidateWitnessView


class ReviewDecision(StrEnum):
    """An explicit reviewer verdict, not a semantic decision from the producer."""

    ACCEPT = "accept"
    REJECT = "reject"


@dataclass(frozen=True, slots=True)
class SemanticResolutionReview:
    """Declared human review, with separate provenance and no runtime clock key."""

    proposal_id: str
    reviewer: str
    provenance: TaskProvenance
    decision: ReviewDecision
    reason: str

    def __post_init__(self) -> None:
        """Require an explicit reviewer, source and decision; authenticate no person."""
        require_text(self.proposal_id, self.reviewer, self.reason)
        if not isinstance(self.decision, ReviewDecision) or not isinstance(
            self.provenance, TaskProvenance
        ):
            msg = "Malformed human review provenance or decision."
            raise TypeError(msg)
        if not isinstance(self.provenance.source_identity, str):
            msg = "Human review needs an explicit source artifact identity."
            raise TypeError(msg)
        require_text(self.provenance.source_identity)

    @property
    def identity(self) -> str:
        """Keep human review independent of proposal producer identity."""
        return digest(self)


def _resolution_reason(proposal: SemanticResolutionProposal) -> str:
    reason = proposal.reason
    if proposal.argument is not None:
        reason += (
            f"\nObservation: {proposal.argument.observation}"
            f"\nCriterion: {proposal.argument.criterion_link}"
        )
    return reason


def materialize_accepted_resolution(
    request: SemanticDecisionRequest,
    proposal: SemanticResolutionProposal,
    review: SemanticResolutionReview | None,
    candidates: CandidateWitnessView,
) -> CandidateMemberResolution:
    """Explicitly record an ACCEPT-reviewed proposal; promote or mutate nothing."""
    if request is not proposal.request or candidates is not request.candidates:
        msg = (
            "Materialization requires the exact request and current candidate context."
        )
        raise ValueError(msg)
    if (
        review is None
        or review.proposal_id != proposal.identity
        or review.decision is not ReviewDecision.ACCEPT
    ):
        msg = "Materialization requires an explicit ACCEPT review of this proposal."
        raise ValueError(msg)
    WitnessResolutionView(candidates)
    return CandidateMemberResolution(
        candidates,
        request.hypothesis,
        request.member,
        proposal.disposition,
        request.criterion,
        request.claim.statement,
        _resolution_reason(proposal),
        (
            f"{request.policy.name}@{request.policy.version}; "
            f"human reviewer {review.reviewer}"
        ),
        TaskProvenance(
            (SCHEMA, request.identity, proposal.identity, review.identity),
            explanation=(
                f"External decision artifact; producer "
                f"{proposal.producer.kind.value}: {proposal.producer.identity}; "
                f"review: {review.reason}"
            ),
        ),
        tuple(
            LocalizationEvidenceReference(
                reference.support,
                candidates.snapshot.repository_id,
                candidates.snapshot.id,
            )
            for reference in proposal.support_references
        ),
    )


@dataclass(frozen=True, slots=True)
class SemanticDecisionLedger:
    """Report one proposal/review per request, keeping unprocessed work absent."""

    batch: SemanticDecisionBatch
    proposals: tuple[SemanticResolutionProposal, ...] = ()
    reviews: tuple[SemanticResolutionReview, ...] = ()

    def __post_init__(self) -> None:
        """Reject duplicate proposals/reviews and foreign request or output lineage."""
        if any(
            not any(p.request is r for r in self.batch.requests) for p in self.proposals
        ):
            msg = "Ledger proposal belongs to a foreign request."
            raise ValueError(msg)
        if len({p.request.identity for p in self.proposals}) != len(self.proposals):
            msg = "Ledger repeats a proposal or request decision."
            raise ValueError(msg)
        known = {p.identity for p in self.proposals}
        if any(r.proposal_id not in known for r in self.reviews):
            msg = "Ledger review belongs to a foreign proposal."
            raise ValueError(msg)
        if len({r.proposal_id for r in self.reviews}) != len(self.reviews):
            msg = "Ledger repeats a human review."
            raise ValueError(msg)
        object.__setattr__(
            self, "proposals", tuple(sorted(self.proposals, key=lambda p: p.identity))
        )
        object.__setattr__(
            self, "reviews", tuple(sorted(self.reviews, key=lambda r: r.identity))
        )

    @property
    def identity(self) -> str:
        """Bind reporting state without inferring any materialized decisions."""
        return digest(
            (
                self.batch.identity,
                tuple(p.identity for p in self.proposals),
                tuple(r.identity for r in self.reviews),
            )
        )

    @property
    def unprocessed(self) -> tuple[SemanticDecisionRequest, ...]:
        """Preserve absence without synthesizing unresolved/abstained proposals."""
        processed = {p.request.identity for p in self.proposals}
        return tuple(r for r in self.batch.requests if r.identity not in processed)

    def report(
        self, materialized: tuple[CandidateMemberResolution, ...] = ()
    ) -> dict[str, object]:
        """Report costs and independently supplied materializations; perform none."""
        decisions = {r.proposal_id: r.decision for r in self.reviews}
        accepted = {
            p.identity: p
            for p in self.proposals
            if decisions.get(p.identity) is ReviewDecision.ACCEPT
        }
        for record in materialized:
            source = record.provenance.source_identity
            if (
                not isinstance(source, tuple)
                or len(source) != len((SCHEMA, "request", "proposal", "review"))
                or source[2] not in accepted
                or record.candidates is not self.batch.candidates
            ):
                msg = "Reporting received a foreign/unreviewed materialization."
                raise ValueError(msg)
            proposal = accepted[source[2]]
            review = next(r for r in self.reviews if r.proposal_id == proposal.identity)
            if (
                source
                != (
                    SCHEMA,
                    proposal.request.identity,
                    proposal.identity,
                    review.identity,
                )
                or record.hypothesis is not proposal.request.hypothesis
                or record.member is not proposal.request.member
                or record.disposition is not proposal.disposition
                or record.claim != proposal.request.claim.statement
                or record.criterion != proposal.request.criterion
                or record.reason != _resolution_reason(proposal)
                or len(record.basis) != len(proposal.support_references)
                or not all(
                    any(b.identity is s.support for b in record.basis)
                    for s in proposal.support_references
                )
            ):
                msg = "Reported materialization differs from its reviewed proposal."
                raise ValueError(msg)
        if len({r.provenance.source_identity for r in materialized}) != len(
            materialized
        ):
            msg = "Reporting repeats a materialization."
            raise ValueError(msg)
        materialized = tuple(
            sorted(materialized, key=lambda r: digest(r.provenance.source_identity))
        )
        return {
            "requests": len(self.batch.requests),
            "proposals": len(self.proposals),
            "unprocessed": len(self.unprocessed),
            "accepted": len(accepted),
            "rejected": sum(r.decision is ReviewDecision.REJECT for r in self.reviews),
            "unreviewed": sum(p.identity not in decisions for p in self.proposals),
            "proposed_dispositions": [p.disposition.value for p in self.proposals],
            "materialized_dispositions": [r.disposition.value for r in materialized],
            "disclosed_utf8_bytes": self.batch.disclosed_utf8_bytes,
            "candidate_frame_digest": self.batch.requests[0].candidate_frame_digest,
            "request_ids": [r.identity for r in self.batch.requests],
            "members": [
                {
                    "hypothesis": r.hypothesis.identity.value,
                    "obligation": r.claim.obligation.value,
                    "resource": r.member.target.address.value,
                    "content_cost": r.content_cost,
                }
                for r in self.batch.requests
            ],
        }
