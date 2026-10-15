# Copyright (c) 2026
# ruff: noqa: ANN401, E501 -- exact experiment-owned native projection
"""Derive the complete BROAD pair universe from parent frames, never treatment."""

from typing import Any

from devtools.context.python.references import derive_python_declaration_references
from devtools.context.repository.resource import RepositoryResourceAddress
from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.codex_dogfood.case_0015.stage_b.execute import prepare, prepare_fields
from experiments.orchestration.storage import require
from experiments.source_grounding import capture, contracts
from experiments.structural_discrimination.evidence import prepare_references
from experiments.structural_discrimination.stage_b import capture as native


def mechanical(design: Any, rows: Any) -> Any:
    """Compose existing deterministic B components without a scientific journal.

    This is prospective candidate generation, not B execution: there is no
    grounding callback, treatment judgment, qualification or scientific entry.
    """
    frame = prepare(rows, design["parent_frame"])
    index = native.index(prepare_fields(frame))
    modules = native.universe(frame.snapshot)
    by: dict[str, list[Any]] = {}
    for item in modules.interpretations:
        by.setdefault(str(item.resource.address), []).append(item)
    analyses = {
        row["address"]: derive_python_declaration_references(
            frame.snapshot,
            resource_address=RepositoryResourceAddress(row["address"]),
            module_universe=modules,
            source_interpretations=tuple(by.get(row["address"], ())),
        )
        for row in rows
        if row["address"].endswith(".py")
    }
    refs = prepare_references(
        frame.snapshot,
        tuple(f for r in analyses.values() for f in r.references),
    )
    values = {
        "frame": frame,
        "references": refs,
        **{"ri:" + a: r for a, r in analyses.items()},
    }
    for o in design["obligations"]:
        a = native.acquire(o["query"], index, len(rows))
        surface = native.annotation(refs, a["result"], design, o)
        values[o["id"] + ":A"] = a
        values[o["id"] + ":annotation"] = surface
        values[o["id"] + ":pairs"] = native.pairs(surface["result"])
    broad = capture.projection(design, values)
    for q in broad["queries"]:
        q.pop("timings")
    contracts.validate_channels(broad, rows)
    return broad


def build(design: Any, rows: Any, broad: Any) -> Any:
    """One source-target-obligation pair, retaining every supporting occurrence."""
    contracts.validate_channels(broad, rows)
    by = {r["address"]: r for r in rows}
    facts = {f["fact_identity"]: f for f in broad["facts"]}
    units = []
    for q in broad["queries"]:
        for target in q["broad"]:
            for source in target["sources"]:
                unit = {
                    "case": design["case"],
                    "obligation_id": q["obligation"],
                    "source": contracts.endpoint(by[source["source"]]),
                    "target": contracts.endpoint(by[target["target"]]),
                    "source_a_position": source["rank"],
                    "target_a_position": target["rank"],
                    "references": [facts[f] for f in source["facts"]],
                }
                units.append({"identity": digest(json_bytes(unit)), **unit})
    units.sort(
        key=lambda u: (
            u["obligation_id"],
            u["source"]["address"],
            u["target"]["address"],
        ),
    )
    require(
        len({u["identity"] for u in units}) == len(units),
        "Duplicate candidate identity",
    )
    value = {
        "schema": "broad-candidate-discrimination-universe-v1",
        "case": design["case"],
        "frame": design["frame"],
        "analysis_unit": "SOURCE_TARGET_OBLIGATION_PAIR",
        "occurrences": "All distinct native fact identities retained; no occurrence weighting",
        "units": units,
    }
    return {**value, "sha256": digest(json_bytes(value))}
