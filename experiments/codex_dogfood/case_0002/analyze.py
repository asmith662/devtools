# Copyright (c) 2026
# ruff: noqa: T201, S101
"""Recompute the Case 0002 provenance join after the immutable blind freeze."""

from __future__ import annotations

import gzip
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any, cast

from devtools.evaluation.coverage import compare_identity_coverage

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
EXPECTED_RESOURCE_COUNT = 302
DEPTHS = (5, 10, 20, 30, 50, 100)


def read_json(path: Path) -> dict[str, Any]:
    """Read one retained case artifact."""
    return cast("dict[str, Any]", json.loads(path.read_text(encoding="utf-8-sig")))


def digest(path: Path) -> str:
    """Return an artifact's exact byte identity."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_text_digest(path: Path) -> str:
    """Match pre-write LF text hashes despite Windows text-mode CRLF storage."""
    return hashlib.sha256(path.read_text(encoding="utf-8").encode()).hexdigest()


def role(address: str, judgments: dict[str, dict[str, Any]]) -> str:
    """Classify one observed eligible address using only frozen judgments."""
    if address not in judgments:
        return "outside_eligible_frame"
    states = judgments[address]["states"]
    if any(state.startswith("required_") for state in states):
        return "required"
    return cast("str", states[0])


def arm_result(
    entries: list[dict[str, Any]],
    required: set[str],
    judgments: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Account for all required resources at every native lexical depth."""
    by_address = {entry["address"]: entry for entry in entries}
    assert len(by_address) == len(entries)
    ranks = [
        entry["lexical_rank"] for entry in entries if entry["lexical_rank"] is not None
    ]
    assert sorted(ranks) == list(range(1, len(ranks) + 1))
    for entry in entries:
        if entry["lexical_rank"] is None:
            continue
        assert math.isclose(
            entry["lexical_score"],
            entry["content_score"] + entry["weighted_filename_score"],
        )
        assert math.isclose(
            entry["content_score"],
            sum(item["contribution"] for item in entry["content_term_contributions"]),
        )
        assert math.isclose(
            entry["filename_score"],
            sum(item["contribution"] for item in entry["filename_term_contributions"]),
        )
    present = required & by_address.keys()
    lexical_required = {a for a in present if by_address[a]["lexical_rank"] is not None}
    structural_required = {a for a in present if by_address[a]["structural_supports"]}
    complete_depth = (
        max(by_address[a]["lexical_rank"] for a in required)
        if lexical_required == required
        else None
    )
    count_before = {
        state: sum(
            role(entry["address"], judgments) == state
            for entry in entries
            if complete_depth is not None
            and entry["lexical_rank"] is not None
            and entry["lexical_rank"] <= complete_depth
        )
        for state in ("required", "helpful_only", "unnecessary", "unresolved")
    }
    curves = {}
    for depth in DEPTHS:
        count = sum(
            by_address[address]["lexical_rank"] <= depth
            for address in lexical_required
        )
        curves[str(depth)] = f"{count}/{len(required)}"
    curves["complete"] = f"{len(lexical_required)}/{len(required)}"
    structural_entries = [entry for entry in entries if entry["structural_supports"]]
    structural_by_family = {
        family: sorted(
            {
                entry["address"]
                for entry in structural_entries
                if entry["address"] in required
                and any(
                    support["family"] == family
                    for support in entry["structural_supports"]
                )
            },
        )
        for family in (
            "PythonResolvedModuleImportRelation",
            "PythonFunctionReferenceKnowledge",
            "PythonImmediatePackageMembership",
        )
    }
    return {
        "candidate_count": len(entries),
        "lexical_count": len(ranks),
        "structural_count": len(structural_entries),
        "required_present": len(present),
        "required_absent": sorted(required - present),
        "required_lexical": len(lexical_required),
        "required_structural": sorted(structural_required),
        "required_structural_only": sorted(structural_required - lexical_required),
        "required_both": sorted(structural_required & lexical_required),
        "required_by_structural_family": structural_by_family,
        "smallest_complete_lexical_prefix": complete_depth,
        "prefix_roles": count_before,
        "coverage_curve": curves,
        "required": {
            address: {
                "lexical_rank": by_address[address]["lexical_rank"]
                if address in by_address
                else None,
                "lexical_score": by_address[address]["lexical_score"]
                if address in by_address
                else None,
                "structural_supports": by_address[address]["structural_supports"]
                if address in by_address
                else [],
            }
            for address in sorted(required)
        },
        "structural_candidates_by_role": {
            state: sorted(
                entry["address"]
                for entry in structural_entries
                if role(entry["address"], judgments) == state
            )
            for state in ("required", "helpful_only", "unnecessary", "unresolved")
        },
    }


