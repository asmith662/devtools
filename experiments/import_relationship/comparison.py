# Copyright (c) 2026
# ruff: noqa: COM812, D103, E501, E701, F401, I001, PLR0911, PT018, S101
# mypy: disable-error-code="attr-defined,arg-type,index,misc,no-any-return,no-untyped-call,no-untyped-def,return-value"
"""Execute one bounded comparison using frozen import-relationship cases."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from devtools.context.python.imports import (
    PythonImportParseError,
    PythonImportResolutionOutcome,
    derive_python_import_declarations,
    derive_python_resolved_module_import_relations,
    resolve_python_import_declaration,
)
from devtools.context.python.modules import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.document import represent_repository_text_corpus
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.lexical.analysis import (
    analyze_repository_text_document_collection,
)
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from devtools.context.retrieval.lexical.index import build_repository_text_lexical_inverted_index
from devtools.context.retrieval.lexical.statistics import (
    calculate_repository_text_lexical_corpus_statistics,
)
from devtools.core.paths import resolve_path
from experiments.import_relationship_cases import (
    ImportRelationshipCase,
    ImportRelationshipDirection,
    import_relationship_cases,
)
from scripts.retrieval_bm25_baseline import select_benchmark_addresses

if TYPE_CHECKING:
    from devtools.context.python.modules import PythonModuleInterpretation

_K = 5
_REPOSITORY_ID = "d0e7c9e0-0c4f-4ea7-a345-3eb793ab6eb8"
_ROOTS = (
    ("src", "Installed src-layout root; supplies devtools.* module names."),
    ("tests", "Test-layout root; supplies test-module source interpretations."),
    ("scripts", "Operational entry-point root; supplies script module names."),
    ("experiments", "Experiment root; supplies experiment module names."),
)


@dataclass(frozen=True, slots=True)
class RelationRecord:
    """Serialize one exact declaration-grounded relation for experiment use."""

    identity: str
    source: PythonModuleInterpretation
    declaration: object
    resolution: object
    target: PythonModuleInterpretation


@dataclass(frozen=True, slots=True)
class Candidate:
    """One deduplicated resource candidate retaining every relation support."""

    address: RepositoryResourceAddress
    supports: tuple[RelationRecord, ...]


def expand_candidates(
    *,
    lexical_seeds: tuple[RepositoryResourceAddress, ...],
    interpretations_by_address: dict[RepositoryResourceAddress, tuple[PythonModuleInterpretation, ...]],
    relations: tuple[RelationRecord, ...],
    direction: ImportRelationshipDirection,
) -> tuple[tuple[dict[str, object], ...], tuple[Candidate, ...]]:
    """Project direct relations from eligible lexical seeds without ranking them."""
    participations: list[dict[str, object]] = []
    supports: dict[RepositoryResourceAddress, list[RelationRecord]] = defaultdict(list)
    for rank, seed in enumerate(lexical_seeds, start=1):
        interpretations = interpretations_by_address.get(seed, ())
        status = (
            "available" if len(interpretations) == 1 else "missing"
            if not interpretations else "ambiguous"
        )
        seed_supports: list[RelationRecord] = []
        if len(interpretations) == 1:
            interpretation = interpretations[0]
            for relation in relations:
                endpoint = relation.source if direction is ImportRelationshipDirection.OUTGOING else relation.target
                if endpoint.identity == interpretation.identity:
                    seed_supports.append(relation)
                    candidate = relation.target if direction is ImportRelationshipDirection.OUTGOING else relation.source
                    supports[candidate.resource.address].append(relation)
        participations.append({"address": str(seed), "rank": rank, "status": status, "interpretation_count": len(interpretations), "relation_count": len(seed_supports)})
    return tuple(participations), tuple(
        Candidate(address=address, supports=tuple(values))
        for address, values in supports.items()
    )


def fixed_k(
    *, lexical: tuple[RepositoryResourceAddress, ...], additions: tuple[RepositoryResourceAddress, ...]
) -> tuple[RepositoryResourceAddress, ...]:
    """Use Increment-16's fixed policy: rank one, additions, then lexical order."""
    return tuple(dict.fromkeys((*lexical[:1], *additions, *lexical)))[:_K]


