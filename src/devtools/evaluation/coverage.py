# Copyright (c) 2026
"""Expected-versus-observed identity coverage accounting."""

from __future__ import annotations

from collections.abc import Hashable, Iterable
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class IdentityCoverage[Identity: Hashable]:
    """Describe identity presence against a caller-supplied expected frame.

    Diagnostic tuples contain each affected identity once, ordered by its first
    occurrence in the corresponding input sequence.
    """

    duplicate_expected: tuple[Identity, ...]
    duplicate_observed: tuple[Identity, ...]
    missing: tuple[Identity, ...]
    unexpected: tuple[Identity, ...]

    @property
    def is_exact(self) -> bool:
        """Whether both inputs are unique and contain the same identities."""
        return not (
            self.duplicate_expected
            or self.duplicate_observed
            or self.missing
            or self.unexpected
        )


def compare_identity_coverage[Identity: Hashable](
    *,
    expected: Iterable[Identity],
    observed: Iterable[Identity],
) -> IdentityCoverage[Identity]:
    """Compare identity presence without interpreting caller-owned payloads.

    Missing identities are unique members of ``expected`` absent from
    ``observed``. Unexpected identities are unique members of ``observed``
    absent from ``expected``. Neither category expresses an outcome or a
    judgment about relevance or usefulness.
    """
    expected_items = tuple(expected)
    observed_items = tuple(observed)
    expected_unique, duplicate_expected = _unique_and_duplicates(expected_items)
    observed_unique, duplicate_observed = _unique_and_duplicates(observed_items)
    expected_set = set(expected_unique)
    observed_set = set(observed_unique)
    return IdentityCoverage(
        duplicate_expected=duplicate_expected,
        duplicate_observed=duplicate_observed,
        missing=tuple(
            identity for identity in expected_unique if identity not in observed_set
        ),
        unexpected=tuple(
            identity for identity in observed_unique if identity not in expected_set
        ),
    )


def _unique_and_duplicates[Identity: Hashable](
    identities: tuple[Identity, ...],
) -> tuple[tuple[Identity, ...], tuple[Identity, ...]]:
    unique: list[Identity] = []
    seen: set[Identity] = set()
    duplicate_set: set[Identity] = set()
    for identity in identities:
        if identity in seen:
            duplicate_set.add(identity)
        else:
            seen.add(identity)
            unique.append(identity)
    return tuple(unique), tuple(
        identity for identity in unique if identity in duplicate_set
    )
