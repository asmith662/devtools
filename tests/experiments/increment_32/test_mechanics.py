# Copyright (c) 2026
# ruff: noqa: COM812, D103, E501, PLR2004
"""One-round typed expansion, native support, and novelty semantics."""

from __future__ import annotations

from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, cast

import pytest

from experiments.increment_32 import mechanics

if TYPE_CHECKING:
    from experiments.increment_25.development import SnapshotCorpus


def _sources() -> tuple[dict[str, Any], ...]:
    seeds = [
        {"address": f"seed-{rank}", "canonical_rank": rank} for rank in range(1, 6)
    ]
    imports = {
        "case_id": "case-1",
        "parent_snapshot_sha": "parent-1",
        "snapshot_id": "snapshot-1",
        "corpus_id": "corpus-1",
        "information_need": {"purpose": "purpose", "lexical_query": "query"},
        "seeds": seeds,
        "arms": {
            "outgoing": {
                "candidates": [
                    {
                        "address": "frontier-a",
                        "paths": [
                            {
                                "seed_address": "seed-1",
                                "direction": "outgoing",
                                "relation_identity": "first-import",
                            },
                            {
                                "seed_address": "seed-2",
                                "direction": "outgoing",
                                "relation_identity": "other-import",
                            },
                        ],
                    }
                ]
            },
            "incoming": {"candidates": []},
        },
    }
    lexical: dict[str, Any] = {"rankings": {method: [] for method in mechanics.METHODS}}
    lexical["rankings"]["canonical"] = [
        {"address": "direct-lexical", "rank": 6},
        {"address": "lexical-control", "rank": 7},
    ]
    references = {
        "candidates": [
            {
                "address": "frontier-b",
                "supports": [
                    {
                        "seed_address": "seed-3",
                        "direction": "forward",
                        "direct_call": True,
                    }
                ],
            }
        ]
    }
    containment = {
        "candidates": [
            {
                "address": "frontier-c",
                "supports": [
                    {"seed_address": "seed-4", "direction": "child_to_package"}
                ],
            }
        ]
    }
    mirrors = {
        "candidates": [
            {
                "address": "frontier-d",
                "supports": [{"seed_address": "seed-5", "direction": "source_to_test"}],
            }
        ]
    }
    return imports, lexical, references, containment, mirrors


def _edge(
    target: str,
    family: str = "import",
    direction: str = "forward",
    identity: str = "second",
) -> dict[str, Any]:
    return {
        "target": target,
        "family": family,
        "direction": direction,
        "support": {
            "snapshot_id": "snapshot-1",
            "identity": identity,
            "direct_call": family == "reference",
        },
    }


def test_saved_frontier_excludes_seeds_and_direct_union_is_complete() -> None:
    imports, lexical, references, containment, mirrors = _sources()
    frontier = mechanics.direct_frontier(imports, references, containment, mirrors)
    assert set(frontier) == {"frontier-a", "frontier-b", "frontier-c", "frontier-d"}
    assert len(frontier["frontier-a"]) == 2
    assert not set(frontier) & {row["address"] for row in imports["seeds"]}
    known = mechanics.direct_union(imports, lexical, references, containment, mirrors)
    assert {"seed-1", "direct-lexical", *frontier} <= known


def test_one_round_novelty_overlap_paths_and_no_multiplicity_score() -> None:
    imports, lexical, references, containment, mirrors = _sources()
    edges = {
        "seed-1": [_edge("must-not-expand")],
        "frontier-a": [
            _edge("seed-1"),
            _edge("direct-lexical"),
            _edge("novel", identity="one"),
            _edge("novel", identity="one"),
            _edge("novel", identity="two"),
        ],
        "frontier-b": [_edge("novel", "reference", "inverse"), _edge("third-hop-only")],
        "frontier-c": [_edge("frontier-d", "immediate_package", "package_to_child")],
        "frontier-d": [],
        "novel": [_edge("must-not-expand")],
    }
    # The other first-edge seed still has a valid seed-1 return; it is known-direct overlap.
    result = mechanics.project_case(
        imports=imports,
        lexical=lexical,
        references=references,
        containment=containment,
        mirrors=mirrors,
        edges=edges,
        diagnostics={},
    )
    assert result["candidate_count"] == 2
    assert {row["address"] for row in result["candidates"]} == {
        "novel",
        "third-hop-only",
    }
    assert result["overlap_direct_union_addresses"] == [
        "direct-lexical",
        "frontier-d",
        "seed-1",
    ]
    assert result["backtrack_path_count"] == 1
    novel = next(row for row in result["candidates"] if row["address"] == "novel")
    assert (
        novel["support_count"] == 5
    )  # two first supports x two distinct imports, plus reference
    assert set(novel) == {"address", "support_count", "paths"}
    assert {path["seed_resource"] for path in novel["paths"]} == {
        "seed-1",
        "seed-2",
        "seed-3",
    }
    assert all(
        path["frontier_resource"] in {"frontier-a", "frontier-b"}
        for path in novel["paths"]
    )
    assert result["lexical_volume_comparator"] == {
        "requested": 2,
        "addresses": ["direct-lexical", "lexical-control"],
        "actual": 2,
        "exhausted": False,
    }


