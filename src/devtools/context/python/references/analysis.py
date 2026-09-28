# Copyright (c) 2026
"""Conservative occurrence-to-function Repository Intelligence.

Only a unique direct module-body ``from`` binding can qualify a Name load.
The resolved target is an existing direct module-body function declaration,
possibly through the production one-facade imported-member resolver. A Name
load in ``ast.Call.func`` is additionally a *direct Call* occurrence. Neither
fact asserts runtime invocation, method dispatch, or caller identity.
"""

from __future__ import annotations

import ast
import hashlib
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, ClassVar, cast

from devtools.context.python.function.declarations import (
    PythonFunctionDeclarationKnowledge,
    PythonFunctionSubject,
    PythonModuleResourceDependency,
    PythonSourceOccurrence,
    PythonSourceRange,
    derive_python_function_declarations,
)
from devtools.context.python.imports.declarations import (
    PythonImportDeclarationKnowledge,
    derive_python_import_declarations,
)
from devtools.context.python.imports.members import (
    PythonFacadeCompetingBindingKind,
    PythonImportedMemberResolution,
    PythonImportedMemberResolutionOutcome,
    PythonImportedMemberUnsupportedReason,
    resolve_python_imported_member,
)
from devtools.context.python.imports.resolution import (
    PythonImportResolution,
    PythonImportResolutionOutcome,
    resolve_python_import_declaration,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.python.modules.interpretation import (
        PythonModuleInterpretation,
        PythonModuleInterpretationUniverse,
    )
    from devtools.context.repository.resource import RepositoryResourceAddress
    from devtools.context.repository.snapshot import RepositorySnapshot

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


def derive_python_function_references(  # noqa: C901, PLR0912
    snapshot: RepositorySnapshot,
    *,
    resource_address: RepositoryResourceAddress,
    module_universe: PythonModuleInterpretationUniverse,
    source_interpretations: Sequence[PythonModuleInterpretation] = (),
) -> PythonFunctionReferenceAnalysis:
    """Derive qualified references from one observed source, without retrieval.

    Ambiguous, dynamic, shadowed, and unsupported bindings establish no fact.
    A successful result never asserts exhaustive Python name resolution.
    """
    resource = snapshot.resource_at(resource_address)
    if module_universe.repository_id != snapshot.repository_id or any(
        item.snapshot_id != snapshot.id
        or item.resource != snapshot.resource_at(item.resource.address)
        for item in module_universe.interpretations
    ):
        msg = "Module universe does not belong to the supplied snapshot."
        raise ValueError(msg)
    if any(
        item.snapshot_id != snapshot.id or item.resource != resource
        for item in source_interpretations
    ):
        msg = "Source interpretations do not match the selected source."
        raise ValueError(msg)
    imports = derive_python_import_declarations(
        snapshot,
        resource_address=resource_address,
    )
    tree = ast.parse(
        resource.content,
        filename=str(resource_address),
        feature_version=(3, 12),
    )
    derivation = PythonFunctionReferenceDerivation(
        dependency=PythonModuleResourceDependency(
            snapshot_id=snapshot.id,
            repository_id=snapshot.repository_id,
            resource=resource,
        ),
        module_universe_identity=module_universe.identity,
        source_interpretation_identities=tuple(
            sorted(item.identity for item in source_interpretations),
        ),
    )
    bindings, wildcard = _bindings(tree)
    dynamic = any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in {"exec", "globals", "locals"}
        for node in ast.walk(tree)
    )
    unsupported: list[PythonReferenceUnsupportedBinding] = []
    references: list[PythonFunctionReferenceKnowledge] = []
    uncertain_scope = PythonReferenceBindingStatus.SHADOWED_OR_UNSUPPORTED_SCOPE
    for declaration in imports.declarations:
        status: PythonReferenceBindingStatus | None = None
        resolution: PythonImportResolution | None = None
        member: PythonImportedMemberResolution | None = None
        uncertain_occurrences: tuple[PythonSourceOccurrence, ...] = ()
        if declaration.imported_name in {None, "*"}:
            status = PythonReferenceBindingStatus.NOT_NAMED_IMPORT
        else:
            local = declaration.local_alias or declaration.imported_name
            if bindings[local] != 1 or wildcard or _has_dynamic_binding(tree, local):
                status = PythonReferenceBindingStatus.COMPETING_OR_WILDCARD_BINDING
            elif dynamic:
                status = PythonReferenceBindingStatus.DYNAMIC_NAMESPACE
            else:
                resolution = resolve_python_import_declaration(
                    imports,
                    declaration,
                    target_universe=module_universe,
                    source_interpretations=source_interpretations,
                )
                if resolution.outcome is not PythonImportResolutionOutcome.RESOLVED:
                    status = PythonReferenceBindingStatus.MODULE_UNRESOLVED
                else:
                    member = resolve_python_imported_member(
                        snapshot,
                        imports,
                        declaration,
                        module_universe=module_universe,
                        source_interpretations=source_interpretations,
                    )
                    target, path = _target(snapshot, declaration, resolution, member)
                    if target is None or path is None:
                        status = PythonReferenceBindingStatus.MEMBER_UNRESOLVED
                    else:
                        loads, uncertain = _qualified_loads(tree, local)
                        uncertain_occurrences = tuple(
                            _occurrence(snapshot, resource_address, node)
                            for node in uncertain
                        )
                        if uncertain_occurrences:
                            status = uncertain_scope
                        references.extend(
                            PythonFunctionReferenceKnowledge(
                                derivation_identity=derivation.identity,
                                occurrence=_occurrence(
                                    snapshot,
                                    resource_address,
                                    node,
                                ),
                                target_declaration=target,
                                import_declaration=declaration,
                                module_resolution=resolution,
                                member_resolution=member,
                                resolution_path=path,
                                direct_call=call,
                            )
                            for node, call in loads
                        )
        if status is not None:
            unsupported.append(
                PythonReferenceUnsupportedBinding(
                    declaration,
                    status,
                    resolution,
                    member,
                    uncertain_occurrences,
                ),
            )
    values = tuple(references)
    return PythonFunctionReferenceAnalysis(
        derivation=derivation,
        references=values,
        coverage=PythonFunctionReferenceCoverage(
            derivation.identity,
            len(imports.declarations),
            len(values),
            tuple(unsupported),
        ),
    )


