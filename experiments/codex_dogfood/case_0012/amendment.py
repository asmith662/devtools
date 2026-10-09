# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, TRY003 -- literal prospective protocol; formatter owns commas
"""Pre-execution attribution clarification, separate from frozen treatment inputs."""

from __future__ import annotations

import json
from typing import Any

from experiments.exact_hint_routing.behavior import CONTRACT

ORIGINAL = "bd82f6481d0f993c1757fe1689b8b772b1948db9"
RESEAL_PARENT = "afe9fc75e7d4da0cc92df50331d92233e4ff8243"
FAMILIES = {
    "RESOURCE_ADDRESS": ("H07", "H08", "H09", "H10"),
    "PYTHON_DIRECT_DECLARATION": ("H01", "H02"),
    "PYTHON_MODULE": ("H03",),
    "PYTHON_DIRECT_METHOD": ("H04",),
    "UNSUPPORTED_BARE_CLASS": ("H05", "H06"),
}
FIELDS = (
    "hint_count",
    "associated_obligations",
    "admitted_route_count",
    "RESOLVED_count",
    "AMBIGUOUS_count",
    "UNRESOLVED_count",
    "UNSUPPORTED_count",
    "unique_resolved_resources",
    "REQUIRED_exact_targets",
    "HELPFUL_ONLY_exact_targets",
    "UNNECESSARY_exact_targets",
    "native_lexical_rank_distribution",
    "routed_positions",
    "rank_depth_saved",
    "prefix_burden_changes",
    "complete_obligation_effect",
    "cost",
)
EQUIVALENCE = {
    "expectation": "Pre-execution equality covers route-request identities, locator families/inputs, associated obligations, selected mechanisms and repository/snapshot/frame bindings. Post-resolution and post-presentation equality uses exact-hint-behavior-projection-v1, not literal equality of complete native accounts/views. TASK_EXTRACTION_PROVENANCE intentionally differs; REPOSITORY_RESOLUTION_PROVENANCE must be behaviorally equivalent.",
    "forbidden_differences": [
        "resolution disposition",
        "native target",
        "promoted resource",
        "routed order",
        "fallback candidate membership",
        "fallback order",
        "native rank",
        "native score",
        "native repository evidence",
        "native score contributions",
    ],
    "cost": "Independent execution costs may differ only through measurement noise; extraction/reference projection is the same ordered task-text input surface. Timing differences confer no semantic/result difference.",
    "failure": "Any field difference in the frozen behavioral equality projection selects EXPERIMENTAL_CONTRACT_DEFECT under the existing first-precedence contract gate unless frozen semantic route inputs are first proven different. Extraction-rule, caller/mechanical authorship, syntactic-form and treatment-explanation differences alone are expected, retained and never a contract defect. Do not normalize native objects or alter arms to force equality.",
    "provenance_layers": {
        "TASK_EXTRACTION_PROVENANCE": "U2-owned inventory/arm identity, extraction rule, syntactic form, author/review/extraction explanation and task-observation provenance. Retain exact B/C differences in full scientific artifacts; the semantic task identity/text/span is still compared.",
        "REPOSITORY_RESOLUTION_PROVENANCE": "Native referents, candidates, evidence, locator inputs including native class-parent provenance, repository/snapshot/frame bindings and reasons from deterministic mechanisms. Compare all native fields except the explicitly identified task-extraction request.provenance pass-through, never strip provenance recursively.",
    },
    "projection": CONTRACT,
    "scope": "Case 0012 does not provide a differential effectiveness test of mechanical extraction versus caller-reviewed extraction. It provides one-case task-text extraction agreement plus prospective exact-first route-value evidence. Caller review is not universal truth.",
}
SCOPE = {
    "path_only": "If meaningful value is established only by RESOURCE_ADDRESS hints, say: exact repository-path routing supported in Case 0012. Do not claim empirical support for module routing, direct declaration routing or direct method routing.",
    "code_symbols": "Name only the exact code-symbol reporting families that establish value; do not extrapolate to other families or repositories.",
    "no_required_target": "A family with no resolved REQUIRED target has effectiveness NOT_ASSESSED. Explicitly report any HELPFUL_ONLY-only, UNNECESSARY-only or mixed non-required targets; absence of a required target is not a measured negative effectiveness result.",
    "primary_rule": "The original primary gates, thresholds and outcome vocabulary remain unchanged. EXACT_HINT_ROUTING_SUPPORTED may be the global outcome while the architecture conclusion is qualified by observed route family.",
}


