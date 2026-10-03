# Copyright (c) 2026
"""Caller preferences and lossless routed views over native lexical lanes."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

from devtools.context.localization.roles.models import RepositoryRoleKind

if TYPE_CHECKING:
    from devtools.context.localization.identity import (
        LocalizationObligationIdentity,
        LocalizationQueryIdentity,
    )
    from devtools.context.localization.lexical import (
        LocalizationLexicalAcquisition,
        ObligationLexicalEvidence,
    )
    from devtools.context.localization.roles.models import (
        ResourceRoleEvidence,
    )
    from devtools.context.retrieval.lexical.bm25 import (
        RepositoryTextLexicalBm25Match,
    )


class RoutingTier(Enum):
    """Name the two attention tiers without implying relevance or satisfaction."""

    PREFERRED_ROLE_SUPPORTED = "preferred-role-supported"
    ESCAPE = "escape"


@dataclass(frozen=True, slots=True)
class ObligationRolePreference:
    """Caller-authored preferred roles for one explicit query lane."""

    query: LocalizationQueryIdentity
    obligation: LocalizationObligationIdentity
    preferred_roles: tuple[RepositoryRoleKind, ...]

    def __post_init__(self) -> None:
        """Keep lane identity scoped and roles within the supported vocabulary."""
        if self.query.task != self.obligation.task:
            msg = "Routing preference query and obligation must share task scope."
            raise ValueError(msg)
        if any(
            not isinstance(role, RepositoryRoleKind) for role in self.preferred_roles
        ):
            msg = "Routing preference contains an unsupported repository role."
            raise ValueError(msg)
        if len(set(self.preferred_roles)) != len(self.preferred_roles):
            msg = "Routing preference repeats a preferred role."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class RoutedLexicalCandidate:
    """Reference a native match and its role explanation at a routed position."""

    native_rank: int
    routed_position: int
    tier: RoutingTier
    match: RepositoryTextLexicalBm25Match
    role_evidence: tuple[ResourceRoleEvidence, ...]


@dataclass(frozen=True, slots=True)
class RoutedObligationLane:
    """Project one native lane into preferred and complete escape tiers."""

    native_lane: ObligationLexicalEvidence
    preference: ObligationRolePreference
    preferred: tuple[RoutedLexicalCandidate, ...]
    escape: tuple[RoutedLexicalCandidate, ...]

    @property
    def candidates(self) -> tuple[RoutedLexicalCandidate, ...]:
        """Present preferred candidates followed by every escape candidate."""
        return self.preferred + self.escape


@dataclass(frozen=True, slots=True)
class LocalizationRoleRoutingView:
    """Add caller-directed lane views while retaining the complete acquisition."""

    acquisition: LocalizationLexicalAcquisition
    global_retrieval: RepositoryTextLexicalBm25RetrievalResult
    role_evidence: RepositoryRoleEvidenceView
    obligation_lanes: tuple[RoutedObligationLane, ...]


if TYPE_CHECKING:
    from devtools.context.localization.roles.models import RepositoryRoleEvidenceView
    from devtools.context.retrieval.lexical.bm25 import (
        RepositoryTextLexicalBm25RetrievalResult,
    )
