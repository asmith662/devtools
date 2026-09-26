# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, PLR2004, TRY003
"""Outcome-blind, one-relation module-import candidate generation."""

from __future__ import annotations

import gzip
import hashlib
import json
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from devtools.context.python.imports.declarations import (
    PythonImportParseError,
    derive_python_import_declarations,
)
from devtools.context.python.imports.relations import (
    derive_python_resolved_module_import_relations,
)
from devtools.context.python.imports.resolution import resolve_python_import_declaration
from devtools.context.python.modules import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from experiments.increment_25.development import (
    _build_snapshot_corpus,
    _materialize_git_snapshot,
    _task_card,
    write_artifact,
)
from experiments.increment_27.depth_diagnostic import (
    _read_json,
    canonical_json_bytes,
    sha256_file,
)
from experiments.increment_27.window_unit import (
    EXPECTED_I25_FREEZE_SHA256,
    audit_saved_baseline,
)

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from devtools.context.python.imports.relations import (
        PythonResolvedModuleImportRelation,
    )
    from devtools.context.python.modules import (
        PythonModuleInterpretation,
        PythonModuleInterpretationUniverse,
    )
    from experiments.increment_25.development import SnapshotCorpus

FREEZE_NAME = "structural_import_freeze.json"
MECHANICS_NAME = "structural_import_candidates.json.gz"
RAW_CANDIDATE_SHA256 = (
    "f42215df4ab75455f8a6fc5993993d81093f411b0835f449afe9ece16d6551b5"
)
GZIP_COMPRESSLEVEL = 9
DIRECTIONS = ("outgoing", "incoming")
METHODS = ("canonical", "bm25_plus", "identifier", "path", "rrf")


def _digest(value: object) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def read_candidate_artifact(path: Path) -> dict[str, Any]:
    """Read exact UTF-8 candidate JSON from its deterministic gzip envelope."""
    raw = gzip.decompress(path.read_bytes())
    if hashlib.sha256(raw).hexdigest() != RAW_CANDIDATE_SHA256:
        raise ValueError("Compressed candidate raw-byte identity differs.")
    artifact = json.loads(raw.decode("utf-8"))
    if not isinstance(artifact, dict) or raw != canonical_json_bytes(artifact):
        raise ValueError("Compressed candidate is not canonical JSON.")
    if artifact.get("content_identity") != _digest(
        {key: value for key, value in artifact.items() if key != "content_identity"}
    ):
        raise ValueError("Compressed candidate content identity differs.")
    return cast("dict[str, Any]", artifact)


def build_freeze(root: Path) -> dict[str, object]:
    """Bind one-hop rules to saved development inputs without reading labels."""
    cases, heldout = audit_saved_baseline(root)
    source_path = root.parent / "increment_25" / "task_population_freeze.json"
    if sha256_file(source_path) != EXPECTED_I25_FREEZE_SHA256:
        raise ValueError("Historical task-card freeze changed.")
    population = _read_json(root / "experiment_freeze.json")
    suspended = cast("dict[str, Any]", population["payload"])[
        "preserved_suspended_increment_26_confirmation"
    ]
    development_ids = [str(case["case_id"]) for case in cases]
    if (
        len(development_ids) != 24
        or len(set(development_ids)) != 24
        or set(development_ids) & set(heldout)
        or len(suspended["case_ids"]) != 16
    ):
        raise ValueError("Structural development population is invalid.")
    payload = {
        "development_case_ids": development_ids,
        "heldout_case_ids_sealed": heldout,
        "suspended_increment_26_case_ids_not_executed": suspended["case_ids"],
        "source_sha256": {
            name: sha256_file(root / name)
            for name in (
                "experiment_freeze.json",
                "canonical_positive_lexical_rankings.json",
                "lexical_comparison_rankings.json",
            )
        }
        | {"increment_25/task_population_freeze.json": sha256_file(source_path)},
        "seed": "saved canonical first five positive resource results, unchanged",
        "relation": "PythonResolvedModuleImportRelation, RESOLVED target and one source interpretation",
        "path_schemas": {
            "outgoing": "seed source module -> one directed resolved module-import relation -> target module resource",
            "incoming": "importer source module -> one directed resolved module-import relation -> seed target module; reverse lookup only",
        },
        "maximum_relation_count_per_path": 1,
        "source_roots": "exact frozen task-card corpus_source_roots",
        "module_roots": "each frozen corpus source root, no precedence",
        "projection": "endpoint resource address; exclude all seed addresses; deduplicate address while preserving every path",
        "lexical_control": "next m saved positive canonical results after the seed, independently per direction",
        "candidate_volume": "natural expansion; no structural result cap",
        "judgment_join_during_generation": False,
    }
    return {
        "schema": "devtools-i27-structural-import-freeze-v1",
        "content_identity": _digest(payload),
        "payload": payload,
    }


