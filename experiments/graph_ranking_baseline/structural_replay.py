# Copyright (c) 2026
# ruff: noqa: COM812
"""Compare frozen and broadened RI on retained development state.

The trusted pickle is a frozen local development input. The required-resource
join happens only after both graph projections and rankings are complete.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import pickle
from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING, Any

from devtools.context.python.modules.interpretation import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.python.references import derive_python_declaration_references
from devtools.context.retrieval.graph import (
    build_python_resource_graph_view,
    rank_python_repository_resources,
)
from devtools.context.retrieval.lexical import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from experiments.graph_ranking_baseline.evaluate import ADJUDICATION, ARCHIVE, FREEZE

if TYPE_CHECKING:
    from devtools.context.retrieval.graph.view import PythonResourceGraphView

OUTPUT = Path(__file__).with_name("structural_replay.json")
EXPECTED_REQUIRED = 10


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _topology(view: PythonResourceGraphView) -> dict[str, Any]:
    incident = {str(edge.source) for edge in view.edges} | {
        str(edge.target) for edge in view.edges
    }
    return {
        "nodes": len(view.resources),
        "edges": len(view.edges),
        "isolated": sorted(
            str(item) for item in view.resources if str(item) not in incident
        ),
        "contributions_by_kind": dict(
            sorted(
                Counter(c.kind for e in view.edges for c in e.contributions).items()
            ),
        ),
    }


def measure() -> dict[str, Any]:
    """Replay the unchanged graph configuration after deriving broader facts."""
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    if _sha(ARCHIVE) != freeze["input_archive_sha256"]:
        msg = "Retained development input archive differs from freeze."
        raise ValueError(msg)
    with gzip.open(ARCHIVE, "rb") as stream:
        case = pickle.load(stream)  # noqa: S301
    snapshot = case.snapshot
    old = build_python_resource_graph_view(
        snapshot,
        imports=case.imports,
        references=case.references,
    )
    python_addresses = tuple(
        resource.address
        for resource in snapshot.resources
        if resource.address.value.endswith(".py")
    )
    source_addresses = tuple(
        item for item in python_addresses if item.value.startswith("src/")
    )
    other_addresses = tuple(
        item for item in python_addresses if item not in source_addresses
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
    analyses = tuple(
        derive_python_declaration_references(
            snapshot,
            resource_address=address,
            module_universe=universe,
            source_interpretations=(by_address[address],)
            if address in by_address
            else (),
        )
        for address in python_addresses
    )
    references = tuple(fact for analysis in analyses for fact in analysis.references)
    old_keys = {
        (
            fact.occurrence.resource_address,
            fact.occurrence.source_range,
            fact.target_declaration.subject.identity,
            fact.direct_call,
        )
        for fact in case.references
    }
    new_keys = {
        (
            fact.occurrence.resource_address,
            fact.occurrence.source_range,
            fact.target_declaration.subject.identity,
            fact.direct_call,
        )
        for fact in references
    }
    new = build_python_resource_graph_view(
        snapshot,
        imports=case.imports,
        references=references,
    )
    rankings: dict[str, Any] = {}
    for arm in freeze["lexical_query_arms"]:
        query = getattr(case, arm)
        lexical = retrieve_repository_text_documents_by_bm25(
            query=analyze_repository_text_lexical_query(text=query),
            index=case.index,
            maximum_results=len(snapshot.resources),
            settings=case.lexical_settings,
        )
        rankings[arm] = {
            "old": [
                str(item.resource_address)
                for item in rank_python_repository_resources(
                    snapshot,
                    purpose=query,
                    lexical_result=lexical,
                    graph_view=old,
                ).resources
            ],
            "new": [
                str(item.resource_address)
                for item in rank_python_repository_resources(
                    snapshot,
                    purpose=query,
                    lexical_result=lexical,
                    graph_view=new,
                ).resources
            ],
        }
    old_topology = _topology(old)
    new_topology = _topology(new)
    # Development outcome join: no labels influence derivation or ranking above.
    if (
        _sha(ADJUDICATION)
        != "427c2936db23d1a04538c74420b565e50c7e8e480abfd1b7899a07231b2da9e2"
    ):
        msg = "Frozen development adjudication differs."
        raise ValueError(msg)
    labels = json.loads(ADJUDICATION.read_text(encoding="utf-8"))
    if labels["snapshot_id"] != str(snapshot.id):
        msg = "Development adjudication snapshot differs."
        raise ValueError(msg)
    required = sorted(
        item["address"]
        for item in labels["judgments"]
        if any(state.startswith("required_for_") for state in item["states"])
    )
    if len(required) != EXPECTED_REQUIRED:
        msg = "Expected ten frozen required resources."
        raise ValueError(msg)
    old_isolated = set(old_topology["isolated"])
    new_isolated = set(new_topology["isolated"])
    for arm, arm_rankings in rankings.items():
        rankings[arm] = {
            channel: {
                "last_required_rank": max(
                    order.index(address) + 1 for address in required
                )
                if all(address in order for address in required)
                else None,
                "required_ranks": {
                    address: order.index(address) + 1 if address in order else None
                    for address in required
                },
            }
            for channel, order in arm_rankings.items()
        }
    return {
        "schema": "development-broader-reference-topology-replay-v1",
        "snapshot_id": str(snapshot.id),
        "reference_facts_before": len(case.references),
        "reference_facts_after": len(references),
        "legacy_positive_facts_preserved": len(old_keys & new_keys),
        "legacy_positive_facts_total": len(old_keys),
        "reference_source_resources_after": len(
            {r.occurrence.resource_address for r in references}
        ),
        "reference_target_resources_after": len(
            {r.target_resource.address for r in references}
        ),
        "reference_target_kinds_after": dict(
            sorted(
                Counter(type(r.target_declaration).__name__ for r in references).items()
            )
        ),
        "reference_routes_after": dict(
            sorted(Counter(r.route.value for r in references).items())
        ),
        "old_graph": {k: v for k, v in old_topology.items() if k != "isolated"},
        "new_graph": {k: v for k, v in new_topology.items() if k != "isolated"},
        "isolated_resources_before": len(old_isolated),
        "isolated_resources_after": len(new_isolated),
        "newly_connected": sorted(old_isolated - new_isolated),
        "required_isolated_before": sorted(set(required) & old_isolated),
        "required_isolated_after": sorted(set(required) & new_isolated),
        "newly_connected_required": sorted(
            set(required) & (old_isolated - new_isolated)
        ),
        "unchanged_ppr": rankings,
        "confirmation_executed": False,
    }


if __name__ == "__main__":
    OUTPUT.write_text(
        json.dumps(measure(), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