def _target(
    snapshot: RepositorySnapshot,
    declaration: PythonImportDeclarationKnowledge,
    resolution: PythonImportResolution,
    member: PythonImportedMemberResolution,
) -> tuple[
    PythonFunctionDeclarationKnowledge | None,
    PythonReferenceResolutionPath | None,
]:
    if member.outcome is PythonImportedMemberResolutionOutcome.RESOLVED:
        return member.target_declaration, PythonReferenceResolutionPath.ONE_FACADE
    if (
        member.unsupported_reason
        is not PythonImportedMemberUnsupportedReason.COMPETING_FACADE_BINDING
        or member.facade is None
        or member.facade_bindings
        or len(member.competing_facade_bindings) != 1
        or member.competing_facade_bindings[0].kind
        is not PythonFacadeCompetingBindingKind.FUNCTION
    ):
        return None, None
    analysis = derive_python_function_declarations(
        snapshot,
        resource_address=member.facade.resource.address,
    )
    matches = tuple(
        item
        for item in analysis.declarations
        if item.declared_name == declaration.imported_name
    )
    if len(matches) != 1:
        return None, None
    span = matches[0].support.source_range
    competing = member.competing_facade_bindings[0].support
    if (
        span.start_line,
        span.start_column_utf8,
        span.end_line,
        span.end_column_utf8,
    ) != (
        competing.start_line,
        competing.start_column_utf8,
        competing.end_line,
        competing.end_column_utf8,
    ) or resolution.matches[0] != member.facade:
        return None, None
    return matches[0], PythonReferenceResolutionPath.DIRECT_MODULE


def _bindings(tree: ast.Module) -> tuple[Counter[str], bool]:  # noqa: C901
    names: Counter[str] = Counter()
    wildcard = False

    def visit(node: ast.AST) -> None:
        nonlocal wildcard
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            names[node.name] += 1
            return
        if isinstance(node, ast.Import | ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    wildcard = True
                else:
                    names[
                        alias.asname
                        or (
                            alias.name
                            if isinstance(node, ast.ImportFrom)
                            else alias.name.split(".")[0]
                        )
                    ] += 1
            return
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store | ast.Del):
            names[node.id] += 1
        if isinstance(node, ast.ExceptHandler) and node.name:
            names[node.name] += 1
        if isinstance(node, ast.MatchAs | ast.MatchStar) and node.name:
            names[node.name] += 1
        if isinstance(node, ast.MatchMapping) and node.rest:
            names[node.rest] += 1
        for child in ast.iter_child_nodes(node):
            visit(child)

    for stmt in tree.body:
        visit(stmt)
    return names, wildcard