def freeze_protocol(root: Path) -> dict[str, object]:
    """Persist the protocol before deriving any new structural candidate."""
    artifact = build_freeze(root)
    path = root / FREEZE_NAME
    if path.exists() and _read_json(path) != artifact:
        raise ValueError("Existing structural-import freeze differs.")
    write_artifact(path=path, payload=artifact)
    return artifact


def _module_universe(
    corpus: SnapshotCorpus, roots: Sequence[str]
) -> tuple[
    PythonModuleInterpretationUniverse, dict[str, list[PythonModuleInterpretation]]
]:
    interpretations: list[PythonModuleInterpretation] = []
    for root in roots:
        addresses = tuple(
            address for address in corpus.addresses if address.parts[0] == root
        )
        analysis = interpret_python_module_resources(
            corpus.snapshot,
            module_root=PythonModuleRoot(root),
            resource_addresses=addresses,
        )
        interpretations.extend(analysis.interpretations)
    universe = define_python_module_interpretation_universe(
        repository_id=corpus.snapshot.repository_id,
        interpretations=interpretations,
    )
    by_address: dict[str, list[PythonModuleInterpretation]] = defaultdict(list)
    for item in interpretations:
        by_address[str(item.resource.address)].append(item)
    return universe, by_address


def _derive_relations(
    corpus: SnapshotCorpus,
    *,
    universe: PythonModuleInterpretationUniverse,
    by_address: Mapping[str, Sequence[PythonModuleInterpretation]],
) -> tuple[list[PythonResolvedModuleImportRelation], dict[str, Any]]:
    """Retain all direct-import qualification, including non-relational outcomes."""
    relations: list[PythonResolvedModuleImportRelation] = []
    sources: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    for address in corpus.addresses:
        source_address = str(address)
        if not source_address.endswith(".py"):
            continue
        interpretations = tuple(by_address.get(source_address, ()))
        try:
            analysis = derive_python_import_declarations(
                corpus.snapshot, resource_address=address
            )
        except PythonImportParseError as error:
            counts["parse_failed"] += 1
            sources.append(
                {
                    "address": source_address,
                    "status": "parse-failed",
                    "reason": str(error),
                }
            )
            continue
        resolutions = [
            resolve_python_import_declaration(
                analysis,
                declaration,
                target_universe=universe,
                source_interpretations=interpretations,
            )
            for declaration in analysis.declarations
        ]
        relation_analysis = derive_python_resolved_module_import_relations(
            analysis, resolutions=resolutions, source_interpretations=interpretations
        )
        relations.extend(relation_analysis.relations)
        counts["python_resources_parsed"] += 1
        counts["import_occurrences_examined"] += len(resolutions)
        counts[f"source_{relation_analysis.source_status.value}"] += 1
        source_resolutions: list[dict[str, Any]] = []
        for resolution in resolutions:
            declaration = resolution.declaration
            support = declaration.support
            counts[f"resolution_{resolution.outcome.value}"] += 1
            source_resolutions.append(
                {
                    "declaration_derivation_identity": declaration.derivation_identity,
                    "declaration_ordinal": declaration.declaration_ordinal,
                    "import_source_span": [
                        support.start_line,
                        support.start_column_utf8,
                        support.end_line,
                        support.end_column_utf8,
                    ],
                    "module_text": declaration.module,
                    "relative_level": declaration.level,
                    "imported_name": declaration.imported_name,
                    "local_alias": declaration.local_alias,
                    "resolution_identity": resolution.identity,
                    "resolution_outcome": resolution.outcome.value,
                    "requested_module": resolution.requested_module,
                    "matched_module_interpretation_ids": [
                        item.identity for item in resolution.matches
                    ],
                    "unsupported_reason": (
                        resolution.unsupported_reason.value
                        if resolution.unsupported_reason
                        else None
                    ),
                }
            )
        sources.append(
            {
                "address": source_address,
                "status": relation_analysis.source_status.value,
                "source_module_interpretation_ids": [
                    item.identity for item in interpretations
                ],
                "import_analysis_identity": analysis.derivation_identity,
                "resolutions": source_resolutions,
                "resolved_relation_ids": [
                    item.identity for item in relation_analysis.relations
                ],
            }
        )
    counts["resolved_relation_count"] = len(relations)
    return relations, {"counts": dict(sorted(counts.items())), "sources": sources}


