# Copyright (c) 2026
"""Caller-authored fixed and bounded branching candidate families."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

from devtools.context.localization.association import WitnessHypothesisFamilyIdentity
from devtools.context.localization.association.structural import structural_support_key

if TYPE_CHECKING:
    from devtools.context.localization.association import (
        CandidateWitnessHypothesis,
        CandidateWitnessView,
        GeneratedWitnessHypothesisIdentity,
        WitnessHypothesisIdentity,
    )
    from devtools.context.localization.association.structural import (
        StructuralMemberSupport,
    )
    from devtools.context.localization.grounding import AnchorGrounding
    from devtools.context.localization.grounding.contract import NativeGroundingReferent
    from devtools.context.localization.identity import (
        LocalizationAnchorIdentity,
        LocalizationObligationIdentity,
        TaskProvenance,
    )
    from devtools.context.localization.lexical import LocalizationLexicalAcquisition
    from devtools.context.localization.roles.models import RepositoryRoleEvidenceView
    from devtools.context.localization.routing.models import LocalizationRoleRoutingView
    from devtools.context.localization.task import LocalizationTaskInterpretation
    from devtools.context.python.mirrored_paths import PythonMirroredPathAnalysis
    from devtools.context.repository.resource import RepositoryResourceOccurrence
    from devtools.context.repository.snapshot import RepositorySnapshot


class ProjectionKind(Enum):
    """The two exact, single-target native projection policies in v1."""

    OWNER_RESOURCE = "owner-resource"
    MIRRORED_RESOURCE = "mirrored-resource"


class GenerationDisposition(Enum):
    """Report bounded recipe results without judging witness satisfaction."""

    GENERATED = "generated"
    NO_TARGET = "no-target"
    AMBIGUOUS_SOURCE = "ambiguous-source"
    UNRESOLVED_SOURCE = "unresolved-source"
    UNSUPPORTED_SOURCE = "unsupported-source"
    MULTI_TARGET = "multi-target"
    DUPLICATE_TARGET = "duplicate-target"
    GENERATED_WITH_BRANCH_FAILURES = "generated-with-branch-failures"
    FIXED_MEMBER_FAILED = "fixed-member-failed"
    WORK_BOUND_EXCEEDED = "work-bound-exceeded"
    RESULT_BOUND_EXCEEDED = "result-bound-exceeded"
    INVALID_BRANCH = "invalid-branch"
    INVALID_MEMBER = "invalid-member"
    ABSTAINED = "abstained"


@dataclass(frozen=True, slots=True)
class GroundedMemberRecipe:
    """Caller-select one grounded anchor, projection and interpretation reason."""

    key: str
    grounding: AnchorGrounding
    projection: ProjectionKind
    reason: str
    provenance: TaskProvenance

    def __post_init__(self) -> None:
        """Require explicit intent, not inferred operator or empty rationale."""
        if not self.key.strip() or not self.reason.strip():
            msg = "Grounded member recipe needs a key and interpretation reason."
            raise ValueError(msg)
        if not isinstance(self.projection, ProjectionKind):
            msg = "Grounded member recipe has an unsupported projection."
            raise TypeError(msg)


@dataclass(frozen=True, slots=True)
class BranchingGroundedMemberRecipe(GroundedMemberRecipe):
    """Authorize substitution of one exact target per child, within a hard bound."""

    max_results: int

    def __post_init__(self) -> None:
        """Require positive explicit result admission, separate from native work."""
        GroundedMemberRecipe.__post_init__(self)
        if self.max_results < 1:
            msg = "Branching member needs a positive result bound."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class WitnessGenerationRecipe:
    """Caller-authored all-member candidate explanation for one obligation."""

    identity: WitnessHypothesisIdentity | WitnessHypothesisFamilyIdentity
    members: tuple[GroundedMemberRecipe, ...]
    provenance: TaskProvenance

    def __post_init__(self) -> None:
        """Preserve distinct conjuncts; several recipes compete by identity."""
        if not self.members:
            msg = "Witness generation recipe needs at least one member."
            raise ValueError(msg)
        if len({item.key for item in self.members}) != len(self.members):
            msg = "Witness generation recipe repeats a member key."
            raise ValueError(msg)
        branching = tuple(
            item
            for item in self.members
            if isinstance(item, BranchingGroundedMemberRecipe)
        )
        if len(branching) > 1:
            msg = "A generation recipe permits at most one branching member."
            raise ValueError(msg)
        if bool(branching) != isinstance(
            self.identity,
            WitnessHypothesisFamilyIdentity,
        ):
            msg = "A branching recipe needs a family identity; fixed recipes do not."
            raise ValueError(msg)
        object.__setattr__(
            self,
            "members",
            tuple(sorted(self.members, key=lambda item: item.key)),
        )


@dataclass(frozen=True, slots=True)
class WitnessGenerationPlan:
    """Bind explicit recipes and optional native support views to one frame."""

    task: LocalizationTaskInterpretation
    snapshot: RepositorySnapshot
    recipes: tuple[WitnessGenerationRecipe, ...]
    acquisition: LocalizationLexicalAcquisition | None = None
    role_evidence: RepositoryRoleEvidenceView | None = None
    routing: LocalizationRoleRoutingView | None = None

    def __post_init__(self) -> None:
        """Reject duplicate alternatives before running any native projection."""
        if len({item.identity for item in self.recipes}) != len(self.recipes):
            msg = "Generation plan repeats a hypothesis recipe identity."
            raise ValueError(msg)
        order = {
            item.identity: index for index, item in enumerate(self.task.obligations)
        }
        object.__setattr__(
            self,
            "recipes",
            tuple(
                sorted(
                    self.recipes,
                    key=lambda item: (
                        order.get(item.identity.obligation, len(order)),
                        type(item.identity).__name__,
                        item.identity.value,
                    ),
                ),
            ),
        )


@dataclass(frozen=True, slots=True)
class ProjectedMemberTarget:
    """Keep one exact resource and only the native support establishing it."""

    target: RepositoryResourceOccurrence
    structural: tuple[StructuralMemberSupport, ...]

    def __post_init__(self) -> None:
        """Canonicalize native support without duplicate evidence votes."""
        supports = set(self.structural)
        if len({structural_support_key(item) for item in supports}) != len(supports):
            msg = "Projection structural support stable key collides."
            raise ValueError(msg)
        object.__setattr__(
            self,
            "structural",
            tuple(sorted(supports, key=structural_support_key)),
        )

    @property
    def stable_key(self) -> tuple[str, str]:
        """Use native addressed content identity, never relevance order."""
        return self.target.address.value, self.target.content_identity.value


@dataclass(frozen=True, slots=True)
class MemberProjectionAttempt:
    """Retain complete or incomplete native enumeration and independent work quota."""

    recipe: GroundedMemberRecipe
    disposition: GenerationDisposition
    source: NativeGroundingReferent | None
    projections: tuple[ProjectedMemberTarget, ...]
    work_performed: int
    mirror_analysis: PythonMirroredPathAnalysis | None = None
    complete: bool = True
    work_limit: int | None = None
    uncovered_frontier: tuple[RepositoryResourceOccurrence, ...] = ()
    failure_reason: str | None = None

    def __post_init__(self) -> None:
        """Group repeated exact targets and retain all their native support."""
        if self.work_performed < 0 or (
            self.work_limit is not None
            and (self.work_limit < 0 or self.work_performed > self.work_limit)
        ):
            msg = "Projection work must stay within its nonnegative work bound."
            raise ValueError(msg)
        if self.complete and self.uncovered_frontier:
            msg = "Complete projection cannot retain an uncovered frontier."
            raise ValueError(msg)
        grouped: dict[RepositoryResourceOccurrence, list[StructuralMemberSupport]] = {}
        for item in self.projections:
            grouped.setdefault(item.target, []).extend(item.structural)
        object.__setattr__(
            self,
            "projections",
            tuple(
                sorted(
                    (
                        ProjectedMemberTarget(target, tuple(support))
                        for target, support in grouped.items()
                    ),
                    key=lambda item: item.stable_key,
                ),
            ),
        )
        if len({item.stable_key for item in self.projections}) != len(self.projections):
            msg = "Projection target stable key collides."
            raise ValueError(msg)
        if self.disposition in (
            GenerationDisposition.GENERATED,
            GenerationDisposition.NO_TARGET,
            GenerationDisposition.MULTI_TARGET,
        ):
            object.__setattr__(
                self,
                "disposition",
                GenerationDisposition.NO_TARGET
                if not self.projections
                else GenerationDisposition.GENERATED
                if len(self.projections) == 1
                else GenerationDisposition.MULTI_TARGET,
            )
        object.__setattr__(
            self,
            "uncovered_frontier",
            tuple(
                sorted(
                    set(self.uncovered_frontier),
                    key=lambda item: (
                        item.address.value,
                        item.content_identity.value,
                    ),
                ),
            ),
        )

    @property
    def targets(self) -> tuple[RepositoryResourceOccurrence, ...]:
        """Expose the deterministic diagnostic surface, never an admitted prefix."""
        return tuple(item.target for item in self.projections)

    @property
    def structural(self) -> tuple[StructuralMemberSupport, ...]:
        """Expose all diagnostic support; children use target-specific projections."""
        return tuple(item for target in self.projections for item in target.structural)

    @property
    def examined_resources(self) -> int:
        """Retain resource work diagnostics of the existing owner/mirror operators."""
        return self.work_performed

    @property
    def result_limit(self) -> int:
        """Report the member's independent target admission bound."""
        return (
            self.recipe.max_results
            if isinstance(self.recipe, BranchingGroundedMemberRecipe)
            else 1
        )

    @property
    def truncated(self) -> bool:
        """Incomplete work cannot authorize any candidate prefix."""
        return not self.complete

    @property
    def result_count(self) -> int | None:
        """Report exact distinct target count only for complete enumeration."""
        return len(self.projections) if self.complete else None


