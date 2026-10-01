# Copyright (c) 2026
"""Resolve one observed module's unique direct class or function member."""

from __future__ import annotations

import ast
import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, ClassVar

from devtools.context.python.classes.declarations import (
    PythonClassMethodAnalysis,
    derive_python_class_method_declarations,
)
from devtools.context.python.function.declarations import (
    PythonFunctionDeclarationAnalysis,
    derive_python_function_declarations,
)

if TYPE_CHECKING:
    from devtools.context.python.classes.declarations import (
        PythonClassDeclarationKnowledge,
    )
    from devtools.context.python.function.declarations import (
        PythonFunctionDeclarationKnowledge,
    )
    from devtools.context.python.modules.interpretation import (
        PythonModuleInterpretation,
    )
    from devtools.context.repository.snapshot import RepositorySnapshot

type PythonDirectModuleDeclaration = (
    PythonClassDeclarationKnowledge | PythonFunctionDeclarationKnowledge
)


class PythonModuleDeclarationLookupOutcome(Enum):
    """Classify one bounded direct member lookup."""

    RESOLVED = "resolved"
    UNRESOLVED = "unresolved"
    AMBIGUOUS = "ambiguous"
    NOT_DECLARATION = "not-supported-declaration"


@dataclass(frozen=True, slots=True)
class PythonModuleDeclarationLookup:
    """Retain a direct target or a qualified absence within one observed module."""

    module: PythonModuleInterpretation
    declared_name: str
    function_analysis: PythonFunctionDeclarationAnalysis
    class_analysis: PythonClassMethodAnalysis
    outcome: PythonModuleDeclarationLookupOutcome
    target: PythonDirectModuleDeclaration | None

    SEMANTICS: ClassVar[str] = "direct-observed-python-module-declaration-lookup-v1"

    @property
    def identity(self) -> str:
        """Bind the lookup to exact source and bounded analysis dependencies."""
        return _digest(
            self.SEMANTICS,
            self.module.identity,
            self.declared_name,
            self.function_analysis.derivation.identity,
            self.class_analysis.derivation.identity,
            self.outcome.value,
            self.target.identity if self.target else "",
        )


def lookup_python_module_declaration(  # noqa: C901, PLR0912, PLR0915
    snapshot: RepositorySnapshot,
    *,
    module: PythonModuleInterpretation,
    declared_name: str,
) -> PythonModuleDeclarationLookup:
    """Resolve only one unique undecorated direct declaration binding.

    Competing, nested, wildcard, and dynamic bindings do not establish a
    target. This is static repository syntax, never runtime attribute lookup.
    """
    if not declared_name.isidentifier():
        msg = "Direct member name must be a Python identifier."
        raise ValueError(msg)
    if (
        module.repository_id != snapshot.repository_id
        or module.snapshot_id != snapshot.id
        or module.resource != snapshot.resource_at(module.resource.address)
    ):
        msg = "Direct member module differs from the supplied snapshot."
        raise ValueError(msg)
    address = module.resource.address
    functions = derive_python_function_declarations(snapshot, resource_address=address)
    classes = derive_python_class_method_declarations(
        snapshot,
        resource_address=address,
    )
    tree = ast.parse(module.resource.content, filename=str(address))
    candidates: list[PythonDirectModuleDeclaration | None] = []
    uncertain = False
    for node in tree.body:
        if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
            if node.name == declared_name:
                if node.decorator_list:
                    candidates.append(None)
                elif isinstance(node, ast.ClassDef):
                    candidates.extend(
                        item
                        for item in classes.classes
                        if item.support.source_range.start_line == node.lineno
                        and item.support.source_range.start_column_utf8
                        == node.col_offset
                    )
                else:
                    candidates.extend(
                        item
                        for item in functions.declarations
                        if item.support.source_range.start_line == node.lineno
                        and item.support.source_range.start_column_utf8
                        == node.col_offset
                    )
            continue
        if isinstance(node, ast.Import | ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    uncertain = True
                elif (
                    alias.asname
                    or (
                        alias.name
                        if isinstance(node, ast.ImportFrom)
                        else alias.name.split(".")[0]
                    )
                ) == declared_name:
                    candidates.append(None)
            continue
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and isinstance(
                child.ctx,
                ast.Store | ast.Del,
            ):
                if child.id == declared_name:
                    candidates.append(None)
            elif isinstance(
                child,
                ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef,
            ):
                if child.name == declared_name:
                    candidates.append(None)
            elif isinstance(child, ast.Import | ast.ImportFrom):
                for alias in child.names:
                    if alias.name == "*":
                        uncertain = True
                    elif (
                        alias.asname
                        or (
                            alias.name
                            if isinstance(child, ast.ImportFrom)
                            else alias.name.split(".")[0]
                        )
                    ) == declared_name:
                        candidates.append(None)
    if any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in {"exec", "globals", "locals"}
        for node in ast.walk(tree)
    ):
        uncertain = True
    if uncertain or len(candidates) > 1:
        outcome = PythonModuleDeclarationLookupOutcome.AMBIGUOUS
        target = None
    elif not candidates:
        outcome = PythonModuleDeclarationLookupOutcome.UNRESOLVED
        target = None
    elif candidates[0] is None:
        outcome = PythonModuleDeclarationLookupOutcome.NOT_DECLARATION
        target = None
    else:
        outcome = PythonModuleDeclarationLookupOutcome.RESOLVED
        target = candidates[0]
    return PythonModuleDeclarationLookup(
        module,
        declared_name,
        functions,
        classes,
        outcome,
        target,
    )


def _digest(*values: str) -> str:
    digest = hashlib.sha256()
    for value in values:
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()
