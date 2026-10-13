# Copyright (c) 2026
# ruff: noqa: ANN401, EM101, TRY003, E501, T201, B023, PLR0915, TRY300, TRY301 -- fixed scientific failure boundary
"""Capture all three cases once, then sealed verification; never gold or a retry."""

from __future__ import annotations

import argparse
import asyncio
import gzip
import json
import math
import platform
import statistics
import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

from devtools.context.python.references import derive_python_declaration_references
from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.core.time import Timestamp
from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    binary,
    digest,
    json_bytes,
    put_binary,
    put_text,
)
from experiments.codex_dogfood.case_0012.stage_b.durability import exclusive
from experiments.codex_dogfood.case_0015.stage_b.execute import prepare, prepare_fields
from experiments.codex_dogfood.verification.journal import journal_type
from experiments.codex_dogfood.verification.native import NativeMemo
from experiments.codex_dogfood.verification.proof import CHECKS, publish_proof
from experiments.structural_discrimination import freeze
from experiments.structural_discrimination.evidence import annotate, prepare_references
from experiments.structural_discrimination.stage_b import (
    authentication,
    capture,
    reporting,
)


def progress(  # noqa: PLR0913, PLR0917 -- operational progress record only
    case: str,
    phase: str,
    operation: str,
    count: int,
    total: int,
    start: int,
) -> None:
    """Operational progress must never veto an authoritative returned value."""
    value = {
        "timestamp": Timestamp.now().isoformat(),
        "case": case,
        "phase": phase,
        "operation": operation,
        "count": count,
        "total": total,
        "elapsed_ns": time.perf_counter_ns() - start,
    }
    try:
        with (ROOT / ".local" / "direct-discrimination-progress.jsonl").open(
            "a",
            encoding="utf8",
        ) as stream:
            stream.write(json_bytes(value).decode().replace("\n", " ") + "\n")
        if not operation.startswith("ri:references:") or count % 20 == 0:
            print(json.dumps(value), flush=True)
    except (OSError, UnicodeError):
        pass


def ablation(values: Any, prepared: Any) -> Any:
    """Empty-channel validation only; no primary treatment or scoring repeated."""
    empty = prepare_references(prepared.snapshot, ())
    for i in range(1, 4):
        surface = values[f"query:Q{i}:annotation"]["result"]
        result = annotate(
            empty,
            obligation=surface.obligation,
            query=surface.query,
            purpose=surface.purpose,
            lexical_result=surface.lexical_result,
        )
        if result.annotations or result.lexical_result is not surface.lexical_result:
            raise ValueError("Structural ablation changed A")
    return {
        "status": "PASS",
        "primary_annotation_passes": 3,
        "empty_reference_validation_ablations": 3,
        "ranking_side_effect": "NONE",
    }


def write_files(root: Path, files: Any) -> None:
    """Exclusive canonical publication through existing artifact substrates."""
    if any((root / name).exists() for name in files):
        raise FileExistsError("Scientific artifact overwrite refused")
    for name, raw in files.items():
        if name.endswith(".gz"):
            put_binary(root / name, raw)
        else:
            put_text(root / name, raw.decode())


