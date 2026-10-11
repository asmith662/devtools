# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, COM812, C901, PLR0912, PLR0915, PLR2004 -- single auditable native/weighted reconstruction contract
"""Explicit query-side multipliers over immutable native BM25 contributions."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

from devtools.context.retrieval.lexical.bm25 import RepositoryTextLexicalBm25Settings
from devtools.context.retrieval.lexical.scoring import (
    calculate_bm25_inverse_document_frequency,
    calculate_bm25_term_contribution,
)
from experiments.query_term_weighting.classification import (
    Arm,
    QueryPolicy,
    Role,
    multiplier,
)

if TYPE_CHECKING:
    from devtools.context.retrieval.lexical.bm25 import (
        RepositoryTextLexicalBm25Match,
        RepositoryTextLexicalBm25RetrievalResult,
    )


@dataclass(frozen=True, slots=True)
class Contribution:
    """Expose each channel's native term value and explicit weighting arithmetic."""

    term: str
    role: Role
    channel: str
    native: float
    multiplier: float
    weighted: float
    channel_weight: float


@dataclass(frozen=True, slots=True)
class WeightedMatch:
    """Keep native match provenance intact beside weighted score evidence."""

    native_match: RepositoryTextLexicalBm25Match
    collection_position: int
    score: float
    contributions: tuple[Contribution, ...]


@dataclass(frozen=True, slots=True)
class WeightedResult:
    """Retain the full native universe and policy for deterministic reconstruction."""

    native_result: RepositoryTextLexicalBm25RetrievalResult
    policy: QueryPolicy
    arm: Arm
    matches: tuple[WeightedMatch, ...]

    def validate(self) -> None:
        """Reject modified scores, provenance, candidates or ordering."""
        if self != score(self.native_result, self.policy, self.arm):
            raise ValueError("Weighted trace fails reconstruction")


