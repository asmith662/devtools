# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, PLR0913, PLR2004, TRY003
"""One outcome-blind expansion from frozen direct structural resources."""

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
from experiments.increment_27.structural_imports.mechanics import (
    _derive_relations,
    _digest,
    _module_universe,
    _support,
    read_candidate_artifact,
)
from experiments.increment_29.mechanics import _source_occurrences
from experiments.increment_30.mechanics import _case_relations, _verified_json
from experiments.increment_31.mechanics import derive_mirrors

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from experiments.increment_25.development import SnapshotCorpus

ROOT = Path(__file__).resolve().parent
FREEZE_NAME = "graph_round_one_freeze.json"
CANDIDATES_NAME = "graph_round_one_candidates.json"
SOURCE_FILES = (
    ("increment_25", "task_population_freeze.json"),
    ("increment_27", "experiment_freeze.json"),
    ("increment_27", "structural_import_candidates.json.gz"),
    ("increment_27", "lexical_comparison_rankings.json"),
    ("increment_29", "references_calls_candidates.json"),
    ("increment_30", "package_containment_candidates.json"),
    ("increment_31", "mirrored_test_paths_candidates.json"),
)
METHODS = ("canonical", "bm25_plus", "identifier", "path", "rrf")


def _sources(root: Path) -> tuple[dict[str, Any], ...]:
    imports = read_candidate_artifact(
        root.parent / SOURCE_FILES[2][0] / SOURCE_FILES[2][1]
    )
    return (
        imports,
        _verified_json(root.parent / SOURCE_FILES[3][0] / SOURCE_FILES[3][1]),
        _verified_json(root.parent / SOURCE_FILES[4][0] / SOURCE_FILES[4][1]),
        _verified_json(root.parent / SOURCE_FILES[5][0] / SOURCE_FILES[5][1]),
        _verified_json(root.parent / SOURCE_FILES[6][0] / SOURCE_FILES[6][1]),
    )


