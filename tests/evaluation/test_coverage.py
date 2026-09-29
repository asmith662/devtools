# Copyright (c) 2026
"""Tests for domain-neutral identity coverage."""

# ruff: noqa: D101, D103, D105, D107

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from devtools.evaluation.coverage import IdentityCoverage, compare_identity_coverage


def test_exact_and_empty_coverage() -> None:
    exact = compare_identity_coverage(expected=("a", "b"), observed=("b", "a"))
    empty: IdentityCoverage[str] = compare_identity_coverage(expected=(), observed=())

    assert exact.is_exact
    assert empty.is_exact
    assert exact.missing == ()
    assert exact.unexpected == ()


def test_missing_unexpected_and_simultaneous_diagnostics() -> None:
    missing = compare_identity_coverage(expected=("a",), observed=())
    unexpected = compare_identity_coverage(expected=(), observed=("b",))
    both = compare_identity_coverage(expected=("a", "b"), observed=("c", "b"))

    assert missing.missing == ("a",)
    assert missing.unexpected == ()
    assert unexpected.missing == ()
    assert unexpected.unexpected == ("b",)
    assert both.missing == ("a",)
    assert both.unexpected == ("c",)


def test_duplicates_are_reported_independently_and_in_first_order() -> None:
    coverage = compare_identity_coverage(
        expected=("b", "a", "b", "a", "c"),
        observed=("x", "y", "x", "z", "y"),
    )

    assert coverage.duplicate_expected == ("b", "a")
    assert coverage.duplicate_observed == ("x", "y")
    assert coverage.missing == ("b", "a", "c")
    assert coverage.unexpected == ("x", "y", "z")
    assert not coverage.is_exact


@dataclass(frozen=True)
class DomainIdentity:
    case: str
    resource: str


class NonSortableIdentity:
    """Hashable identity with equality but no ordering operations."""

    def __init__(self, value: int) -> None:
        self.value = value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, NonSortableIdentity) and self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)


def test_structured_hashable_and_non_sortable_identities() -> None:
    structured = DomainIdentity("case-1", "resource.py")
    structured_result = compare_identity_coverage(
        expected=(structured,),
        observed=(DomainIdentity("case-1", "resource.py"),),
    )
    left = NonSortableIdentity(1)
    right = NonSortableIdentity(2)
    unordered_result = compare_identity_coverage(
        expected=(left, right),
        observed=(NonSortableIdentity(2), NonSortableIdentity(1)),
    )

    assert structured_result.is_exact
    assert unordered_result.is_exact


class ConsumerOutcome(StrEnum):
    USEFUL = "useful"
    NOT_USEFUL = "not_useful"
    UNJUDGED = "unjudged"


@dataclass(frozen=True)
class ConsumerRecord:
    identity: str
    outcome: ConsumerOutcome


def test_unjudged_payload_is_observed_and_unsampled_expected_identity_is_missing() -> (
    None
):
    records = (
        ConsumerRecord("a", ConsumerOutcome.USEFUL),
        ConsumerRecord("b", ConsumerOutcome.NOT_USEFUL),
        ConsumerRecord("c", ConsumerOutcome.UNJUDGED),
    )
    coverage = compare_identity_coverage(
        expected=("a", "b", "c", "d"),
        observed=(record.identity for record in records),
    )

    assert coverage.missing == ("d",)
    assert coverage.unexpected == ()
