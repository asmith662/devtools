# Copyright (c) 2026
# ruff: noqa: ANN401, E501 -- exact human-readable scientific surfaces
"""Render every diagnostic without semantic evidence quote duplication."""

from __future__ import annotations

from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import json_bytes

INTERPRETATION = (
    "NON-GATING: The pattern is mixed/ambiguous enough that stronger purpose-relative conditions appear necessary before another bounded-consumption experiment. "
    "Case 0018 is STRUCTURAL_DISCRIMINATION_SIGNAL (one strong beneficial, zero strong harmful); Cases 0017 and 0019 have NO_MATERIAL_STRUCTURAL_DISCRIMINATION_SIGNAL. "
    "Among 121 pairs, 7 are beneficial, 110 neutral and 4 harmful. Direct support reaches 6/39 REQUIRED-in-A cells and 15/121 supported targets are useful; 106/121 are UNNECESSARY. "
    "The cohort supported-useful rate (12.3967%) exceeds baseline A's descriptive 9.2308%, but this is neither causal improvement nor consistent cross-case evidence: Case 0018 has only 8/96 useful supported targets against 72/904 baseline useful candidates. "
    "The single strong signal and absence of strong harm keep the bounded evidence question open; high neutrality/noise and low required coverage do not justify consuming this broad condition as a promotion policy. "
    "This interpretation creates no cohort gate, changes no case category, authorizes no production behavior and validates no reranker. The maintainer decides the next architecture."
)
LIMITATIONS = [
    "Three historical DEVELOPMENT cases; no statistical significance claim or formal cohort success gate.",
    "Structural candidate universe == A. No lexically absent REQUIRED evidence can be rescued here; no graph expansion or structural-only candidate utility is tested. Unsupported lexical misses are baseline non-reach, not structural failure.",
    "Actual rankings are unchanged. Local predecessor pairs are COUNTERFACTUAL DIAGNOSTICS ONLY; no rank gain/regression, witness-depth change or burden change is claimed.",
    "Supported-useful rates are descriptive discrimination evidence, not causal improvement. Gold labels of sources do not change frozen eligibility.",
    "Native resolved direct cross-resource References only; bounded/non-exhaustive resolution, no self-support, no independent Imports/Calls treatment, no multi-hop/PPR/RRF.",
    "One designated GPT-6 Astra / High primary per case; deterministic verification is not independent semantic validation. Host routing is not independently verified. No second reviewer or reconciliation.",
    "Case 0017 same-primary corrections R092/O2 and R268/O2 REQUIRED -> HELPFUL_ONLY and retired proposed unit are authoritative.",
    "Case 0018 TASK_INTERPRETATION_GAP = RESOLVED_WITH_EXPLICIT_QUALIFICATION; TASK_GAP = OPEN_DESIGN_FREEDOM_NOT_UNRESOLVED_CELL; REPOSITORY_INFORMATION_GAP = BOUNDED_LIMITATION_NO_BLOCKING_SUPPORT_GAP. Frozen O1-O3 remain evaluable.",
    "Case 0019 repository-integration judgments are CONDITIONAL on unresolved future provider-contract semantics: option spelling, value domain, version applicability and default behavior. TASK_INTERPRETATION_GAP remains PRESENT. Unconditional future task satisfaction has zero complete witnesses/combinations, empty sufficient unions, undefined ranges and indispensability. The conditional two-resource union does not close this gap. Pair classification remains valid within the frozen obligation interpretation.",
    "No production policy, structural score, threshold, rank movement or next experiment is authorized by this diagnostic. Historical child implementations/paths/diffs, confirmation and reserve remain unopened.",
]


def fenced(value: Any) -> str:
    """Render canonical JSON as an inspectable Markdown block."""
    return "```json\n" + json_bytes(value).decode() + "```\n"


