# Copyright (c) 2026
# ruff: noqa: E501, PLR0913
"""Frozen Increment-23 validation design, with no retrieval or admission work.

This is immutable experiment configuration.  It does not construct a corpus,
rank resources, derive relations, qualify supports, or apply the Increment-22
rule.  Its judgments are evaluation inputs rather than mechanism inputs.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import StrEnum

from devtools.context.repository.resource import RepositoryResourceAddress
from experiments.import_relationship_cases import ImportRelationshipDirection
from experiments.purpose_relative_admission.design import PurposeProfile
from experiments.purpose_relative_import.cases import (
    ResourceJudgment,
    UsefulnessJudgment,
)

INCREMENT_22_RULE_FINGERPRINT = (
    "7e215ac2961a4329074e9a25d35d3decc554f394435aa0b73cb2251254160345"
)


class ValidationRoute(StrEnum):
    """Keep heterogeneous admission separate from exact direct resolution."""

    HETEROGENEOUS_K5 = "heterogeneous-k5"
    DIRECT_RESOLUTION = "direct-resolution"


class AdjudicationCompleteness(StrEnum):
    """Describe how much of one case is judged before a surface exists."""

    INITIAL_JUDGMENTS_ONLY = "initial-judgments-only"


@dataclass(frozen=True, slots=True)
class RelationshipControl:
    """A true, purpose-irrelevant relation retained as an explicit control."""

    address: RepositoryResourceAddress
    relation_source: RepositoryResourceAddress
    relation_target: RepositoryResourceAddress
    direction: ImportRelationshipDirection
    relation_truth_rationale: str
    not_useful_rationale: str


@dataclass(frozen=True, slots=True)
class FrozenValidationCase:
    """One pre-surface Increment-23 heterogeneous evaluation configuration."""

    name: str
    information_need: str
    query_text: str
    profile: PurposeProfile
    route: ValidationRoute
    judgments: tuple[ResourceJudgment, ...]
    relationship_controls: tuple[RelationshipControl, ...]
    provenance_assumption: str
    adjudication_completeness: AdjudicationCompleteness
    caveat: str


@dataclass(frozen=True, slots=True)
class DirectResolutionValidationControl:
    """An exact-name control excluded from heterogeneous K=5 evaluation."""

    name: str
    information_need: str
    declared_name: str
    useful_address: RepositoryResourceAddress
    rationale: str


@dataclass(frozen=True, slots=True)
class BlindedAdjudicationProtocol:
    """Freeze the Pass-5 judgment view before any material surface is captured."""

    hidden_fields: tuple[str, ...]
    visible_fields: tuple[str, ...]
    address_handling: str
    immutability_rule: str


def _judgment(
    address: str,
    judgment: UsefulnessJudgment,
    rationale: str,
    *,
    control: bool = False,
) -> ResourceJudgment:
    return ResourceJudgment(
        RepositoryResourceAddress(address), judgment, rationale, control,
    )


def _control(
    *,
    address: str,
    relation_source: str,
    relation_target: str,
    direction: ImportRelationshipDirection,
    relation_truth_rationale: str,
    not_useful_rationale: str,
) -> RelationshipControl:
    return RelationshipControl(
        RepositoryResourceAddress(address),
        RepositoryResourceAddress(relation_source),
        RepositoryResourceAddress(relation_target),
        direction,
        relation_truth_rationale,
        not_useful_rationale,
    )


_COMMON_PROVENANCE = (
    "Pass 4 must acquire one bounded repository corpus and derive all lexical "
    "and relation evidence from its single retained snapshot."
)

_CASES = (
    FrozenValidationCase(
        "content-bm25-term-formula",
        "Identify the implementation, formula helper, and focused test needed to "
        "change content-only Okapi BM25 term scoring without changing filename-field "
        "fusion behavior.",
        "content only BM25 term formula",
        PurposeProfile.OUTGOING_DEPENDENCY,
        ValidationRoute.HETEROGENEOUS_K5,
        (
            _judgment(
                "src/devtools/context/retrieval/lexical/bm25.py",
                UsefulnessJudgment.USEFUL,
                "Owns content BM25 retrieval and invokes the term-scoring formula.",
            ),
            _judgment(
                "src/devtools/context/retrieval/lexical/scoring.py",
                UsefulnessJudgment.USEFUL,
                "Owns the reusable inverse-document-frequency and term-contribution formula helpers.",
            ),
            _judgment(
                "tests/context/retrieval/lexical/test_bm25.py",
                UsefulnessJudgment.USEFUL,
                "Provides focused content-only score and contribution behavioral evidence.",
            ),
            _judgment(
                "src/devtools/context/retrieval/lexical/filename.py",
                UsefulnessJudgment.NOT_USEFUL,
                "Owns filename-field analysis and scoring, which is outside the requested content-only formula change.",
                control=True,
            ),
        ),
        (
            _control(
                address="src/devtools/context/retrieval/lexical/filename.py",
                relation_source="src/devtools/context/retrieval/lexical/bm25.py",
                relation_target="src/devtools/context/retrieval/lexical/filename.py",
                direction=ImportRelationshipDirection.OUTGOING,
                relation_truth_rationale="bm25.py directly imports filename-field index and scoring functions at module body, producing an explicit resolved repository relation.",
                not_useful_rationale="Filename fusion is a genuine imported neighbor but does not answer the requested content-only term-formula change.",
            ),
        ),
        _COMMON_PROVENANCE,
        AdjudicationCompleteness.INITIAL_JUDGMENTS_ONLY,
        "An outgoing useful opportunity is frozen; qualification and admission are intentionally unknown.",
    ),
    FrozenValidationCase(
        "baseline-lexical-analysis-definition",
        "Identify the local implementation and focused test that define baseline "
        "lexical span extraction and collection analysis semantics.",
        "baseline lexical analysis",
        PurposeProfile.LOCAL_DEFINITION_OR_GOVERNANCE,
        ValidationRoute.HETEROGENEOUS_K5,
        (
            _judgment(
                "src/devtools/context/retrieval/lexical/analysis.py",
                UsefulnessJudgment.USEFUL,
                "Owns lexical span and document/collection analysis semantics.",
            ),
            _judgment(
                "tests/context/retrieval/lexical/test_analysis.py",
                UsefulnessJudgment.USEFUL,
                "Provides focused behavioral evidence for span and collection analysis.",
            ),
            _judgment(
                "src/devtools/context/retrieval/lexical/bm25.py",
                UsefulnessJudgment.NOT_USEFUL,
                "Consumes analysis for scoring but does not define lexical analysis semantics.",
            ),
        ),
        (),
        _COMMON_PROVENANCE,
        AdjudicationCompleteness.INITIAL_JUDGMENTS_ONLY,
        "Local-definition purpose must abstain regardless of any later relation surface.",
    ),
    FrozenValidationCase(
        "content-bm25-analysis-consumer",
        "Identify the downstream content-BM25 implementation and focused behavioral "
        "test that consume baseline lexical analysis.",
        "baseline lexical analysis",
        PurposeProfile.INCOMING_CONSUMER_OR_TEST,
        ValidationRoute.HETEROGENEOUS_K5,
        (
            _judgment(
                "src/devtools/context/retrieval/lexical/bm25.py",
                UsefulnessJudgment.USEFUL,
                "Directly consumes lexical spans while owning content BM25 retrieval behavior.",
            ),
            _judgment(
                "tests/context/retrieval/lexical/test_bm25.py",
                UsefulnessJudgment.USEFUL,
                "Provides focused content-BM25 scoring and retrieval evidence.",
            ),
            _judgment(
                "src/devtools/context/retrieval/lexical/filename.py",
                UsefulnessJudgment.NOT_USEFUL,
                "Consumes analysis for a separate filename field, not the requested content-BM25 behavior.",
                control=True,
            ),
            _judgment(
                "tests/context/retrieval/lexical/test_filename.py",
                UsefulnessJudgment.NOT_USEFUL,
                "Tests the separate filename field and is not evidence for content-BM25 behavior.",
                control=True,
            ),
        ),
        (
            _control(
                address="src/devtools/context/retrieval/lexical/filename.py",
                relation_source="src/devtools/context/retrieval/lexical/filename.py",
                relation_target="src/devtools/context/retrieval/lexical/analysis.py",
                direction=ImportRelationshipDirection.INCOMING,
                relation_truth_rationale="filename.py directly imports lexical analysis helpers, producing an incoming repository relation when analysis.py is a seed.",
                not_useful_rationale="Filename-field scoring is a genuine consumer but is outside this content-BM25 information need.",
            ),
            _control(
                address="tests/context/retrieval/lexical/test_filename.py",
                relation_source="tests/context/retrieval/lexical/test_filename.py",
                relation_target="src/devtools/context/retrieval/lexical/analysis.py",
                direction=ImportRelationshipDirection.INCOMING,
                relation_truth_rationale="test_filename.py directly imports lexical analysis helpers, producing an incoming test-module relation when analysis.py is a seed.",
                not_useful_rationale="The test is a true relationship neighbor but evaluates filename behavior rather than the requested content-BM25 consumer.",
            ),
        ),
        _COMMON_PROVENANCE,
        AdjudicationCompleteness.INITIAL_JUDGMENTS_ONLY,
        "The paired local case shares this query but freezes a different purpose and judgment set.",
    ),
    FrozenValidationCase(
        "python-function-token-candidate-boundary",
        "Identify the implementation and focused test that keep tokenizer-based Python "
        "function name candidates distinct from declaration analysis.",
        "Python function candidate selection tokenizer",
        PurposeProfile.OUTGOING_DEPENDENCY,
        ValidationRoute.HETEROGENEOUS_K5,
        (
            _judgment(
                "src/devtools/context/python/function/candidates.py",
                UsefulnessJudgment.USEFUL,
                "Owns bounded tokenizer-based pre-analysis candidate selection.",
            ),
            _judgment(
                "tests/context/python/function/test_candidates.py",
                UsefulnessJudgment.USEFUL,
                "Provides focused evidence that token candidates remain distinct from declaration analysis.",
            ),
        ),
        (),
        _COMMON_PROVENANCE,
        AdjudicationCompleteness.INITIAL_JUDGMENTS_ONLY,
        "A directional no-qualifier abstention opportunity: no target is presumed eligible or qualified before execution.",
    ),
    FrozenValidationCase(
        "import-declaration-source-evidence-contract",
        "Identify the implementation and focused test that preserve direct module-body "
        "import declaration source-occurrence and span evidence.",
        "direct module body import declaration source occurrence",
        PurposeProfile.LOCAL_DEFINITION_OR_GOVERNANCE,
        ValidationRoute.HETEROGENEOUS_K5,
        (
            _judgment(
                "src/devtools/context/python/imports/declarations.py",
                UsefulnessJudgment.USEFUL,
                "Owns direct module-body import declaration derivation and source evidence.",
            ),
            _judgment(
                "tests/context/python/imports/test_declarations.py",
                UsefulnessJudgment.USEFUL,
                "Provides focused source-occurrence and declaration-derivation evidence.",
            ),
        ),
        (),
        _COMMON_PROVENANCE,
        AdjudicationCompleteness.INITIAL_JUDGMENTS_ONLY,
        "This local source-and-test need must not receive relationship admission merely because relations exist nearby.",
    ),
    FrozenValidationCase(
        "repository-context-taxonomy-boundary",
        "Identify the authoritative current documentation defining Context as purpose-"
        "relative information and distinguishing it from Memory and Persistence.",
        "Context purpose relative information Memory Persistence",
        PurposeProfile.LOCAL_DEFINITION_OR_GOVERNANCE,
        ValidationRoute.HETEROGENEOUS_K5,
        (
            _judgment(
                "docs/architecture/taxonomy.md",
                UsefulnessJudgment.USEFUL,
                "Authoritative taxonomy defines Context and its distinctions from Memory and Persistence.",
            ),
            _judgment(
                "docs/architecture.md",
                UsefulnessJudgment.USEFUL,
                "Authoritative architecture records accepted Context and disclosure boundaries.",
            ),
            _judgment(
                "src/devtools/context/python/function/request_assembly.py",
                UsefulnessJudgment.NOT_USEFUL,
                "A model-facing implementation detail cannot establish the requested current architectural semantics.",
            ),
        ),
        (),
        _COMMON_PROVENANCE,
        AdjudicationCompleteness.INITIAL_JUDGMENTS_ONLY,
        "Governance/documentation need; relationship admission is purpose-inapplicable rather than a source/test heuristic.",
    ),
)

_DIRECT_RESOLUTION_CONTROLS = (
    DirectResolutionValidationControl(
        "exact-name-function-retrieval",
        "Locate the exact declared Python function that performs exact-name declaration retrieval.",
        "retrieve_python_functions_by_exact_name",
        RepositoryResourceAddress("src/devtools/context/python/function/retrieval.py"),
        "Exact declared-name resolution is the appropriate bounded operation, so this control is outside heterogeneous K=5 metrics.",
    ),
    DirectResolutionValidationControl(
        "exact-name-source-materialization",
        "Locate the exact declared Python function that materializes source for a Python-function disclosure.",
        "materialize_python_function_disclosure_source",
        RepositoryResourceAddress("src/devtools/context/python/function/materialization.py"),
        "Exact declared-name resolution is the appropriate bounded operation, so this control is outside heterogeneous K=5 metrics.",
    ),
)

_BLINDED_ADJUDICATION_PROTOCOL = BlindedAdjudicationProtocol(
    hidden_fields=(
        "lexical rank and score",
        "lexical versus relationship origin",
        "relationship direction and support count",
        "qualification and admission status",
        "displaced-resource status",
        "oracle membership and result",
        "final mechanism result",
    ),
    visible_fields=(
        "frozen information need and purpose rationale",
        "resource content or the bounded evidence needed to judge usefulness",
    ),
    address_handling=(
        "Show a resource address only when needed to interpret the supplied content; "
        "otherwise use a neutral local label.  Address visibility is recorded per judgment."
    ),
    immutability_rule=(
        "The independent adjudicator records USEFUL, NOT_USEFUL, or UNJUDGED with a rationale; "
        "the complete material-surface judgment set is fingerprinted before unblinding."
    ),
)

_FAILURE_TAXONOMY = (
    "corpus-acquisition",
    "lexical-surfacing",
    "relationship-surfacing",
    "qualification",
    "admission",
    "reservation-capacity",
    "rejection",
    "abstention",
    "direct-resolution",
    "judgment-coverage",
)

_COMPARISON_ARMS = (
    ("canonical-lexical-top-5", "practical baseline"),
    ("directional-reservation-v1", "unchanged practical experimental rule"),
    ("blind-relationship-insertion", "falsification reference"),
    ("lexical-top-15", "coverage control"),
    ("oracle-headroom", "evaluation-only"),
    ("direct-resolution-controls", "outside heterogeneous K=5 metrics"),
)

_SHADOW_READINESS_CRITERIA = (
    "material decision surfaces are fully adjudicated",
    "each represented directional profile with eligible opportunity has a useful admission",
    "eligible explicit negative controls are exposed and rejected",
    "no confirmed useful lexical rank-five resource is displaced",
    "abstentions are explainable and appropriate",
    "fingerprints and provenance are complete",
    "production retrieval and Context disclosure remain unaffected",
)

_ABANDONMENT_CRITERIA = (
    "an eligible explicit NOT_USEFUL control is admitted",
    "a confirmed useful lexical rank-five resource is displaced",
    "material decision surfaces cannot be fully adjudicated",
    "no useful qualified admission occurs",
    "no useful evidence is provided beyond canonical lexical retrieval",
)


def frozen_validation_cases() -> tuple[FrozenValidationCase, ...]:
    """Return configuration only; never execute a prospective mechanism."""
    return _CASES


def direct_resolution_validation_controls() -> tuple[DirectResolutionValidationControl, ...]:
    """Return the two exact-name controls outside heterogeneous evaluation."""
    return _DIRECT_RESOLUTION_CONTROLS


def blinded_adjudication_protocol() -> BlindedAdjudicationProtocol:
    """Return the precommitted post-surface judgment procedure."""
    return _BLINDED_ADJUDICATION_PROTOCOL


def failure_taxonomy() -> tuple[str, ...]:
    """Return the precommitted failure-localization categories."""
    return _FAILURE_TAXONOMY


def comparison_arms() -> tuple[tuple[str, str], ...]:
    """Return practical, control, and evaluation-only comparison roles."""
    return _COMPARISON_ARMS


def shadow_readiness_criteria() -> tuple[str, ...]:
    """Return the pre-result threshold for a non-controlling shadow baseline."""
    return _SHADOW_READINESS_CRITERIA


def abandonment_criteria() -> tuple[str, ...]:
    """Return the pre-result conditions that retire this practical rule untuned."""
    return _ABANDONMENT_CRITERIA


def increment_23_validation_design_fingerprint() -> str:
    """Fingerprint all behavior- and evaluation-affecting frozen input only."""
    payload = {
        "semantics": "increment-23-independent-validation-design-v1",
        "increment-22-rule-fingerprint": INCREMENT_22_RULE_FINGERPRINT,
        "cases": [
            {
                "name": case.name,
                "information_need": case.information_need,
                "query_text": case.query_text,
                "profile": case.profile.value,
                "route": case.route.value,
                "judgments": [
                    (item.address.value, item.judgment.value, item.rationale, item.is_control)
                    for item in case.judgments
                ],
                "relationship_controls": [
                    (
                        control.address.value,
                        control.relation_source.value,
                        control.relation_target.value,
                        control.direction.value,
                        control.relation_truth_rationale,
                        control.not_useful_rationale,
                    )
                    for control in case.relationship_controls
                ],
                "provenance_assumption": case.provenance_assumption,
                "adjudication_completeness": case.adjudication_completeness.value,
                "caveat": case.caveat,
            }
            for case in _CASES
        ],
        "direct_resolution_controls": [
            (
                control.name,
                control.information_need,
                control.declared_name,
                control.useful_address.value,
                control.rationale,
            )
            for control in _DIRECT_RESOLUTION_CONTROLS
        ],
        "blinded_adjudication": {
            "hidden": _BLINDED_ADJUDICATION_PROTOCOL.hidden_fields,
            "visible": _BLINDED_ADJUDICATION_PROTOCOL.visible_fields,
            "address_handling": _BLINDED_ADJUDICATION_PROTOCOL.address_handling,
            "immutability_rule": _BLINDED_ADJUDICATION_PROTOCOL.immutability_rule,
        },
        "failure_taxonomy": _FAILURE_TAXONOMY,
        "comparison_arms": _COMPARISON_ARMS,
        "shadow_readiness": _SHADOW_READINESS_CRITERIA,
        "abandonment": _ABANDONMENT_CRITERIA,
        "material_decision_surface": (
            "canonical lexical top five, rank-five resource, profile-eligible relationship "
            "targets, qualified targets, admitted target, and eligible explicit controls; "
            "top-fifteen resources are adjudicated only when needed for a coverage claim."
        ),
        "metrics": (
            "surface recall, beyond-top-five and beyond-top-fifteen useful exposure, "
            "qualification, fully-judged admission precision, conditional admission recall, "
            "control exposure/qualification/rejection, rank-five displacement, useful losses, "
            "abstention appropriateness, final Hit@5/Recall@5/MRR, profile-direction evidence, "
            "and separate direct-resolution results"
        ),
    }
    encoded = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()
