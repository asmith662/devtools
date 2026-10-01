# Copyright (c) 2026
"""Bounded Python module-body class and direct class-body method knowledge."""

from __future__ import annotations

import ast
import hashlib
import platform
import sys
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, ClassVar, Protocol, cast

from devtools.context.python.function.declarations import (
    PythonFunctionDeclarationKind,
    PythonModuleResourceDependency,
    PythonSourceOccurrence,
    PythonSourceRange,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.repository.resource import RepositoryResourceAddress
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )

_GRAMMAR_FEATURE_VERSION = (3, 12)
_ANALYZER_SEMANTICS_VERSION = "1"


class _LocatedAstNode(Protocol):
    lineno: int
    col_offset: int
    end_lineno: int | None
    end_col_offset: int | None


@dataclass(frozen=True, slots=True)
class PythonClassMethodDerivationDefinition:
    """Identify the parser and the bounded class/method traversal contract."""

    analyzer_semantics_version: str
    parser_implementation: str
    parser_runtime_version: str
    grammar_feature_version: tuple[int, int]

    TRAVERSAL_SEMANTICS: ClassVar[str] = "module-class-direct-method-v1"
    NODE_VOCABULARY: ClassVar[tuple[str, str, str]] = (
        "ast.ClassDef",
        "ast.FunctionDef",
        "ast.AsyncFunctionDef",
    )

    @property
    def identity(self) -> str:
        """Bind every result-affecting definition setting."""
        return _digest(
            "python-class-method-definition-v1",
            self.analyzer_semantics_version,
            self.parser_implementation,
            self.parser_runtime_version,
            ".".join(str(part) for part in self.grammar_feature_version),
            self.TRAVERSAL_SEMANTICS,
            *self.NODE_VOCABULARY,
        )


@dataclass(frozen=True, slots=True)
class PythonClassMethodDerivation:
    """Apply one class/method definition to one exact observed resource."""

    definition: PythonClassMethodDerivationDefinition
    dependency: PythonModuleResourceDependency

    @property
    def identity(self) -> str:
        """Bind semantics to the observed resource and content."""
        return _digest(
            "python-class-method-derivation-v1",
            self.definition.identity,
            self.dependency.identity,
        )


@dataclass(frozen=True, slots=True)
class PythonClassSubject:
    """Identify one direct module-body class structurally, not at runtime."""

    snapshot_id: RepositorySnapshotId
    resource_dependency_identity: str
    derivation_definition_identity: str
    declaration_ordinal: int

    KIND: ClassVar[str] = "python-module-body-class"

    @property
    def identity(self) -> str:
        """Distinguish repeated names and classes in different resources."""
        return _digest(
            "python-class-subject-v1",
            str(self.snapshot_id),
            self.resource_dependency_identity,
            self.derivation_definition_identity,
            self.KIND,
            str(self.declaration_ordinal),
        )


@dataclass(frozen=True, slots=True)
class PythonMethodSubject:
    """Identify one direct method under a particular class subject."""

    snapshot_id: RepositorySnapshotId
    resource_dependency_identity: str
    derivation_definition_identity: str
    containing_class_subject_identity: str
    declaration_ordinal: int

    KIND: ClassVar[str] = "python-direct-class-body-method"

    @property
    def identity(self) -> str:
        """Use structural parent and ordinal, never a bare method name."""
        return _digest(
            "python-method-subject-v1",
            str(self.snapshot_id),
            self.resource_dependency_identity,
            self.derivation_definition_identity,
            self.containing_class_subject_identity,
            self.KIND,
            str(self.declaration_ordinal),
        )


@dataclass(frozen=True, slots=True)
class PythonClassBaseSyntax:
    """Retain one direct base-expression span without resolving its target."""

    ordinal: int
    occurrence: PythonSourceOccurrence
    source_text: str


@dataclass(frozen=True, slots=True)
class PythonClassDeclarationKnowledge:
    """Assert a direct module-body ``ClassDef`` occurrence and subject."""

    derivation_identity: str
    subject: PythonClassSubject
    support: PythonSourceOccurrence
    declared_name: str
    base_syntax: tuple[PythonClassBaseSyntax, ...]

    PROPOSITION: ClassVar[str] = "direct-module-body-classdef-declares-class-subject"

    @property
    def identity(self) -> str:
        """Identify this source-grounded declaration, distinct from its subject."""
        span = self.support.source_range
        return _digest(
            "python-class-declaration-knowledge-v1",
            self.PROPOSITION,
            self.derivation_identity,
            self.subject.identity,
            str(self.support.snapshot_id),
            str(self.support.resource_address),
            *(_range_values(span)),
            self.declared_name,
            *(
                value
                for base in self.base_syntax
                for value in (
                    str(base.ordinal),
                    *_range_values(base.occurrence.source_range),
                    base.source_text,
                )
            ),
        )