def case_markdown(case: Any) -> str:
    """Render per-obligation baseline, coverage and evidence distributions."""
    lines = [
        f"# Case {case['case']} — Stage D direct structural discrimination",
        "",
        f"Frozen category: **{case['category']}**. No actual rank movement.",
        "",
        "| Obligation | A R/H/U | Supported R/H/U | Supported useful | Baseline useful | REQUIRED coverage | B/N/H | Strong B/H |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for q in case["queries"]:
        a, s, p = q["A_gold_labels"], q["supported_gold_labels"], q["pair_counts"]
        supported = q["supported_useful_rate"]
        baseline = q["baseline_A_useful_rate"]
        coverage = q["required_in_A_support_coverage"]
        lines.append(
            f"| {q['obligation']} | {a['REQUIRED']}/{a['HELPFUL_ONLY']}/{a['UNNECESSARY']} | {s['REQUIRED']}/{s['HELPFUL_ONLY']}/{s['UNNECESSARY']} | {supported['numerator']}/{supported['denominator']} | {baseline['numerator']}/{baseline['denominator']} | {coverage['numerator']}/{coverage['denominator']} | {p['BENEFICIAL']}/{p['NEUTRAL']}/{p['HARMFUL']} | {p['STRONG_BENEFICIAL']}/{p['STRONG_HARMFUL']} |",
        )
    lines += [
        "",
        "R/H/U = REQUIRED / HELPFUL_ONLY / UNNECESSARY. B/N/H = BENEFICIAL / NEUTRAL / HARMFUL. Rates are descriptive, not causal improvement.",
        "",
        "## Case totals",
        "",
        fenced(case["totals"]),
        "",
        f"Captured self References: {case['captured_self_reference_count']}; primary contribution = 0.",
        "",
        "## Exact join validation",
        "",
        fenced(case["join_validation"]),
    ]
    for q in case["queries"]:
        lines += [
            "",
            f"## {q['obligation']} coverage and diagnostics",
            "",
            q["indispensability_scope"],
            "",
            fenced(
                {
                    k: q[k]
                    for k in (
                        "required_cells",
                        "baseline_lexical_non_reach",
                        "indispensable_resources",
                        "evidence_characteristics",
                        "source_label_diagnostics",
                        "captured_timings_ns",
                    )
                },
            ),
        ]
    lines += [
        "",
        "## Structural characteristics by target label",
        "",
        fenced(case["evidence_characteristics"]),
        "",
        "## Source gold — secondary/descriptive",
        "",
        fenced(case["source_label_diagnostics"]),
        "",
        "## Limitations",
        "",
        *["- " + s for s in LIMITATIONS],
        "",
        "Every pair and exact supporting fact is inspectable in TRACE.md / trace.json. Gold evidence uses original primary cell pointers; no evidence quotes are reproduced.",
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


def trace_markdown(case: Any) -> str:
    """Expose every pair's ranks, labels, direction, sources and native IDs."""
    lines = [
        f"# Case {case['case']} Stage D complete local-pair trace",
        "",
        "COUNTERFACTUAL DIAGNOSTICS ONLY. Captured A rankings are unchanged. Each source remains eligible regardless of its gold label.",
        "",
        "Stage C cell pointers refer to ../adjudication/primary/stage_c_review.json. Full native support provenance is preserved from sealed Stage B.",
        "",
    ]
    for q in case["queries"]:
        for t in q["targets"]:
            target, predecessor = t["target"], t["predecessor"]
            strong = (
                "STRONG_BENEFICIAL"
                if t["strong_beneficial"]
                else "STRONG_HARMFUL"
                if t["strong_harmful"]
                else "NO"
            )
            lines += [
                f"## {t['case']} / {t['obligation']} / target rank {target['a_rank']}",
                "",
                f"Target `{target['address']}`: A rank {target['a_rank']}, gold **{t['target_gold_label']}**, primary {t['target_primary_cell_pointer']}.",
                "",
                f"Original predecessor `{predecessor['address']}`: A rank {predecessor['a_rank']}, gold **{t['predecessor_gold_label']}**, primary {t['predecessor_primary_cell_pointer']}.",
                "",
                f"Classification **{t['classification']}**; strong classification: **{strong}**. Distinct sources {t['distinct_supporting_source_count']}; qualifying occurrences {t['native_occurrence_count']}; best source rank {t['best_supporting_source_rank']}; rank distance {t['rank_distance']}; intervening UNNECESSARY {t['intervening_unnecessary']}.",
                "",
                "Exact supporting source addresses/ranks, source labels and native fact/derivation/declaration/subject/range provenance IDs:",
                "",
                fenced(t["sources"]),
                "",
            ]
    return "\n".join(lines).rstrip() + "\n"


def cohort_markdown(analysis: Any) -> str:
    """Present formal case categories plus descriptive cohort totals."""
    lines = [
        "# Direct structural discrimination — completed three-case Stage D",
        "",
        "STAGE C: THREE PRIMARY GOLD SETS IMPORTED. STAGE D: COMPLETE. This joins frozen lexical acquisition/support/predecessors to independent blind semantic gold under Stage A's previously frozen rules.",
        "",
        "## Formal case outputs and descriptive cohort counts",
        "",
        fenced(analysis["cohort"]),
        "",
        "## Non-gating interpretation",
        "",
        analysis["non_gating_interpretation"],
        "",
        "## Cases",
        "",
    ]
    lines.extend(
        f"- [Case {case['case']} analysis](../../../codex_dogfood/case_{case['case']}/stage_d/analysis.md); [complete pair trace](../../../codex_dogfood/case_{case['case']}/stage_d/TRACE.md)."
        for case in analysis["cases"]
    )
    lines += [
        "",
        "## Gold semantics and qualifications",
        "",
        fenced(analysis["gold_summaries"]),
        "",
        "## Performance — captured samples only",
        "",
        fenced(analysis["performance"]),
        "",
        "## Mechanical invariants",
        "",
        fenced(analysis["mechanical_invariants"]),
        "",
        "## Limitations",
        "",
        *["- " + s for s in LIMITATIONS],
        "",
        "## Durable state and exact next step",
        "",
        "Production behavior unchanged. GRAPH-3 = COMPLETE / GRAPH_HARMFUL. RETRIEVAL_PERFORMANCE_BASELINE = COMPLETE. Verifier = COMPLETE / SEALED_AND_DEEP_VERIFICATION_SEPARATED. Historical development population = FROZEN. SEARCH_POLICY_FAILURE = NOT_ASSESSED. Confirmation/reserve = NOT_ACCESSED. Historical child access = NO.",
        "",
        "Maintainer reviews the completed three-case structural-discrimination result. Do NOT open historical child implementations yet. Based on the frozen categories and descriptive evidence, decide whether a future prospective experiment should A) consume direct structural evidence in a bounded promotion/discrimination policy, B) require stronger purpose-relative structural conditions, or C) stop near-term direct-Reference discrimination work. Do not design or execute that next experiment here.",
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"
