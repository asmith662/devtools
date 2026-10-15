# Copyright (c) 2026
# ruff: noqa: S101 -- representation-size stress fixtures, no model calls
"""An exact card bound must account for actual host-disclosure escaping."""

from dataclasses import replace
from typing import Any

import pytest

from experiments.orchestration.workers.budget import BudgetError
from experiments.source_grounding.chunked.cards import (
    EvidenceCard,
    EvidenceState,
    require_strong_fit,
    worst_case_cards,
)


def card() -> EvidenceCard:
    """Use fictional identities; no scientific judgments are constructed."""
    return EvidenceCard(
        "c0000",
        "a" * 64,
        "O1",
        EvidenceState.USEFUL,
        "Useful fact",
        ("e0000",),
        "",
        representation_complete=True,
    )


def test_card_bounds_and_incomplete_representation_fail_closed() -> None:
    """Representation overflow never changes a label or trims evidence."""
    card().validate()
    overflow: list[dict[str, Any]] = [
        {"summary": ""},
        {"summary": "x" * 513},
        {"uncertainty_note": "x" * 257},
        {"evidence_ids": tuple(str(i) for i in range(5))},
        {"representation_complete": False},
    ]
    for changes in overflow:
        with pytest.raises(BudgetError, match="EVIDENCE_REPRESENTATION_LIMIT"):
            replace(card(), **changes).validate()
    invalid: list[dict[str, Any]] = [
        {"evidence_ids": ()},
        {"evidence_ids": ("e0000", "e0000")},
        {"state": EvidenceState.NO_USEFUL},
    ]
    for changes in invalid:
        with pytest.raises(ValueError, match="mismatch"):
            replace(card(), **changes).validate()
    with pytest.raises(ValueError, match="mismatch"):
        replace(card(), state=EvidenceState.NO_USEFUL, evidence_ids=()).validate()
    with pytest.raises(UnicodeError):
        replace(card(), summary="\ud800").validate()


@pytest.mark.parametrize("count", [744, 640, 444])
def test_current_transport_cannot_claim_worst_case_strong_fit(count: int) -> None:
    """Bounded decoded Unicode does not imply bounded serialized ASCII length."""
    raw = worst_case_cards(count)
    assert raw == worst_case_cards(count)
    assert len(raw) == len(raw.decode())
    with pytest.raises(BudgetError, match="70%"):
        require_strong_fit(raw)
    assert b'"quote"' not in raw
    assert b'"content"' not in raw


def test_sizing_rejects_unknown_population_and_accepts_small_frame() -> None:
    """A stress calculation is deterministic and does not publish a partition."""
    for count in [0, 10001]:
        with pytest.raises(ValueError, match="cell-count"):
            worst_case_cards(count)
    require_strong_fit(worst_case_cards(1))
