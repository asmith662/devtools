# Copyright (c) 2026
# ruff: noqa: ANN401, COM812 -- private metadata-derived exact field checker
"""Inline primitive checks in the original ordered dataclass field traversal."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from enum import Enum
from pathlib import PurePath
from typing import Any

from devtools.core.identity import Identity


class FieldChecks:
    """Invocation-owned functions derived only from native dataclass metadata."""

    def __init__(self) -> None:
        """Start with no cached checker or previously authenticated input."""
        self.functions: dict[type[Any], Any] = {}

    def checker(self, item: Any) -> Any:
        """Preserve encoder dispatch before selecting dataclass field semantics."""
        if isinstance(
            item, (dict, tuple, list, Identity, PurePath, Enum, type)
        ) or not is_dataclass(item):
            return None
        cls = type(item)
        if cls not in self.functions:
            names = tuple(field.name for field in fields(item))
            lines = [
                "def check(item, actual, visit):",
                f"    if set(actual) != set({names!r}): return False",
            ]
            for name in names:
                lines.extend(
                    [
                        f"    value = getattr(item, {name!r})",
                        f"    expected = actual[{name!r}]",
                        "    kind = type(value)",
                        "    if value is None or kind in (bool, int, float, str):",
                        "        if kind is not type(expected): return False",
                        "        if kind is float:",
                        "            if value.hex() != expected.hex(): return False",
                        "        elif value != expected: return False",
                        "    elif not visit(value, expected): return False",
                    ]
                )
            lines.append("    return True")
            namespace: dict[str, Any] = {}
            # Native field names are quoted literals, never executable input.
            exec(  # noqa: S102 -- quoted native metadata; private namespace
                compile("\n".join(lines), "<authenticated-native-field-check>", "exec"),
                namespace,
            )
            self.functions[cls] = namespace["check"]
        return self.functions[cls]
