"""Complete inspectable human and machine surfaces for the bounded U2 join."""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, ANN401, D103, E501, COM812, RUF005
from typing import Any

from experiments.codex_dogfood.case_0012.stage_d.authentication import encoded


def block(value: Any) -> list[str]:
    return ["", "```json", encoded(value).decode().rstrip(), "```", ""]


def trace(analysis: Any) -> Any:
    return {
        "schema": "case-0012-stage-d-trace-v1",
        "checkpoints": analysis["checkpoints"],
        "task": analysis["task_identity"],
        "frame": analysis["frame"],
        "reviewed_gold_sha256": analysis["reviewed_gold_sha256"],
        "hints": analysis["hints"],
        "obligations": {
            ob["key"]: {
                "statement": ob["statement"],
                "reviewed_units": [
                    u
                    for u in analysis["reviewed_units"]
                    if ob["key"] in u["obligations"]
                ],
                "witnesses": analysis["reviewed_witnesses"][ob["key"]],
                "acquisition": {
                    arm: analysis["arms"][arm]["lanes"][ob["key"]]
                    for arm in ("A", "B", "C")
                },
                "comparison": analysis["comparisons"]["C"]["lanes"][ob["key"]],
            }
            for ob in analysis["obligations"]
        },
        "attribution": analysis["attribution"],
        "frozen_gates": analysis["frozen_gates"],
        "outcome": analysis["outcome"],
        "SEARCH_POLICY_FAILURE": "NOT_ASSESSED",
    }


