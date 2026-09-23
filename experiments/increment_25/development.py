# Copyright (c) 2026
# ruff: noqa: E501
"""Development-only candidate generation for Increment 25.

The module composes existing Repository Intelligence and lexical retrieval
operations over Git-backed parent snapshots.  It deliberately contains no
usefulness judgment or retrieval-quality evaluation.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Final, cast

from devtools.context.python.imports.declarations import (
    derive_python_import_declarations,
)
from devtools.context.python.imports.members import (
    PythonImportedMemberResolution,
    PythonImportedMemberResolutionOutcome,
    resolve_python_imported_member,
)
from devtools.context.python.modules import (
    PythonModuleInterpretation,
    PythonModuleRoot,
    define_python_module_interpretation_universe,
    interpret_python_module_resources,
)
from devtools.context.repository.corpus import (
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import (
    discover_repository_resource_addresses,
)
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
from devtools.context.retrieval.lexical.index import (
    build_repository_text_lexical_inverted_index,
)
from devtools.context.retrieval.lexical.statistics import (
    calculate_repository_text_lexical_corpus_statistics,
)
from devtools.core.paths import resolve_path
from experiments.increment_25.task_population import TaskCard, validate_freeze

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from devtools.context.repository.snapshot import RepositorySnapshot
    from devtools.context.retrieval.lexical.index import (
        RepositoryTextLexicalInvertedIndex,
    )

SCHEMA: Final = "devtools-increment-25-development-candidates-v1"
JUDGMENT_SCHEMA: Final = "devtools-increment-25-development-judgment-input-v1"
EXECUTION_SEMANTICS: Final = "increment-25-development-generator-v1"
LEXICAL_SEED_SIZE: Final = 5
MAXIMUM_RESOURCES: Final = 20_000
MAXIMUM_TRAVERSAL_ENTRIES: Final = 40_000
MAXIMUM_RESOURCE_BYTES: Final = 1_048_576
REPOSITORY_ID: Final = "00000000-0000-4000-8000-000000000025"


class DevelopmentBoundaryError(ValueError):
    """Reject execution outside the frozen development partition."""


@dataclass(frozen=True, slots=True)
class FrozenDevelopment:
    """Validated freeze metadata and its only executable task cards."""

    freeze_identity: str
    cards: tuple[TaskCard, ...]
    development_case_ids: tuple[str, ...]
    confirmation_case_ids: frozenset[str]
    reserve_case_ids: frozenset[str]

    def require_case(self, case_id: str) -> TaskCard:
        """Return a development card or reject sealed/reserve/unknown execution."""
        if case_id in self.confirmation_case_ids:
            msg = f"Confirmation case is sealed and cannot execute: {case_id}."
            raise DevelopmentBoundaryError(msg)
        if case_id in self.reserve_case_ids:
            msg = f"Reserve case cannot execute in development mode: {case_id}."
            raise DevelopmentBoundaryError(msg)
        for card in self.cards:
            if card.case_id == case_id:
                return card
        msg = f"Case is not in the frozen development partition: {case_id}."
        raise DevelopmentBoundaryError(msg)


@dataclass(frozen=True, slots=True)
class SnapshotCorpus:
    """Canonical corpus components built from one materialized parent snapshot."""

    snapshot: RepositorySnapshot
    index: RepositoryTextLexicalInvertedIndex
    addresses: tuple[RepositoryResourceAddress, ...]
    corpus_id: str


def load_frozen_development(path: Path) -> FrozenDevelopment:
    """Load and validate the committed freeze, exposing development cards only."""
    envelope = cast(
        "dict[str, object]",
        json.loads(path.read_text(encoding="utf-8")),
    )
    if not validate_freeze(envelope):
        msg = "Increment-25 task-population freeze failed validation."
        raise ValueError(msg)
    payload = envelope["payload"]
    if not isinstance(payload, dict):
        msg = "Validated Increment-25 freeze has no mapping payload."
        raise TypeError(msg)
    split = cast("dict[str, list[str]]", payload["split"])
    development_ids = tuple(split["development_case_ids"])
    confirmation_ids = frozenset(split["confirmation_case_ids"])
    reserve_ids = frozenset(split["reserve_case_ids"])
    if (set(development_ids) & confirmation_ids) or (
        set(development_ids) & reserve_ids
    ) or (confirmation_ids & reserve_ids):
        msg = "Frozen Increment-25 partitions overlap."
        raise ValueError(msg)
    cards_by_id = {
        str(item["case_id"]): _task_card(item)
        for item in cast("list[dict[str, object]]", payload["task_cards"])
    }
    if any(case_id not in cards_by_id for case_id in development_ids):
        msg = "Frozen development partition references a missing task card."
        raise ValueError(msg)
    cards = tuple(cards_by_id[case_id] for case_id in development_ids)
    return FrozenDevelopment(
        freeze_identity=str(envelope["content_identity"]),
        cards=cards,
        development_case_ids=development_ids,
        confirmation_case_ids=confirmation_ids,
        reserve_case_ids=reserve_ids,
    )


def run_development(
    *, repository_root: Path, freeze_path: Path,
) -> tuple[dict[str, object], dict[str, object]]:
    """Execute all and only frozen development cases and return two artifacts."""
    frozen = load_frozen_development(freeze_path)
    case_payloads: list[dict[str, object]] = []
    judgment_cases: list[dict[str, object]] = []
    for case_id in frozen.development_case_ids:
        card = frozen.require_case(case_id)
        with tempfile.TemporaryDirectory(prefix=f"devtools-i25-{case_id}-") as raw:
            snapshot_root = Path(raw)
            _materialize_git_snapshot(
                repository_root=repository_root,
                snapshot_sha=card.parent_snapshot_sha,
                source_roots=card.corpus_source_roots,
                destination=snapshot_root,
            )
            corpus = _build_snapshot_corpus(
                snapshot_root=snapshot_root,
                source_roots=card.corpus_source_roots,
            )
            case = generate_case(card=card, corpus=corpus)
            case_payloads.append(case)
            judgment_cases.append(
                _judgment_case(card=card, case=case, snapshot=corpus.snapshot),
            )
    evidence: dict[str, object] = {
        "schema": SCHEMA,
        "execution": {
            "semantics": EXECUTION_SEMANTICS,
            "freeze_identity": frozen.freeze_identity,
            "mode": "development-only",
            "case_count": len(case_payloads),
            "canonical_lexical": "content BM25 + 0.25 * filename-stem BM25",
            "lexical_seed_size": LEXICAL_SEED_SIZE,
            "structural_rule": "outgoing resolved imported-member binding to defining resource; one facade; one hop",
        },
        "cases": case_payloads,
    }
    judgment: dict[str, object] = {
        "schema": JUDGMENT_SCHEMA,
        "execution_identity": _identity(evidence),
        "scope": "neutral development resources awaiting human judgment",
        "cases": judgment_cases,
    }
    _assert_candidate_artifact(evidence, frozen=frozen)
    _assert_judgment_artifact(judgment)
    return evidence, judgment


def generate_case(*, card: TaskCard, corpus: SnapshotCorpus) -> dict[str, object]:
    """Generate one frozen development candidate surface without adjudication."""
    query = analyze_repository_text_lexical_query(text=card.lexical_query)
    retrieval = retrieve_repository_text_documents_by_bm25(
        query=query,
        index=corpus.index,
        maximum_results=max(1, len(corpus.addresses)),
    )
    lexical = tuple(
        match.document_statistics.analysis.document.resource.address
        for match in retrieval.matches
    )
    scores = tuple(match.score for match in retrieval.matches)
    seed = lexical[:LEXICAL_SEED_SIZE]
    resolutions, per_seed_diagnostics = _resolve_seed_imported_members(
        snapshot=corpus.snapshot,
        addresses=corpus.addresses,
        source_roots=card.corpus_source_roots,
        seed=seed,
    )
    additions, provenance = _structural_additions(
        resolutions=resolutions,
        seed=seed,
    )
    m = len(additions)
    matched = lexical[len(seed) : len(seed) + m]
    lexical_ranks = {address: rank for rank, address in enumerate(lexical, start=1)}
    overlap = tuple(address for address in additions if address in set(matched))
    structural_only = tuple(address for address in additions if address not in set(matched))
    lexical_only = tuple(address for address in matched if address not in set(additions))
    aggregate_diagnostics = Counter[str]()
    for item in per_seed_diagnostics:
        for name, value in cast("dict[str, int]", item["counts"]).items():
            aggregate_diagnostics[name] += value
    return {
        "case_id": card.case_id,
        "parent_snapshot_sha": card.parent_snapshot_sha,
        "source_commit_sha": card.source_commit_sha,
        "information_need": {
            "purpose": card.information_need_purpose,
            "lexical_query": card.lexical_query,
            "maintenance_category": card.maintenance_category,
            "repository_domain": card.repository_domain,
            "corpus_source_roots": list(card.corpus_source_roots),
        },
        "corpus": {
            "snapshot_id": str(corpus.snapshot.id),
            "corpus_id": corpus.corpus_id,
            "resource_count": len(corpus.addresses),
            "addresses": [str(value) for value in corpus.addresses],
        },
        "positive_lexical_ordering": [
            {"rank": rank, "address": str(address), "score": score}
            for rank, (address, score) in enumerate(zip(lexical, scores, strict=True), start=1)
        ],
        "shared_lexical_seed": [str(value) for value in seed],
        "structural_additions": [
            {
                "address": str(address),
                "positive_lexical_rank": lexical_ranks.get(address),
                "has_positive_lexical_rank": address in lexical_ranks,
                "supports": provenance[address],
            }
            for address in additions
        ],
        "matched_lexical_additions": [str(value) for value in matched],
        "overlap": {
            "intersection": [str(value) for value in overlap],
            "structural_only": [str(value) for value in structural_only],
            "lexical_only": [str(value) for value in lexical_only],
        },
        "capacity": {
            "m": m,
            "actual_lexical_control_additions": len(matched),
            "lexical_exhausted": len(matched) < m,
        },
        "resolution_diagnostics": {
            "by_seed": per_seed_diagnostics,
            "aggregate": dict(sorted(aggregate_diagnostics.items())),
        },
    }


def write_artifact(*, path: Path, payload: Mapping[str, object]) -> None:
    """Write deterministic experiment-local JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _task_card(item: dict[str, object]) -> TaskCard:
    return TaskCard(
        case_id=str(item["case_id"]),
        source_commit_sha=str(item["source_commit_sha"]),
        parent_snapshot_sha=str(item["parent_snapshot_sha"]),
        original_subject=str(item["original_subject"]),
        original_body=str(item["original_body"]),
        information_need_purpose=str(item["information_need_purpose"]),
        lexical_query=str(item["lexical_query"]),
        maintenance_category=str(item["maintenance_category"]),
        repository_domain=str(item["repository_domain"]),
        corpus_source_roots=tuple(cast("list[str]", item["corpus_source_roots"])),
        evaluator_only_changed_paths=tuple(cast("list[str]", item["evaluator_only_changed_paths"])),
    )