def run_comparison(*, repository_root: Path) -> dict[str, object]:
    """Run the one allowed real-repository import-relationship comparison."""
    repository = Repository(RepositoryId.parse(_REPOSITORY_ID))
    root = resolve_path(repository_root)
    discovery = discover_repository_resource_addresses(repository=repository, root=root, maximum_resource_count=10_000, maximum_traversal_entry_count=20_000)
    definition = define_repository_text_corpus(discovery=discovery, selected_addresses=select_benchmark_addresses(discovery=discovery))
    snapshot = observe_repository_resources(repository=repository, root=root, addresses=definition.selected_addresses, maximum_resource_bytes=1_048_576)
    corpus = realize_repository_text_corpus(definition=definition, snapshot=snapshot)
    documents = represent_repository_text_corpus(corpus=corpus)
    statistics = calculate_repository_text_lexical_corpus_statistics(collection_analysis=analyze_repository_text_document_collection(document_collection=documents))
    index = build_repository_text_lexical_inverted_index(corpus_statistics=statistics)
    python_addresses = tuple(item.address for item in snapshot.resources if item.address.value.endswith(".py"))
    root_analyses = tuple(interpret_python_module_resources(snapshot, module_root=PythonModuleRoot(value), resource_addresses=python_addresses) for value, _reason in _ROOTS)
    interpretations = tuple(item for analysis in root_analyses for item in analysis.interpretations)
    by_address: dict[RepositoryResourceAddress, list[PythonModuleInterpretation]] = defaultdict(list)
    for interpretation in interpretations:
        by_address[interpretation.resource.address].append(interpretation)
    universe = define_python_module_interpretation_universe(repository_id=snapshot.repository_id, interpretations=interpretations)
    records: list[RelationRecord] = []
    outcomes: dict[str, int] = defaultdict(int)
    source_statuses: dict[str, int] = defaultdict(int)
    declaration_count = 0
    parse_errors = 0
    for address in python_addresses:
        try:
            analysis = derive_python_import_declarations(snapshot, resource_address=address)
        except PythonImportParseError:
            parse_errors += 1
            continue
        declaration_count += len(analysis.declarations)
        source_values = tuple(by_address[address])
        resolutions = tuple(resolve_python_import_declaration(analysis, declaration, target_universe=universe, source_interpretations=source_values) for declaration in analysis.declarations)
        for resolution in resolutions:
            outcomes[resolution.outcome.value] += 1
        derived = derive_python_resolved_module_import_relations(analysis, resolutions=resolutions, source_interpretations=source_values)
        source_statuses[derived.source_status.value] += 1
        records.extend(RelationRecord(relation.identity, relation.source, relation.declaration, relation.resolution, relation.target) for relation in derived.relations)
    lexical_cases = tuple(_lexical_case(case=case, index=index) for case in import_relationship_cases())
    variants = {
        f"{direction.value}-seed-{count}": _variant_cases(lexical_cases=lexical_cases, direction=direction, seed_count=count, interpretations_by_address={key: tuple(value) for key, value in by_address.items()}, relations=tuple(records))
        for direction in ImportRelationshipDirection for count in (1, 3)
    }
    return {
        "schema": "devtools-b0002-import-relationship-comparison-v1",
        "scope": "experiment-only one-hop declaration-grounded resolved repository module-import candidates",
        "checkpoint": {"head": "d493c26bbb1866cb9e5ead8f23f02aac3a7f12b9", "snapshot_id": str(snapshot.id), "corpus_id": str(corpus.id), "document_count": len(documents.documents), "python_resource_count": len(python_addresses), "bounds": {"maximum_discovered_resources": 10000, "maximum_traversal_entries": 20000, "maximum_resource_bytes": 1048576}},
        "module_roots": [{"root": value, "rationale": rationale} for value, rationale in _ROOTS],
        "lexical_configuration": {"canonical": "content-bm25 + 0.25 filename-stem-bm25", "k": _K, "seed_counts": [1, 3]},
        "relation_semantics": "declaration-grounded-repository-module-import-relation-v1",
        "coverage": {"module_interpretation_count": len(interpretations), "declaration_count": declaration_count, "parse_error_count": parse_errors, "resolution_outcomes": dict(outcomes), "relation_count": len(records), "source_statuses": dict(source_statuses)},
        "frozen_cases": [_case_definition(case) for case in import_relationship_cases()],
        "canonical_lexical": {"cases": lexical_cases, "metrics": _metrics(lexical_cases, "lexical")},
        "variants": {name: {"cases": values, "metrics": _metrics(values, "fixed_k"), "augmentation": _augmentation_summary(values)} for name, values in variants.items()},
    }


def _lexical_case(*, case: ImportRelationshipCase, index: object) -> dict[str, object]:
    result = retrieve_repository_text_documents_by_bm25(query=analyze_repository_text_lexical_query(text=case.query_text), index=index, maximum_results=_K)
    return {"case": case, "lexical": tuple(match.document_statistics.analysis.document.resource.address for match in result.matches), "lexical_scores": tuple(match.score for match in result.matches)}


