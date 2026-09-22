# Copyright (c) 2026
# ruff: noqa: COM812, D103, D401, E501, E701, E702, I001, SIM101
# mypy: disable-error-code="assignment,attr-defined,arg-type,index,no-any-return,no-untyped-call,no-untyped-def,return-value"
"""Bounded oracle-headroom evaluation over lexical and import surfaces.

This is an evaluator.  It neither implements nor proposes a selection policy.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from devtools.context.python.imports import (
    PythonImportParseError,
    derive_python_import_declarations,
    derive_python_resolved_module_import_relations,
    resolve_python_import_declaration,
)
from devtools.context.python.modules import (
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.repository.corpus import define_repository_text_corpus, realize_repository_text_corpus
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.context.repository.document import represent_repository_text_corpus
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import observe_repository_resources
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.lexical.analysis import analyze_repository_text_document_collection
from devtools.context.retrieval.lexical.bm25 import analyze_repository_text_lexical_query, retrieve_repository_text_documents_by_bm25
from devtools.context.retrieval.lexical.index import build_repository_text_lexical_inverted_index
from devtools.context.retrieval.lexical.statistics import calculate_repository_text_lexical_corpus_statistics
from devtools.core.paths import resolve_path
from experiments.import_relationship.comparison import RelationRecord
from experiments.import_relationship_cases import ImportRelationshipDirection
from experiments.purpose_relative_import.cases import PurposeRelativeNeed, ResourceJudgment, UsefulnessJudgment, purpose_relative_needs
from scripts.retrieval_bm25_baseline import select_benchmark_addresses

if TYPE_CHECKING:
    from devtools.context.python.modules import PythonModuleInterpretation

_K = 5
_LEXICAL_WIDTH = 15
_SEED_WIDTH = 3
_REPOSITORY_ID = "d0e7c9e0-0c4f-4ea7-a345-3eb793ab6eb8"
_CHECKPOINT_HEAD = "b76abf41b79cc71daae351309459eae2609885b6"
_ROOTS = (
    ("src", "Installed src-layout root; supplies devtools.* module names."),
    ("tests", "Test-layout root; supplies test-module source interpretations."),
    ("scripts", "Operational entry-point root; supplies script module names."),
    ("experiments", "Experiment root; supplies experiment module names."),
)


@dataclass(frozen=True, slots=True)
class RankedLexicalSurface:
    """One lexical retrieval observation, retaining native rank and score."""

    address: RepositoryResourceAddress
    rank: int
    score: float


@dataclass(frozen=True, slots=True)
class ImportRelationshipSurface:
    """One directional relation exposure from a ranked lexical seed."""

    address: RepositoryResourceAddress
    seed: RepositoryResourceAddress
    seed_rank: int
    direction: ImportRelationshipDirection
    relation: RelationRecord


def build_consideration_universe(
    *, lexical: tuple[RankedLexicalSurface, ...], relations: tuple[ImportRelationshipSurface, ...]
) -> dict[RepositoryResourceAddress, dict[str, object]]:
    """Ephemerally group typed surfaces by existing resource address only."""
    grouped: dict[RepositoryResourceAddress, dict[str, object]] = {}
    for surface in lexical:
        grouped.setdefault(surface.address, {"lexical": [], "relationships": []})["lexical"].append(surface)
    for surface in relations:
        grouped.setdefault(surface.address, {"lexical": [], "relationships": []})["relationships"].append(surface)
    return grouped


def evaluate_universe(
    *, need: PurposeRelativeNeed, universe: dict[RepositoryResourceAddress, dict[str, object]], canonical: tuple[RepositoryResourceAddress, ...], lexical_top_15: tuple[RepositoryResourceAddress, ...]
) -> dict[str, object]:
    """Apply frozen judgments only after a resource universe is constructed."""
    judgments = {item.address: item for item in need.judgments}
    addresses = tuple(universe)
    useful = tuple(address for address in addresses if judgments.get(address, _UNJUDGED).judgment is UsefulnessJudgment.USEFUL)
    not_useful = tuple(address for address in addresses if judgments.get(address, _UNJUDGED).judgment is UsefulnessJudgment.NOT_USEFUL)
    controls = tuple(address for address in not_useful if judgments[address].is_control)
    return {
        "size": len(addresses),
        "useful_present": useful,
        "candidate_recall": len(useful) / len(_useful_addresses(need)),
        "not_useful_present": not_useful,
        "controls_present": controls,
        "unjudged_present": tuple(address for address in addresses if address not in judgments),
        "useful_absent_canonical_present_lexical_width": tuple(address for address in useful if address not in canonical and address in lexical_top_15),
        "useful_absent_lexical_width_relationship_only": tuple(address for address in useful if address not in lexical_top_15 and universe[address]["relationships"]),
    }


_UNJUDGED = ResourceJudgment(RepositoryResourceAddress("__unjudged__"), UsefulnessJudgment.UNJUDGED, "sentinel")


def oracle_size_five(*, need: PurposeRelativeNeed, universe: dict[RepositoryResourceAddress, dict[str, object]]) -> dict[str, object]:
    """Evaluate best useful recall; address order is only a serialization tie-break."""
    useful = _useful_addresses(need)
    present = set(universe)
    admitted_useful = tuple(sorted(useful & present, key=str))[:_K]
    remainder = tuple(sorted(present - set(admitted_useful), key=str))
    subset = (*admitted_useful, *remainder)[:_K]
    return {
        "serialization_tie_break": "repository-resource-address lexical order only; not semantic ranking",
        "addresses": subset,
        "recall_at_5": len(set(subset) & useful) / len(useful),
        "useful_admitted": tuple(address for address in subset if address in useful),
        "not_useful_admitted": tuple(address for address in subset if _judgment_for(need, address).judgment is UsefulnessJudgment.NOT_USEFUL),
        "unjudged_admitted": tuple(address for address in subset if _judgment_for(need, address).judgment is UsefulnessJudgment.UNJUDGED),
        "useful_omitted_for_capacity": tuple(sorted((useful & present) - set(subset), key=str)),
    }


def blind_insert(*, canonical: tuple[RepositoryResourceAddress, ...], relationship_surfaces: tuple[ImportRelationshipSurface, ...]) -> tuple[RepositoryResourceAddress, ...]:
    """Fixed Increment-20-style negative control: rank one, raw relations, lexical."""
    relation_addresses = tuple(dict.fromkeys(surface.address for surface in relationship_surfaces if surface.address not in canonical))
    return tuple(dict.fromkeys((*canonical[:1], *relation_addresses, *canonical)))[:_K]


def run_comparison(*, repository_root: Path) -> dict[str, object]:
    """Acquire one bounded corpus and evaluate already frozen needs once."""
    repository = Repository(RepositoryId.parse(_REPOSITORY_ID))
    root = resolve_path(repository_root)
    discovery = discover_repository_resource_addresses(repository=repository, root=root, maximum_resource_count=10_000, maximum_traversal_entry_count=20_000)
    definition = define_repository_text_corpus(discovery=discovery, selected_addresses=select_benchmark_addresses(discovery=discovery))
    snapshot = observe_repository_resources(repository=repository, root=root, addresses=definition.selected_addresses, maximum_resource_bytes=1_048_576)
    corpus = realize_repository_text_corpus(definition=definition, snapshot=snapshot)
    documents = represent_repository_text_corpus(corpus=corpus)
    statistics = calculate_repository_text_lexical_corpus_statistics(collection_analysis=analyze_repository_text_document_collection(document_collection=documents))
    index = build_repository_text_lexical_inverted_index(corpus_statistics=statistics)
    relations, coverage, interpretations_by_address = _derive_relations(snapshot)
    cases = tuple(_evaluate_need(need=need, index=index, relations=relations, interpretations_by_address=interpretations_by_address) for need in purpose_relative_needs())
    return {
        "schema": "devtools-b0002-purpose-relative-oracle-headroom-v1",
        "scope": "experiment-only oracle evaluation; no selection policy or production retrieval behavior",
        "checkpoint": {"head": _CHECKPOINT_HEAD, "repository_id": _REPOSITORY_ID, "snapshot_id": str(snapshot.id), "corpus_id": str(corpus.id), "document_count": len(documents.documents), "bounds": {"maximum_discovered_resources": 10000, "maximum_traversal_entries": 20000, "maximum_resource_bytes": 1048576}},
        "configuration": {"canonical_lexical": "content-bm25 + 0.25 filename-stem-bm25", "k": _K, "lexical_consideration_width": _LEXICAL_WIDTH, "relationship_seed_width": _SEED_WIDTH, "relationship_depth": 1, "module_roots": [{"root": root, "rationale": rationale} for root, rationale in _ROOTS], "relation_semantics": "declaration-grounded-repository-module-import-relation-v1"},
        "relation_coverage": coverage,
        "frozen_needs": [_need_payload(need) for need in purpose_relative_needs()],
        "cases": cases,
        "aggregate": _aggregate(cases),
        "h1_same_query_pair": _h1(cases),
    }


def _derive_relations(snapshot: object) -> tuple[tuple[RelationRecord, ...], dict[str, object], dict[RepositoryResourceAddress, tuple[PythonModuleInterpretation, ...]]]:
    python_addresses = tuple(item.address for item in snapshot.resources if item.address.value.endswith(".py"))
    analyses = tuple(interpret_python_module_resources(snapshot, module_root=PythonModuleRoot(value), resource_addresses=python_addresses) for value, _ in _ROOTS)
    interpretations = tuple(item for analysis in analyses for item in analysis.interpretations)
    by_address: dict[RepositoryResourceAddress, list[PythonModuleInterpretation]] = defaultdict(list)
    for item in interpretations: by_address[item.resource.address].append(item)
    universe = define_python_module_interpretation_universe(repository_id=snapshot.repository_id, interpretations=interpretations)
    records: list[RelationRecord] = []; outcomes: dict[str, int] = defaultdict(int); statuses: dict[str, int] = defaultdict(int); declarations = 0; parse_errors = 0
    for address in python_addresses:
        try: analysis = derive_python_import_declarations(snapshot, resource_address=address)
        except PythonImportParseError: parse_errors += 1; continue
        declarations += len(analysis.declarations); source = tuple(by_address[address])
        resolutions = tuple(resolve_python_import_declaration(analysis, declaration, target_universe=universe, source_interpretations=source) for declaration in analysis.declarations)
        for resolution in resolutions: outcomes[resolution.outcome.value] += 1
        derived = derive_python_resolved_module_import_relations(analysis, resolutions=resolutions, source_interpretations=source)
        statuses[derived.source_status.value] += 1
        records.extend(RelationRecord(item.identity, item.source, item.declaration, item.resolution, item.target) for item in derived.relations)
    return tuple(records), {"python_resource_count": len(python_addresses), "module_interpretation_count": len(interpretations), "declaration_count": declarations, "parse_error_count": parse_errors, "resolution_outcomes": dict(outcomes), "source_statuses": dict(statuses), "relation_count": len(records)}, {address: tuple(values) for address, values in by_address.items()}


def _evaluate_need(*, need: PurposeRelativeNeed, index: object, relations: tuple[RelationRecord, ...], interpretations_by_address: dict[RepositoryResourceAddress, tuple[PythonModuleInterpretation, ...]]) -> dict[str, object]:
    result = retrieve_repository_text_documents_by_bm25(query=analyze_repository_text_lexical_query(text=need.query_text), index=index, maximum_results=_LEXICAL_WIDTH)
    lexical = tuple(RankedLexicalSurface(match.document_statistics.analysis.document.resource.address, rank, match.score) for rank, match in enumerate(result.matches, 1))
    canonical = tuple(surface.address for surface in lexical[:_K]); lexical_width = tuple(surface.address for surface in lexical)
    outgoing = _relationship_surfaces(lexical=lexical, relations=relations, interpretations_by_address=interpretations_by_address, direction=ImportRelationshipDirection.OUTGOING)
    incoming = _relationship_surfaces(lexical=lexical, relations=relations, interpretations_by_address=interpretations_by_address, direction=ImportRelationshipDirection.INCOMING)
    arms = {"A_canonical": (lexical[:_K], ()), "B_lexical_width": (lexical, ()), "C_outgoing": (lexical, outgoing), "D_incoming": (lexical, incoming), "E_bidirectional": (lexical, (*outgoing, *incoming))}
    payload: dict[str, object] = {"name": need.name, "canonical_ranking": lexical[:_K], "lexical_top_15": lexical, "relationship_surfaces": {"outgoing": outgoing, "incoming": incoming}, "arms": {}}
    for name, (lexical_surfaces, relationship_surfaces) in arms.items():
        universe = build_consideration_universe(lexical=lexical_surfaces, relations=relationship_surfaces)
        evaluation = evaluate_universe(need=need, universe=universe, canonical=canonical, lexical_top_15=lexical_width)
        oracle = None if name == "A_canonical" else oracle_size_five(need=need, universe=universe)
        blind = None if name in {"A_canonical", "B_lexical_width"} else blind_insert(canonical=canonical, relationship_surfaces=relationship_surfaces)
        payload["arms"][name] = {"universe": universe, "coverage": evaluation, "oracle": oracle, "blind_insertion": blind, "blind_recall_at_5": _recall(need, blind) if blind else None, "blind_controls": tuple(address for address in blind or () if _judgment_for(need, address).is_control)}
    canonical_recall = payload["arms"]["A_canonical"]["coverage"]["candidate_recall"]
    lexical_width_recall = payload["arms"]["B_lexical_width"]["oracle"]["recall_at_5"]
    for name in ("B_lexical_width", "C_outgoing", "D_incoming", "E_bidirectional"):
        oracle = payload["arms"][name]["oracle"]
        oracle["headroom_over_canonical_top5"] = oracle["recall_at_5"] - canonical_recall
        oracle["headroom_over_lexical_width"] = oracle["recall_at_5"] - lexical_width_recall
    payload["useful_resource_classification"] = _classify_useful(need, canonical, lexical_width, outgoing, incoming)
    return payload


def _relationship_surfaces(*, lexical: tuple[RankedLexicalSurface, ...], relations: tuple[RelationRecord, ...], interpretations_by_address: dict[RepositoryResourceAddress, tuple[PythonModuleInterpretation, ...]], direction: ImportRelationshipDirection) -> tuple[ImportRelationshipSurface, ...]:
    values: list[ImportRelationshipSurface] = []
    for seed in lexical[:_SEED_WIDTH]:
        interpretations = interpretations_by_address.get(seed.address, ())
        if len(interpretations) != 1: continue
        for relation in relations:
            endpoint = relation.source if direction is ImportRelationshipDirection.OUTGOING else relation.target
            if endpoint.identity == interpretations[0].identity:
                resource = relation.target.resource.address if direction is ImportRelationshipDirection.OUTGOING else relation.source.resource.address
                values.append(ImportRelationshipSurface(resource, seed.address, seed.rank, direction, relation))
    return tuple(values)


def _classify_useful(need: PurposeRelativeNeed, canonical: tuple[RepositoryResourceAddress, ...], lexical_width: tuple[RepositoryResourceAddress, ...], outgoing: tuple[ImportRelationshipSurface, ...], incoming: tuple[ImportRelationshipSurface, ...]) -> dict[str, tuple[RepositoryResourceAddress, ...]]:
    """Classify only frozen useful resources; absence makes no irrelevance claim."""
    outgoing_addresses = {surface.address for surface in outgoing}
    incoming_addresses = {surface.address for surface in incoming}
    buckets: dict[str, list[RepositoryResourceAddress]] = defaultdict(list)
    for address in sorted(_useful_addresses(need), key=str):
        if address in canonical: buckets["already_canonical_top_5"].append(address)
        elif address in lexical_width and address in outgoing_addresses | incoming_addresses: buckets["lexical_top_15_and_relationship_surfaced"].append(address)
        elif address in lexical_width: buckets["lexical_only_recovery_ranks_6_to_15"].append(address)
        elif address in outgoing_addresses and address in incoming_addresses: buckets["both_relationship_directions_beyond_lexical_top_15"].append(address)
        elif address in outgoing_addresses: buckets["outgoing_relationship_only_beyond_lexical_top_15"].append(address)
        elif address in incoming_addresses: buckets["incoming_relationship_only_beyond_lexical_top_15"].append(address)
        else: buckets["not_surfaced_in_fixed_universes"].append(address)
    return {name: tuple(values) for name, values in buckets.items()}


def _useful_addresses(need: PurposeRelativeNeed) -> set[RepositoryResourceAddress]: return {item.address for item in need.judgments if item.judgment is UsefulnessJudgment.USEFUL}
def _judgment_for(need: PurposeRelativeNeed, address: RepositoryResourceAddress) -> ResourceJudgment: return next((item for item in need.judgments if item.address == address), _UNJUDGED)
def _recall(need: PurposeRelativeNeed, addresses: tuple[RepositoryResourceAddress, ...] | None) -> float: return len(set(addresses or ()) & _useful_addresses(need)) / len(_useful_addresses(need))
def _need_payload(need: PurposeRelativeNeed) -> dict[str, object]: return {"name": need.name, "information_need": need.information_need, "query": need.query_text, "categories": sorted(need.categories), "judgments": [{"address": str(item.address), "judgment": item.judgment.value, "rationale": item.rationale, "is_control": item.is_control} for item in need.judgments]}
def _surface_payload(surface: object) -> object:
    if isinstance(surface, RepositoryResourceAddress): return str(surface)
    if isinstance(surface, RankedLexicalSurface): return {"address": str(surface.address), "rank": surface.rank, "score": surface.score}
    if isinstance(surface, ImportRelationshipSurface): return {"address": str(surface.address), "seed": str(surface.seed), "seed_rank": surface.seed_rank, "direction": surface.direction.value, "relation": {"identity": surface.relation.identity, "source": str(surface.relation.source.resource.address), "target": str(surface.relation.target.resource.address), "declaration_ordinal": surface.relation.declaration.declaration_ordinal, "resolution": surface.relation.resolution.outcome.value}}
    if isinstance(surface, tuple) or isinstance(surface, list): return [_surface_payload(item) for item in surface]
    if isinstance(surface, dict): return {str(key): _surface_payload(item) for key, item in surface.items()}
    return surface
def _aggregate(cases: tuple[dict[str, object], ...]) -> dict[str, object]:
    values = {}
    for arm in ("A_canonical", "B_lexical_width", "C_outgoing", "D_incoming", "E_bidirectional"):
        recalls = [case["arms"][arm]["oracle"]["recall_at_5"] if case["arms"][arm]["oracle"] else _recall(purpose_relative_needs()[index], tuple(item.address for item in case["canonical_ranking"])) for index, case in enumerate(cases)]
        values[arm] = {"mean_oracle_recall_at_5": sum(recalls) / len(recalls)}
    return values
def _h1(cases: tuple[dict[str, object], ...]) -> dict[str, object]:
    pair = {case["name"]: case for case in cases}; architecture = pair["context-disclosure-architecture"]; implementation = pair["context-disclosure-implementation"]
    return {"same_query": True, "canonical_rankings_identical": architecture["canonical_ranking"] == implementation["canonical_ranking"], "universes_identical_before_judgment": architecture["arms"]["E_bidirectional"]["universe"] == implementation["arms"]["E_bidirectional"]["universe"], "oracle_outcomes_differ": architecture["arms"]["E_bidirectional"]["oracle"] != implementation["arms"]["E_bidirectional"]["oracle"]}
def write_report(*, path: Path, payload: dict[str, object]) -> None: path.write_text(json.dumps(_surface_payload(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--repository-root", type=Path, default=Path.cwd()); parser.add_argument("--report-path", type=Path, default=Path(".b0002-purpose-relative-oracle-headroom.json")); parsed = parser.parse_args(); write_report(path=parsed.report_path, payload=run_comparison(repository_root=parsed.repository_root.resolve()))
if __name__ == "__main__": main()
