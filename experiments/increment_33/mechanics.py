# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, PLR0913, PLR0915, PLR2004, TRY003, C901
"""One outcome-blind third edge from every frozen Graph-1 novel resource."""

from __future__ import annotations

import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from experiments.increment_25.development import (
    _build_snapshot_corpus,
    _materialize_git_snapshot,
    _task_card,
    write_artifact,
)
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_30.mechanics import _verified_json
from experiments.increment_32.mechanics import (
    _sources,
    direct_frontier,
    direct_union,
    incident_edges,
)

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

ROOT = Path(__file__).resolve().parent
GRAPH_ONE_NAME = "graph_round_one_candidates.json"
GRAPH_ONE_SHA256 = "b8cb242dc0ff3d9184bcd14da2572864806f8986390ffe8000d4ff9a4e9fba0a"
FREEZE_NAME = "graph_round_two_freeze.json"
CANDIDATES_NAME = "graph_round_two_candidates.json"


def graph_one(root: Path = ROOT) -> dict[str, Any]:
    """Load only frozen, outcome-free Graph-1 mechanics."""
    path = root.parent / "increment_32" / GRAPH_ONE_NAME
    if sha256_file(path) != GRAPH_ONE_SHA256:
        raise ValueError("Frozen Graph-1 candidate artifact differs.")
    artifact = _verified_json(path)
    if artifact["judgments_loaded"] or artifact["heldout_executed"]:
        raise ValueError("Graph-1 frontier is not outcome-free development data.")
    return artifact


