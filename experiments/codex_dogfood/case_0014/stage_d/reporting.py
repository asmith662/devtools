"""Deterministic human review of gold-relative arithmetic and causal evidence."""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, ANN401, D103, COM812, E501, C901
from typing import Any

from experiments.codex_dogfood.case_0014.adjudication.reviewed.materialize import (
    encoded,
)


def block(title: str, value: Any) -> str:
    return (
        "\n\n## "
        + title
        + "\n\n```json\n"
        + encoded(value).decode().rstrip()
        + "\n```\n"
    )


def rank(value: int | None) -> str:
    return "UNREACHED" if value is None else str(value)


def review(value: Any) -> str:
    resources = {r["resource"]: r["address"] for r in value["required_cells"]}
    text: str = (
        "# Case 0014 Stage D effectiveness review\n\nR1.7 = COMPLETE / **"
        + value["gates"]["outcome"]
        + "**\n\n"
    )
    text += (
        "## DID R1.7 IMPROVE?\n\n"
        + value["answer"]
        + "\n\n"
        + "C versus A is the sole effectiveness comparison. B versus A isolates anchor emphasis; C versus B diagnoses generic attenuation. No arm is selected retrospectively.\n"
    )
    text += block(
        "C versus A dimensions",
        value["did_r17_improve"],
    )
    text += "\n## Exact task\n\n" + value["task_text"]
    text += block(
        "Primary and reviewed gold",
        {
            "provenance": value["primary_policy"],
            "statistics": value["reviewed_summary"],
            "joins": value["joins"],
        },
    )
    text += "\n## All 30 semantic units\n\n| Unit | Evidence class | Owning obligations | Exact primary statement |\n|---|---|---|---|\n"
    for unit in value["semantic_units"]:
        text += f"| {unit['identity']} | {unit['evidence_class']} | {', '.join('O' + str(o) for o in unit['obligations'])} | {unit['statement'].replace('|', '&#124;')} |\n"
    text += "\nExact alternatives, spans and task provenance remain unchanged in [reviewed gold](../adjudication/reviewed/REVIEWED_GOLD.md) and analysis.json: semantic_units. Task-backed units have no retrieval rank or repository-byte cost.\n"
    text += "\n## All 34 REQUIRED resource/obligation cells\n\nDeltas are treatment rank minus baseline rank: negative improves. UNREACHED is never assigned a numeric rank. Required union membership denotes at least one minimal witness, not simultaneous necessity.\n\n| Obligation | Resource | A | B | C | B-A | C-B | C-A | Meaningful C/A | Regression bounded C/A | Obligation / task indispensable | Witnesses |\n|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---|\n"
    for row in value["required_cells"]:
        a, b, c = [rank(row["ranks"][arm]) for arm in "ABC"]
        changes = row["changes"]
        text += f"| {row['obligation']} | `{row['address']}` | {a} | {b} | {c} | {changes['A_to_B']['rank_delta_after_minus_before']} | {changes['B_to_C']['rank_delta_after_minus_before']} | {changes['A_to_C']['rank_delta_after_minus_before']} | {changes['A_to_C']['meaningful_rank_gain']} | {changes['A_to_C']['bounded']} | {row['obligation_indispensable']} / {row['task_indispensable']} | {', '.join(row['witness_memberships'])} |\n"
    text += "\n## All 36 witnesses calculated independently in A/B/C\n\nEvery row preserves the reviewed ALL-member witness. Alternative rows are never mixed. Metrics are occurrences / unique resources / REQUIRED / HELPFUL_ONLY / UNNECESSARY / distinct UTF-8 bytes.\n\n| Obligation | Witness | Arm | Repository member ranks | State | Completion depth | Prefix metrics |\n|---|---|---|---|---|---:|---|\n"
    for key, obligation in value["arms"]["A"]["lanes"].items():
        for i, witness in enumerate(obligation["witnesses"]):
            for arm in "ABC":
                w = value["arms"][arm]["lanes"][key]["witnesses"][i]
                members = "; ".join(
                    resources[rid] + "=" + rank(r)
                    for rid, r in w["member_ranks"].items()
                )
                metrics = w["metrics"]
                fields = (
                    "NOT_ASSESSED"
                    if metrics is None
                    else "/".join(
                        str(v)
                        for v in [
                            metrics["prefix_occurrences"],
                            metrics["unique_prefix_resources"],
                            metrics["label_occurrences"]["REQUIRED"],
                            metrics["label_occurrences"]["HELPFUL_ONLY"],
                            metrics["label_occurrences"]["UNNECESSARY"],
                            metrics["distinct_utf8_bytes"],
                        ]
                    )
                )
                text += f"| {key} | {witness['identity']} | {arm} | {members} | {w['state']} | {rank(w['completion_depth'])} | {fields} |\n"
    text += "\n## Selected witnesses and exact depth/gain decisions\n\nSelect minimum complete depth, then stable reviewed witness identity.\n\n| Obligation | A witness / depth | B witness / depth | C witness / depth | Meaningful B/A | Meaningful C/B | Meaningful C/A | C/A bounded |\n|---|---|---|---|---|---|---|---|\n"
    for key, row in value["obligation_comparisons"].items():
        selected = [
            str(row["selected_witnesses"][a]) + " / " + rank(row["depths"][a])
            for a in "ABC"
        ]
        text += f"| {key} | {' | '.join(selected)} | {row['comparisons']['A_to_B']['meaningful_witness_gain']} | {row['comparisons']['B_to_C']['meaningful_witness_gain']} | {row['comparisons']['A_to_C']['meaningful_witness_gain']} | {row['comparisons']['A_to_C']['bounded']} |\n"
    text += block(
        "Exact selected-depth integer arithmetic", value["obligation_comparisons"]
    )
    text += block(
        "Every witness change and captured role attribution",
        value["witness_comparisons"],
    )
    text += "\n## Case-wide completion-prefix burden\n\nUnique resources and exact UTF-8 bytes union selected mandatory prefixes. Repeated occurrences retain their own obligation label. There is no task-global ranking.\n\n| Arm | Complete obligations | Occurrences | Unique | Duplicates | REQUIRED | HELPFUL_ONLY | UNNECESSARY | UTF-8 bytes |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|\n"
    for arm, result in value["arms"].items():
        b = result["burden"]
        text += f"| {arm} | {result['complete_obligation_count']} | {b['prefix_occurrences']} | {b['unique_prefix_resources']} | {b['duplicate_occurrences']} | {b['label_occurrences']['REQUIRED']} | {b['label_occurrences']['HELPFUL_ONLY']} | {b['label_occurrences']['UNNECESSARY']} | {b['distinct_utf8_bytes']} |\n"
    text += block(
        "Required resource/cell/semantic-unit reach and no-loss checks",
        {
            "arms": {
                arm: result["required_reach"] for arm, result in value["arms"].items()
            },
            "C_loses_from_A": value["required_reach_losses"],
        },
    )
    text += block("A to B anchor attribution", value["anchor_attribution"])
    text += block(
        "B to C generic attenuation attribution", value["generic_attribution"]
    )
    text += "\n## Causal proofs for every REQUIRED cell\n\nAnchor emphasis and attenuation use unchanged captured native evidence. Crossing rows show the exact non-required consequence, rather than treating any upward non-required movement as harm. Each overtaker retains before/after ranks, labels, score gaps, exact per-term roles/multipliers and channel-adjusted totals. All scientific contribution values are read from the Stage B capture.\n"
    for row in value["required_cells"]:
        text += block(row["obligation"] + " / " + row["address"], row)
    text += block(
        "Query dilution not reduced: unchanged bottleneck overtaker proofs",
        value["query_dilution_not_reduced"],
    )
    text += block("Failure taxonomy", value["failure_attribution"])
    text += "\nQUERY_AUTHORING_LIMIT and LEXICAL_REPRESENTATION_LIMIT are not forced where evidence is insufficient. SEARCH_POLICY_FAILURE = NOT_ASSESSED. If every required cell is reached, neither unreached lexical class is observed.\n"
    text += "\n## Top-K gold-labeled diagnostics\n\nPair inversions/crossings are the captured Stage B diagnostics, joined to owning-obligation labels. They never select an outcome. R/H/U denotes REQUIRED / HELPFUL_ONLY / UNNECESSARY. Exact entered/exited identities and all inversion labels are in analysis.json: top_k_diagnostics.\n\n| Obligation | Pair | K | Entered R/H/U | Exited R/H/U | Inversions | Label-pair counts |\n|---|---|---:|---|---|---:|---|\n"
    for key, pairs in value["top_k_diagnostics"].items():
        for pair, sizes in pairs.items():
            for k, row in sizes.items():
                entered = "/".join(
                    str(row["entered_counts"][label])
                    for label in ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")
                )
                exited = "/".join(
                    str(row["exited_counts"][label])
                    for label in ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")
                )
                text += f"| {key} | {pair} | {k} | {entered} | {exited} | {row['inversion_count']} | {row['inversion_label_pair_counts']} |\n"
    text += block("Descriptive captured costs only", value["costs"])
    text += "\nNo shared, arm-child, wall or durability interval is charged twice. The unchanged reference acquisition is separate. Single-run cost differences do not select the ranking outcome.\n"
    text += block("Contract gates", value["contract_checks"])
    text += block("Application/classification gates", value["application_checks"])
    text += block("Frozen rule", value["frozen_rule"])
    text += block("Exact frozen gate inputs", value["gate_evidence"])
    text += block("Strong burden cross-products", value["gate_arithmetic"])
    text += block("Every gate result", value["gates"])
    text += block("Outcome precedence", value["precedence_application"])
    text += (
        "\n## Bounded interpretation and roadmap\n\n"
        + value["scope"]
        + "\n\nProduction behavior = UNCHANGED. Confirmation/reserve = NOT_ACCESSED. SEARCH_POLICY_FAILURE = NOT_ASSESSED. U1 = COMPLETE / INFORMATION_NEED_AUTHORING_DEFECT; U2 = COMPLETE / EXACT_HINT_ROUTING_SUPPORTED; U3 = COMPLETE / SELECTIVE_MECHANISM_ROUTING_SUPPORTED. Identifier-aware R1 remains a separate retrieval view. U2/U3 support bounded exact mechanism routing; R1.7 supplies query-side weighting evidence only.\n\nR1.7 = COMPLETE / "
        + value["gates"]["outcome"]
        + ". R2 true BM25F = NEXT / MANDATORY. Begin R2 true BM25F design/freeze. Test actual multi-field BM25F semantics rather than summing independent BM25 scores. Do not automatically productionize R1.7.\n"
    )
    return text.rstrip() + "\n"


