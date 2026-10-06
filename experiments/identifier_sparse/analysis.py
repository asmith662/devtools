# Copyright (c) 2026
"""Reuse the retained Increment-27 splitter without rewriting query prose."""

from __future__ import annotations

from itertools import islice
from typing import TYPE_CHECKING, TypedDict

from devtools.context.retrieval.lexical.analysis import iter_lexical_spans
from experiments.retrieval_identifier import expand_identifier_terms

if TYPE_CHECKING:
    from collections.abc import Iterator

ANALYZER_SEMANTICS = "r1-unicode-word-whole-plus-unique-identifier-components-v1"


class SpanDiagnostic(TypedDict):
    """Expose exact native spans and both lexical representations."""

    observed: str
    start: int
    end: int
    canonical: str
    identifier: tuple[str, ...]


class RepresentationDiagnostic(TypedDict):
    """Keep a bounded, typed diagnostic rather than corpus dumps."""

    semantics: str
    truncated: bool
    spans: list[SpanDiagnostic]


def iter_terms(text: str, *, identifier: bool = True) -> Iterator[str]:
    """Yield occurrence frequencies; deduplicate whole/components within each span."""
    for observed, canonical, _, _ in iter_lexical_spans(text=text):
        if identifier:
            yield from expand_identifier_terms(observed_text=observed)
        else:
            yield canonical


def query_terms(text: str) -> tuple[str, ...]:
    """Use identical analysis and canonical BM25's distinct-query-term policy."""
    return tuple(dict.fromkeys(iter_terms(text)))


def compare_terms(text: str, *, maximum_spans: int = 32) -> RepresentationDiagnostic:
    """Inspect a bounded source/query prefix without disclosing an entire corpus."""
    if maximum_spans <= 0:
        msg = "Diagnostic span bound must be positive."
        raise ValueError(msg)
    spans = tuple(islice(iter_lexical_spans(text=text), maximum_spans + 1))
    return {
        "semantics": ANALYZER_SEMANTICS,
        "truncated": len(spans) > maximum_spans,
        "spans": [
            {
                "observed": observed,
                "start": start,
                "end": end,
                "canonical": canonical,
                "identifier": expand_identifier_terms(observed_text=observed),
            }
            for observed, canonical, start, end in spans[:maximum_spans]
        ],
    }
