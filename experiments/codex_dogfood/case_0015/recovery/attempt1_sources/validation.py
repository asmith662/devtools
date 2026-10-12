# Copyright (c) 2026
# ruff: noqa: PLR0917, PLR0913, COM812, E501, EM101, TRY003 -- complete arithmetic boundary
"""Independent arithmetic checks from durable observations; never invoke treatments."""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import asdict
from fractions import Fraction
from pathlib import PurePosixPath
from typing import TYPE_CHECKING, Any

from devtools.context.retrieval.lexical.analysis import iter_lexical_spans

if TYPE_CHECKING:
    from devtools.context.retrieval.lexical.bm25 import (
        RepositoryTextLexicalBm25RetrievalResult,
    )
from experiments.bm25f.fields import FieldState, validate_state
from experiments.bm25f.trace import attribution, serialize


def equal(actual: object, expected: object, message: str) -> None:
    """Compare exact hex numerical evidence and ordering, never float tolerances."""
    if serialize(actual) != serialize(expected):
        raise ValueError(message)


def observations(text: str) -> list[dict[str, Any]]:
    """Replay only canonical spans, without constructing an index or scoring query."""
    return [
        {
            "encounter_ordinal": i,
            "observed_text": o,
            "normalized_term": t,
            "start": a,
            "end": b,
        }
        for i, (o, t, a, b) in enumerate(iter_lexical_spans(text=text))
    ]


def field_surface(state: FieldState) -> dict[str, Any]:
    """Project complete retained fields, lengths, frequencies and collection positions."""
    content = state.content.corpus_statistics
    rows = []
    for i, (d, c, f) in enumerate(
        zip(
            state.collection.documents,
            content.document_statistics,
            state.filename.document_statistics,
            strict=True,
        )
    ):
        rows.append(
            {
                "collection_position": i,
                "repository_id": str(d.repository_id),
                "snapshot_id": str(state.snapshot.id),
                "corpus_id": str(state.collection.corpus.id),
                "address": str(d.resource.address),
                "document_identity": str(d.id),
                "content_identity": str(d.resource.content_identity),
                "CONTENT": {
                    "length": c.document_length,
                    "observations": [asdict(o) for o in c.analysis.observations],
                    "term_frequencies": {
                        t.normalized_term: t.frequency for t in c.term_frequencies
                    },
                },
                "FILENAME": {
                    "stem": f.analysis.filename_stem,
                    "length": f.document_length,
                    "observations": [asdict(o) for o in f.analysis.observations],
                    "term_frequencies": {
                        t.normalized_term: t.frequency for t in f.term_frequencies
                    },
                },
            }
        )
    return {
        "N": content.document_count,
        "content_average_length": content.average_document_length,
        "filename_average_length": state.filename.average_document_length,
        "documents": rows,
    }