def conclusion_scope(
    required_targets: dict[str, int], value_families: frozenset[str]
) -> dict[str, str]:
    """Apply future family qualification to supplied counts, never acquire evidence."""
    if set(required_targets) != set(FAMILIES) or not value_families <= FAMILIES.keys():
        raise ValueError("Route-family partition differs")
    if any(n < 0 for n in required_targets.values()) or any(
        required_targets[f] == 0 for f in value_families
    ):
        raise ValueError("Value requires a resolved REQUIRED target")
    status = {
        f: "NOT_ASSESSED"
        if n == 0
        else "VALUE_ESTABLISHED"
        if f in value_families
        else "ASSESSED_NO_ESTABLISHED_VALUE"
        for f, n in required_targets.items()
    }
    status["conclusion"] = (
        "exact repository-path routing supported in Case 0012"
        if value_families == frozenset({"RESOURCE_ADDRESS"})
        else "Case 0012 value established for: " + ", ".join(sorted(value_families))
        if value_families
        else "No route-family value established"
    )
    return status


def definition(treatment: dict[str, Any]) -> dict[str, Any]:
    """Freeze clarification and review decisions without changing any treatment value."""
    requests = treatment["exact_route_requests"]
    if [r["identity"] for r in requests["B"]] != [r["identity"] for r in requests["C"]]:
        raise ValueError("B/C route-request identities differ")
    for b, c in zip(requests["B"], requests["C"], strict=True):
        if any(b[k] != c[k] for k in ("locator", "association", "mechanism")):
            raise ValueError("B/C semantic route inputs differ")
    hints = treatment["caller_reviewed_hint_reference"]
    members = [h for family in FAMILIES.values() for h in family]
    if len(members) != len(set(members)) or set(members) != {
        f"H{n:02}" for n in range(1, len(hints) + 1)
    }:
        raise ValueError("Route-family partition incomplete or duplicated")
    families = {}
    for family, identifiers in FAMILIES.items():
        rows = [requests["B"][int(h[1:]) - 1] for h in identifiers]
        families[family] = {
            "hints": list(identifiers),
            "hint_texts": [r["hint"]["text"] for r in rows],
            "hint_count": len(rows),
            "associated_obligations": sorted(
                {r["association"]["lane"]["value"] for r in rows}
            ),
            "admitted_route_count": sum(r["locator"] is not None for r in rows),
            "required_future_fields": list(FIELDS),
        }
    return {
        "schema": "case-0012-stage-a-clarification-v2",
        "history": {
            "original_stage_a_checkpoint": ORIGINAL,
            "original_subject": "Freeze prospective exact-hint routing case",
            "prior_equivalence_checkpoint": RESEAL_PARENT,
            "authoritative_stage_a": "This amended, resealed pre-execution checkpoint supersedes the original protocol clarification; original inputs and history remain preserved at the original commit.",
            "scope": "Protocol clarification and attribution only; no task, treatment inputs, frame, universes, BM25 settings, primary thresholds or outcome vocabulary change.",
        },
        "bc_equivalence": EQUIVALENCE,
        "route_families": families,
        "family_reporting": "Report every field per family and per arm in Stage B/Stage D; native/measurement fields are absent before execution, gold-dependent labels/burden/completion/value fields unavailable until independent blind adjudication. Counts are hints/routes separately; deduplicate native resources within family, preserve cross-family overlap and associated lane ownership. Unsupported bare classes are not failed extraction merely because routing is unsupported. No fabricated costs or zero-valued outcome placeholders.",
        "conclusion_scope": SCOPE,
        "baseline_scope": "Arm A is obligation-level canonical BM25, not the whole-task query. U2 tests exact-first routing on top of the obligation-query baseline established after U1. The unchanged full-task/global lexical lane is a safety/reference lane, not the primary U2 baseline arm. Frozen arm names remain unchanged.",
        "maintainer_review": {
            "H03": "devtools.context.planning remains associated only with choices: the hint occurs in the choices/integration task clause; cross-obligation semantic mechanism routing belongs to U3.",
            "H05": "ContextDisclosure remains UNSUPPORTED_EXACT_HINT: unqualified class, no task-only sound module owner; repository-familiarity inference and broad global class search are not admitted.",
            "H06": "ModelRequest remains UNSUPPORTED_EXACT_HINT: unqualified class, no task-only sound module owner; repository-familiarity inference and broad global class search are not admitted.",
            "paths": "Exact file-path hints remain admitted. Their likely ease does not invalidate U2; path value and code-symbol route value must be reported separately.",
        },
        "execution": {"exact_routes": 0, "lexical_queries": 0, "treatments": 0},
        "stage_b": "NOT_EXECUTED",
        "effectiveness": "UNKNOWN",
    }


def review(clarification: dict[str, Any]) -> str:
    """Render all frozen clarification fields for both human review surfaces."""
    return (
        "\n".join(
            ["## Pre-execution protocol amendment", ""]
            + [
                line
                for key, value in clarification.items()
                for line in (
                    "### " + key,
                    "",
                    value
                    if isinstance(value, str)
                    else "```json\n" + json.dumps(value, indent=2) + "\n```",
                    "",
                )
            ]
        ).rstrip("\n")
        + "\n"
    )
