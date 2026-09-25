# Copyright (c) 2026
# ruff: noqa: C901, COM812, E501, EM101, EM102, PLR0912, PLR0913, PLR0915, PLR2004, PERF401, TRY003
"""Increment-27 population freeze and canonical lexical-depth diagnostic."""

from __future__ import annotations

import hashlib
import json
import tempfile
from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING, cast

from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from experiments.increment_25.confirmation_judgments import (
    audit_frozen_confirmation_judgments,
)
from experiments.increment_25.development import (
    SnapshotCorpus,
    _build_snapshot_corpus,
    _materialize_git_snapshot,
    _task_card,
    write_artifact,
)
from experiments.increment_25.task_population import TaskCard, validate_freeze
from experiments.increment_26.development_judgments import (
    USEFULNESS_SEMANTICS,
    audit_frozen_development_judgments,
)
from experiments.purpose_relative_admission.validation_execution import (
    validate_artifact_envelope,
)

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

SCHEMA = "devtools-increment-27-depth-diagnostic-v1"
FREEZE_SCHEMA = "devtools-increment-27-protocol-population-freeze-v1"
K_CHECKPOINTS = (1, 3, 5, 10, 20, 50)
EXPECTED_DEVELOPMENT_SIZE = 24
EXPECTED_CONFIRMATION_SIZE = 14
I25_FREEZE_IDENTITY = "df4128bf1a6afc246aff072ff3922e4b9deb0205c95b74310a64d29497c02c0b"
I26_FREEZE_IDENTITY = "a8d57b68a8043b88300c8ea5f28d12266a1d74f7aa9e9a09e323a4c6ba9f22c1"


