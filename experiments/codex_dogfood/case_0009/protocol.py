# Copyright (c) 2026
# ruff: noqa: COM812, E501 -- bounded case-local JSON/CLI convention
"""Outcome-free task, caller-authored queries and precommitted R1 decision rule."""

from __future__ import annotations

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

TASK = (
    "Add a bounded caller-directed batch bridge from completely supported candidate witness hypotheses "
    "to LocalizationAssessment values. Reuse the existing explicit promotion and accepted witness contracts. "
    "The caller must select the obligations and accepted alternatives, rather than treating candidate support "
    "as automatic obligation satisfaction. Validate that every promoted resource witness and its evidence "
    "belong to the same task, obligation, repository and snapshot frame; preserve complementary members "
    "and keep competing alternatives independent. Reject incomplete support, foreign or stale provenance, "
    "duplicate assignments and attempts to silently add an unaccepted witness alternative. Preserve "
    "applicability, explicit non-applicability and named deferred discovery as separate caller decisions. "
    "Integrate the resulting assessments with existing readiness checks without mutating candidate views, "
    "resolution records or task interpretations. Keep contradiction separate from elimination. Add focused "
    "tests for complete and partial support, complementary witnesses, competing hypotheses, conditional "
    "applicability and invalid frames. Follow the public package and dependency conventions, update the "
    "governing architecture and package documentation, and run protected development validation. "
    "Do not implement automatic semantic resolution, ranking, candidate elimination, unresolved frontiers, "
    "autonomous acquisition, Context Planning admission or agent execution."
)

# Predicates/queries are ordinary task interpretation, not gold-resource hints.
OBLIGATIONS = (
    (
        "bridge",
        "Find the existing candidate resolution and explicit promotion contracts needed by the batch bridge.",
        "candidate witness hypothesis complete supported resolution promotion assessment bridge",
    ),
    (
        "alternatives",
        "Find the accepted alternative and complementary witness semantics that the bridge must preserve.",
        "accepted witness alternatives complementary members competing hypotheses supported witness",
    ),
    (
        "frame",
        "Find exact task, obligation, repository and snapshot evidence validation contracts.",
        "task obligation repository snapshot identity evidence provenance frame validation",
    ),
    (
        "applicability",
        "Find applicability, non-applicability and named deferred-discovery assessment semantics.",
        "assessment applicability non applicability deferred discovery conditional handoff",
    ),
    (
        "readiness",
        "Find how caller assessments feed readiness without changing candidate or resolution state.",
        "LocalizationAssessment readiness mandatory resolved supported witnesses invalid frame",
    ),
    (
        "package",
        "Find the public package and dependency boundaries that constrain this integration.",
        "localization public package exports dependency resolution assessment boundary",
    ),
    (
        "tests",
        "Find existing tests establishing candidate support, promotion, assessment and readiness behavior.",
        "tests resolution promotion complementary supported witness assessment readiness stale frame",
    ),
    (
        "documentation",
        "Find governing architecture and package documentation that must describe the bridge accurately.",
        "localization architecture obligation witness resolution promotion assessment documentation",
    ),
    (
        "validation",
        "Find the supported development validation contract and its scope.",
        "protected development validation branch coverage experiment exclusion ruff mypy",
    ),
)


def task_inputs() -> tuple[
    LocalizationTaskInterpretation, tuple[ObligationLexicalQuery, ...]
]:
    """Construct canonical caller task/query values, never accepted gold witnesses."""
    identity = LocalizationTaskIdentity("case-0009-explicit-assessment-bridge")
    provenance = TaskProvenance("case-0009-frozen-development-task")
    anchor_id = LocalizationAnchorIdentity(identity, "assessment-bridge")
    anchors = (
        LocalizationAnchor(
            anchor_id, "explicit supported witness assessment bridge", provenance
        ),
    )
    obligations = tuple(
        LocalizationObligation(
            LocalizationObligationIdentity(identity, key),
            predicate,
            (anchor_id,),
            provenance,
            RequirementStatus.MANDATORY,
            SatisfactionCriterion(key + "-information", predicate),
            (),
            None,
        )
        for key, predicate, _ in OBLIGATIONS
    )
    queries = tuple(
        ObligationLexicalQuery(
            LocalizationQueryIdentity(identity, key + "-query"),
            obligation.identity,
            query,
        )
        for obligation, (key, _, query) in zip(obligations, OBLIGATIONS, strict=True)
    )
    return LocalizationTaskInterpretation(
        identity, provenance, anchors, obligations
    ), queries


