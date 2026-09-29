# Copyright (c) 2026
"""Freeze two lexical query arms and any justified direct structural evidence."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from devtools.context.retrieval.composition import (
    LexicalStructuralResourceEntry,
    LexicalStructuralResourceInventory,
    compose_lexical_structural_resource_evidence,
)
from devtools.context.retrieval.lexical.bm25 import (
    RepositoryTextLexicalBm25Match,
    RepositoryTextLexicalBm25RetrievalResult,
    RepositoryTextLexicalBm25Settings,
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from devtools.context.retrieval.structural import (
    PythonDirectStructuralRetrievalRequest,
    retrieve_python_direct_structural_resources,
)

if TYPE_CHECKING:
    from devtools.context.python.imports.relations import (
        PythonResolvedModuleImportRelation,
    )
    from devtools.context.python.modules.membership import (
        PythonImmediatePackageMembership,
    )
    from devtools.context.python.references.analysis import (
        PythonFunctionReferenceKnowledge,
    )
    from devtools.context.repository.resource import (
        RepositoryResourceAddress,
        RepositoryResourceOccurrence,
    )
    from devtools.context.repository.snapshot import (
        RepositorySnapshot,
        RepositorySnapshotId,
    )
    from devtools.context.retrieval.lexical.index import (
        RepositoryTextLexicalInvertedIndex,
    )
    from devtools.context.retrieval.structural import (
        PythonDirectStructuralResourceEvidence,
    )


@dataclass(frozen=True, slots=True)
class CodexDogfoodCase:
    """Inputs frozen before retrieval for one real development task.

    The lexical work bound is the complete eligible corpus size. It is not a
    relevance cutoff or a selected file budget. RI fact inputs are already
    derived and remain available for later audit.
    """

    snapshot: RepositorySnapshot
    index: RepositoryTextLexicalInvertedIndex
    full_prompt: str
    short_information_need: str
    seed_origins: tuple[tuple[RepositoryResourceAddress, str], ...]
    imports: tuple[PythonResolvedModuleImportRelation, ...] = ()
    references: tuple[PythonFunctionReferenceKnowledge, ...] = ()
    memberships: tuple[PythonImmediatePackageMembership, ...] = ()
    lexical_settings: RepositoryTextLexicalBm25Settings = field(
        default_factory=RepositoryTextLexicalBm25Settings,
    )

    def __post_init__(self) -> None:
        """Require a real task and qualified origins for any supplied seeds."""
        if not self.full_prompt.strip() or not self.short_information_need.strip():
            msg = "Dogfood task prompt and short InformationNeed must be nonempty."
            raise ValueError(msg)
        seeds = tuple(address for address, _ in self.seed_origins)
        if (
            len(set(seeds)) != len(seeds)
            or any(not origin.strip() for _, origin in self.seed_origins)
        ):
            msg = "Dogfood requires distinct seeds with explicit origin notes."
            raise ValueError(msg)

    @property
    def lexical_work_bound(self) -> int:
        """Permit every positive match, including in an empty corpus."""
        document_count = self.index.corpus_statistics.document_count
        return max(1, document_count)


@dataclass(frozen=True, slots=True)
class CodexDogfoodRetrievalCapture:
    """Keep each native query arm and a neutral, complete address handoff."""

    case: CodexDogfoodCase
    full_prompt_inventory: CodexDogfoodInventory
    short_need_inventory: CodexDogfoodInventory
    orientation_addresses: tuple[RepositoryResourceAddress, ...]


@dataclass(frozen=True, slots=True)
class CodexDogfoodLexicalEntry:
    """One snapshot resource with its native lexical match and rank."""

    resource: RepositoryResourceOccurrence
    lexical_rank: int
    lexical_match: RepositoryTextLexicalBm25Match


@dataclass(frozen=True, slots=True)
class CodexDogfoodLexicalInventory:
    """Keep a zero-seed arm's native result in neutral address order."""

    snapshot_id: RepositorySnapshotId
    purpose: str
    lexical_result: RepositoryTextLexicalBm25RetrievalResult
    resources: tuple[CodexDogfoodLexicalEntry, ...]


type CodexDogfoodInventory = (
    LexicalStructuralResourceInventory | CodexDogfoodLexicalInventory
)


def _require_lexical_snapshot(case: CodexDogfoodCase) -> None:
    """Check the full observed corpus, including resources with no BM25 match."""
    collection = case.index.corpus_statistics.collection_analysis.document_collection
    if (
        collection.corpus.definition.discovery.repository_id
        != case.snapshot.repository_id
    ):
        msg = "Lexical corpus belongs to another repository."
        raise ValueError(msg)
    if collection.corpus.resources != tuple(
        document.resource for document in collection.documents
    ):
        msg = "Lexical documents differ from their observed corpus."
        raise ValueError(msg)
    for document in collection.documents:
        if document.repository_id != case.snapshot.repository_id:
            msg = "Lexical document belongs to another repository."
            raise ValueError(msg)
        try:
            current = case.snapshot.resource_at(document.resource.address)
        except ValueError as error:
            msg = "Lexical corpus resource is absent from the supplied snapshot."
            raise ValueError(msg) from error
        if current != document.resource:
            msg = "Lexical corpus resource differs from the supplied snapshot."
            raise ValueError(msg)
    statistics = case.index.corpus_statistics.document_statistics
    if tuple(item.analysis.document for item in statistics) != collection.documents:
        msg = "Lexical index statistics differ from its document collection."
        raise ValueError(msg)


