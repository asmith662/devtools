# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004
"""Graph-2 one-edge expansion and exact compact support tests."""

from __future__ import annotations

from typing import Any

import pytest

from experiments.increment_33.mechanics import graph_one, project_case, reconstruct_path


def fixture() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """One Graph-1 frontier resource with two distinct frozen prefix supports."""
    seeds = [{"address": f"seed{i}.py", "canonical_rank": i} for i in range(1, 6)]
    prefixes = [
        {
            "candidate_resource": "graph1.py",
            "frontier_resource": "direct.py",
            "seed_resource": "seed1.py",
            "first_relation": {
                "family": "import",
                "direction": "outgoing",
                "support": {"ordinal": 1},
            },
            "second_relation": {
                "family": "reference",
                "direction": "forward",
                "support": {"ordinal": ordinal},
            },
        }
        for ordinal in (1, 2)
    ]
    first = {
        "case_id": "case-1",
        "parent_snapshot_sha": "parent",
        "snapshot_id": "snapshot",
        "information_need": {"purpose": "example", "lexical_query": "example"},
        "corpus_id": "corpus",
        "seed_addresses": [row["address"] for row in seeds],
        "candidates": [{"address": "graph1.py", "paths": prefixes}],
    }
    imports = {
        "seeds": seeds,
        "arms": {
            "outgoing": {
                "candidates": [
                    {
                        "address": "direct.py",
                        "paths": [
                            {"seed_address": "seed1.py", "direction": "outgoing"}
                        ],
                    }
                ]
            }
        },
    }
    lexical: dict[str, Any] = {
        "rankings": {
            name: [] for name in ("canonical", "bm25_plus", "identifier", "path", "rrf")
        }
    }
    return first, imports, lexical


def project(edges: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    first, imports, lexical = fixture()
    empty: dict[str, Any] = {"candidates": []}
    return project_case(
        first=first,
        imports=imports,
        lexical=lexical,
        references=empty,
        containment=empty,
        mirrors=empty,
        edges=edges,
        diagnostics={},
    )


def edge(
    target: str, family: str = "import", direction: str = "forward", ordinal: int = 1
) -> dict[str, Any]:
    return {
        "target": target,
        "family": family,
        "direction": direction,
        "support": {"snapshot_id": "snapshot", "ordinal": ordinal},
    }


def test_complete_frozen_frontier_is_outcome_free() -> None:
    artifact = graph_one()
    assert sum(len(case["candidates"]) for case in artifact["cases"]) == 704
    assert not artifact["judgments_loaded"]
    assert not artifact["heldout_executed"]


def test_one_edge_classifies_prior_surfaces_and_retains_exact_supports() -> None:
    result = project(
        {
            "graph1.py": [
                edge("seed1.py"),
                edge("direct.py"),
                edge("graph1.py"),
                edge("new.py", ordinal=1),
                edge("new.py", ordinal=1),
                edge("new.py", ordinal=2),
            ],
            "new.py": [edge("would_be_fourth_edge.py")],
        }
    )
    assert result["projection_categories"] == {
        "original_seed": 1,
        "other_direct": 1,
        "graph_one": 1,
        "new": 1,
    }
    assert result["candidate_count"] == 1
    assert result["candidates"][0]["address"] == "new.py"
    assert len(result["candidates"][0]["third_edge_ids"]) == 2
    assert result["candidates"][0]["support_path_count"] == 4
    assert result["novel_typed_paths"] == 4
    assert result["immediate_reverse_paths"] == 2
    assert "would_be_fourth_edge.py" not in {
        row["address"] for row in result["candidates"]
    }
    first, _, _ = fixture()
    edges = result["third_edges"]
    paths = [
        reconstruct_path(prefix, edges[edge_id])
        for prefix in first["candidates"][0]["paths"]
        for edge_id in result["candidates"][0]["third_edge_ids"]
    ]
    assert (
        len(paths)
        == len(
            {
                (
                    path["second_relation"]["support"]["ordinal"],
                    path["third_relation"]["support"]["ordinal"],
                )
                for path in paths
            }
        )
        == 4
    )
    assert all(path["graph_two_candidate_resource"] == "new.py" for path in paths)


@pytest.mark.parametrize(
    ("family", "direction"),
    [
        ("import", "forward"),
        ("import", "inverse"),
        ("reference", "forward"),
        ("reference", "inverse"),
        ("immediate_package", "child_to_package"),
        ("immediate_package", "package_to_child"),
        ("mirrored_path", "source_to_test"),
        ("mirrored_path", "test_to_source"),
    ],
)
def test_all_native_relation_directions_are_projected(
    family: str, direction: str
) -> None:
    result = project({"graph1.py": [edge("new.py", family, direction)]})
    assert result["third_edge_raw_by_direction"] == {f"{family}:{direction}": 1}
    assert result["candidate_count"] == 1
    assert result["candidates"][0]["support_path_count"] == 2


def test_call_is_one_reference_edge_with_specialization() -> None:
    occurrence = edge("new.py", "reference", "forward")
    occurrence["support"]["direct_call"] = True
    result = project({"graph1.py": [occurrence]})
    assert result["raw_third_edge_supports"] == 1
    assert result["third_edge_raw_by_family"] == {"reference": 1}
    assert next(iter(result["third_edges"].values()))["support"]["direct_call"]


def test_snapshot_isolation_and_deterministic_projection() -> None:
    incoming = {"graph1.py": [edge("new.py")]}
    assert project(incoming) == project(incoming)
    incoming["graph1.py"][0]["support"]["snapshot_id"] = "alien"
    with pytest.raises(ValueError, match="crosses parent snapshot"):
        project(incoming)
