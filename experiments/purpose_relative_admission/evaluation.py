# Copyright (c) 2026
# ruff: noqa: ANN401, E501, I001, PLR0913, T201
# mypy: disable-error-code="arg-type,assignment,attr-defined,index,no-any-return,no-untyped-call,union-attr"
"""Execute and evaluate frozen directional reservation without judgment leakage."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from devtools.context.python.function.declarations import (
    PythonModuleParseError,
    derive_python_function_declarations,
)
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from experiments.import_relationship_cases import ImportRelationshipDirection
from experiments.purpose_relative_admission.design import (
    ExperimentPartition,
    FrozenAdmissionCase,
    PurposeProfile,
    directional_reservation_v1_fingerprint,
    direct_resolution_controls,
    frozen_admission_cases,
)
from experiments.purpose_relative_admission.direct_resolution import (
    DirectResolutionControlResult,
    run_exact_name_direct_resolution_control,
)
from experiments.purpose_relative_admission.reservation import (
    AdmissionDisposition,
    DirectionalReservationResult,
    RetainedRelationshipTarget,
    apply_directional_reservation_v1,
    direction_for_profile,
)
from experiments.purpose_relative_admission.surfaces import (
    canonical_lexical_top_five,
    construct_relationship_surfaces,
)
from experiments.purpose_relative_import.cases import (
    PurposeRelativeNeed,
    UsefulnessJudgment,
)
from experiments.purpose_relative_import.comparison import (
    ImportRelationshipSurface,
    RankedLexicalSurface,
    _derive_relations,
    _relationship_surfaces,
    blind_insert,
)
from scripts.retrieval_bm25_baseline import run_benchmark

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from devtools.context.python.function.declarations import (
        PythonFunctionDeclarationKnowledge,
    )
    from devtools.context.python.modules import PythonModuleInterpretation
    from devtools.context.retrieval.lexical.index import (
        RepositoryTextLexicalInvertedIndex,
    )

_EXPECTED_FINGERPRINT = "7e215ac2961a4329074e9a25d35d3decc554f394435aa0b73cb2251254160345"
_CHECKPOINT_HEAD = "251e290c985d1b93aa97b346ee44dbb949f21932"
_K = 5
_LEXICAL_WIDTH = 15
_SEED_WIDTH = 3
_SUPPORT_THRESHOLD = 2
_RESERVATION_RANK = 5
_ADMISSION_LIMIT = 1
_HISTORICAL_REPORT = ".b0002-purpose-relative-oracle-headroom.json"
_REPORT_SCHEMA = "devtools-b0002-purpose-relative-admission-rule-v1"


@dataclass(frozen=True, slots=True)
class FrozenCaseRanking:
    """A judgment-free ranking and its native relationship evidence."""

    name: str
    query: str
    profile: PurposeProfile
    lexical: tuple[RankedLexicalSurface, ...]
    outgoing: tuple[ImportRelationshipSurface, ...]
    incoming: tuple[ImportRelationshipSurface, ...]
    practical: DirectionalReservationResult


@dataclass(frozen=True, slots=True)
class FrozenRankingRun:
    """All rankings constructed before evaluation configuration is consulted."""

    rankings: tuple[FrozenCaseRanking, ...]


def construct_frozen_case_ranking(
    *,
    name: str,
    query: str,
    profile: PurposeProfile,
    index: RepositoryTextLexicalInvertedIndex,
    relations: tuple[Any, ...],
    interpretations_by_address: Mapping[
        RepositoryResourceAddress,
        tuple[PythonModuleInterpretation, ...],
    ],
) -> FrozenCaseRanking:
    """Construct a ranking from query/profile and repository evidence only."""
    result = retrieve_repository_text_documents_by_bm25(
        query=analyze_repository_text_lexical_query(text=query),
        index=index,
        maximum_results=_LEXICAL_WIDTH,
    )
    lexical = tuple(
        RankedLexicalSurface(
            match.document_statistics.analysis.document.resource.address,
            rank,
            match.score,
        )
        for rank, match in enumerate(result.matches, start=1)
    )
    outgoing = _relationship_surfaces(
        lexical=lexical,
        relations=relations,
        interpretations_by_address=dict(interpretations_by_address),
        direction=ImportRelationshipDirection.OUTGOING,
    )
    incoming = _relationship_surfaces(
        lexical=lexical,
        relations=relations,
        interpretations_by_address=dict(interpretations_by_address),
        direction=ImportRelationshipDirection.INCOMING,
    )
    practical = apply_directional_reservation_v1(
        profile=profile,
        canonical_lexical_top_five=canonical_lexical_top_five(lexical=lexical),
        surfaces=construct_relationship_surfaces(surfaces=(*outgoing, *incoming)),
    )
    return FrozenCaseRanking(name, query, profile, lexical, outgoing, incoming, practical)


def construct_frozen_rankings(
    *,
    cases: Sequence[tuple[str, str, PurposeProfile]],
    index: RepositoryTextLexicalInvertedIndex,
    relations: tuple[Any, ...],
    interpretations_by_address: Mapping[
        RepositoryResourceAddress,
        tuple[PythonModuleInterpretation, ...],
    ],
) -> FrozenRankingRun:
    """Construct rankings without accepting judgments, controls, or rationales."""
    return FrozenRankingRun(
        tuple(
            construct_frozen_case_ranking(
                name=name,
                query=query,
                profile=profile,
                index=index,
                relations=relations,
                interpretations_by_address=interpretations_by_address,
            )
            for name, query, profile in cases
        ),
    )


def ranking_metrics(
    *,
    rankings: Sequence[tuple[RepositoryResourceAddress, ...]],
    relevant: Sequence[set[RepositoryResourceAddress]],
) -> dict[str, float]:
    """Aggregate binary relevance after rankings have already been constructed."""
    if not rankings or len(rankings) != len(relevant):
        msg = "Metric aggregation requires equally sized non-empty ranking/judgment inputs."
        raise ValueError(msg)
    hits: list[bool] = []
    recalls: list[float] = []
    reciprocal_ranks: list[float] = []
    for ranking, useful in zip(rankings, relevant, strict=True):
        recovered = tuple(address for address in ranking[:_K] if address in useful)
        hits.append(bool(recovered))
        recalls.append(len(recovered) / len(useful))
        reciprocal_ranks.append(
            next(
                (1 / rank for rank, address in enumerate(ranking[:_K], start=1) if address in useful),
                0.0,
            ),
        )
    count = len(rankings)
    return {
        "hit_at_5": sum(hits) / count,
        "mean_recall_at_5": sum(recalls) / count,
        "mrr": sum(reciprocal_ranks) / count,
    }


def evaluate_rankings(
    *,
    rankings: FrozenRankingRun,
    cases: Sequence[FrozenAdmissionCase],
    historical: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Apply frozen judgments only after all practical rankings exist."""
    by_name = {case.name: case for case in rankings.rankings}
    evaluated = tuple(
        _evaluate_case(
            case=case,
            ranking=by_name[case.need.name],
            historical=historical,
        )
        for case in cases
    )
    calibration = tuple(item for item in evaluated if item["partition"] == ExperimentPartition.CALIBRATION.value)
    held_out = tuple(item for item in evaluated if item["partition"] == ExperimentPartition.HELD_OUT.value)
    return {
        "calibration": calibration,
        "held_out": held_out,
        "held_out_aggregate": aggregate_evaluated_cases(held_out),
        "same_query_different_purpose": _same_query_pair(held_out),
    }