@dataclass(frozen=True, slots=True)
class PythonMethodDeclarationKnowledge:
    """Assert a direct class-body function syntax with one lexical parent."""

    derivation_identity: str
    subject: PythonMethodSubject
    support: PythonSourceOccurrence
    declared_name: str
    declaration_kind: PythonFunctionDeclarationKind
    containing_class: PythonClassDeclarationKnowledge

    PROPOSITION: ClassVar[str] = "direct-class-body-functiondef-declares-method-subject"

    @property
    def identity(self) -> str:
        """Identify this method occurrence and its direct class parent."""
        return _digest(
            "python-method-declaration-knowledge-v1",
            self.PROPOSITION,
            self.derivation_identity,
            self.subject.identity,
            self.containing_class.identity,
            str(self.support.snapshot_id),
            str(self.support.resource_address),
            *_range_values(self.support.source_range),
            self.declared_name,
            self.declaration_kind.value,
        )


class PythonExcludedClassMethodSyntaxKind(Enum):
    """Classify encountered declarations outside this analyzer's positive scope."""

    CLASS_OUTSIDE_MODULE_BODY = "class-outside-module-body"
    FUNCTION_OUTSIDE_SUPPORTED_CLASS = "function-outside-supported-class"


@dataclass(frozen=True, slots=True)
class PythonExcludedClassMethodSyntax:
    """Retain an encountered but unsupported declaration occurrence."""

    kind: PythonExcludedClassMethodSyntaxKind
    occurrence: PythonSourceOccurrence


@dataclass(frozen=True, slots=True)
class PythonClassMethodCoverage:
    """Account for bounded positive syntax and encountered exclusions."""

    derivation_identity: str
    class_count: int
    method_count: int
    module_body_function_count: int
    excluded_class_count: int
    excluded_function_count: int

    SCOPE: ClassVar[str] = "module-body-ClassDef-and-direct-class-body-methods"
    IS_EXHAUSTIVE_FOR_SCOPE: ClassVar[bool] = True


@dataclass(frozen=True, slots=True)
class PythonClassMethodAnalysis:
    """One successful resource derivation and its native facts and coverage."""

    derivation: PythonClassMethodDerivation
    classes: tuple[PythonClassDeclarationKnowledge, ...]
    methods: tuple[PythonMethodDeclarationKnowledge, ...]
    excluded_syntax: tuple[PythonExcludedClassMethodSyntax, ...]
    coverage: PythonClassMethodCoverage


@dataclass(frozen=True, slots=True)
class PythonClassMethodAnalysisAggregate:
    """Ordered independent analyses for an explicit resource selection."""

    analyses: tuple[PythonClassMethodAnalysis, ...]

    @property
    def classes(self) -> tuple[PythonClassDeclarationKnowledge, ...]:
        """Preserve selection order and module source order."""
        return tuple(item for analysis in self.analyses for item in analysis.classes)

    @property
    def methods(self) -> tuple[PythonMethodDeclarationKnowledge, ...]:
        """Preserve selection, class, and method source order."""
        return tuple(item for analysis in self.analyses for item in analysis.methods)


class PythonClassMethodParseError(Exception):
    """Report parse failure without publishing positive facts or coverage."""

    def __init__(
        self,
        derivation: PythonClassMethodDerivation,
        error: SyntaxError,
    ) -> None:
        """Retain the failed semantic application and parser diagnostic."""
        self.derivation = derivation
        self.parser_message = error.msg
        self.line_number = error.lineno
        self.parser_offset = error.offset
        super().__init__(
            f"Could not parse observed Python module "
            f"{derivation.dependency.resource.address}: {error.msg}",
        )


