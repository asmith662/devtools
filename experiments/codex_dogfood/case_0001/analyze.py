# Copyright (c) 2026
# ruff: noqa: T201, S101
"""Recompute the Case 0001 provenance join after the immutable blind freeze."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, cast

from devtools.evaluation.coverage import compare_identity_coverage

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
EXPECTED_RESOURCE_COUNT = 299


def read_json(path: Path) -> dict[str, Any]:
    """Read one retained case artifact."""
    return cast("dict[str, Any]", json.loads(path.read_text(encoding="utf-8-sig")))


def digest(path: Path) -> str:
    """Return an artifact's byte identity."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:  # noqa: PLR0915
    """Check identities, join frozen labels, and emit descriptive accounting."""
    frozen_path = PARENT / "case_0001_adjudication_frozen.json"
    frame_path = PARENT / "case_0001_adjudication_input.json"
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
    frame = read_json(frame_path)
    pre = read_json(HERE / "pre_retrieval.json")
    retrieval = read_json(HERE / "retrieval.json")
    pre_agent = read_json(HERE / "pre_agent.json")
    post = read_json(HERE / "post_run.json")
    assert frame["resources"] == pre["snapshot_resources"]
    assert frame["snapshot_id"] == pre["snapshot_id"] == post["starting_snapshot_id"]
    assert pre["case_id"] == pre_agent["case_id"] == post["case_id"]
    assert digest(HERE / "codex_trace.jsonl") == post["trace_sha256"]
    assert digest(HERE / "post_run.patch") == post["post_run_patch_sha256"]
    orientation_text = (HERE / "orientation.txt").read_text(encoding="utf-8")
    handoff_text = (HERE / "handoff.txt").read_text(encoding="utf-8")
    assert hashlib.sha256(orientation_text.encode()).hexdigest() == pre_agent[
        "orientation_sha256"
    ]
    assert hashlib.sha256(handoff_text.encode()).hexdigest() == pre_agent[
        "handoff_sha256"
    ]
    coverage = compare_identity_coverage(
        expected=(item[0] for item in frame["resources"]),
        observed=(item["address"] for item in frozen["judgments"]),
    )
    assert coverage.is_exact
    assert len(frame["resources"]) == EXPECTED_RESOURCE_COUNT
    assert len(frozen["judgments"]) == EXPECTED_RESOURCE_COUNT
    judgments = {item["address"]: item for item in frozen["judgments"]}
    required = {
        a
        for a, j in judgments.items()
        if any(s.startswith("required_") for s in j["states"])
    }
    helpful = {a for a, j in judgments.items() if "helpful_only" in j["states"]}
    observation = post["observation"]
    opened = set(observation["opened_resources"])
    modified = set(observation["modified_resources"])
    validation = set(observation["validation_resources"])
    arms = {}
    for name, entries in retrieval.items():
        by_address = {entry["address"]: entry for entry in entries}
        assert len(by_address) == len(entries)
        ranks = [
            entry["lexical_rank"]
            for entry in entries
            if entry["lexical_rank"] is not None
        ]
        assert len(ranks) == len(set(ranks))
        details = {
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
        }
        present = required & by_address.keys()
        missing = required - by_address.keys()
        lexical_required = {
            a for a in present if by_address[a]["lexical_rank"] is not None
        }
        structural_required = {
            a for a in present if by_address[a]["structural_supports"]
        }
        prefix = max(
            (by_address[a]["lexical_rank"] for a in lexical_required), default=None,
        )
        arms[name] = {
            "candidate_count": len(entries),
            "lexical_count": len(ranks),
            "structural_count": sum(bool(e["structural_supports"]) for e in entries),
            "required_present": len(present),
            "required_absent": sorted(missing),
            "required_lexical": len(lexical_required),
            "required_structural": sorted(structural_required),
            "required_structural_only": sorted(structural_required - lexical_required),
            "smallest_lexical_prefix_for_lexically_satisfiable_required": prefix,
            "required": details,
        }
    result = {
        "schema": "codex-dogfood-case-0001-joined-analysis-v1",
        "case_id": pre["case_id"],
        "adjudication_identity": identity,
        "adjudication_artifact_sha256": digest(frozen_path),
        "identity_coverage": frozen["identity_coverage"],
        "counts": {
            "required": len(required),
            "helpful_only": len(helpful),
            "unnecessary": sum(
                j["states"] == ["unnecessary"] for j in frozen["judgments"]
            ),
            "unresolved": sum(
                j["states"] == ["unresolved"] for j in frozen["judgments"]
            ),
            "alternatives": len(frozen["alternatives"]),
        },
        "required": {a: judgments[a]["states"] for a in sorted(required)},
        "helpful_only": sorted(helpful),
        "arms": arms,
        "orientation_count": pre_agent["orientation_count"],
        "handoff_bytes": pre_agent["handoff_bytes"],
        "agent": {
            "search_count": len(observation["searches"]),
            "searches": observation["searches"],
            "direct_open_events": len(observation["opened_resources"]),
            "distinct_direct_opens": len(opened),
            "required_opened": sorted(required & opened),
            "required_not_opened": sorted(required - opened),
            "helpful_opened": sorted(helpful & opened),
            "unnecessary_opened": sorted(opened - required - helpful),
            "required_modified": sorted(required & modified),
            "modified_not_required": sorted(modified - required),
            "validation_resources": sorted(validation),
            "required_validation_resources": sorted(
                {
                    a
                    for a in required
                    if "required_for_validation" in judgments[a]["states"]
                },
            ),
            "task_success": observation["task_success"],
            "validation_success": observation["validation_success"],
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
