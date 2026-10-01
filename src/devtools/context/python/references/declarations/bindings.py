# Copyright (c) 2026
"""Bounded direct module bindings and lexical scope checks for References."""

from __future__ import annotations

import ast
from collections import Counter
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.context.python.classes.declarations import (
        PythonClassDeclarationKnowledge,
    )
    from devtools.context.python.function.declarations import (
        PythonFunctionDeclarationKnowledge,
    )
    from devtools.context.python.imports.declarations import (
        PythonImportDeclarationAnalysis,
        PythonImportDeclarationKnowledge,
    )
    from devtools.context.python.references.declarations.model import (
        PythonReferenceTarget,
    )


@dataclass(frozen=True, slots=True)
class _Binding:
    name: str
    kind: str
    line: int
    declaration: PythonReferenceTarget | None = None
    import_declaration: PythonImportDeclarationKnowledge | None = None


def _module_bindings(  # noqa: C901, PLR0912
    tree: ast.Module,
    imports: PythonImportDeclarationAnalysis,
    functions: tuple[PythonFunctionDeclarationKnowledge, ...],
    classes: tuple[PythonClassDeclarationKnowledge, ...],
) -> tuple[tuple[_Binding, ...], bool]:
    values: list[_Binding] = []
    uncertain = False
    for node in tree.body:
        if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
            declarations: tuple[PythonReferenceTarget, ...] = (
                classes if isinstance(node, ast.ClassDef) else functions
            )
            target = next(
                (
                    item
                    for item in declarations
                    if item.support.source_range.start_line == node.lineno
                    and item.support.source_range.start_column_utf8 == node.col_offset
                ),
                None,
            )
            values.append(
                _Binding(
                    node.name,
                    "other"
                    if node.decorator_list
                    else ("class" if isinstance(node, ast.ClassDef) else "function"),
                    node.lineno,
                    target if not node.decorator_list else None,
                ),
            )
        elif isinstance(node, ast.Import | ast.ImportFrom):
            import_declarations = tuple(
                item
                for item in imports.declarations
                if item.support.start_line == node.lineno
                and item.support.start_column_utf8 == node.col_offset
            )
            for alias, import_declaration in zip(
                node.names,
                import_declarations,
                strict=True,
            ):
                if alias.name == "*":
                    uncertain = True
                    continue
                name = alias.asname or (
                    alias.name
                    if isinstance(node, ast.ImportFrom)
                    else alias.name.split(".")[0]
                )
                values.append(
                    _Binding(
                        name,
                        "imported-member"
                        if isinstance(node, ast.ImportFrom)
                        else "imported-module",
                        node.lineno,
                        import_declaration=import_declaration,
                    ),
                )
        else:
            for child in ast.walk(node):
                if isinstance(child, ast.Name) and isinstance(
                    child.ctx,
                    ast.Store | ast.Del,
                ):
                    values.append(_Binding(child.id, "other", node.lineno))
                elif isinstance(
                    child,
                    ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef,
                ):
                    values.append(_Binding(child.name, "other", node.lineno))
                elif isinstance(child, ast.Import | ast.ImportFrom):
                    for alias in child.names:
                        if alias.name == "*":
                            uncertain = True
                        else:
                            name = alias.asname or (
                                alias.name
                                if isinstance(child, ast.ImportFrom)
                                else alias.name.split(".")[0]
                            )
                            values.append(_Binding(name, "other", node.lineno))
    uncertain = uncertain or any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in {"exec", "globals", "locals"}
        for node in ast.walk(tree)
    )
    return tuple(values), uncertain


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


def _ancestors(node: ast.AST, parents: dict[ast.AST, ast.AST]) -> tuple[ast.AST, ...]:
    values: list[ast.AST] = []
    current = node
    while current in parents:
        current = parents[current]
        values.append(current)
    return tuple(values)


def _unsupported_scope(node: ast.AST, parents: dict[ast.AST, ast.AST]) -> bool:
    ancestors = _ancestors(node, parents)
    if any(
        isinstance(
            item,
            (ast.Lambda, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp),
        )
        for item in ancestors
    ):
        return True
    if any(isinstance(item, ast.arg) for item in ancestors):
        return True
    if any(
        isinstance(item, ast.ClassDef)
        and not any(
            isinstance(inner, ast.FunctionDef | ast.AsyncFunctionDef)
            for inner in ancestors[: ancestors.index(item)]
        )
        and item is not parents.get(node)
        for item in ancestors
    ):
        return True
    return any(
        isinstance(item, ast.FunctionDef | ast.AsyncFunctionDef)
        and not _within_body(node, item, parents)
        for item in ancestors
    )


def _within_body(
    node: ast.AST,
    scope: ast.AST,
    parents: dict[ast.AST, ast.AST],
) -> bool:
    current = node
    while current in parents and parents[current] is not scope:
        current = parents[current]
    return current in getattr(scope, "body", ())


def _shadowed(node: ast.AST, parents: dict[ast.AST, ast.AST], root: str) -> bool:
    return any(
        isinstance(item, ast.FunctionDef | ast.AsyncFunctionDef)
        and _scope_bindings(item)[root] > 0
        for item in _ancestors(node, parents)
    )


def _at_module_scope(node: ast.AST, parents: dict[ast.AST, ast.AST]) -> bool:
    return not any(
        isinstance(item, ast.FunctionDef | ast.AsyncFunctionDef | ast.Lambda)
        for item in _ancestors(node, parents)
    )
