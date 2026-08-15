# Copyright (c) 2026
"""JSON object filesystem models."""

from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping
from dataclasses import dataclass, field, replace
from typing import TYPE_CHECKING

from devtools.conversion import convert
from devtools.filesystem.models.json.base import (
    JsonCompatible,
    JsonFile,
    JsonMutableValue,
    JsonValue,
)
from devtools.filesystem.models.json.conversion import freeze_json, thaw_json

if TYPE_CHECKING:
    from devtools.conversion import Converter


@dataclass(frozen=True, slots=True)
class JsonObjectFile(JsonFile, Mapping[str, JsonValue]):
    """Represent a JSON document whose root value is an object.

    The object provides normal read-only mapping behavior while immutable
    transformation methods return new file values.
    """

    value: Mapping[str, JsonValue] = field(kw_only=True)

    def __post_init__(self) -> None:
        """Validate inherited text fields and freeze JSON storage."""
        super().__post_init__()
        frozen = freeze_json(self.value)

        if not isinstance(frozen, Mapping):
            msg = "JsonObjectFile requires an object value."
            raise TypeError(msg)

        object.__setattr__(self, "value", frozen)

    def __getitem__(self, key: str) -> JsonValue:
        """Return a JSON value by key.

        :param key: Object key.
        :returns: Associated JSON value.
        """
        return self.value[key]

    def __iter__(self) -> Iterator[str]:
        """Iterate over object keys.

        :returns: Iterator over keys.
        """
        return iter(self.value)

    def __len__(self) -> int:
        """Return the number of object members.

        :returns: Object member count.
        """
        return len(self.value)

    def find(
        self,
        predicate: Callable[[str, JsonValue], bool],
    ) -> tuple[str, JsonValue] | None:
        """Return the first member satisfying a predicate.

        :param predicate: Predicate receiving key and value.
        :returns: Matching key/value pair or ``None``.
        """
        for key, value in self.value.items():
            if predicate(key, value):
                return key, value

        return None

    def find_all(
        self,
        predicate: Callable[[str, JsonValue], bool],
    ) -> tuple[tuple[str, JsonValue], ...]:
        """Return all members satisfying a predicate.

        :param predicate: Predicate receiving key and value.
        :returns: Immutable sequence of matching key/value pairs.
        """
        return tuple(
            (key, value) for key, value in self.value.items() if predicate(key, value)
        )

    def convert[TargetT](
        self,
        converter: Converter[dict[str, JsonMutableValue], TargetT],
    ) -> TargetT:
        """Convert a thawed ordinary object through an explicit callable.

        :param converter: Callable receiving an ordinary mutable JSON object.
        :returns: Converter result.
        :raises ConversionError: If the converter raises an ordinary exception.
        """
        return convert(_thaw_object(self.value), converter)

    def with_items(
        self,
        values: Mapping[str, JsonCompatible],
    ) -> JsonObjectFile:
        """Return a copy containing additional or replaced members.

        :param values: Members to merge.
        :returns: Updated immutable JSON object file.
        """
        updated = dict(self.value)
        updated.update(
            {key: freeze_json(value) for key, value in values.items()},
        )

        return replace(
            self,
            value=updated,
        )

    def with_item(
        self,
        key: str,
        value: JsonCompatible,
    ) -> JsonObjectFile:
        """Return a copy containing a replaced or added member.

        :param key: Object key.
        :param value: JSON value.
        :returns: Updated immutable JSON object file.
        """
        updated = dict(self.value)
        updated[key] = freeze_json(value)

        return replace(
            self,
            value=updated,
        )

    def without(
        self,
        key: str,
    ) -> JsonObjectFile:
        """Return a copy without a member.

        :param key: Object key to remove.
        :returns: Updated immutable JSON object file.
        :raises KeyError: If the key does not exist.
        """
        if key not in self.value:
            raise KeyError(key)

        updated = dict(self.value)
        del updated[key]

        return replace(
            self,
            value=updated,
        )


def _thaw_object(value: Mapping[str, JsonValue]) -> dict[str, JsonMutableValue]:
    """Return a conventional mutable object for explicit conversion."""
    return {key: thaw_json(item) for key, item in value.items()}