def validate_fields(state: FieldState, union: dict[str, Any]) -> dict[str, Any]:
    """Validate every canonical field observation and membership against retained text."""
    validate_state(state)
    surface = field_surface(state)
    memberships: dict[str, dict[str, list[str]]] = {}
    for d, row in zip(state.collection.documents, surface["documents"], strict=True):
        for name, text in (
            ("CONTENT", d.text),
            ("FILENAME", PurePosixPath(str(d.resource.address)).stem),
        ):
            expected = observations(text)
            equal(
                row[name]["observations"],
                expected,
                "BM25F_FIELD_DEFINITION_DEFECT: observations",
            )
            equal(
                row[name]["length"],
                len(expected),
                "BM25F_FIELD_DEFINITION_DEFECT: length",
            )
            counts = dict(Counter(o["normalized_term"] for o in expected))
            equal(row[name]["term_frequencies"], counts, "BM25F_DF_DEFECT: tf")
            if name == "FILENAME":
                equal(row[name]["stem"], text, "BM25F_FIELD_DEFINITION_DEFECT: stem")
            for term in counts:
                memberships.setdefault(term, {"CONTENT": [], "FILENAME": []})[
                    name
                ].append(row["document_identity"])
    n = len(surface["documents"])
    equal(surface["N"], n, "BM25F_DF_DEFECT: N")
    for name, key in (
        ("CONTENT", "content_average_length"),
        ("FILENAME", "filename_average_length"),
    ):
        equal(
            surface[key],
            sum(r[name]["length"] for r in surface["documents"]) / n if n else 0.0,
            "BM25F_NORMALIZATION_DEFECT: average",
        )
    positions = {
        r["document_identity"]: r["collection_position"] for r in surface["documents"]
    }
    expected_union = {
        "N": n,
        "terms": {
            term: {
                **fields,
                "union": sorted(
                    set(fields["CONTENT"]) | set(fields["FILENAME"]),
                    key=positions.__getitem__,
                ),
                "df_union": len(set(fields["CONTENT"]) | set(fields["FILENAME"])),
            }
            for term, fields in sorted(memberships.items())
        },
    }
    equal(union, expected_union, "BM25F_DF_DEFECT: union membership/document once")
    for name, actual in (
        ("CONTENT", state.content.corpus_statistics.document_frequencies),
        ("FILENAME", state.filename.document_frequencies),
    ):
        equal(
            {t.normalized_term: t.document_frequency for t in actual},
            {t: len(fields[name]) for t, fields in memberships.items() if fields[name]},
            "Native field DF mismatch",
        )
    return surface


def native_surface(native: RepositoryTextLexicalBm25RetrievalResult) -> dict[str, Any]:
    """Project authoritative native scores/contributions without a reconstruction arm."""
    return {
        "query": asdict(native.query),
        "settings": asdict(native.settings),
        "maximum_results": native.maximum_results,
        "matches": [
            {
                "rank": i,
                "address": str(
                    m.document_statistics.analysis.document.resource.address
                ),
                "document_identity": str(m.document_statistics.analysis.document.id),
                "content_identity": str(
                    m.document_statistics.analysis.document.resource.content_identity
                ),
                "score": m.score,
                "content_score": m.content_score,
                "filename_score": m.filename_score,
                "filename_weight": m.filename_weight,
                "weighted_filename_score": m.weighted_filename_score,
                "content_terms": [asdict(t) for t in m.term_contributions],
                "filename_terms": [asdict(t) for t in m.filename_term_contributions],
            }
            for i, m in enumerate(native.matches, 1)
        ],
    }


def idf(n: int, df: int) -> float:
    """Reconstruct exact frozen Robertson arithmetic, not another retrieval call."""
    return math.log(1 + (n - df + 0.5) / (df + 0.5))


