# Copyright (c) 2026
# ruff: noqa: COM812, E501, PLR2004 -- exact replay fixture values

"""Native-oracle parity, linear filename combination and accepted alternatives."""

from __future__ import annotations

from dataclasses import replace
from itertools import product
from typing import Any

import pytest

from devtools.context.retrieval.lexical.bm25 import (
    RepositoryTextLexicalBm25Settings,
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from experiments.bm25_sensitivity.metrics import completion, normalize
from experiments.codex_dogfood.case_0009.freeze import canonical_index
from experiments.retrieval_diagnostics.mechanics import Mechanics
from tests.context.retrieval.lexical._helpers import _collection, _document
from tests.experiments.retrieval_diagnostics.helpers import capture


def test_parameter_replay_matches_native_fields_across_factorial_points() -> None:
    """Changed parameters preserve representation/ties and reproduce the real scorer."""
    docs = (("a.py", "plain plain detail"), ("b.py", "plain"), ("plain.txt", ""))
    c = capture(docs)
    engine = Mechanics(c)
    index = canonical_index(_collection(tuple(_document(a, t) for a, t in docs)))
    for k1, b in product((0.6, 1.2, 2.4), (0.0, 0.75, 1.0)):
        native = retrieve_repository_text_documents_by_bm25(
            query=analyze_repository_text_lexical_query(text="plain"),
            index=index,
            maximum_results=3,
            settings=RepositoryTextLexicalBm25Settings(k1=k1, b=b),
        )
        for weight in (0.0, 0.25, 2.0):
            actual = engine.reconfigured(
                replace(c.configuration, k1=k1, b=b, filename_weight=weight)
            )
            expected = {
                m.document_statistics.analysis.document.resource.address.value: m.content_score
                + weight * m.filename_score
                for m in native.matches
                if m.content_score + weight * m.filename_score > 0
            }
            assert actual.rows.keys() == expected.keys()
            for address, score in expected.items():
                assert actual.rows[address].score == pytest.approx(score, abs=1e-10)
                assert actual.explain(actual.resources[address])["score_reconstructed"]
            # Independently revalidate the new immutable capture with full source checks.
            assert Mechanics(actual.capture).capture == actual.capture
    with pytest.raises(ValueError, match="representation/index"):
        engine.reconfigured(replace(c.configuration, analyzer="identifier"))


def test_alternatives_never_mix_incompatible_members_and_misses_stay_null() -> None:
    """Accepted ALL alternatives supply sufficient depth, not all possible gold."""
    choices = (("a", ("one", "two")), ("b", ("three", "four")))
    assert completion(choices, {"one": 1, "four": 2}) is None
    assert completion(choices, {"one": 5, "two": 8, "three": 3, "four": 6}) == 6


def test_normalization_safety_uses_identities_not_equal_counts() -> None:
    """A different required witness cannot mask a lost baseline cell/resource."""
    baseline: dict[str, Any] = {
        "global": 100,
        "max_own": 50,
        "prefix_union": 40,
        "prefix_occurrences": 60,
        "required_resource_reach": ["one"],
        "required_cells_reached": [["o", "one"]],
        "required_unit_judgments_reached": [["o", "unit"]],
    }
    current = {
        **baseline,
        "global": 90,
        "max_own": 40,
        "prefix_union": 30,
        "required_resource_reach": ["other"],
        "required_cells_reached": [["o", "other"]],
    }
    normalize(current, baseline)
    assert current["normalized_exact"]["max_own"] == [4, 5]
    assert not current["reach_safe"]
    assert current["required_losses"]["required_resource_reach"] == ["one"]
    current = {**baseline, "max_own": None}
    normalize(current, baseline)
    assert current["normalized"]["max_own"] is None
