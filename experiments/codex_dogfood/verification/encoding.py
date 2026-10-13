# Copyright (c) 2026
# ruff: noqa: ANN401, COM812 -- exact historical codec boundary
"""Invocation-local native node templates with exact historical graph encoding.

Node content is projected once. Each envelope assigns its own DFS ordinals and
renders reference bindings; these ordinals must never become cross-return trust.
"""

from __future__ import annotations

import re
from dataclasses import is_dataclass
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import json_bytes


class GraphEncoding:
    """Retain strong native references and exact unique-node projections locally."""

    def __init__(self, memo: Any) -> None:
        """Retain templates only in this experiment invocation."""
        self.memo = memo
        self.nodes: dict[
            int, tuple[Any, tuple[Any, ...], tuple[bytes, ...], tuple[Any, ...]]
        ] = {}
        self.projected = 0
        self.hits = 0
        self.bindings = 0

    def node(self, item: Any) -> Any:
        """Project the exact ordered native field/item/value surface."""
        mutable = isinstance(item, (dict, list)) or (
            is_dataclass(item) and not vars(type(item))["__dataclass_params__"].frozen
        )
        cached = self.nodes.get(id(item))
        if cached is not None and not mutable:
            self.hits += 1
            return cached
        children: list[Any] = []

        def reference(value: Any) -> Any:
            if value is None or type(value) in (bool, int, float, str):
                return value
            children.append(value)
            return {"ref": -len(children)}

        kind, value = self.memo.description(item)
        node: dict[str, Any] = {
            "type": type(item).__module__ + "." + type(item).__qualname__
        }
        if kind == "fields":
            node["fields"] = {name: reference(child) for name, child in value}
        elif kind == "mapping":
            node["items"] = [[reference(k), reference(v)] for k, v in value]
        elif kind == "items":
            node["items"] = [reference(v) for v in value]
        else:
            node["value"] = value
        raw = b"    " + json_bytes(node).rstrip(b"\n").replace(b"\n", b"\n    ")
        parts: list[bytes] = []
        ordered: list[Any] = []
        start = 0
        matches = () if kind == "value" else re.finditer(rb'"ref": (-[1-9][0-9]*)', raw)
        for match in matches:
            parts.append(raw[start : match.start(1)])
            ordered.append(children[-int(match[1]) - 1])
            start = match.end(1)
        parts.append(raw[start:])
        result = (item, tuple(children), tuple(parts), tuple(ordered))
        self.projected += 1
        self.memo.recursive_visits += 1
        self.memo.unique_nodes[id(item)] = item
        if not mutable:
            self.nodes[id(item)] = result
        return result

    def encode(self, root: Any) -> bytes:
        """Preserve exact type, field/item order, primitive bytes and aliases."""
        if root is None or type(root) in (bool, int, float, str):
            return json_bytes(
                {"nodes": [], "root": root, "schema": "case-0012-native-graph-v1"}
            )
        seen: dict[int, int] = {}
        records: list[Any] = []
        stack = [root]
        while stack:
            item = stack.pop()
            if id(item) in seen:
                continue
            seen[id(item)] = len(records)
            record = self.node(item)
            records.append(record)
            stack.extend(reversed(record[1]))
        ordinals = [str(i).encode("ascii") for i in range(len(records))]
        rendered: list[bytes] = []
        for _, _, parts, children in records:
            if not children:
                rendered.append(parts[0])
            else:
                fragments: list[bytes] = []
                for part, child in zip(parts, children, strict=False):
                    fragments.extend((part, ordinals[seen[id(child)]]))
                fragments.append(parts[-1])
                rendered.append(b"".join(fragments))
        self.bindings += len(records)
        self.memo.nodes_checked += len(records)
        return (
            b'{\n  "nodes": [\n'
            + b",\n".join(rendered)
            + b'\n  ],\n  "root": {\n    "ref": 0\n  },\n'
            + b'  "schema": "case-0012-native-graph-v1"\n}\n'
        )
