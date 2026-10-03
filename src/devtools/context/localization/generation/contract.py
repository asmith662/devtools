# Copyright (c) 2026
"""Explicit single-target projections and caller-authored hypothesis shape."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.context.localization.association import (
        CandidateWitnessHypothesis,
        CandidateWitnessView,
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
class WitnessGenerationRecipe:
    """Caller-authored all-member candidate explanation for one obligation."""

    identity: WitnessHypothesisIdentity
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
                        item.identity.value,
                    ),
                ),
            ),
        )


@dataclass(frozen=True, slots=True)
class MemberProjectionAttempt:
    """Audit one exact projection, including bounded failure and native support."""

    recipe: GroundedMemberRecipe
    disposition: GenerationDisposition
    source: NativeGroundingReferent | None
    targets: tuple[RepositoryResourceOccurrence, ...]
    structural: tuple[StructuralMemberSupport, ...]
    examined_resources: int
    mirror_analysis: PythonMirroredPathAnalysis | None = None
    result_limit: int = 1
    truncated: bool = False
    uncovered_frontier: tuple[RepositoryResourceOccurrence, ...] = ()

    @property
    def result_count(self) -> int:
        """Count exact native targets, without treating the count as a score."""
        return len(self.targets)


@dataclass(frozen=True, slots=True)
class HypothesisGenerationAttempt:
    """Keep all complementary member outcomes even when no hypothesis forms."""

    recipe: WitnessGenerationRecipe
    disposition: GenerationDisposition
    members: tuple[MemberProjectionAttempt, ...]
    hypothesis: CandidateWitnessHypothesis | None


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