def derive_python_class_method_declarations(
    snapshot: RepositorySnapshot,
    *,
    resource_address: RepositoryResourceAddress | None = None,
) -> PythonClassMethodAnalysis:
    """Derive only direct module classes and their direct sync/async methods."""
    resource = (
        snapshot.resource
        if resource_address is None
        else snapshot.resource_at(resource_address)
    )
    definition = PythonClassMethodDerivationDefinition(
        analyzer_semantics_version=_ANALYZER_SEMANTICS_VERSION,
        parser_implementation=sys.implementation.name,
        parser_runtime_version=platform.python_version(),
        grammar_feature_version=_GRAMMAR_FEATURE_VERSION,
    )
    dependency = PythonModuleResourceDependency(
        snapshot_id=snapshot.id,
        repository_id=snapshot.repository_id,
        resource=resource,
    )
    derivation = PythonClassMethodDerivation(definition, dependency)
    try:
        module = ast.parse(
            resource.content,
            filename=str(resource.address),
            mode="exec",
            type_comments=False,
            feature_version=definition.grammar_feature_version,
        )
    except SyntaxError as error:
        raise PythonClassMethodParseError(derivation, error) from error

    classes: list[PythonClassDeclarationKnowledge] = []
    methods: list[PythonMethodDeclarationKnowledge] = []
    supported_nodes: set[int] = set()
    module_functions: set[int] = set()
    for node in module.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            module_functions.add(id(node))
        if not isinstance(node, ast.ClassDef):
            continue
        supported_nodes.add(id(node))
        subject = PythonClassSubject(
            snapshot_id=snapshot.id,
            resource_dependency_identity=dependency.identity,
            derivation_definition_identity=definition.identity,
            declaration_ordinal=len(classes),
        )
        declaration = PythonClassDeclarationKnowledge(
            derivation_identity=derivation.identity,
            subject=subject,
            support=_occurrence(snapshot.id, resource.address, node),
            declared_name=node.name,
            base_syntax=tuple(
                PythonClassBaseSyntax(
                    ordinal=ordinal,
                    occurrence=_occurrence(snapshot.id, resource.address, base),
                    source_text=_base_source_text(resource.content, base),
                )
                for ordinal, base in enumerate(node.bases)
            ),
        )
        classes.append(declaration)
        method_ordinal = 0
        for child in node.body:
            if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            supported_nodes.add(id(child))
            method_subject = PythonMethodSubject(
                snapshot_id=snapshot.id,
                resource_dependency_identity=dependency.identity,
                derivation_definition_identity=definition.identity,
                containing_class_subject_identity=subject.identity,
                declaration_ordinal=method_ordinal,
            )
            methods.append(
                PythonMethodDeclarationKnowledge(
                    derivation_identity=derivation.identity,
                    subject=method_subject,
                    support=_occurrence(snapshot.id, resource.address, child),
                    declared_name=child.name,
                    declaration_kind=(
                        PythonFunctionDeclarationKind.ASYNCHRONOUS
                        if isinstance(child, ast.AsyncFunctionDef)
                        else PythonFunctionDeclarationKind.SYNCHRONOUS
                    ),
                    containing_class=declaration,
                ),
            )
            method_ordinal += 1

    excluded_function_kind = (
        PythonExcludedClassMethodSyntaxKind.FUNCTION_OUTSIDE_SUPPORTED_CLASS
    )
    excluded = tuple(
        sorted(
            (
                PythonExcludedClassMethodSyntax(
                    kind=(
                        PythonExcludedClassMethodSyntaxKind.CLASS_OUTSIDE_MODULE_BODY
                        if isinstance(node, ast.ClassDef)
                        else excluded_function_kind
                    ),
                    occurrence=_occurrence(snapshot.id, resource.address, node),
                )
                for node in ast.walk(module)
                if isinstance(
                    node,
                    (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef),
                )
                and id(node) not in supported_nodes
                and id(node) not in module_functions
            ),
            key=lambda item: (
                item.occurrence.source_range.start_line,
                item.occurrence.source_range.start_column_utf8,
                item.kind.value,
            ),
        ),
    )
    return PythonClassMethodAnalysis(
        derivation=derivation,
        classes=tuple(classes),
        methods=tuple(methods),
        excluded_syntax=excluded,
        coverage=PythonClassMethodCoverage(
            derivation_identity=derivation.identity,
            class_count=len(classes),
            method_count=len(methods),
            module_body_function_count=len(module_functions),
            excluded_class_count=sum(
                item.kind
                is PythonExcludedClassMethodSyntaxKind.CLASS_OUTSIDE_MODULE_BODY
                for item in excluded
            ),
            excluded_function_count=sum(
                item.kind is excluded_function_kind for item in excluded
            ),
        ),
    )


def analyze_python_class_method_resources(
    snapshot: RepositorySnapshot,
    *,
    resource_addresses: Sequence[RepositoryResourceAddress],
) -> PythonClassMethodAnalysisAggregate:
    """Analyze a caller-ordered distinct selection without a synthetic derivation."""
    addresses = tuple(resource_addresses)
    if not addresses:
        msg = "Class/method analysis requires at least one resource address."
        raise ValueError(msg)
    if len(set(addresses)) != len(addresses):
        msg = "Class/method analysis resource addresses must be distinct."
        raise ValueError(msg)
    for address in addresses:
        snapshot.resource_at(address)
    return PythonClassMethodAnalysisAggregate(
        analyses=tuple(
            derive_python_class_method_declarations(snapshot, resource_address=address)
            for address in addresses
        ),
    )


def _occurrence(
    snapshot_id: RepositorySnapshotId,
    resource_address: RepositoryResourceAddress,
    node: ast.AST,
) -> PythonSourceOccurrence:
    located = cast("_LocatedAstNode", node)
    return PythonSourceOccurrence(
        snapshot_id=snapshot_id,
        resource_address=resource_address,
        source_range=PythonSourceRange(
            start_line=located.lineno,
            start_column_utf8=located.col_offset,
            end_line=cast("int", located.end_lineno),
            end_column_utf8=cast("int", located.end_col_offset),
        ),
    )


def _range_values(source_range: PythonSourceRange) -> tuple[str, str, str, str]:
    return (
        str(source_range.start_line),
        str(source_range.start_column_utf8),
        str(source_range.end_line),
        str(source_range.end_column_utf8),
    )


def _base_source_text(content: str, base: ast.expr) -> str:
    source_text = ast.get_source_segment(content, base)
    if source_text is None:
        msg = "Parsed base expression lacks exact observed source text."
        raise ValueError(msg)
    return source_text


def _digest(*values: str) -> str:
    digest = hashlib.sha256()
    for value in values:
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()
