# Copyright (c) 2026
"""Shared Okapi BM25 arithmetic for concrete lexical retrieval fields."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.context.retrieval.lexical.bm25 import (
        RepositoryTextLexicalBm25Settings,
    )


def calculate_bm25_inverse_document_frequency(
    *,
    document_count: int,
    document_frequency: int,
) -> float:
    """Calculate the bounded Okapi BM25 inverse-document-frequency component."""
    return math.log(
        1 + (document_count - document_frequency + 0.5) / (document_frequency + 0.5),
    )


def calculate_bm25_term_contribution(
    *,
    term_frequency: int,
    inverse_document_frequency: float,
    document_length: int,
    average_document_length: float,
    settings: RepositoryTextLexicalBm25Settings,
) -> float:
    """Calculate one term's standard Okapi BM25 contribution."""
    numerator = term_frequency * (settings.k1 + 1)
    denominator = term_frequency + settings.k1 * (
        1 - settings.b + settings.b * document_length / average_document_length
    )
    return inverse_document_frequency * numerator / denominator
