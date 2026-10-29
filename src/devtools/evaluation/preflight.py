# Copyright (c) 2026
"""Finite expectation cross-checks, not an oracle executor or certification."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from devtools.evaluation.coverage import compare_identity_coverage


@dataclass(frozen=True, slots=True)
class OracleComparison:
    """One supervisor-owned expectation and a separately derived observation.

    Labels and derivation are caller evidence, not proof of independence. Values
    must have ordinary deterministic equality; equality errors propagate. This
    record neither executes an oracle nor makes its expected value authoritative.
    """

    name: str
    obligation: str
    category: Literal["normal", "boundary", "empty"]
    expected: object
    independently_derived: object
    derivation: str


def check_oracle_expectations(
    *,
    obligations: tuple[str, ...],
    comparisons: tuple[OracleComparison, ...],
) -> tuple[str, ...]:
    """Return explicit blockers for a finite bounded-evaluation preflight.

    The supervisor must also verify executable focused/held-out controls,
    baseline assertion failures, environment errors, privacy and frozen input
    identities using existing test and Command mechanisms. An empty result
    establishes only the supplied comparisons, never general correctness or
    permission for model execution. No callback, effect or retry is performed.
    """
    issues: list[str] = []
    if not obligations or any(not item.strip() for item in obligations):
        issues.append("Obligations must be nonempty named expectations.")
    coverage = compare_identity_coverage(
        expected=obligations,
        observed=dict.fromkeys(case.obligation for case in comparisons),
    )
    if not coverage.is_exact:
        issues.append(f"Obligation coverage is not exact: {coverage}")
    names = tuple(case.name for case in comparisons)
    if len(set(names)) != len(names) or any(not name.strip() for name in names):
        issues.append("Comparison names must be distinct and nonempty.")
    categories = {case.category for case in comparisons}
    if categories != {"normal", "boundary", "empty"}:
        issues.append("Normal, boundary and empty-input comparisons are required.")
    for case in comparisons:
        if not case.derivation.strip():
            issues.append(f"{case.name}: independent derivation is undocumented.")
        if case.expected != case.independently_derived:
            issues.append(f"{case.name}: expected value disagrees with cross-check.")
    return tuple(issues)
