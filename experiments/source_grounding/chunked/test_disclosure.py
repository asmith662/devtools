# Copyright (c) 2026
# ruff: noqa: S101 -- deterministic bounded Unicode fixtures
"""Lossless framing preserves all permitted text without JSON escape growth."""

from dataclasses import replace
from typing import Any

import pytest

from experiments.source_grounding.chunked.cards import maximal_cards, require_strong_fit
from experiments.source_grounding.chunked.disclosure import decode, render


def context(count: int) -> dict[str, Any]:
    """No real scientific input or treatment information enters this fixture."""
    return {
        "case": "SYNTHETIC-CARD-FRAME",
        "task": "A fictional obligation",
        "obligations": [{"id": "O1"}, {"id": "O2"}],
        "coverage_root": "0" * 64,
        "cell_count": count,
        "card_count": count,
        "resource_count": (count + 1) // 2,
        "negative_counts": {"O1": 0, "O2": 0},
        "unresolved_cells": [],
    }


@pytest.mark.parametrize("count", [744, 640, 444])
def test_all_maximum_cards_fit_without_escaping(count: int) -> None:
    """Worst-case free-text cardinality is independent of Unicode repertoire."""
    cards = maximal_cards(count)
    raw = render(context(count), cards)
    require_strong_fit(raw)
    assert decode(raw) == (context(count), cards)
    assert len(raw) > len(raw.decode())
    assert b'"quote"' not in raw
    assert b'"content"' not in raw


@pytest.mark.parametrize(
    "text",
    ["\U0001f600\r\n0:alpha", '\\"\x00\x01\t', "512:raw\nCARD c0000", "a\u0301\u2028z"],
)
def test_exact_unicode_including_frame_looking_text(text: str) -> None:
    """No trimming, normalization, case folding or delimiter guessing occurs."""
    card = replace(maximal_cards(1)[0], summary=text)
    raw = render(context(1), (card,))
    assert decode(raw)[1] == (card,)


def test_ambiguity_truncation_and_foreign_context_reject() -> None:
    """A framing failure is never inferred to be valid semantic evidence."""
    raw = render(context(1), maximal_cards(1))
    for malformed in (raw[:-1], raw + b"trailing", b"invalid" + raw):
        with pytest.raises(ValueError, match=r"separator|replay|contract"):
            decode(malformed)
    with pytest.raises(ValueError, match="allowlist"):
        render({**context(1), "treatment": "forbidden"}, maximal_cards(1))
    with pytest.raises(ValueError, match="coverage"):
        render(context(2), maximal_cards(1))