def treatment() -> dict[str, object]:
    """Freeze hypotheses and outcomes before any prospective query execution."""
    return {
        "schema": "case-0009-r1-treatment-v1",
        "task": TASK,
        "full_task_query": TASK,
        "obligations": [
            {
                "id": key,
                "predicate": predicate,
                "query": query,
                "requirement": "MANDATORY",
                "applicability_condition": None,
                "accepted_alternatives": [],
            }
            for key, predicate, query in OBLIGATIONS
        ],
        "case_selection": "New caller-directed assessment integration task drawn from existing public contracts; no gold resources selected. Not a tokenizer task. Task family overlaps prior Localization work; not independent-repository evidence.",
        "primary_failure_class": "REPRESENTATION_FAILURE",
        "secondary_failure_class": "RANKING_DISCRIMINATION_FAILURE",
        "arms": {
            "A": "Exact production content BM25 + 0.25 canonical filename-stem BM25",
            "B": "Same whole resources and BM25 arithmetic; whole identifiers + unique subtokens for content, filename stems and queries",
        },
        "settings": {
            "k1": 1.2,
            "b": 0.75,
            "filename_weight": 0.25,
            "maximum_results": "entire eligible resource frame",
            "ties": "native corpus order",
        },
        "metrics": [
            "required resource/cell positive reach and misses",
            "global task-complete depth",
            "own-obligation best-alternative completion and maximum depth",
            "completion-prefix occurrences and union",
            "excess above minimum sufficient union",
            "required rank gain/loss/ties and paired net change",
            "usefulness at K=1,3,5,10,20,50",
            "A-only/B-only useful reach",
            "canonical misses rescued and losses",
            "exact content/filename/query term attribution",
            "index build/query timing and traced peak bytes",
            "vocabulary/postings and serialized index size",
        ],
        "decision_rule": {
            "precedence": [
                "scientific validity",
                "concrete analyzer defect",
                "promotion candidate",
                "complementary view",
                "park",
            ],
            "invalid": "Any gold gap, unresolved required applicability/alternative, incomplete join or integrity failure prevents a promotion/park effectiveness conclusion; report bounded results and obtain valid adjudication.",
            "defect": "Investigate only a demonstrated violation of the frozen analyzer/scoring contract, not an unwanted outcome. Corrected treatment requires a new prospective case.",
            "promotion_candidate": "Zero A-positive required cells lost; B completion no worse for every obligation and global lane; at least 20% reduction in own completion-prefix unique union or at least one independently verified required representation rescue; B median query time and total index+query time <=3x A, serialized index and traced peak <=3x A. Even then no production replacement here; one case is insufficient for default adoption.",
            "separate_view": "At least one verified required positive-reach rescue or required top-20 entry gain; at least one obligation completion improves; promotion conditions not met. Retain as complementary experimental view, not default fusion.",
            "park": "With complete valid gold, neither condition is met. Report all paired gains/losses and costs; no parameter/splitter tuning on outcomes.",
        },
        "representation_attribution": "A rank gain alone is not a recovery. Cite exact canonical/R1 query and content/filename spans; distinguish positive reach rescue from length/DF-induced reranking. Inspect regressions too.",
        "recovery": "One Stage B execution only. Failure leaves an exclusive execution-start marker; no retry without a separately recorded authorization and unchanged treatment. Tests/replay checks are not additional prospective treatment runs.",
        "execution_authorization": "Current user task authorizes one post-freeze A/B execution and blind packet. No blind effectiveness judgments, model invocation, structural arms, fusion or production replacement.",
        "R2": "True BM25F / field-aware sparse retrieval proceeds regardless of whether R1 improves, ties or worsens canonical BM25.",
    }
