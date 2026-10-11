# Copyright (c) 2026
# ruff: noqa: E501, COM812, EM101, TRY003, ANN401 -- bounded heterogeneous trace schema
"""Lossless float serialization and deterministic attribution/reconstruction traces."""

from __future__ import annotations

import hashlib
import json
from typing import TYPE_CHECKING, Any

from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
)

if TYPE_CHECKING:
    from experiments.bm25f.fields import FieldState
from experiments.bm25f.scoring import Parameters, score


def lossless(value: Any) -> Any:
    """Encode every floating value as float.hex; preserve integer and text evidence."""
    if isinstance(value, float):
        return {"float_hex": value.hex()}
    if isinstance(value, dict):
        return {k: lossless(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [lossless(v) for v in value]
    return value


def serialize(value: object) -> bytes:
    """Encode stable UTF-8 LF JSON independently of host line endings."""
    return (
        json.dumps(lossless(value), sort_keys=True, ensure_ascii=True, indent=2) + "\n"
    ).encode()


def envelope(value: object) -> bytes:
    """Seal exact lossless payload; integrity is separate from semantic replay."""
    payload = serialize(value)
    return serialize(
        {"sha256": hashlib.sha256(payload).hexdigest(), "payload": json.loads(payload)}
    )


def validate_envelope(raw: bytes) -> object:
    """Reject noncanonical serialization and payload mutation."""
    value = json.loads(raw)
    if (
        serialize(value) != raw
        or hashlib.sha256(serialize(value["payload"])).hexdigest() != value["sha256"]
    ):
        raise ValueError("Trace serialization/hash tamper")
    return value["payload"]


def verify_score(result: dict[str, Any], state: FieldState) -> None:
    """Replay score from retained observations; never build another index or query native A."""
    expected = score(
        state,
        analyze_repository_text_lexical_query(text=result["query"]["text"]),
        snapshot_id=state.snapshot.id,
        parameters=Parameters(**result["parameters"]),
    )
    if serialize(result) != serialize(expected):
        raise ValueError("BM25F contribution/score tamper")


def attribution(comparison: dict[str, Any]) -> list[dict[str, Any]]:
    """Explain movement with a fixed telescoping diagnostic, never choose another arm."""
    a_by_id = {r["document_identity"]: r for r in comparison["A"]}
    parameters = comparison["B"]["parameters"]
    k1 = float(parameters["k1"])

    def saturation(tf: float) -> float:
        return (k1 + 1) * tf / (k1 + tf)

    rows = []
    for b in comparison["B"]["matches"]:
        a = a_by_id[b["document_identity"]]
        content = {t["normalized_term"]: t for t in a["content_terms"]}
        filename = {t["normalized_term"]: t for t in a["filename_terms"]}
        terms = []
        for t in b["terms"]:
            term = t["term"]
            native = content.get(term, {}).get("contribution", 0.0) + a[
                "filename_weight"
            ] * filename.get(term, {}).get("contribution", 0.0)
            nc = t["CONTENT"]["normalized_tf"]
            nf = t["FILENAME"]["normalized_tf"]
            union = t["idf_union"] * (
                saturation(nc) + parameters["filename_weight"] * saturation(nf)
            )
            weighted = t["idf_union"] * (
                saturation(parameters["content_weight"] * nc)
                + saturation(parameters["filename_weight"] * nf)
            )
            terms.append(
                {
                    "term": term,
                    "native_additive_term": native,
                    "CONTENT_native": content.get(term),
                    "FILENAME_native": filename.get(term),
                    "union_idf_delta": union - native,
                    "pre_saturation_weight_delta": weighted - union,
                    "cross_field_single_saturation_delta": t["term_score"] - weighted,
                    "term_score_delta": t["term_score"] - native,
                    "field_normalization": {f: t[f] for f in ("CONTENT", "FILENAME")},
                }
            )
        rows.append(
            {
                "address": b["address"],
                "document_identity": b["document_identity"],
                "A_rank": a["rank"],
                "B_rank": b["rank"],
                "score_delta": b["score"] - a["score"],
                "native_channel_grouping_residual": a["score"]
                - sum(t["native_additive_term"] for t in terms),
                "terms": terms,
            }
        )
    return rows


def render(comparison: dict[str, Any]) -> str:
    """Expose exact evidence and signed fixed-order diagnostics for human review."""
    return (
        "# Two-field BM25F controlled/execution trace\n\n"
        "Union-IDF replacement, then moving field weights inside saturation, then single cross-field saturation form a fixed telescoping diagnostic. These are explanatory counterfactual calculations, not extra ranked treatment arms. Native normalization inputs are unchanged; field-length interactions remain in every term record. Floating grouping residuals are explicit.\n\n"
        "```json\n"
        + serialize(
            {"comparison": comparison, "attribution": attribution(comparison)}
        ).decode()
        + "```\n"
    )