def canonical_json_bytes(value: object) -> bytes:
    """Serialize a JSON value deterministically using repository conventions."""
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def sha256_file(path: Path) -> str:
    """Return a file's SHA-256 without altering it."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_freeze(*, experiment_root: Path) -> dict[str, object]:
    """Freeze the 24 executed cards and 14 sealed cards from Increment 25."""
    i25_path = experiment_root / "increment_25" / "task_population_freeze.json"
    i26_path = experiment_root / "increment_26" / "experiment_freeze.json"
    i25 = _read_json(i25_path)
    i26 = _read_json(i26_path)
    if not validate_freeze(i25):
        raise ValueError("Increment-25 source population freeze failed validation.")
    if i25.get("content_identity") != I25_FREEZE_IDENTITY:
        raise ValueError(
            "Increment-25 population identity differs from the frozen source."
        )
    if i26.get("content_identity") != I26_FREEZE_IDENTITY:
        raise ValueError(
            "Increment-26 freeze identity differs from the suspended source."
        )
    i25_payload = cast("dict[str, object]", i25["payload"])
    i26_payload = cast("dict[str, object]", i26["payload"])
    split = cast("dict[str, list[str]]", i25_payload["split"])
    dev_ids = list(split["development_case_ids"])
    executed_confirmation_ids = list(split["confirmation_case_ids"])
    heldout_ids = list(split["reserve_case_ids"])
    if (
        len(dev_ids) != 8
        or len(executed_confirmation_ids) != 16
        or len(heldout_ids) != EXPECTED_CONFIRMATION_SIZE
    ):
        raise ValueError("Increment-25 source partition sizes do not match 8/16/14.")
    cards = cast("list[dict[str, object]]", i25_payload["task_cards"])
    cards_by_id = {str(item["case_id"]): item for item in cards}
    if len(cards_by_id) != 38 or set(cards_by_id) != set(
        dev_ids + executed_confirmation_ids + heldout_ids
    ):
        raise ValueError(
            "Increment-25 frozen task cards do not form the expected 38-card partition."
        )
    development_ids = dev_ids + executed_confirmation_ids
    suspended_i26_confirmation = cast("dict[str, object]", i26_payload["population"])
    suspended_ids = list(
        cast("list[str]", suspended_i26_confirmation["confirmation_case_ids"])
    )
    if suspended_ids != executed_confirmation_ids:
        raise ValueError("Suspended Increment-26 confirmation identity changed.")

    def card_record(case_id: str, *, heldout: bool = False) -> dict[str, object]:
        card = cards_by_id[case_id]
        return {
            "case_id": case_id,
            "source_commit_sha": card["source_commit_sha"],
            "parent_snapshot_sha": card["parent_snapshot_sha"],
            "information_need": {
                "purpose": card["information_need_purpose"],
                "lexical_query": card["lexical_query"],
            },
            "corpus_source_roots": card["corpus_source_roots"],
            "execution_status": "sealed-heldout-no-retrieval"
            if heldout
            else "previously-executed",
        }

    payload: dict[str, object] = {
        "source_population": {
            "increment_25_freeze_identity": I25_FREEZE_IDENTITY,
            "increment_25_freeze_sha256": sha256_file(i25_path),
            "increment_26_freeze_identity": I26_FREEZE_IDENTITY,
            "increment_26_freeze_sha256": sha256_file(i26_path),
            "development_cases": [card_record(case_id) for case_id in development_ids],
            "increment_25_source_partition": {
                "development_case_ids": dev_ids,
                "previously_executed_confirmation_case_ids": executed_confirmation_ids,
                "increment_27_heldout_confirmation_case_ids": heldout_ids,
            },
        },
        "preserved_suspended_increment_26_confirmation": {
            "case_ids": suspended_ids,
            "status": "preserved-suspended; not executed by Increment 27",
        },
        "increment_27_confirmation": {
            "case_ids": heldout_ids,
            "cards": [card_record(case_id, heldout=True) for case_id in heldout_ids],
            "status": "sealed; no retrieval outcomes or resource rankings included",
            "release_rule": "Do not execute or inspect retrieval outcomes until Increment-27 development diagnostic and any later protocol are frozen.",
        },
        "judgment_reuse": {
            "identity_rule": [
                "exact InformationNeed identity (purpose and frozen query text)",
                "exact parent snapshot identity",
                "exact repository resource address",
                "exact usefulness semantics",
            ],
            "usefulness_semantics": USEFULNESS_SEMANTICS,
            "unknown_rule": "UNJUDGED remains UNJUDGED and is never coerced to NOT_USEFUL.",
            "reuse_is_candidate_origin_independent": True,
        },
        "canonical_retrieval": {
            "identity": "devtools.context.retrieval.lexical.retrieve_repository_text_documents_by_bm25",
            "combination": "content BM25 + 0.25 * filename-stem BM25",
            "bm25_k1": 1.2,
            "bm25_b": 0.75,
            "query_serialization": "frozen task-card lexical_query exactly",
            "positive_results_only": True,
            "ordering": "descending combined score; canonical document order breaks ties",
            "result_limit": "all corpus addresses (max(1, corpus resource count))",
            "implementation_reuse": "Increment-25 _build_snapshot_corpus and canonical lexical query/retrieval operations; no retrieval implementation changes",
        },
        "diagnostic": {
            "k_checkpoints": list(K_CHECKPOINTS),
            "metric_terminology": "known-useful judged-pool depth counts; not exhaustive repository Recall@K",
            "unreachable": "a judged resource absent from all positive canonical lexical results",
            "beyond_50": "a known-useful resource with positive rank greater than 50",
        },
        "protocol_boundary": {
            "new_usefulness_judgments": False,
            "top_50_neutral_judgment_pool": False,
            "heldout_confirmation_execution": False,
            "other_increment_27_retrieval_hypotheses_tested": [],
        },
    }
    return {
        "schema": FREEZE_SCHEMA,
        "content_identity": _digest(payload),
        "payload": payload,
    }


def load_existing_judgments(
    *, experiment_root: Path, cards: Mapping[str, TaskCard]
) -> dict[str, list[dict[str, object]]]:
    """Join frozen labels to exact development identities or reject mismatch."""
    results: dict[str, list[dict[str, object]]] = {case_id: [] for case_id in cards}
    i25_input = _read_json(
        experiment_root / "increment_25" / "confirmation_judgment_input.json"
    )
    i25_judged = _read_json(
        experiment_root / "increment_25" / "confirmation_frozen_judgments.json"
    )
    i25_mapping = _read_json(
        experiment_root / "increment_25" / "confirmation_neutral_mapping.json"
    )
    audit_frozen_confirmation_judgments(i25_judged)
    if not validate_artifact_envelope(i25_mapping):
        raise ValueError("Increment-25 neutral judgment mapping identity is invalid.")
    judged_payload = cast("dict[str, object]", i25_judged["payload"])
    mapping_payload = cast("dict[str, object]", i25_mapping["payload"])
    if (
        judged_payload["blinded_package_identity"]
        != mapping_payload["blinded_package_identity"]
    ):
        raise ValueError(
            "Increment-25 judgments and neutral mapping bind to different blinded inputs."
        )
    i25_cases = _case_maps(i25_input)
    judged_cases = _payload_case_maps(i25_judged)
    mapping_cases = _payload_case_maps(i25_mapping)
    if set(i25_cases) != set(judged_cases) or set(i25_cases) != set(mapping_cases):
        raise ValueError(
            "Increment-25 confirmation judgment artifacts have different case populations."
        )
    for case_id, blind_case in i25_cases.items():
        card = cards.get(case_id)
        if card is None:
            raise ValueError(f"Unexpected Increment-25 judgment case: {case_id}.")
        _check_case_identity(blind_case, card)
        mappings = cast("list[dict[str, object]]", mapping_cases[case_id]["mappings"])
        source_records = cast(
            "list[dict[str, object]]", judged_cases[case_id]["records"]
        )
        address_by_neutral = {
            str(item["neutral_id"]): str(item["address"]) for item in mappings
        }
        records_by_neutral = {str(item["neutral_id"]): item for item in source_records}
        if len(address_by_neutral) != len(mappings) or len(records_by_neutral) != len(
            source_records
        ):
            raise ValueError(
                f"Increment-25 neutral judgment identities repeat in {case_id}."
            )
        blind_resources = cast("list[dict[str, object]]", blind_case["resources"])
        blind_addresses = {str(item["address"]) for item in blind_resources}
        if set(address_by_neutral.values()) != blind_addresses:
            raise ValueError(
                f"Increment-25 judgment addresses do not match blinded resources in {case_id}."
            )
        if set(address_by_neutral) != set(records_by_neutral):
            raise ValueError(
                f"Increment-25 judgment mapping is incomplete for {case_id}."
            )
        for neutral_id, record in records_by_neutral.items():
            address = address_by_neutral[neutral_id]
            if not prior_judgment_matches(
                card=card,
                prior_information_need=cast("dict[str, object]", blind_case["task"]),
                prior_parent_snapshot=str(
                    cast("dict[str, object]", blind_case["task"])["parent_snapshot_sha"]
                ),
                prior_address=address,
                resource_address=address,
                prior_usefulness_semantics=USEFULNESS_SEMANTICS,
            ):
                raise ValueError(
                    f"Increment-25 judgment identity mismatch for {case_id}/{address}."
                )
            results[case_id].append(
                _judgment_record(
                    card, address, str(record["judgment"]), "increment-25-confirmation"
                )
            )

    i26_input = _read_json(
        experiment_root / "increment_26" / "development_judgment_input.json"
    )
    i26_judged = _read_json(
        experiment_root / "increment_26" / "development_frozen_judgments.json"
    )
    audit_frozen_development_judgments(
        i26_judged,
        blinded_bytes=(
            experiment_root / "increment_26" / "development_judgment_input.json"
        ).read_bytes(),
    )
    i26_cases = _case_maps(i26_input)
    i26_judged_cases = _payload_case_maps(i26_judged)
    if set(i26_cases) != set(i26_judged_cases):
        raise ValueError(
            "Increment-26 development judgment artifacts have different case populations."
        )
    for case_id, blind_case in i26_cases.items():
        card = cards.get(case_id)
        if card is None:
            raise ValueError(f"Unexpected Increment-26 judgment case: {case_id}.")
        _check_case_identity(blind_case, card)
        records = cast("list[dict[str, object]]", i26_judged_cases[case_id]["records"])
        resource_records = cast("list[dict[str, object]]", blind_case["resources"])
        allowed_addresses = {str(item["address"]) for item in resource_records}
        if len(allowed_addresses) != len(resource_records):
            raise ValueError(
                f"Increment-26 blinded resource identities repeat in {case_id}."
            )
        for record in records:
            address = str(record["address"])
            if address not in allowed_addresses:
                raise ValueError(
                    f"Increment-26 judgment is outside its exact blinded pair in {case_id}: {address}."
                )
            if not prior_judgment_matches(
                card=card,
                prior_information_need=cast("dict[str, object]", blind_case["task"]),
                prior_parent_snapshot=str(
                    cast("dict[str, object]", blind_case["task"])["parent_snapshot_sha"]
                ),
                prior_address=address,
                resource_address=address,
                prior_usefulness_semantics=USEFULNESS_SEMANTICS,
            ):
                raise ValueError(
                    f"Increment-26 judgment identity mismatch for {case_id}/{address}."
                )
            results[case_id].append(
                _judgment_record(
                    card,
                    address,
                    str(record["judgment"]),
                    "increment-26-development",
                )
            )
    for case_id, records in results.items():
        identities = [
            (str(record["address"]), str(record["judgment_semantics"]))
            for record in records
        ]
        if len(identities) != len(set(identities)):
            # Same pair may be retained in both sources only after exact identity checks.
            by_address: dict[str, set[str]] = {}
            for address, state in identities:
                by_address.setdefault(address, set()).add(state)
            if any(len(states) > 1 for states in by_address.values()):
                raise ValueError(f"Conflicting prior judgments found for {case_id}.")
            records[:] = _deduplicate_exact(records)
    return results


def build_depth_case(
    *,
    case_id: str,
    parent_snapshot_sha: str,
    query_text: str,
    rankings: Sequence[Mapping[str, object]],
    judgments: Sequence[Mapping[str, object]],
    k_checkpoints: Sequence[int] = K_CHECKPOINTS,
) -> dict[str, object]:
    """Build explicit per-case known-judgment depth counts without new labels."""
    rank_by_address = {
        str(item["address"]): int(cast("int", item["rank"])) for item in rankings
    }
    if len(rank_by_address) != len(rankings) or list(rank_by_address.values()) != list(
        range(1, len(rankings) + 1)
    ):
        raise ValueError(
            "Positive lexical ranking must contain unique addresses and contiguous complete ranks."
        )
    judgment_addresses: set[str] = set()
    judged: list[dict[str, object]] = []
    for item in judgments:
        address = str(item["address"])
        if address in judgment_addresses:
            raise ValueError(f"Duplicate judgment identity in {case_id}: {address}.")
        judgment_addresses.add(address)
        state = str(item["judgment"])
        if state not in {"useful", "not-useful", "unjudged"}:
            raise ValueError(f"Unknown three-state usefulness value: {state}.")
        rank = rank_by_address.get(address)
        judged.append(
            {
                **dict(item),
                "positive_lexical_rank": rank,
                "positive_rank_state": "ranked"
                if rank is not None
                else "absent-from-positive-results",
            }
        )
    useful = [item for item in judged if item["judgment"] == "useful"]
    checkpoints = [
        {
            "requested_k": k,
            "effective_k": min(k, len(rankings)),
            "known_useful_count": sum(
                item["positive_lexical_rank"] is not None
                and int(cast("int", item["positive_lexical_rank"]))
                <= min(k, len(rankings))
                for item in useful
            ),
        }
        for k in k_checkpoints
    ]
    useful_ranks = [
        int(cast("int", item["positive_lexical_rank"]))
        for item in useful
        if item["positive_lexical_rank"] is not None
    ]
    no_positive = [
        item["address"] for item in useful if item["positive_lexical_rank"] is None
    ]
    first_rank = min(useful_ranks) if useful_ranks else None
    return {
        "case_id": case_id,
        "parent_snapshot_sha": parent_snapshot_sha,
        "query_text": query_text,
        "positive_lexical_result_count": len(rankings),
        "judged_resources": judged,
        "known_useful_count": len(useful),
        "first_known_useful_rank": first_rank,
        "known_useful_reached_by_k": checkpoints,
        "known_useful_beyond_50": [
            item["address"]
            for item in useful
            if item["positive_lexical_rank"] is not None
            and int(cast("int", item["positive_lexical_rank"])) > 50
        ],
        "known_useful_without_positive_rank": no_positive,
        "unjudged_identities": [
            item["address"] for item in judged if item["judgment"] == "unjudged"
        ],
    }


def build_summary(*, cases: Sequence[Mapping[str, object]]) -> dict[str, object]:
    """Aggregate known-useful ranks and first-known-useful categories."""
    useful_ranks: list[int | None] = []
    first_categories = Counter[str]()
    cases_without_useful = 0
    for case in cases:
        resources = cast("list[dict[str, object]]", case["judged_resources"])
        useful = [item for item in resources if item["judgment"] == "useful"]
        useful_ranks.extend(
            cast("int | None", item["positive_lexical_rank"]) for item in useful
        )
        if not useful:
            cases_without_useful += 1
            category = "no-known-useful-resource"
        else:
            rank = case["first_known_useful_rank"]
            if rank is None:
                category = "unreachable"
            elif int(cast("int", rank)) <= 5:
                category = "<=5"
            elif int(cast("int", rank)) <= 10:
                category = "6-10"
            elif int(cast("int", rank)) <= 20:
                category = "11-20"
            elif int(cast("int", rank)) <= 50:
                category = "21-50"
            else:
                category = ">50"
        first_categories[category] += 1
    total_useful = len(useful_ranks)
    judgment_counts = Counter(
        str(item["judgment"])
        for case in cases
        for item in cast("list[dict[str, object]]", case["judged_resources"])
    )
    checkpoints = []
    for k in K_CHECKPOINTS:
        reached = sum(rank is not None and rank <= k for rank in useful_ranks)
        checkpoints.append(
            {
                "k": k,
                "known_useful_reached": reached,
                "total_known_useful": total_useful,
            }
        )
    distribution = Counter[str]()
    for rank in useful_ranks:
        if rank is None:
            distribution["unreachable"] += 1
        elif rank <= 5:
            distribution["1-5"] += 1
        elif rank <= 10:
            distribution["6-10"] += 1
        elif rank <= 20:
            distribution["11-20"] += 1
        elif rank <= 50:
            distribution["21-50"] += 1
        else:
            distribution[">50"] += 1
    return {
        "case_count": len(cases),
        "total_known_useful_pairs": total_useful,
        "existing_judgment_counts": {
            state: judgment_counts[state]
            for state in ("useful", "not-useful", "unjudged")
        },
        "known_useful_rank_distribution": {
            key: distribution[key]
            for key in ("1-5", "6-10", "11-20", "21-50", ">50", "unreachable")
        },
        "known_useful_reached_by_k": checkpoints,
        "known_useful_beyond_50": distribution[">50"],
        "known_useful_unreachable_by_positive_lexical_retrieval": distribution[
            "unreachable"
        ],
        "cases_with_no_known_useful_resource": cases_without_useful,
        "first_known_useful_rank_case_distribution": {
            key: first_categories[key]
            for key in (
                "<=5",
                "6-10",
                "11-20",
                "21-50",
                ">50",
                "unreachable",
                "no-known-useful-resource",
            )
        },
        "metric_caveat": "Judged-pool depth diagnostics only; these counts are not exhaustive repository Recall@K.",
    }


def run_diagnostic(
    *, repository_root: Path, experiment_root: Path, output_root: Path
) -> tuple[dict[str, object], dict[str, object], dict[str, object], dict[str, object]]:
    """Execute the unchanged canonical lexical baseline for exactly 24 cases."""
    freeze = build_freeze(experiment_root=experiment_root)
    payload = cast(
        "dict[str, object]",
        cast("dict[str, object]", freeze["payload"])["source_population"],
    )
    case_records = cast("list[dict[str, object]]", payload["development_cases"])
    cards: dict[str, TaskCard] = {}
    task_freeze = _read_json(
        experiment_root / "increment_25" / "task_population_freeze.json"
    )
    task_payload = cast("dict[str, object]", task_freeze["payload"])
    task_cards = cast("list[dict[str, object]]", task_payload["task_cards"])
    for item in task_cards:
        card = _task_card(item)
        if card.case_id in {str(case["case_id"]) for case in case_records}:
            cards[card.case_id] = card
    if len(cards) != EXPECTED_DEVELOPMENT_SIZE:
        raise ValueError("Could not load exactly 24 Increment-27 development cards.")
    judgments_by_case = load_existing_judgments(
        experiment_root=experiment_root, cards=cards
    )
    rankings: list[dict[str, object]] = []
    diagnostics: list[dict[str, object]] = []
    prior_checks = _prior_lexical_rank_checks(experiment_root=experiment_root)
    for case_record in case_records:
        case_id = str(case_record["case_id"])
        card = cards[case_id]
        with tempfile.TemporaryDirectory(prefix=f"devtools-i27-{case_id}-") as raw:
            snapshot_root = Path(raw)
            _materialize_git_snapshot(
                repository_root=repository_root,
                snapshot_sha=card.parent_snapshot_sha,
                source_roots=card.corpus_source_roots,
                destination=snapshot_root,
            )
            corpus = _build_snapshot_corpus(
                snapshot_root=snapshot_root, source_roots=card.corpus_source_roots
            )
            ranking = _rank_case(card=card, corpus=corpus)
        rankings.append(ranking)
        depth = build_depth_case(
            case_id=case_id,
            parent_snapshot_sha=card.parent_snapshot_sha,
            query_text=card.lexical_query,
            rankings=cast(
                "list[dict[str, object]]", ranking["positive_lexical_ordering"]
            ),
            judgments=judgments_by_case[case_id],
        )
        diagnostics.append(depth)
    prior_rank_agreement = _assert_prior_ranks_agree(
        rankings=rankings, prior_checks=prior_checks
    )
    summary = build_summary(cases=diagnostics)
    ranking_artifact = {
        "schema": "devtools-increment-27-canonical-positive-lexical-rankings-v1",
        "freeze_identity": freeze["content_identity"],
        "prior_rank_agreement": prior_rank_agreement,
        "cases": rankings,
    }
    diagnostic_artifact = {
        "schema": SCHEMA,
        "freeze_identity": freeze["content_identity"],
        "judgment_sources": _judgment_source_identities(experiment_root),
        "cases": diagnostics,
    }
    summary_artifact = {
        "schema": "devtools-increment-27-development-depth-summary-v1",
        "freeze_identity": freeze["content_identity"],
        "summary": summary,
    }
    output_root.mkdir(parents=True, exist_ok=True)
    write_artifact(path=output_root / "experiment_freeze.json", payload=freeze)
    write_artifact(
        path=output_root / "canonical_positive_lexical_rankings.json",
        payload=ranking_artifact,
    )
    write_artifact(
        path=output_root / "existing_judgment_depth_diagnostics.json",
        payload=diagnostic_artifact,
    )
    write_artifact(
        path=output_root / "development_depth_summary.json", payload=summary_artifact
    )
    return freeze, ranking_artifact, diagnostic_artifact, summary_artifact


def _rank_case(*, card: TaskCard, corpus: SnapshotCorpus) -> dict[str, object]:
    query = analyze_repository_text_lexical_query(text=card.lexical_query)
    retrieved = retrieve_repository_text_documents_by_bm25(
        query=query, index=corpus.index, maximum_results=max(1, len(corpus.addresses))
    )
    positive = [
        {
            "rank": rank,
            "address": str(
                match.document_statistics.analysis.document.resource.address
            ),
            "score": match.score,
        }
        for rank, match in enumerate(retrieved.matches, start=1)
    ]
    return {
        "case_id": card.case_id,
        "parent_snapshot_sha": card.parent_snapshot_sha,
        "source_commit_sha": card.source_commit_sha,
        "information_need": {
            "purpose": card.information_need_purpose,
            "lexical_query": card.lexical_query,
        },
        "corpus_resource_count": len(corpus.addresses),
        "positive_result_count": len(positive),
        "positive_lexical_ordering": positive,
    }


def _prior_lexical_rank_checks(*, experiment_root: Path) -> list[dict[str, object]]:
    checks: list[dict[str, object]] = []
    for filename in (
        "development_candidate_evidence.json",
        "confirmation_candidate_evidence.json",
    ):
        path = experiment_root / "increment_25" / filename
        artifact = _read_json(path)
        for case in cast("list[dict[str, object]]", artifact["cases"]):
            checks.append(
                {
                    "case_id": case["case_id"],
                    "source": f"increment-25/{filename}",
                    "ranked": case["positive_lexical_ordering"],
                }
            )
    i26 = _read_json(
        experiment_root / "increment_26" / "development_candidate_evidence.json"
    )
    for case in cast("list[dict[str, object]]", i26["cases"]):
        checks.append(
            {
                "case_id": case["case_id"],
                "source": "increment-26/development_candidate_evidence.json",
                "ranked": [
                    {"address": item["address"], "rank": item["positive_lexical_rank"]}
                    for item in cast(
                        "list[dict[str, object]]", case["semantic_candidates"]
                    )
                ],
            }
        )
    return checks


def _assert_prior_ranks_agree(
    *,
    rankings: Sequence[Mapping[str, object]],
    prior_checks: Sequence[Mapping[str, object]],
) -> dict[str, int | str]:
    actual_by_case = {
        str(case["case_id"]): cast(
            "list[dict[str, object]]", case["positive_lexical_ordering"]
        )
        for case in rankings
    }
    checked_entries = 0
    for prior in prior_checks:
        case_id = str(prior["case_id"])
        actual = actual_by_case.get(case_id)
        if actual is None:
            raise ValueError(
                f"Retained lexical ranks exist for unknown development case {case_id}."
            )
        actual_ranks = {
            str(item["address"]): int(cast("int", item["rank"])) for item in actual
        }
        for retained in cast("list[dict[str, object]]", prior["ranked"]):
            checked_entries += 1
            address = str(retained["address"])
            rank_value = retained.get("rank", retained.get("positive_lexical_rank"))
            if rank_value is None:
                if address in actual_ranks:
                    raise ValueError(
                        f"Prior artifact says no positive rank but canonical result contains {case_id}/{address}."
                    )
            elif actual_ranks.get(address) != int(cast("int", rank_value)):
                raise ValueError(
                    f"Canonical lexical rank mismatch for {case_id}/{address}: prior={rank_value}, recomputed={actual_ranks.get(address)}."
                )
            if "score" in retained and rank_value is not None:
                actual_item = actual[int(cast("int", rank_value)) - 1]
                if float(cast("float", actual_item["score"])) != float(
                    cast("float", retained["score"])
                ):
                    raise ValueError(
                        f"Canonical lexical score mismatch for {case_id}/{address}."
                    )
    return {
        "status": "all retained ranks and available scores agree",
        "prior_artifact_case_checks": len(prior_checks),
        "retained_resource_rank_checks": checked_entries,
    }


def _judgment_record(
    card: TaskCard, address: str, judgment: str, source: str
) -> dict[str, object]:
    if judgment not in {"useful", "not-useful", "unjudged"}:
        raise ValueError(f"Unsupported prior usefulness state: {judgment}.")
    return {
        "address": address,
        "judgment": judgment,
        "judgment_semantics": USEFULNESS_SEMANTICS,
        "source": source,
        "information_need_identity": {
            "purpose": card.information_need_purpose,
            "lexical_query": card.lexical_query,
        },
        "parent_snapshot_sha": card.parent_snapshot_sha,
    }


def prior_judgment_matches(
    *,
    card: TaskCard,
    prior_information_need: Mapping[str, object],
    prior_parent_snapshot: str,
    prior_address: str,
    resource_address: str,
    prior_usefulness_semantics: str,
) -> bool:
    """Require exact InformationNeed, snapshot, address, and label semantics."""
    return (
        prior_information_need.get("purpose") == card.information_need_purpose
        and prior_information_need.get("lexical_query") == card.lexical_query
        and prior_parent_snapshot == card.parent_snapshot_sha
        and prior_address == resource_address
        and bool(resource_address)
        and prior_usefulness_semantics == USEFULNESS_SEMANTICS
    )


def _check_case_identity(blind_case: Mapping[str, object], card: TaskCard) -> None:
    task = cast("dict[str, object]", blind_case["task"])
    expected = {
        "purpose": card.information_need_purpose,
        "lexical_query": card.lexical_query,
    }
    actual = {"purpose": task["purpose"], "lexical_query": task["lexical_query"]}
    if (
        str(blind_case["case_id"]) != card.case_id
        or actual != expected
        or task["parent_snapshot_sha"] != card.parent_snapshot_sha
    ):
        raise ValueError(
            f"Prior judgment fails exact InformationNeed/snapshot identity for {card.case_id}."
        )


def _deduplicate_exact(records: list[dict[str, object]]) -> list[dict[str, object]]:
    output: dict[str, dict[str, object]] = {}
    for item in records:
        address = str(item["address"])
        if address in output and output[address]["judgment"] != item["judgment"]:
            raise ValueError(
                f"Conflicting judgments for exact resource identity {address}."
            )
        output[address] = item
    return list(output.values())


def _case_maps(document: Mapping[str, object]) -> dict[str, dict[str, object]]:
    return {
        str(case["case_id"]): case
        for case in cast("list[dict[str, object]]", document["cases"])
    }


def _payload_case_maps(document: Mapping[str, object]) -> dict[str, dict[str, object]]:
    payload = cast("dict[str, object]", document["payload"])
    return {
        str(case["case_id"]): case
        for case in cast("list[dict[str, object]]", payload["cases"])
    }


def _judgment_source_identities(experiment_root: Path) -> dict[str, str]:
    names = {
        "increment_25_confirmation_judgments": "increment_25/confirmation_frozen_judgments.json",
        "increment_25_neutral_mapping": "increment_25/confirmation_neutral_mapping.json",
        "increment_26_development_judgments": "increment_26/development_frozen_judgments.json",
    }
    return {name: sha256_file(experiment_root / path) for name, path in names.items()}


def _read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"Expected JSON object in {path}.")
    return cast("dict[str, object]", value)


def _digest(value: object) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()
