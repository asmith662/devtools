# Copyright (c) 2026
"""Freeze two lexical query arms and native direct structural evidence."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from devtools.context.retrieval.composition import (
    LexicalStructuralResourceInventory,
    compose_lexical_structural_resource_evidence,
)
from devtools.context.retrieval.lexical.bm25 import (
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
    from devtools.context.repository.resource import RepositoryResourceAddress
    from devtools.context.repository.snapshot import RepositorySnapshot
    from devtools.context.retrieval.lexical.index import (
        RepositoryTextLexicalInvertedIndex,
    )


@dataclass(frozen=True, slots=True)
class CodexDogfoodCase:
    """Inputs frozen before retrieval for one seeded, real development task.

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
        """Require a real task, distinct purpose, and qualified seed origins."""
        if not self.full_prompt.strip() or not self.short_information_need.strip():
            msg = "Dogfood task prompt and short InformationNeed must be nonempty."
            raise ValueError(msg)
        seeds = tuple(address for address, _ in self.seed_origins)
        if (
            not seeds
            or len(set(seeds)) != len(seeds)
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
    full_prompt_inventory: LexicalStructuralResourceInventory
    short_need_inventory: LexicalStructuralResourceInventory
    orientation_addresses: tuple[RepositoryResourceAddress, ...]


def capture_codex_dogfood_retrieval(
    case: CodexDogfoodCase,
) -> CodexDogfoodRetrievalCapture:
    """Run production retrieval twice under identical corpus and settings."""
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

    def inventory(query_text: str) -> LexicalStructuralResourceInventory:
        lexical = retrieve_repository_text_documents_by_bm25(
            query=analyze_repository_text_lexical_query(text=query_text),
            index=case.index,
            maximum_results=case.lexical_work_bound,
            settings=case.lexical_settings,
        )
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
        structural = (
            full_entry.structural_supports
            if full_entry is not None
            else short_entry.structural_supports
            if short_entry is not None
            else ()
        )
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