def _lexical_inventory(
    case: CodexDogfoodCase,
    lexical: RepositoryTextLexicalBm25RetrievalResult,
) -> CodexDogfoodLexicalInventory:
    """Orient matched resources without changing the native BM25 result."""
    entries = tuple(
        sorted(
            (
                CodexDogfoodLexicalEntry(
                    resource=match.document_statistics.analysis.document.resource,
                    lexical_rank=rank,
                    lexical_match=match,
                )
                for rank, match in enumerate(lexical.matches, start=1)
            ),
            key=lambda entry: str(entry.resource.address),
        ),
    )
    return CodexDogfoodLexicalInventory(
        snapshot_id=case.snapshot.id,
        purpose=case.short_information_need,
        lexical_result=lexical,
        resources=entries,
    )


def capture_codex_dogfood_retrieval(
    case: CodexDogfoodCase,
) -> CodexDogfoodRetrievalCapture:
    """Run production retrieval twice under identical corpus and settings."""
    structural = None
    if case.seed_origins:
        structural = retrieve_python_direct_structural_resources(
            case.snapshot,
            request=PythonDirectStructuralRetrievalRequest(
                purpose=case.short_information_need,
                seed_resources=tuple(address for address, _ in case.seed_origins),
            ),
            imports=case.imports,
            references=case.references,
            memberships=case.memberships,
        )
    else:
        _require_lexical_snapshot(case)

    def inventory(
        query_text: str,
    ) -> CodexDogfoodInventory:
        lexical = retrieve_repository_text_documents_by_bm25(
            query=analyze_repository_text_lexical_query(text=query_text),
            index=case.index,
            maximum_results=case.lexical_work_bound,
            settings=case.lexical_settings,
        )
        if structural is None:
            return _lexical_inventory(case, lexical)
        return compose_lexical_structural_resource_evidence(
            case.snapshot,
            purpose=case.short_information_need,
            lexical_result=lexical,
            structural_result=structural,
        )

    full = inventory(case.full_prompt)
    short = inventory(case.short_information_need)
    addresses = tuple(
        sorted(
            {
                entry.resource.address
                for result in (full, short)
                for entry in result.resources
            },
            key=str,
        ),
    )
    return CodexDogfoodRetrievalCapture(case, full, short, addresses)


def render_codex_dogfood_orientation(
    capture: CodexDogfoodRetrievalCapture,
) -> str:
    """Present every surfaced address with provenance, without ranking it."""
    full = {
        entry.resource.address: entry
        for entry in capture.full_prompt_inventory.resources
    }
    short = {
        entry.resource.address: entry
        for entry in capture.short_need_inventory.resources
    }
    corpus_id = (
        capture.case.index.corpus_statistics.collection_analysis.document_collection.corpus.id
    )
    lines = [
        "Advisory repository orientation; this list is not a sufficiency claim.",
        "Search and open any additional repository resources needed for the task.",
        f"Snapshot: {capture.case.snapshot.id}",
        f"Eligible corpus: {corpus_id}",
    ]
    for address in capture.orientation_addresses:
        full_entry = full.get(address)
        short_entry = short.get(address)
        evidence: list[str] = []
        if full_entry is not None and full_entry.lexical_rank is not None:
            evidence.append(f"full-prompt lexical rank {full_entry.lexical_rank}")
        if short_entry is not None and short_entry.lexical_rank is not None:
            evidence.append(f"short-need lexical rank {short_entry.lexical_rank}")
        structural: tuple[PythonDirectStructuralResourceEvidence, ...] = ()
        if isinstance(full_entry, LexicalStructuralResourceEntry):
            structural = full_entry.structural_supports
        elif isinstance(short_entry, LexicalStructuralResourceEntry):
            structural = short_entry.structural_supports
        evidence.extend(
            f"{support.direction} from {support.seed_resource} "
            f"(RI {support.fact.identity})"
            for support in structural
        )
        lines.append(f"{address}: {', '.join(evidence)}")
    return "\n".join(lines)


@dataclass(frozen=True, slots=True)
class CodexDogfoodAgentObservation:
    """Post-run observations; no field asserts that a resource was required."""

    searches: tuple[str, ...]
    opened_resources: tuple[RepositoryResourceAddress, ...]
    modified_resources: tuple[RepositoryResourceAddress, ...]
    validation_resources: tuple[RepositoryResourceAddress, ...]
    task_success: bool | None
    validation_success: bool | None
    observation_source: str
    bytes_read: int | None = None
    tokens_read: int | None = None

    def __post_init__(self) -> None:
        """Keep observation basis explicit and measurements nonnegative."""
        if not self.observation_source.strip():
            msg = "Agent observation requires a source or completeness note."
            raise ValueError(msg)
        if any(
            value is not None and value < 0
            for value in (self.bytes_read, self.tokens_read)
        ):
            msg = "Measured reads cannot be negative."
            raise ValueError(msg)
