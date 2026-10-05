# Copyright (c) 2026
# ruff: noqa: COM812
"""Frozen member inputs and semantic proposals, without execution or acceptance."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import TYPE_CHECKING

from devtools.context.localization.identity import (
    LocalizationObligationIdentity,
    LocalizationTaskIdentity,
    TaskProvenance,
)
from devtools.context.localization.resolution import (
    MemberResolutionDisposition,
    WitnessResolutionView,
)
from experiments.codex_dogfood.semantic_resolution._identity import digest, require_text

if TYPE_CHECKING:
    from devtools.context.localization.association import (
        CandidateWitnessHypothesis,
        CandidateWitnessMember,
        CandidateWitnessView,
    )
    from devtools.context.localization.association.hypothesis import (
        CandidateHypothesisIdentity,
    )
    from devtools.context.localization.obligation import SatisfactionCriterion
    from devtools.context.repository.resource import RepositoryResourceOccurrence
    from experiments.codex_dogfood.semantic_resolution.citations import (
        ContentBounds,
        ContentCitation,
        FrozenContentSlice,
    )

SCHEMA = "semantic-resolution-v1"
_SHA256_LENGTH = 64


@dataclass(frozen=True, slots=True)
class SemanticPolicyIdentity:
    """Freeze policy and disclosure definitions without a model registry."""

    name: str
    version: str
    disclosure_name: str
    disclosure_version: str
    instruction_digest: str
    schema_version: str = SCHEMA

    def __post_init__(self) -> None:
        """Require explicit definition identity and supported schema version."""
        require_text(
            self.name, self.version, self.disclosure_name, self.disclosure_version
        )
        if (
            self.schema_version != SCHEMA
            or len(self.instruction_digest) != _SHA256_LENGTH
            or any(c not in "0123456789abcdef" for c in self.instruction_digest)
        ):
            msg = "Invalid policy schema or instruction digest."
            raise ValueError(msg)

    @property
    def identity(self) -> str:
        """Fingerprint exact policy definition, not runtime execution."""
        return digest(self)


@dataclass(frozen=True, slots=True)
class SemanticMemberClaim:
    """Caller-owned task-local prose; not a universal executable claim ontology."""

    key: str
    task: LocalizationTaskIdentity
    obligation: LocalizationObligationIdentity
    hypothesis: CandidateHypothesisIdentity
    target: RepositoryResourceOccurrence
    statement: str
    reason: str
    provenance: TaskProvenance

    def __post_init__(self) -> None:
        """Keep caller scope coherent; request admission checks exact membership."""
        require_text(self.key, self.statement, self.reason)
        if (
            self.obligation.task != self.task
            or self.hypothesis.obligation != self.obligation
        ):
            msg = "Member claim has a foreign task or obligation."
            raise ValueError(msg)

    @property
    def identity(self) -> str:
        """Retain text, scope and caller provenance in the claim key."""
        return digest(self)


@dataclass(frozen=True, slots=True)
class NativeSupportReference:
    """Request-local handle to an exact attached support, never a vote."""

    request_id: str
    key: str
    channel: str
    support: object


@dataclass(frozen=True, slots=True)
class SemanticDecisionRequest:
    """One exact member, explicit claim/criterion and caller-selected content."""

    policy: SemanticPolicyIdentity
    candidates: CandidateWitnessView
    hypothesis: CandidateWitnessHypothesis
    member: CandidateWitnessMember
    claim: SemanticMemberClaim
    bounds: ContentBounds
    disclosures: tuple[FrozenContentSlice, ...]
    _frame: str = field(init=False, repr=False, compare=False)
    _key: str = field(init=False, repr=False, compare=False)
    _supports: tuple[NativeSupportReference, ...] = field(
        init=False, repr=False, compare=False
    )

    def __post_init__(self) -> None:
        """Revalidate native frames and reject undisclosed/oversized content."""
        WitnessResolutionView(self.candidates)
        if not any(h is self.hypothesis for h in self.candidates.hypotheses):
            msg = "Decision hypothesis is foreign or stale."
            raise ValueError(msg)
        if not any(m is self.member for m in self.hypothesis.members):
            msg = "Decision member is foreign or stale."
            raise ValueError(msg)
        if (
            self.claim.task != self.candidates.task.identity
            or self.claim.hypothesis != self.hypothesis.identity
            or self.claim.target is not self.member.target
        ):
            msg = "Decision claim differs from the exact candidate/member frame."
            raise ValueError(msg)
        if any(s.resource is not self.member.target for s in self.disclosures):
            msg = "V1 disclosures must use the exact member target resource."
            raise ValueError(msg)
        if len({s.identity for s in self.disclosures}) != len(self.disclosures):
            msg = "Decision repeats a disclosure."
            raise ValueError(msg)
        object.__setattr__(
            self,
            "disclosures",
            tuple(
                sorted(
                    self.disclosures,
                    key=lambda s: (s.start, s.end, s.identity),
                )
            ),
        )
        resources, excerpts, size = self.content_cost
        if (
            resources > self.bounds.max_resources
            or excerpts > self.bounds.max_excerpts
            or size > self.bounds.max_utf8_bytes
        ):
            msg = (
                "Decision disclosure exceeds declared bounds; no truncation permitted."
            )
            raise ValueError(msg)
        object.__setattr__(self, "_frame", digest(self.candidates))
        object.__setattr__(
            self,
            "_key",
            digest(
                (
                    SCHEMA,
                    self.policy.identity,
                    self._frame,
                    self.hypothesis.identity,
                    self.member.target,
                    self.claim.identity,
                    self.criterion,
                    self.bounds,
                    tuple(s.identity for s in self.disclosures),
                )
            ),
        )
        object.__setattr__(
            self,
            "_supports",
            tuple(
                NativeSupportReference(
                    self.identity,
                    digest((self.identity, channel, support)),
                    channel,
                    support,
                )
                for channel in ("lexical", "roles", "routed", "structural")
                for support in getattr(self.member, channel)
            ),
        )

    @property
    def criterion(self) -> SatisfactionCriterion:
        """Use the exact obligation value; never interpret its name as a rule."""
        return next(
            o.satisfaction
            for o in self.candidates.task.obligations
            if o.identity == self.hypothesis.identity.obligation
        )

    @property
    def candidate_frame_digest(self) -> str:
        """Bind the entire native association frame without disclosing its content."""
        return self._frame

    @property
    def identity(self) -> str:
        """Canonical request identity independent of incoming disclosure order."""
        return self._key

    @property
    def content_cost(self) -> tuple[int, int, int]:
        """Return resources, excerpts and summed UTF-8 disclosed bytes."""
        return (
            int(bool(self.disclosures)),
            len(self.disclosures),
            sum(s.utf8_bytes for s in self.disclosures),
        )

    @property
    def supports(self) -> tuple[NativeSupportReference, ...]:
        """Expose every attached support independently with request-bound handles."""
        return self._supports

    def validate_support(self, reference: NativeSupportReference) -> None:
        """Reject copied, foreign or forged support handles even for equal values."""
        if not any(
            reference.request_id == native.request_id
            and reference.key == native.key
            and reference.channel == native.channel
            and reference.support is native.support
            for native in self.supports
        ):
            msg = "Proposal support is not exact attached request evidence."
            raise ValueError(msg)

    def validate_citation(self, citation: ContentCitation) -> None:
        """Require a disclosed slice and request, not repository-wide browsing."""
        if (
            citation.request_id != self.identity
            or citation.content.resource is not self.member.target
            or citation.content not in self.disclosures
        ):
            msg = "Proposal citation is foreign or not disclosed to this request."
            raise ValueError(msg)


class ProducerKind(StrEnum):
    """Describe provenance, without implementing any producer capability."""

    HUMAN = "human"
    EXTERNAL_MODEL = "external-model"
    OTHER = "other-explicit-resolver"


@dataclass(frozen=True, slots=True)
class ProducerProvenance:
    """Separate producer identity/configuration from human review."""

    kind: ProducerKind
    identity: str
    source: TaskProvenance
    input_request_digest: str
    model: str | None = None
    provider: str | None = None
    runtime: str | None = None
    configuration: str | None = None

    def __post_init__(self) -> None:
        """Require complete model metadata only when a future model is declared."""
        require_text(self.identity, self.input_request_digest)
        if (
            not isinstance(self.kind, ProducerKind)
            or not isinstance(self.source, TaskProvenance)
            or not isinstance(self.source.source_identity, str)
            or self.source.span is not None
        ):
            msg = "Malformed producer provenance."
            raise ValueError(msg)
        require_text(self.source.source_identity)
        metadata = (self.model, self.provider, self.runtime, self.configuration)
        if self.kind is ProducerKind.EXTERNAL_MODEL:
            if any(not isinstance(v, str) or not v.strip() for v in metadata):
                msg = "Model provenance needs model/provider/runtime/configuration."
                raise ValueError(msg)
        elif any(v is not None for v in metadata):
            msg = "Non-model producer cannot carry model provenance."
            raise ValueError(msg)


class AbstentionReason(StrEnum):
    """Distinguish declining adjudication from inspected-but-unestablished evidence."""

    UNSUPPORTED_CRITERION = "unsupported-criterion"
    INSUFFICIENT_CONTENT = "insufficient-bounded-content"
    MISSING_OBSERVATION = "missing-observation"
    CAPABILITY_LIMIT = "policy-capability-limit"
    AMBIGUOUS_SEMANTICS = "ambiguous-semantics"


@dataclass(frozen=True, slots=True)
class SemanticArgument:
    """Require a content observation and criterion link, not relevance alone."""

    observation: str
    criterion_link: str

    def __post_init__(self) -> None:
        """Validate argument structure; human review owns semantic adequacy."""
        require_text(self.observation, self.criterion_link)


@dataclass(frozen=True, slots=True)
class SemanticResolutionProposal:
    """An auditable proposal, never an accepted kernel resolution."""

    request: SemanticDecisionRequest
    disposition: MemberResolutionDisposition
    reason: str
    producer: ProducerProvenance
    citations: tuple[ContentCitation, ...] = ()
    support_references: tuple[NativeSupportReference, ...] = ()
    argument: SemanticArgument | None = None
    abstention: AbstentionReason | None = None

    def __post_init__(self) -> None:
        """Validate evidence lineage and pilot disposition/argument constraints."""
        require_text(self.reason)
        if (
            not isinstance(self.disposition, MemberResolutionDisposition)
            or self.disposition is MemberResolutionDisposition.CONTRADICTED
        ):
            msg = "Pilot proposals exclude contradiction and unknown dispositions."
            raise ValueError(msg)
        if self.producer.input_request_digest != self.request.identity:
            msg = "Producer input digest differs from decision request."
            raise ValueError(msg)
        for citation in self.citations:
            self.request.validate_citation(citation)
        for support in self.support_references:
            self.request.validate_support(support)
        if len({c.identity for c in self.citations}) != len(self.citations) or len(
            {s.key for s in self.support_references}
        ) != len(self.support_references):
            msg = "Proposal repeats citations or native supports."
            raise ValueError(msg)
        if self.disposition is MemberResolutionDisposition.SUPPORTED and not (
            self.citations
            and self.support_references
            and isinstance(self.argument, SemanticArgument)
        ):
            msg = "Support needs citations, native basis and structured argument."
            raise ValueError(msg)
        if self.disposition is MemberResolutionDisposition.ABSTAINED:
            if not isinstance(self.abstention, AbstentionReason):
                msg = "Abstained proposal needs an explicit capability reason."
                raise ValueError(msg)
        elif self.abstention is not None:
            msg = "Only abstained proposals carry an abstention category."
            raise ValueError(msg)
        object.__setattr__(
            self, "citations", tuple(sorted(self.citations, key=lambda c: c.identity))
        )
        object.__setattr__(
            self,
            "support_references",
            tuple(sorted(self.support_references, key=lambda s: s.key)),
        )

    @property
    def identity(self) -> str:
        """Fingerprint output with its exact request and producer lineage."""
        return digest(
            (
                self.request.identity,
                self.disposition,
                self.reason,
                self.producer,
                tuple(c.identity for c in self.citations),
                tuple(s.key for s in self.support_references),
                self.argument,
                self.abstention,
            )
        )


@dataclass(frozen=True, slots=True)
class SemanticDecisionBatch:
    """Freeze inclusion before proposals; no automatic association or execution."""

    policy: SemanticPolicyIdentity
    candidates: CandidateWitnessView
    requests: tuple[SemanticDecisionRequest, ...]
    inclusion_reason: str
    provenance: TaskProvenance

    def __post_init__(self) -> None:
        """Require one frozen request per included member in an exact native frame."""
        require_text(self.inclusion_reason)
        if not self.requests or any(
            r.candidates is not self.candidates or r.policy != self.policy
            for r in self.requests
        ):
            msg = "Batch needs requests in one exact candidate/policy frame."
            raise ValueError(msg)
        members = {(r.hypothesis.identity, r.member.target) for r in self.requests}
        if len(members) != len(self.requests):
            msg = "Batch repeats a candidate member."
            raise ValueError(msg)
        object.__setattr__(
            self, "requests", tuple(sorted(self.requests, key=lambda r: r.identity))
        )

    @property
    def identity(self) -> str:
        """Freeze population, inclusion metadata and policy without any verdict."""
        return digest(
            (
                self.policy.identity,
                digest(self.candidates),
                tuple(r.identity for r in self.requests),
                self.inclusion_reason,
                self.provenance,
            )
        )

    @property
    def disclosed_utf8_bytes(self) -> int:
        """Sum request disclosure occurrences, not deduplicated or token estimates."""
        return sum(r.content_cost[2] for r in self.requests)
