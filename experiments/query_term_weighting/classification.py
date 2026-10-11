# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, COM812, C901, PLR0913 -- one auditable task/query classification contract
"""Task/query-only term policies retaining native analysis and exact provenance."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from devtools.context.localization.identity import (
        LocalizationObligationIdentity,
        LocalizationQueryIdentity,
        TaskProvenance,
    )
from devtools.context.retrieval.lexical.bm25 import (
    RepositoryTextLexicalQuery,
    RepositoryTextLexicalQueryObservation,
    analyze_repository_text_lexical_query,
)


class Role(StrEnum):
    """Distinguish literal anchors, sought facts and generic work verbs."""

    EXPLICIT_ANCHOR = "EXPLICIT_ANCHOR"
    SEMANTIC = "SEMANTIC"
    GENERIC_OPERATION = "GENERIC_OPERATION"


class Arm(StrEnum):
    """Freeze the baseline and two separately attributable interventions."""

    A = "CANONICAL_BM25"
    B = "ANCHOR_EMPHASIS"
    C = "FULL_QUERY_TERM_DISCRIMINATION"


GENERIC_LEXICON = ("add", "build", "create", "implement", "update")
LEXICON_RATIONALE = (
    "Five repository-independent work verbs; no domain nouns or test terminology."
)


def multiplier(role: Role, arm: Arm) -> float:
    """Apply the fixed, positive, binary-exact discrete hypothesis."""
    if arm is Arm.A:
        return 1.0
    if role is Role.EXPLICIT_ANCHOR:
        return 2.0
    if arm is Arm.C and role is Role.GENERIC_OPERATION:
        return 0.5
    return 1.0


@dataclass(frozen=True, slots=True)
class AnchorCopy:
    """Bind a whole query literal to an exact original task-text occurrence."""

    query_start: int
    query_end: int
    task_provenance: TaskProvenance


@dataclass(frozen=True, slots=True)
class WeightedQueryTerm:
    """Own frozen importance semantics absent from the native query observations."""

    analyzed_term: str
    observations: tuple[RepositoryTextLexicalQueryObservation, ...]
    role: Role
    classification_provenance: str
    multipliers: tuple[float, float, float]


@dataclass(frozen=True, slots=True)
class QueryPolicy:
    """Scope term roles to a native query, obligation and task-only evidence."""

    identity: LocalizationQueryIdentity
    obligation: LocalizationObligationIdentity
    native_query: RepositoryTextLexicalQuery
    task_text: str
    source: TaskProvenance
    anchors: tuple[AnchorCopy, ...]
    terms: tuple[WeightedQueryTerm, ...]

    def validate(self) -> None:
        """Reject foreign identities, analysis mutation and altered classification."""
        rebuilt = classify(
            identity=self.identity,
            obligation=self.obligation,
            query_text=self.native_query.text,
            task_text=self.task_text,
            source=self.source,
            anchors=self.anchors,
        )
        if self != rebuilt:
            raise ValueError("Query policy differs from task/query-only derivation")


def classify(
    *,
    identity: LocalizationQueryIdentity,
    obligation: LocalizationObligationIdentity,
    query_text: str,
    task_text: str,
    source: TaskProvenance,
    anchors: tuple[AnchorCopy, ...] = (),
) -> QueryPolicy:
    """Derive all distinct term roles without accepting any repository evidence."""
    if identity.task != obligation.task or source.source_identity != identity.task:
        raise ValueError("Foreign task/query/obligation provenance")
    if source.span is None or source.span.end > len(task_text):
        raise ValueError("Missing exact task clause provenance")
    query = analyze_repository_text_lexical_query(text=query_text)
    if not query.normalized_terms:
        raise ValueError("Empty analyzed query")
    occupied: set[int] = set()
    for anchor in anchors:
        span = anchor.task_provenance.span
        if (
            anchor.task_provenance.source_identity != identity.task
            or span is None
            or not source.span.start <= span.start < span.end <= source.span.end
            or not 0 <= anchor.query_start < anchor.query_end <= len(query_text)
            or task_text[span.start : span.end]
            != query_text[anchor.query_start : anchor.query_end]
        ):
            raise ValueError("Anchor lacks exact clause-local literal provenance")
        # Intentional literals are delimited in the task, not inferred from casing.
        if (
            task_text[span.start - 1 : span.start] != "`"
            or task_text[span.end : span.end + 1] != "`"
        ):
            raise ValueError("Anchor is not a task-marked literal")
        positions = set(range(anchor.query_start, anchor.query_end))
        if occupied & positions:
            raise ValueError("Ambiguous overlapping anchor classification")
        occupied |= positions
        for observation in query.observations:
            overlap = (
                observation.start < anchor.query_end
                and anchor.query_start < observation.end
            )
            if (
                overlap
                and not anchor.query_start
                <= observation.start
                < observation.end
                <= anchor.query_end
            ):
                raise ValueError("Anchor splits native analyzed term")
    terms = []
    for term in query.normalized_terms:
        observations = tuple(o for o in query.observations if o.normalized_term == term)
        literal = any(
            a.query_start <= o.start < o.end <= a.query_end
            for a in anchors
            for o in observations
        )
        role = (
            Role.EXPLICIT_ANCHOR
            if literal
            else Role.GENERIC_OPERATION
            if term in GENERIC_LEXICON
            else Role.SEMANTIC
        )
        reason = (
            "Exact task-marked literal copied into query; "
            "anchor precedence across repeated observations"
            if literal
            else "Frozen repository-independent five-verb lexicon"
            if role is Role.GENERIC_OPERATION
            else "Intentionally authored obligation fact term from the cited "
            "task clause; no corpus evidence"
        )
        terms.append(
            WeightedQueryTerm(
                term,
                observations,
                role,
                reason,
                (
                    multiplier(role, Arm.A),
                    multiplier(role, Arm.B),
                    multiplier(role, Arm.C),
                ),
            )
        )
    return QueryPolicy(
        identity, obligation, query, task_text, source, anchors, tuple(terms)
    )
