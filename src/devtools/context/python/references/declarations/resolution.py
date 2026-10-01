# Copyright (c) 2026
"""Resolve bounded Name and Attribute occurrences to supported declarations."""

from __future__ import annotations

import ast
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, cast

from devtools.context.python.classes.declarations import (
    PythonClassDeclarationKnowledge,
    PythonMethodDeclarationKnowledge,
    derive_python_class_method_declarations,
)
from devtools.context.python.imports.members import (
    PythonImportedMemberResolution,
    PythonImportedMemberResolutionOutcome,
    resolve_python_imported_member,
)
from devtools.context.python.imports.resolution import (
    PythonImportResolution,
    PythonImportResolutionOutcome,
    resolve_python_import_declaration,
)
from devtools.context.python.modules.declarations import (
    PythonModuleDeclarationLookup,
    PythonModuleDeclarationLookupOutcome,
    lookup_python_module_declaration,
)
from devtools.context.python.references.declarations.bindings import (
    _at_module_scope,
    _Binding,
    _shadowed,
    _unsupported_scope,
)
from devtools.context.python.references.declarations.model import (
    PythonDeclarationReferenceOutcome,
    PythonDeclarationReferenceRoute,
    PythonReferenceTarget,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.python.imports.declarations import (
        PythonImportDeclarationAnalysis,
        PythonImportDeclarationKnowledge,
    )
    from devtools.context.python.modules.interpretation import (
        PythonModuleInterpretation,
        PythonModuleInterpretationUniverse,
    )
    from devtools.context.repository.snapshot import RepositorySnapshot

_PAIR = 2


@dataclass(frozen=True, slots=True)
class _Resolved:
    outcome: PythonDeclarationReferenceOutcome
    target: PythonReferenceTarget | None = None
    route: PythonDeclarationReferenceRoute | None = None
    import_declaration: PythonImportDeclarationKnowledge | None = None
    module_resolution: PythonImportResolution | None = None
    direct_member_resolution: PythonModuleDeclarationLookup | None = None
    imported_member_resolution: PythonImportedMemberResolution | None = None
    containing_class: PythonClassDeclarationKnowledge | None = None


def _resolve(  # noqa: C901, PLR0911, PLR0912, PLR0913, PLR0917
    snapshot: RepositorySnapshot,
    node: ast.Name | ast.Attribute,
    parents: dict[ast.AST, ast.AST],
    bindings: tuple[_Binding, ...],
    uncertain_namespace: bool,  # noqa: FBT001
    imports: PythonImportDeclarationAnalysis,
    universe: PythonModuleInterpretationUniverse,
    source_interpretations: Sequence[PythonModuleInterpretation],
    classes: tuple[PythonClassDeclarationKnowledge, ...],
    methods: tuple[PythonMethodDeclarationKnowledge, ...],
) -> _Resolved:
    parts = _parts(node)
    if parts is None:
        return _Resolved(PythonDeclarationReferenceOutcome.UNSUPPORTED_EXPRESSION)
    root = parts[0]
    if len(parts) > 1 and root in {"self", "cls"}:
        return _Resolved(PythonDeclarationReferenceOutcome.UNSUPPORTED_RECEIVER)
    if _unsupported_scope(node, parents):
        return _Resolved(PythonDeclarationReferenceOutcome.UNSUPPORTED_SCOPE)
    if _shadowed(node, parents, root):
        return _Resolved(PythonDeclarationReferenceOutcome.SHADOWED_BINDING)
    if uncertain_namespace:
        return _Resolved(PythonDeclarationReferenceOutcome.AMBIGUOUS_BINDING)
    matches = tuple(item for item in bindings if item.name == root)
    if not matches:
        return _Resolved(
            PythonDeclarationReferenceOutcome.UNSUPPORTED_RECEIVER
            if len(parts) > 1
            else PythonDeclarationReferenceOutcome.UNRESOLVED_BINDING,
        )
    if len(matches) != 1:
        return _Resolved(PythonDeclarationReferenceOutcome.AMBIGUOUS_BINDING)
    binding = matches[0]
    if _at_module_scope(node, parents) and binding.line > node.lineno:
        return _Resolved(PythonDeclarationReferenceOutcome.UNRESOLVED_BINDING)
    if binding.kind == "other":
        return _Resolved(PythonDeclarationReferenceOutcome.SHADOWED_BINDING)
    if binding.kind in {"class", "function"}:
        target = binding.declaration
        if target is None:
            return _Resolved(PythonDeclarationReferenceOutcome.TARGET_NOT_DECLARATION)
        if len(parts) == 1:
            return _Resolved(
                PythonDeclarationReferenceOutcome.RESOLVED,
                target,
                PythonDeclarationReferenceRoute.SAME_MODULE,
            )
        if isinstance(target, PythonClassDeclarationKnowledge) and len(parts) == _PAIR:
            return _method_target(
                snapshot,
                target,
                parts[-1],
                classes,
                methods,
            )
        return _Resolved(PythonDeclarationReferenceOutcome.UNSUPPORTED_RECEIVER)
    declaration = binding.import_declaration
    if declaration is None:
        return _Resolved(PythonDeclarationReferenceOutcome.UNSUPPORTED_RECEIVER)
    module_resolution = resolve_python_import_declaration(
        imports,
        declaration,
        target_universe=universe,
        source_interpretations=source_interpretations,
    )
    if module_resolution.outcome is not PythonImportResolutionOutcome.RESOLVED:
        return _Resolved(
            PythonDeclarationReferenceOutcome.MODULE_UNRESOLVED,
            import_declaration=declaration,
            module_resolution=module_resolution,
        )
    if binding.kind == "imported-member":
        if len(parts) > _PAIR:
            return _Resolved(PythonDeclarationReferenceOutcome.UNSUPPORTED_RECEIVER)
        member_name = cast("str", declaration.imported_name)
    else:
        prefix = tuple(
            (declaration.local_alias or declaration.module or "").split("."),
        )
        if len(parts) < len(prefix) + 1 or parts[: len(prefix)] != prefix:
            return _Resolved(PythonDeclarationReferenceOutcome.UNSUPPORTED_RECEIVER)
        if len(parts) > len(prefix) + 2:
            return _Resolved(PythonDeclarationReferenceOutcome.UNSUPPORTED_RECEIVER)
        member_name = parts[len(prefix)]
    member = lookup_python_module_declaration(
        snapshot,
        module=module_resolution.matches[0],
        declared_name=member_name,
    )
    support = _Resolved(
        PythonDeclarationReferenceOutcome.MEMBER_UNRESOLVED,
        import_declaration=declaration,
        module_resolution=module_resolution,
        direct_member_resolution=member,
    )
    if member.outcome is not PythonModuleDeclarationLookupOutcome.RESOLVED:
        if binding.kind == "imported-member" and len(parts) == 1:
            facade = resolve_python_imported_member(
                snapshot,
                imports,
                declaration,
                module_universe=universe,
                source_interpretations=source_interpretations,
            )
            if facade.outcome is PythonImportedMemberResolutionOutcome.RESOLVED:
                return replace(
                    support,
                    outcome=PythonDeclarationReferenceOutcome.RESOLVED,
                    target=facade.target_declaration,
                    route=PythonDeclarationReferenceRoute.ONE_FACADE,
                    imported_member_resolution=facade,
                )
        outcome = {
            PythonModuleDeclarationLookupOutcome.UNRESOLVED: (
                PythonDeclarationReferenceOutcome.MEMBER_UNRESOLVED
            ),
            PythonModuleDeclarationLookupOutcome.AMBIGUOUS: (
                PythonDeclarationReferenceOutcome.AMBIGUOUS_BINDING
            ),
            PythonModuleDeclarationLookupOutcome.NOT_DECLARATION: (
                PythonDeclarationReferenceOutcome.TARGET_NOT_DECLARATION
            ),
        }[member.outcome]
        return replace(support, outcome=outcome)
    target = member.target
    # A RESOLVED direct lookup establishes a declaration target by contract.
    target = cast("PythonReferenceTarget", target)
    if binding.kind == "imported-member":
        if len(parts) == 1:
            route = PythonDeclarationReferenceRoute.IMPORTED_MEMBER
        elif isinstance(target, PythonClassDeclarationKnowledge):
            return _method_target(
                snapshot,
                target,
                parts[-1],
                (),
                (),
                import_declaration=declaration,
                module_resolution=module_resolution,
                direct_member_resolution=member,
            )
        else:
            return _Resolved(PythonDeclarationReferenceOutcome.UNSUPPORTED_RECEIVER)
    elif len(parts) == len(prefix) + 1:
        route = PythonDeclarationReferenceRoute.MODULE_QUALIFIED
    elif isinstance(target, PythonClassDeclarationKnowledge):
        return _method_target(
            snapshot,
            target,
            parts[-1],
            (),
            (),
            import_declaration=declaration,
            module_resolution=module_resolution,
            direct_member_resolution=member,
        )
    else:
        return _Resolved(PythonDeclarationReferenceOutcome.UNSUPPORTED_RECEIVER)
    return replace(
        support,
        outcome=PythonDeclarationReferenceOutcome.RESOLVED,
        target=target,
        route=route,
    )


def _method_target(  # noqa: PLR0913
    snapshot: RepositorySnapshot,
    parent: PythonClassDeclarationKnowledge,
    name: str,
    local_classes: tuple[PythonClassDeclarationKnowledge, ...],
    local_methods: tuple[PythonMethodDeclarationKnowledge, ...],
    *,
    import_declaration: PythonImportDeclarationKnowledge | None = None,
    module_resolution: PythonImportResolution | None = None,
    direct_member_resolution: PythonModuleDeclarationLookup | None = None,
) -> _Resolved:
    methods = local_methods
    resource = snapshot.resource_at(parent.support.resource_address)
    if parent not in local_classes:
        analysis = derive_python_class_method_declarations(
            snapshot,
            resource_address=parent.support.resource_address,
        )
        methods = analysis.methods
    tree = ast.parse(resource.content)
    class_node = next(
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef)
        and node.lineno == parent.support.source_range.start_line
        and node.col_offset == parent.support.source_range.start_column_utf8
    )
    competing = sum(_class_body_binds_name(node, name) for node in class_node.body)
    candidates = tuple(
        item
        for item in methods
        if item.containing_class == parent and item.declared_name == name
    )
    decorated = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and node.name == name
        and bool(node.decorator_list)
        for node in class_node.body
    )
    if competing != 1:
        return _Resolved(
            PythonDeclarationReferenceOutcome.AMBIGUOUS_BINDING
            if competing > 1
            else PythonDeclarationReferenceOutcome.METHOD_UNRESOLVED,
            import_declaration=import_declaration,
            module_resolution=module_resolution,
            direct_member_resolution=direct_member_resolution,
        )
    if len(candidates) != 1 or decorated:
        return _Resolved(
            PythonDeclarationReferenceOutcome.METHOD_UNRESOLVED,
            import_declaration=import_declaration,
            module_resolution=module_resolution,
            direct_member_resolution=direct_member_resolution,
        )
    return _Resolved(
        PythonDeclarationReferenceOutcome.RESOLVED,
        candidates[0],
        PythonDeclarationReferenceRoute.CLASS_QUALIFIED_METHOD,
        import_declaration=import_declaration,
        module_resolution=module_resolution,
        direct_member_resolution=direct_member_resolution,
        containing_class=parent,
    )


def _class_body_binds_name(node: ast.stmt, name: str) -> bool:
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == name
    if isinstance(node, ast.Import | ast.ImportFrom):
        return any(
            alias.name == "*"
            or (
                alias.asname
                or (
                    alias.name
                    if isinstance(node, ast.ImportFrom)
                    else alias.name.split(".")[0]
                )
            )
            == name
            for alias in node.names
        )
    return any(
        (
            isinstance(child, ast.Name)
            and isinstance(child.ctx, ast.Store | ast.Del)
            and child.id == name
        )
        or (
            isinstance(child, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef)
            and child.name == name
        )
        for child in ast.walk(node)
    )


def _parts(node: ast.Name | ast.Attribute) -> tuple[str, ...] | None:
    if isinstance(node, ast.Name):
        return (node.id,)
    if isinstance(node.value, (ast.Name, ast.Attribute)):
        parts = _parts(node.value)
        return (*parts, node.attr) if parts is not None else None
    return None
