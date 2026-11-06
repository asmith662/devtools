# Copyright (c) 2026
"""Type-preserving categorical target identity and finite-value validation."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from collections.abc import Iterable

type CategoryValue = str | int | float | bool


def validate_category_values(values: Iterable[object]) -> tuple[CategoryValue, ...]:
    """Validate the scalar category values shared by target consumers.

    Exact scalar types are retained so Python's equality between values such
    as ``1`` and ``True`` does not erase their distinct category identities.
    """
    categories: list[CategoryValue] = []
    for value in values:
        if type(value) not in (str, int, float, bool):
            msg = (
                "target categories must be immutable string, integer, float, or "
                "boolean values"
            )
            raise TypeError(
                msg,
            )
        if isinstance(value, float) and not math.isfinite(value):
            msg = "target categories must not be non-finite"
            raise ValueError(msg)
        categories.append(cast("CategoryValue", value))
    return tuple(categories)


def category_identity(value: CategoryValue) -> tuple[type[object], object]:
    """Return a type-aware identity for a validated category scalar."""
    return type(value), value