def build_freeze(root: Path = ROOT) -> dict[str, Any]:
    """Bind source identities and exact round-two mechanics before outcomes."""
    first = graph_one(root)
    imports, lexical, references, containment, mirrors = _sources(
        root.parent / "increment_32"
    )
    sources = (imports, lexical, references, containment, mirrors)
    ids = [case["case_id"] for case in first["cases"]]
    if (
        len(ids) != 24
        or len(set(ids)) != 24
        or any([row["case_id"] for row in source["cases"]] != ids for source in sources)
    ):
        raise ValueError("Graph-2 development source population differs.")
    source_freeze = _verified_json(
        root.parent / "increment_32" / "graph_round_one_freeze.json"
    )
    if first["freeze_identity"] != source_freeze["content_identity"]:
        raise ValueError("Graph-1 source freeze differs.")
    source_names = (
        "increment_27/structural_import_candidates.json.gz",
        "increment_27/lexical_comparison_rankings.json",
        "increment_29/references_calls_candidates.json",
        "increment_30/package_containment_candidates.json",
        "increment_31/mirrored_test_paths_candidates.json",
    )
    if any(
        source["content_identity"]
        != source_freeze["payload"]["source_content_identities"][name]
        or sha256_file(root.parent / name)
        != source_freeze["payload"]["source_sha256"][name]
        for name, source in zip(source_names, sources, strict=True)
    ):
        raise ValueError("Graph-2 direct evidence source artifacts differ.")
    frontier = [
        [case["case_id"], case["parent_snapshot_sha"], candidate["address"]]
        for case in first["cases"]
        for candidate in case["candidates"]
    ]
    payload = {
        "development_case_ids": ids,
        "heldout_case_ids_sealed": source_freeze["payload"]["heldout_case_ids_sealed"],
        "source_artifact_sha256": source_freeze["payload"]["source_sha256"],
        "source_content_identities": source_freeze["payload"][
            "source_content_identities"
        ],
        "graph_one_candidate_content_identity": first["content_identity"],
        "graph_one_candidate_sha256": GRAPH_ONE_SHA256,
        "graph_one_frontier_identities": frontier,
        "expansion": "one supported third edge from every Graph-1 novel case/resource; no recursive expansion",
        "relations": source_freeze["payload"]["relation_families"],
        "reference_direct_call": "one reference occurrence with optional direct_call specialization",
        "prior_surface": "all five positive lexical universes, four direct structural candidate surfaces, and all frozen Graph-1 novel candidates",
        "categories": ["original_seed", "other_direct", "graph_one", "new"],
        "candidate_identity": source_freeze["payload"]["candidate_identity"],
        "support_identity": "exact Graph-1 prefix path indexed by frozen candidate address and path index, crossed with exact deduplicated native third-edge support indexed by its canonical digest",
        "compact_support": "each novel third edge is stored once with native support; its candidate linkage expands across every frozen Graph-1 path for that edge's source resource",
        "deduplication": "one case/snapshot/resource candidate; one exact native third edge per source/target/family/direction/support; all distinct prefix x edge paths retained",
        "cycle_diagnostics": "measure immediate second-edge reversal, original seed return, direct-frontier return, direct and Graph-1 overlap; do not prune",
        "fanout": "uncapped natural third edge, no scoring, weighting, or ranking",
        "lexical_comparator": "next N frozen canonical positive resources after rank five; report exhaustion",
        "judgments_loaded": False,
        "confirmation_executed": False,
    }
    return {
        "schema": "devtools-i33-graph-round-two-freeze-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }


def freeze_protocol(root: Path = ROOT) -> dict[str, Any]:
    """Write the outcome-free Graph-2 protocol once."""
    artifact = build_freeze(root)
    path = root / FREEZE_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing Graph-2 protocol differs.")
    write_artifact(path=path, payload=artifact)
    return artifact


def reconstruct_path(
    prefix: Mapping[str, Any], edge: Mapping[str, Any]
) -> dict[str, Any]:
    """Exactly reconstruct one full three-edge native-support path."""
    if prefix["candidate_resource"] != edge["source"]:
        raise ValueError("Third edge does not start at Graph-1 prefix endpoint.")
    return {
        **prefix,
        "third_relation": {
            "family": edge["family"],
            "direction": edge["direction"],
            "support": edge["support"],
        },
        "graph_two_candidate_resource": edge["target"],
    }


def project_case(
    *,
    first: Mapping[str, Any],
    imports: Mapping[str, Any],
    lexical: Mapping[str, Any],
    references: Mapping[str, Any],
    containment: Mapping[str, Any],
    mirrors: Mapping[str, Any],
    edges: Mapping[str, Sequence[Mapping[str, Any]]],
    diagnostics: Mapping[str, Any],
) -> dict[str, Any]:
    """Project one uncapped third edge; store only novel native edge supports."""
    known = direct_union(imports, lexical, references, containment, mirrors)
    graph_one_addresses = {row["address"] for row in first["candidates"]}
    seeds = set(first["seed_addresses"])
    direct_frontier_addresses = set(
        direct_frontier(imports, references, containment, mirrors)
    )
    if graph_one_addresses & known:
        raise ValueError("Graph-1 novel frontier intersects direct evidence.")
    buckets: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    projected: dict[str, str] = {}
    raw_family: Counter[str] = Counter()
    raw_direction: Counter[str] = Counter()
    path_family: Counter[str] = Counter()
    path_direction: Counter[str] = Counter()
    combinations: Counter[str] = Counter()
    novel_combinations: Counter[str] = Counter()
    per_seed: dict[str, set[str]] = defaultdict(set)
    active = raw = unique_edges = paths_all = paths_novel = reversals = (
        seed_path_returns
    ) = frontier_path_returns = 0
    max_neighbors = 0
    for candidate in first["candidates"]:
        source = str(candidate["address"])
        prefixes = candidate["paths"]
        incident = edges.get(source, ())
        active += bool(incident)
        raw += len(incident)
        max_neighbors = max(
            max_neighbors, len({str(edge["target"]) for edge in incident})
        )
        dedup: dict[str, dict[str, Any]] = {}
        for edge in incident:
            support = edge["support"]
            if (
                "snapshot_id" in support
                and str(support["snapshot_id"]) != first["snapshot_id"]
            ):
                raise ValueError("Third edge crosses parent snapshot.")
            normalized = {
                "source": source,
                "target": str(edge["target"]),
                "family": edge["family"],
                "direction": edge["direction"],
                "support": support,
            }
            dedup[_digest(normalized)] = normalized
            raw_family[str(edge["family"])] += 1
            raw_direction[f"{edge['family']}:{edge['direction']}"] += 1
        unique_edges += len(dedup)
        for edge_id, edge in dedup.items():
            target = edge["target"]
            category = (
                "original_seed"
                if target in seeds
                else "other_direct"
                if target in known
                else "graph_one"
                if target in graph_one_addresses
                else "new"
            )
            if target in projected and projected[target] != category:
                raise ValueError("Graph-2 projection classification changed.")
            projected[target] = category
            if category == "new":
                buckets[target][edge_id] = edge
            for prefix in prefixes:
                paths_all += 1
                direction = f"{edge['family']}:{edge['direction']}"
                path_family[str(edge["family"])] += 1
                path_direction[direction] += 1
                combination = f"{prefix['first_relation']['family']}:{prefix['first_relation']['direction']} -> {prefix['second_relation']['family']}:{prefix['second_relation']['direction']} -> {direction}"
                combinations[combination] += 1
                if target == prefix["frontier_resource"]:
                    reversals += 1
                if target == prefix["seed_resource"]:
                    seed_path_returns += 1
                if target in direct_frontier_addresses:
                    frontier_path_returns += 1
                if category == "new":
                    paths_novel += 1
                    novel_combinations[combination] += 1
                    per_seed[str(prefix["seed_resource"])].add(target)
    third_edges = {
        edge_id: edge
        for support in buckets.values()
        for edge_id, edge in support.items()
    }
    candidates = [
        {
            "address": address,
            "third_edge_ids": sorted(supports),
            "support_path_count": sum(
                len(
                    next(
                        row["paths"]
                        for row in first["candidates"]
                        if row["address"] == edge["source"]
                    )
                )
                for edge in supports.values()
            ),
        }
        for address, supports in sorted(buckets.items())
    ]
    canonical = [
        str(row["address"])
        for row in lexical["rankings"]["canonical"]
        if int(row["rank"]) > 5
    ]
    counts = Counter(projected.values())
    return {
        "case_id": first["case_id"],
        "parent_snapshot_sha": first["parent_snapshot_sha"],
        "snapshot_id": first["snapshot_id"],
        "information_need": first["information_need"],
        "corpus_id": first["corpus_id"],
        "seed_addresses": first["seed_addresses"],
        "frontier_count": len(first["candidates"]),
        "active_frontier_count": active,
        "third_edges": dict(sorted(third_edges.items())),
        "candidates": candidates,
        "candidate_count": len(candidates),
        "projected_pair_count": len(projected),
        "projection_categories": dict(sorted(counts.items())),
        "raw_third_edge_supports": raw,
        "unique_third_edges": unique_edges,
        "complete_typed_paths": paths_all,
        "novel_typed_paths": paths_novel,
        "immediate_reverse_paths": reversals,
        "seed_return_paths": seed_path_returns,
        "direct_frontier_return_paths": frontier_path_returns,
        "max_distinct_frontier_neighbors": max_neighbors,
        "max_seed_novel_fanout": max(map(len, per_seed.values()), default=0),
        "third_edge_raw_by_family": dict(sorted(raw_family.items())),
        "third_edge_raw_by_direction": dict(sorted(raw_direction.items())),
        "third_edge_path_by_family": dict(sorted(path_family.items())),
        "third_edge_path_by_direction": dict(sorted(path_direction.items())),
        "path_combinations": dict(sorted(combinations.items())),
        "novel_path_combinations": dict(sorted(novel_combinations.items())),
        "lexical_volume_comparator": {
            "requested": len(candidates),
            "addresses": canonical[: len(candidates)],
            "actual": min(len(canonical), len(candidates)),
            "exhausted": len(canonical) < len(candidates),
        },
        "relation_diagnostics": diagnostics,
    }


def summarize(
    cases: Sequence[Mapping[str, Any]],
    first_cases: Sequence[Mapping[str, Any]],
    sources: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    """Aggregate outcome-free reach, path volume, and prior-address novelty."""
    previous = set()
    for imports, lexical, references, containment, mirrors in zip(
        *(source["cases"] for source in sources), strict=True
    ):
        previous.update(
            direct_union(imports, lexical, references, containment, mirrors)
        )
    previous.update(
        candidate["address"] for case in first_cases for candidate in case["candidates"]
    )
    addresses = {
        candidate["address"] for case in cases for candidate in case["candidates"]
    }
    fields = (
        "frontier_count",
        "active_frontier_count",
        "raw_third_edge_supports",
        "unique_third_edges",
        "projected_pair_count",
        "candidate_count",
        "complete_typed_paths",
        "novel_typed_paths",
        "immediate_reverse_paths",
        "seed_return_paths",
        "direct_frontier_return_paths",
    )
    summary: dict[str, Any] = {
        field: sum(int(case[field]) for case in cases) for field in fields
    }
    summary.update(
        {
            "development_cases": len(cases),
            "cases_with_novelty": sum(bool(case["candidate_count"]) for case in cases),
            "distinct_novel_addresses": len(addresses),
            "addresses_absent_all_prior_development": len(addresses - previous),
            "max_case_novelty": max(
                (int(case["candidate_count"]) for case in cases), default=0
            ),
            "max_seed_novel_fanout": max(
                (int(case["max_seed_novel_fanout"]) for case in cases), default=0
            ),
            "max_distinct_frontier_neighbors": max(
                (int(case["max_distinct_frontier_neighbors"]) for case in cases),
                default=0,
            ),
        }
    )
    for field in (
        "projection_categories",
        "third_edge_raw_by_family",
        "third_edge_raw_by_direction",
        "third_edge_path_by_family",
        "third_edge_path_by_direction",
        "path_combinations",
        "novel_path_combinations",
    ):
        summary[field] = dict(
            sorted(sum((Counter(case[field]) for case in cases), Counter()).items())
        )
    summary["lexical_comparator_requested"] = sum(
        case["lexical_volume_comparator"]["requested"] for case in cases
    )
    summary["lexical_comparator_actual"] = sum(
        case["lexical_volume_comparator"]["actual"] for case in cases
    )
    summary["lexical_comparator_exhausted_cases"] = sum(
        case["lexical_volume_comparator"]["exhausted"] for case in cases
    )
    return summary


def run_mechanics(*, repository_root: Path, root: Path = ROOT) -> dict[str, Any]:
    """Freeze the complete unpruned Graph-2 candidate and support surface."""
    protocol = build_freeze(root)
    if _read_json(root / FREEZE_NAME) != protocol:
        raise ValueError("Graph-2 protocol must be frozen first.")
    first = graph_one(root)
    sources = _sources(root.parent / "increment_32")
    population = cast(
        "dict[str, Any]",
        _read_json(root.parent / "increment_25" / "task_population_freeze.json"),
    )
    cards = {
        str(row["case_id"]): _task_card(row)
        for row in population["payload"]["task_cards"]
        if row["case_id"] in protocol["payload"]["development_case_ids"]
    }
    if len(cards) != 24:
        raise ValueError("Graph-2 development cards are incomplete.")
    cases = []
    for first_case, group in zip(
        first["cases"],
        zip(*(source["cases"] for source in sources), strict=True),
        strict=True,
    ):
        imports, lexical, references, containment, mirrors = group
        card = cards[first_case["case_id"]]
        if any(
            row["case_id"] != first_case["case_id"]
            or row["parent_snapshot_sha"] != card.parent_snapshot_sha
            for row in group
        ):
            raise ValueError("Graph-2 source case/snapshot differs.")
        with tempfile.TemporaryDirectory(prefix="devtools-i33-graph2-") as raw:
            location = Path(raw)
            _materialize_git_snapshot(
                repository_root=repository_root,
                snapshot_sha=card.parent_snapshot_sha,
                source_roots=card.corpus_source_roots,
                destination=location,
            )
            corpus = _build_snapshot_corpus(
                snapshot_root=location, source_roots=card.corpus_source_roots
            )
            if (
                str(corpus.snapshot.id) != first_case["snapshot_id"]
                or len(corpus.addresses) != imports["corpus_resource_count"]
            ):
                raise ValueError("Graph-2 historical parent corpus differs.")
            edges, diagnostics = incident_edges(corpus, card.corpus_source_roots)
            cases.append(
                project_case(
                    first=first_case,
                    imports=imports,
                    lexical=lexical,
                    references=references,
                    containment=containment,
                    mirrors=mirrors,
                    edges=edges,
                    diagnostics=diagnostics,
                )
            )
    artifact = {
        "schema": "devtools-i33-graph-round-two-candidates-v1",
        "freeze_identity": protocol["content_identity"],
        "graph_one_identity": first["content_identity"],
        "judgments_loaded": False,
        "heldout_executed": False,
        "cases": cases,
        "summary": summarize(cases, first["cases"], sources),
    }
    artifact["content_identity"] = _digest(artifact)
    path = root / CANDIDATES_NAME
    if path.exists() and _verified_json(path) != artifact:
        raise ValueError("Existing Graph-2 candidate artifact differs.")
    write_artifact(path=path, payload=artifact)
    return artifact


if __name__ == "__main__":
    freeze_protocol()
    run_mechanics(repository_root=ROOT.parents[1])
