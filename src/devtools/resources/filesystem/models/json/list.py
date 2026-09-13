# Copyright (c) 2026
"""JSON list filesystem models."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from dataclasses import dataclass, field, replace
from typing import TYPE_CHECKING, overload

from devtools.core.conversion import convert_all
from devtools.resources.filesystem.models.json.base import (
    JsonCompatible,
    JsonFile,
    JsonMutableValue,
    JsonValue,
)
from devtools.resources.filesystem.models.json.conversion import freeze_json, thaw_json

if TYPE_CHECKING:
    from devtools.core.conversion import Converter


@dataclass(frozen=True, slots=True)
class JsonListFile(JsonFile, Sequence[JsonValue]):
    """Represent a JSON document whose root value is an array."""

    value: tuple[JsonValue, ...] = field(kw_only=True)

    def __post_init__(self) -> None:
        """Validate inherited text fields and freeze JSON storage."""
        super().__post_init__()
        frozen = freeze_json(self.value)

        if not isinstance(frozen, tuple):
            msg = "JsonListFile requires an array value."
            raise TypeError(msg)

        object.__setattr__(self, "value", frozen)

    @overload
    def __getitem__(self, index: int) -> JsonValue: ...

    @overload
    def __getitem__(self, index: slice) -> tuple[JsonValue, ...]: ...

    def __getitem__(
        self,
        index: int | slice,
    ) -> JsonValue | tuple[JsonValue, ...]:
        """Return an item or slice.

        :param index: Integer index or slice.
        :returns: JSON item or list slice.
        """
        return self.value[index]

    def __iter__(self) -> Iterator[JsonValue]:
        """Iterate over JSON array items.

        :returns: Iterator over items.
        """
        return iter(self.value)

    def __len__(self) -> int:
        """Return the number of array items.

        :returns: Array length.
        """
        return len(self.value)

    def find(
        self,
        predicate: Callable[[JsonValue], bool],
    ) -> JsonValue | None:
        """Return the first item satisfying a predicate.

        :param predicate: Item predicate.
        :returns: First matching item or ``None``.
        """
        for item in self.value:
            if predicate(item):
                return item

        return None

    def find_all(
        self,
        predicate: Callable[[JsonValue], bool],
    ) -> tuple[JsonValue, ...]:
        """Return all items satisfying a predicate.

        :param predicate: Item predicate.
        :returns: Immutable sequence of matches.
        """
        return tuple(item for item in self.value if predicate(item))

    def convert_items[TargetT](
        self,
        converter: Converter[JsonMutableValue, TargetT],
    ) -> tuple[TargetT, ...]:
        """Convert thawed array items through an explicit callable.

        :param converter: Callable receiving ordinary mutable JSON values.
        :returns: Immutable converted results in array order.
        :raises ConversionError: If an item conversion fails.
        """
        return convert_all((thaw_json(item) for item in self.value), converter)

    def find_by(
        self,
        key: str,
        value: JsonCompatible,
    ) -> JsonValue | None:
        """Find the first mapping item containing a matching member.

        Only top-level array items that are mappings participate.

        :param key: Mapping key.
        :param value: Required member value.
        :returns: First matching JSON item or ``None``.
        """
        for item in self.value:
            if isinstance(item, Mapping) and item.get(key) == value:
                return item

        return None

    def appended(
        self,
        value: JsonCompatible,
    ) -> JsonListFile:
        """Return a copy with an appended item.

        :param value: Item to append.
        :returns: Updated immutable JSON list file.
        """
        return replace(
            self,
            value=(*self.value, freeze_json(value)),
        )

    def extended(
        self,
        values: Iterable[JsonCompatible],
    ) -> JsonListFile:
        """Return a copy with additional items.

        :param values: Items to append.
        :returns: Updated immutable JSON list file.
        """
        return replace(
            self,
            value=(*self.value, *(freeze_json(value) for value in values)),
        )

    def with_item(
        self,
        index: int,
        value: JsonCompatible,
    ) -> JsonListFile:
        """Return a copy with one item replaced.

        :param index: Item index.
        :param value: Replacement value.
        :returns: Updated immutable JSON list file.
        :raises IndexError: If the index does not exist.
        """
        updated = list(self.value)
        updated[index] = freeze_json(value)

        return replace(
            self,
            value=tuple(updated),
        )

    def without_index(
        self,
        index: int,
    ) -> JsonListFile:
        """Return a copy without one item.

        :param index: Item index to remove.
        :returns: Updated immutable JSON list file.
        :raises IndexError: If the index does not exist.
        """
        updated = list(self.value)
        del updated[index]

        return replace(
            self,
            value=tuple(updated),
        )