def _git(repository_root: Path, *arguments: str) -> bytes:
    completed = subprocess.run(  # noqa: S603
        ("git", *arguments),  # noqa: S607
        cwd=repository_root,
        check=True,
        capture_output=True,
    )
    return completed.stdout


def _materialize_git_snapshot(
    *, repository_root: Path, snapshot_sha: str, source_roots: Sequence[str], destination: Path,
) -> None:
    """Materialize tracked blobs from a commit without changing the worktree."""
    records = _git(
        repository_root,
        "ls-tree",
        "-r",
        "-z",
        "--full-tree",
        snapshot_sha,
        "--",
        *source_roots,
    ).split(b"\0")
    for record in records:
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", maxsplit=1)
        mode, object_type, object_sha = metadata.decode("ascii").split()
        if object_type != "blob" or mode == "120000":
            continue
        address = RepositoryResourceAddress(raw_path.decode("utf-8"))
        if address.parts[0] not in source_roots:
            msg = f"Git materialization escaped frozen source roots: {address}."
            raise RuntimeError(msg)
        target = destination.joinpath(*address.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(_git(repository_root, "cat-file", "blob", object_sha))


def _build_snapshot_corpus(
    *, snapshot_root: Path, source_roots: Sequence[str],
) -> SnapshotCorpus:
    repository = Repository(RepositoryId.parse(REPOSITORY_ID))
    root = resolve_path(snapshot_root)
    discovery = discover_repository_resource_addresses(
        repository=repository,
        root=root,
        maximum_resource_count=MAXIMUM_RESOURCES,
        maximum_traversal_entry_count=MAXIMUM_TRAVERSAL_ENTRIES,
    )
    selected = tuple(
        address for address in discovery.addresses if address.parts[0] in source_roots
    )
    definition = define_repository_text_corpus(
        discovery=discovery,
        selected_addresses=selected,
    )
    snapshot = observe_repository_resources(
        repository=repository,
        root=root,
        addresses=definition.selected_addresses,
        maximum_resource_bytes=MAXIMUM_RESOURCE_BYTES,
    )
    corpus = realize_repository_text_corpus(definition=definition, snapshot=snapshot)
    documents = represent_repository_text_corpus(corpus=corpus)
    analysis = analyze_repository_text_document_collection(document_collection=documents)
    statistics = calculate_repository_text_lexical_corpus_statistics(
        collection_analysis=analysis,
    )
    index = build_repository_text_lexical_inverted_index(corpus_statistics=statistics)
    return SnapshotCorpus(
        snapshot=snapshot,
        index=index,
        addresses=definition.selected_addresses,
        corpus_id=str(corpus.id),
    )


def _module_interpretations(
    *, snapshot: RepositorySnapshot, addresses: tuple[RepositoryResourceAddress, ...], source_roots: Sequence[str],
) -> tuple[PythonModuleInterpretation, ...]:
    values: list[PythonModuleInterpretation] = []
    for root in source_roots:
        root_addresses = tuple(address for address in addresses if address.parts[0] == root)
        analysis = interpret_python_module_resources(
            snapshot,
            module_root=PythonModuleRoot(root),
            resource_addresses=root_addresses,
        )
        values.extend(analysis.interpretations)
    return tuple(values)


def _resolve_seed_imported_members(
    *, snapshot: RepositorySnapshot, addresses: tuple[RepositoryResourceAddress, ...], source_roots: Sequence[str], seed: tuple[RepositoryResourceAddress, ...],
) -> tuple[tuple[PythonImportedMemberResolution, ...], list[dict[str, object]]]:
    interpretations = _module_interpretations(
        snapshot=snapshot,
        addresses=addresses,
        source_roots=source_roots,
    )
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=interpretations,
    )
    by_address: dict[RepositoryResourceAddress, list[PythonModuleInterpretation]] = {}
    for interpretation in interpretations:
        by_address.setdefault(interpretation.resource.address, []).append(interpretation)
    all_resolutions: list[PythonImportedMemberResolution] = []
    diagnostics: list[dict[str, object]] = []
    seed_set = set(seed)
    for address in seed:
        counts = Counter(
            {
                "relevant_imported_member_observations_considered": 0,
                "resolved": 0,
                "unresolved_in_universe": 0,
                "ambiguous": 0,
                "unsupported": 0,
                "resolved_targets_already_in_seed": 0,
                "distinct_structural_additions": 0,
            },
        )
        local_targets: set[RepositoryResourceAddress] = set()
        if address.value.endswith(".py"):
            analysis = derive_python_import_declarations(snapshot, resource_address=address)
            for declaration in analysis.declarations:
                counts["relevant_imported_member_observations_considered"] += 1
                resolution = resolve_python_imported_member(
                    snapshot,
                    analysis,
                    declaration,
                    module_universe=universe,
                    source_interpretations=tuple(by_address.get(address, ())),
                )
                all_resolutions.append(resolution)
                counts[resolution.outcome.value.replace("-", "_")] += 1
                if resolution.outcome is PythonImportedMemberResolutionOutcome.RESOLVED:
                    target = cast("PythonModuleInterpretation", resolution.target)
                    if target.resource.address in seed_set:
                        counts["resolved_targets_already_in_seed"] += 1
                    else:
                        local_targets.add(target.resource.address)
        counts["distinct_structural_additions"] = len(local_targets)
        diagnostics.append({"seed": str(address), "counts": dict(counts)})
    return tuple(all_resolutions), diagnostics


