# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003 -- formatter owns commas; bounded experiment validation
"""Immutable experimental task observations and native acquisition views."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

from devtools.context.localization.identity import LocalizationObligationIdentity

if TYPE_CHECKING:
    from devtools.context.localization.grounding.contract import (
        AnchorGrounding,
        PythonDirectDeclarationLocator,
        PythonModuleLocator,
        ResourceAddressLocator,
    )
    from devtools.context.localization.identity import (
        LocalizationTaskIdentity,
        TaskProvenance,
        TaskTextSpan,
    )
    from devtools.context.repository.identity import RepositoryId
    from devtools.context.repository.resource import RepositoryResourceOccurrence
    from devtools.context.repository.snapshot import RepositorySnapshotId
    from devtools.context.retrieval.lexical.bm25 import (
        RepositoryTextLexicalBm25Match,
        RepositoryTextLexicalBm25RetrievalResult,
    )


class HintCategory(StrEnum):
    """Tentative task syntax, never native repository truth."""

    RESOURCE_ADDRESS = "RESOURCE_ADDRESS"
    PYTHON_MODULE = "PYTHON_MODULE"
    PYTHON_DIRECT_FUNCTION = "PYTHON_DIRECT_FUNCTION"
    PYTHON_DIRECT_CLASS = "PYTHON_DIRECT_CLASS"
    PYTHON_DIRECT_METHOD = "PYTHON_DIRECT_METHOD"


class ResolutionDisposition(StrEnum):
    """Preserve native qualification without relevance or confidence."""

    RESOLVED = "RESOLVED"
    AMBIGUOUS = "AMBIGUOUS"
    UNRESOLVED = "UNRESOLVED"
    UNSUPPORTED = "UNSUPPORTED"


class GlobalTaskLane(StrEnum):
    """Name the optional global lane without inventing an obligation identity."""

    GLOBAL_TASK = "GLOBAL_TASK"


@dataclass(frozen=True, slots=True)
class ExactHintIdentity:
    """Deterministically identify one task-scoped syntax observation."""

    task: LocalizationTaskIdentity
    value: str


@dataclass(frozen=True, slots=True)
class ExactHintObservation:
    """Keep exact source, span, rule and task-only provenance."""

    task: LocalizationTaskIdentity
    text: str
    span: TaskTextSpan
    rule: str
    syntactic_form: str
    category: HintCategory
    provenance: TaskProvenance

    def __post_init__(self) -> None:
        """Reject observations without a complete source explanation."""
        if not self.text or self.span.end - self.span.start != len(self.text):
            raise ValueError("Hint text/span length differs")
        if not self.rule or not self.syntactic_form:
            raise ValueError("Hint rule/form missing")
        if self.provenance.span != self.span:
            raise ValueError("Hint provenance span differs")
        if self.provenance.source_identity != self.task.value or not isinstance(
            self.category, HintCategory
        ):
            raise ValueError("Hint task provenance or category differs")

    @property
    def identity(self) -> ExactHintIdentity:
        """Match caller and rule observations independently of author/rule name."""
        raw = f"{self.task.value}\0{self.span.start}\0{self.span.end}\0{self.text}"
        return ExactHintIdentity(self.task, hashlib.sha256(raw.encode()).hexdigest())


@dataclass(frozen=True, slots=True)
class ExtractionDecision:
    """Retain accepted observations and explicit rejected syntax boundaries."""

    span: TaskTextSpan
    text: str
    reason: str
    observation: ExactHintObservation | None


@dataclass(frozen=True, slots=True)
class HintAssociation:
    """Caller-authored task-only lane association, without satisfaction claims."""

    hint: ExactHintIdentity
    lane: LocalizationObligationIdentity | GlobalTaskLane
    reason: str
    provenance: TaskProvenance

    def __post_init__(self) -> None:
        """Bind obligation lanes to the original native task identity."""
        if not isinstance(self.lane, LocalizationObligationIdentity | GlobalTaskLane):
            raise TypeError("Unsupported lane type; use native obligation identity")
        if (
            not isinstance(self.lane, GlobalTaskLane)
            and self.lane.task != self.hint.task
        ):
            raise ValueError("Association obligation belongs to another task")
        if not self.reason.strip():
            raise ValueError("Association requires task-only reason")


@dataclass(frozen=True, slots=True)
class QualifiedMethodLocator:
    """Defer parent acquisition: explicit module/class/method, no inferred owner."""

    module: PythonModuleLocator
    class_name: str
    method_name: str


type HintLocator = (
    ResourceAddressLocator
    | PythonModuleLocator
    | PythonDirectDeclarationLocator
    | QualifiedMethodLocator
    | None
)


@dataclass(frozen=True, slots=True)
class ExactHintRouteRequest:
    """Frozen bounded association and typed locator admission."""

    hint: ExactHintObservation
    association: HintAssociation
    locator: HintLocator
    mechanism: str
    reason: str

    def __post_init__(self) -> None:
        """Require one matching task observation and justified lane."""
        if self.association.hint != self.hint.identity:
            raise ValueError("Route association names another hint")
        if not self.association.lane or not self.association.reason or not self.reason:
            raise ValueError("Route association/reason missing")

    @property
    def identity(self) -> str:
        """Task-local stable request identity independent of resolution results."""
        raw = (
            f"{self.hint.identity.value}\0{self.association.lane}\0"
            f"{self.mechanism}\0{self.locator!r}"
        )
        return hashlib.sha256(raw.encode()).hexdigest()


@dataclass(frozen=True, slots=True)
class ExactHintResolution:
    """Keep native grounding accounts and their explicit frozen frame."""

    request: ExactHintRouteRequest
    disposition: ResolutionDisposition
    resources: tuple[RepositoryResourceOccurrence, ...]
    native_provenance: tuple[AnchorGrounding, ...]
    reason: str
    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    frame_identity: str

    def __post_init__(self) -> None:
        """Do not publish unsupported promotion or unexplained results."""
        if not self.reason:
            raise ValueError("Resolution reason missing")
        if self.disposition is ResolutionDisposition.RESOLVED and (
            len(self.resources) != 1 or not self.native_provenance
        ):
            raise ValueError("Resolved route requires unique native support")
        if self.disposition is not ResolutionDisposition.RESOLVED and self.resources:
            raise ValueError("Non-resolved account cannot supply promoted resources")


@dataclass(frozen=True, slots=True)
class ExactFirstCandidate:
    """One exact resource with original lexical reference and independent position."""

    resource: RepositoryResourceOccurrence
    hint: ExactHintObservation
    resolution: ExactHintResolution
    exact_tier_position: int
    native_lexical_rank: int | None
    lexical_result_reference: RepositoryTextLexicalBm25Match | None


@dataclass(frozen=True, slots=True)
class PresentationEntry:
    """Record routed position without changing or synthesizing a score."""

    resource: RepositoryResourceOccurrence
    position: int
    exact: ExactFirstCandidate | None
    native_lexical_rank: int | None
    lexical_result_reference: RepositoryTextLexicalBm25Match | None


@dataclass(frozen=True, slots=True)
class ExactHintRoutingView:
    """Preserve a complete native lane and separately unchanged global safety lane."""

    lane: LocalizationObligationIdentity | GlobalTaskLane
    original_lexical_acquisition: RepositoryTextLexicalBm25RetrievalResult
    exact_resolutions: tuple[ExactHintResolution, ...]
    exact_first: tuple[PresentationEntry, ...]
    global_lexical_safety_lane: RepositoryTextLexicalBm25RetrievalResult
    provenance: TaskProvenance
