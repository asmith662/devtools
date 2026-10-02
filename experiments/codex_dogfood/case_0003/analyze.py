# Copyright (c) 2026
# ruff: noqa: COM812, E501
"""Freeze neutral blind judgments first; explicitly join provenance afterward."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from typing import Any, cast

from devtools.evaluation.coverage import compare_identity_coverage

HERE = Path(__file__).resolve().parent
DEPTHS = (5, 10, 20, 50, 100)
REQUIRED = frozenset(
    {
        "required_for_understanding",
        "required_for_implementation",
        "required_for_api_contract",
        "required_for_tests",
        "required_for_configuration",
        "required_for_validation",
    }
)
STATES = REQUIRED | {"helpful_only", "unnecessary", "unresolved"}


def read_json(path: Path) -> dict[str, Any]:
    """Read an explicitly addressed retained protocol artifact."""
    return cast("dict[str, Any]", json.loads(path.read_text(encoding="utf-8-sig")))


def digest(path: Path) -> str:
    """Hash exact retained artifact bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_trace(path: Path) -> str:
    """Decode raw external JSONL without changing retained byte identities.

    Windows PowerShell redirection may write UTF-16 with a byte order mark;
    Codex output captured directly is UTF-8, optionally with its own mark.
    """
    content = path.read_bytes()
    return content.decode(
        "utf-16" if content.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig"
    )


def expand_judgments(
    frame: dict[str, Any], raw: dict[str, Any]
) -> list[dict[str, Any]]:
    """Validate neutral outcomes and explicit unlisted-unnecessary affirmation."""
    if raw["snapshot_id"] != frame["snapshot_id"]:
        msg = "Blind judgment snapshot differs from neutral frame."
        raise ValueError(msg)
    expected = [item[0] for item in frame["resources"]]
    observed = [item["address"] for item in raw["judgments"]]
    coverage = compare_identity_coverage(expected=expected, observed=observed)
    if (
        coverage.duplicate_expected
        or coverage.duplicate_observed
        or coverage.unexpected
    ):
        msg = "Blind judgment identities are duplicate or outside the neutral frame."
        raise ValueError(msg)
    if coverage.missing and not raw["unlisted_resources_are_unnecessary"]:
        msg = (
            "Blind judgment leaves identities unassessed without explicit affirmation."
        )
        raise ValueError(msg)
    by_address = {item["address"]: item for item in raw["judgments"]}
    for item in by_address.values():
        states = item["states"]
        if not states or len(set(states)) != len(states) or set(states) - STATES:
            msg = "Blind judgment contains invalid obligation states."
            raise ValueError(msg)
        if not set(states) <= REQUIRED and len(states) != 1:
            msg = "Blind judgment combines incompatible outcome categories."
            raise ValueError(msg)
        if not item["rationale"].strip():
            msg = "Blind judgment lacks a rationale."
            raise ValueError(msg)
    return [
        by_address.get(
            address,
            {
                "address": address,
                "states": ["unnecessary"],
                "rationale": "Adjudicator explicitly affirmed every unlisted eligible resource unnecessary.",
            },
        )
        for address in expected
    ]


def freeze_adjudication(directory: Path = HERE) -> None:
    """Freeze labels and identity accounting without opening retrieval or traces."""
    target = directory / "adjudication_frozen.json"
    if target.exists():
        msg = "Blind adjudication already frozen; refuse to overwrite."
        raise ValueError(msg)
    frame = read_json(directory / "adjudication_input.json")
    raw = read_json(directory / "blind_raw_judgment.json")
    judgments = expand_judgments(frame, raw)
    coverage = compare_identity_coverage(
        expected=(item[0] for item in frame["resources"]),
        observed=(item["address"] for item in judgments),
    )
    trace = directory / "blind_adjudicator_trace.jsonl"
    if not trace.exists():
        msg = "Blind adjudicator trace is required before judgment freeze."
        raise ValueError(msg)
    events = [
        json.loads(line) for line in read_trace(trace).splitlines() if line.strip()
    ]
    if not any(item.get("type") == "turn.completed" for item in events) or any(
        item.get("item", {}).get("type") == "file_change" for item in events
    ):
        msg = "Blind adjudicator trace is incomplete or modified repository state."
        raise ValueError(msg)
    payload = {
        "schema": "codex-blind-adjudication-frozen-v1",
        "snapshot_id": frame["snapshot_id"],
        "neutral_frame_sha256": digest(directory / "adjudication_input.json"),
        "raw_judgment_sha256": digest(directory / "blind_raw_judgment.json"),
        "adjudicator_trace_sha256": digest(trace),
        "identity_coverage": {
            **asdict(coverage),
            "is_exact": coverage.is_exact,
            "expected_count": len(frame["resources"]),
            "observed_count": len(judgments),
        },
        "judgments": judgments,
        "acceptable_alternatives": raw["acceptable_alternatives"],
        "limitations": raw["limitations"],
        "provenance_joined": False,
    }
    target.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def role(judgment: dict[str, Any]) -> str:
    """Interpret dogfood obligation categories, independently of identity kernel."""
    return (
        "required"
        if set(judgment["states"]) & REQUIRED
        else cast("str", judgment["states"][0])
    )