def test_snapshot_isolation_and_no_recursive_expansion() -> None:
    imports, lexical, references, containment, mirrors = _sources()
    edges = {"frontier-a": [_edge("novel")], "novel": [_edge("next-round")]}
    result = mechanics.project_case(
        imports=imports,
        lexical=lexical,
        references=references,
        containment=containment,
        mirrors=mirrors,
        edges=edges,
        diagnostics={},
    )
    assert [row["address"] for row in result["candidates"]] == ["novel"]
    edges["frontier-a"][0]["support"]["snapshot_id"] = "other-snapshot"
    with pytest.raises(ValueError, match="crosses parent snapshot"):
        mechanics.project_case(
            imports=imports,
            lexical=lexical,
            references=references,
            containment=containment,
            mirrors=mirrors,
            edges=edges,
            diagnostics={},
        )


def test_native_relation_projection_all_directions_and_call_tag(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def module(address: str) -> SimpleNamespace:
        return SimpleNamespace(resource=SimpleNamespace(address=address))

    import_relation = SimpleNamespace(
        source=module("importer"), target=module("imported")
    )
    monkeypatch.setattr(
        mechanics, "_module_universe", lambda _corpus, _roots: (None, {})
    )
    monkeypatch.setattr(
        mechanics,
        "_derive_relations",
        lambda *_args, **_kwargs: ([import_relation], {"counts": {}}),
    )
    monkeypatch.setattr(
        mechanics, "_support", lambda _relation: {"relation_identity": "import-fact"}
    )
    monkeypatch.setattr(
        mechanics,
        "_source_occurrences",
        lambda **_kwargs: (
            [
                {
                    "source_resource": "caller",
                    "target_resource": "definition",
                    "snapshot_id": "s",
                    "source_span_utf8": [1, 2, 1, 3],
                    "direct_call": True,
                }
            ],
            {"counts": {}},
        ),
    )
    monkeypatch.setattr(
        mechanics,
        "_case_relations",
        lambda *_args: (
            [
                {
                    "child_address": "child",
                    "package_address": "package",
                    "snapshot_id": "s",
                }
            ],
            {},
        ),
    )
    monkeypatch.setattr(
        mechanics,
        "derive_mirrors",
        lambda _corpus: (
            [
                {
                    "source_address": "source",
                    "test_address": "test",
                    "snapshot_id": "s",
                    "rule": "exact-mirrored-test-path-v1",
                }
            ],
            {},
        ),
    )
    edges, _ = mechanics.incident_edges(
        cast("SnapshotCorpus", SimpleNamespace()), ("src", "tests")
    )
    expected = {
        "importer": ("imported", "import", "forward"),
        "imported": ("importer", "import", "inverse"),
        "caller": ("definition", "reference", "forward"),
        "definition": ("caller", "reference", "inverse"),
        "child": ("package", "immediate_package", "child_to_package"),
        "package": ("child", "immediate_package", "package_to_child"),
        "source": ("test", "mirrored_path", "source_to_test"),
        "test": ("source", "mirrored_path", "test_to_source"),
    }
    assert {
        key: (rows[0]["target"], rows[0]["family"], rows[0]["direction"])
        for key, rows in edges.items()
    } == expected
    assert sum(len(rows) for rows in edges.values()) == 8
    assert edges["caller"][0]["support"]["direct_call"] is True
    assert edges["source"][0]["support"]["rule"] == "exact-mirrored-test-path-v1"
