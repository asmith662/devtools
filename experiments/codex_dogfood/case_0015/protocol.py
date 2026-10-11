# Copyright (c) 2026
# ruff: noqa: COM812, E501 -- exact prospective scientific prose
"""Prospective two-arm document-field experiment; query analysis only at freeze."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from devtools.context.localization.identity import (
    LocalizationObligationIdentity,
    LocalizationQueryIdentity,
    LocalizationTaskIdentity,
)
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
)
from experiments.bm25f.scoring import Parameters
from experiments.codex_dogfood.case_0009.artifacts import binary, digest

CASE = Path(__file__).resolve().parent
START = "53a1d087a24e7880f305e167e2d5f3bbb727ff61"
TASK_ID = LocalizationTaskIdentity("case-0015-strict-bounded-filesystem-read-v1")
SPEC = (
    (
        "O1",
        "Compatible bounded read contract",
        "reading.py read read_bytes ResolvedPath file_format max_bytes DEFAULT_MAX_READ_BYTES finite unbounded negative zero exact byte boundary growing file",
        "Identify current signature, default, limit semantics and allocation-before-rejection behavior; locate the owning implementation.",
    ),
    (
        "O2",
        "Acquisition bound and lifecycle",
        "filesystem bounded chunk acquisition payload bytes EOF FileTooLargeError stream closure memory stat snapshot containment authorization locking",
        "Establish precise max_bytes plus one sentinel acquisition, bounded requests, closure and distinction from model memory/security/snapshot guarantees.",
    ),
    (
        "O3",
        "Codec and rich-model fidelity",
        "resolve_file_format resolve_codec TextFile MarkdownFile CsvFile JsonObjectFile JsonListFile JsonScalarFile UTF-8 decoding encoding byte_size line endings TextDecodingError",
        "Identify complete-byte codec contracts, format override/inference, concrete models, metadata and strict decoding behavior.",
    ),
    (
        "O4",
        "Error and ownership boundaries",
        "filesystem reading FilesystemNotFoundError NotAFileError FilesystemPermissionError FileTooLargeError FileFormatError permission stream opening chunk read write atomic paths Tool authorization",
        "Establish existing error normalization, causal exceptions and package/atomic-write/path/authorization boundaries.",
    ),
    (
        "O5",
        "Controlled regression tests",
        "tests/resources/filesystem/test_reading.py codecs models empty zero exact over-limit negative unbounded growth stat short reads EOF closure permission multibyte UTF-8 invalid format override",
        "Find current read/codec/model test patterns and evidence needed for deterministic instrumented-stream tests of bounds and compatibility.",
    ),
    (
        "O6",
        "Documentation and protected validation",
        "src/devtools/resources/filesystem/docs/io.md overview roadmap public API docs/development/validation.md scripts/validate_development.py pyproject.toml protected validation Ruff formatting mypy binary formats streaming security",
        "Identify authoritative behavior documentation, deferred scope and protected validation policy/configuration without changing exclusions or coverage.",
    ),
)
SCORER: dict[str, Any] = {
    "analysis": "Query and both fields: canonical Unicode regex \\w+ spans, casefold. Underscores remain inside words; no identifier splitting, stemming or stopwords. Query duplicates retained as observations; distinct terms score once in first encounter order.",
    "CONTENT": "RepositoryTextDocument.text: exact decoded whole-resource UTF-8 text, not a window or AST view.",
    "FILENAME": "PurePosixPath(resource.address.value).stem: final basename without final suffix; no directories, extension field or full path. Canonical iter_lexical_spans on that stem.",
    "length": "Each field length is its own observation count. Each average is total field length divided by N including zero-length field documents; empty corpus average 0.",
    "df": "Independent field df counts documents with at least one field occurrence; N is all eligible resource documents in both fields.",
    "idf": "Each field independently: ln(1 + (N - df_field + 0.5)/(df_field + 0.5)).",
    "term": "idf_field * tf_field * (k1+1) / (tf_field + k1*(1-b+b*length_field/average_field_length))",
    "score": "sum(content term contributions in distinct query encounter order) + 0.25 * sum(filename term contributions in distinct query encounter order)",
    "k1": 1.2,
    "b_content": 0.75,
    "b_filename": 0.75,
    "filename_coefficient": 0.25,
    "candidate": "Positive native content OR filename term matches; full maximum_results >= N. With positive IDF/settings these are exactly positive-score resources.",
    "ties": "Descending score, then original native document collection position; full candidate enumeration before result bound.",
    "provenance": "Native result retains query observations, content statistics/index, independent filename index, both channel scores and every contributing term tf, df, idf, length, average and score.",
    "not_bm25f": "Independent field IDFs and independent saturations precede additive channel combination. True BM25F requires combined normalized tf before one saturation and one union IDF.",
    "canonical_sources": [
        f"src/devtools/context/retrieval/lexical/{name}.py"
        for name in ("analysis", "bm25", "filename", "scoring", "statistics", "index")
    ],
}
FORMULA = {
    "normalized_tf": "tf_f / (1 - b_f + b_f * field_length_f / average_field_length_f)",
    "combined_tf": "sum(field_weight_f * normalized_tf_f) in CONTENT then FILENAME order",
    "df_union": "Count each eligible resource document once if t occurs in CONTENT OR FILENAME; never twice.",
    "idf_union": "ln(1 + (N - df_union + 0.5)/(df_union + 0.5)) using canonical calculate_bm25_inverse_document_frequency",
    "term_score": "idf_union * ((k1+1)*combined_tf) / (k1+combined_tf)",
    "document_score": "sum term_score in distinct canonical query encounter order; every query multiplier = 1.0",
    "empty_field": "If tf=0 normalized tf=0. If average=0 all field lengths/tfs must be zero: disclosed denominator=1 convention with zero contribution. No division by zero. Zero-length document in nonempty field may have denominator=0 when synthetic b=1, but tf=0 still contributes zero.",
    "arithmetic": "Python float, fixed grouping and field/query order; every floating input/intermediate/output serialized as float.hex; do not regroup native A channels.",
    "invariants": [
        "ONE aggregated tf",
        "ONE union IDF",
        "ONE saturation per term/document",
        "Only CONTENT and FILENAME",
        "Exact native tokens",
        "Identical A/B positive candidates",
        "Canonical collection-order ties",
    ],
}
COUNTS = dict.fromkeys(
    (
        "prospective_frame_retrieval_executions",
        "prospective_index_builds",
        "prospective_obligation_queries",
        "prospective_reference_queries",
        "prospective_bm25f_scorings",
        "prospective_treatment_rankings",
    ),
    0,
)
COUNTS["gold"] = "ABSENT"  # type: ignore[assignment]
FAILURES = {
    "BM25F_FIELD_DEFINITION_DEFECT": "Admitted text/lengths differ from sealed canonical representations.",
    "BM25F_DF_DEFECT": "Union document frequency incorrect or double-counts a document.",
    "BM25F_NORMALIZATION_DEFECT": "Per-field normalization cannot reconstruct from exact observations/averages/b.",
    "BM25F_AGGREGATION_DEFECT": "Evidence is not aggregated before a single saturation.",
    "BM25F_APPLICATION_DEFECT": "Term/document score, tie or lossless provenance does not reconstruct.",
    "REQUIRED_RANKING_REGRESSION": "Baseline-reached necessary cell or selected completion worsens; exact magnitude and bounds retained.",
    "FILENAME_FIELD_OVERWEIGHT": "Filename influence promotes non-required overtakers with proven necessary-evidence consequence, not mere upward movement.",
    "CONTENT_FIELD_DOMINANCE": "Content influence leaves necessary filename evidence behind with captured contribution/overtaker proof.",
    "CROSS_FIELD_SATURATION_HARM": "Fixed-order single-saturation delta contributes to necessary-rank/completion harm; signed score movement alone is insufficient.",
    "UNION_IDF_HARM": "Fixed-order union-IDF delta contributes to necessary-rank/completion harm, with exact overtaker evidence.",
    "FIELD_REPRESENTATION_LIMIT": "Unchanged existing fields cannot represent/discriminate necessary fact; no structural/graph claim.",
    "QUERY_AUTHORING_LIMIT": "Necessary fact omitted from frozen query; cannot be repaired by field scoring.",
    "EXPERIMENTAL_CONTRACT_DEFECT": "Identity/query/token/candidate/blindness/execution/authoritative gold/reference contract broken; no effectiveness inference.",
}
DECISION_RULE = {
    "primary": "B true BM25F versus A canonical additive only; never select an explanatory counterfactual as an arm",
    "implementation": "experiments/bm25f/gates.py",
    "meaningful_witness": "A incomplete and B complete OR A_depth > 0 AND 5*B_depth <= 4*A_depth",
    "meaningful_required_rank": "A and B reached; A_rank - B_rank >= 2 AND 5*B_rank <= 4*A_rank",
    "strong_safety": "No selected mandatory baseline-complete witness depth regression, no baseline-reached REQUIRED-cell rank regression, no REQUIRED resource/cell/repository-supported-unit reach loss.",
    "strong_burden": "Positive baseline and (10*B_unique <= 9*A_unique OR 10*B_occurrences <= 9*A_occurrences), with B_unique <= A_unique AND B_occurrences <= A_occurrences AND B_bytes <= A_bytes.",
    "complementary_bounds": "All baseline-complete obligations remain complete; every reached REQUIRED cell retained. Each depth: 5*B <= 6*A AND B-A <= 5. Each REQUIRED rank: 5*B <= 6*A AND B-A <= 10.",
    "zero_depth": "Fully task-backed complete witness depth=0 allowed; 0->0 not meaningful; incomplete represented None, never fabricated rank.",
    "precedence": [
        "Contract defect => EXPERIMENTAL_CONTRACT_DEFECT",
        "Field/DF/normalization/aggregation/application defect or REQUIRED reach loss => BM25F_IMPLEMENTATION_DEFECT",
        "Meaningful witness gain AND strong safety AND strong burden => TRUE_BM25F_SUPPORTED",
        "Meaningful witness gain OR meaningful REQUIRED rank gain, WITH all complementary bounds => COMPLEMENTARY_BM25F_VALUE",
        "Completion loss or unbounded REQUIRED regression => BM25F_HARMFUL",
        "Otherwise => NO_MATERIAL_VALUE",
    ],
    "contract_checks": [
        "Exact source ancestry and frame/content/document joins",
        "Same task/obligations/queries/analysis/field representations",
        "Identical full positive A/B candidates",
        "Unchanged canonical reference lane",
        "Exactly-once prospective execution with no tuning",
        "Complete clean treatment-blind primary gold and no unresolved cells",
        "Lossless replay and captured cost",
    ],
    "implementation_checks": [
        "Canonical field observations and lengths",
        "Correct union df/N/IDF",
        "Exact per-field normalization",
        "Aggregation before one saturation",
        "Deterministic contributions/doc score/ties",
        "REQUIRED resource/cell/repository-unit reach safety",
    ],
}
METRICS = [
    "REQUIRED resource reach",
    "REQUIRED cell reach",
    "required semantic-unit reach",
    "every reviewed witness completion depth",
    "selected minimum witness depth per obligation, then stable witness identity",
    "obligation completeness",
    "obligation-indispensable resource ranks",
    "task-indispensable resource ranks",
    "every REQUIRED-cell rank",
    "meaningful REQUIRED-cell improvements",
    "REQUIRED-cell regressions",
    "unique completion-prefix resources",
    "repeated prefix occurrences",
    "duplicate occurrences",
    "owning-obligation REQUIRED occurrences",
    "owning-obligation HELPFUL_ONLY occurrences",
    "owning-obligation UNNECESSARY occurrences",
    "distinct exact UTF-8 whole-resource bytes",
    "treatment execution cost",
    "diagnostic top-K inversions K=10,20,50 gold-labeled after gold",
    "per-field contribution effects",
    "union-IDF deltas",
    "pre-saturation weighting and single-saturation deltas",
]
GOLD_POLICY = {
    "MODEL": "GPT-6 Astra",
    "REASONING": "High",
    "treatment_blind": True,
    "automatic_second_reviewer": False,
    "allowed": [
        "case",
        "task_identity",
        "task_text",
        "obligations",
        "eligible_resources",
    ],
    "excluded": [
        "queries",
        "analyzed query terms",
        "BM25F field definitions as experiment metadata",
        "field weights",
        "b values",
        "BM25F formula",
        "arms",
        "rankings",
        "scores",
        "field contributions",
        "df values",
        "IDF values",
        "candidate results",
        "metrics",
        "gates",
        "costs",
        "outcome",
        "prior gold",
        "confirmation/reserve",
        "repository checkout/history",
        "web",
        "prior Codex-session content",
    ],
    "resource_text": "Original natural task/resource text unchanged; exclusion removes metadata, never edits source text.",
    "review": "One clean primary semantic adjudication; no automatic second reviewer or reconciliation. Full cell matrix, task/repository semantic units, support alternatives/spans, complete minimal witnesses, task combinations, indispensability, gaps/limitations/design freedom. Clean blindness attestation required before publication.",
}


def authored() -> dict[str, Any]:
    """Materialize exact task obligations and queries without any document analysis."""
    task = binary(CASE / "task.txt").decode()
    matrix = []
    queries = []
    for i, (key, title, text, satisfaction) in enumerate(SPEC):
        start = task.index(key + ". ")
        end = task.index(SPEC[i + 1][0] + ". ") if i + 1 < len(SPEC) else len(task)
        obligation = LocalizationObligationIdentity(TASK_ID, key)
        query_id = LocalizationQueryIdentity(TASK_ID, "Q" + key[1:])
        matrix.append(
            {
                "requirement": key,
                "identity": asdict(obligation),
                "title": title,
                "mandatory": True,
                "applicability": "APPLICABLE",
                "task_span": {"start": start, "end": end},
                "task_clause": task[start:end],
                "satisfaction": satisfaction,
                "query_identity": asdict(query_id),
            }
        )
        native = analyze_repository_text_lexical_query(text=text)
        queries.append(
            {
                "identity": asdict(query_id),
                "obligation": asdict(obligation),
                "text": text,
                "analysis": asdict(native),
                "normalized_terms": native.normalized_terms,
                "all_term_multipliers": 1.0,
                "authoring": "One query authored from this task clause before any prospective document statistics/rank; identical for both arms; no reformulation.",
            }
        )
    return {
        "schema": "case-0015-r2-stage-a-v1",
        "case": "0015",
        "source_head": START,
        "task_identity": TASK_ID.value,
        "task_text": task,
        "task_sha256": digest(task.encode()),
        "hypothesis": "Given the same query, query analysis, positive candidate universe and existing CONTENT/FILENAME representations, true BM25F field combination improves task-relative necessary-evidence ranking compared with independent content BM25 plus 0.25 filename BM25. Improvement is unknown and not presumed.",
        "primary_failure_class": "RANKING_DISCRIMINATION_FAILURE through document-side field combination; representation is held fixed",
        "boundary": "Only document-field combination architecture changes. No query weights, identifiers/subtokens, path/symbol/AST/graph fields, expansion, reranking, fusion, routing, reformulation, sequential search, software feature or production implementation.",
        "scorer_semantics": SCORER,
        "bm25f_formula": FORMULA,
        "parameters": asdict(Parameters()),
        "parameter_rationale": "Retain native k1=1.2, both b=0.75 and content:filename prior 1:0.25; no semantic incompatibility found. Values fixed before prospective statistics/execution; no grid search or task-specific tuning.",
        "arms": {
            "A": "CANONICAL_ADDITIVE_BM25: exact production retrieve_repository_text_documents_by_bm25, defaults and full bound",
            "B": "TRUE_BM25F: canonical field observations; per-field normalized tf, positive field weights, one union IDF and one saturation",
        },
        "requirement_matrix": matrix,
        "queries": queries,
        "global_reference_lane": {
            "text": task,
            "analysis": asdict(analyze_repository_text_lexical_query(text=task)),
            "semantics": "Whole-task canonical additive BM25 unchanged, separate safety lane, never rescue; future execute once with same frame.",
        },
        "candidate_invariants": [
            "Same eligible resource/document/content universe",
            "Same normalized queries and exact field tokens",
            "Full positive CONTENT OR FILENAME union independently observed in A and B",
            "No candidates added/lost; mismatch contract defect, no post-hoc union repair",
            "Canonical collection-order tie semantics",
            "Query multipliers all 1.0",
        ],
        "metrics": METRICS,
        "burden_accounting": "Calculate every reviewed witness independently; TASK_BACKED units have no retrieval rank; honor encoded repository support choices, never mix witnesses. Choose minimum complete depth then stable reviewed identity; incomplete None. Union selected owning-obligation prefixes for unique resources and exact UTF-8 bytes, retain repeated occurrences and own obligation-relative labels. No task-global ranking.",
        "cost_accounting": "Future exactly-once run: shared frame/content index/field observation acquisition charged equally to A/B once. Native A retrieval (including its native filename construction) and B union statistics/scoring/sort/trace timed separately at top-level. Whole-task reference cost separate and unchanged. Disclosure includes setup, scoring, memory/index size where observed; publication/durability/wall/child timers descriptive and never double-counted. No cost threshold chooses effectiveness.",
        "diagnostic_attribution": "Fixed per-term telescoping: replace independent field IDFs with union IDF, move positive filename weight inside otherwise independent saturation, then combine into one saturation. Retain native channel grouping residual. Field normalization inputs identical to A; trace exact lengths/averages. Counterfactual calculations are unranked explanations, not additional arms; harmful causes require necessary-evidence/overtaker consequences, allow ambiguity and interacting causes.",
        "decision_rule": DECISION_RULE,
        "failure_definitions": FAILURES,
        "SEARCH_POLICY_FAILURE": "NOT_ASSESSED",
        "gold_policy": GOLD_POLICY,
        "no_execution": COUNTS,
        "execution_policy": "No Stage B entry point at this checkpoint. Maintainer reviews frozen Stage A; only after authorization execute A/B and reference prospectively exactly once. Synthetic controlled fixtures are segregated and cannot use the prospective frame.",
        "status": "R2 CURRENT / STAGE_A_FROZEN; effectiveness NOT_EVALUATED; production UNCHANGED; confirmation/reserve NOT_ACCESSED",
    }
