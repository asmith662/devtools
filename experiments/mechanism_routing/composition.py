# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003 -- formatter owns commas; experiment validation
"""Present captured native outcomes without executing any acquisition mechanism."""

from __future__ import annotations

from typing import TYPE_CHECKING

from experiments.exact_hint_routing.presentation import present
from experiments.mechanism_routing.policy import decide

if TYPE_CHECKING:
    from devtools.context.localization.identity import (
        LocalizationObligationIdentity,
        TaskProvenance,
    )
    from devtools.context.retrieval.lexical.bm25 import (
        RepositoryTextLexicalBm25RetrievalResult,
    )
    from experiments.exact_hint_routing.models import (
        ExactHintResolution,
        ExactHintRoutingView,
    )
    from experiments.exact_hint_routing.routing import ExactFrame
    from experiments.mechanism_routing.policy import RouteDecision


def compose(  # noqa: PLR0913, PLR0917 -- explicit native lane composition boundary
    frame: ExactFrame,
    lane: LocalizationObligationIdentity,
    lexical: RepositoryTextLexicalBm25RetrievalResult,
    global_safety: RepositoryTextLexicalBm25RetrievalResult,
    plan: tuple[RouteDecision, ...],
    resolutions: tuple[ExactHintResolution, ...],
    provenance: TaskProvenance,
) -> ExactHintRoutingView:
    """Require the exact isolated arm/lane request set, then reuse U2 safety.

    No resolver, query executor or index builder is called here. Later Stage B
    must execute each admitted request separately in each arm, without sharing
    resolution outcomes between arms.
    """
    if len({d.arm for d in plan}) > 1:
        raise ValueError("Mixed arm plan")
    if any(d != decide(d.arm, d.basis) for d in plan) or len(
        {d.basis.need.identity for d in plan}
    ) != len(plan):
        raise ValueError("Forged or duplicated frozen policy decision")
    if provenance.source_identity != lane.task.value:
        raise ValueError("Foreign composition provenance")
    expected = tuple(d.request for d in plan if d.request is not None)
    if any(d.basis.need.obligation != lane for d in plan):
        raise ValueError("Foreign lane plan")
    if (
        len({r.request.identity for r in resolutions}) != len(resolutions)
        or {r.request.identity for r in resolutions} != {r.identity for r in expected}
        or any(r.request not in expected for r in resolutions)
    ):
        raise ValueError("Missing, duplicated or unexpected arm resolution")
    return present(
        frame=frame,
        lane=lane,
        lexical=lexical,
        global_safety=global_safety,
        resolutions=resolutions,
        provenance=provenance,
    )
