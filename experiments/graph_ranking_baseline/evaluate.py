# Copyright (c) 2026
# ruff: noqa: COM812
"""Replay a frozen production-RI dogfood snapshot, then join blind labels.

The trusted local pickle is historical retained state, never an external input.
Ranking completes before this script loads the development adjudication.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import pickle
from pathlib import Path
from typing import TYPE_CHECKING, Any

from devtools.context.retrieval.fusion import fuse_lexical_graph_rankings
from devtools.context.retrieval.graph import (
    build_python_resource_graph_view,
    rank_python_repository_resources,
)
from devtools.context.retrieval.lexical import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)

if TYPE_CHECKING:
    from experiments.codex_dogfood.capture import CodexDogfoodCase

ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT / "experiments/codex_dogfood/case_0002"
ARCHIVE = CASE / "inputs.pkl.gz"
ADJUDICATION = CASE.parent / "case_0002_adjudication_frozen.json"
FREEZE = Path(__file__).with_name("freeze.json")
OUTPUT = Path(__file__).with_name("development_results.json")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate() -> dict[str, Any]:
    """Rank without labels, then assess only exact observed required resources."""
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    if _sha(ARCHIVE) != freeze["input_archive_sha256"]:
        msg = "Retained development input archive differs from freeze."
        raise ValueError(msg)
    with gzip.open(ARCHIVE, "rb") as stream:
        case: CodexDogfoodCase = pickle.load(stream)  # noqa: S301
    snapshot = case.snapshot
    graph_view = build_python_resource_graph_view(
        snapshot, imports=case.imports, references=case.references
    )
    rankings: dict[str, dict[str, list[str]]] = {}
    diagnostics: dict[str, dict[str, object]] = {}
    for arm in freeze["lexical_query_arms"]:
        query = getattr(case, arm)
        lexical = retrieve_repository_text_documents_by_bm25(
            query=analyze_repository_text_lexical_query(text=query),
            index=case.index,
            maximum_results=len(case.snapshot.resources),
            settings=case.lexical_settings,
        )
        graph = rank_python_repository_resources(
            snapshot,
            purpose=query,
            lexical_result=lexical,
            graph_view=graph_view,
        )
        fusion = fuse_lexical_graph_rankings(
            snapshot, purpose=query, lexical_result=lexical, graph_result=graph
        )
        rankings[arm] = {
            "bm25": [
                str(item.document_statistics.analysis.document.resource.address)
                for item in lexical.matches
            ],
            "ppr": [str(item.resource_address) for item in graph.resources],
            "fusion": [str(item.resource_address) for item in fusion.resources],
        }
        diagnostics[arm] = {
            "iterations": graph.iterations,
            "converged": graph.converged,
            "seed_count": len(lexical.matches),
            "graph_positive_count": len(graph.resources),
        }

    # This is the outcome join boundary. No ranking path above reads labels.
    if _sha(ADJUDICATION) != (
        "427c2936db23d1a04538c74420b565e50c7e8e480abfd1b7899a07231b2da9e2"
    ):
        msg = "Frozen development adjudication differs."
        raise ValueError(msg)
    labels = json.loads(ADJUDICATION.read_text(encoding="utf-8"))
    if (
        labels["snapshot_id"] != str(snapshot.id)
        or not labels["identity_coverage"]["is_exact"]
    ):
        msg = "Adjudication does not cover the retained snapshot."
        raise ValueError(msg)
    identity_by_address = {
        str(item.address): str(item.content_identity) for item in snapshot.resources
    }
    if len(labels["judgments"]) != len(snapshot.resources) or any(
        identity_by_address.get(item["address"]) != item["content_identity"]
        for item in labels["judgments"]
    ):
        msg = "Adjudicated resource identities differ from the retained snapshot."
        raise ValueError(msg)
    required = sorted(
        item["address"]
        for item in labels["judgments"]
        if any(state.startswith("required_for_") for state in item["states"])
    )
    if len(required) != 10:  # noqa: PLR2004
        msg = "Frozen required-resource population differs."
        raise ValueError(msg)
    cases = {}
    for arm, channels in rankings.items():
        assessed = {}
        for channel, ordering in channels.items():
            ranks = {address: rank for rank, address in enumerate(ordering, 1)}
            required_ranks = {address: ranks.get(address) for address in required}
            assessed[channel] = {
                "candidate_count": len(ordering),
                "coverage": {
                    str(depth): sum(
                        rank is not None and rank <= depth
                        for rank in required_ranks.values()
                    )
                    for depth in (5, 10, 20, 30, 50, 100)
                },
                "last_required_rank": max(
                    (rank for rank in required_ranks.values() if rank is not None),
                    default=None,
                )
                if all(rank is not None for rank in required_ranks.values())
                else None,
                "required_ranks": required_ranks,
            }
        lexical_addresses = set(channels["bm25"])
        assessed["ppr"]["required_absent_from_bm25"] = sorted(
            set(required) & (set(channels["ppr"]) - lexical_addresses)
        )
        cases[arm] = assessed
    return {
        "schema": "devtools-query-conditioned-ppr-development-results-v1",
        "freeze_sha256": _sha(FREEZE),
        "adjudication_sha256": _sha(ADJUDICATION),
        "snapshot_id": str(snapshot.id),
        "snapshot_resource_count": len(snapshot.resources),
        "import_fact_count": len(case.imports),
        "reference_fact_count": len(case.references),
        "graph_edge_count": len(graph_view.edges),
        "graph_node_count": len(graph_view.resources),
        "diagnostics": diagnostics,
        "required_resource_count": len(required),
        "arms": cases,
        "confirmation_executed": False,
    }


if __name__ == "__main__":
    OUTPUT.write_text(
        json.dumps(evaluate(), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