def markdown(analysis: Any, *, trace_only: bool = False) -> bytes:
    lines = [
        "# Case 0012 Stage D effectiveness review",
        "",
        "## DID U2 IMPROVE ACQUISITION IN CASE 0012?",
        "",
        f"**YES, within this case: {analysis['outcome']}.**",
        "",
        "Exact-first routing reduces completion depth for choices, integrity, documentation and validation while retaining all REQUIRED resources/cells/units. Gains are supported for the tested direct-declaration, direct-method and resource-address families. Module routing has no owning-obligation REQUIRED target and is NOT_ASSESSED. Unsupported bare classes remain unsupported.",
        "",
        "The integrity snapshot target moves 138 to 1, but complete evidence finishes at 113 because another required member becomes the bottleneck. Source's selector moves 4 to 1 without changing depth 15. Resource-address documentation moves 13 to 2; choices moves 2 to 1 and validation 5 to 3. Semantic completeness ties. Case-wide unique union and byte reductions are small; captured execution cost increases within the frozen three-times gate.",
        "",
        "All prefix figures describe counterfactual inspection of independent obligation lists. No fictional task-global ranking, native treatment rerun, family ablation, actual evidence-inspection measurement or production routing change occurs.",
        "",
        "## Original task",
        "",
        "```text",
        analysis["task_text"].rstrip(),
        "```",
        "",
        "## Did we improve, by dimension",
    ]
    lines += block(analysis["did_we_improve"])
    lines += ["## Checkpoints, frame and exact join"] + block(
        {
            "checkpoints": analysis["checkpoints"],
            "frame": analysis["frame"],
            "reviewed_gold_sha256": analysis["reviewed_gold_sha256"],
            "B_C_effectiveness_equal": analysis["B_C_effectiveness_equal"],
        }
    )
    lines += ["## Task obligations"] + block(analysis["obligations"])
    lines += [
        "## H01-H10 exact targets and reviewed gold",
        "",
        "B and C have equal targets/ranks/effects; full native provenance and independently measured costs remain separate in analysis.json.",
        "",
        "| Hint | Family / obligation | Disposition | Native target | Reviewed label | Native rank | Exact tier | Routed | Saved | Witness / indispensable |",
        "|---|---|---|---|---|---:|---:|---:|---:|---|",
    ]
    for hint in analysis["hints"]["C"]:
        if not hint["target_effects"]:
            lines.append(
                f"| {hint['hint']} `{hint['text']}` | {hint['family']} / {hint['obligation']} | {hint['disposition']} | None; no locator | NOT_APPLICABLE | â€” | â€” | â€” | â€” | No promotion |"
            )
        for target in hint["target_effects"]:
            lines.append(
                f"| {hint['hint']} `{hint['text']}` | {hint['family']} / {hint['obligation']} | {hint['disposition']} | `{target['address']}` | {target['label']} | {target['native_rank']} | {target['exact_tier_position']} | {target['routed_position']} | {target['depth_saved']} | {target['in_at_least_one_complete_witness']} / {target['obligation_indispensable']} |"
            )
    lines += [
        "",
        "## Complete hint provenance, units and bottleneck shifts",
        "",
        "Witness effects are the combined captured route effects in that owning lane. A target's presence in an improved witness does not establish that its individual promotion caused the gain. Prior/post bottlenecks expose this distinction.",
    ]
    for arm in ("B", "C"):
        lines += ["### Arm " + arm] + block(analysis["hints"][arm])
    lines += [
        "## Route-family effectiveness",
        "",
        "| Family | Hints / admitted | Resolved / unsupported | REQUIRED / HELPFUL / UNNECESSARY | Effectiveness | C route ns |",
        "|---|---:|---:|---:|---|---:|",
    ]
    for family, values in analysis["route_families"]["C"].items():
        labels = values["target_labels"]
        lines.append(
            f"| {family} | {values['hint_count']} / {values['admitted_routes']} | {values['RESOLVED']} / {values['UNSUPPORTED']} | {labels.get('REQUIRED', 0)} / {labels.get('HELPFUL_ONLY', 0)} / {labels.get('UNNECESSARY', 0)} | {values['effectiveness']} | {values['resolution_ns']} |"
        )
    lines += block(analysis["route_families"])
    lines += [
        "## Every obligation completion and burden",
        "",
        "| Obligation | A depth | B/C depth | Delta | A unique bytes | B/C unique bytes | A unnecessary | B/C unnecessary |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for obligation in analysis["obligations"]:
        ob = obligation["key"]
        before, after = (
            analysis["arms"]["A"]["lanes"][ob],
            analysis["arms"]["C"]["lanes"][ob],
        )
        lines.append(
            f"| {ob} | {before['completion_depth']} | {after['completion_depth']} | {after['completion_depth'] - before['completion_depth']} | {before['metrics']['unique_utf8_bytes']} | {after['metrics']['unique_utf8_bytes']} | {before['metrics']['label_occurrences']['UNNECESSARY']} | {after['metrics']['label_occurrences']['UNNECESSARY']} |"
        )
    for arm in ("A", "B", "C"):
        lines += [
            "### Arm " + arm + ": every witness, chosen identity and exact prefixes"
        ] + block(analysis["arms"][arm]["lanes"])
    lines += [
        "## Complete task acquisition",
        "",
        "Frozen selection chooses minimum completion depth then reviewed witness identity independently for each obligation. Cross-lane union deduplicates resources; owning labels remain occurrence-relative. Every complete combination below is evaluated without mixing alternatives. Resource minima do not redefine the acquisition selection rule.",
    ]
    for arm in ("A", "B", "C"):
        value = analysis["arms"][arm]
        combinations = [
            {k: v for k, v in c.items() if k != "metrics"}
            | {
                "metrics": None
                if c["metrics"] is None
                else {
                    k: v
                    for k, v in c["metrics"].items()
                    if k not in {"prefixes", "unique_prefix_resources"}
                }
            }
            for c in value["all_complete_task_combinations"]
        ]
        selected = value["selected_complete_structure"]
        lines += ["### Arm " + arm] + block(
            {
                "selected_witnesses": selected["witnesses"],
                "selected_sufficient_resources": selected["sufficient_resources"],
                "selected_task_metrics": value["task"],
                "all_complete_combinations": combinations,
                "all_four_minimal_resource_unions": value[
                    "minimal_complete_resource_unions"
                ],
            }
        )
    lines += ["## Exact deltas and percentage fractions"] + block(
        analysis["comparisons"]
    )
    lines += ["## Candidate safety and exact reach sets"] + block(
        analysis["candidate_safety"]
    )
    lines += [
        "## Captured cost accounting",
        "",
        "Parent/child timings are retained separately. Composite arm and native grounding times overlap component measurements and are descriptive. Charged treatment arithmetic adds only the frozen index/query/inventory/route/presentation components. Frame preparation and final publication have no separately captured timing; no new benchmark runs.",
    ] + block(analysis["costs"])
    lines += ["## Every frozen gate, arithmetic and precedence"] + block(
        analysis["frozen_gates"]
    )
    lines += ["## Frozen decision rule, verbatim"] + block(
        analysis["frozen_decision_rule"]
    )
    lines += ["## Failure and non-improvement attribution"] + block(
        analysis["attribution"]
    )
    lines += [
        "## All final reviewed semantic units and exact support",
        "",
        "These are the committed treatment-blind units, not a new adjudication. Task-only supports contribute no repository resource; ALL resources in a support are complementary and ANY complete support substitutes.",
    ] + block(analysis["reviewed_units"])
    lines += ["## All final reviewed witnesses"] + block(analysis["reviewed_witnesses"])
    lines += ["## Reviewed sufficiency, all combinations and intersections"] + block(
        analysis["reviewed_task_sufficiency"]
    )
    if trace_only:
        lines += ["## Machine correspondence trace"] + block(trace(analysis))
    lines += [
        "## Scope and next step",
        "",
        "U1 COMPLETE / INFORMATION_NEED_AUTHORING_DEFECT; U2 COMPLETE / "
        + analysis["outcome"]
        + "; U3 FUTURE; R1.7 RETAINED; R2 true BM25F MANDATORY; downstream Localization continuation PRESERVED.",
        "",
        "No production routing or source-disclosure behavior changes. Confirmation/reserve data were not accessed. Stop after Stage D publication; subsequent upstream/retained roadmap work requires its own scoped task. `.local/codex-result.md` remains operational and excluded from scientific evidence/hashes.",
        "",
    ]
    return "\n".join(lines).encode("utf-8")
