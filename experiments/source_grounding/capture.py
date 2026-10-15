# Copyright (c) 2026
# ruff: noqa: COM812, ANN401, PLR2004, PLR0915, PLR0913 -- fixed scientific capture composition
"""Future once-only B adapter. Importing this module executes no science."""

from __future__ import annotations

import asyncio
import base64
import platform
from pathlib import Path
from typing import Any

from devtools.context.python.references import derive_python_declaration_references
from devtools.context.repository.resource import RepositoryResourceAddress
from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes, put_binary
from experiments.codex_dogfood.case_0015.stage_b.execute import prepare, prepare_fields
from experiments.codex_dogfood.verification.journal import journal_type
from experiments.codex_dogfood.verification.native import NativeMemo
from experiments.codex_dogfood.verification.proof import (
    CHECKS,
    CompletionBindings,
    authenticate_proof,
    publish_proof,
)
from experiments.orchestration.observation import append_operational
from experiments.orchestration.storage import bundle, load, require
from experiments.source_grounding import contracts
from experiments.structural_discrimination.evidence import prepare_references
from experiments.structural_discrimination.stage_b import capture
from experiments.structural_discrimination.stage_b.reporting import fact_row


def projection(design: Any, values: Any) -> Any:
    """Derive complete canonical BROAD projections from captured native returns."""
    frame = values["frame"]
    references = values["references"]
    ri = capture.validate_references(
        frame,
        {k.removeprefix("ri:"): v for k, v in values.items() if k.startswith("ri:")},
        references,
    )
    queries = []
    for obligation in design["obligations"]:
        prefix = obligation["id"]
        acquired = values[prefix + ":A"]
        annotated = values[prefix + ":annotation"]
        surface = annotated["result"]
        lexical = acquired["result"]
        require(surface.lexical_result is lexical, "Native A identity")
        require(
            lexical.query.text == obligation["query"]
            and lexical.maximum_results == design["parent_frame"]["resource_count"]
            and lexical.settings.k1 == 1.2
            and lexical.settings.b == 0.75,
            "Canonical A configuration",
        )
        capture.validate_surface(
            references,
            surface,
            values[prefix + ":pairs"]["result"],
        )
        a = [
            {
                **capture.identity(
                    m.document_statistics.analysis.document.resource,
                    m.document_statistics.analysis.document.id,
                    i,
                ),
                "score": m.score,
                "content_score": m.content_score,
                "filename_score": m.filename_score,
                "filename_weight": m.filename_weight,
            }
            for i, m in enumerate(lexical.matches, 1)
        ]
        broad = [
            {
                "target": str(t.resource.address),
                "rank": t.a_rank,
                "predecessor": a[t.a_rank - 2],
                "sources": [
                    {
                        "source": str(s.resource.address),
                        "rank": s.a_rank,
                        "facts": sorted(
                            support.fact.identity for support in s.supports
                        ),
                    }
                    for s in t.sources
                ],
            }
            for t in surface.annotations
        ]
        queries.append(
            {
                "obligation": prefix,
                "A": a,
                "broad": broad,
                "timings": {
                    "canonical_A_ns": acquired["online_ns"],
                    "projection_ns": annotated["online_ns"],
                    "pairs_ns": values[prefix + ":pairs"]["online_ns"],
                },
            },
        )
    return {
        "schema": "source-grounding-captured-B-v1",
        "case": design["case"],
        "frame": design["frame"],
        "facts": [fact_row(f) for f in references.facts],
        "queries": queries,
        "ri": ri,
        "rank_modifications": 0,
        "A_ablation": "PASS",
    }