def score(
    native: RepositoryTextLexicalBm25RetrievalResult, policy: QueryPolicy, arm: Arm
) -> WeightedResult:
    """Score every native positive candidate; never execute retrieval here."""
    policy.validate()
    if not isinstance(arm, Arm):
        raise TypeError("Unknown frozen treatment arm")
    if native.query != policy.native_query:
        raise ValueError("Foreign query supplied to weighting")
    if (
        native.settings != RepositoryTextLexicalBm25Settings()
        or native.filename_index is None
    ):
        raise ValueError("Canonical combined BM25 required")
    statistics = native.index.corpus_statistics.document_statistics
    if native.maximum_results < len(statistics):
        raise ValueError("Truncated native candidate bound")
    positions = {id(d): i for i, d in enumerate(statistics)}
    document_positions = {id(d.analysis.document): i for i, d in enumerate(statistics)}
    if (
        native.filename_index.document_collection
        is not native.index.corpus_statistics.collection_analysis.document_collection
    ):
        raise ValueError("Foreign filename frame")
    expected_candidates = {
        positions[id(p.document_statistics)]
        for t in native.index.term_postings
        if t.normalized_term in native.query.normalized_terms
        for p in t.postings
    } | {
        document_positions[id(p.document_statistics.analysis.document)]
        for t in native.filename_index.term_postings
        if t.normalized_term in native.query.normalized_terms
        for p in t.postings
    }
    roles = {t.analyzed_term: t.role for t in policy.terms}
    filename_statistics = {
        id(d.analysis.document): d for d in native.filename_index.document_statistics
    }
    matches = []
    seen: set[int] = set()
    for match in native.matches:
        position = positions.get(id(match.document_statistics))
        if position is None or position in seen:
            raise ValueError("Foreign or duplicate native candidate")
        seen.add(position)
        if (
            match.filename_weight != 0.25
            or match.content_score
            != sum(t.contribution for t in match.term_contributions)
            or match.filename_score
            != sum(t.contribution for t in match.filename_term_contributions)
            or match.weighted_filename_score != 0.25 * match.filename_score
            or match.score != match.content_score + match.weighted_filename_score
        ):
            raise ValueError("Native score provenance differs")
        values = []
        channel_scores = []
        for channel, evidence, channel_weight in (
            ("content", match.term_contributions, 1.0),
            ("filename", match.filename_term_contributions, 0.25),
        ):
            local_statistics = (
                match.document_statistics
                if channel == "content"
                else filename_statistics[
                    id(match.document_statistics.analysis.document)
                ]
            )
            local_frequencies = {
                t.normalized_term: t.frequency
                for t in local_statistics.term_frequencies
            }
            corpus_frequencies = (
                native.index.corpus_statistics.document_frequencies
                if channel == "content"
                else native.filename_index.document_frequencies
            )
            frequencies = {
                t.normalized_term: t.document_frequency for t in corpus_frequencies
            }
            average = (
                native.index.corpus_statistics.average_document_length
                if channel == "content"
                else native.filename_index.average_document_length
            )
            channel_terms = tuple(t.normalized_term for t in evidence)
            if channel_terms != tuple(
                t for t in native.query.normalized_terms if t in local_frequencies
            ):
                raise ValueError("Native contribution term identity/order differs")
            for term in evidence:
                idf = calculate_bm25_inverse_document_frequency(
                    document_count=len(statistics),
                    document_frequency=frequencies[term.normalized_term],
                )
                expected = calculate_bm25_term_contribution(
                    term_frequency=local_frequencies[term.normalized_term],
                    inverse_document_frequency=idf,
                    document_length=local_statistics.document_length,
                    average_document_length=average,
                    settings=native.settings,
                )
                if (
                    term.term_frequency != local_frequencies[term.normalized_term]
                    or term.document_frequency != frequencies[term.normalized_term]
                    or term.inverse_document_frequency != idf
                    or term.document_length != local_statistics.document_length
                    or term.average_document_length != average
                    or term.contribution != expected
                ):
                    raise ValueError("Native term contribution/statistics tamper")
                role = roles[term.normalized_term]
                weight = multiplier(role, arm)
                weighted = term.contribution * weight
                if not math.isfinite(weighted) or weighted <= 0:
                    raise ValueError("Invalid or underflowed positive contribution")
                values.append(
                    Contribution(
                        term.normalized_term,
                        role,
                        channel,
                        term.contribution,
                        weight,
                        weighted,
                        channel_weight,
                    )
                )
            # Preserve native summation order and channel grouping, including Arm A.
            channel_scores.append(
                sum(
                    t.contribution * multiplier(roles[t.normalized_term], arm)
                    for t in evidence
                )
            )
        total = channel_scores[0] + 0.25 * channel_scores[1]
        if not math.isfinite(total) or total <= 0:
            raise ValueError("Invalid weighted positive score")
        matches.append(WeightedMatch(match, position, total, tuple(values)))
    if seen != expected_candidates:
        raise ValueError(
            "EXPERIMENTAL_CONTRACT_DEFECT: missing/added native positive candidate"
        )
    matches.sort(key=lambda m: (-m.score, m.collection_position))
    result = WeightedResult(native, policy, arm, tuple(matches))
    if arm is Arm.A and tuple(m.native_match for m in result.matches) != native.matches:
        raise ValueError("Arm A differs from canonical score/tie ordering")
    return result


def require_identical_candidates(results: tuple[WeightedResult, ...]) -> None:
    """Compare full frame/index/query identity as well as exact candidate identities."""
    if not results:
        raise ValueError("No arms supplied")
    first = results[0]
    for result in results:
        result.validate()
        if (
            result.native_result is not first.native_result
            or result.policy != first.policy
        ):
            raise ValueError("Foreign query/frame/statistics across arms")
        if {m.collection_position for m in result.matches} != {
            m.collection_position for m in first.matches
        }:
            raise ValueError("EXPERIMENTAL_CONTRACT_DEFECT: candidate difference")