def build_freeze(root: Path = ROOT) -> dict[str, Any]:
    """Bind the development sources and all candidate mechanics before outcomes."""
    imports, lexical, references, containment, mirrors = _sources(root)
    cases = imports["cases"]
    allowed = [str(row["case_id"]) for row in cases]
    population = cast(
        "dict[str, Any]",
        _read_json(root.parent / "increment_27" / "experiment_freeze.json"),
    )
    structural = cast(
        "dict[str, Any]",
        _read_json(root.parent / "increment_27" / "structural_import_freeze.json"),
    )
    if (
        len(allowed) != 24
        or len(set(allowed)) != 24
        or allowed != structural["payload"]["development_case_ids"]
        or set(allowed) & set(structural["payload"]["heldout_case_ids_sealed"])
        or population["payload"]["increment_27_confirmation"]["case_ids"]
        != structural["payload"]["heldout_case_ids_sealed"]
        or any(
            [str(row["case_id"]) for row in source["cases"]] != allowed
            for source in (lexical, references, containment, mirrors)
        )
    ):
        raise ValueError("Graph-1 sources differ from frozen development population.")
    for group in zip(
        *(
            source["cases"]
            for source in (imports, lexical, references, containment, mirrors)
        ),
        strict=True,
    ):
        if len({str(row["parent_snapshot_sha"]) for row in group}) != 1:
            raise ValueError("Graph-1 source parent snapshots differ.")
    source_sha = {
        f"{directory}/{name}": sha256_file(root.parent / directory / name)
        for directory, name in SOURCE_FILES
    }
    payload = {
        "development_case_ids": allowed,
        "heldout_case_ids_sealed": structural["payload"]["heldout_case_ids_sealed"],
        "source_sha256": source_sha,
        "source_content_identities": {
            f"{directory}/{name}": source["content_identity"]
            for (directory, name), source in zip(
                SOURCE_FILES[2:],
                (imports, lexical, references, containment, mirrors),
                strict=True,
            )
        },
        "seeds": "saved first five positive canonical resource results per case",
        "frontier": "union of saved direct Imports, References/Calls, immediate Containment, and exact mirrored-path candidate resources; lexical seeds are not expanded",
        "relation_families": {
            "import": ["forward", "inverse"],
            "reference": ["forward", "inverse"],
            "immediate_package": ["child_to_package", "package_to_child"],
            "mirrored_path": ["source_to_test", "test_to_source"],
        },
        "reference_direct_call": "one reference occurrence with a direct_call specialization tag",
        "expansion": "exactly one edge from each direct structural frontier resource; no recursive traversal",
        "candidate_identity": [
            "InformationNeed purpose",
            "frozen query",
            "parent snapshot",
            "resource address",
            "usefulness semantics",
        ],
        "primary_novelty": "outside all five saved positive lexical universes and all four completed direct structural candidate surfaces",
        "backtracking": "reject return to the originating lexical seed; direct-union landings are overlap diagnostics only",
        "path_identity": "exact canonical content of case, seed, frontier, first native support, second native support, candidate, relation families and directions",
        "deduplication": "one case/snapshot/resource candidate; retain all distinct exact typed support paths",
        "fanout": "uncapped natural one-round fan-out; no score, pruning, weighting, or ordering",
        "lexical_comparator": "next N frozen canonical positive resources after rank five, where N is the primary novel case count; report exhaustion",
        "judgments_loaded": False,
        "confirmation_executed": False,
    }
    return {
        "schema": "devtools-i32-graph-round-one-freeze-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }


def freeze_protocol(root: Path = ROOT) -> dict[str, Any]:
    """Persist the protocol only when its frozen source bindings agree."""
    artifact = build_freeze(root)
    path = root / FREEZE_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing Graph-1 protocol differs.")
    write_artifact(path=path, payload=artifact)
    return artifact


def direct_frontier(
    imports: Mapping[str, Any],
    references: Mapping[str, Any],
    containment: Mapping[str, Any],
    mirrors: Mapping[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    """Retain every saved first-edge support, excluding lexical seeds."""
    seeds = {str(row["address"]) for row in imports["seeds"]}
    if len(imports["seeds"]) != 5 or [
        row["canonical_rank"] for row in imports["seeds"]
    ] != [1, 2, 3, 4, 5]:
        raise ValueError("Graph-1 seeds differ from canonical first five.")
    frontier: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for arm in imports["arms"].values():
        for candidate in arm["candidates"]:
            for support in candidate["paths"]:
                frontier[str(candidate["address"])].append(
                    {
                        "seed": support["seed_address"],
                        "family": "import",
                        "direction": support["direction"],
                        "support": support,
                    }
                )
    for source, family in (
        (references, "reference"),
        (containment, "immediate_package"),
        (mirrors, "mirrored_path"),
    ):
        for candidate in source["candidates"]:
            for support in candidate["supports"]:
                frontier[str(candidate["address"])].append(
                    {
                        "seed": support["seed_address"],
                        "family": family,
                        "direction": support["direction"],
                        "support": support,
                    }
                )
    if any(address in seeds for address in frontier) or any(
        first["seed"] not in seeds for paths in frontier.values() for first in paths
    ):
        raise ValueError("Graph-1 frontier contains a lexical seed or alien support.")
    return dict(sorted(frontier.items()))


def direct_union(
    imports: Mapping[str, Any],
    lexical: Mapping[str, Any],
    references: Mapping[str, Any],
    containment: Mapping[str, Any],
    mirrors: Mapping[str, Any],
) -> set[str]:
    """Return all already reachable resources in the five lexical and four structural surfaces."""
    known = {str(row["address"]) for row in imports["seeds"]}
    for method in METHODS:
        known.update(str(row["address"]) for row in lexical["rankings"][method])
    for arm in imports["arms"].values():
        known.update(str(row["address"]) for row in arm["candidates"])
    for source in (references, containment, mirrors):
        known.update(str(row["address"]) for row in source["candidates"])
    return known


def incident_edges(
    corpus: SnapshotCorpus, roots: Sequence[str]
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any]]:
    """Reconstruct native facts, then index their two resource projections."""
    universe, by_address = _module_universe(corpus, roots)
    imports, import_diagnostics = _derive_relations(
        corpus, universe=universe, by_address=by_address
    )
    references, reference_diagnostics = _source_occurrences(
        corpus=corpus, universe=universe, by_address=by_address
    )
    containment, containment_diagnostics = _case_relations(corpus, roots)
    mirrors, mirror_diagnostics = derive_mirrors(corpus)
    edges: dict[str, list[dict[str, Any]]] = defaultdict(list)

    def add(
        source: str, target: str, family: str, direction: str, support: dict[str, Any]
    ) -> None:
        edges[source].append(
            {
                "target": target,
                "family": family,
                "direction": direction,
                "support": support,
            }
        )

    for relation in imports:
        support = cast("dict[str, Any]", _support(relation))
        source, target = (
            str(relation.source.resource.address),
            str(relation.target.resource.address),
        )
        add(source, target, "import", "forward", support)
        add(target, source, "import", "inverse", support)
    for occurrence in references:
        source, target = (
            str(occurrence["source_resource"]),
            str(occurrence["target_resource"]),
        )
        add(source, target, "reference", "forward", occurrence)
        add(target, source, "reference", "inverse", occurrence)
    for membership in containment:
        source, target = (
            str(membership["child_address"]),
            str(membership["package_address"]),
        )
        add(source, target, "immediate_package", "child_to_package", membership)
        add(target, source, "immediate_package", "package_to_child", membership)
    for mirror in mirrors:
        source, target = str(mirror["source_address"]), str(mirror["test_address"])
        add(source, target, "mirrored_path", "source_to_test", mirror)
        add(target, source, "mirrored_path", "test_to_source", mirror)
    return edges, {
        "imports": import_diagnostics["counts"],
        "references": reference_diagnostics["counts"],
        "containment": containment_diagnostics,
        "mirrors": mirror_diagnostics,
    }


def project_case(
    *,
    imports: Mapping[str, Any],
    lexical: Mapping[str, Any],
    references: Mapping[str, Any],
    containment: Mapping[str, Any],
    mirrors: Mapping[str, Any],
    edges: Mapping[str, Sequence[Mapping[str, Any]]],
    diagnostics: Mapping[str, Any],
) -> dict[str, Any]:
    """Expand exactly one new edge; separate novel candidates from overlap."""
    frontier = direct_frontier(imports, references, containment, mirrors)
    known = direct_union(imports, lexical, references, containment, mirrors)
    snapshot_id = str(imports["snapshot_id"])
    case_id = str(imports["case_id"])
    parent = str(imports["parent_snapshot_sha"])
    need = imports["information_need"]
    paths: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    overlap: set[str] = set()
    backtracks = 0
    fanout_family: Counter[str] = Counter()
    fanout_direction: Counter[str] = Counter()
    max_neighbors = 0
    for resource, firsts in frontier.items():
        incident = edges.get(resource, ())
        max_neighbors = max(
            max_neighbors, len({str(edge["target"]) for edge in incident})
        )
        for edge in incident:
            support = edge["support"]
            if "snapshot_id" in support and str(support["snapshot_id"]) != snapshot_id:
                raise ValueError("Graph-1 second edge crosses parent snapshot.")
        for first in firsts:
            for edge in incident:
                support = edge["support"]
                target = str(edge["target"])
                if target == first["seed"]:
                    backtracks += 1
                    continue
                fanout_family[str(edge["family"])] += 1
                fanout_direction[f"{edge['family']}:{edge['direction']}"] += 1
                if target in known:
                    overlap.add(target)
                    continue
                path = {
                    "case_id": case_id,
                    "information_need": need,
                    "parent_snapshot_sha": parent,
                    "snapshot_id": snapshot_id,
                    "seed_resource": first["seed"],
                    "frontier_resource": resource,
                    "first_relation": {
                        "family": first["family"],
                        "direction": first["direction"],
                        "support": first["support"],
                    },
                    "second_relation": {
                        "family": edge["family"],
                        "direction": edge["direction"],
                        "support": support,
                    },
                    "candidate_resource": target,
                }
                paths[target][_digest(path)] = path
    candidates: list[dict[str, Any]] = [
        {
            "address": address,
            "support_count": len(supports),
            "paths": [supports[key] for key in sorted(supports)],
        }
        for address, supports in sorted(paths.items())
    ]
    per_seed: dict[str, set[str]] = defaultdict(set)
    combinations: Counter[str] = Counter()
    for candidate in candidates:
        for path in candidate["paths"]:
            per_seed[str(path["seed_resource"])].add(str(candidate["address"]))
            first, second = path["first_relation"], path["second_relation"]
            combinations[
                f"{first['family']}:{first['direction']} -> {second['family']}:{second['direction']}"
            ] += 1
    canonical = [
        str(row["address"])
        for row in lexical["rankings"]["canonical"]
        if int(row["rank"]) > 5
    ]
    count = len(candidates)
    comparator = canonical[:count]
    return {
        "case_id": case_id,
        "parent_snapshot_sha": parent,
        "snapshot_id": snapshot_id,
        "information_need": need,
        "corpus_id": imports["corpus_id"],
        "seed_addresses": [row["address"] for row in imports["seeds"]],
        "frontier_count": len(frontier),
        "frontier_first_support_count": sum(map(len, frontier.values())),
        "candidate_count": count,
        "candidates": candidates,
        "overlap_direct_union_count": len(overlap),
        "overlap_direct_union_addresses": sorted(overlap),
        "backtrack_path_count": backtracks,
        "max_frontier_distinct_neighbors": max_neighbors,
        "max_seed_novel_fanout": max(map(len, per_seed.values()), default=0),
        "second_edge_path_fanout_by_family": dict(sorted(fanout_family.items())),
        "second_edge_path_fanout_by_direction": dict(sorted(fanout_direction.items())),
        "path_combinations": dict(sorted(combinations.items())),
        "lexical_volume_comparator": {
            "requested": count,
            "addresses": comparator,
            "actual": len(comparator),
            "exhausted": len(comparator) < count,
        },
        "relation_diagnostics": diagnostics,
    }


def summarize(cases: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Describe natural reach and fan-out without ranking or pruning."""
    candidates = [row for case in cases for row in case["candidates"]]
    families: Counter[str] = Counter()
    directions: Counter[str] = Counter()
    combinations: Counter[str] = Counter()
    for case in cases:
        families.update(case["second_edge_path_fanout_by_family"])
        directions.update(case["second_edge_path_fanout_by_direction"])
        combinations.update(case["path_combinations"])
    return {
        "development_cases": len(cases),
        "frontier_case_resource_pairs": sum(case["frontier_count"] for case in cases),
        "frontier_first_supports": sum(
            case["frontier_first_support_count"] for case in cases
        ),
        "cases_with_novelty": sum(bool(case["candidate_count"]) for case in cases),
        "candidate_pairs": len(candidates),
        "distinct_candidate_addresses": len({row["address"] for row in candidates}),
        "retained_typed_paths": sum(row["support_count"] for row in candidates),
        "max_case_novelty": max((case["candidate_count"] for case in cases), default=0),
        "max_seed_novel_fanout": max(
            (case["max_seed_novel_fanout"] for case in cases), default=0
        ),
        "max_frontier_distinct_neighbors": max(
            (case["max_frontier_distinct_neighbors"] for case in cases), default=0
        ),
        "direct_union_overlap_case_resource_pairs": sum(
            case["overlap_direct_union_count"] for case in cases
        ),
        "backtrack_paths": sum(case["backtrack_path_count"] for case in cases),
        "second_edge_path_fanout_by_family": dict(sorted(families.items())),
        "second_edge_path_fanout_by_direction": dict(sorted(directions.items())),
        "path_combinations": dict(sorted(combinations.items())),
        "lexical_comparator_requested": sum(
            case["lexical_volume_comparator"]["requested"] for case in cases
        ),
        "lexical_comparator_actual": sum(
            case["lexical_volume_comparator"]["actual"] for case in cases
        ),
        "lexical_comparator_exhausted_cases": sum(
            case["lexical_volume_comparator"]["exhausted"] for case in cases
        ),
        "case_candidate_counts": {
            str(case["case_id"]): case["candidate_count"] for case in cases
        },
    }


def run_mechanics(*, repository_root: Path, root: Path = ROOT) -> dict[str, Any]:
    """Persist one complete candidate surface without reading outcomes."""
    frozen = build_freeze(root)
    if _read_json(root / FREEZE_NAME) != frozen:
        raise ValueError("Graph-1 protocol must be frozen before mechanics.")
    imports, lexical, references, containment, mirrors = _sources(root)
    population = cast(
        "dict[str, Any]",
        _read_json(root.parent / "increment_25" / "task_population_freeze.json"),
    )
    cards = {
        str(row["case_id"]): _task_card(row)
        for row in population["payload"]["task_cards"]
        if row["case_id"] in frozen["payload"]["development_case_ids"]
    }
    if len(cards) != 24:
        raise ValueError("Graph-1 development cards are incomplete.")
    cases: list[dict[str, Any]] = []
    for group in zip(
        *(
            source["cases"]
            for source in (imports, lexical, references, containment, mirrors)
        ),
        strict=True,
    ):
        original, ranking, ref_case, package_case, mirror_case = group
        card = cards[str(original["case_id"])]
        if any(
            row["case_id"] != original["case_id"]
            or row["parent_snapshot_sha"] != card.parent_snapshot_sha
            for row in group
        ):
            raise ValueError("Graph-1 source case/snapshot identity differs.")
        if original["information_need"] != {
            "purpose": card.information_need_purpose,
            "lexical_query": card.lexical_query,
        }:
            raise ValueError("Graph-1 InformationNeed differs.")
        with tempfile.TemporaryDirectory(prefix="devtools-i32-graph1-") as raw:
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
                str(corpus.snapshot.id) != original["snapshot_id"]
                or len(corpus.addresses) != original["corpus_resource_count"]
            ):
                raise ValueError("Graph-1 historical parent corpus differs.")
            edges, diagnostics = incident_edges(corpus, card.corpus_source_roots)
            cases.append(
                project_case(
                    imports=original,
                    lexical=ranking,
                    references=ref_case,
                    containment=package_case,
                    mirrors=mirror_case,
                    edges=edges,
                    diagnostics=diagnostics,
                )
            )
    if [case["case_id"] for case in cases] != frozen["payload"]["development_case_ids"]:
        raise ValueError("Graph-1 candidate population escaped development.")
    artifact = {
        "schema": "devtools-i32-graph-round-one-candidates-v1",
        "freeze_identity": frozen["content_identity"],
        "judgments_loaded": False,
        "heldout_executed": False,
        "cases": cases,
        "summary": summarize(cases),
    }
    artifact["content_identity"] = _digest(artifact)
    path = root / CANDIDATES_NAME
    if path.exists() and _verified_json(path) != artifact:
        raise ValueError("Existing Graph-1 candidates differ.")
    write_artifact(path=path, payload=artifact)
    return artifact


if __name__ == "__main__":
    freeze_protocol()
    run_mechanics(repository_root=ROOT.parents[1])
