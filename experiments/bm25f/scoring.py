# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003 -- explicit mathematical provenance
"""One union IDF and one saturation after weighted normalized field aggregation."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, Any

from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from devtools.context.retrieval.lexical.scoring import (
    calculate_bm25_inverse_document_frequency,
)
from experiments.bm25f.fields import FieldState, validate_state

if TYPE_CHECKING:
    from devtools.context.repository.snapshot import RepositorySnapshotId
    from devtools.context.retrieval.lexical.bm25 import RepositoryTextLexicalQuery


@dataclass(frozen=True, slots=True)
class Parameters:
    """Freeze positive field weights and independently bounded field normalization."""

    k1: float = 1.2
    content_weight: float = 1.0
    filename_weight: float = 0.25
    b_content: float = 0.75
    b_filename: float = 0.75

    def __post_init__(self) -> None:
        """Require finite parameters and positive field weights."""
        if (
            not all(math.isfinite(v) for v in asdict(self).values())
            or self.k1 <= 0
            or self.content_weight <= 0
            or self.filename_weight <= 0
            or not 0 <= self.b_content <= 1
            or not 0 <= self.b_filename <= 1
        ):
            raise ValueError("Invalid positive BM25F parameters")


DEFAULT_PARAMETERS = Parameters()


def field_evidence(
    tf: int, length: int, average: float, b: float, weight: float
) -> dict[str, int | float]:
    """Record per-field normalization, including empty fields."""
    # If average=0 all field lengths/tfs must be zero; ratio=0 is a disclosed
    # zero-evidence convention, never a substitute for a nonempty denominator.
    if tf < 0 or length < tf or average < 0 or (average == 0 and (length or tf)):
        raise ValueError("Inconsistent field counts")
    denominator = 1 - b + b * length / average if average else 1.0
    normalized = tf / denominator if tf else 0.0
    return {
        "tf": tf,
        "length": length,
        "average_length": average,
        "b": b,
        "normalization_denominator": denominator,
        "normalized_tf": normalized,
        "weight": weight,
        "weighted_normalized_tf": weight * normalized,
    }


def score(
    state: FieldState,
    query: RepositoryTextLexicalQuery,
    *,
    snapshot_id: RepositorySnapshotId,
    parameters: Parameters = DEFAULT_PARAMETERS,
) -> dict[str, Any]:
    """Rank the native positive union with canonical query and collection-order ties."""
    validate_state(state)
    if snapshot_id != state.snapshot.id:
        raise ValueError("Stale/foreign requested snapshot")
    if query != analyze_repository_text_lexical_query(text=query.text):
        raise ValueError("Noncanonical query analysis")
    contents = state.content.corpus_statistics.document_statistics
    filenames = state.filename.document_statistics
    count = len(contents)
    content_counts = [
        {t.normalized_term: t.frequency for t in d.term_frequencies} for d in contents
    ]
    filename_counts = [
        {t.normalized_term: t.frequency for t in d.term_frequencies} for d in filenames
    ]
    union_df = {
        term: sum(
            term in c or term in f
            for c, f in zip(content_counts, filename_counts, strict=True)
        )
        for term in query.normalized_terms
    }
    matches: list[dict[str, Any]] = []
    for position, (document, content, filename, c, f) in enumerate(
        zip(
            state.collection.documents,
            contents,
            filenames,
            content_counts,
            filename_counts,
            strict=True,
        )
    ):
        if not any(t in c or t in f for t in query.normalized_terms):
            continue
        terms: list[dict[str, Any]] = []
        for term in query.normalized_terms:
            ce = field_evidence(
                c.get(term, 0),
                content.document_length,
                state.content.corpus_statistics.average_document_length,
                parameters.b_content,
                parameters.content_weight,
            )
            fe = field_evidence(
                f.get(term, 0),
                filename.document_length,
                state.filename.average_document_length,
                parameters.b_filename,
                parameters.filename_weight,
            )
            combined = float(ce["weighted_normalized_tf"]) + float(
                fe["weighted_normalized_tf"]
            )
            idf = calculate_bm25_inverse_document_frequency(
                document_count=count, document_frequency=union_df[term]
            )
            numerator = (parameters.k1 + 1) * combined
            denominator = parameters.k1 + combined
            terms.append(
                {
                    "term": term,
                    "query_multiplier": 1.0,
                    "CONTENT": ce,
                    "FILENAME": fe,
                    "content_observations": [
                        asdict(o)
                        for o in content.analysis.observations
                        if o.normalized_term == term
                    ],
                    "filename_observations": [
                        asdict(o)
                        for o in filename.analysis.observations
                        if o.normalized_term == term
                    ],
                    "combined_tf": combined,
                    "df_union": union_df[term],
                    "N": count,
                    "idf_union": idf,
                    "saturation_numerator": numerator,
                    "saturation_denominator": denominator,
                    "term_score": idf * numerator / denominator,
                }
            )
        matches.append(
            {
                "collection_position": position,
                "address": str(document.resource.address),
                "document_identity": str(document.id),
                "content_identity": str(document.resource.content_identity),
                "terms": terms,
                "score": sum(t["term_score"] for t in terms),
            }
        )
    matches.sort(key=lambda row: (-row["score"], row["collection_position"]))
    for rank, row in enumerate(matches, 1):
        row["rank"] = rank
    return {
        "schema": "two-field-true-bm25f-v1",
        "query": asdict(query),
        "repository_id": str(state.snapshot.repository_id),
        "snapshot_id": str(snapshot_id),
        "corpus_id": str(state.collection.corpus.id),
        "parameters": asdict(parameters),
        "field_statistics": {
            "N": count,
            "content_average_length": (
                state.content.corpus_statistics.average_document_length
            ),
            "filename_average_length": state.filename.average_document_length,
            "documents": [
                {
                    "document_identity": str(d.id),
                    "content_length": c.document_length,
                    "filename_length": f.document_length,
                }
                for d, c, f in zip(
                    state.collection.documents, contents, filenames, strict=True
                )
            ],
            "query_terms": [
                {
                    "term": term,
                    "content_df": sum(term in c for c in content_counts),
                    "filename_df": sum(term in f for f in filename_counts),
                    "df_union": union_df[term],
                    "union_document_identities": [
                        str(d.id)
                        for d, c, f in zip(
                            state.collection.documents,
                            content_counts,
                            filename_counts,
                            strict=True,
                        )
                        if term in c or term in f
                    ],
                }
                for term in query.normalized_terms
            ],
        },
        "matches": matches,
    }


def compare(
    state: FieldState,
    query: RepositoryTextLexicalQuery,
    *,
    snapshot_id: RepositorySnapshotId,
) -> dict[str, Any]:
    """Capture exact native Arm A and true BM25F Arm B without candidate repair."""
    treatment = score(state, query, snapshot_id=snapshot_id)
    native = retrieve_repository_text_documents_by_bm25(
        query=query,
        index=state.content,
        maximum_results=max(1, len(state.collection.documents)),
    )
    baseline = []
    for rank, m in enumerate(native.matches, 1):
        document = m.document_statistics.analysis.document
        baseline.append(
            {
                "rank": rank,
                "address": str(document.resource.address),
                "document_identity": str(document.id),
                "content_identity": str(document.resource.content_identity),
                "score": m.score,
                "content_score": m.content_score,
                "filename_score": m.filename_score,
                "filename_weight": m.filename_weight,
                "weighted_filename_score": m.weighted_filename_score,
                "content_terms": [asdict(t) for t in m.term_contributions],
                "filename_terms": [asdict(t) for t in m.filename_term_contributions],
            }
        )

    def keys(rows: list[dict[str, Any]]) -> set[tuple[str, str, str]]:
        identities = {
            (r["address"], r["document_identity"], r["content_identity"]) for r in rows
        }
        if len(identities) != len(rows):
            raise ValueError("EXPERIMENTAL_CONTRACT_DEFECT: duplicate candidate")
        return identities

    if keys(baseline) != keys(treatment["matches"]):
        raise ValueError("EXPERIMENTAL_CONTRACT_DEFECT: candidate mismatch")
    return {"A": baseline, "B": treatment, "candidate_identity": "PASS"}
