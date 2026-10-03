# Copyright (c) 2026
"""Task-local locator requests and native, unresolved grounding accounts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

from devtools.context.python.modules.interpretation import PythonModuleKind

if TYPE_CHECKING:
    from devtools.context.localization.identity import (
        LocalizationAnchorIdentity,
        LocalizationTaskIdentity,
        TaskProvenance,
    )
    from devtools.context.python.classes.declarations import (
        PythonClassDeclarationKnowledge,
        PythonClassMethodAnalysis,
        PythonMethodDeclarationKnowledge,
    )
    from devtools.context.python.modules.declarations import (
        PythonDirectModuleDeclaration,
        PythonModuleDeclarationLookup,
    )
    from devtools.context.python.modules.interpretation import (
        PythonModuleInterpretation,
        PythonModuleInterpretationUniverse,
    )
    from devtools.context.repository.identity import RepositoryId
    from devtools.context.repository.resource import (
        RepositoryResourceAddress,
        RepositoryResourceOccurrence,
    )
    from devtools.context.repository.snapshot import RepositorySnapshotId


class AnchorGroundingDisposition(Enum):
    """Qualify a result only within its explicit locator and native scope."""

    RESOLVED = "resolved"
    AMBIGUOUS = "ambiguous"
    UNRESOLVED = "unresolved"
    UNSUPPORTED = "unsupported"


class GroundingResolver(Enum):
    """Name the native bounded operation without asserting task acceptance."""

    SNAPSHOT_RESOURCE_AT = "repository-snapshot-resource-at"
    PYTHON_MODULE_LOOKUP = "python-module-exact-name-lookup"
    PYTHON_MODULE_DECLARATION_LOOKUP = "python-direct-module-declaration-lookup"
    PYTHON_METHOD_CONTAINMENT = "python-direct-method-containment"


class PythonDirectDeclarationKind(Enum):
    """Constrain one supported direct module declaration syntax family."""

    FUNCTION = "function"
    CLASS = "class"


@dataclass(frozen=True, slots=True)
class ResourceAddressLocator:
    """Ask for one exact canonical repository-relative resource address."""

    address: RepositoryResourceAddress


@dataclass(frozen=True, slots=True)
class PythonModuleLocator:
    """Ask for an exact dotted name in a supplied explicit-root universe."""

    dotted_name: str
    kind: PythonModuleKind | None = None

    def __post_init__(self) -> None:
        """Exclude arbitrary text and unsupported module-kind values."""
        if not _dotted_identifier(self.dotted_name):
            msg = "Python module locator needs a canonical dotted identifier."
            raise ValueError(msg)
        if self.kind is not None and not isinstance(self.kind, PythonModuleKind):
            msg = "Python module locator has an unsupported module kind."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class PythonDirectDeclarationLocator:
    """Ask for direct syntax of one class/function in an explicit module."""

    module: PythonModuleLocator
    declared_name: str
    kind: PythonDirectDeclarationKind

    def __post_init__(self) -> None:
        """Require a supported exact declaration form, not a qualified guess."""
        if not self.declared_name.isidentifier():
            msg = "Direct declaration locator needs an identifier name."
            raise ValueError(msg)
        if not isinstance(self.kind, PythonDirectDeclarationKind):
            msg = "Direct declaration locator has an unsupported kind."
            raise TypeError(msg)


@dataclass(frozen=True, slots=True)
class PythonDirectMethodLocator:
    """Ask for direct class-body syntax under one known native class declaration."""

    containing_class: PythonClassDeclarationKnowledge
    declared_name: str

    def __post_init__(self) -> None:
        """Require the method name to be an exact Python identifier."""
        if not self.declared_name.isidentifier():
            msg = "Direct method locator needs an identifier name."
            raise ValueError(msg)


type AnchorLocator = (
    ResourceAddressLocator
    | PythonModuleLocator
    | PythonDirectDeclarationLocator
    | PythonDirectMethodLocator
)


@dataclass(frozen=True, slots=True)
class AnchorGroundingRequest:
    """Bind one caller interpretation to a task anchor and retained frame."""

    task: LocalizationTaskIdentity
    anchor: LocalizationAnchorIdentity
    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    locator: AnchorLocator
    provenance: TaskProvenance

    def __post_init__(self) -> None:
        """Reject a foreign anchor or unrecognized locator representation."""
        if self.anchor.task != self.task:
            msg = "Grounding request anchor belongs to another task."
            raise ValueError(msg)
        if not isinstance(
            self.locator,
            (
                ResourceAddressLocator,
                PythonModuleLocator,
                PythonDirectDeclarationLocator,
                PythonDirectMethodLocator,
            ),
        ):
            msg = "Grounding request has an unsupported locator type."
            raise TypeError(msg)


type NativeGroundingReferent = (
    RepositoryResourceOccurrence
    | PythonModuleInterpretation
    | PythonDirectModuleDeclaration
    | PythonMethodDeclarationKnowledge
)
type NativeGroundingEvidence = (
    RepositoryResourceOccurrence
    | PythonModuleInterpretation
    | PythonModuleDeclarationLookup
    | PythonClassMethodAnalysis
)


@dataclass(frozen=True, slots=True)
class AnchorGroundingCandidate:
    """Retain one native referent and the native observation supporting it."""

    referent: NativeGroundingReferent
    evidence: NativeGroundingEvidence


@dataclass(frozen=True, slots=True)
class AnchorGrounding:
    """Report a bounded locator result, never task-semantic acceptance."""

    request: AnchorGroundingRequest
    disposition: AnchorGroundingDisposition
    resolver: GroundingResolver
    candidates: tuple[AnchorGroundingCandidate, ...]
    native_evidence: tuple[NativeGroundingEvidence, ...]
    module_universe: PythonModuleInterpretationUniverse | None
    reason: str

    def __post_init__(self) -> None:
        """Keep outcome cardinality and explanation internally consistent."""
        if not self.reason.strip():
            msg = "Anchor grounding needs an explicit bounded-result reason."
            raise ValueError(msg)
        if (
            self.disposition is AnchorGroundingDisposition.RESOLVED
            and len(
                self.candidates,
            )
            != 1
        ):
            msg = "Resolved grounding requires exactly one native candidate."
            raise ValueError(msg)
        if (
            self.disposition
            in {
                AnchorGroundingDisposition.UNRESOLVED,
                AnchorGroundingDisposition.UNSUPPORTED,
            }
            and self.candidates
        ):
            msg = "Unresolved or unsupported grounding cannot claim a referent."
            raise ValueError(msg)


def _dotted_identifier(value: str) -> bool:
    return bool(value) and all(part.isidentifier() for part in value.split("."))