def validate_native(
    native: RepositoryTextLexicalBm25RetrievalResult,
    state: FieldState,
    surface: dict[str, Any],
    union: dict[str, Any],
    query: dict[str, Any],
) -> dict[str, Any]:
    """Check authoritative Arm A score, contribution, field view and canonical ties."""
    equal(asdict(native.query), query["analysis"], "Native query/analysis changed")
    if native.index is not state.content or native.filename_index is None:
        raise ValueError("Native index provenance differs")
    equal(asdict(native.settings), {"k1": 1.2, "b": 0.75}, "Native settings changed")
    if native.maximum_results != len(state.collection.documents):
        raise ValueError("Native candidate bound differs")
    if native.filename_index != state.filename:
        raise ValueError("Native intrinsic filename representation/statistics changed")
    actual = native_surface(native)
    expected_rows: list[dict[str, Any]] = []
    for row in surface["documents"]:
        channels: dict[str, list[dict[str, Any]]] = {"CONTENT": [], "FILENAME": []}
        for field, average_key in (
            ("CONTENT", "content_average_length"),
            ("FILENAME", "filename_average_length"),
        ):
            for term in query["normalized_terms"]:
                tf = row[field]["term_frequencies"].get(term, 0)
                if not tf:
                    continue
                df = len(union["terms"][term][field])
                inverse = idf(surface["N"], df)
                average = surface[average_key]
                numerator = tf * (1.2 + 1)
                denominator = tf + 1.2 * (
                    1 - 0.75 + 0.75 * row[field]["length"] / average
                )
                channels[field].append(
                    {
                        "normalized_term": term,
                        "term_frequency": tf,
                        "document_frequency": df,
                        "inverse_document_frequency": inverse,
                        "document_length": row[field]["length"],
                        "average_document_length": average,
                        "contribution": inverse * numerator / denominator,
                    }
                )
        cs = (
            sum(t["contribution"] for t in channels["CONTENT"])
            if channels["CONTENT"]
            else 0.0
        )
        fs = sum(t["contribution"] for t in channels["FILENAME"])
        final = cs + 0.25 * fs
        if final <= 0:
            continue
        expected_rows.append(
            {
                "collection_position": row["collection_position"],
                "address": row["address"],
                "document_identity": row["document_identity"],
                "content_identity": row["content_identity"],
                "score": final,
                "content_score": cs,
                "filename_score": fs,
                "filename_weight": 0.25,
                "weighted_filename_score": 0.25 * fs,
                "content_terms": channels["CONTENT"],
                "filename_terms": channels["FILENAME"],
            }
        )
    expected_rows.sort(key=lambda r: (-r["score"], r["collection_position"]))
    for rank, row in enumerate(expected_rows, 1):
        row.pop("collection_position")
        row["rank"] = rank
    equal(
        actual["matches"],
        expected_rows,
        "Native Arm A authenticity/arithmetic/tie mismatch",
    )
    return actual


def validate_b(
    treatment: dict[str, Any],
    state: FieldState,
    surface: dict[str, Any],
    union: dict[str, Any],
    query: dict[str, Any],
) -> None:
    """Reconstruct frozen B from captured counts only; no B scorer invocation."""
    equal(treatment["query"], query["analysis"], "BM25F query changed")
    equal(
        treatment["parameters"],
        {
            "k1": 1.2,
            "content_weight": 1.0,
            "filename_weight": 0.25,
            "b_content": 0.75,
            "b_filename": 0.75,
        },
        "BM25F frozen parameters changed",
    )
    for key, value in (
        ("repository_id", str(state.snapshot.repository_id)),
        ("snapshot_id", str(state.snapshot.id)),
        ("corpus_id", str(state.collection.corpus.id)),
    ):
        equal(treatment[key], value, "BM25F frame mismatch")
    n = surface["N"]
    terms = query["normalized_terms"]
    expected: list[dict[str, Any]] = []
    for row in surface["documents"]:
        if not any(
            t in row["CONTENT"]["term_frequencies"]
            or t in row["FILENAME"]["term_frequencies"]
            for t in terms
        ):
            continue
        contributions = []
        for term in terms:
            fields = {}
            for field, average_key, weight in (
                ("CONTENT", "content_average_length", 1.0),
                ("FILENAME", "filename_average_length", 0.25),
            ):
                tf = row[field]["term_frequencies"].get(term, 0)
                average = surface[average_key]
                denominator = (
                    1 - 0.75 + 0.75 * row[field]["length"] / average if average else 1.0
                )
                normalized = tf / denominator if tf else 0.0
                fields[field] = {
                    "tf": tf,
                    "length": row[field]["length"],
                    "average_length": average,
                    "b": 0.75,
                    "normalization_denominator": denominator,
                    "normalized_tf": normalized,
                    "weight": weight,
                    "weighted_normalized_tf": weight * normalized,
                }
            combined = (
                fields["CONTENT"]["weighted_normalized_tf"]
                + fields["FILENAME"]["weighted_normalized_tf"]
            )
            df = union["terms"].get(term, {"df_union": 0})["df_union"]
            inverse = idf(n, df)
            numerator = (1.2 + 1) * combined
            denominator = 1.2 + combined
            contributions.append(
                {
                    "term": term,
                    "query_multiplier": 1.0,
                    **fields,
                    "content_observations": [
                        o
                        for o in row["CONTENT"]["observations"]
                        if o["normalized_term"] == term
                    ],
                    "filename_observations": [
                        o
                        for o in row["FILENAME"]["observations"]
                        if o["normalized_term"] == term
                    ],
                    "combined_tf": combined,
                    "df_union": df,
                    "N": n,
                    "idf_union": inverse,
                    "saturation_numerator": numerator,
                    "saturation_denominator": denominator,
                    "term_score": inverse * numerator / denominator,
                }
            )
        expected.append(
            {
                k: row[k]
                for k in (
                    "collection_position",
                    "address",
                    "document_identity",
                    "content_identity",
                )
            }
            | {
                "terms": contributions,
                "score": sum(t["term_score"] for t in contributions),
            }
        )
    expected.sort(key=lambda row: (-row["score"], row["collection_position"]))
    for rank, row in enumerate(expected, 1):
        row["rank"] = rank
    equal(
        treatment["matches"],
        expected,
        "BM25F_APPLICATION_DEFECT: exact field/aggregation/one-IDF/one-saturation/score/tie reconstruction",
    )
    expected_statistics = {
        "N": n,
        "content_average_length": surface["content_average_length"],
        "filename_average_length": surface["filename_average_length"],
        "documents": [
            {
                "document_identity": r["document_identity"],
                "content_length": r["CONTENT"]["length"],
                "filename_length": r["FILENAME"]["length"],
            }
            for r in surface["documents"]
        ],
        "query_terms": [
            {
                "term": t,
                "content_df": len(union["terms"].get(t, {"CONTENT": []})["CONTENT"]),
                "filename_df": len(union["terms"].get(t, {"FILENAME": []})["FILENAME"]),
                "df_union": union["terms"].get(t, {"df_union": 0})["df_union"],
                "union_document_identities": union["terms"].get(t, {"union": []})[
                    "union"
                ],
            }
            for t in terms
        ],
    }
    equal(
        treatment["field_statistics"],
        expected_statistics,
        "BM25F_DF_DEFECT: query statistics",
    )