def _variant_cases(*, lexical_cases: tuple[dict[str, object], ...], direction: ImportRelationshipDirection, seed_count: int, interpretations_by_address: dict[RepositoryResourceAddress, tuple[PythonModuleInterpretation, ...]], relations: tuple[RelationRecord, ...]) -> tuple[dict[str, object], ...]:
    values = []
    for item in lexical_cases:
        lexical = item["lexical"]
        case = item["case"]
        assert isinstance(lexical, tuple) and isinstance(case, ImportRelationshipCase)
        participation, candidates = expand_candidates(lexical_seeds=lexical[:seed_count], interpretations_by_address=interpretations_by_address, relations=relations, direction=direction)
        additions = tuple(candidate.address for candidate in candidates if candidate.address not in lexical)
        selected = fixed_k(lexical=lexical, additions=additions)
        relevant = set(case.relevant_resource_addresses)
        controls = set(case.negative_control_resource_addresses)
        values.append({**item, "direction": direction.value, "seed_count": seed_count, "seed_participation": participation, "candidates": candidates, "candidate_fan_out": {"candidate_count": len(candidates), "support_count": sum(len(candidate.supports) for candidate in candidates), "maximum_candidate_supports": max((len(candidate.supports) for candidate in candidates), default=0)}, "augmentation": (*lexical, *additions), "additions": additions, "augmentation_new_relevant": tuple(address for address in additions if address in relevant), "augmentation_controls": tuple(address for address in additions if address in controls), "fixed_k": selected, "fixed_k_new_relevant": tuple(address for address in selected if address in relevant and address not in lexical), "relevant_losses": tuple(address for address in lexical if address in relevant and address not in selected), "fixed_k_controls": tuple(address for address in selected if address in controls and address not in lexical), "displacements": tuple({"lexical": str(old), "fixed_k": str(new)} for old, new in zip(lexical, selected, strict=False) if old != new)})
    return tuple(values)


def _metrics(items: tuple[dict[str, object], ...], ranking_key: str) -> dict[str, float]:
    hits, recalls, reciprocal = [], [], []
    for item in items:
        case = item["case"]
        ranking = item[ranking_key]
        assert isinstance(case, ImportRelationshipCase) and isinstance(ranking, tuple)
        relevant = set(case.relevant_resource_addresses)
        recovered = [address for address in ranking if address in relevant]
        hits.append(bool(recovered))
        recalls.append(len(recovered) / len(relevant))
        reciprocal.append(next((1 / rank for rank, address in enumerate(ranking, 1) if address in relevant), 0.0))
    return {"hit_at_5": sum(hits) / len(hits), "mean_recall_at_5": sum(recalls) / len(recalls), "mrr": sum(reciprocal) / len(reciprocal)}


def _case_definition(case: ImportRelationshipCase) -> dict[str, object]:
    return {"name": case.name, "query": case.query_text, "seed": str(case.lexical_seed_resource_address), "direction": case.direction.value, "relevant": [str(item) for item in case.relevant_resource_addresses], "relevant_rationales": list(case.relevant_rationales), "controls": [str(item) for item in case.negative_control_resource_addresses], "control_rationales": list(case.negative_control_rationales)}


def _augmentation_summary(values: tuple[dict[str, object], ...]) -> dict[str, int]:
    return {"case_count": len(values), "candidate_count": sum(len(item["additions"]) for item in values), "cases_with_new_relevant": sum(bool(item["augmentation_new_relevant"]) for item in values), "new_relevant_count": sum(len(item["augmentation_new_relevant"]) for item in values), "control_exposure_count": sum(len(item["augmentation_controls"]) for item in values), "maximum_direct_fan_out": max((item["candidate_fan_out"]["candidate_count"] for item in values), default=0)}


def write_report(*, path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(_payload(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def _payload(value: object) -> object:
    if isinstance(value, RepositoryResourceAddress): return str(value)
    if isinstance(value, ImportRelationshipCase): return _case_definition(value)
    if isinstance(value, RelationRecord): return {"identity": value.identity, "source": _interpretation(value.source), "declaration": _declaration(value.declaration), "resolution": _resolution(value.resolution), "target": _interpretation(value.target)}
    if isinstance(value, Candidate): return {"address": str(value.address), "supports": [_payload(item) for item in value.supports]}
    if isinstance(value, tuple): return [_payload(item) for item in value]
    if isinstance(value, list): return [_payload(item) for item in value]
    if isinstance(value, dict): return {str(key): _payload(item) for key, item in value.items()}
    return value


def _interpretation(value: PythonModuleInterpretation) -> dict[str, str]:
    return {"address": str(value.resource.address), "root": value.module_root.value, "dotted_name": value.dotted_name, "kind": value.kind.value, "identity": value.identity}


def _declaration(value: object) -> dict[str, object]:
    return {"ordinal": value.declaration_ordinal, "module": value.module, "level": value.level, "imported_name": value.imported_name, "local_alias": value.local_alias, "support": {"address": str(value.support.resource_address), "start_line": value.support.start_line, "start_column_utf8": value.support.start_column_utf8, "end_line": value.support.end_line, "end_column_utf8": value.support.end_column_utf8}}


def _resolution(value: object) -> dict[str, object]:
    return {"identity": value.identity, "outcome": value.outcome.value, "requested_module": value.requested_module, "unsupported_reason": value.unsupported_reason.value if value.unsupported_reason else None, "matches": [_interpretation(item) for item in value.matches]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--report-path", type=Path, default=Path(".b0002-import-relationship-comparison.json"))
    parsed = parser.parse_args()
    write_report(
        path=parsed.report_path,
        payload=run_comparison(repository_root=parsed.repository_root.resolve()),
    )


if __name__ == "__main__": main()