def _support(relation: PythonResolvedModuleImportRelation) -> dict[str, object]:
    declaration = relation.resolution.declaration
    occurrence = declaration.support
    return {
        "relation_identity": relation.identity,
        "resolution_identity": relation.resolution.identity,
        "resolution_outcome": relation.resolution.outcome.value,
        "declaration_derivation_identity": declaration.derivation_identity,
        "declaration_ordinal": declaration.declaration_ordinal,
        "import_source_span": [
            occurrence.start_line,
            occurrence.start_column_utf8,
            occurrence.end_line,
            occurrence.end_column_utf8,
        ],
        "source_module_interpretation_identity": relation.source.identity,
        "source_resource": str(relation.source.resource.address),
        "target_module_interpretation_identity": relation.target.identity,
        "target_resource": str(relation.target.resource.address),
    }


def project_direction(
    *,
    direction: str,
    seeds: Sequence[Mapping[str, Any]],
    relations: Sequence[PythonResolvedModuleImportRelation],
    positive: Sequence[Mapping[str, Any]],
    lexical_rankings: Mapping[str, Sequence[Mapping[str, Any]]],
) -> dict[str, Any]:
    """Project one directed relation at most, retaining every native support."""
    if direction not in DIRECTIONS:
        raise ValueError("Unknown structural direction.")
    seed_addresses = {str(seed["address"]) for seed in seeds}
    by_address: dict[str, list[dict[str, object]]] = {}
    paths_per_seed: dict[str, int] = {}
    targets_per_seed: dict[str, int] = {}
    seed_overlap = 0
    duplicates_within = 0
    duplicates_across = 0
    for seed in seeds:
        seed_address = str(seed["address"])
        local: set[str] = set()
        path_count = 0
        for relation in relations:
            endpoint = relation.source if direction == "outgoing" else relation.target
            projected = relation.target if direction == "outgoing" else relation.source
            if endpoint.identity != seed.get("module_interpretation_identity"):
                continue
            path_count += 1
            candidate = str(projected.resource.address)
            if candidate in seed_addresses:
                seed_overlap += 1
                continue
            if candidate in local:
                duplicates_within += 1
            elif candidate in by_address:
                duplicates_across += 1
            local.add(candidate)
            by_address.setdefault(candidate, []).append(
                {
                    "direction": direction,
                    "seed_address": seed_address,
                    "seed_rank": seed["canonical_rank"],
                    "seed_module_interpretation_identity": seed[
                        "module_interpretation_identity"
                    ],
                    **_support(relation),
                }
            )
        paths_per_seed[seed_address] = path_count
        targets_per_seed[seed_address] = len(local)
    rank_maps = {
        method: {str(row["address"]): int(row["rank"]) for row in rows}
        for method, rows in lexical_rankings.items()
    }
    candidates = []
    for address, paths in by_address.items():
        canonical = rank_maps["canonical"].get(address)
        ranks = {method: rank_maps[method].get(address) for method in METHODS}
        candidates.append(
            {
                "address": address,
                "support_count": len(paths),
                "paths": paths,
                "canonical_positive_rank": canonical,
                "canonical_category": (
                    "no-positive-rank"
                    if canonical is None
                    else "top-five-overlap"
                    if canonical <= 5
                    else "deeper-positive-rank"
                ),
                "saved_positive_method_ranks": ranks,
                "absent_all_saved_positive_lexical": all(
                    rank is None for rank in ranks.values()
                ),
            }
        )
    m = len(candidates)
    control = [str(row["address"]) for row in positive[len(seeds) : len(seeds) + m]]
    return {
        "direction": direction,
        "candidates": candidates,
        "candidate_count": m,
        "relation_path_count": sum(paths_per_seed.values()),
        "retained_support_count": sum(
            len(cast("list[dict[str, object]]", item["paths"])) for item in candidates
        ),
        "paths_per_seed": paths_per_seed,
        "targets_per_seed": targets_per_seed,
        "duplicates_within_seeds": duplicates_within,
        "duplicates_across_seeds": duplicates_across,
        "seed_overlap_path_count": seed_overlap,
        "same_volume_lexical_control": {
            "requested_m": m,
            "addresses": control,
            "actual_count": len(control),
            "lexical_exhausted": len(control) < m,
        },
    }