def execute_case(case: str, design: Any, rows: Any, plan: Any) -> Any:  # noqa: C901 -- fixed scientific operation composition
    """Refuse every reuse of a claimed execution identity."""
    root = capture.capture_root(case)
    start = time.perf_counter_ns()
    implementation = capture.source_hashes()
    frame_binding = {
        k: design["parent_frame"][k]
        for k in ("repository_id", "snapshot_id", "corpus_id")
    }
    marker = {
        "schema": "direct-discrimination-execution-v1",
        "case": case,
        "execution": plan["execution"],
        "stage_a_checkpoint": capture.STAGE_A,
        "protocol_sha256": design["shared_protocol_sha256"],
        "schedule_sha256": digest(json_bytes(plan)),
        "frame": frame_binding,
        "runtime": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
        },
        "implementation": implementation,
        "operations": plan["operations"],
        "design": design,
        "stage_a_artifacts": {
            name: digest(binary(capture.case_root(case) / name))
            for name in (
                "protocol.json",
                "frame.json",
                "resources.json.gz",
                "blind_spec.json",
                "task.txt",
            )
        },
    }
    journal = capture.Journal.start(root, marker)
    exclusive(root / "operation_schedule.json", plan)
    journal.context({})
    sequence = 0

    def call(identity: str, inputs: Any, invoke: Any) -> Any:
        nonlocal sequence
        if plan["operations"][sequence] != identity:
            raise ValueError("Prospective operation order differs")
        progress(case, "ENTERING", identity, sequence, len(plan["operations"]), start)
        result = journal.call(identity, inputs, invoke)
        sequence += 1
        progress(case, "RETURNED", identity, sequence, len(plan["operations"]), start)
        return result

    try:
        frame = call(
            "frame:prepare",
            {"stage_a": marker["stage_a_artifacts"], "frame": frame_binding},
            lambda: prepare(rows, design["parent_frame"]),
        )
        fields = call(
            "lexical:fields",
            {"frame": frame_binding},
            lambda: prepare_fields(frame),
        )
        retained_index = call(
            "lexical:index",
            {"k1": 1.2, "b": 0.75, "filename_weight": 0.25},
            lambda: capture.index(fields),
        )
        universe = call(
            "ri:module-universe",
            {"roots": ["src", "."], "root_preference": False},
            lambda: capture.universe(frame.snapshot),
        )
        analyses = {}
        source_interpretations: dict[str, list[Any]] = {}
        for interpreted in universe.interpretations:
            source_interpretations.setdefault(
                str(interpreted.resource.address),
                [],
            ).append(interpreted)
        for row in rows:
            address = row["address"]
            if address.endswith(".py"):
                analyses[address] = call(
                    "ri:references:" + address,
                    {"source": address, "content_identity": row["content_identity"]},
                    lambda: derive_python_declaration_references(
                        frame.snapshot,
                        resource_address=RepositoryResourceAddress(address),
                        module_universe=universe,
                        source_interpretations=tuple(
                            source_interpretations.get(address, ()),
                        ),
                    ),
                )
        prepared = call(
            "references:prepare",
            {"sources": len(analyses), "frame": frame_binding},
            lambda: prepare_references(
                frame.snapshot,
                tuple(f for result in analyses.values() for f in result.references),
            ),
        )
        for i, obligation in enumerate(design["obligations"], 1):
            prefix = f"query:Q{i}:"
            binding = {
                "obligation": obligation["obligation_identity"],
                "query": obligation["query_identity"],
                "text": obligation["query"],
            }
            acquired = call(
                prefix + "A",
                binding,
                lambda: capture.acquire(obligation["query"], retained_index, len(rows)),
            )
            annotation = call(
                prefix + "annotation",
                binding,
                lambda: capture.annotation(
                    prepared,
                    acquired["result"],
                    design,
                    obligation,
                ),
            )
            pair_return = call(
                prefix + "pairs",
                binding,
                lambda: capture.pairs(annotation["result"]),
            )
            call(
                prefix + "validate",
                binding,
                lambda: capture.validate_surface(
                    prepared,
                    annotation["result"],
                    pair_return["result"],
                ),
            )
        call(
            "annotation:ablation",
            {"channel": "empty References; exact A retained"},
            lambda: ablation(journal.state["values"], prepared),
        )
        call(
            "capture:validate",
            {"sources": len(analyses)},
            lambda: capture.validate_references(frame, analyses, prepared),
        )
        if sequence != len(plan["operations"]):
            raise ValueError("Incomplete scientific schedule")
        journal.complete()
        files = reporting.derive(marker, journal.state["values"])
        files["capture_costs.json"] = json_bytes(
            {
                "native_capture_wall_ns": time.perf_counter_ns() - start,
                "journal_durability_ns": journal.overhead_ns,
                "online_samples": 3,
                "timing_observer": "one frozen annotate line boundary; observer overhead included",
                "timing_exclusions": "offline frame/index/RI, journal, serialization, proof, reports/hash/Git",
            },
        )
        write_files(root, files)
        hashes = {
            p.relative_to(root).as_posix(): digest(p.read_bytes())
            for p in sorted(root.rglob("*"))
            if p.is_file()
        }
        inputs = authentication.bindings(root, hashes, implementation)
        deep_start = time.perf_counter_ns()

        def prove() -> bytes:
            memo = NativeMemo()
            memo.on_envelope = lambda: (
                progress(
                    case,
                    "DEEP_CORRESPONDENCE",
                    "native/canonical",
                    memo.envelopes,
                    len(plan["operations"]) + 1,
                    deep_start,
                )
                if memo.envelopes % 20 == 0
                else None
            )
            replay = journal_type(memo).load(root)
            expected = reporting.derive(replay.state["marker"], replay.state["values"])
            if replay.state["state"] != "NATIVE_CAPTURE_COMPLETE" or any(
                (root / p).read_bytes() != raw for p, raw in expected.items()
            ):
                raise ValueError("Deep scientific reconstruction differs")
            return json_bytes(
                {"status": "PASS", "checks": dict.fromkeys(CHECKS, "PASS")},
            )

        progress(
            case,
            "DEEP_PROOF_STARTED",
            "finalization",
            sequence,
            sequence,
            deep_start,
        )
        publish_proof(root / "completion_proof.json", inputs, prove)
        # The proof's own bytes are anchored outside its acyclic input bindings.
        hashes["completion_proof.json"] = digest(
            (root / "completion_proof.json").read_bytes(),
        )
        exclusive(
            root / "integrity.json",
            {
                "schema": "direct-discrimination-capture-integrity-v1",
                "execution": marker["execution"],
                "sha256": hashes,
                "implementation": implementation,
            },
        )
        result = authentication.sealed(root, (root / "integrity.json").read_bytes())
        progress(
            case,
            "PREPUBLICATION_SEALED_PASS",
            "finalization",
            sequence,
            sequence,
            start,
        )
        return result
    except BaseException as error:
        if not (root / "capture_failure.json").exists():
            exclusive(
                root / "capture_failure.json",
                {
                    "execution": plan["execution"],
                    "status": "FAILED; IDENTITY DEAD; NO RETRY",
                    "error_type": type(error).__qualname__,
                    "error": str(error),
                    "active": journal.state["active"],
                    "returned_operations": [
                        o["identity"]
                        for o in journal.state["operations"]
                        if o["status"] == "RETURNED"
                    ],
                    "last_chain_sha256": journal.chain,
                },
            )
        raise


