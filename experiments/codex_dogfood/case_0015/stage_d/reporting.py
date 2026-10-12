"""Expose complete exact gold-relative calculations and frozen gate decisions."""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, ANN401, D103, COM812, E501, RUF001
from typing import Any

from experiments.bm25f.trace import serialize


def section(title: str, value: Any) -> str:
    return "## " + title + "\n\n```json\n" + serialize(value).decode() + "```\n\n"


def render(value: Any) -> bytes:
    parts = [
        "# Case 0015 R2 Stage D reviewed effectiveness\n\n",
        "## Did true BM25F improve acquisition in Case 0015?\n\n",
        "**Frozen outcome: " + value["gates"]["outcome"] + ".**\n\n",
        value["answer"] + "\n\n",
        "O2's repository-empty witness is COMPLETE at depth 0 in both arms, with zero prefix occurrences/resources/bytes. Zero-to-zero is not a meaningful gain, rescue or retrieval failure. TASK_BACKED units have no retrieval rank.\n\n",
        "No meaningful witness or REQUIRED-rank gain is established. O6 completion depth worsens 137 → 138. AGENTS.md's O6 rank worsens 2 → 3: 5×3=15 exceeds 6×2=12. Strong rank safety fails for any worsening; complementary bounds fail here. The frozen harmful gate therefore selects the case outcome after the contract and implementation gates pass.\n\n",
        value["scope"] + "\n\n",
        "SEARCH_POLICY_FAILURE = NOT_ASSESSED. Production behavior = UNCHANGED. Confirmation/reserve = NOT_ACCESSED.\n\n",
        section(
            "Did true BM25F improve? Every dimension and magnitude",
            value["did_true_bm25f_improve"],
        ),
        "## Exact task\n\n" + value["task_text"] + "\n",
        section("Six exact obligations", value["obligations"]),
        section(
            "Primary authentication, provenance and exact joins",
            {
                k: value[k]
                for k in (
                    "provenance",
                    "primary_policy",
                    "frame",
                    "joins",
                    "native_authentication",
                )
            },
        ),
        section("Reviewed gold summary", value["reviewed_summary"]),
        section(
            "All 42 semantic units, classes, alternatives and exact spans",
            value["semantic_units"],
        ),
        section("All 12 reviewed minimal witnesses", value["gold_witnesses"]),
        section(
            "Obligation and task indispensability",
            {
                k: value[k]
                for k in (
                    "obligation_indispensability",
                    "task_indispensable_resources",
                    "task_indispensable_units",
                )
            },
        ),
        "## All 21 REQUIRED-cell A/B ranks\n\n",
        "Ranks use the owning obligation query only. UNREACHED is preserved as missing rank, never assigned a numeric position.\n\n",
        "| Obligation | Resource | Witness membership | Obligation indispensable | Task indispensable | A | B | B−A | Meaningful gain | Complementary bound | Regression |\n",
        "|---|---|---|---|---|---:|---:|---:|---|---|---:|\n",
    ]
    for row in value["required_cells"]:
        c = row["change"]
        parts.append(
            f"| {row['obligation']} | {row['address']} | {', '.join(row['witness_membership'])} | {row['obligation_indispensable']} | {row['task_indispensable']} | {row['ranks']['A'] if row['ranks']['A'] is not None else 'UNREACHED'} | {row['ranks']['B'] if row['ranks']['B'] is not None else 'UNREACHED'} | {c['B_minus_A']} | {c['meaningful_improvement']} | {c['complementary_bound']} | {c['regression_magnitude']} |\n"
        )
    parts += [
        "\n",
        section(
            "All REQUIRED cells: field evidence, native contributions, union-IDF, inside-tf weight, single saturation and observed crossing consequences",
            value["required_cells"],
        ),
        "## All witness completion calculations\n\n",
        "| Obligation | Witness | A status/depth | B status/depth | A occurrences/unique | B occurrences/unique | A R/H/U | B R/H/U | A UTF-8 bytes | B UTF-8 bytes |\n",
        "|---|---|---|---|---|---|---|---|---:|---:|\n",
    ]
    for o, arms in value["witness_calculations"].items():
        for a, b in zip(arms["A"], arms["B"], strict=True):
            ac, bc = a["label_occurrences"], b["label_occurrences"]
            parts.append(
                f"| {o} | {a['witness']} | {a['completion_status']}/{a['depth']} | {b['completion_status']}/{b['depth']} | {a['prefix_occurrences']}/{a['unique_prefix_resources']} | {b['prefix_occurrences']}/{b['unique_prefix_resources']} | {ac['REQUIRED']}/{ac['HELPFUL_ONLY']}/{ac['UNNECESSARY']} | {bc['REQUIRED']}/{bc['HELPFUL_ONLY']}/{bc['UNNECESSARY']} | {a['distinct_utf8_bytes']} | {b['distinct_utf8_bytes']} |\n"
            )
    parts += [
        "\n",
        section(
            "Every witness member rank and exact prefix", value["witness_calculations"]
        ),
        section(
            "Selected witnesses and minimum complete depths, then stable identity",
            value["obligation_comparisons"],
        ),
        section(
            "Meaningful gains and REQUIRED regressions",
            {
                k: value[k]
                for k in (
                    "meaningful_witness_gains",
                    "meaningful_required_rank_gains",
                    "required_regressions",
                )
            },
        ),
        section(
            "Case-wide burden: selected mandatory prefix union and repeated occurrences",
            value["case_wide_burden"],
        ),
        section(
            "Full REQUIRED resource/cell/repository-unit/all-unit reach",
            value["required_reach"],
        ),
        section(
            "Mechanical causal attribution and interacting mechanisms",
            {k: value[k] for k in ("failure_attribution", "multi_cause_cells")},
        ),
        "Fixed-order score deltas explain observed necessary-resource/overtaker crossings. Intermediate stages are not treatment arms. Component effects can oppose or interact; signed margin effects do not prove a unique sufficient cause. No missing REQUIRED cell occurs, so QUERY_AUTHORING_LIMIT and FIELD_REPRESENTATION_LIMIT have no demonstrated cases here. CONTENT_FIELD_DOMINANCE is not inferred from raw content scores alone.\n\n",
        section(
            "Already captured top-K gold-labeled diagnostics, K=10/20/50",
            value["top_k_gold_diagnostics"],
        ),
        "Top-K crossings and pair inversions are explanation only; they never select outcome. Labels are relative to the owning obligation.\n\n",
        section(
            "Captured single-run cost, scopes retained without double counting",
            value["costs"],
        ),
        "Arm B's experimental scoring overhead is large. These single-run values are descriptive and no cost threshold selects the outcome. They do not imply an optimized production BM25F implementation would retain the overhead. Reference, publication/durability, mechanical checks, derived construction and capture wall are separate observations and are not added to charged arm totals.\n\n",
        section(
            "Frozen decision rule and precedence",
            {"rule": value["frozen_rule"], "precedence": value["precedence"]},
        ),
        section(
            "Every contract, implementation and reach gate",
            {
                k: value[k]
                for k in (
                    "contract_checks",
                    "implementation_checks",
                    "reach_gate",
                    "required_reach_losses",
                )
            },
        ),
        section(
            "Exact frozen gate inputs and burden arithmetic",
            {k: value[k] for k in ("gate_evidence", "gate_arithmetic")},
        ),
        section(
            "Frozen meaningful gain, safety, burden and bound decisions", value["gates"]
        ),
        section("Precedence application and outcome", value["precedence_application"]),
        section(
            "Gaps, exact limitations and preserved ambiguity",
            {k: value[k] for k in ("gaps", "limitations", "ambiguities")},
        ),
        section("Once-only attempt-2 journal, attempt-1 isolated", value["journal"]),
    ]
    return ("".join(parts).rstrip() + "\n").encode()


def artifacts(value: Any) -> dict[str, bytes]:
    report = render(value)
    trace = {
        "schema": "case-0015-stage-d-trace-v1",
        "provenance": value["provenance"],
        "joins": value["joins"],
        "native_authentication": value["native_authentication"],
        "journal": value["journal"],
        "gate_evidence": value["gate_evidence"],
        "gates": value["gates"],
        "claims": {
            "scientific_reruns": 0,
            "semantic_reviewers_added": 0,
            "semantic_transformation": "NONE",
            "confirmation_reserve": "NOT_ACCESSED",
            "production": "UNCHANGED",
            "SEARCH_POLICY_FAILURE": "NOT_ASSESSED",
        },
    }
    return {
        "analysis.json": serialize(value),
        "analysis.md": report,
        "STAGE_D_REVIEW.md": report,
        "trace.json": serialize(trace),
        "TRACE.md": (
            (
                "# Case 0015 Stage D trace\n\n"
                + section("Exact authentication and frozen decision", trace)
            ).rstrip()
            + "\n"
        ).encode(),
    }
