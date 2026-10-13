# Copyright (c) 2026
# ruff: noqa: ANN401, E501 -- inspectable post-hoc diagnostic reports
"""POST_HOC / ORACLE / NON_GATING / NOT_RUNTIME_AVAILABLE human-readable surfaces."""

from __future__ import annotations

from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import json_bytes
from experiments.structural_discrimination.post_hoc.source_quality.analysis import (
    GROUPS,
    STATUS,
)
from experiments.structural_discrimination.stage_c.import_gold import LABELS

INTERPRETATION = (
    "SOURCE_QUALITY_LOOKS_EXPLANATORY (POST_HOC / ORACLE / NON_GATING / NOT_RUNTIME_AVAILABLE). "
    "All 15 useful supported targets have at least one useful same-obligation source: 15/21 targets in the useful-source groups are useful, versus 0/100 with only unnecessary sources. "
    "At the primary distinct source-target/obligation pair level, useful sources point to useful targets in 21/29 pairs, versus 4/189 for unnecessary sources. "
    "All seven beneficial local pairs, including the sole strong beneficial, lie in useful-source groups. The strong event has one REQUIRED source at lexical rank 2. "
    "Most broad-support noise is associated with only unnecessary sources (100/106 unnecessary targets), but useful sources still support six unnecessary targets and two harmful local pairs. "
    "This consistent descriptive separation makes source credibility worth investigating prospectively. It establishes association, not causation or a deployable gold filter, and does not amend the completed Stage D result."
)
LIMITATIONS = [
    "POST_HOC / ORACLE / NON_GATING / NOT_RUNTIME_AVAILABLE: all new source-quality grouping uses frozen semantic gold unavailable to a runtime policy.",
    "Three DEVELOPMENT cases; sparse useful-source groups, correlated resources/obligations and repeated References. No significance test, numeric acceptance threshold or prospective effectiveness claim.",
    "Pair-weighted cross-tabs are primary. Occurrence weighting is secondary and can amplify repeated References to the same declaration; it does not redefine the diagnostic.",
    "Useful-source support is not sufficient: six unnecessary targets and two harmful local comparisons remain in useful-source groups. No causal responsibility is assigned to a supporting source.",
    "The candidate universe remains A. The 33 REQUIRED-in-A cells with no direct support are retained separately, not source-qualification failures. No source filter can manufacture support for them within this experiment.",
    "All original predecessor identities/ranks, labels and outcomes are retained. No reranking, pair removal, promotion rule, rank cutoff, distance cutoff, top-K or frequency threshold is introduced.",
    "Case 0018 retains its interpretation/design/repository qualifications. Case 0019 repository-integration gold and indispensability remain conditional on unresolved provider option spelling/domain/version/default; unconditional task satisfaction is not established.",
    "One designated primary per case; host routing was not independently verified. No reviewer, semantic reconciliation, historical child, confirmation or reserve access occurred here.",
]
NEXT = (
    "Maintainer reviews this separate oracle diagnostic. The recommended next prospective question is whether source evidence can become credible for an unresolved obligation WITHOUT gold, so Localization-established source evidence can guide selective pursuit of a direct structural relation and subsequent target evaluation. "
    "This is a direction to investigate, not a runtime rule or prospective treatment design. No next experiment is designed or executed here. Keep historical child implementations/paths/diffs and confirmation/reserve sealed."
)


def fenced(value: Any) -> str:
    """Expose canonical data without replacing the authoritative machine surface."""
    return "```json\n" + json_bytes(value).decode() + "```\n"


def matrix(value: Any) -> str:
    """Render counts plus row and column percentages with explicit denominators."""
    lines = [
        "| Source gold | Target REQUIRED | Target HELPFUL_ONLY | Target UNNECESSARY | Row total |",
        "|---|---:|---:|---:|---:|",
    ]
    for source in LABELS:
        entries = []
        for target in LABELS:
            row, column = (
                value["row_percentages"][source][target],
                value["column_percentages"][source][target],
            )
            percentages = f"row {row:.2f}%" if row is not None else "row undefined"
            percentages += (
                f"; col {column:.2f}%" if column is not None else "; col undefined"
            )
            entries.append(f"{value['counts'][source][target]} ({percentages})")
        lines.append(
            f"| {source} | "
            + " | ".join(entries)
            + f" | {value['row_totals'][source]} |",
        )
    lines += [
        "| Column total | "
        + " | ".join(str(value["column_totals"][t]) for t in LABELS)
        + f" | {value['total']} |",
        "",
        "Useful-source collapse and exact useful-target rates:",
        "",
        fenced(
            {
                k: value[k]
                for k in (
                    "useful_source_collapse",
                    "collapsed_useful_target_rate",
                    "collapsed_row_percentages",
                    "collapsed_column_percentages",
                )
            },
        ),
    ]
    return "\n".join(lines)


