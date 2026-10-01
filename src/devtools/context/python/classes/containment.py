# Copyright (c) 2026
"""Validated navigation over class/method occurrence and lexical containment."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context.python.classes.declarations import (
    PythonExcludedClassMethodSyntaxKind,
)

if TYPE_CHECKING:
    from devtools.context.python.classes.declarations import (
        PythonClassDeclarationKnowledge,
        PythonClassMethodAnalysisAggregate,
        PythonMethodDeclarationKnowledge,
    )
    from devtools.context.repository.identity import RepositoryId
    from devtools.context.repository.resource import (
        RepositoryResourceAddress,
        RepositoryResourceOccurrence,
    )
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )


@dataclass(frozen=True, slots=True)
class PythonClassMethodContainmentView:
    """Navigate one validated selection without adding duplicate RI facts."""

    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    aggregate: PythonClassMethodAnalysisAggregate

    def module_body_classes_in(
        self,
        resource_address: RepositoryResourceAddress,
    ) -> tuple[PythonClassDeclarationKnowledge, ...]:
        """Return supported direct classes; reject an unselected resource."""
        for analysis in self.aggregate.analyses:
            if analysis.derivation.dependency.resource.address == resource_address:
                return analysis.classes
        msg = "Resource was not selected for class/method analysis."
        raise ValueError(msg)

    def direct_methods_of(
        self,
        class_declaration: PythonClassDeclarationKnowledge,
    ) -> tuple[PythonMethodDeclarationKnowledge, ...]:
        """Return direct methods in class source order, including empty."""
        for analysis in self.aggregate.analyses:
            if class_declaration in analysis.classes:
                return tuple(
                    item
                    for item in analysis.methods
                    if item.containing_class == class_declaration
                )
        msg = "Class declaration does not belong to the selected analyses."
        raise ValueError(msg)

    def containing_class_of(
        self,
        method: PythonMethodDeclarationKnowledge,
    ) -> PythonClassDeclarationKnowledge:
        """Return the method's one established direct lexical parent."""
        for analysis in self.aggregate.analyses:
            if method in analysis.methods:
                return method.containing_class
        msg = "Method declaration does not belong to the selected analyses."
        raise ValueError(msg)

    def occurrence_resource_of(
        self,
        declaration: PythonClassDeclarationKnowledge | PythonMethodDeclarationKnowledge,
    ) -> RepositoryResourceOccurrence:
        """Return where a selected class or method occurs, not its lexical parent."""
        for analysis in self.aggregate.analyses:
            if declaration in analysis.classes or declaration in analysis.methods:
                return analysis.derivation.dependency.resource
        msg = "Declaration does not belong to the selected analyses."
        raise ValueError(msg)


def build_python_class_method_containment_view(  # noqa: C901
    snapshot: RepositorySnapshot,
    *,
    aggregate: PythonClassMethodAnalysisAggregate,
) -> PythonClassMethodContainmentView:
    """Check native facts against the same retained observed snapshot."""
    if not aggregate.analyses:
        msg = "Class/method containment requires at least one resource analysis."
        raise ValueError(msg)
    seen_addresses: set[RepositoryResourceAddress] = set()
    for analysis in aggregate.analyses:
        derivation = analysis.derivation
        dependency = derivation.dependency
        address = dependency.resource.address
        if address in seen_addresses:
            msg = "Class/method containment repeats a resource analysis."
            raise ValueError(msg)
        seen_addresses.add(address)
        if (
            dependency.repository_id != snapshot.repository_id
            or dependency.snapshot_id != snapshot.id
        ):
            msg = "Class/method analysis belongs to another repository snapshot."
            raise ValueError(msg)
        try:
            observed = snapshot.resource_at(address)
        except ValueError as error:
            msg = "Analyzed resource is absent from the supplied snapshot."
            raise ValueError(msg) from error
        if observed != dependency.resource:
            msg = "Class/method analysis uses stale observed resource content."
            raise ValueError(msg)
        coverage = analysis.coverage
        if (
            coverage.derivation_identity != derivation.identity
            or coverage.class_count != len(analysis.classes)
            or coverage.method_count != len(analysis.methods)
            or coverage.excluded_class_count
            != sum(
                item.kind
                is PythonExcludedClassMethodSyntaxKind.CLASS_OUTSIDE_MODULE_BODY
                for item in analysis.excluded_syntax
            )
            or coverage.excluded_function_count
            != sum(
                item.kind
                is PythonExcludedClassMethodSyntaxKind.FUNCTION_OUTSIDE_SUPPORTED_CLASS
                for item in analysis.excluded_syntax
            )
        ):
            msg = "Class/method coverage differs from its analysis."
            raise ValueError(msg)
        for ordinal, declaration in enumerate(analysis.classes):
            class_subject = declaration.subject
            if (
                declaration.derivation_identity != derivation.identity
                or class_subject.snapshot_id != snapshot.id
                or class_subject.resource_dependency_identity != dependency.identity
                or class_subject.derivation_definition_identity
                != derivation.definition.identity
                or class_subject.declaration_ordinal != ordinal
                or declaration.support.snapshot_id != snapshot.id
                or declaration.support.resource_address != address
                or any(
                    base.ordinal != base_ordinal
                    or base.occurrence.snapshot_id != snapshot.id
                    or base.occurrence.resource_address != address
                    for base_ordinal, base in enumerate(declaration.base_syntax)
                )
            ):
                msg = "Class declaration differs from its resource analysis."
                raise ValueError(msg)
        method_ordinals: dict[str, int] = {}
        for method in analysis.methods:
            parent = method.containing_class
            ordinal = method_ordinals.get(parent.subject.identity, 0)
            method_subject = method.subject
            if (
                parent not in analysis.classes
                or method.derivation_identity != derivation.identity
                or method_subject.snapshot_id != snapshot.id
                or method_subject.resource_dependency_identity != dependency.identity
                or method_subject.derivation_definition_identity
                != derivation.definition.identity
                or method_subject.containing_class_subject_identity
                != parent.subject.identity
                or method_subject.declaration_ordinal != ordinal
                or method.support.snapshot_id != snapshot.id
                or method.support.resource_address != address
            ):
                msg = "Method declaration differs from its class or resource."
                raise ValueError(msg)
            method_ordinals[parent.subject.identity] = ordinal + 1
        if any(
            item.occurrence.snapshot_id != snapshot.id
            or item.occurrence.resource_address != address
            for item in analysis.excluded_syntax
        ):
            msg = "Excluded syntax differs from its observed resource."
            raise ValueError(msg)
    return PythonClassMethodContainmentView(
        repository_id=snapshot.repository_id,
        snapshot_id=snapshot.id,
        aggregate=aggregate,
    )