def aggregate_evaluated_cases(cases: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Aggregate outcome, displacement, control, and fan-out evidence."""
    if not cases:
        msg = "Admission aggregation requires at least one evaluated case."
        raise ValueError(msg)
    canonical_rankings = tuple(
        tuple(RepositoryResourceAddress(value["address"]) for value in case["canonical_lexical_top_5"])
        for case in cases
    )
    practical_rankings = tuple(
        tuple(RepositoryResourceAddress(value) for value in case["practical"]["final_top_5"])
        for case in cases
    )
    relevant = tuple(
        {RepositoryResourceAddress(value["address"]) for value in case["judgments"] if value["judgment"] == UsefulnessJudgment.USEFUL.value}
        for case in cases
    )
    abstentions = Counter(
        case["practical"]["abstention_reason"]
        for case in cases
        if case["practical"]["abstention_reason"] is not None
    )
    qualifying_supports = [
        target["unique_support_count"]
        for case in cases
        for target in case["relationship_evidence"]["deduplicated_targets"]
        if target["qualification_reason"] == "qualified"
    ]
    admitted_supports = [
        case["practical"]["admitted_unique_support_count"]
        for case in cases
        if case["practical"]["admitted_unique_support_count"] is not None
    ]
    direction_counts: Counter[str] = Counter()
    for case in cases:
        direction = case["relationship_evidence"]["eligible_direction"]
        if direction is not None:
            direction_counts[direction] += case["relationship_evidence"]["deduplicated_candidate_count"]
    displacements = tuple(case for case in cases if case["practical"]["displaced_lexical_rank_5"] is not None)
    return {
        "case_count": len(cases),
        "canonical_lexical": ranking_metrics(rankings=canonical_rankings, relevant=relevant),
        "directional_reservation_v1": ranking_metrics(rankings=practical_rankings, relevant=relevant),
        "admitted_case_count": sum(case["practical"]["disposition"] == AdmissionDisposition.ADMITTED.value for case in cases),
        "local_profile_abstention_count": abstentions["local-profile"],
        "no_qualifying_target_abstention_count": abstentions["no-qualifying-target"],
        "newly_recovered_relevant_resource_count": sum(len(case["comparison_to_canonical"]["newly_recovered_relevant"]) for case in cases),
        "previously_retrieved_relevant_resource_lost_count": sum(len(case["comparison_to_canonical"]["relevant_losses"]) for case in cases),
        "explicit_controls_admitted_count": sum(len(case["control_evidence"]["admitted"]) for case in cases),
        "explicit_controls_exposed_count": sum(len(case["control_evidence"]["exposed_or_considered"]) for case in cases),
        "rank_5_displacement_count": len(displacements),
        "displacements_removing_relevant_count": sum(bool(case["comparison_to_canonical"]["relevant_losses"]) for case in displacements),
        "admissions_relevant_count": sum(case["practical"]["admitted_judgment"] == UsefulnessJudgment.USEFUL.value for case in cases),
        "admissions_irrelevant_or_unjudged_count": sum(case["practical"]["admitted_judgment"] in {UsefulnessJudgment.NOT_USEFUL.value, UsefulnessJudgment.UNJUDGED.value} for case in cases),
        "candidate_counts_by_direction": dict(sorted(direction_counts.items())),
        "maximum_relation_target_fan_out": max(case["relationship_evidence"]["deduplicated_candidate_count"] for case in cases),
        "maximum_relation_encounter_fan_out": max(case["relationship_evidence"]["encounter_count"] for case in cases),
        "unique_support_count_distribution": {
            "qualifying": dict(sorted(Counter(qualifying_supports).items())),
            "admitted": dict(sorted(Counter(admitted_supports).items())),
        },
    }


def build_report(
    *,
    benchmark: Any,
    relation_coverage: Mapping[str, Any],
    evaluation: Mapping[str, Any],
    direct_controls: Sequence[tuple[str, DirectResolutionControlResult]],
    fingerprint: str,
    historical: Mapping[str, Any] | None,
    failure_notes: Sequence[str] = (),
) -> dict[str, Any]:
    """Construct the deterministic, versioned Pass 4 audit artifact."""
    return {
        "schema": _REPORT_SCHEMA,
        "scope": "Increment 22 Pass 4 frozen real-repository evaluation; no promotion decision",
        "repository_checkpoint": {
            "branch": "main",
            "head": _CHECKPOINT_HEAD,
            "repository_id": str(benchmark.definition.discovery.repository_id),
            "snapshot_id": str(benchmark.snapshot.id),
            "corpus_id": str(benchmark.corpus.id),
        },
        "acquisition": {
            "maximum_discovered_resources": 10_000,
            "maximum_traversal_entries": 20_000,
            "maximum_resource_bytes": 1_048_576,
            "discovered_resource_count": len(benchmark.discovery.addresses),
            "examined_entry_count": benchmark.discovery.examined_entry_count,
            "selected_resource_count": len(benchmark.definition.selected_addresses),
            "observed_resource_count": len(benchmark.snapshot.resources),
            "document_count": len(benchmark.documents.documents),
        },
        "relation_coverage": dict(relation_coverage),
        "configuration": {
            "production_lexical": "content-bm25 + 0.25 filename-stem-bm25",
            "k": _K,
            "lexical_consideration_width": _LEXICAL_WIDTH,
            "relationship_seed_width": _SEED_WIDTH,
            "minimum_distinct_relation_supports": _SUPPORT_THRESHOLD,
            "reservation_rank": _RESERVATION_RANK,
            "maximum_relationship_admissions": _ADMISSION_LIMIT,
            "design_rule_fingerprint": fingerprint,
            "expected_design_rule_fingerprint": _EXPECTED_FINGERPRINT,
            "purpose_assignments": [
                {
                    "name": case.need.name,
                    "partition": case.partition.value,
                    "profile": case.profile.value,
                }
                for case in frozen_admission_cases()
            ],
        },
        "direct_resolution_controls": [
            {
                "name": name,
                "declared_name": result.declared_name,
                "direct_resolution_succeeded": bool(result.resource_addresses),
                "returned_resources": list(result.resource_addresses),
                "result_cardinality": len(result.resource_addresses),
                "ambiguity_or_zero_behavior": "zero" if not result.resource_addresses else "multiple-matches-retained" if len(result.resource_addresses) > 1 else "one-match",
                "applicable_to_heterogeneous_k5_metrics": result.applicable_to_heterogeneous_k5_metrics,
                "directional_reservation_heterogeneous_admission_performed": False,
            }
            for name, result in direct_controls
        ],
        "calibration": list(evaluation["calibration"]),
        "held_out": list(evaluation["held_out"]),
        "held_out_aggregate": dict(evaluation["held_out_aggregate"]),
        "same_query_different_purpose": dict(evaluation["same_query_different_purpose"]),
        "oracle_headroom_reference": {
            "status": "historical-unpaired-reference" if historical else "unavailable",
            "historical_checkpoint": historical.get("checkpoint") if historical else None,
            "historical_aggregate": historical.get("aggregate") if historical else None,
            "reason": "Increment 21 report used a different checkpoint/corpus; retained without fabricating a paired comparison.",
        },
        "run_history": {
            "successful_held_out_run_count": 1,
            "mechanical_failure_notes": list(failure_notes),
            "tuning_after_results": False,
        },
    }


def run_evaluation(*, repository_root: Path) -> dict[str, Any]:
    """Perform the one frozen real-repository ranking/evaluation realization."""
    fingerprint = directional_reservation_v1_fingerprint()
    if fingerprint != _EXPECTED_FINGERPRINT:
        msg = f"Frozen fingerprint mismatch: expected {_EXPECTED_FINGERPRINT}, got {fingerprint}."
        raise RuntimeError(msg)
    benchmark = run_benchmark(repository_root=repository_root)
    relations, relation_coverage, interpretations = _derive_relations(benchmark.snapshot)
    cases = frozen_admission_cases()
    rankings = construct_frozen_rankings(
        cases=tuple((case.need.name, case.need.query_text, case.profile) for case in cases),
        index=benchmark.index,
        relations=relations,
        interpretations_by_address=interpretations,
    )
    historical_path = repository_root / _HISTORICAL_REPORT
    historical = json.loads(historical_path.read_text(encoding="utf-8")) if historical_path.exists() else None
    evaluation = evaluate_rankings(rankings=rankings, cases=cases, historical=historical)
    declarations = _function_declarations(benchmark.snapshot)
    controls = tuple(
        (
            control.name,
            run_exact_name_direct_resolution_control(
                declared_name=control.declared_name,
                declarations=declarations,
            ),
        )
        for control in direct_resolution_controls()
    )
    return build_report(
        benchmark=benchmark,
        relation_coverage=relation_coverage,
        evaluation=evaluation,
        direct_controls=controls,
        fingerprint=fingerprint,
        historical=historical,
    )


def _function_declarations(snapshot: Any) -> tuple[PythonFunctionDeclarationKnowledge, ...]:
    values: list[PythonFunctionDeclarationKnowledge] = []
    for resource in snapshot.resources:
        if not resource.address.value.endswith(".py"):
            continue
        try:
            analysis = derive_python_function_declarations(snapshot, resource_address=resource.address)
        except PythonModuleParseError:
            continue
        values.extend(analysis.declarations)
    return tuple(values)


def _evaluate_case(
    *,
    case: FrozenAdmissionCase,
    ranking: FrozenCaseRanking,
    historical: Mapping[str, Any] | None,
) -> dict[str, Any]:
    need = case.need
    useful = {item.address for item in need.judgments if item.judgment is UsefulnessJudgment.USEFUL}
    controls = {item.address for item in need.judgments if item.is_control}
    canonical = tuple(surface.address for surface in ranking.lexical[:_K])
    practical = ranking.practical.addresses
    direction = direction_for_profile(case.profile)
    eligible = () if direction is None else ranking.outgoing if direction is ImportRelationshipDirection.OUTGOING else ranking.incoming
    adapted = construct_relationship_surfaces(surfaces=eligible)
    retained = ranking.practical.retained_targets
    admitted = ranking.practical.admitted_target.address if ranking.practical.admitted_target else None
    displaced = canonical[-1] if ranking.practical.disposition is AdmissionDisposition.ADMITTED else None
    historical_case = _historical_case(historical, need.name)
    blind = blind_insert(canonical=canonical, relationship_surfaces=(*ranking.outgoing, *ranking.incoming))
    exposed_controls = tuple(sorted(controls & {surface.address for surface in eligible}, key=str))
    return {
        "name": need.name,
        "partition": case.partition.value,
        "query": need.query_text,
        "information_need": need.information_need,
        "purpose_profile": case.profile.value,
        "judgments": [
            {
                "address": str(item.address),
                "judgment": item.judgment.value,
                "rationale": item.rationale,
                "is_control": item.is_control,
            }
            for item in need.judgments
        ],
        "canonical_lexical_top_5": [
            {"rank": surface.rank, "address": str(surface.address), "native_score": surface.score}
            for surface in ranking.lexical[:_K]
        ],
        "lexical_seeds": [
            {"rank": surface.rank, "address": str(surface.address), "native_score": surface.score}
            for surface in ranking.lexical[:_SEED_WIDTH]
        ],
        "relationship_evidence": {
            "eligible_direction": direction.value if direction else None,
            "local_profile_abstention": direction is None,
            "encounter_count": len(adapted),
            "considered_target_encounters": [_encounter_payload(surface) for surface in adapted],
            "deduplicated_candidate_count": len(retained),
            "deduplicated_targets": [_target_payload(target, canonical) for target in retained],
        },
        "practical": {
            "disposition": ranking.practical.disposition.value,
            "abstention_reason": ranking.practical.abstention_reason.value if ranking.practical.abstention_reason else None,
            "admitted_resource": str(admitted) if admitted else None,
            "admitted_unique_support_count": ranking.practical.admitted_target.support_count if ranking.practical.admitted_target else None,
            "admitted_judgment": _judgment(need, admitted).value if admitted else None,
            "displaced_lexical_rank_5": str(displaced) if displaced else None,
            "final_top_5": [str(address) for address in practical],
        },
        "comparison_to_canonical": {
            "canonical_metrics": _case_metrics(canonical, useful),
            "practical_metrics": _case_metrics(practical, useful),
            "newly_recovered_relevant": [str(address) for address in practical if address in useful and address not in canonical],
            "relevant_losses": [str(address) for address in canonical if address in useful and address not in practical],
        },
        "control_evidence": {
            "exposed_or_considered": [str(address) for address in exposed_controls],
            "admitted": [str(admitted)] if admitted in controls else [],
            "present_in_final_top_5": [str(address) for address in practical if address in controls],
        },
        "comparison_arms": {
            "canonical_lexical_top_5": [str(address) for address in canonical],
            "directional_reservation_v1": [str(address) for address in practical],
            "blind_bidirectional_insertion_reference": {
                "addresses": [str(address) for address in blind],
                "metrics": _case_metrics(blind, useful),
            },
            "increment_21_historical": _historical_reference(historical_case),
        },
    }


def _target_payload(
    target: RetainedRelationshipTarget,
    canonical: tuple[RepositoryResourceAddress, ...],
) -> dict[str, Any]:
    already_lexical = target.address in canonical
    if already_lexical:
        reason = "already-in-canonical-lexical-top-5"
    elif target.support_count < _SUPPORT_THRESHOLD:
        reason = "fewer-than-two-distinct-relation-supports"
    else:
        reason = "qualified"
    return {
        "address": str(target.address),
        "direction": target.direction.value,
        "unique_support_count": target.support_count,
        "earliest_supporting_lexical_seed_rank": target.earliest_seed_rank,
        "earliest_native_encounter_order": target.earliest_encounter_ordinal,
        "qualification_reason": reason,
        "unique_relation_supports": [_encounter_payload(surface) for surface in target.unique_supports],
        "all_encounters": [_encounter_payload(surface) for surface in target.encounters],
    }


def _encounter_payload(surface: Any) -> dict[str, Any]:
    return {
        "target_address": str(surface.address),
        "direction": surface.direction.value,
        "seed_address": str(surface.seed_address),
        "seed_rank": surface.seed_rank,
        "relation_identity": surface.relation_identity,
        "native_encounter_order": surface.encounter_ordinal,
    }


def _case_metrics(
    ranking: tuple[RepositoryResourceAddress, ...],
    useful: set[RepositoryResourceAddress],
) -> dict[str, float | bool]:
    recovered = tuple(address for address in ranking[:_K] if address in useful)
    return {
        "hit_at_5": bool(recovered),
        "recall_at_5": len(recovered) / len(useful),
        "reciprocal_rank": next((1 / rank for rank, address in enumerate(ranking[:_K], 1) if address in useful), 0.0),
    }


def _judgment(need: PurposeRelativeNeed, address: RepositoryResourceAddress | None) -> UsefulnessJudgment:
    return next(
        (item.judgment for item in need.judgments if item.address == address),
        UsefulnessJudgment.UNJUDGED,
    )


def _historical_case(historical: Mapping[str, Any] | None, name: str) -> Mapping[str, Any] | None:
    if historical is None:
        return None
    return next((item for item in historical.get("cases", ()) if item.get("name") == name), None)


def _historical_reference(case: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if case is None:
        return None
    arms = case["arms"]
    return {
        "status": "historical-unpaired-different-checkpoint",
        "lexical_width_oracle": arms["B_lexical_width"]["oracle"],
        "outgoing_relationship_oracle": arms["C_outgoing"]["oracle"],
        "incoming_relationship_oracle": arms["D_incoming"]["oracle"],
        "bidirectional_relationship_oracle": arms["E_bidirectional"]["oracle"],
        "blind_outgoing": {
            "addresses": arms["C_outgoing"]["blind_insertion"],
            "recall_at_5": arms["C_outgoing"]["blind_recall_at_5"],
            "controls": arms["C_outgoing"]["blind_controls"],
        },
        "blind_incoming": {
            "addresses": arms["D_incoming"]["blind_insertion"],
            "recall_at_5": arms["D_incoming"]["blind_recall_at_5"],
            "controls": arms["D_incoming"]["blind_controls"],
        },
    }


def _same_query_pair(cases: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_name = {case["name"]: case for case in cases}
    architecture = by_name["context-disclosure-architecture"]
    implementation = by_name["context-disclosure-implementation"]
    return {
        "query_text_identical": architecture["query"] == implementation["query"],
        "query": architecture["query"],
        "architecture_profile": architecture["purpose_profile"],
        "implementation_profile": implementation["purpose_profile"],
        "architecture_local_profile_abstained": architecture["practical"]["abstention_reason"] == "local-profile",
        "implementation_eligible_direction": implementation["relationship_evidence"]["eligible_direction"],
        "practical_outcomes_differ": architecture["practical"]["final_top_5"] != implementation["practical"]["final_top_5"],
        "architecture_metrics": architecture["comparison_to_canonical"]["practical_metrics"],
        "implementation_metrics": implementation["comparison_to_canonical"]["practical_metrics"],
        "explanation": "The query and lexical ranking are shared; the local architecture profile abstains, while the implementation profile permits only incoming relation evidence and still must satisfy the frozen support threshold.",
    }


def write_report(*, path: Path, payload: Mapping[str, Any]) -> None:
    """Write deterministic JSON for the caller-selected Pass 4 artifact."""
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    """Execute the one authorized real-repository evaluation and write its report."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--report-path", type=Path, required=True)
    parsed = parser.parse_args()
    payload = run_evaluation(repository_root=parsed.repository_root.resolve())
    write_report(path=parsed.report_path, payload=payload)
    print(json.dumps(payload["held_out_aggregate"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
