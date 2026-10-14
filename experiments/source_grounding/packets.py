# Copyright (c) 2026
# ruff: noqa: ANN401, C901, PLR0912 -- two fixed audited serializer branches
"""Specialize the frozen packet codec to one blinded branch before disclosure.

This bounded source projection removes the other branch entirely. It accepts
only the pinned repository codec, never worker-authored code. It is not a workflow
DSL or model transformation; all judgment semantics remain in the authored codec.
"""

from __future__ import annotations

import ast
from typing import Any

from experiments.orchestration.storage import require


def builder(raw: bytes, *, gold: bool) -> bytes:
    """Retain only the selected branch and its necessary semantic vocabulary."""
    tree = ast.parse(raw)
    packet_schema = (
        "blind-semantic-gold-packet-v1" if gold else "source-grounding-packet-v1"
    )
    found = set()
    nodes = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == ("VERDICTS" if gold else "LABELS")
            for t in node.targets
        ):
            continue
        if isinstance(node, ast.FunctionDef) and node.name == "minimal" and not gold:
            continue
        if isinstance(node, ast.FunctionDef) and node.name == "packet":
            body = []
            for statement in node.body:
                if (
                    isinstance(statement, ast.If)
                    and ast.unparse(statement.test)
                    == "p['schema'] == 'source-grounding-packet-v1'"
                ):
                    body.extend(statement.orelse if gold else statement.body)
                    found.add("packet")
                else:
                    body.append(statement)
            node.body = body
        if isinstance(node, ast.FunctionDef) and node.name == "validate":
            body = []
            for statement in node.body:
                if isinstance(statement, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id == "gold"
                    for t in statement.targets
                ):
                    statement.value = ast.Constant(value=gold)
                if (
                    isinstance(statement, ast.If)
                    and ast.unparse(statement.test) == "not gold"
                ):
                    found.add("validate")
                    if not gold:
                        body.extend(statement.body)
                        break  # The grounding branch returns; no gold code survives.
                else:
                    body.append(statement)
            node.body = body
        nodes.append(node)
    tree.body = nodes

    class Vocabulary(ast.NodeTransformer):
        def visit_IfExp(self, node: ast.IfExp) -> Any:
            """Fold only the named, fixed branch selector."""
            if isinstance(node.test, ast.Name) and node.test.id == "gold":
                return self.visit(node.body if gold else node.orelse)
            return self.generic_visit(node)

        def visit_Set(self, node: ast.Set) -> Any:
            """Make packet acceptance single-schema rather than expose its sibling."""
            if {e.value for e in node.elts if isinstance(e, ast.Constant)} == {
                "source-grounding-packet-v1",
                "blind-semantic-gold-packet-v1",
            }:
                node.elts = [ast.Constant(value=packet_schema)]
            return self.generic_visit(node)

    tree = Vocabulary().visit(tree)
    tree.body[0] = ast.Expr(
        value=ast.Constant(
            value="Frozen standalone packet-only primary serializer; stdlib only.",
        ),
    )
    result = (ast.unparse(ast.fix_missing_locations(tree)) + "\n").encode()
    require(
        found == {"packet", "validate"},
        "Reviewer codec shape changed; audit disclosure projection",
    )
    forbidden = (
        (b"GROUNDED_SOURCE", b"GPT-6 Sol", b"source-grounding")
        if gold
        else (b"REQUIRED", b"HELPFUL_ONLY", b"GPT-6 Astra", b"conditional_repository")
    )
    require(
        not any(word in result for word in forbidden),
        "Cross-branch reviewer code leakage",
    )
    return result
