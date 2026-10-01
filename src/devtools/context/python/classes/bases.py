# Copyright (c) 2026
"""Snapshot-bound, bounded resolution of direct Python class base syntax."""

from __future__ import annotations

import ast
import hashlib
from dataclasses import dataclass, replace
from enum import Enum
from typing import TYPE_CHECKING, ClassVar

from devtools.context.python.classes.containment import (
    build_python_class_method_containment_view,
)
from devtools.context.python.classes.declarations import (
    PythonClassDeclarationKnowledge,
    PythonClassMethodAnalysis,
)
from devtools.context.python.imports.declarations import (
    PythonImportDeclarationAnalysis,
    PythonImportDeclarationKnowledge,
    derive_python_import_declarations,
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

if TYPE_CHECKING:
    from devtools.context.python.classes.declarations import (
        PythonClassBaseSyntax,
        PythonClassMethodAnalysisAggregate,
    )
    from devtools.context.python.modules.interpretation import (
        PythonModuleInterpretation,
        PythonModuleInterpretationUniverse,
    )
    from devtools.context.repository.snapshot import RepositorySnapshot

_SEMANTICS = "bounded-direct-python-class-base-v1"


class PythonDirectBaseOutcome(Enum):
    """One assessment for every retained direct base expression."""

    RESOLVED = "resolved"
    UNSUPPORTED_EXPRESSION = "unsupported-expression"
    UNRESOLVED_BINDING = "unresolved-binding"
    AMBIGUOUS_BINDING = "ambiguous-binding"
    UNSUPPORTED_BINDING = "unsupported-binding"
    UNRESOLVED_MODULE = "unresolved-module"
    AMBIGUOUS_MODULE = "ambiguous-module"
    UNSUPPORTED_MODULE = "unsupported-module"
    UNRESOLVED_TARGET = "unresolved-target"
    AMBIGUOUS_TARGET = "ambiguous-target"
    TARGET_NOT_CLASS = "target-not-class"


class PythonDirectBaseRoute(Enum):
    """The bounded source-to-target route used by a positive assessment."""

    LOCAL_CLASS = "local-class"
    IMPORTED_MEMBER = "imported-member"
    IMPORTED_MODULE_ATTRIBUTE = "imported-module-attribute"


@dataclass(frozen=True, slots=True)
class PythonDirectBaseAssessment:
    """Assess one exact base expression; only RESOLVED establishes a relation."""

    child_analysis: PythonClassMethodAnalysis
    child: PythonClassDeclarationKnowledge
    base: PythonClassBaseSyntax
    module_universe_identity: str
    outcome: PythonDirectBaseOutcome
    route: PythonDirectBaseRoute | None = None
    target_analysis: PythonClassMethodAnalysis | None = None
    target: PythonClassDeclarationKnowledge | None = None
    import_declaration: PythonImportDeclarationKnowledge | None = None
    import_resolution: PythonImportResolution | None = None
    direct_member_resolution: PythonModuleDeclarationLookup | None = None

    SEMANTICS: ClassVar[str] = _SEMANTICS

    @property
    def identity(self) -> str:
        """Bind the result to syntax, both resources, and resolution support."""
        span = self.base.occurrence.source_range
        return _digest(
            self.SEMANTICS,
            self.child.identity,
            self.child_analysis.derivation.identity,
            str(self.base.ordinal),
            str(span.start_line),
            str(span.start_column_utf8),
            str(span.end_line),
            str(span.end_column_utf8),
            self.base.source_text,
            self.module_universe_identity,
            self.outcome.value,
            self.route.value if self.route else "",
            self.target.identity if self.target else "",
            self.target_analysis.derivation.identity if self.target_analysis else "",
            (
                self.import_declaration.derivation_identity
                if self.import_declaration
                else ""
            ),
            str(self.import_declaration.declaration_ordinal)
            if self.import_declaration
            else "",
            self.import_resolution.identity if self.import_resolution else "",
            self.direct_member_resolution.identity
            if self.direct_member_resolution
            else "",
        )


@dataclass(frozen=True, slots=True)
class PythonDirectBaseAnalysis:
    """Ordered assessments over validated source analyses and a module universe."""

    aggregate: PythonClassMethodAnalysisAggregate
    module_universe: PythonModuleInterpretationUniverse
    assessments: tuple[PythonDirectBaseAssessment, ...]

    def direct_bases_of(
        self,
        child: PythonClassDeclarationKnowledge,
    ) -> tuple[PythonDirectBaseAssessment, ...]:
        """Return established direct bases in syntax order; reject unknown child."""
        if child not in self.aggregate.classes:
            msg = "Child class is outside the analyzed selection."
            raise ValueError(msg)
        return tuple(
            item
            for item in self.assessments
            if item.child == child and item.outcome is PythonDirectBaseOutcome.RESOLVED
        )

    def direct_subclasses_of(
        self,
        base: PythonClassDeclarationKnowledge,
    ) -> tuple[PythonDirectBaseAssessment, ...]:
        """Project the same positive assessments backward in deterministic order."""
        if base not in self.aggregate.classes and not any(
            item.target == base for item in self.assessments
        ):
            msg = "Base class is outside the analyzed universe."
            raise ValueError(msg)
        return tuple(
            item
            for item in self.assessments
            if item.target == base and item.outcome is PythonDirectBaseOutcome.RESOLVED
        )


@dataclass(frozen=True, slots=True)
class _Binding:
    name: str
    kind: str
    declaration: PythonImportDeclarationKnowledge | None = None
    class_declaration: PythonClassDeclarationKnowledge | None = None


def derive_python_direct_bases(
    snapshot: RepositorySnapshot,
    *,
    aggregate: PythonClassMethodAnalysisAggregate,
    module_universe: PythonModuleInterpretationUniverse,
) -> PythonDirectBaseAnalysis:
    """Assess each selected class base using only retained snapshot state.

    Local and target bindings are direct module-body syntax. Conditional,
    competing, wildcard, and unsupported bindings prevent a positive claim.
    No runtime Python evaluator, facade traversal, or transitive inference runs.
    """
    build_python_class_method_containment_view(snapshot, aggregate=aggregate)
    if module_universe.repository_id != snapshot.repository_id or any(
        item.snapshot_id != snapshot.id
        or item.resource != snapshot.resource_at(item.resource.address)
        for item in module_universe.interpretations
    ):
        msg = "Base-resolution module universe differs from the snapshot."
        raise ValueError(msg)
    assessments: list[PythonDirectBaseAssessment] = []
    for analysis in aggregate.analyses:
        address = analysis.derivation.dependency.resource.address
        source_imports = derive_python_import_declarations(
            snapshot,
            resource_address=address,
        )
        tree = ast.parse(analysis.derivation.dependency.resource.content)
        source_interpretations = tuple(
            item
            for item in module_universe.interpretations
            if item.resource.address == address
        )
        for child in analysis.classes:
            bindings = _bindings(
                tree,
                analysis,
                source_imports.declarations,
                before_line=child.support.source_range.start_line,
            )
            assessments.extend(
                _assess(
                    snapshot,
                    analysis,
                    child,
                    base,
                    bindings,
                    source_imports,
                    source_interpretations,
                    module_universe,
                )
                for base in child.base_syntax
            )
    return PythonDirectBaseAnalysis(aggregate, module_universe, tuple(assessments))


def _assess(  # noqa: C901, PLR0911, PLR0912, PLR0913, PLR0917
    snapshot: RepositorySnapshot,
    child_analysis: PythonClassMethodAnalysis,
    child: PythonClassDeclarationKnowledge,
    base: PythonClassBaseSyntax,
    bindings: tuple[_Binding, ...],
    source_imports: PythonImportDeclarationAnalysis,
    source_interpretations: tuple[PythonModuleInterpretation, ...],
    universe: PythonModuleInterpretationUniverse,
) -> PythonDirectBaseAssessment:
    expression = ast.parse(base.source_text, mode="eval").body
    names = _attribute_parts(expression)
    result = PythonDirectBaseAssessment(
        child_analysis=child_analysis,
        child=child,
        base=base,
        module_universe_identity=universe.identity,
        outcome=PythonDirectBaseOutcome.UNRESOLVED_BINDING,
    )
    if names is None:
        return replace(result, outcome=PythonDirectBaseOutcome.UNSUPPORTED_EXPRESSION)
    matches = tuple(item for item in bindings if item.name == names[0])
    if any(item.kind == "wildcard" for item in bindings):
        return replace(result, outcome=PythonDirectBaseOutcome.AMBIGUOUS_BINDING)
    if not matches:
        return result
    if len(matches) != 1:
        return replace(result, outcome=PythonDirectBaseOutcome.AMBIGUOUS_BINDING)
    binding = matches[0]
    if binding.kind == "class" and len(names) == 1:
        return replace(
            result,
            outcome=PythonDirectBaseOutcome.RESOLVED,
            route=PythonDirectBaseRoute.LOCAL_CLASS,
            target_analysis=child_analysis,
            target=binding.class_declaration,
        )
    declaration = binding.declaration
    if binding.kind != "import" or declaration is None:
        return replace(result, outcome=PythonDirectBaseOutcome.UNSUPPORTED_BINDING)
    resolution = resolve_python_import_declaration(
        source_imports,
        declaration,
        target_universe=universe,
        source_interpretations=source_interpretations,
    )
    result = replace(
        result,
        import_declaration=declaration,
        import_resolution=resolution,
    )
    if resolution.outcome is not PythonImportResolutionOutcome.RESOLVED:
        outcome = {
            PythonImportResolutionOutcome.UNRESOLVED_IN_UNIVERSE: (
                PythonDirectBaseOutcome.UNRESOLVED_MODULE
            ),
            PythonImportResolutionOutcome.AMBIGUOUS: (
                PythonDirectBaseOutcome.AMBIGUOUS_MODULE
            ),
            PythonImportResolutionOutcome.UNSUPPORTED: (
                PythonDirectBaseOutcome.UNSUPPORTED_MODULE
            ),
        }[resolution.outcome]
        return replace(result, outcome=outcome)
    if declaration.imported_name is not None and len(names) == 1:
        target_name = declaration.imported_name
        route = PythonDirectBaseRoute.IMPORTED_MEMBER
    elif declaration.imported_name is None and len(names) > 1:
        prefix = (declaration.local_alias or declaration.module or "").split(".")
        if declaration.local_alias is None:
            prefix = (declaration.module or "").split(".")
        if tuple(names[:-1]) != tuple(prefix):
            return replace(result, outcome=PythonDirectBaseOutcome.UNSUPPORTED_BINDING)
        target_name = names[-1]
        route = PythonDirectBaseRoute.IMPORTED_MODULE_ATTRIBUTE
    else:
        return replace(result, outcome=PythonDirectBaseOutcome.UNSUPPORTED_BINDING)
    target_module = resolution.matches[0]
    member = lookup_python_module_declaration(
        snapshot,
        module=target_module,
        declared_name=target_name,
    )
    target_analysis = member.class_analysis
    result = replace(
        result,
        target_analysis=target_analysis,
        direct_member_resolution=member,
    )
    if member.outcome is not PythonModuleDeclarationLookupOutcome.RESOLVED:
        outcome = {
            PythonModuleDeclarationLookupOutcome.UNRESOLVED: (
                PythonDirectBaseOutcome.UNRESOLVED_TARGET
            ),
            PythonModuleDeclarationLookupOutcome.AMBIGUOUS: (
                PythonDirectBaseOutcome.AMBIGUOUS_TARGET
            ),
            PythonModuleDeclarationLookupOutcome.NOT_DECLARATION: (
                PythonDirectBaseOutcome.TARGET_NOT_CLASS
            ),
        }[member.outcome]
        return replace(result, outcome=outcome)
    target = member.target
    if not isinstance(target, PythonClassDeclarationKnowledge):
        return replace(result, outcome=PythonDirectBaseOutcome.TARGET_NOT_CLASS)
    return replace(
        result,
        outcome=PythonDirectBaseOutcome.RESOLVED,
        route=route,
        target=target,
    )


def _attribute_parts(node: ast.expr) -> tuple[str, ...] | None:
    if isinstance(node, ast.Name):
        return (node.id,)
    if isinstance(node, ast.Attribute):
        parts = _attribute_parts(node.value)
        return (*parts, node.attr) if parts is not None else None
    return None


def _bindings(
    tree: ast.Module,
    analysis: PythonClassMethodAnalysis,
    imports: tuple[PythonImportDeclarationKnowledge, ...],
    *,
    before_line: int | None = None,
) -> tuple[_Binding, ...]:
    values: list[_Binding] = []
    for node in tree.body:
        if before_line is not None and node.lineno >= before_line:
            break
        if isinstance(node, ast.ClassDef):
            declaration = next(
                (
                    item
                    for item in analysis.classes
                    if item.support.source_range.start_line == node.lineno
                    and item.support.source_range.start_column_utf8 == node.col_offset
                ),
                None,
            )
            values.append(
                _Binding(
                    node.name,
                    "other" if node.decorator_list else "class",
                    class_declaration=declaration if not node.decorator_list else None,
                ),
            )
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            declarations = tuple(
                item
                for item in imports
                if item.support.start_line == node.lineno
                and item.support.start_column_utf8 == node.col_offset
            )
            for alias, import_declaration in zip(
                node.names,
                declarations,
                strict=True,
            ):
                name = alias.asname or (
                    alias.name
                    if isinstance(node, ast.ImportFrom)
                    else alias.name.split(".")[0]
                )
                values.append(
                    _Binding(
                        name,
                        "import",
                        declaration=import_declaration,
                    ),
                )
                if alias.name == "*":
                    values.append(_Binding("*", "wildcard"))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            values.append(_Binding(node.name, "other"))
        else:
            values.extend(
                _Binding(child.id, "other")
                for child in ast.walk(node)
                if isinstance(child, ast.Name)
                and isinstance(child.ctx, (ast.Store, ast.Del))
            )
            values.extend(
                _Binding(parts[0], "other")
                for child in ast.walk(node)
                if isinstance(child, ast.Attribute)
                and isinstance(child.ctx, (ast.Store, ast.Del))
                if (parts := _attribute_parts(child)) is not None
            )
            values.extend(
                _Binding(child.name, "other")
                for child in ast.walk(node)
                if child is not node
                and isinstance(
                    child,
                    (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef),
                )
            )
            values.extend(
                _Binding(
                    alias.asname
                    or (
                        alias.name
                        if isinstance(child, ast.ImportFrom)
                        else alias.name.split(".")[0]
                    ),
                    "other",
                )
                for child in ast.walk(node)
                if isinstance(child, (ast.Import, ast.ImportFrom))
                for alias in child.names
                if alias.name != "*"
            )
            if any(
                isinstance(child, ast.ImportFrom)
                and any(alias.name == "*" for alias in child.names)
                for child in ast.walk(node)
            ):
                values.append(_Binding("*", "wildcard"))
    return tuple(values)


def _digest(*values: str) -> str:
    digest = hashlib.sha256()
    for value in values:
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()