@dataclass(frozen=True, slots=True)
class BranchGenerationAttempt:
    """Audit one fully enumerated target's candidate instantiation independently."""

    identity: GeneratedWitnessHypothesisIdentity
    projection: ProjectedMemberTarget
    disposition: GenerationDisposition
    hypothesis: CandidateWitnessHypothesis | None
    reason: str

    @property
    def stable_key(self) -> str:
        """Use exact child identity without execution order."""
        return self.identity.value


@dataclass(frozen=True, slots=True)
class HypothesisGenerationAttempt:
    """Keep one fixed recipe or family beside its zero or more child outcomes."""

    recipe: WitnessGenerationRecipe
    disposition: GenerationDisposition
    members: tuple[MemberProjectionAttempt, ...]
    hypothesis: CandidateWitnessHypothesis | None
    branches: tuple[BranchGenerationAttempt, ...] = ()

    @property
    def children(self) -> tuple[CandidateWitnessHypothesis, ...]:
        """Expose successful unresolved children, with fixed recipe compatibility."""
        if self.hypothesis is not None:
            return (self.hypothesis,)
        return tuple(
            item.hypothesis for item in self.branches if item.hypothesis is not None
        )

    @property
    def failed_branches(self) -> tuple[BranchGenerationAttempt, ...]:
        """Retain rejected complete combinations without hiding valid siblings."""
        return tuple(item for item in self.branches if item.hypothesis is None)