def validate_pair(
    state: FieldState,
    native: RepositoryTextLexicalBm25RetrievalResult,
    treatment: dict[str, Any],
    surface: dict[str, Any],
    union: dict[str, Any],
    query: dict[str, Any],
) -> dict[str, Any]:
    """Verify candidate identity, exact native A and frozen B before publication."""
    a = native_surface(native)

    def identities(rows: list[dict[str, Any]]) -> set[tuple[str, str, str]]:
        keys = {
            (r["address"], r["document_identity"], r["content_identity"]) for r in rows
        }
        if len(keys) != len(rows):
            raise ValueError("EXPERIMENTAL_CONTRACT_DEFECT: duplicate candidate")
        return keys

    if identities(a["matches"]) != identities(treatment["matches"]):
        raise ValueError("EXPERIMENTAL_CONTRACT_DEFECT: candidate mismatch")
    validate_native(native, state, surface, union, query)
    validate_b(treatment, state, surface, union, query)
    return {"A": a["matches"], "B": treatment, "candidate_identity": "PASS"}


def diagnostic(comparison: dict[str, Any]) -> list[dict[str, Any]]:
    """Retain frozen attribution and exact rational subtraction residuals."""
    rows = attribution(comparison)
    for row in rows:
        for t in row["terms"]:
            parts = sum(
                (
                    Fraction(t[k])
                    for k in (
                        "union_idf_delta",
                        "pre_saturation_weight_delta",
                        "cross_field_single_saturation_delta",
                    )
                ),
                Fraction(0),
            )
            residual = Fraction(t["term_score_delta"]) - parts
            t["exact_subtraction_residual"] = {
                "numerator": residual.numerator,
                "denominator": residual.denominator,
            }
    return rows
