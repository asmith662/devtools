# Copyright (c) 2026
"""Analyze exact Name and Attribute occurrences over retained source."""

from __future__ import annotations

import ast
from typing import TYPE_CHECKING, cast

from devtools.context.python.classes.declarations import (
    derive_python_class_method_declarations,
)
from devtools.context.python.function.declarations import (
    PythonModuleResourceDependency,
    PythonSourceOccurrence,
    PythonSourceRange,
    derive_python_function_declarations,
)
from devtools.context.python.imports.declarations import (
    derive_python_import_declarations,
)
from devtools.context.python.references.declarations.bindings import _module_bindings
from devtools.context.python.references.declarations.model import (
    PythonDeclarationReferenceAnalysis,
    PythonDeclarationReferenceAssessment,
    PythonDeclarationReferenceCoverage,
    PythonDeclarationReferenceDerivation,
    PythonDeclarationReferenceKnowledge,
)
from devtools.context.python.references.declarations.resolution import _resolve

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.python.modules.interpretation import (
        PythonModuleInterpretation,
        PythonModuleInterpretationUniverse,
    )
    from devtools.context.repository.resource import RepositoryResourceAddress
    from devtools.context.repository.snapshot import RepositorySnapshot


def derive_python_declaration_references(
    snapshot: RepositorySnapshot,
    *,
    resource_address: RepositoryResourceAddress,
    module_universe: PythonModuleInterpretationUniverse,
    source_interpretations: Sequence[PythonModuleInterpretation] = (),
) -> PythonDeclarationReferenceAnalysis:
    """Assess static Name and outermost Attribute loads over retained content."""
    resource = snapshot.resource_at(resource_address)
    if module_universe.repository_id != snapshot.repository_id or any(
        item.snapshot_id != snapshot.id
        or item.resource != snapshot.resource_at(item.resource.address)
        for item in module_universe.interpretations
    ):
        msg = "Reference module universe differs from the snapshot."
        raise ValueError(msg)
    if any(
        item.snapshot_id != snapshot.id or item.resource != resource
        for item in source_interpretations
    ):
        msg = "Reference source interpretation differs from the snapshot."
        raise ValueError(msg)
    tree = ast.parse(
        resource.content,
        filename=str(resource_address),
        feature_version=(3, 12),
    )
    imports = derive_python_import_declarations(
        snapshot,
        resource_address=resource_address,
    )
    functions = derive_python_function_declarations(
        snapshot,
        resource_address=resource_address,
    )
    classes = derive_python_class_method_declarations(
        snapshot,
        resource_address=resource_address,
    )
    derivation = PythonDeclarationReferenceDerivation(
        PythonModuleResourceDependency(snapshot.id, snapshot.repository_id, resource),
        module_universe.identity,
        tuple(sorted(item.identity for item in source_interpretations)),
    )
    bindings, uncertain_namespace = _module_bindings(
        tree,
        imports,
        functions.declarations,
        classes.classes,
    )
    parents = {
        child: parent
        for parent in ast.walk(tree)
        for child in ast.iter_child_nodes(parent)
    }
    candidates = tuple(
        sorted(
            (
                node
                for node in ast.walk(tree)
                if isinstance(node, (ast.Name, ast.Attribute))
                and isinstance(node.ctx, ast.Load)
                and not _is_inner_attribute(node, parents.get(node))
            ),
            key=lambda node: (
                node.lineno,
                node.col_offset,
                cast("int", node.end_lineno),
                cast("int", node.end_col_offset),
            ),
        ),
    )
    assessments: list[PythonDeclarationReferenceAssessment] = []
    references: list[PythonDeclarationReferenceKnowledge] = []
    for node in candidates:
        occurrence = _occurrence(snapshot, resource_address, node)
        source_text = ast.get_source_segment(resource.content, node)
        if source_text is None:
            msg = "Reference candidate lacks retained exact source text."
            raise ValueError(msg)
        resolved = _resolve(
            snapshot,
            node,
            parents,
            bindings,
            uncertain_namespace,
            imports,
            module_universe,
            source_interpretations,
            classes.classes,
            classes.methods,
        )
        reference = None
        if resolved.target is not None and resolved.route is not None:
            target_resource = snapshot.resource_at(
                resolved.target.support.resource_address,
            )
            reference = PythonDeclarationReferenceKnowledge(
                derivation.identity,
                occurrence,
                resolved.target,
                target_resource,
                resolved.route,
                _is_direct_call(node, parents.get(node)),
                resolved.import_declaration,
                resolved.module_resolution,
                resolved.direct_member_resolution,
                resolved.imported_member_resolution,
                resolved.containing_class,
            )
            references.append(reference)
        assessments.append(
            PythonDeclarationReferenceAssessment(
                occurrence,
                source_text,
                resolved.outcome,
                reference,
            ),
        )
    return PythonDeclarationReferenceAnalysis(
        derivation,
        tuple(references),
        tuple(assessments),
        PythonDeclarationReferenceCoverage(
            derivation.identity,
            len(assessments),
            len(references),
        ),
    )


def _is_inner_attribute(node: ast.AST, parent: ast.AST | None) -> bool:
    return isinstance(parent, ast.Attribute) and parent.value is node


def _is_direct_call(node: ast.AST, parent: ast.AST | None) -> bool:
    return isinstance(parent, ast.Call) and parent.func is node


def _occurrence(
    snapshot: RepositorySnapshot,
    address: RepositoryResourceAddress,
    node: ast.Name | ast.Attribute,
) -> PythonSourceOccurrence:
    return PythonSourceOccurrence(
        snapshot.id,
        address,
        PythonSourceRange(
            node.lineno,
            node.col_offset,
            cast("int", node.end_lineno),
            cast("int", node.end_col_offset),
        ),
    )