@dataclass(frozen=True, slots=True)
class WitnessGenerationView:
    """Retain attempted recipes beside the validated unresolved association view."""

    plan: WitnessGenerationPlan
    attempts: tuple[HypothesisGenerationAttempt, ...]
    association: CandidateWitnessView

    def for_obligation(
        self,
        obligation: LocalizationObligationIdentity,
    ) -> tuple[HypothesisGenerationAttempt, ...]:
        """Inspect every caller recipe attempted for one known obligation."""
        if obligation not in {item.identity for item in self.plan.task.obligations}:
            msg = "Generation view has no such obligation."
            raise ValueError(msg)
        return tuple(
            item
            for item in self.attempts
            if item.recipe.identity.obligation == obligation
        )

    def for_anchor(
        self,
        anchor: LocalizationAnchorIdentity,
    ) -> tuple[MemberProjectionAttempt, ...]:
        """Find all attempted projections using one known task anchor."""
        if anchor not in {item.identity for item in self.plan.task.anchors}:
            msg = "Generation view has no such anchor."
            raise ValueError(msg)
        return tuple(
            member
            for attempt in self.attempts
            for member in attempt.members
            if member.recipe.grounding.request.anchor == anchor
        )

    @property
    def generated(self) -> tuple[CandidateWitnessHypothesis, ...]:
        """Expose only unresolved hypotheses accepted by association validation."""
        return self.association.hypotheses

    @property
    def no_target(self) -> tuple[MemberProjectionAttempt, ...]:
        """Expose exact projection misses without claiming global irrelevance."""
        return tuple(
            member
            for attempt in self.attempts
            for member in attempt.members
            if member.disposition is GenerationDisposition.NO_TARGET
        )

    def for_target(
        self,
        target: RepositoryResourceOccurrence,
    ) -> tuple[CandidateWitnessHypothesis, ...]:
        """Inspect convergent generated hypotheses through the association view."""
        return self.association.for_target(target)

    @property
    def cross_obligation_targets(self) -> tuple[RepositoryResourceOccurrence, ...]:
        """Expose many-to-many participation, never global task relevance."""
        return self.association.cross_obligation_targets

    def for_family(
        self,
        identity: WitnessHypothesisFamilyIdentity,
    ) -> HypothesisGenerationAttempt:
        """Inspect an attempted family even when no child was admitted."""
        for item in self.attempts:
            if item.recipe.identity == identity:
                return item
        msg = "Generation view has no such family."
        raise ValueError(msg)

    def parent_family(
        self,
        identity: GeneratedWitnessHypothesisIdentity,
    ) -> HypothesisGenerationAttempt:
        """Find retained lineage for a successful or failed child identity."""
        family = self.for_family(identity.family)
        if not any(item.identity == identity for item in family.branches):
            msg = "Generation family has no such branch child."
            raise ValueError(msg)
        return family
