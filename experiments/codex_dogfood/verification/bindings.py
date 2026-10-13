# Copyright (c) 2026
# ruff: noqa: ANN401, EM101, TRY003, S102, COM812 -- sealed local source bindings
"""Bind sealed function bodies to explicit invocation-owned services.

No imported module, class, or production function is patched. The only AST
substitutions accelerate identity reads and exact resource/span lookups.
"""

from __future__ import annotations

import ast
import inspect
import textwrap
from types import SimpleNamespace
from typing import Any


class LookupBindings(ast.NodeTransformer):
    """Preserve every branch and arithmetic expression of historical bodies."""

    def visit_Attribute(self, node: ast.Attribute) -> ast.AST:
        """Route read-only identity properties through the invocation memo."""
        self.generic_visit(node)
        if node.attr == "identity" and isinstance(node.ctx, ast.Load):
            return ast.copy_location(
                ast.Call(ast.Name("_memo_identity", ast.Load()), [node.value], []),
                node,
            )
        return node

    def visit_Call(self, node: ast.Call) -> ast.AST:
        """Route exact snapshot lookup, without changing its address argument."""
        self.generic_visit(node)
        if (
            isinstance(node.func, ast.Name)
            and node.func.id == "next"
            and len(node.args) == 1
            and isinstance(node.args[0], ast.GeneratorExp)
        ):
            expression = ast.unparse(node.args[0])
            replacements = {
                (
                    "(s.stationary_mass for s in ranking.states "
                    "if s.address == e.source)"
                ): "_memo_state(ranking, e.source)",
                (
                    "(e for e in ranking.view.edges if str(e.source) == "
                    "occurrence.source_resource and str(e.target) == "
                    "occurrence.target_resource)"
                ): (
                    "_memo_pair(ranking.view, occurrence.source_resource, "
                    "occurrence.target_resource)"
                ),
                "(r for r in members if str(r) == row.address)": (
                    "_memo_member(members, row.address)"
                ),
            }
            if expression in replacements:
                return ast.copy_location(
                    ast.parse(replacements[expression], mode="eval").body, node
                )
        if isinstance(node.func, ast.Attribute) and node.func.attr == "resource_at":
            return ast.copy_location(
                ast.Call(
                    ast.Name("_memo_resource", ast.Load()),
                    [node.func.value, *node.args],
                    node.keywords,
                ),
                node,
            )
        return node


def bind(function: Any, services: dict[str, Any], *, lookups: bool = False) -> Any:
    """Compile one sealed body into a private globals dictionary."""
    tree = ast.parse(textwrap.dedent(inspect.getsource(function)))
    definition = tree.body[0]
    if not isinstance(definition, (ast.FunctionDef, ast.AsyncFunctionDef)):
        raise TypeError("Function body required")
    definition.decorator_list = []
    if lookups:
        tree = LookupBindings().visit(tree)
    namespace = {**function.__globals__, **services}
    exec(
        compile(ast.fix_missing_locations(tree), inspect.getfile(function), "exec"),
        namespace,
    )
    return namespace[function.__name__]


def module_bindings(
    module: Any, services: dict[str, Any], *, lookups: bool = False
) -> Any:
    """Retain constants/classes; reconnect only this module's function bodies."""
    values = dict(vars(module))
    namespace = SimpleNamespace(**values)
    functions = {
        name: item
        for name, item in values.items()
        if inspect.isfunction(item) and item.__module__ == module.__name__
    }
    for name, function in functions.items():
        setattr(namespace, name, bind(function, services, lookups=lookups))
    for name in functions:
        getattr(namespace, name).__globals__.update(
            {n: getattr(namespace, n) for n in functions} | services,
        )
    for name, value in services.items():
        setattr(namespace, name, value)
    return namespace