def grouping(value: Any) -> str:
    """Show the precedence target partition and unchanged local comparisons."""
    lines = [
        "| Source-quality group | Targets | Target R/H/U | Useful rate | Original B/N/H | Strong B/H |",
        "|---|---:|---|---|---|---|",
    ]
    for group in GROUPS:
        row = value[group]
        labels, outcomes, rate = (
            row["target_labels"],
            row["original_pair_outcomes"],
            row["useful_target_rate"],
        )
        proportion = (
            f"{rate['proportion'] * 100:.2f}%"
            if rate["proportion"] is not None
            else "undefined"
        )
        lines.append(
            f"| {group} | {row['targets']} | {labels['REQUIRED']}/{labels['HELPFUL_ONLY']}/{labels['UNNECESSARY']} | {rate['numerator']}/{rate['denominator']} ({proportion}) | {outcomes['BENEFICIAL']}/{outcomes['NEUTRAL']}/{outcomes['HARMFUL']} | {row['STRONG_BENEFICIAL']}/{row['STRONG_HARMFUL']} |",
        )
    return "\n".join(lines)


def render(result: Any) -> str:
    """Retain every declared case/obligation surface and the separate interpretation."""
    lines = [
        "# Structural support source quality diagnostic",
        "",
        " / ".join(STATUS),
        "",
        INTERPRETATION,
        "",
        "## Cohort primary pair-weighted cross-tab",
        "",
        matrix(result["cohort"]["pair_weighted"]),
        "",
        "## Cohort secondary occurrence-weighted cross-tab",
        "",
        matrix(result["cohort"]["occurrence_weighted"]),
        "",
        "## Most important diagnostic: target source-quality partition",
        "",
        grouping(result["cohort"]["target_source_quality"]),
    ]
    for case, data in result["cases"].items():
        for name, scope in [("case aggregate", data), *data["obligations"].items()]:
            lines += [
                "",
                f"## {case} / {name} — POST_HOC ORACLE",
                "",
                "Primary pair-weighted:",
                "",
                matrix(scope["pair_weighted"]),
                "",
                "Secondary occurrence-weighted:",
                "",
                matrix(scope["occurrence_weighted"]),
                "",
                grouping(scope["target_source_quality"]),
                "",
                "Ranks and captured relation density:",
                "",
                fenced(scope["rank_and_density"]),
            ]
    lines += [
        "",
        "## Cohort source ranks and relation density",
        "",
        fenced(result["cohort"]["rank_and_density"]),
        "",
        "## Published strong-beneficial event and every supporting source",
        "",
        fenced(result["strong_beneficial_trace"]),
        "",
        "## Supported REQUIRED and useful targets",
        "",
        fenced(
            {
                k: result[k]
                for k in (
                    "supported_REQUIRED_targets",
                    "supported_useful_partition",
                    "supported_unnecessary_partition",
                )
            },
        ),
        "",
        "## 33 unsupported REQUIRED-in-A cells — separate accounting",
        "",
        fenced(result["unsupported_REQUIRED_in_A"]),
        "",
        "## Original scientific result preserved",
        "",
        fenced(
            {
                k: result[k]
                for k in (
                    "unchanged_published_categories",
                    "unchanged_published_cohort_totals",
                    "published_interpretation_sha256",
                    "invariants",
                )
            },
        ),
        "",
        "## Limitations",
        "",
        *["- " + s for s in LIMITATIONS],
        "",
        "## Recommended next question — no treatment design",
        "",
        NEXT,
        "",
        "Exact identities, all native provenance and every original local outcome are inspectable in TRACE.md and trace.json. Input and implementation hashes are in analysis.json / integrity.json.",
    ]
    return "\n".join(lines).rstrip() + "\n"


def trace(value: Any, strong: Any) -> str:
    """Expose all 218 pair identities/provenance and the 121 target partitions."""
    lines = [
        "# Source-quality complete diagnostic trace",
        "",
        " / ".join(STATUS),
        "",
        "Original lexical ranks, sources, native Reference facts and predecessor outcomes are unchanged. Gold grouping is oracle-only; source labels do not alter eligibility.",
        "",
        "## Target-level precedence partition",
        "",
        fenced(value["target_source_quality_partition"]),
        "",
        "## Strong-beneficial target and all sources",
        "",
        fenced(strong),
    ]
    for pair in value["distinct_source_target_obligation_pairs"]:
        lines += [
            "",
            f"## {pair['case']} / {pair['obligation']}: {pair['source']['address']} -> {pair['target']['address']}",
            "",
            fenced(pair),
        ]
    return "\n".join(lines).rstrip() + "\n"
