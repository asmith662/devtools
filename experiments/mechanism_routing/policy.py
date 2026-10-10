# Copyright (c) 2026
# ruff: noqa: EM101, TRY003 -- formatter owns commas; experiment validation
"""Freeze routing permission over existing purpose and native exact-hint contracts."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

from experiments.exact_hint_routing.routing import admit
from experiments.exact_hint_routing.serialization import encode

if TYPE_CHECKING:
    from devtools.context.localization.identity import TaskProvenance
    from experiments.codex_dogfood.acquisition.needs import InformationNeed
    from experiments.exact_hint_routing.models import (
        ExactHintObservation,
        ExactHintRouteRequest,
        HintAssociation,
    )


class IntentRole(StrEnum):
    """Caller-visible purpose roles; none asserts repository relevance."""

    INSPECT_EXISTING = "INSPECT_EXISTING"
    INTRODUCE_NEW = "INTRODUCE_NEW"
    CONCEPTUAL = "CONCEPTUAL"


class Arm(StrEnum):
    """Separate exact-mechanism value from selection value."""

    A = "LEXICAL_BASELINE"
    B = "ALWAYS_ON_EXACT_FIRST"
    C = "SELECTIVE_MECHANISM_ROUTER"


def classify(statement: str) -> IntentRole:
    """Classify a frozen caller purpose by an explicit, challengeable grammar.

    This is not natural-language inference. Unknown grammar fails authoring;
    the author must make the intended role explicit before execution.
    """
    for prefix, role in (
        ("Inspect existing ", IntentRole.INSPECT_EXISTING),
        ("Introduce new ", IntentRole.INTRODUCE_NEW),
        ("Understand ", IntentRole.CONCEPTUAL),
    ):
        if statement.startswith(prefix) and statement[len(prefix) :].strip():
            return role
    raise ValueError("Intent statement lacks the frozen role grammar")


@dataclass(frozen=True, slots=True)
class RoutingBasis:
    """Add task-only mechanism permission to an existing information purpose.

    A native obligation still owns lexical coverage. This wrapper owns only the
    role/optional exact input link; it is not another desired-information type.
    """

    need: InformationNeed
    hint: ExactHintObservation | None
    association: HintAssociation | None
    provenance: TaskProvenance

    def __post_init__(self) -> None:
        """Reject incomplete, cross-task or cross-obligation intent links."""
        classify(self.need.statement)
        if (self.hint is None) != (self.association is None):
            raise ValueError("Hint and association must be supplied together")
        if self.provenance.source_identity != self.need.obligation.task.value:
            raise ValueError("Foreign routing provenance")
        if (
            self.hint is not None
            and self.association is not None
            and (
                self.hint.task != self.need.obligation.task
                or self.association.lane != self.need.obligation
                or self.association.hint != self.hint.identity
                or self.need.provenance.span != self.hint.span
                or self.provenance.span != self.hint.span
            )
        ):
            raise ValueError("Foreign or mismatched intent/hint association")

    @property
    def role(self) -> IntentRole:
        """Compute permission from the frozen statement, never repository data."""
        return classify(self.need.statement)


@dataclass(frozen=True, slots=True)
class RouteDecision:
    """Keep skipped admission distinct from unsupported native syntax."""

    arm: Arm
    basis: RoutingBasis
    request: ExactHintRouteRequest | None
    disposition: str
    reason: str

    @property
    def identity(self) -> str:
        """Bind arm and complete task-only basis with canonical serialization."""
        return hashlib.sha256(encode(self)).hexdigest()


def decide(arm: Arm, basis: RoutingBasis) -> RouteDecision:
    """Select existing native mechanisms, with lexical fallback unconditional."""
    if not isinstance(arm, Arm):
        raise TypeError("Arm must be the frozen native experiment enum")
    request = None
    if basis.hint is None:
        disposition, reason = "LEXICAL_ONLY", "No explicit native locator input"
    elif arm is Arm.A:
        disposition, reason = "LEXICAL_ONLY", "Baseline excludes exact mechanisms"
    elif arm is Arm.C and basis.role is not IntentRole.INSPECT_EXISTING:
        disposition, reason = (
            "LEXICAL_ONLY",
            (
                "New destinations and conceptual purposes do not request "
                "existing exact evidence"
            ),
        )
    else:
        if basis.association is None:
            raise ValueError("Missing exact hint association")
        admitted = admit(basis.hint, basis.association)
        if admitted.locator is None:
            disposition, reason = (
                "UNSUPPORTED_WITH_LEXICAL_FALLBACK",
                admitted.reason,
            )
        else:
            request = admitted
            disposition, reason = (
                "EXACT_PLUS_LEXICAL",
                "Explicit typed native locator; original lexical lane remains complete",
            )
    return RouteDecision(arm, basis, request, disposition, reason)


def decisions(arm: Arm, bases: tuple[RoutingBasis, ...]) -> tuple[RouteDecision, ...]:
    """Reject duplicated authoring before creating an isolated arm plan."""
    if len({b.need.identity for b in bases}) != len(bases):
        raise ValueError("Duplicate intent identity")
    hints = [b.hint.identity for b in bases if b.hint is not None]
    if len(set(hints)) != len(hints):
        raise ValueError("Duplicate hint association in this bounded first slice")
    return tuple(decide(arm, basis) for basis in bases)
