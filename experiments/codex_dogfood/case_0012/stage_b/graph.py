# Copyright (c) 2026
# ruff: noqa: COM812 -- bounded native audit codec
"""Canonical complete native graph description; no domain semantics change."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from enum import Enum
from pathlib import PurePath
from typing import Any

from devtools.core.identity import Identity
from experiments.codex_dogfood.case_0012.stage_b.canonical import NativeEncoder


def describe(value: object) -> dict[str, Any]:
    """Retain every field, primitive, container order, native type and alias."""
    nodes: list[dict[str, Any]] = []
    seen: dict[int, int] = {}

    def visit(item: object) -> object:
        if item is None or type(item) in (bool, int, float, str):
            return item
        if id(item) in seen:
            return {"ref": seen[id(item)]}
        ordinal = len(nodes)
        seen[id(item)] = ordinal
        node: dict[str, Any] = {
            "type": type(item).__module__ + "." + type(item).__qualname__
        }
        nodes.append(node)
        if isinstance(item, dict):
            node["items"] = [[visit(k), visit(v)] for k, v in item.items()]
        elif isinstance(item, (tuple, list)):
            node["items"] = [visit(v) for v in item]
        elif isinstance(item, (Identity, PurePath, Enum)):
            node["value"] = NativeEncoder().default(item)
        elif is_dataclass(item) and not isinstance(item, type):
            node["fields"] = {
                f.name: visit(getattr(item, f.name)) for f in fields(item)
            }
        else:
            node["value"] = NativeEncoder().default(item)
        return {"ref": ordinal}

    root = visit(value)
    return {"schema": "case-0012-native-graph-v1", "root": root, "nodes": nodes}
