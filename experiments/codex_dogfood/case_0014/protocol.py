# Copyright (c) 2026
# ruff: noqa: E501, COM812 -- exact prospective protocol prose
"""Rank-free prospective design, task clauses and query provenance."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from devtools.context.localization.identity import (
    LocalizationObligationIdentity,
    LocalizationQueryIdentity,
    LocalizationTaskIdentity,
    TaskProvenance,
    TaskTextSpan,
)
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
)
from experiments.codex_dogfood.case_0009.artifacts import binary, digest
from experiments.query_term_weighting.classification import (
    GENERIC_LEXICON,
    LEXICON_RATIONALE,
    AnchorCopy,
    Arm,
    QueryPolicy,
    classify,
)

CASE = Path(__file__).resolve().parent
START = "3aafd897a6a46a201180dc51dbef5e5201669a58"
TASK_ID = LocalizationTaskIdentity("case-0014-command-result-diagnostics-v1")
SPEC = (
    (
        "O1",
        "Completed-result contract and pure rendering",
        "implement Command CommandResult exit_code duration succeeded failed structured executable arguments nonzero completed result pure operation",
        ("Command", "CommandResult", "exit_code", "duration", "succeeded", "failed"),
    ),
    (
        "O2",
        "Byte-preserving UTF-8 diagnostic decoding",
        "implement stdout stderr UTF-8 diagnostic excerpts original bytes replacement decoding invalid incomplete loss",
        ("stdout", "stderr"),
    ),
    (
        "O3",
        "Display bounds versus retention bounds",
        "add CommandOutputPolicy stdout_truncated stderr_truncated nonnegative per-stream character display limit leading prefix byte retention zero omitted output",
        ("CommandOutputPolicy", "stdout_truncated", "stderr_truncated"),
    ),
    (
        "O4",
        "Event loss and execution-failure boundary",
        "implement events_dropped CommandResult output truncation event interleaving timeout cancellation executable-not-found completed result",
        ("events_dropped", "CommandResult"),
    ),
    (
        "O5",
        "Public API and domain boundary",
        "create src/devtools/resources/commands/__init__.py public API deterministic immutable presentation decoding display policy logging Evidence Trace subprocess persistence secret redaction",
        ("src/devtools/resources/commands/__init__.py",),
    ),
    (
        "O6",
        "Controlled tests, documentation and protected validation",
        "update tests/resources/commands/ src/devtools/resources/commands/docs/ docs/development/validation.md controlled tests success nonzero UTF-8 invalid incomplete zero default custom bounds flags event loss immutability protected validation",
        (
            "tests/resources/commands/",
            "src/devtools/resources/commands/docs/",
            "docs/development/validation.md",
        ),
    ),
)
HYPOTHESIS = "Deterministic task-side term importance can improve necessary-evidence ranking discrimination while query text, analyzed identities, native representation/statistics, positive candidates and fallback remain unchanged. More weighting is not presumed better."
SCORER: dict[str, Any] = {
    "analysis": "Unicode regex \\w+ spans, casefold; distinct normalized terms in first encounter order; duplicate observations retained but query term frequency does not score",
    "idf": "ln(1 + (N - df + 0.5)/(df + 0.5))",
    "term_contribution": "idf * tf * (k1+1) / (tf + k1*(1-b+b*document_length/average_document_length)); tf is document frequency of the term within one document",
    "k1": 1.2,
    "b": 0.75,
    "filename": "Independent native filename-stem BM25 statistics/contributions; fixed additive weight 0.25; inseparable canonical baseline contract, not BM25F",
    "equation": "sum(native_content_term * query_multiplier) + 0.25 * sum(native_filename_term * query_multiplier)",
    "arithmetic": "Python float with native channel summation order; no regrouping; retain raw native evidence and float.hex values for lossless reconstruction",
    "tie_break": "Original native document collection position after descending treatment score, not previous rank",
    "candidate_bound": "Full universe: maximum_results >= frozen document count; all positive content OR filename matches",
    "canonical_sources": [
        "src/devtools/context/retrieval/lexical/analysis.py",
        "src/devtools/context/retrieval/lexical/bm25.py",
        "src/devtools/context/retrieval/lexical/filename.py",
        "src/devtools/context/retrieval/lexical/scoring.py",
        "src/devtools/context/retrieval/lexical/statistics.py",
        "src/devtools/context/retrieval/lexical/index.py",
    ],
}
DECISION_RULE = {
    "primary": "C versus A only; B versus A evaluated separately for attribution, C versus B diagnostic; never pick the better arm after results",
    "precedence": [
        "contract defect => EXPERIMENTAL_CONTRACT_DEFECT",
        "classification/application or REQUIRED reach defect => QUERY_TERM_WEIGHTING_DEFECT",
        "meaningful witness gain AND no selected-depth or REQUIRED-cell rank regression AND >=10% unique-resource OR occurrence reduction AND neither resources, occurrences nor bytes increase => QUERY_TERM_WEIGHTING_SUPPORTED",
        "meaningful witness gain OR meaningful REQUIRED-cell rank gain, with bounded regressions => COMPLEMENTARY_QUERY_WEIGHTING_VALUE",
        "unbounded regression or completion loss => QUERY_TERM_WEIGHTING_HARMFUL",
        "otherwise => NO_MATERIAL_VALUE",
    ],
    "meaningful_witness": "A incomplete and treatment complete OR A_depth > 0 AND 5*T_depth <= 4*A_depth",
    "meaningful_required_rank": "At least two positions improvement AND 5*T_rank <= 4*A_rank",
    "strong_no_regression": "No regression at all in any baseline-complete mandatory selected witness depth or any baseline-reached REQUIRED cell rank",
    "complementary_bounds": "Every baseline-complete obligation stays complete; each selected-depth regression <=20% AND <=5 positions; each REQUIRED-cell rank regression <=20% AND <=10 positions: 5*T <= 6*A; equality alone is not value",
    "burden": "Positive baseline AND 10*T <= 9*A for chosen unique resources OR repeated occurrences; resources, occurrences and bytes each <= baseline for strong support",
    "unreached": "No REQUIRED reach loss. Unreached baseline ranks are not fabricated; rescue only if future validated completion/reach records establish it",
    "implementation": "experiments/query_term_weighting/gates.py",
    "contract_checks": [
        "Exact committed ancestry and frame/query identities",
        "Unchanged task and complete mandatory obligation coverage",
        "Full canonical contribution capture with unchanged settings/representation/statistics",
        "Identical candidate set, native contribution recoverability and unchanged reference lane",
        "Task/query-only pre-execution classifications and frozen multipliers",
        "Exactly-once capture and cost disclosure",
        "Valid complete treatment-blind primary gold, no unresolved required interpretation and exact content/frame joins",
    ],
    "application_checks": [
        "Every role reconstructs from task/query spans and frozen lexicon",
        "Every term/channel contribution equals unchanged native contribution times frozen positive multiplier",
        "Native tie semantics preserved",
        "No REQUIRED resource/cell/semantic-unit reach loss",
    ],
}
FAILURES = [
    "QUERY_TERM_CLASSIFICATION_DEFECT",
    "QUERY_WEIGHT_APPLICATION_DEFECT",
    "REQUIRED_RANKING_REGRESSION",
    "QUERY_DILUTION_NOT_REDUCED",
    "EXPLICIT_ANCHOR_OVERWEIGHT",
    "GENERIC_TERM_ATTENUATION_HARM",
    "LEXICAL_REPRESENTATION_LIMIT",
    "QUERY_AUTHORING_LIMIT",
    "EXPERIMENTAL_CONTRACT_DEFECT",
]
METRICS = [
    "REQUIRED resource reach",
    "REQUIRED cell reach",
    "required semantic-unit reach",
    "every reviewed witness completion depth",
    "selected minimum complete witness depth per mandatory obligation, then stable reviewed witness identity",
    "unique completion-prefix resources",
    "total prefix occurrences",
    "duplicate occurrences",
    "owning-obligation REQUIRED occurrences",
    "owning-obligation HELPFUL_ONLY occurrences",
    "owning-obligation UNNECESSARY occurrences",
    "distinct UTF-8 whole-resource bytes",
    "REQUIRED resource rank changes",
    "REQUIRED cell rank changes",
    "obligation-indispensable resource rank changes",
    "task-indispensable resource rank changes",
    "improved/regressed REQUIRED target counts and maximum regression",
    "term-role contribution totals and per-role score shares",
    "captured treatment execution cost",
    "top-K rank inversions at K=10,20,50",
    "per-term native versus weighted contributions",
]
GOLD_POLICY: dict[str, Any] = {
    "MODEL": "GPT-6 Astra",
    "REASONING": "High",
    "treatment_blind": True,
    "automatic_second_review": False,
    "allowed": [
        "case",
        "task_identity",
        "task_text",
        "obligations",
        "eligible_resources",
    ],
    "excluded": [
        "queries",
        "analyzed terms",
        "term roles",
        "term weights",
        "arms",
        "scores",
        "ranks",
        "results",
        "metrics",
        "decision rule",
        "prior case outcomes",
        "confirmation/reserve",
        "web",
        "repository/history access",
        "prior-session content",
    ],
    "resource_policy": "Natural original task/resource identifiers intact; complete eligible resource content; no semantic rewriting",
}
COUNTS = {
    "prospective_index_builds": 0,
    "prospective_obligation_query_executions": 0,
    "treatment_scorings": 0,
    "weighted_rankings": 0,
    "gold": "ABSENT",
}


def policies(task: str) -> tuple[QueryPolicy, ...]:
    """Bind each query to its literal original task clause without repository access."""
    result = []
    for index, (key, _title, query, literals) in enumerate(SPEC):
        start = 0 if index == 0 else task.index(key + ". ")
        end = (
            task.index(SPEC[index + 1][0] + ". ")
            if index + 1 < len(SPEC)
            else len(task)
        )
        source = TaskProvenance(
            TASK_ID,
            TaskTextSpan(start, end),
            "Exact mandatory task clause; fixed authoring, not a treatment",
        )
        anchors = []
        for literal in literals:
            task_start = task.index("`" + literal + "`", start, end) + 1
            query_start = query.index(literal)
            anchors.append(
                AnchorCopy(
                    query_start,
                    query_start + len(literal),
                    TaskProvenance(
                        TASK_ID,
                        TaskTextSpan(task_start, task_start + len(literal)),
                        "Verbatim task-marked literal",
                    ),
                )
            )
        result.append(
            classify(
                identity=LocalizationQueryIdentity(TASK_ID, "Q" + key[1:]),
                obligation=LocalizationObligationIdentity(TASK_ID, key),
                query_text=query,
                task_text=task,
                source=source,
                anchors=tuple(anchors),
            )
        )
    return tuple(result)


def authored() -> dict[str, Any]:
    """Expose the complete prospective protocol, never a retrieval result."""
    task = binary(CASE / "task.txt").decode()
    query_policies = policies(task)
    reference = analyze_repository_text_lexical_query(text=task)
    return {
        "schema": "case-0014-r17-stage-a-v1",
        "case": "0014",
        "source_head": START,
        "task_identity": TASK_ID.value,
        "task_sha256": digest(task.encode()),
        "task_text": task,
        "hypothesis": HYPOTHESIS,
        "boundary": "Only query-term contribution multipliers differ. Whole exact text, canonical tokens, query text/identities, statistics, k1/b, filename behavior, candidate membership and native tie-break are invariant. No feature implementation, expansion, reranking, routing, BM25F or sequential search.",
        "scorer_semantics": SCORER,
        "taxonomy": {
            "EXPLICIT_ANCHOR": "Native token from exact task-marked literal intentionally copied into query; anchor occurrence dominates duplicate neutral occurrences",
            "SEMANTIC": "Intentionally authored obligation-specific fact term, neutral by default",
            "GENERIC_OPERATION": "Member of the small frozen repository-independent work-verb lexicon unless anchored",
            "generic_lexicon": GENERIC_LEXICON,
            "lexicon_rationale": LEXICON_RATIONALE,
        },
        "weights": {
            "A": {"EXPLICIT_ANCHOR": 1, "SEMANTIC": 1, "GENERIC_OPERATION": 1},
            "B": {"EXPLICIT_ANCHOR": 2, "SEMANTIC": 1, "GENERIC_OPERATION": 1},
            "C": {"EXPLICIT_ANCHOR": 2, "SEMANTIC": 1, "GENERIC_OPERATION": 0.5},
        },
        "weight_rationale": "2 emphasizes a task-marked literal; 1 retains neutral semantic evidence; 0.5 challenges dilution by five generic work verbs. Positive binary-exact discrete values, not optimized, not based on corpus statistics. Three roles/arms isolate anchor emphasis from generic attenuation.",
        "arms": {a.name: a.value for a in Arm},
        "requirement_matrix": [
            {
                "requirement": key,
                "obligation": key,
                "mandatory": True,
                "title": title,
                "source_task_clause": task[p.source.span.start : p.source.span.end]
                if p.source.span
                else "",
                "query_identity": p.identity.value,
            }
            for (key, title, _q, _l), p in zip(SPEC, query_policies, strict=True)
        ],
        "queries": [asdict(p) for p in query_policies],
        "global_reference_lane": {
            "text": task,
            "analysis": asdict(reference),
            "semantics": "Whole-task canonical BM25 only; identical unchanged safety/reference lane; no treatment and no post-result rescue",
        },
        "candidate_invariants": [
            "Same exact query analysis and all terms",
            "Same native index/statistics and full positive content OR filename set",
            "No added/dropped resource",
            "Every positive contribution reconstructs native * frozen multiplier",
            "Same collection-order ties and unchanged reference lane",
            "Any violation is an experimental contract defect",
        ],
        "metrics": METRICS,
        "burden_accounting": "Compute every reviewed complete alternative independently; choose minimum depth then stable witness identity; never mix alternatives. Union chosen mandatory prefixes for unique resource/byte burden; occurrences stay repeated; labels stay owning-obligation relative; no fictional global ranking.",
        "cost_accounting": "Future single-run capture: frame/index and native full contribution acquisition shared once; charge shared acquisition equally to each arm plus its explicit multiplier/sort/trace construction top-level interval. Capture shared filename construction within native query cost. Reference lane separately, identical. Classification/publication/durability separate, excluded from mechanism cost; no child/composite double counting. No cost threshold selects ranking outcome.",
        "decision_rule": DECISION_RULE,
        "failure_taxonomy": FAILURES,
        "failure_definitions": {
            "QUERY_TERM_CLASSIFICATION_DEFECT": "Role or literal provenance cannot be reconstructed from frozen task/query-only evidence",
            "QUERY_WEIGHT_APPLICATION_DEFECT": "Contribution multiplier, channel grouping, score or tie cannot be reconstructed",
            "REQUIRED_RANKING_REGRESSION": "Positive candidate retained but necessary target/selected witness worsens; report exact rank/depth and frozen materiality bounds",
            "QUERY_DILUTION_NOT_REDUCED": "Generic attenuation does not change the contribution/overtaker pattern blocking reviewed completion",
            "EXPLICIT_ANCHOR_OVERWEIGHT": "B/C anchor contributions promote reviewed HELPFUL_ONLY or UNNECESSARY evidence ahead of necessary semantic evidence",
            "GENERIC_TERM_ATTENUATION_HARM": "C-versus-B attenuation reduces useful discrimination and worsens required ranking/completion",
            "LEXICAL_REPRESENTATION_LIMIT": "Necessary evidence has no discriminative native analyzed terms under unchanged whole-text representation",
            "QUERY_AUTHORING_LIMIT": "Frozen query does not express the necessary fact; multipliers cannot repair missing terms",
            "EXPERIMENTAL_CONTRACT_DEFECT": "Broken frame/query/candidate/statistics/blindness/execution/gold/cost contract; no effectiveness inference",
        },
        "SEARCH_POLICY_FAILURE": "NOT_ASSESSED",
        "gold_policy": GOLD_POLICY,
        "no_execution": COUNTS,
        "execution_policy": "No Stage B entry point exists at this checkpoint. Future maintainer authorization required; exactly one prospective execution, no tuning or query changes. Controlled fixtures are synthetic and separate.",
        "status": "R1.7 CURRENT / STAGE_A_FROZEN; effectiveness UNKNOWN; BM25F MANDATORY IMMEDIATELY AFTER R1.7; Localization PRESERVED",
    }
