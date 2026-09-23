# Copyright (c) 2026
# ruff: noqa: C901, COM812, E501, PLR0913, PLR0915, PLR2004, T201
"""Complete the retained Increment-23 evaluation after authorized unblinding."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from experiments.purpose_relative_admission.validation_design import (
    comparison_arms,
    frozen_validation_cases,
)
from experiments.purpose_relative_admission.validation_evaluation import (
    ControlAdjudicationConflictReview,
    ControlConflictDisposition,
)
from experiments.purpose_relative_admission.validation_execution import (
    artifact_envelope,
    load_blinded_adjudication_packages,
    load_frozen_adjudication_artifact,
    validate_artifact_correspondence,
    validate_artifact_envelope,
    write_artifact,
)
from experiments.purpose_relative_import.cases import UsefulnessJudgment

_REPORT_SCHEMA = "devtools-b0002-purpose-relative-independent-validation-v1"
_PRODUCTION_BEHAVIOR = "content BM25 + 0.25 * filename-stem BM25; K = 5; unchanged"
_ARTIFACT_NAMES = {
    "capture": ".b0002-increment-23-hidden-surface-capture.json",
    "mapping": ".b0002-increment-23-neutral-resource-mapping.json",
    "package": ".b0002-increment-23-blinded-adjudication-package.json",
    "frozen_adjudication": ".b0002-increment-23-frozen-adjudication.json",
}


def increment_23_control_conflict_review() -> ControlAdjudicationConflictReview:
    """Retain the single authorized post-unblinding semantic review."""
    case = next(
        item
        for item in frozen_validation_cases()
        if item.name == "content-bm25-term-formula"
    )
    control = next(
        item
        for item in case.relationship_controls
        if item.address.value == "src/devtools/context/retrieval/lexical/filename.py"
    )
    return ControlAdjudicationConflictReview(
        case_name=case.name,
        neutral_id="resource-a14175c2072d3f9c",
        address=control.address,
        frozen_blinded_judgment=UsefulnessJudgment.USEFUL,
        frozen_control_expectation=UsefulnessJudgment.NOT_USEFUL,
        original_control_rationale=control.not_useful_rationale,
        reviewed_evidence=(
            "filename.py imports both shared Okapi BM25 formula helpers from scoring.py.",
            "score_repository_text_filename_lexical_bm25 invokes the shared term-contribution helper with the same settings type.",
            "bm25.py imports filename-field indexing/scoring and combines that field at the frozen 0.25 weight.",
        ),
        disposition=ControlConflictDisposition.CONTROL_EXPECTATION_UNSUPPORTED,
        rationale=(
            "The resource materially identifies the coupled filename-scoring boundary that "
            "must be protected while changing content-only term scoring; the original negative "
            "control expectation is therefore unsupported for this exact InformationNeed."
        ),
    )


def build_increment_23_report(*, repository_root: Path) -> dict[str, Any]:
    """Evaluate immutable retained artifacts without rerunning capture or retrieval."""
    envelopes = {
        name: json.loads((repository_root / filename).read_text(encoding="utf-8"))
        for name, filename in _ARTIFACT_NAMES.items()
    }
    capture_envelope = envelopes["capture"]
    mapping_envelope = envelopes["mapping"]
    package_envelope = envelopes["package"]
    frozen_envelope = envelopes["frozen_adjudication"]
    if not validate_artifact_correspondence(
        capture=capture_envelope,
        package=package_envelope,
        mapping=mapping_envelope,
    ):
        msg = "Increment-23 capture, package, and mapping do not correspond."
        raise ValueError(msg)
    packages = load_blinded_adjudication_packages(package_envelope)
    frozen = load_frozen_adjudication_artifact(
        envelope=frozen_envelope,
        packages=packages,
        package_set_identity=package_envelope["payload"]["package_set_identity"],
    )
    capture_payload = capture_envelope["payload"]
    mapping_payload = mapping_envelope["payload"]
    case_designs = {case.name: case for case in frozen_validation_cases()}
    conflict = increment_23_control_conflict_review()
    unsupported_controls = {(conflict.case_name, conflict.address.value)}
    case_results: list[dict[str, Any]] = []
    arm_cases: dict[str, list[dict[str, Any]]] = {
        "canonical-lexical-top-5": [],
        "directional-reservation-v1": [],
        "blind-relationship-insertion": [],
        "lexical-top-15": [],
    }
    all_failures: list[dict[str, str]] = []
    aggregate: Counter[str] = Counter()
    all_useful: set[tuple[str, str]] = set()
    all_not_useful: set[tuple[str, str]] = set()
    all_unjudged: set[tuple[str, str]] = set()
    active_control_addresses: set[tuple[str, str]] = set()
    annotated_control_addresses: set[tuple[str, str]] = set()

    for package, (case_name, case_frozen), capture_case, mappings in zip(
        packages,
        frozen.cases,
        capture_payload["cases"],
        mapping_payload["mappings"],
        strict=True,
    ):
        if package.case_name != case_name or capture_case["case_name"] != case_name:
            msg = "Increment-23 case ordering differs across frozen artifacts."
            raise ValueError(msg)
        mapping_ids = [item["neutral_id"] for item in mappings]
        record_ids = [record.neutral_id for record in case_frozen.records]
        if mapping_ids != record_ids or len({item["address"] for item in mappings}) != len(mappings):
            msg = "Increment-23 neutral mapping is not ordered and one-to-one."
            raise ValueError(msg)
        judgments = {
            mapping["address"]: record.judgment.value
            for mapping, record in zip(mappings, case_frozen.records, strict=True)
        }
        neutral_ids = {
            mapping["address"]: mapping["neutral_id"] for mapping in mappings
        }
        if case_name == conflict.case_name and (
            neutral_ids.get(conflict.address.value) != conflict.neutral_id
            or judgments.get(conflict.address.value)
            != conflict.frozen_blinded_judgment.value
        ):
            msg = "The retained conflict no longer matches frozen adjudication evidence."
            raise ValueError(msg)
        useful = {address for address, value in judgments.items() if value == "useful"}
        not_useful = {
            address for address, value in judgments.items() if value == "not-useful"
        }
        unjudged = {
            address for address, value in judgments.items() if value == "unjudged"
        }
        all_useful.update((case_name, address) for address in useful)
        all_not_useful.update((case_name, address) for address in not_useful)
        all_unjudged.update((case_name, address) for address in unjudged)

        lexical_five = tuple(item["address"] for item in capture_case["lexical_top_five"])
        lexical_fifteen = tuple(
            item["address"] for item in capture_case["lexical_top_fifteen"]
        )
        practical = tuple(capture_case["practical"]["addresses"])
        blind = tuple(capture_case["blind_reference_top_five"])
        eligible = tuple(
            dict.fromkeys(
                item["address"] for item in capture_case["profile_eligible_surfaces"]
            )
        )
        retained = {
            item["address"]: item for item in capture_case["retained_targets"]
        }
        qualified = {
            address
            for address, item in retained.items()
            if len(item["unique_supports"]) >= 2 and address not in lexical_five
        }
        admitted = (
            capture_case["practical"]["admitted_target"]["address"]
            if capture_case["practical"]["admitted_target"] is not None
            else None
        )
        design_controls = {
            item.address.value
            for item in case_designs[case_name].relationship_controls
            if item.address.value in judgments
        }
        active_controls = {
            address
            for address in design_controls
            if (case_name, address) not in unsupported_controls
        }
        annotated_control_addresses.update(
            (case_name, address) for address in design_controls
        )
        active_control_addresses.update(
            (case_name, address) for address in active_controls
        )
        for name, addresses in (
            ("canonical-lexical-top-5", lexical_five),
            ("directional-reservation-v1", practical),
            ("blind-relationship-insertion", blind),
            ("lexical-top-15", lexical_fifteen),
        ):
            outside_material = {address for address in addresses if address not in judgments}
            arm_cases[name].append(
                _arm_case_metrics(
                    case_name=case_name,
                    addresses=addresses,
                    useful=useful,
                    unjudged=unjudged | outside_material,
                    outside_material=outside_material,
                    cutoff=len(addresses),
                ),
            )

        missed = sorted(useful - set(practical))
        failures: list[dict[str, str]] = []
        for address in missed:
            if address in lexical_five:
                boundary = "reservation-capacity"
                detail = "Useful lexical rank five was displaced by the sole reservation slot."
            elif address in eligible and address not in qualified:
                boundary = "surfaced-but-failed-qualification"
                detail = "Useful relationship evidence surfaced but did not meet the frozen support threshold."
            elif address in qualified:
                boundary = "qualified-but-lost-admission-ordering"
                detail = "Useful qualified evidence did not win the sole admission slot."
            elif address in lexical_fifteen:
                boundary = "lexical-top-5-capacity/no-relationship-recovery"
                detail = "Useful evidence appeared in lexical top fifteen but not top five and was not recovered by the eligible relationship surface."
            else:
                boundary = "not-surfaced-lexically-or-relationally"
                detail = "Useful evidence was absent from both retained lexical and relationship surfaces."
            failure = {
                "case_name": case_name,
                "address": address,
                "boundary": boundary,
                "detail": detail,
            }
            failures.append(failure)
            all_failures.append(failure)

        rank_five = lexical_five[4]
        displaced = rank_five not in practical
        case_result = {
            "case_name": case_name,
            "profile": capture_case["profile"],
            "judgments": dict(Counter(judgments.values())),
            "judged_fraction": (len(judgments) - len(unjudged)) / len(judgments),
            "known_useful": sorted(useful),
            "canonical_known_useful": sorted(useful & set(lexical_five)),
            "top_fifteen_known_useful": sorted(useful & set(lexical_fifteen)),
            "relationship_known_useful": sorted(useful & set(eligible)),
            "qualified": {
                "useful": sorted(qualified & useful),
                "not_useful": sorted(qualified & not_useful),
                "unjudged": sorted(qualified & unjudged),
            },
            "admission": {
                "address": admitted,
                "judgment": judgments.get(admitted) if admitted else None,
            },
            "displacement": {
                "occurred": displaced,
                "address": rank_five if displaced else None,
                "judgment": judgments[rank_five] if displaced else None,
            },
            "abstention_reason": capture_case["practical"]["abstention_reason"],
            "controls": {
                "historically_annotated": sorted(design_controls),
                "validated_negative": sorted(active_controls),
                "exposed": sorted(active_controls & set(eligible)),
                "qualified": sorted(active_controls & qualified),
                "admitted": sorted(active_controls & ({admitted} if admitted else set())),
                "unsupported_expectations": sorted(
                    address
                    for address in design_controls
                    if (case_name, address) in unsupported_controls
                ),
            },
            "useful_misses": failures,
        }
        case_results.append(case_result)
        aggregate.update(
            {
                "relationship_candidates": len(set(eligible)),
                "useful_relationship_candidates": len(set(eligible) & useful),
                "not_useful_relationship_candidates": len(set(eligible) & not_useful),
                "unjudged_relationship_candidates": len(set(eligible) & unjudged),
                "useful_relationship_beyond_top_5": len(
                    (set(eligible) & useful) - set(lexical_five)
                ),
                "useful_relationship_beyond_top_15": len(
                    (set(eligible) & useful) - set(lexical_fifteen)
                ),
                "useful_qualified": len(qualified & useful),
                "not_useful_qualified": len(qualified & not_useful),
                "unjudged_qualified": len(qualified & unjudged),
                "admissions": int(admitted is not None),
                "useful_admissions": int(admitted in useful),
                "not_useful_admissions": int(admitted in not_useful),
                "unjudged_admissions": int(admitted in unjudged),
                "displacements": int(displaced),
                "useful_displacements": int(displaced and rank_five in useful),
                "not_useful_displacements": int(displaced and rank_five in not_useful),
                "unjudged_displacements": int(displaced and rank_five in unjudged),
                "local_profile_abstentions": int(
                    capture_case["practical"]["abstention_reason"] == "local-profile"
                ),
                "no_qualifying_target_abstentions": int(
                    capture_case["practical"]["abstention_reason"]
                    == "no-qualifying-target"
                ),
            },
        )

    judgment_counts = {
        "useful": len(all_useful),
        "not_useful": len(all_not_useful),
        "unjudged": len(all_unjudged),
        "total": len(all_useful | all_not_useful | all_unjudged),
    }
    arm_results = {
        name: {
            "cases": values,
            "aggregate": _aggregate_arm_metrics(values),
        }
        for name, values in arm_cases.items()
    }
    active_controls_exposed = sum(
        len(case["controls"]["exposed"]) for case in case_results
    )
    active_controls_qualified = sum(
        len(case["controls"]["qualified"]) for case in case_results
    )
    active_controls_admitted = sum(
        len(case["controls"]["admitted"]) for case in case_results
    )
    payload = {
        "status": "complete-independent-validation",
        "repository_checkpoint": capture_payload["repository_checkpoint"],
        "fingerprints": {
            "increment_22_rule": capture_payload["rule_fingerprint"],
            "increment_23_design": capture_payload["design_fingerprint"],
            "adjudication": frozen.fingerprint,
        },
        "artifact_identities": {
            name: {
                "path": filename,
                "raw_sha256": hashlib.sha256(
                    (repository_root / filename).read_bytes()
                ).hexdigest(),
                "content_identity": envelopes[name]["content_identity"],
            }
            for name, filename in _ARTIFACT_NAMES.items()
        },
        "capture_set_identity": capture_payload["capture_set_identity"],
        "package_set_identity": package_envelope["payload"]["package_set_identity"],
        "mapping_set_identity": mapping_payload["mapping_set_identity"],
        "judgment_coverage": {
            **judgment_counts,
            "judged": judgment_counts["total"] - judgment_counts["unjudged"],
            "judged_fraction": (
                judgment_counts["total"] - judgment_counts["unjudged"]
            )
            / judgment_counts["total"],
            "cases": [
                {
                    "case_name": case["case_name"],
                    "counts": case["judgments"],
                    "judged_fraction": case["judged_fraction"],
                }
                for case in case_results
            ],
            "limitation": "UNJUDGED resources are retained as unresolved and produce metric bounds rather than coerced labels.",
        },
        "control_conflict": {
            "case_name": conflict.case_name,
            "neutral_id": conflict.neutral_id,
            "address": conflict.address.value,
            "frozen_blinded_judgment": conflict.frozen_blinded_judgment.value,
            "frozen_control_expectation": conflict.frozen_control_expectation.value,
            "original_control_rationale": conflict.original_control_rationale,
            "reviewed_evidence": list(conflict.reviewed_evidence),
            "disposition": conflict.disposition.value,
            "rationale": conflict.rationale,
            "metric_policy": "Retain both historical labels; exclude this expectation from validated-negative control claims and retain the frozen USEFUL judgment in usefulness metrics.",
        },
        "comparison_arms": arm_results,
        "comparison_arm_definitions": [list(item) for item in comparison_arms()],
        "surface_quality": {
            "known_useful_material_resources": len(all_useful),
            "known_useful_surface_recall": 1.0,
            "canonical_known_useful_recovered": sum(
                len(case["canonical_known_useful"]) for case in case_results
            ),
            "known_useful_beyond_top_5": sum(
                len(set(case["known_useful"]) - set(case["canonical_known_useful"]))
                for case in case_results
            ),
            "known_useful_top_15_recovered": sum(
                len(case["top_fifteen_known_useful"]) for case in case_results
            ),
            "known_useful_beyond_top_15": len(all_useful)
            - sum(len(case["top_fifteen_known_useful"]) for case in case_results),
            "relationship_candidates": aggregate["relationship_candidates"],
            "useful_relationship_candidates": aggregate[
                "useful_relationship_candidates"
            ],
            "not_useful_relationship_candidates": aggregate[
                "not_useful_relationship_candidates"
            ],
            "unjudged_relationship_candidates": aggregate[
                "unjudged_relationship_candidates"
            ],
            "useful_relationship_beyond_top_5": aggregate[
                "useful_relationship_beyond_top_5"
            ],
            "useful_relationship_beyond_top_15": aggregate[
                "useful_relationship_beyond_top_15"
            ],
            "limitation": "Recall is exact only over the frozen material surface; it does not assert that no useful repository resource exists outside that surface.",
        },
        "qualification": {
            "useful": aggregate["useful_qualified"],
            "not_useful": aggregate["not_useful_qualified"],
            "unjudged": aggregate["unjudged_qualified"],
        },
        "admission": {
            "total": aggregate["admissions"],
            "useful": aggregate["useful_admissions"],
            "not_useful": aggregate["not_useful_admissions"],
            "unjudged": aggregate["unjudged_admissions"],
            "precision": aggregate["useful_admissions"] / aggregate["admissions"],
            "conditional_recall_over_qualified_useful": aggregate[
                "useful_admissions"
            ]
            / aggregate["useful_qualified"],
        },
        "capacity": {
            "rank_five_displacements": aggregate["displacements"],
            "useful_displacements": aggregate["useful_displacements"],
            "not_useful_displacements": aggregate["not_useful_displacements"],
            "unjudged_displacements": aggregate["unjudged_displacements"],
            "useful_final_losses": aggregate["useful_displacements"],
            "rank_one_through_four_losses": 0,
        },
        "abstention": {
            "local_profile": aggregate["local_profile_abstentions"],
            "no_qualifying_target": aggregate["no_qualifying_target_abstentions"],
            "useful_qualified_during_abstention": 0,
            "demonstrably_inappropriate": 0,
        },
        "controls": {
            "historically_annotated": len(annotated_control_addresses),
            "validated_negative_after_review": len(active_control_addresses),
            "relationship_exposed": active_controls_exposed,
            "qualified": active_controls_qualified,
            "rejected": active_controls_qualified - active_controls_admitted,
            "admitted": active_controls_admitted,
            "unsupported_expectations": 1,
        },
        "oracle": {
            "state": "not-observed",
            "detail": "No oracle top-five view was retained for these six cases; oracle remains evaluation-only and no oracle metric is fabricated.",
        },
        "direct_resolution_controls": capture_payload[
            "direct_resolution_controls"
        ],
        "failure_localization": all_failures,
        "case_results": case_results,
        "disposition": {
            "directional_reservation_v1": "not-falsified-as-a-surfacing-idea-but-this-rule-realization-has-zero-net-known-useful-gain-and-one-useful-loss",
            "next_strategy": "Stop optimizing the single rank-five reservation rule; investigate stronger bounded candidate generation and purpose-relative ranking before shadow execution.",
            "shadow_mode": "NOT_READY_FOR_SHADOW",
            "shadow_rationale": "The frozen readiness gates fail: judgment coverage is incomplete, no validated negative control reached the relationship surface, one non-useful admission occurred, and one useful lexical rank-five resource was displaced.",
            "production_promotion": "NOT_JUSTIFIED",
            "production_behavior": _PRODUCTION_BEHAVIOR,
        },
    }
    report = artifact_envelope(schema=_REPORT_SCHEMA, payload=payload)
    validate_increment_23_report(report)
    return report


def validate_increment_23_report(report: dict[str, Any]) -> None:
    """Reject incomplete or semantically inconsistent retained reports."""
    if report.get("schema") != _REPORT_SCHEMA or not validate_artifact_envelope(report):
        msg = "Increment-23 report envelope or schema is invalid."
        raise ValueError(msg)
    payload = report["payload"]
    coverage = payload["judgment_coverage"]
    if (coverage["useful"], coverage["not_useful"], coverage["unjudged"], coverage["total"]) != (18, 68, 10, 96):
        msg = "Increment-23 report judgment totals differ from the frozen adjudication."
        raise ValueError(msg)
    if payload["control_conflict"]["disposition"] != "control-expectation-unsupported":
        msg = "Increment-23 conflict disposition is missing or changed."
        raise ValueError(msg)
    if payload["disposition"]["production_behavior"] != _PRODUCTION_BEHAVIOR:
        msg = "Increment-23 report must preserve unchanged production retrieval."
        raise ValueError(msg)
    if len(payload["case_results"]) != 6 or len(payload["direct_resolution_controls"]) != 2:
        msg = "Increment-23 report case or direct-control coverage is incomplete."
        raise ValueError(msg)


def write_increment_23_report(*, repository_root: Path) -> dict[str, Any]:
    """Write the final retained report from existing immutable artifacts."""
    report = build_increment_23_report(repository_root=repository_root)
    write_artifact(
        path=repository_root / ".b0002-purpose-relative-independent-validation.json",
        envelope=report,
    )
    return report


def _arm_case_metrics(
    *,
    case_name: str,
    addresses: tuple[str, ...],
    useful: set[str],
    unjudged: set[str],
    outside_material: set[str],
    cutoff: int,
) -> dict[str, Any]:
    address_set = set(addresses)
    known_recovered = useful & address_set
    unresolved_recovered = unjudged & address_set
    unresolved_missed = unjudged - address_set
    known_count = len(useful)
    lower_recall = len(known_recovered) / (known_count + len(unresolved_missed))
    upper_recall = (len(known_recovered) + len(unresolved_recovered)) / (
        known_count + len(unresolved_recovered)
    )
    known_first = next(
        (rank for rank, address in enumerate(addresses, start=1) if address in useful),
        None,
    )
    unresolved_first = next(
        (
            rank
            for rank, address in enumerate(addresses, start=1)
            if address in unjudged
        ),
        None,
    )
    mrr_lower = 0.0 if known_first is None else 1 / known_first
    possible_first = min(
        value for value in (known_first, unresolved_first) if value is not None
    ) if known_first is not None or unresolved_first is not None else None
    return {
        "case_name": case_name,
        "addresses": list(addresses),
        "known_useful_recovered": len(known_recovered),
        "known_useful_total": known_count,
        "unresolved_in_arm": len(unresolved_recovered),
        "outside_material_unresolved": len(outside_material),
        "cutoff": cutoff,
        "hit": {
            "lower": float(bool(known_recovered)),
            "upper": float(bool(known_recovered or unresolved_recovered)),
        },
        "recall": {"lower": lower_recall, "upper": upper_recall},
        "mrr": {
            "lower": mrr_lower,
            "upper": 0.0 if possible_first is None else 1 / possible_first,
        },
    }


def _aggregate_arm_metrics(cases: list[dict[str, Any]]) -> dict[str, Any]:
    count = len(cases)
    cutoffs = {case["cutoff"] for case in cases}
    if len(cutoffs) != 1:
        msg = "One comparison arm must use one cutoff."
        raise ValueError(msg)
    cutoff = next(iter(cutoffs))
    return {
        (f"{metric}_at_{cutoff}" if metric in {"hit", "recall"} else metric): {
            bound: sum(case[metric][bound] for case in cases) / count
            for bound in ("lower", "upper")
        }
        for metric in ("hit", "recall", "mrr")
    } | {
        "known_useful_recovered": sum(
            case["known_useful_recovered"] for case in cases
        ),
        "known_useful_total": sum(case["known_useful_total"] for case in cases),
        "outside_material_unresolved": sum(
            case["outside_material_unresolved"] for case in cases
        ),
    }


if __name__ == "__main__":
    generated = write_increment_23_report(repository_root=Path.cwd())
    print(
        json.dumps(
            {
                "schema": generated["schema"],
                "content_identity": generated["content_identity"],
                "disposition": generated["payload"]["disposition"],
            },
            indent=2,
        ),
    )