def generate_case(
    *,
    corpus: SnapshotCorpus,
    baseline: Mapping[str, Any],
    comparison: Mapping[str, Any],
    roots: Sequence[str],
) -> dict[str, Any]:
    """Derive qualified relations and two separate one-relation projections."""
    positive = cast("list[dict[str, Any]]", baseline["positive_lexical_ordering"])
    rankings = cast("dict[str, list[dict[str, Any]]]", comparison["rankings"])
    if (
        len(positive) != baseline["positive_result_count"]
        or any(row["rank"] != rank for rank, row in enumerate(positive, 1))
        or len({row["address"] for row in positive}) != len(positive)
        or [str(address) for address in corpus.addresses]
        != sorted(str(address) for address in corpus.addresses)
    ):
        raise ValueError("Saved ranking or corpus order is invalid.")
    universe, by_address = _module_universe(corpus, roots)
    seeds: list[dict[str, Any]] = []
    for row in positive[:5]:
        address = str(row["address"])
        options = by_address.get(address, [])
        status = (
            "non-python-resource"
            if not address.endswith(".py")
            else "no-module-interpretation"
            if not options
            else "ambiguous-module-interpretation"
            if len(options) != 1
            else "eligible"
        )
        seeds.append(
            {
                "case_id": baseline["case_id"],
                "address": address,
                "canonical_rank": row["rank"],
                "status": status,
                "module_interpretation_identity": options[0].identity
                if len(options) == 1
                else None,
                "module_interpretation_ids": [item.identity for item in options],
            }
        )
    relations, derivation = _derive_relations(
        corpus, universe=universe, by_address=by_address
    )
    arms = {
        direction: project_direction(
            direction=direction,
            seeds=seeds,
            relations=relations,
            positive=positive,
            lexical_rankings=rankings,
        )
        for direction in DIRECTIONS
    }
    outgoing = {row["address"] for row in arms["outgoing"]["candidates"]}
    incoming = {row["address"] for row in arms["incoming"]["candidates"]}
    return {
        "case_id": baseline["case_id"],
        "parent_snapshot_sha": baseline["parent_snapshot_sha"],
        "information_need": baseline["information_need"],
        "corpus_id": corpus.corpus_id,
        "snapshot_id": str(corpus.snapshot.id),
        "corpus_resource_count": len(corpus.addresses),
        "module_universe_identity": universe.identity,
        "seed_count": len(seeds),
        "eligible_seed_count": sum(seed["status"] == "eligible" for seed in seeds),
        "seeds": seeds,
        "relation_derivation": derivation,
        "arms": arms,
        "outgoing_incoming_overlap": sorted(outgoing & incoming),
    }