def _has_dynamic_binding(tree: ast.Module, local: str) -> bool:
    return any(
        (
            isinstance(node, ast.NamedExpr)
            and isinstance(node.target, ast.Name)
            and node.target.id == local
        )
        or (isinstance(node, ast.Global | ast.Nonlocal) and local in node.names)
        for node in ast.walk(tree)
    )


def _occurrence(
    snapshot: RepositorySnapshot,
    address: RepositoryResourceAddress,
    node: ast.Name,
) -> PythonSourceOccurrence:
    return PythonSourceOccurrence(
        snapshot_id=snapshot.id,
        resource_address=address,
        source_range=PythonSourceRange(
            node.lineno,
            node.col_offset,
            cast("int", node.end_lineno),
            cast("int", node.end_col_offset),
        ),
    )


def _qualified_loads(  # noqa: C901
    tree: ast.Module,
    local: str,
) -> tuple[list[tuple[ast.Name, bool]], list[ast.Name]]:
    calls = {
        id(node.func)
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    supported: list[tuple[ast.Name, bool]] = []
    uncertain: list[ast.Name] = []

    def visit(  # noqa: C901, PLR0912
        node: ast.AST,
        scopes: tuple[tuple[str, Counter[str], bool], ...],
    ) -> None:
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            for expression in (
                *node.decorator_list,
                *node.args.defaults,
                *node.args.kw_defaults,
            ):
                if expression is not None:
                    visit(expression, scopes)
            # Annotation evaluation varies with Python semantics; do not infer it.
            bound = _scope_bindings(node)
            for child in node.body:
                visit(child, (*scopes, ("function", bound, False)))
            return
        if isinstance(node, ast.Lambda):
            bound = _scope_bindings(node)
            visit(node.body, (*scopes, ("function", bound, False)))
            return
        if isinstance(node, ast.ClassDef):
            for expression in (*node.decorator_list, *node.bases):
                visit(expression, scopes)
            for child in node.body:
                visit(child, (*scopes, ("class", Counter(), True)))
            return
        if isinstance(node, ast.AnnAssign):
            visit(node.target, scopes)
            if node.value is not None:
                visit(node.value, scopes)
            return
        if isinstance(
            node,
            ast.ListComp | ast.SetComp | ast.DictComp | ast.GeneratorExp,
        ):
            uncertain.extend(
                child
                for child in ast.walk(node)
                if isinstance(child, ast.Name)
                and isinstance(child.ctx, ast.Load)
                and child.id == local
            )
            return
        if (
            isinstance(node, ast.Name)
            and isinstance(node.ctx, ast.Load)
            and node.id == local
        ):
            if any(
                kind != "function" or bound[local] or blocked
                for kind, bound, blocked in scopes
            ):
                uncertain.append(node)
            else:
                supported.append((node, id(node) in calls))
            return
        for descendant in ast.iter_child_nodes(node):
            visit(descendant, scopes)

    visit(tree, ())
    return supported, uncertain


def _scope_bindings(  # noqa: C901
    node: ast.FunctionDef | ast.AsyncFunctionDef | ast.Lambda,
) -> Counter[str]:
    names: Counter[str] = Counter()
    args = node.args
    for arg in (*args.posonlyargs, *args.args, *args.kwonlyargs):
        names[arg.arg] += 1
    if args.vararg is not None:
        names[args.vararg.arg] += 1
    if args.kwarg is not None:
        names[args.kwarg.arg] += 1

    def visit(current: ast.AST) -> None:  # noqa: C901
        if isinstance(current, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            names[current.name] += 1
            return
        if isinstance(
            current,
            ast.Lambda | ast.ListComp | ast.SetComp | ast.DictComp | ast.GeneratorExp,
        ):
            return
        if isinstance(current, ast.Import | ast.ImportFrom):
            for alias in current.names:
                if alias.name != "*":
                    names[
                        alias.asname
                        or (
                            alias.name
                            if isinstance(current, ast.ImportFrom)
                            else alias.name.split(".")[0]
                        )
                    ] += 1
            return
        if isinstance(current, ast.Name) and isinstance(
            current.ctx,
            ast.Store | ast.Del,
        ):
            names[current.id] += 1
        if isinstance(current, ast.ExceptHandler) and current.name:
            names[current.name] += 1
        if isinstance(current, ast.MatchAs | ast.MatchStar) and current.name:
            names[current.name] += 1
        if isinstance(current, ast.MatchMapping) and current.rest:
            names[current.rest] += 1
        for child in ast.iter_child_nodes(current):
            visit(child)

    for child in node.body if not isinstance(node, ast.Lambda) else (node.body,):
        visit(child)
    return names


def _digest(*values: str) -> str:
    digest = hashlib.sha256()
    for value in values:
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()
