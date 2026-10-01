# Copyright (c) 2026
"""Historical passive Reference values for the frozen development input archive.

Active Reference derivation lives in ``references.declarations``. These value
classes retain their original module paths solely to deserialize the retained
Case 0002 input archive; no second derivation is defined here.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from devtools.context.python.function.declarations import (
        PythonFunctionDeclarationKnowledge,
        PythonFunctionSubject,
        PythonModuleResourceDependency,
        PythonSourceOccurrence,
    )
    from devtools.context.python.imports.declarations import (
        PythonImportDeclarationKnowledge,
    )
    from devtools.context.python.imports.members import PythonImportedMemberResolution
    from devtools.context.python.imports.resolution import PythonImportResolution

_SEMANTICS = "bounded-python-imported-function-reference-v1"


class PythonReferenceResolutionPath(Enum):
    """Name the qualified target-resolution route."""

    DIRECT_MODULE = "direct-module"
    ONE_FACADE = "one-facade"


class PythonReferenceBindingStatus(Enum):
    """Classify why an import did not establish all possible references."""

    NOT_NAMED_IMPORT = "not-named-import"
    MODULE_UNRESOLVED = "module-unresolved"
    MEMBER_UNRESOLVED = "member-unresolved"
    COMPETING_OR_WILDCARD_BINDING = "competing-or-wildcard-binding"
    DYNAMIC_NAMESPACE = "dynamic-namespace"
    SHADOWED_OR_UNSUPPORTED_SCOPE = "shadowed-or-unsupported-scope"


@dataclass(frozen=True, slots=True)
class PythonReferenceUnsupportedBinding:
    """Record one bounded analysis limitation, not a negative reference fact."""

    declaration: PythonImportDeclarationKnowledge
    status: PythonReferenceBindingStatus
    module_resolution: PythonImportResolution | None = None
    member_resolution: PythonImportedMemberResolution | None = None
    uncertain_occurrences: tuple[PythonSourceOccurrence, ...] = ()


@dataclass(frozen=True, slots=True)
class PythonFunctionReferenceDerivation:
    """Identify the source and explicit module universe used by this analysis."""

    dependency: PythonModuleResourceDependency
    module_universe_identity: str
    source_interpretation_identities: tuple[str, ...]

    @property
    def identity(self) -> str:
        """Identify the semantic application and its direct inputs."""
        return _digest(
            _SEMANTICS,
            self.dependency.identity,
            self.module_universe_identity,
            *self.source_interpretation_identities,
        )


@dataclass(frozen=True, slots=True)
class PythonFunctionReferenceKnowledge:
    """One qualified Name load referring to an existing function subject.

    ``direct_call`` specializes this same reference when the Name occupies
    ``ast.Call.func``. It makes no runtime execution claim.
    """

    derivation_identity: str
    occurrence: PythonSourceOccurrence
    target_declaration: PythonFunctionDeclarationKnowledge
    import_declaration: PythonImportDeclarationKnowledge
    module_resolution: PythonImportResolution
    member_resolution: PythonImportedMemberResolution
    resolution_path: PythonReferenceResolutionPath
    direct_call: bool

    PROPOSITION: ClassVar[str] = "qualified-name-load-references-direct-python-function"

    @property
    def identity(self) -> str:
        """Identify the occurrence, target, and exact qualification support."""
        span = self.occurrence.source_range
        return _digest(
            self.PROPOSITION,
            self.derivation_identity,
            str(self.occurrence.snapshot_id),
            str(self.occurrence.resource_address),
            str(span.start_line),
            str(span.start_column_utf8),
            str(span.end_line),
            str(span.end_column_utf8),
            self.target_declaration.identity,
            self.import_declaration.derivation_identity,
            str(self.import_declaration.declaration_ordinal),
            self.module_resolution.identity,
            self.member_resolution.identity,
            self.resolution_path.value,
            str(self.direct_call),
        )

    @property
    def target_subject(self) -> PythonFunctionSubject:
        """Expose the existing snapshot-local function subject."""
        return self.target_declaration.subject


@dataclass(frozen=True, slots=True)
class PythonFunctionReferenceCoverage:
    """Record bounded positive results and reasons completeness is limited."""

    derivation_identity: str
    examined_imports: int
    reference_count: int
    unsupported_bindings: tuple[PythonReferenceUnsupportedBinding, ...]

    SCOPE: ClassVar[str] = "direct-module-body-named-imports-and-qualified-Name-loads"
    IS_EXHAUSTIVE: ClassVar[bool] = False


@dataclass(frozen=True, slots=True)
class PythonFunctionReferenceAnalysis:
    """One source resource's identified positive facts and bounded coverage."""

    derivation: PythonFunctionReferenceDerivation
    references: tuple[PythonFunctionReferenceKnowledge, ...]
    coverage: PythonFunctionReferenceCoverage


def _digest(*values: str) -> str:
    digest = hashlib.sha256()
    for value in values:
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()