def run_mechanics(*, repository_root: Path, root: Path) -> dict[str, Any]:
    """Persist the outcome-blind 24-case candidate artifact before any label load."""
    freeze = build_freeze(root)
    if _read_json(root / FREEZE_NAME) != freeze:
        raise ValueError("Structural-import protocol was not frozen unchanged.")
    baseline, heldout = audit_saved_baseline(root)
    comparison = _read_json(root / "lexical_comparison_rankings.json")
    compared = cast("list[dict[str, Any]]", comparison["cases"])
    task_freeze = _read_json(
        root.parent / "increment_25" / "task_population_freeze.json"
    )
    task_cards = cast("dict[str, Any]", task_freeze["payload"])["task_cards"]
    cards = {str(row["case_id"]): _task_card(row) for row in task_cards}
    allowed = cast(
        "list[str]", cast("dict[str, Any]", freeze["payload"])["development_case_ids"]
    )
    cases: list[dict[str, Any]] = []
    for base, other in zip(baseline, compared, strict=True):
        case_id = str(base["case_id"])
        if case_id != allowed[len(cases)] or case_id in heldout:
            raise ValueError("Attempted to execute outside the 24 development cases.")
        card = cards[case_id]
        if (
            card.parent_snapshot_sha != base["parent_snapshot_sha"]
            or card.lexical_query != base["information_need"]["lexical_query"]
            or card.information_need_purpose != base["information_need"]["purpose"]
            or other["parent_snapshot_sha"] != card.parent_snapshot_sha
        ):
            raise ValueError("Frozen task, baseline, and comparison case differ.")
        with tempfile.TemporaryDirectory(
            prefix=f"devtools-i27-import-{case_id}-"
        ) as raw:
            snapshot_root = Path(raw)
            _materialize_git_snapshot(
                repository_root=repository_root,
                snapshot_sha=card.parent_snapshot_sha,
                source_roots=card.corpus_source_roots,
                destination=snapshot_root,
            )
            corpus = _build_snapshot_corpus(
                snapshot_root=snapshot_root, source_roots=card.corpus_source_roots
            )
            if len(corpus.addresses) != base["corpus_resource_count"]:
                raise ValueError("Historical corpus differs from saved baseline.")
            cases.append(
                generate_case(
                    corpus=corpus,
                    baseline=base,
                    comparison=other,
                    roots=card.corpus_source_roots,
                )
            )
    if len(cases) != 24:
        raise ValueError("Structural mechanics did not execute exactly 24 cases.")
    artifact: dict[str, Any] = {
        "schema": "devtools-i27-structural-import-candidates-v1",
        "freeze_identity": freeze["content_identity"],
        "heldout_executed": False,
        "judgment_artifacts_loaded": False,
        "cases": cases,
    }
    artifact["content_identity"] = _digest(artifact)
    path = root / MECHANICS_NAME
    if path.exists() and read_candidate_artifact(path) != artifact:
        raise ValueError("Existing structural candidate artifact differs.")
    path.write_bytes(
        gzip.compress(
            canonical_json_bytes(artifact),
            compresslevel=GZIP_COMPRESSLEVEL,
            mtime=0,
        )
    )
    if read_candidate_artifact(path) != artifact:
        raise ValueError("Persisted structural candidate artifact differs.")
    return artifact
