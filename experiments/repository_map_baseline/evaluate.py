# Copyright (c) 2026
# ruff: noqa: COM812
"""Diagnostic replay after algorithm freeze; never a prospective validation case."""

from __future__ import annotations

import gzip
import hashlib
import json
import pickle
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any

from devtools.context.retrieval.fusion import fuse_lexical_repository_map_rankings
from devtools.context.retrieval.graph import rank_python_repository_resources
from devtools.context.retrieval.lexical import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from devtools.context.retrieval.repository_map import (
    build_repository_map_view,
    calculate_repository_map_importance,
    rank_repository_map,
)
from devtools.context.retrieval.repository_map.relevance import (
    score_repository_map_symbols,
)
from experiments.graph_ranking_baseline.evaluate import ADJUDICATION, ARCHIVE, ROOT
from experiments.typed_graph_baseline.evaluate import VIEWS, _derive_views

if TYPE_CHECKING:
    from experiments.codex_dogfood.capture import CodexDogfoodCase

FREEZE = Path(__file__).with_name("freeze.json")
OUTPUT = Path(__file__).with_name("diagnostic_results.json")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assess(order: list[str], judgments: list[dict[str, Any]]) -> dict[str, Any]:
    required = {
        item["address"]
        for item in judgments
        if any(state.startswith("required_for_") for state in item["states"])
    }
    ranks = {address: rank for rank, address in enumerate(order, 1)}
    missing = sorted(required - ranks.keys())
    last = None if missing else max(ranks[address] for address in required)
    # Incomplete channels have no complete-coverage prefix; report their entire
    # returned inventory separately rather than pretending they completed.
    prefix = order[:last] if last else order
    states = {item["address"]: item["states"] for item in judgments}
    return {
        "candidate_count": len(order),
        "required_count": len(required),
        "required_ranks": {address: ranks.get(address) for address in sorted(required)},
        "missing_required": missing,
        "recall": {
            str(depth): sum(
                ranks.get(address, float("inf")) <= depth for address in required
            )
            / len(required)
            for depth in (5, 10, 20, 50, 100)
        },
        "last_required_rank": last,
        "prefix_scope": "through complete required coverage"
        if last
        else "entire incomplete inventory",
        "helpful_in_prefix": sum(
            "helpful_only" in states[address] for address in prefix
        ),
        "unnecessary_in_prefix": sum(
            "unnecessary" in states[address] for address in prefix
        ),
        "unjudged_in_prefix": sum("unjudged" in states[address] for address in prefix),
    }


