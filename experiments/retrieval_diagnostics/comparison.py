# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, TRY003 -- bounded paired diagnostics
"""Same-frame treatment comparisons and exact lexical representation witnesses."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from experiments.retrieval_diagnostics.mechanics import Mechanics, term_deltas

if TYPE_CHECKING:
    from devtools.context.repository.resource import RepositoryResourceOccurrence


def compare(
    a: Mechanics, b: Mechanics, resource: RepositoryResourceOccurrence
) -> dict[str, Any]:
    """Compare two captured configurations without executing either ranker."""
    if (
        a.capture.frame != b.capture.frame
        or a.capture.lane != b.capture.lane
        or a.capture.query != b.capture.query
        or a.capture.resources != b.capture.resources
        or a.capture.obligation != b.capture.obligation
        or a.judgments != b.judgments
    ):
        raise ValueError("Paired diagnostic frame/query/judgment differs.")
    left, right = a.explain(resource), b.explain(resource)
    ar, br = left["rank"], right["rank"]
    valid_frame = resource in a.capture.resources
    deltas = term_deltas(left["terms"], right["terms"])
    hidden = _hidden(a, right["terms"], resource) if valid_frame else []
    lost = _hidden(b, left["terms"], resource) if valid_frame else []
    required = left["judgment"] is not None and left["judgment"]["label"] == "REQUIRED"
    representation = {
        "classification": "REPRESENTATION_FAILURE",
        "diagnostic": "VERIFIED_REPRESENTATION_FAILURE"
        if hidden or lost
        else "NO_HIDDEN_MATCH_DEMONSTRATED",
        "certainty": "DETERMINISTICALLY_ESTABLISHED"
        if hidden or lost
        else "INSUFFICIENT_EVIDENCE",
        "witnesses": hidden,
        "reverse_witnesses": lost,
        "required_resource": required,
        "positive_reach_rescue": bool(hidden)
        and left["status"] == "NO_QUERY_TERM_OVERLAP"
        and br is not None,
        "positive_reach_loss": bool(lost)
        and right["status"] == "NO_QUERY_TERM_OVERLAP"
        and ar is not None,
        "required_unit_specific_importance": "INSUFFICIENT_EVIDENCE: unit linkage does not prove the lexical cue itself is necessary.",
    }
    no_overlap = (
        valid_frame and left["status"] == right["status"] == "NO_QUERY_TERM_OVERLAP"
    )
    semantic = {
        "classification": "VOCABULARY_SEMANTIC_MISMATCH",
        "diagnostic": "POSSIBLE_VOCABULARY_SEMANTIC_MISMATCH"
        if required and no_overlap and not hidden
        else "NOT_ESTABLISHED",
        "certainty": "POSSIBLE_UNRESOLVED"
        if required and no_overlap and not hidden
        else "INSUFFICIENT_EVIDENCE",
        "limit": "No overlap in these two available representations; lexical evidence does not prove semantic equivalence.",
    }
    ahead_a, ahead_b = (
        set(left["ranking"]["ahead_resources"]),
        set(right["ranking"]["ahead_resources"]),
    )
    added = sorted(ahead_b - ahead_a)
    removed = sorted(ahead_a - ahead_b)
    labels = {p: j.label for p, j in b.judgments.items()}
    return {
        "subject_A": left["subject"],
        "subject_B": right["subject"],
        "transition": "POSITIVE_TO_POSITIVE"
        if ar is not None and br is not None
        else "POSITIVE_TO_MISS"
        if ar is not None
        else "MISS_TO_POSITIVE"
        if br is not None
        else "MISS_TO_MISS",
        "status_A": left["status"],
        "status_B": right["status"],
        "miss_reason_A": "REPRESENTATION_HIDDEN_TERM"
        if hidden and left["status"] == "NO_QUERY_TERM_OVERLAP"
        else left["status"],
        "miss_reason_B": "REPRESENTATION_HIDDEN_TERM"
        if lost and right["status"] == "NO_QUERY_TERM_OVERLAP"
        else right["status"],
        "rank_A": ar,
        "rank_B": br,
        "rank_delta": br - ar if ar is not None and br is not None else None,
        "score_A": left["score"],
        "score_B": right["score"],
        "configuration_changes": {
            key: {
                "A": getattr(a.capture.configuration, key),
                "B": getattr(b.capture.configuration, key),
            }
            for key in ("analyzer", "k1", "b", "filename_weight", "index_identity")
            if getattr(a.capture.configuration, key)
            != getattr(b.capture.configuration, key)
        },
        "changed_query_terms": {
            "added": sorted(set(b.capture.query_terms) - set(a.capture.query_terms)),
            "removed": sorted(set(a.capture.query_terms) - set(b.capture.query_terms)),
        },
        "mechanics": deltas,
        "new_overtakers": added,
        "removed_overtakers": removed,
        "positive_candidate_changes": {
            "A_only": sorted(a.rows.keys() - b.rows.keys()),
            "B_only": sorted(b.rows.keys() - a.rows.keys()),
            "complete_universes": a.capture.complete_positive_universe
            and b.capture.complete_positive_universe,
        },
        "new_overtaker_labels": {
            label: sum(labels.get(p) == label for p in added)
            for label in ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY", "UNRESOLVED")
        },
        "representation": representation,
        "semantic_mismatch": semantic,
        "limits": "No positive-rank recovery inferred from partial lexical mismatch. Completion remains caller-owned accepted-alternative evaluation.",
    }


def _hidden(
    hidden: Mechanics,
    exposed_terms: list[dict[str, Any]],
    resource: RepositoryResourceOccurrence,
) -> list[dict[str, Any]]:
    """Verify a source/query component is omitted by the compared analyzer."""
    witnesses = []
    p = hidden.positions[resource.address.value]
    for t in exposed_terms:
        field_hidden = (
            not hidden.postings.get(t["field"], {}).get(t["term"], {}).get(p, 0)
        )
        query_hidden = t["term"] not in hidden.capture.query_terms
        source_hidden = field_hidden and any(
            t["term"] != observed.casefold()
            for observed in t["source"]["whole_form_counts"]
        )
        query_derived = query_hidden and any(
            t["term"] != observed.casefold()
            for observed in t["query_source"]["whole_form_counts"]
        )
        if source_hidden or query_derived:
            witnesses.append(
                {
                    "field": t["field"],
                    "term": t["term"],
                    "source_hidden": source_hidden,
                    "query_hidden": query_derived,
                    "source": t["source"],
                    "query_source": t["query_source"],
                    "hidden_treatment": hidden.capture.configuration.treatment,
                    "hidden_exposes_query_term": not query_hidden,
                    "hidden_matches_field_term": not field_hidden,
                    "exposed_weighted_contribution": t["weighted_contribution"],
                }
            )
    return witnesses
