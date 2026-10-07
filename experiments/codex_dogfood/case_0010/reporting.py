# Copyright (c) 2026
# ruff: noqa: C901, COM812, E501, ISC004, PLR0912, PLR0915, RUF001 -- bounded scientific report with intentional mathematical notation
"""Render the joined analysis without ranking candidates by a new objective."""

from __future__ import annotations

from typing import Any

INTERPRETATION = {
    "decision": "No development-selected configuration earned a production-adoption checkpoint. The exact outcome is MIXED / NO SAFE REPLACEMENT. BASELINE_ROBUST is inapplicable: C's union ratio 232/257 and D's max-own ratio 178/192 are outside the required 0.95–1.05 band. C's 9.728% union reduction is below 10%, without rounding or discretionary near-pass; satisfying that threshold would require at most 231 resources (0.9 × 257 = 231.3). Useful sensitivity exists, but no challenger passes every frozen gate.",
    "D_k1_only": "D is the clean k1-only comparison. Higher k1 preserves all REQUIRED reach. It worsens global completion 360→366 (+1.667%), improves max-own 192→178 (−7.292%), and reduces union 257→243 (−5.447%), below the meaningful threshold. Eight obligations improve (ownership, range, identity, frame, materialization, package, tests, validation), assembly ties, and documentation worsens 15→19 (1.266667×), exceeding 1.25×. Development's stable max-own/union improvement replicates directionally, including nine nonworse obligations, but prospective per-obligation safety does not. Thus k1=2.4 does not earn production-candidate status under this protocol.",
    "D_mechanics": "For REQUIRED repository/resource.py in the identity lane, identity TF=4, DF=189, IDF=1.032254, length=299 versus average 569.743879: saturation rises 1.843968→2.452822, content score 1.903444→2.531936, and rank 192→178. There is no filename contribution. Repetition gains also benefit UNNECESSARY competitors: conversation/history.py's order TF=3, DF=79, IDF=1.900886, length=158 has D saturation 2.488308 and contribution 4.729990, moving 111→96 and newly overtaking REQUIRED observation.py. That target's own score rises 3.739272→4.112282 while its rank worsens 105→112. Exact overtaker-set changes, rather than target score alone, explain ranking movement. The documentation bottleneck has its own paired diagnostic below.",
    "B_aggressive": "B does not replicate a generally improved own completion: max-own worsens 192→196 (+2.083%), occurrences grow 556→623, and only three obligations are nonworse (range, frame, tests). Global depth worsens modestly 360→363, within the global gate; union falls to 243, below 10% improvement. Materialization 8→31, assembly 1→12, package 32→54, and validation 12→41 violate 1.25×. The development pattern remains mixed and prospective completion benefit weakens; global cost is less severe here than Case 0006's 155→212. Removing length normalization removes long-resource suppression while amplified filename evidence helps and collides: codecs/text.py gets 10.720706 weighted filename score versus 1.558687 at A. In the frame lane, unnecessary B-0015 validation and B-0008 repository filenames contribute 10.047761 each, newly overtaking required materialization.py. Long REQUIRED architecture.md improves package rank 9→3, while long UNNECESSARY ADR-0002 (8,240 tokens) improves range rank 77→5. These are joint configuration effects, not isolated causal attribution to b or filename weight.",
    "C_burden": "C directionally reinforces development burden reduction: union 257→232 (−9.728%), occurrences 556→506, max-own 192→183 (−4.688%), and global depth ties at 360. Six obligations improve, assembly ties, and materialization, package and validation worsen. Materialization 8→13 (1.625×) and validation 12→16 (1.333333×) violate safety. Medium length normalization and filename weight 1 jointly boost text.py: weighted filename contribution 1.558687→6.098211, content 8.881946→10.561142, rank 65→26. Filename collisions also boost unnecessary localization/identity.py (identity lane 130→61), whose filename identity contribution is 5.429515. C is a near-threshold burden improvement, not a passing replacement.",
    "parameters": "k1: the isolated D comparison supports useful repetition sensitivity, not adoption of 2.4. b: the selected b=0 arm has serious obligation regressions and benefits both long required and irrelevant resources; b=0.5 offers burden improvements with regressions; b=0.75 with higher k1 is mostly stable but fails documentation safety. Filename weights 1 and 2 strengthen both helpful and colliding stems in C/B; 0.25 remains the unchanged production setting. Only D isolates one parameter. No causal optimum for b or filename weight, untested values, or universal production optimum follows from these three joint arms.",
    "development": "Keep development and Case 0010 separate. B weakens the completion-selected pattern and reinforces its known mixed/global-risk character. C reinforces the burden direction, with materially smaller gains than Case 0005's 151→106 and unsafe prospective obligations. D reinforces development's broad directional own/union stability, while its documentation regression weakens any claim of per-obligation robustness. Worst historical own/union ratios are B=194/185, C=1, D=253/256; all satisfy 1.25. No configuration was reselected or optimized using prospective gold.",
    "R1_7_inputs": "Retain obligation-specific footprint/yield profiles, high-TF required/competitor changes, filename collisions and full-task term evidence. Examples: frame/repository DF=217, IDF=0.894445, 217/531 matched, 5 REQUIRED, 4 HELPFUL, 208 UNNECESSARY; identity/identity DF=189, IDF=1.032254, 4/7/178; ownership/context DF=234, IDF=0.819188, 5/4/225. More selective cues include ownership/planning (DF=28, 5/3/20), range/range (DF=18, 2/2/14), identity/lineage (DF=14, 1/1/12), and validation/mypy (DF=13, 2/1/10). In the full-task global bottleneck, rare planning/public evidence competes with ubiquitous context/repository/python/from evidence in long query text. Those contributions and repeated identity/order terms are direct inputs for R1.7 to investigate; this checkpoint neither implements weighting nor claims a term is harmful merely from footprint.",
    "failure_classes": "All required evidence is positively retrieved; the remaining observed problem is ranking discrimination, not required reach. Even C's smallest union is 232 versus the gold minimum 22, with 439 unnecessary prefix occurrences. R1.5 establishes RANKING_DISCRIMINATION_FAILURE on REQUIRED subjects with at least 20 unnecessary overtakers. REPRESENTATION_FAILURE and VOCABULARY_SEMANTIC_MISMATCH are not established by identical canonical parameter arms with no misses; RELATIONAL_RELEVANCE is not assessed by these lexical captures. CONTEXT_DISCLOSURE_FAILURE is outside this experiment's scope; INFORMATION_NEED_OBLIGATION_FAILURE is not supported (clean task gap NONE), without claiming end-to-end task success. Potential purpose-relative tuning is a future hypothesis suggested by mixed obligation effects, not implementation authorization.",
}


