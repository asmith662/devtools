# Copyright (c) 2026
"""Names held outside Name nodes in bounded Python binding inventories."""

from __future__ import annotations

import ast
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator


def non_name_binding(node: ast.AST) -> str | None:
    """Return a pattern capture or handler alias, not a declaration or store.

    This identifies syntax only. A handler alias is cleared on handler exit;
    a pattern capture has different lifetime. Neither establishes a declaration.
    Callers retain their own scope, ordering and conservative ambiguity policy.
    """
    if isinstance(node, ast.ExceptHandler | ast.MatchAs | ast.MatchStar):
        return node.name
    if isinstance(node, ast.MatchMapping):
        return node.rest
    return None


def iter_non_name_bindings(node: ast.AST) -> Iterator[str]:
    """Inspect compound syntax without entering nested function/class scopes.

    This is only the additional string-name inventory. Existing callers own
    ordinary stores, imports, declaration names and source-order cutoffs.
    """
    pending = [node]
    while pending:
        current = pending.pop()
        if isinstance(current, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            continue
        name = non_name_binding(current)
        if name is not None:
            yield name
        pending.extend(reversed(tuple(ast.iter_child_nodes(current))))
