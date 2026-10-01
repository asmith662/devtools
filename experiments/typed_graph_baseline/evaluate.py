# Copyright (c) 2026
# ruff: noqa: COM812
"""Replay prospectively fixed typed graph views on retained development state.

The trusted pickle is a frozen local input. All graph views and rankings are
built before the frozen development required-resource judgment is opened.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import pickle
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import TYPE_CHECKING, Any

from devtools.context.python.classes.bases import (
    PythonDirectBaseOutcome,
    derive_python_direct_bases,
)
from devtools.context.python.classes.declarations import (
    PythonClassMethodAnalysisAggregate,
    derive_python_class_method_declarations,
)
from devtools.context.python.function.declarations import (
    derive_python_function_declarations,
)
from devtools.context.python.mirrored_paths import (
    derive_python_mirrored_path_correspondences,
)
from devtools.context.python.modules.interpretation import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.python.modules.membership import (
    derive_python_immediate_package_memberships,
)
from devtools.context.python.references import derive_python_declaration_references
from devtools.context.retrieval.fusion import fuse_lexical_graph_rankings
from devtools.context.retrieval.graph import (
    PythonGraphProjection,
    build_python_graph_view,
    build_python_resource_graph_view,
    rank_python_repository_resources,
)
from devtools.context.retrieval.lexical import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from experiments.graph_ranking_baseline.evaluate import ADJUDICATION, ARCHIVE

if TYPE_CHECKING:
    from devtools.context.retrieval.graph.pagerank import PythonGraphRankingResult
    from devtools.context.retrieval.graph.view import PythonGraphView
    from experiments.codex_dogfood.capture import CodexDogfoodCase

FREEZE = Path(__file__).with_name("freeze.json")
OUTPUT = Path(__file__).with_name("development_results.json")
ADJUDICATION_SHA256 = "427c2936db23d1a04538c74420b565e50c7e8e480abfd1b7899a07231b2da9e2"
DEFAULT_DAMPING = 0.85
ARMS = ("full_prompt", "short_information_need")
VIEWS = (
    "resource-forward-frozen-input-v1",
    "resource-forward-current-ri-v1",
    "typed-core-v1",
    "typed-navigation-v1",
)
DEPTHS = (5, 10, 20, 50, 100)
EXPECTED_REQUIRED = 10


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _derive_views(case: CodexDogfoodCase) -> dict[str, PythonGraphView]:
    snapshot = case.snapshot
    python_addresses = tuple(
        resource.address
        for resource in snapshot.resources
        if resource.address.value.endswith(".py")
    )
    source_addresses = tuple(
        address for address in python_addresses if address.value.startswith("src/")
    )
    other_addresses = tuple(
        address for address in python_addresses if address not in source_addresses
    )
    source_modules = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("src"),
        resource_addresses=source_addresses,
    )
    other_modules = interpret_python_module_resources(
        snapshot,
        module_root=PythonModuleRoot("."),
        resource_addresses=other_addresses,
    )
    interpretations = source_modules.interpretations + other_modules.interpretations
    by_address = {item.resource.address: item for item in interpretations}
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=interpretations,
    )
    functions = tuple(
        declaration
        for address in python_addresses
        for declaration in derive_python_function_declarations(
            snapshot,
            resource_address=address,
        ).declarations
    )
    class_aggregate = PythonClassMethodAnalysisAggregate(
        tuple(
            derive_python_class_method_declarations(snapshot, resource_address=address)
            for address in python_addresses
        ),
    )
    references = tuple(
        fact
        for address in python_addresses
        for fact in derive_python_declaration_references(
            snapshot,
            resource_address=address,
            module_universe=universe,
            source_interpretations=(by_address[address],)
            if address in by_address
            else (),
        ).references
    )
    direct_bases = tuple(
        assessment
        for assessment in derive_python_direct_bases(
            snapshot,
            aggregate=class_aggregate,
            module_universe=universe,
        ).assessments
        if assessment.outcome is PythonDirectBaseOutcome.RESOLVED
    )
    memberships = tuple(
        fact
        for analysis in (source_modules, other_modules)
        for fact in derive_python_immediate_package_memberships(
            snapshot,
            interpretation_analysis=analysis,
        ).memberships
    )
    mirrors = derive_python_mirrored_path_correspondences(snapshot).correspondences
    return {
        VIEWS[0]: build_python_resource_graph_view(
            snapshot,
            imports=case.imports,
            references=case.references,
        ),
        VIEWS[1]: build_python_resource_graph_view(
            snapshot,
            imports=case.imports,
            references=references,
        ),
        VIEWS[2]: build_python_graph_view(
            snapshot,
            projection=PythonGraphProjection.TYPED_CORE,
            imports=case.imports,
            references=references,
            functions=functions,
            classes=class_aggregate.classes,
            methods=class_aggregate.methods,
            direct_bases=direct_bases,
        ),
        VIEWS[3]: build_python_graph_view(
            snapshot,
            projection=PythonGraphProjection.TYPED_NAVIGATION,
            imports=case.imports,
            references=references,
            functions=functions,
            classes=class_aggregate.classes,
            methods=class_aggregate.methods,
            direct_bases=direct_bases,
            memberships=memberships,
            mirrored_paths=mirrors,
        ),
    }


def _topology(view: PythonGraphView) -> dict[str, Any]:
    incident = {edge.source for edge in view.edges} | {
        edge.target for edge in view.edges
    }
    undirected: dict[str, set[str]] = defaultdict(set)
    for edge in view.edges:
        undirected[edge.source.identity].add(edge.target.identity)
        undirected[edge.target.identity].add(edge.source.identity)
    nodes_by_identity = {node.identity: node for node in view.nodes}
    cross_connected: set[str] = set()
    seen: set[str] = set()
    for node in view.nodes:
        if node.identity in seen:
            continue
        frontier = [node.identity]
        component: set[str] = set()
        while frontier:
            current = frontier.pop()
            if current in component:
                continue
            component.add(current)
            frontier.extend(undirected[current] - component)
        seen.update(component)
        addresses = {
            str(nodes_by_identity[item].resource_address) for item in component
        }
        if len(addresses) > 1:
            cross_connected.update(addresses)
    resources = {str(address) for address in view.resources}
    return {
        "node_count": len(view.nodes),
        "nodes_by_kind": dict(
            sorted(Counter(node.kind.value for node in view.nodes).items())
        ),
        "edge_count": len(view.edges),
        "contributions_by_family_direction": dict(
            sorted(
                Counter(
                    f"{support.family}:{support.direction}"
                    for edge in view.edges
                    for support in edge.contributions
                ).items()
            )
        ),
        "isolated_resource_nodes": sorted(
            str(node.resource_address)
            for node in view.nodes
            if node.kind.value == "resource" and node not in incident
        ),
        "cross_resource_isolated": sorted(resources - cross_connected),
    }


def _resource_order(result: PythonGraphRankingResult) -> list[str]:
    return [str(item.resource_address) for item in result.resources]


def _assess_order(order: list[str], required: list[str]) -> dict[str, Any]:
    ranks = {address: rank for rank, address in enumerate(order, start=1)}
    required_ranks = {address: ranks.get(address) for address in required}
    return {
        "candidate_count": len(order),
        "required_ranks": required_ranks,
        "coverage": {
            str(depth): sum(
                rank is not None and rank <= depth for rank in required_ranks.values()
            )
            for depth in DEPTHS
        },
        "last_required_rank": max(
            rank for rank in required_ranks.values() if rank is not None
        )
        if all(rank is not None for rank in required_ranks.values())
        else None,
    }


def evaluate() -> dict[str, Any]:  # noqa: C901
    """Freeze views and rankings first; then assess frozen development obligations."""
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    if (
        freeze["views"] != list(VIEWS)
        or freeze["input_archive_sha256"] != _sha(ARCHIVE)
        or freeze["damping"] != DEFAULT_DAMPING
        or freeze["personalization"]
        != "positive BM25 reciprocal rank 1/(60+rank), normalized, resource nodes only"
    ):
        msg = "Typed graph freeze differs from the evaluator's fixed configuration."
        raise ValueError(msg)
    with gzip.open(ARCHIVE, "rb") as stream:
        case: CodexDogfoodCase = pickle.load(stream)  # noqa: S301
    snapshot = case.snapshot
    views = _derive_views(case)
    topology = {name: _topology(view) for name, view in views.items()}
    rankings: dict[str, dict[str, list[str]]] = {}
    diagnostics: dict[str, dict[str, Any]] = {}
    provenance: dict[str, dict[str, Any]] = {}
    for arm in ARMS:
        query = getattr(case, arm)
        lexical = retrieve_repository_text_documents_by_bm25(
            query=analyze_repository_text_lexical_query(text=query),
            index=case.index,
            maximum_results=len(snapshot.resources),
            settings=case.lexical_settings,
        )
        rankings[arm] = {
            "bm25": [
                str(item.document_statistics.analysis.document.resource.address)
                for item in lexical.matches
            ],
        }
        diagnostics[arm] = {}
        provenance[arm] = {}
        for name, view in views.items():
            start = time.perf_counter()
            result = rank_python_repository_resources(
                snapshot,
                purpose=query,
                lexical_result=lexical,
                graph_view=view,
            )
            duration = time.perf_counter() - start
            rankings[arm][name] = _resource_order(result)
            diagnostics[arm][name] = {
                "iterations": result.iterations,
                "converged": result.converged,
                "elapsed_seconds": duration,
                "ranked_resources": len(result.resources),
                "winner_kinds": dict(
                    sorted(
                        Counter(
                            item.winning_node.kind.value for item in result.resources
                        ).items()
                    )
                ),
                "stationary_mass_by_node_kind": {
                    kind: sum(
                        item.score
                        for item in result.node_scores
                        if item.node.kind.value == kind
                    )
                    for kind in sorted(
                        {item.node.kind.value for item in result.node_scores}
                    )
                },
            }
            provenance[arm][name] = {
                str(item.resource_address): {
                    "winning_node": item.winning_node.identity,
                    "winning_node_kind": item.winning_node.kind.value,
                    "top_incoming": [
                        {
                            "source": support.source.identity,
                            "family": support.contribution.family,
                            "direction": support.contribution.direction,
                            "fact": support.contribution.fact.identity,
                            "flow": support.flow,
                        }
                        for support in item.incoming_supports[:3]
                    ],
                }
                for item in result.resources
            }
            if name in {VIEWS[2], VIEWS[3]} and result.resources:
                fused = fuse_lexical_graph_rankings(
                    snapshot,
                    purpose=query,
                    lexical_result=lexical,
                    graph_result=result,
                )
                rankings[arm][f"rrf:{name}"] = [
                    str(item.resource_address) for item in fused.resources
                ]
        lexical_addresses = set(rankings[arm]["bm25"])
        for name in views:
            diagnostics[arm][name]["ranked_absent_from_bm25"] = sorted(
                set(rankings[arm][name]) - lexical_addresses
            )

    # Outcome join boundary: none of the derivation or ranking above read labels.
    if _sha(ADJUDICATION) != ADJUDICATION_SHA256:
        msg = "Frozen development adjudication differs."
        raise ValueError(msg)
    labels = json.loads(ADJUDICATION.read_text(encoding="utf-8"))
    if labels["snapshot_id"] != str(snapshot.id):
        msg = "Adjudicated snapshot identity differs from replay input."
        raise ValueError(msg)
    required = sorted(
        item["address"]
        for item in labels["judgments"]
        if any(state.startswith("required_for_") for state in item["states"])
    )
    if len(required) != EXPECTED_REQUIRED:
        msg = "Frozen required-resource population differs."
        raise ValueError(msg)
    assessed = {
        arm: {name: _assess_order(order, required) for name, order in channels.items()}
        for arm, channels in rankings.items()
    }
    for arm, channels in rankings.items():
        lexical_addresses = set(channels["bm25"])
        for name in views:
            assessed[arm][name]["required_absent_from_bm25"] = sorted(
                set(required) & (set(channels[name]) - lexical_addresses)
            )
    concise_provenance = {
        arm: {
            name: {
                address: entries[address] for address in required if address in entries
            }
            for name, entries in views_provenance.items()
        }
        for arm, views_provenance in provenance.items()
    }
    return {
        "schema": "devtools-typed-graph-development-results-v1",
        "freeze_sha256": _sha(FREEZE),
        "snapshot_id": str(snapshot.id),
        "required": required,
        "topology": topology,
        "diagnostics": diagnostics,
        "arms": assessed,
        "required_provenance": concise_provenance,
        "confirmation_executed": False,
    }


if __name__ == "__main__":
    OUTPUT.write_text(
        json.dumps(evaluate(), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
