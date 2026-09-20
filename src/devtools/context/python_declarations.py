# Copyright (c) 2026
"""Direct module-body Python function declaration knowledge.

The analyzer consumes one caller-selected resource from an already observed
repository snapshot. It parses that admitted UTF-8 text with an explicitly
identified stdlib ``ast`` configuration and accounts exhaustively for only
direct ``Module.body`` ``FunctionDef`` and ``AsyncFunctionDef`` declarations.
"""

from __future__ import annotations

import ast
import hashlib
import platform
import sys
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, ClassVar, cast

if TYPE_CHECKING:
    from devtools.context.repository import (
        RepositoryId,
        RepositoryResourceAddress,
        RepositoryResourceOccurrence,
        RepositorySnapshot,
        RepositorySnapshotId,
    )

_ANALYZER_SEMANTICS_VERSION = "2"
_GRAMMAR_FEATURE_VERSION = (3, 12)
_DEFINITION_IDENTITY_SEMANTICS = (
    "python-direct-module-function-declaration-definition-v1"
)
_DEPENDENCY_IDENTITY_SEMANTICS = "python-module-resource-dependency-v1"
_DERIVATION_IDENTITY_SEMANTICS = "python-function-declaration-derivation-v1"
_SUBJECT_IDENTITY_SEMANTICS = "snapshot-local-python-function-subject-v2"
_KNOWLEDGE_IDENTITY_SEMANTICS = "python-function-declaration-knowledge-v1"


class PythonFunctionDeclarationKind(Enum):
    """Distinguish the two declaration forms covered by this analyzer."""

    SYNCHRONOUS = "function-def"
    ASYNCHRONOUS = "async-function-def"


@dataclass(frozen=True, slots=True)
class PythonSourceRange:
    """Locate Python syntax using the stdlib AST coordinate contract.

    Lines are one-based. Columns are zero-based UTF-8 byte offsets. The end
    position is exclusive. This is a local Python-parser coordinate value, not
    a universal source-location convention.
    """

    start_line: int
    start_column_utf8: int
    end_line: int
    end_column_utf8: int


@dataclass(frozen=True, slots=True)
class PythonSourceOccurrence:
    """Anchor one declaration occurrence in observed snapshot source."""

    snapshot_id: RepositorySnapshotId
    resource_address: RepositoryResourceAddress
    source_range: PythonSourceRange


@dataclass(frozen=True, slots=True)
class PythonModuleResourceDependency:
    """Retain the exact observed module resource consumed by a derivation."""

    snapshot_id: RepositorySnapshotId
    repository_id: RepositoryId
    resource: RepositoryResourceOccurrence

    @property
    def identity(self) -> str:
        """Return the deterministic identity of this direct semantic input."""
        return _semantic_digest(
            _DEPENDENCY_IDENTITY_SEMANTICS,
            str(self.snapshot_id),
            str(self.repository_id),
            str(self.resource.address),
            str(self.resource.content_identity),
        )


@dataclass(frozen=True, slots=True)
class PythonFunctionDeclarationDerivationDefinition:
    """Identify the reusable semantics of the bounded declaration analysis."""

    analyzer_semantics_version: str
    parser_implementation: str
    parser_runtime_version: str
    grammar_feature_version: tuple[int, int]

    TRAVERSAL_SEMANTICS: ClassVar[str] = "direct-ast-module-body-only-v1"
    NODE_VOCABULARY: ClassVar[tuple[str, str]] = (
        "ast.FunctionDef",
        "ast.AsyncFunctionDef",
    )
    PROPOSITION: ClassVar[str] = (
        "direct-module-body-python-function-source-occurrence-"
        "syntactically-declares-snapshot-local-function-subject"
    )

    @property
    def identity(self) -> str:
        """Return identity for all result-affecting definition semantics."""
        return _semantic_digest(
            _DEFINITION_IDENTITY_SEMANTICS,
            self.analyzer_semantics_version,
            self.parser_implementation,
            self.parser_runtime_version,
            ".".join(str(part) for part in self.grammar_feature_version),
            self.TRAVERSAL_SEMANTICS,
            *self.NODE_VOCABULARY,
            self.PROPOSITION,
        )


@dataclass(frozen=True, slots=True)
class PythonFunctionDeclarationDerivation:
    """Apply identified declaration semantics to one direct module dependency."""

    definition: PythonFunctionDeclarationDerivationDefinition
    dependency: PythonModuleResourceDependency

    @property
    def identity(self) -> str:
        """Return the reproducible semantic application identity."""
        return _semantic_digest(
            _DERIVATION_IDENTITY_SEMANTICS,
            self.definition.identity,
            self.dependency.identity,
        )


@dataclass(frozen=True, slots=True)
class PythonFunctionSubject:
    """Represent one analyzer-established snapshot-local function subject."""

    snapshot_id: RepositorySnapshotId
    resource_dependency_identity: str
    declaration_ordinal: int
    derivation_definition_identity: str

    KIND: ClassVar[str] = "python-function"

    @property
    def identity(self) -> str:
        """Return a reproducible identity distinct from name and source range."""
        return _semantic_digest(
            _SUBJECT_IDENTITY_SEMANTICS,
            str(self.snapshot_id),
            self.derivation_definition_identity,
            self.resource_dependency_identity,
            self.KIND,
            str(self.declaration_ordinal),
        )