async def capture_all() -> Any:
    """All schedules frozen before first claim, no case result can change another."""
    await freeze.verify(capture.STAGE_A)
    if any(capture.capture_root(case).exists() for case in capture.CASES):
        raise FileExistsError("A cohort execution identity already exists; no retry")
    designs, resources, plans = {}, {}, {}
    for case in capture.CASES:
        root = capture.case_root(case)
        if any(
            (root / name).exists()
            for name in ("adjudication", "stage_d", "stage_c/packet")
        ):
            raise ValueError("Premature gold/packet/result contamination")
        designs[case] = json.loads(binary(root / "protocol.json"))
        resources[case] = json.loads(
            gzip.decompress(binary(root / "resources.json.gz")),
        )
        plans[case] = capture.schedule(case, resources[case])
        schedule_path = root / "stage_b/operation_schedule.json"
        if schedule_path.exists():
            raise FileExistsError("Operation schedule already frozen")
    for case in capture.CASES:
        put_text(
            capture.case_root(case) / "stage_b/operation_schedule.json",
            json_bytes(plans[case]).decode(),
        )
    results = [
        execute_case(case, designs[case], resources[case], plans[case])
        for case in capture.CASES
    ]
    summaries = [result["summary"] for result in results]
    timing_samples = [
        query["timings"]["complete_online_equivalent_ns"]
        for summary in summaries
        for query in summary["queries"]
    ]
    totals = {
        "a_candidate_occurrences": sum(
            query["a_results"] for summary in summaries for query in summary["queries"]
        ),
        "positive_native_references": sum(
            summary["ri"]["positive_references"] for summary in summaries
        ),
        "cross_resource_reference_occurrences": sum(
            summary["ri"]["cross_resource_references"] for summary in summaries
        ),
        "direct_cross_resource_pairs": sum(
            summary["ri"]["direct_cross_resource_pairs"] for summary in summaries
        ),
        "qualifying_support_occurrences": sum(
            query["qualifying_occurrences"]
            for summary in summaries
            for query in summary["queries"]
        ),
        "support_source_target_pairs": sum(
            query["support_source_target_pairs"]
            for summary in summaries
            for query in summary["queries"]
        ),
        "supported_target_occurrences": sum(
            query["supported_targets"]
            for summary in summaries
            for query in summary["queries"]
        ),
        "local_predecessor_pairs": sum(
            query["local_pairs"]
            for summary in summaries
            for query in summary["queries"]
        ),
    }
    cohort = {
        "status": "ALL_THREE_CAPTURED; NO GOLD; NO SCIENTIFIC INTERPRETATION",
        "stage_a_checkpoint": capture.STAGE_A,
        "cases": results,
        "totals": totals,
        "online_equivalent": {
            "samples_ns": timing_samples,
            "n": len(timing_samples),
            "median_ns": statistics.median(timing_samples),
            "p95_ns": sorted(timing_samples)[math.ceil(0.95 * len(timing_samples)) - 1],
            "p95_definition": "nearest rank; one scientific sample per obligation; mixed workload descriptive only",
        },
    }
    write_files(
        capture.PACKAGE,
        {
            "cohort_capture.json": json_bytes(cohort),
            "COHORT_REVIEW.md": (
                "# Cohort treatment capture\n\nMechanical only; no semantic labels or usefulness inference.\n\n```json\n"
                + json_bytes(cohort).decode()
                + "```\n"
            ).encode(),
        },
    )
    return cohort


async def verify_all(checkpoint: str) -> Any:
    """One Stage A authentication followed by normal sealed capture verification."""
    await freeze.verify(capture.STAGE_A)
    return {
        "cases": [
            await authentication.verify(case, checkpoint) for case in capture.CASES
        ],
        "native_archives_decoded": 0,
    }


def main() -> None:
    """No resume/retry or semantic adjudication entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("capture", "verify"))
    parser.add_argument("--checkpoint")
    args = parser.parse_args()
    if args.command == "verify" and not args.checkpoint:
        parser.error("Normal verify requires an externally authoritative checkpoint")
    result = asyncio.run(
        capture_all() if args.command == "capture" else verify_all(args.checkpoint),
    )
    print(json.dumps({"status": "PASS", "cases": len(result["cases"])}, indent=2))


if __name__ == "__main__":
    main()
