# Copyright (c) 2026
"""One-facade resolution of imported members to direct Python functions."""

from __future__ import annotations

import ast
import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, ClassVar, cast

from devtools.context.python.function.declarations import (
    PythonFunctionDeclarationAnalysis,
    PythonFunctionDeclarationKnowledge,
    derive_python_function_declarations,
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

if TYPE_CHECKING:
    from collections.abc import Sequence

    from devtools.context.python.modules.interpretation import (
        PythonModuleInterpretation,
        PythonModuleInterpretationUniverse,
    )
    from devtools.context.repository.resource import RepositoryResourceAddress
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )

_SEMANTICS = "one-facade-python-imported-member-function-resolution-v1"


class PythonImportedMemberResolutionOutcome(Enum):
    """Classify one bounded imported-member resolution."""

    RESOLVED = "resolved"
    UNRESOLVED_IN_UNIVERSE = "unresolved-in-universe"
    AMBIGUOUS = "ambiguous"
    UNSUPPORTED = "unsupported"


class PythonImportedMemberUnsupportedReason(Enum):
    """Explain why relevant syntax is outside the bounded proposition."""

    SOURCE_NOT_IMPORTED_MEMBER = "source-not-imported-member"
    SOURCE_STAR_IMPORT = "source-star-import"
    SOURCE_MODULE_RESOLUTION = "source-module-resolution-unsupported"
    FACADE_STAR_IMPORT = "facade-star-import"
    NESTED_FACADE_IMPORT = "nested-facade-import"
    COMPETING_FACADE_BINDING = "competing-facade-direct-binding"
    FACADE_MODULE_RESOLUTION = "facade-module-resolution-unsupported"


class PythonFacadeCompetingBindingKind(Enum):
    """Identify only the direct binding forms checked by this slice."""

    IMPORT = "import"
    FUNCTION = "function"
    CLASS = "class"
    ASSIGNMENT = "assignment"


@dataclass(frozen=True, slots=True)
class PythonFacadeBindingSourceOccurrence:
    """Anchor one competing direct facade binding in observed source."""

    snapshot_id: RepositorySnapshotId
    resource_address: RepositoryResourceAddress
    start_line: int
    start_column_utf8: int
    end_line: int
    end_column_utf8: int


@dataclass(frozen=True, slots=True)
class PythonFacadeCompetingBinding:
    """Retain one observed direct facade binding that excludes resolution."""

    name: str
    kind: PythonFacadeCompetingBindingKind
    support: PythonFacadeBindingSourceOccurrence


@dataclass(frozen=True, slots=True)
class PythonImportedMemberResolution:
    """Retain the complete bounded source-to-facade-to-function derivation."""

    source_analysis: PythonImportDeclarationAnalysis
    source_declaration: PythonImportDeclarationKnowledge
    module_universe: PythonModuleInterpretationUniverse
    outcome: PythonImportedMemberResolutionOutcome
    source_module_resolution: PythonImportResolution | None
    facade: PythonModuleInterpretation | None
    facade_analysis: PythonImportDeclarationAnalysis | None
    facade_bindings: tuple[PythonImportDeclarationKnowledge, ...]
    competing_facade_bindings: tuple[PythonFacadeCompetingBinding, ...]
    facade_module_resolution: PythonImportResolution | None
    target: PythonModuleInterpretation | None
    target_function_analysis: PythonFunctionDeclarationAnalysis | None
    target_declarations: tuple[PythonFunctionDeclarationKnowledge, ...]
    unsupported_reason: PythonImportedMemberUnsupportedReason | None

    SEMANTICS: ClassVar[str] = _SEMANTICS

    @property
    def identity(self) -> str:
        """Identify the result without making universe input order semantic."""
        return _digest(
            self.SEMANTICS,
            self.source_declaration.derivation_identity,
            str(self.source_declaration.declaration_ordinal),
            self.module_universe.identity,
            self.outcome.value,
            self.facade.identity if self.facade is not None else "",
            *(
                sorted(
                    item.derivation_identity + ":" + str(item.declaration_ordinal)
                    for item in self.facade_bindings
                )
            ),
            self.target.identity if self.target is not None else "",
            *(sorted(item.identity for item in self.target_declarations)),
            (
                self.unsupported_reason.value
                if self.unsupported_reason is not None
                else ""
            ),
        )

    @property
    def target_declaration(self) -> PythonFunctionDeclarationKnowledge | None:
        """Return the unique target declaration only for a resolved result."""
        if self.outcome is not PythonImportedMemberResolutionOutcome.RESOLVED:
            return None
        return self.target_declarations[0]