def report(data: dict[str, Any]) -> str:
    """Keep JSON and Markdown measurements mechanically correspondent."""
    arms = data["arms"]
    lines = [
        "# Case 0010 Stage D — joined canonical BM25 parameter sensitivity",
        "",
        "## Join integrity",
        "",
        "The blind was intentionally lifted only after independent clean Stage C was committed. "
        "Frozen checkpoint ancestry, committed input bytes, Stage A/B seals, gold hashes, full content identities, "
        "native query identities and R1.5 score/positive-universe/tie replay all pass.",
        "",
    ]
    lines.extend(
        f"- {k}: `{v}`"
        for k, v in data["join"].items()
        if k in {"repository_id", "snapshot_id", "corpus_id", "task_identity"}
    )
    lines += [
        "",
        "531/531 resources, 10/10 obligations, 5,310/5,310 cells; zero duplicate, missing or unexpected identities. "
        "All four arms have the same eleven exact queries. Gold: 39 REQUIRED, 47 HELPFUL_ONLY, 5,224 UNNECESSARY, "
        "0 UNRESOLVED; 40 distinct units, 45 obligation-relative unit judgments, 22 unique REQUIRED resources. "
        "All ten obligations apply. Fourteen alternatives and nine complete combinations are validated. "
        "Every combination's resource union equals the complete 22-resource REQUIRED universe: global completion "
        "therefore equals its last resource's rank. All 40 units are INFERABLE_AT_START; inherent discovery is zero. "
        "Task and repository-information gaps are NONE.",
        "",
        "## Primary prospective measurements",
        "",
        "Ratios use A as denominator; lower is better. Parameters are (k1, b, filename weight). "
        "Canonical tokenization, whole-resource frame, independent content/filename scoring and stable corpus tie rules "
        "remain identical. No identifier expansion, query rewriting or BM25F.",
        "",
        "| Arm | Parameters | Global positive | Own positive union | Own positive cells | REQUIRED resources/cells/unit judgments/distinct units |",
        "|---|---|---:|---:|---:|---|",
    ]
    for a, row in arms.items():
        m, p = row["metrics"], row["positive"]
        reach = f"{len(m['required_resource_reach'])}/22; {len(m['required_cells_reached'])}/39; {len(m['required_unit_judgments_reached'])}/45; {len(m['distinct_units_reached'])}/40"
        lines.append(
            f"| {a} | {row['parameters']} | {p['global_resources']} | {p['own_union']} | {p['own_cells']} | {reach} |"
        )
    lines += [
        "",
        "For B, C and D, A-only REQUIRED, challenger-only REQUIRED and missed-by-both are empty "
        "for resources, cells, obligation-relative units and distinct units. Membership is stable, verified by exact sets.",
        "",
        "| Arm | Global completion | Ratio | Max-own | Ratio | Change | Prefix occurrences | Unique union | Union/22 | Excess | Union change vs A | REQUIRED | HELPFUL | UNNECESSARY |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for a, row in arms.items():
        m = row["metrics"]
        n, c = m["normalized"], m["complete_prefix_composition"]
        lines.append(
            f"| {a} | {m['global']} | {n['global']:.6f} | {m['max_own']} | {n['max_own']:.6f} | {(n['max_own'] - 1) * 100:+.3f}% | {m['prefix_occurrences']} | {m['prefix_union']} | {m['prefix_union'] / 22:.6f} | {m['excess']} | {(n['prefix_union'] - 1) * 100:+.3f}% | {c.get('REQUIRED', 0)} | {c.get('HELPFUL_ONLY', 0)} | {c.get('UNNECESSARY', 0)} |"
        )
    lines += [
        "",
        "### Per-obligation accepted-alternative completion",
        "",
        "All members of one alternative are required. Equal-depth alternatives tie by frozen alternative identity; "
        "no members are mixed between alternatives. Each cell below reports depth (ratio to A).",
        "",
        "| Obligation | A | B | C | D | Best | Notes |",
        "|---|---:|---:|---:|---:|---|---|",
    ]
    for ob in arms["A"]["metrics"]["own_depths"]:
        depths = {a: arms[a]["metrics"]["own_depths"][ob] for a in "ABCD"}
        values = [f"{depths[a]} ({depths[a] / depths['A']:.6f})" for a in "ABCD"]
        best = ", ".join(a for a in "ABCD" if depths[a] == min(depths.values()))
        notes = "; ".join(
            f"{a} {'improves' if depths[a] < depths['A'] else 'worsens' if depths[a] > depths['A'] else 'ties'}"
            for a in "BCD"
        )
        lines.append(f"| {ob} | " + " | ".join(values) + f" | {best} | {notes} |")
    lines += [
        "",
        "### Exact frozen gates",
        "",
        data["decision_rule"],
        "",
        "| Gate | A | B | C | D |",
        "|---|---|---|---|---|",
    ]
    labels = {
        "required_reach_safe": "REQUIRED reach safe",
        "global_le_1_05": "Global ≤1.05×",
        "max_own_le_1_05": "Max-own ≤1.05×",
        "meaningful_primary_improvement": "≥10% primary improvement",
        "no_obligation_gt_1_25": "No obligation >1.25×",
        "half_obligations_nonworse": "≥half obligations nonworse",
        "cost_le_3": "Cost ≤3×",
        "development_safe_le_1_25": "Development safety ≤1.25",
    }
    for key, label in labels.items():
        values = ["PASS" if arms[a]["gates"][key] else "FAIL" for a in "BCD"]
        reference = (
            "—"
            if key
            in {
                "meaningful_primary_improvement",
                "no_obligation_gt_1_25",
                "half_obligations_nonworse",
            }
            else "baseline"
        )
        lines.append(f"| {label} | {reference} | " + " | ".join(values) + " |")
    lines += [
        "| Overall prospective rule | BASELINE | "
        + " | ".join(
            "PASS" if all(arms[a]["gates"].values()) else "FAIL" for a in "BCD"
        )
        + " |",
        "",
        f"**Outcome: {data['outcome']}. Passing candidates: {data['passing_candidates']}.**",
        "No pre-frozen prospective precedence chooses a single winner if several candidates pass; all would be retained. "
        "A candidate earns a separate production-adoption checkpoint, never automatic adoption.",
        "",
        "## Supporting top-K and paired REQUIRED ranks",
        "",
        "Global labels are an explicit resource projection: REQUIRED if required by any obligation, otherwise "
        "HELPFUL_ONLY if helpful to any, otherwise UNNECESSARY. Own labels are obligation-relative. "
        "R+H is REQUIRED plus HELPFUL_ONLY. These descriptive metrics do not override the frozen gates.",
        "",
        "| Arm | K | Global R | Global R+H | Global U | Own R | Own R+H | Own U | Own denominator |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for a, row in arms.items():
        for k in ("5", "10", "20"):
            g, own = row["global_top_k"][k], row["metrics"]["top_k"][k]
            labels = own["labels"]
            lines.append(
                f"| {a} | {k} | {g['REQUIRED']} | {g['REQUIRED'] + g['HELPFUL_ONLY']} | {g['UNNECESSARY']} | {labels.get('REQUIRED', 0)} | {labels.get('REQUIRED', 0) + labels.get('HELPFUL_ONLY', 0)} | {labels.get('UNNECESSARY', 0)} | {own['denominator']} |"
            )
    lines += [
        "",
        "Rank delta = challenger minus A; negative improves. All 39 REQUIRED cells are paired.",
        "",
        "| Arm | Improved | Unchanged | Worsened | Median delta | Best improvement | Worst regression |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for a in "BCD":
        p = arms[a]["paired_required"]
        lines.append(
            f"| {a} | {p['improved']} | {p['unchanged']} | {p['worsened']} | {p['median_delta']} | {p['best_improvement']} | {p['worst_regression']} |"
        )
    lines += [
        "",
        "## R1.5 diagnostic evidence",
        "",
        "Representatives are chosen deterministically: largest own-lane REQUIRED gain and regression for each challenger "
        "(obligation/address ties), its largest completion-ratio regression bottleneck, plus its global completion bottleneck. Full explanations, source spans, every "
        "term and changed unnecessary overtaker are in analysis.json. Mechanics reconstruct captured scores, "
        "not a second query execution. DF/IDF and lexical matches do not change between arms. Global-lane diagnostics retain no obligation judgment; their overtaker label counts are unjudged, rather than negative evidence.",
    ]
    for record in data["diagnostics"]:
        a, b, pair = record["A"], record["challenger"], record["pair"]
        lines += [
            "",
            f"### {record['arm']} / {record['selection']}: {record['obligation']}",
            "",
            f"`{record['resource']}`: rank {a['rank']} → {b['rank']}, score {a['score']:.6f} → {b['score']:.6f}. "
            f"Overtakers added {len(pair['new_overtakers'])}, removed {len(pair['removed_overtakers'])}. "
            f"New overtaker labels: {pair['new_overtaker_labels']}.",
            "",
            "| Field/term | TF | DF | IDF | Length / average | Saturation A → challenger | Weighted contribution A → challenger |",
            "|---|---:|---:|---:|---|---|---|",
        ]
        old = {(t["field"], t["term"]): t for t in a["terms"]}
        # Largest positive/negative term changes plus high TF and filename evidence.
        ranked = sorted(
            b["terms"],
            key=lambda t: (
                -abs(
                    t["weighted_contribution"]
                    - old[t["field"], t["term"]]["weighted_contribution"]
                ),
                t["field"],
                t["term"],
            ),
        )
        selected = ranked[:6] + [t for t in b["terms"] if t["field"] == "filename"]
        seen = set()
        for t in selected:
            term_key = t["field"], t["term"]
            if term_key in seen:
                continue
            seen.add(term_key)
            prev = old[term_key]
            lines.append(
                f"| {t['field']}/{t['term']} | {t['tf']} | {t['df']} | {t['idf']:.6f} | {t['length']} / {t['average_length']:.6f} | {prev['tf_saturation']:.6f} → {t['tf_saturation']:.6f} | {prev['weighted_contribution']:.6f} → {t['weighted_contribution']:.6f} |"
            )
        for side, ex in (("A", a), (record["arm"], b)):
            content = sum(
                t["weighted_contribution"]
                for t in ex["terms"]
                if t["field"] == "content"
            )
            filename = sum(
                t["weighted_contribution"]
                for t in ex["terms"]
                if t["field"] == "filename"
            )
            lines.append(
                f"\n{side}: content {content:.6f}; weighted filename {filename:.6f}."
            )
        for changed in record["unnecessary_overtakers"][:3]:
            ex = changed["challenger"]
            top = max(ex["terms"], key=lambda t: t["weighted_contribution"])
            lines.append(
                f"\n{changed['change']} UNNECESSARY overtaker `{changed['resource']}`: "
                f"rank {changed['A']['rank']} → {ex['rank']}; leading {top['field']}/{top['term']} "
                f"TF {top['tf']}, DF {top['df']}, IDF {top['idf']:.6f}, length {top['length']}/{top['average_length']:.6f}, "
                f"saturation {top['tf_saturation']:.6f}, weighted contribution {top['weighted_contribution']:.6f}."
            )
    lines += [
        "",
        "## Query-term discrimination inputs for R1.7",
        "",
        "Profiles are obligation-relative. Matching resources are content/positive filename union; DF/IDF below "
        "refer to content, with independent filename profiles retained in JSON. Yields describe gold, "
        "not instructions to remove or weight terms. Representative high-footprint terms are selected per lane "
        "by descending effective matched count; high-value terms by REQUIRED yield (then count, then term).",
        "",
        "| Obligation | Selection | Term | Content DF | IDF | Matched/frame | REQUIRED | HELPFUL | UNNECESSARY | R yield | H yield | U yield |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for ob, profiles in data["query_profiles"].items():
        positive = [p for p in profiles if p["effective_matching_resources"]]
        common = sorted(
            positive, key=lambda p: (-len(p["effective_matching_resources"]), p["term"])
        )[:2]
        valuable = sorted(
            positive,
            key=lambda p: (
                -p["required_yield"],
                -p["judged_labels"].get("REQUIRED", 0),
                p["term"],
            ),
        )[:2]
        for selection, group in (("footprint", common), ("yield", valuable)):
            for p in group:
                f = p["fields"][0]
                n, labels = len(p["effective_matching_resources"]), p["judged_labels"]
                r, h, u = (
                    labels.get(k, 0)
                    for k in ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")
                )
                lines.append(
                    f"| {ob} | {selection} | {p['term']} | {f['df']} | {f['idf']:.6f} | {n}/531 ({n / 531:.3%}) | {r} | {h} | {u} | {r / n:.3%} | {h / n:.3%} | {u / n:.3%} |"
                )
    lines += [
        "",
        "## Captured costs and development comparison",
        "",
        "Single treatment-run descriptive observations, not latency benchmarks. Shared index construction is "
        "0.4245589000056498 s; diagnostics are excluded from query timing. No second treatment execution.",
        "",
        "| Arm | Median ms | p95 ms | Eleven-query sum s | Median ratio | p95 ratio | Development worst own/union |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    base = arms["A"]["cost"]
    for a, row in arms.items():
        c, d = row["cost"], row["development"]["worst_own_union_exact"]
        lines.append(
            f"| {a} | {c['median_query_seconds'] * 1000:.6f} | {c['p95_query_seconds'] * 1000:.6f} | {c['sum_query_seconds']:.9f} | {c['median_query_seconds'] / base['median_query_seconds']:.6f} | {c['p95_query_seconds'] / base['p95_query_seconds']:.6f} | {d[0]}/{d[1]} ({d[0] / d[1]:.6f}) |"
        )
    lines += [
        "",
        "Development and prospective data remain separate; only the pre-frozen development safety bound enters "
        "candidate gating. Case 0008 remains supplementary for incomplete own metrics.",
        "",
        "## Interpretation and limits",
        "",
        *[value + "\n" for value in data["interpretation"].values()],
        "",
        "Production parameters remain k1=1.2, b=0.75, filename weight=0.25. No production change, query weighting, "
        "BM25F, or R1.7 execution occurred. Confirmation/reserve access: NO. All Stage C attestations retain their "
        "historical NO values; this later authorized Stage D intentionally accesses treatment data.",
        "",
        "R1 DONE; R1.5 DONE; R1.6 DONE. R1.6b remains not required before BM25F; no concrete scorer pathology "
        "was exposed. Next: R1.7 — investigate query-term discrimination and weighting using the completed "
        "R1.5 diagnostics and R1.6 parameter evidence, without yet changing production query semantics. "
        "After R1.7, R2 — true BM25F / field-aware sparse retrieval remains mandatory. R3–R6 and the "
        "preserved Localization continuation follow.",
        "",
    ]
    return "\n".join(lines)
