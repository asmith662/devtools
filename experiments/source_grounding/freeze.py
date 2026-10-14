# Copyright (c) 2026
# ruff: noqa: COM812, ANN401, E501, T201, PLC0415 -- bounded Stage A builder
"""Observe/replay prospective inputs only; never import a treatment runner."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import json
import time
from pathlib import Path
from typing import Any

from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    digest,
    git,
    json_bytes,
    put_binary,
)
from experiments.orchestration.cache import PreparationCache
from experiments.orchestration.storage import require
from experiments.source_grounding import reviewer
from experiments.source_grounding.cases import CASES
from experiments.structural_discrimination.frames import (
    POPULATION,
    POPULATION_SHA,
    SELECTION_SHA,
    START,
    observe,
    parent_blobs,
)

PACKAGE = Path(__file__).resolve().parent
PREFIX = "experiments/source_grounding/"
STAGE_A_PREFIX = PREFIX + "stage_a/host-disclosure-03/"
STATUS = "FROZEN / NOT_AUTHORIZED / NOT_EXECUTED"


def implementations() -> dict[str, str]:
    """Bind all local contracts, adapters and transitive native/proof owners."""
    paths = {
        *PACKAGE.glob("*.py"),
        *PACKAGE.glob("*.md"),
        PACKAGE / ".gitattributes",
        ROOT / "pyproject.toml",
        ROOT / "uv.lock",
        *(ROOT / "src/devtools").rglob("*.py"),
        *(ROOT / "src/devtools/core").rglob("*.py"),
        *(ROOT / "src/devtools/resources/commands").rglob("*.py"),
        *(ROOT / "src/devtools/resources/filesystem").rglob("*.py"),
        *(ROOT / "experiments/codex_dogfood/verification").glob("*.py"),
        *(ROOT / "experiments/codex_dogfood/case_0012/stage_b").glob("*.py"),
        *(ROOT / "experiments/codex_dogfood/case_0015/stage_b").glob("*.py"),
        *(ROOT / "experiments/structural_discrimination").glob("*.py"),
        *(ROOT / "experiments/structural_discrimination/stage_b").glob("*.py"),
        *(ROOT / "experiments/structural_discrimination/stage_c").glob("*.py"),
        ROOT / "experiments/codex_dogfood/case_0009/artifacts.py",
        ROOT / "experiments/codex_dogfood/case_0015/freeze.py",
        ROOT / "experiments/codex_dogfood/case_0015/protocol.py",
        ROOT / "experiments/codex_dogfood/case_0016/stage_b/durability.py",
        ROOT / "experiments/bm25f/fields.py",
        ROOT / "experiments/bm25f/scoring.py",
        ROOT / "experiments/exact_hint_routing/behavior.py",
        ROOT / "experiments/exact_hint_routing/serialization.py",
        *(
            p
            for p in (ROOT / "experiments/orchestration").rglob("*.py")
            if "tests" not in p.parts
        ),
        ROOT
        / "experiments/orchestration/engineering/host_disclosure/smoke-receipt.json",
    }
    return {
        p.relative_to(ROOT).as_posix(): digest(p.read_bytes())
        for p in sorted(paths)
        if "__pycache__" not in p.parts
    }


async def cards() -> list[Any]:
    """Authenticate public records only; never call population administration."""
    for name, expected in (
        ("population_freeze.json", POPULATION_SHA),
        ("selection_provenance.json", SELECTION_SHA),
    ):
        raw = await git("show", START + ":" + POPULATION + name)
        require(
            digest(raw) == expected and (ROOT / POPULATION / name).read_bytes() == raw,
            "Public population authentication",
        )
    selected: list[Any] = json.loads(
        (ROOT / POPULATION / "population_freeze.json").read_bytes()
    )["selected_development_tasks"]
    selected = [selected[CASES[case]["position"] - 1] for case in CASES]
    for case, card in zip(CASES, selected, strict=True):
        require(
            card["selection_position"] == CASES[case]["position"]
            and card["case_id"]
            == f"historical-development-{CASES[case]['position']:03}",
            "Frozen cohort order",
        )
        require(
            digest(card["task_text"].encode()) == card["task_source"]["task_sha256"],
            "Task hash",
        )
    return selected


def frame_contract(card: Any, metadata: Any, rows: Any) -> Any:
    """Authenticate complete native identities using the standalone packet codec."""
    require(
        metadata["source_head"] == card["frame"]["parent_commit"]
        and metadata["source_tree"] == card["frame"]["parent_tree"],
        "Parent identity",
    )
    require(
        metadata["resource_count"] == len(rows)
        and metadata["python_resource_count"]
        == sum(r["address"].endswith(".py") for r in rows),
        "Frame counts",
    )
    require(
        metadata["resources"]
        == [{k: v for k, v in r.items() if k != "content"} for r in rows],
        "Complete metadata resource bindings",
    )
    frame = {k: metadata[k] for k in ("repository_id", "snapshot_id", "corpus_id")}
    frame["parent_tree"] = metadata["source_tree"]
    for r in rows:
        require(
            all(
                r[k] == frame[k] for k in ("repository_id", "snapshot_id", "corpus_id")
            ),
            "Resource frame",
        )
        reviewer.source({k: r[k] for k in reviewer.SOURCE}, frame)
        require(
            digest(r["content"].encode()) == r["source_blob_sha256"],
            "Parent byte identity",
        )
    require(
        [r["address"] for r in rows] == sorted({r["address"] for r in rows}),
        "Ordered complete frame",
    )
    pairs = tuple(x for r in rows for x in (r["address"], r["content_identity"]))
    require(
        frame["snapshot_id"]
        == reviewer.semantic(
            "explicit-required-text-resources-sha256-v1",
            frame["repository_id"],
            *pairs,
        )
        and frame["corpus_id"]
        == reviewer.semantic(
            "selected-observed-utf8-resource-occurrences-sha256-v1",
            frame["repository_id"],
            *pairs,
        ),
        "Native complete frame identity",
    )
    return frame


async def prepared(card: Any) -> tuple[Any, Any]:
    """Cache exact serialized observation only; reauthenticate parent on every hit."""
    before = time.perf_counter_ns()
    implementation = implementations()
    binding = {
        "schema": "immutable-preparation-v1",
        "parent_tree": card["frame"]["parent_tree"],
        "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
        "observation_semantics": "case-0015-retained-whole-resource-observation-v1",
        "implementation": implementation,
        "configuration": {
            "scope": "case_0015.freeze.eligible",
            "maximum_resource_bytes": 1 << 20,
            "resource_limit": 10000,
            "traversal_limit": 20000,
        },
        "surfaces": ["frame.json", "resources.json.gz"],
    }
    cache = PreparationCache(ROOT / ".local/source-grounding-frame-cache")
    event, files = cache.get(binding)
    blobs, objects = await parent_blobs(card)
    try:
        if files is not None:
            metadata = json.loads(files["frame.json"])
            rows = json.loads(gzip.decompress(files["resources.json.gz"]))
            frame_contract(card, metadata, rows)
            require(
                {r["address"]: r["content"].encode() for r in rows} == blobs
                and {r["address"]: r["git_blob_oid"] for r in rows} == objects,
                "Cache source correspondence",
            )
    except (ValueError, KeyError, TypeError, OSError):
        event, files = "CACHE_REJECTED", None
    if files is None:
        metadata, rows = await observe(card)
        frame_contract(card, metadata, rows)
        files = {
            "frame.json": json_bytes(metadata),
            "resources.json.gz": gzip.compress(json_bytes(rows), mtime=0),
        }
        cache.put(binding, files)
    print(
        json.dumps(
            {
                "preparation": card["case_id"],
                "event": event,
                "recomputed": event != "CACHE_HIT",
                "cache_key": cache.key(binding),
                "bytes": sum(len(v) for v in files.values()),
                "elapsed_ns": time.perf_counter_ns() - before,
                "implementation_sha256": digest(json_bytes(implementation)),
            },
        ),
        flush=True,
    )
    return metadata, rows


def protocol() -> Any:
    """Bind the scientific clauses and launcher/analysis contracts without results."""
    from experiments.source_grounding.workers import configuration

    return {
        "schema": "purpose-relative-source-grounding-stage-a-v1",
        "status": STATUS,
        "supersession": {
            "prior_stage_a": "f03523e2d06150e4497b038a49c20885db956810",
            "engineering_checkpoint": "3f49fd359b767701ad43796d8fc247e2182841d1",
            "invalidation_checkpoint": "f25daa62edc8a79584aca4347fa58d86ede865f6",
            "reason": "0020/0021 infrastructure-invalidated; 0022 scientifically unentered; next untouched public positions 7/8",
            "scientific_hypothesis": "UNCHANGED",
            "semantic_labels_and_canonical_spans": "UNCHANGED",
            "disclosure_content_meaning": "UNCHANGED",
            "runtime_delivery": "HOST_STDIN_DISCLOSURE; TOOL_FREE_STRUCTURED_RESPONSE",
            "evidence_representation": "MODEL_CHOOSES_EXACT_QUOTE_AND_OVERLAPPING_OCCURRENCE; HOST_DERIVES_IDENTITY_AND_UNICODE_BOUNDS; NO_REPAIR",
            "case_0022": "EXACT_SIX_ORIGINAL_FILES_REUSED; ORIGINAL_PROTOCOL_DIGEST_RETAINED; GLOBAL_EXECUTION_BINDING_SUPERSEDED",
            "failed_semantic_judgments_used": False,
            "gold_access": False,
            "child_access": False,
            "confirmation_reserve_access": False,
        },
        "cases": list(CASES),
        "population_sha256": POPULATION_SHA,
        "design": "README.md",
        "design_sha256": digest((PACKAGE / "README.md").read_bytes()),
        "grounding_instructions_sha256": digest(
            (PACKAGE / "INSTRUCTIONS_GROUNDING.md").read_bytes(),
        ),
        "gold_instructions_sha256": digest(
            (PACKAGE / "INSTRUCTIONS_GOLD.md").read_bytes(),
        ),
        "grounding_model": {
            "model": "GPT-6 Sol",
            "model_id": "gpt-6-sol",
            "reasoning": "High",
        },
        "gold_model": {
            "model": "GPT-6 Astra",
            "model_id": "gpt-6-astra",
            "reasoning": "High",
        },
        "launcher": {"cli_version": "0.162.1", "fresh": True, "continuation": False},
        "workers": {"grounding": configuration("Sol"), "gold": configuration("Astra")},
        "baseline": {
            "analysis": "unicode-word-span-casefold-v1",
            "k1": 1.2,
            "b": 0.75,
            "filename_weight": 0.25,
            "positive_universe": "complete",
            "exact_route": "NOT_APPLICABLE",
        },
        "grounding_verdicts": list(reviewer.VERDICTS),
        "gold_labels": list(reviewer.LABELS),
        "retry": "NEVER_SCIENTIFIC",
        "ranking_modifications": 0,
        "cohort_gate": None,
        "worker_timeout": 21600,
        "grounding_timeout": 7200,
        "validation_timeout": 3600,
        "grace": 10,
        "concurrency": {
            "cases": 3,
            "workers": 3,
            "semantic": 1,
            "maximum_total_model_workers_including_nested_grounding": 3,
        },
        "no_execution": dict.fromkeys(
            (
                "retrieval",
                "references",
                "grounding_workers",
                "gold_workers",
                "gold",
                "stage_d",
                "scientific_entered",
                "approval",
            ),
            0,
        ),
    }


async def build() -> dict[str, bytes]:
    """Derive only Stage A files from authenticated public/parent inputs."""
    files = {STAGE_A_PREFIX + "protocol.json": json_bytes(protocol())}
    cohort = []
    for case, card in zip(CASES, await cards(), strict=True):
        authored = CASES[case]
        metadata, rows = await prepared(card)
        frame = frame_contract(card, metadata, rows)
        by = {r["address"]: r for r in rows}
        require(
            set(authored["basis"]) <= set(by),
            "Authoring basis absent from own parent",
        )
        obligations = [
            {
                **o,
                "gap": authored["gap"],
                "information_need_identity": f"N{i}",
                "obligation_identity": {
                    "task": f"case-{case}:{card['case_id']}",
                    "value": o["id"],
                },
                "query_identity": {
                    "task": f"case-{case}:{card['case_id']}",
                    "value": f"Q{i}",
                },
                "routing": "LEXICAL",
                "exact_route": "NOT_APPLICABLE",
            }
            for i, o in enumerate(authored["obligations"], 1)
        ]
        design = {
            "schema": "source-grounding-case-stage-a-v1",
            "case": case,
            "population": card,
            "task_text": card["task_text"],
            "task_identity": f"case-{case}:{card['case_id']}",
            "frame": frame,
            "parent_frame": {k: v for k, v in metadata.items() if k != "resources"},
            "obligations": obligations,
            "authoring_basis": {
                p: by[p]["source_blob_sha256"] for p in authored["basis"]
            },
            "status": STATUS,
            "protocol_sha256": digest(json_bytes(protocol())),
        }
        prefix = f"experiments/codex_dogfood/case_{case}/"
        generated = {
            prefix + "protocol.json": json_bytes(design),
            prefix + "frame.json": json_bytes(metadata),
            prefix + "resources.json.gz": gzip.compress(json_bytes(rows), mtime=0),
            prefix + "task.txt": card["task_text"].encode(),
            prefix + "README.md": (
                f"# Case {case}: prospective source grounding\n\nFROZEN / NOT_AUTHORIZED / NOT_EXECUTED.\n\nSee ../../source_grounding/README.md and protocol.json. Exact parent resources only; no child/gold/treatment.\n"
            ).encode(),
            prefix
            + ".gitattributes": b"*.json -text\n*.gz -text\n*.txt -text\n*.md text eol=lf\n",
        }
        if case == "0022":
            # Reuse all original scientific authoring and parent bytes exactly.
            for name in generated:
                raw = await git(
                    "show", "f25daa62edc8a79584aca4347fa58d86ede865f6:" + name
                )
                require((ROOT / name).read_bytes() == raw, "Reused 0022 bytes changed")
                generated[name] = raw
            old = json.loads(generated[prefix + "protocol.json"])
            require(
                old["population"] == card
                and old["frame"] == frame
                and old["obligations"] == obligations
                and old["authoring_basis"] == design["authoring_basis"],
                "0022 scientific authoring changed",
            )
        files.update(generated)
        cohort.append(
            {
                "case": case,
                "public_position": authored["position"],
                "population_case": card["case_id"],
                "task": card["task_text"],
                "parent_commit": card["frame"]["parent_commit"],
                "frame": frame,
                "resources": len(rows),
                "python_resources": metadata["python_resource_count"],
            },
        )
    files[STAGE_A_PREFIX + "cohort.json"] = json_bytes(cohort)
    files[STAGE_A_PREFIX + "validation.json"] = json_bytes(
        {
            "status": "PASS",
            "population": "PUBLIC_ONLY_AUTHENTICATED",
            "parent_observation": "PASS",
            "scientific_execution": "NOT_STARTED",
            "deterministic_contract_tests": "PASS; focused contracts/runtime/static-scope; see REPLACEMENT_STAGE_A_REVIEW.md",
        },
    )
    files[STAGE_A_PREFIX + "integrity.json"] = json_bytes(
        {
            "schema": "source-grounding-stage-a-integrity-v1",
            "artifacts": {n: digest(v) for n, v in files.items()},
            "implementation": implementations(),
        },
    )
    return files


async def main() -> None:
    """Create once or replay exact Stage A; never create a run plan here."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "verify"))
    args = parser.parse_args()
    files = await build()
    if args.mode == "build":
        require(
            not any(
                (ROOT / n).exists()
                for n in files
                if not n.startswith("experiments/codex_dogfood/case_0022/")
            ),
            "Stage A overwrite refused",
        )
        for name, raw in files.items():
            if not name.startswith("experiments/codex_dogfood/case_0022/"):
                put_binary(ROOT / name, raw)
    else:
        require(
            all((ROOT / n).read_bytes() == raw for n, raw in files.items()),
            "Deterministic Stage A replay differs",
        )
    print(
        json.dumps(
            {
                "status": "PASS",
                "mode": args.mode,
                "artifacts": len(files),
                "scientific_execution": "NOT_STARTED",
            },
        ),
    )


if __name__ == "__main__":
    asyncio.run(main())