def evaluate() -> dict[str, Any]:  # noqa: C901, PLR0915
    """Build rankings under hashed production implementation before label join."""
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    for path, expected in freeze["implementation_newline_normalized_sha256"].items():
        normalized = (ROOT / path).read_text(encoding="utf-8").encode("utf-8")
        if hashlib.sha256(normalized).hexdigest() != expected:
            msg = f"Frozen implementation differs: {path}"
            raise ValueError(msg)
    if _sha(ARCHIVE) != freeze["input_archive_sha256"]:
        msg = "Diagnostic archive differs from retained input."
        raise ValueError(msg)
    with gzip.open(ARCHIVE, "rb") as stream:
        case: CodexDogfoodCase = pickle.load(stream)  # noqa: S301
    start = time.perf_counter()
    core = _derive_views(case)[VIEWS[2]]
    derivation_seconds = time.perf_counter() - start
    start = time.perf_counter()
    view = build_repository_map_view(case.snapshot, core=core)
    view_seconds = time.perf_counter() - start
    start = time.perf_counter()
    importance = calculate_repository_map_importance(case.snapshot, view=view)
    importance_seconds = time.perf_counter() - start
    orders: dict[str, dict[str, list[str]]] = {}
    diagnostics: dict[str, dict[str, Any]] = {}
    provenance: dict[str, dict[str, Any]] = {}
    for arm in ("full_prompt", "short_information_need"):
        text = getattr(case, arm)
        query = analyze_repository_text_lexical_query(text=text)
        start = time.perf_counter()
        lexical = retrieve_repository_text_documents_by_bm25(
            query=query,
            index=case.index,
            maximum_results=len(case.snapshot.resources),
            settings=case.lexical_settings,
        )
        lexical_seconds = time.perf_counter() - start
        start = time.perf_counter()
        ppr = rank_python_repository_resources(
            case.snapshot, purpose=text, lexical_result=lexical, graph_view=core
        )
        ppr_seconds = time.perf_counter() - start
        start = time.perf_counter()
        ranked = rank_repository_map(
            case.snapshot, purpose=text, query=query, importance=importance
        )
        map_seconds = time.perf_counter() - start
        start = time.perf_counter()
        fused = fuse_lexical_repository_map_rankings(
            case.snapshot, purpose=text, lexical_result=lexical, map_result=ranked
        )
        fusion_seconds = time.perf_counter() - start
        lexical_symbols = score_repository_map_symbols(view, query=query)
        symbol_only: dict[str, float] = {}
        for item in lexical_symbols:
            address = str(item.symbol.node.resource_address)
            symbol_only[address] = max(symbol_only.get(address, 0), item.score)
        global_only: dict[str, float] = {}
        for symbol in view.symbols:
            mass = next(
                item.score
                for item in importance.node_scores
                if item.node == symbol.node
            )
            if mass > 0:
                address = str(symbol.node.resource_address)
                global_only[address] = max(global_only.get(address, 0), mass)
        orders[arm] = {
            "bm25": [
                str(item.document_statistics.analysis.document.resource.address)
                for item in lexical.matches
            ],
            "typed_ppr": [str(item.resource_address) for item in ppr.resources],
            "repository_map": [str(item.resource_address) for item in ranked.resources],
            "bm25_map_rrf": [str(item.resource_address) for item in fused.resources],
            "symbol_bm25_only": sorted(
                symbol_only, key=lambda address: (-symbol_only[address], address)
            ),
            "global_symbol_only": sorted(
                global_only, key=lambda address: (-global_only[address], address)
            ),
        }
        diagnostics[arm] = {
            "bm25_seconds": lexical_seconds,
            "typed_ppr_seconds": ppr_seconds,
            "map_ranking_seconds": map_seconds,
            "fusion_seconds": fusion_seconds,
            "ranked_symbols": len(ranked.symbols),
            "positive_lexical_symbols": len(lexical_symbols),
            "map_resources": len(ranked.resources),
        }
        provenance[arm] = {
            str(item.resource_address): {
                "symbol": item.winning_symbol.symbol.qualified_name,
                "subject": item.winning_symbol.symbol.declaration.subject.identity,
                "importance": item.winning_symbol.importance,
                "importance_rank": item.winning_symbol.importance_rank,
                "symbol_lexical_rank": item.winning_symbol.lexical_rank,
                "matched_terms": [
                    term
                    for term, _ in item.winning_symbol.lexical_match.term_contributions
                ]
                if item.winning_symbol.lexical_match
                else [],
                "supports": [
                    {
                        "source": support.source.identity,
                        "family": support.contribution.family,
                        "fact": support.contribution.fact.identity,
                        "flow": support.flow,
                    }
                    for support in item.winning_symbol.incoming_supports
                ],
            }
            for item in ranked.resources
        }
    # Explicit outcome join. Case 0002 labels are development evidence, not sealed
    # confirmation. Neither the design nor parameters are selected from them.
    if _sha(ADJUDICATION) != freeze["adjudication_sha256"]:
        msg = "Diagnostic adjudication differs."
        raise ValueError(msg)
    labels = json.loads(ADJUDICATION.read_text(encoding="utf-8"))
    if labels["snapshot_id"] != str(case.snapshot.id):
        msg = "Diagnostic adjudication snapshot differs."
        raise ValueError(msg)
    assessed = {
        arm: {
            name: _assess(order, labels["judgments"])
            for name, order in channels.items()
        }
        for arm, channels in orders.items()
    }
    for arm, channels in orders.items():
        lexical_ranks = {
            address: rank for rank, address in enumerate(channels["bm25"], 1)
        }
        for name in channels:
            required_ranks = assessed[arm][name]["required_ranks"]
            assessed[arm][name]["rescued_required_lexical_misses"] = [
                address
                for address, rank in required_ranks.items()
                if rank and address not in lexical_ranks
            ]
            assessed[arm][name]["required_rank_movements"] = {
                address: {"bm25": lexical_ranks.get(address), "channel": rank}
                for address, rank in required_ranks.items()
            }
    return {
        "role": "Case 0002 diagnostic; not tuning or prospective validation",
        "freeze_sha256": _sha(FREEZE),
        "snapshot_id": str(case.snapshot.id),
        "construction": {
            "current_ri_and_four_retained_views_seconds": derivation_seconds,
            "map_view_seconds": view_seconds,
            "global_importance_seconds": importance_seconds,
            "nodes": len(view.dependencies.nodes),
            "edges": len(view.dependencies.edges),
            "symbols": len(view.symbols),
            "resources": len(view.core.resources),
            "iterations": importance.iterations,
            "converged": importance.converged,
        },
        "arms": assessed,
        "runtime": diagnostics,
        "rankings": orders,
        "map_provenance": provenance,
        "prospective_evaluation": "awaiting independent natural task",
        "confirmation_accessed": False,
    }


if __name__ == "__main__":
    OUTPUT.write_text(
        json.dumps(evaluate(), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