@dataclass(frozen=True, slots=True)
class PythonFunctionDeclarationKnowledge:
    """Assert that one direct declaration occurrence declares one subject."""

    derivation_identity: str
    subject: PythonFunctionSubject
    support: PythonSourceOccurrence
    declared_name: str
    declaration_kind: PythonFunctionDeclarationKind

    PROPOSITION: ClassVar[str] = (
        PythonFunctionDeclarationDerivationDefinition.PROPOSITION
    )

    @property
    def identity(self) -> str:
        """Return reproducible identity for this separately referable result."""
        source_range = self.support.source_range
        return _semantic_digest(
            _KNOWLEDGE_IDENTITY_SEMANTICS,
            self.derivation_identity,
            self.subject.identity,
            str(self.support.snapshot_id),
            str(self.support.resource_address),
            str(source_range.start_line),
            str(source_range.start_column_utf8),
            str(source_range.end_line),
            str(source_range.end_column_utf8),
            self.declared_name,
            self.declaration_kind.value,
            self.PROPOSITION,
        )


@dataclass(frozen=True, slots=True)
class PythonFunctionDeclarationCoverage:
    """Record exhaustive coverage of the definition's bounded result scope."""

    derivation_identity: str
    declaration_count: int

    SCOPE: ClassVar[str] = (
        "direct-module-body-ast.FunctionDef-or-ast.AsyncFunctionDef"
    )
    IS_EXHAUSTIVE: ClassVar[bool] = True


@dataclass(frozen=True, slots=True)
class PythonFunctionDeclarationAnalysis:
    """Group one successful derivation's knowledge and exhaustive coverage."""

    derivation: PythonFunctionDeclarationDerivation
    declarations: tuple[PythonFunctionDeclarationKnowledge, ...]
    coverage: PythonFunctionDeclarationCoverage


class PythonModuleParseError(Exception):
    """Report a failed parse without publishing successful coverage."""

    derivation: PythonFunctionDeclarationDerivation
    parser_message: str
    line_number: int | None
    parser_offset: int | None

    def __init__(
        self,
        *,
        derivation: PythonFunctionDeclarationDerivation,
        error: SyntaxError,
    ) -> None:
        """Capture the failed semantic application and narrow parser diagnostic."""
        self.derivation = derivation
        self.parser_message = error.msg
        self.line_number = error.lineno
        self.parser_offset = error.offset
        address = derivation.dependency.resource.address
        message = f"Could not parse observed Python module {address}: {error.msg}"
        super().__init__(message)


def derive_python_function_declarations(
    snapshot: RepositorySnapshot,
    *,
    resource_address: RepositoryResourceAddress | None = None,
) -> PythonFunctionDeclarationAnalysis:
    """Derive declarations from one explicitly selected observed resource.

    A returned value accounts exhaustively for the bounded declaration scope.
    A syntax failure raises :class:`PythonModuleParseError` and returns no
    coverage or declaration knowledge. Omitting ``resource_address`` is a
    compatibility path valid only for a snapshot containing exactly one
    resource.
    """
    resource = (
        snapshot.resource
        if resource_address is None
        else snapshot.resource_at(resource_address)
    )
    definition = _current_definition()
    dependency = PythonModuleResourceDependency(
        snapshot_id=snapshot.id,
        repository_id=snapshot.repository_id,
        resource=resource,
    )
    derivation = PythonFunctionDeclarationDerivation(
        definition=definition,
        dependency=dependency,
    )
    try:
        module = ast.parse(
            dependency.resource.content,
            filename=str(dependency.resource.address),
            mode="exec",
            type_comments=False,
            feature_version=definition.grammar_feature_version,
        )
    except SyntaxError as error:
        raise PythonModuleParseError(derivation=derivation, error=error) from error

    declarations: list[PythonFunctionDeclarationKnowledge] = []
    for node in module.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        declaration_ordinal = len(declarations)
        subject = PythonFunctionSubject(
            snapshot_id=snapshot.id,
            resource_dependency_identity=dependency.identity,
            declaration_ordinal=declaration_ordinal,
            derivation_definition_identity=definition.identity,
        )
        source_occurrence = PythonSourceOccurrence(
            snapshot_id=snapshot.id,
            resource_address=dependency.resource.address,
            source_range=PythonSourceRange(
                start_line=node.lineno,
                start_column_utf8=node.col_offset,
                end_line=cast("int", node.end_lineno),
                end_column_utf8=cast("int", node.end_col_offset),
            ),
        )
        declaration_kind = (
            PythonFunctionDeclarationKind.ASYNCHRONOUS
            if isinstance(node, ast.AsyncFunctionDef)
            else PythonFunctionDeclarationKind.SYNCHRONOUS
        )
        declarations.append(
            PythonFunctionDeclarationKnowledge(
                derivation_identity=derivation.identity,
                subject=subject,
                support=source_occurrence,
                declared_name=node.name,
                declaration_kind=declaration_kind,
            ),
        )

    immutable_declarations = tuple(declarations)
    return PythonFunctionDeclarationAnalysis(
        derivation=derivation,
        declarations=immutable_declarations,
        coverage=PythonFunctionDeclarationCoverage(
            derivation_identity=derivation.identity,
            declaration_count=len(immutable_declarations),
        ),
    )


def _current_definition() -> PythonFunctionDeclarationDerivationDefinition:
    """Identify analyzer and ambient parser semantics used for this realization."""
    return PythonFunctionDeclarationDerivationDefinition(
        analyzer_semantics_version=_ANALYZER_SEMANTICS_VERSION,
        parser_implementation=sys.implementation.name,
        parser_runtime_version=platform.python_version(),
        grammar_feature_version=_GRAMMAR_FEATURE_VERSION,
    )


def _semantic_digest(semantics: str, *values: str) -> str:
    """Hash length-framed semantic values for this bounded analyzer."""
    digest = hashlib.sha256()
    for value in (semantics, *values):
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, byteorder="big"))
        digest.update(encoded)
    return digest.hexdigest()
