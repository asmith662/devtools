# Copyright (c) 2026
"""Bounded retained Python object-graph size, with shared objects counted once."""

from __future__ import annotations

import sys
from dataclasses import fields, is_dataclass


def retained_size(value: object) -> dict[str, int]:
    """Count Python containers/dataclass fields; exclude interpreter/global state."""
    pending = [value]
    seen = set()
    total = 0
    while pending:
        item = pending.pop()
        if id(item) in seen:
            continue
        seen.add(id(item))
        total += sys.getsizeof(item)
        if isinstance(item, dict):
            pending.extend(item.keys())
            pending.extend(item.values())
        elif isinstance(item, (tuple, list, set, frozenset)):
            pending.extend(item)
        elif is_dataclass(item) and not isinstance(item, type):
            pending.extend(getattr(item, field.name) for field in fields(item))
    return {"bytes": total, "distinct_objects": len(seen)}