def resolve_python_imported_member(  # noqa: PLR0911
    snapshot: RepositorySnapshot,
    source_analysis: PythonImportDeclarationAnalysis,
    source_declaration: PythonImportDeclarationKnowledge,
    *,
    module_universe: PythonModuleInterpretationUniverse,
    source_interpretations: Sequence[PythonModuleInterpretation] = (),
) -> PythonImportedMemberResolution:
    """Resolve one direct imported member through exactly one facade binding.

    This performs no runtime import execution, submodule fallback, recursive
    facade traversal, later-use resolution, or public-export analysis.
    """
    _validate_inputs(
        snapshot=snapshot,
        source_analysis=source_analysis,
        source_declaration=source_declaration,
        module_universe=module_universe,
        source_interpretations=source_interpretations,
    )
    if source_declaration.imported_name is None:
        return _result(
            source_analysis,
            source_declaration,
            module_universe,
            PythonImportedMemberResolutionOutcome.UNSUPPORTED,
            unsupported_reason=(
                PythonImportedMemberUnsupportedReason.SOURCE_NOT_IMPORTED_MEMBER
            ),
        )
    if source_declaration.imported_name == "*":
        return _result(
            source_analysis,
            source_declaration,
            module_universe,
            PythonImportedMemberResolutionOutcome.UNSUPPORTED,
            unsupported_reason=PythonImportedMemberUnsupportedReason.SOURCE_STAR_IMPORT,
        )

    source_resolution = resolve_python_import_declaration(
        source_analysis,
        source_declaration,
        target_universe=module_universe,
        source_interpretations=source_interpretations,
    )
    if source_resolution.outcome is not PythonImportResolutionOutcome.RESOLVED:
        outcome = _import_outcome(source_resolution.outcome)
        return _result(
            source_analysis,
            source_declaration,
            module_universe,
            outcome,
            source_module_resolution=source_resolution,
            unsupported_reason=(
                PythonImportedMemberUnsupportedReason.SOURCE_MODULE_RESOLUTION
                if outcome is PythonImportedMemberResolutionOutcome.UNSUPPORTED
                else None
            ),
        )

    facade = source_resolution.matches[0]
    facade_analysis = derive_python_import_declarations(
        snapshot,
        resource_address=facade.resource.address,
    )
    requested_name = source_declaration.imported_name
    facade_bindings = tuple(
        declaration
        for declaration in facade_analysis.declarations
        if declaration.imported_name not in {None, "*"}
        and (declaration.local_alias or declaration.imported_name) == requested_name
    )
    syntax = _inspect_facade_bindings(
        snapshot=snapshot,
        facade=facade,
        requested_name=requested_name,
    )
    if syntax.star_import:
        return _result(
            source_analysis,
            source_declaration,
            module_universe,
            PythonImportedMemberResolutionOutcome.UNSUPPORTED,
            source_module_resolution=source_resolution,
            facade=facade,
            facade_analysis=facade_analysis,
            facade_bindings=facade_bindings,
            competing_facade_bindings=syntax.competing,
            unsupported_reason=PythonImportedMemberUnsupportedReason.FACADE_STAR_IMPORT,
        )
    if syntax.nested_import:
        return _result(
            source_analysis,
            source_declaration,
            module_universe,
            PythonImportedMemberResolutionOutcome.UNSUPPORTED,
            source_module_resolution=source_resolution,
            facade=facade,
            facade_analysis=facade_analysis,
            facade_bindings=facade_bindings,
            competing_facade_bindings=syntax.competing,
            unsupported_reason=PythonImportedMemberUnsupportedReason.NESTED_FACADE_IMPORT,
        )
    if syntax.competing:
        return _result(
            source_analysis,
            source_declaration,
            module_universe,
            PythonImportedMemberResolutionOutcome.UNSUPPORTED,
            source_module_resolution=source_resolution,
            facade=facade,
            facade_analysis=facade_analysis,
            facade_bindings=facade_bindings,
            competing_facade_bindings=syntax.competing,
            unsupported_reason=(
                PythonImportedMemberUnsupportedReason.COMPETING_FACADE_BINDING
            ),
        )
    if not facade_bindings:
        return _result(
            source_analysis,
            source_declaration,
            module_universe,
            PythonImportedMemberResolutionOutcome.UNRESOLVED_IN_UNIVERSE,
            source_module_resolution=source_resolution,
            facade=facade,
            facade_analysis=facade_analysis,
        )
    if len(facade_bindings) > 1:
        return _result(
            source_analysis,
            source_declaration,
            module_universe,
            PythonImportedMemberResolutionOutcome.AMBIGUOUS,
            source_module_resolution=source_resolution,
            facade=facade,
            facade_analysis=facade_analysis,
            facade_bindings=facade_bindings,
        )

    facade_binding = facade_bindings[0]
    facade_resolution = resolve_python_import_declaration(
        facade_analysis,
        facade_binding,
        target_universe=module_universe,
        source_interpretations=(facade,),
    )
    if facade_resolution.outcome is not PythonImportResolutionOutcome.RESOLVED:
        outcome = _import_outcome(facade_resolution.outcome)
        return _result(
            source_analysis,
            source_declaration,
            module_universe,
            outcome,
            source_module_resolution=source_resolution,
            facade=facade,
            facade_analysis=facade_analysis,
            facade_bindings=facade_bindings,
            facade_module_resolution=facade_resolution,
            unsupported_reason=(
                PythonImportedMemberUnsupportedReason.FACADE_MODULE_RESOLUTION
                if outcome is PythonImportedMemberResolutionOutcome.UNSUPPORTED
                else None
            ),
        )

    target = facade_resolution.matches[0]
    target_analysis = derive_python_function_declarations(
        snapshot,
        resource_address=target.resource.address,
    )
    target_declarations = tuple(
        declaration
        for declaration in target_analysis.declarations
        if declaration.declared_name == facade_binding.imported_name
    )
    outcome = (
        PythonImportedMemberResolutionOutcome.UNRESOLVED_IN_UNIVERSE
        if not target_declarations
        else PythonImportedMemberResolutionOutcome.RESOLVED
        if len(target_declarations) == 1
        else PythonImportedMemberResolutionOutcome.AMBIGUOUS
    )
    return _result(
        source_analysis,
        source_declaration,
        module_universe,
        outcome,
        source_module_resolution=source_resolution,
        facade=facade,
        facade_analysis=facade_analysis,
        facade_bindings=facade_bindings,
        facade_module_resolution=facade_resolution,
        target=target,
        target_function_analysis=target_analysis,
        target_declarations=target_declarations,
    )