def assess_order(order: list[str], judgments: list[dict[str, Any]]) -> dict[str, Any]:
    """Measure complete required coverage, including incomplete inventories."""
    if len(set(order)) != len(order):
        msg = "Ranking repeats resource identities."
        raise ValueError(msg)
    roles = {item["address"]: role(item) for item in judgments}
    if set(order) - roles.keys():
        msg = "Ranking contains identities outside the frozen judged frame."
        raise ValueError(msg)
    required = {address for address, state in roles.items() if state == "required"}
    ranks = {address: rank for rank, address in enumerate(order, 1)}
    missing = sorted(required - ranks.keys())
    last = (
        max((ranks[address] for address in required), default=0)
        if not missing
        else None
    )
    prefix = order[:last] if last is not None else order
    counts = Counter(roles[address] for address in prefix)
    return {
        "candidate_count": len(order),
        "required_count": len(required),
        "required_ranks": {address: ranks.get(address) for address in sorted(required)},
        "missing_required": missing,
        "required_present": len(required) - len(missing),
        "recall": {
            str(depth): sum(
                ranks.get(address, float("inf")) <= depth for address in required
            )
            / len(required)
            if required
            else None
            for depth in DEPTHS
        },
        "last_required_rank": last,
        "prefix_scope": "through complete required coverage"
        if last is not None
        else "entire incomplete inventory; complete-coverage prefix does not exist",
        "prefix_roles": {
            state: counts[state]
            for state in ("required", "helpful_only", "unnecessary", "unresolved")
        },
    }


def trace_observation(trace: Path, frame_addresses: set[str]) -> dict[str, Any]:
    """Record explicit commands/opens without converting behavior into obligations."""
    commands = []
    modified: set[str] = set()
    completed = False
    usage: object = None
    invalid_lines = 0
    for line in read_trace(trace).splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            invalid_lines += 1
            continue
        if event.get("type") == "turn.completed":
            completed = True
            usage = event.get("usage")
        item = event.get("item", {})
        if (
            event.get("type") == "item.completed"
            and item.get("type") == "command_execution"
        ):
            commands.append(
                {
                    "command": item["command"],
                    "exit_code": item.get("exit_code"),
                    "status": item.get("status"),
                }
            )
        if item.get("type") == "file_change":
            modified.update(
                change["path"].replace("\\", "/") for change in item.get("changes", [])
            )
    searches = [
        item
        for item in commands
        if re.search(r"\brg(?:\.exe)?\b|Select-String", item["command"])
    ]
    open_events: list[str] = []
    # Explicit Get-Content file tokens only; search output and validation transitive
    # reads are not direct opens, and generalized script reads stay unmeasured.
    pattern = re.compile(r"\bGet-Content\b(?P<args>[^;\n|]+)", re.IGNORECASE)
    path_pattern = re.compile(
        r"(?:[A-Za-z0-9_.-]+[/\\])*[A-Za-z0-9_.-]+\.(?:py|md|toml|yaml|yml)\b"
    )
    for item in commands:
        for match in pattern.finditer(item["command"]):
            open_events.extend(
                path.replace("\\", "/") for path in path_pattern.findall(match["args"])
            )
    opened = set(open_events)
    validation = [
        item
        for item in commands
        if re.search(r"\bpytest\b|\bmypy\b|\bruff\b|git diff", item["command"])
    ]
    return {
        "completed": completed,
        "usage": usage,
        "invalid_lines": invalid_lines,
        "command_count": len(commands),
        "commands": commands,
        "search_count": len(searches),
        "searches": searches,
        "direct_open_event_count": len(open_events),
        "direct_open_resources": sorted(opened),
        "outside_frame_opens": sorted(opened - frame_addresses),
        "modified_resources_from_trace": sorted(modified),
        "validation_commands": validation,
        "limitation": "Explicit command/direct-Get-Content telemetry only; searches, indirect Python reads and transitive validation reads are not inferred. File changes/opens do not establish requirements. No comparable unaided control.",
    }


