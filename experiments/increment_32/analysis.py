# Copyright (c) 2026
# ruff: noqa: COM812, E501, EM101, PLR2004, TRY003
"""Join frozen sampled Graph-1 outcomes without labeling unsampled pairs."""

from __future__ import annotations

import math
from collections import Counter
from typing import TYPE_CHECKING, Any

from experiments.increment_25.development import write_artifact
from experiments.increment_26.development_judgments import USEFULNESS_SEMANTICS
from experiments.increment_27.depth_diagnostic import _read_json, sha256_file
from experiments.increment_27.structural_imports.mechanics import _digest
from experiments.increment_30.mechanics import _verified_json
from experiments.increment_32.judgments import JUDGMENTS_NAME, build_judgments
from experiments.increment_32.mechanics import (
    CANDIDATES_NAME,
    FREEZE_NAME,
    ROOT,
    build_freeze,
)
from experiments.increment_32.population import BLINDED_NAME, JUDGMENT_FREEZE_NAME
from experiments.increment_32.sampling import (
    FREEZE_NAME as SAMPLING_FREEZE_NAME,
)
from experiments.increment_32.sampling import (
    SAMPLED_INPUT_NAME,
    build_sample,
)
from experiments.retrieval_judgment_coverage import (
    judgment_identity,
    validate_frozen_judgment_coverage,
    validate_neutral_target_coverage,
    validated_outcome_mappings,
)

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

SOURCE_SHA256 = {
    FREEZE_NAME: "4869d561b9cf2b50665102f775f0d2d450b52db7e75bfa576e2ddb42911412f9",
    CANDIDATES_NAME: "b8cb242dc0ff3d9184bcd14da2572864806f8986390ffe8000d4ff9a4e9fba0a",
    JUDGMENT_FREEZE_NAME: "a461d48a3c33dcfcbb1f8a1ab3a6174d1ce9c3a8d06710fb67ddc8803538dd5e",
    BLINDED_NAME: "2721f737aff1bc0d266f767dcbb49ab623bc1b2d7c19c05aec4ef55a89b603b9",
    SAMPLING_FREEZE_NAME: "1b1b113a17939a5cadfbe731c4282d756b5835422de99845207e06789e03d00d",
    SAMPLED_INPUT_NAME: "dc922555365307e8146c00ae5bda2c646372badbc45574dbbd30c707d4190949",
    JUDGMENTS_NAME: "5406ecf910664a6fe347cd5f23269bcce9a7f61718b2cfeb89832a0366cdde5c",
}
RESULT_NAME = "graph_round_one_development_results.json"
STATES = ("USEFUL", "NOT_USEFUL", "UNJUDGED")


def _wilson_interval(successes: int, n: int) -> dict[str, Any]:
    """Compute a descriptive 95% Wilson interval without finite-population correction."""
    z = 1.959963984540054
    fraction = successes / n
    denominator = 1 + z * z / n
    center = (fraction + z * z / (2 * n)) / denominator
    radius = (
        z * math.sqrt(fraction * (1 - fraction) / n + z * z / (4 * n * n)) / denominator
    )
    return {
        "method": "Wilson score 95% binomial approximation",
        "finite_population_correction": False,
        "interpretation": "descriptive uncertainty for the useful proportion of the 702 frozen unresolved pairs; simple random sampling without replacement",
        "sampled_fraction": fraction,
        "lower": max(0.0, center - radius),
        "upper": min(1.0, center + radius),
    }


def _candidate_summary(candidate: Mapping[str, Any]) -> dict[str, Any]:
    combinations = Counter(
        f"{path['first_relation']['family']}:{path['first_relation']['direction']} -> {path['second_relation']['family']}:{path['second_relation']['direction']}"
        for path in candidate["paths"]
    )
    return {
        "support_count": candidate["support_count"],
        "path_combinations": dict(sorted(combinations.items())),
    }


