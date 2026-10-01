# Copyright (c) 2026
"""Source-grounded Reference facts and bounded occurrence assessments."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, ClassVar

from devtools.context.python.classes.declarations import (
    PythonClassDeclarationKnowledge,
    PythonClassSubject,
    PythonMethodDeclarationKnowledge,
    PythonMethodSubject,
)
from devtools.context.python.function.declarations import (
    PythonFunctionDeclarationKnowledge,
    PythonFunctionSubject,
    PythonModuleResourceDependency,
    PythonSourceOccurrence,
)

if TYPE_CHECKING:
    from devtools.context.python.imports.declarations import (
        PythonImportDeclarationKnowledge,
    )
    from devtools.context.python.imports.members import PythonImportedMemberResolution
    from devtools.context.python.imports.resolution import PythonImportResolution
    from devtools.context.python.modules.declarations import (
        PythonModuleDeclarationLookup,
    )
    from devtools.context.repository.resource import RepositoryResourceOccurrence

type PythonReferenceTarget = (
    PythonFunctionDeclarationKnowledge
    | PythonClassDeclarationKnowledge
    | PythonMethodDeclarationKnowledge
)
_SEMANTICS = "bounded-declaration-reference-v1"


class PythonDeclarationReferenceRoute(Enum):
    """Name one established static path to a supported declaration."""

    SAME_MODULE = "same-module"
    IMPORTED_MEMBER = "imported-member"
    ONE_FACADE = "one-facade-imported-member"
    MODULE_QUALIFIED = "module-qualified-member"
    CLASS_QUALIFIED_METHOD = "class-qualified-method"


class PythonDeclarationReferenceOutcome(Enum):
    """Assess an encountered Name or outermost Attribute load."""

    RESOLVED = "resolved"
    UNRESOLVED_BINDING = "unresolved-binding"
    AMBIGUOUS_BINDING = "ambiguous-binding"
    SHADOWED_BINDING = "shadowed-binding"
    UNSUPPORTED_SCOPE = "unsupported-scope"
    UNSUPPORTED_RECEIVER = "unsupported-receiver"
    UNSUPPORTED_EXPRESSION = "unsupported-expression"
    MODULE_UNRESOLVED = "module-unresolved"
    MEMBER_UNRESOLVED = "member-unresolved"
    TARGET_NOT_DECLARATION = "target-not-supported-declaration"
    METHOD_UNRESOLVED = "method-unresolved"


@dataclass(frozen=True, slots=True)
class PythonDeclarationReferenceDerivation:
    """Bind the source resource and explicit interpretation universe."""

    dependency: PythonModuleResourceDependency
    module_universe_identity: str
    source_interpretation_identities: tuple[str, ...]

    @property
    def identity(self) -> str:
        """Identify this bounded static interpretation."""
        return _digest(
            _SEMANTICS,
            self.dependency.identity,
            self.module_universe_identity,
            *self.source_interpretation_identities,
        )


@dataclass(frozen=True, slots=True)
class PythonDeclarationReferenceKnowledge:
    """One exact syntactic expression referring to a supported declaration."""

    derivation_identity: str
    occurrence: PythonSourceOccurrence
    target_declaration: PythonReferenceTarget
    target_resource: RepositoryResourceOccurrence
    route: PythonDeclarationReferenceRoute
    direct_call: bool
    import_declaration: PythonImportDeclarationKnowledge | None = None
    module_resolution: PythonImportResolution | None = None
    direct_member_resolution: PythonModuleDeclarationLookup | None = None
    imported_member_resolution: PythonImportedMemberResolution | None = None
    containing_class: PythonClassDeclarationKnowledge | None = None

    PROPOSITION: ClassVar[str] = "bounded-expression-references-python-declaration"

    @property
    def target_subject(
        self,
    ) -> PythonFunctionSubject | PythonClassSubject | PythonMethodSubject:
        """Expose the existing structural subject, never a display name."""
        return self.target_declaration.subject

    @property
    def identity(self) -> str:
        """Bind both exact occurrences, dependencies, and qualification support."""
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
            str(self.target_resource.content_identity),
            self.route.value,
            str(self.direct_call),
            self.import_declaration.derivation_identity
            if self.import_declaration
            else "",
            str(self.import_declaration.declaration_ordinal)
            if self.import_declaration
            else "",
            self.module_resolution.identity if self.module_resolution else "",
            self.direct_member_resolution.identity
            if self.direct_member_resolution
            else "",
            self.imported_member_resolution.identity
            if self.imported_member_resolution
            else "",
            self.containing_class.identity if self.containing_class else "",
        )


@dataclass(frozen=True, slots=True)
class PythonDeclarationReferenceAssessment:
    """Account for one candidate expression, including unresolved forms."""

    occurrence: PythonSourceOccurrence
    source_text: str
    outcome: PythonDeclarationReferenceOutcome
    reference: PythonDeclarationReferenceKnowledge | None = None


@dataclass(frozen=True, slots=True)
class PythonDeclarationReferenceCoverage:
    """Bounded occurrence inventory; never exhaustive Python name resolution."""

    derivation_identity: str
    assessed_count: int
    reference_count: int

    SCOPE: ClassVar[str] = "Name-and-outermost-Attribute-loads-in-observed-source"
    IS_EXHAUSTIVE: ClassVar[bool] = False


@dataclass(frozen=True, slots=True)
class PythonDeclarationReferenceAnalysis:
    """One source's ordered positive facts and per-expression assessments."""

    derivation: PythonDeclarationReferenceDerivation
    references: tuple[PythonDeclarationReferenceKnowledge, ...]
    assessments: tuple[PythonDeclarationReferenceAssessment, ...]
    coverage: PythonDeclarationReferenceCoverage


def _digest(*values: str) -> str:
    digest = hashlib.sha256()
    for value in values:
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()