def bindings(root: Path, hashes: Any) -> CompletionBindings:
    """Bind proof to physical native journal, projections, schedule and code."""
    marker = load(root / "native/execution_started.json")
    native = {n: h for n, h in hashes.items() if n.startswith("native/")}
    canonical = {
        n: h
        for n, h in hashes.items()
        if not n.startswith("native/") and n != "completion_proof.json"
    }
    return CompletionBindings.create(
        {
            "case": marker["case"],
            "execution": marker["execution"],
            "frame": {k: marker["frame"][k] for k in contracts.FRAME},
            "protocol_sha256": marker["protocol_sha256"],
            "schedule_sha256": digest(json_bytes(marker["operations"])),
            "journal_chain_sha256": digest(
                (root / "native/execution_completed.json").read_bytes(),
            ),
            "native_sha256": native,
            "canonical_sha256": canonical,
            "implementation_sha256": marker["implementation"],
            "verifier_sha256": {
                "capture.py": marker["implementation"].get(
                    "experiments/source_grounding/capture.py",
                    digest(Path(__file__).read_bytes()),
                )
            },
            "completion_sha256": native["native/execution_completed.json"],
        },
    )


def execute(
    root: Path,
    design: Any,
    rows: Any,
    grounding: Any,
    *,
    implementation: Any,
    run_binding: Any,
    grounding_preflight: Any = None,
) -> None:
    """One cohort-authorized B operation; never call this during Stage A."""
    operations = [
        "frame",
        "fields",
        "index",
        "universe",
        *("ri:" + r["address"] for r in rows if r["address"].endswith(".py")),
        "references",
        *(
            o["id"] + suffix
            for o in design["obligations"]
            for suffix in (":A", ":annotation", ":pairs")
        ),
        "grounding",
    ]
    journal = capture.Journal.start(
        root / "native",
        {
            "case": design["case"],
            "execution": run_binding["run_id"] + ":" + design["case"] + ":B",
            "run_binding": run_binding,
            "frame": design["frame"],
            "runtime": platform.python_version(),
            "protocol_sha256": design["protocol_sha256"],
            "implementation": implementation,
            "operations": operations,
            "design": design,
        },
    )
    journal.context({})
    position = 0

    def call(identity: str, inputs: Any, fn: Any) -> Any:
        nonlocal position
        require(identity == operations[position], "Prospective schedule")
        append_operational(
            root / "operational-progress.jsonl",
            {"operation": identity, "current": position, "total": len(operations)},
        )
        value = journal.call(identity, inputs, fn)
        position += 1
        return value

    frame = call(
        "frame",
        design["frame"],
        lambda: prepare(rows, design["parent_frame"]),
    )
    fields = call("fields", {}, lambda: prepare_fields(frame))
    index = call("index", {}, lambda: capture.index(fields))
    universe = call("universe", {}, lambda: capture.universe(frame.snapshot))
    interpreted: dict[str, list[Any]] = {}
    for item in universe.interpretations:
        interpreted.setdefault(str(item.resource.address), []).append(item)
    analyses = {}
    for row in rows:
        address = row["address"]
        if address.endswith(".py"):
            analyses[address] = call(
                "ri:" + address,
                contracts.endpoint(row),
                lambda address=address: derive_python_declaration_references(
                    frame.snapshot,
                    resource_address=RepositoryResourceAddress(address),
                    module_universe=universe,
                    source_interpretations=tuple(interpreted.get(address, ())),
                ),
            )
    references = call(
        "references",
        {},
        lambda: prepare_references(
            frame.snapshot,
            tuple(f for result in analyses.values() for f in result.references),
        ),
    )
    for obligation in design["obligations"]:
        prefix = obligation["id"]
        a = call(
            prefix + ":A",
            obligation,
            lambda obligation=obligation: capture.acquire(
                obligation["query"], index, len(rows)
            ),
        )
        surface = call(
            prefix + ":annotation",
            obligation,
            lambda a=a, obligation=obligation: capture.annotation(
                references, a["result"], design, obligation
            ),
        )
        call(
            prefix + ":pairs",
            {},
            lambda surface=surface: capture.pairs(surface["result"]),
        )
    broad = projection(design, journal.state["values"])
    contracts.validate_channels(broad, rows)
    grounding_input = contracts.grounding_packet(design, rows, broad)
    if grounding_preflight is not None:
        grounding_preflight(grounding_input)
    returned = call(
        "grounding",
        {"packet_sha256": digest(json_bytes(grounding_input))},
        lambda: asyncio.run(grounding(grounding_input)),
    )
    require(position == len(operations), "Incomplete scientific schedule")
    qualified = contracts.qualify(broad, returned["review"]["cells"])
    costs = []
    by = {r["address"]: r for r in rows}
    for query in qualified["queries"]:
        sources = {s["source"] for t in query["broad"] for s in t["sources"]}
        targets = {t["target"] for t in query["qualified"]}
        cells = [
            c
            for c in returned["review"]["cells"]
            if c["obligation"] == query["obligation"]
        ]
        costs.append(
            {
                "obligation": query["obligation"],
                "A_candidates": len(query["A"]),
                "A_candidate_bytes": sum(
                    len(by[r["address"]]["content"].encode()) for r in query["A"]
                ),
                "broad_sources": len(sources),
                "grounding_cells": len(cells),
                "source_content_bytes": sum(
                    len(by[a]["content"].encode()) for a in sources
                ),
                "verdicts": {
                    v: sum(c["verdict"] == v for c in cells) for v in contracts.VERDICTS
                },
                "broad_targets": len(query["broad"]),
                "qualified_targets": len(targets),
                "qualified_targets_not_grounding_sources": sorted(targets - sources),
                "qualified_target_bytes": sum(
                    len(by[a]["content"].encode()) for a in targets
                ),
                "timings": query["timings"],
            },
        )
    journal.complete()
    files = {
        "analysis_input.json": json_bytes(qualified),
        "grounding/packet.json": json_bytes(grounding_input),
        "grounding/review.json": json_bytes(returned["review"]),
        "costs.json": json_bytes({"obligations": costs, **returned["costs"]}),
    }
    files.update(
        {
            "grounding/primary/" + n: base64.b64decode(encoded, validate=True)
            for n, encoded in returned["files_b64"].items()
        },
    )
    for name, raw in files.items():
        put_binary(root / name, raw)
    hashes = {
        p.relative_to(root).as_posix(): digest(p.read_bytes())
        for p in (root / "native").rglob("*")
        if p.is_file()
    }
    hashes.update({n: digest(v) for n, v in files.items()})
    hashes.update(
        {
            n: digest((root / n).read_bytes())
            for n in ("design.json", "resources.json.gz")
        },
    )

    def prove() -> bytes:
        replay = journal_type(NativeMemo()).load(root / "native")
        require(
            replay.state["state"] == "NATIVE_CAPTURE_COMPLETE",
            "Incomplete native journal",
        )
        require(
            json_bytes(projection(design, replay.state["values"])) == json_bytes(broad),
            "Native projection correspondence",
        )
        require(
            json_bytes(
                contracts.qualify(
                    broad,
                    replay.state["values"]["grounding"]["review"]["cells"],
                ),
            )
            == files["analysis_input.json"],
            "Qualified correspondence",
        )
        return json_bytes({"status": "PASS", "checks": dict.fromkeys(CHECKS, "PASS")})

    publish_proof(root / "completion_proof.json", bindings(root, hashes), prove)
    hashes["completion_proof.json"] = digest(
        (root / "completion_proof.json").read_bytes(),
    )
    put_binary(
        root / "integrity.json",
        json_bytes({"schema": "source-grounding-B-integrity-v1", "sha256": hashes}),
    )


def sealed(root: Path, rows: Any) -> Any:
    """Authenticate the sealed proof without native decoding or reacquisition."""
    integrity = load(root / "integrity.json")
    hashes = integrity["sha256"]
    bundle(root, hashes)
    authenticate_proof(
        (root / "completion_proof.json").read_bytes(),
        hashes["completion_proof.json"],
        bindings(root, hashes),
    )
    capture_data = load(root / "analysis_input.json")
    contracts.validate_channels(capture_data, rows)
    expected = contracts.qualify(
        capture_data,
        load(root / "grounding/review.json")["cells"],
    )
    require(
        expected == capture_data
        and capture_data["rank_modifications"] == 0
        and capture_data["A_ablation"] == "PASS",
        "Qualified subset/A identity",
    )
    return {
        "status": "PASS",
        "mode": "SEALED",
        "native_archives_decoded": 0,
        "deep_correspondence_executions": 0,
        "completion_proof_sha256": hashes["completion_proof.json"],
    }
