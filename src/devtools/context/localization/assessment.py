# Copyright (c) 2026
"""Snapshot-bound evidence references and caller-supplied obligation dispositions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Hashable

    from devtools.context.localization.identity import LocalizationObligationIdentity
    from devtools.context.repository.identity import RepositoryId
    from devtools.context.repository.snapshot import RepositorySnapshotId


class ApplicabilityStatus(StrEnum):
    """Record conditional applicability separately from requirement priority."""

    NOT_REQUIRED = "not-required"
    UNASSESSED = "unassessed"
    APPLIES = "applies"
    DOES_NOT_APPLY = "does-not-apply"


class Disposition(StrEnum):
    """State an obligation assessment without turning abstention into satisfaction."""

    OPEN = "open"
    RESOLVED = "resolved"
    NOT_APPLICABLE = "not-applicable"
    DEFERRED_DISCOVERY = "deferred-discovery"
    ABSTAINED = "abstained"


@dataclass(frozen=True, slots=True)
class LocalizationEvidenceReference:
    """Reference a caller-owned evidence item qualified by repository snapshot."""

    identity: Hashable
    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId

    def __post_init__(self) -> None:
        """Reject evidence references without stable hashable identity."""
        _require_hashable(self.identity, label="Evidence")


@dataclass(frozen=True, slots=True)
class SupportedWitness:
    """Associate one native/caller target identity with snapshot-qualified supports."""

    target: Hashable
    evidence: tuple[LocalizationEvidenceReference, ...]

    def __post_init__(self) -> None:
        """Require positive provenance for a witness presented as supported."""
        _require_hashable(self.target, label="Witness target")
        if not self.evidence:
            msg = "Supported witness needs at least one evidence reference."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class DeferredDiscovery:
    """Name a later observation and caller acceptance of conditional handoff."""

    observation: str
    reason: str
    accepted_for_handoff: bool = False

    def __post_init__(self) -> None:
        """Require a named observation and why it cannot yet be performed."""
        if not self.observation.strip() or not self.reason.strip():
            msg = "Deferred discovery needs an observation and reason."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class LocalizationAssessment:
    """Supply one obligation disposition and its exact evidence frame."""

    obligation: LocalizationObligationIdentity
    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    disposition: Disposition
    applicability: ApplicabilityStatus = ApplicabilityStatus.NOT_REQUIRED
    applicability_evidence: tuple[LocalizationEvidenceReference, ...] = ()
    supported_witnesses: tuple[SupportedWitness, ...] = ()
    deferred: DeferredDiscovery | None = None
    explanation: str | None = None

    def __post_init__(self) -> None:
        """Check structure; the frame is validated during readiness assessment."""
        targets = tuple(item.target for item in self.supported_witnesses)
        # SupportedWitness owns target hashability, so no duplicate validation
        # path is needed here to catch an unhashable target.
        unique = set(targets)
        if len(unique) != len(targets):
            msg = "Assessment must aggregate evidence per distinct witness target."
            raise ValueError(msg)
        if self.explanation is not None and not self.explanation.strip():
            msg = "Assessment explanation must not be blank when supplied."
            raise ValueError(msg)
        if self.disposition is Disposition.DEFERRED_DISCOVERY and self.deferred is None:
            msg = "Deferred disposition must name its later observation."
            raise ValueError(msg)
        if (
            self.disposition is not Disposition.DEFERRED_DISCOVERY
            and self.deferred is not None
        ):
            msg = "Only a deferred disposition may carry a deferred observation."
            raise ValueError(msg)


def _require_hashable(value: Hashable, *, label: str) -> None:
    """Validate a caller-owned identity without wrapping its domain semantics."""
    try:
        hash(value)
    except TypeError as error:
        msg = f"{label} identity must be hashable."
        raise ValueError(msg) from error