@dataclass(frozen=True, slots=True)
class _FacadeSyntax:
    star_import: bool
    nested_import: bool
    competing: tuple[PythonFacadeCompetingBinding, ...]


def _inspect_facade_bindings(
    *,
    snapshot: RepositorySnapshot,
    facade: PythonModuleInterpretation,
    requested_name: str,
) -> _FacadeSyntax:
    tree = ast.parse(facade.resource.content, filename=str(facade.resource.address))
    competing: list[PythonFacadeCompetingBinding] = []
    star_import = False
    nested_import = False
    for node in tree.body:
        support = _support(snapshot, facade, node)
        if isinstance(node, ast.ImportFrom):
            star_import = star_import or any(alias.name == "*" for alias in node.names)
        else:
            kind = _direct_competing_kind(node, requested_name)
            if kind is not None:
                competing.append(PythonFacadeCompetingBinding(
                    name=requested_name,
                    kind=kind,
                    support=support,
                ))
        nested_import = nested_import or _contains_nested_import(node, requested_name)
    return _FacadeSyntax(
        star_import=star_import,
        nested_import=nested_import,
        competing=tuple(competing),
    )


def _direct_competing_kind(
    node: ast.stmt,
    requested_name: str,
) -> PythonFacadeCompetingBindingKind | None:
    if isinstance(node, ast.Import):
        if any(
            (alias.asname or alias.name.split(".", 1)[0]) == requested_name
            for alias in node.names
        ):
            return PythonFacadeCompetingBindingKind.IMPORT
    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        if node.name == requested_name:
            return PythonFacadeCompetingBindingKind.FUNCTION
    elif isinstance(node, ast.ClassDef):
        if node.name == requested_name:
            return PythonFacadeCompetingBindingKind.CLASS
    elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
        targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
        if any(_binds_name(target, requested_name) for target in targets):
            return PythonFacadeCompetingBindingKind.ASSIGNMENT
    return None