def _structural_additions(
    *, resolutions: Sequence[PythonImportedMemberResolution], seed: Sequence[RepositoryResourceAddress],
) -> tuple[tuple[RepositoryResourceAddress, ...], dict[RepositoryResourceAddress, list[dict[str, object]]]]:
    seed_set = set(seed)
    ordered: list[RepositoryResourceAddress] = []
    provenance: dict[RepositoryResourceAddress, list[dict[str, object]]] = {}
    for resolution in resolutions:
        if resolution.outcome is not PythonImportedMemberResolutionOutcome.RESOLVED:
            continue
        target = cast("PythonModuleInterpretation", resolution.target)
        address = target.resource.address
        if address in seed_set:
            continue
        if address not in provenance:
            ordered.append(address)
            provenance[address] = []
        source = resolution.source_declaration.support
        binding = resolution.facade_bindings[0].support
        declaration = resolution.target_declaration
        if declaration is None:
            msg = "Resolved imported-member result lacks its target declaration."
            raise RuntimeError(msg)
        target_support = declaration.support
        target_range = target_support.source_range
        provenance[address].append(
            {
                "resolution_identity": resolution.identity,
                "source_resource": str(source.resource_address),
                "source_declaration_ordinal": resolution.source_declaration.declaration_ordinal,
                "source_location": [source.start_line, source.start_column_utf8, source.end_line, source.end_column_utf8],
                "facade_resource": str(cast("PythonModuleInterpretation", resolution.facade).resource.address),
                "facade_binding_resource": str(binding.resource_address),
                "target_resource": str(address),
                "target_function": declaration.declared_name,
                "target_location": [target_range.start_line, target_range.start_column_utf8, target_range.end_line, target_range.end_column_utf8],
            },
        )
    return tuple(ordered), provenance


