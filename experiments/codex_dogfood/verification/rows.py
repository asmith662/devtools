# Copyright (c) 2026
# ruff: noqa: ANN401, EM101, TRY003, S102 -- exact sealed-body adapter
"""Exact historical row totals from one canonical pair ordering."""

from __future__ import annotations

import ast
import inspect
import math
import textwrap
from typing import Any

from .bindings import LookupBindings


def totals(weights: dict[Any, float], nodes: tuple[Any, ...]) -> dict[Any, float]:
    """Preserve sorted(key=str) addition order separately from published edge order."""
    outgoing: dict[Any, list[float]] = {}
    for (source, _), weight in sorted(weights.items(), key=str):
        outgoing.setdefault(source, []).append(weight)
    return {node: math.fsum(outgoing.get(node, ())) for node in nodes}


def build(function: Any, services: dict[str, Any]) -> Any:
    """Replace exactly the historical totals comprehension, preserving other checks."""
    tree = ast.parse(textwrap.dedent(inspect.getsource(function)))
    substitutions = 0
    definition = tree.body[0]
    if not isinstance(definition, ast.FunctionDef):
        raise TypeError("Function body required")
    for statement in definition.body:
        if (
            isinstance(statement, ast.Assign)
            and isinstance(statement.targets[0], ast.Name)
            and statement.targets[0].id == "totals"
        ):
            statement.value = ast.Call(
                ast.Name("_row_totals", ast.Load()),
                [ast.Name("weights", ast.Load()), ast.Name("nodes", ast.Load())],
                [],
            )
            substitutions += 1
    if substitutions != 1:
        raise ValueError("Historical row-total binding shape changed")
    namespace = {**function.__globals__, **services, "_row_totals": totals}
    exec(
        compile(
            ast.fix_missing_locations(LookupBindings().visit(tree)),
            inspect.getfile(function),
            "exec",
        ),
        namespace,
    )
    return namespace[function.__name__]
