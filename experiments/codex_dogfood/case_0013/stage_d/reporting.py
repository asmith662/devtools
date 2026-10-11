"""Render deterministic effectiveness reports from the computed development case."""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, ANN401, D103, E501, COM812
from typing import Any

from experiments.codex_dogfood.case_0013.adjudication.reviewed.materialize import (
    encoded,
)


def json_section(lines: list[str], title: str, value: Any) -> None:
    lines.extend(
        ["## " + title, "", "```json", encoded(value).decode().rstrip(), "```", ""]
    )


def report(a: Any) -> bytes:
    outcome = a["gates"]["outcome"]
    lines = [
        "# Case 0013 Stage D effectiveness evaluation",
        "",
        "**DID TASK-ROLE-CONDITIONED SELECTIVE EXACT-ROUTE ADMISSION IMPROVE OVER ALWAYS-ON EXACT-FIRST IN CASE 0013?**",
        "",
        "**Frozen U3 outcome: " + outcome + "**",
        "",
        "Read the frozen gates and dimensions below. C retains every meaningful B-over-A witness gain and all required reach while avoiding actual native nonresolution; semantic completeness and inspection burden are evaluated separately from route cost.",
        "",
        "No new semantic review, reliability comparison, reconciliation or treatment operation. PRIMARY_ASTRA_HIGH / semantic_transformation = NONE.",
        "",
        "## Did selective routing improve?",
        "",
        "| Dimension | Classification | B | C | C minus B |",
        "| --- | --- | --- | --- | --- |",
    ]
    for key, value in a["did_selective_routing_improve"].items():
        if isinstance(value.get("B"), dict):
            b, c = "per-obligation table below", "per-obligation table below"
        else:
            b, c = (
                str(value.get("B", "NOT_ASSESSED")),
                str(value.get("C", "NOT_ASSESSED")),
            )
        lines.append(
            f"| {key} | {value['classification']} | {b} | {c} | {value.get('C_minus_B', 'see exact detail')} |"
        )
    lines += [
        "",
        "Single-run captured timings are descriptive development evidence. A smaller request set avoids four genuine native nonresolutions; it preserves the selected compatibility witness gain. C has higher presentation cost in this capture. Neither completeness nor equal completion burden alone supplies selective value.",
        "",
        "## Exact task",
        "",
        "```text",
        a["task_text"].rstrip(),
        "```",
        "",
    ]
    json_section(
        lines,
        "Authority, primary policy and exact frame joins",
        {
            k: a[k]
            for k in (
                "provenance",
                "primary_policy",
                "frame",
                "joins",
                "native_authentication",
            )
        },
    )
    json_section(lines, "Reviewed gold summary", a["reviewed_summary"])
    lines += [
        "## Complete H01-H10 table",
        "",
        "| Hint | Role | Family | Obligation | B admission/disposition | C admission/disposition | Target | Gold | Native → routed | Depth saved | Witnesses | Indispensable | Attribution |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for h in a["hints"]:
        position = (
            "NO TARGET"
            if h["resolved_resource"] is None
            else f"{h['native_rank']} → {h['routed_position']} (exact {h['exact_tier_position']})"
        )
        lines.append(
            f"| {h['hint']} | {h['frozen_role']} | {h['family']} | {h['obligation']} | {h['B_admission']} / {h['B_native_disposition']} | {h['C_admission']} / {h['C_native_disposition']} | {h['resolved_resource'] or 'NONE'} | {h['reviewed_label'] or 'NO RESOURCE LABEL'} | {position} | {h['depth_saved']} | {len(h['obligation_witness_membership'])} | {h['obligation_indispensable']} | {h['failure_or_nonvalue_attribution']} |"
        )
    lines += [
        "",
        "B-only future destinations remain actual B UNRESOLVED with no candidates and C NOT_INVOKED / LEXICAL_ONLY. They have no existing target and no resource gold label. Avoidance is genuine native nonresolution, not universal uselessness.",
        "",
    ]
    json_section(
        lines,
        "Every hint: exact classifications, reviewed units, positions, witness effects and native accounts",
        a["hints"],
    )
    json_section(lines, "Skipped-route account", a["skipped_routes"])
    json_section(lines, "Separate family effects and captured costs", a["families"])
    lines += [
        "## Selected mandatory witnesses and completion depths",
        "",
        "| Obligation | A witness | A depth | B witness | B depth | C witness | C depth |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for key, row in a["obligation_safety_checks"].items():
        lines.append(
            f"| {key} | {row['A_selected_witness']} | {row['A_depth']} | {row['B_selected_witness']} | {row['B_depth']} | {row['C_selected_witness']} | {row['C_depth']} |"
        )
    lines += [
        "",
        "Selection uses minimum complete depth then the unchanged primary witness identity. Depth 0 means task-backed evidence needs no repository prefix. No alternatives are mixed; no global retrieval ranking is invented.",
        "",
        "## All 48 witnesses in each arm",
        "",
        "| Obligation | Witness | Arm | Depth | Occurrences | Unique | REQUIRED | HELPFUL_ONLY | UNNECESSARY | UTF-8 bytes | Bottleneck |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for arm, result in a["arms"].items():
        for key, lane in result["lanes"].items():
            for witness in lane["all_witnesses"]:
                metrics = witness["metrics"]
                if metrics is None:
                    fields = "NOT_ASSESSED | NOT_ASSESSED | NOT_ASSESSED | NOT_ASSESSED | NOT_ASSESSED | NOT_ASSESSED"
                else:
                    comp = metrics["label_occurrences"]
                    fields = f"{metrics['prefix_occurrences']} | {metrics['unique_prefix_count']} | {comp['REQUIRED']} | {comp['HELPFUL_ONLY']} | {comp['UNNECESSARY']} | {metrics['unique_utf8_bytes']}"
                lines.append(
                    f"| {key} | {witness['identity']} | {arm} | {witness['completion_depth']} | {fields} | {', '.join(witness['bottlenecks'])} |"
                )
    lines += [""]
    json_section(
        lines,
        "All meaningful B-over-A gains and bottleneck changes",
        a["meaningful_B_gains"],
    )
    json_section(
        lines, "Full witness member ranks, every prefix and exact burden", a["arms"]
    )
    json_section(
        lines, "Required reach losses relative to A and B", a["required_reach_losses"]
    )
    json_section(
        lines,
        "Native positive candidate/fallback/global safety preservation",
        a["preservation"],
    )
    json_section(lines, "Single-run cost accounting", a["costs"])
    json_section(
        lines, "Separate publication and durability cost", a["publication_durability"]
    )
    json_section(lines, "Every frozen contract gate", a["contract_checks"])
    json_section(lines, "Every frozen soundness gate", a["soundness_checks"])
    json_section(
        lines, "Every frozen obligation-safety gate", a["obligation_safety_checks"]
    )
    json_section(lines, "Frozen authoritative decision rule", a["frozen_rule"])
    json_section(
        lines, "Exact evidence supplied to unchanged gates.py", a["gate_evidence"]
    )
    json_section(lines, "Every integer cross-product", a["gate_arithmetic"])
    json_section(
        lines,
        "Gate results and exact precedence",
        {"gates": a["gates"], "precedence": a["precedence_application"]},
    )
    json_section(lines, "Failure and non-value attribution", a["failure_attribution"])
    json_section(lines, "Exactly-once journal authentication", a["journal"])
    lines += [
        "SEARCH_POLICY_FAILURE = NOT_ASSESSED.",
        "",
        "## Bounded conclusion and next step",
        "",
        a["scope"],
        "",
        "No production routing or manifest feature was implemented. Confirmation and reserve were not accessed. U1 remains COMPLETE / INFORMATION_NEED_AUTHORING_DEFECT; U2 remains COMPLETE / EXACT_HINT_ROUTING_SUPPORTED. U3 is COMPLETE / "
        + outcome
        + ".",
        "",
        "R1.7 = NEXT. Begin R1.7 — prospective query-term discrimination / weighting investigation. Do not modify U3 production routing automatically. True BM25F remains MANDATORY AFTER R1.7. Downstream Localization continuation is PRESERVED. This task stops after Stage D.",
        "",
    ]
    return "\n".join(lines).encode()


def artifacts(a: Any) -> dict[str, bytes]:
    markdown = report(a)
    trace = {
        "schema": "case-0013-stage-d-trace-v1",
        "scope": "Inert captured development evidence; complete deterministic calculation trace",
        "analysis": a,
    }
    return {
        "analysis.json": encoded(a),
        "analysis.md": markdown,
        "STAGE_D_REVIEW.md": markdown,
        "trace.json": encoded(trace),
        "TRACE.md": markdown,
    }
