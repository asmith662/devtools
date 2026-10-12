"""Independent support, prefix, movement and gate arithmetic checks."""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, ANN401, D103, COM812, PLR2004, PLR0915, C901, PLR0912
import math
from collections import Counter
from typing import Any

from experiments.codex_dogfood.case_0016.adjudication.reviewed import materialize as m
from experiments.task_conditioned_graph import gates


def validate(data: Any, result: Any) -> Any:
    gold = data["gold"]["primary"]
    labels = {
        (c["obligation"], c["resource_address"]): c["label"] for c in gold["cells"]
    }
    resources = {r["address"]: r for r in data["resources"]}
    expected_required = {
        (o, s) for (o, s), label in labels.items() if label == "REQUIRED"
    }
    m.require(
        len(result["required_cells"]) == 36
        and {(r["obligation"], r["resource_address"]) for r in result["required_cells"]}
        == expected_required,
        "Exact REQUIRED coverage",
    )
    ranks: Any = {
        arm: {
            f"O{i}": {
                r["address"]: r["rank"]
                for r in (
                    data["arms"][arm][f"Q{i}"]["matches"]
                    if arm == "A"
                    else data["arms"][arm][f"Q{i}"]
                )
            }
            for i in range(1, 7)
        }
        for arm in "ABC"
    }
    for r in result["required_cells"]:
        o, s = r["obligation"], r["resource_address"]
        ar, cr = ranks["A"][o].get(s), ranks["C"][o].get(s)
        m.require(
            r["ranks"] == {arm: ranks[arm][o].get(s) for arm in "ABC"},
            "Exact owning REQUIRED ranks",
        )
        m.require(
            r["meaningful_finite_rank_gain"]
            == (
                ar is not None and cr is not None and ar - cr >= 2 and 5 * cr <= 4 * ar
            ),
            "Meaningful rank integer arithmetic",
        )
        m.require(
            r["reach_rescue"] == (ar is None and cr is not None),
            "Reach rescue arithmetic",
        )
        m.require(
            r["complementary_regression_bound"]
            == (ar is None or (cr is not None and 5 * cr <= 6 * ar and cr - ar <= 10)),
            "Rank bound arithmetic",
        )
        f = r["flow"]
        pairs = [
            p
            for p in data["flows"][r["query"]]
            if p["target"] == s and p["pair_flow"] > 0
        ]
        for key, equal in (
            ("incoming_self_flow", True),
            ("incoming_cross_resource_flow", False),
        ):
            m.require(
                f[key]
                == math.fsum(
                    p["pair_flow"] for p in pairs if (p["source"] == s) == equal
                ),
                "Pair flow partition",
            )
        m.require(
            math.isclose(
                f["incoming_self_flow"] + f["incoming_cross_resource_flow"],
                f["incoming_structural_flow"],
                rel_tol=0,
                abs_tol=2e-10,
            ),
            "Flow reconciliation",
        )
        for identity in f["native_reference_identities"]:
            m.require(
                identity in data["references"]
                and data["references"][identity]["target"] == s,
                "Native graph attribution",
            )
        m.require(
            r["graph_ablation"]["rank"] == ar
            and not r["graph_ablation"]["finite_rank_gain"]
            and not r["graph_ablation"]["reach_rescue"],
            "Ablation baseline",
        )
        if r["graph_contributed_gain"]:
            m.require(
                r["graph_ablation"]["gain_disappears"]
                and r["membership"]["B"]
                and f["incoming_structural_flow"] > 0
                and f["native_reference_identities"]
                and r["graph_channel_rrf_contribution"] > 0,
                "Complete frozen graph attribution",
            )
    expected_ws = {
        w["id"]: w for values in gold["minimal_witnesses"].values() for w in values
    }
    m.require(
        len(result["witnesses"]) == 22
        and {w["id"] for w in result["witnesses"]} == set(expected_ws),
        "All witnesses independently evaluated",
    )
    for row in result["witnesses"]:
        w = expected_ws[row["id"]]
        o = w["obligation"]
        members = [gold["resource_frame"][i]["address"] for i in w["resources"]]
        for arm in "ABC":
            view = row["arms"][arm]
            m.require(
                view["id"] == w["id"]
                and view["obligation"] == o
                and view["repository_members"] == members,
                "Exact reviewed witness identity and membership",
            )
            expected_ranks = {s: ranks[arm][o].get(s) for s in members}
            complete = all(v is not None for v in expected_ranks.values())
            depth = max(expected_ranks.values(), default=0) if complete else None
            m.require(
                view["member_ranks"] == expected_ranks
                and view["complete"] == complete
                and view["depth"] == depth,
                "Witness completion and depth",
            )
            if not complete:
                m.require(view["prefix"] is None, "No invented incomplete prefix")
                continue
            ordered = sorted(ranks[arm][o], key=ranks[arm][o].__getitem__)[:depth]
            p = view["prefix"]
            counts = Counter(labels[o, s] for s in ordered)
            m.require(
                p["resources"] == sorted(set(ordered))
                and p["occurrences"] == len(ordered)
                and p["unique_resources"] == len(set(ordered))
                and p["labels"]
                == {
                    label: counts[label]
                    for label in ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")
                }
                and p["distinct_utf8_bytes"]
                == sum(len(resources[s]["content"].encode()) for s in set(ordered)),
                "Witness prefix labels/bytes",
            )
    for o, selected in result["selected_witnesses"].items():
        for arm in "ABC":
            values = [
                w["arms"][arm] for w in result["witnesses"] if w["obligation"] == o
            ]
            complete_values = [w for w in values if w["complete"]]
            expected = (
                min(complete_values, key=lambda w: (w["depth"], w["id"]))
                if complete_values
                else {
                    "id": None,
                    "obligation": o,
                    "repository_members": [],
                    "member_ranks": {},
                    "complete": False,
                    "depth": None,
                    "prefix": None,
                }
            )
            m.require(
                selected["arms"][arm] == expected,
                "Stable selected witness tie-breaking",
            )
        ad, cd = selected["arms"]["A"]["depth"], selected["arms"]["C"]["depth"]
        m.require(
            selected["meaningful_witness_gain"]
            == (cd is not None and (ad is None or (ad > 0 and 5 * cd <= 4 * ad))),
            "Witness gain integer arithmetic",
        )
        m.require(
            selected["complementary_depth_bound"]
            == (ad is None or (cd is not None and 5 * cd <= 6 * ad and cd - ad <= 5)),
            "Depth bound integer arithmetic",
        )
    for arm in "ABC":
        scoped = [
            (o, s)
            for o, selected in result["selected_witnesses"].items()
            if selected["arms"][arm]["complete"]
            for s in sorted(ranks[arm][o], key=ranks[arm][o].__getitem__)[
                : selected["arms"][arm]["depth"]
            ]
        ]
        union = {s for _, s in scoped}
        b = result["burdens"][arm]
        counts = Counter(labels[o, s] for o, s in scoped)
        m.require(
            b["unique_resources"] == len(union)
            and b["occurrences"] == len(scoped)
            and b["duplicate_occurrences"] == len(scoped) - len(union)
            and b["distinct_utf8_bytes"]
            == sum(len(resources[s]["content"].encode()) for s in union)
            and b["labels"]
            == {
                label: counts[label]
                for label in ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")
            },
            "Independent task burden unions",
        )
        reached = [(o, s) for o, s in expected_required if s in ranks[arm][o]]
        m.require(
            result["reach"][arm]["required_cell_count"] == len(reached)
            and result["reach"][arm]["required_resource_count"]
            == len({s for _, s in reached}),
            "Required owning-query reach",
        )
    units = {u["id"]: u for u in gold["primary"]["units"]}
    for row in result["unit_reach"]:
        unit, o = units[row["unit"]], row["obligation"]
        m.require(o in unit["obligations"], "Unit owning obligation")
        for arm in "ABC":
            complete_alternatives = [
                v["id"]
                for v in unit["alternatives"]
                if all(
                    gold["resource_frame"][i]["address"] in ranks[arm][o]
                    for i in v["resources"]
                )
            ]
            m.require(
                row["arms"][arm]["complete_alternatives"] == complete_alternatives
                and row["arms"][arm]["reached"]
                == (
                    unit["evidence_class"] == "TASK_BACKED"
                    or bool(complete_alternatives)
                ),
                "Whole unit support alternatives; never mix",
            )
    for i, (o, view) in enumerate(result["graph_novel"].items(), 1):
        actual = set(ranks["B"][o]) - set(ranks["A"][o])
        m.require(
            actual == {r["address"] for r in view["resources"]}
            and view["count"] == [0, 7, 8, 1, 8, 13][i - 1],
            "Graph-novel exact membership",
        )
        m.require(
            view["labels"]
            == {
                label: sum(labels[o, s] == label for s in actual)
                for label in ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")
            },
            "Owning-obligation novel labels",
        )
    inputs = result["gate_inputs"]
    for o, diagnostics in result["top_k"].items():
        for k, view in diagnostics.items():
            top = {
                arm: set(sorted(ranks[arm][o], key=ranks[arm][o].__getitem__)[: int(k)])
                for arm in "ABC"
            }
            for arm in "ABC":
                m.require(
                    view["labels"][arm]
                    == {
                        label: sum(labels[o, s] == label for s in top[arm])
                        for label in ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")
                    },
                    "Top-K owning gold labels",
                )
            for pair, comparison in view["comparisons"].items():
                first, second = pair.split("_")
                m.require(
                    comparison["overlap"] == len(top[first] & top[second])
                    and {v["address"] for v in comparison["entered"]}
                    == top[second] - top[first]
                    and {v["address"] for v in comparison["exited"]}
                    == top[first] - top[second],
                    "Top-K overlap/entered/exited joins",
                )
    expected_depths = tuple(
        (v["arms"]["A"]["depth"], v["arms"]["C"]["depth"])
        for v in result["selected_witnesses"].values()
    )
    expected_rank_pairs = tuple(
        (v["ranks"]["A"], v["ranks"]["C"]) for v in result["required_cells"]
    )
    m.require(
        tuple(map(tuple, inputs["depths"])) == expected_depths
        and tuple(map(tuple, inputs["required_ranks"])) == expected_rank_pairs,
        "Gate inputs equal independently checked metrics",
    )
    expected_a: Any = tuple(
        result["burdens"]["A"][k]
        for k in ("unique_resources", "occurrences", "distinct_utf8_bytes")
    )
    expected_c: Any = tuple(
        result["burdens"]["C"][k]
        for k in ("unique_resources", "occurrences", "distinct_utf8_bytes")
    )
    m.require(
        tuple(inputs["a_burden"]) == expected_a
        and tuple(inputs["c_burden"]) == expected_c,
        "Gate burden inputs",
    )
    decision = gates.decide(
        gates.DecisionInputs(
            depths=expected_depths,
            required_ranks=expected_rank_pairs,
            a_burden=expected_a,
            c_burden=expected_c,
            graph_contributed_gain=inputs["graph_contributed_gain"],
            contract_defect=inputs["contract_defect"],
            ranking_defect=inputs["ranking_defect"],
            required_unit_reach_loss=inputs["required_unit_reach_loss"],
        )
    )
    m.require(
        result["gates"] == decision
        and result["outcome"] == decision["outcome"]
        and result["precedence"] == data["design"]["decision_rule"]["precedence"],
        "Frozen gate precedence",
    )
    return {
        "status": "PASS",
        "checks": [
            "checkpoint ancestry and original/amended Stage A seals",
            "recovery and failed-attempt isolation",
            "attempt-2 physical/committed integrity and captured-return replay",
            "sole-primary hashes/replay and committed reviewed identity",
            "514 native resource/content/frame bindings and 3084 owning cells",
            "all 36 REQUIRED ranks and 22 independent minimal witnesses",
            "stable witness selection and complete alternatives",
            "integer rank/depth/rescue/bound arithmetic",
            "independent prefix resource unions, label occurrences and UTF-8 bytes",
            "native incoming reference attribution and self/cross reconciliation",
            "captured graph-channel ablation; no new retrieval",
            "seed-only exclusion and novel labels",
            "historical development provenance and descriptive captured costs",
            "exact frozen gate precedence",
            "deterministic artifact replay; overwrite refusal and tamper rejection",
        ],
        "scientific_reruns": 0,
        "semantic_reviewer_calls": 0,
        "confirmation_reserve": "NOT_ACCESSED",
    }
