# Copyright (c) 2026
# ruff: noqa: E501 -- finite captured-evidence projections
"""Explain reviewed query yields, hints and paired score competition."""

from __future__ import annotations

from collections import Counter
from typing import Any

from experiments.codex_dogfood.case_0011.stage_d.metrics import explain, label


def diagnose(s: dict[str, Any], subset: dict[str, Any]) -> dict[str, Any]:
    """Use retained R1.5 profiles and exact contributions; never score queries."""
    profiles = {}
    for qid, q in s["queries"].items():
        capture = s["capture"]["queries"][qid]
        terms = []
        for p in capture["query_profile"]:
            counts = Counter(
                label(s, q["obligation"], address)
                for address in p["effective_matching_resources"]
            )
            terms.append(
                {
                    **p,
                    "reviewed_yield_counts": {
                        k: counts[k]
                        for k in ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")
                    },
                    "reviewed_yield_scope": q["obligation"] or "GLOBAL_STRONGEST_LABEL",
                    "matched_frame_fraction": len(p["effective_matching_resources"])
                    / 531,
                },
            )
        profiles[qid] = {
            "literal_query": q["text"],
            "terms": terms,
            "positive_label_counts": dict(
                Counter(
                    label(s, q["obligation"], r["address"]) for r in capture["rows"]
                ),
            ),
        }
    hints = []
    declarations = {
        "ModelRequest": "src/devtools/models/interaction/models.py",
        "ContextDisclosure": "src/devtools/context/planning/materialization.py",
        "DisclosurePlan": "src/devtools/context/planning/plan.py",
    }
    for symbol, address in declarations.items():
        source = s["contents"][address]
        declaration = next(
            line for line in source.splitlines() if line.startswith(f"class {symbol}:")
        )
        qs = [q for q in s["queries"].values() if symbol in q["text"]]
        hints.append(
            {
                "hint": symbol,
                "canonical_analyzed_term": symbol.casefold(),
                "declaration_resource": address,
                "expected_U2_route": {
                    "mechanism": "select_python_module_source_declarations",
                    "module": address.removeprefix("src/")
                    .removesuffix(".py")
                    .replace("/", "."),
                    "kind": "PythonSourceDeclarationKind.CLASS",
                    "declared_name": symbol,
                    "prerequisite": "Caller supplies the frozen snapshot and explicit qualified module interpretation; preserve multiple/absent outcomes in a bounded universe.",
                    "executed": False,
                },
                "declaration_line": declaration,
                "deterministic_target": "Single literal class declaration in the frozen named owner; exact routing is a future hypothesis, not executed.",
                "handling": "NOT_ROUTED_IN_U1",
                "queries": [
                    {
                        "query": q["identity"],
                        "text": q["text"],
                        "declaration": explain(
                            s,
                            q["identity"],
                            address,
                            q["obligation"],
                        ),
                        "assembly_owner": explain(
                            s,
                            q["identity"],
                            "src/devtools/context/planning/rendering.py",
                            q["obligation"],
                        ),
                    }
                    for q in qs
                ],
                "burden_evidence": "Owner/declaration ranks exceed one wherever higher scored resources intervene. Exact lookup could target a declaration deterministically; it would not supply the full task witness or fix omitted needs.",
                "class": "EXACT_HINT_NOT_ROUTED",
                "classification_scope": "Only containing-query rows with positive unnecessary_overtaker_count evidence avoidable lexical candidate burden; a rank-one target supplies no such evidence.",
            },
        )
    pairs = []
    for u in subset["units"]:
        for cr in u["responsible_routes"]:
            for br in u["B_routes"]:
                for ce, be in zip(cr["evidence"], br["evidence"], strict=True):
                    pairs.append(
                        {
                            "unit": u["unit"],
                            "alias": u["alias"],
                            "obligation": br["obligation"],
                            "resource": ce["resource"],
                            "B": be,
                            "C": ce,
                            "rank_delta": ce["rank"] - be["rank"],
                            "unnecessary_overtaker_delta": ce[
                                "unnecessary_overtaker_count"
                            ]
                            - be["unnecessary_overtaker_count"],
                            "matched_B_terms": [
                                t["term"] for t in be["score_evidence"]["content_terms"]
                            ],
                            "matched_C_terms": [
                                t["term"] for t in ce["score_evidence"]["content_terms"]
                            ],
                        },
                    )
    qid = "C.tests.request-preservation"
    target = explain(s, qid, "tests/context/planning/test_plan.py", "tests")
    top = s["capture"]["queries"][qid]["rows"][0]
    competing = [
        t
        for t in top["content_terms"]
        if t["term"] in {"request", "invalid", "argument"}
    ]
    mixed = {
        "status": "MIXED_INTENT_EVIDENCE_PRESENT",
        "query": qid,
        "distinct_concerns": [
            "copied-request field preservation (U05)",
            "invalid numeric argument/validation test conventions (U26)",
        ],
        "semantic_basis": "N14 directly covers both U05 and U26. Its literal query combines preservation and invalid argument validation. The reviewed U05 resource matches only 'tests'; the top Codex CLI document is UNNECESSARY for this obligation and scores predominantly on request/invalid/argument.",
        "target": target,
        "unnecessary_competitor": top,
        "competitor_label": label(s, "tests", top["address"]),
        "cross_concern_contributions": competing,
        "cross_concern_score": sum(t["contribution"] for t in competing),
        "score_margin": top["score"] - target["score_evidence"]["score"],
        "interpretation_limit": "Observed additive competition supports dilution as a contributor. No term ablation, causal intervention or improved query was executed; DF alone is not the evidence.",
        "class": "QUERY_DILUTION",
    }
    return {
        "query_profiles": profiles,
        "exact_hints": hints,
        "paired_required_evidence": pairs,
        "mixed_intent": [mixed],
        "representation_example": {
            "unit": "U27",
            "resource": "src/devtools/context/planning/rendering.py",
            "query": "C.bytes.rendered-boundary",
            "hidden_concept": "rendered",
            "observed_whole_identifier": "RenderedContextDisclosure",
            "query_analyzer_term": "rendered",
            "canonical_source_term": "renderedcontextdisclosure",
            "evidence": explain(
                s,
                "C.bytes.rendered-boundary",
                "src/devtools/context/planning/rendering.py",
                "bytes",
            ),
            "limit": "Canonical analysis leaves this occurrence whole. Identifier-aware retrieval was not executed, so potential rank improvement is unknown.",
        },
        "vocabulary_example": {
            "unit": "U06",
            "query": "C.tests.text-boundaries",
            "status": "POSSIBLE_VOCABULARY_SEMANTIC_MISMATCH",
            "semantic_basis": "Exact UTF-8 fixture bytes establish the need, while the query asks descriptive non-ASCII/newline/boundary vocabulary; the retained score evidence shows which words actually overlap.",
            "evidence": explain(
                s,
                "C.tests.text-boundaries",
                "tests/context/planning/test_plan.py",
                "tests",
            ),
        },
        "SEARCH_POLICY_FAILURE": "NOT_ASSESSED",
    }
