# Copyright (c) 2026
"""Regular-expression value objects."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RegexMatch:
    """Represent one regular-expression match.

    :ivar value: Complete matched text.
    :ivar start: Inclusive character offset where the match begins.
    :ivar end: Exclusive character offset where the match ends.
    :ivar groups: Captured groups in pattern order.
    :ivar named_groups: Named captured groups as immutable key/value pairs.
    """

    value: str
    start: int
    end: int
    groups: tuple[str | None, ...] = ()
    named_groups: tuple[tuple[str, str | None], ...] = ()

    def __post_init__(self) -> None:
        """Validate regex match invariants."""
        self._validate()

    def _validate(self) -> None:
        """Validate match offsets.

        :raises ValueError: If the stored offsets are invalid.
        """
        if self.start < 0:
            msg = "Regex match start cannot be negative."
            raise ValueError(msg)

        if self.end < self.start:
            msg = "Regex match end cannot precede its start."
            raise ValueError(msg)

    @property
    def span(self) -> tuple[int, int]:
        """Return the match span.

        :returns: Inclusive start and exclusive end offsets.
        """
        return self.start, self.end

    @property
    def length(self) -> int:
        """Return the matched character count.

        :returns: Number of matched characters.
        """
        return self.end - self.start

    def group(self, index: int) -> str | None:
        """Return a captured group by zero-based index.

        :param index: Captured group index.
        :returns: Captured group value.
        :raises IndexError: If the group index does not exist.
        """
        return self.groups[index]

    def named_group(self, name: str) -> str | None:
        """Return a named captured group.

        :param name: Captured group name.
        :returns: Captured value.
        :raises KeyError: If the named group does not exist.
        """
        return dict(self.named_groups)[name]