def build_results(root: Path = ROOT) -> dict[str, Any]:
    """Join exactly the frozen 128 sampled and two reused judgments."""
    sources = {name: _verified_json(root / name) for name in SOURCE_SHA256}
    if any(
        sha256_file(root / name) != expected for name, expected in SOURCE_SHA256.items()
    ):
        raise ValueError("Graph-1 source artifact hash changed before outcome join.")
    protocol = sources[FREEZE_NAME]
    candidates = sources[CANDIDATES_NAME]
    population = sources[JUDGMENT_FREEZE_NAME]["payload"]
    sampling = sources[SAMPLING_FREEZE_NAME]
    sampled_input = sources[SAMPLED_INPUT_NAME]
    judgments = sources[JUDGMENTS_NAME]["payload"]
    if (
        protocol != build_freeze(root)
        or (sampling, sampled_input) != build_sample(root)
        or sources[JUDGMENTS_NAME] != build_judgments(root)
        or candidates["freeze_identity"] != protocol["content_identity"]
        or candidates["judgments_loaded"]
        or candidates["heldout_executed"]
        or population["candidate_identity"] != candidates["content_identity"]
        or population["candidate_sha256"] != SOURCE_SHA256[CANDIDATES_NAME]
        or population["blinded_input_identity"]
        != sources[BLINDED_NAME]["content_identity"]
        or sampling["payload"]["sampled_input_content_identity"]
        != sampled_input["content_identity"]
        or judgments["sampled_input_content_identity"]
        != sampled_input["content_identity"]
        or judgments["usefulness_semantics"] != USEFULNESS_SEMANTICS
        or set(judgments["three_states"]) != set(STATES)
    ):
        raise ValueError(
            "Graph-1 frozen candidate, sample, and judgment bindings differ."
        )
    if (
        len(candidates["cases"]) != 24
        or candidates["summary"]["candidate_pairs"] != 704
    ):
        raise ValueError("Complete Graph-1 development surface differs.")
    selected = {
        tuple(identity)
        for identity in sampling["payload"]["sampled_neutral_identities"]
    }
    unsampled = {
        tuple(identity)
        for identity in sampling["payload"]["unsampled_neutral_identities"]
    }
    unresolved = population["new_judgment_pairs"]
    frozen_targets = validate_neutral_target_coverage(unresolved)
    if (
        len(frozen_targets) != 702
        or len(selected) != 128
        or len(unsampled) != 574
        or selected & unsampled
        or selected | unsampled != set(frozen_targets)
    ):
        raise ValueError(
            "Graph-1 sampled and unsampled frames do not partition 702 targets."
        )
    targets = [
        row
        for row in unresolved
        if (row["neutral_case_id"], row["neutral_resource_id"]) in selected
    ]
    sampled = validate_frozen_judgment_coverage(
        targets, judgments["records"], STATES, selected
    )
    reused, sampled = validated_outcome_mappings(
        population["reused_judgments"], sampled
    )
    if len(reused) != 2 or len(sampled) != 128:
        raise ValueError("Graph-1 exact outcome populations differ.")
    all_candidates = {
        judgment_identity(
            {
                "information_need": case["information_need"],
                "parent_snapshot_sha": case["parent_snapshot_sha"],
                "address": candidate["address"],
                "usefulness_semantics": USEFULNESS_SEMANTICS,
            }
        ): (case, candidate)
        for case in candidates["cases"]
        for candidate in case["candidates"]
    }
    if len(all_candidates) != 704 or not set(reused) | set(sampled) <= set(
        all_candidates
    ):
        raise ValueError("Frozen judgments do not map to unique Graph-1 candidates.")
    sampled_rows: list[dict[str, Any]] = []
    reused_rows: list[dict[str, Any]] = []
    for identity, decision in sampled.items():
        case, candidate = all_candidates[identity]
        sampled_rows.append(
            {
                "case_id": case["case_id"],
                "information_need": case["information_need"],
                "parent_snapshot_sha": case["parent_snapshot_sha"],
                "address": candidate["address"],
                "judgment": decision["judgment"],
                "judgment_origin": "probability-sample-blinded",
                **_candidate_summary(candidate),
            }
        )
    for identity, decision in reused.items():
        case, candidate = all_candidates[identity]
        reused_rows.append(
            {
                "case_id": case["case_id"],
                "parent_snapshot_sha": case["parent_snapshot_sha"],
                "address": candidate["address"],
                "judgment": decision["judgment"],
                "judgment_origin": "exact-reuse",
                "judgment_source": decision["source"],
            }
        )
    sampled_rows.sort(key=lambda row: (str(row["case_id"]), str(row["address"])))
    reused_rows.sort(key=lambda row: (str(row["case_id"]), str(row["address"])))
    counts = Counter(row["judgment"] for row in sampled_rows)
    useful = [row for row in sampled_rows if row["judgment"] == "USEFUL"]
    payload = {
        "schema": "devtools-i32-graph-round-one-development-results-v1",
        "source_content_identities": {
            name: source["content_identity"] for name, source in sources.items()
        },
        "source_sha256": SOURCE_SHA256,
        "development_case_ids": protocol["payload"]["development_case_ids"],
        "confirmation_executed": False,
        "candidate_mechanics_changed": False,
        "sampling_method": sampling["payload"]["sampling_method"],
        "sampling_seed": sampling["payload"]["seed"],
        "usefulness_semantics": USEFULNESS_SEMANTICS,
        "population_counts": {
            "complete_novel_candidate_pairs": 704,
            "exact_reused": len(reused_rows),
            "new_sampled_adjudicated": len(sampled_rows),
            "unsampled_unadjudicated": len(unsampled),
            "sampled_states": {state: counts[state] for state in STATES},
            "reused_states": {
                state: sum(row["judgment"] == state for row in reused_rows)
                for state in STATES
            },
        },
        "sampled_useful_proportion": _wilson_interval(
            counts["USEFUL"], len(sampled_rows)
        ),
        "sampled_pairs": sampled_rows,
        "reused_pairs": reused_rows,
        "sampled_useful_pairs": useful,
        "unsampled_semantic_judgments_assigned": False,
        "complete_outcome_coverage_claimed": False,
        "breadth_verdict": "sampled useful complementary reach established"
        if useful
        else "no useful candidate observed in the probability sample",
        "outcome_free_reach_and_cost": candidates["summary"],
    }
    return {
        "schema": payload["schema"],
        "content_identity": _digest(payload),
        "payload": payload,
    }


def write_results(root: Path = ROOT) -> dict[str, Any]:
    """Persist the completed sampled development result without fabricating labels."""
    result = build_results(root)
    path = root / RESULT_NAME
    if path.exists() and _read_json(path) != result:
        raise ValueError("Existing Graph-1 sampled development result differs.")
    write_artifact(path=path, payload=result)
    return result


if __name__ == "__main__":
    write_results()