def join(directory: Path = HERE) -> dict[str, Any]:
    """Verify immutable boundaries before joining retrieval and agent evidence."""
    frozen_path = directory / "adjudication_frozen.json"
    if not frozen_path.exists() or not (directory / "post_run.json").exists():
        msg = "Join requires frozen blind adjudication and frozen implementation observation."
        raise ValueError(msg)
    labels = read_json(frozen_path)
    for key, name in (
        ("neutral_frame_sha256", "adjudication_input.json"),
        ("raw_judgment_sha256", "blind_raw_judgment.json"),
        ("adjudicator_trace_sha256", "blind_adjudicator_trace.jsonl"),
    ):
        if labels[key] != digest(directory / name):
            msg = "Frozen blind adjudication input has changed."
            raise ValueError(msg)
    frame = read_json(directory / "adjudication_input.json")
    capture = read_json(directory / "retrieval.json")
    pre_agent = read_json(directory / "pre_agent.json")
    post = read_json(directory / "post_run.json")
    if (
        not labels["identity_coverage"]["is_exact"]
        or labels["snapshot_id"] != capture["snapshot_id"]
        or labels["snapshot_id"] != frame["snapshot_id"]
    ):
        msg = "Judged and retrieved snapshot frames differ."
        raise ValueError(msg)
    if (
        capture["freeze_sha256"] != digest(directory / "initial_pre_retrieval.json")
        or digest(directory / "pre_retrieval.json")
        != pre_agent["freeze_corrected_sha256"]
        or digest(directory / "handoff.txt") != pre_agent["handoff_sha256"]
        or capture["native_capture_sha256"] != digest(directory / "capture.pkl.gz")
    ):
        msg = "Captured retrieval or advisory handoff differs from immutable boundary."
        raise ValueError(msg)
    judgments = labels["judgments"]
    required = {item["address"] for item in judgments if role(item) == "required"}
    arms = {}
    for arm, payload in capture["arms"].items():
        orders = payload["rankings"]
        lexical_ranks = {
            address: rank for rank, address in enumerate(orders["bm25"], 1)
        }
        assessed = {
            channel: assess_order(order, judgments) for channel, order in orders.items()
        }
        for channel, result in assessed.items():
            result["rescued_required_lexical_misses"] = [
                address
                for address, rank in result["required_ranks"].items()
                if rank is not None and address not in lexical_ranks
            ]
            result["required_rank_movements"] = {
                address: {
                    "bm25": lexical_ranks.get(address),
                    "channel": rank,
                    "rank_delta": lexical_ranks[address] - rank
                    if address in lexical_ranks and rank is not None
                    else None,
                }
                for address, rank in result["required_ranks"].items()
            }
            provenance = payload.get(
                "map_provenance"
                if channel == "repository_map"
                else "ppr_provenance"
                if channel == "typed_ppr"
                else "",
                {},
            )
            result["required_native_provenance"] = {
                address: provenance[address]
                for address in sorted(required & provenance.keys())
            }
        arms[arm] = {
            "channels": assessed,
            "runtime_seconds": payload["runtime_seconds"],
            "ranked_symbols": payload["ranked_symbols"],
            "structurally_absent_map_required": sorted(
                required - payload["map_provenance"].keys()
            ),
        }
    frame_addresses = {item[0] for item in frame["resources"]}
    observation = trace_observation(directory / "codex_trace.jsonl", frame_addresses)
    surfaced = {
        address
        for arm in capture["arms"].values()
        for order in arm["rankings"].values()
        for address in order[:10]
    }
    opened = set(observation["direct_open_resources"])
    observation["advisory_surfaced_then_opened"] = sorted(opened & surfaced)
    observation["opened_outside_advisory"] = sorted(opened - surfaced)
    observation["required_opened_outside_advisory"] = sorted(
        required & (opened - surfaced)
    )
    observation["required_not_directly_opened"] = sorted(required - opened)
    observation["required_missing_both_lexical_arms_then_opened"] = sorted(
        required
        & opened
        - set(capture["arms"]["full_prompt"]["rankings"]["bm25"])
        - set(capture["arms"]["short_information_need"]["rankings"]["bm25"])
    )
    return {
        "schema": "codex-case3-joined-analysis-v1",
        "snapshot_id": frame["snapshot_id"],
        "adjudication_sha256": digest(frozen_path),
        "retrieval_sha256": digest(directory / "retrieval.json"),
        "post_run_sha256": digest(directory / "post_run.json"),
        "counts": dict(sorted(Counter(role(item) for item in judgments).items())),
        "required_resources": sorted(required),
        "arms": arms,
        "global_importance_seconds": capture["global_importance_seconds"],
        "global_iterations": capture["global_iterations"],
        "implementation_observation": post,
        "agent": observation,
        "protocol_limitation": "Handwritten initial filename-weight metadata typo corrected transparently; canonical unchanged production scoring remained0.25; capture-time manifest and correction both retained.",
        "confirmation_accessed": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("freeze-adjudication", "join"))
    args = parser.parse_args()
    if args.phase == "freeze-adjudication":
        freeze_adjudication()
    else:
        (HERE / "joined_analysis.json").write_text(
            json.dumps(join(), indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