def _judgment_case(
    *, card: TaskCard, case: dict[str, object], snapshot: RepositorySnapshot,
) -> dict[str, object]:
    structural = cast("list[dict[str, object]]", case["structural_additions"])
    matched = cast("list[str]", case["matched_lexical_additions"])
    addresses = sorted({str(item["address"]) for item in structural} | set(matched))
    return {
        "case_id": card.case_id,
        "task": {
            "purpose": card.information_need_purpose,
            "lexical_query": card.lexical_query,
            "maintenance_category": card.maintenance_category,
            "repository_domain": card.repository_domain,
            "parent_snapshot_sha": card.parent_snapshot_sha,
        },
        "resources": [
            {
                "address": address,
                "content": snapshot.resource_at(RepositoryResourceAddress(address)).content,
            }
            for address in addresses
        ],
    }


def _identity(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(),
    ).hexdigest()


def _all_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value) | set().union(*(_all_keys(item) for item in value.values()))
    if isinstance(value, list):
        return set().union(*(_all_keys(item) for item in value)) if value else set()
    return set()


def _assert_candidate_artifact(
    artifact: dict[str, object], *, frozen: FrozenDevelopment,
) -> None:
    cases = cast("list[dict[str, object]]", artifact["cases"])
    case_ids = tuple(str(case["case_id"]) for case in cases)
    if case_ids != frozen.development_case_ids:
        msg = "Development artifact does not contain exactly the frozen development cases."
        raise RuntimeError(msg)
    if set(case_ids) & (frozen.confirmation_case_ids | frozen.reserve_case_ids):
        msg = "Sealed or reserve outcomes contaminated the development artifact."
        raise RuntimeError(msg)
    prohibited = {"useful", "not_useful", "usefulness", "usefulness_labels", "metrics"}
    if _all_keys(artifact) & prohibited:
        msg = "Development candidate artifact contains prohibited adjudication data."
        raise RuntimeError(msg)


def _assert_judgment_artifact(artifact: dict[str, object]) -> None:
    prohibited = {
        "origin",
        "structural_additions",
        "matched_lexical_additions",
        "lexical_rank",
        "positive_lexical_rank",
        "supports",
        "support_count",
        "resolution_state",
        "structural_only",
        "lexical_only",
        "evaluator_only_changed_paths",
        "changed_paths",
        "useful",
        "not_useful",
        "usefulness",
    }
    leaked = _all_keys(artifact) & prohibited
    if leaked:
        msg = f"Blinded judgment artifact leaks prohibited fields: {sorted(leaked)}."
        raise RuntimeError(msg)
