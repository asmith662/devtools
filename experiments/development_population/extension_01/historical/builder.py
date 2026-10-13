# Copyright (c) 2026
# ruff: noqa: ANN401, COM812, EM101, TRY003, PLR2004, E501 -- bounded codec and exact SHA literals
"""Build/replay a population from authenticated pre-selection Git metadata.

Never reads child patches/path lists during replay. The pinned input receipt was
captured before selection; native Git commit/tree objects remain independent
source bindings. This is not relevance gold or a retrieval implementation.
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
from typing import Any, cast

from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    digest,
    git,
    json_bytes,
    put_text,
)
from experiments.increment_25.task_population import validate_freeze

PACKAGE = Path(__file__).resolve().parent
INPUT = PACKAGE / "holdout/captured_metadata.json"
INPUT_SHA = "f1128adc5fef3abfc701bada6f069cf42bfd0447068a38ddcd5cd9773a50a426"
DOMAIN = "devtools-historical-development-extension-v1"
PRIOR_TASK_SHA = "e5ebb4f576f58ddeee43e07eee62ef8035936c9f2b0f22449d4ee8d4f561ec72"
AUDIT_HASHES = {
    "access_record.json": "c1612ce78ef6ad11bbab1e2b2096f79d953b96feffa5df3c4194e08b7ed18730",
    "candidate_inventory.json": "c033f34f12c155aea2f1f73df0e56f353831c9df7dfca4a0de2b075157c776b3",
    "eligibility_rules.json": "b2347fe0f031d03e1d236dcec9b0d5e1185bfa834072506a8a319a769e364833",
    "README.md": "914a880e570de0bd95cc1be8f2210971b0d9e94e3ebfb618a870cccd9826cd93",
    "source_hashes.json": "507516040ecf92ae737ff369ef2106fb5695be5195cdd212daf5a7d943ef9e95",
    "validation.json": "64111b0f968d7f9efba5c32a6e3dd1f0d1b183af7b26223adeead09c19582545",
}


def inputs() -> Any:
    """Authenticate exact pre-selection receipt without reopening holdout diffs."""
    raw = INPUT.read_bytes()
    if digest(raw) != INPUT_SHA:
        raise ValueError("Pre-selection metadata receipt differs")
    return json.loads(raw)


def source_hashes() -> dict[str, str]:
    """Bind builder/test/documentation bytes, never outcome-dependent inputs."""
    paths = [*PACKAGE.glob("*.py"), PACKAGE / "README.md"]
    return {p.name: digest(p.read_bytes()) for p in sorted(paths)}


def supporting_inputs() -> Any:
    """Authenticate preserved non-population audit and prior-task-only receipt."""
    audit = ROOT / "experiments/development_population/extension_01/audit"
    if {
        p.name: digest(p.read_bytes()) for p in audit.iterdir() if p.is_file()
    } != AUDIT_HASHES:
        raise ValueError("Source exhaustion audit differs")
    raw = (Path(__file__).resolve().parent / "prior_task_exclusions.json").read_bytes()
    if digest(raw) != PRIOR_TASK_SHA:
        raise ValueError("Prior-task exclusion receipt differs")
    return json.loads(raw)


def expected(value: Any) -> dict[str, bytes]:
    """Canonicalize the complete inventory before deriving any selection seed."""
    supporting = supporting_inputs()
    rows = sorted(value["rows"], key=lambda r: r["child"])
    eligible = [r for r in rows if r["reason"] == "ELIGIBLE"]
    grouped: dict[str, list[Any]] = {}
    for row in eligible:
        text = " ".join(row["task_text"].casefold().split())
        grouped.setdefault(text, []).append(row)
    representatives = [group[0] for _, group in sorted(grouped.items())]
    representatives.sort(key=lambda r: r["child"])
    if len(representatives) < 8:
        raise ValueError("Fewer than eight independent eligible episodes")
    prior, scope, rules = value["prior"], value["scope"], value["rules"]
    prior_texts = {
        " ".join(r["task_text"].casefold().split()) for r in supporting["records"]
    }
    for row in representatives:
        size = rules["size"]
        if (
            len(row["parents"]) != 1
            or row["child"][:12] in prior["excluded_id_prefixes"]
            or " ".join(row["task_text"].casefold().split()) in prior_texts
            or not 1 <= row["production_files"] <= size["maximum_production_files"]
            or row["total_files"] > size["maximum_total_changed_files"]
            or row["lines"] > size["maximum_production_test_changed_lines"]
            or row["binary_production_test"]
        ):
            raise ValueError("Eligibility/previous-task exclusion differs")
    inventory = {
        "schema": "historical-development-candidate-inventory-v1",
        "role": "POPULATION_ADMINISTRATION; NOT A STAGE A/B/C TASK PACKET",
        "candidates": [
            {
                "candidate_id": "episode-" + r["child"],
                "child_commit": r["child"],
                "parent_commit": r["parents"][0] if r["parents"] else None,
                "subject": r["subject"],
                "body_sha256": r["body_sha256"],
                "task_sha256": digest(r["task_text"].encode())
                if r["task_text"] is not None
                else None,
                "commit_timestamp": r["timestamp"],
                "changed_file_count": r["total_files"],
                "production_file_count": r["production_files"],
                "production_test_changed_lines": r["lines"],
                "path_categories": r["categories"],
                "binary_production_test": r["binary_production_test"],
                "eligible": r["reason"] == "ELIGIBLE",
                "disposition": r["reason"],
                "prior_task_duplicate": r["prior_task_duplicate"],
                "linked_parent_work_item": None,
                "prior_task_message_withheld": r["task_text"] is None,
            }
            for r in rows
        ],
        "deduplication": [
            {
                "canonical": group[0]["child"],
                "duplicates": [r["child"] for r in group[1:]],
                "reason": "Identical normalized original task text",
            }
            for group in grouped.values()
            if len(group) > 1
        ],
    }
    eligible_inventory = [
        {
            "candidate_id": "episode-" + r["child"],
            "task_sha256": digest(r["task_text"].encode()),
            "parent_commit": r["parents"][0],
            "parent_tree": r["parent_tree"],
        }
        for r in representatives
    ]
    inventory_sha = digest(json_bytes(eligible_inventory))
    scope_sha = digest(json_bytes(scope))
    seed_inputs = [
        DOMAIN,
        scope["starting_head"],
        scope_sha,
        prior["original_sha256"],
        prior["expanded_sha256"],
        inventory_sha,
    ]
    seed = digest(json_bytes(seed_inputs))
    ordered = sorted(
        representatives,
        key=lambda r: (
            bytes.fromhex(
                digest(bytes.fromhex(seed) + ("episode-" + r["child"]).encode())
            ),
            r["child"],
        ),
    )[:16]
    cards, holdout = [], []
    for position, row in enumerate(ordered, 1):
        case = f"historical-development-{position:03}"
        cards.append(
            {
                "schema": "historical-development-public-task-v1",
                "case_id": case,
                "population_id": DOMAIN,
                "selection_position": position,
                "title": row["subject"],
                "task_text": row["task_text"],
                "task_source": {
                    "kind": "EXACT_ORIGINAL_GIT_COMMIT_MESSAGE",
                    "task_sha256": digest(row["task_text"].encode()),
                    "provenance_reference": case + "/commit-message",
                },
                "frame": {
                    "kind": "GIT_PARENT_TREE",
                    "parent_commit": row["parents"][0],
                    "parent_tree": row["parent_tree"],
                    "native_repository_snapshot": "NOT_CONSTRUCTED",
                },
            }
        )
        holdout.append(
            {
                "case_id": case,
                "child_commit": row["child"],
                "child_tree": row["child_tree"],
                "parent_commit": row["parents"][0],
                "parent_tree": row["parent_tree"],
                "diff_sha256": row["diff_sha256"],
                "changed_path_sha256": row["changed_path_sha256"],
                "numstat_sha256": row["numstat_sha256"],
                "commit_metadata_sha256": row["commit_metadata_sha256"],
                "task_sha256": digest(row["task_text"].encode()),
            }
        )
    audit_hashes = AUDIT_HASHES
    provenance = {
        "schema": "historical-development-selection-v1",
        "seed_inputs": seed_inputs,
        "seed_sha256": seed,
        "history_scope_sha256": scope_sha,
        "complete_inventory_sha256": digest(json_bytes(inventory)),
        "eligible_inventory_sha256": inventory_sha,
        "selection": (
            "SHA256(seed raw bytes + UTF8 candidate identity), "
            "raw bytes then identity; first16 or all8..15"
        ),
        "prior_exclusions": prior,
        "selected_count": len(cards),
        "rerolls": 0,
    }
    freeze = {
        "schema": "historical-development-population-freeze-v1",
        "population_id": DOMAIN,
        "starting_head": scope["starting_head"],
        "history_scope_sha256": scope_sha,
        "candidate_inventory_sha256": digest(json_bytes(inventory)),
        "eligibility_rules_sha256": digest(json_bytes(rules)),
        "selection_sha256": digest(json_bytes(provenance)),
        "input_receipt_sha256": INPUT_SHA,
        "prior_task_exclusions_sha256": PRIOR_TASK_SHA,
        "source_exhaustion_role": "NON_POPULATION / SOURCE_EXHAUSTION_AUDIT",
        "source_exhaustion_sha256": audit_hashes,
        "implementation_sha256": source_hashes(),
        "selected_development_tasks": cards,
        "next_case_id": cards[0]["case_id"],
        "treatment_design": "PENDING",
        "retrieval_execution": "NOT_RUN",
        "gold": "NOT_CREATED",
    }
    files = {
        "candidate_inventory.json": json_bytes(inventory),
        "eligibility_rules.json": json_bytes(rules),
        "history_scope.json": json_bytes(scope),
        "selection_provenance.json": json_bytes(provenance),
        "population_freeze.json": json_bytes(freeze),
        "selected_next_case.json": json_bytes(cards[0]),
        "holdout/reference_implementations.json": json_bytes(
            {
                "schema": "historical-development-reference-implementation-holdout-v1",
                "restriction": (
                    "RESTRICTED UNTIL POST-GOLD / STAGE D; "
                    "CHILD DIFF IS NOT RELEVANCE GOLD"
                ),
                "reference_implementations": holdout,
            }
        ),
        "access_record.json": json_bytes(
            {
                "previous_development_ids": True,
                "previous_development_task_text": True,
                "previous_development_gold": False,
                "previous_development_retrieval_outputs": "INCIDENTAL_CONTAINER_KEYS_ONLY",
                "confirmation_ids": True,
                "confirmation_task_bodies": False,
                "confirmation_gold": False,
                "reserve_ids": True,
                "reserve_task_bodies": False,
                "reserve_gold": False,
                "candidate_commit_metadata": True,
                "candidate_changed_path_names": True,
                "candidate_diff_semantic_contents": False,
                "diff_bytes_mechanically_hashed": True,
                "selected_case_changed_paths_after_selection": False,
                "selected_case_diff_after_selection": False,
                "bm25_rankings": False,
                "graph_ranks": False,
                "native_reference_relations": False,
                "incidental_exposure": (
                    "Retained exhaustion audit contains known historical aggregate "
                    "narratives; never selection inputs. "
                    "Prior/held-out commit messages withheld."
                    " Case0001/0002 pre_agent result-field keys incidentally seen "
                    "while locating task text; no result values inspected/used."
                ),
            }
        ),
    }
    validate_files(files)
    files["integrity.json"] = json_bytes(
        {
            "schema": "historical-development-integrity-v1",
            "sha256": {n: digest(raw) for n, raw in files.items()},
            "input_receipt_sha256": INPUT_SHA,
            "prior_task_exclusions_sha256": PRIOR_TASK_SHA,
            "implementation_sha256": source_hashes(),
            "source_exhaustion_sha256": audit_hashes,
        }
    )
    return files


def validate_files(files: dict[str, bytes]) -> None:
    """Reject any public task schema/byte leakage or parent/task identity drift."""
    population = json.loads(files["population_freeze.json"])
    selected = json.loads(files["selected_next_case.json"])
    cards = population["selected_development_tasks"]
    if selected != cards[0] or not 8 <= len(cards) <= 16:
        raise ValueError("Population membership/next case differs")
    for card in cards:
        if set(card) != {
            "schema",
            "case_id",
            "population_id",
            "selection_position",
            "title",
            "task_text",
            "task_source",
            "frame",
        }:
            raise ValueError("Public task leakage/schema differs")
        if set(card["frame"]) != {
            "kind",
            "parent_commit",
            "parent_tree",
            "native_repository_snapshot",
        } or set(card["task_source"]) != {
            "kind",
            "task_sha256",
            "provenance_reference",
        }:
            raise ValueError("Public provenance/frame leakage")
        if digest(card["task_text"].encode()) != card["task_source"]["task_sha256"]:
            raise ValueError("Task source hash differs")


async def authenticate_scope(scope: Any) -> None:
    """Authenticate the immutable pre-program first-parent history boundary."""
    await git("merge-base", "--is-ancestor", scope["starting_head"], "HEAD")
    all_commits = (
        (await git("rev-list", "--first-parent", scope["starting_head"]))
        .decode()
        .splitlines()
    )
    if (
        len(all_commits) != scope["all_first_parent_count"]
        or digest(json_bytes(all_commits)) != scope["all_first_parent_sha256"]
    ):
        raise ValueError("Starting first-parent history differs")
    anchor_parent = (
        (await git("rev-parse", scope["anchor_commit"] + "^1")).decode().strip()
    )
    if anchor_parent != scope["scope_tip"] or anchor_parent != scope["anchor_parent"]:
        raise ValueError("Historical cutoff differs")


async def authenticate_sources(value: Any) -> None:
    """Authenticate cutoff, previous populations and task-only exclusion sources."""
    scope = value["scope"]
    await authenticate_scope(scope)
    freezes = {}
    for name, address in (
        ("original", "experiments/increment_25/task_population_freeze.json"),
        ("expanded", "experiments/increment_27/experiment_freeze.json"),
    ):
        raw = await git("show", scope["starting_head"] + ":" + address)
        if digest(raw) != value["prior"][name + "_sha256"]:
            raise ValueError("Previous population source hash differs")
        record = json.loads(raw)
        if record["content_identity"] != value["prior"][name + "_identity"]:
            raise ValueError("Previous population identity differs")
        freezes[name] = record
    original = freezes["original"]
    if not validate_freeze(original):
        raise ValueError("Original population content identity differs")
    expanded = freezes["expanded"]
    canonical = (
        json.dumps(expanded["payload"], indent=2, sort_keys=True, ensure_ascii=False)
        + "\n"
    ).encode()
    if digest(canonical) != expanded["content_identity"]:
        raise ValueError("Expanded population content identity differs")
    prior_ids = {
        cid.removeprefix("i25-")
        for ids in original["payload"]["split"].values()
        for cid in ids
    }
    expanded_ids = {
        r["case_id"].removeprefix("i25-")
        for r in expanded["payload"]["source_population"]["development_cases"]
    }
    if (
        prior_ids != set(value["prior"]["excluded_id_prefixes"])
        or not expanded_ids <= prior_ids
        or len(expanded_ids) != 24
        or len(original["payload"]["split"]["development_case_ids"]) != 8
    ):
        raise ValueError("Previous task exclusions differ")
    for record in supporting_inputs()["records"]:
        raw = await git("show", scope["starting_head"] + ":" + record["source_address"])
        if digest(raw) != record["source_sha256"]:
            raise ValueError("Previous task source bytes differ")


async def authenticate_git(value: Any) -> None:
    """Verify traversal and native Git identities without selected paths/patches."""
    await authenticate_sources(value)
    scope = value["scope"]
    actual = (
        (await git("rev-list", "--first-parent", scope["scope_tip"]))
        .decode()
        .splitlines()
    )
    if actual != scope["scope_commits"]:
        raise ValueError("History traversal differs")
    semaphore = asyncio.Semaphore(4)

    async def check(row: Any) -> None:
        async with semaphore:
            raw = await git("cat-file", "commit", row["child"])
            if digest(raw) != row["commit_metadata_sha256"]:
                raise ValueError("Commit metadata binding differs")
            header, message = raw.split(b"\n\n", 1)
            parents = [
                line[7:].decode()
                for line in header.splitlines()
                if line.startswith(b"parent ")
            ]
            if parents != row["parents"] or (
                row["task_text"] is not None
                and message.decode("utf8") != row["task_text"]
            ):
                raise ValueError("Parent/task source binding differs")
            tree = (await git("rev-parse", row["child"] + "^{tree}")).decode().strip()
            if tree != row["child_tree"]:
                raise ValueError("Child tree binding differs")
            if row["parents"]:
                parent = (
                    (await git("rev-parse", row["parents"][0] + "^{tree}"))
                    .decode()
                    .strip()
                )
                if parent != row["parent_tree"]:
                    raise ValueError("Parent tree binding differs")

    await asyncio.gather(*(check(row) for row in value["rows"]))


def verify(directory: Path = PACKAGE) -> dict[str, str]:
    """Rebuild expected artifacts and reject altered bytes without holdout replay."""
    value = inputs()
    asyncio.run(authenticate_git(value))
    files = expected(value)
    compare(files, {name: (directory / name).read_bytes() for name in files})
    return {n: digest(raw) for n, raw in files.items()}


def compare(expected_files: dict[str, bytes], actual: dict[str, bytes]) -> None:
    """Reject changed seed/order/membership/holdout bindings and exact bytes."""
    if expected_files != actual:
        raise ValueError("Frozen artifact differs")


def publish() -> None:
    """Refuse overwriting any frozen artifact, including partial publication."""
    value = inputs()
    asyncio.run(authenticate_git(value))
    files = expected(value)
    if any((PACKAGE / n).exists() for n in files):
        raise FileExistsError("Population freeze overwrite refused")
    for name, raw in files.items():
        put_text(PACKAGE / name, raw.decode("utf8"))


def main() -> None:
    """Publish once or verify without retrieval or child implementation inspection."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "verify"))
    args = parser.parse_args()
    if args.command == "build":
        publish()
    else:
        print(json_bytes(cast("Any", verify())).decode())  # noqa: T201 -- explicit CLI


if __name__ == "__main__":
    main()
