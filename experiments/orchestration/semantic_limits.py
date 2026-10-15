# Copyright (c) 2026

"""Experiment-local invocation reservations, never billing or execution approval."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable

from experiments.orchestration.storage import require
from experiments.orchestration.workers.budget import BudgetError, FailureClass

SCOPE_ARITY = 3


@dataclass(frozen=True)
class InvocationLimits:
    """Explicit prospective stage/case/cohort limits; no scientific defaults."""

    stages: dict[str, int]
    cases: dict[str, int]
    cohort: int

    def __post_init__(self) -> None:
        """Unknown scope is not an unlimited grant."""
        require(
            bool(self.stages) and bool(self.cases),
            "Invocation limit scopes required",
        )
        require(
            all(
                type(n) is int and n >= 0
                for n in [self.cohort, *self.stages.values(), *self.cases.values()]
            ),
            "Finite nonnegative invocation limits required",
        )


class InvocationBudget:
    """Reserve the complete static/dynamic partition before its first entry."""

    def __init__(self, limits: InvocationLimits) -> None:
        """Bind trusted-controller per-run reservation state."""
        self.limits = limits
        self.reserved: dict[str, tuple[str, str, str]] = {}
        self.entered: set[str] = set()

    def reserve(
        self,
        stage: str,
        case: str,
        partition: str,
        invocation_ids: tuple[str, ...],
    ) -> None:
        """All-or-nothing partition reservation; no launch or journal on rejection."""
        require(
            stage in self.limits.stages
            and case in self.limits.cases
            and bool(partition),
            "Unbound invocation budget scope/partition",
        )
        require(
            len(set(invocation_ids)) == len(invocation_ids)
            and all(invocation_ids)
            and not set(invocation_ids) & self.reserved.keys(),
            "Duplicate invocation reservation; no retry",
        )
        count = len(invocation_ids)
        exceeded = (
            len(self.reserved) + count > self.limits.cohort
            or sum(s == stage for s, _, _ in self.reserved.values()) + count
            > self.limits.stages[stage]
            or sum(c == case for _, c, _ in self.reserved.values()) + count
            > self.limits.cases[case]
        )
        if exceeded:
            raise BudgetError(
                FailureClass.SEMANTIC_INVOCATION_BUDGET,
                f"{case}/{stage}: additional={count}; no semantic entry",
            )
        self.reserved.update(dict.fromkeys(invocation_ids, (stage, case, partition)))

    def enter(
        self,
        invocation: str,
        exact_preflight: Callable[[], None],
        persist_entered: Callable[[], None],
    ) -> None:
        """Exact dynamic sizing precedes ENTERED; ambiguous entry is never retried.

        The trusted caller must durably persist the reserved partition before this
        method and must not reconstruct an empty budget on resume. Existing dead
        journal/authority authentication remains independently mandatory.
        """
        require(
            invocation in self.reserved and invocation not in self.entered,
            "Invocation not reserved or already entered; no retry",
        )
        exact_preflight()
        self.entered.add(invocation)
        persist_entered()

    def snapshot(self) -> dict[str, object]:
        """Expose explicit host-persisted state; restoring empty state is not resume."""
        return {
            "schema": "semantic-invocation-budget-v1",
            "stages": self.limits.stages,
            "cases": self.limits.cases,
            "cohort": self.limits.cohort,
            "reserved": {k: list(v) for k, v in self.reserved.items()},
            "entered": sorted(self.entered),
        }

    @classmethod
    def restore(
        cls,
        limits: InvocationLimits,
        snapshot: dict[str, Any],
    ) -> InvocationBudget:
        """Restore trusted durable reservations, never erase entered identities."""
        require(
            set(snapshot)
            == {"schema", "stages", "cases", "cohort", "reserved", "entered"}
            and snapshot["schema"] == "semantic-invocation-budget-v1"
            and snapshot["stages"] == limits.stages
            and snapshot["cases"] == limits.cases
            and snapshot["cohort"] == limits.cohort,
            "Invocation budget resume binding differs",
        )
        restored = cls(limits)
        for invocation, scope in snapshot["reserved"].items():
            require(
                isinstance(scope, list) and len(scope) == SCOPE_ARITY,
                "Malformed reserved scope",
            )
            restored.reserve(scope[0], scope[1], scope[2], (invocation,))
        entered = snapshot["entered"]
        require(
            isinstance(entered, list)
            and len(set(entered)) == len(entered)
            and set(entered) <= restored.reserved.keys(),
            "Malformed entered invocation state",
        )
        restored.entered = set(entered)
        return restored
