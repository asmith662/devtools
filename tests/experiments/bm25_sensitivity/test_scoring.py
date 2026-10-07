# Copyright (c) 2026
# ruff: noqa: COM812 -- native parity fixture
"""The prospective common code path is exactly canonical at baseline."""

from __future__ import annotations

from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from devtools.context.retrieval.lexical.filename import (
    build_repository_text_filename_lexical_index,
)
from experiments.bm25_sensitivity.scoring import retrieve
from experiments.codex_dogfood.case_0009.freeze import canonical_index
from experiments.retrieval_diagnostics.models import Configuration
from tests.context.retrieval.lexical._helpers import _collection, _document


def test_prospective_adapter_exact_native_baseline_tie_order_and_empty_query() -> None:
    """No change to tokenization, fields, IDF, evidence or combination arithmetic."""
    docs = _collection(
        (
            _document("a.py", "plain plain"),
            _document("b.py", "plain plain"),
            _document("plain.txt", ""),
        )
    )
    index = canonical_index(docs)
    filename = build_repository_text_filename_lexical_index(document_collection=docs)
    config = Configuration("A", "test", "canonical", 1.2, 0.75, 0.25)
    for query in ("plain", "missing", ""):
        actual = retrieve(index, filename, query, config)
        expected = retrieve_repository_text_documents_by_bm25(
            query=analyze_repository_text_lexical_query(text=query),
            index=index,
            maximum_results=3,
        )
        assert actual == expected