def main() -> None:
    """Verify source identities, join frozen judgments, and emit accounting."""
    frozen_path = PARENT / "case_0002_adjudication_frozen.json"
    frame_path = PARENT / "case_0002_adjudication_input.json"
    frozen = read_json(frozen_path)
    identity = frozen.pop("adjudication_identity")
    canonical = json.dumps(
        frozen,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    assert hashlib.sha256(canonical).hexdigest() == identity
    assert digest(frame_path) == frozen["neutral_frame_sha256"]
    assert (
        digest(HERE / "blind_raw_judgment.json") == frozen["raw_blind_judgment_sha256"]
    )
    assert (
        digest(HERE / "blind_adjudicator_trace.jsonl") == frozen["blind_trace_sha256"]
    )
    assert digest(HERE / "blind_prompt.txt") == frozen["blind_prompt_sha256"]
    frame = read_json(frame_path)
    pre = read_json(HERE / "pre_retrieval.json")
    retrieval = read_json(HERE / "retrieval.json")
    pre_agent = read_json(HERE / "pre_agent.json")
    post = read_json(HERE / "post_run.json")
    assert frame["resources"] == pre["snapshot_resources"]
    assert frame["snapshot_id"] == pre["snapshot_id"] == post["starting_snapshot_id"]
    assert pre["case_id"] == pre_agent["case_id"] == post["case_id"]
    pre_identity = pre.pop("case_id")
    assert (
        hashlib.sha256(
            json.dumps(pre, sort_keys=True, ensure_ascii=False).encode(),
        ).hexdigest()
        == pre_identity
    )
    for name, expected in post["trace_sha256"].items():
        assert digest(HERE / name) == expected
    assert digest(HERE / "post_run.patch") == post["post_run_patch_sha256"]
    assert (
        digest(HERE / "continuation_handoff.txt") == post["continuation_handoff_sha256"]
    )
    assert (
        normalized_text_digest(HERE / "orientation.txt")
        == pre_agent["orientation_sha256"]
    )
    assert normalized_text_digest(HERE / "handoff.txt") == pre_agent["handoff_sha256"]
    native_input_sha256 = hashlib.sha256(
        gzip.decompress((HERE / "inputs.pkl.gz").read_bytes()),
    ).hexdigest()
    native_capture_sha256 = hashlib.sha256(
        gzip.decompress((HERE / "capture.pkl.gz").read_bytes()),
    ).hexdigest()
    coverage = compare_identity_coverage(
        expected=(row[0] for row in frame["resources"]),
        observed=(item["address"] for item in frozen["judgments"]),
    )
    assert coverage.is_exact
    assert len(frame["resources"]) == EXPECTED_RESOURCE_COUNT
    assert len(frozen["judgments"]) == EXPECTED_RESOURCE_COUNT
    judgments = {item["address"]: item for item in frozen["judgments"]}
    required = {
        address for address in judgments if role(address, judgments) == "required"
    }
    helpful = {
        address for address in judgments if role(address, judgments) == "helpful_only"
    }
    observation = post["observation"]
    opened = set(observation["opened_resources"])
    modified = set(observation["modified_resources"])
    validation = set(observation["validation_resources"])
    arms = {
        name: arm_result(entries, required, judgments)
        for name, entries in retrieval.items()
    }
    result = {
        "schema": "codex-dogfood-case-0002-joined-analysis-v1",
        "case_id": pre_identity,
        "adjudication_identity": identity,
        "adjudication_artifact_sha256": digest(frozen_path),
        "native_inputs_sha256": native_input_sha256,
        "native_capture_sha256": native_capture_sha256,
        "identity_coverage": frozen["identity_coverage"],
        "counts": {
            "required": len(required),
            "helpful_only": len(helpful),
            "unnecessary": sum(role(a, judgments) == "unnecessary" for a in judgments),
            "unresolved": sum(role(a, judgments) == "unresolved" for a in judgments),
            "alternatives": len(frozen["alternatives"]),
        },
        "required": {
            address: judgments[address]["states"] for address in sorted(required)
        },
        "helpful_only": sorted(helpful),
        "arms": arms,
        "orientation_count": pre_agent["orientation_count"],
        "handoff_bytes": pre_agent["handoff_bytes"],
        "agent": {
            "session_count": len(post["trace_sha256"]),
            "interrupted_trace_truncated_lines": post[
                "interrupted_trace_truncated_lines"
            ],
            "command_count": post["command_count"],
            "search_count": len(observation["searches"]),
            "searches": observation["searches"],
            "direct_open_events": len(observation["opened_resources"]),
            "distinct_direct_opens": len(opened),
            "required_opened": sorted(required & opened),
            "required_not_opened": sorted(required - opened),
            "helpful_opened": sorted(helpful & opened),
            "unnecessary_opened": sorted(
                {a for a in opened if role(a, judgments) == "unnecessary"},
            ),
            "outside_frame_opened": sorted(opened - judgments.keys()),
            "modified_by_role": {a: role(a, judgments) for a in sorted(modified)},
            "validation_by_role": {a: role(a, judgments) for a in sorted(validation)},
            "task_success": observation["task_success"],
            "validation_success": observation["validation_success"],
            "model_token_usage": post["model_token_usage"],
            "bytes_read": observation["bytes_read"],
            "tokens_read": observation["tokens_read"],
        },
    }
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if sys.argv[1:] == ["--write"]:
        with (HERE / "joined_analysis.json").open("xb") as output:
            output.write(rendered.encode("utf-8"))
    else:
        assert (HERE / "joined_analysis.json").read_bytes() == rendered.encode("utf-8")
        print(rendered)


if __name__ == "__main__":
    main()
