# Copyright (c) 2026
# ruff: noqa: COM812
"""Caller-supplied candidate explanations, distinct from accepted witnesses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context.retrieval.composition import require_lexical_result_snapshot

if TYPE_CHECKING:
    from devtools.context.localization.identity import (
        LocalizationObligationIdentity,
        LocalizationQueryIdentity,
    )
    from devtools.context.localization.lexical import LocalizationLexicalAcquisition
    from devtools.context.localization.roles.models import (
        RepositoryRoleEvidenceView,
        ResourceRoleEvidence,
    )
    from devtools.context.localization.routing.models import (
        LocalizationRoleRoutingView,
        RoutedLexicalCandidate,
    )
    from devtools.context.localization.task import LocalizationTaskInterpretation
    from devtools.context.repository.resource import RepositoryResourceOccurrence
    from devtools.context.repository.snapshot import RepositorySnapshot
    from devtools.context.retrieval.lexical.bm25 import RepositoryTextLexicalBm25Match


@dataclass(frozen=True, slots=True)
class WitnessHypothesisIdentity:
    """Caller-named alternative within one task obligation, not RI identity."""

    obligation: LocalizationObligationIdentity
    value: str

    def __post_init__(self) -> None:
        """Reject unnamed alternatives."""
        if not self.value.strip():
            msg = "Candidate witness hypothesis identity must not be blank."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class LexicalMatchSupport:
    """Reference an exact native match and its global or obligation query lane."""

    query: LocalizationQueryIdentity | None
    native_rank: int
    match: RepositoryTextLexicalBm25Match


@dataclass(frozen=True, slots=True)
class RoutedMatchSupport:
    """Retain presentation provenance without treating tier as satisfaction."""

    query: LocalizationQueryIdentity
    candidate: RoutedLexicalCandidate


@dataclass(frozen=True, slots=True)
class CandidateWitnessMember:
    """Hypothesize one observed resource with individually retained supports."""

    target: RepositoryResourceOccurrence
    reason: str
    lexical: tuple[LexicalMatchSupport, ...] = ()
    roles: tuple[ResourceRoleEvidence, ...] = ()
    routed: tuple[RoutedMatchSupport, ...] = ()

    def __post_init__(self) -> None:
        """Require a reason, support, and unambiguous support membership."""
        if not self.reason.strip() or not (self.lexical or self.roles or self.routed):
            msg = "Candidate member needs a reason and positive native support."
            raise ValueError(msg)
        if len({(item.query, item.native_rank) for item in self.lexical}) != len(
            self.lexical
        ) or len(
            {(item.query, item.candidate.routed_position) for item in self.routed}
        ) != len(self.routed):
            msg = "Candidate member repeats a native match support."
            raise ValueError(msg)
        if len({item.identity for item in self.roles}) != len(self.roles):
            msg = "Candidate member repeats role evidence."
            raise ValueError(msg)
        object.__setattr__(
            self,
            "lexical",
            tuple(
                sorted(
                    self.lexical,
                    key=lambda item: (
                        item.query is not None,
                        item.query.value if item.query is not None else "",
                        item.native_rank,
                    ),
                )
            ),
        )
        object.__setattr__(
            self,
            "roles",
            tuple(
                sorted(self.roles, key=lambda item: (item.role.value, item.identity))
            ),
        )
        object.__setattr__(
            self,
            "routed",
            tuple(
                sorted(
                    self.routed,
                    key=lambda item: (item.query.value, item.candidate.routed_position),
                )
            ),
        )


@dataclass(frozen=True, slots=True)
class CandidateWitnessHypothesis:
    """One unresolved all-member explanation competing with same-obligation peers."""

    identity: WitnessHypothesisIdentity
    members: tuple[CandidateWitnessMember, ...]

    def __post_init__(self) -> None:
        """Keep each hypothesized conjunct distinct."""
        if not self.members:
            msg = "Candidate witness hypothesis needs at least one member."
            raise ValueError(msg)
        addresses = tuple(item.target.address for item in self.members)
        if len(set(addresses)) != len(addresses):
            msg = "Candidate hypothesis repeats a resource target."
            raise ValueError(msg)
        object.__setattr__(
            self,
            "members",
            tuple(sorted(self.members, key=lambda item: item.target.address.value)),
        )


@dataclass(frozen=True, slots=True)
class CandidateWitnessView:
    """Keep native inputs beside ordered unresolved alternatives."""

    task: LocalizationTaskInterpretation
    snapshot: RepositorySnapshot
    hypotheses: tuple[CandidateWitnessHypothesis, ...]
    acquisition: LocalizationLexicalAcquisition | None
    role_evidence: RepositoryRoleEvidenceView | None
    routing: LocalizationRoleRoutingView | None

    def for_obligation(
        self, obligation: LocalizationObligationIdentity
    ) -> tuple[CandidateWitnessHypothesis, ...]:
        """Return competing alternatives without ranking or disposition."""
        if obligation not in {item.identity for item in self.task.obligations}:
            msg = "Candidate view has no such obligation."
            raise ValueError(msg)
        return tuple(
            item for item in self.hypotheses if item.identity.obligation == obligation
        )

    def for_target(
        self, target: RepositoryResourceOccurrence
    ) -> tuple[CandidateWitnessHypothesis, ...]:
        """Find all hypotheses sharing a native target across obligations."""
        if self.snapshot.resource_at(target.address) != target:
            msg = "Candidate target differs from the retained snapshot."
            raise ValueError(msg)
        return tuple(
            item
            for item in self.hypotheses
            if any(member.target == target for member in item.members)
        )

    @property
    def cross_obligation_targets(self) -> tuple[RepositoryResourceOccurrence, ...]:
        """Expose resources hypothesized for more than one obligation."""
        targets = {
            member.target.address: member.target
            for item in self.hypotheses
            for member in item.members
        }
        return tuple(
            targets[address]
            for address in sorted(targets, key=str)
            if len(
                {item.identity.obligation for item in self.for_target(targets[address])}
            )
            > 1
        )


def build_candidate_witness_view(  # noqa: C901, PLR0913
    *,
    task: LocalizationTaskInterpretation,
    snapshot: RepositorySnapshot,
    hypotheses: tuple[CandidateWitnessHypothesis, ...],
    acquisition: LocalizationLexicalAcquisition | None = None,
    role_evidence: RepositoryRoleEvidenceView | None = None,
    routing: LocalizationRoleRoutingView | None = None,
) -> CandidateWitnessView:
    """Validate caller hypotheses against supplied native frames; generate none."""
    if acquisition is not None:
        if (
            acquisition.task != task
            or acquisition.repository_id != snapshot.repository_id
            or acquisition.snapshot_id != snapshot.id
        ):
            msg = "Lexical acquisition differs from the association frame."
            raise ValueError(msg)
        require_lexical_result_snapshot(snapshot, acquisition.full_task_retrieval)
        for lane in acquisition.obligation_retrievals:
            require_lexical_result_snapshot(snapshot, lane.retrieval)
    if role_evidence is not None and (
        role_evidence.repository_id != snapshot.repository_id
        or role_evidence.snapshot_id != snapshot.id
        or role_evidence.resources != snapshot.resources
    ):
        msg = "Role evidence differs from the association frame."
        raise ValueError(msg)
    if routing is not None and (
        acquisition is None
        or role_evidence is None
        or routing.acquisition is not acquisition
        or routing.role_evidence is not role_evidence
        or routing.global_retrieval is not acquisition.full_task_retrieval
    ):
        msg = "Routing view differs from its native association inputs."
        raise ValueError(msg)
    known = {item.identity: position for position, item in enumerate(task.obligations)}
    seen: set[WitnessHypothesisIdentity] = set()
    for hypothesis in hypotheses:
        if hypothesis.identity.obligation not in known:
            msg = "Candidate hypothesis names an unknown obligation."
            raise ValueError(msg)
        if hypothesis.identity in seen:
            msg = "Candidate hypothesis identity is duplicated."
            raise ValueError(msg)
        seen.add(hypothesis.identity)
        for member in hypothesis.members:
            if snapshot.resource_at(member.target.address) != member.target:
                msg = "Candidate target differs from the association snapshot."
                raise ValueError(msg)
            _validate_supports(
                member,
                hypothesis.identity.obligation,
                acquisition,
                role_evidence,
                routing,
            )
    ordered = tuple(
        sorted(
            hypotheses,
            key=lambda item: (known[item.identity.obligation], item.identity.value),
        )
    )
    return CandidateWitnessView(
        task, snapshot, ordered, acquisition, role_evidence, routing
    )


def _validate_supports(
    member: CandidateWitnessMember,
    obligation: LocalizationObligationIdentity,
    acquisition: LocalizationLexicalAcquisition | None,
    role_evidence: RepositoryRoleEvidenceView | None,
    routing: LocalizationRoleRoutingView | None,
) -> None:
    for lexical_support in member.lexical:
        if acquisition is None:
            msg = "Lexical support requires its native acquisition."
            raise ValueError(msg)
        native_lanes = (
            (acquisition.full_task_retrieval,)
            if lexical_support.query is None
            else tuple(
                item.retrieval
                for item in acquisition.obligation_retrievals
                if item.request.identity == lexical_support.query
                and item.request.obligation == obligation
            )
        )
        if (
            len(native_lanes) != 1
            or not (1 <= lexical_support.native_rank <= len(native_lanes[0].matches))
            or native_lanes[0].matches[lexical_support.native_rank - 1]
            is not lexical_support.match
            or _match_target(lexical_support.match) != member.target
        ):
            msg = "Lexical support is foreign to its obligation, lane, rank, or target."
            raise ValueError(msg)
    for role_support in member.roles:
        if (
            role_evidence is None
            or role_support.repository_id != role_evidence.repository_id
            or role_support.snapshot_id != role_evidence.snapshot_id
            or role_support.derivation_identity != role_evidence.derivation_identity
            or role_support.resource != member.target
            or not any(item is role_support for item in role_evidence.evidence)
        ):
            msg = "Role support is stale or foreign to the association target."
            raise ValueError(msg)
    for routed_support in member.routed:
        if routing is None:
            msg = "Routed support requires its native routing view."
            raise ValueError(msg)
        routed_lanes = tuple(
            item
            for item in routing.obligation_lanes
            if item.preference.query == routed_support.query
            and item.preference.obligation == obligation
            and item.native_lane.request.identity == routed_support.query
        )
        if (
            len(routed_lanes) != 1
            or not any(
                item is routed_support.candidate for item in routed_lanes[0].candidates
            )
            or _match_target(routed_support.candidate.match) != member.target
        ):
            msg = "Routed support is foreign to its obligation, lane, or target."
            raise ValueError(msg)


def _match_target(
    match: RepositoryTextLexicalBm25Match,
) -> RepositoryResourceOccurrence:
    return match.document_statistics.analysis.document.resource