def artifacts(value: Any) -> dict[str, bytes]:
    full = review(value)
    short = (
        "# Case 0014 R1.7 analysis\n\nOutcome: **"
        + value["gates"]["outcome"]
        + "**\n\n"
        + value["answer"]
        + "\n\n[Complete human review](STAGE_D_REVIEW.md) includes every REQUIRED cell and every witness in each arm. [analysis.json](analysis.json) owns complete deterministic arithmetic and captured attribution joins.\n"
    )
    short += block(
        "DID R1.7 IMPROVE?",
        value["did_r17_improve"],
    )
    short += block(
        "Gate decisions and precedence",
        {"gates": value["gates"], "precedence": value["precedence_application"]},
    )
    short += "\n" + value["scope"] + "\n"
    trace = {
        "schema": "case-0014-stage-d-trace-v1",
        "scientific_inputs": value["provenance"],
        "operations": "Read sealed bytes; authenticate inert JSON; join exact gold; calculate every witness; select frozen minimum/tie-break; apply frozen gates. No native operation or semantic adjudication.",
        "analysis": value,
    }
    trace_md = "# Case 0014 Stage D trace\n\n[Full replayable trace](trace.json) retains exact input checkpoints, all joins, cell/witness arithmetic, captured contributions, gates and precedence. [Human review](STAGE_D_REVIEW.md) explains every gate. No scientific native execution occurred.\n"
    trace_md += (
        block("Authentication", value["provenance"])
        + block(
            "Native/journal status",
            {
                "native": value["native_authentication"],
                "journal": {
                    k: v for k, v in value["journal"].items() if k != "operations"
                },
            },
        )
        + block("Final rule result", value["gates"])
    )
    return {
        "analysis.json": encoded(value),
        "analysis.md": short.rstrip().encode() + b"\n",
        "STAGE_D_REVIEW.md": full.encode(),
        "trace.json": encoded(trace),
        "TRACE.md": trace_md.rstrip().encode() + b"\n",
    }