def _contains_nested_import(node: ast.stmt, requested_name: str) -> bool:
    return any(
        nested is not node
        and isinstance(nested, ast.ImportFrom)
        and any(
            alias.name == "*" or (alias.asname or alias.name) == requested_name
            for alias in nested.names
        )
        for nested in ast.walk(node)
    )


def _binds_name(target: ast.expr, requested_name: str) -> bool:
    if isinstance(target, ast.Name):
        return target.id == requested_name
    if isinstance(target, (ast.Tuple, ast.List)):
        return any(_binds_name(item, requested_name) for item in target.elts)
    return False


def _support(
    snapshot: RepositorySnapshot,
    facade: PythonModuleInterpretation,
    node: ast.stmt,
) -> PythonFacadeBindingSourceOccurrence:
    return PythonFacadeBindingSourceOccurrence(
        snapshot_id=snapshot.id,
        resource_address=facade.resource.address,
        start_line=node.lineno,
        start_column_utf8=node.col_offset,
        end_line=cast("int", node.end_lineno),
        end_column_utf8=cast("int", node.end_col_offset),
    )


def _validate_inputs(
    *,
    snapshot: RepositorySnapshot,
    source_analysis: PythonImportDeclarationAnalysis,
    source_declaration: PythonImportDeclarationKnowledge,
    module_universe: PythonModuleInterpretationUniverse,
    source_interpretations: Sequence[PythonModuleInterpretation],
) -> None:
    if source_declaration not in source_analysis.declarations:
        msg = "Imported-member declaration does not belong to source analysis."
        raise ValueError(msg)
    if (
        source_analysis.repository_id != snapshot.repository_id
        or source_analysis.snapshot_id != snapshot.id
        or source_analysis.resource
        != snapshot.resource_at(source_analysis.resource.address)
    ):
        msg = "Imported-member source analysis does not match snapshot."
        raise ValueError(msg)
    if module_universe.repository_id != snapshot.repository_id:
        msg = "Imported-member module universe does not match snapshot repository."
        raise ValueError(msg)
    if any(
        item.snapshot_id != snapshot.id
        or item.resource != snapshot.resource_at(item.resource.address)
        for item in module_universe.interpretations
    ):
        msg = "Imported-member module universe contains another snapshot state."
        raise ValueError(msg)
    if any(item.snapshot_id != snapshot.id for item in source_interpretations):
        msg = "Imported-member source interpretation contains another snapshot state."
        raise ValueError(msg)


def _import_outcome(
    outcome: PythonImportResolutionOutcome,
) -> PythonImportedMemberResolutionOutcome:
    return PythonImportedMemberResolutionOutcome(outcome.value)


def _result(  # noqa: PLR0913
    source_analysis: PythonImportDeclarationAnalysis,
    source_declaration: PythonImportDeclarationKnowledge,
    module_universe: PythonModuleInterpretationUniverse,
    outcome: PythonImportedMemberResolutionOutcome,
    *,
    source_module_resolution: PythonImportResolution | None = None,
    facade: PythonModuleInterpretation | None = None,
    facade_analysis: PythonImportDeclarationAnalysis | None = None,
    facade_bindings: tuple[PythonImportDeclarationKnowledge, ...] = (),
    competing_facade_bindings: tuple[PythonFacadeCompetingBinding, ...] = (),
    facade_module_resolution: PythonImportResolution | None = None,
    target: PythonModuleInterpretation | None = None,
    target_function_analysis: PythonFunctionDeclarationAnalysis | None = None,
    target_declarations: tuple[PythonFunctionDeclarationKnowledge, ...] = (),
    unsupported_reason: PythonImportedMemberUnsupportedReason | None = None,
) -> PythonImportedMemberResolution:
    return PythonImportedMemberResolution(
        source_analysis=source_analysis,
        source_declaration=source_declaration,
        module_universe=module_universe,
        outcome=outcome,
        source_module_resolution=source_module_resolution,
        facade=facade,
        facade_analysis=facade_analysis,
        facade_bindings=facade_bindings,
        competing_facade_bindings=competing_facade_bindings,
        facade_module_resolution=facade_module_resolution,
        target=target,
        target_function_analysis=target_function_analysis,
        target_declarations=target_declarations,
        unsupported_reason=unsupported_reason,
    )


def _digest(*values: str) -> str:
    digest = hashlib.sha256()
    for value in values:
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()
