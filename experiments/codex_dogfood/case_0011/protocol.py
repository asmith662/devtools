# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, TRY003 -- finite pre-authored protocol projection
"""Project immutable manual authoring; never construct new needs or queries."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from devtools.context.localization import (
    LocalizationAnchor,
    LocalizationAnchorIdentity,
    LocalizationObligation,
    LocalizationObligationIdentity,
    LocalizationQueryIdentity,
    LocalizationTaskIdentity,
    LocalizationTaskInterpretation,
    ObligationLexicalQuery,
    RequirementStatus,
    SatisfactionCriterion,
    TaskProvenance,
)
from devtools.context.localization.identity import TaskTextSpan
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
)
from experiments.codex_dogfood.acquisition.needs import InformationNeed
from experiments.codex_dogfood.acquisition.trace import validate
from experiments.codex_dogfood.case_0009.artifacts import digest, read_json

CASE = Path(__file__).resolve().parent
START = "85f9f088c5be2afb7861803ee1a96ac7db0448a2"
AUTHOR_HASHES = {
    "task.txt": "37b23f717a8c35ecf390c3169aff24bd7c39f271afc9208fb7d9e780f91239d1",
    "authoring.json": "5f60a2d04a0b94c34c5b0014282f9393ce8bc4ff947d3d5754e84ff320a1e7ff",
    "AUTHORING.md": "db8dec9dc0f0241194fb7ea0954cfe16587195625a136f24b9f7cb2dd8bbc036",
}
ROUTE = "CANONICAL_RESOURCE_BM25"
DECISION = {
    "safety": "C loses no B REQUIRED unique resources, obligation/resource cells or obligation-relative/distinct REQUIRED units; compare exact sets, not just counts.",
    "coverage": "100% of Stage C REQUIRED units must map to at least one frozen need in committed independent C.5. Every missed unit is counted; nearly-all is not used.",
    "burden": "C completion-prefix unique union <=0.80*B OR C UNNECESSARY prefix occurrences <=0.80*B, AND the other burden metric <=1.05*B. Use exact rational comparisons; zero B unnecessary burden requires zero C unnecessary burden and cannot itself supply improvement.",
    "obligation_safety": "For every mandatory applicable obligation, C's unique union of responsible need-query completion prefixes <=1.25*B's best valid obligation-query depth. No rank fusion.",
    "cost": "Report every additional query and captured cost; no query-count gate. Cost to sufficient mandatory coverage is the global unique union of independently necessary query prefixes.",
    "C_assignment": "C.5 maps units to all responsible needs before outcomes are joined. Multiple mappings make each named query responsible; no post-hoc choice of the best-performing need. Unmapped units remain misses. Zero-unit needs have zero completion prefix but their query cost/positive results remain reported.",
    "alternatives": "Preserve complete gold alternatives. For each obligation and alternative, take all supporting resources for each mapped unit in that alternative; a need depth is the last required resource in its own captured ranking, or null for a miss. Choose a complete C alternative by minimum unique prefix union, then summed prefix occurrences, then maximum need depth, then frozen alternative identity. B chooses minimum all-member depth then alternative identity. Never mix members of competing alternatives.",
    "incomplete": "Unreachable completion remains null, never a synthetic rank. Undefined baseline ratios cannot pass the quantitative supported gate. A genuine reach rescue may qualify as complementary evidence, not an invented burden ratio. Report all incomplete mandatory obligations.",
    "metrics": [
        "REQUIRED resource/cell/unit reach",
        "query count",
        "positive candidate count",
        "completion-prefix occurrences",
        "completion-prefix unique resource union",
        "required/helpful/unnecessary prefix occurrences",
        "excess over minimum sufficient union",
        "resources inspected per REQUIRED unit",
        "resources inspected per completed obligation",
        "duplicate resources returned",
        "cost to sufficient obligation coverage",
    ],
    "outcomes": [
        "INFORMATION_NEED_DECOMPOSITION_SUPPORTED",
        "COMPLEMENTARY_BUT_NOT_CLEARLY_BETTER",
        "NO_MATERIAL_VALUE",
        "INFORMATION_NEED_AUTHORING_DEFECT",
        "EXPERIMENTAL_CONTRACT_DEFECT",
    ],
    "precedence": "Invalid scientific identity/score/packet/mapping contracts stop as EXPERIMENTAL_CONTRACT_DEFECT. Any unmapped REQUIRED unit or a MISFORMULATED need responsible for a REQUIRED unit yields INFORMATION_NEED_AUTHORING_DEFECT. Otherwise all safety/completeness/burden/obligation gates yield SUPPORTED. Reach-safe positive burden improvement or genuine completion rescue without all gates yields COMPLEMENTARY_BUT_NOT_CLEARLY_BETTER. Otherwise NO_MATERIAL_VALUE.",
    "need_labels": ["NECESSARY", "USEFUL_REDUNDANT", "UNNECESSARY", "MISFORMULATED"],
    "failure_attribution": [
        "GOOD_NEED / BAD_QUERY",
        "MISSING_INFORMATION_NEED",
        "REDUNDANT_INFORMATION_NEED",
        "QUERY_DILUTION",
        "RETRIEVAL_RANKING_FAILURE",
        "REPRESENTATION_FAILURE",
        "POSSIBLE_VOCABULARY_SEMANTIC_MISMATCH",
    ],
    "mixed_intent": "MIXED_INTENT_EVIDENCE_PRESENT requires distinct obligation concepts plus judged diagnostic competition attributable to them. Broad footprint alone is insufficient. QUERY_DILUTION / MIXED_INTENT is a contributor, not a runtime or top-level failure enum.",
}


def source() -> tuple[str, dict[str, Any]]:
    """Require exact pre-content author bytes, without newline normalization."""
    for name, expected in AUTHOR_HASHES.items():
        if digest((CASE / name).read_bytes()) != expected:
            raise ValueError("Pre-content authoring changed: " + name)
    return (CASE / "task.txt").read_bytes().decode("utf-8"), read_json(
        CASE / "authoring.json"
    )


def basis(text: str, numbers: list[int]) -> list[dict[str, Any]]:
    """Project explicitly authored line references into exact task spans."""
    lines = text.splitlines(keepends=True)
    output = []
    for number in numbers:
        if not 1 <= number <= len(lines):
            raise ValueError("Invalid authored task line")
        start = sum(len(s) for s in lines[: number - 1])
        output.append(
            {
                "line": number,
                "start": start,
                "end": start + len(lines[number - 1]),
                "text": lines[number - 1],
                "origin": "VERBATIM_TASK",
            }
        )
    return output


def definition() -> tuple[
    dict[str, Any], LocalizationTaskInterpretation, tuple[ObligationLexicalQuery, ...]
]:
    """Retain manual inputs and native identities; analyze only literal query text."""
    text, authored = source()
    tid = LocalizationTaskIdentity(authored["task_identity"])
    hints: list[dict[str, Any]] = []
    anchors = []
    for name in ("ModelRequest", "ContextDisclosure", "DisclosurePlan"):
        positions: list[dict[str, Any]] = []
        start = 0
        while (position := text.find(name, start)) >= 0:
            positions.append(
                {"start": position, "end": position + len(name), "text": name}
            )
            start = position + len(name)
        if not positions:
            raise ValueError("Manually declared hint not in task")
        hint = {
            "hint": name,
            "locations": positions,
            "interpretation": "literal symbol named in task; no repository resolution",
            "exact_hint_routed": False,
            "action": "NOT_ROUTED_IN_U1",
            "reason": "U1_CONTROLLED_LEXICAL_ONLY",
        }
        hints.append(hint)
        anchors.append(
            LocalizationAnchor(
                LocalizationAnchorIdentity(tid, name),
                name,
                TaskProvenance(
                    "task.txt",
                    TaskTextSpan(positions[0]["start"], positions[0]["end"]),
                    "literal caller task hint",
                ),
            )
        )
    native_obligations = []
    b_queries = []
    obligations = []
    needs = []
    queries: list[dict[str, Any]] = []

    def query(
        arm: str, key: str, ob: str | None, need: str | None, literal: str
    ) -> None:
        terms = analyze_repository_text_lexical_query(text=literal).normalized_terms
        queries.append(
            {
                "identity": key,
                "arm": arm,
                "obligation": ob,
                "information_need": need,
                "text": literal,
                "analyzed_terms": list(terms),
                "origin": "MANUAL_LITERAL" if arm != "A" else "VERBATIM_TASK",
                "route": {
                    "mechanism": ROUTE,
                    "reason": "U1_CONTROLLED_LEXICAL_ONLY",
                    "exact_hint_routed": False,
                    "exact_hints_detected": [
                        h["hint"] for h in hints if h["hint"] in literal
                    ],
                },
                "execution_status": "NOT_EXECUTED",
            }
        )

    query("A", "A.task", None, None, text)
    for ob in authored["obligations"]:
        identity = LocalizationObligationIdentity(tid, ob["id"])
        spans = basis(text, ob["task_lines"])
        provenance = TaskProvenance(
            "task.txt",
            TaskTextSpan(spans[0]["start"], spans[-1]["end"]),
            "Manual interpretation of listed verbatim task statements",
        )
        anchor_names = sorted({h for n in ob["needs"] for h in n["hints"]})
        native_obligations.append(
            LocalizationObligation(
                identity,
                ob["statement"],
                tuple(LocalizationAnchorIdentity(tid, h) for h in anchor_names),
                provenance,
                RequirementStatus.MANDATORY,
                SatisfactionCriterion(ob["id"] + "-information", ob["criterion"]),
                (),
                None,
            )
        )
        obligations.append(
            {
                "identity": ob["id"],
                "predicate": ob["statement"],
                "criterion": {
                    "name": ob["id"] + "-information",
                    "statement": ob["criterion"],
                },
                "requirement": "mandatory",
                "applicability_condition": None,
                "provenance": "manual interpretation before source inspection",
                "author": authored["author"],
                "task_basis": spans,
            }
        )
        b = ObligationLexicalQuery(
            LocalizationQueryIdentity(tid, "B." + ob["id"]), identity, ob["query"]
        )
        b_queries.append(b)
        query("B", b.identity.value, ob["id"], None, b.text)
        for row in ob["needs"]:
            n = InformationNeed(
                row["id"],
                identity,
                row["statement"],
                row["reason"],
                provenance,
                tuple(LocalizationAnchorIdentity(tid, h) for h in row["hints"]),
            )
            needs.append(
                {
                    "identity": n.identity,
                    "obligation": ob["id"],
                    "statement": n.statement,
                    "reason": n.reason,
                    "task_basis": basis(text, row["task_lines"]),
                    "anchors": row["hints"],
                    "author": authored["author"],
                    "provenance": "manual from task/obligation/criterion only; before source inspection",
                }
            )
            query(
                "C",
                "C." + ob["id"] + "." + row["id"],
                ob["id"],
                n.identity,
                row["query"],
            )
    treatment = {
        "schema": "case-0011-u1-treatment-v1",
        "task": text,
        "task_identity": tid.value,
        "task_sha256": digest(text.encode()),
        "authoring_sha256": AUTHOR_HASHES,
        "obligations": obligations,
        "information_needs": needs,
        "queries": queries,
        "literal_query_sha256": {
            q["identity"]: digest(q["text"].encode()) for q in queries
        },
        "hints": hints,
        "parameters": [1.2, 0.75, 0.25],
        "analyzer": "canonical",
        "route": ROUTE,
        "tie_order": "descending positive score; stable frozen corpus order",
        "fusion": "NONE",
        "primary_failure_class": "INFORMATION_NEED_OBLIGATION_FAILURE",
        "secondary_failure_class": "RANKING_DISCRIMINATION_FAILURE",
        "decision_rule": DECISION,
        "execution": "each frozen query once; no retries or reformulation",
        "effectiveness": "UNKNOWN",
    }
    validate(treatment)
    return (
        treatment,
        LocalizationTaskInterpretation(
            tid, TaskProvenance("task.txt"), tuple(anchors), tuple(native_obligations)
        ),
        tuple(b_queries),
    )
